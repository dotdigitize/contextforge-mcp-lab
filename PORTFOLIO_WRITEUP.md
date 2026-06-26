# ContextForge MCP Lab

## Research Question

How can an AI system safely interact with structured local data without exposing raw database access?

## Problem

AI assistants are most useful when they can access project context, tasks, documents, and operational notes. The risk is that direct access to databases or files can expose more information and more capability than the assistant needs.

This project explores a safer pattern: expose a narrow set of controlled tools that map to real workflows and keep raw database access private.

## System Design

ContextForge MCP Lab uses a layered design:

- A Python MCP-style server dispatches named tool calls.
- A tool layer exposes task and document actions.
- A database layer owns all SQLite queries.
- Seed data comes from JSON manifests and sample text files.
- Tests verify database behavior, tool behavior, validation, and rejected unsafe access.

## What I Built

I built a local MCP-style portfolio project with:

- A SQLite database containing `tasks` and `documents`
- Controlled task tools: `create_task`, `list_tasks`, `search_tasks`, `complete_task`, and `delete_task`
- Controlled document tools: `list_documents`, `search_documents`, `get_document`, and `summarize_document_metadata`
- Seed data loaded from realistic dummy files
- A command-line server entrypoint for local tool calls
- Setup, architecture, and demo planning documentation
- Pytest tests for the core workflow

## Sample Data Design

The sample data is intentionally believable. The task records cover RAG evaluation, MCP documentation, Ollama setup, public demo planning, and GitHub screenshots.

The document records come from five text files:

- `marketing_campaign_notes.txt`
- `server_maintenance_log.txt`
- `customer_support_policy.txt`
- `research_brief_llm_evals.txt`
- `project_meeting_summary.txt`

The content is fictional and contains no real personal, customer, credential, or production data.

## How I Tested It

The test suite verifies that:

- Database tables are created correctly.
- Tasks can be created, searched, completed, listed, and deleted.
- Empty task titles are rejected.
- The seed workflow loads five tasks and five documents.
- Document search and metadata summaries work.
- Unknown tools such as `raw_sql_query` are rejected.

## Results

The result is a reproducible local AI infrastructure demo. A reviewer can clone the repository, create a virtual environment, seed the database, run tests, and execute example tool calls.

The project demonstrates a concrete safety boundary: the AI-facing layer can perform useful actions, but it cannot run arbitrary SQL.

## Skills Demonstrated

- Python engineering
- SQLite schema design
- Controlled tool interface design
- MCP-style architecture
- Input validation
- Error handling
- Test-driven verification
- Seed data management
- Technical writing for portfolio presentation

## How This Connects to AI Infrastructure Roles

AI infrastructure roles often require connecting models to tools, documents, databases, queues, and internal systems. The hard part is not only making the connection work. It is designing the boundary so the model gets useful context without unsafe authority.

ContextForge MCP Lab shows that I can build and explain that boundary using practical tools: Python, SQLite, structured files, tests, and clear documentation.

## Future Demo Plan

The next version can add a portfolio website layer that calls a hosted demo API. The public demo should use a demo-only database, strict rate limits, input validation, a reset option, and the same constrained actions used by the local tool layer.

The public version should continue to avoid raw SQL, private data, and broad filesystem access.

