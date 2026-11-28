# Kosher Hike + Coffee Map (Israel)

A phone-friendly map of kosher coffee carts, food trucks and hikes near Ramat Bet Shemesh. It's a static site with no server: open `index.html` through any web server, or host it on GitHub Pages.

## The app
- `index.html`, `app.js`, `styles.css`: the app. It reads `data/places.json`.
- Map: Leaflet + OpenStreetMap (bundled in `vendor/leaflet`, no API key needed).
- Drive times ("Near me" and the hike pairings) come from the free public OSRM router. If that's unavailable, the app shows straight-line distances labelled "approx.".
- Tapping Google Maps opens the place in the Google Maps app (food spots are searched by name so you see reviews and photos). Waze opens navigation to the pin.
- "I've been here" and personal notes are saved on the phone itself (browser storage), not in the data file.
- `manifest.webmanifest`, `sw.js`, `icons/`: make it installable ("Add to Home screen") and usable offline. Map areas you've already viewed are cached.

## Adding a place from Google Maps or Instagram
- In the app: **➕ Suggest a place** (bottom of the list or filters), or on Android **Share → Coffee & Tiyul** from Google Maps or Instagram. Either one opens a ready-made GitHub issue ("Add place: @handle"); tap Submit.
- Or just paste the link to Claude in any session on this repo.
- Claude follows `.claude/skills/add-place/SKILL.md`: it matches the handle in `data/sources/coffeetrail_index.json` (rebuild with `python3 scripts/coffeetrail_index.py`), drafts an entry with `python3 scripts/add_place.py`, checks it, rebuilds and publishes. Added places live in `data/sources/added_places.json`.

## Data

- `data/places.json`: the master list that the app will read.
- `data/places_mymaps.csv`: import into Google My Maps (Create map → Import → choose file → pick `lat`/`lng` for position and `name_en` for the title).
- `scripts/build_data.py`: the source. Edit places here, then run `python3 scripts/build_data.py` to rebuild both files.

## Data rules
Every place has a `last_checked` date.

**`kashrut_status` / `hours.status`** tell you who said it:
- `certificate_seen`: you photographed the certificate (photos in `data/sources/certificates/`; `kashrut_valid_until` holds the expiry).
- `owner_stated`: the business says it, on its own website or in an owner-verified CoffeeTrail listing. Nobody has seen the certificate in person yet.
- `official`: from the Nature & Parks Authority, KKL or a regional tourism authority.
- `third_party`: from a guide site, an article or a social post. Treat as unconfirmed.
- `user_reported`: from your own visit or knowledge (shown in the app as "Your own report").
- `unconfirmed`: no reliable source.

**Hike details (`details_status`, `details_source`):** `official` (KKL, Parks Authority or Etzion Tourism) or `blog_post` (a Hiking the Holyland post, read in full; see `data/sources/hith_hikes.csv`). Fields the post doesn't mention are left empty. `scripts/hith_mapping.py` lists which posts are on the map and where each pin is.

**Kashrut levels:** `badatz`, `rabbanut_mehadrin`, `rabbanut_regular`, `other` (e.g. a private hashgacha), `unconfirmed`.

**`coords_confidence`:** `exact` (a CoffeeTrail pin or an OpenStreetMap feature), `plus_code_from_own_site`, or `approx` (check before you navigate).
