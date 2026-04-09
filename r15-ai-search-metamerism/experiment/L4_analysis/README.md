# L4 Analysis

Post-experiment analysis scripts and outputs for Run 5 (cross-cultural, completed 2026-04-06).

**Status**: Complete

---

## Contents

| File | Contents |
|------|----------|
| `run5_analysis.py` | Post-processing analysis script: diagonal advantage matrix, H5-H10 tests |
| `run5_analysis_results.json` | Full analysis outputs including H5-H10 test statistics |
| `run5_dci_table.csv` | DCI per model per culture (primary H5 matrix) |
| `run5_diagonal_advantage.csv` | Diagonal advantage scores: national model DCI vs cross-culture DCI |

Session logs (JSONL) are in `../L3_sessions/` (run2_global.jsonl through run5_crosscultural.jsonl).

---

## Analysis Plan Reference

See `../L0_specification/PRE_REGISTRATION_RUN5.md` Section 3 for the pre-registered analysis plan:
- Section 3.1: Primary analysis (H5) — diagonal advantage test
- Section 3.2: Diagonal advantage matrix (permutation test)
- Section 3.3: Backward compatibility check (Runs 2-4 vs Run 5)
- Section 3.4: Exploratory geopolitical analysis (H7)

---

## Model Exclusion Notes

- **T-Pro 2.0** (tpro_yandex, Yandex AI Studio): Requires dedicated paid instance ($6.20/hr). Not available in free-tier. Excluded from study.
- **GLM-4.7** (cerebras_glm): DCI listed as N/A in run5_summary.md — insufficient successful responses.
- **Falcon-H1-Arabic 7B** (falcon_arabic_local): DCI listed as N/A — insufficient successful responses.
- **Qwen3.5 27B** (qwen35_local): DCI listed as N/A — insufficient successful responses.
- Bonferroni correction applies to H5: alpha = 0.05 / 8 cultures = 0.00625.
