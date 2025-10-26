
import pandas as pd, numpy as np, torch, joblib, json, os
from train_gru import GRUModel, preprocess, GROUP_COLUMNS

# Load encoder & model
le = joblib.load("model/label_encoder.pkl")
model = GRUModel(input_size=len(GROUP_COLUMNS), hidden_size=32, num_classes=len(le.classes_))
model.load_state_dict(torch.load("model/model_gru.pt", map_location="cpu"))
model.eval()

# Load data and build the same features as training
df = pd.read_csv("data/aruba_week.csv")
pivot = preprocess(df)

# Take last 30 minutes; if fewer than 30 rows, pad with zeros at the top
w_in = 30
feat = pivot[GROUP_COLUMNS]
if len(feat) < w_in:
    pad = pd.DataFrame(np.zeros((w_in - len(feat), len(GROUP_COLUMNS))), columns=GROUP_COLUMNS, index=pd.RangeIndex(w_in - len(feat)))
    feat = pd.concat([pad, feat], axis=0)

X = torch.tensor(feat.tail(w_in).values.reshape(1, w_in, len(GROUP_COLUMNS)), dtype=torch.float32)
with torch.no_grad():
    logits = model(X)
    pred_idx = int(torch.argmax(logits, dim=1).item())
    label = le.inverse_transform([pred_idx])[0]

out = {"timestamp": pd.Timestamp.now().isoformat(), "predicted_action": label}
os.makedirs("output", exist_ok=True)
with open("output/predictions.json", "w") as f:
    json.dump(out, f, indent=2)
print(out)
