# L2 Prompts

This directory holds prompt templates and rendered prompt examples.

## Structure

- `templates/` — raw prompt templates (parameterized, language-agnostic)
- `rendered/` — example rendered prompts for specific brand pairs (documentation)

## Prompt Types

The experiment uses three prompt types, all defined in `ai_search_metamerism.py`:

| Constant | Type string | Purpose |
|----------|-------------|---------|
| `WEIGHTED_RECOMMENDATION_PROMPT` | `weighted_recommendation` | 100-point weight allocation across 8 SBT dimensions. Primary DCI measure. |
| `DIMENSIONAL_DIFFERENTIATION_PROMPT` | `dimensional_differentiation` | Structured 0-10 difference scores per dimension. JSON output. |
| `DIMENSION_PROBE_PROMPT` | `dimension_probe` | Individual brand scoring per dimension (0-10). 16 probes per pair. |

## Native-Language Condition (H10)

For Run 5, the `weighted_recommendation` prompt is also run in native languages:

| Language | Code | Model(s) | Brand pair |
|----------|------|----------|-----------|
| Chinese | zh | qwen3_local, cerebras_qwen3, sambanova_qwen3, sambanova_deepseek, cerebras_glm, groq_kimi, qwen35_local | china_water |
| Russian | ru | gigachat_api, yandexgpt_pro, yandexgpt_local, gigachat_local | russia_grocery |
| Japanese | ja | sambanova_swallow, swallow_local | japan_snacks |
| Korean | ko | exaone_local | korea_dairy |
| Arabic | ar | jais_local, falcon_arabic_local, groq_allam | uae_dairy |
| Hindi | hi | sarvam | india_dairy |

Native translations are in `NATIVE_WEIGHTED_RECOMMENDATION` dict in the script (manually verified, not machine-generated). JSON keys remain in English across all languages.

## Status

Run 5 is complete (2026-04-06). Representative rendered prompt examples for each
culture-language condition can be extracted from `../L3_sessions/run5_crosscultural.jsonl`.
The templates/ and rendered/ directories remain available for curated examples to be
committed manually.
