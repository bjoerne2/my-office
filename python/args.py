from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")


def validate_year_month(year_value: str, month_value: str, *, example: str = "2026 01") -> tuple[int, int]:
    try:
        year = int(year_value)
        month = int(month_value)
    except ValueError as exc:
        raise ValueError(f"Jahr und Monat müssen numerisch sein, z.B. {example}") from exc

    if year < 1900 or year > 9999:
        raise ValueError(f"Ungültiges Jahr: {year}")

    if month < 1 or month > 12:
        raise ValueError(f"Ungültiger Monat: {month}")

    return year, month


def validate_vendor(vendor_value: str, resolver: Callable[[str], T]) -> T:
    return resolver(vendor_value.strip().lower())


def validate_staging_folder_name(folder_value: str) -> str:
    folder_name = folder_value.strip()
    if not folder_name:
        raise ValueError("Ordnername darf nicht leer sein")

    if folder_name in {".", ".."} or "/" in folder_name or "\\" in folder_name:
        raise ValueError("Ordnername muss ohne Pfadangabe übergeben werden")

    return folder_name


