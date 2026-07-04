#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0"]
# ///
"""prism_m_lib.py — shared core for the PRISM-M metamerism campaign (2026az).

Provider layer (4 families via raw HTTP: Anthropic native /v1/messages;
OpenAI / DeepSeek / DashScope via OpenAI-compatible /chat/completions),
PL2 prompt builders (renderer, eight-dimension extractor, A-SCORE / A-RANK /
A-PICK aggregator extractors), and the PL3 append-only JSONL session writer
(via the shared llm_call_logger).

Config: ../PL1_CONFIG.yaml (operator pairs, channels, retry policy).
Bank:   ../PL2_BRAND_BANK.yaml (frozen stratified stimulus frame).

Keys via `bws run -- <wrapper.sh>`: ANTHROPIC_API_KEY, OPENAI_API_KEY,
DEEPSEEK_API_KEY, DASHSCOPE_API_KEY.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

import httpx
import yaml

HERE = Path(__file__).resolve().parent
PRISM_M_DIR = HERE.parent
REPO = PRISM_M_DIR.parents[1]
LOGS_DIR = PRISM_M_DIR / "logs"
DATA_DIR = PRISM_M_DIR / "data"

# llm_call_logger moved into prism_core 2026-07-02 (owner: the instrument-
# family base library; dependency arrow now Spectrometer -> prism_core).
sys.path.insert(0, str(REPO / "research" / "prism_core"))
from llm_call_logger import log_call  # noqa: E402

DIMENSIONS = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
]

SEED = 20260702

FAMILY_ENDPOINTS = {
    "anthropic": "https://api.anthropic.com/v1/messages",
    "openai": "https://api.openai.com/v1/chat/completions",
    "deepseek": "https://api.deepseek.com/chat/completions",
    "alibaba": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions",
}
FAMILY_KEYS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "alibaba": "DASHSCOPE_API_KEY",
}


def load_config() -> dict:
    return yaml.safe_load((PRISM_M_DIR / "PL1_CONFIG.yaml").read_text())


def load_bank() -> dict:
    return yaml.safe_load((PRISM_M_DIR / "PL2_BRAND_BANK.yaml").read_text())


def bank_brands(bank: dict) -> list[dict]:
    """Flatten strata to a list of brand dicts with stratum metadata."""
    out = []
    for cell, brands in bank["strata"].items():
        ctype, sector = cell.rsplit("_", 1)
        for b in brands:
            row = dict(b)
            row["coherence_type"] = ctype
            row["sector"] = sector
            out.append(row)
    return out


# ---------------------------------------------------------------------------
# PL2 prompts — version tag prism-m/v1.0.0
# ---------------------------------------------------------------------------
PROMPT_VERSION = "prism-m/v1.0.0"

RENDERER_SYSTEM = (
    "You are an observer of brands as they appear through public artifacts. "
    "You describe what an attentive member of the public would perceive of a "
    "brand through ONE specific channel of its public presence, based on the "
    "brand's publicly observable artifacts in that channel as reflected in "
    "your knowledge. You do not have and must not assume any internal or "
    "ground-truth brand information. Write plain analytical prose. Do not "
    "score, rate, or rank; describe."
)

RENDERER_SYSTEM_ABLATED = (
    "Describe how a brand is perceived by the public through one channel of "
    "its public presence, using only publicly observable material reflected "
    "in your knowledge. Plain prose only; no scores or rankings."
)

RENDERER_USER_TMPL = (
    "Brand (nominative reference only): {brand}\n"
    "Category: {category}\n"
    "Observation channel: {channel_desc}\n\n"
    "In 250-400 words of analytical prose, describe what this channel "
    "conveys about the brand's perceived: symbols and visual identity; story "
    "and narrative; values and ideology; product/service experience; social "
    "meaning and community; price/value positioning; cultural presence; and "
    "relationship to time (heritage vs novelty). Cover each aspect at least "
    "briefly; ground every claim in the kind of public material this channel "
    "contains."
)

EXTRACTOR_SYSTEM = (
    "You convert analytical prose about a brand's public perception into a "
    "strict structured score sheet. You see ONLY the prose below. You have no "
    "other knowledge of the brand and must not add any. Score conservatively "
    "from the prose. Output JSON only, no code fences, no commentary."
)

EXTRACTOR_USER_TMPL = (
    "Read the prose and emit JSON with EXACTLY these keys, each a float 0-10 "
    "(intensity of the perception on that dimension as conveyed by the "
    "prose):\n\n"
    '{{"semiotic": <f>, "narrative": <f>, "ideological": <f>, '
    '"experiential": <f>, "social": <f>, "economic": <f>, "cultural": <f>, '
    '"temporal": <f>}}\n\n'
    "semiotic=symbols/visual identity; narrative=story; ideological=values; "
    "experiential=product/service experience; social=social meaning/community; "
    "economic=price/value positioning; cultural=cultural presence; "
    "temporal=heritage/time relationship.\n\nProse to score:\n{prose}"
)

A_SCORE_SYSTEM = (
    "You are a brand-health scorecard. From the prose below (your ONLY "
    "evidence), assign ONE overall brand-health grade from this scale: "
    "A+, A, A-, B+, B, B-, C+, C, C-, D, F. "
    'Output JSON only: {"grade": "<grade>"}.'
)
A_SCORE_USER_TMPL = "Prose:\n{prose}"

A_RANK_SYSTEM = (
    "You are a recommendation-ranking engine. From the prose below (your "
    "ONLY evidence), estimate where this brand would place in a ranked list "
    "of the ten leading brands a typical customer would be shown when asking "
    "for a recommendation in this category (1 = ranked first, 10 = ranked "
    'last). Output JSON only: {"rank": <integer 1-10>}.'
)
A_RANK_USER_TMPL = "Category: {category}\nProse:\n{prose}"

A_PICK_SYSTEM = (
    "You are a recommendation engine making a binary call. From the prose "
    "below (your ONLY evidence), decide: would you recommend this brand to a "
    "typical customer in its category, yes or no? "
    'Output JSON only: {"pick": "yes"} or {"pick": "no"}.'
)
A_PICK_USER_TMPL = "Category: {category}\nProse:\n{prose}"

GRADE_MAP = {
    "A+": 1.0,
    "A": 0.9,
    "A-": 0.8,
    "B+": 0.7,
    "B": 0.6,
    "B-": 0.5,
    "C+": 0.4,
    "C": 0.3,
    "C-": 0.2,
    "D": 0.1,
    "F": 0.0,
}


# ---------------------------------------------------------------------------
# Provider call with PL3 logging + retry policy
# ---------------------------------------------------------------------------
def call_model(
    model_id: str,
    family: str,
    system: str,
    user: str,
    *,
    role: str,
    operation: str,
    phase: str,
    max_out: int = 1200,
) -> str:
    key = os.environ[FAMILY_KEYS[family]]
    endpoint = FAMILY_ENDPOINTS[family]
    prompt_sha = hashlib.sha256((system + "\n" + user).encode()).hexdigest()
    backoffs = [5, 15, 45]
    last_exc: Exception | None = None
    for attempt in range(4):
        try:
            with log_call(
                phase=phase,
                operation=operation,
                operator=model_id,
                operator_role=role,
                endpoint=endpoint,
                sdk_version="httpx>=0.27 (raw HTTP)",
                logs_dir=LOGS_DIR,
            ) as logger:
                logger.set_system_prompt(system)
                logger.set_user_prompt(user)
                if family == "anthropic":
                    # Opus 4.7+ rejects sampling params (400) - omit
                    # temperature; PL1 "temperature 0 where honored".
                    params = {"max_tokens": max_out}
                    logger.set_parameters(
                        {
                            **params,
                            "prompt_sha256": prompt_sha,
                            "sdk_param_note": "Anthropic 4.7+: temperature omitted",
                        }
                    )
                    r = httpx.post(
                        endpoint,
                        headers={
                            "x-api-key": key,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json",
                        },
                        json={
                            "model": model_id,
                            "system": system,
                            "messages": [{"role": "user", "content": user}],
                            **params,
                        },
                        timeout=180,
                    )
                    r.raise_for_status()
                    data = r.json()
                    logger.capture_response(data)
                    text = "".join(b.get("text", "") for b in data.get("content", []))
                else:
                    body: dict = {
                        "model": model_id,
                        "messages": [
                            {"role": "system", "content": system},
                            {"role": "user", "content": user},
                        ],
                        "temperature": 0,
                    }
                    if model_id.startswith("gpt-5"):
                        body.pop("temperature")  # gpt-5.x: default only
                        body["max_completion_tokens"] = max_out
                        body["seed"] = SEED
                    else:
                        body["max_tokens"] = max_out
                    logger.set_parameters(
                        {k: v for k, v in body.items() if k not in ("messages",)}
                        | {"prompt_sha256": prompt_sha}
                    )
                    r = httpx.post(
                        endpoint,
                        headers={"Authorization": f"Bearer {key}"},
                        json=body,
                        timeout=180,
                    )
                    r.raise_for_status()
                    data = r.json()
                    logger.capture_response(data)
                    text = data["choices"][0]["message"]["content"] or ""
            return text
        except Exception as exc:  # noqa: BLE001 - logged + retried per policy
            last_exc = exc
            if attempt < 3:
                time.sleep(backoffs[attempt])
    raise RuntimeError(f"{model_id} failed after retries: {last_exc}")


def parse_json_block(raw: str) -> dict:
    """Parse model JSON output, tolerating code fences and stray prose."""
    s = raw.strip()
    if s.startswith("```"):
        s = s.split("```")[1]
        if s.startswith("json"):
            s = s[4:]
    start, end = s.find("{"), s.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON object in output: {raw[:200]}")
    return json.loads(s[start : end + 1])


def parse_dims(raw: str) -> list[float]:
    d = parse_json_block(raw)
    vec = [float(d[k]) for k in DIMENSIONS]
    if not all(0.0 <= v <= 10.0 for v in vec):
        raise ValueError(f"dimension out of range: {vec}")
    return vec


def parse_score(raw: str) -> float:
    g = str(parse_json_block(raw)["grade"]).strip().upper().replace(" ", "")
    if g not in GRADE_MAP:
        raise ValueError(f"bad grade: {g}")
    return GRADE_MAP[g]


def parse_rank(raw: str) -> float:
    v = int(parse_json_block(raw)["rank"])
    if not 1 <= v <= 10:
        raise ValueError(f"rank out of range: {v}")
    return (v - 1) / 9.0  # normalized to [0,1]


def parse_pick(raw: str) -> float:
    v = str(parse_json_block(raw)["pick"]).strip().lower()
    if v not in ("yes", "no"):
        raise ValueError(f"bad pick: {v}")
    return 1.0 if v == "yes" else 0.0


def append_record(path: Path, record: dict) -> None:
    """PL3: append-only JSONL, one parsed record per (brand, channel,
    op-pair, readout). Immutable: never rewritten."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def measure_brand(
    brand_row: dict,
    channel: dict,
    op_id: str,
    op: dict,
    *,
    phase: str,
    readouts: tuple[str, ...],
    out_path: Path,
    prompt_variant: str = "main",
) -> None:
    """One full measurement: render once, extract each requested readout."""
    rsys = RENDERER_SYSTEM if prompt_variant == "main" else RENDERER_SYSTEM_ABLATED
    user = RENDERER_USER_TMPL.format(
        brand=brand_row["brand"],
        category=brand_row["category"],
        channel_desc=channel["description"],
    )
    prose = call_model(
        op["renderer"]["model"],
        op["renderer"]["family"],
        rsys,
        user,
        role="renderer",
        operation=f"render_{brand_row['brand']}_{channel['id']}_{op_id}",
        phase=phase,
        max_out=1400,
    )
    ext = op["extractor"]
    jobs = {
        "dims": (EXTRACTOR_SYSTEM, EXTRACTOR_USER_TMPL.format(prose=prose), parse_dims),
        "score": (A_SCORE_SYSTEM, A_SCORE_USER_TMPL.format(prose=prose), parse_score),
        "rank": (
            A_RANK_SYSTEM,
            A_RANK_USER_TMPL.format(category=brand_row["category"], prose=prose),
            parse_rank,
        ),
        "pick": (
            A_PICK_SYSTEM,
            A_PICK_USER_TMPL.format(category=brand_row["category"], prose=prose),
            parse_pick,
        ),
    }
    for readout in readouts:
        sys_p, usr_p, parser = jobs[readout]
        value = None
        for _ in range(2):  # redraw_once_then_flag
            raw = call_model(
                ext["model"],
                ext["family"],
                sys_p,
                usr_p,
                role="extractor",
                operation=f"extract_{readout}_{brand_row['brand']}_{channel['id']}_{op_id}",
                phase=phase,
                # thinking-tier extractors (deepseek-v4) spend hundreds of
                # reasoning tokens before content - cap must cover both
                max_out=2000,
            )
            try:
                value = parser(raw)
                break
            except (ValueError, KeyError, json.JSONDecodeError):
                continue
        append_record(
            out_path,
            {
                "brand": brand_row["brand"],
                "coherence_type": brand_row["coherence_type"],
                "sector": brand_row["sector"],
                "goods_type": brand_row.get("goods_type"),
                "channel": channel["id"],
                "op_pair": op_id,
                "readout": readout,
                "value": value,
                "flagged_malformed": value is None,
                "prompt_variant": prompt_variant,
                "prompt_version": PROMPT_VERSION,
            },
        )


def load_records(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows
