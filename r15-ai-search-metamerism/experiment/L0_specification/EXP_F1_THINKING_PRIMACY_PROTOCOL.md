# Experiment F1: Thinking-Mode Primacy

**Protocol version**: 1.0
**Date**: 2026-04-17
**Status**: PRE-REGISTERED (frozen before data collection)
**Open Problem**: Does chain-of-thought reasoning eliminate the shallow-attention artifact underlying serial position bias?
**Paper target**: R15 extension or PRISM instrument paper

---

## Research Question

Does thinking-mode (chain-of-thought) processing reduce the serial position (primacy) effect in structured LLM elicitation, and does any such reduction depend on response format?

## Background

Experiment E (Primacy Effect Generalization) established that serial position of a dimension in the prompt systematically biases weight allocation: dimensions listed first receive inflated weights relative to dimensions listed last. The effect is large in JSON allocation format (d = 1.39) and attenuated but present in Likert format (d = .22).

A mechanistic account of primacy posits shallow attention: the model allocates disproportionate weight to tokens encountered early in the input before sufficient context has accumulated. Thinking/reasoning models process the full input through an explicit chain-of-thought before generating the final answer. This intermediate deliberation step may re-read dimensions holistically and counteract the shallow-attention artifact.

If thinking mode eliminates primacy in JSON format but has no effect on Likert format (which already attenuates the bias), this constitutes evidence that the mechanism is format-specific and tied to constrained allocation rather than attention per se.

This experiment operationalizes the contrast by pairing each standard model with its thinking-mode counterpart from the same provider family, holding all other factors constant.

---

## Design

### Independent Variables

**IV1: Thinking mode** (between-condition, 2 levels)
1. **Standard**: normal API call, no chain-of-thought reasoning
2. **Thinking**: model-specific thinking activation (see Model Pairs below)

**IV2: Response format** (between-condition, 2 levels)
1. **JSON**: Allocate integer weights summing to 100 across 8 dimensions
2. **Likert**: Rate each of 8 dimensions on 1-5 scale (all 8 presented simultaneously)

**IV3: Dimension position** (within-subject, 8 levels)
Positions 1 through 8 in the prompt. Manipulated via 8 Latin-square cyclic orderings.

### Model Pairs (Standard vs Thinking)

| Pair | Standard | Thinking | Provider |
|------|----------|----------|----------|
| gemini | `gemini-2.5-flash` (thinking_config disabled) | `gemini-2.5-flash` (thinking_budget=1024) | Google |
| deepseek | `deepseek-chat` (V3) | `deepseek-reasoner` (R1) | DeepSeek |
| grok | `grok-4-1-fast-non-reasoning` | `grok-4-1` (reasoning mode) | xAI |

Each pair shares the same provider and base architecture family, isolating the thinking-mode activation as the only variable.

### Thinking Activation Details

**Gemini**: Same model (`gemini-2.5-flash`), different `generation_config`:
- Standard: `thinking_config={"thinking_budget": 0}` (disables thinking)
- Thinking: `thinking_config={"thinking_budget": 1024}` (enables explicit CoT)

**DeepSeek**: Separate model endpoints:
- Standard: `deepseek-chat` (V3, instruction-tuned)
- Thinking: `deepseek-reasoner` (R1, trained with reinforcement learning on reasoning chains)

**Grok**: Separate model endpoints:
- Standard: `grok-4-1-fast-non-reasoning`
- Thinking: `grok-4-1` (reasoning mode)

### Stimuli

**Brands** (canonical 5, same as Experiment E):
- Hermes: [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]
- IKEA: [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]
- Patagonia: [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]
- Erewhon: [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5]
- Tesla: [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]

**Dimensions** (SBT canonical order):
Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal

**Latin-square orderings**: 8 cyclic rotations of the canonical dimension list.

### Sample Size

**Per cell** (thinking_mode x format x model_pair): 8 orderings x 5 brands x 1 rep = 40 calls
**Total**: 2 modes x 2 formats x 3 model_pairs x 8 orderings x 5 brands x 1 rep = **480 calls**

### Power Analysis

Using Experiment E effect sizes as priors:
- JSON primacy: d = 1.39 (large)
- Likert primacy: d = .22 (small)
- Expected reduction from thinking mode: moderate (d = .40-.60 on the primacy score)
- For independent-samples t-test on primacy magnitude, alpha = .05, power = .80, d = .40: n = 99 per group
- Per thinking-mode condition per format: 3 models x 8 orderings x 5 brands = 120 observations
- Conclusion: Adequately powered for medium effects; underpowered for small effects (d < .25). Pre-specified as inconclusive if d < .25.

### Dimension Ordering

Latin-square balanced (8 cyclic orderings). Each call receives ordering index `trial_idx % 8`.

### Random Seed

42 (all randomization reproducible)

---

## Hypotheses

### H_F1a: Thinking Mode Reduces JSON Primacy

Thinking-mode processing reduces the primacy effect magnitude (positions 1-2 vs 7-8 weight difference) in JSON allocation format.

- **Test**: Independent-samples t-test on per-trial primacy score (mean weight pos 1-2 minus mean weight pos 7-8) between standard and thinking conditions, within JSON format, per model pair
- **Alpha**: .05
- **Effect size**: Cohen's d + 95% bootstrap CI (10,000 iterations)
- **Success criterion**: p < .05 AND d >= .30 AND thinking_mean_primacy < standard_mean_primacy (directional)
- **Pooled test**: Combine across all three model pairs; report per-pair as secondary

### H_F1b: Thinking Mode Has No Effect on Likert Primacy

Thinking-mode processing does not significantly change the primacy effect in Likert format (because Likert already attenuates the bias mechanistically).

- **Test**: Independent-samples t-test on per-trial primacy score between standard and thinking conditions, within Likert format, per model pair
- **Alpha**: .05 (null hypothesis retained if p >= .05 AND d < .25)
- **Success criterion**: p >= .05 AND d < .25 across all three model pairs (null result)
- **Note**: This is a null-hypothesis test. Report Bayes factor (BF01) as supplementary evidence for the null.

### H_F1c: Model-Specific Primacy Reduction Magnitudes

The magnitude of thinking-mode primacy reduction (Cohen's d on primacy score) differs across the three model pairs.

- **Test**: Report per-model-pair d and 95% CI. No pooling. Descriptive comparison only.
- **Success criterion**: At least one pair shows d >= .50 AND at least one pair shows d < .30 (heterogeneity present)
- **Note**: This is exploratory-confirmatory; the heterogeneity threshold is pre-registered but the direction is not.

---

## Prompts

### JSON Format (condition = "json")

```
System: You are evaluating brand perception.
User: Evaluate the brand {brand_name} by allocating importance weights across
eight dimensions of brand perception. The weights must sum to 100.
Respond in this exact JSON format:
{"Semiotic": <weight>, "Narrative": <weight>, ...}
```

### Likert Format (condition = "likert")

```
System: You are evaluating brand perception.
User: Evaluate the brand {brand_name} on eight dimensions of brand perception.
Rate each dimension on a scale of 1-5 (1 = not at all important, 5 = extremely important).
Respond in this exact JSON format:
{"Semiotic": <1-5>, "Narrative": <1-5>, ...}
```

Dimensions are presented in the Latin-square order for each call.

---

## Analysis Plan

### Primary Analyses (pre-registered)

1. **Position weight extraction**: For each record, map each dimension's weight to its position (1-8) based on `dimension_order`. For Likert, normalize to 0-100 scale (divide by total and multiply by 100).

2. **Per-trial primacy score**: For each valid record, compute `primacy_score = mean(pos 1-2 weights) - mean(pos 7-8 weights)`.

3. **H_F1a test**: For JSON format only, compare primacy_score distributions between standard and thinking conditions. Independent t-test. Cohen's d + 95% bootstrap CI. Report per model pair and pooled (all three pairs combined).

4. **H_F1b test**: For Likert format only, compare primacy_score distributions between standard and thinking conditions. Independent t-test. Report Cohen's d and p-value. Compute BF01 under unit-information prior.

5. **H_F1c test**: Compute Cohen's d for primacy reduction per model pair. Report 95% CI for each. Test for heterogeneity (Cochran's Q if three estimates with CIs available).

### Secondary Analyses (pre-registered)

6. **Full position curve**: Mean weight by position (1-8) for each of the four conditions (json_standard, json_thinking, likert_standard, likert_thinking). Linear trend slope and R-squared per condition.

7. **Primacy slope**: Linear regression of weight on position (1-8) per condition. Slope (negative = primacy) as single summary statistic. Compare slopes between thinking modes per format.

8. **Per-model primacy slopes**: Report position slopes separately for each of the 6 model variants (3 pairs x 2 modes).

### Exploratory Analyses (labeled as such)

9. **Thinking token usage**: Does thinking_tokens_used correlate with primacy reduction? (Gemini only, where thinking_budget is bounded.)
10. **Brand moderation**: Does thinking-mode primacy reduction vary by brand?
11. **Recency asymmetry**: Does thinking mode differentially affect positions 1-2 vs 7-8, or does it shift the entire curve uniformly?

## Multiple Comparison Correction

- H_F1a per-pair tests (3 pairs): Bonferroni alpha = .017
- H_F1b per-pair tests (3 pairs): Bonferroni alpha = .017
- Secondary position-curve tests: Benjamini-Hochberg FDR at .05

## Exclusion Criteria

- API errors: recorded with error field, excluded from analysis
- Unparseable JSON: recorded, excluded from analysis
- JSON weights outside 100 +/- 5: included after renormalization, flagged
- Likert values outside 1-5: excluded
- Models with >50% error rate in any condition: excluded from that condition's analysis

## Reproducibility

- Random seed: 42
- All scripts committed before execution
- JSONL is append-only
- Full prompts stored in each record
- Thinking mode, format, and dimension order stored per record
- API metadata (tokens, latency, cost) per call
- Temperature: .7 for standard; .7 for thinking (where overrideable; some thinking endpoints fix temperature)
- 3-second minimum delay between API calls
- Exponential backoff on 429: 5s, 10s, 20s, 60s, 120s

## JSONL Schema (extends EXPERIMENT_DATA_STANDARD.md base)

**Required base fields**: timestamp, model, prompt_type, prompt

**Recommended base fields**: model_id, response, parsed, latency_ms, tokens_in, tokens_out, error, temperature, brand, run

**Experiment-specific fields** (additional):
- `thinking_mode`: bool -- True if thinking/reasoning was activated for this call
- `response_format`: str -- "json" or "likert"
- `dimension_order`: list[str] -- ordered list of 8 dimension names used in this call
- `ordering_index`: int -- 0-7, which Latin-square rotation
- `position_weights`: dict[str, float] -- weight at each position 1-8 (derived from parsed + dimension_order)
- `primacy_score`: float -- mean(pos 1-2) - mean(pos 7-8), null if parse failed
- `model_pair`: str -- "gemini", "deepseek", or "grok"
- `thinking_tokens`: int or null -- tokens used for chain-of-thought (provider-specific; null if unavailable)

**prompt_type**: `primacy_thinking` (new; must be registered in `validation/schemas/session_record.schema.json` before data collection)

## Estimated Cost

480 calls across 6 model variants (80 per variant):
- gemini-2.5-flash standard: ~$0.0003/call x 80 = ~$0.02
- gemini-2.5-flash thinking: ~$0.0010/call x 80 = ~$0.08 (thinking tokens add cost)
- deepseek-chat (V3): ~$0.0005/call x 80 = ~$0.04
- deepseek-reasoner (R1): ~$0.0020/call x 80 = ~$0.16
- grok-4-1-fast-non-reasoning: ~$0.004/call x 80 = ~$0.32
- grok-4-1 reasoning: ~$0.008/call x 80 = ~$0.64
- **Total estimated: ~$1.26**

Conservative estimate accounting for thinking token overhead: ~$1.50. Capped at $2.00 before aborting.

---

*This protocol was committed before any API calls were made. Any analysis not listed above is labeled EXPLORATORY in the results.*
