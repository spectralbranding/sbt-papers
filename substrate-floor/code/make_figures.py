#!/usr/bin/env python3
"""Generate the two paper figures, deterministically (paper Figures 1 and 2).

Companion figure script for "The Substrate Floor." Both figures are reproduced from committed,
seeded code (no hand-drawing), the same reproducibility standard as the numerical results.

  Figure 1 (nested_floors): the nesting operator <= artifact <= substrate and the no-rescue
    geometry — two instruments that agree yet each read below their own floor cannot lift the
    consensus above the effective (outermost) floor.
  Figure 2 (verdict_regions): the four typed verdicts as regions of the (substrate dispersion,
    consensus signal) plane, from a seeded Monte-Carlo sweep of the two-instrument lattice.

Reproduce:
    uv run --with numpy --with matplotlib python code/make_figures.py
Fixed seed 20260624. Writes PNGs to figures/.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

import sys  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verdict_regions_mc import classify_vec, _CODE, VERDICTS  # noqa: E402

FIGDIR = HERE.parent / "figures"
SEED = 20260624

# Colour-blind-safe palette (Okabe-Ito), one per verdict.
COLOURS = {
    "corroborated": "#009E73",  # green
    "contested": "#D55E00",  # vermilion
    "substrate-conditional": "#0072B2",  # blue
    "jointly-unresolved": "#999999",  # grey
}
INK = "#222222"


def figure_nested_floors() -> None:
    """Figure 1: nesting + no-rescue, drawn as a clean two-panel schematic."""
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.0, 3.8))

    # --- Left panel: nesting operator <= artifact <= substrate ----------------
    floors = [
        ("operator floor", 0.18),
        ("artifact floor", 0.30),
        ("substrate floor", 0.46),
    ]
    ys = [2.4, 1.6, 0.8]
    for (label, f), y in zip(floors, ys):
        axL.barh(y, f, height=0.42, color="#cfe8df", edgecolor=INK, linewidth=1.0)
        axL.text(
            f + 0.012,
            y,
            f"{label}\n(width {f:.2f})",
            va="center",
            fontsize=8.5,
            color=INK,
        )
    eff = max(f for _, f in floors)
    axL.axvline(eff, color=COLOURS["contested"], lw=1.6, ls="--")
    axL.text(
        eff + 0.005,
        3.15,
        "effective floor = max",
        color=COLOURS["contested"],
        fontsize=8.5,
        fontweight="bold",
    )
    # two example consensus signals
    axL.annotate(
        "",
        xy=(0.62, 0.2),
        xytext=(0.0, 0.2),
        arrowprops=dict(arrowstyle="-|>", color=COLOURS["corroborated"], lw=2.2),
    )
    axL.text(
        0.62,
        0.2,
        "  clears -> survives",
        va="center",
        fontsize=8.5,
        color=COLOURS["corroborated"],
        fontweight="bold",
    )
    axL.annotate(
        "",
        xy=(0.40, -0.4),
        xytext=(0.0, -0.4),
        arrowprops=dict(arrowstyle="-|>", color=COLOURS["jointly-unresolved"], lw=2.2),
    )
    axL.text(0.40, -0.4, "  below -> abstain", va="center", fontsize=8.5, color=INK)
    axL.set_xlim(0, 0.95)
    axL.set_ylim(-0.9, 3.5)
    axL.set_yticks([])
    axL.set_xlabel("signal magnitude", fontsize=9)
    axL.set_title(
        "a  Floors nest; clear the outermost",
        fontsize=10,
        loc="left",
        fontweight="bold",
    )
    for s in ("top", "right", "left"):
        axL.spines[s].set_visible(False)

    # --- Right panel: no rescue from agreement --------------------------------
    # two instruments agree (small dispersion) yet each reads below its own floor.
    v1, f1 = 0.22, 0.34
    v2, f2 = 0.26, 0.30
    eff_r = max(abs(v1 - v2), f1, f2)
    consensus = (v1 + v2) / 2
    for v, f, y, name in [(v1, f1, 1.7, "instrument 1"), (v2, f2, 1.0, "instrument 2")]:
        axR.errorbar(
            v,
            y,
            xerr=f,
            fmt="o",
            color=COLOURS["substrate-conditional"],
            ecolor=INK,
            elinewidth=1.3,
            capsize=4,
            ms=7,
        )
        axR.text(
            v,
            y + 0.22,
            f"{name}: |signal| {v:.2f} < floor {f:.2f}",
            ha="center",
            fontsize=8.3,
            color=INK,
        )
    axR.axvline(eff_r, color=COLOURS["contested"], lw=1.6, ls="--")
    axR.text(
        eff_r + 0.006,
        2.35,
        "effective floor",
        color=COLOURS["contested"],
        fontsize=8.5,
        fontweight="bold",
    )
    axR.plot(
        [consensus], [0.35], marker="v", color=COLOURS["jointly-unresolved"], ms=10
    )
    axR.text(
        consensus,
        0.05,
        "consensus (agreement)\nstill below floor -> no rescue",
        ha="center",
        va="top",
        fontsize=8.3,
        color=INK,
    )
    axR.set_xlim(0, 0.62)
    axR.set_ylim(-0.5, 2.7)
    axR.set_yticks([])
    axR.set_xlabel("signal magnitude", fontsize=9)
    axR.set_title(
        "b  No rescue from agreement", fontsize=10, loc="left", fontweight="bold"
    )
    for s in ("top", "right", "left"):
        axR.spines[s].set_visible(False)

    fig.tight_layout()
    out = FIGDIR / "figure1_nested_floors.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")


def figure_verdict_regions() -> None:
    """Figure 2: the four verdicts as CLEAN regions of the (dispersion, consensus) plane.

    At a fixed per-instrument floor f, the pair (dispersion D, consensus c) uniquely determines the
    two verdict values v1 = c + D/2, v2 = c - D/2, so the verdict is a crisp function of (D, c).
    Two panels show how the regions shift as the floor widens (a narrow floor resolves more; a wide
    floor abstains more), the qualitative content of the Monte-Carlo fractions reported in the text.
    """
    floors = [0.10, 0.25]
    grid = 600
    Dv = np.linspace(0, 1, grid)
    Cv = np.linspace(0, 1, grid)
    DD, CC = np.meshgrid(Dv, Cv)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 5.0), sharey=True)
    for ax, f in zip(axes, floors):
        v1 = CC + DD / 2.0
        v2 = CC - DD / 2.0
        valid = (v1 <= 1.0) & (v2 >= 0.0)
        f1 = np.full_like(v1, f)
        f2 = np.full_like(v2, f)
        code, _ = classify_vec(v1.ravel(), v2.ravel(), f1.ravel(), f2.ravel())
        code = code.reshape(v1.shape).astype(float)
        code[~valid] = np.nan  # outside the achievable (D, c) triangle

        cmap = matplotlib.colors.ListedColormap([COLOURS[v] for v in VERDICTS])
        cmap.set_bad("white")
        ax.pcolormesh(DD, CC, code, cmap=cmap, vmin=-0.5, vmax=3.5, shading="auto")
        ax.set_xlabel("substrate dispersion  D = |v1 - v2|", fontsize=10)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(
            f"per-instrument floor f = {f:.2f}",
            fontsize=10,
            loc="left",
            fontweight="bold",
        )
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[0].set_ylabel("consensus signal  |c| = mean(resolvers)", fontsize=10)
    handles = [mpatches.Patch(color=COLOURS[v], label=v) for v in VERDICTS]
    axes[1].legend(
        handles=handles,
        loc="upper right",
        fontsize=8.3,
        framealpha=0.96,
        title="typed verdict",
        title_fontsize=8.3,
    )
    fig.suptitle(
        "Verdict regions of the two-instrument lattice (k_resolve = 2, k_marginal = 1)",
        fontsize=11,
        fontweight="bold",
        x=0.02,
        ha="left",
    )

    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = FIGDIR / "figure2_verdict_regions.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")


def main() -> None:
    FIGDIR.mkdir(exist_ok=True)
    figure_nested_floors()
    figure_verdict_regions()


if __name__ == "__main__":
    main()
