#!/usr/bin/env python3
"""Prepare HuggingFace dataset files for Experiment E.

Reads the JSONL and produces:
  - data/exp_primacy_generalization.jsonl (cleaned, no raw prompts)
  - README.md (dataset card)

Usage:
    python prepare_dataset.py
"""

import json
from pathlib import Path

JSONL_PATH = Path(__file__).parent.parent / "L3_sessions" / "exp_primacy_generalization.jsonl"
OUTPUT_DIR = Path(__file__).parent
DATA_DIR = OUTPUT_DIR / "data"


def clean_record(r: dict) -> dict:
    """Strip verbose fields (full prompts, raw responses) for HF upload."""
    return {
        "timestamp": r.get("timestamp"),
        "experiment": r.get("experiment"),
        "model_id": r.get("model_id"),
        "model_provider": r.get("model_provider"),
        "brand": r.get("brand"),
        "response_format": r.get("response_format"),
        "repetition": r.get("repetition"),
        "ordering_index": r.get("ordering_index"),
        "dimension_order": r.get("dimension_order"),
        "parsed_weights": r.get("parsed_weights"),
        "weights_valid": r.get("weights_valid"),
        "weight_sum_raw": r.get("weight_sum_raw"),
        "position_weights": r.get("position_weights"),
        "response_time_ms": r.get("response_time_ms"),
        "token_count_input": r.get("token_count_input"),
        "token_count_output": r.get("token_count_output"),
        "api_cost_usd": r.get("api_cost_usd"),
    }


def main():
    if not JSONL_PATH.exists():
        print(f"ERROR: {JSONL_PATH} not found. Run the experiment first.")
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    with open(JSONL_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    valid = [r for r in records if r.get("weights_valid")]
    print(f"Total records: {len(records)}, valid: {len(valid)}")

    # Write cleaned JSONL
    out_path = DATA_DIR / "exp_primacy_generalization.jsonl"
    with open(out_path, "w") as f:
        for r in records:
            f.write(json.dumps(clean_record(r), ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} records to {out_path}")

    # Write dataset card
    card = f"""---
dataset_info:
  features:
  - name: timestamp
    dtype: string
  - name: experiment
    dtype: string
  - name: model_id
    dtype: string
  - name: model_provider
    dtype: string
  - name: brand
    dtype: string
  - name: response_format
    dtype: string
  - name: repetition
    dtype: int32
  - name: ordering_index
    dtype: int32
  - name: weights_valid
    dtype: bool
  - name: weight_sum_raw
    dtype: float64
  - name: response_time_ms
    dtype: int32
  - name: api_cost_usd
    dtype: float64
  splits:
  - name: train
    num_examples: {len(records)}
license: cc-by-4.0
task_categories:
- text-generation
language:
- en
tags:
- brand-perception
- llm-evaluation
- survey-methodology
- primacy-effect
- spectral-branding
---

# Experiment E: Primacy Effect Generalization

## Dataset Description

This dataset contains {len(records)} API responses ({len(valid)} valid) from 5 LLMs
evaluating 5 brands across 4 response formats and 8 Latin-square dimension orderings.

**Research question**: Does the serial position of a dimension in the prompt systematically
bias the weight allocated to it, and does this primacy/recency effect generalize across
response formats?

## Design

- **Models**: Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Grok 4.1 Fast
- **Brands**: Hermes, IKEA, Patagonia, Erewhon, Tesla
- **Response formats**: JSON (weights sum to 100), Likert (1-5), Ranking (1-8), Natural Language
- **Orderings**: 8 Latin-square cyclic rotations of 8 SBT dimensions
- **Repetitions**: 3 per cell
- **Temperature**: 0.7

## Key Fields

- `response_format`: json, likert, ranking, nl
- `ordering_index`: 0-7 (Latin-square rotation index)
- `dimension_order`: list of 8 dimension names in prompt order
- `parsed_weights`: dict of dimension -> weight (normalized to 0-100 scale)
- `position_weights`: dict of position (1-8) -> weight

## Citation

Part of the Spectral Branding Theory (SBT) research program.
Paper: Zharnikov (2026v), "Spectral Metamerism in AI-Mediated Brand Perception."
"""
    card_path = OUTPUT_DIR / "README.md"
    with open(card_path, "w") as f:
        f.write(card)
    print(f"Wrote dataset card to {card_path}")


if __name__ == "__main__":
    main()
