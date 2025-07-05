import hmac
import hashlib

def verify_hmac(payload: bytes, signature: str, secret: str) -> bool:
    expected_signature = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, signature)
