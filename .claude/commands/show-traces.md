# /show-traces

List decision traces in the current project.

## Usage

```
/show-traces [filter]
```

## Arguments (optional)

- No args: Show all traces
- `pattern|correction|exception|lesson`: Filter by type
- `--recent N`: Show only the last N traces

## Instructions

When invoked, Claude should:

1. Parse optional filter from arguments: `$ARGUMENTS`
2. Read all JSON files from `.claude-decisions/traces/`
3. Apply filtering if specified
4. Format and display as a table

## Implementation

1. Check if `.claude-decisions/traces/` exists
2. If not, report "No traces found in this project"
3. Read each `.json` file in the traces directory
4. Parse the JSON and extract key fields
5. Sort by timestamp (newest first)
6. Apply filter if provided
7. Display as formatted table

## Output Format

```
| Date       | Type       | Title                          | Status  |
|------------|------------|--------------------------------|---------|
| 2025-12-26 | pattern    | Use dataclass for DTOs         | pending |
| 2025-12-25 | correction | Prefer explicit imports        | promoted|
| 2025-12-24 | lesson     | LanceDB faster for local dev   | pending |

Total: 3 traces (2 pending, 1 promoted)
```

## Filter Examples

```
/show-traces              # All traces
/show-traces pattern      # Only patterns
/show-traces correction   # Only corrections
/show-traces --recent 5   # Last 5 traces
```

## No Traces Found

If the directory doesn't exist or is empty:

```
No traces found in this project.

To create a trace:
  /trace pattern "Description of the pattern"
  /trace lesson "What you learned"
```
