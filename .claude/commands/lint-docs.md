# Lint Documentation

**Purpose**: Check documentation compliance with standards
**Usage**: `/lint-docs [path]`
**Category**: Quality Assurance

---

## Overview

Analyzes documentation files for compliance with DOCUMENTATION_STANDARDS.md. Provides detailed reports on size, structure, code block formatting, cross-references, and content quality.

## Checks Performed

### 1. File Size
- **Warn**: Files >300 lines (guides/references), >600 lines (architecture docs)
- **Error**: Files >800 lines (guides/references), >1000 lines (architecture docs)
- **Exception**: Foundational architecture docs clearly marked

### 2. File Header
- Version or status present
- Last updated date present (YYYY-MM-DD format)
- Related docs referenced

### 3. Structure
- TOC required for files >200 lines
- Clear purpose in first paragraph
- Examples included (for concept/usage docs)

### 4. Code Blocks (CRITICAL)
- **Zero-indent enforcement**: All code blocks must be flush-left (column 0)
- Language identifiers present (```bash, ```python, etc.)
- No leading spaces or tabs before opening fence
- Terminal paste compatibility ensured

### 5. Cross-References
- All `[FILENAME.md]` or `FILENAME.md` references resolve
- No broken links to archived files
- Bidirectional references exist where appropriate

### 6. Content Quality
- No duplicate content (warns about potential overlap)
- Clear file purpose in first paragraph
- Related docs referenced in header or References section

### 7. Mermaid Diagrams
- Valid Mermaid syntax in all code blocks
- Proper diagram type declarations
- No unclosed quotes or mismatched brackets
- Closed code blocks (no missing closing ```)

## Output Format

```
Documentation Lint Report
============================================================

File: knowledge-base/EXAMPLE.md
------------------------------------------------------------
✅ PASS: file_size (245 lines)
⚠️  WARN: toc (Missing TOC for file >200 lines)
❌ FAIL: code_blocks (Code block with leading spaces at line 87)
✅ PASS: header (File header present)
❌ FAIL: cross_refs (Broken link: ARCHIVED_DOC.md at line 142)
✅ PASS: examples (Examples found)

Errors:
   ❌ Code block with leading spaces at line 87 - breaks terminal paste
   ❌ Broken link: ARCHIVED_DOC.md at line 142

Warnings:
   ⚠️  Missing TOC for file >200 lines

============================================================
Summary: 3 files checked
Errors: 2
Warnings: 1
Status: ❌ FAILED
```

## Usage Examples

Check single file:
```
/lint-docs knowledge-base/SECRETS.md
```

Check directory:
```
/lint-docs knowledge-base/
```

Check all docs (default):
```
/lint-docs
```

Check specific pattern:
```
/lint-docs knowledge-base/WEBSITE_*.md
```

## Exit Codes

- `0`: All checks passed (or only warnings)
- `1`: One or more errors found

## Implementation

Invokes: `uv run /Users/d/projects/fleet-standards/scripts/lint_docs.py`

## Integration

Can be used:
- Manually via `/lint-docs` command
- In pre-commit hooks
- In CI/CD pipelines
- Before documentation PRs

## Related

- **DOCUMENTATION_STANDARDS.md** - Standards reference
- **DOCUMENTATION_CHECKLIST.md** - Manual checklist
- **DOCUMENTATION_MAINTENANCE.md** - Maintenance guide
