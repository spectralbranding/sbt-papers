"""
Monte Carlo companion script for Zharnikov (2026s) "Coherence Type as Crisis Predictor."

Simulates the Wright-Fisher SDE specified in section 2.1 for the five canonical
SBT-8 brands (Hermes, IKEA, Patagonia, Erewhon, Tesla), applies a perturbation
of varying magnitude to a single dimension, and measures recovery time and
absorption frequency. Verifies the qualitative orderings asserted in
Theorems 1, 2, and 3.

SDE per dimension i (per section 2.1, Wright-Fisher-type linear drift modulator
h(x_i) = x_i; Wright-Fisher diffusion coefficient sqrt(x_i (1 - x_i))):

  dx_i = [gamma * s_i * x_i - delta * (x_i - x_i^*)] * dt
         + sigma_0 * sqrt(x_i * (1 - x_i)) * dW_i

with absorbing boundary at x_i = 0. Discretized via Euler-Maruyama with a
reflecting upper boundary at x_i = 1 to keep the diffusion coefficient real.

Run:

  uv run python code/coherence_resilience_mc.py

No arguments. Outputs:

  data/results.json      -- per-brand per-dimension recovery statistics
  data/run.log           -- timestamped log of the run

Fixed seed (1729). No external API calls. Deterministic given the seed.
"""

from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path

# ----- canonical inputs ------------------------------------------------------

# Order: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal
DIMENSIONS = (
    "Semiotic", "Narrative", "Ideological", "Experiential",
    "Social", "Economic", "Cultural", "Temporal",
)

PROFILES: dict[str, tuple[float, ...]] = {
    "Hermes":    (9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5),
    "IKEA":      (8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0),
    "Patagonia": (6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5),
    "Erewhon":   (7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5),
    "Tesla":     (7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0),
}

# ----- SDE parameters (illustrative; per section 5.3 working ranges) --------

GAMMA = 0.020       # signal-driven coupling (per month, normalized)
DELTA = 0.050       # decay rate toward neutral prior (per month, ~14-month half-life)
SIGMA0 = 0.080      # diffusion scale (within-month perception SD)
DT = 0.25           # 1/4 month per step
T_HORIZON = 60.0    # 60 months (5 years) post-shock
N_PATHS = 2000      # paths per (brand, dimension, severity) cell
SEED = 1729

X_NEUTRAL = 1.0 / math.sqrt(8.0)   # ~0.3536 -- neutral prior on each axis

# Pre-shock equilibrium: each dimension sits near a brand- and dimension-specific
# fixed point determined by gamma * s_i. We pre-burn each path to a stationary
# distribution before shocking; for tractability we approximate the pre-shock
# location as the deterministic fixed point of the drift equation:
#     gamma * s_i * x = delta * (x - x*)
# i.e., x* = x_neutral * delta / (delta - gamma * s_i) when gamma * s_i < delta,
# else the dynamics drive x_i upward without an interior equilibrium and the
# attractor is the reflecting boundary x_i = 1. Solved numerically below.

SEVERITIES = (0.05, 0.10, 0.15, 0.20)   # absolute drop applied to chosen dim


def deterministic_equilibrium(s_i: float, x_star: float = X_NEUTRAL,
                              gamma: float = GAMMA, delta: float = DELTA) -> float:
    """Find x in (0, 1) solving gamma * s_i * x = delta * (x - x*).

    Closed form: x = delta * x_star / (delta - gamma * s_i), valid when
    gamma * s_i < delta. Otherwise the linear drift gamma * s_i * x exceeds
    the decay restoring force on every x in (x_star, 1), and the attractor
    is the reflecting upper boundary at x_i = 1; we cap the equilibrium at
    0.999 to keep the burn-in numerically well-behaved.
    """
    if gamma * s_i >= delta:
        return 0.999
    return delta * x_star / (delta - gamma * s_i)


def step(x: float, s_i: float, rng: random.Random,
         dt: float = DT, gamma: float = GAMMA, delta: float = DELTA,
         sigma0: float = SIGMA0, x_star: float = X_NEUTRAL) -> float:
    """Single Euler-Maruyama step for one dimension. Absorbing at 0, reflecting at 1."""
    if x <= 0.0:
        return 0.0
    # Drift modulator h(x_i) = x_i (Wright-Fisher-type linear; section 2.1)
    # Diffusion coefficient sigma_i(x) = sigma_0 * sqrt(x_i (1 - x_i)) (Wright-Fisher)
    drift = gamma * s_i * x - delta * (x - x_star)
    diffusion = sigma0 * math.sqrt(max(x * (1.0 - x), 0.0))
    # Box-Muller via random module (gauss handles it)
    dw = rng.gauss(0.0, math.sqrt(dt))
    new_x = x + drift * dt + diffusion * dw
    if new_x <= 0.0:
        return 0.0
    if new_x >= 1.0:
        return 1.0 - (new_x - 1.0)   # reflect
    return new_x


def simulate_recovery(brand: str, dim_idx: int, severity: float,
                      rng: random.Random, n_paths: int = N_PATHS,
                      t_horizon: float = T_HORIZON) -> dict:
    """Apply shock at t=0; track absorption + recovery.

    Recovery defined as x_i returning to within 90% of its pre-shock equilibrium.
    """
    profile = PROFILES[brand]
    s_i = profile[dim_idx]
    x_eq = deterministic_equilibrium(s_i)
    x_post_shock = max(x_eq - severity, 0.0)
    recovery_threshold = 0.90 * x_eq

    n_steps = int(t_horizon / DT)
    absorbed = 0
    recovery_times: list[float] = []

    for _ in range(n_paths):
        x = x_post_shock
        recovered_at: float | None = None
        for step_idx in range(n_steps):
            x = step(x, s_i, rng)
            t_now = (step_idx + 1) * DT
            if x <= 0.0:
                absorbed += 1
                break
            if recovered_at is None and x >= recovery_threshold:
                recovered_at = t_now
                # continue running to allow possible later absorption
        if recovered_at is not None and x > 0.0:
            recovery_times.append(recovered_at)

    n = len(recovery_times)
    p_abs = absorbed / n_paths
    p_rec = n / n_paths
    if n > 0:
        mean_t = sum(recovery_times) / n
        # sample standard deviation
        if n > 1:
            mean_sq = sum(t * t for t in recovery_times) / n
            var = max(mean_sq - mean_t * mean_t, 0.0) * n / (n - 1)
            sd_t = math.sqrt(var)
        else:
            sd_t = 0.0
        median_t = sorted(recovery_times)[n // 2]
    else:
        mean_t = float("nan")
        sd_t = float("nan")
        median_t = float("nan")

    return {
        "brand": brand,
        "dimension": DIMENSIONS[dim_idx],
        "s_i": s_i,
        "severity": severity,
        "x_equilibrium": round(x_eq, 4),
        "x_post_shock": round(x_post_shock, 4),
        "n_paths": n_paths,
        "P_absorption": round(p_abs, 4),
        "P_recovery": round(p_rec, 4),
        "recovery_time_mean_months": round(mean_t, 3) if not math.isnan(mean_t) else None,
        "recovery_time_sd_months": round(sd_t, 3) if not math.isnan(sd_t) else None,
        "recovery_time_median_months": round(median_t, 3) if not math.isnan(median_t) else None,
    }


def main() -> None:
    rng = random.Random(SEED)
    here = Path(__file__).resolve().parent
    data_dir = here / "data"
    data_dir.mkdir(exist_ok=True)
    log_path = data_dir / "run.log"
    out_path = data_dir / "results.json"

    log_lines: list[str] = []
    def log(msg: str) -> None:
        stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        line = f"[{stamp}] {msg}"
        print(line)
        log_lines.append(line)

    log(f"R12 coherence-resilience MC: seed={SEED}, n_paths={N_PATHS}, T={T_HORIZON} months")
    log(f"Parameters: gamma={GAMMA}, delta={DELTA}, sigma0={SIGMA0}, dt={DT}")

    results: list[dict] = []
    # Each brand: probe its WEAKEST dimension (per-brand worst case) at several severities
    # and probe its STRONGEST dimension as a contrast.
    for brand, profile in PROFILES.items():
        weakest_idx = profile.index(min(profile))
        strongest_idx = profile.index(max(profile))
        log(f"{brand}: weakest dim = {DIMENSIONS[weakest_idx]} (s={profile[weakest_idx]}); "
            f"strongest dim = {DIMENSIONS[strongest_idx]} (s={profile[strongest_idx]})")
        for severity in SEVERITIES:
            r_weak = simulate_recovery(brand, weakest_idx, severity, rng)
            r_strong = simulate_recovery(brand, strongest_idx, severity, rng)
            results.append(r_weak)
            results.append(r_strong)
            log(f"  severity={severity:.2f}  weak: P_abs={r_weak['P_absorption']:.3f}, "
                f"P_rec={r_weak['P_recovery']:.3f}  strong: P_abs={r_strong['P_absorption']:.3f}, "
                f"P_rec={r_strong['P_recovery']:.3f}")

    # Summary: rank brands by mean P_absorption on their weakest dim at severity=0.15
    log("\nSummary: brand ranking by P_absorption on weakest dimension (severity=0.15)")
    ranking = []
    for r in results:
        if r["severity"] == 0.15:
            # only weakest-dim entries (where the brand's worst dim was probed)
            if r["s_i"] == min(PROFILES[r["brand"]]):
                ranking.append((r["brand"], r["P_absorption"], r["P_recovery"],
                                r["recovery_time_median_months"]))
    ranking.sort(key=lambda t: t[1])
    for brand, p_abs, p_rec, t_med in ranking:
        log(f"  {brand:<10}  P_abs={p_abs:.3f}  P_rec={p_rec:.3f}  median tau_rec={t_med}")

    out = {
        "metadata": {
            "seed": SEED,
            "n_paths_per_cell": N_PATHS,
            "t_horizon_months": T_HORIZON,
            "dt_months": DT,
            "gamma": GAMMA,
            "delta": DELTA,
            "sigma0": SIGMA0,
            "x_neutral_prior": round(X_NEUTRAL, 6),
            "severities": list(SEVERITIES),
            "n_brands": len(PROFILES),
        },
        "results": results,
        "ranking_at_severity_0_15": [
            {"brand": b, "P_absorption": pa, "P_recovery": pr, "median_tau_rec_months": tm}
            for b, pa, pr, tm in ranking
        ],
    }
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    log(f"Wrote {out_path}")
    log_path.write_text("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
