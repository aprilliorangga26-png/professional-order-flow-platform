const instrumentCatalog = [
  {
    id: "xauusd-spot",
    name: "XAUUSD Spot",
    symbol: "OANDA:XAUUSD",
    feed: "OANDA",
    status: "delayed",
    market: "Spot",
    sourceType: "Broker-specific"
  },
  {
    id: "gc-comex",
    name: "COMEX Gold Futures",
    symbol: "COMEX:GC1!",
    feed: "TradingView / Simulated",
    status: "historical",
    market: "Futures",
    sourceType: "Contract metadata"
  }
];

const dataCapabilities = {
  "xauusd-spot": {
    ohlc: true,
    tickTrades: false,
    aggressorSide: false,
    bidAskVolume: false,
    level2: false,
    historicalBook: false,
    replay: true,
    liveStatus: "delayed",
    notes: "Data is illustrative in this prototype; no live broker feed is configured by default."
  },
  "gc-comex": {
    ohlc: true,
    tickTrades: true,
    aggressorSide: true,
    bidAskVolume: true,
    level2: true,
    historicalBook: true,
    replay: true,
    liveStatus: "historical",
    notes: "Simulated futures dataset for UI and analytics validation only."
  }
};

const uiState = {
  selectedInstrument: "xauusd-spot",
  playing: false,
  replayValue: 32,
  chartReady: false
};

const marketSnapshots = [
  { price: 2332.15, bid: [2332.12, 2332.08, 2332.03, 2331.98, 2331.94], ask: [2332.18, 2332.22, 2332.27, 2332.31, 2332.36], volume: 1240 },
  { price: 2332.22, bid: [2332.18, 2332.12, 2332.07, 2332.04, 2332.01], ask: [2332.25, 2332.29, 2332.33, 2332.39, 2332.44], volume: 1315 },
  { price: 2332.31, bid: [2332.26, 2332.22, 2332.18, 2332.11, 2332.06], ask: [2332.34, 2332.38, 2332.43, 2332.46, 2332.51], volume: 1390 },
  { price: 2332.45, bid: [2332.38, 2332.34, 2332.31, 2332.27, 2332.22], ask: [2332.49, 2332.53, 2332.57, 2332.62, 2332.67], volume: 1450 },
  { price: 2332.56, bid: [2332.49, 2332.45, 2332.41, 2332.37, 2332.31], ask: [2332.62, 2332.66, 2332.69, 2332.74, 2332.79], volume: 1535 },
  { price: 2332.60, bid: [2332.52, 2332.48, 2332.42, 2332.39, 2332.35], ask: [2332.66, 2332.71, 2332.76, 2332.81, 2332.87], volume: 1660 }
];

const tradeEvents = [
  { time: "09:45:12", price: 2332.18, volume: 26, side: "buy" },
  { time: "09:45:22", price: 2332.23, volume: 18, side: "sell" },
  { time: "09:45:33", price: 2332.28, volume: 30, side: "buy" },
  { time: "09:45:45", price: 2332.32, volume: 21, side: "sell" },
  { time: "09:45:56", price: 2332.35, volume: 35, side: "buy" },
  { time: "09:46:02", price: 2332.41, volume: 24, side: "sell" },
  { time: "09:46:18", price: 2332.47, volume: 41, side: "buy" },
  { time: "09:46:27", price: 2332.51, volume: 19, side: "sell" },
  { time: "09:46:39", price: 2332.55, volume: 32, side: "buy" },
  { time: "09:46:51", price: 2332.58, volume: 28, side: "sell" },
  { time: "09:47:10", price: 2332.61, volume: 43, side: "buy" },
  { time: "09:47:24", price: 2332.63, volume: 22, side: "sell" }
];

const cvdSeries = [
  { label: "09:45", delta: 19, total: 19 },
  { label: "09:46", delta: 26, total: 45 },
  { label: "09:47", delta: 12, total: 57 },
  { label: "09:48", delta: -8, total: 49 },
  { label: "09:49", delta: 17, total: 66 },
  { label: "09:50", delta: 10, total: 76 },
  { label: "09:51", delta: -4, total: 72 }
];

const macroNews = [
  {
    title: "Federal Reserve policy discussion",
    time: "Illustrative session window",
    detail: "Macro risk: real rate expectations and USD strength influence gold price sensitivity."
  },
  {
    title: "US inflation / CPI",
    time: "Illustrative macro release",
    detail: "Inflation data can alter real-rate expectations and drive gold volatility around key catalysts."
  },
  {
    title: "Treasury yields",
    time: "Illustrative market driver",
    detail: "Bond yields influence opportunity cost and the relative attractiveness of non-yielding gold."
  },
  {
    title: "Geopolitical risk premium",
    time: "Illustrative event",
    detail: "Risk-off demand can add bid support when macro uncertainty expands."
  }
];

const quantMetrics = [
  { label: "Order Flow Imbalance", value: "+1.38" },
  { label: "Trade Intensity", value: "2.4σ" },
  { label: "Volume Imbalance", value: "+6.1%" },
  { label: "Spread", value: "0.32" },
  { label: "Liquidity Replenishment", value: "67%" },
  { label: "Absorption Score", value: "0.78" },
  { label: "Slippage Est.", value: "0.14" },
  { label: "CVD Divergence", value: "Moderate" }
];

const connectionStatusMap = {
  "xauusd-spot": "Mode: Delayed / Broker feed",
  "gc-comex": "Mode: Historical / Simulated futures"
};

function loadTradingViewWidget(symbol) {
  const container = document.getElementById("tradingviewWidget");
  container.innerHTML = "";

  if (window.TradingView && window.TradingView.widget) {
    new window.TradingView.widget({
      autosize: true,
      symbol,
      interval: "5",
      timezone: "Etc/UTC",
      theme: "dark",
      style: "1",
      locale: "en",
      toolbar_bg: "#0b1220",
      enable_publishing: false,
      withdateranges: true,
      hide_side_toolbar: false,
      allow_symbol_change: true,
      save_image: false,
      details: true,
      studies: ["MASimple@tv-basicstudies"],
      container_id: "tradingviewWidget"
    });
  } else {
    container.innerHTML = "<div class='empty-state'>TradingView widget not available. Check network access and supported browser environment.</div>";
  }
}

function renderInstrumentSelector() {
  const el = document.getElementById("instrumentSwitcher");
  el.innerHTML = instrumentCatalog
    .map((instrument) => {
      const activeClass = uiState.selectedInstrument === instrument.id ? "active" : "";
      return `<button class="instrument-btn ${activeClass}" data-id="${instrument.id}">${instrument.name}</button>`;
    })
    .join("");

  el.querySelectorAll(".instrument-btn").forEach((button) => {
    button.addEventListener("click", () => {
      uiState.selectedInstrument = button.dataset.id;
      renderAll();
    });
  });
}

function renderStatus() {
  const instrument = instrumentCatalog.find((item) => item.id === uiState.selectedInstrument);
  const element = document.getElementById("connectionStatus");
  element.textContent = connectionStatusMap[uiState.selectedInstrument] || "Mode: Simulated";

  const statusClass = instrument.status === "delayed" ? "delayed" : instrument.status === "historical" ? "historical" : "simulated";
  const dot = element.previousElementSibling;
  dot.className = `status-dot ${statusClass}`;

  document.getElementById("chartSummary").textContent = `${instrument.name} · ${instrument.sourceType} · ${instrument.status}`;
}

function getDepthRows() {
  const levels = [
    { price: 2332.62, bid: 220, ask: 180 },
    { price: 2332.57, bid: 290, ask: 160 },
    { price: 2332.52, bid: 340, ask: 210 },
    { price: 2332.47, bid: 280, ask: 260 },
    { price: 2332.42, bid: 220, ask: 300 },
    { price: 2332.37, bid: 150, ask: 280 },
    { price: 2332.32, bid: 110, ask: 340 },
    { price: 2332.27, bid: 80, ask: 290 },
    { price: 2332.22, bid: 75, ask: 220 },
    { price: 2332.17, bid: 52, ask: 180 }
  ];

  return levels.map((level) => {
    const direction = level.bid >= level.ask ? "bid" : "ask";
    const displayPrice = level.price.toFixed(2);
    return `
      <div class="dom-row">
        <div class="price ${direction}">${displayPrice}</div>
        <div class="qty">${level.bid}</div>
        <div class="qty">${level.ask}</div>
      </div>
    `;
  }).join("");
}

function renderHeatmap() {
  const rows = [
    ["bid", "bid", "bid", "ask", "ask", "ask", "ask", "bid", "bid", "ask", "ask", "bid", "bid", "ask", "bid", "bid", "ask", "ask", "ask", "bid", "ask", "bid"],
    ["bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask"],
    ["ask", "ask", "bid", "bid", "ask", "bid", "ask", "ask", "bid", "ask", "ask", "bid", "ask", "bid", "bid", "ask", "bid", "ask", "bid", "ask", "ask", "bid"],
    ["ask", "bid", "ask", "bid", "bid", "ask", "bid", "bid", "ask", "bid", "ask", "ask", "bid", "ask", "bid", "bid", "ask", "bid", "ask", "bid", "ask", "bid"],
    ["bid", "bid", "ask", "ask", "bid", "ask", "ask", "ask", "bid", "bid", "ask", "bid", "ask", "ask", "bid", "ask", "bid", "bid", "ask", "bid", "ask", "bid"],
    ["bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "ask", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "bid"],
    ["ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "ask", "bid", "ask", "bid", "ask", "bid"],
    ["bid", "bid", "ask", "ask", "bid", "ask", "bid", "ask", "bid", "ask", "bid", "bid", "ask", "bid", "ask", "bid", "ask", "ask", "bid", "ask", "bid", "ask"]
  ];

  const heatmap = document.getElementById("heatmapContainer");
  const html = rows.map((row) => {
    const cells = row.map((cell) => `<div class="heatmap-cell ${cell}"></div>`).join("");
    return `<div class="heatmap-row">${cells}</div>`;
  }).join("");

  heatmap.innerHTML = html;
}

function renderFootprint() {
  const footprint = document.getElementById("footprintContainer");
  const html = [80, 120, 90, 140, 110, 160, 130]
    .map((value, index) => {
      const bid = value;
      const ask = [110, 90, 140, 100, 120, 90, 130][index];
      return `
        <div class="footprint-bar">
          <div class="footprint-bid" style="height:${Math.min(bid / 1.9, 100)}%">${bid}</div>
          <div class="footprint-ask" style="height:${Math.min(ask / 1.9, 100)}%">${ask}</div>
        </div>
      `;
    })
    .join("");

  footprint.innerHTML = html;
}

function renderBubbles() {
  const bubbles = document.getElementById("bubblesContainer");
  const html = tradeEvents
    .filter((event) => event.volume >= 15)
    .map((event) => {
      const size = Math.max(22, event.volume * 1.8);
      return `<div class="bubble ${event.side}" style="width:${size}px;height:${size}px">${event.volume}</div>`;
    })
    .join("");

  bubbles.innerHTML = html;
}

function renderCVD() {
  const cvd = document.getElementById("cvdChart");
  const max = Math.max(...cvdSeries.map((item) => item.total));
  const html = cvdSeries.map((item) => {
    const height = (item.total / max) * 100;
    return `
      <div class="cvd-bar">
        <div class="bar" style="height:${height}%"></div>
        <span>${item.label}</span>
      </div>
    `;
  }).join("");
  cvd.innerHTML = html;
}

function renderNews() {
  const news = document.getElementById("newsList");
  news.innerHTML = macroNews
    .map((item) => `
      <div class="news-item">
        <strong>${item.title}</strong>
        <small>${item.time}</small>
        <div>${item.detail}</div>
      </div>
    `)
    .join("");
}

function renderQuantMetrics() {
  const metrics = document.getElementById("quantMetrics");
  metrics.innerHTML = quantMetrics
    .map((metric) => `
      <div class="metric-card">
        <span class="label">${metric.label}</span>
        <div class="value">${metric.value}</div>
      </div>
    `)
    .join("");
}

function renderReplay() {
  const slider = document.getElementById("replaySlider");
  const time = document.getElementById("replayTime");
  const speed = document.getElementById("replaySpeed");

  const replayTimes = [
    "09:45:00",
    "09:46:00",
    "09:47:00",
    "09:48:00",
    "09:49:00",
    "09:50:00",
    "09:51:00"
  ];

  const index = Math.min(Math.floor((slider.value / 100) * replayTimes.length), replayTimes.length - 1);
  time.textContent = replayTimes[index];
  speed.textContent = `Speed: ${(0.5 + slider.value / 100).toFixed(1)}x`;
}

function attachReplayHandlers() {
  const btn = document.getElementById("playPauseBtn");
  const slider = document.getElementById("replaySlider");

  btn.addEventListener("click", () => {
    uiState.playing = !uiState.playing;
    btn.textContent = uiState.playing ? "Pause" : "Play";
  });

  slider.addEventListener("input", (event) => {
    uiState.replayValue = Number(event.target.value);
    renderReplay();
  });
}

function renderAll() {
  renderInstrumentSelector();
  renderStatus();
  renderHeatmap();
  renderFootprint();
  renderBubbles();
  renderCVD();
  renderNews();
  renderQuantMetrics();
  renderReplay();
  loadTradingViewWidget(instrumentCatalog.find((item) => item.id === uiState.selectedInstrument).symbol);
  document.getElementById("domContainer").innerHTML = getDepthRows();
}

document.getElementById("saveLayoutBtn").addEventListener("click", () => {
  localStorage.setItem("goldflow-layout", JSON.stringify({ instrument: uiState.selectedInstrument }));
  alert("Layout saved to browser local storage.");
});

document.getElementById("resetLayoutBtn").addEventListener("click", () => {
  uiState.selectedInstrument = "xauusd-spot";
  localStorage.removeItem("goldflow-layout");
  renderAll();
});

const storedLayout = localStorage.getItem("goldflow-layout");
if (storedLayout) {
  try {
    const parsed = JSON.parse(storedLayout);
    if (parsed.instrument) {
      uiState.selectedInstrument = parsed.instrument;
    }
  } catch (error) {
    console.warn("Unable to parse saved layout:", error);
  }
}

attachReplayHandlers();
renderAll();

window.addEventListener("resize", () => {
  if (uiState.selectedInstrument) {
    loadTradingViewWidget(instrumentCatalog.find((item) => item.id === uiState.selectedInstrument).symbol);
  }
});
