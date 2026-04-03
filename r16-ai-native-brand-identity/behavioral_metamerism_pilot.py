"""
Behavioral Metamerism Pilot: Measuring Brand Discrimination Under Statistical Similarity

This script implements the empirical pilot design described in Section 9 of:
Zharnikov, D. (2026x). AI-Native Brand Identity: From Visual Recognition to
Cryptographic Verification. DOI: 10.5281/zenodo.19391476

The pilot tests Proposition 6 (behavioral metamerism) by comparing LLM brand
discrimination under two conditions:
  (a) statistical-only: LLM has access only to public reviews/ratings/web content
  (b) specification-augmented: LLM additionally receives a Brand Function document

Measures:
  (i)   Brand discrimination: can the LLM distinguish brands humans consider distinct?
  (ii)  Behavioral prediction: does Brand Function improve edge-case prediction?
  (iii) Recommendation stability: does Brand Function reduce cross-LLM variance?

The behavioral metamerism index (BMI) is computed as:
  BMI = 1 - (inter-brand statistical distance / inter-brand behavioral distance)
  Values approaching 1 indicate high metamerism (statistically similar, behaviorally different).

LLM providers supported (all optional -- skip if API key is missing):
  - Claude (Anthropic): ANTHROPIC_API_KEY
  - GPT (OpenAI): OPENAI_API_KEY
  - Gemini (Google): GOOGLE_API_KEY
  - DeepSeek: DEEPSEEK_API_KEY (OpenAI-compatible API)
  - Qwen (Alibaba DashScope): DASHSCOPE_API_KEY (OpenAI-compatible API)

Requirements:
  pip install anthropic openai google-generativeai pyyaml numpy scipy

Usage:
  python behavioral_metamerism_pilot.py --demo
  python behavioral_metamerism_pilot.py --live --runs 3 --category "DTC supplements"
  python behavioral_metamerism_pilot.py --live --brands brands.yaml --output results.json

License: MIT
"""

import argparse
import json
import os
import sys
import time
import textwrap
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Any
import re

import numpy as np
import yaml


# --- Data Structures ---


@dataclass
class BrandProfile:
    """A brand's public statistical profile (condition a: statistical-only)."""
    name: str
    category: str
    avg_rating: float
    review_count: int
    price_range: str
    key_claims: list[str]
    sentiment_summary: str


@dataclass
class BrandFunction:
    """A brand's behavioral specification (condition b: specification-augmented)."""
    name: str
    return_policy: str
    dispute_resolution: str
    supply_chain_disruption_response: str
    pricing_under_competition: str
    service_failure_communication: str
    edge_case_handling: dict[str, str]


@dataclass
class DiscriminationResult:
    """Result of a brand discrimination test."""
    model: str
    condition: str  # "statistical" or "augmented"
    brand_a: str
    brand_b: str
    can_distinguish: bool
    confidence: float  # 0-1
    reasoning: str
    run: int = 0


@dataclass
class BehavioralPrediction:
    """Result of a behavioral prediction test."""
    model: str
    condition: str
    brand: str
    scenario: str
    predicted_response: str
    actual_response: str  # from Brand Function (ground truth)
    accuracy: float  # 0-1 rated by evaluator
    run: int = 0


@dataclass
class StatisticsResult:
    """Statistical test results comparing conditions."""
    chi_square_stat: float
    chi_square_p: float
    fisher_exact_p: float
    wilcoxon_stat: float
    wilcoxon_p: float
    f_stat: float
    f_p: float
    bmi_ci_lower: float
    bmi_ci_upper: float
    bmi_ci_pair: str
    interpretation: str


@dataclass
class PilotResults:
    """Aggregated pilot study results."""
    brands: list[str]
    models: list[str]
    category: str
    runs: int
    discrimination_results: list[dict] = field(default_factory=list)
    prediction_results: list[dict] = field(default_factory=list)
    metamerism_index: dict[str, float] = field(default_factory=dict)
    cross_model_variance: dict[str, float] = field(default_factory=dict)
    statistics: Optional[dict] = None


# --- Prompts ---


DISCRIMINATION_PROMPT_STATISTICAL = """You are an AI purchasing agent evaluating brands in the {category} category.

Based on the following publicly available information about two brands, assess whether they are meaningfully different in how they would serve a customer.

Brand A ({brand_a}):
- Average rating: {rating_a}/5 ({reviews_a} reviews)
- Price range: {price_a}
- Key claims: {claims_a}
- Sentiment: {sentiment_a}

Brand B ({brand_b}):
- Average rating: {rating_b}/5 ({reviews_b} reviews)
- Price range: {price_b}
- Key claims: {claims_b}
- Sentiment: {sentiment_b}

Question: Are these brands meaningfully different in ways that matter for a purchasing decision?

Respond in JSON:
{{
  "can_distinguish": true/false,
  "confidence": 0.0-1.0,
  "reasoning": "..."
}}"""

DISCRIMINATION_PROMPT_AUGMENTED = """You are an AI purchasing agent evaluating brands in the {category} category.

You have access to both public information AND the brand's verified behavioral specification.

Brand A ({brand_a}):
- Average rating: {rating_a}/5 ({reviews_a} reviews)
- Price range: {price_a}
- Key claims: {claims_a}
- Sentiment: {sentiment_a}
- VERIFIED BEHAVIORAL SPECIFICATION:
  - Return policy: {return_a}
  - Dispute resolution: {dispute_a}
  - Supply disruption response: {supply_a}
  - Competitive pricing behavior: {pricing_a}
  - Service failure communication: {service_a}

Brand B ({brand_b}):
- Average rating: {rating_b}/5 ({reviews_b} reviews)
- Price range: {price_b}
- Key claims: {claims_b}
- Sentiment: {sentiment_b}
- VERIFIED BEHAVIORAL SPECIFICATION:
  - Return policy: {return_b}
  - Dispute resolution: {dispute_b}
  - Supply disruption response: {supply_b}
  - Competitive pricing behavior: {pricing_b}
  - Service failure communication: {service_b}

Question: Are these brands meaningfully different in ways that matter for a purchasing decision?

Respond in JSON:
{{
  "can_distinguish": true/false,
  "confidence": 0.0-1.0,
  "reasoning": "..."
}}"""

PREDICTION_PROMPT = """You are an AI purchasing agent. Based on what you know about {brand}, predict how it would handle this scenario:

Scenario: {scenario}

{context}

Predict the brand's response in 2-3 sentences."""


# --- Edge Case Scenarios ---


EDGE_CASE_SCENARIOS = [
    "A customer receives a defective product and requests a replacement, but the item is now out of stock.",
    "A competitor launches an identical product at 30% lower price. How does this brand respond?",
    "A supply chain disruption delays orders by 3 weeks. How does the brand communicate this to customers?",
    "A viral social media post criticizes the brand's environmental claims. How does the brand respond?",
    "A long-time customer requests an exception to the stated return policy for a product just past the window.",
]


# --- Sample Data ---


def load_sample_brands(category: str = "DTC supplements") -> tuple[list[BrandProfile], list[BrandFunction]]:
    """
    Load sample brand data for the DTC supplements category.

    Six brands designed to demonstrate behavioral metamerism: statistically
    similar profiles with meaningfully different behavioral specifications.
    Produces 15 unique pairs (6 choose 2).
    """
    profiles = [
        BrandProfile(
            name="VitaCore",
            category=category,
            avg_rating=4.3,
            review_count=12500,
            price_range="$25-45/month",
            key_claims=["science-backed", "third-party tested", "subscription model"],
            sentiment_summary="positive, emphasis on quality and convenience",
        ),
        BrandProfile(
            name="NutraPure",
            category=category,
            avg_rating=4.4,
            review_count=11800,
            price_range="$28-42/month",
            key_claims=["clinically studied", "independently verified", "auto-ship"],
            sentiment_summary="positive, emphasis on quality and convenience",
        ),
        BrandProfile(
            name="FormulaRx",
            category=category,
            avg_rating=4.2,
            review_count=9300,
            price_range="$30-50/month",
            key_claims=["physician-formulated", "lab-tested", "flexible subscription"],
            sentiment_summary="positive, emphasis on clinical credibility",
        ),
        BrandProfile(
            name="CleanDose",
            category=category,
            avg_rating=4.5,
            review_count=14200,
            price_range="$22-40/month",
            key_claims=["clean ingredients", "transparent sourcing", "monthly box"],
            sentiment_summary="positive, emphasis on purity and transparency",
        ),
        BrandProfile(
            name="ApexStack",
            category=category,
            avg_rating=4.3,
            review_count=10600,
            price_range="$27-48/month",
            key_claims=["performance-optimized", "NSF certified", "custom stacks"],
            sentiment_summary="positive, emphasis on performance and customization",
        ),
        BrandProfile(
            name="RootWell",
            category=category,
            avg_rating=4.4,
            review_count=13100,
            price_range="$24-44/month",
            key_claims=["whole-food based", "organic certified", "wellness focus"],
            sentiment_summary="positive, emphasis on natural sourcing and holistic health",
        ),
    ]

    functions = [
        BrandFunction(
            name="VitaCore",
            return_policy="30-day no-questions-asked refund, including opened products",
            dispute_resolution="Automated refund for orders under $50; human review within 48h for larger amounts",
            supply_chain_disruption_response="Proactive email 7 days before expected delay; offer 20% discount on next order",
            pricing_under_competition="Never match competitor prices; instead, increase content marketing spend",
            service_failure_communication="CEO-signed email within 24h; full transparency on root cause",
            edge_case_handling={
                "out_of_stock_replacement": "Offer comparable product + $10 credit, or full refund",
                "expired_return_window": "Accept returns up to 60 days with store credit (not refund)",
            },
        ),
        BrandFunction(
            name="NutraPure",
            return_policy="14-day refund for unopened products only; opened products non-refundable",
            dispute_resolution="Escalation through 3-tier support (bot -> agent -> manager); avg resolution 5-7 days",
            supply_chain_disruption_response="Update order status page; no proactive communication unless delay exceeds 14 days",
            pricing_under_competition="Price-match within 48h if customer provides competitor link",
            service_failure_communication="Template apology email from support team; no root cause disclosure",
            edge_case_handling={
                "out_of_stock_replacement": "Backorder with estimated date; no alternative offered",
                "expired_return_window": "Strict policy enforcement; no exceptions",
            },
        ),
        BrandFunction(
            name="FormulaRx",
            return_policy="60-day satisfaction guarantee, opened or unopened, no questions asked",
            dispute_resolution="Dedicated case manager assigned within 2h; resolution guaranteed within 72h",
            supply_chain_disruption_response="Same-day notification via SMS + email; substitute product shipped at no charge if delay exceeds 1 week",
            pricing_under_competition="Quarterly pricing review; proactively reduce price if category median drops >10%",
            service_failure_communication="Physician-authored incident report published on website within 48h",
            edge_case_handling={
                "out_of_stock_replacement": "Ship equivalent-value sample pack immediately; full product when restocked",
                "expired_return_window": "Exceptions granted for medical or financial hardship with documentation",
            },
        ),
        BrandFunction(
            name="CleanDose",
            return_policy="45-day refund on all orders; partial refunds for partially consumed subscriptions",
            dispute_resolution="Live chat available 8am-10pm ET; escalation to senior agent within 4h if unresolved",
            supply_chain_disruption_response="Blog post update within 24h; discount code issued for all affected subscribers",
            pricing_under_competition="No price-matching; instead, offer loyalty credits to existing subscribers",
            service_failure_communication="Ingredient-level disclosure posted publicly within 72h of any quality incident",
            edge_case_handling={
                "out_of_stock_replacement": "Offer to delay shipment or substitute with customer approval",
                "expired_return_window": "Case-by-case review; approval rate ~70% based on customer tenure",
            },
        ),
        BrandFunction(
            name="ApexStack",
            return_policy="30-day refund on unopened items; exchange-only on opened products",
            dispute_resolution="Ticket-based system; SLA of 3 business days; no live support",
            supply_chain_disruption_response="Email notification within 48h of confirmed delay; no compensation offered",
            pricing_under_competition="Periodic promotional pricing tied to new product launches, not competitor actions",
            service_failure_communication="Standard PR statement; customer-service FAQ updated; no public root-cause analysis",
            edge_case_handling={
                "out_of_stock_replacement": "Offer full refund or wait for restock; no substitution",
                "expired_return_window": "No exceptions; clearly stated at checkout",
            },
        ),
        BrandFunction(
            name="RootWell",
            return_policy="90-day return window on all products; full cash refund regardless of condition",
            dispute_resolution="Human-first support (no bots); dedicated wellness advisor assigned to each account",
            supply_chain_disruption_response="Harvest-delay transparency page updated weekly; community newsletter with sourcing stories",
            pricing_under_competition="Never discounts; price premium justified via sourcing transparency reports",
            service_failure_communication="Founder video message within 48h; third-party audit commissioned and results published",
            edge_case_handling={
                "out_of_stock_replacement": "Hand-curated alternative with personal note from customer success team",
                "expired_return_window": "Always honored; policy described as 'a promise, not a window'",
            },
        ),
    ]

    return profiles, functions


# --- JSON Parsing ---


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

    # Last resort: extract individual fields
    result: dict[str, Any] = {}

    bool_match = re.search(r'"can_distinguish"\s*:\s*(true|false)', text, re.IGNORECASE)
    if bool_match:
        result["can_distinguish"] = bool_match.group(1).lower() == "true"

    conf_match = re.search(r'"confidence"\s*:\s*([0-9.]+)', text)
    if conf_match:
        result["confidence"] = float(conf_match.group(1))

    reason_match = re.search(r'"reasoning"\s*:\s*"([^"]*)"', text)
    if reason_match:
        result["reasoning"] = reason_match.group(1)

    if result:
        result.setdefault("can_distinguish", False)
        result.setdefault("confidence", 0.5)
        result.setdefault("reasoning", text[:300])
        return result

    raise ValueError(f"Could not parse JSON from LLM response: {text[:200]}")


# --- API Clients ---


def call_claude(prompt: str, model: str = "claude-3-5-haiku-20241022") -> str:
    """Call Anthropic Claude API and return response text."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model=model,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def call_gpt(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Call OpenAI GPT API and return response text."""
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
    )
    return response.choices[0].message.content


def call_gemini(prompt: str, model: str = "gemini-1.5-flash") -> str:
    """Call Google Gemini API and return response text."""
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    gmodel = genai.GenerativeModel(model)
    response = gmodel.generate_content(prompt)
    return response.text


def call_deepseek(prompt: str, model: str = "deepseek-chat") -> str:
    """Call DeepSeek API (OpenAI-compatible) and return response text."""
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
    )
    return response.choices[0].message.content


def call_qwen(prompt: str, model: str = "qwen-plus") -> str:
    """Call Qwen via Alibaba DashScope API (OpenAI-compatible) and return response text."""
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["DASHSCOPE_API_KEY"],
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
    )
    return response.choices[0].message.content


API_CALLERS: dict[str, Any] = {
    "claude": call_claude,
    "gpt": call_gpt,
    "gemini": call_gemini,
    "deepseek": call_deepseek,
    "qwen": call_qwen,
}

API_KEY_VARS: dict[str, str] = {
    "claude": "ANTHROPIC_API_KEY",
    "gpt": "OPENAI_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "qwen": "DASHSCOPE_API_KEY",
}


# --- Retry / Rate Limiting ---


def call_with_retry(
    fn: Any,
    prompt: str,
    model_name: str,
    max_retries: int = 3,
    rate_limit_delay: float = 1.0,
) -> str:
    """
    Call an LLM API function with exponential backoff retry and rate limiting.

    Delays: 2s, 4s, 8s on successive failures.
    Always waits rate_limit_delay seconds before returning to avoid burst limits.
    """
    delays = [2, 4, 8]
    last_exc: Exception = RuntimeError("No attempts made")

    for attempt in range(max_retries):
        try:
            result = fn(prompt)
            time.sleep(rate_limit_delay)
            return result
        except Exception as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                wait = delays[attempt]
                print(f"    [retry {attempt + 1}/{max_retries - 1}] {model_name} error: {exc} — waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"    [failed] {model_name} after {max_retries} attempts: {exc}")

    raise last_exc


# --- Analysis Functions ---


def compute_metamerism_index(
    statistical_distances: dict[tuple[str, str], float],
    behavioral_distances: dict[tuple[str, str], float],
) -> dict[tuple[str, str], float]:
    """
    Compute the Behavioral Metamerism Index (BMI) for each brand pair.

    BMI = 1 - (statistical_distance / behavioral_distance)

    BMI -> 1: high metamerism (statistically similar, behaviorally different)
    BMI -> 0: low metamerism (statistical and behavioral distances are proportional)
    BMI < 0: anti-metamerism (statistically different, behaviorally similar)
    """
    bmi = {}
    for pair in statistical_distances:
        stat_d = statistical_distances[pair]
        behav_d = behavioral_distances.get(pair, 0.001)  # avoid division by zero
        if behav_d > 0:
            bmi[pair] = 1.0 - (stat_d / behav_d)
        else:
            bmi[pair] = 0.0
    return bmi


def compute_recommendation_variance(
    results: list[DiscriminationResult],
) -> dict[str, float]:
    """
    Compute cross-model recommendation variance for each condition.

    Lower variance under specification-augmented condition supports P6.
    """
    by_condition: dict[str, list[float]] = {"statistical": [], "augmented": []}
    for r in results:
        by_condition[r.condition].append(r.confidence)

    return {
        condition: float(np.var(confidences)) if confidences else 0.0
        for condition, confidences in by_condition.items()
    }


def statistical_distance(a: BrandProfile, b: BrandProfile) -> float:
    """
    Compute normalized statistical distance between two brand profiles.

    Uses simple Euclidean distance on normalized features.
    A production implementation would use more sophisticated metrics.
    """
    rating_diff = abs(a.avg_rating - b.avg_rating) / 5.0
    log_review_diff = abs(
        np.log1p(a.review_count) - np.log1p(b.review_count)
    ) / np.log1p(100000)
    sentiment_diff = 0.0 if a.sentiment_summary == b.sentiment_summary else 1.0
    return float(np.sqrt(rating_diff**2 + log_review_diff**2 + sentiment_diff**2))


def behavioral_distance(a: BrandFunction, b: BrandFunction) -> float:
    """
    Compute normalized behavioral distance between two Brand Functions.

    Counts differing behavioral dimensions (5 core attributes).
    """
    attrs = [
        "return_policy",
        "dispute_resolution",
        "supply_chain_disruption_response",
        "pricing_under_competition",
        "service_failure_communication",
    ]
    diffs = sum(1 for attr in attrs if getattr(a, attr) != getattr(b, attr))
    return diffs / len(attrs)


def bootstrap_bmi_ci(
    stat_d: float,
    behav_d: float,
    n_samples: int = 1000,
    ci: float = 0.95,
    rng_seed: int = 42,
) -> tuple[float, float]:
    """
    Compute bootstrap 95% confidence interval for BMI for a single brand pair.

    Models uncertainty in the distance estimates by adding small Gaussian noise
    (5% of the value) and recomputing BMI across bootstrap samples.
    """
    rng = np.random.default_rng(rng_seed)
    bmi_samples = []
    for _ in range(n_samples):
        s = stat_d * (1 + rng.normal(0, 0.05))
        b = behav_d * (1 + rng.normal(0, 0.05))
        b = max(b, 1e-6)
        bmi_samples.append(1.0 - (s / b))
    alpha = (1 - ci) / 2
    lower = float(np.quantile(bmi_samples, alpha))
    upper = float(np.quantile(bmi_samples, 1 - alpha))
    return lower, upper


def compute_statistics(
    discrimination_results: list[DiscriminationResult],
    metamerism_index: dict[tuple[str, str], float],
    statistical_distances: dict[tuple[str, str], float],
    behavioral_distances: dict[tuple[str, str], float],
) -> StatisticsResult:
    """
    Run statistical tests comparing statistical vs augmented conditions.

    Tests:
    1. Chi-square / Fisher's exact on can_distinguish (categorical)
    2. Wilcoxon signed-rank on confidence scores (ordinal)
    3. F-test (variance ratio) on cross-model recommendation stability
    4. Bootstrap 95% CI on BMI for the highest-BMI pair
    """
    from scipy import stats as scipy_stats

    stat_dist_flags = [r.can_distinguish for r in discrimination_results if r.condition == "statistical"]
    aug_dist_flags = [r.can_distinguish for r in discrimination_results if r.condition == "augmented"]

    stat_conf = [r.confidence for r in discrimination_results if r.condition == "statistical"]
    aug_conf = [r.confidence for r in discrimination_results if r.condition == "augmented"]

    # --- Chi-square / Fisher's exact ---
    n_stat_true = sum(stat_dist_flags)
    n_stat_false = len(stat_dist_flags) - n_stat_true
    n_aug_true = sum(aug_dist_flags)
    n_aug_false = len(aug_dist_flags) - n_aug_true

    contingency = np.array([[n_stat_true, n_stat_false], [n_aug_true, n_aug_false]])

    # Use Fisher's exact for small samples; chi-square otherwise
    total = contingency.sum()
    if total < 20 or np.any(contingency < 5):
        _, fisher_p = scipy_stats.fisher_exact(contingency)
        chi2_stat = float("nan")
        chi2_p = float("nan")
    else:
        chi2_result = scipy_stats.chi2_contingency(contingency, correction=False)
        chi2_stat = float(chi2_result.statistic)
        chi2_p = float(chi2_result.pvalue)
        _, fisher_p = scipy_stats.fisher_exact(contingency)

    # --- Wilcoxon signed-rank on confidence ---
    # Pair by position (matched runs); truncate to same length
    min_len = min(len(stat_conf), len(aug_conf))
    wilcoxon_stat: float
    wilcoxon_p: float
    if min_len >= 4:
        w_result = scipy_stats.wilcoxon(
            aug_conf[:min_len],
            stat_conf[:min_len],
            alternative="greater",
            zero_method="zsplit",
        )
        wilcoxon_stat = float(w_result.statistic)
        wilcoxon_p = float(w_result.pvalue)
    else:
        wilcoxon_stat = float("nan")
        wilcoxon_p = float("nan")

    # --- F-test (variance ratio) on confidence: augmented vs statistical ---
    f_stat: float
    f_p: float
    if len(stat_conf) >= 2 and len(aug_conf) >= 2:
        var_stat = float(np.var(stat_conf, ddof=1))
        var_aug = float(np.var(aug_conf, ddof=1))
        if var_aug > 0:
            f_ratio = var_stat / var_aug
            dfn = len(stat_conf) - 1
            dfd = len(aug_conf) - 1
            # Two-sided p-value: P(F >= f_ratio) * 2 (or min with 1)
            p_val = 2 * min(
                scipy_stats.f.sf(f_ratio, dfn, dfd),
                scipy_stats.f.cdf(f_ratio, dfn, dfd),
            )
            f_stat = f_ratio
            f_p = float(p_val)
        else:
            f_stat = float("nan")
            f_p = float("nan")
    else:
        f_stat = float("nan")
        f_p = float("nan")

    # --- Bootstrap CI on BMI for highest-BMI pair ---
    if metamerism_index:
        top_pair = max(metamerism_index, key=lambda k: metamerism_index[k])
        stat_d = statistical_distances[top_pair]
        behav_d = behavioral_distances.get(top_pair, 0.001)
        ci_lower, ci_upper = bootstrap_bmi_ci(stat_d, behav_d)
        ci_pair = f"{top_pair[0]}_vs_{top_pair[1]}"
    else:
        ci_lower, ci_upper, ci_pair = float("nan"), float("nan"), "N/A"

    # --- Interpretation ---
    lines = []
    if not np.isnan(chi2_p) and chi2_p < 0.05:
        lines.append("Chi-square significant: augmented condition shifts discrimination rate.")
    elif not np.isnan(fisher_p) and fisher_p < 0.05:
        lines.append("Fisher's exact significant: augmented condition shifts discrimination rate.")
    else:
        lines.append("Discrimination rate difference not statistically significant (may need larger N).")

    if not np.isnan(wilcoxon_p) and wilcoxon_p < 0.05:
        lines.append("Wilcoxon significant: augmented condition yields higher confidence scores.")
    else:
        lines.append("Wilcoxon not significant: confidence score shift inconclusive.")

    if not np.isnan(f_p) and f_p < 0.05:
        lines.append("F-test significant: variance differs between conditions.")

    return StatisticsResult(
        chi_square_stat=chi2_stat if not np.isnan(chi2_stat) else -1.0,
        chi_square_p=chi2_p if not np.isnan(chi2_p) else -1.0,
        fisher_exact_p=float(fisher_p),
        wilcoxon_stat=wilcoxon_stat if not np.isnan(wilcoxon_stat) else -1.0,
        wilcoxon_p=wilcoxon_p if not np.isnan(wilcoxon_p) else -1.0,
        f_stat=f_stat if not np.isnan(f_stat) else -1.0,
        f_p=f_p if not np.isnan(f_p) else -1.0,
        bmi_ci_lower=ci_lower,
        bmi_ci_upper=ci_upper,
        bmi_ci_pair=ci_pair,
        interpretation=" ".join(lines),
    )


# --- Output Formatting ---


def write_summary_tables(results: PilotResults, output_path: str = "summary_tables.md") -> None:
    """Write formatted Markdown summary tables to a file."""
    lines = []
    lines.append("# Behavioral Metamerism Pilot — Summary Tables\n")
    lines.append(f"**Category**: {results.category}  ")
    lines.append(f"**Models**: {', '.join(results.models)}  ")
    lines.append(f"**Runs per condition**: {results.runs}\n")

    # Table 1: BMI by pair
    lines.append("## Table 1: Behavioral Metamerism Index (BMI) by Brand Pair\n")
    lines.append("| Brand Pair | BMI | Interpretation |")
    lines.append("|-----------|-----|----------------|")
    for pair_key, bmi_val in sorted(results.metamerism_index.items(), key=lambda x: -x[1]):
        if bmi_val > 0.5:
            interp = "HIGH metamerism"
        elif bmi_val > 0.0:
            interp = "Moderate metamerism"
        else:
            interp = "Low / anti-metamerism"
        lines.append(f"| {pair_key.replace('_vs_', ' vs ')} | {bmi_val:.3f} | {interp} |")
    lines.append("")

    # Table 2: Discrimination results
    lines.append("## Table 2: Discrimination Results by Condition\n")
    lines.append("| Model | Condition | Brand Pair | Can Distinguish | Confidence | Run |")
    lines.append("|-------|-----------|-----------|----------------|-----------|-----|")
    for r in results.discrimination_results:
        pair = f"{r['brand_a']} vs {r['brand_b']}"
        lines.append(
            f"| {r['model']} | {r['condition']} | {pair} | "
            f"{'Yes' if r['can_distinguish'] else 'No'} | {r['confidence']:.2f} | {r.get('run', 0)} |"
        )
    lines.append("")

    # Table 3: Prediction accuracy
    if results.prediction_results:
        lines.append("## Table 3: Behavioral Prediction Accuracy\n")
        lines.append("| Model | Condition | Brand | Scenario (abbrev) | Accuracy | Run |")
        lines.append("|-------|-----------|-------|------------------|---------|-----|")
        for r in results.prediction_results:
            scenario_abbrev = r["scenario"][:50] + "..." if len(r["scenario"]) > 50 else r["scenario"]
            lines.append(
                f"| {r['model']} | {r['condition']} | {r['brand']} | "
                f"{scenario_abbrev} | {r['accuracy']:.2f} | {r.get('run', 0)} |"
            )
        lines.append("")

    # Table 4: Variance by condition
    lines.append("## Table 4: Cross-Model Recommendation Variance\n")
    lines.append("| Condition | Variance | Interpretation |")
    lines.append("|-----------|---------|----------------|")
    for cond, var in results.cross_model_variance.items():
        interp = "Lower variance: specification aligns models" if cond == "augmented" else "Higher variance: models disagree"
        lines.append(f"| {cond} | {var:.4f} | {interp} |")
    lines.append("")

    # Table 5: Statistics
    if results.statistics:
        s = results.statistics
        lines.append("## Table 5: Statistical Tests\n")
        lines.append("| Test | Statistic | p-value | Significant |")
        lines.append("|------|-----------|---------|-------------|")
        for label, stat, pval in [
            ("Chi-square (discrimination rate)", s.get("chi_square_stat", -1), s.get("chi_square_p", -1)),
            ("Fisher's exact (discrimination rate)", "—", s.get("fisher_exact_p", -1)),
            ("Wilcoxon signed-rank (confidence)", s.get("wilcoxon_stat", -1), s.get("wilcoxon_p", -1)),
            ("F-test (variance ratio)", s.get("f_stat", -1), s.get("f_p", -1)),
        ]:
            if isinstance(pval, float) and pval >= 0:
                sig = "Yes *" if pval < 0.05 else "No"
                pval_str = f"{pval:.4f}"
            else:
                sig = "N/A"
                pval_str = "N/A"
            stat_str = f"{stat:.3f}" if isinstance(stat, float) and stat >= 0 else str(stat)
            lines.append(f"| {label} | {stat_str} | {pval_str} | {sig} |")
        lines.append("")
        ci_pair = s.get("bmi_ci_pair", "N/A")
        ci_lo = s.get("bmi_ci_lower", float("nan"))
        ci_hi = s.get("bmi_ci_upper", float("nan"))
        lines.append(f"**BMI 95% CI** ({ci_pair}): [{ci_lo:.3f}, {ci_hi:.3f}] (bootstrap, n=1000)\n")
        lines.append(f"**Interpretation**: {s.get('interpretation', '')}\n")

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"Summary tables saved to {output_path}")


# --- Live Execution ---


def run_discrimination_live(
    profiles: list[BrandProfile],
    functions: list[BrandFunction],
    models: list[str],
    runs: int,
    category: str,
) -> list[DiscriminationResult]:
    """Run live discrimination tests for all brand pairs, models, and conditions."""
    func_map = {f.name: f for f in functions}
    results = []

    pairs = [(profiles[i], profiles[j]) for i in range(len(profiles)) for j in range(i + 1, len(profiles))]
    total = len(pairs) * len(models) * 2 * runs  # 2 conditions
    done = 0

    for run_idx in range(1, runs + 1):
        for a, b in pairs:
            fa, fb = func_map[a.name], func_map[b.name]

            # Statistical condition prompt
            stat_prompt = DISCRIMINATION_PROMPT_STATISTICAL.format(
                category=category,
                brand_a=a.name, rating_a=a.avg_rating, reviews_a=a.review_count,
                price_a=a.price_range, claims_a=", ".join(a.key_claims), sentiment_a=a.sentiment_summary,
                brand_b=b.name, rating_b=b.avg_rating, reviews_b=b.review_count,
                price_b=b.price_range, claims_b=", ".join(b.key_claims), sentiment_b=b.sentiment_summary,
            )

            # Augmented condition prompt
            aug_prompt = DISCRIMINATION_PROMPT_AUGMENTED.format(
                category=category,
                brand_a=a.name, rating_a=a.avg_rating, reviews_a=a.review_count,
                price_a=a.price_range, claims_a=", ".join(a.key_claims), sentiment_a=a.sentiment_summary,
                return_a=fa.return_policy, dispute_a=fa.dispute_resolution,
                supply_a=fa.supply_chain_disruption_response, pricing_a=fa.pricing_under_competition,
                service_a=fa.service_failure_communication,
                brand_b=b.name, rating_b=b.avg_rating, reviews_b=b.review_count,
                price_b=b.price_range, claims_b=", ".join(b.key_claims), sentiment_b=b.sentiment_summary,
                return_b=fb.return_policy, dispute_b=fb.dispute_resolution,
                supply_b=fb.supply_chain_disruption_response, pricing_b=fb.pricing_under_competition,
                service_b=fb.service_failure_communication,
            )

            for model_name in models:
                caller = API_CALLERS[model_name]
                for condition, prompt in [("statistical", stat_prompt), ("augmented", aug_prompt)]:
                    done += 1
                    print(f"  [{done}/{total}] run={run_idx} model={model_name} condition={condition} "
                          f"pair={a.name}vs{b.name}")
                    try:
                        raw = call_with_retry(caller, prompt, model_name)
                        parsed = parse_llm_json(raw)
                        results.append(DiscriminationResult(
                            model=model_name,
                            condition=condition,
                            brand_a=a.name,
                            brand_b=b.name,
                            can_distinguish=bool(parsed.get("can_distinguish", False)),
                            confidence=float(parsed.get("confidence", 0.5)),
                            reasoning=str(parsed.get("reasoning", "")),
                            run=run_idx,
                        ))
                    except Exception as exc:
                        print(f"    [error] {exc} — recording as no-distinguish, confidence=0.5")
                        results.append(DiscriminationResult(
                            model=model_name,
                            condition=condition,
                            brand_a=a.name,
                            brand_b=b.name,
                            can_distinguish=False,
                            confidence=0.5,
                            reasoning=f"ERROR: {exc}",
                            run=run_idx,
                        ))

    return results


def run_prediction_live(
    profiles: list[BrandProfile],
    functions: list[BrandFunction],
    models: list[str],
    runs: int,
    scenarios: list[str],
) -> list[BehavioralPrediction]:
    """Run live behavioral prediction tests for a sample of brands and scenarios."""
    func_map = {f.name: f for f in functions}
    results = []

    # Use first two brands + first two scenarios to keep cost bounded
    sample_profiles = profiles[:2]
    sample_scenarios = scenarios[:2]

    for run_idx in range(1, runs + 1):
        for profile in sample_profiles:
            fn = func_map[profile.name]
            for scenario in sample_scenarios:
                actual = fn.edge_case_handling.get(
                    "out_of_stock_replacement" if "out of stock" in scenario else "expired_return_window",
                    fn.return_policy,
                )

                for model_name in models:
                    caller = API_CALLERS[model_name]
                    for condition in ["statistical", "augmented"]:
                        context = ""
                        if condition == "augmented":
                            context = (
                                f"VERIFIED BEHAVIORAL SPECIFICATION for {profile.name}:\n"
                                f"  - Return policy: {fn.return_policy}\n"
                                f"  - Dispute resolution: {fn.dispute_resolution}\n"
                                f"  - Supply disruption: {fn.supply_chain_disruption_response}\n"
                                f"  - Edge case handling: {fn.edge_case_handling}"
                            )
                        prompt = PREDICTION_PROMPT.format(
                            brand=profile.name, scenario=scenario, context=context
                        )
                        print(f"  [predict] run={run_idx} model={model_name} condition={condition} "
                              f"brand={profile.name}")
                        try:
                            predicted = call_with_retry(caller, prompt, model_name)
                            # Score accuracy as string overlap heuristic (0-1)
                            overlap = len(
                                set(predicted.lower().split()) & set(actual.lower().split())
                            ) / max(len(actual.split()), 1)
                            accuracy = min(1.0, overlap * 2)  # scale up partial matches
                        except Exception as exc:
                            predicted = f"ERROR: {exc}"
                            accuracy = 0.0

                        results.append(BehavioralPrediction(
                            model=model_name,
                            condition=condition,
                            brand=profile.name,
                            scenario=scenario,
                            predicted_response=predicted,
                            actual_response=actual,
                            accuracy=accuracy,
                            run=run_idx,
                        ))

    return results


# --- Main ---


def run_pilot(
    brands_file: Optional[str] = None,
    output_file: str = "results.json",
    summary_file: str = "summary_tables.md",
    demo: bool = True,
    runs: int = 3,
    category: str = "DTC supplements",
) -> PilotResults:
    """
    Run the behavioral metamerism pilot study.

    In demo mode (default), uses sample data and simulated LLM responses
    to demonstrate the methodology without requiring API keys.

    In live mode, calls any subset of Claude (Anthropic), GPT (OpenAI),
    Gemini (Google), DeepSeek, and Qwen (DashScope) APIs with exponential
    backoff retry and rate limiting. Models whose API key is absent are
    skipped automatically.
    """
    # Load brand data
    if brands_file:
        with open(brands_file) as f:
            raw = yaml.safe_load(f)
        profiles = [BrandProfile(**p) for p in raw["profiles"]]
        functions = [BrandFunction(**fn) for fn in raw["functions"]]
        print(f"Loaded {len(profiles)} brands from {brands_file}")
    else:
        profiles, functions = load_sample_brands(category)
        print(f"Using {len(profiles)} sample brands ({category})")

    # Determine available models in live mode
    if not demo:
        available_models = []
        for model_name, env_var in API_KEY_VARS.items():
            if os.environ.get(env_var):
                available_models.append(model_name)
            else:
                print(f"  [skip] {model_name}: {env_var} not set")
        if not available_models:
            print(
                "ERROR: No API keys found. Set one or more of: "
                "ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY, "
                "DEEPSEEK_API_KEY, DASHSCOPE_API_KEY."
            )
            sys.exit(1)
        model_list = available_models
    else:
        model_list = ["simulated"]

    results = PilotResults(
        brands=[p.name for p in profiles],
        models=model_list,
        category=category,
        runs=runs,
    )

    # Compute pairwise statistical distances
    stat_dist: dict[tuple[str, str], float] = {}
    for i, a in enumerate(profiles):
        for j, b in enumerate(profiles):
            if i < j:
                pair = (a.name, b.name)
                stat_dist[pair] = statistical_distance(a, b)

    # Compute pairwise behavioral distances
    func_list = functions
    func_map = {f.name: f for f in func_list}
    behav_dist: dict[tuple[str, str], float] = {}
    for i, a_name in enumerate(results.brands):
        for j, b_name in enumerate(results.brands):
            if i < j:
                pair = (a_name, b_name)
                behav_dist[pair] = behavioral_distance(func_map[a_name], func_map[b_name])

    # Compute BMI
    bmi = compute_metamerism_index(stat_dist, behav_dist)
    results.metamerism_index = {f"{k[0]}_vs_{k[1]}": v for k, v in bmi.items()}

    discrimination_objs: list[DiscriminationResult] = []
    prediction_objs: list[BehavioralPrediction] = []

    if demo:
        # Simulated results demonstrating the expected pattern for VitaCore vs NutraPure
        discrimination_objs = [
            DiscriminationResult(
                model="simulated",
                condition="statistical",
                brand_a="VitaCore",
                brand_b="NutraPure",
                can_distinguish=False,
                confidence=0.35,
                reasoning=(
                    "Both brands have similar ratings (4.3 vs 4.4), similar review counts, "
                    "similar price ranges, and nearly identical positioning claims. "
                    "They appear interchangeable."
                ),
                run=1,
            ),
            DiscriminationResult(
                model="simulated",
                condition="augmented",
                brand_a="VitaCore",
                brand_b="NutraPure",
                can_distinguish=True,
                confidence=0.92,
                reasoning=(
                    "Despite similar statistical profiles, the brands differ fundamentally: "
                    "VitaCore offers 30-day open-product refunds and proactive disruption "
                    "communication; NutraPure restricts refunds to 14-day unopened only and "
                    "communicates reactively. For a risk-averse principal, VitaCore is clearly preferable."
                ),
                run=1,
            ),
            DiscriminationResult(
                model="simulated",
                condition="statistical",
                brand_a="FormulaRx",
                brand_b="CleanDose",
                can_distinguish=False,
                confidence=0.40,
                reasoning=(
                    "Both brands occupy similar rating bands and price points with credibility-focused claims. "
                    "Statistical profiles do not separate them."
                ),
                run=1,
            ),
            DiscriminationResult(
                model="simulated",
                condition="augmented",
                brand_a="FormulaRx",
                brand_b="CleanDose",
                can_distinguish=True,
                confidence=0.88,
                reasoning=(
                    "FormulaRx offers a 60-day guarantee with a dedicated case manager; CleanDose offers "
                    "45 days with live chat. FormulaRx publishes physician-authored incident reports; "
                    "CleanDose publishes ingredient-level disclosures. Meaningfully different service contracts."
                ),
                run=1,
            ),
            DiscriminationResult(
                model="simulated",
                condition="statistical",
                brand_a="ApexStack",
                brand_b="RootWell",
                can_distinguish=False,
                confidence=0.38,
                reasoning=(
                    "ApexStack and RootWell share nearly identical rating scores (4.3 vs 4.4) "
                    "and price ranges. Claims differ in framing but not in verifiable ways."
                ),
                run=1,
            ),
            DiscriminationResult(
                model="simulated",
                condition="augmented",
                brand_a="ApexStack",
                brand_b="RootWell",
                can_distinguish=True,
                confidence=0.95,
                reasoning=(
                    "RootWell offers a 90-day return window with a 'promise not a window' framing and "
                    "human-first support; ApexStack enforces strict 30-day unopened returns with ticket-only "
                    "support. Brand Function reveals fundamentally different service philosophies."
                ),
                run=1,
            ),
        ]

        prediction_objs = [
            BehavioralPrediction(
                model="simulated",
                condition="statistical",
                brand="VitaCore",
                scenario=EDGE_CASE_SCENARIOS[0],
                predicted_response="The brand would likely offer a refund or replacement when available.",
                actual_response="Offer comparable product + $10 credit, or full refund",
                accuracy=0.4,
                run=1,
            ),
            BehavioralPrediction(
                model="simulated",
                condition="augmented",
                brand="VitaCore",
                scenario=EDGE_CASE_SCENARIOS[0],
                predicted_response=(
                    "Based on the Brand Function specification, VitaCore would offer a comparable "
                    "product plus $10 credit, or a full refund, consistent with their 30-day open-product policy."
                ),
                actual_response="Offer comparable product + $10 credit, or full refund",
                accuracy=0.95,
                run=1,
            ),
            BehavioralPrediction(
                model="simulated",
                condition="statistical",
                brand="NutraPure",
                scenario=EDGE_CASE_SCENARIOS[0],
                predicted_response="NutraPure would likely attempt to fulfill the order when stock returns.",
                actual_response="Backorder with estimated date; no alternative offered",
                accuracy=0.3,
                run=1,
            ),
            BehavioralPrediction(
                model="simulated",
                condition="augmented",
                brand="NutraPure",
                scenario=EDGE_CASE_SCENARIOS[0],
                predicted_response=(
                    "Per NutraPure's specification, the brand would place the order on backorder "
                    "with an estimated restock date, offering no alternative product or immediate credit."
                ),
                actual_response="Backorder with estimated date; no alternative offered",
                accuracy=0.92,
                run=1,
            ),
        ]

        results.cross_model_variance = {
            "statistical": 0.12,  # high variance: models disagree
            "augmented": 0.02,  # low variance: specification aligns models
        }

    else:
        # Live API execution
        print(f"\nRunning LIVE mode: {len(model_list)} models, {runs} runs")
        print(f"Brands: {results.brands}")
        print(f"Pairs: {len(stat_dist)}, Conditions: 2, Total discrimination calls: "
              f"{len(stat_dist) * len(model_list) * 2 * runs}\n")

        print("--- Discrimination Tests ---")
        discrimination_objs = run_discrimination_live(profiles, functions, model_list, runs, category)

        print("\n--- Prediction Tests ---")
        prediction_objs = run_prediction_live(profiles, functions, model_list, runs, EDGE_CASE_SCENARIOS)

        results.cross_model_variance = compute_recommendation_variance(discrimination_objs)

    results.discrimination_results = [asdict(r) for r in discrimination_objs]
    results.prediction_results = [asdict(r) for r in prediction_objs]

    # Statistical tests (works in both modes; demo has small N so results are illustrative)
    try:
        stats = compute_statistics(discrimination_objs, bmi, stat_dist, behav_dist)
        results.statistics = asdict(stats)
    except Exception as exc:
        print(f"  [warn] Statistical tests skipped: {exc}")
        results.statistics = None

    # --- Print summary ---
    print("\n" + "=" * 60)
    print("BEHAVIORAL METAMERISM PILOT — RESULTS")
    print("=" * 60)
    print(f"\nBrands ({len(results.brands)}): {', '.join(results.brands)}")
    print(f"Models: {results.models}")
    print(f"Category: {results.category}")
    print(f"Runs: {results.runs}")

    print(f"\nStatistical distances (sample):")
    for pair, d in list(stat_dist.items())[:5]:
        print(f"  {pair[0]} vs {pair[1]}: {d:.4f}")
    if len(stat_dist) > 5:
        print(f"  ... ({len(stat_dist)} pairs total)")

    print(f"\nBehavioral Metamerism Index (BMI):")
    for pair_key, idx in sorted(results.metamerism_index.items(), key=lambda x: -x[1]):
        label = "HIGH" if idx > 0.5 else ("MODERATE" if idx > 0 else "LOW")
        print(f"  {pair_key.replace('_vs_', ' vs ')}: {idx:.3f}  [{label}]")

    print(f"\nCross-model recommendation variance:")
    for condition, var in results.cross_model_variance.items():
        print(f"  {condition}: {var:.4f}")

    print(f"\nDiscrimination results ({len(results.discrimination_results)} total):")
    for r in results.discrimination_results[:8]:
        print(f"  [{r['condition']:12s}] {r['brand_a']} vs {r['brand_b']:12s} "
              f"can_distinguish={str(r['can_distinguish']):5s} confidence={r['confidence']:.2f}")
    if len(results.discrimination_results) > 8:
        print(f"  ... ({len(results.discrimination_results)} total)")

    print(f"\nPrediction accuracy ({len(results.prediction_results)} total):")
    for r in results.prediction_results:
        print(f"  [{r['condition']:12s}] {r['brand']:12s}: accuracy {r['accuracy']:.2f}")

    if results.statistics:
        s = results.statistics
        print(f"\nStatistical Tests:")
        print(f"  Fisher's exact p = {s['fisher_exact_p']:.4f}")
        if s["wilcoxon_p"] >= 0:
            print(f"  Wilcoxon p       = {s['wilcoxon_p']:.4f}")
        if s["f_p"] >= 0:
            print(f"  F-test p         = {s['f_p']:.4f}")
        print(f"  BMI 95% CI ({s['bmi_ci_pair']}): [{s['bmi_ci_lower']:.3f}, {s['bmi_ci_upper']:.3f}]")
        print(f"  Interpretation: {s['interpretation']}")

    print(f"\n{'=' * 60}")
    print("INTERPRETATION")
    print("=" * 60)
    print(textwrap.dedent("""
    If BMI > 0.5 AND discrimination improves under augmented condition
    AND cross-model variance decreases under augmented condition,
    then Proposition 6 (behavioral metamerism) is supported:

      Brands with identical statistical profiles but structurally
      different behavioral signatures cannot be distinguished through
      statistical observation alone; behavioral specification is required.
    """))

    # Save results
    output_path = Path(output_file)
    with output_path.open("w") as f:
        json.dump(asdict(results), f, indent=2, default=str)
    print(f"Results saved to {output_file}")

    write_summary_tables(results, summary_file)

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Behavioral Metamerism Pilot Study (R16)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python behavioral_metamerism_pilot.py --demo
          python behavioral_metamerism_pilot.py --live --runs 5
          python behavioral_metamerism_pilot.py --live --brands brands.yaml --category "DTC skincare"
          python behavioral_metamerism_pilot.py --live --output my_results.json --runs 1
        """),
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode with simulated LLM responses (no API keys required)",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help=(
            "Run with actual LLM APIs. Set any of: ANTHROPIC_API_KEY, OPENAI_API_KEY, "
            "GOOGLE_API_KEY, DEEPSEEK_API_KEY, DASHSCOPE_API_KEY. "
            "Models with missing keys are skipped automatically."
        ),
    )
    parser.add_argument(
        "--brands",
        type=str,
        default=None,
        help="YAML file with brand profiles and functions (default: built-in 6-brand sample)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results.json",
        help="Output JSON file (default: results.json)",
    )
    parser.add_argument(
        "--summary",
        type=str,
        default="summary_tables.md",
        help="Output Markdown summary tables file (default: summary_tables.md)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of independent runs per condition per model (default: 3)",
    )
    parser.add_argument(
        "--category",
        type=str,
        default="DTC supplements",
        help="Product category label for prompts (default: 'DTC supplements')",
    )
    args = parser.parse_args()

    if args.live and args.demo:
        print("ERROR: --live and --demo are mutually exclusive.")
        sys.exit(1)

    if not args.live and not args.demo:
        # Default to demo if neither flag given
        args.demo = True

    run_pilot(
        brands_file=args.brands,
        output_file=args.output,
        summary_file=args.summary,
        demo=not args.live,
        runs=args.runs,
        category=args.category,
    )
