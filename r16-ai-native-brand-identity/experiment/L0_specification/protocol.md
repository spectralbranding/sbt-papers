# R16 Behavioral Metamerism Pilot — Pre-Registration Protocol

**Study**: Behavioral Metamerism in AI Brand Perception
**Paper**: Zharnikov (2026x), DOI 10.5281/zenodo.19391476
**Proposition tested**: P6 (behavioral metamerism)
**Protocol registered**: 2026-04-03 (before data collection)
**Script**: `behavioral_metamerism_pilot.py` (commit hash recorded in metadata)

---

## Hypotheses

**H1 (Metamerism existence)**: Brand pairs with high statistical similarity (BMI > 0.5) will exhibit low discrimination rates under the statistical-only condition across all LLM families. This tests whether statistical brand observation produces perceptual equivalence despite behavioral differences.

**H2 (Specification effect)**: The specification-augmented condition will significantly improve discrimination rates compared to the statistical-only condition (Fisher's exact test, p < 0.05; Cohen's h > 0.3). This tests whether behavioral specifications resolve metamerism.

**H3 (Variance reduction)**: Cross-model variance in brand characterizations will be significantly lower in the augmented condition than in the statistical condition (F-test, p < 0.05). This tests whether specifications align AI brand perception across architectures.

**H4 (Cross-architecture generality)**: The metamerism-discrimination relationship will replicate across Western cloud, Chinese cloud, and local open-weight model clusters with no significant cluster x condition interaction. This tests whether behavioral metamerism is architectural rather than training-corpus-dependent.

---

## Design

### Independent Variables
- **Condition** (within-model): statistical-only vs specification-augmented
- **Model cluster** (between-model): Western cloud, Chinese cloud, local open-weight

### Dependent Variables
- **Discrimination rate**: binary (can/cannot distinguish brand pair)
- **Discrimination confidence**: continuous (0-1 scale)
- **Prediction accuracy**: continuous (0-1 scale, behavioral prediction task)
- **Cross-model variance**: continuous (variance of confidence scores across models)

### Stimuli
- 6 synthetic DTC supplement brands (VitaCore, NutraPure, FormulaRx, CleanDose, ApexStack, RootWell)
- 15 brand pairs (all pairwise combinations)
- Brands designed with varying statistical-behavioral dissociation levels

### Models (7 LLMs, 4 clusters)

| Cluster | Model | Provider | Rationale |
|---------|-------|----------|-----------|
| Western cloud | Claude Haiku 3.5 | Anthropic | Constitutional AI alignment |
| Western cloud | GPT-4o-mini | OpenAI | RLHF alignment |
| Western cloud | Gemini 2.5 Flash | Google | MoE + distillation |
| Chinese cloud | DeepSeek V3 | DeepSeek | Chinese training corpus |
| Chinese cloud | Qwen Plus | Alibaba DashScope | Chinese e-commerce data |
| Local open-weight | Qwen3 30B | Ollama | Cloud-local pair with Qwen Plus |
| Local open-weight | Gemma 4 27B | Ollama | Cloud-local pair with Gemini |

Note: Claude Sonnet 4.6 run planned as additional data point (different scale, same family).

---

## Stopping Rules

1. **Minimum**: 3 runs per condition per model (established before data collection)
2. **Extension**: If Fisher's exact p > 0.10 after 3 runs, extend to 5 runs
3. **Null reporting**: If Fisher's exact p > 0.10 after 5 runs, report null result with power analysis

---

## Analysis Plan

### Primary Analysis
- Fisher's exact test comparing discrimination rates between conditions (statistical vs augmented)
- Unit of analysis: brand pair x model x run

### Secondary Analyses
- Wilcoxon signed-rank test on paired confidence scores (statistical vs augmented, per model)
- F-test (Levene's) comparing cross-model variance between conditions
- Bootstrap 95% CI on the highest-BMI brand pair (n=1000 resamples)

### Effect Size Measures
- Cohen's h for discrimination rate differences
- Cohen's d for confidence score differences
- Cramer's V for chi-square association strength
- Fleiss' kappa for inter-model agreement

### Exploratory Analyses
- Per-cluster discrimination rates (Western vs Chinese vs local)
- Cloud-local pair comparison (Qwen Plus vs Qwen3 30B; Gemini vs Gemma 4)
- Per-brand-pair BMI vs discrimination rate correlation

---

## Exclusion Criteria

- API errors resulting in unparseable responses: recorded as `{can_distinguish: false, confidence: 0.5}` and flagged in session log with `error` field
- Models with >50% error rate in any condition: excluded from aggregate statistics but reported separately in supplementary tables
- Rate-limited responses that succeed after retry: included (retry count logged)
- Responses that do not contain valid JSON after 3 parse attempts: treated as API errors

---

## Data Management

- **Raw session logs**: `experiment/L3_sessions/session_log.jsonl` (every prompt-response pair with timestamps)
- **Configuration**: `experiment/L1_configuration/` (model configs, API versions)
- **Rendered prompts**: `experiment/L2_prompts/rendered/` (exact prompts sent to each model)
- **Analysis outputs**: `experiment/L4_analysis/` (tables, figures, statistics)
- **Results**: `experiment/live_results.json` (structured results) + `experiment/live_summary_tables.md` (formatted tables)
- **Validation**: `experiment/validation/validate.py` (reproducibility checks)

---

## Transparency

- All code is public: `github.com/spectralbranding/sbt-papers/r16-ai-native-brand-identity/`
- Preprint available: Zenodo DOI 10.5281/zenodo.19391476
- Session logs will be committed to the repository after data collection
- This protocol was written before the first live API call

---

## Amendments

| Date | Amendment | Rationale |
|------|-----------|-----------|
| 2026-04-03 | Initial protocol | Pre-registration before data collection |
| 2026-04-03 | Added Claude Haiku 3.5 as first run | Cost-effective baseline; Sonnet 4.6 run planned as scale comparison |
| 2026-04-08 | Qwen Plus backfill planned | DashScope account verification pending |
