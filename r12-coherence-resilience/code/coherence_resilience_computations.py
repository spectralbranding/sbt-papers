"""
Companion computation script for Zharnikov (2026s) "Coherence Type as Crisis Predictor."

Reproduces the inline numerical values cited in the paper body:

  - per-brand sum of emissions (sum_i s_i) used in section 2.3 and section 6.4
  - per-brand variance Var(s_i) used in section 2.3 (Tesla) and section 6.4 (Tesla)
  - per-brand floor-crossing count k(alpha; alpha_min) used in Definition 1 (the
    (alpha_min, k)-robust criterion adopted for the case analysis)

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
    "Hermes":     (9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5),
    "IKEA":       (8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0),
    "Patagonia":  (6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5),
    "Erewhon":    (7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5),
    "Tesla":      (7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0),
}

# Working floor for the (alpha_min, k)-robust drift criterion.
# Section 2.1 sets alpha_i = gamma * s_i * h(x_i) with h(x_i) = x_i (Wright-Fisher).
# The working floor adopted in Definition 1 corresponds to s_i = 3.0 at the neutral
# prior x_i^* = 1 / sqrt(8). Both gamma and x_i^* are positive constants common to
# every brand, so the floor-crossing count k(alpha; alpha_min) reduces to counting
# dimensions with s_i >= 3.0.
EMISSION_FLOOR: float = 3.0


def floor_crossing_count(profile: tuple[float, ...], floor: float = EMISSION_FLOOR) -> int:
    """Number of dimensions with emission s_i >= floor (k in Definition 1)."""
    return sum(1 for s_i in profile if s_i >= floor)


def population_variance(profile: tuple[float, ...]) -> float:
    """Population variance Var(s_i) used in section 2.3 (Tesla note) and section 6.4."""
    return statistics.pvariance(profile)


def main() -> None:
    print(f"Working emission floor: s_i >= {EMISSION_FLOOR} (floor-crossing count k)")
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


if __name__ == "__main__":
    main()
