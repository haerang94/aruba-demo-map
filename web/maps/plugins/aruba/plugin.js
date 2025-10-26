
// Toggle icon layers based on predicted action
console.log("Aruba plugin (visual fix) loaded");
const layerMap = { sleep: "icon_sleep", meal: "icon_meal", toilet: "icon_toilet", out: "icon_out" };

function updateFromJSON() {
  const url = "https://adventuretestfordemo.netlify.app/web/output/wa_events.json?ts=" + Date.now();
  fetch(url).then(r => r.json()).then(d => {
    const target = layerMap[d.action] || layerMap["out"];
    // hide all first
    Object.values(layerMap).forEach(name => WA.room.hideLayer(name));
    // show the predicted one
    WA.room.showLayer(target);
    console.log("Shown layer:", target, "action:", d.action);
  }).catch(err => console.error("Failed to load wa_events.json", err));
}

// initial + periodic refresh
updateFromJSON();
setInterval(updateFromJSON, 15000);
