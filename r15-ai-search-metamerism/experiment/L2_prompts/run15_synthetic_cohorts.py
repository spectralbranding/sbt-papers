#!/usr/bin/env python3
"""Run 15: Synthetic Cohort Differentiation Experiment.

Tests whether PRISM-B differentiates synthetic observer cohorts defined by
behavioral vignettes. Two-stage prompt separation: vignette in system prompt,
PRISM-B evaluation in user prompt. No SBT dimension name appears in any
system prompt.

Usage:
    uv run python run15_synthetic_cohorts.py --smoke   # 5 calls, verify setup
    uv run python run15_synthetic_cohorts.py --live     # 800 calls, full run
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

# Banned words: no SBT dimension name or close synonym may appear in system prompts
BANNED_WORDS = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
    "dimension",
    "spectral",
    "prism",
    "brand perception",
    "perception cloud",
    "observer spectral",
]

CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

BRANDS = list(CANONICAL_PROFILES.keys())

# ---------------------------------------------------------------------------
# Cohort Vignettes
# ---------------------------------------------------------------------------

COHORTS = {
    "C1": {
        "name": "Green Advocate",
        "implied_dims": ["Ideological", "Narrative"],
        "vignette": (
            "Marina cycles to work year-round and volunteers at a food "
            "co-op on weekends. She switched her bank account last year "
            "after learning her previous bank financed pipeline "
            "construction. Before buying anything packaged, she checks "
            "for third-party certifications and reads the sourcing "
            "disclosure on the company website. She keeps a notebook "
            "where she tracks which brands have changed their "
            "supply-chain practices over time."
        ),
    },
    "C2": {
        "name": "Taste Curator",
        "implied_dims": ["Semiotic", "Social"],
        "vignette": (
            "Dario lives in a converted loft in the gallery district "
            "and frequents a members-only dining club on Thursday "
            "evenings. He rotates between three tailors for his shirts, "
            "prefers restaurants that seat fewer than thirty, and will "
            "not carry a bag or wear a watch that he has seen on more "
            "than two other people at the same event. His apartment "
            "contains no visible branding except on book spines."
        ),
    },
    "C3": {
        "name": "Spreadsheet Shopper",
        "implied_dims": ["Economic", "Experiential"],
        "vignette": (
            "Jun maintains a shared spreadsheet where she logs the "
            "per-unit cost and durability rating of every household "
            "product she buys. She waits for end-of-season clearance "
            "sales, reads teardown reviews on engineering forums, and "
            "bought her current phone refurbished after comparing "
            "benchmark scores across six models. She canceled a "
            "streaming subscription when the hourly entertainment cost "
            "exceeded her threshold."
        ),
    },
    "C4": {
        "name": "Feed Native",
        "implied_dims": ["Social", "Semiotic"],
        "vignette": (
            "Priya posts unboxing videos for her 8,000 followers and "
            "rates every purchase on at least two platforms. She "
            "screenshots outfits and room setups that catch her eye "
            "and saves them in folders organized by color palette. She "
            "adopted three micro-trends in the past month -- each "
            "lasting about two weeks -- and tracks which of her "
            "friends reposted her recommendations."
        ),
    },
    "C5": {
        "name": "Long Habit",
        "implied_dims": ["Temporal", "Cultural"],
        "vignette": (
            "Gerald has ordered the same coffee at the same cafe every "
            "morning for twenty-two years. He resoled his leather shoes "
            "twice rather than replacing them, keeps a handwritten "
            "ledger of household expenses, and spends two weeks each "
            "August at the same coastal cottage his parents rented. "
            "When an appliance breaks, his first call is to a repair "
            "shop, not a retailer."
        ),
    },
    "C6": {
        "name": "Collective Organizer",
        "implied_dims": ["Social", "Cultural"],
        "vignette": (
            "Amara hosts a large family dinner every Sunday and "
            "coordinates a monthly potluck for her apartment building. "
            "She lends kitchen equipment and tools to neighbors without "
            "hesitation, organized a group trip for twelve relatives "
            "last summer, and keeps a rotating calendar of birthdays, "
            "name days, and local festivals so that no occasion passes "
            "unacknowledged."
        ),
    },
    "C7": {
        "name": "Experience Collector",
        "implied_dims": ["Experiential", "Narrative"],
        "vignette": (
            "Tomasz books flights to cities he has never visited and "
            "picks accommodation by proximity to neighborhoods not "
            "listed in guidebooks. He fills a journal per trip, tries "
            "a different restaurant every evening, and has enrolled in "
            "courses ranging from glassblowing to emergency wilderness "
            "medicine. When friends ask for a recommendation, he gives "
            "a ten-minute account of how he discovered the place."
        ),
    },
    "C8": {
        "name": "Decade Planner",
        "implied_dims": ["Economic", "Temporal"],
        "vignette": (
            "Sonia selects appliances by calculating the ten-year cost "
            "of ownership, including energy consumption and replacement "
            "parts availability. She maintains a detailed "
            "home-maintenance log with scheduled service dates for "
            "every major fixture, chooses products from manufacturers "
            "that have been operating for at least forty years, and "
            "built a twelve-month emergency fund before putting a "
            "single dollar into equities."
        ),
    },
    "C9": {
        "name": "Deep Reader",
        "implied_dims": ["Narrative", "Ideological"],
        "vignette": (
            "Mikhail annotates the margins of every book he reads and "
            "subscribes to four long-form magazines. He writes letters "
            "to editors when an article misrepresents a source, "
            "attends public lectures at the university most Thursdays, "
            "and maintains a personal reference library organized by "
            "subject rather than author. He selects products from "
            "companies whose published reports he has actually read."
        ),
    },
    "C10": {
        "name": "Spec Evaluator",
        "implied_dims": ["Experiential", "Semiotic"],
        "vignette": (
            "Lena reads technical documentation before purchasing any "
            "device and benchmarks her electronics against manufacturer "
            "claims. She prefers products that publish full performance "
            "data and has disassembled two laptops and a coffee machine "
            "to understand their internal design. She dismissed a "
            "well-reviewed headphone after finding that its "
            "frequency-response curve did not match the advertised "
            "specification."
        ),
    },
}

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# API Callers (two-stage: system + user prompt)
# ---------------------------------------------------------------------------


def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:16]


def call_claude_two_stage(
    system_prompt: str, user_prompt: str
) -> tuple[str, dict[str, Any]]:
    """Call Anthropic Claude with separate system and user prompts."""
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    t0 = time.time()
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    text = message.content[0].text
    meta = {
        "response_time_ms": elapsed_ms,
        "token_count_input": message.usage.input_tokens,
        "token_count_output": message.usage.output_tokens,
        "api_cost_usd": round(
            message.usage.input_tokens * 0.80 / 1_000_000
            + message.usage.output_tokens * 4.00 / 1_000_000,
            6,
        ),
    }
    return text, meta


def call_gpt_two_stage(
    system_prompt: str, user_prompt: str
) -> tuple[str, dict[str, Any]]:
    """Call OpenAI GPT with separate system and user prompts."""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    t0 = time.time()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    text = response.choices[0].message.content
    usage = response.usage
    meta = {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
        "api_cost_usd": round(
            (usage.prompt_tokens * 0.15 / 1_000_000 if usage else 0)
            + (usage.completion_tokens * 0.60 / 1_000_000 if usage else 0),
            6,
        ),
    }
    return text, meta


def call_gemini_two_stage(
    system_prompt: str, user_prompt: str
) -> tuple[str, dict[str, Any]]:
    """Call Google Gemini with system instruction and user content."""
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
                system_instruction=system_prompt,
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
    meta = {
        "response_time_ms": elapsed_ms,
        "token_count_input": inp_tokens,
        "token_count_output": out_tokens,
        "api_cost_usd": round(
            inp_tokens * 0.15 / 1_000_000 + out_tokens * 0.60 / 1_000_000,
            6,
        ),
    }
    return text, meta


def call_deepseek_two_stage(
    system_prompt: str, user_prompt: str
) -> tuple[str, dict[str, Any]]:
    """Call DeepSeek with separate system and user prompts."""
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    t0 = time.time()
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    text = response.choices[0].message.content
    usage = response.usage
    meta = {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
        "api_cost_usd": round(
            (usage.prompt_tokens * 0.27 / 1_000_000 if usage else 0)
            + (usage.completion_tokens * 1.10 / 1_000_000 if usage else 0),
            6,
        ),
    }
    return text, meta


def call_grok_two_stage(
    system_prompt: str, user_prompt: str
) -> tuple[str, dict[str, Any]]:
    """Call xAI Grok with system and user prompts.

    Grok is trained on X/Twitter corpus — a social-media-first data
    distribution distinct from web-crawl-trained models. Tests whether
    training corpus type affects dimensional perception.
    """
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["GROK_API_KEY"],
        base_url="https://api.x.ai/v1",
    )
    t0 = time.time()
    response = client.chat.completions.create(
        model="grok-4-1-fast-non-reasoning",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    text = response.choices[0].message.content
    usage = response.usage
    meta = {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
        "api_cost_usd": round(
            (usage.prompt_tokens * 3.00 / 1_000_000 if usage else 0)
            + (usage.completion_tokens * 15.00 / 1_000_000 if usage else 0),
            6,
        ),
    }
    return text, meta


CALLERS = {
    "claude": call_claude_two_stage,
    "gpt": call_gpt_two_stage,
    "gemini": call_gemini_two_stage,
    "deepseek": call_deepseek_two_stage,
    "grok": call_grok_two_stage,
}


# ---------------------------------------------------------------------------
# Prompt Construction
# ---------------------------------------------------------------------------


def build_system_prompt(vignette: str) -> str:
    """Build system prompt with behavioral vignette. No SBT terms."""
    return (
        "You are answering as the person described below. Adopt their "
        "perspective, priorities, and way of evaluating products and "
        "organizations.\n\n" + vignette
    )


def build_user_prompt(brand: str, dim_order: Optional[list[str]] = None) -> str:
    """Build user prompt with PRISM-B evaluation task."""
    dims = dim_order if dim_order else DIMENSIONS
    dim_json = ", ".join(f'"{d}": <number>' for d in dims)
    return (
        f"Evaluate the brand {brand} by allocating importance weights "
        f"across eight dimensions of brand perception. The weights must "
        f"sum to 100.\n\n"
        f"Respond in this exact JSON format:\n"
        f"{{\n  {dim_json}\n}}"
    )


def verify_no_banned_words(text: str) -> bool:
    """Verify system prompt contains no banned SBT vocabulary."""
    lower = text.lower()
    for word in BANNED_WORDS:
        if word in lower:
            return False
    return True


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------


def parse_weights(raw: str) -> Optional[dict[str, int]]:
    """Extract dimension weights from model response JSON."""
    # Find JSON object in response
    match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError:
        return None

    weights = {}
    for dim in DIMENSIONS:
        # Try exact match, then case-insensitive
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


# ---------------------------------------------------------------------------
# Experiment Runner
# ---------------------------------------------------------------------------


def run_experiment(
    mode: str = "live",
    output_dir: Optional[Path] = None,
) -> list[dict]:
    """Execute the synthetic cohort experiment.

    Args:
        mode: 'smoke' (5 calls) or 'live' (800 calls)
        output_dir: directory for JSONL output
    """
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "L3_sessions"
    output_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = output_dir / "run15_synthetic_cohorts.jsonl"

    # Determine available models
    available_models = {}
    for name, cfg in MODELS.items():
        env_key = cfg["api_key_env"]
        if os.environ.get(env_key):
            available_models[name] = cfg
        else:
            print(f"  Skipping {name}: {env_key} not set")

    if not available_models:
        print("ERROR: No models available. Set API keys.")
        sys.exit(1)

    print(f"Available models: {list(available_models.keys())}")

    # Build call list
    rng = random.Random(RANDOM_SEED)
    calls = []

    cohort_ids = list(COHORTS.keys())
    model_names = list(available_models.keys())

    if mode == "smoke":
        # 5 calls: 1 cohort x 1 brand x all models x 1 rep
        for model_name in model_names[:5]:
            calls.append(
                {
                    "cohort_id": "C1",
                    "brand": "Patagonia",
                    "model": model_name,
                    "rep": 1,
                    "condition": "baseline",
                    "dim_order": None,
                }
            )
    else:
        # Main: 10 cohorts x 5 brands x N models x 3 reps
        for cohort_id in cohort_ids:
            for brand in BRANDS:
                for model_name in model_names:
                    for rep in range(1, 4):
                        calls.append(
                            {
                                "cohort_id": cohort_id,
                                "brand": brand,
                                "model": model_name,
                                "rep": rep,
                                "condition": "baseline",
                                "dim_order": None,
                            }
                        )

        # Robustness: 50 calls with scrambled dimension order
        # 5 cohorts x 5 brands x 2 models
        robustness_cohorts = ["C1", "C3", "C5", "C7", "C9"]
        robustness_models = model_names[:2]
        for cohort_id in robustness_cohorts:
            for brand in BRANDS:
                for model_name in robustness_models:
                    scrambled = list(DIMENSIONS)
                    rng.shuffle(scrambled)
                    calls.append(
                        {
                            "cohort_id": cohort_id,
                            "brand": brand,
                            "model": model_name,
                            "rep": 1,
                            "condition": "robustness_scrambled",
                            "dim_order": scrambled,
                        }
                    )

    # Shuffle call order to avoid systematic bias
    rng.shuffle(calls)

    print(f"\nTotal calls: {len(calls)}")
    print(f"Output: {jsonl_path}\n")

    records = []
    errors = 0

    for i, call in enumerate(calls):
        cohort = COHORTS[call["cohort_id"]]
        system_prompt = build_system_prompt(cohort["vignette"])
        user_prompt = build_user_prompt(call["brand"], call["dim_order"])

        # Verify no banned words in system prompt
        assert verify_no_banned_words(
            system_prompt
        ), f"BANNED WORD in system prompt for {call['cohort_id']}"

        model_name = call["model"]
        model_cfg = available_models[model_name]
        caller = CALLERS[model_name]

        record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "experiment": "exp1_cohort_differentiation",
            "model_id": model_cfg["model_id"],
            "model_provider": model_cfg["provider"],
            "temperature": TEMPERATURE,
            "top_p": 1.0,
            "max_tokens": MAX_TOKENS,
            "system_prompt": system_prompt,
            "system_prompt_hash": _sha256(system_prompt),
            "user_prompt": user_prompt,
            "user_prompt_hash": _sha256(user_prompt),
            "cohort_id": call["cohort_id"],
            "vignette": cohort["vignette"],
            "brand": call["brand"],
            "condition": call["condition"],
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
            raw_text, meta = caller(system_prompt, user_prompt)
            record["raw_response"] = raw_text
            record.update(meta)

            weights = parse_weights(raw_text)
            if weights:
                record["parsed_weights"] = weights
                weight_sum = sum(weights.values())
                record["weight_sum_raw"] = weight_sum
                record["weights_valid"] = abs(weight_sum - 100) <= 5
            else:
                record["parsed_weights"] = None
                record["weights_valid"] = False

        except Exception as e:
            record["raw_response"] = f"ERROR: {type(e).__name__}: {e}"
            record["weights_valid"] = False
            errors += 1

        records.append(record)

        # Write incrementally
        with open(jsonl_path, "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        # Progress
        status = "OK" if record["weights_valid"] else "FAIL"
        cost_str = f"${record['api_cost_usd']:.4f}"
        print(
            f"  [{i+1}/{len(calls)}] {model_name} "
            f"{call['cohort_id']} {call['brand']} "
            f"rep={call['rep']} {call['condition']} "
            f"-> {status} ({record['response_time_ms']}ms, "
            f"{cost_str})"
        )

        # Rate limiting (all cloud APIs)
        time.sleep(0.5)

    # Summary
    valid = sum(1 for r in records if r["weights_valid"])
    total_cost = sum(r["api_cost_usd"] for r in records)
    print(f"\n--- Run 15 Complete ---")
    print(f"Total calls: {len(records)}")
    print(f"Valid: {valid} ({100*valid/len(records):.1f}%)")
    print(f"Errors: {errors}")
    print(f"Total cost: ${total_cost:.4f}")
    print(f"Output: {jsonl_path}")

    return records


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Run 15: Synthetic Cohort Differentiation"
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Smoke test: 5 calls only",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Full run: 800 calls",
    )
    args = parser.parse_args()

    if not args.smoke and not args.live:
        parser.print_help()
        sys.exit(1)

    mode = "smoke" if args.smoke else "live"
    print(f"Run 15: Synthetic Cohort Differentiation ({mode})")
    print(f"Temperature: {TEMPERATURE}")
    print(f"Random seed: {RANDOM_SEED}")
    print()

    run_experiment(mode=mode)


if __name__ == "__main__":
    main()
