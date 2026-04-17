#!/usr/bin/env python3
"""Analysis script for Experiment B: Cross-Language Semantic Drift.

Reads exp_cross_language.jsonl, computes:
1. Per-language x condition mean spectral profiles
2. Cross-language cosine similarity matrix (H1)
3. Condition A vs B drift magnitude per language (H2)
4. Dimension-specific cultural drift (H3)
5. Collectivist vs individualist Social weights (H4)
6. Exploratory: model x language interaction, clustering

Usage:
    uv run python exp_cross_language_analysis.py
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DIMENSIONS = [
    "Semiotic", "Narrative", "Ideological", "Experiential",
    "Social", "Economic", "Cultural", "Temporal",
]

LANGUAGES = ["en", "zh", "ru", "ja", "ko", "ar", "hi", "es"]

COLLECTIVIST = {"zh", "ja", "ko"}
INDIVIDUALIST = {"en", "es"}

BOOTSTRAP_SEED = 12345
BOOTSTRAP_N = 10000

CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_data(jsonl_path: Path) -> list[dict]:
    records = []
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if r["weights_valid"] and r["parsed_weights"]:
                records.append(r)
    return records


def normalize_weights(weights: dict) -> np.ndarray:
    """Normalize parsed weights to sum to 1, in canonical dimension order."""
    raw = np.array([float(weights[d]) for d in DIMENSIONS])
    total = raw.sum()
    if total == 0:
        return np.ones(8) / 8
    return raw / total


# ---------------------------------------------------------------------------
# Analysis Functions
# ---------------------------------------------------------------------------

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    dot = np.dot(a, b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0.0
    return float(dot / norm)


def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return float((np.mean(group1) - np.mean(group2)) / pooled_std)


def paired_cohens_d(diffs: np.ndarray) -> float:
    std = np.std(diffs, ddof=1)
    if std == 0:
        return 0.0
    return float(np.mean(diffs) / std)


def bootstrap_ci(data: np.ndarray, stat_func=np.mean, n_boot=BOOTSTRAP_N,
                  ci=.95, seed=BOOTSTRAP_SEED) -> tuple[float, float]:
    rng = np.random.RandomState(seed)
    stats_arr = np.array([
        stat_func(rng.choice(data, size=len(data), replace=True))
        for _ in range(n_boot)
    ])
    alpha = (1 - ci) / 2
    return float(np.percentile(stats_arr, 100 * alpha)), \
        float(np.percentile(stats_arr, 100 * (1 - alpha)))


# ---------------------------------------------------------------------------
# Main Analysis
# ---------------------------------------------------------------------------

def analyze(jsonl_path: Path, output_dir: Path):
    records = load_data(jsonl_path)
    print(f"Loaded {len(records)} valid records")

    # Group by language, condition
    by_lang_cond = defaultdict(list)
    for r in records:
        key = (r["language"], r["condition"])
        by_lang_cond[key].append(r)

    # Summary counts
    print("\n--- Record Counts ---")
    for lang in LANGUAGES:
        for cond in ["bilingual", "native_only"]:
            key = (lang, cond)
            n = len(by_lang_cond.get(key, []))
            if n > 0:
                print(f"  {lang} {cond}: {n}")

    # -----------------------------------------------------------------------
    # 1. Per-language x condition mean spectral profiles
    # -----------------------------------------------------------------------
    print("\n--- Mean Spectral Profiles ---")
    profiles = {}
    for (lang, cond), recs in by_lang_cond.items():
        vecs = [normalize_weights(r["parsed_weights"]) for r in recs]
        mean_profile = np.mean(vecs, axis=0)
        profiles[(lang, cond)] = mean_profile
        weights_pct = [f"{v*100:.1f}" for v in mean_profile]
        print(f"  {lang} {cond}: [{', '.join(weights_pct)}]")

    # -----------------------------------------------------------------------
    # 2. H1: Cross-language cosine similarity under bilingual anchoring
    # -----------------------------------------------------------------------
    print("\n--- H1: Cross-Language Cosine Similarity (Bilingual Condition) ---")

    # Per-brand cosine matrix
    brands = list(CANONICAL_PROFILES.keys())
    all_cosines = []

    for brand in brands:
        brand_profiles = {}
        for lang in LANGUAGES:
            recs = [
                r for r in by_lang_cond.get((lang, "bilingual"), [])
                if r["brand"] == brand
            ]
            if recs:
                vecs = [normalize_weights(r["parsed_weights"]) for r in recs]
                brand_profiles[lang] = np.mean(vecs, axis=0)

        cosines = []
        langs = list(brand_profiles.keys())
        for i in range(len(langs)):
            for j in range(i + 1, len(langs)):
                cos = cosine_similarity(
                    brand_profiles[langs[i]], brand_profiles[langs[j]]
                )
                cosines.append(cos)
                all_cosines.append(cos)

        if cosines:
            med = np.median(cosines)
            mn = np.min(cosines)
            mx = np.max(cosines)
            print(f"  {brand}: median={med:.3f}, min={mn:.3f}, max={mx:.3f} "
                  f"(n={len(cosines)} pairs)")

    if all_cosines:
        overall_med = np.median(all_cosines)
        overall_min = np.min(all_cosines)
        h1_pass = overall_med > .90
        print(f"\n  OVERALL: median={overall_med:.3f}, min={overall_min:.3f}")
        print(f"  H1 {'SUPPORTED' if h1_pass else 'NOT SUPPORTED'}: "
              f"median cosine {'>' if h1_pass else '<='} .90")

    # -----------------------------------------------------------------------
    # 3. H2: Condition A vs B drift magnitude per language
    # -----------------------------------------------------------------------
    print("\n--- H2: Native-Only Drift Magnitude ---")

    non_english = [l for l in LANGUAGES if l != "en"]
    h2_results = {}
    h2_sig_count = 0
    bonferroni_alpha_h2 = .05 / 7

    for lang in non_english:
        bi_recs = by_lang_cond.get((lang, "bilingual"), [])
        nat_recs = by_lang_cond.get((lang, "native_only"), [])

        if not bi_recs or not nat_recs:
            print(f"  {lang}: SKIP (missing condition data)")
            continue

        # Compute per-observation absolute drift across 8 dimensions
        bi_vecs = [normalize_weights(r["parsed_weights"]) for r in bi_recs]
        nat_vecs = [normalize_weights(r["parsed_weights"]) for r in nat_recs]

        bi_mean = np.mean(bi_vecs, axis=0)
        nat_mean = np.mean(nat_vecs, axis=0)

        # Mean absolute drift per dimension
        abs_drift = np.abs(nat_mean - bi_mean) * 100
        mean_drift = np.mean(abs_drift)

        # Per-dimension weight arrays for Wilcoxon
        bi_arr = np.array(bi_vecs)
        nat_arr = np.array(nat_vecs)

        # Aggregate drift per observation (average across dims)
        bi_obs_mean = np.mean(bi_arr, axis=1)
        nat_obs_mean = np.mean(nat_arr, axis=1)

        # Use per-dimension paired differences pooled
        all_bi_flat = bi_arr.flatten()
        all_nat_flat = nat_arr.flatten()

        # Wilcoxon on mean profile difference (per-dimension)
        diffs = nat_mean - bi_mean
        # Use Mann-Whitney on the dimension-wise distributions
        try:
            stat, p_val = stats.mannwhitneyu(
                nat_arr.flatten(), bi_arr.flatten(), alternative="two-sided"
            )
        except Exception:
            p_val = 1.0

        sig = p_val < bonferroni_alpha_h2
        if sig:
            h2_sig_count += 1

        h2_results[lang] = {
            "mean_abs_drift_pct": mean_drift,
            "p_value": p_val,
            "significant": sig,
            "n_bilingual": len(bi_recs),
            "n_native": len(nat_recs),
        }

        drift_str = ", ".join(
            f"{DIMENSIONS[i][:4]}={abs_drift[i]:+.1f}"
            for i in range(8)
        )
        print(f"  {lang}: mean_abs_drift={mean_drift:.2f}pp, "
              f"p={p_val:.3f} {'*' if sig else ''}")
        print(f"    dims: [{drift_str}]")

    print(f"\n  H2: {h2_sig_count}/7 languages significant "
          f"(threshold: 4/7)")
    print(f"  H2 {'SUPPORTED' if h2_sig_count >= 4 else 'NOT SUPPORTED'}")

    # -----------------------------------------------------------------------
    # 4. H3: Dimension-specific cultural drift
    # -----------------------------------------------------------------------
    print("\n--- H3: Dimension-Specific Cultural Drift ---")

    h3_tests = [
        ("H3a", "ar", "Ideological", "increases"),
        ("H3b", "ja", "Cultural", "increases"),
        ("H3c", "hi", "Economic", "increases"),
    ]
    bonferroni_alpha_h3 = .05 / 3
    h3_confirmed = 0

    for label, lang, dim, direction in h3_tests:
        dim_idx = DIMENSIONS.index(dim)
        bi_recs = by_lang_cond.get((lang, "bilingual"), [])
        nat_recs = by_lang_cond.get((lang, "native_only"), [])

        if not bi_recs or not nat_recs:
            print(f"  {label}: SKIP (missing data for {lang})")
            continue

        bi_weights = np.array([
            normalize_weights(r["parsed_weights"])[dim_idx] * 100
            for r in bi_recs
        ])
        nat_weights = np.array([
            normalize_weights(r["parsed_weights"])[dim_idx] * 100
            for r in nat_recs
        ])

        # Independent t-test (not strictly paired since different reps)
        t_stat, p_val = stats.ttest_ind(nat_weights, bi_weights)
        d = cohens_d(nat_weights, bi_weights)

        # Check direction
        mean_diff = np.mean(nat_weights) - np.mean(bi_weights)
        correct_direction = mean_diff > 0 if direction == "increases" else mean_diff < 0
        sig = p_val < bonferroni_alpha_h3 and correct_direction and abs(d) > .30

        if sig:
            h3_confirmed += 1

        # Bootstrap CI on effect size
        combined = np.concatenate([nat_weights, bi_weights])
        ci_lo, ci_hi = bootstrap_ci(
            nat_weights - np.mean(bi_weights),
            stat_func=np.mean,
        )

        print(f"  {label} ({lang} {dim}): "
              f"bilingual={np.mean(bi_weights):.1f}, "
              f"native={np.mean(nat_weights):.1f}, "
              f"diff={mean_diff:+.2f}pp")
        print(f"    t={t_stat:.3f}, p={p_val:.3f}, d={d:.3f}, "
              f"95% CI=[{ci_lo:.2f}, {ci_hi:.2f}] "
              f"{'CONFIRMED' if sig else ''}")

    print(f"\n  H3: {h3_confirmed}/3 predictions confirmed "
          f"(threshold: 1/3)")
    print(f"  H3 {'SUPPORTED' if h3_confirmed >= 1 else 'NOT SUPPORTED'}")

    # -----------------------------------------------------------------------
    # 5. H4: Collectivist vs individualist Social weights
    # -----------------------------------------------------------------------
    print("\n--- H4: Collectivist vs Individualist Social Weights ---")

    social_idx = DIMENSIONS.index("Social")

    # Collectivist: native-only condition for zh, ja, ko
    collectivist_social = []
    for lang in COLLECTIVIST:
        recs = by_lang_cond.get((lang, "native_only"), [])
        for r in recs:
            w = normalize_weights(r["parsed_weights"])[social_idx] * 100
            collectivist_social.append(w)

    # Individualist: en bilingual + es native-only
    individualist_social = []
    for r in by_lang_cond.get(("en", "bilingual"), []):
        w = normalize_weights(r["parsed_weights"])[social_idx] * 100
        individualist_social.append(w)
    for r in by_lang_cond.get(("es", "native_only"), []):
        w = normalize_weights(r["parsed_weights"])[social_idx] * 100
        individualist_social.append(w)

    if collectivist_social and individualist_social:
        col_arr = np.array(collectivist_social)
        ind_arr = np.array(individualist_social)

        h4_t, h4_p = stats.ttest_ind(col_arr, ind_arr)
        h4_d = cohens_d(col_arr, ind_arr)

        print(f"  Collectivist (n={len(col_arr)}): "
              f"mean={np.mean(col_arr):.2f}, sd={np.std(col_arr, ddof=1):.2f}")
        print(f"  Individualist (n={len(ind_arr)}): "
              f"mean={np.mean(ind_arr):.2f}, sd={np.std(ind_arr, ddof=1):.2f}")
        print(f"  t={h4_t:.3f}, df={len(col_arr)+len(ind_arr)-2}, "
              f"p={h4_p:.3f}, d={h4_d:.3f}")

        h4_pass = h4_p < .05 and np.mean(col_arr) > np.mean(ind_arr)
        print(f"  H4 {'SUPPORTED' if h4_pass else 'NOT SUPPORTED'}")
    else:
        print("  H4: SKIP (insufficient data)")

    # -----------------------------------------------------------------------
    # 6. EXPLORATORY: Per-dimension ANOVA (Language as factor)
    # -----------------------------------------------------------------------
    print("\n--- EXPLORATORY: Per-Dimension ANOVA (Language Effect) ---")
    print("  (Bonferroni alpha = .00625 for 8 tests)")

    for dim_idx, dim in enumerate(DIMENSIONS):
        groups = []
        for lang in LANGUAGES:
            recs = by_lang_cond.get((lang, "bilingual"), [])
            weights = [
                normalize_weights(r["parsed_weights"])[dim_idx] * 100
                for r in recs
            ]
            if weights:
                groups.append(weights)

        if len(groups) >= 2:
            f_stat, p_val = stats.f_oneway(*groups)
            # Eta-squared
            all_vals = np.concatenate(groups)
            grand_mean = np.mean(all_vals)
            ss_between = sum(
                len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups
            )
            ss_total = np.sum((all_vals - grand_mean) ** 2)
            eta_sq = ss_between / ss_total if ss_total > 0 else 0

            sig = "*" if p_val < .00625 else ""
            print(f"  {dim}: F={f_stat:.3f}, p={p_val:.3f}, "
                  f"eta_sq={eta_sq:.3f} {sig}")

    # -----------------------------------------------------------------------
    # 7. EXPLORATORY: Drift direction heatmap data
    # -----------------------------------------------------------------------
    print("\n--- EXPLORATORY: Drift Direction (native_only - bilingual) ---")
    print(f"  {'Lang':<6}", end="")
    for d in DIMENSIONS:
        print(f"{d[:5]:>7}", end="")
    print()

    for lang in non_english:
        bi_key = (lang, "bilingual")
        nat_key = (lang, "native_only")
        if bi_key in profiles and nat_key in profiles:
            drift = (profiles[nat_key] - profiles[bi_key]) * 100
            print(f"  {lang:<6}", end="")
            for v in drift:
                print(f"{v:+7.2f}", end="")
            print()

    # -----------------------------------------------------------------------
    # Save results
    # -----------------------------------------------------------------------
    # Build H4 result dict
    h4_result = {}
    if collectivist_social and individualist_social:
        h4_result = {
            "collectivist_mean": float(np.mean(col_arr)),
            "individualist_mean": float(np.mean(ind_arr)),
            "p_value": float(h4_p),
            "cohens_d": float(h4_d),
            "supported": bool(h4_pass),
        }
    else:
        h4_result = {
            "collectivist_mean": None,
            "individualist_mean": None,
            "p_value": None,
            "cohens_d": None,
            "supported": None,
        }

    results = {
        "experiment": "exp_b_cross_language_drift",
        "total_valid_records": len(records),
        "h1": {
            "overall_median_cosine": float(overall_med) if all_cosines else None,
            "overall_min_cosine": float(overall_min) if all_cosines else None,
            "supported": bool(overall_med > .90) if all_cosines else None,
        },
        "h2": {
            "significant_languages": int(h2_sig_count),
            "threshold": 4,
            "supported": bool(h2_sig_count >= 4),
            "per_language": {
                lang: {
                    "mean_abs_drift_pct": float(r["mean_abs_drift_pct"]),
                    "p_value": float(r["p_value"]),
                    "significant": bool(r["significant"]),
                }
                for lang, r in h2_results.items()
            },
        },
        "h3": {
            "confirmed_predictions": int(h3_confirmed),
            "threshold": 1,
            "supported": bool(h3_confirmed >= 1),
        },
        "h4": h4_result,
        "profiles": {
            f"{lang}_{cond}": [float(v) for v in profile]
            for (lang, cond), profile in profiles.items()
        },
    }

    results_path = output_dir / "exp_cross_language_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {results_path}")

    # Write summary markdown
    write_summary(results, output_dir)

    return results


def write_summary(results: dict, output_dir: Path):
    """Write human-readable summary markdown."""
    summary_path = output_dir / "exp_cross_language_summary.md"

    h1 = results["h1"]
    h2 = results["h2"]
    h3 = results["h3"]
    h4 = results["h4"]

    lines = [
        "# Experiment B Results: Cross-Language Semantic Drift",
        "",
        f"**Total valid records**: {results['total_valid_records']}",
        "",
        "## H1: Configural Invariance Under Bilingual Anchoring",
        "",
        f"- Overall median cosine: {h1['overall_median_cosine']:.3f}"
        if h1["overall_median_cosine"] else "- No data",
        f"- Overall min cosine: {h1['overall_min_cosine']:.3f}"
        if h1["overall_min_cosine"] else "",
        f"- **{'SUPPORTED' if h1.get('supported') else 'NOT SUPPORTED'}**"
        f" (threshold: median > .90)",
        "",
        "## H2: Native-Only Drift Magnitude",
        "",
        f"- Significant languages: {h2['significant_languages']}/7 "
        f"(threshold: 4/7)",
        f"- **{'SUPPORTED' if h2['supported'] else 'NOT SUPPORTED'}**",
        "",
        "| Language | Mean Abs Drift (pp) | p-value | Significant |",
        "|----------|-------------------|---------|-------------|",
    ]

    for lang, r in h2.get("per_language", {}).items():
        sig_str = "Yes" if r["significant"] else "No"
        lines.append(
            f"| {lang} | {r['mean_abs_drift_pct']:.2f} | "
            f"{r['p_value']:.3f} | {sig_str} |"
        )

    lines += [
        "",
        "## H3: Dimension-Specific Cultural Drift",
        "",
        f"- Confirmed predictions: {h3['confirmed_predictions']}/3 "
        f"(threshold: 1/3)",
        f"- **{'SUPPORTED' if h3['supported'] else 'NOT SUPPORTED'}**",
        "",
        "## H4: Collectivist Social Amplification",
        "",
    ]

    if h4.get("collectivist_mean") is not None:
        lines += [
            f"- Collectivist mean Social: {h4['collectivist_mean']:.2f}",
            f"- Individualist mean Social: {h4['individualist_mean']:.2f}",
            f"- p = {h4['p_value']:.3f}, d = {h4['cohens_d']:.3f}",
            f"- **{'SUPPORTED' if h4.get('supported') else 'NOT SUPPORTED'}**",
        ]
    else:
        lines.append("- Insufficient data")

    lines += [
        "",
        "---",
        "*Generated by exp_cross_language_analysis.py*",
    ]

    with open(summary_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Summary saved to {summary_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    script_dir = Path(__file__).parent
    jsonl_path = script_dir.parent / "L3_sessions" / "exp_cross_language.jsonl"
    output_dir = script_dir

    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found. Run exp_cross_language.py first.")
        sys.exit(1)

    analyze(jsonl_path, output_dir)


if __name__ == "__main__":
    main()
