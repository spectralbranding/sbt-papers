"""Fixed-seed power simulation for the pre-registered monotone-link test (2026bf).

Simulates the primary analysis of the Perception Sets the Matrix design:
Kendall tau_b between spectral match m(c,b) and stated choice propensity
p(c,b) over cohort x brand cells, with a within-cohort brand-label
permutation null (one-sided, direction pre-registered positive), per
operator and pooled (median tau_b across operators, shared permutations
because the match values are common to all operators).

Data-generating process: match values are drawn uniformly per cell (the
space-filling design spans the match range); propensities are generated
through a Gaussian copula whose correlation is set from the target Kendall
tau via rho = sin(pi * tau / 2), with independent operator noise. Cell
counts follow the design: Study 1 = 10 cohorts x 6 brands = 60 cells;
Study 2 = 10 cohorts x 5 brands = 50 cells.

Run:
    uv run python code/power_simulation.py

Fixed seed 20260712. Runtime is a few minutes on a laptop; results print
as a table and are the source of the sample-size statements in the paper's
Method section.
"""

import numpy as np

SEED = 20260712
N_SIMS = 1000
N_PERM = 1000
ALPHA = 0.05
N_COHORTS = 10


def tau_from_pairs(sm, sp):
    """Kendall tau_a over precomputed pairwise sign arrays (no ties by
    construction: continuous draws). sm: (n_pairs,), sp: (..., n_pairs)."""
    return (sm * sp).mean(axis=-1)


def simulate(tau_target, n_brands, n_operators, rng):
    """One simulated dataset -> (reject, tau_obs_pooled).

    Permutation null: brand labels shuffled within cohort; the SAME
    permutation is applied to every operator's propensity table before
    re-pooling, because the match table is shared across operators.
    """
    rho = np.sin(np.pi * tau_target / 2)
    n_cells = N_COHORTS * n_brands

    m = rng.uniform(0, 1, size=n_cells)
    z_m = (np.argsort(np.argsort(m)) + 0.5) / n_cells  # rank-uniform
    z_m = np.sqrt(2) * erfinv_vec(2 * z_m - 1)

    p_ops = rho * z_m + np.sqrt(1 - rho**2) * rng.standard_normal(
        (n_operators, n_cells)
    )

    iu, ju = np.triu_indices(n_cells, k=1)
    sm = np.sign(m[iu] - m[ju])
    tau_obs = np.median(tau_from_pairs(sm, np.sign(p_ops[:, iu] - p_ops[:, ju])))

    # Within-cohort permutations of brand labels, shared across operators.
    cells = np.arange(n_cells).reshape(N_COHORTS, n_brands)
    taus_null = np.empty(N_PERM)
    for k in range(N_PERM):
        perm = np.empty(n_cells, dtype=int)
        for c in range(N_COHORTS):
            perm[cells[c]] = rng.permutation(cells[c])
        p_perm = p_ops[:, perm]
        taus_null[k] = np.median(
            tau_from_pairs(sm, np.sign(p_perm[:, iu] - p_perm[:, ju]))
        )

    p_value = (1 + np.sum(taus_null >= tau_obs)) / (1 + N_PERM)
    return p_value < ALPHA, tau_obs


def erfinv_vec(x):
    from scipy.special import erfinv

    return erfinv(x)


def main():
    rng = np.random.default_rng(SEED)
    configs = [
        ("Study 1, per operator, tau=.30", 0.30, 6, 1),
        ("Study 1, per operator, tau=.20", 0.20, 6, 1),
        ("Study 1, pooled 4 operators, tau=.20", 0.20, 6, 4),
        ("Study 2, per operator, tau=.30", 0.30, 5, 1),
        ("Study 2, pooled 4 operators, tau=.20", 0.20, 5, 4),
    ]
    print(f"seed={SEED} sims={N_SIMS} perms={N_PERM} alpha={ALPHA}")
    print(f"{'config':45s} {'power':>7s} {'median tau_b':>13s}")
    for name, tau, n_brands, n_ops in configs:
        rejections = 0
        taus = []
        for _ in range(N_SIMS):
            rej, t = simulate(tau, n_brands, n_ops, rng)
            rejections += rej
            taus.append(t)
        print(f"{name:45s} {rejections / N_SIMS:7.3f} {np.median(taus):13.3f}")


if __name__ == "__main__":
    main()
