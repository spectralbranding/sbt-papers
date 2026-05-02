# Companion Computation Scripts — R22 Spectral Gap Restoration

All scripts require Python 3.12+ and `uv`.

## Scripts

### monte_carlo_simulation.py

Produces Table 1 (Monte Carlo Regime Contrast) and the Companion Computation Script numerics cited in the Numerical Illustration section.

**Run command:**
```
uv run --with statsmodels --with numpy --with scipy python3 ../monte_carlo_simulation.py
```

Seed: 2026. Outputs: `monte_carlo_results.json`.

---

### plot_bifurcation_curve.py

Produces Figure 2 (Bifurcation diagram of spectral gap vs mu/lambda ratio).

**Run command:**
```
uv run python plot_bifurcation_curve.py
```

Seed: 42. Outputs: `../figures/figure2_bifurcation.png` (300 dpi).

**What it does:** For 50 values of mu/lambda in [0.5, 2.0], simulates N=2000 discrete-time OU sample paths with lambda=0.1 fixed, mu = ratio * lambda. Tracks mean terminal spectral gap at t=100. The bifurcation at ratio=1.0 (mu=lambda) confirms the threshold is a sharp demarcation rather than a smooth gradient.
