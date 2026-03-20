# /search-decisions

Search decision traces across all projects using semantic search.

## Usage

```
/search-decisions [query]
```

## Arguments

- `query`: Search term or phrase to find related decisions

## Instructions

When invoked, Claude should:

1. Parse the query from arguments: `$ARGUMENTS`
2. Use the MCP tool `mcp__agent-system__search_decisions` to search
3. Format and display results with context

## MCP Tool Usage

Call the MCP tool with:

```
mcp__agent-system__search_decisions
  query: "[user's query]"
  limit: 10
```

Optional parameters:
- `decision_type`: Filter by type (pattern, exception, lesson, correction)
- `scope`: "global" (all projects) or "promoted" (patterns only)

## Output Format

Format the results as:

```
=== Decision Search: "[query]" ===

1. [pattern] Repository pattern for Supabase
   Project: agent-system
   Date: 2025-12-20
   "Use repository classes to encapsulate data access..."

2. [lesson] LanceDB vs ChromaDB performance
   Project: fleet-standards
   Date: 2025-12-15
   "LanceDB is significantly faster for local development..."

Found 2 matching decisions.
```

## No Results

If no results found:

```
No decisions found matching "[query]".

Tips:
- Try broader search terms
- Check spelling
- Use /show-traces to see local project traces
```

## Examples

```
/search-decisions "error handling"
/search-decisions "supabase RLS"
/search-decisions "testing strategy"
```

## Related Commands

- `/show-traces` - View traces in current project only
- `/trace` - Create a new trace
- `/review-traces` - Review and promote traces
