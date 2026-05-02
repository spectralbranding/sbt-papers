# R17 Brand Triangulation — Companion Computation Script

This directory contains the Monte Carlo script that generates Figure 2 of
Zharnikov (2026y) "Brand Triangulation: A Geometric Framework for
Multi-Observer Brand Positioning."

## Files

| File | Description |
|------|-------------|
| `compute_pdop_rmse.py` | Monte Carlo simulation; PEP 723 inline-deps script (numpy, matplotlib) |
| `pdop_rmse.csv` | Per-trial output: `trial_id, K, geometry, PDOP, RMSE` (630 rows) |
| `figure2_pdop_rmse.png` | Log-log scatter of RMSE vs PDOP, colored by cohort count K |

## Run

```
uv run --script compute_pdop_rmse.py
```

The script is self-contained: the PEP 723 header declares numpy and matplotlib,
and `uv` resolves them automatically. Fixed seed `SEED = 42` makes results
deterministic.

## What the script does

For each cohort count `K in {9, 10, 12, 15, 20, 30, 50}` and each geometry
prior in `{clustered, random, diverse}`:

1. Draw a `K x 8` cohort weight matrix `W` from a Dirichlet on the 8-simplex.
2. Compute `PDOP(W) = sqrt(trace((W^T W)^{-1}) / K)`.
3. Sample a brand-position `x_true` uniformly from the simplex in R^8.
4. Generate `R = 200` noisy replications `y = W x_true + epsilon`,
   `epsilon ~ N(0, sigma^2 I)` with `sigma = 0.5`.
5. Recover `x_hat = (W^T W)^{-1} W^T y` for each replication.
6. Record `RMSE = sqrt(mean(||x_hat - x_true||^2))`.

The script writes 630 trials (7 K-values x 3 geometries x 30 weight-matrix
draws) to `pdop_rmse.csv` and the log-log scatter to `figure2_pdop_rmse.png`.

## Theoretical relationship

GPS theory (Kaplan & Hegarty, 2017) and the multivariate Cramér-Rao bound
(Cramér 1946, Rao 1945) predict

```
RMSE = sigma * sqrt(K) * PDOP        (PDOP normalized by sqrt(K))
```

so the log-log slope of `RMSE` versus `PDOP` at fixed K equals exactly 1.
Across all seven K values, the script recovers per-K slopes in the range
0.998-1.004 (theoretical: 1.000) and a mean
`RMSE / (sigma * sqrt(K) * PDOP)` ratio of 0.999 — confirming the
proportionality empirically. The pooled cross-K slope is biased downward
(each K has a different intercept `sigma * sqrt(K)`); per-K analysis is the
correct test.

## Citation

Zharnikov, D. (2026y). *Brand Triangulation: A Geometric Framework for
Multi-Observer Brand Positioning*. Working Paper. DOI:
[10.5281/zenodo.19482547](https://doi.org/10.5281/zenodo.19482547)
