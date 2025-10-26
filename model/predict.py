
import pandas as pd, numpy as np, torch, torch.nn.functional as F, joblib, json,os
from train_gru import GRUModel, preprocess, GROUP_COLUMNS

le = joblib.load("model/label_encoder.pkl")
model = GRUModel(input_size=len(GROUP_COLUMNS), hidden_size=32, num_classes=len(le.classes_))
model.load_state_dict(torch.load("model/model_gru.pt", map_location="cpu"))
model.eval()

df = pd.read_csv("data/aruba_week.csv")
pivot = preprocess(df)
feat = pivot[GROUP_COLUMNS].tail(30).values.reshape(1,30,len(GROUP_COLUMNS)).astype(np.float32)
X = torch.tensor(feat)

with torch.no_grad():
    logits = model(X)
    probs = F.softmax(logits, dim=1).cpu().numpy()[0]
    pred_idx = int(np.argmax(probs))
    label = le.inverse_transform([pred_idx])[0]

probs_map = {c: float(probs[i]) for i, c in enumerate(le.classes_)}
# Normalize to our four canonical keys
keys = ["sleep","meal","toilet","out"]
norm = {k: float(probs_map.get(k, 0.0)) for k in keys}
s = sum(norm.values()) or 1.0
norm = {k: v/s for k, v in norm.items()}

out = {"predicted_action": label, "probs": norm}
os.makedirs("output", exist_ok=True)
with open("output/predictions.json","w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print(out)
