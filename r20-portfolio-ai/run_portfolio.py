#!/usr/bin/env python3
"""
R20 Portfolio-AI Experiment: Solo vs Portfolio Framing

Tests whether framing a brand as part of a corporate portfolio changes
LLM perception of that brand across 8 SBT dimensions.

Design:
  - 9 brands in 3 portfolios (LVMH, Unilever, P&G)
  - 2 conditions: SOLO (brand alone) vs PORTFOLIO (brand + parent + siblings)
  - 7 models: Claude, GPT-4o, Gemini, DeepSeek, Qwen3 local, Gemma4 local, Llama 3.3 (Groq)
  - 3 repetitions per cell
  - Total: 9 x 2 x 7 x 3 = 378 API calls

Usage:
    uv run python research/R20_portfolio_ai/run_portfolio.py [--model MODEL] [--dry-run]
    uv run python research/R20_portfolio_ai/run_portfolio.py --analyze

Requirements:
    uv add anthropic openai google-generativeai pyyaml
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
}

MODELS = [
    {
        "id": "claude",
        "name": "Claude Sonnet 4",
        "provider": "anthropic",
        "model_id": "claude-sonnet-4-20250514",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "gpt4o",
        "name": "GPT-4o",
        "provider": "openai",
        "model_id": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "gemini",
        "name": "Gemini 2.0 Flash",
        "provider": "google",
        "model_id": "gemini-2.0-flash",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "deepseek",
        "name": "DeepSeek V3",
        "provider": "deepseek",
        "model_id": "deepseek-chat",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "qwen3",
        "name": "Qwen3 30B",
        "provider": "ollama",
        "model_id": "qwen3:30b",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "gemma4",
        "name": "Gemma 4",
        "provider": "ollama",
        "model_id": "gemma4:latest",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "llama",
        "name": "Llama 3.3 70B",
        "provider": "groq",
        "model_id": "llama-3.3-70b-versatile",
        "temperature": 0.7,
        "max_tokens": 500,
    },
]

REPETITIONS = 3


# ---------------------------------------------------------------------------
# Prompt Templates
# ---------------------------------------------------------------------------

SOLO_TEMPLATE = """Rate the brand {brand} on each of the following 8 perceptual dimensions using a 0-10 scale (0 = not at all associated, 10 = extremely strongly associated).

Dimensions:
{dimensions}

Return ONLY a JSON object with your ratings, no other text. Example format:
{{"semiotic": 7, "narrative": 8, "ideological": 6, "experiential": 7, "social": 8, "economic": 5, "cultural": 7, "temporal": 6}}"""

PORTFOLIO_TEMPLATE = """Rate the brand {brand} on each of the following 8 perceptual dimensions using a 0-10 scale (0 = not at all associated, 10 = extremely strongly associated).

Context: {brand} is part of the {parent} {descriptor}, which also includes {siblings}.

Dimensions:
{dimensions}

Return ONLY a JSON object with your ratings, no other text. Example format:
{{"semiotic": 7, "narrative": 8, "ideological": 6, "experiential": 7, "social": 8, "economic": 5, "cultural": 7, "temporal": 6}}"""


def format_dimensions() -> str:
    lines = []
    for i, dim in enumerate(DIMENSIONS, 1):
        lines.append(f"{i}. {dim.capitalize()}: {DIMENSION_DESCRIPTIONS[dim]}")
    return "\n".join(lines)


def make_prompt(brand: str, condition: str, portfolio_key: str) -> str:
    dims_text = format_dimensions()
    if condition == "solo":
        return SOLO_TEMPLATE.format(brand=brand, dimensions=dims_text)

    portfolio = PORTFOLIOS[portfolio_key]
    siblings = [b["name"] for b in portfolio["brands"] if b["name"] != brand]
    return PORTFOLIO_TEMPLATE.format(
        brand=brand,
        parent=portfolio["parent"],
        descriptor=portfolio["descriptor"],
        siblings=", ".join(siblings),
        dimensions=dims_text,
    )


# ---------------------------------------------------------------------------
# API Providers
# ---------------------------------------------------------------------------


def call_anthropic(prompt: str, model_config: dict) -> str:
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def call_openai(prompt: str, model_config: dict) -> str:
    import openai

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def call_google(prompt: str, model_config: dict) -> str:
    import google.generativeai as genai

    model = genai.GenerativeModel(model_config["model_id"])
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
        ),
    )
    return response.text


def call_deepseek(prompt: str, model_config: dict) -> str:
    import openai

    client = openai.OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def call_ollama(prompt: str, model_config: dict) -> str:
    import urllib.request

    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    url = f"{host}/api/generate"
    # Qwen3 uses /think by default; disable thinking for clean JSON output
    actual_prompt = prompt
    if "qwen3" in model_config["model_id"].lower():
        actual_prompt = prompt + "\n\n/no_think"

    payload = json.dumps(
        {
            "model": model_config["model_id"],
            "prompt": actual_prompt,
            "stream": False,
            "options": {
                "temperature": model_config["temperature"],
                "num_predict": model_config["max_tokens"],
            },
        }
    ).encode()
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    return data["response"]


def call_groq(prompt: str, model_config: dict) -> str:
    import openai

    client = openai.OpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


PROVIDERS = {
    "anthropic": call_anthropic,
    "openai": call_openai,
    "google": call_google,
    "deepseek": call_deepseek,
    "ollama": call_ollama,
    "groq": call_groq,
}


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------


def parse_scores(response_text: str) -> dict | None:
    """Extract 8-dimension scores from LLM response."""
    # Try to find JSON object in the response
    # Strip markdown code fences if present
    text = response_text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

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


def get_all_cells():
    """Generate all experiment cells."""
    cells = []
    for portfolio_key, portfolio in PORTFOLIOS.items():
        for brand_info in portfolio["brands"]:
            for condition in ["solo", "portfolio"]:
                for model in MODELS:
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


def run_experiment(model_filter: str | None = None, dry_run: bool = False):
    output_dir = Path(__file__).parent / "responses"
    output_dir.mkdir(exist_ok=True)

    cells = get_all_cells()
    if model_filter:
        cells = [c for c in cells if c["model"]["id"] == model_filter]

    total = len(cells)
    completed = 0
    errors = 0
    skipped = 0

    print(f"R20 Portfolio-AI Experiment: {total} cells to process")
    print(f"Models: {', '.join(set(c['model']['id'] for c in cells))}")
    print()

    for cell in cells:
        output_file = output_dir / f"{cell['cell_id']}.json"

        if output_file.exists():
            skipped += 1
            continue

        prompt = make_prompt(cell["brand"], cell["condition"], cell["portfolio_key"])

        if dry_run:
            print(f"[DRY RUN] {cell['cell_id']}")
            print(f"  Prompt preview: {prompt[:100]}...")
            completed += 1
            continue

        provider_fn = PROVIDERS[cell["model"]["provider"]]

        try:
            response_text = provider_fn(prompt, cell["model"])
            scores = parse_scores(response_text)

            record = {
                "cell_id": cell["cell_id"],
                "portfolio": cell["portfolio_key"],
                "brand": cell["brand"],
                "category": cell["category"],
                "condition": cell["condition"],
                "model_id": cell["model"]["id"],
                "model_name": cell["model"]["name"],
                "repetition": cell["repetition"],
                "prompt": prompt,
                "response": response_text,
                "scores": scores,
                "parse_success": scores is not None,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            with open(output_file, "w") as f:
                json.dump(record, f, indent=2)

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
            elif provider == "groq":
                time.sleep(1.0)  # Groq has tighter limits
            else:
                time.sleep(0.5)

        except Exception as e:
            errors += 1
            n_done = completed + skipped + errors
            print(f"[{n_done}/{total}] {cell['cell_id']} ERROR: {e}")

    print(
        f"\nComplete: {completed} new, {skipped} skipped, {errors} errors, {total} total"
    )
    print(f"Output: {output_dir}/")

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
    args = parser.parse_args()

    if args.reparse:
        reparse_failures()
    else:
        run_experiment(model_filter=args.model, dry_run=args.dry_run)
