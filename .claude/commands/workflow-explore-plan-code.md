---
description: Standard workflow for complex features
---

Feature: $ARGUMENTS

Phase 1: EXPLORE (read-only, no code)
- Analyze relevant files, git history, decision-traces
- Use subagent if >10 files involved
- Deliverable: exploration-summary.md

Phase 2: PLAN (think hard - extended budget)
- Design architecture with 3 alternative approaches
- Document in designs/[feature].md
- Wait for approval

Phase 3: CODE (implement)
- Write code following approved plan
- Test incrementally
- Commit with semantic versioning

Phase 4: DOCUMENT
- Update CHANGELOG.md
- Update relevant knowledge-base/ docs
- Create decision-trace if architectural
