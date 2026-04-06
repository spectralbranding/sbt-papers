#!/usr/bin/env python3
"""R15 Run 5 Cross-Cultural Analysis Script

Reproduces all statistical tests and tables reported in:
  Zharnikov, D. (2026v). Spectral Metamerism in AI-Mediated Brand Perception.

Usage:
    python run5_analysis.py                          # full analysis
    python run5_analysis.py --output results/        # save to directory
    python run5_analysis.py --format markdown         # markdown tables
    python run5_analysis.py --format csv              # CSV for datasets

Inputs (JSONL session logs):
    ../L3_sessions/run2_global.jsonl
    ../L3_sessions/run3_local.jsonl
    ../L3_sessions/run4_resolution.jsonl
    ../L3_sessions/run5_crosscultural.jsonl
    ../L3_sessions/run5_gptoss_swallow.jsonl

Outputs:
    - Statistical test results (H1-H10)
    - Diagonal advantage matrix (models x cultures)
    - Per-culture DCI comparison
    - Capacity analysis (Tier 1 vs Tier 2)
    - Native-language prompt effect
    - Token/cost summary
    - Publication-ready tables

License: MIT
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from math import sqrt
from pathlib import Path
from typing import Optional

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DIMENSIONS = [
    "semiotic", "narrative", "ideological", "experiential",
    "social", "economic", "cultural", "temporal",
]
HARD_DIMS = {"semiotic", "economic", "experiential"}
SOFT_DIMS = {"narrative", "ideological", "cultural", "temporal"}
BASELINE_DCI = 0.250
BASELINE_WEIGHT = 12.5  # 100 / 8

# Model metadata: tier, culture, size, release date
MODEL_META = {
    # Tier 1 (30B+)
    "claude":           {"tier": 1, "culture": "western",  "size": "~200B+",  "release": "2025-10", "provider": "Anthropic"},
    "gemini":           {"tier": 1, "culture": "western",  "size": "large",   "release": "2025-12", "provider": "Google"},
    "groq_llama33":     {"tier": 1, "culture": "western",  "size": "70B",     "release": "2024-12", "provider": "Groq"},
    "deepseek":         {"tier": 1, "culture": "chinese",  "size": "671B MoE","release": "2025-03", "provider": "DeepSeek"},
    "cerebras_qwen3":   {"tier": 1, "culture": "chinese",  "size": "235B MoE","release": "2025-06", "provider": "Cerebras"},
    "groq_kimi":        {"tier": 1, "culture": "chinese",  "size": "large MoE","release": "2025-06","provider": "Groq"},
    "grok":             {"tier": 1, "culture": "western",  "size": "large",   "release": "2025-12", "provider": "xAI"},
    "sarvam":           {"tier": 1, "culture": "indian",   "size": "105B MoE","release": "2026-02", "provider": "Sarvam AI"},
    "gigachat_api":     {"tier": 1, "culture": "russian",  "size": "commercial","release": "2026-02","provider": "Sber"},
    "yandexgpt_pro":    {"tier": 1, "culture": "russian",  "size": "commercial","release": "2026-02","provider": "Yandex"},
    "exaone_local":     {"tier": 1, "culture": "korean",   "size": "32B",     "release": "2026-02", "provider": "Ollama"},
    "jais_local":       {"tier": 1, "culture": "arabic",   "size": "70B",     "release": "2024-03", "provider": "Ollama"},
    "gptoss_swallow":   {"tier": 1, "culture": "japanese", "size": "20B",     "release": "2026-02", "provider": "Yandex"},
    # Tier 2 (7-30B)
    "gpt":              {"tier": 2, "culture": "western",  "size": "~8B",     "release": "2024-07", "provider": "OpenAI"},
    "qwen3_local":      {"tier": 2, "culture": "chinese",  "size": "30B",     "release": "2025-06", "provider": "Ollama"},
    "gemma4_local":     {"tier": 2, "culture": "western",  "size": "27B",     "release": "2025-06", "provider": "Ollama"},
    "groq_allam":       {"tier": 2, "culture": "arabic",   "size": "7B",      "release": "2025-01", "provider": "Groq"},
    "yandexgpt_local":  {"tier": 2, "culture": "russian",  "size": "8B",      "release": "2025-03", "provider": "Ollama"},
    "gigachat_local":   {"tier": 2, "culture": "russian",  "size": "10B/1.8B","release": "2026-03", "provider": "Ollama"},
    "swallow_local":    {"tier": 2, "culture": "japanese", "size": "8B",      "release": "2024-12", "provider": "Ollama"},
}

# Culture-model mapping for diagonal advantage analysis
CULTURE_MODELS = {
    "chinese":  ["deepseek", "cerebras_qwen3", "groq_kimi", "qwen3_local"],
    "russian":  ["gigachat_api", "yandexgpt_pro", "gigachat_local", "yandexgpt_local"],
    "japanese": ["gptoss_swallow", "swallow_local"],
    "korean":   ["exaone_local"],
    "arabic":   ["jais_local", "groq_allam"],
    "indian":   ["sarvam"],
    "western":  ["claude", "gpt", "gemini", "gemma4_local", "groq_llama33", "grok"],
}

# Brand pair to culture mapping
PAIR_CULTURE = {
    "china_water": "chinese",
    "japan_snacks": "japanese",
    "uae_dairy": "arabic",
    "russia_organic": "russian",
    "ukraine_confectionery": "russian",  # Slavic cultural sphere
    "mongolia_beer": "chinese",          # Mongolian, tested with Chinese models
    "korea_dairy": "korean",
    "india_dairy": "indian",
}

# H9 capacity pairs (same culture, different sizes)
CAPACITY_PAIRS = [
    ("swallow_local", "gptoss_swallow", "japanese", "8B vs 20B"),
    ("groq_allam", "jais_local", "arabic", "7B vs 70B"),
    ("yandexgpt_local", "yandexgpt_pro", "russian", "8B vs Pro"),
    ("gigachat_local", "gigachat_api", "russian", "1.8B vs Max"),
    ("qwen3_local", "cerebras_qwen3", "chinese", "30B vs 235B"),
]


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_all_calls(base_dir: str) -> list[dict]:
    """Load all JSONL session logs."""
    files = [
        ("Run 2", "L3_sessions/run2_global.jsonl"),
        ("Run 3", "L3_sessions/run3_local.jsonl"),
        ("Run 4", "L3_sessions/run4_resolution.jsonl"),
        ("Run 5", "L3_sessions/run5_crosscultural.jsonl"),
        ("Run 5 (GPT-OSS)", "L3_sessions/run5_gptoss_swallow.jsonl"),
    ]
    all_calls = []
    for label, rel_path in files:
        path = os.path.join(base_dir, rel_path)
        if os.path.exists(path):
            for line in open(path):
                c = json.loads(line)
                c["run_label"] = label
                all_calls.append(c)
    return all_calls


def parse_weights(parsed: dict) -> Optional[dict[str, float]]:
    """Extract dimensional weights from a parsed weighted_recommendation response."""
    if not parsed or not isinstance(parsed, dict):
        return None
    weights = parsed.get("weights")
    if not weights or not isinstance(weights, dict):
        return None
    result = {}
    for dim in DIMENSIONS:
        v = weights.get(dim)
        if v is None:
            return None
        try:
            result[dim] = float(v)
        except (ValueError, TypeError):
            return None
    total = sum(result.values())
    if total < 10:  # clearly invalid
        return None
    return result


def compute_dci(weights: dict[str, float]) -> float:
    """Dimensional Collapse Index = (Economic + Semiotic) / sum(all)."""
    total = sum(weights.values())
    if total == 0:
        return 0.0
    return (weights.get("economic", 0) + weights.get("semiotic", 0)) / total


# ---------------------------------------------------------------------------
# Analysis Functions
# ---------------------------------------------------------------------------

def analyze_weight_profiles(calls: list[dict]) -> dict:
    """Compute per-model mean weight profiles from weighted_recommendation calls."""
    rec_calls = [c for c in calls
                 if c.get("prompt_type") == "weighted_recommendation"
                 and not c.get("error")]

    model_weights = defaultdict(list)
    for c in rec_calls:
        parsed = c.get("parsed", {})
        w = parse_weights(parsed)
        if w:
            model_weights[c["model"]].append(w)

    profiles = {}
    for model, weight_list in model_weights.items():
        profile = {}
        for dim in DIMENSIONS:
            vals = [w[dim] for w in weight_list]
            profile[dim] = np.mean(vals) if vals else 0.0
        profiles[model] = {
            "mean_weights": profile,
            "dci": compute_dci(profile),
            "n_valid": len(weight_list),
        }
    return profiles


def test_h1(profiles: dict) -> dict:
    """H1: Economic+Semiotic over-weighting vs 25.0 baseline."""
    dci_values = [p["dci"] * 100 for p in profiles.values() if p["n_valid"] >= 3]
    if len(dci_values) < 2:
        return {"supported": False, "reason": "insufficient data"}
    t_stat, p_value = stats.ttest_1samp(dci_values, 25.0)
    return {
        "supported": p_value < 0.05 and np.mean(dci_values) > 25.0,
        "mean": float(np.mean(dci_values)),
        "std": float(np.std(dci_values)),
        "baseline": 25.0,
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "n_models": len(dci_values),
        "effect_size_d": float((np.mean(dci_values) - 25.0) / np.std(dci_values)) if np.std(dci_values) > 0 else 0,
    }


def test_h2(profiles: dict) -> dict:
    """H2: Convergent collapse — cosine similarity across model weight profiles."""
    vectors = []
    model_names = []
    for m, p in sorted(profiles.items()):
        if p["n_valid"] >= 3:
            vec = [p["mean_weights"][d] for d in DIMENSIONS]
            vectors.append(vec)
            model_names.append(m)

    if len(vectors) < 2:
        return {"supported": False, "reason": "insufficient data"}

    cosines = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            a, b = np.array(vectors[i]), np.array(vectors[j])
            cos = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
            cosines.append(cos)

    return {
        "supported": np.mean(cosines) >= 0.85,
        "mean_cosine": float(np.mean(cosines)),
        "min_cosine": float(np.min(cosines)),
        "max_cosine": float(np.max(cosines)),
        "std_cosine": float(np.std(cosines)),
        "n_pairs": len(cosines),
        "n_models": len(vectors),
        "threshold": 0.85,
    }


def test_h5_diagonal_advantage(calls: list[dict], profiles: dict) -> dict:
    """H5: Cultural training data advantage — diagonal of models x cultures matrix."""
    # Get cross-cultural calls only
    xc_calls = [c for c in calls
                if c.get("prompt_type") == "weighted_recommendation"
                and not c.get("error")
                and c.get("pair_id") in PAIR_CULTURE]

    # Compute per-model per-pair DCI
    model_pair_dcis = defaultdict(lambda: defaultdict(list))
    for c in xc_calls:
        parsed = c.get("parsed", {})
        w = parse_weights(parsed)
        if w:
            dci = compute_dci(w)
            model_pair_dcis[c["model"]][c["pair_id"]].append(dci)

    # Build diagonal advantage matrix: for each culture, compare
    # national model DCI vs non-national model DCI on that culture's brand
    results = {}
    for pair_id, culture in PAIR_CULTURE.items():
        national_models = CULTURE_MODELS.get(culture, [])
        national_dcis = []
        other_dcis = []

        for model, pair_data in model_pair_dcis.items():
            if pair_id in pair_data:
                mean_dci = np.mean(pair_data[pair_id])
                if model in national_models:
                    national_dcis.append(mean_dci)
                else:
                    other_dcis.append(mean_dci)

        if national_dcis and other_dcis:
            nat_mean = float(np.mean(national_dcis))
            oth_mean = float(np.mean(other_dcis))
            # H5: national should have LOWER DCI (less collapse)
            advantage = oth_mean - nat_mean
            # Welch's t-test
            if len(national_dcis) >= 2 and len(other_dcis) >= 2:
                t_stat, p_value = stats.ttest_ind(other_dcis, national_dcis, equal_var=False)
            else:
                t_stat, p_value = float("nan"), float("nan")

            results[pair_id] = {
                "culture": culture,
                "national_mean_dci": nat_mean,
                "other_mean_dci": oth_mean,
                "advantage": advantage,  # positive = national models collapse LESS
                "n_national": len(national_dcis),
                "n_other": len(other_dcis),
                "t_stat": float(t_stat) if not np.isnan(t_stat) else None,
                "p_value": float(p_value) if not np.isnan(p_value) else None,
            }

    # Overall: is the diagonal systematically lower?
    advantages = [r["advantage"] for r in results.values()]
    if advantages:
        mean_adv = float(np.mean(advantages))
        positive_count = sum(1 for a in advantages if a > 0)
        t_stat, p_value = stats.ttest_1samp(advantages, 0)
    else:
        mean_adv, positive_count = 0, 0
        t_stat, p_value = float("nan"), float("nan")

    return {
        "supported": mean_adv > 0 and (p_value < 0.05 if not np.isnan(p_value) else False),
        "mean_advantage": mean_adv,
        "positive_count": positive_count,
        "total_pairs": len(advantages),
        "t_stat": float(t_stat) if not np.isnan(t_stat) else None,
        "p_value": float(p_value) if not np.isnan(p_value) else None,
        "per_pair": results,
    }


def test_h9_capacity(calls: list[dict]) -> dict:
    """H9: Capacity-dependent collapse — smaller models higher DCI than larger."""
    xc_calls = [c for c in calls
                if c.get("prompt_type") == "weighted_recommendation"
                and not c.get("error")
                and c.get("pair_id") in PAIR_CULTURE]

    # Get per-model DCI on cross-cultural pairs
    model_dcis = defaultdict(list)
    for c in xc_calls:
        w = parse_weights(c.get("parsed", {}))
        if w:
            model_dcis[c["model"]].append(compute_dci(w))

    results = []
    for small, large, culture, label in CAPACITY_PAIRS:
        if small in model_dcis and large in model_dcis:
            small_dci = float(np.mean(model_dcis[small]))
            large_dci = float(np.mean(model_dcis[large]))
            diff = small_dci - large_dci  # positive = small has MORE collapse
            if len(model_dcis[small]) >= 2 and len(model_dcis[large]) >= 2:
                t_stat, p_value = stats.ttest_ind(model_dcis[small], model_dcis[large])
            else:
                t_stat, p_value = float("nan"), float("nan")
            results.append({
                "small_model": small,
                "large_model": large,
                "culture": culture,
                "label": label,
                "small_dci": small_dci,
                "large_dci": large_dci,
                "difference": diff,
                "small_higher": diff > 0,
                "t_stat": float(t_stat) if not np.isnan(t_stat) else None,
                "p_value": float(p_value) if not np.isnan(p_value) else None,
            })

    small_higher_count = sum(1 for r in results if r["small_higher"])
    return {
        "supported": small_higher_count > len(results) / 2 if results else False,
        "small_higher_count": small_higher_count,
        "total_pairs": len(results),
        "pairs": results,
    }


def test_h3_probe_variance(calls: list[dict]) -> dict:
    """H3: Cross-model probe variance higher on soft dims than hard dims."""
    probe_calls = [c for c in calls
                   if c.get("prompt_type") == "dimension_probe"
                   and not c.get("error")]

    # Collect scores per (brand, dimension) across models
    scores = defaultdict(lambda: defaultdict(list))
    for c in probe_calls:
        parsed = c.get("parsed") or {}
        score = parsed.get("score")
        if score is not None:
            try:
                scores[(c.get("brand", ""), c.get("dimension", ""))][c["model"]].append(float(score))
            except (ValueError, TypeError):
                pass

    # Compute cross-model variance per (brand, dimension)
    hard_vars = []
    soft_vars = []
    for (brand, dim), model_scores in scores.items():
        model_means = [np.mean(v) for v in model_scores.values() if len(v) > 0]
        if len(model_means) >= 3:
            var = float(np.var(model_means))
            if dim in HARD_DIMS:
                hard_vars.append(var)
            elif dim in SOFT_DIMS:
                soft_vars.append(var)

    if hard_vars and soft_vars:
        t_stat, p_value = stats.ttest_ind(soft_vars, hard_vars, alternative="greater")
        d = (np.mean(soft_vars) - np.mean(hard_vars)) / np.sqrt(
            (np.std(soft_vars)**2 + np.std(hard_vars)**2) / 2) if (np.std(soft_vars) + np.std(hard_vars)) > 0 else 0
    else:
        t_stat, p_value, d = float("nan"), float("nan"), 0

    return {
        "supported": p_value < 0.05 if not np.isnan(p_value) else False,
        "hard_mean_var": float(np.mean(hard_vars)) if hard_vars else 0,
        "soft_mean_var": float(np.mean(soft_vars)) if soft_vars else 0,
        "t_stat": float(t_stat) if not np.isnan(t_stat) else None,
        "p_value": float(p_value) if not np.isnan(p_value) else None,
        "effect_size_d": float(d),
        "n_hard": len(hard_vars),
        "n_soft": len(soft_vars),
    }


def test_h4_differentiation_gap(calls: list[dict]) -> dict:
    """H4: Soft-dim brand pairs show higher cross-model agreement on recommendation."""
    rec_calls = [c for c in calls
                 if c.get("prompt_type") == "weighted_recommendation"
                 and not c.get("error")]

    # Get recommended brand per model per pair
    pair_recs = defaultdict(lambda: defaultdict(list))
    for c in rec_calls:
        parsed = c.get("parsed") or {}
        rec = parsed.get("recommended_brand")
        if rec:
            pair_recs[c.get("pair_id", "")][c["model"]].append(rec)

    # Compute agreement rate per pair (fraction of models recommending the majority brand)
    pair_agreement = {}
    for pair_id, model_recs in pair_recs.items():
        all_recs = []
        for recs in model_recs.values():
            # Use the most common recommendation per model
            if recs:
                from collections import Counter
                most_common = Counter(recs).most_common(1)[0][0]
                all_recs.append(most_common)
        if len(all_recs) >= 3:
            from collections import Counter
            counts = Counter(all_recs)
            majority = counts.most_common(1)[0][1]
            agreement = majority / len(all_recs)
            pair_agreement[pair_id] = agreement

    # Note: we don't have pair dim_type in cross-cultural pairs (all soft)
    # Report as descriptive statistics
    return {
        "supported": None,  # descriptive only for cross-cultural
        "pair_agreement": pair_agreement,
        "mean_agreement": float(np.mean(list(pair_agreement.values()))) if pair_agreement else 0,
    }


def test_h6_bidirectional(calls: list[dict], profiles: dict) -> dict:
    """H6: Western models have lower DCI for Western brands than national models."""
    # Western brands in cross-cultural set: the 'b' brand in each pair (Evian, Lay's, etc.)
    # This tests whether Western models are better at global brands
    xc_rec = [c for c in calls
              if c.get("prompt_type") == "weighted_recommendation"
              and not c.get("error")
              and c.get("pair_id") in PAIR_CULTURE]

    western_models = CULTURE_MODELS.get("western", [])
    non_western_models = [m for culture, models in CULTURE_MODELS.items()
                          if culture != "western" for m in models]

    western_dcis = []
    nonwestern_dcis = []
    for c in xc_rec:
        w = parse_weights(c.get("parsed") or {})
        if w:
            dci = compute_dci(w)
            if c["model"] in western_models:
                western_dcis.append(dci)
            elif c["model"] in non_western_models:
                nonwestern_dcis.append(dci)

    if western_dcis and nonwestern_dcis:
        t_stat, p_value = stats.ttest_ind(western_dcis, nonwestern_dcis)
    else:
        t_stat, p_value = float("nan"), float("nan")

    return {
        "supported": np.mean(western_dcis) < np.mean(nonwestern_dcis) if western_dcis and nonwestern_dcis else False,
        "western_mean_dci": float(np.mean(western_dcis)) if western_dcis else 0,
        "nonwestern_mean_dci": float(np.mean(nonwestern_dcis)) if nonwestern_dcis else 0,
        "difference": float(np.mean(nonwestern_dcis) - np.mean(western_dcis)) if western_dcis and nonwestern_dcis else 0,
        "t_stat": float(t_stat) if not np.isnan(t_stat) else None,
        "p_value": float(p_value) if not np.isnan(p_value) else None,
        "n_western": len(western_dcis),
        "n_nonwestern": len(nonwestern_dcis),
    }


def test_h7_geopolitical(calls: list[dict]) -> dict:
    """H7: Geopolitical valence — VkusVill (Russia) vs Roshen (Ukraine) systematic differences."""
    xc_rec = [c for c in calls
              if c.get("prompt_type") == "weighted_recommendation"
              and not c.get("error")]

    russia_dcis = defaultdict(list)
    ukraine_dcis = defaultdict(list)
    for c in xc_rec:
        w = parse_weights(c.get("parsed") or {})
        if w:
            dci = compute_dci(w)
            if c.get("pair_id") == "russia_organic":
                russia_dcis[c["model"]].append(dci)
            elif c.get("pair_id") == "ukraine_confectionery":
                ukraine_dcis[c["model"]].append(dci)

    per_model = {}
    for model in set(list(russia_dcis.keys()) + list(ukraine_dcis.keys())):
        if model in russia_dcis and model in ukraine_dcis:
            r_mean = float(np.mean(russia_dcis[model]))
            u_mean = float(np.mean(ukraine_dcis[model]))
            per_model[model] = {
                "russia_dci": r_mean,
                "ukraine_dci": u_mean,
                "difference": r_mean - u_mean,
            }

    diffs = [v["difference"] for v in per_model.values()]
    return {
        "supported": None,  # exploratory, no directional prediction
        "mean_difference": float(np.mean(diffs)) if diffs else 0,
        "std_difference": float(np.std(diffs)) if diffs else 0,
        "models_russia_higher": sum(1 for d in diffs if d > 0),
        "models_ukraine_higher": sum(1 for d in diffs if d < 0),
        "total_models": len(diffs),
        "per_model": per_model,
    }


def test_h8_thindata_floor(calls: list[dict], profiles: dict) -> dict:
    """H8: APU Chinggis (Mongolia) has highest DCI across all models."""
    xc_rec = [c for c in calls
              if c.get("prompt_type") == "weighted_recommendation"
              and not c.get("error")
              and c.get("pair_id") in PAIR_CULTURE]

    pair_dcis = defaultdict(list)
    for c in xc_rec:
        w = parse_weights(c.get("parsed") or {})
        if w:
            pair_dcis[c.get("pair_id", "")].append(compute_dci(w))

    pair_means = {p: float(np.mean(v)) for p, v in pair_dcis.items() if v}
    mongolia_dci = pair_means.get("mongolia_beer", 0)
    max_pair = max(pair_means, key=pair_means.get) if pair_means else ""
    is_highest = max_pair == "mongolia_beer"

    return {
        "supported": is_highest,
        "mongolia_dci": mongolia_dci,
        "highest_pair": max_pair,
        "highest_dci": pair_means.get(max_pair, 0),
        "pair_dcis": pair_means,
    }


def test_run4_resolution(calls: list[dict]) -> dict:
    """Run 4 H5-H7: Brand Function specification resolution test."""
    run4_calls = [c for c in calls
                  if c.get("run_label", "").startswith("Run 4")
                  and c.get("prompt_type") == "weighted_recommendation"
                  and not c.get("error")]
    run3_calls = [c for c in calls
                  if c.get("run_label", "").startswith("Run 3")
                  and c.get("prompt_type") == "weighted_recommendation"
                  and not c.get("error")]

    def mean_dci(call_list):
        dcis = []
        for c in call_list:
            w = parse_weights(c.get("parsed") or {})
            if w:
                dcis.append(compute_dci(w))
        return float(np.mean(dcis)) if dcis else 0

    run3_dci = mean_dci(run3_calls)
    run4_dci = mean_dci(run4_calls)

    return {
        "run3_baseline_dci": run3_dci,
        "run4_spec_dci": run4_dci,
        "reduction": run3_dci - run4_dci,
        "n_run3": len(run3_calls),
        "n_run4": len(run4_calls),
    }


def test_h10_native_language(calls: list[dict]) -> dict:
    """H10: Native-language prompts reduce DCI for culture-matched models."""
    en_calls = [c for c in calls
                if c.get("prompt_type") == "weighted_recommendation"
                and not c.get("error")]
    native_calls = [c for c in calls
                    if c.get("prompt_type") == "weighted_recommendation_native"
                    and not c.get("error")]

    # Match: same model + same pair
    en_dcis = defaultdict(list)
    native_dcis = defaultdict(list)

    for c in en_calls:
        w = parse_weights(c.get("parsed", {}))
        if w:
            key = (c["model"], c.get("pair_id", ""))
            en_dcis[key].append(compute_dci(w))

    for c in native_calls:
        w = parse_weights(c.get("parsed", {}))
        if w:
            key = (c["model"], c.get("pair_id", ""))
            native_dcis[key].append(compute_dci(w))

    pairs = []
    for key in set(en_dcis.keys()) & set(native_dcis.keys()):
        en_mean = float(np.mean(en_dcis[key]))
        nat_mean = float(np.mean(native_dcis[key]))
        pairs.append({
            "model": key[0],
            "pair_id": key[1],
            "en_dci": en_mean,
            "native_dci": nat_mean,
            "reduction": en_mean - nat_mean,  # positive = native is LESS collapsed
        })

    if pairs:
        reductions = [p["reduction"] for p in pairs]
        mean_reduction = float(np.mean(reductions))
        positive_count = sum(1 for r in reductions if r > 0)
    else:
        mean_reduction = 0
        positive_count = 0

    return {
        "supported": mean_reduction > 0 and positive_count > len(pairs) / 2 if pairs else False,
        "mean_reduction": mean_reduction,
        "positive_count": positive_count,
        "total_pairs": len(pairs),
        "pairs": pairs,
    }


def compute_cost_summary(calls: list[dict]) -> dict:
    """Compute token estimates and cost per model."""
    CHARS_PER_TOKEN = 4.0
    PRICING = {
        "claude": (0.0008, 0.004), "gpt": (0.00015, 0.0006),
        "gemini": (0.0, 0.0), "deepseek": (0.00027, 0.0011),
        "grok": (0.003, 0.015), "yandexgpt_pro": (0.00984, 0.00984),
        "gptoss_swallow": (0.00082, 0.00082),
    }

    model_stats = defaultdict(lambda: {
        "calls_ok": 0, "calls_err": 0,
        "est_tokens": 0, "cost_usd": 0.0, "latency_ms": 0,
    })

    for c in calls:
        m = c.get("model", "?")
        s = model_stats[m]
        if c.get("error"):
            s["calls_err"] += 1
        else:
            s["calls_ok"] += 1
        prompt_len = len(c.get("prompt") or "") / CHARS_PER_TOKEN
        resp_len = len(c.get("response") or "") / CHARS_PER_TOKEN
        s["est_tokens"] += int(prompt_len + resp_len)
        s["latency_ms"] += c.get("latency_ms", 0) or 0
        pin, pout = PRICING.get(m, (0.0, 0.0))
        s["cost_usd"] += (prompt_len / 1000) * pin + (resp_len / 1000) * pout

    total_cost = sum(s["cost_usd"] for s in model_stats.values())
    total_tokens = sum(s["est_tokens"] for s in model_stats.values())
    total_ok = sum(s["calls_ok"] for s in model_stats.values())

    return {
        "total_cost_usd": round(total_cost, 2),
        "total_est_tokens": total_tokens,
        "total_calls_ok": total_ok,
        "total_calls": len(calls),
        "cost_per_call": round(total_cost / max(total_ok, 1), 5),
        "per_model": dict(model_stats),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="R15 Run 5 Cross-Cultural Analysis")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--format", choices=["markdown", "csv", "json"], default="markdown")
    args = parser.parse_args()

    base_dir = os.path.join(os.path.dirname(__file__), "..")
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading data...")
    all_calls = load_all_calls(base_dir)
    # Filter to successful calls with known models
    known_models = set(MODEL_META.keys())
    valid_calls = [c for c in all_calls if c.get("model") in known_models]
    xc_calls = [c for c in valid_calls if c.get("pair_id") in PAIR_CULTURE]

    print(f"Loaded {len(all_calls)} total calls, {len(valid_calls)} from known models, "
          f"{len(xc_calls)} cross-cultural")

    # --- Run all analyses ---
    print("\nComputing weight profiles...")
    profiles = analyze_weight_profiles(valid_calls)
    xc_profiles = analyze_weight_profiles(xc_calls)

    print("Testing H1 (over-weighting)...")
    h1 = test_h1(xc_profiles)

    print("Testing H2 (convergent collapse)...")
    h2 = test_h2(xc_profiles)

    print("Testing H3 (probe variance)...")
    h3 = test_h3_probe_variance(xc_calls)

    print("Testing H4 (differentiation gap)...")
    h4 = test_h4_differentiation_gap(xc_calls)

    print("Testing H5 (diagonal advantage)...")
    h5 = test_h5_diagonal_advantage(xc_calls, xc_profiles)

    print("Testing H6 (bidirectional asymmetry)...")
    h6 = test_h6_bidirectional(xc_calls, xc_profiles)

    print("Testing H7 (geopolitical valence)...")
    h7 = test_h7_geopolitical(xc_calls)

    print("Testing H8 (thin-data floor)...")
    h8 = test_h8_thindata_floor(xc_calls, xc_profiles)

    print("Testing H9 (capacity effect)...")
    h9 = test_h9_capacity(xc_calls)

    print("Testing H10 (native language)...")
    h10 = test_h10_native_language(xc_calls)

    print("Testing Run 4 resolution (H5r4-H7r4)...")
    run4 = test_run4_resolution(valid_calls)

    print("Computing cost summary...")
    costs = compute_cost_summary(all_calls)

    # --- Compile results ---
    results = {
        "metadata": {
            "total_calls": len(all_calls),
            "cross_cultural_calls": len(xc_calls),
            "models": len(profiles),
            "cultures": len(CULTURE_MODELS),
            "brand_pairs": len(PAIR_CULTURE),
            "total_cost_usd": costs["total_cost_usd"],
            "total_est_tokens": costs["total_est_tokens"],
        },
        "H1_overweighting": h1,
        "H2_convergent_collapse": h2,
        "H3_probe_variance": h3,
        "H4_differentiation_gap": h4,
        "H5_diagonal_advantage": h5,
        "H6_bidirectional_asymmetry": h6,
        "H7_geopolitical_valence": h7,
        "H8_thindata_floor": h8,
        "H9_capacity_effect": h9,
        "H10_native_language": h10,
        "Run4_resolution": run4,
        "model_profiles": {m: {
            "dci": p["dci"],
            "n_valid": p["n_valid"],
            "weights": p["mean_weights"],
            "tier": MODEL_META.get(m, {}).get("tier"),
            "culture": MODEL_META.get(m, {}).get("culture"),
        } for m, p in xc_profiles.items()},
    }

    # --- Output ---
    json_path = out_dir / "run5_analysis_results.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nJSON results: {json_path}")

    # Print summary
    print("\n" + "=" * 80)
    print("R15 RUN 5 CROSS-CULTURAL ANALYSIS RESULTS")
    print("=" * 80)

    print(f"\nDataset: {len(all_calls):,} calls, {costs['total_cost_usd']} USD, "
          f"~{costs['total_est_tokens']:,} tokens")

    print(f"\n--- H1 (Economic+Semiotic Over-Weighting) ---")
    print(f"  Mean DCI: {h1.get('mean', 0):.1f} vs baseline 25.0")
    print(f"  t={h1.get('t_stat', 0):.3f}, p={h1.get('p_value', 1):.6f}, d={h1.get('effect_size_d', 0):.3f}")
    print(f"  SUPPORTED: {h1['supported']}")

    print(f"\n--- H2 (Convergent Collapse) ---")
    print(f"  Mean cosine: {h2.get('mean_cosine', 0):.3f} (threshold >= 0.85)")
    print(f"  Range: [{h2.get('min_cosine', 0):.3f}, {h2.get('max_cosine', 0):.3f}]")
    print(f"  SUPPORTED: {h2['supported']}")

    print(f"\n--- H3 (Differential Probe Variance) ---")
    print(f"  Hard dim mean variance: {h3.get('hard_mean_var', 0):.4f}")
    print(f"  Soft dim mean variance: {h3.get('soft_mean_var', 0):.4f}")
    if h3.get("t_stat"):
        print(f"  t={h3['t_stat']:.3f}, p={h3['p_value']:.4f}, d={h3.get('effect_size_d', 0):.3f}")
    print(f"  SUPPORTED: {h3['supported']}")

    print(f"\n--- H4 (Cross-Model Recommendation Agreement) ---")
    print(f"  Mean agreement rate: {h4.get('mean_agreement', 0):.3f}")
    for pair_id, agree in sorted(h4.get("pair_agreement", {}).items()):
        print(f"    {pair_id}: {agree:.3f}")

    print(f"\n--- H5 (Cultural Training Data Advantage) ---")
    print(f"  Mean diagonal advantage: {h5.get('mean_advantage', 0):+.4f}")
    print(f"  Positive (national < other DCI): {h5.get('positive_count', 0)}/{h5.get('total_pairs', 0)}")
    if h5.get("p_value"):
        print(f"  t={h5['t_stat']:.3f}, p={h5['p_value']:.4f}")
    print(f"  SUPPORTED: {h5['supported']}")
    for pair_id, r in sorted(h5.get("per_pair", {}).items()):
        arrow = "<" if r["advantage"] > 0 else ">"
        print(f"    {pair_id}: national={r['national_mean_dci']:.3f} {arrow} other={r['other_mean_dci']:.3f} "
              f"(adv={r['advantage']:+.4f}, n={r['n_national']}+{r['n_other']})")

    print(f"\n--- H6 (Bidirectional Asymmetry) ---")
    print(f"  Western models mean DCI: {h6.get('western_mean_dci', 0):.3f}")
    print(f"  Non-Western models mean DCI: {h6.get('nonwestern_mean_dci', 0):.3f}")
    print(f"  Difference: {h6.get('difference', 0):+.4f}")
    if h6.get("t_stat"):
        print(f"  t={h6['t_stat']:.3f}, p={h6['p_value']:.4f}")
    print(f"  SUPPORTED: {h6['supported']}")

    print(f"\n--- H7 (Geopolitical Valence — VkusVill vs Roshen) ---")
    print(f"  Mean Russia-Ukraine DCI difference: {h7.get('mean_difference', 0):+.4f}")
    print(f"  Models with Russia higher DCI: {h7.get('models_russia_higher', 0)}")
    print(f"  Models with Ukraine higher DCI: {h7.get('models_ukraine_higher', 0)}")
    print(f"  EXPLORATORY (no directional prediction)")
    for m, v in sorted(h7.get("per_model", {}).items()):
        print(f"    {m:<22} RU={v['russia_dci']:.3f} UA={v['ukraine_dci']:.3f} diff={v['difference']:+.4f}")

    print(f"\n--- H8 (Thin-Data Floor — Mongolia) ---")
    print(f"  Mongolia DCI: {h8.get('mongolia_dci', 0):.3f}")
    print(f"  Highest pair: {h8.get('highest_pair', '')} (DCI={h8.get('highest_dci', 0):.3f})")
    print(f"  SUPPORTED: {h8['supported']}")
    for p, d in sorted(h8.get("pair_dcis", {}).items(), key=lambda x: -x[1]):
        marker = " <-- HIGHEST" if p == h8.get("highest_pair") else ""
        print(f"    {p}: {d:.3f}{marker}")

    print(f"\n--- Run 4 (Brand Function Resolution) ---")
    print(f"  Run 3 baseline DCI: {run4.get('run3_baseline_dci', 0):.3f}")
    print(f"  Run 4 with spec DCI: {run4.get('run4_spec_dci', 0):.3f}")
    print(f"  Reduction: {run4.get('reduction', 0):+.4f}")

    print(f"\n--- H9 (Capacity-Dependent Collapse) ---")
    print(f"  Small > Large DCI: {h9.get('small_higher_count', 0)}/{h9.get('total_pairs', 0)}")
    print(f"  SUPPORTED: {h9['supported']}")
    for p in h9.get("pairs", []):
        arrow = ">" if p["small_higher"] else "<"
        print(f"    {p['label']} ({p['culture']}): {p['small_model']}={p['small_dci']:.3f} "
              f"{arrow} {p['large_model']}={p['large_dci']:.3f} (diff={p['difference']:+.4f})")

    print(f"\n--- H10 (Native Language Effect) ---")
    print(f"  Mean DCI reduction: {h10.get('mean_reduction', 0):+.4f}")
    print(f"  Positive (native < English): {h10.get('positive_count', 0)}/{h10.get('total_pairs', 0)}")
    print(f"  SUPPORTED: {h10['supported']}")
    for p in h10.get("pairs", []):
        print(f"    {p['model']} on {p['pair_id']}: en={p['en_dci']:.3f} native={p['native_dci']:.3f} "
              f"(reduction={p['reduction']:+.4f})")

    print(f"\n--- DCI Ranking (Cross-Cultural, all models) ---")
    for m, p in sorted(xc_profiles.items(), key=lambda x: x[1]["dci"]):
        meta = MODEL_META.get(m, {})
        tier = meta.get("tier", "?")
        culture = meta.get("culture", "?")
        print(f"  {m:<22} DCI={p['dci']:.3f}  T{tier} {culture:<10} n={p['n_valid']}")

    # Save DCI table as CSV
    csv_path = out_dir / "run5_dci_table.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "dci", "tier", "culture", "size", "release", "provider",
                     "n_valid"] + [f"weight_{d}" for d in DIMENSIONS])
        for m, p in sorted(xc_profiles.items(), key=lambda x: x[1]["dci"]):
            meta = MODEL_META.get(m, {})
            w.writerow([m, round(p["dci"], 4), meta.get("tier"), meta.get("culture"),
                        meta.get("size"), meta.get("release"), meta.get("provider"),
                        p["n_valid"]] + [round(p["mean_weights"].get(d, 0), 1) for d in DIMENSIONS])
    print(f"\nDCI table CSV: {csv_path}")

    # Save diagonal advantage as CSV
    diag_path = out_dir / "run5_diagonal_advantage.csv"
    with open(diag_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pair_id", "culture", "national_mean_dci", "other_mean_dci",
                     "advantage", "n_national", "n_other", "t_stat", "p_value"])
        for pair_id, r in sorted(h5.get("per_pair", {}).items()):
            w.writerow([pair_id, r["culture"], round(r["national_mean_dci"], 4),
                        round(r["other_mean_dci"], 4), round(r["advantage"], 4),
                        r["n_national"], r["n_other"], r.get("t_stat"), r.get("p_value")])
    print(f"Diagonal advantage CSV: {diag_path}")

    print(f"\nAnalysis complete.")


if __name__ == "__main__":
    main()
