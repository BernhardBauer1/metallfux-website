# -*- coding: utf-8 -*-
"""Übernimmt die verkleinerten Fotos aus Website-Fotos (Ordner Website-Fotos-web am Rechner).

  python import_fotos.py <ordner mit manifest.json und img/>

Kopiert img/ nach site/img und ersetzt die betroffenen Einträge in images.json.
Material: aus dem Dateinamen, sonst aus material.json."""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import PAGES

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1]
OUT = os.path.join(BASE, '..', 'site')
LABEL = {p['slug']: p['title'] for p in PAGES}
LABEL['hero'] = 'METALLFUX'
MAT = {'stahl': 'Stahlgeländer', 'edelstahl': 'Edelstahlgeländer', 'glas': 'Glasgeländer'}
OVR = {k: v.split() for k, v in json.load(open(os.path.join(BASE, 'material.json'), encoding='utf-8')).items() if not k.startswith('_')}

man = json.load(open(os.path.join(SRC, 'manifest.json'), encoding='utf-8'))
images = json.load(open(os.path.join(BASE, 'images.json'), encoding='utf-8'))
for key, lst in man.items():
    out = []
    for i, e in enumerate(lst):
        mat = e['mat'] or (OVR[key][i] if key in OVR else None)
        alt = f"{LABEL.get(key, key)} – {MAT[mat]}" if mat else LABEL.get(key, key)
        for f in (e['file'], e['thumb']):
            os.makedirs(os.path.dirname(os.path.join(OUT, f)), exist_ok=True)
            shutil.copy2(os.path.join(SRC, f), os.path.join(OUT, f))
        out.append(dict(file=e['file'], thumb=e['thumb'], w=e['w'], h=e['h'], tw=e['tw'], th=e['th'], alt=alt, placeholder=False, mat=mat, src=e['src']))
    images[key] = out
    print(key, len(out), {m: sum(1 for x in out if x['mat'] == m) for m in MAT})
json.dump(images, open(os.path.join(BASE, 'images.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
