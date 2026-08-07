#!/usr/bin/env bash
# Reproduce: download raw data from HuggingFace into experiment/_hf/,
# then run the L4_analysis scripts.
#
# Dependencies: uv only. The HuggingFace client is resolved per-run by
# `uv run --with huggingface_hub`, so nothing has to be installed globally
# first -- this stays a one-command reproduction from a clean machine.
#
# Public datasets: no token needed. If you are rate-limited, `HF_TOKEN` is
# honoured from the environment.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p experiment/L3_sessions experiment/L4_analysis experiment/_hf

command -v uv >/dev/null || {
  echo "ERROR: 'uv' is required and was not found on PATH." >&2
  echo "Install it from https://docs.astral.sh/uv/ and re-run." >&2
  exit 1
}

# repo_id  local_dir  DOI
DATASETS=(
  "spectralbranding/r19-rate-distortion-sweep   r19-rate-distortion-sweep   10.57967/hf/8362"
)

echo 'Downloading raw datasets from HuggingFace...'
for entry in "${DATASETS[@]}"; do
  read -r repo_id local_name doi <<<"$entry"
  echo "  $repo_id  (DOI $doi)"
  uv run --with huggingface_hub python - "$repo_id" "experiment/_hf/$local_name" <<'PY'
import sys

from huggingface_hub import snapshot_download

repo_id, local_dir = sys.argv[1], sys.argv[2]
path = snapshot_download(repo_id=repo_id, repo_type="dataset", local_dir=local_dir)
print("    downloaded to", path)
PY
done

echo 'Done. Raw logs are under experiment/_hf/<dataset>/data/.'
echo 'See DATA_MANIFEST.yaml hf_archive: for the file -> dataset map.'
