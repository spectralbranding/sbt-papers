#!/usr/bin/env python3
"""R15: AI Search Metamerism Experiment

Tests whether LLMs produce convergent brand recommendations that mask structural
differences across SBT's 8 perception dimensions. The central claim: LLMs
systematically over-weight Economic and Semiotic dimensions (quantifiable,
explicit in training data) and under-weight Narrative, Ideological, Cultural,
and Temporal dimensions (perception-dependent, harder to extract from text corpora).

This produces a form of spectral metamerism: brands that appear identical through
AI-mediated search may have structurally different perception clouds when observed
directly by human cohorts across all 8 dimensions.

Paper: Zharnikov, D. (2026v). Spectral Metamerism in AI-Mediated Brand Perception.
       Target: Journal of Advertising Research (JAR special call on AI + search).

Measures:
  (i)  Dimensional citation frequency: which of the 8 SBT dimensions do LLMs
       surface in recommendation and differentiation prompts?
  (ii) Dimensional collapse index: ratio of Economic + Semiotic citations to
       total citations; values approaching 1.0 indicate high collapse.
  (iii) Cross-model convergence: Fleiss' kappa on dimensional citation patterns
        across the 6 model families.
  (iv) Dimension-specific probe variance: cross-model variance in dimension scores;
       low variance on Economic/Semiotic, high variance on Cultural/Temporal =
       evidence of differential dimensional sensitivity.

LLM providers supported (all optional -- skip if API key missing):
  - Claude (Anthropic): ANTHROPIC_API_KEY
  - GPT (OpenAI): OPENAI_API_KEY
  - Gemini (Google): GOOGLE_API_KEY
  - DeepSeek: DEEPSEEK_API_KEY (OpenAI-compatible)
  - Qwen Plus (Alibaba DashScope): DASHSCOPE_API_KEY (OpenAI-compatible)
  - Qwen3 30B (local Ollama): requires Ollama running at localhost:11434
  - Gemma 4 27B (local Ollama): requires Ollama running at localhost:11434

Usage:
    python ai_search_metamerism.py --demo
    python ai_search_metamerism.py --live --runs 1
    python ai_search_metamerism.py --live --runs 3 --output results.json

License: MIT
"""

import argparse
import datetime
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
import textwrap
import time
import urllib.request
from dataclasses import dataclass, field, asdict
from math import asin, sqrt
from pathlib import Path
from typing import Any, Optional


import numpy as np
import yaml


# ---------------------------------------------------------------------------
# Pre-registration protocol (embedded -- written before data collection)
# ---------------------------------------------------------------------------

PRE_REGISTRATION = """
## Pre-Registration Protocol

### Study
R15: Spectral Metamerism in AI-Mediated Brand Perception
Paper: Zharnikov (2026v), target JAR special call on AI + search

### Hypotheses

H1 (Dimensional over-weighting): LLMs will cite Economic and Semiotic dimensions
    significantly more frequently than other dimensions in recommendation and
    differentiation prompts. Test: one-sample binomial test against uniform baseline
    (12.5% per dimension), p < 0.05.

H2 (Convergent collapse): Dimensional citation frequency will be correlated across
    model families (cross-model Fleiss' kappa >= 0.40), indicating that the collapse
    pattern is systematic rather than model-specific.

H3 (Differential probe variance): Cross-model variance in dimension-specific probe
    scores will be significantly lower for Economic and Semiotic dimensions than for
    Narrative, Cultural, and Temporal dimensions (F-test on variance ratios, p < 0.05).

H4 (Soft-dimension pair convergence): Brand pairs differentiated primarily on
    Narrative, Ideological, Cultural, or Temporal dimensions will show higher
    cross-model recommendation convergence (lower variance, higher Fleiss' kappa)
    than pairs differentiated on Semiotic, Economic, or Experiential dimensions.

### Stopping Rules
- Minimum: 3 runs per prompt per model (established before data collection)
- If H1 binomial p > 0.10 after 3 runs: extend to 5 runs
- If H1 binomial p > 0.10 after 5 runs: report null result with power analysis

### Analysis Plan
Primary:
  - Dimensional citation frequency per model and aggregate (recommendation +
    differentiation prompts)
  - One-sample binomial test: Economic + Semiotic citation rate vs uniform baseline

Secondary:
  - Fleiss' kappa on citation presence/absence per dimension across models
  - F-test on cross-model probe score variance by dimension cluster (hard vs soft)
  - Dimensional collapse index per brand pair (DCI = (Economic + Semiotic) / Total)

Exploratory:
  - Per-brand-pair DCI vs human-judged spectral distance
  - Western vs Chinese vs local model cluster comparison
  - Correlation between DCI and dimension pair design (hard vs soft differentiator)

### Exclusion Criteria
- API errors resulting in unparseable responses: recorded with error field in JSONL
- Models with >50% error rate in any prompt type: excluded from aggregate statistics,
  reported separately
- Dimension probe responses where score cannot be parsed as 0-10 numeric:
  recorded as null and excluded from variance analysis
"""


# ---------------------------------------------------------------------------
# SBT Dimensions
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

# Plain-language descriptions for dimension probes (no SBT jargon in prompts)
DIMENSION_DESCRIPTIONS = {
    "semiotic": "visual identity and brand recognition (logos, packaging, design language)",
    "narrative": "brand story and origin narrative (founding story, mission, brand mythology)",
    "ideological": "values and beliefs the brand stands for (social causes, environmental stance, ethical commitments)",
    "experiential": "quality and distinctiveness of the customer experience (in-store, online, unboxing, service)",
    "social": "social signaling and community (what owning or using this brand says about you socially)",
    "economic": "value proposition and pricing strategy (price point, perceived value for money)",
    "cultural": "cultural relevance and heritage (connection to cultural movements, traditions, zeitgeist)",
    "temporal": "brand heritage and time horizon (how long the brand has existed, its relationship to time and legacy)",
}

# Which dimensions each brand pair is designed to test (the "hard" differentiators)
# Hard dimensions: Semiotic, Economic, Experiential (more quantifiable)
# Soft dimensions: Narrative, Ideological, Cultural, Temporal (perception-dependent)
HARD_DIMS = {"semiotic", "economic", "experiential"}
SOFT_DIMS = {"narrative", "ideological", "cultural", "temporal"}


# ---------------------------------------------------------------------------
# Brand Pairs
# ---------------------------------------------------------------------------

@dataclass
class BrandPair:
    """A pair of brands designed to differ on specific SBT dimensions."""
    id: str                           # short identifier, e.g. "luxury_heritage"
    brand_a: str
    brand_b: str
    category: str
    differentiating_dims: list[str]   # dimensions that most distinguish A from B
    dim_type: str                     # "hard", "soft", or "mixed"
    description: str                  # brief design rationale


BRAND_PAIRS: list[BrandPair] = [
    BrandPair(
        id="luxury_heritage",
        brand_a="Hermes",
        brand_b="Coach",
        category="luxury leather goods",
        differentiating_dims=["temporal", "cultural"],
        dim_type="soft",
        description="Both are premium leather goods with strong visual identities; "
                    "key difference is temporal depth (Hermes 1837 vs Coach 1941) and "
                    "cultural positioning (Parisian artisanal vs accessible American luxury).",
    ),
    BrandPair(
        id="purpose_driven",
        brand_a="Patagonia",
        brand_b="Columbia",
        category="outdoor apparel",
        differentiating_dims=["ideological", "narrative"],
        dim_type="soft",
        description="Both are outdoor brands with similar price points and product quality; "
                    "key difference is ideological commitment (Patagonia's environmental mission) "
                    "and narrative (Yvon Chouinard founder story vs Columbia's regional origin).",
    ),
    BrandPair(
        id="premium_tech",
        brand_a="Apple",
        brand_b="Samsung",
        category="consumer electronics",
        differentiating_dims=["experiential", "semiotic"],
        dim_type="hard",
        description="Both are premium global tech brands; key difference is experiential ecosystem "
                    "(Apple's end-to-end closed system) and semiotic minimalism vs Samsung's "
                    "feature-forward design language.",
    ),
    BrandPair(
        id="artisanal_food",
        brand_a="Erewhon",
        brand_b="Whole Foods",
        category="specialty grocery",
        differentiating_dims=["social", "economic"],
        dim_type="hard",
        description="Both are premium natural grocery retailers; key difference is social signaling "
                    "(Erewhon as extreme status marker) and economic positioning (Erewhon's "
                    "ultra-premium vs Whole Foods' mass-premium).",
    ),
    BrandPair(
        id="auto_disruption",
        brand_a="Mercedes",
        brand_b="Tesla",
        category="premium automobiles",
        differentiating_dims=["temporal", "ideological"],
        dim_type="soft",
        description="Both are aspirational premium car brands; key difference is temporal depth "
                    "(Mercedes 1886 vs Tesla 2003) and ideology (engineering tradition vs "
                    "sustainable disruption mission).",
    ),
    BrandPair(
        id="indie_beauty",
        brand_a="Glossier",
        brand_b="Maybelline",
        category="cosmetics and beauty",
        differentiating_dims=["narrative", "social"],
        dim_type="mixed",
        description="Both target everyday beauty; key difference is narrative origin "
                    "(Glossier born from Into The Gloss community vs Maybelline's mass-market heritage) "
                    "and social positioning (Glossier as identity marker vs Maybelline as utility).",
    ),
    BrandPair(
        id="craft_spirits",
        brand_a="Hendricks",
        brand_b="Gordons",
        category="gin and spirits",
        differentiating_dims=["cultural", "experiential"],
        dim_type="mixed",
        description="Both are widely distributed gin brands; key difference is cultural eccentricity "
                    "(Hendrick's Victorian curiosity cabinet aesthetic) and experiential ritual "
                    "(Hendrick's cucumber garnish protocol vs Gordon's straightforward serve).",
    ),
    BrandPair(
        id="boutique_hotel",
        brand_a="Aman",
        brand_b="Four Seasons",
        category="luxury hospitality",
        differentiating_dims=["experiential", "temporal"],
        dim_type="mixed",
        description="Both are ultra-luxury hotel groups; key difference is experiential philosophy "
                    "(Aman's minimalist sanctuary vs Four Seasons' full-service luxury) and "
                    "temporal positioning (Aman's timeless retreat vs Four Seasons' institutional heritage).",
    ),
    BrandPair(
        id="heritage_sportswear",
        brand_a="Nike",
        brand_b="Shein",
        category="apparel and footwear",
        differentiating_dims=["narrative", "cultural"],
        dim_type="soft",
        description="Both sell clothing at scale; key difference is narrative legitimacy "
                    "(Nike's athletic heritage and 'Just Do It' mythology vs Shein's purely "
                    "commercial rapid-fashion model) and cultural depth (Nike as cultural institution "
                    "vs Shein as price-driven trend aggregator).",
    ),
    BrandPair(
        id="ethical_finance",
        brand_a="Aspiration",
        brand_b="Chase",
        category="personal banking and finance",
        differentiating_dims=["ideological", "social"],
        dim_type="soft",
        description="Both offer consumer financial products; key difference is ideological commitment "
                    "(Aspiration's fossil-fuel-free banking and carbon offsets vs Chase's conventional "
                    "profit-first model) and social positioning (Aspiration as values statement vs "
                    "Chase as institutional default).",
    ),
]


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

RECOMMENDATION_PROMPT = """You are an AI shopping assistant helping a consumer choose between two brands.

Category: {category}

The consumer says: "I'm looking for {category}. Should I choose {brand_a} or {brand_b}? Explain your recommendation."

Provide a clear recommendation. In your explanation, mention all the factors that drove your recommendation — such as quality, price, values, heritage, community, aesthetics, or any other relevant considerations.

Respond in plain prose (2-4 sentences). Do not use bullet points."""


DIFFERENTIATION_PROMPT = """You are a brand analyst comparing two brands for a consumer research report.

Category: {category}

Compare {brand_a} and {brand_b}. What are the key differences between them? Consider all relevant dimensions: visual identity, brand story, values, customer experience, social meaning, price positioning, cultural relevance, and heritage.

Then provide an overall differentiation score.

You MUST respond with ONLY a valid JSON object (no other text before or after):
{{
  "key_differences": "2-4 sentence description of the most important differences",
  "dimensions_cited": ["list", "of", "factors", "you", "mentioned"],
  "differentiation_score": 0.75
}}

The differentiation_score must be 0.0 (nearly identical) to 1.0 (completely different). The dimensions_cited field must be a JSON array of strings (e.g. ["price", "values", "heritage"])."""


DIMENSION_PROBE_PROMPT = """You are a brand researcher scoring brands on specific attributes.

Rate {brand} on the following attribute:

Attribute: {dimension_description}

Score on a scale of 0 to 10, where:
- 0 = extremely weak or absent on this attribute
- 10 = the global benchmark, one of the best examples in any category

You MUST respond with ONLY a valid JSON object (no other text before or after):
{{
  "dimension": "{dimension}",
  "brand": "{brand}",
  "score": 7.5,
  "reasoning": "Brief explanation of the score (1-2 sentences)"
}}

The score must be a number between 0.0 and 10.0."""


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class ExperimentCall:
    """Raw record of a single LLM call and its parsed output."""
    model: str
    brand_pair: str           # e.g. "Hermes vs Coach"
    pair_id: str              # e.g. "luxury_heritage"
    prompt_type: str          # "recommendation" | "differentiation" | "dimension_probe"
    dimension: Optional[str]  # set for dimension_probe calls only
    brand: Optional[str]      # set for dimension_probe calls only (the brand being scored)
    run: int
    response: str
    parsed: dict
    timestamp: str
    latency_ms: int
    error: Optional[str] = None


@dataclass
class ExperimentResults:
    """Aggregated results for the full experiment."""
    brand_pairs: list[str]
    models: list[str]
    runs: int
    calls: list[dict] = field(default_factory=list)
    dimensional_citation_freq: dict = field(default_factory=dict)
    dimensional_collapse_index: dict = field(default_factory=dict)
    probe_scores: dict = field(default_factory=dict)
    cross_model_variance: dict = field(default_factory=dict)
    statistics: Optional[dict] = None
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# JSON Parsing (robust -- handles markdown fences, trailing commas, prose)
# ---------------------------------------------------------------------------

def parse_llm_json(text: str) -> dict[str, Any]:
    """
    Robustly parse JSON from LLM response text.

    Handles: markdown code fences, leading/trailing prose, partial JSON,
    single-quoted keys, and trailing commas.
    """
    # Strip markdown code fences
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE)
    text = text.strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Extract first {...} block
    match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
    if match:
        candidate = match.group(0)
        # Fix trailing commas before } or ]
        candidate = re.sub(r",\s*([}\]])", r"\1", candidate)
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # Last resort: extract individual known fields by regex
    result: dict[str, Any] = {}

    score_match = re.search(r'"score"\s*:\s*([0-9.]+)', text)
    if score_match:
        result["score"] = float(score_match.group(1))

    diff_match = re.search(r'"differentiation_score"\s*:\s*([0-9.]+)', text)
    if diff_match:
        result["differentiation_score"] = float(diff_match.group(1))

    dims_match = re.search(r'"dimensions_cited"\s*:\s*\[([^\]]*)\]', text)
    if dims_match:
        raw_dims = dims_match.group(1)
        result["dimensions_cited"] = [
            d.strip().strip('"').strip("'").lower()
            for d in raw_dims.split(",")
            if d.strip()
        ]

    diff_text_match = re.search(r'"key_differences"\s*:\s*"([^"]*)"', text)
    if diff_text_match:
        result["key_differences"] = diff_text_match.group(1)

    reason_match = re.search(r'"reasoning"\s*:\s*"([^"]*)"', text)
    if reason_match:
        result["reasoning"] = reason_match.group(1)

    if result:
        return result

    raise ValueError(f"Could not parse JSON from LLM response: {text[:300]}")


# ---------------------------------------------------------------------------
# Dimension Citation Extraction
# ---------------------------------------------------------------------------

# Keywords that map to each SBT dimension for citation extraction from free text
DIMENSION_KEYWORDS: dict[str, list[str]] = {
    "semiotic": [
        "logo", "visual", "design", "packaging", "aesthetic", "identity",
        "look", "appearance", "branding", "iconography", "symbol", "color",
        "recogni",  # recognizable, recognition
    ],
    "narrative": [
        "story", "origin", "founding", "mission", "history", "myth", "narrative",
        "heritage story", "brand journey", "founded", "founder",
    ],
    "ideological": [
        "value", "belief", "mission", "purpose", "ethical", "sustainability",
        "environment", "social cause", "commitment", "principle", "stance",
        "authentic", "transparent", "responsible",
    ],
    "experiential": [
        "experience", "quality", "service", "in-store", "unboxing", "product",
        "craftsmanship", "feel", "texture", "satisfaction", "customer service",
    ],
    "social": [
        "social", "status", "signal", "community", "tribe", "belonging",
        "identity marker", "cool", "prestige", "peer", "aspiration",
    ],
    "economic": [
        "price", "cost", "affordable", "expensive", "value for money", "premium",
        "budget", "luxury price", "accessible", "cheap", "pricing", "roi",
    ],
    "cultural": [
        "culture", "cultural", "zeitgeist", "movement", "tradition", "heritage",
        "zeitgeist", "generation", "trend", "subculture", "relevance",
    ],
    "temporal": [
        "heritage", "legacy", "history", "long-standing", "established", "decades",
        "centuries", "old", "classic", "timeless", "since ", "years",
    ],
}


def extract_cited_dimensions(text: str, explicit_dims: Optional[list[str]] = None) -> list[str]:
    """
    Extract SBT dimensions cited in a response.

    First uses any explicit dimensions_cited field from JSON, then falls back
    to keyword matching on the full response text. Returns a deduplicated list
    of dimension names.
    """
    cited = set()

    # Use explicit citations if available
    if explicit_dims:
        for d in explicit_dims:
            d_lower = d.lower().strip()
            # Direct dimension name match
            for dim in DIMENSIONS:
                if dim in d_lower or d_lower in dim:
                    cited.add(dim)
                    break

    # Keyword matching on response text
    text_lower = text.lower()
    for dim, keywords in DIMENSION_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                cited.add(dim)
                break

    return sorted(cited)


# ---------------------------------------------------------------------------
# Model-Specific API Callers (reused from R16, temperature=0.7)
# ---------------------------------------------------------------------------

def call_claude(prompt: str, model: str = "claude-haiku-4-5") -> str:
    """Call Anthropic Claude API at temperature 0.7 and return response text."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model=model,
        max_tokens=512,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def call_gpt(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Call OpenAI GPT API at temperature 0.7 and return response text."""
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7,
    )
    return response.choices[0].message.content


def call_gemini(prompt: str, model: str = "gemini-2.5-flash") -> str:
    """Call Google Gemini via google-genai SDK at temperature 0.7 and return response text."""
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7, max_output_tokens=512),
    )
    return response.text


def call_deepseek(prompt: str, model: str = "deepseek-chat") -> str:
    """Call DeepSeek API (OpenAI-compatible) at temperature 0.7 and return response text."""
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7,
    )
    return response.choices[0].message.content


def call_qwen(prompt: str, model: str = "qwen-plus-latest") -> str:
    """Call Qwen via Alibaba DashScope API (OpenAI-compatible) at temperature 0.7."""
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["DASHSCOPE_API_KEY"],
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7,
    )
    return response.choices[0].message.content


def call_qwen3_local(prompt: str, model: str = "qwen3:30b") -> str:
    """Call Qwen3 30B via local Ollama with fallback to native /api/generate.

    Qwen3 thinking mode may put content in reasoning_content instead of content.
    We check both fields and strip think tags.
    """
    # Attempt 1: OpenAI-compatible endpoint with system message to suppress thinking
    try:
        from openai import OpenAI
        client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a brand research assistant. "
                        "Respond with ONLY valid JSON. "
                        "No markdown, no explanation, no thinking -- just the JSON."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        msg = response.choices[0].message
        content = msg.content or ""
        if not content.strip() and hasattr(msg, "reasoning_content") and msg.reasoning_content:
            content = msg.reasoning_content
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        content = re.sub(r"```(?:json)?\s*", "", content).strip()
        content = re.sub(r"```\s*$", "", content).strip()
        if content.strip():
            return content
    except Exception:
        pass

    # Attempt 2: Ollama native /api/generate (bypasses OpenAI-compatible layer)
    payload = json.dumps({
        "model": model,
        "prompt": prompt + "\n\nRespond with ONLY a JSON object:",
        "stream": False,
        "options": {"num_predict": 1024, "temperature": 0.7},
    }).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    content = data.get("response", "")
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    content = re.sub(r"```(?:json)?\s*", "", content).strip()
    content = re.sub(r"```\s*$", "", content).strip()
    return content


def call_gemma4_local(prompt: str, model: str = "gemma4:latest") -> str:
    """Call Gemma 4 27B via local Ollama (OpenAI-compatible) at temperature 0.7."""
    from openai import OpenAI
    client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a brand research assistant. "
                    "Respond with ONLY valid JSON. "
                    "No markdown, no explanation -- just the JSON."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1024,
        temperature=0.7,
    )
    content = response.choices[0].message.content or ""
    content = re.sub(r"```(?:json)?\s*", "", content).strip()
    content = re.sub(r"```\s*$", "", content).strip()
    return content


API_CALLERS: dict[str, Any] = {
    "claude": call_claude,
    "gpt": call_gpt,
    "gemini": call_gemini,
    "deepseek": call_deepseek,
    "qwen": call_qwen,
    "qwen3_local": call_qwen3_local,
    "gemma4_local": call_gemma4_local,
}

API_KEY_VARS: dict[str, str] = {
    "claude": "ANTHROPIC_API_KEY",
    "gpt": "OPENAI_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "qwen": "DASHSCOPE_API_KEY",
    "qwen3_local": "OLLAMA_AVAILABLE",
    "gemma4_local": "OLLAMA_AVAILABLE",
}

MODEL_IDS: dict[str, str] = {
    "claude": "claude-haiku-4-5",
    "gpt": "gpt-4o-mini",
    "gemini": "gemini-2.5-flash",
    "deepseek": "deepseek-chat",
    "qwen": "qwen-plus-latest",
    "qwen3_local": "qwen3:30b",
    "gemma4_local": "gemma4:latest",
    "simulated": "simulated",
}


# ---------------------------------------------------------------------------
# JSONL Session Logging
# ---------------------------------------------------------------------------

def _ensure_log_dir(log_path: str) -> Path:
    """Ensure the session log directory exists and return the Path object."""
    p = Path(log_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def append_session_log(
    log_path: str,
    *,
    model: str,
    model_id: str,
    prompt_type: str,
    brand_pair: str,
    pair_id: str,
    dimension: Optional[str],
    brand: Optional[str],
    run: int,
    prompt: str,
    response: str,
    parsed: Optional[dict],
    latency_ms: int,
    tokens_in: Optional[int] = None,
    tokens_out: Optional[int] = None,
    error: Optional[str] = None,
) -> None:
    """Append a single JSONL entry to the session log (crash-safe: flush after each write)."""
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model": model,
        "model_id": model_id,
        "prompt_type": prompt_type,
        "brand_pair": brand_pair,
        "pair_id": pair_id,
        "dimension": dimension,
        "brand": brand,
        "run": run,
        "prompt": prompt,
        "response": response,
        "parsed": parsed,
        "latency_ms": latency_ms,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "error": error,
    }
    p = _ensure_log_dir(log_path)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, default=str) + "\n")
        f.flush()


# ---------------------------------------------------------------------------
# Retry / Rate Limiting
# ---------------------------------------------------------------------------

def call_with_retry(
    fn: Any,
    prompt: str,
    model_name: str,
    max_retries: int = 3,
    rate_limit_delay: float = 1.0,
    *,
    log_path: Optional[str] = None,
    log_context: Optional[dict] = None,
) -> str:
    """
    Call an LLM API function with exponential backoff retry and rate limiting.

    Delays: 2s, 4s, 8s on successive failures.
    Always waits rate_limit_delay seconds before returning to avoid burst limits.
    """
    delays = [2, 4, 8]
    last_exc: Exception = RuntimeError("No attempts made")

    for attempt in range(max_retries):
        t0 = time.monotonic()
        try:
            result = fn(prompt)
            latency_ms = int((time.monotonic() - t0) * 1000)
            time.sleep(rate_limit_delay)

            if log_path and log_context:
                parsed = None
                try:
                    parsed = parse_llm_json(result)
                except Exception:
                    pass
                append_session_log(
                    log_path,
                    model=model_name,
                    model_id=MODEL_IDS.get(model_name, "unknown"),
                    prompt_type=log_context.get("prompt_type", ""),
                    brand_pair=log_context.get("brand_pair", ""),
                    pair_id=log_context.get("pair_id", ""),
                    dimension=log_context.get("dimension"),
                    brand=log_context.get("brand"),
                    run=log_context.get("run", 0),
                    prompt=prompt,
                    response=result,
                    parsed=parsed,
                    latency_ms=latency_ms,
                )
            return result

        except Exception as exc:
            last_exc = exc
            latency_ms = int((time.monotonic() - t0) * 1000)
            if attempt < max_retries - 1:
                wait = delays[attempt]
                print(f"    [retry {attempt + 1}/{max_retries - 1}] {model_name} error: {exc} -- waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"    [failed] {model_name} after {max_retries} attempts: {exc}")
                if log_path and log_context:
                    append_session_log(
                        log_path,
                        model=model_name,
                        model_id=MODEL_IDS.get(model_name, "unknown"),
                        prompt_type=log_context.get("prompt_type", ""),
                        brand_pair=log_context.get("brand_pair", ""),
                        pair_id=log_context.get("pair_id", ""),
                        dimension=log_context.get("dimension"),
                        brand=log_context.get("brand"),
                        run=log_context.get("run", 0),
                        prompt=prompt,
                        response="",
                        parsed=None,
                        latency_ms=latency_ms,
                        error=str(exc),
                    )
    raise last_exc


# ---------------------------------------------------------------------------
# Reproducibility Metadata
# ---------------------------------------------------------------------------

def collect_experiment_metadata(models: list[str], start_time: str) -> dict:
    """Collect reproducibility metadata for the experiment."""
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        git_hash = "unknown"

    pkg_versions: dict[str, str] = {}
    for pkg in ["anthropic", "openai", "google-genai", "scipy", "numpy", "pyyaml"]:
        try:
            pkg_versions[pkg] = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            pkg_versions[pkg] = "not installed"

    api_key_hashes: dict[str, str] = {}
    for model_name, env_var in API_KEY_VARS.items():
        key = os.environ.get(env_var, "")
        if key and key != "1":
            api_key_hashes[model_name] = hashlib.sha256(key.encode()).hexdigest()[:8]

    model_configs: dict[str, dict] = {}
    for m in models:
        model_configs[m] = {
            "model_id": MODEL_IDS.get(m, "unknown"),
            "max_tokens": 512,
            "temperature": 0.7,
        }

    return {
        "script_version": git_hash,
        "python_version": sys.version,
        "package_versions": pkg_versions,
        "hardware": platform.machine(),
        "processor": platform.processor(),
        "os": platform.platform(),
        "start_time": start_time,
        "end_time": None,
        "model_configs": model_configs,
        "api_key_hash": api_key_hashes,
        "experiment": "R15-ai-search-metamerism",
        "temperature": 0.7,
        "dimensions": DIMENSIONS,
        "n_brand_pairs": len(BRAND_PAIRS),
        "prompts_per_pair": "1 recommendation + 1 differentiation + 8 probes x 2 brands = 18",
    }


# ---------------------------------------------------------------------------
# Statistical Analysis
# ---------------------------------------------------------------------------

def cohens_d(group1: list[float], group2: list[float]) -> float:
    """Cohen's d for comparing two group means."""
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return float("nan")
    m1, m2 = float(np.mean(group1)), float(np.mean(group2))
    var1, var2 = float(np.var(group1, ddof=1)), float(np.var(group2, ddof=1))
    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    pooled_sd = sqrt(max(pooled_var, 1e-12))
    return float((m1 - m2) / pooled_sd)


def fleiss_kappa(ratings_matrix: np.ndarray) -> float:
    """
    Fleiss' kappa for inter-rater reliability.

    ratings_matrix: shape (n_subjects, n_categories)
    Each row sums to the number of raters.
    """
    N, k = ratings_matrix.shape
    n = ratings_matrix[0].sum()
    if N == 0 or n <= 1:
        return float("nan")

    p_j = ratings_matrix.sum(axis=0) / (N * n)
    P_i = (np.sum(ratings_matrix ** 2, axis=1) - n) / (n * (n - 1))
    P_bar = float(np.mean(P_i))
    P_e = float(np.sum(p_j ** 2))

    if abs(1.0 - P_e) < 1e-12:
        return 1.0 if abs(P_bar - 1.0) < 1e-12 else float("nan")

    return float((P_bar - P_e) / (1.0 - P_e))


def compute_dimensional_citation_frequency(
    calls: list[dict],
) -> dict[str, dict[str, float]]:
    """
    Compute how often each dimension is cited per model in recommendation and
    differentiation prompts.

    Returns: {model: {dimension: citation_rate_0_to_1}}
    """
    # Filter to recommendation and differentiation only
    relevant = [c for c in calls if c.get("prompt_type") in {"recommendation", "differentiation"}]

    by_model: dict[str, dict[str, int]] = {}
    by_model_total: dict[str, int] = {}

    for call in relevant:
        model = call["model"]
        if model not in by_model:
            by_model[model] = {d: 0 for d in DIMENSIONS}
            by_model_total[model] = 0

        by_model_total[model] += 1

        # Use cited dims from parsed output or extract from response text
        parsed = call.get("parsed") or {}
        explicit = parsed.get("dimensions_cited") if isinstance(parsed.get("dimensions_cited"), list) else None
        response_text = call.get("response", "") + " " + str(parsed.get("key_differences", ""))
        cited = extract_cited_dimensions(response_text, explicit)

        for dim in cited:
            if dim in by_model[model]:
                by_model[model][dim] += 1

    # Normalize to rates
    result: dict[str, dict[str, float]] = {}
    for model, counts in by_model.items():
        total = by_model_total[model]
        result[model] = {d: counts[d] / max(total, 1) for d in DIMENSIONS}

    return result


def compute_dimensional_collapse_index(
    citation_freq: dict[str, dict[str, float]],
) -> dict[str, float]:
    """
    Compute the Dimensional Collapse Index (DCI) per model.

    DCI = (Economic_rate + Semiotic_rate) / sum(all_rates)

    DCI approaching 1.0 = near-total collapse to two dimensions.
    DCI at 0.25 = uniform citation across 8 dimensions (baseline).
    """
    dci: dict[str, float] = {}
    for model, freq in citation_freq.items():
        total = sum(freq.values())
        if total < 1e-9:
            dci[model] = float("nan")
            continue
        hard_mass = freq.get("economic", 0.0) + freq.get("semiotic", 0.0)
        dci[model] = hard_mass / total
    return dci


def compute_probe_scores(calls: list[dict]) -> dict[str, dict[str, dict[str, list[float]]]]:
    """
    Extract dimension probe scores per brand and model.

    Returns: {brand: {dimension: {model: [scores...]}}}
    """
    result: dict[str, dict[str, dict[str, list[float]]]] = {}

    probe_calls = [c for c in calls if c.get("prompt_type") == "dimension_probe"]
    for call in probe_calls:
        brand = call.get("brand") or ""
        dimension = call.get("dimension") or ""
        model = call.get("model") or ""
        parsed = call.get("parsed") or {}

        score = parsed.get("score")
        if score is None:
            continue
        try:
            score = float(score)
        except (TypeError, ValueError):
            continue

        if brand not in result:
            result[brand] = {}
        if dimension not in result[brand]:
            result[brand][dimension] = {}
        if model not in result[brand][dimension]:
            result[brand][dimension][model] = []
        result[brand][dimension][model].append(score)

    return result


def compute_cross_model_probe_variance(
    probe_scores: dict[str, dict[str, dict[str, list[float]]]],
) -> dict[str, dict[str, float]]:
    """
    Compute cross-model variance in probe scores per brand and dimension.

    Returns: {brand: {dimension: variance_across_models}}
    High variance on soft dims (cultural, temporal) vs low variance on hard dims
    (economic, semiotic) is the key hypothesis H3 prediction.
    """
    result: dict[str, dict[str, float]] = {}

    for brand, dims in probe_scores.items():
        result[brand] = {}
        for dim, model_scores in dims.items():
            # Compute mean score per model, then variance across models
            model_means = [float(np.mean(scores)) for scores in model_scores.values() if scores]
            if len(model_means) >= 2:
                result[brand][dim] = float(np.var(model_means, ddof=1))
            else:
                result[brand][dim] = float("nan")

    return result


def compute_cross_model_kappa(
    citation_freq: dict[str, dict[str, float]],
) -> float:
    """
    Compute Fleiss' kappa on binary dimension citation patterns across models.

    For each (model, dimension) combination, a "1" means the dimension was
    cited above the uniform baseline (1/8 = 0.125). This gives a matrix of
    shape (n_dimensions, 2_categories) for each model as a rater.
    """
    models = list(citation_freq.keys())
    if len(models) < 2:
        return float("nan")

    # Build ratings matrix: n_subjects = 8 dimensions, raters = models
    # Each cell = 1 if cited above baseline, 0 otherwise
    baseline = 1.0 / len(DIMENSIONS)
    n_subjects = len(DIMENSIONS)
    ratings = np.zeros((n_subjects, 2), dtype=int)  # (dimension, [below, above])

    for dim_idx, dim in enumerate(DIMENSIONS):
        for model in models:
            freq = citation_freq.get(model, {}).get(dim, 0.0)
            if freq >= baseline:
                ratings[dim_idx, 1] += 1
            else:
                ratings[dim_idx, 0] += 1

    return fleiss_kappa(ratings)


def run_statistical_tests(
    citation_freq: dict[str, dict[str, float]],
    probe_variance: dict[str, dict[str, float]],
    calls: list[dict],
) -> dict:
    """
    Run statistical tests for H1-H4.

    H1: Binomial test -- do Economic + Semiotic get cited more than uniform baseline?
    H2: Fleiss' kappa across models on citation patterns.
    H3: F-test on variance ratios (hard dims vs soft dims).
    H4: Cross-model convergence for soft-dim pairs vs hard-dim pairs.
    """
    from scipy import stats as scipy_stats

    stats_out: dict[str, Any] = {}

    # H1: Aggregate citation counts, binomial test vs uniform baseline (1/8 = 0.125)
    dim_totals: dict[str, int] = {d: 0 for d in DIMENSIONS}
    n_total_responses = 0
    for model_freq in citation_freq.values():
        n_responses = max(1, len([c for c in calls if c["model"] == list(citation_freq.keys())[0]
                                  and c.get("prompt_type") in {"recommendation", "differentiation"}]))
        for dim, rate in model_freq.items():
            # Approximate count from rate (since we don't store raw counts here)
            dim_totals[dim] += round(rate * n_responses)

    grand_total = sum(dim_totals.values())
    uniform_p = 1.0 / len(DIMENSIONS)
    econ_semio_count = dim_totals.get("economic", 0) + dim_totals.get("semiotic", 0)

    if grand_total > 0:
        h1_result = scipy_stats.binomtest(econ_semio_count, grand_total, 2 * uniform_p, alternative="greater")
        stats_out["h1_binomial_p"] = float(h1_result.pvalue)
        stats_out["h1_econ_semio_rate"] = econ_semio_count / grand_total
        stats_out["h1_uniform_baseline"] = 2 * uniform_p
        stats_out["h1_supported"] = h1_result.pvalue < 0.05
    else:
        stats_out["h1_binomial_p"] = float("nan")
        stats_out["h1_supported"] = None

    # H2: Fleiss' kappa across models
    kappa = compute_cross_model_kappa(citation_freq)
    stats_out["h2_fleiss_kappa"] = kappa
    stats_out["h2_supported"] = bool(kappa >= 0.40) if not np.isnan(kappa) else None

    # H3: F-test on cross-model probe variance (hard vs soft dims)
    hard_variances: list[float] = []
    soft_variances: list[float] = []
    for brand_vars in probe_variance.values():
        for dim, var in brand_vars.items():
            if not np.isnan(var):
                if dim in HARD_DIMS:
                    hard_variances.append(var)
                elif dim in SOFT_DIMS:
                    soft_variances.append(var)

    if len(hard_variances) >= 2 and len(soft_variances) >= 2:
        var_hard = float(np.var(hard_variances, ddof=1))
        var_soft = float(np.var(soft_variances, ddof=1))
        mean_hard = float(np.mean(hard_variances))
        mean_soft = float(np.mean(soft_variances))

        # F-test: is variance in soft dims higher than hard dims?
        if var_hard > 0:
            f_stat = var_soft / var_hard
            dfn = len(soft_variances) - 1
            dfd = len(hard_variances) - 1
            f_p = float(scipy_stats.f.sf(f_stat, dfn, dfd))
        else:
            f_stat = float("nan")
            f_p = float("nan")

        # Also t-test on mean cross-model variance (soft > hard)
        t_result = scipy_stats.ttest_ind(soft_variances, hard_variances, alternative="greater")

        stats_out["h3_mean_variance_hard_dims"] = mean_hard
        stats_out["h3_mean_variance_soft_dims"] = mean_soft
        stats_out["h3_f_stat"] = f_stat
        stats_out["h3_f_p"] = f_p
        stats_out["h3_ttest_p"] = float(t_result.pvalue)
        stats_out["h3_cohens_d"] = cohens_d(soft_variances, hard_variances)
        stats_out["h3_supported"] = bool(float(t_result.pvalue) < 0.05) if not np.isnan(float(t_result.pvalue)) else None
    else:
        stats_out["h3_supported"] = None

    # H4: Cross-model convergence by pair type (soft vs hard differentiator)
    # Recommendation prompts: do soft-dim pairs show less disagreement?
    rec_calls = [c for c in calls if c.get("prompt_type") == "recommendation"]
    soft_pair_ids = {p.id for p in BRAND_PAIRS if p.dim_type == "soft"}
    hard_pair_ids = {p.id for p in BRAND_PAIRS if p.dim_type == "hard"}

    soft_recs: dict[str, list[str]] = {}
    hard_recs: dict[str, list[str]] = {}

    for call in rec_calls:
        pair_id = call.get("pair_id", "")
        response = call.get("response", "").lower()
        pair = next((p for p in BRAND_PAIRS if p.id == pair_id), None)
        if not pair:
            continue
        brand_a = pair.brand_a.lower()
        brand_b = pair.brand_b.lower()

        # Determine which brand was recommended
        rec = "brand_a" if brand_a in response[:200] else ("brand_b" if brand_b in response[:200] else "unclear")

        key = (pair_id, call.get("run", 0))
        if pair_id in soft_pair_ids:
            soft_recs.setdefault(str(key), []).append(rec)
        elif pair_id in hard_pair_ids:
            hard_recs.setdefault(str(key), []).append(rec)

    # Compute recommendation agreement rate within each pair_type group
    def agreement_rate(group: dict[str, list[str]]) -> float:
        rates = []
        for recs in group.values():
            if len(recs) >= 2:
                mode_count = max([recs.count(r) for r in set(recs)])
                rates.append(mode_count / len(recs))
        return float(np.mean(rates)) if rates else float("nan")

    soft_agreement = agreement_rate(soft_recs)
    hard_agreement = agreement_rate(hard_recs)
    stats_out["h4_soft_pair_recommendation_agreement"] = soft_agreement
    stats_out["h4_hard_pair_recommendation_agreement"] = hard_agreement
    stats_out["h4_supported"] = bool(soft_agreement > hard_agreement) if (
        not np.isnan(soft_agreement) and not np.isnan(hard_agreement)
    ) else None

    # Per-dimension citation rates (aggregate across models)
    if citation_freq:
        n_models = len(citation_freq)
        agg_freq: dict[str, float] = {d: 0.0 for d in DIMENSIONS}
        for model_freq in citation_freq.values():
            for dim, rate in model_freq.items():
                agg_freq[dim] += rate / n_models
        stats_out["aggregate_citation_rates"] = {d: round(agg_freq[d], 4) for d in DIMENSIONS}
        stats_out["dim_totals"] = {d: dim_totals.get(d, 0) for d in DIMENSIONS}

    return stats_out


# ---------------------------------------------------------------------------
# Live Experiment Execution
# ---------------------------------------------------------------------------

def run_experiment_live(
    brand_pairs: list[BrandPair],
    models: list[str],
    runs: int,
    log_path: Optional[str] = None,
) -> list[ExperimentCall]:
    """
    Run all experiment calls: recommendation, differentiation, and dimension probes.

    Total calls = n_pairs x (1 rec + 1 diff + 8 probes x 2 brands) x runs x n_models
                = 10 x 18 x runs x n_models
    """
    all_calls: list[ExperimentCall] = []

    # Pre-compute total for progress display
    calls_per_pair = 1 + 1 + len(DIMENSIONS) * 2  # rec + diff + 8 probes x 2 brands
    total = len(brand_pairs) * calls_per_pair * runs * len(models)
    done = 0

    for run_idx in range(1, runs + 1):
        for pair in brand_pairs:
            pair_label = f"{pair.brand_a} vs {pair.brand_b}"

            # Build prompts for this pair
            rec_prompt = RECOMMENDATION_PROMPT.format(
                category=pair.category,
                brand_a=pair.brand_a,
                brand_b=pair.brand_b,
            )
            diff_prompt = DIFFERENTIATION_PROMPT.format(
                category=pair.category,
                brand_a=pair.brand_a,
                brand_b=pair.brand_b,
            )

            # Dimension probes for each brand
            probe_prompts: list[tuple[str, str, str]] = []  # (brand, dimension, prompt)
            for brand_name in [pair.brand_a, pair.brand_b]:
                for dim in DIMENSIONS:
                    probe_prompt = DIMENSION_PROBE_PROMPT.format(
                        brand=brand_name,
                        dimension_description=DIMENSION_DESCRIPTIONS[dim],
                        dimension=dim,
                    )
                    probe_prompts.append((brand_name, dim, probe_prompt))

            for model_name in models:
                caller = API_CALLERS[model_name]

                # --- Recommendation prompt ---
                done += 1
                print(
                    f"  [{done}/{total}] run={run_idx} model={model_name} "
                    f"type=recommendation pair={pair.id}"
                )
                log_ctx = {
                    "prompt_type": "recommendation",
                    "brand_pair": pair_label,
                    "pair_id": pair.id,
                    "dimension": None,
                    "brand": None,
                    "run": run_idx,
                }
                t0 = time.monotonic()
                try:
                    raw = call_with_retry(caller, rec_prompt, model_name, log_path=log_path, log_context=log_ctx)
                    latency_ms = int((time.monotonic() - t0) * 1000)
                    parsed = {}
                    cited = extract_cited_dimensions(raw)
                    parsed["dimensions_cited"] = cited
                    # Try to determine recommended brand
                    raw_lower = raw.lower()
                    if pair.brand_a.lower() in raw_lower[:300] and pair.brand_b.lower() not in raw_lower[:150]:
                        parsed["recommended_brand"] = pair.brand_a
                    elif pair.brand_b.lower() in raw_lower[:300] and pair.brand_a.lower() not in raw_lower[:150]:
                        parsed["recommended_brand"] = pair.brand_b
                    else:
                        parsed["recommended_brand"] = None
                    all_calls.append(ExperimentCall(
                        model=model_name,
                        brand_pair=pair_label,
                        pair_id=pair.id,
                        prompt_type="recommendation",
                        dimension=None,
                        brand=None,
                        run=run_idx,
                        response=raw,
                        parsed=parsed,
                        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        latency_ms=latency_ms,
                    ))
                except Exception as exc:
                    print(f"    [error] recommendation {model_name}: {exc}")
                    all_calls.append(ExperimentCall(
                        model=model_name,
                        brand_pair=pair_label,
                        pair_id=pair.id,
                        prompt_type="recommendation",
                        dimension=None,
                        brand=None,
                        run=run_idx,
                        response="",
                        parsed={},
                        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        latency_ms=0,
                        error=str(exc),
                    ))

                # --- Differentiation prompt ---
                done += 1
                print(
                    f"  [{done}/{total}] run={run_idx} model={model_name} "
                    f"type=differentiation pair={pair.id}"
                )
                log_ctx = {
                    "prompt_type": "differentiation",
                    "brand_pair": pair_label,
                    "pair_id": pair.id,
                    "dimension": None,
                    "brand": None,
                    "run": run_idx,
                }
                t0 = time.monotonic()
                try:
                    raw = call_with_retry(caller, diff_prompt, model_name, log_path=log_path, log_context=log_ctx)
                    latency_ms = int((time.monotonic() - t0) * 1000)
                    parsed = {}
                    try:
                        parsed = parse_llm_json(raw)
                    except Exception:
                        pass
                    # Augment cited dimensions from free text + explicit field
                    explicit = parsed.get("dimensions_cited") if isinstance(parsed.get("dimensions_cited"), list) else None
                    cited = extract_cited_dimensions(
                        raw + " " + str(parsed.get("key_differences", "")),
                        explicit,
                    )
                    parsed["dimensions_cited_extracted"] = cited
                    all_calls.append(ExperimentCall(
                        model=model_name,
                        brand_pair=pair_label,
                        pair_id=pair.id,
                        prompt_type="differentiation",
                        dimension=None,
                        brand=None,
                        run=run_idx,
                        response=raw,
                        parsed=parsed,
                        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        latency_ms=latency_ms,
                    ))
                except Exception as exc:
                    print(f"    [error] differentiation {model_name}: {exc}")
                    all_calls.append(ExperimentCall(
                        model=model_name,
                        brand_pair=pair_label,
                        pair_id=pair.id,
                        prompt_type="differentiation",
                        dimension=None,
                        brand=None,
                        run=run_idx,
                        response="",
                        parsed={},
                        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        latency_ms=0,
                        error=str(exc),
                    ))

                # --- Dimension probes ---
                for brand_name, dim, probe_prompt in probe_prompts:
                    done += 1
                    print(
                        f"  [{done}/{total}] run={run_idx} model={model_name} "
                        f"type=probe dim={dim} brand={brand_name}"
                    )
                    log_ctx = {
                        "prompt_type": "dimension_probe",
                        "brand_pair": pair_label,
                        "pair_id": pair.id,
                        "dimension": dim,
                        "brand": brand_name,
                        "run": run_idx,
                    }
                    t0 = time.monotonic()
                    try:
                        raw = call_with_retry(
                            caller, probe_prompt, model_name, log_path=log_path, log_context=log_ctx
                        )
                        latency_ms = int((time.monotonic() - t0) * 1000)
                        parsed = {}
                        try:
                            parsed = parse_llm_json(raw)
                        except Exception:
                            # Fallback: extract score by regex
                            score_m = re.search(r'\b([0-9](?:\.[0-9]+)?|10(?:\.0+)?)\b', raw)
                            if score_m:
                                parsed["score"] = float(score_m.group(1))
                        parsed.setdefault("dimension", dim)
                        parsed.setdefault("brand", brand_name)
                        all_calls.append(ExperimentCall(
                            model=model_name,
                            brand_pair=pair_label,
                            pair_id=pair.id,
                            prompt_type="dimension_probe",
                            dimension=dim,
                            brand=brand_name,
                            run=run_idx,
                            response=raw,
                            parsed=parsed,
                            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            latency_ms=latency_ms,
                        ))
                    except Exception as exc:
                        print(f"    [error] probe {dim} {brand_name} {model_name}: {exc}")
                        all_calls.append(ExperimentCall(
                            model=model_name,
                            brand_pair=pair_label,
                            pair_id=pair.id,
                            prompt_type="dimension_probe",
                            dimension=dim,
                            brand=brand_name,
                            run=run_idx,
                            response="",
                            parsed={},
                            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            latency_ms=0,
                            error=str(exc),
                        ))

    return all_calls


# ---------------------------------------------------------------------------
# Demo Mode (simulated responses)
# ---------------------------------------------------------------------------

def run_experiment_demo() -> list[ExperimentCall]:
    """
    Generate simulated experiment calls to demonstrate the data structure
    without requiring API keys.

    Simulated responses are designed to exhibit the predicted metamerism pattern:
    Economic and Semiotic over-cited, Cultural and Temporal under-cited.
    """
    import random
    random.seed(42)
    rng = random.Random(42)

    calls: list[ExperimentCall] = []
    demo_pairs = BRAND_PAIRS[:3]  # first 3 pairs for demo

    # Simulated citation bias: hard dims 3x more likely to be cited
    dim_weights = {
        "semiotic": 0.22,
        "economic": 0.20,
        "experiential": 0.16,
        "social": 0.13,
        "narrative": 0.11,
        "ideological": 0.08,
        "cultural": 0.06,
        "temporal": 0.04,
    }

    for pair in demo_pairs:
        pair_label = f"{pair.brand_a} vs {pair.brand_b}"

        for prompt_type in ["recommendation", "differentiation"]:
            # Sample cited dims according to skewed weights
            cited = [d for d, w in dim_weights.items() if rng.random() < w * 4]

            parsed: dict[str, Any] = {
                "dimensions_cited": cited,
                "recommended_brand": rng.choice([pair.brand_a, pair.brand_b]),
            }
            if prompt_type == "differentiation":
                parsed["differentiation_score"] = round(rng.uniform(0.3, 0.9), 2)
                parsed["key_differences"] = f"Simulated differences for {pair_label}"

            calls.append(ExperimentCall(
                model="simulated",
                brand_pair=pair_label,
                pair_id=pair.id,
                prompt_type=prompt_type,
                dimension=None,
                brand=None,
                run=1,
                response=f"[simulated {prompt_type} response for {pair_label}]",
                parsed=parsed,
                timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                latency_ms=0,
            ))

        # Dimension probes
        for brand_name in [pair.brand_a, pair.brand_b]:
            for dim in DIMENSIONS:
                # Hard dims get tighter cross-model scores, soft dims get more spread
                base_score = rng.uniform(5.0, 9.0)
                calls.append(ExperimentCall(
                    model="simulated",
                    brand_pair=pair_label,
                    pair_id=pair.id,
                    prompt_type="dimension_probe",
                    dimension=dim,
                    brand=brand_name,
                    run=1,
                    response=f"[simulated probe: {brand_name} {dim} = {base_score:.1f}]",
                    parsed={"dimension": dim, "brand": brand_name, "score": base_score, "reasoning": "Simulated."},
                    timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    latency_ms=0,
                ))

    return calls


# ---------------------------------------------------------------------------
# Summary Tables
# ---------------------------------------------------------------------------

def write_summary_tables(results: ExperimentResults, output_path: str) -> None:
    """Write formatted Markdown summary tables for the experiment."""
    lines: list[str] = []
    lines.append("# R15 AI Search Metamerism -- Summary Tables\n")

    meta = results.metadata or {}
    lines.append("## Table 0: Experiment Metadata\n")
    lines.append("| Parameter | Value |")
    lines.append("|-----------|-------|")
    lines.append(f"| Date | {str(meta.get('start_time', 'N/A'))[:10]} |")
    lines.append(f"| Models | {', '.join(results.models)} |")
    lines.append(f"| Runs per prompt | {results.runs} |")
    lines.append(f"| Brand pairs | {len(results.brand_pairs)} |")
    lines.append(f"| Total calls | {len(results.calls)} |")
    lines.append(f"| Temperature | {meta.get('temperature', 0.7)} |")
    lines.append(f"| Script version | {meta.get('script_version', 'N/A')} |")
    lines.append("")

    # Table 1: Dimensional citation frequency per model
    lines.append("## Table 1: Dimensional Citation Frequency (Recommendation + Differentiation Prompts)\n")
    dim_freq = results.dimensional_citation_freq
    if dim_freq:
        header = "| Dimension | " + " | ".join(results.models) + " | Aggregate |"
        sep = "|-----------|" + "|".join(["----------:" for _ in results.models]) + "|----------:|"
        lines.append(header)
        lines.append(sep)
        for dim in DIMENSIONS:
            model_rates = [f"{dim_freq.get(m, {}).get(dim, 0.0):.3f}" for m in results.models]
            agg = float(np.mean([dim_freq.get(m, {}).get(dim, 0.0) for m in results.models]))
            lines.append(f"| {dim} | " + " | ".join(model_rates) + f" | {agg:.3f} |")
        lines.append("")

    # Table 2: Dimensional Collapse Index per model
    lines.append("## Table 2: Dimensional Collapse Index (Economic + Semiotic / Total)\n")
    lines.append("Baseline (uniform): 2/8 = 0.250. Values above 0.250 indicate dimensional collapse.\n")
    lines.append("| Model | DCI | vs Baseline | Interpretation |")
    lines.append("|-------|-----|-------------|----------------|")
    dci = results.dimensional_collapse_index
    for model in results.models:
        val = dci.get(model, float("nan"))
        if not np.isnan(val):
            delta = val - 0.25
            direction = f"+{delta:.3f}" if delta >= 0 else f"{delta:.3f}"
            interp = "HIGH collapse" if val > 0.40 else ("Moderate" if val > 0.30 else "Near-uniform")
            lines.append(f"| {model} | {val:.3f} | {direction} | {interp} |")
        else:
            lines.append(f"| {model} | N/A | N/A | Insufficient data |")
    lines.append("")

    # Table 3: Dimension probe scores per brand (aggregate across models and runs)
    lines.append("## Table 3: Mean Dimension Probe Scores (0-10) by Brand\n")
    probe = results.probe_scores
    if probe:
        all_brands = sorted(probe.keys())
        for brand in all_brands:
            lines.append(f"### {brand}\n")
            lines.append("| Dimension | Type | " + " | ".join(results.models) + " | Mean | Cross-Model Var |")
            lines.append("|-----------|------|" + "|".join(["------:" for _ in results.models]) + "|------:|----------------:|")
            for dim in DIMENSIONS:
                dim_type = "hard" if dim in HARD_DIMS else "soft"
                model_means = []
                for m in results.models:
                    scores = probe.get(brand, {}).get(dim, {}).get(m, [])
                    if scores:
                        model_means.append(f"{float(np.mean(scores)):.1f}")
                    else:
                        model_means.append("--")
                numeric_means = [float(m) for m in model_means if m != "--"]
                mean_str = f"{float(np.mean(numeric_means)):.1f}" if numeric_means else "--"
                var_str = f"{float(np.var(numeric_means, ddof=1)):.2f}" if len(numeric_means) >= 2 else "--"
                lines.append(f"| {dim} | {dim_type} | " + " | ".join(model_means) + f" | {mean_str} | {var_str} |")
            lines.append("")

    # Table 4: Cross-model probe variance by dimension cluster
    lines.append("## Table 4: Cross-Model Probe Score Variance by Dimension Type\n")
    lines.append("Prediction (H3): soft-dimension variance > hard-dimension variance.\n")
    cross_var = results.cross_model_variance
    if cross_var:
        lines.append("| Brand | Hard Dim Mean Var | Soft Dim Mean Var | Hard < Soft? |")
        lines.append("|-------|------------------:|------------------:|:------------:|")
        for brand, dim_vars in sorted(cross_var.items()):
            hard_v = [v for d, v in dim_vars.items() if d in HARD_DIMS and not np.isnan(v)]
            soft_v = [v for d, v in dim_vars.items() if d in SOFT_DIMS and not np.isnan(v)]
            hv_str = f"{float(np.mean(hard_v)):.3f}" if hard_v else "--"
            sv_str = f"{float(np.mean(soft_v)):.3f}" if soft_v else "--"
            check = "Yes" if (hard_v and soft_v and float(np.mean(soft_v)) > float(np.mean(hard_v))) else "No"
            lines.append(f"| {brand} | {hv_str} | {sv_str} | {check} |")
        lines.append("")

    # Table 5: Statistical test results
    if results.statistics:
        s = results.statistics
        lines.append("## Table 5: Statistical Tests\n")
        lines.append("| Hypothesis | Test | Result | Supported? |")
        lines.append("|------------|------|--------|------------|")

        h1_p = s.get("h1_binomial_p", float("nan"))
        h1_rate = s.get("h1_econ_semio_rate", float("nan"))
        lines.append(
            f"| H1 (Economic+Semiotic over-weighting) | Binomial (p={h1_p:.4f}) | "
            f"Rate={h1_rate:.3f} vs baseline=0.250 | {'Yes *' if s.get('h1_supported') else 'No'} |"
        )

        kappa = s.get("h2_fleiss_kappa", float("nan"))
        lines.append(
            f"| H2 (Cross-model convergence) | Fleiss kappa={kappa:.3f} | "
            f"Threshold >= 0.40 | {'Yes *' if s.get('h2_supported') else 'No'} |"
        )

        h3_t = s.get("h3_ttest_p", float("nan"))
        h3_d = s.get("h3_cohens_d", float("nan"))
        lines.append(
            f"| H3 (Soft-dim higher variance) | t-test (p={h3_t:.4f}), d={h3_d:.3f} | "
            f"Mean var hard={s.get('h3_mean_variance_hard_dims', float('nan')):.3f}, "
            f"soft={s.get('h3_mean_variance_soft_dims', float('nan')):.3f} | "
            f"{'Yes *' if s.get('h3_supported') else 'No'} |"
        )

        h4_soft = s.get("h4_soft_pair_recommendation_agreement", float("nan"))
        h4_hard = s.get("h4_hard_pair_recommendation_agreement", float("nan"))
        lines.append(
            f"| H4 (Soft-dim pair convergence) | Agreement rates | "
            f"Soft={h4_soft:.3f}, Hard={h4_hard:.3f} | "
            f"{'Yes *' if s.get('h4_supported') else 'No'} |"
        )
        lines.append("")

        # Citation rate table
        agg_rates = s.get("aggregate_citation_rates", {})
        if agg_rates:
            lines.append("## Table 6: Aggregate Citation Rates by Dimension\n")
            lines.append("Uniform baseline = 0.125 (1/8). Values > baseline = over-cited.\n")
            lines.append("| Dimension | Type | Agg Rate | vs Baseline | Over-cited? |")
            lines.append("|-----------|------|:--------:|:-----------:|:-----------:|")
            for dim in DIMENSIONS:
                rate = agg_rates.get(dim, 0.0)
                delta = rate - 0.125
                over = "Yes" if delta > 0 else "No"
                dim_type = "hard" if dim in HARD_DIMS else "soft"
                lines.append(
                    f"| {dim} | {dim_type} | {rate:.3f} | "
                    f"{'+' if delta >= 0 else ''}{delta:.3f} | {over} |"
                )
            lines.append("")

    # Interpretation
    lines.append("---\n")
    lines.append("## Interpretation\n")
    lines.append(textwrap.dedent("""\
    If H1 is supported: LLMs systematically collapse multi-dimensional brand perception
    to Economic and Semiotic dimensions, producing spectral metamerism in AI-mediated search.

    If H2 is supported: This collapse is consistent across model families, indicating it
    is a property of text-based training corpora rather than any specific architecture.

    If H3 is supported: LLMs have differential dimensional sensitivity -- they measure
    Economic and Semiotic with high cross-model agreement but diverge on Cultural and
    Temporal dimensions, which are observer-dependent and perception-dense.

    If H4 is supported: Brands differentiated on "soft" dimensions (Narrative, Ideological,
    Cultural, Temporal) appear more similar through AI-mediated search than brands
    differentiated on "hard" dimensions -- a direct operational consequence of spectral
    metamerism.

    Theoretical implication: Brands that invest in soft-dimension differentiation face an
    AI search penalty. Their perception clouds are real but invisible to the AI mediator.
    """))

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"Summary tables saved to {output_path}")


# ---------------------------------------------------------------------------
# Main Orchestrator
# ---------------------------------------------------------------------------

def run_experiment(
    output_file: str = "results.json",
    summary_file: str = "summary_tables.md",
    demo: bool = True,
    runs: int = 3,
    log_path: Optional[str] = None,
) -> ExperimentResults:
    """
    Run the R15 AI Search Metamerism experiment.

    In demo mode: uses simulated responses to demonstrate methodology.
    In live mode: calls all available LLM APIs (skips missing API keys gracefully).
    """
    start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"\nR15 AI Search Metamerism Experiment")
    print(f"Mode: {'DEMO (simulated)' if demo else 'LIVE'}")
    print(f"Brand pairs: {len(BRAND_PAIRS)}")
    if not demo:
        print(f"Runs per prompt: {runs}")
        print(f"Temperature: 0.7 (variance measurement)\n")

    # Check Ollama availability
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2)
        os.environ["OLLAMA_AVAILABLE"] = "1"
        print("Ollama: available (local models enabled)")
    except Exception:
        print("Ollama: not reachable (local models will be skipped)")

    # Select models
    if demo:
        model_list = ["simulated"]
    else:
        model_list = []
        for model_name, env_var in API_KEY_VARS.items():
            if os.environ.get(env_var):
                model_list.append(model_name)
                print(f"  [available] {model_name} ({MODEL_IDS.get(model_name, '?')})")
            else:
                print(f"  [skip] {model_name}: {env_var} not set")
        if not model_list:
            print(
                "\nERROR: No API keys found. Set one or more of:\n"
                "  ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY,\n"
                "  DEEPSEEK_API_KEY, DASHSCOPE_API_KEY\n"
                "Or ensure Ollama is running at localhost:11434."
            )
            sys.exit(1)

    # Collect metadata
    metadata = collect_experiment_metadata(model_list, start_time)

    # Write pre-registration protocol and metadata (live mode only)
    if not demo and log_path:
        exp_dir = Path(log_path).parent
        exp_dir.mkdir(parents=True, exist_ok=True)
        pre_reg_path = exp_dir / "PRE_REGISTRATION.md"
        if not pre_reg_path.exists():
            pre_reg_path.write_text(PRE_REGISTRATION.strip() + "\n", encoding="utf-8")
            print(f"Pre-registration written to {pre_reg_path}")
        else:
            print(f"Pre-registration already exists at {pre_reg_path}")

        metadata_path = exp_dir / "metadata.yaml"
        metadata_path.write_text(
            yaml.dump(metadata, default_flow_style=False, sort_keys=False), encoding="utf-8"
        )
        print(f"Metadata written to {metadata_path}")

    # Execute experiment
    print(f"\nStarting experiment at {start_time}")
    if demo:
        raw_calls = run_experiment_demo()
    else:
        raw_calls = run_experiment_live(BRAND_PAIRS, model_list, runs, log_path=log_path)

    print(f"\nCompleted {len(raw_calls)} calls. Running analysis...")

    # Convert dataclasses to dicts for serialization and analysis
    calls_as_dicts = [asdict(c) for c in raw_calls]

    # Analysis
    citation_freq = compute_dimensional_citation_frequency(calls_as_dicts)
    dci = compute_dimensional_collapse_index(citation_freq)
    probe_scores = compute_probe_scores(calls_as_dicts)
    cross_var = compute_cross_model_probe_variance(probe_scores)

    stats = {}
    try:
        stats = run_statistical_tests(citation_freq, cross_var, calls_as_dicts)
    except Exception as exc:
        print(f"  [warn] Statistical tests failed: {exc}")

    # Record end time
    metadata["end_time"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    results = ExperimentResults(
        brand_pairs=[f"{p.brand_a} vs {p.brand_b}" for p in BRAND_PAIRS],
        models=model_list,
        runs=runs,
        calls=calls_as_dicts,
        dimensional_citation_freq=citation_freq,
        dimensional_collapse_index=dci,
        probe_scores=probe_scores,
        cross_model_variance=cross_var,
        statistics=stats,
        metadata=metadata,
    )

    # Serialize results
    Path(output_file).write_text(
        json.dumps(asdict(results), indent=2, default=str), encoding="utf-8"
    )
    print(f"Results saved to {output_file}")

    # Write summary tables
    write_summary_tables(results, summary_file)

    # Print brief console summary
    print("\n--- Summary ---")
    print(f"Models run: {', '.join(model_list)}")
    if citation_freq:
        print("\nDimensional Collapse Index (Economic+Semiotic / Total, baseline=0.250):")
        for m, val in dci.items():
            if not np.isnan(val):
                print(f"  {m}: {val:.3f} ({'above' if val > 0.25 else 'below'} baseline)")

    if stats:
        print(f"\nH1 (dimensional over-weighting): {'SUPPORTED' if stats.get('h1_supported') else 'NOT SUPPORTED'} "
              f"(p={stats.get('h1_binomial_p', float('nan')):.4f})")
        print(f"H2 (cross-model convergence):    kappa={stats.get('h2_fleiss_kappa', float('nan')):.3f} "
              f"({'SUPPORTED' if stats.get('h2_supported') else 'NOT SUPPORTED'})")
        print(f"H3 (soft-dim variance):          {'SUPPORTED' if stats.get('h3_supported') else 'NOT SUPPORTED'} "
              f"(t-test p={stats.get('h3_ttest_p', float('nan')):.4f})")
        print(f"H4 (soft-dim convergence):       {'SUPPORTED' if stats.get('h4_supported') else 'NOT SUPPORTED'}")

    print("\nDone.")
    return results


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="R15: AI Search Metamerism Experiment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
        Examples:
          python ai_search_metamerism.py --demo
          python ai_search_metamerism.py --live --runs 1
          python ai_search_metamerism.py --live --runs 3 --output results.json
        """),
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode with simulated responses (no API keys required)",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Run with real LLM APIs (requires at least one API key or Ollama)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of repetitions per prompt per model (default: 3; start with 1 for pilot)",
    )
    parser.add_argument(
        "--output",
        default="results.json",
        help="Output JSON file for full results (default: results.json)",
    )
    parser.add_argument(
        "--summary",
        default="summary_tables.md",
        help="Output Markdown file for summary tables (default: summary_tables.md)",
    )
    parser.add_argument(
        "--log",
        default=None,
        help="Path for JSONL session log (e.g. L3_sessions/session_log.jsonl)",
    )
    args = parser.parse_args()

    if args.live and args.demo:
        print("ERROR: --live and --demo are mutually exclusive.")
        sys.exit(1)

    if not args.live and not args.demo:
        # Default to demo if no mode specified
        args.demo = True
        print("No mode specified -- defaulting to --demo. Use --live for real API calls.")

    run_experiment(
        output_file=args.output,
        summary_file=args.summary,
        demo=args.demo,
        runs=args.runs,
        log_path=args.log,
    )


if __name__ == "__main__":
    main()
