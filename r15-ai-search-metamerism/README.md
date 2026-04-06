# R15: Spectral Metamerism in AI-Mediated Brand Perception

**Citation key**: 2026v | **DOI**: [10.5281/zenodo.19422427](https://doi.org/10.5281/zenodo.19422427) | **Status**: Empirical results complete (16,270 calls across 5 runs)

## Paper

Zharnikov, D. (2026). Spectral Metamerism in AI-Mediated Brand Perception: How Large Language Models Collapse Multi-Dimensional Brand Differentiation in Consumer Search. Working Paper.

## Abstract

AI-mediated search is replacing traditional consumer search, yet no formal model predicts which brand attributes survive AI mediation. This paper applies Spectral Brand Theory's eight-dimensional framework to model large language models as observer cohorts with systematically biased spectral profiles. An experimental study across 22 LLMs --- organized into Western cloud, Chinese cloud, Russian, Japanese, Korean, Arabic, and Indian clusters --- tests 22 brand pairs using structured weight allocation. Results from Runs 2-4: Cultural meaning collapses to 58% of baseline, Temporal heritage to 65%, while Experiential inflates to 150%. Cross-model cosine similarity of 0.975 confirms the collapse is structural, not model-specific. Local brands from underrepresented markets show significantly amplified collapse (p < 0.0001, Cohen's d = 0.878). Run 5 (cross-cultural, 11,410 calls, 7,999 successful): H1 supported (p < 0.0001, DCI = 35.6 vs 25.0 baseline), H2 supported (cosine = 0.976). Cultural dimension most collapsed (-4.9 points below baseline).

## Key Results

| Run | Pairs | Calls | H1 (collapse) | H2 (convergence) |
|-----|-------|-------|---------------|-------------------|
| Run 2 (global) | 10 | 3,240 | p = 0.017, DCI = 29.1 | cosine = 0.975 |
| Run 3 (local) | 5 | 1,620 | p = 0.0006, DCI = 35.3 | cosine = 0.975 |
| Run 4 (resolution) | 5 | 90 | DCI drops 0.355 -> 0.284 | -- |
| Run 5 (cross-cultural) | 7 | 11,410 (7,999 successful) | p < 0.0001, DCI = 35.6 | cosine = 0.976 |

## Repository Structure

This directory follows the [Research-as-Repository protocol](https://github.com/spectralbranding/paper-repo) (Zharnikov, 2026u).

| File | Purpose |
|------|---------|
| `paper.md` | Full paper (v2.0, 10 hypotheses, includes Run 5 cross-cultural results) |
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
| `experiment/run5_results.json` | Run 5 results (7 cross-cultural pairs, 22 models, 11,410 calls) |
| `experiment/run5_summary.md` | Run 5 summary tables (DCI, cosine, H5-H10 tests) |

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
