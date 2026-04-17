---
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
    num_examples: 2400
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

This dataset contains 2400 API responses (2351 valid) from 5 LLMs
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
