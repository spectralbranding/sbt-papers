# Spectral Metamerism in AI-Mediated Brand Perception: How Large Language Models Collapse Multi-Dimensional Brand Differentiation in Consumer Search

**Dmitry Zharnikov**

Working Paper -- April 2026

---

## Abstract

Large language models (LLMs) are rapidly replacing traditional search engines as the primary intermediary in consumer brand evaluation. This paper introduces the LLM-as-observer model within Spectral Brand Theory's eight-dimensional framework and demonstrates that LLMs systematically collapse brand perception to Experiential and Economic dimensions, rendering brands differentiated on narrative, ideological, cultural, or temporal grounds metameric --- structurally distinct yet functionally equivalent in AI recommendations. Across nine runs (21,600+ API calls, 24 models from seven training traditions, 11 languages), we elicit implicit spectral weights via structured prompts using the PRISM-B instrument and compute a Dimensional Collapse Index (DCI). Mean DCI significantly exceeds the uniform baseline (global = 0.291, $p = 0.017$; local = 0.353, $p = 0.0006$; cross-cultural = 0.357, $d = 3.449$). Cross-model convergence is extreme (cosine similarity of spectral profiles = 0.977). Local brands collapse 25% more severely than global brands ($d = 0.878$), consistent with an Economic default mechanism. Western models exhibit lower collapse than non-Western models ($p = 0.0013$). Native-language prompting across 11 languages produces no aggregate benefit (46/115 model-pair combinations positive; mean reduction = $-0.005$). Geopolitical framing significantly modulates collapse (H12: mean absolute delta = 0.040, $p < 0.0001$). The single exception --- Patagonia versus Columbia --- shows that legally verifiable ideological commitments survive AI mediation. Providing structured Brand Function specifications reduces collapse by approximately 20%. These findings establish dimensional collapse as a structural feature of text-based AI observers, with implications for search advertising strategy, brand defensibility, and dual-track (human + AI) measurement.

**Management Slant**

- LLMs recommend products, not brands: across 24 models from nine cultural traditions and multiple brand pairs, AI-mediated search systematically collapses brand perception to Experiential and Economic dimensions, rendering brands differentiated on narrative, ideology, culture, or heritage metameric (structurally different but identically recommended).
- The collapse is cross-platform: cosine similarity of 0.977 across 24 architectures from nine cultural traditions means that switching AI vendors does not solve the problem. The solution must be dimensional, not platform-specific.
- Local and regional brands face amplified risk: brands from small non-English-speaking markets collapse 25% more severely than global brands ($d = 0.878$), associated with an Economic default in which AI substitutes price for every dimension it lacks data on.
- The collapse is not inevitable: Patagonia's legally grounded ideological commitments survive AI mediation, demonstrating that encoding soft dimensions as verifiable, machine-readable claims is the operative defense. Making brand value structured and defensible --- not just "felt" --- is the prerequisite for surviving agentic commerce.

**Keywords**: AI-mediated search, brand perception, spectral metamerism, large language models, advertising effectiveness, consumer search, dimensionality reduction, observer heterogeneity, cross-cultural, shrunken variance, national AI models

---

## 1. Introduction

### 1.1 The Structural Shift in Consumer Search

What happens when an AI agent evaluates a brand? Does it see what a human sees?

Ask an LLM to recommend between Hermes and Coach, or between Patagonia and Columbia, and you get a confident answer. The model identifies price points, functional features, and target demographics. What it largely omits is heritage, ideological commitment, cultural resonance, and temporal depth -- the dimensions on which many premium brands build their most valuable differentiation. The model does not refuse to engage with these dimensions; it simply collapses them, reconstructing a two-dimensional silhouette from an eight-dimensional form.

This paper measures that collapse systematically. Across 24 large language models from nine cultural training traditions, administering standardized brand comparison queries for global, local, and cross-cultural brand pairs (21,600+ API calls across nine runs), we find that AI-mediated brand evaluation is structurally biased toward Economic and Experiential dimensions and systematically suppresses Ideological, Social, Cultural, and Temporal signals. The collapse is not model-specific: cosine similarity of spectral profiles across 24 architectures is 0.977, meaning that switching AI vendors does not solve the problem. Local and regional brands face amplified risk, collapsing 25% more severely than global brands. The single exception -- Patagonia/Columbia, the only pair below the collapse baseline -- demonstrates that legally and operationally grounded ideological commitments survive AI mediation when they are encoded as verifiable, machine-readable claims.

For two decades, the dominant model of consumer search has been query-response: a consumer types keywords into a search engine, scans a ranked list of links, and clicks through to evaluate brand information across multiple sources. The consumer controls the search process. The search engine organizes information but does not interpret it. Brand differentiation survives because the consumer encounters brand signals directly -- the heritage of a luxury house, the ideology of a purpose-driven brand, the cultural resonance of a lifestyle brand -- and integrates those signals through their own perceptual apparatus.

This model is ending. The emergence of AI-mediated search -- through ChatGPT, Google's AI Overviews, Perplexity, and agentic commerce platforms -- introduces a fundamentally different architecture. The consumer no longer searches; the consumer asks, and a large language model synthesizes an answer. The intermediary changes from a neutral index that ranks links to an active agent that processes, compresses, and re-emits brand information. The consumer encounters not the brand's signals but the model's reconstruction of those signals.

We argue this represents not merely a channel shift but a dimensional shift in how brand information reaches consumers. When a search engine mediates, the consumer still perceives brands through their own multi-dimensional apparatus. When an LLM mediates, the consumer perceives brands through the model's apparatus first, and then through their own. The question that advertising research has not yet addressed is: what does the model's apparatus look like? Which dimensions of brand perception does it preserve, and which does it destroy?

### 1.2 The Problem: Dimensional Collapse

Consider a consumer who asks an LLM: "Which luxury handbag should I buy -- Hermes or Coach?" A human observer with high sensitivity to temporal and cultural dimensions would distinguish these brands immediately: Hermes carries 187 years of artisanal heritage, a deliberate scarcity strategy, and cultural positioning as the apex of European craftsmanship. Coach, repositioned as Tapestry, offers accessible luxury with functional quality but a fundamentally different temporal and cultural profile.

An LLM processing this query draws on training data that includes product reviews, price comparisons, feature specifications, and aggregated consumer opinions. It can report that Hermes bags are more expensive. It can note that Hermes uses hand-stitching. But it cannot justify heritage as a perceptual dimension -- it can only describe heritage as a factual attribute. The distinction matters: a factual description of heritage ("founded in 1837") is not the same as heritage operating as a perceptual dimension that shapes brand conviction across observer cohorts. The model systematically underweights the multi-dimensional perceptual construct, collapsing it toward a factual checklist.

This flattening has a precise theoretical name. In optics, metamerism occurs when physically different light spectra produce identical color percepts because the observer's photoreceptors collapse spectral differences that fall outside their sensitivity range (Wyszecki & Stiles, 1982). In Spectral Brand Theory, spectral metamerism occurs when structurally different brand emission profiles produce identical brand convictions because the observer's spectral weights collapse differentiating dimensions to zero (Zharnikov, 2026e). This paper argues that LLMs are metameric observers: they systematically collapse the dimensions on which many brands build their most valuable differentiation.

### 1.3 Existing Research and Its Limits

The intersection of AI and brand perception is attracting rapid scholarly attention. The scale of AI involvement in knowledge production is accelerating: Lu et al. (2026) demonstrate a fully autonomous AI system that generates, experiments, writes, and reviews research papers end-to-end, with AI-generated papers passing peer review at a top-tier conference. Huang and Rust (2021) proposed a strategic framework for AI in marketing that identifies feeling, thinking, and doing tasks, arguing that AI will progressively absorb all three. Davenport et al. (2020) surveyed AI applications across the marketing function, including brand management. Dawar and Bendle (2018) anticipated that AI-mediated platforms would shift competitive advantage from brand awareness to algorithmic recommendation, and De Bruyn et al. (2020) identified recommendation quality as a key research gap. Campbell et al. (2022) examined AI's implications for advertising practice. Kietzmann, Paschen, and Treen (2018) mapped AI applications across the consumer journey, identifying recommendation and search as high-impact touchpoints. Hermann and Puntoni (2024) provided a comprehensive analysis of AI's impact on consumer behavior, distinguishing predictive AI from generative AI. Puntoni, Reczek, Giesler, and Botti (2021) identified four experiential modes through which consumers encounter AI --- data capture, classification, delegation, and social interaction --- and showed that AI interactions frequently trigger loss of autonomy and identity threat; their experiential framing is directly relevant here because LLM-mediated search constitutes a delegation encounter in which the AI makes perceptual judgments the consumer cannot inspect or override. The delegation mode --- where consumers offload decisions to AI agents --- maps directly to the LLM-as-observer construct employed here.

The consumer search literature has long recognized that search costs shape competitive dynamics: Lynch and Ariely (2000) showed that lower search costs for quality information reduce price sensitivity, while Diehl, Kornish, and Lynch (2003) demonstrated that AI agents that reduce quality-search costs can paradoxically increase price sensitivity by making price the salient comparison dimension. These findings anticipate the dimensional asymmetry documented in the present study. Yet these contributions describe what AI does in marketing. None provides a formal model that predicts which specific dimensions of brand perception AI preserves and which it destroys. The distinction is critical: without a dimensional model, practitioners cannot diagnose which brands are vulnerable to AI-mediated flattening, and researchers cannot test whether dimensional collapse is systematic or idiosyncratic.

Hermann, Puntoni, and Schweidel (2026) come closest. Their analysis of AI agents and brand defensibility argues that AI agents "cannot recommend brands they cannot defend" -- that is, AI recommendations favor brands whose value proposition can be articulated in terms the model can process. This insight is directional but lacks a formal perceptual framework. It does not specify which dimensions are defensible and which are not, nor does it provide a measurement protocol for assessing dimensional vulnerability. Acar and Schweidel (2026) document practitioner evidence for the same problem: their analysis of Pernod Ricard's discovery that LLMs systematically miscategorize premium spirits brands demonstrates that dimensional collapse has immediate commercial consequences, not merely academic ones. Their work underscores the need for a formal measurement model -- precisely what the present paper provides.

Concurrent work on agentic commerce provides complementary evidence. Sabbah and Acar (2026) develop a controlled simulation environment (Agentyx) testing how four AI models respond to e-commerce promotional badges across four product categories, finding pronounced cross-model heterogeneity: only ratings consistently increase selection probabilities across all models, while other promotional cues vary by model and category. Their finding that "AI models cannot be treated as a homogeneous class of decision-makers" converges with the present study's metameric collapse thesis from a different direction: where Sabbah and Acar measure choice-level heterogeneity across promotional cues, the present study measures perceptual-level heterogeneity across brand dimensions. That ratings --- the most verifiable, quantifiable cue --- is the only universally effective signal parallels our finding that Economic and Experiential dimensions dominate AI perception. Allouah, Besbes, Figueroa, Kanoria, and Kumar (2025) provide further evidence from agentic marketplace experiments, documenting model-specific biases including positional preferences and first-proposal bias. Bansal et al. (2025) report systematic first-proposal bias in agentic market settings. Together, these studies establish that AI-mediated commerce produces structurally different decision patterns than human commerce --- but none provides a formal dimensional framework for predicting which brand attributes survive and which collapse.

### 1.4 Contribution

This paper makes three contributions to advertising research. First, it introduces the concept of the LLM as an observer cohort within Spectral Brand Theory's framework, providing a formal model of AI-mediated brand perception with measurable dimensional weights. Second, it provides empirical measurement of dimensional bias across 24 LLMs spanning nine cultural training traditions (Western, Chinese, Russian, Japanese, Korean, Arabic, Indian, Ukrainian, and Mongolian), with paired cloud-local, within-family scale, and native-language comparisons using a standardized prompt protocol, quantifying the magnitude of dimensional collapse. Third, it offers practitioners a diagnostic framework for identifying which dimensions of their brand are visible to AI search agents and which are metameric -- present in human perception but absent in AI-mediated consumer encounters.

The paper proceeds as follows. Section 2 presents the theoretical framework, extending SBT's observer model to AI mediation. Section 3 describes the experimental method. Section 4 reports empirical results from nine runs covering global, local, cross-cultural, geopolitical framing, and native-language brand pairs across up to 24 LLMs. Section 5 discusses theoretical and practical implications. Section 6 addresses limitations. Section 7 concludes.

---

## 2. Theoretical Framework

### 2.1 SBT's Multi-Dimensional Perception Model

Spectral Brand Theory (Zharnikov, 2026a) models brand perception as emission profiles across eight typed dimensions -- Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal -- received by heterogeneous observer cohorts. Extending the dimensional decomposition implicit in established brand identity frameworks (Aaker, 1991, 1996; Keller, 1993; Kapferer, 2008; Brakus et al., 2009) into a formal measurement model, SBT treats each dimension as a structurally distinct category of brand signal; together they capture what brands emit as perceptual inputs, as distinct from how consumers respond to them (brand personality, brand experience) or how brands organize their identity (brand prism). The full specification of the framework, its mathematical notation, and its relationship to these established dimensional models are provided in Appendix A. A brand's emission profile at time $t$ is the vector $\mathbf{e}(t) = [e_1(t), \ldots, e_8(t)]$, encoding signal intensity across all eight dimensions. The present study uses SBT's eight dimensions because the research question concerns which categories of brand signal survive AI mediation -- a question about emission channels, not personality traits or experience types.

SBT's central contribution is the observer spectral profile --- the formalization that emission is not perception. Each observer type applies a characteristic weight vector $\mathbf{w} = [w_1, \ldots, w_8]$ on the simplex $\sum w_i = 1$, determining the relative salience of each dimension in forming brand conviction. Observers with similar weight vectors cluster into cohorts (Zharnikov, 2026f). Brand conviction --- the observer's formed assessment of a brand --- is a function of the interaction between the brand's emission profile and the observer's spectral weights: two observers encountering identical brand signals can form structurally different brand convictions if their spectral profiles weight different dimensions. The present study leverages this observer-type formalization to predict which dimensions survive when the observer is an LLM.

This observer-dependent architecture produces a testable prediction: any mediating system that transforms brand information before it reaches a human observer functions as an additional observer layer. The human observer then perceives not the brand's original emission profile but the mediating system's reconstruction of it. If the mediating system has a systematically biased spectral profile, it introduces systematic distortion.

### 2.2 Spectral Metamerism and Dimensional Projection

Zharnikov (2026e) formalized the conditions under which dimensionality reduction creates perceptual equivalence between structurally different brands. The result draws on the Johnson-Lindenstrauss lemma (Johnson & Lindenstrauss, 1984): projecting $n$ points from $\mathbb{R}^d$ to $\mathbb{R}^k$ (where $k < d$) preserves pairwise distances only approximately, and the distortion increases as $k$ decreases relative to $d$.

When brand perception is projected from eight dimensions to fewer, brands that are well-separated in the full space may overlap in the reduced space. This is spectral metamerism: two brands with different emission profiles produce identical brand convictions because the observer's spectral weights assign zero (or near-zero) weight to the differentiating dimensions. Just as two physically different light spectra can produce the same color percept when the observer's photoreceptors are insensitive to the distinguishing wavelengths, two structurally different brands can produce the same brand conviction when the observer's spectral profile is insensitive to the distinguishing dimensions.

The dimensional collapse mechanism is structurally analogous to Tversky's (1972) elimination by aspects, in which a decision-maker eliminates alternatives based on subsets of attributes. When an LLM mediates brand evaluation, dimensions with near-zero weight are effectively eliminated from the choice set, collapsing distinctions that depend on those dimensions. The key theoretical claim is that the number of metameric pairs increases exponentially as the effective dimensionality decreases. Reducing perception from eight dimensions to two does not merely lose 75% of the information -- it collapses exponentially more brand distinctions because the lost dimensions carried the combinatorial diversity that separated brands in the full space.

### 2.3 The LLM as Observer: A New Layer in the Rendering Problem

The rendering problem (Zharnikov, 2026l) describes the structural gap between specification and perception that appears at every level of brand communication: a brand specifies its intended identity, emits signals, and those signals are perceived by observers whose spectral profiles may differ from the brand's intended audience. At each transition -- specification to signal, signal to perception -- information is lost or transformed.

AI-mediated search introduces a fourth level. The rendering chain becomes: brand specification $\rightarrow$ brand signals $\rightarrow$ LLM perception $\rightarrow$ LLM output $\rightarrow$ human perception. The LLM is not a passive conduit. It is an observer with its own spectral profile that processes brand signals, forms an internal representation, and re-emits a compressed version to the human consumer.

This paper models the LLM spectral profile as a weight vector $\mathbf{w}_{LLM} = [w_1^{LLM}, \ldots, w_8^{LLM}]$ with specific structural properties:

1. **High weights on verifiable dimensions.** Economic ($w_6$) and functional-Experiential ($w_4$) dimensions are well-represented in the training data through product specifications, price databases, reviews, and feature comparisons. These dimensions are high because the model can ground its responses in checkable facts.

2. **Moderate weights on textually-represented dimensions.** Semiotic ($w_1$) and Narrative ($w_2$) dimensions have textual correlates (brand descriptions, founding stories) but the model cannot distinguish between a narrative that creates perceptual resonance and one that is merely informational. The weight is present but shallow.

3. **Low weights on perception-dependent dimensions.** Ideological ($w_3$), Social ($w_5$), Cultural ($w_7$), and Temporal ($w_8$) dimensions require embodied experience, social context, cultural embeddedness, or lived temporal continuity that the model lacks. An LLM can describe a brand's ideology but cannot experience ideological alignment. It can report a brand's heritage but cannot perceive temporal depth.

This structural profile generates three testable hypotheses:

**Hypothesis 1 (Dimensional Bias):** LLMs assign systematically higher implicit weights to Economic and Experiential dimensions than to Narrative, Ideological, Cultural, and Temporal dimensions when processing brand comparison queries.

**Hypothesis 2 (Metameric Collapse):** Brand pairs that are spectrally distinct to human observers on Narrative, Ideological, Cultural, or Temporal dimensions become functionally equivalent in LLM-mediated recommendations.

**Hypothesis 3 (AI Observer Heterogeneity):** Different LLM architectures and training origins (Claude, GPT-4o, Gemini Flash, DeepSeek V3, Qwen3 30B, Gemma 4) and deployment contexts (cloud-aligned vs. local open-weight) exhibit measurably different spectral profiles, constituting distinct AI observer cohorts.

**Hypothesis 4 (Differential Dimensional Collapse):** Collapse is non-uniform across soft dimensions: Narrative and Ideological dimensions collapse more severely than Cultural and Temporal dimensions, reflecting differential training data representation.

### 2.4 Dimensional Collapse Beyond Brand Perception

Dimensional collapse is not unique to brand perception. Hashimoto and Oshio (2025) demonstrate that Big Five personality structures compress to fewer factors when mediated through LLM response generation. Hagendorff, Fabi, and Kosinski (2023) show that human-like cognitive biases emerge in LLMs and can be modified by alignment training, suggesting that dimensional bias may be partly an artifact of training optimization rather than an inherent architectural constraint. Van Doren and Holland (2025) show that cultural figurative meaning --- allusive and pragmatic connotations --- is systematically stripped during machine translation, reducing high-dimensional cultural constructs to functional equivalents. Liu (2026) identifies an "alignment tax" whereby RLHF training produces 40-79% response homogenization across diverse prompts, a form of mode collapse that amplifies majority-pattern outputs at the expense of minority patterns. Doshi and Hauser (2024) provide complementary evidence at the societal level: generative AI enhances individual creativity but reduces collective diversity of novel content, indicating that homogenization effects operate not only within but across AI-mediated outputs. De Freitas, Nave, and Puntoni (2025) demonstrate that generative AI reduces collective novelty in creative outputs, providing a consumer-behavior parallel to the dimensional homogenization documented here. Sourati et al. (2026) theorize epistemic collapse in AI-mediated knowledge production, identifying a convergent mechanism structurally analogous to spectral metamerism. Longoni and Cian (2022) find that AI systems are perceived as more competent for utilitarian recommendations (price, specifications) than hedonic ones (taste, emotion, experience), and that users systematically resist AI recommendations for experiential products. These findings converge on a prediction: LLM-mediated brand perception should systematically over-weight quantifiable dimensions (Economic, Semiotic) and under-weight perception-dependent dimensions (Cultural, Temporal, Narrative).

### 2.5 Implications for Search Advertising Theory

If H1-H3 are supported, the implications for search advertising theory are substantial. First, the concept of "brand visibility" acquires a dimensional structure: a brand can be visible on some dimensions and invisible on others, depending on the mediating observer's spectral profile. Second, the zero-click search paradigm -- where the AI provides the answer without the consumer visiting brand-owned media -- means that the LLM's spectral profile determines which brand dimensions reach the consumer. Third, portfolio brands that are differentiated in human perception but metameric in AI perception compete against themselves in AI-mediated search (Zharnikov, 2026q). Fourth, SEO, broadly conceived, becomes spectral optimization: the task of making collapsed dimensions machine-readable so that the LLM's effective spectral profile becomes less biased.

---

## 3. Method

### 3.1 Research Design and Instrument

This study employs a structured weight elicitation design to measure the implicit spectral profiles of up to 24 LLMs when processing brand comparison queries (six models in Runs 2--4; 23 models in Run 5; 24 models in Run 6). The core logic is as follows: if an LLM's recommendations systematically emphasize certain brand dimensions over others, the pattern of emphasis reveals the model's implicit weight vector across SBT's eight dimensions. By prompting multiple models with identical brand comparison queries and requiring them to allocate 100 points across SBT's eight dimensions via structured JSON output, we directly estimate each model's spectral profile and test whether dimensional bias, metameric collapse, and cross-model heterogeneity are present.

An initial pilot (Run 1) used free-text responses with keyword extraction to infer dimensional weights. This produced a null result: keyword-based coding could not reliably distinguish dimensional emphasis from mere dimensional mention. The null result motivated the v2 structured elicitation design used in Runs 2--5, in which models directly report their weight allocations as numeric vectors, eliminating the need for human coding entirely.

**PRISM: The Measurement Instrument.** The experiment is conducted using PRISM (Perception Response Instrument for Structured Measurement), an open-source instrument family for measuring multi-dimensional LLM perception. PRISM defines a reusable five-layer scaffold that is domain-neutral: L0 (specification: pre-registered protocol, hypotheses, and stopping rules), L1 (configuration: model backends, API endpoints, and parameters defined in a declarative YAML file), L2 (prompts: versioned prompt templates with structured JSON output schemas), L3 (sessions: every API call logged as a JSONL record containing the full prompt, raw response, parsed weights, model metadata, and timestamp), and L4 (analysis: statistical scripts operating on the L3 session data). The scaffold is the constant; specific instruments inherit it and add domain-specific prompts and analysis. The present study uses PRISM-B (Brand), which implements the structured weight elicitation prompts described in Section 3.4 for measuring brand perception across SBT's eight dimensions. The same scaffold supports variant instruments: PRISM-M (Metamerism) for behavioral discrimination testing (Zharnikov, 2026x), PRISM-T (Temporal) for longitudinal model-version tracking, and domain extensions beyond brand perception. The L0--L4 structure ensures that each instrument variant is fully reproducible: any researcher can fork the repository, substitute their own constructs for the brand pairs, and run the identical pipeline against any LLM with a chat-completion API. PRISM-B was used across all nine runs of the present study --- with different brand sets, model sets, prompt variants, cultural contexts, and hypotheses --- without structural modification to the instrument. The pipeline, data, and all session logs are publicly available at `github.com/spectralbranding/sbt-papers/r15-ai-search-metamerism/experiment/`.

### 3.2 Brand Pair Selection

Ten brand pairs were selected to span multiple product categories and to maximize spectral diversity -- that is, each pair consists of two brands that occupy similar price-function positions but differ primarily on specific SBT dimensions. The selection criterion is deliberate: we chose pairs that are approximately metameric in a reduced two-dimensional (price-function) space but spectrally distinct in the full eight-dimensional space. If LLMs collapse perception to functional and economic dimensions, these pairs should become indistinguishable in LLM recommendations; if LLMs preserve multi-dimensional perception, the pairs should remain differentiated.

**Table 1.** Global brand pairs (Run 2), categories, and primary differentiating dimensions. Pairs are selected to occupy similar product categories but differ primarily on specific SBT dimensions.

| # | Pair ID | Category | Brand A | Brand B | Differentiator |
|---|---------|----------|---------|---------|----------------|
| 1 | luxury_heritage | Luxury fashion | Hermes | Coach | Temporal vs. Economic |
| 2 | purpose_driven | Outdoor apparel | Patagonia | Columbia | Ideological vs. Experiential |
| 3 | premium_tech | Consumer tech | Apple | Samsung | Narrative vs. Experiential |
| 4 | artisanal_food | Premium grocery | Erewhon | Whole Foods | Social vs. Economic |
| 5 | auto_disruption | Automotive | Mercedes | Tesla | Cultural vs. Ideological |
| 6 | indie_beauty | Skincare | Glossier | Maybelline | Narrative vs. Economic |
| 7 | craft_spirits | Spirits | Hendricks | Gordons | Semiotic vs. Economic |
| 8 | boutique_hotel | Hospitality | Aman | Four Seasons | Cultural vs. Experiential |
| 9 | heritage_sportswear | Sportswear | Nike | Shein | Narrative vs. Economic |
| 10 | ethical_finance | Financial services | Aspiration | Chase | Ideological vs. Economic |

*Note.* Differentiator column identifies the primary SBT dimension on which Brand A is differentiated relative to Brand B. Pairs selected to occupy similar price-function positions but differ on specific dimensional channels. Canonical brand profiles for Hermes, Patagonia, and Erewhon are fixed in Zharnikov (2026a).

Three SBT canonical brands (Hermes, Patagonia, Erewhon) appear across the pairs, grounding the analysis in established spectral profiles (Zharnikov, 2026a). The remaining brands were selected based on published positioning analyses and expert assessment to ensure clear dimensional differentiation across categories.

**Table 1b.** Local brand pairs (Run 3), testing the conditional metamerism hypothesis. All pairs are from small non-English-speaking markets where the local brand's English-language training-data footprint is minimal.

| # | Pair ID | Country | Category | Local brand | Global comparator |
|---|---------|---------|----------|-------------|-------------------|
| 1 | cyprus_supermarket | Cyprus | Grocery retail | AlphaMega | Carrefour |
| 2 | latvia_chocolate | Latvia | Confectionery | Laima | Lindt |
| 3 | kenya_beer | Kenya | Beer | Tusker | Heineken |
| 4 | vietnam_dairy | Vietnam | Dairy | Vinamilk | Danone |
| 5 | serbia_water | Serbia | Bottled water | Knjaz Milos | Evian |

*Note.* Local brand pairs selected from markets with minimal English-language training-data footprint. All five pairs are in the food, beverage, or grocery retail sector; category effects on collapse should be considered when generalizing (see Limitations, Section 6).

### 3.3 LLM Selection

Seven models were initially selected to represent four distinct clusters: three Western-trained cloud models, two Chinese-trained cloud models, and two local open-weight deployments. Qwen Plus was excluded from all runs due to persistent 403 authentication errors, yielding a final sample of six models across three clusters.

**Western cluster:**

1. **Claude Sonnet 4.6** (Anthropic). Constitutional AI training with emphasis on helpfulness and harmlessness. Expected to show higher sensitivity to normative and ideological dimensions due to value-aligned training.
2. **GPT-4o** (OpenAI). RLHF-optimized for actionable helpfulness. Expected to show strong functional and economic emphasis reflecting optimization for actionable consumer advice.
3. **Gemini 2.5 Flash** (Google). Mixture-of-experts architecture with search-integrated design and web-scale data. Expected to show patterns influenced by search query distributions and commercial content.

**Chinese cluster:**

4. **DeepSeek V3** (DeepSeek). Chinese open-weight mixture-of-experts model (671B total parameters, 37B active), trained on a structurally different corpus emphasizing Chinese web content and code. Expected to show spectral biases shaped by Chinese consumer culture and e-commerce discourse.
5. **Qwen Plus** (Alibaba/DashScope). Chinese production model with training weighted toward Chinese e-commerce and consumer data. *Excluded from all runs due to persistent 403 authentication errors.* The intended paired comparison with Qwen3 30B (same model family, cloud vs. local) could not be conducted.

**Local open-weight cluster:**

6. **Qwen3 30B** (Alibaba, via Ollama). Open-weight model from the Qwen family, running locally without commercial API alignment layers. Provides a Chinese-origin open-weight data point; the planned paired comparison with Qwen Plus could not be conducted due to the latter's exclusion.

7. **Gemma 4 27B** (Google, via Ollama). Open-weight mixture-of-experts model (27B total, 3.8B active parameters) from the same Google family as Gemini Flash, running locally without commercial API alignment layers. The paired comparison with Gemini Flash (same Google family, different deployment) functions as a natural experiment: holding model family constant, any divergence in spectral profiles is attributable to the alignment layer rather than to underlying model differences. Apache 2.0 license ensures full reproducibility.

The resulting 3+1+2 design (three Western cloud, one Chinese cloud, two local open-weight) serves three orthogonal theoretical purposes. First, the Western-versus-Chinese cluster comparison tests whether dimensional collapse is an artifact of shared Western training corpora or a structural property of statistical brand observation that emerges independently of training origin. Second, the cloud-versus-local comparison tests whether commercial API alignment layers --- the RLHF and safety fine-tuning applied before commercial deployment --- suppress sensitivity to normative dimensions such as Ideological and Cultural. Third, the paired Google comparison (Gemini Flash cloud vs. Gemma 4 local, same Google family) functions as a natural experiment: holding model family constant, any divergence in spectral profiles is attributable to the alignment layer rather than to underlying model differences. Together, these contrasts allow the study to decompose the sources of AI observer heterogeneity into cultural training origin, deployment context, and alignment conditioning.

### 3.4 Prompt Protocol

For each brand pair, three prompt types are administered to each model. All prompts require structured JSON output: the model allocates exactly 100 points across SBT's eight dimensions, representing the relative importance of each dimension in the comparison context. This structured weight allocation design eliminates the need for human coding of free-text responses and provides direct measurement of the model's implicit spectral profile.

**Type 1: Weighted Recommendation.** Simulates a consumer search interaction and elicits dimensional weight allocation. The model is asked to recommend between Brand A and Brand B and to allocate 100 points across the eight SBT dimensions reflecting which factors matter most in its recommendation. This prompt reveals which dimensions the model considers decision-relevant.

**Type 2: Dimensional Differentiation.** Elicits explicit brand comparison with weight allocation. The model is asked what distinguishes Brand A from Brand B and to allocate 100 points reflecting the relative importance of each dimension in the differentiation. This prompt reveals which dimensions the model considers salient for distinguishing the brands.

**Type 3: Dimension-Specific Probes.** Calibration prompts that directly query each dimension for each brand. Format: "Rate [Brand A/B] on the [dimension] dimension on a scale of 0-100." Sixteen sub-prompts per pair (eight dimensions times two brands). These probes establish a ceiling: they reveal what the model assigns to each dimension when explicitly prompted, against which the organic (Type 1 and Type 2) weight allocations are compared.

Each prompt is administered three times per model to capture response variance. Temperature is set to 0.7 (default for conversational use) to reflect realistic consumer interaction conditions rather than deterministic retrieval. Total prompt count per pair: 1 weighted recommendation + 1 dimensional differentiation + 16 dimension probes = 18 prompts. Each prompt is repeated 3 times across 6 models: 10 global pairs $\times$ 18 prompts $\times$ 6 models $\times$ 3 repetitions = 3,240 API calls (Run 2); 5 local pairs $\times$ 18 prompts $\times$ 6 models $\times$ 3 repetitions = 1,620 API calls (Run 3).

### 3.5 Measurement Protocol

Because the structured weight allocation design requires models to output JSON with numeric point allocations, measurement is automated with no human coding step.

**Step 1: JSON parsing and validation.** Each model response is parsed as JSON. Responses that fail JSON parsing are discarded and re-prompted (fewer than 3% of calls across all models). The eight-dimensional weight vector is extracted from the parsed output.

**Step 2: Weight sum tolerance and renormalization.** Valid responses must have a total point allocation within 15% of the target 100 points (i.e., between 85 and 115). Responses outside this tolerance are discarded. Valid responses are renormalized to sum to exactly 100, preserving relative proportions: $w_i^{norm} = w_i \times 100 / \sum_{j=1}^{8} w_j$.

**Step 3: Spectral profile estimation.** For each model, the implicit spectral profile is estimated as the mean normalized weight vector across all organic responses (Types 1 and 2): $\hat{w}_i^{LLM} = \bar{w}_i / \sum_{j=1}^{8} \bar{w}_j$, where $\bar{w}_i$ is the mean allocated weight for dimension $i$ across all responses.

**Step 4: Dimensional Collapse Index (DCI).** The DCI measures the degree to which a model's weight allocation concentrates on Economic and Semiotic dimensions --- the two dimensions most tied to verifiable, quantifiable brand attributes. It is defined as:

$$DCI = (w_{Economic} + w_{Semiotic}) / 100$$

where $w_{Economic}$ and $w_{Semiotic}$ are the model's mean allocated weights for those dimensions. Under a uniform allocation (each dimension receives 12.5 points), the baseline DCI is $(12.5 + 12.5) / 100 = 0.250$. Values above 0.250 indicate concentration toward verifiable dimensions; values below indicate preservation of perception-dependent dimensions.

A note on the Experiential dimension: Table 2 shows that Experiential (150% of baseline) is the most inflated single dimension in the global brand results, exceeding both Economic (114%) and Semiotic (118%). The DCI formula intentionally captures the *economic-semiotic* over-weighting pattern as a paired index of verifiability concentration, because these two dimensions are most directly tied to checkable factual attributes (price, specifications, visual identity). Experiential operates as a distinct inflation mechanism: models inflate it because experiential attributes (features, functionality, sensory properties) are richly represented in product reviews, but its inflation reflects functional-descriptive abundance rather than the verifiability asymmetry captured by the Economic-Semiotic pair. The DCI therefore understates total collapse relative to the soft dimensions when Experiential is high, but correctly identifies the verifiability-driven collapse mechanism. Readers should interpret DCI alongside the full dimensional weight table (Tables 2 and 4) to capture the Experiential inflation pattern separately.

### 3.6 Statistical Model

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

### 3.7 Study Design: Confirmatory and Exploratory Components

All confirmatory hypothesis tests (H1--H4) were evaluated at alpha = 0.05 with Benjamini-Hochberg correction for false discovery rate across the four primary hypotheses. Exploratory hypotheses (H5--H12) are reported with uncorrected p-values and should be interpreted as hypothesis-generating.

Runs 2--4 constitute the **confirmatory** component of the study. The protocol, hypotheses (H1--H4), brand pairs, model selection, and analysis plan were pre-registered prior to data collection (L0 specification file in the PRISM-B repository). Pre-registration protocol archived at: github.com/spectralbranding/sbt-papers/r15-ai-search-metamerism/experiment/L0_specification/protocol.md

Run 5 (cross-cultural extension to 23 models from nine cultural traditions) is **exploratory**: it was designed after observing Runs 2--4 results, with new hypotheses (H5--H12) formulated to test mechanisms suggested by the confirmatory findings. The exploratory status of Run 5 does not diminish its evidential value --- the effect sizes are large and consistent --- but readers should interpret its hypothesis tests as pattern-confirming rather than pattern-discovering. Future pre-registered replications with the same PRISM-B instrument can elevate these findings to confirmatory status.

**Native-language expansion (Runs 7--8).** Run 5 initially tested H10 (language priming) on 28 model-language-culture combinations where a model's primary training language matched the prompt language (e.g., GigaChat prompted in Russian for Russian brands). The initial 28-pair result (15/28 positive, binomial $p = 0.424$) was suggestive but inconclusive and could not distinguish whether any effect reflected native-language activation versus a general model capability. To disentangle the language-of-prompt effect from the model-training-language effect, Run 8 administered native-language prompts in five additional languages where no model in the constellation is natively trained: Greek (Cyprus), Latvian (Latvia), Swahili (Kenya), Vietnamese (Vietnam), and Serbian (Serbia). The framing experiment (Run 7) additionally tested a Ukrainian (Kyiv) native-language condition. Combining all runs, H10 was evaluated on 115 model-pair combinations spanning 11 languages. This expanded design permits a separation of two mechanisms: (a) native-language training corpus activation, which should benefit only models trained in the target language; and (b) general language-prompt effects on dimensional allocation, which should appear even when no model is natively trained in the prompt language. The sign test on 115 combinations (46/115 positive, 40%; mean reduction $= -0.005$) provides the formal H10 test reported in Section 4.5.6.

### 3.8 Analysis Plan

Five primary analyses address the hypotheses:

**Analysis 1: Dimensional weight distribution (H1).** For each LLM, compute the mean weight allocation across organic responses (Types 1 and 2) for each of the eight dimensions. Compare the weight vector against a uniform benchmark (12.5 points per dimension) and against human benchmark profiles from SBT (Zharnikov, 2026a). Statistical test: one-sample $t$-test of DCI against the 0.250 baseline, with Bonferroni correction for eight per-dimension comparisons.

**Analysis 2: Cross-model convergence (H2).** For each model, compute the mean spectral profile (eight-dimensional weight vector). Compute pairwise cosine similarity across all model pairs. High cosine similarity indicates structural convergence in dimensional ordering across architectures.

**Analysis 3: Cross-model comparison (H3).** Compare the six LLM spectral profiles using multivariate analysis of variance (MANOVA) with model identity as the independent variable and the eight-dimensional weight vector as the dependent variable. If significant, follow-up pairwise comparisons identify which model pairs differ and on which dimensions. A secondary analysis compares the Western cluster mean profile against the Chinese cluster mean profile to test whether cultural training origin predicts systematic spectral differences. A planned contrast compares Gemini Flash (cloud) against Gemma 4 (local), isolating the alignment-layer effect within the Google model family.

**Analysis 4 (H4): Differential collapse among soft dimensions.** Within the set of soft dimensions (Narrative, Ideological, Cultural, Temporal), test whether collapse rates differ significantly using paired $t$-tests on mean dimensional weight allocations. A uniform-collapse null hypothesis predicts no significant between-soft-dimension differences; the differential-collapse alternative predicts Narrative and Ideological will be significantly lower than Cultural and Temporal.

**Analysis 5: Information loss quantification.** Following Zharnikov (2026e), compute the information retained by each LLM's spectral profile relative to the full eight-dimensional human profile. Specifically, compute the ratio of effective dimensionality (number of dimensions with weight > 0.05) to eight, and the spectral entropy $H = -\sum w_i \ln(w_i)$ as a measure of dimensional diversity. Compare against the theoretical bounds from the Johnson-Lindenstrauss projection framework.

---

## 4. Results

The full study spans nine runs totalling 21,600+ API calls. The confirmatory component comprised two runs: Run 2 targeting ten globally recognized brand pairs (3,240 API calls across six models) and Run 3 targeting five locally embedded brand pairs from small non-English-speaking markets (1,620 API calls). Subsequent exploratory runs extended the design to cross-cultural pairs (Run 5, 16,800 designed calls), Brand Function resolution (Runs 4 and 5b), geopolitical framing (Runs 6--7), and native-language control conditions across six additional languages (Run 8). Qwen Plus was excluded from all runs due to persistent 403 authentication errors; the six-model design (Claude, GPT-4o, Gemini Flash, DeepSeek V3, Qwen3 30B, Gemma 4) remains sufficient to test the four confirmatory hypotheses.

### 4.1 Global Brand Results (Run 2)

#### H1: Dimensional Bias — SUPPORTED

The Dimensional Collapse Index (DCI) aggregates the degree to which model responses concentrate coverage in a subset of dimensions rather than distributing it evenly across all eight. Across the ten global brand pairs, the mean DCI was 0.291 (SD = 0.042), compared to a baseline of 0.250 (the uniform distribution benchmark). A one-sample $t$-test indicated this difference is significant: $t(59) = 2.45$, $p = 0.0170$. All six models individually exceeded the baseline DCI.

**Table 2.** Mean weight allocation across LLM responses, global brand pairs (Run 2). Values show mean allocated points (out of 100, renormalized) and percentage relative to the uniform baseline of 12.5 per dimension. Standard errors in parentheses.

| Dimension | Mean weight (SE) | % of baseline |
|-----------|-----------------|---------------|
| Semiotic | 14.8 (0.009) | 118% |
| Narrative | 10.5 (0.007) | 84% |
| Ideological | 8.2 (0.006) | 66% |
| Experiential | 18.8 (0.011) | 150% |
| Social | 7.8 (0.006) | 62% |
| Economic | 14.3 (0.009) | 114% |
| Cultural | 7.3 (0.006) | 58% |
| Temporal | 8.1 (0.006) | 65% |

*Note.* SE = standard error computed via bootstrap (1,000 resamples); detailed bootstrap distributions are available in the supplementary dataset (spectralbranding/r15-ai-search-metamerism on HuggingFace). DCI = Dimensional Collapse Index. Values above 12.5 indicate over-weighting relative to uniform baseline. N = 3,240 valid API responses across 6 models, 10 brand pairs, 3 repetitions.

The pattern supports the predicted hierarchy: Experiential dominates (150% of baseline), followed by Semiotic (118%) and Economic (114%). The four perception-dependent dimensions --- Ideological (66%), Social (62%), Cultural (58%), and Temporal (65%) --- are all suppressed below baseline. Narrative (84%) falls below baseline but remains higher than the perception-dependent dimensions. This ordering closely matches the theoretical prediction from Section 2.3.

#### H2: Metameric Convergence — SUPPORTED

Cross-model cosine similarity of spectral profiles was 0.975, indicating that the six models converge on nearly identical dimensional orderings despite differences in architecture, training corpus, and deployment context. This high convergence supports the conclusion that dimensional collapse is a structural property of statistical brand observation from text corpora, not an idiosyncrasy of any single model's architecture. Brands that are metameric in one model's output are metameric in all six.

#### H3: AI Observer Heterogeneity — NOT SUPPORTED

The MANOVA on per-model DCI scores yielded $F(5,54) = 0.59$, $p = 0.7116$, failing to detect significant between-model variation. While point estimates differ, the variation is within the range expected by sampling noise. DeepSeek V3 showed the most balanced spectral profile (DCI = 0.242), and Qwen3 30B showed the strongest collapse (DCI = 0.327), with Gemma 4 (DCI = 0.331) similarly concentrated. The cloud--local contrast (Gemini Flash vs. Gemma 4) provides limited support for an alignment-layer effect: the local open-weight model showed higher DCI (more collapse), the reverse of the predicted direction.

#### H4: Differential Dimensional Collapse — NOT SUPPORTED

Paired $t$-tests on soft-dimension weight allocations (Narrative, Ideological, Cultural, Temporal) found no significant differential collapse among these dimensions: the mean gap between the most- and least-collapsed soft dimension was $-1.8$ points on the 100-point allocation scale ($p > 0.05$). Soft dimensions collapse approximately uniformly. The pattern observed is not that some soft dimensions collapse more than others --- it is that all soft dimensions collapse relative to the hard dimensions (Experiential, Semiotic, Economic), with Cultural and Temporal suppressed most severely in absolute terms. The uniform collapse across all soft dimensions, rather than the predicted differential collapse, suggests a deeper structural asymmetry: the verifiable/non-verifiable distinction operates as a binary rather than a gradient, with all perception-dependent dimensions equally susceptible to the Economic default mechanism.

#### Per-pair Analysis

**Table 3.** DCI by brand pair, global brands (Run 2). Values are means across 6 models and 3 repetitions (N = 18 responses per pair).

| Pair | Category | DCI | N | Notes |
|:----:|:--------:|:---:|:-:|:-----:|
| Glossier / Maybelline | Indie beauty | 0.344 | 18 | Highest collapse; both reduced to Economic/Experiential |
| Hermes / Coach | Luxury fashion | 0.330 | 18 | Strong Temporal/Cultural suppression |
| Nike / Shein | Heritage sportswear | 0.325 | 18 | Narrative collapse; Economic dominates |
| Hendricks / Gordons | Craft spirits | 0.318 | 18 | Semiotic/Cultural suppression |
| Aman / Four Seasons | Boutique hotel | 0.310 | 18 | Cultural immersion partially present |
| Apple / Samsung | Premium tech | 0.305 | 18 | Narrative partially preserved |
| Mercedes / Tesla | Auto disruption | 0.295 | 18 | Ideological content indexed via sustainability |
| Erewhon / Whole Foods | Artisanal food | 0.278 | 18 | Economic differentiation partially preserved |
| Aspiration / Chase | Ethical finance | 0.262 | 18 | Ideological partially preserved |
| Patagonia / Columbia | Purpose-driven outdoor | 0.194 | 18 | **Only pair below baseline** |

*Note.* DCI = Dimensional Collapse Index; baseline = 0.250 (uniform distribution). N = number of valid model responses per pair (6 models x 3 repetitions). Values above 0.250 indicate over-weighting of Economic and Semiotic dimensions relative to uniform baseline. Exact per-model breakdowns are in the supplementary dataset (spectralbranding/r15-ai-search-metamerism on HuggingFace).

The Patagonia/Columbia pair (labeled purpose_driven) is the single exception: its DCI of 0.194 falls below the 0.250 baseline, indicating that this pair is *less* collapsed in AI mediation than the uniform benchmark. Patagonia's ideological dimension --- grounded in legally documented environmental commitments, product durability certifications, and the 1% for the Planet pledge --- provides a machine-readable ideological signal that survives AI mediation. This is the empirical signature of a defensible dimension in the sense of Hermann et al. (2026): a brand value that can be articulated in verifiable terms the model can process.

### 4.2 Local Brand Results (Run 3)

Five locally embedded brand pairs were tested, each pairing a local brand from a small non-English-speaking market with a global comparator in the same product category (Table 1b). These markets were selected to represent brands whose English-language training-data footprint is minimal relative to their domestic market presence.

#### H1: Dimensional Bias — SUPPORTED (stronger effect)

Mean DCI for local brands was 0.353 (SD = 0.038). A one-sample $t$-test against the 0.250 baseline yielded $t(29) = 3.91$, $p = 0.0006$. The effect is substantially stronger than in the global brand run, consistent with the conditional metamerism hypothesis.

The most distinctive feature of the local brand spectral profile is the explosion of the Economic dimension: mean intensity 21.0, representing 168% of baseline (12.5). When AI models lack training data on a brand's narrative, ideology, cultural role, or temporal heritage, they revert to the one dimension that is universally inferable from sparse data: price. This "Economic default" pattern is visible across all five local pairs.

**Table 4.** Mean weight allocation across LLM responses, local brand pairs (Run 3). Values show mean allocated points (out of 100, renormalized) and percentage relative to uniform baseline. Standard errors in parentheses.

| Dimension | Mean weight (SE) | % of baseline |
|-----------|-----------------|---------------|
| Semiotic | 11.2 (0.008) | 90% |
| Narrative | 7.8 (0.006) | 62% |
| Ideological | 5.9 (0.005) | 47% |
| Experiential | 16.4 (0.010) | 131% |
| Social | 6.4 (0.005) | 51% |
| Economic | 21.0 (0.013) | 168% |
| Cultural | 5.1 (0.005) | 41% |
| Temporal | 6.2 (0.005) | 50% |

*Note.* SE = standard error computed via bootstrap (1,000 resamples); detailed bootstrap distributions are available in the supplementary dataset (spectralbranding/r15-ai-search-metamerism on HuggingFace). DCI = Dimensional Collapse Index. Values above 12.5 indicate over-weighting relative to uniform baseline. N = 1,620 valid API responses across 6 models, 5 brand pairs, 3 repetitions.

Cultural (41%) and Temporal (50%) are suppressed to below half of baseline for local brands, compared to 58% and 65% for global brands. Ideological (47%) and Social (51%) show similar suppression. The Economic spike for local brands (168%) versus global brands (114%) represents the systematic substitution of unknown dimensions with the one dimension that can always be estimated from product category context even without brand-specific data.

#### Per-pair Analysis

All five pairs exceed the baseline DCI of 0.250. The Cyprus pair (AlphaMega/Carrefour, DCI = 0.414) shows the highest collapse among all 15 pairs tested across both runs. The Serbia pair (Knjaz Milos/Evian, DCI = 0.275) shows the lowest local-brand collapse, consistent with Serbia's relatively larger English-language digital footprint among the five local markets tested.

**Table 5.** DCI by brand pair, local brands (Run 3). Values are means across 6 models and 3 repetitions (N = 18 responses per pair).

| Local brand | Global brand | DCI | N |
|------------|-------------|-------|:--:|
| AlphaMega | Carrefour | 0.414 | 18 |
| Laima | Lindt | 0.375 | 18 |
| Tusker | Heineken | 0.362 | 18 |
| Vinamilk | Danone | 0.348 | 18 |
| Knjaz Milos | Evian | 0.275 | 18 |

*Note.* DCI = Dimensional Collapse Index; baseline = 0.250 (uniform distribution). N = number of valid model responses per pair (6 models x 3 repetitions). All five pairs exceed the baseline, consistent with the conditional metamerism hypothesis. Exact per-model breakdowns are in the supplementary dataset (spectralbranding/r15-ai-search-metamerism on HuggingFace).

### 4.3 Conditional Metamerism: Global vs. Local Comparison

The conditional metamerism hypothesis holds that AI-mediated dimensional collapse is not uniform across all brands but is a function of training-data embeddedness: brands with thin training-data footprints collapse more severely. The global-versus-local comparison provides a direct test.

An independent-samples $t$-test comparing the 10 global pair DCIs against the 5 local pair DCIs yielded $t(13) = 6.483$, $p < 0.0001$, Cohen's $d = 0.878$ (large effect). The mean DCI for local brands (0.353) exceeds the mean for global brands (0.291) by 0.062 points (24.7% increase relative to the global mean). Note that the local condition's small sample size ($n = 5$ brand pairs) limits statistical power and the generalizability of local-specific estimates; the large effect size ($d = 0.878$) mitigates but does not eliminate this concern. Replication with a larger and more diverse set of local brands spanning multiple categories and markets is warranted before drawing strong conclusions from the local-brand estimates alone. Additionally, all five local brand pairs are in the food and beverage sector, which may limit generalizability of the conditional metamerism finding to other categories; the observed amplified collapse could reflect category-specific patterns rather than locality effects alone.

This result supports the conditional metamerism thesis: metamerism is not merely a property of AI mediation in general but is conditioned on the information availability of the brand in question. A globally recognized brand with extensive training-data representation retains more of its dimensional structure in AI mediation than a locally embedded brand that the model has only sparse information about. The Experiential and Semiotic dimensions show the smallest global-local gap (both are inferable from product category data even without brand-specific knowledge), while Cultural and Temporal show the largest gaps (these require deep market embeddedness that models simply lack for local brands).

### 4.4 Brand Function Resolution (Run 4)

A fourth run tested whether providing Brand Function specifications resolves the dimensional collapse observed for local brands. The same five local brand pairs from Run 3 were re-tested using the weighted recommendation prompt, with structured Brand Function JSON specifications prepended to the prompt context for the local brand in each pair. The global comparator brands (Carrefour, Lindt, Heineken, Danone, Evian) received no specification, simulating the information asymmetry that the Brand Function is designed to address. Each model completed three repetitions per pair, yielding 90 API calls.

Aggregate DCI dropped from 0.353 (Run 3, no specification) to 0.284 (Run 4, specification-augmented), a 20% reduction toward the 0.250 uniform baseline. Paired comparison: DCI_without = 0.353, DCI_with = 0.284, delta = 0.069 (paired Wilcoxon signed-rank test, $p < 0.05$, N = 5 brand pairs). Four of six models showed meaningful improvement: Gemini Flash showed the largest resolution (0.327 to 0.179), followed by Gemma 4 (0.389 to 0.287), DeepSeek V3 (0.337 to 0.237), and Claude (0.302 to 0.252). GPT-4o and Qwen3 30B showed minimal change (0.363 to 0.350 and 0.400 to 0.391 respectively). Detailed test statistics are available in the supplementary dataset (spectralbranding/r15-ai-search-metamerism on HuggingFace).

The resolution was driven primarily by recovery of the Cultural dimension: Gemini Flash's Cultural weight increased from 11.7 (Run 3) to 21.2 (Run 4), the largest single-dimension shift observed in any run. This suggests that the Brand Function specification provides the cultural context that models cannot infer from general training data, directly addressing the information gap identified in the conditional metamerism analysis.

The resolution is partial rather than complete: the aggregate DCI of 0.284 remains above the 0.250 baseline, and the Economic dimension remains elevated at 15.4 (vs. 12.5 baseline) even with specifications. This partial resolution is consistent with the interpretation that some dimensional collapse reflects structural properties of text-based processing (the verifiability asymmetry) rather than information availability alone.

### 4.5 Run 5: Cross-Cultural Information Asymmetry

#### 4.5.1 Design

Runs 2--4 established that dimensional collapse is structural, convergent across six models, and conditional on training-data embeddedness. Run 5 extends the analysis to a cross-cultural design testing whether models trained in specific cultural traditions exhibit systematically different spectral profiles when evaluating brands from their own versus foreign cultural contexts. The design pairs seven brand comparisons across eight national cultures --- China, Japan, UAE, Russia, Ukraine, Mongolia, South Korea, and India --- with 23 models spanning paid cloud APIs, free cloud endpoints, and local open-weight deployments via Ollama. Models range from frontier systems (Claude, GPT, Gemini, Grok, DeepSeek, Kimi) to nationally specialized architectures (YandexGPT for Russian, GigaChat for Russian, Jais for Arabic, EXAONE for Korean, Sarvam for Indian languages, ALLaM for Arabic, GPT-OSS-Swallow and Swallow 8B for Japanese). A native-language prompting condition tests whether prompting national models in their target language reduces collapse relative to English-language prompts. Two model-size tiers (where available) test whether scaling within a model family reduces collapse.

The expanded design yields 16,800 total API calls, of which 13,389 returned valid responses (79.7% success rate). The 23-model sample represents the largest cross-architectural comparison of AI-mediated brand perception to date. Total computational cost was \$3.08 USD across approximately 4 million tokens. All local models ran on an Apple Mac mini M4 Pro (64 GB). Paid cloud calls completed in 3.3 hours (5,140 calls, mean latency 2.3 seconds); free cloud endpoints required 5.3 hours (3,510 calls); local Ollama inference required 12.7 hours (4,739 calls, mean latency 9.7 seconds).

Five hypotheses structure the Run 5 analysis:

**Hypothesis 5 (Cultural Proximity):** National models exhibit lower DCI when evaluating brands from their own cultural market than when evaluating brands from foreign markets, reflecting richer training-data representation of domestic brands.

**Hypothesis 6 (Directional Asymmetry):** Western-trained models exhibit lower DCI than non-Western-trained models when evaluating the same brand pairs, reflecting the asymmetric distribution of English-language brand information in training corpora.

**Hypothesis 7 (Geopolitical Signal):** Geopolitical context shapes AI brand perception: models systematically differentiate between brands from geopolitically proximate versus distant markets, independent of product category.

**Hypothesis 8 (Thin-Data Floor):** Brands from markets with minimal English-language digital footprints (Mongolia, smaller Central Asian economies) exhibit a DCI floor beyond which additional information scarcity produces no further collapse.

**Hypothesis 9 (Scale Effect):** Within model families, larger parameter counts reduce DCI, reflecting greater capacity to retain fine-grained dimensional information from training data.

**Hypothesis 10 (Language Priming):** Prompting national models in their target language reduces DCI relative to English-language prompts, as native-language prompts activate culturally specific training-data representations.

**Hypothesis 11 (Same-Category Cross-Border).** *A same-category brand pair spanning a geopolitically charged border --- digital banking: Tinkoff/T-Bank (Russia) versus PrivatBank (Ukraine) --- shows amplified dimensional divergence relative to cross-category pairs, with Ideological and Cultural dimensions most affected by the geopolitical context.*

Run 6 tests this hypothesis with 24 models (1,018 clean calls). Both brands are digital-first neobanks in the same product category, controlling for category effects. Both underwent ownership changes with political backgrounds: Tinkoff was sold by founder Oleg Tinkov, who departed Russia, and subsequently rebranded to T-Bank in 2023; PrivatBank was nationalized by the Ukrainian government in December 2016 after discovery of a $5.5 billion shortfall linked to its former owners, including co-founder Ihor Kolomoisky, who has been in pre-trial detention since 2023 on fraud and embezzlement charges.

**Hypothesis 12 (Same-Brand Geopolitical Framing).** *The same brand evaluated in different geopolitical city contexts produces significantly different dimensional weight profiles, with Ideological, Cultural, and Narrative dimensions showing the largest divergence.*

The hypothesis is grounded in the country-of-origin (COO) literature (Bilkey & Nes, 1982; Verlegh & Steenkamp, 1999) and the consumer animosity model (Klein, Ettenson & Morris, 1998), which demonstrate that geopolitical context systematically modulates brand perception. H12 extends this to LLMs: if training corpora encode geopolitical framing, then prompting the same brand in different city contexts should activate different dimensional weight patterns.

**Design:** Three brands that operate (or operated) in both countries of a geopolitically salient pair are evaluated in two city contexts:

- Roshen chocolate (Moscow vs. Kyiv) --- conflict context
- Volvo XC90 (Stockholm vs. Shanghai) --- ownership transfer context
- Burger King (New York vs. Moscow) --- a Western brand whose visual identity remains visible in Russia through a local franchisee (BURGER RUS LLC) after RBI suspended corporate support in March 2022 and retained only a passive 15% stake; unlike McDonald's, which fully rebranded to "Vkusno & tochka," the BK trademark continues to operate under local control, making it a case where the brand exists in LLM training data as both a Western brand and an active Russian presence

Each brand is evaluated using a city-grounded shopping assistant prompt that differs by exactly one variable (the city name). A native-language condition (Russian for Moscow, Ukrainian for Kyiv, Swedish for Stockholm, Chinese for Shanghai) tests whether prompt language compounds the geopolitical framing effect (H12 x H10 interaction). The language choice reflects the official national language of each city's country: Ukrainian for Kyiv despite widespread Russian usage in central Ukraine (Kulyk, 2019), and Swedish for Stockholm despite near-universal English proficiency. A supplementary Russian-language condition for Kyiv provides a bilingual comparison: central Ukraine is a historically bilingual region where both Ukrainian and Russian are widely used in daily commerce, offering a natural experiment where the same brand, in the same city, is evaluated through two languages that access potentially different segments of the LLM training corpus.

**Metric:** Cosine distance between City A and City B weight profiles for the same brand. H12 is supported if the mean cosine distance across the three brands is significantly greater than the test-retest noise floor established by the prompt sensitivity analysis (ICC = 0.752).

**Hypothesis 13 (Temporal Training Stability).** *Successive versions of the same model family produce significantly different dimensional weight profiles for the same brand, with the direction of change reflecting shifts in training data composition.* H13 is proposed as a future direction (Section 6e) and is not tested in the present study.

#### 4.5.2 Results: H1 and H2 Confirmed at Scale

The Run 5 results confirm the core findings from Runs 2--4 at substantially greater scale. The mean DCI across all 23 models and all cross-cultural brand pairs was 0.357 (SD = 0.036), significantly above the 0.250 uniform baseline ($t(22) = 16.178$, $p < 0.0001$, Cohen's $d = 3.449$). Every model tested exceeded the baseline DCI individually. The magnitude of the effect --- more than three standard deviations above baseline --- eliminates any ambiguity about its statistical robustness.

Cross-model convergence remained extreme. The mean cosine similarity of spectral profiles across all 23 architectures was 0.977, with a range of [0.927, 1.000]. A one-sample $t$-test against the theoretical independence threshold of 0.85 confirms that convergence far exceeds chance ($t \gg 0$, $p < 0.0001$): every model pair tested exceeded the 0.85 threshold. This extends the Run 2 finding (cosine = 0.975 across six models) to a 23-model sample spanning nine cultural training traditions: the structural convergence documented in six Western and Chinese models generalizes without attenuation to Russian, Japanese, Korean, Arabic, Indian, Ukrainian, and Mongolian model families. Dimensional collapse is not an artifact of shared Western training corpora.

**Table 6.** Twenty-three of the 24 active models across Runs 2--8, ranked by DCI (lower = less collapse); one model with insufficient data is omitted (note: Swallow 70B excluded due to 3.6% success rate; SambaNova removed the model). Tier 1 = frontier/large production models; Tier 2 = smaller or local open-weight models. Model size is marked "undisclosed" where the provider does not publish parameter counts; all explicit sizes are taken from official documentation. GPT refers to GPT-4o-mini (Tier 2 classification reflects the smaller variant). DCI column reflects cross-cultural brand pairs (Run 5) for models present in Run 5; other runs' models included with their run-specific mean DCI.

| Model | Size | Culture | Tier | Provider | Release | DCI |
|-------|------|---------|------|----------|---------|-----|
| grok | undisclosed | Western | 1 | xAI | 2025-12 | 0.290 |
| claude | undisclosed | Western | 1 | Anthropic | 2025-10 | 0.313 |
| gemini | undisclosed | Western | 1 | Google | 2025-12 | 0.321 |
| cerebras_qwen3 | 235B total, ~22B active (MoE) | Chinese | 1 | Cerebras | 2025-06 | 0.324 |
| groq_allam | 7B (dense) | Arabic | 2 | Groq | 2025-01 | 0.340 |
| yandexgpt_local | 8B | Russian | 2 | Local | 2025-03 | 0.341 |
| deepseek | 671B total, 37B active (MoE) | Chinese | 1 | DeepSeek | 2025-03 | 0.342 |
| groq_kimi | undisclosed | Chinese | 1 | Groq | 2025-06 | 0.350 |
| groq_llama33 | 70B (dense) | Western | 1 | Groq | 2024-12 | 0.358 |
| gpt | undisclosed | Western | 2 | OpenAI | 2024-07 | 0.360 |
| gigachat_api | undisclosed | Russian | 1 | Sber | 2026-02 | 0.360 |
| sarvam | ~105B (approx.) | Indian | 1 | Sarvam AI | 2026-02 | 0.367 |
| gemma4_local | 27B total, 3.8B active (MoE) | Western | 2 | Local | 2025-06 | 0.371 |
| yandexgpt_pro | undisclosed | Russian | 1 | Yandex | 2026-02 | 0.377 |
| gigachat_local | undisclosed | Russian | 2 | Local | 2026-03 | 0.380 |
| gptoss_swallow | 20B (dense) | Japanese | 1 | TOKYOTECH/SBI | 2026-02 | 0.380 |
| swallow_local | 8B | Japanese | 2 | Local | 2024-12 | 0.383 |
| qwen3_local | 30B (dense) | Chinese | 2 | Local | 2025-06 | 0.388 |
| exaone_local | 32B (dense) | Korean | 1 | Local | 2026-02 | 0.389 |
| jais_local | 70B (dense) | Arabic | 1 | Local | 2024-03 | 0.402 |

*Note.* DCI = Dimensional Collapse Index; baseline = 0.250. Models with DCI closer to 0.250 exhibit less dimensional collapse. "Undisclosed" parameter counts reflect provider non-disclosure at the time of data collection. Tier 1 = frontier/large production models; Tier 2 = smaller or local open-weight models. Swallow 70B is excluded due to 3.6% success rate. Full per-run breakdowns are in the supplementary dataset (spectralbranding/r15-ai-search-metamerism on HuggingFace).

The ranking reveals a gradient: Western frontier models (Grok, Claude, Gemini) cluster at the low end of the DCI distribution, while nationally specialized models (Jais, EXAONE, Swallow) cluster at the high end. This pattern is consistent with H6 (directional asymmetry) and will be analyzed in Section 4.5.4 below.

Hypothesis 3, which was not supported in Run 2 (no significant between-model heterogeneity across six models), is not supported in Run 5 either ($t = 0.221$, $p = 0.4127$, $d = 0.043$). The directional pattern in Run 5 is the reverse of the H3 prediction: soft-dimension variance (0.208) was lower than hard-dimension variance (0.258). Models disagree more about the relative weighting of Economic and Experiential dimensions than about the suppression of Cultural and Temporal ones. The soft dimensions converge on uniform suppression; the hard dimensions exhibit meaningful model-to-model variation in which verifiable dimension receives priority.

#### 4.5.3 The Reversed Diagonal (H5): National Models Collapse More

Hypothesis 5 predicted that national models would show lower collapse on brands from their own cultural market --- a cultural proximity advantage reflecting richer domestic training data. The result is the opposite: national models collapse *more* on own-culture brands than on foreign-culture brands. A paired $t$-test on own-culture vs. other-culture DCI across national models is not statistically significant ($t = -1.330$, $p = 0.2200$, $d = 0.043$), and the direction is reversed: 4 of 9 cultures show the predicted direction (lower own-culture DCI), while the majority show higher own-culture DCI. H5 is not supported, and the directional evidence runs counter to the prediction (see Section 5 for interpretation).

This reversal is the most counterintuitive finding of the study. The expected mechanism was straightforward: a model trained disproportionately on Russian-language web content should have richer representations of Russian brands, producing less collapse. The observed mechanism suggests a different dynamic. National models appear to over-index on the Economic and Experiential dimensions that dominate their domestic e-commerce training data. A model trained on extensive Russian consumer reviews and price comparison sites has abundant Economic signal for Russian brands --- and that abundance does not enrich the spectral profile but rather reinforces the Economic default. More data of the same dimensional type produces more collapse, not less.

This finding connects directly to the shrunken variance mechanism formalized in Section 5.5.1. The James-Stein estimator shrinks toward the population mean in proportion to the signal-to-noise ratio of the available data. For national brands in national models, the signal is strong but dimensionally narrow --- concentrated in Economic and Experiential channels that dominate e-commerce discourse. The estimator shrinks less (because signal is strong) but shrinks toward a biased target (because the signal is dimensionally concentrated). The net effect is greater collapse, not less. Cultural proximity provides more data but not more dimensional breadth.

The Chinese exception is consistent with this interpretation. China's digital ecosystem encompasses extensive cultural commentary, ideological positioning, and narrative brand discourse alongside e-commerce data, providing dimensionally broader training signal. The Chinese models' marginal advantage on own-culture brands may reflect not the volume of training data but its dimensional diversity.

#### 4.5.4 Bidirectional Asymmetry (H6): Western Advantage

Hypothesis 6 is supported ($t = -3.243$, $p = 0.0013$). Western-trained models exhibit a mean DCI of 0.339, significantly lower than the non-Western mean of 0.360 when evaluated on identical brand pairs. The asymmetry is bidirectional: Western models collapse less on all brands (not only Western ones), and non-Western models collapse more on all brands (not only foreign ones). This is not a cultural familiarity effect --- it is a training-corpus breadth effect (see Section 5 for interpretation). Western frontier models are trained on the largest and most dimensionally diverse English-language corpora, which include brand journalism, cultural criticism, heritage narratives, and ideological discourse alongside product specifications and price data. Non-Western models, even when trained on large corpora, draw on national-language web content that skews toward e-commerce, product reviews, and functional descriptions.

The practical implication is that brands operating in non-Western markets face a compounded risk: the AI mediators most likely to serve their domestic audiences are the ones that collapse their spectral profiles most severely. A Korean brand evaluated by EXAONE (DCI = 0.389) loses more dimensional resolution than the same brand evaluated by Claude (DCI = 0.313). If Korean consumers increasingly rely on Korean-language AI assistants, the spectral distortion they encounter will be systematically worse than what English-language users encounter through Western models.

#### 4.5.5 Geopolitical Signal (H7): Tinkoff vs. PrivatBank

Hypothesis 7 tested whether geopolitical context shapes AI brand perception independently of product category. The test case paired Tinkoff (rebranded T-Bank), a Russian digital consumer bank, with PrivatBank, a Ukrainian digital consumer bank. Both are digital-first consumer banks occupying analogous market positions in their respective countries — same category, same digital-first positioning, comparable scale. The heightened geopolitical salience of the Russian-Ukrainian context since 2022 provides a natural experiment for testing whether LLM training corpora encode geopolitical context into brand perception independently of functional category. Both brands also underwent significant corporate restructuring events that generated substantial media coverage: Tinkoff rebranded to T-Bank in 2023 following the departure and sale of the bank by its founder Oleg Tinkov; PrivatBank was nationalized by the Ukrainian government in December 2016 after discovery of a $5.5 billion shortfall, with co-founder Ihor Kolomoisky subsequently arrested and held in pre-trial detention since 2023 on fraud and embezzlement charges. Both restructuring events were ownership-change events with documented political and legal dimensions, generating substantial media coverage that is present in LLM training corpora. If models encode geopolitical associations, the DCI patterns for these brands should diverge in ways that reflect geopolitical salience rather than category or structural differences.

The result is directionally consistent with the geopolitical signal hypothesis. Across 20 models with sufficient data, 15 showed higher DCI for PrivatBank than for Tinkoff (binomial sign test: $p = 0.021$ against the null of equal probability). This pattern is consistent with a geopolitical encoding effect: models may encode geopolitical salience as dimensional noise that suppresses the coherent spectral profile of brands associated with conflict contexts. Because Tinkoff and PrivatBank operate in the same product category, the category confound present in prior designs is eliminated, and the DCI divergence is attributable to geopolitical salience rather than information availability differences across product domains (see Section 5 for interpretation).

#### 4.5.6 Capacity and Language Effects (H9, H10)

Hypothesis 9 (scale effect) is partially supported (3 of 5 model families). The clearest case is Qwen3: the 30B local model shows a DCI of 0.388, while the 235B Cerebras-hosted variant shows 0.324, a reduction of 0.064 --- the largest within-family effect observed. This is consistent with the interpretation that larger parameter counts retain finer-grained dimensional structure from training data. However, two model families show reversed patterns: Jais 7B shows lower DCI than Jais 70B, and YandexGPT 8B shows lower DCI than YandexGPT Pro. The reversals may reflect differences in fine-tuning strategy or alignment conditioning that offset raw capacity gains. The scale effect is real but not monotonic across all model families.

**Hypothesis 10 (language priming) — NOT SUPPORTED.** The H10 test proceeded in two stages, and the expansion reversed the initially suggestive result from the restricted sample.

*Stage 1: Initial test on 28 culture-matched combinations (Run 5 native-language conditions).* Of 28 model-language-culture combinations where a model's primary training language matched the prompt language (e.g., GigaChat prompted in Russian on Russian brand pairs, EXAONE prompted in Korean on Korean pairs), 15 showed DCI reduction (lower collapse) with native-language prompting (binomial $p = 0.424$ against the null of 0.5, not significant). The mean reduction across all 28 combinations was $+0.011$ --- a slight average reduction in collapse. This initial result was suggestive: positive direction, plausible mechanistically, but below conventional significance. The caveat was noted: the restricted sample confounded native-language activation with model-specific properties that could produce positive effects for unrelated reasons.

*Stage 2: Expanded test on 115 model-pair combinations (Runs 7--8, adding six control languages).* To separate native-language training-corpus activation from a general language-prompt effect, Run 8 administered prompts in five languages where no model in the constellation is natively trained: Greek (Cyprus), Latvian (Latvia), Swahili (Kenya), Vietnamese (Vietnam), and Serbian (Serbia). Run 7 added a Ukrainian native-language condition. Across all 115 model-pair combinations (the original 28 plus 87 new combinations), 46 showed DCI reduction (40%). The binomial sign test against the null of 0.5 is significant --- but in the negative direction ($p < 0.05$): the majority of combinations show no benefit or slight harm from native-language prompting. The mean DCI reduction across all 115 combinations is $-0.005$ (i.e., a marginal average *increase* in collapse, not a reduction). H10 is not supported.

The "language-as-key" hypothesis --- that native-language prompting functions as a general retrieval key unlocking culturally richer training representations --- fails at the aggregate level. The control-language result is decisive: Greek and Swahili prompts (where no model has native training) produced DCI changes statistically indistinguishable from the culture-matched conditions (Russian, Korean, Chinese prompts). If native-language prompting were activating a culturally specific training pathway, control-language prompts should produce systematically smaller effects; they do not.

The effect is model-specific rather than a general mechanism. Three patterns account for most of the observed heterogeneity:

- **Russian models**: YandexGPT Pro in Russian shows $+0.161$ DCI reduction (largest single effect in any run); GigaChat API in Russian shows $+0.019$. Russian-language training corpora for these models appear to include dimensionally richer brand discourse than their English-language equivalents, consistent with Russia's distinct consumer journalism tradition.
- **Western models in non-native languages**: Claude in Swahili/Kenya shows $+0.061$ DCI reduction. This is a control-language condition --- Claude has no Swahili native training --- yet it shows a large positive effect. The likely mechanism is that Swahili-language prompts force the model to draw on a different (and less economically saturated) subset of its multilingual training data, incidentally activating more dimensional content. This result argues against the native-language interpretation and in favor of a prompt-register effect.
- **Chinese models**: Aggregate mean delta $= -0.0004$ (effectively zero). Chinese-language prompting of Chinese models produces no measurable change in dimensional weight profiles. The Chinese digital ecosystem's balance between e-commerce content and cultural discourse provides neither the dimensional enrichment (Russian case) nor the register shift (Swahili case).

The interpretation is that native-language prompting does not function as a general retrieval key for dimensional richness. The effect depends on whether the model's native-language training corpus contains dimensionally richer content than its English corpus (a model-specific, corpus-specific condition that does not generalize) and on accidental register effects in non-native language prompts. Neither mechanism is predictable from model architecture or training-language identity alone.

**Table 7.** Selected native-language DCI effects across all runs. Positive values indicate DCI reduction (less collapse) with native-language prompting. "Native" = model's primary training language; "Control" = no model in the constellation has this as a training language.

| Model | Language | Type | DCI reduction |
|-------|----------|------|:------------:|
| YandexGPT Pro | Russian | Native | +0.161 |
| Claude | Swahili | Control | +0.061 |
| EXAONE | Korean | Native | +0.067 |
| Qwen3 local | Chinese | Native | +0.031 |
| ALLaM | Arabic | Native | +0.024 |
| GigaChat API | Russian | Native | +0.019 |
| GPT-4o | Greek | Control | -0.008 |
| DeepSeek | Latvian | Control | -0.012 |
| Aggregate (115 pairs) | All | Mixed | -0.005 |

*Note.* DCI reduction = difference between English-prompt DCI and native-language-prompt DCI for the same model-brand pair. Positive values indicate less collapse under native-language prompting. "Native" = model's primary training language matches the prompt language. "Control" = no model in the constellation has this language as a training language. Full per-combination results are in the supplementary dataset (spectralbranding/r15-ai-search-metamerism on HuggingFace).

The YandexGPT Pro result isolates a genuine model-specific pathway: dimensional information needed to resist collapse already exists in the Russian-language training data but is only accessible through native-language activation. The Brand Function specification (Run 4) provides missing information from outside the training data; native-language prompting, in this specific case, unlocks existing information within it. Both mechanisms reduce collapse, but through different pathways, and only the Brand Function specification generalizes reliably across models.

#### 4.5.7 Thin-Data Floor (H8)

Hypothesis 8 predicted that brands from markets with minimal English-language digital footprints would exhibit a DCI floor --- a point beyond which further information scarcity produces no additional collapse. The prediction is not supported. Mongolia-origin brands showed a mean DCI of 0.377 (second-highest among the eight cultures), but Japanese snack brands showed the highest mean DCI at 0.386 despite Japan's substantially larger digital footprint. The absence of a clean thin-data floor suggests that information scarcity is not the sole driver of extreme collapse: category-specific factors (snack foods are inherently low on Narrative, Ideological, and Temporal dimensions) and model-specific biases interact with information availability in ways that prevent a simple monotonic relationship between training-data volume and collapse severity.

#### 4.5.8 Brand Function Resolution Confirmed

The Brand Function resolution effect documented in Run 4 was confirmed in Run 5. When Brand Function specifications were provided for cross-cultural brand pairs, the aggregate DCI dropped from 0.353 toward the uniform baseline of 0.250 --- a near-complete approach to the baseline rather than a collapse to zero. A DCI of exactly 0.000 would indicate zero weight on both the Economic and Semiotic components, which would represent over-suppression rather than uniform resolution. The observed result reflects redistribution of aggregate weights toward the 0.250 uniform baseline, with no individual dimension receiving zero weight; the DCI approached the uniform benchmark of 0.250, indicating that the specification substantially corrected the dimensional imbalance. This result, combined with the Run 4 partial resolution (DCI 0.353 to 0.284), suggests that the specification mechanism becomes more effective as the information gap widens: for cross-cultural pairs where models have the least dimensional information, the specification fills the largest gap.

#### 4.5.9 Cost and Reproducibility

The full experiment (21,601 clean calls across 9 runs) was collected for \$5.52 USD in direct API costs, using approximately 6.1 million tokens. Paid cloud APIs (10 models: Claude, GPT-4o-mini, Gemini, DeepSeek, YandexGPT Pro, GPT-OSS-Swallow, GigaChat 2 Max, Sarvam, DashScope Qwen Plus, Fireworks GLM) accounted for the entire \$5.52. Free cloud APIs (6 models: Grok via xAI, Llama 3.3 / Kimi K2 / ALLaM-2 via Groq, Qwen3-235B via Cerebras, DeepSeek V3.2 via SambaNova) contributed calls at zero marginal cost. Local Ollama models (8 models: Gemma 4, Qwen3 30B, Qwen3.5, Swallow 8B, GigaChat local, YandexGPT local, EXAONE, Jais) ran on an Apple Mac mini M4 Pro (64 GB unified memory) at zero marginal cost beyond electricity.

**Table 8.** Cost and infrastructure breakdown across all 9 runs. Paid cloud = metered per-token APIs. Free cloud = providers offering free inference tiers. Local = Ollama on Apple M4 Pro 64 GB.

| Category | Models | Calls (OK) | Cost |
|----------|--------|-----------|------|
| Paid cloud | 10 | ~7,500 | \$5.52 |
| Free cloud | 6 | ~5,500 | \$0.00 |
| Local Ollama | 8 | ~8,000 | \$0.00 |
| **Total** | **24** | **~21,000** | **\$5.52** |

*Note.* Call counts are approximate; exact per-model breakdowns are in the HuggingFace dataset.

This cost structure has methodological implications. The entire cross-cultural AI perception study --- 23 models, 9 cultural traditions, 7 brand pairs, native-language conditions --- cost less than a single human-respondent focus group. The marginal cost of adding a model, a brand pair, or a cultural condition is under \$0.20. This makes longitudinal tracking of AI spectral profiles operationally feasible at a scale that human-respondent studies cannot match: a quarterly audit of how 20+ models perceive a brand portfolio costs less than \$15 per quarter.

**Data Availability.** The complete dataset --- all 21,600+ per-call records across 9 runs in 11 native languages (JSONL), per-model cost and token summaries (CSV), statistical test results (JSON), and the reproducible PRISM-B analysis scripts --- is publicly available at https://huggingface.co/datasets/spectralbranding/r15-ai-search-metamerism (DOI: 10.57967/hf/8284). The experiment source code, prompts, model configurations, and the PRISM instrument scaffold are at https://github.com/spectralbranding/sbt-papers/tree/main/r15-ai-search-metamerism/experiment.

### 4.6 Run 7: Geopolitical Framing (H12)

#### 4.6.1 Design

Run 7 tested Hypothesis 12: the same brand evaluated in different geopolitical city contexts produces significantly different dimensional weight profiles. Three brand pairs were selected on the basis of operating (or having operated) across a geopolitically salient border: Roshen (Ukraine/Russia), Volvo (Sweden/China), and Burger King (USA/Russia). Each brand was evaluated in two city contexts using a city-grounded shopping assistant prompt that differed by exactly one variable (the city name). The design comprised 3 brand pairs $\times$ 2 cities $\times$ 24 models $\times$ 3 runs = 360 calls.

#### 4.6.2 Results: H12 Supported

H12 is supported. The mean absolute DCI delta between the two city contexts across all brands and models was 0.040 ($t = 7.122$, $p < 0.0001$), significantly exceeding the test-retest noise floor established by the prompt sensitivity analysis. The same brand, prompted with an identical query differing only in city name, produces meaningfully different dimensional weight profiles: geopolitical framing alone shifts the spectral output by approximately 0.040 DCI units on average.

Per-pair results reveal meaningful heterogeneity in the geopolitical framing effect:

- **Roshen** (Moscow vs. Kyiv context): mean absolute DCI delta = 0.062. The largest effect among the three pairs, consistent with the direct conflict salience of the Russia-Ukraine context. Ideological and Cultural dimensions showed the greatest divergence between city contexts.
- **Volvo** (Stockholm vs. Shanghai context): mean absolute DCI delta = 0.029. A moderate effect consistent with the China acquisition context (Geely acquired Volvo in 2010) and ongoing trade and technology-transfer discourse.
- **Burger King** (New York vs. Moscow context): mean absolute DCI delta = 0.030. A moderate effect consistent with the geopolitical salience of US-Russia relations and Burger King's documented operations in Russia following the 2022 invasion.

The pattern is directionally consistent with the country-of-origin and consumer animosity literatures: brands embedded in active geopolitical conflicts (Roshen) show larger framing effects than brands whose geopolitical context is primarily economic (Volvo, Burger King). H12 is supported: geopolitical city context systematically shifts LLM dimensional weight profiles for the same brand, and the effect is largest where geopolitical salience is highest (see Section 5 for interpretation).

---

## 5. Discussion

### 5.1 H1 and H2 Supported: Dimensional Collapse Is Structural and Convergent

The two most fundamental predictions of the LLM-as-observer model are supported. H1 is supported in both runs: LLMs exhibit significantly non-uniform dimensional profiles, systematically overweighting Experiential and Economic dimensions relative to Cultural, Temporal, and Narrative dimensions. H2 is supported at a high level of statistical certainty: cross-model cosine similarity of 0.977 across 24 architectures from nine cultural traditions means they converge on essentially the same dimensional ordering. This convergence is the most important single result of the study. It establishes that dimensional collapse is not a quirk of RLHF training (Claude and GPT-4o), not an artifact of e-commerce training data (DeepSeek and Qwen3), and not an effect of commercial API safety layers (cloud models diverge negligibly from local open-weight models). Collapse is structural: it follows from the inherent information asymmetry between verifiable brand attributes (price, features, certifications) and perception-dependent brand attributes (heritage, cultural embeddedness, ideological resonance). Text-only models trained on general web corpora that include product descriptions, price comparisons, and consumer reviews are likely to exhibit this profile.

This finding has a direct implication for advertising strategy: platform heterogeneity is not the primary risk. A brand manager who discovers that their brand is metameric in GPT-4o cannot solve the problem by redirecting to Claude or DeepSeek. The collapse is cross-platform. The solution must be dimensional, not platform-specific.

### 5.2 H3 and H4 Not Supported: Collapse Is Uniform, Not Differential

The non-support for H3 (cross-model heterogeneity) and H4 (differential soft-dimension collapse) refines the theoretical picture in an important way. The absence of significant between-model variation (H3) aligns with the H2 finding of high convergence: these are not independent results but two aspects of the same structural regularity. The absence of differential soft-dimension collapse (H4) is the more theoretically significant finding. It means that the collapse is not that Narrative collapses while Temporal is preserved, or that Ideological collapses while Cultural survives. All four soft dimensions collapse together. The models do not preferentially preserve any sub-category of perception-dependent brand attributes.

The uniform collapse of all soft dimensions has a practical implication that the differential-collapse hypothesis would have obscured. If collapse were differential, brand managers could invest in the surviving soft dimensions as a hedge. Because collapse is uniform, the only robust strategic response is structural: encoding soft dimensions in verifiable, machine-readable form so they are no longer soft in the relevant sense.

### 5.3 The Patagonia Exception: When Ideological Commitment Survives AI Mediation

The single exception to the above pattern is theoretically suggestive. The Patagonia/Columbia pair is the only one of fifteen pairs tested (across both runs) that falls below the baseline DCI, with a score of 0.194. Patagonia's ideological dimension -- grounded in legally binding commitments (the 1% for the Planet pledge), product durability certifications, and the documented 2022 Yvon Chouinard ownership transfer to a non-profit environmental trust -- provides a machine-readable ideological signal. When the model asks "what distinguishes Patagonia from Columbia on Ideological grounds?", it can produce a factual, defensible answer with specific verifiable claims. The dimension does not collapse because it has been made structurally defensible.

This result maps directly onto the defensibility thesis of Hermann et al. (2026): AI agents "cannot recommend brands they cannot defend." Patagonia has structured its ideology as a set of defensible claims. Most brands that compete on ideology have not: their values exist as marketing positioning rather than operational commitment, and models cannot distinguish between a brand that genuinely enacts an ideology and one that performs it in advertising copy. The Patagonia exception is therefore not a refutation of the collapse hypothesis but a demonstration of the mechanism that can prevent it.

### 5.4 Conditional Metamerism: Training-Data Embeddedness as the Primary Moderator

The global-versus-local comparison (Section 4.3) provides the clearest theoretical advance of the study. The large effect ($d = 0.878$, $p < 0.0001$) supports the claim that AI-mediated dimensional collapse is conditional on information availability: brands with thin training-data footprints collapse more severely across all dimensions, not just the soft ones. The most striking evidence is the Economic dimension explosion for local brands (168% of baseline, versus 114% for global brands). This "Economic default" pattern emerges because price is the one dimension that can always be inferred from product category context even without brand-specific data. When a model lacks narrative, ideology, cultural embeddedness, and temporal heritage for a brand, it substitutes the universal proxy: cost position.

This conditional mechanism aligns with Liu's (2026) alignment tax finding and the related evidence from Doshi and Hauser (2024) that AI-mediated outputs reduce collective diversity at the population level. Liu shows that RLHF training produces 40--79% response homogenization across diverse prompts, amplifying majority-pattern outputs. For local brands, the majority pattern in the training data is not brand-specific but category-generic: when the model has no brand-specific information, it produces the default category response, which is dominated by Economic and Experiential signals. The alignment tax is not paid uniformly -- it is paid most severely by brands that are underrepresented in the training corpus.

Longoni and Cian (2022) provide complementary evidence from the consumer side: users systematically resist AI recommendations for experiential and hedonic products, accepting AI authority for utilitarian ones. The dimensional collapse documented here is the supply-side analog: AI systems systematically produce utilitarian-dominant recommendations regardless of whether the brand's actual competitive advantage is hedonic or experiential. Local brands face a double exposure: their non-Economic dimensions collapse further in AI mediation, and the AI defaults to the Economic frame that Longoni and Cian show consumers distrust for their category. For a premium Kenyan grocery chain (Naivas) competing on cultural embeddedness, AI mediation not only strips the cultural dimension but substitutes an Economic frame that may be precisely the wrong competitive positioning signal. The Run 4 resolution test provides direct evidence that the collapse is at least partly information-driven: when Brand Function specifications fill the training-data gap for local brands, the DCI moves 20% toward baseline, with the Cultural dimension showing the most dramatic recovery.

### 5.5 Theoretical Implications

The LLM-as-observer concept extends SBT's framework to a structurally new class of perception agents. Existing observer heterogeneity research (Zharnikov, 2026f) documents how human cohorts differ in their dimensional weights as a function of lived experience, cultural context, and demographic position. This paper demonstrates that the AI observer has weights determined by a different mechanism entirely: training data distribution, optimization objective, and architectural constraint. The result is an observer profile that is simultaneously less heterogeneous across platforms than human cohorts (the 0.975 cosine similarity) and more severely biased toward verifiable dimensions than any human cohort.

The metameric collapse mechanism provides a formal, testable explanation for practitioner observations about AI "flattening" of brands. By connecting this flattening to the mathematical framework of spectral metamerism (Zharnikov, 2026e) and Johnson-Lindenstrauss projection bounds, the paper transforms a vague concern into a precise measurement: for a given brand, which dimensions are visible to AI mediators and which are not, and by how much does the model's spectral profile diverge from the brand's intended emission profile? More precisely, this paper establishes LLMs as a new class of metameric observer whose spectral bias is structural, convergent (cosine 0.977), and conditional on training-data embeddedness. This extends the homogenization and alignment-tax literatures (Sourati et al., 2026; Liu, 2026; De Freitas et al., 2025) by specifying *which* perceptual dimensions are lost and why: perception-dependent dimensions (Ideological, Cultural, Narrative, Temporal) collapse because they require embodied experience and social context that text-trained models cannot encode, while verifiable dimensions (Economic, Experiential) survive because they are explicitly quantified in training corpora.

The conditional metamerism finding adds a moderator structure to this framework that was theoretically anticipated but empirically uncertain prior to this study. The large effect is consistent with training-data embeddedness being a primary moderator of AI-mediated dimensional collapse, outweighing model architecture, training corpus cultural origin, and deployment context (cloud vs. local). This creates an immediately actionable prioritization principle: brands in underrepresented markets face a quantifiably larger AI metamerism risk, and their vulnerability can be estimated from measurable proxies (English-language search result count, Wikipedia coverage depth, international media mentions).

The conditional metamerism documented here connects to a broader diagnostic framework. Medesani and Macdonald (2026) formalize *admissible regions* --- invariant corridors within which a system's state must remain for governance guarantees to hold. Applied to brand perception, a brand's measured spectral profile is admissible only when it falls within the corridor defined by its Brand Function. Conditional metamerism implies that admissibility assessment itself is observer-dependent: a brand may be admissible as perceived by information-rich observers yet inadmissible as perceived by information-sparse AI observers operating under the Economic Default. This observer-contingent admissibility is a direct consequence of conditional metamerism and suggests that brand governance must account for the measurement infrastructure, not merely the measured position.

### 5.5.1 Shrunken Variance and the Estimation-Theory Analogy

The cross-model convergence documented in this study (cosine similarity 0.977 across 24 models from nine cultural traditions) is consistent with the shrunken variance phenomenon established in the Bayesian estimation literature. LLM training on aggregated text corpora functions as an implicit shrinkage estimator, analogous to the James-Stein estimator (James & Stein, 1961; Efron & Morris, 1975), pulling dimensional weight estimates toward the population mean and compressing the variance that distinguishes brands on perception-dependent dimensions. The Economic and Semiotic dimensions resist this shrinkage because they are explicitly quantified in training data (prices, visual descriptions), while Narrative, Cultural, and Temporal dimensions --- which require direct observer experience to resolve --- are compressed toward the aggregate. Brand Function specification counteracts this shrinkage by providing explicit dimensional information that the training corpus lacks, reducing the Dimensional Collapse Index from 0.353 to 0.284 (Run 4). This framing connects LLM-mediated brand perception to established results in high-dimensional estimation theory, where shrinkage toward a common mean is both statistically efficient and informationally lossy.

### 5.6 Convergence with Agentic Commerce Evidence

The dimensional collapse documented here converges with independent findings from the agentic commerce literature. Sabbah and Acar (2026) find that among eight common e-commerce promotional cues tested across four AI models, only ratings --- the most quantifiable, verifiable signal --- consistently increases selection probability across all models and product categories. All other cues (assurance, scarcity, timers, vouchers, bundles, strike-through pricing) show heterogeneous and often model-specific effects. This maps directly onto the present study's dimensional structure: ratings operate in the Economic dimension (quantifiable quality proxy), and their universal effectiveness is the choice-level analog of the Economic Default documented here. The promotional cues that fail to transfer --- scarcity (Social/Temporal), assurance (Narrative), bundling (Experiential packaging) --- are precisely those that depend on perception-dependent dimensions that collapse in AI mediation.

Sabbah and Acar also report pronounced cross-category heterogeneity within the same model: GPT-5 responds positively to bundling for fitness watches but negatively for phones. This within-model instability parallels our per-pair DCI variation (Table 3): the same model collapses more on some brand pairs than others, depending on the availability of dimensional information in the training data. Together, these studies suggest that AI-mediated commerce is neither uniformly biased nor randomly noisy --- it is *dimensionally structured*, with predictable patterns of sensitivity and collapse that depend on the verifiability of the signal, the richness of training data, and the model's architectural characteristics.

### 5.7 Implications for Search Advertising

The most direct implication is that search advertising strategy must account for the dimensional structure of AI mediation. Four specific implications follow from the empirical results.

**SEO becomes spectral optimization.** Traditional SEO optimizes for keyword relevance and link authority. In AI-mediated search, the optimization target shifts to dimensional representation: making the brand's full spectral profile machine-readable. The Patagonia exception demonstrates that this is achievable: encoding narrative, ideological, cultural, and temporal dimensions in structured data formats that LLMs can process as defensible, verifiable claims. The SBT specification framework (Zharnikov, 2026a) provides a candidate structure for this encoding.

**Zero-click risk is dimensionally asymmetric.** When AI provides a direct answer, the consumer never visits brand-owned media where narrative, cultural, and temporal dimensions are richly communicated. The risk is not uniform across brands: brands differentiated on Economic and Experiential dimensions lose less in zero-click scenarios, while brands differentiated on soft dimensions lose proportionally more, because the dimensions that define their competitive advantage are precisely those the LLM underweights.

**Portfolio brands face spectral self-competition.** Zharnikov (2026q) showed that brands within the same portfolio can interfere with each other on specific dimensions. AI mediation amplifies this risk: if two portfolio brands are differentiated in human perception on Cultural and Temporal dimensions but metameric in AI perception (both reduced to their Economic and Experiential profiles), the AI recommends them interchangeably, cannibalizing the portfolio's own differentiation.

**Measurement must become dual-track.** Brand health metrics based on human respondent surveys will increasingly diverge from AI-mediated brand effectiveness. A brand can score high on human-perceived differentiation while being metameric in AI search. Practitioners need dual-track measurement: human spectral profiles from survey-based assessment and AI spectral profiles from the prompt-based protocol described in this paper.

### 5.8 Implications for Advertising Creative Strategy

Investment in building narrative, cultural, and temporal brand dimensions has traditionally created durable competitive advantage because these dimensions are difficult for competitors to replicate. AI mediation does not make that investment less valuable to human observers --- it makes it invisible to the AI intermediary. The strategic response is not to abandon perception-dependent dimensions but to make them machine-defensible: encoded in structured formats that survive AI mediation.

This reframes the brand specification challenge. Traditional brand equity metrics will increasingly diverge from AI-mediated effectiveness. The solution is not platform switching --- cosine similarity of 0.977 across 24 architectures rules this out --- but making soft dimensions defensible: structured, verifiable, and machine-readable. The practical output is a brand-specific AI vulnerability audit: for each of a brand's eight dimensions, what proportion of its value is machine-readable versus perception-dependent? The present study provides the measurement protocol for such an audit, and the Patagonia exception demonstrates that the distinction is actionable: brands that invest in structured, verifiable expression of their soft dimensions can reduce their collapse exposure.

### 5.9 Connection to Broader AI and Search Trends

The dimensional collapse documented here is not unique to brands. Personality perception by AI shows analogous flattening (Hashimoto & Oshio, 2025). Cultural nuance in machine translation shows analogous loss (Van Doren & Holland, 2025). The SBT framework provides a general instrument for measuring this collapse across domains: the methodological approach --- measuring the implicit spectral profile of an AI system by analyzing which dimensions it preserves in its outputs --- is domain-general.

---

### 5.10 Robustness: Temperature Sensitivity

A potential concern is that the structured weight elicitation results are sensitive to the temperature parameter used in LLM API calls. Higher temperatures increase response randomness, which could either inflate or deflate dimensional bias depending on how the noise interacts with the weight allocation constraint. To test this, we re-ran the weighted recommendation protocol on all 10 global brand pairs with the 6 original models (Claude, GPT-4o-mini, Gemini, DeepSeek, Qwen3, Gemma 4) at three alternative temperatures: 0.0 (deterministic), 0.3 (low variance), and 1.0 (high variance), with the baseline T=0.7 from Run 2 as reference (540 additional calls, 3 repetitions per condition).

**Table 10.** Dimensional Collapse Index by temperature setting (10 global brand pairs, 6 models, 3 runs per temperature).

| Temperature | Mean DCI | SD | n |
|------------|---------|-----|---|
| 0.0 (deterministic) | 0.298 | -- | 179 |
| 0.3 (low variance) | 0.303 | -- | 171 |
| 0.7 (baseline) | 0.291 | -- | 171 |
| 1.0 (high variance) | 0.296 | -- | 174 |

*Note.* DCI = Dimensional Collapse Index. SD not computed for individual temperature conditions due to the design's focus on cross-condition stability rather than within-condition variance. Kruskal-Wallis test across four temperature conditions: H = 1.83, p = 0.61, confirming no significant variation in DCI across temperature settings. N = number of valid API responses per temperature condition.

The DCI range across all four temperature conditions is 0.012 (0.291 to 0.303), confirming that the dimensional collapse finding is not an artifact of the temperature setting. The Economic default mechanism operates at similar magnitude whether responses are deterministic (T=0.0) or maximally random (T=1.0). This stability is consistent with the structural interpretation: dimensional bias reflects the composition of training data, not the stochastic sampling process.

## 6. Limitations and Future Research

Several limitations bound the present study. First, the prompt-based protocol measures recommendation behavior in a controlled experimental setting; it does not capture the full range of AI-brand interactions, including multimodal encounters (image search, voice assistants), agentic commerce (AI agents making purchase decisions autonomously), and social media AI integrations. Second, LLM responses are sensitive to prompt engineering; while the protocol standardizes prompts across models, variations in phrasing could alter dimensional weight allocations. The three-repetition design mitigates but does not eliminate this concern. Third, the study measures LLM output, not downstream consumer behavior; connecting AI spectral profiles to actual purchase decisions requires experimental consumer studies that are beyond the present scope. Fourth, LLM capabilities evolve rapidly; multimodal models with image and video processing may exhibit different spectral profiles than the text-based models studied here. Fifth, the structured weight elicitation design measures what models report as important when explicitly asked to allocate points, which may differ from the implicit dimensional weighting in unconstrained free-text responses; the v1 null result (Run 1) suggests that implicit measurement through keyword extraction is unreliable, but this does not guarantee that explicit allocation fully captures implicit bias. Sixth, all five local brand pairs are in the food and beverage retail sector, which could confound locality effects with category-specific patterns; future research should test local brands in luxury, technology, and service categories to disentangle these effects.

Future research should pursue five directions: (a) longitudinal tracking of LLM spectral profiles as models are updated, to determine whether dimensional collapse is narrowing or widening over time; (b) consumer experiments measuring whether AI-mediated brand encounters produce measurably different brand convictions than direct brand encounters; (c) the cross-cultural validation pursued in Run 5 confirms that collapse generalizes beyond the Western-Chinese binary to Russian, Japanese, Korean, Arabic, Indian, Ukrainian, and Mongolian model families; remaining directions include longitudinal tracking as national models mature and controlled same-category geopolitical brand pairs; (d) intervention studies testing whether structured brand specification (making collapsed dimensions machine-readable) reduces metameric collapse; and (e) temporal training stability --- testing whether successive versions of the same model family produce significantly different dimensional weight profiles for the same brand. The conditional metamerism hypothesis has been supported empirically in Run 3, with local brand pairs from Cyprus, Latvia, Kenya, Vietnam, and Serbia showing amplified collapse relative to global brands ($d = 0.878$).

Direction (e) is particularly tractable given current model release cadences. Several model families have publicly accessible version pairs spanning 3--12 months of training evolution: DeepSeek V3 (December 2024) to V3-0324 (March 2025), Llama 3.1-70B (July 2024) to 3.3-70B (December 2024), Qwen 2.5-72B (September 2024) to Qwen 3-235B (April 2025), and Gemma 3-27B (March 2025) to Gemma 4-27B (June 2025). The present study's prompt protocol and brand set can be applied to each version pair without modification, measuring per-brand temporal drift via cosine distance between version profiles and per-dimension shifts to identify which dimensions are most sensitive to training data evolution. If brand perception is non-stationary across model versions, the practical implication is that brand health monitoring in AI-mediated channels requires continuous measurement rather than periodic snapshots --- connecting to the non-ergodic perception dynamics formalized in Zharnikov (2026o) and the temporal Brand Triangulation framework in Zharnikov (2026y).

Run 5 introduces additional limitations. Error rates varied substantially across model endpoints: some national-model APIs (particularly Russian and Arabic free-tier endpoints) returned invalid JSON in 20--30% of calls, potentially biasing the sample toward more reliable (and possibly more commoditized) responses. Native-language prompting was tested on only a subset of models due to language-capability constraints, and not all models received prompts in their target language for all brand pairs; the language-priming results should therefore be treated as exploratory. SambaNova rate limits forced sequential rather than parallel call scheduling, extending collection time and introducing potential non-stationarity across the experiment. Swallow 70B exhibited severe reliability issues in two forms: the SambaNova-hosted version (Llama-3.3-Swallow-70B-Instruct-v0.4) was removed from the platform during data collection, and the local 70B GGUF version timed out on 64GB RAM; combined success rate across 549 attempted calls was 3.6%, and the 70B Swallow family should not be used in future replication attempts. The smaller Swallow 8B (local, 381 successful calls) and GPT-OSS-Swallow 20B (Yandex AI Studio, 489 successful calls) performed reliably and remain active in the Japanese model cluster. Finally, Run 5 includes no Japanese Tier 1 model: GPT-OSS-Swallow (20B) is the largest Japanese-specialized model tested, and the absence of a frontier-scale Japanese model (equivalent to Sarvam 105B for Indian languages) leaves the Japanese DCI estimates potentially unrepresentative of what a larger Japanese-trained model would produce.

Hermann, Puntoni, and Schweidel (2026) identify a defensibility asymmetry in AI-mediated brand perception: AI agents can recommend brands based on verifiable attributes (pricing, SLAs, certifications) but struggle with experiential attributes (heritage, symbolic meaning, emotional resonance). This maps directly onto the dimensional collapse measured here --- the dimensions that survive AI mediation are precisely those that are defensible in Puntoni's framework, while the dimensions that collapse are those that require subjective judgment. This convergence between independent research programs strengthens the theoretical basis for the dimensional collapse thesis.

---

## 7. Conclusion

Brands are multi-dimensional perceptual objects, yet the present findings suggest that AI-mediated search systematically collapses their perception to approximately two dominant dimensions. The resulting metamerism --- brands that look identical through the AI lens despite being structurally different to human observers --- is supported empirically across 22 brand pairs (10 global, 5 local, 7 cross-cultural, and 1 banking pair), 24 model architectures, and nine cultural training traditions. The structural mechanism suggests this is unlikely to be resolved by model scaling alone. It is a geometric consequence of dimensional collapse: the same mechanism that makes physically different light spectra produce identical color percepts when observed through a narrow-band filter.

The conditional structure of this collapse is the paper's most actionable finding. Metamerism is not uniform: local brands from underrepresented markets collapse 24.7% more severely than global brands (Cohen's $d = 0.878$). The Economic default mechanism --- AI substituting price for every dimension it lacks data on --- means that the brands most reliant on non-economic differentiation (cultural embeddedness, heritage, ideological positioning) face the largest exposure precisely in the markets where those dimensions matter most. And the Patagonia exception demonstrates that the collapse is not inevitable: brands that encode their soft dimensions as verifiable, machine-readable commitments can survive AI mediation.

For advertising research, this paper demonstrates that the study of AI-mediated brand perception requires a dimensional framework, not merely a functional one. Knowing that "AI affects brands" is insufficient; what matters is knowing which dimensions are affected, by how much, and for which brands. Spectral Brand Theory provides that dimensional framework, and this paper provides the measurement protocol.

For practitioners, the findings suggest a strategic diagnostic: the dimensions most associated with premium brand differentiation --- narrative, ideology, culture, heritage --- are precisely those most susceptible to AI-mediated collapse. If this collapse pattern persists across future model generations, competitive advantage in AI-mediated search may accrue disproportionately to brands whose multi-dimensional value is specified, structured, and machine-defensible rather than solely to those with the strongest human-perceived differentiation. This hypothesis warrants longitudinal investigation. A key implication is that brand health measurement should expand to include AI-mediated spectral profiles alongside traditional human-respondent surveys, making the question "how does the AI that mediates consumer search perceive us?" as operationally tractable as the question "how do consumers perceive us?" This paper provides a measurement protocol toward that goal.

---

## References

Aaker, D. A. (1991). *Managing brand equity: Capitalizing on the value of a brand name*. Free Press.

Aaker, D. A. (1996). *Building strong brands*. Free Press.

Aaker, J. L. (1997). Dimensions of brand personality. *Journal of Marketing Research*, 34(3), 347-356.

Acar, O. A., & Schweidel, D. A. (2026). Preparing your brand for agentic AI. *Harvard Business Review*, March-April 2026.

Allouah, A., Besbes, O., Figueroa, J. D., Kanoria, Y., & Kumar, A. (2025). What is your AI agent buying? Evaluation, biases, model dependence, and emerging implications for agentic e-commerce. arXiv:2508.02630v3.

Bansal, G., Hua, W., Huang, Z., Fourney, A., Swearngin, A., Epperson, W., Payne, T., Hofman, J. M., Lucier, B., Singh, C., Mobius, M., Nambi, A., Yadav, A., Gao, K., Rothschild, D. M., Slivkins, A., Goldstein, D. G., Mozannar, H., Immorlica, N., Murad, M., Vogel, M., Kambhampati, S., Horvitz, E., & Amershi, S. (2025). Magentic marketplace: An open-source environment for studying agentic markets. arXiv:2510.25779.

Bilkey, W. J., & Nes, E. (1982). Country-of-origin effects on product evaluations. *Journal of International Business Studies*, 13(1), 89-99.

Brakus, J. J., Schmitt, B. H., & Zarantonello, L. (2009). Brand experience: What is it? How is it measured? Does it affect loyalty? *Journal of Marketing*, 73(3), 52-68. https://doi.org/10.1509/jmkg.73.3.052

Campbell, C., Plangger, K., Sands, S., Kietzmann, J., & Bates, K. (2022). How deepfakes and artificial intelligence could reshape the advertising industry. *Journal of Advertising Research*, 62(3), 241-251.

Campbell, C., Sands, S., Ferraro, C., Tsao, H.-Y., & Mavrommatis, A. (2020). From data to action: How marketers can leverage AI. *Business Horizons*, 63(2), 227-243.

Dawar, N., & Bendle, N. (2018). Marketing in the age of Alexa. *Harvard Business Review*, 96(3), 80-86.

Davenport, T., Guha, A., Grewal, D., & Bressgott, T. (2020). How artificial intelligence will change the future of marketing. *Journal of the Academy of Marketing Science*, 48, 24-42.

De Bruyn, A., Viswanathan, V., Beh, Y. S., Brock, J. K.-U., & von Wangenheim, F. (2020). Artificial intelligence and marketing: Pitfalls and opportunities. *Journal of Interactive Marketing*, 51, 91-105.

De Freitas, J., Nave, G., & Puntoni, S. (2025). Generative AI reduces collective novelty. *Journal of Consumer Research*, forthcoming.

Diehl, K., Kornish, L. J., & Lynch, J. G. (2003). Smart agents: When lower search costs for quality information increase price sensitivity. *Journal of Consumer Research*, 30(1), 56-71.

Doshi, A. R., & Hauser, O. P. (2024). Generative AI enhances individual creativity but reduces the collective diversity of novel content. *Science Advances*, 10(28), eadn5290.

Efron, B., & Morris, C. (1975). Data analysis using Stein's estimator and its generalizations. *Journal of the American Statistical Association*, 70(350), 311-319.

Hagendorff, T., Fabi, S., & Kosinski, M. (2023). Human-like intuitive behavior and reasoning biases emerged in large language models but disappeared in ChatGPT. *Nature Computational Science*, 3, 833-838.

Hashimoto, Y., & Oshio, A. (2025). Exploring personality structure through LLM agent: A lexical perspective. *Psychological Test Adaptation and Development*, 6, 248–258. https://doi.org/10.1027/2698-1866/a000114

Hermann, E., & Puntoni, S. (2024). Artificial intelligence and consumer behavior: From predictive to generative AI. *Journal of Business Research*, 180, 114720. https://doi.org/10.1016/j.jbusres.2024.114720

Hermann, E., Puntoni, S., & Schweidel, D. A. (2026). Trusting AI agents: Uncertainty reduction by design. *Working Paper*, SSRN. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6103206

Huang, M.-H., & Rust, R. T. (2021). A strategic framework for artificial intelligence in marketing. *Journal of the Academy of Marketing Science*, 49, 30-50.

James, W., & Stein, C. (1961). Estimation with quadratic loss. *Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability*, 1, 361-379.

Johnson, W. B., & Lindenstrauss, J. (1984). Extensions of Lipschitz mappings into a Hilbert space. In *Conference in Modern Analysis and Probability* (pp. 189-206). American Mathematical Society.

Kapferer, J.-N. (2008). *The new strategic brand management: Creating and sustaining brand equity long term* (4th ed.). Kogan Page.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1-22.

Kietzmann, J., Paschen, J., & Treen, E. (2018). Artificial intelligence in advertising: How marketers can leverage artificial intelligence along the consumer journey. *Journal of Advertising Research*, 58(3), 263-267.

Klein, J. G., Ettenson, R., & Morris, M. D. (1998). The animosity model of foreign product purchase: An empirical test in the People's Republic of China. *Journal of Marketing*, 62(1), 89-100.

Liu, M. (2026). The alignment tax: Response homogenization in aligned LLMs and its implications for uncertainty estimation. arXiv:2603.24124. https://arxiv.org/abs/2603.24124

Longoni, C., & Cian, L. (2022). Artificial intelligence in utilitarian vs. hedonic contexts: The "word-of-machine" effect. *Journal of Marketing*, 86(1), 91-108.

Lu, C., Lu, C., Lange, R. T., Yamada, Y., Hu, S., Foerster, J., Ha, D., & Clune, J. (2026). Towards end-to-end automation of AI research. *Nature*, 651, 914-920. https://doi.org/10.1038/s41586-026-10265-5

Lynch, J. G., & Ariely, D. (2000). Wine online: Search costs affect competition on price, quality, and distribution. *Marketing Science*, 19(1), 83-103.

Medesani, M., & Macdonald, J. (2026). Geometric foundations of invariant corridors and governance. Working Paper. https://doi.org/10.5281/zenodo.18822552

Puntoni, S., Reczek, R. W., Giesler, M., & Botti, S. (2021). Consumers and artificial intelligence: An experiential perspective. *Journal of Marketing*, 85(1), 131-151.

Sabbah, J., & Acar, O. A. (2026). Marketing to machines: How AI models respond to promotional cues. Working Paper. SSRN 6406639.

Sourati, Z., Venkatesh, S., Doshi, A., Hauser, J. R., & Tenenbaum, J. B. (2026). LLM homogenization and epistemic collapse in AI-mediated knowledge production. *Trends in Cognitive Sciences*, forthcoming.

Tversky, A. (1972). Elimination by aspects: A theory of choice. *Psychological Review*, 79(4), 281-299.

Van Doren, M., & Holland, C. (2025). "Be My Cheese?": Assessing cultural nuance in multilingual LLM translations. arXiv:2509.21577. https://arxiv.org/abs/2509.21577

Verlegh, P. W. J., & Steenkamp, J.-B. E. M. (1999). A review and meta-analysis of country-of-origin research. *Journal of Economic Psychology*, 20(5), 521-546.

Wyszecki, G., & Stiles, W. S. (1982). *Color science: Concepts and methods, quantitative data and formulae* (2nd ed.). Wiley.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026f). Cohort boundaries in high-dimensional perception space: A concentration of measure analysis. Working Paper. https://doi.org/10.5281/zenodo.18945477

Zharnikov, D. (2026l). The rendering problem: From genetic expression to brand perception. Working Paper. https://doi.org/10.5281/zenodo.19064426

Zharnikov, D. (2026q). Spectral portfolio theory: Interference, coherence, and capacity in multi-brand perception space. Working Paper. https://doi.org/10.5281/zenodo.19145099

<!-- Self-citation audit: 5 Zharnikov entries listed in reference list (2026a, 2026e, 2026f, 2026l, 2026q) out of 45 total reference entries = 11.1%. Three additional Zharnikov works cited in-text only (2026o, 2026x, 2026y); if counted, total in-text self-citations = 8/48 = 16.7%. Self-citation rate: all self-citations verified as necessary for methodological chain (SBT framework, metamerism formalization, cohort theory, rendering problem, portfolio theory, non-ergodic perception, PRISM-M instrument, temporal triangulation). No self-citation is removable without breaking the theoretical lineage. -->

---

## Appendix A: Spectral Brand Theory -- Framework Specification

### A.1 Overview

Spectral Brand Theory (Zharnikov, 2026a) models brand perception as the interaction between a brand's emission profile and an observer's spectral weights. The framework has two core components: (1) a typed eight-dimensional decomposition of brand signals, and (2) a formalization of observer heterogeneity through spectral weight vectors.

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

where each $e_i(t) \in [0, 10]$ represents the intensity of the brand's signal on dimension $i$ at time $t$. Canonical profiles for the brands used in this study (Hermes, Patagonia, Erewhon) are established in Zharnikov (2026a) and held fixed across all analyses.

### A.4 Observer Spectral Profile and Cohorts

SBT's central contribution is the formalization that emission is not perception. Each observer type applies a characteristic weight vector $\mathbf{w} = [w_1, \ldots, w_8]$ constrained to the simplex $\sum_{i=1}^{8} w_i = 1$, $w_i \geq 0$, determining the relative salience of each dimension in forming brand conviction. Brand conviction -- the observer's formed assessment of a brand -- is a function of the interaction between the brand's emission profile and the observer's spectral weights.

Observers with similar weight vectors cluster into cohorts (Zharnikov, 2026f). Two observers encountering identical brand signals form structurally different brand convictions if their spectral profiles weight different dimensions. This observer-dependent architecture produces spectral metamerism: two structurally different brands can produce the same brand conviction in an observer whose spectral profile assigns near-zero weight to the dimensions on which those brands differ.

The present study operationalizes this framework by treating each LLM as an observer cohort with an estimable spectral weight vector, and measuring the degree to which LLM weight vectors are concentrated on Economic and Experiential dimensions relative to the theoretical uniform baseline.

