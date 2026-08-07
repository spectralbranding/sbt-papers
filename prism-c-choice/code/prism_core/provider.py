#!/usr/bin/env python3
"""provider.py — shared 4-family LLM provider layer for PRISM campaigns.

Raw HTTP: Anthropic native /v1/messages; OpenAI / DeepSeek / DashScope via
OpenAI-compatible /chat/completions. Every call is PL3-logged via the shared
llm_call_logger (append-only JSONL, format v1.2).

Provenance: extracted from code/prism_m_lib.py (2026az,
commit dc75b6f5) with logs_dir promoted to a required argument.

API gotchas carried from the 2026az campaign:
- Anthropic Opus 4.7+ rejects sampling params (400) — temperature omitted and
  the omission logged ("temperature 0 where honored").
- gpt-5.x: max_completion_tokens (not max_tokens), temperature default-only,
  seed honored.
- Thinking-tier extractors (deepseek-v4) spend hundreds of reasoning tokens
  before content — callers must pass max_out >= 2000 for extraction jobs.

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

# The logger ships beside this module in the published bundle, so the
# import resolves without any repo-relative path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_call_logger import log_call  # noqa: E402

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


def call_model(
    model_id: str,
    family: str,
    system: str,
    user: str,
    *,
    role: str,
    operation: str,
    phase: str,
    logs_dir: Path,
    max_out: int = 1200,
    seed: int | None = None,
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
                logs_dir=logs_dir,
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
                        if seed is not None:
                            body["seed"] = seed
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


def append_record(path: Path, record: dict) -> None:
    """Parsed-record layer: append-only JSONL, never rewritten."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_records(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows
