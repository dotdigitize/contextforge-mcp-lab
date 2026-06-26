# Architecture

ContextForge MCP Lab is organized as a layered local AI infrastructure demo. Each layer has a clear responsibility and keeps the AI-facing surface narrow.

## Portfolio Website Demo Layer

A future portfolio website can provide a simple interface for visitors to try controlled demo actions. This layer should show tasks, document search results, and selected document content.

The website should not connect directly to SQLite. It should call a small API or server layer that enforces the same constraints as the local tool functions.

## Safe API Layer

The safe API layer is responsible for request validation, rate limiting, response shaping, and demo reset behavior.

It should expose only approved actions:

- Create a demo task
- List demo tasks
- Search demo tasks
- Complete a demo task
- Delete a demo task
- List demo documents
- Search demo documents
- Open a demo document

This layer should never forward arbitrary query text to the database as SQL.

## MCP Server Layer

The MCP server layer exposes named tools to an AI system. In this repository, `src/server.py` and `src/tools.py` provide a local command-based version of that idea.

The tool layer is intentionally small. Each tool maps to a clear workflow and calls controlled database functions. The AI system can ask for a tool call, but it cannot invent new permissions.

## SQLite Database Layer

The SQLite layer stores two tables:

- `tasks`
- `documents`

All SQLite access lives in `src/database.py`. Queries use parameterized statements, input validation, and explicit functions. There is no raw SQL tool.

The database is suitable for a local demo because it is easy to inspect, reset, seed, and test.

## Sample Files Layer

The `sample_files/` directory contains realistic fictional documents. The seed script reads these files and stores their content in the `documents` table along with metadata from `data/sample_documents.json`.

This keeps the demo grounded in real text content while avoiding private or personal data.

## Why Raw Database Access Should Never Be Public

Raw database access should never be public because it gives callers more power than the demo requires. A raw query endpoint can expose hidden records, reveal schema details, modify data unexpectedly, or become a path for injection vulnerabilities.

For AI systems, raw access also makes behavior harder to evaluate. A controlled tool such as `search_documents` has predictable inputs, outputs, and tests. A raw SQL prompt has an unbounded action space.

The safer pattern is to design narrow tools that match user workflows, validate inputs, and return only the data needed for the task.

