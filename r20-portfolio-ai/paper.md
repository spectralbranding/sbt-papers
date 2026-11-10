# Does Corporate Ownership Matter to AI? Portfolio Interference in Large Language Model Brand Perception

Dmitry Zharnikov

ORCID: 0009-0000-6893-9231

DOI: [10.5281/zenodo.19555282](https://doi.org/10.5281/zenodo.19555282)

Working Paper v1.3.0 – April 2026 (revised November 2026)

## Abstract

Large language models (LLMs) increasingly shape how consumers discover and evaluate brands. Brand portfolio theory predicts that revealing corporate ownership produces perceptual interference via an awareness gate [@keller-1993-conceptualizing-measuring-managing; @aaker-1990-consumer-evaluations-brand]. Because LLMs encode portfolio relationships permanently in their parameters, they should exhibit either maximal interference or complete immunity. This study tests these hypotheses across 13 LLMs spanning seven training traditions. Twenty brands from seven portfolio archetypes were rated under four prompt modalities---direct rating, naturalistic recommendation, multi-turn conversation with mid-dialogue portfolio reveal, and native-language framing---yielding 7,975 observations. An extension added 20 brands from published marketing research (1,950 observations, zero overlap), replicating immunity and bringing the combined dataset to 9,925 observations across 40 brands. Portfolio framing produces near-zero change in Dimensional Concentration Index (mean $|\Delta\mathrm{DCI}| = .23$); equivalence testing confirms the null for 18 of 20 brands within $\pm 1.0$ DCI points. Multi-turn revelation unlocks modest flattening for reverse-aspiration structures (Geely Auto $d = -1.11$, FDR-significant), but effects remain portfolio- and modality-specific. These results generalize spectral immunity across model traditions and portfolio types: house-of-brands shielding is automatic in AI-mediated markets, while constructive interference is impossible except in extended conversational contexts. Implications for awareness-gate mechanisms and "Share of Model" strategy are discussed.

**Keywords:** brand perception, large language models, portfolio interference, awareness gate, TOST equivalence, cross-cultural AI, multi-turn conversation, native-language framing, Share of Model

---

When a consumer asks an LLM "Which luxury bag should I buy?", the model's response reflects its internal brand encoding, shaped by training data composition rather than lived experience. Understanding these AI observers is now operationally critical [@dubois-2025-forget-what-you]. LLMs increasingly mediate consumer access to brand information through search, recommendation, and conversational interfaces, constituting a new class of brand observer whose perceptual structure differs systematically from human observers (Li et al. [-@li-2024-frontiers-determining-validity]; Sabbah and Acar [-@sabbah-2026-marketing-machines-understanding]).

Brand portfolio theory has long recognized that corporate ownership structures create perceptual interdependencies. Classic portfolio theory [@aaker-1990-consumer-evaluations-brand; @keller-1993-conceptualizing-measuring-managing] predicts interference when corporate ownership becomes salient: constructive for spectrally similar brands, destructive for contradictory ones. The mechanism is an awareness gate---the degree to which the observer recognizes shared corporate ownership. Erdem [-@erdem-1998-empirical-analysis-umbrella] demonstrated that umbrella branding creates correlated quality expectations. Lei, Dawar, and Lemmink [-@lei-2008-negative-spillover-brand] showed that portfolio spillover is asymmetric and sensitive to perceived fit. Brand, Israeli, and Ngwe [-@brand-2023-using-gpt-market] demonstrated that LLMs can be used for market research, raising the question of whether these instruments respond to contextual manipulations the way human respondents do. Recent work on AI-mediated brand perception [@arora-2025-aihuman-hybrids-marketing; @hermann-2025-empowering-genai-stakeholders] further establishes that LLM brand responses are systematic and measurable---but whether they are sensitive to portfolio context has not been tested.

For LLMs, the awareness gate is permanently saturated. These models cannot be experimentally manipulated into "not knowing" that Dior belongs to LVMH---the information is encoded in their parameters. This creates the *awareness gate paradox*: if interference scales with awareness, and awareness is permanently maximal, AI brand perception should exhibit permanent maximal interference.

Alternatively, LLMs may operate near minimum-distortion encodings of brand information. If dimensional compression is already at its limit, adding portfolio context provides no additional signal that would alter the encoding. One theoretical framework that predicts this immunity via rate-distortion compression is Spectral Brand Theory [@zharnikov-2026-spectral-brand-theory-computational-framework], but the prediction follows from any account in which LLM brand encodings are compressed and stable.

This paper provides the first comprehensive test of portfolio interference in LLM brand perception. We test competing hypotheses---maximal interference vs. spectral immunity---through an experiment with six design innovations: 13 models from 7 training traditions, 7 portfolio archetypes, 4 prompt modalities, multi-turn conversation with mid-dialogue portfolio reveal, native-language ablation, and prompt-location ablation. Across 7,975 observations, the predominant finding is clear: 0/20 brands show FDR-significant portfolio effects in direct rating or recommendation conditions.

## Theoretical Background

### Portfolio Interference in Human Perception

Corporate brand portfolios create perceptual interdependencies. Keller's [-@keller-1993-conceptualizing-measuring-managing; -@keller-2013-strategic-brand-management] customer-based brand equity model predicts that corporate associations transfer to subsidiary brands through associative network activation. Aaker and Keller [-@aaker-1990-consumer-evaluations-brand] showed that brand extension attitudes depend on perceived fit between parent brand and extension. Erdem [-@erdem-1998-empirical-analysis-umbrella] demonstrated that umbrella branding creates correlated quality expectations across portfolio members. Lei, Dawar, and Lemmink [-@lei-2008-negative-spillover-brand] showed that portfolio spillover is asymmetric: negative spillover is stronger from weaker to stronger brands. Peng et al. [-@peng-2023-metaanalysis-brand-extension] meta-analyzed 2,134 effect sizes from three decades of brand extension research, confirming that both parent brand equity and extension fit positively influence extension success. At the financial level, Morgan and Rego [-@morgan-2009-brand-portfolio-strategy] established that brand portfolio characteristics explain meaningful variance in firm performance.

Interference direction depends on the structural relationship between portfolio members. *Constructive interference* arises when sibling brands occupy proximate positions on high-salience dimensions. *Destructive interference* arises when siblings contradict on those dimensions. *Negligible interference* characterizes brands occupying distinct perceptual territories with low shared dimensionality. The key moderator in all accounts is the awareness gate: the consumer must know about the ownership relationship for any interference to occur [@aaker-2000-brand-leadership; @strebinger-2014-rethinking-brand-architecture].

Four portfolio archetypes operationalize these predictions. *Spectral clusters* (e.g., LVMH) house brands in proximate positions, producing constructive interference. *Spectral contradictions* (e.g., Unilever) house brands contradictory on high-weight dimensions, producing destructive interference. *Spectral spreads* (e.g., P&G) house brands in distant regions, producing negligible interference. *Spectral layers* (e.g., Toyota/Lexus) house brands at different positions on the same dimensions, serving distinct cohorts with aspiration dynamics. The present study adds three further archetypes: *prestige spread* (L'Oreal), *reverse aspiration* (Geely), and *branded house* (Yandex).

### AI as Brand Observer

Li et al. [-@li-2024-frontiers-determining-validity] validated LLMs as brand perception instruments, achieving over 75% agreement with human perceptual data across a large-scale Marketing Science study. The underlying capability is well established in computational social science, where LLMs match or exceed trained crowd workers as zero-shot text annotators across classification tasks such as stance, topic, and frame detection [@gilardi-2023-chatgpt-outperforms-crowd; @ziems-2024-can-large-language-models]. Brand, Israeli, and Ngwe [-@brand-2023-using-gpt-market] demonstrated the use of GPT for market research tasks including brand positioning. Arora, Chakraborty, and Nishimura [-@arora-2025-aihuman-hybrids-marketing] demonstrated AI-human hybrid approaches for marketing research, establishing reliability and validity benchmarks. Hermann and Puntoni [-@hermann-2025-empowering-genai-stakeholders] examined how generative AI shapes stakeholder engagement, arguing that understanding the internal structure of LLM brand responses is now a strategic necessity. Grewal, Levy, and Kumar [-@grewal-2025-generative-ai-marketing] document the broader shift toward generative AI in marketing practice. Cillo, Verona, and Wuyts [-@cillo-2025-generative-ai-future] outline a research roadmap for generative AI in marketing, identifying brand perception measurement as a priority area. Wang, Zhang, and Zhang [-@wang-2026-llm-market-research-data-augmentation] survey LLM applications for market research via a data-augmentation approach, noting both capabilities and limitations of current approaches.

LLM brand responses show systematic dimensional patterns. Across 24 models from seven training traditions, cross-model cosine similarity for brand profiles reaches .977, with systematic compression of the Cultural, Temporal, and Economic dimensions [@zharnikov-2026-dimensional-collapse-ai-mediated-search]. Sabbah and Acar [-@sabbah-2026-marketing-machines-understanding] found that only quantitative ratings are stable across models. Goli and Singh [-@goli-2024-frontiers-can-large] demonstrated structural divergence between LLM and human preferences in choice tasks. None of this prior work tested whether LLM brand perception is sensitive to contextual manipulation---specifically, whether adding portfolio context to a brand query changes the model's brand encoding.

The cognitive science literature reveals relevant evidence. Binz and Schulz [-@binz-2023-using-cognitive-psychology] found that GPT-3 exhibits human-like framing effects yet also systematic deviations. Germani and Spitale [-@germani-2025-source-framing-triggers] showed that source framing---attributing identical statements to different authors---triggers systematic bias across LLMs. Portfolio framing is a content-level manipulation (adding factual context the model already knows) rather than a social-attribution manipulation, which may explain divergent results.

### The Awareness Gate Paradox

The awareness gate mechanism [@keller-1993-conceptualizing-measuring-managing] holds that portfolio interference requires the observer to recognize the ownership relationship. In human samples, this gate is calibrated experimentally: studies manipulate whether respondents learn about corporate ownership. In LLMs, no such manipulation is possible---the ownership relationship is encoded in parameters. The awareness gate is permanently saturated at $\alpha \approx 1$.

This creates the awareness gate paradox. If interference scales with awareness (as standard portfolio theory predicts), LLMs should show maximal portfolio effects. Yet if LLM encodings are already compressed to near-minimum-distortion representations of brands, adding portfolio context provides no additional information the encoding can absorb. The distinction is between an observer for whom portfolio knowledge is *new* (human experimental manipulation) and one for whom it is *structural* (LLM parameters). The present study tests which regime governs LLM brand perception.

One formal representation of this compression account is the SBT interference equation:

$$I_d(B_i, B_j, C_k) = \alpha_{C_k} \cdot \bar{w}_d^{(C_k)} \cdot (e_d^{(B_j)} - \mu_d) \quad (1)$$

where $\alpha_{C_k}$ is the awareness gate, $\bar{w}_d^{(C_k)}$ is the cohort's weight on dimension $d$, $e_d^{(B_j)}$ is the sibling brand's emission, and $\mu_d$ is the category mean.[^1] Under immunity, $\alpha_{C_k}$ is maximal but the compression constraint prevents the interference term from propagating into the observable profile. The present paper tests this prediction empirically without requiring acceptance of any particular theoretical framework.

[^1]: This formulation is from Spectral Brand Theory [@zharnikov-2026-spectral-brand-theory-computational-framework], where Dimensional Concentration Index (DCI) measures profile concentration across eight brand perception dimensions. DCI is a new metric not yet validated against human data; the Boundary Conditions and Limitations section discusses this as a primary boundary condition on our conclusions.

## Research Hypotheses

Core hypotheses (H1--H5) are derived from portfolio theory and the awareness gate mechanism. Extension hypotheses H6--H7 test new archetypes added in the present study; H8--H9 are exploratory tests of the native-language modality (see Method).

*H1 (Constructive Interference).* Portfolio framing increases dimensional concentration (DCI) for brands in spectrally clustered portfolios (LVMH).

*H2 (Destructive Interference).* Portfolio framing decreases dimensional concentration for brands in spectrally contradictory portfolios (Unilever).

*H3 (Negligible Interference).* Portfolio framing produces no measurable change for brands in spectrally spread portfolios (P&G).

*H4 (Aspirational Interference).* Portfolio framing produces asymmetric effects for brands in spectrally layered portfolios (Toyota/Lexus), with greater effect on the aspirational brand (Lexus).

*H5 (Spectral Immunity).* Across all portfolios and prompt modalities, the magnitude of portfolio-induced perception change is equivalent to zero within meaningful bounds ($\pm 1.0$ DCI points).

*H6 (Prestige Gradient).* Portfolio framing flattens the prestige gradient in L'Oreal's brand portfolio, pulling Lancome toward Maybelline's position.

*H7 (Reverse Aspiration).* Portfolio framing suppresses Volvo's premium positioning under Geely ownership, reflecting downward aspirational interference.

*H8 (Language-Dependent Immunity).* Native-language portfolio framing produces larger $|\Delta\mathrm{DCI}|$ than English-language framing for the same brands.

*H9 (Home-Model Amplification).* The native-language effect is strongest when model training tradition matches the language of framing.

## Method

### Design

The experiment employed a fully crossed design across four prompt modalities:

1. **Direct rating** (main experiment): 20 brands x 2 conditions (solo vs. portfolio) x 13 models x 5 repetitions = 2,600 observations.
2. **Naturalistic recommendation**: 20 brands x 2 conditions x 13 models x 5 repetitions = 2,600 observations. Prompts framed as conversational queries ("What do you think of [BRAND]?").
3. **Multi-turn conversation**: 20 brands x 13 models x 5 repetitions = 1,300 observations. Turn 1 = solo rating; Turn 2 = portfolio reveal + re-rating within the same conversation context.
4. **Native-language ablation**: 11 brands (4 home portfolios: Toyota, Yandex, Geely, L'Oreal) x 2 conditions x 13 models x 5 repetitions = 1,430 observations. Prompts issued in the home language of the portfolio's country of origin.
5. **Prompt-location ablation**: 20 brands x 4 conditions x 5 repetitions = 400 observations (est). Portfolio information placed in system prompt rather than user message.

Total: 8,330 designed observation cells, of which 8,022 produced a recorded response and 7,975 were successfully parsed. All ratings used a 1--5 scale following the PRISM-B specification [@zharnikov-2026-empirical-rate-distortion-curve-ai].

Hypotheses H1--H7 were specified prior to data collection on the basis of the theoretical framework; H8--H9 were added after initial analysis as exploratory tests. This study was not formally preregistered.

### Brands and Portfolios

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

### Models

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

*Notes*: Models span 7 training traditions. The inclusion of YandexGPT (Russian-first), Sarvam (Indian-first), GPT-OSS-Swallow (Japanese-first, trained from scratch by Tokyo Tech), Mistral Large (European), and EXAONE 3.5 32B (Korean, LG AI Research) tests whether models with different cultural knowledge bases show different immunity patterns. Temperature = .7 for all models. Parse success rate: 7,975/8,022 (99.4%) of recorded responses. Local models ran on Apple Mac mini M4 Pro (48 GB RAM) via Ollama v0.20.0. Technical reports for the regional and open models: Qwen3 [@qwen-2025-qwen3-technical-report], Mistral Large [@mistral-2024-mistral-large-frontierclass], and EXAONE 3.5 [@lg-2024-exaone-3-5].

### Power Analysis

The experiment had 70% power to detect a medium effect (d = .50; [@cohen-1988-statistical-power-analysis]) at alpha = .05 with N = 50 per group in the main experiment; with N = 65 per cell in v2.0, power exceeds 80% for d = .50. The consistently small observed effect sizes indicate that even substantially larger samples would confirm the null. TOST equivalence testing provides a more appropriate framework for this confirmatory-null design.

### Metrics

The *Dimensional Concentration Index* (DCI) measures profile concentration:

$$DCI = \frac{\sum_{d=1}^{8} |w_d - \frac{1}{8}|}{2} \times 100 \quad (2)$$

This generalizes the two-dimension form $\mathrm{DCI}_{\mathrm{R15}} = (w_{\mathrm{Economic}} + w_{\mathrm{Semiotic}}) / 100$ used in Zharnikov [-@zharnikov-2026-dimensional-collapse-ai-mediated-search], which was specialized to the AI Economic Default; the 8-dimension L1 form here measures total concentration regardless of which dimensions absorb the mass.

TOST equivalence testing with bounds of $\pm 1.0$ DCI points assesses statistical equivalence to zero. Benjamini-Hochberg correction controls false discovery rate across all 20 brand-level tests.

## Results

### Main Results: Direct Rating Solo vs. Portfolio

The predominant finding is clear: 0/20 brands show FDR-significant portfolio effects in direct rating conditions. Table 3 presents the full brand-level results.

**Table 3.** DCI by Brand and Condition.

| Portfolio | Brand | Solo DCI | Port DCI | Delta | t | p | d | TOST p | Equivalent |
|-----------|-------|----------|----------|-------|---|---|---|--------|------------|
| LVMH | Dior | 3.5 | 3.8 | +.35 | 1.13 | .262 | +.20 | .020 | Yes |
| LVMH | Fendi | 5.7 | 5.8 | +.09 | .38 | .702 | +.07 | < .001 | Yes |
| LVMH | Louis Vuitton | 4.4 | 4.7 | +.34 | .90 | .368 | +.16 | .043 | Yes |
| Unilever | Axe | 8.6 | 8.7 | +.04 | .12 | .909 | +.02 | .002 | Yes |
| Unilever | Ben & Jerry's | 6.4 | 6.4 | -.04 | -.24 | .809 | -.04 | < .001 | Yes |
| Unilever | Dove | 5.6 | 5.9 | +.30 | 1.20 | .234 | +.21 | .003 | Yes |
| P&G | Gillette | 6.4 | 6.3 | -.15 | -.71 | .477 | -.13 | < .001 | Yes |
| P&G | Pampers | 6.5 | 6.2 | -.29 | -1.27 | .207 | -.22 | .001 | Yes |
| P&G | Tide | 7.4 | 7.2 | -.20 | -.55 | .580 | -.10 | .016 | Yes |
| Toyota | Toyota | 6.8 | 6.4 | -.37 | -1.69 | .093 | -.30 | .003 | Yes |
| Toyota | Lexus | 5.2 | 5.8 | +.59 | 2.94 | .004 | +.52 | .022 | Yes |
| L'Oreal | L'Oreal Paris | 5.6 | 5.5 | -.15 | -.75 | .456 | -.13 | < .001 | Yes |
| L'Oreal | Lancome | 5.4 | 5.4 | +.05 | .28 | .783 | +.05 | < .001 | Yes |
| L'Oreal | Maybelline | 6.6 | 6.6 | -.10 | -.29 | .771 | -.05 | .004 | Yes |
| Geely | Volvo | 6.5 | 6.2 | -.28 | -1.30 | .196 | -.23 | < .001 | Yes |
| Geely | Polestar | 8.6 | 8.5 | -.08 | -.27 | .788 | -.05 | .001 | Yes |
| Geely | Geely Auto | 8.0 | 8.5 | +.54 | 1.49 | .139 | +.27 | .102 | No |
| Yandex | Yandex | 6.6 | 6.6 | -.01 | -.03 | .976 | -.01 | < .001 | Yes |
| Yandex | Yandex Market | 8.2 | 8.4 | +.21 | .54 | .592 | +.10 | .021 | Yes |
| Yandex | Yandex Taxi | 8.9 | 8.5 | -.36 | -.87 | .384 | -.16 | .062 | No |

*Notes*: N = 2,555 direct ratings (the solo and portfolio cells of the 7,975-observation main experiment); 13 models, 5 repetitions, up to 65 per cell (seven brands have fewer in at least one cell, the smallest 58). Benjamini-Hochberg correction yields 0/20 significant at FDR = .05. TOST equivalence confirmed for 18/20 brands within $\pm 1.0$ DCI bounds. Geely Auto and Yandex Taxi are inconclusive (neither equivalent nor significantly different). Lexus shows p = .004 in the independent-samples t-test but does not survive FDR correction with 20 tests. The mean absolute delta over the 20 brands is .23. SEs of the 40 cell means (SD/sqrt(n)) range from .10 to .31.

### Hypothesis Tests

One decision rule governs every verdict below, and it is stated before the verdicts so that it is visibly applied uniformly. Difference hypotheses (H1, H2, H4, H6, H7, H8, H9) are scored *supported* only on an effect that survives FDR correction at $\alpha$ = .05 across the 20 tests, and *not supported* otherwise, whatever the uncorrected magnitude. Equivalence hypotheses (H3, H5) are scored on TOST against the $\pm 1.0$ DCI bound. No verdict is graded on direction, on an uncorrected *p*, or on a subset of cells chosen after the fact. Where an uncorrected effect is large enough to be worth recording, it is reported as an observation and named as one, and it does not move the verdict.

**H1 (LVMH constructive): Not supported.** Mean $\Delta\mathrm{DCI} = +.26$, effect sizes small (d range +.07 to +.20), no FDR-significant results.

**H2 (Unilever destructive): Not supported.** Mean $\Delta\mathrm{DCI} = +.10$, effect sizes negligible (d range -.04 to +.21), no FDR-significant results.

**H3 (P&G negligible): Supported.** Mean $\Delta\mathrm{DCI} = -.21$, TOST equivalent for all 3 brands, no FDR-significant results.

**H4 (Toyota/Lexus aspirational): Not supported at corrected alpha.** Lexus showed $\Delta = +.59$ (d = .52, p = .004) but does not survive FDR correction across 20 tests. The direction is consistent with aspiration dynamics but the evidence is inconclusive. Lexus (d = +.52) shows a larger effect than Toyota (d = -.30), directionally consistent with the H4 prediction of a greater effect on the aspirational brand. However, neither effect survives FDR correction, making this suggestive rather than conclusive.

**H5 (Spectral Immunity): Supported.** TOST equivalence confirmed for 18/20 brands. Mean $|\Delta\mathrm{DCI}| = .23$. Cosine similarity $> .999$ for all brands. 0/20 FDR-significant results. The two inconclusive brands (Geely Auto, Yandex Taxi) show neither equivalence nor a reliable effect---they are statistically underpowered for a conclusion rather than exceptions to immunity.

**H6 (L'Oreal prestige gradient): Not supported.** All three L'Oreal brands show near-zero $\Delta$ (range -.15 to +.05, all $d < .14$). Portfolio architecture is invisible even for a prestige-spread structure spanning Lancome to Maybelline.

**H7 (Geely reverse aspiration): Not supported in direct framing.** Volvo shows $\Delta = -.28$ (d = -.23, TOST equivalent). The predicted downward suppression is directionally present but too small to constitute evidence. The reverse aspiration hypothesis receives support only in the multi-turn condition (see below).

**H8 (Language-dependent immunity; exploratory): Not supported.** No native-language effect survives FDR correction, which under the rule stated above settles the verdict. Two uncorrected observations are worth recording and do not change it: the Japanese Swallow model returns $\Delta = -2.35$ for Toyota and YandexGPT returns $\Delta = +.72$ for Yandex. Effects are portfolio-specific and model-specific with no systematic directional pattern. Because each tradition is represented by a single model, H8 and H9 cannot distinguish home-model amplification from model-specific idiosyncrasy in any case---the Swallow/Toyota effect ($\Delta = -2.35$) may reflect a Swallow-specific response pattern rather than a general Japanese-tradition phenomenon. An earlier version scored H8 and H9 as *Mixed*; that label rested on uncorrected magnitude, which is not the basis on which H1, H2, H6 and H7 were scored, and it has been withdrawn in favour of the single rule.

**H9 (Home-model amplification; exploratory): Not supported.** No home-model effect survives FDR correction. The largest uncorrected signal is Swallow (Japanese) for Toyota ($\Delta = -2.35$); YandexGPT (Russian) for Yandex (+.72) and Qwen3 (Chinese) for Volvo (+2.07) are smaller, and no consistent pattern of amplification holds across home-market pairs. Selective appearance in single-model traditions is what the exploratory design cannot distinguish from noise, and it is not scored as partial support.

### Cross-Cultural Generalizability

**Table 4.** Sub-Group Analysis by Training Tradition.

| Tradition | Models (n) | Delta DCI | d | p (tradition level) |
|-----------|-----------|-----------|---|---------------------|
| Western | 6 | +.01 | +.02 | .913 |
| Chinese | 2 | -.06 | -.09 | .692 |
| European | 1 | -.35 | -.46 | .055 |
| Japanese | 1 | -.59 | -.63 | .011 |
| Korean | 1 | +.34 | +.35 | .130 |
| Russian | 1 | -.24 | -.32 | .168 |
| Indian | 1 | -.13 | -.07 | .743 |

*Notes*: The Japanese model (GPT-OSS-Swallow) shows the only tradition-level p-value below .05 (p = .011, d = -.63). This pattern is driven primarily by the Toyota-related brands, consistent with deeper Japanese automotive market knowledge. However, this is a single model, and the effect does not survive FDR correction across 7 tradition comparisons. All other traditions show identical immunity. The European model (Mistral Large) shows a non-significant trend (p = .055) in the direction of sensitivity. SEs of the tradition-level mean deltas (SD of the 20 brand deltas / sqrt(20)) range from .12 to .38.

### Variance Decomposition

**Table 5.** Variance Decomposition of DCI.

| Factor | % Variance |
|--------|-----------|
| Portfolio (parent company) | 25.2 |
| Brand within portfolio | 16.2 |
| Model | 7.5 |
| Condition (solo vs. portfolio) | < .01 |
| Residual | 51.1 |

*Notes*: N = 2,555 direct ratings (20 brands, solo and portfolio conditions). Shares are sequential (type I) sums of squares in the order listed, each factor adjusted for those above it, as a percentage of the total sum of squares, so the five shares sum to 100. Brand is nested in portfolio (each brand has one parent), so marginal one-factor shares would overlap. Brand identity, portfolio plus brand within portfolio, explains 41.4% of DCI variance. Condition (solo vs. portfolio framing) explains .003%, under .01% and about four orders of magnitude less than brand identity. Residual variance (51.1%) reflects within-cell variation (repetition-level noise), model x brand interactions, and condition x brand interactions not captured by the main effects.

### Robustness Checks

**Naturalistic recommendation prompts.** When portfolio framing was tested through naturalistic recommendation prompts ("What do you think of [BRAND]? I know it's part of [PARENT]"), the pattern was identical to direct rating: mean $\Delta\mathrm{DCI} = -.23$, cosine $> .999$, 0/20 FDR-significant. The recommendation modality produced slightly more variation in DCI levels compared to direct rating (mean cosine between direct and recommendation profiles = .998), but the solo-vs-portfolio differential remained near zero.

**Prompt-location ablation.** Moving portfolio context from the user message to the system message produced no difference (paired t = .91, p = .368, d = .15; 4 models, 20 brands). Portfolio information location is irrelevant to perception outcomes.

### Extensions

**Multi-turn conversation: Portfolio reveal.** Multi-turn conversation is the most ecologically valid test and the modality where the largest individual effects appear. Four brands showed FDR-significant DCI shifts after portfolio reveal:

**Table 6.** Multi-Turn Results: FDR-Significant Brands (Turn 1 Before vs. Turn 2 After the Portfolio Reveal).

| Brand | T1 DCI | T2 DCI | Delta | p | d |
|-------|--------|--------|-------|---|---|
| Geely Auto | 8.1 | 5.1 | -2.93 | <.001 | -1.11 |
| Polestar | 8.8 | 7.4 | -1.47 | <.001 | -.54 |
| Toyota | 6.8 | 6.0 | -.80 | <.001 | -.61 |
| Yandex | 6.2 | 5.1 | -1.06 | <.001 | -.49 |

*Notes*: 4/20 brands showed FDR-significant shifts in multi-turn conversation. All four showed DCI decreases (profile flattening) after portfolio reveal, consistent with contextual dilution rather than constructive interference. Geely Auto shows the largest effect in the entire experiment (d = -1.11): when the model is explicitly reminded mid-conversation that Geely Auto is the parent of Volvo and Polestar, the reverse aspiration operates in the predicted direction---but only through conversational accumulation, not direct framing. Mean $\Delta$ across all 20 brands was -.26: the mean of the 20 per-brand Turn 1 to Turn 2 changes (SD = .88; t(19) = -1.31, p = .205, d = -.29), so it is not distinguishable from zero across brands, and the 16 brands not shown average +.07. Pooled over all 1,235 parsed response pairs the mean change is -.23 (paired t(1234) = -3.13, p = .002, d = -.09). Turn 1 is the rating given in the same conversation before the portfolio is disclosed, not the separate solo condition of Table 3. The Geely Auto multi-turn finding is notable but conditional: it requires extended conversational context and reflects a specific reverse-aspiration dynamic rather than a general exception to immunity.

**Native-language ablation.** Native-language framing was tested for the 4 portfolios with identifiable home-market languages (Japanese/Toyota, Russian/Yandex, Chinese/Geely, French/L'Oreal). Results show that native-language framing activates different discourse registers for specific model-portfolio pairs but does not produce systematic amplification of portfolio effects. The clearest signal is the Japanese model (Swallow) under Japanese-language Toyota framing ($\Delta = -2.35$ vs. -.37 in English), and YandexGPT under Russian-language Yandex framing (+.72 vs. -.01 in English). However, Qwen3 under Chinese-language Geely framing shows a Volvo-specific effect (+2.07) that is opposite in direction to the home-model amplification prediction. No native-language effect survives FDR correction.

## Replication with Published Brand Stimuli

The 20 brands in the main experiment were selected to represent seven portfolio archetypes. That selection, while theoretically motivated, is concentrated in a narrow band of portfolio combinations. To address the external validity concern, we conducted an extension using an independent brand stimulus set drawn entirely from published peer-reviewed marketing research.

### Brand Selection

Twenty brands were drawn from canonical empirical studies: Aaker [-@aaker-1997-dimensions-brand-personality], Brakus, Schmitt, and Zarantonello [-@brakus-2009-brand-experience-what], Li, Castelo, Katona, and Sarvary [-@li-2024-frontiers-determining-validity], Erdem [-@erdem-1998-empirical-analysis-umbrella], Dew, Ansari, and Toubia [-@dew-2022-letting-logos-speak], Morgan and Rego [-@morgan-2009-brand-portfolio-strategy], and Malar, Krohmer, Hoyer, and Nyffenegger [-@malar-2011-emotional-brand-attachment]. These stimulus sets span brand personality, brand experience, brand extensions, umbrella branding, and emotional brand attachment---traditions that are empirically distinct from the portfolio interference literature. Zero overlap exists between the 20 extension brands and the 20 main-experiment brands.

Ten brands were tested in both solo and portfolio conditions: Coca-Cola (Coca-Cola Co), Pepsi (PepsiCo), BMW (BMW Group), Audi (Volkswagen Group), Google (Alphabet), Disney (Walt Disney Co), Colgate (Colgate-Palmolive), Samsung (Samsung Group), H&M (H&M Group), and Dell (Dell Technologies). Ten brands were tested in solo condition only: Apple, Nike, Starbucks, IBM, Harley-Davidson, Rolex, Amazon, Adidas, McDonald's, and Red Bull. The same 13-model, 7-tradition panel and identical PRISM-B protocol were applied. Total: 1,950 observations (1,300 solo + 650 portfolio), 5 repetitions per cell. The 10 brands rated under both conditions (1,300 observations) form the immunity test in Table 7, which uses the same DCI metric (Equation 2) as Table 3; solo cell means fall in the same range (5.2 to 9.1 in Table 7 vs. 3.5 to 8.9 in Table 3).

### Results

**Table 7.** Published-Brand Extension: Portfolio Immunity Test (N = 1,300).

| Brand | Parent | Solo DCI | Port DCI | Delta | d |
|-------|--------|----------|----------|-------|---|
| Coca-Cola | Coca-Cola Co | 5.8 | 6.0 | +.21 | +.16 |
| Pepsi | PepsiCo | 6.2 | 6.8 | +.52 | +.34 |
| BMW | BMW Group | 5.2 | 5.1 | -.13 | -.12 |
| Audi | VW Group | 5.5 | 5.0 | -.45 | -.44 |
| Google | Alphabet | 5.8 | 6.0 | +.22 | +.16 |
| Disney | Walt Disney Co | 5.2 | 5.3 | +.12 | +.07 |
| Colgate | Colgate-Palmolive | 7.9 | 8.4 | +.47 | +.20 |
| Samsung | Samsung Group | 5.5 | 5.6 | +.09 | +.07 |
| H&M | H&M Group | 9.1 | 9.1 | +.04 | +.01 |
| Dell | Dell Technologies | 8.4 | 8.4 | -.03 | -.02 |

*Notes*: DCI is computed by Equation 2, as in Table 3. N = 65 per cell (13 models x 5 repetitions). 0/10 brands FDR-significant at q = .05 (Benjamini-Hochberg; the smallest uncorrected p is Audi's, .012, against a threshold of .005). TOST equivalence within $\pm 1.0$ DCI bounds is confirmed for 9 of 10 brands; Colgate is inconclusive ($\Delta$ = +.47, TOST p = .104). SEs of the 20 cell means (SD/sqrt(n)) range from .11 to .38.

The extension replicates the core immunity finding: no brand is FDR-significant and 9 of 10 are TOST-equivalent (Colgate, $\Delta$ = +.47, is inconclusive). No brand shows $|d| > .50$ in the portfolio condition. The largest uncorrected effect is Audi's (d = -.44, p = .012, Volkswagen Group framing), a reduction in concentration that falls just below the medium-effect threshold and does not survive FDR correction; the largest positive effect is Pepsi (d = +.34, p = .053, PepsiCo framing). H&M (d = +.01), Dell (d = -.02), Disney (d = +.07), and Samsung (d = +.07) show near-exact immunity regardless of whether the parent conglomerate name substantially differs from the brand name.

Audi's effect is opposite in sign to the Lexus finding from the main experiment (Lexus d = +.52, Toyota framing): Lexus concentrates under portfolio framing while Audi diffuses. Neither survives FDR correction (Audi p = .012 against a Benjamini-Hochberg threshold of .005), so neither displaces the immunity conclusion.

Combined with the main experiment, R20 now encompasses 9,925 observations across 40 brands (20 + 20, zero overlap), 13 models, and 7 training traditions. Spectral immunity generalizes across stimulus sets drawn from independent empirical research traditions spanning three decades of brand theory.

## Discussion

### Theoretical Contribution

**We resolve the awareness-gate paradox by showing that maximal awareness is necessary but not sufficient for interference when observers operate near minimum-distortion encodings.** Standard portfolio theory [@keller-1993-conceptualizing-measuring-managing; @aaker-1990-consumer-evaluations-brand] treats the awareness gate as a scalar that amplifies interference when activated. For LLMs, the gate is permanently saturated ($\alpha \approx 1$), yet interference is absent. The resolution is that LLMs encode brand knowledge holistically: the solo profile already incorporates portfolio relationships implicitly. The gate amplifies an interference *term* that is structurally near zero, not an absent gate suppressing a nonzero term.

**Spectral immunity generalizes to 7 portfolio archetypes.** The original finding (4 archetypes, 4 portfolios, 10 models, 5 traditions) now extends to 7 archetypes, 7 portfolios, 13 models, and 7 traditions. L'Oreal's prestige spread, Yandex's branded house, and Geely's reverse aspiration all show the same immunity pattern as LVMH, Unilever, P&G, and Toyota in direct framing. The structural property holds regardless of portfolio type.

**Immunity is architectural, not knowledge-based.** All 7 model traditions show immunity. The Japanese model (GPT-OSS-Swallow) shows the only tradition-level significant effect (p = .011, d = -.63), driven primarily by Toyota-related brands, consistent with deeper Japanese automotive market knowledge. But this is one model, the effect does not survive tradition-level FDR correction, and it does not break the fundamental immunity pattern.

**The Lexus finding is suggestive but no longer statistically robust.** With 20 brands and FDR correction, the Lexus result (p = .004, d = .52) yields 0/20 FDR-significant results. Aspiration dynamics remain directionally suggestive---Lexus shows the largest positive $\Delta$ of any brand---but the evidence does not support concluding that aspiration dynamics are an exception to immunity. Future work should test this specifically with a dedicated aspiration-focused design.

**Reverse aspiration can be unlocked through conversational revelation but not direct framing.** The Geely Auto multi-turn finding (d = -1.11) is the strongest single effect in the experiment. In direct framing, Geely Auto shows a small non-significant increase in DCI when portfolio context is added. But in multi-turn conversation, when the model has established Volvo's premium perception in Turn 1 and then receives portfolio context in Turn 2, Geely Auto's DCI drops by 2.93 points. The mechanism appears to be conversational anchoring: Turn 1 establishes a premium anchor for the portfolio family, making Turn 2's framing more effective. This pattern does not appear for portfolios without the reverse-aspiration dynamic (LVMH, P&G), suggesting it is specific to ownership structures that violate the quality-hierarchy expectation.

**Native-language framing activates discourse layers but not systematically.** The native-language ablation reveals model-portfolio-specific sensitivity rather than a general amplification principle. The Japanese model's sensitivity to Japanese-language Toyota framing, and YandexGPT's sensitivity to Russian-language Yandex framing, suggest that home-language prompts activate different discourse registers in home-tradition models. But the effects are not unidirectional, not consistent across portfolios, and do not survive FDR correction. This is consistent with Zharnikov [-@zharnikov-2026-dimensional-collapse-ai-mediated-search]'s finding that cross-cultural differences in AI brand perception represent discourse-layer activation rather than systematic cultural bias.

### Managerial Contribution

**Portfolio architecture is invisible to AI across all archetype types.** As AI-mediated brand interactions grow---what Dubois, Dawson, and Jaiswal [-@dubois-2025-forget-what-you] term the "Share of Model" economy---portfolio strategies become irrelevant in these channels across all 7 archetypes tested. Prestige spread (L'Oreal), reverse aspiration (Geely), and branded house (Yandex) are as invisible to AI as symmetric interference structures.

**Shielding is automatic but amplification is impossible.** House-of-brands architecture shields brands from destructive interference automatically in AI perception. But constructive interference is equally blocked. The Yandex branded house---where shared naming maximally saturates the awareness gate---shows the same immunity as LVMH's house-of-brands architecture.

**Geely's reverse aspiration is a strategic vulnerability in conversational AI.** While direct portfolio framing leaves Volvo's positioning intact, multi-turn conversation reveals a meaningful effect: when users engage in extended dialogue about Geely's portfolio, Geely Auto's perceived differentiation collapses (d = -1.11). Brand managers with reverse-aspiration portfolio structures should anticipate that extended AI interactions about the portfolio can surface dynamics that are invisible in single-turn queries.

**The Lexus strategy remains an open empirical question.** The aspirational differentiation pattern (Lexus d = .52) is directionally consistent but not statistically robust after FDR correction with 20 brands. Portfolio managers pursuing vertical differentiation strategies (Toyota/Lexus, Volkswagen/Audi, Gap/Banana Republic) should treat AI-channel aspiration dynamics as warranting dedicated replication before acting on them.

**Brand coherence, not portfolio coherence, drives AI perception.** Brand identity explains 41.4% of DCI variance (portfolio plus brand within portfolio); condition explains under .01%, about four orders of magnitude less.

### Boundary Conditions and Limitations

First, as with any use of LLMs as research instruments [@stromberg-2025-blind-spots-broad-strokes], interpretive caveats apply: DCI is a new metric not yet validated against human perceptual data. The core finding---near-zero portfolio effects---is robust to this limitation (a null is a null regardless of the specific metric), but the theoretical interpretation in terms of rate-distortion compression depends on DCI's construct validity, which is the primary boundary condition on our conclusions. Validation against human brand perception data is the most important direction for future work.

Second, with 20 tests and FDR correction, the study has limited power to detect effects at the brand level (the Lexus finding would be significant under a per-comparison alpha). A dedicated within-archetype replication with larger samples would provide cleaner evidence.

Third, the multi-turn design uses a two-turn protocol; longer conversations with more gradual portfolio disclosure might accumulate larger effects.

Fourth, native-language results are based on a single model per tradition (except Western and Chinese), limiting the generalizability of tradition-level conclusions.

### Future Research

Four extensions are warranted. First, validation of DCI against human perceptual data to establish construct validity for the metric and the immunity finding. Second, a dedicated replication of the Lexus finding with a multi-brand aspirational layer panel (Toyota/Lexus, Volkswagen/Audi, Marriott/Ritz-Carlton) to determine whether d = .52 represents a real exception. Third, agentic simulations and extended multi-turn designs (5+ turns) to test whether conversational accumulation can unlock portfolio effects in non-reverse-aspiration portfolios. Fourth, longitudinal testing of whether spectral immunity is stable as models are updated or fine-tuned, which is critical for "Share of Model" strategy planning.

## Conclusion

This study provides the first comprehensive test of portfolio interference in LLM brand perception. Across 7,975 observations, 13 models from 7 training traditions, 7 portfolio archetypes, and 4 prompt modalities, the predominant finding is clear: portfolio framing does not systematically alter how LLMs perceive brands. We term this phenomenon *spectral immunity*. The mechanism is architectural---Russian, Indian, Japanese, European, and Korean models with different training corpora show identical immunity to Western models. The original Lexus finding (d = .52) is suggestive but FDR-inconclusive with the full 20-brand panel. The multi-turn Geely Auto finding (d = -1.11) is the strongest effect in the experiment, revealing that reverse aspiration can be unlocked through conversational revelation---but this is a conditional vulnerability, not a general exception to immunity. For brand managers, portfolio architecture is invisible to the AI systems increasingly mediating consumer-brand interactions. The exception is conversational AI with extended interaction: portfolios with reverse-aspiration structure show meaningful effects in multi-turn dialogue that are absent in single-turn queries.

*Falsification conditions:* The condition previously stated for spectral immunity (H5) conjoined six requirements---a panel of 7+ models from 3+ traditions, DCI shifts above 2.0 points, effect sizes above .50, survival of multiple-testing correction, and both of these across 5+ portfolio archetypes and 3+ prompt modalities, all simultaneously. A six-way conjunction is close to unfalsifiable in practice, and this study's own largest result already clears three of the six: the present panel is 13 models drawn from seven training traditions, the Swallow/Toyota native-language cell returns a DCI shift of $-2.35$, and the Japanese tradition-level effect behind it is $d = -.63$ (Table 4). What stops that cell from being a refutation is FDR correction and the absence of a pattern across archetypes---which are two conjuncts, not six. The condition is therefore restated on the two that carry the content.

Spectral immunity (H5) is falsified if a study using the present design and a comparable panel finds portfolio-induced $|\Delta\mathrm{DCI}|$ above the $\pm 1.0$ TOST bound for more than half the brands tested, with those tests FDR-significant at $\alpha$ = .05. A narrower result also refutes immunity as a general property, though not for the remaining archetypes: any single portfolio archetype in which every brand shows an FDR-significant shift above the bound. Neither condition requires agreement across modalities or archetypes, and either could be produced by a single well-powered replication.

## Data Availability

Experiment data (7,975 observations) are archived at https://doi.org/10.57967/hf/11560 (HuggingFace). The archived multi-turn records hold both the Turn 1 and the Turn 2 ratings behind Table 6; the raw response files are in the public repository at https://github.com/spectralbranding/sbt-papers/tree/main/r20-portfolio-ai/responses. Source code and analysis scripts are available at https://doi.org/10.5281/zenodo.19555282. The dataset contains 2,555 direct-rating observations, 2,518 recommendation-prompt observations, 1,235 multi-turn conversation observations, 1,322 native-language ablation observations, and 345 prompt-location ablation observations across 13 models from 7 training traditions. Local model experiments were conducted on Apple Mac mini M4 Pro (48 GB RAM) running Ollama v0.20.0.

## Acknowledgments

AI assistants (Claude Opus 4.8, Grok 4.20, Gemini 2.5 Pro) were used for initial literature search, for software development — authoring the experiment harness and the analysis and scoring scripts — and for orchestrating and running the reported experiments through those scripts, as well as for editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

## Author Contributions (CRediT)

Dmitry Zharnikov: Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Project administration, Software, Validation, Writing — original draft, Writing — review and editing.

## References

::: {#refs}
:::
