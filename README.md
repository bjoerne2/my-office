# PayPal Report Processor

Kleines CLI-Tool zur Verarbeitung von PayPal-CSV-Reports und Umwandlung in Excel.

## Voraussetzungen

- Python ≥ 3.10 (z.B. installiert über Homebrew)
- pip

## Python Installation (Homebrew)

```bash
brew install python
```

## Python Update (Homebrew)

```bash
brew update
brew upgrade python
```

## Abhängigkeiten installieren

```bash
pip3 install pandas openpyxl
```

## Verwendung

```bash
./monkkee/process_paypal_report <report.csv>
```

Die Ausgabe (`*_processed.xlsx`) wird im selben Verzeichnis wie die Eingabedatei erzeugt.
