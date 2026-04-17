---
license: cc-by-4.0
task_categories:
  - text-classification
language:
  - en
tags:
  - brand-perception
  - llm-evaluation
  - spectral-brand-theory
  - agentic-commerce
  - dimensional-collapse
  - PRISM-B
pretty_name: "Compounding x Format: Specification Framing in Agentic Pipelines"
size_categories:
  - 1K<n<10K
---

# Compounding x Format: Specification Framing in Agentic Pipelines

Two experiments testing whether specification framing attenuates or amplifies dimensional collapse across multi-step agentic shopping pipelines.

## Dataset Description

**Paper**: Zharnikov, D. (2026). Dimensional Collapse in AI-Mediated Brand Perception: Large Language Models as Metameric Observers. DOI: [10.5281/zenodo.19422427](https://doi.org/10.5281/zenodo.19422427)

**Section**: 5.16 (Specification Paradox)

**Key finding**: The *specification paradox* — Brand Function specification works in single-step contexts (reducing DCI toward uniform baseline) but **amplifies** distortion in multi-step agentic pipelines (d = .820, p < .001). Constraint framing ("distribute attention equally") is tested as an alternative in v2.

## Experiments

### v1: Information Framing (480 calls)
- **Conditions**: baseline (no spec) vs information (Brand Function scores in system prompt)
- **Models**: Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek Chat, Grok 4.1 Fast, Gemma 4 (local)
- **Result**: H_CF1 REVERSED. Specification amplifies compounding (delta +1.295 vs +.274)

### v2: Constraint Framing (600 calls)
- **Conditions**: baseline vs information vs constraint ("distribute weight equally across all eight dimensions")
- **Models**: Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek Chat, Grok 4.1 Fast
- **Result**: [pending v2 completion]

## Pipeline Structure

Three-step single conversation (mirrors Exp A):
1. **Step 1**: Recommend 5 brands in category (free text)
2. **Step 2**: Compare focal brand vs competitor on 8 dimensions (100-point allocation)
3. **Step 3**: Final recommendation with 8-dimension weights (100-point allocation)
4. **Control**: Single PRISM-B call (no pipeline context)

## Brands

Hermes, Patagonia, Erewhon, Tesla, IKEA (canonical SBT profiles)

## JSONL Schema

Each record contains:
- `experiment`: experiment identifier
- `model_id`, `model_provider`: model metadata
- `brand`, `condition` (step_1/step_2/step_3/control), `bf_condition` (baseline/information/constraint)
- `system_prompt`, `user_prompt`, `raw_response`: full prompt-response chain
- `parsed_weights`: dict of 8 dimensions to float values (sum ~100)
- `conversation_id`, `conversation_turn`, `conversation_history`: multi-turn context
- `dim_order`: Latin-square dimension ordering
- `api_cost_usd`, `response_time_ms`, `token_count_input`, `token_count_output`

## DCI (Dimensional Collapse Index)

DCI = mean(|w_i - 12.5|) for all 8 dimensions. Baseline = 12.5 (uniform allocation = 100/8). Higher DCI = more collapse.

## Files

| File | Records | Description |
|------|---------|-------------|
| exp_compounding_format.jsonl | 480 | v1: baseline vs information |
| exp_compounding_format_v2.jsonl | 600 | v2: baseline vs information vs constraint |

## Protocol

Full experiment protocol (pre-registration style) with hypotheses, power analysis, and statistical test plan: [EXP_COMPOUNDING_FORMAT_PROTOCOL.md](https://github.com/spectralbranding/sbt-papers/tree/main/r15-ai-search-metamerism/experiment/L0_specification/EXP_COMPOUNDING_FORMAT_PROTOCOL.md)

## Citation

```bibtex
@article{zharnikov2026v,
  title={Dimensional Collapse in AI-Mediated Brand Perception: Large Language Models as Metameric Observers},
  author={Zharnikov, Dmitry},
  year={2026},
  journal={Working Paper},
  doi={10.5281/zenodo.19422427}
}
```

## License

CC-BY-4.0
