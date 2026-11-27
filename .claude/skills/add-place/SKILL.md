---
name: add-place
description: Add a kosher coffee cart / café / food truck (or a hike) to the Coffee & Tiyul map from an Instagram link, or process open "Add place:" GitHub issues created by the app's "Suggest a place" button. Use whenever the user pastes an Instagram/Facebook/website link for a place, or asks to process place requests.
---

# Add a place from a link

The owner pastes a link (usually Instagram) and expects you to research the place, add it to the map, and publish. Requests also arrive as GitHub issues in this repo titled `Add place: …` (made by the app's "➕ Suggest a place" button or Android Share).

## Kashrut rules (non-negotiable)
- Record the **exact** hechsher text the source gives (Hebrew is fine), e.g. `רבנות מטה יהודה` + level `rabbanut_mehadrin`.
- Levels: `badatz`, `rabbanut_mehadrin`, `rabbanut_regular`, `other`, `unconfirmed`. A "Mehadrin" certificate with no certifying body named → level `unconfirmed`, body `not stated`.
- `kashrut_status`: `owner_stated` (the business itself: its own site, or an owner-verified CoffeeTrail listing), `official` (regional tourism authority/INPA/KKL), `third_party` (guides, articles, social posts by others), `user_reported` (the owner told you from his own visit/knowledge — record it as he said, with the date), `unconfirmed`. The Ministry of Religious Services registry (shown on kasher.info, with valid-until date) counts as `official`. Same scale for `hours.status`.
- **Never guess.** Missing hechsher or hours → `unconfirmed`, and set `last_checked` to today.
- A place open on Shabbat is a red flag: say so in `kashrut_note` and tell the owner; don't present it as kosher without a clear certificate.

## Steps
1. **Get the handle** from the link (`instagram.com/<handle>`). Instagram itself can't be read (login wall / blocked) — don't try to get around that.
2. **Look it up:** `python3 scripts/add_place.py lookup <link>`. It searches `data/sources/coffeetrail_index.json` (every CoffeeTrail cart, with Instagram handles) and reports `ALREADY ON MAP` duplicates. If it's already on the map, tell the owner and stop (or update that entry if the info changed).
   - Index stale or no match? Rebuild it: `python3 scripts/coffeetrail_index.py` (a few minutes), then retry.
   - Still no match: research by name/handle — the place's own website, Etzion Tourism (etziontour.org.il), CoffeeTrail search, web search. Read pages you cite; don't rely on search snippets for kashrut or hours.
3. **Draft:** `python3 scripts/add_place.py draft <coffeetrail-slug> --name-en "English name" [--type cart|cafe|food_truck]` appends an entry to `data/sources/added_places.json`. For a non-CoffeeTrail place, add the entry to that file by hand with the same fields (see an existing entry; `hours.by_day` keys `sun`…`sat`, values like `"08:00-14:00"`, `"closed"` or `null`).
4. **Review the draft by hand:** sensible English name and `id`; `area` (the helper copies the nearest place's area — fix "SET AREA"); `type`; `dairy_meat` if the menu shows it; read the CoffeeTrail page itself to confirm the hechsher text and hours; check the owner's note for "closed for now"/winter break. Coordinates: CoffeeTrail pin (exact) or an OpenStreetMap lookup (mark `approx`).
5. **Build and check:** `python3 scripts/build_data.py` (fails on duplicate ids). Optionally serve locally (`python3 -m http.server`) and open `#<id>` to see the detail page.
6. **Publish:** commit (`Add <name> from Instagram link`) and push to the working branch; GitHub Pages republishes in ~2 minutes.
7. **Report back** in a few lines: name, hechsher exactly as stated + who stated it, Friday hours, nearest hikes, anything unconfirmed or suspicious. If it came from an issue, comment the same summary on the issue (end with the repo's comment footer) and close it; if you couldn't add it, comment why and leave it open.

## Processing requests in bulk
"Process place requests" = list open issues in this repo whose title starts with `Add place:`, do the steps above for each, one commit per place (or one commit for the batch), then comment and close each.
