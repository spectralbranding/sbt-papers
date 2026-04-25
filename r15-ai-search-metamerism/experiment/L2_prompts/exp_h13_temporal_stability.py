#!/usr/bin/env python3
"""Experiment H13: Temporal Stability Across Model Versions.

Tests whether successive versions of the same model family produce
significantly different brand perception profiles. Compares old vs new
model versions within 4 families (DeepSeek, Llama, Qwen, Gemini) using
the standard R15 weighted_recommendation prompt.

Protocol: L0_specification/EXP_H13_TEMPORAL_STABILITY_PROTOCOL.md
Paper: R15 v3.0 Section 6 direction (e)

Design:
    4 model pairs x 5 brand pairs x 3 reps = 120 calls

Usage:
    uv run python exp_h13_temporal_stability.py --dry-run   # print plan, no calls
    uv run python exp_h13_temporal_stability.py --smoke     # 2 calls, verify setup
    uv run python exp_h13_temporal_stability.py --live      # 120 calls, full run
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TEMPERATURE = 0.7
MAX_TOKENS = 512
RANDOM_SEED = 42
INTER_CALL_DELAY = 3.0  # seconds between API calls

DIMENSIONS = [
    "Semiotic",
    "Narrative",
    "Ideological",
    "Experiential",
    "Social",
    "Economic",
    "Cultural",
    "Temporal",
]

# Latin-square balanced dimension orderings (8 cyclic rotations)
LATIN_SQUARE_ORDERINGS = [DIMENSIONS[i:] + DIMENSIONS[:i] for i in range(8)]

# ---------------------------------------------------------------------------
# Model Pairs
# ---------------------------------------------------------------------------

# Each entry: (model_short_old, model_short_new) -> both keys into MODELS dict
MODEL_PAIRS = [
    ("deepseek_v3", "deepseek_r1"),
    ("llama31", "llama33"),
    ("qwen25", "qwen3"),
    ("gemini20", "gemini25"),
]

# family label for each model short name
MODEL_FAMILY = {
    "deepseek_v3": "deepseek",
    "deepseek_r1": "deepseek",
    "llama31": "llama",
    "llama33": "llama",
    "qwen25": "qwen",
    "qwen3": "qwen",
    "gemini20": "gemini",
    "gemini25": "gemini",
}

MODEL_GENERATION = {
    "deepseek_v3": "old",
    "deepseek_r1": "new",
    "llama31": "old",
    "llama33": "new",
    "qwen25": "old",
    "qwen3": "new",
    "gemini20": "old",
    "gemini25": "new",
}

MODELS = {
    "deepseek_v3": {
        "model_id": "deepseek-chat",
        "provider": "deepseek",
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "input_cost_per_m": 0.27,
        "output_cost_per_m": 1.10,
    },
    "deepseek_r1": {
        "model_id": "deepseek-reasoner",
        "provider": "deepseek",
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "input_cost_per_m": 0.55,
        "output_cost_per_m": 2.19,
    },
    "llama31": {
        "model_id": "llama-3.1-70b-versatile",
        "provider": "groq",
        "api_key_env": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "input_cost_per_m": 0.05,
        "output_cost_per_m": 0.08,
    },
    "llama33": {
        "model_id": "llama-3.3-70b-versatile",
        "provider": "groq",
        "api_key_env": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "input_cost_per_m": 0.05,
        "output_cost_per_m": 0.08,
    },
    "qwen25": {
        "model_id": "qwen-2.5-72b-instruct",
        "provider": "cerebras",
        "api_key_env": "CEREBRAS_API_KEY",
        "base_url": "https://api.cerebras.ai/v1",
        "input_cost_per_m": 0.60,
        "output_cost_per_m": 0.60,
    },
    "qwen3": {
        "model_id": "qwen-3-235b-a22b-instruct-2507",
        "provider": "cerebras",
        "api_key_env": "CEREBRAS_API_KEY",
        "base_url": "https://api.cerebras.ai/v1",
        "input_cost_per_m": 0.60,
        "output_cost_per_m": 0.60,
    },
    "gemini20": {
        "model_id": "gemini-2.0-flash",
        "provider": "google",
        "api_key_env": "GOOGLE_API_KEY",
        "base_url": None,
        "input_cost_per_m": 0.10,
        "output_cost_per_m": 0.40,
    },
    "gemini25": {
        "model_id": "gemini-2.5-flash",
        "provider": "google",
        "api_key_env": "GOOGLE_API_KEY",
        "base_url": None,
        "input_cost_per_m": 0.15,
        "output_cost_per_m": 0.60,
    },
}

# ---------------------------------------------------------------------------
# Brand Pairs (R15 global set)
# ---------------------------------------------------------------------------

BRAND_PAIRS = [
    {
        "pair_id": "luxury_heritage",
        "brand_pair": "Hermes vs Coach",
        "brand_a": "Hermes",
        "brand_b": "Coach",
    },
    {
        "pair_id": "purpose_driven",
        "brand_pair": "Patagonia vs Columbia",
        "brand_a": "Patagonia",
        "brand_b": "Columbia",
    },
    {
        "pair_id": "premium_tech",
        "brand_pair": "Apple vs Samsung",
        "brand_a": "Apple",
        "brand_b": "Samsung",
    },
    {
        "pair_id": "artisanal_food",
        "brand_pair": "Erewhon vs Whole Foods",
        "brand_a": "Erewhon",
        "brand_b": "Whole Foods",
    },
    {
        "pair_id": "auto_disruption",
        "brand_pair": "Tesla vs Mercedes",
        "brand_a": "Tesla",
        "brand_b": "Mercedes",
    },
]

# ---------------------------------------------------------------------------
# Prompt Construction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = "You are evaluating brand perception for market research."


def build_prompt(brand_a: str, brand_b: str, dim_order: list) -> str:
    """Build the weighted_recommendation prompt with given dimension ordering."""
    dim_json = ", ".join(f'"{d}": <number>' for d in dim_order)
    return (
        f"Compare {brand_a} and {brand_b}. Allocate 100 importance points "
        f"across these eight brand perception dimensions. Points must sum to 100. "
        f"Respond ONLY in this exact JSON format with no additional text:\n"
        f"{{{dim_json}}}"
    )


# ---------------------------------------------------------------------------
# API Callers
# ---------------------------------------------------------------------------


def _sha256_prefix(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:16]


def _compute_cost(inp_tokens: int, out_tokens: int, model_short: str) -> float:
    cfg = MODELS[model_short]
    return round(
        inp_tokens * cfg["input_cost_per_m"] / 1_000_000
        + out_tokens * cfg["output_cost_per_m"] / 1_000_000,
        6,
    )


def call_api(model_short: str, prompt: str) -> tuple[str, dict[str, Any]]:
    """Call the model API with exponential backoff on rate limits.

    Returns (response_text, metadata_dict).
    """
    cfg = MODELS[model_short]
    provider = cfg["provider"]

    for attempt in range(5):
        try:
            text, meta = _call_provider(provider, cfg, prompt)
            meta["api_cost_usd"] = _compute_cost(
                meta["token_count_input"], meta["token_count_output"], model_short
            )
            return text, meta
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str or "limit" in err_str:
                backoff = [5, 10, 20, 60, 120][attempt]
                print(
                    f"    Rate limited ({model_short}), backing off {backoff}s..."
                )
                time.sleep(backoff)
            else:
                raise
    raise RuntimeError(
        f"Rate limit exceeded after 5 retries for {model_short}"
    )


def _call_provider(
    provider: str, cfg: dict, prompt: str
) -> tuple[str, dict[str, Any]]:
    """Dispatch to the correct provider's API."""
    if provider == "google":
        return _call_google(cfg["model_id"], prompt)
    else:
        # DeepSeek, Groq, Cerebras all expose an OpenAI-compatible endpoint
        return _call_openai_compat(
            cfg["model_id"],
            cfg["base_url"],
            os.environ[cfg["api_key_env"]],
            prompt,
        )


def _call_openai_compat(
    model_id: str,
    base_url: str,
    api_key: str,
    prompt: str,
) -> tuple[str, dict[str, Any]]:
    """Call any OpenAI-compatible endpoint (DeepSeek, Groq, Cerebras)."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    t0 = time.time()
    response = client.chat.completions.create(
        model=model_id,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    usage = response.usage
    text = response.choices[0].message.content or ""
    # Strip <think>...</think> blocks (deepseek-reasoner emits these)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    return text, {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
    }


def _call_google(model_id: str, prompt: str) -> tuple[str, dict[str, Any]]:
    """Call Google Gemini via google-genai SDK."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    t0 = time.time()
    gemini_max = max(MAX_TOKENS, 1024)
    response = client.models.generate_content(
        model=model_id,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE,
            max_output_tokens=gemini_max,
            system_instruction=SYSTEM_PROMPT,
        ),
    )
    try:
        text = response.text
    except Exception:
        if response.candidates:
            text = response.candidates[0].content.parts[0].text
        else:
            raise ValueError("Gemini returned no usable response")
    elapsed_ms = int((time.time() - t0) * 1000)
    usage = getattr(response, "usage_metadata", None)
    inp_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
    out_tokens = getattr(usage, "candidates_token_count", 0) if usage else 0
    return text, {
        "response_time_ms": elapsed_ms,
        "token_count_input": inp_tokens,
        "token_count_output": out_tokens,
    }


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------


def parse_weights(raw: str) -> Optional[dict[str, float]]:
    """Extract 8-dimension weight dict from JSON response."""
    # Strip markdown code fences if present
    cleaned = re.sub(r"```(?:json)?\s*", "", raw)
    cleaned = re.sub(r"```\s*", "", cleaned)
    match = re.search(r"\{[^{}]*\}", cleaned, re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError:
        return None
    weights = {}
    for dim in DIMENSIONS:
        val = data.get(dim)
        if val is None:
            # Case-insensitive fallback
            for k, v in data.items():
                if k.lower() == dim.lower():
                    val = v
                    break
        if val is None:
            return None
        try:
            weights[dim] = float(val)
        except (ValueError, TypeError):
            return None
    return weights


# ---------------------------------------------------------------------------
# Record Construction
# ---------------------------------------------------------------------------


def make_record(
    model_short: str,
    pair_info: dict,
    rep: int,
    dim_order: list,
    prompt: str,
) -> dict:
    """Create a base JSONL record (fields filled in after API call)."""
    cfg = MODELS[model_short]
    return {
        # Required fields (EXPERIMENT_DATA_STANDARD.md)
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model": model_short,
        "model_id": cfg["model_id"],
        "prompt_type": "temporal_stability",
        "prompt": prompt,
        # Recommended fields
        "response": None,
        "parsed": None,
        "latency_ms": None,
        "tokens_in": None,
        "tokens_out": None,
        "error": None,
        "temperature": TEMPERATURE,
        "run": rep,
        # Experiment-specific fields
        "model_family": MODEL_FAMILY[model_short],
        "model_generation": MODEL_GENERATION[model_short],
        "brand_pair": pair_info["brand_pair"],
        "pair_id": pair_info["pair_id"],
        "brand_a": pair_info["brand_a"],
        "brand_b": pair_info["brand_b"],
        "dim_order": dim_order,
        "parsed_weights": None,
        "weights_valid": False,
        "weight_sum_raw": None,
        "api_cost_usd": 0.0,
    }


def write_record(jsonl_path: Path, record: dict) -> None:
    """Append one record to the JSONL file."""
    with open(jsonl_path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def print_status(record: dict) -> None:
    """Print one-line progress summary."""
    status = "OK" if record["weights_valid"] else "FAIL"
    cost = record.get("api_cost_usd", 0)
    lat = record.get("latency_ms") or 0
    print(
        f"  {record['model_family']:>8} {record['model_generation']:>3} | "
        f"{record['pair_id']:<20} rep={record['run']} -> {status} "
        f"({lat}ms, ${cost:.5f})"
    )


# ---------------------------------------------------------------------------
# Call Runner
# ---------------------------------------------------------------------------


def run_call(
    model_short: str,
    pair_info: dict,
    rep: int,
    call_idx: int,
    jsonl_path: Path,
    dry_run: bool = False,
) -> dict:
    """Execute one API call and write the record.

    In dry_run mode, prints the plan without making any API call.
    """
    dim_order = LATIN_SQUARE_ORDERINGS[call_idx % 8]
    prompt = build_prompt(pair_info["brand_a"], pair_info["brand_b"], dim_order)
    record = make_record(model_short, pair_info, rep, dim_order, prompt)

    if dry_run:
        cfg = MODELS[model_short]
        print(
            f"  [DRY RUN] {model_short:>12} ({cfg['model_id']}) | "
            f"{pair_info['pair_id']:<20} rep={rep} | "
            f"dim_order[0]={dim_order[0]}"
        )
        return record

    try:
        raw, meta = call_api(model_short, prompt)
        record["response"] = raw
        record["latency_ms"] = meta["response_time_ms"]
        record["tokens_in"] = meta["token_count_input"]
        record["tokens_out"] = meta["token_count_output"]
        record["api_cost_usd"] = meta["api_cost_usd"]
        record["error"] = None

        weights = parse_weights(raw)
        if weights:
            record["parsed_weights"] = weights
            record["parsed"] = weights
            wsum = sum(weights.values())
            record["weight_sum_raw"] = wsum
            record["weights_valid"] = abs(wsum - 100) <= 5
        else:
            record["error"] = "parse_failed"

    except Exception as e:
        record["response"] = f"ERROR: {type(e).__name__}: {e}"
        record["error"] = f"{type(e).__name__}: {e}"

    write_record(jsonl_path, record)
    print_status(record)
    return record


# ---------------------------------------------------------------------------
# Main Experiment Runner
# ---------------------------------------------------------------------------


def build_call_plan(models_available: list[str], reps: int) -> list[dict]:
    """Build the ordered list of calls to make.

    Interleaves old and new versions within each pair to minimise
    systematic time effects.
    """
    calls = []
    call_idx = 0
    for old_short, new_short in MODEL_PAIRS:
        for pair_info in BRAND_PAIRS:
            for rep in range(1, reps + 1):
                for model_short in (old_short, new_short):
                    if model_short in models_available:
                        calls.append(
                            {
                                "model_short": model_short,
                                "pair_info": pair_info,
                                "rep": rep,
                                "call_idx": call_idx,
                            }
                        )
                    call_idx += 1
    return calls


def run_experiment(mode: str = "live") -> None:
    """Execute the H13 temporal stability experiment."""
    output_dir = (
        Path(__file__).parent.parent / "L3_sessions"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "exp_h13_temporal_stability.jsonl"

    dry_run = mode == "dry-run"

    if not dry_run and jsonl_path.exists():
        backup = jsonl_path.with_suffix(".jsonl.bak")
        jsonl_path.rename(backup)
        print(f"Backed up existing data to {backup.name}")

    # Check which models are available
    available = []
    skipped = []
    for model_short, cfg in MODELS.items():
        env_val = os.environ.get(cfg["api_key_env"])
        if env_val:
            available.append(model_short)
        else:
            skipped.append((model_short, cfg["api_key_env"]))

    for model_short, env_var in skipped:
        print(f"  Skipping {model_short}: {env_var} not set")

    if not available and not dry_run:
        print("ERROR: No models available. Set API keys.")
        sys.exit(1)

    if dry_run:
        # In dry-run, include all models
        available = list(MODELS.keys())

    print(f"Available models ({len(available)}): {available}")

    # Determine reps and call set by mode
    if mode == "smoke":
        # One pair, one family, one rep each (old + new = 2 calls)
        smoke_pair = [BRAND_PAIRS[0]]  # luxury_heritage
        smoke_models = []
        for old_s, new_s in MODEL_PAIRS[:1]:  # deepseek pair only
            for m in (old_s, new_s):
                if m in available:
                    smoke_models.append(m)
        calls = []
        call_idx = 0
        for pair_info in smoke_pair:
            for model_short in smoke_models:
                calls.append(
                    {
                        "model_short": model_short,
                        "pair_info": pair_info,
                        "rep": 1,
                        "call_idx": call_idx,
                    }
                )
                call_idx += 1
    else:
        reps = 3
        calls = build_call_plan(available, reps)

    total = len(calls)
    print(f"\nCalls planned: {total}")
    if not dry_run:
        est_min = total * (INTER_CALL_DELAY + 2) / 60
        print(f"Estimated time: ~{est_min:.0f} min")
    print(f"Output: {jsonl_path}\n")

    if dry_run:
        print("=== DRY RUN: call plan ===")
        for c in calls:
            run_call(
                c["model_short"],
                c["pair_info"],
                c["rep"],
                c["call_idx"],
                jsonl_path,
                dry_run=True,
            )
        print(f"\nTotal calls that would be made: {total}")
        return

    all_records = []
    total_cost = 0.0
    errors = 0

    for i, c in enumerate(calls):
        print(
            f"\n[{i+1}/{total}] {c['model_short']} | "
            f"{c['pair_info']['pair_id']} | rep {c['rep']}"
        )
        rec = run_call(
            c["model_short"],
            c["pair_info"],
            c["rep"],
            c["call_idx"],
            jsonl_path,
            dry_run=False,
        )
        all_records.append(rec)
        total_cost += rec.get("api_cost_usd", 0)
        if not rec["weights_valid"]:
            errors += 1
        time.sleep(INTER_CALL_DELAY)

    valid = sum(1 for r in all_records if r["weights_valid"])
    print(f"\n{'='*60}")
    print("Experiment H13: Temporal Stability -- COMPLETE")
    print(f"{'='*60}")
    print(f"Total records: {len(all_records)}")
    print(
        f"Valid weights: {valid}/{len(all_records)} "
        f"({100*valid/max(len(all_records),1):.1f}%)"
    )
    print(f"Parse/API errors: {errors}")
    print(f"Total cost: ${total_cost:.4f}")
    print(f"Output: {jsonl_path}")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Experiment H13: Temporal Stability Across Model Versions"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print call plan without making any API calls",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Smoke test: 2 calls (1 pair, deepseek old+new, 1 rep)",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Full run: 120 calls (4 pairs x 5 brand pairs x 3 reps)",
    )
    args = parser.parse_args()

    if not any([args.dry_run, args.smoke, args.live]):
        parser.print_help()
        sys.exit(1)

    if args.dry_run:
        mode = "dry-run"
    elif args.smoke:
        mode = "smoke"
    else:
        mode = "live"

    print(f"Experiment H13: Temporal Stability ({mode})")
    print(f"Temperature: {TEMPERATURE}")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Inter-call delay: {INTER_CALL_DELAY}s")
    print()
    run_experiment(mode=mode)


if __name__ == "__main__":
    main()
