# Office Scripts

Dieses Repository enthält kleine Office-Automatisierungen.

Aktuell enthalten:

- `monkkee/process_paypal_report`: Verarbeitung von PayPal-CSV-Reports und Umwandlung in Excel.

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
