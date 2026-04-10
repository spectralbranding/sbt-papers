# Run 10 — Corrective Comparators Results

**Generated:** 2026-04-10T17:47:28.402070+00:00

## Design

Three focal brands × two comparator conditions × 7 models × 3 runs.
Tests whether changing the comparator produces a different dimensional
weight profile for the same focal brand.

## Cross-model mean DCI by pair

| Focal brand | Comparator | DCI (mean across models) | Δ vs control |
|---|---|---|---|
| VkusVill | vkusvill_vs_whole_foods (control) | 28.904 | — |
| VkusVill | vkusvill_vs_trader_joes (corrective) | 36.286 | +7.382 |
| Calbee | calbee_vs_frito_lay (control) | 38.334 | — |
| Calbee | calbee_vs_koikeya (corrective) | 39.047 | +0.713 |
| Roshen | roshen_vs_cadbury (control) | 36.334 | — |
| Roshen | roshen_vs_hershey (corrective) | 36.762 | +0.428 |

## Per-dimension delta (corrective − control)

Positive values mean the corrective comparator preserves *more* of that
dimension; negative values mean it preserves less.

| Focal brand | Cultural | Temporal | Narrative | Ideological | Experiential | Social |
|---|---|---|---|---|---|---|
| VkusVill | -0.667 | -0.857 | -0.761 | -5.952 | +0.714 | -0.095 |
| Calbee | -1.095 | +0.857 | -0.238 | -0.952 | +1.285 | -0.571 |
| Roshen | +0.095 | -0.524 | +0.905 | -0.096 | -0.953 | +0.619 |

## Per-model breakdown

See `run10_corrective_results.json` for per-model dimensional weights
for every pair-model cell.

## Verdicts

- **VkusVill**: Comparator-sensitive. ΔDCI = +7.4 when paired with Trader Joe's vs Whole Foods. The corrective comparator (Trader Joe's, US organic-grocery analogue) produces measurably higher collapse, suggesting VkusVill's dimensional profile is partially driven by which Western reference brand anchors the comparison. Largest effect in the experiment.
- **Calbee**: Comparator-robust. ΔDCI = +0.7 when paired with Koikeya vs Frito-Lay. Switching to a same-culture Japanese snack comparator produces negligible change in collapse depth. Collapse appears intrinsic to Calbee in LLM training data, not driven by the comparator choice.
- **Roshen**: Comparator-robust. ΔDCI = +0.4 when paired with Hershey's vs Cadbury. Negligible comparator effect; collapse is structurally similar regardless of whether the Western comparator is British (Cadbury) or American (Hershey's).
