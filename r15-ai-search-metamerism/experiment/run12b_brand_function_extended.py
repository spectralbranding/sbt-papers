#!/usr/bin/env python3
"""Run 12 — Brand Function Specification Test.

Tests whether providing a Brand Function JSON specification in the LLM
prompt context reduces the Dimensional Collapse Index (DCI) compared to
the unspecified baseline.

HYPOTHESIS

H_BF: DCI(with_spec) < DCI(without_spec) for each brand, with paired
      t-test across the model panel.

DESIGN

Two conditions for each of the 5 canonical SBT brands:
  1. BASELINE: standard R15 weighted_recommendation prompt (no spec)
  2. SPECIFIED: same prompt, prefixed with Brand Function JSON

The baseline condition replicates Runs 2-4 methodology on the same
brand pairs. The specified condition adds the Brand Function JSON to
the system prompt before the standard R15 prompt.

BRANDS AND PAIRS (same as R15 Runs 2-4 global pairs)

| Brand      | Comparator      | Category           |
|------------|----------------|--------------------|
| Hermes     | Louis Vuitton  | luxury fashion     |
| IKEA       | West Elm       | home furnishings   |
| Patagonia  | The North Face | outdoor apparel    |
| Erewhon    | Whole Foods    | premium grocery    |
| Tesla      | Rivian         | electric vehicles  |

MODEL PANEL (cloud only — Ollama may be occupied by parallel sessions)

1. claude      — Claude Sonnet 4.6      (Anthropic, Western, paid)
2. gpt         — GPT-4o-mini            (OpenAI, Western, paid)
3. gemini      — Gemini 2.5 Flash       (Google, Western, paid)
4. deepseek    — DeepSeek V3            (DeepSeek, Chinese, paid)

Optional extension (when Ollama available):
5. qwen3_local  — Qwen3 30B             (local)
6. gemma4_local — Gemma 4 27B           (local)

RUNS: 3 per condition per brand per model.

VOLUME:
  Cloud only: 5 brands × 4 models × 2 conditions × 3 runs = 120 calls
  With local: 5 brands × 6 models × 2 conditions × 3 runs = 180 calls

COST: ~$0.10-0.20 (weighted_rec_only, short prompts)

OUTPUT

L3_sessions/run12_brand_function.jsonl  — raw session log
L4_analysis/run12_brand_function_results.json — aggregated results
L4_analysis/run12_brand_function_summary.md   — human-readable report

USAGE

    cd experiment
    python run12_brand_function.py --demo     # offline dry run
    python run12_brand_function.py --smoke    # 1 brand × 1 model × 1 run × 2 conditions
    python run12_brand_function.py --live     # full cloud experiment
    python run12_brand_function.py --live --local  # full experiment including Ollama models

Requires env vars: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY,
DEEPSEEK_API_KEY. Local models require Ollama with qwen3:30b and
gemma4:latest pulled.

PRE-REGISTRATION: L0_specification/PRE_REGISTRATION_RUN12.md
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

sys.path.insert(0, str(Path(__file__).parent))
import ai_search_metamerism as asm  # noqa: E402

EXPERIMENT_DIR = Path(__file__).resolve().parent
L1_DIR = EXPERIMENT_DIR / "L1_configuration" / "brand_functions"
L3_DIR = EXPERIMENT_DIR / "L3_sessions"
L4_DIR = EXPERIMENT_DIR / "L4_analysis"
OUT_LOG = L3_DIR / "run12b_brand_function_extended.jsonl"
OUT_RESULTS = L4_DIR / "run12b_brand_function_extended_results.json"
OUT_SUMMARY = L4_DIR / "run12b_brand_function_extended_summary.md"

DIMENSIONS = [
    "semiotic", "narrative", "ideological", "experiential",
    "social", "economic", "cultural", "temporal",
]
BASELINE_DCI = 12.5  # equal weighting across 8 dimensions = 100/8


# ── Brand pairs ───────────────────────────────────────────────────────────────

BRAND_PAIRS: list[asm.BrandPair] = [
    # ── Run 12 original (5 canonical SBT brands) ──────────────────────────
    asm.BrandPair(id="hermes_vs_louis_vuitton", brand_a="Hermes", brand_b="Louis Vuitton",
        category="luxury fashion house", differentiating_dims=["economic", "social", "temporal"], dim_type="hard",
        description="Canonical. Hermes: dark signal, scarcity. LV: visible luxury, volume."),
    asm.BrandPair(id="ikea_vs_west_elm", brand_a="IKEA", brand_b="West Elm",
        category="home furnishings", differentiating_dims=["economic", "experiential", "narrative"], dim_type="mixed",
        description="Canonical. IKEA: democratic design. West Elm: premium casual."),
    asm.BrandPair(id="patagonia_vs_north_face", brand_a="Patagonia", brand_b="The North Face",
        category="outdoor apparel and gear", differentiating_dims=["ideological", "narrative", "temporal"], dim_type="soft",
        description="Canonical. Patagonia: activism core. TNF: performance + lifestyle."),
    asm.BrandPair(id="erewhon_vs_whole_foods", brand_a="Erewhon", brand_b="Whole Foods Market",
        category="premium organic grocery", differentiating_dims=["social", "experiential", "economic"], dim_type="mixed",
        description="Canonical. Erewhon: LA wellness culture. WF: mainstream organic."),
    asm.BrandPair(id="tesla_vs_rivian", brand_a="Tesla", brand_b="Rivian",
        category="electric vehicle manufacturer", differentiating_dims=["narrative", "ideological", "social"], dim_type="soft",
        description="Canonical. Tesla: disruptor narrative. Rivian: adventure EV."),
    # ── Registry brands (global) ──────────────────────────────────────────
    asm.BrandPair(id="nike_vs_adidas", brand_a="Nike", brand_b="Adidas",
        category="athletic footwear and apparel", differentiating_dims=["narrative", "cultural", "semiotic"], dim_type="mixed",
        description="Sports/fashion. Nike: Just Do It, athlete endorsements. Adidas: European football heritage."),
    asm.BrandPair(id="apple_vs_samsung", brand_a="Apple", brand_b="Samsung",
        category="consumer electronics", differentiating_dims=["semiotic", "experiential", "cultural"], dim_type="hard",
        description="Tech. Apple: ecosystem + design. Samsung: breadth + display tech."),
    asm.BrandPair(id="starbucks_vs_dunkin", brand_a="Starbucks", brand_b="Dunkin'",
        category="coffee chain", differentiating_dims=["experiential", "social", "cultural"], dim_type="mixed",
        description="Coffee. Starbucks: third place. Dunkin: speed + value."),
    asm.BrandPair(id="coca_cola_vs_pepsi", brand_a="Coca-Cola", brand_b="Pepsi",
        category="carbonated soft drink", differentiating_dims=["cultural", "temporal", "narrative"], dim_type="soft",
        description="Beverage. Coca-Cola: 1886 heritage, Americana. Pepsi: youth, generation."),
    asm.BrandPair(id="mercedes_vs_bmw", brand_a="Mercedes-Benz", brand_b="BMW",
        category="luxury automobile", differentiating_dims=["narrative", "experiential", "temporal"], dim_type="mixed",
        description="Luxury auto. Mercedes: invented the car, 1886. BMW: driving machine, sport."),
    asm.BrandPair(id="zara_vs_hm", brand_a="Zara", brand_b="H&M",
        category="fast fashion retail", differentiating_dims=["experiential", "cultural", "economic"], dim_type="mixed",
        description="Fast fashion. Zara: speed-to-rack, European. H&M: collaborations, Scandinavian."),
    asm.BrandPair(id="rolex_vs_omega", brand_a="Rolex", brand_b="Omega",
        category="luxury watches", differentiating_dims=["social", "temporal", "narrative"], dim_type="hard",
        description="Luxury watches. Rolex: status symbol. Omega: space/Bond heritage."),
    asm.BrandPair(id="netflix_vs_disney_plus", brand_a="Netflix", brand_b="Disney+",
        category="streaming entertainment", differentiating_dims=["cultural", "narrative", "temporal"], dim_type="soft",
        description="Streaming. Netflix: algorithm + originals. Disney+: IP vault, family."),
    asm.BrandPair(id="lululemon_vs_gymshark", brand_a="Lululemon", brand_b="Gymshark",
        category="athleisure apparel", differentiating_dims=["experiential", "social", "economic"], dim_type="mixed",
        description="Athleisure. Lululemon: yoga community, premium. Gymshark: fitness influencers, DTC."),
    asm.BrandPair(id="trader_joes_vs_aldi", brand_a="Trader Joe's", brand_b="Aldi",
        category="value grocery chain", differentiating_dims=["experiential", "narrative", "cultural"], dim_type="soft",
        description="Value grocery. TJ: treasure hunt, quirky. Aldi: German efficiency, no-frills."),
    # ── R15/R10 comparators as focal brands ───────────────────────────────
    asm.BrandPair(id="louis_vuitton_vs_gucci", brand_a="Louis Vuitton", brand_b="Gucci",
        category="luxury fashion house", differentiating_dims=["semiotic", "cultural", "narrative"], dim_type="soft",
        description="Luxury. LV: monogram, French trunk heritage. Gucci: Italian maximalism."),
    asm.BrandPair(id="north_face_vs_columbia", brand_a="The North Face", brand_b="Columbia",
        category="outdoor apparel", differentiating_dims=["semiotic", "experiential", "economic"], dim_type="mixed",
        description="Outdoor. TNF: mountaineering + streetwear. Columbia: family outdoor, value."),
    asm.BrandPair(id="whole_foods_vs_sprouts", brand_a="Whole Foods Market", brand_b="Sprouts Farmers Market",
        category="natural and organic grocery", differentiating_dims=["economic", "experiential", "social"], dim_type="mixed",
        description="Organic grocery. WF: premium, Amazon. Sprouts: farmers market feel, value."),
    asm.BrandPair(id="rivian_vs_lucid", brand_a="Rivian", brand_b="Lucid Motors",
        category="electric vehicle startup", differentiating_dims=["narrative", "experiential", "ideological"], dim_type="soft",
        description="EV startup. Rivian: adventure. Lucid: luxury sedan, ex-Tesla engineering."),
    asm.BrandPair(id="dove_vs_nivea", brand_a="Dove", brand_b="Nivea",
        category="personal care", differentiating_dims=["ideological", "narrative", "cultural"], dim_type="soft",
        description="Personal care. Dove: Real Beauty, body positivity. Nivea: family care, trust."),
    # ── Regional brands ───────────────────────────────────────────────────
    asm.BrandPair(id="toyota_vs_honda", brand_a="Toyota", brand_b="Honda",
        category="automobile manufacturer", differentiating_dims=["narrative", "cultural", "economic"], dim_type="mixed",
        description="Japan auto. Toyota: TPS, reliability. Honda: engineering, motorcycle heritage."),
    asm.BrandPair(id="samsung_vs_lg", brand_a="Samsung", brand_b="LG",
        category="consumer electronics and appliances", differentiating_dims=["semiotic", "experiential", "economic"], dim_type="mixed",
        description="Korea tech. Samsung: Galaxy premium. LG: appliances + value electronics."),
    asm.BrandPair(id="huawei_vs_xiaomi", brand_a="Huawei", brand_b="Xiaomi",
        category="smartphone and technology", differentiating_dims=["narrative", "ideological", "cultural"], dim_type="soft",
        description="China tech. Huawei: sanctions resilience, sovereignty. Xiaomi: value disruption, Mi ecosystem."),
    asm.BrandPair(id="volvo_vs_audi", brand_a="Volvo", brand_b="Audi",
        category="premium automobile", differentiating_dims=["ideological", "cultural", "narrative"], dim_type="soft",
        description="European premium. Volvo: safety + Swedish values. Audi: Vorsprung, German tech."),
    asm.BrandPair(id="uniqlo_vs_muji", brand_a="Uniqlo", brand_b="Muji",
        category="Japanese minimalist retail", differentiating_dims=["semiotic", "cultural", "economic"], dim_type="mixed",
        description="Japan minimal. Uniqlo: LifeWear basics. Muji: no-brand, anti-branding."),
    asm.BrandPair(id="emirates_vs_qatar", brand_a="Emirates", brand_b="Qatar Airways",
        category="premium airline", differentiating_dims=["experiential", "cultural", "economic"], dim_type="mixed",
        description="Gulf aviation. Emirates: A380 bar, Dubai hub. Qatar: Qsuite, Doha hub."),
]


# ── Model panels ──────────────────────────────────────────────────────────────

CLOUD_MODELS = [
    "claude",
    "gpt",
    "gemini",
    "deepseek",
]

LOCAL_MODELS = [
    "qwen3_local",
    "gemma4_local",
]


# ── Brand Function loader ─────────────────────────────────────────────────────

def load_brand_function(brand_name: str) -> dict:
    """Load the Brand Function JSON for a given brand."""
    slug = brand_name.lower().replace(" ", "_").replace("-", "_").replace("the_", "").replace("'", "")
    path = L1_DIR / f"{slug}.json"
    if not path.exists():
        raise FileNotFoundError(f"Brand Function not found: {path}")
    with open(path) as f:
        return json.load(f)


def format_brand_function_prompt(bf: dict) -> str:
    """Format a Brand Function as a system prompt prefix."""
    lines = [
        f"BRAND SPECIFICATION: {bf['brand']}",
        f"(Source: {bf.get('source', 'Canonical SBT brand profile')})",
        "",
    ]
    for dim_name in DIMENSIONS:
        dim_data = bf["dimensions"].get(dim_name, {})
        score = dim_data.get("score", "N/A")
        positioning = dim_data.get("positioning", "")
        signals = dim_data.get("key_signals", [])
        lines.append(f"{dim_name.upper()} ({score}/10): {positioning}")
        if signals:
            lines.append(f"  Signals: {', '.join(signals)}")
    return "\n".join(lines)


# ── Analysis ──────────────────────────────────────────────────────────────────

def parse_weighted_recommendation(record: dict) -> dict[str, float] | None:
    """Extract the 8-dimensional weight vector from a session record."""
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


def compute_dci(weights: dict[str, float]) -> float:
    """Compute DCI from a weight vector. DCI = mean |w_i - 12.5|."""
    return mean(abs(w - BASELINE_DCI) for w in weights.values())


def aggregate_condition(
    records: list[dict], condition: str
) -> dict[str, Any]:
    """Aggregate results for one condition across all brands and models."""
    by_brand: dict[str, dict[str, list[dict[str, float]]]] = {}

    for r in records:
        if r.get("condition") != condition:
            continue
        w = parse_weighted_recommendation(r)
        if w is None:
            continue
        brand = r.get("focal_brand", "unknown")
        model = r.get("model", "unknown")
        by_brand.setdefault(brand, {}).setdefault(model, []).append(w)

    results = {}
    for brand, models in by_brand.items():
        brand_dcis = []
        brand_weights = {d: [] for d in DIMENSIONS}
        for model, weight_list in models.items():
            for w in weight_list:
                dci = compute_dci(w)
                brand_dcis.append(dci)
                for d in DIMENSIONS:
                    brand_weights[d].append(w[d])

        results[brand] = {
            "n_calls": sum(len(wl) for wl in models.values()),
            "n_models": len(models),
            "mean_dci": round(mean(brand_dcis), 3) if brand_dcis else None,
            "sd_dci": round(stdev(brand_dcis), 3) if len(brand_dcis) > 1 else None,
            "mean_weights": {
                d: round(mean(brand_weights[d]), 2) if brand_weights[d] else None
                for d in DIMENSIONS
            },
        }

    return results


# ── Experiment runner ─────────────────────────────────────────────────────────

def build_rec_prompt(pair: asm.BrandPair) -> str:
    """Build the standard R15 weighted_recommendation prompt for a pair."""
    dim_block = asm._dim_block()
    return asm.WEIGHTED_RECOMMENDATION_PROMPT.format(
        category=pair.category,
        brand_a=pair.brand_a,
        brand_b=pair.brand_b,
        dim_block=dim_block,
    )


def run_experiment(
    model_list: list[str],
    n_runs: int = 3,
    demo: bool = False,
) -> list[dict]:
    """Run the full Brand Function specification test.

    For each (brand, model, run), makes TWO API calls:
    1. Baseline: standard R15 weighted_recommendation prompt
    2. Specified: Brand Function text + standard prompt

    Uses asm.API_CALLERS directly (same functions as R15 Runs 2-11).
    """
    all_records: list[dict] = []
    done = 0
    total = len(BRAND_PAIRS) * len(model_list) * n_runs * 2  # 2 conditions

    for pair in BRAND_PAIRS:
        focal_brand = pair.brand_a
        pair_label = f"{pair.brand_a} vs {pair.brand_b}"
        bf = load_brand_function(focal_brand)
        bf_text = format_brand_function_prompt(bf)
        rec_prompt = build_rec_prompt(pair)

        # Specified prompt: Brand Function context + standard prompt
        spec_prefix = (
            f"You have access to the following verified brand specification "
            f"for {focal_brand}. Use this information when evaluating the brand.\n\n"
            f"{bf_text}\n\n---\n\n"
        )
        spec_prompt = spec_prefix + rec_prompt

        for model_key in model_list:
            if model_key not in asm.API_CALLERS:
                print(f"  SKIP: {model_key} not in API_CALLERS")
                continue
            key_var = asm.API_KEY_VARS.get(model_key)
            if key_var and "local" not in model_key and key_var not in os.environ:
                print(f"  SKIP: {model_key} ({key_var} not set)")
                continue

            caller = asm.API_CALLERS[model_key]

            for run_idx in range(1, n_runs + 1):
                for condition, prompt in [("baseline", rec_prompt), ("specified", spec_prompt)]:
                    done += 1
                    tag = f"[{done}/{total}] {model_key} run={run_idx} {condition} {focal_brand}"

                    model_id = asm.MODEL_IDS.get(model_key, "unknown")
                    temperature = asm.EXPERIMENT_TEMPERATURE

                    if demo:
                        record = {
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "run_id": "run12_brand_function",
                            "condition": condition,
                            "focal_brand": focal_brand,
                            "pair_id": pair.id,
                            "brand_pair": pair_label,
                            "model": model_key,
                            "model_id": model_id,
                            "temperature": temperature,
                            "run": run_idx,
                            "prompt_type": "weighted_recommendation",
                            "demo": True,
                            "prompt_length": len(prompt),
                        }
                        all_records.append(record)
                        print(f"  [DEMO] {tag} — prompt {len(prompt)} chars")
                        continue

                    print(f"  {tag}", end=" ", flush=True)
                    t0 = time.monotonic()
                    try:
                        raw = asm.call_with_retry(
                            caller, prompt, model_key,
                            log_path=str(OUT_LOG),
                            log_context={
                                "prompt_type": "weighted_recommendation",
                                "brand_pair": pair_label,
                                "pair_id": pair.id,
                                "condition": condition,
                                "focal_brand": focal_brand,
                                "run": run_idx,
                                "run_id": "run12_brand_function",
                            },
                        )
                        latency_ms = int((time.monotonic() - t0) * 1000)

                        parsed: dict[str, Any] = {}
                        try:
                            parsed = asm.parse_llm_json(raw)
                        except Exception:
                            pass

                        record = {
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "run_id": "run12_brand_function",
                            "condition": condition,
                            "focal_brand": focal_brand,
                            "pair_id": pair.id,
                            "brand_pair": pair_label,
                            "model": model_key,
                            "model_id": model_id,
                            "temperature": temperature,
                            "run": run_idx,
                            "prompt_type": "weighted_recommendation",
                            "response": raw[:500] if raw else None,
                            "parsed": parsed,
                            "latency_ms": latency_ms,
                            "prompt_length": len(prompt),
                        }
                        all_records.append(record)

                        # Also append to JSONL directly (call_with_retry
                        # logs its own record, but we add our enriched one)
                        with open(OUT_LOG, "a") as f:
                            f.write(json.dumps(record, default=str) + "\n")

                        w = parse_weighted_recommendation(record)
                        dci = f"DCI={compute_dci(w):.3f}" if w else "PARSE_FAIL"
                        print(f"— {latency_ms}ms {dci}")

                    except Exception as e:
                        latency_ms = int((time.monotonic() - t0) * 1000)
                        record = {
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "run_id": "run12_brand_function",
                            "condition": condition,
                            "focal_brand": focal_brand,
                            "pair_id": pair.id,
                            "brand_pair": pair_label,
                            "model": model_key,
                            "model_id": model_id,
                            "temperature": temperature,
                            "run": run_idx,
                            "prompt_type": "weighted_recommendation",
                            "error": str(e),
                            "latency_ms": latency_ms,
                        }
                        all_records.append(record)
                        with open(OUT_LOG, "a") as f:
                            f.write(json.dumps(record, default=str) + "\n")
                        print(f"— ERROR: {e}")

                    time.sleep(0.5)

    return all_records


# ── Report generation ─────────────────────────────────────────────────────────

def generate_summary(records: list[dict]) -> str:
    """Generate the human-readable summary report."""
    baseline = aggregate_condition(records, "baseline")
    specified = aggregate_condition(records, "specified")

    lines = [
        "# Run 12: Brand Function Specification Test — Summary",
        "",
        f"**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"**Total records**: {len(records)}",
        f"**Conditions**: baseline (no spec), specified (Brand Function in prompt)",
        "",
        "## DCI Comparison by Brand",
        "",
        "| Brand | Baseline DCI | Specified DCI | Delta | Direction |",
        "|-------|-------------|--------------|-------|-----------|",
    ]

    all_baseline_dcis = []
    all_specified_dcis = []

    for brand in [p.brand_a for p in BRAND_PAIRS]:
        b = baseline.get(brand, {})
        s = specified.get(brand, {})
        b_dci = b.get("mean_dci")
        s_dci = s.get("mean_dci")
        if b_dci is not None and s_dci is not None:
            delta = round(s_dci - b_dci, 3)
            direction = "REDUCED" if delta < 0 else "INCREASED" if delta > 0 else "UNCHANGED"
            lines.append(f"| {brand} | {b_dci:.3f} | {s_dci:.3f} | {delta:+.3f} | {direction} |")
            all_baseline_dcis.append(b_dci)
            all_specified_dcis.append(s_dci)
        else:
            lines.append(f"| {brand} | {'N/A' if b_dci is None else f'{b_dci:.3f}'} | {'N/A' if s_dci is None else f'{s_dci:.3f}'} | -- | -- |")

    if all_baseline_dcis and all_specified_dcis:
        overall_b = mean(all_baseline_dcis)
        overall_s = mean(all_specified_dcis)
        overall_delta = overall_s - overall_b
        lines.extend([
            "",
            f"**Overall mean**: baseline {overall_b:.3f}, specified {overall_s:.3f}, delta {overall_delta:+.3f}",
        ])

        # Paired comparison (brand-level means)
        if len(all_baseline_dcis) >= 2:
            from scipy import stats
            t_stat, p_val = stats.ttest_rel(all_baseline_dcis, all_specified_dcis)
            d_pairs = [(b - s) for b, s in zip(all_baseline_dcis, all_specified_dcis)]
            cohens_d = mean(d_pairs) / stdev(d_pairs) if stdev(d_pairs) > 0 else float("inf")
            lines.extend([
                f"**Paired t-test** (N={len(all_baseline_dcis)} brands): t = {t_stat:.3f}, p = {p_val:.3f}",
                f"**Cohen's d**: {cohens_d:.3f}",
                f"**H_BF**: {'SUPPORTED' if p_val < .05 and overall_delta < 0 else 'NOT SUPPORTED'}",
            ])

    # Per-dimension analysis
    lines.extend([
        "",
        "## Per-Dimension Weight Shift (mean across all brands)",
        "",
        "| Dimension | Baseline | Specified | Shift toward 12.5 |",
        "|-----------|----------|-----------|-------------------|",
    ])
    for dim in DIMENSIONS:
        b_vals = [baseline.get(brand, {}).get("mean_weights", {}).get(dim)
                  for brand in [p.brand_a for p in BRAND_PAIRS]]
        s_vals = [specified.get(brand, {}).get("mean_weights", {}).get(dim)
                  for brand in [p.brand_a for p in BRAND_PAIRS]]
        b_vals = [v for v in b_vals if v is not None]
        s_vals = [v for v in s_vals if v is not None]
        if b_vals and s_vals:
            b_mean = mean(b_vals)
            s_mean = mean(s_vals)
            # Shift toward 12.5 = reduction in distance from baseline
            b_dist = abs(b_mean - BASELINE_DCI)
            s_dist = abs(s_mean - BASELINE_DCI)
            shift = b_dist - s_dist  # positive = moved toward baseline
            lines.append(f"| {dim} | {b_mean:.1f} | {s_mean:.1f} | {shift:+.1f} |")

    lines.extend([
        "",
        "---",
        "",
        "*Generated by run12_brand_function.py*",
        f"*Pre-registration: L0_specification/PRE_REGISTRATION_RUN12.md*",
    ])

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Run 12: Brand Function Specification Test")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true", help="Offline dry run (no API calls)")
    mode.add_argument("--smoke", action="store_true", help="1 brand x 1 model x 1 run x 2 conditions")
    mode.add_argument("--live", action="store_true", help="Full experiment")
    parser.add_argument("--local", action="store_true", help="Include local Ollama models")
    args = parser.parse_args()

    L3_DIR.mkdir(parents=True, exist_ok=True)
    L4_DIR.mkdir(parents=True, exist_ok=True)

    models = CLOUD_MODELS[:]
    if args.local:
        models.extend(LOCAL_MODELS)

    n_runs = 3
    if args.smoke:
        # Smoke test: 1 brand, 1 model, 1 run, 2 conditions
        global BRAND_PAIRS
        BRAND_PAIRS = BRAND_PAIRS[:1]  # Hermes only
        models = models[:1]
        n_runs = 1

    print(f"Run 12: Brand Function Specification Test")
    print(f"  Brands: {len(BRAND_PAIRS)}")
    print(f"  Models: {models}")
    print(f"  Runs per condition: {n_runs}")
    print(f"  Conditions: baseline, specified")
    print(f"  Estimated calls: {len(BRAND_PAIRS) * len(models) * 2 * n_runs}")
    print()

    records = run_experiment(models, n_runs, demo=args.demo)

    # Save results
    results = {
        "experiment": "run12_brand_function",
        "date": datetime.now(timezone.utc).isoformat(),
        "n_records": len(records),
        "models": models,
        "brands": [p.brand_a for p in BRAND_PAIRS],
        "baseline": aggregate_condition(records, "baseline"),
        "specified": aggregate_condition(records, "specified"),
    }
    with open(OUT_RESULTS, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {OUT_RESULTS}")

    # Generate summary
    summary = generate_summary(records)
    with open(OUT_SUMMARY, "w") as f:
        f.write(summary)
    print(f"Summary saved to {OUT_SUMMARY}")

    if not args.demo:
        print(f"Raw session log: {OUT_LOG}")


if __name__ == "__main__":
    main()
