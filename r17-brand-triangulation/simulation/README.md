# R17 Monte Carlo Simulation Archive

This directory contains the simulation code and results for the Perception DOP Monte Carlo validation reported in Section 9.6 of the Brand Triangulation paper.

## Files

| File | Description |
|------|-------------|
| `R17_pdop_simulation.py` | Monte Carlo simulation: 2,000 trials, varying N and observer geometry, verifying MSE ~ sigma² × PDOP² relationship |
| `R17_pdop_simulation_results.json` | Full per-trial results (2,000 rows), including PDOP, RMSE, N, geometry type, per-dimension DOP and MSE |

## Status

**Pending upload.** The simulation was run locally; code and results need to be committed here before submission.

- TODO: Add `R17_pdop_simulation.py` (Python 3.12, numpy/scipy)
- TODO: Add `R17_pdop_simulation_results.json` (~2,000 records)

## Key Results (reported in paper)

- MSE ~ sigma² × PDOP²: slope = .968 [.945, .991], R² = .926
- log(RMSE) ~ log(PDOP): slope = .995 [.981, 1.009], R² = .994
- Spearman rho = .996 (all p < 10^{-300})
- Per-dimension Spearman range: .978 to .990

## Citation

Zharnikov, D. (2026y). Brand Triangulation: A Geometric Framework for Multi-Observer Brand Positioning. Working Paper. DOI: 10.5281/zenodo.19482547
