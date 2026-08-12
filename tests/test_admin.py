import csv
import io

from admin_auth import DEFAULT_ADMIN_PASSWORD_HASH, verify_admin_password
from admin_export import news_to_csv
from database import NewsItem


def test_requested_admin_password_is_accepted():
    assert verify_admin_password("isai12admin", DEFAULT_ADMIN_PASSWORD_HASH)
    assert not verify_admin_password("incorrect", DEFAULT_ADMIN_PASSWORD_HASH)


def test_admin_csv_contains_full_data_and_blocks_formula_injection():
    item = NewsItem(
        id=7,
        section="Section 2",
        student_id="6612345678",
        news_summary="=DANGEROUS_FORMULA",
        source_uri="https://example.org/source",
        created_at="2026-08-12T01:02:03+00:00",
        status="hidden",
        moderated_at="2026-08-12T02:03:04+00:00",
    )

    exported = news_to_csv([item]).decode("utf-8-sig")
    row = next(csv.DictReader(io.StringIO(exported)))

    assert row["student_id"] == "6612345678"
    assert row["status"] == "hidden"
    assert row["news_summary"] == "'=DANGEROUS_FORMULA"
