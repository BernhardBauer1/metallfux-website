<?php
/*
 * METALLFUX – Anfrageformular
 * Verschickt die Anfrage samt Fotos/Plänen per E-Mail. Läuft auf jedem PHP-Webspace mit mail() (z. B. ALL-INKL).
 * Vor dem Livegang: EMPFAENGER und ABSENDER prüfen und einmal selbst testen.
 */
const EMPFAENGER = 'office@metallfux-wien.at';
const ABSENDER   = 'webseite@metallfux-wien.at';   // Adresse der eigenen Domain, damit die Mail nicht im Spam landet
const MAX_DATEIEN = 8;
const MAX_GESAMT  = 20 * 1024 * 1024;               // 20 MB
const ERLAUBT = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/heic' => 'heic', 'image/heif' => 'heic', 'application/pdf' => 'pdf'];

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

function antwort($ok, $fehler = null, $code = 200) {
    http_response_code($code);
    echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $fehler], JSON_UNESCAPED_UNICODE);
    exit;
}
function feld($name, $max = 200) {
    $v = isset($_POST[$name]) ? trim((string)$_POST[$name]) : '';
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
}
function zeile($v) { return str_replace(["\n", "\r"], ' ', $v); }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') antwort(false, 'Ungültige Anfrage.', 405);

// Spam-Schutz: verstecktes Feld muss leer bleiben, Mindestzeit über Session wäre optional
if (feld('website') !== '') antwort(true);

$name   = zeile(feld('name', 120));
$email  = zeile(feld('email', 160));
$tel    = zeile(feld('telefon', 60));
$plz    = zeile(feld('plz', 10));
$ort    = zeile(feld('ort', 120));
$bereich= zeile(feld('bereich', 40));
$produkt= zeile(feld('produkt', 120));
$text   = feld('nachricht', 5000);
$rueck  = feld('rueckruf', 5) === 'ja' ? 'Ja' : 'Nein';

if ($name === '' || $plz === '' || $ort === '') antwort(false, 'Bitte Name, PLZ und Ort ausfüllen.', 422);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) antwort(false, 'Bitte eine gültige E-Mail-Adresse angeben.', 422);
if (feld('datenschutz', 5) !== 'ja') antwort(false, 'Bitte der Datenverarbeitung zustimmen.', 422);

// Dateien prüfen
$anhaenge = [];
if (!empty($_FILES['dateien']) && is_array($_FILES['dateien']['name'])) {
    $anzahl = count($_FILES['dateien']['name']);
    $summe = 0;
    $finfo = new finfo(FILEINFO_MIME_TYPE);
    for ($i = 0; $i < $anzahl; $i++) {
        if ($_FILES['dateien']['error'][$i] === UPLOAD_ERR_NO_FILE) continue;
        if ($_FILES['dateien']['error'][$i] !== UPLOAD_ERR_OK) antwort(false, 'Eine Datei konnte nicht hochgeladen werden (zu groß?).', 422);
        if (count($anhaenge) >= MAX_DATEIEN) antwort(false, 'Bitte höchstens ' . MAX_DATEIEN . ' Dateien anhängen.', 422);
        $tmp = $_FILES['dateien']['tmp_name'][$i];
        $mime = $finfo->file($tmp);
        if (!isset(ERLAUBT[$mime])) antwort(false, 'Erlaubt sind JPG, PNG, HEIC und PDF.', 422);
        $summe += filesize($tmp);
        if ($summe > MAX_GESAMT) antwort(false, 'Die Dateien sind zusammen größer als 20 MB.', 422);
        $basis = preg_replace('/[^A-Za-z0-9._-]/', '_', pathinfo($_FILES['dateien']['name'][$i], PATHINFO_FILENAME));
        $anhaenge[] = ['name' => substr($basis, 0, 60) . '.' . ERLAUBT[$mime], 'mime' => $mime, 'data' => file_get_contents($tmp)];
    }
}

$betreff = 'Website-Anfrage: ' . $produkt . ' – ' . $plz . ' ' . $ort;
$inhalt = "Neue Anfrage über " . ($_SERVER['HTTP_HOST'] ?? 'die Website') . "\n\n"
    . "Name:      $name\nE-Mail:    $email\nTelefon:   $tel\nRückruf:   $rueck\n"
    . "Ort:       $plz $ort\nBereich:   $bereich\nProdukt:   $produkt\n"
    . "Anhänge:   " . count($anhaenge) . "\n\nNachricht:\n" . ($text !== '' ? $text : '(keine)') . "\n";

$grenze = 'mfx_' . bin2hex(random_bytes(12));
$kopf  = 'From: METALLFUX Website <' . ABSENDER . ">\r\n";
$kopf .= 'Reply-To: ' . mb_encode_mimeheader($name, 'UTF-8') . ' <' . $email . ">\r\n";
$kopf .= "MIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary=\"$grenze\"\r\n";

$body  = "--$grenze\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n";
$body .= chunk_split(base64_encode($inhalt)) . "\r\n";
foreach ($anhaenge as $a) {
    $body .= "--$grenze\r\nContent-Type: {$a['mime']}; name=\"{$a['name']}\"\r\nContent-Transfer-Encoding: base64\r\n";
    $body .= "Content-Disposition: attachment; filename=\"{$a['name']}\"\r\n\r\n" . chunk_split(base64_encode($a['data'])) . "\r\n";
}
$body .= "--$grenze--\r\n";

$ok = mail(EMPFAENGER, mb_encode_mimeheader($betreff, 'UTF-8'), $body, $kopf, '-f' . ABSENDER);
if (!$ok) antwort(false, 'Der Mailversand ist fehlgeschlagen.', 500);
antwort(true);
