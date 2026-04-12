# R19: Empirical Rate-Distortion Curve for AI Brand Perception Encoders

**Status:** In preparation. The full paper draft is scheduled for the next research session.

This file is a placeholder. The experiment is complete (see `experiment/L4_analysis/r19_summary.md` and the `_supplementary.md` files), but the publication-ready manuscript has not yet been written.

The headline findings are:

1. **J-shaped R(D) curve** with minimum distortion at R2 (1-5 scale per dimension, ~19 bits), NOT at R1 (100-point allocation, ~26 bits). All seven AI architectures show this non-monotonic pattern. Paired t-tests yield t(6) = 5.81 (R1 vs R2), 6.04 (R3 vs R2), 7.70 (R4 vs R2), all p < .001 with Cohen's d_z > 2.20. Combined Fisher test p < .0001.

2. **Codebook convergence** across architectures. The mean cross-model coefficient of variation in distortion is .107 across all five rate conditions, well below the .15 threshold pre-registered for H2. The seven LLMs (Anthropic Claude, OpenAI GPT, Google Gemini, xAI Grok, DeepSeek, Alibaba Qwen via Cerebras, Meta Llama via Groq) all trace essentially the same J-shaped curve.

3. **Brand-specific encoding patterns** in R1 reveal that AI dimensional collapse is condition-dependent. When asked directly about famous brands, models do NOT uniformly collapse toward Economic + Semiotic. Hermes (DCI shift +2.3pp) and Erewhon (+0.5pp) are recovered close to canonical; Tesla (-8.6pp) and Patagonia (-3.2pp) are shifted AWAY from Economic + Semiotic; only IKEA shows clear collapse-direction inflation (+5.2pp). This refines the cross-category R15 finding (DCI .355) by showing that direct elicitation produces much smaller distortion (mean L1/2 = .153) than pair comparison.

4. **H4 (architectural separation between Western and cross-cultural model groups)** is NOT SUPPORTED, but the test is severely underpowered (n=4 vs n=3, p = .534, Cohen's d = -.464).

The full paper draft will be added in the next research session and will target Marketing Letters (Springer) as the primary venue, with Quantitative Marketing and Economics (Springer) as the backup.

## Reproducing the experiment

1. Use the R15 virtualenv: `/Users/d/projects/sbt-papers/r15-ai-search-metamerism/experiment/.venv/bin/python`
2. Set required API keys: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY, DEEPSEEK_API_KEY, GROQ_API_KEY, CEREBRAS_API_KEY, GROK_API_KEY
3. From `experiment/`: `python run19_rate_sweep.py --smoke` then `python run19_rate_sweep.py --live`
4. Validation: `python validation/validate.py --all`

Total runtime: ~33 minutes wall clock. Total cost: $0.225 (cloud APIs only).
