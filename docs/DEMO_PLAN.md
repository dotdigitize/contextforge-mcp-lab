# Demo Plan

ContextForge MCP Lab can later support a safe hosted demo. The public version should preserve the same principle as the local project: useful AI-facing actions without unrestricted database access.

## Public Demo Goal

The goal is to let visitors see how an AI system can work with structured local-style context through controlled tools. The demo should feel interactive but remain limited to fictional sample data.

## Controlled Demo Actions

The public demo should allow only these actions:

- Create demo task
- List demo tasks
- Search demo tasks
- Complete demo task
- Delete demo task
- List demo documents
- Search demo documents
- Open demo document

These actions map directly to the safe tool concepts in the local repository.

## Protection Notes

Use a demo database only. It should not share infrastructure or credentials with personal projects, private records, or production systems.

Use no personal data. All task and document content should be fictional, seeded, and safe to display publicly.

Add rate limiting. Public endpoints should limit repeated requests by IP or session to avoid abuse and unnecessary hosting cost.

Validate all inputs. Titles, descriptions, search terms, IDs, and document requests should have type checks, length limits, and clear error responses.

Do not expose a raw SQL endpoint. The website should never accept arbitrary SQL, database table names, or unrestricted query instructions.

Provide a reset demo data option. The demo should be easy to restore to known records after visitors create, complete, or delete tasks.

## Suggested Flow

1. Visitor opens the demo page.
2. The page lists seeded tasks and documents.
3. Visitor creates a small demo task.
4. Visitor searches tasks for a keyword such as `RAG`.
5. Visitor completes or deletes a demo task.
6. Visitor searches documents for `maintenance` or `policy`.
7. Visitor opens a selected document.
8. Visitor sees a short explanation that all actions were routed through controlled tools, not raw database access.

## Implementation Notes

A simple public implementation could use a small web API in front of a resettable SQLite database. A scheduled job or manual admin action could restore seed data. The same Python validation rules used in the local project should be reused or mirrored.

Screenshots or recordings should show the local terminal workflow first: seed database, run tests, list tasks, search documents, and reject an unknown raw SQL-style tool.
