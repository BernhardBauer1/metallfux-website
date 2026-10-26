# -*- coding: utf-8 -*-
"""Inhalte der METALLFUX-Website. Quelle: winnox.at (Texte, Preise), METALLFUX-Styleguide, Angaben von Bernhard."""

SITE = {
    'name': 'METALLFUX',
    'firma': 'METALLFUX GmbH',
    'strasse': 'Telephonweg 256',
    'ort': '1220 Wien',
    'tel': '0664 9917 1224',
    'tel_link': '+4366499171224',
    'mail': 'office@metallfux-wien.at',
    'domain': 'www.metallfux-wien.at',
    'gebiet': 'Wien, Niederösterreich und Burgenland',
    'zeiten': 'Mo–Fr, 08:00–18:00 Uhr',
    'gf': 'Bernhard Bauer',
    'whatsapp': '4366499171224',   # Nummer für wa.me-Links (ohne + und Leerzeichen)
}

# Einsatzgebiet (Startseite, Abschnitt „Wo wir montieren“)
GEBIET = [
    ('Wien', 'Alle 23 Bezirke', ['Innere Stadt', 'Leopoldstadt', 'Landstraße', 'Wieden', 'Margareten', 'Mariahilf', 'Neubau', 'Josefstadt',
        'Alsergrund', 'Favoriten', 'Simmering', 'Meidling', 'Hietzing', 'Penzing', 'Rudolfsheim-Fünfhaus', 'Ottakring', 'Hernals',
        'Währing', 'Döbling', 'Brigittenau', 'Floridsdorf', 'Donaustadt', 'Liesing']),
    ('Niederösterreich', 'Ganz Niederösterreich', ['Amstetten', 'Baden', 'Bruck an der Leitha', 'Gänserndorf', 'Gmünd', 'Hollabrunn', 'Horn',
        'Korneuburg', 'Krems', 'Lilienfeld', 'Melk', 'Mistelbach', 'Mödling', 'Neunkirchen', 'St. Pölten', 'Scheibbs', 'Tulln',
        'Waidhofen an der Thaya', 'Waidhofen an der Ybbs', 'Wiener Neustadt', 'Zwettl']),
    ('Burgenland', 'Ganzes Burgenland', ['Eisenstadt', 'Rust', 'Neusiedl am See', 'Mattersburg', 'Oberpullendorf', 'Oberwart', 'Güssing', 'Jennersdorf']),
]

# Häufige Fragen (Startseite). Antworten vor dem Livegang fachlich prüfen.
FAQ = [
    ('Was kostet ein Geländer?',
     'Das hängt von Material, Länge, Form und Montage ab. Als Richtwert je Laufmeter exkl. MwSt.: Stahl verzinkt ab € 320, '
     'Edelstahl-Stabgeländer ab € 330, Edelstahl-Glas ab € 380, Nurglas ab € 590 (gerade Ausführung ab 10 lfm). '
     'Den genauen Preis erhalten Sie mit dem unverbindlichen Kostenvoranschlag.'),
    ('Wie lange dauert es vom Auftrag bis zur Montage?',
     'Nach Ihrer Freigabe der Pläne wird gefertigt, in der Regel in rund 8 Wochen. Den Montagetermin stimmen wir mit Ihnen '
     'und den anderen Gewerken auf der Baustelle ab.'),
    ('Wie hoch muss ein Geländer sein?',
     'In Österreich gilt die OIB-Richtlinie 4. Absturzsicherungen müssen in der Regel mindestens 100 cm hoch sein, ab 12 m '
     'Absturzhöhe mindestens 110 cm. Öffnungen dürfen höchstens 12 cm breit sein, und das Geländer darf nicht zum Hochklettern '
     'einladen. Wir planen jedes Geländer danach.'),
    ('Verzinkt oder pulverbeschichtet – was ist besser?',
     'Feuerverzinken schützt Stahl vor Rost, die Pulverbeschichtung gibt ihm die Farbe. Innen reicht pulverbeschichteter Stahl. '
     'Außen empfehlen wir feuerverzinkt, auf Wunsch zusätzlich pulverbeschichtet in Ihrer RAL-Farbe.'),
    ('Welcher Edelstahl eignet sich für außen?',
     'Innen verwenden wir meist V2A. Für Balkone, Terrassen und besonders in der Nähe von Pool oder Streusalz empfehlen wir '
     'den widerstandsfähigeren V4A.'),
    ('Kommen Sie zur Beratung vor Ort?',
     'Ja, in Wien, Niederösterreich und im Burgenland. Für eine erste Einschätzung reichen ein Foto der Einbausituation und grobe '
     'Maße. Danach kommen wir zum Aufmaß zu Ihnen.'),
    ('Wie pflege ich Edelstahl und Glas?',
     'Mit Wasser und einem milden Reinigungsmittel. Bitte keine Scheuermittel und keine Stahlwolle verwenden, sie zerkratzen '
     'die Oberfläche und können Flugrost verursachen.'),
]

# Impressum (Pflichtangaben laut ECG/UGB/GewO). Leere Felder erscheinen in der Vorschau
# als „[bitte ergänzen]“; der Live-Bau (build.py --live) bricht ab, solange eines fehlt.
IMPRESSUM = {
    'fn': '',           # Firmenbuchnummer, z. B. 'FN 123456 a'
    'fb_gericht': '',   # z. B. 'Handelsgericht Wien'
    'uid': '',          # z. B. 'ATU12345678'
    'fachgruppe': '',   # WKO-Fachgruppe, z. B. 'Metalltechnik'
    'gewerbe': '',      # Gewerbewortlaut laut GISA
    'behoerde': '',     # z. B. 'Magistratisches Bezirksamt für den 22. Bezirk'
}

PRICE_NOTE = 'Alle Preise exkl. MwSt. Preisbeispiel für die Herstellung bei gerader Ausführung ab 10 lfm.'

# Ausführungen (Varianten) mit Preisen von winnox.at
V = {
    'nurglas': dict(t='Nurglasgeländer', tag='Das Elegante',
        p='Ganz ohne Steher. Teilvorgespanntes Verbundsicherheitsglas (VSG TVG) mit insgesamt 18 mm Stärke sorgt für hohe Stabilität.',
        li=['Edelstahl-Punkthalter oder Schiene', 'Schiene aufgesetzt oder seitlich montiert', 'Glas transparent, satiniert oder getönt'],
        price='ab € 590,– / lfm'),
    'nurglas-treppe': dict(t='Nurglasgeländer', tag='Das Elegante',
        p='Ganz ohne Steher. Teilvorgespanntes Verbundsicherheitsglas (VSG TVG) mit insgesamt 18 mm Stärke sorgt für hohe Stabilität.',
        li=['Edelstahl-Punkthalter oder Schiene', 'Passt besonders gut zur Kragarmtreppe', 'Steigende Ausführung an der Treppe +40 %'],
        price='ab € 590,– / lfm'),
    'edelstahl-glas': dict(t='Edelstahl-Glasgeländer', tag='Das Moderne',
        p='Edelstahlrohre mit einer Füllung aus Verbundsicherheitsglas (VSG). Kindersicher und mit vollverschweißtem Unterzug für zusätzliche Stabilität.',
        li=['Glas transparent, blickdicht oder farbig', 'Gehalten von Edelstahl-Glasklemmen', 'Rohre eckig oder rund'],
        price='ab € 380,– / lfm'),
    'stab': dict(t='Stabgeländer', tag='Der Klassiker',
        p='Senkrechte Stäbe, eingeschweißt zwischen zwei Durchzügen. Mit maximal 12 cm Stababstand kindersicher und normgerecht.',
        li=['Edelstahl, vollverschweißt', 'Rohre eckig oder rund', 'Ohne Steck- und Schraubverbindungen'],
        price='ab € 330,– / lfm'),
    'reling': dict(t='Relinggeländer', tag='Der Bestseller',
        p='Die Stäbe laufen waagrecht, parallel zum Handlauf. Das wirkt leicht und fließend.',
        li=['Edelstahl, vollverschweißt', 'Rohre eckig oder rund', 'Verschiedenste Befestigungsarten'],
        price='ab € 310,– / lfm'),
    'seil': dict(t='Seilgeländer', tag='Das Zarte',
        p='Ein 4 mm Edelstahlseil statt 16 mm Relingstäben. Die Seilspanner lassen sich auch nach Jahren ohne Werkzeug nachspannen.',
        li=['Hochwertige Edelstahl-Seilspanner', 'Sehr filigrane Optik', 'Rahmen vollverschweißt'],
        price='ab € 300,– / lfm'),
    'design': dict(t='Designgeländer aus Stahl', tag='Das Individuelle',
        p='Klassische Füllstäbe oder kreuz und quer eingeschweißte Verstrebungen. Vollverschweißt und kratzfest pulverbeschichtet.',
        li=['Jede RAL-Farbe möglich', 'Mit Holzhandlauf passend zum Boden', 'Ihre Wunschvorstellung prüfen wir gern'],
        price='ab € 390,– / lfm'),
    'stahl-pulver': dict(t='Stahlgeländer pulverbeschichtet', tag='Farbe nach Wahl',
        p='Stahlgeländer mit Flachstahl- oder Stabfüllung, pulverbeschichtet in der RAL-Farbe Ihrer Wahl – zum Beispiel Anthrazit.',
        li=['Flachstahl oder Stabfüllung', 'Jede RAL-Farbe möglich', 'Vollverschweißte Ausführung'],
        price='ab € 450,– / lfm'),
    'stahl-verzinkt': dict(t='Stahlgeländer verzinkt', tag='Robust und pflegeleicht',
        p='Feuerverzinkter Stahl für Terrassen, Stiegen und Balkone. Die Füllung wählen Sie, zum Beispiel Stäbe oder Lochblech.',
        li=['Feuerverzinkt', 'Füllung mit Stäben oder Lochblech', 'Vollverschweißte Ausführung'],
        price='ab € 320,– / lfm'),
    'sonder': dict(t='Sonderfüllungen', tag='Sichtschutz nach Wunsch',
        p='Holzlatten, Lochblech, Schichtstoffplatten oder Blech als Sichtschutz – auf einem Rahmen aus Edelstahl oder Stahl.',
        li=['Holz, Lochblech, Schichtstoff oder Blech', 'Farben nach Wahl', 'Auch für Abtrennungen und Windschutz'],
        price=None),
    'franz-edelstahl': dict(t='Französischer Balkon aus Edelstahl', tag='Stab, Reling oder Seil',
        p='Alle unsere Edelstahl-Geländer gibt es auch als französischen Balkon. Montiert wird wahlweise auf die Fassade oder in die Fensterlichte.',
        li=['Montage auf der Fassade oder in der Laibung', 'Stab-, Reling- oder Seilfüllung', 'Vollverschweißte Ausführung'],
        price='ab € 390,– / lfm'),
    'franz-stahl': dict(t='Französischer Balkon aus Stahl', tag='Pulverbeschichtet',
        p='Flachstahl oder Stäbe, pulverbeschichtet in der Farbe Ihrer Fenster – zum Beispiel Anthrazit. Montiert auf der Fassade oder in der Fensterlichte.',
        li=['Montage auf der Fassade oder in der Laibung', 'RAL-Farbe passend zu den Fenstern', 'Vollverschweißte Ausführung'],
        price=None),
    'franz-glas': dict(t='Französischer Balkon aus Glas', tag='Freie Sicht',
        p='Eine Glasscheibe als Absturzsicherung vor dem Fenster. Montiert wird wahlweise auf die Fassade oder in die Fensterlichte.',
        li=['Montage auf der Fassade oder in der Laibung', 'Glas transparent oder getönt', 'Mit oder ohne Handlauf'],
        price='ab € 450,– / lfm'),
    'handlauf-edelstahl': dict(t='Edelstahl-Handlauf', tag='Der Klassiker',
        p='Rund oder eckig, an der Wand oder am Geländer. Wie unsere Geländer komplett vollverschweißt.',
        li=['Rohre eckig oder rund', 'Wand- oder Geländerbefestigung', 'Auch in barrierefreier Ausführung'],
        price='ab € 119,– / lfm'),
    'handlauf-holz': dict(t='Holzhandlauf', tag='Warm in der Hand',
        p='In allen gängigen Holzarten, passend zu Stufen und Boden. Auf Wunsch mit Haltern aus Edelstahl oder schwarzem Stahl.',
        li=['Alle gängigen Holzarten', 'Halter Edelstahl oder Stahl schwarz', 'Kombinierbar mit LED'],
        price=None),
    'handlauf-stahl': dict(t='Stahl-Handlauf', tag='Klar und grafisch',
        p='Flachstahl oder Rohr, pulverbeschichtet – oft in Schwarz als bewusster Kontrast zur weißen Wand.',
        li=['Flachstahl oder Rohr', 'Pulverbeschichtet in RAL-Farbe', 'Auch als Rahmen um eine Holzauflage'],
        price=None),
    'handlauf-led': dict(t='Handlauf mit LED', tag='Licht auf jeder Stufe',
        p='Ein Handlauf mit integrierter LED-Beleuchtung macht die Treppe auch nachts sicher und setzt sie in Szene.',
        li=['LED-Band im Handlauf integriert', 'Holz, Edelstahl oder Stahl', 'Indirektes, blendfreies Licht'],
        price=None),
    'handlauf-aussen-stahl': dict(t='Stahl-Handlauf', tag='Pulverbeschichtet',
        p='Flachstahl oder Rohr, verzinkt und pulverbeschichtet. Unauffällig an der Wand oder als markanter Akzent.',
        li=['Wandhandlauf oder freistehend', 'RAL-Farbe nach Wahl', 'Vollverschweißte Ausführung'],
        price=None),
    'stahlwangen': dict(t='Stahlwangentreppe', tag='Gelaserte Wangen',
        p='Beschichtete Stahlwangen in Ihrer Wunschfarbe nach RAL – abgetreppt, durchgehend oder kombiniert. Dazu 4 bis 8 cm starke Trittstufen aus massivem Holz.',
        li=['Wangen in RAL-Farbe', 'Massivholzstufen in allen heimischen Holzarten', 'Mit allen Geländermodellen kombinierbar'],
        price=None),
    'kragarm': dict(t='Kragarmtreppe', tag='Scheinbar schwebend',
        p='Die Stufen scheinen direkt aus der Wand zu wachsen. Eine verdeckte Stahlunterkonstruktion trägt jede Stufe sicher in der Betonwand oder in einer Stahlkonstruktion.',
        li=['Verdeckte Unterkonstruktion', 'Jede Stufe präzise gefertigt', 'Besonders schön mit Nurglasgeländer'],
        price=None),
    'aussen-wangen': dict(t='Stahlwangentreppe außen', tag='Modern und wetterfest',
        p='Moderne Stahlwangentreppen für Terrasse, Balkon oder Garten. Stufen aus Gitterrost, Kunststoff oder massivem Lärchenholz.',
        li=['Stufen Gitterrost, Kunststoff oder Lärche', 'Verzinkt und auf Wunsch beschichtet', 'Mit jedem Geländertyp kombinierbar'],
        price=None),
    'spindel': dict(t='Spindeltreppe', tag='Maßgefertigt',
        p='Wenn wenig Platz ist: Maßgefertigte Spindeltreppen führen platzsparend auf Balkon, Terrasse oder Dach.',
        li=['Durchmesser nach Maß', 'Stufen nach Wahl', 'Geländer passend zum Haus'],
        price=None),
    'holm': dict(t='Holmtreppe verzinkt', tag='Einfach und robust',
        p='Einfache Stufen auf einer verzinkten Holmkonstruktion – robust, pflegeleicht und schnell montiert.',
        li=['Verzinkte Holmkonstruktion', 'Gitterrost- oder Holzstufen', 'Ideal für Garten und Nebeneingang'],
        price=None),
    'pool': dict(t='Pooltreppe V4A', tag='Für Salz- und Chlorwasser',
        p='Aus Edelstahl V4A, beständig in salz- und chlorhaltigen Schwimmbecken. Wir fertigen jede Treppe individuell an.',
        li=['Edelstahl V4A', 'Individuell gefertigt', 'Passend zu Ihrem Becken'],
        price=None),
    'see': dict(t='Seetreppe', tag='Sicherer Einstieg',
        p='Stahlholmkonstruktion mit geschraubten Gitterroststufen. Ein Handlauf aus Edelstahl gibt Halt beim Ein- und Ausstieg.',
        li=['Stahlholme mit Gitterroststufen', 'Handlauf aus Edelstahl', 'Für Badesee und Teich'],
        price=None),
    'rfk': dict(t='RFK-Steg', tag='Für den Rauchfangkehrer',
        p='Ein verlässlicher Dachzugang mit festem Stand für Inspektion und Reinigung. Solide Stahlkonstruktion mit rutschsicheren Trittstufen.',
        li=['Wetterfest und langlebig', 'Rutschsichere Oberfläche', 'Privat und gewerblich'],
        price=None),
}

LEISTUNGEN = ['Vollverschweißte Ausführung', 'Fertigung aus eckigen oder runden Rohren',
              'Ohne Steck- und Schraubverbindungen', 'Verschiedenste Befestigungsarten',
              'Montage durch erfahrene Monteure', 'Nach EU-anerkannten Sicherheits- und Qualitätsnormen']

# Ordner-Beschreibungen für Alt-Texte
FOLDER = {0: 'Französischer Balkon', 1: 'Geländer mit Sonderfüllung', 2: 'Edelstahl-Glasgeländer', 3: 'Edelstahl-Handlauf',
          4: 'Nurglasgeländer', 5: 'Relinggeländer', 6: 'Seilgeländer', 7: 'Stabgeländer', 11: 'Außentreppe',
          13: 'Edelstahl-Glasgeländer', 14: 'Handlauf', 15: 'Nurglasgeländer', 16: 'Relinggeländer', 17: 'Seilgeländer',
          18: 'Stabgeländer', 19: 'Innentreppe', 21: 'Stahlgeländer', 30: 'Designgeländer aus Stahl', 31: 'Seetreppe', 32: 'Spindeltreppe', 10: 'Überdachung', 33: 'Duschverglasung'}

# Produktseiten
PAGES = [
    dict(slug='innen-treppengelaender', area='innen', materials=True, nav='Treppen- und Galeriegeländer', short='Stahl · Glas · Edelstahl',
         title='Treppen- und Galeriegeländer für innen', h1='Treppen- und Galeriegeländer für innen',
         lead='Treppen- und Galeriegeländer prägen Stiegenhaus und Wohnraum. Wir planen sie passend zu Stufen, Boden und Licht – als sichere Absturzsicherung an Treppe, Galerie und Luftraum, aus Glas, Edelstahl oder Stahl in Ihrer Farbe.',
         variants=['edelstahl-glas', 'nurglas-treppe', 'nurglas', 'design', 'stab', 'reling', 'seil'],
         cross=('aussen-treppengelaender', 'Sie suchen ein Treppengeländer für draußen?'),
         card='Glas, Edelstahl oder Stahl – passend zu Stufen und Boden.'),
    dict(slug='innen-handlaeufe', area='innen', nav='Handläufe', short='Holz · Edelstahl · Stahl · LED',
         title='Handläufe für innen', h1='Handläufe für innen',
         lead='Ein guter Handlauf liegt angenehm in der Hand und passt zur Treppe. Wir fertigen ihn aus Holz, Edelstahl oder Stahl – auf Wunsch mit integrierter LED.',
         variants=['handlauf-edelstahl', 'handlauf-holz', 'handlauf-stahl', 'handlauf-led'],
         cross=('aussen-handlaeufe', 'Sie suchen einen Handlauf für draußen?'),
         card='Holz, Edelstahl oder Stahl, auf Wunsch mit LED.'),
    dict(slug='innentreppen', area='innen', nav='Innentreppen', short='Stahlwangen · Kragarm',
         title='Innentreppen', h1='Innentreppen aus Stahl und Holz',
         lead='Treppe und Geländer aus einer Hand: Stahlwangentreppen mit massiven Holzstufen oder Kragarmtreppen, die frei aus der Wand kommen.',
         variants=['stahlwangen', 'kragarm'],
         cross=('aussentreppen', 'Sie suchen eine Treppe für draußen?'),
         card='Stahlwangen- und Kragarmtreppen mit Massivholzstufen.'),
    dict(slug='aussen-balkon-terrasse', materials=True, area='aussen', nav='Balkon- und Terrassengeländer', short='Glas · Edelstahl · Stahl',
         title='Balkon- und Terrassengeländer', h1='Balkon- und Terrassengeländer',
         lead='Draußen muss ein Geländer Wind, Wetter und Jahrzehnte aushalten. Wir fertigen es vollverschweißt aus Edelstahl, Glas oder verzinktem Stahl – passend zu Fassade und Aussicht.',
         variants=['nurglas', 'edelstahl-glas', 'stab', 'reling', 'seil', 'stahl-verzinkt', 'stahl-pulver', 'sonder'],
         cross=('innen-treppengelaender', 'Sie suchen ein Geländer für Treppe, Galerie oder Luftraum im Haus?'),
         card='Glas, Edelstahl oder Stahl für Balkon, Terrasse und Dach.'),
    dict(slug='aussen-treppengelaender', materials=True, area='aussen', nav='Treppengeländer', short='Verzinkt · Edelstahl · Glas',
         title='Treppengeländer für außen', h1='Treppengeländer für außen',
         lead='Für Eingangsstufen, Gartenstiegen und Außentreppen. Außen zählt vor allem der Korrosionsschutz: Edelstahl, feuerverzinkter oder beschichteter Stahl.',
         variants=['stahl-verzinkt', 'stahl-pulver', 'stab', 'reling', 'seil', 'edelstahl-glas', 'nurglas-treppe'],
         cross=('innen-treppengelaender', 'Sie suchen ein Treppen- oder Galeriegeländer für innen?'),
         card='Edelstahl oder verzinkter Stahl für Stiegen im Freien.'),
    dict(slug='aussen-franzoesische-balkone', materials=True, area='aussen', nav='Französische Balkone', short='Glas · Edelstahl',
         title='Französische Balkone', h1='Französische Balkone',
         lead='Bodentiefe Fenster brauchen eine Absturzsicherung. Ein französischer Balkon aus Glas oder Edelstahl sitzt direkt vor dem Fenster – auf der Fassade oder in der Laibung.',
         variants=['franz-glas', 'franz-edelstahl', 'franz-stahl'],
         cross=('aussen-balkon-terrasse', 'Sie haben einen richtigen Balkon oder eine Terrasse?'),
         card='Absturzsicherung vor bodentiefen Fenstern, aus Glas oder Edelstahl.'),
    dict(slug='aussen-handlaeufe', area='aussen', nav='Handläufe', short='Edelstahl · Stahl',
         title='Handläufe für außen', h1='Handläufe für außen',
         lead='Ein Handlauf gibt Halt an Eingangsstufen, Rampen und Gartenwegen. Für draußen fertigen wir ihn aus Edelstahl oder verzinktem und beschichtetem Stahl.',
         variants=['handlauf-edelstahl', 'handlauf-aussen-stahl'],
         cross=('innen-handlaeufe', 'Sie suchen einen Handlauf für innen?'),
         card='Halt an Eingang, Rampe und Gartenstiege.'),
    dict(slug='aussentreppen', area='aussen', nav='Außentreppen, Pool und See', short='Stahlwangen · Spindel · Pool',
         title='Außentreppen, Pool- und Seetreppen', h1='Außentreppen, Pool- und Seetreppen',
         lead='Vom Garten auf die Terrasse, vom Balkon in den Hof oder ins Wasser: Wir planen und montieren Außentreppen aus Stahl, auf Wunsch mit passendem Geländer.',
         variants=['aussen-wangen', 'spindel', 'holm', 'pool', 'see', 'rfk'],
         cross=('innentreppen', 'Sie suchen eine Treppe für innen?'),
         card='Stahltreppen für Terrasse, Garten, Pool und See.'),
]

AREAS = {
    'innen': dict(slug='innenbereich', nav='Innenbereich', title='Innenbereich',
                  h1='Geländer, Handläufe und Treppen für innen',
                  lead='Innen zählen Optik und Haptik. Ein Geländer prägt den Raum, ein Handlauf wird täglich angefasst. Wir planen beides passend zu Treppe, Boden und Licht.'),
    'aussen': dict(slug='aussenbereich', nav='Außenbereich', title='Außenbereich',
                   h1='Geländer, Handläufe und Treppen für außen',
                   lead='Außen zählen Korrosionsschutz und Witterung. Wir fertigen vollverschweißt aus Edelstahl, Glas und verzinktem Stahl – für Balkon, Terrasse, Stiege und Garten.'),
}

# Referenzen (Projekte von winnox.at, Texte wörtlich übernommen)
# entwurf=True: nur in der Vorschau sichtbar, beim Live-Bau (build.py --live) ausgeblendet
REFS = [
    dict(id='gablitz', title='Einfamilienhaus, Gablitz', objekt='Einfamilienhaus', ort='Gablitz (NÖ)', produkte='Edelstahl-Glasgeländer, Podesttreppe',
         li=['Edelstahl-Glasgeländer mit blickdichtem Verbundscheiben-Sicherheitsglas 8,76 mm', 'Ausführung einer Podesttreppe mit feuerverzinktem Gitterrostbelag'], img='aussen-balkon-terrasse', entwurf=True),
    dict(id='wien-1190', title='Wohnhausanlage, Wien 1190', objekt='Wohnhausanlage', ort='Wien, 19. Bezirk', produkte='Treppengeländer, Handlauf',
         li=['Flachstahl-Treppengeländer pulverbeschichtet RAL 1019 matt', 'Mit vorgesetztem Edelstahl-Handlauf'], img='innen-treppengelaender', entwurf=True),
    dict(id='wien-1210-efh', title='Einfamilienhaus, Wien 1210', objekt='Einfamilienhaus', ort='Wien, 21. Bezirk', produkte='Nurglasgeländer',
         li=['Nurglasgeländer mit Punkthaltern und aufgesetztem Edelstahl-U-Profil', 'VSG TVG 16,76 mm transparent'], img='innen-galerie', entwurf=True),
    dict(id='medizinproduktion', title='Medizinproduktion, Wien 1210', objekt='Gewerbe', ort='Wien, 21. Bezirk', produkte='Edelstahlgeländer, Wandhandläufe',
         li=['Edelstahlgeländer über 4 Geschosse mit vorgesetztem Handlauf und Flachstahlfüllung', 'Passende Wandhandläufe in barrierefreier Ausführung'], img='innen-handlaeufe', entwurf=True),
    dict(id='buero-wien-1210', title='Bürogebäude, Wien 1210', objekt='Bürogebäude', ort='Wien, 21. Bezirk', produkte='Treppengeländer Edelstahl-Glas',
         li=['Treppengeländer aus Edelstahl über mehrere Geschosse', 'Gefüllt mit Verbundscheiben-Sicherheitsglas 8,76 mm, transparent'], img='innen-treppengelaender', entwurf=True),
    dict(id='michelhausen', title='Wohnhausanlage, Michelhausen', objekt='Wohnhausanlage', ort='Michelhausen (NÖ)', produkte='Balkongeländer, Pfosten-Riegel-Konstruktion',
         li=['Edelstahl-Balkongeländer mit aufgeschraubten Schichtstoffplatten im Außenbereich', 'Passende Pfosten-Riegel-Konstruktion für die Abtrennung von 16 Abstellräumen'], img='ref-michelhausen'),
    dict(id='zistersdorf', title='Wohnhausanlage, Zistersdorf', objekt='Wohnhausanlage', ort='Zistersdorf (NÖ)', produkte='Edelstahl-Glasgeländer',
         li=['Edelstahl-Glasgeländer mit blickdichtem Verbundscheiben-Sicherheitsglas 8,76 mm', 'Seitliche Verblendung mit großem Windfang'], img='aussen-balkon-terrasse', entwurf=True),
    dict(id='klosterneuburg', title='Wohnhausanlage, Klosterneuburg', objekt='Wohnhausanlage', ort='Klosterneuburg (NÖ)', produkte='Flachstahlgeländer',
         li=['Flachstahlgeländer in verzinkter und pulverbeschichteter Ausführung', 'Geländer seitlich mit 3 mm Abdeckblech montiert'], img='aussen-treppengelaender', entwurf=True),
]

# ---------- Weitere Produkte (am Seitenende der Startseite und im Fußbereich) ----------
V.update({
    'ueberdachung-terrasse': dict(t='Terrassenüberdachung', tag='Schutz vor Wind und Wetter',
        p='Eine robuste Konstruktion aus Stahl oder Aluminium hält Regen und Sonne ab und wertet zugleich das Gebäude auf. Jede Überdachung wird nach Maß geplant.',
        li=['Stahl oder Aluminium', 'Eindeckung nach Wahl', 'Mit Erweiterungen kombinierbar'], price=None),
    'ueberdachung-vordach': dict(t='Vordach', tag='Für Eingang und Stiege',
        p='Ein Vordach über Haustür oder Außenstiege schützt den Eingang. Passend zu Geländer und Fassade gestaltet.',
        li=['Stahl, Edelstahl oder Aluminium', 'Glas- oder Blecheindeckung', 'Passend zum Geländer'], price=None),
    'dusche-walkin': dict(t='Walk-in-Duschwand', tag='Offen und bodeneben',
        p='Eine feststehende Glaswand für bodenebene Duschen. Ohne Tür, leicht zu reinigen und optisch ganz leicht.',
        li=['Sicherheitsglas klar oder satiniert', 'Wand- oder Deckenstabilisierung', 'Nach Maß gefertigt'], price=None),
    'dusche-tuer': dict(t='Duschabtrennung mit Tür', tag='Nische oder Ecke',
        p='Pendel- oder Schiebetür für Nische und Ecke. Beschläge in Chrom, Edelstahl oder Schwarz.',
        li=['Pendel- oder Schiebetür', 'Beschläge in verschiedenen Oberflächen', 'Maßanfertigung für Dachschrägen'], price=None),
    'hochbeet-mono': dict(t='Hochbeet Mono', tag='Vollverschweißt',
        p='Am Stück gefertigt und komplett montagebereit geliefert. Zentimetergenau nach Ihren Maßen, bis 230 cm Länge.',
        li=['Cortenstahl oder pulverbeschichtet in RAL-Farbe', 'Offener Boden für den Garten oder geschlossener Boden mit Abrinnlöchern für Terrasse und Balkon', 'Lieferung per Spedition'],
        price='ab € 469,–', pnote='Endpreis je nach Konfiguration'),
    'hochbeet-modular': dict(t='Hochbeet Modular', tag='Verschraubt und erweiterbar',
        p='Wird in passgenauen Einzelteilen geliefert und mit einem Steck- und Schraubsystem aufgebaut – ideal für enge Stiegenhäuser und Dachterrassen. Beliebig erweiterbar, auch für Übergrößen.',
        li=['Cortenstahl oder pulverbeschichtet in RAL-Farbe', 'Endlos erweiterbar', 'Einfacher Aufbau vor Ort'],
        price='ab € 119,–', pnote='Endpreis je nach Konfiguration'),
})

AREAS['weitere'] = dict(slug='weitere-produkte', nav='Weitere Produkte', title='Weitere Produkte',
    h1='Weitere Produkte aus Metall und Glas',
    lead='Was wir für Geländer und Treppen können, passt auch für mehr: Überdachungen, Duschverglasungen und Hochbeete – geplant, gefertigt und montiert aus einer Hand.')

PAGES += [
    dict(slug='ueberdachungen', area='weitere', nav='Überdachungen', short='Terrasse · Vordach',
         title='Überdachungen', h1='Überdachungen für Terrasse und Eingang',
         lead='Zuverlässiger Schutz vor Wind und Wetter: Robuste Konstruktionen aus Stahl oder Aluminium, individuell gestaltet und passend zu Ihrem Haus.',
         variants=['ueberdachung-terrasse', 'ueberdachung-vordach'],
         cross=('aussen-balkon-terrasse', 'Dazu ein passendes Terrassengeländer?'),
         card='Terrassenüberdachungen und Vordächer aus Stahl oder Aluminium.'),
    dict(slug='duschverglasung', area='weitere', nav='Duschverglasung', short='Walk-in · Tür · Nische',
         title='Duschverglasung', h1='Duschverglasung nach Maß',
         lead='Glas nach Maß für Ihr Bad: als offene Walk-in-Wand oder als Abtrennung mit Tür – auch für Nischen und Dachschrägen.',
         variants=['dusche-walkin', 'dusche-tuer'],
         cross=('innen-treppengelaender', 'Glas auch im Stiegenhaus? Zu den Glasgeländern'),
         card='Walk-in-Duschwände und Abtrennungen mit Tür, nach Maß.'),
    dict(slug='hochbeete', area='weitere', nav='Hochbeete', short='Cortenstahl · RAL-Farbe · nach Maß',
         title='Hochbeete', h1='Hochbeete aus Stahl',
         lead='Hochbeete und Pflanzgefäße nach Maß, in Handarbeit in Österreich gefertigt. Aus Cortenstahl mit natürlicher Rost-Patina oder pulverbeschichtet in Ihrer RAL-Farbe – zum Beispiel Anthrazit, Lichtgrau, Creme oder Weiß.',
         variants=['hochbeet-mono', 'hochbeet-modular'], unit='', extra_note='Lieferzeit rund 21 Werktage, 2 Jahre Garantie. Konfigurieren und bestellen können Sie Ihr Hochbeet auch direkt auf wunschbeet.com.',
         link=('https://www.wunschbeet.com/konfigurator', 'Hochbeet auf wunschbeet.com konfigurieren'),
         cross=('aussentreppen', 'Dazu eine Gartentreppe?'),
         card='Hochbeete aus Cortenstahl oder in RAL-Farbe, zentimetergenau.'),
]
