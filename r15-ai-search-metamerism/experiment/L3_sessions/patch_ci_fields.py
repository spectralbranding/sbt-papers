#!/usr/bin/env python3
"""Post-hoc patch: add CI validator required fields to experiment JSONL.

The validate.py CI check requires every JSONL record to have:
  - model (str): short model name matching models.yaml keys
  - prompt_type (str): one of the enum values
  - prompt (str): full rendered prompt text

Run AFTER the experiment completes (append-only JSONL must not be mid-write).

Usage:
    python patch_ci_fields.py exp_primacy_generalization.jsonl
"""

import json
import sys
from pathlib import Path

MODEL_MAP = {
    "claude-haiku-4-5-20251001": "claude",
    "claude-haiku-4-5": "claude",
    "gpt-4o-mini": "gpt",
    "gemini-2.5-flash": "gemini",
    "deepseek-chat": "deepseek",
    "grok-4-1-fast-non-reasoning": "grok",
}


def patch_file(path: Path) -> None:
    records = []
    patched = 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)

            changed = False
            if "model" not in r:
                r["model"] = MODEL_MAP.get(r.get("model_id", ""), "unknown")
                changed = True
            if "prompt_type" not in r:
                r["prompt_type"] = "weighted_recommendation"
                changed = True
            if "prompt" not in r:
                r["prompt"] = r.get("user_prompt", "")
                changed = True

            if changed:
                patched += 1
            records.append(r)

    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Patched {patched}/{len(records)} records in {path.name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default: patch the primacy experiment JSONL
        target = Path(__file__).parent / "exp_primacy_generalization.jsonl"
    else:
        target = Path(sys.argv[1])

    if not target.exists():
        print(f"ERROR: {target} not found")
        sys.exit(1)

    patch_file(target)
