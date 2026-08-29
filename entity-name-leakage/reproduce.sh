#!/usr/bin/env bash
# Re-derive every computed value this paper reports.
#
# The records are not in this repository. They are the dataset of record, at
# https://huggingface.co/datasets/spectralbranding/entity-name-leakage, and this
# script takes the downloaded collection as its one argument:
#
#     hf download spectralbranding/entity-name-leakage \
#         --repo-type dataset --local-dir enl-data
#     ./reproduce.sh enl-data/second_collection
#
# Needs `uv` and nothing else: each script pins its own dependencies inline.
# Writes output/tables/. Deterministic -- run it twice and diff.
set -euo pipefail
cd "$(dirname "$0")"

DATA="${1:-${ENL_DATA_ROOT:-}}"
if [ -z "$DATA" ]; then
    echo "usage: ./reproduce.sh <collection-dir>   (or set \$ENL_DATA_ROOT)" >&2
    echo "the collection dir is the one holding data/ and PROTOCOL.yaml" >&2
    exit 2
fi

echo "== Table 4: guard interaction against the within-cell residual =="
uv run code/estimate_guard_ratio.py --data-root "$DATA"

echo "== Table 3: per-dimension movement under a name exchange =="
uv run code/per_dimension_leakage.py --data-root "$DATA"

echo "== Table 5: equivalence bounds by text count =="
uv run code/equivalence_power.py

echo "== guard reproducibility, discussed but not tabled =="
uv run code/simulate_guard_power.py

echo
echo "Done. Tables in output/tables/."
