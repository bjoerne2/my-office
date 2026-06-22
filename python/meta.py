from __future__ import annotations

import json
from pathlib import Path
from typing import Any


META_FILENAME = "meta.json"
MetaEntry = dict[str, Any]


def meta_path(target_dir: Path) -> Path:
    return target_dir / META_FILENAME


def _normalize_meta_entries(data: Any) -> list[MetaEntry]:
    if isinstance(data, list):
        entries: list[MetaEntry] = []
        for entry in data:
            if not isinstance(entry, dict):
                return []
            entries.append(dict(entry))
        return entries

    if isinstance(data, dict):
        return [dict(data)] if data else []

    return []


def read_meta_entries(target_dir: Path) -> list[MetaEntry]:
    path = meta_path(target_dir)
    if not path.is_file():
        return []

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return []

    return _normalize_meta_entries(data)


def write_meta_entries(target_dir: Path, entries: list[MetaEntry]) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    path = meta_path(target_dir)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return path


def require_meta_entries(target_dir: Path) -> list[MetaEntry]:
    path = meta_path(target_dir)
    entries = read_meta_entries(target_dir)
    if not entries:
        raise RuntimeError(f"meta.json nicht gefunden oder ungültig: {path}")
    return entries


def require_meta_entry_string(entry: MetaEntry, key: str, *, entry_index: int) -> str:
    value = entry.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"{key} fehlt in meta.json Eintrag {entry_index}")
    return value.strip()
