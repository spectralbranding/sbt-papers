#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0", "numpy>=1.26"]
# ///
"""run_stated.py — PRISM-C stated readings + need vectors (2026bb).

Stated: every brand in the reused frozen bank x 4 artifact channels x the
operator pairs kept after the pilot exclusion rule (render + dims extract).
Need: every confirmatory scenario x the kept operator pairs (need renderer +
dims extract). Writes PL3 JSONL (logs/) + parsed records
(data/stated_records[SUFFIX].jsonl). Resumable: existing (brand, channel,
op) / (scenario, op) cells are skipped.

Run (keys via bws; long runs sandbox OFF; shardable):
    bws run -- research/prism_c/code/run_campaign.sh stated [--ops OP1,OP2]
        [--brands A,B] [--channels official,press] [--needs-only]
        [--stated-only] [--suffix _s1]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))

from prism_c_lib import (  # noqa: E402
    DATA_DIR,
    bank_brands,
    load_brand_bank,
    load_config,
    load_records,
    load_scenario_bank,
    measure_need,
    measure_stated,
)


def kept_ops(cfg: dict, ops_arg: str | None) -> dict:
    """Default: floor-kept pairs only (pilot exclusion applied). An explicit
    --ops list overrides the exclusion so the excluded pair can still be
    collected as the pre-registered exploratory observer."""
    ops = dict(cfg["operator_pairs"])
    if ops_arg:
        keep = set(ops_arg.split(","))
        return {k: v for k, v in ops.items() if k in keep}
    excluded = set(cfg.get("pilot_excluded_op_pairs") or [])
    return {k: v for k, v in ops.items() if k not in excluded}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ops", default=None)
    ap.add_argument("--brands", default=None)
    ap.add_argument("--channels", default=None)
    ap.add_argument("--scenarios", default=None)
    ap.add_argument("--needs-only", action="store_true")
    ap.add_argument("--stated-only", action="store_true")
    ap.add_argument("--suffix", default="")
    args = ap.parse_args()
    out = DATA_DIR / f"stated_records{args.suffix}.jsonl"

    cfg = load_config()
    ops = kept_ops(cfg, args.ops)
    brands = bank_brands(load_brand_bank())
    if args.brands:
        keep = set(args.brands.split(","))
        brands = [b for b in brands if b["brand"] in keep]
    channels = [
        {"id": v["id"], "description": v["description"]}
        for v in cfg["artifact_channels"].values()
    ]
    if args.channels:
        keep = set(args.channels.split(","))
        channels = [c for c in channels if c["id"] in keep]
    scenarios = load_scenario_bank()["scenarios"]
    if args.scenarios:
        keep = set(args.scenarios.split(","))
        scenarios = [s for s in scenarios if s["id"] in keep]

    done = set()
    for shard in sorted(DATA_DIR.glob("stated_records*.jsonl")):
        for r in load_records(shard):
            if r["kind"] == "stated":
                done.add(("stated", r["brand"], r["channel"], r["op_pair"]))
            elif r["kind"] == "need":
                done.add(("need", r["scenario"], r["op_pair"]))

    n = 0
    if not args.needs_only:
        for row in brands:
            for ch in channels:
                for op_id, op in ops.items():
                    if ("stated", row["brand"], ch["id"], op_id) in done:
                        continue
                    measure_stated(
                        row, ch, op_id, op, phase="confirmatory", out_path=out
                    )
                    n += 1
                    print(f"[stated] {row['brand']} {ch['id']} {op_id}", flush=True)
    if not args.stated_only:
        for sc in scenarios:
            for op_id, op in ops.items():
                if ("need", sc["id"], op_id) in done:
                    continue
                measure_need(sc, op_id, op, phase="confirmatory", out_path=out)
                n += 1
                print(f"[need] {sc['id']} {op_id}", flush=True)
    print(f"[stated] complete: {n} new measurements -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
