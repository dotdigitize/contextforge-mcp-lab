from __future__ import annotations

import pytest

from src.seed_data import seed_database
from src.server import call_tool
from src.tools import (
    create_task,
    delete_task,
    list_documents,
    list_tasks,
    search_documents,
    summarize_document_metadata,
)


def test_task_tools_create_list_and_delete(tmp_path):
    db_path = tmp_path / "tools.db"
    seed_database(db_path)

    created = create_task(
        "Validate ContextForge MCP Lab demo reset flow",
        "Confirm the demo reset command restores known ContextForge MCP Lab sample data.",
        db_path=db_path,
    )
    assert created["id"] > 5
    assert any(task["title"] == created["title"] for task in list_tasks(db_path=db_path))
    assert delete_task(created["id"], db_path=db_path) is True


def test_document_tools_search_and_metadata(tmp_path):
    db_path = tmp_path / "tools.db"
    seed_database(db_path)

    docs = list_documents(db_path=db_path)
    results = search_documents("maintenance", db_path=db_path)
    metadata = summarize_document_metadata(db_path=db_path)

    assert len(docs) == 5
    assert results[0]["filename"] == "server_maintenance_log.txt"
    assert metadata["total_documents"] == 5
    assert any(category["category"] == "Operations" for category in metadata["categories"])


def test_server_rejects_unknown_tool():
    with pytest.raises(ValueError):
        call_tool("raw_sql_query", {"query": "SELECT * FROM tasks"})
