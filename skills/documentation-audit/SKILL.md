---
name: documentation-audit
description: Automated documentation quality audits with compliance reporting
---

# Documentation Audit Skill

**Version**: 1.0.0
**Created**: 2026-02-05
**Purpose**: Systematic documentation quality checking workflow

---

## Overview

Performs comprehensive documentation quality audits across the knowledge-base. Detects files exceeding line limits, missing cross-references, broken links, code block formatting issues, and compliance violations.

This skill provides actionable reports with severity-based prioritization and concrete recommendations for improvements.

## When to Use This Skill

- **Pre-release checks**: Before major version releases
- **Post-refactoring validation**: After documentation consolidation or restructuring
- **Quarterly reviews**: Regular maintenance audits (Q1, Q2, Q3, Q4)
- **New documentation addition**: Verify new docs meet standards
- **Compliance verification**: Ensure adherence to DOCUMENTATION_STANDARDS.md
- **Technical debt assessment**: Identify documentation that needs splitting or updating

## Workflow

### Phase 1: Discovery and Inventory

**Actions**:
1. Scan `knowledge-base/` directory recursively for `.md` files
2. Exclude `archive/` directories and hidden files
3. Count lines in each file (excluding empty lines)
4. Build inventory with metadata (path, size, last modified)

**Output**: File inventory with line counts

### Phase 2: Compliance Analysis

**Checks performed**:

1. **File Size Compliance**
   - Warn: >300 lines (recommend review)
   - Error: >800 lines (requires splitting)
   - Exception: INDEX.md or generated files

2. **Code Block Formatting** (CRITICAL)
   - Detect indented code blocks (breaks terminal paste)
   - Verify zero-indent for all code blocks
   - Check fenced code block syntax

3. **Header Completeness**
   - Version tag present
   - Creation date present
   - Status field (if applicable)
   - Purpose statement

4. **Table of Contents**
   - Required for files >200 lines
   - Proper markdown anchor links
   - Up-to-date section references

5. **Cross-Reference Validation**
   - Links to other knowledge-base docs exist
   - No broken internal links
   - Proper relative path usage

6. **Structure Validation**
   - Hierarchical header structure (H1 > H2 > H3)
   - No skipped header levels
   - Proper section organization

### Phase 3: Metrics Calculation

**Calculated metrics**:
- Total files scanned
- Files >300 lines (percentage)
- Files >800 lines (percentage)
- Average file size
- Total critical issues
- Total warnings
- Compliance score (percentage)

### Phase 4: Report Generation

**Report structure**:
1. Executive summary (files scanned, compliance score)
2. Critical issues (indented code blocks, broken links)
3. High priority issues (oversized files, missing TOC)
4. Medium priority issues (warnings, improvements)
5. Recommendations (actionable fixes prioritized)
6. Trend analysis (if historical data available)

### Phase 5: Actionable Recommendations

**Categories**:
1. **Immediate fixes**: Critical issues (code formatting)
2. **High priority**: File splitting, broken links
3. **Medium priority**: TOC additions, cross-references
4. **Low priority**: Style improvements, consolidations

## Output Format

```
Documentation Audit Report - 2026-02-05 14:30
==============================================

SUMMARY:
Files Scanned: 86
Total Lines: 18,450
Average Size: 214 lines/file

COMPLIANCE:
Files >300 lines: 12 (14%)
Files >800 lines: 4 (5%)
Missing TOC: 8
Code Block Issues: 2 (CRITICAL)
Broken Links: 3
Header Issues: 1

CRITICAL ISSUES (Fix Immediately):
- knowledge-base/EXAMPLE.md:87 - Indented code block (terminal incompatible)
- knowledge-base/SAMPLE.md:142 - Indented code block (terminal incompatible)

HIGH PRIORITY (Fix This Week):
- knowledge-base/LARGE_FILE.md - 1,200 lines (recommend split into 3 files)
  Suggested split:
    * LARGE_FILE_CORE.md (400 lines - core concepts)
    * LARGE_FILE_PATTERNS.md (450 lines - patterns)
    * LARGE_FILE_EXAMPLES.md (350 lines - examples)

- knowledge-base/BROKEN.md - 3 broken links:
  Line 45: Link to nonexistent DELETED_FILE.md
  Line 102: Link to archived OLD_GUIDE.md
  Line 234: Malformed link syntax

MEDIUM PRIORITY (Fix This Month):
- 8 files missing TOC (all >200 lines):
  * DOCKER_PATTERNS.md (320 lines)
  * KUBERNETES_GUIDE.md (280 lines)
  * TESTING_STRATEGIES.md (245 lines)
  [... 5 more]

- 12 files >300 lines (review for consolidation):
  * COMPREHENSIVE_GUIDE.md (650 lines)
  * ADVANCED_PATTERNS.md (540 lines)
  [... 10 more]

LOW PRIORITY (Backlog):
- knowledge-base/OLD_GUIDE.md - Last updated 6 months ago (review for archive)
- 5 files with minor cross-reference opportunities

RECOMMENDATIONS:
1. Fix 2 indented code blocks immediately (breaks terminal compatibility)
2. Split LARGE_FILE.md into 3 focused documents
3. Fix 3 broken links (update or remove)
4. Add TOC to 8 files over 200 lines
5. Review 12 files >300 lines for potential consolidation
6. Consider archiving OLD_GUIDE.md (no updates in 6 months)

COMPLIANCE SCORE: 78/86 (91%)
Target: 95% (need 4 more files compliant)

TREND (vs. last audit):
- Files >300 lines: 12 → 12 (no change)
- Critical issues: 4 → 2 (50% improvement)
- Compliance score: 87% → 91% (+4%)
```

## Automation Options

### Manual Invocation
```bash
# Via Skill tool in Claude Code
User: "Run documentation audit"

# Via command line (if script exists)
cd ~/projects/fleet-standards
./scripts/audit_docs.sh
```

### Scheduled Automation
```bash
# Daily via launchd (create plist)
~/Library/LaunchAgents/com.fleet.doc-audit.plist

# Weekly via cron
0 9 * * 1 cd ~/projects/fleet-standards && ./scripts/audit_docs.sh
```

### CI/CD Integration
```yaml
# .github/workflows/docs-audit.yml
name: Documentation Audit

on:
  pull_request:
    paths:
      - 'knowledge-base/**'

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run documentation audit
        run: ./scripts/audit_docs.sh
      - name: Check compliance threshold
        run: |
          # Fail if compliance <90%
          grep "COMPLIANCE SCORE" audit-report.txt | \
          awk '{if ($3 < 90) exit 1}'
```

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
if git diff --cached --name-only | grep -q 'knowledge-base/.*\.md'; then
    ./scripts/audit_docs.sh --quick
fi
```

## Related Skills

- **lint-docs**: Runs the linter script (implementation of this skill)
- **documentation-consolidate**: Merge overlapping documentation files
- **knowledge-vault**: Knowledge base management

## Related Commands

- `/lint-docs` - Execute documentation linter
- `/review` - Code review workflow (can include docs)
- `/trace` - Capture documentation decisions

## Related Documentation

- `knowledge-base/DOCUMENTATION_STANDARDS.md` - Standards reference
- `knowledge-base/DOCUMENTATION_CHECKLIST.md` - Pre-publish checklist
- `knowledge-base/DOCUMENTATION_MAINTENANCE.md` - Maintenance schedule
- `knowledge-base/QUALITY_BYPASSES_GUIDE.md` - When to skip checks

## Examples

### Example 1: Pre-Release Audit (v3.2)

**User**: "Audit documentation before v3.2 release"

**Agent workflow**:
1. Scans 86 files in `knowledge-base/`
2. Identifies 2 critical issues (indented code blocks in EXAMPLE.md, SAMPLE.md)
3. Detects 4 files >800 lines requiring splits
4. Finds 3 broken links
5. Calculates 91% compliance score
6. Generates prioritized fix list

**Report highlights**:
- 2 critical fixes required before release
- 4 files need splitting (can defer to v3.3)
- Overall: BLOCKER for release until critical fixes complete

**Agent action**:
- Fixes 2 indented code blocks immediately
- Creates issues for file splitting (v3.3 milestone)
- Updates broken links
- Re-runs audit: 95% compliance → APPROVED for release

### Example 2: Post-Consolidation Validation

**User**: "Audit after website docs consolidation"

**Context**: Merged 8 website-related docs into 3 focused files

**Agent workflow**:
1. Scans updated files
2. Validates zero broken links (all updated during consolidation)
3. Confirms file sizes now compliant (all <300 lines)
4. Verifies cross-references intact
5. Checks TOC accuracy
6. Reports 100% compliance

**Report highlights**:
- 8 files consolidated → 3 files
- Average file size reduced 45% (380 → 210 lines)
- Zero broken links
- All cross-references valid
- Compliance: 100%

**Outcome**: Consolidation successful, documentation improved

### Example 3: Quarterly Maintenance Review (Q1 2026)

**User**: "Quarterly documentation audit"

**Agent workflow**:
1. Full scan of `knowledge-base/` (86 files)
2. Identifies 4 files >800 lines (unchanged from Q4)
3. Detects 12% content overlap in secrets documentation (SECRETS.md, SECRETS_MANAGEMENT.md, BITWARDEN.md)
4. Finds 2 files not updated in 9 months
5. Generates 6-month trend report
6. Recommends 2 consolidations

**Report highlights**:
- Files >800 lines: 4 (same as Q4 2025) → ACTION REQUIRED
- Content overlap detected: Secrets docs (12% redundancy)
- Stale content: 2 files (9 months no updates)
- Trend: Compliance declining (-3% vs. Q4)

**Recommendations**:
1. **Q1 Priority**: Split 4 oversized files
2. **Q1 Priority**: Consolidate secrets documentation (reduce redundancy)
3. **Q2 Planning**: Review stale content for archival
4. **Ongoing**: Enforce <300 line limit for new docs

**Outcome**: Action plan created, Q1 documentation sprint scheduled

### Example 4: New Documentation Addition

**User**: "I just added KUBERNETES_DEPLOYMENT.md (450 lines). Audit it."

**Agent workflow**:
1. Scans new file specifically
2. Detects file >300 lines (450 lines)
3. Checks for TOC (missing)
4. Validates code block formatting (all correct)
5. Checks cross-references (3 links valid)
6. Verifies header structure (proper hierarchy)

**Report highlights**:
- File size: 450 lines (OVER LIMIT - recommend split)
- Missing TOC (required for files >200 lines)
- Code formatting: Compliant
- Cross-references: Valid

**Recommendations**:
1. Split into 2 files:
   - KUBERNETES_DEPLOYMENT_SETUP.md (250 lines)
   - KUBERNETES_DEPLOYMENT_PATTERNS.md (200 lines)
2. Add TOC to both files

**Agent action**:
- Proposes split strategy
- Creates both files with proper TOC
- Updates cross-references
- Re-runs audit: 100% compliance

### Example 5: CI/CD Automated Check

**Context**: Pull request with documentation changes

**GitHub Action workflow**:
```
PR #234: Update Docker patterns documentation

Documentation Audit (Automated):
- Files changed: 3
- New critical issues: 0
- New warnings: 1 (DOCKER_PATTERNS.md now 310 lines)
- Compliance: 94% (above 90% threshold)
- Status: ✅ PASSED

Warning Details:
- DOCKER_PATTERNS.md increased from 280 → 310 lines
- Still under 800 line error threshold
- Consider splitting if continues to grow

Action: PR approved for merge (compliance check passed)
```

## Implementation Notes

### File Size Thresholds

**Rationale**:
- 300 lines: Typical file readability limit (warning)
- 800 lines: Cognitive overload threshold (error)
- Exceptions: INDEX.md (intentionally comprehensive)

### Critical Code Block Rule

**Why zero-indent matters**:
```markdown
# BAD (indented - breaks terminal paste)
    ```bash
    git commit -m "message"
    ```

# GOOD (zero-indent - terminal compatible)
```bash
git commit -m "message"
```
```

Indented code blocks add leading spaces when copied, causing terminal paste failures. This is a CRITICAL issue for fleet-standards where users copy commands frequently.

### TOC Requirements

**Required for files >200 lines because**:
- Improves navigation in long documents
- Enables quick section jumping
- Provides document structure overview
- Required by DOCUMENTATION_STANDARDS.md

### Compliance Score Calculation

```
Compliance Score = (Total Files - Files with Issues) / Total Files * 100

Issues include:
- Critical: Indented code blocks, broken links
- High: Files >800 lines, missing required TOC
- Medium: Files >300 lines (warnings)

Example:
86 files total
2 critical issues
4 high priority issues
6 files with warnings (not counted as issues)

Issues = 2 + 4 = 6
Compliant = 86 - 6 = 80
Score = 80/86 * 100 = 93%
```

## Quality Bypass Tracking

If audit reveals issues that cannot be immediately fixed, document bypasses:

```bash
# Log quality bypass
./scripts/quality_bypass.py log \
  --file LARGE_FILE.md \
  --rule "file-size-limit" \
  --reason "Comprehensive reference guide, splitting would reduce utility" \
  --expiry "2026-12-31" \
  --reviewer "username"
```

See `knowledge-base/QUALITY_BYPASSES_GUIDE.md` for details.

## Exit Codes

When run as script:
- `0`: All checks passed (≥95% compliance)
- `1`: Critical issues found (requires immediate fix)
- `2`: High priority issues (fix within 1 week)
- `3`: Medium priority warnings only

## Configuration

Create `.docsaudit.yml` in repository root for customization:

```yaml
# Documentation audit configuration
thresholds:
  warn_lines: 300
  error_lines: 800
  required_toc_lines: 200
  compliance_target: 95

exclude_patterns:
  - "archive/**"
  - "**/INDEX.md"
  - "generated/**"

rules:
  enforce_zero_indent: true
  require_version_header: true
  check_broken_links: true
  validate_toc: true

output:
  format: "markdown"  # or "json", "html"
  save_to: "audit-reports/"
  include_trends: true
```

---

**Version History**:
- v1.0.0 (2026-02-05): Initial skill creation
