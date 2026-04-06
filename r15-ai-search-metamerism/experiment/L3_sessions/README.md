# L3 Sessions

JSONL session logs for all R15 experiment runs. Each file contains one JSON object per
API call with prompt, raw response, parsed output, model ID, latency, and error codes.

## Contents

| File | Run | Calls | Description |
|------|-----|-------|-------------|
| `run2_global.jsonl` | Run 2 | 3,240 | 10 global brand pairs, 6 models, 3 repetitions each |
| `run3_local.jsonl` | Run 3 | 1,620 | 5 local brand pairs (Cyprus, Latvia, Kenya, Vietnam, Serbia), 6 models |
| `run4_resolution.jsonl` | Run 4 | 90 | Brand Function resolution test, 5 local pairs with behavioral specs |
| `run5_crosscultural.jsonl` | Run 5 | 11,410 total (7,999 successful) | 7 cross-cultural pairs, 22 models, 8 cultures, 69 native-language calls |
| `run5_gptoss_swallow.jsonl` | Run 5 supplemental | 435 | gpt-oss-20b/Swallow supplemental run |
| `metadata.yaml` | -- | -- | Run 5 session metadata: package versions, API key hashes, hardware info |

## Run 5 Notes

- **Success rate**: 70.1% (7,999 of 11,410 calls)
- **T-Pro 2.0**: 0 successful responses; excluded from all analysis
- **GLM-4.7, Falcon-H1-Arabic 7B, Qwen3.5 27B**: Insufficient responses for DCI calculation (N/A in tables)
- **Native-language calls**: 69 total (H10 test) across Chinese, Russian, Japanese, Korean, Arabic, Hindi
- **File size**: run5_crosscultural.jsonl is approximately 14MB

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
