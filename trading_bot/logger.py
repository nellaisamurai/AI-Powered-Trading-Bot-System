import logging
import sqlite3
from datetime import datetime

# === Logging to file ===
logging.basicConfig(
    filename="trading_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === SQLite Setup ===
conn = sqlite3.connect("trades.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    symbol TEXT,
    side TEXT,
    price REAL,
    rsi REAL,
    macd REAL
)
""")
conn.commit()

def log_trade(signal):
    logging.info(f"Trade executed: {signal}")
    cursor.execute("""
        INSERT INTO trades (timestamp, symbol, side, price, rsi, macd)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        signal.get("symbol", "N/A"),
        signal.get("side", "N/A"),
        float(signal.get("price", 0)),
        float(signal.get("rsi", 0)),
        float(signal.get("macd", 0))
    ))
    conn.commit()
