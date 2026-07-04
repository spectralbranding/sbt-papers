#!/bin/sh
# PRISM-O campaign wrapper — run under `bws run --` so provider keys are
# injected (bws mangles quoted args; version-pins live here, not inline).
# Usage: bws run -- research/prism_o/code/run_campaign.sh {stage1|score1} [...]
set -e
STAGE="$1"
shift || true
cd "$(dirname "$0")/../../.."
case "$STAGE" in
  stage1) uv run --with 'httpx>=0.27' --with 'pyyaml>=6.0' --with 'numpy>=1.26' python research/prism_o/code/run_stage1.py "$@" ;;
  score1) uv run --with 'pyyaml>=6.0' python research/prism_o/code/score_stage1.py "$@" ;;
  collect) uv run --with 'httpx>=0.27' --with 'pyyaml>=6.0' python research/prism_o/code/collect_stage2.py "$@" ;;
  stage2) uv run --with 'httpx>=0.27' --with 'pyyaml>=6.0' python research/prism_o/code/run_stage2.py "$@" ;;
  estimate2) uv run --with 'pyyaml>=6.0' --with 'numpy>=1.26' --with 'scipy>=1.12' python research/prism_o/code/estimator_stage2.py "$@" ;;
  rc1) uv run --with 'httpx>=0.27' --with 'pyyaml>=6.0' python research/prism_o/code/rerun_rc1.py "$@" ;;
  posthoc) uv run --with 'pyyaml>=6.0' --with 'numpy>=1.26' --with 'scipy>=1.12' python research/prism_o/code/analyze_posthoc.py "$@" ;;
  *) echo "usage: run_campaign.sh {stage1|score1|collect|stage2|estimate2}" >&2; exit 2 ;;
esac
