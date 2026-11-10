"""Companion computation for R19 (2026aa): the four correction-pass derivations.

Paper: "Optimal Response Formats for AI Brand Perception Measurement: Evidence
for a J-Shaped Rate-Distortion Curve" (2026aa).

These derivations are closed-form. They need no API calls and no dataset; the
only inputs are values the paper itself prints (Table 3 CVs, Table 4 columns,
the Welch df, group sizes) and the five canonical SBT profiles that
`analysis.py` also uses. Every figure is computed, printed next to the paper's
printed value, and asserted to the printed precision.

Figures reproduced, with paper location:

  1. H1 permutation floor (Results, "H1: Monotonic Rate-Distortion Shape")
     - 5! = 120 permutation points for a Spearman test at n = 5
     - minimum two-tailed p = 2/120 = .0167 (attained only at rho = -1)
     - Bonferroni threshold alpha = .05/17 = .00294
     - floor / alpha = 5.67
  2. H4 t = 1.97 d relation (Results, "H4: Architectural Separation")
     - t = d * sqrt(n1 * n2 / (n1 + n2)) = 1.97 d at n1 = 6, n2 = 11
     - two-sided p < .05 at Welch df = 11.4 requires |d| > 1.11
  3. H2 averaging change (Results, "H2: Common Rate-Distortion Curve")
     - mean cross-model CV over R1-R5 = .140; over R1-R4 = .171
     - difference attributable to the R5 cell = .031
  4. Uniform-vector baseline (Table 4 Notes)
     - total variation distance from the uniform vector to each canonical
       profile: IKEA .071, Patagonia .081, Hermes .095, Erewhon .153, Tesla .170
     - Spearman rho = .900 against the R2 column, rho = -.900 against the
       R1-to-R2 reduction column

The Table 3 and Table 4 values used as inputs are the paper's printed values;
`analysis.py` reproduces them from the raw dataset (DOI 10.57967/hf/8362).

Random seed: SEED = 42. Nothing here is stochastic (the H1 floor is an exact
enumeration of all 120 permutations), so the seed does not affect any value.

Run from the paper root (the folder that holds paper.md and code/):
    uv run --with numpy --with scipy python code/correction_pass_derivations.py

Exits 0 if every assertion passes; raises AssertionError otherwise.
"""

from __future__ import annotations

import itertools
import math
import random

import numpy as np
from scipy import stats

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# Canonical SBT 8-D reference profiles (raw 0-10 scale; same as analysis.py).
CANONICAL_RAW = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
}

# Paper Table 3: cross-model CV by rate condition (printed values).
PAPER_CV = {"R1": 0.210, "R2": 0.132, "R3": 0.143, "R4": 0.198, "R5": 0.018}

# Paper Table 4: R2 mean distortion and R1-to-R2 drop (%) by brand (printed).
PAPER_R2 = {
    "Patagonia": 0.055,
    "IKEA": 0.057,
    "Hermes": 0.062,
    "Erewhon": 0.118,
    "Tesla": 0.138,
}
PAPER_DROP_PCT = {
    "Patagonia": 66.7,
    "IKEA": 65.9,
    "Hermes": 56.9,
    "Erewhon": 35.9,
    "Tesla": 22.0,
}
PAPER_TV_UNIFORM = {
    "IKEA": 0.071,
    "Patagonia": 0.081,
    "Hermes": 0.095,
    "Erewhon": 0.153,
    "Tesla": 0.170,
}

N_MODELS = 17
N_RATE = 5
ALPHA_FAMILY = 0.05

CHECKS: list[tuple[str, str, str, str]] = []


def check(label: str, paper: str, computed: str, ok: bool, near: bool = False) -> None:
    """Print a figure beside the paper's value and record the verdict.

    PASS = equal at printed precision. DISCREP = differs by one unit in the last printed digit
    (reported, not hidden). FAIL = anything else; main() asserts there are none.
    """
    status = "PASS" if ok else ("DISCREP" if near else "FAIL")
    CHECKS.append((label, paper, computed, status))
    print(f"  {label:<46} paper {paper:>7}  computed {computed:>7}  {status}")


def spearman_rho_exact(ranks_a: tuple[int, ...], ranks_b: tuple[int, ...]) -> float:
    """Spearman rho for tie-free rank vectors: 1 - 6 sum d^2 / (n (n^2 - 1))."""
    n = len(ranks_a)
    d2 = sum((a - b) ** 2 for a, b in zip(ranks_a, ranks_b))
    return 1 - 6 * d2 / (n * (n * n - 1))


def figure_1_h1_floor() -> None:
    print("1. H1 permutation floor (n = 5 rate conditions)")
    base = tuple(range(1, N_RATE + 1))
    rhos = [spearman_rho_exact(base, perm) for perm in itertools.permutations(base)]
    n_perm = len(rhos)
    n_extreme = sum(1 for r in rhos if abs(r) >= 1 - 1e-12)
    p_min = n_extreme / n_perm
    alpha = ALPHA_FAMILY / N_MODELS
    ratio = p_min / alpha
    check(
        "permutation points, 5!", "120", str(n_perm), n_perm == 120 == math.factorial(5)
    )
    check("extreme permutations (rho = +/-1)", "2", str(n_extreme), n_extreme == 2)
    check(
        "minimum two-tailed p = 2/120",
        ".0167",
        f"{p_min:.4f}",
        f"{p_min:.4f}" == "0.0167",
    )
    check(
        "Bonferroni alpha = .05/17",
        ".00294",
        f"{alpha:.5f}",
        f"{alpha:.5f}" == "0.00294",
    )
    check("floor / alpha", "5.67", f"{ratio:.2f}", f"{ratio:.2f}" == "5.67")
    # The floor is above the threshold, so H1 cannot be cleared at any data value.
    assert p_min > alpha


def figure_2_h4_t_d_relation() -> None:
    print("2. H4 t = 1.97 d relation (n1 = 6, n2 = 11, Welch df = 11.4)")
    n1, n2, welch_df = 6, 11, 11.4
    factor = math.sqrt(n1 * n2 / (n1 + n2))
    t_crit = float(stats.t.ppf(0.975, welch_df))
    d_min = t_crit / factor
    d_min_df11 = float(stats.t.ppf(0.975, 11)) / factor
    check(
        "sqrt(n1 n2 / (n1 + n2)) = sqrt(66/17)",
        "1.97",
        f"{factor:.2f}",
        f"{factor:.2f}" == "1.97",
    )
    # The paper prints 1.11 "at the reported Welch df of 11.4": exact df 11.4 gives
    # 2.1916 / 1.9704 = 1.1123 -> 1.11. Integer df 11 would give 1.12 (1.1170);
    # earlier versions printed that figure, and the cross-check below keeps it.
    check(
        "|d| needed for p < .05 at df 11.4",
        "1.11",
        f"{d_min:.2f}",
        f"{d_min:.2f}" == "1.11",
    )
    print(
        f"    (critical t at df 11.4 = {t_crit:.3f}; |d| at integer df 11 = {d_min_df11:.2f})"
    )
    assert f"{d_min_df11:.2f}" == "1.12"
    assert (
        d_min > 0.50
    )  # the pre-registered |d| > .50 floor sits inside the excluded region


def figure_3_h2_averaging() -> None:
    print("3. H2 mean cross-model CV: R1-R5 versus R1-R4")
    all5 = float(np.mean([PAPER_CV[r] for r in ("R1", "R2", "R3", "R4", "R5")]))
    four = float(np.mean([PAPER_CV[r] for r in ("R1", "R2", "R3", "R4")]))
    pull = four - all5
    check("mean CV over R1-R5", ".140", f"{all5:.3f}", f"{all5:.3f}" == "0.140")
    check("mean CV over R1-R4", ".171", f"{four:.3f}", f"{four:.3f}" == "0.171")
    check("pull from the R5 cell", ".031", f"{pull:.3f}", f"{pull:.3f}" == "0.031")
    assert all5 < 0.15 < four  # the verdict flips across the pre-registered threshold


def figure_4_uniform_baseline() -> None:
    print("4. Uniform-vector total variation baseline")
    uniform = np.full(8, 1 / 8)
    tv = {}
    for brand, raw in CANONICAL_RAW.items():
        w = np.asarray(raw) / np.sum(raw)
        tv[brand] = 0.5 * float(np.sum(np.abs(uniform - w)))
    for brand in PAPER_TV_UNIFORM:
        printed = f"{PAPER_TV_UNIFORM[brand]:.3f}"
        check(
            f"TV(uniform, {brand})",
            printed.lstrip("0"),
            f"{tv[brand]:.3f}".lstrip("0"),
            f"{tv[brand]:.3f}" == printed,
            near=abs(tv[brand] - PAPER_TV_UNIFORM[brand]) < 0.0015,
        )
    brands = list(PAPER_R2)
    tv_vec = [tv[b] for b in brands]
    r2_vec = [PAPER_R2[b] for b in brands]
    drop_vec = [PAPER_DROP_PCT[b] for b in brands]
    rho_r2 = float(stats.spearmanr(tv_vec, r2_vec).statistic)
    rho_drop = float(stats.spearmanr(tv_vec, drop_vec).statistic)
    check(
        "Spearman rho, TV vs R2 column",
        ".900",
        f"{rho_r2:.3f}".lstrip("0"),
        f"{rho_r2:.3f}" == "0.900",
    )
    check(
        "Spearman rho, TV vs R1-to-R2 reduction",
        "-.900",
        f"{rho_drop:.3f}".replace("0.", "."),
        f"{rho_drop:.3f}" == "-0.900",
    )


def main() -> None:
    print("R19 (2026aa) correction-pass derivations  (SEED = 42; nothing stochastic)")
    figure_1_h1_floor()
    figure_2_h4_t_d_relation()
    figure_3_h2_averaging()
    figure_4_uniform_baseline()
    n_pass = sum(1 for c in CHECKS if c[3] == "PASS")
    discrep = [c for c in CHECKS if c[3] == "DISCREP"]
    failed = [c for c in CHECKS if c[3] == "FAIL"]
    print(f"\n{n_pass} / {len(CHECKS)} figures reproduce at printed precision.")
    for label, paper, computed, _ in discrep:
        print(
            f"  DISCREPANCY (one unit, last digit): {label}: paper {paper}, computed {computed}"
        )
    assert not failed, f"mismatches: {[c[0] for c in failed]}"


if __name__ == "__main__":
    main()
