"""Helper for adding a place from an Instagram link (see .claude/skills/add-place/SKILL.md).

  python3 scripts/add_place.py lookup <instagram link | @handle | name>
      Finds the place in the CoffeeTrail index and says whether it's already on the map.
  python3 scripts/add_place.py gmaps <Google Maps link> [shared text]
      Reads a Google Maps share link (maps.app.goo.gl/... or google.com/maps/...): name, exact pin,
      duplicates already on the map, and nearby CoffeeTrail listings.
  python3 scripts/add_place.py draft-gmaps <Google Maps link> --name-en "English name" [--name-he "שם"] [--type cart|cafe|food_truck|restaurant]
      Appends a draft from the Google Maps pin with kashrut/hours UNCONFIRMED - research them, then edit.
  python3 scripts/add_place.py draft <coffeetrail-slug> [--name-en "English name"] [--type cart|cafe|food_truck]
      Appends a draft entry to data/sources/added_places.json, filled from the CoffeeTrail listing
      with the project's kashrut rules. Review/edit the entry, then run: python3 scripts/build_data.py
"""
import json, math, pathlib, re, sys, datetime
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "data/sources/coffeetrail_index.json"
ADDED = ROOT / "data/sources/added_places.json"
PLACES = ROOT / "data/places.json"

def handle_of(s):
    m = re.search(r"instagram\.com/([A-Za-z0-9_.]+)", s)
    if m: return m.group(1).lower().rstrip(".")
    return s.lstrip("@").lower() if re.fullmatch(r"@?[A-Za-z0-9_.]+", s) else None

def km(a, b):
    r = math.pi / 180
    x = math.sin((b[0] - a[0]) * r / 2) ** 2 + math.cos(a[0] * r) * math.cos(b[0] * r) * math.sin((b[1] - a[1]) * r / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(x))

def kashrut(text, verified):
    """Map CoffeeTrail's Hebrew kashrut sentence to (body, level, status). Never guesses a body."""
    if not text:
        return "not stated", "unconfirmed", "unconfirmed"
    t = text.replace("״", '"').replace("''", '"')
    m = re.search(r"(?:של|בהשגחת)\s+(.+)$", t) or re.search(r"כשרות\s+(?:ל?מהדרין)?[,\s]*(.+)$", t)
    body = m.group(1).strip(" ,") if m else ""
    if body in ("", "מהדרין", "למהדרין"): body = "not stated"
    if re.search(r'בד"?\'?צ', t): level = "badatz"
    elif "מהדרין" in t and re.search(r"רבנות|מועצה", t): level = "rabbanut_mehadrin"
    elif "מהדרין" in t: level = "unconfirmed"   # Mehadrin certificate but no certifying body named
    elif re.search(r"רבנות|מועצה", t): level = "rabbanut_regular"
    else: level = "other"
    return body, level, ("owner_stated" if verified else "third_party")

def resolve_gmaps(link):
    """Follow a Google Maps (short) link's redirects WITHOUT loading Maps; return (final_url, name, lat, lng, how)."""
    import subprocess
    from urllib.parse import unquote, urlparse, parse_qs
    m = re.search(r"https?://\S+", link); url = m.group(0) if m else link
    for _ in range(6):
        if "google." in urlparse(url).netloc and "/maps" in url: break
        r = subprocess.run(["curl", "-sI", "--max-time", "20", "-A", "Mozilla/5.0", url], capture_output=True, text=True).stdout
        loc = re.search(r"^location:\s*(\S+)", r, re.I | re.M)
        if not loc: break
        url = loc.group(1)
    name = lat = lng = None; how = None
    m = re.search(r"/maps/place/([^/@?]+)", url)
    if m: name = unquote(m.group(1).replace("+", " "))
    m = re.search(r"!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)", url)          # the place's own pin
    if m: lat, lng, how = float(m.group(1)), float(m.group(2)), "exact (Google Maps place pin)"
    else:
        m = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", url)          # map centre
        if m: lat, lng, how = float(m.group(1)), float(m.group(2)), "approx (Google Maps view centre)"
    if lat is None and name and "," in name:   # e.g. "חווה באלה, Tsafririm" – fall back to the village centre
        import time, subprocess as sp
        town = name.split(",")[-1].strip().strip("\u200e\u200f\u202a\u202b\u202c\u202d")
        from urllib.parse import urlencode
        out = sp.run(["curl", "-s", "--max-time", "20", "-A", "kosher-map-data-builder/0.1",
                      "https://nominatim.openstreetmap.org/search?" + urlencode(dict(q=town, format="json", limit=1, countrycodes="il"))],
                     capture_output=True, text=True).stdout
        try:
            r = json.loads(out)
            if r: lat, lng, how = float(r[0]["lat"]), float(r[0]["lon"]), f"approx ({town} village centre – the Google link had no pin)"
        except ValueError:
            pass
        name = name.split(",")[0].strip()
    q = parse_qs(urlparse(url).query)
    if not name and q.get("q"):
        v = q["q"][0]; mm = re.fullmatch(r"\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\s*", v)
        if mm and lat is None: lat, lng, how = float(mm.group(1)), float(mm.group(2)), "exact (coordinates in the link)"
        elif not mm: name = v
    return url, name, lat, lng, how

def gmaps(link, shared=""):
    url, name, lat, lng, how = resolve_gmaps(link)
    if not name and shared: name = shared.strip().split("\n")[0][:80]
    print(json.dumps(dict(final_url=url, name=name, lat=lat, lng=lng, coords=how), ensure_ascii=False, indent=1))
    if lat is None:
        print("No pin in the link. Ask the owner for the full link, or look the place up by name.")
        return
    dup = [(p["id"], round(km((p["lat"], p["lng"]), (lat, lng)) * 1000)) for p in places() if km((p["lat"], p["lng"]), (lat, lng)) < 0.3]
    print("ON THE MAP WITHIN 300 m:", dup or "none")
    carts = json.loads(INDEX.read_text(encoding="utf-8"))["carts"]
    near = sorted(((round(km((c["lat"], c["lng"]), (lat, lng)) * 1000), c["slug"], c["name"], c["kashrut_text"]) for c in carts if c["lat"] and km((c["lat"], c["lng"]), (lat, lng)) < 0.5))
    print("COFFEETRAIL LISTINGS WITHIN 500 m (m, slug, name, kashrut):", near or "none")
    print("Next: research kashrut/hours (own site/Instagram via search, kasher.info registry for the town, CoffeeTrail), then draft-gmaps.")

def draft_gmaps(link, name_en, name_he=None, ptype="cafe"):
    url, name, lat, lng, how = resolve_gmaps(link)
    if lat is None: sys.exit("No pin in the link.")
    name_he = name_he or name or name_en
    near = min(places(), key=lambda p: km((p["lat"], p["lng"]), (lat, lng)))
    area = near["area"] if km((near["lat"], near["lng"]), (lat, lng)) < 10 else "SET AREA"
    entry = dict(id=re.sub(r"[^a-z0-9]+", "-", name_en.lower()).strip("-"), type=ptype, name_he=name_he, name_en=name_en,
        lat=round(lat, 6), lng=round(lng, 6), coords_confidence=how, area=area,
        kashrut_body="not stated", kashrut_level="unconfirmed", kashrut_status="unconfirmed",
        kashrut_note="Added from a Google Maps link; hechsher not yet researched.", dairy_meat="unconfirmed",
        hours={"by_day": {k: None for k in ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]}, "status": "unconfirmed", "notes": ""},
        instagram=None, website=None, phone=None, google_maps_url=link.strip(), source_urls=[link.strip()],
        last_checked=datetime.date.today().isoformat(), my_notes="Added from a Google Maps link.", visited=False)
    added = json.loads(ADDED.read_text(encoding="utf-8"))
    if any(e["id"] == entry["id"] for e in added) or any(p["id"] == entry["id"] for p in places()):
        sys.exit(f"id {entry['id']} already exists")
    added.append(entry); ADDED.write_text(json.dumps(added, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(entry, ensure_ascii=False, indent=1))

def places():
    return json.loads(PLACES.read_text(encoding="utf-8"))["places"]

def lookup(q):
    carts = json.loads(INDEX.read_text(encoding="utf-8"))["carts"]
    h = handle_of(q)
    hits = [c for c in carts if h and c["instagram_handle"] == h] or \
           [c for c in carts if h and c["instagram_handle"] and (h in c["instagram_handle"] or c["instagram_handle"] in h)] or \
           [c for c in carts if q.strip().lower() in (c["name"] or "").lower()]
    if not hits:
        print(f"No CoffeeTrail match for {q!r} (handle {h!r}). Research it another way (Etzion Tourism, web search).")
    for c in hits:
        print(json.dumps(c, ensure_ascii=False, indent=1))
        dup = [p for p in places() if (c["lat"] and km((p["lat"], p["lng"]), (c["lat"], c["lng"])) < 0.15)
               or (h and h in (p.get("instagram") or "").lower())]
        print("ALREADY ON MAP:", [p["id"] for p in dup] if dup else "no")
    return hits

def draft(slug, name_en=None, ptype="cart"):
    carts = {c["slug"]: c for c in json.loads(INDEX.read_text(encoding="utf-8"))["carts"]}
    c = carts[slug]
    if not c["lat"]:
        sys.exit("Listing has no coordinates - find the location another way.")
    body, level, status = kashrut(c["kashrut_text"], c["verified_listing"])
    near = min(places(), key=lambda p: km((p["lat"], p["lng"]), (c["lat"], c["lng"])))
    area = near["area"] if km((near["lat"], near["lng"]), (c["lat"], c["lng"])) < 10 else "SET AREA"
    notes = [f"CoffeeTrail: '{c['kashrut_text']}'" if c["kashrut_text"] else "CoffeeTrail lists no kashrut.",
             "Owner-verified listing." if c["verified_listing"] else "Listing NOT verified by the owner.",
             "Certificate not seen."]
    if c["open_on_shabbat"]: notes.append("WARNING: listing says it is open on Shabbat - check before treating as kosher.")
    hrs = c["hours"] or {}
    entry = dict(
        id=re.sub(r"[^a-z0-9]+", "-", (name_en or slug).lower()).strip("-"), type=ptype,
        name_he=c["name"], name_en=name_en or c["name"], lat=c["lat"], lng=c["lng"],
        coords_confidence="exact (CoffeeTrail pin)", area=area,
        kashrut_body=body, kashrut_level=level, kashrut_status=status, kashrut_note=" ".join(notes),
        dairy_meat="unconfirmed",
        hours={"by_day": {k: hrs.get(k) for k in ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]},
               "status": status if hrs else "unconfirmed", "notes": c["owner_note"]},
        instagram=c["instagram"], website=None, phone=c["phone"],
        google_maps_url="https://www.google.com/maps/search/?api=1&query=" + quote(f"{c['name']} {c['address']}"),
        source_urls=[c["url"]], last_checked=datetime.date.today().isoformat(),
        my_notes=f"Address: {c['address']}. Added from an Instagram link.", visited=False,
    )
    added = json.loads(ADDED.read_text(encoding="utf-8"))
    if any(e["id"] == entry["id"] for e in added) or any(p["id"] == entry["id"] for p in places()):
        sys.exit(f"id {entry['id']} already exists")
    added.append(entry)
    ADDED.write_text(json.dumps(added, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(entry, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "lookup": lookup(" ".join(a[1:]))
    elif len(a) >= 2 and a[0] == "gmaps": gmaps(a[1], " ".join(a[2:]))
    elif len(a) >= 2 and a[0] == "draft-gmaps":
        opt = lambda k: a[a.index(k) + 1] if k in a else None
        draft_gmaps(a[1], opt("--name-en") or sys.exit("--name-en is required"), opt("--name-he"), opt("--type") or "cafe")
    elif len(a) >= 2 and a[0] == "draft":
        opt = lambda k: a[a.index(k) + 1] if k in a else None
        draft(a[1], opt("--name-en"), opt("--type") or "cart")
    else: print(__doc__)
