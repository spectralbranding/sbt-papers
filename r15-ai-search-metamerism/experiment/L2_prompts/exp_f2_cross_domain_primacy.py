#!/usr/bin/env python3
"""Experiment F2: Cross-Domain Primacy.

Tests whether the serial position primacy effect found in brand perception
(Exp E, d=1.39 JSON / d=.22 Likert) generalizes to political attitude
measurement using adapted Moral Foundations Theory dimensions.

Design: 2 (domain: brand, political) x 2 (format: JSON, Likert)
        x 8 (orderings) x 5 (stimuli) x 5 (models) x 1 (rep) = 800 calls

Protocol: L0_specification/EXP_F2_CROSS_DOMAIN_PRIMACY_PROTOCOL.md
Paper: R15 extension or PRISM instrument validity paper

Usage:
    uv run python exp_f2_cross_domain_primacy.py --dry-run   # print plan, no calls
    uv run python exp_f2_cross_domain_primacy.py --smoke     # ~20 calls, verify setup
    uv run python exp_f2_cross_domain_primacy.py --live      # 800 calls, full run
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

EXPERIMENT_ID = "f2_cross_domain_primacy"
PROMPT_TYPE = "primacy_cross_domain"

# SBT dimensions (brand domain)
SBT_DIMENSIONS = [
    "Semiotic",
    "Narrative",
    "Ideological",
    "Experiential",
    "Social",
    "Economic",
    "Cultural",
    "Temporal",
]

# MFT dimensions (political domain), short names used as keys
MFT_DIMENSIONS = [
    "Care/Harm",
    "Fairness/Cheating",
    "Loyalty/Betrayal",
    "Authority/Subversion",
    "Sanctity/Degradation",
    "Liberty/Oppression",
    "Efficiency/Waste",
    "Tradition/Progress",
]

# MFT dimension descriptions for prompt context
MFT_DESCRIPTIONS = {
    "Care/Harm": "sensitivity to suffering",
    "Fairness/Cheating": "proportionality and justice",
    "Loyalty/Betrayal": "group solidarity",
    "Authority/Subversion": "respect for hierarchy",
    "Sanctity/Degradation": "purity concerns",
    "Liberty/Oppression": "freedom from constraint",
    "Efficiency/Waste": "resource optimization",
    "Tradition/Progress": "preservation vs change",
}

# Canonical brand stimuli
BRANDS = ["Hermes", "IKEA", "Patagonia", "Erewhon", "Tesla"]

# Policy scenario stimuli (ID -> text)
POLICY_SCENARIOS = {
    "P1": (
        "Universal basic income: providing every citizen $1,000/month "
        "regardless of employment"
    ),
    "P2": (
        "Immigration policy: reducing visa processing time from 18 months "
        "to 3 months"
    ),
    "P3": (
        "Carbon tax: $50/ton on all fossil fuel emissions, revenue returned "
        "as dividend"
    ),
    "P4": (
        "Military spending: increasing defense budget by 15% with cuts "
        "to education"
    ),
    "P5": (
        "Social media: requiring platforms to remove harmful content "
        "within 24 hours"
    ),
}

RESPONSE_FORMATS = ["json", "likert"]

# Latin-square cyclic orderings (8 rotations, same logic for both dimension sets)
def _make_latin_square(dims: list[str]) -> list[list[str]]:
    return [dims[i:] + dims[:i] for i in range(8)]

LATIN_SQUARE_SBT = _make_latin_square(SBT_DIMENSIONS)
LATIN_SQUARE_MFT = _make_latin_square(MFT_DIMENSIONS)

DOMAIN_TO_LATIN_SQUARE = {
    "brand": LATIN_SQUARE_SBT,
    "political": LATIN_SQUARE_MFT,
}

SYSTEM_PROMPT = (
    "You are a research assistant participating in a social science study. "
    "Answer honestly based on the information provided."
)


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
# Utilities
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


# ---------------------------------------------------------------------------
# API Callers
# ---------------------------------------------------------------------------


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
        return _call_openai(model_id, system_prompt, user_prompt, max_tokens, None, None)
    elif provider == "google":
        return _call_google(model_id, system_prompt, user_prompt, max_tokens)
    elif provider == "deepseek":
        return _call_openai(
            model_id, system_prompt, user_prompt, max_tokens,
            os.environ["DEEPSEEK_API_KEY"], "https://api.deepseek.com",
        )
    elif provider == "xai":
        return _call_openai(
            model_id, system_prompt, user_prompt, max_tokens,
            os.environ["GROK_API_KEY"], "https://api.x.ai/v1",
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

    kwargs: dict[str, Any] = {}
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
    t0 = time.time()
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=max_tokens,
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
                max_output_tokens=max_tokens,
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


def _json_template(dim_order: list[str]) -> str:
    """JSON template for weight allocation (sum to 100)."""
    return "{" + ", ".join(f'"{d}": <weight>' for d in dim_order) + "}"


def _likert_template(dim_order: list[str]) -> str:
    """JSON template for Likert 1-5 ratings."""
    return "{" + ", ".join(f'"{d}": <1-5>' for d in dim_order) + "}"


def build_brand_json_prompt(brand: str, dim_order: list[str]) -> str:
    """Brand JSON allocation prompt."""
    tmpl = _json_template(dim_order)
    return (
        f"Consider the brand {brand}. Allocate 100 points across these 8 dimensions "
        f"reflecting their importance to this brand:\n"
        f"{', '.join(dim_order)}\n"
        f"The weights must sum to 100. Respond in this exact JSON format:\n{tmpl}"
    )


def build_brand_likert_prompt(brand: str, dim_order: list[str]) -> str:
    """Brand Likert 1-5 prompt."""
    tmpl = _likert_template(dim_order)
    return (
        f"Consider the brand {brand}. Rate this brand on each of the following "
        f"8 dimensions using a scale of 1-5 "
        f"(1 = not at all important to this brand, 5 = extremely important to this brand):\n"
        f"{', '.join(dim_order)}\n"
        f"Respond in this exact JSON format:\n{tmpl}"
    )


def build_political_json_prompt(scenario: str, dim_order: list[str]) -> str:
    """Political JSON allocation prompt."""
    tmpl = _json_template(dim_order)
    # Include brief descriptions for MFT dimensions to reduce ambiguity
    dim_lines = "\n".join(
        f"- {d} ({MFT_DESCRIPTIONS[d]})" for d in dim_order
    )
    return (
        f"Consider this policy: {scenario}\n"
        f"Allocate 100 points across these 8 moral dimensions reflecting their "
        f"relevance to evaluating this policy:\n"
        f"{dim_lines}\n"
        f"The weights must sum to 100. Respond in this exact JSON format:\n{tmpl}"
    )


def build_political_likert_prompt(scenario: str, dim_order: list[str]) -> str:
    """Political Likert 1-5 prompt."""
    tmpl = _likert_template(dim_order)
    dim_lines = "\n".join(
        f"- {d} ({MFT_DESCRIPTIONS[d]})" for d in dim_order
    )
    return (
        f"Consider this policy: {scenario}\n"
        f"Rate the relevance of each of the following 8 dimensions to evaluating "
        f"this policy using a scale of 1-5 "
        f"(1 = not at all relevant, 5 = extremely relevant):\n"
        f"{dim_lines}\n"
        f"Respond in this exact JSON format:\n{tmpl}"
    )


def build_prompt(
    domain: str,
    stimulus: str,
    response_format: str,
    dim_order: list[str],
) -> str:
    """Dispatch to the appropriate prompt builder."""
    if domain == "brand":
        if response_format == "json":
            return build_brand_json_prompt(stimulus, dim_order)
        else:
            return build_brand_likert_prompt(stimulus, dim_order)
    else:  # political
        scenario_text = POLICY_SCENARIOS[stimulus]
        if response_format == "json":
            return build_political_json_prompt(scenario_text, dim_order)
        else:
            return build_political_likert_prompt(scenario_text, dim_order)


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------


def _extract_json_object(raw: str) -> Optional[dict]:
    """Extract the first JSON object from raw text."""
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
        return json.loads(text[start:end])
    except json.JSONDecodeError:
        return None


def parse_json_weights(
    raw: str, dim_order: list[str]
) -> Optional[dict[str, float]]:
    """Parse JSON allocation response (weights sum to 100)."""
    data = _extract_json_object(raw)
    if data is None:
        return None

    if "weights" in data and isinstance(data["weights"], dict):
        data = data["weights"]

    result: dict[str, float] = {}
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
    """Parse Likert 1-5 response. Returns weights normalized to 0-100 scale."""
    weights = parse_json_weights(raw, dim_order)
    if weights is None:
        return None

    for val in weights.values():
        if val < 1 or val > 5 or val != int(val):
            return None

    total = sum(weights.values())
    if total == 0:
        return None
    return {dim: round(v / total * 100, 2) for dim, v in weights.items()}


def parse_response(
    raw: str, dim_order: list[str], response_format: str
) -> Optional[dict[str, float]]:
    if response_format == "json":
        return parse_json_weights(raw, dim_order)
    else:
        return parse_likert_response(raw, dim_order)


def compute_position_weights(
    parsed: dict[str, float], dim_order: list[str]
) -> dict[int, float]:
    """Map dimension weights to prompt positions (1-indexed)."""
    return {
        pos + 1: parsed.get(dim, 0.0)
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
    domain: str,
    stimulus: str,
    response_format: str,
    ordering_index: int,
    dim_order: list[str],
    user_prompt: str,
    raw_response: str,
    parsed: Optional[dict[str, float]],
    meta: dict[str, Any],
) -> dict:
    """Build a JSONL record conforming to EXPERIMENT_DATA_STANDARD.md."""
    cfg = MODELS[model_name]
    weights_valid = parsed is not None
    weight_sum = round(sum(parsed.values()), 2) if parsed else 0.0
    position_weights = (
        compute_position_weights(parsed, dim_order) if parsed else None
    )
    dimension_set = "sbt" if domain == "brand" else "mft"

    return {
        # --- Required fields (EXPERIMENT_DATA_STANDARD.md) ---
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model": model_name,
        "prompt_type": PROMPT_TYPE,
        "prompt": user_prompt,
        # --- Recommended fields ---
        "model_id": cfg["model_id"],
        "response": raw_response,
        "parsed": parsed,
        "latency_ms": meta.get("response_time_ms", 0),
        "tokens_in": meta.get("token_count_input", 0),
        "tokens_out": meta.get("token_count_output", 0),
        "error": None,
        "temperature": TEMPERATURE,
        # --- Experiment-specific fields ---
        "domain": domain,
        "stimulus": stimulus,
        "response_format": response_format,
        "dimension_order": dim_order,
        "ordering_index": ordering_index,
        "dimension_set": dimension_set,
        "position_weights": position_weights,
        "weights_valid": weights_valid,
        "weight_sum_raw": weight_sum,
        "system_prompt": SYSTEM_PROMPT,
        "system_prompt_hash": _sha256(SYSTEM_PROMPT),
        "user_prompt_hash": _sha256(user_prompt),
        "api_cost_usd": meta.get("api_cost_usd", 0.0),
    }


def make_error_record(
    model_name: str,
    domain: str,
    stimulus: str,
    response_format: str,
    ordering_index: int,
    dim_order: list[str],
    user_prompt: str,
    error_msg: str,
) -> dict:
    """Build a JSONL record for a failed API call."""
    cfg = MODELS[model_name]
    dimension_set = "sbt" if domain == "brand" else "mft"
    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model": model_name,
        "prompt_type": PROMPT_TYPE,
        "prompt": user_prompt,
        "model_id": cfg["model_id"],
        "response": None,
        "parsed": None,
        "latency_ms": 0,
        "tokens_in": 0,
        "tokens_out": 0,
        "error": error_msg,
        "temperature": TEMPERATURE,
        "domain": domain,
        "stimulus": stimulus,
        "response_format": response_format,
        "dimension_order": dim_order,
        "ordering_index": ordering_index,
        "dimension_set": dimension_set,
        "position_weights": None,
        "weights_valid": False,
        "weight_sum_raw": 0.0,
        "system_prompt": SYSTEM_PROMPT,
        "system_prompt_hash": _sha256(SYSTEM_PROMPT),
        "user_prompt_hash": _sha256(user_prompt),
        "api_cost_usd": 0.0,
    }


# ---------------------------------------------------------------------------
# Trial Generation
# ---------------------------------------------------------------------------


def get_stimuli_for_domain(domain: str) -> list[str]:
    if domain == "brand":
        return BRANDS
    return list(POLICY_SCENARIOS.keys())


def generate_trials(smoke: bool = False) -> list[dict]:
    """Generate all trial specifications.

    Full design: 2 domains x 2 formats x 8 orderings x 5 stimuli x 5 models = 800
    Smoke test:  2 domains x 2 formats x 1 ordering x 1 stimulus x available models
    """
    available = {
        name: cfg
        for name, cfg in MODELS.items()
        if os.environ.get(cfg["api_key_env"])
    }

    if not available:
        raise RuntimeError("No API keys found. Set at least one model's env var.")

    model_names = sorted(available.keys())
    orderings = list(range(8)) if not smoke else [0]
    domains = ["brand", "political"]
    formats = RESPONSE_FORMATS

    trials = []
    for domain in domains:
        stimuli = get_stimuli_for_domain(domain)
        if smoke:
            stimuli = stimuli[:1]
        for fmt in formats:
            for ord_idx in orderings:
                for stimulus in stimuli:
                    for model_name in model_names:
                        trials.append({
                            "domain": domain,
                            "response_format": fmt,
                            "ordering_index": ord_idx,
                            "stimulus": stimulus,
                            "model_name": model_name,
                        })

    # Shuffle to spread load across providers
    import random
    random.seed(RANDOM_SEED)
    random.shuffle(trials)
    return trials


# ---------------------------------------------------------------------------
# Dry Run
# ---------------------------------------------------------------------------


def print_dry_run() -> None:
    """Print experiment plan without making any API calls."""
    available = {
        name: cfg
        for name, cfg in MODELS.items()
        if os.environ.get(cfg["api_key_env"])
    }

    print(f"\n{'='*65}")
    print(f"Experiment F2: Cross-Domain Primacy -- DRY RUN")
    print(f"{'='*65}")
    print(f"\nDesign:")
    print(f"  2 domains (brand, political)")
    print(f"  2 formats (json, likert)")
    print(f"  8 dimension orderings (Latin-square cyclic)")
    print(f"  5 stimuli per domain")
    print(f"  5 models")
    print(f"  1 repetition")
    print(f"  = 800 total calls (full run)")

    print(f"\nAvailable models ({len(available)} of {len(MODELS)}):")
    for name, cfg in sorted(available.items()):
        print(f"  {name:12s} ({cfg['model_id']})")
    if len(available) < len(MODELS):
        missing = [n for n in MODELS if n not in available]
        print(f"  Missing keys: {', '.join(missing)}")

    print(f"\nBrand stimuli: {', '.join(BRANDS)}")
    print(f"Political stimuli:")
    for pid, text in POLICY_SCENARIOS.items():
        print(f"  {pid}: {text[:60]}...")

    print(f"\nSBT dimensions: {', '.join(SBT_DIMENSIONS)}")
    print(f"MFT dimensions: {', '.join(MFT_DESCRIPTIONS.keys())}")

    print(f"\nSample prompts (ordering 0):")
    print(f"\n  [brand / json / Hermes / ord=0]")
    p = build_prompt("brand", "Hermes", "json", LATIN_SQUARE_SBT[0])
    print("  " + p[:200].replace("\n", "\n  "))

    print(f"\n  [political / json / P1 / ord=0]")
    p = build_prompt("political", "P1", "json", LATIN_SQUARE_MFT[0])
    print("  " + p[:300].replace("\n", "\n  "))

    print(f"\n  [political / likert / P3 / ord=3]")
    p = build_prompt("political", "P3", "likert", LATIN_SQUARE_MFT[3])
    print("  " + p[:300].replace("\n", "\n  "))

    print(f"\nOutput: L3_sessions/exp_f2_cross_domain_primacy.jsonl")
    print(f"{'='*65}\n")


# ---------------------------------------------------------------------------
# Main Execution Loop
# ---------------------------------------------------------------------------


def run_experiment(smoke: bool = False) -> dict:
    """Execute the full experiment."""
    trials = generate_trials(smoke=smoke)

    output_dir = Path(__file__).parent.parent / "L3_sessions"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "exp_f2_cross_domain_primacy.jsonl"

    print(f"\n{'='*65}")
    print(f"Experiment F2: Cross-Domain Primacy")
    print(f"{'='*65}")
    print(f"Trials: {len(trials)}")
    print(f"Output: {output_path}")
    print(f"Mode: {'SMOKE TEST' if smoke else 'LIVE'}")
    print(f"{'='*65}\n")

    stats: dict[str, Any] = {
        "total_calls": 0,
        "successful": 0,
        "failed": 0,
        "parse_errors": 0,
        "total_cost": 0.0,
        "per_model": {},
        "per_domain": {},
        "per_format": {},
    }

    for trial_idx, trial in enumerate(trials):
        domain = trial["domain"]
        fmt = trial["response_format"]
        ord_idx = trial["ordering_index"]
        stimulus = trial["stimulus"]
        model_name = trial["model_name"]

        latin_sq = DOMAIN_TO_LATIN_SQUARE[domain]
        dim_order = latin_sq[ord_idx]

        stats["total_calls"] += 1
        model_stats = stats["per_model"].setdefault(
            model_name, {"calls": 0, "success": 0, "failed": 0, "cost": 0.0}
        )
        domain_stats = stats["per_domain"].setdefault(
            domain, {"calls": 0, "success": 0, "failed": 0}
        )
        fmt_stats = stats["per_format"].setdefault(
            fmt, {"calls": 0, "success": 0, "failed": 0}
        )
        model_stats["calls"] += 1
        domain_stats["calls"] += 1
        fmt_stats["calls"] += 1

        user_prompt = build_prompt(domain, stimulus, fmt, dim_order)

        print(
            f"  [{stats['total_calls']:4d}/{len(trials)}] "
            f"{model_name:10s} | {domain:10s} | {stimulus:8s} | "
            f"{fmt:6s} | ord={ord_idx}",
            end="",
            flush=True,
        )

        try:
            raw_response, meta = call_api(model_name, SYSTEM_PROMPT, user_prompt)
            parsed = parse_response(raw_response, dim_order, fmt)

            record = make_record(
                model_name=model_name,
                domain=domain,
                stimulus=stimulus,
                response_format=fmt,
                ordering_index=ord_idx,
                dim_order=dim_order,
                user_prompt=user_prompt,
                raw_response=raw_response,
                parsed=parsed,
                meta=meta,
            )
            append_jsonl(output_path, record)

            cost = meta.get("api_cost_usd", 0.0)
            stats["total_cost"] += cost
            model_stats["cost"] += cost

            if parsed:
                stats["successful"] += 1
                model_stats["success"] += 1
                domain_stats["success"] += 1
                fmt_stats["success"] += 1
                pos_w = compute_position_weights(parsed, dim_order)
                primacy = (pos_w[1] + pos_w[2]) / 2
                recency = (pos_w[7] + pos_w[8]) / 2
                print(f" | OK p1-2={primacy:.1f} p7-8={recency:.1f}")
            else:
                stats["parse_errors"] += 1
                model_stats["failed"] += 1
                domain_stats["failed"] += 1
                fmt_stats["failed"] += 1
                print(f" | PARSE_ERROR")

        except Exception as e:
            stats["failed"] += 1
            model_stats["failed"] += 1
            domain_stats["failed"] += 1
            fmt_stats["failed"] += 1
            print(f" | ERROR: {e}")

            record = make_error_record(
                model_name=model_name,
                domain=domain,
                stimulus=stimulus,
                response_format=fmt,
                ordering_index=ord_idx,
                dim_order=dim_order,
                user_prompt=user_prompt,
                error_msg=str(e),
            )
            append_jsonl(output_path, record)

        time.sleep(INTER_CALL_DELAY)

    # Summary
    print(f"\n{'='*65}")
    print(f"COMPLETE")
    print(f"{'='*65}")
    print(f"Total calls:  {stats['total_calls']}")
    print(f"Successful:   {stats['successful']}")
    print(f"Parse errors: {stats['parse_errors']}")
    print(f"API errors:   {stats['failed']}")
    print(f"Total cost:   ${stats['total_cost']:.2f}")
    print(f"\nPer model:")
    for m, s in sorted(stats["per_model"].items()):
        print(f"  {m:12s}: {s['success']}/{s['calls']} ok, ${s['cost']:.3f}")
    print(f"\nPer domain:")
    for d, s in sorted(stats["per_domain"].items()):
        print(f"  {d:10s}: {s['success']}/{s['calls']} ok")
    print(f"\nPer format:")
    for f, s in sorted(stats["per_format"].items()):
        print(f"  {f:8s}: {s['success']}/{s['calls']} ok")
    print(f"{'='*65}\n")

    # Save run summary
    summary_path = (
        Path(__file__).parent.parent / "L4_analysis" / "exp_f2_cross_domain_primacy_run_summary.json"
    )
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w") as f:
        json.dump(stats, f, indent=2)

    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Experiment F2: Cross-Domain Primacy"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Print plan and sample prompts, make no API calls",
    )
    group.add_argument(
        "--smoke",
        action="store_true",
        help="Smoke test (~20 calls, verify setup)",
    )
    group.add_argument(
        "--live",
        action="store_true",
        help="Full run (800 calls)",
    )
    args = parser.parse_args()

    if args.dry_run:
        print_dry_run()
    else:
        run_experiment(smoke=args.smoke)
