
import json, os, datetime

PRED_FILE  = os.path.join("output","predictions.json")
OUTPUT_WEB = os.path.join("web","output","wa_events.json")

def main():
    probs = {"sleep":0.25,"meal":0.25,"toilet":0.25,"out":0.25}
    start_action = "out"
    if os.path.exists(PRED_FILE):
        with open(PRED_FILE, "r", encoding="utf-8") as f:
            pred = json.load(f)
        start_action = pred.get("predicted_action", start_action)
        probs = pred.get("probs", probs)

    order = ["sleep","toilet","meal","out"]
    if start_action in order:
        start_idx = order.index(start_action)
    else:
        start_idx = 0

    t0 = datetime.datetime.now().replace(second=0, microsecond=0)
    timeline = []
    for i in range(12):
        a = order[(start_idx + i) % len(order)]
        t = (t0 + datetime.timedelta(minutes=i*10)).strftime("%H:%M")
        timeline.append({"time": t, "action": a, "probs": probs})

    os.makedirs(os.path.dirname(OUTPUT_WEB), exist_ok=True)
    with open(OUTPUT_WEB, "w", encoding="utf-8") as f:
        json.dump({"timeline": timeline}, f, indent=2, ensure_ascii=False)
    print("✅ wrote", OUTPUT_WEB)

if __name__ == "__main__":
    main()
