# R15 AI Search Metamerism -- Summary Tables (v2)

## Table 0: Experiment Metadata

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-04 |
| Script revision | v2-structured-elicitation |
| Models | claude, gpt, gemini, deepseek, qwen3_local, gemma4_local |
| Runs per prompt | 3 |
| Brand pairs | 10 |
| Total calls | 1620 |
| Temperature | 0.7 |
| Script version | 649ed3fa5f6a8bef0b873e6231c5099b956a510e |

## Table 1: Mean Dimensional Weight Profiles (weighted_recommendation prompts)

Uniform baseline = 12.5 per dimension (100/8). Values > 12.5 = over-weighted.

| Dimension | Type | claude | gpt | gemini | deepseek | qwen3_local | gemma4_local | Aggregate |
|-----------|------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| semiotic | hard | 12.0 | 17.7 | 13.3 | 11.0 | 15.0 | 17.1 | 14.3 |
| narrative | soft | 8.0 | 12.7 | 9.3 | 11.3 | 10.0 | 10.3 | 10.3 |
| ideological | soft | 12.3 | 7.3 | 9.2 | 9.3 | 5.0 | 6.2 | 8.2 |
| experiential | hard | 18.6 | 19.3 | 15.9 | 15.7 | 20.0 | 18.1 | 17.9 * |
| social | soft | 12.1 | 11.3 | 11.6 | 10.0 | 10.0 | 12.0 | 11.2 |
| economic | hard | 18.2 | 18.7 | 19.3 | 22.7 | 25.0 | 21.8 | 20.9 * |
| cultural | soft | 7.4 | 5.7 | 11.7 | 11.3 | 5.3 | 6.0 | 7.9 |
| temporal | soft | 11.5 | 7.3 | 9.7 | 8.7 | 9.7 | 8.6 | 9.2 |

\* = noticeably above uniform baseline (12.5)

## Table 2: Dimensional Collapse Index

DCI = (Economic_weight + Semiotic_weight) / 100. Baseline = 0.250.

| Model | DCI | vs Baseline | Interpretation |
|-------|-----|-------------|----------------|
| claude | 0.302 | +0.052 | Moderate |
| gpt | 0.363 | +0.113 | Moderate |
| gemini | 0.327 | +0.077 | Moderate |
| deepseek | 0.337 | +0.087 | Moderate |
| qwen3_local | 0.400 | +0.150 | Moderate |
| gemma4_local | 0.389 | +0.139 | Moderate |

## Table 3: Cross-Model Dimensional Sensitivity Similarity (Cosine)

Computed from mean weight profiles. High similarity = convergent collapse.

| Model | claude | gpt | gemini | deepseek | qwen3_local | gemma4_local |
|-------|---------:|---------:|---------:|---------:|---------:|---------:|
| claude | 1.000 | 0.965 | 0.984 | 0.972 | 0.960 | 0.969 |
| gpt | 0.965 | 1.000 | 0.970 | 0.960 | 0.979 | 0.993 |
| gemini | 0.984 | 0.970 | 1.000 | 0.991 | 0.965 | 0.977 |
| deepseek | 0.972 | 0.960 | 0.991 | 1.000 | 0.969 | 0.970 |
| qwen3_local | 0.960 | 0.979 | 0.965 | 0.969 | 1.000 | 0.992 |
| gemma4_local | 0.969 | 0.993 | 0.977 | 0.970 | 0.992 | 1.000 |

## Table 4: Differentiation Gap by Brand Pair

Gap = mean(hard_dim_scores) - mean(soft_dim_scores). Positive = models differentiate
harder on hard dims even for pairs designed to differ on soft dims.

| Pair | Dim Type | Soft Mean | Hard Mean | Gap | Collapse? |
|------|----------|:---------:|:---------:|:---:|:---------:|

## Table 5: Cross-Model Probe Score Variance by Dimension Type

Prediction (H3): soft-dimension variance > hard-dimension variance.

| Brand | Hard Dim Mean Var | Soft Dim Mean Var | Soft > Hard? |
|-------|------------------:|------------------:|:------------:|
| AlphaMega | 0.932 | 5.305 | Yes |
| Carrefour | 0.169 | 0.183 | Yes |
| Danone | 0.358 | 0.173 | No |
| Evian | 1.706 | 0.301 | No |
| Heineken | 0.226 | 0.125 | No |
| Knjaz Milos | 0.758 | 0.570 | No |
| Laima | 0.185 | 0.357 | Yes |
| Lindt | 0.182 | 0.204 | Yes |
| Tusker | 0.220 | 0.259 | Yes |
| Vinamilk | 0.269 | 0.209 | No |

## Table 6: Statistical Tests

| Hypothesis | Test | Result | Supported? |
|------------|------|--------|------------|
| H1 (Economic+Semiotic over-weighting) | t-test (p=0.0006) | Mean=35.3 vs baseline=25.0 | Yes * |
| H2 (Convergent collapse) | Cosine similarity=0.975 | Threshold >= 0.85 | Yes * |
| H3 (Soft-dim higher probe variance) | t-test (p=0.2089), d=0.197 | Mean var hard=0.500, soft=0.769 | No |
| H4 (Differentiation gap) | Soft-pair gap=N/A | Positive gap = hard dims scored higher | No |

## Table 7: Aggregate Mean Weights by Dimension

Uniform baseline = 12.5. Values > 12.5 = over-weighted.

| Dimension | Type | Mean Weight | vs Baseline | Over-weighted? |
|-----------|------|:-----------:|:-----------:|:--------------:|
| semiotic | hard | 14.3 | +1.8 | Yes |
| narrative | soft | 10.3 | -2.2 | No |
| ideological | soft | 8.2 | -4.3 | No |
| experiential | hard | 17.9 | +5.4 | Yes |
| social | soft | 11.2 | -1.3 | No |
| economic | hard | 20.9 | +8.4 | Yes |
| cultural | soft | 7.9 | -4.6 | No |
| temporal | soft | 9.2 | -3.3 | No |

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
