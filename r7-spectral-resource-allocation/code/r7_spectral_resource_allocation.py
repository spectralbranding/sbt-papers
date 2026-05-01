"""
Companion Computation Script for R7: Spectral Resource Allocation
=================================================================
Paper: Spectral Resource Allocation: Demand-Driven Investment in Multi-Dimensional Brand Space
Author: Zharnikov, D. (2026k). https://doi.org/10.5281/zenodo.19009268

Run command:
    cd /Users/d/projects/spectral-branding && uv run python research/computation_scripts/r7_spectral_resource_allocation.py

Reproduces:
    - Table 7 (Appendix A.2): alignment-gap computations for all five brands
    - Theorem 1 optimal allocation under uniform costs
    - Theorem 5 cohort-interaction effects (heritage premium / luxury paradox examples)

Fixed seed: SEED = 42 (used for any stochastic elements; all computations here are deterministic)
"""

import numpy as np

SEED = 42
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------------------
# Canonical brand emission profiles (Zharnikov 2026a, 2026d)
# Dimensions: Semiotic, Narrative, Ideological, Experiential, Social,
#             Economic, Cultural, Temporal
# ---------------------------------------------------------------------------
DIMENSIONS = [
    "Semiotic",
    "Narrative",
    "Ideological",
    "Experiential",
    "Social",
    "Economic",
    "Cultural",
    "Temporal",
]

EMISSION_PROFILES = {
    "Hermes": np.array([9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]),
    "IKEA": np.array([8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]),
    "Patagonia": np.array([6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]),
    "Erewhon": np.array([7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5]),
    "Tesla": np.array([7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]),
}

# ---------------------------------------------------------------------------
# Hypothetical founder profiles (from paper §9.2; simplex-normalised)
# ---------------------------------------------------------------------------
FOUNDER_PROFILES_RAW = {
    "Hermes": np.array([0.20, 0.15, 0.10, 0.20, 0.15, 0.02, 0.10, 0.08]),
    "IKEA": np.array([0.05, 0.05, 0.05, 0.10, 0.05, 0.50, 0.10, 0.10]),
    "Patagonia": np.array([0.05, 0.15, 0.30, 0.15, 0.10, 0.05, 0.10, 0.10]),
    "Erewhon": np.array([0.10, 0.05, 0.05, 0.30, 0.20, 0.05, 0.15, 0.10]),
    "Tesla": np.array([0.10, 0.20, 0.05, 0.30, 0.15, 0.05, 0.05, 0.10]),
}

# ---------------------------------------------------------------------------
# Hypothetical target cohort profiles (from paper §9.3; simplex-normalised)
# ---------------------------------------------------------------------------
COHORT_PROFILES_RAW = {
    "Hermes": np.array([0.18, 0.15, 0.08, 0.15, 0.18, 0.03, 0.13, 0.10]),
    "IKEA": np.array([0.10, 0.08, 0.05, 0.15, 0.07, 0.35, 0.10, 0.10]),
    "Patagonia": np.array([0.08, 0.12, 0.20, 0.15, 0.12, 0.08, 0.10, 0.15]),
    "Erewhon": np.array([0.10, 0.08, 0.05, 0.25, 0.20, 0.07, 0.15, 0.10]),
    "Tesla": np.array([0.12, 0.15, 0.05, 0.20, 0.18, 0.12, 0.08, 0.10]),
}


def normalise(v: np.ndarray) -> np.ndarray:
    """Project raw weight vector onto probability simplex (L1 normalisation)."""
    total = v.sum()
    assert total > 0, "Weight vector must be positive"
    return v / total


def hellinger(p: np.ndarray, q: np.ndarray) -> float:
    """Hellinger distance between two probability vectors."""
    return (1.0 / np.sqrt(2.0)) * np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2))


def fisher_rao(p: np.ndarray, q: np.ndarray) -> float:
    """Fisher-Rao (geodesic) distance on the probability simplex."""
    bc = np.sum(np.sqrt(p * q))
    bc = np.clip(bc, -1.0, 1.0)  # guard against floating-point overshoot
    return 2.0 * np.arccos(bc)


def alignment_gap(
    wf: np.ndarray, wc: np.ndarray, lam: float = 1.0, alpha_bar: float = 1.0
) -> dict:
    """
    Compute alignment gap A(f,c) = ||w(f)||^2 - <w(f), w(c)>
    under uniform quadratic costs (alpha_i = alpha_bar, lambda = lam).

    Returns dict with all intermediate and final values.
    """
    norm_sq_f = float(np.dot(wf, wf))
    inner_fc = float(np.dot(wf, wc))
    gap = (norm_sq_f - inner_fc) / (lam * alpha_bar)
    h = hellinger(wf, wc)
    fr = fisher_rao(wf, wc)
    return {
        "norm_sq_f": norm_sq_f,
        "inner_fc": inner_fc,
        "gap": gap,
        "hellinger": h,
        "fisher_rao": fr,
    }


def theorem1_optimal_allocation(
    wc: np.ndarray, lam: float = 1.0, alpha: np.ndarray = None
) -> np.ndarray:
    """
    Theorem 1: s_i* = w_i(c) / (lambda * alpha_i)
    Default: uniform alpha_i = 1.
    """
    if alpha is None:
        alpha = np.ones(8)
    return wc / (lam * alpha)


def theorem5_optimal_allocation(
    wc: np.ndarray,
    W_interaction: np.ndarray,
    lam: float = 1.0,
    alpha: np.ndarray = None,
) -> np.ndarray:
    """
    Theorem 5: (Lambda - W) s* = w(c)
    Lambda = lam * diag(alpha), W = interaction matrix (symmetric, zero diagonal).

    Returns s* = (Lambda - W)^{-1} w(c).
    Raises ValueError if Lambda - W is not positive definite.
    """
    if alpha is None:
        alpha = np.ones(8)
    Lambda = lam * np.diag(alpha)
    M = Lambda - W_interaction
    eigvals = np.linalg.eigvalsh(M)
    if np.any(eigvals <= 0):
        raise ValueError(
            f"Lambda - W is not positive definite (min eigenvalue = {eigvals.min():.6f}). "
            "Increase lambda or reduce interaction weights."
        )
    s_star = np.linalg.solve(M, wc)
    return s_star


# ---------------------------------------------------------------------------
# Heritage premium (Hermès) and Luxury paradox (Tesla) interaction matrices
# ---------------------------------------------------------------------------
def hermes_interaction_matrix(w_nt: float = 0.05) -> np.ndarray:
    """
    Heritage premium: w_{narrative, temporal} = +w_nt > 0.
    Indices: narrative=1, temporal=7 (0-based).
    All other off-diagonal entries = 0.
    """
    W = np.zeros((8, 8))
    W[1, 7] = w_nt
    W[7, 1] = w_nt
    return W


def tesla_interaction_matrix(w_it: float = -0.03) -> np.ndarray:
    """
    Luxury paradox: w_{ideological, temporal} = w_it < 0.
    Indices: ideological=2, temporal=7 (0-based).
    All other off-diagonal entries = 0.
    """
    W = np.zeros((8, 8))
    W[2, 7] = w_it
    W[7, 2] = w_it
    return W


# ---------------------------------------------------------------------------
# Main: run all computations and print canonical output table
# ---------------------------------------------------------------------------
def main() -> None:
    print("=" * 72)
    print("R7 Spectral Resource Allocation — Companion Computation Script")
    print("SEED =", SEED)
    print("=" * 72)

    brands = ["Hermes", "IKEA", "Patagonia", "Erewhon", "Tesla"]

    # Normalise profiles onto simplex
    founders = {b: normalise(FOUNDER_PROFILES_RAW[b]) for b in brands}
    cohorts = {b: normalise(COHORT_PROFILES_RAW[b]) for b in brands}

    # ------------------------------------------------------------------
    # TABLE A: Alignment Gap Results (Table 7 / Appendix A.2)
    # ------------------------------------------------------------------
    print("\n--- Table 7 / Appendix A.2: Alignment Gap (lambda=1, alpha_bar=1) ---\n")
    header = f"{'Brand':<12} {'||w(f)||^2':>12} {'<w(f),w(c)>':>13} {'A(f,c)':>10} {'H(f,c)':>10} {'d_FR':>8}"
    print(header)
    print("-" * len(header))

    results = {}
    for b in brands:
        wf = founders[b]
        wc = cohorts[b]
        r = alignment_gap(wf, wc)
        results[b] = r
        print(
            f"{b:<12} {r['norm_sq_f']:>12.6f} {r['inner_fc']:>13.6f} "
            f"{r['gap']:>10.6f} {r['hellinger']:>10.6f} {r['fisher_rao']:>8.6f}"
        )

    # Rank order by alignment gap
    rank = sorted(brands, key=lambda b: results[b]["gap"])
    print(f"\nRank order (ascending alignment gap): {' < '.join(rank)}")
    gap_str = " < ".join(f"{results[b]['gap']:.4f}" for b in rank)
    print(f"Values: {gap_str}")

    # ------------------------------------------------------------------
    # TABLE B: Theorem 1 Optimal Allocation (uniform costs)
    # ------------------------------------------------------------------
    print(
        "\n--- Theorem 1: Optimal Allocation s_i* = w_i(c) / alpha_i (lambda=1) ---\n"
    )
    dim_abbrev = ["Sem", "Nar", "Ide", "Exp", "Soc", "Eco", "Cul", "Tem"]
    col_w = 6
    header2 = f"{'Brand':<12}" + "".join(f"{d:>{col_w}}" for d in dim_abbrev)
    print(header2)
    print("-" * len(header2))
    for b in brands:
        s_star = theorem1_optimal_allocation(cohorts[b])
        row = f"{b:<12}" + "".join(f"{v:>{col_w}.4f}" for v in s_star)
        print(row)

    # ------------------------------------------------------------------
    # TABLE C: Theorem 5 — Interaction-adjusted allocation
    # ------------------------------------------------------------------
    print("\n--- Theorem 5: Interaction-Adjusted Allocation ---\n")

    # Hermès: heritage premium
    W_hermes = hermes_interaction_matrix(w_nt=0.05)
    s5_hermes = theorem5_optimal_allocation(cohorts["Hermes"], W_hermes)
    s1_hermes = theorem1_optimal_allocation(cohorts["Hermes"])
    delta_hermes = s5_hermes - s1_hermes

    print("Hermès (heritage premium: w_narrative,temporal = +0.05)")
    print(f"  {'Dim':<14} {'s*(linear)':>12} {'s*(interact.)':>14} {'delta':>10}")
    for i, d in enumerate(DIMENSIONS):
        print(
            f"  {d:<14} {s1_hermes[i]:>12.6f} {s5_hermes[i]:>14.6f} {delta_hermes[i]:>10.6f}"
        )

    # Tesla: luxury paradox
    W_tesla = tesla_interaction_matrix(w_it=-0.03)
    s5_tesla = theorem5_optimal_allocation(cohorts["Tesla"], W_tesla)
    s1_tesla = theorem1_optimal_allocation(cohorts["Tesla"])
    delta_tesla = s5_tesla - s1_tesla

    print("\nTesla (luxury paradox: w_ideological,temporal = -0.03)")
    print(f"  {'Dim':<14} {'s*(linear)':>12} {'s*(interact.)':>14} {'delta':>10}")
    for i, d in enumerate(DIMENSIONS):
        print(
            f"  {d:<14} {s1_tesla[i]:>12.6f} {s5_tesla[i]:>14.6f} {delta_tesla[i]:>10.6f}"
        )

    # ------------------------------------------------------------------
    # Appendix A.2 step-by-step arithmetic (per-brand)
    # ------------------------------------------------------------------
    print("\n--- Appendix A.2: Step-by-Step Arithmetic ---\n")
    for b in brands:
        wf = founders[b]
        wc = cohorts[b]
        norm_sq = np.sum(wf**2)
        inner = np.dot(wf, wc)
        gap = norm_sq - inner
        h = hellinger(wf, wc)
        terms_norm = " + ".join(f"{wf[i]:.4f}^2" for i in range(8))
        print(f"{b}:")
        print(f"  ||w(f)||^2 = {terms_norm}")
        print(f"           = {norm_sq:.6f}")
        inner_terms = " + ".join(f"{wf[i]:.4f}*{wc[i]:.4f}" for i in range(8))
        print(f"  <w(f),w(c)> = {inner_terms}")
        print(f"             = {inner:.6f}")
        print(f"  A(f,c) = {norm_sq:.6f} - {inner:.6f} = {gap:.6f}")
        print(f"  H(f,c) = {h:.6f}")
        print()

    print("=" * 72)
    print("All computations complete.")


if __name__ == "__main__":
    main()
