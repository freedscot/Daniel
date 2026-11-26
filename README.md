# Kosher Hike + Coffee Map (Israel)

Phase 1: data. Phase 2 (app) and Phase 3 (hosting) come next.

- `data/places.json`: the master list that the app will read.
- `data/places_mymaps.csv`: import into Google My Maps (Create map → Import → choose file → pick `lat`/`lng` for position and `name_en` for the title).
- `scripts/build_data.py`: the source. Edit places here, then run `python3 scripts/build_data.py` to rebuild both files.

## Data rules
- `kashrut_status` / `hours.status` = `unconfirmed` until someone has seen the teudat kashrut or the place's own current hours. Every entry has a `last_checked` date.
- `coords_confidence` = `approx`: the pin is near the place, not exact. Verify it before relying on it for navigation.
- Kashrut levels: `badatz`, `rabbanut_mehadrin`, `rabbanut_regular`, `other`, `unconfirmed`.
