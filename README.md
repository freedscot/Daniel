# Kosher Hike + Coffee Map (Israel)

Phase 1: data. Phase 2 (app) and Phase 3 (hosting) come next.

- `data/places.json`: the master list that the app will read.
- `data/places_mymaps.csv`: import into Google My Maps (Create map → Import → choose file → pick `lat`/`lng` for position and `name_en` for the title).
- `scripts/build_data.py`: the source. Edit places here, then run `python3 scripts/build_data.py` to rebuild both files.

## Data rules
Every place has a `last_checked` date.

**`kashrut_status` / `hours.status`** tell you who said it:
- `owner_stated`: the business says it, on its own website or in an owner-verified CoffeeTrail listing. Nobody has seen the certificate in person yet.
- `official`: from the Nature & Parks Authority, KKL or a regional tourism authority.
- `third_party`: from a guide site, an article or a social post. Treat as unconfirmed.
- `unconfirmed`: no reliable source.

**Kashrut levels:** `badatz`, `rabbanut_mehadrin`, `rabbanut_regular`, `other` (e.g. a private hashgacha), `unconfirmed`.

**`coords_confidence`:** `exact` (a CoffeeTrail pin or an OpenStreetMap feature), `plus_code_from_own_site`, or `approx` (check before you navigate).
