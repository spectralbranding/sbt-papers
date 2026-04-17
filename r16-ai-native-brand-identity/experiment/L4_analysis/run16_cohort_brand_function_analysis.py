#!/usr/bin/env python3
"""Run 16: Brand Function x Cohort — Analysis.

Tests H1 (interaction), H2 (DCI range), H3 (Run 14 null replication).
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


def compute_dci(weights: dict) -> float:
    """DCI = (Economic + Semiotic weight) / total."""
    vec = weights_to_vector(weights)
    return float(vec[0] + vec[5])  # Semiotic + Economic


def test_h1(records: list[dict]) -> dict:
    """H1: Cohort x Condition interaction on DCI (2-way ANOVA approximation).

    Since scipy doesn't have 2-way ANOVA, we use a proxy:
    test whether the effect of condition on DCI varies across cohorts.
    """
    cohorts = sorted(set(r["cohort_id"] for r in records))
    conditions = sorted(set(r["condition"] for r in records))

    # Per-cohort DCI reduction from A to B
    reductions = {}
    for cohort in cohorts:
        for condition in conditions:
            subset = [
                r
                for r in records
                if r["cohort_id"] == cohort and r["condition"] == condition
            ]
            dcis = [compute_dci(r["parsed_weights"]) for r in subset]
            reductions[(cohort, condition)] = np.mean(dcis) if dcis else 0

    # Interaction test: does the B-A reduction differ across cohorts?
    cohort_reductions = []
    for cohort in cohorts:
        a_dci = reductions.get((cohort, "A_baseline"), 0)
        b_dci = reductions.get((cohort, "B_structural"), 0)
        cohort_reductions.append(a_dci - b_dci)

    # Per-cell DCI values for ANOVA-like analysis
    groups_by_cohort_condition = {}
    for r in records:
        key = (r["cohort_id"], r["condition"])
        groups_by_cohort_condition.setdefault(key, []).append(
            compute_dci(r["parsed_weights"])
        )

    # Test: does condition B affect cohorts differently?
    # Compare DCI under condition B across cohorts
    b_groups = []
    for cohort in cohorts:
        vals = groups_by_cohort_condition.get((cohort, "B_structural"), [])
        if vals:
            b_groups.append(np.array(vals))

    if len(b_groups) >= 2:
        f_stat, p_val = stats.f_oneway(*b_groups)
    else:
        f_stat, p_val = 0.0, 1.0

    # Eta-squared
    if b_groups and p_val < 1.0:
        all_vals = np.concatenate(b_groups)
        grand_mean = all_vals.mean()
        ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in b_groups)
        ss_total = np.sum((all_vals - grand_mean) ** 2)
        eta_sq = ss_between / ss_total if ss_total > 0 else 0
    else:
        eta_sq = 0

    return {
        "F": round(float(f_stat), 3),
        "p": round(float(p_val), 4),
        "partial_eta_sq": round(float(eta_sq), 4),
        "cohort_reductions_A_to_B": {
            c: round(r, 4) for c, r in zip(cohorts, cohort_reductions)
        },
        "h1_supported": p_val < 0.05 and eta_sq > 0.04,
    }


def test_h2(records: list[dict]) -> dict:
    """H2: DCI reduction range across cohorts."""
    cohorts = sorted(set(r["cohort_id"] for r in records))

    reductions = {}
    for cohort in cohorts:
        a_dcis = [
            compute_dci(r["parsed_weights"])
            for r in records
            if r["cohort_id"] == cohort and r["condition"] == "A_baseline"
        ]
        b_dcis = [
            compute_dci(r["parsed_weights"])
            for r in records
            if r["cohort_id"] == cohort and r["condition"] == "B_structural"
        ]
        a_mean = np.mean(a_dcis) if a_dcis else 0
        b_mean = np.mean(b_dcis) if b_dcis else 0
        reductions[cohort] = round(float(a_mean - b_mean) * 100, 2)

    vals = list(reductions.values())
    span = max(vals) - min(vals) if vals else 0

    return {
        "dci_reduction_pct_by_cohort": reductions,
        "range_pct": round(span, 2),
        "h2_supported": span >= 15,
    }


def test_h3(records: list[dict]) -> dict:
    """H3: Condition C does not outperform Condition B."""
    cohorts = sorted(set(r["cohort_id"] for r in records))

    results = {}
    for cohort in cohorts:
        b_dcis = [
            compute_dci(r["parsed_weights"])
            for r in records
            if r["cohort_id"] == cohort and r["condition"] == "B_structural"
        ]
        c_dcis = [
            compute_dci(r["parsed_weights"])
            for r in records
            if r["cohort_id"] == cohort and r["condition"] == "C_enriched"
        ]
        if len(b_dcis) >= 2 and len(c_dcis) >= 2:
            t_stat, p_val = stats.ttest_ind(b_dcis, c_dcis)
            pooled_std = np.sqrt(
                (
                    (len(b_dcis) - 1) * np.var(b_dcis, ddof=1)
                    + (len(c_dcis) - 1) * np.var(c_dcis, ddof=1)
                )
                / (len(b_dcis) + len(c_dcis) - 2)
            )
            d = (
                (np.mean(b_dcis) - np.mean(c_dcis)) / pooled_std
                if pooled_std > 0
                else 0
            )
        else:
            t_stat, p_val, d = 0.0, 1.0, 0.0

        results[cohort] = {
            "b_mean": round(float(np.mean(b_dcis)) if b_dcis else 0, 4),
            "c_mean": round(float(np.mean(c_dcis)) if c_dcis else 0, 4),
            "t": round(float(t_stat), 3),
            "p": round(float(p_val), 4),
            "cohens_d": round(float(d), 3),
            "c_outperforms_b": p_val < 0.05 and np.mean(c_dcis) < np.mean(b_dcis),
        }

    any_outperforms = any(r["c_outperforms_b"] for r in results.values())
    return {
        "per_cohort": results,
        "h3_confirmed": not any_outperforms,
    }


def main():
    data_dir = Path(__file__).parent.parent / "L3_sessions"
    jsonl_path = data_dir / "run16_cohort_brand_function.jsonl"

    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found.")
        sys.exit(1)

    records = load_data(jsonl_path)
    print(f"Loaded {len(records)} valid records")

    print("\n--- H1: Cohort x Condition Interaction ---")
    h1 = test_h1(records)
    print(f"  F = {h1['F']}, p = {h1['p']}, eta_sq = {h1['partial_eta_sq']}")
    print(f"  Cohort reductions: {h1['cohort_reductions_A_to_B']}")
    print(f"  H1 {'SUPPORTED' if h1['h1_supported'] else 'NOT SUPPORTED'}")

    print("\n--- H2: DCI Reduction Range ---")
    h2 = test_h2(records)
    print(f"  Per-cohort: {h2['dci_reduction_pct_by_cohort']}")
    print(f"  Range: {h2['range_pct']} pct points")
    print(f"  H2 {'SUPPORTED' if h2['h2_supported'] else 'NOT SUPPORTED'}")

    print("\n--- H3: C vs B (Run 14 Null Replication) ---")
    h3 = test_h3(records)
    for cid, r in h3["per_cohort"].items():
        print(
            f"  {cid}: B={r['b_mean']:.4f} C={r['c_mean']:.4f} "
            f"t={r['t']:.3f} p={r['p']:.4f} d={r['cohens_d']:.3f}"
        )
    print(f"  H3 {'CONFIRMED' if h3['h3_confirmed'] else 'NOT CONFIRMED'}")

    total_cost = sum(r.get("api_cost_usd", 0) for r in records)

    results = {
        "experiment": "exp2_brand_function_cohort",
        "date": "2026-04-16",
        "total_records": len(records),
        "total_cost_usd": round(total_cost, 4),
        "h1": h1,
        "h2": h2,
        "h3": h3,
    }

    results_path = Path(__file__).parent / "run16_cohort_brand_function_results.json"

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


if __name__ == "__main__":
    main()
