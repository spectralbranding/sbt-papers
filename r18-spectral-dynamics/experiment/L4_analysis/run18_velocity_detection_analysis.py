#!/usr/bin/env python3
"""Run 18: Dimensional Velocity Detection — Analysis.

Tests H1 (rising vs falling), H2 (Bonnet pair), H3 (oscillating variance).
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


def test_h1(records: list[dict]) -> dict:
    """H1: Rising vs Falling produce different profiles on >=3 dims."""
    rising = [r for r in records if r["condition"] == "rising"]
    falling = [r for r in records if r["condition"] == "falling"]

    results = {}
    sig_count = 0

    for i, dim in enumerate(DIMENSIONS):
        r_vals = [weights_to_vector(r["parsed_weights"])[i] for r in rising]
        f_vals = [weights_to_vector(r["parsed_weights"])[i] for r in falling]

        if len(r_vals) < 2 or len(f_vals) < 2:
            results[dim] = {"t": 0, "p": 1.0, "d": 0, "significant": False}
            continue

        t_stat, p_val = stats.ttest_ind(r_vals, f_vals)
        pooled_std = np.sqrt(
            (
                (len(r_vals) - 1) * np.var(r_vals, ddof=1)
                + (len(f_vals) - 1) * np.var(f_vals, ddof=1)
            )
            / (len(r_vals) + len(f_vals) - 2)
        )
        d = (np.mean(r_vals) - np.mean(f_vals)) / pooled_std if pooled_std > 0 else 0

        sig = p_val < 0.05
        if sig:
            sig_count += 1

        results[dim] = {
            "rising_mean": round(float(np.mean(r_vals)), 4),
            "falling_mean": round(float(np.mean(f_vals)), 4),
            "t": round(float(t_stat), 3),
            "p": round(float(p_val), 4),
            "cohens_d": round(float(d), 3),
            "significant": sig,
        }

    return {
        "per_dimension": results,
        "significant_count": sig_count,
        "h1_supported": sig_count >= 3,
    }


def test_h2(records: list[dict]) -> dict:
    """H2: Stable-high vs Falling differ (Bonnet pair resolution)."""
    stable = [r for r in records if r["condition"] == "stable_high"]
    falling = [r for r in records if r["condition"] == "falling"]

    results = {}
    sig_count = 0

    for i, dim in enumerate(DIMENSIONS):
        s_vals = [weights_to_vector(r["parsed_weights"])[i] for r in stable]
        f_vals = [weights_to_vector(r["parsed_weights"])[i] for r in falling]

        if len(s_vals) < 2 or len(f_vals) < 2:
            results[dim] = {"t": 0, "p": 1.0, "d": 0, "significant": False}
            continue

        t_stat, p_val = stats.ttest_ind(s_vals, f_vals)
        pooled_std = np.sqrt(
            (
                (len(s_vals) - 1) * np.var(s_vals, ddof=1)
                + (len(f_vals) - 1) * np.var(f_vals, ddof=1)
            )
            / (len(s_vals) + len(f_vals) - 2)
        )
        d = (np.mean(s_vals) - np.mean(f_vals)) / pooled_std if pooled_std > 0 else 0

        sig = p_val < 0.05
        if sig:
            sig_count += 1

        results[dim] = {
            "stable_mean": round(float(np.mean(s_vals)), 4),
            "falling_mean": round(float(np.mean(f_vals)), 4),
            "t": round(float(t_stat), 3),
            "p": round(float(p_val), 4),
            "cohens_d": round(float(d), 3),
            "significant": sig,
        }

    return {
        "per_dimension": results,
        "significant_count": sig_count,
        "h2_supported": sig_count >= 1,
    }


def test_h3(records: list[dict]) -> dict:
    """H3: Oscillating produces wider variance than Stable (exploratory)."""
    oscillating = [r for r in records if r["condition"] == "oscillating"]
    stable = [r for r in records if r["condition"] == "stable_high"]

    osc_vecs = np.array([weights_to_vector(r["parsed_weights"]) for r in oscillating])
    stb_vecs = np.array([weights_to_vector(r["parsed_weights"]) for r in stable])

    if len(osc_vecs) < 2 or len(stb_vecs) < 2:
        return {"note": "Insufficient data", "h3_exploratory": False}

    osc_var = float(np.mean(np.var(osc_vecs, axis=0)))
    stb_var = float(np.mean(np.var(stb_vecs, axis=0)))

    # Levene test across all dimensions
    per_dim = {}
    wider_count = 0
    for i, dim in enumerate(DIMENSIONS):
        o_vals = osc_vecs[:, i]
        s_vals = stb_vecs[:, i]
        lev_stat, lev_p = stats.levene(o_vals, s_vals)
        wider = float(np.var(o_vals)) > float(np.var(s_vals))
        if wider:
            wider_count += 1
        per_dim[dim] = {
            "osc_var": round(float(np.var(o_vals)), 6),
            "stable_var": round(float(np.var(s_vals)), 6),
            "levene_F": round(float(lev_stat), 3),
            "levene_p": round(float(lev_p), 4),
            "osc_wider": wider,
        }

    return {
        "mean_osc_variance": round(osc_var, 6),
        "mean_stable_variance": round(stb_var, 6),
        "per_dimension": per_dim,
        "dims_osc_wider": wider_count,
        "h3_exploratory": osc_var > stb_var,
    }


def main():
    data_dir = Path(__file__).parent.parent / "L3_sessions"
    jsonl_path = data_dir / "run18_velocity_detection.jsonl"

    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found.")
        sys.exit(1)

    records = load_data(jsonl_path)
    print(f"Loaded {len(records)} valid records")

    for traj in ["rising", "falling", "stable_high", "oscillating"]:
        n = len([r for r in records if r["condition"] == traj])
        print(f"  {traj}: {n}")

    print("\n--- H1: Rising vs Falling ---")
    h1 = test_h1(records)
    for dim, r in h1["per_dimension"].items():
        sig = "***" if r["significant"] else ""
        print(
            f"  {dim:14s} t={r['t']:7.3f} p={r['p']:.4f} "
            f"d={r['cohens_d']:.3f} {sig}"
        )
    print(
        f"  Significant: {h1['significant_count']}/8  "
        f"H1 {'SUPPORTED' if h1['h1_supported'] else 'NOT SUPPORTED'}"
    )

    print("\n--- H2: Stable vs Falling (Bonnet Pair) ---")
    h2 = test_h2(records)
    for dim, r in h2["per_dimension"].items():
        sig = "***" if r["significant"] else ""
        print(
            f"  {dim:14s} t={r['t']:7.3f} p={r['p']:.4f} "
            f"d={r['cohens_d']:.3f} {sig}"
        )
    print(
        f"  Significant: {h2['significant_count']}/8  "
        f"H2 {'SUPPORTED' if h2['h2_supported'] else 'NOT SUPPORTED'}"
    )

    print("\n--- H3: Oscillating Variance (Exploratory) ---")
    h3 = test_h3(records)
    if "per_dimension" in h3:
        for dim, r in h3["per_dimension"].items():
            wider = "WIDER" if r["osc_wider"] else ""
            print(
                f"  {dim:14s} osc={r['osc_var']:.6f} "
                f"stb={r['stable_var']:.6f} {wider}"
            )
    print(
        f"  Overall: {'Oscillating wider' if h3['h3_exploratory'] else 'Stable wider'}"
    )

    total_cost = sum(r.get("api_cost_usd", 0) for r in records)

    results = {
        "experiment": "exp3_velocity_detection",
        "date": "2026-04-16",
        "total_records": len(records),
        "total_cost_usd": round(total_cost, 4),
        "h1": h1,
        "h2": h2,
        "h3": h3,
    }

    results_path = Path(__file__).parent / "run18_velocity_detection_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()
