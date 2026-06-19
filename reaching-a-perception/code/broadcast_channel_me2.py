"""ME2: calibrated broadcast-channel simulation + two case studies (2026av).

This is the Empirical-Strategy *fallback* of "Reaching a Perception" (the path
taken when a field partnership for the primary two-cell experiment is
infeasible). It does three things, all deterministic and reproducible from a
fixed seed:

  1. CALIBRATE a cohort-distinctiveness distribution to an OBSERVED public proxy
     -- the five canonical SBT brand profiles (Hermes, IKEA, Patagonia, Erewhon,
     Tesla), the public anchors used throughout the corpus -- NOT the work-in-
     progress atom-based instrument. Distinctiveness for a SINGLE-dimension
     broadcast is the concentration of the *centered* profile on its dominant
     dimension: s = max_k (v_k - mean(v))^2 / sum_k (v_k - mean(v))^2, which
     removes the common "halo" level (every brand scores positive on every
     dimension) and measures how much of a cohort's off-generic sensitivity is
     focused on one broadcastable axis. s in [1/8, 1].

  2. Run the paper's MINIMAL two-type broadcast-channel model (Cover 1972) as a
     Monte Carlo over cohorts drawn from the calibrated distribution, and report
     the resonance over-index of a dimension-strong creative versus a
     dimension-neutral control on the matched cohort, with an effect size
     (Cohen's d) and bootstrap 95% confidence intervals.

  3. Instantiate the measurement-to-activation HANDOFF CONTRACT on TWO case
     studies -- a maintenance campaign (an established, distinctive brand) and a
     category-creation campaign (an undifferentiated new entrant) -- and report,
     for each, which of the three bridges the contract recommends and at what
     cost. The two cases demonstrate bridge SELECTION (the reaching decision),
     not perception formation, which is deferred to the spectral-dynamics
     companion (2026z).

Minimal model (faithful to the paper's "A Minimal Broadcast-Channel Model").
Two observer types whose sensitivity vectors are separated by angle beta with
sin^2(beta) = s. Place the matched type on axis 1, w_match = (1, 0); the
off-target type at w_off = (cos beta, sin beta). A dimension-strong creative
emits x_strong = (1, 0); a dimension-neutral control emits x_neutral =
(1/sqrt2, 1/sqrt2) (equal energy spread). An observer's channel quality is the
absolute inner product q = |x . w| (the degraded-broadcast-channel reading), and
salience is monotone in q via a logistic link, sal(q) = 1 / (1 + exp(-KAPPA (q -
Q0))). The matched type receives the strong creative at q = 1 regardless of s;
the off-target type receives it at q = cos beta = sqrt(1 - s), which FALLS as s
rises -- that is the self-selection sharpening. The resonance over-index is the
matched-type salience relative to the off-target salience for the strong
creative, and the per-impression spill is the off-target salience (impressions
paid on a non-resonant receiver).

Calibration constants (documented; illustrative, not fit to live response data):
    KAPPA, Q0  logistic reception steepness / midpoint
    L0         minimal-loss-proxy decision loss L(P*) (matches Figure 1)
    C_REF      representative per-impression spill cost (matches Figure 1)
The routing threshold s* = 1 - L0 / C_REF = .355 is inherited from Figure 1, so
the simulation and the loss surface are calibrated consistently.

Run:
    uv run python code/broadcast_channel_me2.py
Outputs (deterministic, seed=20260619):
    figures/figure2_me2_overindex.png
    output/tables/me2_results.csv
    prints the calibration summary, Monte-Carlo effect sizes + CIs, and the two
    case-study contract recommendations.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEED = 20260619

# Canonical public brand profiles (CLAUDE.md; the corpus's public anchors).
# Dimension order: Semiotic, Narrative, Ideological, Experiential, Social,
# Economic, Cultural, Temporal.
PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

# --- documented reception + cost constants (illustrative, not fit to data) ---
KAPPA = 6.0  # logistic reception steepness
Q0 = 0.45  # logistic reception midpoint (channel-quality units)
L0 = 0.20  # minimal-loss-proxy decision loss L(P*) (Figure 1)
C_REF = 0.31  # representative per-impression spill cost (Figure 1)
N_COHORTS = 10_000
N_BOOT = 2_000


def distinctiveness(profile) -> float:
    """Single-dimension distinctiveness s of a profile: concentration of the
    centered profile on its dominant dimension. s in [1/8, 1]."""
    v = np.asarray(profile, float)
    vc = v - v.mean()
    ss = float((vc**2).sum())
    if ss == 0.0:
        return 1.0 / len(v)
    return float((vc**2).max() / ss)


def fit_beta(samples):
    """Method-of-moments Beta(a, b) for samples in (0, 1)."""
    x = np.asarray(samples, float)
    m, v = x.mean(), x.var(ddof=1)
    common = m * (1 - m) / v - 1
    a = m * common
    b = (1 - m) * common
    return float(a), float(b)


def salience(q):
    """Logistic reception: salience monotone in channel quality q."""
    return 1.0 / (1.0 + np.exp(-KAPPA * (np.asarray(q, float) - Q0)))


def over_index(s):
    """Resonance over-index of the dimension-strong creative vs the neutral
    control on the matched cohort, given distinctiveness s = sin^2(beta).

    Returned as the matched-type salience for the strong creative divided by the
    OFF-target-type salience for the same creative: how much more the strong
    creative reaches the cohort it is tuned to than the cohort it is not."""
    cos_beta = np.sqrt(np.clip(1.0 - s, 0.0, 1.0))
    q_match = 1.0  # x_strong . w_match = (1,0).(1,0)
    q_off = cos_beta  # x_strong . w_off  = (1,0).(cosb,sinb)
    sal_match = salience(q_match)
    sal_off = salience(q_off)
    return sal_match / sal_off, sal_match, sal_off


def neutral_match_salience():
    """Matched-type salience for the dimension-NEUTRAL control (q = 1/sqrt2)."""
    return float(salience(1.0 / np.sqrt(2.0)))


def cohens_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    return float((a.mean() - b.mean()) / sp)


def ci95(values):
    lo, hi = np.percentile(values, [2.5, 97.5])
    return float(lo), float(hi)


def recommend_bridge(s, c=C_REF, l0=L0):
    """Handoff-contract bridge recommendation for distinctiveness s.
    Returns (bridge, cost, rationale)."""
    spill = c * (1.0 - s)
    s_star = 1.0 - l0 / c
    if s >= s_star and spill <= l0:
        return (
            "broadcast-a-dimension",
            spill,
            f"s={s:.3f} >= s*={s_star:.3f}; spill {spill:.3f} <= proxy loss {l0:.3f}",
        )
    return (
        "minimal-loss proxy / provenance-as-address",
        l0,
        f"s={s:.3f} < s*={s_star:.3f}; broadcast spill {spill:.3f} > proxy loss {l0:.3f}",
    )


def main():
    rng = np.random.default_rng(SEED)
    here = Path(__file__).resolve().parent
    figdir = here.parent / "figures"
    tabdir = here.parent / "output" / "tables"
    figdir.mkdir(parents=True, exist_ok=True)
    tabdir.mkdir(parents=True, exist_ok=True)

    # --- 1. calibration to the observed public-proxy distribution -------------
    obs = {n: distinctiveness(p) for n, p in PROFILES.items()}
    obs_vals = np.array(list(obs.values()))
    a, b = fit_beta(obs_vals)
    s_star = 1.0 - L0 / C_REF

    print("=== ME2 calibration: observed single-dimension distinctiveness s ===")
    for n, s in sorted(obs.items(), key=lambda kv: -kv[1]):
        print(f"  {n:10s} s = {s:.3f}")
    print(
        f"  observed mean = {obs_vals.mean():.3f}  sd = {obs_vals.std(ddof=1):.3f}"
        f"  (N = {len(obs_vals)} public anchors)"
    )
    print(f"  fitted Beta(a={a:.2f}, b={b:.2f}); routing threshold s* = {s_star:.3f}")

    # --- 2. Monte-Carlo broadcast-channel over the calibrated population ------
    s_pop = rng.beta(a, b, size=N_COHORTS)
    oi, sal_match, sal_off = over_index(s_pop)
    neutral = neutral_match_salience()
    # over-index of strong vs neutral on the matched cohort (>1 == resonance lift)
    oi_strong_vs_neutral = sal_match / neutral  # constant: strong always q=1
    frac_above = float((s_pop >= s_star).mean())
    # effect size: matched- vs off-target salience for the strong creative
    d = cohens_d(sal_match * np.ones_like(s_pop), sal_off)

    # bootstrap CIs over cohorts
    boot_oi, boot_frac, boot_spill = [], [], []
    for _ in range(N_BOOT):
        idx = rng.integers(0, N_COHORTS, N_COHORTS)
        boot_oi.append(float(oi[idx].mean()))
        boot_frac.append(float((s_pop[idx] >= s_star).mean()))
        boot_spill.append(float((C_REF * (1.0 - s_pop[idx])).mean()))
    oi_lo, oi_hi = ci95(boot_oi)
    fr_lo, fr_hi = ci95(boot_frac)
    sp_lo, sp_hi = ci95(boot_spill)

    print("\n=== ME2 Monte-Carlo (N = %d cohorts, seed = %d) ===" % (N_COHORTS, SEED))
    print(
        f"  resonance over-index (matched / off-target, strong creative):"
        f" mean = {oi.mean():.3f}  95% CI [{oi_lo:.3f}, {oi_hi:.3f}]"
    )
    print(
        f"  over-index strong vs neutral on matched cohort: {oi_strong_vs_neutral:.3f}"
    )
    print(f"  matched-vs-off salience effect size (Cohen's d): {d:.3f}")
    print(
        f"  fraction of cohorts above routing threshold s*={s_star:.3f}:"
        f" {frac_above:.3f}  95% CI [{fr_lo:.3f}, {fr_hi:.3f}]"
    )
    print(
        f"  mean broadcast spill cost: {C_REF*(1-s_pop).mean():.3f}"
        f"  95% CI [{sp_lo:.3f}, {sp_hi:.3f}]"
    )

    # --- 3. two case studies: the handoff contract in operation ---------------
    # Maintenance: established distinctive brand (highest observed anchor).
    maint_name = max(obs, key=obs.get)
    s_maint = obs[maint_name]
    # Category creation: an undifferentiated new entrant whose perception is not
    # yet FORMED -- a flat profile in which no dimension stands out, so the
    # single-dimension distinctiveness sits at the s = 1/8 floor. This is the
    # empirical face of "no sensitivity yet formed"; MOVING the cohort off the
    # floor (forming the distinctiveness) is the perception-FORMATION problem
    # deferred to the spectral-dynamics companion (2026z), not a reaching
    # decision. Equal-magnitude alternating deviations land exactly at the floor.
    new_entrant = [6.1, 5.9, 6.1, 5.9, 6.1, 5.9, 6.1, 5.9]
    s_newcat = distinctiveness(new_entrant)
    cases = [
        ("Maintenance (established, distinctive brand: %s)" % maint_name, s_maint),
        ("Category creation (undifferentiated new entrant)", s_newcat),
    ]
    print("\n=== ME2 case studies: handoff-contract bridge selection ===")
    rows = []
    for label, s in cases:
        bridge, cost, why = recommend_bridge(s)
        oi_case, sm, so = over_index(s)
        print(f"  {label}")
        print(f"      distinctiveness s = {s:.3f}")
        print(f"      -> bridge: {bridge}")
        print(f"      -> cost:   {cost:.3f}   ({why})")
        print(f"      -> resonance over-index at this s: {oi_case:.3f}")
        rows.append(
            {
                "case": label,
                "distinctiveness_s": round(s, 4),
                "bridge": bridge,
                "cost": round(cost, 4),
                "over_index": round(float(oi_case), 4),
            }
        )

    # --- write results table -------------------------------------------------
    csv_path = tabdir / "me2_results.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value", "ci_low", "ci_high"])
        w.writerow(
            ["observed_distinctiveness_mean", round(float(obs_vals.mean()), 4), "", ""]
        )
        w.writerow(["routing_threshold_s_star", round(s_star, 4), "", ""])
        w.writerow(
            [
                "resonance_over_index_mean",
                round(float(oi.mean()), 4),
                round(oi_lo, 4),
                round(oi_hi, 4),
            ]
        )
        w.writerow(
            [
                "over_index_strong_vs_neutral",
                round(float(oi_strong_vs_neutral), 4),
                "",
                "",
            ]
        )
        w.writerow(["matched_vs_off_cohens_d", round(d, 4), "", ""])
        w.writerow(
            [
                "fraction_above_threshold",
                round(frac_above, 4),
                round(fr_lo, 4),
                round(fr_hi, 4),
            ]
        )
        w.writerow(
            [
                "mean_broadcast_spill",
                round(float(C_REF * (1 - s_pop).mean()), 4),
                round(sp_lo, 4),
                round(sp_hi, 4),
            ]
        )
        w.writerow([])
        w.writerow(["case", "distinctiveness_s", "bridge", "cost", "over_index"])
        for r in rows:
            w.writerow(
                [
                    r["case"],
                    r["distinctiveness_s"],
                    r["bridge"],
                    r["cost"],
                    r["over_index"],
                ]
            )
    print(f"\nwrote {csv_path}")

    # --- figure: over-index vs distinctiveness, with calibrated population ----
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    grid = np.linspace(1 / 8, 1.0, 300)
    oi_grid, _, _ = over_index(grid)
    ax.plot(
        grid,
        oi_grid,
        color="#2b6cb0",
        lw=2.2,
        label="resonance over-index (matched / off-target)",
    )
    ax.axvline(
        s_star,
        color="black",
        ls="--",
        lw=1.2,
        label=f"routing threshold s* = {s_star:.2f}",
    )
    # observed anchors
    for n, s in obs.items():
        oi_n, _, _ = over_index(s)
        ax.plot(s, oi_n, "o", color="#dd6b20", ms=7, markeredgecolor="black")
        ax.annotate(n, (s, oi_n), textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.set_xlabel(r"cohort distinctiveness  $s = \sin^2\beta$ (single-dimension)")
    ax.set_ylabel("resonance over-index")
    ax.set_title("ME2: resonance over-index vs distinctiveness (2026av Figure 2)")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    out = figdir / "figure2_me2_overindex.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
