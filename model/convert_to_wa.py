
import json, os, datetime

OUTPUT_WEB = os.path.join("web","output","wa_events.json")
PRED_FILE  = os.path.join("output","predictions.json")

def build_timeline(start_action=None, steps=12, step_minutes=10):
    order = ["sleep","toilet","meal","out"]
    if start_action in order:
        start_idx = order.index(start_action)
    else:
        start_idx = 0
    t0 = datetime.datetime.now().replace(second=0, microsecond=0)
    timeline = []
    for i in range(steps):
        a = order[(start_idx + i) % len(order)]
        t = (t0 + datetime.timedelta(minutes=i*step_minutes)).strftime("%H:%M")
        timeline.append({"time": t, "action": a})
    return {"timeline": timeline}

def main():
    start_action = None
    if os.path.exists(PRED_FILE):
        try:
            pred = json.load(open(PRED_FILE, "r", encoding="utf-8"))
            start_action = pred.get("predicted_action")
        except Exception as e:
            print("WARN: could not read predictions.json:", e)

    data = build_timeline(start_action=start_action, steps=12, step_minutes=10)
    os.makedirs(os.path.dirname(OUTPUT_WEB), exist_ok=True)
    with open(OUTPUT_WEB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("✅ wrote", OUTPUT_WEB)

if __name__ == "__main__":
    main()
