#!/usr/bin/env python3
"""Experiment D: Brand Function Format Optimization.

Tests which representational format of brand function specifications
maximizes AI comprehension fidelity across 5 LLMs.

Design: 5 formats x 5 brands x 5 models x 3 reps = 375 calls.
Output: L3_sessions/exp_bf_format.jsonl

Usage:
    uv run python exp_bf_format.py --dry-run   # preview trial count
    uv run python exp_bf_format.py              # execute experiment
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
from typing import Optional

import numpy as np

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RANDOM_SEED = 20260416
TEMPERATURE = 0.7
MAX_TOKENS = 2048
INTER_CALL_DELAY = 3.0
BACKOFF_SCHEDULE = [5, 10, 20, 60]

DIMENSIONS = [
    "Semiotic", "Narrative", "Ideological", "Experiential",
    "Social", "Economic", "Cultural", "Temporal",
]

CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

BRANDS = list(CANONICAL_PROFILES.keys())

FORMAT_CONDITIONS = ["F1_json", "F2_prose", "F3_tabular", "F4_ranked", "F5_vector"]

# ---------------------------------------------------------------------------
# Brand function data (from r15 brand_functions/*.json)
# ---------------------------------------------------------------------------

BRAND_FUNCTIONS = {
    "Hermes": {
        "semiotic": {"score": 9.5, "positioning": "Handcrafted luxury with deliberate restraint. Orange box as icon. No visible logos on most products. Typography and materials communicate exclusivity without declaration.", "key_signals": ["Birkin silhouette", "orange packaging", "saddle-stitching", "no visible branding on leather goods"]},
        "narrative": {"score": 9.0, "positioning": "Equestrian heritage since 1837. Thierry Hermes, Parisian saddler. Six generations of family stewardship. The brand story is one of continuous craft refinement, not expansion.", "key_signals": ["1837 founding", "equestrian origin", "family ownership", "artisan training program (3+ years per craftsman)"]},
        "ideological": {"score": 7.0, "positioning": "Quiet excellence over conspicuous consumption. Anti-trend. Objects are made to last decades. Sustainability through durability rather than through messaging.", "key_signals": ["lifetime repair policy", "no seasonal markdowns", "limited production", "anti-fast-fashion stance"]},
        "experiential": {"score": 9.0, "positioning": "Tactile luxury. Every touchpoint is choreographed: the weight of the box, the ribbon, the tissue paper, the store architecture. Purchase is a ceremony.", "key_signals": ["white-glove service", "appointment-based purchasing for key items", "store as gallery", "packaging as ritual"]},
        "social": {"score": 8.5, "positioning": "Ultra-exclusive community. Waitlists as social filter. Ownership signals membership in a circle that cannot be bought into directly.", "key_signals": ["Birkin waitlist", "purchase history requirements", "no celebrity endorsements", "word-of-mouth as primary channel"]},
        "economic": {"score": 3.0, "positioning": "Price is a structural barrier, not a value signal. Hermes does not compete on price. Price is set to preserve exclusivity and fund craftsmanship.", "key_signals": ["no sales", "no outlet stores", "annual price increases", "secondary market premium (Birkin appreciates)"]},
        "cultural": {"score": 9.0, "positioning": "French haute couture tradition. Parisian craft culture. The brand is inseparable from French cultural identity and the luxury-as-art philosophy.", "key_signals": ["Paris ateliers", "French craft guilds", "art collaborations", "Fondation d'entreprise Hermes"]},
        "temporal": {"score": 9.5, "positioning": "187 years of continuous operation under the same family. One of the oldest luxury houses. Heritage is not marketed -- it is the brand.", "key_signals": ["1837 founding", "six generations", "unchanged core craft methods", "leather goods still hand-stitched"]},
    },
    "IKEA": {
        "semiotic": {"score": 8.0, "positioning": "Blue-and-yellow Swedish palette is globally legible without language. The BILLY bookcase and POANG chair are objects of cultural recognition. Flat-pack form is itself a sign of the IKEA system.", "key_signals": ["blue-and-yellow wordmark", "Swedish product names", "BILLY and POANG as cultural icons", "flat-pack box as brand signifier"]},
        "narrative": {"score": 7.5, "positioning": "Founded 1943 in Almhult, Sweden by Ingvar Kamprad at age 17. The origin story of democratic design -- good furniture for people with thin wallets -- is embedded in every product and price tag.", "key_signals": ["1943 founding by teenage entrepreneur", "Almhult origin", "Kamprad's frugality mythology", "IKEA name as personal acronym"]},
        "ideological": {"score": 6.0, "positioning": "Democratic design: beautiful, functional, sustainable, and affordable for the many. The ideology is explicit -- IKEA openly states it exists to create 'a better everyday life for the many people.'", "key_signals": ["'democratic design' as named doctrine", "People & Planet Positive sustainability strategy", "solar panels on stores", "circular economy product lines"]},
        "experiential": {"score": 7.0, "positioning": "The warehouse journey is a designed experience: one-way path, room vignettes, meatballs in the cafeteria, and the satisfaction of self-assembly.", "key_signals": ["one-way store layout", "Swedish meatballs as destination", "room vignettes at scale", "flat-pack assembly as ritual"]},
        "social": {"score": 5.0, "positioning": "Mass-market accessibility creates universal familiarity rather than exclusivity. IKEA ownership is a near-universal life-stage marker, particularly among young adults.", "key_signals": ["BILLY bookcase in 1-in-5 European homes", "student and first-home positioning", "IKEA hacking community", "broad demographic reach"]},
        "economic": {"score": 9.0, "positioning": "Price accessibility is the central value proposition and a structural design constraint. Every product starts with a target price point; design works backward from affordability.", "key_signals": ["price-first design process", "IKEA Family loyalty discounts", "visible price tags in every vignette", "annual IKEA catalogue as price reference"]},
        "cultural": {"score": 7.5, "positioning": "Swedish design culture -- minimalism, functionality, hygge-adjacent warmth -- exported globally. IKEA is the world's largest exporter of Scandinavian aesthetic values.", "key_signals": ["Swedish product naming convention", "Scandinavian minimalism aesthetic", "Almhult Design Centre", "Swedish food court as cultural export"]},
        "temporal": {"score": 6.0, "positioning": "80+ years of continuous operation with the founding philosophy intact. Products are periodically updated but core lines span decades, creating generational continuity.", "key_signals": ["1943 founding", "BILLY bookcase unchanged since 1979", "three-generation brand familiarity", "annual catalogue as temporal ritual"]},
    },
    "Patagonia": {
        "semiotic": {"score": 6.0, "positioning": "The mountain silhouette logo and muted earth-tone palette signal outdoor authenticity without luxury posturing. Patagonia gear is recognized by those who use it, not by those who display it.", "key_signals": ["Fitzroy mountain wordmark", "earth-tone colorways", "simple fleece as category-defining object", "repair patches as visible brand signal"]},
        "narrative": {"score": 9.0, "positioning": "Yvon Chouinard's 1973 founding from a blacksmith shop making reusable climbing pitons. The story of a reluctant capitalist building a company to save the planet is Patagonia's most powerful product.", "key_signals": ["1973 founding from climbing hardware roots", "Chouinard's memoir", "2022 transfer of ownership to Earth Tax trust", "'Don't Buy This Jacket' 2011 ad"]},
        "ideological": {"score": 9.5, "positioning": "Environmental activism is not a marketing position -- it is the governing logic of the company. In 2022, Chouinard transferred ownership to a nonprofit trust dedicated to fighting climate change.", "key_signals": ["1% for the Planet founding member", "2022 Holdfast Collective ownership transfer", "anti-growth statements", "Worn Wear repair and resale program"]},
        "experiential": {"score": 7.5, "positioning": "Products are tools for genuine outdoor activity. The experiential dimension is in field performance -- gear tested in Patagonia the region, not just named after it.", "key_signals": ["field-testing in extreme conditions", "lifetime guarantee", "repair centers in stores", "Worn Wear trucks"]},
        "social": {"score": 8.0, "positioning": "Tight community of outdoor athletes, environmentalists, and activists. Brand membership implies values alignment, not just product ownership.", "key_signals": ["environmental grant program ($140M+ donated)", "grassroots activism network", "Patagonia Action Works platform", "ambassador athletes"]},
        "economic": {"score": 5.0, "positioning": "Premium pricing justified by product longevity and repair infrastructure, not exclusivity. Patagonia explicitly argues that buying less but better is the ethical consumer choice.", "key_signals": ["premium price points", "no seasonal sales on core gear", "Worn Wear secondhand platform", "repair cost transparency"]},
        "cultural": {"score": 7.0, "positioning": "West Coast American outdoor culture -- Ventura, California roots, surf-and-climb ethos -- combined with global environmental movement.", "key_signals": ["Ventura headquarters", "surf-to-climb culture origin", "environmental litigation participation", "Patagonia Films"]},
        "temporal": {"score": 6.5, "positioning": "50+ years of consistent mission, with the 2022 ownership transfer as a permanent structural commitment to longevity beyond any founder's lifespan.", "key_signals": ["1973 founding", "2022 Holdfast trust as permanent structure", "Worn Wear extending product lifespan", "multi-decade customer relationships"]},
    },
    "Erewhon": {
        "semiotic": {"score": 7.0, "positioning": "Minimalist earth-tone store aesthetic, hand-lettered signage, and brown paper bags signal ethical purity without corporate polish. The $20 smoothie cup is itself a social currency token.", "key_signals": ["brown paper bag as social signal", "$20+ smoothie as status object", "hand-lettered produce labels", "tonic bar as physical centerpiece"]},
        "narrative": {"score": 6.5, "positioning": "Founded 1966 in Boston by Aveline and Michio Kushi as a macrobiotic food store. Revived in LA by Tony and Josephine Antoci. The narrative blends 1960s counterculture health philosophy with 2020s wellness capital.", "key_signals": ["1966 macrobiotic origins", "Kushi Institute lineage", "LA revival as cultural inflection point", "Hailey Bieber tonic as viral origin moment"]},
        "ideological": {"score": 5.0, "positioning": "Wellness as lifestyle ideology: organic, biodynamic, raw, and regenerative sourcing presented as moral choices. The ideology is real but increasingly entangled with social performance.", "key_signals": ["certified organic sourcing policy", "regenerative agriculture partnerships", "no seed oils policy", "biodynamic wine selection"]},
        "experiential": {"score": 9.0, "positioning": "The store is a full sensory environment -- smells, sounds, textures, and social theater. Shopping at Erewhon is an activity, not a transaction.", "key_signals": ["tonic bar as social gathering point", "store ambiance as wellness spa", "sampling culture", "celebrity sightings as experiential layer"]},
        "social": {"score": 8.5, "positioning": "Extreme social exclusivity through price. The Erewhon shopper is a visible status category in LA -- a demographic of wellness-affluent consumers.", "key_signals": ["$20-30 smoothies as social filter", "celebrity regular customer circuit", "branded collaborations with influencers", "parking lot as social scene"]},
        "economic": {"score": 3.5, "positioning": "Price is a near-exclusionary barrier. Erewhon makes no concessions to affordability -- the premium is structural and deliberate.", "key_signals": ["$13+ green juice standard pricing", "no discount programs", "no private label budget tier", "price premium 3-5x conventional grocery"]},
        "cultural": {"score": 7.5, "positioning": "LA wellness culture as its own subculture: the intersection of Hollywood, health optimization, and conspicuous virtue.", "key_signals": ["Beverly Hills and Silver Lake locations", "influencer content hub", "wellness culture media coverage", "Hailey Bieber smoothie as cultural artifact"]},
        "temporal": {"score": 2.5, "positioning": "Despite a 1966 founding, Erewhon's current cultural moment is recent and acutely of-the-moment. The brand's peak relevance is tightly tied to 2020s LA wellness culture.", "key_signals": ["2011 LA relaunch as effective brand birth", "viral moment dependency (2021-2023)", "rapidly shifting product collaborations", "trend-sensitive customer base"]},
    },
    "Tesla": {
        "semiotic": {"score": 7.5, "positioning": "The T-badge and Cybertruck silhouette are instantly legible as technological disruption signals. Tesla's visual language borrows from aerospace and consumer electronics.", "key_signals": ["T-badge as technology marker", "Cybertruck form as radical departure", "minimalist interior as anti-dashboard statement", "no grille as visible EV signal"]},
        "narrative": {"score": 8.5, "positioning": "Founded 2003, then transformed under Elon Musk into a mission narrative: accelerating the world's transition to sustainable energy. The narrative is grand, technological, and founder-dependent.", "key_signals": ["'accelerating sustainable energy transition' mission", "Elon Musk as narrative engine", "Roadster as proof-of-concept origin story", "SpaceX parallel as narrative amplifier"]},
        "ideological": {"score": 3.0, "positioning": "The founding environmental ideology has significantly eroded. Tesla began as a climate mission; by the mid-2020s the brand's ideological coherence is contested.", "key_signals": ["original 'sustainable energy' mission text", "2024-2025 sales decline in progressive markets", "owner community ideological splits", "growing separation between product and founder values"]},
        "experiential": {"score": 6.0, "positioning": "Over-the-air software updates, Autopilot engagement, and in-car gaming create an experience closer to a connected device than a vehicle.", "key_signals": ["OTA software updates", "Autopilot as feature and controversy", "17-inch touchscreen", "service center scarcity as friction point"]},
        "social": {"score": 7.0, "positioning": "Tesla ownership was a strong social signal of tech-forward environmental values. That signal has become ambiguous.", "key_signals": ["early-adopter tech community", "shifting ownership demographics", "Tesla owner forums", "geographic variation in social signal valence"]},
        "economic": {"score": 6.0, "positioning": "Multiple price cuts since 2023 have repositioned Tesla from premium to competitive-mainstream on cost.", "key_signals": ["2023 price cuts of 20-30%", "base Model 3 under $40K post-incentives", "no dealership margin extraction", "supercharger network as economic moat"]},
        "cultural": {"score": 4.0, "positioning": "Silicon Valley tech culture transplanted into automotive -- move fast, iterate in public, dismiss legacy incumbents.", "key_signals": ["Silicon Valley origin and ethos", "direct sales model", "Gigafactory as cultural spectacle", "Musk persona as cultural liability/asset"]},
        "temporal": {"score": 2.0, "positioning": "Tesla was founded in 2003 and has no deep heritage. The brand's legitimacy is built on future promise, not historical continuity.", "key_signals": ["2003 founding with no automotive heritage", "product cycles measured in software versions", "Cybertruck as 'future aesthetic' without historical anchor", "mission framed around future transition"]},
    },
}


# ---------------------------------------------------------------------------
# Latin-square orderings
# ---------------------------------------------------------------------------

def get_ordering(trial_index: int) -> list[str]:
    """Return a cyclic Latin-square ordering for a given trial index."""
    n = len(DIMENSIONS)
    i = trial_index % n
    return [DIMENSIONS[(i + j) % n] for j in range(n)]


# ---------------------------------------------------------------------------
# Format generators
# ---------------------------------------------------------------------------

def format_f1_json(brand: str, ordering: list[str]) -> str:
    """F1: Full JSON brand function with scores, positioning, key_signals."""
    bf = BRAND_FUNCTIONS[brand]
    spec = {}
    for dim in ordering:
        dim_lower = dim.lower()
        d = bf[dim_lower]
        spec[dim] = {
            "score": d["score"],
            "positioning": d["positioning"],
            "key_signals": d["key_signals"],
        }
    json_str = json.dumps({"brand": brand, "dimensions": spec}, indent=2)
    return (
        f"Here is the full brand function specification for {brand}:\n\n"
        f"{json_str}\n\n"
        f"Based on this brand specification, allocate exactly 100 points across these "
        f"eight dimensions to reflect the brand's relative emphasis. "
        f"Your weights MUST sum to exactly 100. Respond with valid JSON only: {{{', '.join(f'\"{d}\": X' for d in ordering)}}}."
    )


def format_f2_prose(brand: str, ordering: list[str]) -> str:
    """F2: Prose narrative description of the brand across all dimensions."""
    bf = BRAND_FUNCTIONS[brand]
    paragraphs = []
    for dim in ordering:
        dim_lower = dim.lower()
        d = bf[dim_lower]
        signals = ", ".join(d["key_signals"][:3])
        paragraphs.append(
            f"On the {dim} dimension, {brand} is characterized by: {d['positioning']} "
            f"Key signals include {signals}."
        )
    prose = " ".join(paragraphs)
    return (
        f"Here is a description of {brand}'s brand positioning:\n\n"
        f"{prose}\n\n"
        f"Based on this brand description, allocate exactly 100 points across these "
        f"eight dimensions to reflect the brand's relative emphasis. "
        f"Your weights MUST sum to exactly 100. Respond with valid JSON only: {{{', '.join(f'\"{d}\": X' for d in ordering)}}}."
    )


def format_f3_tabular(brand: str, ordering: list[str]) -> str:
    """F3: Tabular minimal -- dimension name + brief positioning only (no scores)."""
    bf = BRAND_FUNCTIONS[brand]
    rows = []
    for dim in ordering:
        pos = bf[dim.lower()]["positioning"][:100]
        rows.append(f"  {dim}: {pos}")
    table = "\n".join(rows)
    return (
        f"Here are {brand}'s brand dimension descriptions:\n\n"
        f"{table}\n\n"
        f"Based on these brand dimension descriptions, allocate exactly 100 points across these "
        f"eight dimensions to reflect the brand's relative emphasis. "
        f"Your weights MUST sum to exactly 100. Respond with valid JSON only: {{{', '.join(f'\"{d}\": X' for d in ordering)}}}."
    )


def format_f4_ranked(brand: str, ordering: list[str]) -> str:
    """F4: Ranked list -- dimensions ranked by importance with rationale (no scores)."""
    bf = BRAND_FUNCTIONS[brand]
    ranked = sorted(
        [(dim, bf[dim.lower()]["score"], bf[dim.lower()]["positioning"][:80])
         for dim in DIMENSIONS],
        key=lambda x: x[1],
        reverse=True,
    )
    lines = []
    for rank, (dim, _score, desc) in enumerate(ranked, 1):
        lines.append(f"  {rank}. {dim} -- {desc}")
    rank_text = "\n".join(lines)
    return (
        f"Here is {brand}'s brand priority ranking (most to least important):\n\n"
        f"{rank_text}\n\n"
        f"Based on this brand priority ranking, allocate exactly 100 points across these "
        f"eight dimensions to reflect the brand's relative emphasis. "
        f"Your weights MUST sum to exactly 100. Respond with valid JSON only: {{{', '.join(f'\"{d}\": X' for d in ordering)}}}."
    )


def _score_to_level(score: float) -> str:
    """Convert a 0-10 score to a qualitative level (no numeric leakage)."""
    if score >= 9.0:
        return "Very High"
    elif score >= 7.0:
        return "High"
    elif score >= 5.0:
        return "Moderate"
    elif score >= 3.0:
        return "Low"
    else:
        return "Very Low"


def format_f5_vector(brand: str, ordering: list[str]) -> str:
    """F5: Qualitative levels -- ordinal descriptors without numeric scores."""
    bf = BRAND_FUNCTIONS[brand]
    rows = []
    for dim in ordering:
        level = _score_to_level(bf[dim.lower()]["score"])
        rows.append(f"  {dim}: {level}")
    level_text = "\n".join(rows)
    return (
        f"Here are {brand}'s brand dimension importance levels:\n\n"
        f"{level_text}\n\n"
        f"Based on these importance levels, allocate exactly 100 points across the eight "
        f"dimensions to reflect the brand's relative emphasis. Your weights MUST sum to "
        f"exactly 100. "
        f"Your weights MUST sum to exactly 100. Respond with valid JSON only: {{{', '.join(f'\"{d}\": X' for d in ordering)}}}."
    )


FORMAT_FNS = {
    "F1_json": format_f1_json,
    "F2_prose": format_f2_prose,
    "F3_tabular": format_f3_tabular,
    "F4_ranked": format_f4_ranked,
    "F5_vector": format_f5_vector,
}

SYSTEM_PROMPT = (
    "You are a brand perception analyst. You will be given information about a brand's "
    "positioning across eight perceptual dimensions. Your task is to read the brand "
    "specification and then produce a perceptual weight profile: allocate exactly 100 "
    "points across the eight dimensions to reflect the brand's relative emphasis. "
    "IMPORTANT: Your weights MUST sum to exactly 100. Verify your total before responding. "
    "Respond with valid JSON only."
)


# ---------------------------------------------------------------------------
# API callers (self-contained, from experiment_shared/api_callers.py)
# ---------------------------------------------------------------------------

STANDARD_MODELS = {
    "claude-haiku-4-5": {
        "provider": "anthropic",
        "model_id": "claude-haiku-4-5-20251001",
        "env_var": "ANTHROPIC_API_KEY",
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "model_id": "gpt-4o-mini",
        "env_var": "OPENAI_API_KEY",
    },
    "gemini-2.5-flash": {
        "provider": "google",
        "model_id": "gemini-2.5-flash",
        "env_var": "GOOGLE_API_KEY",
    },
    "deepseek-chat": {
        "provider": "deepseek",
        "model_id": "deepseek-chat",
        "env_var": "DEEPSEEK_API_KEY",
    },
    "grok-4-1-fast": {
        "provider": "xai",
        "model_id": "grok-4-1-fast-non-reasoning",
        "env_var": "GROK_API_KEY",
    },
}


def available_models() -> dict:
    return {
        name: info
        for name, info in STANDARD_MODELS.items()
        if os.environ.get(info["env_var"])
    }


def call_claude(prompt: str, system_prompt: str = "") -> tuple[str, dict]:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    kwargs = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt
    t0 = time.time()
    message = client.messages.create(**kwargs)
    elapsed = int((time.time() - t0) * 1000)
    return message.content[0].text, {
        "response_time_ms": elapsed,
        "token_count_input": message.usage.input_tokens,
        "token_count_output": message.usage.output_tokens,
    }


def call_gpt(prompt: str, system_prompt: str = "") -> tuple[str, dict]:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    t0 = time.time()
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages,
        max_tokens=MAX_TOKENS, temperature=TEMPERATURE,
    )
    elapsed = int((time.time() - t0) * 1000)
    return response.choices[0].message.content, {
        "response_time_ms": elapsed,
        "token_count_input": response.usage.prompt_tokens,
        "token_count_output": response.usage.completion_tokens,
    }


def call_gemini(prompt: str, system_prompt: str = "") -> tuple[str, dict]:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    sys_instr = system_prompt or "You are a brand research assistant. Respond with valid JSON only."
    t0 = time.time()
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE,
            max_output_tokens=8192,
            system_instruction=sys_instr,
        ),
    )
    elapsed = int((time.time() - t0) * 1000)
    try:
        text = response.text
    except Exception:
        if response.candidates:
            text = response.candidates[0].content.parts[0].text
        else:
            raise ValueError("Gemini returned no usable response candidates")
    return text, {
        "response_time_ms": elapsed,
        "token_count_input": getattr(getattr(response, "usage_metadata", None), "prompt_token_count", 0),
        "token_count_output": getattr(getattr(response, "usage_metadata", None), "candidates_token_count", 0),
    }


def _call_openai_compatible(
    prompt: str, system_prompt: str, model: str, env_var: str, base_url: str
) -> tuple[str, dict]:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ[env_var], base_url=base_url)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    t0 = time.time()
    response = client.chat.completions.create(
        model=model, messages=messages,
        max_tokens=MAX_TOKENS, temperature=TEMPERATURE,
    )
    elapsed = int((time.time() - t0) * 1000)
    content = response.choices[0].message.content or ""
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    content = re.sub(r"```(?:json)?\s*", "", content).strip()
    content = re.sub(r"```\s*$", "", content).strip()
    return content, {
        "response_time_ms": elapsed,
        "token_count_input": getattr(getattr(response, "usage", None), "prompt_tokens", 0),
        "token_count_output": getattr(getattr(response, "usage", None), "completion_tokens", 0),
    }


def call_deepseek(prompt: str, system_prompt: str = "") -> tuple[str, dict]:
    return _call_openai_compatible(
        prompt, system_prompt, "deepseek-chat", "DEEPSEEK_API_KEY", "https://api.deepseek.com"
    )


def call_grok(prompt: str, system_prompt: str = "") -> tuple[str, dict]:
    return _call_openai_compatible(
        prompt, system_prompt, "grok-4-1-fast-non-reasoning", "GROK_API_KEY", "https://api.x.ai/v1"
    )


CALLERS = {
    "claude-haiku-4-5": call_claude,
    "gpt-4o-mini": call_gpt,
    "gemini-2.5-flash": call_gemini,
    "deepseek-chat": call_deepseek,
    "grok-4-1-fast": call_grok,
}


def call_model(model_name: str, prompt: str, system_prompt: str = "") -> tuple[str, dict]:
    caller = CALLERS[model_name]
    last_err = None
    for attempt, backoff in enumerate([0] + BACKOFF_SCHEDULE):
        if backoff > 0:
            print(f"  [backoff] {model_name}: waiting {backoff}s (attempt {attempt + 1})")
            time.sleep(backoff)
        try:
            text, meta = caller(prompt, system_prompt=system_prompt)
            meta["model_id"] = STANDARD_MODELS[model_name]["model_id"]
            meta["model_provider"] = STANDARD_MODELS[model_name]["provider"]
            return text, meta
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "rate" in err_str.lower():
                last_err = e
                continue
            raise
    raise RuntimeError(f"Exhausted backoff for {model_name}: {last_err}")


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def parse_weights(raw: str) -> Optional[dict[str, float]]:
    """Extract dimension weights from a JSON response."""
    text = raw.strip()
    text = text.replace("```json", "").replace("```", "").strip()
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
        data = json.loads(text[start:end])
    except json.JSONDecodeError:
        return None
    if "weights" in data and isinstance(data["weights"], dict):
        data = data["weights"]
    result = {}
    for dim in DIMENSIONS:
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


def cosine_sim(a: list[float], b: list[float]) -> float:
    a_arr = np.array(a, dtype=float)
    b_arr = np.array(b, dtype=float)
    dot = np.dot(a_arr, b_arr)
    na = np.linalg.norm(a_arr)
    nb = np.linalg.norm(b_arr)
    if na == 0 or nb == 0:
        return 0.0
    return float(dot / (na * nb))


def compute_dci(weights: dict[str, float]) -> float:
    total = sum(weights.values())
    if total == 0:
        return 0.0
    return (weights.get("Economic", 0) + weights.get("Semiotic", 0)) / total


def estimate_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
    pricing = {
        "claude-haiku-4-5": (0.80, 4.00),
        "gpt-4o-mini": (0.15, 0.60),
        "gemini-2.5-flash": (0.15, 0.60),
        "deepseek-chat": (0.27, 1.10),
        "grok-4-1-fast": (0.60, 4.00),
    }
    rates = pricing.get(model_name, (1.0, 4.0))
    return (input_tokens * rates[0] + output_tokens * rates[1]) / 1_000_000


# ---------------------------------------------------------------------------
# JSONL record
# ---------------------------------------------------------------------------

def make_record(
    model_id: str, model_provider: str, brand: str, condition: str,
    repetition: int, system_prompt: str, user_prompt: str,
    raw_response: str, parsed_weights: Optional[dict[str, float]],
    response_time_ms: int, token_count_input: int, token_count_output: int,
    api_cost_usd: float, dimension_order: list[str],
    canonical_cosine: Optional[float] = None,
) -> dict:
    weights_valid = parsed_weights is not None
    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "experiment": "exp_d_bf_format",
        "model_id": model_id,
        "model_provider": model_provider,
        "temperature": TEMPERATURE,
        "top_p": 1.0,
        "max_tokens": MAX_TOKENS,
        "system_prompt_hash": f"sha256:{hashlib.sha256(system_prompt.encode()).hexdigest()[:16]}",
        "user_prompt_hash": f"sha256:{hashlib.sha256(user_prompt.encode()).hexdigest()[:16]}",
        "user_prompt": user_prompt,
        "brand": brand,
        "condition": condition,
        "repetition": repetition,
        "raw_response": raw_response,
        "parsed_weights": parsed_weights,
        "weights_valid": weights_valid,
        "weight_sum_raw": round(sum(parsed_weights.values()), 2) if parsed_weights else 0.0,
        "response_time_ms": response_time_ms,
        "token_count_input": token_count_input,
        "token_count_output": token_count_output,
        "api_cost_usd": round(api_cost_usd, 6),
        "dimension_order": dimension_order,
        "dci": round(compute_dci(parsed_weights), 4) if parsed_weights else None,
        "canonical_cosine": round(canonical_cosine, 4) if canonical_cosine is not None else None,
    }


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Main experiment loop
# ---------------------------------------------------------------------------

def build_trials(reps: int = 3) -> list[dict]:
    """Build all trials: 5 formats x 5 brands x reps."""
    np.random.seed(RANDOM_SEED)
    trials = []
    for brand_idx, brand in enumerate(BRANDS):
        for fmt_idx, fmt in enumerate(FORMAT_CONDITIONS):
            for rep in range(1, reps + 1):
                ordering_idx = (brand_idx * 5 + fmt_idx * 3 + rep) % 8
                ordering = get_ordering(ordering_idx)
                trials.append({
                    "brand": brand,
                    "condition": fmt,
                    "repetition": rep,
                    "ordering_index": ordering_idx,
                    "ordering": ordering,
                })
    # Shuffle to avoid systematic provider fatigue
    np.random.shuffle(trials)
    return trials


def run_experiment(dry_run: bool = False, reps: int = 3) -> dict:
    """Execute the full experiment."""
    models = available_models()
    if not models:
        print("ERROR: No API keys found.")
        sys.exit(1)

    trials = build_trials(reps)
    total_calls = len(trials) * len(models)

    output_dir = Path(__file__).parent.parent / "L3_sessions"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "exp_bf_format_v2.jsonl"

    print(f"\n{'=' * 60}")
    print(f"Experiment D: Brand Function Format Optimization")
    print(f"Models: {', '.join(models.keys())}")
    print(f"Trials: {len(trials)} x {len(models)} models = {total_calls} calls")
    print(f"Output: {output_path}")
    print(f"{'=' * 60}\n")

    if dry_run:
        print("[DRY RUN] Would execute above. Exiting.")
        return {"total_calls": total_calls, "dry_run": True}

    stats = {
        "total_calls": 0,
        "successful": 0,
        "failed": 0,
        "parse_errors": 0,
        "total_cost": 0.0,
        "per_model": {},
        "per_format": {f: {"calls": 0, "success": 0} for f in FORMAT_CONDITIONS},
    }

    for trial_idx, trial in enumerate(trials):
        brand = trial["brand"]
        condition = trial["condition"]
        rep = trial["repetition"]
        ordering = trial["ordering"]
        format_fn = FORMAT_FNS[condition]
        prompt = format_fn(brand, ordering)

        for model_name, model_info in models.items():
            stats["total_calls"] += 1
            m_stats = stats["per_model"].setdefault(
                model_name, {"calls": 0, "success": 0, "failed": 0, "cost": 0.0}
            )
            m_stats["calls"] += 1
            stats["per_format"][condition]["calls"] += 1

            call_num = stats["total_calls"]
            print(
                f"  [{call_num:4d}/{total_calls}] {model_name:20s} | {brand:12s} | "
                f"{condition:12s} | rep {rep}",
                end="", flush=True,
            )

            try:
                raw_response, meta = call_model(model_name, prompt, SYSTEM_PROMPT)
                parsed = parse_weights(raw_response)

                cost = estimate_cost(
                    model_name,
                    meta.get("token_count_input", 0),
                    meta.get("token_count_output", 0),
                )

                # Compute cosine similarity to canonical
                canonical_cosine = None
                if parsed:
                    canonical = CANONICAL_PROFILES[brand]
                    observed = [parsed.get(dim, 0.0) for dim in DIMENSIONS]
                    canonical_cosine = cosine_sim(observed, canonical)

                record = make_record(
                    model_id=meta.get("model_id", model_info["model_id"]),
                    model_provider=meta.get("model_provider", model_info["provider"]),
                    brand=brand,
                    condition=condition,
                    repetition=rep,
                    system_prompt=SYSTEM_PROMPT,
                    user_prompt=prompt,
                    raw_response=raw_response,
                    parsed_weights=parsed,
                    response_time_ms=meta.get("response_time_ms", 0),
                    token_count_input=meta.get("token_count_input", 0),
                    token_count_output=meta.get("token_count_output", 0),
                    api_cost_usd=cost,
                    dimension_order=ordering,
                    canonical_cosine=canonical_cosine,
                )
                append_jsonl(output_path, record)

                if parsed:
                    stats["successful"] += 1
                    m_stats["success"] += 1
                    stats["per_format"][condition]["success"] += 1
                    print(f" | OK cos={canonical_cosine:.3f} DCI={compute_dci(parsed):.3f}")
                else:
                    stats["parse_errors"] += 1
                    m_stats["failed"] += 1
                    print(f" | PARSE_ERROR")

                stats["total_cost"] += cost
                m_stats["cost"] += cost

            except Exception as e:
                stats["failed"] += 1
                m_stats["failed"] += 1
                print(f" | ERROR: {e}")

                record = make_record(
                    model_id=model_info["model_id"],
                    model_provider=model_info["provider"],
                    brand=brand,
                    condition=condition,
                    repetition=rep,
                    system_prompt=SYSTEM_PROMPT,
                    user_prompt=prompt,
                    raw_response=f"ERROR: {e}",
                    parsed_weights=None,
                    response_time_ms=0,
                    token_count_input=0,
                    token_count_output=0,
                    api_cost_usd=0.0,
                    dimension_order=ordering,
                )
                append_jsonl(output_path, record)

            time.sleep(INTER_CALL_DELAY)

    print(f"\n{'=' * 60}")
    print(f"Complete: {stats['successful']}/{stats['total_calls']} successful")
    print(f"Parse errors: {stats['parse_errors']}")
    print(f"Failed: {stats['failed']}")
    print(f"Total cost: ${stats['total_cost']:.2f}")
    print(f"\nPer-format success rates:")
    for fmt, fs in stats["per_format"].items():
        rate = fs["success"] / fs["calls"] * 100 if fs["calls"] > 0 else 0
        print(f"  {fmt}: {fs['success']}/{fs['calls']} ({rate:.0f}%)")
    print(f"{'=' * 60}\n")

    # Save stats
    stats_path = output_dir / "exp_bf_format_v2_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)

    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experiment D: Brand Function Format Optimization")
    parser.add_argument("--dry-run", action="store_true", help="Preview without executing")
    parser.add_argument("--reps", type=int, default=3, help="Repetitions per cell (default: 3)")
    args = parser.parse_args()
    run_experiment(dry_run=args.dry_run, reps=args.reps)
