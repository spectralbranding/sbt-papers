#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "numpy>=1.26", "pyyaml>=6.0"]
# ///
"""run_ve1.py — PRISM-T epoch VE-1 capture (2026ba).

Reads the sealed pinned panel (byte-identical artifacts, manifest-verified on
every load) under three jobs:

  floor      40 brands x 4 channels x the 4 contemporaneous operator pairs
             (the H1 baseline; 1,280 calls)
  ladder     40 brands x 4 channels x every NON-TOP ladder rung under the
             ladder's fixed extractor (top rungs are shared with OP1/OP2/OP3
             and reuse the floor records; 8 rungs -> 2,560 calls)
  negcontrol run 2 of the designated same-version pair on the full panel
             (PL0 §5 negative control; 320 calls)

At VE-1 the live panel coincides with the pinned capture (PL0 §9.1);
the positive control is the designated distant pair INSIDE the openai-gpt
ladder (no extra calls). Resumable: existing (panel, brand, channel,
renderer, extractor, run) records are skipped. Shardable via --job /
--ladders / --ops / --brands i:j / --suffix.

Run (keys via bws; long runs sandbox OFF):
    bws run -- research/prism_t/code/run_campaign.sh floor
    bws run -- research/prism_t/code/run_campaign.sh ladder
    bws run -- research/prism_t/code/run_campaign.sh negcontrol
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_t_lib import (  # noqa: E402
    DATA_DIR,
    bank_brands,
    load_artifact,
    load_bank,
    load_config,
    load_records,
    measure_artifact,
    record_key,
)


def existing_keys() -> set:
    done = set()
    for shard in DATA_DIR.glob("ve1_records*.jsonl"):
        for r in load_records(shard):
            if r.get("dims") is not None and not r.get("flagged"):
                done.add(record_key(r))
    return done


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True, choices=["floor", "ladder", "negcontrol"])
    ap.add_argument("--ops", default=None, help="comma list, e.g. OP1,OP3")
    ap.add_argument("--ladders", default=None, help="comma list, e.g. anthropic-opus")
    ap.add_argument("--brands", default=None, help="slice i:j over the bank order")
    ap.add_argument("--suffix", default="", help="output shard suffix")
    args = ap.parse_args()
    out = DATA_DIR / f"ve1_records{args.suffix}.jsonl"

    cfg = load_config()
    brands = bank_brands(load_bank())
    if args.brands:
        i, j = (int(x) if x else None for x in args.brands.split(":"))
        brands = brands[i:j]
    channels = [
        {"id": v["id"], "description": v["description"]}
        for v in cfg["artifact_channels"].values()
    ]
    done = existing_keys()

    def run_cell(brand_row, channel, renderer, extractor, *, run=1, phase="ve1"):
        key = (
            "pinned",
            brand_row["brand"],
            channel["id"],
            renderer["model"],
            extractor["model"],
            run,
        )
        if key in done:
            return
        art = load_artifact(brand_row["brand"], channel["id"])
        print(
            f"[{args.job}] {brand_row['brand']} / {channel['id']} / "
            f"{renderer['model']} -> {extractor['model']} (run {run})",
            flush=True,
        )
        measure_artifact(
            brand_row,
            channel,
            art,
            renderer,
            extractor,
            phase=phase,
            run=run,
            out_path=out,
        )

    if args.job == "floor":
        ops = cfg["operator_pairs"]
        if args.ops:
            keep = set(args.ops.split(","))
            ops = {k: v for k, v in ops.items() if k in keep}
        for brand_row in brands:
            for channel in channels:
                for op in ops.values():
                    run_cell(brand_row, channel, op["renderer"], op["extractor"])

    elif args.job == "ladder":
        ladders = cfg["ladders"]
        if args.ladders:
            keep = set(args.ladders.split(","))
            ladders = {k: v for k, v in ladders.items() if k in keep}
        for lname, ladder in ladders.items():
            non_top = ladder["rungs"][:-1]  # top rung shared with the floor job
            for brand_row in brands:
                for channel in channels:
                    for rung in non_top:
                        run_cell(brand_row, channel, rung, ladder["extractor"])

    elif args.job == "negcontrol":
        neg = cfg["controls"]["negative"]
        renderer = {"model": neg["model"], "family": neg["family"]}
        for brand_row in brands:
            for channel in channels:
                run_cell(
                    brand_row,
                    channel,
                    renderer,
                    neg["extractor"],
                    run=2,
                    phase="ve1-negcontrol",
                )

    print(f"[{args.job}] complete -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
