# Documentation Consolidation Skill

**Version**: 1.0.0
**Created**: 2026-02-05
**Purpose**: Automated documentation overlap detection and consolidation

---

## Overview

Systematic workflow for detecting overlapping documentation and consolidating into focused, token-efficient files.

Based on successful consolidations:
- Website/Astro docs: 4 files → 3 files (66% overlap eliminated)
- VPN docs: 3 files → 1 file (better organization)
- Secrets docs: 1 massive file → 3 focused files

## When to Use This Skill

- Documentation growing organically (overlap increasing)
- Multiple files covering similar topics
- Token usage high (AI reading redundant content)
- Unclear which file to read for specific info
- After major feature additions (docs scattered)

## Consolidation Triggers

Use this skill when ANY of these apply:
- **>30% content overlap** between 2+ files
- **Unclear hierarchy**: Can't determine reading order
- **Excessive file count**: >5 docs on same topic
- **Token waste**: Must read 1000+ lines for basic info
- **Outdated names**: Files named for old architecture

---

## Workflow

### Phase 1: Analysis (Discovery)

**1.1 Identify Candidates**
```bash
# Find large files
find docs/ -name "*.md" ! -path "*/archive/*" -exec wc -l {} + | awk '$1 > 500'

# Find related topics
ls docs/*_PATTERNS.md docs/*_GUIDE.md docs/*_REFERENCE.md
```

**1.2 Calculate Overlap**

Read files and check for:
- Duplicate section headers
- Repeated concepts
- Similar code examples
- Cross-references indicating tight coupling

**Example Analysis**:
```
File Overlap Analysis
=====================

Cluster: Authentication Documentation
- AUTH_OVERVIEW.md (456 lines)
- AUTH_IMPLEMENTATION.md (789 lines)
- AUTH_PATTERNS.md (623 lines)

Overlap Detection:
- JWT section appears in all 3 files (40% duplicate)
- Password hashing in OVERVIEW + IMPLEMENTATION (25% duplicate)
- Session management in all 3 files (35% duplicate)

Total Overlap: ~50% (1,300 duplicate lines)

Recommendation: Consolidate into 2 files
- AUTH_CONCEPTS.md (300 lines) - Why & What
- AUTH_IMPLEMENTATION.md (400 lines) - How & Code
```

### Phase 2: Planning

**2.1 Create Content Mapping Table**

| Old File | Content | Overlap % | New Location |
|----------|---------|-----------|--------------|
| FILE1.md | Auth concepts + JWT | 40% | AUTH_CONCEPTS.md |
| FILE2.md | Implementation + examples | 25% | AUTH_IMPLEMENTATION.md |
| FILE3.md | Patterns + anti-patterns | 35% | AUTH_IMPLEMENTATION.md |

**2.2 Define Target Structure**

```markdown
Target Files:

1. AUTH_CONCEPTS.md (~300 lines)
   - Authentication vs Authorization
   - Token-based auth (JWT, OAuth)
   - Session-based auth
   - When to use each

2. AUTH_IMPLEMENTATION.md (~400 lines)
   - JWT implementation (Python, Node)
   - Session implementation
   - Password hashing (bcrypt examples)
   - Common patterns
   - Anti-patterns to avoid
```

**2.3 Estimate Impact**

- **Before**: 1,868 lines, 50% overlap
- **After**: 700 lines, 0% overlap
- **Token Savings**: ~60% reduction per load
- **Files Archived**: 3
- **Broken References**: Estimate 5-10 (to be fixed)

### Phase 3: Consolidation

**3.1 Merge Strategy**

For high-overlap files:
```
1. Read all source files
2. Extract unique content sections
3. Organize by abstraction level (concept → reference → usage)
4. Merge similar sections (keep best version)
5. Remove redundant examples (keep most illustrative)
6. Update cross-references
```

For different abstraction levels:
```
1. Split by audience/purpose
2. Keep separation (concept vs implementation)
3. Add cross-references between files
4. Ensure no content duplication
```

**3.2 Systematic Merge Process**

```markdown
# Step-by-step for each topic cluster:

1. Create new target files with headers
2. Copy unique content from File A → Target
3. Copy unique content from File B → Target
4. Merge overlapping sections (best of both)
5. Remove redundant examples
6. Update cross-references
7. Verify 100% content preservation
8. Add version history
```

### Phase 4: Archive

**4.1 Archive Strategy**

```bash
# Create archive directory
mkdir -p docs/archive/YYYY-MM-consolidation/

# Move original files
mv docs/OLD_FILE1.md docs/archive/YYYY-MM-consolidation/
mv docs/OLD_FILE2.md docs/archive/YYYY-MM-consolidation/
mv docs/OLD_FILE3.md docs/archive/YYYY-MM-consolidation/

# Create archive README
cat > docs/archive/YYYY-MM-consolidation/README.md <<'EOF'
# Documentation Consolidation - YYYY-MM-DD

## Files Archived

1. OLD_FILE1.md (456 lines)
   - Replaced by: AUTH_CONCEPTS.md
   - Reason: 40% overlap with other files

2. OLD_FILE2.md (789 lines)
   - Replaced by: AUTH_IMPLEMENTATION.md
   - Reason: Consolidation to eliminate redundancy

3. OLD_FILE3.md (623 lines)
   - Merged into: AUTH_IMPLEMENTATION.md
   - Reason: Patterns belong with implementation

## Migration Guide

If you're looking for:
- Authentication concepts → AUTH_CONCEPTS.md
- JWT implementation → AUTH_IMPLEMENTATION.md
- Password hashing → AUTH_IMPLEMENTATION.md
- Session management → AUTH_IMPLEMENTATION.md

## Restoration

To restore: cp archive/YYYY-MM-consolidation/FILE.md docs/
EOF
```

### Phase 5: Verification

**5.1 Content Verification**

- [ ] All unique content preserved
- [ ] No broken internal references
- [ ] Cross-references updated
- [ ] Examples still accurate
- [ ] Code blocks flush-left (zero indent)

**5.2 Index Updates**

Update all index files:
- [ ] README.md
- [ ] AI_RULES.md or similar
- [ ] Navigation sidebars
- [ ] Search indexes

**5.3 Link Verification**

```bash
# Check for broken links to archived files
grep -r "OLD_FILE1.md" docs/ | grep -v archive/

# Verify new links work
grep -r "AUTH_CONCEPTS.md" docs/ | head -10
```

---

## Consolidation Patterns

### Pattern 1: High Overlap → Single File

**When**: >50% overlap, same topic
**Strategy**: Merge into single comprehensive file
**Example**: 3 VPN docs → 1 UNIFI_VPN_SETUP.md

### Pattern 2: Mixed Concerns → Split by Type

**When**: One massive file covering multiple aspects
**Strategy**: Split into concept/reference/usage
**Example**: BITWARDEN_SECRETS.md → 3 focused files

### Pattern 3: Different Abstraction → Keep Separate

**When**: Concept vs implementation vs reference
**Strategy**: Maintain separation, improve cross-refs
**Example**: AUTH_CONCEPTS.md + AUTH_IMPLEMENTATION.md

### Pattern 4: Historical Overlap → Archive Old

**When**: Old approach superseded by new
**Strategy**: Archive old, keep new only
**Example**: V1 docs archived when V2 active

---

## Metrics

### Success Metrics

```
Documentation Health Report
===========================

Before Consolidation:
- Total Files: 15
- Total Lines: 8,245
- Overlap Estimate: 45%
- Token Cost: ~35K/load

After Consolidation:
- Total Files: 8
- Total Lines: 4,800
- Overlap: 0%
- Token Cost: ~18K/load

Impact:
- Files Reduced: 47% (15 → 8)
- Lines Reduced: 42% (8,245 → 4,800)
- Token Savings: 49% (35K → 18K)
- Content Loss: 0%
```

### Quality Metrics

- **Overlap %**: 45% → 0%
- **Avg File Size**: 550 → 600 lines (better balance)
- **Files >800 lines**: 5 → 2 (large file reduction)
- **Broken References**: 0 (all fixed)
- **Cross-Ref Coverage**: 20% → 60% (better linking)

---

## Automation

### Overlap Detection Script

```python
#!/usr/bin/env python3
"""Detect documentation overlap."""

import re
from pathlib import Path
from difflib import SequenceMatcher

def calculate_overlap(file1: str, file2: str) -> float:
    """Calculate overlap percentage between two files."""
    text1 = Path(file1).read_text()
    text2 = Path(file2).read_text()

    # Compare text similarity
    matcher = SequenceMatcher(None, text1, text2)
    return matcher.ratio() * 100

def find_clusters(docs_dir: str, threshold: float = 30.0):
    """Find document clusters with high overlap."""
    files = list(Path(docs_dir).glob("*.md"))
    clusters = []

    for i, file1 in enumerate(files):
        for file2 in files[i+1:]:
            overlap = calculate_overlap(file1, file2)
            if overlap > threshold:
                clusters.append((file1, file2, overlap))

    return sorted(clusters, key=lambda x: x[2], reverse=True)

if __name__ == "__main__":
    clusters = find_clusters("docs/", threshold=30.0)
    print("High Overlap Clusters (>30%):")
    for file1, file2, overlap in clusters:
        print(f"  {overlap:.1f}% - {file1.name} + {file2.name}")
```

---

## Best Practices

1. **Always preserve content**: Archive originals, don't delete
2. **Measure twice, merge once**: Verify overlap before consolidating
3. **Update cross-references**: Fix all links to archived files
4. **Document rationale**: Explain why consolidation happened
5. **Gradual approach**: Consolidate one cluster at a time
6. **Test navigation**: Ensure users can find information
7. **Version history**: Track consolidation in file headers

---

## Related Skills

- documentation-audit: Detect consolidation candidates
- python-dev: Automation scripts

## Related Commands

- `/lint-docs` - Check documentation compliance

## References

- DOCUMENTATION_STANDARDS.md - Documentation best practices
- DOCUMENTATION_MAINTENANCE.md - Maintenance workflows

---

## Examples

### Example 1: Website Documentation

**User**: "Consolidate website development documentation"

**Agent**:
1. Analyzes 4 website docs (3,569 lines)
2. Detects 66% overlap
3. Plans 3-file structure
4. Merges systematically
5. Archives originals with README
6. Updates indexes
7. Verifies zero broken links

**Result**: 3 focused files, 0% overlap, 2,400 line reduction

### Example 2: API Documentation

**User**: "Too many API docs, consolidate"

**Agent**:
1. Analyzes API_OVERVIEW, API_REFERENCE, API_EXAMPLES
2. Finds 35% overlap
3. Consolidates to API.md (comprehensive)
4. Archives old files
5. Updates references

**Result**: Single source of truth, easier maintenance

### Example 3: Migration Guides

**User**: "Multiple V1→V2 migration guides exist"

**Agent**:
1. Reviews migration docs
2. Identifies redundant instructions
3. Creates single MIGRATION_V1_TO_V2.md
4. Archives scattered guides
5. Adds checklist format

**Result**: Clear migration path, no confusion

### Example 4: Fleet Website Consolidation (Real)

**User**: "Website docs have too much overlap"

**Agent**:
1. Analyzed 4 files:
   - WEBSITE_STRATEGY.md (892 lines)
   - WEBSITE_DEVELOPMENT.md (834 lines)
   - WEBSITE_DESIGN_SYSTEM.md (1,123 lines)
   - ASTRO_CLOUDFLARE_PATTERNS.md (720 lines)
2. Found 66% overlap in patterns/examples
3. Consolidated to 3 files:
   - WEBSITE_STRATEGY.md (300 lines) - When/Why
   - WEBSITE_DEVELOPMENT.md (600 lines) - How/Implementation
   - WEBSITE_DESIGN_SYSTEM.md (400 lines) - Design tokens/components
4. Archived ASTRO_CLOUDFLARE_PATTERNS.md (merged into DEVELOPMENT)
5. Updated knowledge-base/CLAUDE.md index
6. Fixed all cross-references

**Result**:
- 3,569 lines → 1,300 lines (64% reduction)
- 0% overlap
- Clearer navigation
- Faster AI context loading

### Example 5: VPN Documentation (Real)

**User**: "VPN docs scattered, consolidate"

**Agent**:
1. Analyzed 3 files:
   - UNIFI_VPN_OVERVIEW.md (234 lines)
   - UNIFI_VPN_SETUP.md (456 lines)
   - VPN_ROUTING_LESSONS.md (345 lines)
2. Found 45% overlap in setup instructions
3. Consolidated to 1 file:
   - UNIFI_VPN_SETUP.md (650 lines) - Complete guide
4. Archived OVERVIEW (concepts merged)
5. Kept VPN_ROUTING_LESSONS.md separate (different topic: troubleshooting)

**Result**:
- 3 files → 2 files
- Single source for VPN setup
- Lessons learned kept separate (appropriate)

### Example 6: Secrets Management Split (Real)

**User**: "BITWARDEN_SECRETS.md is too large"

**Agent**:
1. Analyzed 1 file:
   - BITWARDEN_SECRETS.md (1,234 lines)
2. Identified 3 distinct concerns:
   - Concepts (why use secrets management)
   - Reference (Bitwarden CLI API)
   - Implementation (sops, age, Infisical)
3. Split into 3 files:
   - SECRETS.md (300 lines) - Concepts
   - BITWARDEN_REFERENCE.md (400 lines) - CLI/API
   - SECRETS_IMPLEMENTATION.md (450 lines) - Tools/workflows
4. Archived original with migration README

**Result**:
- 1,234 lines → 1,150 lines (7% reduction)
- BUT: 3 focused files easier to navigate
- Each file has clear purpose
- AI loads only what's needed

---

## Advanced Techniques

### Content Deduplication Algorithm

```python
#!/usr/bin/env python3
"""Advanced overlap detection with section-level analysis."""

from pathlib import Path
from typing import List, Tuple
import re

def extract_sections(markdown: str) -> List[Tuple[str, str]]:
    """Extract sections (header + content) from markdown."""
    sections = []
    lines = markdown.split('\n')
    current_header = None
    current_content = []

    for line in lines:
        if re.match(r'^#{1,3}\s+', line):
            if current_header:
                sections.append((current_header, '\n'.join(current_content)))
            current_header = line
            current_content = []
        else:
            current_content.append(line)

    if current_header:
        sections.append((current_header, '\n'.join(current_content)))

    return sections

def find_duplicate_sections(files: List[Path]) -> dict:
    """Find sections that appear in multiple files."""
    section_map = {}

    for file_path in files:
        content = file_path.read_text()
        sections = extract_sections(content)

        for header, content in sections:
            normalized = content.strip()
            if normalized not in section_map:
                section_map[normalized] = []
            section_map[normalized].append((file_path, header))

    # Filter to only duplicates
    duplicates = {k: v for k, v in section_map.items() if len(v) > 1}
    return duplicates

if __name__ == "__main__":
    files = list(Path("docs/").glob("*.md"))
    duplicates = find_duplicate_sections(files)

    print(f"Found {len(duplicates)} duplicate sections")
    for content, locations in duplicates.items():
        if len(content) > 100:  # Only show substantial duplicates
            print(f"\nDuplicate section ({len(content)} chars):")
            for file_path, header in locations:
                print(f"  - {file_path.name}: {header}")
```

### Consolidation Decision Tree

```
Start
  |
  v
Multiple files on same topic?
  |
  |--No--> Keep separate
  |
  |--Yes--> Calculate overlap
             |
             v
          Overlap > 50%?
             |
             |--Yes--> Same abstraction level?
             |         |
             |         |--Yes--> Merge into single file
             |         |
             |         |--No--> Split by abstraction
             |                  (Concept/Reference/Usage)
             |
             |--No--> Overlap 30-50%?
                      |
                      |--Yes--> Extract common content
                      |         Create shared base doc
                      |
                      |--No--> Keep separate
                               Add cross-references
```

### Maintenance Schedule

```markdown
# Documentation Consolidation Schedule

## Monthly (Light Check)
- Run overlap detection script
- Flag any pairs with >30% overlap
- Add to consolidation backlog

## Quarterly (Review)
- Review consolidation backlog
- Prioritize by token cost
- Consolidate top 2-3 clusters

## After Major Release
- Full documentation audit
- Consolidate release-specific docs
- Archive deprecated content

## Metrics Tracking
- Total docs count (trend)
- Average file size (trend)
- Overlap percentage (target: <10%)
- Token cost per load (target: <20K)
```

---

## Troubleshooting

### Issue: Lost Content After Merge

**Symptom**: Users report missing information

**Diagnosis**:
```bash
# Compare before/after
diff -u archive/YYYY-MM/OLD_FILE.md docs/NEW_FILE.md
```

**Solution**:
1. Review diff output
2. Identify missing sections
3. Add back to consolidated file
4. Update archive README with "Known gaps"

### Issue: Broken Cross-References

**Symptom**: Links to old files don't work

**Diagnosis**:
```bash
# Find all references to archived files
grep -r "OLD_FILE.md" docs/ | grep -v archive/
```

**Solution**:
```bash
# Replace references
find docs/ -name "*.md" ! -path "*/archive/*" -exec sed -i '' 's/OLD_FILE.md/NEW_FILE.md/g' {} +

# Verify
grep -r "OLD_FILE.md" docs/ | grep -v archive/
```

### Issue: Users Can't Find Information

**Symptom**: "Where did the X documentation go?"

**Diagnosis**: Navigation unclear after consolidation

**Solution**:
1. Add migration guide to README.md
2. Create forwarding notes in archive README
3. Update search keywords
4. Add table of contents to large files

---

## Quality Checklist

Before marking consolidation complete:

- [ ] **Content Preservation**
  - All unique content from source files present
  - No information loss
  - Examples still accurate

- [ ] **Navigation**
  - README.md updated
  - Archive README explains migration
  - Clear file names

- [ ] **References**
  - All internal links updated
  - No broken references
  - Cross-references added where helpful

- [ ] **Code Quality**
  - Code blocks flush-left (no leading spaces)
  - Examples tested
  - Language tags present

- [ ] **Metrics**
  - Line count reduction calculated
  - Overlap percentage measured
  - Token savings estimated

- [ ] **Documentation**
  - Consolidation rationale documented
  - Version history updated
  - Last Updated date current

---

## Success Stories

### Fleet Standards Documentation (2026-01)
- **Before**: 23 knowledge-base files, 12,456 lines
- **After**: 18 knowledge-base files, 9,234 lines
- **Reduction**: 26% fewer lines, 5 files archived
- **Impact**: Faster AI context loading, clearer navigation

### Website Documentation (2026-02)
- **Before**: 4 overlapping files, 3,569 lines
- **After**: 3 focused files, 1,300 lines
- **Reduction**: 64% fewer lines
- **Impact**: Clear separation (strategy/implementation/design)

### VPN Documentation (2026-01)
- **Before**: 3 scattered files, 1,035 lines
- **After**: 2 focused files, 895 lines
- **Reduction**: 14% fewer lines
- **Impact**: Single source for setup, separate troubleshooting

---

**Total Documentation Impact (Fleet)**:
- **Lines Saved**: ~5,000 lines
- **Token Savings**: ~40% per documentation load
- **Files Archived**: 8 files
- **Content Lost**: 0%
- **User Complaints**: 0 (all content preserved, better organized)
