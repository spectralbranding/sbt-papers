---
name: research
description: Web research, documentation lookup, and information synthesis for the fleet.
---

# Research Skill

**Version**: 2.0.0
**Created**: 2026-02-05
**Purpose**: Structured web research, information synthesis, and citation management for AI-assisted investigations

---

## Overview

The research skill provides systematic approaches to information gathering, evaluation, and synthesis. It leverages WebSearch, WebFetch, and MCP tools to conduct thorough investigations and produce well-sourced findings.

**Primary Tools**:
- WebSearch: Current web search (2026-aware)
- WebFetch: Content extraction from URLs
- MCP search_docs: Codebase semantic search
- MCP search_decisions: Decision precedent lookup

---

## When to Use This Skill

Invoke this skill when you need to:
- Investigate unfamiliar technologies or APIs
- Compare multiple solutions or tools
- Validate technical assumptions
- Find current best practices (2026 context)
- Gather evidence for architecture decisions
- Synthesize information from multiple sources

---

## Research Types

### 1. Quick Lookup (5-10 minutes)
**Goal**: Fast fact-finding and validation.

**Use cases**:
- API syntax verification
- Version compatibility check
- Quick feature comparison
- Definition lookup

**Process**:
1. Single WebSearch or WebFetch call
2. Extract key fact
3. Cite source in response
4. No permanent documentation

### 2. Deep Dive (30-60 minutes)
**Goal**: Comprehensive understanding of a topic.

**Use cases**:
- Technology evaluation
- Architecture research
- Integration pattern discovery
- Best practices investigation

**Process**:
1. Multiple search queries (5-10 sources)
2. Cross-reference findings
3. Synthesize key insights
4. Document in knowledge vault
5. Create decision trace if needed

### 3. Competitive Analysis (60-120 minutes)
**Goal**: Compare options for decision-making.

**Use cases**:
- Tool selection (database, framework, library)
- Vendor evaluation
- Implementation approach comparison

**Process**:
1. Define comparison criteria
2. Research each option (multiple sources)
3. Create decision matrix
4. Document recommendation
5. Create decision trace

### 4. Continuous Monitoring
**Goal**: Track evolving topics over time.

**Use cases**:
- Framework updates
- Security advisories
- Industry trends

**Process**:
1. Periodic searches (weekly/monthly)
2. Update existing research notes
3. Flag significant changes
4. Update affected projects

---

## Workflows

### Workflow 1: Technology Evaluation

**Scenario**: Need to choose a vector database for RAG system.

**Steps**:

1. **Define requirements**
```markdown
Requirements:
- Self-hosted (local deployment)
- Python support
- Good performance for <1M vectors
- Active maintenance (2026)
```

2. **Identify candidates**
```markdown
Candidates:
- LanceDB
- Chroma
- Weaviate
- Milvus
- Qdrant
```

3. **Research each candidate**
```bash
# For each: WebSearch for recent reviews, documentation, GitHub activity
WebSearch query="LanceDB vs Chroma vs Weaviate 2026 comparison"
WebSearch query="LanceDB Python performance benchmarks 2026"
WebFetch url="https://lancedb.github.io/lancedb/" prompt="Explain deployment options and Python API"
```

4. **Create comparison matrix**
```markdown
| Feature | LanceDB | Chroma | Weaviate |
|---------|---------|--------|----------|
| Deployment | Embedded | Server/Embedded | Server |
| Python API | ✅ Native | ✅ Native | ✅ Client |
| Performance | High | Medium | High |
| Maintenance | Active | Active | Active |
| Local-first | ✅ | ✅ | ❌ (server) |
```

5. **Document recommendation**
```markdown
# Vector Database Selection

**Decision**: LanceDB
**Date**: 2026-02-05
**Context**: RAG system for life-tracker

## Reasoning
1. Embedded deployment (no server)
2. Excellent Python API
3. Active development (2026)
4. Local-first matches fleet architecture

## Sources
- [LanceDB Docs](URL)
- [Benchmark Study](URL)
- [GitHub Activity](URL)

## Alternatives Considered
- Chroma: Good but prefer LanceDB's embedded approach
- Weaviate: Requires server deployment
```

6. **Create decision trace**
```bash
# Save to knowledge vault
cp research-note.md ~/projects/knowledge-vault/decisions/002-lancedb-selection.md
```

### Workflow 2: API Integration Research

**Scenario**: Need to integrate with Airtable API.

**Steps**:

1. **Find official documentation**
```bash
WebSearch query="Airtable Python API documentation 2026"
WebFetch url="https://airtable.com/developers/web/api/introduction" prompt="Explain authentication and rate limits"
```

2. **Search for code examples**
```bash
WebSearch query="Airtable Python pyairtable examples 2026"
WebSearch query="Airtable API best practices error handling"
```

3. **Check for fleet precedents**
```bash
# Use MCP tool
search_docs query="airtable integration pattern"
search_decisions query="airtable API"
```

4. **Document pattern**
```markdown
# Airtable API Pattern

## Authentication
Use personal access token (PAT), store in .env

## Rate Limits
5 requests/second per base

## Error Handling
- Retry with exponential backoff on 429
- Handle 422 for validation errors

## Code Example
[Working code snippet]

## Sources
- [Airtable API Docs](URL)
- [pyairtable GitHub](URL)
- [Fleet precedent: project-x integration]
```

### Workflow 3: Current Best Practices

**Scenario**: What's the current recommended approach for Python async in 2026?

**Steps**:

1. **Search for recent content**
```bash
WebSearch query="Python asyncio best practices 2026"
WebSearch query="Python 3.12 async patterns 2026"
```

2. **Verify with official sources**
```bash
WebFetch url="https://docs.python.org/3.12/library/asyncio.html" prompt="What are the recommended patterns for asyncio in Python 3.12?"
```

3. **Check for fleet context**
```bash
search_docs query="python async macos"
# Found: PYTHON_ASYNC_MACOS.md with selector policy fix
```

4. **Synthesize findings**
```markdown
# Python Async Best Practices (2026)

## Current Recommendations
1. Use `asyncio.run()` for entry points
2. On macOS: Set `DefaultEventLoopPolicy` for subprocess support
3. Prefer `asyncio.TaskGroup` (Python 3.11+) for concurrent tasks
4. Use `asyncio.timeout()` for timeouts

## Fleet-Specific
- See `PYTHON_ASYNC_MACOS.md` for macOS subprocess fix
- Already implemented in project-x

## Sources
- [Python 3.12 Docs](URL)
- [What's New in Python 3.12](URL)
- Fleet precedent: PYTHON_ASYNC_MACOS.md
```

### Workflow 4: Troubleshooting Research

**Scenario**: Getting obscure error message, need to find solution.

**Steps**:

1. **Search for exact error**
```bash
WebSearch query="exact error message text python 2026"
```

2. **Search for related issues**
```bash
WebSearch query="library-name error-keyword workaround"
WebSearch query="library-name GitHub issues error-keyword"
```

3. **Check fleet history**
```bash
search_decisions query="error-keyword"
# Check if we've encountered this before
```

4. **Document solution**
```markdown
# Error: [Error Message]

## Context
When doing X with library Y

## Root Cause
[Explanation]

## Solution
[Code fix or workaround]

## Prevention
[How to avoid in future]

## Sources
- [GitHub Issue](URL)
- [Stack Overflow](URL)
```

---

## Research Patterns

### Pattern: Multi-Source Validation

**Goal**: Verify information from multiple independent sources.

**Process**:
1. Find 3+ sources for key claims
2. Check source credibility (official docs > blog posts)
3. Note publication dates (prefer 2025-2026)
4. Flag contradictions for further investigation

**Example**:
```markdown
## Finding: LanceDB supports filtering
Source 1: Official docs (2026-01) ✅
Source 2: Tutorial (2025-12) ✅
Source 3: Reddit discussion (2024-06) ⚠️ Old
Confidence: High (2/3 recent sources agree)
```

### Pattern: Official Docs First

**Goal**: Prioritize authoritative sources.

**Hierarchy**:
1. Official documentation (latest version)
2. Official GitHub repository
3. Reputable tutorials (dated 2025+)
4. Community discussions (for edge cases)

**Example**:
```markdown
Research order for FastAPI:
1. https://fastapi.tiangolo.com (official)
2. https://github.com/tiangolo/fastapi (source)
3. Real Python tutorials (if needed)
4. Stack Overflow (for specific issues)
```

### Pattern: Version-Aware Search

**Goal**: Find information relevant to current versions.

**Search modifiers**:
- Include year: "FastAPI async patterns 2026"
- Include version: "Python 3.12 async best practices"
- Exclude old: "FastAPI 2026 -2023 -2022"

**Example**:
```bash
# Good (version-aware)
WebSearch query="Next.js app router patterns 2026"

# Bad (may return outdated info)
WebSearch query="Next.js routing"
```

### Pattern: Negative Space Research

**Goal**: Understand what a tool/library CANNOT do.

**Questions**:
- What are the limitations?
- What use cases are NOT supported?
- What are known issues or gotchas?

**Search queries**:
```bash
WebSearch query="LanceDB limitations known issues"
WebSearch query="Airtable API rate limits constraints"
WebSearch query="FastAPI when not to use"
```

---

## Quality Criteria

### Source Credibility

**Tier 1 (Highly Credible)**:
- Official documentation
- Official GitHub repositories
- Peer-reviewed papers
- Reputable technical publishers

**Tier 2 (Generally Credible)**:
- Well-known technical blogs (Real Python, LogRocket)
- Maintainer blog posts
- Conference talks (PyCon, etc.)
- Technical books from known publishers

**Tier 3 (Use with Caution)**:
- Medium posts (check author credentials)
- Personal blogs (verify claims)
- Reddit/forums (good for gotchas, not facts)
- Stack Overflow (good for specific solutions)

### Recency Requirements

**Critical (must be 2025+)**:
- Framework best practices
- API syntax
- Deployment patterns
- Security recommendations

**Important (prefer 2024+)**:
- Architecture patterns
- Tool comparisons
- Performance benchmarks

**Flexible (age acceptable)**:
- Fundamental concepts
- Design patterns
- Algorithm explanations

### Completeness Check

**Before concluding research**:
- [ ] Answered the original question?
- [ ] Found concrete examples (not just theory)?
- [ ] Identified limitations/gotchas?
- [ ] Validated from multiple sources?
- [ ] Noted any conflicting information?
- [ ] Captured source URLs?

---

## Output Formats

### Format 1: Research Brief (Quick Answer)

```markdown
# [Question]

**Answer**: [Direct answer in 1-2 sentences]

**Details**:
- Point 1 with evidence
- Point 2 with evidence

**Sources**:
- [Title](URL)
- [Title](URL)

**Confidence**: High | Medium | Low
**Date**: 2026-02-05
```

### Format 2: Decision Matrix (Comparison)

```markdown
# [Tool/Library] Comparison

**Context**: [Why we're evaluating]
**Date**: 2026-02-05

## Candidates
1. Option A
2. Option B
3. Option C

## Comparison

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Feature 1 | ✅ | ❌ | ✅ |
| Feature 2 | Good | Better | Best |
| Criterion 3 | $0 | $10/mo | $50/mo |

## Recommendation
[Option X] because [reasoning]

## Sources
- [Source 1](URL)
- [Source 2](URL)
```

### Format 3: Annotated Bibliography

```markdown
# [Topic] Resources

**Date**: 2026-02-05

## Official Documentation
- [Title](URL) - What it covers, key sections

## Tutorials
- [Title](URL) - Summary, what you'll learn

## Code Examples
- [Title](URL) - What it demonstrates

## Discussions
- [Title](URL) - Key insights, gotchas mentioned

## Notes
Overall synthesis, key takeaways
```

---

## Examples

### Example 1: Framework Selection

**Question**: Should we use Streamlit or Gradio for internal tools?

**Research**:
```bash
WebSearch query="Streamlit vs Gradio 2026 comparison"
WebSearch query="Streamlit enterprise features 2026"
WebSearch query="Gradio customization capabilities 2026"
```

**Output**:
```markdown
# Streamlit vs Gradio (2026)

**Recommendation**: Streamlit

## Comparison
| Feature | Streamlit | Gradio |
|---------|-----------|--------|
| Use case | Dashboards | ML demos |
| Customization | High | Medium |
| Deployment | Standard | Simpler |
| Fleet fit | ✅ Better | ⚠️ Limited |

## Reasoning
- Better for complex dashboards (our use case)
- More customization options
- Already used in fleet (precedent)

## Sources
- [Streamlit Docs](URL)
- [Gradio Docs](URL)
- [Comparison Article 2026](URL)
```

### Example 2: API Investigation

**Question**: How to handle Airtable rate limits properly?

**Research**:
```bash
WebFetch url="https://airtable.com/developers/web/api/rate-limits" prompt="Explain rate limit strategy"
WebSearch query="Airtable rate limit best practices Python 2026"
search_docs query="airtable rate limit"
```

**Output**:
```markdown
# Airtable Rate Limit Strategy

## Limits
- 5 requests/second per base
- Burst allowance of 15 requests

## Implementation
1. Use token bucket algorithm
2. Exponential backoff on 429
3. Queue requests during bursts

## Code Pattern
[Code snippet with retry logic]

## Sources
- [Airtable Docs](URL)
- [pyairtable example](URL)
```

### Example 3: Best Practices Update

**Question**: What changed in React 18/19 that we should know?

**Research**:
```bash
WebSearch query="React 19 new features changes 2026"
WebFetch url="https://react.dev/blog" prompt="Summarize React 19 breaking changes and new features"
```

**Output**:
```markdown
# React 19 Updates (2026)

## Key Changes
1. Automatic batching (affects setState patterns)
2. Transitions (new concurrent feature)
3. Server Components (stable in Next.js 14+)

## Fleet Impact
- ✅ No breaking changes to existing code
- ⚠️ Consider transitions for heavy updates
- 📝 Server Components for new Next.js projects

## Migration
Not urgent, but beneficial for performance

## Sources
- [React Blog](URL)
- [React 19 Release Notes](URL)
```

---

## Related Skills

- **knowledge-vault**: Documenting research findings
- **python-dev**: Technical implementation research
- **fleet-ops**: Infrastructure and deployment research

---

## Related Documentation

- `knowledge-base/MCP.md` - MCP tool configuration and usage
- `knowledge-base/DECISION_TRACES.md` - Recording research-informed decisions
- `knowledge-base/DOCUMENTATION_STANDARDS.md` - Citation and writing standards
- `skills/knowledge-vault/SKILL.md` - Note-taking and knowledge management

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-02-05 | Comprehensive workflows, patterns, quality criteria, examples |
| 1.0.0 | 2026-02-03 | Initial research workflow outline |
