"""Adds/updates hikes from data/sources/hith_hikes.csv (Hiking the Holyland posts, read in full)."""
import csv, re, pathlib
import hith_mapping as M

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = "Hiking the Holyland"

def load():
    rows = {}
    for r in csv.DictReader(open(ROOT / "data/sources/hith_hikes.csv", encoding="utf-8")):
        rows[r["post_url"].rstrip("/").split("/")[-1]] = r
    return rows

def num(s):
    m = re.search(r"(\d+(?:\.\d+)?|\.\d+)", s or "")
    return float(m.group(1)) if m else None

def loop(route):
    r = route.lower()
    if r.startswith("loop"): return True
    if r.startswith(("out-and-back", "one-way")): return False
    return None

def yes(s):
    s = s.lower()
    if s.startswith("yes"): return True
    if s.startswith(("no", "not for kids", "'i’m not marking", "'not for")): return False
    return None

def fee(s):
    s = s.lower()
    if s.startswith("free"): return False
    if s.startswith("yes") or "nis" in s: return True
    return None

def ns(s): return None if s.strip().lower() == "not stated" else s

def details(r):
    """Hike fields taken from one post row."""
    return dict(
        length_km=num(r["length_km"]), length_text=r["length_km"], route_type=r["route_type"], loop=loop(r["route_type"]),
        duration_hrs=num(r["duration_hrs"]), duration_text=r["duration_hrs"], difficulty=r["difficulty"],
        trail_colors=ns(r["trail_colors"]), water_spring=yes(r["water_spring"]), water_text=ns(r["water_spring"]),
        swimmable_pool=ns(r["swimmable_pool"]), shade=ns(r["shade"]), best_season=ns(r["best_season"]),
        kid_friendly=yes(r["kid_friendly"]), kid_text=ns(r["kid_friendly"]), stroller_ok=ns(r["stroller_ok"]),
        parking_location=ns(r["parking_location"]), entrance_fee=fee(r["entrance_fee"]), fee_text=ns(r["entrance_fee"]),
        warnings=ns(r["warnings"]),
        details_source=f"{SRC} post ({r['post_date']})", details_status="blog_post", post_date=r["post_date"],
    )

def also_text(rows, slugs):
    out = []
    for s in slugs:
        r = rows[s]
        out.append(f"Also on {SRC}: \"{r['name_en']}\" – {r['length_km']} km, {r['route_type'].split(' (')[0]}, {r['difficulty']}.")
    return " ".join(out)

def apply(PLACES, place, hike, hours):
    rows = load()
    by_id = {p["id"]: p for p in PLACES}
    for pid, (slug, also) in M.UPDATE.items():
        p, r = by_id[pid], rows[slug]
        keep_official = p.get("details_status") == "official"
        d = details(r)
        if keep_official:   # official hours/fees stay; post supplies the trail itself
            d.pop("entrance_fee"); d.pop("fee_text")
        p.update(d)
        p["source_urls"] = [r["post_url"]] + [rows[s]["post_url"] for s in also] + [u for u in p["source_urls"] if "hikingintheholyland" not in u]
        extra = also_text(rows, also)
        if extra: p["my_notes"] = (p["my_notes"] + " " + extra).strip()
        p["last_checked"] = "2026-11-26"
    for pid, slug in M.EXTRA_SOURCE.items():
        by_id[pid]["source_urls"].append(rows[slug]["post_url"])
        by_id[pid]["hith_notes"] = f"{SRC}: {rows[slug]['length_km']} km, {rows[slug]['difficulty']}; warnings: {rows[slug]['warnings']}"
    for slug, m in M.NEW.items():
        r = rows[slug]
        h = hike(id=m["id"], name_he=m["name_he"], name_en=r["name_en"], lat=m["lat"], lng=m["lng"],
                 coords_confidence=m["conf"], area=m["area"],
                 hours=hours(None, None, sat=None, status="n/a"),
                 source_urls=[r["post_url"]] + [rows[s]["post_url"] for s in m["also"]],
                 my_notes=" ".join(x for x in [m["note"], also_text(rows, m["also"])] if x))
        h.update(details(r))
        assert h["id"] not in by_id, h["id"]
        PLACES.append(h); by_id[h["id"]] = h
