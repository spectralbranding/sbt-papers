# Compounding x Format v2 — Constraint Framing Results

**Date**: 2026-04-17 (Session 106)
**Design**: 3 (condition: baseline/information/constraint) x 4 (stage) x 5 brands x 5 models x 2 reps
**Calls**: 600 total, 397/450 weight-bearing valid (88.2%)
**Cost**: $0.87

---

## Key Result: Constraint Framing Reduces Collapse by 42%

### Compounding Slopes

| Condition | Control DCI | Step 3 DCI | Delta | d | p |
|-----------|------------|------------|-------|---|---|
| Baseline | 3.935 | 4.770 | +.835 | .570 | .005 |
| Information | 4.342 | 4.539 | +.197 | .125 | .570 (ns) |
| Constraint | .635 | 2.766 | +2.131 | 1.230 | < .001 |

### Step 3 Pairwise Comparisons

| Comparison | DCI A | DCI B | d | p |
|-----------|-------|-------|---|---|
| Constraint vs Baseline | 2.766 | 4.770 | -.983 | < .001 |
| Constraint vs Information | 2.766 | 4.539 | -.883 | < .001 |
| Information vs Baseline | 4.539 | 4.770 | -.133 | .540 (ns) |

---

## Hypothesis Outcomes

**H_CF4 SUPPORTED**: DCI(step_3, constraint) = 2.766 < DCI(step_3, baseline) = 4.770 (d = -.983, p < .001). Constraint framing reduces final collapse by 42%.

**H_CF5 SUPPORTED**: DCI(step_3, constraint) = 2.766 < DCI(step_3, information) = 4.539 (d = -.883, p < .001). Constraint framing outperforms information framing.

**H_CF6 PARTIAL**: Constraint shows the largest absolute compounding (+2.131) but from the lowest base (.635). The final DCI (2.766) is still the lowest of all three conditions. The slope is steeper but the endpoint is lower — the constraint "wears off" across steps but never fully erodes.

---

## Per-Dimension Analysis at Step 3

| Dimension | Baseline | Information | Constraint | Uniform |
|-----------|----------|-------------|------------|---------|
| Semiotic | 13.5 | 12.6 | 12.3 | 12.5 |
| Narrative | 11.9 | 12.4 | 12.4 | 12.5 |
| Ideological | 12.6 | 10.8 | 13.7 | 12.5 |
| Experiential | 17.1 | 17.6 | 14.8 | 12.5 |
| Social | 11.8 | 11.3 | 12.3 | 12.5 |
| Economic | 12.2 | 15.2 | 11.8 | 12.5 |
| Cultural | 12.5 | 12.0 | 13.5 | 12.5 |
| Temporal | 8.8 | 8.2 | 9.4 | 12.5 |

**Constraint framing flattens the Experiential spike**: 17.1 (baseline) and 17.6 (information) drop to 14.8 under constraint. Economic inflation (15.2 under information) drops to 11.8. The constraint brings all dimensions closer to the 12.5 uniform baseline while Temporal remains the most resistant to correction (9.4 vs 12.5).

---

## The Two Mechanisms

1. **Information framing** (Brand Function scores): provides explicit dimensional targets. The model over-applies Experiential (+5.1 above baseline) and Economic (+2.7) while suppressing Ideological (-1.7) and Social (-1.2). The specification becomes a permission to concentrate.

2. **Constraint framing** ("distribute equally"): provides a behavioral directive without specific targets. The model achieves near-uniform allocation in single-step context (DCI .635) and partially maintains it across pipeline steps (DCI 2.766). The constraint acts as a structural anchor that erodes but never fails completely.

---

## Practical Implication

**For agentic pipeline design**: do not inject Brand Function specifications into multi-step shopping pipelines. Instead, inject a constraint directive: "evaluate across all eight dimensions equally." This reduces end-of-pipeline collapse by 42% relative to no intervention and by 39% relative to information-based specification.

**For specification strategy**: the single-step Brand Function (Run 4, Run 12) remains effective for direct queries. The constraint framing is the multi-step complement. A hybrid approach — Brand Function for single-step, constraint directive for multi-step — is the recommended configuration.

---

## Model Validity

| Model | Valid/Total | Rate |
|-------|------------|------|
| claude-haiku-4-5 | 75/90 | 83% |
| deepseek-chat | 85/90 | 94% |
| gemini-2.5-flash | 89/90 | 99% |
| gpt-4o-mini | 79/90 | 88% |
| grok-4-1-fast | 69/90 | 77% |

---

## Combined v1 + v2 Summary

| Finding | Effect | Evidence |
|---------|--------|----------|
| Information framing amplifies compounding | d = .820 (v1) | Specification paradox |
| Constraint framing reduces collapse | d = -.983 (v2) | 42% reduction at step_3 |
| Constraint outperforms information | d = -.883 (v2) | 39% lower DCI |
| Information = baseline at step_3 | d = -.133, ns (v2) | No benefit from scores in pipelines |
| Temporal dimension most resistant | All conditions | 8.2-9.4 vs 12.5 baseline |
| Total experiment calls | 1,080 | v1: 480, v2: 600 |
| Total cost | $1.47 | v1: $0.61, v2: $0.87 |
