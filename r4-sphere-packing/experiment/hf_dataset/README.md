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
  - competitive-interference
  - perception-space
size_categories:
  - n<1K
---

# Experiment C: Competitive Interference in Perception Space

## Overview

This dataset contains raw LLM responses from Experiment C of the Spectral Brand Theory (SBT) research program. The experiment tests whether the presence of a competitor alters a brand's spectral profile in LLM-mediated perception.

## Research Question

Does the presence of a competitor alter a brand's spectral profile? If so, does the magnitude and direction of shift depend on competitor proximity in perception space?

## Design

- **Focal brands**: Hermes, IKEA, Patagonia, Erewhon, Tesla
- **Competitor types**: Direct, Adjacent, Distant (3 per brand)
- **Conditions**: Solo (baseline), Self-Control (format bias check), Paired (explicit comparison), Context (ambient competitive context)
- **Models**: Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Grok 4.1 Fast
- **Temperature**: 0.7
- **Dimension order**: Latin-square balanced (8 cyclic orderings)

## Hypotheses (Pre-Registered)

- **H1**: Spectral profiles shift when a competitor is present vs solo (Bonferroni-corrected for 8 dimensions)
- **H2**: Direct competitors produce larger profile shifts than distant competitors
- **H3**: Brands differentiate away from competitors on shared dimensions (contrast) and toward on distinctive dimensions (assimilation)

## File Structure

```
data/exp_competitive_interference.jsonl   # Raw JSONL (one record per API call)
prompts/                                   # Prompt templates and brand profiles
analysis/                                  # Statistical results and summary
protocol/                                  # Pre-registered protocol
```

## JSONL Schema

Each record contains 23 fields (20 standard + 3 experiment-specific):

| Field | Type | Description |
|-------|------|-------------|
| timestamp | string | ISO 8601 timestamp |
| model | string | Short model name |
| model_id | string | Full model identifier |
| prompt_type | string | solo_evaluation, self_control_evaluation, paired_evaluation, context_evaluation |
| brand | string | Focal brand name |
| run | int | Repetition number |
| prompt | string | Full prompt text |
| response | string | Raw LLM response |
| parsed | object | Parsed JSON from response |
| weights | object | Extracted 8-dimension weights (null if parse failed) |
| error | string | Error message (null if successful) |
| latency_ms | int | Response time in milliseconds |
| temperature | float | 0.7 |
| dimension_order | int | Latin-square ordering index (0-7) |
| competitor | string | Competitor brand name (null for solo/self_control) |
| competitor_type | string | direct, adjacent, distant, self, or null |
| condition | string | solo, self_control, paired, or context |

## Citation

```bibtex
@misc{zharnikov2026competitive,
  author = {Zharnikov, Dmitry},
  title = {Competitive Interference in Perception Space: LLM Experiment Data},
  year = {2026},
  publisher = {Hugging Face},
  url = {https://huggingface.co/datasets/spectralbranding/exp-competitive-interference}
}
```

## Related Papers

- Zharnikov (2026d). Sphere Packing in Perception Space. Zenodo.
- Zharnikov (2026v). Spectral Metamerism in AI-Mediated Brand Perception. Zenodo.
- Zharnikov (2026a). Spectral Brand Theory. Zenodo.

## License

CC-BY-4.0
