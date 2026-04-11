# L3 Sessions

JSONL session logs for all R15 experiment runs. Each file contains one JSON object per
API call with prompt, raw response, parsed output, model ID, latency, and error codes.

## Contents

| File | Run | Calls | Description |
|------|-----|-------|-------------|
| `run2_global.jsonl` | Run 2 | 3,240 | 10 global brand pairs, 6 models, 3 repetitions each |
| `run2_qwen_plus.jsonl` | Run 2 supplement | varies | Qwen Plus (DashScope) backfill for 10 global pairs |
| `run3_local.jsonl` | Run 3 | 1,620 | 5 local brand pairs (Cyprus, Latvia, Kenya, Vietnam, Serbia), 6 models |
| `run3_qwen_plus.jsonl` | Run 3 supplement | varies | Qwen Plus backfill for 5 local pairs |
| `run4_resolution.jsonl` | Run 4 | 90 | Brand Function resolution test, 5 local pairs with behavioral specs |
| `run5_crosscultural.jsonl` | Run 5 | 11,410 total (7,999 successful) | 7 cross-cultural pairs, 22 active models, 7 training traditions, 69 native-language calls (14MB) |
| `run5_fireworks_glm.jsonl` | Run 5 supplement | varies | GLM-4.7 (Zhipu, Fireworks API) backfill |
| `run5_gptoss_swallow.jsonl` | Run 5 supplement | 435 | GPT-OSS Swallow 20B (Japanese) backfill |
| `run6_banking_clean.jsonl` | Run 6 | 1,018 | Banking pair (Tinkoff vs PrivatBank), 24 models; H6 test |
| `run7_framing.jsonl` | Run 7 | varies | Geopolitical framing experiment; H12 test (3 pairs × 2 city contexts) |
| `run7d_swedish.jsonl` | Run 7 sub-run | varies | Swedish sub-run for the framing experiment |
| `run8_native_expansion.jsonl` | Run 8 | 815 | Native language expansion, 11 languages; H10 test (NOT SUPPORTED) |
| `run9_temp_0.0.jsonl` | Run 9 | varies | Temperature=0.0 condition |
| `run9_temp_0.3.jsonl` | Run 9 | varies | Temperature=0.3 condition |
| `run9_temp_1.0.jsonl` | Run 9 | varies | Temperature=1.0 condition; DCI spread=0.012 (robust) |
| `run10_corrective.jsonl` | Run 10 (supplementary) | 126 | Corrective comparators: 3 focal brands × 2 conditions × 7 models × 3 runs (2026-04-10) |
| `metadata.yaml` | -- | -- | Session metadata: package versions, API key hashes, hardware info, run index |

## Notes

**Run 5**: 70.1% success rate (7,999 of 11,410 calls). T-Pro 2.0 excluded (0 responses). GLM-4.7, Falcon-H1-Arabic 7B, Qwen3.5 27B show N/A DCI (insufficient responses). 69 native-language calls for H10.

**Run 10 (supplementary)**: Tests whether comparator choice drives dimensional collapse. VkusVill is comparator-sensitive (ΔDCI=+7.4 with Trader Joe's vs Whole Foods); Calbee and Roshen are comparator-robust (ΔDCI<1.0). Does not alter the headline 9-run results (21,601 calls). Results in `../L4_analysis/run10_corrective_results.json`.

## Data Format

Each JSONL record contains:
```
{
  "model": "<model_name>",
  "prompt_type": "weighted_recommendation|dimensional_differentiation|dimension_probe",
  "brand_pair": "<pair_id>",
  "run_index": 0|1|2,
  "prompt": "<full prompt text>",
  "response": "<raw model response>",
  "parsed": {<parsed JSON output or null>},
  "success": true|false,
  "latency_ms": <float>,
  "error": "<error message or null>",
  "language": "en|zh|ru|ja|ko|ar|hi"
}
```
