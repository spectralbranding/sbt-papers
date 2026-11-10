"""Companion computation script for paper 2026r (dimension justification, SBT).

Reproduces the three data-free reference nulls the paper prints in its RQ1 and RQ3
discussion (Experiments 1 and 3, and the Companion Computation Script subsection).
No source profiles are needed: each null depends only on the number of models (22)
and, for the cosine null, on DCI's printed mean and SD.

Nulls
-----
1. Random re-ranking, mean absolute rank displacement (paper: Experiment 1 text and
   Summary). A uniformly random permutation of 22 model ranks is compared with the
   identity ranking; the statistic is mean(|rank_i - i|). Closed form (n^2-1)/(3n) =
   7.32 at n = 22; 95% interval from 100,000 permutations. One-sided p-values are the
   lower-tail share of draws at or below the observed displacement: Economic drop-one
   3.55 (paper p < .001) and worst computable pair 5.00 (paper p = .014).
2. Cosine reference (paper: Experiment 1 text). Two independent 22-vectors with DCI's
   mean (.356) and SD (.029); expected cosine m^2/(m^2+s^2) = .993, share of
   200,000 simulated pairs with cosine above .994 (paper: 45%).
   Reading chosen: entries are iid uniform with mean .356 and SD .029 (half-width
   .029 * sqrt(3)), the reading that reproduces the printed 45%; iid normal entries
   give about 48%. The analytic .993 is the same under either reading.
3. Exchangeable variance-share null (paper: Experiment 3, RQ3). 22 models x 8
   dimensions of iid standard-normal scores (equal true variance); the share of each
   dimension is its sample variance across the 22 models over the sum of the eight
   variances. Statistics: max/min share ratio, spread (max - min share, percentage
   points), minimum share. Observed values (Table 4): ratio 3.46, spread 13.3 points,
   minimum 5.4%. p-values are the upper tail for ratio and spread, lower tail for the
   minimum share.

Reproducibility
---------------
SEED = 42, numpy default_rng, a fresh generator per null so the nulls do not depend
on each other's draw order. Draw counts as in the paper: 100,000 permutations,
200,000 cosine pairs, 100,000 variance-share draws.

Run from the paper root (the folder that holds paper.md and code/):

    uv run --with numpy python code/reference_nulls.py

Monte Carlo agreement is asserted to the precision the paper prints (two decimals
for displacement and ratio, three for p-values, whole percent for the 45%).
"""

import numpy as np

SEED = 42
N_MODELS = 22
N_PERM = 100_000
N_PAIRS = 200_000
N_SHARE = 100_000
DCI_MEAN, DCI_SD = 0.356, 0.029
N_DIMS = 8


def check(label, computed, printed, tol, unit=""):
    """Print computed beside printed and assert agreement within tol."""
    ok = abs(computed - printed) <= tol
    print(
        f"{label:<44} paper {printed:>8.3f}  computed {computed:>8.3f}{unit}  "
        f"{'PASS' if ok else 'FAIL'}"
    )
    assert ok, f"{label}: computed {computed} vs paper {printed} (tol {tol})"


def rank_displacement_null():
    n = N_MODELS
    rng = np.random.default_rng(SEED)
    perms = np.argsort(rng.random((N_PERM, n)), axis=1)
    disp = np.abs(perms - np.arange(n)).mean(axis=1)
    lo, hi = np.percentile(disp, [2.5, 97.5])
    print("Null 1: random re-ranking, mean absolute rank displacement (n = 22)")
    check("expected displacement (n^2-1)/(3n)", (n * n - 1) / (3 * n), 7.32, 0.005)
    check("95% interval, lower", lo, 5.27, 0.01)
    check("95% interval, upper", hi, 9.27, 0.01)
    p_econ = (disp <= 3.55).mean()
    p_pair = (disp <= 5.00).mean()
    print(f"{'p, Economic drop-one (3.55)':<44} paper  < .001  computed {p_econ:>8.5f}")
    assert p_econ < 0.001
    check("p, worst computable pair (5.00)", p_pair, 0.014, 0.001)


def cosine_null():
    m, s = DCI_MEAN, DCI_SD
    rng = np.random.default_rng(SEED)
    half = s * np.sqrt(3.0)
    x = rng.uniform(m - half, m + half, (N_PAIRS, N_MODELS))
    y = rng.uniform(m - half, m + half, (N_PAIRS, N_MODELS))
    cos = (x * y).sum(axis=1) / np.sqrt((x * x).sum(axis=1) * (y * y).sum(axis=1))
    print("Null 2: cosine between independent DCI-like vectors")
    check("expected cosine m^2/(m^2+s^2)", m * m / (m * m + s * s), 0.993, 0.0005)
    check("simulated mean cosine", cos.mean(), 0.993, 0.001)
    check("share of pairs with cosine > .994", (cos > 0.994).mean(), 0.45, 0.005)


def variance_share_null():
    rng = np.random.default_rng(SEED)
    x = rng.standard_normal((N_SHARE, N_MODELS, N_DIMS))
    var = x.var(axis=1, ddof=1)
    share = var / var.sum(axis=1, keepdims=True)
    ratio = share.max(axis=1) / share.min(axis=1)
    spread = 100 * (share.max(axis=1) - share.min(axis=1))
    smin = share.min(axis=1)
    lo, hi = np.percentile(ratio, [2.5, 97.5])
    print("Null 3: exchangeable variance-share null (22 models x 8 dimensions)")
    check("median max/min share ratio", np.median(ratio), 2.40, 0.01)
    check("95% interval, lower", lo, 1.55, 0.01)
    check("95% interval, upper", hi, 4.39, 0.01)
    check("median spread (points)", np.median(spread), 10.6, 0.05)
    check("p, observed ratio 3.46 (upper tail)", (ratio >= 3.46).mean(), 0.105, 0.002)
    check("p, observed spread 13.3 (upper tail)", (spread >= 13.3).mean(), 0.209, 0.002)
    check("p, observed minimum 5.4% (lower tail)", (smin <= 0.054).mean(), 0.067, 0.002)


def main():
    rank_displacement_null()
    print()
    cosine_null()
    print()
    variance_share_null()
    print("\nAll reference-null assertions passed.")


if __name__ == "__main__":
    main()
