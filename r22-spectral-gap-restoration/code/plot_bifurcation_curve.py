"""
Bifurcation curve for spectral gap vs mu/lambda ratio.

Description:
    For 50 values of mu/lambda in [0.5, 2.0], simulates N=2000 sample paths of a
    discrete-time Ornstein-Uhlenbeck-like process on the spectral gap with fixed
    leakage rate lambda=0.1 and emission rate mu = ratio * lambda. Tracks mean
    spectral gap at t=100 (proxy for tau_mix equilibration). Plots ratio (x) vs
    mean terminal spectral gap (y) with a vertical dashed line at ratio=1.0.

Run command:
    uv run python plot_bifurcation_curve.py

Output:
    ../figures/figure2_bifurcation.png  (300 dpi)

Seed: 42 (fixed for reproducibility)
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

np.random.seed(42)

# --- Parameters ---
lambda_fixed = 0.1
n_ratios = 50
ratios = np.linspace(0.5, 2.0, n_ratios)
N_paths = 2000
T_steps = 100
sigma = 0.05          # noise std for the OU process
gap_init = 1.0        # initial spectral gap

mean_terminal_gaps = np.empty(n_ratios)

for i, ratio in enumerate(ratios):
    mu = ratio * lambda_fixed
    # Discrete-time OU: gap_{t+1} = gap_t + (mu - lambda) * gap_t * dt + sigma * noise
    # dt = 1 (unit step); drift coefficient = (mu - lambda)
    dt = 1.0
    drift = (mu - lambda_fixed) * dt
    gaps = np.full(N_paths, gap_init, dtype=float)
    for _ in range(T_steps):
        noise = np.random.randn(N_paths) * sigma
        gaps = gaps + drift * gaps + noise
        # spectral gap is non-negative by definition
        gaps = np.maximum(gaps, 0.0)
    mean_terminal_gaps[i] = gaps.mean()

# --- Plot ---
fig, ax = plt.subplots(figsize=(7, 4.5))

ax.plot(ratios, mean_terminal_gaps, color="#1f77b4", linewidth=2.0, label="Mean terminal spectral gap")
ax.axvline(x=1.0, color="gray", linestyle="--", linewidth=1.5, label="Threshold mu = lambda")

# Regime annotations
ax.text(0.68, max(mean_terminal_gaps) * 0.55, "Absorbing\nregime",
        ha="center", va="center", fontsize=10, color="#d62728",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#d62728", alpha=0.8))
ax.text(1.60, max(mean_terminal_gaps) * 0.55, "Recoverable\nregime",
        ha="center", va="center", fontsize=10, color="#2ca02c",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#2ca02c", alpha=0.8))

ax.set_xlabel("mu / lambda ratio", fontsize=12)
ax.set_ylabel("Mean terminal spectral gap (t = 100)", fontsize=12)
ax.set_title("Bifurcation of Spectral Gap at mu = lambda Threshold\n"
             "(lambda = 0.1, N = 2,000 paths per ratio, seed = 42)", fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0.5, 2.0)

plt.tight_layout()

# Save to figures/ relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
figures_dir = os.path.join(script_dir, "..", "figures")
os.makedirs(figures_dir, exist_ok=True)
out_path = os.path.join(figures_dir, "figure2_bifurcation.png")
plt.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Saved: {out_path}")
