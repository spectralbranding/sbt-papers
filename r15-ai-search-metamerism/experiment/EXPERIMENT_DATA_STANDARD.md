# Experiment Data Standard

Version: 1.0 (Session 107, 2026-04-17)

Every experiment in this directory MUST produce JSONL data that passes the CI validation pipeline (`validation/validate.py --all`). This document is the single source of truth for data format requirements.

## Directory Structure (Cascade)

```
experiment/
  L0_specification/    # Protocols, pre-registrations (human-readable)
  L1_models/           # Model configs (models.yaml)
  L2_prompts/          # Python scripts + prompt templates
  L3_sessions/         # Raw JSONL output (one line per API call)
  L4_analysis/         # Aggregated results, summaries, figures
  validation/          # Schema, checksums, validate.py
```

## Required Fields (Every JSONL Record)

Every line in every `L3_sessions/*.jsonl` file MUST contain these four fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `timestamp` | string (ISO 8601) | When the API call was made | `"2026-04-17T14:10:11.641018+00:00"` |
| `model` | string | Short model name from models.yaml | `"claude"`, `"gpt"`, `"gemma4_local"` |
| `prompt_type` | string (enum) | Which prompt template was used | `"weighted_recommendation"` |
| `prompt` | string | Full rendered prompt text sent to model | The complete user prompt |

### Model Naming Convention

The `model` field uses a short canonical name. The `model_id` field (optional but recommended) stores the provider-specific identifier.

| `model` (required) | `model_id` (recommended) | Provider |
|---------------------|--------------------------|----------|
| `claude` | `claude-haiku-4-5` | Anthropic |
| `gpt` | `gpt-4o-mini` | OpenAI |
| `gemini` | `gemini-2.5-flash` | Google |
| `deepseek` | `deepseek-chat` | DeepSeek |
| `grok` | `grok-4-1-fast-non-reasoning` | xAI |
| `gemma4_local` | `gemma4:latest` | Ollama (local) |
| `qwen3_local` | `qwen3:32b` | Ollama (local) |
| `qwen35_local` | `qwen2.5:32b` | Ollama (local) |
| `llama` | `llama-3.3-70b-versatile` | Groq |
| `qwen3` | `qwen-3-235b-a22b-instruct-2507` | Cerebras |
| `yandexgpt` | `yandexgpt/latest` | Yandex |
| `gigachat` | `GigaChat-Pro` | Sber |
| `allam` | `sdaia/allam-2-7b-instruct` | SDAIA |
| `jais` | `inception/jais-adapted-70b-chat` | Inception |
| `exaone` | `LGAI-EXAONE/EXAONE-4.0-32B-Instruct` | LG AI |
| `swallow` | `tokyotech-llm/Swallow-70b-instruct-v0.1` | Tokyo Tech |

When adding a new model, add it to this table and to `L1_models/models.yaml`.

### Prompt Type Enum

The `prompt_type` field MUST be one of the values registered in `validation/schemas/session_record.schema.json`. Current valid values:

- `weighted_recommendation` — core R15 brand pair recommendation
- `weighted_recommendation_spec` — with Brand Function specification
- `weighted_recommendation_native` — native-language variant
- `weighted_recommendation_native_spec` — native + specification
- `dimensional_differentiation` — dimension-level differentiation probe
- `dimension_probe` — single-dimension single-brand probe
- `geopolitical_framing` — city-based geopolitical framing
- `geopolitical_framing_native` — native-language geopolitical
- `compounding_format` — multi-step agentic pipeline (specification paradox)

**To add a new prompt type**: update the enum in `session_record.schema.json` BEFORE committing data.

## Recommended Fields

These fields are not required by the schema but SHOULD be included for reproducibility:

| Field | Type | Description |
|-------|------|-------------|
| `model_id` | string | Full provider model identifier |
| `response` | string | Full raw model response |
| `parsed` | object/array/null | Parsed structured output |
| `latency_ms` | number | API call latency in milliseconds |
| `tokens_in` | integer | Input token count |
| `tokens_out` | integer | Output token count |
| `error` | string/null | Error message if call failed; null on success |
| `temperature` | number | Sampling temperature |
| `brand` | string | Brand being evaluated |
| `run` | integer | Repetition number |

## Experiment-Specific Fields

Experiments MAY add additional fields beyond the schema (the schema has `"additionalProperties": true`). Common extensions:

- `condition` — experimental condition (e.g., `"baseline"`, `"specified"`, `"constraint"`)
- `bf_condition` — Brand Function condition
- `native_language` — two-letter language code
- `city` — for geopolitical framing experiments
- `step` — for multi-step pipeline experiments
- `repetition` — within-condition repetition number
- `system_prompt` — full system prompt (for reproducibility)
- `system_prompt_hash` — SHA-256 hash prefix for deduplication

## Validation Pipeline

CI runs `validation/validate.py --all` on every push. This checks:

1. **Schema**: every JSONL record matches `session_record.schema.json`
2. **Completeness**: all expected files exist
3. **Integrity**: SHA-256 checksums match `checksums.sha256`

### After Adding New Data

1. Ensure all JSONL records have the 4 required fields
2. If using a new `prompt_type`, update the schema enum first
3. Run `uv run python validation/validate.py --all` locally
4. If adding new L3/L4 files, run `uv run python validation/validate.py --regenerate-checksums`
5. Commit the updated `checksums.sha256` alongside the data

### Supplementary Experiments

Files matching these prefixes are SKIPPED by core schema validation (they use enriched schemas validated by their own scripts): `run12_`, `run12b_`, `run13_`, `run14_`, `run15_`, `run15b_`.

**New experiments should NOT rely on the skip list.** Instead, ensure data conforms to the standard schema from the start. The skip list exists only for legacy experiments that predate this standard.

## Python Script Template

Every experiment script in `L2_prompts/` SHOULD output JSONL records with at minimum:

```python
record = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "model": MODEL_SHORT_NAME,       # from models.yaml
    "model_id": full_model_id,       # provider-specific
    "prompt_type": "your_type_here", # must be in schema enum
    "prompt": rendered_prompt,        # full text sent to model
    "response": raw_response,
    "parsed": parsed_output,
    "latency_ms": elapsed_ms,
    "tokens_in": usage.get("input"),
    "tokens_out": usage.get("output"),
    "error": None,                   # or error message string
    "temperature": temperature,
    "brand": brand_name,
}
```

## Checklist for New Experiments

- [ ] Protocol written in `L0_specification/`
- [ ] Script in `L2_prompts/` outputs JSONL with all 4 required fields
- [ ] `prompt_type` registered in schema enum
- [ ] Model short names match the table above
- [ ] Local validation passes (`validate.py --all`)
- [ ] Checksums regenerated
- [ ] L4 analysis summary written
- [ ] HuggingFace README updated (if dataset extends existing)
