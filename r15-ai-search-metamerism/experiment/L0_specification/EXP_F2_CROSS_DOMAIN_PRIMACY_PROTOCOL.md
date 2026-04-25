# Experiment F2: Cross-Domain Primacy

**Protocol version**: 1.0
**Date**: 2026-04-17
**Status**: PRE-REGISTERED (frozen before data collection)
**Builds on**: Experiment E (Primacy Effect Generalization, EXP_PRIMACY_GENERALIZATION_PROTOCOL.md)
**Paper target**: R15 extension or PRISM instrument validity paper

---

## Background

Experiment E found a strong serial-position primacy effect in LLM brand perception elicitation: in JSON allocation format, dimensions listed first receive significantly higher weights than dimensions listed last (d = 1.39). In Likert format the effect was much smaller (d = .22). These results were obtained in a single domain: brand perception using the eight SBT dimensions.

The threat to LLM-as-respondent methodology is acute if the effect generalizes across domains. If primacy operates whenever an LLM produces ordered numerical judgments -- regardless of whether the subject matter is brands, political attitudes, product features, or anything else -- then the entire class of survey-via-LLM methods is affected, not just PRISM-B. Conversely, if primacy is domain-specific (i.e., an artifact of SBT dimension structure or brand-evaluation prompting conventions), the finding is informative but not catastrophic.

Exp E controlled for domain by keeping brand stimuli constant across all four response formats. This experiment holds response format constant at two levels (JSON, Likert) and crosses domain (brand / political) as a between-domain factor, using dimensionality-matched stimuli in both domains.

---

## Research Question

Does the serial position effect in LLM elicitation generalize beyond brand perception to political attitude measurement? If so, does the magnitude of primacy differ across domains?

---

## Design

2 (domain: brand, political) x 2 (response format: JSON, Likert) x 8 (dimension orderings) x 5 (stimuli per domain) x 5 (models) x 1 (repetition) = **800 calls**

### Factor 1: Domain (between-domain)

**Domain 1 -- Brand perception (PRISM-B)**
Uses the eight SBT dimensions and five canonical brand stimuli.

**Domain 2 -- Political attitudes (adapted MFT)**
Uses eight Moral Foundations Theory dimensions and five policy scenario stimuli.
The MFT domain was selected because:
- It has established eight-dimensional structure matching SBT dimensionality
- Policy scenarios activate dimensions differentially (not uniformly), mirroring brand variation
- It is maximally distinct from brand evaluation in subject matter

### Factor 2: Response Format (between-condition)

**JSON allocation**: Allocate 100 points across 8 dimensions.
**Likert 1-5**: Rate each dimension independently on 1-5 scale.

These two formats were chosen because Exp E found the largest primacy contrast between them (d_JSON = 1.39 vs d_Likert = .22). The ranking and NL formats are excluded from this experiment to keep call count tractable.

### Factor 3: Dimension Ordering (within-stimulus)

8 Latin-square cyclic orderings, one per trial. Assigned deterministically so each ordering appears once per (domain x format x stimulus x model) cell.

---

## Stimuli

### Brand Stimuli (PRISM-B, 5 brands)

Canonical profiles (SBT dimensions: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal):

- Hermes: [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]
- IKEA: [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]
- Patagonia: [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]
- Erewhon: [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5]
- Tesla: [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]

### Political Stimuli (MFT-adapted, 5 policy scenarios)

Scenarios are designed to differentially activate MFT dimensions, analogous to how canonical brands differentially activate SBT dimensions.

| ID | Scenario |
|----|----------|
| P1 | "Universal basic income: providing every citizen $1,000/month regardless of employment" |
| P2 | "Immigration policy: reducing visa processing time from 18 months to 3 months" |
| P3 | "Carbon tax: $50/ton on all fossil fuel emissions, revenue returned as dividend" |
| P4 | "Military spending: increasing defense budget by 15% with cuts to education" |
| P5 | "Social media: requiring platforms to remove harmful content within 24 hours" |

---

## Dimension Sets

### SBT Dimensions (Brand domain)

1. Semiotic
2. Narrative
3. Ideological
4. Experiential
5. Social
6. Economic
7. Cultural
8. Temporal

### MFT Dimensions (Political domain)

1. Care/Harm -- sensitivity to suffering
2. Fairness/Cheating -- proportionality and justice
3. Loyalty/Betrayal -- group solidarity
4. Authority/Subversion -- respect for hierarchy
5. Sanctity/Degradation -- purity concerns
6. Liberty/Oppression -- freedom from constraint
7. Efficiency/Waste -- resource optimization
8. Tradition/Progress -- preservation vs change

Eight dimensions in each domain. Ordering is manipulated identically across domains using the same Latin-square rotations.

---

## Models

Five models, one per provider family:

| Short name | Model ID | Provider |
|------------|----------|----------|
| claude | claude-haiku-4-5-20251001 | Anthropic |
| gpt | gpt-4o-mini | OpenAI |
| gemini | gemini-2.5-flash | Google |
| deepseek | deepseek-chat | DeepSeek |
| grok | grok-4-1-fast-non-reasoning | xAI |

---

## Prompts

### System Prompt (both domains)

```
You are a research assistant participating in a social science study. Answer honestly based on the information provided.
```

### Brand JSON Prompt

```
Consider the brand {brand}. Allocate 100 points across these 8 dimensions reflecting their importance to this brand:
{ordered_dims}
The weights must sum to 100. Respond in this exact JSON format:
{dim_json_template}
```

### Brand Likert Prompt

```
Consider the brand {brand}. Rate this brand on each of the following 8 dimensions using a scale of 1-5 (1 = not at all important to this brand, 5 = extremely important to this brand):
{ordered_dims}
Respond in this exact JSON format:
{dim_likert_template}
```

### Political JSON Prompt

```
Consider this policy: {scenario}. Allocate 100 points across these 8 moral dimensions reflecting their relevance to evaluating this policy:
{ordered_dims}
The weights must sum to 100. Respond in this exact JSON format:
{dim_json_template}
```

### Political Likert Prompt

```
Consider this policy: {scenario}. Rate the relevance of each of the following 8 dimensions to evaluating this policy using a scale of 1-5 (1 = not at all relevant, 5 = extremely relevant):
{ordered_dims}
Respond in this exact JSON format:
{dim_likert_template}
```

---

## Hypotheses

### H_F2a: Primacy in Political Domain (JSON)

Dimensions listed in positions 1-2 receive significantly higher weights than dimensions in positions 7-8 in the political domain, JSON format.
- **Test**: Independent t-test on mean weight at positions 1-2 vs 7-8 within (domain=political, format=JSON)
- **Alpha**: .05
- **Effect size**: Cohen's d + 95% bootstrap CI (10,000 iterations)
- **Success criterion**: p < .05 AND d >= .30

### H_F2b: Comparable Magnitude Across Domains

The primacy effect magnitude (mean pos 1-2 weight minus mean pos 7-8 weight) does not differ significantly between brand and political domains in JSON format.
- **Test**: Independent t-test on per-call primacy scores (brand JSON vs political JSON)
- **Alpha**: .05 (two-tailed)
- **Success criterion**: p >= .05 (non-significant difference = comparable magnitude)
- **Note**: Supported by absence of evidence, interpreted together with effect size overlap of CIs

### H_F2c: Likert Attenuates Primacy in Both Domains

The primacy effect is significantly smaller in Likert format than JSON format, within each domain.
- **Test**: Independent t-test on primacy magnitude (JSON vs Likert), separately for brand and political domains. Bonferroni alpha = .025 (2 tests).
- **Success criterion**: Both domains show significant attenuation at corrected alpha AND JSON primacy > Likert primacy in both

### H_F2d: Domain-General Finding

Primacy is significant (p < .05, d >= .30) in both domains in JSON format, establishing the effect as domain-general.
- **Test**: H_F2a for political + replication of Exp E H1 for brand domain using this experiment's data
- **Success criterion**: Both domain x JSON cells show significant primacy at alpha = .05

---

## Analysis Plan

### Primary Analyses (pre-registered)

1. **Per-cell primacy computation**: For each record, extract weights at positions 1-2 and 7-8. Compute per-call primacy score = mean(pos 1-2 weight) - mean(pos 7-8 weight).

2. **H_F2a**: t-test on primacy scores in (domain=political, format=JSON). Report d + 95% bootstrap CI.

3. **H_F2b**: Independent t-test comparing per-call primacy scores between (domain=brand, format=JSON) and (domain=political, format=JSON). Report d, CIs, and overlap.

4. **H_F2c**: Within-domain Likert attenuation tests. Brand: t-test on (brand, JSON) vs (brand, Likert) primacy scores. Political: t-test on (political, JSON) vs (political, Likert) primacy scores. Bonferroni correction.

5. **H_F2d**: Significance check for both domain x JSON cells. Report both p-values and effect sizes.

### Secondary Analyses (pre-registered)

6. **Domain x Format x Position three-way**: Mean weight by position (1-8), split by domain and format. Visual inspection of primacy curves. Linear trend test within each cell.

7. **Per-model primacy by domain**: Does the cross-domain generalization hold within each model? Report per-model primacy in (brand, JSON) and (political, JSON).

8. **Stimulus moderation**: Which policy scenarios / brands show the largest primacy effects? Report per-stimulus primacy magnitude.

9. **Cross-domain effect size comparison**: Plot d with 95% CI for all 4 domain x format cells. Are the CIs overlapping?

### Exploratory Analyses (labeled as such)

10. **Dimension-specific primacy**: Which specific dimensions are most vulnerable to position in each domain?

11. **Format x Domain interaction**: Formal 2x2 ANOVA on primacy magnitude with domain and format as factors. Is the interaction significant?

12. **Recency effects**: Is the position curve U-shaped (primacy + recency) or monotonically declining in either domain?

---

## Multiple Comparison Correction

- H_F2c per-domain tests (2): Bonferroni alpha = .025
- Per-model tests (5 models): Bonferroni alpha = .01
- Per-stimulus tests (10 stimuli): Bonferroni alpha = .005
- Exploratory analyses: Benjamini-Hochberg FDR at .05

---

## JSONL Schema

Standard required fields (EXPERIMENT_DATA_STANDARD.md):

| Field | Value |
|-------|-------|
| `timestamp` | ISO 8601 UTC |
| `model` | short name (claude, gpt, gemini, deepseek, grok) |
| `prompt_type` | `primacy_cross_domain` |
| `prompt` | full rendered user prompt |

Recommended fields:

| Field | Type | Description |
|-------|------|-------------|
| `model_id` | string | Provider model identifier |
| `response` | string | Raw model response |
| `parsed` | object/null | Parsed weight dict |
| `latency_ms` | number | API latency |
| `tokens_in` | integer | Input tokens |
| `tokens_out` | integer | Output tokens |
| `error` | string/null | Error message or null |
| `temperature` | number | Sampling temperature |

Experiment-specific fields:

| Field | Type | Description |
|-------|------|-------------|
| `domain` | string | `"brand"` or `"political"` |
| `stimulus` | string | Brand name or policy ID (P1-P5) |
| `response_format` | string | `"json"` or `"likert"` |
| `dimension_order` | list[str] | Dimension names in order used |
| `ordering_index` | int | 0-7, which Latin-square rotation |
| `dimension_set` | string | `"sbt"` or `"mft"` |
| `position_weights` | dict | Weight at each position 1-8 (derived) |
| `weights_valid` | bool | Whether parse succeeded |
| `weight_sum_raw` | float | Raw sum before normalization |

---

## Exclusion Criteria

- API errors: recorded with error field, excluded from weight analysis
- Unparseable JSON: excluded from weight analysis, count reported
- JSON weights: sum outside 100 +/- 5 flagged, included after renormalization
- Likert values outside 1-5: excluded
- Models with >50% error rate in any cell: excluded from that cell's analysis

---

## Reproducibility

- Random seed: 42
- All scripts committed before any API calls
- JSONL is append-only
- Full prompts stored in each record
- Temperature: .7 for all models
- 3-second minimum delay between calls
- Exponential backoff on rate limit: 5s, 10s, 20s, 60s, 120s

---

## Power Analysis

Based on Exp E results (d_JSON = 1.39, d_Likert = .22):

- For H_F2a (primacy in political, JSON): expected d >= .80 (assuming domain generalization). At alpha = .05, power = .80: n = 26 per cell. We have 8 orderings x 5 stimuli x 5 models = 200 observations per (domain, format) cell. Well powered.
- For H_F2b (domain comparison): smallest relevant difference d = .50. At alpha = .05, power = .80: n = 64 per group. We have 200 per domain x JSON cell. Adequate.
- For H_F2c (format attenuation): expected d >= .60. n = 44 per group required. We have 200 per cell. Adequate.

---

## Estimated Cost

800 calls across 5 models (160 per model):

| Model | Cost/call | Subtotal |
|-------|-----------|----------|
| claude (Haiku) | ~$0.001 | ~$0.16 |
| gpt (4o-mini) | ~$0.0003 | ~$0.05 |
| gemini (2.5 Flash) | ~$0.0003 | ~$0.05 |
| deepseek (chat) | ~$0.0005 | ~$0.08 |
| grok (fast) | ~$0.004 | ~$0.64 |

**Total estimated: ~$0.98. Conservative estimate with political prompts ~20% longer: ~$1.20.**

---

*This protocol was committed before any API calls were made. Any analysis not listed above is labeled EXPLORATORY in the results.*
