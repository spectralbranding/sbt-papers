# Experiment D: Brand Function Format Optimization -- Results Summary

**Total API calls**: 375
**Valid responses**: 366
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
| JSON Structured | 0.9726 | 0.0576 | 72 | [0.9580, 0.9841] |
| Prose Narrative | 0.9433 | 0.0388 | 72 | [0.9342, 0.9518] |
| Tabular Minimal | 0.9354 | 0.0261 | 74 | [0.9294, 0.9413] |
| Ranked List | 0.9542 | 0.0318 | 75 | [0.9470, 0.9613] |
| Score-Only Vector | 0.9769 | 0.0209 | 73 | [0.9720, 0.9815] |

## ANOVA: Format Effect on Cosine Similarity

- F(4, 361) = 17.189, p = 0.000000, eta-sq = 0.1600

## Table 2: Pairwise Comparisons (Bonferroni-corrected)

| Comparison | t | p | p_bonf | Cohen's d | Sig? |
|------------|---|---|--------|-----------|------|
| F1_json_vs_F2_prose | 3.581 | 0.000469 | 0.004693 | 0.597 | Yes |
| F1_json_vs_F3_tabular | 5.046 | 0.000001 | 0.000013 | 0.835 | Yes |
| F1_json_vs_F4_ranked | 2.404 | 0.017474 | 0.174736 | 0.397 | No |
| F1_json_vs_F5_vector | -0.606 | 0.545477 | 1.000000 | -0.101 | No |
| F2_prose_vs_F3_tabular | 1.439 | 0.152205 | 1.000000 | 0.238 | No |
| F2_prose_vs_F4_ranked | -1.874 | 0.062934 | 0.629344 | -0.309 | No |
| F2_prose_vs_F5_vector | -6.510 | 0.000000 | 0.000000 | -1.081 | Yes |
| F3_tabular_vs_F4_ranked | -3.943 | 0.000124 | 0.001243 | -0.646 | Yes |
| F3_tabular_vs_F5_vector | -10.631 | 0.000000 | 0.000000 | -1.754 | Yes |
| F4_ranked_vs_F5_vector | -5.112 | 0.000001 | 0.000010 | -0.841 | Yes |

## Table 3: Mean Cosine by Model x Format

| Model | JSON Structured | Prose Narrative | Tabular Minimal | Ranked List | Score-Only Vector |
|-------|--------|--------|--------|--------|--------|
| claude-haiku-4-5-20251001 | 0.9846 | 0.9504 | 0.9372 | 0.9658 | 0.9835 |
| gpt-4o-mini | 0.9559 | 0.9085 | 0.9241 | 0.9328 | 0.9593 |
| deepseek-chat | 0.9850 | 0.9516 | 0.9436 | 0.9616 | 0.9798 |
| grok-4-1-fast-non-reasoning | 0.9454 | 0.9630 | 0.9458 | 0.9374 | 0.9752 |
| gemini-2.5-flash | 0.9968 | 0.9426 | 0.9255 | 0.9734 | 0.9883 |

## Cross-Model Format Ranking Concordance

- Kendall's W = 0.6160 (moderate)

## Table 4: Hard vs Soft Dimension MAE by Format

| Format | Hard MAE | Soft MAE | t | p | Soft worse? |
|--------|----------|----------|---|---|-------------|
| JSON Structured | 1.0483 | 1.0555 | -0.037 | 0.970384 | Yes |
| Prose Narrative | 2.1401 | 1.7281 | 2.739 | 0.006423 | No |
| Tabular Minimal | 2.1105 | 2.2713 | -1.023 | 0.306845 | Yes |
| Ranked List | 2.4285 | 1.5989 | 4.833 | 0.000002 | No |
| Score-Only Vector | 1.2272 | 1.1101 | 1.104 | 0.270384 | No |

## Table 5: Parse Success Rates by Format

| Format | Total | Valid | Rate |
|--------|-------|-------|------|
| JSON Structured | 75 | 72 | 96.0% |
| Prose Narrative | 75 | 72 | 96.0% |
| Tabular Minimal | 75 | 74 | 98.7% |
| Ranked List | 75 | 75 | 100.0% |
| Score-Only Vector | 75 | 73 | 97.3% |
