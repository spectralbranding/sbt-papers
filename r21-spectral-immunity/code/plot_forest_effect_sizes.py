"""
Figure 2: Forest Plot of Portfolio Effect Sizes — R21 Spectral Immunity
=======================================================================
Reads Cohen's d and DCI delta values from Tables 3 and 7 (paper §Results) and
produces figures/figure2_forest.png.

Reproduces Figure 2 in:
    Zharnikov, D. (2026ac). Spectral Immunity: Why Brand Portfolio Interference
    Disappears for AI Observers. Working Paper. DOI 10.5281/zenodo.19765401

Run command:
    uv run python code/plot_forest_effect_sizes.py

Python version: 3.12
Fixed random seed: 42
Output: figures/figure2_forest.png

Requirements: matplotlib (see requirements.txt)
"""

import math
import pathlib
import sys

# ---------------------------------------------------------------------------
# Data extracted from Tables 3 and 7 of the paper
# Format: (brand, archetype, d, tost_equivalent)
# Positive d = portfolio increased DCI; negative = portfolio decreased DCI
# ---------------------------------------------------------------------------

TABLE3_DATA = [
    # (brand, archetype, cohen_d, tost_equivalent)
    ("Dior",           "LVMH cluster",             +0.20, True),
    ("Fendi",          "LVMH cluster",             +0.07, True),
    ("Louis Vuitton",  "LVMH cluster",             +0.16, True),
    ("Axe",            "Unilever contradiction",   +0.02, True),
    ("Ben and Jerrys", "Unilever contradiction",   -0.04, True),
    ("Dove",           "Unilever contradiction",   +0.21, True),
    ("Gillette",       "P&G spread",               -0.13, True),
    ("Pampers",        "P&G spread",               -0.22, True),
    ("Tide",           "P&G spread",               -0.10, True),
    ("Toyota",         "Toyota layer",             -0.30, True),
    ("Lexus",          "Toyota layer",             +0.52, True),
    ("LOreal Paris",   "LOreal prestige",          -0.13, True),
    ("Lancome",        "LOreal prestige",          +0.03, True),
    ("Maybelline",     "LOreal prestige",          -0.07, True),
    ("Volvo",          "Geely reverse",            -0.15, True),
    ("Polestar",       "Geely reverse",            -0.07, True),
    ("Geely Auto",     "Geely reverse",            +0.27, False),
    ("Yandex",         "Yandex branded house",     -0.01, True),
    ("Yandex Market",  "Yandex branded house",     +0.10, True),
    ("Yandex Taxi",    "Yandex branded house",     -0.16, False),
]

TABLE7_DATA = [
    # (brand, archetype_label, cohen_d, tost_equivalent)
    ("Coca-Cola",  "Published brand extension", +0.08, True),
    ("Pepsi",      "Published brand extension", +0.11, True),
    ("BMW",        "Published brand extension", -0.18, True),
    ("Audi",       "Published brand extension", +0.49, True),
    ("Google",     "Published brand extension", +0.06, True),
    ("Disney",     "Published brand extension", +0.04, True),
    ("Colgate",    "Published brand extension", +0.21, True),
    ("Samsung",    "Published brand extension", +0.06, True),
    ("H&M",        "Published brand extension", -0.29, True),
    ("Dell",       "Published brand extension", +0.16, True),
]

TOST_BOUND = 1.0

# Archetype display order (for grouping on y-axis)
ARCHETYPE_ORDER = [
    "LVMH cluster",
    "Unilever contradiction",
    "P&G spread",
    "Toyota layer",
    "LOreal prestige",
    "Geely reverse",
    "Yandex branded house",
    "Published brand extension",
]

ARCHETYPE_COLORS = {
    "LVMH cluster":               "#9370DB",
    "Unilever contradiction":     "#E07B39",
    "P&G spread":                 "#4682B4",
    "Toyota layer":               "#2E8B57",
    "LOreal prestige":            "#D4317A",
    "Geely reverse":              "#8B4513",
    "Yandex branded house":       "#DAA520",
    "Published brand extension":  "#708090",
}


def _ci_from_d(d: float, n: int = 65, alpha: float = 0.05) -> tuple[float, float]:
    """
    Approximate 95% CI for Cohen's d using the large-sample normal approximation.
    se(d) ≈ sqrt((n1+n2)/(n1*n2) + d^2/(2*(n1+n2)))  for two equal groups
    For paired design: se(d) ≈ sqrt(1/n + d^2/(2*n))
    """
    se = math.sqrt(1.0 / n + d ** 2 / (2 * n))
    # z_crit ≈ 1.96 for alpha=.05
    z = 1.96
    return d - z * se, d + z * se


def plot_forest(output_path: pathlib.Path) -> None:
    """Generate the forest plot and save to output_path."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        print("matplotlib is required. Install with: uv add matplotlib")
        sys.exit(1)

    all_data = TABLE3_DATA + TABLE7_DATA

    # Build ordered list: group by archetype in ARCHETYPE_ORDER, within each group
    # order by d descending
    grouped: dict[str, list] = {a: [] for a in ARCHETYPE_ORDER}
    for brand, archetype, d, equiv in all_data:
        grouped[archetype].append((brand, d, equiv))

    for a in grouped:
        grouped[a].sort(key=lambda x: x[1], reverse=True)

    # Flatten to (y_index, label, archetype, d, equiv)
    rows = []
    y = 0
    archetype_midpoints: dict[str, float] = {}
    for archetype in ARCHETYPE_ORDER:
        brands = grouped[archetype]
        if not brands:
            continue
        start_y = y
        for brand, d, equiv in brands:
            rows.append((y, brand, archetype, d, equiv))
            y += 1
        # Add a gap between archetypes
        archetype_midpoints[archetype] = (start_y + y - 1) / 2.0
        y += 0.6  # visual gap

    n_rows = len(rows)
    fig_height = max(8, n_rows * 0.38)
    fig, ax = plt.subplots(figsize=(10, fig_height))

    # Draw TOST equivalence bounds
    ax.axvline(x=-TOST_BOUND, color="crimson", linestyle="--", linewidth=1.2,
               label=f"TOST bound (+-{TOST_BOUND:.1f} DCI)")
    ax.axvline(x=+TOST_BOUND, color="crimson", linestyle="--", linewidth=1.2)
    ax.axvline(x=0, color="black", linestyle="-", linewidth=0.6, alpha=0.4)

    # Plot each row
    y_positions = []
    y_labels = []
    for row_y, brand, archetype, d, equiv in rows:
        lo, hi = _ci_from_d(d)
        color = ARCHETYPE_COLORS.get(archetype, "gray")
        marker = "o" if equiv else "D"
        ax.plot([lo, hi], [row_y, row_y], color=color, linewidth=1.2, alpha=0.7)
        ax.plot(d, row_y, marker=marker, color=color, markersize=7,
                markeredgecolor="white", markeredgewidth=0.5)
        y_positions.append(row_y)
        y_labels.append(brand)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=8)
    ax.invert_yaxis()

    ax.set_xlabel("Cohen's d (portfolio - solo)", fontsize=10)
    ax.set_xlim(-2.0, 2.0)
    ax.set_title(
        "Portfolio-Framing Effect Sizes by Archetype and Modality\n"
        "Circles = TOST equivalent; diamonds = inconclusive",
        fontsize=10,
    )

    # Archetype group labels on right margin
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    archetype_y: list[float] = []
    archetype_labels: list[str] = []
    for archetype, midpoint in archetype_midpoints.items():
        archetype_y.append(midpoint)
        archetype_labels.append(archetype.replace(" ", "\n"))
    ax2.set_yticks(archetype_y)
    ax2.set_yticklabels(archetype_labels, fontsize=7.5, color="dimgray")
    ax2.tick_params(axis="y", length=0)

    # Legend
    legend_handles = [
        mpatches.Patch(color=ARCHETYPE_COLORS[a], label=a) for a in ARCHETYPE_ORDER
    ]
    legend_handles.append(
        plt.Line2D([0], [0], color="crimson", linestyle="--",
                   label=f"TOST bound +/-{TOST_BOUND:.1f}")
    )
    ax.legend(handles=legend_handles, loc="lower right", fontsize=7.5,
              framealpha=0.8, ncol=2)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Figure 2 saved to {output_path}")
    plt.close(fig)


if __name__ == "__main__":
    repo_root = pathlib.Path(__file__).parent.parent
    output = repo_root / "figures" / "figure2_forest.png"
    plot_forest(output)
