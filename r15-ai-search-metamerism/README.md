# R15: Spectral Metamerism in AI-Mediated Brand Perception

**Citation key**: 2026v | **Target**: Journal of Advertising Research | **Status**: Experiment pending

## Paper

Zharnikov, D. (2026). Spectral Metamerism in AI-Mediated Brand Perception: How Large Language Models Collapse Multi-Dimensional Brand Differentiation in Consumer Search. Working Paper.

## Abstract

AI-mediated search is replacing traditional consumer search, yet no formal model predicts which brand attributes survive AI mediation. This paper applies Spectral Brand Theory's eight-dimensional framework to model large language models as observer cohorts with systematically biased spectral profiles. An experimental study prompts seven LLMs --- organized into Western cloud, Chinese cloud, and local open-weight clusters --- with brand comparison queries across ten brand pairs. Two parallel cloud-local comparisons (Qwen Plus vs. Qwen3 30B; Gemini Flash vs. Gemma 4) test whether commercial API alignment layers contribute to dimensional collapse.

## Repository Structure

This directory follows the [Research-as-Repository protocol](https://github.com/spectralbranding/paper-repo) (Zharnikov, 2026u).

| File | Purpose |
|------|---------|
| `paper.yaml` | Machine-readable claims, hypotheses, falsification criteria |
| `CONTRIBUTORS.yaml` | Human and AI contributor roles |
| `PROVENANCE.yaml` | Submission history and fork records |
| `DATA_MANIFEST.yaml` | Experiment data location and description |
| `LICENSE` | CC-BY-NC-ND-4.0 (paper content) |
| `experiment/` | OST-structured experiment data (L0-L4) |

## Reproducing the Experiment

```bash
# Demo mode (no API keys needed)
uv run python experiment/L4_analysis/analyze.py --demo

# Verify results from committed data
uv run python experiment/L4_analysis/analyze.py --verify

# Full reproduction (requires API keys)
uv run python experiment/run_experiment.py --live
```

## LLM Audit

Point your LLM at this repository and use the audit prompt in `experiment/README.md` to validate the full chain from hypotheses to conclusions.
