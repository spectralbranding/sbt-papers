#!/usr/bin/env python3
"""Experiment C: Competitive Interference in Perception Space

Tests whether the presence of a competitor alters a brand's spectral profile
in LLM-mediated perception, and whether shift magnitude depends on competitor
proximity in perception space.

Paper target: R4 (Sphere Packing Capacity) extension
Open Problem: Extends R4 sphere packing capacity

Usage:
    python exp_competitive_interference.py --smoke   # 1 brand, 1 model, 1 condition
    python exp_competitive_interference.py --live    # Full experiment (~225 calls)

License: MIT
"""

import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import numpy as np

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RANDOM_SEED = 42
TEMPERATURE = 0.7
INTER_CALL_DELAY = 3.0  # seconds between API calls
MAX_RETRIES = 4
BACKOFF_DELAYS = [5, 10, 20, 60]  # exponential backoff on 429

DIMENSIONS = [
    "semiotic", "narrative", "ideological", "experiential",
    "social", "economic", "cultural", "temporal",
]

DIMENSION_DESCRIPTIONS = {
    "semiotic": "visual identity, logos, packaging, design language",
    "narrative": "brand story, origin myth, founding narrative",
    "ideological": "values, ethics, social causes, environmental stance",
    "experiential": "customer experience quality, service, unboxing",
    "social": "social signaling, community, what owning it says about you",
    "economic": "price, value for money, pricing strategy",
    "cultural": "cultural relevance, connection to movements/traditions",
    "temporal": "heritage, history, relationship to time",
}

# Canonical brand profiles (from CLAUDE.md)
CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

# Competitor pairings: focal -> {type: competitor}
COMPETITOR_PAIRINGS = {
    "Hermes": {
        "direct": "Louis Vuitton",
        "adjacent": "Rolex",
        "distant": "Walmart",
    },
    "IKEA": {
        "direct": "H&M Home",
        "adjacent": "Muji",
        "distant": "Ferrari",
    },
    "Patagonia": {
        "direct": "Arc'teryx",
        "adjacent": "REI",
        "distant": "Shein",
    },
    "Erewhon": {
        "direct": "Whole Foods",
        "adjacent": "Blue Bottle",
        "distant": "McDonald's",
    },
    "Tesla": {
        "direct": "Rivian",
        "adjacent": "Apple",
        "distant": "Toyota",
    },
}

# Standard models (from spec)
MODELS = {
    "claude": {
        "id": "claude-haiku-4-5-20251001",
        "display": "Claude Haiku 4.5",
        "env_key": "ANTHROPIC_API_KEY",
    },
    "gpt": {
        "id": "gpt-4o-mini",
        "display": "GPT-4o-mini",
        "env_key": "OPENAI_API_KEY",
    },
    "gemini": {
        "id": "gemini-2.5-flash",
        "display": "Gemini 2.5 Flash",
        "env_key": "GOOGLE_API_KEY",
    },
    "deepseek": {
        "id": "deepseek-chat",
        "display": "DeepSeek V3",
        "env_key": "DEEPSEEK_API_KEY",
    },
    "grok": {
        "id": "grok-4-1-fast-non-reasoning",
        "display": "Grok 4.1 Fast",
        "env_key": "GROK_API_KEY",
    },
}

# Latin-square orderings (8 cyclic rotations)
LATIN_SQUARE = []
for i in range(8):
    LATIN_SQUARE.append(DIMENSIONS[i:] + DIMENSIONS[:i])


# ---------------------------------------------------------------------------
# Prompt Construction
# ---------------------------------------------------------------------------

def _dim_block(ordering_idx: int) -> str:
    """Return formatted dimension list in the given Latin-square ordering."""
    order = LATIN_SQUARE[ordering_idx % 8]
    lines = []
    for dim in order:
        lines.append(f"- {dim.capitalize()}: {DIMENSION_DESCRIPTIONS[dim]}")
    return "\n".join(lines)


def _dim_json_example(ordering_idx: int) -> str:
    """Return JSON example keys in the given ordering."""
    order = LATIN_SQUARE[ordering_idx % 8]
    parts = []
    for dim in order:
        parts.append(f'    "{dim}": <number>')
    return "{\n" + ",\n".join(parts) + "\n  }"


SOLO_PROMPT = (
    "You are evaluating brand perception.\n\n"
    "Evaluate the brand {brand} by allocating importance weights across "
    "eight perception dimensions. Weights must sum to 100.\n\n"
    "Dimensions:\n{dim_block}\n\n"
    "Respond with ONLY valid JSON:\n"
    '{{\n'
    '  "brand": "{brand}",\n'
    '  "weights": {weights_example},\n'
    '  "reasoning": "1-2 sentence explanation"\n'
    '}}\n\n'
    "The weights MUST sum to exactly 100."
)

PAIRED_PROMPT = (
    "You are evaluating brand perception.\n\n"
    "Evaluate the brand {brand} compared to {competitor} by allocating "
    "importance weights across eight perception dimensions. The weights "
    "should reflect how {brand} is perceived when directly compared to "
    "{competitor}. Weights must sum to 100.\n\n"
    "Dimensions:\n{dim_block}\n\n"
    "Respond with ONLY valid JSON:\n"
    '{{\n'
    '  "brand": "{brand}",\n'
    '  "compared_to": "{competitor}",\n'
    '  "weights": {weights_example},\n'
    '  "reasoning": "1-2 sentence explanation"\n'
    '}}\n\n'
    "The weights MUST sum to exactly 100."
)

CONTEXT_PROMPT = (
    "You are evaluating brand perception.\n\n"
    "Evaluate the brand {brand} in a market that also includes "
    "{competitor}. Allocate importance weights across eight perception "
    "dimensions reflecting how {brand} is perceived in this competitive "
    "context. Weights must sum to 100.\n\n"
    "Dimensions:\n{dim_block}\n\n"
    "Respond with ONLY valid JSON:\n"
    '{{\n'
    '  "brand": "{brand}",\n'
    '  "market_includes": "{competitor}",\n'
    '  "weights": {weights_example},\n'
    '  "reasoning": "1-2 sentence explanation"\n'
    '}}\n\n'
    "The weights MUST sum to exactly 100."
)


def build_prompt(
    brand: str,
    condition: str,
    competitor: Optional[str],
    ordering_idx: int,
) -> str:
    """Build the appropriate prompt for the given condition."""
    dim_block = _dim_block(ordering_idx)
    weights_example = _dim_json_example(ordering_idx)

    if condition == "solo":
        return SOLO_PROMPT.format(
            brand=brand,
            dim_block=dim_block,
            weights_example=weights_example,
        )
    elif condition == "paired":
        return PAIRED_PROMPT.format(
            brand=brand,
            competitor=competitor,
            dim_block=dim_block,
            weights_example=weights_example,
        )
    elif condition == "context":
        return CONTEXT_PROMPT.format(
            brand=brand,
            competitor=competitor,
            dim_block=dim_block,
            weights_example=weights_example,
        )
    else:
        raise ValueError(f"Unknown condition: {condition}")


# ---------------------------------------------------------------------------
# JSON Parsing (from R15)
# ---------------------------------------------------------------------------

def parse_llm_json(text: str) -> dict[str, Any]:
    """Robustly parse JSON from LLM response text."""
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    brace_start = text.find("{")
    if brace_start != -1:
        depth = 0
        brace_end = -1
        for i, ch in enumerate(text[brace_start:], start=brace_start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    brace_end = i
                    break
        if brace_end != -1:
            candidate = text[brace_start:brace_end + 1]
            candidate = re.sub(r",\s*([}\]])", r"\1", candidate)
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

    raise ValueError(f"Could not parse JSON from LLM response: {text[:300]}")


def parse_weights(parsed: dict) -> Optional[dict[str, float]]:
    """Extract and validate 8-dimension weight dict."""
    weights_raw = parsed.get("weights")
    if not isinstance(weights_raw, dict):
        return None

    result: dict[str, float] = {}
    for dim in DIMENSIONS:
        val = weights_raw.get(dim)
        if val is None:
            return None
        try:
            result[dim] = float(val)
        except (TypeError, ValueError):
            return None

    total = sum(result.values())
    if total < 1e-6:
        return None
    if abs(total - 100.0) > 15.0:
        return None
    if abs(total - 100.0) > 0.01:
        result = {d: v * 100.0 / total for d, v in result.items()}

    return result


# ---------------------------------------------------------------------------
# Model-Specific API Callers
# ---------------------------------------------------------------------------

def call_claude(prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        temperature=TEMPERATURE,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def call_gpt(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content


def call_gemini(prompt: str) -> str:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=2048,
                response_mime_type="application/json",
                system_instruction="You are a brand research assistant. Respond with valid JSON only.",
            ),
        )
        text = response.text
        if text and text.strip():
            return text
    except Exception:
        pass
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE, max_output_tokens=2048
        ),
    )
    try:
        return response.text
    except Exception:
        if response.candidates:
            return response.candidates[0].content.parts[0].text
        raise ValueError("Gemini returned no usable response")


def call_deepseek(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content


def call_grok(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["GROK_API_KEY"],
        base_url="https://api.x.ai/v1",
    )
    response = client.chat.completions.create(
        model="grok-4-1-fast-non-reasoning",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content


MODEL_CALLERS = {
    "claude": call_claude,
    "gpt": call_gpt,
    "gemini": call_gemini,
    "deepseek": call_deepseek,
    "grok": call_grok,
}


# ---------------------------------------------------------------------------
# API Call with Retry
# ---------------------------------------------------------------------------

def call_model(model_name: str, prompt: str) -> tuple[str, int, Optional[str]]:
    """Call a model with exponential backoff on rate limits.

    Returns (response_text, latency_ms, error_or_none).
    """
    caller = MODEL_CALLERS[model_name]
    for attempt in range(MAX_RETRIES + 1):
        try:
            t0 = time.time()
            response = caller(prompt)
            latency_ms = int((time.time() - t0) * 1000)
            return response, latency_ms, None
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "rate" in err_str.lower():
                if attempt < MAX_RETRIES:
                    delay = BACKOFF_DELAYS[attempt]
                    print(f"  Rate limited ({model_name}), backing off {delay}s...")
                    time.sleep(delay)
                    continue
            return "", 0, f"Error on attempt {attempt + 1}: {err_str[:500]}"
    return "", 0, "Max retries exceeded"


# ---------------------------------------------------------------------------
# Experiment Execution
# ---------------------------------------------------------------------------

def get_available_models() -> list[str]:
    """Return list of model names with available API keys."""
    available = []
    for name, info in MODELS.items():
        if os.environ.get(info["env_key"]):
            available.append(name)
    return available


def run_experiment(
    output_path: Path,
    smoke: bool = False,
) -> dict:
    """Execute the full competitive interference experiment."""
    rng = np.random.RandomState(RANDOM_SEED)

    available_models = get_available_models()
    if not available_models:
        print("ERROR: No API keys found. Set at least one of:")
        for name, info in MODELS.items():
            print(f"  {info['env_key']}")
        sys.exit(1)

    print(f"Available models: {', '.join(available_models)}")

    brands = list(CANONICAL_PROFILES.keys())
    if smoke:
        brands = brands[:1]
        available_models = available_models[:1]

    # Build call schedule
    calls = []
    call_idx = 0

    # Solo baselines (3 reps per brand per model)
    solo_reps = 1 if smoke else 3
    for brand in brands:
        for model_name in available_models:
            for rep in range(solo_reps):
                ordering_idx = call_idx % 8
                calls.append({
                    "brand": brand,
                    "condition": "solo",
                    "competitor": None,
                    "competitor_type": None,
                    "model": model_name,
                    "run": rep + 1,
                    "ordering_idx": ordering_idx,
                })
                call_idx += 1

    # Self-comparison control: focal brand compared to itself
    # If this produces different weights from solo, the prompt format
    # itself introduces bias; competitor effects must be measured as
    # delta ABOVE this baseline.
    for brand in brands:
        for model_name in available_models:
            ordering_idx = call_idx % 8
            calls.append({
                "brand": brand,
                "condition": "paired",
                "competitor": brand,  # self-comparison
                "competitor_type": "self",
                "model": model_name,
                "run": 1,
                "ordering_idx": ordering_idx,
            })
            call_idx += 1

    # Competitive conditions (paired + context, 1 rep each)
    comp_reps = 1
    for brand in brands:
        for comp_type, competitor in COMPETITOR_PAIRINGS[brand].items():
            if smoke and comp_type != "direct":
                continue
            for condition in ["paired", "context"]:
                for model_name in available_models:
                    for rep in range(comp_reps):
                        ordering_idx = call_idx % 8
                        calls.append({
                            "brand": brand,
                            "condition": condition,
                            "competitor": competitor,
                            "competitor_type": comp_type,
                            "model": model_name,
                            "run": rep + 1,
                            "ordering_idx": ordering_idx,
                        })
                        call_idx += 1

    # Shuffle to distribute load across providers
    rng.shuffle(calls)

    print(f"\nTotal calls scheduled: {len(calls)}")
    print(f"Output: {output_path}")
    print()

    # Execute calls
    results = []
    success_count = 0
    error_count = 0

    with open(output_path, "w") as f:
        for i, call in enumerate(calls):
            brand = call["brand"]
            condition = call["condition"]
            competitor = call["competitor"]
            model_name = call["model"]
            ordering_idx = call["ordering_idx"]

            prompt = build_prompt(brand, condition, competitor, ordering_idx)

            comp_str = f" vs {competitor} ({call['competitor_type']})" if competitor else ""
            print(
                f"[{i+1}/{len(calls)}] {model_name}: {brand}{comp_str} "
                f"({condition}) order={ordering_idx}",
                end=" ... ",
                flush=True,
            )

            response_text, latency_ms, error = call_model(model_name, prompt)

            # Parse response
            parsed = {}
            weights = None
            if not error:
                try:
                    parsed = parse_llm_json(response_text)
                    weights = parse_weights(parsed)
                    if weights is None:
                        error = "Could not extract valid weights"
                except Exception as e:
                    error = f"Parse error: {str(e)[:300]}"

            if error:
                error_count += 1
                print(f"ERROR: {error[:80]}")
            else:
                success_count += 1
                w = weights
                top_dim = max(w, key=w.get)
                print(f"OK (top: {top_dim}={w[top_dim]:.1f}, latency={latency_ms}ms)")

            # Build JSONL record (20 standard + 3 experiment-specific fields)
            record = {
                "timestamp": datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat(),
                "model": model_name,
                "model_id": MODELS[model_name]["id"],
                "prompt_type": f"{condition}_evaluation",
                "brand_pair": None,
                "pair_id": None,
                "dimension": None,
                "brand": brand,
                "run": call["run"],
                "prompt": prompt,
                "response": response_text,
                "parsed": parsed,
                "weights": weights,
                "error": error,
                "latency_ms": latency_ms,
                "temperature": TEMPERATURE,
                "dimension_order": ordering_idx,
                "prompt_language": "en",
                "token_count_input": None,
                "token_count_output": None,
                # Experiment-specific fields
                "competitor": competitor,
                "competitor_type": call["competitor_type"],
                "condition": condition,
            }

            f.write(json.dumps(record) + "\n")
            f.flush()
            results.append(record)

            # Inter-call delay
            if i < len(calls) - 1:
                time.sleep(INTER_CALL_DELAY)

    print(f"\nDone. Success: {success_count}, Errors: {error_count}")
    print(f"Total calls: {len(calls)}")
    return {
        "total_calls": len(calls),
        "success": success_count,
        "errors": error_count,
        "output_path": str(output_path),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Experiment C: Competitive Interference in Perception Space"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--smoke", action="store_true", help="Quick smoke test")
    group.add_argument("--live", action="store_true", help="Full experiment")
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSONL path (default: L3_sessions/exp_competitive_interference.jsonl)",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).parent.parent
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = script_dir / "L3_sessions" / "exp_competitive_interference.jsonl"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    run_experiment(output_path, smoke=args.smoke)


if __name__ == "__main__":
    main()
