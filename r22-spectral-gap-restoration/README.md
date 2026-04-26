# R22: Spectral Gap Restoration

**Spectral Gap Restoration: A Threshold Inequality for Cohort Separability Survival in Brand Perception**

Citation key: `2026ad` | Status: Working draft v0.3 | Target venue: Marketing Letters

## Summary

Cohort-perception separability survives disruption if the rate of corrective brand emission (μ) exceeds the spectral leakage rate (λ) at the observer cohort's detection scale. Below this threshold, perception cloud collapse is self-reinforcing and the invariant brand function cannot be recovered. The paper formalizes this sufficient condition via Kato perturbation theory and Diaconis–Stroock spectral-gap-mixing-time bounds, then proposes an empirical re-analysis of R10 Dove longitudinal data (2003–2023) to test whether spectral gap collapse precedes brand-conviction reorientation by 6–18 months (Hypothesis H22).

R22 fills a gap identified by R12 (coherence-resilience as qualitative dynamic equilibrium) and R9 (non-ergodic absorbing-state attractors): neither states a sharp sufficient condition. R22 supplies one: μ > λ.

## Key contribution

First sufficient condition for brand-cohort separability survival under disruption expressed as an empirically estimable rate inequality. Where prior work (Aaker 1991; Park, Jaworski & MacInnis 1986) identified qualitative conditions for brand resilience, R22 provides an inequality that practitioners can compute from observational time-series data using VECM error-correction methods (Srinivasan, Pauwels, Hanssens & Dekimpe 2004; Ataman, van Heerde & Mela 2010).

## Files

| File | Description |
|------|-------------|
| `paper.md` | Full manuscript (markdown, v0.3) |
| `paper.yaml` | Machine-readable paper specification |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTORS.yaml` | Contributor attribution |
| `DATA_MANIFEST.yaml` | Data sources and empirical-method anchors |
| `PROVENANCE.yaml` | Drafting history and submission records |

## Status

**Working draft.** Five empirical statistics are marked `[STAT TO BE COMPUTED FROM R10 DATA]` pending R10 re-analysis. Three unverified assumptions stated as explicit limitations: (i) perceptual-series stationarity / cointegration, (ii) orthogonality of "purpose" vs. "product" shocks, (iii) magnitude of the critical threshold (μ − λ residual at which separability collapses).

## Independent convergence

James Kovalenko (X: @deburdened) independently arrived at operator-theoretic framing of organizational and epistemic dynamics with closely related vocabulary (spectral leakage, invariant eigenfunction, verification operator) in a numbered X thread (April 24, 2026). Acknowledged in Discussion.

## Target venue

Marketing Letters (Springer). AMA reference style. Double-anonymous review.

## Relationship to other papers

- **R10 (2026p)** Dove longitudinal case — empirical re-analysis target
- **R12 (2026s)** coherence-resilience — qualitative precursor (R22 formalizes the threshold)
- **R6 (2026j)** diffusion dynamics — flow on cohort weight space
- **R9 (2026o)** non-ergodic perception — absorbing-state dynamics below threshold
- **R16 (2026x)** Brand Function — the invariant being projected onto
- **R19 (2026aa)** rate-distortion — bandwidth grounding
- **R21 (2026ac)** spectral immunity — awareness-gate sufficiency framing
