#!/usr/bin/env python3
"""prism_o_lib.py — PRISM-O (2026bd) campaign library.

Adapts the PRISM-M campaign pattern (research/prism_m/code/, 2026az) to the
optimization-depth instrument's two roles per operator pair:

- SEGMENTER: reads an artifact/vignette text and returns the list of
  improvement interventions (verbatim evidence spans). On the Stage-1 bank
  (single-intervention by construction) it validates the one-intervention
  premise; on Stage-2 artifacts it does the real segmentation work.
- CLASSIFIER (different family — 2026ap discipline): codes ONE intervention
  onto the D4-D1 depth ladder under the frozen rubric (RUBRIC.md embedded
  verbatim: decision rules + tie-breaker + the 12 worked hard cases).

All calls go through prism_core.provider.call_model (PL3 JSONL logging,
family gotchas, retries). Keys via `bws run -- <wrapper.sh>`.

Ground-truth hygiene note (scoring, frozen ex ante in run/score code): bank
bases B01-B12 are the rubric's worked examples and are therefore IN the
classifier prompt; H1(i) is reported for the full bank (as registered) AND
for the 14 held-out bases, and the Stage-2 gate requires BOTH >= .80 — the
conservative reading of the pre-registered threshold.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

PRISM_O_DIR = Path(__file__).resolve().parents[1]
REPO = PRISM_O_DIR.parents[1]
LOGS_DIR = PRISM_O_DIR / "logs"
DATA_DIR = PRISM_O_DIR / "data"
CODE_DIR = PRISM_O_DIR / "code"

sys.path.insert(0, str(REPO / "research"))
from prism_core.provider import (  # noqa: E402
    FAMILY_ENDPOINTS,
    FAMILY_KEYS,
    append_record,
    call_model,
    load_records,
    parse_json_block,
)

RUNGS = ("D1", "D2", "D3", "D4", "UNCLASSIFIED")
# Bases whose worked answers are embedded in the classifier prompt (RUBRIC §4).
ANCHORED_BASES = {f"B{i:02d}" for i in range(1, 13)}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_config() -> dict:
    return yaml.safe_load((PRISM_O_DIR / "PL1_CONFIG.yaml").read_text())


def load_bank() -> dict:
    return yaml.safe_load((PRISM_O_DIR / "PL2_VIGNETTE_BANK.yaml").read_text())


def expand_bank(bank: dict) -> list[dict]:
    """26 bases x (named, masked) -> 52 reading units, deterministic order."""
    units = []
    token = bank["masked_token"]
    for v in bank["vignettes"]:
        for variant in ("named", "masked"):
            org = v["org_named"] if variant == "named" else token
            units.append(
                {
                    "base_id": v["id"],
                    "variant": variant,
                    "text": v["text"].replace("{ORG}", org).strip(),
                    "rung_truth": v["rung_truth"],
                    "register": v["register"],
                    "probe": bool(v.get("concordance_probe")),
                    "anchored": v["id"] in ANCHORED_BASES,
                }
            )
    return units


# ---------------------------------------------------------------------------
# Prompts (PL2). The rubric text is loaded from the frozen RUBRIC.md so the
# instrument and its documentation cannot drift apart.
# ---------------------------------------------------------------------------


def _rubric_prompt_block() -> str:
    """Sections 2-4 of the frozen rubric (tree, tie-breaker, hard cases),
    with the mermaid figure replaced by its plain-rule equivalent already
    present in the prose."""
    text = (PRISM_O_DIR / "RUBRIC.md").read_text()
    # Drop the mermaid block (models read the prose rules; the figure is for
    # humans) but keep everything else between §2 and the end of §4.
    text = re.sub(r"```mermaid.*?```", "(decision tree stated in prose below)", text, flags=re.S)
    start = text.index("## 2. Decision tree")
    end = text.index("## 5.")
    return text[start:end].strip()


SEGMENTER_SYSTEM = """You segment organizational texts into improvement interventions.

An improvement intervention is one announced or reported change with an
identifiable object (what is being changed). Read the text and list every
distinct improvement intervention it describes. For each, quote the verbatim
evidence span and give a one-line summary. Do not classify, judge, or infer
anything beyond what the text states.

Return ONLY a JSON object:
{"interventions": [{"span": "<verbatim quote>", "summary": "<one line>"}]}"""


def classifier_system(rubric_block: str) -> str:
    return f"""You code organizational improvement interventions onto a four-rung
optimization-depth ladder under a fixed mechanical rubric. Apply the rubric
EXACTLY as written; do not use outside knowledge about any named company —
code only what the text specifies.

{rubric_block}

Return ONLY a JSON object:
{{"rung": "D1|D2|D3|D4|UNCLASSIFIED", "evidence_span": "<verbatim quote>",
"rationale_brief": "<one sentence naming the object the intervention changes>",
"confidence": "high|medium|low"}}"""


def segmenter_user(text: str) -> str:
    return f"TEXT:\n{text}\n\nSegment this text into improvement interventions."


def classifier_user(text: str) -> str:
    return f"INTERVENTION TEXT:\n{text}\n\nCode this intervention's optimization depth."


# ---------------------------------------------------------------------------
# One Stage-1 reading = segmenter call + classifier call on one bank unit.
# ---------------------------------------------------------------------------


def read_unit(
    unit: dict,
    op_id: str,
    op: dict,
    rubric_block: str,
    phase: str,
    out_path: Path,
) -> dict:
    seg = op["segmenter"]
    cls = op["classifier"]
    seg_raw = call_model(
        seg["model"],
        seg["family"],
        SEGMENTER_SYSTEM,
        segmenter_user(unit["text"]),
        role="segmenter",
        operation=f"{phase}:{unit['base_id']}:{unit['variant']}:{op_id}:segment",
        phase=phase,
        logs_dir=LOGS_DIR,
        max_out=2400,
    )
    try:
        seg_json = parse_json_block(seg_raw)
        n_interventions = len(seg_json.get("interventions", []))
    except ValueError:
        seg_json, n_interventions = {"interventions": []}, -1  # malformed; flagged

    cls_raw = call_model(
        cls["model"],
        cls["family"],
        classifier_system(rubric_block),
        classifier_user(unit["text"]),
        role="classifier",
        operation=f"{phase}:{unit['base_id']}:{unit['variant']}:{op_id}:classify",
        phase=phase,
        logs_dir=LOGS_DIR,
        max_out=2400,
    )
    try:
        cls_json = parse_json_block(cls_raw)
        rung_pred = str(cls_json.get("rung", "")).strip().upper()
        if rung_pred not in RUNGS:
            rung_pred = "MALFORMED"
    except ValueError:
        cls_json, rung_pred = {}, "MALFORMED"

    record = {
        "phase": phase,
        "base_id": unit["base_id"],
        "variant": unit["variant"],
        "register": unit["register"],
        "probe": unit["probe"],
        "anchored": unit["anchored"],
        "op_pair": op_id,
        "segmenter_model": seg["model"],
        "classifier_model": cls["model"],
        "n_interventions_detected": n_interventions,
        "rung_pred": rung_pred,
        "rung_truth": unit["rung_truth"],
        "confidence": cls_json.get("confidence"),
        "rationale_brief": cls_json.get("rationale_brief"),
        "ts": utc_now(),
    }
    append_record(out_path, record)
    return record


# ---------------------------------------------------------------------------
# Pre-run version check (2026ba equipment): pinned IDs vs live /models.
# ---------------------------------------------------------------------------

MODELS_ENDPOINTS = {
    "anthropic": "https://api.anthropic.com/v1/models?limit=1000",
    "openai": "https://api.openai.com/v1/models",
    "deepseek": "https://api.deepseek.com/models",
    "alibaba": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models",
}


def version_check(cfg: dict, stage: str) -> dict:
    """Assert every pinned model id for the stage is present in its family's
    live catalog. Read-only; writes the epoch record to DATA_DIR."""
    import os

    import httpx

    pins: dict[str, set] = {}
    for op_id, op in cfg["operator_pairs"].items():
        if stage not in op.get("stages", []):
            continue
        for role in ("segmenter", "classifier"):
            pins.setdefault(op[role]["family"], set()).add(op[role]["model"])
    result = {"stage": stage, "checked_at": utc_now(), "families": {}, "ok": True}
    for family, models in sorted(pins.items()):
        key = os.environ[FAMILY_KEYS[family]]
        headers = (
            {"x-api-key": key, "anthropic-version": "2023-06-01"}
            if family == "anthropic"
            else {"Authorization": f"Bearer {key}"}
        )
        r = httpx.get(MODELS_ENDPOINTS[family], headers=headers, timeout=60)
        r.raise_for_status()
        live = {m.get("id") for m in r.json().get("data", [])}
        fam = {"pinned": sorted(models), "present": {}, "ok": True}
        for m in sorted(models):
            present = m in live
            fam["present"][m] = present
            if not present:
                fam["ok"] = False
                result["ok"] = False
        result["families"][family] = fam
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / f"version_check_{stage}.json"
    out.write_text(json.dumps(result, indent=2))
    return result


def usage_from_log_record(rec: dict) -> tuple[int, int]:
    """(input_tokens, output_tokens) from a PL3 record, tolerating both the
    logger's derived `tokens` field and the raw provider usage shapes
    (OpenAI-compatible prompt/completion_tokens; Anthropic input/output)."""
    toks = rec.get("tokens") or {}
    tin = int(toks.get("input") or 0)
    tout = int(toks.get("output") or 0)
    if tin or tout:
        return tin, tout
    usage = (rec.get("response_metadata") or {}).get("usage") or {}
    tin = int(usage.get("prompt_tokens") or usage.get("input_tokens") or 0)
    tout = int(usage.get("completion_tokens") or usage.get("output_tokens") or 0)
    return tin, tout


__all__ = [
    "usage_from_log_record",
    "ANCHORED_BASES",
    "DATA_DIR",
    "FAMILY_ENDPOINTS",
    "LOGS_DIR",
    "PRISM_O_DIR",
    "RUNGS",
    "_rubric_prompt_block",
    "append_record",
    "classifier_system",
    "expand_bank",
    "load_bank",
    "load_config",
    "load_records",
    "read_unit",
    "utc_now",
    "version_check",
]
