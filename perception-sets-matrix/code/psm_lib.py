#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0"]
# ///
"""psm_lib.py — shared core for the 2026bf campaign (Perception Sets the Matrix).

Provider layer (3 primary families + Alibaba reserve, raw HTTP: Anthropic
native /v1/messages; OpenAI / DeepSeek / DashScope via OpenAI-compatible
/chat/completions), frozen prompt set (psm/1.0.0), parsers, and append-only
JSONL logging via the shared llm_call_logger.

PROMPT PURITY (frozen): no operator prompt ever contains a target profile,
a cohort profile vector, or salience weights — reading prompts carry stimulus
text or brand names only; eliciting prompts carry the natural-language
persona rendering and the stimulus materials only. Reading and eliciting are
separate instruments issued to disjoint (stateless) operator calls; only the
same-call arm deliberately combines them, as the pre-registered common-method
contrast.

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
PAPER_DIR = HERE.parent
REPO = PAPER_DIR.parents[2]
LOGS_DIR = PAPER_DIR / "logs"
DATA_DIR = PAPER_DIR / "data"

sys.path.insert(0, str(REPO / "research" / "code"))
from llm_call_logger import log_call  # noqa: E402

SEED = 20260712
PROMPT_VERSION = "psm/1.0.0"

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


def load_protocol() -> dict:
    return yaml.safe_load((PAPER_DIR / "PROTOCOL.yaml").read_text())


def load_personas() -> dict:
    return yaml.safe_load((PAPER_DIR / "PERSONAS.yaml").read_text())


def load_study1() -> dict:
    return yaml.safe_load((PAPER_DIR / "STIMULI_STUDY1.yaml").read_text())


def load_study2() -> dict:
    return yaml.safe_load((PAPER_DIR / "BRANDS_STUDY2.yaml").read_text())


def pack_text(brand: dict) -> str:
    """Render a Study-1 stimulus pack as plain text (no target profile)."""
    parts = [
        f"BRAND: {brand['name']}",
        "",
        "POSITIONING PAGE:",
        brand["positioning_page"].strip(),
    ]
    for art in brand["artifacts"]:
        parts += ["", f"[{art['kind'].upper()}]", art["text"].strip()]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Frozen prompt set — psm/1.0.0
# ---------------------------------------------------------------------------
DIM_GLOSS = (
    "semiotic: symbols, visual identity, design language;\n"
    "narrative: story and storytelling richness;\n"
    "ideological: values, ethics, principles in the brand's meaning;\n"
    "experiential: product/service experience quality and care;\n"
    "social: social meaning, community, what choosing it says about you;\n"
    "economic: value/affordability positioning (10 = strong everyday value "
    "and low price emphasis, 1 = ultra-premium pricing);\n"
    "cultural: cultural presence and relevance to the current conversation;\n"
    "temporal: relationship to time (10 = deep heritage and tradition, "
    "1 = pure novelty and newness)."
)

READ_SYSTEM = (
    "You are a careful observer of brands. You read a brand's public "
    "presentation and report its perceived position on eight dimensions of "
    "brand meaning, each scored on a 1-10 scale (half points allowed):\n"
    + DIM_GLOSS
    + "\nBase your reading ONLY on the material or public knowledge "
    "referenced in the prompt. Respond with a single JSON object with keys "
    "semiotic, narrative, ideological, experiential, social, economic, "
    "cultural, temporal and numeric values. No other text."
)

READ_PACK_USER_TMPL = (
    "Read the following brand materials and score the brand's perceived "
    "position on the eight dimensions.\n\nCategory: {category}\n\n{pack}\n\n"
    "JSON only."
)

READ_ELICITED_USER_TMPL = (
    "Score the brand '{brand}' in the category '{category}' as it is "
    "perceived through its publicly observable presence reflected in your "
    "knowledge. JSON only."
)

READ_PERSONA_USER_TMPL = (
    "The following text describes a cohort of buyers — how they attend to "
    "brands and what matters to them. Score the COHORT itself on the same "
    "eight dimensions, interpreting each dimension as the cohort's "
    "orientation (e.g., semiotic = how much they respond to symbols and "
    "design; economic = how price/value-driven they are; temporal = how "
    "heritage-oriented rather than novelty-oriented they are).\n\n"
    "COHORT DESCRIPTION:\n{persona}\n\nJSON only."
)

ELICIT_SYSTEM = (
    "You simulate the collective purchase behavior of a described cohort of "
    "buyers. You will be given the cohort description and the category's "
    "consideration set. Respond with a single JSON object and no other "
    "text, with keys:\n"
    '  "constant_sum": object mapping each brand name to an integer number '
    "of purchases, summing to exactly 10 — of the cohort's next 10 category "
    "purchases, how many go to each brand;\n"
    '  "juster": object mapping each brand name to an integer 0-10 on the '
    "Juster purchase-probability scale (10 = practically certain the cohort "
    "buys this brand in the period, 0 = no chance);\n"
    '  "switching": object with "current_brand" (copied from the prompt) '
    'and "next_purchase" mapping each brand name to the probability '
    "(numbers summing to 1) that the cohort's next purchase is that brand "
    "GIVEN its current brand is the one named.\n"
    "Judge only from the cohort description and the brand materials given."
)

ELICIT_USER_TMPL = (
    "COHORT DESCRIPTION:\n{persona}\n\n"
    "CATEGORY: {category}\n\nCONSIDERATION SET:\n{materials}\n\n"
    "For the switching question, the cohort's current brand is: "
    "{current_brand}.\n\nJSON only."
)

SAMECALL_SYSTEM = (
    "You will do two tasks in one response for a described cohort of buyers "
    "and a category consideration set. Respond with a single JSON object "
    "and no other text, with keys:\n"
    '  "readings": object mapping each brand name to an object with the '
    "eight dimension keys (semiotic, narrative, ideological, experiential, "
    "social, economic, cultural, temporal), each scored 1-10 as the brand "
    "is perceived BY THIS COHORT:\n"
    + DIM_GLOSS
    + '\n  "constant_sum": object mapping each brand name to an integer '
    "number of purchases, summing to exactly 10 — of the cohort's next 10 "
    "category purchases, how many go to each brand."
)

SAMECALL_USER_TMPL = (
    "COHORT DESCRIPTION:\n{persona}\n\n"
    "CATEGORY: {category}\n\nCONSIDERATION SET:\n{materials}\n\nJSON only."
)


# ---------------------------------------------------------------------------
# Provider call with logging + retry
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
    max_out: int = 2000,
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
                    # Anthropic 4.7+ rejects sampling params — temperature
                    # omitted ("temperature 0 where honored").
                    params = {"max_tokens": max_out}
                    logger.set_parameters(
                        params
                        | {
                            "prompt_sha256": prompt_sha,
                            "prompt_version": PROMPT_VERSION,
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
                        timeout=240,
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
                        # thinking-tier models (deepseek-v4) spend reasoning
                        # tokens before content — cap must cover both.
                        body["max_tokens"] = max_out
                    logger.set_parameters(
                        {k: v for k, v in body.items() if k != "messages"}
                        | {
                            "prompt_sha256": prompt_sha,
                            "prompt_version": PROMPT_VERSION,
                        }
                    )
                    r = httpx.post(
                        endpoint,
                        headers={"Authorization": f"Bearer {key}"},
                        json=body,
                        timeout=240,
                    )
                    r.raise_for_status()
                    data = r.json()
                    logger.capture_response(data)
                    text = data["choices"][0]["message"]["content"] or ""
            return text
        except Exception as exc:  # noqa: BLE001 — logged + retried per policy
            last_exc = exc
            if attempt < 3:
                time.sleep(backoffs[attempt])
    raise RuntimeError(f"{model_id} failed after retries: {last_exc}")


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------
def parse_json_block(raw: str) -> dict:
    s = raw.strip()
    if s.startswith("```"):
        s = s.split("```")[1]
        if s.startswith("json"):
            s = s[4:]
    start, end = s.find("{"), s.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON object in output: {raw[:200]}")
    return json.loads(s[start : end + 1])


def parse_dims(raw: str | dict) -> list[float]:
    d = parse_json_block(raw) if isinstance(raw, str) else raw
    vec = [float(d[k]) for k in DIMENSIONS]
    if not all(1.0 <= v <= 10.0 for v in vec):
        raise ValueError(f"dimension out of range: {vec}")
    return vec


def _match_brand_keys(d: dict, brand_names: list[str], what: str) -> dict:
    """Map model output keys to canonical brand names (exact or substring)."""
    out = {}
    for name in brand_names:
        if name in d:
            out[name] = d[name]
            continue
        hits = [k for k in d if name.lower() in k.lower() or k.lower() in name.lower()]
        if len(hits) != 1:
            raise ValueError(f"{what}: cannot match brand '{name}' in {list(d)}")
        out[name] = d[hits[0]]
    return out


def parse_elicitation(raw: str, brand_names: list[str]) -> dict:
    d = parse_json_block(raw)
    cs = {
        k: int(round(float(v)))
        for k, v in _match_brand_keys(
            d["constant_sum"], brand_names, "constant_sum"
        ).items()
    }
    juster = {
        k: float(v)
        for k, v in _match_brand_keys(d["juster"], brand_names, "juster").items()
    }
    sw = d.get("switching") or {}
    nxt = sw.get("next_purchase") or {}
    switching = None
    if nxt:
        try:
            np_ = {
                k: float(v)
                for k, v in _match_brand_keys(nxt, brand_names, "switching").items()
            }
            switching = {"current_brand": sw.get("current_brand"), "next_purchase": np_}
        except (ValueError, TypeError):
            switching = None  # descriptive-only probe; tolerate malformation
    if sum(cs.values()) != 10:
        raise ValueError(f"constant_sum != 10: {cs}")
    if not all(0.0 <= v <= 10.0 for v in juster.values()):
        raise ValueError(f"juster out of range: {juster}")
    return {"constant_sum": cs, "juster": juster, "switching": switching}


def parse_samecall(raw: str, brand_names: list[str]) -> dict:
    d = parse_json_block(raw)
    readings = {
        k: parse_dims(v)
        for k, v in _match_brand_keys(d["readings"], brand_names, "readings").items()
    }
    cs = {
        k: int(round(float(v)))
        for k, v in _match_brand_keys(
            d["constant_sum"], brand_names, "constant_sum"
        ).items()
    }
    if sum(cs.values()) != 10:
        raise ValueError(f"constant_sum != 10: {cs}")
    return {"readings": readings, "constant_sum": cs}


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------
def append_record(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def existing_keys(path: Path) -> set[str]:
    return {r["record_key"] for r in load_records(path) if not r.get("failed")}
