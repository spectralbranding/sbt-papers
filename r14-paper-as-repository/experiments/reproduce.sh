#!/usr/bin/env bash
# Reproduce the three federated ontology-negotiation experiments backing the
# paper's Section 5.6. Deterministic: term identity is a content-addressed hash
# of the definition text and the classifier is a pure function of the two parsed
# module sets, so each report + emitted SSSOM reproduces byte-for-byte at a fixed
# tool version, with no random seed, no network, and no credentials.
#
# Run from this experiments/ directory:
#   bash reproduce.sh
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$PWD/tools:${PYTHONPATH:-}"
# Prefer `uv` (fetches PyYAML with zero setup); else python3/python with PyYAML
# already installed (see README).
if command -v uv >/dev/null 2>&1; then PY="uv run --with pyyaml python"
elif command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
else echo "No uv/python3/python found" >&2; exit 1; fi
NEG="$PY tools/negotiate_modules.py"

echo "== negotiation-sbt-ost (clean federation) =="
$NEG --author-a negotiation-sbt-ost/sbt --author-b negotiation-sbt-ost/ost \
     --sssom negotiation-sbt-ost/sbt_ost.sssom.tsv

echo ""
echo "== negotiation-aaker (dangling reference) =="
$NEG --author-a negotiation-sbt-ost/sbt --author-b negotiation-aaker/aaker \
     --sssom negotiation-aaker/sbt_aaker.sssom.tsv

echo ""
echo "== negotiation-spence (definitional conflict) =="
$NEG --author-a negotiation-spence/sbt --author-b negotiation-spence/spence \
     --sssom negotiation-spence/sbt_spence.sssom.tsv

echo ""
echo "Append --gate to any run for the federated CI verdict (nonzero on the two"
echo "adversarial runs is the intended behavior). The curated cross-key mapping for"
echo "the Aaker run is negotiation-aaker/sbt_aaker_crosskey_curated.sssom.tsv."
