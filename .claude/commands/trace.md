# /trace

Create a decision trace to capture organizational memory.

## Usage

```
/trace [type] [description]
```

## Arguments

- `type`: One of `pattern`, `correction`, `exception`, `lesson`
- `description`: Brief description of the decision

## Types

| Type | When to Use |
|------|-------------|
| `pattern` | Successful approach worth reusing |
| `correction` | Human corrected AI behavior |
| `exception` | Intentionally broke a rule |
| `lesson` | What worked or didn't |

## Instructions

When invoked, Claude should:

1. Parse the type and description from arguments: `$ARGUMENTS`
2. Determine the current project name from the working directory
3. Generate a unique ID: `dt-{project}-{YYYYMMDD}-{3-char-hex}`
4. Create the trace JSON in `.claude-decisions/traces/`
5. Confirm creation with a summary

## Trace Schema (DecisionTrace Compatible)

Create a JSON file at `.claude-decisions/traces/dt-{project}-{YYYYMMDD}-{hex}.json`:

```json
{
  "domain": "development",
  "project": "[current project folder name]",
  "decision_type": "[pattern|correction|exception|lesson]",
  "description": "[full description of what was decided]",
  "rationale": "[why this approach was chosen]",
  "id": "dt-[project]-[YYYYMMDD]-[3-char-hex]",
  "timestamp": "[ISO8601 with microseconds]",
  "inputs": {
    "trigger": "[what prompted this decision]",
    "context": "[additional context if relevant]"
  },
  "session_context": {
    "goal": "[current session goal if known]"
  },
  "outcome": {
    "result": "success",
    "validation": "[how success was verified]"
  },
  "human_interaction": {},
  "tags": ["[relevant]", "[tags]"],
  "category": "[architecture|security|testing|performance|etc]",
  "applicability": "[project|domain|global]",
  "confidence": 1.0,
  "promotion_status": "pending"
}
```

## Field Guidelines

| Field | Value |
|-------|-------|
| `domain` | Always "development" for manual traces |
| `decision_type` | The type argument (pattern/correction/exception/lesson) |
| `applicability` | "global" for patterns/corrections, "project" for specific implementations |
| `category` | Infer from description (architecture, security, testing, performance, docs) |
| `tags` | Extract 3-6 keywords from description |

## Directory Setup

If `.claude-decisions/traces/` doesn't exist, create it:

```bash
mkdir -p .claude-decisions/traces
```

## Examples

### Pattern
```
/trace pattern "Use .env for non-secret config, .env.template for documenting Bitwarden secrets"
```

Creates:
```json
{
  "domain": "development",
  "project": "fleet-standards",
  "decision_type": "pattern",
  "description": "Use .env for non-secret config, .env.template for documenting Bitwarden secrets",
  "rationale": "Separates configuration from secret documentation, both can be committed safely",
  "id": "dt-fleet-standards-20251228-a1b",
  "timestamp": "2025-12-28T10:30:00.000000",
  "inputs": {"trigger": "Manual trace capture"},
  "session_context": {},
  "outcome": {"result": "success", "validation": "Pattern established"},
  "human_interaction": {},
  "tags": ["secrets", "config", "documentation"],
  "category": "architecture",
  "applicability": "global",
  "confidence": 1.0,
  "promotion_status": "pending"
}
```

### Correction
```
/trace correction "Changed from single .env.example to dual .env + .env.template structure"
```

Creates a trace with `decision_type: "correction"` and includes the original vs new approach.

### Exception
```
/trace exception "Committed plaintext .env.local to status-verification (Supabase demo project)"
```

Creates a trace documenting why a rule was intentionally broken.

### Lesson
```
/trace lesson "Schema mismatch between /trace template and DecisionTrace dataclass caused search failures"
```

Creates a trace capturing what was learned.

## Output

After creating the trace, output:

```
Created [type] trace: dt-[project]-[date]-[hex]
File: .claude-decisions/traces/dt-[project]-[date]-[hex].json
Searchable via: /search-decisions "[keyword]"
```

## Verification

After creating a trace, it should be findable via the MCP tool:
```
mcp__agent-system__search_decisions(query="[keyword from description]")
```
