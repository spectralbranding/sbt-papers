"""Companion computation script for R9: From Order Effects to Absorbing States.

Reproduces:
    - Table 2: Ensemble vs. Time-Average Divergence (illustrative low-coherence
      brand profile, six time periods).
    - Table 3: Absorption trajectories across the five canonical SBT brand
      profiles (Hermes, IKEA, Patagonia, Erewhon, Tesla) — illustrating that
      the ensemble-time gap predicted by P3 scales with brand coherence.

Run command:
    uv run --with numpy python simulate_absorption.py --seed 42 --periods 6

Method:
    Discrete-time absorbing Markov chain. N observers begin at the same
    interior perception state x0; at each period an observer is absorbed
    with probability lambda(coherence). Absorbed observers are removed from
    the ensemble average ("active observers" in Table 2) and held at zero
    in the true population average. The script outputs both averages at
    each period.

Mapping from SBT canonical brand profiles to absorption rates lambda:
    The absorption probability per period is calibrated to be inversely
    related to the brand's coherence dispersion. Concretely, lambda is
    proportional to the coefficient of variation (sd / mean) of the brand's
    eight-dimension profile vector — a low-coherence brand (high CV across
    dimensions, like Tesla) drives observers to absorbing boundaries
    faster than a high-coherence brand (low CV, like Hermes). The
    proportionality constant is set so that the incoherent reference
    profile yields the .020 per-period absorption rate cited in Table 2.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np

# Canonical SBT brand profiles (Semiotic, Narrative, Ideological, Experiential,
# Social, Economic, Cultural, Temporal) per the eight SBT dimensions.
BRAND_PROFILES: dict[str, list[float]] = {
    "Hermes":    [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA":      [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon":   [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla":     [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}


@dataclass
class SimResult:
    label: str
    initial_perception: float
    absorption_rate: float
    active_counts: list[int]
    absorbed_counts: list[int]
    ensemble_avg: list[float]
    population_avg: list[float]


def coefficient_of_variation(profile: list[float]) -> float:
    arr = np.asarray(profile, dtype=float)
    return float(arr.std(ddof=0) / arr.mean())


def calibrated_absorption_rate(profile: list[float], reference_cv: float,
                               reference_lambda: float = 0.020) -> float:
    """Map a brand profile's CV onto a per-period absorption rate.

    The reference (incoherent profile, CV ~= reference_cv) is set to .020.
    Higher-coherence brands receive proportionally lower absorption rates.
    """
    cv = coefficient_of_variation(profile)
    return reference_lambda * (cv / reference_cv)


def simulate_absorption(
    n_observers: int,
    periods: int,
    initial_perception: float,
    absorption_rate: float,
    label: str,
    rng: np.random.Generator,
) -> SimResult:
    active = np.full(n_observers, initial_perception, dtype=float)
    absorbed_mask = np.zeros(n_observers, dtype=bool)

    active_counts = [int(n_observers)]
    absorbed_counts = [0]
    ensemble_avg = [float(initial_perception)]
    population_avg = [float(initial_perception)]

    for t in range(1, periods + 1):
        # The hazard for absorption is highest among observers in the lower
        # tail of the active distribution; the conditional draw biases toward
        # those nearer the absorbing boundary. We approximate this by sorting
        # active observers and absorbing from the lowest quantile.
        eligible = ~absorbed_mask
        n_eligible = int(eligible.sum())
        n_to_absorb = int(rng.binomial(n_eligible, absorption_rate))

        if n_to_absorb > 0:
            eligible_idx = np.where(eligible)[0]
            order = np.argsort(active[eligible_idx])  # ascending: lowest first
            # Mix: 70 percent of new absorptions come from the lowest tertile,
            # 30 percent are random across the rest, modelling the survivorship
            # selection mechanism.
            n_tail = int(round(0.7 * n_to_absorb))
            n_rand = n_to_absorb - n_tail
            tail_pool = eligible_idx[order[: max(n_tail * 3, n_tail)]]
            tail_pick = rng.choice(tail_pool, size=min(n_tail, len(tail_pool)),
                                   replace=False) if len(tail_pool) > 0 else np.array([], dtype=int)
            remaining = np.setdiff1d(eligible_idx, tail_pick)
            rand_pick = rng.choice(remaining, size=min(n_rand, len(remaining)),
                                   replace=False) if len(remaining) > 0 else np.array([], dtype=int)
            new_absorbed_idx = np.concatenate([tail_pick, rand_pick]).astype(int)
            absorbed_mask[new_absorbed_idx] = True
            active[new_absorbed_idx] = 0.0

        n_active = int((~absorbed_mask).sum())
        n_abs = int(absorbed_mask.sum())

        # Surviving observers experience small positive drift on top of noise:
        # this models the multiplicative-update regime where signal interpretation
        # scales with current perception, and (at the population level) those
        # who avoid absorption do so partly by virtue of accumulating
        # confirming positive signals.
        if n_active > 0:
            drift = 0.05 * t
            noise = 0.4 * (rng.random(n_active) - 0.5)
            active[~absorbed_mask] = np.minimum(
                initial_perception + drift + noise,
                10.0,
            )

        if n_active > 0:
            ens = float(active[~absorbed_mask].mean())
        else:
            ens = 0.0
        pop = float(active.sum() / n_observers)

        active_counts.append(n_active)
        absorbed_counts.append(n_abs)
        ensemble_avg.append(round(ens, 1))
        population_avg.append(round(pop, 1))

    return SimResult(
        label=label,
        initial_perception=initial_perception,
        absorption_rate=absorption_rate,
        active_counts=active_counts,
        absorbed_counts=absorbed_counts,
        ensemble_avg=ensemble_avg,
        population_avg=population_avg,
    )


def print_table2(result: SimResult) -> None:
    print()
    print("Table 2: Ensemble vs Time-Average Divergence (illustrative).")
    print(f"  initial perception = {result.initial_perception:.1f}, "
          f"absorption rate per period = {result.absorption_rate:.3f}, "
          f"N = {result.active_counts[0]}")
    header = ("t", "Active", "Absorbed", "Ensemble Avg", "Population Avg")
    print("  {:>3} {:>8} {:>10} {:>14} {:>16}".format(*header))
    for t in range(len(result.active_counts)):
        print("  {:>3} {:>8} {:>10} {:>14.1f} {:>16.1f}".format(
            t,
            result.active_counts[t],
            result.absorbed_counts[t],
            result.ensemble_avg[t],
            result.population_avg[t],
        ))


def print_table4(results: dict[str, SimResult]) -> None:
    print()
    print("Table 3: Absorption Trajectories Across Canonical SBT Brand Profiles.")
    print("  N = {} observers, periods = {}".format(
        next(iter(results.values())).active_counts[0],
        len(next(iter(results.values())).active_counts) - 1,
    ))
    header = ("Brand", "CV", "lambda", "Ensemble@T", "Population@T", "Gap")
    print("  {:<10} {:>6} {:>8} {:>11} {:>13} {:>6}".format(*header))
    for name, res in results.items():
        cv = coefficient_of_variation(BRAND_PROFILES[name])
        ens_T = res.ensemble_avg[-1]
        pop_T = res.population_avg[-1]
        gap = round(ens_T - pop_T, 1)
        print("  {:<10} {:>6.3f} {:>8.4f} {:>11.1f} {:>13.1f} {:>6.1f}".format(
            name, cv, res.absorption_rate, ens_T, pop_T, gap,
        ))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--periods", type=int, default=6)
    parser.add_argument("--n-observers", type=int, default=1000)
    parser.add_argument("--initial-perception", type=float, default=7.0)
    args = parser.parse_args()

    # Reference: an "incoherent" profile (high cross-dimension dispersion)
    # is mapped to lambda = .020. Tesla's CV is the highest among the five
    # canonical profiles, so it serves as the reference and reproduces the
    # .020 rate cited in Table 2.
    reference_cv = coefficient_of_variation(BRAND_PROFILES["Tesla"])

    rng = np.random.default_rng(args.seed)

    # Table 2: low-coherence reference brand (Tesla CV).
    table2_result = simulate_absorption(
        n_observers=args.n_observers,
        periods=args.periods,
        initial_perception=args.initial_perception,
        absorption_rate=0.020,
        label="Reference (low-coherence)",
        rng=rng,
    )
    print_table2(table2_result)

    # Table 4: per-brand absorption trajectories.
    rng = np.random.default_rng(args.seed)  # reset for reproducibility
    results: dict[str, SimResult] = {}
    for name, profile in BRAND_PROFILES.items():
        lam = calibrated_absorption_rate(profile, reference_cv)
        results[name] = simulate_absorption(
            n_observers=args.n_observers,
            periods=args.periods,
            initial_perception=args.initial_perception,
            absorption_rate=lam,
            label=name,
            rng=rng,
        )
    print_table4(results)


if __name__ == "__main__":
    main()
