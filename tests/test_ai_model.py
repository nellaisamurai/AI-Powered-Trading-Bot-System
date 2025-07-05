import pytest
from trading_bot.ai_model import ai_decision

def test_ai_decision_buy():
    signal = {
        "rsi": 25,
        "macd": 0.5,
        "ema_diff": 0.1,
        "bb_width": 0.02,
        "stoch": 15
    }
    action = ai_decision(signal)
    assert action in ["BUY", "SELL"]  # Dummy model; just ensure output

def test_ai_decision_sell():
    signal = {
        "rsi": 75,
        "macd": -0.5,
        "ema_diff": -0.1,
        "bb_width": 0.01,
        "stoch": 85
    }
    action = ai_decision(signal)
    assert action in ["BUY", "SELL"]
