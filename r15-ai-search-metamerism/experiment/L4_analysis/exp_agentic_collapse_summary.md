# Experiment A: Multi-Step Agentic Collapse -- Summary

**Date**: 2026-04-16
**Total records**: 425
**Valid weight records**: 276
**Total cost**: $0.36

## Step Counts

| Step | Records |
|------|---------|
| Control | 89 |
| Comparison | 98 |
| Recommendation | 89 |

## Hypothesis Results

### H1: Monotonic DCI Increase -- SUPPORTED

F = 4.298, p = 0.015, eta-sq = 0.031 (95% CI [0.237, 0.254])
Monotonic trend: True

**Step means (DCI)**:

| Step | Mean DCI |
|------|----------|
| step_0 | 0.231 |
| step_2 | 0.242 |
| step_3 | 0.262 |

**Pairwise comparisons (Bonferroni-corrected)**:

| Comparison | t | p | p_Bonf | Cohen's d | Sig |
|------------|---|---|--------|-----------|-----|
| step0_vs_step2 | -1.152 | 0.251 | 0.753 | 0.169 | No |
| step0_vs_step3 | -2.95 | 0.004 | 0.011 | 0.442 | Yes |
| step2_vs_step3 | -1.755 | 0.081 | 0.243 | 0.257 | No |

### H2: Dimension-Specific Compounding -- SUPPORTED

**Collapse rates (step 3 mean - control mean)**:

| Dimension | Collapse Rate |
|-----------|---------------|
| Cultural | -1.146 |
| Temporal | 0.596 |
| Economic | 1.393 |

Cultural collapsed more than Economic: True
Temporal collapsed more than Economic: True

### H3: Ideological Signal Protection -- SUPPORTED

t = 2.261, p = 0.029, Cohen's d = -0.696 (95% CI [0.014, 0.054])
Strong Ideological (Patagonia) mean compound rate: 0.065 (n=16)
Weak Ideological (Erewhon, Tesla) mean compound rate: 0.018 (n=31)

## Per-Dimension Trajectories

| Dimension | Control | Step 2 | Step 3 | Delta (S3-Ctrl) |
|-----------|---------|--------|--------|-----------------|
| Semiotic | 10.136 | 11.055 | 11.792 | 1.656 |
| Narrative | 12.972 | 11.368 | 10.666 | -2.306 |
| Ideological | 12.753 | 15.345 | 13.512 | 0.759 |
| Experiential | 16.887 | 15.374 | 16.548 | -0.339 |
| Social | 12.406 | 12.881 | 11.644 | -0.762 |
| Economic | 12.97 | 13.192 | 14.428 | 1.458 |
| Cultural | 12.87 | 12.081 | 11.784 | -1.086 |
| Temporal | 9.006 | 8.703 | 9.627 | 0.621 |

## Model Comparison

| Model | Mean Compound | Std | n |
|-------|--------------|-----|---|
| claude-haiku-4-5 | 0.043 | 0.09 | 14 |
| gpt-4o-mini | -0.015 | 0.049 | 13 |
| grok-4-1-fast-non-reasoning | 0.047 | 0.07 | 15 |
| deepseek-chat | 0.036 | 0.068 | 15 |
| gemini-2.5-flash | 0.033 | 0.061 | 25 |
| gemma4:latest | 0.063 | 0.131 | 6 |

Model ANOVA: F = 1.469, p = 0.209

## Exploratory: Retrieval Overlap

| Brand | Included in Step 1 | Total | Rate |
|-------|--------------------|-------|------|
| Hermes | 0 | 11 | 0.0 |
| IKEA | 5 | 14 | 0.357 |
| Patagonia | 9 | 12 | 0.75 |
| Erewhon | 0 | 12 | 0.0 |
| Tesla | 11 | 14 | 0.786 |

## Exploratory: Recommendation Convergence

Shannon entropy: 3.323 (max: 4.0)

| Recommended Brand | Count |
|-------------------|-------|
| IKEA | 18 |
| Tesla | 16 |
| Hermès | 12 |
| Arc'teryx | 10 |
| Erewhon | 9 |
| Patagonia | 8 |
| Vital Farms | 3 |
| Eataly | 2 |
| Chanel | 2 |
| Hermes | 2 |
| Hyundai | 2 |
| Volkswagen | 1 |
| Brunello Cucinelli | 1 |
| REI Co-op | 1 |
| Chevrolet | 1 |
| Fly by Jing | 1 |

---
*Analysis script: L4_analysis/exp_agentic_collapse_analysis.py*
*Protocol: L0_specification/EXP_AGENTIC_COLLAPSE_PROTOCOL.md*
