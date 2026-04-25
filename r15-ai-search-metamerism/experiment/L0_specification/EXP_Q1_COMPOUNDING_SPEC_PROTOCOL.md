# Experiment Protocol: Q1 — Compounding x Structured Specification

**Experiment ID**: compounding_spec_q1
**Paper**: R15 "Dimensional Collapse in AI-Mediated Brand Perception" (Zharnikov, 2026v)
**Section**: 5.17 (Q1: Compounding x Structured Specification)
**Date**: 2026-04-17
**Status**: PRE-REGISTERED (not yet run)

---

## Background

Exp A (Section 5.13) established that DCI compounds across a 3-step agentic shopping pipeline
(eta-sq = .029, d = .442). Exp D (Section 5.16 / compounding_format_v2) replicated the
compounding effect and tested two framing interventions at each pipeline step:

- **Information framing** (Brand Function scores in system prompt): amplified compounding rather
  than reducing it (d = .820 relative to baseline; "specification paradox"). Providing explicit
  dimensional scores gave the model permission to concentrate on Experiential (+5.1 points above
  baseline at step_3) while suppressing Ideological and Social.
- **Constraint framing** ("distribute attention equally across all eight dimensions"): reduced
  final collapse by 42% at step_3 relative to baseline (d = -.983, p < .001) and outperformed
  information framing by 39% (d = -.883, p < .001).

Q1 is a pre-registered replication and extension. It uses an identical 3-condition design to
Exp D to verify that results hold under an independent randomization, extends to a new prompt
phrasing for the constraint condition that explicitly names the procedure ("do not concentrate"),
and adds per-stage DCI trajectory analysis to model the erosion slope of the constraint.

The core question is whether the constraint framing result (d = -.983) replicates in a
fully independent run, and whether the erosion pattern (control DCI .635, step_3 DCI 2.766)
is stable across replications.

---

## Research Questions

1. **RQ1 (Replication)**: Does constraint framing reduce DCI at step_3 relative to baseline
   with effect size d < -.80 in an independent sample?

2. **RQ2 (Mechanism)**: Does the constraint framing produce a steeper compounding slope than
   baseline (i.e., does it start lower but erode faster), or does it produce a uniformly
   lower trajectory across all pipeline stages?

3. **RQ3 (Dimension specificity)**: Which dimensions benefit most from constraint framing
   (i.e., show the largest downward correction from Exp D's over-represented dimensions
   Experiential and Economic)?

---

## Hypotheses

### Pre-registered hypotheses

**H_Q1a** (Replication): DCI(step_3, constraint) < DCI(step_3, baseline) with d < -.80
  — constraint framing reduces final-stage collapse by at least 30%.

**H_Q1b** (Superiority): DCI(step_3, constraint) < DCI(step_3, information) with d < -.50
  — constraint framing outperforms information framing at the final stage.

**H_Q1c** (Control floor): DCI(control, constraint) < DCI(control, baseline)
  — constraint framing also reduces collapse in the single-step PRISM-B control condition,
    consistent with the floor effect observed in Exp D (DCI .635 vs 3.935).

### Exploratory

**H_Q1d** (Erosion): The compounding slope (control -> step_3 DCI delta) under constraint is
  steeper than under baseline, indicating that the constraint wears off under multi-step load
  even if the final endpoint remains lower. This is not a failure condition — it is a
  mechanism finding.

---

## Design

### Factorial structure

| Factor | Levels |
|--------|--------|
| Framing condition | baseline, information, constraint |
| Pipeline stage | control, step_1, step_2, step_3 |
| Brands | Hermes, Patagonia, Erewhon, Tesla, IKEA |
| Models | claude-haiku-4-5, gpt-4o-mini, gemini-2.5-flash, deepseek-chat, grok-4-1-fast-non-reasoning |
| Repetitions | 2 per cell |

**Total calls**: 3 conditions x 4 stages x 5 brands x 5 models x 2 reps = 600
  - Pipeline calls: 3 x 3 x 5 x 5 x 2 = 450 (steps 1-3 per pipeline run)
  - Control calls: 3 x 1 x 5 x 5 x 2 = 150 (single-step PRISM-B)

### Conditions

**Baseline**

System prompt: "You are a helpful AI shopping assistant."

No additional framing. Standard shopping pipeline context. This is the unmodified
observation of dimensional collapse under natural agentic context.

**Information**

System prompt: Brand Function specification prepended at every pipeline step:

```
You have access to the following verified brand specification for {brand}.
Use this information when evaluating the brand.

BRAND SPECIFICATION: {brand}
(Source: Canonical SBT brand profile)

SEMIOTIC ({score}/10): {positioning}
  Signals: {key_signals}
NARRATIVE ({score}/10): {positioning}
  Signals: {key_signals}
[... all 8 dimensions ...]

---

You are a helpful AI shopping assistant.
```

Loaded from `L1_configuration/brand_functions/{brand_slug}.json`.

**Constraint**

System prompt: Structured specification directive prepended at every pipeline step:

```
When evaluating brands, you must distribute your attention equally across all eight
brand perception dimensions: Semiotic, Narrative, Ideological, Experiential, Social,
Economic, Cultural, and Temporal. Do not concentrate your evaluation on price or
functional features alone. Each dimension should receive approximately equal
consideration in your assessment.

---

You are a helpful AI shopping assistant.
```

No brand-specific scores or signals. The constraint is a procedural directive only.

### Pipeline structure

Three-step single multi-turn conversation (mirrors Exp A and Exp D):

**Step 1 (Retrieval)**: "I'm looking for {category} products. List 5 brands you'd
  recommend, with a brief reason for each. Focus on what makes each distinctive."
  — Free-text response. No weight parsing. Conversation history seeds step_2 context.

**Step 2 (Comparison)**: "I'm considering {focal_brand} and {competitor} for {use_case}.
  For each brand, allocate importance weights across eight perception dimensions. Weights
  must sum to 100. Respond in JSON: {"brand_A": {...}, "brand_B": {...}}"
  — Weight-bearing. Competitor extracted from step_1 response.

**Step 3 (Recommendation)**: "Based on your comparison, which brand would you recommend
  for {use_case}? Score your recommended brand on these eight dimensions (weights sum to
  100). Explain your choice briefly. Respond in JSON: {"recommended": "...", "weights":
  {...}, "reason": "..."}"
  — Weight-bearing. Primary outcome measure.

**Control**: Single PRISM-B call (no conversation context):
  "Evaluate the brand {brand} by allocating importance weights across eight dimensions
  of brand perception. The weights must sum to 100. Respond in this exact JSON format:
  {"Semiotic": <number>, ...}"

Conversation history accumulates: step_2 sees step_1 response; step_3 sees steps 1 and 2.
System prompt remains constant across all steps within a conversation.

### Latin-square dimension ordering

Dimension presentation order in JSON templates is rotated across cells using 8 cyclic
rotations. Assignment: `(brand_idx * n_models + model_idx + rep) % 8`. This balances
primacy effects across the full design.

---

## Outcome Measures

**Primary**: Dimensional Collapse Index (DCI) at step_3

  DCI = mean(|w_i - 12.5|) for i in {Semiotic, ..., Temporal}

  where w_i is the observed allocation weight and 12.5 = 100/8 is the uniform baseline.
  DCI = 0 indicates perfect uniform distribution; higher values indicate greater collapse.

**Secondary**:
  - DCI trajectory: per-stage DCI values (control, step_1_NA, step_2, step_3)
  - Per-dimension weight deviations from 12.5 at step_3
  - Compounding delta: DCI(step_3) - DCI(control)
  - Parse success rate per condition and model

---

## Statistical Analysis Plan

### Primary tests (ANOVA + planned contrasts)

1. **One-way ANOVA** on DCI at step_3: factor = framing_condition (3 levels)
   - Report F-statistic, df, p-value, eta-squared
   - Assumption: independence holds (one data point per brand x model x rep cell)

2. **Planned contrast 1** (H_Q1a): constraint vs baseline at step_3
   - Two-sample t-test (Welch)
   - Report: t, df, p, Cohen's d, 95% CI for d

3. **Planned contrast 2** (H_Q1b): constraint vs information at step_3
   - Two-sample t-test (Welch)
   - Report: t, df, p, Cohen's d, 95% CI for d

4. **Planned contrast 3** (H_Q1c): constraint vs baseline in control condition
   - Two-sample t-test (Welch)
   - Report: t, df, p, Cohen's d

### Secondary analyses

5. **Compounding slope** (H_Q1d): DCI(step_3) - DCI(control) by condition
   - One-way ANOVA on delta values
   - Post-hoc pairwise with Bonferroni correction

6. **Per-dimension table**: 8 x 3 mean weights (dimension x condition) at step_3
   - Flag dimensions where constraint weight is within ±1.0 of 12.5 (near-uniform)
   - Flag dimensions where information weight deviates >2.0 from baseline (paradox signal)

7. **Model-level breakdown**: DCI by model x condition at step_3
   - Identify any model that reverses the constraint benefit

### Replication criterion

H_Q1a is considered replicated if: d(constraint vs baseline at step_3) < -.80 AND p < .01.
This is a pre-specified threshold chosen to detect a minimum meaningful reduction (30%) given
the Exp D effect size of -.983. A result in the range -.50 to -.80 would be considered
partial replication.

---

## Stopping Rules

- Run completes when all cells have 2 valid repetitions per brand x model x condition.
- Parse failures are recorded as missing data; cells with 0 valid responses are reported
  but do not trigger reruns.
- No interim analysis or early stopping.
- If overall parse rate falls below 50% for any single model across all conditions, that
  model is excluded from primary analysis and reported as a secondary finding.

---

## Cost Estimate

| Model | ~calls | Input $/M | Output $/M | Est. cost |
|-------|--------|-----------|------------|-----------|
| claude-haiku-4-5 | 120 | 0.80 | 4.00 | ~$0.06 |
| gpt-4o-mini | 120 | 0.15 | 0.60 | ~$0.02 |
| gemini-2.5-flash | 120 | 0.15 | 0.60 | ~$0.03 |
| deepseek-chat | 120 | 0.27 | 1.10 | ~$0.04 |
| grok-4-1-fast-non-reasoning | 120 | 3.00 | 15.00 | ~$0.45 |
| **Total** | **600** | | | **~$0.60** |

Estimate assumes ~200 input tokens and ~150 output tokens per call on average, with step_1
calls using ~350 output tokens. Grok dominates cost due to output pricing.

---

## Models

Cloud-only (no local models):

| Short name | Model ID | Provider |
|------------|----------|----------|
| claude | claude-haiku-4-5 | Anthropic |
| gpt | gpt-4o-mini | OpenAI |
| gemini | gemini-2.5-flash | Google |
| deepseek | deepseek-chat | DeepSeek |
| grok | grok-4-1-fast-non-reasoning | xAI |

Gemma 4 excluded: 0% valid parse rate in compounding_format_v1.
Ollama/local models excluded to keep cost and runtime predictable for a replication run.

---

## Data Availability

| Artifact | Location |
|----------|----------|
| Protocol | `experiment/L0_specification/EXP_Q1_COMPOUNDING_SPEC_PROTOCOL.md` |
| Script | `experiment/L2_prompts/exp_q1_compounding_spec.py` |
| Raw data | `experiment/L3_sessions/exp_q1_compounding_spec.jsonl` |
| Analysis | `experiment/L4_analysis/exp_q1_compounding_spec_analysis.py` |
| Brand Functions | `experiment/L1_configuration/brand_functions/*.json` |
| Prior: Exp D script | `experiment/L2_prompts/exp_compounding_format_v2.py` |
| Prior: Exp D data | `experiment/L3_sessions/exp_compounding_format_v2.jsonl` |

Public:
- GitHub: `github.com/spectralbranding/sbt-papers/tree/main/r15-ai-search-metamerism/experiment/`
- HuggingFace: `huggingface.co/datasets/spectralbranding/exp-compounding-format`

---

## Relationship to Prior Experiments

| Experiment | Design | Key finding |
|------------|--------|-------------|
| Exp A (agentic_collapse) | 3-step pipeline, no framing | Compounding confirmed (eta-sq=.029, d=.442) |
| Exp D v1 (compounding_format) | baseline + information | Information amplifies compounding (d=.820) |
| Exp D v2 (compounding_format_v2) | baseline + information + constraint | Constraint reduces collapse 42% (d=-.983) |
| **Q1 (this protocol)** | **baseline + information + constraint (replication)** | **TBD** |

Q1 uses the same 3-condition design as Exp D v2 with identical prompts, models (minus gemma4),
and brand set. The randomization seed is fixed at 42 for the work queue shuffle, but the
random call ordering is independently re-seeded so results are not identical to Exp D v2.
