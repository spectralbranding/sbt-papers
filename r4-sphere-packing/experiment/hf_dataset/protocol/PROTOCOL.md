# Experiment C: Competitive Interference in Perception Space

**Protocol Version**: 1.0
**Date**: 2026-04-16
**Status**: PRE-REGISTERED (committed before data collection)
**Paper Target**: R4 (Sphere Packing Capacity) extension or new paper
**Open Problem**: Extends R4 sphere packing capacity

---

## Research Question

Does the presence of a competitor alter a brand's spectral profile in LLM-mediated perception? If so, does the magnitude and direction of shift depend on competitor proximity in perception space?

## Background

R4 formalizes brand positioning as sphere packing in 8-dimensional perception space. The theory predicts that brands maintain minimum separation distances. This experiment tests whether the *measurement* of a brand's spectral profile is influenced by competitive context -- a form of context-dependent perception that has implications for both AI-mediated brand evaluation and the sphere packing capacity bounds.

## Design

### Factors
- **Focal brand** (5 levels): Hermes, IKEA, Patagonia, Erewhon, Tesla
- **Competitor** (3 levels per brand): Direct, Adjacent, Distant
- **Condition** (3 levels): Solo, Paired, Context
- **Model** (5 levels): Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Grok 4.1 Fast

### Competitor Pairings

| Focal Brand | Direct Competitor | Adjacent Competitor | Distant Competitor |
|-------------|-------------------|--------------------|--------------------|
| Hermes | Louis Vuitton | Rolex | Walmart |
| IKEA | H&M Home | Muji | Ferrari |
| Patagonia | Arc'teryx | REI | Shein |
| Erewhon | Whole Foods | Blue Bottle | McDonald's |
| Tesla | Rivian | Apple | Toyota |

### Conditions

1. **Solo**: Evaluate focal brand alone (standard PRISM-B)
2. **Paired**: "Evaluate {focal_brand} compared to {competitor}"
3. **Context**: "Evaluate {focal_brand} in a market that also includes {competitor}"

### Sample Size

- Solo baselines: 5 brands x 5 models x 3 reps = 75 calls
- Self-comparison control: 5 brands x 5 models x 1 rep = 25 calls
- Competitive conditions: 5 brands x 3 competitors x 2 conditions (paired + context) x 5 models x 1 rep = 150 calls
- **Total: 250 calls**
- Estimated cost: ~$1

### Self-Comparison Control

For each focal brand, one "paired" condition uses the focal brand as its own competitor ("Compare Hermes vs Hermes on 8 dimensions"). If the self-comparison profile differs from the solo evaluation, the paired prompt format itself introduces bias. All competitor effects are therefore measured as the delta ABOVE this self-comparison baseline, not above the solo baseline alone.

### Power Analysis

Using effect size priors from synthetic cohort experiments:
- Medium cohort effect: eta-sq = .25
- For ANOVA with 3 groups (competitor types) and alpha = .05 / 8 (Bonferroni for 8 dimensions):
  - At eta-sq = .25: n = 15 per cell provides power > .80
  - Each cell has 5 models x 1 rep = 5 observations (underpowered for individual cells)
  - Aggregate across models: 5 brands x 5 models = 25 per competitor type (adequate)
- For paired t-tests (solo vs paired): each brand has 15 solo measurements (3 reps x 5 models) vs 5 paired measurements per competitor type. Cohen's d > 0.8 detectable.

## Hypotheses (Pre-Registered)

### H1: Competitive Context Effect
Spectral profiles shift when a competitor is present vs solo evaluation.
- **Test**: Paired t-test on per-dimension weights (solo vs paired condition, aggregated across competitors)
- **Alpha**: .05 / 8 = .00625 (Bonferroni for 8 dimensions)
- **Success criterion**: At least 2 of 8 dimensions show significant shift at corrected alpha
- **Effect size**: Report Cohen's d with 95% bootstrap CI

### H2: Distance-Dependent Shift
Direct competitors produce larger profile shifts than distant competitors (contrast effect gradient).
- **Test**: One-way ANOVA on Euclidean profile shift magnitude (3 competitor types)
- **Alpha**: .05
- **Success criterion**: F-test significant, with planned contrast: direct > adjacent > distant
- **Effect size**: Report eta-squared with 95% bootstrap CI

### H3: Dimension-Specific Contrast/Assimilation
Brands differentiate *away* from competitors on shared strong dimensions (contrast) and *toward* competitors on distinctive weak dimensions (assimilation).
- **Test**: For each focal-competitor pair, compute per-dimension shift direction. Classify dimensions as "shared strong" (both brands high) vs "distinctive weak" (focal low, competitor high). Test whether shift direction differs by dimension type.
- **Alpha**: .05
- **Success criterion**: Significant interaction between dimension type and shift direction
- **Effect size**: Report Cohen's d for contrast vs assimilation effect sizes

## Analysis Plan

### Primary Analyses
1. Per-dimension paired t-tests: solo vs paired (H1)
2. One-way ANOVA: competitor type on profile shift magnitude (H2)
3. Contrast vs assimilation classification per dimension per pair (H3)

### Secondary Analyses
4. Model x Condition interaction: do models differ in susceptibility to competitive context?
5. Paired vs Context condition comparison: does explicit comparison vs ambient context differ?
6. Regression: spectral distance between focal and competitor predicts shift magnitude

### Exploratory
7. Which specific competitor pairings produce the largest shifts?
8. Is there a "repulsion" pattern in perception space (brands move away from competitors)?
9. Cross-model consistency in shift direction (cosine similarity of shift vectors)

## Exclusion Criteria
- API errors resulting in unparseable responses: recorded with error field in JSONL
- Weights that do not sum to 100 (+/-5 tolerance): renormalized and included
- Weights outside 95-105 tolerance: excluded and recorded
- Models with >50% error rate: excluded from aggregate statistics

## Statistical Software
- Python 3.12, scipy.stats for t-tests and ANOVA
- numpy for vector operations and cosine similarity
- Bootstrap CIs: 10,000 iterations, fixed seed

## Reproducibility
- Random seed: 42 (for Latin-square ordering and bootstrap)
- All scripts committed before execution
- Raw JSONL immutable after collection
- Full prompts stored in JSONL records
- API response metadata recorded per call

## Dimension Order
Latin-square balanced (8 cyclic orderings). Seed: 42.

## Latin-Square Orderings (8 cyclic rotations)

| Ordering | Dimension sequence |
|----------|-------------------|
| 0 | Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal |
| 1 | Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal, Semiotic |
| 2 | Ideological, Experiential, Social, Economic, Cultural, Temporal, Semiotic, Narrative |
| 3 | Experiential, Social, Economic, Cultural, Temporal, Semiotic, Narrative, Ideological |
| 4 | Social, Economic, Cultural, Temporal, Semiotic, Narrative, Ideological, Experiential |
| 5 | Economic, Cultural, Temporal, Semiotic, Narrative, Ideological, Experiential, Social |
| 6 | Cultural, Temporal, Semiotic, Narrative, Ideological, Experiential, Social, Economic |
| 7 | Temporal, Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural |

## JSONL Schema (20 + 3 experiment-specific fields)

Standard 20 fields from SYNTHETIC_COHORT_EXPERIMENTS.md:
1. timestamp (ISO 8601)
2. model (short name)
3. model_id (full model identifier)
4. prompt_type ("solo_evaluation" | "paired_evaluation" | "context_evaluation")
5. brand_pair (not used -- null for solo)
6. pair_id (not used -- null for solo)
7. dimension (null)
8. brand (focal brand name)
9. run (repetition number)
10. prompt (full prompt text)
11. response (raw LLM response)
12. parsed (parsed JSON object)
13. weights (extracted 8-dimension weights or null)
14. error (error message or null)
15. latency_ms (response time)
16. temperature (0.7)
17. dimension_order (which Latin-square ordering used)
18. prompt_language ("en")
19. token_count_input (if available)
20. token_count_output (if available)

Experiment-specific fields:
21. competitor (competitor brand name, null for solo)
22. competitor_type ("direct" | "adjacent" | "distant" | null for solo)
23. condition ("solo" | "paired" | "context")

---
*Protocol frozen at commit time. Any analysis not specified above is labeled EXPLORATORY.*
