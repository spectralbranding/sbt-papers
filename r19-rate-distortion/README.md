# R19: Empirical Rate-Distortion Curve for AI Brand Perception Encoders

**Citation key**: 2026aa | **DOI**: [10.5281/zenodo.19528833](https://doi.org/10.5281/zenodo.19528833) | **Status**: Working paper v1.0 (1,652 API calls, 17 LLM architectures from distinct training lineages, 98.1% parse rate)

## Paper

Zharnikov, D. (2026aa). Empirical Rate-Distortion Curve for AI Brand Perception Encoders. Working Paper. https://doi.org/10.5281/zenodo.19528833

## Abstract

What is the empirical rate-distortion curve for AI brand perception encoders? When AI systems respond to brand queries using different response-format constraints — from unconstrained 100-point allocation to a single most-important dimension — how does the distortion between their output and the canonical brand profile change? This paper applies information-theoretic rate-distortion framing to AI dimensional collapse, treating large language models as encoders mapping brand stimuli to compressed spectral profiles. An experiment across 7 LLMs from 7 distinct training lineages (Anthropic, OpenAI, Google, xAI, DeepSeek, Alibaba, Meta) measures distortion (total variation distance) at 5 rate conditions for 5 canonical SBT reference brands (875 API calls, 100% success rate). The R(D) curve is not monotonically decreasing as classical theory predicts. Instead, all 7 architectures trace a J-shaped curve with minimum distortion at R2 (1–5 ordinal scale, ~19 bits), not R1 (100-point free allocation, ~26 bits). Paired t-tests on 7 per-model means confirm the J-shape: t(6) = 5.81 (R1 vs R2, p < .001, d_z = 2.20), t(6) = 6.04 (R3 vs R2, p < .001, d_z = 2.28), t(6) = 7.70 (R4 vs R2, p < .001, d_z = 2.91); combined Fisher p < .0001. Cross-architectural codebook convergence is confirmed: mean cross-model CV = .107 across all rate conditions (H2 SUPPORTED). The finding implies that bounded ordinal formats suppress within-model variance and produce closer alignment to canonical brand profiles than unconstrained high-rate allocation — a practical implication for AI brand measurement instrument design.

## Hypotheses

| ID | Statement | Status |
|----|-----------|--------|
| H1 | D decreases monotonically as R increases (Spearman, Bonferroni-corrected) | **NOT SUPPORTED** (test-power artifact: n=5 rate conditions insufficient for corrected significance) |
| J-shape | R(D) curve has a non-monotonic J-shape with trough at R2 | **SUPPORTED** (7/7 models; t(6) = 5.81–7.70, all p < .001; Fisher p < .0001) |
| H2 | All 7 models lie on a common curve (mean CV < .15) | **SUPPORTED** (mean CV = .107) |
| H3 | Shannon lower bound comparison | **DEFERRED** (analytical exercise required) |
| H4 | Western vs cross-cultural R(D) slope difference | **NOT SUPPORTED** (n=4 vs n=3; p = .534, d = -.464; severely underpowered) |
| H5 | At R1, cross-model CV < .20 | **SUPPORTED** (CV = .196) |

## Key Results

### R(D) Curve by Model

Mean distortion (L1/2 total variation distance) at each rate condition, averaged over 5 brands and 5 repetitions.

| Model | R1 (26b) | R2 (19b) | R3 (13b) | R4 (8b) | R5 (3b) | fit R² |
|-------|----------|----------|----------|---------|---------|--------|
| cerebras_qwen3 | .100 | **.087** | .114 | .173 | .834 | .000 |
| claude | .159 | **.079** | .099 | .132 | .835 | .986 |
| deepseek | .148 | **.087** | .095 | .166 | .861 | .993 |
| gemini | .155 | **.080** | .088 | .221 | .843 | .985 |
| gpt | .202 | **.078** | .101 | .141 | .879 | .973 |
| grok | .145 | **.077** | .100 | .198 | .833 | .991 |
| groq_llama33 | .162 | **.074** | .102 | .179 | .870 | .989 |

*Notes*: Bold = minimum distortion per model. R2 is the global minimum for all 7 models.

### J-Shape Test Summary

| Comparison | Mean diff | t(6) | p | Cohen's d_z |
|-----------|-----------|------|---|------------|
| R1 vs R2 | .073 | 5.81 | < .001 | 2.20 |
| R3 vs R2 | .019 | 6.04 | < .001 | 2.28 |
| R4 vs R2 | .092 | 7.70 | < .001 | 2.91 |
| Fisher combined | — | — | < .0001 | — |

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
| `paper.md` | Full paper v1.0 (3,074 words, 11 refs, target: Marketing Letters) |
| `paper.yaml` | Machine-readable claims, hypotheses, falsification criteria |
| `CITATION.cff` | Citation metadata (version 1.0.0; DOI 10.5281/zenodo.19528833) |
| `CONTRIBUTORS.yaml` | Human and AI contributor roles |
| `PROVENANCE.yaml` | Version history and submission records |
| `DATA_MANIFEST.yaml` | Experiment data location and description |
| `LICENSE` | CC-BY-NC-ND-4.0 (paper content) |

### Experiment cascade (`experiment/`)

| Path | Purpose |
|------|---------|
| `L0_specification/` | Pre-registration protocol (PROTOCOL.md, timestamped before first API call) |
| `L1_configuration/` | models.yaml, brands.yaml, rate_conditions.yaml |
| `L2_prompts/` | r19_prompts.py — 5 prompt templates (R1-R5) |
| `L3_sessions/` | r19_rate_sweep.jsonl — 875 raw JSONL session records |
| `L4_analysis/` | Results, summary, supplementary analyses (H4, J-shape, per-brand) |
| `validation/` | Schema validation, checksums, completeness checks |
| `run19_rate_sweep.py` | Main experiment script (reuses R15 API callers) |

### L4 analysis outputs

| File | Purpose |
|------|---------|
| `r19_results.json` | Aggregated results: per-cell distortions, R(D) curves, H1-H5 verdicts |
| `r19_per_cell.csv` | Long-format per-cell data (175 rows: 7 models x 5 rates x 5 brands) |
| `r19_rd_curves.csv` | Per-model R(D) curve data + power-law fit (35 rows) |
| `r19_per_brand_rd.csv` | Per-brand R(D) curves (25 rows: 5 brands x 5 rates) |
| `r19_summary.md` | Human-readable results summary with hypothesis verdicts |
| `r19_pre_registration_audit.md` | Pre-registration compliance audit (no deviations) |
| `r19_jshape_supplementary.md` | J-shape formal test (3 paired t-tests + Fisher) |
| `r19_h4_supplementary.md` | H4 architectural separation test (Welch, n=4 vs n=3) |
| `r19_per_brand_supplementary.md` | Per-brand R(D) narrative analysis |

## Reproducing the Experiment

```bash
cd experiment

# Offline dry run (simulated model, no API keys needed)
python run19_rate_sweep.py --demo

# Smoke test (1 brand x 7 models x 5 conditions x 1 rep)
python run19_rate_sweep.py --smoke

# Full run (875 calls)
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

CC-BY-NC-ND-4.0 (paper content). MIT License (code in `experiment/`).
