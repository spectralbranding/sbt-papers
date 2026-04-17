#!/usr/bin/env python3
"""Analysis script for Experiment A: Multi-Step Agentic Collapse.

Reads exp_agentic_collapse.jsonl, tests H1-H3, produces results JSON
and summary markdown.

Usage:
    uv run python exp_agentic_collapse_analysis.py
"""

import datetime
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

RANDOM_SEED = 42
BOOTSTRAP_N = 10_000
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

CANONICAL_PROFILES = {
    "Hermes": [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5],
    "IKEA": [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0],
    "Patagonia": [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5],
    "Erewhon": [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5],
    "Tesla": [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0],
}

STRONG_IDEOLOGICAL = {"Patagonia"}
WEAK_IDEOLOGICAL = {"Erewhon", "Tesla"}


def load_data(jsonl_path: Path) -> list[dict]:
    """Load records from JSONL."""
    records = []
    with open(jsonl_path) as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def renormalize(weights: dict) -> dict:
    """Renormalize weights to sum to 100."""
    total = sum(weights.values())
    if total == 0:
        return weights
    factor = 100.0 / total
    return {k: round(v * factor, 3) for k, v in weights.items()}


def compute_dci(weights: dict) -> float:
    """DCI = (Economic + Semiotic) / 100. Weights are renormalized first."""
    w = renormalize(weights)
    return (w.get("Economic", 0) + w.get("Semiotic", 0)) / 100.0


def bootstrap_ci(
    data: np.ndarray,
    stat_fn=np.mean,
    n_boot: int = BOOTSTRAP_N,
    ci: float = 0.95,
    seed: int = RANDOM_SEED,
) -> tuple[float, float]:
    """Bootstrap confidence interval."""
    rng = np.random.RandomState(seed)
    boot_stats = np.array(
        [stat_fn(rng.choice(data, size=len(data), replace=True)) for _ in range(n_boot)]
    )
    alpha = (1 - ci) / 2
    return (
        float(np.percentile(boot_stats, 100 * alpha)),
        float(np.percentile(boot_stats, 100 * (1 - alpha))),
    )


def eta_squared(groups: list[np.ndarray]) -> float:
    """Compute eta-squared from groups."""
    all_data = np.concatenate(groups)
    grand_mean = np.mean(all_data)
    ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)
    ss_total = np.sum((all_data - grand_mean) ** 2)
    if ss_total == 0:
        return 0.0
    return float(ss_between / ss_total)


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    """Cohen's d (pooled SD). Positive = a > b."""
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return 0.0
    pooled_var = ((na - 1) * np.var(a, ddof=1) + (nb - 1) * np.var(b, ddof=1)) / (
        na + nb - 2
    )
    if pooled_var == 0:
        return 0.0
    return float((np.mean(a) - np.mean(b)) / np.sqrt(pooled_var))


def analyze(jsonl_path: Path) -> dict:
    """Run all pre-registered + exploratory analyses."""
    records = load_data(jsonl_path)

    # Separate by step, keep only valid weight records
    by_step = defaultdict(list)
    for r in records:
        if r.get("weights_valid") and r.get("parsed_weights"):
            by_step[r["step"]].append(r)

    step_counts = {s: len(recs) for s, recs in sorted(by_step.items())}
    total_records = len(records)
    total_valid = sum(step_counts.values())
    total_cost = sum(r.get("api_cost_usd", 0) for r in records)

    # Compute DCI per record
    for recs in by_step.values():
        for r in recs:
            r["_dci"] = compute_dci(r["parsed_weights"])

    # --- H1: Monotonic DCI Increase ---
    step_dcis = {}
    for s in [0, 2, 3]:
        dcis = np.array([r["_dci"] for r in by_step.get(s, [])])
        if len(dcis) > 0:
            step_dcis[s] = dcis

    h1_result = {"supported": False}
    if len(step_dcis) >= 2:
        groups = [step_dcis[s] for s in sorted(step_dcis.keys())]
        f_stat, p_val = stats.f_oneway(*groups)
        eta_sq = eta_squared(groups)

        step_means = {s: float(np.mean(d)) for s, d in sorted(step_dcis.items())}
        means_ordered = [step_means[s] for s in sorted(step_means.keys())]
        monotonic = all(
            means_ordered[i] <= means_ordered[i + 1]
            for i in range(len(means_ordered) - 1)
        )

        # Pairwise comparisons (Bonferroni)
        pairwise = {}
        sorted_steps = sorted(step_dcis.keys())
        n_pairs = len(sorted_steps) * (len(sorted_steps) - 1) // 2
        bonf_alpha = 0.05 / max(n_pairs, 1)
        for i in range(len(sorted_steps)):
            for j in range(i + 1, len(sorted_steps)):
                si, sj = sorted_steps[i], sorted_steps[j]
                t, p = stats.ttest_ind(step_dcis[si], step_dcis[sj])
                d = cohens_d(step_dcis[sj], step_dcis[si])
                pairwise[f"step{si}_vs_step{sj}"] = {
                    "t": round(float(t), 3),
                    "p": round(float(p), 3),
                    "p_bonferroni": round(min(float(p) * n_pairs, 1.0), 3),
                    "cohens_d": round(d, 3),
                    "significant": float(p) < bonf_alpha,
                }

        # Bootstrap CI on eta-sq
        all_dcis = np.concatenate(groups)
        eta_ci = bootstrap_ci(all_dcis, stat_fn=np.mean)

        h1_result = {
            "supported": float(p_val) < 0.05 and monotonic,
            "f_stat": round(float(f_stat), 3),
            "p": round(float(p_val), 3),
            "eta_sq": round(eta_sq, 3),
            "eta_sq_ci_95": [round(eta_ci[0], 3), round(eta_ci[1], 3)],
            "step_means": {f"step_{s}": round(m, 3) for s, m in step_means.items()},
            "monotonic": monotonic,
            "pairwise": pairwise,
        }

    # --- H2: Dimension-Specific Compounding ---
    target_dims = ["Cultural", "Temporal", "Economic"]
    dim_step_data = defaultdict(lambda: defaultdict(list))
    for s in [0, 2, 3]:
        for r in by_step.get(s, []):
            w = r["parsed_weights"]
            for dim in target_dims:
                dim_step_data[dim][s].append(w.get(dim, 0))

    h2_result = {"supported": False}
    collapse_rates = {}
    for dim in target_dims:
        ctrl = np.array(dim_step_data[dim].get(0, []))
        s3 = np.array(dim_step_data[dim].get(3, []))
        if len(ctrl) > 0 and len(s3) > 0:
            collapse_rates[dim] = round(float(np.mean(s3) - np.mean(ctrl)), 3)

    dim_means_by_step = {}
    for dim in target_dims:
        dim_means_by_step[dim] = {}
        for s in [0, 2, 3]:
            vals = dim_step_data[dim].get(s, [])
            if vals:
                dim_means_by_step[dim][f"step_{s}"] = round(float(np.mean(vals)), 3)

    cult_more = collapse_rates.get("Cultural", 0) < collapse_rates.get("Economic", 0)
    temp_more = collapse_rates.get("Temporal", 0) < collapse_rates.get("Economic", 0)
    h2_result = {
        "supported": cult_more or temp_more,
        "collapse_rates": collapse_rates,
        "dim_means_by_step": dim_means_by_step,
        "cultural_collapsed_more": cult_more,
        "temporal_collapsed_more": temp_more,
    }

    # --- H3: Ideological Signal Protection ---
    strong_compound = []
    weak_compound = []
    for r0 in by_step.get(0, []):
        brand = r0["brand"]
        matching_s3 = [
            r3
            for r3 in by_step.get(3, [])
            if r3["brand"] == brand
            and r3["model_id"] == r0["model_id"]
            and r3["repetition"] == r0["repetition"]
        ]
        if matching_s3:
            compound = matching_s3[0]["_dci"] - r0["_dci"]
            if brand in STRONG_IDEOLOGICAL:
                strong_compound.append(compound)
            elif brand in WEAK_IDEOLOGICAL:
                weak_compound.append(compound)

    h3_result = {"supported": False}
    if strong_compound and weak_compound:
        sa = np.array(strong_compound)
        wa = np.array(weak_compound)
        t_val, p_val = stats.ttest_ind(sa, wa)
        d = cohens_d(wa, sa)  # positive = weak compounds more
        d_ci = bootstrap_ci(np.concatenate([sa, wa]), stat_fn=np.mean)
        h3_result = {
            "supported": abs(d) >= 0.50 and float(p_val) < 0.05,
            "t": round(float(t_val), 3),
            "p": round(float(p_val), 3),
            "cohens_d": round(d, 3),
            "cohens_d_ci_95": [round(d_ci[0], 3), round(d_ci[1], 3)],
            "strong_ideo_mean": round(float(np.mean(sa)), 3),
            "strong_ideo_n": len(sa),
            "weak_ideo_mean": round(float(np.mean(wa)), 3),
            "weak_ideo_n": len(wa),
        }

    # --- Secondary: Per-dimension trajectories ---
    dim_trajectories = {}
    for dim in DIMENSIONS:
        dim_trajectories[dim] = {}
        for s in [0, 2, 3]:
            vals = [renormalize(r["parsed_weights"]).get(dim, 0) for r in by_step.get(s, [])]
            if vals:
                dim_trajectories[dim][f"step_{s}"] = {
                    "mean": round(float(np.mean(vals)), 3),
                    "std": round(float(np.std(vals, ddof=1)) if len(vals) > 1 else 0, 3),
                    "n": len(vals),
                }

    # --- Secondary: Model comparison ---
    model_compound = defaultdict(list)
    for r3 in by_step.get(3, []):
        brand = r3["brand"]
        model = r3["model_id"]
        ctrl_matches = [
            r0
            for r0 in by_step.get(0, [])
            if r0["brand"] == brand
            and r0["model_id"] == model
            and r0["repetition"] == r3["repetition"]
        ]
        if ctrl_matches:
            model_compound[model].append(r3["_dci"] - ctrl_matches[0]["_dci"])

    model_comparison = {}
    for model, rates in model_compound.items():
        arr = np.array(rates)
        model_comparison[model] = {
            "mean_compound": round(float(np.mean(arr)), 3),
            "std": round(float(np.std(arr, ddof=1)) if len(arr) > 1 else 0, 3),
            "n": len(arr),
        }
    if len(model_compound) >= 2:
        groups = [np.array(v) for v in model_compound.values()]
        f_m, p_m = stats.f_oneway(*groups)
        model_comparison["anova_f"] = round(float(f_m), 3)
        model_comparison["anova_p"] = round(float(p_m), 3)

    # --- Exploratory: Step 1 brand overlap ---
    step1_recs = [r for r in records if r.get("step") == 1 and r.get("step_1_brands")]
    brand_in_s1 = defaultdict(int)
    brand_total_s1 = defaultdict(int)
    for r in step1_recs:
        brand = r["brand"]
        brand_total_s1[brand] += 1
        s1_lower = [b.lower() for b in (r["step_1_brands"] or [])]
        if brand.lower() in s1_lower:
            brand_in_s1[brand] += 1

    retrieval_overlap = {}
    for brand in CANONICAL_PROFILES:
        total = brand_total_s1.get(brand, 0)
        incl = brand_in_s1.get(brand, 0)
        if total > 0:
            retrieval_overlap[brand] = {
                "included": incl,
                "total": total,
                "rate": round(incl / total, 3),
            }

    # --- Exploratory: Recommendation convergence ---
    rec_counts = defaultdict(int)
    for r in by_step.get(3, []):
        rb = r.get("recommended_brand", "unknown")
        if rb:
            rec_counts[rb] += 1
    total_recs = sum(rec_counts.values())
    if total_recs > 0:
        probs = np.array([c / total_recs for c in rec_counts.values()])
        shannon = float(-np.sum(probs * np.log2(probs + 1e-10)))
    else:
        shannon = 0.0

    return {
        "experiment": "exp_a_agentic_collapse",
        "date": datetime.date.today().isoformat(),
        "total_records": total_records,
        "valid_weight_records": total_valid,
        "step_counts": step_counts,
        "total_cost_usd": round(total_cost, 4),
        "models": list(set(r["model_id"] for r in records)),
        "hypotheses": {
            "H1_monotonic_dci": h1_result,
            "H2_dimension_specific": h2_result,
            "H3_ideological_protection": h3_result,
        },
        "secondary": {
            "dim_trajectories": dim_trajectories,
            "model_comparison": model_comparison,
        },
        "exploratory": {
            "retrieval_overlap": retrieval_overlap,
            "recommendation_convergence": {
                "counts": dict(rec_counts),
                "shannon_entropy": round(shannon, 3),
                "max_entropy": round(
                    float(np.log2(max(len(rec_counts), 1))), 3
                ),
            },
        },
    }


def write_summary(results: dict, summary_path: Path) -> None:
    """Write human-readable summary markdown."""
    h1 = results["hypotheses"]["H1_monotonic_dci"]
    h2 = results["hypotheses"]["H2_dimension_specific"]
    h3 = results["hypotheses"]["H3_ideological_protection"]

    lines = [
        "# Experiment A: Multi-Step Agentic Collapse -- Summary",
        "",
        f"**Date**: {results.get('date', '2026-04-16')}",
        f"**Total records**: {results['total_records']}",
        f"**Valid weight records**: {results['valid_weight_records']}",
        f"**Total cost**: ${results['total_cost_usd']:.2f}",
        "",
        "## Step Counts",
        "",
        "| Step | Records |",
        "|------|---------|",
    ]
    for s, n in sorted(results["step_counts"].items(), key=lambda x: int(x[0])):
        label = {0: "Control", 1: "Retrieval", 2: "Comparison", 3: "Recommendation"}.get(
            int(s), f"Step {s}"
        )
        lines.append(f"| {label} | {n} |")

    lines.extend([
        "",
        "## Hypothesis Results",
        "",
        f"### H1: Monotonic DCI Increase -- {'SUPPORTED' if h1.get('supported') else 'NOT SUPPORTED'}",
        "",
    ])

    if "f_stat" in h1:
        lines.extend([
            f"F = {h1['f_stat']}, p = {h1['p']}, eta-sq = {h1['eta_sq']} "
            f"(95% CI [{h1['eta_sq_ci_95'][0]}, {h1['eta_sq_ci_95'][1]}])",
            f"Monotonic trend: {h1['monotonic']}",
            "",
            "**Step means (DCI)**:",
            "",
            "| Step | Mean DCI |",
            "|------|----------|",
        ])
        for s, m in sorted(h1.get("step_means", {}).items()):
            lines.append(f"| {s} | {m} |")

        if h1.get("pairwise"):
            lines.extend(["", "**Pairwise comparisons (Bonferroni-corrected)**:", ""])
            lines.append("| Comparison | t | p | p_Bonf | Cohen's d | Sig |")
            lines.append("|------------|---|---|--------|-----------|-----|")
            for comp, vals in h1["pairwise"].items():
                sig = "Yes" if vals["significant"] else "No"
                lines.append(
                    f"| {comp} | {vals['t']} | {vals['p']} | "
                    f"{vals['p_bonferroni']} | {vals['cohens_d']} | {sig} |"
                )

    lines.extend([
        "",
        f"### H2: Dimension-Specific Compounding -- "
        f"{'SUPPORTED' if h2.get('supported') else 'NOT SUPPORTED'}",
        "",
    ])
    if "collapse_rates" in h2:
        lines.append("**Collapse rates (step 3 mean - control mean)**:")
        lines.append("")
        lines.append("| Dimension | Collapse Rate |")
        lines.append("|-----------|---------------|")
        for dim, rate in h2["collapse_rates"].items():
            lines.append(f"| {dim} | {rate} |")
        lines.append("")
        lines.append(
            f"Cultural collapsed more than Economic: {h2.get('cultural_collapsed_more')}"
        )
        lines.append(
            f"Temporal collapsed more than Economic: {h2.get('temporal_collapsed_more')}"
        )

    lines.extend([
        "",
        f"### H3: Ideological Signal Protection -- "
        f"{'SUPPORTED' if h3.get('supported') else 'NOT SUPPORTED'}",
        "",
    ])
    if "t" in h3:
        lines.extend([
            f"t = {h3['t']}, p = {h3['p']}, Cohen's d = {h3['cohens_d']} "
            f"(95% CI [{h3['cohens_d_ci_95'][0]}, {h3['cohens_d_ci_95'][1]}])",
            f"Strong Ideological (Patagonia) mean compound rate: "
            f"{h3['strong_ideo_mean']} (n={h3['strong_ideo_n']})",
            f"Weak Ideological (Erewhon, Tesla) mean compound rate: "
            f"{h3['weak_ideo_mean']} (n={h3['weak_ideo_n']})",
        ])

    # Dimension trajectories
    lines.extend(["", "## Per-Dimension Trajectories", ""])
    traj = results["secondary"]["dim_trajectories"]
    lines.append("| Dimension | Control | Step 2 | Step 3 | Delta (S3-Ctrl) |")
    lines.append("|-----------|---------|--------|--------|-----------------|")
    for dim in DIMENSIONS:
        ctrl = traj.get(dim, {}).get("step_0", {}).get("mean", "-")
        s2 = traj.get(dim, {}).get("step_2", {}).get("mean", "-")
        s3 = traj.get(dim, {}).get("step_3", {}).get("mean", "-")
        if isinstance(ctrl, (int, float)) and isinstance(s3, (int, float)):
            delta = round(s3 - ctrl, 3)
        else:
            delta = "-"
        lines.append(f"| {dim} | {ctrl} | {s2} | {s3} | {delta} |")

    # Model comparison
    mc = results["secondary"]["model_comparison"]
    lines.extend(["", "## Model Comparison", ""])
    lines.append("| Model | Mean Compound | Std | n |")
    lines.append("|-------|--------------|-----|---|")
    for model, vals in mc.items():
        if isinstance(vals, dict) and "mean_compound" in vals:
            lines.append(
                f"| {model} | {vals['mean_compound']} | {vals['std']} | {vals['n']} |"
            )
    if "anova_f" in mc:
        lines.append(f"\nModel ANOVA: F = {mc['anova_f']}, p = {mc['anova_p']}")

    # Exploratory
    lines.extend(["", "## Exploratory: Retrieval Overlap", ""])
    ro = results["exploratory"]["retrieval_overlap"]
    lines.append("| Brand | Included in Step 1 | Total | Rate |")
    lines.append("|-------|--------------------|-------|------|")
    for brand, vals in ro.items():
        lines.append(
            f"| {brand} | {vals['included']} | {vals['total']} | {vals['rate']} |"
        )

    rc = results["exploratory"]["recommendation_convergence"]
    lines.extend([
        "",
        "## Exploratory: Recommendation Convergence",
        "",
        f"Shannon entropy: {rc['shannon_entropy']} (max: {rc['max_entropy']})",
        "",
    ])
    if rc.get("counts"):
        lines.append("| Recommended Brand | Count |")
        lines.append("|-------------------|-------|")
        for brand, count in sorted(rc["counts"].items(), key=lambda x: -x[1]):
            lines.append(f"| {brand} | {count} |")

    lines.extend([
        "",
        "---",
        "*Analysis script: L4_analysis/exp_agentic_collapse_analysis.py*",
        "*Protocol: L0_specification/EXP_AGENTIC_COLLAPSE_PROTOCOL.md*",
    ])

    summary_path.write_text("\n".join(lines) + "\n")


def main():
    base = Path(__file__).parent.parent
    jsonl_path = base / "L3_sessions" / "exp_agentic_collapse.jsonl"
    results_path = base / "L4_analysis" / "exp_agentic_collapse_results.json"
    summary_path = base / "L4_analysis" / "exp_agentic_collapse_summary.md"

    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found. Run the experiment first.")
        sys.exit(1)

    print("Analyzing Experiment A: Multi-Step Agentic Collapse...")
    results = analyze(jsonl_path)

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results: {results_path}")

    write_summary(results, summary_path)
    print(f"Summary: {summary_path}")

    h1 = results["hypotheses"]["H1_monotonic_dci"]
    h2 = results["hypotheses"]["H2_dimension_specific"]
    h3 = results["hypotheses"]["H3_ideological_protection"]
    print(f"\nH1 (Monotonic DCI): {'SUPPORTED' if h1.get('supported') else 'NOT SUPPORTED'}")
    print(f"H2 (Dim-specific): {'SUPPORTED' if h2.get('supported') else 'NOT SUPPORTED'}")
    print(f"H3 (Ideo protection): {'SUPPORTED' if h3.get('supported') else 'NOT SUPPORTED'}")
    print(f"\nTotal cost: ${results['total_cost_usd']:.2f}")


if __name__ == "__main__":
    main()
