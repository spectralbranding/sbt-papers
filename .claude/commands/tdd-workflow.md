---
description: Test-first implementation pattern
---

TDD for: $ARGUMENTS

1. Write tests based on expected input/output
   - Explicit: This is TDD, avoid mock implementations
   - Commit tests first

2. Run tests, confirm they fail
   - No implementation yet

3. Implement until tests pass
   - Iterate: code → test → fix → test
   - Use subagent to verify no overfitting

4. Commit implementation
   - Link to test commit in message
