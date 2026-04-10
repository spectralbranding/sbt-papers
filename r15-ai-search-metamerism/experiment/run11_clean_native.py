#!/usr/bin/env python3
"""Run 11 -- Clean Native-Language Re-Test.

Re-runs the R15 native-language experiments with FULLY-LOCALIZED prompts:
native instructions PLUS native brand names, native city names, native
category labels, and native product descriptors. JSON output keys stay
English (documented mechanical parsing constraint); field values
including the reasoning text are produced in the target language by the
model.

This replaces the R15 "dirty native" prompts documented in paper
Section 4.5 -- those wrapped native instructions around English brand
and city tokens. Run 11 is the clean test that the original H10 design
never performed.

Design: clean-only. No within-experiment paired comparison against the
dirty data -- the dirty records in Runs 5/6/7/7d/8 serve as the control;
the Run 11 clean records serve as the treatment. Paired t-tests on DCI
are computed at analysis time (L4_analysis/run11_h10_recalc.py).

Output: experiment/L3_sessions/run11_clean_native.jsonl with prompt_type
values "weighted_recommendation_clean_native" and
"geopolitical_framing_clean_native". These are new prompt_types the
extract_rendered_prompts.py script will pick up automatically, so the
L2_prompts/rendered/example_*_clean_native.txt files are generated from
this run's data.

Usage:
    cd experiment
    .venv/bin/python run11_clean_native.py --demo    # offline
    .venv/bin/python run11_clean_native.py --smoke   # 1 cell x 6 models x 1 run
    .venv/bin/python run11_clean_native.py --live    # full experiment
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import ai_search_metamerism as asm  # noqa: E402

EXPERIMENT_DIR = Path(__file__).resolve().parent
L1_DIR = EXPERIMENT_DIR / "L1_configuration"
L3_DIR = EXPERIMENT_DIR / "L3_sessions"
L4_DIR = EXPERIMENT_DIR / "L4_analysis"

LOCALIZATION_FILE = L1_DIR / "native_localization.yaml"
OUT_LOG = L3_DIR / "run11_clean_native.jsonl"
OUT_RESULTS = L4_DIR / "run11_clean_native_results.json"
OUT_SUMMARY = L4_DIR / "run11_clean_native_summary.md"

DIMENSIONS = [
    "semiotic", "narrative", "ideological", "experiential",
    "social", "economic", "cultural", "temporal",
]

# ----------------------------------------------------------------------------
# Model panel (Run 10 panel + groq_kimi for Chinese-tradition coverage)
# ----------------------------------------------------------------------------

MODEL_PANEL = [
    "claude",
    "gpt",
    "gemini",
    "deepseek",
    "qwen3_local",
    "gemma4_local",
    "yandexgpt_pro",
    "groq_kimi",
]


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def load_localization() -> dict:
    """Load native_localization.yaml."""
    with LOCALIZATION_FILE.open() as fh:
        return yaml.safe_load(fh)


def build_clean_weighted_prompt(lang: str, loc: dict) -> str:
    """Build a fully-localized weighted_recommendation prompt.

    Uses NATIVE_WEIGHTED_RECOMMENDATION template and fills it with
    localized brand names + localized category. The dim_block is the
    native-language dimension descriptions block.
    """
    template = asm.NATIVE_WEIGHTED_RECOMMENDATION.get(lang)
    if template is None:
        raise ValueError(
            f"No NATIVE_WEIGHTED_RECOMMENDATION template for {lang}"
        )
    dim_block = asm._dim_block_native(lang)
    return template.format(
        category=loc["category"],
        brand_a=loc["brand_a"],
        brand_b=loc["brand_b"],
        dim_block=dim_block,
    )


def build_clean_framing_prompt(
    lang: str,
    loc: dict,
    which_city: str,  # 'a' or 'b'
) -> str:
    """Build a fully-localized geopolitical_framing prompt.

    Uses NATIVE_GEOPOLITICAL_FRAMING template and fills it with:
      - {brand}: the invariable nominative brand name
      - {place}: a grammatically complete prepositional phrase
        ("в Москве", "у Києві", "在斯德哥尔摩", "i Stockholm", ...)
        already including the correct preposition and noun case.
      - {what}: a grammatically complete noun phrase naming the
        purchase target ("шоколада Рошен", "a Volvo car", "一辆沃尔沃汽车",
        ...) in whatever case the template requires at the insertion
        point. This is supplied per (pair, language) in
        native_localization.yaml and is designed to read as natural
        native-speaker prose when substituted into the template.
    """
    template = asm.NATIVE_GEOPOLITICAL_FRAMING.get(lang)
    if template is None:
        raise ValueError(
            f"No NATIVE_GEOPOLITICAL_FRAMING template for {lang}"
        )
    dim_block = asm._dim_block_native(lang)
    place_key = f"place_{which_city}"
    if place_key not in loc:
        raise ValueError(
            f"Localization for {lang} is missing {place_key}; update "
            f"native_localization.yaml"
        )
    if "what" not in loc:
        raise ValueError(
            f"Localization for {lang} is missing 'what' phrase"
        )
    return template.format(
        brand=loc["brand"],
        place=loc[place_key],
        what=loc["what"],
        dim_block=dim_block,
    )


def cell_iter(localization: dict, smoke: bool) -> list[dict]:
    """Yield one dict per (lang, pair, condition) cell.

    A "cell" is a specific (pair_id, language, prompt_type) combination
    that Run 11 will iterate over the model panel for. Each cell
    produces one API call per model per run.
    """
    cells: list[dict] = []
    for pair_id, pair_data in localization.get("pairs", {}).items():
        ptype = pair_data.get("type")
        for lang, loc in pair_data.get("localizations", {}).items():
            if ptype == "framing":
                # One cell per (pair, lang, city). Framing pairs have two
                # cities, and the dirty framing data records both. Clean
                # Run 11 reproduces both cities for the same lang.
                for which in ("a", "b"):
                    cells.append({
                        "pair_id": pair_id,
                        "lang": lang,
                        "prompt_type": "geopolitical_framing_clean_native",
                        "which_city": which,
                        "loc": loc,
                        "pair_data": pair_data,
                    })
            elif ptype == "weighted":
                cells.append({
                    "pair_id": pair_id,
                    "lang": lang,
                    "prompt_type": "weighted_recommendation_clean_native",
                    "which_city": None,
                    "loc": loc,
                    "pair_data": pair_data,
                })
    if smoke:
        cells = cells[:1]
    return cells


def select_models() -> list[str]:
    """Return the subset of MODEL_PANEL with valid credentials."""
    valid: list[str] = []
    for model in MODEL_PANEL:
        if model not in asm.API_CALLERS:
            print(f"  SKIP: {model} not in API_CALLERS")
            continue
        key_var = asm.API_KEY_VARS.get(model)
        if key_var and "local" not in model and key_var not in os.environ:
            print(f"  SKIP: {model} ({key_var} not set)")
            continue
        valid.append(model)
    return valid


def run_cell(
    cell: dict,
    models: list[str],
    n_runs: int,
    out_fh: Any,
) -> int:
    """Call every model for this cell n_runs times; write JSONL records."""
    if cell["prompt_type"] == "weighted_recommendation_clean_native":
        prompt_text = build_clean_weighted_prompt(cell["lang"], cell["loc"])
        pair_label = f"{cell['loc']['brand_a']} vs {cell['loc']['brand_b']}"
    else:
        prompt_text = build_clean_framing_prompt(
            cell["lang"], cell["loc"], cell["which_city"]
        )
        place_label = cell["loc"].get(f"place_{cell['which_city']}", "")
        pair_label = f"{cell['loc']['brand']}@{place_label}"

    written = 0
    for model in models:
        caller = asm.API_CALLERS[model]
        for run_idx in range(1, n_runs + 1):
            print(
                f"  cell={cell['pair_id']}[{cell['lang']}"
                f"{('/' + cell['which_city']) if cell['which_city'] else ''}] "
                f"model={model} run={run_idx}"
            )
            log_ctx = {
                "prompt_type": cell["prompt_type"],
                "brand_pair": pair_label,
                "pair_id": cell["pair_id"],
                "dimension": None,
                "brand": None,
                "run": run_idx,
                "prompt_language": cell["lang"],
            }
            t0 = time.monotonic()
            try:
                raw = asm.call_with_retry(
                    caller, prompt_text, model,
                    log_path=str(OUT_LOG),
                    log_context=log_ctx,
                )
                latency_ms = int((time.monotonic() - t0) * 1000)
                try:
                    parsed = asm.parse_llm_json(raw)
                except Exception:
                    parsed = {}
                record = {
                    "model": model,
                    "brand_pair": pair_label,
                    "pair_id": cell["pair_id"],
                    "prompt_type": cell["prompt_type"],
                    "dimension": None,
                    "brand": None,
                    "run": run_idx,
                    "response": raw,
                    "parsed": parsed,
                    "timestamp": datetime.datetime.now(
                        datetime.timezone.utc
                    ).isoformat(),
                    "latency_ms": latency_ms,
                    "prompt_language": cell["lang"],
                    "prompt": prompt_text,
                }
                written += 1
            except Exception as exc:
                print(f"    [error] {model}: {exc}")
                # Still write a failure record so the JSONL has a full
                # grid for the statistical comparison.
                record = {
                    "model": model,
                    "brand_pair": pair_label,
                    "pair_id": cell["pair_id"],
                    "prompt_type": cell["prompt_type"],
                    "dimension": None,
                    "brand": None,
                    "run": run_idx,
                    "response": "",
                    "parsed": {},
                    "timestamp": datetime.datetime.now(
                        datetime.timezone.utc
                    ).isoformat(),
                    "latency_ms": 0,
                    "prompt_language": cell["lang"],
                    "prompt": prompt_text,
                    "error": str(exc),
                }
            out_fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            out_fh.flush()
    return written


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run 11 clean-native-language re-test"
    )
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()

    if not (args.demo or args.smoke or args.live):
        parser.print_help()
        sys.exit(0)

    loc_data = load_localization()
    cells = cell_iter(loc_data, smoke=args.smoke)
    n_runs = 1 if args.smoke else args.runs
    models = select_models() if not args.demo else MODEL_PANEL

    print("Run 11 -- Clean Native-Language Re-Test")
    print(f"Cells: {len(cells)} | Models: {len(models)} | Runs per cell: {n_runs}")
    print(f"Estimated calls: {len(cells) * len(models) * n_runs}")
    print(f"Output log: {OUT_LOG}")

    if args.demo:
        print("DEMO mode -- no API calls.")
        for cell in cells:
            which = f"/{cell['which_city']}" if cell["which_city"] else ""
            print(
                f"  [DEMO] {cell['pair_id']}[{cell['lang']}{which}] "
                f"{cell['prompt_type']}"
            )
        return

    # Clear the log before re-running.
    if OUT_LOG.exists():
        OUT_LOG.unlink()

    total_written = 0
    with OUT_LOG.open("w") as out_fh:
        for cell in cells:
            total_written += run_cell(cell, models, n_runs, out_fh)

    print(f"Wrote {total_written} records to {OUT_LOG}")

    # Minimal aggregation: count records per (pair, lang, model) cell.
    summary_lines = [
        "# Run 11 -- Clean Native-Language Re-Test",
        "",
        f"Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}",
        "",
        f"Cells: {len(cells)} | Models: {len(models)} | "
        f"Runs per cell: {n_runs} | Records: {total_written}",
        "",
        "Full per-cell DCI analysis: see run11_h10_recalc.py (to be "
        "written in a follow-up step). This file is the session log "
        "only.",
        "",
    ]
    OUT_SUMMARY.write_text("\n".join(summary_lines))
    print(f"Wrote {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
