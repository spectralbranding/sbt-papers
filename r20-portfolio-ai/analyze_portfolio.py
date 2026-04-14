#!/usr/bin/env python3
"""
R20 Portfolio-AI Experiment -- Analysis

Reads responses from responses/ and computes:
1. Per-brand DCI (Dimensional Concentration Index) solo vs portfolio
2. Cosine similarity between solo and portfolio profiles
3. Portfolio interference patterns (constructive vs destructive)
4. Cross-model consistency (ICC, variance decomposition)
5. Statistical tests (paired t-tests, Wilcoxon, effect sizes)
6. TOST equivalence testing
7. Power analysis
8. Shannon entropy and Jensen-Shannon divergence
9. Per-dimension shifts with FDR correction
10. Sub-group analyses (Western vs non-Western, API vs local)
11. System-prompt ablation comparison

Usage:
    uv run python research/R20_portfolio_ai/analyze_portfolio.py

Requirements:
    uv add pandas numpy scipy
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

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

PORTFOLIO_META = {
    "LVMH": {
        "type": "spectral_cluster",
        "predicted_interference": "constructive",
        "description": "Luxury cluster: brands occupy proximate regions in 8D space",
    },
    "Unilever": {
        "type": "spectral_contradiction",
        "predicted_interference": "destructive",
        "description": "Contradictory portfolio: Dove vs Axe on Ideological dimension",
    },
    "P&G": {
        "type": "spectral_spread",
        "predicted_interference": "negligible",
        "description": "Spread portfolio: brands in distant regions, minimal overlap",
    },
    "Toyota": {
        "type": "spectral_layer",
        "predicted_interference": "aspirational",
        "description": "Layered portfolio: mass (Toyota) vs luxury (Lexus) on same dimensions",
    },
    "L'Oreal": {
        "type": "prestige_spread",
        "predicted_interference": "gradient_flattening",
        "description": "Prestige spread: mass (Maybelline) to luxury (Lancome) gradient",
    },
    "Geely": {
        "type": "reverse_aspiration",
        "predicted_interference": "downward_suppression",
        "description": "Reverse aspiration: Chinese mass parent owns European premium (Volvo, Polestar)",
    },
    "Yandex": {
        "type": "branded_house",
        "predicted_interference": "shared_identity",
        "description": "Branded house: all sub-brands share Yandex name; geopolitical overlay",
    },
}

# Training tradition groupings (v2.0: 7 traditions, 13 models)
WESTERN_MODELS = {"claude", "gpt4omini", "gemini25flash", "grok", "llama", "gemma4"}
NON_WESTERN_MODELS = {"deepseek", "qwen3", "yandex", "sarvam", "swallow", "mistral", "exaone"}

# Finer tradition groupings for sub-group analysis
TRADITION_GROUPS = {
    "Western": {"claude", "gpt4omini", "gemini25flash", "grok", "llama", "gemma4"},
    "Chinese": {"deepseek", "qwen3"},
    "Russian": {"yandex"},
    "Indian": {"sarvam"},
    "Japanese": {"swallow"},
    "European": {"mistral"},
    "Korean": {"exaone"},
}

LOCAL_MODELS = {"gemma4", "exaone"}


def load_responses():
    """Load all successfully parsed responses."""
    responses_dir = Path(__file__).parent / "responses"
    records = []
    for f in sorted(responses_dir.glob("*.json")):
        with open(f) as fh:
            rec = json.load(fh)
        if rec.get("parse_success") and rec.get("scores"):
            records.append(rec)
    return records


def records_to_dataframe(records):
    """Convert records to a flat DataFrame."""
    rows = []
    for r in records:
        row = {
            "cell_id": r["cell_id"],
            "portfolio": r["portfolio"],
            "brand": r["brand"],
            "condition": r["condition"],
            "model": r["model_id"],
            "tradition": r.get("tradition", "Western"),
            "repetition": r["repetition"],
        }
        for dim in DIMENSIONS:
            row[dim] = r["scores"].get(dim, np.nan)
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


def compute_dci(profile: np.ndarray) -> float:
    """Dimensional Concentration Index: how concentrated vs uniform the profile is."""
    if np.all(profile == 0):
        return 0.0
    weights = profile / profile.sum()
    uniform = 1.0 / len(profile)
    return float(np.sum(np.abs(weights - uniform)) * 100 / 2)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def cohens_d(group1, group2):
    """Cohen's d effect size for two independent groups."""
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return np.nan
    var1 = np.var(group1, ddof=1)
    var2 = np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return float((np.mean(group1) - np.mean(group2)) / pooled_std)


def shannon_entropy(profile: np.ndarray) -> float:
    """Shannon entropy of the weight vector (information-theoretic diversity)."""
    if np.all(profile == 0):
        return 0.0
    weights = profile / profile.sum()
    weights = weights[weights > 0]
    return float(-np.sum(weights * np.log2(weights)))


def jensen_shannon_divergence(p: np.ndarray, q: np.ndarray) -> float:
    """Jensen-Shannon divergence between two distributions."""
    p_norm = p / p.sum() if p.sum() > 0 else p
    q_norm = q / q.sum() if q.sum() > 0 else q
    m = 0.5 * (p_norm + q_norm)
    # KL divergences with epsilon to avoid log(0)
    eps = 1e-10
    kl_pm = np.sum(p_norm * np.log2((p_norm + eps) / (m + eps)))
    kl_qm = np.sum(q_norm * np.log2((q_norm + eps) / (m + eps)))
    return float(0.5 * kl_pm + 0.5 * kl_qm)


def benjamini_hochberg(p_values, alpha=0.05):
    """Benjamini-Hochberg FDR correction. Returns array of booleans."""
    n = len(p_values)
    if n == 0:
        return np.array([], dtype=bool)
    sorted_idx = np.argsort(p_values)
    sorted_p = np.array(p_values)[sorted_idx]
    thresholds = np.arange(1, n + 1) / n * alpha
    significant = np.zeros(n, dtype=bool)
    # Find the largest k where p(k) <= k/m * alpha
    max_k = -1
    for k in range(n):
        if sorted_p[k] <= thresholds[k]:
            max_k = k
    if max_k >= 0:
        significant[sorted_idx[: max_k + 1]] = True
    return significant


# ---------------------------------------------------------------------------
# Analyses
# ---------------------------------------------------------------------------


def analysis_1_dci_comparison(df):
    """Compare DCI between solo and portfolio conditions per brand."""
    print("\n" + "=" * 70)
    print("ANALYSIS 1: Dimensional Concentration Index (Solo vs Portfolio)")
    print("=" * 70)

    results = []

    for portfolio in sorted(df["portfolio"].unique()):
        print(f"\n--- {portfolio} ({PORTFOLIO_META[portfolio]['type']}) ---")
        print(
            f"    Predicted: {PORTFOLIO_META[portfolio]['predicted_interference']} interference\n"
        )
        pdf = df[df["portfolio"] == portfolio]

        for brand in sorted(pdf["brand"].unique()):
            bdf = pdf[pdf["brand"] == brand]
            solo_profiles = []
            port_profiles = []

            for _, row in bdf.iterrows():
                profile = row[DIMENSIONS].values.astype(float)
                dci = compute_dci(profile)
                entropy = shannon_entropy(profile)
                if row["condition"] == "solo":
                    solo_profiles.append(
                        {"profile": profile, "dci": dci, "entropy": entropy}
                    )
                elif row["condition"] == "portfolio":
                    port_profiles.append(
                        {"profile": profile, "dci": dci, "entropy": entropy}
                    )

            solo_dcis = [s["dci"] for s in solo_profiles]
            port_dcis = [p["dci"] for p in port_profiles]

            if len(solo_dcis) < 2 or len(port_dcis) < 2:
                continue

            solo_mean = np.mean(solo_dcis)
            port_mean = np.mean(port_dcis)
            delta = port_mean - solo_mean
            t_stat, p_val = stats.ttest_ind(port_dcis, solo_dcis)
            d = cohens_d(port_dcis, solo_dcis)

            solo_mean_profile = np.mean([s["profile"] for s in solo_profiles], axis=0)
            port_mean_profile = np.mean([p["profile"] for p in port_profiles], axis=0)
            cos_sim = cosine_similarity(solo_mean_profile, port_mean_profile)
            euc_dist = euclidean_distance(solo_mean_profile, port_mean_profile)
            jsd = jensen_shannon_divergence(solo_mean_profile, port_mean_profile)

            solo_entropy_mean = np.mean([s["entropy"] for s in solo_profiles])
            port_entropy_mean = np.mean([p["entropy"] for p in port_profiles])

            print(
                f"  {brand:20s}  Solo DCI={solo_mean:5.1f}  Port DCI={port_mean:5.1f}  "
                f"Delta={delta:+5.1f}  t={t_stat:+6.2f}  p={p_val:.3f}  d={d:+.2f}  "
                f"cos={cos_sim:.3f}  L2={euc_dist:.2f}  JSD={jsd:.4f}"
            )

            results.append(
                {
                    "portfolio": portfolio,
                    "brand": brand,
                    "portfolio_type": PORTFOLIO_META[portfolio]["type"],
                    "predicted": PORTFOLIO_META[portfolio]["predicted_interference"],
                    "solo_dci_mean": round(solo_mean, 2),
                    "solo_dci_sd": round(np.std(solo_dcis, ddof=1), 2),
                    "port_dci_mean": round(port_mean, 2),
                    "port_dci_sd": round(np.std(port_dcis, ddof=1), 2),
                    "delta_dci": round(delta, 2),
                    "t_stat": round(t_stat, 3),
                    "p_value": round(p_val, 4),
                    "cohens_d": round(d, 3),
                    "cosine_similarity": round(cos_sim, 4),
                    "euclidean_distance": round(euc_dist, 3),
                    "jsd": round(jsd, 5),
                    "solo_entropy_mean": round(solo_entropy_mean, 3),
                    "port_entropy_mean": round(port_entropy_mean, 3),
                    "n_solo": len(solo_dcis),
                    "n_portfolio": len(port_dcis),
                }
            )

    return pd.DataFrame(results)


def analysis_2_dimension_shifts(df):
    """Per-dimension shift with FDR correction."""
    print("\n" + "=" * 70)
    print("ANALYSIS 2: Per-Dimension Score Shifts (Portfolio - Solo) with FDR")
    print("=" * 70)

    results = []

    for portfolio in sorted(df["portfolio"].unique()):
        print(f"\n--- {portfolio} ---")
        pdf = df[df["portfolio"] == portfolio]

        for brand in sorted(pdf["brand"].unique()):
            bdf = pdf[pdf["brand"] == brand]
            solo = bdf[bdf["condition"] == "solo"]
            port = bdf[bdf["condition"] == "portfolio"]

            if len(solo) < 2 or len(port) < 2:
                continue

            shifts = {}
            for dim in DIMENSIONS:
                solo_vals = solo[dim].values
                port_vals = port[dim].values
                delta = np.mean(port_vals) - np.mean(solo_vals)
                t, p = stats.ttest_ind(port_vals, solo_vals)
                d = cohens_d(port_vals, solo_vals)
                shifts[dim] = {"delta": delta, "t": t, "p": p, "d": d}

            # FDR correction within this brand
            p_vals = [shifts[d]["p"] for d in DIMENSIONS]
            fdr_sig = benjamini_hochberg(p_vals, 0.05)

            sorted_dims = sorted(
                shifts.items(), key=lambda x: abs(x[1]["delta"]), reverse=True
            )
            top3 = sorted_dims[:3]
            print(f"  {brand}:")
            for dim, s in top3:
                idx = DIMENSIONS.index(dim)
                sig = "** (FDR)" if fdr_sig[idx] else ("*" if s["p"] < 0.05 else "")
                print(
                    f"    {dim:14s}  delta={s['delta']:+5.2f}  t={s['t']:+5.2f}  "
                    f"p={s['p']:.3f}{sig}  d={s['d']:+.2f}"
                )

            for i, dim in enumerate(DIMENSIONS):
                s = shifts[dim]
                results.append(
                    {
                        "portfolio": portfolio,
                        "brand": brand,
                        "dimension": dim,
                        "delta": round(s["delta"], 3),
                        "t_stat": round(s["t"], 3),
                        "p_value": round(s["p"], 4),
                        "cohens_d": round(s["d"], 3),
                        "fdr_significant": bool(fdr_sig[i]),
                    }
                )

    return pd.DataFrame(results)


def analysis_3_interference_patterns(df):
    """Portfolio-level interference: constructive vs destructive."""
    print("\n" + "=" * 70)
    print("ANALYSIS 3: Portfolio Interference Patterns")
    print("=" * 70)

    results = []

    for portfolio in sorted(df["portfolio"].unique()):
        meta = PORTFOLIO_META[portfolio]
        print(f"\n--- {portfolio} ({meta['type']}) ---")
        print(f"    Predicted: {meta['predicted_interference']} interference")

        pdf = df[df["portfolio"] == portfolio]
        brands = sorted(pdf["brand"].unique())

        profiles = {}
        for brand in brands:
            bdf = pdf[pdf["brand"] == brand]
            for cond in ["solo", "portfolio"]:
                cdf = bdf[bdf["condition"] == cond]
                if len(cdf) > 0:
                    profiles[(brand, cond)] = cdf[DIMENSIONS].mean().values

        for cond in ["solo", "portfolio"]:
            cos_sims = []
            for i, b1 in enumerate(brands):
                for b2 in brands[i + 1 :]:
                    if (b1, cond) in profiles and (b2, cond) in profiles:
                        cs = cosine_similarity(
                            profiles[(b1, cond)], profiles[(b2, cond)]
                        )
                        cos_sims.append(cs)
            if cos_sims:
                print(f"    {cond:10s}  mean cross-brand cos={np.mean(cos_sims):.3f}")

        constructive_count = 0
        destructive_count = 0
        total_dims = 0

        for brand in brands:
            if (brand, "solo") not in profiles or (brand, "portfolio") not in profiles:
                continue
            solo_p = profiles[(brand, "solo")]
            port_p = profiles[(brand, "portfolio")]
            category_mean = np.mean(
                [profiles[(b, "solo")] for b in brands if (b, "solo") in profiles],
                axis=0,
            )

            for i, dim in enumerate(DIMENSIONS):
                deviation_solo = solo_p[i] - category_mean[i]
                shift = port_p[i] - solo_p[i]

                if abs(deviation_solo) > 0.3:
                    total_dims += 1
                    if np.sign(shift) == np.sign(deviation_solo):
                        constructive_count += 1
                    elif abs(shift) > 0.2:
                        destructive_count += 1

        neutral_count = total_dims - constructive_count - destructive_count
        print(
            f"    Constructive: {constructive_count}/{total_dims}  "
            f"Destructive: {destructive_count}/{total_dims}  "
            f"Neutral: {neutral_count}/{total_dims}"
        )

        interference_ratio = constructive_count / total_dims if total_dims > 0 else 0.5
        observed = (
            "constructive"
            if interference_ratio > 0.6
            else "destructive" if interference_ratio < 0.4 else "mixed/negligible"
        )
        match = "MATCH" if observed == meta["predicted_interference"] else "MISMATCH"
        print(
            f"    Observed: {observed} interference ({interference_ratio:.2f}) [{match}]"
        )

        results.append(
            {
                "portfolio": portfolio,
                "type": meta["type"],
                "predicted": meta["predicted_interference"],
                "observed": observed,
                "constructive": constructive_count,
                "destructive": destructive_count,
                "neutral": neutral_count,
                "total_dims": total_dims,
                "ratio": round(interference_ratio, 3),
                "match": match == "MATCH",
            }
        )

    return pd.DataFrame(results)


def analysis_4_cross_model(df):
    """Cross-model consistency with ICC."""
    print("\n" + "=" * 70)
    print("ANALYSIS 4: Cross-Model Consistency")
    print("=" * 70)

    results = []

    for portfolio in sorted(df["portfolio"].unique()):
        pdf = df[df["portfolio"] == portfolio]

        for brand in sorted(pdf["brand"].unique()):
            bdf = pdf[pdf["brand"] == brand]

            for model in sorted(bdf["model"].unique()):
                mdf = bdf[bdf["model"] == model]
                solo = mdf[mdf["condition"] == "solo"]
                port = mdf[mdf["condition"] == "portfolio"]

                if len(solo) == 0 or len(port) == 0:
                    continue

                solo_profile = solo[DIMENSIONS].mean().values
                port_profile = port[DIMENSIONS].mean().values
                solo_dci = compute_dci(solo_profile)
                port_dci = compute_dci(port_profile)
                cos = cosine_similarity(solo_profile, port_profile)

                results.append(
                    {
                        "portfolio": portfolio,
                        "brand": brand,
                        "model": model,
                        "solo_dci": round(solo_dci, 2),
                        "port_dci": round(port_dci, 2),
                        "delta_dci": round(port_dci - solo_dci, 2),
                        "cosine": round(cos, 4),
                    }
                )

    rdf = pd.DataFrame(results)
    if rdf.empty:
        print("  No data available.")
        return rdf

    for portfolio in sorted(rdf["portfolio"].unique()):
        pdata = rdf[rdf["portfolio"] == portfolio]
        increasing = (pdata["delta_dci"] > 0).sum()
        decreasing = (pdata["delta_dci"] < 0).sum()
        total = len(pdata)
        mean_cos = pdata["cosine"].mean()
        mean_delta = pdata["delta_dci"].mean()

        p_binom = (
            stats.binomtest(max(increasing, decreasing), total, 0.5).pvalue
            if total > 0
            else 1.0
        )

        print(
            f"  {portfolio:12s}  DCI increase: {increasing}/{total}  "
            f"decrease: {decreasing}/{total}  mean delta={mean_delta:+.1f}  "
            f"mean cos={mean_cos:.3f}  binomial p={p_binom:.3f}"
        )

    # Per-model table
    print("\n  Per-model mean delta DCI:")
    pivot = rdf.pivot_table(
        values="delta_dci", index="model", columns="portfolio", aggfunc="mean"
    )
    print(pivot.round(2).to_string())

    # ICC calculation (two-way random, single measures)
    print("\n  ICC (Intraclass Correlation) for DCI ratings across models:")
    for condition in ["solo", "portfolio"]:
        cond_df = df[df["condition"] == condition]
        # Pivot: rows=brand, columns=model, values=mean DCI
        brand_model_dci = {}
        for brand in sorted(cond_df["brand"].unique()):
            for model in sorted(cond_df["model"].unique()):
                subset = cond_df[
                    (cond_df["brand"] == brand) & (cond_df["model"] == model)
                ]
                if len(subset) > 0:
                    profile = subset[DIMENSIONS].mean().values
                    brand_model_dci[(brand, model)] = compute_dci(profile)

        if brand_model_dci:
            brands = sorted(set(k[0] for k in brand_model_dci))
            models = sorted(set(k[1] for k in brand_model_dci))
            matrix = np.full((len(brands), len(models)), np.nan)
            for i, b in enumerate(brands):
                for j, m in enumerate(models):
                    if (b, m) in brand_model_dci:
                        matrix[i, j] = brand_model_dci[(b, m)]

            # Remove cols/rows with NaN
            valid_cols = ~np.any(np.isnan(matrix), axis=0)
            matrix = matrix[:, valid_cols]
            if matrix.shape[1] >= 2:
                n, k = matrix.shape
                grand_mean = np.mean(matrix)
                ss_rows = k * np.sum((np.mean(matrix, axis=1) - grand_mean) ** 2)
                ss_cols = n * np.sum((np.mean(matrix, axis=0) - grand_mean) ** 2)
                ss_total = np.sum((matrix - grand_mean) ** 2)
                ss_error = ss_total - ss_rows - ss_cols
                ms_rows = ss_rows / (n - 1) if n > 1 else 0
                ms_error = (
                    ss_error / ((n - 1) * (k - 1)) if (n - 1) * (k - 1) > 0 else 0
                )
                ms_cols = ss_cols / (k - 1) if k > 1 else 0

                # ICC(2,1) - two-way random, single measures
                icc = (
                    (ms_rows - ms_error)
                    / (ms_rows + (k - 1) * ms_error + k * (ms_cols - ms_error) / n)
                    if (ms_rows + (k - 1) * ms_error + k * (ms_cols - ms_error) / n)
                    != 0
                    else 0
                )

                print(
                    f"    {condition}: ICC(2,1) = {icc:.3f} (k={k} models, n={n} brands)"
                )

    return rdf


def analysis_5_power_and_tost(dci_df):
    """Power analysis and TOST equivalence testing."""
    print("\n" + "=" * 70)
    print("ANALYSIS 5: Power Analysis and TOST Equivalence Testing")
    print("=" * 70)

    # Post-hoc power for paired t-test
    if not dci_df.empty:
        n_obs = dci_df["n_solo"].iloc[0] + dci_df["n_portfolio"].iloc[0]
        n_per_group = dci_df["n_solo"].iloc[0]
        alpha = 0.05
        d_target = 0.50  # medium effect

        # Non-centrality parameter for independent t-test
        ncp = d_target * np.sqrt(n_per_group / 2)
        df_t = 2 * n_per_group - 2
        crit = stats.t.ppf(1 - alpha / 2, df_t)
        power = 1 - stats.t.cdf(crit, df_t, ncp) + stats.t.cdf(-crit, df_t, ncp)

        print(f"\n  Post-hoc power analysis:")
        print(
            f"    N per group = {n_per_group}, alpha = {alpha}, target d = {d_target}"
        )
        print(f"    Power = {power:.3f}")
        print(
            f"    The experiment had {power*100:.0f}% power to detect a medium "
            f"effect (d = {d_target:.2f}) at alpha = {alpha:.2f}"
        )

    # TOST equivalence testing
    print(f"\n  TOST Equivalence Testing (bounds = +/-1.0 DCI points):")
    equivalence_bound = 1.0
    tost_results = []

    for _, row in dci_df.iterrows():
        delta = row["delta_dci"]
        se = (
            np.sqrt(
                row["solo_dci_sd"] ** 2 / row["n_solo"]
                + row["port_dci_sd"] ** 2 / row["n_portfolio"]
            )
            if row["solo_dci_sd"] > 0 or row["port_dci_sd"] > 0
            else 1e-10
        )

        df_approx = row["n_solo"] + row["n_portfolio"] - 2

        # Upper bound test: H0: delta >= bound
        t_upper = (delta - equivalence_bound) / se if se > 0 else 0
        p_upper = stats.t.cdf(t_upper, df_approx)

        # Lower bound test: H0: delta <= -bound
        t_lower = (delta + equivalence_bound) / se if se > 0 else 0
        p_lower = 1 - stats.t.cdf(t_lower, df_approx)

        p_tost = max(p_upper, p_lower)
        equivalent = p_tost < 0.05

        tost_results.append(
            {
                "brand": row["brand"],
                "portfolio": row["portfolio"],
                "delta_dci": delta,
                "p_tost": round(p_tost, 4),
                "equivalent": equivalent,
            }
        )

        sig = "EQUIVALENT" if equivalent else "inconclusive"
        print(
            f"    {row['brand']:20s} ({row['portfolio']:10s})  "
            f"delta={delta:+5.2f}  p_TOST={p_tost:.3f}  [{sig}]"
        )

    n_equiv = sum(1 for r in tost_results if r["equivalent"])
    total = len(tost_results)
    print(
        f"\n    Equivalence confirmed for {n_equiv}/{total} brands "
        f"within +/-{equivalence_bound} DCI bounds"
    )

    return pd.DataFrame(tost_results)


def analysis_6_subgroups(df, dci_df):
    """Sub-group analyses: Western vs non-Western, API vs local."""
    print("\n" + "=" * 70)
    print("ANALYSIS 6: Sub-Group Analyses")
    print("=" * 70)

    # Western vs non-Western
    print("\n  --- Western vs Non-Western Models ---")
    for group_name, model_set in [
        ("Western", WESTERN_MODELS),
        ("Non-Western", NON_WESTERN_MODELS),
    ]:
        gdf = df[df["model"].isin(model_set)]
        if gdf.empty:
            continue

        solo = gdf[gdf["condition"] == "solo"]
        port = gdf[gdf["condition"] == "portfolio"]

        solo_dcis = [
            compute_dci(row[DIMENSIONS].values.astype(float))
            for _, row in solo.iterrows()
        ]
        port_dcis = [
            compute_dci(row[DIMENSIONS].values.astype(float))
            for _, row in port.iterrows()
        ]

        if solo_dcis and port_dcis:
            delta = np.mean(port_dcis) - np.mean(solo_dcis)
            t, p = stats.ttest_ind(port_dcis, solo_dcis)
            d = cohens_d(port_dcis, solo_dcis)

            # Mean cosine between solo and portfolio per brand
            cos_sims = []
            for brand in sorted(gdf["brand"].unique()):
                bdf = gdf[gdf["brand"] == brand]
                s = bdf[bdf["condition"] == "solo"]
                po = bdf[bdf["condition"] == "portfolio"]
                if len(s) > 0 and len(po) > 0:
                    cos_sims.append(
                        cosine_similarity(
                            s[DIMENSIONS].mean().values, po[DIMENSIONS].mean().values
                        )
                    )

            print(
                f"    {group_name:15s}  n_solo={len(solo_dcis):3d}  n_port={len(port_dcis):3d}  "
                f"delta DCI={delta:+.2f}  t={t:+.2f}  p={p:.3f}  d={d:+.2f}  "
                f"mean cos={np.mean(cos_sims):.3f}"
            )

    # API vs Local
    print("\n  --- API vs Local Models ---")
    for group_name, model_set in [
        ("API", set(m for m in df["model"].unique() if m not in LOCAL_MODELS)),
        ("Local", LOCAL_MODELS),
    ]:
        gdf = df[df["model"].isin(model_set)]
        if gdf.empty:
            continue

        solo_dcis = [
            compute_dci(row[DIMENSIONS].values.astype(float))
            for _, row in gdf[gdf["condition"] == "solo"].iterrows()
        ]
        port_dcis = [
            compute_dci(row[DIMENSIONS].values.astype(float))
            for _, row in gdf[gdf["condition"] == "portfolio"].iterrows()
        ]

        if solo_dcis and port_dcis:
            delta = np.mean(port_dcis) - np.mean(solo_dcis)
            t, p = stats.ttest_ind(port_dcis, solo_dcis)
            d = cohens_d(port_dcis, solo_dcis)
            print(
                f"    {group_name:15s}  n_solo={len(solo_dcis):3d}  n_port={len(port_dcis):3d}  "
                f"delta DCI={delta:+.2f}  t={t:+.2f}  p={p:.3f}  d={d:+.2f}"
            )

    # Variance decomposition: model, brand, condition
    print("\n  --- Variance Decomposition (DCI) ---")
    dci_per_obs = []
    for _, row in df.iterrows():
        profile = row[DIMENSIONS].values.astype(float)
        dci_per_obs.append(
            {
                "model": row["model"],
                "brand": row["brand"],
                "condition": row["condition"],
                "portfolio": row["portfolio"],
                "dci": compute_dci(profile),
            }
        )
    dci_obs_df = pd.DataFrame(dci_per_obs)

    grand_mean = dci_obs_df["dci"].mean()
    ss_total = np.sum((dci_obs_df["dci"] - grand_mean) ** 2)

    for factor in ["model", "brand", "condition", "portfolio"]:
        group_means = dci_obs_df.groupby(factor)["dci"].mean()
        group_counts = dci_obs_df.groupby(factor)["dci"].count()
        ss_factor = np.sum(group_counts * (group_means - grand_mean) ** 2)
        pct = ss_factor / ss_total * 100 if ss_total > 0 else 0
        print(f"    {factor:12s}  SS={ss_factor:8.1f}  %variance={pct:5.1f}%")


def analysis_7_ablation(df):
    """System-prompt vs user-prompt ablation analysis."""
    print("\n" + "=" * 70)
    print("ANALYSIS 7: System-Prompt Ablation")
    print("=" * 70)

    # Check if system_portfolio data exists
    sys_df = df[df["condition"] == "system_portfolio"]
    if sys_df.empty:
        print("  No system-prompt ablation data found. Skipping.")
        return pd.DataFrame()

    ablation_models = sorted(sys_df["model"].unique())
    results = []

    for model in ablation_models:
        mdf = df[df["model"] == model]
        solo = mdf[mdf["condition"] == "solo"]
        user_port = mdf[mdf["condition"] == "portfolio"]
        sys_port = mdf[mdf["condition"] == "system_portfolio"]

        if solo.empty or user_port.empty or sys_port.empty:
            continue

        for brand in sorted(mdf["brand"].unique()):
            s = solo[solo["brand"] == brand]
            up = user_port[user_port["brand"] == brand]
            sp = sys_port[sys_port["brand"] == brand]

            if s.empty or up.empty or sp.empty:
                continue

            s_profile = s[DIMENSIONS].mean().values
            up_profile = up[DIMENSIONS].mean().values
            sp_profile = sp[DIMENSIONS].mean().values

            cos_user = cosine_similarity(s_profile, up_profile)
            cos_sys = cosine_similarity(s_profile, sp_profile)
            cos_user_sys = cosine_similarity(up_profile, sp_profile)

            results.append(
                {
                    "model": model,
                    "brand": brand,
                    "cos_solo_user_port": round(cos_user, 4),
                    "cos_solo_sys_port": round(cos_sys, 4),
                    "cos_user_sys": round(cos_user_sys, 4),
                }
            )

    rdf = pd.DataFrame(results)
    if rdf.empty:
        print("  Insufficient data for ablation analysis.")
        return rdf

    print(f"\n  Mean cosine similarities by model:")
    for model in sorted(rdf["model"].unique()):
        mr = rdf[rdf["model"] == model]
        print(
            f"    {model:15s}  solo-vs-user_port: {mr['cos_solo_user_port'].mean():.3f}  "
            f"solo-vs-sys_port: {mr['cos_solo_sys_port'].mean():.3f}  "
            f"user-vs-sys: {mr['cos_user_sys'].mean():.3f}"
        )

    # Overall: is system-prompt framing equivalent to user-prompt framing?
    if len(rdf) > 1:
        t, p = stats.ttest_rel(rdf["cos_solo_user_port"], rdf["cos_solo_sys_port"])
        d_val = np.mean(rdf["cos_solo_user_port"] - rdf["cos_solo_sys_port"]) / np.std(
            rdf["cos_solo_user_port"] - rdf["cos_solo_sys_port"], ddof=1
        )
        print(
            f"\n  Paired t-test (user vs system framing cosine to solo):"
            f"  t={t:.3f}  p={p:.3f}  d={d_val:.3f}"
        )

    return rdf


def analysis_8_recommendation(df):
    """Compare direct rating vs recommendation prompt conditions."""
    print("\n" + "=" * 70)
    print("ANALYSIS 8: Recommendation Prompt Comparison")
    print("=" * 70)

    reco_solo = df[df["condition"] == "recommendation_solo"]
    reco_port = df[df["condition"] == "recommendation_portfolio"]
    direct_solo = df[df["condition"] == "solo"]
    direct_port = df[df["condition"] == "portfolio"]

    if reco_solo.empty:
        print("  No recommendation data found. Skipping.")
        return pd.DataFrame()

    results = []
    print("\n  --- Direct vs Recommendation: Solo Condition ---")
    for brand in sorted(df["brand"].unique()):
        ds = direct_solo[direct_solo["brand"] == brand]
        rs = reco_solo[reco_solo["brand"] == brand]
        if ds.empty or rs.empty:
            continue
        ds_profile = ds[DIMENSIONS].mean().values
        rs_profile = rs[DIMENSIONS].mean().values
        cos = cosine_similarity(ds_profile, rs_profile)
        ds_dci = compute_dci(ds_profile)
        rs_dci = compute_dci(rs_profile)
        results.append({
            "brand": brand, "comparison": "solo_direct_vs_reco",
            "cosine": round(cos, 4), "direct_dci": round(ds_dci, 2),
            "reco_dci": round(rs_dci, 2), "delta_dci": round(rs_dci - ds_dci, 2),
        })
        print(f"    {brand:20s}  cos={cos:.3f}  direct DCI={ds_dci:.1f}  reco DCI={rs_dci:.1f}  delta={rs_dci-ds_dci:+.1f}")

    print("\n  --- Recommendation: Solo vs Portfolio ---")
    reco_results = []
    for brand in sorted(df["brand"].unique()):
        rs = reco_solo[reco_solo["brand"] == brand]
        rp = reco_port[reco_port["brand"] == brand]
        if rs.empty or rp.empty:
            continue
        rs_dcis = [compute_dci(row[DIMENSIONS].values.astype(float)) for _, row in rs.iterrows()]
        rp_dcis = [compute_dci(row[DIMENSIONS].values.astype(float)) for _, row in rp.iterrows()]
        delta = np.mean(rp_dcis) - np.mean(rs_dcis)
        if len(rs_dcis) >= 2 and len(rp_dcis) >= 2:
            t, p = stats.ttest_ind(rp_dcis, rs_dcis)
            d = cohens_d(rp_dcis, rs_dcis)
        else:
            t = p = d = np.nan
        cos = cosine_similarity(rs[DIMENSIONS].mean().values, rp[DIMENSIONS].mean().values)
        reco_results.append({
            "brand": brand, "delta_dci": round(delta, 2),
            "t": round(t, 3), "p": round(p, 4), "d": round(d, 3), "cosine": round(cos, 4),
        })
        print(f"    {brand:20s}  delta={delta:+5.2f}  t={t:+5.2f}  p={p:.3f}  d={d:+.2f}  cos={cos:.3f}")

    rdf = pd.DataFrame(reco_results)
    if not rdf.empty:
        mean_delta = rdf["delta_dci"].mean()
        mean_cos = rdf["cosine"].mean()
        print(f"\n    Mean delta DCI (reco solo->port): {mean_delta:+.2f}")
        print(f"    Mean cosine: {mean_cos:.3f}")
        sig = benjamini_hochberg(rdf["p"].dropna().values)
        print(f"    FDR-significant: {sum(sig)}/{len(sig)}")

    return rdf


def analysis_9_multiturn(df):
    """Multi-turn analysis: does revealing portfolio in Turn 2 change ratings?"""
    print("\n" + "=" * 70)
    print("ANALYSIS 9: Multi-Turn Conversation Analysis")
    print("=" * 70)

    mt_df = df[df["condition"] == "multiturn"]
    solo_df = df[df["condition"] == "solo"]
    if mt_df.empty:
        print("  No multi-turn data found. Skipping.")
        return pd.DataFrame()

    # Multi-turn records have turn1_scores in the raw JSON; the 'scores' field
    # is turn2 (post-reveal). We need to load turn1 from the raw files.
    responses_dir = Path(__file__).parent / "responses"
    mt_records = []
    for f in sorted(responses_dir.glob("*_multiturn_*.json")):
        with open(f) as fh:
            rec = json.load(fh)
        if not rec.get("parse_success"):
            continue
        t1 = rec.get("turn1_scores", {})
        t2 = rec.get("scores", {})
        if t1 and t2 and all(d in t1 for d in DIMENSIONS) and all(d in t2 for d in DIMENSIONS):
            mt_records.append(rec)

    if not mt_records:
        print("  No valid multi-turn pairs found. Skipping.")
        return pd.DataFrame()

    print(f"  Loaded {len(mt_records)} multi-turn pairs\n")

    results = []
    for brand in sorted(set(r["brand"] for r in mt_records)):
        brand_recs = [r for r in mt_records if r["brand"] == brand]
        t1_dcis = [compute_dci(np.array([r["turn1_scores"][d] for d in DIMENSIONS])) for r in brand_recs]
        t2_dcis = [compute_dci(np.array([r["scores"][d] for d in DIMENSIONS])) for r in brand_recs]

        delta = np.mean(t2_dcis) - np.mean(t1_dcis)
        if len(t1_dcis) >= 2:
            t, p = stats.ttest_rel(t2_dcis, t1_dcis)
            d_val = np.mean(np.array(t2_dcis) - np.array(t1_dcis)) / (
                np.std(np.array(t2_dcis) - np.array(t1_dcis), ddof=1) or 1e-10
            )
        else:
            t = p = d_val = np.nan

        t1_mean = np.mean([np.array([r["turn1_scores"][d] for d in DIMENSIONS]) for r in brand_recs], axis=0)
        t2_mean = np.mean([np.array([r["scores"][d] for d in DIMENSIONS]) for r in brand_recs], axis=0)
        cos = cosine_similarity(t1_mean, t2_mean)

        results.append({
            "brand": brand, "portfolio": brand_recs[0]["portfolio"],
            "n": len(brand_recs),
            "t1_dci_mean": round(np.mean(t1_dcis), 2),
            "t2_dci_mean": round(np.mean(t2_dcis), 2),
            "delta_dci": round(delta, 2),
            "t": round(t, 3) if not np.isnan(t) else None,
            "p": round(p, 4) if not np.isnan(p) else None,
            "d": round(d_val, 3) if not np.isnan(d_val) else None,
            "cosine": round(cos, 4),
        })
        print(
            f"  {brand:20s}  T1 DCI={np.mean(t1_dcis):5.1f}  T2 DCI={np.mean(t2_dcis):5.1f}  "
            f"delta={delta:+5.2f}  t={t:+5.2f}  p={p:.3f}  d={d_val:+.2f}  cos={cos:.3f}"
        )

    rdf = pd.DataFrame(results)
    if not rdf.empty:
        p_vals = rdf["p"].dropna().values
        sig = benjamini_hochberg(p_vals)
        print(f"\n  Mean delta DCI (Turn1->Turn2): {rdf['delta_dci'].mean():+.2f}")
        print(f"  Mean cosine (Turn1 vs Turn2): {rdf['cosine'].mean():.3f}")
        print(f"  FDR-significant: {sum(sig)}/{len(sig)}")

    return rdf


def analysis_10_overall_summary(dci_df, interference_df, model_df):
    """Summary statistics and hypothesis testing."""
    print("\n" + "=" * 70)
    print("ANALYSIS 8: Overall Summary and Hypothesis Tests")
    print("=" * 70)

    if dci_df.empty:
        print("  No DCI data available.")
        return

    for portfolio_key, h_name, direction, h_num in [
        ("LVMH", "constructive", 1, "H1"),
        ("Unilever", "destructive", -1, "H2"),
        ("P&G", "negligible", 0, "H3"),
    ]:
        pdata = dci_df[dci_df["portfolio"] == portfolio_key]
        if pdata.empty:
            continue
        deltas = pdata["delta_dci"].values
        if len(deltas) == 0:
            continue

        t, p = stats.ttest_1samp(deltas, 0)
        d_val = (
            np.mean(deltas) / np.std(deltas, ddof=1)
            if np.std(deltas, ddof=1) > 0
            else 0
        )

        print(
            f"\n  {h_num} ({portfolio_key} {h_name}): mean delta DCI = {np.mean(deltas):+.2f}"
        )
        print(f"      t({len(deltas)-1}) = {t:.2f}, p = {p:.3f}, d = {d_val:.2f}")

        if direction == 0:
            equivalence_bound = 2.0
            within_bound = abs(np.mean(deltas)) < equivalence_bound
            print(f"      Within +/-{equivalence_bound} bound: {within_bound}")
            supported = within_bound and p > 0.05
        elif direction == 1:
            supported = np.mean(deltas) > 0 and p < 0.05
        else:
            supported = np.mean(deltas) < 0 and p < 0.05

        print(f"      {'SUPPORTED' if supported else 'NOT SUPPORTED'}")

    # BH correction across all brands
    if not dci_df.empty:
        p_values = dci_df["p_value"].dropna().values
        if len(p_values) > 1:
            sig = benjamini_hochberg(p_values, 0.05)
            print(f"\n  Benjamini-Hochberg correction ({len(p_values)} tests):")
            print(f"    Significant at FDR = .05: {sum(sig)}/{len(p_values)}")


def save_results(
    dci_df, dim_df, interference_df, model_df, tost_df, ablation_df,
    reco_df=None, mt_df=None,
):
    """Save all results to CSV."""
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    dci_df.to_csv(results_dir / "dci_comparison.csv", index=False)
    dim_df.to_csv(results_dir / "dimension_shifts.csv", index=False)
    interference_df.to_csv(results_dir / "interference_patterns.csv", index=False)
    model_df.to_csv(results_dir / "cross_model.csv", index=False)
    if not tost_df.empty:
        tost_df.to_csv(results_dir / "tost_equivalence.csv", index=False)
    if not ablation_df.empty:
        ablation_df.to_csv(results_dir / "ablation_system_prompt.csv", index=False)
    if reco_df is not None and not reco_df.empty:
        reco_df.to_csv(results_dir / "recommendation_comparison.csv", index=False)
    if mt_df is not None and not mt_df.empty:
        mt_df.to_csv(results_dir / "multiturn_analysis.csv", index=False)

    print(f"\nResults saved to {results_dir}/")


def main():
    records = load_responses()
    if not records:
        print("No parsed responses found. Run run_portfolio.py first.")
        sys.exit(1)

    n_total = len(records)
    conditions = set(r["condition"] for r in records)
    models = set(r["model_id"] for r in records)
    brands = set(r["brand"] for r in records)

    n_main = sum(1 for r in records if r["condition"] in ("solo", "portfolio"))
    n_reco = sum(
        1
        for r in records
        if r["condition"] in ("recommendation_solo", "recommendation_portfolio")
    )
    n_mt = sum(1 for r in records if r["condition"] == "multiturn")
    n_ablation = sum(1 for r in records if r["condition"] == "system_portfolio")

    print(
        f"Loaded {n_total} responses "
        f"({n_main} main, {n_reco} recommendation, {n_mt} multiturn, {n_ablation} ablation)"
    )
    print(f"Models: {', '.join(sorted(models))}")
    print(f"Brands: {', '.join(sorted(brands))}")
    print(f"Conditions: {', '.join(sorted(conditions))}")

    df = records_to_dataframe(records)

    # Main analyses (solo vs portfolio direct rating)
    main_df = df[df["condition"].isin(["solo", "portfolio"])]

    dci_df = analysis_1_dci_comparison(main_df)
    dim_df = analysis_2_dimension_shifts(main_df)
    interference_df = analysis_3_interference_patterns(main_df)
    model_df = analysis_4_cross_model(main_df)
    tost_df = analysis_5_power_and_tost(dci_df)
    analysis_6_subgroups(main_df, dci_df)
    ablation_df = analysis_7_ablation(df)
    reco_df = analysis_8_recommendation(df)
    mt_df = analysis_9_multiturn(df)
    analysis_10_overall_summary(dci_df, interference_df, model_df)

    # New v2.0 analyses
    analysis_11_native_language(df)
    analysis_12_tradition_subgroups(main_df)

    save_results(
        dci_df, dim_df, interference_df, model_df, tost_df, ablation_df,
        reco_df, mt_df,
    )


def analysis_11_native_language(df):
    """Compare English vs native-language portfolio framing for home portfolios."""
    print("\n" + "=" * 70)
    print("ANALYSIS 11: Native-Language Ablation (H8 + H9)")
    print("=" * 70)

    native_portfolios = {
        "L'Oreal": {"language": "French", "home_models": {"mistral"}},
        "Geely": {"language": "Chinese", "home_models": {"deepseek", "qwen3"}},
        "Toyota": {"language": "Japanese", "home_models": {"swallow"}},
        "Yandex": {"language": "Russian", "home_models": {"yandex"}},
    }

    native_df = df[df["condition"].isin(["native_solo", "native_portfolio"])]
    english_df = df[df["condition"].isin(["solo", "portfolio"])]

    if native_df.empty:
        print("  No native-language data found. Skipping.")
        return

    print(f"\n  Native-language observations: {len(native_df)}")

    for portfolio_key, meta in native_portfolios.items():
        print(f"\n  --- {portfolio_key} ({meta['language']}) ---")

        port_native = native_df[native_df["portfolio"] == portfolio_key]
        port_english = english_df[english_df["portfolio"] == portfolio_key]

        if port_native.empty or port_english.empty:
            print("    Insufficient data")
            continue

        brands = sorted(port_native["brand"].unique())
        for brand in brands:
            # English: solo vs portfolio delta DCI
            eng_solo = port_english[(port_english["brand"] == brand) & (port_english["condition"] == "solo")]
            eng_port = port_english[(port_english["brand"] == brand) & (port_english["condition"] == "portfolio")]
            nat_solo = port_native[(port_native["brand"] == brand) & (port_native["condition"] == "native_solo")]
            nat_port = port_native[(port_native["brand"] == brand) & (port_native["condition"] == "native_portfolio")]

            if eng_solo.empty or eng_port.empty or nat_solo.empty or nat_port.empty:
                continue

            eng_solo_dci = eng_solo[DIMENSIONS].apply(lambda row: compute_dci(row.values), axis=1)
            eng_port_dci = eng_port[DIMENSIONS].apply(lambda row: compute_dci(row.values), axis=1)
            nat_solo_dci = nat_solo[DIMENSIONS].apply(lambda row: compute_dci(row.values), axis=1)
            nat_port_dci = nat_port[DIMENSIONS].apply(lambda row: compute_dci(row.values), axis=1)

            eng_delta = eng_port_dci.mean() - eng_solo_dci.mean()
            nat_delta = nat_port_dci.mean() - nat_solo_dci.mean()
            diff = nat_delta - eng_delta

            print(f"    {brand:20s}  eng_delta={eng_delta:+.2f}  nat_delta={nat_delta:+.2f}  diff={diff:+.2f}")

            # H9: Home-model amplification
            for model_id in meta["home_models"]:
                home_nat_solo = nat_solo[nat_solo["model"] == model_id]
                home_nat_port = nat_port[nat_port["model"] == model_id]
                home_eng_solo = eng_solo[eng_solo["model"] == model_id]
                home_eng_port = eng_port[eng_port["model"] == model_id]

                if home_nat_solo.empty or home_nat_port.empty:
                    continue

                home_nat_solo_dci = home_nat_solo[DIMENSIONS].apply(lambda r: compute_dci(r.values), axis=1)
                home_nat_port_dci = home_nat_port[DIMENSIONS].apply(lambda r: compute_dci(r.values), axis=1)
                home_eng_solo_dci = home_eng_solo[DIMENSIONS].apply(lambda r: compute_dci(r.values), axis=1)
                home_eng_port_dci = home_eng_port[DIMENSIONS].apply(lambda r: compute_dci(r.values), axis=1)

                home_eng_d = home_eng_port_dci.mean() - home_eng_solo_dci.mean() if not home_eng_solo_dci.empty else 0
                home_nat_d = home_nat_port_dci.mean() - home_nat_solo_dci.mean()
                home_diff = home_nat_d - home_eng_d

                print(f"      HOME ({model_id:10s})  eng_delta={home_eng_d:+.2f}  nat_delta={home_nat_d:+.2f}  diff={home_diff:+.2f}")


def analysis_12_tradition_subgroups(main_df):
    """Per-tradition subgroup analysis (7 traditions)."""
    print("\n" + "=" * 70)
    print("ANALYSIS 12: Per-Tradition Sub-Group Analysis (7 traditions)")
    print("=" * 70)

    for tradition, model_ids in sorted(TRADITION_GROUPS.items()):
        trad_df = main_df[main_df["model"].isin(model_ids)]
        if trad_df.empty:
            continue

        solo = trad_df[trad_df["condition"] == "solo"]
        port = trad_df[trad_df["condition"] == "portfolio"]

        if solo.empty or port.empty:
            continue

        solo_dcis = solo.groupby(["portfolio", "brand"]).apply(
            lambda g: compute_dci(g[DIMENSIONS].mean().values)
        )
        port_dcis = port.groupby(["portfolio", "brand"]).apply(
            lambda g: compute_dci(g[DIMENSIONS].mean().values)
        )

        # Align indices
        common = solo_dcis.index.intersection(port_dcis.index)
        if len(common) == 0:
            continue

        deltas = port_dcis.loc[common] - solo_dcis.loc[common]
        mean_delta = deltas.mean()

        # Cosine per brand
        cosines = []
        for idx in common:
            s = solo.loc[(solo["portfolio"] == idx[0]) & (solo["brand"] == idx[1]), DIMENSIONS].mean().values
            p = port.loc[(port["portfolio"] == idx[0]) & (port["brand"] == idx[1]), DIMENSIONS].mean().values
            cosines.append(cosine_similarity(s, p))
        mean_cos = np.mean(cosines) if cosines else np.nan

        n_models = len(model_ids.intersection(set(main_df["model"].unique())))
        n_obs = len(trad_df)

        if len(deltas) > 1:
            t_stat, p_val = stats.ttest_1samp(deltas.values, 0)
            d = mean_delta / deltas.std() if deltas.std() > 0 else 0
        else:
            t_stat, p_val, d = np.nan, np.nan, np.nan

        print(
            f"  {tradition:12s}  models={n_models}  n={n_obs:4d}  "
            f"delta DCI={mean_delta:+.2f}  t={t_stat:+.2f}  p={p_val:.3f}  "
            f"d={d:+.2f}  cos={mean_cos:.3f}"
        )


if __name__ == "__main__":
    main()
