from __future__ import annotations

from pathlib import Path

from pypdf import PdfWriter

from python.meta import require_meta_entry_string


def merge_pdfs(receipt_pdf: Path, transaction_pdf: Path, output_pdf: Path) -> None:
    writer = PdfWriter()

    for source_path in (receipt_pdf, transaction_pdf):
        writer.append(str(source_path))

    with output_pdf.open("wb") as handle:
        writer.write(handle)

    writer.close()


def resolve_pdf_from_meta(target_dir: Path, entry: dict[str, str], key: str, label: str, entry_index: int) -> Path:
    filename = require_meta_entry_string(entry, key, entry_index=entry_index)
    pdf_path = target_dir / filename
    if not pdf_path.is_file():
        raise RuntimeError(f"{label} nicht gefunden: {pdf_path}")

    return pdf_path

