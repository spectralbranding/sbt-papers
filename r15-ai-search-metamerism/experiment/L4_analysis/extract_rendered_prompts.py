#!/usr/bin/env python3
"""Extract one rendered example per prompt_type from L3 session logs.

Writes to ../L2_prompts/rendered/example_<prompt_type>.txt for each unique
prompt_type encountered. Used to keep L2_prompts/rendered/ in sync after
new runs are added.

Usage:
    cd experiment
    python L4_analysis/extract_rendered_prompts.py
"""

from __future__ import annotations

import json
from pathlib import Path

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
L3_DIR = EXPERIMENT_DIR / "L3_sessions"
RENDERED_DIR = EXPERIMENT_DIR / "L2_prompts" / "rendered"

# Prompt types that were constructed with the original "dirty" design:
# native-language instructions wrapped around English brand/city/category
# content tokens. These are the prompts documented in paper Section 4.5
# as the mixed-language limitation. Run 11 introduces *_clean_native
# variants that localize the content tokens as well; until Run 11 is
# executed, the dirty examples here are labeled with a warning banner
# so a reader of the repo immediately sees the caveat.
DIRTY_NATIVE_PROMPT_TYPES = {
    "weighted_recommendation_native",
    "geopolitical_framing_native",
}

DIRTY_NATIVE_WARNING = (
    "# -----------------------------------------------------------------\n"
    "# WARNING: known methodological limitation\n"
    "# -----------------------------------------------------------------\n"
    "# This example shows the R15 \"dirty native\" prompt design: the\n"
    "# instructions are translated into the target language, but the\n"
    "# brand names, city names, and category labels remain in English.\n"
    "# This is the mixed-language limitation documented in paper\n"
    "# Section 4.5 (H10). The current H10 result is valid only as the\n"
    "# narrow claim \"switching the instruction language alone does not\n"
    "# reduce dimensional collapse.\" A clean-native re-test (Run 11) is\n"
    "# planned: see CONTINUATION_PROMPT.md \"Session 93 Priorities #0b\"\n"
    "# and experiment/L1_configuration/native_localization.yaml for the\n"
    "# prepared translation data. After Run 11, this file will be\n"
    "# regenerated to show the clean-native variant.\n"
    "# -----------------------------------------------------------------\n"
    "\n"
)


def main() -> None:
    RENDERED_DIR.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    examples: list[dict] = []

    for jsonl_file in sorted(L3_DIR.glob("*.jsonl")):
        with jsonl_file.open() as fh:
            for line in fh:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ptype = record.get("prompt_type", "unknown")
                if ptype in seen:
                    continue
                seen.add(ptype)
                examples.append(
                    {
                        "type": ptype,
                        "model": record.get("model"),
                        "pair_id": record.get("pair_id")
                        or record.get("brand_pair", "unknown"),
                        "source_file": jsonl_file.name,
                        "prompt": record.get("prompt", ""),
                        "response": (record.get("response") or "")[:1000],
                    }
                )

    for ex in examples:
        out_path = RENDERED_DIR / f"example_{ex['type']}.txt"
        header = (
            f"# Rendered example: {ex['type']}\n"
            f"# Model: {ex['model']}\n"
            f"# Pair: {ex['pair_id']}\n"
            f"# Source: L3_sessions/{ex['source_file']}\n"
            f"# (First occurrence of this prompt_type across all session files.)\n\n"
        )
        if ex["type"] in DIRTY_NATIVE_PROMPT_TYPES:
            header += DIRTY_NATIVE_WARNING
        out_path.write_text(
            header
            + "================ PROMPT ================\n\n"
            + f"{ex['prompt']}\n\n"
            + "================ RESPONSE (first 1000 chars) ================\n\n"
            + f"{ex['response']}\n"
        )
        print(f"Wrote {out_path.relative_to(EXPERIMENT_DIR)}")

    print(f"\nTotal: {len(examples)} prompt_type examples written")


if __name__ == "__main__":
    main()
