# Experiment E: Primacy Effect Generalization

**Protocol version**: 1.0
**Date**: 2026-04-16
**Status**: PRE-REGISTERED (frozen before data collection)
**Open Problem**: Extends R15 Latin-square control into a direct test
**Paper target**: R15 extension or PRISM instrument paper

---

## Research Question

Does the serial position of a dimension in the prompt systematically bias the weight allocated to it, and does this primacy/recency effect generalize across response formats (JSON allocation, Likert rating, ranking, natural language)?

## Background

R15 employed Latin-square balanced dimension orderings across 21,350 API calls to *control* for ordering effects, but never directly *tested* whether ordering is a significant source of variance. If LLMs exhibit primacy bias (over-weighting dimensions listed first), the Latin-square design averages this out across conditions -- but the effect itself remains undocumented. This experiment isolates dimension position as the independent variable and tests whether the effect magnitude depends on response format.

The distinction matters practically: if primacy exists and varies by format, PRISM instrument design should prefer formats that minimize positional bias (e.g., Likert over constrained allocation).

---

## Design

### Independent Variables

**IV1: Dimension position** (within-subject, 8 levels)
Position 1 through 8 in the prompt. Manipulated via 8 Latin-square cyclic orderings.

**IV2: Response format** (between-condition, 4 levels)
1. **JSON**: Allocate integer weights summing to 100 across 8 dimensions (R15 standard)
2. **Likert**: Rate each of 8 dimensions on 1-5 scale (1 = not at all important, 5 = extremely important). All 8 presented simultaneously with Latin-square ordering. JSON response with 8 integer values.
3. **Ranking**: Rank 8 dimensions from most important (1) to least important (8). All presented simultaneously with Latin-square ordering.
4. **Natural language (NL)**: Describe which dimensions matter most/least for this brand and estimate a percentage weight for each. Free-form text, parsed to weights.

### Stimuli

**Brands** (canonical 5):
- Hermes: [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]
- IKEA: [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]
- Patagonia: [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]
- Erewhon: [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5]
- Tesla: [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]

**Models** (5):
- Claude Haiku 4.5 (Anthropic)
- GPT-4o-mini (OpenAI)
- Gemini 2.5 Flash (Google)
- DeepSeek V3 (DeepSeek)
- Grok 4.1 Fast (xAI)

### Sample Size

**Per format**: 8 orderings x 5 brands x 5 models x 3 reps = 600 calls
**Total**: 4 formats x 600 = **2,400 calls**

### Power Analysis

Using effect sizes from R15 prompt sensitivity analysis as priors:
- Smallest relevant positional effect: eta-sq = .06 (small-medium)
- Expected effect: eta-sq = .14 (medium, typical for serial position effects in survey design)
- For mixed ANOVA with 8 positions x 4 formats, alpha = .05, power = .80:
  - Medium effect (eta-sq = .14): n = 12 per cell (we have 75 per cell = 5 brands x 5 models x 3 reps)
  - Small effect (eta-sq = .06): n = 28 per cell (well exceeded)
- Conclusion: Design is adequately powered for small-medium effects within each format.

### Dimension Ordering

Latin-square balanced (8 cyclic orderings from DIMENSIONS). Each call receives one of 8 orderings, assigned deterministically by `(format_idx * 600 + brand_idx * models * reps + model_idx * reps + rep_idx) % 8`.

### Random Seed

42 (all randomization reproducible)

---

## Hypotheses

### H1: Primacy Effect in JSON Format
Dimensions presented in positions 1-2 receive significantly higher weights than dimensions in positions 7-8 in the JSON allocation format.
- **Test**: Paired t-test on mean weight at positions 1-2 vs positions 7-8 (aggregated across brands, models, reps)
- **Alpha**: .05
- **Effect size**: Cohen's d + 95% bootstrap CI (10,000 iterations)
- **Success criterion**: p < .05 AND d >= .30 (small-medium)

### H2: Primacy Effect Generalizes Across Formats
The primacy effect (positions 1-2 vs 7-8 weight difference) is significant in all 4 response formats.
- **Test**: Within each format, paired t-test on position 1-2 vs 7-8 weights. Bonferroni correction for 4 tests (alpha = .0125 per test).
- **Success criterion**: At least 3 of 4 formats show significant primacy at corrected alpha.

### H3: Likert Format Attenuates Primacy
The primacy effect magnitude is smaller in Likert format than in JSON format, because Likert ratings are independent (each dimension rated on its own scale) rather than zero-sum (weights must sum to 100).
- **Test**: Independent-samples t-test on primacy magnitude (mean pos 1-2 weight minus mean pos 7-8 weight) between JSON and Likert conditions.
- **Alpha**: .05
- **Success criterion**: Cohen's d >= .40 AND JSON primacy > Likert primacy.

### H4: Cross-Model Consistency
The primacy effect direction (positive = primacy, negative = recency) is consistent across all 5 models.
- **Test**: Sign consistency: do all 5 models show the same direction? Report per-model primacy magnitude and 95% CI.
- **Success criterion**: At least 4 of 5 models show the same direction.

---

## Prompts

### JSON Format (condition = "json")
```
System: You are evaluating brand perception.
User: Evaluate the brand {brand_name} by allocating importance weights across
eight dimensions of brand perception. The weights must sum to 100.
Respond in this exact JSON format:
{dim_json}
```

### Likert Format (condition = "likert")
```
System: You are evaluating brand perception.
User: Evaluate the brand {brand_name} on eight dimensions of brand perception.
Rate each dimension on a scale of 1-5 (1 = not at all important, 5 = extremely important).
Respond in this exact JSON format:
{dim_json_likert}
```

### Ranking Format (condition = "ranking")
```
System: You are evaluating brand perception.
User: Evaluate the brand {brand_name} by ranking these eight dimensions of brand
perception from most important (1) to least important (8). Each rank must be unique.
Respond in this exact JSON format:
{dim_json_ranking}
```

### Natural Language Format (condition = "nl")
```
System: You are evaluating brand perception.
User: Evaluate the brand {brand_name} across these eight dimensions of brand perception:
{dim_list}
For each dimension, explain its importance to this brand and estimate a percentage
weight (all weights should sum to approximately 100). Respond in JSON format:
{dim_json}
```

---

## Analysis Plan

### Primary Analyses (pre-registered)

1. **Position weight extraction**: For each record, map each dimension's weight to its position (1-8) in that call's ordering. Normalize Likert (multiply by 20 to 0-100 scale), invert ranking (9 - rank, then normalize to sum to 100), parse NL weights.

2. **H1 test**: Paired t-test on mean weight at positions 1-2 vs 7-8 in JSON condition. Effect size: Cohen's d + 95% bootstrap CI.

3. **H2 test**: Within each format, paired t-test on position 1-2 vs 7-8. Bonferroni correction at alpha = .0125.

4. **H3 test**: Independent t-test on primacy magnitude (JSON vs Likert). Cohen's d + 95% CI.

5. **H4 test**: Per-model primacy magnitude with 95% CI. Count sign consistency.

### Secondary Analyses (pre-registered)

6. **Full position curve**: Mean weight by position (1-8) per format. Linear and quadratic trend tests.
7. **Brand moderation**: Does the primacy effect vary by brand? Two-way ANOVA: Position (8) x Brand (5) within JSON format.
8. **Per-dimension vulnerability**: Which dimensions are most affected by position? Report position x dimension interaction.

### Exploratory Analyses (labeled as such)

9. **Recency detection**: Is there a U-shaped curve (primacy + recency) or monotonic decline?
10. **Format x model interaction**: Does the format effect differ by model?
11. **Variance by position**: Does weight variance increase at later positions?

## Multiple Comparison Correction

- H2 per-format tests (4): Bonferroni alpha = .0125
- Per-dimension tests (8 dimensions): Bonferroni alpha = .006
- Exploratory analyses: Benjamini-Hochberg FDR at .05

## Exclusion Criteria

- API errors: recorded with error field, excluded from analysis
- Unparseable JSON: recorded, excluded
- JSON weights: sum outside 100 +/- 5 flagged, included after renormalization
- Likert values outside 1-5: excluded
- Rankings with duplicate values: excluded
- NL responses with no parseable weights: excluded
- Models with >50% error rate in any format: excluded from that format's analysis

## Reproducibility

- Random seed: 42
- All scripts committed before execution
- JSONL is append-only
- Full prompts stored in each record
- API metadata (tokens, response time, cost) per call
- Temperature: .7 for all models
- 3-second minimum delay between API calls
- Exponential backoff on 429: 5s, 10s, 20s, 60s, 120s

## JSONL Schema (extends 20-field base)

Standard fields: timestamp, experiment, model_id, model_provider, temperature, top_p, max_tokens, system_prompt, system_prompt_hash, user_prompt, user_prompt_hash, brand, condition, repetition, raw_response, parsed_weights, weights_valid, weight_sum_raw, response_time_ms, token_count_input, token_count_output, api_cost_usd

Experiment-specific fields:
- `response_format`: str (json, likert, ranking, nl)
- `dimension_order`: list[str] (ordering used for this call)
- `ordering_index`: int (0-7, which Latin-square rotation)
- `position_weights`: dict[int, float] (weight at each position 1-8, derived from parsed_weights + ordering)

## Estimated Cost

2,400 calls across 5 providers (480 per model):
- Claude Haiku: ~$0.001/call -> ~$0.48
- GPT-4o-mini: ~$0.0003/call -> ~$0.14
- Gemini Flash: ~$0.0003/call -> ~$0.14
- DeepSeek V3: ~$0.0005/call -> ~$0.24
- Grok Fast: ~$0.004/call -> ~$1.92
- **Total estimated: ~$2.92**

NL format prompts are longer and may increase cost ~50% for that condition. Conservative estimate: ~$3.50.

---

*This protocol was committed before any API calls were made. Any analysis not listed above is labeled EXPLORATORY in the results.*
