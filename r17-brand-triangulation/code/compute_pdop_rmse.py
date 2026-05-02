#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Compute PDOP-vs-RMSE for the Brand Triangulation Monte Carlo demonstration.

Generates the data behind Figure 2 of Zharnikov (2026y) "Brand Triangulation":
for a range of cohort weight matrices W in R^{K x 8}, the script computes

    PDOP(W) = sqrt(trace((W^T W)^{-1}) / K)         (geometric quality)
    RMSE(W) = sqrt(mean(||x_hat - x_true||^2))      (Monte Carlo estimator)

The brand position x_true is sampled uniformly from the open simplex in R^8,
and each cohort observes y = W x_true + epsilon with epsilon ~ N(0, sigma^2 I).
The OLS estimator x_hat = (W^T W)^{-1} W^T y is recovered from R = 200 noisy
replications per (W, x_true) trial.

Run:
    uv run python compute_pdop_rmse.py

Outputs (written next to the script):
    pdop_rmse.csv          — per-trial {trial_id, K, PDOP, RMSE}
    figure2_pdop_rmse.png  — log-log scatter of RMSE vs PDOP

Reproducibility: SEED = 42; deterministic across the supported numpy versions.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SEED = 42
D = 8                         # SBT spectral dimensions
SIGMA = 0.5                   # per-cohort observation noise std
N_REPLICATIONS = 200          # MC replications per trial
K_VALUES = (9, 10, 12, 15, 20, 30, 50)  # cohort counts
TRIALS_PER_K = 30             # weight-matrix draws per K
GEOMETRIES = ("clustered", "random", "diverse")  # weight-matrix priors


def sample_simplex(rng: np.random.Generator, n_rows: int) -> np.ndarray:
    """Draw n_rows points uniformly from the open (D-1)-simplex via Dirichlet(1)."""
    return rng.dirichlet(alpha=np.ones(D), size=n_rows)


def make_weight_matrix(rng: np.random.Generator, K: int, geometry: str) -> np.ndarray:
    """Construct a K x D cohort weight matrix with controlled geometric diversity.

    - clustered: all cohorts cluster around one corner of the simplex (high PDOP)
    - random:    iid Dirichlet(1) draws across cohorts
    - diverse:   Dirichlet(.3) — peaky weights — yields well-spread profiles (low PDOP)
    """
    if geometry == "clustered":
        center = rng.dirichlet(np.ones(D))
        jitter = rng.normal(scale=0.02, size=(K, D))
        W = np.maximum(center[None, :] + jitter, 1e-4)
        W /= W.sum(axis=1, keepdims=True)
    elif geometry == "random":
        W = rng.dirichlet(np.ones(D), size=K)
    elif geometry == "diverse":
        W = rng.dirichlet(0.3 * np.ones(D), size=K)
    else:
        raise ValueError(f"unknown geometry: {geometry}")
    return W


def pdop(W: np.ndarray) -> float:
    """Per-cohort-normalized PDOP: sqrt(trace((W^T W)^{-1}) / K)."""
    K = W.shape[0]
    gram = W.T @ W
    try:
        cov = np.linalg.inv(gram)
    except np.linalg.LinAlgError:
        return float("inf")
    return float(np.sqrt(np.trace(cov) / K))


def rmse_via_monte_carlo(
    rng: np.random.Generator,
    W: np.ndarray,
    x_true: np.ndarray,
    sigma: float,
    n_replications: int,
) -> float:
    """Compute RMSE of OLS x_hat over n_replications noisy observation sets."""
    K = W.shape[0]
    gram_inv = np.linalg.inv(W.T @ W)
    mean_clean = W @ x_true
    sq_errors = np.empty(n_replications)
    for r in range(n_replications):
        noise = rng.normal(scale=sigma, size=K)
        y = mean_clean + noise
        x_hat = gram_inv @ (W.T @ y)
        sq_errors[r] = np.sum((x_hat - x_true) ** 2)
    return float(np.sqrt(np.mean(sq_errors)))


def run() -> tuple[list[dict], Path, Path]:
    rng = np.random.default_rng(SEED)
    rows: list[dict] = []
    trial_id = 0
    for K in K_VALUES:
        for geometry in GEOMETRIES:
            for _ in range(TRIALS_PER_K):
                W = make_weight_matrix(rng, K, geometry)
                p = pdop(W)
                if not np.isfinite(p):
                    continue
                x_true = sample_simplex(rng, 1)[0]
                rmse = rmse_via_monte_carlo(rng, W, x_true, SIGMA, N_REPLICATIONS)
                rows.append(
                    {
                        "trial_id": trial_id,
                        "K": K,
                        "geometry": geometry,
                        "PDOP": p,
                        "RMSE": rmse,
                    }
                )
                trial_id += 1
    here = Path(__file__).resolve().parent
    csv_path = here / "pdop_rmse.csv"
    png_path = here / "figure2_pdop_rmse.png"
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["trial_id", "K", "geometry", "PDOP", "RMSE"])
        writer.writeheader()
        writer.writerows(rows)
    plot_log_log(rows, png_path)
    return rows, csv_path, png_path


def plot_log_log(rows: list[dict], png_path: Path) -> None:
    pdops = np.array([r["PDOP"] for r in rows])
    rmses = np.array([r["RMSE"] for r in rows])
    Ks = np.array([r["K"] for r in rows])

    fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=150)
    cmap = plt.colormaps.get_cmap("viridis")
    unique_K = sorted(set(Ks.tolist()))
    per_k_slopes = []
    for i, K in enumerate(unique_K):
        mask = Ks == K
        color = cmap((i + 0.5) / len(unique_K))
        ax.scatter(
            pdops[mask],
            rmses[mask],
            s=14,
            alpha=0.65,
            color=color,
            edgecolor="none",
        )
        # Per-K log-log fit (theoretical slope = 1 since RMSE = sigma * sqrt(K) * PDOP)
        slope_k, intercept_k = np.polyfit(np.log(pdops[mask]), np.log(rmses[mask]), 1)
        per_k_slopes.append(slope_k)
        x_fit = np.linspace(np.log(pdops[mask].min()), np.log(pdops[mask].max()), 50)
        ax.plot(np.exp(x_fit), np.exp(slope_k * x_fit + intercept_k), color=color, lw=1.0,
                label=f"K = {K}  (slope = {slope_k:.3f})")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("PDOP (log scale)")
    ax.set_ylabel("RMSE (log scale)")
    median_slope = float(np.median(per_k_slopes))
    ax.set_title(
        f"Figure 2: PDOP vs RMSE (Monte Carlo; R = {N_REPLICATIONS} per trial; "
        f"median per-K slope = {median_slope:.3f})"
    )
    ax.grid(True, which="both", ls=":", lw=0.4, alpha=0.6)
    ax.legend(loc="best", fontsize=7, frameon=True, ncol=2)
    fig.tight_layout()
    fig.savefig(png_path)
    plt.close(fig)


if __name__ == "__main__":
    rows, csv_path, png_path = run()
    pdops = np.array([r["PDOP"] for r in rows])
    rmses = np.array([r["RMSE"] for r in rows])
    Ks = np.array([r["K"] for r in rows])

    # Per-K slopes — the theoretical relationship is RMSE = sigma * sqrt(K) * PDOP,
    # so the log-log slope at fixed K equals 1 exactly. The pooled slope across K
    # values is biased because each K has a different intercept (sigma * sqrt(K)).
    print(f"trials               : {len(rows)}")
    print(f"PDOP range           : {pdops.min():.3f} .. {pdops.max():.3f}")
    print(f"RMSE range           : {rmses.min():.3f} .. {rmses.max():.3f}")
    print("per-K log-log slope (theory: 1.000):")
    for K in sorted(set(Ks.tolist())):
        m = Ks == K
        s, _ = np.polyfit(np.log(pdops[m]), np.log(rmses[m]), 1)
        print(f"   K = {K:3d}  n = {m.sum():3d}  slope = {s:.4f}")
    ratios = rmses / (SIGMA * np.sqrt(Ks) * pdops)
    print(f"RMSE / (sigma sqrt(K) PDOP) : mean = {ratios.mean():.4f}  median = {np.median(ratios):.4f}  (theory: 1.0)")
    print(f"wrote                : {csv_path}")
    print(f"wrote                : {png_path}")
