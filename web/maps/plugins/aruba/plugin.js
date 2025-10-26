WA.onInit().then(async () => {
  console.log("🎬 Aruba animated timeline plugin started (2s + fade)");

  // ------ HUD (확률 오버레이) ------
  const hud = document.createElement('div');
  hud.id = 'wa-prob-overlay';
  Object.assign(hud.style, {
    position: 'fixed',
    top: '10px',
    right: '10px',
    background: 'rgba(0,0,0,0.55)',
    color: '#fff',
    font: '14px/1.35 monospace',
    padding: '8px 10px',
    borderRadius: '8px',
    zIndex: 99999,
    pointerEvents: 'none',
    transition: 'opacity 300ms ease'
  });
  document.body.appendChild(hud);

  function setHUD(text) {
    hud.style.opacity = '0';
    setTimeout(() => {
      hud.innerHTML = text;
      hud.style.opacity = '1';
    }, 120);
  }

  // ------ 타임라인 로드 ------
  async function loadTimeline() {
    const url = "https://adventuretestfordemo.netlify.app/web/output/wa_events.json?ts=" + Date.now();
    try {
      const resp = await fetch(url, { cache: "no-store" });
      const data = await resp.json();
      return data.timeline || [];
    } catch (e) {
      console.error("Failed to load timeline JSON:", e);
      return [];
    }
  }

  let timeline = await loadTimeline();
  if (!timeline.length) {
    console.warn("No timeline; using fallback cycle");
    timeline = [
      { time: "00:00", action: "sleep",  probs: {"sleep":1,"toilet":0,"meal":0,"out":0} },
      { time: "00:10", action: "toilet", probs: {"sleep":0,"toilet":1,"meal":0,"out":0} },
      { time: "00:20", action: "meal",   probs: {"sleep":0,"toilet":0,"meal":1,"out":0} },
      { time: "00:30", action: "out",    probs: {"sleep":0,"toilet":0,"meal":0,"out":1} }
    ];
  }

  const LAYERS = ["icon_sleep","icon_meal","icon_toilet","icon_out"];
  const MAP = { sleep: "icon_sleep", meal: "icon_meal", toilet: "icon_toilet", out: "icon_out" };

  // ------ 유틸: 레이어 페이드 ------
  const hasOpacityApi = typeof WA.room.setLayerOpacity === 'function';

  async function setOpacitySafe(name, value) {
    if (hasOpacityApi) {
      await WA.room.setLayerOpacity(name, value);
    } else {
      if (value > 0) await WA.room.showLayer(name);
      else await WA.room.hideLayer(name);
    }
  }

  async function fadeLayer(name, from, to, durationMs) {
    if (!hasOpacityApi) {
      // 폴백: 즉시 show/hide
      await setOpacitySafe(name, to > 0 ? 1 : 0);
      return;
    }
    const steps = 10;
    const dt = durationMs / steps;
    let current = from;
    const delta = (to - from) / steps;

    await setOpacitySafe(name, current);
    if (to > 0) await WA.room.showLayer(name);

    for (let i = 0; i < steps; i++) {
      current += delta;
      await setOpacitySafe(name, Math.max(0, Math.min(1, current)));
      await new Promise(r => setTimeout(r, dt));
    }
    await setOpacitySafe(name, to);

    if (to === 0) await WA.room.hideLayer(name);
  }

  // ------ 한 스텝 적용 ------
  async function applyStep(step) {
    // 모든 아이콘 레이어를 천천히 페이드아웃
    await Promise.all(LAYERS.map(name => fadeLayer(name, 1, 0, 250)));

    // 선택된 아이콘만 페이드인
    const target = MAP[step.action] || "icon_out";
    await fadeLayer(target, 0, 1, 250);

    // HUD 갱신
    const probs = step.probs || {};
    const keys = ["sleep","meal","toilet","out"];
    const lines = keys.map(k => {
      const v = (probs[k] != null) ? Number(probs[k]).toFixed(2) : "--";
      const mark = (k === step.action) ? "◉" : "•";
      return `${mark} ${k.padEnd(6)} ${v}`;
    }).join("<br>");
    setHUD(`<b>${step.time}</b> → <b>${step.action}</b><br>${lines}`);

    console.log("▶️", step.time, "action:", step.action, "probs:", probs);
  }

  // ------ 플레이 루프 (2초 간격) ------
  let idx = 0;
  async function tick() {
    await applyStep(timeline[idx % timeline.length]);
    idx++;
  }
  await tick();
  setInterval(tick, 2000); // ⏱ 2초

  // ------ 60초마다 타임라인 재로드 ------
  setInterval(async () => {
    const fresh = await loadTimeline();
    if (fresh.length) {
      timeline = fresh;
      idx = 0;
      console.log("🔄 timeline reloaded:", timeline.length, "steps");
    }
  }, 60000);
});
