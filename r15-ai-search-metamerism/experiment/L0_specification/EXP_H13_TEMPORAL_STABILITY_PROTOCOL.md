# Experiment H13: Temporal Stability Across Model Versions

**Protocol version**: 1.0
**Date**: 2026-04-17
**Status**: PRE-REGISTERED (frozen before data collection)
**Open Problem**: #11 (Temporal stability of AI brand perception)
**Paper target**: R15 v3.0 Section 6 direction (e) / new supplementary experiment

---

## Background

R15 Section 6 direction (e) identifies temporal stability as an open question:
models evolve through version updates, and if brand perception profiles shift
significantly across versions, brand health monitoring in AI channels requires
continuous measurement rather than one-time benchmarking. This experiment
operationalises that direction with a controlled within-family version
comparison design.

Four model families are compared across their most recent major version
transition: DeepSeek (V3 vs R1), Llama (3.1-70B vs 3.3-70B), Qwen (2.5-72B
vs 3-235B), and Gemini (2.0 Flash vs 2.5 Flash). All pairs use the same API
provider and the same prompt, isolating the model version as the sole
variable.

Note on pair heterogeneity: Pair 1 (DeepSeek) is also an architecture change
(standard transformer vs reasoning model). Pair 4 (Gemini) is a major version
bump with capability improvements. Pairs 2-3 (Llama, Qwen) are
within-architecture version updates. This heterogeneity is intentional: it
allows estimation of whether architecture changes (Pair 1) produce larger
drift than parameter/data updates (Pairs 2-3).

## Research Question

Do successive versions of the same model family produce significantly
different brand perception profiles as measured by the SBT weighted
recommendation task?

## Hypotheses

### H_13a: Version Drift Exists in at Least One Family
At least one model pair produces a mean cosine similarity below .95 between
the old-version and new-version brand perception profiles.

- **Test**: Per-pair cosine similarity between mean weight profiles (old vs
  new). Computed for each of the 4 pairs.
- **Success criterion**: Any pair with cosine < .95 (threshold chosen to
  reflect perceptible drift, cf. R15 H2 cosine = .977 for cross-model
  convergence)
- **Alpha**: .05 (one-sample t-test per pair: mean cosine < .95)

### H_13b: Economic and Semiotic Dimensions Are Most Stable
Economic and Semiotic dimensions show the smallest per-dimension drift
across versions (|delta| < 3 points on the 0-100 scale).

- **Test**: Per-dimension mean weight comparison (old vs new, paired t-test
  across brand-pairs and repetitions). Primary comparison: Economic and
  Semiotic vs all other 6 dimensions.
- **Alpha**: .05 (Bonferroni-corrected for 8 dimensions: .006)
- **Success criterion**: Economic and Semiotic both satisfy |delta| < 3;
  at least 2 of the remaining 6 dimensions satisfy |delta| >= 3

### H_13c: Cultural and Temporal Dimensions Show Most Drift
Cultural and Temporal dimensions show the largest per-dimension drift across
versions (largest |delta| among all 8 dimensions in at least 2 of 4 pairs).

- **Test**: Per-dimension drift ranked by |delta| per pair. Two-sided.
- **Alpha**: .05 (Bonferroni-corrected: .006)
- **Success criterion**: Cultural or Temporal ranks 1st or 2nd by |delta|
  in at least 2 of 4 pairs

### H_13d: DCI Does Not Decrease in Newer Versions
The Dimensional Collapse Index (DCI = Economic + Semiotic weight sum) does
not decrease in the newer model version relative to the older version (i.e.,
collapse persists or worsens, not improves).

- **Test**: Paired t-test: DCI_new >= DCI_old (one-sided, alpha = .05) per
  pair, then Bonferroni-corrected across 4 pairs (.0125)
- **Success criterion**: At least 3 of 4 pairs show DCI_new >= DCI_old
  (non-significant decrease)
- **Effect size reported**: Cohen's d for each pair

## Design

### Model Pairs (cloud-only)

| Pair | Family | Old Version | New Version | Provider | API |
|------|--------|-------------|-------------|----------|-----|
| 1 | DeepSeek | deepseek-chat (V3) | deepseek-reasoner (R1) | DeepSeek | Same base URL, different model param |
| 2 | Llama | llama-3.1-70b-versatile | llama-3.3-70b-versatile | Groq | Same API |
| 3 | Qwen | qwen-2.5-72b-instruct | qwen-3-235b-a22b-instruct-2507 | Cerebras | Same API |
| 4 | Gemini | gemini-2.0-flash | gemini-2.5-flash | Google | Same API |

Rationale for pairs: these are the most recent major version transitions
available at the time of pre-registration where (a) both versions are
available on the same API endpoint, and (b) the provider is already in the
R15 experimental pipeline. This minimises confounds from API and prompt
format differences.

### Stimuli (Brand Pairs)

Five brand pairs from the R15 global set, using the canonical R15
weighted-recommendation prompt. Each pair represents a distinct product
category with distinct competitive dynamics.

| Pair ID | Brand A | Brand B | Category |
|---------|---------|---------|----------|
| luxury_heritage | Hermes | Coach | Luxury accessories |
| purpose_driven | Patagonia | Columbia | Outdoor gear |
| premium_tech | Apple | Samsung | Consumer electronics |
| artisanal_food | Erewhon | Whole Foods | Specialty grocery |
| auto_disruption | Tesla | Mercedes | Automotive |

### Prompt Type

`weighted_recommendation` (standard R15 prompt). System: brand perception
evaluator. User: compare Brand A and Brand B, allocate 100 points across 8
dimensions, respond in JSON.

Single prompt type keeps the design clean. The comparison objective is
version drift, not prompt sensitivity.

### Dimension Ordering

Latin-square balanced across 8 cyclic rotations of the 8 SBT dimensions.
Assignment: call index modulo 8. Ensures dimension-order bias does not
systematically favor old or new versions.

### Sample Size

8 model versions x 5 brand pairs x 3 repetitions = **120 calls total**.

Cell breakdown:
- Per model version: 5 pairs x 3 reps = 15 calls
- Per model family (old + new): 30 calls
- Per brand pair (all models): 8 versions x 3 reps = 24 calls

### Power Analysis

Using cosine similarity standard deviation from R15 Run 2-11 cross-model
data as a prior (SD_cosine ~ .025, drawn from R15 H2 result cosine = .977
with bootstrap CI [.965, .988]).

For a one-sample t-test of cosine < .95 threshold with alpha = .05,
power = .80: required n = 12 (using SD = .025, effect size = (.977 - .95)
/ .025 = 1.08, large). With 15 calls per model version (15 brand-pair x rep
observations contributing to one cosine estimate), the design is adequately
powered to detect version drift of d >= .80.

For H_13b/c (per-dimension drift), with n = 15 observations per condition
(old, new) and expected SD ~ 8 points (from R15 within-model variance),
minimum detectable effect at alpha = .006 (Bonferroni), power = .80:
|delta| ~ 7.5 points. This is a conservative threshold; actual drift in
under-specified dimensions may be larger.

### Random Seed

42 (reproducible).

## Prompts

### Weighted Recommendation (primary prompt)

```
System: You are evaluating brand perception for market research.

User: Compare {Brand_A} and {Brand_B}. Allocate 100 importance points
across these eight brand perception dimensions. Points must sum to 100.
Respond ONLY in this exact JSON format with no additional text:
{{"{dim_1}": <number>, "{dim_2}": <number>, "{dim_3}": <number>,
"{dim_4}": <number>, "{dim_5}": <number>, "{dim_6}": <number>,
"{dim_7}": <number>, "{dim_8}": <number>}}
```

Dimension order is Latin-square balanced per call (8 cyclic rotations).

## Analysis Plan

### Primary Analyses (pre-registered)

1. **Per-pair cosine similarity**: For each of the 4 model pairs, compute
   the mean weight profile for old-version (averaging across 5 brand pairs
   x 3 reps = 15 observations) and new-version (same). Compute cosine
   similarity between these two mean vectors. Report with 95% bootstrap CI
   (10,000 iterations, seed 42). Test H_13a: any cosine < .95.

2. **Per-dimension drift (H_13b, H_13c)**: For each pair and each of 8
   dimensions, compute |delta| = |mean_new - mean_old|. Rank dimensions by
   |delta| per pair. Report paired t-tests (old vs new, n = 15 per
   condition) with Cohen's d and 95% CI. Apply Bonferroni correction for 8
   dimensions (alpha = .006).

3. **DCI comparison (H_13d)**: For each record, compute DCI = Economic +
   Semiotic (renormalized to sum to 100 before computing). Paired t-test
   per pair: DCI_new vs DCI_old (one-sided: DCI_new >= DCI_old). Report
   Cohen's d.

### Secondary Analyses (pre-registered)

4. **Brand-pair moderation**: Does version drift vary by brand pair? One-way
   ANOVA: brand_pair (5 levels) on |cosine_old - cosine_new| within each
   model family.

5. **Architecture change vs data update**: Compare mean |delta| across all
   dimensions for Pair 1 (DeepSeek, architecture change) vs Pairs 2-3
   (within-architecture updates). Independent t-test on |delta|.

6. **DCI trajectory**: Plot DCI for each model version (old, new) per family
   as a bar chart with error bars (95% CI). Shows whether newer models
   maintain, increase, or decrease collapse.

### Exploratory Analyses (labeled as such)

7. **Profile shape preservation**: For each pair, compute Spearman
   correlation between old and new mean profiles (rank-order stability).

8. **Outlier brand pairs**: Identify brand pairs that show the largest
   drift per model family. Are certain brand competitions more version-
   sensitive than others?

9. **Cross-family comparison**: Which model family shows the largest total
   drift (mean |delta| across all dimensions)? Report ranking.

## Multiple Comparison Correction

- H_13a (4 pairs): Bonferroni alpha = .0125
- H_13b/c per-dimension tests (8 dims): Bonferroni alpha = .006
- H_13d (4 pairs, one-sided): Bonferroni alpha = .0125
- Secondary/exploratory analyses: Benjamini-Hochberg FDR at .05

## Exclusion Criteria

- API errors: recorded in `error` field, excluded from analysis
- Unparseable JSON: recorded with `parsed = null`, excluded
- Weight sum outside 100 +/- 5 after renormalization: flagged, included
  after renormalization with `weights_valid = false` note
- Model versions with > 50% error rate: excluded from that pair's
  analysis (reported separately)

## Reproducibility

- Random seed: 42
- All scripts committed before execution
- JSONL is append-only (no in-place edits)
- Full prompt stored in every record
- Temperature: 0.7 (consistent with all R15 experiments)
- 3-second minimum delay between API calls
- Exponential backoff on 429: 5s, 10s, 20s, 60s
- Latin-square ordering deterministic from call index

## JSONL Schema (extends EXPERIMENT_DATA_STANDARD.md base)

Standard required fields: `timestamp`, `model`, `prompt_type`, `prompt`

Recommended fields: `model_id`, `response`, `parsed`, `latency_ms`,
`tokens_in`, `tokens_out`, `error`, `temperature`, `run`

Experiment-specific fields:
- `model_family`: str (`"deepseek"`, `"llama"`, `"qwen"`, `"gemini"`)
- `model_generation`: str (`"old"` or `"new"`)
- `brand_pair`: str (e.g., `"Hermes vs Coach"`)
- `pair_id`: str (e.g., `"luxury_heritage"`)
- `brand_a`: str
- `brand_b`: str
- `dim_order`: list[str] (8-element list of dimension names in prompt order)
- `parsed_weights`: dict[str, float] or null
- `weights_valid`: bool
- `weight_sum_raw`: float

## Estimated Cost

120 calls across 4 providers. Per-call cost estimates from R15 pipeline:

| Provider | Model (old) | Model (new) | Cost/call est. | Calls | Subtotal |
|----------|------------|-------------|----------------|-------|----------|
| DeepSeek | deepseek-chat | deepseek-reasoner | $0.0008 avg | 30 | $0.02 |
| Groq | llama-3.1-70b | llama-3.3-70b | $0.0001 avg | 30 | $0.003 |
| Cerebras | qwen-2.5-72b | qwen-3-235b | $0.0006 avg | 30 | $0.018 |
| Google | gemini-2.0-flash | gemini-2.5-flash | $0.0003 avg | 30 | $0.009 |

**Total estimated: ~$0.20** (conservative; reasoning models may cost more)

Note: deepseek-reasoner (R1) may incur additional cost for chain-of-thought
tokens. If cost exceeds $0.50, reduce to 1 repetition (40 calls).

---

*This protocol was committed before any API calls were made. Any analysis not
listed above is labeled EXPLORATORY in the results.*
