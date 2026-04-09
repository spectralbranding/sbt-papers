# R15 AI Search Metamerism -- Summary Tables (v2)

## Table 0: Experiment Metadata

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-05 |
| Script revision | v2-structured-elicitation |
| Models | claude, gpt, gemini, deepseek, qwen3_local, gemma4_local, cerebras_qwen3, cerebras_glm, sambanova_qwen3, sambanova_swallow, sambanova_deepseek, groq_llama33, groq_allam, groq_kimi, grok, sarvam, gigachat_api, yandexgpt_pro, yandexgpt_local, gigachat_local, exaone_local, swallow_local, falcon_arabic_local, jais_local, qwen35_local |
| Runs per prompt | 3 |
| Brand pairs | 10 |
| Total calls | 11298 |
| Temperature | 0.7 |
| Script version | 2847d81a50c6053faa4074d828ca64aceebd50f2 |

## Table 1: Mean Dimensional Weight Profiles (weighted_recommendation prompts)

Uniform baseline = 12.5 per dimension (100/8). Values > 12.5 = over-weighted.

| Dimension | Type | claude | gpt | gemini | deepseek | qwen3_local | gemma4_local | cerebras_qwen3 | cerebras_glm | sambanova_qwen3 | sambanova_swallow | sambanova_deepseek | groq_llama33 | groq_allam | groq_kimi | grok | sarvam | gigachat_api | yandexgpt_pro | yandexgpt_local | gigachat_local | exaone_local | swallow_local | falcon_arabic_local | jais_local | qwen35_local | Aggregate |
|-----------|------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| semiotic | hard | 12.0 | 16.7 | 13.4 | 12.1 | 13.9 | 14.8 | 14.6 | 0.0 | 15.0 | 15.0 | 12.5 | 11.7 | 16.4 | 11.3 | 12.8 | 13.9 | 14.5 | 14.6 | 14.8 | 12.0 | 15.6 | 18.4 | 0.0 | 21.3 | 0.0 | 12.2 |
| narrative | soft | 8.3 | 11.7 | 8.5 | 11.5 | 9.8 | 9.2 | 9.9 | 0.0 | 10.0 | 7.5 | 12.5 | 7.9 | 15.6 | 9.9 | 11.3 | 9.4 | 10.5 | 8.6 | 10.0 | 8.5 | 9.8 | 11.9 | 0.0 | 10.4 | 0.0 | 8.6 |
| ideological | soft | 12.7 | 10.6 | 9.5 | 10.0 | 7.0 | 8.5 | 10.7 | 0.0 | 5.0 | 5.0 | 10.0 | 9.5 | 10.4 | 9.1 | 12.9 | 5.5 | 11.5 | 10.3 | 12.1 | 6.8 | 6.5 | 6.4 | 0.0 | 7.3 | 0.0 | 7.6 |
| experiential | hard | 18.0 | 19.8 | 17.2 | 15.2 | 20.0 | 17.5 | 18.3 | 0.0 | 20.0 | 17.5 | 15.0 | 18.2 | 15.0 | 18.2 | 18.4 | 20.0 | 17.0 | 19.9 | 20.6 | 22.4 | 20.4 | 18.9 | 0.0 | 15.0 | 0.0 | 15.5 * |
| social | soft | 11.3 | 10.2 | 10.0 | 9.2 | 9.8 | 10.5 | 10.7 | 0.0 | 10.0 | 15.0 | 7.5 | 9.8 | 9.8 | 10.4 | 11.8 | 11.2 | 8.5 | 9.7 | 10.8 | 11.5 | 10.0 | 8.7 | 0.0 | 10.9 | 0.0 | 8.7 |
| economic | hard | 19.3 | 19.2 | 18.8 | 22.1 | 24.8 | 22.3 | 18.0 | 0.0 | 25.0 | 22.5 | 20.0 | 24.2 | 17.6 | 23.6 | 16.2 | 22.9 | 21.5 | 23.1 | 19.4 | 24.5 | 23.3 | 19.9 | 0.0 | 19.0 | 0.0 | 18.0 * |
| cultural | soft | 10.1 | 5.0 | 12.4 | 12.5 | 5.4 | 7.9 | 7.1 | 0.0 | 5.0 | 7.5 | 12.5 | 7.0 | 5.4 | 8.1 | 10.0 | 6.9 | 7.0 | 7.2 | 4.8 | 5.7 | 4.8 | 5.8 | 0.0 | 8.1 | 0.0 | 6.4 |
| temporal | soft | 8.3 | 6.9 | 10.3 | 7.5 | 9.3 | 9.3 | 10.7 | 0.0 | 10.0 | 10.0 | 10.0 | 11.6 | 9.8 | 9.3 | 6.5 | 10.2 | 9.5 | 6.7 | 7.6 | 8.5 | 9.8 | 10.0 | 0.0 | 8.0 | 0.0 | 7.7 |

\* = noticeably above uniform baseline (12.5)

## Table 2: Dimensional Collapse Index

DCI = (Economic_weight + Semiotic_weight) / 100. Baseline = 0.250.

| Model | DCI | vs Baseline | Interpretation |
|-------|-----|-------------|----------------|
| claude | 0.313 | +0.063 | Moderate |
| gpt | 0.358 | +0.108 | Moderate |
| gemini | 0.322 | +0.072 | Moderate |
| deepseek | 0.342 | +0.092 | Moderate |
| qwen3_local | 0.387 | +0.137 | Moderate |
| gemma4_local | 0.371 | +0.121 | Moderate |
| cerebras_qwen3 | 0.326 | +0.076 | Moderate |
| cerebras_glm | N/A | N/A | Insufficient data |
| sambanova_qwen3 | 0.400 | +0.150 | Moderate |
| sambanova_swallow | 0.375 | +0.125 | Moderate |
| sambanova_deepseek | 0.325 | +0.075 | Moderate |
| groq_llama33 | 0.358 | +0.108 | Moderate |
| groq_allam | 0.340 | +0.090 | Moderate |
| groq_kimi | 0.350 | +0.100 | Moderate |
| grok | 0.290 | +0.040 | Near-uniform |
| sarvam | 0.368 | +0.118 | Moderate |
| gigachat_api | 0.360 | +0.110 | Moderate |
| yandexgpt_pro | 0.377 | +0.127 | Moderate |
| yandexgpt_local | 0.342 | +0.092 | Moderate |
| gigachat_local | 0.365 | +0.115 | Moderate |
| exaone_local | 0.388 | +0.138 | Moderate |
| swallow_local | 0.383 | +0.133 | Moderate |
| falcon_arabic_local | N/A | N/A | Insufficient data |
| jais_local | 0.402 | +0.152 | HIGH collapse |
| qwen35_local | N/A | N/A | Insufficient data |

## Table 3: Cross-Model Dimensional Sensitivity Similarity (Cosine)

Computed from mean weight profiles. High similarity = convergent collapse.

| Model | claude | gpt | gemini | deepseek | qwen3_local | gemma4_local | cerebras_qwen3 | sambanova_qwen3 | sambanova_swallow | sambanova_deepseek | groq_llama33 | groq_allam | groq_kimi | grok | sarvam | gigachat_api | yandexgpt_pro | yandexgpt_local | gigachat_local | exaone_local | swallow_local | jais_local |
|-------|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
| claude | 1.000 | 0.976 | 0.991 | 0.984 | 0.969 | 0.985 | 0.989 | 0.956 | 0.965 | 0.979 | 0.981 | 0.958 | 0.986 | 0.991 | 0.971 | 0.987 | 0.986 | 0.984 | 0.969 | 0.965 | 0.958 | 0.953 |
| gpt | 0.976 | 1.000 | 0.967 | 0.962 | 0.980 | 0.985 | 0.990 | 0.975 | 0.964 | 0.960 | 0.968 | 0.983 | 0.975 | 0.980 | 0.977 | 0.988 | 0.989 | 0.997 | 0.973 | 0.985 | 0.988 | 0.977 |
| gemini | 0.991 | 0.967 | 1.000 | 0.987 | 0.968 | 0.987 | 0.987 | 0.961 | 0.971 | 0.989 | 0.978 | 0.958 | 0.983 | 0.981 | 0.976 | 0.983 | 0.978 | 0.969 | 0.963 | 0.967 | 0.967 | 0.965 |
| deepseek | 0.984 | 0.962 | 0.987 | 1.000 | 0.968 | 0.984 | 0.972 | 0.959 | 0.959 | 0.995 | 0.975 | 0.960 | 0.986 | 0.975 | 0.968 | 0.983 | 0.978 | 0.961 | 0.959 | 0.960 | 0.958 | 0.956 |
| qwen3_local | 0.969 | 0.980 | 0.968 | 0.968 | 1.000 | 0.993 | 0.979 | 0.998 | 0.983 | 0.961 | 0.992 | 0.958 | 0.993 | 0.952 | 0.997 | 0.986 | 0.992 | 0.980 | 0.995 | 0.998 | 0.983 | 0.959 |
| gemma4_local | 0.985 | 0.985 | 0.987 | 0.984 | 0.993 | 1.000 | 0.991 | 0.990 | 0.988 | 0.979 | 0.992 | 0.971 | 0.995 | 0.972 | 0.994 | 0.994 | 0.994 | 0.985 | 0.986 | 0.993 | 0.986 | 0.978 |
| cerebras_qwen3 | 0.989 | 0.990 | 0.987 | 0.972 | 0.979 | 0.991 | 1.000 | 0.973 | 0.973 | 0.976 | 0.982 | 0.981 | 0.984 | 0.985 | 0.982 | 0.993 | 0.985 | 0.992 | 0.972 | 0.982 | 0.984 | 0.973 |
| sambanova_qwen3 | 0.956 | 0.975 | 0.961 | 0.959 | 0.998 | 0.990 | 0.973 | 1.000 | 0.984 | 0.953 | 0.986 | 0.955 | 0.986 | 0.939 | 0.997 | 0.978 | 0.984 | 0.972 | 0.992 | 0.998 | 0.985 | 0.961 |
| sambanova_swallow | 0.965 | 0.964 | 0.971 | 0.959 | 0.983 | 0.988 | 0.973 | 0.984 | 1.000 | 0.949 | 0.978 | 0.946 | 0.980 | 0.948 | 0.991 | 0.968 | 0.975 | 0.964 | 0.981 | 0.984 | 0.972 | 0.968 |
| sambanova_deepseek | 0.979 | 0.960 | 0.989 | 0.995 | 0.961 | 0.979 | 0.976 | 0.953 | 0.949 | 1.000 | 0.970 | 0.969 | 0.979 | 0.973 | 0.963 | 0.983 | 0.968 | 0.957 | 0.947 | 0.956 | 0.962 | 0.956 |
| groq_llama33 | 0.981 | 0.968 | 0.978 | 0.975 | 0.992 | 0.992 | 0.982 | 0.986 | 0.978 | 0.970 | 1.000 | 0.951 | 0.996 | 0.956 | 0.989 | 0.989 | 0.987 | 0.976 | 0.988 | 0.986 | 0.968 | 0.947 |
| groq_allam | 0.958 | 0.983 | 0.958 | 0.960 | 0.958 | 0.971 | 0.981 | 0.955 | 0.946 | 0.969 | 0.951 | 1.000 | 0.961 | 0.968 | 0.957 | 0.981 | 0.960 | 0.973 | 0.939 | 0.964 | 0.981 | 0.974 |
| groq_kimi | 0.986 | 0.975 | 0.983 | 0.986 | 0.993 | 0.995 | 0.984 | 0.986 | 0.980 | 0.979 | 0.996 | 0.961 | 1.000 | 0.970 | 0.991 | 0.991 | 0.992 | 0.980 | 0.990 | 0.987 | 0.971 | 0.953 |
| grok | 0.991 | 0.980 | 0.981 | 0.975 | 0.952 | 0.972 | 0.985 | 0.939 | 0.948 | 0.973 | 0.956 | 0.968 | 0.970 | 1.000 | 0.956 | 0.977 | 0.973 | 0.983 | 0.952 | 0.952 | 0.956 | 0.954 |
| sarvam | 0.971 | 0.977 | 0.976 | 0.968 | 0.997 | 0.994 | 0.982 | 0.997 | 0.991 | 0.963 | 0.989 | 0.957 | 0.991 | 0.956 | 1.000 | 0.981 | 0.987 | 0.977 | 0.994 | 0.997 | 0.985 | 0.964 |
| gigachat_api | 0.987 | 0.988 | 0.983 | 0.983 | 0.986 | 0.994 | 0.993 | 0.978 | 0.968 | 0.983 | 0.989 | 0.981 | 0.991 | 0.977 | 0.981 | 1.000 | 0.992 | 0.989 | 0.975 | 0.985 | 0.983 | 0.971 |
| yandexgpt_pro | 0.986 | 0.989 | 0.978 | 0.978 | 0.992 | 0.994 | 0.985 | 0.984 | 0.975 | 0.968 | 0.987 | 0.960 | 0.992 | 0.973 | 0.987 | 0.992 | 1.000 | 0.991 | 0.989 | 0.989 | 0.978 | 0.966 |
| yandexgpt_local | 0.984 | 0.997 | 0.969 | 0.961 | 0.980 | 0.985 | 0.992 | 0.972 | 0.964 | 0.957 | 0.976 | 0.973 | 0.980 | 0.983 | 0.977 | 0.989 | 0.991 | 1.000 | 0.978 | 0.983 | 0.978 | 0.963 |
| gigachat_local | 0.969 | 0.973 | 0.963 | 0.959 | 0.995 | 0.986 | 0.972 | 0.992 | 0.981 | 0.947 | 0.988 | 0.939 | 0.990 | 0.952 | 0.994 | 0.975 | 0.989 | 0.978 | 1.000 | 0.992 | 0.969 | 0.941 |
| exaone_local | 0.965 | 0.985 | 0.967 | 0.960 | 0.998 | 0.993 | 0.982 | 0.998 | 0.984 | 0.956 | 0.986 | 0.964 | 0.987 | 0.952 | 0.997 | 0.985 | 0.989 | 0.983 | 0.992 | 1.000 | 0.991 | 0.969 |
| swallow_local | 0.958 | 0.988 | 0.967 | 0.958 | 0.983 | 0.986 | 0.984 | 0.985 | 0.972 | 0.962 | 0.968 | 0.981 | 0.971 | 0.956 | 0.985 | 0.983 | 0.978 | 0.978 | 0.969 | 0.991 | 1.000 | 0.986 |
| jais_local | 0.953 | 0.977 | 0.965 | 0.956 | 0.959 | 0.978 | 0.973 | 0.961 | 0.968 | 0.956 | 0.947 | 0.974 | 0.953 | 0.954 | 0.964 | 0.971 | 0.966 | 0.963 | 0.941 | 0.969 | 0.986 | 1.000 |

## Table 4: Differentiation Gap by Brand Pair

Gap = mean(hard_dim_scores) - mean(soft_dim_scores). Positive = models differentiate
harder on hard dims even for pairs designed to differ on soft dims.

| Pair | Dim Type | Soft Mean | Hard Mean | Gap | Collapse? |
|------|----------|:---------:|:---------:|:---:|:---------:|

## Table 5: Cross-Model Probe Score Variance by Dimension Type

Prediction (H3): soft-dimension variance > hard-dimension variance.

| Brand | Hard Dim Mean Var | Soft Dim Mean Var | Soft > Hard? |
|-------|------------------:|------------------:|:------------:|
| APU Chinggis | 0.130 | 0.393 | Yes |
| Al Rawabi | 0.102 | 0.194 | Yes |
| Amul | 0.418 | 0.306 | No |
| Binggrae | 0.212 | 0.389 | Yes |
| Cadbury | 0.089 | 0.141 | Yes |
| Calbee | 0.365 | 0.126 | No |
| Danone | 0.177 | 0.064 | No |
| Evian | 0.732 | 0.162 | No |
| Heineken | 0.122 | 0.076 | No |
| Lay's | 0.692 | 0.300 | No |
| Nongfu Spring | 0.202 | 0.210 | Yes |
| PrivatBank | 0.123 | 0.345 | Yes |
| Tinkoff | 0.048 | 0.501 | Yes |
| Whole Foods | 0.761 | 0.065 | No |

## Table 6: Statistical Tests

| Hypothesis | Test | Result | Supported? |
|------------|------|--------|------------|
| H1 (Economic+Semiotic over-weighting) | t-test (p=0.0000) | Mean=35.6 vs baseline=25.0 | Yes * |
| H2 (Convergent collapse) | Cosine similarity=0.976 | Threshold >= 0.85 | Yes * |
| H3 (Soft-dim higher probe variance) | t-test (p=0.7869), d=-0.163 | Mean var hard=0.298, soft=0.234 | No |
| H4 (Differentiation gap) | Soft-pair gap=N/A | Positive gap = hard dims scored higher | No |

## Table 7: Aggregate Mean Weights by Dimension

Uniform baseline = 12.5. Values > 12.5 = over-weighted.

| Dimension | Type | Mean Weight | vs Baseline | Over-weighted? |
|-----------|------|:-----------:|:-----------:|:--------------:|
| semiotic | hard | 14.4 | +1.9 | Yes |
| narrative | soft | 10.1 | -2.4 | No |
| ideological | soft | 9.0 | -3.5 | No |
| experiential | hard | 18.3 | +5.8 | Yes |
| social | soft | 10.3 | -2.2 | No |
| economic | hard | 21.2 | +8.7 | Yes |
| cultural | soft | 7.6 | -4.9 | No |
| temporal | soft | 9.1 | -3.4 | No |

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
