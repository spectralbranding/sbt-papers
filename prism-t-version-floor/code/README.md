# PRISM-T companion code (2026ba)

Deterministic, seeded pipeline for the PRISM-T version-floor instrument.
Fixed seed: `SEED = 20260702` (all bootstrap resampling, synthetic
generators, and the power analysis). Publishes under
`<public-mirror>/prism-t/code/` at submission (PAQS items 37a-37e).
Shared machinery imported from `research/prism_core/` (provider layer,
PRISM-B extractor, floors/bootstrap stats, concordance + exclusion rule).

## Layout

| File | Role |
|---|---|
| `prism_t_lib.py` | PL1 config + frozen bank + pinned-panel loaders (manifest SHA-256 verified on every artifact read), the PL2 prompt set (`prism-t/v1.0.0`: artifact-READING renderer + verbatim PRISM-B extractor), measurement step |
| `run_pilot.py` | Pre-flight operator-concordance pilot (~38 calls): 4-OP leave-one-out screen + mechanical 3x-median exclusion + ladder-rung availability |
| `run_ve1.py` | Epoch VE-1 capture: `--job floor` (4 contemporaneous OPs), `--job ladder` (non-top rungs; top rungs shared with OP1-OP3), `--job negcontrol` (same-version run 2) |
| `estimator.py` | PL4: per-brand operator floor, per-ladder version floor, H1 S/N + brand-cluster bootstrap CI, H3 two-set contrast, H2 live/pinned decomposition (VE-2+), controls, robustness (k sweep, Euclidean + Mahalanobis) |
| `power_analysis.py` | Simulation-based power analysis (runs the REAL estimator on synthetic records; anchors: 2026ax floors .0034-.057, H13 < .03) |
| `synthetic.py` | Seeded synthetic generators in the exact record schema |
| `tests/test_prism_t_estimator.py` | Unit suite run BEFORE any API spend |

## Run commands

```sh
# 0. Unit tests (no API spend; must pass before collection)
uv run pytest research/prism_t/code/tests/ -q

# 0a. Power analysis (no API spend; publishes with the paper)
uv run python research/prism_t/code/power_analysis.py \
    --out research/prism_t/data/power_analysis.json

# 1. Pre-flight pilot (keys via bws; ~38 calls) -> exclusion verdict
bws run -- research/prism_t/code/run_campaign.sh pilot

# 2. VE-1 capture (freeze PL1 first; shardable via --ops/--ladders/--brands i:j/--suffix)
bws run -- research/prism_t/code/run_campaign.sh floor
bws run -- research/prism_t/code/run_campaign.sh ladder
bws run -- research/prism_t/code/run_campaign.sh negcontrol
#    merge shards: cat data/ve1_records_*.jsonl >> data/ve1_records.jsonl

# 3. PL4 analysis (seeded, deterministic; --excluded-ops from the pilot verdict)
uv run python research/prism_t/code/estimator.py \
    --records research/prism_t/data/ve1_records.jsonl \
    --out research/prism_t/data/pl4_results.json \
    --excluded-ops OP4 --robustness
```

## Data layers

- Pinned panel (immutable): `../panel/pinned/<brand-slug>/<channel>.txt`
  + `../panel/PINNED_MANIFEST.json` (URL, retrieval time, chars, SHA-256;
  every artifact read is hash-verified — a mismatch aborts the run).
- PL3 (immutable): `../logs/*.jsonl` — one row per model API call
  (shared `llm_call_logger`, format v1.2).
- Parsed records: `../data/*_records.jsonl` — one row per
  (panel, brand, channel, renderer, extractor, run); append-only, resumable.
- PL4 output: `../data/pl4_results.json`; power: `../data/power_analysis.json`.

## Version-identity discipline

Rungs are pinned to exact model IDs verified live on the collection date;
there is NO fallback substitution (a version ladder with a silently swapped
rung measures nothing) — an unavailable rung is dropped and reported.
