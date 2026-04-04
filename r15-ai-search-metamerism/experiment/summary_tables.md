# R15 AI Search Metamerism -- Summary Tables (v2)

## Table 0: Experiment Metadata

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-04 |
| Script revision | v2-structured-elicitation |
| Models | claude, gpt, gemini, deepseek, qwen3_local, gemma4_local |
| Runs per prompt | 1 |
| Brand pairs | 10 |
| Total calls | 108 |
| Temperature | 0.7 |
| Script version | fb139f11b802c64f38cab6028595287712659d10 |

## Table 1: Mean Dimensional Weight Profiles (weighted_recommendation prompts)

Uniform baseline = 12.5 per dimension (100/8). Values > 12.5 = over-weighted.

| Dimension | Type | claude | gpt | gemini | deepseek | qwen3_local | gemma4_local | Aggregate |
|-----------|------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| semiotic | hard | 18.0 | 20.0 | 0.0 | 15.0 | 0.0 | 0.0 | 8.8 |
| narrative | soft | 12.0 | 15.0 | 0.0 | 10.0 | 0.0 | 0.0 | 6.2 |
| ideological | soft | 8.0 | 5.0 | 0.0 | 5.0 | 0.0 | 0.0 | 3.0 |
| experiential | hard | 16.0 | 20.0 | 0.0 | 20.0 | 0.0 | 0.0 | 9.3 |
| social | soft | 14.0 | 15.0 | 0.0 | 20.0 | 0.0 | 0.0 | 8.2 |
| economic | hard | 12.0 | 10.0 | 0.0 | 5.0 | 0.0 | 0.0 | 4.5 |
| cultural | soft | 4.0 | 5.0 | 0.0 | 10.0 | 0.0 | 0.0 | 3.2 |
| temporal | soft | 16.0 | 10.0 | 0.0 | 15.0 | 0.0 | 0.0 | 6.8 |

\* = noticeably above uniform baseline (12.5)

## Table 2: Dimensional Collapse Index

DCI = (Economic_weight + Semiotic_weight) / 100. Baseline = 0.250.

| Model | DCI | vs Baseline | Interpretation |
|-------|-----|-------------|----------------|
| claude | 0.300 | +0.050 | Near-uniform |
| gpt | 0.300 | +0.050 | Near-uniform |
| gemini | N/A | N/A | Insufficient data |
| deepseek | 0.200 | -0.050 | Near-uniform |
| qwen3_local | N/A | N/A | Insufficient data |
| gemma4_local | N/A | N/A | Insufficient data |

## Table 3: Cross-Model Dimensional Sensitivity Similarity (Cosine)

Computed from mean weight profiles. High similarity = convergent collapse.

| Model | claude | gpt | deepseek |
|-------|---------:|---------:|---------:|
| claude | 1.000 | 0.973 | 0.945 |
| gpt | 0.973 | 1.000 | 0.950 |
| deepseek | 0.945 | 0.950 | 1.000 |

## Table 4: Differentiation Gap by Brand Pair

Gap = mean(hard_dim_scores) - mean(soft_dim_scores). Positive = models differentiate
harder on hard dims even for pairs designed to differ on soft dims.

| Pair | Dim Type | Soft Mean | Hard Mean | Gap | Collapse? |
|------|----------|:---------:|:---------:|:---:|:---------:|

## Table 5: Cross-Model Probe Score Variance by Dimension Type

Prediction (H3): soft-dimension variance > hard-dimension variance.

| Brand | Hard Dim Mean Var | Soft Dim Mean Var | Soft > Hard? |
|-------|------------------:|------------------:|:------------:|
| Coach | 0.131 | 0.210 | Yes |
| Hermes | 2.208 | 0.422 | No |

## Table 6: Statistical Tests

| Hypothesis | Test | Result | Supported? |
|------------|------|--------|------------|
| H1 (Economic+Semiotic over-weighting) | t-test (p=0.3333) | Mean=26.7 vs baseline=25.0 | No |
| H2 (Convergent collapse) | Cosine similarity=0.956 | Threshold >= 0.85 | Yes * |
| H3 (Soft-dim higher probe variance) | t-test (p=0.8225), d=-0.520 | Mean var hard=1.169, soft=0.316 | No |
| H4 (Differentiation gap) | Soft-pair gap=-0.18 | Positive gap = hard dims scored higher | No |

## Table 7: Aggregate Mean Weights by Dimension

Uniform baseline = 12.5. Values > 12.5 = over-weighted.

| Dimension | Type | Mean Weight | vs Baseline | Over-weighted? |
|-----------|------|:-----------:|:-----------:|:--------------:|
| semiotic | hard | 17.7 | +5.2 | Yes |
| narrative | soft | 12.3 | -0.2 | No |
| ideological | soft | 6.0 | -6.5 | No |
| experiential | hard | 18.7 | +6.2 | Yes |
| social | soft | 16.3 | +3.8 | Yes |
| economic | hard | 9.0 | -3.5 | No |
| cultural | soft | 6.3 | -6.2 | No |
| temporal | soft | 13.7 | +1.2 | Yes |

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
