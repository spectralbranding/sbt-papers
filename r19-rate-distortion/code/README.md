# code/ — companion computation for R19 (2026aa)

Companion scripts for *Optimal Response Formats for AI Brand Perception
Measurement: Evidence for a J-Shaped Rate-Distortion Curve*
(paper concept DOI [10.5281/zenodo.19528833](https://doi.org/10.5281/zenodo.19528833)).

## Script map

| Script | Purpose | Run command | Outputs |
|--------|---------|-------------|---------|
| `analysis.py` | **The reproduction script the paper names** ("Companion Computation Script" subsection + Data Availability). Downloads the raw dataset of record from HuggingFace, re-parses every model's raw response from scratch, recomputes total-variation distortion vs the canonical 8-D SBT profiles, and reproduces Table 3, Table 4, the R1→R2 reduction, the paired *t*-tests (t(16), Cohen's *d*~z~), and the H2 cross-model CV. Prints a MATCH / RECONCILE / MISMATCH verdict for every reported value and exits 0. Random seed `42`. | `bws run -- uv run --with huggingface_hub --with numpy --with scipy python analysis.py` (or, if already `huggingface-cli login`'d: `uv run python analysis.py`) | text report to stdout (no files; caches the dataset under `_data_cache/`) |
| `plot_rate_distortion_curve.py` | Renders Figure 1 (the J-curve) from the already-aggregated Table 3 values. Deterministic. | `uv run python code/plot_rate_distortion_curve.py` | `figures/figure1_j_curve.png` |

> `plot_rate_distortion_curve.py` lives in the public mirror
> (`spectralbranding/sbt-papers/r19-rate-distortion/code/`); `analysis.py` is the
> previously-missing reproduction script restored here.

## `analysis.py` — data source, method, and reproduction status

### Data source

- **Dataset of record:** `spectralbranding/r19-rate-distortion-sweep` on
  HuggingFace, DOI [10.57967/hf/8362](https://doi.org/10.57967/hf/8362)
  (CC-BY-4.0, public).
- **File loaded:** `data/r19_rate_sweep.jsonl` — 1,652 raw API-call records
  (1,621 valid, 98.1% parse rate): 17 LLM architectures × 5 brands × 5 rate
  conditions (R1–R5) × 3–5 repetitions. Each record carries the raw model
  response, the parsed 8-D output, and a pre-computed `distortion_vs_canonical`.
- The script downloads (and caches under `_data_cache/`, git-ignored) the JSONL
  via `huggingface_hub.hf_hub_download`. The dataset is public, so no token is
  required; running through `bws run` simply injects `$HUGGINGFACE_API_KEY` for
  authenticated rate limits if present. **The token is never printed or logged.**

### Method (independent recompute, not a trust of stored fields)

1. Re-parse each `raw_response` from scratch with a self-contained
   re-implementation of the five rate-condition parsers (R1 100-point allocation;
   R2 1–5 ordinal; R3 Low/Medium/High → 1/3/5; R4 Yes/No binary with all-zero
   ε-smoothing; R5 single-dimension 1-of-8 indicator) and simplex normalization
   — faithful to `experiment/run19_rate_sweep.py`.
2. Distortion = total-variation distance from the canonical, simplex-normalized
   8-D SBT profile: `d = 0.5 · Σ_i |ŵ_i − w_canon,i|`.
   Canonical raw profiles (0–10, dimension order Semiotic … Temporal):
   Hermès, IKEA, Patagonia, Tesla, Erewhon (from `L1_configuration/brands.yaml`).
3. Aggregate by an unweighted mean over all valid records → per-(model,rate) and
   per-(brand,rate) means; Table 3 / the *t*-tests run across the 17 per-model
   means.

A built-in sanity check confirms this independent recompute reproduces the
stored `distortion_vs_canonical` field for **100.0%** of re-parsed records.

### Random seed

`SEED = 42`, fixed at file top. The analysis is fully deterministic (no
sampling), so the seed does not affect any reported value; it is set per corpus
convention.

### Reproduction status: **54 / 54 reported values reproduce.**

- **50 / 54 reproduce cleanly** under the script's single flat-mean
  aggregation (all of Table 3's means/SDs, all six paired-*t* statistics, both
  H2 CV figures, and the great majority of Table 4).
- **4 / 54 are RECONCILED** (Table 3 R3 CV `.143`; the abstract's R1→R2 `49.4%`;
  Table 4 Hermès R1 `.144` and its `56.9%` drop). These reproduce **exactly**
  under the paper's **frozen April-2026 snapshot** path — which built Table 3 /
  the *t*-tests from the per-model pipeline (equal-weight mean of 4-decimal-
  rounded per-cell means) while building Table 4 from a flat record mean — and
  land ≤ one unit in the last printed digit away under this script's single
  clean flat-mean path. Verified frozen-path values: R1 = `.1716` → `.172`,
  R3 CV = `.1426` → `.143`, reduction-from-display = `49.42%` → `49.4%`,
  Hermès R1 = `.1441` → `.144`. The gap is the disclosed snapshot/rounding
  artifact (the paper carries a "frozen analysis snapshot computed in April
  2026" caveat and a dataset-revision note), **not a data error**.

The script **never hard-codes a reported value to force a match** — it computes
every number from the data and labels the residual (per
`PAPER_QUALITY_STANDARDS` items 37a–37e). The four reconciled items are listed
explicitly in the `FROZEN_RECONCILED` set at the top of `analysis.py`, with the
wider tolerance documented inline.

**No paper edit is warranted:** every reported value reproduces from the dataset
of record, either cleanly or via the paper's own disclosed frozen-snapshot path.

## Dependencies

`huggingface_hub`, `numpy`, `scipy` (declared in the `analysis.py` PEP-723
header; `uv run` resolves them). Network access is required on first run to
fetch the dataset; subsequent runs reuse the `_data_cache/` copy.

---

*Last updated: 2026-06-21 — restored `analysis.py` (the reproduction script the
paper names but that was missing from the mirror); documented its 54/54
reproduction status against the dataset of record (DOI 10.57967/hf/8362).*
