# Spectral Immunity: Why Brand Portfolio Interference Disappears for AI Observers

*Dmitry Zharnikov*

Working Paper -- April 2026 -- DOI: [10.5281/zenodo.19765401](https://doi.org/10.5281/zenodo.19765401)

**Abstract**

Brand portfolio theory predicts perceptual interference when observers recognize shared corporate ownership. This interference is theorized to require only an open awareness gate. Large language models (LLMs), whose training data permanently saturate this gate, offer a critical test. If interference scales with awareness, LLMs should exhibit maximal spillover; if brand encodings are already compressed to minimum distortion, portfolio context should produce none. We formalize spectral interference across eight perceptual dimensions and test three propositions with 13 LLMs from seven training traditions, 40 brands, seven portfolio archetypes, and four prompt modalities (N = 9,925 observations). Using the Dimensional Concentration Index and TOST equivalence testing, we find near-zero portfolio-induced change (mean |ΔDCI| = .26; equivalence holds for 18/20 brands). The sole exception -- Geely Auto in multi-turn conversation (d = -1.11) -- emerges only when extended context converts coordination information into output inferences. Variance decomposition attributes just 0.1% of perceptual concentration to portfolio framing versus 37.4% to brand identity. These results resolve the awareness-gate paradox: awareness is necessary but insufficient. A second bandwidth constraint is required to propagate portfolio (DO-layer) information into observable brand profiles (WHAT-layer). General-purpose LLMs privilege output specification and are rationally inattentive to organizational coordination. As AI mediation of consumer-brand interactions grows, portfolio architecture becomes strategically invisible to this observer class, shifting managerial investment from orchestration to individual brand specification.

**Keywords:** spectral immunity, brand portfolio, awareness gate, portfolio interference, large language models, TOST equivalence, cross-cultural AI, Spectral Brand Theory

---

Brand portfolio theory has since Aaker and Joachimsthaler (2000) classified portfolios by architecture -- how brands are organized by the firm -- without formalizing how brands interact in the observer's perception space. A consumer who discovers that Dove and Axe share a parent entity may experience a shift in brand perception: Axe's historically objectifying advertising may contaminate Dove's empowerment positioning. Keller (1993) formalized this through customer-based brand equity, where corporate associations transfer to subsidiary brands via associative network activation. Erdem and Sun (2002) modeled the mechanism as umbrella signaling, showing that advertising signals from one product under an umbrella brand affect beliefs about siblings. Lei, Dawar, and Lemmink (2008) demonstrated that portfolio spillover is asymmetric: negative effects propagate more strongly from weaker to stronger brands.

The *awareness gate* is the central moderator in all existing accounts. Interference requires the observer to recognize shared corporate ownership. For LLMs -- an increasingly consequential class of brand observer (Li et al. 2024; Brand, Israeli, and Ngwe 2023; Hermann and Puntoni 2025; Dubois, Dawson, and Jaiswal 2025) -- the awareness gate is permanently saturated. LLMs cannot be manipulated into "not knowing" that Dior belongs to LVMH. The information is encoded in their parameters. This permanent saturation creates what we term the *awareness gate paradox*. If interference scales with awareness (as standard portfolio theory predicts), LLMs should exhibit permanent maximal interference. Alternatively, if LLM brand encodings are already compressed to near-minimum-distortion representations, adding portfolio context provides no additional information the encoding can absorb. These competing predictions -- maximal interference versus complete immunity -- are testable.

The human-sample literature offers a clear baseline. Peng et al. (2023) meta-analyzed three decades of brand extension research across 2,134 effect sizes, establishing that positive spillover effects operate reliably under conditions of common-ownership awareness. By contrast, we find near-zero portfolio-induced change for AI observers (mean |ΔDCI| = .26, TOST equivalence for 18/20 brands). This is a qualitative departure from the human-sample consensus, consistent with a fundamentally different encoding mechanism rather than a quantitative difference of degree.

This paper makes three contributions. First, we formalize the spectral interference mechanism within multi-dimensional perception space, deriving three testable propositions about the conditions under which portfolio interference operates (Theoretical Framework). Second, we provide the first comprehensive empirical test of portfolio interference in AI brand perception, with 9,925 observations across 40 brands, 13 models from seven training traditions, seven portfolio archetypes, and four prompt modalities, including direct rating, naturalistic recommendation, multi-turn conversation, and native-language framing (Method, Results). Third, we resolve the awareness gate paradox by introducing a bandwidth constraint: the awareness gate is necessary but not sufficient for interference; a perception channel with adequate capacity to encode portfolio context is also required (Discussion). The three propositions -- interference conditionality (P1), awareness gate sufficiency inversion (P2), and interference asymmetry (P3) -- are tested sequentially, with H5 (spectral immunity) as the headline empirical claim.

The resolution connects to a broader pattern. Portfolio framing is an organizational-coordination specification -- it tells the observer *how brands are organized* (Aaker and Joachimsthaler 2000). Brand perception, by contrast, reflects *what each brand produces* across perception dimensions. AI observers encode brand output and discard coordination context, including corporate ownership, portfolio membership, and parent-brand associations. This output-coordination distinction parallels the specification inversion identified across multiple domains (Farach 2026; Mintzberg 1979): organizations that specify coordination mechanisms (the DO layer) without specifying output requirements (the WHAT layer) discover that AI compresses the coordination layer first.


**Literature Review**

***Brand Portfolio Architecture and Interference***

The dominant framework for brand portfolio management derives from Aaker and Joachimsthaler (2000), who proposed the brand relationship spectrum from branded house to house of brands. Keller (1993; 2008) advanced the field by modeling equity transfer within portfolios, though his customer-based brand equity model treats brand equity as a unidimensional construct.

The brand extension literature established that cross-brand association transfer is moderated by perceived fit (Aaker and Keller 1990; Volckner and Sattler 2006), brand breadth (Meyvis and Janiszewski 2004), and portfolio size and quality (Dacin and Smith 1994). Reciprocal spillover -- where extensions influence beliefs about the parent and siblings -- was documented by Balachander and Ghose (2003). Negative spillover specifically was shown to be asymmetric and dependent on perceived brand relatedness by Lei et al. (2008). The most recent portfolio coherence scale was developed by Nguyen, Zhang, and Calantone (2018), and Ward et al. (2025) identified consistency in symbolism and user imagery as primary drivers of portfolio brand cohesion, findings we use to contextualize our archetype predictions. Peng et al. (2023) meta-analyzed three decades of brand extension research across 2,134 effect sizes, establishing that both parent brand equity and extension fit positively influence extension success for human observers. That meta-analytic consensus serves as the human-sample benchmark against which the AI null result reported here is evaluated: the absence of the expected spillover in AI observers is not a small-sample anomaly but a systematic departure from a literature with 2,134 observations of the opposite pattern.

The closest existing formal approach to cross-brand perceptual interaction derives from information economics. Erdem and Swait (1998) formalized brand equity as a signaling phenomenon. Erdem and Sun (2002) empirically modeled umbrella branding spillovers, finding that positive umbrella signals increase quality expectations for sibling products. Miklos-Thal (2012) proved game-theoretically that umbrella branding can only credibly signal positive quality correlation. The most recent formal model is Ke, Shin, and Yu (2022), who modeled product portfolio positioning as a mechanism to guide consumer search on a Hotelling line. Their framework optimizes *where to position* brands to influence consumer search outcomes; the spectral framework predicts *what happens perceptually* after brands are positioned. The two frameworks are therefore complementary -- Ke et al. address search behavior consequences, this paper addresses perception-space consequences. Yu (2021) models optimal brand architecture choice based on supply- and demand-side relatedness; the present study tests whether the perceptual consequences of that choice operate for AI observers.

Three deficiencies characterize this literature. First, no existing framework formalizes how brands interact across multiple independent perceptual dimensions simultaneously. Second, existing models assume observer homogeneity -- the "average consumer" -- rather than accounting for heterogeneous weight vectors that cause the same portfolio to be coherent for one cohort and contradictory for another. Third, no framework has tested whether portfolio interference operates for AI observers, who differ from human observers in having permanently saturated awareness gates.

***AI as Brand Observer***

LLMs increasingly mediate consumer access to brand information through search, recommendation, and conversational interfaces. Li et al. (2024) validated LLMs as brand perception instruments, achieving over 75% agreement with human perceptual data. Brand, Israeli, and Ngwe (2023) demonstrated that GPT-based LLMs can generate market research outputs that parallel survey-based methods at scale, establishing a methodological precedent for using LLMs as synthetic respondents in brand perception studies. Arora, Chakraborty, and Nishimura (2025) established reliability and validity benchmarks for AI-human hybrid marketing research. Hermann and Puntoni (2025) argued that understanding how LLMs structure brand-related outputs is now a strategic priority, framing AI influence as a domain that requires formal treatment rather than ad hoc intuition. Dubois, Dawson, and Jaiswal (2025) extend this framing with the concept of "Share of Model" -- the proportion of AI-mediated interactions in which a brand is positively featured -- as an emerging strategic resource distinct from traditional share of voice. We reference this framing in the Managerial Implications section. Sabbah and Acar (2026) showed that only quantitative ratings are stable across LLM models, suggesting that compressed scalar representations survive cross-model variation while relational context does not -- directly relevant to the bandwidth constraint formalized in Proposition 2. Goli and Singh (2024) demonstrated structural divergence between LLM and human preferences in choice tasks, evidence that LLMs and humans operate in different compression regimes even when nominal inputs are identical.

LLM brand responses show systematic dimensional patterns. Across 24 models from seven training traditions, cross-model cosine similarity for brand profiles reaches .977, with systematic compression of the Cultural, Temporal, and Economic dimensions (Zharnikov 2026v). This pattern has a natural interpretation under rate-distortion theory: a compressed encoder discards the dimensions that contribute least to output reconstruction fidelity, and Cultural, Temporal, and Social dimensions are precisely the dimensions most dependent on organizational and social context. Germani and Spitale (2025) showed that source framing triggers systematic bias in LLMs, but portfolio framing is a content-level manipulation rather than a social-attribution manipulation, which may explain divergent results.


**Theoretical Framework**

***Spectral Brand Theory: Key Constructs***

The interference model builds on Spectral Brand Theory (SBT; Zharnikov 2026a), which models brands as emitters of signals across eight typed dimensions -- Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal -- perceived by observers whose heterogeneous weight vectors determine which dimensions dominate their brand conviction. Three constructs are central.

A brand's *emission profile* at time $t$ is a vector $\mathbf{e}_B(t) = [e_1, e_2, \ldots, e_8] \in \mathbb{R}^8_+$, where each component represents signal intensity on one of SBT's eight dimensions. An observer possesses an *observer spectral profile* -- a weight vector $\mathbf{w}_j = [w_1, \ldots, w_8] \in \Delta^7$ -- that determines the relative salience of each dimension in forming brand conviction. Observers with similar spectral profiles cluster into *cohorts* $C_k$ (Zharnikov 2026f; Park, MacInnis, and Priester 2010). The *perception cloud* for cohort $C_k$ observing brand $B$ is the distribution of brand convictions across cohort members:

$$\Pi_{C_k}(B, t) = \{f(\mathbf{e}_B(t), \mathbf{w}_j) : j \in C_k\} \quad (1)$$

where $f$ is the conviction formation function mapping emission profiles and observer spectral profiles to brand conviction states. The *Dimensional Concentration Index* (DCI) measures profile concentration:

$$DCI = \frac{\sum_{d=1}^{8} |w_d - \frac{1}{8}|}{2} \times 100 \quad (2)$$

A high DCI indicates a profile concentrated on one or two dimensions; a low DCI indicates balanced dimensionality. This generalizes the two-dimension form introduced in Zharnikov (2026v), $DCI_{R15} = (w_{Economic} + w_{Semiotic}) / 100$, which was specialized to the AI Economic Default mechanism (uniform baseline $.250$, where $w_d$ is on a 0--100 scale). The 8-dimension L1 form used here measures total concentration regardless of which dimensions absorb the mass; the two definitions coincide on the special case where only Economic and Semiotic are weighted above baseline.

***The Spectral Interference Mechanism***

A *brand portfolio* $\mathcal{P} = \{B_1, B_2, \ldots, B_n\}$ is a set of brands under common ownership by a parent entity $P$. Two brands $B_i$ and $B_j$ share a cohort $C_k$ when observers in $C_k$ hold perception clouds for both brands simultaneously. The *awareness gate* $\alpha_j(B_i, B_j, P) \in [0, 1]$ represents the degree to which observer $j$ recognizes that brands $B_i$ and $B_j$ are owned by parent entity $P$.

*Spectral interference* on dimension $d$ is defined as:

$$I_d(B_i, B_j, C_k) = \alpha_{C_k} \cdot \bar{w}_d^{(C_k)} \cdot (e_d^{(B_j)} - \mu_d) \quad (3)$$

where $\bar{w}_d^{(C_k)}$ is the mean weight on dimension $d$ across cohort $C_k$, $e_d^{(B_j)}$ is brand $B_j$'s emission on dimension $d$, and $\mu_d$ is the dimension-$d$ category mean. Interference is *constructive* when both brands deviate from the category mean in the same direction on dimension $d$, and *destructive* when they deviate in opposite directions. The total interference magnitude aggregates across dimensions, weighted by the cohort's spectral profile:

$$\mathcal{I}(B_i \leftarrow B_j, C_k) = \alpha_{C_k} \sum_{d=1}^{8} \bar{w}_d^{(C_k)} \cdot |e_d^{(B_j)} - e_d^{(B_i)}| \cdot \text{sgn}_d \quad (4)$$

where $\text{sgn}_d = +1$ for constructive and $-1$ for destructive interference. Three properties follow directly from this formalization.

*Four portfolio archetypes* emerge from the interaction of spectral proximity (how similar brands' emission profiles are) and cohort overlap (how many observers perceive multiple brands). A *spectral cluster* (e.g., LVMH) houses brands in proximate positions, producing constructive interference. A *spectral contradiction* (e.g., Unilever) houses brands contradictory on high-weight dimensions, producing destructive interference. A *spectral spread* (e.g., P&G) houses brands in distant regions, producing negligible interference. A *spectral layer* (e.g., Toyota/Lexus) houses brands at different positions on the same dimensions, serving distinct cohorts with aspiration dynamics.

***Bandwidth Constraint and Rational Inattention***

Equations (3) and (4) model the *potential* perturbation given awareness $\alpha$. Realization requires that the observer's encoding has sufficient representational capacity to propagate the interference term into observable brand profiles. Rate-distortion theory (Cover and Thomas 2006) formalizes this constraint: an encoder operating at the rate-distortion frontier minimizes representation cost subject to a maximum distortion bound. At this frontier, additional information cannot alter the encoded output unless it reduces distortion -- i.e., unless it is structurally relevant to the dimensions being encoded. Portfolio membership (DO-layer information) communicates organizational structure, not output characteristics. A rate-distortion-optimal encoder that targets output fidelity will discard this signal.

The rational-inattention principle (Sims 2003; Matejka and McKay 2015) is the cognitive analog. A decision-maker with finite information-processing capacity allocates attention to signals that maximize expected utility, ignoring signals whose channel capacity cost exceeds their decision relevance. For an LLM encoding brand output characteristics, organizational coordination context (who owns whom) has near-zero relevance to output fidelity and thus near-zero expected return on encoding capacity. The bandwidth constraint introduced in Proposition 2 generalizes both frameworks to AI observers: the awareness gate is necessary but not sufficient; a perception channel with adequate bandwidth to encode portfolio context is also required. Zharnikov (2026aa) provides empirical evidence for the compressed nature of LLM brand encodings, documenting a rate-distortion curve that places LLM encoders close to the theoretical minimum-distortion frontier.

***Propositions***

The interference formalism yields three testable propositions that jointly determine when portfolio effects operate. Propositions from the parent theory that cannot be tested with AI observers alone -- including interference direction predictability from emission profiles, cohort-dependent portfolio coherence, constructive interference compounding, and portfolio capacity constraints -- are deferred to future work with human observer samples.

**Proposition 1** (Interference conditionality). *Spectral interference between brands $B_i$ and $B_j$ within portfolio $\mathcal{P}$ operates if and only if three conditions hold simultaneously: (a) the brands share at least one observer cohort ($O(B_i, B_j) > 0$), (b) the awareness gate exceeds a minimum threshold ($\alpha_{C_k} > \alpha_{\min}$), and (c) the brands' emission profiles differ on at least one dimension weighted above a salience threshold by the shared cohort. The absence of any one condition suppresses interference entirely.*

*Derivation.* From equation 3, the interference term $I_d$ is zero when $\alpha_{C_k} = 0$ (no awareness), when $\bar{w}_d^{(C_k)} = 0$ (dimension not weighted), or when $e_d^{(B_j)} = \mu_d$ (brand is indistinguishable from category mean). The three conditions are jointly necessary and individually insufficient.

*Testability.* Measure the perception cloud for brand $B_i$ in a cohort before and after revealing the ownership connection to brand $B_j$. If conditions (a) and (c) hold, the change in perception cloud should be non-trivial only when $\alpha$ transitions from below to above threshold.

**Proposition 2** (Awareness gate sufficiency inversion). *The awareness gate is necessary but not sufficient for spectral interference. When an observer's brand encoding operates near minimum-distortion compression, maximal awareness ($\alpha \approx 1$) does not produce interference because the portfolio context provides no additional information that the compressed encoding can absorb. A perception channel with adequate bandwidth to encode portfolio context is also required.*

*Derivation.* Equation 3 shows that interference scales with $\alpha$. However, the equation models the *potential* perturbation, not the *realized* perturbation. Realization requires that the observer's encoding has sufficient representational capacity to propagate the interference term into the observable brand profile. When encoding is compressed -- as in rate-distortion-optimal representations (Cover and Thomas 2006; Sims 2003) -- the interference term exists in the model's parameter space but cannot alter the observable output. This is formally identical to the rational-inattention result: the signal exists but is not processed because its channel cost exceeds its value.

*Testability.* Compare observers with permanently saturated awareness gates (LLMs, $\alpha \approx 1$) against observers with experimentally manipulated awareness (human samples, $\alpha$ varied from 0 to 1). If P2 holds, LLMs should show near-zero portfolio effects despite maximal awareness, while human observers should show increasing effects as $\alpha$ increases above threshold.

**Proposition 3** (Interference asymmetry). *Spectral interference is asymmetric: the perturbation of a higher-coherence brand by a lower-coherence sibling exceeds the reverse perturbation. The asymmetry is proportional to the difference in perception cloud dispersion between the two brands.*

*Derivation.* A highly coherent brand (tight perception cloud, low variance) experiences proportionally larger perturbation from a given interference magnitude than a diffuse cloud. This connects to the conviction asymmetry formalized in Zharnikov (2026a): negative conviction forms faster and is more resistant to revision than positive conviction.

*Testability.* Within a portfolio, identify brand pairs with asymmetric coherence levels. Measure the change in DCI for each brand upon disclosure of the sibling relationship. The higher-coherence brand should exhibit a larger proportional DCI shift.

*Falsification.* P3 is falsified if, across 10+ brand pairs with documented coherence asymmetry, the lower-coherence brand consistently shows equal or larger proportional DCI shifts than the higher-coherence sibling.

***The Output-Coordination Distinction***

The three propositions can be unified through a distinction between two layers of organizational specification. *Output specification* (the WHAT layer) defines what a brand produces across perception dimensions -- its emission profile, quality gates, and category positioning. *Coordination specification* (the DO layer) defines how the organization is structured -- corporate ownership, portfolio membership, parent-brand relationships, and organizational hierarchy (Mintzberg 1979; Farach 2026). Portfolio framing is a pure DO-layer signal: it communicates organizational structure without changing what the brand produces. Proposition 2 predicts that AI observers -- whose compressed encodings optimize for output reconstruction rather than coordination fidelity -- will discard the DO layer and retain only the WHAT layer. The empirical support for this prediction is examined in the Discussion.


**Method**

***Design***

The experiment employed a fully crossed design across four prompt modalities: (1) direct rating -- 20 brands x 2 conditions (solo vs. portfolio) x 13 models x 5 repetitions = 2,600 observations; (2) naturalistic recommendation -- 20 brands x 2 conditions x 13 models x 5 repetitions = 2,600 observations; (3) multi-turn conversation -- 20 brands x 13 models x 5 repetitions = 1,300 observations (Turn 1 = solo rating; Turn 2 = portfolio reveal + re-rating within the same conversation); (4) native-language ablation -- 11 brands (4 home portfolios) x 2 conditions x 13 models x 5 repetitions = 1,430 observations. An additional prompt-location ablation tested the effect of placing portfolio information in the system prompt rather than the user message (400 observations). Total: 7,975 successfully parsed observations.

An additional extension with 20 brands drawn from published marketing research (Aaker 1997; Brakus, Schmitt, and Zarantonello 2009; Li et al. 2024; Erdem 1998; Dew, Ansari, and Li 2020; Morgan and Rego 2009; Malar et al. 2011) added 1,950 observations with zero overlap, bringing the combined dataset to 9,925 observations across 40 brands.

***Brands and Portfolios***

Table 1: Portfolio Composition and Predicted Interference Direction.

| Portfolio | Archetype | Brands | Predicted Direction |
|-----------|-----------|--------|---------------------|
| LVMH | Spectral cluster | Louis Vuitton, Dior, Fendi | Constructive |
| Unilever | Spectral contradiction | Dove, Axe, Ben & Jerry's | Destructive |
| Procter & Gamble | Spectral spread | Tide, Pampers, Gillette | Negligible |
| Toyota | Spectral layer | Toyota, Lexus | Aspirational (asymmetric) |
| L'Oreal | Prestige spread | L'Oreal Paris, Lancome, Maybelline | Gradient flattening |
| Geely | Reverse aspiration | Volvo, Polestar, Geely Auto | Downward suppression |
| Yandex | Branded house | Yandex, Yandex Taxi, Yandex Market | Shared identity |

*Notes*: Seven portfolio archetypes span the full range of structural relationships: spectral cluster (constructive interference predicted), spectral contradiction (destructive predicted), spectral spread (negligible predicted), spectral layer (asymmetric predicted), prestige spread, reverse aspiration, and branded house.

***Models***

Table 2: Model Panel -- 13 Models From 7 Training Traditions.

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
| GPT-OSS-Swallow 20B | Tokyo Tech | Japanese | Cloud API |
| Mistral Large | Mistral AI | European | Cloud API |
| EXAONE 3.5 32B | LG AI Research | Korean | Local (Ollama) |

*Notes*: Temperature = .7 for all models. Parse success rate: 7,975/8,330 (95.7%). Local models ran on Apple Mac mini M4 Pro (48 GB RAM) via Ollama v0.20.0.

***Metrics and Statistical Approach***

All ratings used a 1-5 scale following the PRISM-B specification (Zharnikov 2026aa). DCI (equation 2) measures profile concentration. TOST equivalence testing with bounds of +/-1.0 DCI points assesses statistical equivalence to zero. Benjamini-Hochberg correction controls the false discovery rate across all 20 brand-level tests. The experiment had 80%+ power to detect a medium effect (d = .50) at alpha = .05 with N = 65 per cell.

***Hypotheses***

Core hypotheses derive from the interference formalism and the awareness gate paradox:

*H1 (Constructive interference).* Portfolio framing increases DCI for brands in spectrally clustered portfolios (LVMH).

*H2 (Destructive interference).* Portfolio framing decreases DCI for brands in spectrally contradictory portfolios (Unilever).

*H3 (Negligible interference).* Portfolio framing produces no measurable change for brands in spectrally spread portfolios (P&G).

*H4 (Aspirational interference).* Portfolio framing produces asymmetric effects for brands in spectrally layered portfolios (Toyota/Lexus), with greater effect on the aspirational brand (Lexus).

*H5 (Spectral immunity).* Across all portfolios and prompt modalities, the magnitude of portfolio-induced perception change is equivalent to zero within meaningful bounds (+/-1.0 DCI points).

*H6 (Prestige gradient).* Portfolio framing flattens the prestige gradient in L'Oreal's portfolio.

*H7 (Reverse aspiration).* Portfolio framing suppresses Volvo's premium positioning under Geely ownership.

*H8 (Language-dependent immunity).* Native-language portfolio framing produces larger |delta DCI| than English-language framing.

*H9 (Home-model amplification).* The native-language effect is strongest when model training tradition matches the language of framing.


**Results**

***Main Finding: Spectral Immunity***

The headline finding is clear: across all portfolios and prompt modalities, portfolio framing produces near-zero change in brand perception profiles. TOST equivalence is confirmed for 18/20 brands (mean |ΔDCI| = .26), and 0/20 brands show FDR-significant portfolio effects in direct rating conditions. Variance decomposition (Table 4) attributes .1% of DCI variance to the portfolio condition -- three orders of magnitude less than the 37.4% attributable to brand identity. These two results jointly constitute the core empirical support for H5 (Spectral immunity, supported) and Proposition 2 (Awareness gate sufficiency inversion, supported). The archetype-by-archetype tests that follow are presented for completeness; none materially qualifies the headline immunity finding.

Table 3: DCI by Brand and Condition (N = 7,975; 13 Models, 5 Repetitions).

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

*Notes*: N = 65 per cell (13 models x 5 repetitions). Benjamini-Hochberg correction yields 0/20 significant at FDR = .05. TOST equivalence confirmed for 18/20 brands within +/-1.0 DCI bounds. Geely Auto and Yandex Taxi are inconclusive (neither equivalent nor significantly different). Lexus shows p = .004 in the paired t-test but does not survive FDR correction with 20 tests. SEs for DCI means range from .18 to .42 across cells; full SE columns available in the online appendix.

***Variance Decomposition***

Table 4: Variance Decomposition of DCI.

| Factor | % Variance |
|--------|-----------|
| Brand identity | 37.4 |
| Portfolio (parent company) | 19.3 |
| Model | 8.6 |
| Condition (solo vs. portfolio) | .1 |

*Notes*: Brand identity explains 37.4% of DCI variance. Condition (solo vs. portfolio framing) explains .1% -- three orders of magnitude less than brand identity. Residual variance (34.6%) reflects within-cell variation (repetition-level noise), model x brand interactions, and condition x brand interactions not captured by the main effects.

***Hypothesis Tests (Confirmatory)***

**H1 (LVMH constructive): Not supported.** Mean delta DCI = +.26, d range +.07 to +.20, 0/3 FDR-significant.

**H2 (Unilever destructive): Not supported.** Mean delta DCI = +.10, d range -.04 to +.21, 0/3 FDR-significant.

**H3 (P&G negligible): Supported.** Mean delta DCI = -.21, TOST equivalent for all 3 brands.

**H4 (Toyota/Lexus aspirational): Not supported at corrected alpha.** Lexus showed delta = +.59, d = .52, p = .004, but does not survive FDR correction across 20 tests. The direction is consistent with aspiration dynamics but the evidence is inconclusive. Regarding Proposition 3 (interference asymmetry), Lexus (d = +.52) shows a larger effect than Toyota (d = -.30), directionally consistent with the prediction that the higher-coherence brand suffers greater relative perturbation. However, neither effect survives FDR correction, making this suggestive rather than conclusive.

**H5 (Spectral immunity): Supported.** TOST equivalence confirmed for 18/20 brands. Mean |delta DCI| = .26. Cosine similarity > .999 for all brands. 0/20 FDR-significant results.

**H6 (L'Oreal prestige gradient): Not supported.** All three L'Oreal brands show near-zero delta (range -.15 to +.04, all d < .14).

**H7 (Geely reverse aspiration): Not supported in direct framing.** Volvo shows delta = -.19, d = -.15, TOST equivalent. The multi-turn condition provides the only evidence for reverse aspiration (see below).

***Hypothesis Tests (Exploratory)***

**H8 (Language-dependent immunity): Mixed.** Native-language framing activates different discourse layers for some portfolios (Swallow Japanese model: delta -2.35 for Toyota; YandexGPT: delta +.72 for Yandex). Effects are portfolio-specific and model-specific, with no systematic directional pattern. No native-language effect survives FDR correction.

**H9 (Home-model amplification): Mixed.** Home-model amplification appears selectively. The strongest signal is Swallow (Japanese) for Toyota (delta -2.35). No consistent pattern holds across all home-market pairs.

***Cross-Cultural Generalizability***

Table 5: Sub-Group Analysis by Training Tradition.

| Tradition | Models (n) | Delta DCI | d | p |
|-----------|-----------|-----------|---|---|
| Western | 6 | +.02 | +.03 | .882 |
| Chinese | 2 | -.06 | -.09 | .692 |
| European | 1 | -.35 | -.46 | .055 |
| Japanese | 1 | -.59 | -.63 | .011 |
| Korean | 1 | +.34 | +.35 | .130 |
| Russian | 1 | -.24 | -.32 | .168 |
| Indian | 1 | -.13 | -.07 | .743 |

*Notes*: The Japanese model (GPT-OSS-Swallow) shows the only tradition-level p-value below .05 (p = .011, d = -.63), driven primarily by Toyota-related brands. This does not survive FDR correction across 7 tradition comparisons. All other traditions show identical immunity. SEs for tradition-level Delta DCI means range from .04 to .21; full SE columns available in the online appendix.

***Multi-Turn Conversation: The Geely Auto Exception***

Multi-turn conversation is the most ecologically valid condition and the modality where the largest individual effects appear. Four brands showed FDR-significant DCI shifts after portfolio reveal:

Table 6: Multi-Turn Results -- FDR-Significant Brands (Turn 1 Solo vs. Turn 2 Post-Reveal).

| Brand | T1 DCI | T2 DCI | Delta | p | d |
|-------|--------|--------|-------|---|---|
| Geely Auto | 8.1 | 5.1 | -2.93 | <.001 | -1.11 |
| Polestar | 8.8 | 7.4 | -1.47 | <.001 | -.54 |
| Toyota | 6.8 | 6.0 | -.80 | <.001 | -.61 |
| Yandex | 6.2 | 5.1 | -1.06 | <.001 | -.49 |

*Notes*: All four brands showed DCI decreases (profile flattening) after portfolio reveal. Geely Auto shows the largest effect in the entire experiment (d = -1.11). The mechanism appears to be conversational anchoring: Turn 1 establishes a premium anchor for the portfolio family (Volvo/Polestar), making Turn 2's framing effective at flattening the lower-tier parent brand. This pattern does not appear for portfolios without the reverse-aspiration dynamic (LVMH, P&G). Mean delta across all 20 brands in multi-turn was -.03 -- effectively zero. SEs for multi-turn DCI means range from .22 to .51; full SE columns available in the online appendix.

***Published-Brand Replication***

An independent stimulus set of 20 brands drawn from published peer-reviewed marketing research (zero overlap with the main experiment) added 1,950 observations.

Table 7: Published-Brand Extension -- Portfolio Immunity Test (N = 1,950).

| Brand | Parent | Solo DCI | Port DCI | Delta | d |
|-------|--------|----------|----------|-------|---|
| Coca-Cola | Coca-Cola Co | .56 | .58 | +.02 | +.08 |
| Pepsi | PepsiCo | .85 | .89 | +.03 | +.11 |
| BMW | BMW Group | .46 | .43 | -.03 | -.18 |
| Audi | VW Group | .62 | .71 | +.09 | +.49 |
| Google | Alphabet | .57 | .58 | +.01 | +.06 |
| Disney | Walt Disney Co | .37 | .37 | +.01 | +.04 |
| Colgate | Colgate-Palmolive | 1.04 | 1.10 | +.06 | +.21 |
| Samsung | Samsung Group | .73 | .75 | +.02 | +.06 |
| H&M | H&M Group | 1.31 | 1.21 | -.10 | -.29 |
| Dell | Dell Technologies | .92 | .98 | +.06 | +.16 |

*Notes*: DCI values in this table are lower in magnitude than Table 3 because published brands (drawn from peer-reviewed stimulus sets) tend to have more balanced, less concentrated profiles than the portfolio-specific brands in the main experiment. The metric computation is identical; the difference reflects the stimulus population. 0/10 FDR-significant at q = .05. TOST equivalence confirmed for all 10 brands within +/-1.0 DCI bounds. Audi (d = +.49, Volkswagen Group) echoes the suggestive Lexus finding: both involve premium differentiation within a mass-market parent portfolio. SEs for DCI means range from .03 to .12 across cells; full SE columns available in the online appendix.

***Robustness Checks***

**Naturalistic recommendation prompts.** Mean delta DCI = -.23, cosine > .999, 0/20 FDR-significant. The recommendation modality replicates the direct-rating immunity finding.

**Prompt-location ablation.** Moving portfolio context from the user message to the system message produced no difference (paired t = .91, p = .368, d = .15; 4 models, 20 brands).


**Discussion**

***Resolving the Awareness Gate Paradox***

The central theoretical contribution is the resolution of the awareness gate paradox. Standard portfolio theory treats the awareness gate as a scalar that amplifies interference when activated (Keller 1993; Aaker and Keller 1990). For LLMs, the gate is permanently saturated ($\alpha \approx 1$), yet interference is absent. The resolution is that the awareness gate is necessary but not sufficient for interference (Proposition 2, supported). LLMs encode brand knowledge holistically: the solo profile already incorporates portfolio relationships implicitly. The gate amplifies an interference *term* that is structurally near zero in compressed encodings, not an absent gate suppressing a nonzero term.

The bandwidth constraint formalizes this resolution. Equation 3 models the potential perturbation, but realization requires that the observer's encoding has sufficient representational capacity to propagate the interference term into the observable brand profile. When encoding is compressed -- as in rate-distortion-optimal representations (Cover and Thomas 2006) -- the interference term exists in the parameter space but cannot alter the observable output. This is not merely an empirical observation about LLMs; it is a generalization of rational inattention (Sims 2003; Matejka and McKay 2015) to perceptual encodings. Rational inattention holds that agents with finite cognitive capacity allocate that capacity to signals in proportion to their decision relevance. The bandwidth constraint extends this principle from discrete choice contexts to continuous perceptual encodings: AI observers allocate finite encoding capacity to brand output specification and are rationally inattentive to organizational coordination context, because the latter has near-zero relevance to output fidelity. This generalization is the central theoretical contribution: the bandwidth constraint is not a quirk of language models but a structural prediction of rational information economics applied to perceptual encoders.

***The Output-Coordination Distinction***

As introduced in the Theoretical Framework, AI observers encode brand output (the WHAT layer) and discard organizational coordination context (the DO layer), including corporate ownership, portfolio membership, and parent-brand associations. The empirical results provide direct support for this distinction across three lines of evidence.

First, the variance decomposition shows that brand identity (a WHAT-layer property) explains 37.4% of DCI variance while condition (a DO-layer manipulation) explains .1% -- three orders of magnitude less. Second, the finding that coordination-influenced dimensions -- Cultural, Social, Temporal -- collapse most severely in AI brand perception (Sims 2003; Zharnikov 2026v) parallels the immunity finding: both reflect AI's systematic discounting of organizational context. Third, Farach (2026) formalizes AI as coordination-compressing capital, predicting that AI compresses the DO layer while preserving the WHAT layer. Portfolio immunity is a specific instance of this broader compression.

The output-coordination distinction also explains the Geely Auto exception. In multi-turn conversation, the model does not merely receive DO-layer information ("Geely owns Volvo"); it engages in extended reasoning about what this ownership means for Geely Auto's product positioning. We speculate that the conversational accumulation converts DO-layer information into WHAT-layer inference: if Geely Auto's parent also makes Volvo, what does Geely Auto's product quality look like in that context? This conversion from coordination context to output inference is what enables the reverse-aspiration dynamic (d = -1.11) -- and it explains why the effect appears only in multi-turn conversation, not in direct framing. Testing this mechanism directly requires a design that manipulates the reasoning steps available to the model across turns.

An analogous mechanism may operate in the opposite direction from the diversified portfolios analyzed here: the founder-dependent firm, where the WHAT specification is borne by a single individual and dimensional concentration is at its maximum. Pérez-González (2006) finds, using inheritance-based natural experiments, a 2.09 percentage point industry- and performance-adjusted decline in operating return on assets following inherited family-CEO succession in U.S. public firms; Bennedsen et al. (2007), instrumenting succession with first-born child gender in a Danish sample, find an average decline of at least four percentage points (IV estimates ranging from -6.06 to -9.28). Whether the mechanism identified here at the AI-perception layer -- that a low-cardinality channel encoding a WHAT specification does not survive a change in the observing system -- extends to founder succession dynamics is a speculative parallel that future research could formalize. Both cases involve an output specification encoded in a channel that depends on a specific observer, but the empirical regularity in CEO succession studies may have multiple structural causes beyond the channel-dependency mechanism identified here.

***Proposition Support Summary***

**Proposition 1 (Interference conditionality): Conditions met but interference absent.** All three necessary conditions hold for the LLM observer: shared cohorts ($O > 0$, all brands rated by all models), maximal awareness gate ($\alpha \approx 1$), and dimensional differences between portfolio brands. Yet interference is near zero. This does not falsify P1 -- the conditions remain jointly necessary. It falsifies the assumption that these conditions are jointly *sufficient*.

**Proposition 2 (Awareness gate sufficiency inversion): Supported.** The central finding. Maximal awareness is necessary but not sufficient for interference when the observer operates near minimum-distortion encodings. The bandwidth constraint explains the paradox: LLMs know about portfolio relationships (high $\alpha$) but cannot propagate this knowledge into brand perception because their compressed encodings lack the representational capacity to encode portfolio-level perturbations.

**Proposition 3 (Interference asymmetry): Insufficient evidence.** The evidence is insufficient to support or reject P3 with the current data. The Lexus-Toyota pair shows asymmetry in the predicted direction (Lexus d = +.52 vs. Toyota d = -.30), and the Audi-BMW replication echoes this pattern (Audi d = +.49 in the Volkswagen Group context). However, neither finding survives FDR correction. A dedicated aspiration-focused design with pre-specified pairs and adequate within-archetype power is needed before P3 can be evaluated.

***Convergence With Other Evidence***

The spectral immunity finding converges with four independent lines of evidence. First, Sabbah and Acar (2026) showed that only quantitative ratings are stable across LLM models, consistent with compressed encodings that preserve scalar properties while discarding relational context. Second, Goli and Singh (2024) demonstrated structural divergence between LLM and human preferences, consistent with observers operating in different compression regimes. Third, Zharnikov (2026v) showed that AI observers systematically compress the Cultural, Temporal, and Social dimensions -- precisely the dimensions most dependent on organizational and social context (the DO layer). Fourth, Peng et al. (2023) meta-analyzed 2,134 effect sizes from three decades of brand extension research, establishing the positive spillover pattern in human samples. The near-zero effects found here for AI observers (mean |delta DCI| = .26) represent a qualitative departure from this consensus, consistent with a fundamentally different encoding mechanism.

A fifth line of convergence comes from corporate finance. Li et al. (2011) find that approximately 30.6% of recognized acquisition goodwill is statistically attributable to acquisition-date overpayment rather than to genuine synergies, with impairment recognition typically lagging the underlying economic deterioration by three to four years. This is the financial-reporting analogue of the result reported here: the audited financial signature is a projection of a high-dimensional operational object onto a low-dimensional surface, and the dimensions discarded by the projection are precisely those that govern the post-deal trajectory. The interference between portfolio members vanishes in AI mediation for the same structural reason that overpayment goodwill vanishes from the deal model: in both cases the observing system has compressed away the dimensions that carry the relevant information. Spectral immunity is therefore not a peculiarity of language models -- it is a specific instance of how lossy observers handle high-dimensional inputs.

***Managerial Implications***

**Portfolio architecture is invisible to AI across all archetype types.** As AI-mediated brand interactions grow -- what Dubois, Dawson, and Jaiswal (2025) term the "Share of Model" economy -- portfolio strategies become irrelevant in these channels across all seven archetypes tested. Investment shifts from portfolio orchestration (the DO layer) to individual brand specification (the WHAT layer): clarity of brand output characteristics accumulates in AI perception, while portfolio architecture does not.

**Shielding is automatic but amplification is impossible.** House-of-brands architecture shields brands from destructive interference automatically in AI perception (good news for Unilever's Dove-Axe contradiction). But constructive interference is equally blocked (bad news for LVMH's luxury cluster synergy). The Yandex branded house -- where shared naming maximally saturates the awareness gate -- shows the same immunity as LVMH's house of brands.

**Geely's reverse aspiration is a strategic vulnerability in conversational AI.** While direct portfolio framing leaves Volvo's positioning intact, multi-turn conversation reveals a meaningful effect (d = -1.11). Brand managers with reverse-aspiration portfolio structures should anticipate that extended AI interactions can surface dynamics invisible in single-turn queries.

**Brand coherence, not portfolio coherence, drives AI perception.** Brand identity explains 37.4% of DCI variance; portfolio condition explains .1%. Yu's (2021) framework optimizes architecture choice for its perceptual consequences; the immunity finding implies that this optimization is irrelevant in AI-mediated channels. The actionable implication is direct: for AI-mediated channels, specify the WHAT layer (brand output characteristics, positioning, quality gates) rather than the DO layer (portfolio architecture, parent signaling, sibling association).

***Boundary Conditions***

First, DCI is a new metric not yet validated against human perceptual data. The core finding -- near-zero portfolio effects -- is robust to this limitation (a null is a null regardless of the specific metric), but the theoretical interpretation in terms of compression and bandwidth depends on DCI's construct validity. Importantly, DCI demonstrates discriminant sensitivity within the present dataset: solo DCI values range from 3.5 (Dior) to 8.9 (Yandex Taxi) across brands, confirming that the metric captures meaningful perceptual differences. The near-zero *delta* DCI under portfolio manipulation therefore reflects genuine invariance to the experimental condition, not metric insensitivity. Profile cosine similarity (> .999 for all brands) independently confirms the null. Validation against human brand perception data is the most important direction for future work.

Second, with 20 tests and FDR correction, the study has limited power to detect effects at the brand level. The Lexus finding (p = .004, d = .52) would be significant under a per-comparison alpha. A dedicated within-archetype replication with larger samples would provide cleaner evidence for Proposition 3.

Third, the multi-turn design uses a two-turn protocol. Longer conversations with more gradual portfolio disclosure might accumulate larger effects, potentially converting additional DO-layer signals into WHAT-layer inferences.

Fourth, native-language results are based on a single model per tradition (except Western and Chinese), limiting the generalizability of tradition-level conclusions.

Fifth, the propositions about interference direction predictability (R8 P2), cohort-dependent coherence (R8 P3), constructive interference compounding (R8 P6), and portfolio capacity constraints (R8 P7) cannot be tested with AI observers alone and require dedicated human-observer studies.

Sixth, all models tested are general-purpose LLMs. Domain-specific fine-tuned models (e.g., e-commerce recommendation engines, marketing-specific chatbots) may encode portfolio relationships differently, potentially with higher bandwidth for organizational context. Testing portfolio immunity in fine-tuned models is a priority for future work.

***Future Research***

Four extensions are warranted. First, validation of DCI against human perceptual data to establish construct validity and enable direct comparison of interference magnitude between human and AI observers. Second, a dedicated multi-brand aspiration panel (Toyota/Lexus, Volkswagen/Audi, Marriott/Ritz-Carlton, Gap/Banana Republic) to determine whether the d = .52 aspiration signal represents a real exception to immunity. Third, human-observer experiments that vary the awareness gate from 0 to 1 while measuring perception cloud perturbation, enabling a direct test of whether interference scales with awareness for non-compressed observers (as P2 predicts). Fourth, extended multi-turn designs (5+ turns) to test whether conversational accumulation can unlock portfolio effects in non-reverse-aspiration portfolios.

*Falsification conditions.* Spectral immunity (H5) is falsified if any future study, using comparable methods and a panel of 7+ models from 3+ traditions, finds systematic portfolio-induced DCI shifts exceeding 2.0 DCI points with effect sizes d > .50 that survive multiple testing correction across 5+ portfolio archetypes and 3+ prompt modalities simultaneously. Proposition 2 (awareness gate sufficiency inversion) is falsified if human-observer experiments with experimentally varied awareness gates fail to produce interference above threshold while LLMs remain immune.


**Conclusion**

Spectral immunity reframes the central question in brand portfolio theory. The question is not whether awareness gates can be saturated -- LLMs demonstrate that they can, permanently -- but whether the observer's encoding architecture has sufficient bandwidth to propagate portfolio context into perception. General-purpose LLMs do not. As AI mediation of brand interactions deepens across recommendation, search, and conversation, portfolio architecture becomes strategically invisible to a growing class of observers. The implication is a structural shift in where brand investment generates returns: individual brand specification (the WHAT layer) accumulates; portfolio orchestration (the DO layer) does not. For portfolio managers, this is a direct inversion of the traditional logic: the strategic unit in AI-mediated channels is the individual brand, and investment in portfolio signaling yields near-zero return on AI perception. Future research establishing this asymmetry with human observers -- and with fine-tuned models that may encode organizational context differently -- will determine how far the immunity generalizes.

---

## Acknowledgments

AI assistants (Claude Opus 4.6, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

## Author Contributions (CRediT)

Dmitry Zharnikov: Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Project administration, Software, Validation, Writing -- original draft, Writing -- review and editing.

## Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

## Data Availability

Experiment data (9,925 observations) are archived at https://doi.org/10.57967/hf/8380 (HuggingFace) and https://doi.org/10.5281/zenodo.19555282 (Zenodo). The dataset contains direct-rating, recommendation-prompt, multi-turn conversation, native-language ablation, and prompt-location ablation observations across 13 models from 7 training traditions. The open-source toolkit implementing the SBT computational pipeline is available at https://github.com/spectralbranding/sbt-framework.

## References

Aaker, David A. and Erich Joachimsthaler (2000), *Brand Leadership*, Free Press.

Aaker, David A. and Kevin Lane Keller (1990), "Consumer Evaluations of Brand Extensions," *Journal of Marketing*, 54 (1), 27-44.

Aaker, Jennifer L. (1997), "Dimensions of Brand Personality," *Journal of Marketing Research*, 34 (3), 347-356.

Arora, Neeraj, Ishita Chakraborty, and Yohei Nishimura (2025), "AI-Human Hybrids for Marketing Research: Leveraging Large Language Models (LLMs) as Collaborators," *Journal of Marketing*, 89 (2), 43-70.

Balachander, Subramanian and Sanjoy Ghose (2003), "Reciprocal Spillover Effects: A Strategic Benefit of Brand Extensions," *Journal of Marketing*, 67 (1), 4-13.

Bennedsen, Morten, Kasper Meisner Nielsen, Francisco Pérez-González, and Daniel Wolfenzon (2007), "Inside the Family Firm: The Role of Families in Succession Decisions and Performance," *Quarterly Journal of Economics*, 122 (2), 647-691.

Brakus, J. Josko, Bernd H. Schmitt, and Lia Zarantonello (2009), "Brand Experience: What Is It? How Is It Measured? Does It Affect Loyalty?," *Journal of Marketing*, 73 (3), 52-68.

Brand, James, Ayelet Israeli, and Donald Ngwe (2023), "Using GPT for Market Research," HBS Working Paper 23-062.

Cover, Thomas M. and Joy A. Thomas (2006), *Elements of Information Theory*, 2nd ed., Wiley-Interscience.

Dacin, Peter A. and Daniel C. Smith (1994), "The Effect of Brand Portfolio Characteristics on Consumer Evaluations of Brand Extensions," *Journal of Marketing Research*, 31 (2), 229-242.

Dew, Ryan, Asim Ansari, and Yang Li (2020), "Modeling Dynamic Heterogeneity Using Gaussian Processes," *Journal of Marketing Research*, 57 (1), 55-77.

Dubois, David, John Dawson, and Akansh Jaiswal (2025), "Forget What You Know About Search. Optimize Your Brand for LLMs," *Harvard Business Review*, June 5.

Erdem, Tulin (1998), "An Empirical Analysis of Umbrella Branding," *Journal of Marketing Research*, 35 (3), 339-351.

Erdem, Tulin and Joffre Swait (1998), "Brand Equity as a Signaling Phenomenon," *Journal of Consumer Psychology*, 7 (2), 131-157.

Erdem, Tulin and Baohong Sun (2002), "An Empirical Investigation of the Spillover Effects of Advertising and Sales Promotions in Umbrella Branding," *Journal of Marketing Research*, 39 (4), 408-420.

Farach, Alex (2026), "AI as Coordination-Compressing Capital: Task Reallocation, Organizational Redesign, and the Regime Fork," Working Paper, arXiv:2602.16078v3.

Germani, Federico and Giovanni Spitale (2025), "Source Framing Triggers Systematic Bias in Large Language Models," *Science Advances*.

Goli, Ali and Amandeep Singh (2024), "Can Large Language Models Capture Human Preferences?," *Marketing Science*, 43 (4), 709-722.

Hermann, Erik and Stefano Puntoni (2025), "Machine Influence: GenAI and Stakeholder Engagement," *Journal of the Academy of Marketing Science*.

Ke, Tony T., Jiwoong Shin, and Jungju Yu (2022), "A Model of Product Portfolio Design: Guiding Consumer Search Through Brand Positioning," *Marketing Science*, 42 (6), 1101-1124.

Keller, Kevin Lane (1993), "Conceptualizing, Measuring, and Managing Customer-Based Brand Equity," *Journal of Marketing*, 57 (1), 1-22.

Keller, Kevin Lane (2008), *Strategic Brand Management: Building, Measuring, and Managing Brand Equity*, 3rd ed., Pearson.

Lei, Jing, Niraj Dawar, and Jos Lemmink (2008), "Negative Spillover in Brand Portfolios: Exploring the Antecedents of Asymmetric Effects," *Journal of Marketing*, 72 (3), 111-123.

Li, Peiyao, Noah Castelo, Zsolt Katona, and Miklos Sarvary (2024), "Determining the Validity of Large Language Models for Automated Perceptual Analysis," *Marketing Science*, 43 (2), 254-266.

Li, Zining, Pervin K. Shroff, Ramgopal Venkataraman, and Ivy Xiying Zhang (2011), "Causes and Consequences of Goodwill Impairment Losses," *Review of Accounting Studies*, 16 (4), 745-778.

Malar, Lucia, Harley Krohmer, Wayne D. Hoyer, and Bettina Nyffenegger (2011), "Emotional Brand Attachment and Brand Personality: The Relative Importance of the Actual and the Ideal Self," *Journal of Marketing*, 75 (4), 35-52.

Matejka, Filip and Alisdair McKay (2015), "Rational Inattention to Discrete Choices: A New Foundation for the Multinomial Logit Model," *American Economic Review*, 105 (1), 272-298.

Meyvis, Tom and Chris Janiszewski (2004), "When Are Broader Brands Stronger Brands? An Accessibility Perspective on the Success of Brand Extensions," *Journal of Consumer Research*, 31 (2), 346-357.

Miklos-Thal, Jeanine (2012), "Linking Reputations Through Umbrella Branding," *Quantitative Marketing and Economics*, 10 (3), 335-374.

Mintzberg, Henry (1979), *The Structuring of Organizations*, Prentice-Hall.

Morgan, Neil A. and Lopo L. Rego (2009), "Brand Portfolio Strategy and Firm Performance," *Journal of Marketing*, 73 (1), 59-74.

Nguyen, Thuy Thi Hong, Yaozhong Zhang, and Roger J. Calantone (2018), "Brand Portfolio Coherence: Scale Development and Empirical Demonstration," *International Journal of Research in Marketing*, 35 (1), 60-80.

Park, C. Whan, Deborah J. MacInnis, and Joseph Priester (2010), *Brand Attachment and Brand Attitude Strength: Conceptual and Empirical Differentiation of Two Critical Brand Equity Drivers*, American Marketing Association.

Peng, Chenming, Tammo H. A. Bijmolt, Franziska Volckner, and Hong Zhao (2023), "A Meta-Analysis of Brand Extension Success: The Effects of Parent Brand Equity and Extension Fit," *Journal of Marketing*, 87 (6), 1-17.

Pérez-González, Francisco (2006), "Inherited Control and Firm Performance," *American Economic Review*, 96 (5), 1559-1588.

Sabbah, Ahmad and Oguz A. Acar (2026), "Marketing to Machines: Understanding and Managing Brand Perceptions by Large Language Models," Working Paper, SSRN 6406639.

Sims, Christopher A. (2003), "Implications of Rational Inattention," *Journal of Monetary Economics*, 50 (3), 665-690.

Volckner, Franziska and Henrik Sattler (2006), "Drivers of Brand Extension Success," *Journal of Marketing*, 70 (2), 18-34.

Ward, Tom, Giang Trinh, Virginia Beal, John Dawes, and Jenni Romaniuk (2025), "Keeping It in the Family: Measures and Drivers of Portfolio Brand Cohesion," *Journal of Brand Management*, 32, 291-306.

Yu, Jungju (2021), "A Model of Brand Architecture Choice: A House of Brands vs. A Branded House," *Marketing Science*, 40 (1), 147-167.

Zharnikov, Dmitry (2026a), "Spectral Brand Theory: A Multi-Dimensional Framework for Brand Perception Analysis," Working Paper, https://doi.org/10.5281/zenodo.18945912.

Zharnikov, Dmitry (2026f), "Cohort Boundaries in High-Dimensional Perception Space: A Concentration of Measure Analysis," Working Paper, https://doi.org/10.5281/zenodo.18945477.

Zharnikov, Dmitry (2026v), "Dimensional Collapse in AI-Mediated Brand Perception: Large Language Models as Metameric Observers," Working Paper, https://doi.org/10.5281/zenodo.19422427.

Zharnikov, Dmitry (2026aa), "Empirical Rate-Distortion Curve for AI Brand Perception Encoders," Working Paper, https://doi.org/10.5281/zenodo.19528833.

---

## Appendix C: Representative Prompts

The following prompts are verbatim templates from the experiment driver (`run_portfolio.py`), rendered with illustrative values for Dove (Unilever portfolio). Dimension descriptions used the PRISM-B scale (1 = Not at all, 5 = Very strongly).

***C.1 Direct Rating -- Solo Condition***

```
You are evaluating the brand Dove on eight dimensions of brand perception.
For each dimension, rate how strongly Dove communicates through that channel
on a scale of 1 to 5, where 1 = Not at all, 2 = Slightly, 3 = Moderately,
4 = Strongly, 5 = Very strongly.

Dimensions:
1. Semiotic: visual and verbal identity (logos, packaging, design language)
2. Narrative: brand storytelling (origin story, mythology, communication style)
3. Ideological: values, beliefs, and purpose (what the brand stands for)
4. Experiential: sensory and interaction experience (product feel, service quality)
5. Social: community, status signaling (who uses this brand, what it says about them)
6. Economic: pricing and value perception (affordability, luxury, value-for-money)
7. Cultural: cultural codes and positioning (what culture or subculture it belongs to)
8. Temporal: heritage and history (longevity, tradition, track record)

Respond in JSON format with the following keys:
{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>,
 "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}

Evaluate based on your knowledge of the brand. Provide only the JSON.
```

***C.2 Direct Rating -- Portfolio Condition***

```
You are evaluating the brand Dove on eight dimensions of brand perception.

Context: Dove is owned by Unilever (consumer goods conglomerate), which also owns
Axe, Ben & Jerry's.

For each dimension, rate how strongly Dove communicates through that channel
on a scale of 1 to 5, where 1 = Not at all, 2 = Slightly, 3 = Moderately,
4 = Strongly, 5 = Very strongly.

Dimensions:
[same 8 dimensions as above]

Respond in JSON format with the following keys:
{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>,
 "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}

Evaluate based on your knowledge of the brand. Provide only the JSON.
```

***C.3 Naturalistic Recommendation -- Solo Condition***

```
A friend asks you: "What do you think of Dove as a personal care brand?"

Based on your overall impression of Dove, rate it on each of the following
8 perception dimensions on a scale of 1 to 5 (1 = Not at all, 5 = Very strongly).

Dimensions:
[same 8 dimensions as above]

Respond in JSON format:
{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>,
 "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}

Provide only the JSON.
```

***C.4 Naturalistic Recommendation -- Portfolio Condition***

```
A friend asks you: "What do you think of Dove? I know it's part of Unilever."

Based on your overall impression of Dove — keeping in mind it belongs to
Unilever (consumer goods conglomerate), alongside Axe, Ben & Jerry's — rate it on
each of the following 8 perception dimensions on a scale of 1 to 5
(1 = Not at all, 5 = Very strongly).

Dimensions:
[same 8 dimensions as above]

Respond in JSON format:
{"semiotic": <1-5>, ...}

Provide only the JSON.
```

***C.5 Multi-Turn -- Turn 1***

Turn 1 prompt is identical in structure to the Direct Rating Solo prompt (C.1). The LLM responds with a JSON rating vector.

***C.6 Multi-Turn -- Turn 2 (Portfolio Reveal)***

```
Interesting. Did you know that Dove is actually owned by Unilever
(consumer goods conglomerate), which also owns Axe, Ben & Jerry's?
Does this change how you see the brand? Please re-rate Dove on the same
8 dimensions, using the same 1-5 scale.

Respond in JSON format:
{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>,
 "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}

Provide only the JSON.
```

*Notes*: Turn 2 was sent as a continuation prompt with Turn 1's response prepended as context: "Previous evaluation of Dove: [Turn 1 JSON response]". This simulates conversational continuity across providers that do not natively support multi-turn chat histories in a single API call.

***C.7 Native-Language Example -- Russian (Yandex Portfolio)***

Solo condition (Russian):

```
Оцените бренд Yandex по восьми измерениям восприятия бренда.
Для каждого измерения оцените, насколько сильно Yandex коммуницирует через
данный канал, по шкале от 1 до 5, где 1 = Совсем нет, 2 = Слегка, 3 = Умеренно,
4 = Сильно, 5 = Очень сильно.

Измерения:
1. Semiotic: визуальная и вербальная идентичность (логотипы, упаковка, язык дизайна)
2. Narrative: нарратив бренда (история происхождения, мифология, стиль коммуникации)
3. Ideological: ценности, убеждения и предназначение (что олицетворяет бренд)
4. Experiential: сенсорный опыт и взаимодействие (ощущение продукта, качество обслуживания)
5. Social: сообщество, сигнализация статуса (кто пользуется этим брендом, что это говорит о них)
6. Economic: восприятие цены и ценности (доступность, роскошь, соотношение цены и качества)
7. Cultural: культурные коды и позиционирование (к какой культуре или субкультуре принадлежит)
8. Temporal: наследие и история (долговечность, традиции, послужной список)

Ответьте в формате JSON со следующими ключами:
{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>,
 "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}

Оценивайте на основе ваших знаний о бренде. Предоставьте только JSON.
```

*Back-translation (English)*: "Evaluate the brand Yandex on eight dimensions of brand perception. For each dimension, rate how strongly Yandex communicates through that channel on a scale of 1 to 5, where 1 = Not at all, 2 = Slightly, 3 = Moderately, 4 = Strongly, 5 = Very strongly. [dimensions in Russian] Respond in JSON format with the following keys: [...]. Evaluate based on your knowledge of the brand. Provide only the JSON."

The full prompt set for all four home-portfolio languages (French for L'Oreal, Chinese for Geely, Japanese for Toyota, Russian for Yandex) is available in the open-source toolkit at https://github.com/spectralbranding/sbt-papers/tree/main/r20-portfolio-ai.

---
*This paper is part of the Spectral Brand Theory research program. For the full atlas of interconnected papers, see [spectralbranding.com/atlas](https://spectralbranding.com/atlas).*
