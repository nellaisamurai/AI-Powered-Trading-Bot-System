import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
use_testnet = os.getenv("USE_TESTNET", "true").lower() == "true"

client = Client(api_key, api_secret)

if use_testnet:
    client.API_URL = 'https://testnet.binance.vision/api'

def place_market_order(symbol, side, quantity):
    return client.create_order(
        symbol=symbol,
        side=side.upper(),
        type="MARKET",
        quantity=quantity
    )
