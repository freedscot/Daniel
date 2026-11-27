"""Build data/sources/coffeetrail_index.json: one entry per CoffeeTrail cart page
(name, address, pin, Instagram/Facebook, phone, kashrut text, hours, owner-verified flag).

Used to match an Instagram link to a cart. Run:  python3 scripts/coffeetrail_index.py
(downloads ~450 pages politely; takes a few minutes). --cache DIR reuses saved pages.
"""
import html, json, pathlib, re, subprocess, sys, time, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data/sources/coffeetrail_index.json"
DAYS_HE = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
DAYKEYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]

def get(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", "Mozilla/5.0", url], capture_output=True, text=True)
    return r.stdout

def handle(url):
    m = re.search(r"instagram\.com/([A-Za-z0-9_.]+)", url or "")
    return m.group(1).lower().rstrip(".") if m else None

def parse(slug, t):
    lat = re.findall(r'"(?:lat|latitude)"\s*:\s*"?([0-9.]+)', t)
    lng = re.findall(r'"(?:lng|longitude)"\s*:\s*"?([0-9.]+)', t)
    t2 = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", t, flags=re.S)
    out = " | ".join(l.strip() for l in html.unescape(re.sub(r"<[^>]+>", "\n", t2)).split("\n") if l.strip())
    a = out.find("opening tag is omitted"); body = out[a:out.find("אנחנו על המפה")] if a >= 0 else ""
    parts = body.split(" | ")
    name = parts[2] if len(parts) > 2 else ""
    addr = parts[parts.index("כתובת") + 1] if "כתובת" in parts else ""
    k = re.search(r"סוג הכשרות \| ([^|]+)", body)
    hrs = {}
    m = re.search(r"כל שעות הפתיחה \| (.*?) \| על העגלה", body)
    if m:
        seg = m.group(1).split(" | ")
        for i, x in enumerate(seg):
            if x in DAYS_HE and i + 1 < len(seg):
                v = seg[i + 1].replace(" ", "")
                hrs[DAYKEYS[DAYS_HE.index(x)]] = "closed" if "סגור" in seg[i + 1] else v
    note = re.search(r"שימו לב \| ([^|]+)", body)
    feats = re.search(r"מאפייני העגלה \| (.*?) \| תראו אותנו", body)
    feats = feats.group(1).split(" | ") if feats else []
    igs = [x for x in re.findall(r'https?://(?:www\.)?instagram\.com/[^"\'?\s<]+', t) if "coffeetrail" not in x.lower()]
    fbs = [x for x in re.findall(r'https?://(?:www\.)?facebook\.com/[^"\'?\s<]+', t) if "coffeetrail" not in x.lower() and "sharer" not in x]
    phone = re.findall(r'href="tel:([0-9+\-]+)"', t)
    return dict(slug=slug, url=f"https://coffeetrail.co.il/coffeecart/{urllib.parse.quote(slug)}/", name=name, address=addr,
                lat=float(lat[0]) if lat else None, lng=float(lng[0]) if lng else None,
                kashrut_text=k.group(1).strip() if k else None, kosher_features=[x for x in feats if "כשר" in x],
                open_on_shabbat="פתוח בשבת" in feats, verified_listing="Verified listing" in body,
                hours=hrs, owner_note=note.group(1).strip() if note else "",
                instagram=igs[0] if igs else None, instagram_handle=handle(igs[0]) if igs else None,
                facebook=fbs[0] if fbs else None, phone=phone[0] if phone else None)

def main():
    cache = pathlib.Path(sys.argv[sys.argv.index("--cache") + 1]) if "--cache" in sys.argv else None
    urls = []
    for n in ["", "2", "3", "4"]:
        urls += re.findall(r"<loc>(https://coffeetrail\.co\.il/coffeecart/[^<]+)</loc>", get(f"https://coffeetrail.co.il/job_listing-sitemap{n}.xml"))
    urls = sorted(set(urls))
    print(len(urls), "cart pages")
    res = []
    for u in urls:
        slug = urllib.parse.unquote(u.rstrip("/").split("/")[-1])
        f = cache / (urllib.parse.quote(slug, safe="").lower() + ".html") if cache else None
        alt = cache / (slug + ".html") if cache else None
        if f and f.exists(): t = f.read_text(errors="ignore")
        elif alt and alt.exists(): t = alt.read_text(errors="ignore")
        else: t = get(u); time.sleep(0.3)
        if t: res.append(parse(slug, t))
    OUT.write_text(json.dumps({"built": time.strftime("%Y-%m-%d"), "source": "coffeetrail.co.il", "carts": res}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", OUT, len(res), "carts,", sum(1 for r in res if r["instagram_handle"]), "with Instagram")

if __name__ == "__main__":
    main()
