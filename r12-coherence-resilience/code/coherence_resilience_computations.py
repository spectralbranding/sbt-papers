"""
Companion computation script for Zharnikov (2026s) "Coherence Type as Crisis Predictor."

Reproduces the inline numerical values cited in the paper body:

  - per-brand sum of emissions (sum_i s_i) used in section 2.3 and section 6.4
  - per-brand variance Var(s_i) used in section 2.3 (Tesla) and section 6.4 (Tesla)
  - per-brand floor-crossing count k(alpha; alpha_min) used in Definition 1 (the
    (alpha_min, k)-robust criterion adopted for the case analysis), at the
    derived floor s_crit = delta / gamma = 2.5

The five canonical brand profiles are the SBT canonical reference set
(Hermes, IKEA, Patagonia, Erewhon, Tesla); see Zharnikov (2026d) for the
metric on the eight-dimensional brand space. Dimensions are ordered:
Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural,
Temporal.

Run:

  uv run python code/coherence_resilience_computations.py

No arguments. No external dependencies beyond the Python standard library.
Deterministic output (no randomness; floating-point arithmetic only).
"""

from __future__ import annotations

import statistics

# Canonical emission profiles. Order matters:
# (Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal)
PROFILES: dict[str, tuple[float, ...]] = {
    "Hermes": (9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5),
    "IKEA": (8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0),
    "Patagonia": (6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5),
    "Erewhon": (7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5),
    "Tesla": (7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0),
}

# Derived floor for the (alpha_min, k)-robust drift criterion (Definition 1).
# Section 2.1 sets alpha_i = gamma * s_i * h(x_i) with h(x_i) = x_i (Wright-Fisher).
# The floor is the emission at which the signal-driven drift's marginal contribution
# to mu_i equals the decay drift's restoring rate: gamma * s_crit = delta, so
# s_crit = delta / gamma and alpha_min = delta * h(x*). Because gamma, delta and the
# neutral prior x_i^* = 1 / sqrt(8) are common to every brand, the floor-crossing
# count k(alpha; alpha_min) reduces to counting dimensions with s_i >= s_crit.
# (An earlier version used s_i = 3.0, Hermes's own weakest emission, so the exemplar
# cleared the floor by construction; that assigned floor is withdrawn.)
GAMMA: float = 0.020  # signal-driven drift coefficient (working parameter)
DELTA: float = 0.050  # decay rate toward the prior (working parameter)
EMISSION_FLOOR: float = DELTA / GAMMA  # s_crit = 2.5

# Floor-crossing counts k at s_crit = 2.5, as printed in the paper.
PAPER_K: dict[str, int] = {
    "Hermes": 8,
    "IKEA": 8,
    "Patagonia": 8,
    "Erewhon": 8,
    "Tesla": 7,
}


def floor_crossing_count(
    profile: tuple[float, ...], floor: float = EMISSION_FLOOR
) -> int:
    """Number of dimensions with emission s_i >= floor (k in Definition 1)."""
    return sum(1 for s_i in profile if s_i >= floor)


def population_variance(profile: tuple[float, ...]) -> float:
    """Population variance Var(s_i) used in section 2.3 (Tesla note) and section 6.4."""
    return statistics.pvariance(profile)


def main() -> None:
    print(
        f"Derived emission floor: s_i >= s_crit = delta / gamma = {DELTA} / {GAMMA} "
        f"= {EMISSION_FLOOR:.1f} (floor-crossing count k)"
    )
    print()
    header = f"{'Brand':<10} {'sum_i s_i':>10} {'mean':>8} {'Var(s_i)':>10} {'k':>3}"
    print(header)
    print("-" * len(header))
    for brand, profile in PROFILES.items():
        total = sum(profile)
        mean = total / len(profile)
        var = population_variance(profile)
        k = floor_crossing_count(profile)
        print(f"{brand:<10} {total:>10.1f} {mean:>8.3f} {var:>10.3f} {k:>3d}")
        assert k == PAPER_K[brand], f"{brand}: k = {k}, paper prints {PAPER_K[brand]}"
    assert abs(EMISSION_FLOOR - 2.5) < 1e-12
    print()
    print("Floor-crossing counts match the paper (8 / 8 / 8 / 8 / 7).")


if __name__ == "__main__":
    main()
