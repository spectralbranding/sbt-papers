# PRISM-M companion code (2026az)

Deterministic, seeded pipeline for the PRISM-M metamerism instrument.
Fixed seed: `SEED = 20260702` (all bootstrap resampling and synthetic
generators). Publishes under `<public-mirror>/prism-m/code/` at submission
(PAQS items 37a-37e).

## Layout

| File | Role |
|---|---|
| `prism_m_lib.py` | Shared core: PL1 config + PL2 bank loaders, PL2 prompt set (`prism-m/v1.0.0`), 4-family provider layer (raw HTTP), PL3 JSONL logging via the shared LLM-call logger |
| `run_stage1.py` | Stage 1 exploratory collection (bank x 4 channels x OP1+OP3; dims + provisional A-SCORE) |
| `freeze_pair_bank.py` | Applies the frozen retention rule (full S/N > 2 AND scalar S/N < 1) and freezes `../PAIR_BANK.yaml` |
| `run_stage2.py` | Stage 2 confirmatory collection (frozen-pair brands x 4 channels x OP1-OP4; dims + A-SCORE + A-RANK + A-PICK); `--ablation` collects the prompt-ablation subsample |
| `estimator.py` | PL4 estimator: distances, operator/artifact floors, metameric fractions, source-cluster bootstrap CIs, H1/H2/H3 tests, controls, robustness (k sweep, Euclidean + Mahalanobis) |
| `synthetic.py` | Seeded synthetic generators (planted positive control + test bank) |
| `tests/test_prism_m_estimator.py` | Unit suite run BEFORE any API spend |

## Run commands

```sh
# 0. Unit tests (no API spend; must pass before collection)
uv run pytest research/prism_m/code/tests/ -q

# 1. Stage 1 (keys via bws; shardable)
bws run -- research/prism_m/code/run_campaign.sh stage1
#    parallel shards: --ops OP1 --channels official,press --suffix _s1a  etc.
#    then: cat data/stage1_records_*.jsonl > data/stage1_records.jsonl

# 2. Freeze the metamer-pair bank (PL2 lock before Stage 2)
uv run python research/prism_m/code/freeze_pair_bank.py

# 3. Stage 2 confirmatory + ablation subsample
bws run -- research/prism_m/code/run_campaign.sh stage2
bws run -- research/prism_m/code/run_campaign.sh stage2 --ablation

# 4. PL4 analysis (seeded, deterministic)
uv run python research/prism_m/code/estimator.py \
    --stage2 research/prism_m/data/stage2_records.jsonl \
    --out research/prism_m/data/pl4_results.json --robustness
```

## Data layers

- PL3 (immutable): `../logs/*.jsonl` — one row per model API call
  (full schema per the shared `llm_call_logger`, format v1.2).
- Parsed records: `../data/*_records.jsonl` — one row per
  (brand, channel, op_pair, readout); append-only, resumable.
- PL4 output: `../data/pl4_results.json`.
