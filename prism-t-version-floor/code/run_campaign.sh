#!/bin/sh
# PRISM-T campaign wrapper (2026ba). Wraps the runners so keys can be
# injected via `bws run -- research/prism_t/code/run_campaign.sh <job> [...]`
# (bws mangles quoted args — always route through this wrapper).
set -eu
cd "$(dirname "$0")/../../.."

JOB="$1"
shift || true

case "$JOB" in
  pilot)
    exec uv run python research/prism_t/code/run_pilot.py "$@"
    ;;
  floor|ladder|negcontrol)
    exec uv run python research/prism_t/code/run_ve1.py --job "$JOB" "$@"
    ;;
  *)
    echo "usage: run_campaign.sh {pilot|floor|ladder|negcontrol} [args]" >&2
    exit 2
    ;;
esac
