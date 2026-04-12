# R19 Rate-Distortion Sweep — Pre-Registration Protocol

**Version:** v1.0
**Date:** 2026-04-11T00:00:00Z
**Experimenter:** Dmitry Zharnikov + AI assistant (Claude Sonnet 4.6)
**Status:** Pre-registration (timestamped before first API call to L3_sessions/)
**Repository:** spectral-branding (private)

---

## Research Question

What is the empirical R(D) curve for AI brand perception encoders? Specifically: when the
response-format constraint on an AI encoder is varied from high-rate (100-point allocation
across 8 dimensions) to low-rate (single most-important dimension), does the distortion
between the encoder's output and the canonical brand profile increase monotonically, and
do all tested encoder architectures lie on a common curve?

This is the operationalization of the theoretical framing in NOTE_RATE_DISTORTION_FRAMING.md,
which treats AI dimensional collapse as a rate-distortion-optimal encoding phenomenon.

---

## Hypotheses

**H1 (R(D) shape):** Distortion D decreases monotonically as rate R increases for each
model. Formally: for each model m, Spearman(R_bits, D_mean) < 0 with p < .05 after
Bonferroni correction across 17 models (adjusted alpha = .05/17 = .00294).

**H2 (Common curve):** All 17 confirmatory models lie on a single R(D) curve within
+/-15% relative error. Operationalized: the cross-model coefficient of variation (CV)
of mean distortion, averaged across all 5 rate conditions, is < .15.

**H3 (Shannon bound):** DEFERRED. The analytical Shannon lower bound for an 8D Dirichlet
source requires a separate mathematical exercise outside the scope of this empirical run.
This hypothesis will be addressed in a follow-up theoretical note.

**H4 (Architectural separation):** Test whether the six Western providers (Anthropic,
OpenAI, Google × 2, xAI, Meta) and the eleven cross-cultural providers (DeepSeek × 2,
Alibaba × 2, Zhipu, Moonshot, Sarvam, Sber, Yandex × 2, SDAIA) trace R(D) curves with
different slopes or different floors. Operationalized: two-sample Welch t-test on
per-model R(D) slope estimates (Western vs cross-cultural). H4 SUPPORTED if p < .05
(two-sided) AND |Cohen's d| > .50.

**H5 (Operating point invariance):** At R1 (highest tested rate, ~26 bits), all 17
confirmatory models converge to a similar distortion floor. Test: cross-model CV of
distortion at R1 < .20.

---

## Sampling Plan

### Models (confirmatory core — 17 architectures spanning 17 distinct training pipelines)

| Key | Provider | Model ID | Architectural lineage |
|-----|----------|----------|------------------------|
| claude | Anthropic | claude-haiku-4-5 | Anthropic Western |
| gpt | OpenAI | gpt-4o-mini | OpenAI Western |
| gemini | Google | gemini-2.5-flash | Google Western |
| grok | xAI | grok-3-mini | xAI Western (X/Twitter corpus) |
| groq_llama33 | Groq (Meta) | llama-3.3-70b-versatile | Meta Llama Western |
| gemma4_local | Ollama (Google) | gemma4:latest | Google Gemma Western (local inference) |
| deepseek | DeepSeek | deepseek-chat | DeepSeek Chinese |
| cerebras_qwen3 | Cerebras (Alibaba) | qwen-3-235b-a22b-instruct-2507 | Alibaba Qwen Chinese |
| dashscope_qwen_plus | DashScope (Alibaba) | qwen-plus | Alibaba Qwen Chinese |
| sambanova_deepseek | SambaNova (DeepSeek) | DeepSeek-V3-0324 | DeepSeek Chinese |
| fireworks_glm | Fireworks (Zhipu AI) | glm-4p7 | Zhipu GLM Chinese |
| groq_kimi | Groq (Moonshot AI) | moonshotai/kimi-k2-instruct | Moonshot Kimi Chinese |
| sarvam | Sarvam AI (Indus) | sarvam-m | Sarvam Indian |
| gigachat_api | Sber | GigaChat-2-Max | Sber GigaChat Russian |
| yandexgpt_pro | Yandex AI Studio | yandexgpt-pro | YandexGPT Russian |
| gptoss_swallow | Yandex AI Studio | gpt-oss-swallow | Tokyo Tech Swallow Japanese |
| groq_allam | Groq (SDAIA) | allam-2-7b | SDAIA ALLaM Arabic |

The 17 architectures span six distinct providers (Anthropic, OpenAI, Google × 2, xAI, Meta) on the Western side and eleven distinct providers (DeepSeek × 2, Alibaba × 2, Zhipu, Moonshot, Sarvam, Sber, Yandex × 2, SDAIA) on the cross-cultural side. This is the maximally architecturally diverse subset of cloud-accessible LLMs with consistent JSON-mode response support, plus one local-inference model (Gemma 4 via Ollama) for cross-checking cloud-vs-local consistency in the Western group.

### Brands (5 canonical SBT reference brands)

| Brand | Canonical profile (Sem, Nar, Ide, Exp, Soc, Eco, Cul, Tem) |
|-------|--------------------------------------------------------------|
| Hermes | [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5] |
| IKEA | [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0] |
| Patagonia | [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5] |
| Tesla | [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0] |
| Erewhon | [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5] |

Dimension order (canonical): Semiotic, Narrative, Ideological, Experiential, Social,
Economic, Cultural, Temporal.

### Rate Conditions (5)

| Code | Rate (bits) | Response format |
|------|-------------|-----------------|
| R1 | ~26 | 100-point allocation across 8 dimensions |
| R2 | ~19 | 1-5 scale rating for each dimension |
| R3 | ~13 | Low/Medium/High classification for each dimension |
| R4 | ~8 | Yes/No binary for each dimension |
| R5 | ~3 | Single most important dimension (1 of 8) |

### Repetitions

5 repetitions per (model x brand x rate) cell.

### Total calls

17 models x 5 brands x 5 rate conditions x 5 repetitions = **2,125 calls (core)**

---

## Pre-Specified Analysis Plan

### Distortion Computation

For each call, the model's 8D output is mapped to a normalized profile w_hat on the
8-dimensional simplex, then compared to the canonical brand profile w_canon (also
normalized to sum=1 using the values above / sum(values)):

1. R1 output: 8 floats summing to ~100. Normalize: divide each by their sum.
2. R2 output: 8 integers in {1..5}. Normalize: divide each by their sum.
3. R3 output: 8 categoricals {L, M, H}. Map L=1, M=3, H=5. Normalize as R2.
4. R4 output: 8 binaries {0, 1}. Normalize: divide by sum (if all-zero: add epsilon=0.05
   to each before normalizing to avoid division by zero).
5. R5 output: 1 categorical. Convert to 8D indicator vector (1.0 on chosen dim, 0.0
   elsewhere). Normalize: the vector already sums to 1.

Distortion measure (total variation distance, rescaled to [0,1]):
  d(w_hat, w_canon) = 0.5 * sum_i |w_hat_i - w_canon_i|

This is the pre-registered distortion measure. No other distortion measure will be
reported as primary in R19 (though Euclidean and cosine will be reported as secondary).

### R(D) Curve Fitting

For each model, compute mean distortion at each rate condition (averaging over brands
and repetitions). Fit a power-law decay:

  D = a * R^(-b) + c

using scipy.optimize.curve_fit. Report: fitted parameters (a, b, c), R-squared of fit,
residuals per rate condition.

### Hypothesis Tests

H1: For each of the 17 confirmatory models, compute Spearman rank correlation between
(rate_bits=[26,19,13,8,3]) and (mean_distortion at each rate). One-sided test (rho < 0).
Apply Bonferroni correction: adjusted alpha = .05/17 = .00294.
H1 is SUPPORTED if all 17 models show rho < 0 with p < .00294 (adjusted).

H2: For each rate condition, compute CV = std(mean_distortion) / mean(mean_distortion)
across the 17 models. Average CV across 5 rate conditions. H2 SUPPORTED if mean CV < .15.

H4: Two-sample Welch t-test on per-model R(D) slope estimates (Western providers
{claude, gpt, gemini, grok, groq_llama33, gemma4_local} vs cross-cultural {deepseek,
cerebras_qwen3, dashscope_qwen_plus, sambanova_deepseek, fireworks_glm, groq_kimi,
sarvam, gigachat_api, yandexgpt_pro, gptoss_swallow, groq_allam}).
H4 SUPPORTED if p < .05 (two-sided) AND |Cohen's d| > 0.5.

H5: Compute CV of mean distortion at R1 across 17 models. H5 SUPPORTED if CV < .20.

### Reporting Convention

AMA format throughout: .342 not 0.342, exact p-values (3 decimal places), effect sizes
alongside p-values. No significance stars.

---

## Stopping Rules

- **Hard cost cap:** $5.00. If cumulative cost exceeds $5.00, stop immediately and
  analyze whatever data has been collected.
- **Soft time cap:** 45 minutes wall clock for the core 750 calls. If exceeded, stop.
- **Per-cell minimum:** 3 successful repetitions out of 5. If a model fails > 2 times
  in a single (model x brand x rate) cell, log and skip that cell.
- **Network errors:** Retry once with 2-second delay, then skip. Do not retry > 1 time
  per call (deviating from R15's 3-attempt pattern to control time budget).

---

## Deviations Log

*(Empty at protocol creation. Any mid-experiment deviations must be appended here with
timestamp and justification before the analysis step.)*

---

*Pre-registration timestamp: 2026-04-11T00:00:00Z*
*This document was written BEFORE any API calls to L3_sessions/r19_rate_sweep.jsonl.*
*The analysis plan above is binding; post-hoc analyses must be labeled as exploratory.*
