"""MCP-style tool functions for controlled local data access."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src import database


def create_task(title: str, description: str, status: str = "todo", db_path: Path | str | None = None) -> dict[str, Any]:
    """Create a task without exposing SQL to callers."""
    return database.create_task(title=title, description=description, status=status, database_path=db_path)


def list_tasks(status: str | None = None, db_path: Path | str | None = None) -> list[dict[str, Any]]:
    """List tasks, optionally filtered by status."""
    return database.list_tasks(status=status, database_path=db_path)


def search_tasks(query: str, db_path: Path | str | None = None) -> list[dict[str, Any]]:
    """Search tasks by natural-language text."""
    return database.search_tasks(query=query, database_path=db_path)


def complete_task(task_id: int, db_path: Path | str | None = None) -> dict[str, Any]:
    """Mark a task complete."""
    return database.complete_task(task_id=task_id, database_path=db_path)


def delete_task(task_id: int, db_path: Path | str | None = None) -> bool:
    """Delete a task by id."""
    return database.delete_task(task_id=task_id, database_path=db_path)


def list_documents(db_path: Path | str | None = None) -> list[dict[str, Any]]:
    """List document metadata."""
    return database.list_documents(database_path=db_path)


def search_documents(query: str, db_path: Path | str | None = None) -> list[dict[str, Any]]:
    """Search document metadata and content through a safe operation."""
    return database.search_documents(query=query, database_path=db_path)


def get_document(document_id: int, db_path: Path | str | None = None) -> dict[str, Any]:
    """Open a known document by id."""
    return database.get_document(document_id=document_id, database_path=db_path)


def summarize_document_metadata(db_path: Path | str | None = None) -> dict[str, Any]:
    """Return aggregate document metadata."""
    return database.summarize_document_metadata(database_path=db_path)


TOOL_REGISTRY = {
    "create_task": create_task,
    "list_tasks": list_tasks,
    "search_tasks": search_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "list_documents": list_documents,
    "search_documents": search_documents,
    "get_document": get_document,
    "summarize_document_metadata": summarize_document_metadata,
}

