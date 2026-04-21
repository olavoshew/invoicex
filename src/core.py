import csv
import re
from dataclasses import dataclass, fields
from pathlib import Path

import pdfplumber


@dataclass
class InvoiceResult:
    filename: str
    vendor: str | None
    invoice_number: str | None
    date: str | None
    total: str | None
    gst: str | None


_INVOICE_NUMBER_PATTERNS = [
    r"(?i)invoice\s*(?:no\.?|num(?:ber)?|#)[\s:]*([A-Z0-9/_-]+)",
    r"(?i)inv[\s:]*#?\s*([A-Z0-9/_-]+)",
]

_DATE_PATTERNS = [
    r"\b(\d{1,2}/\d{1,2}/\d{4})\b",
    r"\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b",
    r"\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b",
    r"\b(\d{4}-\d{2}-\d{2})\b",
]

_TOTAL_PATTERNS = [
    r"(?i)(?:total|amount\s+due|balance\s+due)(?:\s+inc\.?\s*gst?)?\s*:?\s*\$?\s*([\d,]+\.?\d*)",
    r"(?i)grand\s+total\s*:?\s*\$?\s*([\d,]+\.?\d*)",
]

_GST_PATTERNS = [
    r"(?im)^gst\s*:?\s*\$?\s*([\d,]+\.?\d*)",
    r"(?im)^tax\s*:?\s*\$?\s*([\d,]+\.?\d*)",
]


def _parse_field(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None


def _parse_vendor(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not re.match(r"^[\d\s\W]+$", stripped) and len(stripped) > 2:
            return stripped
    return None


def find_pdfs(folder: Path) -> list[Path]:
    return sorted(
        path for path in folder.iterdir() if path.is_file() and path.suffix.lower() == ".pdf"
    )


def extract_invoice(pdf_path: Path) -> InvoiceResult:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )
    except Exception as exc:
        raise ValueError(
            f"Could not read {pdf_path.name} -- the file may be corrupt or encrypted. ({exc})"
        )

    return InvoiceResult(
        filename=pdf_path.name,
        vendor=_parse_vendor(text),
        invoice_number=_parse_field(text, _INVOICE_NUMBER_PATTERNS),
        date=_parse_field(text, _DATE_PATTERNS),
        total=_parse_field(text, _TOTAL_PATTERNS),
        gst=_parse_field(text, _GST_PATTERNS),
    )


def write_csv(results: list[InvoiceResult], output_path: Path, columns: list[str]) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for result in results:
            writer.writerow(
                {field.name: getattr(result, field.name) for field in fields(result)}
            )
