---
license: cc-by-4.0
language:
- en
size_categories:
- 1K<n<10K
task_categories:
- text-generation
- text-classification
- feature-extraction
tags:
- spectral-brand-theory
- r19-rate-distortion
- brand-perception
- llm-evaluation
- rate-distortion-theory
- vector-quantization
- dimensional-collapse
- J-curve
- pre-registered
- PRISM-B
- cross-architectural
- codebook-convergence
pretty_name: "Optimal Response Formats for AI Brand Perception Measurement: Evidence for a J-Shaped Rate-Distortion Curve"
configs:
- config_name: default
  data_files:
  - split: train
    path: train.csv
- config_name: rate_sweep
  data_files:
  - split: train
    path: data/r19_rate_sweep.jsonl
- config_name: per_cell
  data_files:
  - split: train
    path: analysis/r19_per_cell.csv
- config_name: per_brand
  data_files:
  - split: train
    path: analysis/r19_per_brand_rd.csv
citation: |
  @article{zharnikov2026r19,
    author = {Dmitry Zharnikov},
    title = {Optimal Response Formats for AI Brand Perception Measurement: Evidence for a J-Shaped Rate-Distortion Curve},
    journal = {Working Paper, Zenodo},
    year = {2026},
    doi = {10.5281/zenodo.19528833},
    orcid = {0009-0000-6893-9231}
  }
paperswithcode_id: null
---

# R19: Empirical Rate-Distortion Curve for AI Brand Perception Encoders

**Paper DOI**: [10.5281/zenodo.19528833](https://doi.org/10.5281/zenodo.19528833)
**Dataset DOI**: [10.57967/hf/8362](https://doi.org/10.57967/hf/8362)
**Source Code**: [spectralbranding/sbt-papers/r19-rate-distortion](https://github.com/spectralbranding/sbt-papers/tree/main/r19-rate-distortion)
**Citation Key**: Zharnikov (2026aa)

## Dataset Summary

This dataset contains **1,652 API calls** (1,621 valid, 98.1% parse rate) from a preregistered experiment testing how response-format constraints affect AI-generated brand perception profiles. 17 LLM architectures from distinct training lineages evaluate 5 canonical brands under 5 response formats spanning 3 to 26 bits of information rate.

**Key finding**: The rate-distortion curve is **J-shaped**, not monotonically decreasing. Minimum distortion occurs at the intermediate 1--5 ordinal scale (19 bits, R2), not at the highest-rate 100-point allocation (26 bits, R1). All 17 models exhibit this pattern (paired *t*(16) = 11.92, *p* < .001, *d*_z = 2.89). This means structured formats suppress encoder bias and yield higher-fidelity brand perception measurements than unconstrained elicitation.

Companion paper: [Optimal Response Formats for AI Brand Perception Measurement: Evidence for a J-Shaped Rate-Distortion Curve](https://doi.org/10.5281/zenodo.19528833) (Zharnikov, 2026).
Companion GitHub repository: https://github.com/spectralbranding/sbt-papers/tree/main/r19-rate-distortion containing the analysis code, prompts, and reproduction pipeline.

## Languages

English (en) is the sole language of prompts and model responses across all 17 evaluated LLM architectures and all 5 brand-perception elicitation formats.

## Dataset Structure

### Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `model` | string | LLM identifier (e.g., `claude-haiku-4.5`, `gpt-4o-mini`) |
| `brand` | string | One of 5 canonical SBT reference brands (Hermes, IKEA, Patagonia, Tesla, Erewhon) |
| `rate_condition` | string | One of R1-R5 (response format constraint) |
| `repetition` | int64 | 1-5; replicate index per cell |
| `scores` | object | 8-dimensional brand perception profile in canonical SBT order |
| `distortion` | float64 | Per-call distortion vs reference profile |
| `parse_status` | string | `valid` or specific failure mode |
| `tokens_in` / `tokens_out` | int64 | Token accounting per call |
| `latency_ms` | int64 | Wall-clock latency per call |

### Data Splits

| Split | Size | Contents |
|-------|------|----------|
| train.csv | 85 | Per-model mean distortion by rate condition (HF viewer default) |
| rate_sweep | 1,652 | Full experiment: every call with raw scores and distortion |
| per_cell | 425 | Per-cell (model x brand x rate) summary statistics |
| per_brand | 25 | Per-brand R(D) curves |

### Source Data

**Curation Rationale**: Existing brand-perception elicitation from LLMs uses unconstrained free-form prompts, conflating encoder capacity with response-format coupling. This dataset enables direct measurement of how format-imposed information rate trades off against distortion, isolating the empirical R(D) curve for AI brand encoders.

**Source**: Synthetic LLM-generated brand perception scores. 17 commercial and open-source LLM APIs were queried under a preregistered protocol (see `L0_specification/PROTOCOL.md`).

**Collection Process**: Each cell (model x brand x rate_condition) was sampled 5 times. Prompts followed PRISM-B canonical templates. Parses validated by structural schema check; failures recorded with `parse_status`. Total cost ~$2; collection window single calendar day.

**Annotation**: Not applicable — outputs are model-generated, not human-annotated. The 8 SBT dimensions (Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal) are imposed as the canonical perception basis.

## Experiment Design

| Parameter | Value |
|-----------|-------|
| Brands | 5 canonical SBT reference brands (Hermes, IKEA, Patagonia, Tesla, Erewhon) |
| Models | 17 from distinct training lineages |
| Rate conditions | 5 (R1: 100-point allocation, R2: 1--5 ordinal, R3: high/med/low, R4: rank order, R5: single best) |
| Repetitions | 5 per cell |
| Total calls | 1,652 (1,621 valid) |
| Parse success | 98.1% |
| Cost | ~$2 |
| Pre-registered | Yes (L0_specification/PROTOCOL.md) |

## Rate Conditions

| Condition | Format | Information Rate | Mean Distortion |
|-----------|--------|:----------------:|:---------------:|
| R1 | 100-point allocation across 8 dims | ~26 bits | .153 |
| R2 | 1--5 ordinal scale per dim | ~19 bits | .077 |
| R3 | High / Medium / Low per dim | ~13 bits | .112 |
| R4 | Rank order of 8 dims | ~16 bits | .131 |
| R5 | Single strongest dimension | ~3 bits | .162 |

## Models Tested

| Model | Training Lineage | Provider |
|-------|-----------------|----------|
| Claude Haiku 4.5 | Anthropic Western | Anthropic |
| GPT-4o-mini | OpenAI Western | OpenAI |
| Gemini 2.5 Flash | Google Western | Google |
| Grok-3-mini | xAI Western | xAI |
| Llama 3.3 70B | Meta Western | Groq |
| Gemma 4 27B | Google Western | Local (Ollama) |
| DeepSeek V3 | DeepSeek Chinese | DeepSeek |
| Qwen3 235B | Alibaba Chinese | Cerebras |
| Qwen Plus | Alibaba Chinese | DashScope |
| DeepSeek V3 (SambaNova) | DeepSeek Chinese | SambaNova |
| GLM-4p7 | Zhipu Chinese | Fireworks |
| Kimi K2 | Moonshot Chinese | Groq |
| Sarvam M | Sarvam Indian | Sarvam AI |
| GigaChat-2-Max | Sber Russian | Sber |
| YandexGPT Pro | Yandex Russian | Yandex AI |
| GPT-OSS-Swallow 20B | Tokyo Tech Japanese | Yandex AI |
| ALLaM 2 7B | SDAIA Arabic | Groq |

## Hypothesis Results

| ID | Hypothesis | Status |
|----|-----------|--------|
| H1 | R(D) curve is non-monotonic (J-shaped) | **Supported** (*t*(16) = 11.92, *d*_z = 2.89) |
| H2 | Cross-architectural codebook convergence (CV < .15) | **Supported** (mean CV = .140) |
| H3 | R2 minimum generalizes across brand categories | **Supported** (4/5 brands, Erewhon exception) |
| H4 | Unconstrained formats (R1) produce higher distortion than R2 | **Supported** (R1 > R2 for 16/17 models) |
| H5 | Convergence tightens at R1 (CV < .20) | **Not supported** (CV = .210, marginal) |

## Dataset Files

| File | Description | Rows |
|------|-------------|-----:|
| `train.csv` | Per-model mean distortion by rate condition (HF viewer default) | 85 |
| `data/r19_rate_sweep.jsonl` | Full experiment: every call with raw scores and distortion | 1,652 |
| `analysis/r19_per_cell.csv` | Per-cell (model x brand x rate) summary statistics | 425 |
| `analysis/r19_per_brand_rd.csv` | Per-brand R(D) curves | 25 |
| `analysis/r19_results.json` | Complete results with hypothesis tests and meta | 1 |
| `analysis/r19_summary.md` | Human-readable results summary | -- |
| `analysis/r19_jshape_supplementary.md` | J-shape statistical tests (17-model panel) | -- |
| `L0_specification/PROTOCOL.md` | Pre-registration protocol | -- |
| `L1_configuration/` | Brand, model, and rate condition YAML configs | -- |
| `paper.md` | Full paper text | -- |
| `paper.yaml` | Machine-readable paper specification | -- |

## Citation

If you build on this dataset, please cite:

> Dmitry Zharnikov (2026). "Optimal Response Formats for AI Brand Perception Measurement: Evidence for a J-Shaped Rate-Distortion Curve." Working Paper. DOI [10.5281/zenodo.19528833](https://doi.org/10.5281/zenodo.19528833). ORCID 0009-0000-6893-9231.

HF dataset DOI: [10.57967/hf/8362](https://doi.org/10.57967/hf/8362).

Companion GitHub mirror: https://github.com/spectralbranding/sbt-papers/tree/main/r19-rate-distortion

```bibtex
@article{zharnikov2026r19,
  title  = {Optimal Response Formats for {AI} Brand Perception Measurement: Evidence for a {J-Shaped} Rate-Distortion Curve},
  author = {Zharnikov, Dmitry},
  year   = {2026},
  doi    = {10.5281/zenodo.19528833},
  note   = {Working Paper; ORCID 0009-0000-6893-9231}
}
```

## Related Datasets

- [spectralbranding/r15-ai-search-metamerism](https://huggingface.co/datasets/spectralbranding/r15-ai-search-metamerism) -- 21,350 calls, 24 LLMs, dimensional collapse baseline
- [spectralbranding/r20-portfolio-ai-perception](https://huggingface.co/datasets/spectralbranding/r20-portfolio-ai-perception) -- 7,975 obs, 13 models, portfolio interference

## Licence

Data licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — you may share and adapt with attribution to the author and citation of the concept DOI above. The `license: cc-by-4.0` declaration in this README frontmatter is the canonical licence statement for this Hub-side artifact.

Companion code lives in the GitHub mirror under MIT licence; see https://github.com/spectralbranding/sbt-papers/blob/main/LICENSE.

## Discipline + Reproducibility

This dataset is the output of a preregistered LLM experiment. The following disciplines apply:

- **Pre-registration**: full protocol at `L0_specification/PROTOCOL.md` (frozen before data collection); hypotheses H1-H5 declared with quantitative thresholds prior to running `run19_rate_sweep.py`.
- **Cross-extractor discipline**: each LLM under test is the renderer; structural parse + distortion computation is performed by a separate non-LLM pipeline (`run19_rate_sweep.py`), so renderer != extractor at the artifact level.
- **LLM-call logging**: every API call recorded in `data/r19_rate_sweep.jsonl` with model, prompt, raw response, parse status, distortion, tokens, latency.
- **Prompt-purity protocol**: all five rate-condition prompts frozen in `r19_prompts.py` at the companion GitHub mirror; no per-brand prompt customisation; identical scaffolds across 17 models.
- **Reproduction recipe**: clone the companion GitHub mirror, install dependencies, set the provider API keys, run `python run19_rate_sweep.py` to regenerate `data/r19_rate_sweep.jsonl`; downstream analysis tables (`analysis/*.csv`, `analysis/r19_results.json`) regenerate deterministically from the sweep file.
- **Validation**: see `validation/` for hypothesis-test reproduction scripts and `analysis/r19_jshape_supplementary.md` for the 17-model J-shape panel.

---

