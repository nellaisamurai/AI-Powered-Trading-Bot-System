# 🤖 AI-Powered Trading Bot System

An intelligent crypto trading bot built with Python, Binance Testnet, TradingView Webhooks, and FastAPI. Uses AI signals like RSI, MACD, EMA crossovers, and more to make automated buy/sell decisions.

---

## 📁 Project Structure

![](images/Screenshot6.png)

yaml
Copy
Edit

---

## 📸 Screenshots

| 📈 TradingView | ⚙️ Webhook Server | ✅ Trade Log |
|---------------|------------------|--------------|
| ![](images/Screenshot1.png) | ![](images/Screenshot2.png) | ![](images/Screenshot3.png) |
| ![](images/Screenshot4.png) | ![](images/Screenshot5.png) |

---

## 🔐 API Keys & Setup

### 🔑 1. TradingView Webhook API Key

Generate from [uuidgenerator.net](https://www.uuidgenerator.net)

```env
API_KEY=tradingview_webhook_uk_bot
SECRET_KEY=d4f0c532-3905-449f-b7da-69ee07125da7
🔑 2. Binance Testnet Keys
Go to https://testnet.binance.vision

Login with Binance

Generate new API Key and Secret

env
Copy
Edit
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
USE_TESTNET=true
⚙️ Example .env File
env
Copy
Edit
# Webhook Authentication
API_KEY=tradingview_webhook_uk_bot
SECRET_KEY=d4f0c532-3905-449f-b7da-69ee07125da7

# Binance Testnet Credentials
BINANCE_API_KEY=3Mq4UvD1ObhsGFVphr9hi4zv5dFxZ6GIWT64G41E0X6aNXwNEnPM0NCHSV3MU8Wq
BINANCE_API_SECRET=1cLewWfB6mxy98lda7gDVlt4ytW1n7uppebEjfpCbdZg149EaaEiqY6iPtPFcvXo
USE_TESTNET=true

# Symbols (Testnet supported)
SYMBOLS=BNBUSDT,BTCUSDT,ETHUSDT

# Defaults
MAX_POSITION_SIZE=0.01
COOLDOWN_SECONDS=60

# Optional Per-Symbol Sizes
MAX_POSITION_SIZE_BNB=0.1
MAX_POSITION_SIZE_ETH=0.02
MAX_POSITION_SIZE_BTC=0.005
🧪 Run Locally (Virtual Environment)
1️⃣ Clone the Repo
bash
Copy
Edit
git clone https://github.com/SarabpreetBedi/AI-Powered-Trading-Bot-System.git
cd AI-Powered-Trading-Bot-System
2️⃣ Setup Virtual Environment
bash
Copy
Edit
python -m venv venv
Activate:

bash
Copy
Edit
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Create .env File
bash
Copy
Edit
cp .env.example .env
Then edit .env with your keys.

5️⃣ Start Webhook Server
bash
Copy
Edit
uvicorn webhook_server.main:app --reload --port 8000
6️⃣ Test Signal Manually
bash
Copy
Edit
python -m trading_bot.main
🐳 Run via Docker
1️⃣ Build and Start
bash
Copy
Edit
docker-compose up --build
2️⃣ Access API Docs
http://localhost:8000/docs

3️⃣ Send Webhook Test (Optional)
bash
Copy
Edit
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT", "rsi": 30, "macd": -0.1, "side": "buy"}'
📡 Connect to TradingView
✅ Alert Payload Example
In strategy.pine, your alert() should be like:

pinescript
Copy
Edit
alert('{' +
  '"api_key": "tradingview_webhook_uk_bot",' +
  '"symbol": "' + syminfo.ticker + '",' +
  '"price": "' + str.tostring(close) + '",' +
  '"side": "buy",' +
  '"rsi": "' + str.tostring(rsi) + '",' +
  '"macd": "' + str.tostring(macdLine) + '"' +
'}', freq=alert.freq_once_per_bar)
🔗 Webhook URL
Set in TradingView alerts:

text
Copy
Edit
http://<your-server-ip>:8000/webhook
Ensure port 8000 is open on your VPS/firewall.

✅ Features
🤖 AI-based decision making (RSI, MACD, EMA crossover, etc.)

🧠 LSTM & rule-based logic

🔄 Symbol-specific trade sizing

⏳ Cooldown management per symbol

🧾 Trade logging to SQLite

⚡ FastAPI webhook endpoint

🐳 Docker + Local support

🧪 Run Unit Tests
bash
Copy
Edit
pytest tests/
⚠️ Disclaimer
This bot operates on Binance Testnet. It’s for educational/testing use only.
Do not use real funds unless you understand the risks involved.

📝 License
MIT License

👨‍💻 Author
Sarabpreet Bedi
For questions, reach out via GitHub Issues.
