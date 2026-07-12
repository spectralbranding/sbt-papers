#!/bin/bash
# reproduce.sh — 2026bf (Perception Sets the Matrix) pipeline orchestrator.
#
# Reproduces every reported number from the committed inputs:
#   analysis-only (default): re-runs the seeded estimator + power simulation
#     on the committed parsed records — no API calls, no keys needed.
#   --collect: additionally re-runs the collection campaign (requires
#     ANTHROPIC_API_KEY / OPENAI_API_KEY / DEEPSEEK_API_KEY, e.g. via
#     `bws run -- ./reproduce.sh --collect`; model behavior is epoch-pinned,
#     so re-collection yields a new epoch, not a byte-identical replication).
#
# Deterministic: all analysis stages run under fixed seed 20260712.
set -euo pipefail
cd "$(dirname "$0")"

echo "== deps check =="
command -v uv >/dev/null || { echo "uv required"; exit 1; }

mkdir -p output/figures output/tables output/logs data logs
LOG=output/logs/master_run.log
: > "$LOG"

echo "== unit suite (must pass before anything) ==" | tee -a "$LOG"
(cd code && uv run --with pytest --with numpy --with pyyaml --with httpx \
    python -m pytest tests/ -q) 2>&1 | tee -a "$LOG"

echo "== design artifacts (seeded; byte-identical regeneration) ==" | tee -a "$LOG"
uv run --with scipy --with pyyaml --with numpy python code/gen_design.py 2>&1 | tee -a "$LOG"

if [[ "${1:-}" == "--collect" ]]; then
    echo "== collection: smoke ==" | tee -a "$LOG"
    (cd code && uv run --with httpx --with pyyaml python run_campaign.py --arm smoke) 2>&1 | tee -a "$LOG"
    echo "== collection: stimulus-validation gate ==" | tee -a "$LOG"
    (cd code && uv run --with httpx --with pyyaml python run_campaign.py --arm validate) 2>&1 | tee -a "$LOG"
    uv run --with numpy --with pyyaml python code/estimator.py --gate 2>&1 | tee -a "$LOG"
    echo "== collection: full campaign (per-operator shards) ==" | tee -a "$LOG"
    for OP in OP1 OP2 OP3 OP4 OP5 OP6; do
        (cd code && uv run --with httpx --with pyyaml python run_campaign.py --arm all --ops "$OP") 2>&1 | tee -a "$LOG" &
    done
    wait
fi

echo "== power simulation ==" | tee -a "$LOG"
uv run --with numpy --with scipy python code/power_simulation.py 2>&1 | tee -a "$LOG" | tee output/tables/power_simulation.txt

echo "== seeded estimator ==" | tee -a "$LOG"
uv run --with numpy --with pyyaml python code/estimator.py \
    --records 'data/records_*.jsonl' --out data/results.json 2>&1 | tee -a "$LOG"
cp data/results.json output/tables/results.json

echo "== done ==" | tee -a "$LOG"
