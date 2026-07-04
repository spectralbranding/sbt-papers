#!/bin/sh
# PRISM-C campaign wrapper — run under `bws run --` so provider keys are
# injected (bws mangles quoted args; version-pins live here, not inline).
# Usage: bws run -- research/prism_c/code/run_campaign.sh {pilot|stated|choice} [args]
set -e
STAGE="$1"
shift || true
cd "$(dirname "$0")/../../.."
case "$STAGE" in
  pilot)  uv run --with 'httpx>=0.27' --with 'pyyaml>=6.0' --with 'numpy>=1.26' python research/prism_c/code/run_pilot.py "$@" ;;
  stated) uv run --with 'httpx>=0.27' --with 'pyyaml>=6.0' --with 'numpy>=1.26' python research/prism_c/code/run_stated.py "$@" ;;
  choice) uv run --with 'httpx>=0.27' --with 'pyyaml>=6.0' --with 'numpy>=1.26' python research/prism_c/code/run_choice.py "$@" ;;
  *) echo "usage: run_campaign.sh {pilot|stated|choice} [args]" >&2; exit 2 ;;
esac
