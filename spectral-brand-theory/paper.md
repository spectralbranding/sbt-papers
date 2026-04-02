# Spectral Brand Theory: A Computational Framework for Multi-Dimensional Brand Perception

**Dmitry Zharnikov**

Working Paper — February 2026 (revised April 2026)

*Zenodo DOI: [10.5281/zenodo.18945912](https://doi.org/10.5281/zenodo.18945912)*

---

## Abstract

This paper develops Spectral Brand Theory (SBT), arguing that brand perception is irreducibly observer-dependent: different observer cohorts perceive structurally different brands from identical signal environments. Unlike traditional brand frameworks that treat brand perception as a uniform property of the brand itself, SBT formalizes the observer as an active assembler of brand meaning. The framework decomposes brand signals across eight perceptual dimensions (semiotic, narrative, ideological, experiential, social, economic, cultural, temporal), defines observer cohorts through formal spectral profiles (sensitivity, weights, tolerances), and models brand perception as probabilistic cloud formation that collapses into conviction through evidence accumulation. We derive five formal propositions — on observer heterogeneity, non-ergodic perception, structural absence, coherence types, and conviction asymmetry — that formalize the framework's distinctive structural claims and specify testable predictions. We demonstrate the framework through structured analysis of five brands spanning luxury (Hermès), mass-market (IKEA), mission-driven (Patagonia), technology (Tesla), and hyperlocal niche (Erewhon). The structured analysis identifies nine candidate mechanisms, four of which are reported in depth: (1) structural absence as a brand strategy, where designed signal restriction generates value through what is not emitted; (2) a five-type coherence taxonomy, where brands with identical coherence scores exhibit fundamentally different resilience properties; (3) asymmetric conviction resilience, where evidence-free negative convictions are more stable than evidence-rich positive ones; and (4) the independence of brand power and brand health as measurable variables. The framework is computationally implementable: the entire analytical pipeline operates as a structured prompt sequence executable by large language models, compressing analysis that would require a multi-week consulting engagement into a single analytical session. Cross-model replication (Claude Opus 4.6 and Gemini 3.1 Pro across all five brands) confirms that structural conclusions are framework-driven rather than model-specific. The analyses constitute a structured demonstration of the framework's analytical capacity; empirical validation against independently collected consumer data remains for future work. An open-source toolkit is publicly available.

**Keywords:** brand perception, computational branding, observer heterogeneity, brand coherence, structural absence, AI-native framework

---

## 1. Introduction

Consider a thought experiment. Six people are asked to describe the same brand — Tesla. One says it is the most innovative technology platform since Apple. Another calls it Elon Musk's political vehicle. A third describes a betrayal of the environmental movement. A fourth sees a practical electric car with a controversial footnote. A fifth, who has never sat in one, holds a strong conviction about exactly what kind of person drives it. A sixth, in Shanghai, sees a premium Western status symbol and is puzzled by the question.

Same brand. Six descriptions. No overlap.

This is not a communication failure. It is a structural condition — and diagnosing it requires a vocabulary that traditional brand frameworks do not have. Each major framework captures a real aspect of brand dynamics but contains a structural limitation that prevents it from modeling the phenomenon above.

Ries & Trout's (1981) positioning theory treats brand perception as a single position in the consumer's mind — a slot to be occupied. The structural limitation is that "position" is singular: the framework has no mechanism for different observers assigning different positions to the same brand. Tesla does not occupy one position; it occupies at least six irreconcilable positions simultaneously, and no repositioning can collapse them into one.

Aaker's (1996) brand identity system describes what the brand *is* — its intended identity across functional, emotional, and self-expressive dimensions. The structural limitation is that identity is sender-side: the framework specifies what the brand emits but does not formalize the observer's role in assembling perceived meaning. Different observers receive the same identity signals and construct different brands; Aaker's model has no parameter for this divergence.

Kapferer's (2008) prism includes "reflection" and "self-image" facets that gesture toward the observer — an important acknowledgment that the receiver matters. The structural limitation is that these facets are not parameterized: Kapferer recognizes that different audiences see different reflections but provides no formal mechanism for specifying *how* or *why* the reflections differ across observer groups.

Keller's (1993) customer-based brand equity model locates equity in the customer's mind — the closest precedent to SBT's approach and the most important one. The structural limitation is that Keller treats "the customer" as a single model: one set of brand associations, one equity structure. The framework acknowledges individual variation but does not formalize it. SBT's central move is to parameterize exactly what Keller left as an acknowledged but unmodeled phenomenon — the heterogeneous observer.

Christodoulides & de Chernatony (2010) consolidate these equity-based approaches into a measurement framework that remains anchored to the single-observer assumption. The broader brand equity literature — including Feldwick's (1996) taxonomy distinguishing brand valuation, brand strength, and brand description; Ambler's (2003) operational metrics approach; and Wood's (2000) reconciliation of financial and consumer perspectives — operates within the same assumption: equity is a property of the brand-observer pair, but the observer is treated as singular. Keller & Lehmann (2006) survey the field's research priorities and identify measurement of brand equity as a central challenge — yet the measurement frameworks they review all assume a single "true" brand perception to be measured. The structural limitation across this measurement tradition is the premise that there exists one correct brand perception to measure, rather than multiple structurally different perceptions that are simultaneously valid.

Sharp's (2010) empirical marketing science measures mental and physical availability — how easily the brand comes to mind and how easily it can be purchased. The structural limitation is that availability is a pre-perceptual construct: Sharp measures whether the brand passes the identity gate but does not model the perception mechanism that translates availability into conviction. Two observers with identical availability can form opposite convictions; Sharp's framework cannot explain why.

The gap is not in any single framework. It is structural: brand measurement collapses multi-dimensional perception into single scores — Net Promoter Score, brand equity indices, awareness metrics — destroying the information that explains why six observers form six irreconcilable perceptions of the same brand. The information is not noise. It is the phenomenon itself.

Every other field that studies complex multi-attribute phenomena independently developed a construct for preserving this information — *dimensional decomposition*: the systematic separation of a complex signal into independent measurement channels.

| Domain | Decomposition Construct | Key Work |
|:---|:---|:---|
| Physics | Spectroscopy | Newton (1672), Fraunhofer (1814) |
| Psychology | Factor analysis | Thurstone (1947), Cattell (1966) |
| Economics | Multi-attribute utility | Lancaster (1966), Fishbein & Ajzen (1975) |
| Consumer research | Conjoint analysis | Green & Srinivasan (1978), Wilkie & Pessemier (1973) |
| Signal processing | Fourier decomposition | Fourier (1822) |
| Computational text analysis | Semantic Brand Score | Colladon (2018) |
| **Brand perception theory** | **???** | **Single-score metrics collapse dimensions** |

**Table 1a.** Dimensional decomposition across fields. Brand perception theory is the only major domain studying multi-attribute phenomena that lacks a formal decomposition framework preserving observer-level information.

The contribution of this paper is not the application of spectral methods to brands — it is the identification that brand perception measurement lacks dimensional decomposition, a construct every other field studying complex multi-attribute phenomena independently developed. The "spectral" label is descriptive: the eight dimensions are independent measurement channels, analogous to spectral bands in that each carries information the others cannot. The analogy names the construct; it does not claim that brands are literally like light.

This paper challenges the field's deeper assumption: that "the brand" is a coherent object that exists independently of who is observing it.

Spectral Brand Theory (SBT) proposes that there is no single brand perception that applies uniformly to all observers — each cohort assembles structurally different brand meaning from the same signal environment. The brand's signal architecture (what it emits and how) can be characterized at the brand level, while brand meaning exists only in observer-specific perception. What we call "the brand" is always already a collapse: a conviction in someone's mind, assembled from whichever signals they could perceive through their particular spectral profile. Different observers, perceiving the same signal environment through different spectral sensitivities, form structurally different brand convictions. These convictions are not errors or variations on a "true" brand — they are the only brands that exist.

The framework contributes to branding theory in three ways:

1. **Formal observer model.** SBT defines each observer cohort through a spectral profile: which dimensions they can perceive (spectrum), how they weight those dimensions (weights), how much inconsistency they accept (tolerances), what they already believe (priors), and whether they can recognize the brand at all (identity gate). This transforms "different people perceive differently" from a qualitative observation into a parameterized scoring function.

2. **Perception pipeline.** SBT models brand perception as a multi-stage pipeline: signal emission → observer filtering → probabilistic cloud formation → threshold-based conviction collapse → re-collapse on new evidence. Each stage is formally specified and computationally implementable. The pipeline explains not only what observers currently believe but how those beliefs will change under disruption.

3. **Computational implementability.** Unlike prior branding frameworks, SBT can be directly executed as software. Signals are typed data structures. Observers are parameter sets. Perception is clustering output. Conviction is a threshold function. The entire pipeline operates as a structured prompt sequence for large language models, making multi-cohort brand analysis accessible without custom engineering.

The remainder of this paper is organized as follows. Section 2 presents the theoretical framework, culminating in five formal propositions (Section 2.6) that specify the framework's testable structural predictions. Section 3 describes the demonstration methodology. Section 4 reports findings, focusing on four candidate mechanisms that emerged from the five-brand demonstration. Section 5 discusses implications, limitations, and future directions. Section 6 concludes.

---

## 2. Theoretical Framework

### 2.1 Epistemic Foundation: Brands as Perceptual Objects

SBT's core claim is epistemic: a brand is not an object with properties but a perceptual process with observers. The metaphor is astronomical. A constellation of stars appears different from every point in the universe and to every creature with a different range of spectral sensitivity. The constellation "itself" — all stars from no perspective — is a theoretical construct no one actually experiences. What exists are observer-specific perceptions of a shared signal field. (The stellar metaphor is useful for visualizing multi-dimensionality and observer sensitivity differences; it should be noted that in optics the spectrum is observer-independent, while in brand perception the observer's profile co-creates the perceived brand.)

Applied to brands: what a company designs and emits (logo, products, campaigns, pricing, culture) are signals. These signals exist across multiple perceptual dimensions. Each observer cohort filters these signals through its spectral profile, clusters the perceived signals into a probabilistic perception cloud, and — if sufficient evidence accumulates — collapses that cloud into a brand conviction. The conviction is observer-specific. The signal environment is shared. The brand, as commonly understood, is the observer's collapse product — not the company's intended identity.

This inversion has a philosophical precedent. Peirce's semiotics (1890s) established that meaning arises in the interpreter, not the sign. Barthes (1957) showed how cultural myths function as second-order semiotic systems that shape interpretation. Keller (1993) located brand equity in the customer's mind. SBT formalizes and extends these insights into a computational architecture.

### 2.2 Signal Architecture: Eight Perceptual Dimensions

SBT decomposes brand signals across eight dimensions, each representing a distinct channel through which observers perceive brand meaning:

| Dimension | Signal Type | Examples |
|:----------|:------------|:---------|
| **Semiotic** | Visual and sensory identity markers | Logo, name, colors, typography, packaging, sonic identity |
| **Narrative** | Story structures and temporal arcs | Origin story, founder myth, key events, brand legends |
| **Ideological** | Values, ethics, and purpose claims | Stated mission, ethical positions, political stance |
| **Experiential** | Direct encounter data | Product use, service quality, physical environment, UX |
| **Social** | Community and status signals | Tribal markers, brand communities (Muniz & O'Guinn, 2001), peer signaling, status display (Veblen, 1899), exclusivity |
| **Economic** | Price and value communication | Pricing strategy, discounting behavior, perceived value |
| **Cultural** | Aesthetic and zeitgeist positioning | Design language, cultural references, humor, taste codes |
| **Temporal** | Heritage and time-depth signals | History, heritage, generational continuity, era associations |

**Table 1.** The eight perceptual dimensions of brand signal architecture.

The eight dimensions emerged from a synthesis of prior frameworks. Kapferer's (2008) "physique" maps to the semiotic dimension; his "culture" maps to cultural and ideological; his "relationship" maps to experiential and social. Aaker's (1996) functional benefits map to experiential and economic; emotional benefits to social and cultural; self-expressive benefits to ideological and social. Holt's (2004) cultural branding theory maps to a combination of ideological and cultural dimensions, treating brands as cultural artifacts that derive meaning from their position in cultural discourse. De Chernatony & McDonald's (2003) brand management framework similarly addresses the multi-faceted nature of brand meaning but treats the facets as brand properties rather than observer-dependent perceptual channels. Floch's (1990) structural semiotics provides a complementary decomposition of the semiotic dimension, distinguishing practical, ludic, utopian, and critical valorizations that map to distinct sub-channels within SBT's semiotic-ideological space. Mick (1986) establishes the semiotic foundations for consumer research, demonstrating that brand signs operate through both denotative and connotative codes — a distinction SBT operationalizes through the designed/ambient signal classification. The temporal dimension — heritage and time-depth — appears in prior work as an attribute of specific brands but has not been modeled as a universal perceptual channel. Our exploratory analysis suggests it should be.

Each signal carries three properties:

- **Source type**: designed (created by the brand), ambient (generated by the environment — reviews, word-of-mouth transmission (Berger, 2013), competitor framing, cultural commentary), or synthetic (AI-generated content, LLM summaries, algorithmic recommendations).
- **Emission type**: positive (signal actively present), null (unintentional absence), or structural absence (designed restriction that functions as a signal — see Section 4.1).
- **Strength**: rated 0–5, reflecting intensity of emission.

The signal concept extends economic signaling theory (Spence, 1973) and its application to brand credibility (Erdem & Swait, 1998; Kirmani & Rao, 2000) from a unidimensional quality indicator to a multi-dimensional perceptual architecture. Connelly, Certo, Ireland, and Reutzel (2011) consolidate signaling theory across management disciplines — their review identifies signal observability, signal cost, and signal honesty as the three properties that determine signal effectiveness. SBT operationalizes all three: observability maps to the observer's spectral sensitivity (invisible dimensions produce no signal regardless of emission strength), cost maps to designed-versus-ambient classification, and honesty maps to the coherence between designed signals and the ambient signal field. Dawar and Parker (1994) demonstrate that signal reliance varies systematically across cultures and product categories — evidence that the observer's context shapes which signals carry information, precisely the mechanism SBT formalizes through cohort-specific weight profiles. In SBT, a brand emits not one signal but a structured field of typed signals across eight dimensions — and the observer, not the market, determines which signals are informative.

The ratio of designed to ambient signals — the **designed/ambient (D/A) ratio** — has emerged as one of the framework's most diagnostic metrics. A brand whose perception is predominantly shaped by ambient signals (D/A < 0.40) faces a structural problem that no communication strategy can solve: the brand's story is being written by others.

### 2.3 Observer Model: Spectral Profiles

The observer model is SBT's primary theoretical contribution. Each observer cohort is defined by a formal spectral profile:

- **Spectrum**: which of the eight dimensions the observer can perceive (some dimensions are invisible to some cohorts)
- **Weights**: how the observer prioritizes perceived dimensions (a numeric weight per dimension, summing to 1.0)
- **Tolerances**: how much inconsistency the observer accepts before a perception cloud destabilizes
- **Priors**: existing brand convictions stored in memory
- **Identity gate**: whether the observer can recognize the brand's signals as belonging to a single entity (analogous to facial recognition — without it, signals are noise)
- **Encounter mode**: direct (product use, store visit), mediated (screens, content, secondhand accounts), or mixed

The weight-based observer profile is structurally analogous to multi-attribute attitude models (Fishbein & Ajzen, 1975), extending the attribute-weighting mechanism from product evaluation to perceptual dimensions with the critical additions of tolerances, priors, and the identity gate. The concept of observer-specific dimensional weights has its methodological precedent in the INDSCAL model (Carroll & Chang, 1970), which demonstrated that individuals weight perceptual dimensions differently when evaluating stimuli — the same structural insight that SBT extends from laboratory stimuli to brand perception at the cohort level. The spectral profile determines not just *what* the observer sees but *how* they assemble what they see into meaning. Two observers exposed to identical signals will form different perception clouds if their weight profiles differ. This is not a failure of communication — it is the fundamental mechanism of brand perception.

**Formal observer model.** SBT defines each observer cohort through a spectral profile — a vector of dimensional weights, tolerances, priors, and gate states. Critically, cohorts are perceptual groupings, not demographic segments. Traditional segmentation variables — age, income, geography — are metadata: descriptive labels attached to the observer that may correlate with perceptual behavior but do not determine it. A cohort is a cluster in spectral-profile space: a group of observers whose profiles are similar enough that they form structurally similar perception clouds from the same signal environment. Two observers who share a demographic segment may belong to different SBT cohorts if their priors diverge — and two observers from entirely different demographics may share a cohort if their spectral profiles are similar. The distinction between a priori demographic segments and empirically discovered perceptual cohorts builds on the foundational segmentation methodology of Wedel and Kamakura (2000), who established latent class models as the standard for discovering unobservable consumer heterogeneity. Smith (1956) introduced market segmentation as a strategic construct; Yankelovich and Meer (2006) subsequently argued that segmentation has become a primarily demographic exercise that fails to predict behavior — precisely because demographic variables are metadata about the observer, not measurements of the observer's perceptual apparatus. SBT's cohort construct addresses Yankelovich and Meer's critique directly: cohorts are clusters in perception space, not in demographic space, and two observers who share every demographic attribute may belong to different cohorts if their spectral profiles diverge. The clustering is a structural property of the observer population, not an analyst's modelling choice.

Cohort membership is dynamic. Because priors are a profile component and priors evolve through signal accumulation, decay, and crystallization (see Section 5.4, Temporal dynamics), an observer's position in spectral-profile space shifts over time. Differential signal exposure — arising from encounter mode, geography, media consumption, and social networks — causes observers who once shared a cohort to drift apart as their priors diverge. Signal events (a CEO controversy, a product failure, a viral campaign) do not merely change perception — they physically redistribute observers across cohort boundaries. This dynamism distinguishes SBT cohorts from traditional market segments: segments describe who the observer *is*; cohorts describe how the observer *perceives*, and perception changes.

\newpage

**Figure 1. The Observer-Mediated Perception Pipeline**

```
  SIGNAL ENVIRONMENT         OBSERVER PROFILE
  +------------------+       +------------------+
  | Brand Signals    |--+    | Identity Gate    |
  | (8 dimensions)   |  +--->| (recognition)    |
  |                  |  |    |                  |
  | Ambient Signals  |--+    | Spectral Filter  |
  | (reviews, news,  |       | (weights, toler- |
  |  culture)        |       |  ances, priors)  |
  +------------------+       +--------+---------+
                                      |
                                      v
                              PERCEPTION CLOUD
                              (probabilistic
                               +/- /ambivalent)
                                      |
                              threshold reached
                                      |
                                      v
                               CONVICTION
                              (stable belief)
                                      |
                              re-collapse on
                               new evidence
                                      |
                                      v
                              [back to cloud]
```

**Figure 2. Observer Heterogeneity: Same Signal Field, Different Perceptions**

```
                    Tesla Signal Environment
                    (Same 8-dimensional signals)
                           /            \
                          /              \
            Tech Loyalist                  Progressive Boycotter
  Experiential: 0.35                       Ideological: 0.45
  Economic:     0.20                       Social:      0.20
  Ideological:  0.10                       Experiential: 0.03
  Tolerance:    High                       Tolerance:    Zero
            |                                        |
            v                                        v
     Positive Cloud                           Negative Cloud
    (Product-anchored)                      (Ideology-anchored)
     Confidence: 0.78                        Confidence: 0.82
            |                                        |
            v                                        v
  "Best EV on the market"              "CEO's political vehicle"
```

### 2.4 Cloud Formation and Conviction Collapse

The terminology — cloud, collapse — deliberately invokes quantum mechanical metaphor. A perception cloud is indeterminate; a conviction is a collapsed state. As in quantum measurement, the collapse is observer-dependent: different observers collapse the same signal environment into different convictions. The metaphor is structural, not mathematical — brand perception does not obey quantum mechanics, but it shares the epistemic property that observation determines outcome.

Brand perception follows a three-stage epistemic pipeline:

**Stage 1: Cloud formation.** Perceived signals cluster in the observer's mind, weighted by the observer's spectral profile. The resulting cluster is a *perception cloud* — a probabilistic, pre-conviction impression. Clouds have valence (positive, negative, or ambivalent) and confidence (weak, moderate, or strong). The clustering mechanism draws on two established findings in consumer cognition: Alba and Hutchinson (1987) demonstrate that expertise and familiarity independently shape how consumers organize product knowledge — expertise determines the dimensions available for encoding (analogous to spectral sensitivity), while familiarity determines the density of stored associations (analogous to cloud confidence). Zajonc (1980) establishes that affective responses can precede cognitive evaluation — cloud valence can form before the observer has consciously processed the dimensional content, particularly for semiotic and experiential signals that activate rapid affective encoding. Critically, clouds can form through direct encounter (experiential signals dominate) or through mediated channels (ideological, social, and narrative signals dominate, experiential signals absent). Mediated clouds tend toward lower confidence but can exhibit higher stability when no experiential data introduces ambiguity (see Section 4.3).

**Stage 2: Conviction collapse.** When a cloud accumulates sufficient evidence — when enough signals align across enough dimensions with enough consistency — it collapses into a brand conviction. The conviction is a stable belief: "Tesla is X" or "Hermès means Y." The collapse threshold varies by observer: high-tolerance observers require less evidence; low-tolerance observers demand more.

**Stage 3: Re-collapse.** New evidence (a product failure, a CEO scandal, a brilliant campaign) introduces signals that contradict the existing conviction. If the contradicting evidence is strong enough, the conviction dissolves and the observer re-forms a cloud from the available evidence — the signals that have survived temporal decay plus crystallized priors, now including the new contradicting signals. The conviction is rebuilt from this evidence, never patched. This explains both brand resilience (convictions resist moderate contradicting evidence) and brand crises (sufficient contradicting evidence forces wholesale re-evaluation).

The re-collapse mechanism is adapted from an epistemological architecture developed for financial document processing (Zharnikov, 2026b), where probabilistic facts about financial transactions are rebuilt from scratch whenever new evidence arrives, rather than incrementally updated. The epistemic architecture is structurally analogous — observations → hypotheses → knowledge — but the domain transfer introduces two critical differences: brand "observations" are filtered through heterogeneous observer profiles rather than a single system, and brand signals decay over time (see Section 5.4), making the available evidence at re-collapse a function of temporal dynamics rather than a complete historical record.

### 2.5 Coherence as Structural Property

A brand's coherence is not the consistency of its messaging but the structural relationship between its observer cohorts' perception clouds. SBT defines coherence as the degree to which different observers' convictions are compatible — not identical, but compatible. This distinction is crucial: a brand where all observers perceive the same thing (signal coherence) and a brand where observers perceive different things that reinforce each other (ecosystem coherence) both exhibit high coherence, but their structural properties diverge dramatically (see Section 4.2).

Coherence is measured through a seven-metric scorecard:

| Metric | What It Measures |
|:-------|:-----------------|
| Dimensional coverage | How many dimensions the brand actively emits on |
| Gate permeability | What proportion of target observers recognize the brand |
| Cloud coherence | Compatibility of perception clouds across cohorts |
| Collapse strength | Confidence level of resulting convictions |
| Re-collapse resistance | Stability of convictions under disruption |
| Emission efficiency | Signal-to-noise ratio of designed signals |
| Designed/ambient ratio | Brand's control over its own signal environment |

**Table 2.** The seven-metric spectral scorecard.

### 2.6 Formal Propositions

The theoretical framework developed in Sections 2.1–2.5 generates five formal propositions that specify testable structural predictions. Each proposition formalizes an argument that the framework makes implicitly; stating them explicitly establishes the empirical commitments that distinguish SBT from a descriptive vocabulary.

**Proposition 1 (Observer heterogeneity).** *Different observer cohorts, exposed to identical brand signal environments, will form systematically different brand convictions as a function of their spectral profile differences (weights, tolerances, priors, encounter mode).*

Keller (1993) locates brand equity in the customer's mind — the most important precedent for SBT's observer-dependent approach. The structural limitation of Keller's model is that it treats "the customer" as a single model: one set of brand associations, one equity structure. Keller acknowledged individual variation but did not parameterize it. SBT formalizes the heterogeneity that Keller's framework recognized but could not model, specifying the observer's spectral profile as the mechanism through which identical signals produce different convictions. Empirical evidence for observer-dependent brand perception already exists in the advertising literature. Grier and Brumbaugh (1999) demonstrated that identical advertisements produce systematically different meanings in target versus non-target cultural groups. Puntoni, Vanhamme, and Ruber (2011) documented "purposeful polysemy" — the deliberate design of messages that activate different meanings in different audiences — providing direct evidence that what SBT formalizes as spectral metamerism is an observed phenomenon in marketing practice. Testable prediction: measuring brand conviction across cohorts with documented spectral profile differences will reveal systematic, profile-predictable divergence rather than random variation.

**Proposition 2 (Non-ergodicity of perception).** *The temporal sequence in which brand signals are encountered affects the resulting brand conviction, even when the set of signals is identical.*

Peters (2019) demonstrates that in multiplicative, path-dependent processes, the order of events matters — ensemble averages diverge from time averages. Brand perception is structurally analogous: signals compound multiplicatively through priors rather than summing additively into a running total. An observer who encounters a product failure before a brand's origin story forms a different conviction than one who encounters the same two signals in reverse order, because the first signal establishes a prior that filters interpretation of the second. In consumer psychology, Hogarth and Einhorn (1992) provided the formal precedent for order-dependent belief updating: their Belief-Adjustment Model demonstrates that step-by-step evaluation produces different outcomes from end-of-sequence evaluation, and that negative evidence has asymmetric updating power relative to positive evidence — a mechanism that SBT formalizes as conviction asymmetry. The structural limitation of cross-sectional brand measurement is that it captures ensemble averages — snapshots across many observers at one moment — which systematically misrepresent individual cohort trajectories. Testable prediction: presenting the same signal set in different temporal orders to matched cohorts will produce measurably different conviction outcomes.

**Proposition 3 (Structural absence as signal).** *Designed restriction of signal emission in specific dimensions generates perceived value that cannot be replicated by signal addition in other dimensions.*

Veblen (1899) identified conspicuous consumption as a value-signaling mechanism; structural absence inverts this into conspicuous restriction. Commodity theory (Brock, 1968) and the scarcity principle (Cialdini, 2001) establish that scarcity enhances perceived value, but they treat scarcity as a unidimensional modifier. The structural limitation is that these accounts do not specify the cross-dimensional generation mechanism: restriction on one dimension (economic, experiential, social) produces a signal on a different dimension. The Hermes analysis in Section 4.1 demonstrates that the brand's A+ coherence grade derives not from what it emits but from what it withholds. Testable prediction: comparing perceived value of brands with designed dimensional restriction against brands with equivalent positive signal strength will reveal a value premium attributable to restriction that cannot be replicated through addition.

**Proposition 4 (Coherence type over coherence score).** *Brands with identical aggregate coherence scores exhibit different resilience properties depending on their coherence type (ecosystem, signal, identity, experiential asymmetry, incoherent).*

Traditional brand scorecards project multi-dimensional coherence onto a single scale — a form of spectral metamerism (Zharnikov, 2026e) where structurally different brands appear identical in lower-dimensional projection. The five-brand demonstration in Section 4.2 reveals that coherence is not a continuum from low to high but a nominal classification with qualitatively distinct resilience mechanisms. Two brands scoring 7/10 on a conventional coherence metric may exhibit radically different responses to disruption: selective absorption (ecosystem) versus uniform transmission (signal). The structural limitation of single-score coherence metrics is that they are geometrically blind to this distinction. Testable prediction: grouping brands by coherence type and subjecting them to matched disruption events will reveal type-specific resilience patterns that aggregate coherence scores fail to predict.

**Proposition 5 (Conviction asymmetry).** *Evidence-free negative brand convictions are more resistant to disconfirmation than evidence-rich positive convictions.*

Kahneman & Tversky (1979) established that losses loom larger than equivalent gains in prospect theory. SBT extends this asymmetry to brand evidence: negative convictions formed without experiential data are structurally more stable than positive convictions formed with extensive experiential data, because the negative-conviction holder's spectral profile excludes the dimensions where disconfirming evidence would need to arrive. The experiential gate is effectively closed. The structural limitation of brand management strategies that attempt to "convert" hostile cohorts is that they target dimensions the cohort cannot perceive. Testable prediction: measuring the evidence required to shift convictions from positive-to-negative versus negative-to-positive will reveal a directional asymmetry, with negative-to-positive requiring substantially more — and dimensionally different — evidence.

These five propositions are not exhaustive predictions of SBT; they formalize the framework's most distinctive structural claims. The falsifiable hypotheses in Section 5.5 operationalize these and additional predictions into specific experimental designs.

---

## 3. Demonstration Methodology

### 3.1 Design

We demonstrated SBT through structured analysis of five brands selected to span the brand architecture space:

| Brand | Selection Rationale | Architecture Type |
|:------|:----------------------------------|:------------------|
| Patagonia | Mission-driven, ideological core, moderate scale | Identity coherence |
| Tesla | Maximum observer divergence, CEO-dominated signals | Incoherence |
| IKEA | Global consistency, designed-signal dominance | Signal coherence |
| Hermès | Scarcity-based luxury, structural absence strategy | Ecosystem coherence |
| Erewhon | Hyperlocal niche, mediated perception dominance | Experiential asymmetry |

**Table 3.** Five case-study brands and selection rationale (exploratory demonstration).

The five brands were chosen to stress-test different properties of the framework: Patagonia tests ideological filtering; Tesla tests extreme observer divergence and ambient signal dominance; IKEA tests consistent signal architecture at global scale; Hermès tests scarcity-based value creation and cross-cohort interdependence; Erewhon tests the framework's minimum viable scale and mediated perception dynamics.

### 3.2 Analytical Pipeline

Each brand was analyzed through six sequential modules, each producing structured YAML output that feeds into subsequent modules:

1. **Brand Decomposition**: inventory of signals across all eight dimensions, source type classification, emission type classification, dimensional heat map
2. **Observer Mapping**: 3–5 observer cohort spectral profiles with weights, tolerances, encounter modes, and cross-cohort dependencies
3. **Cloud Prediction**: per-cohort perception clouds with confidence bands, valence, formation mode, and inter-cohort divergence mapping
4. **Coherence Audit**: seven-metric scorecard, overall grade (A+ through F), coherence type classification
5. **Emission Strategy**: target conviction map, dimensional redesign, D/A ratio optimization, phased action plan
6. **Re-collapse Simulation**: 2–3 disruption scenarios per brand, per-cohort resilience scoring, cascade risk assessment, defensive recommendations

The pipeline was executed using Claude Opus 4.6 (Anthropic) as the primary analytical engine, with structured prompts and YAML output templates ensuring consistency across brands. A full cross-model replication was subsequently conducted using Gemini 3.1 Pro (Google) across all five brands to test for model-specific biases (see Section 3.4). Each module's output was assessed against four validation criteria: non-obvious (a brand strategist could not reach this through standard analysis), dimensionally specific (references specific dimensions and observer profiles), actionable (suggests concrete strategic changes), and observer-differentiated (shows how different cohorts perceive the same signals differently).

### 3.3 Insight Validation Protocol

Each brand analysis was followed by a structured insight assessment that evaluated the top findings against the four criteria. An insight was counted as validated only if it satisfied all four criteria simultaneously. Across five brands, 25 insights were assessed by the framework's author against four criteria; all 25 were judged to satisfy the criteria. Independent blind evaluation by practitioners not familiar with the framework would provide a stronger test. The four mechanisms reported in Section 4 were selected as the most novel — insights that could not have been produced by any existing brand framework because the existing frameworks lack the necessary vocabulary.

### 3.4 Limitations of the Demonstration Approach

The demonstration has several methodological limitations that must be acknowledged.

First, observer weight assignments are expert estimates informed by behavioral inference, not empirically measured through surveys or experiments. The weights are most defensible for polarized brands (Tesla), where stated purchase behavior makes dimensional priorities visible, and least defensible for inaccessible cohorts (Hermès heritage collectors). Future work should validate weight assignments through conjoint analysis or behavioral experiments.

Second, cloud confidence scores are calibrated within each brand analysis but not across brands. A confidence of 0.85 in the Tesla analysis is not directly comparable to 0.85 in the Hermès analysis. We recommend using confidence bands (weak / moderate / strong) rather than cross-brand decimal comparison.

Third, the analytical pipeline was initially executed by a single LLM (Claude Opus 4.6), introducing potential model-specific biases. A full cross-model replication was conducted using Gemini 3.1 Pro (Google) across all five brands. Both models independently produced identical coherence type classifications and identical letter grades for every brand in the sample:

| Brand | Claude Opus 4.6 | Gemini 3.1 Pro | Convergence |
|:------|:----------------|:----------------|:------------|
| Tesla | Incoherent, C- | Incoherent, C- | Identical |
| Hermès | Ecosystem, A+ | Ecosystem, A+ | Identical |
| Patagonia | Identity, B+ | Identity, B+ | Identical |
| IKEA | Signal, A- | Signal, A- | Identical |
| Erewhon | Exp. Asymmetry, B- | Exp. Asymmetry, B- | Identical |

**Table 7.** Cross-model replication convergence: coherence type and grade.

Both models independently derived the structural absence mechanism for Hermès without it being named in the prompt templates, and both independently identified the CEO ambient signal domination as Tesla's core architectural failure. Model-sensitive findings were limited to two dimensions: cohort granularity (Claude consistently identified 5-6 cohorts per brand; Gemini consistently identified 3, aggregating into broader strategic segments) and D/A ratio variance (within 10-15 percentage points, with Gemini attributing slightly more to designed signals). The replication also revealed complementary operational biases. Claude Opus 4.6 generates finer cohort fragmentation, isolating edge-case observer profiles (e.g., separating "Heritage Client" from "Cultural Connoisseur"). Gemini 3.1 Pro produces parsimonious macro-segments suited to strategic planning. Claude's outputs emphasize paradoxes and internal tensions; Gemini's are more clinically operational. Neither model exhibited grade inflation across any of the five brands. These biases are complementary rather than contradictory: the structural diagnosis remains stable regardless of cohort resolution, confirming that the framework — not the model — drives the analytical conclusions. Replication with additional models and by human analysts would further strengthen the validation. Additionally, both models were trained on substantial corpora of brand-related text for these five well-documented brands; convergence may reflect shared training data as well as framework validity. Testing the framework on brands with minimal public information would provide a stronger test of the analytical pipeline.

Fourth, all five brands are well-known entities with extensive public information. The framework's performance on obscure or newly launched brands — where signal inventories are sparse — remains untested.

Fifth, the validation uses the framework's own analytical pipeline to produce the findings that validate the framework. While the four validation criteria (non-obvious, dimensionally specific, actionable, observer-differentiated) impose external constraints on what counts as a validated insight, the framework shapes which phenomena become visible. Independent validation — comparing SBT-generated findings against independently collected consumer survey data or established brand tracking metrics — would provide a stronger test of the framework's explanatory value.

Sixth, the eight dimensions are presented as a working decomposition synthesized from prior frameworks (Section 2.2), not as a proven exhaustive set. Other decompositions are possible — a standalone environmental/sustainability dimension, or a functional/utilitarian dimension, might capture signal channels that the current eight subsume rather than exclude. The claim is that the eight dimensions are sufficient to demonstrate the framework's analytical architecture, not that they are the only valid decomposition. Empirical factor-analytic work on brand perception data would be needed to establish the dimensionality of the perceptual space.

Seventh, the framework treats dimensional weights as independent parameters within each observer's spectral profile. In practice, perceptual dimensions may be correlated — an observer who weights ideological signals heavily may systematically discount economic signals. The independence assumption simplifies the model but may miss interaction effects that shape cloud formation.

Eighth, all five case-study brands are Western-origin, consumer-facing brands analyzed in English. The framework's applicability to non-Western brands (where cultural dimension weights may differ substantially), B2B contexts (where committee-based evaluation and longer decision cycles change cloud formation dynamics), or non-English perception contexts remains untested. The eight dimensions are hypothesized to be universal perceptual channels, but their relative salience is likely culturally variable.

### 3.5 Mathematical Foundations

The framework as presented in Sections 1–3 operates at the level of structured qualitative analysis: dimensions are named, observer profiles are specified, and the analytical pipeline produces assessable insights. A natural question is whether the framework's core constructs — eight-dimensional brand space, observer spectral profiles, perception clouds — admit formal mathematical treatment. A series of eight companion papers (Zharnikov, 2026c–g, 2026j, 2026h, 2026k) establishes that they do.

The research program began with a critical survey of geometric approaches to brand perception (Zharnikov, 2026c), which identified a gap: no existing framework combines high-dimensional geometry, generative signal models, observer heterogeneity, and non-ergodic dynamics. The six subsequent papers address specific mathematical problems within SBT's architecture:

- **Formal metric** (Zharnikov, 2026d): defines a Riemannian metric on the eight-dimensional brand space that respects the structure of observer spectral profiles, enabling rigorous measurement of distances and angles between brand positions.

- **Spectral metamerism** (Zharnikov, 2026e): proves that dimensionality reduction from the full eight-dimensional space to lower-dimensional projections (as traditional frameworks implicitly perform) incurs bounded but unavoidable information loss — two brands that appear identical in a three-dimensional projection can be arbitrarily different in the full space.

- **Cohort boundaries** (Zharnikov, 2026f): applies concentration of measure results to show that observer cohort boundaries in high-dimensional perception space are inherently fuzzy — sharp demographic segmentation is geometrically impossible when perception operates in eight or more dimensions.

- **Sphere packing** (Zharnikov, 2026g): derives upper bounds on the number of distinguishable brand positions a market can sustain, connecting the eight-dimensional structure to classical sphere packing results and the exceptional properties of the E₈ lattice.

- **Non-ergodic dynamics** (Zharnikov, 2026j): models brand perception as a stochastic diffusion process on the perceptual manifold, formalizing the multiplicative, path-dependent nature of conviction formation and proving that ensemble averages (cross-sectional surveys) systematically misrepresent individual cohort trajectories.

- **Specification impossibility** (Zharnikov, 2026h): proves a fundamental limit on organizational specification completeness — no finite specification can fully determine behavior in high-dimensional operational space, providing the mathematical foundation for the companion Organizational Schema Theory (Zharnikov, 2026i), which identifies acceptance testing as a missing construct in organizational design.

- **Resource allocation** (Zharnikov, 2026k): derives optimal dimensional investment prescriptions from measured cohort weight profiles and introduces the alignment gap metric, which quantifies the economic loss when founders allocate resources based on their own perceptual weights rather than their target customers'.

These results transform the framework's constructs from analytical metaphors into mathematically grounded objects with provable properties. The companion papers are self-contained and do not require reading the present paper, though they build on its conceptual vocabulary. All are available as working papers on Zenodo.^[The complete research program comprises 20+ papers available as a collection at the Zenodo community page: zenodo.org/communities/spectral-branding.]

---

## 4. Findings

The five-brand structured analysis identified nine candidate mechanisms. We report four in depth — selected as the most theoretically significant contributions that are difficult to produce through existing brand frameworks.

### 4.1 Structural Absence: Value Creation Through Designed Signal Restriction

**Discovery context:** Hermès case study (Modules 1, 5).

Every brand framework in the literature assumes an emission model: design a signal, emit it, and measure whether it produces the desired perception. More signal generally means more perception. Broader distribution generally means broader awareness. The logic is additive.

Hermès inverts this logic entirely. The brand does almost nothing that brand strategy textbooks recommend. It does not advertise aggressively. It does not maximize reach. It does not hold sales. It does not sell its most iconic products online. It maintains wait lists measured in years. It operates approximately 300 stores worldwide.

By every standard metric of brand communication, Hermès should be weak. It scored A+ in our coherence audit — the highest grade in the study. Not despite the restrictions. Because of them.

We formalize this as **structural absence**: the deliberate withholding of signals that creates value through what is not emitted. The concept has precedent in semiotics — Eco (1976) analyzed how sign systems communicate through absence and overcoding — but has not been formalized as a brand strategy mechanism. The mechanism is analogous to dark matter in physics — invisible but gravitationally active, shaping the perception field without emitting observable signals.

SBT introduces a three-type emission taxonomy:

| Emission Type | Mechanism | Signal Present? | Example |
|:-------------|:-------------------------------|:----------------|:-------------------------------|
| Positive | Brand actively emits signal | Yes | Product launch, campaign |
| Null | Signal absent, unintentional | No (neglect) | Unused heritage, dormant dimension |
| Structural absence | Designed restriction functions as signal | No (strategy) | Wait list, no discounts, geographic scarcity |

**Table 4.** Three emission types in the spectral model.

The key mechanism is cross-dimensional: restriction on one dimension generates a signal on a different dimension. Economic restriction (never discounting) produces a social signal — the product exists outside normal market forces, inverting Veblen's (1899) conspicuous consumption from display of spending to display of access. Experiential restriction (in-store purchase only) produces an economic signal (difficulty of access justifies the price). Social restriction (purchase rituals, relationship requirements) produces an experiential signal (the restriction process *is* the brand experience).

We model cloud formation with structural absence as:

> Conceptually, structural absence amplifies the perceived weight of present signals through contrast — a multiplicative mechanism in perception rather than an additive formula. (Formalizing this as a computable parameter is on the research agenda; the formula is a schematic representation, not a computation.)

The contrast effect amplifies the perceived weight of signals that exist in the context of signals that are withheld. Hermès achieves the highest emission efficiency in the study (9/10) not by optimizing what it sends but by optimizing what it withholds — the signal-to-noise ratio approaches its maximum because noise has been structurally excluded.

**Dimensional constraints.** Structural absence does not operate on all dimensions. It operates primarily on social (exclusivity), economic (pricing discipline), and experiential (geographic scarcity) dimensions. It cannot operate on semiotic (there is no "absent logo" — visual identity requires presence) or narrative (the absence of a story is just absence — Hermès in fact has a rich narrative that *frames* the absence). This constraint is consistent with the finding that structural absence requires existing demand to restrict. The strategy is available only to brands with sufficient heritage and established desire to make the restriction legible as intention rather than failure.

**Prerequisite.** Our cross-brand comparison reveals that structural absence requires heritage legitimization. Hermès' 189 years of continuous operation makes its restrictions legible as "this is how we have always been" rather than "this is artificial scarcity." Brands without heritage depth cannot deploy structural absence at scale — the restriction is interpreted as arrogance, not tradition.

### 4.2 Five Types of Brand Coherence

**Discovery context:** Cross-brand comparison (Module 4 across all five brands).

Traditional brand analysis treats coherence as a single variable from low to high: how consistently is the brand perceived across audiences? Our five-brand exploratory analysis suggests that coherence is not a single variable but a structural property that comes in five qualitatively distinct types, each with different resilience profiles.

| Coherence Type | Grade | Pattern | Resilience Profile | Brand |
|:--------------|:------|:--------------------------------------|:--------------------------------------|:------|
| Ecosystem | A+ | Different clouds reinforce through functional interdependence | Selective — absorbs disruption by purification | Hermès |
| Signal | A- | Consistent designed signals → consistent clouds | Uniform — transmits disruption evenly | IKEA |
| Identity | B+ | Ideological core filters cohort compatibility | Binary — divides along ideology | Patagonia |
| Experiential asymmetry | B- | Evidence gap between direct and mediated observers | Geographic — different impact by location | Erewhon |
| Incoherent | C- | Contradictory signals → irreconcilable clouds | Amplifying — widens existing cracks | Tesla |

**Table 5.** Five-type coherence taxonomy with resilience profiles.

(The letter grades reported here are L2 rendered outputs — human-readable projections of the multi-dimensional spectral profile onto a disruption resilience scale. The underlying coherence classification is nominal (structural type); the grade projects the typical resilience mechanism of each type for practitioner reference. Different spectral profiles can project to the same grade (spectral metamerism); the full L1 spectral profiles are reported in Section 3.3.)

**Figure 3. Spectral Metamerism: Different L1 Structures, Same L2 Grade**

```
  L1: Brand A                                    L1: Brand B
  +---------------------------+                  +---------------------------+
  | Ecosystem coherence       |                  | Signal coherence          |
  | Cross-cohort              |                  | Uniform signal            |
  | interdependence           |                  | distribution              |
  | Selective resilience      |                  | Uniform resilience        |
  +---------------------------+                  +---------------------------+
             \                                              /
              \--- resilience projection ---> L2 Grade <---/
                                              [ 7 / 10 ]
```

The practical consequence is that traditional scorecards are structurally blind to the distinction. A brand with 7/10 signal coherence (the IKEA pattern: everyone perceives the same thing) and a brand with 7/10 ecosystem coherence (the Hermès pattern: different cohorts perceive different things that reinforce each other) would appear identical on any single-variable dashboard. Their responses to disruption are radically different. Empirical support for the claim that coherence type predicts resilience better than coherence degree comes from organizational culture research. Sorensen (2002) demonstrated across more than 200 firms that strong cultures outperform in stable environments but underperform in volatile ones — establishing that the structure of alignment, not its intensity, determines outcomes. Chatman, Caldwell, O'Reilly, and Doerr (2014) extended this by showing that consensus combined with adaptability outperforms consensus alone.

**Ecosystem coherence** (Hermès) exhibits selective resilience. When the Hermès secondary market collapses in our simulation, the Investment Buyer cohort is destroyed — but the Heritage Client and Cultural Connoisseur are *strengthened*: "now the speculators are gone." The ecosystem metabolizes the disruption by sacrificing peripheral elements while purifying the core. This capacity for selective absorption is unique to ecosystem coherence and explains the extraordinary durability of brands that exhibit it.

**Signal coherence** (IKEA) exhibits uniform resilience. When disrupted, the impact transmits evenly across all cohorts because the same designed signals reach everyone. There is no selective absorption — a quality scandal affects every observer equally. Recovery requires system-wide signal correction, not targeted cohort management.

**Identity coherence** (Patagonia) exhibits binary resilience. The brand divides along ideological lines under stress. Aligned cohorts rally ("this proves they are authentic"). Misaligned cohorts deepen their indifference or opposition. The ideological core is either a magnet or a wall — there is no middle ground.

**Experiential asymmetry** (Erewhon) exhibits geographic resilience. Disruption affects local and mediated observers differently because their perception clouds are built on incompatible evidence bases. A food safety incident at the physical store devastates direct-experience observers but barely registers with the Instagram audience. A social media backlash against wellness culture devastates the mediated observers but leaves local regulars unaffected.

**Incoherence** (Tesla) exhibits amplifying fragility. Each disruption widens existing cracks. The system does not absorb disruption — it converts disruption into deeper division. This is the worst resilience profile in the taxonomy.

\newpage

The coherence type is determined by three structural properties: (1) cohort interdependence — how much one cohort's perception depends on another's behavior; (2) ideological centrality — how much coherence depends on a shared ideological commitment; and (3) encounter mode variance — how different the direct-encounter brand is from the mediated brand.

**Figure 4. Coherence Types: Disruption Response Patterns**

```
                         DISRUPTION
                    /    /     |     \      \
                   v    v      v      v      v
              Eco-   Signal Identity Exp.  Incoher.
              system (IKEA) (Patag.) Asym. (Tesla)
              (Herm.)              (Erew.)
                |      |      |      |      |
                v      v      v      v      v
             Select. Uniform Binary Geogr. Amplif.
             absorb. transm. split  split  fragil.
```

### 4.3 Asymmetric Conviction Resilience

**Discovery context:** Tesla case study (Modules 2, 3, 6).

Our analysis of Tesla revealed a counterintuitive structural property of brand perception: evidence-free negative convictions can be more stable than evidence-rich positive ones.

The Tesla Progressive Boycotter cohort holds a brand conviction with 0.82 confidence (classified as "strong"). This conviction is constructed from an ideological weight of 0.45 and a social weight of 0.20 — but an experiential weight of only 0.03. The Boycotter has never driven a Tesla, never visited a showroom, never used a Supercharger. Their entire brand perception is constructed from ambient ideological and social signals encountered through screens.

The Tesla Tech Loyalist, who drives the car daily and has extensive product data, holds a conviction with 0.78 confidence — lower than the Boycotter's.

The person with the most evidence has less certainty than the person with the least.

This is not a cognitive error. It is a structural property of spectral perception. The Boycotter's conviction is uncontested because there is no experiential data to create cognitive dissonance (Festinger, 1957). The ideological signal points in one direction. The social signal confirms it. No product encounter introduces nuance. The conviction is coherent *because* it is evidence-free.

The Loyalist, by contrast, has real product data. They know the car is excellent. They also know the service centers can be frustrating. They have experienced the gap between Autopilot promises and delivery. Their conviction includes contradictions — the somatic markers of mixed emotional experience (Damasio, 1994) create ambivalence that pure ideological conviction never encounters. Evidence-rich convictions are inherently less certain than evidence-free ones because they contain more dimensions that can produce ambiguity.

This asymmetry has a critical resilience implication. In our disruption simulations, negative convictions consistently *strengthen* under brand stress, while positive convictions *weaken*. A brand crisis confirms what the negative-conviction holder already believed. But it introduces contradicting evidence for the positive-conviction holder, who must now reconcile their favorable experience with unfavorable news. The asymmetry is directional: positive → negative is far easier than negative → positive, because the latter requires experiential evidence that the negative-conviction holder's spectral profile is designed to exclude.

The strategic implication is stark: resources spent attempting to convert structurally locked negative cohorts are wasted. The Boycotter's experiential gate is effectively closed (0.03 weight). No test drive campaign will reach them because they are not evaluating the product — they are evaluating the ideology. Brands with locked negative cohorts must accept the structural constraint and invest in addressable cohorts instead.

**Figure 5. Asymmetric Conviction Resilience** (Tesla case)

| | Tech Loyalist | Progressive Boycotter |
|:--|:--|:--|
| **Top weights** | Experiential: 0.35, Economic: 0.20 | Ideological: 0.45, Social: 0.20 |
| **Experiential** | 0.15 (extensive product data) | 0.03 (no product contact) |
| **Confidence** | 0.78 (mixed signals = ambivalence) | 0.82 (no contradiction = certainty) |
| **Crisis effect** | Weakens (new evidence conflicts) | Strengthens (confirms prior belief) |

### 4.4 Brand Power and Brand Health as Independent Variables

**Discovery context:** Cross-brand comparison (Module 4 across all five brands).

The five-brand exploratory analysis produces a finding that inverts conventional brand wisdom: brand power (emission strength, awareness, cultural impact) and brand health (coherence, architectural integrity, resilience) are independent variables. A brand can maximize the first while minimizing the second.

\newpage

| Brand | Power | Health | D/A | Gap |
|:----------|:------------------------------|:----------|:------|:------------------------|
| Tesla | Highest (universal awareness) | C- | 30/65 | Maximum inversion |
| Hermès | Moderate (niche, restricted) | A+ | 60/35 | Architecture > awareness |
| IKEA | High (global, ubiquitous) | A- | 75/25 | Consistent alignment |
| Patagonia | Moderate (category-bound) | B+ | 65/30 | Ideological filter |
| Erewhon | Low-moderate (hyperlocal) | B- | 40/55 | Scale floor |

**Table 6.** Five-brand scorecard: brand power versus spectral health.

Traditional frameworks — BrandAsset Valuator (BAV), Interbrand's brand strength methodology, Keller's brand equity pyramid — measure dimensions of power: differentiation, relevance, esteem, knowledge, awareness, consideration. By these metrics, Tesla is among the world's most valuable brands. Seven of eight dimensions emit at strength 4 or higher. Gate permeability is 10/10 — everyone knows the brand.

But the spectral scorecard reveals Tesla's cloud coherence at 2/10, its designed/ambient ratio at 30/65, and its re-collapse resistance at 4/10. Maximum emission power, minimum architectural health.

The confusion between brand power and brand health is, we argue, the central error in traditional brand management. It leads to the systematic misdiagnosis of brands like Tesla (perceived as "strong" when structurally fragile) and the systematic undervaluation of brands like Hermès (perceived as "niche" when architecturally impregnable).

The D/A ratio is the single metric that most powerfully discriminates between power and health. Our five-brand comparison tentatively suggests a possible optimal zone around 55–65% designed signals; this is an exploratory hypothesis requiring validation across a larger sample. High enough to maintain narrative control. Low enough to allow authentic ambient reinforcement. Tesla, at 30% designed, is 25 points below the floor of this zone — meaning no communication strategy can fix its brand problem because 65% of the signal environment is beyond its control. Hermès, at 60% designed with *aligned* ambient signals, demonstrates that the direction of ambient signals matters as much as the ratio: its ambient signals amplify rather than contradict its designed signals.

\newpage

**Figure 6. D/A Ratio and Coherence Across Five Brands**

```
Coherence
  10 |                                        * Hermès (60/35, A+)
     |                              * IKEA (75/25, A-)
   8 |                                  :
     |                                  :  ← Optimal zone
   6 |                                  :    (55-65% designed)
     |       * Patagonia (65/30, B+) ...:
   4 |                    * Erewhon (40/55, B-)
     |                         ↑
   2 |              * Tesla (30/65, C-)
     |                   ↑
   0 +----+----+----+----+----+----+----+----+----+----
     0   10   20   30   40   50   60   70   80   90  100
                    Designed/Ambient Ratio (% designed)

     Tesla: max power, min health      Hermès: mod power, max health
     ← Under-designed zone →|← Optimal →|← Over-designed zone →
                            55          65
```

---

## 5. Discussion

### 5.1 Relationship to Existing Frameworks

SBT does not replace existing brand frameworks. It explains why each of them works partially and where each breaks down.

Aaker's (1996) brand identity system describes the signal side of the equation — what the brand intends to emit — but lacks the observer model that explains why the same identity produces different perceptions in different cohorts. Kapferer's (2008) prism comes closest to SBT's dimensional approach, with its six facets mapping loosely to SBT's eight dimensions, but treats the facets as properties of the brand rather than perceptual channels through which observers filter signals. Schmitt's (1999) experiential marketing modules (SENSE, FEEL, THINK, ACT, RELATE) decompose the experiential domain; SBT's Experiential dimension encompasses these as sub-types, situating them within a multi-dimensional field where experiential signals interact with and can be overridden by ideological, social, and economic signals. Oswald's (2012) application of Peircean semiotics to brand strategy grounds SBT's Semiotic dimension; SBT extends this by treating semiotic signals as one of eight perceptual channels rather than the primary analytical lens.

The relationship between SBT and Aaker's (1996) Brand Identity Model is one of formalization, not replacement. Aaker's four identity perspectives — Brand as Product, Organisation, Person, Symbol — each bundle multiple independent perceptual channels that SBT decomposes into eight parameterized dimensions. Every insight in Aaker's framework is preserved; SBT adds the observer heterogeneity, coherence taxonomy, and dynamic modelling that the original framework acknowledged as needed but did not formalize. The relationship mirrors that of behavioural economics to classical economics: the predecessor is preserved as a special case within a more general theory.

Keller's (1993) customer-based brand equity is the most direct predecessor: equity lives in the customer's mind, brand knowledge equals awareness plus image. SBT extends Keller by modeling the customer as a heterogeneous population rather than a single model, by formalizing the perception-to-conviction pipeline, and by introducing the re-collapse mechanism that explains how brand equity is lost and rebuilt.

Hatch & Schultz (2010) anticipated SBT's observer-as-co-creator thesis by proposing that brand identity is co-created through stakeholder interactions rather than unilaterally defined by the firm. SBT operationalizes this by making the co-creation mechanism explicit: the observer's spectral profile is the formal instrument of co-creation, and the perception cloud is its product. Urde's (2013) corporate brand identity matrix provides a structured approach to the brand's intended identity — what SBT would call the designed signal architecture — but without the observer model that explains how different cohorts interpret that architecture differently. Park, MacInnis & Priester (2010) distinguish brand attachment from brand attitude strength — a distinction SBT captures as the difference between cloud stability (how resistant the perception cloud is to disruption) and collapse confidence (how certain the conviction is). Swaminathan, Stilley & Ahluwalia (2009) demonstrate that individual differences moderate brand personality effects — direct evidence for the kind of observer heterogeneity SBT formalizes through spectral profiles.

Muniz and O'Guinn's (2001) brand community construct identifies the social dimension as a self-organizing perceptual system: community members share rituals, traditions, and a sense of moral responsibility that function as ambient signals reinforcing the brand's social and narrative dimensions. Fournier and Lee (2009) extend this by distinguishing community structures (pools, webs, hubs) — a typology that maps to SBT's observer cohort architecture, where different community structures produce different ambient signal environments and therefore different perception clouds even within the same brand community.

Sharp's (2010) empirical challenge to brand differentiation — building on the double jeopardy patterns documented by Ehrenberg, Goodhardt, & Barwise (1990) — is complementary rather than contradictory. Sharp describes acquisition: passing the identity gate widely (SBT's "gate permeability"). SBT describes what happens *after* the gate: how different observers cluster signals differently and form different convictions. The frameworks address different stages of the same pipeline.

Vargo & Lusch's (2004) service-dominant logic anticipated a key SBT premise: that value is co-created with the customer rather than delivered to them. SBT operationalizes this by making the observer's spectral profile a formal co-determinant of brand meaning — the brand is literally co-constructed by the observer's perceptual apparatus. Lakoff's (2004) theory of cognitive frames provides a complementary mechanism: priors function as frames that pre-structure which signals are perceived as relevant. An observer with strong ideological priors does not neutrally weigh all signals — they see ideological signals as central and experiential signals as peripheral because their frame makes it so.

Gestalt psychology (Koffka, 1935) provides the perceptual foundations: cloud formation *is* gestalt perception applied to brand signals. Closure (collapsing an incomplete cloud), similarity (dimensional matching), and proximity (temporal clustering) are the mechanisms through which perception clouds form. Kahneman's (2011) dual-process theory maps to the collapse mechanism: strong brand convictions are System 1 shortcuts that bypass deliberate evaluation, while weak or forming clouds require effortful System 2 processing.

Peters' (2019) ergodicity economics offers an unexpected and illuminating organizing analogy. The ergodicity problem — and its implications for decision theory — has attracted growing attention across disciplines (Doctor, Wakker, & Wang, 2020), with experimental evidence confirming that human decision-making reflects time-average rather than ensemble-average optimization (Meder et al., 2021). Peters demonstrates that in multiplicative, path-dependent processes, ensemble averages (averaging across many agents at one moment) diverge systematically from time averages (following one agent across time). This divergence is the formal definition of non-ergodicity. SBT's finding that brand power (an ensemble measure — aggregate awareness across all observers at one moment) and brand health (a time-average measure — how brand architecture performs for any given cohort over its perceptual trajectory) are independent variables is a structural parallel to Peters' thesis in the domain of brand perception. (We use this analogy as an organizing framework — not as a claim that brand perception obeys the specific mathematical properties Peters demonstrates for wealth processes.) The asymmetric conviction resilience finding (Section 4.3) maps to Peters' concept of absorbing states in non-ergodic processes: once a negative conviction crosses a threshold with no experiential friction to reverse it, the observer is on a one-directional compounding trajectory. Peters' framework thus provides a unified root cause — non-ergodic multiplicative dynamics — for multiple independently discovered SBT phenomena.

**Figure 7. Non-Ergodic Brand Perception: Ensemble Average vs. Cohort Trajectories**

```
Brand
Health
  10 |
     |        ........Ensemble average (cross-sectional survey)........
   8 |  ------                                          ------
     |        \  Tech Loyalist                   /-----/
   6 |         \-------\                  /-----/
     |                  \------\   /-----/  Heritage Client
   4 |                         \ /
     |                          X  ← Trajectories cross:
   2 |                         / \    ensemble stays flat,
     |               /--------/   \   cohorts diverge
   0 |  Boycotter --/              \---------\-----------
     +----+----+----+----+----+----+----+----+----+----+----→ Time
     t₀       t₁        t₂        t₃        t₄
          Signal  Crisis   Recovery  New
          shift   event    attempt   equilibrium

     Ensemble average ≈ 6 throughout (misleading stability)
     Individual cohorts: 0 to 8 range (actual dynamics)
```

The divergence between the flat ensemble average and the volatile cohort trajectories is the non-ergodic gap. Cross-sectional brand surveys report the ensemble average — a number that appears stable even as individual cohorts undergo dramatic perceptual shifts in opposite directions.

Attitude strength research (Krosnick & Petty, 1995) establishes that strong attitudes resist change and persist over time. SBT's asymmetric resilience mechanism (Section 4.3) extends this by specifying the dimensional pathway through which resistance operates: evidence-free convictions resist counter-evidence because the observer's spectral profile excludes the dimensions where counter-evidence exists, making the experiential gate structurally closed.

Commodity theory (Brock, 1968) and the scarcity principle (Cialdini, 2001; Lynn, 1991) establish that scarcity enhances perceived value. SBT's structural absence mechanism (Section 4.1) formalizes the underlying pathway: restriction on one dimension generates a cross-dimensional signal on another. The contribution relative to prior scarcity research is not the observation of value enhancement through scarcity — which is well-established — but the specification of the cross-dimensional generation mechanism and its two prerequisites (existing demand and a legitimizing heritage context).

In sum, SBT functions as a meta-framework. The contribution is not the application of spectral methods to brands — it is the identification that brand perception measurement lacks dimensional decomposition, a construct that physics, psychology, economics, consumer research, and signal processing each independently developed for analyzing complex multi-attribute phenomena (see Table 1a). SBT provides the architecture within which Aaker, Kapferer, Keller, Sharp, cognitive science, and ergodicity economics each describe a single stage or dimension of the full perception pipeline.

A complementary question — how organizations *generate* the signals that observers perceive — lies outside SBT's scope but follows naturally from it. Each coherence type discovered in Section 4.2 can be traced to a specific pattern of operational process configuration: Hermès's structural absence emerges from maximally restricted logistical and communication processes; IKEA's signal coherence emerges from globally standardized operations; Tesla's incoherence reflects key signal sources (CEO communication) operating outside any formal process specification. Formalizing the emission side of the pipeline as process-level configuration parameters — where the degree of process specification predicts the designed/ambient ratio, and therefore the coherence type — is a separate research agenda that we plan to develop in a companion paper on the organization as signal source.

### 5.2 Computational Implementability

The closest computational precedent is Colladon's (2018) Semantic Brand Score (SBS), which extracts three network-based dimensions (prevalence, diversity, connectivity) from text data. SBS measures brand *importance* in discourse networks — a salience metric. SBT measures brand *perception* across eight qualitative dimensions — a content metric. The two are complementary: SBS answers "how much is this brand talked about and by whom?" while SBT answers "what do different observers actually perceive?" More broadly, the emerging computational branding literature — including Barari and Eisend's (2024) computational content analysis of brand communications and Sarstedt, Brand, and Ring's (2024) investigation of LLMs as survey respondents — demonstrates growing recognition that brand analysis can be formalized and automated. SBT extends this trajectory from computational *measurement* of existing constructs to computational *execution* of a formal perceptual theory.

A distinguishing property of SBT is that the entire framework can be executed computationally. Signals are typed data structures with dimension, source, emission type, and strength fields. Observer profiles are parameter sets with spectrum, weight, tolerance, and prior fields. Cloud formation is a weighted clustering operation. Conviction collapse is a threshold function. Re-collapse is a full recalculation from the updated evidence set.

This computational character enables AI-native implementation. The seven-module analytical pipeline operates as a structured prompt sequence for large language models. In practice, a capable LLM (Claude, GPT-4, or equivalent) can execute all seven modules in a single analytical session, producing:

- A full signal inventory across eight dimensions
- 3–5 observer cohort spectral profiles
- Per-cohort perception cloud predictions with confidence bands
- A seven-metric coherence scorecard with grade and type classification
- A dimensionally specific emission strategy with phased action plan
- Disruption simulation with per-cohort resilience scoring

The analysis that would require a 4–6 week consulting engagement with a multi-person team compresses into 2–4 hours of LLM interaction. This is not a replacement for human strategic judgment — it is an analytical instrument. The LLM handles the dimensional computation. The strategist handles interpretation, creative response, and stakeholder communication.

The open-source prompt kit and YAML output templates are publicly available at github.com/spectralbranding/sbt-framework.

### 5.3 The AI-Native Thesis

SBT is designed for the AI era in a specific sense. Traditional brand frameworks were designed when brands were analyzed by humans, for humans, about human perceptions. The analysis was qualitative, the insights were narrative, and the frameworks were conceptual tools that could not be coded.

The AI era changes three things simultaneously:

1. **AI as analytical engine.** LLMs can execute multi-dimensional, multi-cohort brand analysis that would overwhelm human cognition. A framework complex enough to capture the actual structure of brand perception — eight dimensions, five cohorts, seven metrics, five coherence types — becomes operational when AI handles the computation.

2. **AI as mediation layer.** Algorithms increasingly mediate between brand signals and human observers — an extension of McLuhan's (1964) thesis that the medium shapes the message. Social media feeds, recommendation engines, and search results filter which signals reach which observers. This mediation layer is itself a spectral filter — it changes which signals are visible to which cohorts based on platform-specific algorithmic logic.

3. **AI as synthetic observer.** LLM-powered recommendation systems ("what EV should I buy?") are a new class of observer with their own spectral profile: trained on text (biased toward narrative and ideological signals), weak on experiential and semiotic signals, and operating without tolerances or identity gates. These synthetic observers will increasingly influence human purchase decisions.

These three shifts are recognized in the emerging AI-era branding literature. Davenport, Guha, Grewal, and Bressgott (2020) identify AI as transforming marketing from segmented to individualized, a trajectory SBT operationalizes through cohort-level spectral profiles. Huang and Rust (2021) propose a theory of AI task replacement that predicts which marketing functions AI will subsume — analytical, mechanical, then intuitive and empathetic. SBT's computational implementability positions it for the analytical phase; the synthetic observer construct addresses the subsequent phases. Puntoni, Reczek, Giesler, and Simester (2021) analyze how consumers experience AI as threatening to their sense of autonomy and uniqueness — perceptual reactions that SBT would model as observer-profile shifts in the ideological and social dimensions triggered by AI-mediated encounters.

SBT accommodates all three changes within its existing architecture. The analytical pipeline was designed for AI execution from inception. The observer model includes encounter modes (direct, mediated, mixed) that capture algorithmic mediation. The signal taxonomy includes synthetic as a source type. The framework does not need to be retrofitted for the AI era because it was built for it.

### 5.4 Limitations and Future Directions

Several limitations warrant discussion. We note that several of the open questions identified below — particularly non-ergodic dynamics, cohort boundary formalization, and resource allocation — now have formal mathematical treatment in the companion papers described in Section 3.5 (Zharnikov, 2026c–k). The limitations discussed here concern the empirical validation of the framework, which remains for future work.

**Weight validation.** Observer dimensional weights are currently expert estimates. While behavioral inference provides defensible ranges — particularly for polarized brands where stated purchase behavior makes priorities visible — empirical validation through conjoint analysis, behavioral experiments, or large-scale survey data would strengthen the framework's credibility. Observer weight assignments are illustrative estimates; the specific values assigned in the case studies were selected for analytical clarity rather than empirical measurement. Different weight assumptions would produce different outputs, and results should be interpreted accordingly.

**Cross-brand calibration.** Cloud confidence scores and coherence metrics are calibrated within each brand analysis but not across brands. Developing an absolute scale — or at minimum, calibration benchmarks across brand categories — is a priority for future work.

**Temporal dynamics.** The framework captures snapshots and simulates disruptions but does not formally model the rate of change. Two temporal properties require formalization: (1) *signal decay* — how individual signal contributions to cloud formation attenuate over time, with decay rates varying by emotional intensity, encounter mode (direct experiential signals persist longer than mediated ones), and reinforcement frequency; and (2) *cohort velocity* — growth rate and conviction migration speed metrics for longitudinal cohort tracking. Per-dimension velocity tracking (signed rate of change, direction classification, acceleration, and linear time-to-absorption estimates) has been implemented in the open-source toolkit (spectralbranding/sbt-framework), operationalizing the discrete approximation to the drift vector defined in Zharnikov (2026j); cohort-level velocity aggregation across observer populations remains an open direction. Signal decay is particularly important because it makes cloud formation recency-weighted: the "evidence set" available at any moment of re-collapse is not the complete historical set but the set of signals that have survived temporal attenuation plus whatever has crystallized into permanent priors.

**Competitive analysis.** The current framework analyzes brands in isolation. Extending the model to competitive contexts — how Brand A's signal environment interacts with Brand B's in the same perceptual space — is a natural extension that the dimensional architecture supports but that has not been validated.

**Temporal compounding.** Our cross-brand comparison reveals that heritage compounds non-linearly — 20 years of heritage is supplementary, 50 years is moderate, 80 years approaches a compounding threshold, and 180+ years becomes the foundational architecture on which all other dimensions rest. Urde, Greyser, and Balmer (2007) formalize brand heritage as a strategic resource with five elements (track record, longevity, core values, use of symbols, and history important to identity) — all of which map to SBT's temporal dimension signals. Brown, Kozinets, and Sherry (2003) demonstrate through retrobranding that heritage signals can be deliberately reconstructed — evidence that the temporal dimension is not merely a passive accumulator but an actively managed signal source. Taleb's (2007) analysis of path-dependent processes under uncertainty provides a formal framework for modeling temporal compounding: small early signals compound into structural priors that resist correction, producing the non-ergodic dynamics formalized in Proposition 2. Formalizing this compounding curve as a mathematical function within the temporal dimension model would strengthen the framework's predictive capacity.

**Multi-model ensemble analysis.** The full cross-model replication (Section 3.4) demonstrates that different LLMs exhibit complementary analytical biases that are consistent across all five brands: Claude Opus 4.6 atomizes observer populations into fine-grained cohorts (5-6 per brand) that isolate perceptual edge cases; Gemini 3.1 Pro synthesizes into parsimonious macro-segments (3 per brand) suited to strategic planning. The structural conclusions (coherence type, grade, key mechanisms) are identical across models for all five brands; the variation occurs exclusively in cohort resolution and minor D/A ratio calibration. This is analogous to viewing the same constellation through telescopes of different apertures — different detail, same structure. Running the pipeline with multiple models produces a richer analysis than either alone, and formalizing this multi-model ensemble approach as a recommended practice would strengthen practitioners' confidence in the framework's outputs.

**Non-ergodic dynamics.** Brand perception operates as a multiplicative, path-dependent process: each new signal multiplies (rather than adds to) an observer's existing cloud confidence. This makes brand perception structurally non-ergodic in Peters' (2019) sense — what happens to the "average observer" in a cross-sectional survey does not predict any individual cohort's perceptual trajectory over time. Introducing an ergodicity coefficient per brand-dimension pair — measuring the degree to which ensemble metrics reliably predict individual cohort trajectories — would strengthen the framework's diagnostic capacity by identifying which dimensions can be safely measured with aggregate surveys and which require longitudinal cohort-trajectory tracking.

**Resource allocation.** The framework identifies *what* observers perceive and *how* convictions form, but does not specify *where* operational investment should be directed given a measured cohort profile. R7 (Zharnikov, 2026k) formalizes spectral resource allocation — the optimal investment of operational resources across dimensions given measured cohort weight profiles. The alignment gap metric quantifies the economic loss from founder weight projection.

### 5.5 Falsifiable Hypotheses

The preceding framework and exploratory analysis generate ten falsifiable hypotheses that constitute the empirical research agenda required to validate SBT as a quantitative theory. The first five hypotheses (H1–H5) are derived from the perception-layer mechanisms reported in Section 4. The remaining five (H6–H10) are derived from the signal dissemination layer (Section 3.5) and address pre-encounter mechanics — how brand signals reach observers in the first place.

**H1 (D/A Goldilocks zone).** Brands with 55–65% designed signals will show higher brand equity and disruption resilience than brands outside this range, controlling for category, age, and market position. *Derivation:* the five-brand D/A comparison (Section 4.4, Figure 6) shows the highest-health brands clustered in this range. *Test:* cross-sectional study of 50+ brands with empirically measured D/A ratios and brand equity scores (e.g., BAV, Interbrand, or bespoke spectral health metrics).

**H2 (Asymmetric conviction resilience).** Evidence-free negative brand convictions will show higher resistance to counter-evidence than evidence-rich positive convictions. *Derivation:* the Tesla Boycotter/Loyalist asymmetry (Section 4.3, Figure 5). *Test:* controlled experiment — expose participants with no product experience and participants with extensive product experience to counter-attitudinal brand information; measure pre/post conviction change magnitude.

**H3 (Coherence type predicts disruption response).** Ecosystem-coherent brands will exhibit selective disruption absorption (periphery sacrificed, core strengthened); incoherent brands will exhibit disruption amplification (existing divisions widen). *Derivation:* the five-type coherence taxonomy (Section 4.2, Figure 4). *Test:* longitudinal cohort tracking before and after documented brand crisis events; compare per-cohort resilience trajectories across coherence types.

**H4 (Non-ergodic gap).** For incoherent brands, cross-sectional brand surveys will systematically overstate cohort-level resilience relative to longitudinal individual-level tracking. For signal-coherent brands, the gap will be minimal. *Derivation:* the brand power/health independence finding (Section 4.4) and the non-ergodic organizing analogy (Section 5.1, Figure 7). *Test:* paired study — compare snapshot survey scores to individual panel tracking data for the same brand across incoherent versus signal-coherent types.

**H5 (Structural absence prerequisite).** Structural absence strategies (designed signal restriction) generate positive scarcity signals only when two conditions are met: (a) existing demand for the restricted dimension, and (b) a legitimizing heritage context that makes restriction legible as intention rather than incapacity. *Derivation:* the Hermès structural absence mechanism (Section 4.1). *Test:* experiment — manipulate scarcity (present vs. absent) crossed with demand level (high vs. low) and heritage context (established vs. novel); measure perceived exclusivity versus perceived arrogance.

**H6 (Gate friction varies by cohort).** Identity gate friction for a given brand will differ significantly across observer cohorts, with cohorts whose dominant dimensions match the brand's strongest emission dimensions showing lower gate friction. *Derivation:* the identity gate mechanism (Section 3.3) combined with dimensional weight heterogeneity across cohorts. *Test:* exposure experiment — present brand cues to cohorts with different spectral profiles; measure recognition threshold (number of exposures to achieve recognition).

**H7 (First-atom primacy).** The dimensional content of the first brand atom encountered will disproportionately determine the observer's initial spectral profile, persisting as a prior even after subsequent atoms provide evidence on other dimensions. *Derivation:* the prior formation mechanism (Section 3.3) and non-ergodic path dependence (Section 5.1). *Test:* experiment — expose different groups to different "first atoms" (experiential versus semiotic versus ideological); measure resulting spectral profiles after equal total exposure.

**H8 (Amplification asymmetry).** Confirmed observers with negative-valence brand facts will have higher amplification rates (secondary emission volume) than those with positive-valence facts, creating faster signal field population for negative atoms. *Derivation:* the asymmetric conviction resilience finding (Section 4.3). *Test:* track secondary emission behavior (reviews, social posts, word-of-mouth) for positive versus negative Confirmed observers; measure volume and reach of emitted ambient atoms.

**H9 (Channel-dimension coupling).** Specific channels show systematic dimensional bias in atom transmission — for example, social media transmits semiotic and social dimensions at high fidelity but experiential at low fidelity; direct encounters transmit experiential at high fidelity but ideological at low fidelity. *Derivation:* the mediated cloud formation finding (Section 4.3) and channel fidelity concept (Section 3.5). *Test:* compare spectral profiles of observers who encountered the same brand through different channels; measure dimensional variance attributable to channel.

**H10 (Field density threshold).** There exists a minimum signal field density below which encounter probability drops to near-zero regardless of observer receptivity, and this threshold is higher for channels with low signal-to-noise ratio. *Derivation:* the signal dissemination layer (Section 3.5) and Sharp's (2010) mental availability framework. *Test:* vary brand signal frequency in controlled environments; measure encounter rate as a function of field density and channel noise level.

\newpage

**Figure 8. Research Agenda: Falsifiable Hypotheses and Testing Methods**

```
                         SBT Framework
                         (Sections 2-4)
                        /              \
                       v                v
  Perception Layer (H1-H5)        Dissemination Layer (H6-H10)
  +---------------------------+   +---------------------------+
  | H1: D/A Goldilocks        |   | H6: Gate Friction         |
  |     55-65% designed opt.   |   |     Varies by cohort      |
  | H2: Asymmetric Resilience |   | H7: First-Atom Primacy    |
  |     Evidence-free > rich   |   |     Initial shapes priors |
  | H3: Coherence->Disruption |   | H8: Amplification Asymm.  |
  |     Type predicts response |   |     Negative > positive   |
  | H4: Non-Ergodic Gap       |   | H9: Channel-Dim. Coupling |
  |     Ensemble != time avg   |   |     Channels bias dims    |
  | H5: Absence Prerequisite  |   | H10: Field Density Thresh.|
  |     Demand + heritage req. |   |      Minimum for encounter|
  +---------------------------+   +---------------------------+
```

The first five hypotheses (H1–H5) test the core perception-layer predictions of SBT: structural predictions (H1, H3), conviction dynamics (H2), non-ergodic diagnostics (H4), and structural absence boundary conditions (H5). The dissemination-layer hypotheses (H6–H10) extend the research agenda to pre-encounter mechanics: how observer cohorts differ in gate friction (H6), how first-atom encounters shape lasting priors (H7), how negative convictions amplify faster than positive ones (H8), how channels systematically bias dimensional transmission (H9), and what minimum signal density is required for encounter events (H10). A program that validates H1–H10 would move SBT from an exploratory framework to a comprehensive, quantitatively grounded theory of brand perception across the full lifecycle — from pre-awareness through conviction formation to re-collapse.

---

## 6. Conclusion

Spectral Brand Theory contributes a formal, computational framework for modeling brand perception as an observer-mediated process. The core claim — there is no brand-in-itself, only signals and observers — produces an analytical architecture that explains phenomena traditional frameworks cannot: how the same brand can be simultaneously powerful and fragile (Tesla), how restricting signals can create more value than emitting them (Hermès), how five qualitatively different types of brand coherence determine resilience profiles that a single coherence score cannot distinguish, and how evidence-free convictions can be more stable than evidence-rich ones.

The five formal propositions — observer heterogeneity, non-ergodic perception, structural absence as signal, coherence type over coherence score, and conviction asymmetry — formalize the framework's most distinctive structural claims and establish a concrete research agenda. Each proposition specifies a testable prediction that existing brand frameworks cannot generate because they lack the necessary constructs: parameterized observer profiles, multi-dimensional signal architecture, and the perception-to-conviction pipeline. The ten falsifiable hypotheses in Section 5.5 operationalize these propositions into experimental designs spanning cross-sectional brand studies, controlled signal-sequence experiments, and longitudinal cohort tracking.

The framework has been demonstrated across five illustrative brand analyses spanning luxury, mass-market, mission-driven, technology, and hyperlocal categories. The exploratory analysis produced 25 non-obvious, dimensionally specific, actionable, observer-differentiated insights (five per brand, formally assessed against all four criteria — see Section 3.3) — a yield that is consistent with the framework capturing structural properties of brand perception, though independent validation with primary consumer data is required to confirm this interpretation (see Section 3.4)

The framework's computational implementability — executable as a structured LLM prompt sequence with open-source templates — makes multi-cohort brand analysis accessible to practitioners without custom engineering, collapsing a multi-week consulting engagement into a single analytical session. The prompt kit, YAML templates, and framework documentation are publicly available.

SBT is not a replacement for strategic judgment. It is an analytical instrument — an X-ray machine for brand architecture. It sees the structure. The strategist decides what to build.

---

## Author Note

Dmitry Zharnikov is an independent researcher and strategist. He holds a Professional MBA (Entrepreneurship & Innovation) from Technische Universitat Wien and Wirtschaftsuniversitat Wien (dual degree, 2018). ORCID: https://orcid.org/0009-0000-6893-9231

---

## References

Aaker, D. A. (1996). *Building strong brands*. Free Press.

Alba, J. W., & Hutchinson, J. W. (1987). Dimensions of consumer expertise. *Journal of Consumer Research*, 13(4), 411–454.

Barari, M., & Eisend, M. (2024). Computational content analysis of brand communications: A review and research agenda. *International Journal of Research in Marketing*, 41(1), 24–47.

Ambler, T. (2003). *Marketing and the bottom line: The marketing metrics to pump up cash flow* (2nd ed.). Financial Times/Prentice Hall.

Barthes, R. (1957). *Mythologies*. Seuil.

Berger, J. (2013). *Contagious: Why things catch on*. Simon & Schuster.

Brown, S., Kozinets, R. V., & Sherry, J. F., Jr. (2003). Teaching old brands new tricks: Retro branding and the revival of brand meaning. *Journal of Marketing*, 67(3), 19–33.

Brock, T. C. (1968). Implications of commodity theory for value change. In A. G. Greenwald, T. C. Brock, & T. M. Ostrom (Eds.), *Psychological foundations of attitudes* (pp. 243–275). Academic Press.

Carroll, J. D., & Chang, J. J. (1970). Analysis of individual differences in multidimensional scaling via an N-way generalization of Eckart-Young decomposition. *Psychometrika*, 35(3), 283–319.

Colladon, A. F. (2018). The Semantic Brand Score. *Journal of Business Research*, 88, 150–160.

Connelly, B. L., Certo, S. T., Ireland, R. D., & Reutzel, C. R. (2011). Signaling theory: A review and assessment. *Journal of Management*, 37(1), 39–67.

Chatman, J. A., Caldwell, D. F., O'Reilly, C. A., & Doerr, B. (2014). Parsing organizational culture: How the norm for adaptability influences the relationship between culture consensus and financial performance in high-technology firms. *Journal of Organizational Behavior*, 35(6), 785–808.

Christodoulides, G., & de Chernatony, L. (2010). Consumer-based brand equity conceptualization and measurement. *International Journal of Market Research*, 52(1), 43–66.

Cialdini, R. B. (2001). *Influence: Science and practice* (4th ed.). Allyn & Bacon.

Damasio, A. R. (1994). *Descartes' error: Emotion, reason, and the human brain*. Putnam.

Davenport, T., Guha, A., Grewal, D., & Bressgott, T. (2020). How artificial intelligence will change the future of marketing. *Journal of the Academy of Marketing Science*, 48(1), 24–42.

Dawar, N., & Parker, P. (1994). Marketing universals: Consumers' use of brand name, price, physical appearance, and retailer reputation as signals of product quality. *Journal of Marketing*, 58(2), 81–95.

De Chernatony, L., & McDonald, M. (2003). *Creating powerful brands*. Butterworth-Heinemann.

Doctor, J. N., Wakker, P. P., & Wang, T. V. (2020). Economists' views on the ergodicity problem. *Nature Physics*, 16, 1168.

Eco, U. (1976). *A theory of semiotics*. Indiana University Press.

Erdem, T., & Swait, J. (1998). Brand equity as a signaling phenomenon. *Journal of Consumer Psychology*, 7(2), 131–157.

Ehrenberg, A. S. C., Goodhardt, G. J., & Barwise, T. P. (1990). Double jeopardy revisited. *Journal of Marketing*, 54(3), 82–91.

Feldwick, P. (1996). What is brand equity anyway, and how do you measure it? *Journal of the Market Research Society*, 38(2), 85–104.

Festinger, L. (1957). *A theory of cognitive dissonance*. Stanford University Press.

Floch, J.-M. (1990). *Semiotics, marketing and communication: Beneath the signs, the strategies*. Palgrave Macmillan.

Fournier, S., & Lee, L. (2009). Getting brand communities right. *Harvard Business Review*, 87(4), 105–111.

Fishbein, M., & Ajzen, I. (1975). *Belief, attitude, intention and behavior: An introduction to theory and research*. Addison-Wesley.

Green, P. E., & Srinivasan, V. (1978). Conjoint analysis in consumer research: Issues and outlook. *Journal of Consumer Research*, 5(2), 103–123.

Grier, S. A., & Brumbaugh, A. M. (1999). Noticing cultural differences: Ad meanings created by target and non-target markets. *Journal of Advertising*, 28(1), 79–93.

Hatch, M. J., & Schultz, M. (2010). Toward a theory of brand co-creation with implications for brand governance. *Journal of Brand Management*, 17(8), 590–604.

Hogarth, R. M., & Einhorn, H. J. (1992). Order effects in belief updating: The belief-adjustment model. *Cognitive Psychology*, 24(1), 1–55.

Holt, D. B. (2004). *How brands become icons: The principles of cultural branding*. Harvard Business Press.

Huang, M.-H., & Rust, R. T. (2021). A strategic framework for artificial intelligence in marketing. *Journal of the Academy of Marketing Science*, 49(1), 30–50.

Kahneman, D. (2011). *Thinking, fast and slow*. Farrar, Straus and Giroux.

Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-291.

Kapferer, J.-N. (2008). *The new strategic brand management* (4th ed.). Kogan Page.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1–22.

Keller, K. L., & Lehmann, D. R. (2006). Brands and branding: Research findings and future priorities. *Marketing Science*, 25(6), 740–759.

Kirmani, A., & Rao, A. R. (2000). No pain, no gain: A critical review of the literature on signaling unobservable product quality. *Journal of Marketing*, 64(2), 66–79.

Koffka, K. (1935). *Principles of Gestalt psychology*. Harcourt, Brace.

Krosnick, J. A., & Petty, R. E. (1995). Attitude strength: An overview. In R. E. Petty & J. A. Krosnick (Eds.), *Attitude strength: Antecedents and consequences* (pp. 1–24). Erlbaum.

Lakoff, G. (2004). *Don't think of an elephant!* Chelsea Green.

Lynn, M. (1991). Scarcity effects on value: A quantitative review of the commodity theory literature. *Psychology & Marketing*, 8(1), 43–57.

McLuhan, M. (1964). *Understanding media: The extensions of man*. McGraw-Hill.

Meder, D., et al. (2021). Ergodicity-breaking reveals time optimal decision making in humans. *PLOS Computational Biology*, 17(9), e1009217.

Mick, D. G. (1986). Consumer research and semiotics: Exploring the morphology of signs, symbols, and significance. *Journal of Consumer Research*, 13(2), 196–213.

Muniz, A. M., & O'Guinn, T. C. (2001). Brand community. *Journal of Consumer Research*, 27(4), 412–432.

Oswald, L. R. (2012). *Marketing semiotics: Signs, strategies, and brand value*. Oxford University Press.

Park, C. W., MacInnis, D. J., & Priester, J. R. (2010). Brand attachment and brand attitude strength: Conceptual and empirical differentiation of two critical brand equity drivers. *Journal of Marketing*, 74(6), 1–17.

Peirce, C. S. (1931–1958). *Collected papers of Charles Sanders Peirce* (C. Hartshorne & P. Weiss, Eds., Vols. 1–6). Harvard University Press.

Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, 15, 1216–1221. https://doi.org/10.1038/s41567-019-0732-0

Puntoni, S., Vanhamme, J., & Ruber, R. (2011). Two birds and one stone: Purposeful polysemy in minority targeting and advertising evaluations. *Journal of Advertising*, 40(1), 25–41.

Puntoni, S., Reczek, R. W., Giesler, M., & Simester, D. (2021). Consumers and artificial intelligence: An experiential perspective. *Journal of Marketing*, 85(1), 131–151.

Ries, A., & Trout, J. (1981). *Positioning: The battle for your mind*. McGraw-Hill.

Sarstedt, M., Brand, B. M., & Ring, C. (2024). Can LLMs replace human survey respondents? An investigation of LLM biases. *Journal of the Academy of Marketing Science*. Advance online publication.

Schmitt, B. H. (1999). *Experiential marketing*. Free Press.

Sharp, B. (2010). *How brands grow: What marketers don't know*. Oxford University Press.

Smith, W. R. (1956). Product differentiation and market segmentation as alternative marketing strategies. *Journal of Marketing*, 21(1), 3–8.

Sorensen, J. B. (2002). The strength of corporate culture and the reliability of firm performance. *Administrative Science Quarterly*, 47(1), 70–91.

Spence, M. (1973). Job market signaling. *The Quarterly Journal of Economics*, 87(3), 355–374.

Swaminathan, V., Stilley, K. M., & Ahluwalia, R. (2009). When brand personality matters: The moderating role of attachment styles. *Journal of Consumer Research*, 35(6), 985–1002.

Taleb, N. N. (2007). *The black swan: The impact of the highly improbable*. Random House.

Urde, M. (2013). The corporate brand identity matrix. *Journal of Brand Management*, 20(9), 742–761.

Urde, M., Greyser, S. A., & Balmer, J. M. T. (2007). Corporate brands with a heritage. *Journal of Brand Management*, 15(1), 4–19.

Vargo, S. L., & Lusch, R. F. (2004). Evolving to a new dominant logic for marketing. *Journal of Marketing*, 68(1), 1–17.

Veblen, T. (1899). *The theory of the leisure class*. Macmillan.

Wedel, M., & Kamakura, W. A. (2000). *Market segmentation: Conceptual and methodological foundations* (2nd ed.). Kluwer Academic.

Wilkie, W. L., & Pessemier, E. A. (1973). Issues in marketing's use of multi-attribute attitude models. *Journal of Marketing Research*, 10(4), 428–441.

Wood, L. (2000). Brands and brand equity: Definition and management. *Management Decision*, 38(9), 662–669.

Yankelovich, D., & Meer, D. (2006). Rediscovering market segmentation. *Harvard Business Review*, 84(2), 122–131.

Zajonc, R. B. (1980). Feeling and thinking: Preferences need no inferences. *American Psychologist*, 35(2), 151–175.

Zharnikov, D. (2026b). The atom-cloud-fact epistemological pipeline: From financial document processing to brand perception modeling. Working Paper. https://doi.org/10.5281/zenodo.18944770

Zharnikov, D. (2026c). Geometric approaches to brand perception: A critical survey and research agenda. Working Paper. https://doi.org/10.5281/zenodo.18945217

Zharnikov, D. (2026d). Brand space geometry: A formal metric for multi-dimensional brand perception. Working Paper. https://doi.org/10.5281/zenodo.18945295

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026f). Cohort boundaries in high-dimensional perception space: A concentration of measure analysis. Working Paper. https://doi.org/10.5281/zenodo.18945477

Zharnikov, D. (2026g). How many brands can a market hold? Sphere packing bounds for multi-dimensional positioning. Working Paper. https://doi.org/10.5281/zenodo.18945522

Zharnikov, D. (2026h). Specification impossibility in organizational design: A high-dimensional geometric analysis. Working Paper. https://doi.org/10.5281/zenodo.18945591

Zharnikov, D. (2026i). The Organizational Schema Theory: Test-driven business design. Working Paper. https://doi.org/10.5281/zenodo.18946043

Zharnikov, D. (2026j). Non-ergodic brand perception: Diffusion dynamics on multi-dimensional perceptual manifolds. Working Paper. https://doi.org/10.5281/zenodo.18945659

Zharnikov, D. (2026k). Spectral resource allocation: Demand-driven investment in multi-dimensional brand space. Working Paper. https://doi.org/10.5281/zenodo.19009268

---

*Working paper. Comments: dmitry@spectralbranding.com. Open-source toolkit: github.com/spectralbranding/sbt-framework. License: MIT.*

