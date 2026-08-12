"""Pure validation helpers shared by the form and automated tests."""

from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit

from database import ALLOWED_SECTIONS


STUDENT_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{4,20}$")


def normalize_uri(value: str) -> str:
    """Return a normalized HTTP(S) URI, or an empty string when invalid."""

    candidate = value.strip()
    try:
        parsed = urlsplit(candidate)
        if parsed.scheme.lower() not in {"http", "https"}:
            return ""
        if not parsed.hostname or any(character.isspace() for character in candidate):
            return ""
        # Accessing port raises ValueError for malformed values such as :abc.
        _ = parsed.port
        return urlunsplit(
            (parsed.scheme.lower(), parsed.netloc, parsed.path, parsed.query, parsed.fragment)
        )
    except (TypeError, ValueError):
        return ""


def validate_news(
    section: str,
    student_id: str,
    news_summary: str,
    source_uri: str,
) -> tuple[dict[str, str], dict[str, str]]:
    """Validate and normalize form input.

    The first result maps field names to language-independent message keys. The
    second result is safe to pass to ``database.create_news`` when no errors exist.
    """

    cleaned = {
        "section": section.strip(),
        "student_id": student_id.strip(),
        "news_summary": news_summary.strip(),
        "source_uri": normalize_uri(source_uri),
    }
    errors: dict[str, str] = {}

    if cleaned["section"] not in ALLOWED_SECTIONS:
        errors["section"] = "invalid_section"
    if not STUDENT_ID_PATTERN.fullmatch(cleaned["student_id"]):
        errors["student_id"] = "invalid_student_id"
    summary_length = len(cleaned["news_summary"])
    if summary_length < 10:
        errors["news_summary"] = "summary_too_short"
    elif summary_length > 2000:
        errors["news_summary"] = "summary_too_long"
    if not cleaned["source_uri"]:
        errors["source_uri"] = "invalid_source_uri"

    return errors, cleaned
