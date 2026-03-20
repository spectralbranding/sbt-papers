# App Settings Compliance Check

Check if this machine's application settings comply with fleet standards.

## Instructions

1. First, identify this machine:
```bash
scutil --get LocalHostName
```

2. Read the compliance requirements:
```bash
cat ~/projects/fleet-standards/knowledge-base/APP_SETTINGS.md
```

3. Check each application configuration:

### Claude Code MCP
```bash
# Project level (in current directory)
cat .mcp.json 2>/dev/null || echo "MISSING: .mcp.json"

# Claude Code status
claude mcp list
```

### Continue Extension
```bash
cat ~/.continue/config.json
```

Expected: `mcpServers` array with `agent-system` and `context7`

### Roo-Cline
```bash
cat ~/Library/Application\ Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json
```

Expected: `mcpServers` object with `agent-system` and `context7`

### Claude Desktop
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Expected: `mcpServers` with `agent-system`

### Ollama (fmini/dbook only)
```bash
curl -s http://localhost:11434/api/tags | head -20
ollama list | grep nomic
```

### agent-system Index
```bash
# Check if documents are indexed
cd ~/projects/agent-system && uv run python -c "
from core.vector_store import VectorStore
store = VectorStore()
print(f'Indexed documents: {store.count()}')
"
```

4. Check terminology in configs:
- Hostnames should be lowercase: `fmini`, `dbook`, `dmini`, `fbook`
- References should say "2-machine M4 Pro fleet" not "4-device ecosystem"

5. Generate compliance report with status for each check.

## CRITICAL: Project-Specific Exceptions

Before "fixing" any configuration, check if it has intentional customizations:

1. Check for `PROJECT_CONTEXT.md` in project root
2. Check CI workflow for custom env vars (don't overwrite if present)
3. Never replace a working config with a "standard" one that would break functionality

Known exceptions:
- `ma-production`: Custom CI env vars for sops decryption
- `hungry-games`: Custom CI env vars for sops decryption

## Fix Commands

If issues found:

```bash
# Fix project MCP configs
cd ~/projects/fleet-standards && ./distribute_rules.sh

# Run ingestion if agent-system shows 0 documents
cd ~/projects/agent-system && uv run bin/ingest.py --prune

# Restart Ollama if embeddings failing
pkill -f ollama && sleep 2 && ollama serve &
```

## Output Format

Provide a summary table:

| Component | Status | Issue | Fix |
|-----------|--------|-------|-----|
| .mcp.json | OK/MISS/WARN | Description | Command |
| Continue | OK/MISS/WARN | Description | Command |
| Roo-Cline | OK/MISS/WARN | Description | Command |
| Claude Desktop | OK/MISS/WARN | Description | Command |
| Ollama | OK/WARN | Description | Command |
| agent-system | OK/WARN | Description | Command |
