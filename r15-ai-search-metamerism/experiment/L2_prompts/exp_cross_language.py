#!/usr/bin/env python3
"""Experiment B: Cross-Language Semantic Drift in Brand Perception.

Tests whether SBT dimension labels carry the same meaning across languages
by comparing bilingual-anchored labels (control) vs native-only labels (test).

Two conditions per language:
  A (bilingual): "符号学 (Semiotic)": <number>
  B (native-only): "符号学": <number>

English has only condition A (bilingual = native for English).

Design: 8 langs x 5 brands x 3 models x 2 conditions x 2 reps = 450 calls.

Usage:
    uv run python exp_cross_language.py --smoke   # ~15 calls, verify setup
    uv run python exp_cross_language.py --live     # 450 calls, full run
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

CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

BRANDS = list(CANONICAL_PROFILES.keys())

# ---------------------------------------------------------------------------
# Dimension Label Translations
# ---------------------------------------------------------------------------

# Each language maps dimension English name -> native label
NATIVE_LABELS = {
    "en": {
        "Semiotic": "Semiotic",
        "Narrative": "Narrative",
        "Ideological": "Ideological",
        "Experiential": "Experiential",
        "Social": "Social",
        "Economic": "Economic",
        "Cultural": "Cultural",
        "Temporal": "Temporal",
    },
    "zh": {
        "Semiotic": "\u7b26\u53f7\u5b66",
        "Narrative": "\u53d9\u4e8b",
        "Ideological": "\u610f\u8bc6\u5f62\u6001",
        "Experiential": "\u4f53\u9a8c",
        "Social": "\u793e\u4f1a",
        "Economic": "\u7ecf\u6d4e",
        "Cultural": "\u6587\u5316",
        "Temporal": "\u65f6\u95f4",
    },
    "ru": {
        "Semiotic": "\u0421\u0435\u043c\u0438\u043e\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439",
        "Narrative": "\u041d\u0430\u0440\u0440\u0430\u0442\u0438\u0432\u043d\u044b\u0439",
        "Ideological": "\u0418\u0434\u0435\u043e\u043b\u043e\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0439",
        "Experiential": "\u042d\u043c\u043f\u0438\u0440\u0438\u0447\u0435\u0441\u043a\u0438\u0439",
        "Social": "\u0421\u043e\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439",
        "Economic": "\u042d\u043a\u043e\u043d\u043e\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0439",
        "Cultural": "\u041a\u0443\u043b\u044c\u0442\u0443\u0440\u043d\u044b\u0439",
        "Temporal": "\u0422\u0435\u043c\u043f\u043e\u0440\u0430\u043b\u044c\u043d\u044b\u0439",
    },
    "ja": {
        "Semiotic": "\u8a18\u53f7\u8ad6\u7684",
        "Narrative": "\u7269\u8a9e\u7684",
        "Ideological": "\u30a4\u30c7\u30aa\u30ed\u30ae\u30fc\u7684",
        "Experiential": "\u4f53\u9a13\u7684",
        "Social": "\u793e\u4f1a\u7684",
        "Economic": "\u7d4c\u6e08\u7684",
        "Cultural": "\u6587\u5316\u7684",
        "Temporal": "\u6642\u9593\u7684",
    },
    "ko": {
        "Semiotic": "\uae30\ud638\ud559\uc801",
        "Narrative": "\uc11c\uc0ac\uc801",
        "Ideological": "\uc774\ub150\uc801",
        "Experiential": "\uccb4\ud5d8\uc801",
        "Social": "\uc0ac\ud68c\uc801",
        "Economic": "\uacbd\uc81c\uc801",
        "Cultural": "\ubb38\ud654\uc801",
        "Temporal": "\uc2dc\uac04\uc801",
    },
    "ar": {
        "Semiotic": "\u0633\u064a\u0645\u064a\u0627\u0626\u064a",
        "Narrative": "\u0633\u0631\u062f\u064a",
        "Ideological": "\u0623\u064a\u062f\u064a\u0648\u0644\u0648\u062c\u064a",
        "Experiential": "\u062a\u062c\u0631\u064a\u0628\u064a",
        "Social": "\u0627\u062c\u062a\u0645\u0627\u0639\u064a",
        "Economic": "\u0627\u0642\u062a\u0635\u0627\u062f\u064a",
        "Cultural": "\u062b\u0642\u0627\u0641\u064a",
        "Temporal": "\u0632\u0645\u0646\u064a",
    },
    "hi": {
        "Semiotic": "\u091a\u093f\u0939\u094d\u0928\u0936\u093e\u0938\u094d\u0924\u094d\u0930\u0940\u092f",
        "Narrative": "\u0915\u0925\u093e\u0924\u094d\u092e\u0915",
        "Ideological": "\u0935\u0948\u091a\u093e\u0930\u093f\u0915",
        "Experiential": "\u0905\u0928\u0941\u092d\u0935\u093e\u0924\u094d\u092e\u0915",
        "Social": "\u0938\u093e\u092e\u093e\u091c\u093f\u0915",
        "Economic": "\u0906\u0930\u094d\u0925\u093f\u0915",
        "Cultural": "\u0938\u093e\u0902\u0938\u094d\u0915\u0943\u0924\u093f\u0915",
        "Temporal": "\u0915\u093e\u0932\u093f\u0915",
    },
    "es": {
        "Semiotic": "Semi\u00f3tico",
        "Narrative": "Narrativo",
        "Ideological": "Ideol\u00f3gico",
        "Experiential": "Experiencial",
        "Social": "Social",
        "Economic": "Econ\u00f3mico",
        "Cultural": "Cultural",
        "Temporal": "Temporal",
    },
}

LANGUAGES = list(NATIVE_LABELS.keys())

# Reverse lookup: for each language, map native label -> English dimension name
NATIVE_TO_ENGLISH = {}
for lang, mapping in NATIVE_LABELS.items():
    NATIVE_TO_ENGLISH[lang] = {v: k for k, v in mapping.items()}


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
}


# ---------------------------------------------------------------------------
# Latin-Square Balanced Orderings
# ---------------------------------------------------------------------------

def get_latin_square_order(index: int) -> list[str]:
    """Return a cyclic permutation of DIMENSIONS based on index % 8."""
    shift = index % 8
    return DIMENSIONS[shift:] + DIMENSIONS[:shift]


# ---------------------------------------------------------------------------
# Prompt Construction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = "You are evaluating brand perception."


def build_user_prompt(
    brand: str,
    language: str,
    condition: str,
    dim_order: list[str],
) -> str:
    """Build user prompt with dimension labels in the specified condition.

    Args:
        brand: Brand name to evaluate
        language: ISO 639-1 language code
        condition: 'bilingual' or 'native_only'
        dim_order: Latin-square ordered dimension list (English names)
    """
    native = NATIVE_LABELS[language]

    if condition == "bilingual":
        if language == "en":
            labels = [f'"{d}": <number>' for d in dim_order]
        else:
            labels = [
                f'"{native[d]} ({d})": <number>' for d in dim_order
            ]
    else:  # native_only
        labels = [f'"{native[d]}": <number>' for d in dim_order]

    json_body = ",\n  ".join(labels)

    return (
        f"Evaluate the brand {brand} by allocating importance weights "
        f"across eight dimensions. Weights must sum to 100.\n\n"
        f"Respond in JSON:\n"
        f"{{\n  {json_body}\n}}"
    )


# ---------------------------------------------------------------------------
# API Callers
# ---------------------------------------------------------------------------

def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:16]


def call_claude(
    system_prompt: str, user_prompt: str
) -> tuple[str, dict[str, Any]]:
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


def call_gpt(
    system_prompt: str, user_prompt: str
) -> tuple[str, dict[str, Any]]:
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


def call_gemini(
    system_prompt: str, user_prompt: str
) -> tuple[str, dict[str, Any]]:
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


CALLERS = {
    "claude": call_claude,
    "gpt": call_gpt,
    "gemini": call_gemini,
}


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------

def parse_weights(
    raw: str, language: str, condition: str, dim_order: list[str]
) -> Optional[dict[str, int]]:
    """Extract dimension weights from model response JSON.

    Handles both bilingual and native-only label formats. Returns weights
    keyed by English dimension names.
    """
    match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError:
        return None

    native = NATIVE_LABELS[language]
    reverse = NATIVE_TO_ENGLISH[language]

    weights = {}
    for dim in DIMENSIONS:
        val = None
        native_label = native[dim]

        # Try various key formats
        candidates = [
            dim,  # English
            native_label,  # Native only
            f"{native_label} ({dim})",  # Bilingual format
        ]

        for candidate in candidates:
            if candidate in data:
                val = data[candidate]
                break

        # Case-insensitive fallback
        if val is None:
            for k, v in data.items():
                k_clean = k.strip()
                if k_clean.lower() == dim.lower():
                    val = v
                    break
                if k_clean == native_label:
                    val = v
                    break
                # Check if key contains the native label
                if native_label in k_clean:
                    val = v
                    break
                # Check reverse lookup
                if k_clean in reverse:
                    mapped_dim = reverse[k_clean]
                    if mapped_dim == dim:
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
    """Execute the cross-language semantic drift experiment."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "L3_sessions"
    output_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = output_dir / "exp_cross_language.jsonl"

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
    call_idx = 0

    model_names = list(available_models.keys())

    if mode == "smoke":
        # Quick test: 1 language (zh) x 1 brand x all models x 2 conditions
        for model_name in model_names:
            for condition in ["bilingual", "native_only"]:
                order = get_latin_square_order(call_idx)
                calls.append({
                    "language": "zh",
                    "brand": "Patagonia",
                    "model": model_name,
                    "condition": condition,
                    "rep": 1,
                    "dim_order": order,
                })
                call_idx += 1
        # Also test English (1 condition only)
        order = get_latin_square_order(call_idx)
        calls.append({
            "language": "en",
            "brand": "Patagonia",
            "model": model_names[0],
            "condition": "bilingual",
            "rep": 1,
            "dim_order": order,
        })
        call_idx += 1
    else:
        # Full run: 450 calls
        for lang_idx, language in enumerate(LANGUAGES):
            conditions = (
                ["bilingual"]
                if language == "en"
                else ["bilingual", "native_only"]
            )
            for brand_idx, brand in enumerate(BRANDS):
                for model_name in model_names:
                    for condition in conditions:
                        for rep in range(1, 3):  # 2 reps
                            order = get_latin_square_order(call_idx)
                            calls.append({
                                "language": language,
                                "brand": brand,
                                "model": model_name,
                                "condition": condition,
                                "rep": rep,
                                "dim_order": order,
                            })
                            call_idx += 1

    # Shuffle to avoid systematic bias
    rng.shuffle(calls)

    print(f"\nTotal calls: {len(calls)}")
    print(f"Output: {jsonl_path}\n")

    records = []
    errors = 0
    total_cost = 0.0

    # Clear output file
    if jsonl_path.exists():
        jsonl_path.unlink()

    for i, call in enumerate(calls):
        user_prompt = build_user_prompt(
            call["brand"],
            call["language"],
            call["condition"],
            call["dim_order"],
        )

        model_name = call["model"]
        model_cfg = available_models[model_name]
        caller = CALLERS[model_name]

        # Build dimension labels for JSONL record
        native = NATIVE_LABELS[call["language"]]
        if call["condition"] == "bilingual" and call["language"] != "en":
            dim_labels = {
                d: f"{native[d]} ({d})" for d in DIMENSIONS
            }
        elif call["condition"] == "native_only":
            dim_labels = {d: native[d] for d in DIMENSIONS}
        else:
            dim_labels = {d: d for d in DIMENSIONS}

        record = {
            "timestamp": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat(),
            "experiment": "exp_b_cross_language_drift",
            "model_id": model_cfg["model_id"],
            "model_provider": model_cfg["provider"],
            "temperature": TEMPERATURE,
            "top_p": 1.0,
            "max_tokens": MAX_TOKENS,
            "system_prompt": SYSTEM_PROMPT,
            "system_prompt_hash": _sha256(SYSTEM_PROMPT),
            "user_prompt": user_prompt,
            "user_prompt_hash": _sha256(user_prompt),
            "brand": call["brand"],
            "condition": call["condition"],
            "repetition": call["rep"],
            "language": call["language"],
            "dimension_labels": dim_labels,
            "dimension_order": call["dim_order"],
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
            raw_text, meta = caller(SYSTEM_PROMPT, user_prompt)
            record["raw_response"] = raw_text
            record.update(meta)

            weights = parse_weights(
                raw_text, call["language"], call["condition"],
                call["dim_order"],
            )
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
        total_cost += record["api_cost_usd"]

        # Write incrementally
        with open(jsonl_path, "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        status = "OK" if record["weights_valid"] else "FAIL"
        cost_str = f"${record['api_cost_usd']:.4f}"
        print(
            f"  [{i+1}/{len(calls)}] {model_name} "
            f"{call['language']} {call['condition']} "
            f"{call['brand']} rep={call['rep']} "
            f"-> {status} ({record['response_time_ms']}ms, {cost_str})"
        )

        # Rate limiting: 3-second delay between calls
        time.sleep(3)

    # Summary
    valid = sum(1 for r in records if r["weights_valid"])
    print(f"\n--- Experiment B Complete ---")
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
        description="Experiment B: Cross-Language Semantic Drift"
    )
    parser.add_argument(
        "--smoke", action="store_true",
        help="Smoke test: ~7 calls only",
    )
    parser.add_argument(
        "--live", action="store_true",
        help="Full run: 450 calls",
    )
    args = parser.parse_args()

    if not args.smoke and not args.live:
        parser.print_help()
        sys.exit(1)

    mode = "smoke" if args.smoke else "live"
    print(f"Experiment B: Cross-Language Semantic Drift ({mode})")
    print(f"Temperature: {TEMPERATURE}")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Languages: {LANGUAGES}")
    print()

    run_experiment(mode=mode)


if __name__ == "__main__":
    main()
