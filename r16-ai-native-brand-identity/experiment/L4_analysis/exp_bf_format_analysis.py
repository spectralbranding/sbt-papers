#!/usr/bin/env python3
"""Analysis script for Experiment D: Brand Function Format Optimization.

Reads exp_bf_format.jsonl and produces:
  - exp_bf_format_results.json (full statistical results)
  - exp_bf_format_summary.md (formatted summary tables)

Usage:
    uv run python exp_bf_format_analysis.py
    uv run python exp_bf_format_analysis.py --verify  # re-derive and diff
"""

import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict
from itertools import combinations

import numpy as np
from scipy import stats as sp_stats

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DIMENSIONS = [
    "Semiotic", "Narrative", "Ideological", "Experiential",
    "Social", "Economic", "Cultural", "Temporal",
]

CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

FORMAT_CONDITIONS = ["F1_json", "F2_prose", "F3_tabular", "F4_ranked", "F5_vector"]
FORMAT_LABELS = {
    "F1_json": "JSON Structured",
    "F2_prose": "Prose Narrative",
    "F3_tabular": "Tabular Minimal",
    "F4_ranked": "Ranked List",
    "F5_vector": "Score-Only Vector",
}

HARD_DIMS = {"Economic", "Semiotic"}
SOFT_DIMS = {"Cultural", "Temporal", "Ideological", "Narrative"}

BONFERRONI_ALPHA = 0.05 / 8  # .00625


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data(path: Path) -> list[dict]:
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def filter_valid(records: list[dict]) -> list[dict]:
    return [r for r in records if r.get("weights_valid")]


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def cosine_sim(a: list[float], b: list[float]) -> float:
    a_arr = np.array(a, dtype=float)
    b_arr = np.array(b, dtype=float)
    dot = np.dot(a_arr, b_arr)
    na = np.linalg.norm(a_arr)
    nb = np.linalg.norm(b_arr)
    if na == 0 or nb == 0:
        return 0.0
    return float(dot / (na * nb))


def per_dim_mae(weights: dict[str, float], brand: str) -> dict[str, float]:
    """Per-dimension MAE relative to canonical (both on 0-10 scale)."""
    canonical = CANONICAL_PROFILES[brand]
    total = sum(weights.values())
    if total == 0:
        return {d: float("nan") for d in DIMENSIONS}
    # Normalize weights to sum to canonical sum
    canon_sum = sum(canonical)
    result = {}
    for i, dim in enumerate(DIMENSIONS):
        observed_norm = weights.get(dim, 0.0) / total * canon_sum
        result[dim] = abs(observed_norm - canonical[i])
    return result


def bootstrap_ci(data: np.ndarray, n_boot: int = 10000, ci: float = 0.95) -> tuple[float, float]:
    """Bootstrap confidence interval for the mean."""
    if len(data) == 0:
        return (float("nan"), float("nan"))
    np.random.seed(42)
    means = np.array([np.mean(np.random.choice(data, size=len(data), replace=True)) for _ in range(n_boot)])
    alpha = (1 - ci) / 2
    return (float(np.percentile(means, alpha * 100)), float(np.percentile(means, (1 - alpha) * 100)))


def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    """Compute Cohen's d for two independent groups."""
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return float("nan")
    var1 = np.var(group1, ddof=1)
    var2 = np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return float((np.mean(group1) - np.mean(group2)) / pooled_std)


# ---------------------------------------------------------------------------
# Primary analyses
# ---------------------------------------------------------------------------

def analyze(records: list[dict]) -> dict:
    valid = filter_valid(records)
    if not valid:
        return {"error": "No valid records"}

    # Group by format
    by_format = defaultdict(list)
    for r in valid:
        by_format[r["condition"]].append(r)

    # 1. Cosine similarity per format
    format_cosines = {}
    for fmt in FORMAT_CONDITIONS:
        cosines = []
        for r in by_format[fmt]:
            brand = r["brand"]
            canonical = CANONICAL_PROFILES[brand]
            observed = [r["parsed_weights"].get(dim, 0.0) for dim in DIMENSIONS]
            cos = cosine_sim(observed, canonical)
            cosines.append(cos)
        arr = np.array(cosines)
        ci_low, ci_high = bootstrap_ci(arr)
        format_cosines[fmt] = {
            "mean": round(float(np.mean(arr)), 4),
            "std": round(float(np.std(arr, ddof=1)), 4),
            "n": len(arr),
            "ci_95_low": round(ci_low, 4),
            "ci_95_high": round(ci_high, 4),
        }

    # 2. One-way ANOVA across formats
    groups = []
    for fmt in FORMAT_CONDITIONS:
        cosines = []
        for r in by_format[fmt]:
            brand = r["brand"]
            canonical = CANONICAL_PROFILES[brand]
            observed = [r["parsed_weights"].get(dim, 0.0) for dim in DIMENSIONS]
            cosines.append(cosine_sim(observed, canonical))
        groups.append(np.array(cosines))
    f_stat, p_val = sp_stats.f_oneway(*groups)

    # Eta-squared
    grand_mean = np.mean(np.concatenate(groups))
    ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)
    ss_total = sum(np.sum((g - grand_mean) ** 2) for g in groups)
    eta_sq = ss_between / ss_total if ss_total > 0 else 0.0

    anova_result = {
        "f_statistic": round(float(f_stat), 3),
        "p_value": round(float(p_val), 6),
        "eta_squared": round(float(eta_sq), 4),
        "k_groups": len(groups),
        "n_total": sum(len(g) for g in groups),
    }

    # 3. Pairwise comparisons (Bonferroni-corrected)
    pairwise = {}
    for (i, fmt_a), (j, fmt_b) in combinations(enumerate(FORMAT_CONDITIONS), 2):
        t_stat, p = sp_stats.ttest_ind(groups[i], groups[j])
        d = cohens_d(groups[i], groups[j])
        key = f"{fmt_a}_vs_{fmt_b}"
        pairwise[key] = {
            "t_statistic": round(float(t_stat), 3),
            "p_value": round(float(p), 6),
            "p_bonferroni": round(min(float(p) * 10, 1.0), 6),  # 10 pairwise comparisons
            "significant_bonferroni": float(p) * 10 < 0.05,
            "cohens_d": round(d, 3),
        }

    # 4. Per-model cosine means
    by_model = defaultdict(lambda: defaultdict(list))
    for r in valid:
        brand = r["brand"]
        canonical = CANONICAL_PROFILES[brand]
        observed = [r["parsed_weights"].get(dim, 0.0) for dim in DIMENSIONS]
        cos = cosine_sim(observed, canonical)
        by_model[r["model_id"]][r["condition"]].append(cos)

    model_results = {}
    for model_id, fmt_data in by_model.items():
        model_results[model_id] = {}
        for fmt in FORMAT_CONDITIONS:
            arr = np.array(fmt_data.get(fmt, []))
            if len(arr) > 0:
                model_results[model_id][fmt] = {
                    "mean": round(float(np.mean(arr)), 4),
                    "std": round(float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0, 4),
                    "n": len(arr),
                }

    # 5. Kendall's W (format ranking concordance across models)
    model_names = list(by_model.keys())
    if len(model_names) >= 2:
        # Each model ranks the 5 formats by mean cosine
        rankings = []
        for model_id in model_names:
            means = []
            for fmt in FORMAT_CONDITIONS:
                arr = np.array(by_model[model_id].get(fmt, [0]))
                means.append(float(np.mean(arr)))
            # Rank: highest cosine = rank 1
            order = np.argsort(means)[::-1]
            ranks = np.empty_like(order)
            ranks[order] = np.arange(1, len(order) + 1)
            rankings.append(ranks)
        rankings = np.array(rankings)  # shape: (n_models, 5)
        k = rankings.shape[0]  # number of raters
        n = rankings.shape[1]  # number of items
        rank_sums = rankings.sum(axis=0)
        mean_rank_sum = np.mean(rank_sums)
        S = np.sum((rank_sums - mean_rank_sum) ** 2)
        W = 12 * S / (k ** 2 * (n ** 3 - n))
        kendall_w = {
            "W": round(float(W), 4),
            "k_raters": k,
            "n_items": n,
            "interpretation": "strong" if W > 0.7 else "moderate" if W > 0.5 else "weak",
        }
    else:
        kendall_w = {"W": None, "note": "insufficient models"}

    # 6. Per-dimension MAE by format (H5: soft vs hard dims)
    dim_mae_by_format = defaultdict(lambda: defaultdict(list))
    for r in valid:
        brand = r["brand"]
        mae = per_dim_mae(r["parsed_weights"], brand)
        for dim in DIMENSIONS:
            dim_mae_by_format[r["condition"]][dim].append(mae[dim])

    dim_analysis = {}
    for fmt in FORMAT_CONDITIONS:
        dim_analysis[fmt] = {}
        for dim in DIMENSIONS:
            arr = np.array(dim_mae_by_format[fmt].get(dim, []))
            if len(arr) > 0:
                dim_analysis[fmt][dim] = {
                    "mean_mae": round(float(np.nanmean(arr)), 4),
                    "std_mae": round(float(np.nanstd(arr, ddof=1)) if len(arr) > 1 else 0.0, 4),
                }

    # Hard vs soft dimension MAE comparison
    hard_soft = {}
    for fmt in FORMAT_CONDITIONS:
        hard_mae = []
        soft_mae = []
        for r in by_format[fmt]:
            mae = per_dim_mae(r["parsed_weights"], r["brand"])
            for dim in HARD_DIMS:
                hard_mae.append(mae[dim])
            for dim in SOFT_DIMS:
                soft_mae.append(mae[dim])
        hard_arr = np.array(hard_mae)
        soft_arr = np.array(soft_mae)
        t_stat, p = sp_stats.ttest_ind(hard_arr, soft_arr)
        hard_soft[fmt] = {
            "hard_mean_mae": round(float(np.nanmean(hard_arr)), 4),
            "soft_mean_mae": round(float(np.nanmean(soft_arr)), 4),
            "t_statistic": round(float(t_stat), 3),
            "p_value": round(float(p), 6),
            "soft_worse": float(np.nanmean(soft_arr)) > float(np.nanmean(hard_arr)),
        }

    # 7. Parse success rate
    total_by_format = defaultdict(int)
    valid_by_format = defaultdict(int)
    for r in records:
        total_by_format[r["condition"]] += 1
        if r.get("weights_valid"):
            valid_by_format[r["condition"]] += 1

    parse_rates = {}
    for fmt in FORMAT_CONDITIONS:
        total = total_by_format[fmt]
        success = valid_by_format[fmt]
        parse_rates[fmt] = {
            "total": total,
            "valid": success,
            "rate": round(success / total, 4) if total > 0 else 0.0,
        }

    # 8. Response time by format
    response_times = defaultdict(list)
    for r in valid:
        response_times[r["condition"]].append(r.get("response_time_ms", 0))

    time_stats = {}
    for fmt in FORMAT_CONDITIONS:
        arr = np.array(response_times[fmt])
        if len(arr) > 0:
            time_stats[fmt] = {
                "mean_ms": round(float(np.mean(arr)), 0),
                "median_ms": round(float(np.median(arr)), 0),
                "p95_ms": round(float(np.percentile(arr, 95)), 0),
            }

    # 9. Summary stats
    total_cost = sum(r.get("api_cost_usd", 0) for r in records)
    total_input = sum(r.get("token_count_input", 0) for r in records)
    total_output = sum(r.get("token_count_output", 0) for r in records)

    # Hypothesis verdicts
    best_fmt = max(FORMAT_CONDITIONS, key=lambda f: format_cosines.get(f, {}).get("mean", 0))
    worst_fmt = min(FORMAT_CONDITIONS, key=lambda f: format_cosines.get(f, {}).get("mean", 1))

    h1 = best_fmt == "F1_json"
    h2_key = "F1_json_vs_F2_prose"
    h2 = pairwise.get(h2_key, {}).get("significant_bonferroni", False) and \
         format_cosines.get("F1_json", {}).get("mean", 0) > format_cosines.get("F2_prose", {}).get("mean", 0)
    h3 = worst_fmt == "F5_vector"
    h4 = kendall_w.get("W", 0) is not None and (kendall_w.get("W", 0) or 0) > 0.7
    # H5: check if soft dims have higher MAE on average across formats
    h5_checks = sum(1 for fmt in FORMAT_CONDITIONS if hard_soft.get(fmt, {}).get("soft_worse", False))
    h5 = h5_checks >= 4  # at least 4 of 5 formats show soft worse

    hypotheses = {
        "H1_structured_advantage": {
            "verdict": "SUPPORTED" if h1 else "NOT SUPPORTED",
            "best_format": best_fmt,
            "best_mean_cosine": format_cosines.get(best_fmt, {}).get("mean"),
            "anova_p": anova_result["p_value"],
        },
        "H2_prose_penalty": {
            "verdict": "SUPPORTED" if h2 else "NOT SUPPORTED",
            "f1_mean": format_cosines.get("F1_json", {}).get("mean"),
            "f2_mean": format_cosines.get("F2_prose", {}).get("mean"),
            "p_bonferroni": pairwise.get(h2_key, {}).get("p_bonferroni"),
            "cohens_d": pairwise.get(h2_key, {}).get("cohens_d"),
        },
        "H3_score_only_floor": {
            "verdict": "SUPPORTED" if h3 else "NOT SUPPORTED",
            "worst_format": worst_fmt,
            "worst_mean_cosine": format_cosines.get(worst_fmt, {}).get("mean"),
        },
        "H4_cross_model_consistency": {
            "verdict": "SUPPORTED" if h4 else "NOT SUPPORTED",
            "kendall_w": kendall_w.get("W"),
        },
        "H5_dimension_specific": {
            "verdict": "SUPPORTED" if h5 else "NOT SUPPORTED",
            "formats_where_soft_worse": h5_checks,
        },
    }

    return {
        "experiment": "exp_d_bf_format",
        "total_records": len(records),
        "valid_records": len(valid),
        "total_cost_usd": round(total_cost, 2),
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "format_cosines": format_cosines,
        "anova": anova_result,
        "pairwise_comparisons": pairwise,
        "model_results": model_results,
        "kendall_w": kendall_w,
        "dimension_mae_by_format": dim_analysis,
        "hard_vs_soft": hard_soft,
        "parse_rates": parse_rates,
        "response_times": time_stats,
        "hypotheses": hypotheses,
    }


# ---------------------------------------------------------------------------
# Summary markdown
# ---------------------------------------------------------------------------

def generate_summary(results: dict) -> str:
    lines = []
    lines.append("# Experiment D: Brand Function Format Optimization -- Results Summary")
    lines.append("")
    lines.append(f"**Total API calls**: {results['total_records']}")
    lines.append(f"**Valid responses**: {results['valid_records']}")
    lines.append(f"**Total cost**: ${results['total_cost_usd']:.2f}")
    lines.append("")

    # Hypothesis verdicts
    lines.append("## Hypothesis Verdicts")
    lines.append("")
    for hid, h in results["hypotheses"].items():
        lines.append(f"- **{hid}**: {h['verdict']}")
    lines.append("")

    # Table 1: Format cosines
    lines.append("## Table 1: Cosine Similarity to Canonical Profile by Format")
    lines.append("")
    lines.append("| Format | Mean Cosine | SD | n | 95% CI |")
    lines.append("|--------|-------------|-----|---|--------|")
    for fmt in FORMAT_CONDITIONS:
        fc = results["format_cosines"].get(fmt, {})
        label = FORMAT_LABELS.get(fmt, fmt)
        lines.append(
            f"| {label} | {fc.get('mean', '-'):.4f} | {fc.get('std', '-'):.4f} | "
            f"{fc.get('n', 0)} | [{fc.get('ci_95_low', '-'):.4f}, {fc.get('ci_95_high', '-'):.4f}] |"
        )
    lines.append("")

    # ANOVA
    a = results["anova"]
    lines.append("## ANOVA: Format Effect on Cosine Similarity")
    lines.append("")
    lines.append(f"- F({a['k_groups']-1}, {a['n_total']-a['k_groups']}) = {a['f_statistic']:.3f}, "
                 f"p = {a['p_value']:.6f}, eta-sq = {a['eta_squared']:.4f}")
    lines.append("")

    # Pairwise
    lines.append("## Table 2: Pairwise Comparisons (Bonferroni-corrected)")
    lines.append("")
    lines.append("| Comparison | t | p | p_bonf | Cohen's d | Sig? |")
    lines.append("|------------|---|---|--------|-----------|------|")
    for key, pw in results["pairwise_comparisons"].items():
        sig = "Yes" if pw["significant_bonferroni"] else "No"
        lines.append(
            f"| {key} | {pw['t_statistic']:.3f} | {pw['p_value']:.6f} | "
            f"{pw['p_bonferroni']:.6f} | {pw['cohens_d']:.3f} | {sig} |"
        )
    lines.append("")

    # Per-model
    lines.append("## Table 3: Mean Cosine by Model x Format")
    lines.append("")
    header = "| Model | " + " | ".join(FORMAT_LABELS[f] for f in FORMAT_CONDITIONS) + " |"
    sep = "|-------|" + "|".join(["--------"] * len(FORMAT_CONDITIONS)) + "|"
    lines.append(header)
    lines.append(sep)
    for model_id, fmt_data in results.get("model_results", {}).items():
        row = f"| {model_id} |"
        for fmt in FORMAT_CONDITIONS:
            val = fmt_data.get(fmt, {}).get("mean", "-")
            if isinstance(val, float):
                row += f" {val:.4f} |"
            else:
                row += f" {val} |"
        lines.append(row)
    lines.append("")

    # Kendall's W
    kw = results["kendall_w"]
    lines.append("## Cross-Model Format Ranking Concordance")
    lines.append("")
    if kw.get("W") is not None:
        lines.append(f"- Kendall's W = {kw['W']:.4f} ({kw['interpretation']})")
    else:
        lines.append("- Insufficient models for Kendall's W")
    lines.append("")

    # Hard vs soft
    lines.append("## Table 4: Hard vs Soft Dimension MAE by Format")
    lines.append("")
    lines.append("| Format | Hard MAE | Soft MAE | t | p | Soft worse? |")
    lines.append("|--------|----------|----------|---|---|-------------|")
    for fmt in FORMAT_CONDITIONS:
        hs = results.get("hard_vs_soft", {}).get(fmt, {})
        label = FORMAT_LABELS.get(fmt, fmt)
        lines.append(
            f"| {label} | {hs.get('hard_mean_mae', '-'):.4f} | {hs.get('soft_mean_mae', '-'):.4f} | "
            f"{hs.get('t_statistic', '-'):.3f} | {hs.get('p_value', '-'):.6f} | "
            f"{'Yes' if hs.get('soft_worse') else 'No'} |"
        )
    lines.append("")

    # Parse rates
    lines.append("## Table 5: Parse Success Rates by Format")
    lines.append("")
    lines.append("| Format | Total | Valid | Rate |")
    lines.append("|--------|-------|-------|------|")
    for fmt in FORMAT_CONDITIONS:
        pr = results.get("parse_rates", {}).get(fmt, {})
        label = FORMAT_LABELS.get(fmt, fmt)
        lines.append(f"| {label} | {pr.get('total', 0)} | {pr.get('valid', 0)} | {pr.get('rate', 0):.1%} |")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--input", type=str, default=None)
    args = parser.parse_args()

    base = Path(__file__).parent.parent
    input_path = Path(args.input) if args.input else base / "L3_sessions" / "exp_bf_format.jsonl"
    output_json = base / "L4_analysis" / "exp_bf_format_results.json"
    output_md = base / "L4_analysis" / "exp_bf_format_summary.md"

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    records = load_data(input_path)
    print(f"Loaded {len(records)} records from {input_path}")

    results = analyze(records)

    if args.verify and output_json.exists():
        existing = json.loads(output_json.read_text())
        # Compare key metrics
        for fmt in FORMAT_CONDITIONS:
            old = existing.get("format_cosines", {}).get(fmt, {}).get("mean")
            new = results.get("format_cosines", {}).get(fmt, {}).get("mean")
            if old != new:
                print(f"MISMATCH {fmt}: old={old} new={new}")
        print("Verification complete.")
        return

    # Write results
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results written to {output_json}")

    summary = generate_summary(results)
    with open(output_md, "w") as f:
        f.write(summary)
    print(f"Summary written to {output_md}")

    # Print hypothesis verdicts
    print("\n" + "=" * 60)
    print("HYPOTHESIS VERDICTS")
    print("=" * 60)
    for hid, h in results["hypotheses"].items():
        print(f"  {hid}: {h['verdict']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
