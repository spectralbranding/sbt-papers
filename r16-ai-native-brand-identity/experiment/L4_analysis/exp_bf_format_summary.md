# Experiment D: Brand Function Format Optimization -- Results Summary

**Total API calls**: 375
**Valid responses**: 355
**Total cost**: $0.13

## Hypothesis Verdicts

- **H1_structured_advantage**: NOT SUPPORTED
- **H2_prose_penalty**: SUPPORTED
- **H3_score_only_floor**: NOT SUPPORTED
- **H4_cross_model_consistency**: SUPPORTED
- **H5_dimension_specific**: NOT SUPPORTED

## Table 1: Cosine Similarity to Canonical Profile by Format

| Format | Mean Cosine | SD | n | 95% CI |
|--------|-------------|-----|---|--------|
| JSON Structured | 0.9837 | 0.0214 | 72 | [0.9784, 0.9883] |
| Prose Narrative | 0.9408 | 0.0444 | 73 | [0.9302, 0.9503] |
| Tabular Minimal | 0.9901 | 0.0224 | 68 | [0.9843, 0.9949] |
| Ranked List | 0.9849 | 0.0225 | 72 | [0.9796, 0.9898] |
| Score-Only Vector | 0.9982 | 0.0073 | 70 | [0.9962, 0.9994] |

## ANOVA: Format Effect on Cosine Similarity

- F(4, 350) = 51.188, p = 0.000000, eta-sq = 0.3691

## Table 2: Pairwise Comparisons (Bonferroni-corrected)

| Comparison | t | p | p_bonf | Cohen's d | Sig? |
|------------|---|---|--------|-----------|------|
| F1_json_vs_F2_prose | 7.408 | 0.000000 | 0.000000 | 1.230 | Yes |
| F1_json_vs_F3_tabular | -1.706 | 0.090167 | 0.901667 | -0.289 | No |
| F1_json_vs_F4_ranked | -0.309 | 0.757501 | 1.000000 | -0.052 | No |
| F1_json_vs_F5_vector | -5.353 | 0.000000 | 0.000003 | -0.899 | Yes |
| F2_prose_vs_F3_tabular | -8.230 | 0.000000 | 0.000000 | -1.387 | Yes |
| F2_prose_vs_F4_ranked | -7.529 | 0.000000 | 0.000000 | -1.251 | Yes |
| F2_prose_vs_F5_vector | -10.682 | 0.000000 | 0.000000 | -1.787 | Yes |
| F3_tabular_vs_F4_ranked | 1.366 | 0.174279 | 1.000000 | 0.231 | No |
| F3_tabular_vs_F5_vector | -2.883 | 0.004574 | 0.045740 | -0.491 | Yes |
| F4_ranked_vs_F5_vector | -4.715 | 0.000006 | 0.000058 | -0.791 | Yes |

## Table 3: Mean Cosine by Model x Format

| Model | JSON Structured | Prose Narrative | Tabular Minimal | Ranked List | Score-Only Vector |
|-------|--------|--------|--------|--------|--------|
| claude-haiku-4-5-20251001 | 0.9834 | 0.9479 | 0.9962 | 0.9799 | 1.0000 |
| gpt-4o-mini | 0.9650 | 0.8988 | 0.9692 | 0.9741 | 0.9998 |
| deepseek-chat | 0.9860 | 0.9499 | 0.9934 | 0.9827 | 0.9924 |
| grok-4-1-fast-non-reasoning | 0.9909 | 0.9629 | 0.9961 | 0.9918 | 0.9994 |
| gemini-2.5-flash | 0.9960 | 0.9449 | 1.0000 | 0.9986 | 0.9999 |

## Cross-Model Format Ranking Concordance

- Kendall's W = 0.8400 (strong)

## Table 4: Hard vs Soft Dimension MAE by Format

| Format | Hard MAE | Soft MAE | t | p | Soft worse? |
|--------|----------|----------|---|---|-------------|
| JSON Structured | 0.9144 | 0.8185 | 0.834 | 0.404844 | No |
| Prose Narrative | 2.1243 | 1.8343 | 1.850 | 0.064926 | No |
| Tabular Minimal | 0.4454 | 0.4773 | -0.289 | 0.772647 | Yes |
| Ranked List | 0.9437 | 0.7774 | 1.470 | 0.142196 | No |
| Score-Only Vector | 0.1524 | 0.1857 | -0.647 | 0.518029 | Yes |

## Table 5: Parse Success Rates by Format

| Format | Total | Valid | Rate |
|--------|-------|-------|------|
| JSON Structured | 75 | 72 | 96.0% |
| Prose Narrative | 75 | 73 | 97.3% |
| Tabular Minimal | 75 | 68 | 90.7% |
| Ranked List | 75 | 72 | 96.0% |
| Score-Only Vector | 75 | 70 | 93.3% |
