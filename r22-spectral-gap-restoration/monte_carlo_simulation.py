"""
Monte Carlo simulation for R22: Spectral Gap Restoration
Tests the mu > lambda threshold inequality for cohort separability survival.

Design parameters motivated by the Dove 2003-2023 illustrative case:
  mu_high  = 4.50  dimension-units/year (Ideological activation rate)
  lambda   = 0.10  dimension-units/year (Cultural passive drift rate)
  mu/lambda = 45 (large-margin threshold satisfaction for Purpose-Aligned cohort)

The sign-inverted Skeptic-Critic regime uses net drift = (mu - lambda) < 0:
  mu_low  = -0.50  (corrective emissions increase leakage for this cohort)
  lambda  =  0.10  (same leakage rate)

Simulation design:
  - 8 cohorts x 4 focal dimensions = 32 cohort-dimension cells per regime
  - 20-year (240-month) horizon, monthly resolution
  - High-mu cells: net = mu_high - lambda > 0 => mean-reverting to equilibrium
    (recoverable basin; spectral gap PRESERVED)
  - Low-mu cells:  net = mu_low  - lambda < 0 => the shock perturbation epsilon
    grows as exp((lambda - mu)*t) => series diverges from equilibrium
    (absorbing basin; spectral gap COLLAPSES)

To make ADF discriminate regimes we simulate:
  - HIGH regime: Ornstein-Uhlenbeck around a stable equilibrium (stationary)
  - LOW  regime: random walk with negative drift on the gap metric
    (the SPECTRAL GAP collapses toward zero; the gap metric is non-stationary)
"""

import json
import numpy as np
from scipy import stats
from statsmodels.tsa.stattools import adfuller

# ──────────────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────────────
RNG_SEED    = 2026
N_COHORTS   = 8
N_DIMS      = 4           # 4 focal dimensions => 32 cohort-dimension cells
N_MONTHS    = 240         # 20-year horizon
DT          = 1 / 12     # monthly step (years)

MU_HIGH     =  4.50       # corrective emission rate - high regime
MU_LOW      = -0.50       # effective mu - low (sign-inverted Skeptic-Critic)
LAMBDA      =  0.10       # spectral leakage rate (identical across regimes)

NOISE_STD   =  0.12       # OU noise magnitude

ADF_ALPHA   =  0.05       # ADF significance level


# ──────────────────────────────────────────────────────────────────────────────
# Simulate a single cohort-dimension PERCEPTION score (the raw 8-pt scale value)
# ──────────────────────────────────────────────────────────────────────────────
def simulate_perception_score(mu: float, lam: float, n_months: int,
                               noise_std: float, rng: np.random.Generator,
                               x0: float = 5.0) -> np.ndarray:
    """
    OU process: dx = theta*(x_eq - x)*dt + sigma*dW
    theta = |mu - lam|  (reversion speed)
    x_eq  = target equilibrium (8.0 for mu>0, 1.0 for mu<0)
    """
    net   = mu - lam
    theta = abs(net)                      # reversion speed
    x_eq  = 8.0 if mu > 0 else 1.0       # equilibrium
    sign  = np.sign(net) if net != 0 else 1.0

    x = np.zeros(n_months)
    x[0] = x0
    for t in range(1, n_months):
        drift = sign * theta * (x_eq - x[t - 1]) * DT
        shock = noise_std * rng.standard_normal() * np.sqrt(DT)
        x[t]  = np.clip(x[t - 1] + drift + shock, 0.1, 9.9)
    return x


# ──────────────────────────────────────────────────────────────────────────────
# Simulate the SPECTRAL GAP PROCESS directly (the key diagnostic metric)
#
# HIGH regime: gap follows OU that reverts to gap_eq > 0  (gap preserved)
# LOW  regime: gap decays as epsilon grows => gap = gap0 * exp(-(net_leak)*t)
#   net_leak = lambda - mu > 0 in the low regime
#   We add noise; the gap trajectory is non-stationary (trending toward zero)
# ──────────────────────────────────────────────────────────────────────────────
def simulate_spectral_gap(mu: float, lam: float, n_months: int,
                           noise_std: float, rng: np.random.Generator,
                           gap0: float = 1.0) -> np.ndarray:
    """
    Spectral gap time series.
    HIGH regime: mean-reverting OU around gap_eq > 0.
    LOW  regime: decaying exponential process trending to zero.
    """
    net_corr = mu - lam   # positive -> gap preserved; negative -> gap collapses

    gap = np.zeros(n_months)
    gap[0] = gap0

    if net_corr > 0:
        # HIGH: OU around gap_eq (positive equilibrium)
        gap_eq = gap0 * (net_corr / (net_corr + lam))  # steady-state fraction
        gap_eq = max(gap_eq, 0.3)  # floor for numerical stability
        theta  = net_corr
        for t in range(1, n_months):
            drift = theta * (gap_eq - gap[t - 1]) * DT
            shock = noise_std * 0.3 * rng.standard_normal() * np.sqrt(DT)
            gap[t] = max(gap[t - 1] + drift + shock, 0.05)
    else:
        # LOW: gap shrinks as epsilon grows; add noise
        net_leak = lam - mu   # positive (leakage dominates)
        for t in range(1, n_months):
            decay = -net_leak * gap[t - 1] * DT
            shock = noise_std * 0.3 * rng.standard_normal() * np.sqrt(DT)
            gap[t] = max(gap[t - 1] + decay + shock, 0.001)
    return gap


# ──────────────────────────────────────────────────────────────────────────────
# IRF half-life from local AR(1) linearisation
# ──────────────────────────────────────────────────────────────────────────────
def irf_halflife(series: np.ndarray) -> float:
    if len(series) < 10:
        return np.nan
    result = stats.linregress(series[:-1], series[1:])
    rho = result.slope
    if abs(rho) >= 1.0:
        return np.inf
    if abs(rho) < 1e-10:
        return 0.0
    return np.log(0.5) / np.log(abs(rho))


# ──────────────────────────────────────────────────────────────────────────────
# Main simulation
# ──────────────────────────────────────────────────────────────────────────────
def run_simulation() -> dict:
    rng = np.random.default_rng(RNG_SEED)
    total_cells = N_COHORTS * N_DIMS

    # Storage
    adf_pvals_high, adf_pvals_low   = [], []
    halflives_high, halflives_low   = [], []
    gap_final_high, gap_final_low   = [], []
    cosine_drift_high, cosine_drift_low = [], []

    for cohort in range(N_COHORTS):
        # Simulate 8 dimensional scores for cosine distance calculation
        scores_high = np.stack([
            simulate_perception_score(MU_HIGH, LAMBDA, N_MONTHS, NOISE_STD,
                                      rng, x0=rng.uniform(3.0, 7.0))
            for _ in range(8)
        ], axis=1)  # (N_MONTHS, 8)

        scores_low = np.stack([
            simulate_perception_score(MU_LOW, LAMBDA, N_MONTHS, NOISE_STD,
                                      rng, x0=rng.uniform(3.0, 7.0))
            for _ in range(8)
        ], axis=1)

        # Cosine distance from initial centroid
        def cosine_drift(mat):
            v0 = mat[0]; n0 = np.linalg.norm(v0) + 1e-9
            drifts = []
            for vt in mat:
                nt = np.linalg.norm(vt) + 1e-9
                drifts.append(1.0 - np.dot(v0, vt) / (n0 * nt))
            return float(np.mean(drifts))

        cosine_drift_high.append(cosine_drift(scores_high))
        cosine_drift_low.append(cosine_drift(scores_low))

        # Per focal-dimension: spectral gap series -> ADF + half-life
        for dim in range(N_DIMS):
            gap0 = rng.uniform(0.8, 1.4)

            # HIGH regime
            sg_h = simulate_spectral_gap(MU_HIGH, LAMBDA, N_MONTHS, NOISE_STD, rng, gap0)
            gap_final_high.append(float(sg_h[-1]))
            try:
                _, p_h, *_ = adfuller(sg_h, autolag='AIC')
            except Exception:
                p_h = np.nan
            adf_pvals_high.append(float(p_h) if not np.isnan(p_h) else None)
            hl_h = irf_halflife(sg_h)
            halflives_high.append(float(hl_h) if np.isfinite(hl_h) else None)

            # LOW regime
            sg_l = simulate_spectral_gap(MU_LOW, LAMBDA, N_MONTHS, NOISE_STD, rng, gap0)
            gap_final_low.append(float(sg_l[-1]))
            try:
                _, p_l, *_ = adfuller(sg_l, autolag='AIC')
            except Exception:
                p_l = np.nan
            adf_pvals_low.append(float(p_l) if not np.isnan(p_l) else None)
            hl_l = irf_halflife(sg_l)
            halflives_low.append(float(hl_l) if np.isfinite(hl_l) else None)

    # ── Aggregate ─────────────────────────────────────────────────────────
    # Stationary = ADF rejects unit root (p < ADF_ALPHA)
    n_stat_high = sum(1 for p in adf_pvals_high if p is not None and p < ADF_ALPHA)
    n_stat_low  = sum(1 for p in adf_pvals_low  if p is not None and p < ADF_ALPHA)
    prop_stat_h = n_stat_high / total_cells
    prop_stat_l = n_stat_low  / total_cells

    valid_hl_h  = [h for h in halflives_high if h is not None and h < 10000]
    valid_hl_l  = [h for h in halflives_low  if h is not None and h < 10000]
    mean_hl_h   = float(np.mean(valid_hl_h)) if valid_hl_h else None
    mean_hl_l   = float(np.mean(valid_hl_l)) if valid_hl_l else None

    mean_cd_h   = float(np.mean(cosine_drift_high))
    mean_cd_l   = float(np.mean(cosine_drift_low))
    mean_gf_h   = float(np.mean(gap_final_high))
    mean_gf_l   = float(np.mean(gap_final_low))

    # Proportion test (one-sided z-test)
    pooled      = (n_stat_high + n_stat_low) / (2 * total_cells)
    se_pool     = np.sqrt(pooled * (1 - pooled) * 2 / total_cells)
    z_stat      = (prop_stat_h - prop_stat_l) / (se_pool + 1e-12)
    z_pval      = float(1 - stats.norm.cdf(z_stat))

    # ── Lead-time estimate ─────────────────────────────────────────────────
    # In the LOW regime, the spectral gap first falls below 10% of its initial
    # value at some month T_gap_collapse. We then compare T_gap_collapse to the
    # conviction reorientation onset (treated as month 12 in our design parameters,
    # matching Effie 2006's ~12-month post-launch timing).
    # We measure the AVERAGE T_gap_collapse across all LOW-regime cells.
    collapse_months = []
    rng2 = np.random.default_rng(RNG_SEED)
    for cohort in range(N_COHORTS):
        for dim in range(N_DIMS):
            gap0 = rng2.uniform(0.8, 1.4) if cohort * N_DIMS + dim > 0 else 1.0
            sg = simulate_spectral_gap(MU_LOW, LAMBDA, N_MONTHS, NOISE_STD, rng2, gap0)
            threshold = 0.10 * sg[0]
            below = np.where(sg < threshold)[0]
            if len(below) > 0:
                collapse_months.append(int(below[0]))
    mean_collapse_month = float(np.mean(collapse_months)) if collapse_months else None

    # ── Compile results ────────────────────────────────────────────────────
    results = {
        "design_parameters": {
            "n_cohorts": N_COHORTS,
            "n_dims_per_cohort": N_DIMS,
            "n_cells_total": total_cells,
            "n_months": N_MONTHS,
            "years": N_MONTHS // 12,
            "mu_high": MU_HIGH,
            "mu_low": MU_LOW,
            "lambda": LAMBDA,
            "mu_lambda_ratio_high_regime": round(MU_HIGH / LAMBDA, 1),
            "net_drift_high": round(MU_HIGH - LAMBDA, 2),
            "net_drift_low":  round(MU_LOW  - LAMBDA, 2),
            "noise_std": NOISE_STD,
            "rng_seed": RNG_SEED,
            "description": (
                "Spectral gap time series simulated for 8 cohorts x 4 focal dimensions = "
                "32 cohort-dimension cells per regime (240 months / 20 years). "
                "HIGH regime: OU mean-reversion toward preserved gap equilibrium. "
                "LOW regime: exponential decay toward gap=0 (absorbing collapse)."
            ),
        },
        "high_regime": {
            "label": "mu > lambda (threshold satisfied; Dove Purpose-Aligned design params)",
            "mu": MU_HIGH,
            "lambda": LAMBDA,
            "n_cells": total_cells,
            "proportion_stationary_adf": round(prop_stat_h, 3),
            "n_stationary_adf": n_stat_high,
            "mean_irf_halflife_months": round(mean_hl_h, 2) if mean_hl_h else None,
            "mean_cosine_drift_from_initial": round(mean_cd_h, 4),
            "mean_terminal_spectral_gap": round(mean_gf_h, 4),
            "adf_pvals_all_cells": [round(p, 4) if p is not None else None for p in adf_pvals_high],
            "irf_halflives_all_cells": [round(h, 2) if h is not None else None for h in halflives_high],
        },
        "low_regime": {
            "label": "mu < lambda (threshold violated; Dove Skeptic-Critic sign-inversion)",
            "mu": MU_LOW,
            "lambda": LAMBDA,
            "n_cells": total_cells,
            "proportion_stationary_adf": round(prop_stat_l, 3),
            "n_stationary_adf": n_stat_low,
            "mean_irf_halflife_months": round(mean_hl_l, 2) if mean_hl_l else None,
            "mean_cosine_drift_from_initial": round(mean_cd_l, 4),
            "mean_terminal_spectral_gap": round(mean_gf_l, 4),
            "mean_gap_collapse_month": round(mean_collapse_month, 1) if mean_collapse_month else None,
            "adf_pvals_all_cells": [round(p, 4) if p is not None else None for p in adf_pvals_low],
            "irf_halflives_all_cells": [round(h, 2) if h is not None else None for h in halflives_low],
        },
        "regime_comparison": {
            "prop_stationary_high": round(prop_stat_h, 3),
            "prop_stationary_low": round(prop_stat_l, 3),
            "difference": round(prop_stat_h - prop_stat_l, 3),
            "z_statistic": round(z_stat, 3),
            "p_value_one_sided": round(z_pval, 4),
            "mean_cosine_drift_high": round(mean_cd_h, 4),
            "mean_cosine_drift_low": round(mean_cd_l, 4),
            "cosine_drift_ratio_low_over_high": round(mean_cd_l / (mean_cd_h + 1e-9), 2),
            "mean_terminal_spectral_gap_high": round(mean_gf_h, 4),
            "mean_terminal_spectral_gap_low": round(mean_gf_l, 4),
            "terminal_gap_ratio_high_over_low": round(mean_gf_h / (mean_gf_l + 1e-9), 2),
            "mean_irf_halflife_high_months": round(mean_hl_h, 2) if mean_hl_h else None,
            "mean_irf_halflife_low_months": round(mean_hl_l, 2) if mean_hl_l else None,
            "mean_gap_collapse_month_low_regime": (
                round(mean_collapse_month, 1) if mean_collapse_month else None
            ),
            "interpretation": (
                "High-mu regime: spectral-gap series are STATIONARY (gap preserved). "
                "Low-mu regime: spectral-gap series are NON-STATIONARY (gap collapses). "
                "Terminal spectral gap ratio confirms preservation in high regime vs "
                "collapse in low regime, consistent with the mu > lambda threshold."
                if prop_stat_h > prop_stat_l
                else "Regimes did not separate on ADF stationarity alone; "
                     "see terminal spectral gap values for regime contrast."
            ),
        },
    }
    return results


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Running Monte Carlo simulation for R22 (Spectral Gap Restoration)...")
    results = run_simulation()

    out_path = "/Users/d/projects/sbt-papers/r22-spectral-gap-restoration/monte_carlo_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {out_path}")
    rc = results["regime_comparison"]
    hr = results["high_regime"]
    lr = results["low_regime"]
    print("\n── Regime comparison ─────────────────────────────────────────────────")
    print(f"  Prop. stationary ADF (high-mu):     {rc['prop_stationary_high']:.3f}  "
          f"({hr['n_stationary_adf']}/{hr['n_cells']} cells)")
    print(f"  Prop. stationary ADF (low-mu):      {rc['prop_stationary_low']:.3f}  "
          f"({lr['n_stationary_adf']}/{lr['n_cells']} cells)")
    print(f"  Difference:                         {rc['difference']:+.3f}")
    print(f"  z = {rc['z_statistic']:.3f},  p (one-sided) = {rc['p_value_one_sided']:.4f}")
    print(f"  Mean terminal spectral gap HIGH:    {rc['mean_terminal_spectral_gap_high']:.4f}")
    print(f"  Mean terminal spectral gap LOW:     {rc['mean_terminal_spectral_gap_low']:.4f}")
    print(f"  Terminal gap ratio (high/low):      {rc['terminal_gap_ratio_high_over_low']:.1f}x")
    print(f"  Mean cosine drift HIGH:             {rc['mean_cosine_drift_high']:.4f}")
    print(f"  Mean cosine drift LOW:              {rc['mean_cosine_drift_low']:.4f}")
    print(f"  Mean IRF half-life HIGH:            {hr['mean_irf_halflife_months']} months")
    print(f"  Mean IRF half-life LOW:             {lr['mean_irf_halflife_months']} months")
    if lr.get('mean_gap_collapse_month') is not None:
        print(f"  Mean spectral gap collapse month:   {lr['mean_gap_collapse_month']:.1f}  "
              f"(conviction onset assumed month 12)")
        lag = 12 - lr['mean_gap_collapse_month']
        print(f"  Gap precedes conviction by:         {lag:.1f} months")
    print(f"\n  {rc['interpretation']}")
