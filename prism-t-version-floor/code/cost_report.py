#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""cost_report.py — post-hoc PL3 cost accounting for the PRISM-T campaign.

The shared llm_call_logger's raw-HTTP dict path stores provider `usage`
inside response_metadata without populating the tokens/cost fields, so the
campaign spend is computed here from the PL3 logs + the PL1 list_prices
table. Read-only.

Run: uv run python research/prism_t/code/cost_report.py
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_t_lib import LOGS_DIR, load_config  # noqa: E402


def usage_of(row: dict) -> tuple[int, int]:
    meta = row.get("response_metadata") or {}
    u = meta.get("usage") or {}
    # Anthropic dict shape
    if "input_tokens" in u:
        return int(u.get("input_tokens", 0)), int(u.get("output_tokens", 0))
    # OpenAI-compatible dict shape
    return int(u.get("prompt_tokens", 0)), int(u.get("completion_tokens", 0))


def main() -> int:
    prices = load_config()["list_prices"]
    calls, spend = defaultdict(int), defaultdict(float)
    missing_usage = 0
    for f in LOGS_DIR.glob("*_calls.jsonl"):
        for line in f.open():
            if not line.strip():
                continue
            row = json.loads(line)
            model = row.get("operator", "?")
            calls[model] += 1
            tin, tout = usage_of(row)
            if tin == 0 and tout == 0:
                missing_usage += 1
                continue
            p = prices.get(model)
            if p:
                spend[model] += (tin * p["input"] + tout * p["output"]) / 1e6
    total_calls = sum(calls.values())
    total = sum(spend.values())
    for m in sorted(spend, key=spend.get, reverse=True):
        print(f"  {m}: {calls[m]} calls, ${spend[m]:.2f}")
    print(
        f"[cost] total: {total_calls} calls, ${total:.2f} (usage missing on {missing_usage})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
