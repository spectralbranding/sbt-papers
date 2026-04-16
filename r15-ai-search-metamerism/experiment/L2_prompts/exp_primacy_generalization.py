#!/usr/bin/env python3
"""Experiment E: Primacy Effect Generalization.

Tests whether the serial position of a dimension in the prompt biases
weight allocation, and whether this effect generalizes across response
formats (JSON allocation, Likert 1-5, ranking 1-8, natural language).

Protocol: L0_specification/EXP_PRIMACY_GENERALIZATION_PROTOCOL.md
Paper: R15 extension or PRISM instrument paper

Usage:
    uv run python exp_primacy_generalization.py --smoke   # ~20 calls, verify setup
    uv run python exp_primacy_generalization.py --live    # ~2400 calls, full run
"""

import argparse
import datetime
import hashlib
import json
import os
import random
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
MAX_TOKENS_NL = 1024  # NL format needs more room for explanations
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

CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

BRANDS = list(CANONICAL_PROFILES.keys())

RESPONSE_FORMATS = ["json", "likert", "ranking", "nl"]

# Latin-square balanced dimension orderings (8 cyclic rotations)
LATIN_SQUARE_ORDERINGS = []
for i in range(8):
    LATIN_SQUARE_ORDERINGS.append(DIMENSIONS[i:] + DIMENSIONS[:i])

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

MODELS = {
    "claude": {
        "model_id": "claude-haiku-4-5-20251001",
        "provider": "anthropic",
        "api_key_env": "ANTHROPIC_API_KEY",
        "input_cost_per_m": 0.80,
        "output_cost_per_m": 4.00,
    },
    "gpt": {
        "model_id": "gpt-4o-mini",
        "provider": "openai",
        "api_key_env": "OPENAI_API_KEY",
        "input_cost_per_m": 0.15,
        "output_cost_per_m": 0.60,
    },
    "gemini": {
        "model_id": "gemini-2.5-flash",
        "provider": "google",
        "api_key_env": "GOOGLE_API_KEY",
        "input_cost_per_m": 0.15,
        "output_cost_per_m": 0.60,
    },
    "deepseek": {
        "model_id": "deepseek-chat",
        "provider": "deepseek",
        "api_key_env": "DEEPSEEK_API_KEY",
        "input_cost_per_m": 0.27,
        "output_cost_per_m": 1.10,
    },
    "grok": {
        "model_id": "grok-4-1-fast-non-reasoning",
        "provider": "xai",
        "api_key_env": "GROK_API_KEY",
        "input_cost_per_m": 3.00,
        "output_cost_per_m": 15.00,
    },
}


# ---------------------------------------------------------------------------
# API Callers (same pattern as exp_agentic_collapse.py)
# ---------------------------------------------------------------------------


def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:16]


def _compute_cost(inp_tokens: int, out_tokens: int, model_name: str) -> float:
    cfg = MODELS[model_name]
    return round(
        inp_tokens * cfg["input_cost_per_m"] / 1_000_000
        + out_tokens * cfg["output_cost_per_m"] / 1_000_000,
        6,
    )


def call_api(
    model_name: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = MAX_TOKENS,
) -> tuple[str, dict[str, Any]]:
    """Unified API caller with exponential backoff on 429."""
    cfg = MODELS[model_name]
    provider = cfg["provider"]

    for attempt in range(5):
        try:
            text, meta = _call_provider(
                provider, cfg["model_id"], system_prompt, user_prompt, max_tokens
            )
            meta["api_cost_usd"] = _compute_cost(
                meta["token_count_input"], meta["token_count_output"], model_name
            )
            return text, meta
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str:
                backoff = [5, 10, 20, 60, 120][attempt]
                print(f"    Rate limited ({model_name}), backing off {backoff}s...")
                time.sleep(backoff)
            else:
                raise
    raise RuntimeError(f"Rate limit exceeded after 5 retries for {model_name}")


def _call_provider(
    provider: str,
    model_id: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
) -> tuple[str, dict[str, Any]]:
    if provider == "anthropic":
        return _call_anthropic(model_id, system_prompt, user_prompt, max_tokens)
    elif provider == "openai":
        return _call_openai(
            model_id, system_prompt, user_prompt, max_tokens, None, None
        )
    elif provider == "google":
        return _call_google(model_id, system_prompt, user_prompt, max_tokens)
    elif provider == "deepseek":
        return _call_openai(
            model_id,
            system_prompt,
            user_prompt,
            max_tokens,
            os.environ["DEEPSEEK_API_KEY"],
            "https://api.deepseek.com",
        )
    elif provider == "xai":
        return _call_openai(
            model_id,
            system_prompt,
            user_prompt,
            max_tokens,
            os.environ["GROK_API_KEY"],
            "https://api.x.ai/v1",
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")


def _call_anthropic(
    model_id: str, system_prompt: str, user_prompt: str, max_tokens: int
) -> tuple[str, dict[str, Any]]:
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    t0 = time.time()
    message = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        temperature=TEMPERATURE,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    return message.content[0].text, {
        "response_time_ms": elapsed_ms,
        "token_count_input": message.usage.input_tokens,
        "token_count_output": message.usage.output_tokens,
    }


def _call_openai(
    model_id: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    api_key: Optional[str],
    base_url: Optional[str],
) -> tuple[str, dict[str, Any]]:
    from openai import OpenAI

    kwargs = {}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    client = OpenAI(**kwargs)
    t0 = time.time()
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tokens,
        temperature=TEMPERATURE,
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    usage = response.usage
    content = response.choices[0].message.content or ""
    # Strip thinking tags if present
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    return content, {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
    }


def _call_google(
    model_id: str, system_prompt: str, user_prompt: str, max_tokens: int
) -> tuple[str, dict[str, Any]]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    # Gemini 2.5 Flash uses thinking tokens that eat into max_output_tokens.
    # Set high limit so thinking doesn't truncate the actual response.
    gemini_max = max(max_tokens, 8192)
    t0 = time.time()
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=gemini_max,
                response_mime_type="application/json",
                system_instruction=system_prompt,
            ),
        )
        text = response.text
    except Exception:
        response = client.models.generate_content(
            model=model_id,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=gemini_max,
                system_instruction=system_prompt,
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
# Prompt Construction
# ---------------------------------------------------------------------------


def get_dim_json_weights(dim_order: list[str]) -> str:
    """JSON template for weight allocation (sum to 100)."""
    return "{" + ", ".join(f'"{d}": <weight>' for d in dim_order) + "}"


def get_dim_json_likert(dim_order: list[str]) -> str:
    """JSON template for Likert 1-5 ratings."""
    return "{" + ", ".join(f'"{d}": <1-5>' for d in dim_order) + "}"


def get_dim_json_ranking(dim_order: list[str]) -> str:
    """JSON template for ranking 1-8."""
    return "{" + ", ".join(f'"{d}": <rank 1-8>' for d in dim_order) + "}"


SYSTEM_PROMPT = "You are evaluating brand perception."


def build_json_prompt(brand: str, dim_order: list[str]) -> str:
    """JSON allocation format (R15 standard). Weights sum to 100."""
    dim_json = get_dim_json_weights(dim_order)
    return (
        f"Evaluate the brand {brand} by allocating importance weights across "
        f"eight dimensions of brand perception. The weights must sum to 100. "
        f"Respond in this exact JSON format:\n{dim_json}"
    )


def build_likert_prompt(brand: str, dim_order: list[str]) -> str:
    """Likert 1-5 format. All 8 dimensions simultaneously, Latin-square ordered."""
    dim_json = get_dim_json_likert(dim_order)
    return (
        f"Evaluate the brand {brand} on eight dimensions of brand perception. "
        f"Rate each dimension on a scale of 1-5 "
        f"(1 = not at all important, 5 = extremely important). "
        f"Respond in this exact JSON format:\n{dim_json}"
    )


def build_ranking_prompt(brand: str, dim_order: list[str]) -> str:
    """Ranking format. Rank 1 (most important) to 8 (least important)."""
    dim_json = get_dim_json_ranking(dim_order)
    return (
        f"Evaluate the brand {brand} by ranking these eight dimensions of brand "
        f"perception from most important (1) to least important (8). "
        f"Each rank must be unique. "
        f"Respond in this exact JSON format:\n{dim_json}"
    )


def build_nl_prompt(brand: str, dim_order: list[str]) -> str:
    """Natural language format with estimated percentage weights."""
    dim_list = ", ".join(dim_order)
    dim_json = get_dim_json_weights(dim_order)
    return (
        f"Evaluate the brand {brand} across these eight dimensions of brand "
        f"perception: {dim_list}. "
        f"For each dimension, explain its importance to this brand and estimate "
        f"a percentage weight (all weights should sum to approximately 100). "
        f"Respond in JSON format:\n{dim_json}"
    )


PROMPT_BUILDERS = {
    "json": build_json_prompt,
    "likert": build_likert_prompt,
    "ranking": build_ranking_prompt,
    "nl": build_nl_prompt,
}


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------


def parse_json_weights(raw: str, dim_order: list[str]) -> Optional[dict[str, float]]:
    """Parse JSON weights (sum-to-100 or NL format)."""
    text = raw.strip()
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```\s*$", "", text).strip()

    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    end = start
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    try:
        data = json.loads(text[start:end])
    except json.JSONDecodeError:
        return None

    if "weights" in data and isinstance(data["weights"], dict):
        data = data["weights"]

    result = {}
    for dim in dim_order:
        found = False
        for key, val in data.items():
            if dim.lower() in key.lower():
                # Handle nested objects like {"importance": "...", "weight": 15}
                if isinstance(val, dict):
                    for sub_key in ("weight", "percentage", "score", "value", "rating", "rank"):
                        if sub_key in val:
                            try:
                                result[dim] = float(val[sub_key])
                                found = True
                                break
                            except (TypeError, ValueError):
                                pass
                    if not found:
                        # Try any numeric value in the dict
                        for sv in val.values():
                            try:
                                result[dim] = float(sv)
                                found = True
                                break
                            except (TypeError, ValueError):
                                pass
                else:
                    try:
                        result[dim] = float(val)
                        found = True
                    except (TypeError, ValueError):
                        pass
                if found:
                    break
        if not found:
            return None

    return result


def parse_likert_response(
    raw: str, dim_order: list[str]
) -> Optional[dict[str, float]]:
    """Parse Likert 1-5 response. Returns weights on 0-100 scale (x20)."""
    weights = parse_json_weights(raw, dim_order)
    if weights is None:
        return None

    # Validate Likert range
    for dim, val in weights.items():
        if val < 1 or val > 5 or val != int(val):
            return None

    # Convert to 0-100 scale for comparability
    total = sum(weights.values())
    if total == 0:
        return None
    return {dim: round(val / total * 100, 2) for dim, val in weights.items()}


def parse_ranking_response(
    raw: str, dim_order: list[str]
) -> Optional[dict[str, float]]:
    """Parse ranking 1-8. Invert (9 - rank) and normalize to sum to 100."""
    weights = parse_json_weights(raw, dim_order)
    if weights is None:
        return None

    # Validate: all values should be integers 1-8, unique
    vals = [int(v) for v in weights.values()]
    if sorted(vals) != list(range(1, 9)):
        return None

    # Invert: rank 1 (most important) -> 8, rank 8 -> 1
    inverted = {dim: 9.0 - val for dim, val in weights.items()}
    total = sum(inverted.values())  # always 36
    return {dim: round(val / total * 100, 2) for dim, val in inverted.items()}


PARSERS = {
    "json": parse_json_weights,
    "likert": parse_likert_response,
    "ranking": parse_ranking_response,
    "nl": parse_json_weights,  # NL also returns JSON weights
}


# ---------------------------------------------------------------------------
# Position mapping
# ---------------------------------------------------------------------------


def compute_position_weights(
    parsed_weights: dict[str, float], dim_order: list[str]
) -> dict[int, float]:
    """Map weights to positions 1-8 based on the ordering used."""
    return {
        pos + 1: parsed_weights.get(dim, 0.0)
        for pos, dim in enumerate(dim_order)
    }


# ---------------------------------------------------------------------------
# JSONL I/O
# ---------------------------------------------------------------------------


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def make_record(
    model_name: str,
    system_prompt: str,
    user_prompt: str,
    brand: str,
    response_format: str,
    repetition: int,
    ordering_index: int,
    dim_order: list[str],
    raw_response: str,
    parsed_weights: Optional[dict[str, float]],
    meta: dict[str, Any],
) -> dict:
    """Build a 20+ field JSONL record."""
    cfg = MODELS[model_name]
    weights_valid = parsed_weights is not None
    weight_sum = sum(parsed_weights.values()) if parsed_weights else 0.0
    position_weights = (
        compute_position_weights(parsed_weights, dim_order)
        if parsed_weights
        else None
    )

    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "experiment": "primacy_effect_generalization",
        "model_id": cfg["model_id"],
        "model_provider": cfg["provider"],
        "temperature": TEMPERATURE,
        "top_p": 1.0,
        "max_tokens": MAX_TOKENS_NL if response_format == "nl" else MAX_TOKENS,
        "system_prompt": system_prompt,
        "system_prompt_hash": _sha256(system_prompt),
        "user_prompt": user_prompt,
        "user_prompt_hash": _sha256(user_prompt),
        "brand": brand,
        "condition": response_format,
        "repetition": repetition,
        "raw_response": raw_response,
        "parsed_weights": parsed_weights,
        "weights_valid": weights_valid,
        "weight_sum_raw": round(weight_sum, 2),
        "response_time_ms": meta.get("response_time_ms", 0),
        "token_count_input": meta.get("token_count_input", 0),
        "token_count_output": meta.get("token_count_output", 0),
        "api_cost_usd": meta.get("api_cost_usd", 0.0),
        # Experiment-specific fields
        "response_format": response_format,
        "dimension_order": dim_order,
        "ordering_index": ordering_index,
        "position_weights": position_weights,
    }


# ---------------------------------------------------------------------------
# Trial Generation
# ---------------------------------------------------------------------------


def generate_trials(smoke: bool = False) -> list[dict]:
    """Generate all trial specifications.

    Full design: 4 formats x 8 orderings x 5 brands x 5 models x 3 reps = 2400
    Smoke test: 4 formats x 1 ordering x 1 brand x available models x 1 rep
    """
    random.seed(RANDOM_SEED)

    available = {
        name: cfg
        for name, cfg in MODELS.items()
        if os.environ.get(cfg["api_key_env"])
    }

    if not available:
        raise RuntimeError("No API keys found. Set at least one model's env var.")

    model_names = sorted(available.keys())
    brands = BRANDS if not smoke else [BRANDS[0]]  # Hermes only for smoke
    reps = 3 if not smoke else 1
    orderings = list(range(8)) if not smoke else [0]

    trials = []
    for fmt_idx, fmt in enumerate(RESPONSE_FORMATS):
        for ord_idx in orderings:
            for brand_idx, brand in enumerate(brands):
                for model_name in model_names:
                    for rep in range(reps):
                        trials.append({
                            "response_format": fmt,
                            "ordering_index": ord_idx,
                            "brand": brand,
                            "model_name": model_name,
                            "repetition": rep,
                        })

    # Shuffle to distribute rate limit load across providers
    random.shuffle(trials)
    return trials


# ---------------------------------------------------------------------------
# Main Execution Loop
# ---------------------------------------------------------------------------


def run_experiment(smoke: bool = False) -> dict:
    """Execute the full experiment."""
    trials = generate_trials(smoke=smoke)

    output_dir = Path(__file__).parent.parent / "L3_sessions"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "exp_primacy_generalization.jsonl"

    print(f"\n{'='*65}")
    print(f"Experiment E: Primacy Effect Generalization")
    print(f"{'='*65}")
    print(f"Trials: {len(trials)}")
    print(f"Output: {output_path}")
    print(f"Mode: {'SMOKE TEST' if smoke else 'LIVE'}")
    print(f"{'='*65}\n")

    stats = {
        "total_calls": 0,
        "successful": 0,
        "failed": 0,
        "parse_errors": 0,
        "total_cost": 0.0,
        "per_model": {},
        "per_format": {},
    }

    for trial_idx, trial in enumerate(trials):
        fmt = trial["response_format"]
        ord_idx = trial["ordering_index"]
        brand = trial["brand"]
        model_name = trial["model_name"]
        rep = trial["repetition"]
        dim_order = LATIN_SQUARE_ORDERINGS[ord_idx]

        stats["total_calls"] += 1
        model_stats = stats["per_model"].setdefault(
            model_name, {"calls": 0, "success": 0, "failed": 0, "cost": 0.0}
        )
        fmt_stats = stats["per_format"].setdefault(
            fmt, {"calls": 0, "success": 0, "failed": 0}
        )
        model_stats["calls"] += 1
        fmt_stats["calls"] += 1

        # Build prompt
        prompt_fn = PROMPT_BUILDERS[fmt]
        user_prompt = prompt_fn(brand, dim_order)
        max_tok = MAX_TOKENS_NL if fmt == "nl" else MAX_TOKENS

        print(
            f"  [{stats['total_calls']:4d}/{len(trials)}] "
            f"{model_name:10s} | {brand:12s} | {fmt:8s} | "
            f"ord={ord_idx} rep={rep}",
            end="",
            flush=True,
        )

        try:
            raw_response, meta = call_api(
                model_name, SYSTEM_PROMPT, user_prompt, max_tok
            )

            parser = PARSERS[fmt]
            parsed = parser(raw_response, dim_order)

            record = make_record(
                model_name=model_name,
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                brand=brand,
                response_format=fmt,
                repetition=rep,
                ordering_index=ord_idx,
                dim_order=dim_order,
                raw_response=raw_response,
                parsed_weights=parsed,
                meta=meta,
            )
            append_jsonl(output_path, record)

            if parsed:
                stats["successful"] += 1
                model_stats["success"] += 1
                fmt_stats["success"] += 1
                pos_w = compute_position_weights(parsed, dim_order)
                primacy = (pos_w[1] + pos_w[2]) / 2
                recency = (pos_w[7] + pos_w[8]) / 2
                print(f" | OK pos1-2={primacy:.1f} pos7-8={recency:.1f}")
            else:
                stats["parse_errors"] += 1
                model_stats["failed"] += 1
                fmt_stats["failed"] += 1
                print(f" | PARSE_ERROR")

            stats["total_cost"] += meta.get("api_cost_usd", 0.0)
            model_stats["cost"] += meta.get("api_cost_usd", 0.0)

        except Exception as e:
            stats["failed"] += 1
            model_stats["failed"] += 1
            fmt_stats["failed"] += 1
            print(f" | ERROR: {e}")

            record = make_record(
                model_name=model_name,
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                brand=brand,
                response_format=fmt,
                repetition=rep,
                ordering_index=ord_idx,
                dim_order=dim_order,
                raw_response=f"ERROR: {e}",
                parsed_weights=None,
                meta={"response_time_ms": 0, "token_count_input": 0,
                      "token_count_output": 0, "api_cost_usd": 0.0},
            )
            append_jsonl(output_path, record)

        time.sleep(INTER_CALL_DELAY)

    # Summary
    print(f"\n{'='*65}")
    print(f"COMPLETE")
    print(f"{'='*65}")
    print(f"Total calls: {stats['total_calls']}")
    print(f"Successful:  {stats['successful']}")
    print(f"Parse errors: {stats['parse_errors']}")
    print(f"API errors:  {stats['failed']}")
    print(f"Total cost:  ${stats['total_cost']:.2f}")
    print(f"\nPer model:")
    for m, s in sorted(stats["per_model"].items()):
        print(f"  {m:12s}: {s['success']}/{s['calls']} ok, ${s['cost']:.3f}")
    print(f"\nPer format:")
    for f, s in sorted(stats["per_format"].items()):
        print(f"  {f:8s}: {s['success']}/{s['calls']} ok")
    print(f"{'='*65}\n")

    # Save summary
    summary_path = output_dir.parent / "L4_analysis" / "exp_primacy_generalization_run_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w") as f:
        json.dump(stats, f, indent=2)

    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Experiment E: Primacy Effect Generalization"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--smoke", action="store_true", help="Smoke test (~20 calls)")
    group.add_argument("--live", action="store_true", help="Full run (~2400 calls)")
    args = parser.parse_args()

    run_experiment(smoke=args.smoke)
