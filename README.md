# Office Scripts

Dieses Repository enthält kleine Office-Automatisierungen.

Aktuell enthalten:

- `monkkee/process_paypal_report`: Verarbeitung von PayPal-CSV-Reports und Umwandlung in Excel.
- `money_money/export_transactions`: Exportiert Monatsumsätze aus MoneyMoney und verschiebt die CSV nach `tmp/accounting/<jahr>/<monat>/transactions.csv`.
- `rclone/sync_app_scripts_data`: Synchronisiert `tmp/app_scripts_data` bidirektional mit Google Drive.

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

Danach z.B. `gdrive` als Remote anlegen und den ersten Sync mit `--resync` starten:

```bash
cd /Users/bjoerne/Source/my-office
./rclone/sync_app_scripts_data gdrive:app_scripts_data --resync
```

Spätere Läufe:

```bash
cd /Users/bjoerne/Source/my-office
RCLONE_REMOTE_PATH="gdrive:app_scripts_data" ./rclone/sync_app_scripts_data
```

