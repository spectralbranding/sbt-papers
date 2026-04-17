---
license: cc-by-4.0
task_categories:
  - text-generation
language:
  - en
tags:
  - brand-perception
  - spectral-brand-theory
  - ai-shopping
  - agentic-commerce
  - dimensional-collapse
pretty_name: "Experiment A: Multi-Step Agentic Collapse in AI Shopping Pipelines"
size_categories:
  - n<1K
---

# Experiment A: Multi-Step Agentic Collapse in AI Shopping Pipelines

## Summary

This dataset tests whether dimensional collapse compounds across steps in a simulated AI shopping pipeline. Five LLMs (Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Grok 4.1 Fast) evaluate 5 canonical brands across a 3-step multi-turn conversation (retrieval, comparison, recommendation) plus a single-step PRISM-B control.

Each pipeline is a **real multi-turn conversation** -- Step 1's response becomes the assistant message in Step 2's history, and Step 2's response feeds into Step 3. This simulates actual agentic commerce where context accumulates.

## Key Findings

- **H1 (Monotonic DCI increase)**: NOT SUPPORTED at p < .05 (p = .051), but trend is monotonic (control .238 -> step 2 .246 -> step 3 .267). The control-to-step-3 comparison is significant after Bonferroni correction (p = .046, d = .454).
- **H2 (Dimension-specific compounding)**: SUPPORTED. Cultural dimension collapses more than Economic across pipeline steps (Cultural delta = -1.035, Economic delta = +0.925).
- **H3 (Ideological signal protection)**: SUPPORTED. Patagonia (strong Ideological signal) compounds less than Erewhon/Tesla (weak Ideological signal), d = .88, p = .024.

## Dataset Structure

    data/exp_agentic_collapse.jsonl    # 300 records, one per API call
    prompts/
      system_prompts.json              # System prompts for pipeline and control
      brand_profiles.json              # Canonical 8-dimension profiles
      experiment_config.yaml           # Full experiment configuration
    analysis/
      exp_agentic_collapse_results.json  # Statistical results
      exp_agentic_collapse_summary.md    # Human-readable summary
    protocol/
      EXP_AGENTIC_COLLAPSE_PROTOCOL.md   # Pre-registered protocol

## JSONL Schema

Each record contains 29 fields including:

| Field | Description |
|-------|-------------|
| step | 0=control, 1=retrieval, 2=comparison, 3=recommendation |
| conversation_id | UUID linking all 3 steps of a pipeline |
| conversation_history | Full multi-turn message history at time of call |
| parsed_weights | Extracted dimension weights (8 dimensions, sum to 100) |
| model_id | LLM model identifier |
| brand | Evaluated brand |
| competitor | Brand used in Step 2 comparison |
| recommended_brand | Brand recommended in Step 3 |

## Methodology

- **Temperature**: 0.7 for all models
- **Dimension ordering**: Latin-square balanced (8 cyclic rotations)
- **Random seed**: 42
- **Inter-call delay**: 3 seconds
- **Conversation type**: Real multi-turn (accumulated context)

## Citation

    Zharnikov, D. (2026). Spectral Metamerism in AI-Mediated Brand Perception.

## License

CC-BY-4.0
