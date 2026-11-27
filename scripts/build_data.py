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

def kosher(body, level, status="unconfirmed", note=""):  # status: owner_stated | official | third_party | unconfirmed
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

CT = "https://coffeetrail.co.il/coffeecart/"
OWNER = "owner_stated"      # stated by the business itself (own site or owner-verified CoffeeTrail listing)
OFFICIAL = "official"       # INPA / KKL / regional tourism authority page
THIRD = "third_party"       # guide site, article, social post — not the business itself

def ct_hours(sun, mon, tue, wed, thu, fri, sat="closed", notes="", status=OWNER):
    return {"by_day": dict(sun=sun, mon=mon, tue=tue, wed=wed, thu=thu, fri=fri, sat=sat), "status": status, "notes": notes}

PLACES = [
# ---------------- CARTS / CAFES / FOOD TRUCKS ----------------
place(id="mamo-machsiya", type="cart", name_he="מאמו מחסיה", name_en="MAM'O Coffee Cart (Machsiya)",
      lat=31.75019, lng=35.00331, coords_confidence="plus_code_from_own_site", area="Emek HaEla / Beit Shemesh",
      **kosher("Rabbanut Mateh Yehuda", "rabbanut_mehadrin", OWNER,
               "Own site: 'כשרה למהדרין רבנות מטה יהודה (כל המוצרים בית יוסף, חלב ישראל וירקות גוש קטיף)'."),
      dairy_meat="dairy",
      hours=hours("08:00-20:00", "08:00-13:00", status=OWNER, notes="Own site header + contact page (Nov 2026). Waze: 'MAMO food truck'."),
      website="https://mamoplace.co.il/", phone="055-4558248",
      source_urls=["https://mamoplace.co.il/", "https://mamoplace.co.il/contact/"],
      my_notes="Own site: 5 min drive from Beit Shemesh."),
place(id="mamo-tzur-hadassah", type="cart", name_he="מאמו צור הדסה (פארק יובל)", name_en="MAM'O Coffee Cart (Tzur Hadassah, Yuval Park)",
      lat=31.7152, lng=35.0989, coords_confidence="approx (town centre)", area="Jerusalem hills",
      **kosher("Rabbanut Mateh Yehuda", "rabbanut_mehadrin", OWNER, "Own site states the MAM'O hechsher for the brand; not branch-specific."),
      dairy_meat="dairy",
      hours=hours("closed", "closed", status=OWNER, notes="Branch is on winter break (own site, Nov 2026)."),
      seasonal_notes="Closed for winter.",
      website="https://mamoplace.co.il/", source_urls=["https://mamoplace.co.il/"]),
place(id="mashav-foodtrucks", type="food_truck", name_he="משב פוד טראקס", name_en="Mashav Food Trucks (Shoresh interchange)",
      lat=31.80149, lng=35.07702, coords_confidence="exact (CoffeeTrail pin)", area="Jerusalem hills / Mateh Yehuda",
      **kosher("Rabbanut Mateh Yehuda", "unconfirmed", THIRD,
               "Only social posts say 'בהשגחת רבנות מטה יהודה'; CoffeeTrail listing is not owner-verified and shows no kashrut. Level (Mehadrin or not) unknown."),
      dairy_meat="both (coffee/pizza dairy; burger truck meat)",
      hours=hours("08:00-22:00", "08:00-16:00", sat="Motzei Shabbat until 00:00 (2024 post)", status=THIRD,
                  notes="Per social posts; older listings say 08:00-16:00. Call 054-608-3698."),
      seasonal_notes="Some trucks are summer-only.", phone="054-608-3698",
      website="https://www.facebook.com/MashsavFoodTrucks",
      source_urls=[CT+"%D7%9E%D7%A9%D7%91-%D7%A4%D7%95%D7%93-%D7%98%D7%A8%D7%90%D7%A7%D7%A1/",
                   "https://www.tiktok.com/@travelee97/video/7383214147737111815"]),
place(id="meshek-segal", type="cart", name_he="משק סגל", name_en="Meshek Segal",
      lat=31.80309, lng=34.90550, coords_confidence="exact (CoffeeTrail pin)", area="Shfela / Nahal Sorek",
      **kosher("Rabbanut Mateh Yehuda", "rabbanut_mehadrin", OWNER, "Owner-verified CoffeeTrail listing."),
      dairy_meat="dairy (per menu)",
      hours=ct_hours(*["closed"]*6, notes="Owner notice: 'העגלה סגורה כרגע נעדכן בהמשך' — temporarily closed."),
      instagram="https://www.instagram.com/mesheksegal", phone="050-6544030",
      source_urls=[CT+"mesheksegal/"], my_notes="Nahal Sorek 82, Tal Shahar. Friday market day when open."),
place(id="cafe-la-maya", type="cart", name_he="קפה לה מאיה", name_en="Cafe La Maya",
      lat=31.80818, lng=34.91356, coords_confidence="exact (CoffeeTrail pin)", area="Shfela / Nahal Sorek",
      **kosher("Local rabbanut", "unconfirmed", THIRD, "Only Easy.co.il says 'כשר רבנות מקומית'; CoffeeTrail listing unverified, no kashrut shown."),
      dairy_meat="unconfirmed",
      hours=hours("07:30-16:00", "08:00-15:00", sun="closed", status=THIRD, notes="Easy.co.il listing."),
      instagram="https://www.instagram.com/cafe_la_maya/",
      source_urls=[CT+"cafe-la-maya/", "https://easy.co.il/page/10138992"]),
place(id="babustan-kfar-uria", type="cart", name_he="בבוסתן", name_en="BaBustan (Eretz Tova, Kfar Uria)",
      lat=31.79301, lng=34.94825, coords_confidence="exact (CoffeeTrail pin)", area="Mateh Yehuda",
      **kosher("Rabbanut Mateh Yehuda", "rabbanut_mehadrin", OWNER, "Owner-verified CoffeeTrail listing."),
      dairy_meat="dairy (per menu)",
      hours=ct_hours(*["closed"]*5, "08:00-13:00", notes="Currently Friday only."),
      instagram="https://www.instagram.com/eretz_tova/", phone="052-5490707",
      source_urls=[CT+"ba-bus-tan/"],
      my_notes="Warning: 'Farm Cafe' in the same Eretz Tova compound is a SEPARATE business, open on Shabbat only, with no hechsher listed."),
place(id="bar-nes", type="cart", name_he="בר נס", name_en="Bar Nes (Nahal Katlav parking)",
      lat=31.73455, lng=35.07147, coords_confidence="exact (CoffeeTrail pin)", area="Jerusalem hills",
      **kosher("not stated", "unconfirmed", "unconfirmed", "Owner-verified listing shows no kashrut; a guide site just says 'kosher'."),
      dairy_meat="unconfirmed",
      hours=ct_hours(*["closed"]*6, notes="Owner notice: closed on weekdays due to long reserve duty."),
      instagram="https://www.instagram.com/bar.nes_agalatcafe", phone="058-7782691",
      source_urls=[CT+"bar-ness/"], my_notes="At the Nahal Katlav trailhead."),
place(id="cafe-yuda", type="cart", name_he="קפה יודה", name_en="Cafe Yuda (Bustan HaShmona)",
      lat=31.87329, lng=35.13250, coords_confidence="exact (CoffeeTrail pin)", area="Binyamin / Route 443",
      **kosher("Local rabbanut", "rabbanut_regular", OWNER, "Owner-verified CoffeeTrail listing."),
      dairy_meat="dairy cart; Thursday nights 19:00-01:00 a separate meat area (cholent, schnitzel)",
      hours=ct_hours(*["07:00-19:00"]*5, "07:00-15:00", notes="Owner text says Friday until 14:00; the hours table says 15:00."),
      instagram="https://www.instagram.com/cafe_yuda", phone="054-5224424",
      source_urls=[CT+"cafe-yuda/"]),
place(id="cafe-rachel", type="cart", name_he="קפה רחל - חוות צהלה", name_en="Cafe Rachel (Zahala Farm)",
      lat=31.8470, lng=35.0310, coords_confidence="approx", area="Modiin area",
      **kosher("Rabbanut & regional religious council Mateh Binyamin", "rabbanut_regular", OWNER,
               "Own site: 'כשר חלבי, בהשגחת הרבנות והמועצה הדתית האזורית מטה בנימין'."),
      dairy_meat="dairy",
      hours=hours("12:00-20:00", "08:00-15:00", status=OWNER, notes="Own site. Call 055-662-6773 in winter."),
      website="https://zahalafarm.co.il/cafe-rachel/", phone="055-662-6773",
      source_urls=["https://zahalafarm.co.il/cafe-rachel/"], my_notes="Horse farm, 7 min from Modiin."),
place(id="katerina", type="cart", name_he="קטרינה", name_en="Katerina (Monkey Park, Kfar Daniel)",
      lat=31.94397, lng=34.93307, coords_confidence="exact (CoffeeTrail pin)", area="Modiin area",
      **kosher("Regional rabbanut", "rabbanut_mehadrin", OWNER, "Owner-verified listing: 'תעודת כשרות מהדרין של הרבנות האזורית'."),
      dairy_meat="dairy (per menu)",
      hours=ct_hours(*["08:00-14:00"]*5, "08:00-13:00"),
      instagram="https://www.instagram.com/katerina_coffee_trail/", phone="050-7087575",
      source_urls=[CT+"katerina/"]),
place(id="juha-har-gilo", type="cafe", name_he="ג'וחה", name_en="Juha Coffee (Har Gilo)",
      lat=31.72177, lng=35.17153, coords_confidence="approx (Har Gilo village; cafe is by the field school)", area="Gush Etzion",
      **kosher("Rabbanut Gush Etzion", "rabbanut_mehadrin", OFFICIAL, "Etzion regional tourism page: 'Kosher Mehadrin Gush Etzion'."),
      dairy_meat="dairy",
      hours=hours("15:00-21:00", "closed", status=OFFICIAL, notes="Reservations required."),
      phone="054-5830579", website="https://etziontour.org.il/en/item/juha-coffee/",
      source_urls=["https://etziontour.org.il/en/item/juha-coffee/"],
      my_notes="Evenings only, opposite the Har Gilo field school."),
place(id="ella-valley-coffee", type="cart", name_he="אלה קפה בעמק", name_en="Ella Valley Coffee (Givat Yeshayahu)",
      lat=31.66989, lng=34.95101, coords_confidence="exact (CoffeeTrail pin)", area="Emek HaEla",
      **kosher("Local rabbanut", "rabbanut_regular", OWNER, "Owner-verified CoffeeTrail listing."),
      dairy_meat="dairy (per menu)",
      hours=ct_hours(*["08:00-16:00"]*5, "08:00-14:00"),
      instagram="https://www.instagram.com/ellavalleycoffee/", phone="055-5685625",
      source_urls=[CT+"ella-coffee-valley/"], my_notes="Full gluten-free menu, kept separate. Near Beit Guvrin."),
place(id="cafe-nachshon", type="cart", name_he="קפה נחשון", name_en="Cafe Nachshon (by Sorek winery)",
      lat=31.83291, lng=34.95414, coords_confidence="exact (CoffeeTrail pin)", area="Shfela / Latrun",
      **kosher("Local rabbanut", "rabbanut_regular", OWNER, "Owner-verified CoffeeTrail listing."),
      dairy_meat="dairy (per menu)",
      hours=ct_hours("closed", "closed", "closed", "09:00-14:30", "09:00-14:30", "08:30-14:00",
                     notes="If the kibbutz gate is shut, call and they open it. On rainy days call first."),
      instagram="https://www.instagram.com/cafe_nachshon_latrun", phone="052-6703759",
      source_urls=[CT+"nachshon-coffee/"]),
place(id="galita-tzuba", type="cart", name_he="גליתא - צובה", name_en="Galita (Kibbutz Tzuba)",
      lat=31.78472, lng=35.11507, coords_confidence="exact (CoffeeTrail pin)", area="Jerusalem hills",
      **kosher("Chatam Sofer Petach Tikva", "other", OWNER, "Owner-verified listing: 'תעודת כשרות חתם סופר פתח תקווה' (private hashgacha)."),
      dairy_meat="unconfirmed",
      hours=ct_hours(*["09:00-17:00"]*5, "08:00-15:30"),
      phone="02-5347650", source_urls=[CT+"galita-coffee-cart/"],
      my_notes="Next to Ein Hemed and Sataf."),
place(id="machtipatly-ora", type="cart", name_he="מחתפתלי 212", name_en="Machtipatly 212 (Ora nursery)",
      lat=31.75508, lng=35.15801, coords_confidence="exact (CoffeeTrail pin)", area="Jerusalem hills",
      **kosher("not stated", "unconfirmed", OWNER, "Owner-verified listing says 'תעודת כשרות למהדרין' but doesn't name the certifying body."),
      dairy_meat="unconfirmed",
      hours=ct_hours(*["08:00-18:00"]*5, "08:00-14:00"),
      instagram="https://www.instagram.com/machtipatly.coffee", phone="054-2494992",
      source_urls=[CT+"mchtipatly212/"], my_notes="About 500 m from Ein Lavan — natural pairing."),
place(id="siftach-efrat", type="cart", name_he="סיפתח אפרת", name_en="Siftach (Efrat, Aqueduct Park)",
      lat=31.68212, lng=35.16954, coords_confidence="exact (CoffeeTrail pin)", area="Gush Etzion",
      **kosher("Local rabbanut (Efrat)", "rabbanut_regular", OWNER, "Owner-verified CoffeeTrail listing."),
      dairy_meat="dairy (per menu)",
      hours=ct_hours(*["07:00-19:00"]*4, "07:00-24:00", "07:00-14:00", sat="Motzei Shabbat 19:00-24:00"),
      instagram="https://www.instagram.com/siftachcoffee", phone="054-9621254",
      source_urls=[CT+"siftach-efrat/"]),
place(id="pastatria-har-herzl", type="food_truck", name_he="הפודטראק של פסטטריה - הר הרצל", name_en="Pastatria Food Truck (Har Herzl)",
      lat=31.77163, lng=35.18098, coords_confidence="exact (CoffeeTrail pin)", area="Jerusalem",
      **kosher("Local rabbanut (Jerusalem)", "rabbanut_mehadrin", OWNER, "Owner-verified listing: 'כשרות מהדרין של הרבנות המקומית'."),
      dairy_meat="unconfirmed",
      hours=ct_hours("07:00-22:00", *["08:00-22:00"]*4, "closed"),
      instagram="https://www.instagram.com/pasta_tria", phone="054-3747186",
      source_urls=[CT+"pastatria-har-herzel/"], my_notes="At the Red Sculpture plaza. Closed Fridays."),
place(id="tanto-shilat", type="cart", name_he="טנטו", name_en="Tanto (Shilat)",
      lat=31.91861, lng=35.01821, coords_confidence="exact (CoffeeTrail pin)", area="Modiin area",
      **kosher("Rabbanut Modiin", "rabbanut_regular", OWNER, "Owner-verified CoffeeTrail listing."),
      dairy_meat="unconfirmed",
      hours=ct_hours(*["08:00-19:00"]*5, "08:00-14:00"),
      instagram="https://www.instagram.com/tanto_shilat", phone="052-5600400",
      source_urls=[CT+"tanto/"]),
place(id="mona-cafe", type="cart", name_he="מונה קפה", name_en="Mona Cafe (Beit Hashmonai)",
      lat=31.89019, lng=34.91987, coords_confidence="exact (CoffeeTrail pin)", area="Modiin area",
      **kosher("Regional rabbanut", "rabbanut_regular", OWNER, "Owner-verified CoffeeTrail listing."),
      dairy_meat="unconfirmed",
      hours=ct_hours("closed", *["08:00-13:30"]*4, "08:00-14:00"),
      instagram="https://www.instagram.com/monacoffeetruck", phone="054-5819921",
      source_urls=[CT+"mona-cafe/"]),
place(id="cafe-nelly", type="cart", name_he="נלי", name_en="Cafe Nelly (Mishmar Ayalon)",
      lat=31.87088, lng=34.94838, coords_confidence="exact (CoffeeTrail pin)", area="Modiin area",
      **kosher("Regional rabbanut", "rabbanut_regular", OWNER, "Owner-verified CoffeeTrail listing."),
      dairy_meat="unconfirmed",
      hours=ct_hours("closed", "closed", "closed", "closed", "08:00-14:00", "08:00-14:00"),
      instagram="https://www.instagram.com/cafe_nelly_/", phone="054-5819921",
      source_urls=[CT+"nelly/"], my_notes="Thursday and Friday only."),

# ---------------- HIKES ----------------
hike(id="ein-mata-ein-tanur", name_he="עין מטע ועין תנור", name_en="Ein Mata & Ein Tanur (Nahal Zanoah)",
     lat=31.71476, lng=35.05177, trailhead_lat=31.71169, trailhead_lng=35.04697,
     coords_confidence="exact (OpenStreetMap)", area="Mateh Yehuda",
     length_km=2.5, duration_hrs=2, difficulty="moderate", loop=True, water_spring=True,
     shade="good (fig & eucalyptus)", best_season="all year", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a", notes="Open area."),
     seasonal_notes="Bring flashlights for the ancient tunnel. Part of the Israel National Trail.",
     source_urls=["https://kkl-jnf.org/tourism-and-recreation/recommended_trips_and_tracks/ein_mata_and_ein_tanur/"],
     my_notes="Trailhead: KKL picnic area at Hurvat Hanut, Route 375 near km 11. Blue dirt road, then black trail."),
hike(id="tel-azeka", name_he="תל עזקה", name_en="Tel Azeka loop",
     lat=31.69917, lng=34.93591, trailhead_lat=31.69917, trailhead_lng=34.93591,
     coords_confidence="exact (OpenStreetMap: the tel itself)", area="Emek HaEla",
     length_km=2.5, duration_hrs=1.5, difficulty="easy", loop=True, water_spring=False,
     shade="little", best_season="winter-spring (flowers)", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Green trail markings are faded at the start.",
     source_urls=["https://hikingintheholyland.com/2020/03/04/taking-it-easy-at-tel-azeka/"],
     my_notes="Drive in through British Park off Route 383. Pairs with Ella Valley Coffee and MAM'O."),
hike(id="ein-kobi", name_he="עין קובי", name_en="Ein Kobi (Begin Park)",
     lat=31.72571, lng=35.11756, coords_confidence="exact (OpenStreetMap: the spring)", area="Jerusalem hills",
     length_km=3, duration_hrs=1.25, difficulty="easy", loop=None, water_spring=False,
     shade="partial", best_season="autumn-spring", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="The spring is mostly dry nowadays. A harder trail continues down to Nahal Kobi.",
     source_urls=["https://hikingintheholyland.com/2018/10/31/walk-to-ein-kobi/"]),
hike(id="nahal-katlav", name_he="נחל קטלב", name_en="Nahal Katlav to Bar Giora station",
     lat=31.74095, lng=35.07463, trailhead_lat=31.73455, trailhead_lng=35.07147,
     coords_confidence="exact (trailhead = Nahal Katlav parking, CoffeeTrail pin)", area="Jerusalem hills",
     length_km=6.4, duration_hrs=3, difficulty="moderate", loop=False, water_spring=True,
     shade="partial", best_season="autumn-spring", kid_friendly=False,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Loop with a hard climb back up, or one-way with a second car by Nahal Sorek at the old Bar Giora station.",
     source_urls=["https://hikingintheholyland.com/2019/08/11/true-nahal-katlav/",
                  "https://www.enjoyingisrael.com/trails/47063/nahal-katlav"],
    ),
hike(id="sataf-springs", name_he="סטף - עין סטף ועין ביכורה", name_en="Sataf: Ein Sataf & Ein Bikura",
     lat=31.77100, lng=35.12739, trailhead_lat=31.77552, trailhead_lng=35.12693,
     coords_confidence="exact (OpenStreetMap; trailhead = upper parking)", area="Jerusalem hills",
     length_km=3, duration_hrs=1.5, difficulty="easy-moderate", loop=True, water_spring=True,
     shade="partial", best_season="all year (spring best)", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Bring a flashlight for the Ein Bikura tunnel.",
     source_urls=["https://hikingintheholyland.com/2019/12/15/sataf-choose-your-own-adventure-walk/"]),
hike(id="ein-hemed", name_he="גן לאומי עין חמד", name_en="Ein Hemed National Park (Aqua Bella)",
     lat=31.79736, lng=35.12602, coords_confidence="exact (OpenStreetMap: park area)", area="Jerusalem hills",
     length_km=1, duration_hrs=1.5, difficulty="easy", loop=True, water_spring=True,
     shade="good", best_season="all year", kid_friendly=True, entrance_fee=True,
     hours=hours("08:00-16:00", "08:00-15:00", sat="08:00-16:00", status=OFFICIAL,
                 notes="WINTER hours. Summer: 08:00-17:00, Fri 08:00-16:00. Last entry 1 hr before closing. Pre-booking recommended. Adult 24 NIS, child 10 NIS."),
     phone="02-5342741", website="https://www.parks.org.il/reserve-park/%D7%92%D7%9F-%D7%9C%D7%90%D7%95%D7%9E%D7%99-%D7%A2%D7%99%D7%9F-%D7%97%D7%9E%D7%93/",
     source_urls=["https://www.parks.org.il/reserve-park/%D7%92%D7%9F-%D7%9C%D7%90%D7%95%D7%9E%D7%99-%D7%A2%D7%99%D7%9F-%D7%97%D7%9E%D7%93/"],
     my_notes="Mostly a park — picnics and wading in the stream. Waze: 'גן לאומי עין חמד'."),
hike(id="ein-lavan-ein-hanya", name_he="עין לבן ועין חניה", name_en="Ein Lavan & Ein Hanya",
     lat=31.74906, lng=35.15926, trailhead_lat=31.74906, trailhead_lng=35.15926,
     coords_confidence="exact (OpenStreetMap: Ein Lavan spring)", area="Jerusalem (Refaim valley)",
     length_km=2, duration_hrs=2.5, difficulty="easy", loop=False, water_spring=True,
     shade="little", best_season="all year; early morning in summer", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a", notes="Ein Hanya (31.74354, 35.15632) is an organized INPA site; check its hours."),
     seasonal_notes="Ein Lavan's parking lot is small; park at the Biblical Zoo.",
     source_urls=["https://hikingintheholyland.com/2021/08/30/two-springs-in-the-city-ein-lavan-and-ein-hania/"],
     my_notes="Pairs with Machtipatly 212 in Ora."),
]

ET = "https://etziontour.org.il/item/"
INPA = "https://www.parks.org.il/reserve-park/"

PLACES += [
# ---------------- GUSH ETZION FOOD (Etzion regional tourism = OFFICIAL source) ----------------
place(id="napolitanit-kfar-etzion", type="cart", name_he="נפוליטנית בקיבוץ", name_en="Napolitanit BaKibbutz (Kfar Etzion)",
      lat=31.64849, lng=35.11444, coords_confidence="exact (OSM: Kfar Etzion field school, where it parks)", area="Gush Etzion",
      **kosher("Rabbanut & religious council Gush Etzion", "rabbanut_regular", OFFICIAL,
               "Etzion Tourism: 'כשרות רבנות ומועצה דתית גוש עציון'. Doesn't say whether it's Mehadrin."),
      dairy_meat="dairy (pizza, per menu)",
      hours=hours("10:00-20:00", "08:30-15:00", thu="10:00-23:00", status=OFFICIAL),
      phone="053-3419705", source_urls=[ET+"%D7%A0%D7%A4%D7%95%D7%9C%D7%99%D7%98%D7%A0%D7%99%D7%AA-%D7%91%D7%A7%D7%99%D7%91%D7%95%D7%A5/"],
      my_notes="Field school parking lot. Waze: 'נפוליטנית בקיבוץ עגלת קפה'. Taboon pizza."),
place(id="baba-yaga-sde-boaz", type="food_truck", name_he="באבא יאגה סמוק האוס", name_en="Baba Yaga Smokehouse (Sde Boaz)",
      lat=31.69371, lng=35.14788, coords_confidence="approx (Sde Boaz hamlet)", area="Gush Etzion",
      **kosher("Rabbanut Gush Etzion", "rabbanut_regular", OFFICIAL, "Etzion Tourism: 'רבנות גוש עציון, בשר חלק בית יוסף'."),
      dairy_meat="meat",
      hours=hours(None, "closed", sun="closed", mon="closed", tue="closed", wed="15:00-late", thu="15:00-late",
                  sat="Motzei Shabbat from 21:00", status=OFFICIAL, notes="Kitchen closes 23:00. Call Aharon to open the gate: 054-7180099."),
      instagram="https://www.instagram.com/baba_yaga_smokehouse", phone="054-7180099",
      source_urls=[ET+"baba_yaga/"], my_notes="Evening meat option, not for Friday morning."),
place(id="himalaya-sde-boaz", type="cafe", name_he="הימלאיה - צ'אי בר", name_en="Himalaya Chai Bar (Sde Boaz)",
      lat=31.68801, lng=35.14622, coords_confidence="exact (pin on official page)", area="Gush Etzion",
      **kosher("not stated", "unconfirmed", "unconfirmed", "Etzion Tourism page lists no kashrut."),
      dairy_meat="vegetarian (Indian)",
      hours=hours(None, "10:00-15:00", sun="closed", mon="closed", tue="closed", wed="12:00-20:00", thu="12:00-20:00",
                  status=OFFICIAL, notes="Winter hours."),
      instagram="https://www.instagram.com/himalaya_chai.bar", phone="050-7626019",
      source_urls=[ET+"%D7%94%D7%99%D7%9E%D7%9C%D7%90%D7%99%D7%94-%D7%A6%D7%90%D7%99-%D7%91%D7%A8-%D7%9E%D7%A1%D7%A2%D7%93%D7%94/"]),
place(id="geona-oz-vegaon", type="cart", name_he="גאונה - קפה באהבה", name_en="Geona Cafe (Oz VeGaon reserve)",
      lat=31.64273, lng=35.13490, coords_confidence="exact (CoffeeTrail pin)", area="Gush Etzion",
      **kosher("not stated", "unconfirmed", "unconfirmed", "Neither Etzion Tourism nor CoffeeTrail shows a hechsher."),
      dairy_meat="dairy (pastries, pizza, per description)",
      hours=hours("09:00-15:00", "08:30-13:00", status=OFFICIAL, notes="Winter hours per Etzion Tourism."),
      instagram="https://www.instagram.com/geona_cafe",
      source_urls=[ET+"%D7%92%D7%90%D7%95%D7%A0%D7%94-%D7%A7%D7%A4%D7%94-%D7%91%D7%90%D7%94%D7%91%D7%94/", CT+"25009/"],
      my_notes="Inside the Oz VeGaon reserve: playground, wading pool."),
place(id="yani-rosh-tzurim", type="cart", name_he="יאני עגלת קפה", name_en="Yani Coffee Cart (Rosh Tzurim)",
      lat=31.66765, lng=35.12535, coords_confidence="approx (village)", area="Gush Etzion",
      **kosher("not stated", "unconfirmed", "unconfirmed", "Etzion Tourism page has a kashrut tab but no text."),
      dairy_meat="unconfirmed",
      hours=hours(None, "08:00-13:00 (winter) / 08:00-14:00 (summer)", sun="closed", mon="08:00-15:00", tue="08:00-15:00",
                  wed="08:00-15:00", thu="08:00-15:00", status=OFFICIAL),
      phone="052-4492097",
      source_urls=[ET+"%D7%99%D7%90%D7%A0%D7%99-%D7%A2%D7%92%D7%9C%D7%AA-%D7%A7%D7%A4%D7%94/"],
      my_notes="Next to the Ein Tzurim pools."),
place(id="lachmasha-tekoa", type="cafe", name_he="לחמשה תקוע", name_en="Lachmasha Bakery Cafe (Tekoa)",
      lat=31.65262, lng=35.22811, coords_confidence="exact (Waze link on official page)", area="Gush Etzion (east)",
      **kosher("Rabbanut Gush Etzion", "rabbanut_mehadrin", OFFICIAL, "Etzion Tourism: 'מהדרין גוש עציון'."),
      dairy_meat="dairy (per menu)",
      hours=hours("07:00-22:00", "07:00-14:00", status=OFFICIAL),
      phone="054-8883554", source_urls=[ET+"%D7%9C%D7%97%D7%9E%D7%A9%D7%94/"],
      my_notes="Sourdough bakery and village cafe looking out over the desert."),

# ---------------- MORE HIKES ----------------
hike(id="soreq-cave", name_he="שמורת טבע מערת הנטיפים", name_en="Soreq (Avshalom) Stalactite Cave",
     lat=31.75587, lng=35.02218, coords_confidence="exact (OpenStreetMap)", area="Beit Shemesh / Mateh Yehuda",
     length_km=0.5, duration_hrs=1, difficulty="easy (steps down to the cave)", loop=True, water_spring=False,
     shade="indoor cave", best_season="all year (good for hot or rainy days)", kid_friendly=True, entrance_fee=True,
     hours=hours("08:00-16:00", "08:00-15:00", sat="08:00-16:00", status=OFFICIAL,
                 notes="WINTER: last entry 15:00 (Fri 14:00). Summer: site open until 17:00 (Fri 16:00). Adult 31 NIS, child 16 NIS. Booking recommended."),
     website=INPA+"%D7%A9%D7%9E%D7%95%D7%A8%D7%AA-%D7%98%D7%91%D7%A2-%D7%9E%D7%A2%D7%A8%D7%AA-%D7%94%D7%A0%D7%98%D7%99%D7%A4%D7%99%D7%9D/",
     source_urls=[INPA+"%D7%A9%D7%9E%D7%95%D7%A8%D7%AA-%D7%98%D7%91%D7%A2-%D7%9E%D7%A2%D7%A8%D7%AA-%D7%94%D7%A0%D7%98%D7%99%D7%A4%D7%99%D7%9D/"],
     my_notes="Cave visit, not a hike. ~10 min from RBS."),
hike(id="beit-guvrin", name_he="גן לאומי בית גוברין", name_en="Beit Guvrin–Maresha National Park (caves)",
     lat=31.59533, lng=34.90248, coords_confidence="exact (OpenStreetMap: park area)", area="Shfela / Lachish",
     length_km=3, duration_hrs=3, difficulty="easy", loop=True, water_spring=False,
     shade="caves give shade; little outside", best_season="autumn-spring", kid_friendly=True, entrance_fee=True,
     hours=hours("08:00-16:00", "08:00-15:00", sat="08:00-16:00", status=OFFICIAL,
                 notes="WINTER hours (summer until 17:00, Fri 16:00). Last entry 1 hr before closing. Adult 31 NIS, child 16 NIS. Phone 08-6811020."),
     website=INPA+"%D7%92%D7%9F-%D7%9C%D7%90%D7%95%D7%9E%D7%99-%D7%91%D7%99%D7%AA-%D7%92%D7%95%D7%91%D7%A8%D7%99%D7%9F/",
     source_urls=[INPA+"%D7%92%D7%9F-%D7%9C%D7%90%D7%95%D7%9E%D7%99-%D7%91%D7%99%D7%AA-%D7%92%D7%95%D7%91%D7%A8%D7%99%D7%9F/"],
     my_notes="Pairs with Ella Valley Coffee (~10 min)."),
hike(id="tzora-sculpture-trail", name_he="דרך הפסלים ביער צרעה", name_en="Tzora Forest Sculpture Trail",
     lat=31.78019, lng=34.97621, coords_confidence="approx (OSM: Tzora Forest recreation ground)", area="Beit Shemesh / Mateh Yehuda",
     length_km=6, duration_hrs=4, difficulty="easy", loop=False, water_spring=False,
     shade="partial (forest)", best_season="all year", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Mostly a drive with short walks between sculptures and viewpoints. Partly wheelchair-accessible. The Samson Ridge trail (~1.5 km) branches off.",
     source_urls=["https://kkl-jnf.org/tourism-and-recreation/recommended_trips_and_tracks/tzora/"],
     my_notes="KKL: 'Basic', 6 km, 3-5 hrs. Pairs with BaBustan (Fridays)."),
hike(id="ein-tzurim-pools", name_he="בריכות עין צורים", name_en="Ein Tzurim Pools (Rosh Tzurim)",
     lat=31.66944, lng=35.12215, coords_confidence="exact (Waze link on official page)", area="Gush Etzion",
     length_km=0.2, duration_hrs=1, difficulty="easy", loop=False, water_spring=True,
     shade="good", best_season="spring-autumn", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Two wading pools, 40 and 60 cm deep. Swing and benches. 2 min walk from the parking.",
     source_urls=[ET+"%D7%91%D7%A8%D7%99%D7%9B%D7%95%D7%AA-%D7%A2%D7%99%D7%9F-%D7%A6%D7%95%D7%A8%D7%99%D7%9D/"],
     my_notes="Turn left before the Rosh Tzurim gate, down to the chicken coops, then follow the signs."),
hike(id="oz-vegaon", name_he="שמורת עוז וגאו\"ן", name_en="Oz VeGaon Reserve",
     lat=31.64232, lng=35.13511, coords_confidence="exact (Waze link on official page)", area="Gush Etzion",
     length_km=1.5, duration_hrs=1.5, difficulty="easy", loop=True, water_spring=False,
     shade="good (forest)", best_season="all year", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Picnic tables, playground, wading pool, toilets. Educational trail up to the Ari Fuld lookout.",
     source_urls=[ET+"%D7%A9%D7%9E%D7%95%D7%A8%D7%AA-%D7%A2%D7%95%D7%96-%D7%95%D7%92%D7%90%D7%95%D7%9F/"],
     my_notes="Geona cafe is on site."),
hike(id="nahal-hapirim", name_he="נחל הפירים - אמות המים", name_en="Nahal HaPirim aqueducts (Efrat)",
     lat=31.68212, lng=35.16954, trailhead_lat=31.68212, trailhead_lng=35.16954,
     coords_confidence="approx (Givat HaDagan, Efrat)", area="Gush Etzion",
     length_km=3.5, duration_hrs=2.5, difficulty="moderate", loop=False, water_spring=True,
     shade="partial", best_season="all year", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Black trail along Second Temple aqueducts; you can walk inside a stretch of the Biar aqueduct (bring a flashlight, expect water). Views of Solomon's Pools.",
     source_urls=[ET+"%D7%A0%D7%97%D7%9C-%D7%94%D7%A4%D7%99%D7%A8%D7%99%D7%9D/"],
     my_notes="Givat HaDagan to Ein Biar, one-way. Starts right by Siftach (HaDagan 1)."),
hike(id="ein-livne", name_he="עין ליבנה", name_en="Ein Livne (Bat Ayin)",
     lat=31.66340, lng=35.09681, coords_confidence="exact (OpenStreetMap: the spring)", area="Gush Etzion",
     length_km=1, duration_hrs=1, difficulty="easy-moderate", loop=False, water_spring=True,
     shade="good (trees)", best_season="spring-autumn", kid_friendly=None,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Pool about 2.5 m deep — not for non-swimmers.",
     source_urls=[ET+"%D7%A2%D7%99%D7%9F-%D7%9C%D7%99%D7%91%D7%A0%D7%94/"],
     my_notes="Through the Bat Ayin entrance, right at the roundabout, right again (hairpin). Park by the turn into the wadi; follow the green trail."),
hike(id="ein-sagma", name_he="עין סג'מה - עין יצחק", name_en="Ein Sagma / Ein Yitzhak",
     lat=31.65961, lng=35.11295, coords_confidence="exact (OpenStreetMap: the spring)", area="Gush Etzion",
     length_km=1, duration_hrs=1, difficulty="easy", loop=False, water_spring=True,
     shade="good (shaded picnic tables)", best_season="spring-autumn", kid_friendly=True,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Pool about 1.5 m deep.",
     source_urls=[ET+"%D7%A2%D7%99%D7%9F-%D7%A1%D7%92%D7%9E%D7%94-%D7%A2%D7%99%D7%9F-%D7%99%D7%A6%D7%97%D7%A7/"],
     my_notes="Toward Bat Ayin, right before the chicken coops, follow the blue trail. Distance is an estimate."),
hike(id="ein-hovila", name_he="עין חובלה", name_en="Ein Hovila (Bat Ayin)",
     lat=31.65900, lng=35.10772, coords_confidence="exact (OpenStreetMap: the spring)", area="Gush Etzion",
     length_km=0.5, duration_hrs=1, difficulty="easy", loop=False, water_spring=True,
     shade="partial", best_season="spring-autumn", kid_friendly=None,
     hours=hours(None, None, sat=None, status="n/a"),
     seasonal_notes="Spring tunnel cut in rock that fills a square pool about 2 m deep. Ancient terraces and a Second Temple burial cave.",
     source_urls=[ET+"%D7%A2%D7%99%D7%9F-%D7%97%D7%95%D7%91%D7%9C%D7%94/"],
     my_notes="In Bat Ayin take the first right; the road turns to dirt and you drive almost to the spring."),
]

# Who supplied each original hike's trail details.
_OFFICIAL = {"ein-mata-ein-tanur": "KKL", "tzora-sculpture-trail": "KKL", "soreq-cave": "INPA (length/time estimated)",
             "ein-hemed": "INPA (length/time estimated)", "nahal-hapirim": "Etzion Tourism", "ein-tzurim-pools": "Etzion Tourism (length estimated)",
             "ein-sagma": "Etzion Tourism (length estimated)", "ein-hovila": "Etzion Tourism (length estimated)",
             "ein-livne": "Etzion Tourism", "oz-vegaon": "Etzion Tourism", "beit-guvrin": "INPA"}
for _p in PLACES:
    if _p["type"] == "hike":
        _p.setdefault("details_status", "official" if _p["id"] in _OFFICIAL else "unconfirmed")
        _p.setdefault("details_source", _OFFICIAL.get(_p["id"], "search snippets only"))

import sys as _sys; _sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import hith_import as _hith
_hith.apply(PLACES, place, hike, hours)

# Places added later from Instagram links (scripts/add_place.py writes these; reviewed by hand).
for _e in json.loads((ROOT / "data/sources/added_places.json").read_text(encoding="utf-8")):
    assert _e["id"] not in {p["id"] for p in PLACES}, f"duplicate id {_e['id']}"
    PLACES.append(hike(**_e) if _e.get("type") == "hike" else place(**_e))

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
            desc = " | ".join(x for x in [p["kashrut_note"], p["hours"]["notes"], p["seasonal_notes"], p.get("warnings") or "", p["my_notes"], p.get("details_source", "")] if x and x != "n/a")
            row = {c: p.get(c, "") for c in cols}
            row.update(friday=bd.get("fri") or "unconfirmed", hours_summary=summary or "unconfirmed",
                       description=desc)
            w.writerow(row)
    print(f"Wrote {len(PLACES)} places")

if __name__ == "__main__":
    main()
