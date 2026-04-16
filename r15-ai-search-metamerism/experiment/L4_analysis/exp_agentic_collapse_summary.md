# Experiment A: Multi-Step Agentic Collapse -- Summary

**Date**: 2026-04-16
**Total records**: 300
**Valid weight records**: 176
**Total cost**: $0.35

## Step Counts

| Step | Records |
|------|---------|
| Control | 59 |
| Comparison | 59 |
| Recommendation | 58 |

## Hypothesis Results

### H1: Monotonic DCI Increase -- NOT SUPPORTED

F = 3.025, p = 0.051, eta-sq = 0.034 (95% CI [0.24, 0.26])
Monotonic trend: True

**Step means (DCI)**:

| Step | Mean DCI |
|------|----------|
| step_0 | 0.238 |
| step_2 | 0.246 |
| step_3 | 0.267 |

**Pairwise comparisons (Bonferroni-corrected)**:

| Comparison | t | p | p_Bonf | Cohen's d | Sig |
|------------|---|---|--------|-----------|-----|
| step0_vs_step2 | -0.715 | 0.476 | 1.0 | 0.132 | No |
| step0_vs_step3 | -2.457 | 0.015 | 0.046 | 0.454 | Yes |
| step2_vs_step3 | -1.573 | 0.119 | 0.356 | 0.291 | No |

### H2: Dimension-Specific Compounding -- SUPPORTED

**Collapse rates (step 3 mean - control mean)**:

| Dimension | Collapse Rate |
|-----------|---------------|
| Cultural | -1.035 |
| Temporal | 0.064 |
| Economic | 0.925 |

Cultural collapsed more than Economic: True
Temporal collapsed more than Economic: True

### H3: Ideological Signal Protection -- SUPPORTED

t = 2.382, p = 0.024, Cohen's d = -0.88 (95% CI [0.003, 0.053])
Strong Ideological (Patagonia) mean compound rate: 0.066 (n=11)
Weak Ideological (Erewhon, Tesla) mean compound rate: 0.007 (n=22)

## Per-Dimension Trajectories

| Dimension | Control | Step 2 | Step 3 | Delta (S3-Ctrl) |
|-----------|---------|--------|--------|-----------------|
| Semiotic | 10.102 | 11.542 | 12.121 | 2.019 |
| Narrative | 13.0 | 11.441 | 10.966 | -2.034 |
| Ideological | 12.119 | 14.966 | 12.983 | 0.864 |
| Experiential | 17.39 | 15.746 | 16.586 | -0.804 |
| Social | 12.051 | 13.356 | 12.138 | 0.087 |
| Economic | 13.678 | 13.051 | 14.603 | 0.925 |
| Cultural | 12.949 | 12.051 | 11.914 | -1.035 |
| Temporal | 8.712 | 7.847 | 8.776 | 0.064 |

## Model Comparison

| Model | Mean Compound | Std | n |
|-------|--------------|-----|---|
| claude-haiku-4-5 | 0.043 | 0.09 | 14 |
| gpt-4o-mini | -0.014 | 0.051 | 13 |
| grok-4-1-fast-non-reasoning | 0.047 | 0.07 | 15 |
| deepseek-chat | 0.036 | 0.068 | 15 |

Model ANOVA: F = 2.097, p = 0.112

## Exploratory: Retrieval Overlap

| Brand | Included in Step 1 | Total | Rate |
|-------|--------------------|-------|------|
| Hermes | 0 | 11 | 0.0 |
| IKEA | 5 | 12 | 0.417 |
| Patagonia | 8 | 10 | 0.8 |
| Erewhon | 0 | 12 | 0.0 |
| Tesla | 10 | 12 | 0.833 |

## Exploratory: Recommendation Convergence

Shannon entropy: 3.423 (max: 3.907)

| Recommended Brand | Count |
|-------------------|-------|
| IKEA | 12 |
| Tesla | 9 |
| Arc'teryx | 7 |
| Hermès | 7 |
| Erewhon | 5 |
| Patagonia | 4 |
| Vital Farms | 3 |
| Eataly | 2 |
| Chanel | 2 |
| Hermes | 2 |
| Volkswagen | 1 |
| Brunello Cucinelli | 1 |
| REI Co-op | 1 |
| Chevrolet | 1 |
| Fly by Jing | 1 |

---
*Analysis script: L4_analysis/exp_agentic_collapse_analysis.py*
*Protocol: L0_specification/EXP_AGENTIC_COLLAPSE_PROTOCOL.md*
