#!/usr/bin/env python3
"""Analysis for Experiment F2: Cross-Domain Primacy.

Reads L3_sessions/exp_f2_cross_domain_primacy.jsonl and tests all
pre-registered hypotheses from EXP_F2_CROSS_DOMAIN_PRIMACY_PROTOCOL.md.

Primary analyses:
  H_F2a -- Primacy in political domain (JSON format)
  H_F2b -- Comparable primacy magnitude across domains
  H_F2c -- Likert attenuates primacy in both domains
  H_F2d -- Domain-general finding (both domains significant in JSON)

Secondary analyses:
  - Per-domain primacy slopes (position 1-8 curve)
  - Domain x Format x Position three-way breakdown
  - Cross-domain effect size comparison

Usage:
    uv run python exp_f2_cross_domain_primacy_analysis.py
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats as sp_stats

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

JSONL_PATH = (
    Path(__file__).parent.parent / "L3_sessions" / "exp_f2_cross_domain_primacy.jsonl"
)
OUTPUT_DIR = Path(__file__).parent
RESULTS_PATH = OUTPUT_DIR / "exp_f2_cross_domain_primacy_results.json"
SUMMARY_PATH = OUTPUT_DIR / "exp_f2_cross_domain_primacy_summary.md"

DOMAINS = ["brand", "political"]
FORMATS = ["json", "likert"]


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------


def load_records() -> list[dict]:
    if not JSONL_PATH.exists():
        print(f"ERROR: {JSONL_PATH} not found.")
        sys.exit(1)
    records = []
    with open(JSONL_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def valid_records(records: list[dict]) -> list[dict]:
    return [r for r in records if r.get("weights_valid") and r.get("position_weights")]


def filter_records(
    records: list[dict],
    domain: str | None = None,
    response_format: str | None = None,
) -> list[dict]:
    out = valid_records(records)
    if domain is not None:
        out = [r for r in out if r.get("domain") == domain]
    if response_format is not None:
        out = [r for r in out if r.get("response_format") == response_format]
    return out


# ---------------------------------------------------------------------------
# Statistical Helpers
# ---------------------------------------------------------------------------


def bootstrap_ci(
    data: np.ndarray,
    n_boot: int = 10000,
    ci: float = .95,
    seed: int = 42,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    boot_means = np.array([
        np.mean(rng.choice(data, size=len(data), replace=True))
        for _ in range(n_boot)
    ])
    alpha = (1 - ci) / 2
    return float(np.percentile(boot_means, alpha * 100)), float(
        np.percentile(boot_means, (1 - alpha) * 100)
    )


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    pooled_std = np.sqrt((np.std(a, ddof=1) ** 2 + np.std(b, ddof=1) ** 2) / 2)
    if pooled_std == 0:
        return 0.0
    return float((np.mean(a) - np.mean(b)) / pooled_std)


def _get_pw(record: dict, pos: int) -> float | None:
    pw = record.get("position_weights")
    if pw is None:
        return None
    val = pw.get(pos, pw.get(str(pos)))
    return float(val) if val is not None else None


def primacy_score(record: dict) -> float | None:
    """Per-call primacy = mean(pos 1-2 weight) - mean(pos 7-8 weight)."""
    early = [_get_pw(record, p) for p in [1, 2]]
    late = [_get_pw(record, p) for p in [7, 8]]
    early_vals = [v for v in early if v is not None]
    late_vals = [v for v in late if v is not None]
    if not early_vals or not late_vals:
        return None
    return float(np.mean(early_vals) - np.mean(late_vals))


def extract_primacy_scores(records: list[dict]) -> np.ndarray:
    scores = [primacy_score(r) for r in records]
    return np.array([s for s in scores if s is not None])


def extract_position_arrays(records: list[dict]) -> dict[int, list[float]]:
    pos_data: dict[int, list[float]] = {p: [] for p in range(1, 9)}
    for r in records:
        for pos in range(1, 9):
            val = _get_pw(r, pos)
            if val is not None:
                pos_data[pos].append(val)
    return pos_data


# ---------------------------------------------------------------------------
# H_F2a: Primacy in Political Domain (JSON)
# ---------------------------------------------------------------------------


def test_hf2a(records: list[dict]) -> dict:
    """H_F2a: Primacy in political domain, JSON format."""
    subset = filter_records(records, domain="political", response_format="json")
    scores = extract_primacy_scores(subset)

    if len(scores) < 2:
        return {"status": "INSUFFICIENT_DATA", "n": len(scores)}

    # t-test against zero (one-sample: is mean primacy > 0?)
    t_stat, p_val = sp_stats.ttest_1samp(scores, popmean=0.0)
    # Also compute positions 1-2 vs 7-8 directly for interpretability
    pos_data = extract_position_arrays(subset)
    early = np.array(pos_data[1] + pos_data[2])
    late = np.array(pos_data[7] + pos_data[8])
    d = cohens_d(early, late)
    d_ci = bootstrap_ci(scores)

    supported = p_val < .05 and abs(d) >= .30
    return {
        "status": "SUPPORTED" if supported else "NOT SUPPORTED",
        "mean_primacy_score": round(float(np.mean(scores)), 3),
        "mean_pos_1_2": round(float(np.mean(early)), 2) if len(early) else None,
        "mean_pos_7_8": round(float(np.mean(late)), 2) if len(late) else None,
        "t_statistic": round(float(t_stat), 3),
        "p_value": round(float(p_val), 4),
        "cohens_d": round(d, 3),
        "d_ci_95": [round(d_ci[0], 3), round(d_ci[1], 3)],
        "n_records": len(subset),
        "n_scores": len(scores),
    }


# ---------------------------------------------------------------------------
# H_F2b: Comparable Magnitude Across Domains
# ---------------------------------------------------------------------------


def test_hf2b(records: list[dict]) -> dict:
    """H_F2b: Primacy magnitude does not differ between brand and political (JSON)."""
    brand_scores = extract_primacy_scores(
        filter_records(records, domain="brand", response_format="json")
    )
    political_scores = extract_primacy_scores(
        filter_records(records, domain="political", response_format="json")
    )

    if len(brand_scores) < 2 or len(political_scores) < 2:
        return {
            "status": "INSUFFICIENT_DATA",
            "n_brand": len(brand_scores),
            "n_political": len(political_scores),
        }

    t_stat, p_val = sp_stats.ttest_ind(brand_scores, political_scores)
    d = cohens_d(brand_scores, political_scores)
    brand_ci = bootstrap_ci(brand_scores)
    political_ci = bootstrap_ci(political_scores)

    # H_F2b is supported by non-significant difference (p >= .05)
    supported = p_val >= .05
    return {
        "status": "SUPPORTED (comparable)" if supported else "NOT SUPPORTED (significant domain difference)",
        "brand_mean_primacy": round(float(np.mean(brand_scores)), 3),
        "political_mean_primacy": round(float(np.mean(political_scores)), 3),
        "brand_ci_95": [round(brand_ci[0], 3), round(brand_ci[1], 3)],
        "political_ci_95": [round(political_ci[0], 3), round(political_ci[1], 3)],
        "t_statistic": round(float(t_stat), 3),
        "p_value": round(float(p_val), 4),
        "cohens_d": round(d, 3),
        "n_brand": len(brand_scores),
        "n_political": len(political_scores),
        "note": "Non-significant p (>= .05) supports domain comparability",
    }


# ---------------------------------------------------------------------------
# H_F2c: Likert Attenuates Primacy in Both Domains
# ---------------------------------------------------------------------------


def test_hf2c(records: list[dict]) -> dict:
    """H_F2c: JSON > Likert primacy within each domain. Bonferroni alpha = .025."""
    bonferroni_alpha = .025
    results = {}

    for domain in DOMAINS:
        json_scores = extract_primacy_scores(
            filter_records(records, domain=domain, response_format="json")
        )
        likert_scores = extract_primacy_scores(
            filter_records(records, domain=domain, response_format="likert")
        )

        if len(json_scores) < 2 or len(likert_scores) < 2:
            results[domain] = {
                "status": "INSUFFICIENT_DATA",
                "n_json": len(json_scores),
                "n_likert": len(likert_scores),
            }
            continue

        t_stat, p_val = sp_stats.ttest_ind(json_scores, likert_scores)
        d = cohens_d(json_scores, likert_scores)
        direction_ok = np.mean(json_scores) > np.mean(likert_scores)
        sig = p_val < bonferroni_alpha and direction_ok

        results[domain] = {
            "status": "SUPPORTED" if sig else "NOT SUPPORTED",
            "json_mean_primacy": round(float(np.mean(json_scores)), 3),
            "likert_mean_primacy": round(float(np.mean(likert_scores)), 3),
            "t_statistic": round(float(t_stat), 3),
            "p_value": round(float(p_val), 4),
            "significant_at_0025": sig,
            "cohens_d": round(d, 3),
            "direction_json_greater": direction_ok,
            "n_json": len(json_scores),
            "n_likert": len(likert_scores),
        }

    both_supported = all(
        r.get("status") == "SUPPORTED"
        for r in results.values()
        if r.get("status") != "INSUFFICIENT_DATA"
    )
    return {
        "status": "SUPPORTED" if both_supported else "NOT SUPPORTED",
        "per_domain": results,
    }


# ---------------------------------------------------------------------------
# H_F2d: Domain-General Finding
# ---------------------------------------------------------------------------


def test_hf2d(records: list[dict]) -> dict:
    """H_F2d: Both domains show significant primacy in JSON (d >= .30, p < .05)."""
    results = {}

    for domain in DOMAINS:
        subset = filter_records(records, domain=domain, response_format="json")
        pos_data = extract_position_arrays(subset)
        early = np.array(pos_data[1] + pos_data[2])
        late = np.array(pos_data[7] + pos_data[8])

        if len(early) < 2 or len(late) < 2:
            results[domain] = {"status": "INSUFFICIENT_DATA"}
            continue

        t_stat, p_val = sp_stats.ttest_ind(early, late)
        d = cohens_d(early, late)
        supported = p_val < .05 and abs(d) >= .30

        results[domain] = {
            "status": "SUPPORTED" if supported else "NOT SUPPORTED",
            "mean_pos_1_2": round(float(np.mean(early)), 2),
            "mean_pos_7_8": round(float(np.mean(late)), 2),
            "difference": round(float(np.mean(early) - np.mean(late)), 2),
            "t_statistic": round(float(t_stat), 3),
            "p_value": round(float(p_val), 4),
            "cohens_d": round(d, 3),
            "n_early": len(early),
            "n_late": len(late),
        }

    both_supported = all(
        r.get("status") == "SUPPORTED"
        for r in results.values()
        if r.get("status") != "INSUFFICIENT_DATA"
    )
    return {
        "status": "SUPPORTED (domain-general)" if both_supported else "NOT SUPPORTED",
        "per_domain": results,
    }


# ---------------------------------------------------------------------------
# Secondary: Position x Domain Interaction
# ---------------------------------------------------------------------------


def position_domain_interaction(records: list[dict]) -> dict:
    """Mean weight by position, split by domain and format."""
    curves: dict[str, dict] = {}

    for domain in DOMAINS:
        for fmt in FORMATS:
            key = f"{domain}_{fmt}"
            subset = filter_records(records, domain=domain, response_format=fmt)
            pos_data = extract_position_arrays(subset)

            means = {}
            for pos in range(1, 9):
                vals = pos_data[pos]
                means[pos] = round(float(np.mean(vals)), 2) if vals else None

            # Linear trend
            positions, weights = [], []
            for pos in range(1, 9):
                for v in pos_data[pos]:
                    positions.append(pos)
                    weights.append(v)

            if len(positions) > 2:
                slope, intercept, r_val, p_val, std_err = sp_stats.linregress(
                    positions, weights
                )
                linear = {
                    "slope": round(float(slope), 4),
                    "r_squared": round(float(r_val ** 2), 4),
                    "p_value": round(float(p_val), 4),
                }
            else:
                linear = {"status": "INSUFFICIENT_DATA"}

            curves[key] = {
                "domain": domain,
                "format": fmt,
                "n_records": len(subset),
                "mean_by_position": means,
                "linear_trend": linear,
            }

    return curves


# ---------------------------------------------------------------------------
# Secondary: Per-Model Primacy by Domain
# ---------------------------------------------------------------------------


def per_model_primacy_by_domain(records: list[dict]) -> dict:
    """Per-model primacy score in (brand, JSON) and (political, JSON)."""
    results: dict[str, dict] = {}

    for domain in DOMAINS:
        subset = filter_records(records, domain=domain, response_format="json")
        model_scores: dict[str, list[float]] = {}
        for r in subset:
            m = r.get("model", "unknown")
            score = primacy_score(r)
            if score is not None:
                model_scores.setdefault(m, []).append(score)

        for model, scores in sorted(model_scores.items()):
            arr = np.array(scores)
            ci = bootstrap_ci(arr)
            key = f"{model}_{domain}"
            results[key] = {
                "model": model,
                "domain": domain,
                "mean_primacy": round(float(np.mean(arr)), 3),
                "ci_95": [round(ci[0], 3), round(ci[1], 3)],
                "n": len(scores),
                "direction": "primacy" if np.mean(arr) > 0 else "recency",
            }

    return results


# ---------------------------------------------------------------------------
# Secondary: Per-Stimulus Primacy
# ---------------------------------------------------------------------------


def per_stimulus_primacy(records: list[dict]) -> dict:
    """Per-stimulus primacy magnitude in JSON format."""
    results: dict[str, dict] = {}

    for domain in DOMAINS:
        subset = filter_records(records, domain=domain, response_format="json")
        stimulus_scores: dict[str, list[float]] = {}
        for r in subset:
            s = r.get("stimulus", "unknown")
            score = primacy_score(r)
            if score is not None:
                stimulus_scores.setdefault(s, []).append(score)

        for stimulus, scores in sorted(stimulus_scores.items()):
            arr = np.array(scores)
            results[f"{domain}_{stimulus}"] = {
                "domain": domain,
                "stimulus": stimulus,
                "mean_primacy": round(float(np.mean(arr)), 3),
                "std": round(float(np.std(arr, ddof=1)), 3),
                "n": len(scores),
            }

    return results


# ---------------------------------------------------------------------------
# Summary Report
# ---------------------------------------------------------------------------


def generate_summary(records: list[dict], results: dict) -> str:
    total = len(records)
    n_valid = len(valid_records(records))
    pct = f"{n_valid / total * 100:.1f}%" if total else "N/A"
    first_ts = records[0]["timestamp"][:10] if records else "N/A"

    lines = [
        "# Experiment F2: Cross-Domain Primacy -- Results Summary",
        "",
        f"**Date**: {first_ts}",
        f"**Total calls**: {total}",
        f"**Valid responses**: {n_valid} ({pct})",
        "",
        "---",
        "",
        "## H_F2a: Primacy in Political Domain (JSON)",
        "",
    ]

    h = results["hf2a"]
    lines.append(f"**Result**: {h['status']}")
    if "mean_primacy_score" in h:
        lines.extend([
            f"- Mean primacy score: {h['mean_primacy_score']}",
            f"- Mean weight pos 1-2: {h['mean_pos_1_2']}",
            f"- Mean weight pos 7-8: {h['mean_pos_7_8']}",
            f"- t = {h['t_statistic']}, p = {h['p_value']}",
            f"- Cohen's d = {h['cohens_d']} (95% CI: {h['d_ci_95']})",
            f"- n = {h['n_records']}",
        ])

    lines.extend(["", "## H_F2b: Comparable Magnitude Across Domains", ""])
    h = results["hf2b"]
    lines.append(f"**Result**: {h['status']}")
    if "brand_mean_primacy" in h:
        lines.extend([
            f"- Brand JSON primacy: {h['brand_mean_primacy']} (95% CI: {h['brand_ci_95']})",
            f"- Political JSON primacy: {h['political_mean_primacy']} (95% CI: {h['political_ci_95']})",
            f"- t = {h['t_statistic']}, p = {h['p_value']}, d = {h['cohens_d']}",
            f"- {h.get('note', '')}",
        ])

    lines.extend(["", "## H_F2c: Likert Attenuates Primacy in Both Domains", ""])
    h = results["hf2c"]
    lines.append(f"**Result**: {h['status']}")
    for domain, dr in h.get("per_domain", {}).items():
        if "json_mean_primacy" in dr:
            sig_mark = " [sig]" if dr.get("significant_at_0025") else ""
            lines.append(
                f"- {domain}: JSON={dr['json_mean_primacy']} vs "
                f"Likert={dr['likert_mean_primacy']}, "
                f"t={dr['t_statistic']}, p={dr['p_value']}, "
                f"d={dr['cohens_d']}{sig_mark}"
            )

    lines.extend(["", "## H_F2d: Domain-General Finding", ""])
    h = results["hf2d"]
    lines.append(f"**Result**: {h['status']}")
    for domain, dr in h.get("per_domain", {}).items():
        if "cohens_d" in dr:
            lines.append(
                f"- {domain}: diff={dr['difference']}, "
                f"t={dr['t_statistic']}, p={dr['p_value']}, "
                f"d={dr['cohens_d']} [{dr['status']}]"
            )

    lines.extend(["", "## Position Curves by Domain x Format (Secondary)", ""])
    for cell_key, curve in results.get("position_curves", {}).items():
        means = curve.get("mean_by_position", {})
        lt = curve.get("linear_trend", {})
        vals = " | ".join(f"P{p}: {means.get(p, 'N/A')}" for p in range(1, 9))
        lines.append(f"**{cell_key}** (n={curve['n_records']}): {vals}")
        if "slope" in lt:
            lines.append(
                f"  Linear trend: slope={lt['slope']}, R2={lt['r_squared']}, p={lt['p_value']}"
            )
        lines.append("")

    lines.extend(["## Per-Model Primacy by Domain (Secondary)", ""])
    for key, mdata in sorted(results.get("per_model_primacy", {}).items()):
        lines.append(
            f"- {mdata['model']} / {mdata['domain']}: "
            f"primacy={mdata['mean_primacy']} (95% CI: {mdata['ci_95']}), "
            f"n={mdata['n']}, direction={mdata['direction']}"
        )

    lines.extend(["", "## Per-Stimulus Primacy (Secondary)", ""])
    for key, sdata in sorted(results.get("per_stimulus_primacy", {}).items()):
        lines.append(
            f"- {sdata['domain']} / {sdata['stimulus']}: "
            f"primacy={sdata['mean_primacy']} (sd={sdata['std']}, n={sdata['n']})"
        )

    lines.extend([
        "",
        "---",
        "",
        "*Analysis follows pre-registered protocol "
        "(EXP_F2_CROSS_DOMAIN_PRIMACY_PROTOCOL.md). "
        "Exploratory analyses labeled as such.*",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print("Loading data...")
    records = load_records()
    n_valid = len(valid_records(records))
    print(f"Loaded {len(records)} records, {n_valid} valid.")

    if n_valid == 0:
        print("No valid records found. Check JSONL file.")
        sys.exit(1)

    print("\nRunning H_F2a (primacy in political domain, JSON)...")
    hf2a = test_hf2a(records)
    print(f"  -> {hf2a['status']}")

    print("Running H_F2b (comparable primacy across domains)...")
    hf2b = test_hf2b(records)
    print(f"  -> {hf2b['status']}")

    print("Running H_F2c (Likert attenuation in both domains)...")
    hf2c = test_hf2c(records)
    print(f"  -> {hf2c['status']}")

    print("Running H_F2d (domain-general finding)...")
    hf2d = test_hf2d(records)
    print(f"  -> {hf2d['status']}")

    print("Running secondary analyses...")
    curves = position_domain_interaction(records)
    per_model = per_model_primacy_by_domain(records)
    per_stimulus = per_stimulus_primacy(records)

    results = {
        "hf2a": hf2a,
        "hf2b": hf2b,
        "hf2c": hf2c,
        "hf2d": hf2d,
        "position_curves": curves,
        "per_model_primacy": per_model,
        "per_stimulus_primacy": per_stimulus,
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved: {RESULTS_PATH}")

    summary = generate_summary(records, results)
    with open(SUMMARY_PATH, "w") as f:
        f.write(summary)
    print(f"Summary saved: {SUMMARY_PATH}")

    print(f"\n{'='*55}")
    print(f"HYPOTHESIS RESULTS")
    print(f"{'='*55}")
    print(f"H_F2a (political primacy, JSON):   {hf2a['status']}")
    print(f"H_F2b (comparable across domains): {hf2b['status']}")
    print(f"H_F2c (Likert attenuates both):    {hf2c['status']}")
    print(f"H_F2d (domain-general):            {hf2d['status']}")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()
