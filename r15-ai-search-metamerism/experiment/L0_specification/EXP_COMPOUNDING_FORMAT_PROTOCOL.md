# Experiment Protocol: Specification Framing in Agentic Pipelines

**Experiment ID**: compounding_format_v1 + compounding_format_v2
**Paper**: R15 "Dimensional Collapse in AI-Mediated Brand Perception" (Zharnikov, 2026v)
**Section**: 5.16 (Specification Paradox)
**Date**: 2026-04-17
**Status**: v1 COMPLETE, v2 DESIGNED

---

## Background

Experiment A (Section 5.13) established that DCI compounds across a 3-step agentic shopping pipeline (eta-sq = .029, d = .442). Run 4 and Run 12 showed that Brand Function specification reduces DCI in single-step contexts (DCI .353 -> .284). The present experiment tests whether specification also reduces compounding in multi-step pipelines.

## Research Questions

1. **RQ1**: Does providing a Brand Function specification at each pipeline step attenuate the compounding effect observed in Exp A?
2. **RQ2**: If information-framing (explicit dimensional scores) does not work, does constraint-framing ("distribute weight equally") attenuate compounding?
3. **RQ3**: Which perceptual dimensions are most affected by each framing condition?

## Hypotheses

### v1 (Information Framing)

- **H_CF1**: DCI(step_3, specified) < DCI(step_3, baseline) — specification reduces final collapse
- **H_CF2**: Compounding rate (control -> step_3) is lower in specified condition
- **H_CF3**: DCI(control, specified) < DCI(control, baseline) — specification reduces collapse even without pipeline

### v2 (Constraint Framing)

- **H_CF4**: DCI(step_3, constraint) < DCI(step_3, baseline) — constraint framing reduces final collapse
- **H_CF5**: DCI(step_3, constraint) < DCI(step_3, information) — constraint framing outperforms information framing
- **H_CF6**: Compounding rate (control -> step_3) is lowest in constraint condition

## Design

### v1: 2 x 4 factorial

| Factor | Levels |
|--------|--------|
| Framing condition | baseline, information (Brand Function scores) |
| Pipeline stage | control, step_1 (free text), step_2 (comparison), step_3 (final weights) |
| Brands | Hermes, Patagonia, Erewhon, Tesla, IKEA |
| Models | claude-haiku-4-5, gpt-4o-mini, gemini-2.5-flash, deepseek-chat, grok-4-1-fast, gemma4-local |
| Repetitions | 2 per cell |

**Total**: 5 x 6 x 2 x 4 x 2 = 480 calls

### v2: 3 x 4 factorial

| Factor | Levels |
|--------|--------|
| Framing condition | baseline, information, constraint |
| Pipeline stage | control, step_1, step_2, step_3 |
| Brands | Hermes, Patagonia, Erewhon, Tesla, IKEA |
| Models | claude-haiku-4-5, gpt-4o-mini, gemini-2.5-flash, deepseek-chat, grok-4-1-fast |
| Repetitions | 2 per cell |

**Total**: 5 x 5 x 3 x 4 x 2 = 600 calls

Gemma 4 excluded from v2 due to 0% parse rate in v1.

### Framing Conditions

**Baseline**: Standard system prompt ("You are a helpful AI shopping assistant.") with no additional framing.

**Information** (v1: "specified"): Brand Function JSON specification prepended to system prompt at every pipeline step. Format:
```
You have access to the following verified brand specification for {brand}.
Use this information when evaluating the brand.

BRAND SPECIFICATION: {brand}
SEMIOTIC (9.5/10): Ultra-premium luxury positioning...
  Signals: Birkin silhouette, orange box, ...
[all 8 dimensions]
```

**Constraint** (v2 only): Equal-weight constraint prepended to system prompt at every pipeline step:
```
When evaluating brands, you must distribute your attention equally 
across all eight perceptual dimensions: Semiotic, Narrative, 
Ideological, Experiential, Social, Economic, Cultural, and Temporal. 
Do not over-weight any single dimension. Each dimension is equally 
important for a complete brand evaluation. Avoid defaulting to price 
or product features — heritage, values, cultural resonance, and 
social meaning are equally valid evaluation criteria.
```

### Pipeline Structure

Three-step single conversation (mirrors Exp A):

1. **Step 1 (Retrieval)**: "Recommend 5 brands in {category}" — free-text response, no weight parsing
2. **Step 2 (Comparison)**: "Compare {focal_brand} vs {competitor} on 8 dimensions, allocate 100 points" — weight-bearing
3. **Step 3 (Recommendation)**: "Make your final recommendation with 8-dimension weight allocation" — weight-bearing

Control: single PRISM-B call (no pipeline context).

Conversation history accumulates: Step 2 sees Step 1's response; Step 3 sees Steps 1 and 2.

### Latin-Square Ordering

Dimension presentation order is rotated across cells using a Latin-square design. The 8 dimensions cycle through 8 starting positions, assigned by `(brand_idx * len(models) + model_idx + rep) % 8`.

### Outcome Measures

**Primary**: Dimensional Collapse Index (DCI) = mean(|w_i - 12.5|) for all 8 dimensions, where w_i is the observed weight for dimension i and 12.5 is the uniform baseline (100/8).

**Secondary**: Per-dimension weight deviations from baseline; cosine similarity between observed and canonical profiles; parse success rate.

### Power Analysis

Based on v1 results:
- Information vs baseline at step_3: d = .599, N = 48 + 45 = 93 → power > .80 for alpha = .05
- Compounding slope (specified): d = .820, N = 50 + 45 = 95 → power > .95
- For v2 3-condition comparison with N ~ 50/cell: detectable effect d >= .50 at power .80

### Statistical Tests

1. **2-way ANOVA** (v2): framing_condition x pipeline_stage on DCI
2. **Planned contrasts**: constraint vs baseline at step_3; constraint vs information at step_3
3. **Effect sizes**: Cohen's d for pairwise comparisons; eta-squared for ANOVA
4. **Per-dimension**: 8 x 3 comparison table with Bonferroni correction

### Stopping Rules

- Run completes when all cells have 2 valid repetitions per brand-model-condition combination
- Parse failures do not trigger re-runs (analyzed as missing data)
- No interim analysis or early stopping

## Data Availability

| Artifact | Location |
|----------|----------|
| v1 script | `experiment/L2_prompts/exp_compounding_format.py` |
| v2 script | `experiment/L2_prompts/exp_compounding_format_v2.py` |
| v1 raw data | `experiment/L3_sessions/exp_compounding_format.jsonl` |
| v2 raw data | `experiment/L3_sessions/exp_compounding_format_v2.jsonl` |
| v1 analysis | `experiment/L4_analysis/exp_compounding_format_summary.md` |
| v2 analysis | `experiment/L4_analysis/exp_compounding_format_v2_summary.md` |
| Protocol | `experiment/L0_specification/EXP_COMPOUNDING_FORMAT_PROTOCOL.md` |
| Brand Functions | `experiment/L1_configuration/brand_functions/*.json` |

All data and scripts publicly available at:
- GitHub: `github.com/spectralbranding/sbt-papers/tree/main/r15-ai-search-metamerism/experiment/`
- HuggingFace: `huggingface.co/datasets/spectralbranding/exp-compounding-format`

## v1 Results Summary

**H_CF1 REVERSED**: DCI(step_3, specified) = 5.394 > DCI(step_3, baseline) = 4.409 (d = .599, p = .004). Specification increases collapse.

**H_CF2 REVERSED**: Compounding rate higher in specified condition (delta +1.295 vs +.274). Interaction = +1.021.

**H_CF3 NULL**: DCI(control, specified) = 4.099 ~ DCI(control, baseline) = 4.135 (negligible difference).

**Interpretation**: The "specification paradox" — Brand Function specification works in single-step contexts but amplifies distortion in multi-step agentic pipelines. The model over-applies Experiential dimension scores (+3.7 at step_3) while suppressing Ideological (-2.7) and Social (-2.0).

**v2 rationale**: If explicit dimensional scores create over-application, a constraint framing that directs equal attention without providing specific targets may avoid the amplification mechanism.
