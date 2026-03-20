# /parallel-work

Set up infrastructure for parallel Claude sessions with conflict prevention.

## Usage

```
/parallel-work [command] [args]
```

## Commands

- `setup [branch]` - Create worktree and session for parallel work
- `status` - Show active sessions and claimed tasks
- `claim [task]` - Claim a task for current session (prevents conflicts)
- `release [task]` - Release a claimed task
- `cleanup` - Remove stale sessions and lock files

## Instructions

When invoked, Claude should:

1. Parse command and arguments from: `$ARGUMENTS`
2. Manage `.claude-active-sessions` lock file
3. Coordinate with git worktrees
4. Use zellij for session management when available

## Session Lock File Format

```json
// .claude-active-sessions (at project root)
{
  "sessions": [
    {
      "id": "abc123",
      "worktree": "project-feature-auth",
      "started": "2025-12-27T10:00:00Z",
      "tasks_claimed": ["implement auth API", "write auth tests"],
      "files_modified": ["src/auth/*.py"]
    }
  ]
}
```

## Workflow: Setup New Session

```bash
# 1. Create worktree
git worktree add ../[project]-[branch] [branch]

# 2. Generate session ID
SESSION_ID=$(openssl rand -hex 4)

# 3. Update lock file (create if needed)
# Add session entry to .claude-active-sessions

# 4. Launch zellij (if available)
zellij --layout claude-dev --session [project]-[branch]
```

## Workflow: Check Before Editing

Before modifying any file, check if another session has claimed it:

```bash
# Parse .claude-active-sessions
# If file is in another session's files_modified -> warn user
```

## Output Format

### /parallel-work setup feature-auth

```
=== Parallel Work Session ===

Session ID: abc123
Branch: feature/auth
Worktree: ../project-feature-auth
Started: 2025-12-27T10:00:00Z

Lock file updated: .claude-active-sessions

To claim tasks:
  /parallel-work claim "implement auth API"

To start zellij session:
  zellij --layout claude-dev --session project-feature-auth
```

### /parallel-work status

```
=== Active Sessions ===

Session: abc123
  Worktree: project-feature-auth
  Started: 2 hours ago
  Tasks: implement auth API, write auth tests
  Files: src/auth/*.py

Session: def456
  Worktree: project-feature-dashboard
  Started: 1 hour ago
  Tasks: dashboard UI components
  Files: src/dashboard/*.tsx
```

## Conflict Prevention Rules

1. **One session per worktree** - Cannot start second session in same worktree
2. **Task claiming** - Use `claim` before working on multi-file changes
3. **File ownership** - Check lock file before editing files
4. **Merge via PRs** - Each worktree merges to main via pull request

## Zellij Integration

Start parallel sessions with zellij layouts:

```bash
# Single Claude session with terminal
zellij --layout claude-dev --session project-feature

# Side-by-side for monitoring
zellij --layout parallel-claude --session parallel-work
```

## Cleanup

When done with a parallel session:

```bash
# 1. Commit and push changes
git add . && git commit -m "feat: complete auth" && git push

# 2. Remove session from lock file
/parallel-work cleanup

# 3. Remove worktree
git worktree remove ../project-feature-auth

# 4. Create PR
gh pr create
```

## Related

- [/worktree](worktree.md) - Basic worktree creation
- [GIT.md](../knowledge-base/GIT.md) - Git workflow
- [PARALLEL_WORK.md](../knowledge-base/PARALLEL_WORK.md) - Full protocol
