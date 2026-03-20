# /context

Fetch up-to-date documentation for a library using Context7.

## Usage

```
/context [library]
```

## Arguments

- `library`: Name of the library to look up (e.g., "react", "fastapi", "pydantic")

## Instructions

When invoked, Claude should:

1. Parse library name from arguments: `$ARGUMENTS`
2. Use `mcp__context7__resolve-library-id` to find the library
3. Use `mcp__context7__get-library-docs` to fetch documentation
4. Present relevant documentation to the user

## MCP Tool Usage

### Step 1: Resolve Library ID

```
mcp__context7__resolve-library-id
  libraryName: "[library]"
```

This returns a Context7-compatible library ID.

### Step 2: Fetch Documentation

```
mcp__context7__get-library-docs
  context7CompatibleLibraryID: "[resolved-id]"
  topic: "[optional topic]"
  mode: "code"  # or "info" for conceptual guides
```

## Output Format

```
=== Documentation: [Library] ===

Library: FastAPI
Version: 0.104.1
Source: /tiangolo/fastapi

## Quick Start

[Relevant documentation snippet]

## Code Examples

[Code examples from docs]

---
Fetched from Context7. Use /context [library] [topic] for specific topics.
```

## Topic-Specific Queries

For targeted documentation:

```
/context fastapi routing
/context react hooks
/context pydantic validation
```

## Modes

- `code` (default): API references and code examples
- `info`: Conceptual guides and architecture

## Examples

```
/context react
/context fastapi "dependency injection"
/context pydantic "custom validators"
```

## Related

- Context7 MCP server configuration
- [MCP.md](../knowledge-base/MCP.md) - MCP setup
