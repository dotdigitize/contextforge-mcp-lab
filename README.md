# ContextForge MCP Lab

ContextForge MCP Lab is a professional AI infrastructure portfolio project that shows how an AI system can interact with local structured data through controlled tools instead of unrestricted database access.

The project implements a local MCP-style Python server backed by SQLite, structured JSON seed data, and realistic sample text files. It is designed to demonstrate safe tool boundaries, reproducible demo data, and practical testing for AI-agent infrastructure.

## Why the Name ContextForge MCP Lab Matters

"ContextForge" describes the core idea: turning local files, tasks, and structured records into useful AI context. "MCP Lab" signals that this is an experimental but concrete Model Context Protocol-style environment where tool access is explicit, testable, and limited.

The name is intentionally specific. ContextForge MCP Lab is a small infrastructure lab for showing how controlled context access can be designed, seeded, tested, and explained.

## What MCP Is

MCP stands for Model Context Protocol. It is a pattern for connecting AI systems to external context and tools through defined interfaces. Instead of giving a model broad access to a machine, database, or application, an MCP server exposes specific actions the AI system is allowed to request.

In this project, the MCP-style tools are Python functions such as `list_tasks`, `search_documents`, and `complete_task`. They use safe database functions internally and do not expose raw SQL.

## Why This Project Matters

AI agents become risky when they are connected directly to private systems without clear boundaries. A controlled tool layer makes it easier to decide what an agent can do, validate inputs, test behavior, audit outputs, and build public demos without exposing sensitive access.

ContextForge MCP Lab demonstrates that pattern with a small but realistic local dataset.

## Features

- Python MCP-style tool server
- SQLite database with `tasks` and `documents` tables
- Realistic seeded task records
- Realistic sample document files
- JSON seed manifests for repeatable demo rebuilds
- Safe controlled functions for all data access
- No raw SQL tool and no arbitrary query endpoint
- Configurable database path through `.env`
- Pytest coverage for database setup, tools, validation, and rejected raw-access behavior
- Documentation for setup, architecture, portfolio value, and future demo hosting

## Folder Structure

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
  screenshots/
```

## Installation

```bash
cd ~/ai-portfolio/contextforge-mcp-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional environment setup:

```bash
cp .env.example .env
```

The default database path is `data/contextforge.db`.

## Seed Database Command

```bash
python -m src.seed_data
```

This rebuilds the ContextForge MCP Lab demo database with five realistic tasks and five realistic documents loaded from `sample_files/`.

## Run Commands

List tasks:

```bash
python -m src.server list_tasks
```

Search documents:

```bash
python -m src.server search_documents --args '{"query": "maintenance"}'
```

Create a task:

```bash
python -m src.server create_task --args '{"title": "Capture demo screenshot", "description": "Save terminal output showing seeded data and passing tests."}'
```

Complete a task:

```bash
python -m src.server complete_task --args '{"task_id": 1}'
```

## Test Commands

```bash
python -m pytest
```

## Example Tool Calls

Task tools:

- `create_task(title, description, status="todo")`
- `list_tasks(status=None)`
- `search_tasks(query)`
- `complete_task(task_id)`
- `delete_task(task_id)`

Document tools:

- `list_documents()`
- `search_documents(query)`
- `get_document(document_id)`
- `summarize_document_metadata()`

There is no `raw_sql_query` tool. All data access goes through constrained Python functions using validation and parameterized SQLite queries.

## Portfolio Value

This project gives hiring managers and technical reviewers a clear example of AI infrastructure work:

- It connects AI tooling concepts to a real local database.
- It shows judgment around access control.
- It uses realistic fictional data instead of empty placeholders.
- It is reproducible from seed files.
- It includes tests that verify both useful actions and rejected unsafe access.

## Skills Demonstrated

- Python application structure
- SQLite schema design
- Safe data access patterns
- MCP-style tool design
- Input validation and error handling
- Seed data workflows
- Local environment setup
- Pytest testing
- Technical documentation
- Portfolio-ready AI infrastructure explanation
