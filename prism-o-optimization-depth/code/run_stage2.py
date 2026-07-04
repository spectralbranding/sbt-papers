#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0"]
# ///
"""run_stage2.py — PRISM-O (2026bd) Stage-2 confirmatory campaign.

For every organization x channel x pinned artifact x operator pair:
  1. SEGMENTER call on the pinned artifact text -> intervention list
     (verbatim spans; capped at MAX_IV_PER_ARTIFACT = 8, a frozen
     implementation constant for cost control — overflow count logged);
  2. CLASSIFIER call (other family) per intervention span -> rung.

Masked arm: the first MASKED_ORGS organizations in deterministic org-name
order are re-read with every name variant replaced by the masking token
(PL1 masking block). arm in {named, masked}.

HARD order: pre-run version check (stage2 pins) before any substantive
call. Budget guard: logged stage-2 spend (PL3 usage x PL1 prices) checked
every unit against budget_cap_usd_stage2 = $193 (user-approved 2026-07-03).
Resumable: done keys (org, channel, artifact_id, op_pair, arm) skipped —
safe to shard by --ops / --org-slice across parallel processes.

Run (keys via bws; sandbox OFF; one shard per operator pair):
    bws run -- research/prism_o/code/run_campaign.sh stage2 --ops OP1
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_o_lib import (  # noqa: E402
    DATA_DIR,
    LOGS_DIR,
    PRISM_O_DIR,
    RUNGS,
    SEGMENTER_SYSTEM,
    _rubric_prompt_block,
    append_record,
    classifier_system,
    classifier_user,
    load_config,
    load_records,
    segmenter_user,
    utc_now,
    version_check,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "research"))
from prism_core.provider import call_model, parse_json_block  # noqa: E402

MAX_IV_PER_ARTIFACT = 8
MASKED_ORGS = 15
MASK_TOKEN = "[the company]"


def stage2_spend_usd(prices: dict) -> float:
    from prism_o_lib import usage_from_log_record

    total = 0.0
    for f in LOGS_DIR.glob("phase_stage2_*.jsonl"):
        with f.open() as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                tin, tout = usage_from_log_record(rec)
                p = prices.get(rec.get("operator") or "")
                if p:
                    total += (tin * p["input"] + tout * p["output"]) / 1_000_000
    return total


def mask_text(text: str, variants: list[str]) -> str:
    out = text
    for v in sorted(set(variants), key=len, reverse=True):
        if len(v) >= 2:
            out = re.sub(re.escape(v), MASK_TOKEN, out, flags=re.I)
    return out


def read_artifact(org, channel, art, text, op_id, op, rubric_block, arm, out_path):
    seg, cls = op["segmenter"], op["classifier"]
    base_op = f"stage2:{org['org']}:{channel}:{art['artifact_id']}:{op_id}:{arm}"
    seg_raw = call_model(
        seg["model"], seg["family"], SEGMENTER_SYSTEM, segmenter_user(text),
        role="segmenter", operation=base_op + ":segment", phase="stage2",
        logs_dir=LOGS_DIR, max_out=3000,
    )
    try:
        ivs = parse_json_block(seg_raw).get("interventions", [])
    except ValueError:
        ivs = None  # malformed segmentation; logged + flagged
    n_detected = len(ivs) if ivs is not None else -1
    kept = (ivs or [])[:MAX_IV_PER_ARTIFACT]
    for idx, iv in enumerate(kept):
        span = str(iv.get("span", ""))[:1500]
        summary = str(iv.get("summary", ""))[:300]
        if not span.strip():
            continue
        cls_raw = call_model(
            cls["model"], cls["family"], classifier_system(rubric_block),
            classifier_user(span if len(span) > 40 else f"{span}\n(context summary: {summary})"),
            role="classifier", operation=base_op + f":classify:{idx}", phase="stage2",
            logs_dir=LOGS_DIR, max_out=2400,
        )
        try:
            cj = parse_json_block(cls_raw)
            rung = str(cj.get("rung", "")).strip().upper()
            if rung not in RUNGS:
                rung = "MALFORMED"
        except ValueError:
            cj, rung = {}, "MALFORMED"
        append_record(
            out_path,
            {
                "phase": "stage2", "arm": arm, "org": org["org"],
                "stratum": org["stratum"], "ai_announcer": org["ai_announcer"],
                "channel": channel, "artifact_id": art["artifact_id"],
                "artifact_class": art["class"], "artifact_sha256": art["sha256"],
                "op_pair": op_id, "segmenter_model": seg["model"],
                "classifier_model": cls["model"], "iv_idx": idx,
                "n_interventions_detected": n_detected,
                "n_interventions_read": len(kept), "span": span,
                "rung_pred": rung, "confidence": cj.get("confidence"),
                "ts": utc_now(),
            },
        )
    # completion sentinel so resumability works even for 0-intervention artifacts
    append_record(
        out_path,
        {
            "phase": "stage2", "arm": arm, "org": org["org"], "channel": channel,
            "artifact_id": art["artifact_id"], "op_pair": op_id, "iv_idx": -1,
            "sentinel": True, "n_interventions_detected": n_detected,
            "n_interventions_read": len(kept), "ts": utc_now(),
        },
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ops", default=None, help="comma list, e.g. OP1")
    ap.add_argument("--suffix", default="", help="output shard suffix, e.g. _op1")
    ap.add_argument("--org-slice", default=None, help="e.g. 0:25 over sorted orgs")
    ap.add_argument("--skip-version-check", action="store_true",
                    help="shard mode: check already done by the launcher this epoch")
    args = ap.parse_args()

    cfg = load_config()
    cap = float(cfg["budget_cap_usd_stage2"])
    prices = cfg["list_prices"]
    rubric_block = _rubric_prompt_block()
    manifest = json.loads((DATA_DIR / "panel_pinned_manifest.json").read_text())
    orgs = sorted(manifest["orgs"], key=lambda o: o["org"])
    masked_set = {o["org"] for o in orgs[:MASKED_ORGS]}
    if args.org_slice:
        a, b = args.org_slice.split(":")
        orgs = orgs[int(a) : int(b)]
    ops = {
        op_id: op
        for op_id, op in cfg["operator_pairs"].items()
        if "stage2" in op.get("stages", [])
        and (not args.ops or op_id in set(args.ops.split(",")))
    }

    if not args.skip_version_check:
        vc = version_check(cfg, "stage2")
        print(f"[version-check] ok={vc['ok']}", flush=True)
        if not vc["ok"]:
            return 2

    out = DATA_DIR / f"stage2_records{args.suffix}.jsonl"
    done = set()
    for shard in DATA_DIR.glob("stage2_records*.jsonl"):
        for r in load_records(shard):
            if r.get("sentinel"):
                done.add((r["org"], r["channel"], r["artifact_id"], r["op_pair"], r["arm"]))

    total = sum(
        len(o["artifacts"]) * len(ops) * (2 if o["org"] in masked_set else 1) for o in orgs
    )
    i = 0
    for org in orgs:
        texts = {}
        for art in org["artifacts"]:
            texts[art["artifact_id"]] = (PRISM_O_DIR / art["path"]).read_text()
        arms = ["named"] + (["masked"] if org["org"] in masked_set else [])
        for arm in arms:
            for art in org["artifacts"]:
                text = texts[art["artifact_id"]]
                if arm == "masked":
                    text = mask_text(text, org["name_variants"])
                for op_id, op in ops.items():
                    i += 1
                    key = (org["org"], art["channel"], art["artifact_id"], op_id, arm)
                    if key in done:
                        continue
                    spend = stage2_spend_usd(prices)
                    if spend > cap:
                        raise RuntimeError(f"STAGE-2 BUDGET CAP: ${spend:.2f} > ${cap:.2f}")
                    print(
                        f"[stage2 {i}/{total}] {org['org']}/{art['channel']}/"
                        f"{art['artifact_id']}/{op_id}/{arm} (spend ${spend:.2f})",
                        flush=True,
                    )
                    read_artifact(org, art["channel"], art, text, op_id, op,
                                  rubric_block, arm, out)
                    done.add(key)
    print(f"[stage2] shard complete (ops={list(ops)}) spend ${stage2_spend_usd(prices):.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
