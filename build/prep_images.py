# -*- coding: utf-8 -*-
"""Erzeugt site/img aus selection.json.
Quelle 1: Originale (FULL_DIR/<key>-<nn>.<ext>, vorher vom Computer geholt)
Quelle 2 (Notlösung): Ausschnitt aus dem Kontaktbogen (nur 220 px, unscharf)."""
import json, os, sys, glob
from PIL import Image, ImageOps, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import FOLDER, PAGES

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, '..', 'site', 'img')
FULL_DIR = os.path.join(BASE, '..', 'originals')
SHEETS = '/mnt/user-data/uploads/Downloads/metallfux-website-arbeit/sheets'
ASSETS = os.path.join(BASE, '..', 'assets')
SEL = json.load(open(os.path.join(BASE, 'selection.json'), encoding='utf-8'))
LABEL = {p['slug']: p['title'] for p in PAGES}
LABEL.update({'hero': 'METALLFUX', 'ref-michelhausen': 'Wohnhausanlage Michelhausen'})
T, COLS = 220, 6

def sheet_crop(f, n):
    s, k = divmod(n, 36)
    path = os.path.join(SHEETS, f'f{f:02d}_s{s}.jpg')
    if not os.path.exists(path):
        return None
    sh = Image.open(path).convert('RGB')
    x, y = (k % COLS) * T, (k // COLS) * (T + 4)
    cell = sh.crop((x, y + 27, x + T, y + T))
    bg = Image.new('RGB', cell.size, (255, 255, 255))
    bbox = ImageChops.difference(cell, bg).convert('L').point(lambda v: 255 if v > 18 else 0).getbbox()
    return cell.crop(bbox) if bbox else None

def save(im, key, i, alt, placeholder):
    os.makedirs(os.path.join(OUT, 'thumb'), exist_ok=True)
    name = f'{key}-{i:02d}.jpg'
    full = im.copy(); full.thumbnail((1800, 1800), Image.LANCZOS)
    full.save(os.path.join(OUT, name), quality=80, optimize=True, progressive=True)
    th = im.copy(); th.thumbnail((900, 900), Image.LANCZOS)
    th.save(os.path.join(OUT, 'thumb', name), quality=76, optimize=True, progressive=True)
    return dict(file=f'img/{name}', thumb=f'img/thumb/{name}', w=full.width, h=full.height, tw=th.width, th=th.height, alt=alt, placeholder=placeholder)

def main():
    os.makedirs(OUT, exist_ok=True)
    man, missing = {}, []
    for key, items in SEL.items():
        if key.startswith('_'):
            continue
        man[key] = []
        for i, e in enumerate(items):
            f, n = e[0], e[1]
            alt = f"{LABEL.get(key, key)} – {FOLDER.get(f, 'Projektfoto')}"
            cand = glob.glob(os.path.join(FULL_DIR, f'{key}-{i:02d}.*'))
            if cand:
                im = ImageOps.exif_transpose(Image.open(cand[0])).convert('RGB'); ph = False
            else:
                im = sheet_crop(f, n); ph = True
                if im is None:
                    missing.append((key, f, n)); continue
            man[key].append(save(im, key, i, alt, ph))
    # Logos und Favicon
    for src, dst, h in [('logo-dunkel.png', 'logo-dunkel.png', 44), ('logo-weiss.png', 'logo-weiss.png', 40)]:
        im = Image.open(os.path.join(ASSETS, src)); w = round(im.width * h / im.height)
        im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, dst), optimize=True)
    lg = Image.open(os.path.join(ASSETS, 'logo-weiss.png'))
    a = lg.split()[3]; W = lg.width
    xpart = lg.crop((int(W * 0.885), 0, W, lg.height))
    bb = xpart.split()[3].getbbox(); xpart = xpart.crop(bb)
    fav = Image.new('RGBA', (64, 64), (15, 15, 16, 255))
    xp = xpart.copy(); xp.thumbnail((44, 44), Image.LANCZOS)
    orange = Image.new('RGBA', xp.size, (232, 138, 44, 255)); orange.putalpha(xp.split()[3])
    fav.alpha_composite(orange, ((64 - xp.width) // 2, (64 - xp.height) // 2))
    fav.save(os.path.join(OUT, 'favicon.png'))
    json.dump(man, open(os.path.join(BASE, 'images.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    n_ph = sum(1 for v in man.values() for x in v if x['placeholder'])
    print('Bilder:', sum(len(v) for v in man.values()), 'davon Notlösung:', n_ph, 'fehlend:', missing)

if __name__ == '__main__':
    main()
