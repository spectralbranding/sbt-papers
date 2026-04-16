# Experiment D: Brand Function Format Optimization -- Results Summary

**Total API calls**: 375
**Valid responses**: 375
**Total cost**: $0.14

## Hypothesis Verdicts

- **H1_structured_advantage**: NOT SUPPORTED
- **H2_prose_penalty**: SUPPORTED
- **H3_score_only_floor**: NOT SUPPORTED
- **H4_cross_model_consistency**: NOT SUPPORTED
- **H5_dimension_specific**: NOT SUPPORTED

## Table 1: Cosine Similarity to Canonical Profile by Format

| Format | Mean Cosine | SD | n | 95% CI |
|--------|-------------|-----|---|--------|
| JSON Structured | 0.9734 | 0.0566 | 75 | [0.9592, 0.9845] |
| Prose Narrative | 0.9440 | 0.0383 | 75 | [0.9350, 0.9524] |
| Tabular Minimal | 0.9351 | 0.0261 | 75 | [0.9290, 0.9410] |
| Ranked List | 0.9542 | 0.0318 | 75 | [0.9470, 0.9613] |
| Score-Only Vector | 0.9775 | 0.0209 | 75 | [0.9726, 0.9818] |

## ANOVA: Format Effect on Cosine Similarity

- F(4, 370) = 18.516, p = 0.000000, eta-sq = 0.1668

## Table 2: Pairwise Comparisons (Bonferroni-corrected)

| Comparison | t | p | p_bonf | Cohen's d | Sig? |
|------------|---|---|--------|-----------|------|
| F1_json_vs_F2_prose | 3.722 | 0.000280 | 0.002802 | 0.608 | Yes |
| F1_json_vs_F3_tabular | 5.324 | 0.000000 | 0.000004 | 0.869 | Yes |
| F1_json_vs_F4_ranked | 2.560 | 0.011473 | 0.114735 | 0.418 | No |
| F1_json_vs_F5_vector | -0.583 | 0.561081 | 1.000000 | -0.095 | No |
| F2_prose_vs_F3_tabular | 1.669 | 0.097172 | 0.971725 | 0.273 | No |
| F2_prose_vs_F4_ranked | -1.769 | 0.078927 | 0.789269 | -0.289 | No |
| F2_prose_vs_F5_vector | -6.634 | 0.000000 | 0.000000 | -1.083 | Yes |
| F3_tabular_vs_F4_ranked | -4.021 | 0.000092 | 0.000919 | -0.657 | Yes |
| F3_tabular_vs_F5_vector | -10.982 | 0.000000 | 0.000000 | -1.793 | Yes |
| F4_ranked_vs_F5_vector | -5.287 | 0.000000 | 0.000004 | -0.863 | Yes |

## Table 3: Mean Cosine by Model x Format

| Model | JSON Structured | Prose Narrative | Tabular Minimal | Ranked List | Score-Only Vector |
|-------|--------|--------|--------|--------|--------|
| claude-haiku-4-5-20251001 | 0.9846 | 0.9504 | 0.9372 | 0.9658 | 0.9835 |
| gpt-4o-mini | 0.9559 | 0.9085 | 0.9241 | 0.9328 | 0.9593 |
| gemini-2.5-flash | 0.9961 | 0.9466 | 0.9248 | 0.9734 | 0.9895 |
| deepseek-chat | 0.9850 | 0.9516 | 0.9436 | 0.9616 | 0.9798 |
| grok-4-1-fast-non-reasoning | 0.9454 | 0.9630 | 0.9458 | 0.9374 | 0.9752 |

## Cross-Model Format Ranking Concordance

- Kendall's W = 0.6160 (moderate)

## Table 4: Hard vs Soft Dimension MAE by Format

| Format | Hard MAE | Soft MAE | t | p | Soft worse? |
|--------|----------|----------|---|---|-------------|
| JSON Structured | 1.0148 | 1.0365 | -0.116 | 0.907633 | Yes |
| Prose Narrative | 2.1342 | 1.7411 | 2.678 | 0.007684 | No |
| Tabular Minimal | 2.1321 | 2.2660 | -0.856 | 0.392422 | Yes |
| Ranked List | 2.4285 | 1.5989 | 4.833 | 0.000002 | No |
| Score-Only Vector | 1.2094 | 1.0905 | 1.144 | 0.253283 | No |

## Table 5: Parse Success Rates by Format

| Format | Total | Valid | Rate |
|--------|-------|-------|------|
| JSON Structured | 75 | 75 | 100.0% |
| Prose Narrative | 75 | 75 | 100.0% |
| Tabular Minimal | 75 | 75 | 100.0% |
| Ranked List | 75 | 75 | 100.0% |
| Score-Only Vector | 75 | 75 | 100.0% |
