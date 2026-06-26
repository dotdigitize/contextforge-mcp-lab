# ContextForge MCP Lab

## Overview

ContextForge MCP Lab is a local MCP-style data access server for working with task records and seeded documents through controlled tool functions. It uses Python, SQLite, JSON seed manifests, and sample text files to model how an AI-facing tool layer can expose useful application actions without exposing unrestricted database access.

The project is intentionally small: it provides a reproducible local database, a command-line tool dispatcher, and tests around the task and document workflows.

## Features

- MCP-style named tool interface
- SQLite database with `tasks` and `documents` tables
- JSON-based seed data for repeatable local setup
- Seeded sample documents loaded from text files
- Controlled task and document functions
- Input validation for IDs, statuses, search terms, titles, and descriptions
- Parameterized SQLite queries
- Configurable database path through `.env`
- Pytest coverage for database setup, seed loading, tool behavior, validation, and unknown tool rejection

## Architecture

ContextForge MCP Lab is organized into a small set of layers:

- MCP-style tool interface: `src/server.py` dispatches named JSON-compatible tool calls, and `src/tools.py` exposes the registered task and document functions.
- Python service layer: tool functions validate the callable surface and delegate workflow-specific behavior to the database module.
- SQLite persistence layer: `src/database.py` owns schema creation, reads, writes, updates, deletes, and search queries.
- Seeded sample files: `data/*.json` defines seed metadata, while `sample_files/*.txt` provides document bodies.
- Tests: `tests/` verifies database initialization, seed behavior, tool calls, validation, and rejection of unregistered tools.

## Tools

Task functions:

- `create_task(title, description, status="todo")`
- `list_tasks(status=None)`
- `search_tasks(query)`
- `complete_task(task_id)`
- `delete_task(task_id)`

Document functions:

- `list_documents()`
- `search_documents(query)`
- `get_document(document_id)`
- `summarize_document_metadata()`

## Data Model

The `tasks` table stores local task records:

- `id`: auto-incrementing integer primary key
- `title`: required task title
- `description`: required task description
- `status`: one of `todo`, `in_progress`, or `done`
- `created_at`: UTC timestamp
- `completed_at`: UTC timestamp set when a task is completed

The `documents` table stores seeded document metadata and content:

- `id`: auto-incrementing integer primary key
- `filename`: unique source filename
- `title`: document title
- `category`: document category
- `summary`: short document summary
- `content`: full text loaded from `sample_files/`
- `created_at`: UTC timestamp

## Installation

```bash
cd contextforge-mcp-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional environment setup:

```bash
cp .env.example .env
```

The default database path is `data/contextforge.db`.

## Seeding the Demo Database

```bash
python -m src.seed_data
```

This rebuilds the demo database with five task records and five documents loaded from `sample_files/`.

## Running Tests

```bash
python -m pytest
```

## Example Usage

Call tools through the local command dispatcher:

```bash
python -m src.server list_tasks
python -m src.server search_documents --args '{"query": "maintenance"}'
python -m src.server create_task --args '{"title": "Capture demo screenshot", "description": "Save terminal output showing seeded data and passing tests."}'
python -m src.server complete_task --args '{"task_id": 1}'
```

The same functions can be called directly from Python:

```python
from src.server import call_tool

tasks = call_tool("list_tasks")
matches = call_tool("search_documents", {"query": "policy"})
task = call_tool(
    "create_task",
    {
        "title": "Review document metadata",
        "description": "Check seeded document categories and summaries.",
    },
)
completed = call_tool("complete_task", {"task_id": task["id"]})
```

## Security Notes

- There is no raw SQL tool.
- Callers can only use registered task and document functions.
- SQLite access uses parameterized queries.
- Input validation is applied before database operations.
- The repository contains demo data only.
- The sample files are fictional and do not contain personal data.

## Project Structure

```text
contextforge-mcp-lab/
  README.md
  SETUP.md
  PORTFOLIO_WRITEUP.md
  LICENSE
  requirements.txt
  pyproject.toml
  src/
    server.py
    database.py
    tools.py
    config.py
    seed_data.py
  tests/
    test_database.py
    test_tools.py
  docs/
    ARCHITECTURE.md
    DEMO_PLAN.md
  sample_files/
    marketing_campaign_notes.txt
    server_maintenance_log.txt
    customer_support_policy.txt
    research_brief_llm_evals.txt
    project_meeting_summary.txt
  data/
    sample_tasks.json
    sample_documents.json
```

## Roadmap

- Real MCP client integration
- FastAPI demo layer
- Rate limiting for hosted demo endpoints
- GitHub Actions test workflow
- Containerized deployment
