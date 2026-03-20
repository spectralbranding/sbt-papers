# /discover-patterns

Mine decision traces across all projects to discover fleet-wide patterns, lessons, and contradictions.

## Usage

```
/discover-patterns
```

## What It Does

Scans all `.claude-decisions/traces/` directories across the fleet to:

1. Count traces by type (patterns, exceptions, lessons)
2. Identify most common decision topics
3. Surface recent high-value patterns
4. Detect potential contradictions in decisions
5. Provide actionable recommendations

## Output Sections

### Summary Statistics
- Total trace counts by type
- Distribution of patterns vs lessons vs exceptions

### Top Pattern Topics
- What decisions we make most often
- Areas with established patterns

### Top Lesson Topics
- What we learn from most frequently
- Common learning areas across projects

### Recent High-Value Patterns
- Last 5 patterns captured
- Shows decision evolution over time

### Contradictions Detected
- Decisions with same tags but different approaches
- Flags potential inconsistencies to review

### Recommendations
- Specific actions based on analysis
- Suggestions for improving decision system

## Use Cases

**Weekly review**: "What patterns emerged this week?"
```
/discover-patterns
```

**Onboarding**: "What are our key patterns?"
```
/discover-patterns
# Review top pattern topics
```

**Consolidation**: "Do we have conflicting decisions?"
```
/discover-patterns
# Check contradictions section
```

**Documentation**: "What should go in AGENT_QUICK_REF.md?"
```
/discover-patterns
# Review top patterns and lessons
```

## Example Output

```
=== Decision Trace Pattern Analysis ===

Total Traces: 47
Patterns: 28
Exceptions: 5
Lessons: 14

=== Top Pattern Topics ===
python: 8
documentation: 6
security: 4
testing: 3
deployment: 3

=== Recent High-Value Patterns ===

[python] Use uv for all Python dependency management
  Rationale: Faster than pip, better lock files, consistent across fleet
  Project: fleet-standards
  Date: 2026-02-05

[documentation] Architecture diagrams save 80% tokens
  Rationale: Reading .mmd files instead of 5-10 docs dramatically reduces context
  Project: fleet-standards
  Date: 2026-02-05

=== Contradictions Detected ===

Tags: ['testing', 'python']
  - Use pytest for all tests (agent-system)
  - Prefer unittest for simplicity (old-project)

=== Recommendations ===
- Use /search-decisions for specific topics
- Review contradictions and consolidate decisions
- Review traces at: .claude-decisions/traces/
```

## Implementation Details

Uses MCP agent-system tools:
- `search_traces_global('')` - Scans all projects
- Analyzes trace metadata (type, tags, timestamps)
- Detects contradictions via tag grouping
- Generates actionable insights

## Related Commands

- `/trace` - Capture new decisions
- `/search-decisions` - Search for specific patterns
- `/show-traces` - View traces in current project
- `/review-traces` - Review and promote traces

## See Also

- knowledge-base/DECISION_TRACES.md - Decision system overview
- knowledge-base/OPERATIONAL_DECISIONS.md - Fleet-wide decisions
