# PRISM-O campaign code (2026bd)

Campaign implementation for the PRISM-O optimization-depth instrument. All
protocol constants are frozen upstream: PL0 `../PREREGISTRATION.md` (v1.1),
rubric `../RUBRIC.md`, PL1 `../PL1_CONFIG.yaml`, PL2 bank
`../PL2_VIGNETTE_BANK.yaml`, panel `../PANEL_MANIFEST.yaml` +
`../data/panel_pinned_manifest.json` (SHA-256-pinned artifacts).

Pipeline (run order; keys injected via `bws run --`; long runs sandbox-off):

| Step | Command | Output |
|---|---|---|
| Stage-1 run (version check → concordance screen → bank) | `bws run -- research/prism_o/code/run_campaign.sh stage1` | `../data/stage1_records.jsonl`, `version_check_stage1.json`, `concordance_screen_stage1.json` |
| Stage-1 scoring (H1(i) gate) | `run_campaign.sh score1` | `../data/pl4_stage1_results.json`, `STAGE1_REPORT.md` |
| Stage-2 cost table (fires nothing) | `uv run python research/prism_o/code/estimate_stage2.py` | `../data/stage2_cost_estimate.json` |
| Panel collection (EDGAR; no model calls) | `run_campaign.sh collect` | `../panel/`, `../data/panel_pinned_manifest.json` |
| Stage-2 campaign (sharded per pair) | `bws run -- run_campaign.sh stage2 --ops OP1 --suffix _op1 --skip-version-check` (×4; run the version check once first) | `../data/stage2_records_op*.jsonl` |
| PL4 estimator (seed 20260703) | `run_campaign.sh estimate2` | `../data/pl4_stage2_results.json` |

Design notes:
- Two roles per operator pair, families disjoint (2026ap): SEGMENTER lists
  interventions (verbatim spans), CLASSIFIER codes each span on the D4–D1
  ladder under the verbatim rubric. `MAX_IV_PER_ARTIFACT = 8` is a frozen
  implementation constant (overflow logged).
- Every call is PL3-logged (append-only JSONL, format v1.2) via
  `prism_core.llm_call_logger`; budget caps are enforced per stage from the
  logged usage (Stage 1 $10; Stage 2 $193, user-approved).
- Verification equipment before any substantive call: live-catalog version
  check of every pinned model id + the mechanical 3×-median concordance
  screen (`prism_core.concordance`).
- Stage-1 scoring hygiene: bank bases B01–B12 are the rubric's worked
  examples (in-prompt); the gate requires macro accuracy ≥ .80 on the FULL
  bank AND on the 14 held-out bases, per pair.
- H3 instantiation (leave-one-out, non-circular): every pair's gap within
  2× floor of the mean of the other pairs' gaps; see `estimator_stage2.py`
  docstring.
- Reproducibility: fixed seeds (20260703) for bootstrap/permutation;
  deterministic panel selection rule; pinned artifact hashes; logger records
  carry model version, prompt SHA-256, and token usage.
