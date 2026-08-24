"""Reference implementation of the brand-space metrics of paper 2026d (R1).

Paper: "Brand Space Geometry: A Formal Metric for Multi-Dimensional Brand
Perception" (Zharnikov 2026). This module implements, with NumPy, the three
metrics the paper defines plus the closed-form null baseline:

  * ``clr`` / ``ilr``       -- centered / isometric log-ratio transforms on R^8_+
  * ``aitchison_distance``  -- Aitchison metric on the brand signal space
                               B = R^8_+  (Definition 1, Theorem 1)
  * ``fisher_rao_distance`` -- Fisher-Rao metric on the observer simplex
                               O = Delta^7  (Definition 2, Theorem 2):
                               d_FR(p, q) = 2 * arccos(sum_i sqrt(p_i q_i))
  * ``observer_distance``   -- observer-dependent (warped) brand distance
                               d_w(s_A, s_B) (Proposition 3)
  * ``combined_distance``   -- warped product metric D on P (Definition 3)
  * ``expected_observer_distance_sq`` -- Theorem 5(i) closed form
                               E_w[d_w^2] = (1/8) ||clr(s_A) - clr(s_B)||^2

Run command (reproduces the paper's null baseline and the 1/256 compression):

    uv run python code/metrics.py

The ``__main__`` smoke test reproduces the paper's printed numbers with a fixed
seed: the ~.44 concentration null baseline sqrt(7/36) for random observer pairs
at n = 8, the 1/256 positive-octant volume fraction, the Theorem 5(i) closed
form against a Monte Carlo estimate, the case-study Aitchison distances of
Table 6, and (added 2026-08-24 with the corrected paper) the observer-dependent
distances and ordering reversals of Table 7, the Fisher-Rao contraction under
dimension merging, and the tau-classification of the case-study pairs.

Those assertions compare the paper's printed values against the values this
module computes. They catch transcription drift between paper and script; they
are NOT an independent verification that the computations are correct.
"""

from __future__ import annotations

import numpy as np

N_DIM = 8  # SBT eight-dimensional signal architecture


def _as_positive_array(s) -> np.ndarray:
    """Return ``s`` as a float array, asserting strict positivity (R^n_+)."""
    arr = np.asarray(s, dtype=float)
    if np.any(arr <= 0):
        raise ValueError("brand emission profiles must lie in the open orthant R^n_+")
    return arr


def clr(s) -> np.ndarray:
    """Centered log-ratio transform of a composition ``s`` in R^n_+.

    clr(s)_i = log(s_i / g(s)) where g(s) is the geometric mean. The image
    lies on the zero-sum hyperplane of R^n.
    """
    arr = _as_positive_array(s)
    log_arr = np.log(arr)
    return log_arr - log_arr.mean()


def _ilr_basis(n: int) -> np.ndarray:
    """Return an (n-1, n) Helmert-style orthonormal contrast matrix Psi.

    Satisfies ``Psi @ Psi.T = I_{n-1}`` and ``Psi @ ones = 0`` (Egozcue 2003).
    The specific basis does not affect Aitchison distances.
    """
    psi = np.zeros((n - 1, n))
    for i in range(1, n):
        coef = np.sqrt(i / (i + 1.0))
        psi[i - 1, :i] = 1.0 / i
        psi[i - 1, i] = -1.0
        psi[i - 1, : i + 1] *= coef
    return psi


def ilr(s) -> np.ndarray:
    """Isometric log-ratio transform of ``s`` in R^n_+ into R^{n-1}."""
    arr = _as_positive_array(s)
    return _ilr_basis(arr.size) @ clr(arr)


def aitchison_distance(s_a, s_b) -> float:
    """Aitchison distance d_B(s_A, s_B) on the brand signal space (Definition 1).

    Equal to the Euclidean distance between clr (or ilr) images; the two agree.
    """
    return float(np.linalg.norm(clr(s_a) - clr(s_b)))


def _as_simplex(w) -> np.ndarray:
    """Return ``w`` as a float probability vector on the open simplex."""
    arr = np.asarray(w, dtype=float)
    if np.any(arr < 0):
        raise ValueError("observer weights must be non-negative")
    total = arr.sum()
    if total <= 0:
        raise ValueError("observer weights must sum to a positive value")
    return arr / total


def fisher_rao_distance(w_a, w_b) -> float:
    """Fisher-Rao (Rao) distance on the observer simplex (Definition 2).

    d_FR(p, q) = 2 * arccos(sum_i sqrt(p_i q_i)), the geodesic distance under
    the square-root embedding w -> 2 sqrt(w) onto S^{n-1}_+.
    """
    p = _as_simplex(w_a)
    q = _as_simplex(w_b)
    bhattacharyya = np.sum(np.sqrt(p * q))
    # Guard arccos domain against floating-point overshoot of 1.0.
    bhattacharyya = min(1.0, float(bhattacharyya))
    return 2.0 * float(np.arccos(bhattacharyya))


def observer_distance(w, s_a, s_b) -> float:
    """Observer-dependent brand distance d_w(s_A, s_B) for a fixed observer w.

    d_w(s_A, s_B) = sqrt( sum_k w_k (clr_k(s_A) - clr_k(s_B))^2 )  (Proposition 3).
    """
    weights = _as_simplex(w)
    delta = clr(s_a) - clr(s_b)
    return float(np.sqrt(np.sum(weights * delta**2)))


def combined_distance(w_a, s_a, w_b, s_b) -> float:
    """Warped product metric D on the combined space P (Definition 3).

    D^2 = d_FR^2(w_A, w_B) + sum_k wbar_k (clr_k(s_A) - clr_k(s_B))^2 with
    wbar_k = (w_{A,k} + w_{B,k}) / 2.
    """
    p = _as_simplex(w_a)
    q = _as_simplex(w_b)
    wbar = 0.5 * (p + q)
    delta = clr(s_a) - clr(s_b)
    brand_term = float(np.sum(wbar * delta**2))
    return float(np.sqrt(fisher_rao_distance(p, q) ** 2 + brand_term))


def expected_observer_distance_sq(s_a, s_b) -> float:
    """Theorem 5(i): E_w[d_w^2] under uniform observers on Delta^{n-1}.

    Equals (1/n) ||clr(s_A) - clr(s_B)||^2 since E[w_k] = 1/n for the symmetric
    Dirichlet(1, ..., 1) distribution.
    """
    delta = clr(s_a) - clr(s_b)
    return float(np.sum(delta**2) / delta.size)


def expected_simplex_pair_distance_sq(n: int = N_DIM) -> float:
    """Theorem 4: E[||w_A - w_B||^2] = 2(n-1)/(n(n+1)) for uniform simplex points.

    For n = 8 this is 7/36 ~= 0.1944 (exact).
    """
    return float(2.0 * (n - 1) / (n * (n + 1)))


def expected_simplex_pair_distance(n: int = N_DIM) -> float:
    """Null baseline sqrt(E[||w_A - w_B||^2]) for observer pairwise distance.

    Theorem 4 reports the root-mean-square distance sqrt(2(n-1)/(n(n+1))); for
    n = 8 this is sqrt(7/36) ~= 0.4410. By Jensen's inequality this exceeds the
    plain mean distance E[||w_A - w_B||] (~0.424 by Monte Carlo); the paper's
    ".44" baseline is the root-mean-square value.
    """
    return float(np.sqrt(expected_simplex_pair_distance_sq(n)))


def positive_octant_fraction(n: int = N_DIM) -> float:
    """Proposition 4: fraction of S^{n-1} occupied by its positive octant = 1/2^n."""
    return 1.0 / (2.0**n)


CANONICAL_NAMES = ("Hermes", "IKEA", "Patagonia", "Erewhon", "Tesla")
CANONICAL_PROFILES = (
    (9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5),
    (8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0),
    (6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5),
    (7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5),
    (7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0),
)
W_AESTHETE = (0.25, 0.15, 0.05, 0.20, 0.10, 0.05, 0.15, 0.05)
W_PRAGMATIST = (0.05, 0.05, 0.10, 0.15, 0.05, 0.35, 0.05, 0.20)


def merge_dimensions(w, i: int, j: int) -> np.ndarray:
    """Coarse-grain a simplex point by merging categories ``i`` and ``j``."""
    w = np.asarray(w, dtype=float)
    keep = [x for k, x in enumerate(w) if k not in (i, j)]
    return np.array(keep + [w[i] + w[j]])


def split_dimension(w, i: int, frac: float = 0.5) -> np.ndarray:
    """Congruent refinement: split category ``i`` with the same kernel for all."""
    w = list(np.asarray(w, dtype=float))
    mass = w.pop(i)
    return np.array(w + [frac * mass, (1.0 - frac) * mass])


def jnd_threshold(weber_fraction: float, n: int = N_DIM) -> float:
    """Definition 4 threshold tau(k) = sqrt((n-1)/n^2) * ln(1 + k).

    One just-noticeable difference is a factor (1 + k) on a single dimension.
    In clr coordinates that shifts the profile by ln(1+k) along a direction of
    norm sqrt((n-1)/n), and averaging over uniform observer weights (E[w_k] =
    1/n) gives E_w[d_w^2] = ((n-1)/n^2) ln^2(1+k).
    """
    return float(np.sqrt((n - 1) / n**2) * np.log1p(weber_fraction))


def critical_weber_fraction(s_a, s_b, n: int = N_DIM) -> float:
    """Weber fraction at which a pair stops being meaningfully differentiated."""
    rms = np.sqrt(expected_observer_distance_sq(s_a, s_b))
    return float(np.expm1(rms / np.sqrt((n - 1) / n**2)))


def _pair_indices(m: int):
    return [(i, j) for i in range(m) for j in range(i + 1, m)]


def _smoke_test() -> None:
    rng = np.random.default_rng(20260326)

    # 1. Null baseline sqrt(7/36) ~= 0.4410 (Theorem 4). The closed form is the
    #    root-mean-square distance E[||.||^2] = 7/36 (exact); validate that
    #    squared expectation against Monte Carlo, then report the sqrt baseline.
    draws = rng.dirichlet(np.ones(N_DIM), size=(2, 200_000))
    mc_sq = (np.linalg.norm(draws[0] - draws[1], axis=1) ** 2).mean()
    closed_sq = expected_simplex_pair_distance_sq(N_DIM)
    closed_baseline = expected_simplex_pair_distance(N_DIM)
    print(f"Null baseline E[||w_A - w_B||^2]  closed-form: {closed_sq:.4f} (7/36)")
    print(f"Null baseline E[||w_A - w_B||^2]  Monte Carlo: {mc_sq:.4f}")
    print(f"Null baseline sqrt(E[||.||^2])    (paper .44): {closed_baseline:.4f}")
    assert abs(closed_baseline - 0.4410) < 1e-3, closed_baseline
    assert abs(mc_sq - closed_sq) < 5e-3, (mc_sq, closed_sq)

    # 2. Positive-octant compression 1/256 (Proposition 4).
    frac = positive_octant_fraction(N_DIM)
    print(f"Positive-octant volume fraction 1/2^8       : {frac:.6f} (1/{int(1/frac)})")
    assert frac == 1.0 / 256.0, frac

    # 3. Theorem 5(i) closed form vs Monte Carlo over uniform observers.
    hermes = [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]
    ikea = [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]
    closed = expected_observer_distance_sq(hermes, ikea)
    obs = rng.dirichlet(np.ones(N_DIM), size=300_000)
    delta_sq = (clr(hermes) - clr(ikea)) ** 2
    mc = np.mean(obs @ delta_sq)
    print(f"E_w[d_w^2](Hermes, IKEA)  closed-form        : {closed:.4f}")
    print(f"E_w[d_w^2](Hermes, IKEA)  Monte Carlo         : {mc:.4f}")
    assert abs(mc - closed) < 5e-3, (mc, closed)

    # 4. Aitchison distance reproduces the paper's d(Hermes, Tesla) ~= 1.76.
    tesla = [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]
    d_ht = aitchison_distance(hermes, tesla)
    print(f"Aitchison d(Hermes, Tesla)                   : {d_ht:.2f}")
    assert abs(d_ht - 1.76) < 0.01, d_ht

    # 5. Metric sanity: identity, symmetry, INDSCAL reduction (Proposition 2).
    w = [0.25, 0.15, 0.05, 0.20, 0.10, 0.05, 0.15, 0.05]
    assert abs(combined_distance(w, hermes, w, hermes)) < 1e-12
    assert (
        abs(combined_distance(w, hermes, w, ikea) - observer_distance(w, hermes, ikea))
        < 1e-12
    )

    # ------------------------------------------------------------------ 6 --
    # Table 7: observer-dependent distances and ordering reversals.
    prof = [np.array(p, dtype=float) for p in CANONICAL_PROFILES]
    pairs = _pair_indices(len(prof))
    d_a = {pr: observer_distance(W_AESTHETE, prof[pr[0]], prof[pr[1]]) for pr in pairs}
    d_b = {
        pr: observer_distance(W_PRAGMATIST, prof[pr[0]], prof[pr[1]]) for pr in pairs
    }
    print("\nTable 7 — observer-dependent distances")
    for i, j in pairs:
        print(
            f"  {CANONICAL_NAMES[i]:>10s}-{CANONICAL_NAMES[j]:<10s} "
            f"alpha {d_a[(i, j)]:.3f}   beta {d_b[(i, j)]:.3f}   "
            f"ratio {d_b[(i, j)]/d_a[(i, j)]:.2f}"
        )
    reversals = [
        (p, q)
        for idx, p in enumerate(pairs)
        for q in pairs[idx + 1 :]
        if (d_a[p] - d_a[q]) * (d_b[p] - d_b[q]) < 0
    ]
    n_comparisons = len(pairs) * (len(pairs) - 1) // 2
    print(
        f"  ordering reversals between the two observers: {len(reversals)} of "
        f"{n_comparisons} pair-of-pairs comparisons "
        f"({100*len(reversals)/n_comparisons:.1f}%)"
    )
    assert len(reversals) == 13, len(reversals)
    assert abs(d_a[(0, 1)] - 0.323) < 5e-4, d_a[(0, 1)]
    assert abs(d_b[(0, 1)] - 0.738) < 5e-4, d_b[(0, 1)]
    assert abs(d_a[(1, 4)] - 0.384) < 5e-4, d_a[(1, 4)]
    assert abs(d_b[(1, 4)] - 0.425) < 5e-4, d_b[(1, 4)]
    # IKEA's neighbourhood: Hermes moves from rank 2 to rank 4 of 4.
    others = [k for k in range(5) if k != 1]
    rank_a = sorted(
        others, key=lambda k: observer_distance(W_AESTHETE, prof[1], prof[k])
    )
    rank_b = sorted(
        others, key=lambda k: observer_distance(W_PRAGMATIST, prof[1], prof[k])
    )
    print(f"  IKEA neighbourhood, aesthete   : {[CANONICAL_NAMES[k] for k in rank_a]}")
    print(f"  IKEA neighbourhood, pragmatist : {[CANONICAL_NAMES[k] for k in rank_b]}")
    assert rank_a.index(0) == 1 and rank_b.index(0) == 3

    # ------------------------------------------------------------------ 7 --
    # Cencov: merging contracts d_FR; congruent refinement preserves it.
    full = fisher_rao_distance(W_AESTHETE, W_PRAGMATIST)
    merges = {
        (i, j): fisher_rao_distance(
            merge_dimensions(W_AESTHETE, i, j), merge_dimensions(W_PRAGMATIST, i, j)
        )
        for i, j in _pair_indices(N_DIM)
    }
    contractions = {k: 1.0 - v / full for k, v in merges.items()}
    worst = max(contractions, key=contractions.get)
    best = min(contractions, key=contractions.get)
    refined = fisher_rao_distance(
        split_dimension(W_AESTHETE, 0), split_dimension(W_PRAGMATIST, 0)
    )
    print("\nCencov: coarse-graining contracts, congruent refinement preserves")
    print(f"  d_FR(w_alpha, w_beta), 8 categories        : {full:.3f}")
    print(
        f"  merge semiotic+narrative (dims 1+2)        : {merges[(0, 1)]:.3f} "
        f"({100*contractions[(0, 1)]:.1f}% contraction)"
    )
    print(
        f"  largest contraction, merge dims {worst[0]+1}+{worst[1]+1}         : "
        f"{merges[worst]:.3f} ({100*contractions[worst]:.1f}%)"
    )
    print(
        f"  smallest contraction, merge dims {best[0]+1}+{best[1]+1}        : "
        f"{merges[best]:.3f} ({100*contractions[best]:.1f}%)"
    )
    print(
        f"  mean contraction over all 28 merges        : "
        f"{100*np.mean(list(contractions.values())):.1f}%"
    )
    print(f"  congruent refinement (0.5/0.5 split dim 1) : {refined:.3f}")
    assert all(v >= -1e-12 for v in contractions.values()), "a merge expanded d_FR"
    assert abs(full - 1.176) < 5e-4, full
    assert abs(merges[(0, 1)] - 1.171) < 1e-3, merges[(0, 1)]
    assert abs(contractions[worst] - 0.380) < 5e-3, contractions[worst]
    assert abs(np.mean(list(contractions.values())) - 0.075) < 5e-3
    assert abs(refined - full) < 1e-12, (refined, full)

    # ------------------------------------------------------------------ 8 --
    # Definition 4: tau from a Weber JND, and the resulting classification.
    tau = jnd_threshold(0.10)
    obs = rng.dirichlet(np.ones(N_DIM), size=400_000)
    print(f"\nDefinition 4 with tau(k = .10) = {tau:.4f}")
    rms_vals, cvs, p5s, kstars = [], [], [], []
    for i, j in pairs:
        delta_sq = (clr(prof[i]) - clr(prof[j])) ** 2
        d2 = obs @ delta_sq
        rms = float(np.sqrt(expected_observer_distance_sq(prof[i], prof[j])))
        cv = float(d2.std() / d2.mean())
        p5 = float(np.percentile(np.sqrt(d2), 5))
        kstar = critical_weber_fraction(prof[i], prof[j])
        rms_vals.append(rms)
        cvs.append(cv)
        p5s.append(p5)
        kstars.append(kstar)
        print(
            f"  {CANONICAL_NAMES[i]:>10s}-{CANONICAL_NAMES[j]:<10s} "
            f"rms d_w {rms:.3f}  CV {cv:.3f}  5th pct {p5:.3f}  k* {100*kstar:.0f}%  "
            f"{'meaningful' if rms > tau else 'NOT meaningful':>14s}  "
            f"{'robust' if p5 > tau else 'NOT robust'}"
        )
    assert all(v > tau for v in rms_vals), "a pair failed the meaningfulness test"
    assert all(v > tau for v in p5s), "a pair failed the robustness test"
    assert abs(min(rms_vals) - 0.311) < 1e-3, min(rms_vals)
    assert abs(max(rms_vals) - 0.621) < 1e-3, max(rms_vals)
    assert abs(min(kstars) - 1.56) < 0.01, min(kstars)
    assert abs(max(kstars) - 5.54) < 0.02, max(kstars)
    assert abs(min(cvs) - 0.307) < 5e-3, min(cvs)
    assert abs(max(cvs) - 0.692) < 5e-3, max(cvs)
    assert abs(min(p5s) - 0.216) < 5e-3, min(p5s)
    assert abs(max(p5s) - 0.390) < 5e-3, max(p5s)

    print("\nAll smoke-test assertions passed.")
    print(
        "NOTE: these assertions compare the paper's printed values against the\n"
        "values this module computes. They catch transcription drift between\n"
        "paper and script; they are NOT an independent verification that the\n"
        "computations are correct."
    )


if __name__ == "__main__":
    _smoke_test()
