# R16 Experiment: Behavioral Metamerism Pilot

## OST Specification Cascade

| Level | Directory | Contents | Status |
|-------|-----------|----------|--------|
| L0 | `L0_specification/` | Hypotheses, design, acceptance criteria | Ready |
| L1 | `L1_configuration/` | Model configs (7 models, 4 clusters) | Ready |
| L2 | `L2_prompts/` | Prompt templates + rendered prompts | Ready |
| L3 | `L3_sessions/` | Full request-response traces per model | Pending experiment |
| L4 | `L4_analysis/` | Analysis scripts + derived results | Pending experiment |

## LLM Audit Prompt

Point your LLM at this directory and use this prompt:

> You are auditing a research experiment. Read the files in this order:
>
> 1. `L0_specification/experiment.yaml` — understand what is being tested
> 2. `L0_specification/acceptance_criteria.yaml` — understand pass/fail thresholds
> 3. `L1_configuration/*.yaml` — verify model configurations
> 4. `L2_prompts/templates/*.yaml` — verify prompts match the specification
> 5. `L3_sessions/*/session_report.yaml` — review each model's execution summary
> 6. `L3_sessions/*/run_001.jsonl` (sample) — spot-check actual responses
> 7. `L4_analysis/results.json` — verify results match the paper's claims
>
> Report: Does the data support the paper's claims? Are there inconsistencies
> between L0 (spec) and L4 (results)? Are there anomalies in the session logs?

## Reproduction

```bash
# Demo mode (simulated data, no API keys)
uv run python ../behavioral_metamerism_pilot.py --demo

# Verify committed results
uv run python L4_analysis/analyze.py --verify

# Full live run (requires API keys via direnv)
uv run python ../behavioral_metamerism_pilot.py --live --runs 3
```
