# L1 Configuration

Model configuration registry for R15. This is the source of truth for which models
participated in each run, their API endpoints, tier classification, and cultural attribution.

## Contents

| File | Contents |
|------|----------|
| `models.yaml` | Full model registry: 21 active models across 7 cultural clusters |

## Model Summary

- **Total active**: 21 models
- **Runs 2-4**: 6 models (Claude Sonnet 4.6, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Qwen3 30B, Gemma 4 27B)
- **Run 5 additions**: 15 models spanning Chinese, Russian, Japanese, Korean, Arabic, and Indian clusters

## Tier Classification

- **Tier 1 (30B+ parameters)**: Primary analysis models
- **Tier 2 (7-30B parameters)**: H9 capacity comparison models

## Excluded Models

- **T-Pro 2.0** (`tpro_yandex`): Requires dedicated paid instance ($6.20/hr).
  Not available as free-tier API endpoint. Excluded from study. Config retained for reference.

## Usage

The `ai_search_metamerism.py` script reads model configuration at runtime from this file
to resolve API endpoints, key environment variables, and tier assignments.
