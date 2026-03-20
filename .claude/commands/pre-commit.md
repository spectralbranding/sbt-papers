# /pre-commit

Run all linters and checks before committing.

## Usage

```
/pre-commit
```

## Instructions

When invoked, Claude should run these checks in sequence:

```bash
# Format code
uv run black .

# Lint
uv run flake8 .

# Type check
uv run mypy .

# Run tests
uv run pytest
```

## Checks Run

| Tool | Purpose | Fix Command |
|------|---------|-------------|
| black | Code formatting | `uv run black .` |
| flake8 | Style linting | Manual fixes |
| mypy | Type checking | Add type hints |
| pytest | Unit tests | Fix failing tests |

## Output Format

```
=== Pre-Commit Checks ===

[1/4] Running black...
  All files formatted.

[2/4] Running flake8...
  No issues found.

[3/4] Running mypy...
  Success: no issues found

[4/4] Running pytest...
  12 passed in 2.3s

=== All checks passed! ===
Ready to commit.
```

## On Failure

If any check fails:

```
=== Pre-Commit Checks ===

[1/4] Running black...
  Reformatted 2 files.

[2/4] Running flake8...
  src/main.py:42:1: E302 expected 2 blank lines

[FAILED] Fix the issues above before committing.
```

## Skip Specific Checks

For exceptional cases (document with /trace exception):

```bash
# Skip type checking for prototype
uv run black . && uv run flake8 . && uv run pytest
```

## Related

- `.pre-commit-config.yaml` - Hook configuration
- `pyproject.toml` - Tool settings
