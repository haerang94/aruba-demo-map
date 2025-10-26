
import pandas as pd, numpy as np, torch
from torch import nn, optim
from sklearn.preprocessing import LabelEncoder
import joblib

GROUP_COLUMNS = ["bedroom", "kitchen", "bathroom", "entrance"]

def preprocess(df: pd.DataFrame):
    # Expect columns: Date, Time, Sensor, Value, Activity
    # Combine timestamp safely (avoid deprecated parse_dates nested)
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str))
    df["minute"] = df["timestamp"].dt.floor("1min")

    # Map sensor -> group
    group_map = {"M00": "bedroom", "M01": "kitchen", "M02": "bathroom", "M03": "entrance"}
    def to_group(s):
        s = str(s)
        for k, v in group_map.items():
            if k in s:
                return v
        return "other"

    df["group"] = df["Sensor"].map(to_group)

    # 1-min aggregation by group: share of ON events in that minute
    pivot = df.pivot_table(index="minute", columns="group", values="Value",
                           aggfunc=lambda x: (x == "ON").mean()).fillna(0.0)

    # Ensure consistent column order and presence
    for col in GROUP_COLUMNS:
        if col not in pivot.columns:
            pivot[col] = 0.0
    pivot = pivot[GROUP_COLUMNS].sort_index()

    # Weak label from dominant group per minute
    def label_fn(row):
        if row["bedroom"] > 0.5:
            return "sleep"
        if row["kitchen"] > 0.5:
            return "meal"
        if row["bathroom"] > 0.5:
            return "toilet"
        if row["entrance"] > 0.5:
            return "out"
        return "none"

    labels = pivot.apply(label_fn, axis=1)
    pivot["label"] = labels
    return pivot

class GRUModel(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, num_classes: int):
        super().__init__()
        self.gru = nn.GRU(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
    def forward(self, x):
        _, h = self.gru(x)
        return self.fc(h[-1])

def train():
    df = pd.read_csv("data/aruba_week.csv")
    pivot = preprocess(df)

    X, y = [], []
    w_in, w_out = 30, 10
    for i in range(len(pivot) - w_in - w_out):
        X.append(pivot.iloc[i:i+w_in][GROUP_COLUMNS].values)
        y.append(pivot["label"].iloc[i+w_in+w_out-1])
    X, y = np.stack(X), np.array(y)

    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    joblib.dump(le, "model/label_encoder.pkl")

    model = GRUModel(input_size=len(GROUP_COLUMNS), hidden_size=32, num_classes=len(le.classes_))
    criterion = nn.CrossEntropyLoss()
    opt = optim.Adam(model.parameters(), lr=1e-3)

    X_t = torch.tensor(X, dtype=torch.float32)
    y_t = torch.tensor(y_enc, dtype=torch.long)

    for ep in range(5):
        opt.zero_grad()
        out = model(X_t)
        loss = criterion(out, y_t)
        loss.backward()
        opt.step()
        print(f"Epoch {ep+1} Loss {loss.item():.6f}")

    torch.save(model.state_dict(), "model/model_gru.pt")
    print("✅ GRU trained & saved.")

if __name__ == "__main__":
    train()
