# Office Scripts

Dieses Repository enthält kleine Office-Automatisierungen.

Aktuell enthalten:

- `monkkee/process_paypal_report`: Verarbeitung von PayPal-CSV-Reports und Umwandlung in Excel.
- `money_money/export_transactions`: Exportiert Monatsumsätze aus MoneyMoney und verschiebt die CSV nach `tmp/accounting/<jahr>/<monat>/transactions.csv`.
- `rclone/sync_app_scripts_data`: Synchronisiert `tmp/app_scripts_data` unidirektional von Google Drive nach lokal.

## Voraussetzungen

- Python ≥ 3.10 (z.B. installiert über Homebrew)

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
`./monkkee/process_paypal_report` verwendet automatisch `/.venv`, wenn vorhanden.

## Abhängigkeiten aktualisieren

Wenn neue Pakete hinzukommen:

```bash
./.venv/bin/python -m pip install <paketname>
./.venv/bin/python -m pip freeze > requirements.txt
```

## Verwendung

```bash
./monkkee/process_paypal_report <report.csv>
```

Die Ausgabe (`*_processed.xlsx`) wird im selben Verzeichnis wie die Eingabedatei erzeugt.

### MoneyMoney Monats-Export

```bash
./money_money/export_transactions 2026 05
```

Die Ausgabe wird nach `tmp/accounting/2026/05/transactions.csv` verschoben.

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
./rclone/sync_app_scripts_data
```

Falls dein Remote anders heißt:

```bash
cd /Users/bjoerne/Source/my-office
RCLONE_REMOTE_NAME="meinremote" ./rclone/sync_app_scripts_data
```

Hinweis: Das Skript verwendet `rclone sync` von **remote nach lokal**. Lokale Dateien, die remote nicht existieren, werden dabei entfernt.

