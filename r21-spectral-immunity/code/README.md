# R21 Spectral Immunity — Companion Computation Script

Checks the Table 3 deltas (stub mode) and reproduces Tables 3, 4, 5, 6 and 7
(full mode), cell by cell, from:

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
profiles and compares the Table 3 delta DCI values with the differences of the
1-decimal cell means (small discrepancies are expected from that rounding).

**Full mode** (`--full`, requires HuggingFace access or a local copy of the data):
Reads the archived records (HF DOI 10.57967/hf/8380), recomputes every printed
cell, compares it with the value hard-coded in the script, prints OK or MISMATCH
per row, and ends with an all-match line (exit code 1 on any mismatch).

```bash
uv run --with huggingface_hub --with pandas --with scipy python compute_dci.py --full
```

With the raw responses, Table 6 is checked in full:

```bash
git clone https://github.com/spectralbranding/sbt-papers
uv run --with huggingface_hub --with pandas --with scipy python compute_dci.py \
    --full --responses sbt-papers/r20-portfolio-ai/responses
```

Options: `--responses DIR` (raw response files), `--data-dir DIR` (a folder
holding the three jsonl files below, instead of downloading them).

| Table | Reproduced from | What is checked |
|-------|-----------------|-----------------|
| 3 | `main_experiment.jsonl` | all 160 cells (Solo, Port, Delta, t, p, d, TOST p, Equivalent); mean absolute delta DCI; counts of TOST-equivalent and FDR-significant brands; the L'Oreal delta range (H6); range of the 40 cell-mean standard errors |
| 4 | `main_experiment.jsonl` | nested, sequential (type I) variance shares: portfolio, brand within portfolio, model, condition, residual; brand identity (first two rows) |
| 5 | `main_experiment.jsonl` | the seven tradition rows (Delta DCI, d, p) |
| 6 | `multiturn.jsonl` (Turn 2) and the raw responses (Turn 1) | Turn-2 DCI from the HF file always; with `--responses`: Turn-1 DCI, delta, d, p, the FDR-significant set, the mean delta over the 20 brands (and its test), the 8 cell-mean standard errors |
| 7 | `published_brands.jsonl` | the 10 brands rated under both conditions (1,300 observations) on Equation 2: Solo, Port, Delta, d; counts of FDR-significant and TOST-equivalent brands; Colgate's TOST p; the Audi and Pepsi p-values; range of the 20 cell-mean standard errors |

The HF files hold Turn-2 scores only for the multi-turn arm. The Turn-1 scores
are the `turn1_scores` field of the raw response files
(`*_multiturn_*.json`), public at
https://github.com/spectralbranding/sbt-papers/tree/main/r20-portfolio-ai/responses.
Without `--responses` the script checks only what the HF files support and
says so.

Rounding: Table 3 values were transcribed from the original analysis's saved
results (means to 2 decimals, t and d to 3, p and TOST p to 4) and then rounded
half up to the printed precision; the script applies the same two steps. Tables
4, 6 and 7 are rounded once, half up, from the unrounded statistics.

## Data sources

- Primary experiment (7,975 observations, 20 brands):
  https://doi.org/10.57967/hf/8380
- Published-brand extension (1,950 observations, 20 brands; Table 7 tests the
  10 rated under both conditions, 1,300 observations):
  https://doi.org/10.57967/hf/8380
- Raw responses (Table 6 Turn-1 scores):
  https://github.com/spectralbranding/sbt-papers/tree/main/r20-portfolio-ai/responses
- Zenodo archive: https://doi.org/10.5281/zenodo.19555282

## Dependencies

Stub mode: Python 3.12 standard library only (no external packages).

Full mode:
```
pandas>=2.2
scipy>=1.13
huggingface_hub>=0.24   (not needed with --data-dir)
```

Install with: `uv add pandas scipy huggingface_hub`

## DCI formula

```
DCI = (sum_d |w_d - 1/8|) / 2 * 100
```

where `w_d` is the normalized weight on dimension `d` (raw rating / sum of ratings).
A DCI of 0 is perfectly uniform; 100 is fully concentrated on one dimension.
This is the 8-dimension L1 concentration form (Equation 2 in the paper), used
for Tables 3, 4, 5, 6 and 7.

## TOST

Two One-Sided Tests (Lakens 2017) with equivalence bounds ±1.0 DCI points.
The `tost()` function in `compute_dci.py` is the canonical implementation for
the stub demonstration; the full-mode tables use `tost_analysis5()`, which
follows the original analysis (delta and SDs rounded to 2 decimals before the
test).

## Figure 2

`plot_forest_effect_sizes.py` draws the forest plot from the Table 3 and Table 7
effect sizes typed into its data lists. After a change to either table, update
those lists and regenerate `figures/figure2_forest.png` (see the script header).
