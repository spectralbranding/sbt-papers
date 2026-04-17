# Run 16: Brand Function x Synthetic Cohort Interaction Protocol

**Date**: 2026-04-16
**Paper**: R16 — AI-Native Brand Identity (Zharnikov, 2026x)
**Precedent**: Ghasemi, Astvansh & Sepehri (2026), JAMS Study 5

---

## Methodology Selection: Why Behavioral Vignettes

Behavioral vignettes (not trait labels) define cohort personas. No SBT dimension name or synonym appears in any system prompt. This eliminates semantic priming — the instrument must translate behavior into dimensional weights, not shortcut from keyword to weight. See Run 15 protocol for full rationale.

### Two-Stage Prompt Separation
- System prompt: behavioral vignette (who the observer is)
- User prompt: PRISM-B evaluation task (what they are asked to do)

---

## Pre-Registered Hypotheses

- **H1**: Brand Function reduces DCI more for cohorts whose dominant dimensions align with the specified dimensions (interaction effect, p < .05)
- **H2**: Cohort-specific DCI reduction ranges from near-zero (misaligned) to >20% (aligned)
- **H3**: Detailed per-dimension enrichment (Condition C) produces no incremental benefit beyond structural completeness (Condition B) — replicates Run 14 null across cohorts

---

## Design

- 5 synthetic cohorts: C1 (Green Advocate), C2 (Taste Curator), C3 (Spreadsheet Shopper), C5 (Long Habit), C7 (Experience Collector)
- 5 canonical brands: Hermes, IKEA, Patagonia, Erewhon, Tesla
- 3 conditions: (A) no Brand Function, (B) structural Brand Function, (C) enriched Brand Function
- 3 models: Claude (claude-haiku-4-5), GPT (gpt-4o-mini), DeepSeek (deepseek-chat)
- 3 repetitions per cell
- Total: 5 x 5 x 3 x 3 x 3 = **675 API calls**
- Temperature: .7
- Random seed: 42

---

## Conditions

**A (baseline)**: Standard PRISM-B prompt with cohort vignette, no Brand Function.

**B (structural)**: PRISM-B prompt + Brand Function JSON (8-dimension canonical profile).

**C (enriched)**: Same as B + 3 additional key signals per collapsed dimension.

---

## Analysis Plan

1. 2-way ANOVA: Cohort (5) x Condition (3) on DCI, with Brand as random factor
2. Planned contrasts: aligned vs misaligned cohort-dimension pairs under Condition B
3. Condition B vs C comparison per cohort (replicates Run 14 null across cohorts)
4. Effect sizes: partial eta-squared for interaction

---

## Success Criteria

- H1: significant interaction (p < .05, partial eta-sq > .04)
- H2: DCI reduction range spans at least 15 percentage points across cohorts
- H3: Condition C does not outperform Condition B
