import sqlite3

import pytest

from database import (
    count_news_by_status,
    create_news,
    delete_news,
    initialize_database,
    list_news,
    list_news_for_admin,
    update_news_status,
)


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
    assert rows[0].status == "published"
    assert rows[0].moderated_at is None


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


def test_existing_database_is_migrated_without_losing_records(tmp_path):
    database_path = tmp_path / "legacy.db"
    with sqlite3.connect(database_path) as connection:
        connection.executescript(
            """
            CREATE TABLE news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section TEXT NOT NULL,
                student_id TEXT NOT NULL,
                news_summary TEXT NOT NULL,
                source_uri TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            INSERT INTO news (section, student_id, news_summary, source_uri, created_at)
            VALUES ('Section 1', '6612345678', 'A legacy academic news summary.',
                    'https://example.org/legacy', '2026-01-01T00:00:00+00:00');
            """
        )

    initialize_database(database_path)
    records = list_news_for_admin(database_path)

    assert len(records) == 1
    assert records[0].status == "published"
    assert records[0].moderated_at is None


def test_moderation_visibility_restore_and_delete(tmp_path):
    database_path = tmp_path / "moderation.db"
    initialize_database(database_path)
    first_id = create_news(**sample_news(), database_path=database_path)
    second_id = create_news(
        **sample_news(section="Section 2", student_id="6712345678"),
        database_path=database_path,
    )

    assert count_news_by_status(database_path) == (2, 2, 0)
    assert update_news_status(first_id, "hidden", database_path)
    assert [item.id for item in list_news(database_path)] == [second_id]
    assert [item.id for item in list_news_for_admin(database_path, status="hidden")] == [first_id]
    assert count_news_by_status(database_path) == (2, 1, 1)

    assert update_news_status(first_id, "published", database_path)
    assert len(list_news(database_path)) == 2
    assert delete_news(first_id, database_path)
    assert [item.id for item in list_news_for_admin(database_path)] == [second_id]
    assert not delete_news(9999, database_path)
