#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0", "numpy>=1.26"]
# ///
"""run_stage1.py — PRISM-O (2026bd) Stage-1 constructed-ground-truth run.

Order is HARD (PL1 verification equipment, methodology-0.3.0):
  0. pre-run VERSION CHECK: pinned model ids vs live /models catalogs; any
     missing pin aborts the run (re-pin + re-freeze required);
  1. CONCORDANCE SCREEN: the 8 probe bases (both variants, both Stage-1
     pairs), scored as per-pair disagreement with the other pair's rung on
     identical stimuli; mechanical 3x-median exclusion (prism_core).
     A pair excluded here stops the run (with 2 Stage-1 pairs, exclusion
     means no floor is estimable — report and stop, no rescue);
  2. FULL BANK: 52 units x Stage-1 pairs, resumable (done keys skipped).
     Probe records from step 1 count toward completion (same records file).

Budget guard: aborts if the PL3-logged spend exceeds budget_cap_usd_stage1.

Run (keys via bws; sandbox OFF for the long run):
    bws run -- research/prism_o/code/run_campaign.sh stage1
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_o_lib import (  # noqa: E402
    DATA_DIR,
    LOGS_DIR,
    _rubric_prompt_block,
    expand_bank,
    load_bank,
    load_config,
    load_records,
    read_unit,
    version_check,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "research"))
from prism_core.concordance import apply_exclusion_rule  # noqa: E402


def logged_spend_usd() -> float:
    total = 0.0
    for f in LOGS_DIR.glob("*.jsonl"):
        with f.open() as fh:
            for line in fh:
                try:
                    total += float(json.loads(line).get("cost_usd_est") or 0.0)
                except (ValueError, TypeError):
                    continue
    return total


def main() -> int:
    cfg = load_config()
    cap = float(cfg["budget_cap_usd_stage1"])
    bank = load_bank()
    units = expand_bank(bank)
    rubric_block = _rubric_prompt_block()
    out = DATA_DIR / "stage1_records.jsonl"
    stage1_ops = {
        op_id: op
        for op_id, op in cfg["operator_pairs"].items()
        if "stage1" in op.get("stages", [])
    }

    # --- 0. version check (abort on stale pin) ---
    vc = version_check(cfg, "stage1")
    print(f"[version-check] ok={vc['ok']} -> data/version_check_stage1.json", flush=True)
    if not vc["ok"]:
        print("[version-check] STALE PIN — stopping before any substantive call.")
        return 2

    done = set()
    if out.exists():
        for r in load_records(out):
            done.add((r["base_id"], r["variant"], r["op_pair"]))

    def run_units(subset, label):
        total = len(subset) * len(stage1_ops)
        i = 0
        for unit in subset:
            for op_id, op in stage1_ops.items():
                i += 1
                key = (unit["base_id"], unit["variant"], op_id)
                if key in done:
                    continue
                spend = logged_spend_usd()
                if spend > cap:
                    raise RuntimeError(f"budget cap exceeded: ${spend:.2f} > ${cap:.2f}")
                print(
                    f"[{label} {i}/{total}] {unit['base_id']}/{unit['variant']}/{op_id}",
                    flush=True,
                )
                read_unit(unit, op_id, op, rubric_block, "stage1", out)
                done.add(key)

    # --- 1. concordance screen on the probe subset ---
    probes = [u for u in units if u["probe"]]
    run_units(probes, "probe")
    records = load_records(out)
    probe_keys = sorted({(r["base_id"], r["variant"]) for r in records if r["probe"]})
    picks = {}
    for op_id in stage1_ops:
        by_key = {
            (r["base_id"], r["variant"]): r["rung_pred"]
            for r in records
            if r["op_pair"] == op_id and r["probe"]
        }
        picks[op_id] = [by_key.get(k) for k in probe_keys]
    ops = sorted(picks)
    scores = {}
    for op_id in ops:
        pairs = [
            (picks[op_id][i], picks[o][i])
            for o in ops
            if o != op_id
            for i in range(len(probe_keys))
            if picks[op_id][i] is not None and picks[o][i] is not None
        ]
        scores[op_id] = (
            sum(1.0 for a, b in pairs if a != b) / len(pairs) if pairs else float("nan")
        )
    verdict = apply_exclusion_rule(scores)
    (DATA_DIR / "concordance_screen_stage1.json").write_text(
        json.dumps({"picks_aligned_on": len(probe_keys), **verdict}, indent=2)
    )
    print(f"[concordance] scores={scores} excluded={verdict['excluded']}", flush=True)
    if verdict["excluded"]:
        print(
            "[concordance] EXCLUSION FIRED with only two Stage-1 pairs — no floor "
            "estimable; stopping per the no-rescue rule."
        )
        return 3

    # --- 2. full bank ---
    run_units(units, "stage1")
    print(f"[stage1] complete -> {out}  (spend ${logged_spend_usd():.2f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
