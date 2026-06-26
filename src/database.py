"""SQLite data access layer with controlled operations only."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from src.config import get_settings


VALID_TASK_STATUSES = {"todo", "in_progress", "done"}
MAX_TITLE_LENGTH = 160
MAX_DESCRIPTION_LENGTH = 2_000
MAX_SEARCH_LENGTH = 120


class DatabaseError(RuntimeError):
    """Raised when a database operation cannot be completed."""


def utc_now() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_database_path(database_path: Path | str | None = None) -> Path:
    """Resolve the configured database path."""
    if database_path is None:
        return get_settings().database_path
    return Path(database_path)


@contextmanager
def get_connection(database_path: Path | str | None = None) -> Iterator[sqlite3.Connection]:
    """Open a SQLite connection configured for dictionary-like row access."""
    path = get_database_path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as exc:
        conn.rollback()
        raise DatabaseError(str(exc)) from exc
    finally:
        conn.close()


def initialize_database(database_path: Path | str | None = None) -> None:
    """Create database tables if they do not exist."""
    with get_connection(database_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('todo', 'in_progress', 'done')),
                created_at TEXT NOT NULL,
                completed_at TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                summary TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def reset_database(database_path: Path | str | None = None) -> None:
    """Drop and recreate the local demo database."""
    with get_connection(database_path) as conn:
        conn.execute("DROP TABLE IF EXISTS tasks")
        conn.execute("DROP TABLE IF EXISTS documents")
    initialize_database(database_path)


def _validate_text(value: str, field: str, max_length: int) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field} is required")
    if len(cleaned) > max_length:
        raise ValueError(f"{field} must be {max_length} characters or fewer")
    return cleaned


def _validate_status(status: str) -> str:
    cleaned = status.strip()
    if cleaned not in VALID_TASK_STATUSES:
        raise ValueError(f"status must be one of: {', '.join(sorted(VALID_TASK_STATUSES))}")
    return cleaned


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(row)


def create_task(
    title: str,
    description: str,
    status: str = "todo",
    database_path: Path | str | None = None,
) -> dict[str, Any]:
    """Create a task through a constrained insert operation."""
    clean_title = _validate_text(title, "title", MAX_TITLE_LENGTH)
    clean_description = _validate_text(description, "description", MAX_DESCRIPTION_LENGTH)
    clean_status = _validate_status(status)
    created_at = utc_now()
    completed_at = created_at if clean_status == "done" else None

    with get_connection(database_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO tasks (title, description, status, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (clean_title, clean_description, clean_status, created_at, completed_at),
        )
        task_id = int(cursor.lastrowid)
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise DatabaseError("created task could not be read back")
    return _row_to_dict(row)


def list_tasks(
    status: str | None = None,
    database_path: Path | str | None = None,
) -> list[dict[str, Any]]:
    """List tasks, optionally constrained by status."""
    parameters: tuple[Any, ...] = ()
    query = "SELECT * FROM tasks"
    if status is not None:
        query += " WHERE status = ?"
        parameters = (_validate_status(status),)
    query += " ORDER BY id"

    with get_connection(database_path) as conn:
        rows = conn.execute(query, parameters).fetchall()
    return [_row_to_dict(row) for row in rows]


def search_tasks(query: str, database_path: Path | str | None = None) -> list[dict[str, Any]]:
    """Search task titles and descriptions."""
    clean_query = _validate_text(query, "query", MAX_SEARCH_LENGTH)
    like_query = f"%{clean_query}%"
    with get_connection(database_path) as conn:
        rows = conn.execute(
            """
            SELECT * FROM tasks
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY id
            """,
            (like_query, like_query),
        ).fetchall()
    return [_row_to_dict(row) for row in rows]


def complete_task(task_id: int, database_path: Path | str | None = None) -> dict[str, Any]:
    """Mark a task complete."""
    if task_id < 1:
        raise ValueError("task_id must be a positive integer")
    completed_at = utc_now()
    with get_connection(database_path) as conn:
        cursor = conn.execute(
            "UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?",
            ("done", completed_at, task_id),
        )
        if cursor.rowcount == 0:
            raise LookupError(f"task {task_id} was not found")
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise DatabaseError("completed task could not be read back")
    return _row_to_dict(row)


def delete_task(task_id: int, database_path: Path | str | None = None) -> bool:
    """Delete a task by id."""
    if task_id < 1:
        raise ValueError("task_id must be a positive integer")
    with get_connection(database_path) as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cursor.rowcount == 0:
        raise LookupError(f"task {task_id} was not found")
    return True


def create_document(
    filename: str,
    title: str,
    category: str,
    summary: str,
    content: str,
    database_path: Path | str | None = None,
) -> dict[str, Any]:
    """Create or replace document metadata and content from trusted seed files."""
    clean_filename = _validate_text(filename, "filename", 240)
    clean_title = _validate_text(title, "title", MAX_TITLE_LENGTH)
    clean_category = _validate_text(category, "category", 80)
    clean_summary = _validate_text(summary, "summary", 500)
    clean_content = _validate_text(content, "content", 20_000)
    created_at = utc_now()

    with get_connection(database_path) as conn:
        conn.execute(
            """
            INSERT INTO documents (filename, title, category, summary, content, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(filename) DO UPDATE SET
                title = excluded.title,
                category = excluded.category,
                summary = excluded.summary,
                content = excluded.content,
                created_at = excluded.created_at
            """,
            (clean_filename, clean_title, clean_category, clean_summary, clean_content, created_at),
        )
        row = conn.execute("SELECT * FROM documents WHERE filename = ?", (clean_filename,)).fetchone()
    if row is None:
        raise DatabaseError("created document could not be read back")
    return _row_to_dict(row)


def list_documents(database_path: Path | str | None = None) -> list[dict[str, Any]]:
    """List document metadata without returning full content."""
    with get_connection(database_path) as conn:
        rows = conn.execute(
            """
            SELECT id, filename, title, category, summary, created_at
            FROM documents
            ORDER BY id
            """
        ).fetchall()
    return [_row_to_dict(row) for row in rows]


def search_documents(query: str, database_path: Path | str | None = None) -> list[dict[str, Any]]:
    """Search document metadata and content through a controlled query."""
    clean_query = _validate_text(query, "query", MAX_SEARCH_LENGTH)
    like_query = f"%{clean_query}%"
    with get_connection(database_path) as conn:
        rows = conn.execute(
            """
            SELECT id, filename, title, category, summary, created_at
            FROM documents
            WHERE filename LIKE ? OR title LIKE ? OR category LIKE ? OR summary LIKE ? OR content LIKE ?
            ORDER BY id
            """,
            (like_query, like_query, like_query, like_query, like_query),
        ).fetchall()
    return [_row_to_dict(row) for row in rows]


def get_document(document_id: int, database_path: Path | str | None = None) -> dict[str, Any]:
    """Return a complete document by id."""
    if document_id < 1:
        raise ValueError("document_id must be a positive integer")
    with get_connection(database_path) as conn:
        row = conn.execute("SELECT * FROM documents WHERE id = ?", (document_id,)).fetchone()
    if row is None:
        raise LookupError(f"document {document_id} was not found")
    return _row_to_dict(row)


def summarize_document_metadata(database_path: Path | str | None = None) -> dict[str, Any]:
    """Summarize document counts and categories without exposing document bodies."""
    with get_connection(database_path) as conn:
        total = conn.execute("SELECT COUNT(*) AS count FROM documents").fetchone()["count"]
        rows = conn.execute(
            """
            SELECT category, COUNT(*) AS count
            FROM documents
            GROUP BY category
            ORDER BY category
            """
        ).fetchall()
    return {
        "total_documents": total,
        "categories": [_row_to_dict(row) for row in rows],
    }

