---
name: python-project-init
description: Initialize Python projects with uv, SOLID architecture, and fleet standards
---

# Python Project Init Skill

**Version**: 1.0.0
**Created**: 2026-02-05
**Purpose**: Scaffold production-ready Python projects with fleet standards

---

## Overview

Generates complete Python project scaffolds with uv package management, SOLID architecture patterns, comprehensive testing setup, CI/CD workflows, and security best practices. All projects are Python 3.12+ and follow fleet coding principles.

This skill eliminates boilerplate setup and ensures consistency across all Python projects in the fleet.

## When to Use This Skill

- **New projects**: Starting fresh Python applications
- **Legacy migration**: Converting pip-based projects to uv
- **Library development**: Creating reusable Python packages
- **CLI tools**: Building command-line utilities
- **API services**: FastAPI or Flask applications
- **Data pipelines**: ETL and data processing projects
- **Automation scripts**: Complex scripts that need testing

## Project Structure

### Standard Layout

```
project-name/
├── src/
│   └── project_name/              # Package name (underscores)
│       ├── __init__.py
│       ├── models/                # Domain models (SOLID)
│       │   ├── __init__.py
│       │   └── example.py
│       ├── repositories/          # Data access (SOLID)
│       │   ├── __init__.py
│       │   └── example_repository.py
│       ├── services/              # Business logic (SOLID)
│       │   ├── __init__.py
│       │   └── example_service.py
│       ├── cli.py                 # CLI entry point (if applicable)
│       └── main.py                # Application entry point
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_repositories.py
│   │   └── test_services.py
│   ├── integration/
│   │   └── test_api.py
│   └── conftest.py                # Pytest fixtures
├── scripts/
│   ├── pre-commit.sh              # Local quality checks
│   └── setup-dev.sh               # Dev environment setup
├── .github/
│   └── workflows/
│       ├── ci.yml                 # CI/CD pipeline
│       └── security.yml           # Security scanning
├── pyproject.toml                 # uv configuration
├── .env.template                  # Environment variables template
├── .envrc                         # direnv integration
├── .gitignore
├── .flake8
├── README.md
├── PROJECT_CONTEXT.md             # Claude Code context
└── CONTRIBUTING.md
```

### Architecture Principles

**SOLID Application** (from CODING_PRINCIPLES.md):
1. **Single Responsibility**: Each class has one reason to change
2. **Open/Closed**: Open for extension, closed for modification
3. **Liskov Substitution**: Subtypes must be substitutable for base types
4. **Interface Segregation**: Many specific interfaces > one general
5. **Dependency Inversion**: Depend on abstractions, not concretions

**YAGNI Application**:
- Start minimal (no feature speculation)
- Add complexity only when needed
- Defer abstractions until 3rd use case

## Workflow

### Phase 1: Project Initialization

**Actions**:
1. Create directory structure
2. Initialize git repository with `.gitignore`
3. Create feature branch (`feature/project-init`)
4. Generate `README.md` with project description

**Git setup**:
```bash
cd ~/projects
mkdir project-name && cd project-name
git init
git checkout -b feature/project-init
```

### Phase 2: Python Configuration (uv)

**Actions**:
1. Create `pyproject.toml` with uv standards
2. Set Python 3.12 requirement
3. Add core dependencies (based on project type)
4. Add dev dependencies (black, flake8, pytest, mypy)
5. Configure tool settings (black, pytest, mypy)

**Generated `pyproject.toml`**:
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Brief project description"
requires-python = ">=3.12"
dependencies = [
    # Add runtime dependencies here
]

[project.optional-dependencies]
dev = [
    "black>=24.0.0",
    "flake8>=7.0.0",
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.8.0",
]

[project.scripts]
project-name = "project_name.cli:main"  # If CLI

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.black]
line-length = 100
target-version = ['py312']
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "--strict-markers --cov=src --cov-report=term-missing"

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
exclude = ["tests/"]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### Phase 3: SOLID Architecture Scaffolding

**Models layer** (`src/project_name/models/`):
```python
# models/user.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    """User domain model.

    Represents a user entity with validation logic.
    Follows Single Responsibility Principle.
    """
    id: str
    email: str
    name: str
    created_at: datetime
    active: bool = True

    def deactivate(self) -> None:
        """Deactivate this user account."""
        self.active = False

    def validate_email(self) -> bool:
        """Validate email format."""
        return "@" in self.email and "." in self.email.split("@")[1]
```

**Repositories layer** (`src/project_name/repositories/`):
```python
# repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from ..models.user import User

class UserRepository(ABC):
    """User repository interface.

    Follows Dependency Inversion Principle - depend on abstraction.
    Allows multiple implementations (SQL, NoSQL, in-memory, etc.).
    """

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve user by ID."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve user by email."""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Persist user to storage."""
        pass

    @abstractmethod
    def list_active(self) -> List[User]:
        """List all active users."""
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Delete user by ID."""
        pass


# repositories/user_repository_sqlite.py
import sqlite3
from typing import Optional, List
from .user_repository import UserRepository
from ..models.user import User
from datetime import datetime

class UserRepositorySQLite(UserRepository):
    """SQLite implementation of UserRepository.

    Concrete implementation following Interface Segregation.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        """Create users table if not exists."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    active INTEGER NOT NULL
                )
            """)

    def get_by_id(self, user_id: str) -> Optional[User]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, email, name, created_at, active FROM users WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            return self._row_to_user(row) if row else None

    def get_by_email(self, email: str) -> Optional[User]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, email, name, created_at, active FROM users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            return self._row_to_user(row) if row else None

    def save(self, user: User) -> User:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO users (id, email, name, created_at, active)
                   VALUES (?, ?, ?, ?, ?)""",
                (user.id, user.email, user.name,
                 user.created_at.isoformat(), int(user.active))
            )
        return user

    def list_active(self) -> List[User]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, email, name, created_at, active FROM users WHERE active = 1"
            )
            return [self._row_to_user(row) for row in cursor.fetchall()]

    def delete(self, user_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return cursor.rowcount > 0

    @staticmethod
    def _row_to_user(row: tuple) -> User:
        """Convert database row to User model."""
        return User(
            id=row[0],
            email=row[1],
            name=row[2],
            created_at=datetime.fromisoformat(row[3]),
            active=bool(row[4])
        )
```

**Services layer** (`src/project_name/services/`):
```python
# services/user_service.py
from ..models.user import User
from ..repositories.user_repository import UserRepository
from typing import Optional, List

class UserService:
    """User business logic service.

    Follows Single Responsibility and Dependency Inversion.
    Coordinates between repositories and implements business rules.
    """

    def __init__(self, user_repository: UserRepository):
        """Initialize with repository dependency injection."""
        self.user_repository = user_repository

    def create_user(self, email: str, name: str) -> User:
        """Create new user with validation."""
        # Check for duplicate email
        existing = self.user_repository.get_by_email(email)
        if existing:
            raise ValueError(f"User with email {email} already exists")

        # Create and validate user
        from datetime import datetime
        import uuid
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            name=name,
            created_at=datetime.now()
        )

        if not user.validate_email():
            raise ValueError(f"Invalid email format: {email}")

        return self.user_repository.save(user)

    def activate_user(self, user_id: str) -> User:
        """Activate user account."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        user.active = True
        return self.user_repository.save(user)

    def deactivate_user(self, user_id: str) -> User:
        """Deactivate user account."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        user.deactivate()
        return self.user_repository.save(user)

    def get_active_users(self) -> List[User]:
        """Retrieve all active users."""
        return self.user_repository.list_active()
```

### Phase 4: Testing Infrastructure

**Pytest configuration** (`tests/conftest.py`):
```python
# tests/conftest.py
import pytest
import tempfile
import os
from src.project_name.repositories.user_repository_sqlite import UserRepositorySQLite
from src.project_name.services.user_service import UserService

@pytest.fixture
def temp_db():
    """Create temporary database for tests."""
    fd, path = tempfile.mkstemp(suffix=".db")
    yield path
    os.close(fd)
    os.unlink(path)

@pytest.fixture
def user_repository(temp_db):
    """Create test user repository."""
    return UserRepositorySQLite(temp_db)

@pytest.fixture
def user_service(user_repository):
    """Create test user service."""
    return UserService(user_repository)
```

**Unit tests** (`tests/unit/test_services.py`):
```python
# tests/unit/test_services.py
import pytest
from src.project_name.models.user import User

def test_create_user_success(user_service):
    """Test successful user creation."""
    user = user_service.create_user("test@example.com", "Test User")

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.active is True

def test_create_user_duplicate_email(user_service):
    """Test duplicate email rejection."""
    user_service.create_user("test@example.com", "Test User")

    with pytest.raises(ValueError, match="already exists"):
        user_service.create_user("test@example.com", "Another User")

def test_create_user_invalid_email(user_service):
    """Test invalid email rejection."""
    with pytest.raises(ValueError, match="Invalid email"):
        user_service.create_user("invalid-email", "Test User")

def test_deactivate_user(user_service):
    """Test user deactivation."""
    user = user_service.create_user("test@example.com", "Test User")
    deactivated = user_service.deactivate_user(user.id)

    assert deactivated.active is False

def test_get_active_users(user_service):
    """Test active users retrieval."""
    user1 = user_service.create_user("user1@example.com", "User 1")
    user2 = user_service.create_user("user2@example.com", "User 2")
    user_service.deactivate_user(user2.id)

    active_users = user_service.get_active_users()

    assert len(active_users) == 1
    assert active_users[0].id == user1.id
```

### Phase 5: CI/CD and Quality Tools

**GitHub Actions CI** (`.github/workflows/ci.yml`):
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv pip install -e ".[dev]" --system

      - name: Format check (Black)
        run: uv run black . --check

      - name: Lint (Flake8)
        run: uv run flake8 src/ tests/

      - name: Type check (mypy)
        run: uv run mypy src/

      - name: Test with coverage
        run: uv run pytest --cov --cov-report=xml --cov-report=term

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

**Security scanning** (`.github/workflows/security.yml`):
```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

**Pre-commit script** (`scripts/pre-commit.sh`):
```bash
#!/bin/bash
set -e

echo "Running pre-commit checks..."

# Format check
echo "1. Checking code formatting..."
uv run black . --check || {
    echo "❌ Code formatting failed. Run: uv run black ."
    exit 1
}

# Lint
echo "2. Running linter..."
uv run flake8 src/ tests/ || {
    echo "❌ Linting failed."
    exit 1
}

# Type check
echo "3. Running type checker..."
uv run mypy src/ || {
    echo "❌ Type checking failed."
    exit 1
}

# Tests
echo "4. Running tests..."
uv run pytest --collect-only > /dev/null || {
    echo "❌ Test collection failed."
    exit 1
}

echo "✅ All pre-commit checks passed!"
```

### Phase 6: Documentation

**README.md template**:
```markdown
# Project Name

Brief description of what this project does.

## Installation

```bash
# Clone repository
git clone https://github.com/username/project-name.git
cd project-name

# Install with uv
uv pip install -e ".[dev]"
```

## Usage

```python
from project_name.services.user_service import UserService
from project_name.repositories.user_repository_sqlite import UserRepositorySQLite

# Initialize
repo = UserRepositorySQLite("users.db")
service = UserService(repo)

# Create user
user = service.create_user("user@example.com", "John Doe")
print(f"Created user: {user.id}")
```

## Development

```bash
# Run tests
uv run pytest

# Format code
uv run black .

# Lint
uv run flake8 src/ tests/

# Type check
uv run mypy src/

# Pre-commit checks
./scripts/pre-commit.sh
```

## Architecture

This project follows SOLID principles:

- **Models**: Domain entities and value objects
- **Repositories**: Data access interfaces and implementations
- **Services**: Business logic and orchestration

See `PROJECT_CONTEXT.md` for detailed architecture decisions.

## License

MIT
```

**PROJECT_CONTEXT.md template**:
```markdown
# Project Context

**Project**: project-name
**Created**: 2026-02-05
**Python**: 3.12+
**Package Manager**: uv

---

## Purpose

[Describe the project's purpose and goals]

## Architecture

This project follows SOLID principles with clear separation of concerns:

### Layers

1. **Models** (`src/project_name/models/`)
   - Domain entities
   - Value objects
   - Business rules embedded in entities

2. **Repositories** (`src/project_name/repositories/`)
   - Data access interfaces (abstract)
   - Concrete implementations (SQLite, etc.)
   - Follows Dependency Inversion Principle

3. **Services** (`src/project_name/services/`)
   - Business logic
   - Coordinates between repositories
   - Transaction management

### Key Design Decisions

**Decision**: Use SQLite for initial storage
**Rationale**: Simple, local, no external dependencies. Can migrate to PostgreSQL later.
**Alternatives considered**: PostgreSQL (overkill for v1), in-memory (no persistence)

**Decision**: Repository pattern for data access
**Rationale**: Allows swapping implementations, easier testing, follows SOLID.
**Alternatives considered**: Direct database access (less testable)

## Development Workflow

1. Create feature branch: `git checkout -b feature/feature-name`
2. Make changes with tests
3. Run pre-commit: `./scripts/pre-commit.sh`
4. Commit and push
5. Create pull request

## Testing Strategy

- **Unit tests**: Test services and models in isolation
- **Integration tests**: Test with real database
- **Coverage target**: >80%

## Dependencies

### Runtime
- [List runtime dependencies and why they're needed]

### Development
- black: Code formatting
- flake8: Linting
- pytest: Testing
- mypy: Type checking

## Secrets Management

Secrets stored in Bitwarden, loaded via `bws`:

```bash
# Set up .envrc
export $(bws secret get PROJECT_SECRET_ID --output env)
```

## Future Enhancements

- [ ] Add CLI interface (Click)
- [ ] Add API layer (FastAPI)
- [ ] Migrate to PostgreSQL
- [ ] Add observability (logging, metrics)
```

## Related Skills

- **python-dev**: Python development patterns
- **pre-commit**: Run pre-commit checks
- **review**: Code review workflow

## Related Commands

- `/pre-commit` - Run pre-commit checks
- `/trace` - Document architectural decisions
- `/review` - Code review

## Related Documentation

- `knowledge-base/CODING_PRINCIPLES.md` - SOLID principles guide
- `knowledge-base/PYTHON.md` - Python and uv workflows
- `knowledge-base/GIT.md` - Git workflow standards
- `knowledge-base/SECRETS.md` - Secrets management

## Examples

### Example 1: CLI Tool (fleet-sync-cli)

**User**: "Initialize new Python CLI tool called 'fleet-sync-cli'"

**Agent workflow**:
1. Creates project structure with `project_name = fleet_sync_cli`
2. Sets up uv with Python 3.12
3. Creates SOLID architecture (models, repositories, services)
4. Adds Click library for CLI: `dependencies = ["click>=8.1.0"]`
5. Creates `cli.py` with Click commands
6. Configures entry point: `fleet-sync = "fleet_sync_cli.cli:main"`
7. Adds pytest fixtures for CLI testing
8. Generates CI/CD workflow
9. Creates README with CLI usage examples

**Generated CLI** (`src/fleet_sync_cli/cli.py`):
```python
import click
from .services.sync_service import SyncService

@click.group()
def main():
    """Fleet synchronization CLI tool."""
    pass

@main.command()
@click.argument('machine')
def sync(machine):
    """Sync configuration to machine."""
    service = SyncService()
    result = service.sync_to_machine(machine)
    click.echo(f"✅ Synced to {machine}: {result}")

@main.command()
def status():
    """Show sync status for all machines."""
    service = SyncService()
    status = service.get_status()
    for machine, info in status.items():
        click.echo(f"{machine}: {info}")

if __name__ == '__main__':
    main()
```

**Usage**:
```bash
uv pip install -e .
fleet-sync sync fmini
fleet-sync status
```

### Example 2: FastAPI Service (webhook-processor)

**User**: "Initialize FastAPI service for webhook processing"

**Agent workflow**:
1. Creates project structure
2. Adds FastAPI dependencies:
   ```toml
   dependencies = [
       "fastapi>=0.109.0",
       "uvicorn[standard]>=0.27.0",
       "pydantic>=2.5.0",
   ]
   ```
3. Sets up SOLID architecture with webhook models
4. Creates API endpoints in `api/` directory
5. Adds request validation with Pydantic
6. Configures pytest with TestClient
7. Adds .env.template for secrets
8. Generates CI/CD with API testing

**Generated API** (`src/webhook_processor/api/webhooks.py`):
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from ..services.webhook_service import WebhookService
from ..repositories.webhook_repository import WebhookRepository

app = FastAPI(title="Webhook Processor")

class WebhookPayload(BaseModel):
    event: str
    data: dict

def get_webhook_service() -> WebhookService:
    """Dependency injection for service."""
    repo = WebhookRepository()  # Or inject from config
    return WebhookService(repo)

@app.post("/webhooks/")
async def receive_webhook(
    payload: WebhookPayload,
    service: WebhookService = Depends(get_webhook_service)
):
    """Receive and process webhook."""
    try:
        result = service.process_webhook(payload.event, payload.data)
        return {"status": "success", "id": result.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/webhooks/{webhook_id}")
async def get_webhook(
    webhook_id: str,
    service: WebhookService = Depends(get_webhook_service)
):
    """Retrieve webhook by ID."""
    webhook = service.get_webhook(webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return webhook
```

**Run server**:
```bash
uv run uvicorn webhook_processor.api.webhooks:app --reload
```

### Example 3: Data Pipeline (etl-pipeline)

**User**: "Initialize Python data pipeline for ETL processing"

**Agent workflow**:
1. Creates project structure
2. Adds data processing dependencies:
   ```toml
   dependencies = [
       "pandas>=2.1.0",
       "sqlalchemy>=2.0.0",
   ]
   ```
3. Creates SOLID architecture with pipeline stages
4. Implements Extract, Transform, Load services
5. Adds data validation models
6. Creates integration tests with sample data
7. Adds pipeline orchestration logic
8. Generates documentation with pipeline diagrams

**Generated pipeline** (`src/etl_pipeline/services/pipeline_service.py`):
```python
from ..models.data_record import DataRecord
from ..repositories.source_repository import SourceRepository
from ..repositories.destination_repository import DestinationRepository
from typing import List

class PipelineService:
    """ETL pipeline orchestration service."""

    def __init__(
        self,
        source: SourceRepository,
        destination: DestinationRepository
    ):
        self.source = source
        self.destination = destination

    def run_pipeline(self) -> dict:
        """Execute full ETL pipeline."""
        # Extract
        raw_data = self.source.extract()

        # Transform
        transformed = self._transform(raw_data)

        # Load
        loaded_count = self.destination.load(transformed)

        return {
            "extracted": len(raw_data),
            "transformed": len(transformed),
            "loaded": loaded_count
        }

    def _transform(self, records: List[DataRecord]) -> List[DataRecord]:
        """Transform data records."""
        transformed = []
        for record in records:
            # Apply transformations
            if record.validate():
                record.normalize()
                transformed.append(record)
        return transformed
```

### Example 4: Library Package (fleet-utils)

**User**: "Initialize Python library for fleet utility functions"

**Agent workflow**:
1. Creates library structure (focus on `src/fleet_utils/`)
2. Configures for package distribution:
   ```toml
   [project]
   name = "fleet-utils"
   version = "0.1.0"
   description = "Utility functions for fleet management"

   [project.urls]
   Homepage = "https://github.com/username/fleet-utils"
   ```
3. Creates public API in `__init__.py`
4. Adds comprehensive docstrings (library documentation)
5. Creates example usage in README
6. Adds publishing workflow to PyPI
7. Configures versioning strategy

**Public API** (`src/fleet_utils/__init__.py`):
```python
"""Fleet utility functions.

Usage:
    from fleet_utils import parse_machine_name, validate_port

    machine = parse_machine_name("fmini")
    is_valid = validate_port(8080)
"""

from .network import validate_port, get_local_ip
from .machines import parse_machine_name, get_machine_tier

__version__ = "0.1.0"
__all__ = [
    "validate_port",
    "get_local_ip",
    "parse_machine_name",
    "get_machine_tier",
]
```

## Quality Checklist

Before completing project initialization, verify:

- [ ] Git repository initialized with `.gitignore`
- [ ] Python 3.12+ configured in `pyproject.toml`
- [ ] uv dependencies configured (runtime + dev)
- [ ] SOLID architecture implemented (models, repositories, services)
- [ ] Unit tests created with >80% coverage
- [ ] Integration tests created (where applicable)
- [ ] Pre-commit script functional (`./scripts/pre-commit.sh`)
- [ ] CI/CD workflow configured (`.github/workflows/ci.yml`)
- [ ] Security scanning configured (`.github/workflows/security.yml`)
- [ ] README.md with installation and usage
- [ ] PROJECT_CONTEXT.md with architecture decisions
- [ ] .env.template for required secrets
- [ ] .flake8 configuration
- [ ] Type hints throughout codebase
- [ ] All tests passing
- [ ] Code formatted with Black
- [ ] No Flake8 violations
- [ ] MyPy type checks passing

---

**Version History**:
- v1.0.0 (2026-02-05): Initial skill creation
