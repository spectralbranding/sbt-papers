"""
Monte Carlo simulations for R3 (2026f) Cohort Boundaries.

Reproduces the numerical figures cited in:
- Table 2 (distance contrast ratio degradation with dimension)
- Table 5 (boundary volume fraction empirical verification at n=8, k=4)
- Table 7 (Fisher-Rao versus Euclidean contrast on Delta^7)

Paper: Zharnikov, D. (2026f). Geometric Necessity of Fuzzy Cohort Boundaries:
A Concentration Analysis of the 7-Simplex. Working paper.
DOI: 10.5281/zenodo.18945477

Run:
    uv run --with numpy --with scikit-learn python r3_concentration_mc.py

Reproducibility: seed = 42 unless otherwise noted. All quoted figures are
mean +/- standard error over the indicated number of trials.
"""

from __future__ import annotations

import numpy as np
from sklearn.cluster import KMeans

SEED = 42


def euclidean_dist(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    return np.linalg.norm(p - q, axis=-1)


def fisher_rao_dist(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Fisher-Rao distance on Delta^(n-1):
       d_FR(p,q) = 2 * arccos(sum_i sqrt(p_i * q_i))."""
    s = np.sum(np.sqrt(p * q), axis=-1)
    s = np.clip(s, -1.0, 1.0)
    return 2.0 * np.arccos(s)


def distance_contrast(n_dims: int, m: int, n_trials: int,
                      metric: str, rng: np.random.Generator) -> dict:
    """For each trial, draw m points from Dir(1,...,1) on Delta^(n-1).
       Compute distances from a reference to all others. Track contrast
       ratio max/min, mean distance, sd of distances."""
    ratios, means, sds = [], [], []
    dist_fn = euclidean_dist if metric == "euclidean" else fisher_rao_dist
    for _ in range(n_trials):
        pts = rng.dirichlet(np.ones(n_dims), size=m)
        d = dist_fn(pts[1:], pts[0])
        ratios.append(d.max() / d.min())
        means.append(d.mean())
        sds.append(d.std())
    return {
        "ratio_mean": float(np.mean(ratios)),
        "ratio_se": float(np.std(ratios) / np.sqrt(n_trials)),
        "dist_mean": float(np.mean(means)),
        "dist_sd": float(np.mean(sds)),
        "cv": float(np.mean(sds) / np.mean(means)),
    }


def boundary_volume_fraction(n_dims: int, k: int, N: int,
                             deltas: list[float],
                             rng: np.random.Generator) -> dict:
    """Empirical boundary volume fraction at n=8, k=4 partition,
       under Euclidean and Fisher-Rao distances. Procedure matches
       Section 5.2 of the paper."""
    pts = rng.dirichlet(np.ones(n_dims), size=N)

    km = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(pts)
    centers = km.cluster_centers_
    labels = km.labels_

    # Euclidean: distance to nearest perpendicular bisector.
    all_dists = np.linalg.norm(pts[:, None, :] - centers[None, :, :], axis=2)
    masked = np.where(np.eye(k)[labels].astype(bool), np.inf, all_dists)
    nearest_other = np.argmin(masked, axis=1)
    c_own = centers[labels]
    c_other = centers[nearest_other]
    diff = c_other - c_own
    norm = np.linalg.norm(diff, axis=1)
    proj = np.sum((pts - 0.5 * (c_own + c_other)) * diff, axis=1) / norm
    dist_bis_eucl = np.abs(proj)
    mean_ic_eucl = np.mean([
        np.linalg.norm(centers[i] - centers[j])
        for i in range(k) for j in range(i + 1, k)
    ])

    # Fisher-Rao: geodesic on S^7_+ via square-root map.
    sqrt_pts = 2.0 * np.sqrt(pts)
    sqrt_centers = 2.0 * np.sqrt(centers / centers.sum(axis=1, keepdims=True))
    R = 2.0

    def geo(p, c):
        cosang = np.clip(np.sum(p * c, axis=-1) / (R * R), -1.0, 1.0)
        return R * np.arccos(cosang)

    d_own_fr = geo(sqrt_pts, sqrt_centers[labels])
    d_other_fr = geo(sqrt_pts, sqrt_centers[nearest_other])
    dist_bis_fr = np.abs(d_other_fr - d_own_fr) / 2.0
    mean_ic_fr = np.mean([
        geo(sqrt_centers[i], sqrt_centers[j])
        for i in range(k) for j in range(i + 1, k)
    ])

    # δ is interpreted as an absolute Euclidean threshold on Δ^7 for the
    # Euclidean comparison (matches Theorem 2 convention since the simplex
    # has effective diameter ~ √2 and component differences are all <1) and
    # as an absolute geodesic-radian threshold on S^7_+ for the Fisher-Rao
    # comparison.
    out = {"euclidean": {}, "fisher_rao": {}}
    for delta in deltas:
        out["euclidean"][delta] = float(np.mean(dist_bis_eucl < delta))
        out["fisher_rao"][delta] = float(np.mean(dist_bis_fr < delta))
    out["mean_intercentroid_eucl"] = float(mean_ic_eucl)
    out["mean_intercentroid_fr"] = float(mean_ic_fr)
    return out


def main() -> None:
    rng = np.random.default_rng(SEED)

    print("=" * 60)
    print("Table 2 : distance contrast ratio degradation (Euclidean)")
    print("=" * 60)
    print(f"{'n':>4}  {'R_n':>10}  {'mean_d':>8}  {'sd_d':>8}")
    for n in (2, 4, 8, 16, 32):
        r = distance_contrast(n, m=1000, n_trials=1000,
                              metric="euclidean", rng=rng)
        print(f"{n:>4}  {r['ratio_mean']:>10.3f}  "
              f"{r['dist_mean']:>8.4f}  {r['dist_sd']:>8.4f}")

    print()
    print("=" * 60)
    print("Table 7 : Euclidean vs Fisher-Rao at n=8 (m=1000, 1000 trials)")
    print("=" * 60)
    for metric in ("euclidean", "fisher_rao"):
        r = distance_contrast(8, m=1000, n_trials=1000,
                              metric=metric, rng=rng)
        print(f"{metric:>12}  R_8={r['ratio_mean']:.3f} +/- {r['ratio_se']:.3f}"
              f"  mean={r['dist_mean']:.4f}  CV={r['cv']:.4f}")

    print()
    print("=" * 60)
    print("Table 5 : empirical boundary volume fraction (n=8, k=4)")
    print("=" * 60)
    bv = boundary_volume_fraction(
        n_dims=8, k=4, N=100_000,
        deltas=[0.05, 0.10, 0.20], rng=rng,
    )
    print(f"mean inter-centroid (Eucl) = {bv['mean_intercentroid_eucl']:.4f}")
    print(f"mean inter-centroid (FR)   = {bv['mean_intercentroid_fr']:.4f}")
    for delta in (0.05, 0.10, 0.20):
        print(f"  delta={delta}: "
              f"Eucl BVF = {100*bv['euclidean'][delta]:.1f}%  "
              f"FR BVF = {100*bv['fisher_rao'][delta]:.1f}%")


if __name__ == "__main__":
    main()
