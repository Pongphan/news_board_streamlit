"""CSV export helper kept separate from Streamlit for straightforward testing."""

from __future__ import annotations

import csv
import io
from collections.abc import Iterable

from database import NewsItem


EXPORT_FIELDS = (
    "id",
    "section",
    "student_id",
    "news_summary",
    "source_uri",
    "created_at",
    "status",
    "moderated_at",
)


def _safe_cell(value: object) -> object:
    """Prevent spreadsheet applications from evaluating exported text as formulas."""

    if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
        return f"'{value}"
    return value


def news_to_csv(items: Iterable[NewsItem]) -> bytes:
    """Create an Excel-friendly UTF-8 CSV containing the full administrative data."""

    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=EXPORT_FIELDS)
    writer.writeheader()
    for item in items:
        writer.writerow({field: _safe_cell(getattr(item, field)) for field in EXPORT_FIELDS})
    return ("\ufeff" + output.getvalue()).encode("utf-8")
