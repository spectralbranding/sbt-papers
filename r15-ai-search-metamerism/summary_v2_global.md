# R15 AI Search Metamerism -- Summary Tables (v2)

## Table 0: Experiment Metadata

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-04 |
| Script revision | v2-structured-elicitation |
| Models | claude, gpt, gemini, deepseek, qwen3_local, gemma4_local |
| Runs per prompt | 3 |
| Brand pairs | 10 |
| Total calls | 3240 |
| Temperature | 0.7 |
| Script version | 598977bb5f8a21befab298f4f828c77c1db91997 |

## Table 1: Mean Dimensional Weight Profiles (weighted_recommendation prompts)

Uniform baseline = 12.5 per dimension (100/8). Values > 12.5 = over-weighted.

| Dimension | Type | claude | gpt | gemini | deepseek | qwen3_local | gemma4_local | Aggregate |
|-----------|------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| semiotic | hard | 13.2 | 17.5 | 13.4 | 13.2 | 12.7 | 18.8 | 14.8 |
| narrative | soft | 10.7 | 13.5 | 9.4 | 10.5 | 10.0 | 12.7 | 11.1 |
| ideological | soft | 12.0 | 14.2 | 11.6 | 12.7 | 11.9 | 10.6 | 12.2 |
| experiential | hard | 19.1 | 20.3 | 18.1 | 18.3 | 19.6 | 17.6 | 18.8 * |
| social | soft | 13.1 | 11.2 | 15.7 | 14.8 | 11.5 | 14.0 | 13.4 |
| economic | hard | 16.4 | 11.3 | 12.9 | 11.0 | 20.0 | 14.3 | 14.3 |
| cultural | soft | 7.2 | 6.1 | 9.7 | 10.7 | 5.0 | 5.0 | 7.3 |
| temporal | soft | 8.2 | 5.9 | 9.1 | 8.8 | 9.2 | 7.1 | 8.1 |

\* = noticeably above uniform baseline (12.5)

## Table 2: Dimensional Collapse Index

DCI = (Economic_weight + Semiotic_weight) / 100. Baseline = 0.250.

| Model | DCI | vs Baseline | Interpretation |
|-------|-----|-------------|----------------|
| claude | 0.296 | +0.046 | Near-uniform |
| gpt | 0.288 | +0.038 | Near-uniform |
| gemini | 0.264 | +0.014 | Near-uniform |
| deepseek | 0.242 | -0.008 | Near-uniform |
| qwen3_local | 0.327 | +0.077 | Moderate |
| gemma4_local | 0.331 | +0.081 | Moderate |

## Table 3: Cross-Model Dimensional Sensitivity Similarity (Cosine)

Computed from mean weight profiles. High similarity = convergent collapse.

| Model | claude | gpt | gemini | deepseek | qwen3_local | gemma4_local |
|-------|---------:|---------:|---------:|---------:|---------:|---------:|
| claude | 1.000 | 0.976 | 0.989 | 0.983 | 0.992 | 0.982 |
| gpt | 0.976 | 1.000 | 0.968 | 0.973 | 0.955 | 0.985 |
| gemini | 0.989 | 0.968 | 1.000 | 0.997 | 0.967 | 0.974 |
| deepseek | 0.983 | 0.973 | 0.997 | 1.000 | 0.955 | 0.968 |
| qwen3_local | 0.992 | 0.955 | 0.967 | 0.955 | 1.000 | 0.967 |
| gemma4_local | 0.982 | 0.985 | 0.974 | 0.968 | 0.967 | 1.000 |

## Table 4: Differentiation Gap by Brand Pair

Gap = mean(hard_dim_scores) - mean(soft_dim_scores). Positive = models differentiate
harder on hard dims even for pairs designed to differ on soft dims.

| Pair | Dim Type | Soft Mean | Hard Mean | Gap | Collapse? |
|------|----------|:---------:|:---------:|:---:|:---------:|

## Table 5: Cross-Model Probe Score Variance by Dimension Type

Prediction (H3): soft-dimension variance > hard-dimension variance.

| Brand | Hard Dim Mean Var | Soft Dim Mean Var | Soft > Hard? |
|-------|------------------:|------------------:|:------------:|
| Aman | 1.853 | 0.358 | No |
| Apple | 0.205 | 0.317 | Yes |
| Aspiration | 0.306 | 1.303 | Yes |
| Chase | 0.144 | 0.955 | Yes |
| Coach | 0.103 | 0.133 | Yes |
| Columbia | 0.111 | 0.215 | Yes |
| Erewhon | 2.345 | 1.249 | No |
| Four Seasons | 0.271 | 0.149 | No |
| Glossier | 0.197 | 0.507 | Yes |
| Gordons | 1.036 | 0.580 | No |
| Hendricks | 0.232 | 0.216 | No |
| Hermes | 1.573 | 0.275 | No |
| Maybelline | 0.208 | 0.243 | Yes |
| Mercedes | 0.346 | 0.151 | No |
| Nike | 0.146 | 0.334 | Yes |
| Patagonia | 0.234 | 0.259 | Yes |
| Samsung | 0.070 | 0.213 | Yes |
| Shein | 1.013 | 1.828 | Yes |
| Tesla | 0.188 | 0.291 | Yes |
| Whole Foods | 1.096 | 0.107 | No |

## Table 6: Statistical Tests

| Hypothesis | Test | Result | Supported? |
|------------|------|--------|------------|
| H1 (Economic+Semiotic over-weighting) | t-test (p=0.0170) | Mean=29.1 vs baseline=25.0 | Yes * |
| H2 (Convergent collapse) | Cosine similarity=0.975 | Threshold >= 0.85 | Yes * |
| H3 (Soft-dim higher probe variance) | t-test (p=0.7116), d=-0.096 | Mean var hard=0.584, soft=0.484 | No |
| H4 (Differentiation gap) | Soft-pair gap=-0.51 | Positive gap = hard dims scored higher | No |

## Table 7: Aggregate Mean Weights by Dimension

Uniform baseline = 12.5. Values > 12.5 = over-weighted.

| Dimension | Type | Mean Weight | vs Baseline | Over-weighted? |
|-----------|------|:-----------:|:-----------:|:--------------:|
| semiotic | hard | 14.8 | +2.3 | Yes |
| narrative | soft | 11.1 | -1.4 | No |
| ideological | soft | 12.2 | -0.3 | No |
| experiential | hard | 18.8 | +6.3 | Yes |
| social | soft | 13.4 | +0.9 | Yes |
| economic | hard | 14.3 | +1.8 | Yes |
| cultural | soft | 7.3 | -5.2 | No |
| temporal | soft | 8.1 | -4.4 | No |

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
