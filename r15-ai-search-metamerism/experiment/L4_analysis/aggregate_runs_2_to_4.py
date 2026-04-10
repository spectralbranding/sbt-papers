#!/usr/bin/env python3
"""Aggregate Run 2-4 JSONL session logs into per-run results files.

Generates the three top-level results files referenced by DATA_MANIFEST.yaml:
- ../results_v2_global.json
- ../results_v3_local.json
- ../results_v4_resolution.json

Output schema (per file):
{
  "run_id": str,
  "n_calls": int,
  "n_successful": int,
  "models": [str],
  "brand_pairs": [str],
  "dimensional_weights": {model_name: {dim: mean_weight}},
  "dci_per_model": {model_name: float},
  "dci_aggregate": {
    "mean": float, "std": float, "n": int,
    "h1_t_statistic": float, "h1_p_value": float
  },
  "cosine_similarity": {
    "matrix": [[float]],
    "model_order": [str],
    "mean_pairwise": float
  },
  "source_files": [str]
}

Usage:
    cd experiment
    python L4_analysis/aggregate_runs_2_to_4.py
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
L3_DIR = EXPERIMENT_DIR / "L3_sessions"
ROOT_DIR = EXPERIMENT_DIR.parent

DIMENSIONS = [
    "semiotic", "narrative", "ideological", "experiential",
    "social", "economic", "cultural", "temporal",
]

UNIFORM_BASELINE = 12.5  # 100 / 8
DCI_BASELINE = 25.0  # economic + semiotic at uniform


WEIGHTED_PROMPT_TYPES = {"weighted_recommendation", "weighted_recommendation_spec"}


def load_run(jsonl_files: list[Path]) -> list[dict]:
    """Load all weighted_recommendation records (including _spec variant) from given JSONL files."""
    records = []
    for f in jsonl_files:
        if not f.exists():
            continue
        with f.open() as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("prompt_type") not in WEIGHTED_PROMPT_TYPES:
                    continue
                parsed = rec.get("parsed") or {}
                weights = parsed.get("weights") if isinstance(parsed, dict) else None
                if not isinstance(weights, dict):
                    continue
                # Normalize weight values to float
                try:
                    w = {dim: float(weights.get(dim, 0)) for dim in DIMENSIONS}
                except (TypeError, ValueError):
                    continue
                # Skip records with weights that don't sum near 100
                if not (90 <= sum(w.values()) <= 110):
                    continue
                records.append({
                    "model": rec.get("model"),
                    "pair_id": rec.get("pair_id") or rec.get("brand_pair", "unknown"),
                    "weights": w,
                    "dci": w.get("economic", 0) + w.get("semiotic", 0),
                })
    return records


def compute_per_model_means(records: list[dict]) -> dict[str, dict[str, float]]:
    by_model = defaultdict(list)
    for r in records:
        by_model[r["model"]].append(r["weights"])
    out = {}
    for model, weight_list in by_model.items():
        if not weight_list:
            continue
        out[model] = {
            dim: round(mean(w[dim] for w in weight_list), 3)
            for dim in DIMENSIONS
        }
    return out


def compute_per_model_dci(records: list[dict]) -> dict[str, float]:
    by_model = defaultdict(list)
    for r in records:
        by_model[r["model"]].append(r["dci"])
    return {m: round(mean(vs), 3) for m, vs in by_model.items() if vs}


def cosine_similarity(a: dict[str, float], b: dict[str, float]) -> float:
    va = [a[d] for d in DIMENSIONS]
    vb = [b[d] for d in DIMENSIONS]
    dot = sum(x * y for x, y in zip(va, vb))
    na = math.sqrt(sum(x * x for x in va))
    nb = math.sqrt(sum(x * x for x in vb))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def cosine_matrix(per_model_means: dict[str, dict[str, float]]) -> dict:
    models = sorted(per_model_means.keys())
    matrix = []
    for m1 in models:
        row = []
        for m2 in models:
            row.append(round(cosine_similarity(per_model_means[m1], per_model_means[m2]), 4))
        matrix.append(row)
    # Mean pairwise (excluding diagonal)
    pairs = []
    for i in range(len(models)):
        for j in range(i + 1, len(models)):
            pairs.append(matrix[i][j])
    mean_pair = round(mean(pairs), 4) if pairs else 1.0
    return {
        "model_order": models,
        "matrix": matrix,
        "mean_pairwise": mean_pair,
    }


def one_sample_t(values: list[float], baseline: float) -> tuple[float, float]:
    """One-sample t-test against a baseline (no scipy dependency)."""
    n = len(values)
    if n < 2:
        return 0.0, 1.0
    m = mean(values)
    sd = stdev(values)
    if sd == 0:
        return 0.0, 1.0
    t = (m - baseline) / (sd / math.sqrt(n))
    # Approximate two-sided p-value via large-sample normal approximation
    # (good enough for n > 30, which is always the case here)
    z = abs(t)
    # Standard normal CDF approximation (Abramowitz & Stegun 26.2.17)
    p = math.erfc(z / math.sqrt(2))
    return round(t, 4), round(p, 6)


def aggregate_run(
    run_id: str,
    jsonl_files: list[Path],
    description: str,
) -> dict:
    records = load_run(jsonl_files)
    per_model = compute_per_model_means(records)
    dci_per_model = compute_per_model_dci(records)
    dci_values = [r["dci"] for r in records]
    t_stat, p_val = one_sample_t(dci_values, DCI_BASELINE)
    cosine = cosine_matrix(per_model)
    return {
        "run_id": run_id,
        "description": description,
        "n_calls": len(records),
        "n_successful": len(records),
        "models": sorted(per_model.keys()),
        "brand_pairs": sorted({r["pair_id"] for r in records}),
        "dimensional_weights": per_model,
        "dci_per_model": dci_per_model,
        "dci_aggregate": {
            "mean": round(mean(dci_values), 3) if dci_values else 0,
            "std": round(stdev(dci_values), 3) if len(dci_values) > 1 else 0,
            "n": len(dci_values),
            "baseline": DCI_BASELINE,
            "h1_t_statistic": t_stat,
            "h1_p_value": p_val,
        },
        "cosine_similarity": cosine,
        "source_files": sorted(f.name for f in jsonl_files if f.exists()),
        "schema_version": "1.0",
    }


def main() -> None:
    runs = [
        {
            "id": "run2_global",
            "files": [L3_DIR / "run2_global.jsonl", L3_DIR / "run2_qwen_plus.jsonl"],
            "description": "Run 2: 10 global brand pairs, 6 LLMs, 3 runs each. Primary DCI measure.",
            "out_path": ROOT_DIR / "results_v2_global.json",
        },
        {
            "id": "run3_local",
            "files": [L3_DIR / "run3_local.jsonl", L3_DIR / "run3_qwen_plus.jsonl"],
            "description": "Run 3: 5 local brand pairs (Cyprus, Latvia, Kenya, Vietnam, Serbia), 6 LLMs, 3 runs each. Tests conditional metamerism.",
            "out_path": ROOT_DIR / "results_v3_local.json",
        },
        {
            "id": "run4_resolution",
            "files": [L3_DIR / "run4_resolution.jsonl"],
            "description": "Run 4: 5 local brand pairs with Brand Function specifications. Tests whether specification resolves dimensional collapse.",
            "out_path": ROOT_DIR / "results_v4_resolution.json",
        },
    ]

    for r in runs:
        result = aggregate_run(r["id"], r["files"], r["description"])
        r["out_path"].write_text(json.dumps(result, indent=2))
        print(
            f"Wrote {r['out_path'].name}: "
            f"{result['n_calls']} calls, "
            f"{len(result['models'])} models, "
            f"DCI={result['dci_aggregate']['mean']}, "
            f"cosine={result['cosine_similarity']['mean_pairwise']}"
        )


if __name__ == "__main__":
    main()
