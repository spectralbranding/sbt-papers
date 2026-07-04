#!/usr/bin/env python3
"""prism_t_lib.py — PRISM-T campaign core (2026ba).

PL1 config + frozen bank + pinned-panel loaders, the PL2 prompt set
(prism-t/v1.0.0: artifact-READING renderer + the verbatim PRISM-B extractor),
and the (brand, artifact, rung, operator) measurement step.

The PRISM-T renderer variant reads a PROVIDED artifact text (the pinned
panel stores artifacts byte-identical; the prompt bytes around them are part
of the pinned input and are frozen here — changing any wording forks the
instrument version). The extractor layer is prism_core.prism_b verbatim.
"""

from __future__ import annotations

import hashlib
import json
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import yaml

CODE_DIR = Path(__file__).resolve().parent
PAPER_DIR = CODE_DIR.parent
RESEARCH_DIR = PAPER_DIR.parent
sys.path.insert(0, str(RESEARCH_DIR))
from prism_core import prism_b, provider  # noqa: E402

DATA_DIR = PAPER_DIR / "data"
LOGS_DIR = PAPER_DIR / "logs"
PANEL_DIR = PAPER_DIR / "panel" / "pinned"
MANIFEST = PAPER_DIR / "panel" / "PINNED_MANIFEST.json"

SEED = 20260702
PROMPT_VERSION = "prism-t/v1.0.0"

# --- PL2 prompt set (FROZEN; byte-identical across epochs) -------------------

RENDERER_SYSTEM = (
    "You are an observer of brands as they appear through public artifacts. "
    "You will be given the text of ONE public artifact concerning a brand, "
    "captured from a specific channel of its public presence. Describe what "
    "an attentive member of the public would perceive of the brand from THIS "
    "artifact. Ground every claim in the artifact text provided; you may use "
    "general knowledge of the world to interpret it, but the artifact is the "
    "evidence. Write plain analytical prose. Do not score, rate, or rank; "
    "describe."
)

RENDERER_USER_TMPL = (
    "Brand (nominative reference only): {brand}\n"
    "Category: {category}\n"
    "Observation channel: {channel_desc}\n"
    "Artifact text:\n"
    "---\n"
    "{artifact_text}\n"
    "---\n\n"
    "In 250-400 words of analytical prose, describe what this artifact "
    "conveys about the brand's perceived: symbols and visual identity; story "
    "and narrative; values and ideology; product/service experience; social "
    "meaning and community; price/value positioning; cultural presence; and "
    "relationship to time (heritage vs novelty). Cover each aspect at least "
    "briefly; ground every claim in the artifact text."
)

EXTRACTOR_SYSTEM = prism_b.EXTRACTOR_SYSTEM
EXTRACTOR_USER_TMPL = prism_b.EXTRACTOR_USER_TMPL
DIMENSIONS = prism_b.DIMENSIONS

# Pre-registered H3 dimension sets (PL0 §9.2; THEORY_GROUNDING.md §5).
H3_HIGH_DRIFT = ["ideological", "cultural", "social", "temporal", "economic"]
H3_FORMAT_ANCHORED = ["semiotic", "narrative", "experiential"]


# --- Loaders ------------------------------------------------------------------


def load_config() -> dict:
    return yaml.safe_load((PAPER_DIR / "PL1_CONFIG.yaml").read_text())


def load_bank() -> dict:
    cfg = load_config()
    return yaml.safe_load((PAPER_DIR / cfg["brand_bank"]).read_text())


def bank_brands(bank: dict) -> list[dict]:
    rows = []
    for stratum, brands in bank["strata"].items():
        for b in brands:
            rows.append({**b, "stratum": stratum})
    return rows


def brand_slug(brand: str) -> str:
    s = unicodedata.normalize("NFKD", brand.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    for ch in "'’.":
        s = s.replace(ch, "")
    s = s.replace("(", "").replace(")", "")
    return "-".join(s.split())


def load_manifest() -> list[dict]:
    return json.loads(MANIFEST.read_text())


def load_artifact(brand: str, channel_id: str) -> str:
    """Read a pinned artifact byte-identically and verify its manifest hash."""
    path = PANEL_DIR / brand_slug(brand) / f"{channel_id}.txt"
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    for row in load_manifest():
        if row["brand"] == brand and row["channel"] == channel_id:
            if row["sha256"] != sha:
                raise RuntimeError(
                    f"pinned artifact tamper: {path} sha {sha[:12]} != "
                    f"manifest {row['sha256'][:12]}"
                )
            return data.decode("utf-8")
    raise KeyError(f"no manifest row for ({brand}, {channel_id})")


# --- Measurement step ----------------------------------------------------------


def record_key(r: dict) -> tuple:
    return (
        r["panel"],
        r["brand"],
        r["channel"],
        r["renderer"],
        r["extractor"],
        r.get("run", 1),
    )


def measure_artifact(
    brand_row: dict,
    channel: dict,
    artifact_text: str,
    renderer: dict,
    extractor: dict,
    *,
    phase: str,
    panel: str = "pinned",
    epoch: str = "VE-1",
    run: int = 1,
    out_path: Path,
) -> dict:
    """One (brand, artifact, renderer-version, extractor) reading:
    render prose from the artifact, extract the eight-dimension vector,
    append the parsed record. Malformed extract: redraw once then flag."""
    user = RENDERER_USER_TMPL.format(
        brand=brand_row["brand"],
        category=brand_row["category"],
        channel_desc=channel["description"],
        artifact_text=artifact_text,
    )
    prose = ""
    for _ in range(2):  # thinking-tier renderers can return empty content
        prose = provider.call_model(
            renderer["model"],
            renderer["family"],
            RENDERER_SYSTEM,
            user,
            role="renderer",
            operation=f"render:{brand_row['brand']}:{channel['id']}",
            phase=phase,
            logs_dir=LOGS_DIR,
            # reasoning-tier renderers (e.g. gpt-5 dated base) spend budget on
            # reasoning before content — PL1 sets a per-rung max_out override
            max_out=renderer.get("max_out", 1200),
            seed=SEED,
        )
        if prose.strip():
            break
    dims, flagged = None, False
    if not prose.strip():
        flagged = True
    for attempt in range(0 if flagged else 2):
        raw = provider.call_model(
            extractor["model"],
            extractor["family"],
            EXTRACTOR_SYSTEM,
            EXTRACTOR_USER_TMPL.format(prose=prose),
            role="extractor",
            operation=f"extract:{brand_row['brand']}:{channel['id']}",
            phase=phase,
            logs_dir=LOGS_DIR,
            max_out=2000,  # thinking-tier extractors need >= 2000
            seed=SEED,
        )
        try:
            dims = prism_b.parse_dims(raw)
            break
        except (ValueError, KeyError):
            flagged = attempt == 1
    record = {
        "panel": panel,
        "epoch": epoch,
        "brand": brand_row["brand"],
        "stratum": brand_row.get("stratum"),
        "channel": channel["id"],
        "renderer": renderer["model"],
        "renderer_family": renderer["family"],
        "extractor": extractor["model"],
        "extractor_family": extractor["family"],
        "run": run,
        "prompt_version": PROMPT_VERSION,
        "dims": dims,
        "flagged": flagged,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    provider.append_record(out_path, record)
    return record


def load_records(path: Path) -> list[dict]:
    return provider.load_records(path)
