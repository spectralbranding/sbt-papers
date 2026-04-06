# Pre-Registration Protocol: Brand Function Resolution Test (Run 4)

> **NOTE on hypothesis numbering**: This protocol uses H5-H7 for internal naming
> of Run 4 resolution hypotheses. In the consolidated paper these are renumbered
> as H4a-H4c (extensions of the Run 4 specification resolution test). The primary
> hypothesis numbering H5-H10 in `PRE_REGISTRATION_RUN5.md` takes precedence for
> the Run 5 cross-cultural study. There is no conflict: H5-H7 here are Run 4-scoped
> placeholders; H5-H10 in Run 5 are the authoritative paper hypotheses.

**Study**: R15 Extension — Does Brand Function Specification Resolve Dimensional Collapse for Local Brands?
**Paper**: Zharnikov (2026v), Spectral Metamerism in AI-Mediated Brand Perception
**Date registered**: 2026-04-04 (before data collection)
**Status**: Pre-registered. No data collected at time of writing.

---

## Motivation

Runs 2-3 of the R15 experiment established that:
- LLMs systematically over-weight Economic and Semiotic dimensions (H1 SUPPORTED)
- The collapse pattern is structural across 6 model families (H2 SUPPORTED, cosine = 0.975)
- Local brands from underrepresented markets collapse significantly more than global brands (t = 6.483, p < 0.0001, Cohen's d = 0.878)
- The Economic dimension inflates to 168% of baseline for local brands vs 114% for global brands

The companion R16 study demonstrated that Brand Function specifications resolve behavioral metamerism for synthetic brands (100% discrimination, Fisher p = 0.0009).

**The gap**: Does Brand Function specification also resolve *dimensional collapse* for real local brands? This is a stronger test than R16 because:
1. These are real brands with real (thin) training data, not synthetic constructs
2. We measure dimensional weight distribution, not binary discrimination
3. The baseline collapse (DCI = 0.355) is established from Run 3 data

## Research Question

When a Brand Function specification is provided alongside standard prompt context, does the dimensional weight distribution for local brands shift toward the uniform baseline (DCI closer to 0.250)?

## Hypotheses

**H5 (specification resolution)**: The mean DCI for local brand pairs in the specification-augmented condition will be significantly lower than in the unaugmented condition (Run 3 baseline = 0.355).
- Test: paired t-test on per-model DCI means, spec vs no-spec
- Significance threshold: p < 0.05

**H6 (Cultural/Temporal recovery)**: The Cultural and Temporal dimension weights in the specification-augmented condition will be significantly higher than in the unaugmented condition, approaching the 12.5 baseline.
- Test: paired t-test on Cultural weight (baseline from Run 3: 7.9) and Temporal weight (baseline: 9.3)
- Significance threshold: p < 0.05 for each

**H7 (Economic normalization)**: The Economic dimension weight in the specification-augmented condition will be significantly lower than in the unaugmented condition (baseline: 21.0), approaching the 12.5 uniform baseline.
- Test: paired t-test on Economic weight
- Significance threshold: p < 0.05

## Design

- **Brand pairs**: Same 5 local brand pairs as Run 3 (AlphaMega/Carrefour, Laima/Lindt, Tusker/Heineken, Vinamilk/Danone, Knjaz Milos/Evian)
- **Models**: Same 6 models as Runs 2-3 (Claude Haiku 3.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Qwen3 30B, Gemma 4 27B)
- **Prompt**: Weighted recommendation (identical structure to Runs 2-3) with Brand Function JSON specification prepended for both brands in each pair
- **Runs**: 3 repetitions per model per pair (same as Runs 2-3)
- **Temperature**: 0.7 (same as Runs 2-3)
- **Total calls**: 5 pairs x 6 models x 3 runs = 90

## Brand Function Specifications

Specifications were created from publicly available information for each local brand. Each specification includes all 8 SBT dimensions with factual content about the brand's visual identity, origin story, values, customer experience, community role, pricing, cultural positioning, and heritage. Global competitor brands (Carrefour, Lindt, Heineken, Danone, Evian) receive NO specification — they serve as the "rich training data" baseline.

This design is deliberate: the specification fills the information gap for the local brand, testing whether the gap is the mechanism of collapse.

Provenance notes (verified vs inferred claims) are included in the specification file but stripped before prompt injection.

## Analysis Plan

**Primary analysis**: Compare DCI (Economic + Semiotic weight / 100) between Run 3 (no spec) and Run 4 (with spec) using paired t-test on per-model means.

**Secondary analysis**: Per-dimension weight comparison (8 paired t-tests with Bonferroni correction, alpha = 0.05/8 = 0.00625).

**Exploratory**: Per-pair resolution magnitude (which local brand benefits most from specification?), per-model resolution (do local models resolve differently from cloud models?).

## Stopping Rule

- Complete all 90 calls
- If H5 p > 0.10 after 3 runs: extend to 5 runs (additional 60 calls)
- If H5 p > 0.10 after 5 runs: report null result

## Exclusion Criteria

- Same as Runs 2-3: weights that do not sum to 85-115 are flagged and renormalized
- Models with >50% parse failure rate excluded from aggregate statistics
- All calls logged in JSONL with full prompt and response

## Expected Outcome

If the Brand Function resolves dimensional collapse:
- DCI should drop from 0.355 toward 0.250 (baseline)
- Cultural and Temporal weights should increase toward 12.5
- Economic weight should decrease from 21.0 toward 12.5
- The resolution effect should be consistent across models (similar to H2 convergence)

If the Brand Function does NOT resolve collapse:
- This would suggest that dimensional collapse in weight allocation is not driven by information availability alone — it may be a structural property of how LLMs process multi-dimensional comparisons regardless of available information
- This would be a theoretically important null result

## Relationship to R16

R16 tested specification resolution for *discrimination* (can the model tell brands apart?). This test examines specification resolution for *dimensional weighting* (does the model use all dimensions?). Both positive results together would establish that Brand Function specification affects both the binary question (who is this?) and the structural question (what makes them different?).
