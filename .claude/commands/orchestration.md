# /orchestration

Set up multi-session orchestration infrastructure with templates and tracking.

## Usage

```
/orchestration [command] [args]
```

## Commands

- `init` - Initialize orchestration infrastructure in current project
- `session [name]` - Create a new session todo file from template
- `status` - Show orchestration status (phases, sessions, completion)
- `verify [phase]` - Verify phase readiness for merging

## Instructions

When invoked, Claude should:

1. Parse command and arguments from: `$ARGUMENTS`
2. Execute the appropriate workflow based on command
3. Update tracking files as needed
4. Provide clear output with next steps

## Workflow: /orchestration init

Initialize orchestration infrastructure in the current project:

```bash
# 1. Determine project root (find .git directory)
PROJECT_ROOT=$(git rev-parse --show-toplevel)

# 2. Create .claude directory if needed
mkdir -p "$PROJECT_ROOT/.claude/sessions"
mkdir -p "$PROJECT_ROOT/.claude/templates"

# 3. Copy orchestration template
cp ~/projects/fleet-standards/knowledge-base/ORCHESTRATION_TEMPLATE.md \
   "$PROJECT_ROOT/.claude/PARALLEL_WORK_ORCHESTRATION.md"

# 4. Copy quality bypass tracking template
cp ~/projects/fleet-standards/.claude/templates/QUALITY_BYPASSES.md \
   "$PROJECT_ROOT/.claude/QUALITY_BYPASSES.md"

# 5. Update .gitignore if needed
if ! grep -q "!.claude/sessions/" "$PROJECT_ROOT/.gitignore"; then
    echo "
# Claude orchestration files (tracked)
.claude/*
!.claude/commands/
!.claude/sessions/
!.claude/PARALLEL_WORK_ORCHESTRATION.md
!.claude/QUALITY_BYPASSES.md" >> "$PROJECT_ROOT/.gitignore"
fi

# 6. Commit the setup
git add .claude/ .gitignore
git commit -m "Initialize orchestration infrastructure

Added:
- PARALLEL_WORK_ORCHESTRATION.md (ready to customize)
- QUALITY_BYPASSES.md (tracking template)
- sessions/ directory (for session todos)
- .gitignore entries to track orchestration files

Next: Edit PARALLEL_WORK_ORCHESTRATION.md to plan phases and sessions.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

**Output:**
```
=== Orchestration Infrastructure Initialized ===

Created:
  ✅ .claude/PARALLEL_WORK_ORCHESTRATION.md (edit to plan your orchestration)
  ✅ .claude/QUALITY_BYPASSES.md (track pre-commit bypasses)
  ✅ .claude/sessions/ (directory for session todos)
  ✅ .gitignore updated (orchestration files tracked)

Next steps:
  1. Edit .claude/PARALLEL_WORK_ORCHESTRATION.md
     - Define phases and sessions
     - Allocate token budgets
     - Set priorities

  2. Create session todos:
     /orchestration session phase1a-security-auth

  3. Start working:
     Open each session todo and begin implementation

Documentation:
  - Template: knowledge-base/ORCHESTRATION_TEMPLATE.md
  - Token budgets: knowledge-base/SESSION_HANDOFF.md
  - Pre-commit: knowledge-base/PRE_COMMIT_MANAGEMENT.md
```

## Workflow: /orchestration session [name]

Create a new session todo file from template:

```bash
# 1. Validate session name format
SESSION_NAME="$1"
if [[ ! "$SESSION_NAME" =~ ^phase[0-9]+[a-z]?-[a-z-]+$ ]]; then
    echo "Error: Session name must match pattern: phase1a-description"
    exit 1
fi

# 2. Create session todo file
PROJECT_ROOT=$(git rev-parse --show-toplevel)
SESSION_FILE="$PROJECT_ROOT/.claude/sessions/${SESSION_NAME}.todo.md"

# 3. Write session template
cat > "$SESSION_FILE" <<'EOF'
# Session: [SESSION_NAME]

**Status**: ⚪ Not Started
**Branch**: `feature/[session-name]`
**Estimated Budget**: [XX]K tokens
**Actual Usage**: TBD

---

## Prerequisites

- [ ] Phase [N-1] merged to main (if applicable)

---

## GIT SETUP (run at session start)

```bash
git checkout main && git pull origin main
git checkout -b feature/[session-name]
```

---

## Tasks

### TODO
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### In Progress
(none)

### Completed
(none)

---

## Session Notes

(Add notes, blockers, decisions here)

---

## Completion Checklist

- [ ] All tasks completed
- [ ] Tests passing
- [ ] Pre-commit checks passing (or bypasses documented)
- [ ] Changes committed to feature branch
- [ ] Branch pushed to origin
- [ ] Session status updated to Complete
EOF

# 4. Replace placeholders
sed -i '' "s/\[SESSION_NAME\]/$SESSION_NAME/g" "$SESSION_FILE"

# 5. Add to git
git add "$SESSION_FILE"
```

**Output:**
```
=== Session Created ===

File: .claude/sessions/phase1a-security-auth.todo.md

Next steps:
  1. Edit the session file:
     - Set estimated token budget
     - Define specific tasks
     - Add prerequisites

  2. Start the session:
     - Run the GIT SETUP commands
     - Mark session status as "In Progress"
     - Begin working on tasks

  3. Track progress:
     - Move tasks from TODO → In Progress → Completed
     - Update session notes with decisions
     - Document any pre-commit bypasses
```

## Workflow: /orchestration status

Show status of all orchestration sessions:

```bash
# 1. Find all session todo files
PROJECT_ROOT=$(git rev-parse --show-toplevel)
SESSIONS=$(find "$PROJECT_ROOT/.claude/sessions" -name "*.todo.md" | sort)

# 2. Parse status from each file
for SESSION_FILE in $SESSIONS; do
    SESSION_NAME=$(basename "$SESSION_FILE" .todo.md)
    STATUS=$(grep "^\*\*Status\*\*:" "$SESSION_FILE" | sed 's/.*Status\*\*: //')
    BRANCH=$(grep "^\*\*Branch\*\*:" "$SESSION_FILE" | sed 's/.*`\(.*\)`.*/\1/')
    BUDGET=$(grep "^\*\*Estimated Budget\*\*:" "$SESSION_FILE" | sed 's/.*Budget\*\*: //')

    echo "Session: $SESSION_NAME"
    echo "  Status: $STATUS"
    echo "  Branch: $BRANCH"
    echo "  Budget: $BUDGET"
    echo ""
done

# 3. Check orchestration document for phase structure
if [ -f "$PROJECT_ROOT/.claude/PARALLEL_WORK_ORCHESTRATION.md" ]; then
    echo "Orchestration Plan: .claude/PARALLEL_WORK_ORCHESTRATION.md"
fi
```

**Output:**
```
=== Orchestration Status ===

Session: phase1a-security-auth
  Status: ⚪ Not Started
  Branch: feature/phase1a-security-auth
  Budget: 60K tokens

Session: phase1b-security-secrets
  Status: 🟢 Complete
  Branch: feature/phase1b-security-secrets
  Budget: 50K tokens

Session: phase2a-quality-todos
  Status: 🟡 In Progress (45%)
  Branch: feature/phase2a-quality-todos
  Budget: 70K tokens

Orchestration Plan: .claude/PARALLEL_WORK_ORCHESTRATION.md
```

## Workflow: /orchestration verify [phase]

Verify a phase is ready for merging (all sessions complete):

```bash
# 1. Find all sessions for the phase
PHASE="$1"
PROJECT_ROOT=$(git rev-parse --show-toplevel)
SESSIONS=$(find "$PROJECT_ROOT/.claude/sessions" -name "phase${PHASE}*.todo.md" | sort)

if [ -z "$SESSIONS" ]; then
    echo "Error: No sessions found for phase $PHASE"
    exit 1
fi

# 2. Check each session status
INCOMPLETE=0
TOTAL=0

for SESSION_FILE in $SESSIONS; do
    TOTAL=$((TOTAL + 1))
    SESSION_NAME=$(basename "$SESSION_FILE" .todo.md)

    if grep -q "Status\*\*:.*Complete" "$SESSION_FILE"; then
        echo "✅ $SESSION_NAME: Complete"
    else
        echo "❌ $SESSION_NAME: Not complete"
        INCOMPLETE=$((INCOMPLETE + 1))
    fi
done

echo ""
if [ $INCOMPLETE -eq 0 ]; then
    echo "🎉 Phase $PHASE is ready to merge! ($TOTAL/$TOTAL sessions complete)"
    echo ""
    echo "Recommended merge order:"
    for SESSION_FILE in $SESSIONS; do
        SESSION_NAME=$(basename "$SESSION_FILE" .todo.md)
        BRANCH=$(grep "^\*\*Branch\*\*:" "$SESSION_FILE" | sed 's/.*`\(.*\)`.*/\1/')
        echo "  git merge --no-ff $BRANCH"
    done
else
    echo "⚠️  Phase $PHASE has $INCOMPLETE incomplete session(s)"
    echo "Complete all sessions before merging."
fi
```

**Output:**
```
=== Phase 1 Verification ===

✅ phase1a-security-auth: Complete
✅ phase1b-security-secrets: Complete
✅ phase1c-type-hints: Complete

🎉 Phase 1 is ready to merge! (3/3 sessions complete)

Recommended merge order:
  git merge --no-ff feature/phase1a-security-auth
  git merge --no-ff feature/phase1b-security-secrets
  git merge --no-ff feature/phase1c-type-hints
```

## Error Handling

**Project not initialized:**
```
Error: Orchestration not initialized.
Run: /orchestration init
```

**Invalid session name:**
```
Error: Session name must match pattern: phase1a-description
Examples:
  - phase1a-security-auth
  - phase2b-docs-refactor
  - phase3-testing
```

**No sessions for phase:**
```
Error: No sessions found for phase 1
Check .claude/sessions/ directory for available sessions.
```

## Integration with Other Commands

**Pre-commit bypasses:**
```bash
# When bypassing pre-commit, add to quality log
/orchestration init  # Creates QUALITY_BYPASSES.md
# Then document bypasses in that file
```

**Parallel work:**
```bash
# Use with /parallel-work for worktrees
/parallel-work setup phase1a-security-auth
/orchestration session phase1a-security-auth
# Work in parallel on different sessions
```

## Related

- [ORCHESTRATION_TEMPLATE.md](../knowledge-base/ORCHESTRATION_TEMPLATE.md) - Full template
- [SESSION_HANDOFF.md](../knowledge-base/SESSION_HANDOFF.md) - Token budgets
- [PRE_COMMIT_MANAGEMENT.md](../knowledge-base/PRE_COMMIT_MANAGEMENT.md) - Bypass tracking
- [PARALLEL_WORK.md](../knowledge-base/PARALLEL_WORK.md) - Worktree coordination
