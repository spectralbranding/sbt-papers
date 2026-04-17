#!/usr/bin/env python3
"""Run 15b: Latin-Square Dimension-Order Robustness Test.

Tests whether PRISM-B results are invariant to the order in which
dimensions appear in the JSON response template. Uses a balanced
8x8 Latin square: each dimension appears exactly once in each
ordinal position across the 8 orderings.

Design: 8 orderings x 10 cohorts x 5 brands x 1 model = 400 calls.
Single model (GPT-4o-mini) to isolate position effects from model variance.
If position effects are absent, the ordering-averaged profiles should
correlate highly (rho > .90) with the canonical-order profiles from Run 15.

Usage:
    uv run python run15b_robustness_latin_square.py --smoke
    uv run python run15b_robustness_latin_square.py --live
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

# Standard 8x8 Latin square (cyclic construction).
# Row i: dimensions shifted by i positions. Each dimension appears exactly
# once in each column (ordinal position) across all 8 rows.
LATIN_SQUARE = []
for i in range(8):
    LATIN_SQUARE.append([DIMENSIONS[(j + i) % 8] for j in range(8)])

# Verify Latin-square property
for col in range(8):
    col_vals = [LATIN_SQUARE[row][col] for row in range(8)]
    assert len(set(col_vals)) == 8, f"Column {col} is not balanced"

BRANDS = ["Hermes", "IKEA", "Patagonia", "Erewhon", "Tesla"]

COHORTS = {
    "C1": {
        "name": "Green Advocate",
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


def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:16]


def verify_no_banned_words(text: str) -> bool:
    lower = text.lower()
    for word in BANNED_WORDS:
        if word in lower:
            return False
    return True


def build_system_prompt(vignette: str) -> str:
    return (
        "You are answering as the person described below. Adopt their "
        "perspective, priorities, and way of evaluating products and "
        "organizations.\n\n" + vignette
    )


def build_user_prompt(brand: str, dim_order: list[str]) -> str:
    dim_json = ", ".join(f'"{d}": <number>' for d in dim_order)
    return (
        f"Evaluate the brand {brand} by allocating importance weights "
        f"across eight dimensions of brand perception. The weights must "
        f"sum to 100.\n\n"
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
    return text, {
        "response_time_ms": elapsed_ms,
        "token_count_input": usage.prompt_tokens if usage else 0,
        "token_count_output": usage.completion_tokens if usage else 0,
        "api_cost_usd": round(
            (usage.prompt_tokens * 0.15 / 1_000_000 if usage else 0)
            + (usage.completion_tokens * 0.60 / 1_000_000 if usage else 0),
            6,
        ),
    }


def run_experiment(mode: str = "live", output_dir: Optional[Path] = None) -> list[dict]:
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "L3_sessions"
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "run15b_robustness_latin_square.jsonl"

    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set.")
        sys.exit(1)

    rng = random.Random(RANDOM_SEED)
    calls = []

    if mode == "smoke":
        # 8 calls: 1 cohort x 1 brand x 8 orderings
        for ordering_idx in range(8):
            calls.append(
                {
                    "cohort_id": "C1",
                    "brand": "Patagonia",
                    "ordering_idx": ordering_idx,
                    "dim_order": LATIN_SQUARE[ordering_idx],
                }
            )
    else:
        # Full: 10 cohorts x 5 brands x 8 orderings = 400 calls
        for cohort_id in COHORTS:
            for brand in BRANDS:
                for ordering_idx in range(8):
                    calls.append(
                        {
                            "cohort_id": cohort_id,
                            "brand": brand,
                            "ordering_idx": ordering_idx,
                            "dim_order": LATIN_SQUARE[ordering_idx],
                        }
                    )

    rng.shuffle(calls)
    print(f"Total calls: {len(calls)}")
    print(f"Output: {jsonl_path}")
    print(f"Latin square: 8 orderings, each dim in each position once\n")

    records = []
    errors = 0

    for i, call in enumerate(calls):
        cohort = COHORTS[call["cohort_id"]]
        system_prompt = build_system_prompt(cohort["vignette"])
        user_prompt = build_user_prompt(call["brand"], call["dim_order"])

        assert verify_no_banned_words(system_prompt)

        record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "experiment": "exp1b_robustness_latin_square",
            "model_id": "gpt-4o-mini",
            "model_provider": "openai",
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
            "condition": f"ordering_{call['ordering_idx']}",
            "ordering_idx": call["ordering_idx"],
            "dim_order": call["dim_order"],
            "repetition": 1,
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
            raw_text, meta = call_gpt(system_prompt, user_prompt)
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
            f"  [{i+1}/{len(calls)}] {call['cohort_id']} {call['brand']} "
            f"ord={call['ordering_idx']} -> {status} "
            f"({record['response_time_ms']}ms)"
        )
        time.sleep(0.3)

    valid = sum(1 for r in records if r["weights_valid"])
    total_cost = sum(r["api_cost_usd"] for r in records)
    print(f"\n--- Run 15b Complete ---")
    print(f"Total: {len(records)}, Valid: {valid} ({100*valid/len(records):.1f}%)")
    print(f"Errors: {errors}, Cost: ${total_cost:.4f}")
    return records


def main():
    parser = argparse.ArgumentParser(description="Run 15b: Latin-Square Robustness")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    if not args.smoke and not args.live:
        parser.print_help()
        sys.exit(1)
    mode = "smoke" if args.smoke else "live"
    print(f"Run 15b: Latin-Square Dimension-Order Robustness ({mode})")
    print(f"Temperature: {TEMPERATURE}, Seed: {RANDOM_SEED}\n")
    run_experiment(mode=mode)


if __name__ == "__main__":
    main()
