---
license: cc-by-4.0
task_categories:
  - text-generation
language:
  - en
tags:
  - brand-perception
  - spectral-branding
  - format-optimization
  - ai-measurement
  - brand-function
size_categories:
  - n<1K
---

# Experiment D: Brand Function Format Optimization

## Dataset Description

375 LLM responses testing which representational format of brand function specifications maximizes AI comprehension fidelity. Part of the Spectral Branding Theory (SBT) research program.

### Summary

- **Experiment**: Brand Function Format Optimization (Experiment D)
- **Paper**: R16 AI-Native Brand Identity (Zharnikov, 2026x)
- **Total calls**: 375 (355 valid, 20 parse errors, 0 failures)
- **Cost**: $0.13
- **Models**: 5 (Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Grok 4.1 Fast)
- **Brands**: 5 canonical SBT brands (Hermes, IKEA, Patagonia, Tesla, Erewhon)
- **Format conditions**: 5 (JSON structured, prose narrative, tabular minimal, ranked list, score-only vector)
- **Repetitions**: 3 per cell
- **Design**: 5 formats x 5 brands x 5 models x 3 reps

### Key Findings

1. **Score-Only Vector wins** (mean cosine .998): Contrary to H1, the minimal format -- bare numbers with dimension labels -- produced the highest fidelity. LLMs reconstruct canonical profiles nearly perfectly from scores alone.
2. **Prose Narrative penalized** (mean cosine .941, d = 1.23 vs JSON): H2 supported. Unstructured text introduces noise; LLM priors dominate over specification content.
3. **Format ranking consistent across models** (Kendall's W = .84): H4 supported. All 5 architectures agree: F5 > F3 > F4 >= F1 > F2.
4. **ANOVA highly significant**: F(4,350) = 51.19, p < .001, eta-sq = .369.
5. **No hard/soft dimension asymmetry**: H5 not supported. Format choice affects all dimensions roughly equally.

### Practical Implication

For brand function deployment, include numerical scores prominently. Prose descriptions add noise rather than signal when the goal is AI comprehension fidelity. The optimal brand function format is structured with explicit scores -- JSON with numbers is better than JSON with only prose.

## Dataset Structure

Each JSONL record contains 23+ fields including:
- `experiment`, `model_id`, `model_provider`
- `brand`, `condition` (F1-F5), `repetition`
- `user_prompt`, `raw_response`
- `parsed_weights` (8-dimensional allocation)
- `canonical_cosine` (similarity to ground truth)
- `dci` (Dimensional Collapse Index)
- `dimension_order` (Latin-square balanced)
- Token counts, response time, cost

## Citation

```bibtex
@misc{zharnikov2026x,
  title={AI-Native Brand Identity: From Human Semiotics to Machine-Readable Brand Functions},
  author={Zharnikov, Viacheslav},
  year={2026},
  doi={10.5281/zenodo.19391476}
}
```

## License

CC-BY-4.0
