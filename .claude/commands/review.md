# /review

Run specialized code review with focus area.

## Usage

```
/review [type] [target]
```

## Arguments

- `type`: Review focus (security, api, test, db, ux, general)
- `target` (optional): File or directory to review

## Review Types

| Type | Focus Areas |
|------|-------------|
| `security` | Injection, auth, secrets, OWASP Top 10 |
| `api` | REST conventions, error handling, validation |
| `test` | Coverage, edge cases, mocking |
| `db` | Queries, indexes, N+1, migrations |
| `ux` | Accessibility, error messages, loading states |
| `general` | Overall code quality, patterns, readability |

## Instructions

When invoked, Claude should:

1. Parse type and optional target from arguments: `$ARGUMENTS`
2. Use the Task tool with a specialized reviewer agent
3. Present findings with severity and recommendations

## Implementation

Use Task tool with appropriate prompt:

```
Task tool:
  subagent_type: "Explore"
  prompt: "Review [target] with focus on [type]. Check for [specific concerns]. Report issues by severity."
```

## Output Format

```
=== Code Review: [type] ===

Target: src/api/
Focus: Security

## Critical Issues

1. **SQL Injection Risk** [HIGH]
   File: src/api/users.py:42
   Issue: f-string in SQL query
   Fix: Use parameterized queries

## Warnings

2. **Missing Input Validation** [MEDIUM]
   File: src/api/auth.py:28
   Issue: No length limit on password field
   Fix: Add max_length validator

## Suggestions

3. **Consider Rate Limiting** [LOW]
   File: src/api/login.py
   Suggestion: Add rate limiting to prevent brute force

---
Summary: 1 critical, 1 warning, 1 suggestion
```

## Focus Area Details

### Security Review
- Input validation and sanitization
- Authentication/authorization checks
- Secret handling
- CORS and CSP headers
- SQL/NoSQL injection
- XSS vulnerabilities

### API Review
- REST conventions (verbs, status codes)
- Request/response validation
- Error handling consistency
- Documentation accuracy
- Versioning strategy

### Test Review
- Test coverage gaps
- Edge case handling
- Mock appropriateness
- Test isolation
- Flaky test detection

### Database Review
- Query efficiency
- Index usage
- N+1 query problems
- Transaction handling
- Migration safety

### UX Review
- Accessibility (a11y)
- Error message clarity
- Loading/empty states
- Mobile responsiveness
- Keyboard navigation

## Examples

```
/review security src/auth/
/review api
/review test tests/
/review db src/models/
/review ux src/components/
```

## Related

- `/security-scan` - Automated security scanning
- `/pre-commit` - Linting checks
