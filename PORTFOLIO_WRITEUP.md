# ContextForge MCP Lab Case Study

## Research Question

How can an AI-facing system work with structured local data without exposing raw database access?

## Problem

AI assistants are most useful when they can work with project context, task records, documents, and operational notes. The risk is that direct access to databases or files can expose more information and more capability than the workflow requires.

ContextForge MCP Lab explores a narrower pattern: expose controlled tools that map to specific actions, keep database operations behind a service boundary, and make the behavior easy to seed, test, and inspect.

## System Design

ContextForge MCP Lab uses a layered design:

- A local MCP-style dispatcher accepts named tool calls.
- A tool layer exposes task and document actions.
- A database layer owns all SQLite queries.
- Seed data comes from JSON manifests and sample text files.
- Tests verify database behavior, tool behavior, validation, and rejected unsafe access.

## Implementation

The project includes:

- A SQLite database containing `tasks` and `documents`
- Controlled task tools: `create_task`, `list_tasks`, `search_tasks`, `complete_task`, and `delete_task`
- Controlled document tools: `list_documents`, `search_documents`, `get_document`, and `summarize_document_metadata`
- Seed data loaded from fictional sample files
- A command-line entrypoint for local tool calls
- Setup, architecture, and demo planning documentation
- Pytest tests for the core workflow

## Sample Data Design

The sample records are designed to be realistic enough for local testing without using private or production data. Task records cover RAG evaluation, MCP documentation, local model setup, demo planning, and repository maintenance.

The document records come from five text files:

- `marketing_campaign_notes.txt`
- `server_maintenance_log.txt`
- `customer_support_policy.txt`
- `research_brief_llm_evals.txt`
- `project_meeting_summary.txt`

The content is fictional and contains no real personal, customer, credential, or production data.

## Testing

The test suite verifies that:

- Database tables are created correctly.
- Tasks can be created, searched, completed, listed, and deleted.
- Empty task titles are rejected.
- The seed workflow loads five tasks and five documents.
- Document search and metadata summaries work.
- Unknown tools such as `raw_sql_query` are rejected.

## Results

The result is a reproducible local data access service with a clear safety boundary. A developer can seed the database, run tests, and execute task and document actions through a constrained interface.

The AI-facing layer can perform useful operations, but it cannot run arbitrary SQL or invent new database permissions.

## Technical Rationale

The repository focuses on a few practical design choices:

- Keep the public callable surface small and named.
- Keep SQL inside the persistence layer.
- Use parameterized queries for database operations.
- Seed demo data from versioned files.
- Test both successful workflows and rejected access patterns.

## Engineering Notes

- Python application structure
- SQLite schema design
- Controlled tool interface design
- MCP-style architecture
- Input validation
- Error handling
- Seed data management
- Pytest verification
- Technical documentation

## Relevance

AI systems often need access to tools, documents, databases, queues, and internal applications. The connection is only part of the problem; the boundary around that connection determines what the system can read, modify, and expose.

ContextForge MCP Lab demonstrates one local version of that boundary using Python, SQLite, structured files, tests, and explicit tool functions.

## Future Demo Plan

A future hosted version could add a small web API in front of the same constrained actions. That version should use a demo-only database, strict rate limits, input validation, reset behavior, and the same no-raw-SQL rule used by the local tool layer.

The public version should continue to avoid private data, personal data, credentials, and broad filesystem access.
