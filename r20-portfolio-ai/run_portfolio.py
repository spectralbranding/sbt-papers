#!/usr/bin/env python3
"""
R20 Portfolio-AI Experiment: Solo vs Portfolio Framing

Tests whether framing a brand as part of a corporate portfolio changes
LLM perception of that brand across 8 SBT dimensions.

Design:
  - 9 brands in 3 portfolios (LVMH, Unilever, P&G)
  - 3 conditions: SOLO, PORTFOLIO (user msg), SYSTEM_PORTFOLIO (system msg)
  - 9 models from 6 training traditions
  - 5 repetitions per cell
  - Main experiment: 9 x 2 x 9 x 5 = 810 API calls
  - Ablation (system prompt): 9 x 1 x 4 x 5 = 180 API calls
  - Total: 990 API calls

Usage:
    uv run python research/R20_portfolio_ai/run_portfolio.py [--model MODEL] [--dry-run]
    uv run python research/R20_portfolio_ai/run_portfolio.py --ablation [--model MODEL]
    uv run python research/R20_portfolio_ai/run_portfolio.py --reparse
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Experiment Configuration
# ---------------------------------------------------------------------------

DIMENSIONS = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
]

DIMENSION_DESCRIPTIONS = {
    "semiotic": "visual and verbal identity (logos, packaging, design language)",
    "narrative": "brand storytelling (origin story, mythology, communication style)",
    "ideological": "values, beliefs, and purpose (what the brand stands for)",
    "experiential": "sensory and interaction experience (product feel, service quality)",
    "social": "community, status signaling (who uses this brand, what it says about them)",
    "economic": "pricing and value perception (affordability, luxury, value-for-money)",
    "cultural": "cultural codes and positioning (what culture or subculture it belongs to)",
    "temporal": "heritage and history (longevity, tradition, track record)",
}

PORTFOLIOS = {
    "LVMH": {
        "parent": "LVMH Moet Hennessy Louis Vuitton",
        "descriptor": "luxury conglomerate",
        "brands": [
            {"name": "Louis Vuitton", "category": "luxury fashion"},
            {"name": "Dior", "category": "luxury fashion and beauty"},
            {"name": "Fendi", "category": "luxury fashion"},
        ],
    },
    "Unilever": {
        "parent": "Unilever",
        "descriptor": "consumer goods conglomerate",
        "brands": [
            {"name": "Dove", "category": "personal care"},
            {"name": "Axe", "category": "personal care"},
            {"name": "Ben & Jerry's", "category": "ice cream"},
        ],
    },
    "P&G": {
        "parent": "Procter & Gamble",
        "descriptor": "consumer goods conglomerate",
        "brands": [
            {"name": "Tide", "category": "laundry detergent"},
            {"name": "Pampers", "category": "baby care"},
            {"name": "Gillette", "category": "grooming"},
        ],
    },
    "Toyota": {
        "parent": "Toyota Motor Corporation",
        "descriptor": "automotive conglomerate",
        "brands": [
            {"name": "Toyota", "category": "mass-market automotive"},
            {"name": "Lexus", "category": "luxury automotive"},
        ],
    },
}

MODELS = [
    # --- Anthropic, Chinese, Meta/Groq, Google local ---
    {
        "id": "claude",
        "name": "Claude Sonnet 4",
        "provider": "anthropic",
        "model_id": "claude-sonnet-4-20250514",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "deepseek",
        "name": "DeepSeek V3",
        "provider": "deepseek",
        "model_id": "deepseek-chat",
        "tradition": "Chinese",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "llama",
        "name": "Llama 3.3 70B",
        "provider": "groq",
        "model_id": "llama-3.3-70b-versatile",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "gemma4",
        "name": "Gemma 4",
        "provider": "ollama",
        "model_id": "gemma4:latest",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    # --- OpenAI, Google API, xAI ---
    {
        "id": "gpt4omini",
        "name": "GPT-4o-mini",
        "provider": "openai",
        "model_id": "gpt-4o-mini",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "gemini25flash",
        "name": "Gemini 2.5 Flash",
        "provider": "google",
        "model_id": "gemini-2.5-flash",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 2048,  # Gemini 2.5 uses thinking tokens
    },
    {
        "id": "grok",
        "name": "Grok-3-mini",
        "provider": "xai",
        "model_id": "grok-3-mini",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    # --- Cross-cultural additions ---
    {
        "id": "yandex",
        "name": "YandexGPT 5 Pro",
        "provider": "yandex",
        "model_id": "yandexgpt-5-pro/latest",
        "tradition": "Russian",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "sarvam",
        "name": "Sarvam M",
        "provider": "sarvam",
        "model_id": "sarvam-m",
        "tradition": "Indian",
        "temperature": 0.7,
        "max_tokens": 2048,  # Sarvam uses <think> blocks
    },
    {
        "id": "swallow",
        "name": "GPT-OSS-Swallow 20B",
        "provider": "yandex",
        "model_id": "gpt-oss-20b/latest",
        "tradition": "Japanese",
        "temperature": 0.7,
        "max_tokens": 500,
    },
]

# Models used in the system-prompt ablation (4 proven models)
ABLATION_MODEL_IDS = ["claude", "deepseek", "llama", "gemma4"]

REPETITIONS = 5


# ---------------------------------------------------------------------------
# Prompt Templates (1-5 PRISM-B scale)
# ---------------------------------------------------------------------------

SOLO_TEMPLATE = """You are evaluating the brand {brand} on eight dimensions of brand perception.
For each dimension, rate how strongly {brand} communicates through that channel
on a scale of 1 to 5, where 1 = Not at all, 2 = Slightly, 3 = Moderately,
4 = Strongly, 5 = Very strongly.

Dimensions:
{dimensions}

Respond in JSON format with the following keys:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Evaluate based on your knowledge of the brand. Provide only the JSON."""

PORTFOLIO_TEMPLATE = """You are evaluating the brand {brand} on eight dimensions of brand perception.

Context: {brand} is owned by {parent} ({descriptor}), which also owns {siblings}.

For each dimension, rate how strongly {brand} communicates through that channel
on a scale of 1 to 5, where 1 = Not at all, 2 = Slightly, 3 = Moderately,
4 = Strongly, 5 = Very strongly.

Dimensions:
{dimensions}

Respond in JSON format with the following keys:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Evaluate based on your knowledge of the brand. Provide only the JSON."""

SYSTEM_PORTFOLIO_TEMPLATE = """You have access to the following corporate context: {brand} is owned by {parent} ({descriptor}), which also owns {siblings}. Use this context when evaluating brands. Always rate all eight dimensions: semiotic, narrative, ideological, experiential, social, economic, cultural, temporal."""

# Recommendation category mapping for naturalistic prompts
RECOMMENDATION_CATEGORIES = {
    "Louis Vuitton": "luxury fashion brand",
    "Dior": "luxury fashion brand",
    "Fendi": "luxury fashion brand",
    "Dove": "personal care brand",
    "Axe": "personal care brand",
    "Ben & Jerry's": "ice cream brand",
    "Tide": "laundry detergent",
    "Pampers": "baby care brand",
    "Gillette": "grooming brand",
    "Toyota": "car brand",
    "Lexus": "luxury car brand",
}

RECOMMENDATION_SOLO_TEMPLATE = """A friend asks you: "What do you think of {brand} as a {category}?"

Based on your overall impression of {brand}, rate it on each of the following
8 perception dimensions on a scale of 1 to 5 (1 = Not at all, 5 = Very strongly).

Dimensions:
{dimensions}

Respond in JSON format:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Provide only the JSON."""

RECOMMENDATION_PORTFOLIO_TEMPLATE = """A friend asks you: "What do you think of {brand}? I know it's part of {parent}."

Based on your overall impression of {brand} — keeping in mind it belongs to
{parent} ({descriptor}), alongside {siblings} — rate it on each of the following
8 perception dimensions on a scale of 1 to 5 (1 = Not at all, 5 = Very strongly).

Dimensions:
{dimensions}

Respond in JSON format:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Provide only the JSON."""

MULTITURN_TURN1_TEMPLATE = """You are evaluating the brand {brand} on eight dimensions of brand perception.
For each dimension, rate how strongly {brand} communicates through that channel
on a scale of 1 to 5, where 1 = Not at all, 2 = Slightly, 3 = Moderately,
4 = Strongly, 5 = Very strongly.

Dimensions:
{dimensions}

Respond in JSON format with the following keys:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Evaluate based on your knowledge of the brand. Provide only the JSON."""

MULTITURN_TURN2_REVEAL = """Interesting. Did you know that {brand} is actually owned by {parent} ({descriptor}), which also owns {siblings}? Does this change how you see the brand? Please re-rate {brand} on the same 8 dimensions, using the same 1-5 scale.

Respond in JSON format:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Provide only the JSON."""


def format_dimensions() -> str:
    lines = []
    for i, dim in enumerate(DIMENSIONS, 1):
        lines.append(f"{i}. {dim.capitalize()}: {DIMENSION_DESCRIPTIONS[dim]}")
    return "\n".join(lines)


def make_prompt(
    brand: str, condition: str, portfolio_key: str
) -> tuple[str, str | None]:
    """Return (user_prompt, system_prompt_or_None)."""
    dims_text = format_dimensions()

    if condition == "solo":
        return SOLO_TEMPLATE.format(brand=brand, dimensions=dims_text), None

    portfolio = PORTFOLIOS[portfolio_key]
    siblings = [b["name"] for b in portfolio["brands"] if b["name"] != brand]

    if condition == "portfolio":
        return (
            PORTFOLIO_TEMPLATE.format(
                brand=brand,
                parent=portfolio["parent"],
                descriptor=portfolio["descriptor"],
                siblings=", ".join(siblings),
                dimensions=dims_text,
            ),
            None,
        )

    if condition == "system_portfolio":
        system_msg = SYSTEM_PORTFOLIO_TEMPLATE.format(
            brand=brand,
            parent=portfolio["parent"],
            descriptor=portfolio["descriptor"],
            siblings=", ".join(siblings),
        )
        user_msg = SOLO_TEMPLATE.format(brand=brand, dimensions=dims_text)
        return user_msg, system_msg

    if condition == "recommendation_solo":
        category = RECOMMENDATION_CATEGORIES.get(brand, "brand")
        return (
            RECOMMENDATION_SOLO_TEMPLATE.format(
                brand=brand, category=category, dimensions=dims_text
            ),
            None,
        )

    if condition == "recommendation_portfolio":
        return (
            RECOMMENDATION_PORTFOLIO_TEMPLATE.format(
                brand=brand,
                parent=portfolio["parent"],
                descriptor=portfolio["descriptor"],
                siblings=", ".join(siblings),
                dimensions=dims_text,
            ),
            None,
        )

    # Multi-turn conditions are handled separately in run_multiturn()
    raise ValueError(f"Unknown condition: {condition}")


# ---------------------------------------------------------------------------
# API Providers
# ---------------------------------------------------------------------------


def call_anthropic(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import anthropic

    kwargs = {
        "model": model_config["model_id"],
        "max_tokens": model_config["max_tokens"],
        "temperature": model_config["temperature"],
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt
    client = anthropic.Anthropic()
    response = client.messages.create(**kwargs)
    return response.content[0].text


def call_openai(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import openai

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=messages,
    )
    return response.choices[0].message.content


def call_google(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import google.generativeai as genai

    kwargs = {}
    if system_prompt:
        kwargs["system_instruction"] = system_prompt
    model = genai.GenerativeModel(model_config["model_id"], **kwargs)
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
        ),
    )
    return response.text


def call_deepseek(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import openai

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    client = openai.OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=messages,
    )
    return response.choices[0].message.content


def call_ollama(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import urllib.request

    host = os.environ.get("OLLAMA_HOST", "localhost:11434")
    if not host.startswith("http"):
        host = f"http://{host}"
    url = f"{host}/api/chat"

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload_dict = {
        "model": model_config["model_id"],
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": model_config["temperature"],
            "num_predict": 8192,
        },
    }

    payload = json.dumps(payload_dict).encode()
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
    return data["message"]["content"]


def call_groq(prompt: str, model_config: dict, system_prompt: str | None = None) -> str:
    import openai

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    client = openai.OpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=messages,
    )
    return response.choices[0].message.content


def call_xai(prompt: str, model_config: dict, system_prompt: str | None = None) -> str:
    import openai

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    client = openai.OpenAI(
        api_key=os.environ["GROK_API_KEY"],
        base_url="https://api.x.ai/v1",
    )
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=messages,
    )
    return response.choices[0].message.content


def call_yandex(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import openai

    api_key = os.environ["YANDEX_AI_API_KEY"]
    folder_id = os.environ.get("YANDEX_FOLDER_ID", "b1g894jalgr7i0op2s70")

    client = openai.OpenAI(
        api_key=api_key,
        project=folder_id,
        base_url="https://llm.api.cloud.yandex.net/v1",
    )
    model_uri = f"gpt://{folder_id}/{model_config['model_id']}"

    messages = []
    sys_content = (
        "You are a brand analysis assistant. You MUST respond with ONLY a "
        "valid JSON object. No markdown, no explanation. Start with { and end with }."
    )
    if system_prompt:
        sys_content = system_prompt + "\n\n" + sys_content
    messages.append({"role": "system", "content": sys_content})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model_uri,
        messages=messages,
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
    )
    content = response.choices[0].message.content or ""
    content = re.sub(r"```(?:json)?\s*", "", content).strip()
    content = re.sub(r"```\s*$", "", content).strip()
    return content


def call_sarvam(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import urllib.request

    key = os.environ["SARVAM_API_KEY"]
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps(
        {
            "model": model_config["model_id"],
            "messages": messages,
            "max_tokens": model_config["max_tokens"],
            "temperature": model_config["temperature"],
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.sarvam.ai/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "api-subscription-key": key,
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


PROVIDERS = {
    "anthropic": call_anthropic,
    "openai": call_openai,
    "google": call_google,
    "deepseek": call_deepseek,
    "ollama": call_ollama,
    "groq": call_groq,
    "xai": call_xai,
    "yandex": call_yandex,
    "sarvam": call_sarvam,
}


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------


def parse_scores(response_text: str) -> dict | None:
    """Extract 8-dimension scores from LLM response."""
    text = response_text.strip()
    # Strip <think>...</think> reasoning blocks (Sarvam, Qwen, etc.)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```", "", text)

    # Try direct JSON parse
    try:
        data = json.loads(text)
        if isinstance(data, dict) and all(d in data for d in DIMENSIONS):
            return {d: float(data[d]) for d in DIMENSIONS}
    except (json.JSONDecodeError, ValueError, KeyError):
        pass

    # Try to extract JSON from within text
    match = re.search(r"\{[^{}]*\}", text)
    if match:
        try:
            data = json.loads(match.group())
            if isinstance(data, dict) and all(d in data for d in DIMENSIONS):
                return {d: float(data[d]) for d in DIMENSIONS}
        except (json.JSONDecodeError, ValueError, KeyError):
            pass

    return None


# ---------------------------------------------------------------------------
# Experiment Runner
# ---------------------------------------------------------------------------


def get_all_cells(
    ablation: bool = False, conditions: list[str] | None = None
):
    """Generate all experiment cells."""
    cells = []
    if conditions:
        models = MODELS
    elif ablation:
        models = [m for m in MODELS if m["id"] in ABLATION_MODEL_IDS]
        conditions = ["system_portfolio"]
    else:
        models = MODELS
        conditions = ["solo", "portfolio"]

    for portfolio_key, portfolio in PORTFOLIOS.items():
        for brand_info in portfolio["brands"]:
            for condition in conditions:
                for model in models:
                    for rep in range(1, REPETITIONS + 1):
                        cell_id = (
                            f"{portfolio_key}_{brand_info['name'].replace(' ', '_').replace('&', 'and')}"
                            f"_{condition}_{model['id']}_rep{rep}"
                        )
                        cells.append(
                            {
                                "cell_id": cell_id,
                                "portfolio_key": portfolio_key,
                                "brand": brand_info["name"],
                                "category": brand_info["category"],
                                "condition": condition,
                                "model": model,
                                "repetition": rep,
                            }
                        )
    return cells


def run_experiment(
    model_filter: str | None = None,
    dry_run: bool = False,
    ablation: bool = False,
    conditions: list[str] | None = None,
):
    output_dir = Path(__file__).parent / "responses"
    output_dir.mkdir(exist_ok=True)

    cells = get_all_cells(ablation=ablation, conditions=conditions)
    if model_filter:
        cells = [c for c in cells if c["model"]["id"] == model_filter]

    total = len(cells)
    completed = 0
    errors = 0
    skipped = 0

    mode = "ABLATION (system prompt)" if ablation else "MAIN"
    print(f"R20 Portfolio-AI Experiment [{mode}]: {total} cells to process")
    print(f"Models: {', '.join(sorted(set(c['model']['id'] for c in cells)))}")
    print(f"Scale: 1-5 PRISM-B")
    print()

    # Track per-model failure rates for >20% abort
    model_stats: dict[str, dict[str, int]] = {}

    for cell in cells:
        output_file = output_dir / f"{cell['cell_id']}.json"

        if output_file.exists():
            skipped += 1
            continue

        user_prompt, system_prompt = make_prompt(
            cell["brand"], cell["condition"], cell["portfolio_key"]
        )

        if dry_run:
            print(f"[DRY RUN] {cell['cell_id']}")
            completed += 1
            continue

        provider_fn = PROVIDERS[cell["model"]["provider"]]
        mid = cell["model"]["id"]
        if mid not in model_stats:
            model_stats[mid] = {"ok": 0, "fail": 0}

        try:
            response_text = provider_fn(user_prompt, cell["model"], system_prompt)
            scores = parse_scores(response_text)

            record = {
                "cell_id": cell["cell_id"],
                "portfolio": cell["portfolio_key"],
                "brand": cell["brand"],
                "category": cell["category"],
                "condition": cell["condition"],
                "model_id": mid,
                "model_name": cell["model"]["name"],
                "provider": cell["model"]["provider"],
                "tradition": cell["model"]["tradition"],
                "temperature": cell["model"]["temperature"],
                "repetition": cell["repetition"],
                "prompt": user_prompt,
                "system_prompt": system_prompt,
                "response": response_text,
                "scores": scores,
                "parse_success": scores is not None,
                "scale": "1-5",
                "version": "1.0",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            with open(output_file, "w") as f:
                json.dump(record, f, indent=2)

            if scores:
                model_stats[mid]["ok"] += 1
            else:
                model_stats[mid]["fail"] += 1

            completed += 1
            status = "OK" if scores else "PARSE_FAIL"
            n_done = completed + skipped + errors
            print(
                f"[{n_done}/{total}] {cell['cell_id']} {status}"
                + (f" scores={list(scores.values())}" if scores else "")
            )

            # Rate limiting
            provider = cell["model"]["provider"]
            if provider == "ollama":
                time.sleep(0.1)
            elif provider in ("groq", "xai"):
                time.sleep(1.0)
            elif provider == "yandex":
                time.sleep(1.5)  # Conservative for Yandex
            elif provider == "sarvam":
                time.sleep(1.0)
            else:
                time.sleep(0.5)

        except Exception as e:
            errors += 1
            model_stats[mid]["fail"] += 1
            n_done = completed + skipped + errors
            print(f"[{n_done}/{total}] {cell['cell_id']} ERROR: {e}")

        # Check >20% failure rate per model (after at least 10 attempts)
        ms = model_stats[mid]
        total_attempts = ms["ok"] + ms["fail"]
        if total_attempts >= 10 and ms["fail"] / total_attempts > 0.20:
            fail_pct = ms["fail"] / total_attempts * 100
            print(
                f"\n*** WARNING: {mid} has {fail_pct:.0f}% failure rate "
                f"({ms['fail']}/{total_attempts}). Consider substituting. ***\n"
            )

    print(
        f"\nComplete: {completed} new, {skipped} skipped, {errors} errors, {total} total"
    )
    print(f"Output: {output_dir}/")

    # Print per-model stats
    print("\nPer-model statistics:")
    for mid, ms in sorted(model_stats.items()):
        total_m = ms["ok"] + ms["fail"]
        pct = ms["ok"] / total_m * 100 if total_m > 0 else 0
        print(f"  {mid:20s}  {ms['ok']}/{total_m} OK ({pct:.0f}%)")

    # Print parse failure summary
    parse_failures = []
    for f in output_dir.glob("*.json"):
        with open(f) as fh:
            rec = json.load(fh)
            if not rec.get("parse_success"):
                parse_failures.append(rec["cell_id"])
    if parse_failures:
        print(f"\nParse failures ({len(parse_failures)}):")
        for pf in parse_failures:
            print(f"  {pf}")


# ---------------------------------------------------------------------------
# Re-parse failed responses
# ---------------------------------------------------------------------------


def reparse_failures():
    """Attempt to re-parse responses that failed initial parsing."""
    responses_dir = Path(__file__).parent / "responses"
    fixed = 0
    for f in sorted(responses_dir.glob("*.json")):
        with open(f) as fh:
            rec = json.load(fh)
        if rec.get("parse_success"):
            continue
        scores = parse_scores(rec["response"])
        if scores:
            rec["scores"] = scores
            rec["parse_success"] = True
            with open(f, "w") as fh:
                json.dump(rec, fh, indent=2)
            fixed += 1
            print(f"Fixed: {rec['cell_id']}")
    print(f"\nRe-parsed {fixed} responses")


# ---------------------------------------------------------------------------
# Multi-turn Runner
# ---------------------------------------------------------------------------


def run_multiturn(model_filter: str | None = None, dry_run: bool = False):
    """Run multi-turn experiment: Turn 1 = solo, Turn 2 = reveal portfolio + re-rate."""
    output_dir = Path(__file__).parent / "responses"
    output_dir.mkdir(exist_ok=True)

    dims_text = format_dimensions()
    cells = []
    for portfolio_key, portfolio in PORTFOLIOS.items():
        for brand_info in portfolio["brands"]:
            for model in MODELS:
                for rep in range(1, REPETITIONS + 1):
                    cell_id = (
                        f"{portfolio_key}_{brand_info['name'].replace(' ', '_').replace('&', 'and')}"
                        f"_multiturn_{model['id']}_rep{rep}"
                    )
                    cells.append(
                        {
                            "cell_id": cell_id,
                            "portfolio_key": portfolio_key,
                            "brand": brand_info["name"],
                            "category": brand_info["category"],
                            "model": model,
                            "repetition": rep,
                        }
                    )

    if model_filter:
        cells = [c for c in cells if c["model"]["id"] == model_filter]

    total = len(cells)
    completed = 0
    errors = 0
    skipped = 0

    print(f"R20 Multi-Turn Experiment: {total} cells to process")
    print(f"Models: {', '.join(sorted(set(c['model']['id'] for c in cells)))}")
    print()

    for cell in cells:
        output_file = output_dir / f"{cell['cell_id']}.json"
        if output_file.exists():
            skipped += 1
            continue

        if dry_run:
            print(f"[DRY RUN] {cell['cell_id']}")
            completed += 1
            continue

        brand = cell["brand"]
        portfolio = PORTFOLIOS[cell["portfolio_key"]]
        siblings = [b["name"] for b in portfolio["brands"] if b["name"] != brand]
        provider_fn = PROVIDERS[cell["model"]["provider"]]
        mid = cell["model"]["id"]

        try:
            # Turn 1: Solo rating
            turn1_prompt = MULTITURN_TURN1_TEMPLATE.format(
                brand=brand, dimensions=dims_text
            )
            turn1_response = provider_fn(turn1_prompt, cell["model"])
            turn1_scores = parse_scores(turn1_response)

            # Turn 2: Reveal portfolio and re-rate (multi-turn = send both messages)
            turn2_prompt = MULTITURN_TURN2_REVEAL.format(
                brand=brand,
                parent=portfolio["parent"],
                descriptor=portfolio["descriptor"],
                siblings=", ".join(siblings),
            )

            # For providers that support multi-turn via messages, we simulate it
            # by concatenating context. Most providers only take a single prompt.
            combined_prompt = (
                f"Previous evaluation of {brand}:\n{turn1_response}\n\n"
                f"{turn2_prompt}"
            )
            turn2_response = provider_fn(combined_prompt, cell["model"])
            turn2_scores = parse_scores(turn2_response)

            record = {
                "cell_id": cell["cell_id"],
                "portfolio": cell["portfolio_key"],
                "brand": brand,
                "category": cell["category"],
                "condition": "multiturn",
                "model_id": mid,
                "model_name": cell["model"]["name"],
                "provider": cell["model"]["provider"],
                "tradition": cell["model"]["tradition"],
                "temperature": cell["model"]["temperature"],
                "repetition": cell["repetition"],
                "turn1_prompt": turn1_prompt,
                "turn1_response": turn1_response,
                "turn1_scores": turn1_scores,
                "turn2_prompt": turn2_prompt,
                "turn2_response": turn2_response,
                "scores": turn2_scores,  # Final scores after reveal
                "parse_success": turn1_scores is not None and turn2_scores is not None,
                "scale": "1-5",
                "version": "1.0",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            with open(output_file, "w") as f:
                json.dump(record, f, indent=2)

            completed += 1
            status = "OK" if record["parse_success"] else "PARSE_FAIL"
            n_done = completed + skipped + errors
            print(f"[{n_done}/{total}] {cell['cell_id']} {status}")

            provider = cell["model"]["provider"]
            if provider == "ollama":
                time.sleep(0.1)
            elif provider in ("groq", "xai"):
                time.sleep(1.0)
            elif provider == "yandex":
                time.sleep(1.5)
            elif provider == "sarvam":
                time.sleep(1.0)
            else:
                time.sleep(0.5)

        except Exception as e:
            errors += 1
            n_done = completed + skipped + errors
            print(f"[{n_done}/{total}] {cell['cell_id']} ERROR: {e}")

    print(
        f"\nComplete: {completed} new, {skipped} skipped, {errors} errors, {total} total"
    )


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="R20 Portfolio-AI Experiment")
    parser.add_argument(
        "--model",
        choices=[m["id"] for m in MODELS],
        help="Run single model only",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print prompts without calling APIs",
    )
    parser.add_argument(
        "--reparse",
        action="store_true",
        help="Re-parse failed responses",
    )
    parser.add_argument(
        "--ablation",
        action="store_true",
        help="Run system-prompt ablation (4 proven models only)",
    )
    parser.add_argument(
        "--recommendation",
        action="store_true",
        help="Run recommendation prompt conditions (solo + portfolio)",
    )
    parser.add_argument(
        "--multiturn",
        action="store_true",
        help="Run multi-turn experiment (Turn 1 solo, Turn 2 reveal + re-rate)",
    )
    args = parser.parse_args()

    if args.reparse:
        reparse_failures()
    elif args.multiturn:
        run_multiturn(model_filter=args.model, dry_run=args.dry_run)
    elif args.recommendation:
        # Recommendation uses the same runner with different conditions
        run_experiment(
            model_filter=args.model,
            dry_run=args.dry_run,
            ablation=False,
            conditions=["recommendation_solo", "recommendation_portfolio"],
        )
    else:
        run_experiment(
            model_filter=args.model, dry_run=args.dry_run, ablation=args.ablation
        )
