---
name: python-dev
description: Expert Python 3.12 development guidelines for the fleet (uv, typing, async).
---

# Python Development Skill

> **Standards**: Python 3.12, `uv`, Type Hints, Google Docstrings

## Core Rules

1.  **Package Management**:
    -   ALWAYS use `uv` for dependency management.
    -   `uv init` to create projects (includes venv).
    -   `uv add <package>` to add dependencies.
    -   `uv sync` to install from uv.lock.
    -   NEVER use `pip` directly.

2.  **Code Style**:
    -   **Formatter**: `black` (line length 88).
    -   **Linter**: `flake8` (max line length 120 for legacy compatibility).
    -   **Imports**: `isort` (profile=black).
    -   **Typing**: `mypy` strict mode.

3.  **Line Length Strategy**:
    -   `black` formats to 88 chars (strict).
    -   `flake8` allows up to 120 chars (lenient for edge cases).
    -   Target 88 chars for new code.

4.  **Project Structure**:
    ```
    my-project/
    ├── src/
    │   └── my_project/
    │       └── __init__.py
    ├── tests/
    │   └── test_main.py
    ├── pyproject.toml
    └── uv.lock
    ```

## Common Workflows

### New Project
```bash
mkdir my-project && cd my-project
uv init --python 3.12
uv add pytest --dev
```

### Add Dependencies
```bash
uv add fastapi pydantic
uv add pytest pytest-cov --dev
```

### Run Tests
```bash
uv run pytest
uv run pytest --cov=src
```

### Pre-commit Check
```bash
uv run black .
uv run isort .
uv run flake8
uv run mypy src/
```

### Full Lint (fleet standard)
```bash
uv run black . && uv run flake8 && uv run pytest --collect-only
```

## Type Hints Best Practices

```python
from typing import Optional

def process_data(items: list[str], limit: int = 10) -> dict[str, int]:
    """Process items and return counts.

    Args:
        items: List of items to process.
        limit: Maximum items to process.

    Returns:
        Dictionary mapping items to their counts.
    """
    return {item: len(item) for item in items[:limit]}
```

## Async Patterns (macOS)

```python
import asyncio

# On macOS, use this selector policy for subprocess support
if __name__ == "__main__":
    import platform
    if platform.system() == "Darwin":
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())
```

See `knowledge-base/PYTHON_ASYNC_MACOS.md` for details.
