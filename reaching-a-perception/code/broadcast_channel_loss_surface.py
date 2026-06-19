"""Broadcast-channel loss surface for the cohort-reach handoff contract (2026av).

Reproduces Figure 1 of "Reaching a Perception: From Perceptual Cohort to
Reachable Audience". The figure is the total-loss surface over two quantities
that govern the bridge choice in the measurement-to-activation handoff contract:

  - cohort distinctiveness  s = sin^2(beta)  in [0, 1]
        the off-axis perceptual distinctiveness of the target cohort; the same
        quantity that is a perception-metamerism LOSS in the parent paper
        (2026au) is, read forward, the self-selection SHARPNESS of the
        broadcast-a-dimension bridge.
  - per-impression spill cost  c  in [0, 1]
        the cost of an impression delivered to a non-resonant observer; this is
        the only cost of the address-free broadcast route.

Two bridges compete:

  Broadcast-a-dimension (route b): emit on the dimension the cohort is
      sensitive to and let self-selection route the signal. Sharper separation
      as distinctiveness rises, so the spill fraction falls. We model the
      delivered total loss as the spill cost paid on the non-resonant fraction:
          L_broadcast(s, c) = c * (1 - s)
      (a more distinct cohort self-selects more cleanly -> less spill).

  Minimal-loss proxy (route a): map the cohort to the most informative
      addressable proxy P* and pay the Blackwell-garbling decision loss
      L(P*) = L0, independent of the broadcast spill cost. Calibrated to a
      representative proxy-informativeness level (median mutual information
      between perceptual-cohort membership and addressable proxy features in
      the atom corpus); held fixed here as the illustrative constant L0.

The handoff contract routes to whichever bridge has the lower total loss:
          L_min(s, c) = min( c * (1 - s), L0 )
The frontier c*(1 - s) = L0 is where the two bridges tie. Above/left of it the
broadcast bridge dominates (distinct cohort, cheap spill); below/right the proxy
bridge dominates. The critical-distinctiveness scope condition (~.35 in the
paper) is the value of s at which broadcast ties the proxy at a representative
spill cost c_ref.

Deterministic: no randomness, no network, no credentials. NumPy + Matplotlib.

Run:
    uv run python code/broadcast_channel_loss_surface.py
Outputs:
    figures/figure1_loss_surface.png
    prints the critical distinctiveness at the representative spill cost.
"""

from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# A stroke halo makes overlaid text legible on ANY background colour (the
# viridis surface runs dark-purple -> green -> yellow, so neither plain white
# nor plain black text is readable everywhere). White text + a black outline is.
HALO = [pe.withStroke(linewidth=3.0, foreground="black")]

# --- calibration constants (documented; illustrative, not fit to live data) ---
L0 = 0.20  # minimal-loss-proxy decision loss L(P*), representative level
C_REF = 0.31  # representative per-impression spill cost for the threshold read
GRID = 400  # surface resolution


def loss_broadcast(s, c):
    """Total delivered loss of the broadcast-a-dimension bridge."""
    return c * (1.0 - s)


def loss_proxy(_s, _c):
    """Total decision loss of the minimal-loss-proxy bridge (flat in s, c)."""
    return np.full_like(_s, L0)


def critical_distinctiveness(c_ref=C_REF, l0=L0):
    """Value of s at which broadcast ties the proxy at spill cost c_ref:
    c_ref * (1 - s) = l0  =>  s = 1 - l0 / c_ref.
    """
    return 1.0 - l0 / c_ref


def main():
    here = Path(__file__).resolve().parent
    figdir = here.parent / "figures"
    figdir.mkdir(exist_ok=True)

    s = np.linspace(0.0, 1.0, GRID)  # cohort distinctiveness sin^2(beta)
    c = np.linspace(0.0, 1.0, GRID)  # per-impression spill cost
    S, C = np.meshgrid(s, c)

    Lb = loss_broadcast(S, C)
    Lp = loss_proxy(S, C)
    Lmin = np.minimum(Lb, Lp)

    s_crit = critical_distinctiveness()

    fig, ax = plt.subplots(figsize=(7.0, 5.4))
    im = ax.pcolormesh(S, C, Lmin, shading="auto", cmap="viridis")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("minimum total loss  min(spill, proxy-join loss)")

    # frontier where the two bridges tie: c*(1 - s) = L0
    ax.contour(
        S, C, Lb - Lp, levels=[0.0], colors="white", linewidths=2.0, linestyles="--"
    )

    # region labels (white text + black stroke halo -> legible on any background)
    ax.text(
        0.74,
        0.20,
        "broadcast a\ndimension (b)\ndominates",
        color="white",
        ha="center",
        va="center",
        fontsize=10,
        weight="bold",
        path_effects=HALO,
    )
    ax.text(
        0.22,
        0.82,
        "minimal-loss\nproxy (a)\ndominates",
        color="white",
        ha="center",
        va="center",
        fontsize=10,
        weight="bold",
        path_effects=HALO,
    )

    # critical-distinctiveness marker at the representative spill cost
    ax.plot(
        [s_crit], [C_REF], "o", color="white", markersize=8, markeredgecolor="black"
    )
    ann = ax.annotate(
        f"critical distinctiveness\ns = {s_crit:.2f} at spill c = {C_REF:.2f}",
        xy=(s_crit, C_REF),
        xytext=(s_crit + 0.04, C_REF + 0.16),
        color="white",
        fontsize=9,
        weight="bold",
        arrowprops=dict(
            arrowstyle="->",
            color="white",
            path_effects=[pe.withStroke(linewidth=2.5, foreground="black")],
        ),
    )
    ann.set_path_effects(HALO)

    ax.set_xlabel(r"cohort distinctiveness  $\sin^2\beta$")
    ax.set_ylabel("per-impression spill cost  $c$")
    ax.set_title("Total-loss surface and bridge frontier (2026av Figure 1)")
    fig.tight_layout()

    out = figdir / "figure1_loss_surface.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")
    print(f"critical distinctiveness at spill c={C_REF}: s = {s_crit:.3f}")


if __name__ == "__main__":
    main()
