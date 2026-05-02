#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Reproduce R18 Figure 2: Dove (Cultural, Ideological) phase trajectory.

Inputs:
    Table 1 (R18 paper): Dove spectral profiles at four temporal cross-sections,
    scale 1-10, eight dimensions. The Ideological dimension is undefined (None)
    at 2003 (dimensional creation event); the trajectory in (Cultural,
    Ideological) space therefore begins at 2006 once both dimensions are
    defined.

Method:
    Plot the (Cultural, Ideological) position at each available time point
    {2006, 2013, 2023}. Connect consecutive points with arrows showing the
    direction of motion across each period. The figure illustrates how
    trajectory geometry rotates across the Ignition -> Expansion ->
    Normative-Absorption phases.

Outputs:
    figure2_dove_phase.png

Run:
    uv run python phase_portrait.py

Reference:
    Zharnikov, D. (2026z). Spectral Dynamics: Velocity, Acceleration, and Phase
    Space in Multi-Dimensional Brand Perception. Working Paper.
    https://doi.org/10.5281/zenodo.19468204
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Fixed seed for reproducibility of any future randomized extensions; the
# trajectory plot itself is deterministic given Table 1 inputs.
SEED = 20260501
np.random.seed(SEED)

# Table 1 (Dove): (Cultural, Ideological) extracted; Ideological is undefined
# at 2003 (dimensional creation event), so trajectory starts at 2006.
TRAJECTORY = [
    # (year, Cultural, Ideological, label)
    (2006, 8.5, 8.0, "2006"),
    (2013, 8.0, 9.0, "2013"),
    (2023, 5.5, 7.5, "2023"),
]


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / "figure2_dove_phase.png"

    years = [p[0] for p in TRAJECTORY]
    cultural = np.array([p[1] for p in TRAJECTORY])
    ideological = np.array([p[2] for p in TRAJECTORY])
    labels = [p[3] for p in TRAJECTORY]

    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=200)

    # Plot points.
    ax.scatter(cultural, ideological, s=80, color="#1f4e79", zorder=3)

    # Annotate each point with its year.
    for c, i, lab in zip(cultural, ideological, labels):
        ax.annotate(
            lab,
            xy=(c, i),
            xytext=(8, 8),
            textcoords="offset points",
            fontsize=11,
            color="#1f4e79",
        )

    # Arrow segments showing direction of motion.
    for k in range(len(TRAJECTORY) - 1):
        c0, i0 = cultural[k], ideological[k]
        c1, i1 = cultural[k + 1], ideological[k + 1]
        ax.annotate(
            "",
            xy=(c1, i1),
            xytext=(c0, i0),
            arrowprops=dict(
                arrowstyle="-|>",
                color="#666666",
                lw=1.6,
                shrinkA=8,
                shrinkB=8,
            ),
        )

    # Period labels at midpoints.
    period_labels = ["Expansion", "Normative Absorption"]
    for k, lab in enumerate(period_labels):
        cm = (cultural[k] + cultural[k + 1]) / 2.0
        im = (ideological[k] + ideological[k + 1]) / 2.0
        ax.annotate(
            lab,
            xy=(cm, im),
            xytext=(10, -14),
            textcoords="offset points",
            fontsize=9,
            style="italic",
            color="#444444",
        )

    ax.set_xlabel("Cultural dimension (1-10)")
    ax.set_ylabel("Ideological dimension (1-10)")
    ax.set_xlim(4.5, 9.5)
    ax.set_ylim(6.5, 10.0)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_title("Dove (Cultural, Ideological) phase trajectory, 2006-2023")

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
