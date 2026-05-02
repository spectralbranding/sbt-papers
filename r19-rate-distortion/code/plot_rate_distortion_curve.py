# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "matplotlib"]
# ///
"""
plot_rate_distortion_curve.py — Figure 1 for R19 (2026aa)

Generates the J-shaped rate-distortion curve from Table 2 data.

Run:
    uv run python code/plot_rate_distortion_curve.py

Output:
    figures/figure1_j_curve.png

Data source:
    Table 2 of paper.md (Cross-Model Distortion by Rate Condition).
    Values are cross-model means and SDs across 17 LLM architectures.

Seed: 42 (not used for sampling; set for reproducibility of any random state).
"""

import random
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# ── Fixed seed ────────────────────────────────────────────────────────────────
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# ── Table 2 data (hard-coded from paper Table 2) ───────────────────────────────
# Rate condition labels, bits, mean distortion d, SD across 17 models
rate_conditions = ["R1", "R2", "R3", "R4", "R5"]
bits = [26, 19, 13, 8, 3]
mean_d = [0.172, 0.087, 0.111, 0.181, 0.857]
sd_d   = [0.036, 0.011, 0.016, 0.036, 0.015]

# ── Plot ───────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 4.5))

# Main line with markers
ax.errorbar(
    bits, mean_d,
    yerr=sd_d,
    fmt="o-",
    color="#1a1a6e",
    ecolor="#5a5aae",
    elinewidth=1.4,
    capsize=4,
    capthick=1.4,
    linewidth=1.8,
    markersize=7,
    zorder=3,
)

# Annotate each point with rate code
for rc, b, d in zip(rate_conditions, bits, mean_d):
    offset = (4, 10) if rc != "R2" else (-18, 10)
    ax.annotate(
        rc,
        xy=(b, d),
        xytext=offset,
        textcoords="offset points",
        fontsize=9,
        color="#1a1a6e",
    )

# Highlight R2 minimum with a dashed vertical guide
ax.axvline(x=19, color="#cc4444", linestyle="--", linewidth=1.0, alpha=0.6, zorder=1)
ax.text(
    19.6, 0.50,
    "R2 minimum\n(~19 bits,\n1–5 ordinal)",
    fontsize=8,
    color="#cc4444",
    va="top",
)

# Axes labels and formatting
ax.set_xlabel("Information rate (bits)", fontsize=11)
ax.set_ylabel("Mean distortion — total variation distance", fontsize=11)
ax.set_xticks(bits)
ax.set_xticklabels([str(b) for b in bits], fontsize=9)
ax.set_xlim(0, 30)
ax.set_ylim(-0.05, 1.05)
ax.tick_params(axis="y", labelsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.5, zorder=0)

plt.tight_layout()

# ── Save ───────────────────────────────────────────────────────────────────────
out_path = Path(__file__).parent.parent / "figures" / "figure1_j_curve.png"
out_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved: {out_path}")
