---
description: Summarize the current session state and prepare a handoff document for the next agent/session.
---

# Context Handoff Protocol

You are preparing to hand off this work to another agent (or a fresh session of yourself). Your goal is to maximize the *speed to resumption* for the next agent.

## Steps

1.  **Analyze the Session**:
    -   What was the original goal?
    -   What has been successfully completed?
    -   What is currently broken or in progress?
    -   What important context (file paths, specific errors, constraints) must be preserved?

2.  **Update Tracking (if applicable)**:
    -   If `task.md` exists, ensure all completed items are marked `[x]`.

3.  **Generate/Update `HANDOFF.md`**:
    -   **File**: Create or overwrite `HANDOFF.md` in the project root.
    -   **Content**:
        ```markdown
        # Session Handoff: [YYYY-MM-DD HH:MM]

        ## Goal
        [One sentence summary of the objective]

        ## Status
        - [ ] Working on: [Current active task]
        - [x] Completed: [Major milestones from this session]
        - [!] Blockers: [Any specific errors or missing info]

        ## Context & Decisions
        - **Files**: [List of critical files modified]
        - **Decisions**: [Key technical decisions made]
        - **Gotchas**: [Specific things to watch out for]

        ## Next Steps
        1. [Step 1]
        2. [Step 2]
        ```

4.  **Final Action**:
    -   Print: "Handoff document prepared at `HANDOFF.md`. You can safely end this session."
