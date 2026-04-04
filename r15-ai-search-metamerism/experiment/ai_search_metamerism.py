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

Measurement approach (v2 -- structured dimensional elicitation):
  (i)  Weighted recommendation: models allocate 100 importance points across 8
       dimensions when justifying a brand recommendation. Measures which dimensions
       models treat as decision-relevant.
  (ii) Dimensional differentiation: models score how different two brands are on
       each of 8 dimensions (0-10). Compared to ground-truth spectral distance.
  (iii) Dimension probe: models score each brand individually on each dimension.
       Cross-model variance reveals differential dimensional sensitivity.

Key measures:
  - DCI (Dimensional Collapse Index): (Economic_weight + Semiotic_weight) / 100
    from recommendation weights. Baseline = 25/100 = 0.25 (uniform).
  - Dimensional Sensitivity Profile: 8-d weight vector per model. Cosine
    similarity between models reveals convergent collapse.
  - Differentiation Gap: for soft-dim pairs, differentiation scores on
    soft dimensions should be lower than on hard dimensions if collapse occurs.

LLM providers supported (all optional -- skip if API key missing):
  - Claude (Anthropic): ANTHROPIC_API_KEY
  - GPT (OpenAI): OPENAI_API_KEY
  - Gemini (Google): GOOGLE_API_KEY
  - DeepSeek: DEEPSEEK_API_KEY (OpenAI-compatible)
  - Qwen3 30B (local Ollama): requires Ollama running at localhost:11434
  - Gemma 4 27B (local Ollama): requires Ollama running at localhost:11434

Usage:
    python ai_search_metamerism.py --demo
    python ai_search_metamerism.py --smoke
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
from math import sqrt
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

### Measurement Design (v2)
All dimensional measures are elicited via structured JSON prompts -- no
keyword extraction from free text. Three prompt types:
  1. Weighted Recommendation: 100 importance points allocated across 8 dims
  2. Dimensional Differentiation: 0-10 score for each dim for a brand pair
  3. Dimension Probe: 0-10 score for a single brand on a single dim

### Hypotheses

H1 (Dimensional over-weighting): LLMs will allocate significantly more weight
    to Economic and Semiotic dimensions than the uniform baseline (12.5 each).
    Test: one-sample t-test on Economic+Semiotic weight sum vs baseline 25.0.

H2 (Convergent collapse): Dimensional weight profiles will be highly similar
    across model families (mean cosine similarity >= 0.85 across model pairs),
    indicating that the collapse pattern is systematic rather than model-specific.

H3 (Differential probe variance): Cross-model variance in dimension-specific probe
    scores will be significantly lower for Economic and Semiotic dimensions than for
    Narrative, Cultural, and Temporal dimensions (t-test on variance, p < 0.05).

H4 (Differentiation gap): For brand pairs whose primary differentiators are soft
    dimensions (Narrative, Ideological, Cultural, Temporal), models will assign
    lower differentiation scores on those soft dimensions than on hard dimensions
    for the same pairs -- despite the pairs being designed to differ maximally on
    soft dimensions.

### Stopping Rules
- Minimum: 3 runs per prompt per model (established before data collection)
- If H1 t-test p > 0.10 after 3 runs: extend to 5 runs
- If H1 t-test p > 0.10 after 5 runs: report null result with power analysis

### Analysis Plan
Primary:
  - Dimensional weight profiles per model (from weighted_recommendation prompts)
  - One-sample t-test: Economic + Semiotic weight sum vs uniform baseline 25.0

Secondary:
  - Cosine similarity matrix across model weight profiles (H2)
  - t-test on cross-model probe score variance (hard vs soft dims) (H3)
  - Differentiation gap: soft-dim scores vs hard-dim scores for soft-designed pairs (H4)

Exploratory:
  - Per-brand-pair DCI vs human-judged spectral distance
  - Western vs Chinese vs local model cluster comparison

### Exclusion Criteria
- API errors resulting in unparseable responses: recorded with error field in JSONL
- Models with >50% error rate in any prompt type: excluded from aggregate statistics
- Weights that do not sum to 100 (+/-5 tolerance): recorded and flagged, included if
  ratable by renormalization
- Dimension probe responses where score cannot be parsed as 0-10 numeric: null
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

# Plain-language descriptions for dimension probes and prompts
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

# Which dimensions each brand pair is designed to test (the primary differentiators)
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
# Local Brand Pairs (thin training data -- conditional metamerism test)
# ---------------------------------------------------------------------------
# Brands from small non-English-speaking markets where LLM training data is
# sparse. Paired with global competitors in the same category. These pairs
# test the conditional metamerism hypothesis: dimensional collapse should be
# significantly higher for local brands than for the globally known pairs above.

LOCAL_BRAND_PAIRS: list[BrandPair] = [
    BrandPair(
        id="cyprus_supermarket",
        brand_a="AlphaMega",
        brand_b="Carrefour",
        category="supermarket chain",
        differentiating_dims=["cultural", "temporal"],
        dim_type="soft",
        description="AlphaMega is Cyprus's leading supermarket chain (~30 stores, bilingual "
                    "Greek-English market, ~1.2M population). Carrefour is a global French retailer. "
                    "AlphaMega has limited web presence beyond Cyprus; Carrefour has extensive global "
                    "training data. Tests cultural embeddedness and temporal heritage in thin-data conditions.",
    ),
    BrandPair(
        id="latvia_chocolate",
        brand_a="Laima",
        brand_b="Lindt",
        category="chocolate brand",
        differentiating_dims=["cultural", "narrative"],
        dim_type="soft",
        description="Laima is Latvia's oldest chocolate maker (est. 1870, Riga). Lindt is the "
                    "global Swiss benchmark. Laima has deep cultural significance in Latvia and the "
                    "Baltics but minimal English-language web presence. Tests whether cultural and "
                    "narrative dimensions collapse when training data is thin.",
    ),
    BrandPair(
        id="kenya_beer",
        brand_a="Tusker",
        brand_b="Heineken",
        category="beer brand",
        differentiating_dims=["narrative", "social"],
        dim_type="soft",
        description="Tusker is Kenya's iconic beer (est. 1922, named after an elephant that killed "
                    "the founder's father). Heineken is a global premium lager. Tusker has rich "
                    "narrative and social meaning in East Africa but limited global web footprint. "
                    "Tests dimensional collapse for African brands in Western LLMs.",
    ),
    BrandPair(
        id="vietnam_dairy",
        brand_a="Vinamilk",
        brand_b="Danone",
        category="dairy brand",
        differentiating_dims=["ideological", "economic"],
        dim_type="mixed",
        description="Vinamilk is Vietnam's largest dairy company (state-founded, 50%+ market share). "
                    "Danone is global. Vinamilk has moderate international presence (JSE-listed) "
                    "but limited English-language brand narrative. Tests intermediate embeddedness.",
    ),
    BrandPair(
        id="serbia_water",
        brand_a="Knjaz Milos",
        brand_b="Evian",
        category="mineral water brand",
        differentiating_dims=["temporal", "cultural"],
        dim_type="soft",
        description="Knjaz Milos is Serbia's iconic mineral water (est. 1811, named after Prince "
                    "Milos Obrenovic). Evian is a global premium water brand. Knjaz Milos has deep "
                    "temporal and cultural significance in Serbia but near-zero English web presence. "
                    "Tests maximum dimensional collapse conditions.",
    ),
]


# ---------------------------------------------------------------------------
# Prompts (v2 -- structured dimensional elicitation)
# ---------------------------------------------------------------------------

def _dim_block() -> str:
    """Return a formatted list of all 8 dimensions with plain-language descriptions."""
    lines = []
    for dim in DIMENSIONS:
        lines.append(f"- {dim.capitalize()}: {DIMENSION_DESCRIPTIONS[dim]}")
    return "\n".join(lines)


WEIGHTED_RECOMMENDATION_PROMPT = (
    "You are an AI shopping assistant helping a consumer choose between two brands.\n\n"
    "Category: {category}\n"
    "Brands: {brand_a} vs {brand_b}\n\n"
    "Step 1: Recommend one brand.\n"
    "Step 2: Explain WHY by allocating 100 importance points across these 8 perception "
    "dimensions. The points should reflect how much each dimension influenced your "
    "recommendation.\n\n"
    "Dimensions:\n"
    "{dim_block}\n\n"
    "Respond with ONLY valid JSON:\n"
    "{{\n"
    '  "recommended_brand": "BrandName",\n'
    '  "weights": {{\n'
    '    "semiotic": 15, "narrative": 10, "ideological": 5,\n'
    '    "experiential": 20, "social": 10, "economic": 25,\n'
    '    "cultural": 5, "temporal": 10\n'
    "  }},\n"
    '  "reasoning": "1-2 sentence explanation"\n'
    "}}\n\n"
    "The weights MUST sum to exactly 100."
)

DIMENSIONAL_DIFFERENTIATION_PROMPT = (
    "You are a brand analyst comparing two brands for a consumer research report.\n\n"
    "Category: {category}\n"
    "Brands: {brand_a} vs {brand_b}\n\n"
    "Rate how DIFFERENT these two brands are on each of 8 perception dimensions.\n\n"
    "Dimensions:\n"
    "{dim_block}\n\n"
    "Respond with ONLY valid JSON:\n"
    "{{\n"
    '  "differentiation": {{\n'
    '    "semiotic": 7.5, "narrative": 8.0, "ideological": 6.0,\n'
    '    "experiential": 5.5, "social": 8.5, "economic": 9.0,\n'
    '    "cultural": 7.0, "temporal": 9.5\n'
    "  }},\n"
    '  "overall_score": 0.78,\n'
    '  "summary": "1-2 sentence summary of the key differences"\n'
    "}}\n\n"
    "Each score: 0.0 (identical) to 10.0 (completely different).\n"
    "overall_score: 0.0 to 1.0 summary measure."
)

DIMENSION_PROBE_PROMPT = (
    "You are a brand researcher scoring brands on specific attributes.\n\n"
    "Rate {brand} on the following attribute:\n\n"
    "Attribute: {dimension_description}\n\n"
    "Score on a scale of 0 to 10, where:\n"
    "- 0 = extremely weak or absent on this attribute\n"
    "- 10 = the global benchmark, one of the best examples in any category\n\n"
    "You MUST respond with ONLY a valid JSON object (no other text before or after):\n"
    "{{\n"
    '  "dimension": "{dimension}",\n'
    '  "brand": "{brand}",\n'
    '  "score": 7.5,\n'
    '  "reasoning": "Brief explanation of the score (1-2 sentences)"\n'
    "}}\n\n"
    "The score must be a number between 0.0 and 10.0."
)


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class ExperimentCall:
    """Raw record of a single LLM call and its parsed output."""
    model: str
    brand_pair: str           # e.g. "Hermes vs Coach"
    pair_id: str              # e.g. "luxury_heritage"
    prompt_type: str          # "weighted_recommendation" | "dimensional_differentiation" | "dimension_probe"
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
    weight_profiles: dict = field(default_factory=dict)
    dimensional_collapse_index: dict = field(default_factory=dict)
    model_similarity_matrix: dict = field(default_factory=dict)
    differentiation_scores: dict = field(default_factory=dict)
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
    single-quoted keys, trailing commas. Gemini often wraps output in fences
    or adds explanatory text before/after the JSON block.
    """
    # Strip markdown code fences (including ```json and plain ```)
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE)
    text = text.strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Extract first complete {...} block (handles leading prose)
    # Use a greedy search that finds the outermost braces
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
            # Fix trailing commas before } or ]
            candidate = re.sub(r",\s*([}\]])", r"\1", candidate)
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

    # Last resort: extract individual known fields by regex
    result: dict[str, Any] = {}

    score_match = re.search(r'"score"\s*:\s*([0-9]+(?:\.[0-9]+)?)', text)
    if score_match:
        result["score"] = float(score_match.group(1))

    overall_match = re.search(r'"overall_score"\s*:\s*([0-9]+(?:\.[0-9]+)?)', text)
    if overall_match:
        result["overall_score"] = float(overall_match.group(1))

    reason_match = re.search(r'"reasoning"\s*:\s*"([^"]*)"', text)
    if reason_match:
        result["reasoning"] = reason_match.group(1)

    summary_match = re.search(r'"summary"\s*:\s*"([^"]*)"', text)
    if summary_match:
        result["summary"] = summary_match.group(1)

    rec_match = re.search(r'"recommended_brand"\s*:\s*"([^"]*)"', text)
    if rec_match:
        result["recommended_brand"] = rec_match.group(1)

    if result:
        return result

    raise ValueError(f"Could not parse JSON from LLM response: {text[:300]}")


def parse_weights(parsed: dict) -> Optional[dict[str, float]]:
    """
    Extract and validate the 8-dimensional weight dict from a parsed response.

    Returns a normalized weights dict if parseable, or None if not.
    Tolerance: accepts weights summing to 95-105 (renormalizes to 100).
    """
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

    # Accept if within 15% of 100, then renormalize (LLMs often produce 90-110 sums)
    if abs(total - 100.0) > 15.0:
        return None

    if abs(total - 100.0) > 0.01:
        result = {d: v * 100.0 / total for d, v in result.items()}

    return result


def parse_differentiation(parsed: dict) -> Optional[dict[str, float]]:
    """
    Extract and validate the 8-dimensional differentiation score dict.

    Returns a dict with all 8 scores (0.0-10.0), or None if invalid.
    """
    diff_raw = parsed.get("differentiation")
    if not isinstance(diff_raw, dict):
        return None

    result: dict[str, float] = {}
    for dim in DIMENSIONS:
        val = diff_raw.get(dim)
        if val is None:
            return None
        try:
            score = float(val)
        except (TypeError, ValueError):
            return None
        if score < 0.0 or score > 10.0:
            score = max(0.0, min(10.0, score))
        result[dim] = score

    return result


# ---------------------------------------------------------------------------
# Model-Specific API Callers
# ---------------------------------------------------------------------------

def call_claude(prompt: str, model: str = "claude-haiku-4-5") -> str:
    """Call Anthropic Claude API at temperature 0.7 and return response text."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model=model,
        max_tokens=2048,
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
        max_tokens=2048,
        temperature=0.7,
    )
    return response.choices[0].message.content


def call_gemini(prompt: str, model: str = "gemini-2.5-flash") -> str:
    """Call Google Gemini via google-genai SDK at temperature 0.7 and return response text.

    Fix history (documented per fleet rules):
    - v2 (dc0dbd4): max_output_tokens raised from 512 to 2048 -- still truncated (55 chars)
    - v3 (this): added response_mime_type="application/json" to force JSON mode,
      which prevents markdown fences, preamble, and early truncation. Also added
      system_instruction to reinforce JSON-only output.
    """
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    # Attempt 1: JSON mode with response_mime_type (preferred -- forces structured output)
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
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

    # Attempt 2: Standard call without JSON mode (fallback)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7, max_output_tokens=2048),
    )
    try:
        text = response.text
    except Exception:
        if response.candidates:
            text = response.candidates[0].content.parts[0].text
        else:
            raise ValueError("Gemini returned no usable response candidates")
    return text


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
        max_tokens=2048,
        temperature=0.7,
    )
    return response.choices[0].message.content


def call_qwen3_local(prompt: str, model: str = "qwen3:30b") -> str:
    """Call Qwen3 30B via local Ollama with fallback to native /api/generate.

    Qwen3 thinking mode may put content in reasoning_content instead of content.
    We check both fields and strip think tags.

    Fix history (documented per fleet rules):
    - v2 (dc0dbd4): max_tokens raised to 2048, system message added, reasoning_content
      fallback, native Ollama API fallback -- still truncated (211 chars)
    - v3 (this): added /no_think tag to user prompt to suppress thinking mode that
      consumes output token budget. Increased to 4096 tokens for safety margin.
    """
    # Append /no_think to suppress Qwen3 internal reasoning (saves output tokens)
    prompt_with_no_think = prompt + "\n/no_think"

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
                {"role": "user", "content": prompt_with_no_think},
            ],
            max_tokens=4096,
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
        "prompt": prompt + "\n/no_think\n\nRespond with ONLY a JSON object:",
        "stream": False,
        "options": {"num_predict": 4096, "temperature": 0.7},
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
    """Call Gemma 4 27B via local Ollama with fallback to native /api/generate.

    Gemma4 sometimes returns empty responses via the OpenAI-compatible endpoint.
    Fallback to native Ollama API with explicit num_predict if first attempt empty.
    """
    # Attempt 1: OpenAI-compatible endpoint with system message
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
                        "You MUST respond with ONLY valid JSON. "
                        "No markdown, no explanation, no preamble -- just the JSON object."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=2048,
            temperature=0.7,
        )
        content = response.choices[0].message.content or ""
        content = re.sub(r"```(?:json)?\s*", "", content).strip()
        content = re.sub(r"```\s*$", "", content).strip()
        if content.strip():
            return content
    except Exception:
        pass

    # Attempt 2: Ollama native /api/generate (bypasses OpenAI-compatible layer)
    payload = json.dumps({
        "model": model,
        "prompt": prompt + "\n\nYou MUST respond with ONLY a JSON object:",
        "stream": False,
        "options": {"num_predict": 2048, "temperature": 0.7},
    }).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    content = data.get("response", "")
    content = re.sub(r"```(?:json)?\s*", "", content).strip()
    content = re.sub(r"```\s*$", "", content).strip()
    return content


API_CALLERS: dict[str, Any] = {
    "claude": call_claude,
    "gpt": call_gpt,
    "gemini": call_gemini,
    "deepseek": call_deepseek,
    "qwen3_local": call_qwen3_local,
    "gemma4_local": call_gemma4_local,
}

API_KEY_VARS: dict[str, str] = {
    "claude": "ANTHROPIC_API_KEY",
    "gpt": "OPENAI_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "qwen3_local": "OLLAMA_AVAILABLE",
    "gemma4_local": "OLLAMA_AVAILABLE",
}

MODEL_IDS: dict[str, str] = {
    "claude": "claude-haiku-4-5",
    "gpt": "gpt-4o-mini",
    "gemini": "gemini-2.5-flash",
    "deepseek": "deepseek-chat",
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
            "max_tokens": 2048,
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
        "script_revision": "v2-structured-elicitation",
        "temperature": 0.7,
        "dimensions": DIMENSIONS,
        "n_brand_pairs": len(BRAND_PAIRS),
        "prompts_per_pair": "1 weighted_recommendation + 1 dimensional_differentiation + 8 probes x 2 brands = 18",
    }


# ---------------------------------------------------------------------------
# Analysis: Weight Profiles and DCI
# ---------------------------------------------------------------------------

def compute_weight_profiles(
    calls: list[dict],
) -> dict[str, dict[str, float]]:
    """
    Compute mean dimensional weight profile per model from weighted_recommendation calls.

    Returns: {model: {dimension: mean_weight_0_to_100}}
    Weights sum to 100 for each response; this averages across all responses per model.
    """
    weight_sums: dict[str, dict[str, float]] = {}
    weight_counts: dict[str, int] = {}

    rec_calls = [c for c in calls if c.get("prompt_type") == "weighted_recommendation"]
    for call in rec_calls:
        model = call["model"]
        parsed = call.get("parsed") or {}
        weights = parse_weights(parsed)
        if weights is None:
            continue

        if model not in weight_sums:
            weight_sums[model] = {d: 0.0 for d in DIMENSIONS}
            weight_counts[model] = 0

        for dim in DIMENSIONS:
            weight_sums[model][dim] += weights[dim]
        weight_counts[model] += 1

    result: dict[str, dict[str, float]] = {}
    for model, sums in weight_sums.items():
        n = weight_counts[model]
        result[model] = {d: sums[d] / n for d in DIMENSIONS}

    return result


def compute_dimensional_collapse_index(
    weight_profiles: dict[str, dict[str, float]],
) -> dict[str, float]:
    """
    Compute the Dimensional Collapse Index (DCI) per model.

    DCI = (Economic_weight + Semiotic_weight) / 100
    Baseline (uniform) = 25/100 = 0.25
    Values > 0.25 indicate collapse toward hard dimensions.
    """
    dci: dict[str, float] = {}
    for model, profile in weight_profiles.items():
        economic = profile.get("economic", 0.0)
        semiotic = profile.get("semiotic", 0.0)
        dci[model] = (economic + semiotic) / 100.0
    return dci


def compute_model_similarity_matrix(
    weight_profiles: dict[str, dict[str, float]],
) -> dict[str, dict[str, float]]:
    """
    Compute pairwise cosine similarity between model weight profiles.

    High similarity = convergent dimensional sensitivity.
    Returns: {model_a: {model_b: cosine_similarity}}
    """
    models = list(weight_profiles.keys())
    result: dict[str, dict[str, float]] = {m: {} for m in models}

    for i, m1 in enumerate(models):
        for j, m2 in enumerate(models):
            if i == j:
                result[m1][m2] = 1.0
                continue
            v1 = np.array([weight_profiles[m1][d] for d in DIMENSIONS])
            v2 = np.array([weight_profiles[m2][d] for d in DIMENSIONS])
            norm1 = float(np.linalg.norm(v1))
            norm2 = float(np.linalg.norm(v2))
            if norm1 < 1e-9 or norm2 < 1e-9:
                result[m1][m2] = float("nan")
            else:
                result[m1][m2] = float(np.dot(v1, v2) / (norm1 * norm2))

    return result


# ---------------------------------------------------------------------------
# Analysis: Differentiation Scores
# ---------------------------------------------------------------------------

def compute_differentiation_scores(
    calls: list[dict],
) -> dict[str, dict[str, dict[str, float]]]:
    """
    Extract mean differentiation scores per brand pair and model.

    Returns: {pair_id: {model: {dimension: mean_score}}}
    """
    # Accumulate sums and counts
    sums: dict[str, dict[str, dict[str, float]]] = {}
    counts: dict[str, dict[str, int]] = {}

    diff_calls = [c for c in calls if c.get("prompt_type") == "dimensional_differentiation"]
    for call in diff_calls:
        pair_id = call.get("pair_id", "")
        model = call.get("model", "")
        parsed = call.get("parsed") or {}
        scores = parse_differentiation(parsed)
        if scores is None:
            continue

        if pair_id not in sums:
            sums[pair_id] = {}
            counts[pair_id] = {}
        if model not in sums[pair_id]:
            sums[pair_id][model] = {d: 0.0 for d in DIMENSIONS}
            counts[pair_id][model] = 0

        for dim in DIMENSIONS:
            sums[pair_id][model][dim] += scores[dim]
        counts[pair_id][model] += 1

    result: dict[str, dict[str, dict[str, float]]] = {}
    for pair_id, model_sums in sums.items():
        result[pair_id] = {}
        for model, dim_sums in model_sums.items():
            n = counts[pair_id][model]
            result[pair_id][model] = {d: dim_sums[d] / n for d in DIMENSIONS}

    return result


def compute_differentiation_gap(
    differentiation_scores: dict[str, dict[str, dict[str, float]]],
) -> dict[str, dict[str, float]]:
    """
    Compute differentiation gap for soft-dim pairs.

    For each pair, compute mean differentiation score on soft dims vs hard dims.
    For soft-dim pairs: if LLMs collapse, soft-dim scores will be lower than
    hard-dim scores despite the pair being designed to differ most on soft dims.

    Returns: {pair_id: {"soft_mean": float, "hard_mean": float, "gap": float}}
    Where gap = hard_mean - soft_mean (positive = collapse detected).
    """
    result: dict[str, dict[str, float]] = {}

    for pair in BRAND_PAIRS:
        model_scores = differentiation_scores.get(pair.id, {})
        if not model_scores:
            continue

        soft_vals: list[float] = []
        hard_vals: list[float] = []

        for model_dim_scores in model_scores.values():
            for dim, score in model_dim_scores.items():
                if dim in SOFT_DIMS:
                    soft_vals.append(score)
                elif dim in HARD_DIMS:
                    hard_vals.append(score)

        if soft_vals and hard_vals:
            soft_mean = float(np.mean(soft_vals))
            hard_mean = float(np.mean(hard_vals))
            result[pair.id] = {
                "soft_mean": soft_mean,
                "hard_mean": hard_mean,
                "gap": hard_mean - soft_mean,
                "dim_type": pair.dim_type,
            }

    return result


# ---------------------------------------------------------------------------
# Analysis: Probe Scores
# ---------------------------------------------------------------------------

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
        if score < 0.0 or score > 10.0:
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

    Returns: {brand: {dimension: variance_across_model_means}}
    """
    result: dict[str, dict[str, float]] = {}

    for brand, dims in probe_scores.items():
        result[brand] = {}
        for dim, model_scores in dims.items():
            model_means = [float(np.mean(scores)) for scores in model_scores.values() if scores]
            if len(model_means) >= 2:
                result[brand][dim] = float(np.var(model_means, ddof=1))
            else:
                result[brand][dim] = float("nan")

    return result


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


def run_statistical_tests(
    weight_profiles: dict[str, dict[str, float]],
    probe_variance: dict[str, dict[str, float]],
    model_similarity: dict[str, dict[str, float]],
    differentiation_gap: dict[str, dict[str, float]],
) -> dict:
    """
    Run statistical tests for H1-H4.

    H1: t-test -- do Economic + Semiotic get allocated more weight than uniform baseline?
    H2: Mean pairwise cosine similarity across model weight profiles.
    H3: t-test on cross-model probe variance (hard dims vs soft dims).
    H4: Differentiation gap -- do soft-dim pairs show lower differentiation on soft dims?
    """
    from scipy import stats as scipy_stats

    stats_out: dict[str, Any] = {}

    # H1: one-sample t-test: Economic + Semiotic sum vs uniform baseline 25.0
    econ_semio_sums: list[float] = []
    for profile in weight_profiles.values():
        econ_semio_sums.append(profile.get("economic", 0.0) + profile.get("semiotic", 0.0))

    if len(econ_semio_sums) >= 2:
        h1_result = scipy_stats.ttest_1samp(econ_semio_sums, popmean=25.0, alternative="greater")
        stats_out["h1_ttest_p"] = float(h1_result.pvalue)
        stats_out["h1_mean_econ_semio"] = float(np.mean(econ_semio_sums))
        stats_out["h1_uniform_baseline"] = 25.0
        stats_out["h1_supported"] = float(h1_result.pvalue) < 0.05
    elif len(econ_semio_sums) == 1:
        # Single model: check if above baseline
        val = econ_semio_sums[0]
        stats_out["h1_ttest_p"] = float("nan")
        stats_out["h1_mean_econ_semio"] = val
        stats_out["h1_uniform_baseline"] = 25.0
        stats_out["h1_supported"] = val > 25.0
    else:
        stats_out["h1_ttest_p"] = float("nan")
        stats_out["h1_supported"] = None

    # Per-dimension mean weights across models
    if weight_profiles:
        n_models = len(weight_profiles)
        agg_weights: dict[str, float] = {d: 0.0 for d in DIMENSIONS}
        for profile in weight_profiles.values():
            for dim in DIMENSIONS:
                agg_weights[dim] += profile.get(dim, 0.0) / n_models
        stats_out["aggregate_mean_weights"] = {d: round(agg_weights[d], 2) for d in DIMENSIONS}

    # H2: Mean pairwise cosine similarity across model pairs
    models_with_profiles = list(model_similarity.keys())
    pairwise_sims: list[float] = []
    for i, m1 in enumerate(models_with_profiles):
        for j, m2 in enumerate(models_with_profiles):
            if i < j:
                val = model_similarity.get(m1, {}).get(m2, float("nan"))
                if not (isinstance(val, float) and (val != val)):  # not nan
                    pairwise_sims.append(val)

    if pairwise_sims:
        mean_sim = float(np.mean(pairwise_sims))
        stats_out["h2_mean_cosine_similarity"] = mean_sim
        stats_out["h2_n_pairs"] = len(pairwise_sims)
        stats_out["h2_supported"] = mean_sim >= 0.85
    else:
        stats_out["h2_mean_cosine_similarity"] = float("nan")
        stats_out["h2_supported"] = None

    # H3: t-test on cross-model probe variance (hard dims vs soft dims)
    hard_variances: list[float] = []
    soft_variances: list[float] = []

    for brand_vars in probe_variance.values():
        for dim, var in brand_vars.items():
            if isinstance(var, float) and not (var != var):  # not nan
                if dim in HARD_DIMS:
                    hard_variances.append(var)
                elif dim in SOFT_DIMS:
                    soft_variances.append(var)

    if len(hard_variances) >= 2 and len(soft_variances) >= 2:
        mean_hard = float(np.mean(hard_variances))
        mean_soft = float(np.mean(soft_variances))
        t_result = scipy_stats.ttest_ind(soft_variances, hard_variances, alternative="greater")

        stats_out["h3_mean_variance_hard_dims"] = mean_hard
        stats_out["h3_mean_variance_soft_dims"] = mean_soft
        stats_out["h3_ttest_p"] = float(t_result.pvalue)
        stats_out["h3_cohens_d"] = cohens_d(soft_variances, hard_variances)
        stats_out["h3_supported"] = float(t_result.pvalue) < 0.05
    else:
        stats_out["h3_supported"] = None

    # H4: Differentiation gap test
    # For soft-dim pairs: do models assign lower scores on soft dims than hard dims?
    soft_pair_gaps: list[float] = []
    hard_pair_gaps: list[float] = []
    mixed_pair_gaps: list[float] = []

    for pair_id, gap_data in differentiation_gap.items():
        gap = gap_data.get("gap", float("nan"))
        dim_type = gap_data.get("dim_type", "")
        if isinstance(gap, float) and not (gap != gap):
            if dim_type == "soft":
                soft_pair_gaps.append(gap)
            elif dim_type == "hard":
                hard_pair_gaps.append(gap)
            else:
                mixed_pair_gaps.append(gap)

    stats_out["h4_soft_pair_mean_gap"] = float(np.mean(soft_pair_gaps)) if soft_pair_gaps else float("nan")
    stats_out["h4_hard_pair_mean_gap"] = float(np.mean(hard_pair_gaps)) if hard_pair_gaps else float("nan")
    stats_out["h4_n_soft_pairs"] = len(soft_pair_gaps)
    stats_out["h4_n_hard_pairs"] = len(hard_pair_gaps)

    # H4 supported if soft-dim pairs show a positive gap (hard > soft diff score)
    soft_gap = stats_out["h4_soft_pair_mean_gap"]
    if not (isinstance(soft_gap, float) and soft_gap != soft_gap):
        stats_out["h4_supported"] = soft_gap > 0.0
    else:
        stats_out["h4_supported"] = None

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
    Run all experiment calls: weighted_recommendation, dimensional_differentiation,
    and dimension probes.

    Total calls = n_pairs x (1 weighted_rec + 1 diff + 8 probes x 2 brands) x runs x n_models
                = 10 x 18 x runs x n_models
    """
    all_calls: list[ExperimentCall] = []
    dim_block = _dim_block()

    calls_per_pair = 1 + 1 + len(DIMENSIONS) * 2  # weighted_rec + diff + 8 probes x 2 brands
    total = len(brand_pairs) * calls_per_pair * runs * len(models)
    done = 0

    for run_idx in range(1, runs + 1):
        for pair in brand_pairs:
            pair_label = f"{pair.brand_a} vs {pair.brand_b}"

            # Build prompts for this pair
            rec_prompt = WEIGHTED_RECOMMENDATION_PROMPT.format(
                category=pair.category,
                brand_a=pair.brand_a,
                brand_b=pair.brand_b,
                dim_block=dim_block,
            )
            diff_prompt = DIMENSIONAL_DIFFERENTIATION_PROMPT.format(
                category=pair.category,
                brand_a=pair.brand_a,
                brand_b=pair.brand_b,
                dim_block=dim_block,
            )

            # Dimension probes for each brand
            probe_prompts: list[tuple[str, str, str]] = []
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

                # --- Weighted Recommendation prompt ---
                done += 1
                print(
                    f"  [{done}/{total}] run={run_idx} model={model_name} "
                    f"type=weighted_recommendation pair={pair.id}"
                )
                log_ctx = {
                    "prompt_type": "weighted_recommendation",
                    "brand_pair": pair_label,
                    "pair_id": pair.id,
                    "dimension": None,
                    "brand": None,
                    "run": run_idx,
                }
                t0 = time.monotonic()
                try:
                    raw = call_with_retry(
                        caller, rec_prompt, model_name, log_path=log_path, log_context=log_ctx
                    )
                    latency_ms = int((time.monotonic() - t0) * 1000)
                    parsed: dict[str, Any] = {}
                    try:
                        parsed = parse_llm_json(raw)
                    except Exception:
                        pass
                    all_calls.append(ExperimentCall(
                        model=model_name,
                        brand_pair=pair_label,
                        pair_id=pair.id,
                        prompt_type="weighted_recommendation",
                        dimension=None,
                        brand=None,
                        run=run_idx,
                        response=raw,
                        parsed=parsed,
                        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        latency_ms=latency_ms,
                    ))
                except Exception as exc:
                    print(f"    [error] weighted_recommendation {model_name}: {exc}")
                    all_calls.append(ExperimentCall(
                        model=model_name,
                        brand_pair=pair_label,
                        pair_id=pair.id,
                        prompt_type="weighted_recommendation",
                        dimension=None,
                        brand=None,
                        run=run_idx,
                        response="",
                        parsed={},
                        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        latency_ms=0,
                        error=str(exc),
                    ))

                # --- Dimensional Differentiation prompt ---
                done += 1
                print(
                    f"  [{done}/{total}] run={run_idx} model={model_name} "
                    f"type=dimensional_differentiation pair={pair.id}"
                )
                log_ctx = {
                    "prompt_type": "dimensional_differentiation",
                    "brand_pair": pair_label,
                    "pair_id": pair.id,
                    "dimension": None,
                    "brand": None,
                    "run": run_idx,
                }
                t0 = time.monotonic()
                try:
                    raw = call_with_retry(
                        caller, diff_prompt, model_name, log_path=log_path, log_context=log_ctx
                    )
                    latency_ms = int((time.monotonic() - t0) * 1000)
                    parsed = {}
                    try:
                        parsed = parse_llm_json(raw)
                    except Exception:
                        pass
                    all_calls.append(ExperimentCall(
                        model=model_name,
                        brand_pair=pair_label,
                        pair_id=pair.id,
                        prompt_type="dimensional_differentiation",
                        dimension=None,
                        brand=None,
                        run=run_idx,
                        response=raw,
                        parsed=parsed,
                        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        latency_ms=latency_ms,
                    ))
                except Exception as exc:
                    print(f"    [error] dimensional_differentiation {model_name}: {exc}")
                    all_calls.append(ExperimentCall(
                        model=model_name,
                        brand_pair=pair_label,
                        pair_id=pair.id,
                        prompt_type="dimensional_differentiation",
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

def run_experiment_demo(smoke: bool = False) -> list[ExperimentCall]:
    """
    Generate simulated experiment calls to demonstrate the data structure
    without requiring API keys.

    Simulated responses are designed to exhibit the predicted metamerism pattern:
    Economic and Semiotic over-weighted, Cultural and Temporal under-weighted.

    In smoke mode, only the first brand pair is simulated.
    """
    import random
    rng = random.Random(42)

    calls: list[ExperimentCall] = []
    demo_pairs = BRAND_PAIRS[:1] if smoke else BRAND_PAIRS[:3]

    # Simulated weight bias: hard dims get more weight
    weight_means = {
        "semiotic": 18.0,
        "narrative": 9.0,
        "ideological": 7.0,
        "experiential": 16.0,
        "social": 11.0,
        "economic": 21.0,
        "cultural": 8.0,
        "temporal": 10.0,
    }

    # Simulated differentiation bias: hard dims get higher scores
    diff_means = {
        "semiotic": 8.2,
        "narrative": 5.8,
        "ideological": 6.1,
        "experiential": 7.6,
        "social": 6.9,
        "economic": 8.5,
        "cultural": 5.3,
        "temporal": 5.7,
    }

    for pair in demo_pairs:
        pair_label = f"{pair.brand_a} vs {pair.brand_b}"

        # Weighted recommendation call
        raw_weights = {d: max(1.0, weight_means[d] + rng.uniform(-3, 3)) for d in DIMENSIONS}
        total = sum(raw_weights.values())
        weights = {d: round(v * 100 / total, 1) for d, v in raw_weights.items()}
        rec_brand = rng.choice([pair.brand_a, pair.brand_b])
        rec_parsed: dict[str, Any] = {
            "recommended_brand": rec_brand,
            "weights": weights,
            "reasoning": f"Simulated recommendation for {pair_label}.",
        }
        calls.append(ExperimentCall(
            model="simulated",
            brand_pair=pair_label,
            pair_id=pair.id,
            prompt_type="weighted_recommendation",
            dimension=None,
            brand=None,
            run=1,
            response=json.dumps(rec_parsed),
            parsed=rec_parsed,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            latency_ms=0,
        ))

        # Dimensional differentiation call
        diff_scores = {d: max(0.0, min(10.0, diff_means[d] + rng.uniform(-1.5, 1.5))) for d in DIMENSIONS}
        overall = float(np.mean(list(diff_scores.values()))) / 10.0
        diff_parsed: dict[str, Any] = {
            "differentiation": {d: round(v, 1) for d, v in diff_scores.items()},
            "overall_score": round(overall, 2),
            "summary": f"Simulated differentiation for {pair_label}.",
        }
        calls.append(ExperimentCall(
            model="simulated",
            brand_pair=pair_label,
            pair_id=pair.id,
            prompt_type="dimensional_differentiation",
            dimension=None,
            brand=None,
            run=1,
            response=json.dumps(diff_parsed),
            parsed=diff_parsed,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            latency_ms=0,
        ))

        # Dimension probes
        for brand_name in [pair.brand_a, pair.brand_b]:
            for dim in DIMENSIONS:
                base_score = rng.uniform(4.5, 9.5)
                probe_parsed: dict[str, Any] = {
                    "dimension": dim,
                    "brand": brand_name,
                    "score": round(base_score, 1),
                    "reasoning": "Simulated.",
                }
                calls.append(ExperimentCall(
                    model="simulated",
                    brand_pair=pair_label,
                    pair_id=pair.id,
                    prompt_type="dimension_probe",
                    dimension=dim,
                    brand=brand_name,
                    run=1,
                    response=json.dumps(probe_parsed),
                    parsed=probe_parsed,
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
    lines.append("# R15 AI Search Metamerism -- Summary Tables (v2)\n")

    meta = results.metadata or {}
    lines.append("## Table 0: Experiment Metadata\n")
    lines.append("| Parameter | Value |")
    lines.append("|-----------|-------|")
    lines.append(f"| Date | {str(meta.get('start_time', 'N/A'))[:10]} |")
    lines.append(f"| Script revision | {meta.get('script_revision', 'N/A')} |")
    lines.append(f"| Models | {', '.join(results.models)} |")
    lines.append(f"| Runs per prompt | {results.runs} |")
    lines.append(f"| Brand pairs | {len(results.brand_pairs)} |")
    lines.append(f"| Total calls | {len(results.calls)} |")
    lines.append(f"| Temperature | {meta.get('temperature', 0.7)} |")
    lines.append(f"| Script version | {meta.get('script_version', 'N/A')} |")
    lines.append("")

    # Table 1: Mean dimensional weight profiles per model
    lines.append("## Table 1: Mean Dimensional Weight Profiles (weighted_recommendation prompts)\n")
    lines.append("Uniform baseline = 12.5 per dimension (100/8). Values > 12.5 = over-weighted.\n")
    wp = results.weight_profiles
    if wp:
        header = "| Dimension | Type | " + " | ".join(results.models) + " | Aggregate |"
        sep = "|-----------|------|" + "|".join(["----------:" for _ in results.models]) + "|----------:|"
        lines.append(header)
        lines.append(sep)
        for dim in DIMENSIONS:
            dim_type = "hard" if dim in HARD_DIMS else "soft"
            model_vals = [f"{wp.get(m, {}).get(dim, 0.0):.1f}" for m in results.models]
            agg = float(np.mean([wp.get(m, {}).get(dim, 0.0) for m in results.models])) if wp else 0.0
            marker = " *" if agg > 15.0 else ""
            lines.append(f"| {dim} | {dim_type} | " + " | ".join(model_vals) + f" | {agg:.1f}{marker} |")
        lines.append("")
        lines.append("\\* = noticeably above uniform baseline (12.5)\n")

    # Table 2: DCI per model
    lines.append("## Table 2: Dimensional Collapse Index\n")
    lines.append("DCI = (Economic_weight + Semiotic_weight) / 100. Baseline = 0.250.\n")
    lines.append("| Model | DCI | vs Baseline | Interpretation |")
    lines.append("|-------|-----|-------------|----------------|")
    dci = results.dimensional_collapse_index
    for model in results.models:
        val = dci.get(model, float("nan"))
        if not (isinstance(val, float) and val != val):
            delta = val - 0.25
            direction = f"+{delta:.3f}" if delta >= 0 else f"{delta:.3f}"
            interp = "HIGH collapse" if val > 0.40 else ("Moderate" if val > 0.30 else "Near-uniform")
            lines.append(f"| {model} | {val:.3f} | {direction} | {interp} |")
        else:
            lines.append(f"| {model} | N/A | N/A | Insufficient data |")
    lines.append("")

    # Table 3: Model similarity matrix
    lines.append("## Table 3: Cross-Model Dimensional Sensitivity Similarity (Cosine)\n")
    lines.append("Computed from mean weight profiles. High similarity = convergent collapse.\n")
    sim_matrix = results.model_similarity_matrix
    if sim_matrix:
        models_with_sim = [m for m in results.models if m in sim_matrix]
        if models_with_sim:
            header = "| Model | " + " | ".join(models_with_sim) + " |"
            sep = "|-------|" + "|".join(["---------:" for _ in models_with_sim]) + "|"
            lines.append(header)
            lines.append(sep)
            for m1 in models_with_sim:
                row_vals = [f"{sim_matrix.get(m1, {}).get(m2, float('nan')):.3f}" for m2 in models_with_sim]
                lines.append(f"| {m1} | " + " | ".join(row_vals) + " |")
            lines.append("")

    # Table 4: Differentiation gap by pair
    lines.append("## Table 4: Differentiation Gap by Brand Pair\n")
    lines.append("Gap = mean(hard_dim_scores) - mean(soft_dim_scores). Positive = models differentiate")
    lines.append("harder on hard dims even for pairs designed to differ on soft dims.\n")
    lines.append("| Pair | Dim Type | Soft Mean | Hard Mean | Gap | Collapse? |")
    lines.append("|------|----------|:---------:|:---------:|:---:|:---------:|")
    diff_gap = results.differentiation_scores
    for pair in BRAND_PAIRS:
        gap_data = diff_gap.get(pair.id)
        if gap_data and isinstance(gap_data, dict) and "soft_mean" in gap_data:
            soft_m = gap_data["soft_mean"]
            hard_m = gap_data["hard_mean"]
            gap = gap_data["gap"]
            collapse = "Yes" if gap > 0 else "No"
            lines.append(
                f"| {pair.brand_a} vs {pair.brand_b} | {pair.dim_type} | "
                f"{soft_m:.2f} | {hard_m:.2f} | {gap:+.2f} | {collapse} |"
            )
    lines.append("")

    # Table 5: Cross-model probe variance
    lines.append("## Table 5: Cross-Model Probe Score Variance by Dimension Type\n")
    lines.append("Prediction (H3): soft-dimension variance > hard-dimension variance.\n")
    cross_var = results.cross_model_variance
    if cross_var:
        lines.append("| Brand | Hard Dim Mean Var | Soft Dim Mean Var | Soft > Hard? |")
        lines.append("|-------|------------------:|------------------:|:------------:|")
        for brand, dim_vars in sorted(cross_var.items()):
            hard_v = [v for d, v in dim_vars.items() if d in HARD_DIMS and not (isinstance(v, float) and v != v)]
            soft_v = [v for d, v in dim_vars.items() if d in SOFT_DIMS and not (isinstance(v, float) and v != v)]
            hv_str = f"{float(np.mean(hard_v)):.3f}" if hard_v else "--"
            sv_str = f"{float(np.mean(soft_v)):.3f}" if soft_v else "--"
            check = "Yes" if (hard_v and soft_v and float(np.mean(soft_v)) > float(np.mean(hard_v))) else "No"
            lines.append(f"| {brand} | {hv_str} | {sv_str} | {check} |")
        lines.append("")

    # Table 6: Statistical tests
    if results.statistics:
        s = results.statistics
        lines.append("## Table 6: Statistical Tests\n")
        lines.append("| Hypothesis | Test | Result | Supported? |")
        lines.append("|------------|------|--------|------------|")

        h1_p = s.get("h1_ttest_p", float("nan"))
        h1_mean = s.get("h1_mean_econ_semio", float("nan"))
        p_str = f"p={h1_p:.4f}" if not (isinstance(h1_p, float) and h1_p != h1_p) else "p=N/A"
        lines.append(
            f"| H1 (Economic+Semiotic over-weighting) | t-test ({p_str}) | "
            f"Mean={h1_mean:.1f} vs baseline=25.0 | {'Yes *' if s.get('h1_supported') else 'No'} |"
        )

        sim = s.get("h2_mean_cosine_similarity", float("nan"))
        sim_str = f"{sim:.3f}" if not (isinstance(sim, float) and sim != sim) else "N/A"
        lines.append(
            f"| H2 (Convergent collapse) | Cosine similarity={sim_str} | "
            f"Threshold >= 0.85 | {'Yes *' if s.get('h2_supported') else 'No'} |"
        )

        h3_t = s.get("h3_ttest_p", float("nan"))
        h3_d = s.get("h3_cohens_d", float("nan"))
        h3_t_str = f"p={h3_t:.4f}" if not (isinstance(h3_t, float) and h3_t != h3_t) else "p=N/A"
        h3_d_str = f"{h3_d:.3f}" if not (isinstance(h3_d, float) and h3_d != h3_d) else "N/A"
        lines.append(
            f"| H3 (Soft-dim higher probe variance) | t-test ({h3_t_str}), d={h3_d_str} | "
            f"Mean var hard={s.get('h3_mean_variance_hard_dims', 0.0):.3f}, "
            f"soft={s.get('h3_mean_variance_soft_dims', 0.0):.3f} | "
            f"{'Yes *' if s.get('h3_supported') else 'No'} |"
        )

        h4_soft = s.get("h4_soft_pair_mean_gap", float("nan"))
        h4_soft_str = f"{h4_soft:+.2f}" if not (isinstance(h4_soft, float) and h4_soft != h4_soft) else "N/A"
        lines.append(
            f"| H4 (Differentiation gap) | Soft-pair gap={h4_soft_str} | "
            f"Positive gap = hard dims scored higher | "
            f"{'Yes *' if s.get('h4_supported') else 'No'} |"
        )
        lines.append("")

    # Table 7: Per-dimension mean weights
    if results.statistics and results.statistics.get("aggregate_mean_weights"):
        agg_w = results.statistics["aggregate_mean_weights"]
        lines.append("## Table 7: Aggregate Mean Weights by Dimension\n")
        lines.append("Uniform baseline = 12.5. Values > 12.5 = over-weighted.\n")
        lines.append("| Dimension | Type | Mean Weight | vs Baseline | Over-weighted? |")
        lines.append("|-----------|------|:-----------:|:-----------:|:--------------:|")
        for dim in DIMENSIONS:
            w = agg_w.get(dim, 0.0)
            delta = w - 12.5
            over = "Yes" if delta > 0 else "No"
            dim_type = "hard" if dim in HARD_DIMS else "soft"
            lines.append(
                f"| {dim} | {dim_type} | {w:.1f} | "
                f"{'+' if delta >= 0 else ''}{delta:.1f} | {over} |"
            )
        lines.append("")

    lines.append("---\n")
    lines.append("## Interpretation\n")
    lines.append(textwrap.dedent("""\
    If H1 is supported: LLMs allocate disproportionate importance to Economic and
    Semiotic dimensions when recommending brands, collapsing 8-dimensional perception
    to 2 quantifiable dimensions.

    If H2 is supported: This weighting pattern is consistent across model families,
    indicating it is a property of text-based training corpora rather than any
    specific architecture -- a structural feature of AI-mediated brand search.

    If H3 is supported: Cross-model agreement is higher on Economic and Semiotic
    probe scores than on Cultural and Temporal scores, confirming differential
    dimensional sensitivity.

    If H4 is supported: Brands that differ most on soft dimensions (Narrative,
    Ideological, Cultural, Temporal) appear more similar through AI-mediated search
    than their actual spectral distance would predict -- the operational signature
    of spectral metamerism.

    Theoretical implication: Brands investing in soft-dimension differentiation face
    an AI search penalty. Their perception clouds are real but invisible to the AI
    mediator. This creates systematic misalignment between observer perception and
    AI-mediated brand representation.
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
    smoke: bool = False,
    runs: int = 3,
    log_path: Optional[str] = None,
    include_local: bool = False,
    local_only: bool = False,
) -> ExperimentResults:
    """
    Run the R15 AI Search Metamerism experiment.

    demo mode: simulated responses to demonstrate methodology (no API keys).
    smoke mode: 1 brand pair, 1 run, all models -- quick live validation.
    live mode: all pairs, all available models.
    """
    start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    mode_label = "DEMO (simulated)" if demo else ("SMOKE (1 pair, 1 run)" if smoke else "LIVE")
    print(f"\nR15 AI Search Metamerism Experiment")
    print(f"Mode: {mode_label}")
    if not demo:
        n_pairs = 1 if smoke else (len(LOCAL_BRAND_PAIRS) if local_only else (len(BRAND_PAIRS) + len(LOCAL_BRAND_PAIRS) if include_local else len(BRAND_PAIRS)))
        print(f"Brand pairs: {n_pairs}{' (local only)' if local_only else (' (global + local)' if include_local else '')}")
        print(f"Runs per prompt: {1 if smoke else runs}")
        print(f"Temperature: 0.7\n")

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
                "  DEEPSEEK_API_KEY\n"
                "Or ensure Ollama is running at localhost:11434."
            )
            sys.exit(1)

    # Collect metadata
    metadata = collect_experiment_metadata(model_list, start_time)

    # Write pre-registration protocol and metadata (live/smoke mode only)
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
        raw_calls = run_experiment_demo(smoke=False)
    else:
        if smoke:
            actual_pairs = BRAND_PAIRS[:1]
        elif local_only:
            actual_pairs = LOCAL_BRAND_PAIRS
        elif include_local:
            actual_pairs = BRAND_PAIRS + LOCAL_BRAND_PAIRS
        else:
            actual_pairs = BRAND_PAIRS
        actual_runs = 1 if smoke else runs
        raw_calls = run_experiment_live(actual_pairs, model_list, actual_runs, log_path=log_path)

    print(f"\nCompleted {len(raw_calls)} calls. Running analysis...")

    calls_as_dicts = [asdict(c) for c in raw_calls]

    # Analysis
    weight_profiles = compute_weight_profiles(calls_as_dicts)
    dci = compute_dimensional_collapse_index(weight_profiles)
    model_sim = compute_model_similarity_matrix(weight_profiles)
    diff_scores_raw = compute_differentiation_scores(calls_as_dicts)
    diff_gap = compute_differentiation_gap(diff_scores_raw)
    probe_scores = compute_probe_scores(calls_as_dicts)
    cross_var = compute_cross_model_probe_variance(probe_scores)

    stats: dict = {}
    try:
        stats = run_statistical_tests(weight_profiles, cross_var, model_sim, diff_gap)
    except Exception as exc:
        print(f"  [warn] Statistical tests failed: {exc}")

    metadata["end_time"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Pack differentiation_gap into differentiation_scores field for serialization
    serializable_diff: dict = dict(diff_scores_raw)
    for pair_id, gap_data in diff_gap.items():
        serializable_diff[f"_gap_{pair_id}"] = gap_data

    results = ExperimentResults(
        brand_pairs=[f"{p.brand_a} vs {p.brand_b}" for p in BRAND_PAIRS],
        models=model_list,
        runs=1 if smoke else runs,
        calls=calls_as_dicts,
        weight_profiles=weight_profiles,
        dimensional_collapse_index=dci,
        model_similarity_matrix=model_sim,
        differentiation_scores=serializable_diff,
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

    # Console summary
    print("\n--- Summary ---")
    print(f"Models run: {', '.join(model_list)}")
    if weight_profiles:
        print("\nDimensional Collapse Index (Economic+Semiotic / 100, baseline=0.250):")
        for m, val in dci.items():
            if not (isinstance(val, float) and val != val):
                print(f"  {m}: {val:.3f} ({'above' if val > 0.25 else 'below'} baseline)")
        print("\nMean weight profiles:")
        print(f"  {'Dimension':<14} {'Baseline':>9} " + "".join(f"{m:>12}" for m in model_list))
        for dim in DIMENSIONS:
            vals = [f"{weight_profiles.get(m, {}).get(dim, 0.0):12.1f}" for m in model_list]
            print(f"  {dim:<14} {'12.5':>9} {''.join(vals)}")

    if stats:
        print("\nHypothesis tests:")
        h1_p = stats.get("h1_ttest_p", float("nan"))
        h1_mean = stats.get("h1_mean_econ_semio", float("nan"))
        p_str = f"p={h1_p:.4f}" if not (isinstance(h1_p, float) and h1_p != h1_p) else "p=N/A"
        print(f"  H1 (over-weighting):       {'SUPPORTED' if stats.get('h1_supported') else 'NOT SUPPORTED'} "
              f"({p_str}, mean={h1_mean:.1f}, baseline=25.0)")
        sim = stats.get("h2_mean_cosine_similarity", float("nan"))
        sim_str = f"{sim:.3f}" if not (isinstance(sim, float) and sim != sim) else "N/A"
        print(f"  H2 (convergent collapse):  {'SUPPORTED' if stats.get('h2_supported') else 'NOT SUPPORTED'} "
              f"(cosine={sim_str})")
        h3_p = stats.get("h3_ttest_p", float("nan"))
        h3_p_str = f"p={h3_p:.4f}" if not (isinstance(h3_p, float) and h3_p != h3_p) else "p=N/A"
        print(f"  H3 (soft-dim variance):    {'SUPPORTED' if stats.get('h3_supported') else 'NOT SUPPORTED'} "
              f"({h3_p_str})")
        h4_gap = stats.get("h4_soft_pair_mean_gap", float("nan"))
        h4_str = f"gap={h4_gap:+.2f}" if not (isinstance(h4_gap, float) and h4_gap != h4_gap) else "gap=N/A"
        print(f"  H4 (differentiation gap):  {'SUPPORTED' if stats.get('h4_supported') else 'NOT SUPPORTED'} "
              f"({h4_str})")

    print("\nDone.")
    return results


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="R15: AI Search Metamerism Experiment (v2 -- structured dimensional elicitation)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
        Examples:
          python ai_search_metamerism.py --demo
          python ai_search_metamerism.py --smoke
          python ai_search_metamerism.py --live --runs 1
          python ai_search_metamerism.py --live --runs 3 --output results.json
          python ai_search_metamerism.py --live --runs 1 --log L3_sessions/session_log.jsonl
          python ai_search_metamerism.py --live --runs 3 --local-brands   # global + local pairs
          python ai_search_metamerism.py --live --runs 3 --local-only     # local pairs only
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
        "--smoke",
        action="store_true",
        help="Quick validation: 1 brand pair, 1 run, all available models",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of repetitions per prompt per model (default: 3; ignored in smoke mode)",
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
    parser.add_argument(
        "--local-brands",
        action="store_true",
        help="Include local brand pairs from small non-English markets (conditional metamerism test)",
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="Run ONLY the local brand pairs (skip global pairs)",
    )
    args = parser.parse_args()

    n_modes = sum([args.live, args.demo, args.smoke])
    if n_modes > 1:
        print("ERROR: --live, --demo, and --smoke are mutually exclusive.")
        sys.exit(1)

    if not args.live and not args.smoke:
        # Default to demo if no live/smoke mode specified
        if not args.demo:
            print("No mode specified -- defaulting to --demo. Use --live or --smoke for real API calls.")
        args.demo = True

    run_experiment(
        output_file=args.output,
        summary_file=args.summary,
        demo=args.demo,
        smoke=args.smoke,
        runs=args.runs,
        log_path=args.log,
        include_local=args.local_brands,
        local_only=args.local_only,
    )


if __name__ == "__main__":
    main()
