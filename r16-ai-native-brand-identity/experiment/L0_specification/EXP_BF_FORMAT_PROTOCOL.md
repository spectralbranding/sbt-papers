# Experiment D: Brand Function Format Optimization -- Pre-Registration Protocol

**Study**: Brand Function Format Optimization
**Paper**: R16 AI-Native Brand Identity (Zharnikov, 2026x)
**Proposition tested**: P6 (behavioral metamerism) + R19 rate-distortion extension
**Protocol registered**: 2026-04-16 (before data collection)
**Script**: `experiment/L2_prompts/exp_bf_format.py`
**Random seed**: 20260416

---

## Rationale

R19 (Zharnikov, 2026aa) demonstrated a J-shaped rate-distortion curve: 1-5 ordinal scales (19 bits) yield lower distortion than both coarser (8-3 bits) and finer (26-bit) response formats. This finding prescribes the *response* format. But brand functions -- the *input* specifications fed to AI systems -- also vary in representational format: structured JSON, prose narratives, tabular data, ranked lists, or bare numerical vectors. No study has tested which input format maximizes AI comprehension fidelity. This experiment fills that gap.

The practical question: when a brand manager deploys a brand function at `.well-known/brand.json`, what format should the specification take to maximize AI systems' ability to reconstruct the intended brand profile?

---

## Hypotheses

**H1 (Structured advantage)**: The full JSON format (scores + positioning text + key_signals) will produce the lowest mean distortion (highest cosine similarity to canonical profile) compared to all other formats. Rationale: structured data provides both quantitative anchors and qualitative context, reducing ambiguity.

**H2 (Prose penalty)**: Prose narrative format will produce higher distortion than JSON structured format (paired t-test, p < .05, Bonferroni-corrected alpha = .00625 for 8 dimensions). Rationale: unstructured text allows LLM priors to dominate over specification content.

**H3 (Score-only floor)**: Score-only vector format (bare numbers, no context) will produce the highest distortion among all formats. Rationale: without dimensional labels or positioning context, the numerical vector is maximally ambiguous.

**H4 (Cross-model consistency)**: The format ranking (best-to-worst) will be consistent across all 5 LLM architectures (Kendall's W > .7 for concordance of format rankings across models). Rationale: format effects should be structural, not model-specific.

**H5 (Dimension-specific effects)**: Format choice will disproportionately affect "soft" dimensions (Cultural, Temporal, Ideological, Narrative) relative to "hard" dimensions (Economic, Semiotic). Rationale: hard dimensions have less interpretive ambiguity and are more robust to format variation.

---

## Power Analysis

**Design**: 5 formats x 5 brands x 5 models x 3 repetitions = 375 total calls.

For H1 (format comparison): Each format has 5 brands x 5 models x 3 reps = 75 observations. Paired comparisons across formats within-brand-within-model yield 5 x 5 x 3 = 75 paired observations. For a medium effect (Cohen's d = .5), paired t-test with n = 75 gives power = .97 at alpha = .00625 (Bonferroni for 8 pairwise format comparisons). For a small effect (d = .3), power = .64. Sufficient for detecting medium-to-large effects.

For H4 (concordance): Kendall's W with 5 raters (models) ranking 5 items (formats) has good power at W > .7 with n = 5.

**Bonferroni correction**: 8 tests maximum (5 format pairwise + 3 secondary), alpha_adj = .05/8 = .00625.

---

## Design

### Independent Variable

**Format condition** (5 levels, within-subject):

| Code | Format | Description | Information content |
|------|--------|-------------|-------------------|
| F1 | JSON structured | Full brand function: scores + positioning + key_signals per dimension | High (quantitative + qualitative + examples) |
| F2 | Prose narrative | Natural language paragraph describing brand across all 8 dimensions | High (qualitative only, no numeric anchors) |
| F3 | Tabular minimal | Dimension name + score (1-10) only, no explanatory text | Medium (quantitative only) |
| F4 | Ranked list | Dimensions ranked by importance with brief rationale, no scores | Medium (ordinal only) |
| F5 | Score-only vector | Eight numbers in dimension order, no labels or context | Low (bare quantitative) |

### Dependent Variables

1. **Cosine similarity** to canonical profile (primary): cosine(recovered_weights, canonical_profile)
2. **Per-dimension MAE**: |recovered_score_i - canonical_score_i| for each of 8 dimensions
3. **Parse success rate**: proportion of responses yielding valid 8-dimensional weight vectors
4. **Response time** (ms): latency per call

### Stimuli

Five canonical SBT reference brands: Hermes, IKEA, Patagonia, Tesla, Erewhon.

Canonical profiles (dimension order: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal):
- Hermes: [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]
- IKEA: [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]
- Patagonia: [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]
- Erewhon: [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5]
- Tesla: [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]

### Models (5 LLMs, 3 clusters)

| Cluster | Model | Provider |
|---------|-------|----------|
| Western cloud | Claude Haiku 4.5 | Anthropic |
| Western cloud | GPT-4o-mini | OpenAI |
| Western cloud | Gemini 2.5 Flash | Google |
| Chinese cloud | DeepSeek V3 | DeepSeek |
| Western cloud | Grok 4.1 Fast | xAI |

### Dimension ordering

Latin-square balanced: 8 cyclic orderings. Each trial uses ordering_index = (brand_index * 5 + format_index * 3 + rep) % 8 to ensure balanced coverage.

### Temperature

Fixed at 0.7 across all models and conditions.

---

## Prompt Design

### System prompt (constant across all conditions)

```
You are a brand perception analyst. You will be given information about a brand's positioning across eight perceptual dimensions. Your task is to read the brand specification and then produce a perceptual weight profile: allocate exactly 100 points across the eight dimensions to reflect the brand's relative emphasis. Respond with valid JSON only: {"Semiotic": X, "Narrative": X, "Ideological": X, "Experiential": X, "Social": X, "Economic": X, "Cultural": X, "Temporal": X}.
```

Note: The system prompt uses R2-equivalent response format (100-point allocation) as established in R19 for optimal distortion. The dimension ORDER in the user prompt varies per trial (Latin-square balanced).

### User prompt templates

**F1 (JSON structured)**: Presents the full brand function JSON (as in r15 experiment brand_functions/) with scores, positioning text, and key_signals for each dimension. Asks: "Based on this brand specification, allocate 100 points..."

**F2 (Prose narrative)**: Converts the same information into flowing paragraphs. Same content, different format. Asks: "Based on this brand description, allocate 100 points..."

**F3 (Tabular minimal)**: Presents "Dimension: Score" pairs only (e.g., "Semiotic: 9.5/10"). Asks: "Based on these brand dimension scores, allocate 100 points..."

**F4 (Ranked list)**: Presents dimensions ranked by canonical score with brief rationale (e.g., "1. Temporal (9.5) -- 187 years heritage"). Asks: "Based on this brand priority ranking, allocate 100 points..."

**F5 (Score-only vector)**: Presents only "[9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]" with dimension names in order. Asks: "These scores represent a brand's positioning on [dim1, dim2, ...]. Allocate 100 points..."

---

## Stopping Rules

1. **Minimum**: 3 repetitions per cell (pre-registered)
2. **No extension**: Fixed at 3 reps. Power is sufficient at n = 75 per format.
3. **Null reporting**: If no format differences reach significance after Bonferroni correction, report null with effect sizes and CIs.

---

## Analysis Plan

### Primary Analysis

1. One-way repeated-measures ANOVA on cosine similarity across 5 format conditions (within-brand, within-model, averaged over repetitions). Report F-statistic, p-value, eta-squared.
2. Post-hoc pairwise comparisons (paired t-tests) with Bonferroni correction (alpha_adj = .00625).
3. 95% bootstrap CIs on mean cosine similarity per format (n = 10,000 resamples).

### Secondary Analyses

4. Kendall's W concordance coefficient for format ranking consistency across models (H4).
5. Two-way ANOVA: Format x Dimension interaction on per-dimension MAE (H5). Report interaction F, p, partial eta-squared.
6. Per-model breakdown of format effects to identify model-specific sensitivities.

### Effect Size Measures

- Cohen's d for pairwise format comparisons
- Eta-squared for ANOVA effects
- Kendall's W for concordance
- 95% bootstrap CIs on all primary measures

### Exploratory Analyses

- Format x Brand interaction (does format matter more for some brands?)
- Parse success rate differences across formats (chi-square)
- Response time differences across formats (Kruskal-Wallis)

---

## Exclusion Criteria

- API errors: recorded with `weights_valid: false`, excluded from distortion analysis but included in parse-rate analysis
- Models with >50% error rate in any condition: excluded from aggregate but reported in supplementary
- Rate-limited responses that succeed after retry: included (retry count logged)

---

## Data Management

- JSONL output: `experiment/L3_sessions/exp_bf_format.jsonl`
- Analysis output: `experiment/L4_analysis/exp_bf_format_results.json`
- Summary tables: `experiment/L4_analysis/exp_bf_format_summary.md`
- HuggingFace dataset: `experiment/hf_dataset/`

---

## Amendments

| Date | Amendment | Rationale |
|------|-----------|-----------|
| 2026-04-16 | Initial protocol | Pre-registration before data collection |
