from __future__ import annotations

import sqlite3

import pytest

from src.database import (
    complete_task,
    create_task,
    get_document,
    initialize_database,
    list_tasks,
    search_tasks,
)
from src.seed_data import seed_database


def test_initialize_database_creates_required_tables(tmp_path):
    db_path = tmp_path / "test.db"
    initialize_database(db_path)

    with sqlite3.connect(db_path) as conn:
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        }

    assert "tasks" in tables
    assert "documents" in tables


def test_create_search_and_complete_task(tmp_path):
    db_path = tmp_path / "test.db"
    initialize_database(db_path)
    task = create_task("Review RAG evaluation metrics", "Compare faithfulness and answer relevance.", database_path=db_path)

    assert task["status"] == "todo"
    assert search_tasks("faithfulness", database_path=db_path)[0]["id"] == task["id"]

    completed = complete_task(task["id"], database_path=db_path)
    assert completed["status"] == "done"
    assert completed["completed_at"] is not None


def test_validation_rejects_empty_task_title(tmp_path):
    db_path = tmp_path / "test.db"
    initialize_database(db_path)

    with pytest.raises(ValueError):
        create_task("", "Missing title should fail.", database_path=db_path)


def test_seed_database_loads_realistic_sample_data(tmp_path):
    db_path = tmp_path / "seeded.db"
    seed_database(db_path)

    tasks = list_tasks(database_path=db_path)
    first_doc = get_document(1, database_path=db_path)

    assert len(tasks) == 5
    assert "RAG" in tasks[0]["title"]
    assert first_doc["filename"].endswith(".txt")
    assert len(first_doc["content"].splitlines()) > 5

