"""
Gap 5: Dimension Robustness Analysis
=====================================
Tests whether SBT's 8-dimension framework is robust to dimensional perturbation
using R15 empirical data (21,350 API calls, 24 LLMs).

Questions answered:
1. What happens to DCI rankings if you use 7 dimensions (drop-one)?
2. What happens with 6 dimensions (drop-pair)?
3. Which dimensions are most/least critical to ranking stability?
4. Is 8 the minimum complete set, or could fewer dimensions suffice?

Data source: sbt-papers/r15-ai-search-metamerism/experiment/L4_analysis/run5_results.json
"""

import json
import itertools
import sys
from pathlib import Path

import numpy as np
from scipy import stats as sp_stats

# ---------------------------------------------------------------------------
# Configuration
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

DATA_PATH = (
    Path.home()
    / "projects"
    / "sbt-papers"
    / "r15-ai-search-metamerism"
    / "experiment"
    / "L4_analysis"
    / "run5_results.json"
)

OUTPUT_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_data():
    """Load R15 run5 aggregated results."""
    with open(DATA_PATH) as f:
        data = json.load(f)

    # Per-model weight profiles (aggregated across brand pairs)
    weight_profiles = data["weight_profiles"]  # {model: {dim: mean_weight}}

    # Per-call raw data for per-model-per-pair granularity
    calls = data["calls"]
    wr_calls = [
        c
        for c in calls
        if c.get("prompt_type") == "weighted_recommendation"
        and c.get("parsed")
        and isinstance(c["parsed"].get("weights"), dict)
    ]

    # Build per-model-per-pair weight vectors
    model_pair_weights = {}
    for c in wr_calls:
        key = (c["model"], c.get("brand_pair", c.get("pair_id", "unknown")))
        weights = c["parsed"]["weights"]
        if not all(d in weights for d in DIMENSIONS):
            continue
        vec = np.array([weights[d] for d in DIMENSIONS], dtype=float)
        total = vec.sum()
        if total < 50 or total > 150:
            continue
        vec = vec / total * 100  # renormalize to sum=100
        model_pair_weights.setdefault(key, []).append(vec)

    # Average within each model-pair combo
    model_pair_means = {}
    for key, vecs in model_pair_weights.items():
        model_pair_means[key] = np.mean(vecs, axis=0)

    # Also build per-model aggregate profiles from the JSON
    model_profiles = {}
    for model, profile in weight_profiles.items():
        if all(d in profile for d in DIMENSIONS):
            vec = np.array([profile[d] for d in DIMENSIONS], dtype=float)
            model_profiles[model] = vec

    return model_profiles, model_pair_means, data


# ---------------------------------------------------------------------------
# DCI computation
# ---------------------------------------------------------------------------


def compute_dci(weight_vec, dim_indices_map, econ_idx, sem_idx):
    """
    Compute DCI from a weight vector.

    DCI = (w_economic + w_semiotic) / sum(all_weights)

    For reduced dimensions, we recompute over the subset.
    econ_idx and sem_idx are indices into the ORIGINAL 8-dim vector.
    dim_indices_map maps original indices to whether they're included.
    """
    subset = weight_vec[list(dim_indices_map)]
    total = subset.sum()
    if total == 0:
        return np.nan

    # Check if economic and semiotic are in the subset
    econ_in = econ_idx in dim_indices_map
    sem_in = sem_idx in dim_indices_map

    numerator = 0
    if econ_in:
        numerator += weight_vec[econ_idx]
    if sem_in:
        numerator += weight_vec[sem_idx]

    return numerator / total


def compute_dci_for_dims(weight_vec, keep_indices):
    """Compute DCI keeping only specified dimension indices."""
    econ_idx = DIMENSIONS.index("economic")
    sem_idx = DIMENSIONS.index("semiotic")

    subset = weight_vec[keep_indices]
    total = subset.sum()
    if total == 0:
        return np.nan

    numerator = 0
    if econ_idx in keep_indices:
        numerator += weight_vec[econ_idx]
    if sem_idx in keep_indices:
        numerator += weight_vec[sem_idx]

    return numerator / total


def compute_model_dcis(model_profiles, keep_indices):
    """Compute DCI for all models with given dimension subset."""
    dcis = {}
    for model, vec in model_profiles.items():
        dcis[model] = compute_dci_for_dims(vec, keep_indices)
    return dcis


def rank_models(dcis):
    """Return model ranking (sorted by DCI descending)."""
    return sorted(dcis.keys(), key=lambda m: dcis[m], reverse=True)


def rank_correlation(dcis_a, dcis_b):
    """Spearman rank correlation between two DCI dictionaries."""
    common = sorted(set(dcis_a.keys()) & set(dcis_b.keys()))
    if len(common) < 3:
        return np.nan, np.nan
    a = [dcis_a[m] for m in common]
    b = [dcis_b[m] for m in common]
    rho, p = sp_stats.spearmanr(a, b)
    return rho, p


def cosine_sim(dcis_a, dcis_b):
    """Cosine similarity between DCI vectors."""
    common = sorted(set(dcis_a.keys()) & set(dcis_b.keys()))
    if len(common) < 2:
        return np.nan
    a = np.array([dcis_a[m] for m in common])
    b = np.array([dcis_b[m] for m in common])
    dot = np.dot(a, b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return np.nan
    return dot / norm


def mean_abs_rank_displacement(rank_a, rank_b):
    """Mean absolute rank displacement between two rankings."""
    pos_a = {m: i for i, m in enumerate(rank_a)}
    pos_b = {m: i for i, m in enumerate(rank_b)}
    common = set(pos_a.keys()) & set(pos_b.keys())
    if not common:
        return np.nan
    return np.mean([abs(pos_a[m] - pos_b[m]) for m in common])


# ---------------------------------------------------------------------------
# Perturbation experiments
# ---------------------------------------------------------------------------


def drop_one_analysis(model_profiles):
    """Drop each dimension in turn (8 variants of 7D)."""
    all_indices = list(range(8))
    baseline_dcis = compute_model_dcis(model_profiles, all_indices)
    baseline_rank = rank_models(baseline_dcis)

    results = []
    for drop_idx in range(8):
        dim_name = DIMENSIONS[drop_idx]
        keep = [i for i in all_indices if i != drop_idx]
        reduced_dcis = compute_model_dcis(model_profiles, keep)
        reduced_rank = rank_models(reduced_dcis)

        rho, p_rho = rank_correlation(baseline_dcis, reduced_dcis)
        cos = cosine_sim(baseline_dcis, reduced_dcis)
        mard = mean_abs_rank_displacement(baseline_rank, reduced_rank)

        # Mean DCI change
        common = sorted(set(baseline_dcis.keys()) & set(reduced_dcis.keys()))
        dci_deltas = [reduced_dcis[m] - baseline_dcis[m] for m in common]
        mean_delta = np.mean(dci_deltas)
        std_delta = np.std(dci_deltas, ddof=1)

        results.append(
            {
                "dropped": dim_name,
                "spearman_rho": rho,
                "spearman_p": p_rho,
                "cosine_sim": cos,
                "mean_rank_displacement": mard,
                "mean_dci_delta": mean_delta,
                "std_dci_delta": std_delta,
                "n_models": len(common),
            }
        )

    return results, baseline_dcis


def drop_pair_analysis(model_profiles, n_samples=15):
    """Drop pairs of dimensions (sample from 28 combinations)."""
    all_indices = list(range(8))
    baseline_dcis = compute_model_dcis(model_profiles, all_indices)
    baseline_rank = rank_models(baseline_dcis)

    all_pairs = list(itertools.combinations(range(8), 2))
    # Include all 28 pairs -- it's computationally trivial
    results = []
    for drop_pair in all_pairs:
        dim_names = (DIMENSIONS[drop_pair[0]], DIMENSIONS[drop_pair[1]])
        keep = [i for i in all_indices if i not in drop_pair]
        reduced_dcis = compute_model_dcis(model_profiles, keep)
        reduced_rank = rank_models(reduced_dcis)

        rho, p_rho = rank_correlation(baseline_dcis, reduced_dcis)
        cos = cosine_sim(baseline_dcis, reduced_dcis)
        mard = mean_abs_rank_displacement(baseline_rank, reduced_rank)

        common = sorted(set(baseline_dcis.keys()) & set(reduced_dcis.keys()))
        dci_deltas = [reduced_dcis[m] - baseline_dcis[m] for m in common]
        mean_delta = np.mean(dci_deltas)

        results.append(
            {
                "dropped": f"{dim_names[0]} + {dim_names[1]}",
                "spearman_rho": rho,
                "spearman_p": p_rho,
                "cosine_sim": cos,
                "mean_rank_displacement": mard,
                "mean_dci_delta": mean_delta,
                "n_models": len(common),
            }
        )

    return results


def augmented_dimension_analysis(model_profiles, model_pair_means):
    """
    Test 10D: add 2 synthetic dimensions (split experiential into
    functional + hedonic; split economic into price + accessibility).

    Since we don't have separate sub-dimension data, we simulate by
    splitting each target dimension's weight with noise.
    """
    np.random.seed(42)
    all_indices = list(range(8))
    baseline_dcis = compute_model_dcis(model_profiles, all_indices)

    # For each model, split experiential (idx 3) and economic (idx 5)
    augmented_profiles = {}
    for model, vec in model_profiles.items():
        new_vec = np.zeros(10)
        # Copy non-split dimensions
        mapping = {0: 0, 1: 1, 2: 2, 4: 4, 6: 7, 7: 8}  # old -> new
        for old, new in mapping.items():
            new_vec[new] = vec[old]

        # Split experiential (old 3) -> functional (new 3) + hedonic (new 9)
        split_ratio = 0.5 + np.random.normal(0, 0.1)
        split_ratio = np.clip(split_ratio, 0.2, 0.8)
        new_vec[3] = vec[3] * split_ratio
        new_vec[9] = vec[3] * (1 - split_ratio)

        # Split economic (old 5) -> price (new 5) + accessibility (new 6)
        split_ratio = 0.5 + np.random.normal(0, 0.1)
        split_ratio = np.clip(split_ratio, 0.2, 0.8)
        new_vec[5] = vec[5] * split_ratio
        new_vec[6] = vec[5] * (1 - split_ratio)

        augmented_profiles[model] = new_vec

    # DCI in 10D: economic components are indices 5,6; semiotic is 0
    augmented_dcis = {}
    for model, vec in augmented_profiles.items():
        total = vec.sum()
        if total == 0:
            continue
        # Economic = price (5) + accessibility (6); semiotic = 0
        augmented_dcis[model] = (vec[5] + vec[6] + vec[0]) / total

    rho, p_rho = rank_correlation(baseline_dcis, augmented_dcis)
    cos = cosine_sim(baseline_dcis, augmented_dcis)

    return {
        "spearman_rho": rho,
        "spearman_p": p_rho,
        "cosine_sim": cos,
        "n_models": len(augmented_dcis),
        "note": "Synthetic 10D via splitting experiential and economic",
    }


def profile_stability_analysis(model_profiles):
    """
    Test spectral profile cosine similarity under dimension reduction.
    Not just DCI ranking, but full profile shape preservation.
    """
    all_indices = list(range(8))
    models = sorted(model_profiles.keys())

    # Baseline: mean pairwise cosine of 8D profiles
    vecs_8d = [model_profiles[m] for m in models]
    n = len(vecs_8d)
    baseline_cosines = []
    for i in range(n):
        for j in range(i + 1, n):
            a, b = vecs_8d[i], vecs_8d[j]
            cos = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            baseline_cosines.append(cos)
    mean_8d = np.mean(baseline_cosines)

    # For each 7D variant
    results = []
    for drop_idx in range(8):
        keep = [i for i in all_indices if i != drop_idx]
        vecs_7d = [model_profiles[m][keep] for m in models]
        cosines_7d = []
        for i in range(n):
            for j in range(i + 1, n):
                a, b = vecs_7d[i], vecs_7d[j]
                norm = np.linalg.norm(a) * np.linalg.norm(b)
                if norm > 0:
                    cosines_7d.append(np.dot(a, b) / norm)
        mean_7d = np.mean(cosines_7d)
        results.append(
            {
                "dropped": DIMENSIONS[drop_idx],
                "mean_pairwise_cosine_8d": mean_8d,
                "mean_pairwise_cosine_7d": mean_7d,
                "delta": mean_7d - mean_8d,
            }
        )

    return results


def information_loss_analysis(model_profiles):
    """
    Quantify information loss via explained variance.
    For each dimension removed, compute what fraction of total
    variance in model profiles is lost.
    """
    models = sorted(model_profiles.keys())
    matrix = np.array([model_profiles[m] for m in models])  # N_models x 8

    total_var = np.var(matrix, axis=0).sum()

    results = []
    for drop_idx in range(8):
        dim_var = np.var(matrix[:, drop_idx])
        frac_lost = dim_var / total_var if total_var > 0 else 0
        results.append(
            {
                "dimension": DIMENSIONS[drop_idx],
                "variance": dim_var,
                "fraction_of_total": frac_lost,
                "mean_weight": np.mean(matrix[:, drop_idx]),
                "std_weight": np.std(matrix[:, drop_idx], ddof=1),
            }
        )

    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def fmt_p(p):
    """Format p-value per paper quality standards."""
    if p is None or np.isnan(p):
        return "—"
    if p < 0.001:
        return "< .001"
    return f"= .{int(round(p, 3) * 1000):03d}"


def fmt_r(r):
    """Format correlation/cosine (no leading zero if |r| < 1)."""
    if r is None or np.isnan(r):
        return "—"
    if abs(r) >= 0.9995:
        return "-1.000" if r < 0 else "1.000"
    sign = "-" if r < 0 else ""
    return f"{sign}.{abs(round(r, 3) * 1000):03.0f}"


def fmt_d(d):
    """Format decimal (allow leading zero if > 1)."""
    if d is None or np.isnan(d):
        return "—"
    if abs(d) >= 1:
        return f"{d:.3f}"
    sign = "-" if d < 0 else ""
    return f"{sign}.{abs(round(d, 3) * 1000):03.0f}"


def print_drop_one_table(results):
    print("\n## Drop-One Analysis (8D -> 7D)")
    print(
        f"{'Dropped':<14} {'Spearman rho':<14} {'p':<10} {'Cosine':<10} {'Mean rank Δ':<12} {'Mean DCI Δ':<12}"
    )
    print("-" * 72)
    for r in sorted(results, key=lambda x: x["cosine_sim"]):
        print(
            f"{r['dropped']:<14} {fmt_r(r['spearman_rho']):<14} {fmt_p(r['spearman_p']):<10} "
            f"{fmt_r(r['cosine_sim']):<10} {r['mean_rank_displacement']:<12.2f} {fmt_d(r['mean_dci_delta']):<12}"
        )


def print_drop_pair_table(results, top_n=10):
    print(f"\n## Drop-Pair Analysis (8D -> 6D) — Top {top_n} Most Disruptive")
    sorted_results = sorted(results, key=lambda x: x["cosine_sim"])
    print(
        f"{'Dropped pair':<30} {'Spearman rho':<14} {'Cosine':<10} {'Mean rank Δ':<12}"
    )
    print("-" * 66)
    for r in sorted_results[:top_n]:
        print(
            f"{r['dropped']:<30} {fmt_r(r['spearman_rho']):<14} {fmt_r(r['cosine_sim']):<10} {r['mean_rank_displacement']:<12.2f}"
        )

    print(f"\n## Drop-Pair Analysis — Top {top_n} Most Stable")
    for r in sorted_results[-top_n:]:
        print(
            f"{r['dropped']:<30} {fmt_r(r['spearman_rho']):<14} {fmt_r(r['cosine_sim']):<10} {r['mean_rank_displacement']:<12.2f}"
        )


def print_variance_table(results):
    print("\n## Per-Dimension Variance (Information Content)")
    print(
        f"{'Dimension':<14} {'Mean weight':<12} {'SD':<10} {'Variance':<12} {'% of total':<12}"
    )
    print("-" * 60)
    for r in sorted(results, key=lambda x: -x["fraction_of_total"]):
        pct = r["fraction_of_total"] * 100
        print(
            f"{r['dimension']:<14} {r['mean_weight']:<12.2f} {r['std_weight']:<10.2f} "
            f"{r['variance']:<12.3f} {pct:<12.1f}%"
        )


def print_profile_stability(results):
    print("\n## Profile Shape Stability (Mean Pairwise Cosine)")
    print(f"{'Dropped':<14} {'8D cosine':<12} {'7D cosine':<12} {'Delta':<10}")
    print("-" * 48)
    for r in sorted(results, key=lambda x: x["delta"]):
        print(
            f"{r['dropped']:<14} {fmt_r(r['mean_pairwise_cosine_8d']):<12} "
            f"{fmt_r(r['mean_pairwise_cosine_7d']):<12} {r['delta']:+.4f}"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=" * 72)
    print("Gap 5: Dimension Robustness Analysis")
    print("Data: R15 Run 5 (22 models, 8 brand pairs, 3 runs)")
    print("=" * 72)

    model_profiles, model_pair_means, raw_data = load_data()
    print(
        f"\nLoaded {len(model_profiles)} model profiles, "
        f"{len(model_pair_means)} model-pair combinations"
    )

    # --- Baseline ---
    baseline_dcis = compute_model_dcis(model_profiles, list(range(8)))
    baseline_values = list(baseline_dcis.values())
    print(
        f"\nBaseline 8D DCI: mean = {fmt_d(np.mean(baseline_values))}, "
        f"SD = {fmt_d(np.std(baseline_values, ddof=1))}, "
        f"range [{fmt_d(min(baseline_values))}, {fmt_d(max(baseline_values))}]"
    )

    # --- Drop-one ---
    drop_one_results, _ = drop_one_analysis(model_profiles)
    print_drop_one_table(drop_one_results)

    # Summary statistics for drop-one
    rhos = [r["spearman_rho"] for r in drop_one_results]
    cosines = [r["cosine_sim"] for r in drop_one_results]
    print(
        f"\nDrop-one summary: Spearman rho range [{fmt_r(min(rhos))}, {fmt_r(max(rhos))}], "
        f"mean {fmt_r(np.mean(rhos))}"
    )
    print(
        f"Drop-one summary: Cosine range [{fmt_r(min(cosines))}, {fmt_r(max(cosines))}], "
        f"mean {fmt_r(np.mean(cosines))}"
    )

    # --- Drop-pair ---
    drop_pair_results = drop_pair_analysis(model_profiles)
    print_drop_pair_table(drop_pair_results)

    pair_rhos = [
        r["spearman_rho"] for r in drop_pair_results if not np.isnan(r["spearman_rho"])
    ]
    pair_cosines = [
        r["cosine_sim"] for r in drop_pair_results if not np.isnan(r["cosine_sim"])
    ]
    print(
        f"\nDrop-pair summary: Spearman rho range [{fmt_r(min(pair_rhos))}, {fmt_r(max(pair_rhos))}], "
        f"mean {fmt_r(np.mean(pair_rhos))}"
    )
    print(
        f"Drop-pair summary: Cosine range [{fmt_r(min(pair_cosines))}, {fmt_r(max(pair_cosines))}], "
        f"mean {fmt_r(np.mean(pair_cosines))}"
    )

    # --- Augmented 10D ---
    aug_result = augmented_dimension_analysis(model_profiles, model_pair_means)
    print(f"\n## Augmented 10D Analysis")
    print(
        f"Spearman rho: {fmt_r(aug_result['spearman_rho'])}, p {fmt_p(aug_result['spearman_p'])}"
    )
    print(f"Cosine similarity: {fmt_r(aug_result['cosine_sim'])}")
    print(f"Note: {aug_result['note']}")

    # --- Variance decomposition ---
    var_results = information_loss_analysis(model_profiles)
    print_variance_table(var_results)

    # --- Profile stability ---
    stability_results = profile_stability_analysis(model_profiles)
    print_profile_stability(stability_results)

    # --- Critical dimension identification ---
    print("\n## Critical Dimension Ranking")
    print("(Ordered by disruption when removed: most critical first)")
    print()
    drop_one_sorted = sorted(drop_one_results, key=lambda x: x["cosine_sim"])
    for i, r in enumerate(drop_one_sorted, 1):
        econ_idx = DIMENSIONS.index("economic")
        sem_idx = DIMENSIONS.index("semiotic")
        dropped_idx = DIMENSIONS.index(r["dropped"])
        is_dci_component = dropped_idx in (econ_idx, sem_idx)
        marker = " [DCI component]" if is_dci_component else ""
        print(
            f"  {i}. {r['dropped']:<14} cosine = {fmt_r(r['cosine_sim'])}, "
            f"rho = {fmt_r(r['spearman_rho'])}{marker}"
        )

    # --- Effect size: is any single dimension indispensable? ---
    print("\n## Indispensability Test")
    print(
        "If ALL drop-one cosines > .990, no single dimension is indispensable for ranking."
    )
    print("If ANY drop-one cosine < .950, that dimension is structurally critical.")
    all_high = all(c > 0.990 for c in cosines)
    any_critical = any(c < 0.950 for c in cosines)
    print(f"All > .990: {all_high}")
    print(f"Any < .950: {any_critical}")
    if all_high:
        print("=> Ranking is robust to single-dimension removal.")
    if any_critical:
        critical = [r["dropped"] for r in drop_one_results if r["cosine_sim"] < 0.950]
        print(f"=> Critical dimensions: {', '.join(critical)}")

    # --- 6D threshold ---
    print("\n## 6D Stability Threshold")
    stable_6d = [r for r in drop_pair_results if r["cosine_sim"] > 0.990]
    unstable_6d = [r for r in drop_pair_results if r["cosine_sim"] < 0.950]
    print(
        f"Pairs with cosine > .990 (stable): {len(stable_6d)} / {len(drop_pair_results)}"
    )
    print(
        f"Pairs with cosine < .950 (unstable): {len(unstable_6d)} / {len(drop_pair_results)}"
    )

    # --- Save results as JSON ---
    output = {
        "metadata": {
            "analysis": "Gap 5: Dimension Robustness",
            "data_source": "R15 Run 5",
            "n_models": len(model_profiles),
            "dimensions": DIMENSIONS,
        },
        "baseline": {
            "mean_dci": float(np.mean(baseline_values)),
            "std_dci": float(np.std(baseline_values, ddof=1)),
            "min_dci": float(min(baseline_values)),
            "max_dci": float(max(baseline_values)),
        },
        "drop_one": drop_one_results,
        "drop_pair": drop_pair_results,
        "augmented_10d": aug_result,
        "variance_decomposition": var_results,
        "profile_stability": stability_results,
    }

    out_path = OUTPUT_DIR / "gap5_dimension_robustness_results.json"
    with open(out_path, "w") as f:
        json.dump(
            output,
            f,
            indent=2,
            default=lambda x: float(x) if isinstance(x, np.floating) else x,
        )
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
