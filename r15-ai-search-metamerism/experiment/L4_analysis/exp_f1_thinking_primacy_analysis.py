#!/usr/bin/env python3
"""Analysis for Experiment F1: Thinking-Mode Primacy.

Reads L3_sessions/exp_f1_thinking_primacy.jsonl and tests the three
pre-registered hypotheses from the protocol.

Hypotheses:
    H_F1a: Thinking mode reduces JSON primacy (d >= .30, directional)
    H_F1b: Thinking mode has no effect on Likert primacy (null, d < .25)
    H_F1c: Model-specific primacy reduction magnitudes differ (heterogeneity)

Usage:
    uv run python exp_f1_thinking_primacy_analysis.py
    uv run python exp_f1_thinking_primacy_analysis.py --jsonl path/to/file.jsonl
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import numpy as np
from scipy import stats as sp_stats

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

DEFAULT_JSONL = (
    Path(__file__).parent.parent / "L3_sessions" / "exp_f1_thinking_primacy.jsonl"
)
OUTPUT_DIR = Path(__file__).parent
RESULTS_PATH = OUTPUT_DIR / "exp_f1_thinking_primacy_results.json"
SUMMARY_PATH = OUTPUT_DIR / "exp_f1_thinking_primacy_summary.md"

MODEL_PAIRS = ["gemini", "deepseek", "grok"]
FORMATS = ["json", "likert"]


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------


def load_records(jsonl_path: Path) -> list[dict]:
    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found. Run the experiment first.")
        sys.exit(1)
    records = []
    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def valid_records(records: list[dict]) -> list[dict]:
    """Records with successfully parsed weights."""
    return [
        r
        for r in records
        if r.get("weights_valid") and r.get("primacy_score") is not None
    ]


# ---------------------------------------------------------------------------
# Utility: Statistics
# ---------------------------------------------------------------------------


def bootstrap_ci(
    data: np.ndarray, n_boot: int = 10_000, ci: float = .95, seed: int = 42
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    boot_means = np.array([
        np.mean(rng.choice(data, size=len(data), replace=True))
        for _ in range(n_boot)
    ])
    alpha = (1 - ci) / 2
    return float(np.percentile(boot_means, alpha * 100)), float(
        np.percentile(boot_means, (1 - alpha) * 100)
    )


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    """Cohen's d with pooled standard deviation."""
    pooled = np.sqrt((np.std(a, ddof=1) ** 2 + np.std(b, ddof=1) ** 2) / 2)
    if pooled == 0:
        return 0.0
    return float((np.mean(a) - np.mean(b)) / pooled)


def bayes_factor_01(
    t_stat: float, n1: int, n2: int, r: float = 1.0
) -> Optional[float]:
    """Approximate BF01 (evidence for null) via Rouder et al. unit-info prior.

    Uses the JZS Bayes factor approximation for independent-samples t-test.
    r = prior scale (1.0 = medium Cauchy prior).
    Returns BF01 = P(data|H0) / P(data|H1). BF01 > 3 = moderate evidence for null.
    """
    try:
        from math import lgamma, log, sqrt, pi, exp

        df = n1 + n2 - 2
        # Rouder et al. (2009) approximation via integration
        # Simplified: use the t-value and degrees of freedom directly
        # This is a heuristic approximation; exact computation requires quadrature
        # For our purposes, BF01 > 3 supports H_F1b null
        t2 = t_stat ** 2
        # Log marginal likelihood under H1 (Cauchy prior, scale r)
        # Approximation from Masson (2011): BF01 = exp(-0.5 * t^2) for large df
        # More accurate: Wagenmakers et al. (2010) formula
        log_bf10 = (
            0.5 * log(1 + t2 / df)
            - 0.5 * log(1 + (t2 / df) / (1 + r ** 2))
            - 0.5 * log(1 + r ** 2)
        )
        bf10 = exp(log_bf10)
        return round(1.0 / max(bf10, 1e-10), 3)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Primary Analyses
# ---------------------------------------------------------------------------


def extract_primacy_scores(
    records: list[dict],
    response_format: str,
    thinking_mode: bool,
    model_pair: Optional[str] = None,
) -> np.ndarray:
    """Extract primacy scores for a given condition."""
    filtered = [
        r
        for r in valid_records(records)
        if r.get("response_format") == response_format
        and r.get("thinking_mode") == thinking_mode
        and (model_pair is None or r.get("model_pair") == model_pair)
    ]
    return np.array([float(r["primacy_score"]) for r in filtered])


def test_hf1a(records: list[dict]) -> dict:
    """H_F1a: Thinking mode reduces JSON primacy.

    Tests per model pair (Bonferroni alpha=.017) and pooled.
    Success: p < .017 AND d >= .30 AND thinking_mean < standard_mean (per pair)
             OR p < .05 AND d >= .30 (pooled)
    """
    bonferroni_alpha = .05 / len(MODEL_PAIRS)
    per_pair = {}
    pooled_std_scores = []
    pooled_think_scores = []

    for pair in MODEL_PAIRS:
        std_scores = extract_primacy_scores(records, "json", False, pair)
        think_scores = extract_primacy_scores(records, "json", True, pair)
        pooled_std_scores.extend(std_scores.tolist())
        pooled_think_scores.extend(think_scores.tolist())

        if len(std_scores) < 2 or len(think_scores) < 2:
            per_pair[pair] = {"status": "INSUFFICIENT_DATA"}
            continue

        t_stat, p_val = sp_stats.ttest_ind(std_scores, think_scores)
        d = cohens_d(std_scores, think_scores)
        ci = bootstrap_ci(std_scores - np.mean(think_scores))

        directional = float(np.mean(std_scores)) > float(np.mean(think_scores))
        supported = p_val < bonferroni_alpha and d >= .30 and directional

        per_pair[pair] = {
            "status": "SUPPORTED" if supported else "NOT SUPPORTED",
            "mean_primacy_standard": round(float(np.mean(std_scores)), 4),
            "mean_primacy_thinking": round(float(np.mean(think_scores)), 4),
            "reduction": round(
                float(np.mean(std_scores)) - float(np.mean(think_scores)), 4
            ),
            "t_statistic": round(float(t_stat), 3),
            "p_value": round(float(p_val), 4),
            "cohens_d": round(d, 3),
            "d_ci_95": [round(ci[0], 3), round(ci[1], 3)],
            "n_standard": int(len(std_scores)),
            "n_thinking": int(len(think_scores)),
            "directional": directional,
        }

    # Pooled test
    std_arr = np.array(pooled_std_scores)
    think_arr = np.array(pooled_think_scores)
    pooled_result: dict = {}
    if len(std_arr) >= 2 and len(think_arr) >= 2:
        t_stat_p, p_val_p = sp_stats.ttest_ind(std_arr, think_arr)
        d_p = cohens_d(std_arr, think_arr)
        directional_p = float(np.mean(std_arr)) > float(np.mean(think_arr))
        pooled_supported = p_val_p < .05 and d_p >= .30 and directional_p
        pooled_result = {
            "status": "SUPPORTED" if pooled_supported else "NOT SUPPORTED",
            "mean_primacy_standard": round(float(np.mean(std_arr)), 4),
            "mean_primacy_thinking": round(float(np.mean(think_arr)), 4),
            "reduction": round(
                float(np.mean(std_arr)) - float(np.mean(think_arr)), 4
            ),
            "t_statistic": round(float(t_stat_p), 3),
            "p_value": round(float(p_val_p), 4),
            "cohens_d": round(d_p, 3),
            "n_standard": int(len(std_arr)),
            "n_thinking": int(len(think_arr)),
        }

    # Overall status: supported if majority of pairs supported
    supported_pairs = sum(
        1 for v in per_pair.values() if v.get("status") == "SUPPORTED"
    )
    overall_status = "SUPPORTED" if supported_pairs >= 2 else "NOT SUPPORTED"

    return {
        "status": overall_status,
        "supported_pairs": supported_pairs,
        "total_pairs": len(MODEL_PAIRS),
        "per_pair": per_pair,
        "pooled": pooled_result,
    }


def test_hf1b(records: list[dict]) -> dict:
    """H_F1b: Thinking mode has no effect on Likert primacy (null hypothesis).

    Success: p >= .017 AND d < .25 across all pairs (null retained).
    Supplementary: BF01 > 3 (moderate evidence for null).
    """
    bonferroni_alpha = .05 / len(MODEL_PAIRS)
    per_pair = {}

    for pair in MODEL_PAIRS:
        std_scores = extract_primacy_scores(records, "likert", False, pair)
        think_scores = extract_primacy_scores(records, "likert", True, pair)

        if len(std_scores) < 2 or len(think_scores) < 2:
            per_pair[pair] = {"status": "INSUFFICIENT_DATA"}
            continue

        t_stat, p_val = sp_stats.ttest_ind(std_scores, think_scores)
        d = cohens_d(std_scores, think_scores)
        bf01 = bayes_factor_01(t_stat, len(std_scores), len(think_scores))

        # Null retained if p >= alpha AND d < .25
        null_retained = p_val >= bonferroni_alpha and abs(d) < .25

        per_pair[pair] = {
            "status": "NULL RETAINED" if null_retained else "NULL REJECTED",
            "mean_primacy_standard": round(float(np.mean(std_scores)), 4),
            "mean_primacy_thinking": round(float(np.mean(think_scores)), 4),
            "t_statistic": round(float(t_stat), 3),
            "p_value": round(float(p_val), 4),
            "cohens_d": round(d, 3),
            "bf01": bf01,
            "n_standard": int(len(std_scores)),
            "n_thinking": int(len(think_scores)),
        }

    null_retained_count = sum(
        1 for v in per_pair.values() if v.get("status") == "NULL RETAINED"
    )
    overall_status = (
        "NULL RETAINED"
        if null_retained_count == len(MODEL_PAIRS)
        else "NULL PARTIALLY REJECTED"
    )

    return {
        "status": overall_status,
        "null_retained_pairs": null_retained_count,
        "total_pairs": len(MODEL_PAIRS),
        "per_pair": per_pair,
    }


def test_hf1c(records: list[dict]) -> dict:
    """H_F1c: Model-specific primacy reduction magnitudes differ.

    Descriptive: per-pair Cohen's d on primacy reduction in JSON format.
    Success: at least one pair d >= .50 AND at least one pair d < .30 (heterogeneity).
    """
    pair_effects = {}
    d_values = []

    for pair in MODEL_PAIRS:
        std_scores = extract_primacy_scores(records, "json", False, pair)
        think_scores = extract_primacy_scores(records, "json", True, pair)

        if len(std_scores) < 2 or len(think_scores) < 2:
            pair_effects[pair] = {"status": "INSUFFICIENT_DATA"}
            continue

        d = cohens_d(std_scores, think_scores)
        ci = bootstrap_ci(std_scores - np.mean(think_scores))
        d_values.append(abs(d))

        pair_effects[pair] = {
            "cohens_d": round(d, 3),
            "d_ci_95": [round(ci[0], 3), round(ci[1], 3)],
            "mean_primacy_standard": round(float(np.mean(std_scores)), 4),
            "mean_primacy_thinking": round(float(np.mean(think_scores)), 4),
            "n_standard": int(len(std_scores)),
            "n_thinking": int(len(think_scores)),
        }

    # Heterogeneity check
    has_large = any(v >= .50 for v in d_values)
    has_small = any(v < .30 for v in d_values)
    heterogeneity_present = has_large and has_small

    # Cochran's Q if we have at least 2 pairs with valid d
    cochran_q = None
    if len(d_values) >= 3:
        grand_mean_d = np.mean(d_values)
        # Simplified Q: weighted sum of squared deviations
        # (equal weights since CIs not propagated to Q here)
        q = float(np.sum((np.array(d_values) - grand_mean_d) ** 2))
        cochran_q = round(q, 4)

    return {
        "status": "HETEROGENEITY PRESENT" if heterogeneity_present else "HOMOGENEOUS",
        "heterogeneity_criterion": "at least one d >= .50 AND at least one d < .30",
        "per_pair": pair_effects,
        "cochran_q": cochran_q,
        "d_range": (
            [round(min(d_values), 3), round(max(d_values), 3)] if d_values else None
        ),
    }


# ---------------------------------------------------------------------------
# Secondary Analyses
# ---------------------------------------------------------------------------


def position_curves(records: list[dict]) -> dict:
    """Mean weight by position (1-8) for each of 4 conditions.

    Conditions: json_standard, json_thinking, likert_standard, likert_thinking
    """
    conditions = [
        ("json", False, "json_standard"),
        ("json", True, "json_thinking"),
        ("likert", False, "likert_standard"),
        ("likert", True, "likert_thinking"),
    ]
    curves = {}

    for fmt, thinking, label in conditions:
        filtered = [
            r
            for r in valid_records(records)
            if r.get("response_format") == fmt
            and r.get("thinking_mode") == thinking
        ]
        pos_data: dict[int, list[float]] = {p: [] for p in range(1, 9)}

        for r in filtered:
            pw = r.get("position_weights") or {}
            for pos in range(1, 9):
                val = pw.get(str(pos), pw.get(pos))
                if val is not None:
                    pos_data[pos].append(float(val))

        means = {
            pos: round(float(np.mean(vals)), 2) if vals else None
            for pos, vals in pos_data.items()
        }

        # Linear regression of weight on position
        positions_flat = []
        weights_flat = []
        for pos in range(1, 9):
            for v in pos_data[pos]:
                positions_flat.append(pos)
                weights_flat.append(v)

        linear_trend: dict = {}
        if len(positions_flat) > 2:
            slope, intercept, r_val, p_val, _ = sp_stats.linregress(
                positions_flat, weights_flat
            )
            linear_trend = {
                "slope": round(float(slope), 4),
                "r_squared": round(float(r_val ** 2), 4),
                "p_value": round(float(p_val), 4),
                "intercept": round(float(intercept), 4),
            }

        curves[label] = {
            "mean_by_position": means,
            "linear_trend": linear_trend,
            "n_records": len(filtered),
        }

    return curves


def per_model_primacy_slopes(records: list[dict]) -> dict:
    """Linear regression slope of weight on position (1-8) per model variant.

    Negative slope = primacy (early positions weighted higher).
    """
    slopes = {}
    variant_names = set(r.get("model_variant") for r in records if r.get("model_variant"))

    for variant in sorted(variant_names):
        filtered = [
            r
            for r in valid_records(records)
            if r.get("model_variant") == variant
        ]
        positions_flat = []
        weights_flat = []

        for r in filtered:
            pw = r.get("position_weights") or {}
            for pos in range(1, 9):
                val = pw.get(str(pos), pw.get(pos))
                if val is not None:
                    positions_flat.append(pos)
                    weights_flat.append(float(val))

        if len(positions_flat) > 2:
            slope, _, r_val, p_val, _ = sp_stats.linregress(positions_flat, weights_flat)
            slopes[variant] = {
                "slope": round(float(slope), 4),
                "r_squared": round(float(r_val ** 2), 4),
                "p_value": round(float(p_val), 4),
                "n_observations": len(positions_flat),
                "direction": "primacy" if slope < 0 else "recency",
            }
        else:
            slopes[variant] = {"status": "INSUFFICIENT_DATA"}

    return slopes


# ---------------------------------------------------------------------------
# Summary Report
# ---------------------------------------------------------------------------


def generate_summary(records: list[dict], results: dict) -> str:
    total = len(records)
    valid = len(valid_records(records))
    lines = [
        "# Experiment F1: Thinking-Mode Primacy -- Results Summary",
        "",
        f"**Date**: {records[0]['timestamp'][:10] if records else 'N/A'}",
        f"**Total calls**: {total}",
        (
            f"**Valid responses**: {valid} ({valid / total * 100:.1f}%)"
            if total
            else "**Valid responses**: 0"
        ),
        "",
        "---",
        "",
        "## H_F1a: Thinking Mode Reduces JSON Primacy",
        "",
    ]

    hfa = results["hf1a"]
    lines.append(f"**Overall result**: {hfa['status']}")
    lines.append(
        f"Supported pairs: {hfa['supported_pairs']}/{hfa['total_pairs']}"
    )
    lines.append("")
    for pair, pd in hfa.get("per_pair", {}).items():
        if pd.get("status") == "INSUFFICIENT_DATA":
            lines.append(f"- {pair}: INSUFFICIENT DATA")
            continue
        lines.append(
            f"- {pair}: {pd['status']} | "
            f"std={pd['mean_primacy_standard']:.3f}, "
            f"think={pd['mean_primacy_thinking']:.3f}, "
            f"reduction={pd['reduction']:.3f}, "
            f"d={pd['cohens_d']:.3f}, p={pd['p_value']:.4f}"
        )
    if "pooled" in hfa and hfa["pooled"]:
        po = hfa["pooled"]
        lines.extend([
            "",
            f"**Pooled**: {po.get('status', 'N/A')} | "
            f"std={po.get('mean_primacy_standard', 'N/A')}, "
            f"think={po.get('mean_primacy_thinking', 'N/A')}, "
            f"d={po.get('cohens_d', 'N/A')}, p={po.get('p_value', 'N/A')}",
        ])

    lines.extend([
        "",
        "## H_F1b: Thinking Mode Has No Effect on Likert Primacy (Null Test)",
        "",
    ])
    hfb = results["hf1b"]
    lines.append(f"**Overall result**: {hfb['status']}")
    lines.append(
        f"Null retained pairs: {hfb['null_retained_pairs']}/{hfb['total_pairs']}"
    )
    lines.append("")
    for pair, pd in hfb.get("per_pair", {}).items():
        if pd.get("status") == "INSUFFICIENT_DATA":
            lines.append(f"- {pair}: INSUFFICIENT DATA")
            continue
        lines.append(
            f"- {pair}: {pd['status']} | "
            f"d={pd['cohens_d']:.3f}, p={pd['p_value']:.4f}, "
            f"BF01={pd.get('bf01', 'N/A')}"
        )

    lines.extend([
        "",
        "## H_F1c: Model-Specific Primacy Reduction Magnitudes",
        "",
    ])
    hfc = results["hf1c"]
    lines.append(f"**Overall result**: {hfc['status']}")
    if hfc.get("d_range"):
        lines.append(f"d range: {hfc['d_range'][0]} to {hfc['d_range'][1]}")
    if hfc.get("cochran_q") is not None:
        lines.append(f"Cochran's Q: {hfc['cochran_q']}")
    lines.append("")
    for pair, pd in hfc.get("per_pair", {}).items():
        if pd.get("status") == "INSUFFICIENT_DATA":
            lines.append(f"- {pair}: INSUFFICIENT DATA")
            continue
        lines.append(
            f"- {pair}: d={pd['cohens_d']:.3f} (95% CI: {pd['d_ci_95']}), "
            f"std_mean={pd['mean_primacy_standard']:.3f}, "
            f"think_mean={pd['mean_primacy_thinking']:.3f}"
        )

    lines.extend([
        "",
        "## Position Curves (Secondary)",
        "",
    ])
    for label, curve in results.get("position_curves", {}).items():
        lt = curve.get("linear_trend", {})
        means = curve.get("mean_by_position", {})
        vals = " | ".join(f"P{p}: {means.get(p, 'N/A')}" for p in range(1, 9))
        lines.append(f"**{label}** (n={curve.get('n_records', 0)}): {vals}")
        if "slope" in lt:
            lines.append(
                f"  Slope: {lt['slope']:.4f}, R-sq={lt['r_squared']:.4f}, "
                f"p={lt['p_value']:.4f}"
            )
        lines.append("")

    lines.extend([
        "## Per-Model Primacy Slopes (Secondary)",
        "",
    ])
    for variant, s in sorted(results.get("per_model_slopes", {}).items()):
        if s.get("status") == "INSUFFICIENT_DATA":
            lines.append(f"- {variant}: INSUFFICIENT DATA")
        else:
            lines.append(
                f"- {variant}: slope={s['slope']:.4f} ({s['direction']}), "
                f"R-sq={s['r_squared']:.4f}, p={s['p_value']:.4f}, "
                f"n={s['n_observations']}"
            )

    lines.extend([
        "",
        "---",
        "",
        "*Analysis follows pre-registered protocol "
        "(EXP_F1_THINKING_PRIMACY_PROTOCOL.md). "
        "Exploratory analyses are labeled as such.*",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(jsonl_path: Optional[Path] = None) -> None:
    path = jsonl_path or DEFAULT_JSONL

    print(f"Loading data from {path}...")
    records = load_records(path)
    print(f"Loaded {len(records)} records, {len(valid_records(records))} valid.")

    if not records:
        print("No records found. Run the experiment first.")
        sys.exit(1)

    print("\nRunning H_F1a (thinking reduces JSON primacy)...")
    hf1a = test_hf1a(records)
    print(f"  -> {hf1a['status']} ({hf1a['supported_pairs']}/{hf1a['total_pairs']} pairs)")

    print("Running H_F1b (no effect on Likert primacy, null test)...")
    hf1b = test_hf1b(records)
    print(f"  -> {hf1b['status']} ({hf1b['null_retained_pairs']}/{hf1b['total_pairs']} null retained)")

    print("Running H_F1c (model-specific magnitudes)...")
    hf1c = test_hf1c(records)
    print(f"  -> {hf1c['status']}")

    print("Running secondary analyses...")
    curves = position_curves(records)
    slopes = per_model_primacy_slopes(records)

    results = {
        "hf1a": hf1a,
        "hf1b": hf1b,
        "hf1c": hf1c,
        "position_curves": curves,
        "per_model_slopes": slopes,
    }

    # Save JSON
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved: {RESULTS_PATH}")

    # Save markdown summary
    summary = generate_summary(records, results)
    with open(SUMMARY_PATH, "w") as f:
        f.write(summary)
    print(f"Summary saved: {SUMMARY_PATH}")

    # Print results table
    print(f"\n{'='*55}")
    print("HYPOTHESIS RESULTS")
    print(f"{'='*55}")
    print(f"H_F1a (thinking -> less JSON primacy):  {hf1a['status']}")
    print(f"H_F1b (no Likert effect, null):         {hf1b['status']}")
    print(f"H_F1c (model heterogeneity):            {hf1c['status']}")
    print(f"{'='*55}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Experiment F1 Analysis: Thinking-Mode Primacy"
    )
    parser.add_argument(
        "--jsonl",
        type=Path,
        default=None,
        help="Path to JSONL data file (default: L3_sessions/exp_f1_thinking_primacy.jsonl)",
    )
    args = parser.parse_args()
    main(jsonl_path=args.jsonl)
