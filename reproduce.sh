#!/usr/bin/env bash
# reproduce.sh — Hub-level orchestrator for sbt-papers
#
# Iterates each paper-slug subdirectory (any directory containing paper.md
# or paper.yaml) and invokes its own reproduce.sh if present. Conforms to
# PUBLIC_MIRROR_STANDARD.md v1.0.0 at the hub-root level.
#
# Usage:
#   ./reproduce.sh                  # Iterate all paper slugs
#   ./reproduce.sh --check-only     # Verify each slug's dependency block only
#   ./reproduce.sh --fast           # Pass --fast through to per-slug scripts
#
# Outputs: hub-level run log at output/logs/hub_run.log.
# Per-paper outputs land under <paper-slug>/output/ per the per-paper standard.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

mkdir -p output/figures output/tables output/logs
LOG_FILE="output/logs/hub_run.log"

# Parse flags
CHECK_ONLY=0
FAST=0
PASS_THROUGH=()
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1; PASS_THROUGH+=("--check-only") ;;
    --fast) FAST=1; PASS_THROUGH+=("--fast") ;;
    *) echo "Unknown flag: $arg"; exit 2 ;;
  esac
done

echo "==================================================" | tee -a "$LOG_FILE"
echo "Hub run: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG_FILE"
echo "Repo: $REPO_ROOT" | tee -a "$LOG_FILE"
echo "Git SHA: $(git rev-parse HEAD 2>/dev/null || echo 'not-a-repo')" | tee -a "$LOG_FILE"
echo "Flags: check_only=$CHECK_ONLY fast=$FAST" | tee -a "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"

SLUGS_FOUND=0
SLUGS_RUN=0
SLUGS_SKIPPED=0

for slug in */; do
  slug="${slug%/}"
  # Skip hidden / non-paper directories
  case "$slug" in
    .*|output|code|templates) continue ;;
  esac
  if [[ ! -f "$slug/paper.md" && ! -f "$slug/paper.yaml" ]]; then
    continue
  fi
  SLUGS_FOUND=$((SLUGS_FOUND + 1))

  if [[ -x "$slug/reproduce.sh" ]]; then
    echo ">>> [$slug] running reproduce.sh ${PASS_THROUGH[*]:-}" | tee -a "$LOG_FILE"
    ( cd "$slug" && ./reproduce.sh "${PASS_THROUGH[@]:-}" ) 2>&1 | tee -a "$LOG_FILE" || {
      echo "!!! [$slug] reproduce.sh exited non-zero" | tee -a "$LOG_FILE"
    }
    SLUGS_RUN=$((SLUGS_RUN + 1))
  elif [[ -f "$slug/reproduce.sh" ]]; then
    echo ">>> [$slug] reproduce.sh present but not executable; skipping" | tee -a "$LOG_FILE"
    SLUGS_SKIPPED=$((SLUGS_SKIPPED + 1))
  else
    echo ">>> [$slug] no reproduce.sh; skipping (paper bundle without pipeline)" | tee -a "$LOG_FILE"
    SLUGS_SKIPPED=$((SLUGS_SKIPPED + 1))
  fi
done

echo "==================================================" | tee -a "$LOG_FILE"
echo "Hub run complete: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG_FILE"
echo "Paper slugs found: $SLUGS_FOUND  ran: $SLUGS_RUN  skipped: $SLUGS_SKIPPED" | tee -a "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"
