# R15: Spectral Metamerism in AI-Mediated Brand Perception

**Citation key**: 2026v | **DOI**: [10.5281/zenodo.19422427](https://doi.org/10.5281/zenodo.19422427) | **Status**: Empirical results complete (4,860 calls)

## Paper

Zharnikov, D. (2026). Spectral Metamerism in AI-Mediated Brand Perception: How Large Language Models Collapse Multi-Dimensional Brand Differentiation in Consumer Search. Working Paper.

## Abstract

AI-mediated search is replacing traditional consumer search, yet no formal model predicts which brand attributes survive AI mediation. This paper applies Spectral Brand Theory's eight-dimensional framework to model large language models as observer cohorts with systematically biased spectral profiles. An experimental study across 6 LLMs --- organized into Western cloud, Chinese cloud, and local open-weight clusters --- tests 10 global and 5 local brand pairs using structured weight allocation. Results: Cultural meaning collapses to 58% of baseline, Temporal heritage to 65%, while Experiential inflates to 150%. Cross-model cosine similarity of 0.975 confirms the collapse is structural, not model-specific. Local brands from underrepresented markets (Cyprus, Latvia, Kenya, Vietnam, Serbia) show significantly amplified collapse (p < 0.0001, Cohen's d = 0.878), with Economic inflating to 168%. A Brand Function resolution test demonstrates that providing behavioral specifications reduces collapse by 20%.

## Key Results

| Run | Pairs | Calls | H1 (collapse) | H2 (convergence) |
|-----|-------|-------|---------------|-------------------|
| Run 2 (global) | 10 | 3,240 | p = 0.017, DCI = 29.1 | cosine = 0.975 |
| Run 3 (local) | 5 | 1,620 | p = 0.0006, DCI = 35.3 | cosine = 0.975 |
| Run 4 (resolution) | 5 | 90 | DCI drops 0.355 -> 0.284 | -- |

## Repository Structure

This directory follows the [Research-as-Repository protocol](https://github.com/spectralbranding/paper-repo) (Zharnikov, 2026u).

| File | Purpose |
|------|---------|
| `paper.md` | Full paper (v1.0, ~9,000 words, 4 hypotheses, 28 refs) |
| `paper.pdf` | PDF export |
| `paper.yaml` | Machine-readable claims, hypotheses, falsification criteria |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTORS.yaml` | Human and AI contributor roles |
| `PROVENANCE.yaml` | Version history and submission records |
| `DATA_MANIFEST.yaml` | Experiment data location and description |
| `LICENSE` | CC-BY-NC-ND-4.0 (paper content) |
| `experiment/` | Full experiment infrastructure (see experiment/README.md) |
| `results_v2_global.json` | Run 2 results (10 global pairs, 3,240 calls) |
| `results_v3_local.json` | Run 3 results (5 local pairs, 1,620 calls) |
| `results_v4_resolution.json` | Run 4 results (Brand Function resolution, 90 calls) |

## Reproducing the Experiment

```bash
cd experiment
uv pip install -r requirements.txt

# Demo mode (no API keys needed)
python ai_search_metamerism.py --demo

# Smoke test (1 pair, all models)
python ai_search_metamerism.py --smoke

# Full run (10 global pairs, 3 runs)
python ai_search_metamerism.py --live --runs 3 --log L3_sessions/session_log.jsonl

# Local brands only
python ai_search_metamerism.py --live --runs 3 --local-only

# Brand Function resolution test
python run_resolution_test.py --live --runs 3
```

## Run It On Your Own Brands

See [experiment README](experiment/README.md#run-it-on-your-own-brands) for a step-by-step guide. Cost: ~$0.80 for a full run.

## How to Cite

```bibtex
@article{zharnikov2026v,
  title={Spectral Metamerism in AI-Mediated Brand Perception},
  author={Zharnikov, Dmitry},
  year={2026}
}
```

## License

CC-BY-NC-ND-4.0
