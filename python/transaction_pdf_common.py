from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

PURPOSE_FIELD_LABELS = {
    "Umsatzart": "Umsatzart",
    "Referenz": "Referenznummer",
    "Mandat": "Mandatsnummer",
    "Gläubiger-ID": "Gläubiger-ID",
}

PURPOSE_FIELD_PATTERN = re.compile(r",\s*(Umsatzart|Referenz|Mandat|Gläubiger-ID):\s*")
DATE_FIELD_LABELS = ("Datum", "Buchungstag")
ACCOUNT_NAME_FIELD_LABELS = ("Kontobezeichnung",)


def normalize_nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def read_transactions(csv_path: Path) -> tuple[list[str], list[list[str]]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=";")

        try:
            header = next(reader)
        except StopIteration as exc:
            raise RuntimeError(f"Leere CSV-Datei: {csv_path}") from exc

        rows = [row for row in reader if row and any(cell.strip() for cell in row)]

    if not rows:
        raise RuntimeError(f"Keine Transaktionen in {csv_path} gefunden")

    return header, rows


def require_single_transaction(csv_path: Path) -> tuple[list[str], list[str]]:
    header, rows = read_transactions(csv_path)
    if len(rows) != 1:
        raise RuntimeError(
            f"Erwartet genau eine Buchung in {csv_path}, gefunden: {len(rows)}"
        )
    return header, rows[0]


def find_first_column_value(header: list[str], row: list[str], supported_labels: tuple[str, ...]) -> str:
    for label in supported_labels:
        if label in header:
            column_index = header.index(label)
            if column_index < len(row):
                return row[column_index].strip()

    return row[0].strip() if row else ""


def find_optional_column_value(header: list[str], row: list[str], supported_labels: tuple[str, ...]) -> str | None:
    for label in supported_labels:
        if label in header:
            column_index = header.index(label)
            if column_index < len(row):
                value = row[column_index].strip()
                return value or None

    return None


def transaction_pdf_path(header: list[str], target_dir: Path, row: list[str], index: int) -> Path:
    booking_date = find_first_column_value(header, row, DATE_FIELD_LABELS)
    booking_date_slug = booking_date.replace(".", "-") if booking_date else f"row-{index:03d}"
    filename = f"transaction-{booking_date_slug}-{index:03d}.pdf"
    return target_dir / filename


def parse_purpose_details(purpose: str) -> tuple[str, dict[str, str]]:
    normalized_purpose = purpose.strip()
    matches = list(PURPOSE_FIELD_PATTERN.finditer(normalized_purpose))

    if not matches:
        return normalized_purpose, {}

    description = normalized_purpose[: matches[0].start()].strip(" ,")
    parsed_fields: dict[str, str] = {}

    for index, match in enumerate(matches):
        source_label = match.group(1)
        value_start = match.end()
        value_end = matches[index + 1].start() if index + 1 < len(matches) else len(normalized_purpose)
        value = normalized_purpose[value_start:value_end].strip(" ,")
        target_label = PURPOSE_FIELD_LABELS[source_label]
        parsed_fields[target_label] = value

    return description, parsed_fields


def build_table_data(header: list[str], row: list[str], account_name: str | None = None) -> list[list[str]]:
    pairs: list[list[str]] = []
    if account_name:
        pairs.append(["Konto", normalize_nfc(account_name)])

    for key, value in zip(header, row):
        if key in ACCOUNT_NAME_FIELD_LABELS:
            continue
        if key == "Verwendungszweck":
            description, parsed_fields = parse_purpose_details(value or "")

            if description and description != (value or ""):
                pairs.append(["Verwendungszweck", normalize_nfc(description)])

            for label in ("Umsatzart", "Referenznummer", "Mandatsnummer", "Gläubiger-ID"):
                if label in parsed_fields:
                    pairs.append([label, normalize_nfc(parsed_fields[label])])
        else:
            pairs.append([key, normalize_nfc(value or "")])

    return pairs


def make_table(table_data: list[list[str]]) -> Table:
    table = Table(table_data, colWidths=[55 * mm, 115 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f0f0f0")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("LEADING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def write_transaction_pdf(
    output_path: Path,
    header: list[str],
    row: list[str],
    billing_filename: str | None = None,
    description: str | None = None,
    account_name: str | None = None,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    story = [
        Paragraph("Buchung", styles["Title"]),
        Spacer(1, 8 * mm),
    ]

    summary_rows: list[list[str]] = []
    if billing_filename:
        summary_rows.append(["Rechnung", normalize_nfc(billing_filename)])
    if description:
        summary_rows.append(["Leistungsinhalt", normalize_nfc(description)])

    if summary_rows:
        story.append(make_table(summary_rows))
        story.append(Spacer(1, 6 * mm))

    story.append(make_table(build_table_data(header, row, account_name)))

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="Buchung",
    )
    document.build(story)
