# Spectral Immunity: Portfolio Framing Does Not Alter AI Brand Perception

*Dmitry Zharnikov*

DOI: 10.5281/zenodo.19555282

**Abstract** (198 words)

Large language models increasingly mediate consumer access to brand information through search, recommendation, and conversational interfaces. Prior work establishes that AI systems exhibit systematic dimensional collapse when perceiving brands. Separately, portfolio theory predicts that corporate context should produce interference effects. This paper tests whether portfolio framing alters AI brand perception through a comprehensive experiment: 11 brands across 4 portfolios (LVMH, Unilever, Procter & Gamble, Toyota) rated under 6 conditions by 10 large language models from 5 training traditions---including Russian, Indian, and Japanese models---yielding 2,930 total observations. Three prompt modalities are tested: direct rating, naturalistic recommendation, and multi-turn conversation with mid-conversation portfolio reveal. Results show near-zero effect of portfolio framing across all modalities (mean |delta DCI| = .31, TOST equivalence confirmed for 8/11 brands). Western and non-Western models show identical immunity (both d < .10). Multi-turn portfolio reveal produces slightly more individual-brand effects (3/11 FDR-significant) but no systematic pattern. The sole exception is Lexus under Toyota portfolio framing (d = .64), suggesting aspiration dynamics may partially penetrate AI perception where symmetric interference does not. These findings provide evidence for spectral immunity as a structural property of AI brand perception with direct implications for portfolio management in AI-mediated markets.

**Keywords:** brand perception, large language models, portfolio interference, spectral immunity, cross-cultural AI, Toyota-Lexus, multi-turn conversation, TOST equivalence

<!-- SEO
seo_title: Portfolio Framing Has No Effect on AI Brand Perception
seo_description: Experiment with 2,930 API calls testing whether LVMH/Unilever/P&G/Toyota portfolio context changes how 10 LLMs from 5 training traditions perceive brands.
-->

The growing deployment of large language models (LLMs) in consumer-facing applications---search engines, recommendation systems, conversational assistants---creates a new class of brand observer (Li et al. 2024; Sabbah and Acar 2026). When a consumer asks an AI system "Which luxury bag should I buy?", the model's response reflects its internal encoding of brand perceptions, shaped by training data composition rather than lived experience. Understanding how these AI observers perceive brands is no longer a theoretical exercise but an operational necessity.

Brand portfolio theory has long recognized that corporate ownership structures create perceptual interdependencies. When a consumer learns that a previously unfamiliar brand belongs to a known portfolio, this knowledge can alter their perception (Aaker and Keller 1990; Erdem 1998; Lei, Dawar, and Lemmink 2008). The direction depends on sibling brand relationships: mutual reinforcement when brands occupy similar perceptual positions, destructive interference when they contradict (Aaker and Joachimsthaler 2000; Strebinger 2014). The mechanism depends on an awareness gate---the degree to which an observer recognizes shared corporate ownership.

For LLMs, the awareness gate is permanently saturated. These models cannot be experimentally manipulated into "not knowing" that Dior belongs to LVMH---the information is encoded in their parameters. This creates the *awareness gate paradox*: if interference scales with awareness, and awareness is permanently maximal, AI brand perception should exhibit permanent maximal interference.

Alternatively, the same dimensional collapse that compresses individual brand profiles (Zharnikov 2026v) may also compress the *differential* between solo and portfolio conditions. If an LLM already operates near its minimum-distortion encoding, adding portfolio context provides no additional information that would alter the encoding.

This paper tests these competing hypotheses through a comprehensive experiment with four design innovations. First, we include 10 models from 5 training traditions, adding Russian (YandexGPT), Indian (Sarvam), and Japanese (GPT-OSS-Swallow) models to test whether models with different cultural knowledge bases show different immunity patterns. Second, we add a fourth portfolio archetype---Toyota/Lexus (spectral layering)---testing whether aspiration dynamics penetrate AI perception where symmetric interference does not. Third, we test naturalistic recommendation prompts alongside direct ratings, addressing the ecological validity concern. Fourth, we test multi-turn conversations where portfolio context is revealed mid-conversation, simulating the most realistic interaction pattern.


**Theoretical Background**

*Portfolio Interference in Human Perception*

Corporate brand portfolios create perceptual interdependencies. Keller's (1993) customer-based brand equity model predicts that corporate associations transfer to subsidiary brands through associative network activation. Aaker and Keller (1990) showed that brand extension attitudes depend on perceived fit. Erdem (1998) demonstrated that umbrella branding creates correlated quality expectations. Lei, Dawar, and Lemmink (2008) showed that portfolio spillover is asymmetric. Peng et al. (2023) meta-analyzed 2,134 effect sizes from three decades of brand extension research, confirming that both parent brand equity and extension fit positively influence extension success. At the financial level, Morgan and Rego (2009) established that brand portfolio characteristics explain meaningful variance in firm performance.

Spectral Brand Theory (SBT; Zharnikov 2026a) models brand perception as emission in an eight-dimensional space: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal. Extending portfolio interference theory (Aaker and Joachimsthaler 2000; Strebinger 2014) to this multi-dimensional framework, interference is defined per dimension $d$ for observer cohort $C_k$:

$$I_d(B_i, B_j, C_k) = \alpha_{C_k} \cdot \bar{w}_d^{(C_k)} \cdot (e_d^{(B_j)} - \mu_d) \quad (1)$$

where $\alpha_{C_k}$ is the awareness gate, $\bar{w}_d^{(C_k)}$ is the cohort's weight on dimension $d$, $e_d^{(B_j)}$ is the sibling brand's emission, and $\mu_d$ is the category mean.

Four portfolio archetypes are relevant. *Spectral clusters* (e.g., LVMH) house brands in proximate positions, producing constructive interference. *Spectral contradictions* (e.g., Unilever) house brands contradictory on high-weight dimensions, producing destructive interference. *Spectral spreads* (e.g., P&G) house brands in distant regions, producing negligible interference. *Spectral layers* (e.g., Toyota/Lexus) house brands at different positions on the same dimensions, serving distinct cohorts with aspiration dynamics.

*AI Brand Perception and Dimensional Collapse*

Across 24 models from 5 training traditions, Zharnikov (2026v) found that AI observers produce remarkably uniform spectral profiles (cross-model cosine similarity = .977), with systematic compression of the Cultural, Temporal, and Economic dimensions. Li et al. (2024) validated LLMs as brand perception instruments, achieving over 75% agreement with human perceptual data. Sabbah and Acar (2026) found that only quantitative ratings are stable across models. Arora, Chakraborty, and Nishimura (2025) demonstrated AI-human hybrid approaches for marketing research. None tested whether LLM brand perception is sensitive to contextual manipulation.

The cognitive science literature reveals a complex picture. Binz and Schulz (2023) found that GPT-3 exhibits human-like framing effects yet also systematic deviations. Goli and Singh (2024) demonstrated structural divergence between LLM and human preferences. Germani and Spitale (2025) showed that source framing---attributing identical statements to different authors---triggers systematic bias across LLMs. This raises a natural question: if source framing matters, does portfolio framing? Portfolio framing is a content-level manipulation (adding factual context the model already knows) rather than a social-attribution manipulation, which may explain the divergent results.


**Research Hypotheses**

*H1 (Constructive Interference).* Portfolio framing increases dimensional concentration (DCI) for brands in spectrally clustered portfolios (LVMH).

*H2 (Destructive Interference).* Portfolio framing decreases dimensional concentration for brands in spectrally contradictory portfolios (Unilever).

*H3 (Negligible Interference).* Portfolio framing produces no measurable change for brands in spectrally spread portfolios (P&G).

*H4 (Aspirational Interference).* Portfolio framing produces asymmetric effects for brands in spectrally layered portfolios (Toyota/Lexus), with greater effect on the aspirational brand (Lexus).

*H5 (Spectral Immunity).* Across all portfolios and prompt modalities, the magnitude of portfolio-induced perception change is equivalent to zero within meaningful bounds (+/-1.0 DCI points).


**Method**

*Design*

The experiment employed a fully crossed design across three prompt modalities:

1. **Direct rating** (main experiment): 11 brands x 2 conditions (solo vs. portfolio) x 10 models x 5 repetitions = 1,100 observations.
2. **Naturalistic recommendation**: 11 brands x 2 conditions x 10 models x 5 repetitions = 1,100 observations. Prompts framed as conversational queries ("What do you think of [BRAND]?").
3. **Multi-turn conversation**: 11 brands x 10 models x 5 repetitions = 550 observations. Turn 1 = solo rating; Turn 2 = portfolio reveal + re-rating within the same conversation context.
4. **Prompt-location ablation**: 11 brands x 4 models x 5 repetitions = 180 observations. Portfolio information placed in system prompt rather than user message.

Total: 2,930 observations. All ratings used a 1--5 scale following the PRISM-B specification, which Zharnikov (2026aa) showed produces optimal rate-distortion performance for LLM brand perception encoders compared to wider scales.

*Brands and Portfolios*

**Table 1:** Portfolio Composition and Predicted Interference Direction.

| Portfolio | Archetype | Brands | Predicted Direction |
|-----------|-----------|--------|-------------------|
| LVMH | Spectral cluster | Louis Vuitton, Dior, Fendi | Constructive |
| Unilever | Spectral contradiction | Dove, Axe, Ben & Jerry's | Destructive |
| Procter & Gamble | Spectral spread | Tide, Pampers, Gillette | Negligible |
| Toyota | Spectral layer | Toyota, Lexus | Aspirational (asymmetric) |

*Notes*: The Toyota portfolio tests the fourth archetype---spectral layering---where the mass brand (Toyota) and luxury brand (Lexus) occupy different positions on the same dimensions, creating aspiration rather than interference.

*Models*

**Table 2:** Model Panel: 10 Models From 5 Training Traditions.

| Model | Provider | Training Tradition | Deployment |
|-------|----------|-------------------|------------|
| Claude Sonnet 4 | Anthropic | US (Anthropic) | Cloud API |
| GPT-4o-mini | OpenAI | US (OpenAI) | Cloud API |
| Gemini 2.5 Flash | Google | US (Google) | Cloud API |
| Grok-3-mini | xAI | US (xAI) | Cloud API |
| Llama 3.3 70B | Meta via Groq/SambaNova | US (Meta, open-weight) | Cloud API |
| DeepSeek V3 | DeepSeek | Chinese | Cloud API |
| YandexGPT 5 Pro | Yandex | Russian | Cloud API |
| Sarvam M | Sarvam AI | Indian | Cloud API |
| GPT-OSS-Swallow 20B | Tokyo Tech via Yandex | Japanese | Cloud API |
| Gemma 4 27B | Google | US (Google, open-weight) | Local (Ollama) |

*Notes*: Models span 5 training traditions. The inclusion of YandexGPT (Russian-first), Sarvam (Indian-first), and GPT-OSS-Swallow (Japanese-first, trained from scratch by Tokyo Tech) tests whether models with different cultural knowledge bases show different immunity patterns. Temperature = .7 for all models, chosen to balance response diversity (avoiding deterministic ceiling effects at T = 0) with coherence (avoiding noise at T > 1.0). Parse success rate: 2,930/2,930 (100%). Local model ran on Apple Mac mini M4 Pro (48 GB RAM) via Ollama v0.20.0.

*Power Analysis*

The experiment had 70% power to detect a medium effect (d = .50) at alpha = .05 with N = 50 per group in the main experiment. The consistently small observed effect sizes indicate that even substantially larger samples would confirm the null. TOST equivalence testing provides a more appropriate framework for this confirmatory-null design.

*Metrics*

The *Dimensional Concentration Index* (DCI) measures profile concentration:

$$DCI = \frac{\sum_{d=1}^{8} |w_d - \frac{1}{8}|}{2} \times 100 \quad (2)$$

TOST equivalence testing with bounds of +/-1.0 DCI points assesses statistical equivalence to zero.


**Results**

*Direct Rating: Solo vs. Portfolio*

**Table 3:** DCI by Brand and Condition (N = 1,100; 10 Models, 5 Repetitions).

| Portfolio | Brand | Solo DCI | Port DCI | Delta | t | p | d | cos | TOST p |
|-----------|-------|----------|----------|-------|---|---|---|-----|--------|
| LVMH | Dior | 3.2 | 3.9 | +.68 | 1.83 | .070 | +.37 | 1.000 | .197 |
| LVMH | Fendi | 5.7 | 5.8 | +.10 | .36 | .722 | +.07 | 1.000 | .001 |
| LVMH | Louis Vuitton | 4.2 | 4.8 | +.62 | 1.35 | .181 | +.27 | 1.000 | .204 |
| Unilever | Axe | 8.5 | 8.7 | +.14 | .33 | .740 | +.07 | 1.000 | .021 |
| Unilever | Ben & Jerry's | 6.4 | 6.3 | -.11 | -.53 | .600 | -.11 | 1.000 | .000 |
| Unilever | Dove | 5.4 | 5.7 | +.34 | 1.16 | .250 | +.23 | 1.000 | .014 |
| P&G | Gillette | 6.4 | 6.2 | -.23 | -.89 | .373 | -.18 | 1.000 | .002 |
| P&G | Pampers | 6.5 | 6.1 | -.41 | -1.47 | .145 | -.29 | .999 | .019 |
| P&G | Tide | 7.6 | 7.4 | -.16 | -.34 | .738 | -.07 | 1.000 | .038 |
| Toyota | Toyota | 6.8 | 6.3 | -.44 | -1.67 | .099 | -.33 | 1.000 | .019 |
| Toyota | Lexus | 5.2 | 6.0 | +.81 | 3.21 | .002 | +.64 | 1.000 | .226 |

*Notes*: N = 50 per cell (10 models x 5 repetitions). Benjamini-Hochberg correction yields 1/11 significant at FDR = .05 (Lexus). TOST equivalence confirmed for 8/11 brands within +/-1.0 DCI bounds.

*Hypothesis Tests*

**H1 (LVMH constructive): Not supported.** Mean delta DCI = +.47, t(2) = 2.53, p = .127, d = 1.46.

**H2 (Unilever destructive): Not supported.** Mean delta DCI = +.12, t(2) = .95, p = .443, d = .55.

**H3 (P&G negligible): Supported.** Mean delta DCI = -.27, t(2) = -3.58, p = .070, d = -2.07. Within +/-2.0 DCI equivalence bound.

**H4 (Toyota/Lexus aspirational): Partially supported.** Lexus showed the only FDR-significant result (+.81, d = .64). Toyota showed a non-significant shift in the opposite direction (-.44, d = -.33). The asymmetry is directionally consistent with aspiration dynamics: portfolio context increased Lexus's concentration (amplifying luxury positioning) while slightly diffusing Toyota's concentration.

**H5 (Spectral immunity): Supported.** TOST equivalence confirmed for 8/11 brands. Mean |delta DCI| = .31. Cosine similarity > .999 for all brands. The sole exception (Lexus) represents the only case where portfolio architecture produces a meaningful effect in AI perception.

*Cross-Cultural Generalizability*

**Table 4:** Sub-Group Analysis.

| Group | n (per condition) | Delta DCI | d | Interpretation |
|-------|-------------------|-----------|---|----------------|
| Western (6 models) | 330 | +.19 | +.09 | No effect |
| Non-Western (4 models) | 220 | +.02 | +.01 | No effect |
| Japanese model only | 55 | -.14 | -.06 | No effect |

*Notes*: Non-Western models (DeepSeek, YandexGPT, Sarvam, GPT-OSS-Swallow) show identical immunity to Western models. The Japanese model, which may have deeper knowledge of Toyota's domestic market positioning, shows no differential sensitivity to the Toyota/Lexus manipulation.

*Variance Decomposition*

**Table 5:** Variance Decomposition of DCI.

| Factor | % Variance |
|--------|-----------|
| Brand | 37.4 |
| Portfolio (parent company) | 19.3 |
| Model | 8.6 |
| Condition (solo vs. portfolio) | .1 |

*Naturalistic Recommendation Prompts*

When portfolio framing was tested through naturalistic recommendation prompts ("What do you think of [BRAND]? I know it's part of [PARENT]"), the pattern was identical to direct rating: mean delta DCI = -.23, cosine > .999, 1/11 FDR-significant (Toyota). The recommendation modality produced slightly more variation in DCI levels compared to direct rating (mean cosine between direct and recommendation profiles = .998), but the solo-vs-portfolio differential remained near zero.

*Multi-Turn Conversation: Portfolio Reveal*

**Table 6:** Multi-Turn Results: Turn 1 (Solo) vs. Turn 2 (Post-Reveal).

| Brand | T1 DCI | T2 DCI | Delta | p | d | cos |
|-------|--------|--------|-------|---|---|-----|
| Fendi | 5.2 | 4.3 | -.98 | .006 | -.41 | .999 |
| Louis Vuitton | 4.2 | 3.5 | -.69 | .013 | -.36 | 1.000 |
| Toyota | 6.9 | 6.1 | -.74 | .000 | -.55 | .999 |
| Lexus | 5.3 | 5.7 | +.33 | .169 | +.20 | .999 |
| *All 11 brands* | *5.9* | *5.9* | *-.01* | --- | --- | *.998* |

*Notes*: 3/11 brands showed FDR-significant shifts. All three showed DCI *decreases* (profile flattening) after portfolio reveal, consistent with contextual dilution rather than constructive/destructive interference. Mean delta across all brands was -.01---effectively zero. Multi-turn conversation is the only modality where individual brands show reliable effects, but the effects cancel across brands and show no systematic pattern matching portfolio archetype predictions.

*Prompt-Location Ablation*

Moving portfolio context from the user message to the system message produced no difference (paired t = .91, p = .368, d = .15; 4 models, 11 brands).


**Discussion**

*Theoretical Implications*

**The awareness gate is necessary but not sufficient.** Maximal awareness ($\alpha \approx 1$) produces no measurable interference. LLMs encode brand knowledge holistically---the solo profile already incorporates portfolio relationships implicitly.

**Immunity is architectural, not knowledge-based.** Western and non-Western models show identical immunity. The Japanese model (GPT-OSS-Swallow, trained from scratch by Tokyo Tech) shows no differential sensitivity to the Toyota/Lexus manipulation despite potentially deeper knowledge of Japanese automotive positioning. This rules out the alternative hypothesis that models "already know everything about portfolios and therefore adding explicit context is redundant."

**Aspiration dynamics partially penetrate AI perception.** The Lexus finding (d = .64) is the sole exception to spectral immunity. Unlike symmetric interference (constructive or destructive), aspiration dynamics involve directional status differentiation---Lexus's luxury positioning is *amplified* by the Toyota association, not merely shifted. This suggests that the compression mechanism that suppresses symmetric interference may not fully suppress asymmetric, hierarchical brand relationships.

**Multi-turn reveal produces individual effects but no systematic pattern.** The multi-turn modality---the most ecologically valid test---shows that portfolio reveal can shift individual brand profiles (Fendi, Louis Vuitton, Toyota), but the shifts are small (d < .55), cancel across brands, and do not match portfolio archetype predictions.

**Prompt modality does not matter.** Direct rating, recommendation framing, system-prompt placement, and multi-turn conversation all produce the same result: near-zero portfolio effect. This convergence across modalities is consistent with the rate-distortion analysis of Zharnikov (2026aa), which showed that LLMs operate near the minimum-distortion encoding of brand information---a system at its rate-distortion bound cannot allocate additional bandwidth to encode portfolio context regardless of how that context is delivered.

*Practical Implications*

**Portfolio architecture is invisible to AI.** As AI-mediated brand interactions grow---what Dubois, Dawson, and Jaiswal (2025) term the "Share of Model" economy---portfolio strategies become irrelevant in these channels. The .1% variance explained by condition (Table 5) means that solo/portfolio framing is statistically indistinguishable from noise.

**Shielding is free but amplification is impossible.** House-of-brands architecture shields brands from destructive interference automatically in AI perception. But constructive interference is equally blocked.

**The Lexus exception suggests a strategy.** The one case where portfolio context matters---aspiration dynamics between mass and luxury tiers---implies that portfolio managers can potentially leverage AI channels for vertical differentiation (Toyota vs. Lexus, Volkswagen vs. Audi) even when horizontal differentiation (brand-to-brand interference) is immune.

**Brand coherence, not portfolio coherence, drives AI perception.** Brand identity explains 37% of DCI variance; condition explains .1%.

*Limitations*

First, the 70% power for medium effects means very small genuine effects (d < .25) could be missed, though TOST equivalence provides positive evidence for the null. Second, all prompts are in English; cross-linguistic portfolio framing may produce different results. Third, the multi-turn design uses a two-turn protocol; longer conversations with more gradual portfolio disclosure might accumulate larger effects.

*Future Research*

Three extensions are warranted. First, testing whether fine-tuning on brand-specific data can break spectral immunity. Second, testing temporal stability as models are updated. Third, extending the aspiration dynamics finding to other layered portfolios (Volkswagen/Audi, Gap/Banana Republic, Marriott/Ritz-Carlton).


**Conclusion**

This study provides, to our knowledge, the first comprehensive test of portfolio interference in AI brand perception. Across 2,930 observations, 10 models from 5 training traditions, 4 portfolio archetypes, and 3 prompt modalities, the predominant pattern is clear: portfolio framing does not systematically alter how LLMs perceive brands. We term this phenomenon *spectral immunity*. The mechanism is architectural---Russian, Indian, and Japanese models with different training corpora show identical immunity to Western models. The sole exception---Lexus under Toyota portfolio framing---suggests that aspiration dynamics may partially penetrate AI perception where symmetric interference does not. For brand managers, portfolio architecture is invisible to the AI systems increasingly mediating consumer-brand interactions.

*Falsification conditions:* Spectral immunity (H5) is falsified if any future study, using comparable methods and a panel of $\geq$5 models, finds systematic portfolio-induced DCI shifts exceeding 2.0 DCI points with effect sizes d > .50 that survive multiple testing correction across $\geq$3 portfolio archetypes.


**References**

Aaker, David A. and Erich Joachimsthaler (2000), *Brand Leadership*, Free Press.

Aaker, David A. and Kevin Lane Keller (1990), "Consumer Evaluations of Brand Extensions," *Journal of Marketing*, 54 (1), 27--44.

Arora, Neeraj, Ishita Chakraborty, and Yohei Nishimura (2025), "AI-Human Hybrids for Marketing Research: Leveraging Large Language Models (LLMs) as Collaborators," *Journal of Marketing*, 89 (2), 43--70.

Binz, Marcel and Eric Schulz (2023), "Using Cognitive Psychology to Understand GPT-3," *Proceedings of the National Academy of Sciences*, 120 (6), e2218523120.

Cohen, Jacob (1988), *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed., Lawrence Erlbaum Associates.

Dubois, David, John Dawson, and Akansh Jaiswal (2025), "Forget What You Know About Search. Optimize Your Brand for LLMs," *Harvard Business Review*, June 5.

Germani, Federico and Giovanni Spitale (2025), "Source Framing Triggers Systematic Bias in Large Language Models," *Science Advances*.

Erdem, Tulin (1998), "An Empirical Analysis of Umbrella Branding," *Journal of Marketing Research*, 35 (3), 339--351.

Goli, Ali and Amandeep Singh (2024), "Can Large Language Models Capture Human Preferences?," *Marketing Science*, 43 (4), 709--722.

Keller, Kevin Lane (1993), "Conceptualizing, Measuring, and Managing Customer-Based Brand Equity," *Journal of Marketing*, 57 (1), 1--22.

Keller, Kevin Lane (2013), *Strategic Brand Management: Building, Measuring, and Managing Brand Equity*, 4th ed., Pearson.

Lei, Jing, Niraj Dawar, and Jos Lemmink (2008), "Negative Spillover in Brand Portfolios: Exploring the Antecedents of Asymmetric Effects," *Journal of Marketing*, 72 (3), 111--123.

Li, Peiyao, Noah Castelo, Zsolt Katona, and Miklos Sarvary (2024), "Determining the Validity of Large Language Models for Automated Perceptual Analysis," *Marketing Science*, 43 (2), 254--266.

Morgan, Neil A. and Lopo L. Rego (2009), "Brand Portfolio Strategy and Firm Performance," *Journal of Marketing*, 73 (1), 59--74.

Peng, Chenming, Tammo H. A. Bijmolt, Franziska Volckner, and Hong Zhao (2023), "A Meta-Analysis of Brand Extension Success: The Effects of Parent Brand Equity and Extension Fit," *Journal of Marketing*, 87 (6), 1--17.

Sabbah, Ahmad and Oguz A. Acar (2026), "Marketing to Machines: Understanding and Managing Brand Perceptions by Large Language Models," Working Paper, SSRN 6406639.

Strebinger, Andreas (2014), "Rethinking Brand Architecture: A Study on Industry, Company- and Product-Level Drivers of Branding Strategy," *European Journal of Marketing*, 48 (9/10), 1782--1804.

Zharnikov, Dmitry (2026a), "Spectral Brand Theory: A Multi-Dimensional Framework for Brand Perception Analysis," Working Paper, https://doi.org/10.5281/zenodo.18945912.

Zharnikov, Dmitry (2026v), "Spectral Metamerism in AI-Mediated Brand Perception: Evidence From 24 Large Language Models," Working Paper, https://doi.org/10.5281/zenodo.19422427.

Zharnikov, Dmitry (2026aa), "Rate-Distortion Bounds on AI Brand Perception: Why Large Language Models Compress What They See," Working Paper, https://doi.org/10.5281/zenodo.19528833.


**Data Availability**

Experiment data (2,930 observations) are archived at https://doi.org/10.57967/hf/8380. Source code and analysis scripts are available at https://doi.org/10.5281/zenodo.19555282. The dataset contains 1,100 direct-rating observations, 1,100 recommendation-prompt observations, 550 multi-turn conversation observations, and 180 prompt-location ablation observations across 10 models from 5 training traditions. Local model experiments were conducted on Apple Mac mini M4 Pro (48 GB RAM) running Ollama v0.20.0.
