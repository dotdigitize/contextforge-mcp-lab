"""Seed the ContextForge MCP Lab demo database with realistic sample data."""

from __future__ import annotations

import json
from pathlib import Path

from src.config import PROJECT_ROOT, get_settings
from src.database import create_document, create_task, reset_database


TASKS_PATH = PROJECT_ROOT / "data" / "sample_tasks.json"
DOCUMENTS_PATH = PROJECT_ROOT / "data" / "sample_documents.json"
SAMPLE_FILES_DIR = PROJECT_ROOT / "sample_files"


def seed_database(database_path: Path | str | None = None) -> None:
    """Rebuild the demo database from structured JSON and text files."""
    db_path = Path(database_path) if database_path is not None else get_settings().database_path
    reset_database(db_path)

    tasks = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    for task in tasks:
        create_task(
            title=task["title"],
            description=task["description"],
            status=task.get("status", "todo"),
            database_path=db_path,
        )

    documents = json.loads(DOCUMENTS_PATH.read_text(encoding="utf-8"))
    for document in documents:
        content = (SAMPLE_FILES_DIR / document["filename"]).read_text(encoding="utf-8")
        create_document(
            filename=document["filename"],
            title=document["title"],
            category=document["category"],
            summary=document["summary"],
            content=content,
            database_path=db_path,
        )


def main() -> None:
    settings = get_settings()
    seed_database(settings.database_path)
    print(f"Seeded ContextForge demo database at {settings.database_path}")


if __name__ == "__main__":
    main()

