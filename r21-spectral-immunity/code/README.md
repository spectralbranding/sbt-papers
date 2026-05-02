# R21 Spectral Immunity — Companion Computation Script

Reproduces Tables 3-7 from:

> Zharnikov, D. (2026ac). Spectral Immunity: Why Brand Portfolio Interference
> Disappears for AI Observers. Working Paper. DOI 10.5281/zenodo.19765401

## Run command

```bash
uv run python compute_dci.py
```

Fixed random seed: 42. Python version: 3.12.

## Modes

**Stub mode** (default, no network required):
Demonstrates the DCI metric computation against the canonical SBT brand
profiles and verifies all 20 Table 3 delta DCI values.

**Full mode** (requires HuggingFace access):
Downloads the archived experiment data and reproduces all Tables 3-7.

```bash
uv run python compute_dci.py --full
```

## Data sources

- Primary experiment (7,975 observations, 20 brands):
  https://doi.org/10.57967/hf/8380
- Published-brand extension (1,950 observations, 20 brands):
  https://doi.org/10.57967/hf/8380
- Zenodo archive: https://doi.org/10.5281/zenodo.19555282

## Dependencies

Stub mode: Python 3.12 standard library only (no external packages).

Full mode:
```
pandas>=2.2
scipy>=1.13
```

Install with: `uv add pandas scipy`

## DCI formula

```
DCI = (sum_d |w_d - 1/8|) / 2 * 100
```

where `w_d` is the normalized weight on dimension `d` (raw rating / sum of ratings).
A DCI of 0 is perfectly uniform; 100 is fully concentrated on one dimension.
This is the 8-dimension L1 concentration form (Equation 2 in the paper).

## TOST

Two One-Sided Tests (Lakens 2017) with equivalence bounds ±1.0 DCI points.
The `tost()` function in `compute_dci.py` is the canonical implementation.
