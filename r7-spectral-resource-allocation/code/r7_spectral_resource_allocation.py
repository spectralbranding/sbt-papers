"""
Companion Computation Script for R7: Spectral Resource Allocation
=================================================================
Paper: Spectral Resource Allocation: Demand-Driven Investment in
       Multi-Dimensional Brand Space
Author: Zharnikov, D. (2026k). https://doi.org/10.5281/zenodo.19009268

Reproduces all numerical values reported in the paper (Table 7,
Appendix A.2, Theorem 1 optima, Theorem 5 interaction adjustments)
and, when matplotlib is available and ``--write-figures`` is passed,
generates three static figures referenced by the paper:

    figures/r7_alignment_gap_simplex.png
        Theorem 2 illustration: a 2-D barycentric projection of the
        eight-dimensional probability simplex showing each brand's
        founder weight w(f), cohort weight w(c), the geodesic between
        them, and the resulting alignment gap A(f,c) annotated.

    figures/r7_founder_vs_cohort_weights.png
        Founder vs cohort weight comparison: grouped bar chart for the
        five canonical brands across all eight SBT dimensions.
        Visualizes Tables 5-6 and the inputs to Table 7.

    figures/r7_theorem5_interaction_adjustment.png
        Theorem 5 interaction adjustment: side-by-side bar chart for
        Hermes (heritage premium) and Tesla (luxury paradox) showing
        s*(linear) from Theorem 1, s*(interaction) from Theorem 5,
        and the per-dimension delta.

Run command (numerics only):
    uv run python r7_spectral_resource_allocation.py

Run command (numerics + figures):
    uv run python r7_spectral_resource_allocation.py --write-figures

The script also verifies the CORRECTED Theorem 2 (v2.0.0). The
originally published bound A(f,c) >= H(f,c)^2 / (2 * lambda * alpha_bar)
is false: a uniform founder gives A(f,c) = 0 against every cohort on the
simplex while the right-hand side stays positive. The corrected statement
carries the concentration hypothesis ||w(c)||_2 <= ||w(f)||_2 and reads

    A(f,c) >= ||w(f) - w(c)||_2^2 / (2 * lambda * alpha_bar)     (exact)
            >= H(f,c)^4 / (4 * lambda * alpha_bar)               (Hellinger form)

`--verify-theorem2` runs a fixed-seed Monte Carlo that (a) reproduces the
counterexample to the published bound, (b) finds no violation of the
corrected bound over 200,000 Dirichlet pairs satisfying the hypothesis,
and (c) reports the worst observed slack.

Fixed seed: SEED = 42 (used for any stochastic elements; all
deterministic computations are seed-independent).

Dependencies: Python 3.12, numpy; matplotlib only required for
figures (``uv add --dev matplotlib``).
"""

import argparse
import os
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

DIM_ABBREV = ["Sem", "Nar", "Ide", "Exp", "Soc", "Eco", "Cul", "Tem"]

EMISSION_PROFILES = {
    "Hermes": np.array([9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]),
    "IKEA": np.array([8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]),
    "Patagonia": np.array([6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]),
    "Erewhon": np.array([7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5]),
    "Tesla": np.array([7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]),
}

# ---------------------------------------------------------------------------
# Hypothetical founder profiles (paper Table 5; simplex-normalised)
# ---------------------------------------------------------------------------
FOUNDER_PROFILES_RAW = {
    "Hermes": np.array([0.20, 0.15, 0.10, 0.20, 0.15, 0.02, 0.10, 0.08]),
    "IKEA": np.array([0.05, 0.05, 0.05, 0.10, 0.05, 0.50, 0.10, 0.10]),
    "Patagonia": np.array([0.05, 0.15, 0.30, 0.15, 0.10, 0.05, 0.10, 0.10]),
    "Erewhon": np.array([0.10, 0.05, 0.05, 0.30, 0.20, 0.05, 0.15, 0.10]),
    "Tesla": np.array([0.10, 0.20, 0.05, 0.30, 0.15, 0.05, 0.05, 0.10]),
}

# ---------------------------------------------------------------------------
# Hypothetical target cohort profiles (paper Table 6; simplex-normalised)
# ---------------------------------------------------------------------------
COHORT_PROFILES_RAW = {
    "Hermes": np.array([0.18, 0.15, 0.08, 0.15, 0.18, 0.03, 0.13, 0.10]),
    "IKEA": np.array([0.10, 0.08, 0.05, 0.15, 0.07, 0.35, 0.10, 0.10]),
    "Patagonia": np.array([0.08, 0.12, 0.20, 0.15, 0.12, 0.08, 0.10, 0.15]),
    "Erewhon": np.array([0.10, 0.08, 0.05, 0.25, 0.20, 0.07, 0.15, 0.10]),
    "Tesla": np.array([0.12, 0.15, 0.05, 0.20, 0.18, 0.12, 0.08, 0.10]),
}

BRAND_COLORS = {
    "Hermes": "#1f4e79",
    "IKEA": "#2e7d32",
    "Patagonia": "#6a1b9a",
    "Erewhon": "#ef6c00",
    "Tesla": "#b71c1c",
}


# ---------------------------------------------------------------------------
# Figure text helpers
#
# Figures are part of the paper, so they follow the paper's conventions: math is
# set as math (matplotlib mathtext renders the LaTeX subset the paper uses, with
# no external LaTeX install), and a magnitude that cannot exceed one is written
# without a leading zero, as PAQS requires of every reported value.
# ---------------------------------------------------------------------------
DISPLAY_NAME = {"Hermes": "Herm\u00e8s"}


def display_name(brand: str) -> str:
    """The brand as it is written in the paper; dict keys stay ASCII."""
    return DISPLAY_NAME.get(brand, brand)


def nz(value: float, places: int = 4, signed: bool = False) -> str:
    """Format a magnitude bounded by one with no leading zero (PAQS)."""
    text = f"{abs(value):.{places}f}"
    if text.startswith("0."):
        text = text[1:]
    if signed:
        return ("+" if value > 0 else "\u2212" if value < 0 else "") + text
    return ("\u2212" if value < 0 else "") + text


def strip_leading_zero_ticks(ax, axis: str = "y") -> None:
    """Tick labels for a quantity bounded by one, written the paper's way."""
    from matplotlib.ticker import FuncFormatter

    fmt = FuncFormatter(lambda v, _pos: nz(v, 3))
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


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


def optimal_value(wc: np.ndarray, lam: float = 1.0, alpha_bar: float = 1.0) -> float:
    """V*(c) = H(c) / (lambda * alpha_bar) under uniform quadratic costs.

    H(c) = sum_i w_i(c)^2 is the Herfindahl index of the cohort profile.
    """
    return float(np.dot(wc, wc)) / (lam * alpha_bar)


def theorem2_bounds(
    wf: np.ndarray, wc: np.ndarray, lam: float = 1.0, alpha_bar: float = 1.0
) -> dict:
    """Both sides of Theorem 2, published (v1.0.0) and corrected (v2.0.0).

    The corrected theorem holds under the concentration hypothesis
    ||w(c)||_2 <= ||w(f)||_2.  Its first form is exact algebra:

        A(f,c) = (1/2)||w(f)-w(c)||^2 + (1/2)(||w(f)||^2 - ||w(c)||^2),

    so the hypothesis makes the second term non-negative and

        A(f,c) >= ||w(f)-w(c)||^2 / (2 * lambda * alpha_bar).

    The Hellinger form follows from ||d||_2^2 >= ||d||_1^2 / 8 (Cauchy-Schwarz
    on eight coordinates) and ||p-q||_1 >= 2 H(p,q)^2 (total variation), giving

        A(f,c) >= H(f,c)^4 / (4 * lambda * alpha_bar).
    """
    norm_sq_f = float(np.dot(wf, wf))
    norm_sq_c = float(np.dot(wc, wc))
    gap = (norm_sq_f - float(np.dot(wf, wc))) / (lam * alpha_bar)
    h = hellinger(wf, wc)
    diff_sq = float(np.sum((wf - wc) ** 2))
    return {
        "hypothesis_holds": norm_sq_c <= norm_sq_f,
        "norm_sq_f": norm_sq_f,
        "norm_sq_c": norm_sq_c,
        "gap": gap,
        "hellinger": h,
        "fisher_rao": fisher_rao(wf, wc),
        "published_rhs": h**2 / (2.0 * lam * alpha_bar),
        "euclidean_rhs": diff_sq / (2.0 * lam * alpha_bar),
        "hellinger_rhs": h**4 / (4.0 * lam * alpha_bar),
        "gap_ratio": gap / optimal_value(wc, lam, alpha_bar),
    }


def verify_theorem2(n_draws: int = 200_000, seed: int = SEED) -> dict:
    """Monte Carlo check of the published and the corrected Theorem 2.

    Returns counts of violations. The published bound is expected to fail
    massively; the corrected bound is expected to fail never.
    """
    rng = np.random.default_rng(seed)
    n = 8
    uniform = np.full(n, 1.0 / n)

    # (a) The counterexample family: uniform founder, cohorts at every epsilon.
    counterexample = []
    for eps in (1e-6, 1e-3, 1e-2, 5e-2, 0.25):
        wc = np.full(n, eps / (n - 1))
        wc[0] = 1.0 - eps
        b = theorem2_bounds(uniform, wc)
        counterexample.append((eps, b["gap"], b["published_rhs"]))

    # (b) The corrected bound over random pairs satisfying the hypothesis.
    tested = 0
    viol_corrected = 0
    viol_published = 0
    worst_ratio = np.inf
    for _ in range(n_draws):
        wf = rng.dirichlet(np.full(n, 10.0 ** rng.uniform(-2.0, 1.5)))
        wc = rng.dirichlet(np.full(n, 10.0 ** rng.uniform(-2.0, 1.5)))
        b = theorem2_bounds(wf, wc)
        if b["published_rhs"] > 0 and b["gap"] < b["published_rhs"] - 1e-12:
            viol_published += 1
        if not b["hypothesis_holds"] or b["hellinger"] < 1e-3:
            continue
        tested += 1
        if b["gap"] < b["euclidean_rhs"] - 1e-12:
            viol_corrected += 1
        if b["gap"] < b["hellinger_rhs"] - 1e-12:
            viol_corrected += 1
        worst_ratio = min(worst_ratio, b["gap"] / b["hellinger_rhs"])

    return {
        "counterexample": counterexample,
        "draws": n_draws,
        "tested_under_hypothesis": tested,
        "violations_published": viol_published,
        "violations_corrected": viol_corrected,
        "worst_ratio_hellinger_form": float(worst_ratio),
    }


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
# Figure helpers
# ---------------------------------------------------------------------------
def _figure_path(out_dir: str, name: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, name)


def write_alignment_gap_simplex(out_dir: str, founders: dict, cohorts: dict) -> str:
    """Theorem 2 illustration on the probability simplex.

    The eight-dimensional simplex Delta^7 cannot be drawn directly, so we
    project each weight vector onto the 2-D plane spanned by the two
    dominant principal axes of the stacked founder + cohort matrix.  This
    preserves the relative geometry of (w(f), w(c)) within each brand
    while making the alignment-gap construct visually legible.
    """
    import matplotlib.pyplot as plt

    brands = list(founders.keys())
    # Stack all weight vectors and centre.
    stacked = np.vstack([founders[b] for b in brands] + [cohorts[b] for b in brands])
    centred = stacked - stacked.mean(axis=0, keepdims=True)
    # PCA via SVD.
    _, _, vt = np.linalg.svd(centred, full_matrices=False)
    basis = vt[:2].copy()  # (2, 8)
    # Pin the SVD sign convention (largest-magnitude loading positive) so the
    # projection orientation is reproducible and the manual label offsets below
    # stay valid across numpy versions.
    for i in range(basis.shape[0]):
        if basis[i][np.argmax(np.abs(basis[i]))] < 0:
            basis[i] = -basis[i]

    def project(w: np.ndarray) -> np.ndarray:
        return basis @ (w - stacked.mean(axis=0))

    # Manual label placement (fixed illustrative data; PCA sign pinned above)
    # keeps each "{brand} (A=...)" annotation clear of the markers and geodesics.
    # Spec: anchor ("f"=founder dot, "c"=cohort square), (dx, dy) offset points,
    # horizontal- and vertical-alignment.
    label_spec = {
        "Hermes": ("f", (0, 13), "center", "bottom"),
        "IKEA": ("f", (-6, 13), "right", "bottom"),
        "Patagonia": ("f", (10, 2), "left", "center"),
        "Tesla": ("c", (10, 2), "left", "center"),
        "Erewhon": ("c", (10, -9), "left", "center"),
    }
    pts = []

    fig, ax = plt.subplots(figsize=(7.6, 5.8))
    for b in brands:
        wf = founders[b]
        wc = cohorts[b]
        pf = project(wf)
        pc = project(wc)
        # Geodesic on the simplex: square-root parametrisation.
        ts = np.linspace(0.0, 1.0, 50)
        sf = np.sqrt(wf)
        sc = np.sqrt(wc)
        # Spherical interpolation between sqrt(wf) and sqrt(wc) on S^7_+.
        cos_theta = np.clip(np.dot(sf, sc), -1.0, 1.0)
        theta = np.arccos(cos_theta)
        if theta < 1e-6:
            geodesic_pts = np.array([wf for _ in ts])
        else:
            geo = np.array(
                [
                    (np.sin((1 - t) * theta) * sf + np.sin(t * theta) * sc)
                    / np.sin(theta)
                    for t in ts
                ]
            )
            geodesic_pts = geo**2  # back to simplex
        proj_geo = np.array([project(p) for p in geodesic_pts])
        color = BRAND_COLORS[b]
        ax.plot(
            proj_geo[:, 0],
            proj_geo[:, 1],
            "-",
            color=color,
            alpha=0.55,
            linewidth=1.4,
        )
        ax.scatter(
            pf[0],
            pf[1],
            s=70,
            facecolor=color,
            edgecolor="white",
            linewidth=1.0,
            marker="o",
            zorder=4,
        )
        ax.scatter(
            pc[0],
            pc[1],
            s=90,
            facecolor="white",
            edgecolor=color,
            linewidth=1.6,
            marker="s",
            zorder=4,
        )
        gap_val = float(np.dot(wf, wf) - np.dot(wf, wc))
        anchor_key, (dx, dy), ha, va = label_spec[b]
        anchor = pf if anchor_key == "f" else pc
        ax.annotate(
            f"{display_name(b)} ($\\mathcal{{A}}$ = {nz(gap_val)})",
            xy=(anchor[0], anchor[1]),
            xytext=(dx, dy),
            textcoords="offset points",
            ha=ha,
            va=va,
            fontsize=8,
            color=color,
            annotation_clip=False,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75),
        )
        pts.append(pf)
        pts.append(pc)
    # Legend proxies.
    from matplotlib.lines import Line2D

    legend_elems = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="#444",
            markersize=8,
            label="Founder $w(f)$",
        ),
        Line2D(
            [0],
            [0],
            marker="s",
            color="w",
            markerfacecolor="white",
            markeredgecolor="#444",
            markersize=9,
            label="Cohort $w(c)$",
        ),
        Line2D([0], [0], color="#444", linewidth=1.4, label="Fisher\u2013Rao geodesic"),
    ]
    ax.legend(handles=legend_elems, loc="upper right", fontsize=8)
    ax.set_xlabel("PC1 of stacked weight vectors")
    ax.set_ylabel("PC2 of stacked weight vectors")
    # Figure title is carried by the paper caption (AMA: no on-image title).
    ax.grid(True, linestyle=":", alpha=0.5)
    # Pad the data limits so edge labels (e.g. IKEA at the right) are not clipped.
    pts = np.array(pts)
    xpad = 0.18 * (pts[:, 0].max() - pts[:, 0].min())
    ypad = 0.18 * (pts[:, 1].max() - pts[:, 1].min())
    ax.set_xlim(pts[:, 0].min() - xpad, pts[:, 0].max() + xpad)
    ax.set_ylim(pts[:, 1].min() - ypad, pts[:, 1].max() + ypad)
    fig.tight_layout()
    path = _figure_path(out_dir, "r7_alignment_gap_simplex.png")
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def write_founder_vs_cohort_weights(out_dir: str, founders: dict, cohorts: dict) -> str:
    """Grouped bar chart: founder vs cohort weight per brand per dimension."""
    import matplotlib.pyplot as plt

    brands = list(founders.keys())
    fig, axes = plt.subplots(
        len(brands), 1, figsize=(7.2, 1.5 * len(brands)), sharex=True
    )
    x = np.arange(8)
    width = 0.38
    for ax, b in zip(axes, brands):
        wf = founders[b]
        wc = cohorts[b]
        ax.bar(
            x - width / 2,
            wf,
            width,
            color=BRAND_COLORS[b],
            alpha=0.55,
            label="Founder $w(f)$",
            edgecolor="white",
        )
        ax.bar(
            x + width / 2,
            wc,
            width,
            color=BRAND_COLORS[b],
            alpha=1.0,
            label="Cohort $w(c)$",
            edgecolor="white",
        )
        gap = float(np.dot(wf, wf) - np.dot(wf, wc))
        ax.set_ylabel(display_name(b), fontsize=9)
        ax.set_ylim(0, max(0.55, max(wf.max(), wc.max()) * 1.15))
        ax.grid(True, axis="y", linestyle=":", alpha=0.5)
        strip_leading_zero_ticks(ax)
        # Top-left placement avoids colliding with the first panel's legend.
        ax.text(
            0.01,
            0.92,
            f"$\\mathcal{{A}}(f,c)$ = {nz(gap)}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=8,
        )
    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels(DIM_ABBREV, fontsize=8)
    axes[0].legend(loc="upper right", fontsize=8, ncols=2)
    # Figure title is carried by the paper caption (AMA: no on-image title).
    fig.tight_layout()
    path = _figure_path(out_dir, "r7_founder_vs_cohort_weights.png")
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def write_theorem5_interaction_adjustment(out_dir: str, cohorts: dict) -> str:
    """Side-by-side bar chart of Theorem 1 vs Theorem 5 allocation."""
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.4), sharey=True)
    cases = [
        (
            "Hermes",
            hermes_interaction_matrix(0.05),
            "Heritage premium\n($w_{\\mathrm{nar,tem}}$ = +.05)",
        ),
        (
            "Tesla",
            tesla_interaction_matrix(-0.03),
            "Luxury paradox\n($w_{\\mathrm{ide,tem}}$ = \u2212.03)",
        ),
    ]
    x = np.arange(8)
    width = 0.38
    for ax, (b, W, title) in zip(axes, cases):
        wc = cohorts[b]
        s1 = theorem1_optimal_allocation(wc)
        s5 = theorem5_optimal_allocation(wc, W)
        delta = s5 - s1
        ax.bar(
            x - width / 2,
            s1,
            width,
            color=BRAND_COLORS[b],
            alpha=0.45,
            label="Theorem 1 (linear)",
            edgecolor="white",
        )
        ax.bar(
            x + width / 2,
            s5,
            width,
            color=BRAND_COLORS[b],
            alpha=1.0,
            label="Theorem 5 (interaction)",
            edgecolor="white",
        )
        # Annotate the two affected dimensions only.
        for i in range(8):
            if abs(delta[i]) > 1e-6:
                ax.annotate(
                    f"{nz(delta[i], signed=True)}",
                    xy=(x[i] + width / 2, s5[i]),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center",
                    fontsize=8,
                )
        ax.set_xticks(x)
        ax.set_xticklabels(DIM_ABBREV, fontsize=8)
        ax.set_title(f"{display_name(b)}: {title}", fontsize=10)
        ax.grid(True, axis="y", linestyle=":", alpha=0.5)
        strip_leading_zero_ticks(ax)
        ax.legend(loc="upper right", fontsize=8)
    axes[0].set_ylabel("Optimal allocation $s^*$")
    # Figure title is carried by the paper caption (AMA: no on-image title);
    # the per-panel titles label the two illustrative cases.
    fig.tight_layout()
    path = _figure_path(out_dir, "r7_theorem5_interaction_adjustment.png")
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Main: run all computations and (optionally) write figures
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-figures",
        action="store_true",
        help="Generate static PNG figures (requires matplotlib).",
    )
    parser.add_argument(
        "--figure-dir",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures"),
        help="Output directory for figures (default: ./figures next to this script).",
    )
    parser.add_argument(
        "--verify-theorem2",
        action="store_true",
        help=(
            "Run the fixed-seed Monte Carlo check of the corrected Theorem 2 "
            "(200,000 Dirichlet pairs; slow, roughly one minute)."
        ),
    )
    args = parser.parse_args()

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
    header = (
        f"{'Brand':<12} {'||w(f)||^2':>12} {'<w(f),w(c)>':>13} "
        f"{'A(f,c)':>10} {'H(f,c)':>10} {'d_FR':>8}"
    )
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
    col_w = 6
    header2 = f"{'Brand':<12}" + "".join(f"{d:>{col_w}}" for d in DIM_ABBREV)
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

    # ------------------------------------------------------------------
    # Theorem 2 (corrected at v2.0.0): the concentration hypothesis, the
    # exact Euclidean bound, the Hellinger form, and the direct gap ratio
    # that replaces the withdrawn Fisher-Rao audit trigger.
    # ------------------------------------------------------------------
    print("\n--- Theorem 2 (corrected): bounds and the direct gap ratio ---\n")
    header = (
        f"  {'Brand':<11}{'||wf||^2':>10}{'||wc||^2':>10}{'hyp':>6}"
        f"{'A(f,c)':>10}{'|d|^2/2':>10}{'H^4/4':>10}{'d_FR':>8}{'A/V*':>8}"
    )
    print(header)
    t2 = {}
    for b in brands:
        v = theorem2_bounds(founders[b], cohorts[b])
        t2[b] = v
        print(
            f"  {b:<11}{v['norm_sq_f']:>10.4f}{v['norm_sq_c']:>10.4f}"
            f"{('yes' if v['hypothesis_holds'] else 'NO'):>6}{v['gap']:>10.4f}"
            f"{v['euclidean_rhs']:>10.5f}{v['hellinger_rhs']:>10.5f}"
            f"{v['fisher_rao']:>8.4f}{v['gap_ratio']:>8.3f}"
        )
    print(
        "\n  All five illustrative pairs satisfy the concentration hypothesis"
        "\n  ||w(c)||_2 <= ||w(f)||_2, so the corrected Theorem 2 applies to each."
    )

    # Fisher-Rao distance is a proxy for the gap ratio, not a trigger for it:
    # report the rank correlation and count the inversions.
    by_dfr = sorted(brands, key=lambda b: t2[b]["fisher_rao"])
    by_ratio = sorted(brands, key=lambda b: t2[b]["gap_ratio"])
    rank_dfr = {b: i for i, b in enumerate(by_dfr)}
    rank_ratio = {b: i for i, b in enumerate(by_ratio)}
    d2 = sum((rank_dfr[b] - rank_ratio[b]) ** 2 for b in brands)
    n_b = len(brands)
    spearman = 1.0 - 6.0 * d2 / (n_b * (n_b**2 - 1))
    inversions = sum(
        1
        for i, bi in enumerate(brands)
        for bj in brands[i + 1 :]
        if (t2[bi]["fisher_rao"] - t2[bj]["fisher_rao"])
        * (t2[bi]["gap_ratio"] - t2[bj]["gap_ratio"])
        < 0
    )
    print(f"\n  d_FR order:   {' < '.join(by_dfr)}")
    print(f"  A/V* order:   {' < '.join(by_ratio)}")
    print(
        f"  Spearman rho(d_FR, A/V*) = {spearman:.3f} "
        f"over {n_b} pairs, {inversions} inverted pair(s)."
    )
    print(
        "  The distance does not rank-order the gap ratio, so the audit trigger"
        "\n  is stated on A/V* directly, which is computable from the same inputs."
    )

    if args.verify_theorem2:
        print("\n--- Theorem 2 Monte Carlo verification ---\n")
        v = verify_theorem2()
        print("  Counterexample to the PUBLISHED bound (uniform founder):")
        print(f"    {'epsilon':>10}{'A(f,c)':>12}{'H^2/2':>12}   holds?")
        for eps, gap_v, rhs in v["counterexample"]:
            print(f"    {eps:>10g}{gap_v:>12.6f}{rhs:>12.6f}   {gap_v >= rhs}")
        print(
            f"\n  {v['violations_published']} of {v['draws']} random pairs violate"
            " the published bound."
        )
        print(
            f"  {v['violations_corrected']} of {v['tested_under_hypothesis']} pairs"
            " satisfying the concentration hypothesis violate the corrected bound."
        )
        print(
            "  Worst observed A / (H^4/4) = "
            f"{v['worst_ratio_hellinger_form']:.3f} (>= 1 means the bound holds)."
        )
        assert v["violations_corrected"] == 0, v
        assert v["violations_published"] > 0, v

    # Numerical-integrity assertions: catch any drift between paper text
    # and computed values.
    expected = {
        "Hermes": (0.1518, 0.1451, 0.0067, 0.0731),
        "IKEA": (0.2900, 0.2250, 0.0650, 0.1268),
        "Patagonia": (0.1700, 0.1455, 0.0245, 0.1113),
        "Erewhon": (0.1800, 0.1675, 0.0125, 0.0611),
        "Tesla": (0.1800, 0.1515, 0.0285, 0.1315),
    }
    for b, (n2, inn, gap_e, h_e) in expected.items():
        r = results[b]
        assert abs(r["norm_sq_f"] - n2) < 1e-4, (b, r["norm_sq_f"], n2)
        assert abs(r["inner_fc"] - inn) < 1e-4, (b, r["inner_fc"], inn)
        assert abs(r["gap"] - gap_e) < 1e-4, (b, r["gap"], gap_e)
        assert abs(r["hellinger"] - h_e) < 1e-3, (b, r["hellinger"], h_e)

    expected_rank = ["Hermes", "Erewhon", "Patagonia", "Tesla", "IKEA"]
    assert rank == expected_rank, (rank, expected_rank)

    # Theorem 2 (corrected): the hypothesis holds on every illustrative pair,
    # both corrected forms hold, and the published form fails at the uniform
    # founder. These assertions catch transcription drift between the paper
    # text and this script; they are not an independent check of the algebra.
    for b in brands:
        v = t2[b]
        assert v["hypothesis_holds"], b
        assert v["gap"] >= v["euclidean_rhs"] - 1e-12, (b, v)
        assert v["gap"] >= v["hellinger_rhs"] - 1e-12, (b, v)
    _uniform = np.full(8, 1.0 / 8)
    _witness = np.zeros(8)
    _witness[0] = 1.0
    _cx = theorem2_bounds(_uniform, _witness)
    assert abs(_cx["gap"]) < 1e-12, _cx
    assert _cx["published_rhs"] > 0.3, _cx

    expected_ratio = {
        "Hermes": 0.047,
        "IKEA": 0.344,
        "Patagonia": 0.179,
        "Erewhon": 0.079,
        "Tesla": 0.200,
    }
    for b, exp_r in expected_ratio.items():
        assert abs(t2[b]["gap_ratio"] - exp_r) < 1e-3, (b, t2[b]["gap_ratio"], exp_r)

    print("=" * 72)
    print("All computations complete. Numerical-integrity assertions passed.")

    # ------------------------------------------------------------------
    # Optional figures
    # ------------------------------------------------------------------
    if args.write_figures:
        try:
            import matplotlib  # noqa: F401
        except ImportError:
            print(
                "matplotlib is not installed; skipping figures. "
                "Install with `uv add --dev matplotlib`."
            )
            return
        out_dir = args.figure_dir
        print(f"\nWriting figures to: {out_dir}")
        p1 = write_alignment_gap_simplex(out_dir, founders, cohorts)
        print(f"  wrote {p1}")
        p2 = write_founder_vs_cohort_weights(out_dir, founders, cohorts)
        print(f"  wrote {p2}")
        p3 = write_theorem5_interaction_adjustment(out_dir, cohorts)
        print(f"  wrote {p3}")


if __name__ == "__main__":
    main()
