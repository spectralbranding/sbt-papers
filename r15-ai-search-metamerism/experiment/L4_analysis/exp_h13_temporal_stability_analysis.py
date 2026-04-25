#!/usr/bin/env python3
"""Analysis stub for Experiment H13: Temporal Stability Across Model Versions.

Reads exp_h13_temporal_stability.jsonl, tests H_13a-H_13d, and writes
results to exp_h13_temporal_stability_results.json plus a markdown summary.

Pre-registered analyses (from EXP_H13_TEMPORAL_STABILITY_PROTOCOL.md):
    H_13a: At least one pair has cosine(old, new) < .95
    H_13b: Economic and Semiotic are most stable (|delta| < 3)
    H_13c: Cultural and Temporal show most drift (top-2 |delta| in >= 2 pairs)
    H_13d: DCI does not decrease in newer versions

Usage:
    uv run python exp_h13_temporal_stability_analysis.py
    uv run python exp_h13_temporal_stability_analysis.py --jsonl path/to/file.jsonl
"""

import argparse
import datetime
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

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

MODEL_PAIRS = [
    ("deepseek_v3", "deepseek_r1", "deepseek"),
    ("llama31", "llama33", "llama"),
    ("qwen25", "qwen3", "qwen"),
    ("gemini20", "gemini25", "gemini"),
]


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------


def load_records(jsonl_path: Path) -> list[dict]:
    """Load all valid records from JSONL."""
    records = []
    with open(jsonl_path) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  Warning: line {lineno} invalid JSON ({e}), skipping")
                continue
            records.append(rec)
    return records


def renormalize(weights: dict) -> dict:
    """Renormalize weight dict to sum to 100."""
    total = sum(weights.values())
    if total == 0:
        return dict(weights)
    factor = 100.0 / total
    return {k: round(v * factor, 4) for k, v in weights.items()}


def compute_dci(weights: dict) -> float:
    """DCI = (Economic + Semiotic) after renormalization to 100."""
    w = renormalize(weights)
    return w.get("Economic", 0.0) + w.get("Semiotic", 0.0)


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Cosine similarity between two vectors."""
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)
    if denom == 0:
        return 0.0
    return float(np.dot(v1, v2) / denom)


def bootstrap_mean_ci(
    data: np.ndarray,
    n_boot: int = BOOTSTRAP_N,
    ci: float = 0.95,
    seed: int = RANDOM_SEED,
) -> tuple[float, float]:
    """Bootstrap 95% CI for the mean."""
    rng = np.random.RandomState(seed)
    boot = np.array(
        [
            np.mean(rng.choice(data, size=len(data), replace=True))
            for _ in range(n_boot)
        ]
    )
    alpha = (1 - ci) / 2
    return float(np.percentile(boot, 100 * alpha)), float(
        np.percentile(boot, 100 * (1 - alpha))
    )


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    """Cohen's d: pooled standard deviation."""
    n_a, n_b = len(a), len(b)
    if n_a < 2 or n_b < 2:
        return float("nan")
    pooled_sd = np.sqrt(
        ((n_a - 1) * np.var(a, ddof=1) + (n_b - 1) * np.var(b, ddof=1))
        / (n_a + n_b - 2)
    )
    if pooled_sd == 0:
        return 0.0
    return float((np.mean(a) - np.mean(b)) / pooled_sd)


# ---------------------------------------------------------------------------
# Data Preparation
# ---------------------------------------------------------------------------


def extract_weight_vector(record: dict) -> Optional[np.ndarray]:
    """Extract renormalized weight vector (8-dim) from record, or None."""
    weights = record.get("parsed_weights") or record.get("parsed")
    if not weights or not isinstance(weights, dict):
        return None
    if not all(d in weights for d in DIMENSIONS):
        return None
    w = renormalize(weights)
    return np.array([w[d] for d in DIMENSIONS])


def group_records_by_family(records: list[dict]) -> dict[str, dict[str, list]]:
    """Group records by model_family -> model_generation -> list of weight vectors.

    Returns: {family: {"old": [vec, ...], "new": [vec, ...]}}
    """
    groups: dict[str, dict[str, list]] = defaultdict(lambda: {"old": [], "new": []})
    excluded = 0
    for rec in records:
        if rec.get("error") and rec["error"] != "parse_failed":
            excluded += 1
            continue
        vec = extract_weight_vector(rec)
        if vec is None:
            excluded += 1
            continue
        family = rec.get("model_family", "unknown")
        gen = rec.get("model_generation", "unknown")
        if gen not in ("old", "new"):
            continue
        groups[family][gen].append(vec)
    if excluded:
        print(f"  Excluded {excluded} records (API errors or parse failures)")
    return groups


# ---------------------------------------------------------------------------
# H_13a: Cosine Similarity
# ---------------------------------------------------------------------------


def test_h13a(groups: dict, alpha_bonferroni: float = 0.0125) -> dict:
    """H_13a: At least one pair has cosine(old_mean, new_mean) < .95.

    Computes per-family cosine between mean old and mean new profiles.
    Tests H_13a with a one-sample t-test per pair (cosine < .95 threshold).
    """
    results = {}
    threshold = 0.95
    any_below = False

    for family in ["deepseek", "llama", "qwen", "gemini"]:
        old_vecs = groups.get(family, {}).get("old", [])
        new_vecs = groups.get(family, {}).get("new", [])

        if not old_vecs or not new_vecs:
            results[family] = {"status": "insufficient_data", "n_old": len(old_vecs), "n_new": len(new_vecs)}
            continue

        old_arr = np.array(old_vecs)   # shape (n, 8)
        new_arr = np.array(new_vecs)   # shape (n, 8)
        old_mean = old_arr.mean(axis=0)
        new_mean = new_arr.mean(axis=0)
        cosine = cosine_similarity(old_mean, new_mean)

        # Per-observation cosine similarities (paired where possible)
        n_min = min(len(old_vecs), len(new_vecs))
        per_obs_cosines = [
            cosine_similarity(old_vecs[i], new_vecs[i]) for i in range(n_min)
        ]
        per_obs = np.array(per_obs_cosines)
        ci_lo, ci_hi = bootstrap_mean_ci(per_obs)

        # One-sample t-test: mean cosine < .95 (one-sided, H_13a direction)
        t_stat, p_two = stats.ttest_1samp(per_obs, threshold)
        # One-sided p (testing cosine < threshold -> mean < threshold)
        p_one = p_two / 2 if t_stat < 0 else 1.0 - p_two / 2

        below = bool(cosine < threshold)
        if below:
            any_below = True

        results[family] = {
            "n_old": len(old_vecs),
            "n_new": len(new_vecs),
            "cosine_mean_profiles": round(cosine, 4),
            "per_obs_cosine_mean": round(float(per_obs.mean()), 4),
            "per_obs_cosine_ci_95": [round(ci_lo, 4), round(ci_hi, 4)],
            "t_stat": round(float(t_stat), 4),
            "p_one_sided": round(float(p_one), 4),
            "below_threshold": below,
        }

    supported = any_below
    results["_summary"] = {
        "hypothesis": "H_13a",
        "threshold": threshold,
        "alpha_bonferroni": alpha_bonferroni,
        "supported": supported,
        "interpretation": (
            "SUPPORTED: at least one model pair shows cosine < .95"
            if supported
            else "NOT SUPPORTED: all model pairs maintain cosine >= .95 across versions"
        ),
    }
    return results


# ---------------------------------------------------------------------------
# H_13b and H_13c: Per-Dimension Drift
# ---------------------------------------------------------------------------


def test_h13b_h13c(groups: dict, alpha_bonferroni: float = 0.006) -> dict:
    """H_13b/c: Economic+Semiotic stable; Cultural+Temporal show most drift.

    For each model family and each dimension, computes |delta| = |mean_new - mean_old|
    with a paired t-test (or independent if sample sizes differ).
    """
    results = {}

    for family in ["deepseek", "llama", "qwen", "gemini"]:
        old_vecs = groups.get(family, {}).get("old", [])
        new_vecs = groups.get(family, {}).get("new", [])

        if not old_vecs or not new_vecs:
            results[family] = {"status": "insufficient_data"}
            continue

        old_arr = np.array(old_vecs)
        new_arr = np.array(new_vecs)
        dim_results = {}

        for i, dim in enumerate(DIMENSIONS):
            old_dim = old_arr[:, i]
            new_dim = new_arr[:, i]
            delta = float(new_dim.mean() - old_dim.mean())
            abs_delta = abs(delta)

            n_min = min(len(old_dim), len(new_dim))
            if n_min >= 2 and len(old_dim) == len(new_dim):
                t_stat, p_val = stats.ttest_rel(new_dim, old_dim)
            elif n_min >= 2:
                t_stat, p_val = stats.ttest_ind(new_dim, old_dim)
            else:
                t_stat, p_val = float("nan"), float("nan")

            d = cohens_d(new_dim, old_dim)
            significant = bool(p_val < alpha_bonferroni) if not np.isnan(p_val) else False

            dim_results[dim] = {
                "old_mean": round(float(old_dim.mean()), 3),
                "new_mean": round(float(new_dim.mean()), 3),
                "delta": round(delta, 3),
                "abs_delta": round(abs_delta, 3),
                "cohens_d": round(d, 3) if not np.isnan(d) else None,
                "t_stat": round(float(t_stat), 4) if not np.isnan(t_stat) else None,
                "p_val": round(float(p_val), 4) if not np.isnan(p_val) else None,
                "significant_bonferroni": significant,
            }

        # Rank dimensions by |delta|
        ranked = sorted(
            DIMENSIONS, key=lambda d: dim_results[d]["abs_delta"], reverse=True
        )

        results[family] = {
            "dimensions": dim_results,
            "ranking_by_abs_delta": ranked,
            "economic_abs_delta": dim_results["Economic"]["abs_delta"],
            "semiotic_abs_delta": dim_results["Semiotic"]["abs_delta"],
            "cultural_abs_delta": dim_results["Cultural"]["abs_delta"],
            "temporal_abs_delta": dim_results["Temporal"]["abs_delta"],
            "cultural_rank": ranked.index("Cultural") + 1,
            "temporal_rank": ranked.index("Temporal") + 1,
            "economic_rank": ranked.index("Economic") + 1,
            "semiotic_rank": ranked.index("Semiotic") + 1,
        }

    # Evaluate H_13b: Economic and Semiotic both have |delta| < 3
    # in at least 3 of 4 families
    h13b_families = []
    for family in ["deepseek", "llama", "qwen", "gemini"]:
        if "dimensions" not in results.get(family, {}):
            continue
        eco = results[family]["economic_abs_delta"]
        sem = results[family]["semiotic_abs_delta"]
        if eco < 3.0 and sem < 3.0:
            h13b_families.append(family)

    h13b_supported = len(h13b_families) >= 3

    # Evaluate H_13c: Cultural or Temporal in top-2 |delta| in >= 2 pairs
    h13c_families = []
    for family in ["deepseek", "llama", "qwen", "gemini"]:
        if "dimensions" not in results.get(family, {}):
            continue
        cult_rank = results[family]["cultural_rank"]
        temp_rank = results[family]["temporal_rank"]
        if cult_rank <= 2 or temp_rank <= 2:
            h13c_families.append(family)

    h13c_supported = len(h13c_families) >= 2

    results["_summary_h13b"] = {
        "hypothesis": "H_13b",
        "criterion": "Economic and Semiotic |delta| < 3 in >= 3 of 4 families",
        "families_meeting_criterion": h13b_families,
        "supported": h13b_supported,
        "interpretation": (
            "SUPPORTED: Economic and Semiotic are most stable"
            if h13b_supported
            else "NOT SUPPORTED: Economic or Semiotic show substantial drift"
        ),
    }
    results["_summary_h13c"] = {
        "hypothesis": "H_13c",
        "criterion": "Cultural or Temporal ranks top-2 by |delta| in >= 2 of 4 families",
        "families_meeting_criterion": h13c_families,
        "supported": h13c_supported,
        "interpretation": (
            "SUPPORTED: Cultural and/or Temporal show most drift"
            if h13c_supported
            else "NOT SUPPORTED: Cultural and Temporal not consistently highest drift"
        ),
    }
    return results


# ---------------------------------------------------------------------------
# H_13d: DCI Comparison
# ---------------------------------------------------------------------------


def test_h13d(groups: dict, alpha_bonferroni: float = 0.0125) -> dict:
    """H_13d: DCI does not decrease in newer versions (one-sided, DCI_new >= DCI_old).

    Paired t-test per family: DCI_new vs DCI_old.
    Success criterion: >= 3 of 4 pairs show non-significant decrease.
    """
    results = {}

    for family in ["deepseek", "llama", "qwen", "gemini"]:
        old_vecs = groups.get(family, {}).get("old", [])
        new_vecs = groups.get(family, {}).get("new", [])

        if not old_vecs or not new_vecs:
            results[family] = {"status": "insufficient_data"}
            continue

        old_dci = np.array([compute_dci(dict(zip(DIMENSIONS, v))) for v in old_vecs])
        new_dci = np.array([compute_dci(dict(zip(DIMENSIONS, v))) for v in new_vecs])

        delta_dci = float(new_dci.mean() - old_dci.mean())

        n_min = min(len(old_dci), len(new_dci))
        if n_min >= 2 and len(old_dci) == len(new_dci):
            t_stat, p_two = stats.ttest_rel(new_dci, old_dci)
        elif n_min >= 2:
            t_stat, p_two = stats.ttest_ind(new_dci, old_dci)
        else:
            t_stat, p_two = float("nan"), float("nan")

        # One-sided: DCI_new < DCI_old (decrease) -> t_stat < 0
        if not np.isnan(t_stat):
            p_decrease = p_two / 2 if t_stat < 0 else 1.0 - p_two / 2
        else:
            p_decrease = float("nan")

        d = cohens_d(new_dci, old_dci)

        # Significant decrease: p_decrease < alpha_bonferroni AND delta < 0
        sig_decrease = (
            bool(p_decrease < alpha_bonferroni and delta_dci < 0)
            if not np.isnan(p_decrease)
            else False
        )

        results[family] = {
            "n_old": len(old_dci),
            "n_new": len(new_dci),
            "old_dci_mean": round(float(old_dci.mean()), 3),
            "new_dci_mean": round(float(new_dci.mean()), 3),
            "delta_dci": round(delta_dci, 3),
            "cohens_d": round(d, 3) if not np.isnan(d) else None,
            "t_stat": round(float(t_stat), 4) if not np.isnan(t_stat) else None,
            "p_decrease_one_sided": (
                round(float(p_decrease), 4)
                if not np.isnan(p_decrease)
                else None
            ),
            "significant_decrease": sig_decrease,
        }

    # Count families without significant decrease
    no_sig_decrease = [
        fam
        for fam in ["deepseek", "llama", "qwen", "gemini"]
        if "significant_decrease" in results.get(fam, {})
        and not results[fam]["significant_decrease"]
    ]
    h13d_supported = len(no_sig_decrease) >= 3

    results["_summary"] = {
        "hypothesis": "H_13d",
        "criterion": "DCI_new >= DCI_old (no significant decrease) in >= 3 of 4 families",
        "families_no_significant_decrease": no_sig_decrease,
        "supported": h13d_supported,
        "interpretation": (
            "SUPPORTED: DCI does not significantly decrease in newer versions"
            if h13d_supported
            else "NOT SUPPORTED: DCI decreases significantly in >= 2 families"
        ),
    }
    return results


# ---------------------------------------------------------------------------
# Secondary: Aggregate Drift Summary
# ---------------------------------------------------------------------------


def compute_aggregate_drift(groups: dict) -> dict:
    """Compute mean |delta| across all dimensions per family.

    Used to rank families by total drift (secondary analysis 9).
    """
    summary = {}
    for family in ["deepseek", "llama", "qwen", "gemini"]:
        old_vecs = groups.get(family, {}).get("old", [])
        new_vecs = groups.get(family, {}).get("new", [])
        if not old_vecs or not new_vecs:
            summary[family] = {"status": "insufficient_data"}
            continue
        old_mean = np.array(old_vecs).mean(axis=0)
        new_mean = np.array(new_vecs).mean(axis=0)
        abs_deltas = np.abs(new_mean - old_mean)
        summary[family] = {
            "mean_abs_delta_all_dims": round(float(abs_deltas.mean()), 3),
            "max_abs_delta": round(float(abs_deltas.max()), 3),
            "sum_abs_delta": round(float(abs_deltas.sum()), 3),
        }
    families_with_data = [
        f for f in ["deepseek", "llama", "qwen", "gemini"]
        if summary.get(f, {}).get("mean_abs_delta_all_dims") is not None
    ]
    ranking = sorted(
        families_with_data,
        key=lambda f: summary[f]["mean_abs_delta_all_dims"],
        reverse=True,
    )
    summary["_ranking_by_total_drift"] = ranking
    return summary


# ---------------------------------------------------------------------------
# Summary Report
# ---------------------------------------------------------------------------


def build_summary_md(results: dict, n_records: int, n_valid: int) -> str:
    """Build a markdown summary of the analysis results."""
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# Experiment H13: Temporal Stability -- Analysis Summary",
        "",
        f"Generated: {now}",
        f"Records loaded: {n_records} ({n_valid} valid weight-bearing)",
        "",
        "## Pre-Registered Hypotheses",
        "",
    ]

    # H_13a
    h13a = results.get("h13a", {})
    h13a_summary = h13a.get("_summary", {})
    lines += [
        "### H_13a: Version Drift Exists (cosine < .95 in >= 1 pair)",
        "",
        f"**Supported**: {h13a_summary.get('supported', 'N/A')}",
        "",
        f"_{h13a_summary.get('interpretation', '')}_",
        "",
        "| Family | n_old | n_new | Cosine (mean profiles) | Per-obs cosine mean [95% CI] | Below .95 |",
        "|--------|-------|-------|------------------------|------------------------------|-----------|",
    ]
    for family in ["deepseek", "llama", "qwen", "gemini"]:
        d = h13a.get(family, {})
        if d.get("status") == "insufficient_data":
            lines.append(f"| {family} | -- | -- | insufficient data | -- | -- |")
            continue
        ci = d.get("per_obs_cosine_ci_95", ["--", "--"])
        lines.append(
            f"| {family} | {d.get('n_old','--')} | {d.get('n_new','--')} "
            f"| {d.get('cosine_mean_profiles','--')} "
            f"| {d.get('per_obs_cosine_mean','--')} [{ci[0]}, {ci[1]}] "
            f"| {d.get('below_threshold','--')} |"
        )
    lines.append("")

    # H_13b / H_13c
    h13bc = results.get("h13b_h13c", {})
    h13b_sum = h13bc.get("_summary_h13b", {})
    h13c_sum = h13bc.get("_summary_h13c", {})
    lines += [
        "### H_13b: Economic and Semiotic Are Most Stable",
        "",
        f"**Supported**: {h13b_sum.get('supported', 'N/A')}",
        "",
        f"_{h13b_sum.get('interpretation', '')}_",
        "",
        "### H_13c: Cultural and Temporal Show Most Drift",
        "",
        f"**Supported**: {h13c_sum.get('supported', 'N/A')}",
        "",
        f"_{h13c_sum.get('interpretation', '')}_",
        "",
        "| Family | Econ |delta| | Sem |delta| | Cult |delta| | Temp |delta| | Cult rank | Temp rank |",
        "|--------|-------------|------------|-------------|-------------|-----------|-----------|",
    ]
    for family in ["deepseek", "llama", "qwen", "gemini"]:
        d = h13bc.get(family, {})
        if "dimensions" not in d:
            lines.append(f"| {family} | insufficient data | | | | | |")
            continue
        lines.append(
            f"| {family} "
            f"| {d.get('economic_abs_delta','--')} "
            f"| {d.get('semiotic_abs_delta','--')} "
            f"| {d.get('cultural_abs_delta','--')} "
            f"| {d.get('temporal_abs_delta','--')} "
            f"| {d.get('cultural_rank','--')} "
            f"| {d.get('temporal_rank','--')} |"
        )
    lines.append("")

    # H_13d
    h13d = results.get("h13d", {})
    h13d_sum = h13d.get("_summary", {})
    lines += [
        "### H_13d: DCI Does Not Decrease in Newer Versions",
        "",
        f"**Supported**: {h13d_sum.get('supported', 'N/A')}",
        "",
        f"_{h13d_sum.get('interpretation', '')}_",
        "",
        "| Family | DCI old | DCI new | delta DCI | Cohen's d | p (decrease, one-sided) | Sig. decrease |",
        "|--------|---------|---------|-----------|-----------|-------------------------|---------------|",
    ]
    for family in ["deepseek", "llama", "qwen", "gemini"]:
        d = h13d.get(family, {})
        if d.get("status") == "insufficient_data":
            lines.append(f"| {family} | insufficient data | | | | | |")
            continue
        lines.append(
            f"| {family} "
            f"| {d.get('old_dci_mean','--')} "
            f"| {d.get('new_dci_mean','--')} "
            f"| {d.get('delta_dci','--')} "
            f"| {d.get('cohens_d','--')} "
            f"| {d.get('p_decrease_one_sided','--')} "
            f"| {d.get('significant_decrease','--')} |"
        )
    lines.append("")

    # Aggregate drift
    agg = results.get("aggregate_drift", {})
    ranking = agg.get("_ranking_by_total_drift", [])
    lines += [
        "## Secondary: Total Drift Ranking by Family",
        "",
        "| Rank | Family | Mean |delta| (all dims) | Max |delta| |",
        "|------|--------|--------------------------|------------|",
    ]
    for rank, family in enumerate(ranking, 1):
        d = agg.get(family, {})
        lines.append(
            f"| {rank} | {family} "
            f"| {d.get('mean_abs_delta_all_dims','--')} "
            f"| {d.get('max_abs_delta','--')} |"
        )
    lines += [
        "",
        "---",
        "",
        "*Analysis pre-registered in EXP_H13_TEMPORAL_STABILITY_PROTOCOL.md.*",
        "*All exploratory analyses are labeled as such in the full results JSON.*",
    ]

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Experiment H13: Temporal Stability Analysis"
    )
    parser.add_argument(
        "--jsonl",
        type=str,
        default=None,
        help="Path to exp_h13_temporal_stability.jsonl (default: auto-discover)",
    )
    args = parser.parse_args()

    # Locate JSONL
    if args.jsonl:
        jsonl_path = Path(args.jsonl)
    else:
        here = Path(__file__).parent
        jsonl_path = here.parent / "L3_sessions" / "exp_h13_temporal_stability.jsonl"

    if not jsonl_path.exists():
        print(f"ERROR: JSONL not found: {jsonl_path}")
        print("Run the experiment first:")
        print("  uv run python L2_prompts/exp_h13_temporal_stability.py --live")
        sys.exit(1)

    print(f"Loading: {jsonl_path}")
    records = load_records(jsonl_path)
    n_records = len(records)
    print(f"Records loaded: {n_records}")

    # Filter to valid weight-bearing records
    valid_records = [
        r for r in records if r.get("weights_valid") or r.get("parsed_weights")
    ]
    n_valid = len(valid_records)
    print(f"Valid records: {n_valid}")

    if n_valid == 0:
        print("ERROR: No valid records found. Check JSONL contents.")
        sys.exit(1)

    # Group by family and generation
    groups = group_records_by_family(records)
    for family, gens in groups.items():
        print(
            f"  {family}: old={len(gens['old'])}, new={len(gens['new'])}"
        )

    print("\nRunning pre-registered analyses...")

    h13a_results = test_h13a(groups)
    h13bc_results = test_h13b_h13c(groups)
    h13d_results = test_h13d(groups)
    drift_results = compute_aggregate_drift(groups)

    results = {
        "meta": {
            "experiment": "exp_h13_temporal_stability",
            "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "n_records": n_records,
            "n_valid": n_valid,
            "jsonl_path": str(jsonl_path),
        },
        "h13a": h13a_results,
        "h13b_h13c": h13bc_results,
        "h13d": h13d_results,
        "aggregate_drift": drift_results,
    }

    # Write results JSON
    output_dir = Path(__file__).parent
    results_path = output_dir / "exp_h13_temporal_stability_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults written: {results_path}")

    # Write summary markdown
    summary_md = build_summary_md(results, n_records, n_valid)
    summary_path = output_dir / "exp_h13_temporal_stability_summary.md"
    with open(summary_path, "w") as f:
        f.write(summary_md)
    print(f"Summary written: {summary_path}")

    # Print key findings
    print("\n=== Key Findings ===")
    h13a_sum = h13a_results.get("_summary", {})
    h13b_sum = h13bc_results.get("_summary_h13b", {})
    h13c_sum = h13bc_results.get("_summary_h13c", {})
    h13d_sum = h13d_results.get("_summary", {})
    print(f"H_13a (version drift): {h13a_sum.get('interpretation', 'N/A')}")
    print(f"H_13b (Econ/Sem stable): {h13b_sum.get('interpretation', 'N/A')}")
    print(f"H_13c (Cult/Temp drift): {h13c_sum.get('interpretation', 'N/A')}")
    print(f"H_13d (DCI persistent): {h13d_sum.get('interpretation', 'N/A')}")


if __name__ == "__main__":
    main()
