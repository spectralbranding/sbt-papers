# /review-traces

Interactive review of pending decision traces.

## Usage

```
/review-traces
```

## Instructions

When invoked, Claude should:

1. First run the weekly trace review script to show status:
   ```bash
   ~/projects/fleet-standards/scripts/weekly_trace_review.sh --test
   ```

2. Then scan all projects for pending traces
3. Display traces grouped by project
4. For each trace, offer actions: promote, archive, skip

## Review Process

### Step 1: Show Summary

```
=== Decision Trace Review ===

Pending traces from last 7 days: 5
New patterns promoted: 2

Projects with pending traces:
  - agent-system: 3 traces
  - fleet-standards: 2 traces
```

### Step 2: Review Each Trace

For each pending trace, display:

```
--- Trace 1/5 ---
Project: agent-system
Type: pattern
Date: 2025-12-26
Title: Use repository pattern for data access

Description:
  Encapsulate all Supabase queries in repository classes for testability

Tags: python, architecture, supabase

Actions:
  [P]romote - Add to global patterns
  [A]rchive - Not worth keeping
  [S]kip - Review later
  [Q]uit - Exit review

Choice:
```

### Step 3: Handle Actions

**Promote**:
- Copy trace to `decision-graph/pending/`
- Mark `promotion_status: "promoted"` in original
- Inform user to finalize in `decision-graph/patterns/`

**Archive**:
- Mark `promotion_status: "archived"` in trace
- Move to `decision-graph/archive/` if configured

**Skip**:
- Leave unchanged, move to next trace

## Promotion Workflow

When promoting a trace:

1. Create markdown file in `decision-graph/pending/[title-slug].md`
2. Use template format from `decision-graph/patterns/TEMPLATE.md`
3. Update original trace JSON with promotion status
4. Run `scripts/generate_pattern_index.py` to update index

## Completion

After reviewing all traces:

```
=== Review Complete ===

Reviewed: 5 traces
  - Promoted: 2
  - Archived: 1
  - Skipped: 2

Promoted patterns are in: decision-graph/pending/
Run 'distribute_rules.sh' to sync across fleet.
```

## Related Scripts

- `scripts/weekly_trace_review.sh` - Automated reminder
- `scripts/trace_maintenance.py` - Cleanup and stats
- `scripts/promote_trace.py` - Promotion helper
