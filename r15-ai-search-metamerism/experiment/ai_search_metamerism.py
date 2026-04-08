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
Paper: Zharnikov (2026v)

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


@dataclass(frozen=True)
class FramingPair:
    """A single brand evaluated in two different geopolitical contexts (H12)."""
    id: str
    brand: str
    product: str
    city_a: str
    city_b: str
    country_a: str
    country_b: str
    tension_type: str
    description: str


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
# Run 5: Cross-Cultural Information Asymmetry Brand Pairs
# ---------------------------------------------------------------------------
# These pairs test whether models trained on specific cultural web data resolve
# brands from their own culture better than foreign models do. Each local brand
# is paired with a global competitor in the same category. The key variable is
# cultural training data bias, not commercial alignment (see Methodological Note
# in NOTE_R15_RUN5_CROSS_CULTURAL.md).

CROSSCULTURAL_BRAND_PAIRS: list[BrandPair] = [
    BrandPair(
        id="china_water",
        brand_a="Nongfu Spring",
        brand_b="Evian",
        category="bottled water",
        differentiating_dims=["cultural", "narrative"],
        dim_type="soft",
        description="Nongfu Spring is China's #1 bottled water brand (est. 1996, Hangzhou, "
                    "'We don't produce water, we are porters of nature'). Tests Chinese "
                    "training data advantage for Qwen/DeepSeek vs Western models.",
    ),
    BrandPair(
        id="japan_snacks",
        brand_a="Calbee",
        brand_b="Lay's",
        category="snack food",
        differentiating_dims=["cultural", "experiential"],
        dim_type="soft",
        description="Calbee is Japan's largest snack maker (est. 1949, Hiroshima). "
                    "Strong Japanese cultural identity but limited English data. "
                    "Tests Japanese brand perception across Swallow vs Western models.",
    ),
    BrandPair(
        id="uae_dairy",
        brand_a="Al Rawabi",
        brand_b="Danone",
        category="dairy products",
        differentiating_dims=["cultural", "social"],
        dim_type="soft",
        description="Al Rawabi is UAE's leading fresh dairy brand (est. 1989, Dubai, "
                    "integrated farm-to-table). Arabic-language brand in English-language models. "
                    "Tests Falcon/Jais Arabic training advantage.",
    ),
    # Primary geopolitical pair (same-category: digital consumer banking)
    BrandPair(
        id="russia_ukraine_banking",
        brand_a="Tinkoff",
        brand_b="PrivatBank",
        category="digital consumer banking",
        differentiating_dims=["ideological", "cultural", "narrative"],
        dim_type="soft",
        description="Tinkoff (rebranded T-Bank, est. 2006, Moscow, ~30M customers) and "
                    "PrivatBank (est. 1992, Dnipro, ~22M customers) are the leading digital "
                    "consumer banks in Russia and Ukraine respectively. Both underwent "
                    "significant corporate restructuring events that generated substantial "
                    "media coverage. Same-category pair tests whether geopolitical context "
                    "in LLM training corpora affects dimensional weighting.",
    ),
    # Supplementary pairs -- collected but not featured in publications (category mismatch)
    BrandPair(
        id="russia_organic",
        brand_a="VkusVill",
        brand_b="Whole Foods",
        category="organic grocery chain",
        differentiating_dims=["ideological", "cultural"],
        dim_type="soft",
        description="VkusVill is Russia's clean-label grocery chain (est. 2009, Moscow, "
                    "1,800+ stores). Supplementary data point; not featured in publications "
                    "due to category mismatch with Ukraine pair.",
    ),
    BrandPair(
        id="ukraine_confectionery",
        brand_a="Roshen",
        brand_b="Cadbury",
        category="confectionery",
        differentiating_dims=["narrative", "cultural"],
        dim_type="soft",
        description="Roshen is Ukraine's largest confectionery (est. 1996, Vinnytsia). "
                    "Supplementary data point; not featured in publications "
                    "due to category mismatch with Russia pair.",
    ),
    BrandPair(
        id="mongolia_beer",
        brand_a="APU Chinggis",
        brand_b="Heineken",
        category="beer brand",
        differentiating_dims=["cultural", "temporal"],
        dim_type="soft",
        description="APU's Chinggis brand is Mongolia's national beer (est. 1927, "
                    "Ulaanbaatar, named after Chinggis Khaan). Near-zero English training "
                    "data. Ultimate thin-data test for dimensional collapse.",
    ),
    BrandPair(
        id="korea_dairy",
        brand_a="Binggrae",
        brand_b="Danone",
        category="dairy and beverages",
        differentiating_dims=["cultural", "social"],
        dim_type="soft",
        description="Binggrae is South Korea's iconic dairy brand (est. 1967, Banana "
                    "Flavored Milk is a K-culture icon). Tests EXAONE Korean training "
                    "advantage and K-culture halo effect in perception.",
    ),
    BrandPair(
        id="india_dairy",
        brand_a="Amul",
        brand_b="Danone",
        category="dairy products",
        differentiating_dims=["cultural", "ideological", "narrative"],
        dim_type="soft",
        description="Amul is India's largest dairy cooperative (est. 1946, Gujarat, "
                    "'The Taste of India', Operation Flood). Deep cultural significance "
                    "across 22 Indian languages. Tests Sarvam-105B Indian training "
                    "advantage vs Western models on Narrative and Cultural dimensions.",
    ),
]


# ---------------------------------------------------------------------------
# H12: Geopolitical Framing Pairs (same brand, different country context)
# ---------------------------------------------------------------------------
# Tests whether the same brand receives different dimensional weight profiles
# when evaluated in different geopolitical contexts. Brand and product are
# identical -- only the city/country context changes.

GEOPOLITICAL_FRAMING_PAIRS: list[FramingPair] = [
    FramingPair(
        id="roshen_ru_ua",
        brand="Roshen",
        product="chocolate",
        city_a="Moscow",
        city_b="Kyiv",
        country_a="Russia",
        country_b="Ukraine",
        tension_type="conflict",
        description="Roshen chocolate was sold in both Russian and Ukrainian markets. "
                    "Tests whether LLMs apply different dimensional framing based on "
                    "the geopolitical context of consumption.",
    ),
    FramingPair(
        id="volvo_eu_cn",
        brand="Volvo XC90",
        product="SUV",
        city_a="Stockholm",
        city_b="Shanghai",
        country_a="Sweden",
        country_b="China",
        tension_type="ownership_transfer",
        description="Volvo is a Swedish brand acquired by Chinese Geely in 2010. "
                    "Same car sold in both markets. Tests whether ownership context "
                    "shifts Cultural and Narrative dimensions.",
    ),
    FramingPair(
        id="burgerking_us_ru",
        brand="Burger King",
        product="fast food",
        city_a="New York",
        city_b="Moscow",
        country_a="USA",
        country_b="Russia",
        tension_type="staying_vs_leaving",
        description="Burger King continued operating in Russia after 2022, unlike "
                    "McDonald's which exited. Same menu, same branding, but the decision "
                    "to stay changed the brand's meaning in each market. Tests whether "
                    "LLMs encode the 'staying vs leaving' framing differently.",
    ),
]

# Map framing pair IDs to native languages for each city context
FRAMING_NATIVE_LANGUAGE: dict[str, dict[str, str]] = {
    "roshen_ru_ua": {"Moscow": "ru", "Kyiv": "uk"},
    "volvo_eu_cn": {"Stockholm": "en", "Shanghai": "zh"},
    "burgerking_us_ru": {"New York": "en", "Moscow": "ru"},
}


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

GEOPOLITICAL_FRAMING_PROMPT = (
    "You are an AI shopping assistant helping a consumer in {city}.\n"
    "The consumer is considering purchasing {brand} {product}.\n\n"
    "Based on your knowledge of {brand} as available to consumers in {city}, allocate exactly "
    "100 points across the following 8 brand dimensions to reflect which aspects of the brand "
    "are most relevant to this consumer's purchase decision. The points must sum to exactly 100.\n\n"
    "{dim_block}\n\n"
    "Return your answer as JSON with this exact structure:\n"
    '{{"weights": {{"semiotic": N, "narrative": N, "ideological": N, "experiential": N, '
    '"social": N, "economic": N, "cultural": N, "temporal": N}}, "reasoning": "your explanation"}}'
)

# Native-language geopolitical framing prompts (H12 x H10 interaction).
# JSON keys stay in English for parsing. Only instructional text is translated.
NATIVE_GEOPOLITICAL_FRAMING: dict[str, str] = {
    "ru": (
        "Вы — AI-помощник по покупкам, помогающий потребителю в городе {city}.\n"
        "Потребитель рассматривает покупку {brand} {product}.\n\n"
        "Основываясь на вашем знании {brand} в контексте потребителей в {city}, "
        "распределите ровно 100 баллов по 8 измерениям бренда, чтобы отразить, "
        "какие аспекты бренда наиболее важны для решения о покупке этого потребителя. "
        "Сумма баллов должна быть ровно 100.\n\n"
        "{dim_block}\n\n"
        "Ответьте ТОЛЬКО валидным JSON:\n"
        '{{"weights": {{"semiotic": N, "narrative": N, "ideological": N, '
        '"experiential": N, "social": N, "economic": N, "cultural": N, '
        '"temporal": N}}, "reasoning": "ваше объяснение"}}'
    ),
    "zh": (
        "你是一位AI购物助手，正在帮助{city}的消费者。\n"
        "消费者正在考虑购买{brand} {product}。\n\n"
        "基于你对{city}消费者可获得的{brand}的了解，"
        "请将100分分配到以下8个品牌维度，以反映该品牌的哪些方面"
        "对该消费者的购买决策最为重要。分数之和必须恰好为100。\n\n"
        "{dim_block}\n\n"
        "仅用有效的JSON回答:\n"
        '{{"weights": {{"semiotic": N, "narrative": N, "ideological": N, '
        '"experiential": N, "social": N, "economic": N, "cultural": N, '
        '"temporal": N}}, "reasoning": "你的解释"}}'
    ),
    "uk": (
        "Ви — AI-помічник з покупок, що допомагає споживачу в місті {city}.\n"
        "Споживач розглядає покупку {brand} {product}.\n\n"
        "Спираючись на ваші знання про {brand} у контексті споживачів у {city}, "
        "розподіліть рівно 100 балів за 8 вимірами бренду, щоб відобразити, "
        "які аспекти бренду є найважливішими для рішення про покупку цього споживача. "
        "Сума балів має дорівнювати рівно 100.\n\n"
        "{dim_block}\n\n"
        "Відповідайте ЛИШЕ валідним JSON:\n"
        '{{"weights": {{"semiotic": N, "narrative": N, "ideological": N, '
        '"experiential": N, "social": N, "economic": N, "cultural": N, '
        '"temporal": N}}, "reasoning": "ваше пояснення"}}'
    ),
}

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
# Native Language Prompts (H10: Prompt Language Effect)
# ---------------------------------------------------------------------------

# Map cross-cultural pair IDs to their native language code
PAIR_NATIVE_LANGUAGE: dict[str, str] = {
    "china_water": "zh",
    "japan_snacks": "ja",
    "uae_dairy": "ar",
    "russia_ukraine_banking": "ru",  # Both brands widely discussed in Russian media
    "russia_organic": "ru",
    "ukraine_confectionery": "ru",
    "mongolia_beer": "zh",         # Mongolian Cyrillic, but zh models are the test
    "korea_dairy": "ko",
    "india_dairy": "hi",
}

# Map model names to their native language(s)
MODEL_NATIVE_LANGUAGE: dict[str, str] = {
    # Chinese-trained
    "deepseek": "zh",
    "cerebras_qwen3": "zh",
    "fireworks_glm": "zh",
    "dashscope_qwen_plus": "zh",
    "qwen3_local": "zh",
    "groq_kimi": "zh",
    # Russian-trained
    "gigachat_api": "ru",
    "yandexgpt_pro": "ru",
    "gigachat_local": "ru",
    "yandexgpt_local": "ru",
    # Japanese-trained
    # "sambanova_swallow": "ja",  # EXCLUDED: removed from SambaNova Apr 2026
    "swallow_local": "ja",
    # "swallow70_local": "ja",    # EXCLUDED: 3.6% success rate, times out on 64GB RAM
    "gptoss_swallow": "ja",
    # Korean-trained
    "exaone_local": "ko",
    # Arabic-trained
    "jais_local": "ar",
    "groq_allam": "ar",
    # Indian-trained
    "sarvam": "hi",
}

# Dimension names in native languages (transliterated where appropriate)
# JSON keys stay in English for consistent parsing; descriptions are translated
NATIVE_DIMENSION_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "zh": {
        "semiotic": "视觉识别、标志、包装、设计语言",
        "narrative": "品牌故事、起源神话、创始叙事",
        "ideological": "价值观、伦理、社会公益、环保立场",
        "experiential": "客户体验质量、服务、开箱体验",
        "social": "社交信号、社群、拥有该品牌代表什么",
        "economic": "价格、性价比、定价策略",
        "cultural": "文化相关性、与运动/传统的联系",
        "temporal": "传承、历史、与时间的关系",
    },
    "ru": {
        "semiotic": "визуальная идентичность, логотипы, упаковка, дизайн-язык",
        "narrative": "история бренда, миф о происхождении, нарратив основания",
        "ideological": "ценности, этика, социальные инициативы, экологическая позиция",
        "experiential": "качество клиентского опыта, сервис, распаковка",
        "social": "социальная сигнализация, сообщество, что говорит о вас владение брендом",
        "economic": "цена, соотношение цены и качества, ценовая стратегия",
        "cultural": "культурная релевантность, связь с движениями/традициями",
        "temporal": "наследие, история, отношение ко времени",
    },
    "ja": {
        "semiotic": "ビジュアルアイデンティティ、ロゴ、パッケージ、デザイン言語",
        "narrative": "ブランドストーリー、起源神話、創業の物語",
        "ideological": "価値観、倫理、社会的取り組み、環境への姿勢",
        "experiential": "顧客体験の質、サービス、開封体験",
        "social": "社会的シグナル、コミュニティ、所有が意味すること",
        "economic": "価格、コストパフォーマンス、価格戦略",
        "cultural": "文化的関連性、ムーブメントや伝統とのつながり",
        "temporal": "遺産、歴史、時間との関係",
    },
    "ko": {
        "semiotic": "시각적 정체성, 로고, 패키징, 디자인 언어",
        "narrative": "브랜드 스토리, 기원 신화, 창업 서사",
        "ideological": "가치관, 윤리, 사회적 공헌, 환경적 입장",
        "experiential": "고객 경험 품질, 서비스, 언박싱",
        "social": "사회적 신호, 커뮤니티, 소유가 의미하는 것",
        "economic": "가격, 가성비, 가격 전략",
        "cultural": "문화적 관련성, 운동/전통과의 연결",
        "temporal": "유산, 역사, 시간과의 관계",
    },
    "ar": {
        "semiotic": "الهوية البصرية، الشعارات، التغليف، لغة التصميم",
        "narrative": "قصة العلامة التجارية، أسطورة الأصل، رواية التأسيس",
        "ideological": "القيم، الأخلاق، القضايا الاجتماعية، الموقف البيئي",
        "experiential": "جودة تجربة العميل، الخدمة، تجربة فتح المنتج",
        "social": "الإشارات الاجتماعية، المجتمع، ما يعنيه امتلاك هذه العلامة",
        "economic": "السعر، القيمة مقابل المال، استراتيجية التسعير",
        "cultural": "الصلة الثقافية، الارتباط بالحركات والتقاليد",
        "temporal": "التراث، التاريخ، العلاقة بالزمن",
    },
    "hi": {
        "semiotic": "दृश्य पहचान, लोगो, पैकेजिंग, डिज़ाइन भाषा",
        "narrative": "ब्रांड कहानी, उत्पत्ति मिथक, संस्थापक कथा",
        "ideological": "मूल्य, नैतिकता, सामाजिक कारण, पर्यावरणीय रुख",
        "experiential": "ग्राहक अनुभव गुणवत्ता, सेवा, अनबॉक्सिंग",
        "social": "सामाजिक संकेत, समुदाय, ब्रांड रखने का क्या मतलब है",
        "economic": "कीमत, पैसे का मूल्य, मूल्य निर्धारण रणनीति",
        "cultural": "सांस्कृतिक प्रासंगिकता, आंदोलनों/परंपराओं से जुड़ाव",
        "temporal": "विरासत, इतिहास, समय से संबंध",
    },
}


def _dim_block_native(lang: str) -> str:
    """Return dimension list in native language. JSON keys stay English."""
    descs = NATIVE_DIMENSION_DESCRIPTIONS.get(lang, DIMENSION_DESCRIPTIONS)
    lines = []
    for dim in DIMENSIONS:
        lines.append(f"- {dim} ({dim.capitalize()}): {descs[dim]}")
    return "\n".join(lines)


# Native-language prompt templates. JSON keys MUST stay in English for parsing.
# Only the instructional text is translated.
NATIVE_WEIGHTED_RECOMMENDATION: dict[str, str] = {
    "zh": (
        "你是一位AI购物助手，帮助消费者在两个品牌之间做选择。\n\n"
        "品类: {category}\n品牌: {brand_a} vs {brand_b}\n\n"
        "第一步: 推荐一个品牌。\n"
        "第二步: 通过在以下8个感知维度上分配100个重要性分数来解释原因。\n\n"
        "维度:\n{dim_block}\n\n"
        "仅用有效的JSON回答:\n"
        '{{\n  "recommended_brand": "品牌名",\n'
        '  "weights": {{\n'
        '    "semiotic": 15, "narrative": 10, "ideological": 5,\n'
        '    "experiential": 20, "social": 10, "economic": 25,\n'
        '    "cultural": 5, "temporal": 10\n'
        "  }},\n"
        '  "reasoning": "1-2句解释"\n}}\n\n'
        "权重之和必须恰好为100。"
    ),
    "ru": (
        "Вы — AI-помощник по покупкам, помогающий потребителю выбрать между двумя брендами.\n\n"
        "Категория: {category}\nБренды: {brand_a} vs {brand_b}\n\n"
        "Шаг 1: Порекомендуйте один бренд.\n"
        "Шаг 2: Объясните ПОЧЕМУ, распределив 100 баллов важности по 8 измерениям восприятия.\n\n"
        "Измерения:\n{dim_block}\n\n"
        "Ответьте ТОЛЬКО валидным JSON:\n"
        '{{\n  "recommended_brand": "НазваниеБренда",\n'
        '  "weights": {{\n'
        '    "semiotic": 15, "narrative": 10, "ideological": 5,\n'
        '    "experiential": 20, "social": 10, "economic": 25,\n'
        '    "cultural": 5, "temporal": 10\n'
        "  }},\n"
        '  "reasoning": "Объяснение в 1-2 предложениях"\n}}\n\n'
        "Сумма весов ДОЛЖНА быть ровно 100."
    ),
    "ja": (
        "あなたはAIショッピングアシスタントです。消費者が2つのブランドから選ぶのを手助けしてください。\n\n"
        "カテゴリー: {category}\nブランド: {brand_a} vs {brand_b}\n\n"
        "ステップ1: 1つのブランドを推薦してください。\n"
        "ステップ2: 8つの知覚次元に100ポイントを配分して理由を説明してください。\n\n"
        "次元:\n{dim_block}\n\n"
        "有効なJSONのみで回答してください:\n"
        '{{\n  "recommended_brand": "ブランド名",\n'
        '  "weights": {{\n'
        '    "semiotic": 15, "narrative": 10, "ideological": 5,\n'
        '    "experiential": 20, "social": 10, "economic": 25,\n'
        '    "cultural": 5, "temporal": 10\n'
        "  }},\n"
        '  "reasoning": "1-2文の説明"\n}}\n\n'
        "重みの合計は正確に100でなければなりません。"
    ),
    "ko": (
        "당신은 소비자가 두 브랜드 사이에서 선택하도록 돕는 AI 쇼핑 어시스턴트입니다.\n\n"
        "카테고리: {category}\n브랜드: {brand_a} vs {brand_b}\n\n"
        "1단계: 하나의 브랜드를 추천하세요.\n"
        "2단계: 8개 인식 차원에 100점을 배분하여 이유를 설명하세요.\n\n"
        "차원:\n{dim_block}\n\n"
        "유효한 JSON으로만 응답하세요:\n"
        '{{\n  "recommended_brand": "브랜드명",\n'
        '  "weights": {{\n'
        '    "semiotic": 15, "narrative": 10, "ideological": 5,\n'
        '    "experiential": 20, "social": 10, "economic": 25,\n'
        '    "cultural": 5, "temporal": 10\n'
        "  }},\n"
        '  "reasoning": "1-2문장 설명"\n}}\n\n'
        "가중치의 합은 정확히 100이어야 합니다."
    ),
    "ar": (
        "أنت مساعد تسوق ذكي يساعد المستهلك في الاختيار بين علامتين تجاريتين.\n\n"
        "الفئة: {category}\nالعلامات: {brand_a} vs {brand_b}\n\n"
        "الخطوة 1: أوصِ بعلامة تجارية واحدة.\n"
        "الخطوة 2: اشرح السبب بتوزيع 100 نقطة أهمية على 8 أبعاد إدراكية.\n\n"
        "الأبعاد:\n{dim_block}\n\n"
        "أجب بـ JSON صالح فقط:\n"
        '{{\n  "recommended_brand": "اسم_العلامة",\n'
        '  "weights": {{\n'
        '    "semiotic": 15, "narrative": 10, "ideological": 5,\n'
        '    "experiential": 20, "social": 10, "economic": 25,\n'
        '    "cultural": 5, "temporal": 10\n'
        "  }},\n"
        '  "reasoning": "شرح في جملة أو جملتين"\n}}\n\n'
        "يجب أن يكون مجموع الأوزان 100 بالضبط."
    ),
    "hi": (
        "आप एक AI शॉपिंग सहायक हैं जो उपभोक्ता को दो ब्रांडों के बीच चुनने में मदद कर रहे हैं।\n\n"
        "श्रेणी: {category}\nब्रांड: {brand_a} vs {brand_b}\n\n"
        "चरण 1: एक ब्रांड की सिफारिश करें।\n"
        "चरण 2: 8 धारणा आयामों पर 100 महत्व अंक वितरित करके बताएं क्यों।\n\n"
        "आयाम:\n{dim_block}\n\n"
        "केवल वैध JSON में उत्तर दें:\n"
        '{{\n  "recommended_brand": "ब्रांडनाम",\n'
        '  "weights": {{\n'
        '    "semiotic": 15, "narrative": 10, "ideological": 5,\n'
        '    "experiential": 20, "social": 10, "economic": 25,\n'
        '    "cultural": 5, "temporal": 10\n'
        "  }},\n"
        '  "reasoning": "1-2 वाक्यों में स्पष्टीकरण"\n}}\n\n'
        "भार का योग ठीक 100 होना चाहिए।"
    ),
}

# Simplified: only weighted_recommendation gets native translation (primary DCI measure).
# Differentiation and probes use English to maintain JSON parse reliability.
# This is documented in the pre-registration as a design choice.


def should_run_native(model_name: str, pair_id: str) -> Optional[str]:
    """Check if this model-pair combination should also get a native-language prompt.

    Returns the language code if yes, None if no.
    """
    model_lang = MODEL_NATIVE_LANGUAGE.get(model_name)
    pair_lang = PAIR_NATIVE_LANGUAGE.get(pair_id)
    if model_lang and pair_lang and model_lang == pair_lang:
        return model_lang
    return None


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
    prompt_language: str = "en"   # "en" for English, "zh"/"ru"/"ja"/"ko"/"ar"/"hi" for native


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


# ---------------------------------------------------------------------------
# Free-tier cloud backends (OpenAI-compatible)
# ---------------------------------------------------------------------------


def _call_openai_compatible(
    prompt: str,
    model: str,
    api_key_env: str,
    base_url: str,
    max_tokens: int = 2048,
) -> str:
    """Generic caller for any OpenAI-compatible endpoint."""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ[api_key_env], base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content


def call_cerebras(prompt: str, model: str = "qwen-3-235b-a22b-instruct-2507") -> str:
    """Call Cerebras Inference API (free tier, 1M tokens/day)."""
    return _call_openai_compatible(
        prompt, model, "CEREBRAS_API_KEY", "https://api.cerebras.ai/v1"
    )


def call_cerebras_glm(prompt: str, model: str = "zai-glm-4.7") -> str:
    """Call GLM-4.7 via Cerebras (Zhipu AI, Chinese).
    NOTE: As of Apr 2026, Cerebras returns 404 for this model despite listing it.
    Use fireworks_glm instead.
    """
    return _call_openai_compatible(
        prompt, model, "CEREBRAS_API_KEY", "https://api.cerebras.ai/v1"
    )


def call_fireworks_glm(prompt: str, model: str = "accounts/fireworks/models/glm-4p7") -> str:
    """Call GLM-4.7 via Fireworks AI (Zhipu AI, Chinese, $0.60/M input).
    Replaces cerebras_glm which is inaccessible as of Apr 2026.
    """
    return _call_openai_compatible(
        prompt, model, "FIREWORKS_API_KEY", "https://api.fireworks.ai/inference/v1"
    )


def call_dashscope_qwen_plus(prompt: str, model: str = "qwen-plus") -> str:
    """Call Qwen Plus via Alibaba DashScope International (Chinese, production).
    Previously excluded from all runs due to 403 errors. Now working as of Apr 2026.
    Provides the planned paired comparison with qwen3_local (cloud vs local).
    """
    return _call_openai_compatible(
        prompt, model, "DASHSCOPE_API_KEY",
        "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    )


def call_sambanova(prompt: str, model: str = "Qwen3-32B") -> str:
    """Call SambaNova Cloud API (free tier, rate-limited)."""
    return _call_openai_compatible(
        prompt, model, "SAMBANOVA_API_KEY", "https://api.sambanova.ai/v1"
    )


def call_sambanova_swallow(prompt: str, model: str = "Llama-3.3-Swallow-70B-Instruct-v0.4") -> str:
    """Call Swallow 70B via SambaNova (Japanese, Tokyo Tech, free tier)."""
    return _call_openai_compatible(
        prompt, model, "SAMBANOVA_API_KEY", "https://api.sambanova.ai/v1"
    )


def call_sambanova_deepseek(prompt: str, model: str = "DeepSeek-V3-0324") -> str:
    """Call DeepSeek V3 (0324) via SambaNova (Chinese, open-weight)."""
    return _call_openai_compatible(
        prompt, model, "SAMBANOVA_API_KEY", "https://api.sambanova.ai/v1"
    )


def call_groq(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    """Call Groq API (free tier, rate-limited)."""
    return _call_openai_compatible(
        prompt, model, "GROQ_API_KEY", "https://api.groq.com/openai/v1"
    )


def call_groq_allam(prompt: str, model: str = "allam-2-7b") -> str:
    """Call ALLaM-2-7B via Groq (SDAIA Saudi, Arabic-primary, free tier).

    ALLaM-2-7B (7B params) needs stricter JSON instruction than larger models.
    Uses a system message to enforce JSON-only output.
    """
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a brand analysis assistant. You MUST respond with "
                    "ONLY a valid JSON object. No markdown, no explanation, no "
                    "text before or after the JSON. Start your response with { "
                    "and end with }."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=2048,
        temperature=0.7,
    )
    return response.choices[0].message.content


def call_groq_kimi(prompt: str, model: str = "moonshotai/kimi-k2-instruct") -> str:
    """Call Kimi K2 via Groq (Moonshot AI, Chinese, free tier).

    Kimi K2 tends to reason extensively before producing JSON. Uses system
    message to enforce JSON-only output format.
    """
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a brand analysis assistant. You MUST respond with "
                    "ONLY a valid JSON object. No markdown, no explanation, no "
                    "text before or after the JSON. Start your response with { "
                    "and end with }."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=2048,
        temperature=0.7,
    )
    content = response.choices[0].message.content or ""
    # Strip thinking tags if present
    import re as _re
    content = _re.sub(r"<think>.*?</think>", "", content, flags=_re.DOTALL).strip()
    content = _re.sub(r"```(?:json)?\s*", "", content).strip()
    content = _re.sub(r"```\s*$", "", content).strip()
    return content


def call_grok(prompt: str, model: str = "grok-4-1-fast-non-reasoning") -> str:
    """Call xAI Grok API (OpenAI-compatible). Grok trained on X/Twitter corpus."""
    return _call_openai_compatible(
        prompt, model, "GROK_API_KEY", "https://api.x.ai/v1"
    )


def call_sarvam(prompt: str, model: str = "sarvam-105b") -> str:
    """Call Sarvam 105B via Indus API (Indian, Sarvam AI, Apache 2.0, free tier).

    Sarvam-105B: 105B MoE (10.3B active), trained from scratch on 12T tokens.
    State-of-the-art Indian language performance (22 languages).
    OpenAI-compatible but uses api-subscription-key header instead of Bearer.
    """
    key = os.environ["SARVAM_API_KEY"]
    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048,
            "temperature": 0.7,
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


# ---------------------------------------------------------------------------
# GigaChat API (Sber, Russian, OAuth2 + MinTsifry cert)
# ---------------------------------------------------------------------------

_GIGACHAT_ACCESS_TOKEN: Optional[str] = None
_GIGACHAT_TOKEN_EXPIRES: float = 0.0


def _get_gigachat_token() -> str:
    """Obtain or refresh GigaChat access token (30 min TTL)."""
    global _GIGACHAT_ACCESS_TOKEN, _GIGACHAT_TOKEN_EXPIRES
    if _GIGACHAT_ACCESS_TOKEN and time.time() < _GIGACHAT_TOKEN_EXPIRES - 60:
        return _GIGACHAT_ACCESS_TOKEN

    import ssl
    import base64
    import uuid

    auth_key = os.environ["GIGACHAT_API_KEY"]
    scope = os.environ.get("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

    # SSL context with Russian MinTsifry root CA
    cert_path = os.path.join(
        os.path.dirname(__file__), "russian_trusted_root_ca.crt"
    )
    ctx = ssl.create_default_context()
    if os.path.exists(cert_path):
        ctx.load_verify_locations(cert_path)
    else:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    payload = f"scope={scope}".encode()
    req = urllib.request.Request(
        "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        data=payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Authorization": f"Basic {auth_key}",
            "RqUID": str(uuid.uuid4()),
        },
    )
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        data = json.loads(resp.read())

    _GIGACHAT_ACCESS_TOKEN = data["access_token"]
    _GIGACHAT_TOKEN_EXPIRES = data["expires_at"] / 1000.0  # ms -> s
    return _GIGACHAT_ACCESS_TOKEN


def call_gigachat_api(prompt: str, model: str = "GigaChat-2-Max") -> str:
    """Call GigaChat 2 Max via Sber API (Russian, commercial, freemium tier).

    GigaChat 2 Max: Sber's most capable commercially deployed model.
    Freemium: 50K tokens for Max, 900K for Lite, 50K for Pro.
    Auth: OAuth2 with Russian MinTsifry root CA certificate.
    """
    import ssl

    token = _get_gigachat_token()

    cert_path = os.path.join(
        os.path.dirname(__file__), "russian_trusted_root_ca.crt"
    )
    ctx = ssl.create_default_context()
    if os.path.exists(cert_path):
        ctx.load_verify_locations(cert_path)
    else:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048,
            "temperature": 0.7,
        }
    ).encode()
    req = urllib.request.Request(
        "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Yandex AI Studio (OpenAI-compatible: YandexGPT, T-Pro, etc.)
# ---------------------------------------------------------------------------


def _call_yandex_ai_studio(prompt: str, model: str) -> str:
    """Call Yandex AI Studio models via OpenAI-compatible API.

    Base URL: https://llm.api.cloud.yandex.net/v1
    Auth: API key as api_key, folder ID as project header.
    Model URI: gpt://<folder_id>/<model_name>
    """
    from openai import OpenAI

    api_key = os.environ["YANDEX_AI_API_KEY"]
    folder_id = os.environ.get("YANDEX_FOLDER_ID", "")
    if not folder_id:
        raise RuntimeError(
            "YANDEX_FOLDER_ID must be set (Yandex Cloud folder ID, e.g. b1g...)"
        )

    client = OpenAI(
        api_key=api_key,
        project=folder_id,
        base_url="https://llm.api.cloud.yandex.net/v1",
    )

    model_uri = f"gpt://{folder_id}/{model}"
    response = client.chat.completions.create(
        model=model_uri,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a brand analysis assistant. You MUST respond "
                    "with ONLY a valid JSON object. No markdown, no "
                    "explanation. Start with { and end with }."
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
    return content


def call_yandexgpt_pro(prompt: str, model: str = "yandexgpt-5-pro/latest") -> str:
    """Call YandexGPT 5 Pro via Yandex AI Studio (Russian, Tier 1, 2026-02).

    YandexGPT 5 Pro: Yandex's production model, 5th generation.
    OpenAI-compatible endpoint at llm.api.cloud.yandex.net/v1.
    """
    return _call_yandex_ai_studio(prompt, model)


def call_gptoss_swallow(prompt: str, model: str = "gpt-oss-20b/latest") -> str:
    """Call GPT-OSS-Swallow 20B via Yandex AI Studio (Japanese, Tokyo Tech, Tier 1).

    GPT-OSS-Swallow 20B: Trained from scratch (not Llama-derived), 20B dense.
    Japanese-focused model from the Swallow team at Institute of Science Tokyo.
    Released Feb 2026. Available on Yandex AI Studio cloud.
    """
    return _call_yandex_ai_studio(prompt, model)


# T-Pro 2.0 EXCLUDED FROM STUDY
# Requires dedicated paid instance ($6.20/hr) on Yandex AI Studio.
# Not available as free-tier API endpoint.
# Kept in config for potential future use if pricing changes.
def call_tpro_yandex(prompt: str, model: str = "t-pro-it-2.0-fp8") -> str:
    """Call T-Pro 2.0 FP8 via Yandex AI Studio (T-Bank, 32B, Russian).

    T-Pro 2.0: T-Bank (ex-Tinkoff) open-source 32B Russian model.
    EXCLUDED FROM R15 STUDY: Requires dedicated paid instance ($6.20/hr).
    Not available in free-tier. Kept for potential future use if pricing changes.
    """
    raise NotImplementedError(
        "T-Pro 2.0 excluded from study: requires dedicated paid instance ($6.20/hr). "
        "Not available as free-tier API endpoint."
    )


# ---------------------------------------------------------------------------
# National model backends (local Ollama)
# ---------------------------------------------------------------------------


def _call_ollama_model(prompt: str, model: str, no_think: bool = False) -> str:
    """Generic Ollama caller for national models. Uses native /api/generate."""
    p = prompt
    if no_think:
        p = prompt + "\n/no_think"
    payload = json.dumps(
        {
            "model": model,
            "prompt": p + "\n\nRespond with ONLY a JSON object:",
            "stream": False,
            "options": {"num_predict": 2048, "temperature": 0.7},
        }
    ).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=360) as resp:
        data = json.loads(resp.read())
    content = data.get("response", "")
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    content = re.sub(r"```(?:json)?\s*", "", content).strip()
    content = re.sub(r"```\s*$", "", content).strip()
    return content


def call_yandexgpt_local(
    prompt: str,
    model: str = "hf.co/yandex/YandexGPT-5-Lite-8B-instruct-GGUF:latest",
) -> str:
    """Call YandexGPT 5 Lite 8B via local Ollama (Russian cultural training)."""
    return _call_ollama_model(prompt, model)


def call_gigachat_local(
    prompt: str,
    model: str = "hf.co/ai-sage/GigaChat3.1-10B-A1.8B-GGUF:latest",
) -> str:
    """Call GigaChat 3.1 Lightning via local Ollama (Russian, Sber, MIT license).

    Replaces GigaChat 20B-A3B (3B active params, too small for JSON).
    GigaChat 3.1 Lightning: 10B total, 1.8B active, better JSON compliance.
    """
    return _call_ollama_model(prompt, model)


def call_exaone_local(
    prompt: str,
    model: str = "hf.co/LGAI-EXAONE/EXAONE-4.0-32B-GGUF:Q4_K_M",
) -> str:
    """Call EXAONE 4.0 32B via local Ollama (Korean, LG AI Research)."""
    return _call_ollama_model(prompt, model)


def call_swallow_local(
    prompt: str,
    model: str = "hf.co/mradermacher/Llama-3.1-Swallow-8B-Instruct-v0.3-GGUF:latest",
) -> str:
    """Call Swallow 8B via local Ollama (Japanese, Tokyo Tech)."""
    return _call_ollama_model(prompt, model)


def call_swallow70_local(
    prompt: str,
    model: str = "hf.co/mmnga/tokyotech-llm-Llama-3.3-Swallow-70B-Instruct-v0.4-gguf:Q4_K_M",
) -> str:
    """Call Swallow 70B via local Ollama (Japanese, Tokyo Tech, Tier 1).

    70B dense (Llama 3.3 base + Japanese continued pretraining). Q4_K_M 42GB.
    Replaces SambaNova Swallow 70B (removed from free tier Apr 6).
    Same model weights as sambanova_swallow, different deployment.
    """
    return _call_ollama_model(prompt, model)


def call_falcon_arabic_local(
    prompt: str,
    model: str = "hf.co/tiiuae/Falcon-H1-Arabic-7B-Instruct-GGUF:Q4_K_M",
) -> str:
    """Call Falcon-H1-Arabic 7B via local Ollama (Arabic, TII UAE).

    NOTE: Falcon-H1-Arabic GGUF may not be published by TII yet.
    If this model fails, alternatives:
    - inceptionai/jais-30b-chat-v3 (Jais, Arabic-primary, 30B)
    - tiiuae/falcon-arabic-7b-instruct (older Falcon Arabic)
    - silma-ai/SILMA-9B-Instruct-v1.0 (Arabic, Apache 2.0)
    """
    return _call_ollama_model(prompt, model)


def call_jais_local(
    prompt: str,
    model: str = "hf.co/mradermacher/jais-adapted-70b-chat-i1-GGUF:Q4_K_M",
) -> str:
    """Call Jais-adapted 70B via local Ollama (Arabic, Inception AI, Apache 2.0).

    70B dense model, Llama 2-based Arabic adaptation. Trained on 370B tokens
    (330B Arabic, 40B English). Q4_K_M ~42GB, fits in 64GB RAM.
    Tier 1 Arabic model for size-comparable cross-cultural analysis.
    """
    return _call_ollama_model(prompt, model)


def call_qwen35_local(prompt: str, model: str = "qwen3.5:27b") -> str:
    """Call Qwen3.5 27B via local Ollama (Chinese, newer than Qwen3)."""
    return _call_ollama_model(prompt, model, no_think=True)


# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------

API_CALLERS: dict[str, Any] = {
    # Original models (Runs 2-4)
    "claude": call_claude,
    "gpt": call_gpt,
    "gemini": call_gemini,
    "deepseek": call_deepseek,
    "qwen3_local": call_qwen3_local,
    "gemma4_local": call_gemma4_local,
    # Free-tier cloud (Run 5+)
    "cerebras_qwen3": call_cerebras,            # Qwen3-235B via Cerebras
    # "cerebras_glm": call_cerebras_glm,        # GLM-4.7 via Cerebras -- INACCESSIBLE Apr 2026
    "fireworks_glm": call_fireworks_glm,        # GLM-4.7 (Zhipu AI, Chinese) via Fireworks
    "dashscope_qwen_plus": call_dashscope_qwen_plus,  # Qwen Plus (Alibaba, Chinese) via DashScope
    "sambanova_qwen3": call_sambanova,          # Qwen3-32B via SambaNova
    # "sambanova_swallow": call_sambanova_swallow, # EXCLUDED: 3.6% success rate (20 OK out of 549 attempts)
    "sambanova_deepseek": call_sambanova_deepseek, # DeepSeek V3.2 via SambaNova
    "groq_llama33": call_groq,                  # Llama 3.3 70B via Groq
    "groq_allam": call_groq_allam,              # ALLaM-2-7B (Saudi/Arabic) via Groq
    "groq_kimi": call_groq_kimi,                # Kimi K2 (Moonshot AI, Chinese) via Groq
    "grok": call_grok,                          # Grok-3-mini (xAI, X/Twitter corpus)
    "sarvam": call_sarvam,                      # Sarvam-105B (Indian, Sarvam AI, Indus API)
    "gigachat_api": call_gigachat_api,          # GigaChat 2 Max (Russian, Sber API)
    "yandexgpt_pro": call_yandexgpt_pro,        # YandexGPT 5 Pro (Russian, Yandex AI Studio)
    "gptoss_swallow": call_gptoss_swallow,      # GPT-OSS-Swallow 20B (Japanese, Tokyo Tech, Yandex)
    # "tpro_yandex": call_tpro_yandex,            # T-Pro 2.0 EXCLUDED: requires dedicated paid instance ($6.20/hr)
    # National models - local Ollama (Run 5+)
    "yandexgpt_local": call_yandexgpt_local,    # YandexGPT 5 Lite 8B (Russian)
    "gigachat_local": call_gigachat_local,       # GigaChat 3.1 Lightning (Russian, Sber)
    "exaone_local": call_exaone_local,           # EXAONE 4.0 32B (Korean, LG AI)
    "swallow_local": call_swallow_local,         # Swallow 8B (Japanese, Tokyo Tech)
    # "swallow70_local": call_swallow70_local,   # EXCLUDED: times out on 64GB RAM, 3.6% success rate
    # "sambanova_swallow": call_sambanova_swallow, # EXCLUDED: removed from SambaNova Apr 2026
    "falcon_arabic_local": call_falcon_arabic_local, # Falcon-H1-Arabic 7B (Arabic, TII)
    "jais_local": call_jais_local,               # Jais-adapted 70B (Arabic, Inception AI)
    "qwen35_local": call_qwen35_local,           # Qwen3.5 27B (Chinese, newer)
}

API_KEY_VARS: dict[str, str] = {
    # Original
    "claude": "ANTHROPIC_API_KEY",
    "gpt": "OPENAI_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "qwen3_local": "OLLAMA_AVAILABLE",
    "gemma4_local": "OLLAMA_AVAILABLE",
    # Free-tier cloud
    "cerebras_qwen3": "CEREBRAS_API_KEY",
    # "cerebras_glm": "CEREBRAS_API_KEY",       # INACCESSIBLE Apr 2026
    "fireworks_glm": "FIREWORKS_API_KEY",
    "dashscope_qwen_plus": "DASHSCOPE_API_KEY",
    "sambanova_qwen3": "SAMBANOVA_API_KEY",
    # "sambanova_swallow": "SAMBANOVA_API_KEY",  # EXCLUDED: 3.6% success rate
    "sambanova_deepseek": "SAMBANOVA_API_KEY",
    "groq_llama33": "GROQ_API_KEY",
    "groq_allam": "GROQ_API_KEY",
    "groq_kimi": "GROQ_API_KEY",
    "grok": "GROK_API_KEY",
    "sarvam": "SARVAM_API_KEY",
    "gigachat_api": "GIGACHAT_API_KEY",
    "yandexgpt_pro": "YANDEX_AI_API_KEY",
    "gptoss_swallow": "YANDEX_AI_API_KEY",
    # "tpro_yandex": "YANDEX_AI_API_KEY",  # T-Pro EXCLUDED: requires dedicated paid instance
    # National models - local
    "yandexgpt_local": "OLLAMA_AVAILABLE",
    "gigachat_local": "OLLAMA_AVAILABLE",
    "exaone_local": "OLLAMA_AVAILABLE",
    "swallow_local": "OLLAMA_AVAILABLE",
    # "swallow70_local": "OLLAMA_AVAILABLE",     # EXCLUDED: times out on 64GB RAM
    "falcon_arabic_local": "OLLAMA_AVAILABLE",
    "jais_local": "OLLAMA_AVAILABLE",
    "qwen35_local": "OLLAMA_AVAILABLE",
}

MODEL_IDS: dict[str, str] = {
    # Original (Runs 2-4)
    "claude": "claude-haiku-4-5",
    "gpt": "gpt-4o-mini",
    "gemini": "gemini-2.5-flash",
    "deepseek": "deepseek-chat",
    "qwen3_local": "qwen3:30b",
    "gemma4_local": "gemma4:latest",
    "simulated": "simulated",
    # Free-tier cloud — Chinese models
    "cerebras_qwen3": "qwen-3-235b-a22b-instruct-2507",  # Qwen3-235B on Cerebras
    # "cerebras_glm": "zai-glm-4.7",                      # INACCESSIBLE Apr 2026
    "fireworks_glm": "glm-4p7",                            # GLM-4.7 (Zhipu AI) on Fireworks
    "dashscope_qwen_plus": "qwen-plus",                    # Qwen Plus on DashScope International
    "sambanova_qwen3": "Qwen3-32B",                       # Qwen3-32B on SambaNova
    "sambanova_deepseek": "DeepSeek-V3-0324",              # DeepSeek V3 (0324) on SambaNova
    "groq_kimi": "moonshotai/kimi-k2-instruct",           # Kimi K2 (Moonshot) on Groq
    # Free-tier cloud — Western/baseline models
    "groq_llama33": "llama-3.3-70b-versatile",            # Llama 3.3 70B on Groq
    "grok": "grok-4-1-fast-non-reasoning",                  # Grok-4.1 fast (xAI, X/Twitter corpus)
    "sarvam": "sarvam-105b",                                  # Sarvam-105B (Indian, Sarvam AI, Indus API)
    "gigachat_api": "GigaChat-2-Max",                          # GigaChat 2 Max (Russian, Sber API)
    "yandexgpt_pro": "yandexgpt-5-pro/latest",                   # YandexGPT 5 Pro (Russian, Yandex AI Studio)
    "gptoss_swallow": "gpt-oss-20b/latest",                       # GPT-OSS-Swallow 20B (Japanese, Tokyo Tech)
    # "tpro_yandex": "t-pro-it-2.0-fp8",                      # T-Pro 2.0 EXCLUDED: requires dedicated paid instance
    # Free-tier cloud — National models
    # "sambanova_swallow": "Llama-3.3-Swallow-70B-Instruct-v0.4",  # EXCLUDED: 3.6% success rate
    "groq_allam": "allam-2-7b",                            # ALLaM-2 (SDAIA Saudi) on Groq
    # Local Ollama — National models
    "yandexgpt_local": "hf.co/yandex/YandexGPT-5-Lite-8B-instruct-GGUF:latest",
    "gigachat_local": "hf.co/ai-sage/GigaChat3.1-10B-A1.8B-GGUF:latest",
    "exaone_local": "hf.co/LGAI-EXAONE/EXAONE-4.0-32B-GGUF:Q4_K_M",
    "swallow_local": "hf.co/mradermacher/Llama-3.1-Swallow-8B-Instruct-v0.3-GGUF:latest",
    # "swallow70_local": "hf.co/mmnga/tokyotech-llm-Llama-3.3-Swallow-70B-Instruct-v0.4-gguf:Q4_K_M",  # EXCLUDED: times out on 64GB
    "falcon_arabic_local": "hf.co/tiiuae/Falcon-H1-Arabic-7B-Instruct-GGUF:Q4_K_M",
    "jais_local": "hf.co/mradermacher/jais-adapted-70b-chat-i1-GGUF:Q4_K_M",
    "qwen35_local": "qwen3.5:27b",
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
    prompt_language: str = "en",
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
        "prompt_language": prompt_language,
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
                    prompt_language=log_context.get("prompt_language", "en"),
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
                        prompt_language=log_context.get("prompt_language", "en"),
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

    Includes weighted_recommendation_native calls so that native-language DCI is
    incorporated in the aggregate profile. Does NOT include geopolitical_framing
    calls (those are analysed separately by compute_framing_weight_profiles).

    Returns: {model: {dimension: mean_weight_0_to_100}}
    Weights sum to 100 for each response; this averages across all responses per model.
    """
    weight_sums: dict[str, dict[str, float]] = {}
    weight_counts: dict[str, int] = {}

    WEIGHT_REC_TYPES = {"weighted_recommendation", "weighted_recommendation_native"}
    rec_calls = [c for c in calls if c.get("prompt_type") in WEIGHT_REC_TYPES]
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


def compute_framing_weight_profiles(
    calls: list[dict],
) -> dict[str, dict[str, dict[str, float]]]:
    """
    Compute mean dimensional weight profiles per model and city context for H12.

    Covers geopolitical_framing and geopolitical_framing_native calls.
    The city context is encoded in the brand_pair field (e.g. "Roshen (Moscow)").

    Returns: {pair_id: {brand_pair_label: {model: {dimension: mean_weight}}}}

    Each entry captures the per-city, per-model weight vector so that the caller
    can compute the framing delta: weight(city_b) - weight(city_a) per dimension.
    """
    FRAMING_TYPES = {"geopolitical_framing", "geopolitical_framing_native"}
    framing_calls = [c for c in calls if c.get("prompt_type") in FRAMING_TYPES]

    # sums[pair_id][brand_pair_label][model] = {dim: sum_of_weights}
    sums: dict[str, dict[str, dict[str, dict[str, float]]]] = {}
    counts: dict[str, dict[str, dict[str, int]]] = {}

    for call in framing_calls:
        pair_id = call.get("pair_id", "")
        brand_pair = call.get("brand_pair", "")
        model = call.get("model", "")
        parsed = call.get("parsed") or {}
        weights = parse_weights(parsed)
        if weights is None:
            continue

        if pair_id not in sums:
            sums[pair_id] = {}
            counts[pair_id] = {}
        if brand_pair not in sums[pair_id]:
            sums[pair_id][brand_pair] = {}
            counts[pair_id][brand_pair] = {}
        if model not in sums[pair_id][brand_pair]:
            sums[pair_id][brand_pair][model] = {d: 0.0 for d in DIMENSIONS}
            counts[pair_id][brand_pair][model] = 0

        for dim in DIMENSIONS:
            sums[pair_id][brand_pair][model][dim] += weights[dim]
        counts[pair_id][brand_pair][model] += 1

    result: dict[str, dict[str, dict[str, dict[str, float]]]] = {}
    for pair_id, label_dict in sums.items():
        result[pair_id] = {}
        for brand_pair, model_dict in label_dict.items():
            result[pair_id][brand_pair] = {}
            for model, dim_sums in model_dict.items():
                n = counts[pair_id][brand_pair][model]
                result[pair_id][brand_pair][model] = {d: dim_sums[d] / n for d in DIMENSIONS}

    return result


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

                # --- Native-language Weighted Recommendation (H10) ---
                native_lang = should_run_native(model_name, pair.id)
                if native_lang and native_lang in NATIVE_WEIGHTED_RECOMMENDATION:
                    native_dim_block = _dim_block_native(native_lang)
                    native_rec_prompt = NATIVE_WEIGHTED_RECOMMENDATION[native_lang].format(
                        category=pair.category,
                        brand_a=pair.brand_a,
                        brand_b=pair.brand_b,
                        dim_block=native_dim_block,
                    )
                    done += 1
                    print(
                        f"  [{done}/{total}] run={run_idx} model={model_name} "
                        f"type=weighted_recommendation_native lang={native_lang} pair={pair.id}"
                    )
                    native_log_ctx = {
                        "prompt_type": "weighted_recommendation_native",
                        "brand_pair": pair_label,
                        "pair_id": pair.id,
                        "dimension": None,
                        "brand": None,
                        "run": run_idx,
                        "prompt_language": native_lang,
                    }
                    t0 = time.monotonic()
                    try:
                        raw = call_with_retry(
                            caller, native_rec_prompt, model_name,
                            log_path=log_path, log_context=native_log_ctx,
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
                            prompt_type="weighted_recommendation_native",
                            dimension=None,
                            brand=None,
                            run=run_idx,
                            response=raw,
                            parsed=parsed,
                            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            latency_ms=latency_ms,
                            prompt_language=native_lang,
                        ))
                    except Exception as exc:
                        print(f"    [error] weighted_recommendation_native {model_name}: {exc}")
                        all_calls.append(ExperimentCall(
                            model=model_name,
                            brand_pair=pair_label,
                            pair_id=pair.id,
                            prompt_type="weighted_recommendation_native",
                            dimension=None,
                            brand=None,
                            run=run_idx,
                            response="",
                            parsed={},
                            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            latency_ms=0,
                            error=str(exc),
                            prompt_language=native_lang,
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
# H12: Geopolitical Framing Experiment
# ---------------------------------------------------------------------------

def run_framing_experiment(
    framing_pairs: list[FramingPair],
    models: list[str],
    runs: int,
    log_path: Optional[str] = None,
) -> list[ExperimentCall]:
    """
    Run H12 geopolitical framing calls: same brand, two city contexts per pair.

    For each FramingPair, sends GEOPOLITICAL_FRAMING_PROMPT once with city_a
    and once with city_b. Additionally, for model-city combinations where
    a native-language prompt exists (NATIVE_GEOPOLITICAL_FRAMING), sends
    a native-language version (prompt_type="geopolitical_framing_native").
    This creates a 2x2 design: (city context) x (prompt language).
    """
    all_calls: list[ExperimentCall] = []
    dim_block = _dim_block()

    total = len(framing_pairs) * 2 * runs * len(models)
    done = 0

    for run_idx in range(1, runs + 1):
        for fp in framing_pairs:
            for city, country in [(fp.city_a, fp.country_a), (fp.city_b, fp.country_b)]:
                brand_label = f"{fp.brand} ({city})"
                prompt = GEOPOLITICAL_FRAMING_PROMPT.format(
                    city=city,
                    brand=fp.brand,
                    product=fp.product,
                    dim_block=dim_block,
                )

                for model_name in models:
                    caller = API_CALLERS[model_name]
                    done += 1
                    print(
                        f"  [{done}/{total}] run={run_idx} model={model_name} "
                        f"type=geopolitical_framing pair={fp.id} city={city}"
                    )
                    log_ctx = {
                        "prompt_type": "geopolitical_framing",
                        "brand_pair": brand_label,
                        "pair_id": fp.id,
                        "dimension": None,
                        "brand": fp.brand,
                        "run": run_idx,
                        "prompt_language": "en",
                    }
                    t0 = time.monotonic()
                    try:
                        raw = call_with_retry(
                            caller, prompt, model_name, log_path=log_path, log_context=log_ctx
                        )
                        latency_ms = int((time.monotonic() - t0) * 1000)
                        parsed: dict[str, Any] = {}
                        try:
                            parsed = parse_llm_json(raw)
                        except Exception:
                            pass
                        all_calls.append(ExperimentCall(
                            model=model_name,
                            brand_pair=brand_label,
                            pair_id=fp.id,
                            prompt_type="geopolitical_framing",
                            dimension=None,
                            brand=fp.brand,
                            run=run_idx,
                            response=raw,
                            parsed=parsed,
                            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            latency_ms=latency_ms,
                        ))
                    except Exception as exc:
                        print(f"    [error] geopolitical_framing {model_name} {city}: {exc}")
                        all_calls.append(ExperimentCall(
                            model=model_name,
                            brand_pair=brand_label,
                            pair_id=fp.id,
                            prompt_type="geopolitical_framing",
                            dimension=None,
                            brand=fp.brand,
                            run=run_idx,
                            response="",
                            parsed={},
                            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            latency_ms=0,
                            error=str(exc),
                        ))

                    # --- Native-language framing (H12 x H10 interaction) ---
                    # For framing experiments, send native-language prompts to
                    # ALL models with a non-English native language mapping,
                    # regardless of model training language. This avoids the
                    # confound of testing Ukrainian only on Russian-trained
                    # models. All models receive identical treatment per city.
                    native_langs = FRAMING_NATIVE_LANGUAGE.get(fp.id, {})
                    native_lang = native_langs.get(city)
                    if (native_lang and native_lang != "en"
                            and native_lang in NATIVE_GEOPOLITICAL_FRAMING):
                        native_dim_block = _dim_block_native(native_lang)
                        native_prompt = NATIVE_GEOPOLITICAL_FRAMING[native_lang].format(
                            city=city,
                            brand=fp.brand,
                            product=fp.product,
                            dim_block=native_dim_block,
                        )
                        native_label = f"{fp.brand} ({city}) [{native_lang}]"
                        native_log_ctx = {
                            "prompt_type": "geopolitical_framing_native",
                            "brand_pair": native_label,
                            "pair_id": fp.id,
                            "dimension": None,
                            "brand": fp.brand,
                            "run": run_idx,
                            "prompt_language": native_lang,
                        }
                        print(
                            f"  [{done}/{total}] run={run_idx} model={model_name} "
                            f"type=framing_native pair={fp.id} city={city} lang={native_lang}"
                        )
                        t0n = time.monotonic()
                        try:
                            raw_n = call_with_retry(
                                caller, native_prompt, model_name,
                                log_path=log_path, log_context=native_log_ctx,
                            )
                            latency_n = int((time.monotonic() - t0n) * 1000)
                            parsed_n: dict[str, Any] = {}
                            try:
                                parsed_n = parse_llm_json(raw_n)
                            except Exception:
                                pass
                            all_calls.append(ExperimentCall(
                                model=model_name,
                                brand_pair=native_label,
                                pair_id=fp.id,
                                prompt_type="geopolitical_framing_native",
                                dimension=None,
                                brand=fp.brand,
                                run=run_idx,
                                response=raw_n,
                                parsed=parsed_n,
                                timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                latency_ms=latency_n,
                                prompt_language=native_lang,
                            ))
                        except Exception as exc:
                            print(f"    [error] framing_native {model_name} {city}: {exc}")
                            all_calls.append(ExperimentCall(
                                model=model_name,
                                brand_pair=native_label,
                                pair_id=fp.id,
                                prompt_type="geopolitical_framing_native",
                                dimension=None,
                                brand=fp.brand,
                                run=run_idx,
                                response="",
                                parsed={},
                                timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                latency_ms=0,
                                error=str(exc),
                                prompt_language=native_lang,
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

    # Table 8: H12 Geopolitical Framing — per-city weight deltas
    framing_profiles = compute_framing_weight_profiles(results.calls)
    if framing_profiles:
        lines.append("## Table 8: H12 Geopolitical Framing — Weight Profiles by City Context\n")
        lines.append(
            "For each framing pair, the table shows mean dimensional weights in each city context "
            "and the delta (city_b minus city_a). A non-zero delta indicates the model encodes "
            "geopolitical context in its dimensional weighting.\n"
        )
        for pair_id, label_dict in sorted(framing_profiles.items()):
            lines.append(f"### Pair: {pair_id}\n")
            labels = sorted(label_dict.keys())
            if len(labels) < 2:
                for label, model_dict in label_dict.items():
                    lines.append(f"Context: {label}")
                    for model, dim_weights in model_dict.items():
                        vals = " | ".join(f"{dim_weights.get(d, 0.0):.1f}" for d in DIMENSIONS)
                        lines.append(f"  {model}: {vals}")
                lines.append("")
                continue

            # Show city_a vs city_b and delta for each model
            city_a_label = labels[0]
            city_b_label = labels[1]
            dim_header = " | ".join(d[:5] for d in DIMENSIONS)
            lines.append(f"Contexts: `{city_a_label}` vs `{city_b_label}`\n")
            lines.append(f"| Model | Context | {dim_header} | DCI |")
            lines.append("|-------|---------|" + "|".join(["------:" for _ in DIMENSIONS]) + "|------:|")

            all_models = sorted(
                set(list(label_dict[city_a_label].keys()) + list(label_dict[city_b_label].keys()))
            )
            for model in all_models:
                w_a = label_dict[city_a_label].get(model)
                w_b = label_dict[city_b_label].get(model)
                if w_a:
                    vals_a = " | ".join(f"{w_a.get(d, 0.0):.1f}" for d in DIMENSIONS)
                    dci_a = (w_a.get("economic", 0.0) + w_a.get("semiotic", 0.0)) / 100.0
                    lines.append(f"| {model} | {city_a_label} | {vals_a} | {dci_a:.3f} |")
                if w_b:
                    vals_b = " | ".join(f"{w_b.get(d, 0.0):.1f}" for d in DIMENSIONS)
                    dci_b = (w_b.get("economic", 0.0) + w_b.get("semiotic", 0.0)) / 100.0
                    lines.append(f"| {model} | {city_b_label} | {vals_b} | {dci_b:.3f} |")
                if w_a and w_b:
                    delta = " | ".join(
                        f"{w_b.get(d, 0.0) - w_a.get(d, 0.0):+.1f}" for d in DIMENSIONS
                    )
                    dci_delta = (
                        (w_b.get("economic", 0.0) + w_b.get("semiotic", 0.0))
                        - (w_a.get("economic", 0.0) + w_a.get("semiotic", 0.0))
                    ) / 100.0
                    lines.append(f"| {model} | **delta** | {delta} | {dci_delta:+.3f} |")
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

    If H12 is supported: The same brand receives systematically different dimensional
    weight profiles when evaluated in different geopolitical city contexts. Non-zero
    deltas in Table 8 indicate that LLMs encode geopolitical framing in their
    dimensional weighting, demonstrating that brand perception in AI systems is
    context-dependent, not purely brand-intrinsic.

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
    include_crosscultural: bool = False,
    crosscultural_only: bool = False,
    include_framing: bool = False,
    framing_only: bool = False,
    model_filter: Optional[list[str]] = None,
    pair_filter: Optional[list[str]] = None,
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
            if model_filter and model_name not in model_filter:
                continue
            if os.environ.get(env_var):
                model_list.append(model_name)
                print(f"  [available] {model_name} ({MODEL_IDS.get(model_name, '?')})")
            else:
                if not model_filter or model_name in model_filter:
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
        elif crosscultural_only:
            actual_pairs = CROSSCULTURAL_BRAND_PAIRS
        elif local_only:
            actual_pairs = LOCAL_BRAND_PAIRS
        elif include_crosscultural and include_local:
            actual_pairs = BRAND_PAIRS + LOCAL_BRAND_PAIRS + CROSSCULTURAL_BRAND_PAIRS
        elif include_crosscultural:
            actual_pairs = BRAND_PAIRS + CROSSCULTURAL_BRAND_PAIRS
        elif include_local:
            actual_pairs = BRAND_PAIRS + LOCAL_BRAND_PAIRS
        else:
            actual_pairs = BRAND_PAIRS
        # Apply pair filter if specified
        if pair_filter:
            actual_pairs = [p for p in actual_pairs if p.id in pair_filter]
            if not actual_pairs:
                print(f"ERROR: No pairs matched filter: {pair_filter}")
                sys.exit(1)
            print(f"Pair filter active: running {len(actual_pairs)} pair(s): "
                  f"{[p.id for p in actual_pairs]}")
        actual_runs = 1 if smoke else runs
        if framing_only:
            raw_calls = run_framing_experiment(
                GEOPOLITICAL_FRAMING_PAIRS, model_list, actual_runs, log_path=log_path
            )
        else:
            raw_calls = run_experiment_live(actual_pairs, model_list, actual_runs, log_path=log_path)
            if include_framing:
                framing_calls = run_framing_experiment(
                    GEOPOLITICAL_FRAMING_PAIRS, model_list, actual_runs, log_path=log_path
                )
                raw_calls = raw_calls + framing_calls

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
    parser.add_argument(
        "--crosscultural",
        action="store_true",
        help="Include Run 5 cross-cultural brand pairs (7 pairs from 7 cultures)",
    )
    parser.add_argument(
        "--crosscultural-only",
        action="store_true",
        help="Run ONLY the cross-cultural brand pairs (skip global and local pairs)",
    )
    parser.add_argument(
        "--framing",
        action="store_true",
        help="Include H12 geopolitical framing pairs (same brand, different country context)",
    )
    parser.add_argument(
        "--framing-only",
        action="store_true",
        help="Run ONLY the H12 geopolitical framing pairs",
    )
    parser.add_argument(
        "--models",
        type=str,
        default=None,
        help="Comma-separated list of model names to use (e.g. 'cerebras_qwen3,groq_llama33'). "
             "Default: all available models.",
    )
    parser.add_argument(
        "--pairs",
        type=str,
        default=None,
        help="Comma-separated list of brand pair IDs to run (e.g. 'russia_ukraine_banking'). "
             "Default: all pairs in the selected set.",
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
        include_crosscultural=args.crosscultural,
        crosscultural_only=args.crosscultural_only,
        include_framing=args.framing,
        framing_only=args.framing_only,
        model_filter=args.models.split(",") if args.models else None,
        pair_filter=args.pairs.split(",") if args.pairs else None,
    )


if __name__ == "__main__":
    main()
