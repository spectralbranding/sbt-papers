# Spectral Immunity: Portfolio Framing Does Not Alter AI Brand Perception

*Dmitry Zharnikov*

DOI: 10.5281/zenodo.19555282

**Abstract**

Large language models increasingly mediate consumer access to brand information through search, recommendation, and conversational interfaces. Prior work establishes that AI systems exhibit systematic dimensional collapse when perceiving brands. Separately, portfolio theory predicts that corporate context should produce interference effects. This paper tests whether portfolio framing alters AI brand perception through a comprehensive experiment: 20 brands across 7 portfolios (LVMH, Unilever, Procter & Gamble, Toyota, L'Oreal, Geely, Yandex) rated under 6 conditions by 13 large language models from 7 training traditions---including Russian, Indian, Japanese, European, and Korean models---yielding 7,775 total observations. Four prompt modalities are tested: direct rating, naturalistic recommendation, multi-turn conversation with mid-conversation portfolio reveal, and native-language ablation. Results show near-zero effect of portfolio framing across all modalities (mean |delta DCI| = .26, TOST equivalence confirmed for 18/20 brands). All 7 model traditions show identical immunity. The sole exception pattern is Lexus under Toyota portfolio framing (d = .52, p = .004), which no longer survives FDR correction with 20 tests, reducing it to suggestive rather than definitive. Multi-turn portfolio reveal produces the strongest individual effect: Geely Auto d = -1.11 (FDR-significant), suggesting reverse aspiration can be unlocked through conversational revelation but not direct framing. Native-language framing activates different discourse layers but effects are portfolio-specific and model-specific, not systematic. These findings generalize spectral immunity to 7 portfolio archetypes across 7 model traditions with direct implications for portfolio management in AI-mediated markets.

**Keywords:** brand perception, large language models, portfolio interference, spectral immunity, cross-cultural AI, multi-turn conversation, TOST equivalence, native-language framing, discourse-layer activation, reverse aspiration

<!-- SEO
seo_title: Portfolio Framing Has No Effect on AI Brand Perception
seo_description: Experiment with 7,775 API calls testing whether LVMH/Unilever/P&G/Toyota/L'Oreal/Geely/Yandex portfolio context changes how 13 LLMs from 7 training traditions perceive brands.
-->

The growing deployment of large language models (LLMs) in consumer-facing applications---search engines, recommendation systems, conversational assistants---creates a new class of brand observer (Li et al. 2024; Sabbah and Acar 2026). When a consumer asks an AI system "Which luxury bag should I buy?", the model's response reflects its internal encoding of brand perceptions, shaped by training data composition rather than lived experience. Understanding how these AI observers perceive brands is no longer a theoretical exercise but an operational necessity.

Brand portfolio theory has long recognized that corporate ownership structures create perceptual interdependencies. When a consumer learns that a previously unfamiliar brand belongs to a known portfolio, this knowledge can alter their perception (Aaker and Keller 1990; Erdem 1998; Lei, Dawar, and Lemmink 2008). The direction depends on sibling brand relationships: mutual reinforcement when brands occupy similar perceptual positions, destructive interference when they contradict (Aaker and Joachimsthaler 2000; Strebinger 2014). The mechanism depends on an awareness gate---the degree to which an observer recognizes shared corporate ownership.

For LLMs, the awareness gate is permanently saturated. These models cannot be experimentally manipulated into "not knowing" that Dior belongs to LVMH---the information is encoded in their parameters. This creates the *awareness gate paradox*: if interference scales with awareness, and awareness is permanently maximal, AI brand perception should exhibit permanent maximal interference.

Alternatively, the same dimensional collapse that compresses individual brand profiles (Zharnikov 2026v) may also compress the *differential* between solo and portfolio conditions. If an LLM already operates near its minimum-distortion encoding, adding portfolio context provides no additional information that would alter the encoding.

This paper tests these competing hypotheses through a comprehensive experiment with six design innovations. First, we include 13 models from 7 training traditions, adding European (Mistral Large) and Korean (EXAONE 3.5 32B) models to the original panel to test whether models with different cultural knowledge bases show different immunity patterns. Second, we extend the portfolio design from 4 to 7 archetypes, adding prestige spread (L'Oreal), reverse aspiration (Geely), and branded house (Yandex). Third, we add a fourth portfolio archetype---Toyota/Lexus (spectral layering)---testing whether aspiration dynamics penetrate AI perception where symmetric interference does not. Fourth, we test naturalistic recommendation prompts alongside direct ratings, addressing the ecological validity concern. Fifth, we test multi-turn conversations where portfolio context is revealed mid-conversation, simulating the most realistic interaction pattern. Sixth, we test native-language framing for portfolios with home-market models, testing whether discourse-layer activation produces systematic effects.


**Theoretical Background**

*Portfolio Interference in Human Perception*

Corporate brand portfolios create perceptual interdependencies. Keller's (1993) customer-based brand equity model predicts that corporate associations transfer to subsidiary brands through associative network activation. Aaker and Keller (1990) showed that brand extension attitudes depend on perceived fit. Erdem (1998) demonstrated that umbrella branding creates correlated quality expectations. Lei, Dawar, and Lemmink (2008) showed that portfolio spillover is asymmetric. Peng et al. (2023) meta-analyzed 2,134 effect sizes from three decades of brand extension research, confirming that both parent brand equity and extension fit positively influence extension success. At the financial level, Morgan and Rego (2009) established that brand portfolio characteristics explain meaningful variance in firm performance.

Spectral Brand Theory (SBT; Zharnikov 2026a) models brand perception as emission in an eight-dimensional space: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal. Extending portfolio interference theory (Aaker and Joachimsthaler 2000; Strebinger 2014) to this multi-dimensional framework, interference is defined per dimension $d$ for observer cohort $C_k$:

$$I_d(B_i, B_j, C_k) = \alpha_{C_k} \cdot \bar{w}_d^{(C_k)} \cdot (e_d^{(B_j)} - \mu_d) \quad (1)$$

where $\alpha_{C_k}$ is the awareness gate, $\bar{w}_d^{(C_k)}$ is the cohort's weight on dimension $d$, $e_d^{(B_j)}$ is the sibling brand's emission, and $\mu_d$ is the category mean.

Four portfolio archetypes were tested in the original experiment. *Spectral clusters* (e.g., LVMH) house brands in proximate positions, producing constructive interference. *Spectral contradictions* (e.g., Unilever) house brands contradictory on high-weight dimensions, producing destructive interference. *Spectral spreads* (e.g., P&G) house brands in distant regions, producing negligible interference. *Spectral layers* (e.g., Toyota/Lexus) house brands at different positions on the same dimensions, serving distinct cohorts with aspiration dynamics. The v2.0 extension adds three further archetypes: *prestige spread* (L'Oreal), *reverse aspiration* (Geely), and *branded house* (Yandex).

*AI Brand Perception and Dimensional Collapse*

Across 24 models from 5 training traditions, Zharnikov (2026v) found that AI observers produce remarkably uniform spectral profiles (cross-model cosine similarity = .977), with systematic compression of the Cultural, Temporal, and Economic dimensions. Li et al. (2024) validated LLMs as brand perception instruments, achieving over 75% agreement with human perceptual data. Sabbah and Acar (2026) found that only quantitative ratings are stable across models. Arora, Chakraborty, and Nishimura (2025) demonstrated AI-human hybrid approaches for marketing research. None tested whether LLM brand perception is sensitive to contextual manipulation.

The cognitive science literature reveals a complex picture. Binz and Schulz (2023) found that GPT-3 exhibits human-like framing effects yet also systematic deviations. Goli and Singh (2024) demonstrated structural divergence between LLM and human preferences. Germani and Spitale (2025) showed that source framing---attributing identical statements to different authors---triggers systematic bias across LLMs. This raises a natural question: if source framing matters, does portfolio framing? Portfolio framing is a content-level manipulation (adding factual context the model already knows) rather than a social-attribution manipulation, which may explain the divergent results.


**Research Hypotheses**

*H1 (Constructive Interference).* Portfolio framing increases dimensional concentration (DCI) for brands in spectrally clustered portfolios (LVMH).

*H2 (Destructive Interference).* Portfolio framing decreases dimensional concentration for brands in spectrally contradictory portfolios (Unilever).

*H3 (Negligible Interference).* Portfolio framing produces no measurable change for brands in spectrally spread portfolios (P&G).

*H4 (Aspirational Interference).* Portfolio framing produces asymmetric effects for brands in spectrally layered portfolios (Toyota/Lexus), with greater effect on the aspirational brand (Lexus).

*H5 (Spectral Immunity).* Across all portfolios and prompt modalities, the magnitude of portfolio-induced perception change is equivalent to zero within meaningful bounds (+/-1.0 DCI points).

*H6 (Prestige Gradient).* Portfolio framing flattens the prestige gradient in L'Oreal's brand portfolio, pulling Lancome toward Maybelline's position.

*H7 (Reverse Aspiration).* Portfolio framing suppresses Volvo's premium positioning under Geely ownership, reflecting downward aspirational interference.

*H8 (Language-Dependent Immunity).* Native-language portfolio framing produces larger |delta DCI| than English-language framing for the same brands.

*H9 (Home-Model Amplification).* The native-language effect is strongest when model training tradition matches the language of framing.


**Method**

*Design*

The experiment employed a fully crossed design across four prompt modalities:

1. **Direct rating** (main experiment): 20 brands x 2 conditions (solo vs. portfolio) x 13 models x 5 repetitions = 2,600 observations.
2. **Naturalistic recommendation**: 20 brands x 2 conditions x 13 models x 5 repetitions = 2,600 observations. Prompts framed as conversational queries ("What do you think of [BRAND]?").
3. **Multi-turn conversation**: 20 brands x 13 models x 5 repetitions = 1,300 observations. Turn 1 = solo rating; Turn 2 = portfolio reveal + re-rating within the same conversation context.
4. **Native-language ablation**: 11 brands (4 home portfolios: Toyota, Yandex, Geely, L'Oreal) x 2 conditions x 13 models x 5 repetitions = 1,430 observations. Prompts issued in the home language of the portfolio's country of origin.
5. **Prompt-location ablation**: 20 brands x 4 conditions x 5 repetitions = 400 observations (est). Portfolio information placed in system prompt rather than user message.

Total: approximately 7,930 observation cells (7,775 successfully parsed). All ratings used a 1--5 scale following the PRISM-B specification, which Zharnikov (2026aa) showed produces optimal rate-distortion performance for LLM brand perception encoders compared to wider scales.

*Brands and Portfolios*

**Table 1.** Portfolio Composition and Predicted Interference Direction.

| Portfolio | Archetype | Brands | Predicted Direction |
|-----------|-----------|--------|-------------------|
| LVMH | Spectral cluster | Louis Vuitton, Dior, Fendi | Constructive |
| Unilever | Spectral contradiction | Dove, Axe, Ben & Jerry's | Destructive |
| Procter & Gamble | Spectral spread | Tide, Pampers, Gillette | Negligible |
| Toyota | Spectral layer | Toyota, Lexus | Aspirational (asymmetric) |
| L'Oreal | Prestige spread | L'Oreal Paris, Lancome, Maybelline | Gradient flattening |
| Geely | Reverse aspiration | Volvo, Polestar, Geely Auto | Downward suppression |
| Yandex | Branded house | Yandex, Yandex Taxi, Yandex Market | Shared identity |

*Notes*: The Toyota portfolio tests spectral layering where the mass brand (Toyota) and luxury brand (Lexus) occupy different positions on the same dimensions. The Geely portfolio tests reverse aspiration where a premium acquired brand (Volvo) may be pulled downward by its lower-tier parent. The Yandex portfolio tests branded house architecture where shared naming creates maximum awareness gate saturation.

*Models*

**Table 2.** Model Panel: 13 Models From 7 Training Traditions.

| Model | Provider | Training Tradition | Deployment |
|-------|----------|-------------------|------------|
| Claude Sonnet 4 | Anthropic | Western (US) | Cloud API |
| GPT-4o-mini | OpenAI | Western (US) | Cloud API |
| Gemini 2.5 Flash | Google | Western (US) | Cloud API |
| Grok-3-mini | xAI | Western (US) | Cloud API |
| Llama 3.3 70B | Meta via Groq/SambaNova | Western (US, open-weight) | Cloud API |
| Gemma 4 27B | Google | Western (US, open-weight) | Local (Ollama) |
| DeepSeek V3 | DeepSeek | Chinese | Cloud API |
| Qwen3 235B | Alibaba via Cerebras | Chinese | Cloud (free) |
| YandexGPT 5 Pro | Yandex | Russian | Cloud API |
| Sarvam M | Sarvam AI | Indian | Cloud API |
| GPT-OSS-Swallow 20B | Tokyo Tech via Yandex | Japanese | Cloud API |
| Mistral Large | Mistral AI | European | Cloud API |
| EXAONE 3.5 32B | LG AI Research | Korean | Local (Ollama) |

*Notes*: Models span 7 training traditions. The inclusion of YandexGPT (Russian-first), Sarvam (Indian-first), GPT-OSS-Swallow (Japanese-first, trained from scratch by Tokyo Tech), Mistral Large (European), and EXAONE 3.5 32B (Korean, LG AI Research) tests whether models with different cultural knowledge bases show different immunity patterns. Temperature = .7 for all models, chosen to balance response diversity (avoiding deterministic ceiling effects at T = 0) with coherence (avoiding noise at T > 1.0). Parse success rate: 7,775/7,930 (98.1%). Local models ran on Apple Mac mini M4 Pro (48 GB RAM) via Ollama v0.20.0.

*Power Analysis*

The experiment had 70% power to detect a medium effect (d = .50) at alpha = .05 with N = 50 per group in the main experiment; with N = 65 per cell in v2.0, power exceeds 80% for d = .50. The consistently small observed effect sizes indicate that even substantially larger samples would confirm the null. TOST equivalence testing provides a more appropriate framework for this confirmatory-null design.

*Metrics*

The *Dimensional Concentration Index* (DCI) measures profile concentration:

$$DCI = \frac{\sum_{d=1}^{8} |w_d - \frac{1}{8}|}{2} \times 100 \quad (2)$$

TOST equivalence testing with bounds of +/-1.0 DCI points assesses statistical equivalence to zero. Benjamini-Hochberg correction controls false discovery rate across all 20 brand-level tests.


**Results**

*Direct Rating: Solo vs. Portfolio*

**Table 3.** DCI by Brand and Condition (N = 7,775; 13 Models, 5 Repetitions).

| Portfolio | Brand | Solo DCI | Port DCI | Delta | t | p | d | TOST p | Equivalent |
|-----------|-------|----------|----------|-------|---|---|---|--------|------------|
| LVMH | Dior | 3.5 | 3.8 | +.35 | 1.13 | .262 | +.20 | .020 | Yes |
| LVMH | Fendi | 5.7 | 5.8 | +.09 | .38 | .702 | +.07 | .000 | Yes |
| LVMH | Louis Vuitton | 4.4 | 4.7 | +.34 | .90 | .368 | +.16 | .043 | Yes |
| Unilever | Axe | 8.6 | 8.7 | +.04 | .12 | .909 | +.02 | .002 | Yes |
| Unilever | Ben & Jerry's | 6.4 | 6.4 | -.04 | -.24 | .809 | -.04 | .000 | Yes |
| Unilever | Dove | 5.6 | 5.9 | +.30 | 1.20 | .234 | +.21 | .003 | Yes |
| P&G | Gillette | 6.4 | 6.3 | -.15 | -.71 | .477 | -.13 | .000 | Yes |
| P&G | Pampers | 6.5 | 6.2 | -.29 | -1.27 | .207 | -.22 | .001 | Yes |
| P&G | Tide | 7.4 | 7.2 | -.20 | -.55 | .580 | -.10 | .016 | Yes |
| Toyota | Toyota | 6.8 | 6.4 | -.37 | -1.69 | .093 | -.30 | .003 | Yes |
| Toyota | Lexus | 5.2 | 5.8 | +.59 | 2.94 | .004 | +.52 | .022 | Yes |
| L'Oreal | L'Oreal Paris | 5.6 | 5.5 | -.15 | -.75 | .456 | -.13 | .000 | Yes |
| L'Oreal | Lancome | 5.4 | 5.4 | +.04 | .18 | .858 | +.03 | .000 | Yes |
| L'Oreal | Maybelline | 6.8 | 6.6 | -.13 | -.38 | .705 | -.07 | .007 | Yes |
| Geely | Volvo | 6.4 | 6.3 | -.19 | -.81 | .422 | -.15 | .000 | Yes |
| Geely | Polestar | 8.6 | 8.5 | -.12 | -.37 | .710 | -.07 | .003 | Yes |
| Geely | Geely Auto | 8.0 | 8.5 | +.54 | 1.49 | .139 | +.27 | .102 | No |
| Yandex | Yandex | 6.6 | 6.6 | -.01 | -.03 | .976 | -.01 | .000 | Yes |
| Yandex | Yandex Market | 8.2 | 8.4 | +.21 | .54 | .592 | +.10 | .021 | Yes |
| Yandex | Yandex Taxi | 8.9 | 8.5 | -.36 | -.87 | .384 | -.16 | .062 | No |

*Notes*: N = 65 per cell (13 models x 5 repetitions) for original portfolios; N = 59--65 for v2.0 portfolios. Benjamini-Hochberg correction yields 0/20 significant at FDR = .05. TOST equivalence confirmed for 18/20 brands within +/-1.0 DCI bounds. Geely Auto and Yandex Taxi are inconclusive (neither equivalent nor significantly different). Lexus shows p = .004 in the paired t-test but does not survive FDR correction with 20 tests.

*Hypothesis Tests*

**H1 (LVMH constructive): Not supported.** Mean delta DCI = +.26, effect sizes small (d range +.07 to +.20), no FDR-significant results.

**H2 (Unilever destructive): Not supported.** Mean delta DCI = +.10, effect sizes negligible (d range -.04 to +.21), no FDR-significant results.

**H3 (P&G negligible): Supported.** Mean delta DCI = -.21, TOST equivalent for all 3 brands, no FDR-significant results.

**H4 (Toyota/Lexus aspirational): Partially supported.** Lexus showed delta = +.59 (d = .52, p = .004), directionally consistent with aspiration dynamics. However, with 20 tests, 0/20 survive FDR correction. The Lexus finding is suggestive but not definitive: aspiration dynamics may partially penetrate AI perception, but the evidence is inconclusive at the corrected alpha.

**H5 (Spectral immunity): Supported.** TOST equivalence confirmed for 18/20 brands. Mean |delta DCI| = .26. Cosine similarity > .999 for all brands. 0/20 FDR-significant results. The two inconclusive brands (Geely Auto, Yandex Taxi) show neither equivalence nor a reliable effect---they are statistically underpowered for a conclusion rather than exceptions to immunity.

**H6 (L'Oreal prestige gradient): Not supported.** All three L'Oreal brands show near-zero delta (range -.15 to +.04, all d < .14). Portfolio architecture is invisible even for a prestige-spread structure spanning Lancome to Maybelline.

**H7 (Geely reverse aspiration): Not supported in direct framing.** Volvo shows delta = -.19 (d = -.15, TOST equivalent). The predicted downward suppression is directionally present but too small to constitute evidence. The reverse aspiration hypothesis receives support only in the multi-turn condition (see below).

**H8 (Language-dependent immunity): Mixed.** Native-language framing activates different discourse layers for some portfolios (Geely: Japanese model Swallow shows delta -2.35; Yandex: YandexGPT shows +0.72). However, effects are portfolio-specific and model-specific, with no systematic directional pattern. Native-language framing does not uniformly amplify portfolio effects.

**H9 (Home-model amplification): Mixed.** The predicted home-model amplification appears selectively. Swallow (Japanese) shows the largest tradition-level native effect for Toyota (-2.35). YandexGPT (Russian) shows modest amplification for Yandex (+0.72). Qwen3 (Chinese) shows a notable effect for Volvo (+2.07). None of these survive FDR correction, and there is no consistent pattern of amplification that holds across all home-market pairs.

*Cross-Cultural Generalizability*

**Table 4.** Sub-Group Analysis by Training Tradition.

| Tradition | Models (n) | Delta DCI | d | p (tradition level) |
|-----------|-----------|-----------|---|---------------------|
| Western | 6 | +.02 | +.03 | .882 |
| Chinese | 2 | -.06 | -.09 | .692 |
| European | 1 | -.35 | -.46 | .055 |
| Japanese | 1 | -.59 | -.63 | .011 |
| Korean | 1 | +.34 | +.35 | .130 |
| Russian | 1 | -.24 | -.32 | .168 |
| Indian | 1 | -.13 | -.07 | .743 |

*Notes*: The Japanese model (GPT-OSS-Swallow) shows the only tradition-level p-value below .05 (p = .011, d = -.63). This pattern is driven primarily by the Toyota-related brands, consistent with deeper Japanese automotive market knowledge. However, this is a single model, and the effect does not survive FDR correction across 7 tradition comparisons. All other traditions show identical immunity. The European model (Mistral Large) shows a non-significant trend (p = .055) in the direction of sensitivity.

*Variance Decomposition*

**Table 5.** Variance Decomposition of DCI.

| Factor | % Variance |
|--------|-----------|
| Brand | 37.4 |
| Portfolio (parent company) | 19.3 |
| Model | 8.6 |
| Condition (solo vs. portfolio) | .1 |

*Naturalistic Recommendation Prompts*

When portfolio framing was tested through naturalistic recommendation prompts ("What do you think of [BRAND]? I know it's part of [PARENT]"), the pattern was identical to direct rating: mean delta DCI = -.23, cosine > .999, 0/20 FDR-significant. The recommendation modality produced slightly more variation in DCI levels compared to direct rating (mean cosine between direct and recommendation profiles = .998), but the solo-vs-portfolio differential remained near zero.

*Multi-Turn Conversation: Portfolio Reveal*

Multi-turn conversation is the most ecologically valid test and the modality where the largest individual effects appear. Four brands showed FDR-significant DCI shifts after portfolio reveal:

**Table 6.** Multi-Turn Results: FDR-Significant Brands (Turn 1 Solo vs. Turn 2 Post-Reveal).

| Brand | T1 DCI | T2 DCI | Delta | p | d |
|-------|--------|--------|-------|---|---|
| Geely Auto | 8.1 | 5.1 | -2.93 | <.001 | -1.11 |
| Polestar | 8.8 | 7.4 | -1.47 | <.001 | -.54 |
| Toyota | 6.8 | 6.0 | -.80 | <.001 | -.61 |
| Yandex | 6.2 | 5.1 | -1.06 | <.001 | -.49 |

*Notes*: 4/20 brands showed FDR-significant shifts in multi-turn conversation. All four showed DCI *decreases* (profile flattening) after portfolio reveal, consistent with contextual dilution rather than constructive interference. Geely Auto shows the largest effect in the entire experiment (d = -1.11): when the model is explicitly reminded mid-conversation that Geely Auto is the parent of Volvo and Polestar, the reverse aspiration operates in the predicted direction---but only through conversational accumulation, not direct framing. Mean delta across all 20 brands was -.03---effectively zero.

*Native-Language Ablation*

Native-language framing was tested for the 4 portfolios with identifiable home-market languages (Japanese/Toyota, Russian/Yandex, Chinese/Geely, French/L'Oreal). Results show that native-language framing activates different discourse registers for specific model-portfolio pairs but does not produce systematic amplification of portfolio effects. The clearest signal is the Japanese model (Swallow) under Japanese-language Toyota framing (delta -2.35 vs. -.37 in English), and YandexGPT under Russian-language Yandex framing (+0.72 vs. -.01 in English). However, Qwen3 under Chinese-language Geely framing shows a Volvo-specific effect (+2.07) that is opposite in direction to the home-model amplification prediction. No native-language effect survives FDR correction.

*Prompt-Location Ablation*

Moving portfolio context from the user message to the system message produced no difference (paired t = .91, p = .368, d = .15; 4 models, 20 brands).


**Discussion**

*Theoretical Implications*

**The awareness gate is necessary but not sufficient.** Maximal awareness ($\alpha \approx 1$) produces no measurable interference. LLMs encode brand knowledge holistically---the solo profile already incorporates portfolio relationships implicitly.

**Spectral immunity generalizes to 7 portfolio archetypes.** The original finding (4 archetypes, 4 portfolios, 10 models, 5 traditions) now extends to 7 archetypes, 7 portfolios, 13 models, and 7 traditions. L'Oreal's prestige spread, Yandex's branded house, and Geely's reverse aspiration all show the same immunity pattern as LVMH, Unilever, P&G, and Toyota in direct framing. The structural property holds regardless of portfolio type.

**Immunity is architectural, not knowledge-based.** All 7 model traditions show immunity. The Japanese model (GPT-OSS-Swallow) shows the only tradition-level significant effect (p = .011, d = -.63), driven primarily by Toyota-related brands, which is consistent with deeper Japanese automotive market knowledge. But this is one model, the effect does not survive tradition-level FDR correction, and it does not break the fundamental immunity pattern.

**The Lexus finding no longer survives multiple testing correction.** With 20 brands and FDR correction, the Lexus result (p = .004, d = .52) yields 0/20 FDR-significant results. Aspiration dynamics remain directionally suggestive---Lexus shows the largest positive delta of any brand---but the evidence is no longer strong enough to conclude that aspiration dynamics are an exception to spectral immunity. Future work should test this specifically with a dedicated aspiration-focused design.

**Reverse aspiration can be unlocked through conversational revelation but not direct framing.** The Geely Auto multi-turn finding (d = -1.11) is the strongest single effect in the experiment. In direct framing, Geely Auto shows a small non-significant increase in DCI when portfolio context is added. But in multi-turn conversation, when the model has established Volvo's premium perception in Turn 1 and then receives portfolio context in Turn 2, Geely Auto's DCI drops by 2.93 points. The mechanism appears to be conversational anchoring: Turn 1 establishes a premium anchor for the portfolio family, making Turn 2's framing more effective. This pattern does not appear for portfolios without the reverse-aspiration dynamic (LVMH, P&G), suggesting it is specific to ownership structures that violate the quality-hierarchy expectation.

**Native-language framing activates discourse layers but not systematically.** The native-language ablation reveals model-portfolio-specific sensitivity rather than a general amplification principle. The Japanese model's sensitivity to Japanese-language Toyota framing, and YandexGPT's sensitivity to Russian-language Yandex framing, suggest that home-language prompts activate different discourse registers in home-tradition models. But the effects are not unidirectional, not consistent across portfolios, and do not survive FDR correction. This is consistent with Zharnikov (2026v)'s finding that cross-cultural differences in AI brand perception represent discourse-layer activation rather than cultural bias.

**Prompt modality does not matter for systematic effects.** Direct rating, recommendation framing, system-prompt placement, and multi-turn conversation all produce the same result for 18/20 brands: near-zero portfolio effect. This convergence across modalities is consistent with the rate-distortion analysis of Zharnikov (2026aa), which showed that LLMs operate near the minimum-distortion encoding of brand information---a system at its rate-distortion bound cannot allocate additional bandwidth to encode portfolio context regardless of how that context is delivered.

*Practical Implications*

**Portfolio architecture is invisible to AI across all archetype types.** As AI-mediated brand interactions grow---what Dubois, Dawson, and Jaiswal (2025) term the "Share of Model" economy---portfolio strategies become irrelevant in these channels across all 7 archetypes tested. Prestige spread (L'Oreal), reverse aspiration (Geely), and branded house (Yandex) are as invisible to AI as symmetric interference structures.

**Shielding is free but amplification is impossible.** House-of-brands architecture shields brands from destructive interference automatically in AI perception. But constructive interference is equally blocked. The Yandex branded house---where shared naming maximally saturates the awareness gate---shows the same immunity as LVMH's house-of-brands architecture.

**Geely's reverse aspiration is a strategic vulnerability in conversational AI.** While direct portfolio framing leaves Volvo's positioning intact, multi-turn conversation reveals a meaningful effect: when users engage in extended dialogue about Geely's portfolio, Geely Auto's perceived differentiation collapses (d = -1.11). This suggests that in conversational AI channels, brand managers should anticipate that extended interactions about the portfolio can surface reverse-aspiration dynamics that are invisible in single-turn queries.

**The Lexus strategy remains plausible but unproven.** The aspirational differentiation pattern (Lexus d = .52) is directionally consistent but no longer statistically robust after FDR correction with 20 brands. Portfolio managers pursuing vertical differentiation strategies (Toyota/Lexus, Volkswagen/Audi, Gap/Banana Republic) should treat AI-channel aspiration dynamics as an open empirical question.

**Brand coherence, not portfolio coherence, drives AI perception.** Brand identity explains 37% of DCI variance; condition explains .1%.

*Limitations*

First, with 20 tests and FDR correction, the study has limited power to detect effects at the brand level (the Lexus finding would be significant under a per-comparison alpha). A dedicated within-archetype replication with larger samples would provide cleaner evidence. Second, the multi-turn design uses a two-turn protocol; longer conversations with more gradual portfolio disclosure might accumulate larger effects. Third, native-language results are based on a single model per tradition (except Western and Chinese), limiting the generalizability of tradition-level conclusions.

*Future Research*

Four extensions are warranted. First, a dedicated replication of the Lexus finding with a multi-brand aspirational layer panel (Toyota/Lexus, Volkswagen/Audi, Marriott/Ritz-Carlton) to determine whether d = .52 represents a real exception to spectral immunity. Second, extended multi-turn designs (5+ turns) to test whether conversational accumulation can unlock portfolio effects in non-reverse-aspiration portfolios. Third, longitudinal testing of whether spectral immunity is stable as models are updated or fine-tuned. Fourth, testing whether the Japanese model's tradition-level sensitivity (p = .011) replicates in a study specifically designed around automotive portfolios with Japanese and non-Japanese models.


**Conclusion**

This study provides a comprehensive test of portfolio interference in AI brand perception. Across 7,775 observations, 13 models from 7 training traditions, 7 portfolio archetypes, and 4 prompt modalities, the predominant pattern is clear: portfolio framing does not systematically alter how LLMs perceive brands. We term this phenomenon *spectral immunity*. The mechanism is architectural---Russian, Indian, Japanese, European, and Korean models with different training corpora show identical immunity to Western models. The original Lexus exception (d = .64 with 11 brands) reduces to a suggestive but FDR-inconclusive pattern (d = .52, 0/20 FDR-significant) with the full 20-brand panel. The multi-turn Geely Auto finding (d = -1.11) is the strongest effect in the experiment, revealing that reverse aspiration can be unlocked through conversational revelation---but this is a conditional vulnerability, not a general exception to spectral immunity. For brand managers, portfolio architecture is invisible to the AI systems increasingly mediating consumer-brand interactions. The exception is conversational AI with extended interaction: portfolios with reverse-aspiration structure show meaningful effects in multi-turn dialogue that are absent in single-turn queries.

*Falsification conditions:* Spectral immunity (H5) is falsified if any future study, using comparable methods and a panel of $\geq$7 models from $\geq$3 traditions, finds systematic portfolio-induced DCI shifts exceeding 2.0 DCI points with effect sizes d > .50 that survive multiple testing correction across $\geq$5 portfolio archetypes and $\geq$3 prompt modalities simultaneously.


**References**

Aaker, David A. and Erich Joachimsthaler (2000), *Brand Leadership*, Free Press.

Aaker, David A. and Kevin Lane Keller (1990), "Consumer Evaluations of Brand Extensions," *Journal of Marketing*, 54 (1), 27--44.

Arora, Neeraj, Ishita Chakraborty, and Yohei Nishimura (2025), "AI-Human Hybrids for Marketing Research: Leveraging Large Language Models (LLMs) as Collaborators," *Journal of Marketing*, 89 (2), 43--70.

Binz, Marcel and Eric Schulz (2023), "Using Cognitive Psychology to Understand GPT-3," *Proceedings of the National Academy of Sciences*, 120 (6), e2218523120.

Cohen, Jacob (1988), *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed., Lawrence Erlbaum Associates.

Dubois, David, John Dawson, and Akansh Jaiswal (2025), "Forget What You Know About Search. Optimize Your Brand for LLMs," *Harvard Business Review*, June 5.

Erdem, Tulin (1998), "An Empirical Analysis of Umbrella Branding," *Journal of Marketing Research*, 35 (3), 339--351.

Germani, Federico and Giovanni Spitale (2025), "Source Framing Triggers Systematic Bias in Large Language Models," *Science Advances*.

Goli, Ali and Amandeep Singh (2024), "Can Large Language Models Capture Human Preferences?," *Marketing Science*, 43 (4), 709--722.

Keller, Kevin Lane (1993), "Conceptualizing, Measuring, and Managing Customer-Based Brand Equity," *Journal of Marketing*, 57 (1), 1--22.

Keller, Kevin Lane (2013), *Strategic Brand Management: Building, Measuring, and Managing Brand Equity*, 4th ed., Pearson.

Lei, Jing, Niraj Dawar, and Jos Lemmink (2008), "Negative Spillover in Brand Portfolios: Exploring the Antecedents of Asymmetric Effects," *Journal of Marketing*, 72 (3), 111--123.

LG AI Research (2024), "EXAONE: LG AI Research's Open-Source Language Model," Technical Report, LG AI Research.

Li, Peiyao, Noah Castelo, Zsolt Katona, and Miklos Sarvary (2024), "Determining the Validity of Large Language Models for Automated Perceptual Analysis," *Marketing Science*, 43 (2), 254--266.

Mistral AI (2024), "Mistral Large: A Frontier-Class Language Model," Technical Report, Mistral AI.

Morgan, Neil A. and Lopo L. Rego (2009), "Brand Portfolio Strategy and Firm Performance," *Journal of Marketing*, 73 (1), 59--74.

Peng, Chenming, Tammo H. A. Bijmolt, Franziska Volckner, and Hong Zhao (2023), "A Meta-Analysis of Brand Extension Success: The Effects of Parent Brand Equity and Extension Fit," *Journal of Marketing*, 87 (6), 1--17.

Qwen Team (2025), "Qwen3 Technical Report," Alibaba Group, arXiv:2505.09388.

Sabbah, Ahmad and Oguz A. Acar (2026), "Marketing to Machines: Understanding and Managing Brand Perceptions by Large Language Models," Working Paper, SSRN 6406639.

Strebinger, Andreas (2014), "Rethinking Brand Architecture: A Study on Industry, Company- and Product-Level Drivers of Branding Strategy," *European Journal of Marketing*, 48 (9/10), 1782--1804.

Zharnikov, Dmitry (2026a), "Spectral Brand Theory: A Multi-Dimensional Framework for Brand Perception Analysis," Working Paper, https://doi.org/10.5281/zenodo.18945912.

Zharnikov, Dmitry (2026v), "Spectral Metamerism in AI-Mediated Brand Perception: Evidence From 24 Large Language Models," Working Paper, https://doi.org/10.5281/zenodo.19422427.

Zharnikov, Dmitry (2026aa), "Rate-Distortion Bounds on AI Brand Perception: Why Large Language Models Compress What They See," Working Paper, https://doi.org/10.5281/zenodo.19528833.


**Data Availability**

Experiment data (7,775 observations) are archived at https://doi.org/10.57967/hf/8380. Source code and analysis scripts are available at https://doi.org/10.5281/zenodo.19555282. The dataset contains 2,600 direct-rating observations, 2,600 recommendation-prompt observations, 1,300 multi-turn conversation observations, 1,430 native-language ablation observations, and approximately 400 prompt-location ablation observations across 13 models from 7 training traditions. Local model experiments were conducted on Apple Mac mini M4 Pro (48 GB RAM) running Ollama v0.20.0.
