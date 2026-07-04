#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0"]
# ///
"""rerun_rc1.py — RC1 tie-breaker sensitivity via a RE-READ ARM (2026bd).

Executes the pre-registered three-regime sensitivity (RUBRIC.md §3) that the
original design could not compute post hoc (limitation L5): the tie-break
binds inside the classifier prompt, so alternative regimes require re-reads.
This arm re-classifies, under two amended prompts, (a) every named-arm
Stage-2 intervention span and (b) the full Stage-1 bank — SAME spans, SAME
classifier model per pair, ONLY the tie-break regime overridden by an
explicit, labeled paragraph appended after the frozen rubric block:

- regime "up":  ties between adjacent rungs break UPWARD (deeper);
- regime "tie": ties are FLAGGED (rung: "TIE") and excluded in analysis.

Documented as PL0 v1.2 post-campaign amendment: the primary analysis and its
frozen downward regime are unchanged; this arm exists solely to compute the
pre-registered sensitivity. Costs are classifier-only (cheap models); the
$193 Stage-2 cap continues to govern (phase=stage2 logs).

Run:  bws run -- research/prism_o/code/run_campaign.sh rc1 --regime up
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_o_lib import (  # noqa: E402
    DATA_DIR,
    LOGS_DIR,
    RUNGS,
    _rubric_prompt_block,
    append_record,
    classifier_system,
    classifier_user,
    expand_bank,
    load_bank,
    load_config,
    load_records,
    utc_now,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "research"))
from prism_core.provider import call_model, parse_json_block  # noqa: E402

OVERRIDES = {
    "up": (
        "\n\nREGIME OVERRIDE (pre-registered sensitivity arm — supersedes the "
        "tie-break sentence above): ties between adjacent rungs after the "
        "specified-not-promised test break UPWARD, toward the deeper rung "
        "(toward D1). Everything else in the rubric is unchanged."
    ),
    "tie": (
        "\n\nREGIME OVERRIDE (pre-registered sensitivity arm — supersedes the "
        "tie-break sentence above): when adjacent rungs remain equally "
        'supported after the specified-not-promised test, return "rung": '
        '"TIE" instead of choosing. Everything else in the rubric is '
        "unchanged."
    ),
}
VALID = set(RUNGS) | {"TIE"}


def classify(span: str, model: dict, system: str, op_label: str, regime: str) -> str:
    raw = call_model(
        model["model"], model["family"], system, classifier_user(span),
        role="classifier", operation=f"stage2:rc1:{regime}:{op_label}",
        phase="stage2", logs_dir=LOGS_DIR, max_out=2400,
    )
    try:
        rung = str(parse_json_block(raw).get("rung", "")).strip().upper()
        return rung if rung in VALID else "MALFORMED"
    except ValueError:
        return "MALFORMED"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--regime", required=True, choices=["up", "tie"])
    ap.add_argument("--ops", default=None)
    args = ap.parse_args()
    cfg = load_config()
    system = classifier_system(_rubric_prompt_block()) + OVERRIDES[args.regime]

    # Stage-1 bank re-read
    out1 = DATA_DIR / f"stage1_rc1_{args.regime}.jsonl"
    done1 = {(r["base_id"], r["variant"], r["op_pair"]) for r in load_records(out1)} if out1.exists() else set()
    stage1_ops = {k: v for k, v in cfg["operator_pairs"].items() if "stage1" in v["stages"]}
    units = expand_bank(load_bank())
    for unit in units:
        for op_id, op in stage1_ops.items():
            if (unit["base_id"], unit["variant"], op_id) in done1:
                continue
            rung = classify(unit["text"], op["classifier"], system,
                            f"s1:{unit['base_id']}:{unit['variant']}:{op_id}", args.regime)
            append_record(out1, {"regime": args.regime, "base_id": unit["base_id"],
                                 "variant": unit["variant"], "op_pair": op_id,
                                 "rung_pred": rung, "rung_truth": unit["rung_truth"],
                                 "anchored": unit["anchored"], "ts": utc_now()})
    print(f"[rc1:{args.regime}] stage1 bank done", flush=True)

    # Stage-2 named-arm spans re-read
    spans = []
    for shard in sorted(DATA_DIR.glob("stage2_records_op*.jsonl")):
        for r in load_records(shard):
            if not r.get("sentinel") and r.get("arm") == "named" and r.get("span"):
                spans.append(r)
    if args.ops:
        keep = set(args.ops.split(","))
        spans = [r for r in spans if r["op_pair"] in keep]
    out2 = DATA_DIR / f"stage2_rc1_{args.regime}.jsonl"
    done2 = set()
    if out2.exists():
        for r in load_records(out2):
            done2.add((r["org"], r["channel"], r["artifact_id"], r["op_pair"], r["iv_idx"]))
    total = len(spans)
    for i, r in enumerate(spans):
        key = (r["org"], r["channel"], r["artifact_id"], r["op_pair"], r["iv_idx"])
        if key in done2:
            continue
        op = cfg["operator_pairs"][r["op_pair"]]
        if i % 200 == 0:
            print(f"[rc1:{args.regime} {i}/{total}] {r['org']}/{r['channel']}/{r['op_pair']}", flush=True)
        rung = classify(r["span"], op["classifier"], system,
                        f"{r['org']}:{r['channel']}:{r['artifact_id']}:{r['op_pair']}:{r['iv_idx']}",
                        args.regime)
        append_record(out2, {"regime": args.regime, "org": r["org"], "channel": r["channel"],
                             "artifact_id": r["artifact_id"], "op_pair": r["op_pair"],
                             "iv_idx": r["iv_idx"], "rung_pred": rung,
                             "rung_downward": r["rung_pred"], "ts": utc_now()})
        done2.add(key)
    print(f"[rc1:{args.regime}] complete -> {out2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
