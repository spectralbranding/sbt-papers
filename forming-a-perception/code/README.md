# Companion computation — Forming a Perception (2026aw)

One deterministic, dependency-light script reproduces every reported figure and table value
in the paper's *Calibrated Demonstration*. It is a **calibrated simulation, not a field test**.

## Script

`forced_relaxation_demo.py` — the ME-DEMO of the forced Ornstein-Uhlenbeck model of
perception formation/maintenance.

**Model.** Per brand (reduced to the off-generic eigen-direction), the perception-cloud
centroid follows the forced OU process

```
dx = [ -lambda(s) * (x - x_star) + F(t) ] dt + sigma dW
```

with relaxation rate `lambda(s) = LAMBDA0 * (1 - KAPPA * s)` decreasing in the brand's
distinctiveness `s = sin^2(beta)` (a deeper, better-separated potential well relaxes more
slowly), so the perception-decay time constant `tau(s) = 1 / lambda(s)` increases in `s`
(Proposition 3). A forcing pulse drives the centroid to a displacement; forcing then stops and
the displacement relaxes exponentially. `tau` is **recovered** by an OLS fit of log-displacement
on time over the high-SNR window (Proposition 2). The steady-state maintenance forcing to hold a
target displacement `d` is `F_hold = lambda(s) * d` (Proposition 4).

**Calibration.** Distinctiveness `s` reuses the 2026av calibration: the centered-profile
dominant-dimension energy share of the five canonical PUBLIC brand profiles (Hermes, IKEA,
Patagonia, Erewhon, Tesla — NOT a proprietary atom instrument). A Beta is fitted to the five
anchors by method of moments and `N = 10,000` cohorts are drawn and clipped to the observed
anchor range (no extrapolation beyond the most distinctive anchor, which would also drive
`lambda -> 0`).

**Run**

```
uv run --with numpy --with matplotlib python forced_relaxation_demo.py
```

Fixed seed `20260620`. Deps: NumPy + Matplotlib only. No network, no credentials.

**Outputs**
- `../figures/figure1_tau_vs_distinctiveness.png` — recovered `tau` vs distinctiveness, population + 5 anchors (Figure 1).
- `../output/tables/forced_relaxation_results.csv` — per-anchor distinctiveness, true/recovered `tau`, maintenance forcing.
- Console: Spearman rho(s, tau) with bootstrap CI, the high/low-quartile `tau` ratio and Cohen's d, and the maintenance-forcing ratio (the reported Table 1 values).

**Reported values (seed 20260620):** Spearman `rho = .942` (95% CI [.938, .947]); mean `tau`
5.14 weeks (least-distinct quartile) -> 11.78 weeks (most-distinct quartile), ratio 2.29, Cohen's
d = 3.26; maintenance-forcing ratio 2.17 (low/high distinctiveness quartile). Magnitudes are
model properties under the documented illustrative constants; the robust claim is the monotone
increase of `tau` in distinctiveness.
