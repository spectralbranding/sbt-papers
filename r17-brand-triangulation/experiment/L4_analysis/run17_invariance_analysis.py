#!/usr/bin/env python3
"""Run 17: Cross-Cohort Measurement Invariance Proxy — Analysis.

Uses Experiment 1 data (run15_synthetic_cohorts.jsonl) to test configural,
metric, and scalar invariance of PRISM-B across synthetic cohorts.
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

COHORT_IDS = [f"C{i}" for i in range(1, 11)]
BRANDS = ["Hermes", "IKEA", "Patagonia", "Erewhon", "Tesla"]


def load_data(jsonl_path: Path) -> list[dict]:
    records = []
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if r["weights_valid"] and r["parsed_weights"]:
                if r["condition"] == "baseline":
                    records.append(r)
    return records


def weights_to_vector(weights: dict) -> np.ndarray:
    vec = np.array([weights[d] for d in DIMENSIONS], dtype=float)
    total = vec.sum()
    if total > 0:
        vec /= total
    return vec


def test_h1_configural(records: list[dict]) -> dict:
    """H1: All cohorts produce non-zero weights on all 8 dimensions."""
    cohort_dim_means = {}
    for r in records:
        cid = r["cohort_id"]
        vec = weights_to_vector(r["parsed_weights"])
        cohort_dim_means.setdefault(cid, []).append(vec)

    zeroed_dims = {}
    for cid in COHORT_IDS:
        if cid not in cohort_dim_means:
            continue
        mean_vec = np.mean(cohort_dim_means[cid], axis=0)
        for i, dim in enumerate(DIMENSIONS):
            if mean_vec[i] < 0.01:  # Threshold: <1% mean weight
                zeroed_dims.setdefault(cid, []).append(dim)

    return {
        "zeroed_dimensions": zeroed_dims,
        "total_zeroed": sum(len(v) for v in zeroed_dims.values()),
        "h1_confirmed": len(zeroed_dims) == 0,
    }


def test_h2_metric(records: list[dict]) -> dict:
    """H2: Within-brand Spearman correlations across cohort pairs."""
    # Compute mean profile per (cohort, brand)
    profiles = {}
    for r in records:
        key = (r["cohort_id"], r["brand"])
        vec = weights_to_vector(r["parsed_weights"])
        profiles.setdefault(key, []).append(vec)

    mean_profiles = {}
    for key, vecs in profiles.items():
        mean_profiles[key] = np.mean(vecs, axis=0)

    # Within-brand cross-cohort Spearman correlations
    all_rhos = []
    per_brand = {}

    for brand in BRANDS:
        brand_cohorts = [c for c in COHORT_IDS if (c, brand) in mean_profiles]
        brand_rhos = []

        for i in range(len(brand_cohorts)):
            for j in range(i + 1, len(brand_cohorts)):
                c1, c2 = brand_cohorts[i], brand_cohorts[j]
                p1 = mean_profiles[(c1, brand)]
                p2 = mean_profiles[(c2, brand)]
                rho, _ = stats.spearmanr(p1, p2)
                brand_rhos.append(float(rho))
                all_rhos.append(float(rho))

        if brand_rhos:
            per_brand[brand] = {
                "median_rho": round(float(np.median(brand_rhos)), 4),
                "mean_rho": round(float(np.mean(brand_rhos)), 4),
                "min_rho": round(float(np.min(brand_rhos)), 4),
                "n_pairs": len(brand_rhos),
            }

    median_all = float(np.median(all_rhos)) if all_rhos else 0

    return {
        "per_brand": per_brand,
        "overall_median_rho": round(median_all, 4),
        "overall_mean_rho": round(float(np.mean(all_rhos)) if all_rhos else 0, 4),
        "total_pairs": len(all_rhos),
        "h2_confirmed": median_all > 0.70,
    }


def test_h3_scalar(records: list[dict]) -> dict:
    """H3: Kruskal-Wallis per dimension across cohorts (scalar invariance fails)."""
    results = {}
    sig_count = 0

    for i, dim in enumerate(DIMENSIONS):
        groups = {}
        for r in records:
            cid = r["cohort_id"]
            vec = weights_to_vector(r["parsed_weights"])
            groups.setdefault(cid, []).append(vec[i])

        group_arrays = [np.array(v) for k, v in sorted(groups.items()) if len(v) >= 2]

        if len(group_arrays) < 2:
            results[dim] = {"H": 0, "p": 1.0, "significant": False}
            continue

        h_stat, p_val = stats.kruskal(*group_arrays)

        # Epsilon-squared effect size for Kruskal-Wallis
        n = sum(len(g) for g in group_arrays)
        eps_sq = (h_stat - len(group_arrays) + 1) / (n - len(group_arrays))
        eps_sq = max(0, eps_sq)

        sig = p_val < 0.05
        if sig:
            sig_count += 1

        results[dim] = {
            "H": round(float(h_stat), 3),
            "p": round(float(p_val), 4),
            "epsilon_sq": round(float(eps_sq), 4),
            "significant": sig,
        }

    return {
        "per_dimension": results,
        "significant_count": sig_count,
        "h3_confirmed": sig_count >= 4,
    }


def cross_cohort_variance(records: list[dict]) -> dict:
    """Identify dimensions with highest cross-cohort variance."""
    cohort_means = {}
    for r in records:
        cid = r["cohort_id"]
        vec = weights_to_vector(r["parsed_weights"])
        cohort_means.setdefault(cid, []).append(vec)

    mean_profiles = {}
    for cid, vecs in cohort_means.items():
        mean_profiles[cid] = np.mean(vecs, axis=0)

    if not mean_profiles:
        return {"per_dimension_variance": {}}

    profile_matrix = np.array(list(mean_profiles.values()))
    variances = np.var(profile_matrix, axis=0)

    result = {}
    for i, dim in enumerate(DIMENSIONS):
        result[dim] = round(float(variances[i]), 6)

    ranked = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return {
        "per_dimension_variance": result,
        "ranked": [{"dim": d, "variance": v} for d, v in ranked],
    }


def main():
    # Look for Exp 1 data
    exp1_path = (
        Path(__file__).parent.parent.parent
        / "r15-ai-search-metamerism"
        / "experiment"
        / "L3_sessions"
        / "run15_synthetic_cohorts.jsonl"
    )

    if not exp1_path.exists():
        print(f"ERROR: {exp1_path} not found. Run Experiment 1 first.")
        sys.exit(1)

    records = load_data(exp1_path)
    print(f"Loaded {len(records)} baseline records from Experiment 1")

    cohorts_present = sorted(set(r["cohort_id"] for r in records))
    brands_present = sorted(set(r["brand"] for r in records))
    print(f"Cohorts: {cohorts_present}")
    print(f"Brands: {brands_present}")

    print("\n--- H1: Configural Invariance ---")
    h1 = test_h1_configural(records)
    if h1["total_zeroed"] == 0:
        print("  No dimensions systematically zeroed by any cohort")
    else:
        for cid, dims in h1["zeroed_dimensions"].items():
            print(f"  {cid}: zeroed {dims}")
    print(f"  H1 {'CONFIRMED' if h1['h1_confirmed'] else 'FAILS'}")

    print("\n--- H2: Metric Invariance (Spearman rho) ---")
    h2 = test_h2_metric(records)
    for brand, r in h2["per_brand"].items():
        print(
            f"  {brand:12s} median={r['median_rho']:.4f} "
            f"mean={r['mean_rho']:.4f} min={r['min_rho']:.4f} "
            f"({r['n_pairs']} pairs)"
        )
    print(
        f"  Overall median rho: {h2['overall_median_rho']:.4f}  "
        f"H2 {'CONFIRMED' if h2['h2_confirmed'] else 'FAILS'}"
    )

    print("\n--- H3: Scalar Invariance (Kruskal-Wallis) ---")
    h3 = test_h3_scalar(records)
    for dim, r in h3["per_dimension"].items():
        sig = "***" if r["significant"] else ""
        print(
            f"  {dim:14s} H={r['H']:8.3f} p={r['p']:.4f} "
            f"eps_sq={r['epsilon_sq']:.4f} {sig}"
        )
    print(
        f"  Significant: {h3['significant_count']}/8  "
        f"H3 {'CONFIRMED' if h3['h3_confirmed'] else 'FAILS'}"
    )

    print("\n--- Cross-Cohort Variance ---")
    ccv = cross_cohort_variance(records)
    for item in ccv["ranked"]:
        print(f"  {item['dim']:14s} variance={item['variance']:.6f}")

    results = {
        "experiment": "exp4_measurement_invariance",
        "date": "2026-04-16",
        "total_records": len(records),
        "h1_configural": h1,
        "h2_metric": h2,
        "h3_scalar": h3,
        "cross_cohort_variance": ccv,
    }

    results_path = Path(__file__).parent / "run17_invariance_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()
