#!/usr/bin/env python3
"""Backfill failed Gemini records in exp_bf_format_v2.jsonl.

Reads the v2 JSONL, identifies records with weights_valid=false for
gemini-2.5-flash, re-calls Gemini with fixed config (max_output_tokens=8192,
no response_mime_type), and replaces the failed records in-place.

Usage:
    uv run python backfill_gemini.py
"""

import json
import time
from pathlib import Path

# Import the fixed Gemini caller + shared utilities from the main script
from exp_bf_format import (
    call_gemini, parse_weights, cosine_sim, compute_dci, estimate_cost,
    SYSTEM_PROMPT, CANONICAL_PROFILES, DIMENSIONS, INTER_CALL_DELAY,
)

JSONL_PATH = Path(__file__).parent.parent / "L3_sessions" / "exp_bf_format_v2.jsonl"


def main():
    # Load all records
    records = []
    with open(JSONL_PATH) as f:
        for line in f:
            records.append(json.loads(line))

    # Find failed Gemini records
    failed_indices = []
    for i, r in enumerate(records):
        if r.get("model_id") == "gemini-2.5-flash" and not r.get("weights_valid"):
            failed_indices.append(i)

    print(f"Found {len(failed_indices)} failed Gemini records to backfill")
    if not failed_indices:
        print("Nothing to do.")
        return

    success = 0
    for idx in failed_indices:
        r = records[idx]
        prompt = r.get("user_prompt") or r.get("prompt", "")
        brand = r["brand"]
        condition = r["condition"]
        rep = r["repetition"]

        print(f"  Backfilling: {brand} | {condition} | rep {rep}", end="", flush=True)

        try:
            raw_response, meta = call_gemini(prompt, system_prompt=SYSTEM_PROMPT)
            parsed = parse_weights(raw_response)

            canonical_cosine = None
            if parsed:
                canonical = CANONICAL_PROFILES[brand]
                observed = [parsed.get(dim, 0.0) for dim in DIMENSIONS]
                canonical_cosine = cosine_sim(observed, canonical)

            # Update record in place
            r["raw_response"] = raw_response
            r["parsed_weights"] = parsed
            r["weights_valid"] = parsed is not None
            r["weight_sum_raw"] = round(sum(parsed.values()), 2) if parsed else 0.0
            r["dci"] = round(compute_dci(parsed), 4) if parsed else None
            r["canonical_cosine"] = round(canonical_cosine, 4) if canonical_cosine is not None else None
            r["response_time_ms"] = meta.get("response_time_ms", 0)
            r["token_count_input"] = meta.get("token_count_input", 0)
            r["token_count_output"] = meta.get("token_count_output", 0)
            r["api_cost_usd"] = round(estimate_cost("gemini-2.5-flash", meta.get("token_count_input", 0), meta.get("token_count_output", 0)), 6)

            if parsed:
                success += 1
                print(f" | OK cos={canonical_cosine:.3f}")
            else:
                print(f" | STILL FAILED (parse error)")

        except Exception as e:
            print(f" | ERROR: {e}")

        time.sleep(INTER_CALL_DELAY)

    # Write back
    with open(JSONL_PATH, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\nBackfill complete: {success}/{len(failed_indices)} recovered")
    print(f"Updated {JSONL_PATH}")


if __name__ == "__main__":
    main()
