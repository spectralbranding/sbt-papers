#!/usr/bin/env python3
"""Prompt sensitivity analysis for R15: stability of DCI across repetitions.

Each model-pair combination was administered 3 repetitions of the
weighted_recommendation prompt (run=1,2,3). This script assesses whether
the DCI results are stable across those repetitions using:

  1. Within-condition ICC (intraclass correlation) for DCI across runs 1-3.
     ICC(3,1) two-way mixed model, absolute agreement, single measures.
     Interpretation: ICC >= 0.75 = good; >= 0.90 = excellent.

  2. Mean within-condition SD of DCI: absolute variability across repetitions.

  3. Coefficient of variation (CV = SD/mean) per condition.

  4. Kruskal-Wallis test across runs 1, 2, 3 to detect systematic
     ordering effects (prompt fatigue, context drift).

  5. Per-model stability summary: which models are most vs. least stable.

Data: weighted_recommendation calls from run2_global.jsonl and
      run5_crosscultural.jsonl. Run field encodes the repetition (1, 2, 3).

Usage:
    python prompt_sensitivity.py

Requires: numpy, scipy, json, pathlib, collections
"""

import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Optional

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

L4_DIR = Path(__file__).parent
L3_DIR = L4_DIR.parent / "L3_sessions"

DIMENSIONS = [
    "semiotic", "narrative", "ideological", "experiential",
    "social", "economic", "cultural", "temporal",
]

# ICC thresholds (Koo & Mae 2016 guidelines)
ICC_POOR = 0.50
ICC_MODERATE = 0.75
ICC_GOOD = 0.90

JSONL_FILES = [
    "run2_global.jsonl",
    "run5_crosscultural.jsonl",
]


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def parse_weights(parsed: dict) -> Optional[dict]:
    """Extract and validate dimensional weights from a parsed JSON response."""
    if not parsed or not isinstance(parsed, dict):
        return None
    weights = parsed.get("weights")
    if not weights or not isinstance(weights, dict):
        return None
    result = {}
    for dim in DIMENSIONS:
        v = weights.get(dim)
        if v is None:
            return None
        try:
            result[dim] = float(v)
        except (ValueError, TypeError):
            return None
    total = sum(result.values())
    if total < 10:
        return None
    # Renormalize to sum to 100
    return {d: v * 100.0 / total for d, v in result.items()}


def compute_dci(weights: dict) -> float:
    """DCI = (economic + semiotic) / sum(all weights)."""
    total = sum(weights.values())
    if total == 0:
        return 0.0
    return (weights.get("economic", 0) + weights.get("semiotic", 0)) / total


def load_weighted_rec_calls() -> list[dict]:
    """Load all weighted_recommendation calls with valid parsed weights."""
    calls = []
    for fname in JSONL_FILES:
        fpath = L3_DIR / fname
        if not fpath.exists():
            continue
        with fpath.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    c = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if c.get("prompt_type") != "weighted_recommendation":
                    continue
                if c.get("error"):
                    continue
                weights = parse_weights(c.get("parsed") or {})
                if weights is None:
                    continue
                c["_weights"] = weights
                c["_dci"] = compute_dci(weights)
                calls.append(c)
    return calls


# ---------------------------------------------------------------------------
# ICC calculation: ICC(3,1) two-way mixed, absolute agreement, single measures
# ---------------------------------------------------------------------------

def compute_icc_31(data_matrix: np.ndarray) -> dict:
    """Compute ICC(3,1): two-way mixed, absolute agreement, single measures.

    Parameters
    ----------
    data_matrix : np.ndarray, shape (n_subjects, n_raters)
        Each row is one subject (model x pair condition).
        Each column is one rater (repetition 1, 2, 3).
        Missing data not supported; rows with any NaN are dropped.

    Returns
    -------
    dict with keys: icc, f_stat, p_value, df_between, df_within, df_error,
                    ms_between, ms_within, ms_error, n_subjects, n_raters,
                    ci_lower, ci_upper (95% CI via F-distribution).
    """
    # Drop rows with NaN
    mask = ~np.isnan(data_matrix).any(axis=1)
    data = data_matrix[mask]

    n, k = data.shape  # subjects, raters
    if n < 2 or k < 2:
        return {"icc": float("nan"), "n_subjects": n, "n_raters": k,
                "error": "insufficient data"}

    grand_mean = data.mean()
    row_means = data.mean(axis=1)
    col_means = data.mean(axis=0)

    # Sum of squares
    ss_total = np.sum((data - grand_mean) ** 2)
    ss_between = k * np.sum((row_means - grand_mean) ** 2)
    ss_within = np.sum((data - row_means[:, np.newaxis]) ** 2)
    ss_rater = n * np.sum((col_means - grand_mean) ** 2)
    ss_error = ss_within - ss_rater

    df_between = n - 1
    df_rater = k - 1
    df_error = (n - 1) * (k - 1)

    ms_between = ss_between / df_between if df_between > 0 else 0.0
    ms_error = ss_error / df_error if df_error > 0 else 0.0

    if ms_error == 0:
        icc = 1.0
        f_stat = float("inf")
        p_value = 0.0
    else:
        icc = (ms_between - ms_error) / (ms_between + (k - 1) * ms_error)
        f_stat = ms_between / ms_error
        p_value = float(stats.f.sf(f_stat, df_between, df_error))

    # 95% CI via Shrout & Fleiss (1979) formula
    alpha_ci = 0.05
    f_lower = f_stat / stats.f.ppf(1 - alpha_ci / 2, df_between, df_error)
    f_upper = f_stat * stats.f.ppf(1 - alpha_ci / 2, df_error, df_between)
    ci_lower = (f_lower - 1) / (f_lower + k - 1)
    ci_upper = (f_upper - 1) / (f_upper + k - 1)

    return {
        "icc": float(icc),
        "f_stat": float(f_stat),
        "p_value": float(p_value),
        "df_between": int(df_between),
        "df_error": int(df_error),
        "ms_between": float(ms_between),
        "ms_error": float(ms_error),
        "n_subjects": int(n),
        "n_raters": int(k),
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
    }


def icc_interpretation(icc: float) -> str:
    """Classify ICC value per Koo & Mae (2016) guidelines."""
    if math.isnan(icc):
        return "N/A"
    if icc < ICC_POOR:
        return "poor (<0.50)"
    if icc < ICC_MODERATE:
        return "moderate (0.50-0.75)"
    if icc < ICC_GOOD:
        return "good (0.75-0.90)"
    return "excellent (>=0.90)"


# ---------------------------------------------------------------------------
# Main analyses
# ---------------------------------------------------------------------------

def build_condition_matrix(calls: list[dict]) -> tuple[np.ndarray, list[str]]:
    """Build (n_conditions x n_runs) DCI matrix for ICC.

    A condition is a (model, pair_id) combination.
    Runs are repetitions 1, 2, 3.

    Returns
    -------
    matrix : np.ndarray, shape (n_conditions, 3)
        DCI values; NaN where a repetition is missing.
    labels : list[str]
        Condition labels: 'model|pair_id'.
    """
    # Group DCI by (model, pair_id, run)
    data = defaultdict(dict)  # (model, pair_id) -> {run: dci}
    for c in calls:
        key = (c.get("model", ""), c.get("pair_id", ""))
        run = c.get("run")
        if run in (1, 2, 3):
            if run not in data[key]:
                data[key][run] = []
            data[key][run].append(c["_dci"])

    # Build matrix: use mean DCI per (condition, run) in case of duplicates
    labels = sorted(data.keys())
    matrix = np.full((len(labels), 3), fill_value=np.nan)
    for i, key in enumerate(labels):
        for run_idx, run in enumerate([1, 2, 3]):
            if run in data[key] and data[key][run]:
                matrix[i, run_idx] = float(np.mean(data[key][run]))

    label_strs = [f"{m}|{p}" for m, p in labels]
    return matrix, label_strs


def per_model_stability(calls: list[dict]) -> dict:
    """Compute per-model ICC and within-SD for DCI across repetitions."""
    by_model = defaultdict(list)
    for c in calls:
        by_model[c.get("model", "")].append(c)

    results = {}
    for model, model_calls in by_model.items():
        matrix, _ = build_condition_matrix(model_calls)
        # Only use rows where all 3 runs present
        complete = matrix[~np.isnan(matrix).any(axis=1)]
        if len(complete) < 3:
            results[model] = {
                "n_complete_conditions": len(complete),
                "icc": float("nan"),
                "icc_interp": "insufficient data",
                "within_sd_mean": float("nan"),
                "cv_mean": float("nan"),
            }
            continue

        icc_result = compute_icc_31(complete)
        icc_val = icc_result["icc"]

        # Within-condition SDs and CVs
        within_sds = np.std(complete, axis=1, ddof=1)
        row_means = np.mean(complete, axis=1)
        cvs = within_sds / row_means
        cvs = cvs[row_means > 0]

        results[model] = {
            "n_complete_conditions": len(complete),
            "icc": round(icc_val, 4),
            "icc_interp": icc_interpretation(icc_val),
            "within_sd_mean": round(float(np.mean(within_sds)), 4),
            "cv_mean": round(float(np.mean(cvs)) if len(cvs) > 0 else float("nan"), 4),
        }

    return results


def test_run_order_effect(calls: list[dict]) -> dict:
    """Kruskal-Wallis test for DCI differences across runs 1, 2, 3.

    Tests whether there is a systematic ordering effect (e.g., models
    give different DCI on run 3 than run 1).
    """
    by_run = defaultdict(list)
    for c in calls:
        run = c.get("run")
        if run in (1, 2, 3):
            by_run[run].append(c["_dci"])

    if len(by_run) < 2:
        return {"supported": False, "reason": "insufficient run variation"}

    groups = [by_run.get(r, []) for r in [1, 2, 3] if by_run.get(r)]
    if len(groups) < 2 or any(len(g) < 3 for g in groups):
        return {"supported": False, "reason": "insufficient data per run"}

    h_stat, p_value = stats.kruskal(*groups)

    run_means = {r: round(float(np.mean(by_run[r])), 4) for r in [1, 2, 3] if r in by_run}
    run_ns = {r: len(by_run[r]) for r in [1, 2, 3] if r in by_run}

    return {
        "h_stat": round(float(h_stat), 4),
        "p_value": float(p_value),
        "run_means": run_means,
        "run_ns": run_ns,
        "ordering_effect_present": p_value < 0.05,
        "interpretation": (
            "No significant run-order effect detected. DCI is stable "
            "across the 3 repetitions."
            if p_value >= 0.05 else
            "Significant run-order effect detected (p<0.05). "
            "Results may be sensitive to prompt context drift."
        ),
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_separator(char: str = "-", width: int = 70) -> None:
    print(char * width)


def main() -> None:
    """Run prompt sensitivity analysis."""
    print("=" * 70)
    print("R15 PROMPT SENSITIVITY ANALYSIS")
    print("Stability of DCI across 3 repetitions per condition")
    print("=" * 70)

    calls = load_weighted_rec_calls()
    if not calls:
        print("ERROR: No valid weighted_recommendation calls found.")
        print(f"Expected JSONL files in: {L3_DIR}")
        return

    n_total = len(calls)
    n_models = len(set(c.get("model") for c in calls))
    n_pairs = len(set(c.get("pair_id") for c in calls))
    print(f"\nLoaded {n_total} valid weighted_recommendation calls")
    print(f"Models: {n_models}, Brand pairs: {n_pairs}")

    # ----- 1. Global ICC across all conditions -----
    print_separator()
    print("1. GLOBAL ICC (all models x all brand pairs)")
    print_separator()

    matrix, labels = build_condition_matrix(calls)
    complete_mask = ~np.isnan(matrix).any(axis=1)
    complete_matrix = matrix[complete_mask]

    print(f"Total conditions (model x pair): {len(labels)}")
    print(f"Conditions with all 3 repetitions: {len(complete_matrix)}")
    print(f"Conditions with missing repetitions: {len(labels) - len(complete_matrix)}")

    if len(complete_matrix) >= 2:
        icc_result = compute_icc_31(complete_matrix)
        icc_val = icc_result["icc"]
        print(f"\nICC(3,1) = {icc_val:.4f}  [{icc_result['ci_lower']:.4f}, {icc_result['ci_upper']:.4f}]")
        print(f"Interpretation: {icc_interpretation(icc_val)}")
        print(f"F({icc_result['df_between']}, {icc_result['df_error']}) = {icc_result['f_stat']:.3f}, p = {icc_result['p_value']:.4e}")

        # Within-condition variability
        within_sds = np.std(complete_matrix, axis=1, ddof=1)
        row_means = np.mean(complete_matrix, axis=1)
        cvs = within_sds[row_means > 0] / row_means[row_means > 0]

        print(f"\nMean within-condition SD of DCI: {np.mean(within_sds):.4f}")
        print(f"Median within-condition SD: {np.median(within_sds):.4f}")
        print(f"Max within-condition SD: {np.max(within_sds):.4f}")
        print(f"Mean coefficient of variation: {np.mean(cvs):.4f}")
        print(f"Fraction of conditions with SD < 0.02: "
              f"{np.mean(within_sds < 0.02):.2%}")
        print(f"Fraction of conditions with SD > 0.05: "
              f"{np.mean(within_sds > 0.05):.2%}")
    else:
        print("Insufficient complete conditions for ICC.")

    # ----- 2. Run-order effect test -----
    print_separator()
    print("2. RUN-ORDER EFFECT TEST (Kruskal-Wallis across runs 1, 2, 3)")
    print_separator()

    order_result = test_run_order_effect(calls)
    for k, v in order_result.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}")
        else:
            print(f"  {k}: {v}")

    # ----- 3. Per-model stability -----
    print_separator()
    print("3. PER-MODEL STABILITY")
    print_separator()

    model_stability = per_model_stability(calls)
    sorted_models = sorted(
        model_stability.items(),
        key=lambda x: x[1].get("icc", -1) if not math.isnan(x[1].get("icc", float("nan"))) else -1,
        reverse=True,
    )

    print(f"\n{'Model':<22} {'n_cond':>6} {'ICC':>7} {'within_SD':>10} {'CV':>8} {'Stability'}")
    print("-" * 70)
    for model, res in sorted_models:
        icc_str = f"{res['icc']:.4f}" if not math.isnan(res["icc"]) else "  N/A"
        sd_str = f"{res['within_sd_mean']:.4f}" if not math.isnan(res.get("within_sd_mean", float("nan"))) else "  N/A"
        cv_str = f"{res['cv_mean']:.4f}" if not math.isnan(res.get("cv_mean", float("nan"))) else "  N/A"
        print(f"{model:<22} {res['n_complete_conditions']:>6} {icc_str:>7} {sd_str:>10} {cv_str:>8}  {res['icc_interp']}")

    # ----- 4. Per-dimension stability -----
    print_separator()
    print("4. PER-DIMENSION WEIGHT STABILITY")
    print_separator()

    # Build (n_conditions x 3) matrix for each dimension weight
    dim_stability = {}
    for dim in DIMENSIONS:
        by_cond = defaultdict(dict)
        for c in calls:
            key = (c.get("model", ""), c.get("pair_id", ""))
            run = c.get("run")
            if run in (1, 2, 3):
                by_cond[key][run] = c["_weights"][dim]

        keys = sorted(by_cond.keys())
        mat = np.full((len(keys), 3), fill_value=np.nan)
        for i, key in enumerate(keys):
            for ri, r in enumerate([1, 2, 3]):
                if r in by_cond[key]:
                    mat[i, ri] = by_cond[key][r]

        complete = mat[~np.isnan(mat).any(axis=1)]
        if len(complete) < 3:
            dim_stability[dim] = {"icc": float("nan"), "within_sd": float("nan")}
            continue

        icc_r = compute_icc_31(complete)
        within_sds = np.std(complete, axis=1, ddof=1)
        dim_stability[dim] = {
            "icc": round(icc_r["icc"], 4),
            "within_sd": round(float(np.mean(within_sds)), 4),
        }

    print(f"\n{'Dimension':<16} {'ICC':>7} {'within_SD':>10} {'Stability'}")
    print("-" * 50)
    for dim in DIMENSIONS:
        res = dim_stability[dim]
        icc_str = f"{res['icc']:.4f}" if not math.isnan(res["icc"]) else "  N/A"
        sd_str = f"{res['within_sd']:.4f}" if not math.isnan(res["within_sd"]) else "  N/A"
        interp = icc_interpretation(res["icc"])
        print(f"{dim:<16} {icc_str:>7} {sd_str:>10}  {interp}")

    # ----- 5. Summary verdict -----
    print_separator("=")
    print("SUMMARY VERDICT")
    print_separator()

    icc_global = icc_result["icc"] if len(complete_matrix) >= 2 else float("nan")
    order_p = order_result.get("p_value", 1.0)

    print(f"Global ICC(3,1) = {icc_global:.4f}  ({icc_interpretation(icc_global)})")
    print(f"Run-order effect: {'PRESENT (p<0.05)' if order_p < 0.05 else 'NOT DETECTED (p>=0.05)'}")
    print()

    if not math.isnan(icc_global) and icc_global >= ICC_MODERATE and order_p >= 0.05:
        verdict = "STABLE"
        verdict_msg = (
            "Results are STABLE across prompt repetitions. ICC >= 0.75 and no "
            "run-order effect. The 3-repetition design provides reliable DCI "
            "estimates. Averaging across repetitions is justified."
        )
    elif not math.isnan(icc_global) and icc_global >= ICC_POOR:
        verdict = "MODERATE"
        verdict_msg = (
            "Results show MODERATE stability. ICC >= 0.50. Some within-condition "
            "variance present. Main findings are robust but per-condition estimates "
            "should be interpreted with caution."
        )
    else:
        verdict = "LOW"
        verdict_msg = (
            "Results show LOW stability. ICC < 0.50 or significant run-order effect "
            "detected. Primary findings should be verified with additional repetitions."
        )
    print(f"CONCLUSION: {verdict_msg}")
    print()

    # Persist JSON results
    out_path = Path(__file__).resolve().parent / "prompt_sensitivity_results.json"
    payload = {
        "schema_version": "1.0",
        "n_calls": n_total,
        "n_models": n_models,
        "n_pairs": n_pairs,
        "global_icc": {
            "icc": float(icc_result["icc"]) if len(complete_matrix) >= 2 else None,
            "ci_lower": float(icc_result["ci_lower"]) if len(complete_matrix) >= 2 else None,
            "ci_upper": float(icc_result["ci_upper"]) if len(complete_matrix) >= 2 else None,
            "f_stat": float(icc_result["f_stat"]) if len(complete_matrix) >= 2 else None,
            "p_value": float(icc_result["p_value"]) if len(complete_matrix) >= 2 else None,
            "n_complete_conditions": int(len(complete_matrix)),
        },
        "run_order_effect": {k: (float(v) if isinstance(v, (int, float)) else v) for k, v in order_result.items()},
        "per_model": {
            m: {k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                for k, v in res.items()}
            for m, res in model_stability.items()
        },
        "per_dimension": dim_stability,
        "verdict": verdict,
        "verdict_message": verdict_msg,
    }
    out_path.write_text(json.dumps(payload, indent=2, default=float))
    print(f"Wrote: {out_path.name}")


if __name__ == "__main__":
    main()
