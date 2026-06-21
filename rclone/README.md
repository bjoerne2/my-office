# rclone-Sync für `app_scripts_data`

Dieses Verzeichnis enthält ein Skript, das `tmp/app_scripts_data` mit einem Google-Drive-Ordner **in beide Richtungen** synchronisiert.

## Dateien

- `sync_app_scripts_data` – bidirektionaler Sync via `rclone bisync`

## Was synchronisiert wird

- **Lokal:** `tmp/app_scripts_data`
- **Remote:** ein frei wählbarer `rclone`-Pfad, z.B. `gdrive:app_scripts_data`

## rclone unter macOS installieren

`rclone` ist aktuell noch nicht installiert. Die folgenden Schritte kannst du nach der Installation des Scripts selbst ausführen.

### Installation mit Homebrew

```bash
brew update
brew install rclone
```

### Installation prüfen

```bash
rclone version
```

## Google Drive als Remote einrichten

```bash
rclone config
```

Empfohlener Ablauf im Dialog:

1. `n` für **new remote**
2. Name vergeben, z.B. `gdrive`
3. Storage-Typ `drive` auswählen
4. Standard-Client-ID/Secret verwenden, falls du keine eigenen OAuth-Credentials hast
5. Scope in der Regel auf `drive` lassen
6. Auto-Config im Browser bestätigen
7. Am Ende mit `y` speichern

Danach kannst du prüfen, ob der Remote erreichbar ist:

```bash
rclone lsd gdrive:
```

## Zielordner in Google Drive vorbereiten

Wenn der Zielordner noch nicht existiert, kannst du ihn z.B. so anlegen:

```bash
rclone mkdir gdrive:app_scripts_data
```

## Skript ausführbar machen

Falls nötig:

```bash
chmod +x /Users/bjoerne/Source/my-office/rclone/sync_app_scripts_data
```

## Erster Sync

Beim **ersten** bidirektionalen Lauf ist `--resync` sinnvoll, damit `rclone bisync` einen sauberen Ausgangszustand erzeugt.

### Variante 1: Remote direkt als Argument übergeben

```bash
cd /Users/bjoerne/Source/my-office
./rclone/sync_app_scripts_data gdrive:app_scripts_data --resync
```

### Variante 2: Remote über Umgebungsvariable setzen

```bash
cd /Users/bjoerne/Source/my-office
RCLONE_REMOTE_PATH="gdrive:app_scripts_data" ./rclone/sync_app_scripts_data --resync
```

## Normale spätere Syncs

Nach dem ersten erfolgreichen Lauf reicht normalerweise:

```bash
cd /Users/bjoerne/Source/my-office
RCLONE_REMOTE_PATH="gdrive:app_scripts_data" ./rclone/sync_app_scripts_data
```

## Optional: Testlauf ohne Änderungen

```bash
cd /Users/bjoerne/Source/my-office
RCLONE_REMOTE_PATH="gdrive:app_scripts_data" ./rclone/sync_app_scripts_data --dry-run
```

## Logs und Arbeitsdaten

Das Skript legt folgende lokale Hilfsdaten an:

- `rclone/logs/` – Logdateien pro Lauf
- `rclone/.bisync/` – Arbeitsdaten von `rclone bisync`

## Wichtige Hinweise

- Verwende **nicht** `rclone sync`, wenn du in beide Richtungen synchronisieren willst.
- Wenn du lokal und remote parallel viele Änderungen vorgenommen hast und `bisync` Konflikte meldet, kann ein erneuter Lauf mit `--resync` sinnvoll sein.
- `tmp/` ist bereits im Repository ignoriert; deine eigentlichen Sync-Daten werden also nicht versehentlich committed.

