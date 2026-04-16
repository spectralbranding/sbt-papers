#!/usr/bin/env python3
"""Supplementary Gemma 4 run for Experiment A.

Runs the same pipeline + control design using local Gemma 4 27B via Ollama.
Appends to the existing JSONL.

Usage:
    uv run python exp_agentic_collapse_gemma4.py --smoke
    uv run python exp_agentic_collapse_gemma4.py --live
"""

import argparse
import json
import os
import random
import sys
import time
import uuid
from pathlib import Path

# Ensure Ollama is detected as available
os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

sys.path.insert(0, str(Path(__file__).parent))
from exp_agentic_collapse import (
    BRANDS,
    CATEGORIES,
    INTER_CALL_DELAY,
    LATIN_SQUARE_ORDERINGS,
    RANDOM_SEED,
    TEMPERATURE,
    run_pipeline,
    run_control,
    _write_record,
)


def main():
    parser = argparse.ArgumentParser(description="Gemma 4 supplementary run")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    if not args.smoke and not args.live:
        parser.print_help()
        sys.exit(1)

    # Verify Ollama is running
    import urllib.request
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    try:
        with urllib.request.urlopen(f"{host}/api/tags", timeout=5) as resp:
            models = json.loads(resp.read().decode())
            names = [m["name"] for m in models.get("models", [])]
            if not any("gemma4" in n for n in names):
                print(f"ERROR: gemma4 not found in Ollama. Available: {names}")
                sys.exit(1)
            print(f"Ollama OK. Gemma 4 available.")
    except Exception as e:
        print(f"ERROR: Cannot reach Ollama at {host}: {e}")
        sys.exit(1)

    base = Path(__file__).parent.parent
    jsonl_path = base / "L3_sessions" / "exp_agentic_collapse.jsonl"

    mode = "smoke" if args.smoke else "live"
    rng = random.Random(RANDOM_SEED + 100)  # different seed from main run

    if mode == "smoke":
        brands = ["Patagonia"]
        reps = 1
    else:
        brands = BRANDS
        reps = 3

    # Build call lists
    pipeline_calls = []
    control_calls = []
    idx = 1000  # offset to avoid colliding with main run indices

    for brand in brands:
        for rep in range(1, reps + 1):
            pipeline_calls.append({"brand": brand, "model": "gemma4", "rep": rep, "idx": idx})
            idx += 1
            control_calls.append({"brand": brand, "model": "gemma4", "rep": rep, "idx": idx})
            idx += 1

    rng.shuffle(pipeline_calls)
    rng.shuffle(control_calls)

    total = len(pipeline_calls) * 3 + len(control_calls)
    print(f"\nGemma 4 supplementary run ({mode})")
    print(f"Pipeline: {len(pipeline_calls)} (x3 = {len(pipeline_calls)*3})")
    print(f"Control: {len(control_calls)}")
    print(f"Total calls: {total}")
    print(f"Appending to: {jsonl_path}\n")

    all_records = []
    total_cost = 0.0
    errors = 0

    print("=== Control Phase ===")
    for i, call in enumerate(control_calls):
        print(f"\n[Control {i+1}/{len(control_calls)}]")
        rec = run_control(call["brand"], call["model"], call["rep"], call["idx"], jsonl_path)
        all_records.append(rec)
        if not rec["weights_valid"]:
            errors += 1

    print("\n=== Pipeline Phase ===")
    for i, call in enumerate(pipeline_calls):
        print(f"\n[Pipeline {i+1}/{len(pipeline_calls)}] {call['brand']} / gemma4 / rep {call['rep']}")
        recs = run_pipeline(call["brand"], call["model"], call["rep"], call["idx"], jsonl_path)
        all_records.extend(recs)
        for r in recs:
            if r["step"] != 1 and not r["weights_valid"]:
                errors += 1

    valid = sum(1 for r in all_records if r["weights_valid"])
    weight_bearing = sum(1 for r in all_records if r["step"] != 1)

    print(f"\n{'='*60}")
    print("Gemma 4 supplementary run -- COMPLETE")
    print(f"{'='*60}")
    print(f"Total records: {len(all_records)}")
    print(f"Valid weights: {valid}/{weight_bearing} ({100*valid/max(weight_bearing,1):.1f}%)")
    print(f"Errors: {errors}")


if __name__ == "__main__":
    main()
