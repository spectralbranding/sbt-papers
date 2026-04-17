#!/usr/bin/env python3
"""Run 18: Dimensional Velocity Detection.

Tests whether LLMs detect brand trajectory direction (velocity) in
addition to brand position. No behavioral vignettes — trajectory
narratives are in the user prompt alongside PRISM-B evaluation.

Usage:
    uv run python run18_velocity_detection.py --smoke
    uv run python run18_velocity_detection.py --live
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


TEMPERATURE = 0.7
MAX_TOKENS = 512
RANDOM_SEED = 42

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

BRANDS = ["Hermes", "IKEA", "Patagonia", "Erewhon", "Tesla"]

TRAJECTORIES = {
    "rising": (
        "Over the past three years, this brand has invested heavily in "
        "supply chain transparency, launched a repair-and-reuse program, "
        "and publicly committed to reducing its environmental footprint "
        "by 50%. Customer reviews increasingly mention the brand's "
        "values alongside product quality."
    ),
    "falling": (
        "Over the past three years, this brand has cut manufacturing "
        "costs, outsourced customer service, and shifted marketing spend "
        "from experiential retail to performance advertising. Customer "
        "reviews increasingly mention declining quality and impersonal "
        "service."
    ),
    "stable_high": (
        "Over the past three years, this brand has maintained its market "
        "position with consistent product quality, steady marketing "
        "investment, and stable customer satisfaction scores."
    ),
    "oscillating": (
        "Over the past three years, this brand has alternated between "
        "bold sustainability commitments and cost-cutting reversals. In "
        "year one, it launched a high-profile environmental initiative. "
        "In year two, it quietly discontinued the program and raised "
        "prices. In year three, it relaunched with an even more "
        "ambitious sustainability pledge."
    ),
}

MODELS = {
    "claude": {
        "model_id": "claude-haiku-4-5",
        "provider": "anthropic",
        "api_key_env": "ANTHROPIC_API_KEY",
    },
    "gpt": {
        "model_id": "gpt-4o-mini",
        "provider": "openai",
        "api_key_env": "OPENAI_API_KEY",
    },
    "gemini": {
        "model_id": "gemini-2.5-flash",
        "provider": "google",
        "api_key_env": "GOOGLE_API_KEY",
    },
    "deepseek": {
        "model_id": "deepseek-chat",
        "provider": "deepseek",
        "api_key_env": "DEEPSEEK_API_KEY",
    },
    "grok": {
        "model_id": "grok-4-1-fast-non-reasoning",
        "provider": "xai",
        "api_key_env": "GROK_API_KEY",
    },
}


def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# API Callers (single user prompt, no system prompt for this experiment)
# ---------------------------------------------------------------------------


def call_claude(user_prompt: str) -> tuple[str, dict[str, Any]]:
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    t0 = time.time()
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        messages=[{"role": "user", "content": user_prompt}],
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    return message.content[0].text, {
        "response_time_ms": elapsed_ms,
        "token_count_input": message.usage.input_tokens,
        "token_count_output": message.usage.output_tokens,
        "api_cost_usd": round(
            message.usage.input_tokens * 0.80 / 1_000_000
            + message.usage.output_tokens * 4.00 / 1_000_000,
            6,
        ),
    }


def call_gpt(user_prompt: str) -> tuple[str, dict[str, Any]]:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    t0 = time.time()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    usage = response.usage
    return response.choices[0].message.content, {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
        "api_cost_usd": round(
            (usage.prompt_tokens * 0.15 / 1_000_000 if usage else 0)
            + (usage.completion_tokens * 0.60 / 1_000_000 if usage else 0),
            6,
        ),
    }


def call_gemini(user_prompt: str) -> tuple[str, dict[str, Any]]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    t0 = time.time()
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=8192,
                response_mime_type="application/json",
            ),
        )
        text = response.text
    except Exception:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=8192,
            ),
        )
        text = response.text if hasattr(response, "text") else ""
    elapsed_ms = int((time.time() - t0) * 1000)
    usage = getattr(response, "usage_metadata", None)
    inp = getattr(usage, "prompt_token_count", 0) if usage else 0
    out = getattr(usage, "candidates_token_count", 0) if usage else 0
    return text, {
        "response_time_ms": elapsed_ms,
        "token_count_input": inp,
        "token_count_output": out,
        "api_cost_usd": round(inp * 0.15 / 1_000_000 + out * 0.60 / 1_000_000, 6),
    }


def call_deepseek(user_prompt: str) -> tuple[str, dict[str, Any]]:
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    t0 = time.time()
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    usage = response.usage
    return response.choices[0].message.content, {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
        "api_cost_usd": round(
            (usage.prompt_tokens * 0.27 / 1_000_000 if usage else 0)
            + (usage.completion_tokens * 1.10 / 1_000_000 if usage else 0),
            6,
        ),
    }


def call_grok(user_prompt: str) -> tuple[str, dict[str, Any]]:
    """Call xAI Grok (social-media-corpus-trained model)."""
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["GROK_API_KEY"],
        base_url="https://api.x.ai/v1",
    )
    t0 = time.time()
    response = client.chat.completions.create(
        model="grok-4-1-fast-non-reasoning",
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    text = response.choices[0].message.content
    usage = response.usage
    return text, {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
        "api_cost_usd": round(
            (usage.prompt_tokens * 3.00 / 1_000_000 if usage else 0)
            + (usage.completion_tokens * 15.00 / 1_000_000 if usage else 0),
            6,
        ),
    }


CALLERS = {
    "claude": call_claude,
    "gpt": call_gpt,
    "gemini": call_gemini,
    "deepseek": call_deepseek,
    "grok": call_grok,
}


def build_user_prompt(brand: str, trajectory: str, trajectory_text: str) -> str:
    dim_json = ", ".join(f'"{d}": <number>' for d in DIMENSIONS)
    return (
        f"You are evaluating the brand {brand}.\n\n"
        f"Here is a brief history of the brand's recent trajectory:\n"
        f"{trajectory_text}\n\n"
        f"Given this trajectory, evaluate the brand's CURRENT perception "
        f"by allocating importance weights across eight dimensions. "
        f"The weights must sum to 100.\n\n"
        f"Respond in this exact JSON format:\n"
        f"{{\n  {dim_json}\n}}"
    )


def parse_weights(raw: str) -> Optional[dict[str, int]]:
    match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
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
            for k, v in data.items():
                if k.lower() == dim.lower():
                    val = v
                    break
        if val is None:
            return None
        try:
            weights[dim] = int(round(float(val)))
        except (ValueError, TypeError):
            return None
    return weights


def run_experiment(mode: str = "live", output_dir: Optional[Path] = None) -> list[dict]:
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "L3_sessions"
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "run18_velocity_detection.jsonl"

    available = {}
    for name, cfg in MODELS.items():
        env_key = cfg["api_key_env"]
        if os.environ.get(env_key):
            available[name] = cfg
        else:
            print(f"  Skipping {name}: {env_key} not set")

    print(f"Available models: {list(available.keys())}")

    rng = random.Random(RANDOM_SEED)
    calls = []
    model_names = list(available.keys())

    if mode == "smoke":
        for model_name in model_names[:3]:
            calls.append(
                {
                    "brand": "Patagonia",
                    "trajectory": "rising",
                    "model": model_name,
                    "rep": 1,
                }
            )
    else:
        for trajectory in TRAJECTORIES:
            for brand in BRANDS:
                for model_name in model_names:
                    for rep in range(1, 4):
                        calls.append(
                            {
                                "brand": brand,
                                "trajectory": trajectory,
                                "model": model_name,
                                "rep": rep,
                            }
                        )

    rng.shuffle(calls)
    print(f"\nTotal calls: {len(calls)}")
    print(f"Output: {jsonl_path}\n")

    records = []
    errors = 0

    for i, call in enumerate(calls):
        traj_text = TRAJECTORIES[call["trajectory"]]
        user_prompt = build_user_prompt(call["brand"], call["trajectory"], traj_text)

        model_name = call["model"]
        model_cfg = available[model_name]
        caller = CALLERS[model_name]

        record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "experiment": "exp3_velocity_detection",
            "model_id": model_cfg["model_id"],
            "model_provider": model_cfg["provider"],
            "temperature": TEMPERATURE,
            "top_p": 1.0,
            "max_tokens": MAX_TOKENS,
            "system_prompt": "",
            "system_prompt_hash": _sha256(""),
            "user_prompt": user_prompt,
            "user_prompt_hash": _sha256(user_prompt),
            "cohort_id": "none",
            "vignette": "",
            "brand": call["brand"],
            "condition": call["trajectory"],
            "repetition": call["rep"],
            "raw_response": "",
            "parsed_weights": None,
            "weights_valid": False,
            "weight_sum_raw": 0,
            "response_time_ms": 0,
            "token_count_input": 0,
            "token_count_output": 0,
            "api_cost_usd": 0.0,
        }

        try:
            raw_text, meta = caller(user_prompt)
            record["raw_response"] = raw_text
            record.update(meta)
            weights = parse_weights(raw_text)
            if weights:
                record["parsed_weights"] = weights
                weight_sum = sum(weights.values())
                record["weight_sum_raw"] = weight_sum
                record["weights_valid"] = abs(weight_sum - 100) <= 5
        except Exception as e:
            record["raw_response"] = f"ERROR: {type(e).__name__}: {e}"
            errors += 1

        records.append(record)
        with open(jsonl_path, "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        status = "OK" if record["weights_valid"] else "FAIL"
        print(
            f"  [{i+1}/{len(calls)}] {model_name} "
            f"{call['brand']} {call['trajectory']} rep={call['rep']} "
            f"-> {status} ({record['response_time_ms']}ms)"
        )

        time.sleep(0.5)

    valid = sum(1 for r in records if r["weights_valid"])
    total_cost = sum(r["api_cost_usd"] for r in records)
    print(f"\n--- Run 18 Complete ---")
    print(f"Total: {len(records)}, Valid: {valid} ({100*valid/len(records):.1f}%)")
    print(f"Errors: {errors}, Cost: ${total_cost:.4f}")
    return records


def main():
    parser = argparse.ArgumentParser(description="Run 18: Velocity Detection")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    if not args.smoke and not args.live:
        parser.print_help()
        sys.exit(1)
    mode = "smoke" if args.smoke else "live"
    print(f"Run 18: Dimensional Velocity Detection ({mode})")
    run_experiment(mode=mode)


if __name__ == "__main__":
    main()
