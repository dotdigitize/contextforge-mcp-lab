# Setup Guide

This guide explains how to run ContextForge MCP Lab on Ubuntu 22.04.

## Ubuntu Setup

Install Python, virtual environment support, and Git:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

Confirm Python is available:

```bash
python3 --version
```

The project targets Python 3.10 or newer.

## Python Virtual Environment Setup

Create and activate a local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your shell prompt should show that `.venv` is active.

## Dependency Installation

Install test dependencies:

```bash
pip install -r requirements.txt
```

The project uses only Python standard library modules at runtime. `pytest` is required for the test suite.

## Database Seeding

The database path is controlled by `CONTEXTFORGE_DB_PATH`. Copy the example environment file if you want to customize it:

```bash
cp .env.example .env
```

Seed the demo database:

```bash
python -m src.seed_data
```

This creates `data/contextforge.db` by default and loads realistic dummy tasks and documents.

## How to Run Tests

```bash
python -m pytest
```

The tests use temporary databases where appropriate and also verify that the seed workflow loads the sample records correctly.

## How to Run the MCP Server

This project includes a minimal local command entrypoint that behaves like an MCP-style tool dispatcher.

List tasks:

```bash
python -m src.server list_tasks
```

Search tasks:

```bash
python -m src.server search_tasks --args '{"query": "RAG"}'
```

List documents:

```bash
python -m src.server list_documents
```

Open a document:

```bash
python -m src.server get_document --args '{"document_id": 1}'
```

The server accepts only registered tool names. It does not provide a raw SQL endpoint.

## Troubleshooting

If `python -m src.seed_data` cannot find files, run commands from the repository root.

If imports fail during tests, confirm that `pyproject.toml` includes `pythonpath = ["."]` and run tests with:

```bash
python -m pytest
```

If the database appears stale, reseed it:

```bash
python -m src.seed_data
```

If `.env` is not being used, verify the file contains:

```bash
CONTEXTFORGE_DB_PATH=data/contextforge.db
```

If a tool call fails, check that the JSON passed to `--args` is a JSON object and that IDs are positive integers.

