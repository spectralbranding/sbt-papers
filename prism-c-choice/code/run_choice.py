#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0", "numpy>=1.26"]
# ///
"""run_choice.py — PRISM-C choice battery + controls (2026bb).

Confirmatory: every scenario x its counterbalanced arrangements (PL0 §9.1)
x the chooser families kept after the pilot exclusion rule. Controls
(--controls): positive dominating-option sets + negative near-duplicate twin
sets. Writes PL3 JSONL (logs/) + parsed records
(data/choice_records[SUFFIX].jsonl). Resumable per (scenario,
arrangement_id, chooser).

Run (keys via bws; long runs sandbox OFF; shardable):
    bws run -- research/prism_c/code/run_campaign.sh choice
        [--families CH-ANT,CH-OAI] [--scenarios S01,S02] [--suffix _c1]
    bws run -- research/prism_c/code/run_campaign.sh choice --controls
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
    arrangements,
    brand_lookup,
    load_brand_bank,
    load_config,
    load_records,
    load_scenario_bank,
    measure_choice,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--families", default=None, help="comma list of chooser ids")
    ap.add_argument("--scenarios", default=None)
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--suffix", default="")
    args = ap.parse_args()
    out = DATA_DIR / f"choice_records{args.suffix}.jsonl"

    cfg = load_config()
    sbank = load_scenario_bank()
    blookup = brand_lookup(load_brand_bank())
    n_arr = int(cfg.get("n_arrangements", 8))

    choosers = dict(cfg["choosers"])
    excluded = set(cfg.get("pilot_excluded_choosers") or [])
    choosers = {k: v for k, v in choosers.items() if k not in excluded}
    if args.families:
        keep = set(args.families.split(","))
        choosers = {k: v for k, v in choosers.items() if k in keep}

    done = set()
    for shard in sorted(DATA_DIR.glob("choice_records*.jsonl")):
        for r in load_records(shard):
            if r["kind"] == "choice":
                done.add((r["scenario"], r["arrangement_id"], r["chooser"]))

    n = 0
    if args.controls:
        n_ctl_arr = int(cfg["controls"].get("control_arrangements", 8))
        for sc in sbank["positive_controls"]:
            descriptors = {b: blookup[b]["category"] for b in sc["choice_set"]}
            for arr_id, arr in enumerate(arrangements(sc["choice_set"], n_ctl_arr)):
                for ch_id, ch in choosers.items():
                    if (sc["id"], arr_id, ch_id) in done:
                        continue
                    measure_choice(
                        sc,
                        arr,
                        arr_id,
                        ch_id,
                        ch,
                        descriptors,
                        phase="controls",
                        out_path=out,
                        control="positive",
                        dominant=sc["dominant"],
                    )
                    n += 1
                    print(f"[pos] {sc['id']} arr{arr_id} {ch_id}", flush=True)
        for sc in sbank["negative_controls"]:
            names = [o["name"] for o in sc["options"]]
            descriptors = {o["name"]: o["descriptor"] for o in sc["options"]}
            for arr_id, arr in enumerate(arrangements(names, n_ctl_arr)):
                for ch_id, ch in choosers.items():
                    if (sc["id"], arr_id, ch_id) in done:
                        continue
                    measure_choice(
                        sc,
                        arr,
                        arr_id,
                        ch_id,
                        ch,
                        descriptors,
                        phase="controls",
                        out_path=out,
                        control="negative",
                    )
                    n += 1
                    print(f"[neg] {sc['id']} arr{arr_id} {ch_id}", flush=True)
        print(f"[choice] controls complete: {n} new trials -> {out}")
        return 0

    scenarios = sbank["scenarios"]
    if args.scenarios:
        keep = set(args.scenarios.split(","))
        scenarios = [s for s in scenarios if s["id"] in keep]
    for sc in scenarios:
        descriptors = {b: blookup[b]["category"] for b in sc["choice_set"]}
        for arr_id, arr in enumerate(arrangements(sc["choice_set"], n_arr)):
            for ch_id, ch in choosers.items():
                if (sc["id"], arr_id, ch_id) in done:
                    continue
                measure_choice(
                    sc,
                    arr,
                    arr_id,
                    ch_id,
                    ch,
                    descriptors,
                    phase="confirmatory",
                    out_path=out,
                )
                n += 1
                print(f"[choice] {sc['id']} arr{arr_id} {ch_id}", flush=True)
    print(f"[choice] complete: {n} new trials -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
