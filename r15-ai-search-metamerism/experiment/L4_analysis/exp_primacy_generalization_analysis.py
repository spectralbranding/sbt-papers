#!/usr/bin/env python3
"""Analysis for Experiment E: Primacy Effect Generalization.

Reads L3_sessions/exp_primacy_generalization.jsonl and tests all
pre-registered hypotheses from the protocol.

Usage:
    uv run python exp_primacy_generalization_analysis.py
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats as sp_stats

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

JSONL_PATH = (
    Path(__file__).parent.parent / "L3_sessions" / "exp_primacy_generalization.jsonl"
)
OUTPUT_DIR = Path(__file__).parent
SUMMARY_PATH = OUTPUT_DIR / "exp_primacy_generalization_summary.md"

DIMENSIONS = [
    "Semiotic", "Narrative", "Ideological", "Experiential",
    "Social", "Economic", "Cultural", "Temporal",
]

FORMATS = ["json", "likert", "ranking", "nl"]


def load_records() -> list[dict]:
    if not JSONL_PATH.exists():
        print(f"ERROR: {JSONL_PATH} not found.")
        sys.exit(1)
    records = []
    with open(JSONL_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def valid_records(records: list[dict]) -> list[dict]:
    return [r for r in records if r.get("weights_valid") and r.get("position_weights")]


# ---------------------------------------------------------------------------
# Bootstrap CI
# ---------------------------------------------------------------------------


def bootstrap_ci(data: np.ndarray, n_boot: int = 10000, ci: float = .95, seed: int = 42) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    boot_means = np.array([
        np.mean(rng.choice(data, size=len(data), replace=True))
        for _ in range(n_boot)
    ])
    alpha = (1 - ci) / 2
    return float(np.percentile(boot_means, alpha * 100)), float(np.percentile(boot_means, (1 - alpha) * 100))


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    pooled_std = np.sqrt((np.std(a, ddof=1)**2 + np.std(b, ddof=1)**2) / 2)
    if pooled_std == 0:
        return 0.0
    return float((np.mean(a) - np.mean(b)) / pooled_std)


# ---------------------------------------------------------------------------
# Primary analyses
# ---------------------------------------------------------------------------


def extract_position_arrays(records: list[dict], fmt: str) -> dict[int, list[float]]:
    """Extract weight at each position (1-8) for a given format."""
    pos_data = {p: [] for p in range(1, 9)}
    for r in records:
        if r.get("response_format") != fmt:
            continue
        pw = r.get("position_weights")
        if pw is None:
            continue
        for pos in range(1, 9):
            key = str(pos) if str(pos) in pw else pos
            val = pw.get(key, pw.get(str(key)))
            if val is not None:
                pos_data[pos].append(float(val))
    return pos_data


def test_h1(records: list[dict]) -> dict:
    """H1: Primacy effect in JSON format (positions 1-2 vs 7-8)."""
    pos_data = extract_position_arrays(records, "json")
    early = np.array(pos_data[1] + pos_data[2])
    late = np.array(pos_data[7] + pos_data[8])

    if len(early) < 2 or len(late) < 2:
        return {"status": "INSUFFICIENT_DATA", "n_early": len(early), "n_late": len(late)}

    t_stat, p_val = sp_stats.ttest_ind(early, late)
    d = cohens_d(early, late)
    d_ci = bootstrap_ci(early - np.mean(late))

    supported = p_val < .05 and abs(d) >= .30
    return {
        "status": "SUPPORTED" if supported else "NOT SUPPORTED",
        "mean_pos_1_2": round(float(np.mean(early)), 2),
        "mean_pos_7_8": round(float(np.mean(late)), 2),
        "difference": round(float(np.mean(early) - np.mean(late)), 2),
        "t_statistic": round(float(t_stat), 3),
        "p_value": round(float(p_val), 3),
        "cohens_d": round(d, 3),
        "d_ci_95": [round(d_ci[0], 3), round(d_ci[1], 3)],
        "n_early": len(early),
        "n_late": len(late),
    }


def test_h2(records: list[dict]) -> dict:
    """H2: Primacy generalizes across formats (Bonferroni alpha = .0125)."""
    results = {}
    sig_count = 0
    bonferroni_alpha = .0125

    for fmt in FORMATS:
        pos_data = extract_position_arrays(records, fmt)
        early = np.array(pos_data[1] + pos_data[2])
        late = np.array(pos_data[7] + pos_data[8])

        if len(early) < 2 or len(late) < 2:
            results[fmt] = {"status": "INSUFFICIENT_DATA"}
            continue

        t_stat, p_val = sp_stats.ttest_ind(early, late)
        d = cohens_d(early, late)
        sig = p_val < bonferroni_alpha

        if sig:
            sig_count += 1

        results[fmt] = {
            "mean_pos_1_2": round(float(np.mean(early)), 2),
            "mean_pos_7_8": round(float(np.mean(late)), 2),
            "difference": round(float(np.mean(early) - np.mean(late)), 2),
            "t_statistic": round(float(t_stat), 3),
            "p_value": round(float(p_val), 3),
            "cohens_d": round(d, 3),
            "significant_at_0125": sig,
        }

    supported = sig_count >= 3
    return {
        "status": "SUPPORTED" if supported else "NOT SUPPORTED",
        "significant_formats": sig_count,
        "per_format": results,
    }


def test_h3(records: list[dict]) -> dict:
    """H3: Likert attenuates primacy compared to JSON."""
    json_primacy = []
    likert_primacy = []

    for fmt, collector in [("json", json_primacy), ("likert", likert_primacy)]:
        for r in valid_records(records):
            if r.get("response_format") != fmt:
                continue
            pw = r.get("position_weights")
            if pw is None:
                continue
            early_keys = ["1", "2", 1, 2]
            late_keys = ["7", "8", 7, 8]
            early_vals = [float(pw[k]) for k in early_keys if k in pw]
            late_vals = [float(pw[k]) for k in late_keys if k in pw]
            if early_vals and late_vals:
                collector.append(np.mean(early_vals) - np.mean(late_vals))

    if len(json_primacy) < 2 or len(likert_primacy) < 2:
        return {"status": "INSUFFICIENT_DATA"}

    json_arr = np.array(json_primacy)
    likert_arr = np.array(likert_primacy)
    t_stat, p_val = sp_stats.ttest_ind(json_arr, likert_arr)
    d = cohens_d(json_arr, likert_arr)

    supported = p_val < .05 and d >= .40 and np.mean(json_arr) > np.mean(likert_arr)
    return {
        "status": "SUPPORTED" if supported else "NOT SUPPORTED",
        "json_mean_primacy": round(float(np.mean(json_arr)), 3),
        "likert_mean_primacy": round(float(np.mean(likert_arr)), 3),
        "t_statistic": round(float(t_stat), 3),
        "p_value": round(float(p_val), 3),
        "cohens_d": round(d, 3),
        "n_json": len(json_primacy),
        "n_likert": len(likert_primacy),
    }


def test_h4(records: list[dict]) -> dict:
    """H4: Cross-model consistency of primacy direction."""
    model_results = {}

    for r in valid_records(records):
        if r.get("response_format") != "json":
            continue
        model = r.get("model_provider", "unknown")
        pw = r.get("position_weights")
        if pw is None:
            continue
        early_keys = ["1", "2", 1, 2]
        late_keys = ["7", "8", 7, 8]
        early_vals = [float(pw[k]) for k in early_keys if k in pw]
        late_vals = [float(pw[k]) for k in late_keys if k in pw]
        if early_vals and late_vals:
            diff = np.mean(early_vals) - np.mean(late_vals)
            model_results.setdefault(model, []).append(diff)

    per_model = {}
    positive_count = 0
    for model, diffs in sorted(model_results.items()):
        arr = np.array(diffs)
        ci = bootstrap_ci(arr)
        mean_diff = float(np.mean(arr))
        is_positive = mean_diff > 0
        if is_positive:
            positive_count += 1
        per_model[model] = {
            "mean_primacy": round(mean_diff, 3),
            "ci_95": [round(ci[0], 3), round(ci[1], 3)],
            "n": len(diffs),
            "direction": "primacy" if is_positive else "recency",
        }

    same_direction = max(positive_count, len(model_results) - positive_count)
    supported = same_direction >= 4
    return {
        "status": "SUPPORTED" if supported else "NOT SUPPORTED",
        "models_with_same_direction": same_direction,
        "total_models": len(model_results),
        "per_model": per_model,
    }


# ---------------------------------------------------------------------------
# Secondary analyses
# ---------------------------------------------------------------------------


def position_curve(records: list[dict]) -> dict:
    """Mean weight by position (1-8) per format + linear/quadratic trends."""
    curves = {}
    for fmt in FORMATS:
        pos_data = extract_position_arrays(records, fmt)
        means = {}
        for pos in range(1, 9):
            vals = pos_data[pos]
            if vals:
                means[pos] = round(float(np.mean(vals)), 2)
            else:
                means[pos] = None

        # Linear trend test
        positions = []
        weights = []
        for pos in range(1, 9):
            for v in pos_data[pos]:
                positions.append(pos)
                weights.append(v)

        if len(positions) > 2:
            slope, intercept, r_val, p_val, std_err = sp_stats.linregress(
                positions, weights
            )
            linear = {
                "slope": round(float(slope), 3),
                "r_squared": round(float(r_val**2), 4),
                "p_value": round(float(p_val), 3),
            }
        else:
            linear = {"status": "INSUFFICIENT_DATA"}

        curves[fmt] = {
            "mean_by_position": means,
            "linear_trend": linear,
        }

    return curves


def brand_moderation(records: list[dict]) -> dict:
    """Position x Brand interaction in JSON format."""
    brand_pos = {}  # brand -> {pos -> [weights]}
    for r in valid_records(records):
        if r.get("response_format") != "json":
            continue
        brand = r.get("brand", "unknown")
        pw = r.get("position_weights")
        if pw is None:
            continue
        bp = brand_pos.setdefault(brand, {p: [] for p in range(1, 9)})
        for pos in range(1, 9):
            key = str(pos) if str(pos) in pw else pos
            val = pw.get(key, pw.get(str(key)))
            if val is not None:
                bp[pos].append(float(val))

    results = {}
    for brand, pos_data in sorted(brand_pos.items()):
        early = pos_data.get(1, []) + pos_data.get(2, [])
        late = pos_data.get(7, []) + pos_data.get(8, [])
        if len(early) >= 2 and len(late) >= 2:
            diff = float(np.mean(early) - np.mean(late))
            results[brand] = {
                "primacy_magnitude": round(diff, 2),
                "mean_pos_1_2": round(float(np.mean(early)), 2),
                "mean_pos_7_8": round(float(np.mean(late)), 2),
            }

    return results


# ---------------------------------------------------------------------------
# Summary Report
# ---------------------------------------------------------------------------


def generate_summary(records: list[dict], results: dict) -> str:
    """Generate markdown summary."""
    total = len(records)
    valid = len(valid_records(records))
    lines = [
        "# Experiment E: Primacy Effect Generalization -- Results Summary",
        "",
        f"**Date**: {records[0]['timestamp'][:10] if records else 'N/A'}",
        f"**Total calls**: {total}",
        f"**Valid responses**: {valid} ({valid/total*100:.1f}%)" if total else "",
        "",
        "---",
        "",
        "## H1: Primacy Effect in JSON Format",
        "",
    ]

    h1 = results["h1"]
    lines.append(f"**Result**: {h1['status']}")
    if "mean_pos_1_2" in h1:
        lines.extend([
            f"- Mean weight positions 1-2: {h1['mean_pos_1_2']}",
            f"- Mean weight positions 7-8: {h1['mean_pos_7_8']}",
            f"- Difference: {h1['difference']}",
            f"- t = {h1['t_statistic']}, p = {h1['p_value']}",
            f"- Cohen's d = {h1['cohens_d']} (95% CI: {h1['d_ci_95']})",
        ])

    lines.extend(["", "## H2: Primacy Generalizes Across Formats", ""])
    h2 = results["h2"]
    lines.append(f"**Result**: {h2['status']} ({h2['significant_formats']}/4 formats significant)")
    for fmt, fdata in h2.get("per_format", {}).items():
        if "difference" in fdata:
            sig_mark = " *" if fdata.get("significant_at_0125") else ""
            lines.append(
                f"- {fmt}: diff = {fdata['difference']}, "
                f"t = {fdata['t_statistic']}, p = {fdata['p_value']}, "
                f"d = {fdata['cohens_d']}{sig_mark}"
            )

    lines.extend(["", "## H3: Likert Attenuates Primacy", ""])
    h3 = results["h3"]
    lines.append(f"**Result**: {h3['status']}")
    if "json_mean_primacy" in h3:
        lines.extend([
            f"- JSON mean primacy: {h3['json_mean_primacy']}",
            f"- Likert mean primacy: {h3['likert_mean_primacy']}",
            f"- t = {h3['t_statistic']}, p = {h3['p_value']}, d = {h3['cohens_d']}",
        ])

    lines.extend(["", "## H4: Cross-Model Consistency", ""])
    h4 = results["h4"]
    lines.append(f"**Result**: {h4['status']} ({h4['models_with_same_direction']}/{h4['total_models']} same direction)")
    for model, mdata in h4.get("per_model", {}).items():
        lines.append(
            f"- {model}: mean primacy = {mdata['mean_primacy']} "
            f"(95% CI: {mdata['ci_95']}), direction = {mdata['direction']}"
        )

    lines.extend(["", "## Position Curves (Secondary)", ""])
    for fmt, curve in results.get("position_curves", {}).items():
        means = curve.get("mean_by_position", {})
        lt = curve.get("linear_trend", {})
        vals = " | ".join(f"P{p}: {means.get(p, 'N/A')}" for p in range(1, 9))
        lines.append(f"**{fmt}**: {vals}")
        if "slope" in lt:
            lines.append(
                f"  Linear trend: slope = {lt['slope']}, "
                f"R-sq = {lt['r_squared']}, p = {lt['p_value']}"
            )
        lines.append("")

    lines.extend(["## Brand Moderation (Secondary)", ""])
    for brand, bdata in results.get("brand_moderation", {}).items():
        lines.append(
            f"- {brand}: primacy magnitude = {bdata['primacy_magnitude']} "
            f"(pos 1-2: {bdata['mean_pos_1_2']}, pos 7-8: {bdata['mean_pos_7_8']})"
        )

    lines.extend([
        "",
        "---",
        "",
        "*Analysis follows pre-registered protocol. Exploratory analyses labeled as such.*",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Loading data...")
    records = load_records()
    print(f"Loaded {len(records)} records, {len(valid_records(records))} valid.")

    print("\nRunning H1 (Primacy in JSON)...")
    h1 = test_h1(records)
    print(f"  -> {h1['status']}")

    print("Running H2 (Cross-format generalization)...")
    h2 = test_h2(records)
    print(f"  -> {h2['status']}")

    print("Running H3 (Likert attenuation)...")
    h3 = test_h3(records)
    print(f"  -> {h3['status']}")

    print("Running H4 (Cross-model consistency)...")
    h4 = test_h4(records)
    print(f"  -> {h4['status']}")

    print("Running secondary analyses...")
    curves = position_curve(records)
    brand_mod = brand_moderation(records)

    results = {
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "h4": h4,
        "position_curves": curves,
        "brand_moderation": brand_mod,
    }

    # Save JSON results
    results_path = OUTPUT_DIR / "exp_primacy_generalization_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved: {results_path}")

    # Save markdown summary
    summary = generate_summary(records, results)
    with open(SUMMARY_PATH, "w") as f:
        f.write(summary)
    print(f"Summary saved: {SUMMARY_PATH}")

    # Print summary table
    print(f"\n{'='*50}")
    print(f"HYPOTHESIS RESULTS")
    print(f"{'='*50}")
    print(f"H1 (JSON primacy):        {h1['status']}")
    print(f"H2 (Cross-format):        {h2['status']}")
    print(f"H3 (Likert attenuation):  {h3['status']}")
    print(f"H4 (Cross-model):         {h4['status']}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
