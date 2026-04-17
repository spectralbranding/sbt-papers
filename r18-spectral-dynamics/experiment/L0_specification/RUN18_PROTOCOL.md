# Run 18: Dimensional Velocity Detection Protocol

**Date**: 2026-04-16
**Paper**: R18 — Spectral Dynamics (Zharnikov, 2026z)
**Precedent**: Ghasemi et al. (2026) JAMS; Berger et al. (2021) JCR

---

## Methodology: Trajectory Narratives

Each brand is presented with one of four trajectory narratives describing recent directional change. The model evaluates the brand's CURRENT perception given the trajectory context. No behavioral vignette is used — trajectory is in the user prompt alongside the PRISM-B task.

---

## Pre-Registered Hypotheses

- **H1**: Rising vs Falling trajectories produce significantly different spectral profiles on at least 3 dimensions
- **H2**: Stable-high vs Falling brands differ despite matched current description (Bonnet pair resolution, p < .05)
- **H3** (exploratory): Oscillating trajectories produce wider dimensional variance than Stable

---

## Design

- 4 trajectory narratives: Rising, Falling, Stable-high, Oscillating
- 5 canonical brands: Hermes, IKEA, Patagonia, Erewhon, Tesla
- 5 models: Claude, GPT, Gemini, DeepSeek, Ollama (qwen3:30b)
- 3 repetitions per cell
- Total: 4 x 5 x 5 x 3 = **300 API calls**
- Temperature: .7
- Random seed: 42

---

## Trajectory Narratives

**Rising**: Brand investing in supply chain transparency, repair-and-reuse program, environmental footprint reduction. Reviews mention values alongside quality.

**Falling**: Brand cutting manufacturing costs, outsourcing service, shifting to performance ads. Reviews mention declining quality and impersonal service.

**Stable-high**: Brand maintaining position with consistent quality, steady marketing, stable satisfaction.

**Oscillating**: Brand alternating between sustainability commitments and cost-cutting reversals across three years.

---

## Analysis Plan

1. ANOVA: Trajectory (4) as factor, per-dimension weight as DV
2. Planned contrast: Rising vs Falling on Ideological and Cultural
3. Bonnet pair test: Stable-high vs Falling (matched current position, different velocity)
4. Oscillating vs Stable: dimensional variance comparison
5. Velocity estimation: difference between trajectory-primed and unprimed profiles

---

## Success Criteria

- H1: Rising vs Falling differs on at least 3 dimensions (p < .05)
- H2: Stable-high vs Falling differ (p < .05)
- H3: Oscillating shows wider variance than Stable (exploratory)
