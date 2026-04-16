# Experiment A: Multi-Step Agentic Collapse -- Summary

**Date**: 2026-04-16
**Total records**: 365
**Valid weight records**: 241
**Total cost**: $0.36

## Step Counts

| Step | Records |
|------|---------|
| Control | 74 |
| Comparison | 84 |
| Recommendation | 83 |

## Hypothesis Results

### H1: Monotonic DCI Increase -- SUPPORTED

F = 3.533, p = 0.031, eta-sq = 0.029 (95% CI [0.24, 0.258])
Monotonic trend: True

**Step means (DCI)**:

| Step | Mean DCI |
|------|----------|
| step_0 | 0.235 |
| step_2 | 0.245 |
| step_3 | 0.264 |

**Pairwise comparisons (Bonferroni-corrected)**:

| Comparison | t | p | p_Bonf | Cohen's d | Sig |
|------------|---|---|--------|-----------|-----|
| step0_vs_step2 | -0.972 | 0.333 | 0.998 | 0.155 | No |
| step0_vs_step3 | -2.669 | 0.008 | 0.025 | 0.427 | Yes |
| step2_vs_step3 | -1.611 | 0.109 | 0.327 | 0.249 | No |

### H2: Dimension-Specific Compounding -- SUPPORTED

**Collapse rates (step 3 mean - control mean)**:

| Dimension | Collapse Rate |
|-----------|---------------|
| Cultural | -0.776 |
| Temporal | 0.224 |
| Economic | 1.65 |

Cultural collapsed more than Economic: True
Temporal collapsed more than Economic: True

### H3: Ideological Signal Protection -- SUPPORTED

t = 2.656, p = 0.011, Cohen's d = -0.869 (95% CI [0.005, 0.045])
Strong Ideological (Patagonia) mean compound rate: 0.061 (n=14)
Weak Ideological (Erewhon, Tesla) mean compound rate: 0.006 (n=28)

## Per-Dimension Trajectories

| Dimension | Control | Step 2 | Step 3 | Delta (S3-Ctrl) |
|-----------|---------|--------|--------|-----------------|
| Semiotic | 10.27 | 11.19 | 11.566 | 1.296 |
| Narrative | 12.811 | 11.274 | 10.699 | -2.112 |
| Ideological | 12.581 | 15.262 | 13.711 | 1.13 |
| Experiential | 17.297 | 15.56 | 16.301 | -0.996 |
| Social | 12.054 | 12.798 | 11.699 | -0.355 |
| Economic | 13.23 | 13.321 | 14.88 | 1.65 |
| Cultural | 12.824 | 12.238 | 12.048 | -0.776 |
| Temporal | 8.932 | 8.357 | 9.157 | 0.225 |

## Model Comparison

| Model | Mean Compound | Std | n |
|-------|--------------|-----|---|
| claude-haiku-4-5 | 0.043 | 0.09 | 14 |
| gpt-4o-mini | -0.014 | 0.051 | 13 |
| grok-4-1-fast-non-reasoning | 0.047 | 0.07 | 15 |
| deepseek-chat | 0.036 | 0.068 | 15 |
| gemini-2.5-flash | 0.033 | 0.061 | 25 |

Model ANOVA: F = 1.729, p = 0.152

## Exploratory: Retrieval Overlap

| Brand | Included in Step 1 | Total | Rate |
|-------|--------------------|-------|------|
| Hermes | 0 | 11 | 0.0 |
| IKEA | 5 | 12 | 0.417 |
| Patagonia | 8 | 10 | 0.8 |
| Erewhon | 0 | 12 | 0.0 |
| Tesla | 10 | 12 | 0.833 |

## Exploratory: Recommendation Convergence

Shannon entropy: 3.357 (max: 4.0)

| Recommended Brand | Count |
|-------------------|-------|
| IKEA | 18 |
| Tesla | 13 |
| Hermès | 11 |
| Erewhon | 9 |
| Arc'teryx | 8 |
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
