---
name: knowledge-vault
description: Navigation and maintenance of the Obsidian Knowledge Vault (brain of the fleet).
---

# Knowledge Vault Skill

**Version**: 2.0.0
**Created**: 2026-02-05
**Purpose**: Research, note-taking, and knowledge management workflows for the fleet's Obsidian vault

---

## Overview

The knowledge vault is the fleet's persistent memory system, implemented in Obsidian. It stores research, bookmarks, daily logs, and decision traces in an interconnected markdown ecosystem.

**Location**: `~/projects/knowledge-vault/`
**Sync**: Git-tracked across all fleet machines
**Access**: Obsidian app (all machines), CLI/editors (fallback)

---

## When to Use This Skill

Invoke this skill when you need to:
- Capture research findings for long-term reference
- Organize bookmarks and web resources by topic
- Create structured notes for deep dive investigations
- Log daily activities and decisions
- Connect concepts across projects
- Build a personal knowledge graph

---

## Vault Structure

```
knowledge-vault/
├── bookmarks/               # Web links organized by topic
│   ├── inbox.md            # Unsorted bookmarks
│   ├── index.md            # Topic index
│   └── [category]/         # e.g., ai/, dev/, infra/
│       └── links.md
│
├── research/                # Deep dive notes
│   ├── life-tracker/       # Project-specific research
│   ├── obsidian/           # Obsidian workflow research
│   └── [topic]/
│
├── daily/                   # Daily notes (YYYY-MM-DD.md)
│   └── 2026-02-05.md
│
├── projects/                # Project hub notes
│   ├── life-tracker.md
│   ├── fleet-standards.md
│   └── [project].md
│
├── decisions/               # Architecture Decision Records (ADRs)
│   └── [decision-id].md
│
├── integrations/            # Shared definitions
│   ├── categories.yaml     # Taxonomies
│   ├── tags.yaml           # Tag definitions
│   └── vendors.yaml        # Known patterns
│
├── templates/               # Note templates
│   ├── daily-note.md
│   ├── research-note.md
│   └── project-note.md
│
└── attachments/             # Images, PDFs, etc.
```

---

## Workflows

### 1. Research Workflow

**Goal**: Capture findings from web research or technical investigations.

**Steps**:

1. **Check for existing notes**
```bash
# Search vault for existing content
grep -r "topic keyword" ~/projects/knowledge-vault/research/
```

2. **Create research note** (if new topic)
```bash
# Use research template
cp ~/projects/knowledge-vault/templates/research-note.md \
   ~/projects/knowledge-vault/research/[topic]/[subtopic].md
```

3. **Capture findings**
```markdown
# Topic Name

**Created**: YYYY-MM-DD
**Status**: In Progress | Complete
**Related**: [[other-note]], [[project]]

## Summary
Brief overview (2-3 sentences)

## Key Findings
- Finding 1 with source
- Finding 2 with source

## Sources
- [Source Title](URL) - Context
- [Source Title](URL) - Context

## Notes
Detailed observations, quotes, analysis

## Related Research
- [[related-note-1]]
- [[related-note-2]]
```

4. **Link to bookmarks**
```markdown
## Bookmarks
See [[bookmarks/ai/links]] for related resources
```

5. **Connect to daily log**
```markdown
# Daily note (2026-02-05.md)

## Research
- Investigated [[research/topic/subtopic]] - key insight: X
```

### 2. Bookmark Management

**Goal**: Organize web resources for easy retrieval.

**Steps**:

1. **Quick capture** (inbox pattern)
```markdown
# bookmarks/inbox.md

- [ ] [Article Title](URL) #ai #research - Added 2026-02-05
- [ ] [Tool Name](URL) #dev #python - Added 2026-02-05
```

2. **Weekly triage** (organize bookmarks)
```bash
# Move from inbox to categorized files
# Review inbox.md, move to topic-specific files
```

3. **Categorized storage**
```markdown
# bookmarks/ai/llm-tools.md

## Inference Servers
- [Ollama](https://ollama.ai) - Local LLM runner
- [vLLM](https://vllm.ai) - High-performance serving

## Prompting
- [Claude Prompting Guide](URL) - Official guide
```

4. **Index maintenance**
```markdown
# bookmarks/index.md

## Categories
- [[bookmarks/ai/links]] - AI/ML resources (52 links)
- [[bookmarks/dev/links]] - Development tools (38 links)
- [[bookmarks/infra/links]] - Infrastructure (27 links)
```

### 3. Daily Logging

**Goal**: Track daily activities, decisions, and insights.

**Steps**:

1. **Create daily note** (or use Periodic Notes plugin)
```bash
# Manual creation
date=$(date +%Y-%m-%d)
cp ~/projects/knowledge-vault/templates/daily-note.md \
   ~/projects/knowledge-vault/daily/$date.md
```

2. **Daily note structure**
```markdown
# 2026-02-05

## Summary
Brief overview of the day

## Work Log
- Completed [[projects/fleet-standards]] documentation update
- Investigated [[research/obsidian/plugin-architecture]]
- Fixed bug in [[projects/life-tracker]]

## Decisions
- Decided to use Dataview plugin for queries
  - Reason: Better performance than manual aggregation
  - See [[decisions/001-dataview-adoption]]

## Research
- [[research/ai/prompt-engineering]] - discovered X pattern

## Bookmarks
- [Title](URL) #tag - context

## Notes
Random observations, ideas, todos
```

3. **Link to project notes**
```markdown
## Projects
- [[projects/life-tracker]] - Implemented document processing pipeline
```

### 4. Knowledge Synthesis

**Goal**: Connect concepts across multiple notes to build understanding.

**Steps**:

1. **Use WikiLinks liberally**
```markdown
The [[Zettelkasten]] method encourages [[atomic-notes]] that link via [[associative-thinking]].
```

2. **Create index/hub notes**
```markdown
# projects/obsidian-ecosystem.md

## Overview
Obsidian integration across fleet projects

## Related Notes
- [[research/obsidian/plugin-architecture]]
- [[research/obsidian/dataview-queries]]
- [[daily/2026-02-05]] - Initial setup

## Resources
- [[bookmarks/obsidian/links]]
```

3. **Use Obsidian Graph View**
- Open Obsidian
- View → Open graph view
- Identify clusters and gaps

4. **Create connection notes**
```markdown
# How X relates to Y

[[concept-x]] and [[concept-y]] intersect at [[shared-principle]].

Example: [[research/ai/rag]] uses [[research/db/vector-search]].
```

---

## Templates

### Research Note Template

```markdown
# [Topic Name]

**Created**: YYYY-MM-DD
**Status**: In Progress | Complete | Archived
**Related**: [[other-note]]

---

## Question
What are we trying to learn?

## Summary
Brief overview (2-3 sentences)

## Key Findings
1. Finding with supporting evidence
2. Finding with supporting evidence

## Sources
- [Title](URL) - Context and credibility
- [Title](URL) - Context and credibility

## Detailed Notes
Deep dive content, quotes, analysis

## Related Research
- [[related-note-1]]
- [[related-note-2]]

## Follow-up Questions
- Question 1
- Question 2
```

### Daily Note Template

```markdown
# YYYY-MM-DD

## Summary
What happened today (1-2 sentences)

## Work Log
- Task 1
- Task 2

## Decisions
Major choices made

## Research
Links to research notes created/updated

## Bookmarks
New resources found

## Notes
Observations, ideas, todos
```

### Project Hub Template

```markdown
# [Project Name]

**Status**: Active | On Hold | Complete
**Repository**: [URL]
**Documentation**: [URL]

---

## Overview
What is this project?

## Recent Activity
- [[daily/YYYY-MM-DD]] - What happened
- [[daily/YYYY-MM-DD]] - What happened

## Research
- [[research/topic/subtopic]]

## Decisions
- [[decisions/001-decision]]

## Resources
- [[bookmarks/category/links]]

## Notes
Project-specific observations
```

---

## Best Practices

### Atomic Notes Principle
- One concept per note
- Self-contained and understandable
- Linkable from multiple contexts

### Linking Strategy
- Use `[[WikiLinks]]` for internal connections
- Use descriptive link text: `[[note|displayed text]]`
- Link bidirectionally when concepts relate

### Tag Taxonomy
- Use hierarchical tags: `#project/life-tracker`
- Keep tag count manageable (<50 top-level)
- Define tags in `integrations/tags.yaml`

### Folder Structure
- Organize by type (research, bookmarks, daily)
- Keep nesting shallow (2-3 levels max)
- Use hub notes for navigation

### Sync Protocol
```bash
# Before starting work
cd ~/projects/knowledge-vault
git pull

# After capturing notes
git add .
git commit -m "research: Add [topic] findings"
git push
```

---

## Obsidian Plugins

### Required
- **Dataview**: Query notes dynamically
- **Templater**: Advanced templates with variables
- **Periodic Notes**: Auto-create daily notes

### Recommended
- **Excalidraw**: Whiteboard diagrams
- **Tag Wrangler**: Manage tag hierarchies
- **QuickAdd**: Fast capture macros
- **Calendar**: Navigate daily notes by date

---

## Examples

### Example 1: Technology Evaluation Research

**Context**: Evaluating vector databases for RAG system.

**Workflow**:
1. Create `research/db/vector-databases.md`
2. Research Pinecone, Weaviate, LanceDB
3. Capture findings in research note
4. Bookmark documentation in `bookmarks/db/links.md`
5. Log decision in `daily/2026-02-05.md`
6. Create `decisions/002-lancedb-selection.md`
7. Link all notes: research → decision → daily

### Example 2: API Integration Pattern

**Context**: Documenting Airtable API patterns for reuse.

**Workflow**:
1. Create `research/airtable/api-patterns.md`
2. Capture code snippets and gotchas
3. Link from `projects/life-tracker.md`
4. Log in daily note with key insight
5. Tag with `#pattern #api #airtable`

### Example 3: Weekly Link Roundup

**Context**: 15 links saved to inbox, need organization.

**Workflow**:
1. Open `bookmarks/inbox.md`
2. For each link:
   - Categorize by topic (ai, dev, infra)
   - Move to `bookmarks/[category]/links.md`
   - Add context note
3. Clear inbox
4. Update `bookmarks/index.md` counts

---

## Related Skills

- **research**: Web research and synthesis patterns
- **python-dev**: Code documentation workflows
- **fleet-ops**: Vault sync across fleet machines

---

## Related Documentation

- `knowledge-base/OBSIDIAN_PROJECT.md` - Per-project Obsidian integration
- `designs/OBSIDIAN_ARCHITECTURE.md` - "Mycelium" vault architecture
- `knowledge-base/DECISION_TRACES.md` - Decision capture patterns
- `knowledge-base/DOCUMENTATION_STANDARDS.md` - Writing guidelines

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-02-05 | Comprehensive workflows, templates, examples |
| 1.0.0 | 2026-02-03 | Initial structure guidelines |
