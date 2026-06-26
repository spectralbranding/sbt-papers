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

    uv run python research/papers/2026d/code/metrics.py

The ``__main__`` smoke test reproduces two paper numbers with a fixed seed:
the ~.44 concentration null baseline sqrt(7/36) for random observer pairs at
n = 8, and the 1/256 positive-octant volume fraction, and checks the
Theorem 5(i) closed form against a Monte Carlo estimate.
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

    print("\nAll smoke-test assertions passed.")


if __name__ == "__main__":
    _smoke_test()
