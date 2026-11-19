#!/usr/bin/env python3
"""Mete el CSS y los guiones dentro del HTML de las páginas de la raíz.

Un <link rel="stylesheet"> bloquea el pintado y cuesta un viaje de ida y vuelta
entero antes de que se vea nada. Las páginas de la raíz pesan poco con el CSS
adentro, así que entran en el primer envío del servidor y la página pinta sin
esperar un segundo pedido.

Las fuentes de verdad siguen siendo styles.css, assets/fonts/fonts.css, los
guiones (projects.js, cometa.js) y projects.json. Después de tocar cualquiera
hay que correr esto.
"""
import html
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAGINAS = ('index.html', 'projects.html')
HOJAS = ('assets/fonts/fonts.css', 'styles.css')
MARCA_CSS = re.compile(r'(<style id="css-del-sitio">)(.*?)(</style>)', re.S)
# Cada página declara qué guiones quiere con <script id="js:archivo.js">.
# Van adentro del HTML por la misma razón que el CSS: un pedido aparte es un
# viaje de ida y vuelta más, y cuando projects.js armaba la grilla eso dejaba
# pintar la página vacía y después empujaba el pie (0,149 de CLS).
MARCA_JS = re.compile(r'(<script id="js:([A-Za-z0-9_.-]+)">)(.*?)(</script>)', re.S)


# Las tarjetas de Work se escriben en el HTML. Antes las armaba projects.js en
# el navegador y la grilla llegaba vacia: un buscador sin renderizado o un
# extractor de IA leia "Work" y ningun proyecto, ni un solo enlace a las
# landings. La fuente es projects.json.
MARCA_TARJETAS = re.compile(r'(<!-- tarjetas:.*?-->)(.*?)(\n *<!-- /tarjetas -->)', re.S)
DATOS = 'projects.json'


def e_attr(texto):
    return html.escape(texto, quote=True)


def lista_legible(nombres):
    return nombres[0] if len(nombres) == 1 else ', '.join(nombres[:-1]) + ' and ' + nombres[-1]


def medidas(ruta):
    """Ancho y alto de una imagen, para que el navegador reserve el lugar."""
    try:
        from PIL import Image
        with Image.open(RAIZ / ruta) as im:
            return im.size
    except Exception:
        return None


def tarjetas():
    """Las filas de la vitrina de Work: imagen grande con el brillo del color
    de la app, numero, rubro, descripcion, plataformas y enlace."""
    datos = json.loads((RAIZ / DATOS).read_text(encoding='utf-8'))
    plataformas = datos['platforms']
    e = html.escape
    piezas = []
    for i, p in enumerate(visibles(datos)):
        # Nada de enlaces falsos: la landing tiene que existir de verdad
        for campo in ('name', 'description', 'url'):
            if not p.get(campo):
                raise SystemExit(f'{DATOS}: a "{p.get("name", "?")}" le falta "{campo}"')
        destino = RAIZ / p['url'].lstrip('/')
        if p['url'].startswith(('#', 'http')) or not (destino / 'index.html' if p['url'].endswith('/') else destino).exists():
            raise SystemExit(f'{DATOS}: "{p["name"]}" apunta a {p["url"]}, que no es una pagina del sitio')

        fondo = p.get('background') or '#111119'
        imagen = ''
        if p.get('image'):
            webp = re.sub(r'\.(jpe?g|png)$', '.webp', p['image'], flags=re.I)
            fuente = (f'\n              <source type="image/webp" srcset="{e(webp)}">' if webp != p['image'] else '')
            carga = 'loading="eager" fetchpriority="high"' if i == 0 else 'loading="lazy"'
            tam = medidas(p['image'])
            dims = f' width="{tam[0]}" height="{tam[1]}"' if tam else ''
            imagen = (f'\n            <picture>{fuente}'
                      f'\n              <img src="{e(p["image"])}" alt="{e(p.get("alt") or p["name"])}"{dims}'
                      f' {carga} decoding="async">'
                      f'\n            </picture>')

        claves = p.get('platform') or []
        claves = [claves] if isinstance(claves, str) else claves
        insignias = ''.join(
            f'\n            <li>{plataformas[k]["svg"]}<span>{e(plataformas[k]["label"].replace(" app", ""))}</span></li>'
            for k in claves if k in plataformas)
        # Color de marca de la app (el de su landing): tine el brillo de su fila.
        color = e(p.get('accent') or '#b8ff00')
        # "soon": la landing ya existe pero la app todavia no salio. Va en Work
        # con su etiqueta, pero no cuenta en el total, el pie ni los datos estructurados.
        soon = '<span class="show-soon">Coming soon</span>' if p.get('soon') else ''
        piezas.append(f'''
      <article class="show" style="--acento: {color}; --fondo: {e(fondo)}" data-reveal>
        <a class="show-media" href="{e(p["url"])}" tabindex="-1" aria-hidden="true">
          <div class="show-frame">{imagen}
          </div>
        </a>
        <div class="show-info">
          <p class="show-meta"><span class="show-num">{i + 1:02d}</span><span class="show-tag">{e(p.get("tag", ""))}</span>{soon}</p>
          <h2 class="show-name"><a href="{e(p["url"])}">{e(p["name"])}</a></h2>
          <p class="show-desc">{e(p["description"])}</p>
          <ul class="show-plat" aria-label="Platforms">{insignias}
          </ul>
          <a class="show-cta" href="{e(p["url"])}">Explore {e(p["name"])}<span aria-hidden="true">→</span></a>
        </div>
      </article>''')
    nombres = [p['name'] for p in visibles(datos)]
    return ''.join(piezas), nombres


# Cinta de Work: los nombres de las apps pasando en letra grande. Va dos veces
# seguida para que el bucle de la animacion no tenga corte.
MARCA_CINTA = re.compile(r'(<!-- cinta:.*?-->)(.*?)(\n *<!-- /cinta -->)', re.S)
MARCA_CUANTAS = re.compile(r'(<!-- cuantas -->)(.*?)(<!-- /cuantas -->)', re.S)


def cinta():
    e = html.escape
    nombres = [p['name'] for p in visibles(datos())]
    una = ''.join(f'<span>{e(n)}</span><i aria-hidden="true">✦</i>' for n in nombres)
    return (f'\n      <div class="cinta-pista">'
            f'\n        <p class="cinta-tira">{una}</p>'
            f'\n        <p class="cinta-tira" aria-hidden="true">{una}</p>'
            f'\n      </div>')

# Datos estructurados de Work: la lista de apps, para que Google entienda la
# pagina como una coleccion y no como texto suelto.
MARCA_LD = re.compile(r'(<script type="application/ld\+json" id="ld-proyectos">)(.*?)(</script>)', re.S)


def ld_proyectos():
    lista = [{'@type': 'ListItem', 'position': i + 1, 'name': p['name'],
              'url': 'https://dezeo.lat/' + p['url'].lstrip('/')} for i, p in enumerate(publicadas())]
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Work | dezeo',
          'url': 'https://dezeo.lat/projects.html',
          'isPartOf': {'@type': 'WebSite', 'name': 'dezeo', 'url': 'https://dezeo.lat/'},
          'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(lista), 'itemListElement': lista}}
    return json.dumps(ld, ensure_ascii=False, indent=2)


# Pie de las paginas de la raiz: una fila con las apps.
# Le da a la home enlaces rastreables a cada app sin tocar la portada.
MARCA_PIE = re.compile(r'(<!-- apps-pie:.*?-->)(.*?)(\n *<!-- /apps-pie -->)', re.S)


def datos():
    return json.loads((RAIZ / DATOS).read_text(encoding='utf-8'))


def visibles(d):
    """Los proyectos que se muestran en Work, la cinta y el pie. "hidden":
    la landing sigue publicada (las tiendas enlazan su privacidad y soporte)
    pero no aparece en ninguna lista del sitio."""
    return [p for p in d['projects'] if not p.get('hidden')]


def publicadas():
    return [p for p in visibles(datos()) if not p.get('soon')]


def pie_apps(prefijo):
    e = html.escape
    enlaces = [f'<a href="{prefijo}{e(p["url"])}">{e(p["name"])}</a>' for p in publicadas()]
    return ('\n    <nav class="pie-apps" aria-label="Apps by dezeo">\n      '
            + '\n      '.join(enlaces) + '\n    </nav>')



def comprimir(css):
    """Quita comentarios y espacio sobrante. No es un minificador serio: solo
    hace lo que es seguro sin analizar el CSS."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s*\n\s*', '\n', css)
    css = re.sub(r'\n{2,}', '\n', css)
    return css.strip()


def main():
    css = comprimir('\n'.join((RAIZ / h).read_text(encoding='utf-8') for h in HOJAS))

    def guion(nombre):
        ruta = RAIZ / nombre
        if not ruta.exists():
            raise SystemExit(f'falta {nombre}, pedido por un <script id="js:{nombre}">')
        cuerpo = ruta.read_text(encoding='utf-8')
        if '</script' in cuerpo:
            raise SystemExit(f'{nombre} contiene "</script": no se puede insertar tal cual')
        return cuerpo

    for nombre in PAGINAS:
        p = RAIZ / nombre
        t = p.read_text(encoding='utf-8')
        if not MARCA_CSS.search(t):
            raise SystemExit(f'{nombre}: falta <style id="css-del-sitio"></style>')
        antes = len(t)
        # Una pagina en una subcarpeta necesitaria las fuentes un nivel arriba.
        prefijo = '../' * (len(pathlib.Path(nombre).parts) - 1)
        css_pagina = css.replace('url(assets/', f'url({prefijo}assets/')
        t = MARCA_CSS.sub(lambda m: m.group(1) + '\n' + css_pagina + '\n  ' + m.group(3), t, count=1)
        if MARCA_PIE.search(t):
            t = MARCA_PIE.sub(lambda m: m.group(1) + pie_apps(prefijo) + m.group(3), t, count=1)
        if MARCA_CINTA.search(t):
            t = MARCA_CINTA.sub(lambda m: m.group(1) + cinta() + m.group(3), t, count=1)
        if MARCA_CUANTAS.search(t):
            t = MARCA_CUANTAS.sub(lambda m: m.group(1) + str(len(publicadas())) + m.group(3), t, count=1)
        if MARCA_LD.search(t):
            t = MARCA_LD.sub(lambda m: m.group(1) + '\n' + ld_proyectos() + '\n  ' + m.group(3), t, count=1)
        if MARCA_TARJETAS.search(t):
            grilla, nombres = tarjetas()
            t = MARCA_TARJETAS.sub(lambda m: m.group(1) + grilla + m.group(3), t, count=1)
            # La descripcion se arma desde los mismos datos: si se agrega un
            # proyecto, no queda una meta description desactualizada.
            desc = e_attr(f'Apps and games by dezeo, a creative studio: {lista_legible(nombres)}.')
            for patron in (r'(<meta name="description" content=")[^"]*(">)',
                           r'(<meta property="og:description" content=")[^"]*(">)',
                           r'(<meta name="twitter:description" content=")[^"]*(">)'):
                t = re.sub(patron, lambda m: m.group(1) + desc + m.group(2), t, count=1)
            print(f'  {nombre}: {len(nombres)} tarjetas desde {DATOS}')
        metidos = []
        def poner(m):
            metidos.append(m.group(2))
            return m.group(1) + '\n' + guion(m.group(2)) + '  ' + m.group(4)
        t = MARCA_JS.sub(poner, t)
        p.write_text(t, encoding='utf-8')
        guiones = ' + '.join(metidos) if metidos else 'sin guiones'
        print(f'  {nombre}: {antes/1024:.1f} KB -> {len(t)/1024:.1f} KB  ({guiones})')
    print(f'  CSS: {len(css)/1024:.1f} KB desde {", ".join(HOJAS)}')


if __name__ == '__main__':
    main()
