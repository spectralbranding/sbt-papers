"""
Forming a Perception (2026aw) — companion computation script: ME-DEMO.

A deterministic, fixed-seed calibrated demonstration of the forced Ornstein-Uhlenbeck
model of brand-perception formation/maintenance (paper propositions P1-P4). It is a
CALIBRATED SIMULATION, not a field test: it shows the model computes, recovers the
seeded perception-decay time constant tau from a post-pulse centroid trajectory, and
reproduces the qualitative ordering d tau / d sin^2(beta) > 0 and the maintenance-budget
fall-off. Calibration uses the five canonical PUBLIC brand profiles (NOT a proprietary
atom instrument), so inputs and outputs are fully reproducible.

Model (per-brand, reduced to the off-generic eigen-direction):
    dx = [ -lambda(s) * (x - x_star) + F(t) ] dt + sigma dW
  with relaxation rate lambda(s) = LAMBDA0 * (1 - KAPPA * s) decreasing in the brand's
  distinctiveness s = sin^2(beta) proxy (deeper/better-separated well => slower relaxation),
  so the persistence time tau(s) = 1 / lambda(s) increases in s (P3). A forcing pulse drives
  the centroid to a displacement d0, then forcing stops and the displacement relaxes
  exponentially; tau is RECOVERED by an OLS fit of log-displacement on time (P2). The
  steady-state maintenance forcing to hold a fixed target displacement d_target is
  F_hold = lambda(s) * d_target, which falls with distinctiveness (P4).

Distinctiveness proxy s reuses the 2026av calibration (centered-profile dominant-dimension
energy share of the five canonical anchors) for cross-paper consistency. As in 2026av's ME2,
a Beta population is fitted to the five anchors by method-of-moments and N cohorts are drawn
from it, so the monotone tau-vs-distinctiveness ordering (P3) is demonstrated across a
population with a tight bootstrap interval rather than across only five clustered anchors.

Run:    uv run --with numpy --with matplotlib python research/papers/2026aw/code/forced_relaxation_demo.py
Seed:   20260620 (fixed). Deps: NumPy + Matplotlib only. No network, no credentials.
Outputs: figures/figure1_tau_vs_distinctiveness.png, output/tables/forced_relaxation_results.csv
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

SEED = 20260620

# Five canonical PUBLIC brand profiles (CLAUDE.md; order: Semiotic, Narrative, Ideological,
# Experiential, Social, Economic, Cultural, Temporal).
PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

# Documented illustrative constants (model properties, not fits to response data).
LAMBDA0 = 0.30  # base relaxation rate per week (undifferentiated brand)
KAPPA = 1.05  # distinctiveness sensitivity of the relaxation rate (KAPPA*s < 1)
D0 = 1.0  # post-pulse initial centroid displacement (normalized)
D_TARGET = 1.0  # fixed target displacement for the maintenance-budget comparison
SIGMA = 0.015  # measurement/sampling noise on the observed displacement
WEEKS = 52  # post-pulse observation window
SNR_FLOOR = 8.0  # fit only the high-SNR window (true displacement > SNR_FLOOR*SIGMA)
N_POP = 10000  # cohorts drawn from the calibrated Beta population
N_BOOT = 2000  # bootstrap resamples for the monotonicity CI


def distinctiveness(profile: list[float]) -> float:
    """Centered-profile dominant-dimension energy share (the 2026av sin^2(beta) proxy)."""
    x = np.asarray(profile, dtype=float)
    centered = x - x.mean()
    energy = centered**2
    total = energy.sum()
    return float(energy.max() / total) if total > 0 else 0.0


def beta_mom(samples: np.ndarray) -> tuple[float, float]:
    """Method-of-moments Beta(a, b) fit (as in 2026av ME2)."""
    m = float(samples.mean())
    v = float(samples.var(ddof=1))
    common = m * (1 - m) / v - 1
    return m * common, (1 - m) * common


def recover_tau(s: float, rng: np.random.Generator) -> float:
    """Simulate post-pulse exponential relaxation at rate lambda(s) and recover tau by
    OLS of log-displacement on time over the HIGH-SNR window (P2 estimator). Restricting
    the fit to where the true signal exceeds SNR_FLOOR*SIGMA removes the late-time
    noise-domination bias of a naive full-window log fit."""
    lam = LAMBDA0 * (1.0 - KAPPA * s)
    t = np.arange(WEEKS, dtype=float)
    true_disp = D0 * np.exp(-lam * t)
    disp = true_disp + rng.normal(0.0, SIGMA, size=WEEKS)
    mask = (true_disp > SNR_FLOOR * SIGMA) & (disp > 1e-4)
    if mask.sum() < 3:
        mask = (t < 6) & (disp > 1e-4)  # fallback: earliest weeks
    slope = np.polyfit(t[mask], np.log(disp[mask]), 1)[0]  # slope = -1/tau
    lam_hat = -slope
    return float(1.0 / lam_hat) if lam_hat > 1e-6 else float("inf")


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean()
    rb -= rb.mean()
    denom = np.sqrt((ra**2).sum() * (rb**2).sum())
    return float((ra * rb).sum() / denom) if denom > 0 else 0.0


def main() -> None:
    here = Path(__file__).resolve().parent
    paper = here.parent
    fig_dir = paper / "figures"
    tbl_dir = paper / "output" / "tables"
    fig_dir.mkdir(parents=True, exist_ok=True)
    tbl_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(SEED)

    # --- per-anchor reference rows (marked on the figure) ---
    rows = []
    for name, prof in PROFILES.items():
        s = distinctiveness(prof)
        lam_true = LAMBDA0 * (1.0 - KAPPA * s)
        rows.append(
            dict(
                brand=name,
                distinctiveness=s,
                tau_true=1.0 / lam_true,
                tau_recovered=recover_tau(s, rng),
                maintenance_forcing=lam_true * D_TARGET,
            )
        )
    rows.sort(key=lambda r: r["distinctiveness"])
    anchor_s = np.array([r["distinctiveness"] for r in rows])
    anchor_tau = np.array([r["tau_recovered"] for r in rows])

    # --- calibrated Beta population (the headline ordering statistic) ---
    # Clip draws to the observed anchor distinctiveness range: the demonstration is
    # calibrated to the five public anchors and does NOT extrapolate beyond the most
    # distinctive of them (which would also drive lambda(s)->0, an out-of-calibration
    # singularity). Stated as a calibration-domain limitation in the paper.
    a_hat, b_hat = beta_mom(anchor_s)
    pop_s = np.clip(rng.beta(a_hat, b_hat, size=N_POP), anchor_s.min(), anchor_s.max())
    pop_tau = np.array([recover_tau(s, rng) for s in pop_s])

    rho = spearman(pop_s, pop_tau)
    boot = []
    n = N_POP
    for _ in range(N_BOOT):
        idx = rng.integers(0, n, size=n)
        boot.append(spearman(pop_s[idx], pop_tau[idx]))
    lo, hi = np.percentile(boot, [2.5, 97.5])

    # high- vs low-distinctiveness quartiles
    q1, q3 = np.percentile(pop_s, [25, 75])
    tau_low = pop_tau[pop_s <= q1]
    tau_high = pop_tau[pop_s >= q3]
    tau_ratio = float(tau_high.mean() / tau_low.mean())
    # Cohen's d for tau, high vs low distinctiveness quartile
    sp = np.sqrt(((tau_high.var(ddof=1) + tau_low.var(ddof=1)) / 2))
    cohen_d = float((tau_high.mean() - tau_low.mean()) / sp)
    # maintenance forcing ratio across quartiles (low distinct pays more)
    fhold = LAMBDA0 * (1.0 - KAPPA * pop_s) * D_TARGET
    fhold_ratio = float(fhold[pop_s <= q1].mean() / fhold[pop_s >= q3].mean())

    # ---- results table (anchors) ----
    csv_path = tbl_dir / "forced_relaxation_results.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "brand",
                "distinctiveness_s",
                "tau_true_weeks",
                "tau_recovered_weeks",
                "maintenance_forcing",
            ]
        )
        for r in rows:
            w.writerow(
                [
                    r["brand"],
                    f"{r['distinctiveness']:.3f}",
                    f"{r['tau_true']:.3f}",
                    f"{r['tau_recovered']:.3f}",
                    f"{r['maintenance_forcing']:.4f}",
                ]
            )
    s_arr, tau_arr = anchor_s, anchor_tau

    # ---- figure: tau vs distinctiveness (anchors marked) ----
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    s_grid = np.linspace(pop_s.min(), pop_s.max(), 200)
    tau_grid = 1.0 / (LAMBDA0 * (1.0 - KAPPA * s_grid))
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.scatter(
        pop_s,
        pop_tau,
        s=4,
        color="#9bb7d4",
        alpha=0.25,
        label=f"{N_POP:,} calibrated cohorts",
    )
    ax.plot(
        s_grid,
        tau_grid,
        color="#222222",
        lw=1.6,
        label=r"$\tau(s)=1/[\lambda_0(1-\kappa s)]$",
    )
    ax.scatter(
        s_arr,
        tau_arr,
        s=52,
        color="#c0392b",
        zorder=5,
        edgecolor="white",
        label="5 public anchors",
    )
    for r in rows:
        ax.annotate(
            r["brand"],
            (r["distinctiveness"], r["tau_recovered"]),
            textcoords="offset points",
            xytext=(6, 4),
            fontsize=8,
        )
    ax.set_xlabel(r"cohort distinctiveness  $s=\sin^2\beta$")
    ax.set_ylabel(r"perception-decay time constant  $\tau$ (weeks)")
    ax.set_title(
        "Distinctiveness lower-bounds perceptual persistence (calibrated demonstration)"
    )
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(fig_dir / "figure1_tau_vs_distinctiveness.png", dpi=150)

    # ---- console summary (for the paper's reported values) ----
    print("=== Forming a Perception — ME-DEMO (seed", SEED, ") ===")
    for r in rows:
        print(
            f"  {r['brand']:10s} s={r['distinctiveness']:.3f}  "
            f"tau_recovered={r['tau_recovered']:.2f}w  "
            f"F_hold={r['maintenance_forcing']:.4f}"
        )
    print(f"  Beta population fit: Beta({a_hat:.2f}, {b_hat:.2f}), N={N_POP}")
    print(
        f"  population tau: low-quartile mean {tau_low.mean():.2f}w -> "
        f"high-quartile mean {tau_high.mean():.2f}w"
    )
    print(f"  tau ratio (high/low distinctiveness quartile): {tau_ratio:.2f}x")
    print(f"  Cohen's d (tau, high vs low quartile): {cohen_d:.2f}")
    print(
        f"  maintenance-forcing ratio (low/high distinctiveness quartile): {fhold_ratio:.2f}x"
    )
    print(
        f"  Spearman rho(s, tau_recovered) over population = {rho:.3f}, "
        f"bootstrap 95% CI [{lo:.3f}, {hi:.3f}] (N_BOOT={N_BOOT})"
    )
    print(
        f"  wrote {csv_path.relative_to(paper)} and figures/figure1_tau_vs_distinctiveness.png"
    )


if __name__ == "__main__":
    main()
