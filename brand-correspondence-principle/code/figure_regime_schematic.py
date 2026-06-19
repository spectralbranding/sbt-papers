#!/usr/bin/env python3
"""Conceptual figure for "The Correspondence Principle of Brand Management" (2026au).

Figure 1: the perception cloud versus its scalar projection, with the four
regime-departure parameters drawn as the directions along which the cloud leaves
the classical (score-sufficient) corner. This is a SCHEMATIC, not a data figure;
it illustrates the geometry the theorems formalize. It is kept in a SEPARATE
script from the computation (correspondence_loss_surface.py) so that the
computation stays NumPy-only and reproducible without a plotting dependency.

RUN:
    cd [internal path removed]
    uv run --with matplotlib python [internal path removed]

OUTPUT: [internal path removed]  (fixed seed)
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SEED = 20260619
OUT = os.path.join(
    os.path.dirname(__file__), "..", "figures", "figure1_cloud_vs_projection.png"
)


def main():
    rng = np.random.default_rng(SEED)
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 5.0))

    # ---- Left: the flat map (scalar projection) ----
    axL.set_title("The score: a scalar projection", fontsize=12)
    axL.axhline(0, color="0.4", lw=1.2)
    axL.plot([0.42], [0], "o", ms=12, color="#1f77b4")
    axL.annotate(
        "aggregate brand-health score\n(one number on one axis)",
        xy=(0.42, 0),
        xytext=(0.18, 0.55),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="0.3"),
    )
    axL.set_xlim(0, 1)
    axL.set_ylim(-1, 1)
    axL.set_xlabel("read dimension (e.g. Semiotic)")
    axL.set_yticks([])
    axL.set_xticks([])
    for s in ["top", "right", "left"]:
        axL.spines[s].set_visible(False)

    # ---- Right: the perception cloud + the four regime departures ----
    axR.set_title("The perception cloud: where the score fails", fontsize=12)
    # primary human cohort (tight, on the read axis)
    c1 = rng.normal([0.55, 0.0], [0.07, 0.06], size=(140, 2))
    axR.scatter(
        c1[:, 0], c1[:, 1], s=10, color="#1f77b4", alpha=0.6, label="human cohort"
    )
    # the read axis u (horizontal) and the score point
    axR.axhline(0, color="0.6", lw=1.0, ls="--")
    axR.plot([0.55], [0.0], "o", ms=11, color="#1f77b4")
    axR.annotate(
        "score reads only\nthis axis (dashed)",
        xy=(0.30, 0.0),
        xytext=(0.04, -0.42),
        fontsize=8,
        color="0.35",
        arrowprops=dict(arrowstyle="->", color="0.6"),
    )

    # sigma: dispersion / second mode off-axis
    c2 = rng.normal([0.45, 0.55], [0.08, 0.07], size=(70, 2))
    axR.scatter(c2[:, 0], c2[:, 1], s=10, color="#2ca02c", alpha=0.6)
    axR.annotate(
        r"$\sigma$: dispersion / 2nd mode",
        xy=(0.45, 0.55),
        xytext=(0.02, 0.86),
        fontsize=9,
        color="#2ca02c",
        arrowprops=dict(arrowstyle="->", color="#2ca02c"),
    )

    # alpha: AI cohort collapsed off-axis
    c3 = rng.normal([0.78, -0.5], [0.05, 0.05], size=(55, 2))
    axR.scatter(c3[:, 0], c3[:, 1], s=10, color="#d62728", alpha=0.7)
    axR.annotate(
        r"$\alpha$: AI cohort (collapsed)",
        xy=(0.78, -0.5),
        xytext=(0.50, -0.95),
        fontsize=9,
        color="#d62728",
        arrowprops=dict(arrowstyle="->", color="#d62728"),
    )

    # epsilon: exogenous near-uniform mass
    c4 = rng.uniform([0.15, -0.7], [0.95, 0.8], size=(40, 2))
    axR.scatter(c4[:, 0], c4[:, 1], s=8, color="#9467bd", alpha=0.35)
    axR.annotate(
        r"$\varepsilon$: exogenous signal",
        xy=(0.2, 0.5),
        xytext=(0.02, 0.30),
        fontsize=9,
        color="#9467bd",
        arrowprops=dict(arrowstyle="->", color="#9467bd"),
    )

    # v: temporal drift arrow
    axR.annotate(
        "",
        xy=(0.72, 0.22),
        xytext=(0.55, 0.0),
        arrowprops=dict(arrowstyle="->", color="#ff7f0e", lw=2),
    )
    axR.annotate(
        r"$v$: temporal drift",
        xy=(0.72, 0.22),
        xytext=(0.74, 0.55),
        fontsize=9,
        color="#ff7f0e",
    )

    axR.set_xlim(0, 1)
    axR.set_ylim(-1, 1)
    axR.set_xlabel("read dimension (e.g. Semiotic)")
    axR.set_ylabel("off-axis dimensions (projected away by the score)")
    axR.set_xticks([])
    axR.set_yticks([])
    for s in ["top", "right"]:
        axR.spines[s].set_visible(False)

    fig.suptitle(
        "Each regime-departure parameter moves perceptual mass off the score axis; "
        "the dominance gap is that off-axis variance.",
        fontsize=10,
        y=0.05,
    )
    fig.tight_layout(rect=[0, 0.09, 1, 1])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, dpi=150)
    print(f"wrote {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
