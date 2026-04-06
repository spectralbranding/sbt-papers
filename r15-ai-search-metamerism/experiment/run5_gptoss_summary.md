# R15 AI Search Metamerism -- Summary Tables (v2)

## Table 0: Experiment Metadata

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-06 |
| Script revision | v2-structured-elicitation |
| Models | gptoss_swallow |
| Runs per prompt | 3 |
| Brand pairs | 10 |
| Total calls | 435 |
| Temperature | 0.7 |
| Script version | 839f778adea417af3b951f4d848a3181ab395ffe |

## Table 1: Mean Dimensional Weight Profiles (weighted_recommendation prompts)

Uniform baseline = 12.5 per dimension (100/8). Values > 12.5 = over-weighted.

| Dimension | Type | gptoss_swallow | Aggregate |
|-----------|------|----------:|----------:|
| semiotic | hard | 13.3 | 13.3 |
| narrative | soft | 9.1 | 9.1 |
| ideological | soft | 7.4 | 7.4 |
| experiential | hard | 19.8 | 19.8 * |
| social | soft | 10.5 | 10.5 |
| economic | hard | 24.7 | 24.7 * |
| cultural | soft | 5.7 | 5.7 |
| temporal | soft | 9.4 | 9.4 |

\* = noticeably above uniform baseline (12.5)

## Table 2: Dimensional Collapse Index

DCI = (Economic_weight + Semiotic_weight) / 100. Baseline = 0.250.

| Model | DCI | vs Baseline | Interpretation |
|-------|-----|-------------|----------------|
| gptoss_swallow | 0.380 | +0.130 | Moderate |

## Table 3: Cross-Model Dimensional Sensitivity Similarity (Cosine)

Computed from mean weight profiles. High similarity = convergent collapse.

| Model | gptoss_swallow |
|-------|---------:|
| gptoss_swallow | 1.000 |

## Table 4: Differentiation Gap by Brand Pair

Gap = mean(hard_dim_scores) - mean(soft_dim_scores). Positive = models differentiate
harder on hard dims even for pairs designed to differ on soft dims.

| Pair | Dim Type | Soft Mean | Hard Mean | Gap | Collapse? |
|------|----------|:---------:|:---------:|:---:|:---------:|

## Table 5: Cross-Model Probe Score Variance by Dimension Type

Prediction (H3): soft-dimension variance > hard-dimension variance.

| Brand | Hard Dim Mean Var | Soft Dim Mean Var | Soft > Hard? |
|-------|------------------:|------------------:|:------------:|
| APU Chinggis | -- | -- | No |
| Al Rawabi | -- | -- | No |
| Amul | -- | -- | No |
| Binggrae | -- | -- | No |
| Cadbury | -- | -- | No |
| Calbee | -- | -- | No |
| Danone | -- | -- | No |
| Evian | -- | -- | No |
| Heineken | -- | -- | No |
| Lay's | -- | -- | No |
| Nongfu Spring | -- | -- | No |
| Roshen | -- | -- | No |
| VkusVill | -- | -- | No |
| Whole Foods | -- | -- | No |

## Table 6: Statistical Tests

| Hypothesis | Test | Result | Supported? |
|------------|------|--------|------------|
| H1 (Economic+Semiotic over-weighting) | t-test (p=N/A) | Mean=38.0 vs baseline=25.0 | Yes * |
| H2 (Convergent collapse) | Cosine similarity=N/A | Threshold >= 0.85 | No |
| H3 (Soft-dim higher probe variance) | t-test (p=N/A), d=N/A | Mean var hard=0.000, soft=0.000 | No |
| H4 (Differentiation gap) | Soft-pair gap=N/A | Positive gap = hard dims scored higher | No |

## Table 7: Aggregate Mean Weights by Dimension

Uniform baseline = 12.5. Values > 12.5 = over-weighted.

| Dimension | Type | Mean Weight | vs Baseline | Over-weighted? |
|-----------|------|:-----------:|:-----------:|:--------------:|
| semiotic | hard | 13.3 | +0.8 | Yes |
| narrative | soft | 9.1 | -3.4 | No |
| ideological | soft | 7.4 | -5.1 | No |
| experiential | hard | 19.8 | +7.3 | Yes |
| social | soft | 10.5 | -2.0 | No |
| economic | hard | 24.7 | +12.2 | Yes |
| cultural | soft | 5.7 | -6.8 | No |
| temporal | soft | 9.4 | -3.1 | No |

---

## Interpretation

If H1 is supported: LLMs allocate disproportionate importance to Economic and
Semiotic dimensions when recommending brands, collapsing 8-dimensional perception
to 2 quantifiable dimensions.

If H2 is supported: This weighting pattern is consistent across model families,
indicating it is a property of text-based training corpora rather than any
specific architecture -- a structural feature of AI-mediated brand search.

If H3 is supported: Cross-model agreement is higher on Economic and Semiotic
probe scores than on Cultural and Temporal scores, confirming differential
dimensional sensitivity.

If H4 is supported: Brands that differ most on soft dimensions (Narrative,
Ideological, Cultural, Temporal) appear more similar through AI-mediated search
than their actual spectral distance would predict -- the operational signature
of spectral metamerism.

Theoretical implication: Brands investing in soft-dimension differentiation face
an AI search penalty. Their perception clouds are real but invisible to the AI
mediator. This creates systematic misalignment between observer perception and
AI-mediated brand representation.
