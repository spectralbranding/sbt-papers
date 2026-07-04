#!/bin/sh
# PRISM-M campaign wrapper — run under `bws run --` so provider keys are
# injected (bws mangles quoted args; version-pins live here, not inline).
# Usage: bws run -- research/prism_m/code/run_campaign.sh {stage1|stage2} [--ablation]
set -e
STAGE="$1"
shift || true
cd "$(dirname "$0")/../../.."
case "$STAGE" in
  stage1) uv run --with 'httpx>=0.27' --with 'pyyaml>=6.0' python research/prism_m/code/run_stage1.py "$@" ;;
  stage2) uv run --with 'httpx>=0.27' --with 'pyyaml>=6.0' python research/prism_m/code/run_stage2.py "$@" ;;
  *) echo "usage: run_campaign.sh {stage1|stage2} [--ablation]" >&2; exit 2 ;;
esac
