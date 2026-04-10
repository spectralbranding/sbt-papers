#!/usr/bin/env python3
"""Run 10 — Corrective Comparators Experiment.

Tests whether AI dimensional weight profiles change when the same focal
brand is paired against a structurally-correct comparator versus the
dominant Anglophone category template. Built as a thin wrapper over
ai_search_metamerism.py — reuses the PRISM-B prompts, parser, and JSONL
session log format.

DESIGN

For each of three focal brands, we run TWO comparator conditions on the
same focal brand and compare dimensional weight profiles directly.

| Focal brand | Original comparator (R15 control) | Corrective comparator (NEW) |
|-------------|-----------------------------------|-----------------------------|
| VkusVill    | Whole Foods                       | Trader Joe's                |
| Calbee      | Frito-Lay                         | Koikeya (same-culture JP)   |
| Roshen      | Cadbury                           | Hershey (multi-category)    |

HYPOTHESES

H_VkusVill: Pairing VkusVill against Trader Joe's produces a higher
            cross-model mean Cultural + Experiential weight (closer to the
            actual brand) than pairing against Whole Foods.

H_Calbee:   Pairing Calbee against Koikeya (same-culture Japanese) preserves
            Cultural and Temporal dimensions better than pairing against
            any Western brand.

H_Roshen:   Pairing Roshen against Hershey (multi-category US confectionery)
            produces a less collapsed profile than pairing against Cadbury
            (chocolate-only).

These are within-focal-brand paired comparisons across the same model panel.
The R15 cross-model convergence finding (cosine 0.977) means the choice of
model has minimal effect on the underlying spectral profile, so 7 models is
sufficient for power.

MODEL PANEL (7 models, drawn from the R15 v2.0 panel)

1. claude          — Claude Sonnet 4.6        (Anthropic, Western, paid cloud)
2. gpt             — GPT-4o-mini              (OpenAI, Western, paid cloud)
3. gemini          — Gemini 2.5 Flash         (Google, Western, paid cloud)
4. deepseek        — DeepSeek V3              (DeepSeek, Chinese, paid cloud)
5. qwen35_local    — Qwen3.5 27B              (Alibaba, Chinese, local Ollama)
6. gemma4_local    — Gemma 4 27B              (Google, Western, local Ollama)
7. yandexgpt_pro   — YandexGPT 5 Pro          (Yandex, Russian, free cloud)

Notes on model selection:
- Qwen3 30B was removed; Qwen3.5 27B (newer same-family Chinese model)
  is a 1:1 substitute. The two are within ~15% on parameter count and
  cluster identically in Run 5 cross-model cosine, so the substitution
  is methodologically clean.
- YandexGPT 5 Pro is added because VkusVill is a Russian brand. A
  Russian-trained model provides the strongest test of whether AI can
  see VkusVill *as itself* (not through any Western template). The
  Russian-model arm is most informative for VkusVill; for Calbee and
  Roshen it serves as a within-experiment control.
- Total: 7 models, mixing 4 Western (3 cloud + 1 local), 2 Chinese
  (1 cloud + 1 local), and 1 Russian. This is the smallest panel that
  still spans the relevant cultural traditions while keeping the
  experiment short and cheap.

EXPERIMENT VOLUME

6 brand pairs × 7 models × 3 runs × ~5 prompts per call ≈ 630 API calls
Estimated wall-clock time: 30-60 minutes (mostly network latency)
Estimated cost: under $0.50 (most calls are free-tier or local)

OUTPUT

L3_sessions/run10_corrective.jsonl  — raw session log (one JSON object per call)
L4_analysis/run10_corrective_results.json — aggregated dimensional weights
L4_analysis/run10_corrective_summary.md   — human-readable comparison tables

USAGE

    cd experiment
    .venv/bin/python run10_corrective.py --demo    # offline dry run
    .venv/bin/python run10_corrective.py --smoke   # 1 pair × 7 models × 1 run
    .venv/bin/python run10_corrective.py --live    # full experiment

Requires the same env vars as the main R15 script (ANTHROPIC_API_KEY,
OPENAI_API_KEY, GOOGLE_API_KEY, DEEPSEEK_API_KEY, YANDEX_API_KEY) plus
local Ollama running with `qwen3.5:27b` and `gemma4:latest` pulled.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, stdev
from typing import Any

# Reuse the main script's prompt templates, model callers, and parser.
# Import-time the script will run its module-level setup; nothing else fires.
sys.path.insert(0, str(Path(__file__).parent))
import ai_search_metamerism as asm  # noqa: E402

EXPERIMENT_DIR = Path(__file__).resolve().parent
L3_DIR = EXPERIMENT_DIR / "L3_sessions"
L4_DIR = EXPERIMENT_DIR / "L4_analysis"
OUT_LOG = L3_DIR / "run10_corrective.jsonl"
OUT_RESULTS = L4_DIR / "run10_corrective_results.json"
OUT_SUMMARY = L4_DIR / "run10_corrective_summary.md"

DIMENSIONS = [
    "semiotic", "narrative", "ideological", "experiential",
    "social", "economic", "cultural", "temporal",
]


# ----------------------------------------------------------------------------
# Brand pairs — 3 focal brands × 2 comparator conditions = 6 pairs
# ----------------------------------------------------------------------------

CORRECTIVE_PAIRS: list[asm.BrandPair] = [
    # ----- VkusVill: original vs corrective -----
    asm.BrandPair(
        id="vkusvill_vs_whole_foods",
        brand_a="VkusVill",
        brand_b="Whole Foods Market",
        category="organic grocery chain",
        differentiating_dims=["ideological", "cultural"],
        dim_type="soft",
        description=(
            "Run 10 control: re-runs the original R15 supplementary pair "
            "(VkusVill paired against the dominant Anglophone organic grocery "
            "template). Used as the baseline for the corrective comparison."
        ),
    ),
    asm.BrandPair(
        id="vkusvill_vs_trader_joes",
        brand_a="VkusVill",
        brand_b="Trader Joe's",
        category="private-label clean-food grocery chain",
        differentiating_dims=["ideological", "cultural", "experiential"],
        dim_type="soft",
        description=(
            "Run 10 corrective: pairs VkusVill against the structurally "
            "correct US analog. Trader Joe's matches VkusVill on the "
            "operational dimensions that matter (private-label-dominant, "
            "smaller stores, higher turnover, distinctive own-brand identity, "
            "value-positioned). Tests whether changing the comparator "
            "produces a different dimensional weight profile."
        ),
    ),

    # ----- Calbee: original vs corrective -----
    asm.BrandPair(
        id="calbee_vs_frito_lay",
        brand_a="Calbee",
        brand_b="Frito-Lay",
        category="snack foods",
        differentiating_dims=["cultural", "temporal", "experiential"],
        dim_type="soft",
        description=(
            "Run 10 control: pairs Calbee against the dominant Anglophone "
            "snack-food template. Calbee's product architecture (vegetable "
            "bases, seasonal limited editions, kawaii aesthetics) is "
            "structurally different from American salty-snack brands."
        ),
    ),
    asm.BrandPair(
        id="calbee_vs_koikeya",
        brand_a="Calbee",
        brand_b="Koikeya",
        category="Japanese snack foods",
        differentiating_dims=["semiotic", "narrative", "experiential"],
        dim_type="mixed",
        description=(
            "Run 10 corrective: pairs Calbee against Koikeya, the "
            "second-largest Japanese snack maker (founded 1953, Tokyo). "
            "Same-culture pairing tests whether AI preserves Cultural and "
            "Temporal dimensions when the comparator shares the brand's "
            "actual cultural context. There is no clean Western analog for "
            "Calbee; the same-culture comparison is the methodologically "
            "clean alternative to forcing a Western template."
        ),
    ),

    # ----- Roshen: original vs corrective -----
    asm.BrandPair(
        id="roshen_vs_cadbury",
        brand_a="Roshen",
        brand_b="Cadbury",
        category="confectionery",
        differentiating_dims=["narrative", "cultural"],
        dim_type="soft",
        description=(
            "Run 10 control: pairs Roshen against Cadbury (chocolate-only "
            "British template). Same as the R15 supplementary pair."
        ),
    ),
    asm.BrandPair(
        id="roshen_vs_hershey",
        brand_a="Roshen",
        brand_b="The Hershey Company",
        category="multi-category confectionery",
        differentiating_dims=["narrative", "cultural", "experiential"],
        dim_type="mixed",
        description=(
            "Run 10 corrective: pairs Roshen against Hershey, which has "
            "expanded beyond chocolate via acquisitions (Reese's, Twizzlers, "
            "SkinnyPop popcorn, Dot's Pretzels, Pirate Brands snacks) into a "
            "multi-category confectionery and snack conglomerate. Hershey's "
            "structure is closer to Roshen's vertical integration than "
            "Cadbury's chocolate-only positioning, though no single US "
            "brand fully matches Roshen's spread across chocolate, biscuits, "
            "cakes, and jellies."
        ),
    ),
]

# Pair the corrective and control pairs by focal brand for the summary table
COMPARISON_PAIRS = [
    ("VkusVill",  "vkusvill_vs_whole_foods", "vkusvill_vs_trader_joes"),
    ("Calbee",    "calbee_vs_frito_lay",     "calbee_vs_koikeya"),
    ("Roshen",    "roshen_vs_cadbury",       "roshen_vs_hershey"),
]


# ----------------------------------------------------------------------------
# Model panel
# ----------------------------------------------------------------------------

# 7-model panel for Run 10. Names match keys in ai_search_metamerism.MODEL_IDS
# / API_CALLERS / API_KEY_VARS. The script will skip any model whose API key
# is not set in the environment, except for local Ollama models which always
# attempt the call.
MODEL_PANEL = [
    "claude",          # Claude Sonnet 4.6 (Western, paid cloud)
    "gpt",             # GPT-4o-mini (Western, paid cloud)
    "gemini",          # Gemini 2.5 Flash (Western, paid cloud)
    "deepseek",        # DeepSeek V3 (Chinese, paid cloud)
    "qwen35_local",    # Qwen3.5 27B (Chinese, local Ollama) — NEW substitute for qwen3_local
    "gemma4_local",    # Gemma 4 27B (Western, local Ollama)
    "yandexgpt_pro",   # YandexGPT 5 Pro (Russian, free cloud) — NEW addition for VkusVill case
]


# ----------------------------------------------------------------------------
# Analysis helpers
# ----------------------------------------------------------------------------

def parse_weighted_recommendation(record: dict) -> dict[str, float] | None:
    """Extract the 8-dimensional weight vector from a session record.

    Returns None if the record is not a weighted_recommendation call or the
    parsed weights are missing/malformed/out of tolerance.
    """
    if record.get("prompt_type") != "weighted_recommendation":
        return None
    parsed = record.get("parsed") or {}
    if not isinstance(parsed, dict):
        return None
    weights = parsed.get("weights")
    if not isinstance(weights, dict):
        return None
    try:
        w = {dim: float(weights.get(dim, 0)) for dim in DIMENSIONS}
    except (TypeError, ValueError):
        return None
    total = sum(w.values())
    if not (90 <= total <= 110):
        return None
    return w


def aggregate_pair_profile(records: list[dict], pair_id: str) -> dict[str, Any]:
    """Compute mean dimensional weights and DCI for a single pair across all
    models in the panel.
    """
    by_model: dict[str, list[dict[str, float]]] = {}
    for r in records:
        if r.get("pair_id") != pair_id and r.get("brand_pair") != pair_id:
            continue
        w = parse_weighted_recommendation(r)
        if w is None:
            continue
        by_model.setdefault(r.get("model"), []).append(w)

    per_model_profiles: dict[str, dict[str, float]] = {}
    per_model_dci: dict[str, float] = {}
    for model, profiles in by_model.items():
        per_model_profiles[model] = {
            dim: round(mean(p[dim] for p in profiles), 3) for dim in DIMENSIONS
        }
        per_model_dci[model] = round(
            per_model_profiles[model]["economic"]
            + per_model_profiles[model]["semiotic"],
            3,
        )

    if per_model_profiles:
        cross_model_mean: dict[str, float] = {
            dim: round(
                mean(per_model_profiles[m][dim] for m in per_model_profiles),
                3,
            )
            for dim in DIMENSIONS
        }
        cross_model_dci = round(
            cross_model_mean["economic"] + cross_model_mean["semiotic"], 3
        )
    else:
        cross_model_mean = {dim: 0.0 for dim in DIMENSIONS}
        cross_model_dci = 0.0

    return {
        "pair_id": pair_id,
        "n_calls": sum(len(p) for p in by_model.values()),
        "n_models_with_data": len(per_model_profiles),
        "per_model_profiles": per_model_profiles,
        "per_model_dci": per_model_dci,
        "cross_model_mean_profile": cross_model_mean,
        "cross_model_mean_dci": cross_model_dci,
    }


def write_summary(results: dict[str, Any]) -> None:
    """Write a human-readable Markdown summary of Run 10 results."""
    lines = [
        "# Run 10 — Corrective Comparators Results",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Design",
        "",
        "Three focal brands × two comparator conditions × 7 models × 3 runs.",
        "Tests whether changing the comparator produces a different dimensional",
        "weight profile for the same focal brand.",
        "",
        "## Cross-model mean DCI by pair",
        "",
        "| Focal brand | Comparator | DCI (mean across models) | Δ vs control |",
        "|---|---|---|---|",
    ]
    for focal, control_id, corrective_id in COMPARISON_PAIRS:
        control = results["pairs"].get(control_id, {})
        corrective = results["pairs"].get(corrective_id, {})
        c_dci = control.get("cross_model_mean_dci", 0)
        cor_dci = corrective.get("cross_model_mean_dci", 0)
        delta = round(cor_dci - c_dci, 3)
        lines.append(
            f"| {focal} | {control.get('pair_id', '?')} (control) | {c_dci} | — |"
        )
        lines.append(
            f"| {focal} | {corrective.get('pair_id', '?')} (corrective) | {cor_dci} | {delta:+.3f} |"
        )

    lines += [
        "",
        "## Per-dimension delta (corrective − control)",
        "",
        "Positive values mean the corrective comparator preserves *more* of that",
        "dimension; negative values mean it preserves less.",
        "",
        "| Focal brand | Cultural | Temporal | Narrative | Ideological | Experiential | Social |",
        "|---|---|---|---|---|---|---|",
    ]
    for focal, control_id, corrective_id in COMPARISON_PAIRS:
        control = results["pairs"].get(control_id, {}).get("cross_model_mean_profile", {})
        corrective = results["pairs"].get(corrective_id, {}).get("cross_model_mean_profile", {})
        deltas = {
            dim: round(corrective.get(dim, 0) - control.get(dim, 0), 3)
            for dim in ["cultural", "temporal", "narrative", "ideological", "experiential", "social"]
        }
        lines.append(
            f"| {focal} | "
            f"{deltas['cultural']:+.3f} | {deltas['temporal']:+.3f} | "
            f"{deltas['narrative']:+.3f} | {deltas['ideological']:+.3f} | "
            f"{deltas['experiential']:+.3f} | {deltas['social']:+.3f} |"
        )

    lines += [
        "",
        "## Per-model breakdown",
        "",
        "See `run10_corrective_results.json` for per-model dimensional weights",
        "for every pair-model cell.",
        "",
        "## Verdicts",
        "",
        "(populate manually after reviewing the deltas)",
        "",
        "- **VkusVill**: ",
        "- **Calbee**: ",
        "- **Roshen**: ",
        "",
    ]

    OUT_SUMMARY.write_text("\n".join(lines))
    print(f"Wrote {OUT_SUMMARY}")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Run 10 corrective comparators experiment")
    parser.add_argument("--demo", action="store_true", help="Offline dry run (no API calls)")
    parser.add_argument("--smoke", action="store_true", help="1 pair × all models × 1 run")
    parser.add_argument("--live", action="store_true", help="Full experiment")
    parser.add_argument("--runs", type=int, default=3, help="Repetitions per pair-model cell")
    parser.add_argument("--analyze-only", action="store_true",
                        help="Skip API calls; re-aggregate results from existing JSONL log")
    args = parser.parse_args()

    if not (args.demo or args.smoke or args.live or args.analyze_only):
        parser.print_help()
        sys.exit(1)

    L3_DIR.mkdir(parents=True, exist_ok=True)
    L4_DIR.mkdir(parents=True, exist_ok=True)

    if not args.analyze_only:
        # Decide which pairs to run
        if args.smoke:
            pairs_to_run = CORRECTIVE_PAIRS[:1]
            n_runs = 1
        else:
            pairs_to_run = CORRECTIVE_PAIRS
            n_runs = args.runs

        print(f"Run 10 — Corrective Comparators")
        print(f"Pairs: {len(pairs_to_run)} | Models: {len(MODEL_PANEL)} | Runs per cell: {n_runs}")
        print(f"Estimated calls: {len(pairs_to_run) * len(MODEL_PANEL) * n_runs * 5}")
        print(f"Output log: {OUT_LOG}")

        if args.demo:
            print("DEMO mode — no API calls will be made.")
            for pair in pairs_to_run:
                for model in MODEL_PANEL:
                    for run in range(1, n_runs + 1):
                        print(f"  [DEMO] {pair.id} × {model} × run {run}")
            return

        # Live execution: hand off to the main R15 script's run_pair function
        # which writes JSONL records in the same schema as Runs 2-9.
        # This guarantees schema compatibility with validate.py and the
        # existing aggregation scripts.
        records_written = 0
        with OUT_LOG.open("w") as fh:
            for pair in pairs_to_run:
                for model_name in MODEL_PANEL:
                    if model_name not in asm.API_CALLERS:
                        print(f"  SKIP: {model_name} not in API_CALLERS")
                        continue
                    # Skip if API key missing for cloud models
                    key_var = asm.API_KEY_VARS.get(model_name)
                    if key_var and key_var not in os.environ and "local" not in model_name:
                        print(f"  SKIP: {model_name} ({key_var} not set)")
                        continue
                    for run in range(1, n_runs + 1):
                        try:
                            # asm.run_pair returns a list of session records
                            recs = asm.run_pair(pair, model_name, run)
                            for r in recs:
                                fh.write(json.dumps(r) + "\n")
                                records_written += 1
                            print(f"  OK: {pair.id} × {model_name} × run {run} ({len(recs)} records)")
                        except Exception as exc:
                            print(f"  ERROR: {pair.id} × {model_name} × run {run}: {exc}")

        print(f"Wrote {records_written} records to {OUT_LOG}")

    # Aggregation phase
    if not OUT_LOG.exists():
        print(f"ERROR: {OUT_LOG} does not exist; nothing to aggregate.")
        sys.exit(1)

    records = []
    with OUT_LOG.open() as fh:
        for line in fh:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    pairs_results = {}
    for pair in CORRECTIVE_PAIRS:
        pairs_results[pair.id] = aggregate_pair_profile(records, pair.id)

    results = {
        "schema_version": "1.0",
        "run_id": "run10_corrective",
        "description": "Corrective comparators experiment — 3 focal brands × 2 conditions",
        "n_pairs": len(CORRECTIVE_PAIRS),
        "models": MODEL_PANEL,
        "pairs": pairs_results,
        "comparison_groups": [
            {
                "focal_brand": focal,
                "control_pair": control_id,
                "corrective_pair": corrective_id,
            }
            for focal, control_id, corrective_id in COMPARISON_PAIRS
        ],
    }
    OUT_RESULTS.write_text(json.dumps(results, indent=2, default=float))
    print(f"Wrote {OUT_RESULTS}")

    write_summary(results)


if __name__ == "__main__":
    main()
