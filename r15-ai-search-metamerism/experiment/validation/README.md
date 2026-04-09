# Validation

Output directory for data validation checks. The `validate.py` script verifies JSONL schema compliance, weight sum tolerances, and model-pair completeness across all session logs.

## Usage

```bash
cd experiment
uv run python validation/validate.py
```

## Checks

- JSON parse validity for every JSONL line
- Weight sum within 15% tolerance of 100
- All 8 dimensions present in parsed weights
- Model names match MODEL_META in analysis script
- No orphaned runs (every model-pair has 3 repetitions)
