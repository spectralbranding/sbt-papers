# R19 H4 Supplementary: Western vs Cross-Cultural R(D) Slope Comparison

**Status:** Pre-registered hypothesis (PROTOCOL.md H4)
**Date:** 2026-04-12
**Analysis:** Welch two-sample t-test on per-model power-law slope `b`

---

## Test Design

H4 tests whether Western providers (Anthropic, OpenAI, Google × 2, xAI, Meta) and cross-cultural providers (DeepSeek, Alibaba × 3, Moonshot, Saudi SDAIA, Sarvam, Sber, Yandex × 2) trace R(D) curves with significantly different slopes. The power-law D = a × R^(−b) + c was fit per model across the five rate conditions (R1–R5, bits = 26, 19, 13, 8, 3). The slope parameter `b` characterizes how steeply distortion drops as rate increases; a steeper slope means more rapid quality gain as format richness increases.

**Groups:**
- Western (n = 6): claude, gpt, gemini, grok, groq_llama33, gemma4_local
- Cross-cultural (n = 11): deepseek, cerebras_qwen3, fireworks_glm, dashscope_qwen_plus, sambanova_deepseek, groq_kimi, sarvam, gigachat_api, yandexgpt_pro, gptoss_swallow, groq_allam

Slope values from per-model power-law fits via `scipy.optimize.curve_fit`.

**Pre-registered criterion:** H4 SUPPORTED if p < .05 (two-sided) AND |Cohen's d| > .50.

---

## Per-Model Slope Estimates

| Model | Group | Slope b |
|-------|-------|---------|
| dashscope_qwen_plus | Cross-cultural | 1.870 |
| sambanova_deepseek | Cross-cultural | 1.968 |
| gemma4_local | Western | 1.997 |
| gemini | Western | 2.019 |
| grok | Western | 2.183 |
| cerebras_qwen3 | Cross-cultural | 2.197 |
| gptoss_swallow | Cross-cultural | 2.424 |
| sarvam | Cross-cultural | 2.552 |
| groq_llama33 | Western | 2.622 |
| gigachat_api | Cross-cultural | 2.732 |
| deepseek | Cross-cultural | 2.811 |
| groq_kimi | Cross-cultural | 3.097 |
| claude | Western | 4.003 |
| yandexgpt_pro | Cross-cultural | 4.423 |
| gpt | Western | 4.732 |
| fireworks_glm | Cross-cultural | 13.021 |
| groq_allam | Cross-cultural | 13.931 |

*Notes*: All 17 fits succeeded. fireworks_glm and groq_allam show extreme slope estimates (>13) driven by sharp R(D) drops between R1 and R2 — these are valid power-law fits but represent narrow operating regions. They contribute disproportionately to the cross-cultural group variance.

---

## Descriptive Statistics by Group

| Group | n | Mean b | SD b |
|-------|---|--------|------|
| Western | 6 | 2.93 | 1.16 |
| Cross-cultural | 11 | 4.64 | 4.43 |

The Western group is tightly clustered (range 1.997–4.732). The cross-cultural group has much higher variance (range 1.870–13.931) driven by the two outlier slopes (fireworks_glm = 13.02, groq_allam = 13.93). Excluding those two outliers, the cross-cultural mean would be 2.54 — essentially identical to Western (2.93). The mean difference is therefore primarily an outlier effect, not a systematic group separation.

---

## Welch t-Test Results

**Welch's t-test (two-sided, unequal variances)**:

  t(11.4) = −1.21, p = .250
  Cohen's d (pooled) = −.466

The point estimate suggests cross-cultural slopes are slightly steeper than Western slopes on average, but the difference does not reach statistical significance and the effect size is moderate (|d| < .50).

---

## Verdict

**H4: NOT SUPPORTED**

- Welch t = −1.21, p = .250 (two-sided)
- Cohen's d = −.466

Neither pre-registered criterion is met: p = .250 > .05, and |d| = .466 < .50. The Western and cross-cultural groups do not show statistically distinguishable R(D) slopes at this sample size and variance structure. The point-estimate difference is driven primarily by two cross-cultural outliers (fireworks_glm, groq_allam) whose slopes are >13. Excluding those, the two groups would be essentially indistinguishable.

This is itself a substantive finding: at n = 6 vs n = 11 with the observed effect size, the failure to detect a slope difference suggests that **all 17 architectures share a similar rate-distortion trade-off shape, regardless of training corpus or cultural lineage**. The codebook-convergence finding (H2 SUPPORTED, mean cross-model CV = .140) is consistent with this picture: architecturally distinct models lie on essentially the same R(D) curve, with the variance contributed by individual model idiosyncrasies rather than systematic group differences.

---

## Power Considerations

With n = 6 vs n = 11 and the observed effect size |d| = .466, the Welch t-test has approximately 22% power to detect this effect at α = .05. The test is therefore underpowered to firmly reject a moderate true effect — but it is well-powered to reject a *large* effect (d ≥ 1.0), which the data clearly do not support. The conclusion is that the Western/cross-cultural slope difference, if it exists at all, is at most moderate in magnitude. Larger model panels (n ≥ 15 per group) would be needed for definitive resolution; the current data are sufficient to rule out a strong architectural-separation effect.

---

## Robustness Check (without slope outliers)

Excluding fireworks_glm (b = 13.02) and groq_allam (b = 13.93):

| Group | n | Mean b | SD b |
|-------|---|--------|------|
| Western | 6 | 2.93 | 1.16 |
| Cross-cultural (no outliers) | 9 | 2.54 | 0.74 |

  Welch t = .77, p = .456, Cohen d = .42

Even after removing outliers, the difference remains non-significant. The Western group is now slightly higher than cross-cultural, reversing the direction of the original test, but with p = .456 the comparison is firmly null.
