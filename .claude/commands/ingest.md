# /ingest

Index codebase into LanceDB for semantic search.

## Usage

```
/ingest [path]
```

## Arguments (optional)

- No args: Index current project
- `path`: Specific directory to index
- `--all`: Index all projects in ~/projects/

## Instructions

When invoked, Claude should run:

```bash
uv run ~/projects/agent-system/bin/ingest.py
```

For specific path:
```bash
uv run ~/projects/agent-system/bin/ingest.py --path [path]
```

For all projects:
```bash
uv run ~/projects/agent-system/bin/ingest.py --all
```

## What Gets Indexed

- Python files (.py)
- Markdown files (.md)
- Configuration files (.json, .yaml, .toml)
- Decision traces (.claude-decisions/)

## Output Format

```
=== Indexing Codebase ===

Project: agent-system
Path: ~/projects/agent-system

Processing files...
  [OK] src/core/indexer.py (245 chunks)
  [OK] src/core/search.py (128 chunks)
  [OK] README.md (12 chunks)
  ...

Summary:
  Files processed: 42
  Total chunks: 1,847
  Index size: 12.3 MB
  Time: 8.2s

Index ready for semantic search.
```

## When to Re-Index

- After major code changes
- After fleet-sync pulls new code
- After adding new files
- Weekly maintenance

## Storage

Index stored in:
- LanceDB: `~/.lancedb/` (local)
- Synced to fmini hub for fleet-wide search

## Related Commands

- `/fleet-sync` - Sync code before indexing
- `/search-decisions` - Search indexed content
- `mcp__agent-system__search_docs` - MCP search tool
