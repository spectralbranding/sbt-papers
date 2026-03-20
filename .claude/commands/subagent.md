# /subagent

Invoke a specialized subagent for focused tasks.

## Usage

```
/subagent [name] [task]
```

## Arguments

- `name`: Subagent type to invoke
- `task`: Task description for the subagent

## Available Subagents

| Name | Purpose | Use Case |
|------|---------|----------|
| `explore` | Codebase exploration | "Find all API endpoints" |
| `plan` | Implementation planning | "Plan auth system" |
| `qa` | Quality assurance | "Review test coverage" |
| `security` | Security analysis | "Check for vulnerabilities" |
| `docs` | Documentation | "Generate API docs" |

## Instructions

When invoked, Claude should:

1. Parse subagent name and task from arguments: `$ARGUMENTS`
2. Use the Task tool with appropriate subagent_type
3. Return the subagent's findings

## Task Tool Mapping

| Subagent | Task Tool Config |
|----------|-----------------|
| `explore` | `subagent_type: "Explore"` |
| `plan` | `subagent_type: "Plan"` |
| `qa` | `subagent_type: "general-purpose"` with QA prompt |
| `security` | `subagent_type: "general-purpose"` with security prompt |
| `docs` | `subagent_type: "general-purpose"` with docs prompt |

## Output Format

```
=== Subagent: [name] ===

Task: [task description]

[Subagent output]

---
Completed by [subagent] in [time]
```

## Examples

### Explore Codebase
```
/subagent explore "Find how authentication is implemented"
```

### Plan Feature
```
/subagent plan "Design caching layer for API responses"
```

### QA Check
```
/subagent qa "Verify error handling in payment module"
```

### Security Audit
```
/subagent security "Check auth endpoints for vulnerabilities"
```

### Documentation
```
/subagent docs "Generate docstrings for src/api/"
```

## Subagent Details

### Explore
Fast codebase exploration using Glob, Grep, and Read tools.
Best for: Finding files, understanding structure, locating code.

### Plan
Software architect for designing implementation strategies.
Best for: Feature planning, architecture decisions, migration plans.

### QA
Quality assurance focused on testing and correctness.
Best for: Test review, coverage analysis, edge case identification.

### Security
Security-focused analysis and vulnerability detection.
Best for: Security audits, penetration test prep, compliance checks.

### Docs
Documentation generation and maintenance.
Best for: README updates, API docs, code comments.

## Related

- `/engine` - Uses subagents automatically
- `/review` - Specialized code review
- Task tool documentation
