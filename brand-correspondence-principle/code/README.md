# Companion computation script — 2026au (The Correspondence Principle of Brand Management)

`correspondence_loss_surface.py` reproduces the numerical illustration of the paper
(finding F1 in `../SPINE.yaml`): the expected managerial **decision-loss gap** of
score-based management relative to cloud-based management as a function of the four
regime-departure parameters.

## Run

```
cd [internal path removed]
uv run --with numpy python [internal path removed]
```

Deterministic given the fixed seed `SEED = 20260619`. No network, no credentials.
`N = 20000` observers (Monte Carlo draws) per parameter combination — above the
≥ 5,000 floor — reported with Monte Carlo standard errors.

## What it computes

The brand is the observer-completed measure on the perception manifold S⁷ (the eight
SBT dimensions), modeled as a von Mises–Fisher mixture. The managerial decision is a
quadratic-tracking problem; the **cloud** experiment observes the full perception
vector and acts per observer (residual loss zero); the **score** experiment observes
only the scalar incumbent brand-health index s = ⟨u, θ⟩ and acts on its best linear
decode. The reported GAP = score-loss − cloud-loss is exactly the Blackwell dominance
gap for this decision and is ≥ 0 for every experiment by Blackwell–Sherman–Stein.

Each regime-departure parameter injects off-incumbent-axis perceptual variance:
σ (dispersion/multimodality), v (temporal velocity, observer-specific drift),
α (a dimension-collapsed AI-observer von Mises–Fisher component, calibrated to the R15
AI-search-metamerism cohort divergence), ε (an exogenous near-uniform component the
firm signal does not control).

## Expected output (seed 20260619)

- **Classical corner** (all parameters 0): gap ≈ .023 — near zero, the correspondence
  theorem's reduction limit.
- **Monotone** non-decreasing in each of σ, v, α, ε (ε steepest, reaching ≈ .79).
- **Payoff-form robust**: quadratic ≈ linear (orthogonality principle), threshold
  smaller in scale but still monotone.
- **Dimension count**: d = 2 (the appendix toy) < d = 8, both monotone.
- **Best-possible scalar** (top principal eigenvector) leaves a positive, growing gap —
  the gap is not an artifact of a badly chosen incumbent index.

## Calibration anchor

`AI_COLLAPSE_KAPPA` and `AI_MEAN_OFFAXIS_FRAC` set the AI cohort's concentration and
off-axis mean tilt to the scale of the human-vs-AI perception divergence in the R15
AI-search-metamerism corpus (HuggingFace `zharnikov-2026-hf-r15-ai-search-metamerism`),
so the α surface is anchored to a real dataset rather than purely synthetic draws.
