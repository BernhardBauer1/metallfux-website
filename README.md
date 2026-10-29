# METALLFUX Website

Statische Website für www.metallfux-wien.at, erzeugt mit Python.

## Aufbau

- `build/content.py` – alle Texte und Seiten (Produkte, Referenzen, FAQ, Impressum)
- `build/build.py` – Vorlagen und Seitenaufbau
- `build/static/` – CSS, JavaScript, Schriften, PHP (Anfrageformular, Terminkalender)
- `build/images.json` – welche Fotos auf welcher Seite stehen
- `site/img/` – die fertig verkleinerten Fotos (1800 px und Vorschaubilder)
- `assets/` – Logos, Meistersiegel, 3D-Planungsbild

## Bauen

```
python3 build/build.py          # Vorschau, mit Entwurfs-Hinweisen
python3 build/build.py --live   # für den Upload, bricht ab solange das Impressum leer ist
```

Das Ergebnis liegt in `site/` und wird per KAS WebFTP zu All-Inkl hochgeladen.

## Nicht ins Repository

- Die geheime iCal-Adresse in `build/static/termine-config.php` erst am Server eintragen, nie hier committen.
- Originalfotos bleiben am Rechner (Documents\metallfux\Website-Fotos).
