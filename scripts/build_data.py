"""Builds data/places.json and data/places_mymaps.csv.
Edit the PLACES list below, then run:  python3 scripts/build_data.py
"""
import csv, json, pathlib
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKED = "2026-11-26"
DAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]

def hours(sun_thu=None, fri=None, sat="closed", status="unconfirmed", notes="", **override):
    h = {d: sun_thu for d in DAYS[:5]}
    h.update(fri=fri, sat=sat)
    h.update(override)
    return {"by_day": h, "status": status, "notes": notes}

def kosher(body, level, status="unconfirmed", note=""):
    return dict(kashrut_body=body, kashrut_level=level, kashrut_status=status, kashrut_note=note)

def gmaps(q):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(q)

def place(**p):
    base = dict(id=None, type=None, name_he=None, name_en=None, lat=None, lng=None,
                coords_confidence="approx", area=None,
                kashrut_body=None, kashrut_level=None, kashrut_status="unconfirmed", kashrut_note="",
                dairy_meat=None, hours=None, seasonal_notes="", instagram=None, website=None,
                phone=None, google_maps_url=None, source_urls=[], last_checked=CHECKED,
                my_notes="", visited=False)
    base.update(p)
    if not base["google_maps_url"]:
        base["google_maps_url"] = gmaps(f'{base["name_he"]} {base["area_he"]}' if base.get("area_he") else base["name_he"])
    base.pop("area_he", None)
    return base

def hike(**p):
    h = dict(length_km=None, duration_hrs=None, difficulty=None, loop=None, water_spring=None,
             shade=None, best_season=None, kid_friendly=None, trailhead_lat=None, trailhead_lng=None,
             amudanan_url=None, entrance_fee=False)
    h.update(p)
    h.setdefault("type", "hike")
    h["kashrut_body"] = h["kashrut_level"] = h["dairy_meat"] = "n/a"
    h["kashrut_status"] = "n/a"
    if h["trailhead_lat"] is None:
        h["trailhead_lat"], h["trailhead_lng"] = h["lat"], h["lng"]
    return place(**h)

PLACES = [
# ---------------- CARTS / CAFES / FOOD TRUCKS ----------------
place(id="mamo-machsiya", type="cart", name_he="מאמו מחסיה", name_en="MAM'O Coffee Cart (Machsiya)",
      area_he="מחסיה", lat=31.7270, lng=34.9790, area="Emek HaEla / Beit Shemesh",
      **kosher("Rabbanut Mateh Yehuda", "rabbanut_mehadrin",
               note="Own website says 'kosher lemehadrin'; CoffeeTrail lists Rabbanut Mateh Yehuda Mehadrin. Certificate not seen."),
      dairy_meat="dairy",
      hours=hours("08:00-20:00", "08:00-13:00",
                  notes="Own site's pages disagree on Friday close (13:00 / 14:00 / 15:00). Call 055-4558248 before going."),
      website="https://mamoplace.co.il/", phone="055-4558248",
      source_urls=["https://mamoplace.co.il/", "https://mamoplace.co.il/contact/",
                   "https://www.coffeecarts.co.il/%D7%9E%D7%90%D7%9E%D7%95-%D7%A2%D7%92%D7%9C%D7%AA-%D7%A7%D7%A4%D7%94-%D7%9E%D7%97%D7%A1%D7%99%D7%94/"],
      my_notes="Closest cart to RBS (~10 min)."),
place(id="mamo-tzur-hadassah", type="cart", name_he="מאמו צור הדסה (פארק יובל)", name_en="MAM'O Coffee Cart (Tzur Hadassah, Yuval Park)",
      area_he="צור הדסה", lat=31.7170, lng=35.0960, area="Jerusalem hills",
      **kosher("Rabbanut Mateh Yehuda (assumed same as Machsiya branch)", "rabbanut_mehadrin",
               note="Branch-specific certificate not confirmed."),
      dairy_meat="dairy",
      hours=hours("09:00-20:00", "09:00-16:00", notes="Older hours from own site."),
      seasonal_notes="Own site says this branch is CLOSED for the winter break.",
      website="https://mamoplace.co.il/",
      source_urls=["https://mamoplace.co.il/",
                   "https://www.coffeecarts.co.il/%D7%9E%D7%90%D7%9E%D7%95-%D7%A2%D7%92%D7%9C%D7%AA-%D7%A7%D7%A4%D7%94-%D7%A6%D7%95%D7%A8-%D7%94%D7%93%D7%A1%D7%94/"]),
place(id="mashav-foodtrucks", type="food_truck", name_he="משב פודטראקס", name_en="Mashav Food Trucks (Shoresh interchange)",
      area_he="שואבה", lat=31.8060, lng=35.0690, area="Jerusalem hills / Mateh Yehuda",
      **kosher("Rabbanut Mateh Yehuda", "rabbanut_regular",
               note="Rabbanut Mateh Yehuda per social posts; whether Mehadrin is not stated. Several trucks — check each."),
      dairy_meat="both (coffee/pizza dairy; burger truck meat)",
      hours=hours("08:00-22:00", "08:00-16:00",
                  sat="Motzei Shabbat: 1 hr after Shabbat until 00:00 (per 2024 post)",
                  notes="Coffee cart hours per most recent social post (Oct 2026). Pizza/burger/taco trucks open later in the day. Older listings say 08:00-16:00."),
      seasonal_notes="Some trucks are summer-only.",
      phone="054-608-3698", website="https://www.facebook.com/MashsavFoodTrucks",
      source_urls=["https://www.tiuli.com/restaurants/1334/%D7%9E%D7%A9%D7%91-%D7%A4%D7%95%D7%93-%D7%98%D7%A8%D7%90%D7%A7%D7%A1",
                   "https://www.tiktok.com/@travelee97/video/7383214147737111815",
                   "https://www.foodtrack.co.il/foodtrucks/%D7%9E%D7%A9%D7%91-%D7%A4%D7%95%D7%93-%D7%98%D7%A8%D7%90%D7%A7%D7%A1/"],
      my_notes="Waze: 'משב פודטראקס'. Don't confuse with Drive Cafe at the same interchange."),
place(id="meshek-segal", type="cart", name_he="משק סגל", name_en="Meshek Segal",
      area_he="טל שחר", lat=31.8080, lng=34.9040, area="Shfela / Nahal Sorek",
      **kosher("Rabbanut Mateh Yehuda", "rabbanut_mehadrin", note="Per CoffeeTrail listing; certificate not seen."),
      dairy_meat="dairy (unconfirmed)",
      hours=hours(None, None, sat=None, notes="No hours found. CoffeeTrail showed it as closed when indexed."),
      source_urls=["https://coffeetrail.co.il/mag/kosher-mehadrin/"],
      my_notes="Address: Nahal Sorek 82, Moshav Tal Shahar."),
place(id="cafe-la-maya", type="cart", name_he="קפה לה מאיה", name_en="Cafe La Maya",
      area_he="טל שחר", lat=31.8070, lng=34.9060, area="Shfela / Nahal Sorek",
      **kosher("Local rabbanut", "rabbanut_regular", note="Easy.co.il says 'כשר רבנות מקומית'."),
      dairy_meat="dairy (unconfirmed)",
      hours=hours("07:30-16:00", "08:00-15:00", sun="closed"),
      instagram="https://www.instagram.com/cafe_la_maya/",
      source_urls=["https://easy.co.il/page/10138992"],
      my_notes="By the Tal Sorek pool."),
place(id="babustan-kfar-uria", type="cart", name_he="בבוסתן", name_en="BaBustan (Kfar Uria)",
      area_he="כפר אוריה", lat=31.7850, lng=34.9790, area="Mateh Yehuda",
      **kosher("Rabbanut Mateh Yehuda", "rabbanut_mehadrin", note="Per CoffeeTrail; certificate not seen."),
      dairy_meat="dairy (pastries, taboon pizza)",
      hours=hours(None, None, sat=None, notes="No confirmed hours. Possibly same operator/site as 'Farm Cafe' (Fri-Sat 09:00-15:00 on an old listing — Shabbat-open would matter for kashrut; verify)."),
      phone="052-5490707",
      source_urls=["https://coffeetrail.co.il/region/ela/", "https://www.ynet.co.il/food/article/bkd7axwokl"],
      my_notes="Ma'ale Oria 4, among fruit trees on the Lombard farm."),
place(id="bar-nes", type="cart", name_he="בר נס", name_en="Bar Nes",
      area_he="נס הרים", lat=31.7540, lng=35.0560, area="Jerusalem hills",
      **kosher("unconfirmed", "unconfirmed", note="Listing says 'kosher' without naming the body."),
      dairy_meat="dairy (unconfirmed)",
      hours=hours(None, None, sat=None),
      source_urls=["https://traveleat.co.il/listing/bar_nes_agalatcafe/"],
      my_notes="Near Nahal Katlav — good pairing."),
place(id="cafe-yuda", type="cart", name_he="קפה יודה", name_en="Cafe Yuda (Bustan HaShmona)",
      area_he="בוסתן השמונה בית חורון", lat=31.8580, lng=35.1190, area="Binyamin / Route 443",
      **kosher("Local rabbanut", "rabbanut_regular", note="Per CoffeeTrail; certificate not seen."),
      dairy_meat="dairy (unconfirmed)",
      hours=hours("07:00-19:00", "07:00-15:00", notes="Other listing: Sun-Thu 07:00-20:00, Fri 07:00-14:00."),
      source_urls=["https://coffeetrail.co.il/coffeecart/cafe-yuda/",
                   "https://www.coffeecarts.co.il/%D7%A7%D7%A4%D7%94-%D7%99%D7%95%D7%93%D7%94-%D7%A2%D7%92%D7%9C%D7%AA-%D7%A7%D7%A4%D7%94-%D7%91%D7%99%D7%AA-%D7%97%D7%95%D7%A8%D7%95%D7%9F/"]),
place(id="cafe-rachel", type="cart", name_he="עגלת קפה רחל - חוות צהלה", name_en="Cafe Rachel (Zahala Farm)",
      area_he="מבוא חורון", lat=31.8470, lng=35.0310, area="Modiin area",
      **kosher("Rabbanut Mateh Binyamin (regional)", "rabbanut_regular", note="'כשר חלבי בהשגחת הרבנות האזורית מטה בנימין'."),
      dairy_meat="dairy",
      hours=hours("12:00-20:00", "08:00-15:00", notes="Farm's own page; another line says Fri 09:00 until 2 hrs before Shabbat. Call 055-662-6773."),
      website="https://zahalafarm.co.il/cafe-rachel/", phone="055-662-6773",
      source_urls=["https://zahalafarm.co.il/cafe-rachel/"],
      my_notes="Horse farm — kids like it."),
place(id="katerina-ben-shemen", type="cart", name_he="קטרינה", name_en="Katerina (Ben Shemen forest)",
      area_he="בן שמן", lat=31.9460, lng=34.9300, area="Modiin area",
      **kosher("Regional rabbanut", "unconfirmed", note="Sources disagree: 'Mehadrin regional rabbanut' vs 'regional rabbanut, Badatz products'."),
      dairy_meat="dairy (unconfirmed)",
      hours=hours(None, "08:00-13:00", sun="unconfirmed",
                  mon="09:00-13:00, 16:00-19:00", tue="09:00-13:00, 16:00-19:00",
                  wed="09:00-13:00", thu="09:00-13:00, 16:00-19:00",
                  notes="Per a TikTok post; date unknown."),
      source_urls=["https://coffeetrail.co.il/coffeecart/katerina/",
                   "https://familytrips.co.il/%D7%A2%D7%92%D7%9C%D7%AA-%D7%A7%D7%A4%D7%94-%D7%A7%D7%98%D7%A8%D7%99%D7%A0%D7%94-%D7%A2%D7%92%D7%9C%D7%94-%D7%9B%D7%A9%D7%A8%D7%94-%D7%91%D7%91%D7%9F-%D7%A9%D7%9E%D7%9F/"],
      my_notes="~40 min from RBS. Near the monkey sanctuary in Ben Shemen forest."),
place(id="juha-har-gilo", type="cafe", name_he="ג'וחה", name_en="Juha Coffee (Har Gilo)",
      area_he="הר גילה", lat=31.7300, lng=35.1440, area="Gush Etzion",
      **kosher("Rabbanut Gush Etzion", "rabbanut_mehadrin", note="Etzion Tourism: 'Kosher Mehadrin Gush Etzion'."),
      dairy_meat="dairy",
      hours=hours("15:00-21:00", "closed", notes="Reservations required."),
      phone="054-5830579", website="https://etziontour.org.il/en/item/juha-coffee/",
      source_urls=["https://etziontour.org.il/en/item/juha-coffee/"],
      my_notes="Evening only — sunset spot, not a Friday-morning option."),

# ---------------- HIKES ----------------
hike(id="sataf-springs", name_he="סטף - עין סטף ועין ביכורה", name_en="Sataf: Ein Sataf & Ein Bikura",
     area_he="סטף", lat=31.7725, lng=35.1300, area="Jerusalem hills",
     length_km=3, duration_hrs=1.5, difficulty="easy-moderate", loop=True, water_spring=True,
     shade="partial", best_season="all year (spring best)", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a", notes="KKL site, open area."),
     seasonal_notes="Bring a flashlight for the Ein Bikura tunnel.",
     source_urls=["https://hikingintheholyland.com/2019/12/15/sataf-choose-your-own-adventure-walk/",
                  "https://hikingintheholyland.com/2020/09/30/sataf-forest-the-complete-insiders-guide/"]),
hike(id="ein-lavan-ein-hanya", name_he="עין לבן ועין חניה", name_en="Ein Lavan & Ein Hanya",
     area_he="עמק רפאים", lat=31.7470, lng=35.1610, area="Jerusalem (Refaim valley)",
     length_km=2, duration_hrs=2.5, difficulty="easy", loop=False, water_spring=True,
     shade="little", best_season="all year; summer early morning", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a", notes="Ein Hanya is an organized INPA site; Ein Lavan lot is small (park at Biblical Zoo)."),
     seasonal_notes="Ein Hanya has stroller-friendly paths and facilities.",
     source_urls=["https://hikingintheholyland.com/2021/08/30/two-springs-in-the-city-ein-lavan-and-ein-hania/"]),
hike(id="tel-azeka", name_he="תל עזקה", name_en="Tel Azeka loop",
     area_he="פארק בריטניה תל עזקה", lat=31.7010, lng=34.9330, area="Emek HaEla / Beit Shemesh",
     length_km=2.5, duration_hrs=1.5, difficulty="easy", loop=True, water_spring=False,
     shade="little", best_season="winter-spring (flowers)", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Green trail markings are faded at the start.",
     source_urls=["https://hikingintheholyland.com/2020/03/04/taking-it-easy-at-tel-azeka/",
                  "https://www.alltrails.com/parks/israel/tel-azekah-national-park"],
     my_notes="Pairs with MAM'O Machsiya (~10 min)."),
hike(id="ein-kobi", name_he="עין כובי", name_en="Ein Kobi (Begin Park)",
     area_he="פארק בגין עין כובי", lat=31.7210, lng=35.0640, area="Jerusalem hills",
     length_km=3, duration_hrs=1.25, difficulty="easy", loop=None, water_spring=False,
     shade="partial", best_season="autumn-spring", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Spring is mostly dry nowadays. Harder continuation down to Nahal Kobi.",
     source_urls=["https://hikingintheholyland.com/2018/10/31/walk-to-ein-kobi/",
                  "https://enjoyingisrael.com/trails/47062/ein-kobi"]),
hike(id="ein-hemed", name_he="גן לאומי עין חמד", name_en="Ein Hemed National Park (Aqua Bella)",
     area_he="עין חמד", lat=31.7950, lng=35.1265, area="Jerusalem hills",
     length_km=1, duration_hrs=1.5, difficulty="easy", loop=True, water_spring=True,
     shade="good", best_season="all year; summer", kid_friendly=True, entrance_fee=True,
     hours=hours("08:00-17:00 (summer)", "08:00-16:00", sat="08:00-17:00 (summer)", status="unconfirmed",
                 notes="Last entry 1 hr before closing. Winter hours shorter. Book via INPA site."),
     phone="02-5342741",
     source_urls=["https://www.israel-in-photos.com/ein-hemed.html"],
     my_notes="Park more than a hike — picnic, shallow stream. Entry fee."),
hike(id="ein-mata-ein-tanur", name_he="עין מטע ועין תנור", name_en="Ein Mata & Ein Tanur (Nahal Zanoah)",
     area_he="עין מטע", lat=31.7150, lng=35.0400, area="Mateh Yehuda",
     length_km=2.5, duration_hrs=2.5, difficulty="easy", loop=True, water_spring=True,
     shade="good", best_season="all year", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     source_urls=["https://kkl-jnf.org/tourism-and-recreation/recommended_trips_and_tracks/ein_mata_and_ein_tanur/"],
     my_notes="Very close to RBS."),
hike(id="nahal-katlav", name_he="נחל קטלב", name_en="Nahal Katlav to Bar Giora station",
     area_he="נחל קטלב", lat=31.7380, lng=35.0700, area="Jerusalem hills",
     length_km=6.4, duration_hrs=3, difficulty="moderate", loop=False, water_spring=True,
     shade="partial", best_season="autumn-spring", kid_friendly=False,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="One-way: leave a second car at Bar Giora station, or take the train back.",
     source_urls=["https://hikingintheholyland.com/2019/08/11/true-nahal-katlav/",
                  "https://www.enjoyingisrael.com/trails/47063/nahal-katlav"]),
]

def main():
    (ROOT / "data").mkdir(exist_ok=True)
    out = {"generated": CHECKED, "home_base": {"name": "Ramat Bet Shemesh", "lat": 31.7110, "lng": 34.9870},
           "places": PLACES}
    (ROOT / "data/places.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Google My Maps CSV: needs lat/lng columns + a name column; UTF-8 with BOM so Hebrew shows correctly.
    cols = ["name_en", "name_he", "type", "lat", "lng", "area", "kashrut_body", "kashrut_level",
            "kashrut_status", "dairy_meat", "friday", "hours_summary", "length_km", "difficulty",
            "water_spring", "kid_friendly", "website", "google_maps_url", "last_checked", "description"]
    with open(ROOT / "data/places_mymaps.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for p in PLACES:
            bd = p["hours"]["by_day"]
            summary = "; ".join(f"{d}: {bd[d]}" for d in DAYS if bd.get(d))
            desc = " | ".join(x for x in [p["kashrut_note"], p["hours"]["notes"], p["seasonal_notes"], p["my_notes"]] if x)
            row = {c: p.get(c, "") for c in cols}
            row.update(friday=bd.get("fri") or "unconfirmed", hours_summary=summary or "unconfirmed",
                       description=desc)
            w.writerow(row)
    print(f"Wrote {len(PLACES)} places")

if __name__ == "__main__":
    main()
