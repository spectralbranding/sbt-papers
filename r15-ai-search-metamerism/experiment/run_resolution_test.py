#!/usr/bin/env python3
"""R15 Brand Function Resolution Test for Local Brands

Tests whether providing a Brand Function specification resolves the
dimensional collapse observed for local brands in Run 3.

Design: same 5 local brand pairs, same 6 models, same weighted_recommendation
prompt -- but with Brand Function JSON prepended to the prompt context.
Compare DCI before (Run 3) vs after (this run) specification.

Usage:
    python run_resolution_test.py --smoke   # 1 pair, 1 run
    python run_resolution_test.py --live    # all pairs, 3 runs
"""

import json
import os
import sys
import time
import datetime
from pathlib import Path

# Import from main experiment script
sys.path.insert(0, str(Path(__file__).parent))
from ai_search_metamerism import (
    DIMENSIONS, DIMENSION_DESCRIPTIONS, LOCAL_BRAND_PAIRS,
    API_CALLERS, API_KEY_VARS, MODEL_IDS,
    parse_llm_json, parse_weights, call_with_retry,
    append_session_log, collect_experiment_metadata,
)
import numpy as np


def _dim_block() -> str:
    lines = []
    for dim in DIMENSIONS:
        lines.append(f"- {dim.capitalize()}: {DIMENSION_DESCRIPTIONS[dim]}")
    return "\n".join(lines)


def load_brand_specs() -> dict:
    """Load Brand Function specifications for local brands."""
    spec_path = Path(__file__).parent / "local_brand_specs.json"
    with open(spec_path) as f:
        specs = json.load(f)
    # Index by brand name
    return {s["brand"]: s for s in specs}


def make_spec_augmented_prompt(pair, specs: dict) -> str:
    """Create weighted recommendation prompt with Brand Function specs prepended."""
    spec_a = specs.get(pair.brand_a, {})
    spec_b = specs.get(pair.brand_b, {})

    spec_block = ""
    if spec_a:
        spec_block += f"\n--- Brand Function Specification: {pair.brand_a} ---\n"
        spec_block += json.dumps(spec_a.get("dimensions", {}), indent=2) + "\n"
    if spec_b:
        spec_block += f"\n--- Brand Function Specification: {pair.brand_b} ---\n"
        spec_block += json.dumps(spec_b.get("dimensions", {}), indent=2) + "\n"

    prompt = (
        "You are an AI shopping assistant helping a consumer choose between two brands.\n\n"
        f"Category: {pair.category}\n"
        f"Brands: {pair.brand_a} vs {pair.brand_b}\n\n"
        "You have access to detailed Brand Function specifications for both brands "
        "(behavioral commitments, cultural positioning, heritage, values). "
        "Use this information alongside your general knowledge.\n"
        f"{spec_block}\n"
        "Step 1: Recommend one brand.\n"
        "Step 2: Explain WHY by allocating 100 importance points across these 8 perception "
        "dimensions. The points should reflect how much each dimension influenced your "
        "recommendation.\n\n"
        "Dimensions:\n"
        f"{_dim_block()}\n\n"
        "Respond with ONLY valid JSON:\n"
        "{\n"
        '  "recommended_brand": "BrandName",\n'
        '  "weights": {\n'
        '    "semiotic": 15, "narrative": 10, "ideological": 5,\n'
        '    "experiential": 20, "social": 10, "economic": 25,\n'
        '    "cultural": 5, "temporal": 10\n'
        "  },\n"
        '  "reasoning": "1-2 sentence explanation"\n'
        "}\n\n"
        "The weights MUST sum to exactly 100."
    )
    return prompt


def run_resolution_test(smoke: bool = False, runs: int = 3):
    """Run Brand Function resolution test on local brands."""
    start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    specs = load_brand_specs()
    pairs = LOCAL_BRAND_PAIRS[:1] if smoke else LOCAL_BRAND_PAIRS
    actual_runs = 1 if smoke else runs

    print(f"\nR15 Brand Function Resolution Test")
    print(f"Mode: {'SMOKE' if smoke else 'LIVE'}")
    print(f"Brand pairs: {len(pairs)}")
    print(f"Runs: {actual_runs}")
    print(f"Specs loaded: {list(specs.keys())}")

    # Check Ollama
    try:
        import urllib.request
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2)
        os.environ["OLLAMA_AVAILABLE"] = "1"
        print("Ollama: available")
    except Exception:
        print("Ollama: not reachable (local models skipped)")

    # Select available models
    models = []
    for name, env_var in API_KEY_VARS.items():
        if os.environ.get(env_var):
            models.append(name)
            print(f"  [available] {name}")

    if not models:
        print("ERROR: No models available")
        sys.exit(1)

    # Log setup
    log_dir = Path(__file__).parent / "L3_sessions"
    log_dir.mkdir(exist_ok=True)
    log_path = str(log_dir / "run4_resolution.jsonl")

    total = len(pairs) * len(models) * actual_runs
    count = 0
    results = []

    for run in range(1, actual_runs + 1):
        for model_name in models:
            caller = API_CALLERS[model_name]
            for pair in pairs:
                prompt = make_spec_augmented_prompt(pair, specs)
                count += 1
                print(f"  [{count}/{total}] run={run} model={model_name} pair={pair.id}")

                t0 = time.time()
                try:
                    response = call_with_retry(caller, prompt, model_name)
                    latency = int((time.time() - t0) * 1000)
                    parsed = parse_llm_json(response)
                    weights = parse_weights(parsed)

                    record = {
                        "model": model_name,
                        "pair_id": pair.id,
                        "brand_a": pair.brand_a,
                        "brand_b": pair.brand_b,
                        "run": run,
                        "response": response,
                        "parsed": parsed,
                        "weights": weights,
                        "latency_ms": latency,
                        "condition": "spec_augmented",
                    }
                    results.append(record)

                    append_session_log(
                        log_path,
                        model=model_name,
                        model_id=MODEL_IDS.get(model_name, "?"),
                        prompt_type="weighted_recommendation_spec",
                        brand_pair=f"{pair.brand_a} vs {pair.brand_b}",
                        pair_id=pair.id,
                        dimension=None,
                        brand=None,
                        run=run,
                        prompt=prompt,
                        response=response,
                        parsed=parsed,
                        latency_ms=latency,
                    )

                    if weights:
                        dci = (weights.get("economic", 0) + weights.get("semiotic", 0)) / 100
                        print(f"    OK DCI={dci:.3f} ({latency}ms)")
                    else:
                        print(f"    OK (weights not parseable) ({latency}ms)")

                except Exception as e:
                    latency = int((time.time() - t0) * 1000)
                    print(f"    ERROR: {e} ({latency}ms)")
                    results.append({
                        "model": model_name, "pair_id": pair.id,
                        "run": run, "error": str(e),
                        "condition": "spec_augmented",
                    })

                time.sleep(0.5)

    # Analyze
    print(f"\nCompleted {count} calls. Analyzing...")

    # Compute DCI per model
    model_dcis = {}
    model_weights = {}
    for r in results:
        w = r.get("weights")
        if w:
            m = r["model"]
            if m not in model_dcis:
                model_dcis[m] = []
                model_weights[m] = {d: [] for d in DIMENSIONS}
            econ = w.get("economic", 0)
            semi = w.get("semiotic", 0)
            model_dcis[m].append((econ + semi) / 100.0)
            for d in DIMENSIONS:
                model_weights[m][d].append(w.get(d, 0))

    print("\n--- Resolution Test Results ---")
    print("\nDCI per model (WITH Brand Function specification):")
    print(f"  {'Model':<20} {'DCI (with spec)':<18} {'DCI (without, Run 3)':<22} {'Change'}")
    # Run 3 baseline DCIs (from experiment output)
    run3_dcis = {
        "claude": 0.302, "gpt": 0.363, "gemini": 0.327,
        "deepseek": 0.337, "qwen3_local": 0.400, "gemma4_local": 0.389,
    }
    for m in sorted(model_dcis.keys()):
        spec_dci = np.mean(model_dcis[m])
        baseline = run3_dcis.get(m, float("nan"))
        change = spec_dci - baseline
        print(f"  {m:<20} {spec_dci:<18.3f} {baseline:<22.3f} {change:+.3f}")

    # Aggregate
    all_spec_dcis = [d for dcis in model_dcis.values() for d in dcis]
    all_run3_dcis = [0.302]*18 + [0.363]*18 + [0.327]*18 + [0.337]*18 + [0.400]*18 + [0.389]*18
    # Use actual Run 3 per-observation data if available, else use means
    spec_mean = np.mean(all_spec_dcis) if all_spec_dcis else float("nan")
    run3_mean = 0.355  # aggregate from Run 3

    print(f"\n  Aggregate spec DCI:     {spec_mean:.3f}")
    print(f"  Aggregate Run 3 DCI:    {run3_mean:.3f}")
    print(f"  Baseline (uniform):     0.250")
    print(f"  Change:                 {spec_mean - run3_mean:+.3f}")

    # Weight profiles
    print("\nMean weight profiles (WITH specification):")
    print(f"  {'Dimension':<14} {'Baseline':>9}", end="")
    for m in sorted(model_weights.keys()):
        print(f" {m:>12}", end="")
    print()
    for dim in DIMENSIONS:
        print(f"  {dim:<14} {'12.5':>9}", end="")
        for m in sorted(model_weights.keys()):
            vals = model_weights[m][dim]
            print(f" {np.mean(vals):>12.1f}", end="")
        print()

    # Save results
    output = {
        "condition": "spec_augmented",
        "calls": len(results),
        "models": list(model_dcis.keys()),
        "model_dcis": {m: float(np.mean(v)) for m, v in model_dcis.items()},
        "aggregate_dci": float(spec_mean),
        "run3_baseline_dci": run3_mean,
        "model_weights": {
            m: {d: float(np.mean(v)) for d, v in dims.items()}
            for m, dims in model_weights.items()
        },
        "timestamp": start_time,
    }

    out_path = Path(__file__).parent.parent / "results_v4_resolution.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")
    print("Session log: " + log_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="R15 Brand Function Resolution Test")
    parser.add_argument("--smoke", action="store_true", help="1 pair, 1 run")
    parser.add_argument("--live", action="store_true", help="All pairs, 3 runs")
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()

    if not args.live and not args.smoke:
        args.smoke = True

    run_resolution_test(smoke=args.smoke, runs=args.runs)
