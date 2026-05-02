# R19: Empirical Rate-Distortion Curve for AI Brand Perception Encoders

**Citation key**: 2026aa | **DOI**: [10.5281/zenodo.19528833](https://doi.org/10.5281/zenodo.19528833) | **Dataset DOI**: [10.57967/hf/8362](https://doi.org/10.57967/hf/8362) | **Status**: Working paper v1.0.1 (1,652 API calls, 17 LLM architectures from distinct training lineages, 98.1% parse rate)

## Paper

Zharnikov, D. (2026aa). Empirical Rate-Distortion Curve for AI Brand Perception Encoders. Working Paper. https://doi.org/10.5281/zenodo.19528833

## Abstract

This study applies Shannon rate-distortion theory to measure how response-format constraints affect the fidelity of AI-generated brand perception profiles. Seventeen large language model architectures from distinct training lineages (1,652 API calls, 1,621 valid; 98.1% parse rate) are prompted to evaluate five canonical reference brands under five response formats spanning 3 to 26 bits of information rate. Distortion is measured as total variation distance between each model's normalized output and a canonical eight-dimensional brand profile. The resulting rate-distortion curve is J-shaped: minimum distortion occurs not at the highest-rate format (100-point allocation, 26 bits) but at an intermediate bounded format (1-5 ordinal scale, 19 bits). All 17 models exhibit this pattern (paired t(16) = 11.92, p < .001, Cohen's d_z = 2.89 for R1 vs R2). Cross-architectural codebook convergence is confirmed: mean cross-model CV = .140 across all rate conditions (H2 SUPPORTED). The finding implies that bounded ordinal formats suppress within-model variance and produce closer alignment to canonical brand profiles than unconstrained high-rate allocation — a practical implication for AI brand measurement instrument design.

## Hypotheses

| ID | Statement | Status |
|----|-----------|--------|
| H1 | D decreases monotonically as R increases (Spearman, Bonferroni-corrected) | **NOT SUPPORTED** (test-power artifact: n=5 rate conditions insufficient for corrected significance) |
| J-shape | R(D) curve has a non-monotonic J-shape with trough at R2 | **SUPPORTED** (17/17 models; t(16) = 8.53–11.92, all p < .001; Fisher p < .001) |
| H2 | All 17 models lie on a common curve (mean CV < .15) | **SUPPORTED** (mean CV = .140) |
| H3 | Shannon lower bound comparison | **DEFERRED** (analytical exercise required) |
| H4 | Western vs cross-cultural R(D) slope difference | **NOT SUPPORTED** (n=6 vs n=11; p = .250, d = -.466; severely underpowered) |
| H5 | At R1, cross-model CV < .20 | **NOT SUPPORTED** full panel (CV = .210); core 7-model subset: CV = .196 |

## Key Results

### R(D) Curve — Cross-Model Summary

Mean distortion (L1/2 total variation distance) at each rate condition, averaged over 17 models, 5 brands, and 5 repetitions.

| Rate | Bits | Mean d | SD | CV |
|------|------|--------|----|----|
| R1 | 26 | .172 | .036 | .210 |
| R2 | 19 | **.087** | .011 | .132 |
| R3 | 13 | .111 | .016 | .143 |
| R4 | 8 | .181 | .036 | .198 |
| R5 | 3 | .857 | .015 | .018 |

*Notes*: Bold = global minimum. R2 is the minimum for all 17 models. CV computed across 17 per-model means.

### J-Shape Test Summary (df = 16, 17 models)

| Comparison | t(16) | p | Cohen's d_z |
|-----------|-------|---|------------|
| R1 vs R2 | 11.92 | < .001 | 2.89 |
| R3 vs R2 | 8.53 | < .001 | 2.07 |
| R4 vs R2 | 9.35 | < .001 | 2.27 |
| Fisher combined chi-sq(6) = 69.06 | — | < .001 | — |

### Per-Brand R(D) Summary

| Brand | D(R1) | D(R2) | D(R3) | D(R4) | D(R5) | Min at |
|-------|-------|-------|-------|-------|-------|--------|
| Hermes | .133 | **.055** | .062 | .078 | .862 | R2 |
| IKEA | .148 | **.056** | .090 | .178 | .849 | R2 |
| Patagonia | .138 | **.053** | .077 | .124 | .838 | R2 |
| Erewhon | .169 | **.101** | .138 | .179 | .846 | R2 |
| Tesla | .178 | .137 | **.133** | .305 | .860 | R3 |

## Repository Structure

This directory follows the [Research-as-Repository protocol](https://github.com/spectralbranding/paper-repo) (Zharnikov, 2026u).

### Root files

| File | Purpose |
|------|---------|
| `paper.md` | Full paper v1.0 (3,074 words, 11 refs) |
| `paper.yaml` | Machine-readable claims, hypotheses, falsification criteria |
| `CITATION.cff` | Citation metadata (version 1.0.0; DOI 10.5281/zenodo.19528833) |
| `CONTRIBUTORS.yaml` | Human and AI contributor roles |
| `PROVENANCE.yaml` | Version history and submission records |
| `DATA_MANIFEST.yaml` | Experiment data location and description |
| `LICENSE` | CC-BY-4.0 (paper content) |

### Companion code (`code/`)

| File | Purpose |
|------|---------|
| `code/plot_rate_distortion_curve.py` | Generates `figures/figure1_j_curve.png` (Figure 1 in paper) from Table 2 data. Run: `uv run python code/plot_rate_distortion_curve.py`. Output written to `figures/`. Seed: 42. |

### Experiment cascade (`experiment/`)

| Path | Purpose |
|------|---------|
| `L0_specification/` | Pre-registration protocol (PROTOCOL.md, timestamped before first API call) |
| `L1_configuration/` | models.yaml, brands.yaml, rate_conditions.yaml |
| `L2_prompts/` | r19_prompts.py — 5 prompt templates (R1-R5) |
| `L3_sessions/` | r19_rate_sweep.jsonl — 1,652 raw JSONL session records (1,621 valid) |
| `L4_analysis/` | Results, summary, supplementary analyses (H4, J-shape, per-brand) |
| `validation/` | Schema validation, checksums, completeness checks |
| `run19_rate_sweep.py` | Main experiment script (reuses R15 API callers) |

### L4 analysis outputs

| File | Purpose |
|------|---------|
| `r19_results.json` | Aggregated results: per-cell distortions, R(D) curves, H1-H5 verdicts |
| `r19_per_cell.csv` | Long-format per-cell data (425 rows: 17 models x 5 rates x 5 brands) |
| `r19_rd_curves.csv` | Per-model R(D) curve data + power-law fit (85 rows: 17 models x 5 rates) |
| `r19_per_brand_rd.csv` | Per-brand R(D) curves (25 rows: 5 brands x 5 rates) |
| `r19_summary.md` | Human-readable results summary with hypothesis verdicts |
| `r19_pre_registration_audit.md` | Pre-registration compliance audit (no deviations) |
| `r19_jshape_supplementary.md` | J-shape formal test (3 paired t-tests + Fisher) |
| `r19_h4_supplementary.md` | H4 architectural separation test (Welch, n=6 Western vs n=11 cross-cultural) |
| `r19_per_brand_supplementary.md` | Per-brand R(D) narrative analysis |

## Reproducing the Experiment

```bash
cd experiment

# Offline dry run (simulated model, no API keys needed)
python run19_rate_sweep.py --demo

# Smoke test (1 brand x 17 models x 5 conditions x 1 rep)
python run19_rate_sweep.py --smoke

# Full run (1,652 calls)
python run19_rate_sweep.py --live

# Re-aggregate from existing JSONL (no new API calls)
python run19_rate_sweep.py --analyze-only
```

Required environment variables:

```bash
export ANTHROPIC_API_KEY=...
export OPENAI_API_KEY=...
export GOOGLE_API_KEY=...
export DEEPSEEK_API_KEY=...
export GROQ_API_KEY=...
export CEREBRAS_API_KEY=...
export GROK_API_KEY=...
```

**Note**: Uses the R15 virtualenv. From `experiment/`:

```bash
/Users/d/projects/sbt-papers/r15-ai-search-metamerism/experiment/.venv/bin/python run19_rate_sweep.py --demo
```

## Validation

```bash
cd experiment

# Run all checks
python validation/validate.py --all

# Or individually
python validation/validate.py --check-completeness
python validation/validate.py --check-schemas
python validation/validate.py --check-integrity

# Regenerate checksums after intentional data changes
python validation/validate.py --regenerate-checksums
```

## Relationship to R15 and R16

R19, R15, and R16 form a triad examining AI brand perception from different angles:

- **R15** asks: when LLMs make brand recommendations, which SBT dimensions do they over-weight?
  (Answer: Economic + Semiotic, DCI = .355, confirmed across 24 models.)

- **R16** asks: can LLMs tell brands apart when given more behavioral specification?
  (Answer: yes — specification augmentation resolves behavioral metamerism.)

- **R19** asks: how does the information rate budget (prompt format) shape distortion?
  (Answer: J-shaped R(D) curve — bounded 1-5 ordinal scale minimizes distortion, not unconstrained 100-point allocation.)

## How to Cite

```bibtex
@article{zharnikov2026aa,
  title={R19: Empirical Rate-Distortion Curve for AI Brand Perception Encoders},
  author={Zharnikov, Dmitry},
  year={2026},
  doi={10.5281/zenodo.19528833},
  note={Working paper.}
}
```

## License

CC-BY-4.0 (paper content). MIT License (code in `experiment/`).
