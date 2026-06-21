# MoneyMoney-Skripte

Dieses Verzeichnis enthält Hilfsskripte für Exporte aus MoneyMoney.

## Dateien

- `applescript/transactions.applescript` – exportiert Umsätze für einen Datumsbereich
- `applescript/accounts.applescript` – exportiert Konten
- `export_transactions` – Python-Wrapper für Monats-Exporte

## Direkter AppleScript-Aufruf

```bash
osascript /Users/bjoerne/Source/my-office/money_money/applescript/transactions.applescript 2026-05-01 2026-05-31
```

MoneyMoney gibt dabei den Pfad der erzeugten CSV auf `stdout` zurück.

## Python-Wrapper

```bash
/Users/bjoerne/Source/my-office/money_money/export_transactions 2026 05
```

Der Wrapper:

1. berechnet `2026-05-01` und `2026-05-31`
2. ruft das AppleScript auf
3. verschiebt die erzeugte Datei nach
   `tmp/accounting/2026/05/transactions.csv`

