from fastapi import FastAPI, Header, HTTPException, Request
import hmac
import hashlib
import os
import json

from trading_bot.main import handle_signal

app = FastAPI()

# Load secrets from .env file
API_KEY_EXPECTED = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY") 

# === HMAC Validator ===
def verify_hmac_signature(secret: str, message: bytes, signature: str) -> bool:
    computed_hmac = hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_hmac, signature)

@app.post("/webhook")
async def webhook(
    request: Request,
    x_api_key: str = Header(None),
    x_signature: str = Header(None),
):
    body = await request.body()

    # Step 1: Validate API key
    if x_api_key != API_KEY_EXPECTED:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    # Step 2: Validate HMAC signature
    if not x_signature or not verify_hmac_signature(SECRET_KEY, body, x_signature):
        raise HTTPException(status_code=403, detail="Invalid HMAC Signature")

    # Step 3: Parse JSON
    try:
        data = await request.json()
        print("✅ Valid signal received:", data)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Step 4: Pass to AI trading bot
    try:
        handle_signal(data)
        return {"status": "ok", "detail": "Signal processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
