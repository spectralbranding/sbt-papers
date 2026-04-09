# R15 AI Search Metamerism -- Summary Tables (v2)

## Table 0: Experiment Metadata

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-06 |
| Script revision | v2-structured-elicitation |
| Models | groq_llama33, groq_allam, groq_kimi, grok, sarvam, gigachat_api, yandexgpt_local, gigachat_local, exaone_local, swallow_local, jais_local |
| Runs per prompt | 3 |
| Brand pairs | 10 |
| Total calls | 603 |
| Temperature | 0.7 |
| Script version | 0196717aa431a3277d0524e9efa479279aa0351a |

## Table 1: Mean Dimensional Weight Profiles (weighted_recommendation prompts)

Uniform baseline = 12.5 per dimension (100/8). Values > 12.5 = over-weighted.

| Dimension | Type | groq_llama33 | groq_allam | groq_kimi | grok | sarvam | gigachat_api | yandexgpt_local | gigachat_local | exaone_local | swallow_local | jais_local | Aggregate |
|-----------|------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| semiotic | hard | 10.0 | 14.6 | 10.0 | 15.0 | 5.0 | 10.0 | 14.3 | 10.8 | 15.0 | 18.9 | 18.3 | 12.9 |
| narrative | soft | 5.0 | 9.8 | 8.7 | 10.0 | 10.0 | 15.0 | 9.5 | 8.1 | 10.0 | 8.8 | 10.0 | 9.5 |
| ideological | soft | 10.0 | 4.9 | 9.7 | 5.0 | 5.0 | 5.0 | 14.3 | 6.0 | 5.0 | 5.1 | 6.7 | 7.0 |
| experiential | hard | 25.0 | 19.5 | 30.0 | 23.3 | 15.0 | 30.0 | 23.8 | 25.7 | 20.0 | 25.3 | 16.7 | 23.1 * |
| social | soft | 10.0 | 12.1 | 9.3 | 10.0 | 20.0 | 10.0 | 9.5 | 12.4 | 10.0 | 10.1 | 10.0 | 11.2 |
| economic | hard | 25.0 | 24.4 | 19.3 | 25.0 | 20.0 | 20.0 | 19.0 | 24.0 | 25.0 | 16.9 | 21.7 | 21.8 * |
| cultural | soft | 5.0 | 4.9 | 6.3 | 5.0 | 15.0 | 5.0 | 4.8 | 4.7 | 5.0 | 3.7 | 8.3 | 6.2 |
| temporal | soft | 10.0 | 9.8 | 6.7 | 6.7 | 10.0 | 5.0 | 4.8 | 8.2 | 10.0 | 11.2 | 8.3 | 8.2 |

\* = noticeably above uniform baseline (12.5)

## Table 2: Dimensional Collapse Index

DCI = (Economic_weight + Semiotic_weight) / 100. Baseline = 0.250.

| Model | DCI | vs Baseline | Interpretation |
|-------|-----|-------------|----------------|
| groq_llama33 | 0.350 | +0.100 | Moderate |
| groq_allam | 0.390 | +0.140 | Moderate |
| groq_kimi | 0.293 | +0.043 | Near-uniform |
| grok | 0.400 | +0.150 | Moderate |
| sarvam | 0.250 | +0.000 | Near-uniform |
| gigachat_api | 0.300 | +0.050 | Near-uniform |
| yandexgpt_local | 0.333 | +0.083 | Moderate |
| gigachat_local | 0.348 | +0.098 | Moderate |
| exaone_local | 0.400 | +0.150 | Moderate |
| swallow_local | 0.358 | +0.108 | Moderate |
| jais_local | 0.400 | +0.150 | Moderate |

## Table 3: Cross-Model Dimensional Sensitivity Similarity (Cosine)

Computed from mean weight profiles. High similarity = convergent collapse.

| Model | groq_llama33 | groq_allam | groq_kimi | grok | sarvam | gigachat_api | yandexgpt_local | gigachat_local | exaone_local | swallow_local | jais_local |
|-------|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
| groq_llama33 | 1.000 | 0.969 | 0.975 | 0.974 | 0.877 | 0.943 | 0.964 | 0.989 | 0.970 | 0.944 | 0.939 |
| groq_allam | 0.969 | 1.000 | 0.940 | 0.992 | 0.904 | 0.941 | 0.947 | 0.983 | 0.998 | 0.964 | 0.984 |
| groq_kimi | 0.975 | 0.940 | 1.000 | 0.963 | 0.854 | 0.981 | 0.975 | 0.980 | 0.942 | 0.954 | 0.918 |
| grok | 0.974 | 0.992 | 0.963 | 1.000 | 0.874 | 0.965 | 0.962 | 0.989 | 0.994 | 0.967 | 0.976 |
| sarvam | 0.877 | 0.904 | 0.854 | 0.874 | 1.000 | 0.852 | 0.839 | 0.897 | 0.888 | 0.829 | 0.888 |
| gigachat_api | 0.943 | 0.941 | 0.981 | 0.965 | 0.852 | 1.000 | 0.951 | 0.972 | 0.943 | 0.946 | 0.913 |
| yandexgpt_local | 0.964 | 0.947 | 0.975 | 0.962 | 0.839 | 0.951 | 1.000 | 0.961 | 0.948 | 0.951 | 0.948 |
| gigachat_local | 0.989 | 0.983 | 0.980 | 0.989 | 0.897 | 0.972 | 0.961 | 1.000 | 0.981 | 0.960 | 0.950 |
| exaone_local | 0.970 | 0.998 | 0.942 | 0.994 | 0.888 | 0.943 | 0.948 | 0.981 | 1.000 | 0.965 | 0.985 |
| swallow_local | 0.944 | 0.964 | 0.954 | 0.967 | 0.829 | 0.946 | 0.951 | 0.960 | 0.965 | 1.000 | 0.959 |
| jais_local | 0.939 | 0.984 | 0.918 | 0.976 | 0.888 | 0.913 | 0.948 | 0.950 | 0.985 | 0.959 | 1.000 |

## Table 4: Differentiation Gap by Brand Pair

Gap = mean(hard_dim_scores) - mean(soft_dim_scores). Positive = models differentiate
harder on hard dims even for pairs designed to differ on soft dims.

| Pair | Dim Type | Soft Mean | Hard Mean | Gap | Collapse? |
|------|----------|:---------:|:---------:|:---:|:---------:|

## Table 5: Cross-Model Probe Score Variance by Dimension Type

Prediction (H3): soft-dimension variance > hard-dimension variance.

| Brand | Hard Dim Mean Var | Soft Dim Mean Var | Soft > Hard? |
|-------|------------------:|------------------:|:------------:|
| PrivatBank | 0.037 | 0.155 | Yes |
| Tinkoff | 0.071 | 0.918 | Yes |

## Table 6: Statistical Tests

| Hypothesis | Test | Result | Supported? |
|------------|------|--------|------------|
| H1 (Economic+Semiotic over-weighting) | t-test (p=0.0000) | Mean=34.8 vs baseline=25.0 | Yes * |
| H2 (Convergent collapse) | Cosine similarity=0.946 | Threshold >= 0.85 | Yes * |
| H3 (Soft-dim higher probe variance) | t-test (p=0.1129), d=0.689 | Mean var hard=0.054, soft=0.536 | No |
| H4 (Differentiation gap) | Soft-pair gap=N/A | Positive gap = hard dims scored higher | No |

## Table 7: Aggregate Mean Weights by Dimension

Uniform baseline = 12.5. Values > 12.5 = over-weighted.

| Dimension | Type | Mean Weight | vs Baseline | Over-weighted? |
|-----------|------|:-----------:|:-----------:|:--------------:|
| semiotic | hard | 12.9 | +0.4 | Yes |
| narrative | soft | 9.5 | -3.0 | No |
| ideological | soft | 7.0 | -5.5 | No |
| experiential | hard | 23.1 | +10.6 | Yes |
| social | soft | 11.2 | -1.3 | No |
| economic | hard | 21.9 | +9.4 | Yes |
| cultural | soft | 6.2 | -6.3 | No |
| temporal | soft | 8.2 | -4.3 | No |

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
