"""
Companion Computation Script — R21 Spectral Immunity
=====================================================
Reproduces the DCI means, TOST p-values, Cohen's d and variance decomposition
of Tables 3-7 and checks every printed cell against the archived data in:

    Zharnikov, D. (2026ac). Spectral Immunity: Why Brand Portfolio Interference
    Disappears for AI Observers. Working Paper. DOI 10.5281/zenodo.19765401

Run command:
    uv run python compute_dci.py

Python version: 3.12
Fixed random seed: 42

Data sources:
    Primary experiment (7,975 obs): https://doi.org/10.57967/hf/8380
    Published-brand extension (1,950 obs): https://doi.org/10.57967/hf/8380
    Raw responses (Turn-1 scores of Table 6):
        https://github.com/spectralbranding/sbt-papers/tree/main/r20-portfolio-ai/responses
    Zenodo archive: https://doi.org/10.5281/zenodo.19555282

This script has two modes:
    1. Full mode (--full): reads main_experiment.jsonl, multiturn.jsonl and
       published_brands.jsonl (HuggingFace, or a local folder via --data-dir)
       and reproduces
         Table 3  DCI by brand and condition (all 160 cells), mean |delta DCI|,
                  TOST and FDR counts, the H6 range and the cell-mean SE range
         Table 4  nested, sequential (type I) variance decomposition
         Table 5  tradition sub-groups
         Table 6  multi-turn results; the Turn-1 scores exist only in the raw
                  response files, so the Turn-1 cells, delta, d, p, the FDR set,
                  the multi-turn mean delta and the SE range need
                  --responses DIR (without it only the Turn-2 column is
                  checked, and the script says so)
         Table 7  published-brand extension on Equation 2 (10 brands, 1,300
                  observations), TOST and FDR counts, SE range
       Each printed value is hard-coded in this file and compared; the script
       prints OK or MISMATCH per row and a final all-match line (exit code 1 on
       any mismatch).
    2. Stub mode (default, no network required): demonstrates the DCI metric
       computation against the canonical brand profiles and checks Table 3
       values for the 20 brands against themselves.

Usage:
    uv run python compute_dci.py            # stub mode
    uv run --with huggingface_hub --with pandas --with scipy \\
        python compute_dci.py --full        # full mode (network)
    uv run --with huggingface_hub --with pandas --with scipy \\
        python compute_dci.py --full --responses PATH/TO/r20-portfolio-ai/responses
"""

import argparse
import json
import math
import random
import sys
from pathlib import Path

SEED = 42
random.seed(SEED)

# ---------------------------------------------------------------------------
# DCI metric (Equation 2, paper §Theoretical Framework)
# DCI = sum(|w_d - 1/8|) / 2 * 100
# where w_d are the normalized per-dimension weights (ratings / sum of ratings)
# ---------------------------------------------------------------------------


def compute_dci(ratings: list[float]) -> float:
    """
    Compute the Dimensional Concentration Index for an 8-dimension profile.

    Parameters
    ----------
    ratings : list of 8 floats
        Raw 1-5 scale scores on the 8 SBT dimensions
        [Semiotic, Narrative, Ideological, Experiential, Social, Economic,
         Cultural, Temporal]

    Returns
    -------
    float
        DCI value (0 = perfectly uniform; 100 = all mass on one dimension)

    Examples
    --------
    >>> compute_dci([5, 5, 5, 5, 5, 5, 5, 5])   # perfectly flat
    0.0
    >>> compute_dci([5, 1, 1, 1, 1, 1, 1, 1])   # max concentration
    87.5
    """
    if len(ratings) != 8:
        raise ValueError("Expected 8 dimension scores.")
    total = sum(ratings)
    if total == 0:
        raise ValueError("All zero ratings — cannot normalize.")
    w = [r / total for r in ratings]
    uniform = 1.0 / 8.0
    dci = sum(abs(wi - uniform) for wi in w) / 2.0 * 100.0
    return round(dci, 4)


# ---------------------------------------------------------------------------
# TOST equivalence test (Lakens 2017)
# Two one-sided t-tests with bounds [-bound, +bound]
# Returns (t_lower, t_upper, p_lower, p_upper, p_tost, equivalent)
# ---------------------------------------------------------------------------


def tost(
    delta_dci_values: list[float],
    bound: float = 1.0,
    alpha: float = 0.05,
) -> dict:
    """
    Two One-Sided Tests (TOST) for equivalence.

    Tests H0: |mean(delta)| >= bound  vs.  H1: |mean(delta)| < bound.

    Parameters
    ----------
    delta_dci_values : list of floats
        Per-observation DCI differences (portfolio - solo).
    bound : float
        Equivalence bound in DCI points (default 1.0).
    alpha : float
        Significance level (default .05).

    Returns
    -------
    dict with keys: mean_delta, se, t_lower, t_upper, p_lower, p_upper,
                    p_tost, equivalent
    """
    n = len(delta_dci_values)
    if n < 2:
        return {"error": "Need at least 2 observations."}

    mean_d = sum(delta_dci_values) / n
    var = sum((x - mean_d) ** 2 for x in delta_dci_values) / (n - 1)
    se = math.sqrt(var / n)

    if se == 0:
        return {
            "mean_delta": mean_d,
            "se": 0,
            "equivalent": abs(mean_d) < bound,
            "note": "zero variance",
        }

    # t statistics for the two one-sided tests
    t_lower = (mean_d - (-bound)) / se  # test mean > -bound
    t_upper = (mean_d - bound) / se  # test mean < +bound

    # Approximate p-values using the t-distribution (df = n-1)
    # Using a simple approximation for |t| < 10
    df = n - 1
    p_lower = _t_pvalue_one_sided(t_lower, df, direction="greater")
    p_upper = _t_pvalue_one_sided(t_upper, df, direction="less")

    p_tost = max(p_lower, p_upper)
    equivalent = p_tost < alpha

    return {
        "n": n,
        "mean_delta": round(mean_d, 4),
        "se": round(se, 4),
        "t_lower": round(t_lower, 3),
        "t_upper": round(t_upper, 3),
        "p_lower": round(p_lower, 4),
        "p_upper": round(p_upper, 4),
        "p_tost": round(p_tost, 4),
        "equivalent": equivalent,
    }


def _t_pvalue_one_sided(t: float, df: int, direction: str) -> float:
    """Approximate one-sided p-value using normal approximation for df > 30."""
    # For df > 30, t ≈ z; for smaller df, use t-distribution approximation
    # This is sufficient for reproducibility verification purposes.
    # A production implementation should use scipy.stats.t.sf / scipy.stats.t.cdf
    import math

    if df > 30:
        # Normal approximation
        z = t
        p = 0.5 * math.erfc(abs(z) / math.sqrt(2))
        if direction == "greater":
            return p if z > 0 else 1.0 - p
        else:
            return p if z < 0 else 1.0 - p
    else:
        # Simple approximation for small df (Wilson-Hilferty)
        x = df / (df + t**2)
        # Regularized incomplete beta approximation
        p = _betai(df / 2.0, 0.5, x) / 2.0
        if direction == "greater":
            return p if t < 0 else 1.0 - p
        else:
            return 1.0 - p if t < 0 else p


def _betai(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta function (simple continued fraction approx)."""
    if x < 0.0 or x > 1.0:
        return 0.0
    if x == 0.0 or x == 1.0:
        return x
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(math.log(x) * a + math.log(1.0 - x) * b - lbeta) / a
    # Simple approximation via 50-term continued fraction
    cf = _betacf(a, b, x)
    return min(1.0, front * cf)


def _betacf(a: float, b: float, x: float, max_iter: int = 50) -> float:
    """Continued fraction for the incomplete beta function."""
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    d = 1.0 / d if abs(d) < 1e-30 else 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        c = 1.0 + aa / c
        d = 1.0 / d if abs(d) < 1e-30 else 1.0 / d
        c = 1.0 / c if abs(c) < 1e-30 else c
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        c = 1.0 + aa / c
        d = 1.0 / d if abs(d) < 1e-30 else 1.0 / d
        c = 1.0 / c if abs(c) < 1e-30 else c
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-7:
            break
    return h


# ---------------------------------------------------------------------------
# Cohen's d
# ---------------------------------------------------------------------------


def cohens_d(group1: list[float], group2: list[float]) -> float:
    """Pooled Cohen's d for two independent groups."""
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return float("nan")
    mean1 = sum(group1) / n1
    mean2 = sum(group2) / n2
    var1 = sum((x - mean1) ** 2 for x in group1) / (n1 - 1)
    var2 = sum((x - mean2) ** 2 for x in group2) / (n2 - 1)
    pooled_sd = math.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return 0.0
    return (mean1 - mean2) / pooled_sd


# ---------------------------------------------------------------------------
# Canonical brand profiles (from [internal ref removed] project spec)
# Used in stub mode to verify DCI computation
# ---------------------------------------------------------------------------

CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

# ---------------------------------------------------------------------------
# Table 3 reference values (paper Table 3, solo DCI)
# Brands and Solo DCI values as reported in the paper
# ---------------------------------------------------------------------------

TABLE3_SOLO_DCI = {
    "Dior": 3.5,
    "Fendi": 5.7,
    "Louis Vuitton": 4.4,
    "Axe": 8.6,
    "Ben & Jerry's": 6.4,
    "Dove": 5.6,
    "Gillette": 6.4,
    "Pampers": 6.5,
    "Tide": 7.4,
    "Toyota": 6.8,
    "Lexus": 5.2,
    "L'Oreal Paris": 5.6,
    "Lancome": 5.4,
    "Maybelline": 6.6,
    "Volvo": 6.5,
    "Polestar": 8.6,
    "Geely Auto": 8.0,
    "Yandex": 6.6,
    "Yandex Market": 8.2,
    "Yandex Taxi": 8.9,
}

TABLE3_PORT_DCI = {
    "Dior": 3.8,
    "Fendi": 5.8,
    "Louis Vuitton": 4.7,
    "Axe": 8.7,
    "Ben & Jerry's": 6.4,
    "Dove": 5.9,
    "Gillette": 6.3,
    "Pampers": 6.2,
    "Tide": 7.2,
    "Toyota": 6.4,
    "Lexus": 5.8,
    "L'Oreal Paris": 5.5,
    "Lancome": 5.4,
    "Maybelline": 6.6,
    "Volvo": 6.2,
    "Polestar": 8.5,
    "Geely Auto": 8.5,
    "Yandex": 6.6,
    "Yandex Market": 8.4,
    "Yandex Taxi": 8.5,
}


def stub_mode() -> None:
    """Demonstrate DCI computation and verify against Table 3 reference values."""
    print("=" * 60)
    print("R21 Spectral Immunity — Companion Computation Script")
    print("Stub mode (no network required)")
    print("=" * 60)
    print()

    # 1. Verify DCI formula against canonical profiles
    print("1. DCI computation on canonical SBT brand profiles")
    print("-" * 60)
    print(f"{'Brand':<12}  {'DCI':>6}")
    for brand, profile in CANONICAL_PROFILES.items():
        dci = compute_dci(profile)
        print(f"{brand:<12}  {dci:>6.2f}")
    print()

    # 2. Check Table 3 delta DCI values
    print("2. Table 3 delta DCI verification (solo → portfolio)")
    print("-" * 60)
    print(
        f"{'Brand':<16}  {'Solo':>6}  {'Port':>6}  {'Delta':>6}  {'Paper':>6}  {'Match':>5}"
    )

    PAPER_DELTAS = {
        "Dior": +0.35,
        "Fendi": +0.09,
        "Louis Vuitton": +0.34,
        "Axe": +0.04,
        "Ben & Jerry's": -0.04,
        "Dove": +0.30,
        "Gillette": -0.15,
        "Pampers": -0.29,
        "Tide": -0.20,
        "Toyota": -0.37,
        "Lexus": +0.59,
        "L'Oreal Paris": -0.15,
        "Lancome": +0.05,
        "Maybelline": -0.10,
        "Volvo": -0.28,
        "Polestar": -0.08,
        "Geely Auto": +0.54,
        "Yandex": -0.01,
        "Yandex Market": +0.21,
        "Yandex Taxi": -0.36,
    }

    all_match = True
    for brand in TABLE3_SOLO_DCI:
        solo = TABLE3_SOLO_DCI[brand]
        port = TABLE3_PORT_DCI[brand]
        delta = round(port - solo, 2)
        paper_delta = PAPER_DELTAS[brand]
        match = abs(delta - paper_delta) < 0.01
        if not match:
            all_match = False
        marker = "OK" if match else "MISMATCH"
        print(
            f"{brand:<16}  {solo:>6.1f}  {port:>6.1f}  {delta:>+6.2f}  {paper_delta:>+6.2f}  {marker:>5}"
        )

    print()
    if all_match:
        print("All Table 3 delta values match paper-reported values.")
    else:
        print("NOTE: Small discrepancies are expected in stub mode because Table 3")
        print("reports DCI means rounded to 1 decimal place. The paper-reported deltas")
        print("were computed from unrounded cell means in the full dataset.")
        print("Run --full mode with the archived data to reproduce exact values.")

    # 3. TOST demonstration
    print()
    print("3. TOST equivalence test demonstration (simulated, seed=42)")
    print("-" * 60)
    # Simulate N=65 delta DCI values for a brand with mean ~0.23 (paper headline)
    rng_deltas = [random.gauss(0.23, 1.8) for _ in range(65)]
    result = tost(rng_deltas, bound=1.0)
    print(f"  Simulated mean delta DCI: {result['mean_delta']}")
    print(f"  SE: {result['se']}")
    print(f"  TOST p: {result['p_tost']}")
    print(f"  Equivalent (p < .05): {result['equivalent']}")
    print()
    print("Full mode (--full flag): reads the archived records (HuggingFace DOI")
    print("10.57967/hf/8380) and reproduces Tables 3-7, checking every printed cell.")
    print()
    print("Run command: uv run --with huggingface_hub --with pandas --with scipy \\")
    print("    python compute_dci.py --full [--responses DIR]")


DIMS = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
]
HF_REPO = "spectralbranding/r20-portfolio-ai-perception"
RESPONSES_URL = (
    "https://github.com/spectralbranding/sbt-papers/tree/main/"
    "r20-portfolio-ai/responses"
)

TRADITIONS = {
    "Western": {"claude", "gpt4omini", "gemini25flash", "grok", "llama", "gemma4"},
    "Chinese": {"deepseek", "qwen3"},
    "European": {"mistral"},
    "Japanese": {"swallow"},
    "Korean": {"exaone"},
    "Russian": {"yandex"},
    "Indian": {"sarvam"},
}

# Table 5 as printed in the paper: (Delta DCI, d, p) per tradition.
PAPER_TABLE5_SE = (0.12, 0.38)  # Table 5 Notes: SE range of the tradition mean deltas

PAPER_TABLE5 = {
    "Western": (0.01, 0.02, 0.913),
    "Chinese": (-0.06, -0.09, 0.692),
    "European": (-0.35, -0.46, 0.055),
    "Japanese": (-0.59, -0.63, 0.011),
    "Korean": (0.34, 0.35, 0.130),
    "Russian": (-0.24, -0.32, 0.168),
    "Indian": (-0.13, -0.07, 0.743),
}

# fmt: off
# Table 3 as printed (all cells are strings, compared as printed):
# (Solo DCI, Port DCI, Delta, t, p, d, TOST p, Equivalent)
TABLE3_COLUMNS = ["Solo", "Port", "Delta", "t", "p", "d", "TOST p", "Equiv"]
PAPER_TABLE3 = {
    ("LVMH", "Dior"): ("3.5", "3.8", "+.35", "1.13", ".262", "+.20", ".020", "Yes"),
    ("LVMH", "Fendi"): ("5.7", "5.8", "+.09", ".38", ".702", "+.07", "< .001", "Yes"),
    ("LVMH", "Louis Vuitton"): ("4.4", "4.7", "+.34", ".90", ".368", "+.16", ".043", "Yes"),
    ("Unilever", "Axe"): ("8.6", "8.7", "+.04", ".12", ".909", "+.02", ".002", "Yes"),
    ("Unilever", "Ben & Jerry's"): ("6.4", "6.4", "-.04", "-.24", ".809", "-.04", "< .001", "Yes"),
    ("Unilever", "Dove"): ("5.6", "5.9", "+.30", "1.20", ".234", "+.21", ".003", "Yes"),
    ("P&G", "Gillette"): ("6.4", "6.3", "-.15", "-.71", ".477", "-.13", "< .001", "Yes"),
    ("P&G", "Pampers"): ("6.5", "6.2", "-.29", "-1.27", ".207", "-.22", ".001", "Yes"),
    ("P&G", "Tide"): ("7.4", "7.2", "-.20", "-.55", ".580", "-.10", ".016", "Yes"),
    ("Toyota", "Toyota"): ("6.8", "6.4", "-.37", "-1.69", ".093", "-.30", ".003", "Yes"),
    ("Toyota", "Lexus"): ("5.2", "5.8", "+.59", "2.94", ".004", "+.52", ".022", "Yes"),
    ("L'Oreal", "L'Oreal Paris"): ("5.6", "5.5", "-.15", "-.75", ".456", "-.13", "< .001", "Yes"),
    ("L'Oreal", "Lancome"): ("5.4", "5.4", "+.05", ".28", ".783", "+.05", "< .001", "Yes"),
    ("L'Oreal", "Maybelline"): ("6.6", "6.6", "-.10", "-.29", ".771", "-.05", ".004", "Yes"),
    ("Geely", "Volvo"): ("6.5", "6.2", "-.28", "-1.30", ".196", "-.23", "< .001", "Yes"),
    ("Geely", "Polestar"): ("8.6", "8.5", "-.08", "-.27", ".788", "-.05", ".001", "Yes"),
    ("Geely", "Geely Auto"): ("8.0", "8.5", "+.54", "1.49", ".139", "+.27", ".102", "No"),
    ("Yandex", "Yandex"): ("6.6", "6.6", "-.01", "-.03", ".976", "-.01", "< .001", "Yes"),
    ("Yandex", "Yandex Market"): ("8.2", "8.4", "+.21", ".54", ".592", "+.10", ".021", "Yes"),
    ("Yandex", "Yandex Taxi"): ("8.9", "8.5", "-.36", "-.87", ".384", "-.16", ".062", "No"),
}
# Table 3 prose figures: mean |delta| over the 20 brands (abstract, Results, H5,
# Discussion, Conclusion), n TOST-equivalent, n FDR-significant, H6 delta range,
# and the SE range of the 40 cell means (SD / sqrt(n), the Notes sentence).
PAPER_T3_PROSE = {
    "mean |delta|": ".23",
    "TOST-equivalent brands": "18",
    "FDR-significant brands": "0",
    "H6 range low": "-.15",
    "H6 range high": "+.05",
    "SE of cell means low": ".10",
    "SE of cell means high": ".31",
}

# Table 4 as printed (nested, sequential / type I shares of DCI variance, %).
# The condition share prints as "< .01"; its unrounded value is about .003.
PAPER_TABLE4 = {
    "Portfolio (parent company)": "25.2",
    "Brand within portfolio": "16.2",
    "Model": "7.5",
    "Condition (solo vs. portfolio)": "< .01",
    "Residual": "51.1",
}
PAPER_T4_PROSE = {
    "Brand identity (portfolio + brand within portfolio)": "41.4",
    "Shares of the printed rows sum to": "100.0",
}

# Table 6 as printed: (T1 DCI, T2 DCI, Delta, d); every p prints as "<.001".
PAPER_TABLE6 = {
    "Geely Auto": ("8.1", "5.1", "-2.93", "-1.11"),
    "Polestar": ("8.8", "7.4", "-1.47", "-.54"),
    "Toyota": ("6.8", "6.0", "-.80", "-.61"),
    "Yandex": ("6.2", "5.1", "-1.06", "-.49"),
}
PAPER_T6_PROSE = {
    "FDR-significant brands": "Geely Auto, Polestar, Toyota, Yandex",
    "Mean delta over the 20 brands": "-.26",
    "SD of the 20 per-brand deltas": ".88",
    "One-sample t(19) of the 20 deltas": "-1.31",
    "p of that t": ".205",
    "d of that mean (mean / SD)": "-.29",
    "Mean delta of the 16 other brands": "+.07",
    "Pooled mean delta over all response pairs": "-.23",
    "Pooled paired t": "-3.13",
    "Pooled p": ".002",
    "Pooled d": "-.09",
    "SE of the 8 table cell means low": ".17",
    "SE of the 8 table cell means high": ".30",
}

# Table 7 as printed (Equation 2): (Solo DCI, Port DCI, Delta, d).
PAPER_TABLE7 = {
    "Coca-Cola": ("5.8", "6.0", "+.21", "+.16"),
    "Pepsi": ("6.2", "6.8", "+.52", "+.34"),
    "BMW": ("5.2", "5.1", "-.13", "-.12"),
    "Audi": ("5.5", "5.0", "-.45", "-.44"),
    "Google": ("5.8", "6.0", "+.22", "+.16"),
    "Disney": ("5.2", "5.3", "+.12", "+.07"),
    "Colgate": ("7.9", "8.4", "+.47", "+.20"),
    "Samsung": ("5.5", "5.6", "+.09", "+.07"),
    "H&M": ("9.1", "9.1", "+.04", "+.01"),
    "Dell": ("8.4", "8.4", "-.03", "-.02"),
}
PAPER_T7_PROSE = {
    "Observations tested": "1300",
    "FDR-significant brands": "0",
    "TOST-equivalent brands": "9",
    "TOST p of Colgate": ".104",
    "Audi p": ".012",
    "Audi BH threshold (smallest of 10 p)": ".005",
    "Pepsi p": ".053",
    "Solo DCI means low": "5.2",
    "Solo DCI means high": "9.1",
    "SE of cell means low": ".11",
    "SE of cell means high": ".38",
}
# fmt: on


def _libs():
    """Import the full-mode dependencies or exit with the install command."""
    try:
        import numpy as np
        import pandas as pd
        from scipy import stats
    except ImportError:
        print("Full mode requires pandas, scipy and huggingface_hub:")
        print("  uv run --with huggingface_hub --with pandas --with scipy \\")
        print("      python compute_dci.py --full")
        sys.exit(1)
    return np, pd, stats


def _half_up(x, dp):
    """Round half up (Decimal), the way the printed tables were rounded."""
    from decimal import ROUND_HALF_UP, Decimal

    return Decimal(repr(round(float(x), 10))).quantize(
        Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP
    )


def fmt(x, dp, signed=False):
    """Format like the paper: no leading zero, explicit + only when signed."""
    v = _half_up(x, dp)
    s = f"{abs(v):.{dp}f}"
    if s.startswith("0."):
        s = s[1:]
    if v < 0:
        return "-" + s
    return ("+" + s) if signed else s


def fmt_tost(p):
    """TOST p as printed: three decimals, "< .001" below .001."""
    return "< .001" if p < 0.001 else fmt(p, 3)


def dci_matrix(ratings):
    """Equation 2 for every row of an (n, 8) rating matrix, unrounded."""
    np, _, _ = _libs()
    r = np.asarray(ratings, dtype=float)
    s = r.sum(axis=1, keepdims=True)
    safe = np.where(s > 0, s, 1.0)
    dci = np.abs(r / safe - 1.0 / 8.0).sum(axis=1) / 2.0 * 100.0
    return np.where(s[:, 0] > 0, dci, 0.0)


def cohens_d_array(a, b):
    """Pooled-SD Cohen's d of (a - b), numpy version of cohens_d()."""
    np, _, _ = _libs()
    n1, n2 = len(a), len(b)
    v1, v2 = np.var(a, ddof=1), np.var(b, ddof=1)
    pooled = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    return 0.0 if pooled == 0 else float((np.mean(a) - np.mean(b)) / pooled)


def tost_analysis5(solo, port, bound=1.0):
    """TOST as in the original analysis 5 (R20 analyze_portfolio.py).

    The mean difference and both SDs are rounded to 2 decimals first (the
    original reads them from its rounded results frame), SE = sqrt(sd1^2/n1 +
    sd2^2/n2), df = n1 + n2 - 2; equivalent iff max(p_upper, p_lower) < .05.
    """
    np, _, stats = _libs()
    n1, n2 = len(solo), len(port)
    delta = round(float(np.mean(port) - np.mean(solo)), 2)
    sd1 = round(float(np.std(solo, ddof=1)), 2)
    sd2 = round(float(np.std(port, ddof=1)), 2)
    se = np.sqrt(sd1**2 / n1 + sd2**2 / n2) if (sd1 > 0 or sd2 > 0) else 1e-10
    dfa = n1 + n2 - 2
    p_up = stats.t.cdf((delta - bound) / se, dfa)
    p_lo = 1 - stats.t.cdf((delta + bound) / se, dfa)
    p = float(max(p_up, p_lo))
    return p, p < 0.05


def bh_significant(p, alpha=0.05):
    """Benjamini-Hochberg: boolean array of rejected hypotheses."""
    np, _, _ = _libs()
    p = np.asarray(p, dtype=float)
    n = len(p)
    order = np.argsort(p)
    ok = p[order] <= np.arange(1, n + 1) / n * alpha
    sig = np.zeros(n, dtype=bool)
    if ok.any():
        sig[order[: np.max(np.where(ok)[0]) + 1]] = True
    return sig


class Checks:
    """Counts printed-versus-computed cells and prints OK / MISMATCH rows."""

    def __init__(self):
        self.total = 0
        self.bad = []

    def header(self, names):
        print(f"  {'':<16}" + "".join(f"{n:>8}" for n in names))

    def row(self, label, cells):
        """cells: list of (name, printed, computed); strings compared as is."""
        bad = [(n, p, c) for n, p, c in cells if p != c]
        self.total += len(cells)
        self.bad += [(label, n, p, c) for n, p, c in bad]
        shown = "".join(f"{c:>8}" for _, _, c in cells)
        print(f"  {label:<16}{shown}  {'OK' if not bad else 'MISMATCH'}")
        for n, p, c in bad:
            print(f"      {n}: printed {p}, computed {c}")

    def figures(self, cells):
        """Prose figures: one labelled line each, computed [printed]."""
        for n, p, c in cells:
            self.total += 1
            ok = p == c
            if not ok:
                self.bad.append(("prose", n, p, c))
            print(f"  {n:<46} {c:>8} [{p}]  {'OK' if ok else 'MISMATCH'}")

    def skipped(self, text):
        print(f"  NOT CHECKED: {text}")


def load_data(name, data_dir):
    """Read one HuggingFace jsonl file, from data_dir if given, else download."""
    _, pd, _ = _libs()
    if data_dir:
        return pd.read_json(Path(data_dir) / name, lines=True)
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("Downloading the data requires huggingface_hub:")
        print("  uv run --with huggingface_hub --with pandas --with scipy \\")
        print("      python compute_dci.py --full")
        sys.exit(1)
    path = hf_hub_download(HF_REPO, name, repo_type="dataset")
    return pd.read_json(path, lines=True)


def check_table3(df, checks):
    """Table 3 (direct rating, 20 brands) and its prose figures.

    Originals: analysis 1 (pooled-variance t-test, pooled-SD Cohen's d, solo vs
    portfolio per brand) and analysis 5 (TOST, +/-1.0 DCI). The printed numbers
    were transcribed from the original's saved results (means to 2 decimals, t
    and d to 3, p and TOST p to 4) and then rounded half up to the printed
    precision, so the comparison applies that same two-step rounding.
    """
    np, _, stats = _libs()
    df = df[df["condition"].isin(["solo", "portfolio"])]
    print("Table 3 (DCI by brand and condition; 8 cells per brand)")
    checks.header(TABLE3_COLUMNS)
    stats_by_key, ses = {}, []
    for (portfolio, brand), g in df.groupby(["portfolio", "brand"]):
        solo = dci_matrix(g[g.condition == "solo"][DIMS].to_numpy())
        port = dci_matrix(g[g.condition == "portfolio"][DIMS].to_numpy())
        delta = float(np.mean(port) - np.mean(solo))
        t, p = stats.ttest_ind(port, solo)
        tost_p, is_eq = tost_analysis5(solo, port)
        csv = {
            "solo": round(float(np.mean(solo)), 2),
            "port": round(float(np.mean(port)), 2),
            "delta": round(delta, 2),
            "t": round(float(t), 3),
            "p": round(float(p), 4),
            "d": round(cohens_d_array(port, solo), 3),
            "tost": round(tost_p, 4),
        }
        stats_by_key[(portfolio, brand)] = (csv, float(p), is_eq)
        ses += [float(np.std(x, ddof=1) / np.sqrt(len(x))) for x in (solo, port)]
    for key, printed in PAPER_TABLE3.items():
        csv, _, is_eq = stats_by_key[key]
        computed = (
            fmt(csv["solo"], 1),
            fmt(csv["port"], 1),
            fmt(csv["delta"], 2, True),
            fmt(csv["t"], 2),
            fmt(csv["p"], 3),
            fmt(csv["d"], 2, True),
            fmt_tost(csv["tost"]),
            "Yes" if is_eq else "No",
        )
        cells = zip(TABLE3_COLUMNS, printed, computed)
        checks.row(key[1], [(c, pr, co) for c, pr, co in cells])
    deltas = [v[0]["delta"] for v in stats_by_key.values()]
    l_oreal = [v[0]["delta"] for k, v in stats_by_key.items() if k[0] == "L'Oreal"]
    p_values = [v[1] for v in stats_by_key.values()]
    prose = {
        "mean |delta|": fmt(np.mean(np.abs(deltas)), 2),
        "TOST-equivalent brands": str(sum(v[2] for v in stats_by_key.values())),
        "FDR-significant brands": str(int(bh_significant(p_values).sum())),
        "H6 range low": fmt(min(l_oreal), 2, True),
        "H6 range high": fmt(max(l_oreal), 2, True),
        "SE of cell means low": fmt(min(ses), 2),
        "SE of cell means high": fmt(max(ses), 2),
    }
    print("Table 3 prose figures (SE range: 40 cell means, SD / sqrt(n))")
    checks.figures([(k, PAPER_T3_PROSE[k], v) for k, v in prose.items()])
    print()


def check_table4(df, checks):
    """Table 4: nested, sequential (type I) variance decomposition of DCI.

    Rows: portfolio, brand within portfolio, model, condition, residual. Each
    factor's share is the drop in residual sum of squares when it is added to
    the factors above it, as a percentage of the total sum of squares, so the
    five shares sum to 100. Brand is nested in portfolio (each brand has one
    parent), so the marginal one-factor shares overlap and are not used.
    """
    np, pd, _ = _libs()
    df = df[df["condition"].isin(["solo", "portfolio"])]
    y = dci_matrix(df[DIMS].to_numpy())
    sst = float(((y - y.mean()) ** 2).sum())

    def rss(columns):
        x = [np.ones(len(df))]
        for c in columns:
            x.append(pd.get_dummies(df[c]).to_numpy(dtype=float))
        x = np.column_stack(x)
        beta = np.linalg.lstsq(x, y, rcond=None)[0]
        return float(((y - x @ beta) ** 2).sum())

    order = [
        ("Portfolio (parent company)", "portfolio"),
        ("Brand within portfolio", "brand"),
        ("Model", "model"),
        ("Condition (solo vs. portfolio)", "condition"),
    ]
    shares, used, prev = {}, [], sst
    for name, col in order:
        used.append(col)
        cur = rss(used)
        shares[name] = (prev - cur) / sst * 100
        prev = cur
    shares["Residual"] = prev / sst * 100
    nested = df.groupby("brand")["portfolio"].nunique().max() == 1
    print(f"Table 4 (nested, sequential shares of DCI variance; n = {len(df)})")
    checks.header(["Portf.", "Brand", "Model", "Cond.", "Resid."])
    cells = []
    for name, value in shares.items():
        shown = (
            "< .01" if name.startswith("Condition") and value < 0.01 else fmt(value, 1)
        )
        cells.append((name, PAPER_TABLE4[name], shown))
    checks.row("% variance", cells)
    rounded = [
        float(_half_up(v, 1)) for k, v in shares.items() if not k.startswith("Cond")
    ]
    prose = {
        "Brand identity (portfolio + brand within portfolio)": fmt(
            shares["Portfolio (parent company)"] + shares["Brand within portfolio"],
            1,
        ),
        "Shares of the printed rows sum to": f"{sum(rounded):.1f}",
    }
    checks.figures([(k, PAPER_T4_PROSE[k], v) for k, v in prose.items()])
    print(
        f"  brand nested in portfolio: {nested}; unrounded condition share "
        f"{shares['Condition (solo vs. portfolio)']:.4f}%; shares sum to "
        f"{sum(shares.values()):.4f}"
    )
    print()


def _load_turn_pairs(responses_dir):
    """Turn-1 and Turn-2 DCI per parsed multi-turn response (raw files)."""
    _, pd, _ = _libs()
    rows = []
    for f in sorted(Path(responses_dir).glob("*_multiturn_*.json")):
        rec = json.loads(f.read_text())
        if not rec.get("parse_success"):
            continue
        t1, t2 = rec.get("turn1_scores") or {}, rec.get("scores") or {}
        if all(d in t1 for d in DIMS) and all(d in t2 for d in DIMS):
            rows.append(
                (
                    rec["brand"],
                    float(dci_matrix([[t1[d] for d in DIMS]])[0]),
                    float(dci_matrix([[t2[d] for d in DIMS]])[0]),
                )
            )
    return pd.DataFrame(rows, columns=["brand", "t1", "t2"])


def check_table6(multiturn, responses_dir, checks):
    """Table 6 (multi-turn, FDR-significant brands) and the multi-turn prose.

    The published multiturn.jsonl holds Turn-2 scores only, so without
    --responses just the T2 DCI column can be checked. The Turn-1 scores are in
    the raw response files (field turn1_scores), public at RESPONSES_URL.
    Original: analysis 9 (paired t-test per brand, d = mean difference / SD of
    the differences, Benjamini-Hochberg across the 20 brand p-values rounded to
    4 decimals).
    """
    np, _, stats = _libs()
    print("Table 6 (multi-turn, Turn 1 before the reveal vs. Turn 2 after it)")
    t2_pub = (
        multiturn.assign(t2=dci_matrix(multiturn[DIMS].to_numpy()))
        .groupby("brand")["t2"]
        .mean()
    )
    if not responses_dir:
        checks.header(["T2 pub."])
        for brand, printed in PAPER_TABLE6.items():
            checks.row(
                brand,
                [("T2 DCI (published file)", printed[1], fmt(t2_pub[brand], 1))],
            )
        checks.skipped(
            "Turn-1 DCI, delta, d, p, FDR set and the multi-turn prose figures need "
            "the Turn-1 scores; pass --responses DIR (raw responses, "
            f"{RESPONSES_URL})."
        )
        print()
        return
    pairs = _load_turn_pairs(responses_dir)
    checks.header(["T1", "T2 raw", "T2 pub.", "Delta", "d", "p"])
    per = {}
    for brand, g in pairs.groupby("brand"):
        diff = (g.t2 - g.t1).to_numpy()
        per[brand] = {
            "n": len(g),
            "t1": g.t1.mean(),
            "t2": g.t2.mean(),
            "delta": g.t2.mean() - g.t1.mean(),
            "p": round(float(stats.ttest_rel(g.t2, g.t1).pvalue), 4),
            "d": float(diff.mean() / diff.std(ddof=1)),
            "se1": float(g.t1.std(ddof=1) / np.sqrt(len(g))),
            "se2": float(g.t2.std(ddof=1) / np.sqrt(len(g))),
        }
    names = sorted(per)
    sig = bh_significant([per[b]["p"] for b in names])
    sig_set = sorted(b for b, s in zip(names, sig) if s)
    for brand, printed in PAPER_TABLE6.items():
        s = per[brand]
        checks.row(
            brand,
            [
                ("T1 DCI", printed[0], fmt(s["t1"], 1)),
                ("T2 DCI (raw)", printed[1], fmt(s["t2"], 1)),
                ("T2 DCI (published file)", printed[1], fmt(t2_pub[brand], 1)),
                ("Delta", printed[2], fmt(s["delta"], 2, True)),
                ("d", printed[3], fmt(s["d"], 2)),
                ("p", "<.001", "<.001" if s["p"] < 0.001 else fmt(s["p"], 3)),
            ],
        )
    all_delta = np.array([per[b]["delta"] for b in names])
    others = np.array([per[b]["delta"] for b in names if b not in PAPER_TABLE6])
    t_b, p_b = stats.ttest_1samp(all_delta, 0)
    t_pool, p_pool = stats.ttest_rel(pairs.t2, pairs.t1)
    diff_pool = (pairs.t2 - pairs.t1).to_numpy()
    cell_se = [per[b][k] for b in PAPER_TABLE6 for k in ("se1", "se2")]
    prose = {
        "FDR-significant brands": ", ".join(sig_set),
        "Mean delta over the 20 brands": fmt(all_delta.mean(), 2, True),
        "SD of the 20 per-brand deltas": fmt(all_delta.std(ddof=1), 2),
        "One-sample t(19) of the 20 deltas": fmt(t_b, 2),
        "p of that t": fmt(p_b, 3),
        "d of that mean (mean / SD)": fmt(all_delta.mean() / all_delta.std(ddof=1), 2),
        "Mean delta of the 16 other brands": fmt(others.mean(), 2, True),
        "Pooled mean delta over all response pairs": fmt(diff_pool.mean(), 2),
        "Pooled paired t": fmt(t_pool, 2),
        "Pooled p": fmt(p_pool, 3),
        "Pooled d": fmt(diff_pool.mean() / diff_pool.std(ddof=1), 2),
        "SE of the 8 table cell means low": fmt(min(cell_se), 2),
        "SE of the 8 table cell means high": fmt(max(cell_se), 2),
    }
    print(
        f"Table 6 prose figures ({len(pairs)} parsed pairs, "
        f"{len(names)} brands; SE range is over the 8 cell means shown, SD / sqrt(n))"
    )
    checks.figures([(k, PAPER_T6_PROSE[k], v) for k, v in prose.items()])
    print()


def check_table7(df, checks):
    """Table 7: published-brand extension, DCI by Equation 2.

    Only the 10 brands rated under both conditions are tested (65 solo and 65
    portfolio observations each, 1,300 in all). Statistics follow analysis 1
    (pooled-variance t-test, pooled-SD Cohen's d) and analysis 5 (TOST +/-1.0);
    the values are rounded once, half up, from the unrounded statistics.
    """
    np, _, stats = _libs()
    df = df[
        df["brand"].isin(PAPER_TABLE7) & df["condition"].isin(["solo", "portfolio"])
    ]
    print(f"Table 7 (published brands, Equation 2; n = {len(df)} observations)")
    checks.header(["Solo", "Port", "Delta", "d"])
    p_values, equiv, solo_means, ses, tost_p, p_by = [], [], [], [], {}, {}
    for brand, printed in PAPER_TABLE7.items():
        g = df[df.brand == brand]
        solo = dci_matrix(g[g.condition == "solo"][DIMS].to_numpy())
        port = dci_matrix(g[g.condition == "portfolio"][DIMS].to_numpy())
        delta = float(np.mean(port) - np.mean(solo))
        d = cohens_d_array(port, solo)
        p = float(stats.ttest_ind(port, solo).pvalue)
        tp, is_eq = tost_analysis5(solo, port)
        checks.row(
            brand,
            [
                ("Solo DCI", printed[0], fmt(np.mean(solo), 1)),
                ("Port DCI", printed[1], fmt(np.mean(port), 1)),
                ("Delta", printed[2], fmt(delta, 2, True)),
                ("d", printed[3], fmt(d, 2, True)),
            ],
        )
        p_values.append(p)
        p_by[brand] = p
        equiv.append(is_eq)
        tost_p[brand] = tp
        solo_means.append(float(np.mean(solo)))
        ses += [float(np.std(x, ddof=1) / np.sqrt(len(x))) for x in (solo, port)]
    prose = {
        "Observations tested": str(len(df)),
        "FDR-significant brands": str(int(bh_significant(p_values).sum())),
        "TOST-equivalent brands": str(int(sum(equiv))),
        "TOST p of Colgate": fmt(tost_p["Colgate"], 3),
        "Audi p": fmt(p_by["Audi"], 3),
        "Audi BH threshold (smallest of 10 p)": fmt(0.05 / len(p_values), 3),
        "Pepsi p": fmt(p_by["Pepsi"], 3),
        "Solo DCI means low": fmt(min(solo_means), 1),
        "Solo DCI means high": fmt(max(solo_means), 1),
        "SE of cell means low": fmt(min(ses), 2),
        "SE of cell means high": fmt(max(ses), 2),
    }
    print("Table 7 prose figures (SE range is over the 20 cell means, SD / sqrt(n))")
    checks.figures([(k, PAPER_T7_PROSE[k], v) for k, v in prose.items()])
    non_eq = [b for b, e in zip(PAPER_TABLE7, equiv) if not e]
    print(f"  not TOST-equivalent: {', '.join(non_eq) or 'none'}")
    print()


def check_table5(df, checks):
    """Table 5: sub-group analysis by training tradition.

    Method (the same as the original R20 analysis, `analyze_portfolio.py`,
    analysis 12): for each tradition, pool that tradition's models' direct
    ratings, take the mean 8-dimension profile per brand and condition, compute
    the DCI of each mean profile, and test the 20 per-brand differences
    (portfolio minus solo) with a one-sample t-test against 0; d is the mean
    difference over its standard deviation.
    """
    _, _, stats = _libs()
    df = df[df["condition"].isin(["solo", "portfolio"])]
    print("Table 5 (Delta DCI / d / p; paper value in brackets)")
    ses = []
    for tradition, models in TRADITIONS.items():
        sub = df[df["model"].isin(models)]
        means = sub.groupby(["condition", "portfolio", "brand"])[DIMS].mean()
        dci = means.apply(lambda row: compute_dci(list(row.values)), axis=1)
        deltas = (dci.loc["portfolio"] - dci.loc["solo"]).dropna()
        mean_delta = deltas.mean()
        ses.append(deltas.std() / len(deltas) ** 0.5)
        d = mean_delta / deltas.std() if deltas.std() > 0 else 0.0
        p = stats.ttest_1samp(deltas.values, 0).pvalue
        pd_, pdd, pp = PAPER_TABLE5[tradition]
        match = round(mean_delta, 2) == pd_ and round(d, 2) == pdd and round(p, 3) == pp
        checks.total += 3
        if not match:
            checks.bad.append((tradition, "Table 5 row", (pd_, pdd, pp), None))
        print(
            f"  {tradition:<9} {mean_delta:+.2f} [{pd_:+.2f}]  "
            f"{d:+.2f} [{pdd:+.2f}]  {p:.3f} [{pp:.3f}]  {'OK' if match else 'MISMATCH'}"
        )
    # Notes: SE of each tradition-level mean delta (SD of the 20 brand deltas / sqrt(20)).
    for label, value, printed in (
        ("low", min(ses), PAPER_TABLE5_SE[0]),
        ("high", max(ses), PAPER_TABLE5_SE[1]),
    ):
        ok = round(value, 2) == printed
        checks.total += 1
        if not ok:
            checks.bad.append(("Table 5", f"SE {label}", printed, value))
        print(
            f"  SE of tradition mean deltas {label:<5} {value:.2f} [{printed:.2f}]  "
            f"{'OK' if ok else 'MISMATCH'}"
        )
    print()


def full_mode(data_dir=None, responses_dir=None) -> None:
    """
    Full mode: reproduces Tables 3, 4, 5, 6 and 7 from the archived data and
    checks every printed cell, plus the prose figures that depend on them (mean
    |delta DCI|, the variance shares, the multi-turn mean delta, the Table 7
    counts), against the values hard-coded above. Prints OK or MISMATCH per row
    and a final line.

    Data: main_experiment.jsonl (Tables 3, 4, 5), multiturn.jsonl (Table 6,
    Turn 2 only) and published_brands.jsonl (Table 7), read from HuggingFace
    (10.57967/hf/8380) or from --data-dir. Table 6's Turn-1 cells need the raw
    response files (--responses DIR); without them only Table 6's Turn-2 column
    is checked and the script says so.

    Requires: huggingface_hub (unless --data-dir), pandas, scipy.
    """
    checks = Checks()
    main_df = load_data("main_experiment.jsonl", data_dir)
    print(f"Main experiment: {len(main_df)} rows, {main_df['brand'].nunique()} brands")
    print()
    check_table3(main_df, checks)
    check_table4(main_df, checks)
    check_table5(main_df, checks)
    check_table6(load_data("multiturn.jsonl", data_dir), responses_dir, checks)
    check_table7(load_data("published_brands.jsonl", data_dir), checks)
    if checks.bad:
        print(f"{len(checks.bad)} of {checks.total} checks MISMATCH:")
        for item in checks.bad:
            print(f"  {item}")
        sys.exit(1)
    scope = "" if responses_dir else " (Table 6 Turn-1 cells not checked)"
    print(f"All {checks.total} checks match{scope}.")


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--full", action="store_true", help="reproduce Tables 3-7")
    parser.add_argument(
        "--responses",
        metavar="DIR",
        help="folder of raw response files (sbt-papers r20-portfolio-ai/responses); "
        "needed for Table 6's Turn-1 cells",
    )
    parser.add_argument(
        "--data-dir",
        metavar="DIR",
        help="folder holding the HuggingFace jsonl files, instead of downloading",
    )
    args = parser.parse_args(argv)
    if args.full:
        full_mode(args.data_dir, args.responses)
    else:
        stub_mode()


if __name__ == "__main__":
    main()
