"""Which Hiking the Holyland posts go on the map, and where.

Each entry: post slug -> dict(id, name_he, lat, lng, conf, area, also=[other slugs merged into notes], note)
Coordinates are OpenStreetMap features (or CoffeeTrail/official pins) NEAR the trailhead the
post describes; the posts' own parking links are behind a login, so pins are approximate
unless conf says otherwise. Hike details come only from data/sources/hith_hikes.csv.
"""
OSM = "approx (OpenStreetMap: {})"
JH, BS, GE, SH, MO = "Jerusalem hills", "Beit Shemesh / Mateh Yehuda", "Gush Etzion", "Shfela", "Modiin area"
BARBAHAR = (31.73455, 35.07147, "exact (Nahal Katlav parking, CoffeeTrail pin)")
SATAF = (31.77552, 35.12693, "exact (OSM: Sataf upper parking)")
BRIT = (31.68889, 34.92799, OSM.format("Park Britannia area"))
KOBI = (31.72571, 35.11756, OSM.format("Ein Kobi spring, by the Kobi Bridge lot"))

def e(id, he, ll, area, also=(), note=""):
    lat, lng, conf = ll
    return dict(id=id, name_he=he, lat=lat, lng=lng, conf=conf, area=area, also=list(also), note=note)

def o(lat, lng, what): return (lat, lng, OSM.format(what))

NEW = {
"schuster-trail": e("nahal-katlav-scenic", "שביל הנוף נחל קטלב", BARBAHAR, JH, note="Starts at the Bar Bahar café lot."),
"nahal-sorek-beyond": e("nahal-sorek-and-beyond", "נחל שורק ומעבר לו", BARBAHAR, JH),
"sorek-lookout-path": e("sorek-lookout-path", "טיילת תצפית שורק", BARBAHAR, JH),
"har-giora-5k-woodland-walk": e("har-giora", "הר גיורא", o(31.74474, 35.08189, "Har Giora peak"), JH, also=["har-giora"]),
"best-hike-jerusalem-sataf-mt-eitan": e("mount-eitan-loop", "סובב הר איתן", SATAF, JH, also=["mount-eitan-the-summit-and-the-watering-hole"]),
"mount-heret-jerusalem-mountains": e("mount-heret-loop", "סובב הר חרת", SATAF, JH),
"mount-tayasim-to-tayasim-spring": e("tayasim-spring", "מהר טייסים לעין טייסים", o(31.77416, 35.09007, "Har Tayasim peak"), JH),
"begin-park-kobi-ruins-trail": e("kobi-ruins-trail", "שביל חורבת כובי - פארק בגין", KOBI, JH),
"winter-river-nahal-refaim": e("nahal-refaim-winter", "נחל רפאים בחורף", KOBI, JH, also=["beyond-kobi-bridge"]),
"discoveries-kobe-bridge-to-mount-shalmon": e("mount-shalmon", "הר שלמון", o(31.75087, 35.12342, "Mount Shalmon"), JH),
"the-springs-trail-revamped": e("springs-trail-jerusalem", "שביל המעיינות", o(31.75100, 35.12939, "Hurvat Seadim"), JH,
    also=["shvil-hamaayanot-springs-trail-jerusalem", "jerusalem-springs-loop-trail", "through-a-forested-mountain-to-havat-hagitot"]),
"the-hadassah-trail": e("hadassah-trail", "שביל הדסה", o(31.76215, 35.13876, "Ein Hendek"), JH),
"ein-hindak-a-cool-wet-adventure-in-jerusalem": e("ein-hindak", "עין חנדק", o(31.76215, 35.13876, "Ein Hendek spring"), JH),
"the-ein-sapir-springs-trail": e("ein-sapir-springs", "מעיינות אבן ספיר", o(31.76011, 35.13299, "Ein Sapir spring"), JH),
"just-roll-with-it-ein-tzova": e("ein-tzova", "עין צובה ותל צובה", o(31.78289, 35.12941, "Ein Tzova spring"), JH),
"peace-and-beauty-at-ein-kfira": e("ein-kfira", "עין כפירה", o(31.83006, 35.09085, "Ein Kfira spring"), JH),
"spring-beauty-at-ein-mevasser": e("ein-mevasser", "עין מבשר", o(31.80104, 35.15825, "Ein Mevasser spring"), JH),
"loop-trail-to-the-beit-zayit-dam": e("beit-zayit-dam", "מעין כרם לסכר בית זית", o(31.78028, 35.15606, "Beit Zayit dam"), JH,
    also=["hike-for-cheaters-to-derech-hagefen-cafe"], note="Walk starts at a small lot in Ein Karem."),
"kedoshim-forest-carmila-mountain-riverbed": e("kedoshim-forest", "יער הקדושים - הר כרמילה", o(31.77063, 35.04190, "Kedoshim Forest"), JH),
"woodland-and-springs-adventure-near-jerusalem-einot-boker-loop": e("einot-boker", "עינות בוקר ועין כסלון", o(31.78038, 35.05746, "Einot Boker spring"), JH,
    also=["tel-kisalon-wild-beauty"]),
"nahal-yitla-scenic-trail": e("nahal-yitla", "נחל יתלה - שביל הנוף", o(31.82048, 35.06379, "Nahal Yitla, Neve Ilan forest"), JH,
    also=["nahal-yitla-neve-ilan-forest", "nahal-yitla-the-long-way-around"]),
"ilan-stream": e("nahal-ilan", "נחל אילן", o(31.81427, 35.04779, "Nahal Ilan"), JH),
"hike-into-the-holy-city-from-nahal-halilim-to-lifta": e("nahal-halilim", "נחל חלילים לליפתא", o(31.80481, 35.16281, "Nahal Halilim"), JH,
    also=["nahal-halilim"]),
"the-jerusalem-forest-wilderness-in-the-city": e("jerusalem-forest", "יער ירושלים", o(31.78210, 35.18609, "Jerusalem Forest"), JH),
"gazelle-valley-jerusalem": e("gazelle-valley", "עמק הצבאים", o(31.76022, 35.19549, "Gazelle Valley"), "Jerusalem"),
"nebi-samuel-national-park-history-and-fun-in-one": e("nebi-samuel", "גן לאומי נבי סמואל", o(31.83279, 35.18037, "Nebi Samuel site"), "Jerusalem (north)"),
"mount-kitron-tzur-hadassa": e("mount-kitron", "הר כתרון - צור הדסה", o(31.71536, 35.08397, "Mount Kitron peak"), JH),
"journey-to-the-clouds-mount-sansan": e("mount-sansan", "הר סנסן דרך עין גרס", o(31.71131, 35.06621, "Ein Geres spring"), JH),
"loop-trail-at-mount-refaim": e("mount-refaim", "סובב הר רפאים - מבוא ביתר", o(31.72272, 35.10712, "Mevo Beitar"), JH),
"green-valleys-and-a-hasmonean-fortress-hurvat-toura": e("hurvat-toura", "חורבת טורה", (31.75537, 35.06125, "exact (OSM: Hurvat Tura viewpoint)"), JH),
"off-the-beaten-track-around-har-yaale": e("har-yaale", "סובב הר יעלה", o(31.75109, 35.04253, "Har Yaale peak"), BS,
    also=["mount-yaale-summit-and-ancient-ruins-at-the-sorek-reserve"]),
"hike-to-the-stalactite-cave": e("hike-to-soreq-cave", "מהר יעלה למערת הנטיפים", o(31.75109, 35.04253, "Har Yaale (picnic area start)"), BS),
"nahal-hameara": e("nahal-hameara", "נחל המערה - בית עיטאב", o(31.73443, 35.05284, "Beit Itab viewpoint"), BS,
    also=["nahal-hameara-the-best-local-hike", "sweet-and-simple-in-nes-harim-beit-itab"]),
"maarat-hateumim-twins-cave-trail": e("maarat-hateumim", "מערת התאומים", o(31.72623, 35.02052, "Twins Cave entrance"), BS),
"shimshons-cave-a-new-approach": e("shimshons-cave", "מערת שמשון", o(31.76384, 35.02603, "Shimshon's Cave"), BS, also=["climb-to-shimshons-cave"]),
"nahal-dolev-one-way-trail": e("nahal-dolev", "נחל דולב", o(31.73865, 35.02938, "Nahal Dolev"), BS, also=["nahal-dolev"]),
"nahal-zanoah-to-ein-mata": e("nahal-zanoah-ein-mata", "נחל זנוח לעין מטע", o(31.71476, 35.05177, "Ein Mata spring"), BS, also=["beyond-ein-mata"]),
"yishi-forest-a-walk-in-the-woods": e("yishi-forest", "יער ישעי", o(31.72263, 34.95720, "Yishi Forest"), BS),
"isolated-beauty-and-history-hurvat-kiyafeh": e("hurvat-kiyafeh", "חורבת קייאפה", o(31.69643, 34.95736, "Hurvat Qeiyafa site"), BS),
"tzora-forest-6k-loop-trail": e("tzora-forest-6k", "יער צרעה - מסלול 6 ק\"מ", o(31.78019, 34.97621, "Tzora Forest recreation area"), BS),
"tzora-forest-7k-the-north-side": e("tzora-forest-north", "יער צרעה - הצד הצפוני", o(31.77622, 34.98936, "Tzora lookout"), BS),
"beautiful-views-around-mount-tnufa": e("mount-tnufa", "הר תנופה", o(31.78461, 34.97059, "Mount Tnufa"), BS),
"red-poppies-on-burma-road": e("burma-road", "דרך בורמה - מצפה הראל", (31.80775, 34.96417, "exact (OSM: Mitzpe Harel viewpoint)"), BS,
    also=["burma-road", "journey-to-the-past-burma-road-and-shaar-hagay-part-one"]),
"midras-ruins-trail-park-adulam": e("midras-ruins", "חורבת מדרס", o(31.65594, 34.93747, "Hurvat Midras site"), SH),
"tale-of-two-cities-burgin-and-itri-ruins": e("itri-burgin-ruins", "חורבת עתרי וחורבת בורגין", o(31.64923, 34.97213, "Hurvat Itri site"), SH,
    also=["adulam-hurvat-yonim", "little-loop-in-adulam"]),
"tel-adulam": e("tel-adulam", "תל עדולם", o(31.65062, 35.00203, "Tel Adulam"), SH),
"shvil-haelot-2-5k-loop-trail-in-park-britannia": e("shvil-haelot-britannia", "שביל האלות - פארק בריטניה", BRIT, SH,
    also=["borot-beerot-park-britannia", "simple-pleasures-einav-trail-in-park-britannia"]),
"mitzpe-massua-trail-park-britannia": e("mitzpe-massua", "מצפה משואה", (31.66730, 34.92265, "exact (OSM: Mitzpe Massua tower)"), SH),
"britannia-park-hurvat-tsura-and-tel-goded": e("hurvat-tsura-tel-goded", "חורבת צורה ותל גודד", o(31.64678, 34.91705, "Hurvat Tsura"), SH,
    also=["park-britannia-tel-goded-and-hurvat-tabak"]),
"hike-dine-park-britannia-cafe-hike": e("britannia-agrocafe-hike", "פארק בריטניה ואגרו קפה", BRIT, SH,
    note="AgroCafe's kashrut is only stated by the blog post ('kosher') – not verified; not on the food list."),
"tel-tzafit-a-beautiful-walk-through-history": e("tel-tzafit", "תל צפית", (31.70198, 34.84740, "exact (OSM: Tel Tzafit viewpoint)"), SH),
"wander-in-a-woodland-haruvit-forest": e("haruvit-forest", "יער חרובית - שביל בן הסלעים", o(31.73751, 34.89716, "Haruvit Forest"), SH,
    also=["haruvit-forest-loop"]),
"tel-lachish-beauty-at-an-ancient-city": e("tel-lachish", "תל לכיש", o(31.56552, 34.84919, "Tel Lachish site"), SH),
"gevaot-gad-climb-to-a-sheikhs-tomb": e("gevaot-gad", "שמורת גבעות גד", o(31.52118, 34.88193, "Gevaot Gad reserve"), SH, also=["gevaot-gad-hills-and-tunnels"]),
"flowers-and-golden-grain-at-tel-gezer": e("tel-gezer", "תל גזר", o(31.85972, 34.92250, "Tel Gezer"), MO),
"spring-valley-park-canada": e("spring-valley-park-canada", "עמק המעיינות - פארק קנדה", o(31.84146, 35.00704, "Park Canada recreation area"), MO,
    also=["ayalon-forest-7k-loop-trail", "exploring-park-canada-the-ayalon-trail"]),
"ben-shemen-forest-walk": e("ben-shemen-forest", "יער בן שמן", o(31.93595, 34.95980, "Ben Shemen Forest"), MO, also=["ben-shemen-forest-tel-hadid-to-hurvat-gimzu"]),
"hulda-forest-journey-into-the-past": e("hulda-forest", "יער חולדה", o(31.82314, 34.89341, "Hulda Forest"), MO),
"get-your-feet-wet-hameginim-forest-and-varda-spring": e("hameginim-varda", "יער המגינים ועין ורדה", o(31.84091, 34.92857, "HaMeginim Forest"), MO,
    also=["woodland-hike-in-hameginim-forest"]),
"rosh-tzurim-loop-trail": e("rosh-tzurim-loop", "סובב ראש צורים", o(31.65744, 35.12127, "Lone Oak, Path of the Patriarchs"), GE),
"path-of-the-patriarchs": e("path-of-the-patriarchs", "דרך האבות", o(31.67619, 35.14283, "Neve Daniel"), GE),
"derech-ephraim-judean-hills-trail-an-indian-restaurant-in-a-bus": e("derech-ephraim", "דרך אפרים - נווה דניאל", (31.68262, 35.14498, "exact (OSM: Mitzpor HaElef, where the post says to park)"), GE),
"gevaot-forest-cafe-in-the-grove": e("gevaot-forest", "יער גבעות", o(31.67896, 35.10115, "Gevaot village"), GE),
"cafe-hike-at-kashuela-farm": e("kashuela-farm", "חוות קשואלה", o(31.67601, 35.10170, "Kashuela Farm"), GE,
    note="The farm café's kashrut isn't stated – not on the food list."),
"jumjum-ruins-and-bat-ayin-springs": e("jumjum-bat-ayin", "חורבת ג'ומג'ום ומעיינות בת עין", o(31.66867, 35.10190, "Hurvat JumJum"), GE),
"hiking-through-the-biyar-aqueduct": e("biyar-aqueduct", "אמת הביאר", o(31.65613, 35.14514, "Biyar aqueduct"), GE),
"tekoa-canyon-circular-trail": e("tekoa-canyon", "נחל תקוע ומערת חריטון", o(31.64495, 35.23617, "Haritoun Cave"), "Gush Etzion (east)",
    also=["nahal-tekoa-valley-of-monks-and-kings", "nahal-tekoa-and-the-haritoun-cave", "tekoa-canyon-autumn-crocus-trail"]),
"herodion-a-trail-through-time": e("herodion", "גן לאומי הרודיון", (31.66561, 35.24182, "exact (OSM: Herodion)"), "Gush Etzion (east)",
    also=["herodion-to-nahal-tekoa"]),
}

# Existing map hikes -> the post that now supplies their trail details.
UPDATE = {
    "sataf-springs": ("wet-fun-at-sataf", ["sataf-choose-your-own-adventure-walk"]),
    "ein-kobi": ("walk-to-ein-kobi", ["into-jerusalem-ein-kobe-to-ein-lavan"]),
    "nahal-katlav": ("true-nahal-katlav", []),
    "tel-azeka": ("taking-it-easy-at-tel-azeka", []),
    "ein-lavan-ein-hanya": ("two-springs-in-the-city-ein-lavan-and-ein-hania", []),
    "ein-livne": ("bat-ayin-springs-trail-ein-livne", []),
    "oz-vegaon": ("oz-vegaon-loop-trail", []),
    "beit-guvrin": ("adventures-at-tel-maresha-beit-guvrin", []),
}
# Official pages stay the source of truth for these; the post is added as an extra source only.
EXTRA_SOURCE = {
    "ein-hemed": "sweet-spot-at-ein-hemed",
    "ein-tzurim-pools": "ein-tzurim-trail-to-a-spring",
}
