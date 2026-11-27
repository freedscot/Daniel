"""Helper for adding a place from an Instagram link (see .claude/skills/add-place/SKILL.md).

  python3 scripts/add_place.py lookup <instagram link | @handle | name>
      Finds the place in the CoffeeTrail index and says whether it's already on the map.
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
    elif len(a) >= 2 and a[0] == "draft":
        opt = lambda k: a[a.index(k) + 1] if k in a else None
        draft(a[1], opt("--name-en"), opt("--type") or "cart")
    else: print(__doc__)
