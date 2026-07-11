"""Bridging illustration: spectral gap of a stationary Dirichlet switching matrix.

Derives and numerically verifies the closed-form spectral gap of the
purchase-level brand-switching matrix implied by a zero-order stationary
Dirichlet market (Goodhardt, Ehrenberg & Chatfield 1984). Under the
zero-order model with brand shares s_j and switching parameter S, the
population conditional next-purchase matrix given a current purchase of
brand i is the Dirichlet-multinomial posterior predictive

    P_ij = (S * s_j + delta_ij) / (S + 1),

so P = (I + S * 1 s^T) / (S + 1). Its spectrum is {1, 1/(S+1)} with the
non-unit eigenvalue of multiplicity n-1, giving spectral gap

    gap = 1 - 1/(S+1) = S/(S+1)

independent of the share vector. The stationary distribution is s itself,
and the diagonal repeat rate (1 + S*s_i)/(1 + S) increases affinely in
share — the double-jeopardy pattern (Ehrenberg, Goodhardt & Barwise 1990).

All parameter values are author-proposed illustrative calibrations (same
convention as the paper's Monte Carlo design); no panel data are used.

Run: uv run --with numpy python3 switching_matrix_gap.py
Seed: 2026 (used only for the random-share robustness replicate).
"""

import numpy as np

SEED = 2026


def switching_matrix(shares: np.ndarray, s_param: float) -> np.ndarray:
    """Zero-order Dirichlet-multinomial switching matrix P_ij."""
    n = shares.shape[0]
    return (s_param * np.tile(shares, (n, 1)) + np.eye(n)) / (s_param + 1.0)


def analyze(shares: np.ndarray, s_param: float) -> dict:
    p = switching_matrix(shares, s_param)
    assert np.allclose(p.sum(axis=1), 1.0), "rows must sum to 1"
    # stationary distribution: left eigenvector of eigenvalue 1
    assert np.allclose(shares @ p, shares), "stationary distribution must equal shares"
    eigvals = np.sort(np.abs(np.linalg.eigvals(p)))[::-1]
    gap_numeric = 1.0 - eigvals[1]
    gap_analytic = s_param / (s_param + 1.0)
    assert np.isclose(gap_numeric, gap_analytic), "closed form must match spectrum"
    # half-life of a share perturbation, in purchase occasions:
    # perturbation decays by factor 1/(S+1) per occasion
    halflife = np.log(2.0) / np.log(s_param + 1.0)
    repeat = np.diag(p)
    dj_increasing = bool(np.all(np.diff(repeat[np.argsort(shares)]) >= 0))
    return {
        "S": s_param,
        "second_eigenvalue": eigvals[1],
        "gap": gap_numeric,
        "halflife_occasions": halflife,
        "repeat_min": repeat.min(),
        "repeat_max": repeat.max(),
        "double_jeopardy_monotone": dj_increasing,
    }


def main() -> None:
    # Author-proposed illustrative category: 11 national brands + all-other,
    # shares descending in a typical CPG long-tail pattern.
    shares = np.array(
        [0.16, 0.13, 0.11, 0.10, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.15]
    )
    assert np.isclose(shares.sum(), 1.0)

    print("S      lambda2   gap      halflife(occasions)  repeat range   DJ monotone")
    for s_param in (0.5, 1.0, 2.0, 5.0):
        r = analyze(shares, s_param)
        print(
            f"{r['S']:<6.1f} {r['second_eigenvalue']:.4f}   {r['gap']:.4f}   "
            f"{r['halflife_occasions']:>8.2f}             "
            f"{r['repeat_min']:.3f}-{r['repeat_max']:.3f}    "
            f"{r['double_jeopardy_monotone']}"
        )

    # Robustness replicate: random shares, same closed form must hold.
    rng = np.random.default_rng(SEED)
    random_shares = rng.dirichlet(np.ones(12))
    r = analyze(random_shares, 1.0)
    print(
        f"\nrandom-share replicate (seed {SEED}, S=1.0): "
        f"gap={r['gap']:.4f} (analytic .5000), "
        f"DJ monotone={r['double_jeopardy_monotone']}"
    )


if __name__ == "__main__":
    main()
