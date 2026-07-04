# PRISM-C companion code (2026bb)

Deterministic, seeded pipeline for the PRISM-C choice-perception-gap
instrument. Fixed seed: `SEED = 20260702` (all bootstrap resampling and
synthetic generators). Publishes under `<public-mirror>/prism-c/code/` at
submission (PAQS items 37a-37e). Shared machinery lives in
`research/prism_core/` (extracted from the frozen 2026az campaign code).

## Layout

| File | Role |
|---|---|
| `prism_c_lib.py` | Campaign library: PL1 config + bank loaders (brand bank REUSED FROZEN from `research/prism_m/PL2_BRAND_BANK.yaml`), deterministic counterbalancing scheme, choice-elicitation + need-renderer prompts (`prism-c/v1.0.0`), measurement wrappers with PL3 logging |
| `run_pilot.py` | Pre-flight operator-concordance pilot (~56 calls) + mechanical exclusion rule + PILOT GATE (exits nonzero on gate failure; confirmatory collection must not start) |
| `run_stated.py` | Stated readings (bank x 4 channels x kept op pairs) + need vectors (scenarios x kept op pairs); resumable, shardable |
| `run_choice.py` | Choice battery (scenarios x arrangements x kept chooser families) + `--controls` (positive dominating-option + negative near-duplicate sets); resumable, shardable |
| `estimator.py` | PL4: predicted picks, divergence rate vs choice operator floor + scenario-cluster bootstrap CI (H1), conditional-logit dimensional choice weights + LR test (H2), position-covariate robustness (H3), mechanism contrasts M1-M4, boundary tests B1-B2, controls, robustness (k sweep, Euclidean/Mahalanobis) |
| `synthetic.py` | Seeded synthetic generators (known CL weights, planted gap, planted controls) |
| `tests/test_prism_c_estimator.py` | 22-test unit suite run BEFORE any API spend |

## Run commands

```sh
# 0. Unit tests (no API spend; must pass before collection)
uv run pytest research/prism_c/code/tests/ -q

# 1. Pre-flight pilot + gate (keys via bws; STOP if gate fails)
bws run -- research/prism_c/code/run_campaign.sh pilot

# 2. Stated readings + need vectors (shardable by --ops/--brands/--channels)
bws run -- research/prism_c/code/run_campaign.sh stated

# 3. Choice battery + controls (shardable by --families/--scenarios)
bws run -- research/prism_c/code/run_campaign.sh choice
bws run -- research/prism_c/code/run_campaign.sh choice --controls

# 4. PL4 analysis (seeded, deterministic)
uv run python research/prism_c/code/estimator.py \
    --records research/prism_c/data/stated_records*.jsonl \
              research/prism_c/data/choice_records*.jsonl \
    --index-status research/prism_m/PL2_BRAND_BANK.yaml \
    --out research/prism_c/data/pl4_results.json --robustness
```

## Data layers

- PL3 (immutable): `../logs/*.jsonl` — one row per model API call (shared
  `llm_call_logger` schema, format v1.2).
- Parsed records: `../data/*_records*.jsonl` — one row per measurement /
  choice trial; append-only, resumable.
- Pilot report: `../data/pilot_report.json` (exclusion-rule outcome + gate).
- PL4 output: `../data/pl4_results.json`.
