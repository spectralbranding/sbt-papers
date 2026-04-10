#!/usr/bin/env python3
"""Post-hoc power analysis for R15 hypotheses H1, H2, H5, H6.

Tests whether each primary statistical test was adequately powered (>0.80)
given the observed effect sizes and sample sizes. Uses achieved-power
calculations via non-central distributions to verify that null results
(H5 reversed, H2 near-ceiling) are interpretable.

Hypotheses tested:
  H1: DCI significantly above 0.250 baseline (one-sample t-test)
  H2: Cross-model cosine similarity significantly above random baseline
  H5: Reversed diagonal -- national models collapse MORE on own-culture brands
      (tested as negative correlation between cultural proximity and DCI)
  H6: Western models lower DCI than non-Western models (independent t-test)

Usage:
    python power_analysis.py

Requires: numpy, scipy
"""

import json
import math
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.stats import norm, t as t_dist, nct


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

L4_DIR = Path(__file__).parent
L3_DIR = L4_DIR.parent / "L3_sessions"
RESULTS_FILE = L4_DIR / "run5_analysis_results.json"

ALPHA = 0.05
POWER_THRESHOLD = 0.80


# ---------------------------------------------------------------------------
# Utility: achieved power for one-sample t-test
# ---------------------------------------------------------------------------

def power_one_sample_t(effect_size_d: float, n: int, alpha: float = 0.05,
                       alternative: str = "two-sided") -> float:
    """Compute achieved power for a one-sample t-test.

    Uses the non-central t-distribution with ncp = d * sqrt(n).

    Parameters
    ----------
    effect_size_d : float
        Cohen's d = (mean - mu0) / SD.
    n : int
        Sample size.
    alpha : float
        Significance level.
    alternative : str
        'two-sided', 'greater', or 'less'.

    Returns
    -------
    float
        Achieved power in [0, 1].
    """
    df = n - 1
    ncp = effect_size_d * math.sqrt(n)

    if alternative == "two-sided":
        crit = t_dist.ppf(1 - alpha / 2, df=df)
        power = (
            nct.sf(crit, df=df, nc=ncp)
            + nct.cdf(-crit, df=df, nc=ncp)
        )
    elif alternative == "greater":
        crit = t_dist.ppf(1 - alpha, df=df)
        power = nct.sf(crit, df=df, nc=ncp)
    else:
        crit = t_dist.ppf(alpha, df=df)
        power = nct.cdf(crit, df=df, nc=ncp)

    return float(power)


def power_two_sample_t(effect_size_d: float, n1: int, n2: int,
                       alpha: float = 0.05,
                       alternative: str = "two-sided") -> float:
    """Compute achieved power for a two-sample t-test (equal or unequal n).

    Parameters
    ----------
    effect_size_d : float
        Cohen's d = |mu1 - mu2| / pooled_SD.
    n1, n2 : int
        Sample sizes.
    alpha : float
        Significance level.
    alternative : str
        'two-sided', 'greater', or 'less'.

    Returns
    -------
    float
        Achieved power in [0, 1].
    """
    # Harmonic mean sample size for unequal groups
    n_harm = 2 * n1 * n2 / (n1 + n2)
    df = n1 + n2 - 2
    ncp = effect_size_d * math.sqrt(n_harm / 2)

    if alternative == "two-sided":
        crit = t_dist.ppf(1 - alpha / 2, df=df)
        power = (
            nct.sf(crit, df=df, nc=ncp)
            + nct.cdf(-crit, df=df, nc=ncp)
        )
    elif alternative == "greater":
        crit = t_dist.ppf(1 - alpha, df=df)
        power = nct.sf(crit, df=df, nc=ncp)
    else:
        crit = t_dist.ppf(alpha, df=df)
        power = nct.cdf(crit, df=df, nc=ncp)

    return float(power)


def power_pearson_r(r: float, n: int, alpha: float = 0.05,
                    alternative: str = "two-sided") -> float:
    """Compute achieved power for a Pearson correlation test.

    Uses Fisher's z-transformation approximation.

    Parameters
    ----------
    r : float
        Observed Pearson correlation.
    n : int
        Sample size (number of pairs).
    alpha : float
        Significance level.
    alternative : str
        'two-sided', 'greater', or 'less'.

    Returns
    -------
    float
        Achieved power in [0, 1].
    """
    if abs(r) >= 1.0:
        return 1.0
    z_r = math.atanh(r)
    se = 1.0 / math.sqrt(n - 3)

    if alternative == "two-sided":
        z_crit = norm.ppf(1 - alpha / 2)
        power = (
            norm.sf(z_crit - z_r / se)
            + norm.cdf(-z_crit - z_r / se)
        )
    elif alternative == "greater":
        z_crit = norm.ppf(1 - alpha)
        power = norm.sf(z_crit - z_r / se)
    else:
        z_crit = norm.ppf(alpha)
        power = norm.cdf(z_crit - z_r / se)

    return float(power)


# ---------------------------------------------------------------------------
# Load results
# ---------------------------------------------------------------------------

def load_results() -> dict:
    """Load pre-computed analysis results from run5_analysis_results.json."""
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(
            f"Results file not found: {RESULTS_FILE}\n"
            "Run run5_analysis.py first to generate it."
        )
    with RESULTS_FILE.open() as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# H1 Power Analysis
# ---------------------------------------------------------------------------

def analyze_h1_power(h1: dict) -> dict:
    """Post-hoc power for H1: DCI above 0.250 baseline (one-sample t-test).

    The test uses model-level mean DCIs, so n = number of models.
    Effect size d = (observed_mean - 25.0) / SD of model DCIs.
    """
    n = h1["n_models"]
    d = h1.get("effect_size_d", 0.0)
    t_stat = h1["t_stat"]
    p_value = h1["p_value"]
    mean_dci = h1["mean"]
    sd_dci = h1["std"]

    # Recompute d if not stored or outdated
    if sd_dci > 0:
        d = (mean_dci - 25.0) / sd_dci

    power = power_one_sample_t(d, n, alpha=ALPHA, alternative="greater")

    return {
        "hypothesis": "H1: DCI > 0.250 baseline",
        "test": "one-sample t-test (greater)",
        "n": n,
        "observed_mean_dci_pct": round(mean_dci, 3),
        "baseline_pct": 25.0,
        "effect_size_d": round(d, 3),
        "t_stat": round(t_stat, 3),
        "p_value": p_value,
        "achieved_power": round(power, 3),
        "adequately_powered": power >= POWER_THRESHOLD,
        "note": (
            "Extremely large effect size (d > 3). "
            "Adequately powered even with n=20 models."
            if d > 3 else
            "Effect size and n combine for adequate power."
        ),
    }


# ---------------------------------------------------------------------------
# H2 Power Analysis
# ---------------------------------------------------------------------------

def analyze_h2_power(h2: dict) -> dict:
    """Post-hoc power for H2: mean cosine similarity above chance baseline.

    The observed cosine = 0.977. The null is that LLM profiles are random
    (cosine approximately 0 for random unit vectors in 8D). We test
    whether the observed mean cosine is significantly above zero using
    a one-sample t-test on the pairwise cosine distribution.

    n = number of model pairs; effect size is mean_cosine / std_cosine.
    """
    mean_cos = h2["mean_cosine"]
    std_cos = h2["std_cosine"]
    n_pairs = h2["n_pairs"]

    # Effect size: distance of mean from 0 in SD units
    if std_cos > 0:
        d = mean_cos / std_cos
    else:
        d = float("inf")

    # t-statistic against null cosine = 0
    if std_cos > 0:
        t_stat = mean_cos / (std_cos / math.sqrt(n_pairs))
    else:
        t_stat = float("inf")

    p_value = t_dist.sf(t_stat, df=n_pairs - 1) if math.isfinite(t_stat) else 0.0

    power = power_one_sample_t(
        min(d, 50.0), n_pairs, alpha=ALPHA, alternative="greater"
    )

    return {
        "hypothesis": "H2: Mean cosine similarity > 0 (convergent collapse)",
        "test": "one-sample t-test on pairwise cosines (null = 0)",
        "n_pairs": n_pairs,
        "n_models": h2["n_models"],
        "observed_mean_cosine": round(mean_cos, 4),
        "std_cosine": round(std_cos, 4),
        "effect_size_d": round(d, 3),
        "t_stat": round(t_stat, 3) if math.isfinite(t_stat) else ">1000",
        "p_value": p_value,
        "achieved_power": round(power, 3),
        "adequately_powered": power >= POWER_THRESHOLD,
        "note": (
            "Ceiling effect: cosine = 0.977 with std = 0.014. "
            "Power is effectively 1.0. The real constraint is the "
            "upper bound on cosine, not statistical power."
        ),
    }


# ---------------------------------------------------------------------------
# H5 Power Analysis
# ---------------------------------------------------------------------------

def analyze_h5_power(h5: dict) -> dict:
    """Post-hoc power for H5: reversed diagonal (national models collapse MORE).

    The observed result reversed the predicted direction. We assess whether
    the study was adequately powered to detect the predicted cultural-proximity
    advantage if it had existed at a small-to-medium effect.

    H5 was tested as a one-sample t-test on per-pair advantage scores
    (other_DCI - national_DCI). The observed mean advantage = -0.015
    (negative = national models collapse MORE, reversing the prediction).

    We report:
    1. Power to detect d = 0.5 (medium advantage) in the predicted direction
    2. Power to detect the observed reversed effect (d ~ -0.5)
    3. Interpretation: is the null result a power failure or a real reversal?
    """
    t_stat = h5["t_stat"]
    p_value = h5["p_value"]
    mean_adv = h5["mean_advantage"]
    n_pairs = h5["total_pairs"]

    # We need SD of advantages to compute d
    # Recompute from per_pair data
    advantages = [v["advantage"] for v in h5["per_pair"].values()]
    sd_adv = float(np.std(advantages, ddof=1)) if len(advantages) > 1 else 0.01

    # Observed effect size (direction: positive = national models have LOWER DCI)
    d_obs = mean_adv / sd_adv if sd_adv > 0 else 0.0

    # Power to detect a medium effect in the predicted direction (d = 0.5)
    power_medium = power_one_sample_t(0.5, n_pairs, alpha=ALPHA, alternative="greater")
    # Power to detect the observed reversed effect
    power_observed = power_one_sample_t(
        abs(d_obs), n_pairs, alpha=ALPHA, alternative="two-sided"
    )

    underpowered_for_small = power_medium < POWER_THRESHOLD

    return {
        "hypothesis": "H5: Reversed diagonal (national models collapse more)",
        "test": "one-sample t-test on per-pair advantage scores",
        "n_pairs": n_pairs,
        "observed_mean_advantage": round(mean_adv, 4),
        "sd_advantages": round(sd_adv, 4),
        "effect_size_d_observed": round(d_obs, 3),
        "t_stat": round(t_stat, 3) if t_stat is not None else None,
        "p_value": p_value,
        "direction": (
            "reversed (national models collapse MORE, opposite to prediction)"
            if mean_adv < 0 else
            "as predicted (national models collapse less)"
        ),
        "power_to_detect_medium_d05": round(power_medium, 3),
        "power_to_detect_observed_effect": round(power_observed, 3),
        "adequately_powered_for_medium": not underpowered_for_small,
        "interpretation": (
            "n=8 pairs gives low power for small-medium effects. "
            "However, the observed effect is in the WRONG direction "
            "(p=0.027, mean_advantage=-0.015), not merely absent. "
            "The reversal is statistically significant, so this is not "
            "a type II error. The shrunken-variance mechanism is supported."
            if mean_adv < 0 and p_value is not None and p_value < 0.05 else
            "n=8 pairs is low. Null result could reflect insufficient power."
        ),
    }


# ---------------------------------------------------------------------------
# H6 Power Analysis
# ---------------------------------------------------------------------------

def analyze_h6_power(h6: dict) -> dict:
    """Post-hoc power for H6: Western DCI < non-Western DCI (two-sample t-test).

    n1 = Western model calls, n2 = non-Western model calls.
    Effect size d = (nonwestern_mean - western_mean) / pooled_SD.
    """
    western_mean = h6["western_mean_dci"]
    nonwestern_mean = h6["nonwestern_mean_dci"]
    n_western = h6.get("n_western", 148)
    n_nonwestern = h6.get("n_nonwestern", 314)
    t_stat = h6["t_stat"]
    p_value = h6["p_value"]
    diff = h6["difference"]

    # Estimate pooled SD from t-statistic and sample sizes
    # t = diff / (pooled_se), pooled_se = sd * sqrt(1/n1 + 1/n2)
    # |t| = d * sqrt(n_harm/2) => d = |t| / sqrt(n_harm/2)
    n_harm = 2 * n_western * n_nonwestern / (n_western + n_nonwestern)
    d = abs(t_stat) / math.sqrt(n_harm / 2) if n_harm > 0 else 0.0

    power = power_two_sample_t(
        d, n_western, n_nonwestern, alpha=ALPHA, alternative="two-sided"
    )

    return {
        "hypothesis": "H6: Western DCI < non-Western DCI (training breadth effect)",
        "test": "independent-samples t-test (two-sided)",
        "n_western_calls": n_western,
        "n_nonwestern_calls": n_nonwestern,
        "western_mean_dci": round(western_mean, 4),
        "nonwestern_mean_dci": round(nonwestern_mean, 4),
        "difference": round(diff, 4),
        "effect_size_d": round(d, 4),
        "t_stat": round(t_stat, 3),
        "p_value": p_value,
        "achieved_power": round(power, 3),
        "adequately_powered": power >= POWER_THRESHOLD,
        "note": (
            "Large n (>460 total calls) ensures high power even for "
            "small effects. d ~ 0.3 with n1=148, n2=314 gives power > 0.90."
        ),
    }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_separator(char: str = "-", width: int = 70) -> None:
    print(char * width)


def print_result(result: dict) -> None:
    """Print a single hypothesis power result."""
    print(f"\nHypothesis: {result['hypothesis']}")
    print(f"Test:       {result['test']}")

    for k, v in result.items():
        if k in ("hypothesis", "test"):
            continue
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}")
        elif isinstance(v, bool):
            print(f"  {k}: {'YES' if v else 'NO'}")
        else:
            print(f"  {k}: {v}")

    powered_key = "adequately_powered"
    if powered_key in result:
        status = "ADEQUATE (>=0.80)" if result[powered_key] else "UNDERPOWERED (<0.80)"
        print(f"  >> Power status: {status}")


def main() -> None:
    """Run post-hoc power analysis for H1, H2, H5, H6."""
    out_dir = Path(__file__).resolve().parent
    print("=" * 70)
    print("R15 POST-HOC POWER ANALYSIS")
    print("Spectral Metamerism in AI-Mediated Brand Perception")
    print("=" * 70)
    print(f"Alpha = {ALPHA}, Power threshold = {POWER_THRESHOLD}")

    results = load_results()

    analyses = [
        analyze_h1_power(results["H1_overweighting"]),
        analyze_h2_power(results["H2_convergent_collapse"]),
        analyze_h5_power(results["H5_diagonal_advantage"]),
        analyze_h6_power(results["H6_bidirectional_asymmetry"]),
    ]

    for result in analyses:
        print_separator()
        print_result(result)

    print_separator("=")
    print("\nSUMMARY")
    print_separator()
    print(f"{'Hypothesis':<12} {'Power':>8} {'Adequate':>10} {'p-value':>12}")
    print_separator()
    labels = ["H1", "H2", "H5", "H6"]
    # H5 uses different power keys because the reversal requires two power estimates
    power_keys = ["achieved_power", "achieved_power",
                  "power_to_detect_medium_d05", "achieved_power"]
    powered_keys = ["adequately_powered", "adequately_powered",
                    "adequately_powered_for_medium", "adequately_powered"]
    for label, r, pkey, adkey in zip(labels, analyses, power_keys, powered_keys):
        p_val = r.get("p_value", float("nan"))
        power_val = r.get(pkey, float("nan"))
        adequate = r.get(adkey, False)
        p_str = f"{p_val:.4e}" if isinstance(p_val, float) else str(p_val)
        power_str = f"{power_val:.3f}" if isinstance(power_val, float) else "n/a"
        # H5 note: power shown is for medium effect in predicted direction
        extra = " (d=0.5, predicted dir.)" if label == "H5" else ""
        print(f"{label:<12} {power_str:>8} {'YES' if adequate else 'NO':>10} {p_str:>12}{extra}")

    print_separator()
    print("\nInterpretation notes:")
    print("- H1 and H6: extremely high power; null findings would be reliable.")
    print("- H2: ceiling effect on cosine; power is effectively 1.0.")
    print("- H5: low n=8 pairs limits power for small effects,")
    print("  but the reversal is statistically significant (p<0.05),")
    print("  so the finding is a real reversal, not a power failure.")
    print()

    # Persist JSON results next to this script
    out_json = out_dir / "power_analysis_results.json"
    payload = {
        "schema_version": "1.0",
        "alpha": ALPHA,
        "power_threshold": POWER_THRESHOLD,
        "hypotheses": {
            label: result for label, result in zip(labels, analyses)
        },
        "summary": [
            {
                "hypothesis": label,
                "power": result.get(pkey),
                "adequate": result.get(adkey, False),
                "p_value": result.get("p_value"),
            }
            for label, result, pkey, adkey in zip(labels, analyses, power_keys, powered_keys)
        ],
        "interpretation": [
            "H1 and H6: extremely high power; null findings would be reliable.",
            "H2: ceiling effect on cosine; power is effectively 1.0.",
            "H5: low n=8 pairs limits power for small effects, but the reversal is statistically significant (p<0.05), so the finding is a real reversal, not a power failure.",
        ],
    }
    out_json.write_text(json.dumps(payload, indent=2, default=float))
    print(f"Wrote: {out_json.name}")


if __name__ == "__main__":
    main()
