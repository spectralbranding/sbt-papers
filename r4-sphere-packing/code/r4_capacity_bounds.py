"""
R4 Companion Computation Script — Sphere-Packing Bounds for Brand Positioning Capacity
=====================================================================================
Companion to:
  Zharnikov, D. (2026g). How Many Brands Can a Market Hold? Sphere Packing Bounds
  for Multi-Dimensional Positioning. Working Paper v1.2.0.
  https://doi.org/10.5281/zenodo.18945522

Independently RECOMPUTES (does not hard-code) every numerical value cited in the
paper from the documented mathematics, then compares computed-vs-reported and
flags any mismatch. Reproduces:

  - Table 2 : Unit ball volume V_n(1) for n in {1,2,3,4,5,8,16,24,48}
  - Table 4 : Positioning capacity bounds, lower (1/eps)^8 and upper ((2+eps)/eps)^8
  - Table 6 : White-space fractions 1 - n_b * eps^8 (eps = .10)
  - Table 7 : Category saturation thresholds (1/eps)^d_eff
  - Table 8 : Effective dimensionality d_eff = trace/lambda_max = n/(1+(n-1)rho)
              and capacity-collapse values (1/eps)^d_eff
  - Appendix A1 : Key numerical values (V_8(1), Delta_8, kissing number, ...)
  - Appendix B1 : Dimensional capacity lower bounds (1/eps)^n
  - Figure 1   : kissing-shell decomposition 240 = 112 + 128 (deterministic E8
                 minimal-vector enumeration at squared norm 2)
  - In-text    : E8 packing density Delta_8 = pi^4/384 ~ .2537; N_E8 at eps=.10 ~ 6.49e9;
                 corner effect V_8(1)/2^8; mean radius sqrt(8/10) of uniform 8-ball point

Random seed: 42 (no stochastic computations — all results are closed-form or exact
             integer enumeration; the seed is fixed per repository reproducibility
             policy).

Run command:
  uv run --with numpy --with scipy python r4_capacity_bounds.py

The script exposes, per the paper's "Companion Computation Script" subsection:
  - V_n(r)              -- ball_volume(n, r)
  - d_eff(n, rho)       -- effective dimensionality the paper TABULATES,
                           trace/lambda_max = n/(1+(n-1)rho) (the alternative
                           participation ratio (sum lam)^2/sum(lam^2) is computed
                           alongside for transparency; it yields larger values)
  - simple_lower_bound  -- (1/eps)^n
  - covering_upper_bound-- ((2+eps)/eps)^n
  - e8_capacity_estimate-- Delta_8 * V_n(1) / V_n(eps/2)
  - enumerate_e8_minimal_vectors() -- deterministic 112 + 128 = 240 enumeration

Discrepancies between computed and paper-reported values are printed as MISMATCH
with the magnitude of the gap; the script never alters a formula to force a match.
"""

import math
from itertools import combinations, product

import numpy as np
from scipy.special import gamma as gamma_func

SEED = 42
rng = np.random.default_rng(SEED)

# Tolerance for declaring MATCH: relative (for nonzero) or absolute (for small).
REL_TOL = 5e-3  # .5% — paper reports values to ~3 significant figures
ABS_TOL = 5e-4


# ---------------------------------------------------------------------------
# Comparison helper
# ---------------------------------------------------------------------------

_results = []  # collected (label, computed, reported, status) for the final summary


def _fmt(x):
    if x is None:
        return "—"
    if isinstance(x, str):
        return x
    ax = abs(x)
    if ax != 0 and (ax < 1e-3 or ax >= 1e5):
        return f"{x:.4e}"
    return f"{x:.4f}"


def compare(label, computed, reported, rel_tol=REL_TOL, abs_tol=ABS_TOL, note=""):
    """Record a computed-vs-reported comparison. reported=None => no paper claim."""
    if reported is None:
        status = "INFO"
    else:
        denom = abs(reported)
        if denom == 0:
            status = "MATCH" if abs(computed - reported) <= abs_tol else "MISMATCH"
        else:
            rel = abs(computed - reported) / denom
            status = (
                "MATCH"
                if (rel <= rel_tol or abs(computed - reported) <= abs_tol)
                else "MISMATCH"
            )
    _results.append((label, computed, reported, status, note))
    flag = {"MATCH": "OK ", "MISMATCH": "XX ", "INFO": "   "}[status]
    line = f"  [{flag}] {label:<46} computed={_fmt(computed):>13}  paper={_fmt(reported):>13}"
    if note:
        line += f"   ({note})"
    print(line)
    return status


# ---------------------------------------------------------------------------
# Core geometry helpers
# ---------------------------------------------------------------------------


def unit_ball_volume(n):
    """Volume of the unit ball in R^n: V_n(1) = pi^(n/2) / Gamma(n/2 + 1)."""
    return math.pi ** (n / 2.0) / gamma_func(n / 2.0 + 1.0)


def ball_volume(n, r):
    """Volume of a ball of radius r in R^n: V_n(r) = V_n(1) * r^n."""
    return unit_ball_volume(n) * r**n


def simple_lower_bound(eps, n=8):
    """Simple volume lower bound on packing number: N >= (1/eps)^n.

    Derivation (paper, Packing Density Bounds): each brand occupies an eps/2-ball;
    N * V_n(eps) >= V_n(1) with V_n(eps) = V_n(1) * eps^n, so N >= (1/eps)^n.
    """
    return (1.0 / eps) ** n


def covering_upper_bound(eps, n=8):
    """Covering upper bound: N <= ((2+eps)/eps)^n.

    Each eps/2-ball centred in B(0,1) lies in B(0, 1+eps/2); disjointness gives
    N <= V_n(1+eps/2)/V_n(eps/2) = ((1+eps/2)/(eps/2))^n = ((2+eps)/eps)^n.
    """
    return ((2.0 + eps) / eps) ** n


def equicorr_eigenvalues(n, rho):
    """Eigenvalues of the n x n equicorrelation matrix (1 on diagonal, rho off):
    one value 1 + (n-1)rho and (n-1) values 1 - rho.
    """
    return np.array([1.0 + (n - 1) * rho] + [1.0 - rho] * (n - 1))


def d_eff_participation_ratio(n, rho):
    """Participation ratio of the equicorrelation matrix, computed directly from
    its eigenvalues: d_eff_PR = (sum lambda)^2 / sum(lambda^2).

    NOTE: this is an ALTERNATIVE effective-dimensionality measure (noted in the paper's
    Proposition 5 proof). It does NOT equal n/(1+(n-1)rho); the paper tabulates the
    trace/lambda_max measure instead (see d_eff_closed_form below). Computed here for
    transparency.
    """
    lam = equicorr_eigenvalues(n, rho)
    return float(lam.sum() ** 2 / np.square(lam).sum())


def d_eff_closed_form(n, rho):
    """The closed form n/(1+(n-1)rho) = trace / lambda_max that the paper TABULATES
    (Table 8) and uses for all capacity-collapse numbers.
    """
    return n / (1.0 + (n - 1) * rho)


# The paper's reported Table 8 values are reproduced by the closed form, so that is
# the d_eff(n, rho) the script exposes for capacity computation. The participation
# ratio is computed alongside (it differs — flagged as a discrepancy in main()).
def d_eff(n, rho):
    return d_eff_closed_form(n, rho)


# ---------------------------------------------------------------------------
# E8 packing density and minimal-vector enumeration
# ---------------------------------------------------------------------------

E8_DENSITY = math.pi**4 / 384.0  # Viazovska (2017): Delta_8 = pi^4/384


def e8_capacity_estimate(eps, n=8):
    """E8 packing-density estimate of capacity in the unit n-ball:
    N_E8 = Delta_8 * V_n(1) / V_n(eps/2).
    """
    return E8_DENSITY * ball_volume(n, 1.0) / ball_volume(n, eps / 2.0)


def enumerate_e8_minimal_vectors():
    """Deterministically enumerate the 240 minimal vectors of the E8 lattice at
    squared norm 2, decomposed into:

      (a) 112 "specialist" integer-coordinate vectors: exactly two nonzero
          coordinates, each +-1, six zeros. Count = C(8,2) * 2^2 = 28 * 4 = 112.
      (b) 128 "generalist" half-integer vectors: all eight coordinates +-1/2 with
          an EVEN number of minus signs. Count = 2^8 / 2 = 128.

    Returns (specialists, generalists) as lists of tuples; both verified to have
    squared norm exactly 2.
    """
    specialists = []
    for i, j in combinations(range(8), 2):  # 28 coordinate pairs
        for si, sj in product((+1, -1), repeat=2):  # 4 sign choices
            v = [0] * 8
            v[i] = si
            v[j] = sj
            specialists.append(tuple(v))

    generalists = []
    for signs in product((+1, -1), repeat=8):  # 256 sign patterns
        n_minus = sum(1 for s in signs if s < 0)
        if n_minus % 2 == 0:  # even parity -> 128 of them
            generalists.append(tuple(0.5 * s for s in signs))

    # Squared-norm check: every minimal vector must have ||v||^2 == 2.
    for v in specialists:
        assert abs(sum(c * c for c in v) - 2.0) < 1e-12
    for v in generalists:
        assert abs(sum(c * c for c in v) - 2.0) < 1e-12

    return specialists, generalists


# ---------------------------------------------------------------------------
# Table 2 — Unit ball volume V_n(1)
# ---------------------------------------------------------------------------


def table2_unit_ball_volume():
    print("\n--- Table 2: Unit Ball Volume V_n(1) ---")
    reported = {
        1: 2.000,
        2: 3.142,
        3: 4.189,
        4: 4.935,
        5: 5.264,
        8: 4.059,
        16: 0.2353,
        24: 1.930e-3,
        48: 1.377e-12,
    }
    for n in [1, 2, 3, 4, 5, 8, 16, 24, 48]:
        compare(f"V_{n}(1)", unit_ball_volume(n), reported[n])
    # Peak dimension check
    vols = {n: unit_ball_volume(n) for n in range(1, 13)}
    peak = max(vols, key=vols.get)
    compare(
        "argmax_n V_n(1) (peak dimension)",
        float(peak),
        5.0,
        note="paper: peak near n=5",
    )


# ---------------------------------------------------------------------------
# Table 4 — Positioning capacity bounds
# ---------------------------------------------------------------------------


def table4_capacity_bounds():
    print("\n--- Table 4: Positioning Capacity Bounds (n=8) ---")
    reported = {
        0.05: (2.56e10, 7.98e12),
        0.10: (1.00e8, 3.78e10),
        0.15: (3.90e6, 1.78e9),
        0.20: (3.91e5, 2.14e8),
        0.30: (1.52e4, 1.19e7),
        0.50: (2.56e2, 3.91e5),
    }
    for eps in [0.05, 0.10, 0.15, 0.20, 0.30, 0.50]:
        lo_r, hi_r = reported[eps]
        compare(f"lower (1/eps)^8 @ eps={eps}", simple_lower_bound(eps), lo_r)
        compare(f"upper ((2+eps)/eps)^8 @ eps={eps}", covering_upper_bound(eps), hi_r)


# ---------------------------------------------------------------------------
# Table 6 — White space fractions
# ---------------------------------------------------------------------------


def table6_white_space():
    print("\n--- Table 6: White Space Fraction at eps=.10 ---")
    eps = 0.10
    reported_pct = {
        100: 99.9999,
        1_000: 99.9990,
        10_000: 99.9900,
        100_000: 99.9000,
        1_000_000: 99.0000,
    }
    for n_b in [100, 1_000, 10_000, 100_000, 1_000_000]:
        f_white = (1.0 - n_b * eps**8) * 100.0
        compare(
            f"white-space % @ n_b={n_b}",
            f_white,
            reported_pct[n_b],
            rel_tol=1e-6,
            abs_tol=1e-3,
        )


# ---------------------------------------------------------------------------
# Table 7 — Category saturation thresholds
# ---------------------------------------------------------------------------


def table7_saturation():
    print("\n--- Table 7: Category Saturation Capacity (1/eps)^d_eff at eps=.10 ---")
    eps = 0.10
    reported = {2: 100.0, 3: 1_000.0, 5: 100_000.0, 8: 1e8}
    for deff, rep in reported.items():
        compare(
            f"saturation capacity @ d_eff={deff}", simple_lower_bound(eps, deff), rep
        )


# ---------------------------------------------------------------------------
# Table 8 — Effective dimensionality and capacity collapse
# ---------------------------------------------------------------------------


def table8_effective_dimensionality():
    print(
        "\n--- Table 8: Effective Dimensionality & Capacity Collapse (n=8, eps=.10) ---"
    )
    eps = 0.10
    n = 8
    # (rho, reported d_eff, reported capacity exponent as written in the table)
    reported = {
        0.0: (8.00, 1e8),
        0.1: (4.71, 1e5),
        0.2: (3.33, 1e3),
        0.3: (2.58, 1e3),
        0.5: (1.78, 1e2),
        0.7: (1.36, 1e1),
    }
    for rho, (deff_r, cap_r) in reported.items():
        # Paper's tabulated d_eff is the closed form n/(1+(n-1)rho).
        deff_c = d_eff_closed_form(n, rho)
        compare(f"d_eff @ rho={rho}", deff_c, deff_r)
        cap_c = simple_lower_bound(eps, deff_c)
        # Paper rounds capacity to nearest power of 10 ("~10^k"); compare exponents.
        exp_c = math.log10(cap_c)
        exp_r = math.log10(cap_r)
        compare(
            f"capacity exponent log10 @ rho={rho}",
            exp_c,
            exp_r,
            rel_tol=0.0,
            abs_tol=0.5,
            note="paper writes ~10^k (rounded power)",
        )

    # --- Compare the two effective-dimensionality measures (tabulated vs alternative) ---
    print(
        "\n  Effective-dimensionality measures "
        "[tabulated trace/lambda_max vs alternative participation ratio]:"
    )
    for rho in [0.1, 0.3, 0.7]:
        pr = d_eff_participation_ratio(n, rho)
        cf = d_eff_closed_form(n, rho)
        print(
            f"      rho={rho}: trace/lambda_max(tabulated)={cf:.4f}  "
            f"participation_ratio={pr:.4f}"
        )


# ---------------------------------------------------------------------------
# Appendix A1 — Key numerical values
# ---------------------------------------------------------------------------


def appendix_a1():
    print("\n--- Appendix A1: Key Numerical Values ---")
    compare("V_8(1)", unit_ball_volume(8), 4.059)
    compare("E8 packing density pi^4/384", E8_DENSITY, 0.253670, abs_tol=1e-5)
    compare("capacity >= eps=.05", simple_lower_bound(0.05), 2.56e10)
    compare("capacity >= eps=.10", simple_lower_bound(0.10), 1.00e8)
    compare("capacity >= eps=.20", simple_lower_bound(0.20), 3.91e5)
    compare(
        "white space 100 brands %",
        (1 - 100 * 0.10**8) * 100,
        99.9999,
        rel_tol=1e-6,
        abs_tol=1e-3,
    )
    compare(
        "white space 10,000 brands %",
        (1 - 10_000 * 0.10**8) * 100,
        99.9900,
        rel_tol=1e-6,
        abs_tol=1e-3,
    )
    compare("d_eff @ rho=.3", d_eff(8, 0.3), 2.58)
    # In-text E8 estimate and corner / mean-radius facts
    compare("N_E8 @ eps=.10", e8_capacity_estimate(0.10), 6.49e9)
    compare("corner effect V_8(1)/2^8", unit_ball_volume(8) / 2**8, 0.016, rel_tol=0.05)
    compare(
        "mean radius sqrt(8/10) uniform 8-ball",
        math.sqrt(8.0 / 10.0),
        0.89,
        abs_tol=5e-3,
    )


# ---------------------------------------------------------------------------
# Appendix B1 — Dimensional capacity lower bounds (1/eps)^n at eps=.10
# ---------------------------------------------------------------------------


def appendix_b1():
    print(
        "\n--- Appendix B1: Dimensional Capacity Lower Bounds (1/eps)^n at eps=.10 ---"
    )
    eps = 0.10
    reported = {
        1: 10,
        2: 100,
        3: 1_000,
        4: 10_000,
        6: 1e6,
        8: 1e8,
        12: 1e12,
        16: 1e16,
        24: 1e24,
    }
    for n, rep in reported.items():
        compare(f"capacity (1/eps)^{n}", simple_lower_bound(eps, n), float(rep))


# ---------------------------------------------------------------------------
# Figure 1 — E8 kissing-shell decomposition
# ---------------------------------------------------------------------------


def figure1_kissing_decomposition():
    print("\n--- Figure 1: E8 Kissing-Shell Decomposition (240 = 112 + 128) ---")
    specialists, generalists = enumerate_e8_minimal_vectors()
    n_spec = len(specialists)
    n_gen = len(generalists)
    n_total = n_spec + n_gen

    # Uniqueness sanity: no duplicates, no overlap between shells.
    assert len(set(specialists)) == n_spec, "duplicate specialist vectors"
    assert len(set(generalists)) == n_gen, "duplicate generalist vectors"
    assert set(specialists).isdisjoint(set(generalists)), "shells overlap"

    compare("specialist count C(8,2)*2^2", float(n_spec), 112.0, abs_tol=0.0)
    compare("generalist count 2^8/2", float(n_gen), 128.0, abs_tol=0.0)
    compare("total kissing number", float(n_total), 240.0, abs_tol=0.0)
    compare(
        "specialist fraction", n_spec / n_total, 0.47, abs_tol=5e-3, note="paper: ~.47"
    )
    compare(
        "generalist fraction", n_gen / n_total, 0.53, abs_tol=5e-3, note="paper: ~.53"
    )
    print(
        f"      E8 enumeration: {n_spec} + {n_gen} = {n_total} "
        f"(exact: {'YES' if n_total == 240 else 'NO'})"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("R4 Sphere-Packing Capacity Bounds — Companion Computation Script")
    print("Zharnikov (2026g) — DOI: 10.5281/zenodo.18945522")
    print(f"Random seed: {SEED} (no stochastic computations; E8 enumeration is exact)")
    print("=" * 78)

    table2_unit_ball_volume()
    table4_capacity_bounds()
    table6_white_space()
    table7_saturation()
    table8_effective_dimensionality()
    appendix_a1()
    appendix_b1()
    figure1_kissing_decomposition()

    # ---- summary ----
    matches = sum(1 for *_, s, _ in _results if s == "MATCH")
    mism = [r for r in _results if r[3] == "MISMATCH"]
    info = sum(1 for *_, s, _ in _results if s == "INFO")
    print("\n" + "=" * 78)
    print(
        f"SUMMARY: {matches} MATCH, {len(mism)} MISMATCH, {info} INFO "
        f"(of {len(_results)} comparisons)"
    )
    if mism:
        print("\nMISMATCHES (computed vs paper-reported):")
        for label, comp, rep, _s, note in mism:
            print(
                f"  - {label}: computed={_fmt(comp)} paper={_fmt(rep)}"
                + (f" ({note})" if note else "")
            )
    else:
        print("All paper-reported VALUES reproduced within tolerance.")

    print(
        "\nNOTE (effective-dimensionality measure): Proposition 5 defines d_eff as "
        "trace/lambda_max\n  = n/(1+(n-1)rho) for the equicorrelation matrix, the "
        "measure all Table-8 values use.\n  The participation ratio (sum lam)^2/sum(lam^2) "
        "is a DIFFERENT measure that yields\n  larger values (e.g. n=8, rho=.1: "
        "trace/lambda_max=4.71 vs participation ratio=7.48);\n  it is computed alongside "
        "here for transparency. The paper's proof states the\n  trace/lambda_max measure "
        "explicitly and notes the participation ratio as the\n  alternative — both are "
        "reproduced by this script."
    )
    print("=" * 78)


if __name__ == "__main__":
    main()
