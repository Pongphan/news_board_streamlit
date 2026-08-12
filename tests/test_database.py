import sqlite3

import pytest

from database import create_news, initialize_database, list_news


def sample_news(**overrides):
    payload = {
        "section": "Section 1",
        "student_id": "6612345678",
        "news_summary": "ข่าวทดสอบเกี่ยวกับกิจกรรมใหม่ของมหาวิทยาลัย",
        "source_uri": "https://example.com/campus-news",
    }
    payload.update(overrides)
    return payload


def test_initialize_and_create_news(tmp_path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)

    news_id = create_news(**sample_news(), database_path=database_path)
    rows = list_news(database_path)

    assert news_id == 1
    assert len(rows) == 1
    assert rows[0].section == "Section 1"
    assert rows[0].student_id == "6612345678"
    assert rows[0].created_at.endswith("+00:00")


def test_list_news_filters_section_and_escapes_like_wildcards(tmp_path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    create_news(**sample_news(news_summary="ข่าวกิจกรรม 100% สำหรับ Section 1"), database_path=database_path)
    create_news(
        **sample_news(section="Section 2", news_summary="ข่าวกิจกรรมทั่วไปสำหรับ Section 2"),
        database_path=database_path,
    )

    section_rows = list_news(database_path, section="Section 2")
    percent_rows = list_news(database_path, keyword="100%")

    assert [row.section for row in section_rows] == ["Section 2"]
    assert len(percent_rows) == 1
    assert "100%" in percent_rows[0].news_summary


def test_database_constraint_rejects_unknown_section(tmp_path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)

    with pytest.raises(sqlite3.IntegrityError):
        with sqlite3.connect(database_path) as connection:
            connection.execute(
                """
                INSERT INTO news (section, student_id, news_summary, source_uri, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                ("Section 9", "6612345678", "สรุปข่าวที่มีความยาวเพียงพอ", "https://example.com", "2026-01-01T00:00:00+00:00"),
            )
