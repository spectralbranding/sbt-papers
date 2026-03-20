# /engine

Autonomous execution orchestrator for complex, multi-step projects.

## Usage

```
/engine [subcommand] [args]
```

## Subcommands

| Command | Description | Intel Compatible |
|---------|-------------|------------------|
| `start [goal]` | Begin autonomous execution | M4 Pro only |
| `plan [goal]` | Create implementation plan only | Yes |
| `status` | Show current engine state | Yes |
| `pause` | Pause execution, save checkpoint | Yes |
| `resume` | Resume from last checkpoint | M4 Pro only |

## Instructions

### /engine start [goal]

**M4 Pro Only** - Full autonomous execution.

1. Check machine capability (Apple Silicon required for full mode)
2. Create engine branch: `git checkout -b engine/[goal-slug]`
3. Initialize `.claude-engine/` directory structure
4. Break goal into tasks using TodoWrite
5. Execute tasks sequentially with quality gates
6. Save checkpoints every N tasks (per config)
7. Run QA/Security/Docs subagents periodically

### /engine plan [goal]

**Intel Compatible** - Planning only, no execution.

1. Analyze the goal and codebase
2. Create `implementation_plan.md` with:
   - Overview of the goal
   - Step-by-step tasks
   - Files to modify
   - Dependencies and risks
   - Estimated complexity
3. Do NOT execute the plan
4. User can then execute manually or transfer to M4 machine

### /engine status

Show current engine state from `.claude-engine/state.json`:

```
=== Engine Status ===

Status: running
Goal: "Implement user authentication"
Branch: engine/implement-user-auth
Progress: 5/12 tasks (42%)
Current Task: Add password hashing
Last Checkpoint: 2025-12-26T10:30:00Z
Runtime: 45 minutes
```

### /engine pause

1. Save current state to checkpoint
2. Update state.json status to "paused"
3. Commit work in progress
4. Output resume instructions

### /engine resume

1. Load last checkpoint from `.claude-engine/checkpoints/`
2. Verify branch and state
3. Continue from last completed task
4. Update state to "running"

## State Schema

`.claude-engine/state.json`:

```json
{
  "version": "1.0",
  "goal": "User-provided goal",
  "status": "running|paused|completed|failed",
  "current_task": 5,
  "total_tasks": 12,
  "started_at": "2025-12-26T09:00:00Z",
  "last_checkpoint": "2025-12-26T10:30:00Z",
  "branch": "engine/goal-slug",
  "machine": "fmini",
  "errors": []
}
```

## Directory Structure

```
.claude-engine/
  state.json         # Current state
  todos.json         # Task queue
  checkpoints/       # Resume points
    checkpoint-001.json
  logs/              # Execution logs
    2025-12-26.log
```

## Configuration

Settings from `~/projects/fleet-standards/configs/engine.json`:

| Setting | Default | Description |
|---------|---------|-------------|
| `max_iterations` | 100 | Max tasks before auto-pause |
| `checkpoint_interval` | 10 | Tasks between checkpoints |
| `timeout_minutes` | 180 | Max runtime (3 hours) |
| `require_tests` | true | Tests must pass |
| `require_docs` | true | Docs must be updated |

## Safety Features

- Never pushes automatically
- Protected branches: main, master, production
- Max 3-hour runtime
- Checkpoint recovery
- QA gates every 5 tasks
- Security scan every 10 tasks

## Intel Machine Workflow

On Intel machines (dmini, fbook), use plan-only mode:

```
/engine plan "Add feature X"
# Review implementation_plan.md
# Execute manually or transfer to Apple Silicon
```

## Examples

```
/engine start "Add user profile with avatar upload"
/engine plan "Refactor API to async/await"
/engine status
/engine pause
/engine resume
```

## Related

- [ENGINE.md](../knowledge-base/ENGINE.md) - Full documentation
- [engine.json](../configs/engine.json) - Configuration
- ENGINE_ARCHITECTURE.md - Technical design
