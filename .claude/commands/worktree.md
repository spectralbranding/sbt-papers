# /worktree

Create git worktree for parallel work on multiple branches.

## Usage

```
/worktree [branch]
```

## Arguments

- `branch`: Name of the branch to create worktree for

## Instructions

When invoked, Claude should:

1. Parse branch name from arguments: `$ARGUMENTS`
2. Create worktree in sibling directory
3. Report the new worktree location

```bash
# Create worktree
git worktree add ../[project]-[branch] [branch]
```

## What It Does

Git worktrees allow working on multiple branches simultaneously without stashing or switching. Each worktree is a separate directory with its own working copy.

## Output Format

```
=== Creating Worktree ===

Branch: feature/auth
Location: ../project-feature-auth

Created worktree at: /Users/d/projects/project-feature-auth

To switch to worktree:
  cd ../project-feature-auth

To list all worktrees:
  git worktree list

To remove when done:
  git worktree remove ../project-feature-auth
```

## Use Cases

1. **Parallel Development**: Work on feature while fixing bug
2. **Code Review**: Check out PR branch without switching
3. **Comparison**: Compare implementations side-by-side
4. **Engine Mode**: Engine creates worktree for isolation

## Worktree Management

List worktrees:
```bash
git worktree list
```

Remove worktree:
```bash
git worktree remove ../path-to-worktree
```

Prune stale worktrees:
```bash
git worktree prune
```

## Directory Convention

Worktrees are created as siblings with naming:
- `project-branch-name`
- Example: `agent-system-feature-auth`

## Related

- [GIT.md](../knowledge-base/GIT.md) - Git workflow
- `/engine` - Uses worktrees for isolation
