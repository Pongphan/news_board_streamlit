"""SQLite data-access layer for the news board application."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_DATABASE_PATH = PROJECT_DIR / "data" / "news_board.db"
ALLOWED_SECTIONS = ("Section 1", "Section 2", "Section 3")


class DatabaseError(RuntimeError):
    """Raised when a database operation cannot be completed safely."""


@dataclass(frozen=True, slots=True)
class NewsItem:
    """A news item returned from the database."""

    id: int
    section: str
    student_id: str
    news_summary: str
    source_uri: str
    created_at: str


def _database_path(database_path: str | Path | None = None) -> Path:
    return Path(database_path) if database_path is not None else DEFAULT_DATABASE_PATH


def _connect(database_path: str | Path | None = None) -> sqlite3.Connection:
    """Create one short-lived connection per operation.

    A busy timeout and WAL mode make a small Streamlit deployment more tolerant
    of concurrent readers and writers. SQLite still suits a small, single-host app.
    """

    path = _database_path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        connection = sqlite3.connect(path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        connection.execute("PRAGMA journal_mode = WAL")
        return connection
    except sqlite3.Error as exc:
        raise DatabaseError("ไม่สามารถเชื่อมต่อฐานข้อมูลได้") from exc


def initialize_database(database_path: str | Path | None = None) -> None:
    """Create the schema and indexes when the application starts."""

    schema = """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT NOT NULL
                CHECK (section IN ('Section 1', 'Section 2', 'Section 3')),
            student_id TEXT NOT NULL
                CHECK (length(student_id) BETWEEN 4 AND 20),
            news_summary TEXT NOT NULL
                CHECK (length(news_summary) BETWEEN 10 AND 2000),
            source_uri TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_news_created_at
            ON news(created_at DESC, id DESC);
        CREATE INDEX IF NOT EXISTS idx_news_section
            ON news(section);
    """
    try:
        with closing(_connect(database_path)) as connection:
            connection.executescript(schema)
            connection.commit()
    except (sqlite3.Error, OSError) as exc:
        raise DatabaseError("ไม่สามารถเตรียมฐานข้อมูลได้") from exc


def create_news(
    section: str,
    student_id: str,
    news_summary: str,
    source_uri: str,
    database_path: str | Path | None = None,
) -> int:
    """Insert a validated news item and return its generated ID."""

    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    statement = """
        INSERT INTO news (section, student_id, news_summary, source_uri, created_at)
        VALUES (?, ?, ?, ?, ?)
    """
    try:
        with closing(_connect(database_path)) as connection:
            cursor = connection.execute(
                statement,
                (section, student_id, news_summary, source_uri, created_at),
            )
            connection.commit()
            return int(cursor.lastrowid)
    except (sqlite3.Error, OSError) as exc:
        raise DatabaseError("ไม่สามารถบันทึกข่าวได้") from exc


def list_news(
    database_path: str | Path | None = None,
    *,
    section: str | None = None,
    keyword: str = "",
) -> list[NewsItem]:
    """Return newest items first, with optional server-side filtering."""

    clauses: list[str] = []
    parameters: list[str] = []

    if section in ALLOWED_SECTIONS:
        clauses.append("section = ?")
        parameters.append(section)
    if keyword.strip():
        clauses.append("news_summary LIKE ? ESCAPE '\\'")
        escaped = (
            keyword.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        )
        parameters.append(f"%{escaped}%")

    where_clause = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    statement = f"""
        SELECT id, section, student_id, news_summary, source_uri, created_at
        FROM news
        {where_clause}
        ORDER BY created_at DESC, id DESC
    """

    try:
        with closing(_connect(database_path)) as connection:
            rows = connection.execute(statement, parameters).fetchall()
    except (sqlite3.Error, OSError) as exc:
        raise DatabaseError("ไม่สามารถอ่านข่าวจากฐานข้อมูลได้") from exc

    return [NewsItem(**dict(row)) for row in rows]


def count_news(database_path: str | Path | None = None) -> tuple[int, int]:
    """Return total item count and the number of represented sections."""

    statement = "SELECT COUNT(*) AS total, COUNT(DISTINCT section) AS sections FROM news"
    try:
        with closing(_connect(database_path)) as connection:
            row = connection.execute(statement).fetchone()
    except (sqlite3.Error, OSError) as exc:
        raise DatabaseError("ไม่สามารถอ่านสถิติข่าวได้") from exc
    return int(row["total"]), int(row["sections"])
