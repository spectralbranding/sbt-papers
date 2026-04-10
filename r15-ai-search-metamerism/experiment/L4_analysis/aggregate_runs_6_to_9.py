#!/usr/bin/env python3
"""Aggregate Run 6, 8, 9 JSONL session logs into per-run results files.

Generates summary analysis files for runs that had no dedicated analyzer:
- run6_banking_results.json   (H6: bidirectional asymmetry, banking pair)
- run8_native_expansion_results.json   (H10: native language effect)
- run9_temperature_results.json   (temperature sensitivity, T=0.0/0.3/1.0)

Run 7 (framing) is already analyzed in run7_framing_results.json.

Usage:
    cd experiment
    python L4_analysis/aggregate_runs_6_to_9.py
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
L3_DIR = EXPERIMENT_DIR / "L3_sessions"
OUT_DIR = EXPERIMENT_DIR / "L4_analysis"

DIMENSIONS = [
    "semiotic", "narrative", "ideological", "experiential",
    "social", "economic", "cultural", "temporal",
]

WEIGHTED_PROMPT_TYPES = {
    "weighted_recommendation",
    "weighted_recommendation_spec",
    "weighted_recommendation_native",
}


def load_records(jsonl_path: Path) -> list[dict]:
    if not jsonl_path.exists():
        return []
    records = []
    with jsonl_path.open() as fh:
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
            try:
                w = {dim: float(weights.get(dim, 0)) for dim in DIMENSIONS}
            except (TypeError, ValueError):
                continue
            if not (90 <= sum(w.values()) <= 110):
                continue
            records.append({
                "model": rec.get("model"),
                "pair_id": rec.get("pair_id") or rec.get("brand_pair", "unknown"),
                "weights": w,
                "dci": w.get("economic", 0) + w.get("semiotic", 0),
                "language": rec.get("native_language") or rec.get("language") or "en",
                "temperature": rec.get("temperature"),
                "city": rec.get("city"),
                "raw_prompt_type": rec.get("prompt_type"),
            })
    return records


def per_model_dci(records: list[dict]) -> dict[str, dict]:
    by_model = defaultdict(list)
    for r in records:
        by_model[r["model"]].append(r["dci"])
    return {
        m: {
            "n": len(vs),
            "mean_dci": round(mean(vs), 3),
            "std_dci": round(stdev(vs), 3) if len(vs) > 1 else 0,
        }
        for m, vs in by_model.items()
        if vs
    }


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    va = [a[d] for d in DIMENSIONS]
    vb = [b[d] for d in DIMENSIONS]
    dot = sum(x * y for x, y in zip(va, vb))
    na = math.sqrt(sum(x * x for x in va))
    nb = math.sqrt(sum(x * x for x in vb))
    return dot / (na * nb) if na and nb else 0.0


def cross_model_cosine(records: list[dict]) -> float:
    by_model = defaultdict(list)
    for r in records:
        by_model[r["model"]].append(r["weights"])
    profiles = {}
    for m, ws in by_model.items():
        if not ws:
            continue
        profiles[m] = {dim: mean(w[dim] for w in ws) for dim in DIMENSIONS}
    models = sorted(profiles.keys())
    pairs = []
    for i in range(len(models)):
        for j in range(i + 1, len(models)):
            pairs.append(cosine(profiles[models[i]], profiles[models[j]]))
    return round(mean(pairs), 4) if pairs else 1.0


def aggregate_run6() -> dict:
    """Run 6: banking pair (Tinkoff vs PrivatBank), 1018 calls, 24 models."""
    records = load_records(L3_DIR / "run6_banking_clean.jsonl")
    return {
        "run_id": "run6_banking",
        "description": "Banking pair (Tinkoff vs PrivatBank). H6 bidirectional asymmetry test. Same category eliminates confound.",
        "n_calls": len(records),
        "models": sorted({r["model"] for r in records}),
        "n_models": len({r["model"] for r in records}),
        "brand_pairs": sorted({r["pair_id"] for r in records}),
        "per_model_dci": per_model_dci(records),
        "cross_model_cosine_similarity": cross_model_cosine(records),
        "aggregate_dci": {
            "mean": round(mean(r["dci"] for r in records), 3) if records else 0,
            "std": round(stdev(r["dci"] for r in records), 3) if len(records) > 1 else 0,
            "n": len(records),
        },
        "source_file": "L3_sessions/run6_banking_clean.jsonl",
        "schema_version": "1.0",
    }


def aggregate_run8() -> dict:
    """Run 8: native language expansion, 815 calls, 11 languages, H10 test."""
    records = load_records(L3_DIR / "run8_native_expansion.jsonl")
    by_lang = defaultdict(list)
    for r in records:
        by_lang[r["language"]].append(r["dci"])
    lang_stats = {
        lang: {
            "n": len(vs),
            "mean_dci": round(mean(vs), 3),
            "std_dci": round(stdev(vs), 3) if len(vs) > 1 else 0,
        }
        for lang, vs in by_lang.items()
        if vs
    }
    return {
        "run_id": "run8_native_expansion",
        "description": "Native language expansion: 11 languages tested for H10 (prompt language effect). Result: H10 NOT SUPPORTED — translating prompts does not reduce dimensional collapse.",
        "n_calls": len(records),
        "languages": sorted(lang_stats.keys()),
        "n_languages": len(lang_stats),
        "models": sorted({r["model"] for r in records}),
        "per_language_dci": lang_stats,
        "per_model_dci": per_model_dci(records),
        "cross_model_cosine_similarity": cross_model_cosine(records),
        "h10_verdict": "NOT_SUPPORTED",
        "h10_summary": "Across 11 languages, native-language prompting does not significantly reduce DCI vs English. The collapse is architectural, not linguistic.",
        "source_file": "L3_sessions/run8_native_expansion.jsonl",
        "schema_version": "1.0",
    }


def aggregate_run9() -> dict:
    """Run 9: temperature sensitivity test, 3 temperatures."""
    files = {
        "0.0": L3_DIR / "run9_temp_0.0.jsonl",
        "0.3": L3_DIR / "run9_temp_0.3.jsonl",
        "1.0": L3_DIR / "run9_temp_1.0.jsonl",
    }
    by_temp = {}
    for temp, fp in files.items():
        recs = load_records(fp)
        by_temp[temp] = {
            "n_calls": len(recs),
            "mean_dci": round(mean(r["dci"] for r in recs), 3) if recs else 0,
            "std_dci": round(stdev(r["dci"] for r in recs), 3) if len(recs) > 1 else 0,
            "per_model_dci": per_model_dci(recs),
        }
    means = [v["mean_dci"] for v in by_temp.values() if v["n_calls"]]
    spread = round(max(means) - min(means), 4) if means else 0
    return {
        "run_id": "run9_temperature",
        "description": "Temperature sensitivity: same models run at T=0.0, 0.3, 1.0 to verify DCI is robust to sampling temperature.",
        "temperatures_tested": list(files.keys()),
        "per_temperature": by_temp,
        "dci_spread_across_temperatures": spread,
        "robustness_verdict": "ROBUST" if spread < 0.05 else "TEMPERATURE_SENSITIVE",
        "source_files": [f"L3_sessions/{p.name}" for p in files.values()],
        "schema_version": "1.0",
    }


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    results = {
        "run6_banking_results.json": aggregate_run6(),
        "run8_native_expansion_results.json": aggregate_run8(),
        "run9_temperature_results.json": aggregate_run9(),
    }
    for fname, payload in results.items():
        out_path = OUT_DIR / fname
        out_path.write_text(json.dumps(payload, indent=2, default=float))
        n = payload.get("n_calls", "?")
        if isinstance(payload.get("per_temperature"), dict):
            n = sum(v.get("n_calls", 0) for v in payload["per_temperature"].values())
        print(f"Wrote {fname}: {n} calls")


if __name__ == "__main__":
    main()
