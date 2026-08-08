---
license: cc-by-4.0
language:
  - en
size_categories:
  - n<1K
task_categories:
  - text-generation
  - feature-extraction
tags:
  - spectral-brand-theory
  - exp-bf-format
  - r16
  - brand-perception
  - format-optimization
  - ai-measurement
  - brand-function
pretty_name: "Brand Function Format Optimization (Exp D)"
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/*.jsonl
citation: |
  @article{zharnikov2026r16,
    author = {Dmitry Zharnikov},
    title = {AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification},
    year = {2026},
    doi = {10.5281/zenodo.19391476}
  }
paperswithcode_id: null
---

# Brand Function Format Optimization (Exp D)

## Dataset Summary

375 LLM responses (355 valid, 20 parse errors, 0 failures) testing which representational format of a brand function specification maximizes AI comprehension fidelity. Five formats (JSON structured, prose narrative, tabular minimal, ranked list, score-only vector) were crossed with five canonical SBT brands (Hermes, IKEA, Patagonia, Tesla, Erewhon), five model families (Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Grok 4.1 Fast), and three repetitions per cell. Total experiment cost: $0.13.

Companion paper: [AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification](https://doi.org/10.5281/zenodo.19391476) (Zharnikov, 2026). ORCID 0009-0000-6893-9231.

Companion GitHub repository: https://github.com/spectralbranding/sbt-papers/tree/main/r16-ai-native-brand-identity containing the analysis code, prompts, and reproduction pipeline.

### Key Findings

1. **Score-Only Vector wins** (mean cosine .998): contrary to H1, the minimal format -- bare numbers with dimension labels -- produced the highest fidelity. LLMs reconstruct canonical profiles nearly perfectly from scores alone.
2. **Prose Narrative penalized** (mean cosine .941, Cohen's d = 1.23 vs JSON): H2 supported. Unstructured text introduces noise; LLM priors dominate over specification content.
3. **Format ranking consistent across models** (Kendall's W = .84): H4 supported. All five architectures agree: F5 > F3 > F4 >= F1 > F2.
4. **ANOVA highly significant**: F(4,350) = 51.19, p < .001, eta-sq = .369.
5. **No hard/soft dimension asymmetry**: H5 not supported. Format choice affects all dimensions roughly equally.

### Practical Implication

For brand function deployment, include numerical scores prominently. Prose descriptions add noise rather than signal when the goal is AI comprehension fidelity. The optimal brand function format is structured with explicit scores -- JSON with numbers is better than JSON with only prose.

## Languages

English (en) is the sole language of prompts, responses, and brand-function content.

## Dataset Structure

### Data Fields

Each JSONL record in `data/exp_bf_format_v2.jsonl` contains 23+ fields. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `experiment` | string | Experiment identifier (Exp D) |
| `model_id` | string | Concrete model identifier used in the call |
| `model_provider` | string | Provider family (Anthropic, OpenAI, Google, DeepSeek, xAI) |
| `brand` | string | Canonical SBT brand: Hermes / IKEA / Patagonia / Tesla / Erewhon |
| `condition` | string | Format condition F1-F5 (JSON / prose / tabular / ranked / score-only) |
| `repetition` | int | Repetition index 1-3 |
| `user_prompt` | string | Verbatim prompt sent to the model |
| `raw_response` | string | Verbatim model response |
| `parsed_weights` | list[float] | Eight-dimensional allocation extracted from response |
| `canonical_cosine` | float | Cosine similarity vs canonical ground-truth brand profile |
| `dci` | float | Dimensional Collapse Index |
| `dimension_order` | list[string] | Latin-square balanced dimension presentation order |

Additional fields cover token counts, response time, and per-call cost.

### Data Splits

| Split | Size | Contents |
|-------|------|----------|
| train | 375 | Complete 5 formats x 5 brands x 5 models x 3 reps experimental design |

### Source Data

**Curation Rationale**: to identify which representational format of a brand function specification maximizes AI comprehension fidelity, supporting AI-native brand identity deployment.

**Source**: generated via direct LLM API calls following the protocol in `protocol/experiment_config.yaml`. Brand profiles and cohort profiles used as ground truth live under `prompts/`.

**Collection Process**: each cell of the 5 x 5 x 5 x 3 design issued one prompt per repetition; responses were captured verbatim with full metadata (model_id, provider, token counts, latency, cost). Dimension order Latin-square balanced.

**Annotation**: not applicable. `canonical_cosine` and `dci` are computed from `parsed_weights` against the canonical SBT brand profiles documented in the companion paper.

## Citation

If you build on this dataset, please cite:

> Dmitry Zharnikov (2026). "AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification." Working Paper. DOI [10.5281/zenodo.19391476](https://doi.org/10.5281/zenodo.19391476).

HF dataset DOI: [10.57967/hf/8440](https://doi.org/10.57967/hf/8440).

Companion GitHub mirror: https://github.com/spectralbranding/sbt-papers/tree/main/r16-ai-native-brand-identity

## Licence

Data licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) -- you may share and adapt with attribution to the author and citation of the concept DOI above. The `license: cc-by-4.0` declaration in this README frontmatter is the canonical licence statement for this Hub-side artifact.

Companion code lives in the GitHub mirror under MIT licence; see https://github.com/spectralbranding/sbt-papers/blob/main/LICENSE.

## Discipline + Reproducibility

This dataset was generated by LLM experiments. The following disciplines apply:

- **Cross-model coverage**: five distinct model families (Anthropic Claude Haiku 4.5, OpenAI GPT-4o-mini, Google Gemini 2.5 Flash, DeepSeek V3, xAI Grok 4.1 Fast) were called under identical prompts and protocols to test format-ranking invariance.
- **Prompt-purity protocol**: prompts (`prompts/brand_profiles.json`, `prompts/cohort_profiles.json`) and experimental configuration (`protocol/experiment_config.yaml`) ship with the dataset, enabling exact replay. Renderer prompts are stored separately from any downstream extractor prompts; extractors never see canonical ground-truth profiles when scoring.
- **LLM-call provenance**: every record in `data/exp_bf_format_v2.jsonl` carries `model_id`, `model_provider`, `user_prompt`, `raw_response`, token counts, latency, and cost, enabling per-call audit.
- **Reproduction pipeline**: the companion GitHub mirror at https://github.com/spectralbranding/sbt-papers/tree/main/r16-ai-native-brand-identity contains the analysis scripts that regenerate all reported statistics (ANOVA, Cohen's d, Kendall's W, cosine, DCI) from the JSONL records here.

---

