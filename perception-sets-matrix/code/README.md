# Companion code — 2026bf (Perception Sets the Matrix)

Deterministic, seeded pipeline for the pre-registered match-propensity
campaign. Fixed seed everywhere: `SEED = 20260712`. Frozen layer checksums:
`../FREEZE_RECORD.md`. Single-command reproduction: `../reproduce.sh`
(analysis-only from committed records; `--collect` re-runs collection —
new epoch, keys via `bws run --`).

## Layout

| File | Role |
|---|---|
| `gen_design.py` | Seeded design generator: 30 cohort personas (maximin LHS profiles + Dirichlet salience weights + phrase-bank NL renderings, no numbers in text) + Study-1 match-coverage diagnostic |
| `psm_lib.py` | Shared core: frozen prompt set (`psm/1.0.0`), 4-family provider layer (raw HTTP), parsers, append-only JSONL call logging via the shared `llm_call_logger` |
| `run_campaign.py` | Resumable collection: smoke / validate (stimulus gate) / cohorts / readings / eliciting / samecall arms; per-operator record shards |
| `estimator.py` | Frozen analysis: floors F1-F4; Kendall tau_b + within-cohort permutation null (shared permutations, pooled median); isotonic R^2; same-call delta-tau; fluency auxiliary delta-tau_w (paired swap permutation); induced Dirichlet matrix (S, s) + double-jeopardy ordering vs switching probes; band mass vs cohort dispersion; frozen robustness list; kill-condition verdicts K1-K4. `--gate` runs the stimulus-validation gate |
| `power_simulation.py` | Sample-size simulation (source of the Method power numbers) |
| `tests/test_psm_estimator.py` | Unit suite run BEFORE any API spend: planted-positive, null, and weighted-planted controls + kernel/parser tests |

## Run commands

```sh
# 0. Unit suite (no API spend; must pass before collection)
cd code && uv run --with pytest --with numpy --with pyyaml --with httpx python -m pytest tests/ -q

# 1. Smoke (one call per operator)
bws run -- <wrapper.sh: uv run --with httpx --with pyyaml python run_campaign.py --arm smoke>

# 2. Stimulus-validation gate (validation operators; BEFORE the propensity arm)
bws run -- <wrapper: ... run_campaign.py --arm validate --ops OP1,OP3>
uv run --with numpy --with pyyaml python estimator.py --gate

# 3. Full campaign (per-operator shards, resumable)
bws run -- <wrapper: ... run_campaign.py --arm all --ops OP1>   # x OP1..OP6

# 4. Frozen analysis (seeded, deterministic)
uv run --with numpy --with pyyaml python estimator.py \
    --records '../data/records_*.jsonl' --out ../data/results.json
```

## Data layers

- `../logs/*.jsonl` — immutable call log, one record per model API call
  (shared llm_call_logger schema); published as the HF dataset at
  publication.
- `../data/records_*.jsonl` — parsed measurement records (append-only,
  resumable; record_key dedup).
- `../data/results.json` — frozen-estimator output; the paper's Results
  section is filled verbatim from it.

## Power simulation

See `power_simulation.py` docstring; outputs (1,000 sims x 1,000 perms,
alpha = .05): Study 1 power .952 (tau .30) / .702 (tau .20) per operator,
.980 pooled over 4 operators; Study 2 .910 / .952. These are the Method
sample-size numbers.
