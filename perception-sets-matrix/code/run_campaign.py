#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0"]
# ///
"""run_campaign.py — resumable collection for the 2026bf campaign.

Arms (frozen in PROTOCOL.yaml; floors F1/F3 are computed by the estimator
from the reading arm itself — no separate floor calls):
  validate   Study-1 pack recovery gate: validation ops x 6 packs x r=3
  cohorts    cohort-profile validation: persona text -> 8-vector, r=1
  readings   cohort-unconditioned brand readings (pack / elicited), r=3
  eliciting  constant-sum + Juster + switching probe, r=3 per cohort
  samecall   common-method contrast arm: joint readings+allocation, r=1

Usage (keys via bws wrapper; long runs sandbox-OFF):
  uv run python run_campaign.py --arm floors --ops OP1
  uv run python run_campaign.py --arm all --ops OP1   # one operator shard
  uv run python run_campaign.py --arm validate        # validation ops only

Records: ../data/records_<OP>.jsonl (append-only; record_key dedup makes
re-runs resume). Failed-after-reprompt calls are recorded with failed=true
and count toward floor F4. Every model API call is JSONL-logged to ../logs/.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json

import psm_lib as L


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def category_materials(cat: str, proto: dict) -> tuple[list[str], str, str]:
    """Return (brand_names, materials_text, category_label) for a category."""
    cfg = proto["categories"][cat]
    if cfg["mode"] == "pack":
        s1 = L.load_study1()
        names = [b["name"] for b in s1["brands"]]
        materials = "\n\n=====\n\n".join(L.pack_text(b) for b in s1["brands"])
        label = s1["category"]
    else:
        s2 = L.load_study2()[cat]
        names = [b["name"] for b in s2["brands"]]
        materials = (
            "Brands (judge from your knowledge of their public presence): "
            + "; ".join(names)
        )
        label = s2["category_label"]
    return names, materials, label


def collect_one(
    op: dict,
    system: str,
    user: str,
    parser,
    *,
    arm: str,
    record_key: str,
    out_path,
    meta: dict,
    max_out: int = 2000,
) -> None:
    """One logical measurement: call, parse, one reprompt on parse failure."""
    if op["family"] in ("deepseek", "anthropic"):
        # thinking-tier models spend thousands of reasoning tokens before
        # content; cap must cover both (amendment A1 pre-campaign: deepseek;
        # amendment A3 during collection: claude-sonnet-5 hit
        # stop_reason=max_tokens with [thinking, text] blocks on the longest
        # Study-1 eliciting/same-call prompts).
        max_out = max(max_out, 8000)
    for attempt in range(2):
        raw = L.call_model(
            op["model"],
            op["family"],
            system,
            user if attempt == 0 else user + "\n\nRespond with VALID JSON only.",
            role=arm,
            operation=record_key,
            phase=f"psm_{arm}",
            max_out=max_out,
        )
        try:
            payload = parser(raw)
            L.append_record(
                out_path,
                {
                    "record_key": record_key,
                    "arm": arm,
                    "operator": op["id"],
                    "model": op["model"],
                    "family": op["family"],
                    **meta,
                    "payload": payload,
                    "ts": now(),
                },
            )
            return
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            continue
    L.append_record(
        out_path,
        {
            "record_key": record_key,
            "arm": arm,
            "operator": op["id"],
            "model": op["model"],
            "family": op["family"],
            **meta,
            "failed": True,
            "ts": now(),
        },
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--arm",
        required=True,
        choices=[
            "smoke",
            "validate",
            "cohorts",
            "readings",
            "eliciting",
            "samecall",
            "all",
        ],
    )
    ap.add_argument("--ops", default=None, help="comma-separated operator ids")
    ap.add_argument("--categories", default=None)
    args = ap.parse_args()

    proto = L.load_protocol()
    all_ops = {o["id"]: o for o in proto["operators"] + proto["reserves"]}
    ops = [
        all_ops[i]
        for i in (
            args.ops.split(",") if args.ops else [o["id"] for o in proto["operators"]]
        )
    ]
    cats = args.categories.split(",") if args.categories else list(proto["categories"])
    personas = L.load_personas()["categories"]
    arms = (
        [args.arm]
        if args.arm != "all"
        else ["cohorts", "readings", "eliciting", "samecall"]
    )

    if args.arm == "smoke":
        # One cohort-validation call per operator: proves model IDs live and
        # parsers work before the campaign. Records go to smoke files, NOT
        # the campaign record set.
        c0 = personas["coffee_roasters"][0]
        for op in ops:
            out_path = L.DATA_DIR / f"smoke_{op['id']}.jsonl"
            collect_one(
                op,
                L.READ_SYSTEM,
                L.READ_PERSONA_USER_TMPL.format(persona=c0["persona_text"]),
                L.parse_dims,
                arm="smoke",
                record_key=f"smoke|{op['id']}",
                out_path=out_path,
                meta={"cohort_id": c0["cohort_id"]},
            )
            recs = L.load_records(out_path)
            status = "OK" if recs and not recs[-1].get("failed") else "FAILED"
            print(f"SMOKE {op['id']} ({op['model']}): {status}")
        return

    for op in ops:
        out_path = L.DATA_DIR / f"records_{op['id']}.jsonl"
        done = L.existing_keys(out_path)
        n_before = len(done)

        if "validate" in arms or args.arm == "validate":
            if op["id"] in proto["validation_operators"]:
                s1 = L.load_study1()
                for b in s1["brands"]:
                    for rep in range(proto["arms"]["validate_stimuli"]["replicates"]):
                        key = f"validate|{op['id']}|{b['brand_id']}|r{rep}"
                        if key in done:
                            continue
                        collect_one(
                            op,
                            L.READ_SYSTEM,
                            L.READ_PACK_USER_TMPL.format(
                                category=s1["category"], pack=L.pack_text(b)
                            ),
                            L.parse_dims,
                            arm="validate",
                            record_key=key,
                            out_path=out_path,
                            meta={
                                "brand": b["name"],
                                "brand_id": b["brand_id"],
                                "replicate": rep,
                            },
                        )

        if "cohorts" in arms:
            for cat, rows in personas.items():
                for c in rows:
                    key = f"cohorts|{op['id']}|{c['cohort_id']}|r0"
                    if key in done:
                        continue
                    collect_one(
                        op,
                        L.READ_SYSTEM,
                        L.READ_PERSONA_USER_TMPL.format(persona=c["persona_text"]),
                        L.parse_dims,
                        arm="cohorts",
                        record_key=key,
                        out_path=out_path,
                        meta={"category": cat, "cohort_id": c["cohort_id"]},
                    )

        for cat in cats:
            cfg = proto["categories"][cat]
            names, materials, label = category_materials(cat, proto)

            if "readings" in arms:
                s1 = L.load_study1() if cfg["mode"] == "pack" else None
                for bi, name in enumerate(names):
                    for rep in range(proto["arms"]["brand_readings"]["replicates"]):
                        key = f"readings|{op['id']}|{cat}|{name}|r{rep}"
                        if key in done:
                            continue
                        if cfg["mode"] == "pack":
                            user = L.READ_PACK_USER_TMPL.format(
                                category=label, pack=L.pack_text(s1["brands"][bi])
                            )
                        else:
                            user = L.READ_ELICITED_USER_TMPL.format(
                                brand=name, category=label
                            )
                        collect_one(
                            op,
                            L.READ_SYSTEM,
                            user,
                            L.parse_dims,
                            arm="readings",
                            record_key=key,
                            out_path=out_path,
                            meta={"category": cat, "brand": name, "replicate": rep},
                        )

            if "eliciting" in arms:
                for ci, c in enumerate(personas[cat]):
                    for rep in range(proto["arms"]["eliciting"]["replicates"]):
                        key = f"eliciting|{op['id']}|{c['cohort_id']}|r{rep}"
                        if key in done:
                            continue
                        current = names[(ci + rep) % len(names)]
                        collect_one(
                            op,
                            L.ELICIT_SYSTEM,
                            L.ELICIT_USER_TMPL.format(
                                persona=c["persona_text"],
                                category=label,
                                materials=materials,
                                current_brand=current,
                            ),
                            lambda raw, _n=names: L.parse_elicitation(raw, _n),
                            arm="eliciting",
                            record_key=key,
                            out_path=out_path,
                            meta={
                                "category": cat,
                                "cohort_id": c["cohort_id"],
                                "replicate": rep,
                                "current_brand": current,
                            },
                            max_out=3000,
                        )

            if "samecall" in arms:
                for c in personas[cat]:
                    key = f"samecall|{op['id']}|{c['cohort_id']}|r0"
                    if key in done:
                        continue
                    collect_one(
                        op,
                        L.SAMECALL_SYSTEM,
                        L.SAMECALL_USER_TMPL.format(
                            persona=c["persona_text"],
                            category=label,
                            materials=materials,
                        ),
                        lambda raw, _n=names: L.parse_samecall(raw, _n),
                        arm="samecall",
                        record_key=key,
                        out_path=out_path,
                        meta={"category": cat, "cohort_id": c["cohort_id"]},
                        max_out=4000,
                    )

        done_after = L.existing_keys(out_path)
        print(
            f"{op['id']}: +{len(done_after) - n_before} records (total {len(done_after)})"
        )


if __name__ == "__main__":
    main()
