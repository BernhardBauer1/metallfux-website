# -*- coding: utf-8 -*-
"""Baut die statische METALLFUX-Website nach ../site.

  python build.py          Vorschau: Entwurfs-Hinweise und Entwurfs-Referenzen sichtbar
  python build.py --live   Livegang: ohne Entwurfs-Hinweise, nur fertige Referenzen,
                           bricht ab, solange Impressum-Angaben fehlen
"""
import json, os, re, shutil, sys, html
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import SITE, PRICE_NOTE, V, LEISTUNGEN, FOLDER, PAGES, AREAS, REFS as ALL_REFS, IMPRESSUM, GEBIET, FAQ

LIVE = '--live' in sys.argv
REFS = [r for r in ALL_REFS if not (LIVE and r.get('entwurf'))]

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, '..', 'site')
MAN = json.load(open(os.path.join(BASE, 'images.json'), encoding='utf-8'))
E = html.escape

def imgs(key):
    return MAN.get(key, [])

def svg(d, size=22, sw=2):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"></path></svg>'
ARROW = svg('M5 12h14M13 6l6 6-6 6')
CHEV = '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5"></path></svg>'
CHECK = svg('m5 12.5 4.5 4.5L19 7.5', 22, 2.4)
PHONE = svg('M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2', 16)
WA = svg('M3 21l1.6-4.7A8.5 8.5 0 1 1 8 19.6L3 21Z', 16)
MAIL = svg('M3 6h18v12H3zM3 7l9 6 9-6', 16)
BURGER = svg('M4 7h16M4 12h16M4 17h16', 24)

def page_by_slug(s):
    return next(p for p in PAGES if p['slug'] == s)

def area_pages(a):
    return [p for p in PAGES if p['area'] == a]

def head(title, desc, canonical):
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://{SITE['domain']}/{canonical}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0F0F10">
<link rel="icon" href="img/favicon.png" type="image/png">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
'''

def header(active=None, area=None, home=False):
    def drop(a):
        ad = AREAS[a]
        items = ''.join(f'<a href="{p["slug"]}.html"><span>{E(p["nav"])}</span><small>{E(p["short"])}</small></a>' for p in area_pages(a))
        act = ' active' if area == a else ''
        return f'''<li class="nav-item{act}"><button class="nav-link" type="button" aria-expanded="false" aria-controls="dd-{a}">{ad['nav']}{CHEV}</button>
<div class="dropdown" id="dd-{a}">{items}<a class="all" href="{ad['slug']}.html"><span>Alles für den {ad['nav']} {ARROW}</span></a></div></li>'''
    cur = lambda k: ' aria-current="page"' if active == k else ''
    logo_w = '<img class="logo-w" src="img/logo-weiss.png" alt="" width="221" height="22">' if home else ''
    return f'''<header class="site-header{' is-home' if home else ''}">
<div class="scroll-progress" aria-hidden="true"></div>
<div class="wrap header-inner">
<a class="logo" href="index.html" aria-label="METALLFUX Startseite"><img class="logo-d" src="img/logo-dunkel.png" alt="METALLFUX" width="221" height="22">{logo_w}</a>
<nav class="nav" id="nav" aria-label="Hauptmenü">
<ul>
{drop('innen')}
{drop('aussen')}
<li class="nav-item"><a class="nav-link" href="referenzen.html"{cur('referenzen')}>Referenzen</a></li>
<li class="nav-item"><a class="nav-link" href="ueber-uns.html"{cur('ueber-uns')}>Über uns</a></li>
<li class="nav-item"><a class="nav-link" href="termin.html"{cur('termin')}>Termin</a></li>
</ul>
<div class="mobile-cta"><a class="btn btn-orange btn-lg" href="anfrage.html">Anfrage stellen</a><a class="btn btn-ghost" href="tel:{SITE['tel_link']}">{PHONE} {SITE['tel']}</a></div>
</nav>
<div class="header-cta">
<a class="header-phone" href="tel:{SITE['tel_link']}">{PHONE}{SITE['tel']}</a>
<a class="btn btn-orange" href="anfrage.html">Anfrage stellen</a>
<button class="burger" type="button" aria-label="Menü öffnen" aria-expanded="false" aria-controls="nav">{BURGER}</button>
</div>
</div>
</header>
<main id="inhalt">
'''

def footer():
    col = lambda a: ''.join(f'<a href="{p["slug"]}.html">{E(p["nav"])}</a>' for p in area_pages(a))
    return f'''</main>
<footer class="site-footer">
<div class="wrap">
<div class="footer-grid">
<div>
<a class="footer-logo" href="index.html" aria-label="METALLFUX Startseite"><img src="img/logo-weiss.png" alt="METALLFUX" width="201" height="20"></a>
<address>{SITE['firma']}<br>{SITE['strasse']}<br>{SITE['ort']}</address>
<div><a href="tel:{SITE['tel_link']}">{SITE['tel']}</a><br><a href="mailto:{SITE['mail']}">{SITE['mail']}</a></div>
<div class="hint" style="color:var(--on-dark-muted)">Einsatzgebiet: {SITE['gebiet']}</div>
{meister_siegel()}
</div>
<div><h4><a href="innenbereich.html" style="padding:0;color:inherit">Innenbereich</a></h4>{col('innen')}</div>
<div><h4><a href="aussenbereich.html" style="padding:0;color:inherit">Außenbereich</a></h4>{col('aussen')}</div>
<div><h4><a href="weitere-produkte.html" style="padding:0;color:inherit">Weitere Produkte</a></h4>{col('weitere')}</div>
<div><h4>Unternehmen</h4><a href="referenzen.html">Referenzen</a><a href="ueber-uns.html">Über uns</a><a href="anfrage.html">Anfrage</a><a href="termin.html">Beratungstermin</a></div>
</div>
<div class="footer-bottom">
<div>© {SITE['firma']} · Metall · Glas · Holz</div>
<nav aria-label="Rechtliches"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></nav>
</div>
</div>
</footer>
<nav class="m-bar" aria-label="Schnellkontakt">
<a href="tel:{SITE['tel_link']}">{PHONE}<span>Anrufen</span></a>
<a href="https://wa.me/{SITE['whatsapp']}?text={quote('Guten Tag, ich interessiere mich für ein Geländer / eine Treppe.')}" target="_blank" rel="noopener">{WA}<span>WhatsApp</span></a>
<a class="m-bar-main" href="anfrage.html">{MAIL}<span>Anfrage</span></a>
</nav>
<script src="js/main.js" defer></script>
</body>
</html>
'''

def cta_band():
    return f'''<section class="inquiry" aria-labelledby="cta-h">
<div class="wrap section" style="align-items:center">
<div class="inquiry-text" data-reveal>
<h2 id="cta-h">Kostenvoranschlag in zwei Minuten anfragen.</h2>
<p style="font-size:18px">Schicken Sie uns ein Foto der Einbausituation und grobe Maße. Sie bekommen einen unverbindlichen Kostenvoranschlag.</p>
</div>
<div class="btns" data-reveal><a class="btn btn-dark btn-lg" href="anfrage.html">Anfrage stellen</a><a class="btn btn-ghost btn-lg" href="tel:{SITE['tel_link']}">{SITE['tel']}</a></div>
</div>
</section>
'''

def crumbs(items):
    lis = ''.join(f'<li><a href="{h}">{E(t)}</a></li>' if h else f'<li aria-current="page">{E(t)}</li>' for t, h in items)
    return f'<nav class="crumbs wrap" aria-label="Brotkrümelnavigation"><ol>{lis}</ol></nav>'

def variant_card(key):
    v = V[key]
    lis = ''.join(f'<li>{E(x)}</li>' for x in v['li'])
    price = f'<div class="price">{v["price"]}<span>{v.get("pnote", "exkl. MwSt., gerade Ausführung ab 10 lfm")}</span></div>' if v['price'] else '<div class="price none">Preis auf Anfrage</div>'
    return f'<article class="variant" data-reveal><div class="tagline">{E(v["tag"])}</div><h3>{E(v["t"])}</h3><p>{E(v["p"])}</p><ul>{lis}</ul>{price}</article>'

def min_price(keys):
    ps = []
    for k in keys:
        p = V[k]['price']
        if p:
            ps.append(int(re.search(r'€ (\d+)', p).group(1)))
    return min(ps) if ps else None

def gallery_imgs(key):
    p = next((q for q in PAGES if q['slug'] == key), None)
    if p and p.get('materials'):
        lists = [mat_imgs(p, m) for _, m in mat_list(p)]
        mixed, i = [], 0
        while len(mixed) < 15 and any(i < len(l) for l in lists):
            for l in lists:
                if i < len(l) and len(mixed) < 15:
                    mixed.append(l[i])
            i += 1
        return mixed
    return imgs(key)[:15]

def gallery(key, group):
    out = []
    for im in gallery_imgs(key):
        out.append(f'<a href="{im["file"]}" data-lightbox="{group}"><img src="{im["thumb"]}" alt="{E(im["alt"])}" width="{im["tw"]}" height="{im["th"]}" loading="lazy" decoding="async"></a>')
    return '<div class="gallery">' + ''.join(out) + '</div>'

def write(name, s):
    if LIVE:
        s = re.sub(r'<p class="todo">.*?</p>\n?', '', s, flags=re.S)
        # Galerie ohne Fotos (z. B. Hochbeete) samt Sprungmarke weglassen
        leer = re.compile(r'<section class="section" id="galerie"[^>]*><div class="wrap">\n<div class="section-head">(?:(?!</section>).)*?</div>\n</div></section>\n', re.S)
        if leer.search(s) and 'class="gallery"' not in s:
            s = leer.sub('', s)
            s = re.sub(r'<a class="btn [^"]*" href="#galerie">[^<]*</a>', '', s)
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(s)


SEL = json.load(open(os.path.join(BASE, 'selection.json'), encoding='utf-8'))
MATERIALS = [
    ('stahl', dict(key='stahl', label='Stahl', folders={1, 21, 30}, keys=['design', 'stahl-pulver', 'stahl-verzinkt', 'sonder', 'franz-stahl'],
        text='Pulverbeschichtet in jeder RAL-Farbe oder feuerverzinkt – vom klassischen Füllstab bis zur freien Verstrebung.',
        text_innen='Vollverschweißt und pulverbeschichtet in jeder RAL-Farbe – vom klassischen Füllstab bis zur freien Verstrebung.')),
    ('edelstahl', dict(key='edelstahl', label='Edelstahl', folders={3, 5, 6, 7, 14, 16, 17, 18}, keys=['stab', 'reling', 'seil', 'franz-edelstahl'],
        text='Stab, Reling oder Seil – vollverschweißt, pflegeleicht und zeitlos.')),
    ('glas', dict(key='glas', label='Glas', folders={0, 2, 4, 13, 15}, keys=['nurglas', 'nurglas-treppe', 'edelstahl-glas', 'franz-glas'],
        text='Nurglas ohne Steher oder Edelstahl mit Glasfüllung – viel Licht und freie Sicht.')),
]

def mtext(p, m):
    return m.get('text_innen', m['text']) if p['area'] == 'innen' else m['text']

def mat_imgs(p, m):
    sel = SEL.get(p['slug'], [])
    out = []
    lst = imgs(p['slug'])
    if lst and 'mat' in lst[0]:
        # neue Fotos aus Website-Fotos: Material steht am Bild
        return [im for im in lst if im['mat'] == m['key']][:15]
    for im, e in zip(lst, sel):
        mat = e[2] if len(e) > 2 else None
        if (mat == m['key']) if mat else (e[0] in m['folders']):
            out.append(im)
    return out[:15]

def mat_variants(p, m):
    return [k for k in p['variants'] if k in m['keys']]

def mat_list(p):
    return [(mk, m) for mk, m in MATERIALS if mat_variants(p, m)]

def material_cards(p, current=None):
    out = ''
    for mk, m in mat_list(p):
        ims = mat_imgs(p, m)
        im = ims[0] if ims else None
        mp = min_price(mat_variants(p, m))
        img = f'<img src="{im["thumb"]}" alt="{E(im["alt"])}" loading="lazy">' if im else f'<div class="placeholder" style="height:260px;border-radius:0">Foto · {m["label"]}</div>'
        cur = ' aria-current="page" style="outline:3px solid var(--orange);outline-offset:-3px"' if mk == current else ''
        out += f'<a class="ov-card" href="{p["slug"]}-{mk}.html" data-reveal{cur}>{img}<div class="body"><div class="eyebrow">{E(p["nav"])}</div><h3>{m["label"]}</h3><p>{E(mtext(p, m))}</p><div class="from">{"ab € " + str(mp) + ",– / lfm" if mp else "Preis auf Anfrage"} {ARROW}</div></div></a>'
    return f'<div class="overview-grid mat-grid">{out}</div>'

def material_page(p, mk, m):
    a = AREAS[p['area']]
    ims = mat_imgs(p, m)
    hero = ims[0] if ims else None
    keys = mat_variants(p, m)
    mp = min_price(keys)
    chip = f'<div class="price-chip"><small>ab</small><b>€ {mp},–</b><small>/ lfm exkl. MwSt.</small></div>' if mp else ''
    hero_img = f'<div class="page-hero-media"><img src="{hero["file"]}" alt="{E(hero["alt"])}" width="{hero["w"]}" height="{hero["h"]}" fetchpriority="high"></div>' if hero else f'<div class="page-hero-media"><div class="placeholder" style="height:clamp(300px,38vw,520px)">Foto · {E(p["title"])} {m["label"]}</div></div>'
    gal = ''.join(f'<a href="{im["file"]}" data-lightbox="{p["slug"]}-{mk}"><img src="{im["thumb"]}" alt="{E(im["alt"])}" width="{im["tw"]}" height="{im["th"]}" loading="lazy" decoding="async"></a>' for im in ims)
    title = f"{p['title']} aus {m['label']}"
    s = head(f"{title} – METALLFUX Wien", f"{title}: {mtext(p, m)}"[:155], f"{p['slug']}-{mk}.html") + header(area=p['area'])
    s += crumbs([('Startseite', 'index.html'), (a['nav'], f"{a['slug']}.html"), (p['nav'], f"{p['slug']}.html"), (m['label'], None)])
    s += f'''<section class="page-hero"><div class="wrap">
<div class="page-hero-text">
<div class="eyebrow">{a['nav']} · {E(p['nav'])}</div>
<h1>{E(title)}</h1>
<p class="lead">{E(mtext(p, m))}</p>
{chip}
<div class="btns"><a class="btn btn-orange btn-lg" href="anfrage.html">Kostenvoranschlag anfragen</a><a class="btn btn-ghost btn-lg" href="#galerie">Bilder ansehen</a></div>
</div>
{hero_img}
</div></section>
<section class="section" id="galerie" aria-labelledby="gal-h"><div class="wrap">
<div class="section-head"><div class="eyebrow">Galerie</div><h2 class="h2" id="gal-h">{E(p['nav'])} aus {m['label']}</h2><p class="lead">Ein Bild antippen, um es groß zu sehen.</p></div>
{('<div class="gallery">' + gal + '</div>') if gal else '<p class="todo">Entwurf: Fotos für diese Seite folgen.</p>'}
<div class="wunsch" role="note"><div class="wunsch-text"><h3>Kein Foto der Wunschausführung dabei?</h3><p>Senden Sie uns eine Skizze oder ein Bild Ihrer Vorstellungen und wir prüfen die Machbarkeit. Oder sehen Sie sich die beiden anderen Varianten an.</p></div>
<div class="btns"><a class="btn btn-orange" href="anfrage.html">Skizze oder Bild senden</a>{''.join(f'<a class="btn btn-ghost" href="{p["slug"]}-{ok}.html">{om["label"]} ansehen</a>' for ok, om in mat_list(p) if ok != mk)}</div></div>
</div></section>
'''
    s += cta_band() + footer()
    write(f"{p['slug']}-{mk}.html", s)

# ---------- Produktseite ----------
def product_page(p):
    a = AREAS[p['area']]
    ims = imgs(p['slug'])
    hero = ims[0] if ims else None
    mp = min_price(p['variants'])
    unit = p.get('unit', '/ lfm exkl. MwSt.')
    chip = f'<div class="price-chip"><small>ab</small><b>€ {mp},–</b><small>{unit}</small></div>' if mp else ''
    others = [q for q in area_pages(p['area']) if q['slug'] != p['slug']]
    other_links = ''.join(f'<a class="row-link" href="{q["slug"]}.html"><span><b>{E(q["nav"])}</b><small>{E(q["short"])}</small></span>{ARROW}</a>' for q in others)
    cs, ct = p['cross']
    hero_img = f'<div class="page-hero-media"><img src="{hero["file"]}" alt="{E(hero["alt"])}" width="{hero["w"]}" height="{hero["h"]}" fetchpriority="high"></div>' if hero else f'<div class="page-hero-media"><div class="placeholder" style="height:clamp(300px,38vw,520px)">Foto · {E(p["title"])}</div></div>'
    extlink = f'<a class="btn btn-dark btn-lg" href="{p["link"][0]}" target="_blank" rel="noopener">{E(p["link"][1])}</a>' if p.get('link') else ''
    has_price = any(V[k]['price'] for k in p['variants'])
    s = head(f"{p['title']} – METALLFUX Wien", p['lead'][:155], f"{p['slug']}.html") + header(area=p['area'])
    s += crumbs([('Startseite', 'index.html'), (a['nav'], f"{a['slug']}.html"), (p['nav'], None)])
    s += f'''<section class="page-hero"><div class="wrap">
<div class="page-hero-text">
<div class="eyebrow">{a['nav']}</div>
<h1>{E(p['h1'])}</h1>
<p class="lead">{E(p['lead'])}</p>
{chip}
<div class="btns"><a class="btn btn-orange btn-lg" href="anfrage.html">Kostenvoranschlag anfragen</a>{extlink or '<a class="btn btn-ghost btn-lg" href="#galerie">Bilder ansehen</a>'}</div>
</div>
{hero_img}
</div></section>
<section class="section band-white" aria-labelledby="ausf-h"><div class="wrap">
{('<div class="section-head"><div class="eyebrow">Nach Material</div><h2 class="h2" id="ausf-h">Stahl, Edelstahl oder Glas?</h2><p class="lead">Wählen Sie das Material – auf jeder Seite finden Sie die passenden Ausführungen, Preise und Bilder.</p></div>' + material_cards(p)) if p.get('materials') else ''}
{'' if p.get('materials') else '<div class="section-head"><div class="eyebrow">Ausführungen</div><h2 class="h2" id="ausf-h">Welche Ausführung passt?</h2></div>'}
{'' if p.get('materials') else '<div class="variants">' + ''.join(variant_card(k) for k in p['variants']) + '</div>'}
{f'<p class="price-note">{E(p["extra_note"])}</p>' if p.get('extra_note') else ''}
</div></section>
<section class="section" id="galerie" aria-labelledby="gal-h"><div class="wrap">
<div class="section-head"><div class="eyebrow">Galerie</div><h2 class="h2" id="gal-h">Aus unseren Projekten</h2><p class="lead">Ein Bild antippen, um es groß zu sehen.</p></div>
{gallery(p['slug'], p['slug']) if imgs(p['slug']) else '<p class="todo">Entwurf: Fotos für diese Seite folgen.</p>'}
</div></section>
<section class="section band-white" aria-labelledby="leist-h"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:48px 64px">
<div style="flex:1 1 420px;min-width:0">
<div class="section-head" style="margin-bottom:28px"><div class="eyebrow">Gut zu wissen</div><h2 class="h2" id="leist-h">Darauf können Sie sich verlassen.</h2></div>
<ul class="facts">{''.join(f'<li>{CHECK}<span>{E(x)}</span></li>' for x in (LEISTUNGEN if p['area'] != 'weitere' else ['Planung und Beratung aus einer Hand', 'Gefertigt nach Maß', 'Lieferung und Montage', 'Ein Ansprechpartner für alles']))}</ul>
</div>
<div style="flex:1 1 360px;min-width:0">
<div class="eyebrow" style="margin-bottom:12px">Mehr im {a['nav']}</div>
<div class="rows">{other_links}</div>
</div>
</div></section>
<section class="wrap"><div class="cross"><p>{E(ct)}</p><a class="btn btn-dark" href="{cs}.html">{E(page_by_slug(cs)['title'])} {ARROW}</a></div></section>
'''
    s += cta_band() + footer()
    write(f"{p['slug']}.html", s)

# ---------- Bereichsseite ----------
def area_page(key):
    a = AREAS[key]
    cards = ''
    for p in area_pages(key):
        ims = imgs(p['slug'])
        im = ims[0] if ims else None
        mp = min_price(p['variants'])
        img = f'<img src="{im["thumb"]}" alt="{E(im["alt"])}" loading="lazy">' if im else f'<div class="placeholder" style="height:260px;border-radius:0">Foto · {E(p["nav"])}</div>'
        u = ",–" + (" / lfm" if p.get('unit') is None else "")
        cards += f'<a class="ov-card" href="{p["slug"]}.html" data-reveal>{img}<div class="body"><h3>{E(p["nav"])}</h3><p>{E(p["card"])}</p><div class="from">{"ab € " + str(mp) + u if mp else "Preis auf Anfrage"}</div></div></a>'
    other = 'aussen' if key == 'innen' else 'innen'
    s = head(f"{a['title']} – Geländer, Handläufe, Treppen | METALLFUX", a['lead'][:155], f"{a['slug']}.html") + header(area=key)
    s += crumbs([('Startseite', 'index.html'), (a['nav'], None)])
    s += f'''<section class="page-hero"><div class="wrap"><div class="page-hero-text" style="flex-basis:100%">
<div class="eyebrow">{a['nav']}</div><h1>{E(a['h1'])}</h1><p class="lead">{E(a['lead'])}</p></div></div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="overview-grid">{cards}</div>
{'' if key == 'weitere' else f'<p class="price-note">{PRICE_NOTE}</p>'}</div></section>
{'' if key == 'weitere' else f'<section class="wrap"><div class="cross"><p>Sie suchen etwas für den {AREAS[other]["nav"]}?</p><a class="btn btn-dark" href="{AREAS[other]["slug"]}.html">{AREAS[other]["nav"]} {ARROW}</a></div></section>'}
'''
    s += cta_band() + footer()
    write(f"{a['slug']}.html", s)

MEISTER = os.path.join(BASE, '..', 'assets', 'meistersiegel.png')
def meister_siegel():
    if os.path.exists(MEISTER):
        return '<div class="meister"><img src="img/meistersiegel.png" alt="Meisterbetrieb" width="88" height="88" loading="lazy"></div>'
    if LIVE:
        return ''
    return '<div class="meister"><div class="meister-ph">Meister&shy;siegel</div><p class="todo">Platzhalter: offizielle Grafik des Meistersiegels fehlt noch.</p></div>'

# ---------- Startseite: Produkt-Kacheln ----------
PRODUKT_GRUPPEN = [
    ('Geländer', '', ('aussen-balkon-terrasse', 1),
     [('innen-treppengelaender', 'Treppen- und Galeriegeländer Innen'), ('aussen-balkon-terrasse', 'Balkon- und Terrassengeländer'),
      ('aussen-treppengelaender', 'Treppengeländer Außen'), ('aussen-franzoesische-balkone', 'Französische Balkone')]),
    ('Handläufe', '', ('innen-handlaeufe', 0),
     [('innen-handlaeufe', 'Handläufe Innen'), ('aussen-handlaeufe', 'Handläufe Außen')]),
    ('Treppen', '', ('aussentreppen', 0),
     [('innentreppen', 'Innentreppen'), ('aussentreppen', 'Außentreppen'), ('seetreppen', 'Seetreppen')]),
]
def produkt_kacheln():
    tiles = ''
    for title, text, (key, i), links in PRODUKT_GRUPPEN:
        ims = imgs(key); im = ims[min(i, len(ims) - 1)] if ims else None
        img = f'<img src="{im["thumb"]}" alt="" width="{im["tw"]}" height="{im["th"]}" loading="lazy" decoding="async">' if im else '<div class="placeholder"></div>'
        rows = ''.join(f'<a href="{slug}.html"><span>{E(lab)}</span>{ARROW}</a>' for slug, lab in links)
        tiles += f'''<article class="pg-card" data-reveal><a class="pg-img" href="{links[0][0]}.html" tabindex="-1" aria-hidden="true">{img}</a>
<div class="pg-body"><h3>{E(title)}</h3>{f'<p>{E(text)}</p>' if text else ''}<nav class="pg-links" aria-label="{E(title)}">{rows}</nav></div></article>'''
    return f'<div class="pg-grid">{tiles}</div>'

# ---------- Startseite ----------
def index_page():
    hero = imgs('hero')
    slides = ''
    captions = ['Stahlgeländer an einer Innentreppe', 'Balkongeländer an einer Wohnhausanlage']
    for i, im in enumerate(hero):
        cap = captions[i] if i < len(captions) else ''
        slides += f'<div class="hero-slide{" is-active" if i == 0 else ""}" data-caption="{E(cap)}"><img src="{im["file"]}" alt="" {"fetchpriority=\"high\"" if i == 0 else "loading=\"lazy\""}></div>'
    dots = ''.join(f'<button class="hero-dot" type="button" aria-label="Bild {i+1} zeigen" aria-current="{"true" if i == 0 else "false"}"><span></span></button>' for i in range(len(hero)))
    teaser = ''.join(ref_tile(r, 'ref-tile') for r in REFS[:3])
    s = head('METALLFUX – Geländer und Treppen nach Maß in Wien', 'Geländer, Handläufe und Treppen aus Metall, Glas und Holz – geplant, gefertigt und montiert in Wien, Niederösterreich und im Burgenland.', '') + header(home=True)
    if not LIVE:
        s += '<div class="ruhig-hinweis"><div class="wrap"><b>Vergleich</b><a href="startseite-ruhig.html">Variante „Mehr Ruhe“ ansehen</a></div></div>\n'
    s += f'''<section class="hero" aria-label="Einstieg">
<div class="hero-slides">{slides}</div>
<div class="wrap hero-inner">
<div class="hero-tag">Stahl · Edelstahl · Glas</div>
<h1>Geländer und Treppen nach Maß.</h1>
<p>Geplant, gefertigt und montiert – in Wien, Niederösterreich und im Burgenland.</p>
<div class="btns"><a class="btn btn-orange btn-lg" href="anfrage.html">Kostenvoranschlag anfragen</a><a class="btn btn-ghost btn-lg" href="termin.html">Beratungstermin vor Ort</a></div>
</div>
<div class="hero-controls"><div class="wrap">{dots}<span class="hero-caption" aria-live="polite">{captions[0]}</span></div></div>
</section>
<section class="promise on-dark" aria-label="Unser Versprechen"><div class="wrap">
<div><strong>Ein Ansprechpartner</strong><span>Von der Beratung bis zur Montage</span></div>
<div><strong>Metall, Glas, Holz</strong><span>Kombiniert aus einer Hand</span></div>
<div><strong>Exakte Pläne</strong><span>Zur Freigabe vor der Fertigung</span></div>
<div><strong>Wien · NÖ · Bgld.</strong><span>Unser Einsatzgebiet</span></div>
</div></section>
<section class="section" aria-label="Produkte"><div class="wrap">
{produkt_kacheln()}
</div></section>
{projekt_band()}
<section class="section band-white" aria-labelledby="ablauf-h"><div class="wrap">
<div class="section-head"><div class="eyebrow">Ablauf</div><h2 class="h2" id="ablauf-h">Vom Foto zum fertigen Geländer.</h2></div>
<ol class="steps">
<li data-reveal><div class="num">01</div><h3>Foto schicken</h3><p>Ein Foto der Einbausituation und grobe Längenmaße reichen für den Anfang.</p></li>
<li data-reveal><div class="num">02</div><h3>Beratung und Aufmaß</h3><p>Wir beraten telefonisch oder vor Ort, nehmen Maß und erstellen einen unverbindlichen Kostenvoranschlag.</p></li>
<li data-reveal><div class="num">03</div><h3>Planung und Fertigung</h3><p>Sie erhalten exakte Pläne zur Freigabe. Danach wird nach Maß gefertigt, in der Regel in rund 6 bis 8 Wochen.</p></li>
<li data-reveal><div class="num">04</div><h3>Montage</h3><p>Wir montieren bei Ihnen und stimmen uns auf der Baustelle mit den anderen Gewerken ab.</p></li>
</ol>
</div></section>
<section class="plan3d on-dark" aria-labelledby="plan-h"><div class="wrap">
<h2 class="sr-only" id="plan-h">Planung und 3D-Visualisierung: Bis ins Detail geplant</h2>
<div class="plan3d-text" aria-hidden="true"><div class="eyebrow">Planung &amp; 3D-Visualisierung</div><p class="h2">Bis ins Detail geplant.</p><p>Bevor gefertigt wird, sehen Sie Ihr Projekt als Ausführungsplan mit allen Maßen und als 3D-Modell. So können Sie Form, Material und Details in Ruhe prüfen.</p><ul><li>Aufmaß vor Ort</li><li>Ausführungsplan mit Bemaßung</li><li>3D-Ansicht vor der Fertigung</li></ul></div>
<figure class="plan3d-fig" data-reveal><a href="img/planung-3d.jpg" data-lightbox="planung"><picture><source media="(max-width:700px)" srcset="img/planung-3d-mobil.webp" type="image/webp"><source media="(max-width:700px)" srcset="img/planung-3d-mobil.jpg"><source srcset="img/planung-3d.webp" type="image/webp"><img src="img/planung-3d.jpg" width="1600" height="1200" loading="lazy" alt="Bis ins Detail geplant: Bevor gefertigt wird, sehen Sie Ihr Projekt als Ausführungsplan mit allen Maßen und als 3D-Modell – Aufmaß vor Ort, Ausführungsplan mit Bemaßung, 3D-Ansicht vor der Fertigung. Beispiel: Seetreppe aus feuerverzinktem Stahl."></picture></a></figure>
<div class="plan3d-cta" data-reveal><p>Ausführungsplan und 3D-Ansicht bekommen Sie zur Freigabe – erst danach wird gefertigt.</p><a class="btn btn-orange" href="anfrage.html">Projekt anfragen</a></div>
</div></section>
<section class="section" aria-labelledby="proj-h"><div class="wrap">
<div class="section-head row"><div style="display:flex;flex-direction:column;gap:12px;max-width:720px"><div class="eyebrow">Aus unseren Projekten</div><h2 class="h2" id="proj-h">Gebaut in Wien und Umgebung.</h2></div><a class="link-u" href="referenzen.html">Alle Referenzen ansehen</a></div>
<div class="ref-grid ref-grid-3">{teaser}</div>
</div></section>
<section class="on-dark" aria-labelledby="about-h"><div class="wrap section about">
<div class="about-media" data-reveal><div class="placeholder">Foto · Bernhard Bauer</div></div>
<div class="about-text" data-reveal>
<div class="eyebrow">Über uns</div>
<h2 class="h2" id="about-h">Ein Ansprechpartner. Von der Skizze bis zur Montage.</h2>
<p class="lead">Bei METALLFUX sprechen Sie nicht mit einer Hotline, sondern mit dem, der Ihr Geländer plant und die Montage begleitet. Kurze Wege, klare Absprachen.</p>
<div class="person"><b>{SITE['gf']}</b><span>Geschäftsführer</span></div>
<address>{SITE['firma']} · {SITE['strasse']}, {SITE['ort']}</address>
<div class="btns"><a class="btn btn-orange" href="ueber-uns.html">Mehr über uns</a><a class="btn btn-ghost" href="tel:{SITE['tel_link']}">{SITE['tel']}</a></div>
</div>
</div></section>
'''
    extra = ''
    for p in area_pages('weitere'):
        ims = imgs(p['slug']); im = ims[0] if ims else None
        img = f'<img src="{im["thumb"]}" alt="{E(im["alt"])}" loading="lazy">' if im else f'<div class="placeholder" style="height:220px;border-radius:0">Foto · {E(p["nav"])}</div>'
        extra += f'<a class="ov-card" href="{p["slug"]}.html" data-reveal>{img}<div class="body"><h3>{E(p["nav"])}</h3><p>{E(p["card"])}</p></div></a>'
    s += f'''<section class="section band-white" aria-labelledby="weitere-h"><div class="wrap">
<div class="section-head row"><div style="display:flex;flex-direction:column;gap:12px;max-width:720px"><div class="eyebrow">Weitere Produkte</div><h2 class="h2" id="weitere-h">Auch das fertigen wir für Sie.</h2></div><a class="link-u" href="weitere-produkte.html">Alle weiteren Produkte</a></div>
<div class="overview-grid">{extra}</div>
</div></section>
'''
    s += gebiet_section() + cta_band() + footer()
    write('index.html', s)

# ---------- Startseite, ruhigere Variante (nur Vorschau zum Vergleichen) ----------
def index_ruhig():
    hero = imgs('hero')
    slides = ''.join(f'<div class="hero-slide{" is-active" if i == 0 else ""}"><img src="{im["file"]}" alt="" {"fetchpriority=\"high\"" if i == 0 else "loading=\"lazy\""}></div>' for i, im in enumerate(hero))
    dots = ''.join(f'<button class="hero-dot" type="button" aria-label="Bild {i+1} zeigen" aria-current="{"true" if i == 0 else "false"}"><span></span></button>' for i in range(len(hero)))
    teaser = ''.join(ref_tile(r, 'ref-tile') for r in REFS[:3])
    weitere = ''.join(f'<a href="{p["slug"]}.html"><span>{E(p["nav"])}</span>{ARROW}</a>' for p in area_pages('weitere'))
    s = head('METALLFUX – Startseite (ruhige Variante)', 'Vorschau', 'startseite-ruhig.html').replace('<body>', '<body class="ruhig">') + header(home=True)
    s += f'''<div class="ruhig-hinweis"><div class="wrap"><b>Vorschau „Mehr Ruhe“</b><span>Zum Vergleich mit der jetzigen Startseite.</span><a href="index.html">Jetzige Startseite ansehen</a></div></div>
<section class="hero" aria-label="Einstieg">
<div class="hero-slides">{slides}</div>
<div class="wrap hero-inner">
<h1>Geländer und Treppen nach Maß.</h1>
<p>Aus Stahl, Edelstahl und Glas. Geplant, gefertigt und montiert in Wien, Niederösterreich und im Burgenland.</p>
<div class="btns"><a class="btn btn-orange btn-lg" href="anfrage.html">Kostenvoranschlag anfragen</a><a class="hero-link" href="termin.html">Oder Beratungstermin vor Ort vereinbaren {ARROW}</a></div>
</div>
<div class="hero-controls"><div class="wrap">{dots}</div></div>
</section>
<section class="section" aria-labelledby="prod-h"><div class="wrap">
<div class="section-head"><div class="eyebrow">Was wir fertigen</div><h2 class="h2" id="prod-h">Für innen und außen.</h2></div>
{produkt_kacheln()}
</div></section>
<section class="section band-white" aria-labelledby="ablauf-h"><div class="wrap">
<div class="section-head"><div class="eyebrow">Ablauf</div><h2 class="h2" id="ablauf-h">In vier Schritten zum Geländer.</h2></div>
<ol class="steps">
<li data-reveal><div class="num">01</div><h3>Foto schicken</h3><p>Ein Foto und grobe Maße reichen.</p></li>
<li data-reveal><div class="num">02</div><h3>Beratung und Aufmaß</h3><p>Telefonisch oder bei Ihnen vor Ort.</p></li>
<li data-reveal><div class="num">03</div><h3>Plan und Fertigung</h3><p>Pläne zur Freigabe, Fertigung in rund 6 bis 8 Wochen.</p></li>
<li data-reveal><div class="num">04</div><h3>Montage</h3><p>Sauber montiert, abgestimmt mit den anderen Gewerken.</p></li>
</ol>
</div></section>
<section class="section" aria-labelledby="proj-h"><div class="wrap">
<div class="section-head row"><div style="display:flex;flex-direction:column;gap:12px;max-width:720px"><div class="eyebrow">Referenzen</div><h2 class="h2" id="proj-h">Gebaut in Wien und Umgebung.</h2></div><a class="link-u" href="referenzen.html">Alle Referenzen ansehen</a></div>
<div class="ref-grid ref-grid-3">{teaser}</div>
</div></section>
<section class="on-dark" aria-labelledby="about-h"><div class="wrap section about">
<div class="about-media" data-reveal><div class="placeholder">Foto · Bernhard Bauer</div></div>
<div class="about-text" data-reveal>
<div class="eyebrow">Über uns</div>
<h2 class="h2" id="about-h">Ein Ansprechpartner von der Skizze bis zur Montage.</h2>
<p class="lead">Sie sprechen direkt mit dem, der Ihr Geländer plant und die Montage begleitet.</p>
<div class="btns"><a class="btn btn-orange" href="ueber-uns.html">Mehr über uns</a><a class="btn btn-ghost" href="tel:{SITE['tel_link']}">{SITE['tel']}</a></div>
</div>
</div></section>
<section class="section" aria-labelledby="gebiet-h"><div class="wrap ruhig-gebiet">
<div class="section-head"><div class="eyebrow">Einsatzgebiet</div><h2 class="h2" id="gebiet-h">Wien, Niederösterreich und Burgenland.</h2>
<p class="lead">Beratung, Aufmaß und Montage bei Ihnen vor Ort.</p>
<div class="ruhig-weitere"><b>Außerdem fertigen wir</b><nav aria-label="Weitere Produkte">{weitere}</nav></div></div>
{karte()}
</div></section>
'''
    s += cta_band() + footer()
    write('startseite-ruhig.html', s)

BAND = [
    [('innen-treppengelaender', 30), ('aussen-balkon-terrasse', 1), ('ueberdachungen', 0), ('aussen-treppengelaender', 8), ('innen-handlaeufe', 3),
     ('aussen-balkon-terrasse', 14), ('innen-treppengelaender', 0), ('duschverglasung', 1), ('aussen-treppengelaender', 20), ('aussen-balkon-terrasse', 21)],
    [('aussen-treppengelaender', 11), ('innen-treppengelaender', 16), ('aussen-balkon-terrasse', 10), ('aussen-handlaeufe', 2), ('innen-treppengelaender', 35),
     ('aussen-balkon-terrasse', 17), ('ueberdachungen', 4), ('aussen-treppengelaender', 4), ('innen-treppengelaender', 20), ('aussen-balkon-terrasse', 7)],
]
def projekt_band():
    rows = ''
    for d, row in zip((-1, 1), BAND):
        ims = ''.join(f'<img src="{im["thumb"]}" alt="" width="{im["tw"]}" height="{im["th"]}" loading="lazy" decoding="async">'
                      for im in (imgs(k)[i] for k, i in row if i < len(imgs(k))))
        rows += f'<div class="band-row" data-dir="{d}">{ims}</div>'
    return f'''<section class="photo-band on-dark" aria-labelledby="band-h"><div class="wrap">
<div class="section-head"><div class="eyebrow">Einblicke</div><h2 class="h2" id="band-h">Ein Blick auf unsere Arbeit.</h2></div></div>
<div class="band-rows" aria-hidden="true">{rows}</div>
<div class="wrap"><a class="link-u" href="referenzen.html">Zu den Referenzen</a></div>
</section>
'''

KARTE = json.load(open(os.path.join(BASE, 'karte.json'), encoding='utf-8'))
def karte():
    ctx = ''.join(f'<path class="ctx" d="{KARTE[n]}"/>' for n in ('Oberösterreich', 'Steiermark'))
    lands = ''.join(f'<path class="land" style="--i:{i}" d="{KARTE[n]}"/>' for i, n in ((1, 'Niederösterreich'), (2, 'Burgenland'), (0, 'Wien')))
    labels = ''.join(f'<text class="lbl" style="--i:{i}" x="{KARTE["_c_" + n][0] + dx}" y="{KARTE["_c_" + n][1] + dy}" text-anchor="middle">{lab}</text>'
                     for i, n, lab, dx, dy in ((1, 'Niederösterreich', 'Niederösterreich', -50, 60), (2, 'Burgenland', 'Burgenland', 0, 0), (0, 'Wien', 'Wien', 6, -34)))
    return f'''<figure class="karte" data-reveal><svg viewBox="{KARTE['_vb']}" role="img" aria-label="Karte: Einsatzgebiet Wien, Niederösterreich und Burgenland">{ctx}{lands}{labels}</svg>
<figcaption>Kartengrundlage: Statistik Austria, CC BY 4.0</figcaption></figure>'''

def gebiet_section():
    cols = ''.join(f'''<div class="area-col" data-reveal><h3>{E(land)}</h3><p class="area-sub">{E(sub)}</p><p class="area-list">{' · '.join(E(o) for o in orte)}</p></div>''' for land, sub, orte in GEBIET)
    return f'''<section class="section" aria-labelledby="gebiet-h"><div class="wrap">
<div class="section-head"><div class="eyebrow">Einsatzgebiet</div><h2 class="h2" id="gebiet-h">Wir montieren in Wien, Niederösterreich und im Burgenland.</h2>
<p class="lead">Beratung, Aufmaß und Montage bei Ihnen vor Ort.</p></div>
<div class="gebiet">{karte()}<div class="area-grid">{cols}</div></div>
</div></section>
'''

def faq_section():
    items = ''.join(f'<details class="faq-item"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}, ensure_ascii=False)
    return f'''<section class="section band-white" aria-labelledby="faq-h"><div class="wrap faq-wrap">
<div class="section-head"><div class="eyebrow">Häufige Fragen</div><h2 class="h2" id="faq-h">Gut zu wissen, bevor Sie anfragen.</h2></div>
<p class="todo">Entwurf: Antworten bitte fachlich prüfen (Lieferzeit, OIB-Höhen, V2A/V4A, Verzinkung).</p>
<div class="faq">{items}</div>
<script type="application/ld+json">{ld}</script>
</div></section>
'''

# ---------- Referenzen ----------
def ref_cover(r):
    ims = imgs('ref-' + r['id'])
    return ims[min(r.get('cover', 0), len(ims) - 1)] if ims else None

def ref_tile(r, cls='ref-tile'):
    im = ref_cover(r)
    img = f'<img src="{im["thumb"]}" alt="{E(im["alt"])}" width="{im["tw"]}" height="{im["th"]}" loading="lazy" decoding="async">' if im else '<div class="placeholder"></div>'
    return f'''<a class="{cls}" href="referenz-{r['id']}.html" data-reveal><div class="rt-img">{img}</div>
<div class="rt-body"><span class="rt-ort">{E(r['ort'])}</span><h3>{E(r['title'])}</h3><p>{E(r['produkte'])}</p></div></a>'''

def ref_page():
    tiles = ''
    for r in REFS:
        im = ref_cover(r)
        img = f'<img src="{im["thumb"]}" alt="" width="{im["tw"]}" height="{im["th"]}" loading="lazy" decoding="async">' if im else ''
        tiles += f'<a class="mosaic-tile" href="referenz-{r["id"]}.html">{img}<span class="mosaic-cap"><b>{E(r["title"])}</b><small>{E(r["ort"])}</small></span></a>'

    s = head('Referenzen – METALLFUX Wien', 'Ausgewählte Projekte: Geländer, Handläufe und Treppen in Wien, Niederösterreich und darüber hinaus.', 'referenzen.html') + header('referenzen')
    s += crumbs([('Startseite', 'index.html'), ('Referenzen', None)])
    s += f'''<section class="page-hero"><div class="wrap"><div class="page-hero-text" style="flex-basis:100%">
<div class="eyebrow">Referenzen</div><h1>Gebaut in Wien und Umgebung.</h1>
<p class="lead">Eine Auswahl unserer Projekte, vom Einfamilienhaus bis zur Wohnhausanlage. Ein Projekt anklicken, um alle Fotos zu sehen.</p></div></div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="mosaic">{tiles}</div></div></section>
'''
    s += cta_band() + footer()
    write('referenzen.html', s)
    for i, r in enumerate(REFS):
        ref_detail(i, r)

def ref_detail(i, r):
    ims = imgs('ref-' + r['id'])
    cov = ref_cover(r)
    order = ([cov] if cov else []) + [im for im in ims if im is not cov]
    gal = ''.join(f'<a class="rd-item{" rd-wide" if n % 3 == 0 else ""}" href="{im["file"]}" data-lightbox="ref-{r["id"]}"><img src="{im["file"] if n == 0 else im["thumb"]}" alt="{E(im["alt"])}" width="{im["w"] if n == 0 else im["tw"]}" height="{im["h"] if n == 0 else im["th"]}" {"fetchpriority=\"high\"" if n == 0 else "loading=\"lazy\""} decoding="async"></a>' for n, im in enumerate(order))
    prev, nxt = REFS[i - 1], REFS[(i + 1) % len(REFS)]
    s = head(f"{r['title']} – Referenz | METALLFUX", f"{r['produkte']} – {r['title']}. {r['text']}"[:155], f"referenz-{r['id']}.html") + header('referenzen')
    s += crumbs([('Startseite', 'index.html'), ('Referenzen', 'referenzen.html'), (r['title'], None)])
    s += f'''<section class="section rd"><div class="wrap rd-layout">
<aside class="rd-side"><div class="rd-sticky">
<h1 class="rd-h1">{E(r['title'])}</h1>
<dl class="rd-info"><dt>Projekt</dt><dd>{E(r['text'])}</dd><dt>Leistung</dt><dd>{E(r['produkte'])}</dd><dt>Ort</dt><dd>{E(r['ort'])}</dd></dl>
<p class="todo">Entwurf: Text von Claude nach den Fotos formuliert – bitte prüfen und ergänzen.</p>
<a class="link-u" href="referenzen.html">Alle Referenzen</a>
</div></aside>
<div class="rd-main"><div class="rd-gallery">{gal}</div>
<nav class="rd-nav" aria-label="Weitere Projekte"><a href="referenz-{prev['id']}.html"><small>Vorheriges Projekt</small><span>{E(prev['title'])}</span></a>
<a class="rd-next" href="referenz-{nxt['id']}.html"><small>Nächstes Projekt</small><span>{E(nxt['title'])}</span></a></nav></div>
</div></section>
'''
    s += cta_band() + footer()
    write(f"referenz-{r['id']}.html", s)

# ---------- Über uns ----------
def about_page():
    reasons = [
        ('Beratung', 'Schicken Sie uns ein Foto Ihrer Einbausituation. Danach beraten wir Sie telefonisch oder vor Ort und bieten Ihnen das passende Produkt an.'),
        ('Qualität', 'Alle Geländer und Treppen sind werkseitig vollverschweißt. So können die Rohre nicht auffrieren.'),
        ('Planung', 'Sie erhalten exakte Pläne. Das erleichtert Ihnen die Vorbereitung der baulichen Maßnahmen.'),
        ('Koordinierung', 'Wir kommen auf Wunsch zur Baubesprechung und stimmen uns mit den anderen Gewerken ab.'),
        ('Flexibilität', 'Die Lieferzeit für maßgefertigte Elemente beträgt rund 6 bis 8 Wochen. Wenn es schneller gehen muss, kommen wir Ihnen entgegen.'),
        ('Designvielfalt', 'Vom modernen Glasgeländer bis zum klassischen, pulverbeschichteten Stahlgeländer: Für jede Einbausituation gibt es eine passende Lösung.'),
    ]
    values = [('Präzision', 'Sauber gearbeitete Details, vom Schweißpunkt bis zur Glasklemme.'),
              ('Robustheit', 'Material und Ausführung, die Jahrzehnte halten.'),
              ('Handwerk', 'Tradition trifft auf klare, moderne Form.'),
              ('Verlässlichkeit', 'Ein ruhiger, direkter Ton und Termine, die halten.')]
    s = head('Über uns – METALLFUX Wien', 'METALLFUX GmbH plant, liefert und montiert Geländer, Treppen und Handläufe aus Metall, Glas und Holz.', 'ueber-uns.html') + header('ueber-uns')
    s += crumbs([('Startseite', 'index.html'), ('Über uns', None)])
    s += f'''<section class="page-hero"><div class="wrap">
<div class="page-hero-text"><div class="eyebrow">Über uns</div><h1>Ein Ansprechpartner. Von der Skizze bis zur Montage.</h1>
<p class="lead">METALLFUX plant, liefert und montiert Geländer, Treppen und Handläufe aus Metall, Glas und Holz. Sie sprechen dabei immer mit derselben Person: mit dem, der Ihr Projekt plant und die Montage begleitet.</p>
<div class="person"><b>{SITE['gf']}</b><span style="color:var(--muted)">Geschäftsführer</span></div>
<div class="btns"><a class="btn btn-orange btn-lg" href="anfrage.html">Anfrage stellen</a><a class="btn btn-ghost btn-lg" href="tel:{SITE['tel_link']}">{SITE['tel']}</a></div></div>
<div class="page-hero-media"><div class="placeholder" style="height:clamp(300px,38vw,520px)">Foto · Bernhard Bauer</div></div>
</div></section>
<section class="section band-white" aria-labelledby="werte-h"><div class="wrap">
<div class="section-head"><div class="eyebrow">Wofür wir stehen</div><h2 class="h2" id="werte-h">Präzise gearbeitet, klar besprochen.</h2></div>
<div class="variants">{''.join(f'<article class="variant" data-reveal><h3>{t}</h3><p>{d}</p></article>' for t, d in values)}</div>
</div></section>
<section class="section" aria-labelledby="gruende-h"><div class="wrap">
<div class="section-head"><div class="eyebrow">Sechs Gründe</div><h2 class="h2" id="gruende-h">Warum Kundinnen und Kunden mit uns bauen.</h2></div>
<div class="variants">{''.join(f'<article class="variant" data-reveal><div class="tagline">{i+1:02d}</div><h3>{t}</h3><p>{d}</p></article>' for i, (t, d) in enumerate(reasons))}</div>
</div></section>
<section class="on-dark"><div class="wrap section" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<div style="flex:1 1 380px;min-width:0;display:flex;flex-direction:column;gap:16px"><div class="eyebrow">Einsatzgebiet</div><h2 class="h2">{SITE['gebiet']}.</h2>
<p class="lead">Von unserem Standort in Wien-Donaustadt sind wir rasch bei Ihnen – in ganz Wien, in Niederösterreich und im Burgenland.</p></div>
<div style="flex:1 1 300px;min-width:0;display:flex;flex-direction:column;gap:10px">
<address style="font-style:normal;color:var(--on-dark)">{SITE['firma']}<br>{SITE['strasse']}<br>{SITE['ort']}</address>
<div style="color:var(--on-dark-muted)">Telefonisch erreichbar {SITE['zeiten']}</div>
<div style="font-family:var(--font-head);font-size:24px;font-weight:800;user-select:all">{SITE['tel']}</div>
<div style="user-select:all">{SITE['mail']}</div></div>
</div></section>
'''
    s += cta_band() + footer()
    write('ueber-uns.html', s)

# ---------- Anfrage ----------
def inquiry_page():
    opts = ''.join(f'<option>{E(p["nav"])} ({AREAS[p["area"]]["nav"]})</option>' for p in PAGES)
    s = head('Anfrage und Kontakt – METALLFUX Wien', 'Unverbindlichen Kostenvoranschlag für Geländer, Handlauf oder Treppe anfragen. Fotos und Pläne einfach mitschicken.', 'anfrage.html') + header('anfrage')
    s += crumbs([('Startseite', 'index.html'), ('Anfrage', None)])
    s += f'''<section class="inquiry"><div class="wrap section">
<div class="inquiry-text">
<div class="eyebrow" style="color:var(--ink)">Anfrage und Kontakt</div>
<h1 style="font-size:clamp(34px,4.4vw,58px);font-weight:800;line-height:1.05">Kostenvoranschlag in zwei Minuten anfragen.</h1>
<p style="font-size:18px">Je mehr wir sehen, desto genauer wird der Preis. Am meisten hilft uns:</p>
<ul class="checks">
<li>{CHECK}Fotos der Einbausituation</li>
<li>{CHECK}Grobe Längenmaße oder ein Planausschnitt</li>
<li>{CHECK}Ein Bild oder Link Ihrer Wunschausführung</li>
</ul>
<div class="direct">
<div style="font-weight:600">Lieber gleich reden? {SITE['zeiten']}</div>
<a class="big" href="tel:{SITE['tel_link']}">{SITE['tel']}</a>
<a class="mail" href="mailto:{SITE['mail']}">{SITE['mail']}</a>
</div>
<p style="margin:0"><a class="link-u" href="termin.html" style="text-decoration-color:var(--ink)">Lieber gleich einen Termin vor Ort? Freie Zeiten ansehen</a></p>
<address style="font-style:normal">{SITE['firma']}<br>{SITE['strasse']}, {SITE['ort']}</address>
</div>
<form class="form" id="anfrage-form" action="anfrage.php" method="post" enctype="multipart/form-data" novalidate>
<fieldset><legend>Wo wird montiert?</legend>
<div class="choice"><label><input type="radio" name="bereich" value="Innenbereich" checked> Innenbereich</label><label><input type="radio" name="bereich" value="Außenbereich"> Außenbereich</label></div>
</fieldset>
<div class="field"><label class="lbl" for="f-produkt">Was brauchen Sie?</label>
<select id="f-produkt" name="produkt">{opts}<option>Etwas anderes</option></select></div>
<div class="fields">
<div class="field" style="flex:1 1 120px"><label class="lbl" for="f-plz">PLZ</label><input id="f-plz" name="plz" type="text" inputmode="numeric" autocomplete="postal-code" required></div>
<div class="field" style="flex:2 1 200px"><label class="lbl" for="f-ort">Ort des Vorhabens</label><input id="f-ort" name="ort" type="text" autocomplete="address-level2" required></div>
</div>
<div class="hint" style="margin-top:-6px">Wir montieren in {SITE['gebiet']}.</div>
<div class="fields">
<div class="field"><label class="lbl" for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label class="lbl" for="f-tel">Telefon</label><input id="f-tel" name="telefon" type="tel" autocomplete="tel"></div>
</div>
<div class="field"><label class="lbl" for="f-mail">E-Mail</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label class="lbl" for="f-fotos">Fotos und Pläne</label>
<div class="drop"><input id="f-fotos" name="dateien[]" type="file" multiple accept="image/jpeg,image/png,image/heic,application/pdf"><div class="hint">Bis zu 8 Dateien · JPG, PNG, HEIC oder PDF · zusammen max. 20 MB</div></div></div>
<div class="field"><label class="lbl" for="f-text">Nachricht <span style="font-weight:400;color:var(--muted)">(optional)</span></label><textarea id="f-text" name="nachricht" rows="4"></textarea></div>
<div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" type="text" tabindex="-1" autocomplete="off"></div>
<label class="consent"><input type="checkbox" name="rueckruf" value="ja"> <span>Bitte rufen Sie mich zurück.</span></label>
<label class="consent"><input type="checkbox" name="datenschutz" value="ja" required> <span>Ich stimme zu, dass meine Angaben zur Beantwortung der Anfrage verarbeitet werden. Mehr dazu in der <a href="datenschutz.html">Datenschutzerklärung</a>.</span></label>
<button class="btn btn-dark btn-lg" type="submit">Anfrage absenden</button>
<p class="form-status" role="status" hidden></p>
</form>
</div></section>
'''
    s += footer()
    write('anfrage.html', s)

def termin_page():
    opts = ''.join(f'<option>{E(p["nav"])} ({AREAS[p["area"]]["nav"]})</option>' for p in PAGES)
    s = head('Beratungstermin vor Ort – METALLFUX Wien', 'Freie Termine für eine Beratung vor Ort in Wien, Niederösterreich und im Burgenland ansehen und unverbindlich anfragen.', 'termin.html') + header('termin')
    s += crumbs([('Startseite', 'index.html'), ('Beratungstermin', None)])
    s += f'''<section class="section" style="padding-top:24px"><div class="wrap termin-wrap">
<div class="termin-intro">
<div class="eyebrow">Beratung vor Ort</div>
<h1 class="h2" style="font-size:clamp(34px,4.4vw,54px)">Wunschtermin wählen.</h1>
<p class="lead">Wir kommen zu Ihnen, sehen uns die Einbausituation an, beraten Sie und nehmen Maß. Wählen Sie einen freien Termin. Sie bekommen innerhalb von 12 Stunden eine Bestätigung von uns.</p>
<ul class="checks">
<li>{CHECK}Rund 60 Minuten vor Ort</li>
<li>{CHECK}Mo–Fr zwischen 9 und 17 Uhr</li>
<li>{CHECK}In Wien, Niederösterreich und im Burgenland</li>
<li>{CHECK}Unverbindlich, erst nach unserer Bestätigung fix</li>
</ul>
<p class="hint">Kein passender Termin dabei? Rufen Sie uns an unter <a href="tel:{SITE['tel_link']}">{SITE['tel']}</a> oder schicken Sie eine <a href="anfrage.html">Anfrage</a>.</p>
</div>
<div class="termin-app" id="termin-app" data-api="termine.php">
<p class="termin-demo" hidden>Vorschau: Die Zeiten hier sind Beispiele. Auf der fertigen Website kommen sie live aus Ihrem Kalender.</p>
<div class="termin-step"><div class="termin-label"><span>1</span> Tag wählen</div>
<div class="termin-days" role="listbox" aria-label="Verfügbare Tage"><p class="hint">Freie Termine werden geladen …</p></div></div>
<div class="termin-step" hidden><div class="termin-label"><span>2</span> Uhrzeit wählen</div>
<div class="termin-slots" role="listbox" aria-label="Freie Uhrzeiten"></div></div>
<form class="form termin-form" id="termin-form" action="termine.php" method="post" novalidate hidden>
<div class="termin-label"><span>3</span> Ihre Angaben</div>
<div class="termin-wahl" aria-live="polite"></div>
<input type="hidden" name="termin" value="">
<div class="fields">
<div class="field"><label class="lbl" for="t-name">Name</label><input id="t-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label class="lbl" for="t-tel">Telefon</label><input id="t-tel" name="telefon" type="tel" autocomplete="tel" required></div>
</div>
<div class="field"><label class="lbl" for="t-mail">E-Mail</label><input id="t-mail" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label class="lbl" for="t-adr">Straße und Hausnummer</label><input id="t-adr" name="adresse" type="text" autocomplete="street-address"></div>
<div class="fields">
<div class="field" style="flex:1 1 120px"><label class="lbl" for="t-plz">PLZ</label><input id="t-plz" name="plz" type="text" inputmode="numeric" autocomplete="postal-code" required></div>
<div class="field" style="flex:2 1 200px"><label class="lbl" for="t-ort">Ort</label><input id="t-ort" name="ort" type="text" autocomplete="address-level2" required></div>
</div>
<div class="field"><label class="lbl" for="t-produkt">Worum geht es?</label><select id="t-produkt" name="produkt">{opts}<option>Etwas anderes</option></select></div>
<div class="field"><label class="lbl" for="t-text">Nachricht <span style="font-weight:400;color:var(--muted)">(optional)</span></label><textarea id="t-text" name="nachricht" rows="3"></textarea></div>
<div class="hp" aria-hidden="true"><label for="t-web">Website</label><input id="t-web" name="website" type="text" tabindex="-1" autocomplete="off"></div>
<label class="consent"><input type="checkbox" name="datenschutz" value="ja" required> <span>Ich stimme zu, dass meine Angaben zur Vereinbarung des Termins verarbeitet werden. Mehr dazu in der <a href="datenschutz.html">Datenschutzerklärung</a>.</span></label>
<button class="btn btn-orange btn-lg" type="submit">Termin unverbindlich anfragen</button>
<p class="form-status" role="status" hidden></p>
</form>
</div>
</div></section>
'''
    s += footer()
    write('termin.html', s)

# ---------- Rechtstexte (Vorlagen) ----------
def imp_f(k):
    v = IMPRESSUM.get(k, '')
    return E(v) if v else '<mark>[bitte ergänzen]</mark>'

def legal_pages():
    imp = f'''<h1 class="h2">Impressum</h1>
<p class="todo">Entwurf: Bitte die markierten Angaben in content.py (IMPRESSUM) ergänzen und vor dem Livegang prüfen lassen.</p>
<p><b>{SITE['firma']}</b><br>{SITE['strasse']}<br>{SITE['ort']}<br>Österreich</p>
<p>Telefon: {SITE['tel']}<br>E-Mail: {SITE['mail']}</p>
<h2>Unternehmensangaben</h2>
<p>Unternehmensgegenstand: Planung, Handel und Montage von Geländern, Treppen und Handläufen<br>
Geschäftsführer: {SITE['gf']}<br>
Firmenbuchnummer: {imp_f('fn')}<br>Firmenbuchgericht: {imp_f('fb_gericht')}<br>UID-Nummer: {imp_f('uid')}<br>
Mitglied der Wirtschaftskammer Wien, Fachgruppe {imp_f('fachgruppe')}<br>Gewerbe: {imp_f('gewerbe')}, verliehen in Österreich<br>
Gewerbebehörde: {imp_f('behoerde')}<br>Anwendbare Rechtsvorschriften: Gewerbeordnung, abrufbar unter www.ris.bka.gv.at</p>
<h2>Haftung für Inhalte</h2>
<p>Die Inhalte dieser Website wurden sorgfältig erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität übernehmen wir keine Gewähr. Preisangaben sind Preisbeispiele und kein Angebot im rechtlichen Sinn.</p>
<h2>Bildnachweis</h2><p>Alle Fotos: {SITE['firma']}</p>'''
    ds = f'''<h1 class="h2">Datenschutzerklärung</h1>
<p class="todo">Entwurf: Diese Vorlage deckt Kontaktformular und Server-Logfiles ab. Bitte vor dem Livegang rechtlich prüfen lassen.</p>
<h2>Verantwortlicher</h2><p>{SITE['firma']}, {SITE['strasse']}, {SITE['ort']}, {SITE['mail']}</p>
<h2>Anfrage, Terminanfrage und E-Mail</h2><p>Wenn Sie uns über ein Formular oder per E-Mail kontaktieren, verarbeiten wir Ihre Angaben (Name, Kontaktdaten, Ort des Vorhabens, Nachricht und hochgeladene Dateien), um Ihre Anfrage zu beantworten und einen Kostenvoranschlag zu erstellen (Art. 6 Abs. 1 lit. b DSGVO). Die Daten werden gelöscht, sobald sie dafür nicht mehr nötig sind und keine gesetzlichen Aufbewahrungspflichten bestehen.</p>
<h2>Terminkalender</h2><p>Die angezeigten freien Zeiten ermittelt unser Server aus unserem eigenen Kalender. Beim Aufruf der Terminseite werden keine Daten an Kalenderanbieter oder andere Dritte übermittelt. Ihre Terminanfrage (Wunschtermin, Name, Kontaktdaten, Adresse und Nachricht) erhalten wir per E-Mail und verwenden sie nur, um den Termin mit Ihnen zu vereinbaren (Art. 6 Abs. 1 lit. b DSGVO).</p>
<h2>Server-Logfiles</h2><p>Unser Hosting-Anbieter [ALL-INKL.COM – Neue Medien Münnich, Deutschland] speichert beim Aufruf der Website technisch notwendige Daten (z. B. IP-Adresse, Zeitpunkt, aufgerufene Seite), um den Betrieb und die Sicherheit zu gewährleisten (Art. 6 Abs. 1 lit. f DSGVO).</p>
<h2>Schriftarten</h2><p>Die verwendeten Schriftarten sind auf unserem Server gespeichert. Beim Aufruf der Website werden dafür keine Daten an Dritte übermittelt.</p>
<h2>Cookies und Tracking</h2><p>Diese Website setzt keine Cookies und verwendet keine Analyse- oder Werbedienste.</p>
<h2>Ihre Rechte</h2><p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit und Widerspruch. Beschwerden können Sie bei der Österreichischen Datenschutzbehörde einbringen (www.dsb.gv.at).</p>'''
    for name, title, body in [('impressum.html', 'Impressum', imp), ('datenschutz.html', 'Datenschutz', ds)]:
        s = head(f'{title} – METALLFUX', f'{title} der {SITE["firma"]}', name) + header()
        s += crumbs([('Startseite', 'index.html'), (title, None)])
        s += f'<section class="section" style="padding-top:32px"><div class="wrap legal">{body}</div></section>' + footer()
        write(name, s)

def main():
    if LIVE:
        fehlt = [k for k, v in IMPRESSUM.items() if not v]
        if fehlt:
            sys.exit('Live-Bau abgebrochen, im Impressum fehlt noch: ' + ', '.join(fehlt) + ' (content.py, IMPRESSUM)')
    if os.path.isdir(OUT):
        for n in os.listdir(OUT):
            p = os.path.join(OUT, n)
            if n == 'img':
                continue
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(OUT, exist_ok=True)
    shutil.copytree(os.path.join(BASE, 'static', 'css'), os.path.join(OUT, 'css'))
    shutil.copytree(os.path.join(BASE, 'static', 'js'), os.path.join(OUT, 'js'))
    shutil.copytree(os.path.join(BASE, 'static', 'fonts'), os.path.join(OUT, 'fonts'))
    for n in ('anfrage.php', 'termine.php', 'termine-config.php'):
        shutil.copy(os.path.join(BASE, 'static', n), OUT)
    shutil.copy(os.path.join(BASE, 'static', '.htaccess'), OUT)
    os.makedirs(os.path.join(OUT, 'img', 'thumb'), exist_ok=True)
    for n in ('planung-3d.jpg', 'planung-3d.webp', 'planung-3d-mobil.jpg', 'planung-3d-mobil.webp'):
        shutil.copy(os.path.join(BASE, '..', 'assets', n), os.path.join(OUT, 'img', n))
    if os.path.exists(MEISTER):
        shutil.copy(MEISTER, os.path.join(OUT, 'img', 'meistersiegel.png'))
    shutil.copy(os.path.join(BASE, '..', 'assets', 'planung-3d-thumb.jpg'), os.path.join(OUT, 'img', 'thumb', 'planung-3d.jpg'))
    index_page()
    if not LIVE: index_ruhig()
    for k in AREAS: area_page(k)
    for p in PAGES:
        product_page(p)
        if p.get('materials'):
            for mk, m in mat_list(p): material_page(p, mk, m)
    ref_page(); about_page(); inquiry_page(); termin_page(); legal_pages()
    print('ok', 'LIVE' if LIVE else 'Vorschau', len(REFS), 'Referenzen')

if __name__ == '__main__':
    main()
