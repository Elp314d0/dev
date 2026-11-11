#!/usr/bin/env python3
"""Builds the Trip Sort guides from guides.json and content/<slug>.html.

Each content file holds only the body of the article, in English (the site
is English only since October 2026). This script wraps the body with the shared head, header, footer and
structured data, writes tripsort/guides/<slug>/index.html and the guides
index, and refreshes the guides grid on the landing between the
<!-- guides:start --> and <!-- guides:end --> markers.

Run: python3 tools/tripsort-guides/build.py
"""
import html
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent / 'tripsort'
BASE = 'https://dezeo.lat/tripsort/'
PUBLISHED = '2026-10-12'
UPDATED = '2026-11-10'
APP_STORE = 'https://apps.apple.com/app/trip-sort-triple-tile-match/id6818841022'
PLAY = 'https://play.google.com/store/apps/details?id=lat.dezeo.trip_sort'

GUIDES = json.loads((HERE / 'guides.json').read_text(encoding='utf-8'))


def en(text):
    # El sitio es solo en ingles. El texto sigue dentro de un <span>, como
    # cuando cada frase venia en un par ingles/espanol: el CSS no cambia.
    return f'<span>{text}</span>'


def esc(s):
    return html.escape(s, quote=True)


def header(up):
    return f'''<header class="site-header">
  <div class="container">
    <a class="brand" href="{up}">
      <img src="{up}assets/img/tripsort-icon-64.webp" alt="Trip Sort app icon" width="34" height="34">
      <span>Trip <span class="sort">Sort</span></span>
    </a>
    <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">
    <nav class="site-nav" aria-label="Main">
      <a href="{up}#screenshots">{en('Screenshots')}</a>
      <a href="{up}#how-it-works">{en('How it works')}</a>
      <a href="{up}guides/">{en('Guides')}</a>
      <a href="{up}#faq">FAQ</a>
      <a href="/projects.html">{en('All projects')}</a>
      <a class="nav-cta" href="{up}#download">{en('Download')}</a>
    </nav>
    <label class="nav-burger" for="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></label>
  </div>
</header>'''


# Las redes de dezeo, donde salen los videos de Trip Sort.
SOCIAL = '''<div class="footer-social">
          <a href="https://www.tiktok.com/@dezeogsp" target="_blank" rel="noopener" aria-label="Trip Sort videos on TikTok" title="TikTok"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a>
          <a href="https://www.youtube.com/@dezeohq" target="_blank" rel="noopener" aria-label="Trip Sort videos on YouTube" title="YouTube"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
        </div>'''


def footer(up):
    foot = [('triple-tile-match', 'Triple tile match'),
            ('how-to-beat-hard-tile-match-levels', 'Hard level tips'),
            ('offline-games-no-wifi', 'Offline games'),
            ('games-to-play-on-a-plane', 'Games for flights'),
            ('brain-puzzle-games-for-adults', 'Brain games')]
    links = ''.join(f'\n          <li><a href="{up}guides/{s}/">{en(label)}</a></li>' for s, label in foot)
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{up}">
          <img src="{up}assets/img/tripsort-icon-64.webp" alt="Trip Sort app icon" width="34" height="34">
          <span>Trip <span class="sort">Sort</span></span>
        </a>
        <p>{en('A relaxing triple tile match puzzle. Match 3 tiles, train your brain and travel the world, offline.')}</p>
        {SOCIAL}
      </div>
      <div>
        <h4>App</h4>
        <ul>
          <li><a href="{up}#download">{en('Download')}</a></li>
          <li><a href="{up}#screenshots">{en('Screenshots')}</a></li>
          <li><a href="{up}#how-it-works">{en('How it works')}</a></li>
          <li><a href="{up}route/">{en('World route')}</a></li>
          <li><a href="{up}#faq">FAQ</a></li>
          <li><a href="{up}support/">{en('Support')}</a></li>
          <li><a href="/projects.html">{en('All projects')}</a></li>
        </ul>
      </div>
      <div>
        <h4>{en('Guides')}</h4>
        <ul>{links}
          <li><a href="{up}guides/">{en('All guides →')}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Trip Sort · Nicolas Gula · <a href="https://dezeo.lat/">dezeo</a></span>
      <span>
        <a href="{up}privacypolicy/">{en('Privacy Policy')}</a> ·
        <a href="{up}terms/">{en('Terms of Use')}</a> ·
        <a href="{up}support/">{en('Support')}</a>
      </span>
    </div>
  </div>
</footer>'''



def head(title, desc, url, image, up, extra=''):
    return f'''<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#3FB1F2">
  <link rel="icon" type="image/png" href="{up}assets/img/tripsort-icon-180.png">
  <link rel="apple-touch-icon" href="{up}assets/img/tripsort-icon-180.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&display=swap">
  <link rel="stylesheet" href="{up}assets/css/site.css">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Trip Sort">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{image}">{extra}
  <script src="/analitica.js" async></script>'''


def guide_page(g, body):
    slug = g['slug']
    url = f'{BASE}guides/{slug}/'
    image = f'{BASE}assets/img/guides/{slug}.jpg'
    # El <title> puede ser mas corto que el h1: Google corta pasados los ~60 caracteres.
    title = g.get('seo_title') or g['title_en']
    desc = g['desc_en']
    up = '../../'
    faq_path = HERE / 'content' / f'{slug}.faq.json'
    faq_ld = ''
    if faq_path.exists():
        faq = json.loads(faq_path.read_text(encoding='utf-8'))
        faq_ld = '\n  <script type="application/ld+json">\n' + json.dumps({
            '@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]
        }, ensure_ascii=False, indent=2) + '\n  </script>'
    article_ld = json.dumps({
        '@context': 'https://schema.org', '@type': 'Article', 'headline': title, 'description': desc,
        'image': image, 'inLanguage': 'en', 'datePublished': PUBLISHED + 'T12:00:00-03:00', 'dateModified': UPDATED + 'T12:00:00-03:00',
        'author': {'@type': 'Person', 'name': 'Nicolas Gula', 'url': 'https://dezeo.lat/'},
        'publisher': {'@type': 'Organization', 'name': 'dezeo', 'url': 'https://dezeo.lat/',
                      'logo': {'@type': 'ImageObject', 'url': BASE + 'assets/img/tripsort-icon.png'}},
        'mainEntityOfPage': url,
        # Referencia simple: un MobileApplication anidado sin calificaciones sale
        # como 'no valido' en la prueba de resultados enriquecidos de Google.
        'about': {'@type': 'Thing', 'name': 'Trip Sort: Triple Tile Match', 'url': BASE},
    }, ensure_ascii=False, indent=2)
    crumbs = json.dumps({
        '@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Trip Sort', 'item': BASE},
            {'@type': 'ListItem', 'position': 2, 'name': 'Guides', 'item': BASE + 'guides/'},
            {'@type': 'ListItem', 'position': 3, 'name': title}]}, ensure_ascii=False, indent=2)
    extra = f'\n  <script type="application/ld+json">\n{article_ld}\n  </script>\n  <script type="application/ld+json">\n{crumbs}\n  </script>{faq_ld}'
    # Related links: the next three guides in the list, wrapping around.
    i = [x['slug'] for x in GUIDES].index(slug)
    related = [GUIDES[(i + k) % len(GUIDES)] for k in (1, 2, 3)]
    rel = ''.join(f'\n    <a class="guide-card" href="../{r["slug"]}/"><img src="../../assets/img/guides/{r["slug"]}.jpg" width="1200" height="630" loading="lazy" alt=""><div class="body"><span class="tag">{en(esc(r["tag_en"]))}</span><h3>{en(esc(r["title_en"]))}</h3><span class="read">{en("Read the guide →")}</span></div></a>' for r in related)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  {head(title, desc, url, image, up, extra)}
</head>
<body>

{header(up)}

<main>
<article class="article article-hero">
  <div class="narrow">
    <p class="breadcrumb"><a href="{up}">Trip Sort</a> › <a href="../">{en('Guides')}</a></p>
    <h1>{en(esc(g['title_en']))}</h1>
    <p class="meta">{en(f'By Nicolas Gula · Updated {UPDATED} · Trip Sort for iPhone and Android')}</p>
    <img class="cover" src="../../assets/img/guides/{slug}.jpg" width="1200" height="630" alt="{esc(g['title_en'])}">
{body.strip()}
    <section class="related" aria-label="Related guides">
      <h2>{en('Keep reading')}</h2>
      <div class="guides-grid">{rel}
      </div>
    </section>
  </div>
</article>
</main>

{footer(up)}

</body>
</html>
'''


def guide_cards(prefix):
    return ''.join(f'''
        <a class="guide-card" href="{prefix}{g["slug"]}/">
          <img src="{'../' if prefix == '' else ''}assets/img/guides/{g["slug"]}.jpg" width="1200" height="630" loading="lazy" alt="{esc(g["title_en"])}">
          <div class="body">
            <span class="tag">{en(esc(g["tag_en"]))}</span>
            <h3>{en(esc(g["title_en"]))}</h3>
            <p>{en(esc(g["short_en"]))}</p>
            <span class="read">{en("Read the guide →")}</span>
          </div>
        </a>''' for g in GUIDES)


def guides_index():
    url = BASE + 'guides/'
    title = 'Trip Sort Guides: Tile Match Tips, Offline Games and Brain Puzzles'
    desc = 'Guides for tile match players: how triple tile match works, tips for hard levels, offline games for flights, relaxing brain puzzles and how to play Trip Sort.'
    items = [{'@type': 'ListItem', 'position': k + 1, 'url': f'{BASE}guides/{g["slug"]}/', 'name': g['title_en']} for k, g in enumerate(GUIDES)]
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': items}, ensure_ascii=False, indent=2)
    extra = f'\n  <script type="application/ld+json">\n{ld}\n  </script>'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  {head(title, desc, url, BASE + 'assets/img/og-trip-sort-2.jpg', '../', extra)}
</head>
<body>

{header('../')}

<main>
<section class="article-hero">
  <div class="container">
    <div class="section-head">
      <p class="breadcrumb"><a href="../">Trip Sort</a> › {en('Guides')}</p>
      <h1 class="display" style="font-size:clamp(36px,5vw,58px);margin-bottom:14px">{en('Trip Sort guides')}</h1>
      <p>{en('Tile match rules and tips, offline games for your next flight, relaxing brain puzzles and everything Trip Sort can do.')}</p>
    </div>
    <div class="guides-grid">{guide_cards('')}
    </div>
  </div>
</section>
</main>

{footer('../')}

</body>
</html>
'''


def main():
    built = 0
    for g in GUIDES:
        src = HERE / 'content' / f'{g["slug"]}.html'
        if not src.exists():
            print('missing content:', g['slug'])
            continue
        out = SITE / 'guides' / g['slug'] / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(guide_page(g, src.read_text(encoding='utf-8')), encoding='utf-8')
        built += 1
    (SITE / 'guides' / 'index.html').write_text(guides_index(), encoding='utf-8')
    # Landing: the guides grid lives between two markers.
    landing = SITE / 'index.html'
    page = landing.read_text(encoding='utf-8')
    page, n = re.subn(r'(<!-- guides:start -->).*?(\s*<!-- guides:end -->)',
                      lambda m: m.group(1) + guide_cards('guides/') + m.group(2), page, flags=re.S)
    if n:
        landing.write_text(page, encoding='utf-8')
    # Header and footer on the landing and support page come from here too.
    for p, up in ((landing, ''), (SITE / 'support' / 'index.html', '../'),
                  (SITE / 'privacypolicy' / 'index.html', '../'), (SITE / 'terms' / 'index.html', '../')):
        if not p.exists():
            continue
        t = p.read_text(encoding='utf-8')
        t = re.sub(r'<header class="site-header">.*?</header>', lambda m: header(up), t, count=1, flags=re.S)
        t = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: footer(up), t, count=1, flags=re.S)
        p.write_text(t, encoding='utf-8')
    print(f'{built} guides built, landing grid {"updated" if n else "NOT FOUND"}')


if __name__ == '__main__':
    main()
