# Token Dashboard

**Purpose**: Display current session token usage and context window statistics
**Usage**: `/token-dashboard`
**Category**: Session Management

---

## Overview

Shows real-time token usage, context window pressure, and cost projections for the current Claude Code session.

## Output

```
Token Usage Dashboard
=====================

Session Information:
- Model: Claude Sonnet (latest)
- Session Duration: 1h 23m
- Started: 2026-02-05 10:15:32

Token Usage:
- Input Tokens:  45,234 (22.6%)
- Output Tokens: 12,456 (6.2%)
- Total Tokens:  57,690 (28.8%)

Context Window:
- Capacity: 200,000 tokens
- Used: 57,690 tokens (28.8%)
- Remaining: 142,310 tokens (71.2%)
- Status: ✅ Healthy

Recommendations:
✅ Context window healthy (<65%)
ℹ️  Estimated remaining: ~50,000 more tokens of conversation
ℹ️  Consider new session at 130K tokens (65%)

Cost Projection (API users only):
- Current session: $0.142
- Estimated total (if at 65%): $0.321
- Model: Sonnet ($3/MTok input, $15/MTok output)
```

## When to Use

- Check context window pressure before long tasks
- Verify token budget before spawning subagents
- Monitor session health during extended work
- Plan session handoff timing
- Track API costs (if using API key)

## Context Window Thresholds

| Usage | Status | Action |
|-------|--------|--------|
| <65% | ✅ Healthy | Continue normally |
| 65-75% | 🔶 Warning | Complete current task, prepare handoff |
| 75-85% | ⚠️ Critical | Finish urgently, start new session |
| >85% | 🚨 Danger | Stop and handoff immediately |

## Integration

This command displays information that Claude Code tracks internally. The data comes from:
- Session transcript metadata
- Token counts from API responses
- Model-specific context limits

For API users, cost calculation uses current model pricing:
- **Sonnet**: $3/MTok input, $15/MTok output
- **Opus**: $5/MTok input, $25/MTok output
- **Haiku**: $1/MTok input, $5/MTok output

## Related Commands

- `/context` - Simple context usage percentage
- `/handoff` - Prepare session handoff
- `/status` - General session status

## Implementation

The actual implementation is built into Claude Code. This command documentation describes what the output looks like and when to use it.

To check token usage programmatically:

```bash
# Via statusline (shows percentage)
~/.claude/statusline.sh

# Via session transcript (detailed breakdown)
ls -lh ~/.claude/transcripts/*.jsonl | tail -1
cat $(ls -t ~/.claude/transcripts/*.jsonl | head -1) | jq '.usage'
```

## Automation

Can be integrated into:
- Stop hooks (check after each response)
- Session start (baseline measurement)
- Pre-commit (ensure enough context for commit workflow)
- Orchestration (track budget across sessions)

## Example Workflow

```
User: "/token-dashboard"

Agent: [Shows dashboard with 45% usage]

User: "Can we spawn 3 subagents for parallel work?"

Agent: "Yes, you have 110K tokens remaining. 3 subagents would use ~60-80K tokens total, leaving safe margin."

User: "Proceed"

Agent: [Spawns subagents]

User: "/token-dashboard"

Agent: [Shows 72% usage after subagents complete]
Agent: "Approaching 75% threshold. Recommend finishing current task and starting fresh session for next major work."
```

## Notes

- Token counts are estimates (model may tokenize differently)
- Output tokens vary by verbosity (concise vs detailed responses)
- Subagent token usage is additive to main session
- Context window includes system prompts, tools, conversation history

---

**Related**: SESSION_HANDOFF.md, SUBAGENTS.md, AUTONOMOUS_DEVELOPMENT.md
