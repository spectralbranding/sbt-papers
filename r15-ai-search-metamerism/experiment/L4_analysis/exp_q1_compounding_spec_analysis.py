#!/usr/bin/env python3
"""Analysis script for Q1: Compounding x Structured Specification.

Reads exp_q1_compounding_spec.jsonl, runs pre-registered tests (H_Q1a-H_Q1c),
computes per-condition DCI trajectories, and produces results JSON + summary.

Pre-registered hypotheses:
  H_Q1a: DCI(step_3, constraint) < DCI(step_3, baseline)  -- d < -.80
  H_Q1b: DCI(step_3, constraint) < DCI(step_3, information)  -- d < -.50
  H_Q1c: DCI(control, constraint) < DCI(control, baseline)

Usage:
    uv run python exp_q1_compounding_spec_analysis.py
"""

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

CONDITIONS = ["baseline", "information", "constraint"]
PIPELINE_STAGES = ["control", "step_2", "step_3"]


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def load_data(jsonl_path: Path) -> list[dict]:
    """Load records from JSONL, skipping blank lines."""
    records = []
    with open(jsonl_path) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  WARNING: skipping malformed line {line_num}: {e}")
    return records


# ---------------------------------------------------------------------------
# DCI calculation
# ---------------------------------------------------------------------------


def renormalize(weights: dict) -> dict:
    """Renormalize weights to sum to 100."""
    total = sum(weights.values())
    if total == 0:
        return weights
    factor = 100.0 / total
    return {k: round(v * factor, 4) for k, v in weights.items()}


def compute_dci(weights: dict) -> float:
    """DCI = mean(|w_i - 12.5|) after renormalization.

    DCI = 0 indicates perfect uniform distribution.
    """
    w = renormalize(weights)
    return sum(abs(w.get(d, 0) - 12.5) for d in DIMENSIONS) / len(DIMENSIONS)


# ---------------------------------------------------------------------------
# Statistical helpers
# ---------------------------------------------------------------------------


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


def bootstrap_ci(
    data: np.ndarray,
    stat_fn=np.mean,
    n_boot: int = BOOTSTRAP_N,
    ci: float = 0.95,
    seed: int = RANDOM_SEED,
) -> tuple[float, float]:
    """Bootstrap percentile confidence interval."""
    rng = np.random.RandomState(seed)
    boot_stats = np.array(
        [stat_fn(rng.choice(data, size=len(data), replace=True)) for _ in range(n_boot)]
    )
    alpha = (1 - ci) / 2
    return (
        float(np.percentile(boot_stats, 100 * alpha)),
        float(np.percentile(boot_stats, 100 * (1 - alpha))),
    )


def eta_squared_oneway(groups: list[np.ndarray]) -> float:
    """Compute eta-squared from a list of group arrays."""
    all_data = np.concatenate(groups)
    grand_mean = np.mean(all_data)
    ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)
    ss_total = np.sum((all_data - grand_mean) ** 2)
    if ss_total == 0:
        return 0.0
    return float(ss_between / ss_total)


def welch_t(a: np.ndarray, b: np.ndarray) -> tuple[float, float, float]:
    """Welch two-sample t-test. Returns (t, df, p)."""
    result = stats.ttest_ind(a, b, equal_var=False)
    return float(result.statistic), float(result.df), float(result.pvalue)


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------


def analyze(jsonl_path: Path) -> dict:
    """Run all pre-registered and exploratory analyses.

    Returns a nested results dict suitable for JSON serialization.
    """
    records = load_data(jsonl_path)
    print(f"Loaded {len(records)} records from {jsonl_path.name}")

    # Filter to records with valid parsed weights
    valid = [
        r for r in records
        if r.get("weights_valid") and r.get("parsed_weights")
    ]
    print(f"Valid weight records: {len(valid)} / {len(records)}")

    # Re-compute DCI inline for all valid records (source of truth)
    for r in valid:
        r["_dci"] = compute_dci(r["parsed_weights"])

    # Separate by condition and stage
    by_cond_stage: dict[str, dict[str, list[float]]] = {
        cond: defaultdict(list) for cond in CONDITIONS
    }

    parse_by_cond: dict[str, dict] = {cond: {"valid": 0, "total": 0} for cond in CONDITIONS}

    for r in records:
        cond = r.get("bf_condition", "")
        step = r.get("step", -1)
        if cond not in CONDITIONS:
            continue

        parse_by_cond[cond]["total"] += 1 if step != 1 else 0  # step 1 has no weights

        if r.get("weights_valid") and r.get("parsed_weights"):
            dci = compute_dci(r["parsed_weights"])
            if step == 0:
                by_cond_stage[cond]["control"].append(dci)
                parse_by_cond[cond]["valid"] += 1
            elif step == 2:
                by_cond_stage[cond]["step_2"].append(dci)
                parse_by_cond[cond]["valid"] += 1
            elif step == 3:
                by_cond_stage[cond]["step_3"].append(dci)
                parse_by_cond[cond]["valid"] += 1

    # Descriptive statistics per condition x stage
    desc: dict[str, dict[str, dict]] = {}
    for cond in CONDITIONS:
        desc[cond] = {}
        for stage in PIPELINE_STAGES:
            vals = np.array(by_cond_stage[cond][stage])
            if len(vals) == 0:
                desc[cond][stage] = {"n": 0, "mean": None, "sd": None, "ci95": None}
                continue
            ci_lo, ci_hi = bootstrap_ci(vals)
            desc[cond][stage] = {
                "n": int(len(vals)),
                "mean": float(np.mean(vals)),
                "sd": float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0,
                "ci95": [round(ci_lo, 4), round(ci_hi, 4)],
            }

    # Compounding deltas per condition
    deltas: dict[str, dict] = {}
    for cond in CONDITIONS:
        ctrl = np.array(by_cond_stage[cond]["control"])
        s3 = np.array(by_cond_stage[cond]["step_3"])
        if len(ctrl) > 0 and len(s3) > 0:
            mean_ctrl = float(np.mean(ctrl))
            mean_s3 = float(np.mean(s3))
            deltas[cond] = {
                "control_mean": round(mean_ctrl, 4),
                "step_3_mean": round(mean_s3, 4),
                "delta": round(mean_s3 - mean_ctrl, 4),
            }
        else:
            deltas[cond] = {"control_mean": None, "step_3_mean": None, "delta": None}

    # Pre-registered hypothesis tests
    hypotheses: dict[str, dict] = {}

    # H_Q1a: constraint vs baseline at step_3 -- d < -.80
    a_con = np.array(by_cond_stage["constraint"]["step_3"])
    a_base = np.array(by_cond_stage["baseline"]["step_3"])
    if len(a_con) >= 2 and len(a_base) >= 2:
        t_val, df_val, p_val = welch_t(a_con, a_base)
        d_val = cohens_d(a_con, a_base)
        # Replicated if d < -.80 AND p < .01
        replicated = d_val < -0.80 and p_val < 0.01
        hypotheses["H_Q1a"] = {
            "description": "DCI(step_3, constraint) < DCI(step_3, baseline) -- d < -.80",
            "mean_constraint": round(float(np.mean(a_con)), 4),
            "mean_baseline": round(float(np.mean(a_base)), 4),
            "difference": round(float(np.mean(a_con) - np.mean(a_base)), 4),
            "t": round(t_val, 4),
            "df": round(df_val, 2),
            "p": round(p_val, 4),
            "cohens_d": round(d_val, 4),
            "replicated": replicated,
            "outcome": "SUPPORTED" if d_val < -0.80 and p_val < 0.05 else (
                "PARTIAL" if d_val < -0.50 and p_val < 0.05 else "NOT_SUPPORTED"
            ),
        }
    else:
        hypotheses["H_Q1a"] = {"outcome": "INSUFFICIENT_DATA", "n_constraint": len(a_con), "n_baseline": len(a_base)}

    # H_Q1b: constraint vs information at step_3 -- d < -.50
    a_info = np.array(by_cond_stage["information"]["step_3"])
    if len(a_con) >= 2 and len(a_info) >= 2:
        t_val, df_val, p_val = welch_t(a_con, a_info)
        d_val = cohens_d(a_con, a_info)
        hypotheses["H_Q1b"] = {
            "description": "DCI(step_3, constraint) < DCI(step_3, information) -- d < -.50",
            "mean_constraint": round(float(np.mean(a_con)), 4),
            "mean_information": round(float(np.mean(a_info)), 4),
            "difference": round(float(np.mean(a_con) - np.mean(a_info)), 4),
            "t": round(t_val, 4),
            "df": round(df_val, 2),
            "p": round(p_val, 4),
            "cohens_d": round(d_val, 4),
            "outcome": "SUPPORTED" if d_val < -0.50 and p_val < 0.05 else "NOT_SUPPORTED",
        }
    else:
        hypotheses["H_Q1b"] = {"outcome": "INSUFFICIENT_DATA"}

    # H_Q1c: constraint vs baseline at control
    c_con = np.array(by_cond_stage["constraint"]["control"])
    c_base = np.array(by_cond_stage["baseline"]["control"])
    if len(c_con) >= 2 and len(c_base) >= 2:
        t_val, df_val, p_val = welch_t(c_con, c_base)
        d_val = cohens_d(c_con, c_base)
        hypotheses["H_Q1c"] = {
            "description": "DCI(control, constraint) < DCI(control, baseline)",
            "mean_constraint": round(float(np.mean(c_con)), 4),
            "mean_baseline": round(float(np.mean(c_base)), 4),
            "difference": round(float(np.mean(c_con) - np.mean(c_base)), 4),
            "t": round(t_val, 4),
            "df": round(df_val, 2),
            "p": round(p_val, 4),
            "cohens_d": round(d_val, 4),
            "outcome": "SUPPORTED" if d_val < 0 and p_val < 0.05 else "NOT_SUPPORTED",
        }
    else:
        hypotheses["H_Q1c"] = {"outcome": "INSUFFICIENT_DATA"}

    # One-way ANOVA across conditions at step_3
    groups_s3 = [
        np.array(by_cond_stage[cond]["step_3"])
        for cond in CONDITIONS
        if len(by_cond_stage[cond]["step_3"]) >= 2
    ]
    anova: dict = {}
    if len(groups_s3) >= 2:
        f_stat, p_anova = stats.f_oneway(*groups_s3)
        eta_sq = eta_squared_oneway(groups_s3)
        anova = {
            "F": round(float(f_stat), 4),
            "p": round(float(p_anova), 4),
            "eta_squared": round(eta_sq, 4),
            "n_conditions": len(groups_s3),
        }

    # Per-dimension means at step_3 by condition
    per_dim: dict[str, dict[str, float]] = {cond: {} for cond in CONDITIONS}
    for r in records:
        cond = r.get("bf_condition", "")
        if cond not in CONDITIONS:
            continue
        if r.get("step") != 3 or not r.get("weights_valid") or not r.get("parsed_weights"):
            continue
        w = renormalize(r["parsed_weights"])
        for dim in DIMENSIONS:
            if dim not in per_dim[cond]:
                per_dim[cond][dim] = []
            per_dim[cond][dim].append(w.get(dim, 0))

    per_dim_means: dict[str, dict[str, Optional[float]]] = {}
    for cond in CONDITIONS:
        per_dim_means[cond] = {}
        for dim in DIMENSIONS:
            vals = per_dim[cond].get(dim, [])
            per_dim_means[cond][dim] = round(float(np.mean(vals)), 3) if vals else None

    # Model-level breakdown at step_3
    by_model_cond: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in records:
        if r.get("step") != 3 or not r.get("weights_valid") or not r.get("parsed_weights"):
            continue
        model = r.get("model", "unknown")
        cond = r.get("bf_condition", "")
        if cond not in CONDITIONS:
            continue
        by_model_cond[model][cond].append(compute_dci(r["parsed_weights"]))

    model_breakdown: dict[str, dict] = {}
    for model, cond_dict in by_model_cond.items():
        model_breakdown[model] = {}
        for cond in CONDITIONS:
            vals = cond_dict.get(cond, [])
            model_breakdown[model][cond] = {
                "n": len(vals),
                "mean_dci": round(float(np.mean(vals)), 4) if vals else None,
            }

    # Parse rates
    parse_rates: dict[str, dict] = {}
    for r in records:
        cond = r.get("bf_condition", "")
        model = r.get("model", "unknown")
        step = r.get("step", -1)
        if step == 1:
            continue  # step_1 has no weight parsing
        key = f"{model}_{cond}"
        if key not in parse_rates:
            parse_rates[key] = {"model": model, "condition": cond, "valid": 0, "total": 0}
        parse_rates[key]["total"] += 1
        if r.get("weights_valid"):
            parse_rates[key]["valid"] += 1

    return {
        "n_records_total": len(records),
        "n_records_valid": len(valid),
        "descriptive": desc,
        "compounding_deltas": deltas,
        "anova_step3": anova,
        "hypotheses": hypotheses,
        "per_dimension_step3": per_dim_means,
        "model_breakdown_step3": model_breakdown,
        "parse_rates": list(parse_rates.values()),
    }


def write_results_json(results: dict, output_path: Path) -> None:
    """Write results dict to JSON file."""
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Results JSON written to {output_path}")


def write_summary_markdown(results: dict, output_path: Path) -> None:
    """Write human-readable summary markdown."""
    lines = [
        "# Q1 Compounding x Specification — Results Summary",
        "",
        f"**Records**: {results['n_records_valid']} valid / {results['n_records_total']} total",
        "",
        "---",
        "",
        "## Compounding Slopes",
        "",
        "| Condition | Control DCI | Step 3 DCI | Delta |",
        "|-----------|------------|------------|-------|",
    ]

    for cond in CONDITIONS:
        d = results["compounding_deltas"].get(cond, {})
        ctrl = d.get("control_mean")
        s3 = d.get("step_3_mean")
        delta = d.get("delta")
        ctrl_str = f"{ctrl:.3f}" if ctrl is not None else "N/A"
        s3_str = f"{s3:.3f}" if s3 is not None else "N/A"
        delta_str = f"{delta:+.3f}" if delta is not None else "N/A"
        lines.append(f"| {cond} | {ctrl_str} | {s3_str} | {delta_str} |")

    lines += [
        "",
        "---",
        "",
        "## One-Way ANOVA at Step 3",
        "",
    ]
    anova = results.get("anova_step3", {})
    if anova:
        lines.append(
            f"F({anova.get('n_conditions', '?') - 1}, ...) = {anova.get('F', 'N/A')}, "
            f"p = {anova.get('p', 'N/A')}, eta-sq = {anova.get('eta_squared', 'N/A')}"
        )
    else:
        lines.append("Insufficient data for ANOVA.")

    lines += [
        "",
        "---",
        "",
        "## Planned Contrasts",
        "",
    ]

    for hyp_key in ["H_Q1a", "H_Q1b", "H_Q1c"]:
        h = results["hypotheses"].get(hyp_key, {})
        outcome = h.get("outcome", "?")
        desc = h.get("description", "")
        d_val = h.get("cohens_d")
        p_val = h.get("p")
        d_str = f"d = {d_val:.3f}" if d_val is not None else ""
        p_str = f"p = {p_val:.4f}" if p_val is not None else ""
        lines.append(f"**{hyp_key} {outcome}**: {desc}")
        if d_str or p_str:
            lines.append(f"  {d_str}, {p_str}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Per-Dimension Weights at Step 3",
        "",
        "| Dimension | Baseline | Information | Constraint | Uniform |",
        "|-----------|----------|-------------|------------|---------|",
    ]
    per_dim = results.get("per_dimension_step3", {})
    for dim in DIMENSIONS:
        base_val = per_dim.get("baseline", {}).get(dim)
        info_val = per_dim.get("information", {}).get(dim)
        con_val = per_dim.get("constraint", {}).get(dim)
        base_str = f"{base_val:.1f}" if base_val is not None else "N/A"
        info_str = f"{info_val:.1f}" if info_val is not None else "N/A"
        con_str = f"{con_val:.1f}" if con_val is not None else "N/A"
        lines.append(f"| {dim} | {base_str} | {info_str} | {con_str} | 12.5 |")

    lines += [
        "",
        "---",
        "",
        "## Model Breakdown at Step 3 (Mean DCI)",
        "",
        "| Model | Baseline | Information | Constraint |",
        "|-------|----------|-------------|------------|",
    ]
    model_bd = results.get("model_breakdown_step3", {})
    for model in sorted(model_bd.keys()):
        row = model_bd[model]
        b = row.get("baseline", {}).get("mean_dci")
        i = row.get("information", {}).get("mean_dci")
        c = row.get("constraint", {}).get("mean_dci")
        b_str = f"{b:.3f}" if b is not None else "N/A"
        i_str = f"{i:.3f}" if i is not None else "N/A"
        c_str = f"{c:.3f}" if c is not None else "N/A"
        lines.append(f"| {model} | {b_str} | {i_str} | {c_str} |")

    lines += ["", "---", ""]

    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Summary markdown written to {output_path}")


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent  # experiment/
    data_path = repo_root / "L3_sessions" / "exp_q1_compounding_spec.jsonl"

    if not data_path.exists():
        print(f"ERROR: Data file not found: {data_path}")
        print("Run the experiment first:")
        print("  uv run python L2_prompts/exp_q1_compounding_spec.py --live")
        sys.exit(1)

    print(f"Analyzing {data_path}")
    results = analyze(data_path)

    results_json_path = script_dir / "exp_q1_compounding_spec_results.json"
    summary_md_path = script_dir / "exp_q1_compounding_spec_summary.md"

    write_results_json(results, results_json_path)
    write_summary_markdown(results, summary_md_path)

    # Print quick summary to stdout
    print("\n=== Quick Summary ===")
    for hyp_key in ["H_Q1a", "H_Q1b", "H_Q1c"]:
        h = results["hypotheses"].get(hyp_key, {})
        outcome = h.get("outcome", "?")
        d_val = h.get("cohens_d")
        p_val = h.get("p")
        d_str = f"d={d_val:.3f}" if d_val is not None else ""
        p_str = f"p={p_val:.4f}" if p_val is not None else ""
        parts = [s for s in [d_str, p_str] if s]
        suffix = f" ({', '.join(parts)})" if parts else ""
        print(f"  {hyp_key}: {outcome}{suffix}")

    deltas = results.get("compounding_deltas", {})
    for cond in CONDITIONS:
        d = deltas.get(cond, {})
        s3 = d.get("step_3_mean")
        delta = d.get("delta")
        if s3 is not None:
            print(f"  {cond}: step_3 DCI={s3:.3f}, delta={delta:+.3f}")


if __name__ == "__main__":
    main()
