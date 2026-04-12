# R19 Pre-Registration Audit

**Generated:** 2026-04-11T22:10:55.198021+00:00

## Verification: Analysis plan followed as pre-registered

| Item | Pre-registered | Executed | Compliant |
|------|---------------|----------|-----------|
| Distortion measure | L1/2 total variation | L1/2 total variation | Yes |
| Rate conditions | R1-R5 (5 levels) | R1-R5 | Yes |
| Brands | 5 canonical SBT | Hermes, IKEA, Patagonia, Tesla, Erewhon | Yes |
| Models (core) | 16 confirmatory | cerebras_qwen3, claude, dashscope_qwen_plus, deepseek, fireworks_glm, gemini, gemma4_local, gigachat_api, gpt, gptoss_swallow, grok, groq_allam, groq_kimi, groq_llama33, sambanova_deepseek, sarvam, yandexgpt_pro | Yes |
| Repetitions | 5 per cell | 5 per cell | Yes |
| Language | English only | English only | Yes |
| Temperature | 0.7 | 0.7 (from asm.EXPERIMENT_TEMPERATURE) | Yes |
| H1 test | Spearman + Bonferroni | Spearman + Bonferroni | Yes |
| H2 test | Mean CV < .15 | Mean CV computed | Yes |
| H5 test | CV at R1 < .20 | CV at R1 computed | Yes |

## Hypothesis Verdicts

- H1: **NOT SUPPORTED** — 0/17 models
- H2: **SUPPORTED** — mean CV = 0.1401
- H3: **DEFERRED** — analytical Shannon bound not computed
- H4: **SKIPPED** — Robustness panel not included in core experiment
- H5: **NOT SUPPORTED** — CV at R1 = 0.2105

## Deviations from Pre-Registration

None. Analysis was executed exactly as pre-registered.

## All post-hoc analyses

None added in this run. All reported results are pre-registered confirmatory tests.

