#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0"]
# ///
"""run_stage1.py — PRISM-M Stage 1 exploratory bank construction (2026az).

For every brand in the frozen PL2 bank x 4 artifact channels x the two
Stage-1 operator pairs (OP1, OP3): render once, extract the eight-dimension
vector + the provisional A-SCORE scalar. Writes PL3 append-only JSONL
(logs/) + parsed records (data/stage1_records.jsonl). Resumable: already-
present (brand, channel, op_pair, readout) records are skipped.

Run (keys via bws; long runs sandbox OFF):
    bws run -- research/prism_m/code/run_campaign.sh stage1
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_m_lib import (  # noqa: E402
    DATA_DIR,
    bank_brands,
    load_bank,
    load_config,
    load_records,
    measure_brand,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ops", default=None, help="comma list, e.g. OP1")
    ap.add_argument("--channels", default=None, help="comma list, e.g. official,press")
    ap.add_argument("--suffix", default="", help="output shard suffix")
    args = ap.parse_args()
    out = DATA_DIR / f"stage1_records{args.suffix}.jsonl"

    cfg = load_config()
    bank = load_bank()
    brands = bank_brands(bank)
    channels = [
        {"id": v["id"], "description": v["description"]}
        for v in cfg["artifact_channels"].values()
    ]
    if args.channels:
        keep = set(args.channels.split(","))
        channels = [c for c in channels if c["id"] in keep]
    stage1_ops = {
        op_id: op
        for op_id, op in cfg["operator_pairs"].items()
        if "stage1" in op.get("stages", [])
    }
    if args.ops:
        keep_ops = set(args.ops.split(","))
        stage1_ops = {k: v for k, v in stage1_ops.items() if k in keep_ops}
    done = set()
    for shard in DATA_DIR.glob("stage1_records*.jsonl"):
        for r in load_records(shard):
            done.add((r["brand"], r["channel"], r["op_pair"], r["readout"]))

    total = len(brands) * len(channels) * len(stage1_ops)
    i = 0
    for brand_row in brands:
        for channel in channels:
            for op_id, op in stage1_ops.items():
                i += 1
                key_dims = (brand_row["brand"], channel["id"], op_id, "dims")
                key_score = (brand_row["brand"], channel["id"], op_id, "score")
                if key_dims in done and key_score in done:
                    continue
                print(
                    f"[stage1 {i}/{total}] {brand_row['brand']} / "
                    f"{channel['id']} / {op_id}",
                    flush=True,
                )
                measure_brand(
                    brand_row,
                    channel,
                    op_id,
                    op,
                    phase="stage1",
                    readouts=("dims", "score"),
                    out_path=out,
                )
    print(f"[stage1] complete -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
