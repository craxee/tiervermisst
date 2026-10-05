# tiervermisst.at – so geht die Seite online

Die Seite läuft kostenlos auf GitHub Pages. Alle 30 Minuten holt GitHub automatisch die neuen Fundtiere und Fotos von der Stadt Wien und veröffentlicht die Seite neu. Du musst dafür keinen Computer laufen lassen.

## Was in diesem Ordner ist

| Datei | Wozu |
|---|---|
| `index.html` | Die Webseite |
| `data.json` | Die Fundtiere (wird automatisch aktualisiert) |
| `photos/` | Die Fotos (werden automatisch geladen) |
| `scripts/update.py` | Das Programm, das die Daten bei der Stadt Wien abholt |
| `.github/workflows/update.yml` | Sagt GitHub, wann das Programm laufen soll |
| `impressum.html`, `datenschutz.html` | Pflichtseiten – **vor dem Veröffentlichen ausfüllen** |

## 1. GitHub-Konto anlegen
Auf https://github.com kostenlos registrieren. Dein Benutzername kommt später in die Adresse der Seite.

## 2. Neues Projekt (Repository) anlegen
- Oben rechts auf **+** → **New repository**.
- Name: `tiervermisst`
- **Public** auswählen (GitHub Pages ist nur für öffentliche Projekte kostenlos).
- Auf **Create repository** klicken.

## 3. Dateien hochladen
- Im neuen Projekt auf **uploading an existing file** klicken.
- Den **Inhalt** des entpackten Ordners hineinziehen (nicht den Ordner selbst).
- Unten auf **Commit changes** klicken.

**Wichtig:** Der Ordner `.github` beginnt mit einem Punkt und ist auf dem Computer oft unsichtbar.
- Mac: Im Finder **Cmd + Shift + .** drücken, dann wird er sichtbar.
- Windows: Im Explorer unter **Ansicht** „Ausgeblendete Elemente“ einschalten.

Prüf danach im Projekt, ob es den Ordner `.github/workflows` gibt. Falls nicht: **Add file → Create new file**, als Namen `.github/workflows/update.yml` eintippen, den Inhalt der Datei `update.yml` hineinkopieren und speichern.

## 4. Impressum und Datenschutz ausfüllen
In GitHub die Datei `impressum.html` anklicken, oben rechts auf den Stift ✏️, die Platzhalter in eckigen Klammern ersetzen und speichern. Dasselbe bei `datenschutz.html`.

## 5. GitHub Pages einschalten
- Im Projekt auf **Settings** → links **Pages**.
- Bei **Source** „**GitHub Actions**“ auswählen.

## 6. Ersten Durchlauf starten
- Oben auf **Actions**. Falls GitHub fragt, ob Workflows erlaubt werden sollen: bestätigen.
- Links **Fundtiere aktualisieren** anklicken → rechts **Run workflow** → **Run workflow**.
- Nach 2–5 Minuten ist ein grüner Haken da. Die Seite ist dann erreichbar unter:
  `https://DEIN-BENUTZERNAME.github.io/tiervermisst/`

Ab jetzt läuft alles von selbst.

## Wenn etwas nicht klappt
- **Roter Fehler beim Schritt „Neue Daten speichern“:** Settings → Actions → General → ganz unten bei *Workflow permissions* „**Read and write permissions**“ wählen und speichern. Dann noch einmal *Run workflow*.
- **E-Mail von GitHub über einen fehlgeschlagenen Lauf:** Meist war der Server der Stadt kurz nicht erreichbar. Der nächste Lauf 30 Minuten später klappt in der Regel wieder. Die Seite zeigt so lange die letzten Daten. Sind die Daten älter als einen Tag, erscheint auf der Seite automatisch ein Warnhinweis.
- **GitHub hat den automatischen Ablauf pausiert:** Unter **Actions** → **Fundtiere aktualisieren** auf **Enable workflow** klicken.

## Später: eigene Adresse (z. B. tiervermisst.at)
1. Adresse bei einem Anbieter kaufen (Verfügbarkeit vorher auf nic.at prüfen).
2. In GitHub: **Settings → Pages → Custom domain** die Adresse eintragen.
3. Beim Anbieter die DNS-Einträge so setzen, wie GitHub es dort anzeigt.
4. „**Enforce HTTPS**“ anhaken, sobald es verfügbar ist.

## Datenquelle
Stadt Wien – Veterinäramt und Tierschutz (MA 60), „Fund- und Vergabetiere“, data.gv.at, Lizenz CC BY 4.0. Die Quellenangabe auf der Seite muss bleiben.
