# R16: AI-Native Brand Identity

**Paper**: AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification

**Author**: Dmitry Zharnikov

**DOI**: [10.5281/zenodo.19391476](https://doi.org/10.5281/zenodo.19391476)

**Citation key**: 2026x

## Abstract

This paper proposes the observer-driven evolution thesis --- identity verification technologies change discontinuously in response to shifts in the observer type --- and introduces behavioral metamerism as the AI-native equivalent of visual brand confusion. A pre-registered pilot study (684 API calls, 6 LLMs, 4 architectural clusters) provides initial empirical support: three of six models showed zero discrimination for the high-metamerism brand pair under statistical-only observation, rising to 100% discrimination across all models when behavioral specifications were provided (Fisher's exact *p* = 0.0009, Cohen's *d* = 0.791). The paper argues that cryptographic signatures on behavioral specifications (the Brand Function) are positioned to replace logos as the primary brand identity mechanism for AI-mediated commerce.

## Repository Contents

| File | Description |
|------|-------------|
| `paper.md` | Full paper (v1.7, ~12,800 words, 6 propositions, 4 results tables) |
| `paper.pdf` | PDF export (263K) |
| `paper.yaml` | Paper specification (machine-readable claims) |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTORS.yaml` | Contributor attribution (human + AI) |
| `PROVENANCE.yaml` | Version history and submission records |
| `DATA_MANIFEST.yaml` | Experiment data inventory |
| `experiment/` | Full experiment infrastructure (see below) |

## Behavioral Metamerism Pilot

The pilot tests whether LLMs can distinguish brands with identical statistical profiles but different behavioral specifications. Results are reported in Section 9 of the paper.

**Key results (684 API calls, 0 errors):**
- VitaCore vs NutraPure BMI = 0.979 (high behavioral metamerism)
- 3/6 models: 0% discrimination (statistical) -> 100% (augmented)
- All 6 models: 100% discrimination in augmented condition
- Fisher's exact p = 0.0009, Cohen's d = 0.791, Fleiss' kappa = 0.536

### Experiment Structure

```
experiment/
  L0_specification/protocol.md    # Pre-registration (written before data collection)
  L3_sessions/
    session_log.jsonl             # 684 prompt-response pairs with timestamps
    metadata.yaml                 # Model configs, package versions, hardware
    PRE_REGISTRATION.md           # Hypothesis statements
  results.json                    # Full results (6,956 lines)
  summary_tables.md               # Pre-formatted results tables
  behavioral_metamerism_pilot.py  # Experiment script
  requirements.txt                # Python dependencies
```

### Running the Experiment

```bash
cd experiment
pip install -r requirements.txt

# Set API keys (models with missing keys are skipped)
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export GOOGLE_API_KEY=AI...
export DEEPSEEK_API_KEY=sk-...

# Run with local models (Qwen3 30B, Gemma 4 27B via Ollama)
python behavioral_metamerism_pilot.py --live --runs 3
```

### Models Tested

| Model | Cluster | API |
|-------|---------|-----|
| Claude Haiku 3.5 | Western cloud | Anthropic |
| GPT-4o-mini | Western cloud | OpenAI |
| Gemini 2.5 Flash | Western cloud | Google |
| DeepSeek V3 | Chinese cloud | DeepSeek |
| Qwen3 30B | Local open-weight | Ollama |
| Gemma 4 27B | Local open-weight | Ollama |

### Measures

| Measure | What it tests |
|---------|--------------|
| **Brand discrimination** | Can the LLM distinguish brands with identical statistics? |
| **Behavioral prediction** | Does Brand Function access improve edge-case prediction? |
| **Recommendation stability** | Does Brand Function reduce cross-LLM variance? |
| **BMI** | Ratio of statistical similarity to behavioral difference (0-1) |

## How to Cite

```bibtex
@article{zharnikov2026x,
  title={AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification},
  author={Zharnikov, Dmitry},
  year={2026},
  doi={10.5281/zenodo.19391476},
  url={https://doi.org/10.5281/zenodo.19391476}
}
```

## License

MIT
