#!/usr/bin/env python3
"""Analysis script for Experiment C: Competitive Interference in Perception Space

Reads JSONL from L3_sessions/exp_competitive_interference.jsonl and produces:
- Statistical tests for H1, H2, H3
- Summary report
- Results JSON for HuggingFace dataset

Usage:
    python exp_competitive_interference_analysis.py
    python exp_competitive_interference_analysis.py --jsonl path/to/data.jsonl

License: MIT
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RANDOM_SEED = 42
BOOTSTRAP_N = 10_000

DIMENSIONS = [
    "semiotic", "narrative", "ideological", "experiential",
    "social", "economic", "cultural", "temporal",
]

CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

# Bonferroni-corrected alpha for 8 dimension tests
ALPHA_BONFERRONI = 0.05 / 8  # .00625


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_jsonl(path: Path) -> list[dict]:
    """Load JSONL and filter to successful records with valid weights."""
    records = []
    total = 0
    with open(path) as f:
        for line in f:
            total += 1
            record = json.loads(line)
            if record.get("error") is None and record.get("weights") is not None:
                records.append(record)
    print(f"Loaded {len(records)} valid records from {total} total ({path.name})")
    return records


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def weights_to_vector(weights: dict) -> np.ndarray:
    """Convert weights dict to numpy array in canonical dimension order."""
    return np.array([weights[dim] for dim in DIMENSIONS])


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom < 1e-10:
        return 0.0
    return float(np.dot(a, b) / denom)


def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    """Compute Cohen's d (pooled standard deviation)."""
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return 0.0
    var1 = np.var(group1, ddof=1)
    var2 = np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std < 1e-10:
        return 0.0
    return float((np.mean(group1) - np.mean(group2)) / pooled_std)


def bootstrap_ci(data: np.ndarray, statistic_fn, n_boot: int = BOOTSTRAP_N,
                 ci: float = 0.95, seed: int = RANDOM_SEED) -> tuple[float, float]:
    """Compute bootstrap confidence interval for a statistic."""
    rng = np.random.RandomState(seed)
    stats_boot = []
    for _ in range(n_boot):
        sample = rng.choice(data, size=len(data), replace=True)
        stats_boot.append(statistic_fn(sample))
    lower = np.percentile(stats_boot, (1 - ci) / 2 * 100)
    upper = np.percentile(stats_boot, (1 + ci) / 2 * 100)
    return float(lower), float(upper)


def eta_squared(groups: list[np.ndarray]) -> float:
    """Compute eta-squared from groups."""
    all_data = np.concatenate(groups)
    grand_mean = np.mean(all_data)
    ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)
    ss_total = np.sum((all_data - grand_mean) ** 2)
    if ss_total < 1e-10:
        return 0.0
    return float(ss_between / ss_total)


# ---------------------------------------------------------------------------
# Analysis Functions
# ---------------------------------------------------------------------------

def analyze_h1(records: list[dict]) -> dict:
    """H1: Spectral profiles shift when competitor is present vs solo.

    Paired t-test on per-dimension weights: solo vs competitive conditions.
    Bonferroni correction for 8 dimensions.
    """
    print("\n" + "=" * 60)
    print("H1: Competitive Context Effect")
    print("=" * 60)

    # Group by brand and model
    solo_weights = defaultdict(list)  # (brand, model) -> [weight_vector]
    comp_weights = defaultdict(list)  # (brand, model) -> [weight_vector]

    for r in records:
        key = (r["brand"], r["model"])
        vec = weights_to_vector(r["weights"])
        if r["condition"] == "solo":
            solo_weights[key].append(vec)
        else:
            comp_weights[key].append(vec)

    # Aggregate: mean solo profile vs mean competitive profile per brand
    solo_by_brand = defaultdict(list)
    comp_by_brand = defaultdict(list)

    for r in records:
        vec = weights_to_vector(r["weights"])
        if r["condition"] == "solo":
            solo_by_brand[r["brand"]].append(vec)
        else:
            comp_by_brand[r["brand"]].append(vec)

    # Per-dimension analysis
    results = {"per_dimension": {}, "significant_count": 0, "supported": False}

    all_solo = np.array([weights_to_vector(r["weights"]) for r in records
                         if r["condition"] == "solo"])
    all_comp = np.array([weights_to_vector(r["weights"]) for r in records
                         if r["condition"] != "solo"
                         and r.get("competitor_type") != "self"])
    all_self = np.array([weights_to_vector(r["weights"]) for r in records
                         if r.get("competitor_type") == "self"])

    # Report self-comparison baseline bias
    if len(all_self) >= 2 and len(all_solo) >= 2:
        print("\n  Self-comparison control (prompt format bias check):")
        for i, dim in enumerate(DIMENSIONS):
            solo_vals = all_solo[:, i]
            self_vals = all_self[:, i]
            t_s, p_s = stats.ttest_ind(solo_vals, self_vals)
            print(f"    {dim:14s}: solo={np.mean(solo_vals):5.1f}  "
                  f"self={np.mean(self_vals):5.1f}  "
                  f"diff={np.mean(self_vals)-np.mean(solo_vals):+5.1f}  "
                  f"p={p_s:.4f}")
        self_shift = euclidean_distance(np.mean(all_self, axis=0),
                                         np.mean(all_solo, axis=0))
        print(f"    Overall self-comparison Euclidean shift: {self_shift:.2f}")
        results["self_comparison_shift"] = round(self_shift, 3)
        print()

    if len(all_solo) < 2 or len(all_comp) < 2:
        print("  Insufficient data for H1 test")
        return results

    sig_count = 0
    for i, dim in enumerate(DIMENSIONS):
        solo_vals = all_solo[:, i]
        comp_vals = all_comp[:, i]

        t_stat, p_value = stats.ttest_ind(solo_vals, comp_vals)
        d = cohens_d(solo_vals, comp_vals)

        solo_mean = float(np.mean(solo_vals))
        comp_mean = float(np.mean(comp_vals))
        shift = comp_mean - solo_mean

        significant = p_value < ALPHA_BONFERRONI

        if significant:
            sig_count += 1

        results["per_dimension"][dim] = {
            "solo_mean": round(solo_mean, 2),
            "comp_mean": round(comp_mean, 2),
            "shift": round(shift, 2),
            "t_stat": round(float(t_stat), 3),
            "p_value": round(float(p_value), 4),
            "cohens_d": round(d, 3),
            "significant_bonferroni": significant,
        }

        sig_marker = " ***" if significant else ""
        print(
            f"  {dim:14s}: solo={solo_mean:5.1f}  comp={comp_mean:5.1f}  "
            f"shift={shift:+5.1f}  t={t_stat:+6.2f}  p={p_value:.4f}  "
            f"d={d:+.3f}{sig_marker}"
        )

    results["significant_count"] = sig_count
    results["supported"] = sig_count >= 2
    results["n_solo"] = len(all_solo)
    results["n_comp"] = len(all_comp)

    verdict = "SUPPORTED" if results["supported"] else "NOT SUPPORTED"
    print(f"\n  H1 verdict: {verdict} ({sig_count}/8 dimensions significant at Bonferroni alpha)")
    return results


def analyze_h2(records: list[dict]) -> dict:
    """H2: Direct competitors produce larger profile shifts than distant competitors.

    One-way ANOVA on Euclidean shift magnitude by competitor type.
    """
    print("\n" + "=" * 60)
    print("H2: Distance-Dependent Shift")
    print("=" * 60)

    # Get solo baselines per brand per model
    solo_means = {}
    for r in records:
        if r["condition"] == "solo":
            key = (r["brand"], r["model"])
            if key not in solo_means:
                solo_means[key] = []
            solo_means[key].append(weights_to_vector(r["weights"]))

    # Average solo baselines
    solo_avg = {}
    for key, vecs in solo_means.items():
        solo_avg[key] = np.mean(vecs, axis=0)

    # Compute shift magnitudes by competitor type (exclude self-comparison)
    shift_by_type = defaultdict(list)
    for r in records:
        if r["condition"] == "solo" or r.get("competitor_type") == "self":
            continue
        key = (r["brand"], r["model"])
        if key not in solo_avg:
            continue
        comp_vec = weights_to_vector(r["weights"])
        shift_mag = euclidean_distance(comp_vec, solo_avg[key])
        shift_by_type[r["competitor_type"]].append(shift_mag)

    results = {"per_type": {}, "anova": {}, "supported": False}

    for comp_type in ["direct", "adjacent", "distant"]:
        vals = shift_by_type.get(comp_type, [])
        if vals:
            results["per_type"][comp_type] = {
                "n": len(vals),
                "mean": round(float(np.mean(vals)), 3),
                "std": round(float(np.std(vals, ddof=1)), 3) if len(vals) > 1 else 0,
                "median": round(float(np.median(vals)), 3),
            }
            print(f"  {comp_type:10s}: n={len(vals):3d}  mean={np.mean(vals):6.2f}  "
                  f"std={np.std(vals, ddof=1):5.2f}" if len(vals) > 1 else
                  f"  {comp_type:10s}: n={len(vals):3d}  mean={np.mean(vals):6.2f}")

    groups = [
        np.array(shift_by_type.get(t, []))
        for t in ["direct", "adjacent", "distant"]
        if shift_by_type.get(t)
    ]

    if len(groups) >= 2 and all(len(g) >= 2 for g in groups):
        f_stat, p_value = stats.f_oneway(*groups)
        eta_sq = eta_squared(groups)

        results["anova"] = {
            "f_stat": round(float(f_stat), 3),
            "p_value": round(float(p_value), 4),
            "eta_squared": round(eta_sq, 4),
        }

        # Planned contrast: direct > distant
        direct = np.array(shift_by_type.get("direct", []))
        distant = np.array(shift_by_type.get("distant", []))
        if len(direct) >= 2 and len(distant) >= 2:
            t_contrast, p_contrast = stats.ttest_ind(direct, distant)
            d_contrast = cohens_d(direct, distant)
            results["planned_contrast"] = {
                "t_stat": round(float(t_contrast), 3),
                "p_value": round(float(p_contrast), 4),
                "cohens_d": round(d_contrast, 3),
                "direct_mean": round(float(np.mean(direct)), 3),
                "distant_mean": round(float(np.mean(distant)), 3),
            }
            results["supported"] = p_value < 0.05 and float(np.mean(direct)) > float(np.mean(distant))

        print(f"\n  ANOVA: F={f_stat:.3f}, p={p_value:.4f}, eta-sq={eta_sq:.4f}")
        if "planned_contrast" in results:
            pc = results["planned_contrast"]
            print(f"  Contrast (direct vs distant): t={pc['t_stat']:.3f}, "
                  f"p={pc['p_value']:.4f}, d={pc['cohens_d']:.3f}")
    else:
        print("  Insufficient groups for ANOVA")

    verdict = "SUPPORTED" if results["supported"] else "NOT SUPPORTED"
    print(f"\n  H2 verdict: {verdict}")
    return results


def analyze_h3(records: list[dict]) -> dict:
    """H3: Dimension-specific contrast vs assimilation patterns.

    Tests whether brands differentiate away from competitors on shared dimensions
    and toward competitors on distinctive dimensions.
    """
    print("\n" + "=" * 60)
    print("H3: Dimension-Specific Contrast/Assimilation")
    print("=" * 60)

    # Get solo baselines per brand per model
    solo_means = {}
    for r in records:
        if r["condition"] == "solo":
            key = (r["brand"], r["model"])
            if key not in solo_means:
                solo_means[key] = []
            solo_means[key].append(weights_to_vector(r["weights"]))

    solo_avg = {}
    for key, vecs in solo_means.items():
        solo_avg[key] = np.mean(vecs, axis=0)

    # Canonical profiles as weight vectors (normalize to sum 100 for comparison)
    canon = {}
    for brand, profile in CANONICAL_PROFILES.items():
        total = sum(profile)
        canon[brand] = np.array([v / total * 100 for v in profile])

    # For each competitive call, classify each dimension and measure shift direction
    contrast_shifts = []  # shifts on "shared strong" dimensions
    assimilation_shifts = []  # shifts on "distinctive weak" dimensions

    for r in records:
        if r["condition"] == "solo" or r.get("competitor") is None:
            continue
        if r.get("competitor_type") == "self":
            continue
        key = (r["brand"], r["model"])
        if key not in solo_avg:
            continue

        focal_solo = solo_avg[key]
        focal_comp = weights_to_vector(r["weights"])
        shift = focal_comp - focal_solo

        # Use canonical profiles to classify dimensions
        focal_canon = canon.get(r["brand"])
        if focal_canon is None:
            continue

        for i, dim in enumerate(DIMENSIONS):
            focal_strength = focal_canon[i]
            median_strength = float(np.median(focal_canon))

            if focal_strength >= median_strength:
                # "Shared strong" dimension -- expect contrast (negative shift away)
                contrast_shifts.append(shift[i])
            else:
                # "Distinctive weak" dimension -- expect assimilation
                assimilation_shifts.append(shift[i])

    results = {"supported": False}

    contrast_arr = np.array(contrast_shifts) if contrast_shifts else np.array([])
    assim_arr = np.array(assimilation_shifts) if assimilation_shifts else np.array([])

    if len(contrast_arr) >= 2 and len(assim_arr) >= 2:
        t_stat, p_value = stats.ttest_ind(contrast_arr, assim_arr)
        d = cohens_d(contrast_arr, assim_arr)

        results.update({
            "contrast_mean_shift": round(float(np.mean(contrast_arr)), 3),
            "assimilation_mean_shift": round(float(np.mean(assim_arr)), 3),
            "contrast_n": len(contrast_arr),
            "assimilation_n": len(assim_arr),
            "t_stat": round(float(t_stat), 3),
            "p_value": round(float(p_value), 4),
            "cohens_d": round(d, 3),
            "supported": p_value < 0.05,
        })

        print(f"  Contrast dimensions (shared strong): mean shift = {np.mean(contrast_arr):+.3f} (n={len(contrast_arr)})")
        print(f"  Assimilation dimensions (distinctive weak): mean shift = {np.mean(assim_arr):+.3f} (n={len(assim_arr)})")
        print(f"  t={t_stat:.3f}, p={p_value:.4f}, d={d:.3f}")
    else:
        print("  Insufficient data for H3 test")

    verdict = "SUPPORTED" if results["supported"] else "NOT SUPPORTED"
    print(f"\n  H3 verdict: {verdict}")
    return results


def exploratory_analyses(records: list[dict]) -> dict:
    """Secondary and exploratory analyses."""
    print("\n" + "=" * 60)
    print("EXPLORATORY: Additional Analyses")
    print("=" * 60)

    results = {}

    # Model susceptibility to competitive context
    print("\n  Per-model shift magnitudes:")
    solo_by_model_brand = defaultdict(list)
    comp_by_model_brand = defaultdict(list)

    for r in records:
        key = (r["model"], r["brand"])
        vec = weights_to_vector(r["weights"])
        if r["condition"] == "solo":
            solo_by_model_brand[key].append(vec)
        else:
            comp_by_model_brand[key].append(vec)

    model_shifts = defaultdict(list)
    for (model, brand), comp_vecs in comp_by_model_brand.items():
        solo_key = (model, brand)
        if solo_key not in solo_by_model_brand:
            continue
        solo_avg = np.mean(solo_by_model_brand[solo_key], axis=0)
        for cv in comp_vecs:
            shift = euclidean_distance(cv, solo_avg)
            model_shifts[model].append(shift)

    model_susceptibility = {}
    for model in sorted(model_shifts.keys()):
        vals = model_shifts[model]
        mean_shift = float(np.mean(vals))
        model_susceptibility[model] = {
            "n": len(vals),
            "mean_shift": round(mean_shift, 3),
        }
        print(f"    {model:12s}: mean_shift={mean_shift:6.2f} (n={len(vals)})")

    results["model_susceptibility"] = model_susceptibility

    # Paired vs Context condition comparison
    print("\n  Paired vs Context condition:")
    paired_shifts = []
    context_shifts = []

    for r in records:
        if r["condition"] == "solo":
            continue
        key = (r["model"], r["brand"])
        if key not in solo_by_model_brand:
            continue
        solo_avg = np.mean(solo_by_model_brand[key], axis=0)
        shift = euclidean_distance(weights_to_vector(r["weights"]), solo_avg)
        if r["condition"] == "paired":
            paired_shifts.append(shift)
        elif r["condition"] == "context":
            context_shifts.append(shift)

    if len(paired_shifts) >= 2 and len(context_shifts) >= 2:
        t_stat, p_value = stats.ttest_ind(paired_shifts, context_shifts)
        d = cohens_d(np.array(paired_shifts), np.array(context_shifts))
        results["paired_vs_context"] = {
            "paired_mean": round(float(np.mean(paired_shifts)), 3),
            "context_mean": round(float(np.mean(context_shifts)), 3),
            "t_stat": round(float(t_stat), 3),
            "p_value": round(float(p_value), 4),
            "cohens_d": round(d, 3),
        }
        print(f"    Paired mean shift: {np.mean(paired_shifts):.2f}")
        print(f"    Context mean shift: {np.mean(context_shifts):.2f}")
        print(f"    t={t_stat:.3f}, p={p_value:.4f}, d={d:.3f}")

    # Per-brand shift magnitudes
    print("\n  Per-brand mean shift magnitudes:")
    brand_shifts = defaultdict(list)
    for r in records:
        if r["condition"] == "solo":
            continue
        key = (r["model"], r["brand"])
        if key not in solo_by_model_brand:
            continue
        solo_avg = np.mean(solo_by_model_brand[key], axis=0)
        shift = euclidean_distance(weights_to_vector(r["weights"]), solo_avg)
        brand_shifts[r["brand"]].append(shift)

    brand_summary = {}
    for brand in sorted(brand_shifts.keys()):
        vals = brand_shifts[brand]
        brand_summary[brand] = {
            "n": len(vals),
            "mean_shift": round(float(np.mean(vals)), 3),
        }
        print(f"    {brand:12s}: mean_shift={np.mean(vals):6.2f} (n={len(vals)})")

    results["per_brand"] = brand_summary

    return results


# ---------------------------------------------------------------------------
# Summary Generation
# ---------------------------------------------------------------------------

def generate_summary(
    records: list[dict],
    h1: dict,
    h2: dict,
    h3: dict,
    exploratory: dict,
    output_path: Path,
):
    """Generate markdown summary report."""
    total = len(records)
    solo_n = sum(1 for r in records if r["condition"] == "solo")
    comp_n = total - solo_n

    models_used = sorted(set(r["model"] for r in records))
    brands_tested = sorted(set(r["brand"] for r in records))

    lines = [
        "# Experiment C: Competitive Interference -- Results Summary",
        "",
        f"**Date**: {records[0]['timestamp'][:10] if records else 'N/A'}",
        f"**Total valid records**: {total} ({solo_n} solo + {comp_n} competitive)",
        f"**Models**: {', '.join(models_used)}",
        f"**Brands**: {', '.join(brands_tested)}",
        "",
        "---",
        "",
        "## H1: Competitive Context Effect",
        "",
        f"**Verdict**: {'SUPPORTED' if h1.get('supported') else 'NOT SUPPORTED'}",
        f"**Significant dimensions (Bonferroni alpha = {ALPHA_BONFERRONI:.5f})**: "
        f"{h1.get('significant_count', 0)}/8",
        "",
        "| Dimension | Solo Mean | Comp Mean | Shift | t | p | Cohen's d | Sig |",
        "|-----------|-----------|-----------|-------|---|---|-----------|-----|",
    ]

    for dim in DIMENSIONS:
        d = h1.get("per_dimension", {}).get(dim, {})
        sig = "Yes" if d.get("significant_bonferroni") else "No"
        lines.append(
            f"| {dim.capitalize()} | {d.get('solo_mean', 'N/A')} | "
            f"{d.get('comp_mean', 'N/A')} | {d.get('shift', 'N/A'):+.2f} | "
            f"{d.get('t_stat', 'N/A')} | {d.get('p_value', 'N/A')} | "
            f"{d.get('cohens_d', 'N/A')} | {sig} |"
            if isinstance(d.get('shift'), (int, float)) else
            f"| {dim.capitalize()} | N/A | N/A | N/A | N/A | N/A | N/A | N/A |"
        )

    lines.extend([
        "",
        "## H2: Distance-Dependent Shift",
        "",
        f"**Verdict**: {'SUPPORTED' if h2.get('supported') else 'NOT SUPPORTED'}",
        "",
    ])

    if h2.get("anova"):
        a = h2["anova"]
        lines.append(f"ANOVA: F={a['f_stat']}, p={a['p_value']}, eta-sq={a['eta_squared']}")

    if h2.get("planned_contrast"):
        pc = h2["planned_contrast"]
        lines.append(
            f"Planned contrast (direct vs distant): t={pc['t_stat']}, "
            f"p={pc['p_value']}, d={pc['cohens_d']}"
        )

    lines.extend([
        "",
        "| Competitor Type | n | Mean Shift | Std |",
        "|-----------------|---|------------|-----|",
    ])
    for ct in ["direct", "adjacent", "distant"]:
        info = h2.get("per_type", {}).get(ct, {})
        lines.append(
            f"| {ct.capitalize()} | {info.get('n', 'N/A')} | "
            f"{info.get('mean', 'N/A')} | {info.get('std', 'N/A')} |"
        )

    lines.extend([
        "",
        "## H3: Dimension-Specific Contrast/Assimilation",
        "",
        f"**Verdict**: {'SUPPORTED' if h3.get('supported') else 'NOT SUPPORTED'}",
        "",
    ])

    if h3.get("t_stat") is not None:
        lines.extend([
            f"- Contrast dimensions mean shift: {h3['contrast_mean_shift']:+.3f} (n={h3['contrast_n']})",
            f"- Assimilation dimensions mean shift: {h3['assimilation_mean_shift']:+.3f} (n={h3['assimilation_n']})",
            f"- t={h3['t_stat']}, p={h3['p_value']}, d={h3['cohens_d']}",
        ])

    lines.extend([
        "",
        "## Exploratory Analyses",
        "",
        "### Model Susceptibility to Competitive Context",
        "",
        "| Model | Mean Shift | n |",
        "|-------|------------|---|",
    ])
    for model, info in sorted(exploratory.get("model_susceptibility", {}).items()):
        lines.append(f"| {model} | {info['mean_shift']} | {info['n']} |")

    if exploratory.get("paired_vs_context"):
        pvc = exploratory["paired_vs_context"]
        lines.extend([
            "",
            "### Paired vs Context Condition",
            "",
            f"- Paired mean shift: {pvc['paired_mean']}",
            f"- Context mean shift: {pvc['context_mean']}",
            f"- t={pvc['t_stat']}, p={pvc['p_value']}, d={pvc['cohens_d']}",
        ])

    lines.extend([
        "",
        "---",
        "*Analysis generated by exp_competitive_interference_analysis.py*",
    ])

    summary_text = "\n".join(lines)
    output_path.write_text(summary_text)
    print(f"\nSummary written to {output_path}")
    return summary_text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Experiment C: Competitive Interference"
    )
    parser.add_argument(
        "--jsonl", type=str, default=None,
        help="Path to JSONL data file",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).parent.parent
    if args.jsonl:
        jsonl_path = Path(args.jsonl)
    else:
        jsonl_path = script_dir / "L3_sessions" / "exp_competitive_interference.jsonl"

    if not jsonl_path.exists():
        print(f"ERROR: JSONL file not found: {jsonl_path}")
        sys.exit(1)

    records = load_jsonl(jsonl_path)
    if not records:
        print("ERROR: No valid records found")
        sys.exit(1)

    # Run analyses
    h1_results = analyze_h1(records)
    h2_results = analyze_h2(records)
    h3_results = analyze_h3(records)
    exploratory_results = exploratory_analyses(records)

    # Save results JSON
    all_results = {
        "experiment": "C_competitive_interference",
        "n_records": len(records),
        "h1": h1_results,
        "h2": h2_results,
        "h3": h3_results,
        "exploratory": exploratory_results,
    }

    results_path = script_dir / "L4_analysis" / "exp_competitive_interference_results.json"
    results_path.write_text(json.dumps(all_results, indent=2))
    print(f"\nResults JSON written to {results_path}")

    # Generate summary
    summary_path = script_dir / "L4_analysis" / "exp_competitive_interference_summary.md"
    generate_summary(records, h1_results, h2_results, h3_results,
                     exploratory_results, summary_path)

    # Also copy to HF dataset
    hf_dir = script_dir / "hf_dataset"
    (hf_dir / "analysis").mkdir(parents=True, exist_ok=True)
    (hf_dir / "analysis" / "results.json").write_text(json.dumps(all_results, indent=2))
    (hf_dir / "analysis" / "summary.md").write_text(summary_path.read_text())

    return all_results


if __name__ == "__main__":
    main()
