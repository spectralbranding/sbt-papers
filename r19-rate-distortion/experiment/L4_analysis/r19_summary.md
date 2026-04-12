# R19 Rate-Distortion Sweep — Results Summary

**Generated:** 2026-04-11T22:10:55.198021+00:00
**Models:** cerebras_qwen3, claude, dashscope_qwen_plus, deepseek, fireworks_glm, gemini, gemma4_local, gigachat_api, gpt, gptoss_swallow, grok, groq_allam, groq_kimi, groq_llama33, sambanova_deepseek, sarvam, yandexgpt_pro
**Brands:** Hermes, IKEA, Patagonia, Tesla, Erewhon
**Rate conditions:** R1, R2, R3, R4, R5
**Total records:** 1652 (valid: 1621)

## Executive Summary

H1 (monotonic R(D) shape): **NOT SUPPORTED** — 0/17 models pass Spearman test at Bonferroni-corrected alpha = 0.0029.

H2 (common curve): **SUPPORTED** — mean cross-model CV = 0.1401 (threshold .15).

H5 (R1 operating-point convergence): **NOT SUPPORTED** — cross-model CV at R1 = 0.2105 (threshold .20).

## Method

Five rate conditions applied to 5 canonical SBT reference brands across 6 AI models.
Distortion = L1/2 total variation distance between model output (normalized to sum=1)
and canonical brand profile (normalized to sum=1).

| Code | Rate (bits) | Response format |
|------|------------|-----------------|
| R1 | 26 | 100-point allocation across 8 dimensions |
| R2 | 19 | 1-5 scale rating for each dimension |
| R3 | 13 | Low/Medium/High classification |
| R4 | 8 | Yes/No binary for each dimension |
| R5 | 3 | Single most important dimension |

## Per-Model R(D) Curves

Mean distortion at each rate condition, averaged over 5 brands and repetitions.

| Model | R1 (26b) | R2 (19b) | R3 (13b) | R4 (8b) | R5 (3b) | fit R² |
|-------|-------|-------|-------|-------|-------|--------|
| cerebras_qwen3 | .1 | .087 | .114 | .173 | .834 | .0 |
| claude | .159 | .079 | .099 | .132 | .835 | .986 |
| dashscope_qwen_plus | .14 | .083 | .112 | .23 | .865 | .992 |
| deepseek | .148 | .087 | .095 | .166 | .861 | .993 |
| fireworks_glm | .223 | .099 | .098 | .13 | .86 | .962 |
| gemini | .155 | .08 | .088 | .221 | .843 | .985 |
| gemma4_local | .18 | .091 | .107 | .241 | .842 | .981 |
| gigachat_api | .189 | .091 | .119 | .195 | .881 | .986 |
| gpt | .202 | .078 | .101 | .141 | .879 | .973 |
| gptoss_swallow | .162 | .084 | .13 | .193 | .861 | .992 |
| grok | .145 | .077 | .1 | .198 | .833 | .991 |
| groq_allam | .258 | .123 | .151 | .14 | .859 | .954 |
| groq_kimi | .16 | .078 | .106 | .156 | .859 | .989 |
| groq_llama33 | .162 | .074 | .102 | .179 | .87 | .989 |
| sambanova_deepseek | .149 | .087 | .113 | .225 | .859 | .991 |
| sarvam | .187 | .093 | .113 | .205 | .859 | .985 |
| yandexgpt_pro | .198 | .095 | .133 | .154 | .874 | .981 |

## Cross-Model Comparison by Rate Condition

CV = coefficient of variation of mean distortion across models at each rate.

| Rate | Bits | Mean distortion | Std | CV |
|------|------|-----------------|-----|----|
| R1 | 26 | .172 | .036 | .21 |
| R2 | 19 | .087 | .011 | .132 |
| R3 | 13 | .111 | .016 | .143 |
| R4 | 8 | .181 | .036 | .198 |
| R5 | 3 | .857 | .015 | .018 |

## Hypothesis Verdicts

**H1 — R(D) shape** (monotonic decrease): **NOT SUPPORTED**
Bonferroni-corrected alpha = 0.0029

| Model | Spearman rho | p (one-sided) | Monotonic |
|-------|-------------|---------------|-----------|
| cerebras_qwen3 | -.9 | .019 | Yes |
| claude | -.4 | .252 | Yes |
| dashscope_qwen_plus | -.7 | .094 | Yes |
| deepseek | -.7 | .094 | Yes |
| fireworks_glm | -.3 | .312 | Yes |
| gemini | -.7 | .094 | Yes |
| gemma4_local | -.7 | .094 | Yes |
| gigachat_api | -.7 | .094 | Yes |
| gpt | -.4 | .252 | Yes |
| gptoss_swallow | -.7 | .094 | Yes |
| grok | -.7 | .094 | Yes |
| groq_allam | -.3 | .312 | Yes |
| groq_kimi | -.4 | .252 | Yes |
| groq_llama33 | -.7 | .094 | Yes |
| sambanova_deepseek | -.7 | .094 | Yes |
| sarvam | -.7 | .094 | Yes |
| yandexgpt_pro | -.4 | .252 | Yes |

**H2 — Common curve** (mean CV < .15): **SUPPORTED**
Mean cross-model CV = 0.1401 (threshold = .15)

**H3 — Shannon bound**: **DEFERRED** (analytical exercise required)

**H4 — Architectural separation**: **SKIPPED** (robustness panel not run)

**H5 — R1 convergence** (CV < .20): **NOT SUPPORTED**
Cross-model CV at R1 = 0.2105 (threshold = .20, n=17 models)

## Limitations and Caveats

1. Canonical brand profiles are theoretically-derived, not empirically validated from human cohorts.
   Distortion measures deviation from theoretical ideals, not from human perceptual ground truth.
2. R5 (single-dimension) is an extreme compression that produces indicator vectors;
   distortion values at R5 are dominated by the mismatch between 1D and 8D representations.
3. English only. Native-language extensions may shift operating points.
4. Local models (Ollama) may produce systematically different outputs depending on hardware.
5. R2 normalization (divide by sum) may amplify noise when ratings cluster tightly.

## Files Generated

- `/Users/d/projects/spectral-branding/research/R19_rate_distortion/experiment/L3_sessions/r19_rate_sweep.jsonl` — per-call JSONL session log
- `/Users/d/projects/spectral-branding/research/R19_rate_distortion/experiment/L4_analysis/r19_results.json` — aggregated results JSON
- `/Users/d/projects/spectral-branding/research/R19_rate_distortion/experiment/L4_analysis/r19_per_cell.csv` — long-format per-cell CSV
- `/Users/d/projects/spectral-branding/research/R19_rate_distortion/experiment/L4_analysis/r19_rd_curves.csv` — per-model R(D) curve data + fit
- `/Users/d/projects/spectral-branding/research/R19_rate_distortion/experiment/L4_analysis/r19_summary.md` — this summary
- `/Users/d/projects/spectral-branding/research/R19_rate_distortion/experiment/L4_analysis/r19_pre_registration_audit.md` — pre-registration audit

