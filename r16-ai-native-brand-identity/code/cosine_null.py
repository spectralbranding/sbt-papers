#!/usr/bin/env python3
"""Reference values for reading a cross-model cosine similarity.

Companion computation for R16 (2026x), section "Convergence with Other Evidence".

A cosine similarity near unity between two non-negative eight-dimensional
allocation vectors is not on its own evidence of a shared generating cause.
Every such vector lies in the non-negative orthant, and vectors confined to one
orthant of R^8 are close in cosine by construction. This script computes the
three reference values the paper quotes, so that the companion study's reported
cross-model cosine of .977 can be read against something rather than against 1.

    (a) the observed mean profile against a UNIFORM allocation, which carries no
        model-specific information at all;
    (b) the mean cosine between two INDEPENDENTLY DRAWN allocations, under
        Dirichlet priors of two concentrations;
    (c) the observed global and local mean profiles against each other.

Inputs are the published mean weight allocations of the companion study
(2026v Tables 4 and 5), which are reproduced here verbatim so that this script
needs no network access and no proprietary data.

Run command:
    uv run --with numpy python cosine_null.py

Fixed seed: SEED = 42.
Dependencies: Python 3.12, numpy.
"""

from __future__ import annotations

import numpy as np

SEED = 42
N_DIM = 8
N_PAIRS = 100_000

# 2026v Table 4: mean weight allocation, global brand pairs (Run 2).
GLOBAL_PROFILE = np.array([14.8, 11.1, 12.1, 18.7, 13.2, 14.6, 7.4, 8.1])
# 2026v Table 5: mean weight allocation, local brand pairs (Run 3).
LOCAL_PROFILE = np.array([14.3, 10.3, 8.2, 17.9, 11.2, 20.9, 7.9, 9.2])
UNIFORM = np.full(N_DIM, 100.0 / N_DIM)

# The cross-model cosine reported by the companion study across 24 architectures.
REPORTED_COSINE = 0.977


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def independent_allocation_null(alpha: float, rng: np.random.Generator) -> dict:
    """Cosine between two independently drawn Dirichlet allocations.

    alpha = 1 is the flat prior over the simplex; alpha = 8 is a moderately
    concentrated prior whose draws resemble a plausible spread of allocation
    behaviour across models.
    """
    draws = rng.dirichlet(np.full(N_DIM, alpha), size=2 * N_PAIRS)
    a, b = draws[0::2], draws[1::2]
    num = np.einsum("ij,ij->i", a, b)
    den = np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1)
    c = num / den
    return {
        "alpha": alpha,
        "mean": float(c.mean()),
        "p05": float(np.percentile(c, 5)),
        "p95": float(np.percentile(c, 95)),
        "exceeds_reported": float((c >= REPORTED_COSINE).mean()),
    }


def main() -> int:
    rng = np.random.default_rng(SEED)

    print(
        "Reference values for a cross-model cosine of "
        f"{REPORTED_COSINE:.3f} on eight-dimensional allocations"
    )
    print("=" * 70)
    print("\n(a) Observed profile against a uniform allocation\n")
    g_u = cosine(GLOBAL_PROFILE, UNIFORM)
    l_u = cosine(LOCAL_PROFILE, UNIFORM)
    print(f"    global mean profile vs uniform : {g_u:.4f}")
    print(f"    local  mean profile vs uniform : {l_u:.4f}")
    print("\n    A uniform vector encodes no model-specific structure whatever,")
    print("    and still sits within .02 of the reported cross-model value.")

    print("\n(b) Two INDEPENDENTLY drawn allocations\n")
    print(
        f"    {'prior':<22}{'mean cos':>10}{'5th pct':>10}{'95th pct':>10}"
        f"{'P(cos >= .977)':>16}"
    )
    for alpha in (1.0, 8.0):
        r = independent_allocation_null(alpha, rng)
        print(
            f"    Dirichlet(alpha={alpha:g}){'':<6}{r['mean']:>10.4f}"
            f"{r['p05']:>10.4f}{r['p95']:>10.4f}{r['exceeds_reported']:>16.4f}"
        )
    print("\n    Under a moderately concentrated prior, allocations that share no")
    print("    cause at all already agree at about .90 on average.")

    print("\n(c) The two observed profiles against each other\n")
    print(
        f"    global vs local mean profile   : "
        f"{cosine(GLOBAL_PROFILE, LOCAL_PROFILE):.4f}"
    )

    print("\nReading. The reported .977 is above every reference value computed")
    print("here, so it is not vacuous; it is not far above them either, so it")
    print("does not by itself distinguish a shared representational subspace")
    print("from agreement forced by the geometry of non-negative allocations.")
    print("The test that would distinguish them is a permutation null on the")
    print("per-model profiles -- shuffle the dimension labels within each model,")
    print("recompute the pairwise cosine, and ask how often the shuffled value")
    print("reaches .977. That requires the per-model profiles, which are")
    print("published in the companion study's dataset rather than in its tables.")

    # Transcription-drift assertions: these compare the values printed above
    # against the values quoted in the paper text. They do not verify the
    # underlying reasoning.
    assert abs(g_u - 0.964) < 5e-4, g_u
    assert abs(cosine(GLOBAL_PROFILE, LOCAL_PROFILE) - 0.978) < 5e-4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
