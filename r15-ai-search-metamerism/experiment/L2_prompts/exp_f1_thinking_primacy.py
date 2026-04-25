#!/usr/bin/env python3
"""Experiment F1: Thinking-Mode Primacy.

Tests whether thinking/reasoning mode eliminates the serial position (primacy)
bias in structured LLM elicitation, and whether any effect depends on response
format (JSON allocation vs Likert rating).

Protocol: L0_specification/EXP_F1_THINKING_PRIMACY_PROTOCOL.md
Background: Exp E (Primacy Generalization) found d=1.39 (JSON), d=.22 (Likert).

Design: 2 (thinking mode) x 2 (format) x 8 (orderings) x 5 (brands) x 3 (model pairs)
        x 1 (rep) = 480 calls

Model pairs:
    gemini:   gemini-2.5-flash standard vs gemini-2.5-flash thinking (thinking_budget=1024)
    deepseek: deepseek-chat (V3) vs deepseek-reasoner (R1)
    grok:     grok-4-1-fast-non-reasoning vs grok-4-1 (reasoning)

Usage:
    uv run python exp_f1_thinking_primacy.py --dry-run   # print plan, no API calls
    uv run python exp_f1_thinking_primacy.py --smoke     # ~12 calls, verify setup
    uv run python exp_f1_thinking_primacy.py --live      # 480 calls, full run
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
RANDOM_SEED = 42
INTER_CALL_DELAY = 3.0  # seconds between API calls
PROMPT_TYPE = "primacy_thinking"

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

# Latin-square balanced dimension orderings (8 cyclic rotations)
LATIN_SQUARE_ORDERINGS = [DIMENSIONS[i:] + DIMENSIONS[:i] for i in range(8)]

RESPONSE_FORMATS = ["json", "likert"]

SYSTEM_PROMPT = "You are evaluating brand perception."


# ---------------------------------------------------------------------------
# Model Configuration
# ---------------------------------------------------------------------------
#
# Each model pair defines two entries: standard and thinking.
# The pair_name is used for grouping in analysis.
#
# thinking_config is provider-specific and passed to the call function.
# Supported keys:
#   gemini:   thinking_budget (int, 0 = disabled, >0 = enabled)
#   deepseek: use_reasoner (bool, True = use deepseek-reasoner endpoint)
#   grok:     use_reasoning (bool, True = use grok-4-1 instead of fast)

MODEL_VARIANTS = {
    # Gemini standard (thinking disabled)
    "gemini_standard": {
        "model_id": "gemini-2.5-flash",
        "provider": "google",
        "api_key_env": "GOOGLE_API_KEY",
        "thinking_mode": False,
        "model_pair": "gemini",
        "thinking_config": {"thinking_budget": 0},
        "input_cost_per_m": 0.15,
        "output_cost_per_m": 0.60,
    },
    # Gemini thinking (thinking enabled, budget=1024 tokens)
    "gemini_thinking": {
        "model_id": "gemini-2.5-flash",
        "provider": "google",
        "api_key_env": "GOOGLE_API_KEY",
        "thinking_mode": True,
        "model_pair": "gemini",
        "thinking_config": {"thinking_budget": 1024},
        "input_cost_per_m": 0.15,
        "output_cost_per_m": 3.50,  # thinking tokens cost more
    },
    # DeepSeek standard (V3, chat endpoint)
    "deepseek_standard": {
        "model_id": "deepseek-chat",
        "provider": "deepseek",
        "api_key_env": "DEEPSEEK_API_KEY",
        "thinking_mode": False,
        "model_pair": "deepseek",
        "thinking_config": {},
        "input_cost_per_m": 0.27,
        "output_cost_per_m": 1.10,
    },
    # DeepSeek thinking (R1, reasoner endpoint)
    "deepseek_thinking": {
        "model_id": "deepseek-reasoner",
        "provider": "deepseek",
        "api_key_env": "DEEPSEEK_API_KEY",
        "thinking_mode": True,
        "model_pair": "deepseek",
        "thinking_config": {},
        "input_cost_per_m": 0.55,
        "output_cost_per_m": 2.19,
    },
    # Grok standard (fast, non-reasoning)
    "grok_standard": {
        "model_id": "grok-4-1-fast-non-reasoning",
        "provider": "xai",
        "api_key_env": "GROK_API_KEY",
        "thinking_mode": False,
        "model_pair": "grok",
        "thinking_config": {},
        "input_cost_per_m": 3.00,
        "output_cost_per_m": 15.00,
    },
    # Grok thinking (reasoning mode)
    "grok_thinking": {
        "model_id": "grok-4-1",
        "provider": "xai",
        "api_key_env": "GROK_API_KEY",
        "thinking_mode": True,
        "model_pair": "grok",
        "thinking_config": {},
        "input_cost_per_m": 3.00,
        "output_cost_per_m": 15.00,
    },
}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:16]


def _compute_cost(inp_tokens: int, out_tokens: int, variant_name: str) -> float:
    cfg = MODEL_VARIANTS[variant_name]
    return round(
        inp_tokens * cfg["input_cost_per_m"] / 1_000_000
        + out_tokens * cfg["output_cost_per_m"] / 1_000_000,
        6,
    )


# ---------------------------------------------------------------------------
# Prompt Construction
# ---------------------------------------------------------------------------


def build_json_prompt(brand: str, dim_order: list[str]) -> str:
    """JSON allocation: weights sum to 100."""
    dim_json = "{" + ", ".join(f'"{d}": <weight>' for d in dim_order) + "}"
    return (
        f"Evaluate the brand {brand} by allocating importance weights across "
        f"eight dimensions of brand perception. The weights must sum to 100. "
        f"Respond in this exact JSON format:\n{dim_json}"
    )


def build_likert_prompt(brand: str, dim_order: list[str]) -> str:
    """Likert 1-5 ratings. All 8 dimensions in specified order."""
    dim_json = "{" + ", ".join(f'"{d}": <1-5>' for d in dim_order) + "}"
    return (
        f"Evaluate the brand {brand} on eight dimensions of brand perception. "
        f"Rate each dimension on a scale of 1-5 "
        f"(1 = not at all important, 5 = extremely important). "
        f"Respond in this exact JSON format:\n{dim_json}"
    )


PROMPT_BUILDERS = {
    "json": build_json_prompt,
    "likert": build_likert_prompt,
}


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------


def _extract_json_object(raw: str) -> Optional[dict]:
    """Extract first JSON object from raw text, stripping markdown fences."""
    text = re.sub(r"```(?:json)?\s*", "", raw.strip())
    text = re.sub(r"```\s*$", "", text).strip()
    # Strip thinking tags (DeepSeek R1 may include <think>...</think>)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

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
        return json.loads(text[start:end])
    except json.JSONDecodeError:
        return None


def parse_json_weights(
    raw: str, dim_order: list[str]
) -> Optional[dict[str, float]]:
    """Parse sum-to-100 allocation. Returns dict dim->float or None."""
    data = _extract_json_object(raw)
    if data is None:
        return None

    result = {}
    for dim in dim_order:
        found = False
        for key, val in data.items():
            if dim.lower() in key.lower():
                try:
                    result[dim] = float(val)
                    found = True
                    break
                except (TypeError, ValueError):
                    pass
        if not found:
            return None
    return result


def parse_likert_response(
    raw: str, dim_order: list[str]
) -> Optional[dict[str, float]]:
    """Parse Likert 1-5 ratings. Returns normalized weights (sum=100) or None."""
    weights = parse_json_weights(raw, dim_order)
    if weights is None:
        return None
    # Validate Likert range
    for val in weights.values():
        if val < 1 or val > 5:
            return None
    total = sum(weights.values())
    if total == 0:
        return None
    return {dim: round(val / total * 100, 2) for dim, val in weights.items()}


PARSERS = {
    "json": parse_json_weights,
    "likert": parse_likert_response,
}


# ---------------------------------------------------------------------------
# Position Mapping
# ---------------------------------------------------------------------------


def compute_position_weights(
    parsed_weights: dict[str, float], dim_order: list[str]
) -> dict[int, float]:
    """Map parsed dimension weights to serial positions 1-8."""
    return {
        pos + 1: parsed_weights.get(dim, 0.0)
        for pos, dim in enumerate(dim_order)
    }


def compute_primacy_score(position_weights: dict[int, float]) -> float:
    """Primacy score: mean(pos 1-2) - mean(pos 7-8). Positive = primacy bias."""
    early = (position_weights.get(1, 0.0) + position_weights.get(2, 0.0)) / 2
    late = (position_weights.get(7, 0.0) + position_weights.get(8, 0.0)) / 2
    return round(early - late, 4)


# ---------------------------------------------------------------------------
# JSONL I/O
# ---------------------------------------------------------------------------


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def make_record(
    variant_name: str,
    user_prompt: str,
    brand: str,
    response_format: str,
    ordering_index: int,
    dim_order: list[str],
    raw_response: str,
    parsed_weights: Optional[dict[str, float]],
    meta: dict[str, Any],
) -> dict:
    """Build a JSONL record conforming to EXPERIMENT_DATA_STANDARD.md."""
    cfg = MODEL_VARIANTS[variant_name]
    weights_valid = parsed_weights is not None
    weight_sum = sum(parsed_weights.values()) if parsed_weights else 0.0
    position_weights = (
        compute_position_weights(parsed_weights, dim_order)
        if parsed_weights
        else None
    )
    primacy_score = (
        compute_primacy_score(position_weights) if position_weights else None
    )

    # Determine model short name for the `model` required field
    # gemini_standard -> gemini, deepseek_thinking -> deepseek_r1, etc.
    if variant_name == "deepseek_thinking":
        model_short = "deepseek_r1"
    elif variant_name == "grok_thinking":
        model_short = "grok_reasoning"
    else:
        model_short = cfg["model_pair"]

    return {
        # --- Required base fields (EXPERIMENT_DATA_STANDARD.md) ---
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model": model_short,
        "prompt_type": PROMPT_TYPE,
        "prompt": user_prompt,
        # --- Recommended base fields ---
        "model_id": cfg["model_id"],
        "response": raw_response,
        "parsed": parsed_weights,
        "latency_ms": meta.get("response_time_ms", 0),
        "tokens_in": meta.get("token_count_input", 0),
        "tokens_out": meta.get("token_count_output", 0),
        "error": meta.get("error"),
        "temperature": TEMPERATURE,
        "brand": brand,
        "run": 0,
        # --- Experiment-specific fields ---
        "experiment": "f1_thinking_primacy",
        "thinking_mode": cfg["thinking_mode"],
        "model_pair": cfg["model_pair"],
        "model_variant": variant_name,
        "response_format": response_format,
        "dimension_order": dim_order,
        "ordering_index": ordering_index,
        "position_weights": position_weights,
        "primacy_score": primacy_score,
        "weights_valid": weights_valid,
        "weight_sum_raw": round(weight_sum, 2),
        "thinking_tokens": meta.get("thinking_tokens"),
        "system_prompt": SYSTEM_PROMPT,
        "system_prompt_hash": _sha256(SYSTEM_PROMPT),
        "user_prompt_hash": _sha256(user_prompt),
        "api_cost_usd": meta.get("api_cost_usd", 0.0),
        "model_provider": cfg["provider"],
    }


# ---------------------------------------------------------------------------
# API Callers
# ---------------------------------------------------------------------------


def call_api(
    variant_name: str,
    user_prompt: str,
    max_tokens: int = MAX_TOKENS,
) -> tuple[str, dict[str, Any]]:
    """Unified API caller with thinking-mode support and exponential backoff."""
    cfg = MODEL_VARIANTS[variant_name]
    provider = cfg["provider"]

    for attempt in range(5):
        try:
            if provider == "google":
                text, meta = _call_google(
                    cfg["model_id"],
                    SYSTEM_PROMPT,
                    user_prompt,
                    max_tokens,
                    cfg["thinking_config"],
                )
            elif provider == "deepseek":
                text, meta = _call_openai_compat(
                    cfg["model_id"],
                    SYSTEM_PROMPT,
                    user_prompt,
                    max_tokens,
                    api_key=os.environ[cfg["api_key_env"]],
                    base_url="https://api.deepseek.com",
                    strip_think_tags=cfg["thinking_mode"],
                )
            elif provider == "xai":
                text, meta = _call_openai_compat(
                    cfg["model_id"],
                    SYSTEM_PROMPT,
                    user_prompt,
                    max_tokens,
                    api_key=os.environ[cfg["api_key_env"]],
                    base_url="https://api.x.ai/v1",
                    strip_think_tags=False,
                )
            else:
                raise ValueError(f"Unknown provider: {provider}")

            meta["api_cost_usd"] = _compute_cost(
                meta["token_count_input"], meta["token_count_output"], variant_name
            )
            return text, meta

        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str:
                backoff = [5, 10, 20, 60, 120][attempt]
                print(f"    Rate limited ({variant_name}), backing off {backoff}s...")
                time.sleep(backoff)
            else:
                raise
    raise RuntimeError(f"Rate limit exceeded after 5 retries for {variant_name}")


def _call_google(
    model_id: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    thinking_config: dict,
) -> tuple[str, dict[str, Any]]:
    """Google Gemini call. Supports thinking_budget in thinking_config."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    thinking_budget = thinking_config.get("thinking_budget", 0)
    # Build GenerateContentConfig
    config_kwargs: dict[str, Any] = {
        "temperature": TEMPERATURE,
        "max_output_tokens": max_tokens,
        "system_instruction": system_prompt,
    }
    if thinking_budget > 0:
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_budget=thinking_budget
        )
    else:
        # Explicitly disable thinking
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_budget=0
        )

    t0 = time.time()
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=user_prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        text = response.text
    except Exception:
        # Fallback without thinking_config if API version doesn't support it
        fallback_config = types.GenerateContentConfig(
            temperature=TEMPERATURE,
            max_output_tokens=max_tokens,
            system_instruction=system_prompt,
        )
        response = client.models.generate_content(
            model=model_id,
            contents=user_prompt,
            config=fallback_config,
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
    # Thinking tokens (Gemini may report these separately)
    thinking_tokens = getattr(usage, "thoughts_token_count", None) if usage else None

    return text, {
        "response_time_ms": elapsed_ms,
        "token_count_input": inp_tokens,
        "token_count_output": out_tokens,
        "thinking_tokens": thinking_tokens,
    }


def _call_openai_compat(
    model_id: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    api_key: str,
    base_url: str,
    strip_think_tags: bool = False,
) -> tuple[str, dict[str, Any]]:
    """OpenAI-compatible call (DeepSeek, Grok, etc.)."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url)
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

    # Strip reasoning/thinking tags before parsing
    if strip_think_tags:
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

    # DeepSeek R1 may expose reasoning_content separately
    thinking_tokens = None
    if usage:
        ct = getattr(usage, "completion_tokens_details", None)
        if ct:
            thinking_tokens = getattr(ct, "reasoning_tokens", None)

    return content, {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
        "thinking_tokens": thinking_tokens,
    }


# ---------------------------------------------------------------------------
# Trial Generation
# ---------------------------------------------------------------------------


def available_variants() -> list[str]:
    """Return variant names whose API key is set in the environment."""
    return [
        name
        for name, cfg in MODEL_VARIANTS.items()
        if os.environ.get(cfg["api_key_env"])
    ]


def generate_trials(mode: str = "live") -> list[dict]:
    """Generate all trial specifications.

    Modes:
        dry-run: no API calls, just print plan (returns full trial list)
        smoke:   6 calls (1 format x 1 brand x 1 ordering x 3 available pairs, standard only)
        live:    480 calls (2 formats x 8 orderings x 5 brands x 6 variants x 1 rep)
    """
    random.seed(RANDOM_SEED)

    avail = available_variants()
    if not avail:
        raise RuntimeError(
            "No API keys found. Set at least one of: "
            + ", ".join(cfg["api_key_env"] for cfg in MODEL_VARIANTS.values())
        )

    if mode == "smoke":
        # One ordering, one brand, standard variants only, all formats
        smoke_variants = [v for v in avail if "standard" in v][:3]
        if not smoke_variants:
            smoke_variants = avail[:3]
        trials = []
        for fmt in RESPONSE_FORMATS[:1]:  # json only for smoke
            for variant in smoke_variants:
                trials.append({
                    "response_format": fmt,
                    "ordering_index": 0,
                    "brand": BRANDS[0],
                    "variant_name": variant,
                    "repetition": 0,
                })
        return trials

    # Full live design (or dry-run uses same list)
    trials = []
    for fmt in RESPONSE_FORMATS:
        for ord_idx in range(8):
            for brand in BRANDS:
                for variant_name in sorted(avail):
                    trials.append({
                        "response_format": fmt,
                        "ordering_index": ord_idx,
                        "brand": brand,
                        "variant_name": variant_name,
                        "repetition": 0,
                    })

    # Shuffle to spread rate-limit load across providers
    random.shuffle(trials)
    return trials


# ---------------------------------------------------------------------------
# Main Execution Loop
# ---------------------------------------------------------------------------


def run_experiment(mode: str = "live") -> dict:
    """Execute the experiment.

    mode: "dry-run" | "smoke" | "live"
    """
    trials = generate_trials(mode=mode)

    output_dir = Path(__file__).parent.parent / "L3_sessions"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "exp_f1_thinking_primacy.jsonl"

    avail = available_variants()

    print(f"\n{'='*65}")
    print("Experiment F1: Thinking-Mode Primacy")
    print(f"{'='*65}")
    print(f"Mode:           {mode.upper()}")
    print(f"Trials planned: {len(trials)}")
    print(f"Available variants: {', '.join(sorted(avail))}")
    print(f"Output:         {output_path}")
    print(f"{'='*65}\n")

    if mode == "dry-run":
        # Print plan and exit
        pairs_in_trials: dict[str, int] = {}
        for t in trials:
            pairs_in_trials[t["variant_name"]] = (
                pairs_in_trials.get(t["variant_name"], 0) + 1
            )
        print("Dry run -- no API calls will be made.\n")
        print("Trial distribution:")
        for vname, count in sorted(pairs_in_trials.items()):
            cfg = MODEL_VARIANTS.get(vname, {})
            mode_label = "thinking" if cfg.get("thinking_mode") else "standard"
            print(f"  {vname:30s} ({mode_label:8s}): {count:4d} calls")
        print(f"\nFormats: {RESPONSE_FORMATS}")
        print(f"Brands:  {BRANDS}")
        print(f"Orderings: 8 Latin-square rotations")
        print(f"\nDry run complete.")
        return {"mode": "dry-run", "trials_planned": len(trials)}

    stats = {
        "total_calls": 0,
        "successful": 0,
        "failed": 0,
        "parse_errors": 0,
        "total_cost": 0.0,
        "per_variant": {},
        "per_format": {},
        "per_pair": {},
    }

    for trial_idx, trial in enumerate(trials):
        fmt = trial["response_format"]
        ord_idx = trial["ordering_index"]
        brand = trial["brand"]
        variant_name = trial["variant_name"]
        dim_order = LATIN_SQUARE_ORDERINGS[ord_idx]
        cfg = MODEL_VARIANTS[variant_name]

        stats["total_calls"] += 1
        vstats = stats["per_variant"].setdefault(
            variant_name, {"calls": 0, "success": 0, "failed": 0, "cost": 0.0}
        )
        fstats = stats["per_format"].setdefault(
            fmt, {"calls": 0, "success": 0, "failed": 0}
        )
        pair_key = f"{cfg['model_pair']}_{fmt}"
        pstats = stats["per_pair"].setdefault(
            pair_key, {"calls": 0, "primacy_scores": []}
        )
        vstats["calls"] += 1
        fstats["calls"] += 1
        pstats["calls"] += 1

        prompt_fn = PROMPT_BUILDERS[fmt]
        user_prompt = prompt_fn(brand, dim_order)
        mode_label = "THINK" if cfg["thinking_mode"] else "STD  "

        print(
            f"  [{stats['total_calls']:4d}/{len(trials)}] "
            f"{variant_name:22s} | {brand:10s} | {fmt:6s} | "
            f"[{mode_label}] ord={ord_idx}",
            end="",
            flush=True,
        )

        try:
            raw_response, meta = call_api(variant_name, user_prompt, MAX_TOKENS)

            parser = PARSERS[fmt]
            parsed = parser(raw_response, dim_order)

            record = make_record(
                variant_name=variant_name,
                user_prompt=user_prompt,
                brand=brand,
                response_format=fmt,
                ordering_index=ord_idx,
                dim_order=dim_order,
                raw_response=raw_response,
                parsed_weights=parsed,
                meta=meta,
            )
            append_jsonl(output_path, record)

            if parsed:
                stats["successful"] += 1
                vstats["success"] += 1
                fstats["success"] += 1
                pos_w = compute_position_weights(parsed, dim_order)
                p_score = compute_primacy_score(pos_w)
                pstats["primacy_scores"].append(p_score)
                print(f" | OK primacy={p_score:+.2f}")
            else:
                stats["parse_errors"] += 1
                vstats["failed"] += 1
                fstats["failed"] += 1
                print(" | PARSE_ERROR")

            cost = meta.get("api_cost_usd", 0.0)
            stats["total_cost"] += cost
            vstats["cost"] += cost

        except Exception as e:
            stats["failed"] += 1
            vstats["failed"] += 1
            fstats["failed"] += 1
            print(f" | ERROR: {e}")

            record = make_record(
                variant_name=variant_name,
                user_prompt=user_prompt,
                brand=brand,
                response_format=fmt,
                ordering_index=ord_idx,
                dim_order=dim_order,
                raw_response=f"ERROR: {e}",
                parsed_weights=None,
                meta={
                    "response_time_ms": 0,
                    "token_count_input": 0,
                    "token_count_output": 0,
                    "api_cost_usd": 0.0,
                    "error": str(e),
                },
            )
            append_jsonl(output_path, record)

        time.sleep(INTER_CALL_DELAY)

    # Summary
    print(f"\n{'='*65}")
    print("COMPLETE")
    print(f"{'='*65}")
    print(f"Total calls:  {stats['total_calls']}")
    print(f"Successful:   {stats['successful']}")
    print(f"Parse errors: {stats['parse_errors']}")
    print(f"API errors:   {stats['failed']}")
    print(f"Total cost:   ${stats['total_cost']:.3f}")
    print("\nPer variant:")
    for vname, vs in sorted(stats["per_variant"].items()):
        cfg = MODEL_VARIANTS.get(vname, {})
        mode_label = "thinking" if cfg.get("thinking_mode") else "standard"
        print(
            f"  {vname:22s} ({mode_label:8s}): "
            f"{vs['success']:3d}/{vs['calls']:3d} ok, ${vs['cost']:.3f}"
        )
    print("\nPer format:")
    for fname, fs in sorted(stats["per_format"].items()):
        print(f"  {fname:6s}: {fs['success']}/{fs['calls']} ok")
    print(f"{'='*65}\n")

    # Save run summary
    summary_path = (
        Path(__file__).parent.parent
        / "L4_analysis"
        / "exp_f1_thinking_primacy_run_summary.json"
    )
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    # Convert primacy_scores lists to mean+n for JSON serialization
    serializable_stats = {
        k: (
            {
                pk: {
                    "calls": pv["calls"],
                    "n_valid": len(pv["primacy_scores"]),
                    "mean_primacy": (
                        round(
                            sum(pv["primacy_scores"]) / len(pv["primacy_scores"]), 4
                        )
                        if pv["primacy_scores"]
                        else None
                    ),
                }
                for pk, pv in v.items()
            }
            if k == "per_pair"
            else v
        )
        for k, v in stats.items()
    }
    with open(summary_path, "w") as f:
        json.dump(serializable_stats, f, indent=2)

    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Experiment F1: Thinking-Mode Primacy (480 calls)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Print trial plan without making any API calls",
    )
    group.add_argument(
        "--smoke",
        action="store_true",
        help="Smoke test: ~6 calls to verify setup",
    )
    group.add_argument(
        "--live",
        action="store_true",
        help="Full run: 480 calls",
    )
    args = parser.parse_args()

    if args.dry_run:
        run_experiment(mode="dry-run")
    elif args.smoke:
        run_experiment(mode="smoke")
    else:
        run_experiment(mode="live")
