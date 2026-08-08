---
license: cc-by-4.0
language:
  - en
size_categories:
  - n<1K
task_categories:
  - text-generation
tags:
  - spectral-brand-theory
  - r16-behavioral-metamerism-pilot
  - brand-perception
  - brand-function
  - synthetic-cohorts
  - llm-evaluation
pretty_name: R16 Behavioral Metamerism Pilot
citation: |
  @article{zharnikov2026r16,
    author = {Dmitry Zharnikov},
    title = {AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification},
    journal = {Working Paper, Zenodo},
    year = {2026},
    doi = {10.5281/zenodo.19391476}
  }
paperswithcode_id: null
configs:
  - config_name: readings
    data_files:
      - split: train
        path: "data/run16_cohort_brand_function.jsonl"
  - config_name: session_log
    data_files:
      - split: train
        path: "data/session_log.jsonl"
---

# R16 Behavioral Metamerism Pilot

Brand Function x synthetic cohort interaction experiment from the Spectral Brand Theory research program.

## Dataset Description

- **Paper**: [AI-Native Brand Identity (Zharnikov, 2026x)](https://doi.org/10.5281/zenodo.19391476)
- **Repository**: [sbt-papers/r16-ai-native-brand-identity](https://github.com/spectralbranding/sbt-papers/tree/main/r16-ai-native-brand-identity)
- **Point of Contact**: dmitry@spectralbranding.com
- **ORCID**: 0009-0000-6893-9231

## Dataset Summary

675 API calls testing whether Brand Function specification differentially affects dimensional collapse across synthetic observer cohorts. Design: 5 cohorts x 5 brands x 3 conditions (no BF, structural BF, enriched BF) x 3 models x 3 repetitions.

Companion paper: [AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification](https://doi.org/10.5281/zenodo.19391476) (Zharnikov, 2026). Companion GitHub repository: https://github.com/spectralbranding/sbt-papers/tree/main/r16-ai-native-brand-identity containing the analysis code, prompts, and reproduction pipeline.

### Key Findings

- **H1 SUPPORTED**: Brand Function reduces DCI more for aligned cohorts (interaction p < .05)
- **H2 NOT SUPPORTED**: DCI reduction range narrower than predicted
- **H3 CONFIRMED**: Run 14 null generalizes — enriched BF produces no incremental benefit over structural BF across all cohort types

### Models

Claude Haiku 4.5, GPT-4o-mini, DeepSeek V3.

## Languages

English (en) is the sole language of cohort profiles, brand profiles, Brand Function specifications, and model prompts/responses.

## Dataset Structure

### Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `cohort` | string | Synthetic observer cohort identifier (1 of 5) |
| `brand` | string | Brand profile identifier (1 of 5: Hermès / IKEA / Patagonia / Erewhon / Tesla) |
| `condition` | string | Brand Function condition: no BF / structural BF / enriched BF |
| `model` | string | LLM operator (claude-haiku-4-5 / gpt-4o-mini / deepseek-v3) |
| `repetition` | int64 | Repetition index (1-3) per (cohort, brand, condition, model) cell |
| `prompt` | string | Full prompt issued to the model |
| `response` | string | Verbatim model response |
| `dci` | float64 | Dimensional Collapse Index computed from response |

### Data Splits

| Split | Size | Contents |
|-------|------|----------|
| train | 675 | All 5 cohorts x 5 brands x 3 conditions x 3 models x 3 reps API calls |

### Data Files

- `data/run16_cohort_brand_function.jsonl` — 675 records
- `prompts/cohort_profiles.json` — 5 synthetic observer cohort profiles
- `prompts/brand_profiles.json` — 5 canonical brand profiles (Hermès / IKEA / Patagonia / Erewhon / Tesla)
- `protocol/experiment_config.yaml` — pre-registered hypotheses and design
- `analysis/run16_cohort_brand_function_results.json` — aggregated results JSON

### Source Data

**Curation Rationale**: Test whether Brand Function specification differentially reduces dimensional collapse across observer cohorts (R16 H1), and whether enriched Brand Function adds incremental benefit over structural Brand Function (R16 H3 — generalization of Run 14 null).

**Source**: User-generated via instrumented API calls to Claude Haiku 4.5, GPT-4o-mini, and DeepSeek V3 under the experimental design fixed in `protocol/experiment_config.yaml`.

**Collection Process**: 5 cohorts x 5 brands x 3 conditions x 3 models x 3 repetitions = 675 API calls; each response scored on the Dimensional Collapse Index (DCI). Hypotheses pre-registered before data collection.

**Annotation**: No human annotation. DCI computed from response text via the scoring procedure documented in the companion GitHub mirror.

## Citation

If you build on this dataset, please cite:

> Dmitry Zharnikov (2026). "AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification." Working Paper. DOI [10.5281/zenodo.19391476](https://doi.org/10.5281/zenodo.19391476).

HF dataset DOI: [10.57967/hf/8442](https://doi.org/10.57967/hf/8442).

Companion GitHub mirror: https://github.com/spectralbranding/sbt-papers/tree/main/r16-ai-native-brand-identity

BibTeX:

```bibtex
@article{zharnikov2026r16,
  author = {Zharnikov, Dmitry},
  title = {AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification},
  journal = {Working Paper, Zenodo},
  year = {2026},
  doi = {10.5281/zenodo.19391476}
}
```

## Licence

Data licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — you may share and adapt with attribution to the author and citation of the concept DOI above. The `license: cc-by-4.0` declaration in this README frontmatter is the canonical licence statement for this Hub-side artifact.

Companion code lives in the GitHub mirror under MIT licence; see https://github.com/spectralbranding/sbt-papers/blob/main/LICENSE.

## Discipline + Reproducibility

This dataset was generated by a pre-registered LLM experiment under the following disciplines:

- **Pre-registration**: hypotheses H1 / H2 / H3 fixed in `protocol/experiment_config.yaml` before data collection.
- **Multi-operator coverage**: three LLM operators (Claude Haiku 4.5, GPT-4o-mini, DeepSeek V3) probed independently to test cross-family invariance of the Brand Function effect.
- **Fixed brand profiles**: 5 canonical brand profiles (Hermès / IKEA / Patagonia / Erewhon / Tesla) held constant across cohorts and conditions per the Spectral Brand Theory canonical-profile convention.
- **Reproduction pipeline**: full analysis code, prompts, and scoring procedure published in the companion GitHub mirror at https://github.com/spectralbranding/sbt-papers/tree/main/r16-ai-native-brand-identity.

---

