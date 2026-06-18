#!/usr/bin/env bash
# Reproduce: download raw data from HuggingFace into experiment/L3_sessions/,
# then run the L4_analysis scripts. Requires: pip install huggingface_hub
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p experiment/L3_sessions experiment/L4_analysis
echo 'Downloading raw datasets from HuggingFace...'
huggingface-cli download spectralbranding/r19-rate-distortion-sweep --repo-type dataset --local-dir experiment/_hf/r19-rate-distortion-sweep  # DOI 10.57967/hf/8362
echo 'Done. Raw logs are under experiment/_hf/<dataset>/data/.'
echo 'See DATA_MANIFEST.yaml hf_archive: for the file -> dataset map.'
