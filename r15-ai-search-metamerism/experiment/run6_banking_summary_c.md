# R15 AI Search Metamerism -- Summary Tables (v2)

## Table 0: Experiment Metadata

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-07 |
| Script revision | v2-structured-elicitation |
| Models | cerebras_glm, sambanova_qwen3, sambanova_swallow, sambanova_deepseek, groq_llama33, gigachat_api, yandexgpt_pro, gptoss_swallow, swallow70_local, qwen35_local |
| Runs per prompt | 3 |
| Brand pairs | 10 |
| Total calls | 600 |
| Temperature | 0.7 |
| Script version | 12b97c69793751d80f8620aaea6beadf8170a6ee |

## Table 1: Mean Dimensional Weight Profiles (weighted_recommendation prompts)

Uniform baseline = 12.5 per dimension (100/8). Values > 12.5 = over-weighted.

| Dimension | Type | cerebras_glm | sambanova_qwen3 | sambanova_swallow | sambanova_deepseek | groq_llama33 | gigachat_api | yandexgpt_pro | gptoss_swallow | swallow70_local | qwen35_local | Aggregate |
|-----------|------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| semiotic | hard | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 12.5 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| narrative | soft | 0.0 | 0.0 | 0.0 | 0.0 | 5.0 | 11.7 | 0.0 | 0.0 | 0.0 | 0.0 | 1.5 |
| ideological | soft | 0.0 | 0.0 | 0.0 | 0.0 | 7.5 | 5.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.1 |
| experiential | hard | 0.0 | 0.0 | 0.0 | 0.0 | 25.0 | 24.2 | 0.0 | 0.0 | 0.0 | 0.0 | 4.5 |
| social | soft | 0.0 | 0.0 | 0.0 | 0.0 | 12.5 | 10.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| economic | hard | 0.0 | 0.0 | 0.0 | 0.0 | 25.0 | 22.5 | 0.0 | 0.0 | 0.0 | 0.0 | 4.3 |
| cultural | soft | 0.0 | 0.0 | 0.0 | 0.0 | 5.0 | 5.8 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| temporal | soft | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 8.3 | 0.0 | 0.0 | 0.0 | 0.0 | 1.7 |

\* = noticeably above uniform baseline (12.5)

## Table 2: Dimensional Collapse Index

DCI = (Economic_weight + Semiotic_weight) / 100. Baseline = 0.250.

| Model | DCI | vs Baseline | Interpretation |
|-------|-----|-------------|----------------|
| cerebras_glm | N/A | N/A | Insufficient data |
| sambanova_qwen3 | N/A | N/A | Insufficient data |
| sambanova_swallow | N/A | N/A | Insufficient data |
| sambanova_deepseek | N/A | N/A | Insufficient data |
| groq_llama33 | 0.350 | +0.100 | Moderate |
| gigachat_api | 0.350 | +0.100 | Moderate |
| yandexgpt_pro | N/A | N/A | Insufficient data |
| gptoss_swallow | N/A | N/A | Insufficient data |
| swallow70_local | N/A | N/A | Insufficient data |
| qwen35_local | N/A | N/A | Insufficient data |

## Table 3: Cross-Model Dimensional Sensitivity Similarity (Cosine)

Computed from mean weight profiles. High similarity = convergent collapse.

| Model | groq_llama33 | gigachat_api |
|-------|---------:|---------:|
| groq_llama33 | 1.000 | 0.978 |
| gigachat_api | 0.978 | 1.000 |

## Table 4: Differentiation Gap by Brand Pair

Gap = mean(hard_dim_scores) - mean(soft_dim_scores). Positive = models differentiate
harder on hard dims even for pairs designed to differ on soft dims.

| Pair | Dim Type | Soft Mean | Hard Mean | Gap | Collapse? |
|------|----------|:---------:|:---------:|:---:|:---------:|

## Table 5: Cross-Model Probe Score Variance by Dimension Type

Prediction (H3): soft-dimension variance > hard-dimension variance.

| Brand | Hard Dim Mean Var | Soft Dim Mean Var | Soft > Hard? |
|-------|------------------:|------------------:|:------------:|
| PrivatBank | -- | -- | No |
| Tinkoff | 0.000 | 0.000 | No |

## Table 6: Statistical Tests

| Hypothesis | Test | Result | Supported? |
|------------|------|--------|------------|
| H1 (Economic+Semiotic over-weighting) | t-test (p=0.0000) | Mean=35.0 vs baseline=25.0 | Yes * |
| H2 (Convergent collapse) | Cosine similarity=0.978 | Threshold >= 0.85 | Yes * |
| H3 (Soft-dim higher probe variance) | t-test (p=N/A), d=N/A | Mean var hard=0.000, soft=0.000 | No |
| H4 (Differentiation gap) | Soft-pair gap=N/A | Positive gap = hard dims scored higher | No |

## Table 7: Aggregate Mean Weights by Dimension

Uniform baseline = 12.5. Values > 12.5 = over-weighted.

| Dimension | Type | Mean Weight | vs Baseline | Over-weighted? |
|-----------|------|:-----------:|:-----------:|:--------------:|
| semiotic | hard | 11.2 | -1.2 | No |
| narrative | soft | 8.3 | -4.2 | No |
| ideological | soft | 6.2 | -6.2 | No |
| experiential | hard | 24.6 | +12.1 | Yes |
| social | soft | 11.2 | -1.2 | No |
| economic | hard | 23.8 | +11.2 | Yes |
| cultural | soft | 5.4 | -7.1 | No |
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

If H12 is supported: The same brand receives systematically different dimensional
weight profiles when evaluated in different geopolitical city contexts. Non-zero
deltas in Table 8 indicate that LLMs encode geopolitical framing in their
dimensional weighting, demonstrating that brand perception in AI systems is
context-dependent, not purely brand-intrinsic.

Theoretical implication: Brands investing in soft-dimension differentiation face
an AI search penalty. Their perception clouds are real but invisible to the AI
mediator. This creates systematic misalignment between observer perception and
AI-mediated brand representation.
