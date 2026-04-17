#!/usr/bin/env python3
"""Compounding x Format Experiment.

Tests whether providing a Brand Function specification at each step of a
multi-turn agentic pipeline reduces the compounding effect on DCI relative
to a baseline (no spec) condition.

DESIGN

Two conditions x three pipeline stages x control:
  - baseline:   standard shopping pipeline, no Brand Function context
  - specified:  Brand Function JSON prepended to the system prompt at every
                step (spec is part of the assistant's persistent context)

Pipeline stages (mirrors Exp A structure, single multi-turn conversation):
  - step_1:  Retrieval — recommend 5 brands in category
  - step_2:  Comparison — allocate 8-dim weights for focal vs competitor
  - step_3:  Recommendation — final 8-dim weights for chosen brand
  - control: Single PRISM-B call (no pipeline context, direct evaluation)

BRANDS: Hermes, Patagonia, Erewhon, Tesla, IKEA (canonical SBT profiles)
MODELS: claude, gpt, gemini, deepseek, grok, gemma4 (Ollama)
REPS:   2 per cell

VOLUME:
  5 brands x 6 models x 2 conditions x 3 pipeline steps x 2 reps = 360 calls
  5 brands x 6 models x 2 conditions x 1 control step  x 2 reps = 120 calls
  Total: 480 calls

HYPOTHESES
  H_CF1: DCI(step_3, specified) < DCI(step_3, baseline)
         — spec reduces final collapse magnitude
  H_CF2: DCI growth rate (step_1 -> step_3) is lower in specified condition
         — spec attenuates compounding across steps
  H_CF3: DCI(control, specified) < DCI(control, baseline)
         — spec reduces collapse even without pipeline context

OUTPUT

  L3_sessions/exp_compounding_format.jsonl  — raw session log (appended)

USAGE

    uv run python exp_compounding_format.py --dry-run  # no API calls
    uv run python exp_compounding_format.py --smoke    # 1 brand x 1 model
    uv run python exp_compounding_format.py --live     # full 480 calls

Requires env vars: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY,
DEEPSEEK_API_KEY, GROK_API_KEY. Ollama requires OLLAMA_HOST or default
http://localhost:11434.
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
import uuid
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TEMPERATURE = 0.7
MAX_TOKENS = 512
MAX_TOKENS_STEP1 = 1024  # Step 1 needs more room for 5 brand descriptions
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

CATEGORIES = {
    "Hermes": {
        "category": "luxury fashion",
        "use_case": "a luxury accessory purchase",
    },
    "IKEA": {
        "category": "home furnishings",
        "use_case": "furnishing a new apartment",
    },
    "Patagonia": {
        "category": "outdoor gear",
        "use_case": "outdoor adventure equipment",
    },
    "Erewhon": {
        "category": "specialty grocery",
        "use_case": "premium grocery shopping",
    },
    "Tesla": {
        "category": "electric vehicles",
        "use_case": "purchasing an electric vehicle",
    },
}

FALLBACK_COMPETITORS = {
    "Hermes": "Louis Vuitton",
    "IKEA": "West Elm",
    "Patagonia": "Arc'teryx",
    "Erewhon": "Whole Foods",
    "Tesla": "Rivian",
}

# Brand Function JSON files location (relative to this script's parent dir)
BRAND_FUNCTION_DIR = (
    Path(__file__).resolve().parent.parent
    / "L1_configuration"
    / "brand_functions"
)

# Latin-square balanced dimension orderings (8 cyclic rotations)
LATIN_SQUARE_ORDERINGS = []
for _i in range(8):
    LATIN_SQUARE_ORDERINGS.append(DIMENSIONS[_i:] + DIMENSIONS[:_i])


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

MODELS = {
    "claude": {
        "model_id": "claude-haiku-4-5",
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
    "gemma4": {
        "model_id": "gemma4:latest",
        "provider": "ollama",
        "api_key_env": "OLLAMA_HOST",  # not a key, just presence check
        "input_cost_per_m": 0.0,
        "output_cost_per_m": 0.0,
    },
}


# ---------------------------------------------------------------------------
# Brand Function loader
# ---------------------------------------------------------------------------


def load_brand_function(brand_name: str) -> Optional[dict]:
    """Load Brand Function JSON for a given brand.

    Returns None (with a warning) if the file is not found rather than
    raising, so the experiment degrades gracefully when only testing a
    subset of brands.
    """
    slug = brand_name.lower().replace(" ", "_")
    path = BRAND_FUNCTION_DIR / f"{slug}.json"
    if not path.exists():
        print(f"  WARNING: Brand Function not found for {brand_name}: {path}")
        return None
    with open(path) as f:
        return json.load(f)


def format_brand_function_spec(bf: dict) -> str:
    """Format a Brand Function dict as a system-prompt prefix block."""
    dims_lower = [d.lower() for d in DIMENSIONS]
    lines = [
        f"BRAND SPECIFICATION: {bf['brand']}",
        f"(Source: {bf.get('source', 'Canonical SBT brand profile')})",
        "",
    ]
    for dim_lower in dims_lower:
        dim_data = bf.get("dimensions", {}).get(dim_lower, {})
        score = dim_data.get("score", "N/A")
        positioning = dim_data.get("positioning", "")
        signals = dim_data.get("key_signals", [])
        lines.append(f"{dim_lower.upper()} ({score}/10): {positioning}")
        if signals:
            lines.append(f"  Signals: {', '.join(signals)}")
    return "\n".join(lines)


def build_specified_system_prompt(brand: str, base_system: str) -> str:
    """Prepend Brand Function spec to a base system prompt.

    If no Brand Function file is found, falls back to base_system so the
    experiment still runs but logs a warning.
    """
    bf = load_brand_function(brand)
    if bf is None:
        return base_system
    spec_text = format_brand_function_spec(bf)
    return (
        f"You have access to the following verified brand specification for "
        f"{brand}. Use this information when evaluating the brand.\n\n"
        f"{spec_text}\n\n---\n\n"
        f"{base_system}"
    )


# ---------------------------------------------------------------------------
# Multi-turn API callers (identical to exp_agentic_collapse.py)
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


def call_api_multiturn(
    model_name: str,
    system_prompt: str,
    messages: list[dict[str, str]],
    max_tokens: int = MAX_TOKENS,
) -> tuple[str, dict[str, Any]]:
    """Multi-turn API call with exponential backoff on 429.

    Args:
        model_name: Key into MODELS dict.
        system_prompt: System instruction (stays constant across turns).
        messages: List of {"role": "user"|"assistant", "content": "..."} dicts.
        max_tokens: Max output tokens.

    Returns:
        (response_text, metadata_dict)
    """
    cfg = MODELS[model_name]
    provider = cfg["provider"]

    for attempt in range(5):
        try:
            text, meta = _call_provider_multiturn(
                provider, cfg["model_id"], system_prompt, messages, max_tokens
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


def _call_provider_multiturn(
    provider: str,
    model_id: str,
    system_prompt: str,
    messages: list[dict[str, str]],
    max_tokens: int,
) -> tuple[str, dict[str, Any]]:
    """Dispatch multi-turn call to the correct provider."""
    if provider == "anthropic":
        return _call_anthropic_mt(model_id, system_prompt, messages, max_tokens)
    elif provider == "openai":
        return _call_openai_mt(
            model_id, system_prompt, messages, max_tokens, None, None
        )
    elif provider == "google":
        return _call_google_mt(model_id, system_prompt, messages, max_tokens)
    elif provider == "deepseek":
        return _call_openai_mt(
            model_id,
            system_prompt,
            messages,
            max_tokens,
            os.environ["DEEPSEEK_API_KEY"],
            "https://api.deepseek.com",
        )
    elif provider == "xai":
        return _call_openai_mt(
            model_id,
            system_prompt,
            messages,
            max_tokens,
            os.environ["GROK_API_KEY"],
            "https://api.x.ai/v1",
        )
    elif provider == "ollama":
        return _call_ollama_mt(model_id, system_prompt, messages, max_tokens)
    else:
        raise ValueError(f"Unknown provider: {provider}")


def _call_anthropic_mt(
    model_id: str,
    system_prompt: str,
    messages: list[dict[str, str]],
    max_tokens: int,
) -> tuple[str, dict[str, Any]]:
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    t0 = time.time()
    message = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        temperature=TEMPERATURE,
        system=system_prompt,
        messages=messages,
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    return message.content[0].text, {
        "response_time_ms": elapsed_ms,
        "token_count_input": message.usage.input_tokens,
        "token_count_output": message.usage.output_tokens,
    }


def _call_openai_mt(
    model_id: str,
    system_prompt: str,
    messages: list[dict[str, str]],
    max_tokens: int,
    api_key: Optional[str],
    base_url: Optional[str],
) -> tuple[str, dict[str, Any]]:
    from openai import OpenAI

    kwargs: dict[str, Any] = {}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    client = OpenAI(**kwargs)
    t0 = time.time()
    oai_messages = [{"role": "system", "content": system_prompt}] + messages
    response = client.chat.completions.create(
        model=model_id,
        messages=oai_messages,
        max_tokens=max_tokens,
        temperature=TEMPERATURE,
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    usage = response.usage
    return response.choices[0].message.content, {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
    }


def _call_google_mt(
    model_id: str,
    system_prompt: str,
    messages: list[dict[str, str]],
    max_tokens: int,
) -> tuple[str, dict[str, Any]]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    contents = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append(
            types.Content(role=role, parts=[types.Part(text=msg["content"])])
        )

    t0 = time.time()
    # Gemini 2.5 Flash uses internal "thinking" tokens that count against
    # the output budget. Use 8192 min to prevent truncation. Do NOT use
    # response_mime_type="application/json" — causes truncation in multi-turn.
    gemini_max = max(max_tokens, 8192)
    response = client.models.generate_content(
        model=model_id,
        contents=contents,
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


def _call_ollama_mt(
    model_id: str,
    system_prompt: str,
    messages: list[dict[str, str]],
    max_tokens: int,
) -> tuple[str, dict[str, Any]]:
    """Call local Ollama model via its OpenAI-compatible API."""
    import urllib.request

    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    url = f"{ollama_host}/api/chat"

    # Local models (Gemma 4, Qwen3) use thinking tokens that consume output
    # budget. Use 8192 minimum to prevent truncation.
    ollama_predict = max(max_tokens, 8192)
    payload = {
        "model": model_id,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": ollama_predict,
        },
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode())
    elapsed_ms = int((time.time() - t0) * 1000)

    text = data.get("message", {}).get("content", "")
    # Strip <think>...</think> blocks from thinking models
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    inp_tokens = data.get("prompt_eval_count", 0)
    out_tokens = data.get("eval_count", 0)

    return text, {
        "response_time_ms": elapsed_ms,
        "token_count_input": inp_tokens,
        "token_count_output": out_tokens,
    }


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_PIPELINE = "You are a helpful AI shopping assistant."
SYSTEM_PROMPT_CONTROL = "You are evaluating brand perception."


def get_dim_json(dim_order: list[str]) -> str:
    """Build JSON template string with dimension keys in given order."""
    return ", ".join(f'"{d}": <number>' for d in dim_order)


def build_step1_user(category: str) -> str:
    """Build Step 1 (Retrieval) user message."""
    return (
        f"I'm looking for {category} products. List 5 brands you'd recommend, "
        f"with a brief reason for each. Focus on what makes each distinctive."
    )


def build_step2_user(
    brand_a: str, brand_b: str, use_case: str, dim_order: list[str]
) -> str:
    """Build Step 2 (Comparison) user message."""
    dim_json = get_dim_json(dim_order)
    return (
        f"I'm considering {brand_a} and {brand_b} for {use_case}. "
        f"For each brand, allocate importance weights across eight perception "
        f"dimensions. Weights must sum to 100. Respond in JSON:\n"
        f'{{"brand_A": {{{dim_json}}}, "brand_B": {{{dim_json}}}}}'
    )


def build_step3_user(use_case: str, dim_order: list[str]) -> str:
    """Build Step 3 (Recommendation) user message."""
    dim_json = get_dim_json(dim_order)
    return (
        f"Based on your comparison, which brand would you recommend for "
        f"{use_case}? Score your recommended brand on these eight dimensions "
        f"(weights sum to 100). Explain your choice briefly. Respond in JSON:\n"
        f'{{"recommended": "...", "weights": {{{dim_json}}}, "reason": "..."}}'
    )


def build_control_user(brand: str, dim_order: list[str]) -> str:
    """Build Control (single-step PRISM-B) user message."""
    dim_json = get_dim_json(dim_order)
    return (
        f"Evaluate the brand {brand} by allocating importance weights across "
        f"eight dimensions of brand perception. The weights must sum to 100.\n\n"
        f"Respond in this exact JSON format:\n{{{dim_json}}}"
    )


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------


def parse_weights(raw: str) -> Optional[dict[str, float]]:
    """Extract dimension weights from JSON response."""
    match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError:
        return None
    return _extract_dim_weights(data)


def parse_step2_weights(
    raw: str,
) -> tuple[Optional[dict[str, float]], Optional[dict[str, float]]]:
    """Parse Step 2 response with two brand weight sets."""
    try:
        cleaned = re.sub(r"```json\s*", "", raw)
        cleaned = re.sub(r"```\s*", "", cleaned)
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            data = json.loads(match.group())
            brand_a_data = None
            brand_b_data = None
            for k, v in data.items():
                if isinstance(v, dict):
                    if brand_a_data is None:
                        brand_a_data = v
                    else:
                        brand_b_data = v
                        break
            if brand_a_data and brand_b_data:
                return (
                    _extract_dim_weights(brand_a_data),
                    _extract_dim_weights(brand_b_data),
                )
    except (json.JSONDecodeError, AttributeError):
        pass
    return None, None


def _extract_dim_weights(data: dict) -> Optional[dict[str, float]]:
    """Extract dimension weights from a dict, matching case-insensitively."""
    weights = {}
    for dim in DIMENSIONS:
        val = data.get(dim)
        if val is None:
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


def parse_step3_response(
    raw: str,
) -> tuple[Optional[str], Optional[dict[str, float]], Optional[str]]:
    """Parse Step 3 response: recommended brand, weights, reason."""
    try:
        cleaned = re.sub(r"```json\s*", "", raw)
        cleaned = re.sub(r"```\s*", "", cleaned)
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            data = json.loads(match.group())
            recommended = data.get("recommended", "")
            reason = data.get("reason", "")
            weights_data = data.get("weights", data)
            weights = None
            if isinstance(weights_data, dict):
                weights = _extract_dim_weights(weights_data)
            if weights is None:
                weights = _extract_dim_weights(data)
            return recommended, weights, reason
    except (json.JSONDecodeError, AttributeError):
        pass
    return None, None, None


def parse_step1_brands(raw: str) -> list[str]:
    """Extract brand names from Step 1 free-text response."""
    brands = []
    # Numbered list: "1. BrandName" or "1. **BrandName**"
    matches = re.findall(
        r"^\s*\d+[\.\)]\s*\**([A-Z][A-Za-z\s&'.\-]+?)\**(?:\s*[-:—]|\s*\()",
        raw,
        re.MULTILINE,
    )
    if matches:
        brands = [m.strip().rstrip("*") for m in matches]
    if not brands:
        # Fallback: bold text
        matches = re.findall(r"\*\*([A-Z][A-Za-z\s&'.\-]+?)\*\*", raw)
        brands = [m.strip() for m in matches]
    return brands[:5]


# ---------------------------------------------------------------------------
# Record construction
# ---------------------------------------------------------------------------


def _make_record(
    step: int,
    brand: str,
    category: str,
    model_name: str,
    rep: int,
    dim_order: list[str],
    system_prompt: str,
    user_prompt: str,
    conversation_id: str,
    conversation_history: list[dict[str, str]],
    bf_condition: str,
) -> dict:
    """Create a base JSONL record."""
    cfg = MODELS[model_name]
    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "experiment": "exp_compounding_format",
        "model_id": cfg["model_id"],
        "model_provider": cfg["provider"],
        "temperature": TEMPERATURE,
        "top_p": 1.0,
        "max_tokens": MAX_TOKENS_STEP1 if step == 1 else MAX_TOKENS,
        "system_prompt": system_prompt,
        "system_prompt_hash": _sha256(system_prompt),
        "user_prompt": user_prompt,
        "user_prompt_hash": _sha256(user_prompt),
        "brand": brand,
        "condition": f"step_{step}" if step > 0 else "control",
        "bf_condition": bf_condition,  # "baseline" or "specified"
        "repetition": rep,
        "raw_response": "",
        "parsed_weights": None,
        "weights_valid": False,
        "weight_sum_raw": 0,
        "response_time_ms": 0,
        "token_count_input": 0,
        "token_count_output": 0,
        "api_cost_usd": 0.0,
        # Experiment-specific fields
        "step": step,
        "category": category,
        "conversation_id": conversation_id,
        "conversation_turn": step,
        "conversation_history": conversation_history,
        "step_1_brands": None,
        "step_1_raw": None,
        "competitor": None,
        "step_2_raw": None,
        "recommended_brand": None,
        "recommendation_reason": None,
        "dim_order": dim_order,
    }


def _write_record(jsonl_path: Path, record: dict) -> None:
    """Append a single record to JSONL file."""
    with open(jsonl_path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _print_progress(record: dict, label: str) -> None:
    """Print progress line."""
    if record["step"] == 1:
        status = "--"
    elif record["weights_valid"]:
        status = "OK"
    else:
        status = "FAIL"
    cost_str = f"${record.get('api_cost_usd', 0):.4f}"
    bf = record.get("bf_condition", "?")
    print(
        f"  {label} [{bf}] | {record['model_provider']:>9} | {record['brand']:>10} "
        f"rep={record['repetition']} -> {status} "
        f"({record.get('response_time_ms', 0)}ms, {cost_str})"
    )


def _dry_run_record(record: dict, label: str) -> None:
    """Simulate a call in dry-run mode: fill stub values and print."""
    record["raw_response"] = "[DRY RUN]"
    record["response_time_ms"] = 0
    record["token_count_input"] = 0
    record["token_count_output"] = 0
    record["api_cost_usd"] = 0.0
    # Provide fake uniform weights so downstream parsing doesn't fail
    fake_weights = {d: 12.5 for d in DIMENSIONS}
    record["parsed_weights"] = fake_weights
    record["weight_sum_raw"] = 100.0
    record["weights_valid"] = True
    _print_progress(record, label)


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------


def run_pipeline(
    brand: str,
    model_name: str,
    rep: int,
    call_idx: int,
    bf_condition: str,
    jsonl_path: Path,
    dry_run: bool = False,
) -> list[dict]:
    """Run a full 3-step pipeline as a SINGLE multi-turn conversation.

    In the 'specified' condition the Brand Function spec is prepended to the
    system prompt and remains there for all three steps (persistent context).
    In the 'baseline' condition the standard system prompt is used throughout.

    Args:
        brand: Focal brand name (key in CANONICAL_PROFILES).
        model_name: Key in MODELS dict.
        rep: Repetition index (1-based).
        call_idx: Global call counter used for Latin-square rotation.
        bf_condition: "baseline" or "specified".
        jsonl_path: Output JSONL file path.
        dry_run: If True, skip API calls and write stub records.

    Returns:
        List of three record dicts (one per step).
    """
    cat_info = CATEGORIES[brand]
    category = cat_info["category"]
    use_case = cat_info["use_case"]
    dim_order = LATIN_SQUARE_ORDERINGS[call_idx % 8]
    conversation_id = str(uuid.uuid4())
    records = []

    # Build system prompt based on condition
    if bf_condition == "specified":
        system_prompt = build_specified_system_prompt(brand, SYSTEM_PROMPT_PIPELINE)
    else:
        system_prompt = SYSTEM_PROMPT_PIPELINE

    # Conversation history (accumulated across steps)
    history: list[dict[str, str]] = []

    # --- Step 1: Retrieval ---
    step1_user = build_step1_user(category)
    history.append({"role": "user", "content": step1_user})

    record1 = _make_record(
        step=1,
        brand=brand,
        category=category,
        model_name=model_name,
        rep=rep,
        dim_order=dim_order,
        system_prompt=system_prompt,
        user_prompt=step1_user,
        conversation_id=conversation_id,
        conversation_history=list(history),
        bf_condition=bf_condition,
    )

    if dry_run:
        _dry_run_record(record1, "Step 1")
        raw1 = "[DRY RUN]"
        step1_brands = [FALLBACK_COMPETITORS[brand], brand]
        record1["step_1_brands"] = step1_brands
        history.append({"role": "assistant", "content": raw1})
    else:
        try:
            raw1, meta1 = call_api_multiturn(
                model_name, system_prompt, history, MAX_TOKENS_STEP1
            )
            record1["raw_response"] = raw1
            record1.update(meta1)
            step1_brands = parse_step1_brands(raw1)
            record1["step_1_brands"] = step1_brands
            record1["weights_valid"] = False
            history.append({"role": "assistant", "content": raw1})
        except Exception as e:
            record1["raw_response"] = f"ERROR: {type(e).__name__}: {e}"
            step1_brands = []
            history.append({"role": "assistant", "content": record1["raw_response"]})
        _print_progress(record1, "Step 1")
        time.sleep(INTER_CALL_DELAY)

    records.append(record1)
    _write_record(jsonl_path, record1)

    # Pick a competitor from Step 1 results (not the focal brand)
    competitors = [b for b in step1_brands if b.lower() != brand.lower()]
    competitor = competitors[0] if competitors else FALLBACK_COMPETITORS[brand]

    # --- Step 2: Comparison ---
    step2_user = build_step2_user(brand, competitor, use_case, dim_order)
    history.append({"role": "user", "content": step2_user})

    record2 = _make_record(
        step=2,
        brand=brand,
        category=category,
        model_name=model_name,
        rep=rep,
        dim_order=dim_order,
        system_prompt=system_prompt,
        user_prompt=step2_user,
        conversation_id=conversation_id,
        conversation_history=list(history),
        bf_condition=bf_condition,
    )
    record2["competitor"] = competitor
    record2["step_1_brands"] = step1_brands
    record2["step_1_raw"] = record1["raw_response"]

    if dry_run:
        _dry_run_record(record2, "Step 2")
        raw2 = "[DRY RUN]"
        history.append({"role": "assistant", "content": raw2})
    else:
        try:
            raw2, meta2 = call_api_multiturn(
                model_name, system_prompt, history, MAX_TOKENS
            )
            record2["raw_response"] = raw2
            record2.update(meta2)
            wa, wb = parse_step2_weights(raw2)
            if wa:
                record2["parsed_weights"] = wa
                wsum = sum(wa.values())
                record2["weight_sum_raw"] = wsum
                record2["weights_valid"] = abs(wsum - 100) <= 30
            else:
                record2["weights_valid"] = False
            history.append({"role": "assistant", "content": raw2})
        except Exception as e:
            record2["raw_response"] = f"ERROR: {type(e).__name__}: {e}"
            raw2 = ""
            history.append({"role": "assistant", "content": record2["raw_response"]})
        _print_progress(record2, "Step 2")
        time.sleep(INTER_CALL_DELAY)

    records.append(record2)
    _write_record(jsonl_path, record2)

    # --- Step 3: Recommendation ---
    step3_user = build_step3_user(use_case, dim_order)
    history.append({"role": "user", "content": step3_user})

    record3 = _make_record(
        step=3,
        brand=brand,
        category=category,
        model_name=model_name,
        rep=rep,
        dim_order=dim_order,
        system_prompt=system_prompt,
        user_prompt=step3_user,
        conversation_id=conversation_id,
        conversation_history=list(history),
        bf_condition=bf_condition,
    )
    record3["competitor"] = competitor
    record3["step_1_brands"] = step1_brands
    record3["step_1_raw"] = record1["raw_response"]
    record3["step_2_raw"] = record2["raw_response"]

    if dry_run:
        _dry_run_record(record3, "Step 3")
    else:
        try:
            raw3, meta3 = call_api_multiturn(
                model_name, system_prompt, history, MAX_TOKENS
            )
            record3["raw_response"] = raw3
            record3.update(meta3)
            recommended, weights, reason = parse_step3_response(raw3)
            if weights:
                record3["parsed_weights"] = weights
                wsum = sum(weights.values())
                record3["weight_sum_raw"] = wsum
                record3["weights_valid"] = abs(wsum - 100) <= 5
            else:
                record3["weights_valid"] = False
            record3["recommended_brand"] = recommended or ""
            record3["recommendation_reason"] = reason or ""
        except Exception as e:
            record3["raw_response"] = f"ERROR: {type(e).__name__}: {e}"
        _print_progress(record3, "Step 3")
        time.sleep(INTER_CALL_DELAY)

    records.append(record3)
    _write_record(jsonl_path, record3)

    return records


def run_control(
    brand: str,
    model_name: str,
    rep: int,
    call_idx: int,
    bf_condition: str,
    jsonl_path: Path,
    dry_run: bool = False,
) -> dict:
    """Run a single-step PRISM-B control evaluation (no conversation).

    In the 'specified' condition the Brand Function spec is prepended to
    the control system prompt, testing spec effect without pipeline context.
    """
    dim_order = LATIN_SQUARE_ORDERINGS[call_idx % 8]
    cat_info = CATEGORIES[brand]
    conversation_id = str(uuid.uuid4())
    usr_p = build_control_user(brand, dim_order)

    if bf_condition == "specified":
        sys_p = build_specified_system_prompt(brand, SYSTEM_PROMPT_CONTROL)
    else:
        sys_p = SYSTEM_PROMPT_CONTROL

    messages = [{"role": "user", "content": usr_p}]

    record = _make_record(
        step=0,
        brand=brand,
        category=cat_info["category"],
        model_name=model_name,
        rep=rep,
        dim_order=dim_order,
        system_prompt=sys_p,
        user_prompt=usr_p,
        conversation_id=conversation_id,
        conversation_history=messages,
        bf_condition=bf_condition,
    )
    record["condition"] = "control"

    if dry_run:
        _dry_run_record(record, "Control")
    else:
        try:
            raw, meta = call_api_multiturn(model_name, sys_p, messages)
            record["raw_response"] = raw
            record.update(meta)
            weights = parse_weights(raw)
            if weights:
                record["parsed_weights"] = weights
                wsum = sum(weights.values())
                record["weight_sum_raw"] = wsum
                record["weights_valid"] = abs(wsum - 100) <= 30
        except Exception as e:
            record["raw_response"] = f"ERROR: {type(e).__name__}: {e}"
        _print_progress(record, "Control")
        time.sleep(INTER_CALL_DELAY)

    _write_record(jsonl_path, record)
    return record


# ---------------------------------------------------------------------------
# Main experiment orchestrator
# ---------------------------------------------------------------------------


def run_experiment(mode: str = "live", dry_run: bool = False) -> None:
    """Execute the compounding x format experiment."""
    output_dir = Path(__file__).resolve().parent.parent / "L3_sessions"
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "exp_compounding_format.jsonl"

    if jsonl_path.exists() and not dry_run:
        backup = jsonl_path.with_suffix(".jsonl.bak")
        jsonl_path.rename(backup)
        print(f"Backed up existing data to {backup.name}")

    # Model availability check
    available: dict[str, dict] = {}
    for name, cfg in MODELS.items():
        env_val = os.environ.get(cfg["api_key_env"])
        if cfg["provider"] == "ollama":
            # Ollama: always include; will error at call time if not running
            available[name] = cfg
        elif env_val:
            available[name] = cfg
        else:
            print(f"  Skipping {name}: {cfg['api_key_env']} not set")

    if not available and not dry_run:
        print("ERROR: No models available. Set API keys.")
        sys.exit(1)

    model_names = list(available.keys())
    print(f"Available models: {model_names}")

    rng = random.Random(RANDOM_SEED)

    if mode == "smoke":
        brands_to_test = ["Patagonia"]
        models_to_test = model_names[:1]
        reps = 1
    else:
        brands_to_test = BRANDS
        models_to_test = model_names
        reps = 2

    # Build the full work queue
    # Each entry: brand x model x rep x bf_condition
    # We run pipeline (3 API calls) + control (1 API call) per entry
    work_items: list[dict] = []
    call_idx = 0

    for brand in brands_to_test:
        for model_name in models_to_test:
            for rep in range(1, reps + 1):
                for bf_cond in ("baseline", "specified"):
                    work_items.append({
                        "brand": brand,
                        "model": model_name,
                        "rep": rep,
                        "bf_condition": bf_cond,
                        "pipeline_idx": call_idx,
                        "control_idx": call_idx + 1,
                    })
                    call_idx += 2

    rng.shuffle(work_items)

    # Count totals
    n_pipeline = len(work_items)
    n_control = len(work_items)
    total_api_calls = n_pipeline * 3 + n_control
    dry_tag = " [DRY RUN]" if dry_run else ""

    print(f"\nCompounding x Format Experiment{dry_tag}")
    print(f"Pipeline runs: {n_pipeline} (x3 steps = {n_pipeline * 3} calls)")
    print(f"Control calls: {n_control}")
    print(f"Total API calls: {total_api_calls}")
    if not dry_run:
        print(
            f"Estimated time: ~{total_api_calls * (INTER_CALL_DELAY + 2) / 60:.0f} min"
        )
    print(f"Output: {jsonl_path}\n")

    all_records: list[dict] = []
    total_cost = 0.0
    errors = 0

    print("=== Pipeline Phase ===")
    for i, item in enumerate(work_items):
        print(
            f"\n[Pipeline {i+1}/{len(work_items)}] "
            f"{item['brand']} / {item['model']} / rep {item['rep']} "
            f"/ {item['bf_condition']}"
        )
        recs = run_pipeline(
            brand=item["brand"],
            model_name=item["model"],
            rep=item["rep"],
            call_idx=item["pipeline_idx"],
            bf_condition=item["bf_condition"],
            jsonl_path=jsonl_path,
            dry_run=dry_run,
        )
        all_records.extend(recs)
        for r in recs:
            total_cost += r.get("api_cost_usd", 0)
            if r["step"] != 1 and not r["weights_valid"]:
                errors += 1

    print("\n=== Control Phase ===")
    for i, item in enumerate(work_items):
        print(f"\n[Control {i+1}/{len(work_items)}]")
        rec = run_control(
            brand=item["brand"],
            model_name=item["model"],
            rep=item["rep"],
            call_idx=item["control_idx"],
            bf_condition=item["bf_condition"],
            jsonl_path=jsonl_path,
            dry_run=dry_run,
        )
        all_records.append(rec)
        total_cost += rec.get("api_cost_usd", 0)
        if not rec["weights_valid"]:
            errors += 1

    valid_weight_records = sum(1 for r in all_records if r["weights_valid"])
    total_records = len(all_records)
    weight_bearing = sum(1 for r in all_records if r["step"] != 1)

    print(f"\n{'='*60}")
    print(f"Compounding x Format -- COMPLETE{dry_tag}")
    print(f"{'='*60}")
    print(f"Total records: {total_records}")
    print(f"Weight-bearing records: {weight_bearing}")
    print(
        f"Valid weights: {valid_weight_records}/{weight_bearing} "
        f"({100*valid_weight_records/max(weight_bearing, 1):.1f}%)"
    )
    print(f"Parse errors: {errors}")
    if not dry_run:
        print(f"Total cost: ${total_cost:.4f}")
    print(f"Output: {jsonl_path}")

    # Brief condition breakdown
    for bf_cond in ("baseline", "specified"):
        cond_recs = [r for r in all_records if r.get("bf_condition") == bf_cond]
        valid = sum(1 for r in cond_recs if r["weights_valid"] and r["step"] != 1)
        weight_bear = sum(1 for r in cond_recs if r["step"] != 1)
        print(
            f"  {bf_cond}: {len(cond_recs)} records, "
            f"{valid}/{weight_bear} weight-bearing valid"
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compounding x Format: Brand Function spec in agentic pipeline"
    )
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Offline validation: build all prompts, write stub JSONL, no API calls",
    )
    mode_group.add_argument(
        "--smoke",
        action="store_true",
        help="Smoke test: 1 brand x 1 model x 1 rep x 2 conditions (~8 calls)",
    )
    mode_group.add_argument(
        "--live",
        action="store_true",
        help="Full run: 5 brands x 6 models x 2 reps x 2 conditions (~480 calls)",
    )
    args = parser.parse_args()

    if args.dry_run:
        mode = "live"  # use full brand/model set to validate all paths
        dry_run = True
    elif args.smoke:
        mode = "smoke"
        dry_run = False
    else:
        mode = "live"
        dry_run = False

    mode_label = "dry-run" if dry_run else mode
    print(f"Compounding x Format Experiment ({mode_label})")
    print(f"Temperature: {TEMPERATURE}")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Inter-call delay: {INTER_CALL_DELAY}s")
    print()

    run_experiment(mode=mode, dry_run=dry_run)


if __name__ == "__main__":
    main()
