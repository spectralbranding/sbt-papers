#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0", "numpy>=1.26"]
# ///
"""run_pilot.py — PRISM-C pre-flight operator-concordance pilot (PL0 §9.2).

~56 calls BEFORE the banks freeze:
- choice side: 5 spread scenarios x 2 arrangements x 4 chooser families
  (40 calls) -> per-family majority-pick discordance -> mechanical exclusion
  rule (score > 3x median of others) -> post-exclusion choice floor;
- stated side: 2 spread brands x 1 channel x 4 operator pairs (16 calls,
  render+extract) -> per-op-pair leave-one-out vector discordance -> same
  rule.

PILOT GATE: post-exclusion choice floor <= PL1 pilot.gate_max_choice_floor
(.25). If the gate FAILS the script exits nonzero and confirmatory
collection MUST NOT start (PL0 §9.2: stop and report).

Run (keys via bws; sandbox OFF):
    bws run -- research/prism_c/code/run_campaign.sh pilot
"""

from __future__ import annotations

import json
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
    measure_stated,
)
from prism_core.concordance import (  # noqa: E402
    apply_exclusion_rule,
    pairwise_disagreement_floor,
    per_family_pick_table,
    pick_concordance,
    vector_concordance,
)

# Spread across sectors/coherence types (b2c: status / food / identity;
# b2b: platform / infrastructure).
PILOT_SCENARIOS = ["S01", "S07", "S16", "S22", "S27"]
PILOT_BRANDS = ["Apple", "SAP"]  # one b2c ecosystem, one b2b ecosystem
PILOT_CHANNEL = "official"


def main() -> int:
    cfg = load_config()
    sbank = load_scenario_bank()
    blookup = brand_lookup(load_brand_bank())
    out = DATA_DIR / "pilot_records.jsonl"
    done = set()
    if out.exists():
        for r in load_records(out):
            if r["kind"] == "choice":
                done.add(("choice", r["scenario"], r["arrangement_id"], r["chooser"]))
            elif r["kind"] == "stated":
                done.add(("stated", r["brand"], r["channel"], r["op_pair"]))

    scenarios = {s["id"]: s for s in sbank["scenarios"]}
    descriptors_all = {b: blookup[b]["category"] for b in blookup}

    # --- choice side
    n_arr = int(cfg["pilot"]["choice_arrangements"])
    for sid in PILOT_SCENARIOS:
        sc = scenarios[sid]
        arrs = arrangements(sc["choice_set"], 8)[:n_arr]
        for arr_id, arr in enumerate(arrs):
            for ch_id, ch in cfg["choosers"].items():
                if ("choice", sid, arr_id, ch_id) in done:
                    continue
                measure_choice(
                    sc,
                    arr,
                    arr_id,
                    ch_id,
                    ch,
                    descriptors_all,
                    phase="pilot",
                    out_path=out,
                )
                print(f"[pilot] choice {sid} arr{arr_id} {ch_id}", flush=True)

    # --- stated side
    channel = next(
        c for c in cfg["artifact_channels"].values() if c["id"] == PILOT_CHANNEL
    )
    for brand in PILOT_BRANDS:
        row = blookup[brand]
        for op_id, op in cfg["operator_pairs"].items():
            if ("stated", brand, PILOT_CHANNEL, op_id) in done:
                continue
            measure_stated(row, channel, op_id, op, phase="pilot", out_path=out)
            print(f"[pilot] stated {brand} {op_id}", flush=True)

    # --- evaluation
    recs = load_records(out)
    choice_recs = [
        r for r in recs if r["kind"] == "choice" and not r.get("flagged_malformed")
    ]
    stated_recs = [
        r for r in recs if r["kind"] == "stated" and not r.get("flagged_malformed")
    ]

    picks = per_family_pick_table(
        choice_recs, key_fields=("scenario", "arrangement_id")
    )
    fam_scores = pick_concordance(picks)
    fam_rule = apply_exclusion_rule(fam_scores)
    kept_families = set(fam_rule["kept"])
    kept_picks = {f: p for f, p in picks.items() if f in kept_families}
    floor_all = pairwise_disagreement_floor(picks)
    floor_kept = pairwise_disagreement_floor(kept_picks)

    readings: dict = {}
    stims = sorted({(r["brand"], r["channel"]) for r in stated_recs})
    for op_id in cfg["operator_pairs"]:
        vals = []
        for stim in stims:
            match = [
                r["value"]
                for r in stated_recs
                if (r["brand"], r["channel"]) == stim and r["op_pair"] == op_id
            ]
            vals.append(match[0] if match else None)
        readings[op_id] = vals
    op_scores = vector_concordance(readings)
    op_rule = apply_exclusion_rule(op_scores)

    gate_max = float(cfg["pilot"]["gate_max_choice_floor"])
    gate_pass = floor_kept <= gate_max

    report = {
        "pilot_scenarios": PILOT_SCENARIOS,
        "pilot_brands": PILOT_BRANDS,
        "family_discordance": fam_scores,
        "family_exclusion": fam_rule,
        "choice_floor_all_families": floor_all,
        "choice_floor_kept_families": floor_kept,
        "op_pair_discordance": op_scores,
        "op_pair_exclusion": op_rule,
        "gate_max_choice_floor": gate_max,
        "gate_pass": bool(gate_pass),
        "n_choice_records": len(choice_recs),
        "n_stated_records": len(stated_recs),
    }
    report_path = DATA_DIR / "pilot_report.json"
    report_path.write_text(json.dumps(report, indent=2, default=str))
    print(json.dumps(report, indent=2, default=str))
    print(f"[pilot] report: {report_path}")
    if not gate_pass:
        print("[pilot] GATE FAILED - do NOT start confirmatory collection")
        return 1
    print("[pilot] gate PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
