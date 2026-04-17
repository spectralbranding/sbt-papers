# Run 17: Cross-Cohort Measurement Invariance Proxy Protocol

**Date**: 2026-04-16
**Paper**: R17 — Brand Triangulation (Zharnikov, 2026y) + PRISM Instrument
**Precedent**: Putnick & Bornstein (2016), Flake & Fried (2020)

---

## Methodology

This experiment uses data from Experiment 1 (Run 15, 800 calls). No additional API calls. Tests whether PRISM-B produces measurement-invariant responses across synthetic cohorts with different behavioral profiles.

---

## Pre-Registered Hypotheses

- **H1**: Configural invariance holds — all cohorts produce 8-factor structures (no dimension merging, no systematically zeroed dimensions)
- **H2**: Metric invariance approximately holds — dimension rank-ordering is consistent within brands across cohorts (Spearman rho > .70 for same-brand profiles across cohorts)
- **H3**: Scalar invariance fails — intercepts differ across cohorts (expected; this is the observer heterogeneity SBT predicts)

---

## Design

- Uses Experiment 1 data: 10 cohorts x 5 brands x 5 models x 3 reps (baseline only)
- No additional API calls

---

## Analysis Plan

1. For each brand: compute 10-cohort x 8-dimension profile matrix
2. Configural test: every cohort produces non-zero weights on all 8 dimensions
3. Metric test: within-brand Spearman correlations across all cohort pairs (45 pairs per brand, 225 total)
4. Scalar test: Kruskal-Wallis per dimension across cohorts
5. Identify dimensions with highest cross-cohort variance

---

## Success Criteria

- H1: zero dimensions systematically zeroed by any cohort
- H2: median within-brand cross-cohort rho > .70
- H3: significant Kruskal-Wallis on at least 4/8 dimensions
