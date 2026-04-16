#!/usr/bin/env python3
"""Retry failed Gemini calls for Experiment A.

Reads the existing JSONL, identifies failed Gemini records, and re-runs
only those calls. Appends new records to the same JSONL with
condition="retry_gemini".

Usage:
    uv run python exp_agentic_collapse_retry_gemini.py
"""

import json
import sys
import time
from pathlib import Path
from collections import defaultdict

# Import everything from the main experiment script
sys.path.insert(0, str(Path(__file__).parent))
from exp_agentic_collapse import (
    MODELS,
    BRANDS,
    CATEGORIES,
    DIMENSIONS,
    FALLBACK_COMPETITORS,
    LATIN_SQUARE_ORDERINGS,
    INTER_CALL_DELAY,
    SYSTEM_PROMPT_PIPELINE,
    call_api_multiturn,
    build_step1_user,
    build_step2_user,
    build_step3_user,
    build_control_prompt,
    parse_weights,
    parse_step2_weights,
    parse_step3_response,
    parse_step1_brands,
    _make_record,
    _write_record,
    _print_progress,
)


def main():
    base = Path(__file__).parent.parent
    jsonl_path = base / "L3_sessions" / "exp_agentic_collapse.jsonl"

    if not jsonl_path.exists():
        print("ERROR: JSONL not found")
        sys.exit(1)

    # Find failed Gemini records
    records = []
    with open(jsonl_path) as f:
        for line in f:
            records.append(json.loads(line))

    gemini_fails = [
        r for r in records
        if r["model_id"] == "gemini-2.5-flash"
        and not r["weights_valid"]
        and r["step"] != 1
    ]

    print(f"Found {len(gemini_fails)} failed Gemini records to retry")

    # Group pipeline fails by conversation_id
    conv_fails = defaultdict(list)
    for r in gemini_fails:
        if r["step"] == 0:
            # Control: retry independently
            conv_fails[r["conversation_id"]].append(r)
        else:
            conv_fails[r["conversation_id"]].append(r)

    retried = 0
    valid = 0

    for conv_id, fails in conv_fails.items():
        steps_failed = {r["step"] for r in fails}
        sample = fails[0]

        if 0 in steps_failed:
            # Retry control
            brand = sample["brand"]
            dim_order = sample["dim_order"]
            sys_p, usr_p = build_control_prompt(brand, dim_order)
            messages = [{"role": "user", "content": usr_p}]

            print(f"\nRetrying control: {brand}")
            try:
                raw, meta = call_api_multiturn("gemini", sys_p, messages)
                import datetime, uuid
                record = sample.copy()
                record["timestamp"] = datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()
                record["condition"] = "retry_gemini"
                record["raw_response"] = raw
                record.update(meta)
                weights = parse_weights(raw)
                if weights:
                    record["parsed_weights"] = weights
                    wsum = sum(weights.values())
                    record["weight_sum_raw"] = wsum
                    record["weights_valid"] = abs(wsum - 100) <= 5
                    if record["weights_valid"]:
                        valid += 1
                else:
                    record["weights_valid"] = False
                _write_record(jsonl_path, record)
                _print_progress(record, "Retry Ctrl")
                retried += 1
            except Exception as e:
                print(f"  ERROR: {e}")
            time.sleep(INTER_CALL_DELAY)

        elif 2 in steps_failed or 3 in steps_failed:
            # Retry full pipeline for this conversation
            brand = sample["brand"]
            rep = sample["repetition"]
            dim_order = sample["dim_order"]
            category = sample["category"]
            cat_info = CATEGORIES[brand]
            use_case = cat_info["use_case"]

            print(f"\nRetrying pipeline: {brand} rep={rep}")
            import datetime, uuid
            new_conv_id = str(uuid.uuid4())
            history = []

            # Step 1
            step1_user = build_step1_user(category)
            history.append({"role": "user", "content": step1_user})
            try:
                raw1, meta1 = call_api_multiturn(
                    "gemini", SYSTEM_PROMPT_PIPELINE, history, 1024
                )
                history.append({"role": "assistant", "content": raw1})
                step1_brands = parse_step1_brands(raw1)
                print(f"  Step 1: {len(step1_brands)} brands found")
            except Exception as e:
                print(f"  Step 1 ERROR: {e}")
                continue
            time.sleep(INTER_CALL_DELAY)

            competitors = [b for b in step1_brands if b.lower() != brand.lower()]
            competitor = competitors[0] if competitors else FALLBACK_COMPETITORS[brand]

            # Step 2
            step2_user = build_step2_user(brand, competitor, use_case, dim_order)
            history.append({"role": "user", "content": step2_user})
            try:
                raw2, meta2 = call_api_multiturn(
                    "gemini", SYSTEM_PROMPT_PIPELINE, history
                )
                history.append({"role": "assistant", "content": raw2})

                record2 = _make_record(
                    step=2, brand=brand, category=category,
                    model_name="gemini", rep=rep, dim_order=dim_order,
                    system_prompt=SYSTEM_PROMPT_PIPELINE,
                    user_prompt=step2_user,
                    conversation_id=new_conv_id,
                    conversation_history=list(history),
                )
                record2["condition"] = "retry_gemini"
                record2["competitor"] = competitor
                record2["raw_response"] = raw2
                record2.update(meta2)
                wa, wb = parse_step2_weights(raw2)
                if wa:
                    record2["parsed_weights"] = wa
                    wsum = sum(wa.values())
                    record2["weight_sum_raw"] = wsum
                    record2["weights_valid"] = abs(wsum - 100) <= 5
                    if record2["weights_valid"]:
                        valid += 1
                _write_record(jsonl_path, record2)
                _print_progress(record2, "Retry S2")
                retried += 1
            except Exception as e:
                print(f"  Step 2 ERROR: {e}")
                continue
            time.sleep(INTER_CALL_DELAY)

            # Step 3
            step3_user = build_step3_user(use_case, dim_order)
            history.append({"role": "user", "content": step3_user})
            try:
                raw3, meta3 = call_api_multiturn(
                    "gemini", SYSTEM_PROMPT_PIPELINE, history
                )

                record3 = _make_record(
                    step=3, brand=brand, category=category,
                    model_name="gemini", rep=rep, dim_order=dim_order,
                    system_prompt=SYSTEM_PROMPT_PIPELINE,
                    user_prompt=step3_user,
                    conversation_id=new_conv_id,
                    conversation_history=list(history),
                )
                record3["condition"] = "retry_gemini"
                record3["competitor"] = competitor
                record3["raw_response"] = raw3
                record3.update(meta3)
                rec, weights, reason = parse_step3_response(raw3)
                if weights:
                    record3["parsed_weights"] = weights
                    wsum = sum(weights.values())
                    record3["weight_sum_raw"] = wsum
                    record3["weights_valid"] = abs(wsum - 100) <= 5
                    if record3["weights_valid"]:
                        valid += 1
                record3["recommended_brand"] = rec or ""
                record3["recommendation_reason"] = reason or ""
                _write_record(jsonl_path, record3)
                _print_progress(record3, "Retry S3")
                retried += 1
            except Exception as e:
                print(f"  Step 3 ERROR: {e}")
            time.sleep(INTER_CALL_DELAY)

    print(f"\n--- Retry Complete ---")
    print(f"Retried: {retried}")
    print(f"New valid: {valid}")


if __name__ == "__main__":
    main()
