
WA.onInit().then(async () => {
  console.log("⏱️ Aruba timeline plugin started");

  const url = "https://adventuretestfordemo.netlify.app/web/output/wa_events.json?ts=" + Date.now();
  let timeline = [];
  try {
    const resp = await fetch(url, { cache: "no-store" });
    const data = await resp.json();
    timeline = data.timeline || [];
  } catch (e) {
    console.error("Failed to load timeline JSON:", e);
  }

  if (!timeline.length) {
    console.warn("No timeline in wa_events.json; fallback to default");
    timeline = [
      { time: "00:00", action: "sleep" },
      { time: "00:10", action: "toilet" },
      { time: "00:20", action: "meal" },
      { time: "00:30", action: "out" }
    ];
  }

  const layerMap = { sleep: "icon_sleep", meal: "icon_meal", toilet: "icon_toilet", out: "icon_out" };
  let index = 0;

  async function applyAction(act) {
    await WA.room.hideLayer("icon_sleep");
    await WA.room.hideLayer("icon_meal");
    await WA.room.hideLayer("icon_toilet");
    await WA.room.hideLayer("icon_out");
    const layerName = layerMap[act] || "icon_out";
    await WA.room.showLayer(layerName);
    console.log("▶️ shown layer:", layerName, "action:", act);
  }

  async function tick() {
    const step = timeline[index % timeline.length];
    await applyAction(step.action);
    index++;
  }

  await tick();
  setInterval(tick, 10000);
});
