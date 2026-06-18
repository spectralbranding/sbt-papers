#!/usr/bin/env bash
# Reproduce: download raw data from HuggingFace into experiment/L3_sessions/,
# then run the L4_analysis scripts. Requires: pip install huggingface_hub
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p experiment/L3_sessions experiment/L4_analysis
echo 'Downloading raw datasets from HuggingFace...'
huggingface-cli download spectralbranding/exp-agentic-collapse --repo-type dataset --local-dir experiment/_hf/exp-agentic-collapse  # DOI 10.57967/hf/8437
huggingface-cli download spectralbranding/exp-compounding-format --repo-type dataset --local-dir experiment/_hf/exp-compounding-format  # DOI 10.57967/hf/8438
huggingface-cli download spectralbranding/exp-cross-language --repo-type dataset --local-dir experiment/_hf/exp-cross-language  # DOI 10.57967/hf/8439
huggingface-cli download spectralbranding/exp-primacy-generalization --repo-type dataset --local-dir experiment/_hf/exp-primacy-generalization  # DOI 10.57967/hf/8436
huggingface-cli download spectralbranding/r15-ai-search-metamerism --repo-type dataset --local-dir experiment/_hf/r15-ai-search-metamerism  # DOI 10.57967/hf/8284
huggingface-cli download spectralbranding/r15-synthetic-cohorts --repo-type dataset --local-dir experiment/_hf/r15-synthetic-cohorts  # DOI 10.57967/hf/8441
echo 'Done. Raw logs are under experiment/_hf/<dataset>/data/.'
echo 'See DATA_MANIFEST.yaml hf_archive: for the file -> dataset map.'
