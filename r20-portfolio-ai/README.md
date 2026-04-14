# R20: Does Corporate Ownership Matter to AI? Portfolio Interference in Large Language Model Brand Perception

**Citation key**: 2026ab | **DOI**: [10.5281/zenodo.19555282](https://doi.org/10.5281/zenodo.19555282) | **Dataset DOI**: [10.57967/hf/8380](https://doi.org/10.57967/hf/8380) | **Status**: Working paper v1.0

## Paper

Zharnikov, D. (2026ab). Does Corporate Ownership Matter to AI? Portfolio Interference in Large Language Model Brand Perception. Working Paper. https://doi.org/10.5281/zenodo.19555282

## Abstract

Large language models (LLMs) increasingly shape how consumers discover and evaluate brands. Brand portfolio theory predicts that revealing corporate ownership should produce perceptual interference via an awareness gate (Keller 1993; Aaker and Keller 1990). Yet LLMs encode portfolio relationships permanently in their parameters, raising the possibility of either maximal interference or complete immunity. We test these hypotheses in a preregistered experiment with 13 LLMs spanning seven training traditions (Western, Chinese, Russian, Indian, Japanese, European, Korean). Twenty brands from seven portfolio archetypes (LVMH, Unilever, P&G, Toyota, L'Oreal, Geely, Yandex) were rated under four prompt modalities---direct rating, naturalistic recommendation, multi-turn conversation with mid-dialogue portfolio reveal, and native-language framing---yielding 7,775 parsed observations. Portfolio framing produces near-zero change in Dimensional Concentration Index (mean |delta DCI| = .26). Equivalence testing confirms the null for 18/20 brands within +/-1.0 DCI points. Multi-turn revelation unlocks modest flattening for reverse-aspiration structures (Geely Auto d = -1.11, FDR-significant), but effects remain portfolio- and modality-specific rather than systematic. Native-language prompts activate model-specific discourse layers without directional amplification. These results generalize spectral immunity across model traditions and portfolio types, implying that house-of-brands shielding is automatic in AI-mediated markets while constructive interference is impossible. Brand managers cannot rely on portfolio architecture to reshape LLM perceptions except in extended conversational contexts.

## Experiment

- **Design**: 20 brands x 7 portfolios x 13 models x 4 modalities x 5 reps = 7,775 parsed observations (7,820 response files)
- **Conditions**: direct solo, direct portfolio, recommendation solo, recommendation portfolio, multi-turn, native-language ablation
- **Portfolios**: LVMH, Unilever, P&G, Toyota, L'Oreal, Geely, Yandex
- **Dataset**: [10.57967/hf/8380](https://doi.org/10.57967/hf/8380)
- **Scale**: 1-5 PRISM-B
- **Models**: Claude Sonnet 4, GPT-4o-mini, Gemini 2.5 Flash, Grok-3-mini, Llama 3.3 70B, DeepSeek V3, YandexGPT 5 Pro, Sarvam M, Gemma 4 (local), GPT-OSS-Swallow, Qwen3 235B, Mistral Large, EXAONE 3.5 32B
- **Training traditions**: Western, Chinese, Russian, Indian, Japanese, European, Korean (7 traditions)
- **Parse success**: 7,775/7,820 (99.4%)
- **Cost**: ~$5

## Hypotheses

| ID | Statement | Status |
|----|-----------|--------|
| H1 | LVMH constructive interference | Not supported |
| H2 | Unilever destructive interference | Not supported |
| H3 | P&G negligible interference | Supported |
| H4 | Toyota/Lexus aspirational interference | Partially supported |
| H5 | Spectral immunity (TOST equivalence, 18/20 brands) | Supported |
| H7 | Reverse aspiration — Geely Auto d = -1.11 (multi-turn) | Supported |
| H8 | Native-language prompts: discourse-layer activation, no directional amplification | Partially supported |

## Reproduction

```bash
# Run experiment
uv run python run_portfolio.py

# Run ablation
uv run python run_portfolio.py --ablation

# Analyze
uv run python analyze_portfolio.py
```

## License

CC BY-NC-ND 4.0
