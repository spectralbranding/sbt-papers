#!/usr/bin/env python3
"""
R20 Portfolio-AI Experiment — Analysis

Reads responses from responses/ and computes:
1. Per-brand DCI (Dimensional Concentration Index) solo vs portfolio
2. Cosine similarity between solo and portfolio profiles
3. Portfolio interference patterns (constructive vs destructive)
4. Cross-model consistency
5. Statistical tests (paired t-tests, Wilcoxon, effect sizes)

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

# Canonical SBT profiles for reference brands
CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

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
}


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
    """Dimensional Concentration Index: how concentrated vs uniform the profile is.

    DCI = sum of absolute deviations from uniform distribution, normalized to [0, 100].
    Higher = more concentrated (peakier). Lower = more uniform (flatter).
    """
    if np.all(profile == 0):
        return 0.0
    weights = profile / profile.sum()
    uniform = 1.0 / len(profile)
    return float(np.sum(np.abs(weights - uniform)) * 100 / 2)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two profiles."""
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


# ---------------------------------------------------------------------------
# Analysis Functions
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
                if row["condition"] == "solo":
                    solo_profiles.append({"profile": profile, "dci": dci})
                else:
                    port_profiles.append({"profile": profile, "dci": dci})

            solo_dcis = [s["dci"] for s in solo_profiles]
            port_dcis = [p["dci"] for p in port_profiles]

            if len(solo_dcis) < 2 or len(port_dcis) < 2:
                print(
                    f"  {brand}: insufficient data (solo={len(solo_dcis)}, port={len(port_dcis)})"
                )
                continue

            solo_mean = np.mean(solo_dcis)
            port_mean = np.mean(port_dcis)
            delta = port_mean - solo_mean

            # Paired by repetition within each model? No — use independent t-test
            t_stat, p_val = stats.ttest_ind(port_dcis, solo_dcis)
            d = cohens_d(port_dcis, solo_dcis)

            # Also compute mean profiles for cosine
            solo_mean_profile = np.mean([s["profile"] for s in solo_profiles], axis=0)
            port_mean_profile = np.mean([p["profile"] for p in port_profiles], axis=0)
            cos_sim = cosine_similarity(solo_mean_profile, port_mean_profile)
            euc_dist = euclidean_distance(solo_mean_profile, port_mean_profile)

            print(
                f"  {brand:20s}  Solo DCI={solo_mean:5.1f}  Portfolio DCI={port_mean:5.1f}  "
                f"Delta={delta:+5.1f}  t={t_stat:+6.2f}  p={p_val:.3f}  d={d:+.2f}  "
                f"cos={cos_sim:.3f}  L2={euc_dist:.2f}"
            )

            results.append(
                {
                    "portfolio": portfolio,
                    "brand": brand,
                    "portfolio_type": PORTFOLIO_META[portfolio]["type"],
                    "predicted": PORTFOLIO_META[portfolio]["predicted_interference"],
                    "solo_dci_mean": solo_mean,
                    "solo_dci_sd": np.std(solo_dcis, ddof=1),
                    "port_dci_mean": port_mean,
                    "port_dci_sd": np.std(port_dcis, ddof=1),
                    "delta_dci": delta,
                    "t_stat": t_stat,
                    "p_value": p_val,
                    "cohens_d": d,
                    "cosine_similarity": cos_sim,
                    "euclidean_distance": euc_dist,
                    "n_solo": len(solo_dcis),
                    "n_portfolio": len(port_dcis),
                }
            )

    return pd.DataFrame(results)


def analysis_2_dimension_shifts(df):
    """Per-dimension shift analysis: which dimensions move most under portfolio framing."""
    print("\n" + "=" * 70)
    print("ANALYSIS 2: Per-Dimension Score Shifts (Portfolio - Solo)")
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

            # Find largest shifts
            sorted_dims = sorted(
                shifts.items(), key=lambda x: abs(x[1]["delta"]), reverse=True
            )
            top3 = sorted_dims[:3]

            print(f"  {brand}:")
            for dim, s in top3:
                sig = "*" if s["p"] < 0.05 else ""
                print(
                    f"    {dim:14s}  delta={s['delta']:+5.2f}  t={s['t']:+5.2f}  "
                    f"p={s['p']:.3f}{sig}  d={s['d']:+.2f}"
                )

            for dim, s in shifts.items():
                results.append(
                    {
                        "portfolio": portfolio,
                        "brand": brand,
                        "dimension": dim,
                        "delta": s["delta"],
                        "t_stat": s["t"],
                        "p_value": s["p"],
                        "cohens_d": s["d"],
                    }
                )

    return pd.DataFrame(results)


def analysis_3_interference_patterns(df):
    """Compute portfolio-level interference: constructive vs destructive by portfolio."""
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

        # Compute mean profiles per brand per condition
        profiles = {}
        for brand in brands:
            bdf = pdf[pdf["brand"] == brand]
            for cond in ["solo", "portfolio"]:
                cdf = bdf[bdf["condition"] == cond]
                if len(cdf) > 0:
                    profiles[(brand, cond)] = cdf[DIMENSIONS].mean().values

        # Cross-brand cosine similarity within each condition
        for cond in ["solo", "portfolio"]:
            cos_sims = []
            for i, b1 in enumerate(brands):
                for b2 in brands[i + 1 :]:
                    if (b1, cond) in profiles and (b2, cond) in profiles:
                        cs = cosine_similarity(
                            profiles[(b1, cond)], profiles[(b2, cond)]
                        )
                        cos_sims.append(cs)
                        print(f"    {cond:10s}  {b1} x {b2}: cos={cs:.3f}")
            if cos_sims:
                print(f"    {cond:10s}  mean cross-brand cos={np.mean(cos_sims):.3f}")

        # Interference direction per dimension per brand
        print(f"\n    Dimension-level interference:")
        constructive_count = 0
        destructive_count = 0
        total_dims = 0

        for brand in brands:
            if (brand, "solo") not in profiles or (brand, "portfolio") not in profiles:
                continue
            solo_p = profiles[(brand, "solo")]
            port_p = profiles[(brand, "portfolio")]

            # Category mean = mean of all solo profiles in this portfolio
            category_mean = np.mean(
                [profiles[(b, "solo")] for b in brands if (b, "solo") in profiles],
                axis=0,
            )

            for i, dim in enumerate(DIMENSIONS):
                deviation_solo = solo_p[i] - category_mean[i]
                shift = port_p[i] - solo_p[i]

                # Constructive: portfolio framing moves score further from category mean
                # (amplifies brand's distinctive position)
                # Destructive: portfolio framing moves score toward category mean
                # (flattens brand's distinctive position)
                if (
                    abs(deviation_solo) > 0.5
                ):  # only count dimensions where brand deviates
                    total_dims += 1
                    if np.sign(shift) == np.sign(deviation_solo):
                        constructive_count += 1
                    elif abs(shift) > 0.3:  # non-trivial destructive shift
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
                "ratio": interference_ratio,
                "match": match == "MATCH",
            }
        )

    return pd.DataFrame(results)


def analysis_4_cross_model(df):
    """Cross-model consistency: do all models show the same interference direction?"""
    print("\n" + "=" * 70)
    print("ANALYSIS 4: Cross-Model Consistency")
    print("=" * 70)

    results = []

    for portfolio in sorted(df["portfolio"].unique()):
        print(f"\n--- {portfolio} ---")
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
                        "solo_dci": solo_dci,
                        "port_dci": port_dci,
                        "delta_dci": port_dci - solo_dci,
                        "cosine": cos,
                    }
                )

    rdf = pd.DataFrame(results)
    if rdf.empty:
        print("  No data available.")
        return rdf

    # Summary: per-portfolio, how many models show DCI increase vs decrease
    for portfolio in sorted(rdf["portfolio"].unique()):
        pdata = rdf[rdf["portfolio"] == portfolio]
        increasing = (pdata["delta_dci"] > 0).sum()
        decreasing = (pdata["delta_dci"] < 0).sum()
        total = len(pdata)
        mean_cos = pdata["cosine"].mean()
        mean_delta = pdata["delta_dci"].mean()

        # Binomial test: is the direction consistent?
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

    return rdf


def analysis_5_overall_summary(dci_df, interference_df, model_df):
    """Summary statistics and hypothesis testing."""
    print("\n" + "=" * 70)
    print("ANALYSIS 5: Overall Summary and Hypothesis Tests")
    print("=" * 70)

    if dci_df.empty:
        print("  No DCI data available.")
        return

    # H1: LVMH portfolio framing increases DCI (constructive interference)
    lvmh = dci_df[dci_df["portfolio"] == "LVMH"]
    if not lvmh.empty:
        lvmh_delta = lvmh["delta_dci"].values
        if len(lvmh_delta) > 0:
            t, p = stats.ttest_1samp(lvmh_delta, 0)
            d = (
                np.mean(lvmh_delta) / np.std(lvmh_delta, ddof=1)
                if np.std(lvmh_delta, ddof=1) > 0
                else 0
            )
            print(
                f"\n  H1 (LVMH constructive): mean delta DCI = {np.mean(lvmh_delta):+.2f}"
            )
            print(f"      t({len(lvmh_delta)-1}) = {t:.2f}, p = {p:.3f}, d = {d:.2f}")
            print(
                f"      {'SUPPORTED' if np.mean(lvmh_delta) > 0 and p < .05 else 'NOT SUPPORTED'}"
            )

    # H2: Unilever portfolio framing decreases DCI (destructive interference)
    uni = dci_df[dci_df["portfolio"] == "Unilever"]
    if not uni.empty:
        uni_delta = uni["delta_dci"].values
        if len(uni_delta) > 0:
            t, p = stats.ttest_1samp(uni_delta, 0)
            d = (
                np.mean(uni_delta) / np.std(uni_delta, ddof=1)
                if np.std(uni_delta, ddof=1) > 0
                else 0
            )
            print(
                f"\n  H2 (Unilever destructive): mean delta DCI = {np.mean(uni_delta):+.2f}"
            )
            print(f"      t({len(uni_delta)-1}) = {t:.2f}, p = {p:.3f}, d = {d:.2f}")
            print(
                f"      {'SUPPORTED' if np.mean(uni_delta) < 0 and p < .05 else 'NOT SUPPORTED'}"
            )

    # H3: P&G portfolio framing has negligible effect (spectral spread)
    pg = dci_df[dci_df["portfolio"] == "P&G"]
    if not pg.empty:
        pg_delta = pg["delta_dci"].values
        if len(pg_delta) > 0:
            t, p = stats.ttest_1samp(pg_delta, 0)
            d = (
                np.mean(pg_delta) / np.std(pg_delta, ddof=1)
                if np.std(pg_delta, ddof=1) > 0
                else 0
            )
            equivalence_bound = 2.0  # DCI points
            print(f"\n  H3 (P&G negligible): mean delta DCI = {np.mean(pg_delta):+.2f}")
            print(f"      t({len(pg_delta)-1}) = {t:.2f}, p = {p:.3f}, d = {d:.2f}")
            within_bound = abs(np.mean(pg_delta)) < equivalence_bound
            print(f"      Within +/-{equivalence_bound} bound: {within_bound}")
            print(
                f"      {'SUPPORTED' if within_bound and p > .05 else 'NOT SUPPORTED'}"
            )

    # Multiple testing correction (Benjamini-Hochberg)
    if not dci_df.empty:
        p_values = dci_df["p_value"].dropna().values
        if len(p_values) > 1:
            sorted_p = np.sort(p_values)
            m = len(sorted_p)
            bh_threshold = [(i + 1) / m * 0.05 for i in range(m)]
            significant_bh = sum(
                1 for p, thr in zip(sorted_p, bh_threshold) if p <= thr
            )
            print(f"\n  Benjamini-Hochberg correction ({m} tests):")
            print(f"    Significant at FDR=.05: {significant_bh}/{m}")


def save_results(dci_df, dim_df, interference_df, model_df):
    """Save all results to CSV."""
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    dci_df.to_csv(results_dir / "dci_comparison.csv", index=False)
    dim_df.to_csv(results_dir / "dimension_shifts.csv", index=False)
    interference_df.to_csv(results_dir / "interference_patterns.csv", index=False)
    model_df.to_csv(results_dir / "cross_model.csv", index=False)

    print(f"\nResults saved to {results_dir}/")


def main():
    records = load_responses()
    if not records:
        print("No parsed responses found. Run run_portfolio.py first.")
        sys.exit(1)

    n_total = len(records)
    n_solo = sum(1 for r in records if r["condition"] == "solo")
    n_port = sum(1 for r in records if r["condition"] == "portfolio")
    models = set(r["model_id"] for r in records)
    brands = set(r["brand"] for r in records)

    print(f"Loaded {n_total} responses ({n_solo} solo, {n_port} portfolio)")
    print(f"Models: {', '.join(sorted(models))}")
    print(f"Brands: {', '.join(sorted(brands))}")

    df = records_to_dataframe(records)

    dci_df = analysis_1_dci_comparison(df)
    dim_df = analysis_2_dimension_shifts(df)
    interference_df = analysis_3_interference_patterns(df)
    model_df = analysis_4_cross_model(df)
    analysis_5_overall_summary(dci_df, interference_df, model_df)

    save_results(dci_df, dim_df, interference_df, model_df)


if __name__ == "__main__":
    main()
