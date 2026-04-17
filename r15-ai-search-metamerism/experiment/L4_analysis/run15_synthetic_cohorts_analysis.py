#!/usr/bin/env python3
"""Run 15: Synthetic Cohort Differentiation — Analysis.

Reads run15_synthetic_cohorts.jsonl and tests H1-H3.

Usage:
    uv run python run15_synthetic_cohorts_analysis.py
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.spatial.distance import pdist, squareform

# Fixed seed for reproducibility
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

# Expected dominant dimensions per cohort (for H3)
H3_PREDICTIONS = {
    "C1": "Ideological",
    "C2": "Semiotic",
    "C3": "Economic",
}

# Trait-profile similarity matrix (design-time, based on implied dims overlap)
# C1-C10 implied dims:
# C1: Ideo, Narr; C2: Semi, Soc; C3: Econ, Exp; C4: Soc, Semi;
# C5: Temp, Cult; C6: Soc, Cult; C7: Exp, Narr; C8: Econ, Temp;
# C9: Narr, Ideo; C10: Exp, Semi
COHORT_IDS = [f"C{i}" for i in range(1, 11)]
COHORT_DIMS = {
    "C1": {"Ideological", "Narrative"},
    "C2": {"Semiotic", "Social"},
    "C3": {"Economic", "Experiential"},
    "C4": {"Social", "Semiotic"},
    "C5": {"Temporal", "Cultural"},
    "C6": {"Social", "Cultural"},
    "C7": {"Experiential", "Narrative"},
    "C8": {"Economic", "Temporal"},
    "C9": {"Narrative", "Ideological"},
    "C10": {"Experiential", "Semiotic"},
}


def load_data(jsonl_path: Path) -> list[dict]:
    """Load and filter valid records from JSONL."""
    records = []
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if r["weights_valid"] and r["parsed_weights"]:
                records.append(r)
    return records


def weights_to_vector(weights: dict) -> np.ndarray:
    """Convert weights dict to normalized 8-d vector."""
    vec = np.array([weights[d] for d in DIMENSIONS], dtype=float)
    total = vec.sum()
    if total > 0:
        vec /= total
    return vec


def compute_cohort_profiles(
    records: list[dict],
) -> dict[str, np.ndarray]:
    """Compute mean spectral profile per cohort (across brands/models)."""
    cohort_vecs: dict[str, list[np.ndarray]] = {}
    for r in records:
        if r["condition"] != "baseline":
            continue
        cid = r["cohort_id"]
        vec = weights_to_vector(r["parsed_weights"])
        cohort_vecs.setdefault(cid, []).append(vec)

    profiles = {}
    for cid in COHORT_IDS:
        if cid in cohort_vecs and cohort_vecs[cid]:
            profiles[cid] = np.mean(cohort_vecs[cid], axis=0)
    return profiles


def test_h1(records: list[dict]) -> dict:
    """H1: ANOVA — cohort effects on dimension weights.

    Tests whether cohorts produce significantly different spectral profiles.
    One-way ANOVA per dimension, cohort as factor.
    """
    baseline = [r for r in records if r["condition"] == "baseline"]

    results = {}
    significant_count = 0

    for dim_idx, dim in enumerate(DIMENSIONS):
        groups = {}
        for r in baseline:
            cid = r["cohort_id"]
            vec = weights_to_vector(r["parsed_weights"])
            groups.setdefault(cid, []).append(vec[dim_idx])

        group_arrays = [np.array(v) for k, v in sorted(groups.items()) if len(v) >= 2]

        if len(group_arrays) < 2:
            results[dim] = {
                "F": 0,
                "p": 1.0,
                "eta_sq": 0,
                "significant": False,
            }
            continue

        f_stat, p_val = stats.f_oneway(*group_arrays)

        # Eta-squared
        all_vals = np.concatenate(group_arrays)
        grand_mean = all_vals.mean()
        ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in group_arrays)
        ss_total = np.sum((all_vals - grand_mean) ** 2)
        eta_sq = ss_between / ss_total if ss_total > 0 else 0

        sig = p_val < 0.05
        if sig:
            significant_count += 1

        results[dim] = {
            "F": round(float(f_stat), 3),
            "p": round(float(p_val), 4),
            "eta_sq": round(float(eta_sq), 4),
            "significant": sig,
        }

    return {
        "per_dimension": results,
        "significant_count": significant_count,
        "h1_supported": significant_count >= 4,
    }


def test_h2(records: list[dict]) -> dict:
    """H2: Mantel test — trait similarity predicts spectral similarity.

    Computes correlation between design-time trait distance matrix and
    observed spectral distance matrix.
    """
    profiles = compute_cohort_profiles(records)
    present = [c for c in COHORT_IDS if c in profiles]

    if len(present) < 3:
        return {"mantel_r": 0, "p": 1.0, "h2_supported": False}

    # Trait distance matrix (Jaccard distance on implied dim sets)
    n = len(present)
    trait_dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            s1 = COHORT_DIMS[present[i]]
            s2 = COHORT_DIMS[present[j]]
            if s1 | s2:
                trait_dist[i, j] = 1.0 - len(s1 & s2) / len(s1 | s2)

    # Spectral distance matrix (Euclidean on mean profiles)
    profile_matrix = np.array([profiles[c] for c in present])
    spec_dist = squareform(pdist(profile_matrix, metric="euclidean"))

    # Mantel test: Pearson correlation on upper-triangle elements
    idx = np.triu_indices(n, k=1)
    trait_vec = trait_dist[idx]
    spec_vec = spec_dist[idx]

    if len(trait_vec) < 3 or np.std(trait_vec) == 0 or np.std(spec_vec) == 0:
        return {"mantel_r": 0, "p": 1.0, "h2_supported": False}

    observed_r = float(np.corrcoef(trait_vec, spec_vec)[0, 1])

    # Permutation test (999 permutations)
    n_perm = 999
    count_ge = 0
    for _ in range(n_perm):
        perm = RNG.permutation(n)
        perm_spec = spec_dist[np.ix_(perm, perm)]
        perm_vec = perm_spec[idx]
        perm_r = np.corrcoef(trait_vec, perm_vec)[0, 1]
        if perm_r >= observed_r:
            count_ge += 1

    p_val = (count_ge + 1) / (n_perm + 1)

    return {
        "mantel_r": round(observed_r, 4),
        "p": round(float(p_val), 4),
        "n_permutations": n_perm,
        "h2_supported": observed_r > 0.30,
    }


def test_h3(records: list[dict]) -> dict:
    """H3: Dimension-specific sensitivity.

    Tests whether C1 weights Ideological higher than other cohorts,
    C2 weights Semiotic higher, C3 weights Economic higher.
    """
    baseline = [r for r in records if r["condition"] == "baseline"]
    results = {}
    confirmed = 0

    for target_cohort, target_dim in H3_PREDICTIONS.items():
        dim_idx = DIMENSIONS.index(target_dim)

        target_vals = []
        other_vals = []
        for r in baseline:
            vec = weights_to_vector(r["parsed_weights"])
            if r["cohort_id"] == target_cohort:
                target_vals.append(vec[dim_idx])
            else:
                other_vals.append(vec[dim_idx])

        if len(target_vals) < 2 or len(other_vals) < 2:
            results[target_cohort] = {
                "target_dim": target_dim,
                "target_mean": 0,
                "other_mean": 0,
                "t": 0,
                "p": 1.0,
                "d": 0,
                "confirmed": False,
            }
            continue

        t_stat, p_val = stats.ttest_ind(target_vals, other_vals)

        # One-sided: target should be HIGHER
        p_one = p_val / 2 if t_stat > 0 else 1 - p_val / 2

        # Cohen's d
        pooled_std = np.sqrt(
            (
                (len(target_vals) - 1) * np.var(target_vals, ddof=1)
                + (len(other_vals) - 1) * np.var(other_vals, ddof=1)
            )
            / (len(target_vals) + len(other_vals) - 2)
        )
        cohens_d = (
            (np.mean(target_vals) - np.mean(other_vals)) / pooled_std
            if pooled_std > 0
            else 0
        )

        is_confirmed = p_one < 0.05 and t_stat > 0
        if is_confirmed:
            confirmed += 1

        results[target_cohort] = {
            "target_dim": target_dim,
            "target_mean": round(float(np.mean(target_vals)), 4),
            "other_mean": round(float(np.mean(other_vals)), 4),
            "t": round(float(t_stat), 3),
            "p_one_sided": round(float(p_one), 4),
            "cohens_d": round(float(cohens_d), 3),
            "confirmed": is_confirmed,
        }

    return {
        "predictions": results,
        "confirmed_count": confirmed,
        "h3_supported": confirmed >= 2,
    }


def robustness_check(records: list[dict]) -> dict:
    """Compare fixed vs scrambled dimension order results."""
    baseline = [r for r in records if r["condition"] == "baseline"]
    scrambled = [r for r in records if r["condition"] == "robustness_scrambled"]

    if not scrambled:
        return {"spearman_rho": None, "note": "No robustness calls found"}

    # Match by (cohort, brand, model) and compare
    baseline_map = {}
    for r in baseline:
        key = (r["cohort_id"], r["brand"], r["model_id"])
        vec = weights_to_vector(r["parsed_weights"])
        baseline_map.setdefault(key, []).append(vec)

    fixed_vals = []
    scrambled_vals = []
    for r in scrambled:
        key = (r["cohort_id"], r["brand"], r["model_id"])
        if key in baseline_map and baseline_map[key]:
            fixed_mean = np.mean(baseline_map[key], axis=0)
            scram_vec = weights_to_vector(r["parsed_weights"])
            fixed_vals.extend(fixed_mean.tolist())
            scrambled_vals.extend(scram_vec.tolist())

    if len(fixed_vals) < 3:
        return {"spearman_rho": None, "note": "Insufficient matched pairs"}

    rho, p_val = stats.spearmanr(fixed_vals, scrambled_vals)
    return {
        "spearman_rho": round(float(rho), 4),
        "p": round(float(p_val), 6),
        "n_pairs": len(fixed_vals),
        "invariant": rho > 0.90,
    }


def cosine_similarity_matrix(
    records: list[dict],
) -> dict:
    """Compute cosine similarity between all cohort pairs."""
    profiles = compute_cohort_profiles(records)
    present = sorted(profiles.keys())

    matrix = {}
    for i, c1 in enumerate(present):
        for j, c2 in enumerate(present):
            if i <= j:
                v1, v2 = profiles[c1], profiles[c2]
                cos = float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                matrix[f"{c1}-{c2}"] = round(cos, 4)

    return {"cohort_pairs": matrix, "n_cohorts": len(present)}


def main():
    data_dir = Path(__file__).parent.parent / "L3_sessions"
    jsonl_path = data_dir / "run15_synthetic_cohorts.jsonl"

    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found. Run the experiment first.")
        sys.exit(1)

    records = load_data(jsonl_path)
    print(f"Loaded {len(records)} valid records from {jsonl_path}")

    baseline = [r for r in records if r["condition"] == "baseline"]
    print(f"Baseline records: {len(baseline)}")
    print(
        f"Robustness records: "
        f"{len([r for r in records if r['condition'] == 'robustness_scrambled'])}"
    )

    # Run all tests
    print("\n--- H1: Cohort Effects (ANOVA) ---")
    h1 = test_h1(records)
    for dim, res in h1["per_dimension"].items():
        sig_mark = "***" if res["significant"] else ""
        print(
            f"  {dim:14s} F={res['F']:8.3f}  "
            f"p={res['p']:.4f}  "
            f"eta_sq={res['eta_sq']:.4f} {sig_mark}"
        )
    print(
        f"  Significant dims: {h1['significant_count']}/8  "
        f"H1 {'SUPPORTED' if h1['h1_supported'] else 'NOT SUPPORTED'}"
    )

    print("\n--- H2: Mantel Test ---")
    h2 = test_h2(records)
    print(
        f"  Mantel r = {h2['mantel_r']:.4f}, "
        f"p = {h2['p']:.4f}  "
        f"H2 {'SUPPORTED' if h2['h2_supported'] else 'NOT SUPPORTED'}"
    )

    print("\n--- H3: Dimension-Specific Sensitivity ---")
    h3 = test_h3(records)
    for cid, res in h3["predictions"].items():
        conf = "CONFIRMED" if res["confirmed"] else "NOT CONFIRMED"
        print(
            f"  {cid} -> {res['target_dim']:14s} "
            f"mean={res['target_mean']:.4f} vs {res['other_mean']:.4f}  "
            f"t={res['t']:.3f}  p={res.get('p_one_sided', 1.0):.4f}  "
            f"d={res['cohens_d']:.3f}  {conf}"
        )
    print(
        f"  Confirmed: {h3['confirmed_count']}/3  "
        f"H3 {'SUPPORTED' if h3['h3_supported'] else 'NOT SUPPORTED'}"
    )

    print("\n--- Robustness Check ---")
    rob = robustness_check(records)
    if rob["spearman_rho"] is not None:
        print(
            f"  Spearman rho = {rob['spearman_rho']:.4f}, "
            f"p = {rob['p']:.6f}  "
            f"{'INVARIANT' if rob['invariant'] else 'NOT INVARIANT'}"
        )
    else:
        print(f"  {rob.get('note', 'No data')}")

    print("\n--- Cosine Similarity Matrix ---")
    cos_mat = cosine_similarity_matrix(records)
    print(f"  {cos_mat['n_cohorts']} cohorts")

    # Compute summary statistics
    total_cost = sum(r.get("api_cost_usd", 0) for r in records)

    # Save results
    results = {
        "experiment": "exp1_cohort_differentiation",
        "date": "2026-04-16",
        "total_records": len(records),
        "baseline_records": len(baseline),
        "total_cost_usd": round(total_cost, 4),
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "robustness": rob,
        "cosine_similarity": cos_mat,
    }

    results_path = Path(__file__).parent / "run15_synthetic_cohorts_results.json"

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.bool_,)):
                return bool(obj)
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            return super().default(obj)

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
    print(f"\nResults saved to {results_path}")

    return results


if __name__ == "__main__":
    main()
