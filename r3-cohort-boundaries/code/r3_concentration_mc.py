"""Monte Carlo computations for R3 (2026f), Boundary Volume and Cohort Reassignment.

Reproduces every Monte Carlo figure cited in the paper:

  Table 3   distance contrast ratio degradation with dimension (Euclidean)
  Table 4   Euclidean versus Fisher-Rao concentration at n = 8
  Table 7   boundary volume fraction, verification of Theorem 2
  Table 8   inter-cohort bisector proximity (Proposition 4), by k and by seed
  Table 9   fixed-zone Dirichlet contraction (analytic check)
  Table 10  re-fitted partitions on concentrated Dirichlet populations

Theorem 2 bounds the fraction of the simplex lying within relative distance
delta of the boundary of its own convex cell, where delta is normalised by the
cell's VOLUME RADIUS r_V = (vol(C) / omega_d)^(1/d), d = n - 1, and the cell
boundary is the FULL boundary -- internal bisectors together with the faces of
the simplex that bound the cell.  Both choices are forced:

  * Brunn-Minkowski applied to C_{-t} (+) tB <= C yields
    vol(C_{-t})/vol(C) <= (1 - t/r_V)^d.  Normalising by the in-radius R
    instead claims a strictly stronger bound (R <= r_V always) that is false in
    general; `inradius_counterexample()` exhibits a thin box that violates it.
  * The peeling argument is about the boundary of the convex body C, which for
    a Voronoi cell of the simplex includes the simplex faces.

`boundary_volume_fraction` therefore reports the settled reading alongside the
three rejected ones, so the comparison in the paper's Table 7 is reproducible
rather than asserted.

Paper: Zharnikov, D. (2026f). Boundary Volume and Cohort Reassignment on the
7-Simplex: A Concentration Analysis Under the Uniform Null. Working paper.
DOI: 10.5281/zenodo.18945477

Run:
    uv run --with numpy --with scipy --with scikit-learn python r3_concentration_mc.py

Runtime is roughly two minutes on a laptop.  Reproducibility: seed = 42 unless
a table varies the seed deliberately.  Quoted figures are means over the stated
number of trials; binomial standard errors are reported for every fraction.
"""

from __future__ import annotations

from math import gamma, pi, sqrt

import numpy as np
from scipy.optimize import linprog
from sklearn.cluster import KMeans

SEED = 42
N_DIMS = 8
K = 4
N_POINTS = 100_000
DELTAS = (0.05, 0.10, 0.20)

# A face {x_i = 0} of the simplex, measured inside the affine hull sum(x) = 1:
# the outward normal e_i projected onto {v : sum(v) = 0} has norm
# sqrt((n-1)/n), so d(x, face_i) = x_i * sqrt(n/(n-1)).
FACE_SCALE = sqrt(N_DIMS / (N_DIMS - 1.0))


# --------------------------------------------------------------------------
# metrics
# --------------------------------------------------------------------------


def euclidean_dist(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    return np.linalg.norm(p - q, axis=-1)


def fisher_rao_dist(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Fisher-Rao distance on the simplex: 2 * arccos(sum_i sqrt(p_i q_i))."""
    s = np.clip(np.sum(np.sqrt(p * q), axis=-1), -1.0, 1.0)
    return 2.0 * np.arccos(s)


def component_sd(alpha: float, n: int = N_DIMS) -> float:
    """SD of a single component of a symmetric Dirichlet(alpha, ..., alpha)."""
    a0 = n * alpha
    return sqrt(alpha * (a0 - alpha) / (a0**2 * (a0 + 1)))


def simplex_volume(n: int = N_DIMS) -> float:
    """(n-1)-volume of the standard simplex in its affine hull: sqrt(n)/(n-1)!."""
    return sqrt(n) / gamma(n)


def ball_volume(d: int) -> float:
    return pi ** (d / 2.0) / gamma(d / 2.0 + 1.0)


# --------------------------------------------------------------------------
# Table 3 / Table 4 -- distance contrast
# --------------------------------------------------------------------------


def distance_contrast(n_dims, m, n_trials, metric, rng) -> dict:
    """Draw m points from Dir(1,...,1); measure distances from one reference to
    the rest; track the contrast ratio max/min, the mean and the SD."""
    dist_fn = euclidean_dist if metric == "euclidean" else fisher_rao_dist
    ratios, means, sds = [], [], []
    for _ in range(n_trials):
        pts = rng.dirichlet(np.ones(n_dims), size=m)
        d = dist_fn(pts[1:], pts[0])
        ratios.append(d.max() / d.min())
        means.append(d.mean())
        sds.append(d.std())
    ratios = np.asarray(ratios)
    return {
        "ratio_mean": float(ratios.mean()),
        "ratio_median": float(np.median(ratios)),
        "ratio_se": float(ratios.std(ddof=1) / sqrt(n_trials)),
        "ratio_se_pct": float(
            100 * ratios.std(ddof=1) / sqrt(n_trials) / ratios.mean()
        ),
        "dist_mean": float(np.mean(means)),
        "dist_sd": float(np.mean(sds)),
        "cv": float(np.mean(sds) / np.mean(means)),
    }


# --------------------------------------------------------------------------
# Theorem 2 -- the in-radius normalisation is not available
# --------------------------------------------------------------------------


def inradius_counterexample(R=1.0, half_length=20.0, t=0.1) -> dict:
    """A 2d box of half-width R and half-length L >> R.  Its inner parallel
    body at depth t has volume ratio (1-t/R)(1-t/L), which exceeds the
    in-radius form (1-t/R)^2 whenever L > R.  The volume-radius form holds."""
    d = 2
    vol = 4 * R * half_length
    vol_inner = 4 * (R - t) * (half_length - t)
    r_v = sqrt(vol / pi)
    return {
        "true_ratio": vol_inner / vol,
        "inradius_bound": (1 - t / R) ** d,
        "volradius_bound": (1 - t / r_v) ** d,
        "inradius_holds": vol_inner / vol <= (1 - t / R) ** d,
        "volradius_holds": vol_inner / vol <= (1 - t / r_v) ** d,
    }


def cell_inradius(centers: np.ndarray, own: int, n_dims: int = N_DIMS) -> float:
    """In-radius of the Voronoi cell of `own` clipped to the simplex, measured
    inside the affine hull.  Solved as a linear program in [x_0..x_{n-1}, r]:
    maximise r subject to sum(x) = 1, x_i >= r*sqrt(n/(n-1)) for every simplex
    face, and a_j . x + r|a_j| <= b_j for every bisector."""
    c_own = centers[own]
    a_ub, b_ub = [], []
    for j in range(len(centers)):
        if j == own:
            continue
        a = centers[j] - c_own
        a_ub.append(np.append(a, np.linalg.norm(a)))
        b_ub.append((centers[j] @ centers[j] - c_own @ c_own) / 2.0)
    for i in range(n_dims):
        row = np.zeros(n_dims + 1)
        row[i], row[n_dims] = -1.0, FACE_SCALE
        a_ub.append(row)
        b_ub.append(0.0)
    a_eq = np.zeros((1, n_dims + 1))
    a_eq[0, :n_dims] = 1.0
    obj = np.zeros(n_dims + 1)
    obj[n_dims] = -1.0
    res = linprog(
        obj,
        A_ub=np.array(a_ub),
        b_ub=np.array(b_ub),
        A_eq=a_eq,
        b_eq=[1.0],
        bounds=[(0, 1)] * n_dims + [(0, None)],
        method="highs",
    )
    if not res.success:
        raise RuntimeError(f"in-radius LP failed for cell {own}: {res.message}")
    return float(res.x[n_dims])


def partition_distances(
    pts: np.ndarray, centers: np.ndarray, labels: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Per point: distance to the nearest inter-cohort bisector (minimised over
    every other centroid, which is exact for a Voronoi cell), and distance to
    the nearest simplex face."""
    n, k = len(pts), len(centers)
    d_bis = np.full((n, k), np.inf)
    for own in range(k):
        mask = labels == own
        if not mask.any():
            continue
        for j in range(k):
            if j == own:
                continue
            a = centers[j] - centers[own]
            b = (centers[j] @ centers[j] - centers[own] @ centers[own]) / 2.0
            d_bis[mask, j] = (b - pts[mask] @ a) / np.linalg.norm(a)
    return d_bis.min(axis=1), pts.min(axis=1) * FACE_SCALE


def fit_partition(alpha, k, n_dims=N_DIMS, n_points=N_POINTS, seed=SEED):
    rng = np.random.default_rng(seed)
    pts = rng.dirichlet(np.full(n_dims, float(alpha)), size=n_points)
    km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(pts)
    return pts, km.cluster_centers_, km.labels_


def boundary_volume_fraction(
    n_dims=N_DIMS, k=K, n_points=N_POINTS, deltas=DELTAS, seed=SEED
) -> dict:
    """Table 7.  The settled reading is `rel_rv_full`; the other three are the
    rejected readings, reported so the comparison is reproducible."""
    d = n_dims - 1
    pts, centers, labels = fit_partition(1, k, n_dims, n_points, seed)
    d_bis, d_face = partition_distances(pts, centers, labels)
    d_full = np.minimum(d_bis, d_face)

    shares = np.bincount(labels, minlength=k) / n_points
    inradii = np.array([cell_inradius(centers, i, n_dims) for i in range(k)])
    vol_radii = (shares * simplex_volume(n_dims) / ball_volume(d)) ** (1.0 / d)
    r_pt, rv_pt = inradii[labels], vol_radii[labels]

    rows = {}
    for delta in deltas:
        rows[delta] = {
            "bound": 1 - (1 - delta) ** d,
            "rel_rv_full": float(np.mean(d_full < delta * rv_pt)),
            "rel_r_full": float(np.mean(d_full < delta * r_pt)),
            "rel_rv_bisector": float(np.mean(d_bis < delta * rv_pt)),
            "abs_bisector": float(np.mean(d_bis < delta)),
        }
    return {
        "rows": rows,
        "shares": shares,
        "inradii": inradii,
        "vol_radii": vol_radii,
        "face_share": float(np.mean(d_face < d_bis)),
        "mean_d_bis": float(d_bis.mean()),
        "mean_d_face": float(d_face.mean()),
        "mean_d_full": float(d_full.mean()),
        "mean_intercentroid": float(
            np.mean(
                [
                    np.linalg.norm(centers[i] - centers[j])
                    for i in range(k)
                    for j in range(i + 1, k)
                ]
            )
        ),
    }


def bisector_proximity(
    alpha=1, k=K, n_dims=N_DIMS, n_points=N_POINTS, seed=SEED
) -> dict:
    """Proposition 4.  Distance to the nearest inter-cohort bisector against the
    component SD at the same alpha -- both scale as alpha^(-1/2), so the ratio
    is the scale-free quantity."""
    pts, centers, labels = fit_partition(alpha, k, n_dims, n_points, seed)
    d_bis, d_face = partition_distances(pts, centers, labels)
    sd = component_sd(alpha, n_dims)
    within = float(np.mean(d_bis < sd))
    return {
        "alpha": alpha,
        "k": k,
        "seed": seed,
        "component_sd": sd,
        "mean_d_bis": float(d_bis.mean()),
        "sd_d_bis": float(d_bis.std()),
        "median_d_bis": float(np.median(d_bis)),
        "ratio": float(d_bis.mean() / sd),
        "within_1sd": within,
        "within_half_sd": float(np.mean(d_bis < 0.5 * sd)),
        "within_abs_10": float(np.mean(d_bis < 0.10)),
        "face_share": float(np.mean(d_face < d_bis)),
        "se_pp": 100 * sqrt(within * (1 - within) / n_points),
    }


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------


def rule(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def main() -> None:
    rng = np.random.default_rng(SEED)

    rule("Table 3 : distance contrast ratio degradation (Euclidean)")
    print(
        f"{'n':>4} {'R_n':>12} {'median':>12} {'SE(R_n)':>10} {'SE %':>7}"
        f" {'mean d':>9} {'SD d':>8} {'CV':>7}"
    )
    for n in (2, 4, 8, 16, 32):
        r = distance_contrast(n, m=1000, n_trials=1000, metric="euclidean", rng=rng)
        print(
            f"{n:>4} {r['ratio_mean']:>12.2f} {r['ratio_median']:>12.2f}"
            f" {r['ratio_se']:>10.2f} {r['ratio_se_pct']:>6.1f}%"
            f" {r['dist_mean']:>9.4f} {r['dist_sd']:>8.4f} {r['cv']:>7.3f}"
        )
    print("\n  n = 2 is degenerate: max/min is dominated by the closest pair and")
    print("  has no stable mean, so it is reported as an order of magnitude.")
    print("  Independent replications of the n = 2 ratio:")
    reps = [
        distance_contrast(
            2, m=1000, n_trials=1000, metric="euclidean", rng=np.random.default_rng(s)
        )["ratio_mean"]
        for s in (42, 43, 44, 45, 46)
    ]
    print(
        "   "
        + "  ".join(f"{v:,.0f}" for v in reps)
        + f"   (median of means {np.median(reps):,.0f})"
    )

    rule("Table 4 : Euclidean versus Fisher-Rao at n = 8")
    for metric in ("euclidean", "fisher_rao"):
        r = distance_contrast(8, m=1000, n_trials=1000, metric=metric, rng=rng)
        unit = "" if metric == "euclidean" else " rad"
        print(
            f"  {metric:>11}  R_8 = {r['ratio_mean']:.2f} +/- "
            f"{r['ratio_se']:.2f}   mean = {r['dist_mean']:.4f}{unit}"
            f"   CV = {r['cv']:.3f}"
        )
    e_sqrt = gamma(1.5) * gamma(N_DIMS) / gamma(N_DIMS + 0.5)
    bc = N_DIMS * e_sqrt**2
    print(f"\n  analytic E[sqrt(X_i)], X_i ~ Beta(1, n-1)   = {e_sqrt:.5f}")
    print(f"  analytic E[sum_i sqrt(p_i q_i)]             = {bc:.5f}")
    print(
        f"  2 arccos of that mean                       = "
        f"{2 * np.arccos(bc):.4f} rad"
    )
    print("  Jensen: arccos is concave on (0,1), so 2 arccos(E[.]) is an UPPER")
    print("  bound on E[2 arccos(.)]; the Monte Carlo mean above is the latter,")
    print("  and the gap between them is the Jensen gap, not a discrepancy.")

    rule("Theorem 2 : the in-radius normalisation is not available")
    ce = inradius_counterexample()
    print(f"  thin box, R = 1, L = 20, t = .1, d = 2")
    print(f"    true vol(C_-t)/vol(C)      = {ce['true_ratio']:.4f}")
    print(
        f"    in-radius form (1-t/R)^d   = {ce['inradius_bound']:.4f}"
        f"   -> {'holds' if ce['inradius_holds'] else 'VIOLATED'}"
    )
    print(
        f"    vol-radius form (1-t/r_V)^d = {ce['volradius_bound']:.4f}"
        f"  -> {'holds' if ce['volradius_holds'] else 'VIOLATED'}"
    )

    rule(
        f"Table 7 : boundary volume fraction, n = {N_DIMS}, k = {K}, "
        f"N = {N_POINTS:,}, seed {SEED}"
    )
    bv = boundary_volume_fraction()
    print(f"  cell volume shares    = " f"{np.array2string(bv['shares'], precision=4)}")
    print(
        f"  cell in-radii    R    = " f"{np.array2string(bv['inradii'], precision=4)}"
    )
    print(
        f"  cell vol-radii   r_V  = " f"{np.array2string(bv['vol_radii'], precision=4)}"
    )
    print(
        f"  R / r_V (mean)        = " f"{np.mean(bv['inradii'] / bv['vol_radii']):.4f}"
    )
    print(f"  mean inter-centroid   = {bv['mean_intercentroid']:.4f}")
    print(f"  mean d to bisector    = {bv['mean_d_bis']:.4f}")
    print(f"  mean d to face        = {bv['mean_d_face']:.4f}")
    print(f"  mean d to cell bdry   = {bv['mean_d_full']:.4f}")
    print(
        f"  nearest boundary is a simplex FACE for "
        f"{100*bv['face_share']:.1f}% of points"
    )
    print()
    print(
        f"  {'delta':>6} {'Thm 2':>8} | {'rel r_V, full':>14}"
        f" {'rel R, full':>12} | {'rel r_V, bis':>13} {'abs, bis':>9}"
    )
    print("  " + "-" * 72)
    for delta, row in bv["rows"].items():
        flag = "ok" if row["rel_rv_full"] >= row["bound"] else "VIOLATED"
        print(
            f"  {delta:>6.2f} {100*row['bound']:>7.1f}% |"
            f" {100*row['rel_rv_full']:>12.1f}% {flag:<8}"
            f" {100*row['rel_r_full']:>10.1f}% |"
            f" {100*row['rel_rv_bisector']:>12.1f}%"
            f" {100*row['abs_bisector']:>8.1f}%"
        )
    print("\n  Column 'rel r_V, full' is the settled reading and the one Theorem 2")
    print("  bounds.  'rel R, full' sits below the bound at every width, which is")
    print("  the numerical signature of the false in-radius normalisation.")

    rule("Table 8 : inter-cohort bisector proximity (Proposition 4)")
    sd1 = component_sd(1)
    print(f"  component SD at alpha = 1 : {sd1:.4f}")
    print(
        f"\n  {'k':>3} {'mean d':>9} {'d / SD':>8} {'within 1 SD':>12}"
        f" {'within .5 SD':>13} {'face-nearest':>13}"
    )
    for k in (2, 3, 4, 5, 6, 8):
        r = bisector_proximity(alpha=1, k=k)
        print(
            f"  {k:>3} {r['mean_d_bis']:>9.4f} {r['ratio']:>8.3f}"
            f" {100*r['within_1sd']:>11.1f}% {100*r['within_half_sd']:>12.1f}%"
            f" {100*r['face_share']:>12.1f}%"
        )
    print("\n  seed stability at k = 4:")
    vals = []
    for s in (42, 43, 44, 45, 46):
        r = bisector_proximity(alpha=1, k=4, seed=s)
        vals.append(100 * r["within_1sd"])
        print(
            f"    seed {s}: within 1 SD = {vals[-1]:.1f}%"
            f"   mean d = {r['mean_d_bis']:.4f}"
        )
    print(
        f"    across seeds: {np.mean(vals):.1f}% " f"(SD {np.std(vals, ddof=1):.2f} pp)"
    )

    rule("Table 9 : fixed-zone Dirichlet contraction (analytic check)")
    d = N_DIMS - 1
    base = 1 - 0.9**d
    print(f"  V_boundary(1) at delta = .10 : {100*base:.1f}%")
    print(f"\n  {'alpha':>6} {'alpha^-3.5':>14} {'bound':>12}")
    for alpha in (1, 3, 5, 10, 20):
        f = alpha ** (-d / 2.0)
        print(f"  {alpha:>6} {f:>14.6g} {100*base*f:>11.4f}%")
    print(
        f"\n  range over the cited empirical window alpha in [3, 10]: "
        f"{100*base*10**(-d/2):.4f}% to {100*base*3**(-d/2):.4f}%"
    )

    rule("Table 10 : re-fitted partitions on concentrated populations, k = 4")
    print("  Corollary 2 holds the partition fixed; clustering re-fits it.")
    print(
        f"\n  {'alpha':>6} {'comp SD':>9} {'mean d':>9} {'d / SD':>8}"
        f" {'within 1 SD':>12} {'within abs .10':>15}"
    )
    for alpha in (1, 2, 3, 5, 10, 30):
        r = bisector_proximity(alpha=alpha, k=4)
        print(
            f"  {alpha:>6} {r['component_sd']:>9.4f} {r['mean_d_bis']:>9.4f}"
            f" {r['ratio']:>8.3f} {100*r['within_1sd']:>11.1f}%"
            f" {100*r['within_abs_10']:>14.1f}%"
        )
    print("\n  The scale-free ratio FALLS with alpha and the within-1-SD fraction")
    print("  RISES: under a re-fitted partition, concentration does not sharpen")
    print("  cohort boundaries relative to the perturbations observers undergo.")


if __name__ == "__main__":
    main()
