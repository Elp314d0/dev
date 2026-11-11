# Brief for writing a Trip Sort guide

You write the BODY of one SEO guide for the Trip Sort landing (dezeo.lat/tripsort/guides/<slug>/).
`build.py` wraps your file with the head, header, title (h1), cover image, related guides and footer,
so you write only what goes after the cover image.

## Files you write (only these)

- `content/<slug>.html`: the article body in English (fragment, no <html>/<head>/<body>, no h1).
- `content/<slug>.faq.json`: `[["question", "answer"], ...]`, the same 3 "people also ask" questions you put at the end,
  in English, plain text.

Read `guides.json` for the slug, keyword, secondary keywords, titles and descriptions. Don't edit it.

## Format rules

- The site is English only. No translations, no `data-lang` spans, no language switcher.
- Structure:
  1. `<p class="lede">`: answer the search intent in the first two sentences (featured-snippet style), with the main keyword.
  2. 4 to 6 `<h2>` sections that genuinely answer what the searcher wants (general, useful, not an ad), with lists or numbered steps where it helps. Put the main keyword naturally in at least one h2 and the secondary keywords where they fit. No keyword stuffing.
  3. At least one figure using the real images below.
  4. A `<div class="callout">` titled "How to do it in Trip Sort" (h2) with an `<ol>` of concrete steps in the app, then
     `<p><a class="btn btn-primary" href="../../#download">Download Trip Sort free</a></p>`
  5. Optional `<div class="tip"><p>...</p></div>` with a pro tip.
  6. `<h2>` "Questions people also ask" with 3 `<h3>` + `<p>` pairs (the same 3 go in the faq.json).
- Link naturally to 1 or 2 other guides: `<a class="inline" href="../<other-slug>/">...</a>` (slugs in guides.json).
- Length: about 900–1,300 words. Indent with 4 spaces (it sits inside `<div class="narrow">`).
- No emojis. No "best", "#1", "top" claims about Trip Sort. Don't name or criticize competitor apps (generic genres like "mahjong solitaire" are fine).
- No health or medical claims (no "improves memory", "reduces anxiety", "prevents dementia"). Say things like "keeps your mind busy", "a calm break", "practice attention and planning".
- Only claim game facts listed below. If you are not sure something exists in the game, don't mention it.

## Images you can use (paths relative to the guide page)

- Store screenshots of version 2.0, 480x1043, in `../../assets/img/shots/`:
  `match-3-tiles.webp` "Match 3 Tiles!" (Paris board, Eiffel tiles in the tray) ·
  `291-destinations.webp` "291 Destinations" (Your Trip, the travel album: postcards of Strasbourg and Paris, a city stamp) ·
  `travel-the-world.webp` "Travel the World" (home: the planet with its landmarks and the Level button) ·
  `train-your-brain.webp` "Train Your Brain" (Kyoto board, torii, fox masks, sushi) ·
  `relax-and-unwind.webp` "Relax & Unwind" (Santorini board) · `play-offline.webp` "Play Offline" (London board, Big Ben, double-decker bus).
  Use as:
  ```html
    <figure class="phone">
      <img src="../../assets/img/shots/match-3-tiles.webp" width="480" height="1043" loading="lazy" alt="...">
      <figcaption>...</figcaption>
    </figure>
  ```
- Wide art (no text in it), use `<figure><img ...></figure>`:
  `../../assets/img/plane-route.webp` (900x640, the toy plane flying a dotted route) ·
  `../../assets/img/landmarks.webp` (1500x900, twelve landmark tiles).
  Both are drawn with the game's own pieces by TripSortDart's `test/render/landing_art_render_test.dart`,
  like the guide covers.
  Alt text: descriptive, with a keyword where natural.

## Trip Sort facts (the only things you may claim)

- Name: "Trip Sort: Triple Tile Match". iPhone and Android. Made by the studio dezeo (Nicolas Gula).
- Free to play, with optional in-app purchases and ads. A single "Remove Ads" purchase turns off the ads between levels.
  Rewarded videos are always optional (continue after a loss, extra hints). Restore Purchases is in the Shop.
- How to play: tap a tile and it moves into the tray. The tray has 4 slots. Three identical tiles in the tray clear.
  Only tiles that are not covered by other tiles can be picked. Clear every tile to finish the level.
  If the tray fills up with no match, the level is lost; you can continue (with a rewarded video or coins) or retry.
- Lives (since 2.0): a level only costs a life if you don't win it.
- Hard Levels (since 2.0): they pay double and are always solvable.
- No timers. Early boards are calm and easy; later boards stack tiles in layers and ask you to think a few moves ahead.
- 291 real destinations on every continent, 12 levels each (over 3,400 levels). The trip starts in Montevideo.
  (36 of them reach players in weekly batches from 1 to 22 December 2026.)
- Each city has its own tiles: Paris has the Eiffel Tower, croissants and macarons; Kyoto torii gates and sushi;
  Rio Christ the Redeemer and toucans; Buenos Aires tango shoes and mate; London Big Ben and the double-decker bus.
- Every level adds a piece to the city's postcard. Finishing a city adds its stamp to Your Trip, the travel album, then
  the toy plane flies to the next stop across the map (you can tap to skip it). Home is a little planet with the plane
  flying around it, and a won level ends with a victory show of fireworks and raining coins.
- 23 famous landmarks to collect, earned when you complete the destination where they stand: Eiffel Tower, Fushimi Inari Torii,
  Itsukushima Pagoda, Christ the Redeemer, Leaning Tower of Pisa, Colosseum, Chichen Itza, Statue of Liberty, Big Ben,
  Taj Mahal, Great Pyramid, Sydney Opera House, Saint Basil's Cathedral, Great Wall of China, Treasury of Petra,
  Angkor Wat, Parthenon, Burj Khalifa, Hagia Sophia, Brandenburg Gate, Abu Simbel, Uluru, Mount Fuji.
  Each landmark comes with a short real-world story.
- Boosters: Hint (lights up your best move), Undo (puts your last tile back on the board), Magic Wand (clears a whole set for you),
  Shuffle (mixes up the tiles left on the board), Extra Slot (adds a fifth slot to the tray). You start with some and can buy more with coins.
- Coins, daily rewards, daily missions, a Daily Challenge and achievements.
- No replays: what you win stays won. Tapping a finished city in Your Trip opens its postcard.
- Settings: the gear icon. Sound, Music and Vibration each have their own switch. Calm music, one relaxing tune per level, looping.
- Works offline: every level plays with no internet. Offline there are simply no ads and the Shop is not available.
- No account and no sign-up. Progress is saved on the device (deleting the game deletes progress).
- The game is translated into 70+ languages.
