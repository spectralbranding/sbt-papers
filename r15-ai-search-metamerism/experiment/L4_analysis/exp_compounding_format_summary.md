# Compounding x Format Experiment — Summary

**Date**: 2026-04-17 (Session 106)
**Design**: 2 (bf_condition: baseline/specified) x 4 (stage: control/step_1/step_2/step_3) x 5 brands x 6 models x 2 reps
**Calls**: 480 total, 291/360 weight-bearing valid (80.8%)
**Cost**: $0.61

---

## Key Result: Specification AMPLIFIES Compounding

**Hypothesis**: Brand Function specification at each pipeline step attenuates DCI compounding (the Exp A finding).

**Result**: REVERSED. Specification significantly increases compounding.

| Condition | Control DCI | Step 3 DCI | Delta | d | p |
|-----------|------------|------------|-------|---|---|
| Baseline | 4.135 | 4.409 | +.274 | .221 | .275 |
| Specified | 4.099 | 5.394 | +1.295 | .820 | < .001 |

**Interaction**: Specification amplifies compounding by +1.021 DCI points (specified delta - baseline delta).

**Direct comparison at Step 3**: Specified DCI (5.394) > Baseline DCI (4.409), d = .599, p = .004.

---

## Per-Dimension Analysis at Step 3

| Dimension | Baseline | Specified | Delta | Uniform |
|-----------|----------|-----------|-------|---------|
| Semiotic | 12.4 | 13.0 | +.6 | 12.5 |
| Narrative | 13.0 | 12.5 | -.6 | 12.5 |
| Ideological | 13.2 | 10.5 | -2.7 | 12.5 |
| Experiential | 15.0 | 18.7 | +3.7 | 12.5 |
| Social | 12.9 | 10.9 | -2.0 | 12.5 |
| Economic | 13.6 | 15.1 | +1.5 | 12.5 |
| Cultural | 11.6 | 11.7 | +.1 | 12.5 |
| Temporal | 8.5 | 8.3 | -.2 | 12.5 |

**Experiential inflation** (+3.7) dominates the specification effect. Ideological (-2.7) and Social (-2.0) suppress.

---

## Interpretation

The Brand Function specification does not anchor identity across pipeline steps. Instead, it provides the model with explicit dimensional targets that compound: the model over-applies the specification's Experiential weight at each step, creating amplified rather than attenuated collapse.

This suggests a **specification paradox**: making dimensional identity explicit to an agentic pipeline makes the pipeline MORE likely to distort it, not less. The pipeline treats the specification as evidence that the Experiential dimension is the salient one (because it can verify Experiential claims against training data), and progressively inflates it.

**Implication**: The Brand Function specification works in single-step contexts (Run 4, Run 12: DCI reduction toward baseline) but FAILS in multi-step agentic pipelines. The fix requires a different mechanism — possibly injecting the specification at each step as a constraint ("distribute weight equally") rather than as information ("here are the dimensional scores").

---

## Model Validity

| Model | Valid/Total | Rate |
|-------|------------|------|
| claude-haiku-4-5 | 59/60 | 98% |
| deepseek-chat | 60/60 | 100% |
| gemini-2.5-flash | 60/60 | 100% |
| gemma4:latest | 0/60 | 0% |
| gpt-4o-mini | 58/60 | 97% |
| grok-4-1-fast | 54/60 | 90% |

Gemma 4 (local Ollama) failed all weight parsing — excluded from analysis. Effective N = 5 cloud models.

---

## Limitations

1. Gemma 4 exclusion reduces the model diversity (no local model in final analysis)
2. Two repetitions per cell — low power for per-brand comparisons
3. The specification was injected as system prompt information; alternative injection methods (constraint framing, per-step reminders) were not tested
4. The amplification mechanism needs replication with a larger model panel
