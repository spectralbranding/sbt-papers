# Spectral Brand Theory: A Computational Framework for Multi-Dimensional Brand Perception

**Dmitry Zharnikov**

Working Paper v3.1.1 — February 2026 (revised April 2026)

*Zenodo DOI: [10.5281/zenodo.18945912](https://doi.org/10.5281/zenodo.18945912)*

---

## Abstract

Brand measurement collapses multi-dimensional perception into single scores, destroying the information that explains why different observers form irreconcilable perceptions of the same brand. Prior dimensional approaches decompose brand meaning into attribute-level dimensions but treat those dimensions as properties of the brand rather than perceptual channels through which heterogeneous observers filter signals. This paper develops Spectral Brand Theory (SBT), arguing that brand perception is irreducibly observer-dependent. The framework decomposes brand signals across eight perceptual dimensions, defines observer cohorts through formal spectral profiles, and models perception as probabilistic cloud formation that collapses into conviction through evidence accumulation. Five formal propositions address observer heterogeneity, non-ergodic perception, structural absence, coherence types, and conviction asymmetry. An illustrative application to five brands articulates four candidate mechanisms: structural absence as brand strategy, a five-type coherence taxonomy, asymmetric conviction resilience, and independence of brand power from brand health. Cross-model replication suggests structural conclusions are framework-driven rather than model-specific. SBT contributes a computationally implementable, observer-centric architecture that extends customer-based brand equity theory. Empirical validation against independently collected consumer data, including a 21,350-call multi-model study (Zharnikov 2026v), provides initial corroboration of the dimensional collapse predictions.

**Keywords:** brand perception, dimensional decomposition, computational branding, observer heterogeneity, brand coherence, structural absence, non-ergodic dynamics, AI-native framework

---

## 

Consider a thought experiment. Six people are asked to describe the same brand — Tesla. One says it is the most innovative technology platform since Apple. Another calls it Elon Musk's political vehicle. A third describes a betrayal of the environmental movement. A fourth sees a practical electric car with a controversial footnote. A fifth, who has never sat in one, holds a strong conviction about exactly what kind of person drives it. A sixth, in Shanghai, sees a premium Western status symbol and is puzzled by the question.

Same brand. Six descriptions. No overlap.

This is not a communication failure. It is a structural condition — and diagnosing it requires a vocabulary that traditional brand frameworks do not have. Each major framework captures a real aspect of brand dynamics but contains a structural limitation that prevents it from modeling the phenomenon above.

Ries & Trout's (1981) positioning theory treats brand perception as a single position in the consumer's mind — a slot to be occupied. The structural limitation is that "position" is singular: the framework has no mechanism for different observers assigning different positions to the same brand. Tesla does not occupy one position; it occupies at least six irreconcilable positions simultaneously, and no repositioning can collapse them into one.

Aaker's (1996) brand identity system describes what the brand *is* — its intended identity across functional, emotional, and self-expressive dimensions. The structural limitation is that identity is sender-side: the framework specifies what the brand emits but does not formalize the observer's role in assembling perceived meaning. Different observers receive the same identity signals and construct different brands; Aaker's model has no parameter for this divergence.

Kapferer's (2008) prism includes "reflection" and "self-image" facets that gesture toward the observer — an important acknowledgment that the receiver matters. The structural limitation is that these facets are not parameterized: Kapferer recognizes that different audiences see different reflections but provides no formal mechanism for specifying *how* or *why* the reflections differ across observer groups.

Keller's (1993) customer-based brand equity model locates equity in the customer's mind — the closest precedent to SBT's approach and the most important one. The structural limitation is that Keller treats "the customer" as a single model: one set of brand associations, one equity structure. The framework acknowledges individual variation but does not formalize it. SBT's central move is to parameterize exactly what Keller left as an acknowledged but unmodeled phenomenon — the heterogeneous observer.

Christodoulides & de Chernatony (2010) consolidate these equity-based approaches into a measurement framework that remains anchored to the single-observer assumption. The broader brand equity literature — including Feldwick's (1996) taxonomy distinguishing brand valuation, brand strength, and brand description; Ambler's (2003) operational metrics approach; and Wood's (2000) reconciliation of financial and consumer perspectives — operates within the same assumption: equity is a property of the brand-observer pair, but the observer is treated as singular. Keller & Lehmann (2006) survey the field's research priorities and identify measurement of brand equity as a central challenge — yet the measurement frameworks they review all assume a single "true" brand perception to be measured. The structural limitation across this measurement tradition is the premise that there exists one correct brand perception to measure, rather than multiple structurally different perceptions that are simultaneously valid.

Sharp's (2010) empirical marketing science measures mental and physical availability — how easily the brand comes to mind and how easily it can be purchased. The structural limitation is that availability is a pre-perceptual construct: Sharp measures whether the brand passes the identity gate but does not model the perception mechanism that translates availability into conviction. Two observers with identical availability can form opposite convictions; Sharp's framework cannot explain why.

The gap is not in any single framework. It is structural: brand measurement collapses multi-dimensional perception into single scores — Net Promoter Score, brand equity indices, awareness metrics — destroying the information that explains why six observers form six irreconcilable perceptions of the same brand. The information is not noise. It is the phenomenon itself. This dimensional compression is an instance of what Flake and Fried (2020) term *questionable measurement practices* — decisions that raise doubts about whether the measure captures the intended construct. When brand equity indices reduce eight-dimensional perception to a single score, the measurement instrument itself becomes the primary source of information loss.

Fields that study complex multi-attribute phenomena have independently developed constructs for preserving this information — *dimensional decomposition*: the systematic separation of a complex signal into independent measurement channels. While brand researchers have recognized the need for multi-dimensional approaches (France, Davcik, & Kazandjian, 2025; Guhl, 2024; Lambrecht, Baumgarth, & Henseler, 2025), no framework has formalized the observer-dependent filtering mechanism that explains why the same brand signals produce different perceptions in different cohorts.

**Table 1.** Dimensional decomposition across fields. Despite repeated calls for multi-dimensional approaches to brand perception (Keller & Lehmann, 2006; Christodoulides & de Chernatony, 2010), no formal decomposition framework preserving observer-level information has been adopted.

| Domain | Decomposition Construct | Key Work |
|:---|:---|:---|
| Physics | Spectroscopy | Newton (1672), Fraunhofer (1814) |
| Psychology | Factor analysis | Thurstone (1947), Cattell (1966) |
| Economics | Multi-attribute utility | Lancaster (1966), Fishbein & Ajzen (1975) |
| Consumer research | Conjoint analysis | Green & Srinivasan (1978), Wilkie & Pessemier (1973) |
| Signal processing | Fourier decomposition | Fourier (1822) |
| Computational text analysis | Semantic Brand Score | Colladon (2018) |
| **Brand perception theory** | **No standard framework** | **Single-score metrics collapse dimensions** |

The contribution of this paper is not the application of spectral methods to brands — it is the identification that brand perception measurement lacks an *observer-mediated* dimensional decomposition. Prior decompositions in the brand domain — J. Aaker's (1997) personality dimensions, Kervyn, Fiske, and Malone's (2012) warmth-competence space, Brakus, Schmitt, and Zarantonello's (2009) experience scale — treat dimensions as brand attributes. SBT treats them as perceptual channels through which heterogeneous observers filter signals, preserving the observer-level information that attribute-level decompositions collapse. The "spectral" label is descriptive: the eight dimensions are independent measurement channels, analogous to spectral bands in that each carries information the others cannot. The analogy names the construct; it does not claim that brands are literally like light.

This paper challenges the field's deeper assumption: that "the brand" is a coherent object that exists independently of who is observing it.

Spectral Brand Theory (SBT) proposes that there is no single brand perception that applies uniformly to all observers — each cohort assembles structurally different brand meaning from the same signal environment. The brand's signal architecture (what it emits and how) can be characterized at the brand level, while brand meaning exists only in observer-specific perception. What we call "the brand" is always already a collapse: a conviction in someone's mind, assembled from whichever signals they could perceive through their particular spectral profile. Different observers, perceiving the same signal environment through different spectral sensitivities, form structurally different brand convictions. These convictions are not errors or variations on a "true" brand — they are the only brands that exist.

The framework contributes to branding theory in three ways:

1. **Formal observer model.** SBT defines each observer cohort through a spectral profile: which dimensions they can perceive (spectrum), how they weight those dimensions (weights), how much inconsistency they accept (tolerances), what they already believe (priors), and whether they can recognize the brand at all (identity gate). This transforms "different people perceive differently" from a qualitative observation into a parameterized scoring function.

2. **Perception pipeline.** SBT models brand perception as a multi-stage pipeline: signal emission → observer filtering → probabilistic cloud formation → threshold-based conviction collapse → re-collapse on new evidence. Each stage is formally specified and computationally implementable. The pipeline explains not only what observers currently believe but how those beliefs will change under disruption.

3. **Computational implementability.** Unlike prior branding frameworks, SBT can be directly executed as software. Signals are typed data structures. Observers are parameter sets. Perception is clustering output. Conviction is a threshold function. The entire pipeline operates as a structured prompt sequence for large language models, making multi-cohort brand analysis accessible without custom engineering.

The remainder of this paper is organized as follows. Section 2 presents the theoretical framework, culminating in five formal propositions (Section 2.6) that specify the framework's testable structural predictions. Section 3 describes the illustrative application. Section 4 reports findings, focusing on four candidate mechanisms the application makes visible. Section 5 discusses implications, limitations, and future directions. Section 6 concludes.

---

## Theoretical Framework

### 2.1 Epistemic Foundation: Brands as Perceptual Objects

SBT's core claim is epistemic: a brand is not an object with properties but a perceptual process with observers. The metaphor is astronomical. A constellation of stars appears different from every point in the universe and to every creature with a different range of spectral sensitivity. The constellation "itself" — all stars from no perspective — is a theoretical construct no one actually experiences. What exists are observer-specific perceptions of a shared signal field. (The stellar metaphor is useful for visualizing multi-dimensionality and observer sensitivity differences; it should be noted that in optics the spectrum is observer-independent, while in brand perception the observer's profile co-creates the perceived brand.)

Applied to brands: what a company designs and emits (logo, products, campaigns, pricing, culture) are signals. These signals exist across multiple perceptual dimensions. Each observer cohort filters these signals through its spectral profile, clusters the perceived signals into a probabilistic perception cloud, and — if sufficient evidence accumulates — collapses that cloud into a brand conviction. The conviction is observer-specific. The signal environment is shared. The brand, as commonly understood, is the observer's collapse product — not the company's intended identity.

This inversion has a philosophical precedent. Peirce's semiotics (1890s) established that meaning arises in the interpreter, not the sign. Barthes (1957) showed how cultural myths function as second-order semiotic systems that shape interpretation. Keller (1993) located brand equity in the customer's mind. SBT formalizes and extends these insights into a computational architecture.

### 2.2 Signal Architecture: Eight Perceptual Dimensions

SBT decomposes brand signals across eight dimensions, each representing a distinct channel through which observers perceive brand meaning:

**Table 2.** The eight perceptual dimensions of brand signal architecture.

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

The eight dimensions emerged from a synthesis of prior frameworks. Kapferer's (2008) "physique" maps to the semiotic dimension; his "culture" maps to cultural and ideological; his "relationship" maps to experiential and social. Aaker's (1996) functional benefits map to experiential and economic; emotional benefits to social and cultural; self-expressive benefits to ideological and social. Holt's (2004) cultural branding theory maps to a combination of ideological and cultural dimensions, treating brands as cultural artifacts that derive meaning from their position in cultural discourse. De Chernatony & McDonald's (2003) brand management framework similarly addresses the multi-faceted nature of brand meaning but treats the facets as brand properties rather than observer-dependent perceptual channels. Floch's (1990) structural semiotics provides a complementary decomposition of the semiotic dimension, distinguishing practical, ludic, utopian, and critical valorizations that map to distinct sub-channels within SBT's semiotic-ideological space. Mick (1986) establishes the semiotic foundations for consumer research, demonstrating that brand signs operate through both denotative and connotative codes — a distinction SBT operationalizes through the designed/ambient signal classification. The temporal dimension — heritage and time-depth — appears in prior work as an attribute of specific brands but has not been modeled as a universal perceptual channel. Recent work confirms that these dimensions extend to emerging contexts: Pagani and Xie (2025) demonstrate that metaverse brand experiences produce measurable effects across awareness, associations, perceived quality, and loyalty — dimensions that map directly to SBT's experiential, social, and economic channels.

Each signal carries three properties:

- **Source type**: designed (created by the brand), ambient (generated by the environment — reviews, word-of-mouth transmission (Berger, 2013), competitor framing, cultural commentary), or synthetic (AI-generated content, LLM summaries, algorithmic recommendations).
- **Emission type**: positive (signal actively present), null (unintentional absence), or structural absence (designed restriction that functions as a signal — see Section 4.1).
- **Strength**: rated 0–5, reflecting intensity of emission.

The signal concept extends economic signaling theory (Spence, 1973) and its application to brand credibility (Erdem & Swait, 1998; Kirmani & Rao, 2000) from a unidimensional quality indicator to a multi-dimensional perceptual architecture. Connelly, Certo, Ireland, and Reutzel (2011) consolidate signaling theory across management disciplines — their review identifies signal observability, signal cost, and signal honesty as the three properties that determine signal effectiveness. SBT operationalizes all three: observability maps to the observer's spectral sensitivity (invisible dimensions produce no signal regardless of emission strength), cost maps to designed-versus-ambient classification, and honesty maps to the coherence between designed signals and the ambient signal field. Dawar and Parker (1994) demonstrate that signal reliance varies systematically across cultures and product categories — evidence that the observer's context shapes which signals carry information, precisely the mechanism SBT formalizes through cohort-specific weight profiles. In SBT, a brand emits not one signal but a structured field of typed signals across eight dimensions — and the observer, not the market, determines which signals are informative.

The ratio of designed to ambient signals — the **designed/ambient (D/A) ratio** — has emerged as one of the framework's most diagnostic metrics. A brand whose perception is predominantly shaped by ambient signals (D/A < .40) faces a structural problem that no communication strategy can solve: the brand's story is being written by others.

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


**Figure 1.** The Observer-Mediated Perception Pipeline

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


**Figure 2.** Observer Heterogeneity: Same Signal Field, Different Perceptions

```
                    Tesla Signal Environment
                    (Same 8-dimensional signals)
                           /            \
                          /              \
            Tech Loyalist                  Progressive Boycotter
  Experiential: .35                       Ideological: .45
  Economic:     .20                       Social:      .20
  Ideological:  .10                       Experiential: .03
  Tolerance:    High                       Tolerance:    Zero
            |                                        |
            v                                        v
     Positive Cloud                           Negative Cloud
    (Product-anchored)                      (Ideology-anchored)
     Confidence: .78                        Confidence: .82
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

**Table 3.** The seven-metric spectral scorecard.

| Metric | What It Measures |
|:-------|:-----------------|
| Dimensional coverage | How many dimensions the brand actively emits on |
| Gate permeability | What proportion of target observers recognize the brand |
| Cloud coherence | Compatibility of perception clouds across cohorts |
| Collapse strength | Confidence level of resulting convictions |
| Re-collapse resistance | Stability of convictions under disruption |
| Emission efficiency | Signal-to-noise ratio of designed signals |
| Designed/ambient ratio | Brand's control over its own signal environment |

### 2.6 Formal Propositions

The theoretical framework developed in Sections 2.1–2.5 generates five formal propositions that specify testable structural predictions. Each proposition formalizes an argument that the framework makes implicitly; stating them explicitly establishes the empirical commitments that distinguish SBT from a descriptive vocabulary.

**Proposition 1 (Observer heterogeneity).** *Different observer cohorts, exposed to identical brand signal environments, will form systematically different brand convictions as a function of their spectral profile differences (weights, tolerances, priors, encounter mode).*

Keller (1993) locates brand equity in the customer's mind — the most important precedent for SBT's observer-dependent approach. The structural limitation of Keller's model is that it treats "the customer" as a single model: one set of brand associations, one equity structure. Keller acknowledged individual variation but did not parameterize it. SBT formalizes the heterogeneity that Keller's framework recognized but could not model, specifying the observer's spectral profile as the mechanism through which identical signals produce different convictions. Empirical evidence for observer-dependent brand perception already exists in the advertising literature. Grier and Brumbaugh (1999) demonstrated that identical advertisements produce systematically different meanings in target versus non-target cultural groups. Puntoni, Vanhamme, and Ruber (2011) documented "purposeful polysemy" — the deliberate design of messages that activate different meanings in different audiences — providing direct evidence that what SBT formalizes as spectral metamerism is an observed phenomenon in marketing practice. Testable prediction: measuring brand conviction across cohorts with documented spectral profile differences will reveal systematic, profile-predictable divergence rather than random variation.

**Proposition 2 (Non-ergodicity of perception).** *The temporal sequence in which brand signals are encountered affects the resulting brand conviction, even when the set of signals is identical.*

Peters (2019) demonstrates that in multiplicative, path-dependent processes, the order of events matters — ensemble averages diverge from time averages. Brand perception is structurally analogous: signals compound multiplicatively through priors rather than summing additively into a running total. An observer who encounters a product failure before a brand's origin story forms a different conviction than one who encounters the same two signals in reverse order, because the first signal establishes a prior that filters interpretation of the second. In consumer psychology, Hogarth and Einhorn (1992) provided the formal precedent for order-dependent belief updating: their Belief-Adjustment Model demonstrates that step-by-step evaluation produces different outcomes from end-of-sequence evaluation, and that negative evidence has asymmetric updating power relative to positive evidence — a mechanism that SBT formalizes as conviction asymmetry. The structural limitation of cross-sectional brand measurement is that it captures ensemble averages — snapshots across many observers at one moment — which systematically misrepresent individual cohort trajectories. Guhl (2024) provides methodological precedent by tracking time-varying utility-based brand equity from household panel data, demonstrating that brand equity fluctuates at the individual level in ways that aggregate measures obscure. Testable prediction: presenting the same signal set in different temporal orders to matched cohorts will produce measurably different conviction outcomes.

**Proposition 3 (Structural absence as signal).** *Designed restriction of signal emission in specific dimensions generates perceived value that cannot be replicated by signal addition in other dimensions.*

Veblen (1899) identified conspicuous consumption as a value-signaling mechanism; structural absence inverts this into conspicuous restriction. Commodity theory (Brock, 1968) and the scarcity principle (Cialdini, 2001) establish that scarcity enhances perceived value, but they treat scarcity as a unidimensional modifier. The structural limitation is that these accounts do not specify the cross-dimensional generation mechanism: restriction on one dimension (economic, experiential, social) produces a signal on a different dimension. The Hermes analysis in Section 4.1 demonstrates that the brand's A+ coherence grade derives not from what it emits but from what it withholds. Testable prediction: comparing perceived value of brands with designed dimensional restriction against brands with equivalent positive signal strength will reveal a value premium attributable to restriction that cannot be replicated through addition.

**Proposition 4 (Coherence type over coherence score).** *Brands with identical aggregate coherence scores exhibit different resilience properties depending on their coherence type (ecosystem, signal, identity, experiential asymmetry, incoherent).*

Traditional brand scorecards project multi-dimensional coherence onto a single scale — a form of spectral metamerism (Zharnikov, 2026e) where structurally different brands appear identical in lower-dimensional projection. The five-brand illustrative application in Section 4.2 reveals that coherence is not a continuum from low to high but a nominal classification with qualitatively distinct resilience mechanisms. Two brands scoring 7/10 on a conventional coherence metric may exhibit radically different responses to disruption: selective absorption (ecosystem) versus uniform transmission (signal). The structural limitation of single-score coherence metrics is that they are geometrically blind to this distinction. Testable prediction: grouping brands by coherence type and subjecting them to matched disruption events will reveal type-specific resilience patterns that aggregate coherence scores fail to predict.

**Proposition 5 (Conviction asymmetry).** *Evidence-free negative brand convictions are more resistant to disconfirmation than evidence-rich positive convictions.*

Kahneman & Tversky (1979) established that losses loom larger than equivalent gains in prospect theory. SBT extends this asymmetry to brand evidence: negative convictions formed without experiential data are structurally more stable than positive convictions formed with extensive experiential data, because the negative-conviction holder's spectral profile excludes the dimensions where disconfirming evidence would need to arrive. The experiential gate is effectively closed. The structural limitation of brand management strategies that attempt to "convert" hostile cohorts is that they target dimensions the cohort cannot perceive. Testable prediction: measuring the evidence required to shift convictions from positive-to-negative versus negative-to-positive will reveal a directional asymmetry, with negative-to-positive requiring substantially more — and dimensionally different — evidence.

These five propositions are not exhaustive predictions of SBT; they formalize the framework's most distinctive structural claims. The falsifiable hypotheses in Section 5.5 operationalize these and additional predictions into specific experimental designs.

---

## Illustrative Application

### 3.1 Design

To illustrate the framework's analytical architecture, we applied SBT to five brands selected to span the brand architecture space. This application is illustrative rather than empirical: it demonstrates how the framework's constructs operate in practice, not that the framework's propositions have been validated.

**Table 4.** Five case-study brands and selection rationale.

| Brand | Selection Rationale | Architecture Type |
|:------|:----------------------------------|:------------------|
| Patagonia | Mission-driven, ideological core, moderate scale | Identity coherence |
| Tesla | Maximum observer divergence, CEO-dominated signals | Incoherence |
| IKEA | Global consistency, designed-signal dominance | Signal coherence |
| Hermès | Scarcity-based luxury, structural absence strategy | Ecosystem coherence |
| Erewhon | Hyperlocal niche, mediated perception dominance | Experiential asymmetry |

The five brands were chosen to stress-test different properties of the framework: Patagonia tests ideological filtering; Tesla tests extreme observer divergence and ambient signal dominance; IKEA tests consistent signal architecture at global scale; Hermès tests scarcity-based value creation and cross-cohort interdependence; Erewhon tests the framework's minimum viable scale and mediated perception dynamics.

### 3.2 Analytical Pipeline

Each brand was analyzed through six sequential modules. The pipeline produces structured YAML output; each module's output feeds into subsequent modules:

1. **Brand Decomposition**: inventory of signals across all eight dimensions, source type classification, emission type classification, dimensional heat map
2. **Observer Mapping**: 3–5 observer cohort spectral profiles with weights, tolerances, encounter modes, and cross-cohort dependencies
3. **Cloud Prediction**: per-cohort perception clouds with confidence bands, valence, formation mode, and inter-cohort divergence mapping
4. **Coherence Audit**: seven-metric scorecard, overall grade (A+ through F), coherence type classification
5. **Emission Strategy**: target conviction map, dimensional redesign, D/A ratio optimization, phased action plan
6. **Re-collapse Simulation**: 2–3 disruption scenarios per brand, per-cohort resilience scoring, cascade risk assessment, defensive recommendations

The pipeline was executed using Claude Opus 4.6 (Anthropic) as the primary analytical engine, with structured prompts and YAML output templates ensuring consistency across brands. An important methodological clarification: the LLMs serve as *analytical instruments* — structured reasoning engines that apply the framework's constructs to publicly available brand information — not as *synthetic respondents* simulating consumer perception (cf. Brand, Israeli, & Ngwe, 2023; Horton, 2023; Goli & Singh, 2024 for the distinction between these two uses of LLMs in marketing research). The outputs reflect the framework's decomposition applied to public brand discourse, not predictions of how specific consumers would perceive these brands. A full cross-model replication was subsequently conducted using Gemini 3.1 Pro (Google) across all five brands to test for model-specific biases (see Section 3.4). Each module's output was assessed against four validation criteria: non-obvious (a brand strategist could not reach this through standard analysis), dimensionally specific (references specific dimensions and observer profiles), actionable (suggests concrete strategic changes), and observer-differentiated (shows how different cohorts perceive the same signals differently).

### 3.3 Insight Validation Protocol

Each brand analysis was followed by a structured insight assessment that evaluated the top findings against the four criteria. An insight was accepted only if it satisfied all four criteria simultaneously. Across five brands, 25 insights were assessed by the framework's author against four criteria; all 25 were judged to satisfy the criteria. Independent blind evaluation by practitioners not familiar with the framework would provide a stronger test. The four mechanisms reported in Section 4 were selected as the most novel — insights that could not have been produced by any existing brand framework because the existing frameworks lack the necessary vocabulary.

### 3.4 Limitations of the Illustrative Approach

The illustrative application has several methodological limitations. Observer weight assignments are expert estimates, not empirically measured; validation through conjoint analysis or behavioral experiments is needed. Cloud confidence scores are calibrated within each brand analysis but not across brands; confidence bands (weak/moderate/strong) are more defensible than cross-brand decimal comparison.

To test for model-specific biases, a full cross-model replication was conducted using Gemini 3.1 Pro (Google) across all five brands:

**Table 5.** Cross-model replication convergence: coherence type and grade.

| Brand | Claude Opus 4.6 | Gemini 3.1 Pro | Convergence |
|:------|:----------------|:----------------|:------------|
| Tesla | Incoherent, C- | Incoherent, C- | Identical |
| Hermès | Ecosystem, A+ | Ecosystem, A+ | Identical |
| Patagonia | Identity, B+ | Identity, B+ | Identical |
| IKEA | Signal, A- | Signal, A- | Identical |
| Erewhon | Exp. Asymmetry, B- | Exp. Asymmetry, B- | Identical |

Both models independently derived the structural absence mechanism for Hermes and the CEO ambient signal domination for Tesla. Model-sensitive findings were limited to cohort granularity (Claude: 5-6 cohorts per brand; Gemini: 3) and D/A ratio variance (within 10-15 percentage points). The structural diagnosis remains stable regardless of cohort resolution, though convergence may partly reflect shared training data for these well-documented brands. Replication with additional models, human analysts, and lesser-known brands would provide stronger validation.

Additional limitations include: (1) all five brands are well-known Western consumer brands — applicability to non-Western, B2B, or newly launched brands is untested; (2) the illustrative application uses SBT's own pipeline to produce the findings — independent validation against consumer survey data would be stronger; (3) the eight dimensions are a working decomposition, not a proven exhaustive set — empirical factor-analytic work (cf. J. Aaker, 1997; Brakus et al., 2009 for validated dimensional scales in adjacent constructs) would be needed to establish the dimensionality of the perceptual space; and (4) dimensional weights are treated as independent, but in practice dimensions may be correlated — an observer who weights ideological signals heavily may systematically discount economic signals. The spectral analogy is strongest when dimensions are approximately independent; if substantial inter-dimensional correlations exist, the effective dimensionality of the space is lower than eight, and the framework's precision claims would need adjustment.

### 3.5 Mathematical Foundations

The framework as presented in Sections 1-3 operates at the level of structured qualitative analysis. A natural question is whether the framework's core constructs — eight-dimensional brand space, observer spectral profiles, perception clouds — admit formal mathematical treatment. A series of companion working papers establishes that they do, addressing: formal Riemannian metrics on brand space; information-loss bounds under dimensionality reduction (spectral metamerism); concentration-of-measure results showing that cohort boundaries are inherently fuzzy in high-dimensional perception space; sphere-packing bounds on market capacity; stochastic diffusion models for non-ergodic conviction dynamics; optimal resource allocation given measured cohort weight profiles; and the empirical rate-distortion curve for AI brand perception encoders, which establishes that 1-5 ordinal scales minimize distortion from canonical profiles across 17 LLM architectures — the optimal operating point for AI-mediated brand measurement (Zharnikov, 2026aa).^[The companion papers are available as working papers at the Zenodo community page: zenodo.org/communities/spectral-branding.]

**The Gravitational Analogy.** SBT's perception space has a structural analog in general relativity. In GR, gravity is curvature of 4-dimensional space-time, described by a symmetric metric tensor with 10 independent components. In SBT's 8-dimensional perception space, the analogous object is the Fisher-Rao information metric: a symmetric 8x8 matrix with 36 independent components that determine how actual perceptual distances (measured by observer cohort agreement) differ from naive coordinate distances (measured by dimensional score differences). Brand emission intensity curves perception space and observer cohorts follow perceptual geodesics. A critical difference: in GR, all bodies follow the same geodesic regardless of mass (the equivalence principle). In SBT, different cohorts follow different geodesics because their spectral weight profiles determine which dimensions they are sensitive to — the geometry is observer-relative, not universal. The use of differential geometry to model perceptual space has a half-century pedigree in psychophysics: Resnikoff (1974) models perceived color space as a Riemannian manifold, and Koenderink and van Doorn (2012) formalize pictorial space as a fiber bundle where observer-dependent depth representations project from a shared visual field — the same mathematical architecture that SBT applies to brand perception.

**The Correspondence Principle.** The relationship between SBT and classical brand frameworks is analogous to the relationship between general relativity and Newtonian mechanics: the simpler framework is the limiting case of the richer one. When observer diversity is low — when all cohorts share similar spectral weight profiles — the fiber bundle collapses to a trivial bundle, perception space is approximately flat, and classical brand measurement frameworks (Keller, 1993; Aaker, 1996) are adequate. As observer diversity increases structurally — through globalization, AI-mediated perception, and digital fragmentation — the curvature becomes non-negligible and SBT's geometric tools become necessary. Table 6 summarizes this regime hierarchy.

**Table 6.** Correspondence between physical regimes and SBT measurement frameworks

| Physical regime | GR analog | SBT analog | Measurement framework |
|---|---|---|---|
| Weak field, uniform observers | Newtonian gravity | Classical brand measurement | Single observer, no triangulation needed |
| Curved space, uniform observers | GR with test particles | SBT with homogeneous cohorts | Fisher-Rao metric (Zharnikov, 2026d) describes geometry |
| Curved space, diverse observers | Electromagnetism in curved space | SBT with heterogeneous cohorts | Brand Triangulation (Zharnikov, 2026y) needed |
| Extreme curvature, dark signals | Black holes, dark matter | Structural absence, brand singularities | Full fiber bundle + dark signal detection |

**The Cross-Field Geometric Turn.** SBT's adoption of geometric methods — Fisher-Rao metric, geodesics, curvature — is not an idiosyncratic choice imported from physics. It mirrors an independent convergence across fields that discovered flat representations break when working with high-dimensional, AI-relevant data. In machine learning, Bronstein et al. (2021) demonstrated that the architectures that generalize across domains — CNNs, graph neural networks, transformers — are precisely those that preserve geometric structure rather than imposing flat coordinate representations on inherently curved data. In neuroscience, Ma et al. (2025) showed that the visual system transforms a 3-dimensional sensory manifold into a 7-dimensional perceptual manifold, providing direct empirical evidence that perception is not a linear readout but a geometric transformation — the brain encodes meaning by changing the shape of the representation space. In network science, Hansen and Ghrist (2021) applied sheaf theory to opinion dynamics, demonstrating that the consistency constraints governing how local opinions cohere into global positions are inherently topological rather than metric. SBT's geometric apparatus is a local instance of this broader convergence: across fields, high-dimensional heterogeneous data has forced the same methodological conclusion — flat representations destroy the structure that explains the phenomena.

---

## Findings

The five-brand illustrative application identified four candidate mechanisms that the framework's constructs make visible — phenomena that are difficult to articulate through existing brand frameworks because those frameworks lack the necessary vocabulary.

### 4.1 Structural Absence: Value Creation Through Designed Signal Restriction

**Illustrative context:** Hermès case study (Modules 1, 5).

Every brand framework in the literature assumes an emission model: design a signal, emit it, and measure whether it produces the desired perception. More signal generally means more perception. Broader distribution generally means broader awareness. The logic is additive.

Hermès inverts this logic entirely. The brand does almost nothing that brand strategy textbooks recommend. It does not advertise aggressively. It does not maximize reach. It does not hold sales. It does not sell its most iconic products online. It maintains wait lists measured in years. It operates approximately 300 stores worldwide.

By every standard metric of brand communication, Hermès should be weak. It scored A+ in our coherence audit — the highest grade in the study. Not despite the restrictions. Because of them.

We formalize this as **structural absence**: the deliberate withholding of signals that creates value through what is not emitted. The concept has precedent in semiotics — Eco (1976) analyzed how sign systems communicate through absence and overcoding — but has not been formalized as a brand strategy mechanism. The mechanism is analogous to dark matter in physics — invisible but gravitationally active, shaping the perception field without emitting observable signals.

SBT introduces a three-type emission taxonomy:

**Table 7.** Three emission types in the spectral model.

| Emission Type | Mechanism | Signal Present? | Example |
|:-------------|:-------------------------------|:----------------|:-------------------------------|
| Positive | Brand actively emits signal | Yes | Product launch, campaign |
| Null | Signal absent, unintentional | No (neglect) | Unused heritage, dormant dimension |
| Structural absence | Designed restriction functions as signal | No (strategy) | Wait list, no discounts, geographic scarcity |

The key mechanism is cross-dimensional: restriction on one dimension generates a signal on a different dimension. Economic restriction (never discounting) produces a social signal — the product exists outside normal market forces, inverting Veblen's (1899) conspicuous consumption from display of spending to display of access. Experiential restriction (in-store purchase only) produces an economic signal (difficulty of access justifies the price). Social restriction (purchase rituals, relationship requirements) produces an experiential signal (the restriction process *is* the brand experience).

Structural absence amplifies the perceived weight of present signals through contrast — a multiplicative mechanism in perception rather than additive. Hermes achieves the highest emission efficiency in the study (9/10) not by optimizing what it sends but by optimizing what it withholds.

**Dimensional constraints.** Structural absence does not operate on all dimensions. It operates primarily on social (exclusivity), economic (pricing discipline), and experiential (geographic scarcity) dimensions. It cannot operate on semiotic (there is no "absent logo" — visual identity requires presence) or narrative (the absence of a story is just absence — Hermès in fact has a rich narrative that *frames* the absence). This constraint is consistent with the finding that structural absence requires existing demand to restrict. The strategy is available only to brands with sufficient heritage and established desire to make the restriction legible as intention rather than failure.

**Prerequisite.** Our cross-brand comparison reveals that structural absence requires heritage legitimization. Hermès' 189 years of continuous operation makes its restrictions legible as "this is how we have always been" rather than "this is artificial scarcity." Brands without heritage depth cannot deploy structural absence at scale — the restriction is interpreted as arrogance, not tradition.

### 4.2 Five Types of Brand Coherence

**Illustrative context:** Cross-brand comparison (Module 4 across all five brands).

Traditional brand analysis treats coherence as a single variable from low to high: how consistently is the brand perceived across audiences? Our five-brand exploratory analysis suggests that coherence is not a single variable but a structural property that comes in five qualitatively distinct types, each with different resilience profiles.

**Table 8.** Five-type coherence taxonomy with resilience profiles.

| Coherence Type | Grade | Pattern | Resilience Profile | Brand |
|:--------------|:------|:--------------------------------------|:--------------------------------------|:------|
| Ecosystem | A+ | Different clouds reinforce through functional interdependence | Selective — absorbs disruption by purification | Hermès |
| Signal | A- | Consistent designed signals → consistent clouds | Uniform — transmits disruption evenly | IKEA |
| Identity | B+ | Ideological core filters cohort compatibility | Binary — divides along ideology | Patagonia |
| Experiential asymmetry | B- | Evidence gap between direct and mediated observers | Geographic — different impact by location | Erewhon |
| Incoherent | C- | Contradictory signals → irreconcilable clouds | Amplifying — widens existing cracks | Tesla |

The letter grades are projections of multi-dimensional spectral profiles onto a disruption resilience scale. Different structural types can project to the same grade (spectral metamerism) — a brand with 7/10 signal coherence (IKEA: everyone perceives the same thing) and 7/10 ecosystem coherence (Hermes: different cohorts perceive different things that reinforce each other) would appear identical on a single-variable dashboard. Their responses to disruption are radically different. Sorensen (2002) demonstrated across more than 200 firms that the structure of cultural alignment, not its intensity, determines outcomes; Chatman, Caldwell, O'Reilly, and Doerr (2014) extended this by showing that consensus combined with adaptability outperforms consensus alone.

**Ecosystem coherence** (Hermès) exhibits selective resilience. When the Hermès secondary market collapses in our simulation, the Investment Buyer cohort is destroyed — but the Heritage Client and Cultural Connoisseur are *strengthened*: "now the speculators are gone." The ecosystem metabolizes the disruption by sacrificing peripheral elements while purifying the core. This capacity for selective absorption is unique to ecosystem coherence and explains the extraordinary durability of brands that exhibit it.

**Signal coherence** (IKEA) exhibits uniform resilience. When disrupted, the impact transmits evenly across all cohorts because the same designed signals reach everyone. There is no selective absorption — a quality scandal affects every observer equally. Recovery requires system-wide signal correction, not targeted cohort management.

**Identity coherence** (Patagonia) exhibits binary resilience. The brand divides along ideological lines under stress. Aligned cohorts rally ("this proves they are authentic"). Misaligned cohorts deepen their indifference or opposition. The ideological core is either a magnet or a wall — there is no middle ground.

**Experiential asymmetry** (Erewhon) exhibits geographic resilience. Disruption affects local and mediated observers differently because their perception clouds are built on incompatible evidence bases. A food safety incident at the physical store devastates direct-experience observers but barely registers with the Instagram audience. A social media backlash against wellness culture devastates the mediated observers but leaves local regulars unaffected.

**Incoherence** (Tesla) exhibits amplifying fragility. Each disruption widens existing cracks. The system does not absorb disruption — it converts disruption into deeper division. This is the worst resilience profile in the taxonomy.


The coherence type is determined by three structural properties: (1) cohort interdependence — how much one cohort's perception depends on another's behavior; (2) ideological centrality — how much coherence depends on a shared ideological commitment; and (3) encounter mode variance — how different the direct-encounter brand is from the mediated brand.


**Figure 4.** Coherence Types: Disruption Response Patterns

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

**Illustrative context:** Tesla case study (Modules 2, 3, 6).

Our analysis of Tesla revealed a counterintuitive structural property of brand perception: evidence-free negative convictions can be more stable than evidence-rich positive ones.

The Tesla Progressive Boycotter cohort holds a brand conviction with .82 confidence (classified as "strong"). This conviction is constructed from an ideological weight of .45 and a social weight of .20 — but an experiential weight of only .03. The Boycotter has never driven a Tesla, never visited a showroom, never used a Supercharger. Their entire brand perception is constructed from ambient ideological and social signals encountered through screens.

The Tesla Tech Loyalist, who drives the car daily and has extensive product data, holds a conviction with .78 confidence — lower than the Boycotter's.

The person with the most evidence has less certainty than the person with the least.

This is not a cognitive error. It is a structural property of spectral perception. The Boycotter's conviction is uncontested because there is no experiential data to create cognitive dissonance (Festinger, 1957). The ideological signal points in one direction. The social signal confirms it. No product encounter introduces nuance. The conviction is coherent *because* it is evidence-free.

The Loyalist, by contrast, has real product data. They know the car is excellent. They also know the service centers can be frustrating. They have experienced the gap between Autopilot promises and delivery. Their conviction includes contradictions — the somatic markers of mixed emotional experience (Damasio, 1994) create ambivalence that pure ideological conviction never encounters. Evidence-rich convictions are inherently less certain than evidence-free ones because they contain more dimensions that can produce ambiguity.

This asymmetry has a critical resilience implication. In our disruption simulations, negative convictions consistently *strengthen* under brand stress, while positive convictions *weaken*. A brand crisis confirms what the negative-conviction holder already believed. But it introduces contradicting evidence for the positive-conviction holder, who must now reconcile their favorable experience with unfavorable news. The asymmetry is directional: positive → negative is far easier than negative → positive, because the latter requires experiential evidence that the negative-conviction holder's spectral profile is designed to exclude.

The strategic implication is stark: resources spent attempting to convert structurally locked negative cohorts are wasted. The Boycotter's experiential gate is effectively closed (.03 weight). No test drive campaign will reach them because they are not evaluating the product — they are evaluating the ideology. Brands with locked negative cohorts must accept the structural constraint and invest in addressable cohorts instead.

**Table 9.** Asymmetric conviction resilience (Tesla case): evidence-rich Loyalist vs. evidence-free Boycotter.

| | **Tech Loyalist** | **Progressive Boycotter** |
|:--|:--|:--|
| **Top weights** | Experiential: .35, Economic: .20 | Ideological: .45, Social: .20 |
| **Experiential** | .15 (extensive product data) | .03 (no product contact) |
| **Confidence** | .78 (mixed signals = ambivalence) | .82 (no contradiction = certainty) |
| **Crisis effect** | Weakens (new evidence conflicts) | Strengthens (confirms prior belief) |

### 4.4 Brand Power and Brand Health as Independent Variables

**Illustrative context:** Cross-brand comparison (Module 4 across all five brands).

The five-brand exploratory analysis produces a finding that inverts conventional brand wisdom: brand power (emission strength, awareness, cultural impact) and brand health (coherence, architectural integrity, resilience) are independent variables. A brand can maximize the first while minimizing the second.


**Table 10.** Five-brand scorecard: brand power versus spectral health.

| Brand | Power | Health | D/A | Gap |
|:----------|:------------------------------|:----------|:------|:------------------------|
| Tesla | Highest (universal awareness) | C- | 30/65 | Maximum inversion |
| Hermès | Moderate (niche, restricted) | A+ | 60/35 | Architecture > awareness |
| IKEA | High (global, ubiquitous) | A- | 75/25 | Consistent alignment |
| Patagonia | Moderate (category-bound) | B+ | 65/30 | Ideological filter |
| Erewhon | Low-moderate (hyperlocal) | B- | 40/55 | Scale floor |

Traditional frameworks — BrandAsset Valuator (BAV), Interbrand's brand strength methodology, Keller's brand equity pyramid — measure dimensions of power: differentiation, relevance, esteem, knowledge, awareness, consideration. By these metrics, Tesla is among the world's most valuable brands. Seven of eight dimensions emit at strength 4 or higher. Gate permeability is 10/10 — everyone knows the brand.

But the spectral scorecard reveals Tesla's cloud coherence at 2/10, its designed/ambient ratio at 30/65, and its re-collapse resistance at 4/10. Maximum emission power, minimum architectural health.

The confusion between brand power and brand health is, we argue, the central error in traditional brand management. It leads to the systematic misdiagnosis of brands like Tesla (perceived as "strong" when structurally fragile) and the systematic undervaluation of brands like Hermès (perceived as "niche" when architecturally impregnable).

The D/A ratio is the single metric that most powerfully discriminates between power and health. Our five-brand comparison tentatively suggests a possible optimal zone around 55–65% designed signals; this is an exploratory hypothesis requiring validation across a larger sample. High enough to maintain narrative control. Low enough to allow authentic ambient reinforcement. Tesla, at 30% designed, is 25 points below the floor of this zone — meaning no communication strategy can fix its brand problem because 65% of the signal environment is beyond its control. Hermès, at 60% designed with *aligned* ambient signals, demonstrates that the direction of ambient signals matters as much as the ratio: its ambient signals amplify rather than contradict its designed signals.


**Figure 5.** D/A Ratio and Coherence Across Five Brands

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

## Discussion

### 5.1 Relationship to Existing Frameworks

SBT does not replace existing brand frameworks. It formalizes the observer-mediated layer that each identifies but none parameterizes.

Aaker's (1991, 1996) brand equity and identity systems describe what the brand intends to emit but lack the observer model that explains why the same identity produces different perceptions in different cohorts. Aaker's four perspectives — Brand as Product, Organisation, Person, Symbol — each bundle multiple perceptual channels that SBT decomposes into eight parameterized dimensions. Kapferer's (2008) prism comes closest to SBT's dimensional approach, with its six facets mapping loosely to SBT's eight dimensions, but treats the facets as brand properties rather than observer-dependent perceptual channels. Keller's (1993) customer-based brand equity is the most direct predecessor: equity lives in the customer's mind, brand knowledge equals awareness plus image. SBT extends Keller by modeling the customer as a heterogeneous population, formalizing the perception-to-conviction pipeline, and introducing the re-collapse mechanism. Existing dimensional approaches to brand perception — J. Aaker's (1997) five personality dimensions, Kervyn, Fiske, and Malone's (2012) warmth-competence space, Brakus, Schmitt, and Zarantonello's (2009) four experience dimensions, Yoo and Donthu's (2001) multi-dimensional CBBE scale, and Keller's (2001) brand resonance pyramid — each decompose brand meaning into measurable sub-constructs but treat the dimensions as brand attributes rather than observer-mediated perceptual channels. SBT's contribution relative to these predecessors is not the dimensional decomposition itself but the formal parameterization of the observer as a first-class object whose spectral profile determines which dimensions are perceived and how they are weighted. Recent extensions — France, Davcik, and Kazandjian's (2025) digital brand equity framework, Guhl's (2024) time-varying utility-based brand equity, and Lambrecht, Baumgarth, and Henseler's (2025) augmented reality brand equity model — demonstrate growing recognition that brand equity is multi-dimensional and context-dependent; SBT provides the observer-mediated architecture within which these extensions operate.

Fournier (1998) established that consumers form qualitatively different relationship types with brands — a direct precursor to SBT's observer-specific convictions. Hatch & Schultz (2010) anticipated SBT's observer-as-co-creator thesis. Swaminathan, Stilley & Ahluwalia (2009) demonstrate that individual differences moderate brand personality effects — direct evidence for observer heterogeneity. Xi, Yang, Jiao, Wang, and Lu (2022) show that consumer perceived value drives brand identity formation in the luxury sector, providing empirical support for the observer's role in constructing brand meaning. Park, MacInnis & Priester (2010) distinguish brand attachment from brand attitude strength — a distinction SBT captures as cloud stability versus collapse confidence.

Muniz and O'Guinn's (2001) brand community construct identifies the social dimension as a self-organizing perceptual system. Sharp's (2010) empirical challenge to brand differentiation is complementary: Sharp describes acquisition (passing the identity gate widely); SBT describes what happens *after* the gate — how different observers form different convictions. Vargo & Lusch's (2004) service-dominant logic anticipated the co-creation premise; Merz, He, and Vargo (2009) trace brand theory through four eras culminating in stakeholder co-creation, the trajectory SBT formalizes through parameterized observer profiles. Lakoff's (2004) cognitive frames provide a complementary mechanism: priors function as frames that pre-structure which signals are perceived as relevant.

Gestalt psychology (Koffka, 1935) provides the perceptual foundations: cloud formation *is* gestalt perception applied to brand signals. Kahneman's (2011) dual-process theory maps to the collapse mechanism: strong convictions are System 1 shortcuts; weak or forming clouds require effortful System 2 processing.


**Figure 6.** Non-Ergodic Brand Perception: Ensemble Average vs. Cohort Trajectories

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
     |                          X  <- Trajectories cross:
   2 |                         / \    ensemble stays flat,
     |               /--------/   \   cohorts diverge
   0 |  Boycotter --/              \---------\-----------
     +----+----+----+----+----+----+----+----+----+----+----> Time
     t0        t1        t2        t3        t4
          Signal  Crisis   Recovery  New
          shift   event    attempt   equilibrium

     Ensemble average = 6 throughout (misleading stability)
     Individual cohorts: 0 to 8 range (actual dynamics)
```

Peters' (2019) ergodicity economics provides an organizing analogy. In multiplicative, path-dependent processes, ensemble averages diverge systematically from time averages (Doctor, Wakker, & Wang, 2020; Meder et al., 2021). SBT's finding that brand power (an ensemble measure) and brand health (a time-average measure) are independent variables is a structural parallel. The asymmetric conviction resilience finding (Section 4.3) maps to absorbing states in non-ergodic processes: once a negative conviction crosses a threshold with no experiential friction to reverse it, the observer is on a one-directional trajectory. We use this analogy as an organizing framework, not as a claim that brand perception obeys the specific mathematical properties Peters demonstrates for wealth processes.

Attitude strength research (Krosnick & Petty, 1995) establishes that strong attitudes resist change. SBT extends this by specifying the dimensional pathway: evidence-free convictions resist counter-evidence because the observer's spectral profile excludes the dimensions where counter-evidence exists. Commodity theory (Brock, 1968) and scarcity research (Cialdini, 2001; Lynn, 1991) establish that scarcity enhances perceived value. SBT's structural absence mechanism formalizes the cross-dimensional generation pathway and its prerequisites (existing demand and heritage context).

SBT does not capture everything existing frameworks do. Sharp's (2010) empirical regularities — double jeopardy, negative binomial distribution of purchase frequency — describe aggregate market-level patterns that SBT's cohort-level architecture does not address; these phenomena may emerge from the cohort dynamics SBT models but the framework does not predict them. Similarly, the rich phenomenological detail of Fournier's (1998) relationship theory — brand relationships as lived narratives — is reduced to parameter values in SBT's observer profiles. The framework trades phenomenological richness for computational tractability.

In sum, SBT contributes a unifying vocabulary that connects the sender-side frameworks (Aaker, Kapferer), receiver-side frameworks (Keller), acquisition frameworks (Sharp), and process frameworks (cognitive science, ergodicity economics) as complementary descriptions of different stages in a single perception pipeline. The formal criterion for construct validity — that variation in the attribute causally produces variation in the measurement outcome (Borsboom, Mellenbergh and van Heerden 2003) — is satisfied by spectral profiles only when the instrument preserves dimensional structure. Aggregated metrics fail this criterion by design.

### 5.2 Computational Implementability

The closest computational precedent is Colladon's (2018) Semantic Brand Score (SBS), which extracts three network-based dimensions from text data. SBS measures brand *importance* in discourse networks — a salience metric. SBT measures brand *perception* across eight qualitative dimensions — a content metric. More broadly, the emerging computational branding literature — including Barari and Eisend's (2024) computational content analysis and Sarstedt, Brand, and Ring's (2024) investigation of LLMs as survey respondents — demonstrates growing recognition that brand analysis can be formalized and automated. Nguyen (2026) provides cross-national evidence that AI-generated advertising produces measurable effects on brand perception, further validating the computational approach. SBT extends this trajectory from computational *measurement* of existing constructs to computational *execution* of a formal perceptual theory.

SBT's constructs map directly to computational primitives: signals are typed data structures, observer profiles are parameter sets, cloud formation is a weighted clustering operation, and conviction collapse is a threshold function. The analytical pipeline operates as a structured prompt sequence for large language models, producing signal inventories, cohort profiles, perception cloud predictions, coherence scorecards, and disruption simulations. The prompt kit and YAML output templates are available from the corresponding author.

### 5.3 AI-Mediated Brand Perception

The AI era changes brand perception in three ways that SBT's architecture accommodates. First, **AI as analytical engine**: LLMs can execute multi-dimensional, multi-cohort brand analysis that would overwhelm human cognition, making frameworks of SBT's complexity operational. Second, **AI as mediation layer**: algorithms increasingly filter which signals reach which observers — an extension of McLuhan's (1964) thesis — functioning as spectral filters with their own dimensional biases. Third, **AI as synthetic observer**: LLM-powered recommendation systems constitute a new observer class with their own spectral profile (biased toward economic and semiotic signals, weak on narrative, cultural, and temporal dimensions; Zharnikov 2026v), increasingly influencing human purchase decisions.

These shifts are recognized in the emerging literature. Davenport, Guha, Grewal, and Bressgott (2020) identify AI as transforming marketing from segmented to individualized. Huang and Rust (2021) predict which marketing functions AI will subsume. Puntoni, Reczek, Giesler, and Simester (2021) analyze how consumers experience AI as threatening to their autonomy — perceptual reactions that SBT models as observer-profile shifts in the ideological and social dimensions. The observer model's encounter modes (direct, mediated, mixed) and the signal taxonomy's synthetic source type accommodate these developments without retrofitting.

Supplementary experiments provide initial empirical grounding for these predictions. A simulated 3-step agentic shopping pipeline (retrieval, comparison, recommendation) across 6 LLM architectures showed that dimensional collapse compounds across pipeline steps (*F* = 4.298, *p* = .015, eta-sq = .029), with Narrative and Cultural dimensions losing the most weight while Economic gains (Zharnikov 2026v, Section 5.13). The compounding effect is small but systematic — no model-specific differences were observed (*p* = .152) — suggesting that collapse is an architectural property of statistical language modeling, not an artifact of any particular training corpus.

### 5.4 Limitations and Future Directions

Several limitations warrant discussion. The open questions identified below concerning non-ergodic dynamics, cohort boundary formalization, and resource allocation now have formal mathematical treatment in the companion papers described in Section 3.5. The limitations discussed here concern empirical validation, which remains for future work.

**Weight validation.** Observer dimensional weights are currently expert estimates. Empirical validation through conjoint analysis, behavioral experiments, or large-scale survey data would strengthen the framework's credibility. The specific values assigned in the illustrative application were selected for analytical clarity; different weight assumptions would produce different outputs.

**Cross-brand calibration.** Cloud confidence scores and coherence metrics are calibrated within each brand analysis but not across brands. Developing calibration benchmarks across brand categories is a priority for future work.

**Temporal dynamics.** The framework captures snapshots but does not formally model rates of change. Two temporal properties require formalization: (1) *signal decay* — how signal contributions attenuate over time, varying by emotional intensity and encounter mode; and (2) *cohort velocity* — conviction migration speed for longitudinal tracking. Du and Kamakura (2015) demonstrate that dynamic factor analysis can separate true brand movement from measurement drift — a methodology applicable to cohort-level velocity aggregation in the spectral setting.

**Competitive analysis.** An empirical test of competitive interference across 5 focal brands paired with direct, adjacent, and distant competitors found null effects on all hypotheses (largest *d* = .187, all *p* > .05 after Bonferroni correction; Zharnikov 2026g, Section 10.5). Brands occupy stable positions in perception space regardless of competitive context, supporting the fixed-geometry assumptions of the framework. The limitation remains that these tests used LLM observers only; human-subject competitive interference remains untested.

**Temporal compounding.** Heritage compounds non-linearly. Urde, Greyser, and Balmer (2007) formalize brand heritage as a strategic resource; Brown, Kozinets, and Sherry (2003) demonstrate through retrobranding that heritage signals can be deliberately reconstructed. Taleb's (2007) analysis of path-dependent processes provides a framework for modeling how small early signals compound into structural priors that resist correction — the non-ergodic dynamics formalized in Proposition 2.

**Non-ergodic dynamics.** Brand perception operates as a multiplicative, path-dependent process, making it structurally non-ergodic in Peters' (2019) sense. Introducing an ergodicity coefficient per brand-dimension pair — measuring the degree to which ensemble metrics reliably predict individual cohort trajectories — would identify which dimensions can be safely measured with aggregate surveys and which require longitudinal cohort-trajectory tracking.

**Resource allocation.** The framework identifies *what* observers perceive but does not specify *where* operational investment should be directed. Companion work on spectral resource allocation formalizes optimal dimensional investment given measured cohort weight profiles.

**Admissibility versus coherence.** The coherence taxonomy measures internal consistency — whether brand signals align with each other. A complementary concept is *admissibility*: whether the brand's current position falls within the region its specification defines as acceptable. A brand can exhibit perfect coherence while operating in an inadmissible state. This distinction parallels the difference between *state invariance* and *process invariance* formalized in geometric governance frameworks (Medesani & Macdonald, 2026), where invariant corridors preserve system integrity through constraining the *evolution* of the system under stress. Extending the coherence hierarchy with an admissibility criterion would enable the framework to distinguish between brands that are coherently positioned correctly and brands that are coherently positioned incorrectly.

### 5.5 Falsifiable Hypotheses

The framework generates ten falsifiable hypotheses. H1–H5 derive from the perception-layer mechanisms reported in Section 4. H6–H10 address pre-encounter mechanics — how brand signals reach observers.

**H1 (D/A Goldilocks zone).** Brands with 55–65% designed signals will show higher brand equity and disruption resilience than brands outside this range, controlling for category, age, and market position. *Derivation:* the five-brand D/A comparison (Section 4.4, Figure 5) shows the highest-health brands clustered in this range. *Test:* cross-sectional study of 50+ brands with empirically measured D/A ratios and brand equity scores (e.g., BAV, Interbrand, or bespoke spectral health metrics).

**H2 (Asymmetric conviction resilience).** Evidence-free negative brand convictions will show higher resistance to counter-evidence than evidence-rich positive convictions. *Derivation:* the Tesla Boycotter/Loyalist asymmetry (Section 4.3, Table 9). *Test:* controlled experiment — expose participants with no product experience and participants with extensive product experience to counter-attitudinal brand information; measure pre/post conviction change magnitude.

**H3 (Coherence type predicts disruption response).** Ecosystem-coherent brands will exhibit selective disruption absorption (periphery sacrificed, core strengthened); incoherent brands will exhibit disruption amplification (existing divisions widen). *Derivation:* the five-type coherence taxonomy (Section 4.2, Figure 4). *Test:* longitudinal cohort tracking before and after documented brand crisis events; compare per-cohort resilience trajectories across coherence types.

**H4 (Non-ergodic gap).** For incoherent brands, cross-sectional brand surveys will systematically overstate cohort-level resilience relative to longitudinal individual-level tracking. For signal-coherent brands, the gap will be minimal. *Derivation:* the brand power/health independence finding (Section 4.4) and the non-ergodic organizing analogy (Section 5.1, Figure 6). *Test:* paired study — compare snapshot survey scores to individual panel tracking data for the same brand across incoherent versus signal-coherent types.

**H5 (Structural absence prerequisite).** Structural absence strategies (designed signal restriction) generate positive scarcity signals only when two conditions are met: (a) existing demand for the restricted dimension, and (b) a legitimizing heritage context that makes restriction legible as intention rather than incapacity. *Derivation:* the Hermès structural absence mechanism (Section 4.1). *Test:* experiment — manipulate scarcity (present vs. absent) crossed with demand level (high vs. low) and heritage context (established vs. novel); measure perceived exclusivity versus perceived arrogance.

**H6 (Gate friction varies by cohort).** Identity gate friction for a given brand will differ significantly across observer cohorts, with cohorts whose dominant dimensions match the brand's strongest emission dimensions showing lower gate friction. *Derivation:* the identity gate mechanism (Section 3.3) combined with dimensional weight heterogeneity across cohorts. *Test:* exposure experiment — present brand cues to cohorts with different spectral profiles; measure recognition threshold (number of exposures to achieve recognition).

**H7 (First-atom primacy).** The dimensional content of the first brand atom encountered will disproportionately determine the observer's initial spectral profile, persisting as a prior even after subsequent atoms provide evidence on other dimensions. *Derivation:* the prior formation mechanism (Section 3.3) and non-ergodic path dependence (Section 5.1). *Test:* experiment — expose different groups to different "first atoms" (experiential versus semiotic versus ideological); measure resulting spectral profiles after equal total exposure. Preliminary evidence supports this prediction in the LLM observer case. A serial position experiment across 4 elicitation formats and 5 LLM architectures found that the first-listed dimension receives +6.1 weight points above the last-listed dimension in JSON format (*d* = 1.39, *p* < .001), with similar magnitudes in natural-language and ranking formats. The effect is virtually eliminated by independent Likert ratings (*d* = .22), which remove the sequential allocation mechanism that amplifies positional primacy (Zharnikov 2026v, Section 5.15). This suggests that H7's first-atom effect operates through the encoding format, not the perceptual content itself — a distinction the original hypothesis did not make.

**H8 (Amplification asymmetry).** Confirmed observers with negative-valence brand facts will have higher amplification rates (secondary emission volume) than those with positive-valence facts, creating faster signal field population for negative atoms. *Derivation:* the asymmetric conviction resilience finding (Section 4.3). *Test:* track secondary emission behavior (reviews, social posts, word-of-mouth) for positive versus negative Confirmed observers; measure volume and reach of emitted ambient atoms.

**H9 (Channel-dimension coupling).** Specific channels show systematic dimensional bias in atom transmission — for example, social media transmits semiotic and social dimensions at high fidelity but experiential at low fidelity; direct encounters transmit experiential at high fidelity but ideological at low fidelity. *Derivation:* the mediated cloud formation finding (Section 4.3) and channel fidelity concept (Section 3.5). *Test:* compare spectral profiles of observers who encountered the same brand through different channels; measure dimensional variance attributable to channel.

**H10 (Field density threshold).** There exists a minimum signal field density below which encounter probability drops to near-zero regardless of observer receptivity, and this threshold is higher for channels with low signal-to-noise ratio. *Derivation:* the signal dissemination layer (Section 3.5) and Sharp's (2010) mental availability framework. *Test:* vary brand signal frequency in controlled environments; measure encounter rate as a function of field density and channel noise level.


**Figure 7.** Research Agenda: Falsifiable Hypotheses and Testing Methods

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

A program that validates H1–H10 would move SBT from an exploratory framework to a quantitatively grounded theory of brand perception across the full lifecycle.

The eight spectral dimensions are a coordinate system for perception space, not a claim about natural perceptual kinds. The framework's primary contribution is the measurement infrastructure — observer cohorts with measurable spectral weights, the metamerism formalism, and coherence metrics — which enables geometric brand positioning independently of the specific dimensional decomposition. The claim is not that eight is the true dimensionality of brand perception but that eight provides the resolution necessary for reliable multi-observer positioning — a quantity we term Perception DOP (Dilution of Precision), analogous to GPS satellite geometry quality. Fewer dimensions produce unacceptably high DOP; additional dimensions yield diminishing returns. This framing transforms the "why eight?" question into an empirical test: eight is justified if the marginal reduction in Perception DOP from adding a ninth dimension falls below a significance threshold.

---

## Conclusion

Spectral Brand Theory contributes a formal, computational framework for modeling brand perception as an observer-mediated process. The core claim — there is no brand-in-itself, only signals and observers — produces an analytical architecture that explains phenomena traditional frameworks cannot: how the same brand can be simultaneously powerful and fragile (Tesla), how restricting signals can create more value than emitting them (Hermès), how five qualitatively different types of brand coherence determine resilience profiles that a single coherence score cannot distinguish, and how evidence-free convictions can be more stable than evidence-rich ones.

The five formal propositions and ten falsifiable hypotheses establish a concrete research agenda spanning cross-sectional brand studies, controlled signal-sequence experiments, and longitudinal cohort tracking. The illustrative application across five brands demonstrates that the framework's constructs operate coherently across luxury, mass-market, mission-driven, technology, and hyperlocal categories, though independent validation with primary consumer data is required to confirm the framework's explanatory value.

The framework's computational implementability — executable as a structured LLM prompt sequence — makes multi-cohort brand analysis accessible to practitioners without custom engineering.

SBT is not a replacement for strategic judgment. It is an analytical instrument — an X-ray machine for brand architecture. It sees the structure. The strategist decides what to build.

---

## Author Note

Dmitry Zharnikov is an independent researcher and strategist. He holds a Professional MBA (Entrepreneurship & Innovation) from Technische Universitat Wien and Wirtschaftsuniversitat Wien (dual degree, 2018). ORCID: https://orcid.org/0009-0000-6893-9231

---

## Acknowledgments

AI assistants (Claude Opus 4.6, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

---

## References

Aaker, D. A. (1991). *Managing brand equity: Capitalizing on the value of a brand name*. Free Press.

Aaker, D. A. (1996). *Building strong brands*. Free Press.

Aaker, J. L. (1997). Dimensions of brand personality. *Journal of Marketing Research*, 34(3), 347–356.

Alba, J. W., & Hutchinson, J. W. (1987). Dimensions of consumer expertise. *Journal of Consumer Research*, 13(4), 411–454.

Barari, M., & Eisend, M. (2024). Computational content analysis of brand communications: A review and research agenda. *International Journal of Research in Marketing*, 41(1), 24–47.

Borsboom, D., Mellenbergh, G. J., & van Heerden, J. (2003). The theoretical status of latent variables. *Psychological Review*, 110(2), 203–219. https://doi.org/10.1037/0033-295X.110.2.203

Ambler, T. (2003). *Marketing and the bottom line: The marketing metrics to pump up cash flow* (2nd ed.). Financial Times/Prentice Hall.

Barthes, R. (1957). *Mythologies*. Seuil.

Berger, J. (2013). *Contagious: Why things catch on*. Simon & Schuster.

Brown, S., Kozinets, R. V., & Sherry, J. F., Jr. (2003). Teaching old brands new tricks: Retro branding and the revival of brand meaning. *Journal of Marketing*, 67(3), 19–33.

Brakus, J. J., Schmitt, B. H., & Zarantonello, L. (2009). Brand experience: What is it? How is it measured? Does it affect loyalty? *Journal of Marketing*, 73(3), 52–68.

Brand, J., Israeli, A., & Ngwe, D. (2023). Using LLMs for market research. *Harvard Business School Working Paper*, No. 23-062.

Brock, T. C. (1968). Implications of commodity theory for value change. In A. G. Greenwald, T. C. Brock, & T. M. Ostrom (Eds.), *Psychological foundations of attitudes* (pp. 243–275). Academic Press.

Bronstein, M. M., Bruna, J., Cohen, T., & Velickovic, P. (2021). Geometric deep learning: Grids, groups, graphs, geodesics, and gauges. arXiv preprint 2104.13478.

Carroll, J. D., & Chang, J. J. (1970). Analysis of individual differences in multidimensional scaling via an N-way generalization of Eckart-Young decomposition. *Psychometrika*, 35(3), 283–319.

Colladon, A. F. (2018). The Semantic Brand Score. *Journal of Business Research*, 88, 150–160.

Connelly, B. L., Certo, S. T., Ireland, R. D., & Reutzel, C. R. (2011). Signaling theory: A review and assessment. *Journal of Management*, 37(1), 39–67.

Chatman, J. A., Caldwell, D. F., O'Reilly, C. A., & Doerr, B. (2014). Parsing organizational culture: How the norm for adaptability influences the relationship between culture consensus and financial performance in high-technology firms. *Journal of Organizational Behavior*, 35(6), 785–808.

Christodoulides, G., & de Chernatony, L. (2010). Consumer-based brand equity conceptualization and measurement. *International Journal of Market Research*, 52(1), 43–66.

Cialdini, R. B. (2001). *Influence: Science and practice* (4th ed.). Allyn & Bacon.

Damasio, A. R. (1994). *Descartes' error: Emotion, reason, and the human brain*. Putnam.

Davenport, T., Guha, A., Grewal, D., & Bressgott, T. (2020). How artificial intelligence will change the future of marketing. *Journal of the Academy of Marketing Science*, 48(1), 24–42.

Du, R. Y., & Kamakura, W. A. (2015). Improving the statistical performance of tracking studies based on repeated cross-sections with primary dynamic factor analysis. *International Journal of Research in Marketing*, 32(1), 94–112. https://doi.org/10.1016/j.ijresmar.2014.10.002

Dawar, N., & Parker, P. (1994). Marketing universals: Consumers' use of brand name, price, physical appearance, and retailer reputation as signals of product quality. *Journal of Marketing*, 58(2), 81–95.

De Chernatony, L., & McDonald, M. (2003). *Creating powerful brands*. Butterworth-Heinemann.

Doctor, J. N., Wakker, P. P., & Wang, T. V. (2020). Economists' views on the ergodicity problem. *Nature Physics*, 16, 1168.

Eco, U. (1976). *A theory of semiotics*. Indiana University Press.

Erdem, T., & Swait, J. (1998). Brand equity as a signaling phenomenon. *Journal of Consumer Psychology*, 7(2), 131–157.

Ehrenberg, A. S. C., Goodhardt, G. J., & Barwise, T. P. (1990). Double jeopardy revisited. *Journal of Marketing*, 54(3), 82–91.

Feldwick, P. (1996). What is brand equity anyway, and how do you measure it? *Journal of the Market Research Society*, 38(2), 85–104.

Festinger, L. (1957). *A theory of cognitive dissonance*. Stanford University Press.

Flake, J. K., & Fried, E. I. (2020). Measurement schmeasurement: Questionable measurement practices and how to avoid them. *Advances in Methods and Practices in Psychological Science*, 3(4), 456–465. https://doi.org/10.1177/2515245920952393

Fournier, S. (1998). Consumers and their brands: Developing relationship theory in consumer research. *Journal of Consumer Research*, 24(4), 343–373.

Floch, J.-M. (1990). *Semiotics, marketing and communication: Beneath the signs, the strategies*. Palgrave Macmillan.

Fournier, S., & Lee, L. (2009). Getting brand communities right. *Harvard Business Review*, 87(4), 105–111.

France, S. L., Davcik, N. S., & Kazandjian, B. J. (2025). Digital brand equity: The concept, antecedents, measurement, and future development. *Journal of Business Research*, 192.

Fishbein, M., & Ajzen, I. (1975). *Belief, attitude, intention and behavior: An introduction to theory and research*. Addison-Wesley.

Green, P. E., & Srinivasan, V. (1978). Conjoint analysis in consumer research: Issues and outlook. *Journal of Consumer Research*, 5(2), 103–123.

Goli, A., & Singh, A. (2024). Frontiers: Can large language models capture human preferences? *Marketing Science*, 43(4), 709–722.

Grier, S. A., & Brumbaugh, A. M. (1999). Noticing cultural differences: Ad meanings created by target and non-target markets. *Journal of Advertising*, 28(1), 79–93.

Guhl, D. (2024). Tracking time-varying brand equity using household panel data. *Journal of Business Research*, 182, 114799.

Hansen, J., & Ghrist, R. (2021). Opinion dynamics on discourse sheaves. *SIAM Journal on Applied Mathematics*, 81(5), 2033–2060. doi:10.1137/20M1341088

Hatch, M. J., & Schultz, M. (2010). Toward a theory of brand co-creation with implications for brand governance. *Journal of Brand Management*, 17(8), 590–604.

Hogarth, R. M., & Einhorn, H. J. (1992). Order effects in belief updating: The belief-adjustment model. *Cognitive Psychology*, 24(1), 1–55.

Holt, D. B. (2004). *How brands become icons: The principles of cultural branding*. Harvard Business Press.

Horton, J. J. (2023). Large language models as simulated economic agents: What can we learn from homo silicus? *NBER Working Paper*, No. 31122.

Huang, M.-H., & Rust, R. T. (2021). A strategic framework for artificial intelligence in marketing. *Journal of the Academy of Marketing Science*, 49(1), 30–50.

Kahneman, D. (2011). *Thinking, fast and slow*. Farrar, Straus and Giroux.

Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-291.

Kapferer, J.-N. (2008). *The new strategic brand management* (4th ed.). Kogan Page.

Keller, K. L. (2001). Building customer-based brand equity: A blueprint for creating strong brands. *Marketing Science Institute Report*, No. 01-107.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1–22.

Keller, K. L., & Lehmann, D. R. (2006). Brands and branding: Research findings and future priorities. *Marketing Science*, 25(6), 740–759.

Kervyn, N., Fiske, S. T., & Malone, C. (2012). Brands as intentional agents framework: How perceived intentions and ability can map brand perception. *Journal of Consumer Psychology*, 22(2), 166–176.

Kirmani, A., & Rao, A. R. (2000). No pain, no gain: A critical review of the literature on signaling unobservable product quality. *Journal of Marketing*, 64(2), 66–79.

Koenderink, J. J., & van Doorn, A. J. (2012). Gauge fields in pictorial space. *SIAM Journal on Imaging Sciences*, 5(4), 1213–1233. DOI: 10.1137/120861151

Koffka, K. (1935). *Principles of Gestalt psychology*. Harcourt, Brace.

Krosnick, J. A., & Petty, R. E. (1995). Attitude strength: An overview. In R. E. Petty & J. A. Krosnick (Eds.), *Attitude strength: Antecedents and consequences* (pp. 1–24). Erlbaum.

Lakoff, G. (2004). *Don't think of an elephant!* Chelsea Green.

Lambrecht, A., Baumgarth, C., & Henseler, J. (2025). Holistic augmented reality brand equity (HARBE) model: Building customer-based brand equity through augmented reality. *Journal of Brand Management*, 32, 298–314.

Lynn, M. (1991). Scarcity effects on value: A quantitative review of the commodity theory literature. *Psychology & Marketing*, 8(1), 43–57.

Ma, H., Jiang, L., Liu, T., & Liu, J. (2025). From sensory to perceptual manifolds: The twist of neural geometry. *Science Advances*, 11(26):eadv0431. doi:10.1126/sciadv.adv0431

McLuhan, M. (1964). *Understanding media: The extensions of man*. McGraw-Hill.

Medesani, M., & Macdonald, J. (2026). Geometric foundations of invariant corridors and governance: A unified framework with empirical validation (Level 3.3). *Working Paper*. https://doi.org/10.5281/zenodo.18822552

Meder, D., et al. (2021). Ergodicity-breaking reveals time optimal decision making in humans. *PLOS Computational Biology*, 17(9), e1009217.

Mick, D. G. (1986). Consumer research and semiotics: Exploring the morphology of signs, symbols, and significance. *Journal of Consumer Research*, 13(2), 196–213.

Merz, M. A., He, Y., & Vargo, S. L. (2009). The evolving brand logic: A service-dominant logic perspective. *Journal of the Academy of Marketing Science*, 37(3), 328–344.

Muniz, A. M., & O'Guinn, T. C. (2001). Brand community. *Journal of Consumer Research*, 27(4), 412–432.

Nguyen, N. T. (2026). Evaluating the efficacy of AI-generated advertising: A cross-national analysis of customer responses on brand perceptions and customer engagement. *Journal of Global Scholars of Marketing Science*.

Oswald, L. R. (2012). *Marketing semiotics: Signs, strategies, and brand value*. Oxford University Press.

Pagani, M., & Xie, L. (2025). Customer experiences in branded metaverse events: Effects on brand equity. *Journal of Consumer Psychology*.

Park, C. W., MacInnis, D. J., & Priester, J. R. (2010). Brand attachment and brand attitude strength: Conceptual and empirical differentiation of two critical brand equity drivers. *Journal of Marketing*, 74(6), 1–17.

Peirce, C. S. (1931–1958). *Collected papers of Charles Sanders Peirce* (C. Hartshorne & P. Weiss, Eds., Vols. 1–6). Harvard University Press.

Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, 15, 1216–1221. https://doi.org/10.1038/s41567-019-0732-0

Puntoni, S., Vanhamme, J., & Ruber, R. (2011). Two birds and one stone: Purposeful polysemy in minority targeting and advertising evaluations. *Journal of Advertising*, 40(1), 25–41.

Puntoni, S., Reczek, R. W., Giesler, M., & Simester, D. (2021). Consumers and artificial intelligence: An experiential perspective. *Journal of Marketing*, 85(1), 131–151.

Resnikoff, H. L. (1974). Differential geometry and color perception. *Journal of Mathematical Biology*, 1, 97–131. DOI: 10.1007/BF00275798

Ries, A., & Trout, J. (1981). *Positioning: The battle for your mind*. McGraw-Hill.

Sarstedt, M., Brand, B. M., & Ring, C. (2024). Using large language models to generate silicon samples in consumer and marketing research: Challenges, opportunities, and guidelines. *Psychology & Marketing*, 41, 1254–1270.

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

Xi, X., Yang, J., Jiao, K., Wang, S., & Lu, T. (2022). "We buy what we wanna be": Understanding the effect of brand identity driven by consumer perceived value in the luxury sector. *Frontiers in Psychology*, 13, 1002275.

Yoo, B., & Donthu, N. (2001). Developing and validating a multidimensional consumer-based brand equity scale. *Journal of Business Research*, 52(1), 1–14.

Yankelovich, D., & Meer, D. (2006). Rediscovering market segmentation. *Harvard Business Review*, 84(2), 122–131.

Zajonc, R. B. (1980). Feeling and thinking: Preferences need no inferences. *American Psychologist*, 35(2), 151–175.

Zharnikov, D. (2026aa). Empirical rate-distortion curve for AI brand perception encoders. Working Paper. https://doi.org/10.5281/zenodo.19528833

Zharnikov, D. (2026b). The atom-cloud-fact epistemological pipeline: From financial document processing to brand perception modeling. Working Paper. https://doi.org/10.5281/zenodo.18944770

Zharnikov, D. (2026d). Formal metric structure of multi-dimensional brand perception space. Working Paper. https://doi.org/10.5281/zenodo.18945295

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026g). How many brands can a market hold? Sphere packing bounds for multi-dimensional positioning. Working Paper. https://doi.org/10.5281/zenodo.18946429

Zharnikov, D. (2026v). Spectral metamerism in AI-mediated brand perception: How large language models collapse multi-dimensional brand differentiation in consumer search. Working Paper. https://doi.org/10.5281/zenodo.19422427

Zharnikov, D. (2026y). Brand triangulation: A geometric framework for multi-observer brand positioning. Working Paper. https://doi.org/10.5281/zenodo.19468204

---
*This paper is part of the Spectral Brand Theory research program. For the full atlas of 20+ interconnected papers, see [spectralbranding.com/atlas](https://spectralbranding.com/atlas).*

