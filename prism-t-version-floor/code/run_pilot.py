#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "numpy>=1.26", "pyyaml>=6.0"]
# ///
"""run_pilot.py — PRISM-T pre-flight operator-concordance pilot (PL0 §9.4).

~38 calls BEFORE the PL1 freeze:
  (a) 2 brands x official x the 4 contemporaneous operator pairs -> the
      leave-one-out vector-concordance table + the mechanical 3x-median
      exclusion rule (the 2026az/2026bb OP4 screen);
  (b) 1 brand x official x every ladder rung -> rung availability + parse
      sanity (a rung that cannot render/extract is dropped and reported,
      never substituted).

Run (keys via bws; sandbox OFF):
    bws run -- research/prism_t/code/run_campaign.sh pilot
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_t_lib import (  # noqa: E402
    DATA_DIR,
    RESEARCH_DIR,
    bank_brands,
    load_artifact,
    load_bank,
    load_config,
    load_records,
    measure_artifact,
)

sys.path.insert(0, str(RESEARCH_DIR))
from prism_core import concordance  # noqa: E402

PILOT_OUT = DATA_DIR / "pilot_records.jsonl"
REPORT = DATA_DIR / "pilot_report.json"


def main() -> int:
    cfg = load_config()
    bank = load_bank()
    brands = bank_brands(bank)
    channel = {
        "id": "official",
        "description": cfg["artifact_channels"]["A1"]["description"],
    }
    stated_brands = brands[: cfg["pilot"]["stated_brands"]]
    ladder_brand = brands[0]

    done = set()
    if PILOT_OUT.exists():
        for r in load_records(PILOT_OUT):
            if r.get("dims") is not None and not r.get("flagged"):
                done.add((r["brand"], r["channel"], r["renderer"], r["extractor"]))

    # (a) operator-pair concordance screen
    for brand_row in stated_brands:
        art = load_artifact(brand_row["brand"], channel["id"])
        for op_id, op in cfg["operator_pairs"].items():
            key = (
                brand_row["brand"],
                channel["id"],
                op["renderer"]["model"],
                op["extractor"]["model"],
            )
            if key in done:
                continue
            print(f"[pilot:ops] {brand_row['brand']} / {op_id}", flush=True)
            measure_artifact(
                brand_row,
                channel,
                art,
                op["renderer"],
                op["extractor"],
                phase="pilot",
                out_path=PILOT_OUT,
            )

    # (b) ladder rung sanity
    art = load_artifact(ladder_brand["brand"], channel["id"])
    for lname, ladder in cfg["ladders"].items():
        for rung in ladder["rungs"]:
            key = (
                ladder_brand["brand"],
                channel["id"],
                rung["model"],
                ladder["extractor"]["model"],
            )
            if key in done:
                continue
            print(f"[pilot:ladder] {lname} / {rung['model']}", flush=True)
            measure_artifact(
                ladder_brand,
                channel,
                art,
                rung,
                ladder["extractor"],
                phase="pilot",
                out_path=PILOT_OUT,
            )

    # report: concordance + mechanical exclusion + rung availability
    records = load_records(PILOT_OUT)
    op_readings: dict[str, list] = {}
    stimuli = sorted(
        {
            r["brand"]
            for r in records
            if r["brand"] in {b["brand"] for b in stated_brands}
        }
    )
    for op_id, op in cfg["operator_pairs"].items():
        row = []
        for b in stimuli:
            vec = next(
                (
                    r["dims"]
                    for r in records
                    if r["brand"] == b
                    and r["renderer"] == op["renderer"]["model"]
                    and r["extractor"] == op["extractor"]["model"]
                    and r["dims"] is not None
                ),
                None,
            )
            row.append(vec)
        op_readings[op_id] = row
    scores = concordance.vector_concordance(op_readings)
    verdict = concordance.apply_exclusion_rule(scores)

    rungs_ok = {}
    for lname, ladder in cfg["ladders"].items():
        for rung in ladder["rungs"]:
            ok = any(
                r["renderer"] == rung["model"] and r["dims"] is not None
                for r in records
            )
            rungs_ok[rung["model"]] = ok
    report = {
        "operator_concordance": scores,
        "exclusion_verdict": verdict,
        "rung_availability": rungs_ok,
        "n_pilot_records": len(records),
    }
    REPORT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print(f"[pilot] report -> {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
