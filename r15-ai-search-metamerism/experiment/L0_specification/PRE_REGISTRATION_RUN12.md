# Run 12 Pre-Registration: Brand Function Specification Test

**Date**: 2026-04-14
**Registered by**: Dmitry Zharnikov
**Status**: Pre-registered (experiment not yet executed)

## Hypothesis

**H_BF (Brand Function Reduces Collapse)**: Providing a Brand Function JSON specification in the LLM prompt context reduces the Dimensional Collapse Index (DCI) compared to the unspecified baseline.

Formally: DCI(with_spec) < DCI(without_spec) for each brand, with paired t-test across the model panel.

## Secondary hypotheses

**H_BF_dim**: The dimensions that benefit most from specification are those that collapse most without it (Cultural, Temporal, Ideological — the "soft" dimensions identified in R15 H1).

**H_BF_convergence**: Cross-model agreement (cosine similarity) increases when specification is provided, because models are reading the same structured data rather than inferring from heterogeneous training corpora.

## Design

**Condition 1 (Baseline)**: Standard R15 weighted_recommendation prompt. No Brand Function provided. The model perceives the brand from training data alone. Baseline data already exists from R15 Runs 2-4 (global brands).

**Condition 2 (Specified)**: Same R15 weighted_recommendation prompt, prefixed with the Brand Function JSON for the focal brand. The model has structured dimensional data available before answering.

**Brands**: The 5 canonical SBT brands (Hermes, IKEA, Patagonia, Erewhon, Tesla). These have the most complete existing baseline data from R15 Runs 2-4.

**Brand pairs**: Each brand paired against the same comparator used in R15 Runs 2-4:
- Hermes vs Louis Vuitton
- IKEA vs West Elm
- Patagonia vs The North Face
- Erewhon vs Whole Foods Market
- Tesla vs Rivian

**Model panel**: Cloud models only (Ollama may be occupied by parallel experiments).
1. claude (Claude Sonnet 4.6, Anthropic, Western, paid)
2. gpt (GPT-4o-mini, OpenAI, Western, paid)
3. gemini (Gemini 2.5 Flash, Google, Western, paid)
4. deepseek (DeepSeek V3, DeepSeek, Chinese, paid)

Optional extension (when Ollama is available):
5. qwen3_local (Qwen3 30B, local)
6. gemma4_local (Gemma 4 27B, local)

**Runs**: 3 per condition per brand per model.

**Volume**: 5 brands x 4 models x 2 conditions x 3 runs = 120 calls (cloud only). With local: 180 calls.

**Cost**: ~$0.10-0.20 (weighted_rec_only, short prompts).

## Brand Function Specifications

Stored at: `L1_configuration/brand_functions/`

Each Brand Function is a JSON file containing the 8-dimensional specification for one brand, derived from the canonical SBT brand profiles (Zharnikov, 2026a) and the illustrative analyses in Articles 01-10.

The specification content is NOT invented for this experiment. It is extracted from existing published materials. This ensures the experiment tests whether providing existing brand knowledge in structured format reduces collapse — not whether adding new information helps.

## Analysis plan

1. Compute DCI for each (brand, model, condition) triple.
2. Paired t-test: DCI(baseline) vs DCI(specified) across the model panel, per brand.
3. Per-dimension analysis: which dimensions show the largest weight shift toward baseline (12.5) when spec is provided?
4. Cross-model cosine similarity: baseline vs specified conditions.
5. Effect size: Cohen's d for the DCI reduction.

## Output files

- `L3_sessions/run12_brand_function.jsonl` — raw session log
- `L4_analysis/run12_brand_function_results.json` — aggregated results
- `L4_analysis/run12_brand_function_summary.md` — human-readable report

## Reporting standards

Per `research/PAPER_QUALITY_STANDARDS.md`:
- No leading zeros for values < 1
- Exact p-values to 3 digits
- Effect sizes mandatory alongside every test
- AMA reference style
