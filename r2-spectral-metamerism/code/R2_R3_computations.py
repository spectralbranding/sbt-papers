"""
Monte Carlo metameric-fraction computation for Zharnikov (2026e)
================================================================
Companion computation script for the metamerism result in:

  "Spectral Metamerism: Brand Perception Under Projection"  (R2)
  DOI: see paper header (concept DOI on the public mirror)

The paper (Section "Monte Carlo" / Table 8) names this script as
`R2_R3_computations.py` and states it is shared with the R3 cohort-boundaries
paper (2026f), which reuses the same random-projection generator for its
concentration-of-measure tests. This file reproduces the R2 metameric-fraction
result (Table 8); the generator is exposed as importable functions so the R3
concentration tests can reuse it.

Run command:
    uv run --with numpy python R2_R3_computations.py
    # or, if numpy is already available:
    python R2_R3_computations.py

Random seed: 42 (fixed at file top). NOTE on reproducibility: Table 8 reports
three trials "with different random seeds" but the paper does not record those
seeds, so the EXACT per-trial counts (474 / 388 / 374) are not bit-reproducible
from the paper alone. This script fixes SEED=42 and reports (a) the three
trials it produces and (b) the mean metameric fraction over many trials, to
confirm the paper's actual quantitative CLAIM: the metameric fraction is stable
at ~31-39% under uniformly random projection directions. The script does not
tune constants to hit the specific published counts.

Model (Section "Monte Carlo")
-----------------------------
1. Generate N=50 brand profiles in R^8_+ via component-wise log-normal
   (underlying normal mean mu=0.5, sigma=0.5); positivity is automatic.
2. Distances and projection are computed on the LOG-profiles (the paper
   specifies "Euclidean on log-profiles" for the 8D distance), i.e. on the
   underlying normal vectors L = log(profile).
3. Draw a random unit projection direction u in R^8 (Gaussian, normalized).
4. Project every log-profile onto u: s_i = u . L_i.
5. Over all C(50,2)=1225 pairs compute d_8D = ||L_i - L_j||_2 and
   d_1D = |s_i - s_j|.
6. A pair is METAMERIC iff d_8D > 1.0 AND d_1D < 0.3.

Additional computations added 2026-08-24 for the corrected paper
----------------------------------------------------------------
B. Threshold sensitivity grid (paper Table 9): the mean metameric fraction
   over a +/-20% grid on both classification thresholds.
C. Rank-limited PCA nulls for the five canonical brand profiles (paper
   "Variance Retention"): five points in R^8 span at most four dimensions, so
   the sample covariance has at most four nonzero eigenvalues and PC1 >= 25%
   before any correlation exists. Two nulls are computed -- the parametric
   null of Theorem 4 (Sigma = sigma^2 I_8) and a distribution-free permutation
   null that shuffles each dimension independently across the five brands.
D. Brand-space resampling null for Aitchison audit distances (paper "The
   Vectorized Alternative"): the observer-space moment sqrt(7/36) = .441 is
   not a valid threshold for brand-space distances; the null is resampled from
   the observed per-dimension marginals instead.

Every printed paper value is asserted against the value computed here. Those
assertions catch transcription drift between paper and script; they are not an
independent check that the model is the right one.
"""

import sys
from itertools import combinations

import numpy as np

# ---------------------------------------------------------------------------
# Constants (named; edit here to reproduce variants)
# ---------------------------------------------------------------------------
SEED = 42
N_PROFILES = 50
DIM = 8
LOGNORM_MU = 0.5
LOGNORM_SIGMA = 0.5
THRESH_8D = 1.0  # d_8D > 1.0  (well separated in 8D)
THRESH_1D = 0.3  # d_1D < 0.3  (indistinguishable in 1D)
N_TRIALS_TABLE = 3  # Table 8 reports three trials
N_TRIALS_BAND = 2000  # large run to characterize the fraction band robustly

# --- (B) threshold sensitivity grid (paper Table 9) -------------------------
GRID_8D = [0.80, 0.90, 1.00, 1.10, 1.20]  # +/-20% around THRESH_8D
GRID_1D = [0.24, 0.27, 0.30, 0.33, 0.36]  # +/-20% around THRESH_1D
N_TRIALS_GRID = 2000

# --- (C)/(D) canonical brand profiles (project [internal ref removed], canonical) --------
CANONICAL_NAMES = ["Hermes", "IKEA", "Patagonia", "Erewhon", "Tesla"]
CANONICAL_PROFILES = np.array(
    [
        [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
        [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
        [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
        [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
        [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
    ]
)
N_DRAWS_PCA_NULL = 100_000
N_DRAWS_AITCHISON_NULL = 200_000


def generate_log_profiles(
    rng, n=N_PROFILES, dim=DIM, mu=LOGNORM_MU, sigma=LOGNORM_SIGMA
):
    """Return the LOG-profiles (underlying normals) of n log-normal profiles.

    profile = exp(Normal(mu, sigma)); log-profile = Normal(mu, sigma).
    Distances and the 1D projection are computed on the log-profiles per the
    paper's "Euclidean on log-profiles" specification.
    """
    return rng.normal(loc=mu, scale=sigma, size=(n, dim))


def random_unit_direction(rng, dim=DIM):
    u = rng.normal(size=dim)
    return u / np.linalg.norm(u)


def metameric_fraction(rng):
    """One trial: return (n_metameric, total_pairs, fraction)."""
    L = generate_log_profiles(rng)
    u = random_unit_direction(rng)
    s = L @ u  # 1D projections
    n_meta = 0
    total = 0
    for i, j in combinations(range(L.shape[0]), 2):
        total += 1
        d8 = np.linalg.norm(L[i] - L[j])
        d1 = abs(s[i] - s[j])
        if d8 > THRESH_8D and d1 < THRESH_1D:
            n_meta += 1
    return n_meta, total, n_meta / total


def sensitivity_grid(rng, n_trials=N_TRIALS_GRID):
    """(B) Mean metameric fraction over the +/-20% threshold grid (Table 9)."""
    iu = np.triu_indices(N_PROFILES, 1)
    acc = np.zeros((len(GRID_8D), len(GRID_1D)))
    for _ in range(n_trials):
        L = generate_log_profiles(rng)
        u = random_unit_direction(rng)
        s = L @ u
        d8 = np.linalg.norm(L[:, None, :] - L[None, :, :], axis=-1)[iu]
        d1 = np.abs(s[:, None] - s[None, :])[iu]
        for a, x in enumerate(GRID_8D):
            for b, y in enumerate(GRID_1D):
                acc[a, b] += ((d8 > x) & (d1 < y)).mean()
    return acc / n_trials


def variance_shares(X):
    """Sorted eigenvalue shares of the sample covariance of the rows of X."""
    ev = np.sort(np.linalg.eigvalsh(np.cov(X - X.mean(0), rowvar=False)))[::-1]
    ev = np.clip(ev, 0.0, None)
    return ev / ev.sum()


def pca_rank_limited_nulls(rng, draws=N_DRAWS_PCA_NULL):
    """(C) Observed PCA shares vs the two rank-limited nulls."""
    obs = variance_shares(CANONICAL_PROFILES)
    obs_pc1, obs_cum3 = obs[0], obs[:3].sum()

    par_pc1 = np.empty(draws)
    par_cum3 = np.empty(draws)
    for t in range(draws):
        f = variance_shares(rng.normal(size=(len(CANONICAL_PROFILES), DIM)))
        par_pc1[t], par_cum3[t] = f[0], f[:3].sum()

    perm_pc1 = np.empty(draws)
    perm_cum3 = np.empty(draws)
    for t in range(draws):
        X = np.column_stack(
            [rng.permutation(CANONICAL_PROFILES[:, j]) for j in range(DIM)]
        )
        f = variance_shares(X)
        perm_pc1[t], perm_cum3[t] = f[0], f[:3].sum()

    return {
        "obs_pc1": obs_pc1,
        "obs_cum3": obs_cum3,
        "par": (par_pc1, par_cum3),
        "perm": (perm_pc1, perm_cum3),
    }


def clr(x):
    lg = np.log(x)
    return lg - lg.mean(axis=-1, keepdims=True)


def aitchison_brand_space_null(rng, draws=N_DRAWS_AITCHISON_NULL):
    """(D) Null Aitchison distance from per-dimension marginal resampling."""
    cols = [CANONICAL_PROFILES[:, k] for k in range(DIM)]
    d = np.empty(draws)
    for t in range(draws):
        a = np.array([rng.choice(c) for c in cols])
        b = np.array([rng.choice(c) for c in cols])
        d[t] = np.linalg.norm(clr(a) - clr(b))
    return d


def canonical_pair_distances():
    C = clr(CANONICAL_PROFILES)
    out = []
    for i, j in combinations(range(len(CANONICAL_PROFILES)), 2):
        out.append(
            (CANONICAL_NAMES[i], CANONICAL_NAMES[j], float(np.linalg.norm(C[i] - C[j])))
        )
    return out


def _check(label, computed, printed, tol):
    ok = abs(computed - printed) <= tol
    print(
        f"  [{'OK ' if ok else 'DRIFT'}] {label}: script {computed:.3f} "
        f"vs paper {printed:.3f} (tol {tol})"
    )
    return ok


def main():
    print("Monte Carlo metameric-fraction computation — Zharnikov (2026e), Table 8")
    print(
        f"seed={SEED}  N={N_PROFILES} profiles in R^{DIM}_+  "
        f"log-normal(mu={LOGNORM_MU}, sigma={LOGNORM_SIGMA})"
    )
    print(f"metameric iff d_8D > {THRESH_8D} and d_1D < {THRESH_1D}\n")

    rng = np.random.default_rng(SEED)

    print("Three independent trials (this script's seed; paper's seeds unknown):")
    print(
        f"  {'Trial':>5} {'Metameric Pairs':>16} {'Fraction':>10} {'Total Pairs':>12}"
    )
    fracs = []
    for t in range(1, N_TRIALS_TABLE + 1):
        n_meta, total, frac = metameric_fraction(rng)
        fracs.append(frac)
        print(f"  {t:>5} {n_meta:>16} {frac*100:>9.1f}% {total:>12}")

    # Large run to characterize the band robustly.
    rng2 = np.random.default_rng(SEED)
    band = [metameric_fraction(rng2)[2] for _ in range(N_TRIALS_BAND)]
    band = np.array(band)
    lo, hi = band.min(), band.max()
    mean = band.mean()
    p05, p95 = np.percentile(band, [5, 95])

    print(f"\nOver {N_TRIALS_BAND} trials (seed={SEED}):")
    print(f"  mean fraction          = {mean*100:.1f}%")
    print(f"  min / max              = {lo*100:.1f}% / {hi*100:.1f}%")
    print(f"  5th / 95th percentile  = {p05*100:.1f}% / {p95*100:.1f}%")

    # The paper's actual claim is the stable band ~31-39% (Table 8 / Results).
    claim_lo, claim_hi = 0.31, 0.39
    central_in_band = claim_lo - 0.05 <= mean <= claim_hi + 0.05
    print()
    if central_in_band:
        print(
            f"  [MATCH] mean metameric fraction {mean*100:.1f}% is consistent with the"
        )
        print(f"          paper's stated stable band of 31-39% (Table 8).")
    else:
        print(f"  [MISMATCH] mean metameric fraction {mean*100:.1f}% falls outside the")
        print(f"             paper's stated 31-39% band — investigate (do not tune).")
    print()
    print("  NOTE: the specific Table-8 counts (474 / 388 / 374; 38.7% / 31.7% /")
    print("  30.5%) depend on the paper's unrecorded per-trial seeds and are not")
    print("  bit-reproducible from the paper alone. What reproduces is the stable")
    print("  ~31-39% band the paper's qualitative claim rests on. This script is")
    print("  the importable generator the R3 paper (2026f) reuses for its")
    print("  concentration-of-measure tests (generate_log_profiles /")
    print("  random_unit_direction).")

    # ---------------------------------------------------------------- (B) --
    print("\n" + "=" * 72)
    print("(B) Threshold sensitivity grid — paper Table 9")
    print("=" * 72)
    grid = sensitivity_grid(np.random.default_rng(SEED))
    header = "  d_8D \\ d_1D " + " ".join(f"{y:>7.2f}" for y in GRID_1D)
    print(header)
    for a, x in enumerate(GRID_8D):
        print(f"  >{x:>11.2f} " + " ".join(f"{100*v:>6.1f}%" for v in grid[a]))
    lo, hi = grid.min(), grid.max()
    centre = grid[GRID_8D.index(1.00), GRID_1D.index(0.30)]
    swing_8d = grid[0, GRID_1D.index(0.30)] - grid[-1, GRID_1D.index(0.30)]
    swing_1d = grid[GRID_8D.index(1.00), -1] - grid[GRID_8D.index(1.00), 0]
    print(f"\n  grid range          = {100*lo:.1f}% .. {100*hi:.1f}%")
    print(f"  centre cell         = {100*centre:.1f}%")
    print(f"  swing with 8D thr   = {100*swing_8d:.1f} pp")
    print(f"  swing with 1D thr   = {100*swing_1d:.1f} pp")

    # ---------------------------------------------------------------- (C) --
    print("\n" + "=" * 72)
    print("(C) Rank-limited PCA nulls for the five canonical profiles")
    print("=" * 72)
    shares = variance_shares(CANONICAL_PROFILES)
    print("  observed eigenvalue shares: " + " ".join(f"{100*v:.1f}%" for v in shares))
    print("  NOTE: at most four are nonzero — five points in R^8 span <= 4 dimensions,")
    print("        so PC1 >= 25% before any inter-dimensional correlation exists.")
    res = pca_rank_limited_nulls(np.random.default_rng(SEED))
    for tag, key in [
        ("parametric (Sigma = sigma^2 I_8)", "par"),
        ("permutation", "perm"),
    ]:
        pc1, cum3 = res[key]
        print(f"\n  null: {tag}")
        print(
            f"    PC1  median {100*np.median(pc1):.1f}%   "
            f"p(null >= observed {100*res['obs_pc1']:.1f}%) = "
            f"{(pc1 >= res['obs_pc1']).mean():.3f}"
        )
        print(
            f"    cum3 median {100*np.median(cum3):.1f}%   "
            f"p(null >= observed {100*res['obs_cum3']:.1f}%) = "
            f"{(cum3 >= res['obs_cum3']).mean():.3f}"
        )

    # ---------------------------------------------------------------- (D) --
    print("\n" + "=" * 72)
    print("(D) Brand-space null for Aitchison audit distances")
    print("=" * 72)
    for a, b, dv in canonical_pair_distances():
        print(f"  {a:>10s} - {b:<10s} {dv:.3f}")
    dnull = aitchison_brand_space_null(np.random.default_rng(SEED))
    p05, p50, p95 = np.percentile(dnull, [5, 50, 95])
    thr = np.sqrt(7 / 36)
    print(
        f"\n  resampling null: median {p50:.2f}, 5th-95th {p05:.2f}-{p95:.2f}, "
        f"sd {dnull.std():.2f}"
    )
    print(
        f"  observer-space sqrt(7/36) = {thr:.3f} sits at the "
        f"{100*(dnull < thr).mean():.1f}th percentile of the brand-space null"
    )
    obs_pairs = np.array([d for _, _, d in canonical_pair_distances()])
    print(
        f"  case-set distances {obs_pairs.min():.2f}-{obs_pairs.max():.2f} span the "
        f"{100*(dnull < obs_pairs.min()).mean():.0f}th to the "
        f"{100*(dnull < obs_pairs.max()).mean():.0f}th percentile; "
        f"median {np.median(obs_pairs):.2f} vs null median {p50:.2f}"
    )

    # ------------------------------------------------- paper-value asserts --
    print("\n" + "=" * 72)
    print("Paper-vs-script transcription check")
    print("=" * 72)
    print("  These assertions catch transcription drift between the paper and this")
    print("  script. They are NOT an independent check of the model.")
    checks = [
        _check("PC1 share (Variance Retention)", res["obs_pc1"], 0.549, 0.002),
        _check("PC1+PC2+PC3 share", res["obs_cum3"], 0.923, 0.002),
        _check(
            "p(parametric null >= PC1)",
            (res["par"][0] >= res["obs_pc1"]).mean(),
            0.315,
            0.01,
        ),
        _check(
            "p(parametric null >= cum3)",
            (res["par"][1] >= res["obs_cum3"]).mean(),
            0.771,
            0.01,
        ),
        _check(
            "p(permutation null >= PC1)",
            (res["perm"][0] >= res["obs_pc1"]).mean(),
            0.361,
            0.01,
        ),
        _check(
            "p(permutation null >= cum3)",
            (res["perm"][1] >= res["obs_cum3"]).mean(),
            0.813,
            0.01,
        ),
        _check("Table 9 centre cell", centre, 0.316, 0.01),
        _check("Table 9 minimum", lo, 0.238, 0.01),
        _check("Table 9 maximum", hi, 0.385, 0.01),
        _check("brand-space null median", p50, 1.15, 0.03),
        _check("Hermes-Patagonia Aitchison distance", obs_pairs.min(), 0.88, 0.01),
        _check("Hermes-Tesla Aitchison distance", obs_pairs.max(), 1.76, 0.01),
    ]
    print(f"\n  {sum(checks)}/{len(checks)} printed values match the script.")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
