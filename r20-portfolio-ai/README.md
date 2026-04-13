# R20: Spectral Immunity: Portfolio Framing Does Not Alter AI Brand Perception

**Citation key**: 2026ab | **DOI**: [10.5281/zenodo.19555282](https://doi.org/10.5281/zenodo.19555282) | **Dataset DOI**: [10.57967/hf/8380](https://doi.org/10.57967/hf/8380) | **Status**: Working paper v1.0

## Paper

Zharnikov, D. (2026ab). Spectral Immunity: Portfolio Framing Does Not Alter AI Brand Perception. Working Paper. https://doi.org/10.5281/zenodo.19555282

## Abstract

Large language models increasingly mediate consumer access to brand information through search, recommendation, and conversational interfaces. Prior work establishes that AI systems exhibit systematic dimensional collapse when perceiving brands. Separately, portfolio theory predicts that corporate context should produce interference effects. This paper tests whether portfolio framing alters AI brand perception through a comprehensive experiment: 11 brands across 4 portfolios (LVMH, Unilever, Procter & Gamble, Toyota) rated under 6 conditions by 10 large language models from 5 training traditions---including Russian, Indian, and Japanese models---yielding 2,930 total observations. Three prompt modalities are tested: direct rating, naturalistic recommendation, and multi-turn conversation with mid-conversation portfolio reveal. Results show near-zero effect of portfolio framing across all modalities (mean |delta DCI| = .31, TOST equivalence confirmed for 8/11 brands). Western and non-Western models show identical immunity (both d < .10). Multi-turn portfolio reveal produces slightly more individual-brand effects (3/11 FDR-significant) but no systematic pattern. The sole exception is Lexus under Toyota portfolio framing (d = .64), suggesting aspiration dynamics may partially penetrate AI perception where symmetric interference does not. These findings provide evidence for spectral immunity as a structural property of AI brand perception with direct implications for portfolio management in AI-mediated markets.

## Experiment

- **Design**: 11 brands x 6 conditions x 10 models x 5 reps = 2,930 observations
- **Conditions**: direct solo, direct portfolio, recommendation solo, recommendation portfolio, multi-turn, prompt-location ablation
- **Portfolios**: LVMH, Unilever, P&G, Toyota
- **Dataset**: [10.57967/hf/8380](https://doi.org/10.57967/hf/8380)
- **Scale**: 1-5 PRISM-B
- **Models**: Claude Sonnet 4, GPT-4o-mini, Gemini 2.5 Flash, Grok-3-mini, Llama 3.3 70B, DeepSeek V3, YandexGPT 5 Pro, Sarvam M, Gemma 4 (local), GPT-OSS-Swallow
- **Training traditions**: Western, Chinese, Russian, Indian, Japanese (5 traditions)
- **Parse success**: 2,930/2,930 (100%)
- **Cost**: ~$5

## Hypotheses

| ID | Statement | Status |
|----|-----------|--------|
| H1 | LVMH constructive interference | Not supported |
| H2 | Unilever destructive interference | Not supported |
| H3 | P&G negligible interference | Supported |
| H4 | Spectral immunity (TOST equivalence) | Supported |

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
