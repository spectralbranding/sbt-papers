#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26", "scipy>=1.12", "pyyaml>=6.0"]
# ///
"""freeze_pair_bank.py — apply the frozen Stage-1 retention rule and freeze
the PRISM-M metamer-pair bank (PL2, version prism-m/v1.0.0).

Retention rule (PL0 section 6, frozen): retain a candidate pair iff
eight-dimension S/N > 2 (distinct) AND provisional scalar S/N < 1
(collapsed). Pairs in the marginal band (scalar S/N in [1, 2]) are FLAGGED,
not retained. Writes ../PAIR_BANK.yaml — locked before Stage 2.

Run:
    uv run python research/prism_m/code/freeze_pair_bank.py
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import estimator  # noqa: E402
from prism_m_lib import DATA_DIR, PRISM_M_DIR, load_records  # noqa: E402

IN = DATA_DIR / "stage1_records.jsonl"
OUT = PRISM_M_DIR / "PAIR_BANK.yaml"


def main() -> int:
    records = load_records(IN)
    idx = estimator.index_records(records)
    data = idx["data"]
    brands = sorted(data)
    op_pairs = sorted({op for b in data for ro in data[b] for op in data[b][ro]})
    rows = estimator.classify_pairs(data, brands, op_pairs, aggregators=("score",))
    retained, marginal = [], []
    for r in rows:
        if not r["resolved_full"] or r.get("snr_score") is None:
            continue
        entry = {
            "pair": list(r["pair"]),
            "snr_full_stage1": round(r["snr_full"], 3),
            "snr_scalar_stage1": round(r["snr_score"], 3),
        }
        if r["snr_score"] < 1.0:
            retained.append(entry)
        elif r["snr_score"] < 2.0:
            marginal.append(entry)
    payload = {
        "pair_bank_version": "prism-m/v1.0.0",
        "frozen_date": str(date.today()),
        "stage1_op_pairs": op_pairs,
        "retention_rule": "full S/N > 2 AND provisional scalar S/N < 1",
        "n_candidate_pairs_evaluated": len(rows),
        "n_retained": len(retained),
        "n_marginal_flagged": len(marginal),
        "retained_pairs": [{**e, "id": f"MP-{i + 1}"} for i, e in enumerate(retained)],
        "marginal_flagged_pairs": marginal,
    }
    OUT.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
    print(
        f"[freeze] {len(retained)} retained, {len(marginal)} marginal "
        f"of {len(rows)} candidates -> {OUT}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
