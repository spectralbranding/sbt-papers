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
    cd /Users/d/projects/spectral-branding && uv run python \
        research/computation_scripts/r7_spectral_resource_allocation.py

Run command (numerics + figures):
    cd /Users/d/projects/spectral-branding && uv run python \
        research/computation_scripts/r7_spectral_resource_allocation.py \
        --write-figures

Fixed seed: SEED = 42 (used for any stochastic elements; all
computations here are deterministic).

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
    basis = vt[:2]  # (2, 8)

    def project(w: np.ndarray) -> np.ndarray:
        return basis @ (w - stacked.mean(axis=0))

    fig, ax = plt.subplots(figsize=(6.8, 5.2))
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
        ax.annotate(
            f"{b} (A={gap_val:.4f})",
            xy=((pf[0] + pc[0]) / 2, (pf[1] + pc[1]) / 2),
            xytext=(8, 6),
            textcoords="offset points",
            fontsize=8,
            color=color,
        )
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
            label="Founder w(f)",
        ),
        Line2D(
            [0],
            [0],
            marker="s",
            color="w",
            markerfacecolor="white",
            markeredgecolor="#444",
            markersize=9,
            label="Cohort w(c)",
        ),
        Line2D([0], [0], color="#444", linewidth=1.4, label="Fisher-Rao geodesic"),
    ]
    ax.legend(handles=legend_elems, loc="upper right", fontsize=8)
    ax.set_xlabel("PC1 of stacked weight vectors")
    ax.set_ylabel("PC2 of stacked weight vectors")
    ax.set_title("Alignment gap on the probability simplex (Theorem 2)")
    ax.grid(True, linestyle=":", alpha=0.5)
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
            label="Founder w(f)",
            edgecolor="white",
        )
        ax.bar(
            x + width / 2,
            wc,
            width,
            color=BRAND_COLORS[b],
            alpha=1.0,
            label="Cohort w(c)",
            edgecolor="white",
        )
        gap = float(np.dot(wf, wf) - np.dot(wf, wc))
        ax.set_ylabel(b, fontsize=9)
        ax.set_ylim(0, max(0.55, max(wf.max(), wc.max()) * 1.15))
        ax.grid(True, axis="y", linestyle=":", alpha=0.5)
        ax.text(
            0.99,
            0.92,
            f"A(f,c) = {gap:.4f}",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=8,
        )
    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels(DIM_ABBREV, fontsize=8)
    axes[0].legend(loc="upper right", fontsize=8, ncols=2)
    fig.suptitle(
        "Founder vs cohort weights and alignment gap A(f,c)",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
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
            "Heritage premium\n(w_narr,temp = +.05)",
        ),
        (
            "Tesla",
            tesla_interaction_matrix(-0.03),
            "Luxury paradox\n(w_ideo,temp = -.03)",
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
                sign = "+" if delta[i] > 0 else ""
                ax.annotate(
                    f"{sign}{delta[i]:.4f}",
                    xy=(x[i] + width / 2, s5[i]),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center",
                    fontsize=8,
                )
        ax.set_xticks(x)
        ax.set_xticklabels(DIM_ABBREV, fontsize=8)
        ax.set_title(f"{b}: {title}", fontsize=10)
        ax.grid(True, axis="y", linestyle=":", alpha=0.5)
        ax.legend(loc="upper right", fontsize=8)
    axes[0].set_ylabel("Optimal allocation s*")
    fig.suptitle(
        "Theorem 5 interaction adjustment vs Theorem 1 baseline",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.95))
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
