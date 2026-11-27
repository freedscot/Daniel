/* Coffee & Tiyul — kosher coffee/food + hikes map. Static app: reads data/places.json. */
(() => {
  "use strict";

  // ---------- i18n ----------
  const T = {
    en: {
      appName: "Coffee & Tiyul", search: "Search places", qAll: "All", qFood: "☕ Coffee & food", qHike: "🥾 Hikes",
      qFri: "Open Fri morning", qNear: "📍 Near me", tabList: "List", tabFilters: "Filters",
      count: n => `${n} places`, none: "Nothing matches these filters.",
      fType: "Type", cart: "Coffee cart", cafe: "Café", food_truck: "Food truck", hike: "Hike",
      fArea: "Area", anyArea: "All areas", fKosher: "Kashrut level", badatz: "Badatz", rabbanut_mehadrin: "Rabbanut Mehadrin",
      rabbanut_regular: "Rabbanut (regular)", other: "Other hashgacha", unconfirmed: "Unconfirmed",
      onlyConfirmed: "Only hechsher stated by the business or an official source",
      fDairy: "Dairy / meat", any: "Any", dairy: "Dairy", meat: "Meat",
      fOpen: "Open on", anyDay: "Any day", today: "Today", anyTime: "Any time", morning: "Morning (8–11)", midday: "Midday (11–14)",
      afternoon: "Afternoon (14–17)", evening: "Evening (17–21)",
      days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Motzei Shabbat / Sat"],
      daysShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
      fHike: "Hikes", maxLen: km => km >= 15 ? "Any length" : `Up to ${km} km`, easy: "Easy", moderate: "Moderate", hard: "Hard",
      water: "Water / spring", kids: "Kid-friendly", loopOnly: "Loop only", stroller: "Stroller-friendly",
      fMine: "My places", hideVisited: "Hide visited", onlyVisited: "Only visited", reset: "Reset filters",
      openNow: "Open now", closedNow: "Closed now", closedToday: "Closed today", hoursUnknown: "Hours unknown", unconfShort: "unconfirmed",
      kosherBy: "Hechsher", body: "Certified by", level: "Level", status: "Source", lastChecked: "Last checked",
      st_owner_stated: "Stated by the business", st_official: "Official listing", st_third_party: "Third-party only – unconfirmed",
      st_unconfirmed: "Unconfirmed", st_blog_post: "Hiking the Holyland post", "st_n/a": "—",
      hours: "Hours", hoursNote: "Always check before you go.", gmaps: "Google Maps", waze: "Waze", call: "Call", insta: "Instagram", web: "Website",
      dairyMeat: "Dairy/meat", pairings: "Coffee & food within ~15 min", nearbyHikes: "Hikes within ~15 min", findingPairs: "Checking drive times…",
      noPairs: "No kosher stop within 15 minutes' drive.", approxDrive: "approx. – drive times unavailable",
      trail: "The trail", length: "Length", time: "Time", difficulty: "Difficulty", route: "Route", colors: "Trail colors",
      waterSpring: "Water", pool: "Pools", shade: "Shade", season: "Best season", kidsL: "Kids", strollerL: "Stroller",
      parking: "Parking", fee: "Entrance fee", warnings: "Know before you go", details: "Details from",
      coords: "Map pin", notes: "Notes", myNotes: "My notes (saved on this phone)", visited: "I've been here", sources: "Sources",
      km: "km", min: "min", hrs: "hrs", fromHome: "from Ramat Bet Shemesh", fromYou: "from you", back: "Close",
      locErr: "Couldn't get your location. Check location permission for this site.",
      sgTitle: "Suggest a place", sgHelp: "Paste an Instagram (or any) link. It opens a ready-made request on GitHub – tap Submit there, and Claude researches and adds it.", sgLink: "Link", sgNotes: "Notes (optional)", sgCancel: "Cancel", sgSend: "Continue to GitHub", sgBtn: "➕ Suggest a place",
      closedDay: "Closed", free: "Free", paid: "Paid entry", yes: "Yes", no: "No",
    },
    he: {
      appName: "טיול וקפה", search: "חיפוש", qAll: "הכל", qFood: "☕ קפה ואוכל", qHike: "🥾 טיולים",
      qFri: "פתוח שישי בבוקר", qNear: "📍 קרוב אליי", tabList: "רשימה", tabFilters: "סינון",
      count: n => `${n} מקומות`, none: "אין תוצאות לסינון הזה.",
      fType: "סוג", cart: "עגלת קפה", cafe: "בית קפה", food_truck: "פודטראק", hike: "מסלול",
      fArea: "אזור", anyArea: "כל האזורים", fKosher: "רמת כשרות", badatz: "בד\"ץ", rabbanut_mehadrin: "רבנות מהדרין",
      rabbanut_regular: "רבנות", other: "השגחה אחרת", unconfirmed: "לא מאומת",
      onlyConfirmed: "רק כשרות שהעסק או מקור רשמי ציינו",
      fDairy: "חלבי / בשרי", any: "הכל", dairy: "חלבי", meat: "בשרי",
      fOpen: "פתוח ב", anyDay: "כל יום", today: "היום", anyTime: "כל שעה", morning: "בוקר (8–11)", midday: "צהריים (11–14)",
      afternoon: "אחה\"צ (14–17)", evening: "ערב (17–21)",
      days: ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "מוצ\"ש / שבת"],
      daysShort: ["א׳", "ב׳", "ג׳", "ד׳", "ה׳", "ו׳", "ש׳"],
      fHike: "מסלולים", maxLen: km => km >= 15 ? "כל אורך" : `עד ${km} ק"מ`, easy: "קל", moderate: "בינוני", hard: "קשה",
      water: "מים / מעיין", kids: "מתאים לילדים", loopOnly: "מעגלי בלבד", stroller: "מתאים לעגלה",
      fMine: "המקומות שלי", hideVisited: "הסתר מקומות שביקרתי", onlyVisited: "רק מקומות שביקרתי", reset: "איפוס סינון",
      openNow: "פתוח עכשיו", closedNow: "סגור עכשיו", closedToday: "סגור היום", hoursUnknown: "שעות לא ידועות", unconfShort: "לא מאומת",
      kosherBy: "כשרות", body: "גוף משגיח", level: "רמה", status: "מקור", lastChecked: "נבדק לאחרונה",
      st_owner_stated: "לפי בעל העסק", st_official: "מקור רשמי", st_third_party: "מקור משני בלבד – לא מאומת",
      st_unconfirmed: "לא מאומת", st_blog_post: "פוסט ב-Hiking the Holyland", "st_n/a": "—",
      hours: "שעות פתיחה", hoursNote: "כדאי לבדוק לפני שיוצאים.", gmaps: "גוגל מפות", waze: "וייז", call: "התקשרות", insta: "אינסטגרם", web: "אתר",
      dairyMeat: "חלבי/בשרי", pairings: "קפה ואוכל עד ~15 דק׳ נסיעה", nearbyHikes: "מסלולים עד ~15 דק׳ נסיעה", findingPairs: "בודק זמני נסיעה…",
      noPairs: "אין עצירה כשרה במרחק 15 דקות נסיעה.", approxDrive: "בקירוב – זמני נסיעה לא זמינים",
      trail: "המסלול", length: "אורך", time: "זמן", difficulty: "קושי", route: "סוג מסלול", colors: "סימון שבילים",
      waterSpring: "מים", pool: "בריכות", shade: "צל", season: "עונה מומלצת", kidsL: "ילדים", strollerL: "עגלה",
      parking: "חניה", fee: "דמי כניסה", warnings: "חשוב לדעת", details: "פרטים מתוך",
      coords: "נעץ במפה", notes: "הערות", myNotes: "ההערות שלי (נשמר בטלפון הזה)", visited: "ביקרתי כאן", sources: "מקורות",
      km: "ק\"מ", min: "דק׳", hrs: "שע׳", fromHome: "מרמת בית שמש", fromYou: "ממך", back: "סגירה",
      locErr: "לא הצלחתי לקבל מיקום. בדקו הרשאת מיקום לאתר.",
      sgTitle: "הצעת מקום", sgHelp: "הדביקו קישור לאינסטגרם (או כל קישור). ייפתח טופס בקשה מוכן ב-GitHub – לחצו Submit שם, ו-Claude יבדוק ויוסיף.", sgLink: "קישור", sgNotes: "הערות (לא חובה)", sgCancel: "ביטול", sgSend: "המשך ל-GitHub", sgBtn: "➕ הצעת מקום",
      closedDay: "סגור", free: "חינם", paid: "בתשלום", yes: "כן", no: "לא",
    },
  };
  const DAYKEYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
  const FOOD = ["cart", "cafe", "food_truck"];
  const ICON = { cart: "☕", cafe: "🥐", food_truck: "🚚", hike: "🥾" };
  const WINDOWS = { morning: [480, 660], midday: [660, 840], afternoon: [840, 1020], evening: [1020, 1260] };
  const HOME = { lat: 31.711, lng: 34.987 };

  // ---------- state ----------
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode */ } },
  };
  const DEFAULT_F = { types: [], area: "", levels: [], onlyConfirmed: false, dairy: "", day: "", time: "",
    maxLen: 15, diff: [], water: false, kids: false, loop: false, stroller: false, visited: "" };
  const S = {
    lang: store.get("lang", (navigator.language || "").startsWith("he") ? "he" : "en"),
    f: Object.assign({}, DEFAULT_F, store.get("filters", {})),
    q: "", places: [], me: null, drive: {}, selected: null, mine: store.get("mine", {}),
  };
  const t = k => T[S.lang][k] ?? T.en[k] ?? k;
  const $ = s => document.querySelector(s);
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // ---------- helpers ----------
  const isFood = p => FOOD.includes(p.type);
  const name = p => (S.lang === "he" ? p.name_he || p.name_en : p.name_en || p.name_he);
  const altName = p => (S.lang === "he" ? p.name_en : p.name_he);
  const kosherOk = p => ["owner_stated", "official"].includes(p.kashrut_status);
  const mine = p => S.mine[p.id] || {};
  const visited = p => (mine(p).visited ?? p.visited) === true;

  function km(a, b) {
    const R = 6371, r = Math.PI / 180, dLat = (b.lat - a.lat) * r, dLng = (b.lng - a.lng) * r;
    const x = Math.sin(dLat / 2) ** 2 + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dLng / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(x));
  }
  const pt = p => (p.type === "hike" ? { lat: p.trailhead_lat ?? p.lat, lng: p.trailhead_lng ?? p.lng } : { lat: p.lat, lng: p.lng });

  function diffClass(d) {
    const s = String(d || "").toLowerCase();
    if (!s || s === "n/a") return "";
    if (s.includes("strenuous")) return "hard";
    if (s.includes("moderate")) return "moderate";
    return s.includes("easy") ? "easy" : "";
  }
  function dairyClass(p) {
    const s = String(p.dairy_meat || "").toLowerCase();
    if (s.startsWith("both")) return ["dairy", "meat"];
    const out = [];
    if (s.includes("dairy") || s.includes("vegetarian")) out.push("dairy");
    if (s.includes("meat")) out.push("meat");
    return out;
  }

  // Parse "08:00-20:00", "09:00-13:00, 16:00-19:00", "15:00-late", "Motzei Shabbat from 21:00" → [[from,to] minutes]
  function intervals(v) {
    if (v == null) return null;
    const s = String(v).toLowerCase();
    if (s.startsWith("closed")) return [];
    const out = [];
    const re = /(\d{1,2}):(\d{2})\s*[-–]\s*(?:(\d{1,2}):(\d{2})|late)/g;
    let m, seasonal = /\(winter\)|\(summer\)/.test(s), winter = [10, 11, 0, 1, 2].includes(new Date().getMonth());
    const parts = seasonal ? s.split("/").filter(x => x.includes(winter ? "winter" : "summer")) : [s];
    for (const part of parts.length ? parts : [s]) {
      re.lastIndex = 0;
      while ((m = re.exec(part))) out.push([+m[1] * 60 + +m[2], m[3] ? (+m[3] * 60 + +m[4] || 1440) : 1440]);
    }
    const from = s.match(/from (\d{1,2}):(\d{2})/);
    if (from && !out.length) out.push([+from[1] * 60 + +from[2], 1440]);
    return out.length ? out : null;
  }
  function hoursOn(p, dayIdx) { return intervals(p.hours?.by_day?.[DAYKEYS[dayIdx]]); }
  function hoursConfirmed(p) { return ["owner_stated", "official"].includes(p.hours?.status); }
  function nowIL() {
    const parts = new Intl.DateTimeFormat("en-US", { timeZone: "Asia/Jerusalem", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).formatToParts(new Date());
    const g = k => parts.find(x => x.type === k)?.value;
    return { day: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(g("weekday")), min: (+g("hour") % 24) * 60 + +g("minute") };
  }
  function openState(p) {
    if (!isFood(p)) return null;
    const n = nowIL(), iv = hoursOn(p, n.day);
    const unconf = !hoursConfirmed(p);
    if (iv == null) return { cls: "", txt: t("hoursUnknown") };
    if (!iv.length) return { cls: "bad", txt: t("closedToday") + (unconf ? ` (${t("unconfShort")})` : "") };
    const open = iv.some(([a, b]) => n.min >= a && n.min < b);
    return { cls: open ? (unconf ? "warn" : "ok") : "bad", txt: (open ? t("openNow") : t("closedNow")) + (unconf ? ` (${t("unconfShort")})` : "") };
  }
  function openIn(p, dayIdx, win) {
    const iv = hoursOn(p, dayIdx);
    if (!iv || !iv.length) return false;
    if (!win) return true;
    const [a, b] = WINDOWS[win];
    return iv.some(([x, y]) => Math.min(y, b) - Math.max(x, a) >= Math.min(60, b - a));
  }

  // ---------- filtering ----------
  function matches(p) {
    const f = S.f, food = isFood(p);
    if (f.types.length && !f.types.includes(p.type)) return false;
    if (f.area && p.area !== f.area) return false;
    if (f.visited === "hide" && visited(p)) return false;
    if (f.visited === "only" && !visited(p)) return false;
    if (S.q) {
      const q = S.q.toLowerCase();
      if (![p.name_en, p.name_he, p.area, p.kashrut_body].some(x => String(x || "").toLowerCase().includes(q))) return false;
    }
    if (food) {
      if (f.levels.length && !f.levels.includes(p.kashrut_level)) return false;
      if (f.onlyConfirmed && !kosherOk(p)) return false;
      if (f.dairy && !dairyClass(p).includes(f.dairy)) return false;
      if (f.day !== "") {
        const d = f.day === "today" ? nowIL().day : +f.day;
        if (!openIn(p, d, f.time)) return false;
      }
    } else {
      const hikeFilters = f.maxLen < 15 || f.diff.length || f.water || f.kids || f.loop || f.stroller;
      if (f.day !== "" && !f.types.includes("hike") && !hikeFilters) return false; // "open on" is a food filter
      if (f.maxLen < 15 && !(p.length_km != null && p.length_km <= f.maxLen)) return false;
      if (f.diff.length && !f.diff.includes(diffClass(p.difficulty))) return false;
      if (f.water && p.water_spring !== true) return false;
      if (f.kids && p.kid_friendly !== true) return false;
      if (f.loop && p.loop !== true) return false;
      if (f.stroller && !/^(yes|mostly|much|most|partly|the |'?much)/i.test(String(p.stroller_ok || ""))) return false;
    }
    // hike-only filters hide food unless type explicitly includes food
    if (food && !f.types.length && (f.maxLen < 15 || f.diff.length || f.water || f.kids || f.loop || f.stroller)) return false;
    if (!food && !f.types.length && (f.levels.length || f.onlyConfirmed || f.dairy)) return false;
    return true;
  }
  const origin = () => S.me || HOME;
  function sortKey(p) {
    const d = S.drive[p.id];
    return d ? d.min : km(origin(), pt(p)) * 1.4; // rough minutes when no routing yet
  }

  // ---------- map ----------
  let map, layer, markers = {}, meMarker;
  function initMap() {
    map = L.map("map", { zoomControl: false }).setView([31.73, 35.04], 10);
    L.control.zoom({ position: "bottomright" }).addTo(map);
    const osm = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    });
    layer = L.layerGroup().addTo(map);
    loadBaseMaps(osm);
  }

  // Google Maps as the base map when a key is configured; OpenStreetMap otherwise or if Google fails.
  function loadBaseMaps(osm) {
    const key = (window.APP_CONFIG || {}).googleMapsKey;
    const useOsm = () => { if (!map.hasLayer(osm)) osm.addTo(map); };
    if (!key || !L.gridLayer.googleMutant || !navigator.onLine) return useOsm();
    let settled = false;
    const fail = () => { if (settled) return; settled = true; useOsm(); };
    const timer = setTimeout(fail, 7000);
    window.gm_authFailure = () => { // bad/blocked key: drop Google layers, keep the app working
      map.eachLayer(l => { if (l instanceof L.GridLayer.GoogleMutant) map.removeLayer(l); });
      settled = false; fail();
    };
    window.__gmReady = () => {
      if (settled) return; settled = true; clearTimeout(timer);
      const road = L.gridLayer.googleMutant({ type: "roadmap", maxZoom: 20 });
      const terrain = L.gridLayer.googleMutant({ type: "terrain", maxZoom: 20 });
      const bases = { "Google": road, "Google terrain": terrain, "OpenStreetMap": osm };
      const saved = store.get("basemap", "Google");
      (bases[saved] || road).addTo(map);
      L.control.layers(bases, null, { position: "topright" }).addTo(map);
      map.on("baselayerchange", e => store.set("basemap", e.name));
    };
    const sc = document.createElement("script");
    sc.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(key)}&loading=async&callback=__gmReady&language=en&region=IL`;
    sc.async = true; sc.onerror = fail;
    document.head.appendChild(sc);
  }
  function pinIcon(p, sel) {
    const cls = `pin ${isFood(p) ? "food" : "hike"}${isFood(p) && !kosherOk(p) ? " unconf" : ""}${sel ? " sel" : ""}`;
    return L.divIcon({ className: "", html: `<div class="${cls}">${ICON[p.type] || "•"}</div>`, iconSize: [32, 32], iconAnchor: [16, 16] });
  }
  function drawMarkers(list) {
    layer.clearLayers(); markers = {};
    for (const p of list) {
      const m = L.marker([p.lat, p.lng], { icon: pinIcon(p, S.selected === p.id), title: name(p) });
      m.on("click", () => openDetail(p.id));
      m.addTo(layer); markers[p.id] = m;
    }
  }

  // ---------- list ----------
  function distLabel(p) {
    const d = S.drive[p.id];
    if (d) return `🚗 ${Math.round(d.min)} ${t("min")}`;
    return `~${km(origin(), pt(p)).toFixed(0)} ${t("km")}`;
  }
  function kosherBadge(p) {
    if (!isFood(p)) return "";
    const lvl = t(p.kashrut_level || "unconfirmed");
    return `<span class="badge ${kosherOk(p) ? "ok" : "warn"}">✡︎ ${esc(lvl)}${kosherOk(p) ? "" : " ?"}</span>`;
  }
  function hikeBadges(p) {
    const b = [];
    if (p.length_km != null) b.push(`${p.length_km} ${t("km")}`);
    const dc = diffClass(p.difficulty); if (dc) b.push(t(dc));
    if (p.loop === true) b.push("↻");
    if (p.water_spring === true) b.push("💧");
    if (p.kid_friendly === true) b.push("👧");
    return b.map(x => `<span class="badge">${esc(x)}</span>`).join("");
  }
  function renderList(list) {
    $("#count").textContent = t("count")(list.length);
    const sg = `<button type="button" class="btn suggest-btn" data-suggest>${t("sgBtn")}</button>`;
    if (!list.length) { $("#list").innerHTML = `<p class="empty">${t("none")}</p>` + sg; return; }
    $("#list").innerHTML = list.map(p => {
      const os = openState(p);
      return `<button class="card" type="button" data-id="${esc(p.id)}">
        <span class="ico ${isFood(p) ? "food" : "hike"}">${ICON[p.type] || ""}</span>
        <span><h3>${esc(name(p))}${visited(p) ? " ✓" : ""}</h3>
          <div class="sub">${esc(t(p.type))} · ${esc(p.area || "")}${isFood(p) && p.kashrut_body && p.kashrut_body !== "not stated" ? " · " + esc(p.kashrut_body) : ""}</div>
          <div class="meta">${kosherBadge(p)}${os ? `<span class="badge ${os.cls}">${esc(os.txt)}</span>` : ""}${hikeBadges(p)}</div>
        </span>
        <span class="dist">${distLabel(p)}</span></button>`;
    }).join("") + sg;
  }

  // ---------- filters UI ----------
  function opt(group, val, label, on) { return `<button type="button" class="opt${on ? " on" : ""}" data-g="${group}" data-v="${esc(val)}">${esc(label)}</button>`; }
  function renderFilters() {
    const f = S.f, areas = [...new Set(S.places.map(p => p.area).filter(Boolean))].sort();
    const dayOpts = [`<option value="">${t("anyDay")}</option>`, `<option value="today"${f.day === "today" ? " selected" : ""}>${t("today")}</option>`]
      .concat(T[S.lang].days.map((d, i) => `<option value="${i}"${f.day === String(i) ? " selected" : ""}>${esc(d)}</option>`)).join("");
    const timeOpts = ["", "morning", "midday", "afternoon", "evening"].map(k => `<option value="${k}"${f.time === k ? " selected" : ""}>${t(k || "anyTime")}</option>`).join("");
    $("#filters").innerHTML = `
      <div class="fgroup"><h4>${t("fType")}</h4><div class="opts">${["cart", "cafe", "food_truck", "hike"].map(x => opt("types", x, `${ICON[x]} ${t(x)}`, f.types.includes(x))).join("")}</div></div>
      <div class="fgroup"><h4>${t("fArea")}</h4><select data-s="area"><option value="">${t("anyArea")}</option>${areas.map(a => `<option${f.area === a ? " selected" : ""}>${esc(a)}</option>`).join("")}</select></div>
      <div class="fgroup"><h4>${t("fOpen")}</h4><div class="row2"><select data-s="day">${dayOpts}</select><select data-s="time">${timeOpts}</select></div></div>
      <div class="fgroup"><h4>${t("fKosher")}</h4><div class="opts">${["badatz", "rabbanut_mehadrin", "rabbanut_regular", "other", "unconfirmed"].map(x => opt("levels", x, t(x), f.levels.includes(x))).join("")}</div>
        <label class="toggle"><input type="checkbox" data-c="onlyConfirmed"${f.onlyConfirmed ? " checked" : ""}> ${t("onlyConfirmed")}</label></div>
      <div class="fgroup"><h4>${t("fDairy")}</h4><div class="opts">${opt("dairy", "", t("any"), !f.dairy)}${opt("dairy", "dairy", t("dairy"), f.dairy === "dairy")}${opt("dairy", "meat", t("meat"), f.dairy === "meat")}</div></div>
      <div class="fgroup"><h4>${t("fHike")}</h4>
        <label>${esc(t("maxLen")(f.maxLen))}<input class="range" type="range" min="2" max="15" step="1" value="${f.maxLen}" data-r="maxLen"></label>
        <div class="opts" style="margin-top:8px">${["easy", "moderate", "hard"].map(x => opt("diff", x, t(x), f.diff.includes(x))).join("")}</div>
        <label class="toggle"><input type="checkbox" data-c="water"${f.water ? " checked" : ""}> 💧 ${t("water")}</label>
        <label class="toggle"><input type="checkbox" data-c="kids"${f.kids ? " checked" : ""}> 👧 ${t("kids")}</label>
        <label class="toggle"><input type="checkbox" data-c="loop"${f.loop ? " checked" : ""}> ↻ ${t("loopOnly")}</label>
        <label class="toggle"><input type="checkbox" data-c="stroller"${f.stroller ? " checked" : ""}> ${t("stroller")}</label></div>
      <div class="fgroup"><h4>${t("fMine")}</h4><div class="opts">${opt("visited", "", t("any"), !f.visited)}${opt("visited", "hide", t("hideVisited"), f.visited === "hide")}${opt("visited", "only", t("onlyVisited"), f.visited === "only")}</div></div>
      <button type="button" class="reset" id="resetF">${t("reset")}</button>
      <button type="button" class="btn suggest-btn" data-suggest>${t("sgBtn")}</button>`;
  }
  function setFilter(mut) { mut(S.f); store.set("filters", S.f); syncQuick(); render(); renderFilters(); }

  // ---------- quick chips ----------
  function syncQuick() {
    const f = S.f, food = f.types.length === 3 && FOOD.every(x => f.types.includes(x));
    const map = { all: !f.types.length && f.day === "", food: food && f.day === "", hike: f.types.length === 1 && f.types[0] === "hike",
      frimorning: f.day === "5" && f.time === "morning" };
    document.querySelectorAll("[data-quick]").forEach(b => b.classList.toggle("on", !!map[b.dataset.quick]));
    $("#nearBtn").classList.toggle("on", !!S.me);
  }

  // ---------- routing (OSRM public demo; light personal use) ----------
  async function driveTimes(from, targets) {
    if (!targets.length) return {};
    const coords = [from, ...targets.map(pt)].map(c => `${c.lng.toFixed(5)},${c.lat.toFixed(5)}`).join(";");
    const ctl = new AbortController(); const timer = setTimeout(() => ctl.abort(), 8000);
    try {
      const r = await fetch(`https://router.project-osrm.org/table/v1/driving/${coords}?sources=0&annotations=duration,distance`, { signal: ctl.signal });
      const j = await r.json();
      if (j.code !== "Ok") throw new Error(j.code);
      const out = {};
      targets.forEach((p, i) => {
        const s = j.durations[0][i + 1], d = j.distances[0][i + 1];
        if (s != null) out[p.id] = { min: s / 60, km: d / 1000 };
      });
      return out;
    } catch { return null; } finally { clearTimeout(timer); }
  }
  async function locate() {
    if (!navigator.geolocation) return alert(t("locErr"));
    navigator.geolocation.getCurrentPosition(async pos => {
      S.me = { lat: pos.coords.latitude, lng: pos.coords.longitude };
      if (meMarker) meMarker.remove();
      meMarker = L.marker([S.me.lat, S.me.lng], { icon: L.divIcon({ className: "", html: '<div class="me-dot"></div>', iconSize: [16, 16], iconAnchor: [8, 8] }), interactive: false }).addTo(map);
      map.setView([S.me.lat, S.me.lng], 11);
      S.drive = {}; syncQuick(); render();
      const near = S.places.slice().sort((a, b) => km(S.me, pt(a)) - km(S.me, pt(b))).slice(0, 60);
      const d = await driveTimes(S.me, near);
      if (d) { S.drive = d; render(); }
    }, () => alert(t("locErr")), { enableHighAccuracy: true, timeout: 12000, maximumAge: 300000 });
  }

  // ---------- detail ----------
  function linkGmaps(p) {
    if (isFood(p) && p.google_maps_url) return p.google_maps_url; // search by name → reviews & photos
    const c = pt(p); return `https://www.google.com/maps/search/?api=1&query=${c.lat},${c.lng}`;
  }
  function linkWaze(p) { const c = pt(p); return `https://waze.com/ul?ll=${c.lat},${c.lng}&navigate=yes`; }
  const row = (k, v) => (v == null || v === "" || v === "not stated" ? "" : `<dt>${esc(t(k))}</dt><dd>${esc(v)}</dd>`);
  function hoursTable(p) {
    const today = nowIL().day, bd = p.hours?.by_day || {};
    if (!DAYKEYS.some(k => bd[k])) return `<p class="note">${t("hoursUnknown")}</p>`;
    return `<table class="hours">${DAYKEYS.map((k, i) => `<tr class="${i === today ? "today" : ""}${i === 5 ? " fri" : ""}"><td>${esc(T[S.lang].days[i])}</td><td>${esc(bd[k] == null ? "?" : String(bd[k]).toLowerCase() === "closed" ? t("closedDay") : bd[k])}</td></tr>`).join("")}</table>`;
  }
  function openDetail(id) {
    const p = S.places.find(x => x.id === id); if (!p) return;
    S.selected = id; render();
    const c = pt(p); map.setView([p.lat, p.lng], Math.max(map.getZoom(), 12));
    const food = isFood(p), m = mine(p), os = openState(p);
    const actions = [
      `<a class="btn primary" href="${esc(linkGmaps(p))}" target="_blank" rel="noopener">📍 ${t("gmaps")}</a>`,
      `<a class="btn" href="${esc(linkWaze(p))}" target="_blank" rel="noopener">🚗 ${t("waze")}</a>`,
      p.phone ? `<a class="btn" href="tel:${esc(p.phone.replace(/[^0-9+]/g, ""))}">📞 ${t("call")}</a>` : "",
      p.instagram ? `<a class="btn" href="${esc(p.instagram)}" target="_blank" rel="noopener">📷 ${t("insta")}</a>` : "",
      p.website ? `<a class="btn" href="${esc(p.website)}" target="_blank" rel="noopener">🌐 ${t("web")}</a>` : "",
    ].join("");
    const kosher = food ? `<div class="box"><h4>${t("kosherBy")}</h4><dl class="kv">
        ${row("body", p.kashrut_body)}${row("level", t(p.kashrut_level || "unconfirmed"))}
        <dt>${t("status")}</dt><dd><span class="badge ${kosherOk(p) ? "ok" : "warn"}">${esc(t("st_" + p.kashrut_status))}</span></dd>
        ${row("dairyMeat", p.dairy_meat)}${row("lastChecked", p.last_checked)}</dl>
        ${p.kashrut_note ? `<p class="note">${esc(p.kashrut_note)}</p>` : ""}</div>` : "";
    const hours = food || p.hours?.status === "official" ? `<div class="box"><h4>${t("hours")} ${os ? `<span class="badge ${os.cls}">${esc(os.txt)}</span>` : ""}</h4>
        ${hoursTable(p)}<p class="note">${t("status")}: ${esc(t("st_" + (p.hours?.status || "unconfirmed")))} · ${t("lastChecked")}: ${esc(p.last_checked)}. ${p.hours?.notes ? esc(p.hours.notes) + " " : ""}${t("hoursNote")}</p></div>` : "";
    const trail = !food ? `<div class="box"><h4>${t("trail")}</h4><dl class="kv">
        ${row("length", p.length_text ? p.length_text + " " + t("km") : p.length_km != null ? p.length_km + " " + t("km") : "")}
        ${row("time", p.duration_text ? p.duration_text + " " + t("hrs") : p.duration_hrs != null ? p.duration_hrs + " " + t("hrs") : "")}
        ${row("difficulty", p.difficulty)}${row("route", p.route_type ?? (p.loop === true ? "loop" : p.loop === false ? "one-way / out-and-back" : ""))}
        ${row("colors", p.trail_colors)}${row("waterSpring", p.water_text ?? (p.water_spring ? t("yes") : ""))}${row("pool", p.swimmable_pool)}
        ${row("shade", p.shade)}${row("season", p.best_season)}${row("kidsL", p.kid_text ?? (p.kid_friendly === true ? t("yes") : p.kid_friendly === false ? t("no") : ""))}
        ${row("strollerL", p.stroller_ok)}${row("parking", p.parking_location)}
        ${row("fee", p.fee_text ?? (p.entrance_fee === true ? t("paid") : p.entrance_fee === false ? t("free") : ""))}
        ${row("details", p.details_source)}</dl>
        ${p.warnings ? `<p class="note">⚠️ <b>${t("warnings")}:</b> ${esc(p.warnings)}</p>` : ""}</div>` : "";
    const notes = [p.seasonal_notes, p.my_notes, p.hith_notes].filter(Boolean).map(esc).join("<br>");
    $("#detail").innerHTML = `
      <button class="iconbtn close" type="button" id="closeDetail" aria-label="${t("back")}">✕</button>
      <div class="badge">${ICON[p.type]} ${esc(t(p.type))} · ${esc(p.area || "")}</div>
      <h2>${esc(name(p))}</h2><p class="alt">${esc(altName(p) || "")}</p>
      <div class="actions">${actions}</div>
      ${kosher}${hours}${trail}
      <div class="box"><h4>${food ? t("nearbyHikes") : t("pairings")}</h4><div id="pairs" class="note">${t("findingPairs")}</div></div>
      ${notes ? `<div class="box"><h4>${t("notes")}</h4><p class="note">${notes}</p></div>` : ""}
      <div class="box"><h4>${t("myNotes")}</h4>
        <label class="toggle"><input type="checkbox" id="visitedBox"${visited(p) ? " checked" : ""}> ${t("visited")}</label>
        <textarea id="myNote">${esc(m.note ?? "")}</textarea></div>
      <div class="box sources"><h4>${t("sources")}</h4>${(p.source_urls || []).map(u => `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(decodeURI(u))}</a>`).join("")}
        <p class="note">${t("coords")}: ${c.lat.toFixed(5)}, ${c.lng.toFixed(5)} — ${esc(p.coords_confidence || "")}</p></div>`;
    $("#detail").classList.remove("hidden"); $("#detail").scrollTop = 0;
    $("#closeDetail").onclick = closeDetail;
    $("#visitedBox").onchange = e => { saveMine(p.id, { visited: e.target.checked }); render(); };
    $("#myNote").oninput = e => saveMine(p.id, { note: e.target.value });
    loadPairs(p);
  }
  function closeDetail() { $("#detail").classList.add("hidden"); S.selected = null; render(); }
  function saveMine(id, patch) { S.mine[id] = Object.assign({}, S.mine[id], patch); store.set("mine", S.mine); }

  async function loadPairs(p) {
    const from = pt(p), food = isFood(p);
    const cands = S.places.filter(x => x.id !== p.id && (food ? x.type === "hike" : isFood(x)) && km(from, pt(x)) <= 18);
    let d = await driveTimes(from, cands), approx = false;
    if (S.selected !== p.id) return;
    let list;
    if (d) list = cands.filter(x => d[x.id] && d[x.id].min <= 15).map(x => ({ x, min: d[x.id].min, km: d[x.id].km }));
    else { approx = true; list = cands.filter(x => km(from, pt(x)) <= 10).map(x => ({ x, km: km(from, pt(x)) })); }
    list.sort((a, b) => (a.min ?? a.km) - (b.min ?? b.km));
    const el = $("#pairs"); if (!el) return;
    if (!list.length) { el.textContent = t("noPairs"); return; }
    el.classList.remove("note");
    el.innerHTML = (approx ? `<p class="note">${t("approxDrive")}</p>` : "") + list.map(({ x, min, km: k }) => {
      const fri = isFood(x) ? (openIn(x, 5, "morning") ? `<span class="badge ok">${esc(T[S.lang].daysShort[5])} ✓</span>` : "") : "";
      return `<div class="pair" data-id="${esc(x.id)}"><span>${ICON[x.type]} ${esc(name(x))}
          <small>${isFood(x) ? `${[x.kashrut_body && x.kashrut_body !== "not stated" ? esc(x.kashrut_body) : "", esc(t(x.kashrut_level || "unconfirmed"))].filter(Boolean).join(" · ")}${kosherOk(x) ? "" : " ?"}` : esc([x.length_km != null ? x.length_km + " " + t("km") : "", x.difficulty].filter(Boolean).join(" · "))}</small></span>
        <span>${min != null ? `🚗 ${Math.round(min)} ${t("min")}` : `~${k.toFixed(1)} ${t("km")}`} ${fri}</span></div>`;
    }).join("");
  }

  // ---------- suggest a place (→ GitHub issue that Claude processes) ----------
  function openSuggest(link = "", notes = "") {
    const d = $("#suggest"); $("#sgLink").value = link; $("#sgNotes").value = notes;
    if (d.showModal) d.showModal(); else d.setAttribute("open", "");
  }
  function sendSuggest() {
    const link = $("#sgLink").value.trim(); if (!link) return;
    const repo = (window.APP_CONFIG || {}).requestRepo || "freedscot/Daniel";
    const handle = (link.match(/instagram\.com\/([A-Za-z0-9_.]+)/) || [])[1];
    const title = `Add place: ${handle ? "@" + handle : link}`;
    const body = `Link: ${link}\n\nNotes: ${$("#sgNotes").value.trim() || "-"}\n\nRequested from the Coffee & Tiyul app on ${new Date().toISOString().slice(0, 10)}.\nClaude: follow .claude/skills/add-place/SKILL.md.`;
    window.open(`https://github.com/${repo}/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`, "_blank", "noopener");
  }
  function handleShare() { // Android "Share → Coffee & Tiyul" lands here with share_* params
    const q = new URLSearchParams(location.search);
    const raw = [q.get("share_url"), q.get("share_text"), q.get("share_title")].filter(Boolean).join(" ");
    if (!raw) return;
    const link = (raw.match(/https?:\/\/\S+/) || [""])[0];
    history.replaceState(null, "", location.pathname);
    openSuggest(link, link ? raw.replace(link, "").trim() : raw);
  }

  // ---------- render ----------
  function render() {
    const list = S.places.filter(matches).sort((a, b) => sortKey(a) - sortKey(b));
    drawMarkers(list); renderList(list);
  }
  function applyLang() {
    document.documentElement.lang = S.lang; document.documentElement.dir = S.lang === "he" ? "rtl" : "ltr";
    document.querySelectorAll("[data-t]").forEach(el => { el.textContent = t(el.dataset.t); });
    document.querySelectorAll("[data-tp]").forEach(el => { el.placeholder = t(el.dataset.tp); });
    $("#langBtn").textContent = S.lang === "he" ? "EN" : "עב";
    document.title = t("appName");
  }

  // ---------- events ----------
  function bind() {
    $("#langBtn").onclick = () => { S.lang = S.lang === "he" ? "en" : "he"; store.set("lang", S.lang); applyLang(); renderFilters(); render(); if (S.selected) openDetail(S.selected); };
    $("#search").oninput = e => { S.q = e.target.value.trim(); render(); };
    $("#nearBtn").onclick = locate;
    document.querySelectorAll("[data-quick]").forEach(b => b.onclick = () => setFilter(f => {
      const k = b.dataset.quick;
      if (k === "all") Object.assign(f, { types: [], day: "", time: "" });
      if (k === "food") Object.assign(f, { types: FOOD.slice(), day: "", time: "" });
      if (k === "hike") Object.assign(f, { types: ["hike"], day: "", time: "" });
      if (k === "frimorning") Object.assign(f, { types: FOOD.slice(), day: "5", time: "morning" });
    }));
    $("#list").onclick = e => { const c = e.target.closest(".card"); if (c) openDetail(c.dataset.id); };
    $("#detail").addEventListener("click", e => { const c = e.target.closest(".pair"); if (c) openDetail(c.dataset.id); });
    document.querySelectorAll(".tab").forEach(b => b.onclick = () => {
      document.querySelectorAll(".tab").forEach(x => x.classList.toggle("active", x === b));
      $("#list").classList.toggle("hidden", b.dataset.tab !== "list");
      $("#filters").classList.toggle("hidden", b.dataset.tab !== "filters");
      const sh = $("#sheet"); if (sh.classList.contains("peek")) { sh.classList.remove("peek"); sh.classList.add("half"); }
    });
    $("#sheetHandle").onclick = () => {
      const sh = $("#sheet"), order = ["peek", "half", "full"], cur = order.find(c => sh.classList.contains(c)) || "peek";
      sh.classList.remove(cur); sh.classList.add(order[(order.indexOf(cur) + 1) % 3]);
    };
    $("#filters").addEventListener("click", e => {
      const b = e.target.closest(".opt");
      if (b) setFilter(f => {
        const g = b.dataset.g, v = b.dataset.v;
        if (Array.isArray(f[g])) f[g] = f[g].includes(v) ? f[g].filter(x => x !== v) : f[g].concat(v); else f[g] = v;
      });
      if (e.target.id === "resetF") setFilter(f => Object.assign(f, structuredClone(DEFAULT_F)));
    });
    $("#filters").addEventListener("change", e => {
      const el = e.target;
      if (el.dataset.s) setFilter(f => { f[el.dataset.s] = el.value; });
      if (el.dataset.c) setFilter(f => { f[el.dataset.c] = el.checked; });
      if (el.dataset.r) setFilter(f => { f[el.dataset.r] = +el.value; });
    });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && S.selected) closeDetail(); });
    document.addEventListener("click", e => { if (e.target.closest("[data-suggest]")) openSuggest(); });
    $("#suggestForm").addEventListener("submit", e => { // open GitHub inside the tap so it isn't popup-blocked
      if (e.submitter && e.submitter.value === "send") { e.preventDefault(); sendSuggest(); $("#suggest").close(); }
    });
  }

  // ---------- boot ----------
  async function boot() {
    applyLang(); initMap(); bind();
    try {
      const r = await fetch("data/places.json", { cache: "no-cache" });
      S.places = (await r.json()).places;
    } catch { $("#list").innerHTML = `<p class="empty">Couldn't load data/places.json</p>`; return; }
    renderFilters(); syncQuick(); render();
    const hash = decodeURIComponent(location.hash.slice(1)); if (hash) openDetail(hash);
    handleShare();
    if ("serviceWorker" in navigator && location.protocol === "https:") navigator.serviceWorker.register("sw.js").catch(() => {});
  }
  window.__app = { S, intervals, openIn, matches, nowIL }; // for tests
  boot();
})();
