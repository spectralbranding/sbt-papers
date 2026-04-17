# Run 18: Dimensional Velocity Detection — Summary

**Date**: 2026-04-16
**Total calls**: 300
**Valid responses**: 297/300 (99.0%)
**Total cost**: ~$0.25

## Models

5 models: Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Grok 4.1 Fast.

## Hypothesis Results

### H1: Rising vs Falling Trajectories — SUPPORTED (7/8 dimensions)

| Dimension | Rising Mean | Falling Mean | t | p | Cohen's d |
|-----------|-----------|------------|---|---|-----------|
| Ideological | .209 | .067 | 15.08 | <.001 | 2.48 |
| Economic | .058 | .202 | -14.28 | <.001 | -2.35 |
| Experiential | .097 | .189 | -9.82 | <.001 | -1.62 |
| Narrative | .183 | .109 | 7.61 | <.001 | 1.25 |
| Cultural | .128 | .089 | 4.33 | <.001 | .71 |
| Semiotic | .104 | .125 | -2.26 | .025 | -.37 |
| Social | .137 | .118 | 2.07 | .041 | .34 |
| Temporal | .084 | .086 | -.18 | .861 | -.03 |

Rising brands shift heavily toward Ideological (+14.2 pct pts, d = 2.48) and Narrative (+7.4, d = 1.25). Falling brands shift toward Economic (+14.4, d = -2.35) and Experiential (+9.2, d = -1.62). Only Temporal is invariant to trajectory — brands' relationship to time is perceived as constant regardless of trajectory direction.

### H2: Bonnet Pair Resolution (Stable vs Falling) — SUPPORTED (5/8 dimensions)

| Dimension | Stable Mean | Falling Mean | t | p | Cohen's d |
|-----------|-----------|------------|---|---|-----------|
| Cultural | .126 | .089 | 7.74 | <.001 | 1.27 |
| Economic | .135 | .202 | -7.22 | <.001 | -1.18 |
| Experiential | .147 | .189 | -4.19 | <.001 | -.69 |
| Semiotic | .142 | .125 | 4.02 | <.001 | .66 |
| Ideological | .105 | .067 | 3.82 | <.001 | .63 |
| Temporal | .078 | .086 | -1.64 | .104 | -.27 |
| Social | .127 | .118 | .96 | .341 | .16 |
| Narrative | .110 | .109 | .10 | .923 | .02 |

This is the core R18 theorem: two brands at the same current position but different velocities produce different spectral profiles. Stable-high brands differ from Falling brands most on Cultural (d = 1.27) and Economic (d = -1.18). LLMs perceive trajectory, not just position.

### H3: Oscillating Variance — EXPLORATORY SUPPORTED

Oscillating trajectories produce wider variance than Stable on 3/8 dimensions (Temporal, Semiotic, Cultural). Overall mean variance is higher for Oscillating (.001219) vs Stable (.001075). Temporal variance is 6x higher for Oscillating (.00299 vs .00050) — directional flips create maximal uncertainty about a brand's temporal positioning.

## Key Findings

1. **LLMs perceive brand velocity**: Rising vs Falling produce dramatically different profiles (d > 2 on Ideological and Economic). This is not just position — it's direction.
2. **Bonnet pair resolution works**: Stable-high vs Falling brands are perceptually distinct despite no explicit "current state" difference in the prompt. Velocity is an independent perceptual signal.
3. **Temporal dimension is velocity-invariant**: The only dimension unaffected by trajectory direction. Brands' relationship to time is perceived as a fixed attribute, not a dynamic one.
4. **Falling brands collapse toward Economic**: When brands decline, observers weight value/price much higher (d = -2.35 Rising vs Falling). This connects to the "Economic Default" finding in R15.
5. **Oscillating creates Temporal uncertainty**: Dimensional flips produce 6x the Temporal variance of stable brands — observers cannot anchor a brand's temporal identity when its trajectory reverses.
