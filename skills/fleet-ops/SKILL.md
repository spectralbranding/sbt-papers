---
name: fleet-ops
description: Management of the 4-Mac fleet (fmini, dbook, dmini, fbook), deployment, and sync.
---

# Fleet Operations Skill

> **Fleet**: fmini (Hub), dbook (Portable), dmini (Support), fbook (Research)

## Architecture

| Machine | Role | Chip | IP | Services |
|---------|------|------|-----|----------|
| **fmini** | Hub/Server | M4 Pro 64GB | 192.168.1.7 | Ollama, LanceDB, ntfy, MCP |
| **dbook** | Portable Dev | M4 Pro 48GB | Dynamic | Claude Code, local Ollama |
| **dmini** | Support Node | Intel 32GB | 192.168.1.200 | Plex, backups, monitoring |
| **fbook** | Knowledge Terminal | Intel 16GB | 192.168.1.12 | Claude Desktop, research |

## Tier System

| Tier | Machines | Purpose |
|------|----------|---------|
| **Silicon Primary** | fmini, dbook | AI, RAG, development |
| **Intel Support** | dmini, fbook | Backup, monitoring, research |

## Critical Commands

### Connection Modes
```bash
switch_mode home    # Connect to fmini (192.168.1.7)
switch_mode travel  # Use localhost
```

### Synchronization
```bash
sync_fleet          # Shell alias for sync_manager.sh
/fleet-sync         # Slash command equivalent
```

### Deployment
```bash
./distribute_rules.sh                    # Update all projects
./setup_mac.sh && source ~/.zshrc        # Apply to current machine
```

## Network Services

| Service | Host | Port | URL |
|---------|------|------|-----|
| Ollama | fmini | 11434 | http://192.168.1.7:11434 |
| ntfy | fmini | 8090 | http://192.168.1.7:8090 |
| Plex | dmini | 32400 | http://192.168.1.200:32400 |
| Fleet Monitor | dmini | 8280 | http://192.168.1.200:8280 |

## Common Tasks

### Adding a New Machine
1. Clone `fleet-standards`.
2. Run `./setup_mac.sh`.
3. Restart terminal.
4. Run `./distribute_rules.sh`.

### Fleet Health Check
```bash
~/projects/fleet-standards/scripts/fleet_health.sh
```

### Pull Updates on All Machines
```bash
for m in fmini dbook dmini fbook; do
    ssh d@$m.local "cd ~/projects/fleet-standards && git pull"
done
```

## Related Documentation

- `knowledge-base/FLEET_ROLES.md` - Detailed machine roles
- `knowledge-base/PORT_ALLOCATION.md` - Port reservations
- `knowledge-base/SERVICES.md` - launchd services
- `knowledge-base/INSTALL.md` - Installation strategy
