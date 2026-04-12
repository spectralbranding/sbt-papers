# R19 Rate-Distortion Sweep Experiment

Tests whether AI brand perception follows a rate-distortion-optimal encoding pattern
by varying the response-format constraint (rate budget) and measuring distortion between
model output and canonical brand profiles.

**Paper**: Zharnikov, D. (2026aa). R19: Empirical Rate-Distortion Curve for AI Brand Perception Encoders.
**Status**: Experiment complete. Paper in preparation.

---

## Run Status

| Condition | Models | Brands | Reps | Calls | Status | Key Result |
|-----------|--------|--------|------|-------|--------|------------|
| R1 (~26 bits): 100-point allocation | 7 | 5 | 5 | 175 | Complete | Mean distortion .153 |
| R2 (~19 bits): 1-5 scale rating | 7 | 5 | 5 | 175 | Complete | **Minimum distortion .080** |
| R3 (~13 bits): Low/Medium/High | 7 | 5 | 5 | 175 | Complete | Mean distortion .100 |
| R4 (~8 bits): Yes/No binary | 7 | 5 | 5 | 175 | Complete | Mean distortion .173 |
| R5 (~3 bits): Single dimension | 7 | 5 | 5 | 175 | Complete | Mean distortion .851 |
| **TOTAL** | **7** | **5** | **5** | **875** | **Complete** | J-shape SUPPORTED |

---

## OST Specification Cascade

| Level | Directory | Contents | Status |
|-------|-----------|----------|--------|
| L0 | `L0_specification/` | Pre-registration protocol (timestamped before API calls) | Complete |
| L1 | `L1_configuration/` | models.yaml, brands.yaml, rate_conditions.yaml | Complete |
| L2 | `L2_prompts/` | r19_prompts.py — 5 prompt templates (R1-R5) | Complete |
| L3 | `L3_sessions/` | r19_rate_sweep.jsonl — 875 raw records | Complete |
| L4 | `L4_analysis/` | Results, curves, supplementary analyses | Complete |

---

## Quick Start

Uses the R15 virtualenv (no separate install needed):

```bash
# Offline dry run
/Users/d/projects/sbt-papers/r15-ai-search-metamerism/experiment/.venv/bin/python \
  run19_rate_sweep.py --demo

# Smoke test (1 brand, all 7 models, all 5 conditions, 1 rep)
python run19_rate_sweep.py --smoke

# Full run (875 calls)
python run19_rate_sweep.py --live

# Re-aggregate from existing JSONL
python run19_rate_sweep.py --analyze-only
```

---

## Dependencies

R19 reuses R15's API callers (read-only import via sys.path):

```
R15_EXPERIMENT_DIR = Path("/Users/d/projects/sbt-papers/r15-ai-search-metamerism/experiment")
```

This is intentional: R19 is a rate-distortion extension of the R15 infrastructure.
The R15 venv contains all required packages (scipy, numpy, anthropic, openai, etc.).

---

## Output Files

| File | Contents |
|------|----------|
| `L3_sessions/r19_rate_sweep.jsonl` | 875 raw records: model, rate_condition, brand, prompt, response, distortion |
| `L4_analysis/r19_results.json` | Aggregated: per-cell distortions, R(D) curves, H1-H5 verdicts |
| `L4_analysis/r19_per_cell.csv` | Long-format per-cell (175 rows: 7 models x 5 rates x 5 brands) |
| `L4_analysis/r19_rd_curves.csv` | Per-model R(D) curve + power-law fit (35 rows) |
| `L4_analysis/r19_per_brand_rd.csv` | Per-brand R(D) (25 rows: 5 brands x 5 rates) |
| `L4_analysis/r19_summary.md` | Human-readable summary with hypothesis verdicts |
| `L4_analysis/r19_pre_registration_audit.md` | Compliance audit (no deviations) |
| `L4_analysis/r19_jshape_supplementary.md` | J-shape formal test (3 paired t-tests) |
| `L4_analysis/r19_h4_supplementary.md` | H4 architectural separation (Welch, underpowered) |
| `L4_analysis/r19_per_brand_supplementary.md` | Per-brand J-shape analysis |

---

## Validation

```bash
cd experiment

python validation/validate.py --all
# Or individually:
python validation/validate.py --check-completeness
python validation/validate.py --check-schemas
python validation/validate.py --check-integrity

# Regenerate checksums after intentional changes
python validation/validate.py --regenerate-checksums
```

---

## Required Environment Variables

```bash
export ANTHROPIC_API_KEY=...      # Claude Haiku 4.5
export OPENAI_API_KEY=...         # GPT-4o-mini
export GOOGLE_API_KEY=...         # Gemini 2.5 Flash
export DEEPSEEK_API_KEY=...       # DeepSeek V3
export GROQ_API_KEY=...           # Llama 3.3 70B (via Groq, free tier)
export CEREBRAS_API_KEY=...       # Qwen3 235B (via Cerebras, free tier)
export GROK_API_KEY=...           # Grok-3-mini (xAI, free tier)
```

Missing keys are skipped gracefully.
