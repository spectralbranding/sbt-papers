#!/usr/bin/env python3
"""Counterexample to 2026k (R7) Theorem 2, the alignment-gap lower bound.

Theorem 2 as published in v1.0.0 stated, for a founder weight profile
w(f) and a cohort weight profile w(c) on the probability simplex Delta^7:

    A(f, c)  >=  H(f, c)^2 / (2 * lambda * alpha_bar)

with A(f, c) proportional to <w(f), w(f) - w(c)> and H the Hellinger distance.

THE COUNTEREXAMPLE.  Put the founder at the simplex barycentre, w(f)_i = 1/8.
Then <w(f), w(f) - w(c)> = (1/8) * (1 - sum_i w_i(c)) = 0 for EVERY w(c), because
simplex weights sum to one.  The left-hand side is identically zero along a whole
family while the right-hand side is strictly positive, so the inequality fails on
an open set of cohorts, not at an isolated boundary point.

TWO ERRORS PRODUCE IT, both in the v1.0.0 Appendix A.1 derivation:

  1. The step "the L^2 distance on the simplex satisfies ||p - q||^2 >= 2H(p,q)^2
     (a standard inequality)" uses the wrong norm.  The standard result is the
     L^1 one, ||p - q||_1 >= 2H^2, which routes through total variation.  This
     script checks both.

  2. The exact identity
         ||w(f)||^2 - <w(f), w(c)> = (1/2)||w(f) - w(c)||^2
                                     + (1/2)(||w(f)||^2 - ||w(c)||^2)
     is used with the second term dropped as if non-negative.  It is negative
     whenever the cohort is more concentrated than the founder, which is exactly
     the case the counterexample builds.

This script does not check the repair.  The corrected Theorem 2 of v2.0.0
adds the hypothesis ||w(c)|| <= ||w(f)|| and moves the Hellinger step to L^1;
it is checked by the companion script's --verify-theorem2 mode
(r7_spectral_resource_allocation.py).

    uv run --with numpy python falsification_sweep_2026k_theorem2.py
"""

from __future__ import annotations

import numpy as np

SEED = 20260823  # fixed, though nothing below is stochastic except the sweep


def alignment_gap(wf: np.ndarray, wc: np.ndarray) -> float:
    """A(f, c) up to the positive factor 1 / (lambda * alpha_bar)."""
    return float(wf @ (wf - wc))


def hellinger_sq(wf: np.ndarray, wc: np.ndarray) -> float:
    """H(f, c)^2 = (1/2) * ||sqrt(wf) - sqrt(wc)||_2^2."""
    return float(0.5 * np.sum((np.sqrt(wf) - np.sqrt(wc)) ** 2))


def main() -> int:
    n = 8
    uniform = np.full(n, 1.0 / n)

    print("A. The published bound, founder at the barycentre")
    print("   (lambda * alpha_bar set to 1; it is a positive factor on both sides)\n")
    print(f"   {'cohort':<34}{'A(f,c)':>12}{'H^2/2':>12}   holds?")
    rows = []
    for eps in (0.0, 1e-6, 1e-3, 1e-2, 5e-2, 0.25):
        wc = np.full(n, eps / (n - 1))
        wc[0] = 1.0 - eps
        rows.append((f"(1-{eps:g}, {eps:g}/7, ...)", uniform, wc))
    for label, wf, wc in rows:
        a, h = alignment_gap(wf, wc), hellinger_sq(wf, wc) / 2
        print(f"   {label:<34}{a:>12.6f}{h:>12.6f}   {a >= h}")

    print("\n   Every row fails, and A is exactly zero throughout: for a uniform")
    print("   founder the gap vanishes against any cohort on the simplex.\n")

    print("B. The 'standard inequality' step, at w(c) = e_1\n")
    wc = np.zeros(n)
    wc[0] = 1.0
    l2sq = float(np.sum((uniform - wc) ** 2))
    l1 = float(np.sum(np.abs(uniform - wc)))
    two_h2 = 2 * hellinger_sq(uniform, wc)
    print(
        f"   ||p-q||_2^2 = {l2sq:.6f}   2H^2 = {two_h2:.6f}   L^2 form holds? {l2sq >= two_h2}"
    )
    print(
        f"   ||p-q||_1   = {l1:.6f}   2H^2 = {two_h2:.6f}   L^1 form holds? {l1 >= two_h2}"
    )

    print("\nC. The dropped term in the identity, same pair\n")
    dropped = 0.5 * (float(uniform @ uniform) - float(wc @ wc))
    print(f"   (1/2)(||w(f)||^2 - ||w(c)||^2) = {dropped:.6f}")
    print("   Negative, and larger in magnitude than the gap it was dropped from.\n")

    print("D. How common is the failure? Random cohorts against a uniform founder\n")
    rng = np.random.default_rng(SEED)
    draws = rng.dirichlet(np.ones(n), size=100_000)
    fails = sum(
        1 for wc in draws if alignment_gap(uniform, wc) < hellinger_sq(uniform, wc) / 2
    )
    print(f"   {fails} of {len(draws)} uniform-Dirichlet cohorts violate the bound.")
    print("   The failure is generic for this founder, not a corner case.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
