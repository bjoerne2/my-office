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
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Hinweis: In jeder neuen Shell-Session vor der Arbeit im Projekt aktivieren:

```bash
cd /Users/bjoerne/Source/my-office
source .venv/bin/activate
```

## Abhängigkeiten aktualisieren

Wenn neue Pakete hinzukommen:

```bash
python -m pip install <paketname>
python -m pip freeze > requirements.txt
```

## Verwendung

```bash
./monkkee/process_paypal_report <report.csv>
```

Die Ausgabe (`*_processed.xlsx`) wird im selben Verzeichnis wie die Eingabedatei erzeugt.
