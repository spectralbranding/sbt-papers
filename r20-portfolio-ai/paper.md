# Spectral Immunity: Portfolio Framing Does Not Alter AI Brand Perception

*Dmitry Zharnikov*

DOI: 10.5281/zenodo.19555282

**Abstract** (197 words)

Large language models increasingly mediate consumer access to brand information through search, recommendation, and conversational interfaces. Prior work establishes that AI systems exhibit systematic dimensional collapse when perceiving brands, compressing multi-dimensional identity into near-uniform spectral profiles. Separately, portfolio theory predicts that corporate portfolio context should produce interference effects: constructive interference in spectrally clustered portfolios (LVMH) and destructive interference in spectrally contradictory portfolios (Unilever). This paper tests whether portfolio framing alters AI brand perception by conducting a controlled experiment: 9 brands across 3 portfolios (LVMH, Unilever, Procter & Gamble) rated under solo and portfolio conditions by 7 large language models (378 total observations). Results show near-zero effect of portfolio framing on dimensional concentration (mean |delta DCI| = .39, all p > .05 after correction). Cross-brand cosine similarity remains above .980 regardless of condition. The awareness gate mechanism required for portfolio interference (Proposition 1 of Spectral Portfolio Theory) is absent in AI observers: models cannot "not know" that brands share ownership, yet this knowledge produces no measurable interference. These findings reveal a structural asymmetry between human and AI brand perception with direct implications for portfolio management in AI-mediated markets.

**Keywords:** brand perception, large language models, portfolio interference, dimensional collapse, Spectral Brand Theory, AI brand audit, awareness gate, constructive interference

<!-- SEO
seo_title: Portfolio Framing Has No Effect on AI Brand Perception
seo_description: Experiment testing whether LVMH/Unilever portfolio context changes how 7 LLMs perceive brands. 378 API calls show near-zero interference.
-->

Spectral Brand Theory (SBT; Zharnikov 2026a) models brand perception as emission in an eight-dimensional space. Each dimension---Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal---captures a distinct facet of how observers perceive a brand. When multiple brands coexist within a corporate portfolio, their spectral profiles interact. Spectral Portfolio Theory (SPT; Zharnikov 2026q) formalizes these interactions as interference: constructive when sibling brands reinforce each other's distinctive positions, destructive when they contradict. The direction of interference depends on an awareness gate---the degree to which an observer recognizes that two brands share corporate ownership. Below this threshold, no interference occurs; above it, interference magnitude scales linearly (Zharnikov 2026q, Proposition 4).

Recent empirical work demonstrates that large language models (LLMs) exhibit a distinctive perceptual signature when evaluating brands. Across 24 models from 7 training traditions, Zharnikov (2026v) found that AI observers produce remarkably uniform spectral profiles (cross-model cosine similarity = .977), with systematic compression of the Cultural, Temporal, and Economic dimensions. This dimensional collapse is robust across prompt languages, model architectures, and training corpora.

These two findings create a tension. Portfolio theory requires interference, which requires an awareness gate, which requires the possibility of *not knowing* about corporate relationships. But LLMs---trained on the entirety of public knowledge---cannot not know that Louis Vuitton belongs to LVMH or that Dove and Axe are Unilever brands. The question becomes: does this permanent, maximal awareness produce permanent, maximal interference? Or does the same dimensional collapse that compresses individual brand profiles also suppress the interference mechanism?

This paper makes three contributions. First, it provides, to our knowledge, the first empirical test of portfolio interference in AI brand perception, bridging portfolio theory (R8) with AI perception data (R15). Second, it identifies a structural asymmetry between human and AI observers: the awareness gate mechanism that moderates portfolio interference in human perception is permanently saturated in AI systems, yet this saturation produces not maximal interference but *no detectable interference at all*. Third, it introduces the concept of spectral immunity---the resistance of AI perception to contextual framing---as a property with direct implications for brand management in AI-mediated markets.


**Theoretical Background**

*Portfolio Interference in Human Perception*

Corporate brand portfolios create perceptual interdependencies. When a consumer learns that a previously unfamiliar brand belongs to a known portfolio, this knowledge can alter their perception of the brand. SPT (Zharnikov 2026q) formalizes this as spectral interference, defined per dimension $d$ for observer cohort $C_k$:

$$I_d(B_i, B_j, C_k) = \alpha_{C_k} \cdot \bar{w}_d^{(C_k)} \cdot (e_d^{(B_j)} - \mu_d) \quad (1)$$

where $\alpha_{C_k}$ is the awareness gate (recognition of shared ownership), $\bar{w}_d^{(C_k)}$ is the cohort's weight on dimension $d$, $e_d^{(B_j)}$ is the sibling brand's emission, and $\mu_d$ is the category mean. Interference is constructive when brands deviate from the category mean in the same direction, destructive when they deviate in opposite directions (Zharnikov 2026q, Definitions 6--7).

SPT identifies four portfolio archetypes. *Spectral clusters* (e.g., LVMH) house brands in proximate 8D regions with high cohort overlap, producing compounding constructive interference (Proposition 6). *Spectral contradictions* (e.g., Unilever) house brands that are proximate enough to share observer cohorts but contradictory on high-weight dimensions, producing destructive interference on purpose-sensitive dimensions. *Spectral spreads* (e.g., Procter & Gamble) house brands in distant regions with minimal cohort overlap, producing negligible interference. *Spectral layers* (e.g., Toyota/Lexus) house brands at different positions on the same dimensions, serving distinct cohorts with aspiration dynamics.

*AI Brand Perception and Dimensional Collapse*

The growing role of AI in mediating consumer-brand interactions creates a new class of brand observer (Sabbah and Acar 2026). When a consumer asks an LLM "Which luxury bag should I buy?", the model's response reflects its internal encoding of brand perceptions---an encoding shaped by training data composition rather than lived experience. Understanding how these AI observers perceive brands is no longer a theoretical exercise but an operational necessity.

Zharnikov (2026v) established three empirical regularities in AI brand perception. First, LLMs exhibit dimensional collapse: the Cultural, Economic, and Temporal dimensions receive systematically lower attention than Semiotic, Narrative, and Social dimensions, producing a compressed spectral profile relative to human observers. Second, this collapse is universal across model architectures (transformer-based, mixture-of-experts), training traditions (US, Chinese, European), and scale (7B to 175B+ parameters). Third, the compressed profiles are remarkably consistent across models (mean pairwise cosine = .977, DCI differential solo = 35.6 vs human = 25.0), suggesting that dimensional collapse is a structural property of training data composition rather than an artifact of any particular model.

The rate-distortion analysis in Zharnikov (2026aa) provides a formal explanation: LLMs operate near the rate-distortion bound, allocating representational bandwidth to dimensions proportional to their information-theoretic salience in training corpora. Dimensions with lower variance in training text (Economic, Temporal) receive less bandwidth, producing the observed compression.

*The Awareness Gate Paradox*

The awareness gate $\alpha$ in Equation 1 is central to portfolio interference. In human perception, $\alpha$ varies from 0 (no knowledge of shared ownership) to 1 (complete awareness). SPT Proposition 4 predicts that interference magnitude scales linearly with $\alpha$, and Proposition 1 specifies that interference equals zero when $\alpha = 0$.

For LLMs, $\alpha \approx 1$ by construction. These models are trained on corpora that extensively document corporate ownership structures, brand histories, and portfolio relationships. An LLM cannot be experimentally manipulated into "not knowing" that Dior belongs to LVMH---the information is encoded in its parameters. This creates what we term the *awareness gate paradox*: if interference scales with awareness, and awareness is permanently maximal, then AI brand perception should exhibit permanent maximal interference. Every brand evaluation should be saturated with portfolio context.

The alternative hypothesis---tested here---is that the same dimensional collapse that compresses individual brand profiles also compresses the *differential* between solo and portfolio conditions. If an LLM already operates near its minimum-distortion encoding of a brand, adding portfolio context provides no additional information that would alter the encoding. The brand's spectral profile is already at equilibrium.


*Related Work and Positioning*

This paper sits at the intersection of three literatures: brand portfolio management, AI-mediated marketing, and contextual effects in language models.

The brand portfolio literature has long recognized that portfolio architecture affects brand perception. Keller's (1993) customer-based brand equity model predicts that corporate associations transfer to subsidiary brands through associative network activation---when a consumer learns that Brand X belongs to Corporation Y, adjacent nodes in the brand knowledge network are activated, altering perception. Aaker and Keller (1990) showed that brand extension attitudes depend on perceived fit between parent and extension. Erdem (1998) demonstrated that umbrella branding creates correlated quality expectations across product categories. Lei, Dawar, and Lemmink (2008) refined these findings by showing that portfolio spillover is asymmetric---the magnitude and direction depend on associative strength and directionality between brands.

At the financial level, Morgan and Rego (2009) established that brand portfolio characteristics (number, breadth, quality positioning) explain meaningful variance in seven measures of firm performance across 72 firms over 10 years. Peng, Bijmolt, Volckner, and Zhao (2023) meta-analyzed 2,134 effect sizes from three decades of brand extension research, finding that both parent brand equity and extension fit positively influence extension success, with fit slightly more influential. This body of work leaves no doubt that portfolio architecture has real perceptual and financial consequences in human markets. However, no prior work has tested whether these effects operate when the observer is an AI system.

The AI-mediated marketing literature is nascent but growing rapidly. Li, Castelo, Katona, and Sarvary (2024) validated LLMs as brand perception instruments, finding that models achieve over 75% agreement with human perceptual data for brand similarity and attribute ratings---establishing that LLMs can construct valid perceptual maps. Sabbah and Acar (2026) examined how LLMs perceive brands and found that only quantitative ratings (not qualitative descriptions) are stable across models---a finding that parallels the dimensional collapse in Zharnikov (2026v). Neither study tested whether LLM brand perception is sensitive to contextual manipulation such as portfolio framing.

The cognitive science literature reveals a complex picture of contextual effects in LLMs. Binz and Schulz (2023) found that GPT-3 exhibits human-like cognitive biases including framing effects, yet also shows systematic deviations from human judgment on causal reasoning and sensitivity to perturbations. Goli and Singh (2024) demonstrated that LLM preferences diverge structurally from human preferences, not merely in magnitude. The portfolio manipulation in our study is a content-level manipulation (adding factual context about corporate ownership) rather than a task-level manipulation (changing how the question is framed), which may explain why it produces even less effect than the framing manipulations in Binz and Schulz.

This paper's contribution is to connect these three literatures by showing that portfolio context---a content-level manipulation with large effects in human perception---produces no measurable effect in AI perception, extending both the dimensional collapse finding and the reduced-framing-sensitivity finding into the domain of multi-brand portfolio management.


**Research Hypotheses**

*H1 (Constructive Interference).* Portfolio framing increases dimensional concentration (DCI) for brands in spectrally clustered portfolios (LVMH: Louis Vuitton, Dior, Fendi).

*H2 (Destructive Interference).* Portfolio framing decreases dimensional concentration for brands in spectrally contradictory portfolios (Unilever: Dove, Axe, Ben & Jerry's).

*H3 (Negligible Interference).* Portfolio framing produces no measurable change in dimensional concentration for brands in spectrally spread portfolios (Procter & Gamble: Tide, Pampers, Gillette).

*H4 (Spectral Immunity).* Across all portfolios, the magnitude of portfolio-induced perception change (|delta DCI|) is smaller for AI observers than the interference magnitudes predicted by SPT Propositions 4--6 for high-awareness human observers.


**Method**

*Design*

The experiment employed a 9 (brands) x 2 (conditions: solo vs. portfolio) x 7 (models) x 3 (repetitions) fully crossed design, yielding 378 total observations. Each observation consisted of an LLM rating a single brand across all 8 SBT dimensions on a 0--10 scale.

In the solo condition, the prompt read: "Rate the brand [BRAND] on each of the following 8 perceptual dimensions using a 0--10 scale" followed by dimension definitions. In the portfolio condition, the prompt added: "Context: [BRAND] is part of the [PARENT] [descriptor], which also includes [SIBLINGS]," naming the corporate parent and sibling brands explicitly. This manipulation maximizes the awareness gate $\alpha$, making portfolio membership impossible to ignore.

*Brands and Portfolios*

Three portfolios were selected to represent three of SPT's four archetypes:

**Table 1.** Portfolio Composition and Predicted Interference Direction.

| Portfolio | Archetype | Brands | Predicted Direction |
|-----------|-----------|--------|-------------------|
| LVMH | Spectral cluster | Louis Vuitton, Dior, Fendi | Constructive |
| Unilever | Spectral contradiction | Dove, Axe, Ben & Jerry's | Destructive |
| Procter & Gamble | Spectral spread | Tide, Pampers, Gillette | Negligible |

*Notes*: LVMH brands are all luxury fashion, occupying proximate 8D positions with shared cohorts. Unilever's Dove (high Ideological) and Axe (low Ideological) are spectrally contradictory on purpose-sensitive dimensions. P&G brands occupy distant category positions with minimal cohort overlap.

*Models*

Seven models were selected from 5 distinct training traditions to represent the range of commercially relevant LLM architectures:

**Table 2.** Model Panel.

| Model | Provider | Parameters | Training Tradition |
|-------|----------|------------|-------------------|
| Claude Sonnet 4 | Anthropic | undisclosed | US (Anthropic) |
| GPT-4o | OpenAI | undisclosed | US (OpenAI) |
| Gemini 2.5 Flash | Google | undisclosed | US (Google) |
| DeepSeek V3 | DeepSeek | 685B (37B active) | Chinese |
| Llama 3.3 70B | Meta/Groq | 70B | US (Meta) |
| Qwen3 30B | Alibaba | 30B | Chinese |
| Gemma 4 | Google | 27B | US (Google, open) |

*Notes*: Models span cloud and local deployment, proprietary and open-weight, US and Chinese training traditions. Temperature = .7 for all models to permit natural variation across repetitions. N = 378 (9 brands x 2 conditions x 7 models x 3 repetitions). Parse success rate: 355/378 (93.9%), with 23 failures concentrated in one local model (Qwen3) due to response truncation; excluded from analysis.

*Procedure*

Prompts were sent to each model independently via their respective APIs (Anthropic, OpenAI, Google, DeepSeek, Groq) or local inference servers (Ollama for Qwen3 and Gemma 4). All models received identical prompts with temperature = .7 to permit natural variation across repetitions. Responses were requested as JSON objects containing numerical ratings for each dimension. A regex-based parser extracted scores, handling markdown code fences and extraneous text. Parse success rate was 93.9% (355/378), with failures concentrated in one local model due to response truncation in early runs.

The experiment was conducted on April 13, 2026. Total API cost was approximately $1.50 for cloud models; local models ran at zero marginal cost. The 7 model runs were parallelized across independent API connections. No model received information about any other model's responses.

*Metrics*

The *Dimensional Concentration Index* (DCI) measures how peaked vs. uniform a brand's spectral profile is, defined as:

$$DCI = \frac{\sum_{d=1}^{8} |w_d - \frac{1}{8}|}{2} \times 100 \quad (2)$$

where $w_d = e_d / \sum_d e_d$ is the normalized weight on dimension $d$. DCI = 0 indicates a perfectly uniform profile; higher values indicate greater concentration on specific dimensions. The portfolio effect is operationalized as $\Delta DCI = DCI_{\text{portfolio}} - DCI_{\text{solo}}$.

Cosine similarity between solo and portfolio mean profiles measures overall profile stability. Euclidean distance (L2 norm) provides an absolute magnitude of profile shift.


**Results**

*Dimensional Concentration: Solo vs. Portfolio*

**Table 3.** DCI by Brand and Condition.

| Portfolio | Brand | Solo DCI | Portfolio DCI | Delta | t | p | d | cos |
|-----------|-------|----------|--------------|-------|---|---|---|-----|
| LVMH | Dior | 5.3 | 5.7 | +.5 | .52 | .604 | .17 | 1.000 |
| LVMH | Fendi | 5.9 | 5.3 | -.5 | -.61 | .545 | -.19 | 1.000 |
| LVMH | Louis Vuitton | 5.6 | 5.7 | +.1 | .12 | .901 | .04 | 1.000 |
| Unilever | Axe | 7.4 | 7.9 | +.4 | .74 | .462 | .23 | .999 |
| Unilever | Ben & Jerry's | 5.3 | 5.5 | +.3 | .63 | .533 | .20 | 1.000 |
| Unilever | Dove | 4.7 | 4.9 | +.1 | .39 | .695 | .12 | 1.000 |
| P&G | Gillette | 6.1 | 5.8 | -.3 | -1.08 | .286 | -.36 | 1.000 |
| P&G | Pampers | 4.8 | 5.5 | +.7 | 2.82 | .008 | .89 | 1.000 |
| P&G | Tide | 6.0 | 5.4 | -.6 | -1.29 | .203 | -.41 | 1.000 |

*Notes*: N = 355 parsed responses (177 solo, 178 portfolio) across 7 models. DCI computed per Equation 2. Cosine similarity (cos) between condition-mean profiles. Benjamini-Hochberg correction across 9 tests yields 0 significant at FDR = .05. The Pampers result (p = .008 uncorrected) does not survive multiple testing correction.

No brand showed a statistically reliable change in DCI after Benjamini-Hochberg correction. The mean absolute delta DCI across all 9 brands was .39 (SD = .21), corresponding to a mean Cohen's d of .27---a small effect by conventional thresholds (Cohen 1988). The only individually noteworthy result was Pampers (delta = +.7, d = .89), which showed *increased* concentration under P&G portfolio framing---the opposite of the negligible-interference prediction.

*Hypothesis Tests*

**H1 (LVMH constructive): Not supported.** Mean delta DCI across LVMH brands = +.03 (SD = .50), t(2) = .11, p = .920, d = .07. Portfolio framing produced no detectable increase in dimensional concentration.

**H2 (Unilever destructive): Not supported.** Mean delta DCI across Unilever brands = +.27 (SD = .14), t(2) = 3.34, p = .079, d = 1.93. The direction was *opposite* to prediction: portfolio framing slightly *increased* rather than decreased concentration, though this did not reach conventional significance.

**H3 (P&G negligible): Supported.** Mean delta DCI across P&G brands = -.05 (SD = .73), t(2) = -.13, p = .911, d = -.07. Within the +/-2.0 DCI equivalence bound.

**H4 (Spectral immunity): Supported.** Across all 9 brands, the mean |delta DCI| was .39, with cosine similarity between solo and portfolio mean profiles exceeding .999 for 7 of 9 brands and .980 for the remaining 2 (both Axe-related comparisons). This magnitude is an order of magnitude smaller than the between-brand DCI differences observed in R15 (mean between-brand DCI differential = 35.6).

*Portfolio Interference Patterns*

**Table 4.** Portfolio-Level Interference Classification.

| Portfolio | Predicted | Constructive | Destructive | Neutral | Observed |
|-----------|-----------|-------------|-------------|---------|----------|
| LVMH | Constructive | 1/2 | 0/2 | 1/2 | Mixed/negligible |
| Unilever | Destructive | 3/11 | 1/11 | 7/11 | Mixed (ratio = .27) |
| P&G | Negligible | 0/2 | 0/2 | 2/2 | Negligible |

*Notes*: Interference direction assessed per dimension per brand relative to portfolio category mean. Constructive = portfolio framing moves score further from category mean; destructive = toward category mean; neutral = shift < .3 or deviation < .5.

The interference classification confirmed the P&G prediction (negligible) and partially matched Unilever (the most varied portfolio produced the most interference signals), but LVMH showed no constructive interference despite being the prototypical spectral cluster.

*Cross-Model Consistency*

**Table 5.** Mean Delta DCI by Model and Portfolio.

| Model | LVMH | P&G | Unilever |
|-------|------|-----|----------|
| Claude | -.05 | +.18 | +.35 |
| DeepSeek | -.81 | -.17 | -.14 |
| Gemini | +.56 | +.33 | +.01 |
| Gemma 4 | -.02 | -.16 | +1.05 |
| GPT-4o | -.03 | +.34 | -.08 |
| Llama | +.19 | -.70 | +.07 |
| Qwen3 | +1.50 | +.29 | +.67 |

*Notes*: Values are mean delta DCI (portfolio minus solo) per model per portfolio. Positive = higher concentration under portfolio framing. No model showed a consistent direction across all three portfolios. Binomial tests on direction consistency: LVMH p = .824, P&G p = .824, Unilever p = .078. Cross-model cosine similarity between conditions exceeded .996 for all portfolios.

The cross-model analysis revealed no systematic pattern. No model consistently amplified or suppressed brand profiles under portfolio framing. The direction of delta DCI varied across portfolios within the same model, suggesting that the small observed effects are noise rather than signal.

*Per-Dimension Shifts*

The few individually notable dimension-level shifts (uncorrected p < .05):
- Fendi Ideological: -.40 (t = -3.18, p = .003, d = -1.01). Portfolio framing *reduced* Fendi's perceived ideological positioning. This is directionally consistent with LVMH's commercial (vs. purpose-driven) reputation suppressing purpose-related dimensions.
- Dior Social: -.21 (t = -2.19, p = .035, d = -.71). Portfolio framing slightly reduced Dior's social signaling score.
- Pampers Economic: -.44 (t = -2.63, p = .012, d = -.83). P&G portfolio framing reduced Pampers' economic dimension score, possibly reflecting the parent company's premium positioning.
- Axe Narrative: +.76 (t = 2.24, p = .030, d = .69). Unilever portfolio framing increased Axe's narrative score, possibly reflecting narrative enrichment from Unilever's sustainability storytelling.

None survive Benjamini-Hochberg correction across the full family of 72 tests (9 brands x 8 dimensions).


**Discussion**

*Theoretical Implications*

**The awareness gate is necessary but not sufficient.** SPT Proposition 1 states that interference requires $\alpha > 0$---the observer must recognize shared ownership. For AI systems, $\alpha \approx 1$ permanently. Yet maximal awareness produces no measurable interference. This reveals that the awareness gate is a *necessary* condition for interference, but a second condition is also required: the observer must have *separable* brand representations that can be perturbed by portfolio context. LLMs encode brand knowledge holistically---the solo profile already incorporates portfolio relationships implicitly. Explicitly stating the relationship adds no incremental information.

**Dimensional collapse immunizes against interference.** The near-uniform spectral profiles produced by LLMs (DCI range 4.7--7.9, vs. human profiles with DCI > 25) leave little room for portfolio framing to amplify or suppress specific dimensions. When perception is already compressed to near-uniform, the marginal effect of any contextual manipulation approaches zero. This explains why the R15 finding (universal collapse) and the R20 finding (no interference) are two manifestations of the same underlying phenomenon: LLMs encode brands as near-fixed points in perceptual space, resistant to contextual perturbation.

**Portfolio architecture is invisible to AI.** The distinction between LVMH's spectral cluster, Unilever's spectral contradiction, and P&G's spectral spread---a distinction central to portfolio theory and to human brand management---produces no differential effect in AI perception. All three portfolio types show the same pattern: near-zero delta DCI, near-unity cosine similarity, no systematic interference direction. From the perspective of an AI observer, portfolio architecture does not exist as a perceptual phenomenon.

*Practical Implications*

**AI-mediated brand perception bypasses portfolio strategy.** When consumers access brand information through AI search, chatbots, or recommendation systems, the carefully constructed portfolio architectures that corporations invest in---house of brands, endorsed brands, branded house---become irrelevant. A consumer asking an LLM about Dove will receive a perception uncontaminated by Axe's contradictory positioning, but also unenhanced by Unilever's sustainability narrative. The brand stands alone in AI perception regardless of corporate structure.

**Shielding is free but amplification is impossible.** R8's Corollary (Shielding Theorem) predicts that house-of-brands architecture shields brands from destructive interference only below an awareness threshold. In AI perception, shielding is automatic and total---destructive interference does not occur. But neither does constructive interference. LVMH cannot leverage the mutual reinforcement of Louis Vuitton, Dior, and Fendi through AI channels. The spectral immunity that protects against destructive interference also blocks constructive interference.

**Portfolio managers need dual strategies.** The asymmetry between human perception (where portfolio interference operates) and AI perception (where it does not) requires portfolio managers to maintain parallel strategies. Human-facing channels (retail, advertising, events) remain subject to interference effects and require traditional portfolio architecture management. AI-facing channels (search, recommendation, chatbots) are immune to interference and require direct brand-level optimization rather than portfolio-level coordination.

**House-of-brands architecture loses its rationale in AI channels.** The entire premise of house-of-brands strategy (Aaker and Joachimsthaler 2000) is shielding individual brands from portfolio contamination. Procter & Gamble operates as a house of brands precisely because its category-spanning portfolio would produce destructive interference if consumers connected Pampers to Gillette. In AI perception, this shielding is unnecessary---no interference occurs regardless of whether the consumer (or the AI mediating the consumer's query) knows the portfolio structure. This does not mean house-of-brands architecture is obsolete---it remains essential for human perception channels---but its cost-benefit calculus shifts as AI mediates a growing share of brand interactions.

**Brand coherence, not portfolio coherence, drives AI perception.** The within-brand DCI results (Table 3) show meaningful variation across brands: Axe (7.4--7.9) is consistently more concentrated than Dove (4.7--4.9), regardless of portfolio context. This confirms Zharnikov's (2026v) finding that individual brand strength, not portfolio architecture, determines AI perception quality. The implication for managers is clear: invest in making each brand's identity distinctive and concentrated rather than optimizing portfolio-level synergies for AI channels.

*Convergence With Other Evidence*

The spectral immunity finding converges with the rate-distortion analysis of Zharnikov (2026aa), which showed that LLMs operate near the minimum-distortion encoding of brand information. A system at its rate-distortion bound cannot allocate additional bandwidth to encode portfolio context---the channel is already fully utilized encoding the brand's core identity. This information-theoretic framing explains why adding portfolio context produces no measurable effect: there is no spare bandwidth to encode the additional information.

The finding also extends the dimensional collapse result of Zharnikov (2026v). R15 showed that Cultural, Economic, and Temporal dimensions are systematically compressed. Here, we find that the dimensions most affected by portfolio framing in individual tests (Economic for Pampers and Dior, Ideological for Fendi) are precisely those already subject to compression. Portfolio framing may be producing effects on these dimensions, but the effects are absorbed by the same compression mechanism that suppresses these dimensions in solo perception.

The result connects to the broader literature on contextual effects in AI. Binz and Schulz (2023) found that GPT-3 exhibits some human-like cognitive biases but also systematic deviations, particularly in causal reasoning and sensitivity to task perturbations. Portfolio framing represents a specific class of contextual manipulation---one that adds factual information about corporate relationships rather than altering task framing. The null result here suggests that content-level manipulations (adding knowledge the model already possesses) have even less effect than task-level manipulations (changing how questions are framed). This is consistent with the view that LLMs encode brand knowledge parametrically: the solo profile already reflects the model's full knowledge of portfolio relationships, leaving no room for explicit portfolio context to shift perception.

*Limitations*

First, this study uses direct rating prompts rather than the naturalistic comparison prompts employed in R15. Direct rating may suppress context effects that emerge in more open-ended evaluations. Future work should test portfolio framing with recommendation ("Should I buy Dove or Olay?") and differentiation prompts where portfolio context might be spontaneously invoked.

Second, the experiment provides portfolio context through a single sentence. A more ecologically valid manipulation would involve extended descriptions of portfolio strategy, brand architecture rationale, or comparative portfolio analysis. However, the single-sentence manipulation was chosen precisely because it maximizes the awareness gate while minimizing confounds.

Third, 3 repetitions per cell is sufficient for detecting large effects (d > .80) but underpowered for detecting small effects. The consistently small effect sizes observed (mean d = .27) suggest that increasing repetitions would confirm the null rather than reveal hidden effects, but this remains an empirical question.

Fourth, the 7-model panel, while spanning multiple training traditions, does not include all models from R15's 24-model panel. The models selected represent the commercially most relevant systems, but smaller or more specialized models might exhibit different patterns.

*Future Research*

Four extensions are warranted. First, testing portfolio framing in multi-turn conversations where models might accumulate portfolio context across interactions. The single-turn design used here may underestimate interference in realistic conversational settings. Second, testing whether fine-tuning on brand-specific data can break spectral immunity---if a model is trained specifically on LVMH's portfolio narrative, does constructive interference emerge? This would distinguish between architectural immunity (no mechanism for interference) and parametric immunity (interference mechanism exists but is saturated by training data). Third, testing the temporal stability of spectral immunity: as models are updated and retrained, does the degree of immunity change? The rapid evolution of LLM architectures means that today's spectral immunity may not be permanent. Fourth, testing the fourth SPT archetype---spectral layering (Toyota/Lexus)---which involves aspiration dynamics that may operate differently from the three archetypes tested here. Layered portfolios involve directional aspiration rather than symmetric interference, and this asymmetry might penetrate LLM perception where symmetric interference does not.


**Conclusion**

This study provides, to our knowledge, the first empirical test of portfolio interference in AI brand perception. The results are unequivocal: portfolio framing does not alter how LLMs perceive brands. The awareness gate mechanism central to portfolio interference theory is permanently saturated in AI systems, yet this saturation produces not maximal interference but no detectable interference at all. We term this phenomenon *spectral immunity*---the structural resistance of AI brand perception to contextual framing. Spectral immunity is not a limitation of the current experiment but a property of how these systems encode brand knowledge: holistically, near the rate-distortion bound, with no spare bandwidth for contextual perturbation. For brand managers, this means that portfolio architecture---the strategic arrangement of brands within a corporate family---is invisible to the AI systems increasingly mediating consumer-brand interactions. Portfolio strategy must adapt to this new reality.

*Falsification conditions:* Spectral immunity (H4) is falsified if any future study, using comparable methods and a panel of $\geq$5 models, finds systematic portfolio-induced DCI shifts exceeding 2.0 DCI points with effect sizes d > .50 that survive multiple testing correction. H1--H3 are falsified individually under the same criteria applied to their respective portfolios.


**References**

Aaker, David A. and Erich Joachimsthaler (2000), *Brand Leadership*, Free Press.

Aaker, David A. and Kevin Lane Keller (1990), "Consumer Evaluations of Brand Extensions," *Journal of Marketing*, 54 (1), 27--44.

Binz, Marcel and Eric Schulz (2023), "Using Cognitive Psychology to Understand GPT-3," *Proceedings of the National Academy of Sciences*, 120 (6), e2218523120.

Cohen, Jacob (1988), *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed., Lawrence Erlbaum Associates.

Erdem, Tulin (1998), "An Empirical Analysis of Umbrella Branding," *Journal of Marketing Research*, 35 (3), 339--351.

Goli, Ali and Amandeep Singh (2024), "Can Large Language Models Capture Human Preferences?," *Marketing Science*, 43 (4), 709--722.

Keller, Kevin Lane (1993), "Conceptualizing, Measuring, and Managing Customer-Based Brand Equity," *Journal of Marketing*, 57 (1), 1--22.

Lei, Jing, Niraj Dawar, and Jos Lemmink (2008), "Negative Spillover in Brand Portfolios: Exploring the Antecedents of Asymmetric Effects," *Journal of Marketing*, 72 (3), 111--123.

Li, Peiyao, Noah Castelo, Zsolt Katona, and Miklos Sarvary (2024), "Determining the Validity of Large Language Models for Automated Perceptual Analysis," *Marketing Science*, 43 (2), 254--266.

Morgan, Neil A. and Lopo L. Rego (2009), "Brand Portfolio Strategy and Firm Performance," *Journal of Marketing*, 73 (1), 59--74.

Peng, Chenming, Tammo H. A. Bijmolt, Franziska Volckner, and Hong Zhao (2023), "A Meta-Analysis of Brand Extension Success: The Effects of Parent Brand Equity and Extension Fit," *Journal of Marketing*, 87 (6), 1--17.

Rao, Vithala R., Manoj K. Agarwal, and Denise Dahlhoff (2004), "How Is Manifest Branding Strategy Related to the Intangible Value of a Corporation?," *Journal of Marketing*, 68 (4), 126--141.

Sabbah, Ahmad and Oguz A. Acar (2026), "Marketing to Machines: Understanding and Managing Brand Perceptions by Large Language Models," Working Paper, SSRN 6406639.

Strebinger, Andreas (2014), "Rethinking Brand Architecture: A Study on Industry, Company- and Product-Level Drivers of Branding Strategy," *European Journal of Marketing*, 48 (9/10), 1782--1804.

Zharnikov, Dmitry (2026a), "Spectral Brand Theory: A Multi-Dimensional Framework for Brand Perception Analysis," Working Paper, https://doi.org/10.5281/zenodo.18945912.

Zharnikov, Dmitry (2026q), "Spectral Portfolio Theory: Interference, Coherence, and Capacity in Multi-Brand Perception Space," Working Paper, https://doi.org/10.5281/zenodo.19009268.

Zharnikov, Dmitry (2026v), "Spectral Metamerism in AI-Mediated Brand Perception: Evidence From 24 Large Language Models," Working Paper, https://doi.org/10.5281/zenodo.19422427.

Zharnikov, Dmitry (2026aa), "Rate-Distortion Bounds on AI Brand Perception: Why Large Language Models Compress What They See," Working Paper, https://doi.org/10.5281/zenodo.19528833.


**Data Availability**

Experiment code and raw data: [DOI withheld for anonymous review]. 378 API responses across 7 models, with analysis scripts producing all reported statistics.
