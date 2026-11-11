#!/usr/bin/env python3
"""The Trip Sort landing's pictures, from the game's own art.

Reads:
  ~/Documents/TripSortDart/build/landing/  drawn by the game's
      test/render/landing_art_render_test.dart (hero, og, landmarks, plane,
      covers/<slug>.png)
  ~/Downloads/tripsort/screenshots/en/     the store screenshots (iphone-0N.png)
  ~/Documents/TripSortDart/assets/icons/   button art (boosters, lives...)
  ~/Documents/TripSortDart/build/store/world.png  the planet
Writes WebP and JPEG into tripsort/assets/img/.

Run: python3 tools/tripsort-landing/assets.py        (all of them)
     python3 tools/tripsort-landing/assets.py hero   (only the hero scene's pieces)
"""
import pathlib
from PIL import Image

HOME = pathlib.Path.home()
GAME = HOME / 'Documents/TripSortDart'
ART = GAME / 'build/landing'
SHOTS = HOME / 'Downloads/tripsort/screenshots/en'
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / 'tripsort/assets/img'

# The store screenshots, in the store's order, named by what they show.
SHOT_NAMES = ['match-3-tiles', '291-destinations', 'travel-the-world', 'train-your-brain', 'relax-and-unwind', 'play-offline']

# Where the store screenshots' title band ends (1320 x 2868): below it is
# the game's own screen.
BAND_BOTTOM = 376

ICONS = {'hint': 'hint_btn', 'undo': 'undo_btn', 'wand': 'wand_btn', 'shuffle': 'shuffle_btn', 'slot': 'slot_btn',
         'ticket': 'ticket', 'coins': 'coins_3', 'map': 'tab_map', 'star': 'star_btn', 'trophy': 'trophy_btn'}


def save(im, path, width=None, quality=82):
    path = OUT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    if width and im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    if path.suffix == '.jpg':
        im.convert('RGB').save(path, quality=quality, optimize=True, progressive=True)
    else:
        im.save(path, quality=quality, method=6)
    print(f'{path.relative_to(OUT)} {im.width}x{im.height} {path.stat().st_size // 1024} KB')


def main():
    hero = Image.open(ART / 'hero.png').convert('RGBA')
    save(hero, 'hero.webp', 1200)
    save(hero, 'hero-840.webp', 840)
    save(Image.open(ART / 'og.png'), 'og-trip-sort-2.jpg', 1200, quality=86)
    save(Image.open(ART / 'landmarks.png').convert('RGBA'), 'landmarks.webp', 1500)
    save(Image.open(ART / 'plane.png').convert('RGBA'), 'plane-route.webp', 900)
    for cover in sorted((ART / 'covers').glob('*.png')):
        save(Image.open(cover), f'guides/{cover.stem}.jpg', 1200, quality=84)
    for i, name in enumerate(SHOT_NAMES, 1):
        shot = Image.open(SHOTS / f'iphone-0{i}.png').convert('RGB')
        save(shot, f'shots/{name}.webp', 480, quality=84)
        # The game's screen alone, for a phone frame on the page.
        if name in ('291-destinations', 'travel-the-world'):
            save(shot.crop((0, BAND_BOTTOM, shot.width, shot.height)), f'features/{name}.webp', 640, quality=84)
    for name, art in ICONS.items():
        save(Image.open(GAME / f'assets/icons/{art}.webp').convert('RGBA'), f'icons/{name}.webp', 128, quality=88)
    planet = Image.open(GAME / 'build/store/world.png').convert('RGBA')
    save(planet.crop(planet.getbbox()), 'icons/planet.webp', 128, quality=88)
    hero_pieces()


# The living hero's pieces (the scene at the top of index.html): the planet,
# each tile alone (drawn by the same render test as hero tile <type>), the
# clouds, and the plane's sheets cut down from the game's: 64 of its 128
# headings (the page blends two neighbours, as the game does) at three
# quarters of the size, and the propeller every other of its headings.
HERO_TILES = ['autobusrojo', 'eiffel', 'gondolavenice', 'mascarazorrokyoto', 'globoluxor']


def cells(sheet, size, per_row, picks, out_size, out_per_row=8):
    """The cells [picks] of a sheet of [size] cells, [per_row] a row, in a new
    sheet of [out_size] cells, [out_per_row] a row."""
    (w, h), (ow, oh) = size, out_size
    rows = -(-len(picks) // out_per_row)
    out = Image.new('RGBA', (out_per_row * ow, rows * oh))
    for i, n in enumerate(picks):
        cell = sheet.crop((n % per_row * w, n // per_row * h, n % per_row * w + w, n // per_row * h + h))
        out.paste(cell.resize(out_size, Image.LANCZOS), (i % out_per_row * ow, i // out_per_row * oh))
    return out


def hero_pieces():
    save(Image.open(GAME / 'build/store/world.png').convert('RGBA'), 'hero/world.webp', 640, quality=84)
    for t in HERO_TILES:
        save(Image.open(ART / f'hero/tile_{t}.png').convert('RGBA'), f'hero/tile-{t}.webp', 260, quality=86)
    for n in (1, 2, 3):
        save(Image.open(GAME / f'assets/backdrops/cloud_{n}.webp').convert('RGBA'), f'hero/cloud-{n}.webp', 360, quality=86)
    plane = Image.open(GAME / 'assets/backdrops/plane.webp').convert('RGBA')
    save(cells(plane, (282, 182), 14, [2 * i for i in range(64)], (212, 137)), 'hero/plane.webp', quality=78)
    # The game's propeller cell is heading * 2 + blade, for 64 headings.
    prop = Image.open(GAME / 'assets/backdrops/plane_prop.webp').convert('RGBA')
    save(cells(prop, (134, 136), 16, [4 * (i // 2) + i % 2 for i in range(64)], (100, 102)), 'hero/prop.webp', quality=80)


if __name__ == '__main__':
    import sys
    hero_pieces() if sys.argv[1:] == ['hero'] else main()
