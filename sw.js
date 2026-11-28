// Offline support: app shell cache-first, place data network-first, map tiles cached as you browse.
const VERSION = "v8";
const SHELL = ["./", "index.html", "styles.css", "app.js", "manifest.webmanifest", "vendor/leaflet/leaflet.js",
  "vendor/leaflet/leaflet.css", "vendor/googlemutant/Leaflet.GoogleMutant.js", "config.js", "icons/icon-192.png", "icons/icon-512.png"];
const TILE_LIMIT = 600;

self.addEventListener("install", e => e.waitUntil(caches.open("shell-" + VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("shell-") && k !== "shell-" + VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim())));

async function trimTiles(cache) {
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - TILE_LIMIT; i++) await cache.delete(keys[i]);
}

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET") return;
  if (url.hostname === "tile.openstreetmap.org") {
    e.respondWith(caches.open("tiles").then(async c => {
      const hit = await c.match(e.request);
      if (hit) return hit;
      const res = await fetch(e.request);
      if (res.ok) { c.put(e.request, res.clone()); trimTiles(c); }
      return res;
    }));
    return;
  }
  if (url.origin !== location.origin) return; // routing API etc. go straight to the network
  if (url.pathname.endsWith("/data/places.json")) {
    e.respondWith(fetch(e.request).then(res => {
      const copy = res.clone(); caches.open("data").then(c => c.put(e.request, copy)); return res;
    }).catch(() => caches.match(e.request)));
    return;
  }
  e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request)));
});
