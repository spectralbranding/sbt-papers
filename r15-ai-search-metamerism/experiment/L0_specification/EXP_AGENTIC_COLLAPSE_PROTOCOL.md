# Experiment A: Multi-Step Agentic Collapse Compounding

**Protocol version**: 1.0
**Date**: 2026-04-16
**Status**: PRE-REGISTERED (frozen before data collection)
**Open Problem**: #3 (Agentic commerce integration)
**Paper target**: R15 extension or new R21

---

## Research Question

Does dimensional collapse compound across steps in a simulated AI shopping pipeline? When an LLM retrieves, compares, and recommends brands sequentially, does the Dimensional Collapse Index (DCI) increase monotonically, and is the compounding dimension-specific?

## Background

R15 established that LLMs exhibit dimensional collapse in single-step brand evaluation: Economic and Semiotic dimensions are systematically over-weighted relative to Narrative, Cultural, and Temporal dimensions. Open Problem #3 asks whether this collapse worsens in multi-step agentic commerce pipelines where each step's output constrains the next step's input. If collapse compounds, agentic shopping assistants would progressively erase brand differentiation across pipeline stages.

## Hypotheses

### H1: Monotonic DCI Increase
DCI increases monotonically across pipeline steps (step 3 > step 2 > step 1 > control).
- **Test**: Repeated-measures ANOVA: Step (4 levels: control, step 1, step 2, step 3) as within-subject factor
- **Alpha**: .05 (Bonferroni-corrected for 3 pairwise comparisons: .017)
- **Success criterion**: F-test significant AND monotonic trend (linear contrast p < .017)

### H2: Dimension-Specific Compounding
Cultural and Temporal dimensions collapse faster across steps than Economic.
- **Test**: Two-way repeated-measures ANOVA: Step (3) x Dimension (3: Cultural, Temporal, Economic)
- **Alpha**: .05
- **Success criterion**: Significant Step x Dimension interaction AND post-hoc pairwise comparisons show Cultural/Temporal slope > Economic slope

### H3: Ideological Signal Protection
Brands with strong Ideological signal (Patagonia, eta-sq from R15 Run 15 cohort data) compound less than brands with weak Ideological signal (Erewhon, Tesla).
- **Test**: Independent-samples t-test on DCI compounding rate (step 3 minus control) for strong-Ideological vs weak-Ideological brands
- **Alpha**: .05
- **Success criterion**: Cohen's d >= .50 (medium effect)

## Design

### Pipeline Steps

**Step 1 (Retrieval)**: LLM generates a consideration set from the product category.
**Step 2 (Comparison)**: LLM compares the focal brand against a competitor from Step 1, allocating weights across 8 dimensions.
**Step 3 (Recommendation)**: LLM makes a final recommendation with dimensional weights, using Step 2 comparison as context.
**Control**: Standard single-step PRISM-B evaluation (no pipeline context).

### Stimuli

**Brands** (canonical 5):
- Hermes: [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]
- IKEA: [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]
- Patagonia: [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]
- Erewhon: [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5]
- Tesla: [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]

**Categories** (5, matched to brands):
- Luxury fashion (Hermes)
- Home furnishings (IKEA)
- Outdoor gear (Patagonia)
- Specialty grocery (Erewhon)
- Electric vehicles (Tesla)

**Models** (5):
- Claude Haiku 4.5 (Anthropic, claude-haiku-4-5)
- GPT-4o-mini (OpenAI, gpt-4o-mini)
- Gemini 2.5 Flash (Google, gemini-2.5-flash)
- DeepSeek V3 (DeepSeek, deepseek-chat)
- Grok 4.1 Fast (xAI, grok-4-1-fast-non-reasoning)

### Sample Size

**Pipeline calls**: 5 categories x 5 brands x 5 models x 3 steps x 3 reps = 1,125
**Control calls**: 5 brands x 5 models x 3 reps = 75
**Extended control** (per-category context): 5 categories x 5 brands x 5 models x 1 rep = 125
**Total**: ~1,325 calls (conservative estimate; Step 1 may generate fewer parseable weight records)

### Power Analysis

Using effect sizes from R15 synthetic cohort experiments as priors:
- Smallest relevant effect: eta-sq = .091 (Cultural dimension, weakest cohort effect)
- Expected effect: eta-sq = .25 (medium, typical for dimensional effects)
- For repeated-measures ANOVA with 4 levels (control + 3 steps), alpha = .05, power = .80:
  - Small effect (eta-sq = .091): n = 45 per cell -> 225 per condition (we have ~375 per step)
  - Medium effect (eta-sq = .25): n = 18 per cell -> 90 per condition (well exceeded)
- Conclusion: Design is adequately powered for medium effects. Small effects may require pooling across categories.

### Dimension Ordering

Latin-square balanced (8 cyclic orderings). Each call receives one of 8 orderings, assigned deterministically by call index modulo 8.

### Random Seed

42 (all randomization reproducible)

## Prompts

### Step 1 (Retrieval)
```
System: You are a helpful AI shopping assistant.
User: I'm looking for {category} products. List 5 brands you'd recommend,
with a brief reason for each. Focus on what makes each distinctive.
```

### Step 2 (Comparison)
```
System: You are a helpful AI shopping assistant helping compare brands.
User: I'm considering {brand_A} and {brand_B} for {use_case}.
For each brand, allocate importance weights across eight perception dimensions.
Weights must sum to 100. Respond in JSON:
{{"brand_A": {{{dim_json}}}, "brand_B": {{{dim_json}}}}}
```
(Dimension order: Latin-square balanced per call)

### Step 3 (Recommendation)
```
System: You are a helpful AI shopping assistant making a final recommendation.
User: Based on your comparison, which brand would you recommend for {use_case}?
Score your recommended brand on these eight dimensions (weights sum to 100).
Explain your choice briefly. Respond in JSON:
{{"recommended": "...", "weights": {{{dim_json}}}, "reason": "..."}}
```

### Control (Single-step PRISM-B)
```
System: You are evaluating brand perception.
User: Evaluate the brand {brand_name} by allocating importance weights across
eight dimensions of brand perception. The weights must sum to 100.
Respond in this exact JSON format:
{{{dim_json}}}
```

## Analysis Plan

### Primary Analyses (pre-registered)

1. **DCI computation**: DCI = (Economic_weight + Semiotic_weight) / 100 at each step, per brand per model
2. **H1 test**: Repeated-measures ANOVA on DCI across 4 conditions (control, step 1, 2, 3). Linear contrast for monotonic trend. Effect size: eta-squared + 95% bootstrap CI (10,000 iterations).
3. **H2 test**: Two-way ANOVA: Step (3) x Dimension (Cultural, Temporal, Economic) on per-dimension weight. Interaction F-test + post-hoc Tukey HSD.
4. **H3 test**: Independent t-test on compounding rate (step 3 DCI minus control DCI) between strong-Ideological brands (Patagonia) and weak-Ideological brands (Erewhon, Tesla). Cohen's d + 95% CI.

### Secondary Analyses (pre-registered)

5. **Per-dimension trajectory**: Plot each dimension's mean weight across 4 conditions (8 trajectories). Identify which dimensions accelerate vs plateau.
6. **Model comparison**: Does the compounding rate differ by model? One-way ANOVA: Model (5) on compounding rate.
7. **Category effect**: Does the product category moderate compounding? One-way ANOVA: Category (5) on DCI at step 3.

### Exploratory Analyses (labeled as such)

8. **Step 1 brand retrieval overlap**: How often does each model include the focal brand in its Step 1 consideration set?
9. **Competitor selection effect**: Does the identity of the Step 1 competitor affect Step 2/3 profiles?
10. **Recommendation convergence**: Do all models recommend the same brand? Shannon entropy of recommendation distribution.

## Multiple Comparison Correction

- H1 pairwise comparisons (3 pairs): Bonferroni alpha = .017
- H2 post-hoc (3 dimension pairs): Tukey HSD
- Per-dimension tests (8 dimensions): Bonferroni alpha = .006
- Exploratory analyses: Benjamini-Hochberg FDR at .05

## Exclusion Criteria

- API errors: recorded with error field, excluded from analysis
- Unparseable JSON: recorded, excluded
- Weight sum outside 100 +/- 5: flagged, included after renormalization
- Step 1 responses that do not list 5 brands: recorded, pipeline continues with available brands
- Models with >50% error rate in any step: excluded from that step's analysis

## Reproducibility

- Random seed: 42
- All scripts committed before execution
- JSONL is append-only
- Full prompts stored in each record
- API metadata (tokens, response time, cost) per call
- Temperature: 0.7 for all models
- 3-second minimum delay between API calls
- Exponential backoff on 429: 5s, 10s, 20s, 60s

## JSONL Schema (extends 20-field base)

Standard fields: timestamp, experiment, model_id, model_provider, temperature, top_p, max_tokens, system_prompt, system_prompt_hash, user_prompt, user_prompt_hash, brand, condition, repetition, raw_response, parsed_weights, weights_valid, weight_sum_raw, response_time_ms, token_count_input, token_count_output, api_cost_usd

Experiment-specific fields:
- `step`: int (0=control, 1=retrieval, 2=comparison, 3=recommendation)
- `category`: str (luxury_fashion, home_furnishings, outdoor_gear, specialty_grocery, electric_vehicles)
- `step_1_brands`: list[str] (brands returned in Step 1, null for control)
- `step_1_raw`: str (raw Step 1 response, null for control/step 1)
- `competitor`: str (brand used in Step 2 comparison, null for control/step 1)
- `step_2_raw`: str (raw Step 2 response, null for control/step 1/step 2)
- `recommended_brand`: str (brand recommended in Step 3, null for non-step-3)
- `recommendation_reason`: str (reason text from Step 3, null for non-step-3)
- `dim_order`: list[str] (dimension ordering used for this call)

## Estimated Cost

~1,325 calls across 5 providers. Based on Run 15 per-call costs:
- Claude Haiku: ~$0.001/call -> ~$0.27
- GPT-4o-mini: ~$0.0003/call -> ~$0.08
- Gemini Flash: ~$0.0003/call -> ~$0.08
- DeepSeek V3: ~$0.0005/call -> ~$0.13
- Grok Fast: ~$0.004/call -> ~$1.06
- **Total estimated: ~$1.62** (well under $5 budget)

Note: Step 2 and Step 3 prompts include prior step context, increasing token counts. Actual cost may be 2-3x higher for those steps. Conservative estimate: ~$4.

---

*This protocol was committed before any API calls were made. Any analysis not listed above is labeled EXPLORATORY in the results.*
