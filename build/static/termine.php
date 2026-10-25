<?php
/*
 * METALLFUX – Beratungstermine
 *
 *   GET  termine.php?slots=1   freie Zeiten als JSON (aus dem Google Kalender, nur frei/belegt)
 *   POST termine.php           Terminanfrage, wird per E-Mail an EMPFAENGER geschickt (mit .ics zum Eintragen)
 *
 * Der Kalender wird nur hier am Server gelesen (geheime iCal-Adresse in termine-config.php).
 * Besucher sehen keine Termininhalte und laden nichts von Google.
 */
require __DIR__ . '/termine-config.php';

const EMPFAENGER   = 'office@metallfux-wien.at';
const ABSENDER     = 'webseite@metallfux-wien.at';
const TAG_START    = 9;     // erster Termin um 09:00
const TAG_ENDE     = 17;    // letzter Termin endet um 17:00
const DAUER_MIN    = 60;    // Länge eines Beratungstermins
const PUFFER_MIN   = 30;    // Fahrzeit vor und nach bestehenden Terminen
const TAGE_VORAUS  = 28;    // buchbar bis 4 Wochen im Voraus
const CACHE_MIN    = 10;    // Kalender höchstens alle 10 Minuten neu laden
const CACHE_DATEI  = __DIR__ . '/termine-cache/kalender.ics';
const ANGEFRAGT    = __DIR__ . '/termine-cache/angefragt.json';   // angefragte Zeiten 24 h ausblenden

date_default_timezone_set('Europe/Vienna');

// ---------- Kalender laden ----------
function kalender_text() {
    if (!is_dir(dirname(CACHE_DATEI))) @mkdir(dirname(CACHE_DATEI), 0700, true);
    $alter = is_file(CACHE_DATEI) ? time() - filemtime(CACHE_DATEI) : PHP_INT_MAX;
    if ($alter < CACHE_MIN * 60) return file_get_contents(CACHE_DATEI);
    if (ICAL_URL === '') return null;
    $ctx = stream_context_create(['http' => ['timeout' => 8, 'user_agent' => 'METALLFUX-Termine']]);
    $neu = @file_get_contents(ICAL_URL, false, $ctx);
    if ($neu !== false && strpos($neu, 'BEGIN:VCALENDAR') !== false) {
        @file_put_contents(CACHE_DATEI, $neu, LOCK_EX);
        return $neu;
    }
    // Google nicht erreichbar: alten Stand bis 24 h weiterverwenden
    return $alter < 86400 ? file_get_contents(CACHE_DATEI) : null;
}

// ---------- iCal auswerten ----------
function ics_zeit($wert, $params) {
    if (preg_match('/^\d{8}$/', $wert)) return [new DateTimeImmutable($wert . 'T000000'), true];
    $tz = null;
    if (substr($wert, -1) === 'Z') { $tz = new DateTimeZone('UTC'); $wert = substr($wert, 0, -1); }
    elseif (preg_match('/TZID=("?)([^";:]+)\1/', $params, $m)) { try { $tz = new DateTimeZone($m[2]); } catch (Exception $e) { $tz = null; } }
    $d = DateTimeImmutable::createFromFormat('Ymd\THis', $wert, $tz ?: new DateTimeZone('Europe/Vienna'));
    return [$d ? $d->setTimezone(new DateTimeZone('Europe/Vienna')) : null, false];
}

function ics_events($text) {
    $text = preg_replace("/\r?\n[ \t]/", '', str_replace("\r\n", "\n", $text));
    $events = []; $e = null;
    foreach (explode("\n", $text) as $zeile) {
        if ($zeile === 'BEGIN:VEVENT') { $e = ['exdate' => []]; continue; }
        if ($zeile === 'END:VEVENT') { if ($e) $events[] = $e; $e = null; continue; }
        if ($e === null || !preg_match('/^([A-Z-]+)((?:;[^:]*)?):(.*)$/', $zeile, $m)) continue;
        [, $key, $params, $wert] = $m;
        switch ($key) {
            case 'DTSTART': case 'DTEND': case 'RECURRENCE-ID':
                [$d, $ganztags] = ics_zeit($wert, $params);
                $e[$key] = $d; if ($key === 'DTSTART') $e['ganztags'] = $ganztags; break;
            case 'EXDATE':
                foreach (explode(',', $wert) as $w) { [$d] = ics_zeit($w, $params); if ($d) $e['exdate'][] = $d->format('YmdHi'); } break;
            case 'DURATION': $e['DURATION'] = $wert; break;
            case 'RRULE': case 'UID': case 'STATUS': case 'TRANSP': $e[$key] = $wert; break;
        }
    }
    return $events;
}

function wiederholungen($start, $rrule, $bis) {
    $r = [];
    foreach (explode(';', $rrule) as $teil) { [$k, $v] = array_pad(explode('=', $teil, 2), 2, ''); $r[$k] = $v; }
    $freq = $r['FREQ'] ?? ''; $iv = max(1, (int)($r['INTERVAL'] ?? 1));
    $count = isset($r['COUNT']) ? (int)$r['COUNT'] : null;
    $until = null;
    if (isset($r['UNTIL'])) { [$until] = ics_zeit($r['UNTIL'], ''); if ($until && strlen($r['UNTIL']) === 8) $until = $until->setTime(23, 59, 59); }
    $tage = ['MO' => 1, 'TU' => 2, 'WE' => 3, 'TH' => 4, 'FR' => 5, 'SA' => 6, 'SU' => 7];
    $byday = isset($r['BYDAY']) ? explode(',', $r['BYDAY']) : [];
    $zeit = $start->format('H:i:s');
    $out = []; $n = 0;
    $ende = ($until && $until < $bis) ? $until : $bis;
    $nimm = function ($d) use (&$out, &$n, $count, $start, $ende) {
        if ($d < $start || $d > $ende) return $d <= $ende;
        if ($count !== null && $n >= $count) return false;
        $out[] = $d; $n++; return true;
    };
    for ($i = 0; $i < 3000; $i++) {
        if ($freq === 'DAILY') {
            $d = $start->modify('+' . ($i * $iv) . ' days');
            if (!$nimm($d)) break;
        } elseif ($freq === 'WEEKLY') {
            $woche = $start->modify('monday this week')->modify('+' . ($i * $iv) . ' weeks');
            if ($woche > $ende) break;
            $liste = $byday ?: [array_search((int)$start->format('N'), $tage)];
            $kandidaten = [];
            foreach ($liste as $t) if (isset($tage[$t])) $kandidaten[] = $woche->modify('+' . ($tage[$t] - 1) . ' days')->modify($zeit);
            sort($kandidaten);
            foreach ($kandidaten as $d) if (!$nimm($d) && $d > $ende) break 2;
            if ($count !== null && $n >= $count) break;
        } elseif ($freq === 'MONTHLY' || $freq === 'YEARLY') {
            $basis = $start->modify('first day of this month')->modify('+' . ($i * $iv * ($freq === 'YEARLY' ? 12 : 1)) . ' months');
            if ($basis > $ende) break;
            if ($byday && preg_match('/^(-?\d)?([A-Z]{2})$/', $byday[0], $m) && isset($tage[$m[2]])) {
                $namen = [1 => 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
                $nr = (int)($m[1] ?: 1); $wort = [1 => 'first', 'second', 'third', 'fourth', 'fifth', -1 => 'last'][$nr] ?? 'first';
                $d = $basis->modify($wort . ' ' . $namen[$tage[$m[2]]] . ' of this month')->modify($zeit);
            } else {
                $tag = (int)$start->format('j');
                if ($tag > (int)$basis->format('t')) continue;
                $d = $basis->setDate((int)$basis->format('Y'), (int)$basis->format('n'), $tag)->modify($zeit);
            }
            if (!$nimm($d)) break;
        } else break;
        if ($count !== null && $n >= $count) break;
    }
    return $out;
}

function belegt($von, $bis) {
    $text = kalender_text();
    if ($text === null) return null;
    $events = ics_events($text);
    $verschoben = [];
    foreach ($events as $e) if (!empty($e['RECURRENCE-ID']) && !empty($e['UID'])) $verschoben[$e['UID']][] = $e['RECURRENCE-ID']->format('YmdHi');
    $zeiten = [];
    foreach ($events as $e) {
        if (empty($e['DTSTART']) || ($e['STATUS'] ?? '') === 'CANCELLED' || ($e['TRANSP'] ?? '') === 'TRANSPARENT') continue;
        $start = $e['DTSTART'];
        if (!empty($e['DTEND'])) $laenge = $e['DTEND']->getTimestamp() - $start->getTimestamp();
        elseif (!empty($e['DURATION'])) { try { $laenge = $start->add(new DateInterval(ltrim($e['DURATION'], '+')))->getTimestamp() - $start->getTimestamp(); } catch (Exception $x) { $laenge = 3600; } }
        else $laenge = $e['ganztags'] ? 86400 : 0;
        $starts = (!empty($e['RRULE']) && empty($e['RECURRENCE-ID'])) ? wiederholungen($start, $e['RRULE'], $bis) : [$start];
        $aus = array_merge($e['exdate'], empty($e['RECURRENCE-ID']) ? ($verschoben[$e['UID'] ?? ''] ?? []) : []);
        foreach ($starts as $s) {
            if (in_array($s->format('YmdHi'), $aus, true)) continue;
            $a = $s->getTimestamp(); $b = $a + max($laenge, 60);
            if ($b < $von->getTimestamp() || $a > $bis->getTimestamp()) continue;
            $zeiten[] = [$a, $b];
        }
    }
    return $zeiten;
}

// ---------- Feiertage Österreich ----------
function feiertage($jahr) {
    $a = $jahr % 19; $b = intdiv($jahr, 100); $c = $jahr % 100; $d = intdiv($b, 4); $e = $b % 4;
    $f = intdiv($b + 8, 25); $g = intdiv($b - $f + 1, 3); $h = (19 * $a + $b - $d - $g + 15) % 30;
    $i = intdiv($c, 4); $k = $c % 4; $l = (32 + 2 * $e + 2 * $i - $h - $k) % 7; $m = intdiv($a + 11 * $h + 22 * $l, 451);
    $monat = intdiv($h + $l - 7 * $m + 114, 31); $tag = (($h + $l - 7 * $m + 114) % 31) + 1;
    $ostern = new DateTimeImmutable(sprintf('%04d-%02d-%02d', $jahr, $monat, $tag));
    $liste = ["$jahr-01-01", "$jahr-01-06", "$jahr-05-01", "$jahr-08-15", "$jahr-10-26", "$jahr-11-01", "$jahr-12-08", "$jahr-12-25", "$jahr-12-26"];
    foreach ([1, 39, 50, 60] as $plus) $liste[] = $ostern->modify("+$plus days")->format('Y-m-d');
    return $liste;
}

// ---------- bereits angefragte Zeiten ----------
function angefragt($neu = null) {
    $liste = is_file(ANGEFRAGT) ? (json_decode(file_get_contents(ANGEFRAGT), true) ?: []) : [];
    $liste = array_filter($liste, function ($zeit) { return $zeit > time() - 86400; });
    if ($neu !== null) { $liste[$neu] = time(); @file_put_contents(ANGEFRAGT, json_encode($liste), LOCK_EX); }
    return $liste;
}

// ---------- freie Zeiten ----------
function freie_zeiten() {
    $heute = new DateTimeImmutable('today');
    $von = $heute->modify('+1 day');
    while ((int)$von->format('N') > 5 || in_array($von->format('Y-m-d'), feiertage((int)$von->format('Y')), true)) $von = $von->modify('+1 day');
    $bis = $heute->modify('+' . TAGE_VORAUS . ' days')->setTime(23, 59);
    $busy = belegt($von, $bis);
    if ($busy === null) return null;
    $angefragt = angefragt();
    $frei = [];
    for ($tag = $von; $tag <= $bis; $tag = $tag->modify('+1 day')) {
        if ((int)$tag->format('N') > 5 || in_array($tag->format('Y-m-d'), feiertage((int)$tag->format('Y')), true)) continue;
        for ($t = $tag->setTime(TAG_START, 0); $t->modify('+' . DAUER_MIN . ' minutes') <= $tag->setTime(TAG_ENDE, 0); $t = $t->modify('+' . DAUER_MIN . ' minutes')) {
            $a = $t->getTimestamp() - PUFFER_MIN * 60; $b = $t->getTimestamp() + (DAUER_MIN + PUFFER_MIN) * 60;
            $ok = true;
            foreach ($busy as [$x, $y]) if ($x < $b && $y > $a) { $ok = false; break; }
            if ($ok && isset($angefragt[$t->format('Y-m-d H:i')])) $ok = false;
            if ($ok) $frei[$tag->format('Y-m-d')][] = $t->format('H:i');
        }
    }
    return $frei;
}

// ---------- Ausgabe ----------
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

function antwort($daten, $code = 200) { http_response_code($code); echo json_encode($daten, JSON_UNESCAPED_UNICODE); exit; }
function feld($name, $max = 200) {
    $v = isset($_POST[$name]) ? trim((string)$_POST[$name]) : '';
    return mb_substr(str_replace(["\r", "\0"], '', $v), 0, $max);
}
function zeile($v) { return str_replace(["\n", "\r"], ' ', $v); }

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $frei = freie_zeiten();
    if ($frei === null) antwort(['ok' => false, 'error' => 'Der Kalender ist gerade nicht erreichbar.'], 503);
    antwort(['ok' => true, 'dauer' => DAUER_MIN, 'slots' => $frei]);
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') antwort(['ok' => false, 'error' => 'Ungültige Anfrage.'], 405);

if (feld('website') !== '') antwort(['ok' => true]);   // Spam-Falle

$termin = feld('termin', 20);
$name   = zeile(feld('name', 120));
$email  = zeile(feld('email', 160));
$tel    = zeile(feld('telefon', 60));
$adr    = zeile(feld('adresse', 160));
$plz    = zeile(feld('plz', 10));
$ort    = zeile(feld('ort', 120));
$produkt= zeile(feld('produkt', 120));
$text   = feld('nachricht', 3000);

if (!preg_match('/^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})$/', $termin, $tm)) antwort(['ok' => false, 'error' => 'Bitte einen Termin wählen.'], 422);
if ($name === '' || $tel === '' || $plz === '' || $ort === '') antwort(['ok' => false, 'error' => 'Bitte Name, Telefon, PLZ und Ort ausfüllen.'], 422);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) antwort(['ok' => false, 'error' => 'Bitte eine gültige E-Mail-Adresse angeben.'], 422);
if (feld('datenschutz', 5) !== 'ja') antwort(['ok' => false, 'error' => 'Bitte der Datenverarbeitung zustimmen.'], 422);

$frei = freie_zeiten();
if ($frei !== null && !in_array($tm[2], $frei[$tm[1]] ?? [], true)) antwort(['ok' => false, 'error' => 'Dieser Termin ist leider gerade vergeben worden. Bitte wählen Sie einen anderen.', 'vergeben' => true], 409);

$start = new DateTimeImmutable($termin);
$wt = ['', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'][(int)$start->format('N')];
$wann = $wt . ', ' . $start->format('d.m.Y') . ' um ' . $start->format('H:i') . ' Uhr';

$betreff = 'Terminanfrage: ' . $wt . ' ' . $start->format('d.m. H:i') . ' – ' . $plz . ' ' . $ort;
$inhalt = "Neue Terminanfrage für eine Beratung vor Ort\n\n"
    . "Wunschtermin: $wann (" . DAUER_MIN . " Min.)\n\n"
    . "Name:      $name\nTelefon:   $tel\nE-Mail:    $email\n"
    . "Adresse:   $adr, $plz $ort\nThema:     $produkt\n\nNachricht:\n" . ($text !== '' ? $text : '(keine)') . "\n\n"
    . "Der Termin ist noch nicht fix. Bitte innerhalb von 12 Stunden bestätigen oder einen anderen Termin vorschlagen.\n"
    . "Im Anhang liegt der Termin als Kalenderdatei (vorläufig).\n";

$utc = new DateTimeZone('UTC');
$ics = "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//METALLFUX//Termine//DE\r\nBEGIN:VEVENT\r\n"
    . 'UID:' . bin2hex(random_bytes(8)) . "@metallfux-wien.at\r\n"
    . 'DTSTAMP:' . (new DateTimeImmutable('now', $utc))->format('Ymd\THis\Z') . "\r\n"
    . 'DTSTART:' . $start->setTimezone($utc)->format('Ymd\THis\Z') . "\r\n"
    . 'DTEND:' . $start->modify('+' . DAUER_MIN . ' minutes')->setTimezone($utc)->format('Ymd\THis\Z') . "\r\n"
    . 'SUMMARY:' . addcslashes('Beratung (angefragt): ' . $name, ',;\\') . "\r\n"
    . 'LOCATION:' . addcslashes("$adr, $plz $ort", ',;\\') . "\r\n"
    . 'DESCRIPTION:' . addcslashes("Tel. $tel · $email · $produkt", ',;\\') . "\r\n"
    . "STATUS:TENTATIVE\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n";

$grenze = 'mfx_' . bin2hex(random_bytes(12));
$kopf  = 'From: METALLFUX Website <' . ABSENDER . ">\r\n";
$kopf .= 'Reply-To: ' . mb_encode_mimeheader($name, 'UTF-8') . ' <' . $email . ">\r\n";
$kopf .= "MIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary=\"$grenze\"\r\n";
$body  = "--$grenze\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($inhalt)) . "\r\n";
$body .= "--$grenze\r\nContent-Type: text/calendar; charset=UTF-8; name=\"termin.ics\"\r\nContent-Transfer-Encoding: base64\r\n"
    . "Content-Disposition: attachment; filename=\"termin.ics\"\r\n\r\n" . chunk_split(base64_encode($ics)) . "\r\n--$grenze--\r\n";

angefragt($termin);
if (getenv('MFX_TEST_MAIL')) { file_put_contents(getenv('MFX_TEST_MAIL'), $betreff . "\n\n" . $inhalt . "\n" . $ics); antwort(['ok' => true]); }
$ok = mail(EMPFAENGER, mb_encode_mimeheader($betreff, 'UTF-8'), $body, $kopf, '-f' . ABSENDER);
if (!$ok) antwort(['ok' => false, 'error' => 'Der Versand ist fehlgeschlagen.'], 500);
antwort(['ok' => true]);
