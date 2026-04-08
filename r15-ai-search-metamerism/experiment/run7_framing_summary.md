# R15 AI Search Metamerism -- Summary Tables (v2)

## Table 0: Experiment Metadata

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-08 |
| Script revision | v2-structured-elicitation |
| Models | claude, gpt, gemini, deepseek, qwen3_local, gemma4_local, cerebras_qwen3, fireworks_glm, dashscope_qwen_plus, sambanova_qwen3, sambanova_deepseek, groq_llama33, groq_allam, groq_kimi, grok, sarvam, gigachat_api, yandexgpt_pro, gptoss_swallow, yandexgpt_local, gigachat_local, exaone_local, swallow_local, falcon_arabic_local, jais_local, qwen35_local |
| Runs per prompt | 3 |
| Brand pairs | 10 |
| Total calls | 522 |
| Temperature | 0.7 |
| Script version | be35a8247ef5a4db5d513440cc387192787b668b |

## Table 1: Mean Dimensional Weight Profiles (weighted_recommendation prompts)

Uniform baseline = 12.5 per dimension (100/8). Values > 12.5 = over-weighted.

## Table 2: Dimensional Collapse Index

DCI = (Economic_weight + Semiotic_weight) / 100. Baseline = 0.250.

| Model | DCI | vs Baseline | Interpretation |
|-------|-----|-------------|----------------|
| claude | N/A | N/A | Insufficient data |
| gpt | N/A | N/A | Insufficient data |
| gemini | N/A | N/A | Insufficient data |
| deepseek | N/A | N/A | Insufficient data |
| qwen3_local | N/A | N/A | Insufficient data |
| gemma4_local | N/A | N/A | Insufficient data |
| cerebras_qwen3 | N/A | N/A | Insufficient data |
| fireworks_glm | N/A | N/A | Insufficient data |
| dashscope_qwen_plus | N/A | N/A | Insufficient data |
| sambanova_qwen3 | N/A | N/A | Insufficient data |
| sambanova_deepseek | N/A | N/A | Insufficient data |
| groq_llama33 | N/A | N/A | Insufficient data |
| groq_allam | N/A | N/A | Insufficient data |
| groq_kimi | N/A | N/A | Insufficient data |
| grok | N/A | N/A | Insufficient data |
| sarvam | N/A | N/A | Insufficient data |
| gigachat_api | N/A | N/A | Insufficient data |
| yandexgpt_pro | N/A | N/A | Insufficient data |
| gptoss_swallow | N/A | N/A | Insufficient data |
| yandexgpt_local | N/A | N/A | Insufficient data |
| gigachat_local | N/A | N/A | Insufficient data |
| exaone_local | N/A | N/A | Insufficient data |
| swallow_local | N/A | N/A | Insufficient data |
| falcon_arabic_local | N/A | N/A | Insufficient data |
| jais_local | N/A | N/A | Insufficient data |
| qwen35_local | N/A | N/A | Insufficient data |

## Table 3: Cross-Model Dimensional Sensitivity Similarity (Cosine)

Computed from mean weight profiles. High similarity = convergent collapse.

## Table 4: Differentiation Gap by Brand Pair

Gap = mean(hard_dim_scores) - mean(soft_dim_scores). Positive = models differentiate
harder on hard dims even for pairs designed to differ on soft dims.

| Pair | Dim Type | Soft Mean | Hard Mean | Gap | Collapse? |
|------|----------|:---------:|:---------:|:---:|:---------:|

## Table 5: Cross-Model Probe Score Variance by Dimension Type

Prediction (H3): soft-dimension variance > hard-dimension variance.

## Table 6: Statistical Tests

| Hypothesis | Test | Result | Supported? |
|------------|------|--------|------------|
| H1 (Economic+Semiotic over-weighting) | t-test (p=N/A) | Mean=nan vs baseline=25.0 | No |
| H2 (Convergent collapse) | Cosine similarity=N/A | Threshold >= 0.85 | No |
| H3 (Soft-dim higher probe variance) | t-test (p=N/A), d=N/A | Mean var hard=0.000, soft=0.000 | No |
| H4 (Differentiation gap) | Soft-pair gap=N/A | Positive gap = hard dims scored higher | No |

## Table 8: H12 Geopolitical Framing — Weight Profiles by City Context

For each framing pair, the table shows mean dimensional weights in each city context and the delta (city_b minus city_a). A non-zero delta indicates the model encodes geopolitical context in its dimensional weighting.

### Pair: burgerking_us_ru

Contexts: `Burger King (Moscow)` vs `Burger King (Moscow) [ru]`

| Model | Context | semio | narra | ideol | exper | socia | econo | cultu | tempo | DCI |
|-------|---------|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| cerebras_qwen3 | Burger King (Moscow) | 12.0 | 7.3 | 5.0 | 18.0 | 10.0 | 20.0 | 12.7 | 15.0 | 0.320 |
| claude | Burger King (Moscow) | 13.1 | 5.0 | 3.0 | 28.2 | 8.1 | 29.9 | 8.0 | 4.7 | 0.430 |
| dashscope_qwen_plus | Burger King (Moscow) | 12.0 | 5.0 | 8.0 | 20.0 | 11.7 | 25.0 | 11.3 | 7.0 | 0.370 |
| deepseek | Burger King (Moscow) | 10.7 | 5.0 | 4.3 | 19.3 | 4.0 | 35.0 | 15.0 | 6.7 | 0.457 |
| gemini | Burger King (Moscow) | 16.7 | 5.0 | 4.7 | 23.3 | 8.3 | 26.7 | 10.0 | 5.3 | 0.433 |
| gemma4_local | Burger King (Moscow) | 13.6 | 4.5 | 8.5 | 24.2 | 12.1 | 22.7 | 8.5 | 5.8 | 0.364 |
| gigachat_api | Burger King (Moscow) | 5.0 | 5.0 | 5.0 | 33.3 | 8.3 | 30.0 | 5.0 | 8.3 | 0.350 |
| gigachat_api | Burger King (Moscow) [ru] | 5.0 | 3.0 | 6.0 | 35.0 | 9.0 | 25.0 | 11.0 | 6.0 | 0.300 |
| gigachat_api | **delta** | +0.0 | -2.0 | +1.0 | +1.7 | +0.7 | -5.0 | +6.0 | -2.3 | -0.050 |
| gpt | Burger King (Moscow) | 13.3 | 8.3 | 6.7 | 25.0 | 11.7 | 20.0 | 10.0 | 5.0 | 0.333 |
| gptoss_swallow | Burger King (Moscow) | 6.3 | 3.3 | 7.7 | 21.7 | 9.3 | 28.3 | 16.7 | 6.7 | 0.347 |
| grok | Burger King (Moscow) | 8.7 | 3.3 | 3.3 | 28.3 | 10.0 | 33.3 | 10.0 | 3.0 | 0.420 |
| groq_allam | Burger King (Moscow) | 38.1 | 19.0 | 14.3 | 9.5 | 4.8 | 4.8 | 4.8 | 4.8 | 0.429 |
| groq_kimi | Burger King (Moscow) | 12.7 | 4.3 | 3.7 | 22.0 | 16.3 | 26.0 | 10.0 | 5.0 | 0.387 |
| groq_llama33 | Burger King (Moscow) | 11.7 | 5.0 | 5.0 | 20.0 | 13.3 | 25.0 | 10.0 | 10.0 | 0.367 |
| qwen3_local | Burger King (Moscow) | 15.0 | 5.0 | 5.0 | 23.3 | 10.0 | 30.0 | 6.7 | 5.0 | 0.450 |
| sambanova_deepseek | Burger King (Moscow) | 13.3 | 5.0 | 6.7 | 20.0 | 8.3 | 26.7 | 10.0 | 10.0 | 0.400 |
| sarvam | Burger King (Moscow) | 13.4 | 4.6 | 7.2 | 26.3 | 9.2 | 25.6 | 9.2 | 4.6 | 0.390 |
| yandexgpt_pro | Burger King (Moscow) | 15.0 | 5.0 | 10.0 | 21.7 | 10.0 | 23.3 | 9.3 | 5.7 | 0.383 |
| yandexgpt_pro | Burger King (Moscow) [ru] | 10.0 | 5.0 | 5.0 | 25.0 | 10.0 | 30.0 | 9.0 | 6.0 | 0.400 |
| yandexgpt_pro | **delta** | -5.0 | +0.0 | -5.0 | +3.3 | +0.0 | +6.7 | -0.3 | +0.3 | +0.017 |

### Pair: roshen_ru_ua

Contexts: `Roshen (Kyiv)` vs `Roshen (Kyiv) [ru]`

| Model | Context | semio | narra | ideol | exper | socia | econo | cultu | tempo | DCI |
|-------|---------|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| cerebras_qwen3 | Roshen (Kyiv) | 10.0 | 10.7 | 17.0 | 9.3 | 10.0 | 15.0 | 16.3 | 11.7 | 0.250 |
| claude | Roshen (Kyiv) | 12.7 | 8.0 | 7.0 | 16.0 | 10.0 | 16.7 | 15.0 | 14.7 | 0.293 |
| dashscope_qwen_plus | Roshen (Kyiv) | 12.0 | 8.0 | 18.7 | 10.0 | 11.3 | 15.0 | 15.0 | 10.0 | 0.270 |
| deepseek | Roshen (Kyiv) | 19.3 | 9.3 | 8.3 | 10.7 | 5.0 | 25.0 | 15.0 | 7.3 | 0.443 |
| gemini | Roshen (Kyiv) | 15.0 | 5.0 | 19.0 | 10.0 | 5.0 | 20.0 | 18.5 | 7.5 | 0.350 |
| gemma4_local | Roshen (Kyiv) | 15.6 | 8.8 | 3.7 | 10.8 | 12.7 | 11.5 | 21.2 | 15.8 | 0.271 |
| gigachat_api | Roshen (Kyiv) | 15.0 | 10.0 | 10.0 | 15.0 | 10.0 | 20.0 | 11.7 | 8.3 | 0.350 |
| gigachat_api | Roshen (Kyiv) [ru] | 15.0 | 10.0 | 5.0 | 15.0 | 10.0 | 20.0 | 15.0 | 10.0 | 0.350 |
| gigachat_api | **delta** | +0.0 | +0.0 | -5.0 | +0.0 | +0.0 | +0.0 | +3.3 | +1.7 | +0.000 |
| gpt | Roshen (Kyiv) | 15.0 | 10.0 | 10.0 | 20.0 | 13.3 | 20.0 | 6.7 | 5.0 | 0.350 |
| gptoss_swallow | Roshen (Kyiv) | 12.5 | 7.5 | 10.0 | 15.0 | 15.0 | 17.5 | 15.0 | 7.5 | 0.300 |
| grok | Roshen (Kyiv) | 16.7 | 9.3 | 5.0 | 10.0 | 9.3 | 25.0 | 18.3 | 6.3 | 0.417 |
| groq_allam | Roshen (Kyiv) | 36.4 | 18.2 | 18.2 | 9.1 | 4.5 | 4.5 | 4.5 | 4.5 | 0.409 |
| groq_kimi | Roshen (Kyiv) | 14.3 | 6.0 | 5.7 | 14.0 | 18.3 | 20.0 | 14.0 | 7.7 | 0.343 |
| groq_llama33 | Roshen (Kyiv) | 15.0 | 10.0 | 5.0 | 12.0 | 8.0 | 20.0 | 18.3 | 11.7 | 0.350 |
| qwen3_local | Roshen (Kyiv) | 18.3 | 3.3 | 5.0 | 1.7 | 23.3 | 16.7 | 25.0 | 6.7 | 0.350 |
| sambanova_deepseek | Roshen (Kyiv) | 20.0 | 10.0 | 8.3 | 15.0 | 10.0 | 20.0 | 10.0 | 6.7 | 0.400 |
| sarvam | Roshen (Kyiv) | 13.6 | 4.5 | 9.1 | 22.7 | 9.1 | 22.7 | 13.6 | 4.5 | 0.364 |
| yandexgpt_pro | Roshen (Kyiv) [ru] | 15.0 | 10.0 | 11.3 | 12.7 | 8.0 | 20.0 | 15.0 | 8.0 | 0.350 |

### Pair: volvo_eu_cn

Contexts: `Volvo XC90 (Shanghai)` vs `Volvo XC90 (Shanghai) [zh]`

| Model | Context | semio | narra | ideol | exper | socia | econo | cultu | tempo | DCI |
|-------|---------|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| cerebras_qwen3 | Volvo XC90 (Shanghai) | 14.2 | 9.3 | 15.6 | 14.8 | 12.8 | 11.4 | 9.3 | 12.7 | 0.256 |
| cerebras_qwen3 | Volvo XC90 (Shanghai) [zh] | 15.0 | 10.0 | 16.7 | 15.0 | 11.3 | 10.0 | 7.0 | 15.0 | 0.250 |
| cerebras_qwen3 | **delta** | +0.8 | +0.7 | +1.1 | +0.2 | -1.4 | -1.4 | -2.3 | +2.3 | -0.006 |
| claude | Volvo XC90 (Shanghai) | 14.0 | 8.0 | 16.0 | 18.0 | 15.0 | 12.0 | 4.0 | 13.0 | 0.260 |
| dashscope_qwen_plus | Volvo XC90 (Shanghai) | 12.0 | 8.0 | 18.0 | 15.0 | 14.0 | 16.0 | 7.0 | 10.0 | 0.280 |
| dashscope_qwen_plus | Volvo XC90 (Shanghai) [zh] | 12.0 | 8.0 | 18.0 | 15.0 | 17.3 | 12.7 | 7.0 | 10.0 | 0.247 |
| dashscope_qwen_plus | **delta** | +0.0 | +0.0 | +0.0 | +0.0 | +3.3 | -3.3 | +0.0 | +0.0 | -0.033 |
| deepseek | Volvo XC90 (Shanghai) | 20.0 | 5.0 | 25.0 | 15.0 | 15.0 | 10.0 | 5.0 | 5.0 | 0.300 |
| deepseek | Volvo XC90 (Shanghai) [zh] | 15.0 | 8.7 | 18.7 | 14.3 | 13.0 | 10.0 | 10.0 | 10.3 | 0.250 |
| deepseek | **delta** | -5.0 | +3.7 | -6.3 | -0.7 | -2.0 | +0.0 | +5.0 | +5.3 | -0.050 |
| fireworks_glm | Volvo XC90 (Shanghai) | 15.0 | 5.0 | 20.0 | 12.0 | 18.0 | 12.0 | 10.0 | 8.0 | 0.270 |
| fireworks_glm | Volvo XC90 (Shanghai) [zh] | 12.0 | 8.0 | 15.0 | 15.0 | 12.0 | 18.0 | 10.0 | 10.0 | 0.300 |
| fireworks_glm | **delta** | -3.0 | +3.0 | -5.0 | +3.0 | -6.0 | +6.0 | +0.0 | +2.0 | +0.030 |
| gemini | Volvo XC90 (Shanghai) | 18.0 | 5.0 | 18.0 | 12.3 | 19.3 | 15.7 | 6.7 | 5.0 | 0.337 |
| gemma4_local | Volvo XC90 (Shanghai) | 18.1 | 10.3 | 27.6 | 14.5 | 16.7 | 7.0 | 4.1 | 1.6 | 0.252 |
| gigachat_api | Volvo XC90 (Shanghai) | 15.0 | 6.7 | 20.0 | 15.0 | 10.0 | 15.0 | 6.7 | 11.7 | 0.300 |
| gpt | Volvo XC90 (Shanghai) | 15.0 | 10.0 | 20.0 | 18.3 | 11.7 | 13.3 | 6.7 | 5.0 | 0.283 |
| gptoss_swallow | Volvo XC90 (Shanghai) | 14.0 | 7.7 | 14.0 | 18.3 | 16.7 | 13.3 | 7.7 | 8.3 | 0.273 |
| grok | Volvo XC90 (Shanghai) | 12.0 | 8.0 | 19.3 | 15.0 | 12.7 | 20.0 | 7.0 | 6.0 | 0.320 |
| groq_kimi | Volvo XC90 (Shanghai) | 13.0 | 7.0 | 18.0 | 15.0 | 21.7 | 13.0 | 6.7 | 5.7 | 0.260 |
| groq_kimi | Volvo XC90 (Shanghai) [zh] | 14.3 | 8.0 | 17.7 | 14.0 | 12.7 | 13.7 | 9.3 | 10.3 | 0.280 |
| groq_kimi | **delta** | +1.3 | +1.0 | -0.3 | -1.0 | -9.0 | +0.7 | +2.7 | +4.7 | +0.020 |
| groq_llama33 | Volvo XC90 (Shanghai) | 15.0 | 5.0 | 20.0 | 18.0 | 12.0 | 10.0 | 5.0 | 15.0 | 0.250 |
| qwen3_local | Volvo XC90 (Shanghai) | 11.7 | 6.7 | 28.3 | 10.0 | 13.3 | 16.7 | 8.3 | 5.0 | 0.283 |
| qwen3_local | Volvo XC90 (Shanghai) [zh] | 7.5 | 12.5 | 27.5 | 10.0 | 12.5 | 22.5 | 2.5 | 5.0 | 0.300 |
| qwen3_local | **delta** | -4.2 | +5.8 | -0.8 | +0.0 | -0.8 | +5.8 | -5.8 | +0.0 | +0.017 |
| sambanova_deepseek | Volvo XC90 (Shanghai) | 15.0 | 10.0 | 20.0 | 15.0 | 15.0 | 10.0 | 6.7 | 8.3 | 0.250 |
| sarvam | Volvo XC90 (Shanghai) | 14.8 | 9.5 | 16.4 | 14.2 | 18.6 | 12.7 | 8.0 | 5.8 | 0.275 |
| yandexgpt_pro | Volvo XC90 (Shanghai) | 15.0 | 8.7 | 14.7 | 18.3 | 13.3 | 15.0 | 6.0 | 9.0 | 0.300 |

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
