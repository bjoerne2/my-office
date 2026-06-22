# Office Scripts

Dieses Repository enthält kleine Office-Automatisierungen.

Aktuell enthalten:

- `process_paypal_report`: Verarbeitung von PayPal-CSV-Reports und Umwandlung in Excel.
- `export_transactions`: Exportiert Monatsumsätze aus MoneyMoney und verschiebt die CSV nach `tmp/staging/<jahr>/<monat>/transactions.csv`.
- `extract_transactions`: Filtert Monatsumsätze pro Rechnungssteller nach `tmp/staging/<jahr>/<monat>/<Rechnungssteller>/transactions.csv`.
- `match_receipts`: Findet passende PDFs in `tmp/app_scripts_data/<Rechnungssteller>` und kopiert sie direkt in den Staging-Monatsordner.
- `create_transaction_pdfs`: Erzeugt aus extrahierten Transaktionen einfache PDF-Dateien mit Schlüssel/Wert-Tabelle im Staging-Monatsordner.
- `merge_receipt_and_transaction_pdfs`: Führt Rechnungs-PDFs und Kontobeleg-PDFs paarweise zu kombinierten PDFs zusammen.
- `process_vendor_month`: Führt alle Schritte für einen Anbieter und Monat als Gesamt-Workflow aus.
- `sync_app_scripts_data`: Synchronisiert `tmp/app_scripts_data` unidirektional von Google Drive nach lokal.

## Voraussetzungen

- Python ≥ 3.10 (z.B. installiert über Homebrew)

## Gemeinsame Python-Hilfsmodule

Wiederverwendbare Python-Helfer liegen unter `python/`, z. B.:

- `python/args.py` für Argument-Validierung
- `python/vendors.py` für Anbieter-/Namenszuordnungen
- `python/meta.py` für zentrales Lesen/Schreiben von `meta.json`

## Python Installation (Homebrew)

```bash
brew install python
```

## Python Update (Homebrew)

```bash
brew update
brew upgrade python
```

## Virtuelle Umgebung einrichten

Die Python-Abhängigkeiten werden projektlokal in `/.venv` installiert.

```bash
cd /Users/bjoerne/Source/my-office
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
```

Danach ist keine manuelle Aktivierung pro Shell-Session nötig.
`./process_paypal_report` sowie die Python-Skripte im Repository verwenden automatisch `/.venv`, wenn vorhanden.

## Abhängigkeiten aktualisieren

Wenn neue Pakete hinzukommen:

```bash
./.venv/bin/python -m pip install <paketname>
./.venv/bin/python -m pip freeze > requirements.txt
```

## Verwendung

```bash
./process_paypal_report <report.csv>
```

Die Ausgabe (`*_processed.xlsx`) wird im selben Verzeichnis wie die Eingabedatei erzeugt.

### MoneyMoney Monats-Export

```bash
./export_transactions 2026 05
```

Die Ausgabe wird nach `tmp/staging/2026/05/transactions.csv` verschoben.

### MoneyMoney Rechnungssteller-Extraktion

```bash
./extract_transactions 2026 01 github
```

Die Ausgabe wird nach `tmp/staging/2026/01/GitHub/transactions.csv` geschrieben.

### MoneyMoney PDF-Matching

```bash
./match_receipts 2026 01 github
```

Die passenden PDFs werden aus `tmp/app_scripts_data/GitHub/` gelesen, direkt nach `tmp/staging/2026/01/GitHub/` kopiert
und als Eintragsliste in `meta.json` abgelegt.

### MoneyMoney Transaktions-PDF erzeugen

```bash
./create_transaction_pdfs 2026 01 github
```

Das Skript liest `tmp/staging/2026/01/GitHub/transactions.csv`, erzeugt pro Zeile ein PDF mit einer einfachen
Schlüssel/Wert-Tabelle direkt in `tmp/staging/2026/01/GitHub/` und ergänzt die zugehörigen Meta-Einträge.

### Rechnung und Buchung zusammenführen

```bash
./merge_receipt_and_transaction_pdfs 2026 01 github
```

Das Skript führt die in `meta.json` zugeordneten Rechnungs- und Kontobeleg-PDFs im Ordner
`tmp/staging/2026/01/GitHub/` paarweise zusammen und schreibt Ausgabedateien auf Basis des Rechnungsdateinamens.

### Gesamt-Workflow für einen Anbieter

```bash
./process_vendor_month 2026 01 github
```

Der Workflow führt nacheinander aus:

1. `export_transactions`
2. `extract_transactions`
3. `match_receipts`
4. `create_transaction_pdfs`
5. `merge_receipt_and_transaction_pdfs`

Wenn die Exportdatei bereits vorhanden ist und der MoneyMoney-Export übersprungen werden soll:

```bash
./process_vendor_month 2026 01 github --skip-export
```

## rclone / Google Drive Sync

Installation unter macOS:

```bash
brew update
brew install rclone
```

Google Drive als Remote einrichten:

```bash
rclone config
```

Dabei z.B. `gdrive` als Remote anlegen und den Zielordner direkt über `root_folder_id` fest verdrahten.
Danach startet der Download-Sync von diesem Remote-Root nach lokal so:

```bash
cd /Users/bjoerne/Source/my-office
./sync_app_scripts_data
```

Falls dein Remote anders heißt:

```bash
cd /Users/bjoerne/Source/my-office
RCLONE_REMOTE_NAME="meinremote" ./sync_app_scripts_data
```

Hinweis: Das Skript verwendet `rclone sync` von **remote nach lokal**. Lokale Dateien, die remote nicht existieren, werden dabei entfernt.
