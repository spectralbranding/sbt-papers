# /fleet-sync

Synchronize git repositories across the fleet.

## Usage

```
/fleet-sync
```

## Instructions

When invoked, Claude should run the sync manager script:

```bash
~/projects/fleet-standards/sync_manager.sh
```

## What It Does

1. Iterates through all projects in `~/projects/`
2. For each git repository:
   - Fetches latest from remote
   - Shows status (ahead/behind)
   - Optionally pulls changes
3. Reports sync status across fleet

## Output Format

```
=== Fleet Git Sync ===

Syncing projects in ~/projects/...

[OK] agent-system - up to date
[OK] fleet-standards - up to date
[!]  hungry-games - 2 commits behind
[!]  ma-production - uncommitted changes

Summary:
  - Up to date: 2
  - Behind: 1
  - Dirty: 1

Run 'git pull' in behind repos to update.
```

## Related Commands

- `/ingest` - Re-index after sync
- `distribute_rules.sh` - Sync config files
