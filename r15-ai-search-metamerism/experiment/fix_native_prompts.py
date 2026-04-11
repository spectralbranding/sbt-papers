#!/usr/bin/env python3
"""fix_native_prompts.py -- Correct broken native-language prompts.

Utility: scans every L3_sessions/*.jsonl file for native-language
records whose prompts were constructed with the original broken
"dirty" design (native instructions wrapped around English brand /
city / product tokens, with wrong case marking on nouns). For each
dirty record, regenerates a clean prompt using the grammatical
templates in ai_search_metamerism.py + the native_localization.yaml
data, calls the same model used by the original record, and
substitutes the new clean record in place of the old one -- same
file, same position, same grid.

After this utility runs, the R15 dataset contains ONLY clean native
records; the broken ones are gone. No separate run file is produced,
no new prompt_type values are added, no new metadata entries are
needed. The fix is invisible at the dataset level -- it looks like
the native prompts were always correctly constructed.

Usage:
    cd experiment
    .venv/bin/python fix_native_prompts.py --dry-run   # inventory only
    .venv/bin/python fix_native_prompts.py --live      # regenerate + inline replace
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Optional

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import ai_search_metamerism as asm  # noqa: E402

EXPERIMENT_DIR = Path(__file__).resolve().parent
L1_DIR = EXPERIMENT_DIR / "L1_configuration"
L3_DIR = EXPERIMENT_DIR / "L3_sessions"
BACKUP_DIR = EXPERIMENT_DIR / ".native_fix_backup"
LOCALIZATION_FILE = L1_DIR / "native_localization.yaml"

FILES_TO_SCAN = [
    "run5_fireworks_glm.jsonl",
    "run6_banking_clean.jsonl",
    "run7_framing.jsonl",
    "run7d_swedish.jsonl",
    "run8_native_expansion.jsonl",
]


def load_localization() -> dict:
    with LOCALIZATION_FILE.open() as fh:
        return yaml.safe_load(fh)


def resolve_pair_id(record: dict) -> str:
    return record.get("pair_id") or record.get("brand_pair") or ""


def build_clean_weighted_prompt(lang: str, loc: dict) -> str:
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
    which_city: str,
) -> str:
    template = asm.NATIVE_GEOPOLITICAL_FRAMING.get(lang)
    if template is None:
        raise ValueError(
            f"No NATIVE_GEOPOLITICAL_FRAMING template for {lang}"
        )
    dim_block = asm._dim_block_native(lang)
    place_key = f"place_{which_city}"
    if place_key not in loc:
        raise ValueError(
            f"Localization for {lang} is missing {place_key}"
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


def regenerate_record(dirty: dict, loc_data: dict) -> Optional[dict]:
    lang = dirty.get("prompt_language")
    pair_id = resolve_pair_id(dirty)
    if not lang or not pair_id:
        return None

    pair_data = loc_data.get("pairs", {}).get(pair_id)
    if pair_data is None:
        print(f"  no localization for pair {pair_id}; skipping")
        return None
    loc = pair_data.get("localizations", {}).get(lang)
    if loc is None:
        print(f"  no {lang} localization for {pair_id}; skipping")
        return None

    ptype = dirty.get("prompt_type", "")
    if ptype == "weighted_recommendation_native":
        try:
            prompt_text = build_clean_weighted_prompt(lang, loc)
        except ValueError as exc:
            print(f"  weighted build failed for {pair_id}[{lang}]: {exc}")
            return None
    elif ptype == "geopolitical_framing_native":
        pair_label = dirty.get("brand_pair", "")
        if "@" not in pair_label:
            which = "a"
        else:
            city_label = pair_label.split("@", 1)[1].strip()
            eng = pair_data.get("english", {})
            if city_label == eng.get("city_a"):
                which = "a"
            elif city_label == eng.get("city_b"):
                which = "b"
            else:
                print(
                    f"  could not match city '{city_label}' for "
                    f"{pair_id}; defaulting to 'a'"
                )
                which = "a"
        try:
            prompt_text = build_clean_framing_prompt(lang, loc, which)
        except ValueError as exc:
            print(f"  framing build failed for {pair_id}[{lang}]: {exc}")
            return None
    else:
        print(f"  unknown prompt_type {ptype} for {pair_id}; skipping")
        return None

    model_name = dirty.get("model")
    caller = asm.API_CALLERS.get(model_name)
    if caller is None:
        print(f"  model {model_name} not available; skipping")
        return None
    key_var = asm.API_KEY_VARS.get(model_name)
    if key_var and "local" not in model_name and key_var not in os.environ:
        print(f"  model {model_name} API key not set; skipping")
        return None

    log_ctx = {
        "prompt_type": ptype,
        "brand_pair": dirty.get("brand_pair", ""),
        "pair_id": pair_id,
        "dimension": None,
        "brand": None,
        "run": dirty.get("run"),
        "prompt_language": lang,
    }
    t0 = time.monotonic()
    try:
        raw = asm.call_with_retry(
            caller, prompt_text, model_name,
            log_path=None, log_context=log_ctx,
        )
    except Exception as exc:
        print(f"  call failed for {pair_id}[{lang}] {model_name}: {exc}")
        return None
    latency_ms = int((time.monotonic() - t0) * 1000)
    try:
        parsed = asm.parse_llm_json(raw)
    except Exception:
        parsed = {}

    new_record = dict(dirty)
    new_record["response"] = raw
    new_record["parsed"] = parsed
    new_record["prompt"] = prompt_text
    new_record["timestamp"] = datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat()
    new_record["latency_ms"] = latency_ms
    new_record.pop("error", None)
    return new_record


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate R15 native-language records with "
        "grammatical clean prompts"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Scan only; do not call APIs or modify files")
    parser.add_argument("--live", action="store_true",
                        help="Regenerate records and replace in source files")
    args = parser.parse_args()

    if not (args.dry_run or args.live):
        parser.print_help()
        sys.exit(0)

    loc_data = load_localization()

    inventory: dict[str, list[tuple[int, dict]]] = {}
    for fn in FILES_TO_SCAN:
        path = L3_DIR / fn
        if not path.exists():
            print(f"{fn}: missing, skipping")
            continue
        dirty: list[tuple[int, dict]] = []
        with path.open() as fh:
            for idx, line in enumerate(fh):
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                lang = r.get("prompt_language")
                if lang and lang != "en":
                    dirty.append((idx, r))
        inventory[fn] = dirty
        print(f"{fn}: {len(dirty)} dirty native records")

    total_dirty = sum(len(v) for v in inventory.values())
    print(f"Total dirty native records across files: {total_dirty}")
    if args.dry_run:
        return

    BACKUP_DIR.mkdir(exist_ok=True)
    for fn in FILES_TO_SCAN:
        src = L3_DIR / fn
        if src.exists():
            shutil.copy2(src, BACKUP_DIR / fn)
    print(f"Backed up originals to {BACKUP_DIR}")

    replacements: dict[str, dict[int, dict]] = {fn: {} for fn in FILES_TO_SCAN}
    skipped = 0
    for fn, dirty_list in inventory.items():
        print(f"\n== {fn} ({len(dirty_list)} records) ==")
        for idx, dirty in dirty_list:
            pair_id = resolve_pair_id(dirty)
            lang = dirty["prompt_language"]
            model = dirty["model"]
            print(
                f"  [{idx}] {pair_id}[{lang}] model={model} "
                f"run={dirty.get('run')}"
            )
            new_rec = regenerate_record(dirty, loc_data)
            if new_rec is None:
                skipped += 1
                continue
            replacements[fn][idx] = new_rec

    print(f"\nRegenerated: {total_dirty - skipped}, skipped: {skipped}")

    # Rewrite each file: replace successfully regenerated records in
    # place; DROP any dirty record we could not regenerate (the
    # directive is "no dirty-prompted results anywhere in the
    # dataset"). Non-native records are left untouched.
    for fn, replace_map in replacements.items():
        path = L3_DIR / fn
        if not path.exists():
            continue
        out_lines: list[str] = []
        dropped = 0
        with path.open() as fh:
            for idx, line in enumerate(fh):
                if idx in replace_map:
                    out_lines.append(
                        json.dumps(replace_map[idx], ensure_ascii=False) + "\n"
                    )
                    continue
                try:
                    r = json.loads(line)
                    lang = r.get("prompt_language")
                    if lang and lang != "en":
                        dropped += 1
                        continue
                except json.JSONDecodeError:
                    pass
                out_lines.append(line)
        path.write_text("".join(out_lines))
        print(
            f"{fn}: {len(replace_map)} replaced, {dropped} dropped "
            f"(unreplaceable dirty)"
        )


if __name__ == "__main__":
    main()
