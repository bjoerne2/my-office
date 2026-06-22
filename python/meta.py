from __future__ import annotations

import json
from pathlib import Path
from typing import Any


META_FILENAME = "meta.json"


def meta_path(target_dir: Path) -> Path:
    return target_dir / META_FILENAME


def read_meta(target_dir: Path) -> dict[str, Any]:
    path = meta_path(target_dir)
    if not path.is_file():
        return {}

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}

    return data if isinstance(data, dict) else {}


def write_meta(target_dir: Path, data: dict[str, Any]) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    path = meta_path(target_dir)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return path


def set_meta_value(target_dir: Path, key: str, value: Any) -> Path:
    data = read_meta(target_dir)
    data[key] = value
    return write_meta(target_dir, data)


def require_meta(target_dir: Path) -> dict[str, Any]:
    path = meta_path(target_dir)
    data = read_meta(target_dir)
    if not data:
        raise RuntimeError(f"meta.json nicht gefunden oder ungültig: {path}")
    return data


def require_meta_string(target_dir: Path, key: str) -> str:
    data = require_meta(target_dir)
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"{key} fehlt in meta.json")
    return value.strip()

