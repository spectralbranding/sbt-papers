#!/usr/bin/env python3
"""Companion computation script for "The Correspondence Principle of Brand Management"
(SBT paper 2026au).

Computes the expected managerial DECISION-LOSS surface of score-based management
relative to cloud-based management as a function of the four regime-departure
parameters, and verifies the two numerical claims of the paper (finding F1 in
SPINE.yaml):

  1. The loss gap is monotone non-decreasing in each of the four regime-departure
     parameters: perceptual dispersion/multimodality (sigma), temporal velocity (v),
     AI-observer share (alpha), and exogenous-signal share (epsilon).
  2. The loss gap approaches zero at the classical corner (all four parameters small,
     a tight unimodal cloud aligned with the incumbent score axis), numerically
     instantiating the correspondence theorem's reduction limit.

MODEL (decision-theoretic, faithful to the Blackwell garbling argument).
A brand is the observer-completed measure mu on the perception manifold S^{d-1}
(the d = 8 SBT dimensions; the unit-sphere/directional model is the von Mises-Fisher
mixture asked for in the spine). The managerial decision is a quadratic-tracking
problem: choose, per observer, an action that tracks that observer's perception
ideal point; payoff is negative squared (chordal) tracking error. The CLOUD
experiment observes the full perception vector theta and can act per observer, so
its residual loss is zero. The SCORE experiment observes only the scalar incumbent
brand-health index s = <u, theta> (a one-dimensional projection-and-aggregation,
T_k); the best action it supports is the linear minimum-mean-squared-error estimate
E_hat[theta | s], and its residual loss is the unexplained (off-axis) variance. The
reported GAP = score_loss - cloud_loss = score_loss is exactly the Blackwell
dominance gap for this decision problem; it is >= 0 for every experiment by
Blackwell-Sherman-Stein, and this script measures how it grows away from the
classical corner.

Each regime-departure parameter injects off-incumbent-axis perceptual variance:
  sigma   -> concentration spread (1/kappa) + a second human mode separated off-axis
             (dispersion + multimodality).
  alpha   -> a von Mises-Fisher AI-observer component whose mean direction is
             dimension-collapsed onto the Semiotic/Narrative sub-basis (R15), i.e.
             off the incumbent axis.
  epsilon -> an exogenous (near-uniform-on-sphere) component the firm signal does not
             control, hence uncorrelated with the incumbent score.
  v       -> temporal drift: the cloud is rotated by an angle proportional to v in a
             random off-axis direction between measurement and action, adding off-axis
             variance the static snapshot/score never saw.

The incumbent score axis u is fixed to the first canonical dimension (Semiotic), the
sub-basis the single-index trackers privilege. ROBUSTNESS sweeps additionally report:
  - payoff form: quadratic / linear / threshold (the loss-gap sign and monotonicity
    are payoff-form-robust, since Blackwell dominance holds for all bounded losses);
  - dimension count d in {2, 8} (the 2-D case is the appendix toy garbling example);
  - the BEST POSSIBLE scalar index (top principal eigenvector of the realized cloud
    covariance), not just the incumbent's fixed axis -- to pre-empt "your score is a
    straw man": even the best scalar leaves a positive gap once the cloud has rank > 1
    off-axis structure.

REPRODUCIBILITY (PAQS 37a-37e). Deterministic given the fixed seed below. No network,
no credentials. Monte Carlo with N = 20000 observers per parameter combination (well
above the >= 5000 floor); reported with Monte Carlo standard errors.

RUN:
    cd [internal path removed]
    uv run python [internal path removed]

CALIBRATION ANCHOR (observation O1 in SPINE.yaml). The AI-observer dispersion and the
collapsed AI mean direction are set to the scale of the human-vs-AI cohort perception
divergence reported in the R15 AI-search-metamerism corpus
(HuggingFace: zharnikov-2026-hf-r15-ai-search-metamerism), so the surface is anchored
to a real dataset rather than purely synthetic draws. The default AI_COLLAPSE_KAPPA and
AI_MEAN_OFFAXIS_FRAC below encode that scale; see README.md.
"""

import numpy as np

SEED = 20260619  # fixed; do not change without re-reporting all numbers
N_OBS = 20000  # observers (Monte Carlo draws) per parameter combination
D_DEFAULT = 8  # the 8 SBT dimensions

# Calibration constants anchored to R15 AI-search-metamerism cohort divergence
AI_COLLAPSE_KAPPA = (
    18.0  # AI cohort is tightly concentrated (collapsed onto a sub-basis)
)
AI_MEAN_OFFAXIS_FRAC = (
    0.85  # fraction of the AI mean direction lying off the incumbent axis
)


def _normalize(x):
    return x / np.linalg.norm(x, axis=-1, keepdims=True)


def sample_vmf(mu, kappa, n, rng):
    """Sample n points from a von Mises-Fisher distribution on S^{d-1}.

    Wood (1994) rejection algorithm for the tangent component + uniform on the
    orthogonal subsphere. mu must be a unit vector of length d.
    """
    mu = np.asarray(mu, dtype=float)
    d = mu.shape[0]
    if kappa < 1e-8:  # uniform on the sphere (mu irrelevant)
        x = rng.standard_normal((n, d))
        return _normalize(x)
    mu = _normalize(mu)
    # sample the component w = <mu, x> via Wood's algorithm
    b = (-2.0 * kappa + np.sqrt(4.0 * kappa**2 + (d - 1) ** 2)) / (d - 1)
    x0 = (1.0 - b) / (1.0 + b)
    c = kappa * x0 + (d - 1) * np.log(1.0 - x0**2)
    w = np.empty(n)
    for i in range(n):
        while True:
            z = rng.beta((d - 1) / 2.0, (d - 1) / 2.0)
            wt = (1.0 - (1.0 + b) * z) / (1.0 - (1.0 - b) * z)
            u = rng.uniform()
            if kappa * wt + (d - 1) * np.log(1.0 - x0 * wt) - c >= np.log(u):
                w[i] = wt
                break
    # sample directions in the tangent subspace orthogonal to mu
    v = rng.standard_normal((n, d))
    v = v - (v @ mu)[:, None] * mu[None, :]
    v = _normalize(v)
    x = w[:, None] * mu[None, :] + np.sqrt(np.clip(1.0 - w**2, 0.0, None))[:, None] * v
    return _normalize(x)


def build_cloud(d, sigma, v, alpha, epsilon, rng, n=N_OBS):
    """Sample the observer-completed perception cloud on S^{d-1} for a regime point.

    Returns an (n, d) array of unit perception vectors.
    """
    u = np.zeros(d)
    u[0] = 1.0  # incumbent score axis = first (Semiotic) dimension

    # Human primary mode: tight at the classical corner (gap -> ~0), spread rises with sigma.
    kappa_primary = 300.0 / (1.0 + 14.0 * sigma)
    # Human secondary mode (multimodality): appears with sigma, separated off-axis.
    offaxis = np.zeros(d)
    offaxis[1] = 1.0  # second (Narrative) dimension, off the score axis
    mode2_dir = _normalize(np.cos(0.9) * u + np.sin(0.9) * offaxis)
    w2 = 0.45 * sigma  # weight of the second human mode grows with sigma

    # AI cohort: collapsed onto a sub-basis, mean tilted off-axis (dimension collapse).
    ai_dir = _normalize(
        (1.0 - AI_MEAN_OFFAXIS_FRAC) * u + AI_MEAN_OFFAXIS_FRAC * offaxis
    )

    # Mixture weights (renormalized): human primary, human secondary, AI, exogenous.
    w_ai = alpha
    w_exo = epsilon
    w_human = max(1.0 - w_ai - w_exo, 1e-6)
    w_h1 = w_human * (1.0 - w2)
    w_h2 = w_human * w2
    weights = np.array([w_h1, w_h2, w_ai, w_exo])
    weights = weights / weights.sum()

    counts = rng.multinomial(n, weights)
    parts = []
    parts.append(sample_vmf(u, kappa_primary, counts[0], rng))
    if counts[1] > 0:
        parts.append(sample_vmf(mode2_dir, kappa_primary, counts[1], rng))
    if counts[2] > 0:
        parts.append(sample_vmf(ai_dir, AI_COLLAPSE_KAPPA, counts[2], rng))
    if counts[3] > 0:
        parts.append(
            sample_vmf(np.zeros(d), 0.0, counts[3], rng)
        )  # uniform / exogenous
    theta = np.vstack(parts)

    # Temporal drift between measurement and action: perception moves by an observer-
    # specific amount (proportional to velocity v) in off-axis directions the static
    # snapshot/score never saw -- this INJECTS off-axis variance (it is not a coherent
    # shift, which would add none). Dims 2-3 = Ideological/Experiential.
    if v > 0 and d >= 3:
        kdrift = min(2, d - 1)
        noise = np.zeros((theta.shape[0], d))
        noise[:, 2 : 2 + kdrift] = (
            1.3 * v * rng.standard_normal((theta.shape[0], kdrift))
        )
        theta = _normalize(theta + noise)
    rng.shuffle(theta)
    return theta, u


def gap_quadratic(theta, score_axis):
    """Blackwell dominance gap for the quadratic-tracking decision.

    cloud_loss = 0 (acts per observer on the full vector); score_loss = residual
    variance unexplained by the best LINEAR action from the scalar s = <axis, theta>.
    Returns (gap_mean, gap_se).
    """
    s = theta @ score_axis
    mu_t = theta.mean(axis=0)
    mu_s = s.mean()
    cov_ts = ((theta - mu_t) * (s - mu_s)[:, None]).mean(
        axis=0
    )  # Cov(theta, s), shape (d,)
    var_s = ((s - mu_s) ** 2).mean()
    pred = mu_t[None, :] + (cov_ts / max(var_s, 1e-12))[None, :] * (s - mu_s)[:, None]
    resid = ((theta - pred) ** 2).sum(axis=1)  # per-observer squared error
    return resid.mean(), resid.std(ddof=1) / np.sqrt(len(resid))


def gap_linear(theta, score_axis):
    """Linear payoff g(a, theta) = <a, theta>; loss gap = shortfall in attainable
    aligned value between acting on the full vector vs on the scalar's linear decode."""
    s = theta @ score_axis
    mu_t = theta.mean(axis=0)
    mu_s = s.mean()
    cov_ts = ((theta - mu_t) * (s - mu_s)[:, None]).mean(axis=0)
    var_s = ((s - mu_s) ** 2).mean()
    pred = mu_t[None, :] + (cov_ts / max(var_s, 1e-12))[None, :] * (s - mu_s)[:, None]
    # full action a_full = theta_i (perfect alignment); score action a_score = pred_i
    val_full = (theta * theta).sum(axis=1)
    val_score = (theta * pred).sum(axis=1)
    g = val_full - val_score
    return g.mean(), g.std(ddof=1) / np.sqrt(len(g))


def gap_threshold(theta, score_axis, tau=0.5):
    """Threshold payoff: reward 1 if the action's primary off-axis component is within
    tau of the observer's, else 0; loss gap = fraction the score's decode misclassifies.
    """
    s = theta @ score_axis
    mu_t = theta.mean(axis=0)
    mu_s = s.mean()
    cov_ts = ((theta - mu_t) * (s - mu_s)[:, None]).mean(axis=0)
    var_s = ((s - mu_s) ** 2).mean()
    pred = mu_t[None, :] + (cov_ts / max(var_s, 1e-12))[None, :] * (s - mu_s)[:, None]
    err = np.abs(theta[:, 1] - pred[:, 1])  # off-axis (Narrative) miss
    miss = (err > tau).astype(float)
    return miss.mean(), miss.std(ddof=1) / np.sqrt(len(miss))


def best_scalar_axis(theta):
    """The best possible single index = top principal eigenvector of the cloud cov."""
    c = np.cov(theta.T)
    w, vecs = np.linalg.eigh(c)
    return vecs[:, -1]


CLASSICAL = dict(sigma=0.0, v=0.0, alpha=0.0, epsilon=0.0)


def sweep_one(param, grid, d=D_DEFAULT, gap_fn=gap_quadratic, best_scalar=False):
    rng = np.random.default_rng(SEED)
    rows = []
    for val in grid:
        kw = dict(CLASSICAL)
        kw[param] = val
        theta, u = build_cloud(d, rng=rng, n=N_OBS, **kw)
        axis = best_scalar_axis(theta) if best_scalar else u
        g, se = gap_fn(theta, axis)
        rows.append((val, g, se))
    return rows


def main():
    grid = [0.0, 0.1, 0.2, 0.35, 0.5, 0.7, 0.9]
    print(
        f"# Correspondence-principle decision-loss surface  (seed={SEED}, N={N_OBS}/combo, d={D_DEFAULT})"
    )
    print(
        "# GAP = score-based minus cloud-based expected decision loss (Blackwell dominance gap).\n"
    )

    print("## Classical corner (all parameters = 0)")
    rng = np.random.default_rng(SEED)
    theta, u = build_cloud(D_DEFAULT, rng=rng, n=N_OBS, **CLASSICAL)
    g0, se0 = gap_quadratic(theta, u)
    print(
        f"  quadratic gap = {g0:.4f} (SE {se0:.4f})  -> expected ~0 (reduction limit)\n"
    )

    print(
        "## Monotonicity in each regime-departure parameter (quadratic payoff, incumbent axis)"
    )
    for p in ["sigma", "v", "alpha", "epsilon"]:
        rows = sweep_one(p, grid)
        cells = "  ".join(f"{v:.2f}:{g:.3f}" for v, g, _ in rows)
        mono = all(
            rows[i + 1][1] >= rows[i][1] - 3 * rows[i + 1][2]
            for i in range(len(rows) - 1)
        )
        print(f"  {p:8s} {cells}   monotone_up={mono}")
    print()

    print("## Robustness: payoff form (sweep sigma)")
    for name, fn in [
        ("quadratic", gap_quadratic),
        ("linear", gap_linear),
        ("threshold", gap_threshold),
    ]:
        rows = sweep_one("sigma", grid, gap_fn=fn)
        cells = "  ".join(f"{v:.2f}:{g:.3f}" for v, g, _ in rows)
        print(f"  {name:9s} {cells}")
    print()

    print("## Robustness: dimension count d in {2, 8} (sweep sigma, quadratic)")
    for d in (2, 8):
        rows = sweep_one("sigma", grid, d=d)
        cells = "  ".join(f"{v:.2f}:{g:.3f}" for v, g, _ in rows)
        print(f"  d={d}  {cells}")
    print()

    print(
        "## Robustness: best-possible scalar vs incumbent fixed axis (sweep sigma, quadratic)"
    )
    for label, bs in [("incumbent-axis", False), ("best-scalar", True)]:
        rows = sweep_one("sigma", grid, best_scalar=bs)
        cells = "  ".join(f"{v:.2f}:{g:.3f}" for v, g, _ in rows)
        print(f"  {label:14s} {cells}")
    print(
        "\n# Even the best single index leaves a positive gap once the cloud has off-axis (rank>1) structure."
    )


if __name__ == "__main__":
    main()
