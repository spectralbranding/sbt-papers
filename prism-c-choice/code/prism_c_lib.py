#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0", "numpy>=1.26"]
# ///
"""prism_c_lib.py — campaign library for PRISM-C (2026bb, choice-perception gap).

Reuses the shared PRISM machinery (research/prism_core/): 4-family provider
layer + PL3 logging, the frozen PRISM-B stated-reading prompt set (brand
readings AND need-vector elicitation), stats + concordance. Adds the PL2
choice-elicitation prompt battery and the deterministic counterbalancing
scheme.

Config: ../PL1_CONFIG.yaml. Banks: ../PL2_SCENARIO_BANK.yaml (scenarios +
controls) and the REUSED FROZEN ../../prism_m/PL2_BRAND_BANK.yaml (brands).

Keys via `bws run -- <wrapper.sh>`: ANTHROPIC_API_KEY, OPENAI_API_KEY,
DEEPSEEK_API_KEY, DASHSCOPE_API_KEY.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PRISM_C_DIR = HERE.parent
RESEARCH = PRISM_C_DIR.parent
sys.path.insert(0, str(RESEARCH))

from prism_core import prism_b  # noqa: E402
from prism_core.provider import (  # noqa: E402
    append_record,
    call_model,
    load_records,
    parse_json_block,
)

LOGS_DIR = PRISM_C_DIR / "logs"
DATA_DIR = PRISM_C_DIR / "data"

SEED = 20260702
PROMPT_VERSION = "prism-c/v1.0.0"
DIMENSIONS = prism_b.DIMENSIONS


# ---------------------------------------------------------------------------
# Config + banks
# ---------------------------------------------------------------------------
def load_config() -> dict:
    return yaml.safe_load((PRISM_C_DIR / "PL1_CONFIG.yaml").read_text())


def load_scenario_bank() -> dict:
    return yaml.safe_load((PRISM_C_DIR / "PL2_SCENARIO_BANK.yaml").read_text())


def load_brand_bank() -> dict:
    return yaml.safe_load((RESEARCH / "prism_m" / "PL2_BRAND_BANK.yaml").read_text())


def bank_brands(bank: dict) -> list[dict]:
    """Flatten strata to a list of brand dicts with stratum metadata
    (same shape as the 2026az loader)."""
    out = []
    for cell, brands in bank["strata"].items():
        ctype, sector = cell.rsplit("_", 1)
        for b in brands:
            row = dict(b)
            row["coherence_type"] = ctype
            row["sector"] = sector
            out.append(row)
    return out


def brand_lookup(bank: dict) -> dict[str, dict]:
    return {b["brand"]: b for b in bank_brands(bank)}


# ---------------------------------------------------------------------------
# Counterbalancing (PL0 section 9.1) — deterministic, seed-free by design:
# the scheme is a fixed function of the option list, so it is reproducible
# without RNG state. For n options: the n rotations of the base order (each
# option once in first position) followed by the n rotations of the reversed
# order, deduplicated preserving construction order, truncated to
# n_arrangements. n=4 -> exactly 8; n=5 -> 8 of 10 with all-option
# first-position coverage; n=3 -> the full permutation-scheme set of 6;
# n=2 -> the full set of 2 (smaller-than-8 sets use the full scheme set).
# ---------------------------------------------------------------------------
def arrangements(options: list[str], n_arrangements: int = 8) -> list[list[str]]:
    n = len(options)
    base = list(options)
    rev = list(reversed(options))
    pool: list[tuple] = []
    for i in range(n):
        pool.append(tuple(base[i:] + base[:i]))
    for i in range(n):
        pool.append(tuple(rev[i:] + rev[:i]))
    seen, out = set(), []
    for p in pool:
        if p not in seen:
            seen.add(p)
            out.append(list(p))
    return out[:n_arrangements]


# ---------------------------------------------------------------------------
# PL2 prompts — choice elicitation (new) + need-vector renderer (new);
# brand stated readings + all extraction reuse prism_core.prism_b verbatim.
# ---------------------------------------------------------------------------
CHOICE_SYSTEM = (
    "You are a shopping and procurement assistant choosing on behalf of a "
    "client. From the numbered options, choose the ONE brand that best "
    "serves the client's stated need, then rank all options from best to "
    "worst fit. Use only your own knowledge of these brands as they appear "
    "publicly; the client provides no further information and you must not "
    "ask questions. Output JSON only, no code fences, no commentary: "
    '{"pick": "<brand name exactly as listed>", '
    '"ranking": ["<best>", "...", "<worst>"]}.'
)

CHOICE_USER_TMPL = (
    "Client need: {need}\n\nOptions:\n{options_block}\n\nChoose and rank."
)

NEED_RENDERER_SYSTEM = (
    "You are an analyst translating a buyer's stated need into the profile "
    "of the ideal brand for that need. You reason from the stated need "
    "alone. Do not name or allude to any real brand. Write plain analytical "
    "prose. Do not score, rate, or rank; describe."
)

NEED_RENDERER_USER_TMPL = (
    "Buyer need: {need}\n\n"
    "In 150-300 words of analytical prose, describe what the ideal brand "
    "for this need would convey in terms of the buyer's priorities: symbols "
    "and visual identity; story and narrative; values and ideology; "
    "product/service experience; social meaning and community; price/value "
    "positioning; cultural presence; and relationship to time (heritage vs "
    "novelty). Cover each aspect at least briefly, weighting each by how "
    "much it matters for this need."
)


def options_block(arrangement: list[str], descriptors: dict[str, str]) -> str:
    return "\n".join(
        f"{i + 1}. {name} - {descriptors[name]}" for i, name in enumerate(arrangement)
    )


def _norm(s: str) -> str:
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def _match_option(s: str, option_names: list[str]) -> str | None:
    """Map a model-emitted option string onto exactly one listed option.
    Accepts the bare name, the presented 'Name - descriptor' line (models
    routinely echo the option exactly as listed), or an unambiguous prefix
    in either direction; returns None on no match or ambiguity."""
    ns = _norm(s)
    if not ns:
        return None
    exact = {_norm(o): o for o in option_names}.get(ns)
    if exact is not None:
        return exact
    matches = [
        o for o in option_names if ns.startswith(_norm(o)) or _norm(o).startswith(ns)
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        # nested-prefix case: keep the longest option norm iff strictly longest
        matches.sort(key=lambda o: len(_norm(o)), reverse=True)
        if len(_norm(matches[0])) > len(_norm(matches[1])):
            return matches[0]
    return None


def parse_choice(raw: str, option_names: list[str]) -> dict:
    """Parse the chooser's JSON; the pick MUST resolve to exactly one listed
    option (case-insensitive, punctuation-tolerant, descriptor-echo-tolerant
    - the July-2026 pilot showed choosers echo 'Name - descriptor' exactly as
    presented). Ranking is validated leniently (kept only if it maps to a
    permutation of the options)."""
    d = parse_json_block(raw)
    pick = _match_option(d.get("pick", ""), option_names)
    if pick is None:
        raise ValueError(f"pick not among options: {d.get('pick')!r}")
    ranking = None
    r = d.get("ranking")
    if isinstance(r, list):
        mapped = [_match_option(x, option_names) for x in r]
        if None not in mapped and sorted(mapped) == sorted(option_names):
            ranking = mapped
    return {"pick": pick, "ranking": ranking}


# ---------------------------------------------------------------------------
# Measurement wrappers (all calls PL3-logged to ../logs/)
# ---------------------------------------------------------------------------
def measure_stated(
    brand_row: dict, channel: dict, op_id: str, op: dict, *, phase: str, out_path: Path
) -> None:
    """One brand stated reading: PRISM-B render (channel-scoped prose) +
    dims extraction, cross-family pair. Identical instrument to 2026az."""
    user = prism_b.RENDERER_USER_TMPL.format(
        brand=brand_row["brand"],
        category=brand_row["category"],
        channel_desc=channel["description"],
    )
    prose = call_model(
        op["renderer"]["model"],
        op["renderer"]["family"],
        prism_b.RENDERER_SYSTEM,
        user,
        role="renderer",
        operation=f"render_stated_{brand_row['brand']}_{channel['id']}_{op_id}",
        phase=phase,
        logs_dir=LOGS_DIR,
        max_out=1400,
        seed=SEED,
    )
    value = None
    for _ in range(2):  # redraw_once_then_flag
        raw = call_model(
            op["extractor"]["model"],
            op["extractor"]["family"],
            prism_b.EXTRACTOR_SYSTEM,
            prism_b.EXTRACTOR_USER_TMPL.format(prose=prose),
            role="extractor",
            operation=f"extract_stated_{brand_row['brand']}_{channel['id']}_{op_id}",
            phase=phase,
            logs_dir=LOGS_DIR,
            max_out=2000,  # thinking-tier extractors: reasoning tokens
            seed=SEED,
        )
        try:
            value = prism_b.parse_dims(raw)
            break
        except (ValueError, KeyError):
            continue
    append_record(
        out_path,
        {
            "kind": "stated",
            "brand": brand_row["brand"],
            "coherence_type": brand_row["coherence_type"],
            "sector": brand_row["sector"],
            "goods_type": brand_row.get("goods_type"),
            "channel": channel["id"],
            "op_pair": op_id,
            "readout": "dims",
            "value": value,
            "flagged_malformed": value is None,
            "prompt_version": PROMPT_VERSION,
        },
    )


def measure_need(
    scenario: dict, op_id: str, op: dict, *, phase: str, out_path: Path
) -> None:
    """One need-vector elicitation: need renderer + the unchanged PRISM-B
    dims extractor, cross-family pair."""
    prose = call_model(
        op["renderer"]["model"],
        op["renderer"]["family"],
        NEED_RENDERER_SYSTEM,
        NEED_RENDERER_USER_TMPL.format(need=scenario["need"]),
        role="renderer",
        operation=f"render_need_{scenario['id']}_{op_id}",
        phase=phase,
        logs_dir=LOGS_DIR,
        max_out=1400,
        seed=SEED,
    )
    value = None
    for _ in range(2):
        raw = call_model(
            op["extractor"]["model"],
            op["extractor"]["family"],
            prism_b.EXTRACTOR_SYSTEM,
            prism_b.EXTRACTOR_USER_TMPL.format(prose=prose),
            role="extractor",
            operation=f"extract_need_{scenario['id']}_{op_id}",
            phase=phase,
            logs_dir=LOGS_DIR,
            max_out=2000,
            seed=SEED,
        )
        try:
            value = prism_b.parse_dims(raw)
            break
        except (ValueError, KeyError):
            continue
    append_record(
        out_path,
        {
            "kind": "need",
            "scenario": scenario["id"],
            "sector": scenario.get("sector"),
            "op_pair": op_id,
            "readout": "dims",
            "value": value,
            "flagged_malformed": value is None,
            "prompt_version": PROMPT_VERSION,
        },
    )


def measure_choice(
    scenario: dict,
    arrangement: list[str],
    arrangement_id: int,
    chooser_id: str,
    chooser: dict,
    descriptors: dict[str, str],
    *,
    phase: str,
    out_path: Path,
    control: str | None = None,
    dominant: str | None = None,
) -> None:
    """One choice trial: single chooser call, structured pick + ranking."""
    user = CHOICE_USER_TMPL.format(
        need=scenario["need"],
        options_block=options_block(arrangement, descriptors),
    )
    parsed = None
    for _ in range(2):  # redraw_once_then_flag
        raw = call_model(
            chooser["model"],
            chooser["family"],
            CHOICE_SYSTEM,
            user,
            role="renderer",  # the chooser renders a decision from its own knowledge
            operation=f"choice_{scenario['id']}_arr{arrangement_id}_{chooser_id}",
            phase=phase,
            logs_dir=LOGS_DIR,
            max_out=2000,  # thinking-tier choosers: reasoning tokens
            seed=SEED,
        )
        try:
            parsed = parse_choice(raw, arrangement)
            break
        except (ValueError, KeyError):
            continue
    append_record(
        out_path,
        {
            "kind": "choice",
            "scenario": scenario["id"],
            "sector": scenario.get("sector"),
            "choice_set": sorted(arrangement),
            "arrangement": arrangement,
            "arrangement_id": arrangement_id,
            "chooser": chooser_id,
            "family": chooser["family"],
            "model": chooser["model"],
            "pick": parsed["pick"] if parsed else None,
            "ranking": parsed["ranking"] if parsed else None,
            "flagged_malformed": parsed is None,
            "control": control,
            "dominant": dominant,
            "prompt_version": PROMPT_VERSION,
        },
    )


__all__ = [
    "DIMENSIONS",
    "SEED",
    "PROMPT_VERSION",
    "LOGS_DIR",
    "DATA_DIR",
    "load_config",
    "load_scenario_bank",
    "load_brand_bank",
    "bank_brands",
    "brand_lookup",
    "arrangements",
    "options_block",
    "parse_choice",
    "measure_stated",
    "measure_need",
    "measure_choice",
    "append_record",
    "load_records",
    "CHOICE_SYSTEM",
    "CHOICE_USER_TMPL",
    "NEED_RENDERER_SYSTEM",
    "NEED_RENDERER_USER_TMPL",
]
