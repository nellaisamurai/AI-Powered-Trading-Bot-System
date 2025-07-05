import os
import time
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
from trading_bot.ai_model import ai_decision
from trading_bot.logger import log_trade

# === Load env variables ===
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
USE_TESTNET = os.getenv("USE_TESTNET", "true").lower() == "true"
SYMBOLS = os.getenv("SYMBOLS", "").split(",")
COOLDOWN_SECONDS = int(os.getenv("COOLDOWN_SECONDS", 60))

# === Binance Client ===
client = Client(API_KEY, API_SECRET)
if USE_TESTNET:
    client.API_URL = "https://testnet.binance.vision/api"

# === Track cooldowns ===
last_trade_time = {symbol: 0 for symbol in SYMBOLS}

# === Utility to get precision for a symbol ===
def get_symbol_filters(symbol):
    try:
        info = client.get_symbol_info(symbol)
        if not info:
            raise Exception(f"Symbol {symbol} not found.")
        filters = {f['filterType']: f for f in info['filters']}
        return filters
    except Exception as e:
        print(f"⚠️ Error fetching filters for {symbol}: {e}")
        return {}

def round_quantity(symbol, quantity):
    filters = get_symbol_filters(symbol)
    step_size = float(filters.get('LOT_SIZE', {}).get('stepSize', 1))
    precision = abs(round(-1 * (step_size).as_integer_ratio()[1].bit_length() / 3.32193))
    return round(float(quantity), int(precision))

# === Trade Execution ===
def place_order(symbol: str, side: str):
    try:
        max_qty_key = f"MAX_POSITION_SIZE_{symbol.replace('USDT', '')}"
        max_qty = float(os.getenv(max_qty_key, os.getenv("MAX_POSITION_SIZE", "0.01")))
        quantity = round_quantity(symbol, max_qty)
        print(f"Placing {side} order for {symbol} with qty: {quantity}")

        order = client.create_order(
            symbol=symbol,
            side=SIDE_BUY if side == "BUY" else SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"✅ Order placed for {symbol}: {order['status']}")
        return order
    except Exception as e:
        print(f"❌ Failed to place order for {symbol}: {e}")
        return None

# === Signal Handler ===
def handle_signal(signal: dict):
    for symbol in SYMBOLS:
        now = time.time()
        if now - last_trade_time[symbol] < COOLDOWN_SECONDS:
            print(f"⏳ Skipping {symbol} due to cooldown.")
            continue

        signal['symbol'] = symbol
        print(f"\n📥 Processing signal for {symbol}: {signal}")

        decision = ai_decision(signal)
        print(f"🤖 AI Decision for {symbol}: {decision}")

        if decision in ["BUY", "SELL"]:
            order = place_order(symbol, decision)
            if order:
                signal['side'] = decision
                signal['price'] = order['fills'][0]['price'] if order.get("fills") else "0"
                log_trade(signal)
                last_trade_time[symbol] = now
        else:
            print(f"⚠️ No trade for {symbol}, decision = {decision}")

# === Manual test ===
if __name__ == "__main__":
    test_signal = {
        "rsi": 28.7,
        "macd": -0.021,
        "ema_diff": 1.1,
        "bb_width": 0.035,
        "stoch": 17.0
    }
    handle_signal(test_signal)

