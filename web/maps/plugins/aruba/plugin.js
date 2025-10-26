
console.log("Aruba plugin (icons on white circles) loaded");
const layerMap = { sleep: "icon_sleep", meal: "icon_meal", toilet: "icon_toilet", out: "icon_out" };

function updateFromJSON() {
  const url = "https://adventuretestfordemo.netlify.app/web/output/wa_events.json?ts=" + Date.now();
  fetch(url).then(r => r.json()).then(d => {
    const target = layerMap[d.action] || layerMap["out"];
    Object.values(layerMap).forEach(name => WA.room.hideLayer(name));
    WA.room.showLayer(target);
    console.log("Shown layer:", target, "action:", d.action);
  }).catch(err => console.error("Failed to load wa_events.json", err));
}

updateFromJSON();
setInterval(updateFromJSON, 15000);
