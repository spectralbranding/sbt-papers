#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26", "scipy>=1.12", "matplotlib>=3.8"]
# ///
"""power_analysis.py — PRISM-O (2026bd) pre-registered power computation + figure.

Reproduces the PREREGISTRATION.md §6 power analysis: a two-sided one-sample
t-test on resolved per-organization gaps at alpha = .017 (Bonferroni across
H1-H3), across-organization gap SD assumed 1.0 rung (conservative on a 4-rung
ladder). Power via the noncentral t distribution: for n resolved
organizations and mean gap g, ncp = (g / SD) * sqrt(n).

Emits research/papers/2026bd/figures/power_curves.png (300 dpi, no on-image
title per corpus figure standard) and prints the .80-power crossing for each
curve. Deterministic computation; SEED fixed for reproducibility of any
future stochastic extension.

Run command:
    uv run python research/prism_o/code/power_analysis.py

Output:
    research/papers/2026bd/figures/power_curves.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

SEED = 20260703
ALPHA = 0.017  # Bonferroni: family-wise .05 across H1-H3
SD_GAP = 1.0  # rung units, conservative (PL0 section 6)
GAPS = (0.25, 0.50, 0.75)  # mean gap in rung units
N_RANGE = np.arange(5, 121)
MIN_RESOLVED_N = 45  # PL0 section 6/7 minimum-resolved-N target

FIG_DIR = Path(__file__).resolve().parents[2] / "papers" / "2026bd" / "figures"


def power_one_sample_t(n: int, gap: float, sd: float, alpha: float) -> float:
    """Exact two-sided one-sample t power via the noncentral t."""
    df = n - 1
    ncp = (gap / sd) * np.sqrt(n)
    t_crit = stats.t.ppf(1.0 - alpha / 2.0, df)
    return float(1.0 - stats.nct.cdf(t_crit, df, ncp) + stats.nct.cdf(-t_crit, df, ncp))


def main() -> int:
    np.random.seed(SEED)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    styles = ("-", "--", ":")
    for gap, ls in zip(GAPS, styles):
        power = [power_one_sample_t(int(n), gap, SD_GAP, ALPHA) for n in N_RANGE]
        ax.plot(
            N_RANGE,
            power,
            ls,
            color="#1f4e79",
            linewidth=2.0,
            label=f"gap = {gap:.2f} rung".replace("0.", "."),
        )
        crossing = next((int(n) for n, p in zip(N_RANGE, power) if p >= 0.80), None)
        print(f"gap {gap:.2f}: .80 power at n = {crossing}")
    ax.axhline(0.80, color="gray", linestyle="-", linewidth=1.0, alpha=0.6)
    ax.axvline(
        MIN_RESOLVED_N,
        color="#b2182b",
        linestyle="--",
        linewidth=1.5,
        label=f"minimum-resolved-N = {MIN_RESOLVED_N}",
    )
    ax.set_xlabel("Resolved organizations (n)", fontsize=12)
    ax.set_ylabel("Power (two-sided one-sample t, alpha = .017)", fontsize=12)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlim(int(N_RANGE[0]), int(N_RANGE[-1]))
    ax.legend(fontsize=10, loc="lower right")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / "power_curves.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    print(f"Saved: {out}")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
