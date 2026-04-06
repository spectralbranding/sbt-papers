# R15 AI Search Metamerism -- Pre-Registration Protocol

**Study**: Spectral Metamerism in AI-Mediated Brand Perception
**Paper**: Zharnikov, D. (2026v)
**Proposition tested**: AI-mediated brand search produces systematic dimensional collapse
**Protocol registered**: 2026-04-03 (before data collection)
**Script**: `ai_search_metamerism.py` (commit hash recorded in metadata.yaml)

---

## Background

Spectral metamerism in optics describes two surfaces that appear identical under one
illuminant but differ under another. The analogous phenomenon in AI-mediated brand
perception: brands that appear interchangeable through an LLM search interface may
have structurally different perception clouds when observed directly by human cohorts
across all 8 SBT dimensions.

The theoretical claim is that LLMs over-weight Economic and Semiotic dimensions because
these are most quantifiable and explicitly represented in text corpora (price comparisons,
visual descriptions), while under-weighting Narrative, Ideological, Cultural, and Temporal
dimensions because these are perception-dependent and require direct observer experience
to collapse from possibility space to conviction.

---

## Hypotheses

**H1 (Dimensional over-weighting)**: LLMs will cite Economic and Semiotic dimensions
significantly more frequently than other dimensions in recommendation and differentiation
prompts. Operationalized as: aggregate (Economic + Semiotic) citation rate > 2/8 = 0.250
(uniform baseline across 8 dimensions). Statistical test: one-sample binomial test,
alternative = "greater", alpha = 0.05.

**H2 (Convergent collapse)**: The dimensional citation frequency pattern will be
consistent across model families, indicating the collapse is a property of text-based
training corpora rather than any specific architecture. Operationalized as: Fleiss'
kappa on binary above/below-baseline citation patterns across models >= 0.40 (moderate
agreement threshold).

**H3 (Differential probe variance)**: Cross-model variance in dimension-specific probe
scores will be significantly lower for Economic and Semiotic dimensions than for
Narrative, Cultural, and Temporal dimensions. Operationalized as: Welch's t-test
comparing mean cross-model variance between hard-dimension cluster
(Semiotic, Economic, Experiential) and soft-dimension cluster
(Narrative, Ideological, Cultural, Temporal), alternative = "soft > hard", alpha = 0.05.

**H4 (Soft-dimension pair convergence)**: Brand pairs designed to differ primarily on
soft dimensions (Narrative, Ideological, Cultural, Temporal) will show higher cross-model
recommendation convergence (higher agreement rate on recommended brand) than brand pairs
designed to differ on hard dimensions (Semiotic, Economic, Experiential). Operationalized
as: mean recommendation agreement rate for soft pairs > mean agreement rate for hard pairs.

---

## Design

### Variables

**Independent variables:**
- Dimension type (within-dimension): hard (Semiotic, Economic, Experiential) vs
  soft (Narrative, Ideological, Cultural, Temporal)
- Brand pair type (between-pair): hard-differentiated (3 pairs) vs soft-differentiated
  (5 pairs) vs mixed (2 pairs)
- Model cluster (between-model): Western cloud, Chinese cloud, local open-weight

**Dependent variables:**
- Dimensional citation rate: proportion of responses citing each dimension (0-1)
- Dimensional Collapse Index (DCI): (Economic + Semiotic citation rate) / sum(all rates)
- Dimension probe score: 0-10 score per brand per dimension per model per run
- Cross-model probe variance: variance of mean scores across model families
- Recommendation agreement rate: proportion of models recommending the same brand

### Brand Pairs (10 pairs across 5 category types)

| Pair ID | Brand A | Brand B | Category | Differentiating Dims | Pair Type |
|---------|---------|---------|----------|----------------------|-----------|
| luxury_heritage | Hermes | Coach | luxury leather goods | Temporal, Cultural | soft |
| purpose_driven | Patagonia | Columbia | outdoor apparel | Ideological, Narrative | soft |
| premium_tech | Apple | Samsung | consumer electronics | Experiential, Semiotic | hard |
| artisanal_food | Erewhon | Whole Foods | specialty grocery | Social, Economic | hard |
| auto_disruption | Mercedes | Tesla | premium automobiles | Temporal, Ideological | soft |
| indie_beauty | Glossier | Maybelline | cosmetics | Narrative, Social | mixed |
| craft_spirits | Hendricks | Gordons | gin and spirits | Cultural, Experiential | mixed |
| boutique_hotel | Aman | Four Seasons | luxury hospitality | Experiential, Temporal | mixed |
| heritage_sportswear | Nike | Shein | apparel | Narrative, Cultural | soft |
| ethical_finance | Aspiration | Chase | personal banking | Ideological, Social | soft |

### Prompt Types (18 prompts per pair per run per model)

1. **Recommendation** (1 per pair): Free prose recommendation with explanation
   - Measures: which dimensions are spontaneously cited when making a recommendation
   - No JSON required; dimension extraction via keyword matching

2. **Differentiation** (1 per pair): Structured comparison with JSON output
   - Measures: which dimensions are identified as key differentiators
   - Includes self-reported dimensions_cited field + keyword extraction fallback

3. **Dimension probes** (8 per brand x 2 brands = 16 per pair): Structured 0-10 scoring
   - Plain-language descriptions (no SBT jargon in prompts)
   - Measures: absolute dimensional scores and cross-model variance

### Models (6 model families, 3 clusters)

| Cluster | Short Name | Model ID | Provider |
|---------|-----------|----------|----------|
| Western cloud | claude | claude-haiku-4-5 | Anthropic |
| Western cloud | gpt | gpt-4o-mini | OpenAI |
| Western cloud | gemini | gemini-2.5-flash | Google |
| Chinese cloud | deepseek | deepseek-chat | DeepSeek |
| Chinese cloud | qwen | qwen-plus-latest | Alibaba DashScope |
| Local open-weight | qwen3_local | qwen3:30b | Ollama |
| Local open-weight | gemma4_local | gemma4:latest | Ollama |

### Call Volume

| Configuration | Formula | Total |
|--------------|---------|-------|
| 1 run pilot | 10 pairs x 18 prompts x 6 models x 1 run | 1,080 calls |
| 3 run standard | 10 pairs x 18 prompts x 6 models x 3 runs | 3,240 calls |
| 5 run extended | 10 pairs x 18 prompts x 6 models x 5 runs | 5,400 calls |

Estimated cost at ~$0.001/call average: $1.08 (pilot), $3.24 (standard), $5.40 (extended).

### Temperature

All calls use temperature = 0.7. This is intentionally higher than the default (not 0.0)
because the experiment measures cross-model variance in responses. Temperature 0.0 would
suppress within-model variation; 0.7 provides realistic variation while maintaining
coherent outputs.

---

## Stopping Rules

1. **Minimum**: 3 runs per prompt per model (established before data collection)
2. **Extension trigger**: If H1 binomial p > 0.10 after 3 runs, extend to 5 runs
3. **Null reporting**: If H1 binomial p > 0.10 after 5 runs, report null result with
   power analysis estimating required N for 80% power
4. **Pilot rule**: Run 1 run (1,080 calls) first to verify data collection pipeline;
   review session log before scaling to 3 runs

---

## Analysis Plan

### Primary Analysis

Fisher's exact test is not applicable here (no binary outcome per call). Primary test:

**H1**: One-sample binomial test on aggregate Economic + Semiotic citation counts vs
null hypothesis that each dimension is cited at rate 1/8 = 0.125.
- Unit of analysis: individual recommendation or differentiation response
- Expected: Economic + Semiotic jointly cited in > 25% of responses

### Secondary Analyses

**H2**: Fleiss' kappa computed on binary (above/below uniform baseline) citation
patterns. Each dimension is a "subject"; each model is a "rater."

**H3**: Cross-model probe score variance computed per brand per dimension.
Welch's t-test on variance values comparing hard-dim cluster to soft-dim cluster.
Effect size: Cohen's d.

**H4**: Recommendation agreement rate per brand pair type (soft vs hard).
Simple proportion comparison (no formal test in pre-registration; treated as
exploratory if sample size too small for t-test).

### Effect Size Measures

- Cohen's d for H3 (variance comparison between dim clusters)
- Relative lift: (observed DCI - 0.250) / 0.250 for H1
- Kappa interpretation: 0-0.20 slight, 0.21-0.40 fair, 0.41-0.60 moderate,
  0.61-0.80 substantial, 0.81-1.0 almost perfect

### Exploratory Analyses (not pre-registered, clearly labeled)

- Per-cluster citation rates (Western cloud vs Chinese cloud vs local open-weight)
- Cloud-local pair comparison (Qwen Plus vs Qwen3 30B; Gemini vs Gemma 4 27B)
- Correlation between pair DCI and pair's designed differentiating dimension type
- Brand-level spectral profiles derived from probe scores vs canonical SBT profiles

---

## Exclusion Criteria

- API errors resulting in unparseable responses: recorded in JSONL with error field;
  dimension citations for that call treated as empty set (contributes 0 to all dims)
- Models with >50% error rate across any prompt type: excluded from aggregate statistics,
  reported separately in supplementary material
- Dimension probe responses where score cannot be parsed as 0-10 numeric after 3
  parse attempts: treated as missing, excluded from probe variance analysis
- Rate-limited responses that succeed after retry: included in analysis (retry count
  available in session log)

---

## Data Management

- **Raw session logs**: `experiment/L3_sessions/session_log.jsonl` (every prompt-response
  pair with timestamps, latency, parsed output, and error field)
- **Configuration**: `experiment/L1_configuration/` (model configs, API version hashes)
- **Rendered prompts**: `experiment/L2_prompts/` (dimension descriptions, prompt templates)
- **Analysis outputs**: `experiment/L4_analysis/` (tables, statistics)
- **Results**: `experiment/results.json` (full structured results)
- **Summary**: `experiment/summary_tables.md` (formatted Markdown tables)
- **Metadata**: `experiment/metadata.yaml` (package versions, hardware, git hash)

---

## Transparency

- All code is public: `github.com/spectralbranding/sbt-papers/r15-ai-search-metamerism/`
- Preprint available: target Zenodo upload before journal submission
- Session logs committed to repository after data collection is complete
- This protocol was written before the first live API call

---

## Amendments

| Date | Amendment | Rationale |
|------|-----------|-----------|
| 2026-04-03 | Initial protocol | Pre-registration before data collection |
