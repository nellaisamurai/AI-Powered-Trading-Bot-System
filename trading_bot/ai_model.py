#Set-ExecutionPolicy RemoteSigned -Scope Process
#.\venv\Scripts\Activate.ps1
#pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


import torch 
import torch.nn as nn
import numpy as np

# ===============================
# 1. LSTM Model Definition
# ===============================
class LSTMModel(nn.Module):
    def __init__(self, input_size=5, hidden_size=64, num_layers=2, output_size=2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Use last time step
        return out


# ===============================
# 2. Dummy Training Dataset
# ===============================
def generate_dummy_data(seq_len=10, num_samples=200):
    """
    Generates dummy signal data for model pretraining/testing
    """
    X = np.random.randn(num_samples, seq_len, 5)  # features: RSI, MACD, EMA_diff, BB_width, Stoch
    y = np.random.randint(0, 2, size=(num_samples,))  # 0: SELL, 1: BUY
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.long)


# ===============================
# 3. Training Procedure
# ===============================
def train_lstm(model, X, y, epochs=10):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    model.train()
    for epoch in range(epochs):
        out = model(X)
        loss = criterion(out, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return model


# ===============================
# 4. Trade Prediction
# ===============================
def predict_trade_action(model, signal_vector):
    """
    Takes a 10-step sequence of signal features, outputs "BUY" or "SELL"
    """
    model.eval()
    with torch.no_grad():
        signal_vector = torch.tensor(signal_vector, dtype=torch.float32).unsqueeze(0)  # shape: (1, 10, 5)
        out = model(signal_vector)
        prediction = torch.argmax(out, dim=1).item()
        return "BUY" if prediction == 1 else "SELL"


# ===============================
# 5. RL Policy Stub (to be extended)
# ===============================
class RLPolicy:
    def __init__(self):
        self.experiences = []

    def decide(self, state):
        # Placeholder: LSTM decision only for now
        return None

    def store_experience(self, state, action, reward):
        self.experiences.append((state, action, reward))

    def train(self):
        # Placeholder for future RL training logic
        pass


# ===============================
# 6. AI Decision Wrapper
# ===============================
# Initialize Model + Policy
model = LSTMModel()
X_dummy, y_dummy = generate_dummy_data()
model = train_lstm(model, X_dummy, y_dummy)
rl_policy = RLPolicy()

def ai_decision(signal: dict):
    """
    Input: signal = {
        'rsi': float,
        'macd': float,
        'ema_diff': float,
        'bb_width': float,
        'stoch': float
    }
    Output: "BUY" or "SELL"
    """
    features = [
        signal.get("rsi", 50) / 100.0,
        signal.get("macd", 0),
        signal.get("ema_diff", 0),
        signal.get("bb_width", 1),
        signal.get("stoch", 50) / 100.0
    ]
    signal_sequence = [features] * 10  # dummy sequence (you can replace with rolling window)

    # LSTM Prediction
    action = predict_trade_action(model, signal_sequence)

    # RL Override (not active yet)
    rl_override = rl_policy.decide(signal_sequence)

    return rl_override if rl_override else action
