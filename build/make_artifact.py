import os, re, shutil, sys
S=sys.argv[1]; src=os.path.join(S,'site'); dst=os.path.join(S,'site-artifact')
if os.path.isdir(dst): shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns('anfrage.php','.htaccess'))
p=os.path.join(dst,'index.html'); s=open(p,encoding='utf-8').read()
headm=re.search(r'<head>(.*?)</head>', s, re.S).group(1)
headm=re.sub(r'<meta charset[^>]*>\s*|<meta name="viewport"[^>]*>\s*','',headm)
headm=re.sub(r'<title>.*?</title>','<title>METALLFUX Website</title>',headm)
body=re.search(r'<body>(.*)</body>', s, re.S).group(1)
open(p,'w',encoding='utf-8').write(headm.strip()+'\n'+body.strip()+'\n')
files=[]
for root,_,fs in os.walk(dst):
    for f in fs:
        rel=os.path.relpath(os.path.join(root,f),dst)
        if rel!='index.html': files.append(rel)
print(len(files))
import json; json.dump(sorted(files), open(os.path.join(S,'artifact-files.json'),'w'))
# Vorschau: nur eine Bildgröße (900 px) verwenden, um unter 512 Dateien zu bleiben; Titelbilder bleiben groß
import re as _re
for _f in os.listdir(dst):
    if _f.endswith('.html'):
        _p = os.path.join(dst, _f); _s = open(_p, encoding='utf-8').read()
        _s = _re.sub(r'(?<!thumb/)img/((?!hero-)[a-z0-9-]+-\d\d\.jpg)', r'img/thumb/\1', _s)
        open(_p, 'w', encoding='utf-8').write(_s)
