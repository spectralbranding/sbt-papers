"""LLM-call professional logger — single-source schema + JSONL writer + redaction.

Implements feedback_llm_call_professional_logging.md (HARD RULE 2026-05-27):
every LLM/model API call in this paper's research work is JSONL-logged in an
academically-acceptable schema, published on the public GitHub mirror at
Zenodo upload, and cited in paper.md by GitHub URL.

Pattern:

    from llm_call_logger import log_call
    with log_call(
        phase="3.5b",
        operation="render_PB_abstract_to_chinese",
        operator="deepseek",
        endpoint="https://api.deepseek.com/v1/chat/completions",
        sdk_version="openai==1.51.0",
    ) as logger:
        logger.set_system_prompt("...")
        logger.set_user_prompt("...")
        logger.set_parameters({"temperature": 0.7, "max_tokens": 4000, "seed": 42})
        response = client.chat.completions.create(...)
        logger.capture_response(response)
    # On exit: writes JSONL row to logs/3.5b_render_PB_abstract_to_chinese_calls.jsonl

Schema (per feedback_llm_call_professional_logging.md):
- log_format_version + phase + operation + operator + operator_role + model_version
- timestamp_utc + system_prompt + user_prompt + parameters

operator_role (added v1.1 for Brand Spectrometer T4-RE pipeline + Paper B cross-operator
discipline): one of {"renderer", "extractor", "orchestrator"} or None for unspecified.
Renderer infers structured output from inputs; extractor recovers a structured
representation from rendered prose; orchestrator coordinates the pipeline.

cost_usd_est auto-population (added v1.2): when the caller does not call
set_cost_estimate, _build_row computes a fallback estimate from PRICE_TABLE[model_version]
and the captured token counts. Callers should still override via set_cost_estimate
when actual billed cost differs from list (promotional discounts, prompt caching
credits, batch-API rates).
- request_id + endpoint + sdk_version
- response + response_metadata + tokens + latency_seconds + cost_usd_est
- errors + retries + git_sha_caller + python_env_hash + human_in_loop +
  reconstructed_post_hoc

Redaction discipline enforced at write time:
- API key values stripped if accidentally embedded
- BWS-secret-value patterns stripped
- Authorization headers stripped
- Internal-file references (PENDING_UPDATES, SESSION_*_COMPLETION, etc.) flagged

Logs land at <repo>/logs/<jsonl-file>.
"""

from __future__ import annotations

import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

LOG_FORMAT_VERSION = "1.2"

# Default logs directory relative to this script.
DEFAULT_LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"

# Per-provider price table (USD per 1M tokens). Used to auto-populate
# cost_usd_est at write time when the caller did not call set_cost_estimate.
# Prices reflect May 2026 list-price tiers; promotional discounts (e.g.,
# DeepSeek V4 Pro 75% off through 2026-05-31) are NOT applied here — the
# caller should override via set_cost_estimate when actual billed cost
# differs from list. Keys are exact model-version strings as passed to
# `operator` or `model_version`.
PRICE_TABLE: dict[str, dict[str, float]] = {
    # Anthropic
    "claude-opus-5": {"input": 5.00, "output": 25.00},
    "claude-opus-4-8": {"input": 5.00, "output": 25.00},
    "claude-opus-4-7": {"input": 5.00, "output": 25.00},
    "claude-sonnet-5": {"input": 3.00, "output": 15.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-fable-5": {"input": 10.00, "output": 50.00},
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
    # OpenAI
    "gpt-5.5-2026-04-23": {"input": 5.00, "output": 30.00},
    "gpt-5.5": {"input": 5.00, "output": 30.00},
    "gpt-5.4-mini-2026-03-17": {"input": 0.55, "output": 2.20},
    "gpt-5.4-mini": {"input": 0.55, "output": 2.20},
    "gpt-4o-2024-11-20": {"input": 2.50, "output": 10.00},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini-2024-07-18": {"input": 0.15, "output": 0.60},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    # Alibaba DashScope (Qwen)
    "qwen3.7-max": {"input": 2.50, "output": 7.50},
    "qwen-max": {"input": 2.50, "output": 7.50},
    "qwen-plus": {"input": 0.50, "output": 1.50},
    "qwen-turbo": {"input": 0.10, "output": 0.30},
    # DeepSeek (cache-miss list pricing; promo windows applied by caller)
    "deepseek-v4-flash": {"input": 0.14, "output": 0.28},
    "deepseek-v4-pro": {"input": 1.74, "output": 3.48},
    "deepseek-chat": {"input": 0.27, "output": 1.10},
    "deepseek-coder": {"input": 0.27, "output": 1.10},
    # Perplexity (May 2026 list; discovery operator_role only per
    # reference_perplexity_role_in_t4_re). Excludes per-request search
    # surcharges, which the caller should add via set_cost_estimate.
    "sonar": {"input": 1.00, "output": 1.00},
    "sonar-pro": {"input": 3.00, "output": 15.00},
    "sonar-reasoning": {"input": 1.00, "output": 5.00},
    # xAI Grok (June 2026 list; OpenAI-compatible endpoint)
    "grok-4.3": {"input": 1.25, "output": 2.50},
}


def _compute_cost_from_tokens(model_version: str, tokens: dict[str, int]) -> float:
    """Compute cost_usd_est from token counts using PRICE_TABLE.

    Returns 0.0 if model_version is unknown or token counts are missing.
    Callers should override via set_cost_estimate when billed cost differs
    from list (e.g., promotional discounts, prompt caching credits).
    """
    if not model_version or model_version not in PRICE_TABLE:
        return 0.0
    prices = PRICE_TABLE[model_version]
    input_tokens = tokens.get("input", 0) if isinstance(tokens, dict) else 0
    output_tokens = tokens.get("output", 0) if isinstance(tokens, dict) else 0
    return (
        input_tokens * prices["input"] + output_tokens * prices["output"]
    ) / 1_000_000.0


# Patterns to redact from any prompt / response / parameters field before writing.
REDACT_PATTERNS = [
    # API key fragments (Anthropic / OpenAI / DeepSeek / etc.)
    (re.compile(r"sk-[A-Za-z0-9_\-]{20,}", re.IGNORECASE), "[REDACTED:api_key]"),
    (
        re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}", re.IGNORECASE),
        "[REDACTED:anthropic_key]",
    ),
    (
        re.compile(r"sk-proj-[A-Za-z0-9_\-]{20,}", re.IGNORECASE),
        "[REDACTED:openai_proj_key]",
    ),
    # Yandex IAM tokens
    (re.compile(r"AQVN[A-Za-z0-9_\-]{60,}"), "[REDACTED:yandex_iam]"),
    # Generic Bearer tokens
    (re.compile(r"Bearer\s+[A-Za-z0-9._\-]{20,}"), "Bearer [REDACTED:token]"),
    # Authorization headers in URLs
    (
        re.compile(r"Authorization:\s*[A-Za-z]+\s+[A-Za-z0-9._\-]{20,}"),
        "Authorization: [REDACTED]",
    ),
]

# Internal-doc references that must NOT leak into public logs.
INTERNAL_DOC_PATTERNS = [
    re.compile(r"PENDING_UPDATES\.md", re.IGNORECASE),
    re.compile(r"SESSION_[A-Z](?:_COMPLETION|_HANDOFF|_INIT)", re.IGNORECASE),
    re.compile(r"TRIAGE_MEMO_", re.IGNORECASE),
    re.compile(r"AUDIT_INTERNAL_", re.IGNORECASE),
]


def _redact(text: str) -> tuple[str, list[str]]:
    """Apply redaction patterns; return (redacted_text, list_of_warnings)."""
    if not isinstance(text, str):
        return text, []
    out = text
    warnings: list[str] = []
    for pattern, replacement in REDACT_PATTERNS:
        if pattern.search(out):
            out = pattern.sub(replacement, out)
    for pattern in INTERNAL_DOC_PATTERNS:
        if pattern.search(out):
            warnings.append(
                f"internal-doc reference matched pattern '{pattern.pattern}' — "
                "review for redaction before public mirror"
            )
    return out, warnings


def _redact_recursive(obj: Any) -> tuple[Any, list[str]]:
    warnings: list[str] = []
    if isinstance(obj, str):
        out, w = _redact(obj)
        warnings.extend(w)
        return out, warnings
    if isinstance(obj, dict):
        out_dict: dict[str, Any] = {}
        for k, v in obj.items():
            redacted_v, w = _redact_recursive(v)
            warnings.extend(w)
            out_dict[k] = redacted_v
        return out_dict, warnings
    if isinstance(obj, list):
        out_list: list[Any] = []
        for v in obj:
            redacted_v, w = _redact_recursive(v)
            warnings.extend(w)
            out_list.append(redacted_v)
        return out_list, warnings
    return obj, warnings


def _git_sha() -> str:
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
        )
        return sha.decode().strip()
    except Exception:
        return "unknown"


def _env_hash() -> str:
    """Hash a deterministic representation of the Python environment.

    Prefers `uv.lock` SHA if present; falls back to sys.version_info.
    """
    repo_root = Path(__file__).resolve().parents[3]
    uv_lock = repo_root / "uv.lock"
    if uv_lock.exists():
        return hashlib.sha256(uv_lock.read_bytes()).hexdigest()[:16]
    return hashlib.sha256(sys.version.encode()).hexdigest()[:16]


@dataclass
class _CallLogger:
    """Mutable buffer assembled inside the `log_call` context manager."""

    phase: str
    operation: str
    operator: str
    operator_role: str | None = None
    endpoint: str = ""
    sdk_version: str = ""
    logs_dir: Path = field(default_factory=lambda: DEFAULT_LOGS_DIR)
    human_in_loop: bool = False
    reconstructed_post_hoc: bool = False

    _start_time: float = 0.0
    _system_prompt: str = ""
    _user_prompt: str = ""
    _parameters: dict[str, Any] = field(default_factory=dict)
    _response: str = ""
    _response_metadata: dict[str, Any] = field(default_factory=dict)
    _model_version: str = ""
    _request_id: str | None = None
    _tokens: dict[str, int] = field(default_factory=dict)
    _cost_usd_est: float = 0.0
    _errors: list[str] = field(default_factory=list)
    _retries: int = 0
    _redaction_warnings: list[str] = field(default_factory=list)

    def set_system_prompt(self, text: str) -> None:
        self._system_prompt = text

    def set_user_prompt(self, text: str) -> None:
        self._user_prompt = text

    def set_parameters(self, params: dict[str, Any]) -> None:
        self._parameters = dict(params)

    def set_model_version(self, model_version: str) -> None:
        self._model_version = model_version

    def set_cost_estimate(self, usd: float) -> None:
        self._cost_usd_est = usd

    def add_error(self, msg: str) -> None:
        self._errors.append(msg)

    def increment_retry(self) -> None:
        self._retries += 1

    def capture_response(self, response: Any) -> None:
        """Best-effort capture of response text + metadata + tokens.

        Supports common SDK response shapes:
        - Anthropic Messages API (.content[0].text + .usage)
        - OpenAI ChatCompletion (.choices[0].message.content + .usage)
        - Raw dict / string
        """
        # Anthropic
        if hasattr(response, "content") and hasattr(response, "usage"):
            try:
                self._response = response.content[0].text  # type: ignore[attr-defined]
            except Exception:
                self._response = str(response.content)
            usage = response.usage
            self._tokens = {
                "input": getattr(usage, "input_tokens", 0),
                "output": getattr(usage, "output_tokens", 0),
            }
            self._model_version = self._model_version or getattr(response, "model", "")
            self._request_id = getattr(response, "id", None)
            return

        # OpenAI / DeepSeek (openai-compatible)
        if hasattr(response, "choices") and hasattr(response, "usage"):
            try:
                self._response = response.choices[0].message.content  # type: ignore[attr-defined]
            except Exception:
                self._response = str(response.choices)
            usage = response.usage
            self._tokens = {
                "input": getattr(usage, "prompt_tokens", 0),
                "output": getattr(usage, "completion_tokens", 0),
            }
            self._model_version = self._model_version or getattr(response, "model", "")
            self._request_id = getattr(response, "id", None)
            try:
                self._response_metadata = {
                    "finish_reason": response.choices[0].finish_reason  # type: ignore[attr-defined]
                }
            except Exception:
                pass
            return

        # Dict-shaped response (raw HTTP fallback, e.g. Perplexity via httpx)
        if isinstance(response, dict):
            self._response_metadata = {
                k: v for k, v in response.items() if k != "choices"
            }
            try:
                self._response = response["choices"][0]["message"]["content"]
            except Exception:
                try:
                    self._response = response["result"]["alternatives"][0]["message"][
                        "text"
                    ]
                except Exception:
                    self._response = json.dumps(response)
            # Extract usage / id / model from the OpenAI-compatible shape so
            # tokens + cost_usd_est populate for raw-HTTP callers too.
            usage = response.get("usage")
            if isinstance(usage, dict):
                self._tokens = {
                    "input": usage.get("prompt_tokens", usage.get("input_tokens", 0)),
                    "output": usage.get(
                        "completion_tokens", usage.get("output_tokens", 0)
                    ),
                }
            if response.get("id") and self._request_id is None:
                self._request_id = response.get("id")
            if response.get("model") and not self._model_version:
                self._model_version = response.get("model")
            return

        # String / unknown — capture as-is
        self._response = str(response)

    def _build_row(self) -> dict[str, Any]:
        latency = max(time.time() - self._start_time, 0.0)
        # Redact prompts + response + parameters recursively
        sys_prompt, w1 = _redact(self._system_prompt)
        user_prompt, w2 = _redact(self._user_prompt)
        response, w3 = _redact(self._response)
        params, w4 = _redact_recursive(self._parameters)
        resp_meta, w5 = _redact_recursive(self._response_metadata)
        self._redaction_warnings.extend(w1 + w2 + w3 + w4 + w5)
        return {
            "log_format_version": LOG_FORMAT_VERSION,
            "phase": self.phase,
            "operation": self.operation,
            "operator": self.operator,
            "operator_role": self.operator_role,
            "model_version": self._model_version,
            "timestamp_utc": dt.datetime.now(dt.timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "system_prompt": sys_prompt,
            "user_prompt": user_prompt,
            "parameters": params,
            "request_id": self._request_id,
            "endpoint": self.endpoint,
            "sdk_version": self.sdk_version,
            "response": response,
            "response_metadata": resp_meta,
            "tokens": self._tokens,
            "latency_seconds": round(latency, 3),
            "cost_usd_est": round(
                self._cost_usd_est
                or _compute_cost_from_tokens(self._model_version, self._tokens),
                5,
            ),
            "errors": self._errors,
            "retries": self._retries,
            "git_sha_caller": _git_sha(),
            "python_env_hash": _env_hash(),
            "human_in_loop": self.human_in_loop,
            "reconstructed_post_hoc": self.reconstructed_post_hoc,
        }

    def write(self) -> Path:
        """Write the assembled JSONL row to disk; return path."""
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        filename = f"phase_{self.phase}_{self.operation}_calls.jsonl"
        # Sanitize filename
        filename = re.sub(r"[^\w\.\-]", "_", filename)
        out_path = self.logs_dir / filename
        row = self._build_row()
        with out_path.open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        if self._redaction_warnings:
            warning_path = self.logs_dir / "REDACTION_WARNINGS.log"
            with warning_path.open("a") as f:
                for w in self._redaction_warnings:
                    f.write(
                        f"{dt.datetime.now(dt.timezone.utc).isoformat()} "
                        f"{filename} {w}\n"
                    )
        return out_path


@contextlib.contextmanager
def log_call(
    *,
    phase: str,
    operation: str,
    operator: str,
    operator_role: str | None = None,
    endpoint: str = "",
    sdk_version: str = "",
    logs_dir: Path | None = None,
    human_in_loop: bool = False,
    reconstructed_post_hoc: bool = False,
) -> Iterator[_CallLogger]:
    """Context manager that times a call and writes a JSONL row on exit."""
    logger = _CallLogger(
        phase=phase,
        operation=operation,
        operator=operator,
        operator_role=operator_role,
        endpoint=endpoint,
        sdk_version=sdk_version,
        logs_dir=logs_dir or DEFAULT_LOGS_DIR,
        human_in_loop=human_in_loop,
        reconstructed_post_hoc=reconstructed_post_hoc,
    )
    logger._start_time = time.time()
    try:
        yield logger
    except Exception as e:
        logger.add_error(f"{type(e).__name__}: {e}")
        logger.write()
        raise
    logger.write()


def log_call_post_hoc(
    *,
    phase: str,
    operation: str,
    operator: str,
    model_version: str,
    system_prompt: str,
    user_prompt: str,
    response: str,
    operator_role: str | None = None,
    parameters: dict[str, Any] | None = None,
    endpoint: str = "harness-internal",
    sdk_version: str = "claude-code-harness",
    tokens: dict[str, int] | None = None,
    cost_usd_est: float = 0.0,
    timestamp_utc: str | None = None,
    logs_dir: Path | None = None,
    human_in_loop: bool = True,
) -> Path:
    """Convenience: write a reconstructed-post-hoc JSONL row in one call.

    Use for Claude Code harness work that happened before the logger was built.
    Sets reconstructed_post_hoc=True so reviewers can distinguish real-time
    logged calls from post-hoc reconstructions.
    """
    logger = _CallLogger(
        phase=phase,
        operation=operation,
        operator=operator,
        operator_role=operator_role,
        endpoint=endpoint,
        sdk_version=sdk_version,
        logs_dir=logs_dir or DEFAULT_LOGS_DIR,
        human_in_loop=human_in_loop,
        reconstructed_post_hoc=True,
    )
    logger._start_time = time.time()  # latency won't be meaningful for reconstructions
    logger.set_system_prompt(system_prompt)
    logger.set_user_prompt(user_prompt)
    logger.set_parameters(parameters or {})
    logger.set_model_version(model_version)
    if cost_usd_est:
        logger.set_cost_estimate(cost_usd_est)
    if tokens:
        logger._tokens = tokens
    logger._response = response
    if timestamp_utc:
        # override timestamp for true post-hoc reconstruction
        row = logger._build_row()
        row["timestamp_utc"] = timestamp_utc
        # rewrite directly
        logger.logs_dir.mkdir(parents=True, exist_ok=True)
        filename = re.sub(
            r"[^\w\.\-]", "_", f"phase_{logger.phase}_{logger.operation}_calls.jsonl"
        )
        out_path = logger.logs_dir / filename
        with out_path.open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return out_path
    return logger.write()


if __name__ == "__main__":
    # Smoke test
    with log_call(
        phase="0_test",
        operation="smoke_test",
        operator="self",
        endpoint="local",
        sdk_version="llm_call_logger 1.0",
    ) as lg:
        lg.set_system_prompt("test system prompt")
        lg.set_user_prompt("test user prompt")
        lg.set_parameters({"temperature": 0.0, "max_tokens": 100})
        lg.set_model_version("test-model-v0")
        lg.capture_response({"choices": [{"message": {"content": "ok"}}]})
        lg.set_cost_estimate(0.0)
    print("Smoke test wrote JSONL row to logs/")
