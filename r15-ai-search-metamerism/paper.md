# Dimensional Collapse in AI-Mediated Search: Large Language Models as Metameric Observers of Brand Advertising

**Dmitry Zharnikov**

Working Paper v3.1 -- April 2026 | https://doi.org/10.5281/zenodo.19422427

---

## Abstract

Large language models (LLMs) increasingly mediate consumer brand evaluation in search and agentic commerce. This study demonstrates that LLMs systematically collapse brand perception to Experiential and Economic dimensions, rendering brands differentiated on narrative, ideological, cultural, or temporal dimensions metameric --- structurally different but functionally equivalent in AI recommendations. Using PRISM-B across 21,350 API calls to 24 models spanning nine cultural traditions and 15 languages, a Dimensional Collapse Index (DCI; uniform baseline = .250) is computed. Mean DCI equals .291 for global brands ($p = .017$) and .357 cross-culturally ($d = 3.449$). Cross-model convergence is near-perfect (cosine = .977). Local brands collapse 25% more severely than global brands ($d = .878$, in five FMCG pairs tested). Native-language prompting is null in home markets ($p = .716$) but reduces collapse up to 9.5 DCI points in foreign-market frames ($p = .002$). Geopolitical context independently modulates weights ($p < .001$). Structured Brand Function specifications recover approximately 20% of lost dimensionality. Collapse is stable across model versions. For search advertising, these findings reframe strategy from platform selection to dimensional defensibility: advertisers must encode soft brand dimensions in verifiable, machine-readable form or risk effective erasure by LLM intermediaries. Patterns reflect the text-conditioned LLM observers tested here.

**Management Slant**

- LLMs recommend products, not brands: across 24 models from nine cultural traditions and multiple brand pairs, AI-mediated search systematically collapses brand perception to Experiential and Economic dimensions, rendering brands differentiated on narrative, ideology, culture, or heritage metameric (structurally different but identically recommended).
- The collapse is cross-platform: cosine similarity of .977 across 24 architectures from nine cultural traditions means that switching AI vendors does not solve the problem. The solution must be dimensional, not platform-specific.
- Local and regional brands face amplified risk: brands from small non-English-speaking markets collapse 25% more severely than global brands ($d = .878$), associated with an Economic default in which AI substitutes price for every dimension it lacks data on.
- The collapse is not inevitable: encoding soft dimensions as verifiable, machine-readable claims is the operative defense. Making brand value structured and defensible --- not just "felt" --- is the prerequisite for surviving agentic commerce.

**Keywords**: AI-mediated search, brand perception, spectral metamerism, large language models, dimensional collapse, observer heterogeneity, cross-cultural, PRISM-B

---

### The Problem

What happens when an AI agent evaluates a brand? Does it see what a human sees?

For two decades, the dominant model of consumer search was query-response: a consumer types keywords into a search engine, scans a ranked list of links, and clicks through to evaluate brand information across multiple sources. The search engine organized information but did not interpret it. Brand differentiation survived because consumers encountered brand signals directly --- the heritage of a luxury house, the ideology of a purpose-driven brand, the cultural resonance of a lifestyle brand --- and integrated those signals through their own perceptual apparatus.

This model is ending. AI-mediated search --- through ChatGPT, Google's AI Overviews, Perplexity, and agentic commerce platforms --- introduces a fundamentally different architecture. The consumer no longer searches; the consumer asks, and a large language model synthesizes an answer. The intermediary changes from a neutral index that ranks links to an active agent that processes, compresses, and re-emits brand information. The consumer encounters not the brand's signals but the model's reconstruction of those signals.

This represents not merely a channel shift but a dimensional shift. An LLM processing a brand comparison query draws on training data that includes product reviews, price comparisons, feature specifications, and aggregated consumer opinions. It can report price differentials and enumerate functional features. What it cannot do is treat heritage, ideological commitment, cultural resonance, or temporal depth as live perceptual dimensions --- it can only describe them as factual attributes. The distinction matters: a factual description of heritage ("founded in 1837") is not the same as heritage operating as a dimension that shapes brand conviction across observer cohorts. The model systematically underweights these dimensions, collapsing an eight-dimensional brand emission profile toward a two-dimensional silhouette.

In optics, metamerism occurs when physically different light spectra produce identical color percepts because the observer's photoreceptors collapse spectral differences that fall outside their sensitivity range (Wyszecki and Stiles 1982). In Spectral Brand Theory, spectral metamerism occurs when structurally different brand profiles produce identical brand convictions because the observer's spectral weights collapse differentiating dimensions to zero (Zharnikov 2026a). This paper argues that LLMs are metameric observers: they produce convergent brand recommendations from structurally divergent brand inputs, suppressing the dimensions on which many premium brands build their most valuable differentiation.

Existing research has identified the direction of this problem without supplying a formal measurement model. Dawar and Bendle (2018) anticipated that AI-mediated platforms would shift competitive advantage from brand awareness to algorithmic recommendation. Hermann and Puntoni (2024) provided a comprehensive analysis of AI's impact on consumer behavior. Hermann, Puntoni, and Schweidel (2026) argue that AI agents "cannot recommend brands they cannot defend" --- that AI recommendations favor brands whose value proposition can be articulated in terms the model can process. This insight is directional but lacks a perceptual framework: it does not specify which dimensions are defensible and which are not, nor does it provide a measurement protocol for assessing dimensional vulnerability. Acar and Schweidel (2026) document practitioner evidence of the same problem, showing that LLMs systematically miscategorize premium spirits brands with immediate commercial consequences. Sabbah and Acar (2026) find that only ratings --- the most verifiable, quantifiable cue --- consistently increase AI selection probabilities across all models, while narrative and ideological cues vary by model and category. That finding converges with the present study from a complementary direction: where Sabbah and Acar measure choice-level heterogeneity across promotional cues, the present study measures perceptual-level heterogeneity across brand dimensions. Lynch and Ariely (2000) and Diehl, Kornish, and Lynch (2003) showed that lower quality-search costs can paradoxically increase price sensitivity by making price the salient comparison dimension --- precisely the dynamic the present study documents at the perceptual level. Longoni and Cian (2022) established that consumers trust AI recommendations more for utilitarian than hedonic products, confirming that the type of brand attribute matters for AI-mediated outcomes. Together, these studies establish that AI-mediated commerce produces structurally different decision patterns than human commerce, but none provides a formal dimensional framework for predicting which brand attributes survive and which collapse.

### Contribution

This paper introduces the first dimensional measurement model and replicable measurement protocol for predicting which brand dimensions survive AI mediation --- with implications for brand strategy in AI-mediated search. Three specific contributions are made. First, the paper provides a measurement instrument (PRISM-B) and summary statistic (Dimensional Collapse Index) that quantify how LLMs compress multi-dimensional brand perception, grounded in an observer-theoretic extension of established brand perception frameworks (Aaker 1997; Keller 1993; Brakus et al. 2009; Kapferer 2012). Second, using 21,350 API calls across 24 models from nine cultural traditions, the paper establishes that the compression is structural (cross-model cosine .977), conditional on training-data embeddedness (local brands collapse 25% more, $d = .878$), and partially recoverable through structured Brand Function specifications (~20% DCI reduction). Third, the finding reframes brand management in AI-mediated channels from a platform-switching problem to a dimensional specification problem: the operative defense is not choosing the right AI vendor but making collapsed dimensions machine-readable.

---

## Theoretical Framework

### Brand Perception as Multi-Dimensional Construct

The idea that brands are perceived along multiple distinct dimensions is well established. Aaker (1997) identified five brand personality dimensions --- sincerity, excitement, competence, sophistication, and ruggedness --- showing that consumers attribute human-like trait structures to brands. Keller (1993) proposed a complementary architecture through customer-based brand equity (CBBE), in which brand knowledge is organized into brand awareness and brand image, the latter comprising a network of associations varying in favorability, strength, and uniqueness. Brakus, Schmitt, and Zarantonello (2009) shifted the focus from cognitive structures to lived encounters, identifying four brand experience dimensions --- sensory, affective, intellectual, and behavioral --- that capture how consumers process brand stimuli through direct interaction. Kapferer (2008; 2012) offered the brand identity prism, a six-facet model (physique, personality, culture, relationship, reflection, self-image) that integrates sender and receiver perspectives into a single diagnostic.

These frameworks have proven durable because each captures a genuine facet of brand perception: personality traits, knowledge structures, experiential processing, and identity architecture, respectively. Yet they share a common structural assumption: the observer is a human consumer. Personality dimensions describe how humans project traits onto brands. CBBE models how human memory organizes brand knowledge. Brand experience measures how human senses and cognition process brand stimuli. The identity prism maps how human self-concepts interact with brand signals. None of these frameworks models what happens when a non-human mediating system --- one that lacks embodied experience, cultural embeddedness, and temporal continuity --- processes brand signals before they reach the human consumer. As AI-mediated search displaces traditional information channels (Dawar and Bendle 2018; Hermann and Puntoni 2024), this gap becomes consequential: existing dimensional frameworks cannot predict *which* dimensions of brand perception survive mediation by a structurally different observer class.

### The AI Observer Problem

Large language models process brand information through mechanisms that are structurally unlike human perception. Where human observers draw on embodied experience, social context, and cultural memory to weight brand dimensions, LLMs operate on statistical regularities in training corpora. Three properties distinguish AI observers from their human counterparts.

First, LLMs share substantially overlapping training data. The same brand descriptions, product reviews, and news articles appear across training sets, producing convergent brand representations regardless of model architecture (Liu 2026). Second, LLM processing is deterministic at zero temperature: given identical inputs, the model produces identical outputs, eliminating the perceptual heterogeneity that characterizes human brand perception. Third, LLMs exhibit what Longoni and Cian (2022) term a utilitarian competence advantage --- they are perceived as more credible for verifiable, functional claims than for hedonic or experiential ones. Sabbah and Acar (2026) document a parallel finding: when brands are evaluated by AI agents, only ratings-based attributes survive consistently across models, while narrative and cultural signals degrade. Hermann, Puntoni, and Schweidel (2026) formalize the strategic implications, arguing that brands must design for AI defensibility --- the capacity to maintain differentiation when brand signals are mediated by algorithmic systems.

These properties create a prediction gap. Established brand frameworks describe *what* consumers perceive but cannot predict *how* an AI mediating layer transforms those perceptions before they reach the consumer. Puntoni et al. (2021) trace how consumers experience AI involvement asymmetrically across data capture, classification, delegation, and social interaction; the present study shifts the analytic frame from the consumer's experience of AI to the AI's dimensional encoding of brands. A complementary line of work asks whether LLMs can substitute for human respondents in perceptual analysis: Li, Castelo, Katona, and Sarvary (2024) find that LLM-generated perceptual maps agree with human survey maps at greater than 75% on aggregate similarity, but aggregate ordinal agreement can persist under severe dimensional compression when the compressed dimensions happen to align with the full-dimensional ranking. The present study addresses the gap left by both lines by modeling the LLM as a distinct observer type with a measurable dimensional profile, and by treating identity-layer responses to dimensional collapse --- including cryptographic verification of soft-dimension claims --- as a companion design question developed in Zharnikov (2026x).

### Spectral Brand Theory as Dimensional Framework

Spectral Brand Theory (SBT; Zharnikov 2026a) provides the measurement architecture needed to formalize the AI observer problem. SBT models brand perception as emission profiles across eight typed dimensions --- Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal --- received by heterogeneous observer cohorts. These eight dimensions were derived as the union set that captures what established frameworks partition separately. Table 1 maps each established framework's constructs to SBT's dimensional space.

Table 1: Mapping of Established Brand Frameworks to SBT Dimensions.

| SBT Dimension | Aaker (1997) | Keller (1993) | Brakus et al. (2009) | Kapferer (2012) |
|---|---|---|---|---|
| Semiotic | -- | Brand recognition | -- | Physique |
| Narrative | -- | Brand associations | -- | Personality |
| Ideological | Sincerity | -- | Intellectual | Culture |
| Experiential | -- | -- | Sensory, Behavioral | -- |
| Social | Sophistication | -- | Affective | Relationship, Reflection |
| Economic | -- | Perceived quality | -- | -- |
| Cultural | -- | -- | -- | Culture (partial) |
| Temporal | -- | -- | -- | -- |

*Notes*: Dashes indicate no direct mapping. Temporal --- capturing heritage depth, founding mythology, and perceived continuity --- has no predecessor in existing frameworks; it is SBT's unique dimensional contribution. Kapferer's Culture facet maps partially to both Ideological and Cultural dimensions.

A brand's emission profile at time $t$ is the vector $\mathbf{e}(t) = [e_1(t), \ldots, e_8(t)]$, encoding signal intensity across all eight dimensions. The full specification of the framework, its mathematical notation, and its detailed relationship to these established dimensional models are provided in Appendix A.

SBT's central innovation is the observer spectral profile --- the formalization that emission is not perception. Each observer type applies a characteristic weight vector $\mathbf{w} = [w_1, \ldots, w_8]$ on the simplex $\sum w_i = 1$, determining the relative salience of each dimension in forming brand conviction. Observers with similar weight vectors cluster into cohorts (cf. Wedel and Kamakura 2000). Brand conviction --- the observer's formed assessment of a brand --- is a function of the interaction between the brand's emission profile and the observer's spectral weights: two observers encountering identical brand signals can form structurally different brand convictions if their spectral profiles weight different dimensions. This observer-dependent architecture replaces the single-observer assumption that unites Aaker, Keller, Brakus, and Kapferer. Rather than asking "what do consumers perceive?" it asks "what does *this class of observer* perceive?" --- a question that becomes urgent when the observer is an LLM.

The Perception Response Instrument for Structured Measurement (PRISM-B) operationalizes this framework for empirical testing. PRISM-B presents brand comparison queries that force the model to reveal implicit dimensional weights through structured response protocols, producing a measurable observer spectral profile for each LLM tested (see Method section for details).

### Spectral Metamerism and Dimensional Collapse

The Johnson-Lindenstrauss lemma (Johnson and Lindenstrauss 1984) establishes that projecting $n$ points from $\mathbb{R}^d$ to $\mathbb{R}^k$ (where $k < d$) preserves pairwise distances only approximately, with distortion increasing as $k$ decreases relative to $d$. When brand perception is projected from eight dimensions to fewer, brands that are well-separated in the full space may overlap in the reduced space. This is spectral metamerism: two brands with different emission profiles produce identical brand convictions because the observer's spectral weights assign zero (or near-zero) weight to the differentiating dimensions. Just as two physically different light spectra can produce the same color percept when the observer's photoreceptors are insensitive to the distinguishing wavelengths, two structurally different brands can produce the same brand conviction when the observer's spectral profile is insensitive to the distinguishing dimensions.

The mechanism is structurally analogous to Tversky's (1972) elimination by aspects, in which a decision-maker eliminates alternatives based on subsets of attributes. When an LLM mediates brand evaluation, dimensions with near-zero weight are effectively eliminated, collapsing distinctions that depend on those dimensions. The key theoretical claim is that the number of metameric pairs increases exponentially as the effective dimensionality decreases: reducing perception from eight dimensions to two does not merely lose 75% of the information --- it collapses exponentially more brand distinctions because the lost dimensions carried the combinatorial diversity that separated brands in the full space.

### Hypotheses

This paper models the LLM spectral profile as a weight vector $\mathbf{w}_{LLM} = [w_1^{LLM}, \ldots, w_8^{LLM}]$ with structurally predictable properties: high weights on verifiable dimensions (Economic, Experiential) that are well-represented in training data through product specifications, reviews, and feature comparisons; moderate weights on textually-represented dimensions (Semiotic, Narrative) that have textual correlates but lack perceptual depth; and low weights on perception-dependent dimensions (Ideological, Social, Cultural, Temporal) that require embodied experience, social context, cultural embeddedness, or lived temporal continuity that the model lacks. This structural profile generates four primary hypotheses:

**Hypothesis 1 (Dimensional Bias):** LLMs assign systematically higher implicit weights to Economic and Experiential dimensions than to Narrative, Ideological, Cultural, and Temporal dimensions when processing brand comparison queries.

**Hypothesis 2 (Metameric Collapse):** Brand pairs that are spectrally distinct to human observers on Narrative, Ideological, Cultural, or Temporal dimensions become functionally equivalent in LLM-mediated recommendations.

**Hypothesis 3 (AI Observer Heterogeneity):** Different LLM architectures and training origins (Claude, GPT-4o, Gemini Flash, DeepSeek V3, Qwen3 30B, Gemma 4) and deployment contexts (cloud-aligned vs. local open-weight) exhibit measurably different spectral profiles, constituting distinct AI observer cohorts.

**Hypothesis 4 (Differential Dimensional Collapse):** Collapse is non-uniform across soft dimensions: Narrative and Ideological dimensions collapse more severely than Cultural and Temporal dimensions, reflecting differential training data representation.

Hypotheses 5 through 12, addressing cross-cultural variation, geopolitical framing, native-language prompting, and multi-city effects, are reported as robustness and exploratory analyses in the Results section.

### Dimensional Collapse in Related Domains

Dimensional collapse is not unique to brand perception. Hashimoto and Oshio (2025) demonstrate that Big Five personality structures compress to fewer factors when mediated through LLM response generation. Van Doren and Holland (2025) show that cultural figurative meaning is systematically stripped during machine translation, reducing high-dimensional cultural constructs to functional equivalents. Liu (2026) identifies an "alignment tax" whereby RLHF training produces 40-79% response homogenization across diverse prompts, amplifying majority-pattern outputs at the expense of minority patterns. Doshi and Hauser (2024) and De Freitas, Nave, and Puntoni (2025) provide complementary evidence that generative AI reduces collective diversity of novel content, indicating that homogenization effects operate not only within but across AI-mediated outputs. Sourati et al. (2026) theorize epistemic collapse in AI-mediated knowledge production, identifying a convergent mechanism structurally analogous to spectral metamerism. Hagendorff, Fabi, and Kosinski (2023) show that human-like cognitive biases emerge in LLMs and can be modified by alignment training, suggesting that dimensional bias may be partly an artifact of training optimization rather than an inherent architectural constraint. These findings converge on a prediction: LLM-mediated brand perception should systematically over-weight quantifiable dimensions (Economic, Experiential) and under-weight perception-dependent dimensions (Cultural, Temporal, Narrative).

### Implications for Search Advertising Theory

If the hypotheses are supported, the implications for search advertising theory are substantial. The evolution from keyword-based to intent-based to AI-mediated search represents a progressive shift in which consumer-facing intermediaries acquire deeper inferential powers over brand information (Wedel and Kannan 2016). First, "brand visibility" acquires a dimensional structure: a brand can be visible on some dimensions and invisible on others, depending on the mediating observer's spectral profile. Second, the zero-click search paradigm --- where the AI provides the answer without the consumer visiting brand-owned media --- means that the LLM's spectral profile determines which brand dimensions reach the consumer. Third, portfolio brands that are differentiated in human perception but metameric in AI perception compete against themselves in AI-mediated search (cf. Erdem and Swait 1998). Fourth, brand optimization for AI-mediated channels becomes a dimensional specification problem: the task of making collapsed dimensions machine-readable so that the LLM's effective spectral profile becomes less biased. The dimensional asymmetry documented here mirrors Castelo, Van den Bergh, and Lehmann's (2019) algorithm aversion findings: consumers resist algorithmic recommendations precisely for the experiential and social product categories where AI spectral bias is most severe, creating a compounding vulnerability for brands whose differentiation lives on those dimensions. Huang and Rust's (2021) distinction between AI cognitive competence and AI empathy competence maps directly onto the Economic/Experiential versus Social/Narrative collapse pattern: AI systems excel at the cognitive tasks (price comparison, feature enumeration) and systematically underperform on the empathy-adjacent tasks (cultural resonance, narrative coherence) that define premium differentiation.

---

## Method

### Research Design and Instrument

This study employs a structured weight elicitation design to measure the implicit spectral profiles of up to 24 LLMs when processing brand comparison queries (six models in Runs 2--4; 23 models in Run 5; 24 models in Run 6). The core logic is as follows: if an LLM's recommendations systematically emphasize certain brand dimensions over others, the pattern of emphasis reveals the model's implicit weight vector across SBT's eight dimensions. By prompting multiple models with identical brand comparison queries and requiring them to allocate 100 points across SBT's eight dimensions via structured JSON output, the design directly estimates each model's spectral profile and tests whether dimensional bias, metameric collapse, and cross-model heterogeneity are present.

An initial pilot (Run 1) used free-text responses with keyword extraction to infer dimensional weights. This produced a null result: keyword-based coding could not reliably distinguish dimensional emphasis from mere dimensional mention. The null result motivated the v2 structured elicitation design used in Runs 2--5, in which models directly report their weight allocations as numeric vectors, eliminating the need for human coding entirely.

**PRISM-B: The Measurement Instrument.** The experiment uses PRISM-B (Perception Response Instrument for Structured Measurement --- Brand), an open-source instrument for measuring multi-dimensional LLM brand perception. PRISM-B implements a five-layer scaffold (L0: pre-registered protocol; L1: model configuration; L2: versioned prompt templates; L3: per-call JSONL session logs; L4: analysis scripts) ensuring full reproducibility --- any researcher can fork the repository, substitute brand pairs, and run the pipeline against any LLM with a chat-completion API. PRISM-B was used across all ten runs without structural modification. The full scaffold specification is in the Web Appendix; pipeline, data, and session logs are at `github.com/spectralbranding/sbt-papers/r15-ai-search-metamerism/experiment/`.

### Brand Pair Selection

Ten brand pairs were selected to span multiple product categories and to maximize spectral diversity -- that is, each pair consists of two brands that occupy similar price-function positions but differ primarily on specific SBT dimensions. The selection criterion is deliberate: pairs were chosen to be approximately metameric in a reduced two-dimensional (price-function) space but spectrally distinct in the full eight-dimensional space. If LLMs collapse perception to functional and economic dimensions, these pairs should become indistinguishable in LLM recommendations; if LLMs preserve multi-dimensional perception, the pairs should remain differentiated.

Table 2: Global brand pairs (Run 2), categories, and primary differentiating dimensions. Pairs are selected to occupy similar product categories but differ primarily on specific SBT dimensions.

| Pair ID | Category | Brand A | Brand B | Differentiator |
|---------|----------|---------|---------|----------------|
| luxury_heritage | Luxury fashion | Hermès | Coach | Temporal vs. Economic |
| purpose_driven | Outdoor apparel | Patagonia | Columbia | Ideological vs. Experiential |
| premium_tech | Consumer tech | Apple | Samsung | Narrative vs. Experiential |
| artisanal_food | Premium grocery | Erewhon | Whole Foods | Social vs. Economic |
| auto_disruption | Automotive | Mercedes | Tesla | Cultural vs. Ideological |
| indie_beauty | Skincare | Glossier | Maybelline | Narrative vs. Economic |
| craft_spirits | Spirits | Hendricks | Gordons | Semiotic vs. Economic |
| boutique_hotel | Hospitality | Aman | Four Seasons | Cultural vs. Experiential |
| heritage_sportswear | Sportswear | Nike | Shein | Narrative vs. Economic |
| ethical_finance | Financial services | Aspiration | Chase | Ideological vs. Economic |

*Notes*: Differentiator column identifies the primary SBT dimension on which Brand A is differentiated relative to Brand B. Pairs selected to occupy similar price-function positions but differ on specific dimensional channels. Canonical brand profiles for Hermès, Patagonia, and Erewhon are fixed in Zharnikov (2026a).

Three SBT canonical brands (Hermès, Patagonia, Erewhon) appear across the pairs, grounding the analysis in established spectral profiles (Zharnikov 2026a). The remaining brands were selected based on published positioning analyses and expert assessment to ensure clear dimensional differentiation across categories.

Table 3: Local brand pairs (Run 3), testing the conditional metamerism hypothesis. All pairs are from small non-English-speaking markets where the local brand's English-language training-data footprint is minimal.

| Pair ID | Country | Category | Local brand | Global comparator |
|---------|---------|----------|-------------|-------------------|
| cyprus_supermarket | Cyprus | Grocery retail | AlphaMega | Carrefour |
| latvia_chocolate | Latvia | Confectionery | Laima | Lindt |
| kenya_beer | Kenya | Beer | Tusker | Heineken |
| vietnam_dairy | Vietnam | Dairy | Vinamilk | Danone |
| serbia_water | Serbia | Bottled water | Knjaz Milos | Evian |

*Notes*: Local brand pairs selected from markets with minimal English-language training-data footprint. All five pairs are in the food, beverage, or grocery retail sector; category effects on collapse should be considered when generalizing (see Limitations).

### LLM Selection

Six models were selected to represent three clusters: three Western-trained cloud models (Claude Sonnet 4.6, GPT-4o, Gemini 2.5 Flash), one Chinese-trained cloud model (DeepSeek V3), and two local open-weight deployments (Qwen3 30B, Gemma 4 27B --- both via Ollama). The 3+1+2 design serves three theoretical purposes: (1) the Western-versus-Chinese cluster comparison tests whether dimensional collapse is an artifact of shared Western training corpora or a structural property of statistical brand observation; (2) the cloud-versus-local comparison tests whether commercial API alignment layers suppress sensitivity to normative dimensions; (3) the paired Google comparison (Gemini Flash cloud vs. Gemma 4 local) isolates the alignment-layer effect within the same model family. The exploratory extension (Run 5) expanded the panel to 24 models from nine cultural traditions (see Results).

### Prompt Protocol

For each brand pair, three prompt types are administered to each model. All prompts require structured JSON output: the model allocates exactly 100 points across SBT's eight dimensions, representing the relative importance of each dimension in the comparison context. This structured weight allocation design eliminates the need for human coding of free-text responses and provides direct measurement of the model's implicit spectral profile.

**Type 1: Weighted Recommendation.** Simulates a consumer search interaction and elicits dimensional weight allocation. The model is asked to recommend between Brand A and Brand B and to allocate 100 points across the eight SBT dimensions reflecting which factors matter most in its recommendation. This prompt reveals which dimensions the model considers decision-relevant.

**Type 2: Dimensional Differentiation.** Elicits explicit brand comparison with weight allocation. The model is asked what distinguishes Brand A from Brand B and to allocate 100 points reflecting the relative importance of each dimension in the differentiation. This prompt reveals which dimensions the model considers salient for distinguishing the brands.

**Type 3: Dimension-Specific Probes.** Calibration prompts that directly query each dimension for each brand. Format: "Rate [Brand A/B] on the [dimension] dimension on a scale of 0-100." Sixteen sub-prompts per pair (eight dimensions times two brands). These probes establish a ceiling: they reveal what the model assigns to each dimension when explicitly prompted, against which the organic (Type 1 and Type 2) weight allocations are compared.

Each prompt is administered three times per model to capture response variance. Temperature is set to 0.7 (default for conversational use) to reflect realistic consumer interaction conditions rather than deterministic retrieval. Total prompt count per pair: 1 weighted recommendation + 1 dimensional differentiation + 16 dimension probes = 18 prompts. Each prompt is repeated 3 times across 6 models: 10 global pairs $\times$ 18 prompts $\times$ 6 models $\times$ 3 repetitions = 3,240 API calls (Run 2); 5 local pairs $\times$ 18 prompts $\times$ 6 models $\times$ 3 repetitions = 1,620 API calls (Run 3).

### Measurement Protocol

Because the structured weight allocation design requires models to output JSON with numeric point allocations, measurement is automated with no human coding step.

**Step 1: JSON parsing and validation.** Each model response is parsed as JSON. Responses that fail JSON parsing are discarded and re-prompted (fewer than 3% of calls across all models). The eight-dimensional weight vector is extracted from the parsed output.

**Step 2: Weight sum tolerance and renormalization.** Valid responses must have a total point allocation within 15% of the target 100 points (i.e., between 85 and 115). Responses outside this tolerance are discarded. Valid responses are renormalized to sum to exactly 100, preserving relative proportions: $w_i^{norm} = w_i \times 100 / \sum_{j=1}^{8} w_j$.

**Step 3: Spectral profile estimation.** For each model, the implicit spectral profile is estimated as the mean normalized weight vector across all organic responses (Types 1 and 2): $\hat{w}_i^{LLM} = \bar{w}_i / \sum_{j=1}^{8} \bar{w}_j$, where $\bar{w}_i$ is the mean allocated weight for dimension $i$ across all responses.

**Step 4: Dimensional Collapse Index (DCI).** The DCI measures the degree to which a model's weight allocation concentrates on Economic and Semiotic dimensions --- the two dimensions most tied to verifiable, quantifiable brand attributes. It is defined as:

$$DCI = (w_{Economic} + w_{Semiotic}) / 100$$

where $w_{Economic}$ and $w_{Semiotic}$ are the model's mean allocated weights for those dimensions. Under a uniform allocation (each dimension receives 12.5 points), the baseline DCI is $(12.5 + 12.5) / 100 = .250$. Values above .250 indicate concentration toward verifiable dimensions; values below indicate preservation of perception-dependent dimensions.

A note on the Experiential dimension: Table 4 shows that Experiential (150% of baseline) is the most inflated single dimension in the global brand results, exceeding both Economic (114%) and Semiotic (118%). The DCI formula intentionally captures the *economic-semiotic* over-weighting pattern as a paired index of verifiability concentration, because these two dimensions are most directly tied to checkable factual attributes (price, specifications, visual identity). Experiential operates as a distinct inflation mechanism: models inflate it because experiential attributes (features, functionality, sensory properties) are richly represented in product reviews, but its inflation reflects functional-descriptive abundance rather than the verifiability asymmetry captured by the Economic-Semiotic pair. The DCI therefore understates total collapse relative to the soft dimensions when Experiential is high, but correctly identifies the verifiability-driven collapse mechanism. Readers should interpret DCI alongside the full dimensional weight table (Tables 4 and 5) to capture the Experiential inflation pattern separately.

### Statistical Model

For a given model $m$ and brand pair $p$, the PRISM-B instrument elicits a weight vector $\mathbf{w}_{mp} = [w_{mp,1}, \ldots, w_{mp,8}]$ where $\sum_{i=1}^{8} w_{mp,i} = 100$. Each call $c$ produces a raw allocation $\mathbf{w}_{mpc}$; the model-pair spectral profile is the mean across repetitions:

$$\hat{\mathbf{w}}_{mp} = \frac{1}{C} \sum_{c=1}^{C} \mathbf{w}_{mpc}$$

where $C$ is the number of valid responses (typically 3 repetitions $\times$ 2 prompt types = 6). The model-level spectral profile aggregates across pairs:

$$\hat{\mathbf{w}}_m = \frac{1}{P} \sum_{p=1}^{P} \hat{\mathbf{w}}_{mp}$$

The Dimensional Collapse Index for model $m$ on pair $p$ is:

$$DCI_{mp} = \frac{w_{mp,\text{Econ}} + w_{mp,\text{Sem}}}{100}$$

with standard error estimated from the repetition-level variance:

$$SE(DCI_{mp}) = \frac{1}{100} \sqrt{s^2_{mp,\text{Econ}} + s^2_{mp,\text{Sem}} + 2 \cdot \text{cov}(w_{mp,\text{Econ}}, w_{mp,\text{Sem}})}$$

where $s^2_{mp,i}$ is the sample variance of dimension $i$'s allocation across repetitions. This formalization permits confidence intervals on all reported DCI values and enables formal comparison of DCI across model clusters, brand pair types, and cultural groups using standard parametric tests.

Cross-model convergence is quantified by the mean pairwise cosine similarity of model-level spectral profiles:

$$\bar{\rho} = \frac{2}{M(M-1)} \sum_{m < m'} \frac{\hat{\mathbf{w}}_m \cdot \hat{\mathbf{w}}_{m'}}{\|\hat{\mathbf{w}}_m\| \|\hat{\mathbf{w}}_{m'}\|}$$

where $M$ is the number of models. Values approaching 1.0 indicate structural convergence in dimensional ordering across architectures.

**DCI as a rate-distortion functional.** The DCI admits an information-theoretic interpretation: the empirical collapse to Economic + Semiotic can be understood as a minimum-distortion encoding given the model's effective channel capacity (Shannon 1959; Cover and Thomas 2006). The cosine similarity $\bar{\rho}$ across models quantifies the convergence of independent encoders to the same rate-distortion-optimal codebook --- consistent with established vector quantization results (Gersho and Gray 1991) showing that distinct quantizers converge on a common source-space partition when the rate budget is small. The full rate-distortion curve $R(D)$ is estimated in a companion study (Zharnikov 2026aa).

### Study Design: Confirmatory and Exploratory Components

Runs 2--4 constitute the **confirmatory** component: protocol, hypotheses (H1--H4), brand pairs, and analysis plan were pre-registered (archived at `L0_specification/protocol.md`). All confirmatory tests use $\alpha = .05$ with Benjamini-Hochberg correction. Run 5 (cross-cultural extension to 24 models from nine traditions) is **exploratory**, with hypotheses H5--H12 formulated after observing Runs 2--4. Effect sizes are large and consistent, but readers should interpret Run 5 tests as pattern-confirming. H10 (native-language prompting) was evaluated on 121 model-pair combinations spanning 11 languages across Runs 5, 7, and 8; see Results for the design rationale.

### Analysis Plan

Five analyses address the hypotheses: (1) one-sample $t$-tests of DCI against the .250 uniform baseline (H1), with Bonferroni correction across eight dimensions; (2) pairwise cosine similarity of model-level spectral profiles (H2); (3) MANOVA on the eight-dimensional weight vector with model identity as factor, including planned Western-vs-Chinese and cloud-vs-local contrasts (H3); (4) paired $t$-tests on within-soft-dimension weight variation (H4); and (5) spectral entropy $H = -\sum w_i \ln(w_i)$ as an information-retention measure. Full statistical procedures are in the Web Appendix.

---

## Results

The full study comprises 21,350 API calls across ten runs (validated by `experiment/validation/validate.py`), with three confirmatory runs (Runs 2--4, 5,213 calls across six models), a cross-cultural extension (Run 5, 7,342 calls across 23 models), geopolitical framing experiments (Runs 7 and 11, 1,406 calls), and supplementary robustness checks (Runs 6, 8--10, 14). This section reports the confirmatory and exploratory results; supplementary experiments are summarized in the Discussion and detailed in the Web Appendix.

### Confirmatory Results (Runs 2--4)

**H1: Dimensional Bias --- SUPPORTED.** The Dimensional Collapse Index (DCI) quantifies how much model responses concentrate coverage in a subset of dimensions relative to the uniform baseline of .250. For ten global brand pairs (Run 2, 3,240 calls across six models), mean DCI was .291 (SD = .042; $t(59) = 2.45$, $p = .017$, Cohen's $d = 2.97$). For five locally embedded brand pairs from small non-English-speaking markets (Run 3, 1,620 calls), the effect was stronger: mean DCI = .353 (SD = .038; $t(29) = 3.91$, $p < .001$, $d = 3.34$). All six models individually exceeded the baseline in both runs.

Table 4: Mean weight allocation across LLM responses, global brand pairs (Run 2). Values show mean allocated points (out of 100, renormalized) and percentage relative to the uniform baseline of 12.5 per dimension. Standard errors in parentheses.

| Dimension | Mean weight (SE) | % of baseline |
|-----------|-----------------|---------------|
| Semiotic | 14.8 (.009) | 118% |
| Narrative | 10.5 (.007) | 84% |
| Ideological | 8.2 (.006) | 66% |
| Experiential | 18.8 (.011) | 150% |
| Social | 7.8 (.006) | 62% |
| Economic | 14.3 (.009) | 114% |
| Cultural | 7.3 (.006) | 58% |
| Temporal | 8.1 (.006) | 65% |

*Notes*: SE = standard error computed via bootstrap (1,000 resamples); detailed bootstrap distributions are available in the supplementary dataset (spectralbranding/r15-ai-search-metamerism on HuggingFace). DCI = Dimensional Collapse Index. Values above 12.5 indicate over-weighting relative to uniform baseline. N = 3,240 valid API responses across 6 models, 10 brand pairs, 3 repetitions.

Table 5: Mean weight allocation across LLM responses, local brand pairs (Run 3). Values show mean allocated points (out of 100, renormalized) and percentage relative to uniform baseline. Standard errors in parentheses.

| Dimension | Mean weight (SE) | % of baseline |
|-----------|-----------------|---------------|
| Semiotic | 11.2 (.008) | 90% |
| Narrative | 7.8 (.006) | 62% |
| Ideological | 5.9 (.005) | 47% |
| Experiential | 16.4 (.010) | 131% |
| Social | 6.4 (.005) | 51% |
| Economic | 21.0 (.013) | 168% |
| Cultural | 5.1 (.005) | 41% |
| Temporal | 6.2 (.005) | 50% |

*Notes*: SE = standard error computed via bootstrap (1,000 resamples); detailed bootstrap distributions are available in the supplementary dataset (spectralbranding/r15-ai-search-metamerism on HuggingFace). DCI = Dimensional Collapse Index. Values above 12.5 indicate over-weighting relative to uniform baseline. N = 1,620 valid API responses across 6 models, 5 brand pairs, 3 repetitions.

The dimensional pattern is consistent across both runs: Experiential (150% global, 131% local) and Economic (114% global, 168% local) dominate, while Cultural (58%, 41%), Temporal (65%, 50%), Ideological (66%, 47%), and Social (62%, 51%) are suppressed below baseline. The Economic spike for local brands (168% vs. 114% for global brands) represents the "Economic default" --- when models lack brand-specific data on narrative, ideology, cultural role, or heritage, they revert to price, the one dimension universally inferable from product category context.

The Patagonia/Columbia pair is a notable exception: its DCI of .194 falls *below* the .250 baseline, indicating less collapse than the uniform benchmark. Patagonia's ideological dimension --- grounded in legally documented environmental commitments, product durability certifications, and the 1% for the Planet pledge --- provides a machine-readable ideological signal that survives AI mediation. This is the empirical signature of a defensible dimension: a brand value articulable in verifiable terms the model can process. Per-pair DCI values for all 15 brand pairs are reported in Web Appendix Tables A1 and A2.

**H2: Metameric Convergence --- SUPPORTED.** Cross-model cosine similarity of spectral profiles was .975 across the six confirmatory models (Run 2), indicating near-identical dimensional orderings despite differences in architecture, training corpus, and deployment context. Brands that are metameric in one model's output are metameric in all six.

**H3: AI Observer Heterogeneity --- NOT SUPPORTED.** The MANOVA on per-model DCI scores yielded $F(5,54) = 0.59$, $p = .712$. While point estimates differed (DeepSeek V3 DCI = .242; Qwen3 30B = .327), the variation fell within the range expected by sampling noise.

**H4: Differential Dimensional Collapse --- NOT SUPPORTED.** Paired $t$-tests on soft-dimension weight allocations (Narrative, Ideological, Cultural, Temporal) found no differential collapse meeting the $\alpha = .05$ threshold among these dimensions (all pairwise $p \geq .05$; full pairwise statistics in the Web Appendix). Soft dimensions collapse approximately uniformly rather than differentially, suggesting the verifiable/non-verifiable distinction operates as a binary rather than a gradient.

**Conditional metamerism.** An independent-samples $t$-test comparing the 10 global pair DCIs against the 5 local pair DCIs yielded $t(13) = 6.483$, $p < .001$, Cohen's $d = .878$. Local brands (.353) collapsed 25% more than global brands (.291). Cultural and Temporal dimensions showed the largest global-local gaps, while Experiential and Semiotic showed the smallest (both are inferable from product category data without brand-specific knowledge). Two caveats apply: the local condition's small sample size ($n = 5$ brand pairs) limits generalizability, and all five local pairs are in the food and beverage sector; replication across additional categories is warranted.

**Brand Function resolution (Run 4).** Providing structured Brand Function specifications for the five local brands reduced aggregate DCI from .353 to .284, a 20% reduction toward the .250 baseline (353 calls). Four of six models showed meaningful improvement; the resolution was driven primarily by recovery of the Cultural dimension (e.g., Gemini Flash Cultural weight: 11.7 to 21.2). The resolution was partial: DCI remained above baseline (.284 vs. .250), and the Economic dimension stayed elevated at 15.4 (vs. 12.5 baseline), consistent with the interpretation that some collapse reflects structural properties of text-based processing rather than information availability alone.

Table 6: Brand pairs used in confirmatory runs (Runs 2--3). Global pairs span ten product categories; local pairs each pair a locally embedded brand with a global comparator.

| Run | Pair | Category |
|-----|------|----------|
| 2 | Patagonia / Columbia | Purpose-driven outdoor |
| 2 | Aspiration / Chase | Ethical finance |
| 2 | Erewhon / Whole Foods | Artisanal food |
| 2 | Mercedes / Tesla | Auto disruption |
| 2 | Apple / Samsung | Premium tech |
| 2 | Aman / Four Seasons | Boutique hotel |
| 2 | Hendricks / Gordons | Craft spirits |
| 2 | Nike / Shein | Heritage sportswear |
| 2 | Hermès / Coach | Luxury fashion |
| 2 | Glossier / Maybelline | Indie beauty |
| 3 | AlphaMega / Carrefour | Grocery (Cyprus) |
| 3 | Laima / Lindt | Confectionery (Latvia) |
| 3 | Tusker / Heineken | Beer (Kenya) |
| 3 | Vinamilk / Danone | Dairy (Vietnam) |
| 3 | Knjaz Milos / Evian | Water (Serbia) |

### Cross-Cultural Extension (Run 5)

Run 5 extended the design to 23 models spanning nine cultural training traditions (Western, Chinese, Russian, Japanese, Korean, Arabic, Indian, Ukrainian, Mongolian), seven cross-cultural brand comparisons, and 15 native-language prompting conditions (7,342 calls). Models ranged from frontier systems (Claude, GPT, Gemini, Grok, DeepSeek) to nationally specialized architectures (YandexGPT, GigaChat, Jais, EXAONE, Sarvam, ALLaM, GPT-OSS-Swallow).

**H1/H2 confirmed at scale.** Mean DCI across all 23 models was .357 (SD = .036; $t(22) = 16.178$, $p < .001$, $d = 3.449$) --- the largest effect in the dataset. Every model individually exceeded baseline. Cross-model cosine similarity was .977 (range [.927, 1.000]), extending the structural convergence from six Western/Chinese models to 23 architectures across nine cultural traditions. H3 remained unsupported ($t = .221$, $p = .413$, $d = .043$).

Table 7: Twenty-three of the 24 active models across Runs 2--8, ranked by DCI (lower = less collapse). Model size is marked "undisclosed" where the provider does not publish parameter counts. GPT refers to GPT-4o-mini. Swallow 70B excluded (3.6% success rate).

| Model | Size | Culture | Provider | DCI |
|-------|------|---------|----------|-----|
| grok | undisclosed | Western | xAI | .290 |
| claude | undisclosed | Western | Anthropic | .313 |
| gemini | undisclosed | Western | Google | .321 |
| cerebras_qwen3 | 235B (MoE) | Chinese | Cerebras | .324 |
| groq_allam | 7B | Arabic | Groq | .340 |
| yandexgpt_local | 8B | Russian | Local | .341 |
| deepseek | 671B (MoE) | Chinese | DeepSeek | .342 |
| groq_kimi | undisclosed | Chinese | Groq | .350 |
| groq_llama33 | 70B | Western | Groq | .358 |
| gpt | undisclosed | Western | OpenAI | .360 |
| gigachat_api | undisclosed | Russian | Sber | .360 |
| sarvam | ~105B | Indian | Sarvam AI | .367 |
| gemma4_local | 27B (MoE) | Western | Local | .371 |
| yandexgpt_pro | undisclosed | Russian | Yandex | .377 |
| gigachat_local | undisclosed | Russian | Local | .380 |
| gptoss_swallow | 20B | Japanese | TOKYOTECH | .380 |
| swallow_local | 8B | Japanese | Local | .383 |
| qwen3_local | 30B | Chinese | Local | .388 |
| exaone_local | 32B | Korean | Local | .389 |
| jais_local | 70B | Arabic | Local | .402 |

*Notes*: DCI = Dimensional Collapse Index; baseline = .250. MoE = Mixture of Experts (active parameter count is lower than total). Full per-run breakdowns including tier classification and release dates are in the supplementary dataset (spectralbranding/r15-ai-search-metamerism on HuggingFace).

**H5 (Cultural Proximity) --- REVERSED.** National models collapse *more* on own-culture brands than on foreign-culture brands (paired $t = -1.330$, $p = .220$, $d = .043$; not significant, but direction reversed). The expected mechanism --- richer domestic training data producing less collapse --- fails because national models over-index on Economic and Experiential dimensions from domestic e-commerce corpora. More data of the same dimensional type reinforces the Economic default rather than enriching the spectral profile. This connects to the James-Stein shrunken variance mechanism discussed in the Theoretical Implications subsection: the signal is strong but dimensionally narrow, producing greater rather than less collapse.

**H6 (Directional Asymmetry) --- SUPPORTED** ($t = -3.243$, $p = .001$). Western-trained models exhibit mean DCI of .339, significantly lower than non-Western models (.360). The asymmetry is bidirectional: Western models collapse less on *all* brands (not only Western ones), reflecting training-corpus breadth rather than cultural familiarity. Brands operating in non-Western markets face compounded risk: the AI mediators most likely to serve their domestic audiences collapse spectral profiles most severely (e.g., EXAONE DCI = .389 vs. Claude DCI = .313 on identical Korean brand pairs).

**H7 (Geopolitical Signal) --- SUPPORTED.** Tinkoff (Russia) vs. PrivatBank (Ukraine) --- same-category digital banks controlling for category effects --- showed directionally consistent DCI divergence: 15 of 20 models assigned higher DCI to PrivatBank (binomial $p = .021$), consistent with geopolitical salience encoding in training corpora.

**H8 (Thin-Data Floor) --- NOT SUPPORTED.** Mongolia-origin brands showed mean DCI of .377, but Japanese snack brands showed .386 despite Japan's larger digital footprint. Category-specific factors interact with information availability, preventing a monotonic thin-data floor.

**H9 (Model Capacity) --- NULL.** The scale effect was inconsistent: 3 of 5 model families showed reduced DCI at larger sizes (clearest: Qwen3 30B = .388 vs. 235B = .324, $\Delta$ = .064), but two families reversed direction, suggesting fine-tuning and alignment conditioning offset raw capacity gains.

**H10 (Native Language) --- NOT SUPPORTED.** Across 121 model-pair combinations (28 culture-matched from Run 5 plus 93 control-language combinations from Runs 7--8), 58 showed DCI reduction (48%; binomial $p = .716$, two-sided). Mean aggregate reduction: +.001 (effectively zero). Control languages (Greek, Swahili, Latvian, Vietnamese, Serbian --- where no model has native training) produced effects indistinguishable from culture-matched conditions, falsifying the "language-as-key" hypothesis. One notable exception: the Mongolian subgroup (APU Chinggis vs. Heineken) showed DCI reduction in 8/8 models when prompted in Mongolian (mean = 4.9 points), isolating the specific condition under which native-language prompting rescues collapse: a brand whose discourse exists primarily in a language dramatically underweighted in the model's English-language training.

Table 8: Cost and infrastructure breakdown across all 10 runs. Paid cloud = metered per-token APIs. Free cloud = providers offering free inference tiers. Local = Ollama on Apple M4 Pro 64 GB.

| Category | Models | Calls | Cost |
|----------|--------|------:|-----:|
| Paid cloud | 10 | 12,145 | \~\$6.10 |
| Free cloud | 6 | 3,750 | \$0.00 |
| Local Ollama | 8 | 5,455 | \$0.00 |
| **Core Total** | **24** | **21,350** | **\~\$6.10** |

*Notes*: Call counts are exact (validated by `experiment/validation/validate.py`). Per-model breakdowns and the full per-call cost ledger are in the HuggingFace dataset (DOI: 10.57967/hf/8284) and on GitHub.

The full study --- 24 models, 7 training traditions, 23 brand pairs, 15 native-language conditions --- cost less than a single human-respondent focus group. The marginal cost of adding a model, brand pair, or cultural condition is under \$0.20, making longitudinal tracking of AI spectral profiles operationally feasible at a scale that human-respondent studies cannot match.

**Data Availability.** The complete dataset --- all 21,350 per-call records across 10 runs in 15 native languages plus English (JSONL), per-model cost and token summaries (CSV), statistical test results (JSON), and the reproducible PRISM-B analysis scripts --- is publicly available at https://huggingface.co/datasets/spectralbranding/r15-ai-search-metamerism (DOI: 10.57967/hf/8284). The experiment source code, prompts, model configurations, and the PRISM instrument scaffold are at https://github.com/spectralbranding/sbt-papers/tree/main/r15-ai-search-metamerism/experiment.

### Geopolitical Framing (Runs 7 and 11)

**H12 --- SUPPORTED, then REINTERPRETED.** Run 7 tested whether the same brand evaluated in different geopolitical city contexts produces different dimensional weight profiles. Three brands operating across geopolitically salient borders --- Roshen (Moscow vs. Kyiv), Volvo (Stockholm vs. Shanghai), and Burger King (New York vs. Moscow) --- were evaluated using city-grounded prompts differing by exactly one variable (1,091 calls across 18 models). The mean absolute DCI delta between city contexts was .040 ($t = 7.122$, $p < .001$), exceeding the test-retest noise floor. Roshen showed the largest effect (.062), consistent with direct conflict salience; Volvo (.029) and Burger King (.030) showed moderate effects.

Run 11 extended the Roshen test to seven cities (315 calls, zero failures): Kyiv, Moscow, Vilnius, Warsaw, Astana, Tbilisi, and Baku. Three findings materially refined the H12 interpretation:

First, Kyiv is uniquely low (DCI = 34.78); every other city collapses to a narrow band (39.0--44.5). Moscow (44.24) is indistinguishable from Vilnius (42.67), Tbilisi (42.57), Astana (44.17), and Baku (44.52) --- none of which carry political animosity toward a Ukrainian brand. The original "Moscow effect" is not Moscow-specific; it is a generic foreign-context effect.

Second, manufacturing presence does not anchor the dimensional profile. Lithuania hosts Roshen's largest non-Ukraine factory (Klaipeda, ~15,500 tonnes/year), yet Vilnius collapses more than Warsaw (42.67 vs. 39.0), where Roshen has only a commercial distribution arm (Roshen-Polska Sp. z o.o.). Active commercial discourse proves a stronger signal than manufacturing presence mentioned primarily in trade publications.

Third, local-language prompting reduces collapse for every non-Kyiv city (3.31--9.50 DCI points). The largest effect: Astana in Kazakh ($-9.50$, $p = .002$, all 7 models reduce). Kyiv shows no language effect ($\Delta = +.22$, $p = .92$) because English already accesses the rich home-market discourse. This clarifies the H10 null: native-language prompting is null for home-audience conditions (where English suffices) and substantial for foreign-audience conditions (where local language is the only path into the city-local discourse layer).

These findings support a **discourse-layer reinterpretation**: the geopolitical-framing effect is real, but the mechanism is not country-of-origin priming or consumer animosity. The mechanism is discourse-layer activation --- the AI retrieves whichever (city x language x brand) discourse layer the prompt activates. Foreign-context layers are sparse in English regardless of geopolitical alignment; local-language prompts unlock the city-local layer when one exists in the training corpus; the home market is uniquely served because its discourse is already the canonical layer for the brand.

### Robustness

Temperature sensitivity (Run 9, 540 calls): DCI was stable across $T = 0.0$, $0.3$, and $1.0$, confirming that dimensional collapse is a property of the model's learned representations rather than sampling stochasticity. Brand Function per-dimension targeting (Run 14, 252 calls): providing specifications that emphasized specific collapsed dimensions did not produce differential recovery --- specification works structurally, reducing aggregate DCI, but does not allow granular per-dimension steering. Full robustness tables are reported in the Web Appendix.

---

## Discussion

### Summary of Findings

The two most fundamental predictions of the LLM-as-observer model are supported. H1 confirms that LLMs exhibit non-uniform dimensional profiles, systematically overweighting Experiential and Economic dimensions relative to Cultural, Temporal, and Narrative dimensions. H2 establishes the convergence result: cross-model cosine similarity of .977 across 24 architectures from nine cultural traditions means that dimensional collapse is not a quirk of RLHF training, e-commerce data, or commercial API safety layers. Collapse is structural, following from the inherent information asymmetry between verifiable brand attributes (price, features, certifications) and perception-dependent brand attributes (heritage, cultural embeddedness, ideological resonance). A brand manager who discovers metamerism in GPT-4o cannot solve the problem by redirecting to Claude or DeepSeek. The solution must be dimensional, not platform-specific.

The non-support for H3 (cross-model heterogeneity) and H4 (differential soft-dimension collapse) refines this picture. All four perception-dependent dimensions collapse together; the models do not preferentially preserve any sub-category. Because collapse is uniform rather than differential, brand managers cannot invest in surviving soft dimensions as a hedge. The only robust strategic response is structural: encoding soft dimensions in verifiable, machine-readable form.

The single exception is theoretically instructive. The Patagonia/Columbia pair falls below the baseline DCI at .194 because Patagonia's ideological dimension is grounded in legally binding commitments (the 1% for the Planet pledge, the 2022 ownership transfer to a non-profit trust) that provide machine-readable ideological signals. This maps onto the defensibility thesis of Hermann et al. (2026): AI agents "cannot recommend brands they cannot defend." The Patagonia exception demonstrates the mechanism that can prevent collapse, not a refutation of it.

The global-versus-local comparison provides the clearest theoretical advance. The large effect ($d = .878$, $p < .001$) supports the claim that AI-mediated collapse is conditional on training-data embeddedness: brands with thin footprints collapse more severely across all dimensions, with an "Economic default" pattern (168% of baseline for local brands versus 114% for global brands) emerging because price is the one dimension that can always be inferred from product category context. This conditional mechanism aligns with Liu's (2026) alignment tax finding and connects to Longoni and Cian's (2022) evidence that consumers resist AI recommendations for experiential products. Local brands face double exposure: their non-Economic dimensions collapse further in AI mediation, and the AI defaults to the Economic frame that consumers distrust for their category. The Run 4 resolution test confirms that collapse is at least partly information-driven: Brand Function specifications move DCI 20% toward baseline, with the Cultural dimension showing the most dramatic recovery.

### Theoretical Implications

The LLM-as-observer concept extends the brand perception literature to a structurally new class of perception agents. Research on observer heterogeneity documents how human cohorts differ in dimensional weights as a function of lived experience, cultural context, and demographic position (cf. Wedel and Kamakura 2000; Grier and Brumbaugh 1999). The AI observer's weights are determined by a different mechanism entirely: training data distribution, optimization objective, and architectural constraint. The result is an observer profile simultaneously less heterogeneous across platforms than human cohorts and more severely biased toward verifiable dimensions than any human cohort.

This paper establishes LLMs as a new class of metameric observer whose spectral bias is structural, convergent (cosine .977), and conditional on training-data embeddedness. This extends the homogenization and alignment-tax literatures (Sourati et al. 2026; Liu 2026; De Freitas et al. 2025) by specifying *which* perceptual dimensions are lost and why: perception-dependent dimensions (Ideological, Cultural, Narrative, Temporal) collapse because they require embodied experience and social context that text-trained models cannot encode, while verifiable dimensions (Economic, Experiential) survive because they are explicitly quantified in training corpora. The conditional metamerism finding adds a moderator structure to this framework: training-data embeddedness outweighs model architecture, training corpus cultural origin, and deployment context as a determinant of collapse severity. This creates an actionable prioritization principle: brands in underrepresented markets face quantifiably larger AI metamerism risk, estimable from measurable proxies (English-language search result count, Wikipedia coverage depth, international media mentions).

The cross-model convergence is also consistent with the shrunken variance phenomenon from Bayesian estimation theory. LLM training on aggregated text corpora functions as an implicit shrinkage estimator, analogous to the James-Stein estimator (James and Stein 1961; Efron and Morris 1975), pulling dimensional weight estimates toward the population mean and compressing the variance that distinguishes brands on perception-dependent dimensions. Brand Function specification counteracts this shrinkage by providing explicit dimensional information (DCI reduced from .353 to .284 in Run 4), though the counteraction operates at the structural level: enriching specific dimensions with additional signal detail produces no incremental per-dimension improvement (Experiential: $p = .742$; Ideological: $p = .508$). The model's dimensional priors respond to the presence of multi-dimensional specification but not to the granularity of per-dimension content.

### Practical Implications

The dimensional collapse documented here converges with independent findings from the agentic commerce literature. Sabbah and Acar (2026) find that among eight e-commerce promotional cues tested across four AI models, only ratings --- the most quantifiable, verifiable signal --- consistently increase selection probability. The promotional cues that fail to transfer --- scarcity (Social/Temporal), assurance (Narrative), bundling (Experiential packaging) --- are precisely those that depend on perception-dependent dimensions. Together, these studies suggest that AI-mediated commerce is *dimensionally structured*, with predictable patterns of sensitivity and collapse.

Four specific implications follow for search advertising strategy. First, SEO becomes spectral optimization: the optimization target shifts from keyword relevance to dimensional representation, making the brand's full spectral profile machine-readable. The SBT specification framework (Zharnikov 2026a) provides a candidate structure for this encoding, though the operative mechanism is structural --- a concise specification across all eight dimensions rather than exhaustive elaboration on any single dimension. The Brand Function works because it encodes output specifications --- what the brand does in each dimension --- not coordination specifications for how the organization manages its brand internally. AI cannot read internal processes; it can read structured output claims. Second, zero-click risk is dimensionally asymmetric: brands differentiated on Economic and Experiential dimensions lose less when AI provides direct answers, while brands differentiated on soft dimensions lose proportionally more. Third, portfolio brands face spectral self-competition: if two portfolio brands are differentiated in human perception on Cultural and Temporal dimensions but metameric in AI perception, the AI recommends them interchangeably, cannibalizing the portfolio's own differentiation (cf. Erdem and Swait 1998; Aaker and Joachimsthaler 2000). Fourth, measurement must become dual-track: human spectral profiles from survey-based assessment and AI spectral profiles from the prompt-based protocol described in this paper.

Investment in building narrative, cultural, and temporal brand dimensions remains valuable to human observers; AI mediation makes it invisible to the AI intermediary. The strategic response is not to abandon perception-dependent dimensions but to make them machine-defensible: encoded in structured, verifiable formats that survive AI mediation. The practical output is a brand-specific AI vulnerability audit: for each of the eight dimensions, what proportion of value is machine-readable versus perception-dependent? The Patagonia exception demonstrates that the distinction is actionable, and the solution is not platform switching --- cosine similarity of .977 across 24 architectures rules this out.

### Supplementary Experiments

Ten supplementary experiments extend and robustify the core findings. Temperature sensitivity testing (540 calls, four temperature conditions from 0.0 to 1.0) confirmed that the DCI is invariant to sampling temperature (Kruskal-Wallis $H = 1.83$, $p = .610$; range .012). Brand Function per-dimension targeting (Run 14, 252 calls) established that specification operates at the structural level: enriching individual dimensions produces no incremental per-dimension benefit. Agentic pipeline compounding (Experiment A, 425 calls) demonstrated that DCI increases monotonically across pipeline stages ($F(2, 273) = 4.298$, $p = .015$, $\eta^2 = .029$), with Patagonia exhibiting the highest compounding rate ($d = .869$). The specification paradox (Experiments D1/D2, 1,440 calls across 8 models) revealed that information framing amplifies collapse ($d = .820$) while constraint framing reduces it by 42% ($d = -.983$) --- "tell the model what to DO, not what to KNOW." Injecting constraint framing at every step of a multi-turn pipeline (Experiment Q1, 1,200 calls) does not shift mean DCI ($d = .197$, $p = .169$) but dramatically compresses DCI variance (Levene $F = 64.77$, $p < .001$; sd reduction from .072 to .027), indicating that specification-as-constraint prevents catastrophic collapse events in agentic contexts rather than correcting the mean. Cross-language validation (Experiment B, 450 calls across 8 languages) confirmed PRISM-B configural invariance (median cosine .992) and identified Experiential as the most measurement-fragile dimension across languages. Serial position testing (Experiment E, 2,400 calls) quantified primacy bias at $d > 1.3$ for constrained-allocation formats and demonstrated that Likert-format elicitation virtually eliminates positional artifacts ($d = .22$), validating PRISM-B's design choice. An 8-model decomposition (Experiment F1, 640 calls) revealed that the aggregate primacy effect is driven almost entirely by a single architecture --- GPT-4o-mini ($d = 1.748$) --- while all other models exhibit negligible primacy ($|d| < .30$) and Gemini shows a recency pattern ($d = -.642$). Cross-domain testing (Experiment F2, 2,400 calls) confirmed that primacy is domain-specific to brand perception ($d = +.193$, $p < .001$) and absent in political attitude measurement ($d = -.020$, $p = .619$), ruling out a universal LLM positional bias. Temporal stability testing (Experiment H13, 450 calls across 4 model pairs) established that dimensional collapse is stable across model versions (all pairwise cosines $> .97$), ruling out the hypothesis that model scaling will naturally resolve collapse. Full protocols, data, and statistical results for all supplementary experiments are available in the Web Appendix.

### Connection to Broader Trends

The dimensional collapse documented here is not unique to brands. Personality perception by AI shows analogous flattening (Hashimoto and Oshio 2025), and cultural nuance in machine translation shows analogous loss (Van Doren and Holland 2025). Representation collapse is also a central challenge in self-supervised learning: Joint-Embedding Predictive Architectures (JEPAs) suffer from an analogous failure mode in which encoders map structurally distinct inputs to near-identical latent representations, requiring explicit regularization to maintain dimensional diversity (Maes et al. 2026). The parallel is structural: both phenomena arise when a system optimizes a prediction objective without a constraint that forces it to preserve the full dimensionality of its input space. The SBT framework provides a general instrument for measuring this collapse across domains: the methodological approach --- measuring the implicit spectral profile of an AI system by analyzing which dimensions it preserves in its outputs --- is domain-general.

The perceptual collapse documented in the present study also represents one of two independent failure modes in AI-mediated commerce. The second is task failure: even the best-performing AI shopping agents achieve only 30% holistic task success on complex product discovery queries (Lyu et al. 2025). These failure modes are structurally orthogonal: an agent can locate the correct product while systematically misrepresenting the brand's narrative, cultural, and temporal dimensions, and an agent with perfect perceptual fidelity can still fail to navigate website filters. AI shopping agents face a dual remediation challenge: structured product data and improved navigation capabilities address task failure, while Brand Function specifications and structured dimensional encoding address perceptual failure. Neither intervention addresses the other's failure mode, and both are required for AI-mediated commerce to function at the level consumers and brands expect.

## Limitations and Future Research

Several limitations bound the present study. First, all observations are LLM-generated with no human validation of dimensional weight profiles; connecting AI spectral profiles to actual purchase decisions requires consumer experiments beyond the present scope. Second, LLM responses are sensitive to prompt engineering; while the protocol standardizes prompts and uses three repetitions per cell, variations in phrasing could alter weight allocations. Third, the structured elicitation design measures what models report as important when explicitly asked, which may differ from implicit weighting in unconstrained responses. Fourth, LLM capabilities evolve rapidly; multimodal models may exhibit different spectral profiles. Fifth, all five local brand pairs are in the food and beverage sector, potentially confounding locality with category effects. Sixth, some national-model APIs exhibited 20--30% invalid-JSON rates, potentially biasing the cross-cultural sample toward more reliable responses.

Future research should pursue four directions: (a) consumer experiments measuring whether AI-mediated brand encounters produce measurably different brand convictions than direct encounters; (b) intervention studies testing alternative specification formats beyond the structural Brand Function tested here --- the remaining frontier appears qualitative (causal attributions, legally-grounded commitments) rather than quantitative, and Experiment Q1 suggests that specification-in-pipeline operates through variance compression rather than mean correction, opening a new design space for adaptive specification strategies; (c) category-specific collapse variation to determine whether the Economic Default is uniform or category-modulated; and (d) estimation of the empirical rate-distortion curve $R(D)$ for AI brand-perception encoders, which has been pursued in a companion study (Zharnikov 2026aa) finding a J-shaped curve across 17 architectures. A fifth direction --- longitudinal tracking of spectral profiles across model versions --- has been addressed in Experiment H13: all four model pairs tested (Qwen family, DeepSeek V3/R1, Llama/Grok, GLM/Qwen cross-family) exhibit profile cosines above .97, indicating that collapse is temporally stable and unlikely to be resolved by model scaling alone.

---

## Conclusion

Brands are multi-dimensional perceptual objects, yet the present findings suggest that AI-mediated search systematically collapses their perception to approximately two dominant dimensions. The resulting metamerism --- brands that look identical through the AI lens despite being structurally different to human observers --- is supported empirically across 22 brand pairs (10 global, 5 local, 7 cross-cultural, and 1 banking pair), 24 model architectures, and nine cultural training traditions. The structural mechanism suggests this is unlikely to be resolved by model scaling alone. It is a geometric consequence of dimensional collapse: the same mechanism that makes physically different light spectra produce identical color percepts when observed through a narrow-band filter.

The conditional structure of this collapse is the paper's most actionable finding. Metamerism is not uniform: in the five FMCG pairs tested, local brands from underrepresented markets collapse 24.7% more severely than global brands (Cohen's $d = .878$). The Economic default mechanism --- AI substituting price for every dimension it lacks data on --- means that the brands most reliant on non-economic differentiation (cultural embeddedness, heritage, ideological positioning) face the largest exposure precisely in the markets where those dimensions matter most. And the Patagonia exception demonstrates that the collapse is not inevitable: brands that encode their soft dimensions as verifiable, machine-readable commitments can survive AI mediation.

For advertising research, this paper demonstrates that the study of AI-mediated brand perception requires a dimensional framework, not merely a functional one. Knowing that "AI affects brands" is insufficient; what matters is knowing which dimensions are affected, by how much, and for which brands. Spectral Brand Theory provides that dimensional framework, and this paper provides the measurement protocol.

For practitioners, the findings suggest a strategic diagnostic: the dimensions most associated with premium brand differentiation --- narrative, ideology, culture, heritage --- are precisely those most susceptible to AI-mediated collapse. If this collapse pattern persists across future model generations, competitive advantage in AI-mediated search may accrue disproportionately to brands whose multi-dimensional value is specified, structured, and machine-defensible rather than solely to those with the strongest human-perceived differentiation. This hypothesis warrants longitudinal investigation. A key implication is that brand health measurement should expand to include AI-mediated spectral profiles alongside traditional human-respondent surveys, making the question "how does the AI that mediates consumer search perceive us?" as operationally tractable as the question "how do consumers perceive us?" This paper provides a measurement protocol toward that goal.

### Companion Computation Script

All numerical values reported in this paper --- DCI point estimates, bootstrap standard errors, cross-model cosines, MANOVA and t-test statistics, per-pair effect sizes, and the Run 4 / Run 11 / Run 14 robustness statistics --- are reproducible from the public PRISM-B pipeline at `https://github.com/spectralbranding/sbt-papers/tree/main/r15-ai-search-metamerism/experiment`. The pipeline includes the run scripts (`ai_search_metamerism.py`, `run11_roshen_multicity.py`, `run12_brand_function.py`, `run12b_brand_function_extended.py`, `run_resolution_test.py`), a fixed-seed analysis layer (`L4_analysis/`), a validator (`validation/validate.py`) that verifies the 21,350 core call count, and a `requirements.txt` that pins Python 3.12 + scipy + numpy. The full per-call dataset (JSONL) and per-model cost ledger are mirrored at the HuggingFace dataset (DOI: 10.57967/hf/8284). To reproduce the headline statistics: clone the repository, install requirements, set the model API keys named in `L1_configuration/`, and execute `L4_analysis/run_all.py` against the published session logs.

---

## Acknowledgments

AI assistants (Claude Opus 4.6, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

---

## References

Aaker, David A. (1991). *Managing Brand Equity: Capitalizing on the Value of a Brand Name*. Free Press.

Aaker, David A., and Erich Joachimsthaler (2000). *Brand Leadership*. Free Press.

Aaker, Jennifer L. (1997). Dimensions of brand personality. *Journal of Marketing Research*, 34(3), 347-356.

Acar, Oguz A., and David A. Schweidel (2026). Preparing your brand for agentic AI. *Harvard Business Review*, March-April 2026.

Brakus, J. Joško, Bernd H. Schmitt, and Lia Zarantonello (2009). Brand experience: What is it? How is it measured? Does it affect loyalty? *Journal of Marketing*, 73(3), 52-68. https://doi.org/10.1509/jmkg.73.3.052

Castelo, Noah, Bram Van den Bergh, and Donald R. Lehmann (2019). Task-dependent algorithm aversion. *Journal of Marketing Research*, 56(5), 809-825. https://doi.org/10.1177/0022243719851788

Cover, Thomas M., and Joy A. Thomas (2006). *Elements of Information Theory* (2nd ed.). Wiley-Interscience.

Dawar, Niraj, and Neil Bendle (2018). Marketing in the age of Alexa. *Harvard Business Review*, 96(3), 80-86.

De Freitas, Julian, Gideon Nave, and Stefano Puntoni (2025). Ideation with generative AI---in consumer research and beyond. *Journal of Consumer Research*, 52(1), 18-31.

Diehl, Kristin, Laura J. Kornish, and John G. Lynch (2003). Smart agents: When lower search costs for quality information increase price sensitivity. *Journal of Consumer Research*, 30(1), 56-71.

Doshi, Anil R., and Oliver P. Hauser (2024). Generative AI enhances individual creativity but reduces the collective diversity of novel content. *Science Advances*, 10(28), eadn5290.

Efron, Bradley, and Carl Morris (1975). Data analysis using Stein's estimator and its generalizations. *Journal of the American Statistical Association*, 70(350), 311-319.

Erdem, Tülin, and Joffre Swait (1998). Brand equity as a signaling phenomenon. *Journal of Consumer Psychology*, 7(2), 131-157.

Gersho, Allen, and Robert M. Gray (1991). *Vector Quantization and Signal Compression*. The Kluwer International Series in Engineering and Computer Science, Vol. 159. Kluwer Academic Publishers. https://doi.org/10.1007/978-1-4615-3626-0

Grier, Sonya A., and Anne M. Brumbaugh (1999). Noticing cultural differences: Ad meanings created by target and non-target markets. *Journal of Advertising*, 28(1), 79-93.

Hagendorff, Thilo, Sarah Fabi, and Michal Kosinski (2023). Human-like intuitive behavior and reasoning biases emerged in large language models but disappeared in ChatGPT. *Nature Computational Science*, 3, 833-838.

Hashimoto, Yuji, and Atsushi Oshio (2025). Exploring personality structure through LLM agent: A lexical study. *Psychological Test Adaptation and Development*, 6, 248-258. https://doi.org/10.1027/2698-1866/a000114

Hermann, Erik, and Stefano Puntoni (2024). Artificial intelligence and consumer behavior: From predictive to generative AI. *Journal of Business Research*, 180, 114720. https://doi.org/10.1016/j.jbusres.2024.114720

Hermann, Erik, Stefano Puntoni, and David A. Schweidel (2026). Trusting AI Agents: Uncertainty Reduction by Design. Working Paper, SSRN. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6103206

Huang, Ming-Hui, and Roland T. Rust (2021). A strategic framework for artificial intelligence in marketing. *Journal of the Academy of Marketing Science*, 49(1), 30-50. https://doi.org/10.1007/s11747-020-00749-9

James, William, and Charles Stein (1961). Estimation with quadratic loss. *Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability*, 1, 361-379.

Johnson, William B., and Joram Lindenstrauss (1984). Extensions of Lipschitz mappings into a Hilbert space. In *Contemporary Mathematics* (Vol. 26, pp. 189-206). American Mathematical Society. https://doi.org/10.1090/conm/026/737400

Kapferer, Jean-Noël (2008). *The New Strategic Brand Management: Creating and Sustaining Brand Equity Long Term* (4th ed.). Kogan Page.

Kapferer, Jean-Noël (2012). *The New Strategic Brand Management: Advanced Insights and Strategic Thinking* (5th ed.). Kogan Page.

Keller, Kevin Lane (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1-22.

Li, Yi, Sandra Castelo, Zsolt Katona, and Miklos Sarvary (2024). Determining the validity of large language models for automated perceptual analysis. *Marketing Science*, 43(2), 254-266.

Liu, Mingfu (2026). The alignment tax: Response homogenization in aligned LLMs and its implications for uncertainty estimation. arXiv:2603.24124. https://arxiv.org/abs/2603.24124

Longoni, Chiara, and Luca Cian (2022). Artificial intelligence in utilitarian vs. hedonic contexts: The "word-of-machine" effect. *Journal of Marketing*, 86(1), 91-108.

Lyu, Yougang, Xiaoyu Zhang, Lingyong Yan, Maarten de Rijke, Zhaochun Ren, and Xiuying Chen (2025). DeepShop: A benchmark for deep research shopping agents. Working Paper, arXiv:2506.02839.

Lynch, John G., and Dan Ariely (2000). Wine online: Search costs affect competition on price, quality, and distribution. *Marketing Science*, 19(1), 83-103.

Maes, Léon, Quentin Le Lidec, Damien Scieur, Yann LeCun, and Randall Balestriero (2026). LeWorldModel: Stable end-to-end joint-embedding predictive architecture from pixels. arXiv:2603.19312. https://doi.org/10.48550/arXiv.2603.19312

Puntoni, Stefano, Rebecca Walker Reczek, Markus Giesler, and Simona Botti (2021). Consumers and artificial intelligence: An experiential perspective. *Journal of Marketing*, 85(1), 131-151.

Sabbah, Jamil, and Oguz A. Acar (2026). Marketing to machines: How AI models respond to promotional cues. Working Paper, SSRN. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6406639

Shannon, Claude E. (1959). Coding theorems for a discrete source with a fidelity criterion. *IRE National Convention Record*, 7(Part 4), 142-163.

Sourati, Zhivar, Saumya Venkatesh, Anil Doshi, John R. Hauser, and Joshua B. Tenenbaum (2026). LLM homogenization and epistemic collapse in AI-mediated knowledge production. *Trends in Cognitive Sciences*, forthcoming.

Tversky, Amos (1972). Elimination by aspects: A theory of choice. *Psychological Review*, 79(4), 281-299.

Van Doren, Mira, and Cameron Holland (2025). "Be My Cheese?": Assessing cultural nuance in multilingual LLM translations. arXiv:2509.21577. https://arxiv.org/abs/2509.21577

Wedel, Michel, and Wagner A. Kamakura (2000). *Market Segmentation: Conceptual and Methodological Foundations* (2nd ed.). Kluwer Academic Publishers.

Wedel, Michel, and P. K. Kannan (2016). Marketing analytics for data-rich environments. *Journal of Marketing*, 80(6), 97-121. https://doi.org/10.1509/jm.15.0413

Wyszecki, Günther, and Walter S. Stiles (1982). *Color Science: Concepts and Methods, Quantitative Data and Formulae* (2nd ed.). Wiley.

Zharnikov, Dmitry (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, Dmitry (2026aa). Empirical rate-distortion curve for AI brand perception encoders. Working Paper. https://doi.org/10.5281/zenodo.19528833

Zharnikov, Dmitry (2026x). AI-native brand identity: From visual recognition to cryptographic verification. Working Paper. https://doi.org/10.5281/zenodo.19391476

---

## Appendix A: Spectral Brand Theory -- Framework Specification

### A.1 Overview

Spectral Brand Theory (Zharnikov 2026a) models brand perception as the interaction between a brand's emission profile and an observer's spectral weights. The framework has two core components: (1) a typed eight-dimensional decomposition of brand signals, and (2) a formalization of observer heterogeneity through spectral weight vectors.

### A.2 The Eight Dimensions

The eight dimensions represent structurally distinct categories of brand signal. They are not factors derived empirically from consumer surveys; they are typed emission channels that a brand can activate to varying degrees, and that different observer types weight differently.

| # | Dimension | What it captures |
|---|-----------|-----------------|
| 1 | **Semiotic** | Visual identity, logos, symbols, design language, naming |
| 2 | **Narrative** | Brand story, founding myth, archetype, voice, editorial identity |
| 3 | **Ideological** | Stated values, purpose, political-ethical commitments, worldview |
| 4 | **Experiential** | Sensory, functional, and hedonic properties of the product or service encounter |
| 5 | **Social** | Community, belonging, identity signaling, peer endorsement |
| 6 | **Economic** | Price positioning, value exchange, scarcity, accessibility |
| 7 | **Cultural** | Geographic, subcultural, or heritage embeddedness; cultural codes |
| 8 | **Temporal** | Heritage depth, longevity, stability, historical continuity |

This taxonomy builds on established frameworks in brand research. Aaker's (1991) foundational equity model identifies brand awareness and brand associations as the core assets through which brands create value in consumer memory; SBT's eight-dimensional framework refines the associations construct, decomposing it into typed emission channels rather than treating it as a unitary cognitive category. Kapferer's (2008) Brand Identity Prism organizes brand identity across six facets -- physique, personality, culture, relationship, reflection, and self-image; SBT's Cultural and Temporal dimensions subsume and extend Kapferer's culture facet. Aaker's (1997) five brand personality dimensions (sincerity, excitement, competence, sophistication, ruggedness) capture anthropomorphic brand attribution; SBT's dimensions capture what brands emit as perceptual inputs, not how consumers project personality onto them. Brakus, Schmitt, and Zarantonello's (2009) brand experience scale (sensory, affective, intellectual, behavioral) is subsumed within SBT's Experiential dimension as one of eight emission channels.

### A.3 Brand Emission Profile

A brand's emission profile at time $t$ is a vector encoding signal intensity across all eight dimensions:

$$\mathbf{e}(t) = [e_1(t), e_2(t), e_3(t), e_4(t), e_5(t), e_6(t), e_7(t), e_8(t)]$$

where each $e_i(t) \in [0, 10]$ represents the intensity of the brand's signal on dimension $i$ at time $t$. Canonical profiles for the brands used in this study (Hermès, Patagonia, Erewhon) are established in Zharnikov (2026a) and held fixed across all analyses.

### A.4 Observer Spectral Profile and Cohorts

SBT's central contribution is the formalization that emission is not perception. Each observer type applies a characteristic weight vector $\mathbf{w} = [w_1, \ldots, w_8]$ constrained to the simplex $\sum_{i=1}^{8} w_i = 1$, $w_i \geq 0$, determining the relative salience of each dimension in forming brand conviction. Brand conviction -- the observer's formed assessment of a brand -- is a function of the interaction between the brand's emission profile and the observer's spectral weights.

Observers with similar weight vectors cluster into cohorts (cf. Wedel and Kamakura 2000). Two observers encountering identical brand signals form structurally different brand convictions if their spectral profiles weight different dimensions. This observer-dependent architecture produces spectral metamerism: two structurally different brands can produce the same brand conviction in an observer whose spectral profile assigns near-zero weight to the dimensions on which those brands differ.

The present study operationalizes this framework by treating each LLM as an observer cohort with an estimable spectral weight vector, and measuring the degree to which LLM weight vectors are concentrated on Economic and Experiential dimensions relative to the theoretical uniform baseline.

---
*This paper is part of the Spectral Brand Theory research program. For the full atlas of 20+ interconnected papers, see [spectralbranding.com/atlas](https://spectralbranding.com/atlas).*
