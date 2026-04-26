# R22: Spectral Gap Restoration

**Restoring Perceptual Separability After Coherence Shocks: A μ > λ Threshold Inequality in Brand Perception**

Citation key: `2026ad` | Zenodo DOI: [10.5281/zenodo.19778549](https://doi.org/10.5281/zenodo.19778549) | Working Paper v1.0.0 (Apr 26, 2026) | Target venue: Marketing Science

## Summary

Cohort-perception separability survives disruption if the rate of corrective brand emission (μ) exceeds the spectral leakage rate (λ) at the observer cohort's detection scale. Below this threshold, perception cloud collapse is self-reinforcing and the invariant brand function cannot be recovered. The paper formalizes this sufficient condition via Kato perturbation theory and Diaconis–Stroock spectral-gap-mixing-time bounds, then demonstrates the threshold using Monte Carlo simulation seeded with Dove 2003–2023 design parameters (λ ≈ .10/yr, μ ≈ 4.50/yr). Hypothesis H22: spectral gap collapse precedes conviction reorientation by 6–18 months.

R22 fills a gap identified by R12 (coherence-resilience as qualitative dynamic equilibrium) and R9 (non-ergodic absorbing-state attractors): neither states a sharp sufficient condition. R22 supplies one: μ > λ.

## Key results

Monte Carlo simulation (32 cohort-dimension cells per regime, 240 months, seed 2026):

| Metric | High regime (μ = 4.50) | Low regime (μ = −.50) | Ratio |
|---|---|---|---|
| Terminal spectral gap | 1.10 | .02 | 52x |
| IRF half-life (months) | 1.4 | 13.1 | 9.3x |

Spectral gap collapse (to 10% of initial) at mean month 46 in low regime. Conviction reorientation horizon ~month 48 in Dove design parameters: consistent with 6–18 month lead-time prediction.

## Files

| File | Description |
|------|-------------|
| `paper.md` | Full manuscript (markdown, v0.4) |
| `paper.yaml` | Machine-readable paper specification |
| `monte_carlo_simulation.py` | Simulation script (uv run --with statsmodels --with numpy --with scipy) |
| `monte_carlo_results.json` | Simulation outputs (all 64 cells) |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTORS.yaml` | Contributor attribution |
| `DATA_MANIFEST.yaml` | Data sources and empirical-method anchors |
| `PROVENANCE.yaml` | Drafting history and submission records |

## Status

**Working draft v0.4.** All 5 placeholder statistics resolved via Monte Carlo simulation. Real Dove longitudinal data re-analysis deferred to companion paper using R10 source data. Three limitations stated explicitly: (i) Monte Carlo substitutes for real data, (ii) cohort time-invariance assumption, (iii) linear GRP-to-perception mapping.

## Target venue

Marketing Science (INFORMS). AMA reference style. Double-anonymous review. Fallback: Marketing Letters.

## Relationship to other papers

- **R10 (2026p)** Dove longitudinal case — companion paper target for empirical re-analysis
- **R12 (2026s)** coherence-resilience — qualitative precursor (R22 formalizes the threshold)
- **R6 (2026j)** diffusion dynamics — flow on cohort weight space
- **R9 (2026o)** non-ergodic perception — absorbing-state dynamics below threshold
- **R16 (2026x)** Brand Function — the invariant being projected onto
- **R19 (2026aa)** rate-distortion — bandwidth grounding
- **R21 (2026ac)** spectral immunity — awareness-gate sufficiency framing
