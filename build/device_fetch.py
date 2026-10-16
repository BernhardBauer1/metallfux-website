import os, json, sys
from PIL import Image, ImageOps
W = os.path.expanduser('~/mnt/Downloads/metallfux-website-arbeit')
ROOT = os.path.expanduser('~/mnt/Präsentation')
SEL = json.load(open(os.path.join(W, 'selection.json'), encoding='utf-8'))
OUT = os.path.join(W, 'originals'); os.makedirs(OUT, exist_ok=True)
idx = {}
for f in os.listdir(os.path.join(W, 'sheets')):
    if f.startswith('index_') and f.endswith('.tsv'):
        for line in open(os.path.join(W, 'sheets', f), encoding='utf-8'):
            fi, n, d, name, _ = line.rstrip('\n').split('\t')
            idx[(int(fi), int(n))] = os.path.join(ROOT, d, name)
done = 0
for key, items in SEL.items():
    if key.startswith('_'): continue
    for i, (fi, n) in enumerate(items):
        dst = os.path.join(OUT, f'{key}-{i:02d}.jpg')
        if os.path.exists(dst): continue
        src = idx.get((fi, n))
        if not src: print('FEHLT', key, fi, n); continue
        im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
        im.thumbnail((1800, 1800), Image.LANCZOS)
        im.save(dst, quality=84, optimize=True)
        done += 1
print('fertig', done, len(os.listdir(OUT)))
