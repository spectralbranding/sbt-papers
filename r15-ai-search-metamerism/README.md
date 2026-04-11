# R15: Spectral Metamerism in AI-Mediated Brand Perception

**Citation key**: 2026v | **DOI**: [10.5281/zenodo.19422427](https://doi.org/10.5281/zenodo.19422427) | **Status**: Empirical results complete (21,601 calls across 9 runs, 24 models, 9 cultural traditions; plus supplementary Run 10 corrective comparators, 126 calls)

## Paper

Zharnikov, D. (2026). Spectral Metamerism in AI-Mediated Brand Perception: How Large Language Models Collapse Multi-Dimensional Brand Differentiation in Consumer Search. Working Paper.

## Abstract

AI-mediated search is replacing traditional consumer search, yet no formal model predicts which brand attributes survive AI mediation. This paper applies Spectral Brand Theory's eight-dimensional framework to model large language models as observer cohorts with systematically biased spectral profiles. An experimental study across 24 LLMs from 7 training traditions — covering 9 cultural traditions in brand pairs (Western, Chinese, Russian, Japanese, Korean, Arabic, Indian, Ukrainian, Mongolian) — tests brand pairs using structured weight allocation across 9 runs (21,600+ API calls, 815 native-language calls in 11 languages). Results: Cultural meaning collapses to 58% of baseline, Temporal heritage to 65%, while Experiential inflates to 150%. Cross-model cosine similarity of 0.977 confirms the collapse is structural, not model-specific. Local brands from underrepresented markets show significantly amplified collapse (Cohen's d = 0.878 vs global brands). H1 supported (p < 0.0001, DCI = 35.6 vs 25.0 baseline, cross-cultural d = 3.449), H2 supported (cosine = 0.977), H6 supported (Western DCI 0.339 < non-Western 0.360, p = 0.0013), H12 supported (p < 0.0001, delta = 0.040). H10 (native language reduces collapse) NOT SUPPORTED (46/115 pairs, mean = -0.005). H5 NOT SUPPORTED — reversed (national models collapse MORE on own-culture brands).

## Hypotheses (12 tested + 1 future direction)

| ID | Statement | Run | Result |
|----|-----------|-----|--------|
| H1 | DCI significantly above 0.250 baseline (Economic + Semiotic over-weighting) | 2-9 | **SUPPORTED** (p < 0.0001) |
| H2 | Cross-model dimensional weight profiles converge (cosine >= 0.85) | 2-9 | **SUPPORTED** (cosine = 0.977) |
| H3 | Lower probe variance for hard dimensions (Economic, Semiotic) than soft | 2 | exploratory |
| H4 | Differentiation gap on soft-dim brand pairs | 2 | exploratory |
| H5 | National models collapse less on own-culture brands | 5 | **NOT SUPPORTED** (reversed) |
| H6 | Bidirectional cultural advantage (Western lower DCI than non-Western) | 5 | **SUPPORTED** (Western 0.339 vs non-Western 0.360, t = -3.243, p = 0.0013) |
| H7 | Geopolitical valence (Tinkoff vs PrivatBank) | 6, 7 | exploratory |
| H8 | Thin-data floor (Mongolia highest DCI) | 5 | partial |
| H9 | Capacity-dependent collapse (smaller models collapse more) | 5 | partial |
| H10 | Native-language prompting reduces collapse | 5, 8 | **NOT SUPPORTED** (mean = -0.005) |
| H11 | Same-category cross-border (Tinkoff vs PrivatBank banking pair) | 6 | tested (geopolitical signal, Run 6) |
| H12 | Geopolitical framing — same brand in different cities | 7 | **SUPPORTED** (p < 0.0001, delta = 0.040) |
| H13 | Temporal training stability (successive model versions) | -- | future work (proposed, not tested) |

## Key Results

| Run | Pairs | Calls | H1 (collapse) | H2 (convergence) |
|-----|-------|-------|---------------|-------------------|
| Run 2 (global) | 10 | 3,240 | p = 0.017, DCI = 29.1 | cosine = 0.975 |
| Run 3 (local) | 5 | 1,620 | p = 0.0006, DCI = 35.3 | cosine = 0.975 |
| Run 4 (resolution) | 5 | 90 | DCI drops 0.355 → 0.284 | -- |
| Run 5 (cross-cultural) | 7 | 11,410 (7,999 successful) | p < 0.0001, DCI = 35.6 | cosine = 0.977 |
| Run 6 (banking) | 1 | 1,018 | H6 p = 0.0013, d = 3.449 | cosine = 0.977 |
| Run 7 (framing) | varies | varies | H12 p < 0.0001 | -- |
| Run 8 (native expansion) | varies | 815 | H10 NOT SUPPORTED (mean = -0.005) | -- |
| Run 9 (temperature) | varies | varies | DCI spread = 0.012 (robust) | -- |
| Run 10 (corrective comparators, supplementary) | 3 focal × 2 conditions | 126 | VkusVill shows largest comparator effect (ΔDCI = +7.4) | -- |

## Repository Structure

This directory follows the [Research-as-Repository protocol](https://github.com/spectralbranding/paper-repo) (Zharnikov, 2026u).

### Root files

| File | Purpose |
|------|---------|
| `paper.md` | Full paper (v2.0, 12 hypotheses, includes Run 5 cross-cultural results) |
| `paper.yaml` | Machine-readable claims, hypotheses, falsification criteria |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTORS.yaml` | Human and AI contributor roles |
| `PROVENANCE.yaml` | Version history and submission records |
| `DATA_MANIFEST.yaml` | Experiment data location and description |
| `LICENSE` | CC-BY-NC-ND-4.0 (paper content) |
| `results_v2_global.json` | Run 2 aggregated results (per-model weights, DCI, cosine, H1 t-test) |
| `results_v3_local.json` | Run 3 aggregated results (local brand pairs) |
| `results_v4_resolution.json` | Run 4 aggregated results (Brand Function resolution test) |
| `experiment/` | Full experiment infrastructure (see `experiment/README.md`) |

### Experiment cascade (`experiment/`)

| Path | Purpose |
|------|---------|
| `L0_specification/` | Pre-registered protocols for Runs 2-4 and Run 5 |
| `L1_configuration/` | `models.yaml` — 24 model configurations |
| `L2_prompts/` | Prompt templates (`templates/`) and rendered examples (`rendered/`) |
| `L3_sessions/` | Raw JSONL session logs — 16 files, 21,727+ records (Runs 2-9 main study + Run 10 supplementary) |
| `L4_analysis/` | Analysis scripts and outputs (per-run results, robustness tests) |
| `validation/` | Schema validation, checksums, completeness checks |
| `ai_search_metamerism.py` | Main experiment script (179K, 24 models, 4 prompt types) |
| `local_brand_specs.json` | Brand Function specifications for 5 local brands (Run 4) |
| `requirements.txt` | Python dependencies |

### L4 analysis outputs

| File | Purpose |
|------|---------|
| `run5_results.json` | Run 5 detailed (10.8 MB): DCI per model per culture, H5-H10 tests |
| `run5_summary.md` | Run 5 human-readable summary tables |
| `run5_analysis_results.json` | Post-processed Run 5 statistics |
| `run5_dci_table.csv` | DCI matrix (models × cultures) |
| `run5_diagonal_advantage.csv` | H5 primary measure |
| `run6_banking_results.json` | Run 6 banking pair aggregated results |
| `run7_framing_results.json` | Run 7 framing experiment results (H12) |
| `run7_framing_summary.md` | Run 7 human-readable summary |
| `run8_native_expansion_results.json` | Run 8 per-language DCI + H10 verdict |
| `run9_temperature_results.json` | Run 9 temperature sensitivity |
| `power_analysis_results.json` | Post-hoc power for H1, H2, H5, H6 |
| `prompt_sensitivity_results.json` | ICC(3,1) across 3 repetitions per condition |
| `exclude_patagonia_results.json` | Robustness: replication with Patagonia excluded |
| `run10_corrective_results.json` | Run 10 supplementary: per-model profiles for 6 corrective-comparator pairs |
| `run10_corrective_summary.md` | Run 10 supplementary: per-dimension delta table (corrective − control) |

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

## Validation

Three checks are implemented in `experiment/validation/validate.py`:

```bash
cd experiment

# Run all checks
python validation/validate.py --all

# Or individually
python validation/validate.py --check-completeness   # 15 L3 + 13 L4 + 3 root files
python validation/validate.py --check-schemas        # JSON schema compliance
python validation/validate.py --check-integrity      # SHA-256 hash verification

# Regenerate checksums after intentional data changes
python validation/validate.py --regenerate-checksums
```

See `experiment/validation/README.md` for the schema and checksum architecture.

## Re-running Analysis Outputs

```bash
cd experiment

# Aggregate Run 2-4 into root results files
python L4_analysis/aggregate_runs_2_to_4.py

# Aggregate Run 6, 8, 9 into L4 results files
python L4_analysis/aggregate_runs_6_to_9.py

# Re-extract one rendered prompt example per prompt_type
python L4_analysis/extract_rendered_prompts.py

# Robustness tests (each writes a *_results.json next to itself)
.venv/bin/python L4_analysis/power_analysis.py
.venv/bin/python L4_analysis/prompt_sensitivity.py
.venv/bin/python L4_analysis/exclude_patagonia.py
```

## Run It On Your Own Brands

See [experiment README](experiment/README.md#run-it-on-your-own-brands) for a step-by-step guide.

**Cost**: roughly $0.25 (5-6 models, 3 runs) to $0.80 (all 24 models, 3 runs) for a single brand pair audit at current paid-model rates. The full 9-run cross-cultural study cost $5.52 total; Run 10 supplementary (~$0.04) brings the project total to ~$5.56.

## How to Cite

```bibtex
@article{zharnikov2026v,
  title={Spectral Metamerism in AI-Mediated Brand Perception:
         How Large Language Models Collapse Multi-Dimensional Brand
         Differentiation in Consumer Search},
  author={Zharnikov, Dmitry},
  year={2026},
  doi={10.5281/zenodo.19422427}
}
```

## License

CC-BY-NC-ND-4.0 (paper content). MIT License (code in `experiment/`).
