#!/usr/bin/env python3
"""Run 15b: Latin-Square Robustness — Analysis.

Compares ordering-aggregated profiles from the Latin-square experiment
with canonical-order profiles from Run 15. Tests whether dimension
position in the JSON template affects weight allocation.

Key metric: Spearman rho between ordering-averaged and canonical-order
mean profiles. If rho > .90, position effects are negligible.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

RNG = np.random.default_rng(42)

DIMENSIONS = [
    "Semiotic",
    "Narrative",
    "Ideological",
    "Experiential",
    "Social",
    "Economic",
    "Cultural",
    "Temporal",
]


def load_data(jsonl_path: Path) -> list[dict]:
    records = []
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if r["weights_valid"] and r["parsed_weights"]:
                records.append(r)
    return records


def weights_to_vector(weights: dict) -> np.ndarray:
    vec = np.array([weights[d] for d in DIMENSIONS], dtype=float)
    total = vec.sum()
    if total > 0:
        vec /= total
    return vec


def analyze_position_effects(records: list[dict]) -> dict:
    """Test whether ordinal position affects dimension weights.

    For each of the 8 positions in the JSON template, compute the mean
    weight assigned to whichever dimension occupied that position.
    If position has no effect, all 8 position means should be ~12.5%.
    """
    # Group weights by position
    position_weights = {i: [] for i in range(8)}
    for r in records:
        dim_order = r.get("dim_order", DIMENSIONS)
        w = r["parsed_weights"]
        for pos, dim in enumerate(dim_order):
            val = w.get(dim, 0) / sum(w.values()) if sum(w.values()) > 0 else 0
            position_weights[pos].append(val)

    position_means = {}
    for pos in range(8):
        vals = position_weights[pos]
        position_means[f"position_{pos}"] = {
            "mean": round(float(np.mean(vals)), 4),
            "std": round(float(np.std(vals)), 4),
            "n": len(vals),
        }

    # ANOVA: does position matter?
    groups = [np.array(position_weights[i]) for i in range(8)]
    f_stat, p_val = stats.f_oneway(*groups)

    all_vals = np.concatenate(groups)
    grand_mean = all_vals.mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
    ss_total = np.sum((all_vals - grand_mean) ** 2)
    eta_sq = ss_between / ss_total if ss_total > 0 else 0

    return {
        "position_means": position_means,
        "anova_F": round(float(f_stat), 3),
        "anova_p": round(float(p_val), 4),
        "eta_sq": round(float(eta_sq), 6),
        "position_effect_negligible": eta_sq < 0.01,
    }


def compare_with_canonical(latin_records: list[dict], canonical_path: Path) -> dict:
    """Compare Latin-square-averaged profiles with canonical-order profiles.

    For each (cohort, brand) cell, compute the mean profile across all
    8 orderings. Compare with the mean profile from canonical-order
    Run 15 data (GPT-4o-mini only, to match the Latin-square model).
    """
    # Latin-square: mean per (cohort, brand) across all orderings
    latin_profiles = {}
    for r in latin_records:
        key = (r["cohort_id"], r["brand"])
        vec = weights_to_vector(r["parsed_weights"])
        latin_profiles.setdefault(key, []).append(vec)

    latin_means = {}
    for key, vecs in latin_profiles.items():
        latin_means[key] = np.mean(vecs, axis=0)

    # Canonical: load Run 15 baseline, filter to GPT-4o-mini only
    if not canonical_path.exists():
        return {"note": f"Canonical data not found: {canonical_path}"}

    canonical_records = []
    with open(canonical_path) as f:
        for line in f:
            r = json.loads(line)
            if (
                r["weights_valid"]
                and r["parsed_weights"]
                and r["condition"] == "baseline"
                and r["model_id"] == "gpt-4o-mini"
            ):
                canonical_records.append(r)

    canonical_profiles = {}
    for r in canonical_records:
        key = (r["cohort_id"], r["brand"])
        vec = weights_to_vector(r["parsed_weights"])
        canonical_profiles.setdefault(key, []).append(vec)

    canonical_means = {}
    for key, vecs in canonical_profiles.items():
        canonical_means[key] = np.mean(vecs, axis=0)

    # Match keys present in both
    common_keys = sorted(set(latin_means) & set(canonical_means))
    if not common_keys:
        return {"note": "No matching (cohort, brand) cells found"}

    # Profile-level Spearman correlations
    rhos = []
    for key in common_keys:
        rho, _ = stats.spearmanr(latin_means[key], canonical_means[key])
        rhos.append(float(rho))

    # Element-level correlation (flatten all profiles)
    latin_flat = np.concatenate([latin_means[k] for k in common_keys])
    canonical_flat = np.concatenate([canonical_means[k] for k in common_keys])
    overall_rho, overall_p = stats.spearmanr(latin_flat, canonical_flat)
    overall_pearson, pearson_p = stats.pearsonr(latin_flat, canonical_flat)

    return {
        "n_cells": len(common_keys),
        "n_canonical_records": len(canonical_records),
        "per_cell_rho_median": round(float(np.median(rhos)), 4),
        "per_cell_rho_mean": round(float(np.mean(rhos)), 4),
        "per_cell_rho_min": round(float(np.min(rhos)), 4),
        "overall_spearman_rho": round(float(overall_rho), 4),
        "overall_spearman_p": round(float(overall_p), 6),
        "overall_pearson_r": round(float(overall_pearson), 4),
        "overall_pearson_p": round(float(pearson_p), 6),
        "invariant": float(overall_rho) > 0.90,
    }


def within_ordering_consistency(records: list[dict]) -> dict:
    """Test consistency across the 8 orderings for same (cohort, brand)."""
    cells = {}
    for r in records:
        key = (r["cohort_id"], r["brand"])
        oidx = r.get("ordering_idx", 0)
        vec = weights_to_vector(r["parsed_weights"])
        cells.setdefault(key, {}).setdefault(oidx, vec)

    # For each cell, compute pairwise Spearman across orderings
    all_rhos = []
    for key, orderings in cells.items():
        vecs = list(orderings.values())
        if len(vecs) < 2:
            continue
        for i in range(len(vecs)):
            for j in range(i + 1, len(vecs)):
                rho, _ = stats.spearmanr(vecs[i], vecs[j])
                all_rhos.append(float(rho))

    if not all_rhos:
        return {"note": "Insufficient data"}

    return {
        "n_pairs": len(all_rhos),
        "median_rho": round(float(np.median(all_rhos)), 4),
        "mean_rho": round(float(np.mean(all_rhos)), 4),
        "min_rho": round(float(np.min(all_rhos)), 4),
        "pct_above_90": round(100 * np.mean(np.array(all_rhos) > 0.90), 1),
        "pct_above_70": round(100 * np.mean(np.array(all_rhos) > 0.70), 1),
    }


def main():
    data_dir = Path(__file__).parent.parent / "L3_sessions"
    jsonl_path = data_dir / "run15b_robustness_latin_square.jsonl"
    canonical_path = data_dir / "run15_synthetic_cohorts.jsonl"

    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found.")
        sys.exit(1)

    records = load_data(jsonl_path)
    print(f"Loaded {len(records)} valid Latin-square records")

    print("\n--- Position Effects (ANOVA) ---")
    pos = analyze_position_effects(records)
    for pname, pdata in pos["position_means"].items():
        print(f"  {pname}: mean={pdata['mean']:.4f} std={pdata['std']:.4f}")
    print(f"  ANOVA: F={pos['anova_F']}, p={pos['anova_p']}, eta_sq={pos['eta_sq']}")
    print(
        f"  Position effect: "
        f"{'NEGLIGIBLE' if pos['position_effect_negligible'] else 'PRESENT'}"
    )

    print("\n--- Within-Ordering Consistency ---")
    woc = within_ordering_consistency(records)
    print(
        f"  {woc.get('n_pairs', 0)} ordering pairs, "
        f"median rho={woc.get('median_rho', 0):.4f}, "
        f"mean={woc.get('mean_rho', 0):.4f}"
    )
    print(
        f"  {woc.get('pct_above_90', 0):.1f}% pairs rho>.90, "
        f"{woc.get('pct_above_70', 0):.1f}% pairs rho>.70"
    )

    print("\n--- Comparison with Canonical Order (Run 15) ---")
    comp = compare_with_canonical(records, canonical_path)
    if "overall_spearman_rho" in comp:
        print(
            f"  {comp['n_cells']} cells matched "
            f"({comp['n_canonical_records']} canonical records)"
        )
        print(
            f"  Overall Spearman rho = {comp['overall_spearman_rho']:.4f} "
            f"(p = {comp['overall_spearman_p']:.6f})"
        )
        print(
            f"  Overall Pearson r = {comp['overall_pearson_r']:.4f} "
            f"(p = {comp['overall_pearson_p']:.6f})"
        )
        print(
            f"  Per-cell median rho = {comp['per_cell_rho_median']:.4f}, "
            f"min = {comp['per_cell_rho_min']:.4f}"
        )
        print(
            f"  Dimension-order invariant: "
            f"{'YES' if comp['invariant'] else 'NO'} "
            f"(threshold: rho > .90)"
        )
    else:
        print(f"  {comp.get('note', 'Error')}")

    total_cost = sum(r.get("api_cost_usd", 0) for r in records)

    results = {
        "experiment": "exp1b_robustness_latin_square",
        "date": "2026-04-16",
        "design": "8x8 Latin square, 10 cohorts, 5 brands, 1 model (GPT-4o-mini)",
        "total_records": len(records),
        "total_cost_usd": round(total_cost, 4),
        "position_effects": pos,
        "within_ordering_consistency": woc,
        "canonical_comparison": comp,
    }

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.bool_,)):
                return bool(obj)
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            return super().default(obj)

    results_path = Path(__file__).parent / "run15b_robustness_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
    print(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()
