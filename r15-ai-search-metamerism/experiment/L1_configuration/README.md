# L1 Configuration

Model configuration registry for R15. This is the source of truth for which models
participated in each run, their API endpoints, tier classification, and cultural attribution.

## Contents

| File | Contents |
|------|----------|
| `models.yaml` | Full model registry: 22 configured models across 7 cultural clusters |

## Model Summary

- **Total configured**: 22 models
- **Active in Run 5 analysis**: 21 models (T-Pro 2.0 excluded — 0 successful responses)
- **Runs 2-4**: 6 models (Claude Sonnet 4.6, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Qwen3 30B, Gemma 4 27B)
- **Run 5 additions**: 16 models spanning Chinese, Russian, Japanese, Korean, Arabic, and Indian clusters

## Tier Classification

- **Tier 1 (30B+ parameters)**: Primary analysis models
- **Tier 2 (7-30B parameters)**: H9 capacity comparison models

## Excluded Models

- **T-Pro 2.0** (`tpro_yandex`): Configured for Run 5 but produced 0 successful responses.
  Excluded from all analysis tables. The entry is retained in models.yaml for reproducibility.

## Usage

The `ai_search_metamerism.py` script reads model configuration at runtime from this file
to resolve API endpoints, key environment variables, and tier assignments.
