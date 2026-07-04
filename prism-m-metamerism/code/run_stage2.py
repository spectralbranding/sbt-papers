#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0"]
# ///
"""run_stage2.py — PRISM-M Stage 2 confirmatory collection (2026az).

Re-runs the full battery on every brand appearing in the frozen PAIR_BANK:
4 artifact channels x ALL FOUR cross-family operator pairs x readouts
(dims + A-SCORE + A-RANK + A-PICK). Fresh draws for every op-pair (PL0
section 3 "re-run"). Writes data/stage2_records.jsonl. Resumable.

With --ablation, additionally collects the prompt-ablation robustness
subsample (first 10 bank brands x 1 channel x OP1+OP3, ablated renderer
prompt, prompt_variant="ablated").

Run (keys via bws; long runs sandbox OFF):
    bws run -- research/prism_m/code/run_campaign.sh stage2
    bws run -- research/prism_m/code/run_campaign.sh stage2 --ablation
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_m_lib import (  # noqa: E402
    DATA_DIR,
    PRISM_M_DIR,
    bank_brands,
    load_bank,
    load_config,
    load_records,
    measure_brand,
)

READOUTS = ("dims", "score", "rank", "pick")


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--ablation", action="store_true")
    ap.add_argument("--ops", default=None, help="comma list, e.g. OP2,OP4")
    ap.add_argument("--channels", default=None)
    ap.add_argument("--suffix", default="", help="output shard suffix")
    args = ap.parse_args()
    ablation = args.ablation
    cfg = load_config()
    bank = load_bank()
    pair_bank = yaml.safe_load((PRISM_M_DIR / "PAIR_BANK.yaml").read_text())
    in_pairs = sorted({b for e in pair_bank["retained_pairs"] for b in e["pair"]})
    brand_rows = [b for b in bank_brands(bank) if b["brand"] in in_pairs]
    channels = [
        {"id": v["id"], "description": v["description"]}
        for v in cfg["artifact_channels"].values()
    ]
    if args.channels:
        keep = set(args.channels.split(","))
        channels = [c for c in channels if c["id"] in keep]
    ops = cfg["operator_pairs"]
    if args.ops:
        keep_ops = set(args.ops.split(","))
        ops = {k: v for k, v in ops.items() if k in keep_ops}

    out = DATA_DIR / f"stage2_records{args.suffix}.jsonl"
    done = set()
    for shard in DATA_DIR.glob("stage2_records*.jsonl"):
        for r in load_records(shard):
            done.add(
                (
                    r["brand"],
                    r["channel"],
                    r["op_pair"],
                    r["readout"],
                    r.get("prompt_variant", "main"),
                )
            )

    if not ablation:
        total = len(brand_rows) * len(channels) * len(ops)
        i = 0
        for brand_row in brand_rows:
            for channel in channels:
                for op_id, op in ops.items():
                    i += 1
                    if all(
                        (brand_row["brand"], channel["id"], op_id, ro, "main") in done
                        for ro in READOUTS
                    ):
                        continue
                    print(
                        f"[stage2 {i}/{total}] {brand_row['brand']} / "
                        f"{channel['id']} / {op_id}",
                        flush=True,
                    )
                    measure_brand(
                        brand_row,
                        channel,
                        op_id,
                        op,
                        phase="stage2",
                        readouts=READOUTS,
                        out_path=out,
                    )
        print(f"[stage2] complete -> {out}")
    else:
        sub = brand_rows[:10]
        chan = channels[0]
        abl_ops = {k: v for k, v in ops.items() if k in ("OP1", "OP3")}
        total = len(sub) * len(abl_ops)
        i = 0
        for brand_row in sub:
            for op_id, op in abl_ops.items():
                i += 1
                if all(
                    (brand_row["brand"], chan["id"], op_id, ro, "ablated") in done
                    for ro in ("dims", "score")
                ):
                    continue
                print(
                    f"[ablation {i}/{total}] {brand_row['brand']} / {op_id}",
                    flush=True,
                )
                measure_brand(
                    brand_row,
                    chan,
                    op_id,
                    op,
                    phase="stage2_ablation",
                    readouts=("dims", "score"),
                    out_path=out,
                    prompt_variant="ablated",
                )
        print(f"[stage2 ablation] complete -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
