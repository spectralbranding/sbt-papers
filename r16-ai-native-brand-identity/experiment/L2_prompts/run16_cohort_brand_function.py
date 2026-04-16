#!/usr/bin/env python3
"""Run 16: Brand Function x Synthetic Cohort Interaction.

Tests whether Brand Function specification differentially affects
dimensional collapse across synthetic observer cohorts.

Usage:
    uv run python run16_cohort_brand_function.py --smoke
    uv run python run16_cohort_brand_function.py --live
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

# Brand Function enrichment: additional signals per collapsed dimension
BRAND_ENRICHMENT = {
    "Hermes": {
        "Experiential": [
            "Each leather goods piece undergoes 15+ hours of hand-stitching",
            "Customers experience private appointment-based shopping",
            "Products develop unique patina through extended personal use",
        ],
        "Ideological": [
            "Refuses to scale production beyond artisan capacity",
            "Maintains in-house tanning and leather treatment facilities",
            "Publicly opposes fast fashion and disposable luxury",
        ],
    },
    "IKEA": {
        "Experiential": [
            "Stores designed as full-home walk-through experiences",
            "In-store restaurant creates distinct sensory memory",
            "Assembly process creates personal investment in product",
        ],
        "Ideological": [
            "Democratic design principle: good design for everyone",
            "Published sustainability strategy targeting climate positive by 2030",
            "Circular product take-back and resale programs",
        ],
    },
    "Patagonia": {
        "Experiential": [
            "Worn Wear program lets customers trade and repair gear in-store",
            "Stores feature local environmental photography exhibitions",
            "Products tested by ambassador athletes in extreme conditions",
        ],
        "Economic": [
            "Ironclad lifetime guarantee reduces long-term cost of ownership",
            "Repair services extend product life by 2-5x vs competitors",
            "Used gear resale creates secondary market at 40-60% retail",
        ],
    },
    "Erewhon": {
        "Temporal": [
            "Founded 1966 as one of America's first natural food stores",
            "Named after Samuel Butler's 1872 utopian novel",
            "Pre-dates Whole Foods by 14 years",
        ],
        "Ideological": [
            "Sources from farms with documented regenerative practices",
            "Zero-waste deli program with compostable packaging",
            "Stocks only products meeting 200+ ingredient criteria",
        ],
    },
    "Tesla": {
        "Cultural": [
            "Named after Nikola Tesla, linking to inventor culture",
            "Open-sourced patents to accelerate industry shift",
            "Owner community forms distinct subculture with meetups and forums",
        ],
        "Temporal": [
            "Founded 2003, but positioned as heir to Edison-era innovation",
            "Over-the-air updates mean the car improves over ownership years",
            "Master Plan trilogy creates multi-decade narrative arc",
        ],
    },
}

# Subset of cohorts from Experiment 1 (maximally diverse)
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
    "deepseek": {
        "model_id": "deepseek-chat",
        "provider": "deepseek",
        "api_key_env": "DEEPSEEK_API_KEY",
    },
}


def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:16]


def verify_no_banned_words(text: str) -> bool:
    lower = text.lower()
    for word in BANNED_WORDS:
        if word in lower:
            return False
    return True


# ---------------------------------------------------------------------------
# API Callers
# ---------------------------------------------------------------------------


def call_claude(system_prompt: str, user_prompt: str) -> tuple[str, dict[str, Any]]:
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


def call_gpt(system_prompt: str, user_prompt: str) -> tuple[str, dict[str, Any]]:
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


def call_deepseek(system_prompt: str, user_prompt: str) -> tuple[str, dict[str, Any]]:
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


CALLERS = {
    "claude": call_claude,
    "gpt": call_gpt,
    "deepseek": call_deepseek,
}


# ---------------------------------------------------------------------------
# Prompt Construction
# ---------------------------------------------------------------------------


def build_system_prompt(vignette: str) -> str:
    return (
        "You are answering as the person described below. Adopt their "
        "perspective, priorities, and way of evaluating products and "
        "organizations.\n\n" + vignette
    )


def build_user_prompt_baseline(brand: str) -> str:
    dim_json = ", ".join(f'"{d}": <number>' for d in DIMENSIONS)
    return (
        f"Evaluate the brand {brand} by allocating importance weights "
        f"across eight dimensions of brand perception. The weights must "
        f"sum to 100.\n\n"
        f"Respond in this exact JSON format:\n"
        f"{{\n  {dim_json}\n}}"
    )


def build_brand_function_json(brand: str) -> dict:
    profile = CANONICAL_PROFILES[brand]
    return {d: profile[i] for i, d in enumerate(DIMENSIONS)}


def build_user_prompt_structural(brand: str) -> str:
    bf = build_brand_function_json(brand)
    bf_str = json.dumps(bf, indent=2)
    dim_json = ", ".join(f'"{d}": <number>' for d in DIMENSIONS)
    return (
        f"The brand {brand} has published the following Brand Function "
        f"specification:\n{bf_str}\n\n"
        f"Evaluate this brand by allocating importance weights "
        f"across eight dimensions of brand perception. The weights must "
        f"sum to 100.\n\n"
        f"Respond in this exact JSON format:\n"
        f"{{\n  {dim_json}\n}}"
    )


def build_user_prompt_enriched(brand: str) -> str:
    bf = build_brand_function_json(brand)
    bf_str = json.dumps(bf, indent=2)
    enrichment = BRAND_ENRICHMENT.get(brand, {})
    enrich_text = ""
    if enrichment:
        enrich_text = "\n\nAdditional brand signals:\n"
        for dim, signals in enrichment.items():
            enrich_text += f"\n{dim}:\n"
            for s in signals:
                enrich_text += f"- {s}\n"
    dim_json = ", ".join(f'"{d}": <number>' for d in DIMENSIONS)
    return (
        f"The brand {brand} has published the following Brand Function "
        f"specification:\n{bf_str}{enrich_text}\n\n"
        f"Evaluate this brand by allocating importance weights "
        f"across eight dimensions of brand perception. The weights must "
        f"sum to 100.\n\n"
        f"Respond in this exact JSON format:\n"
        f"{{\n  {dim_json}\n}}"
    )


PROMPT_BUILDERS = {
    "A_baseline": build_user_prompt_baseline,
    "B_structural": build_user_prompt_structural,
    "C_enriched": build_user_prompt_enriched,
}


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


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def run_experiment(mode: str = "live", output_dir: Optional[Path] = None) -> list[dict]:
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "L3_sessions"
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "run16_cohort_brand_function.jsonl"

    available = {}
    for name, cfg in MODELS.items():
        if os.environ.get(cfg["api_key_env"]):
            available[name] = cfg
        else:
            print(f"  Skipping {name}: {cfg['api_key_env']} not set")

    if not available:
        print("ERROR: No models available.")
        sys.exit(1)

    print(f"Available models: {list(available.keys())}")

    rng = random.Random(RANDOM_SEED)
    calls = []
    cohort_ids = list(COHORTS.keys())
    conditions = list(PROMPT_BUILDERS.keys())
    model_names = list(available.keys())

    if mode == "smoke":
        for model_name in model_names[:3]:
            calls.append(
                {
                    "cohort_id": "C1",
                    "brand": "Patagonia",
                    "model": model_name,
                    "rep": 1,
                    "condition": "A_baseline",
                }
            )
    else:
        for cohort_id in cohort_ids:
            for brand in BRANDS:
                for condition in conditions:
                    for model_name in model_names:
                        for rep in range(1, 4):
                            calls.append(
                                {
                                    "cohort_id": cohort_id,
                                    "brand": brand,
                                    "model": model_name,
                                    "rep": rep,
                                    "condition": condition,
                                }
                            )

    rng.shuffle(calls)
    print(f"\nTotal calls: {len(calls)}")
    print(f"Output: {jsonl_path}\n")

    records = []
    errors = 0

    for i, call in enumerate(calls):
        cohort = COHORTS[call["cohort_id"]]
        system_prompt = build_system_prompt(cohort["vignette"])
        user_prompt = PROMPT_BUILDERS[call["condition"]](call["brand"])

        assert verify_no_banned_words(
            system_prompt
        ), f"BANNED WORD in system prompt for {call['cohort_id']}"

        model_name = call["model"]
        model_cfg = available[model_name]
        caller = CALLERS[model_name]

        record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "experiment": "exp2_brand_function_cohort",
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
        except Exception as e:
            record["raw_response"] = f"ERROR: {type(e).__name__}: {e}"
            errors += 1

        records.append(record)
        with open(jsonl_path, "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        status = "OK" if record["weights_valid"] else "FAIL"
        print(
            f"  [{i+1}/{len(calls)}] {model_name} "
            f"{call['cohort_id']} {call['brand']} "
            f"{call['condition']} rep={call['rep']} "
            f"-> {status} ({record['response_time_ms']}ms)"
        )

        time.sleep(0.5)

    valid = sum(1 for r in records if r["weights_valid"])
    total_cost = sum(r["api_cost_usd"] for r in records)
    print(f"\n--- Run 16 Complete ---")
    print(f"Total: {len(records)}, Valid: {valid} ({100*valid/len(records):.1f}%)")
    print(f"Errors: {errors}, Cost: ${total_cost:.4f}")
    return records


def main():
    parser = argparse.ArgumentParser(description="Run 16: Brand Function x Cohort")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    if not args.smoke and not args.live:
        parser.print_help()
        sys.exit(1)
    mode = "smoke" if args.smoke else "live"
    print(f"Run 16: Brand Function x Cohort ({mode})")
    run_experiment(mode=mode)


if __name__ == "__main__":
    main()
