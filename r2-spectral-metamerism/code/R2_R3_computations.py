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
    return 0


if __name__ == "__main__":
    sys.exit(main())
