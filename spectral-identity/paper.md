# From Brand Identity to Spectral Identity: Formalizing Aaker's Framework for Testable, AI-Operable Brand Analysis

Dmitry Zharnikov

ORCID: 0009-0000-6893-9231

DOI: [10.5281/zenodo.20741256](https://doi.org/10.5281/zenodo.20741256)

Working Paper v1.0.0 – March 2026 (revised June 2026)

---

## Abstract

Aaker's Brand Identity Model [-@aaker-1996-building-strong-brands] remains the most widely taught brand management framework, yet it relies on practitioner judgment at three critical points: which identity perspectives matter, which elements are core versus extended, and how to resolve the identity-image gap. This paper proposes Spectral Brand Theory (SBT) as a conceptual formalization that preserves Aaker's multi-perspectival structure while adding parametric precision, testability, and computational operability. The paper demonstrates that Aaker's four perspectives map onto eight parametrized perceptual dimensions; that core and extended elements correspond to empirically discoverable spectral weights; and that the identity-image gap becomes a formally specified rendering problem. The formalization advances a threefold contribution: an explicit perspective-to-dimension mapping showing why eight dimensions are required, spectral counterparts for Aaker's core/extended distinction and brand essence, and observer-specific predictions the original framework cannot express. Applying both frameworks illustratively to Patagonia, IKEA, and Tesla shows that SBT reproduces Aaker's strategic diagnoses while generating new predictions about coherence type, disruption response, and AI operability. The relationship mirrors behavioral economics to classical economics: the predecessor is preserved as a limiting case within a more general theory.

**Keywords:** brand coherence typology, brand identity formalization, brand perception measurement, computational branding, observer heterogeneity, Spectral Brand Theory

---

## 1. Introduction: Why Formalize Aaker?

When David Aaker published *Building Strong Brands* in 1996, he gave the field of brand management its most durable analytical vocabulary. The Brand Identity Model --- with its four perspectives, core and extended identity elements, brand essence, and value proposition architecture --- became the framework that practitioners reach for first and that business schools teach most frequently. Thirty years later, Aaker's conceptual architecture remains the dominant way that brand strategists think about what a brand is, what it should communicate, and how to manage it over time.

The framework works. It has guided brand strategy at organizations from startups to Fortune 500 companies. Its flexibility --- the deliberate refusal to impose a fill-in-the-box rigidity --- allows practitioners to adapt the model to wildly different brand contexts without forcing artificial standardization. This flexibility is a feature, not a limitation, and any successor framework must preserve it.

Yet the flexibility comes at a cost. At three critical decision points, Aaker's framework requires practitioner judgment with no formal mechanism for resolution:

First, **perspective selection**. Aaker's four identity perspectives --- Brand as Product, Brand as Organization, Brand as Person, Brand as Symbol --- describe the dimensions along which brand identity can be constructed. But which perspectives matter for a given brand? A luxury heritage house and a direct-to-consumer subscription service operate in different identity spaces. Aaker's guidance is to select the relevant perspectives through strategic judgment. This works when the strategist has deep domain expertise; it does not scale to portfolio-level analysis or to contexts where the analyst has limited brand familiarity.

Second, **element prioritization**. Within each perspective, the framework distinguishes core identity elements (which remain constant) from extended identity elements (which provide texture and completeness). How does one determine which elements are core? Aaker's answer: judgment, informed by aspiration and market understanding. The distinction is essential --- without it, brands cannot maintain coherence through change --- but the mechanism for making it is unspecified.

Third, **gap resolution**. Aaker's Brand Identity Planning Model explicitly recognizes the gap between brand identity (what the brand intends) and brand image (what consumers perceive). But the framework provides no formal mechanism for diagnosing why the gap exists, whether it is reducible, or how different audience cohorts experience it differently. The gap is acknowledged but not parameterized.

These are not criticisms. They are boundaries --- and boundaries that Aaker himself acknowledged. In *Managing Brand Equity* [@aaker-1991-managing-brand-equity], he emphasized that brand management is "more art than science" and that judgment would always play a central role. The question is whether the field has developed the analytical tools to formalize some of that judgment without losing the art.

This paper argues that it has. Spectral Brand Theory (SBT; Zharnikov [-@zharnikov-2026-spectral-brand-theory-computational-framework]) provides a mathematical formalization of Aaker's framework that converts each of the three judgment-dependent decisions into parametrized, testable, computationally executable operations. The relationship between the two frameworks is not adversarial. It mirrors the relationship between behavioral economics and classical economics [@kahneman-1979-prospect-theory-analysis]: the predecessor framework is not replaced but preserved as a special case within a more general theory. Classical economics describes how rational agents should behave; behavioral economics describes how they actually behave. Aaker's model describes what a brand identity should be; SBT describes how brand identity is actually perceived by heterogeneous observers.

The contribution is threefold. First, this paper provides an explicit mapping between Aaker's four perspectives and SBT's eight perceptual dimensions, showing why eight dimensions are needed to capture what four perspectives bundle [@zharnikov-2026-why-eight-completeness-necessity-sbt]. Second, it demonstrates that Aaker's core/extended distinction, brand essence, and value proposition architecture all have formal spectral counterparts that make them empirically discoverable rather than subjectively assigned. Third, it derives four falsifiable propositions that differentiate SBT predictions from Aaker's framework and applies both to three illustrative brands to show where additional observer-specific predictions become available. The worked examples in Section 6 reproduce Aaker's strategic diagnoses while generating coherence-type predictions the original framework cannot express; the limiting-case relationship is stated as a working geometric argument in Section 7.1, with formal metric-space conditions reserved for follow-on work.

---

## 2. Aaker's Brand Identity Model: A Sympathetic Reading

### 2.1 The Four Perspectives

Aaker's [-@aaker-1996-building-strong-brands] Brand Identity Model defines brand identity through four complementary perspectives, each illuminating a different facet of what the brand represents:

**Brand as Product** encompasses product scope, attributes, quality/value, uses, users, and country of origin. This perspective grounds the brand in its tangible offering --- what the consumer actually buys and experiences. It is the most concrete of the four perspectives and the one most accessible to measurement.

**Brand as Organization** captures organizational attributes (innovation, customer concern, trustworthiness), local versus global orientation, and the values and culture that the organization embodies. Aaker recognized that organizational identity is a brand asset --- one that competitors find extraordinarily difficult to replicate because it is embedded in routines, culture, and history rather than in transferable product features.

**Brand as Person** addresses brand personality --- the set of human characteristics associated with the brand [@aaker-1997-dimensions-brand-personality] --- and the brand-customer relationship. This perspective acknowledges that consumers relate to brands as they relate to people: with expectations of consistency, reciprocity, and character.

**Brand as Symbol** encompasses visual imagery and metaphors, brand heritage, and the symbolic associations that transcend functional attributes. This perspective captures the semiotic dimension of brand meaning --- what the brand signifies beyond what it does.

### 2.2 Core, Extended, and Essence

Within these four perspectives, Aaker distinguishes between core identity elements --- the timeless essence that remains constant as the brand moves across markets and product categories --- and extended identity elements that provide texture, completeness, and context. The brand essence is the single thought that captures the soul of the brand; it is the centroid of the identity system, the element that, if removed, would render the brand unrecognizable.

This architecture is powerful precisely because it is not rigid. Aaker explicitly warns against treating the model as a checklist. Not every brand needs all four perspectives to be active. The number of identity elements varies from six to fourteen depending on the brand's complexity. The framework provides vocabulary and structure without imposing uniformity --- a rare achievement in management theory.

### 2.3 The Brand Identity Planning Model

Aaker's complete system extends beyond identity definition to include brand image analysis (what consumers currently perceive), strategic positioning (the subset of identity to be actively communicated), and execution across touchpoints. The Brand Identity Planning Model integrates these elements into a strategic workflow that connects identity to implementation.

Importantly, the planning model explicitly acknowledges the identity-image gap. Aaker recognizes that what a brand intends and what consumers perceive may diverge. The strategic task is to close this gap through consistent execution. What the framework does not formalize is why the gap exists structurally, whether it is fully closeable, or how different audiences may experience different gaps simultaneously.

### 2.4 Kapferer's Complementary Contribution

Kapferer's [-@kapferer-2008-new-strategic-brand] Brand Identity Prism provides a complementary architecture with six facets: physique, personality, culture, relationship, reflection, and self-image. Where Aaker's model is sender-focused (what the brand is), Kapferer explicitly includes receiver-side facets (reflection and self-image), acknowledging that brand identity is co-constructed between sender and receiver.

Both frameworks recognize that brands are multi-dimensional. Both resist reduction to a single variable. Both acknowledge that different audiences may perceive different facets. The critical limitation they share is that neither parameterizes the observer: both describe the brand's identity structure but do not formalize how or why different observers construct different meanings from the same identity signals. Kapferer's "reflection" facet gestures toward the observer, but it remains a property of the brand (the brand's typical buyer image), not a model of the observer's perceptual apparatus.

This is the boundary that invites formalization.

---

## 3. Three Boundaries That Invite Formalization

The following three limitations are not flaws in Aaker's framework. They are structural boundaries that become visible only when one attempts to operationalize the model at scale, delegate it to computational systems, or apply it to contexts where multiple audiences perceive the same brand simultaneously. They are, in the language of science, the empirical anomalies that a successor theory must explain.

### 3.1 Observer Invariance

Aaker's framework describes what the brand *is* --- its intended identity. Kapferer's prism describes what the brand *projects*, including its reflection in the consumer's mind. Both frameworks assume that brand identity exists as a coherent, sender-defined property that consumers perceive with varying degrees of accuracy. The strategic task is to close the perception gap: bring image closer to identity through better communication, more consistent execution, more compelling storytelling.

This assumption --- that there is one brand identity perceived with noise by many audiences --- is empirically untenable. Grier and Brumbaugh [-@grier-1999-noticing-cultural-differences] demonstrated that identical advertisements produce systematically different meanings in target versus non-target groups. The divergence is not random; it follows the audience's cultural position and prior knowledge. Puntoni, Vanhamme, and Ruber [-@puntoni-2011-two-birds-one] documented purposeful polysemy --- the deliberate design of brand communications that carry different meanings for different audiences simultaneously. Mora, Vila-López, and Küster-Boluda [-@mora-2021-segmenting-audience-cause-related] showed that viral campaigns produce audience-specific effects that aggregate brand tracking cannot detect.

These findings challenge the observer-invariance assumption at its foundation. The brand identity-image gap is not a communication failure to be closed through better execution. It is a structural property of perception: different observers, processing identical signals through different perceptual apparatus, construct different brands. No amount of consistency can produce uniform perception, because perception itself is observer-dependent. Aaker's framework recognizes that the gap exists but has no mechanism for modeling systematic, predictable, observer-dependent divergence.

### 3.2 Element Selection

How does one determine which of Aaker's six to fourteen identity elements are core? The framework's guidance is to select elements that are "timeless" and that would remain constant across markets and product categories. In practice, this decision is made through executive workshops, strategic intuition, and competitive analysis. When a skilled practitioner makes the selection, the results are often excellent.

The limitation emerges at scale. Coleman [-@coleman-2011-service-brand-identity-definition] attempted the first full operationalization of Aaker's Brand Identity Model in a B2B context and found it necessary to develop a custom measurement scale because no standardized operationalization exists. The Brand Personality Scale [@aaker-1997-dimensions-brand-personality] operationalizes one perspective --- Brand as Person --- with validated psychometric properties, but Azoulay and Kapferer [-@azoulay-2003-do-brand-personality-scales] demonstrated that it conflates personality traits with user imagery, blurring the boundary between what the brand is and who uses it. No validated instrument covers all four perspectives simultaneously.

This operationalization gap means that the core/extended distinction, however strategically useful, cannot be verified empirically. Two practitioners analyzing the same brand may designate different elements as core, with no mechanism to adjudicate between them. For individual brand strategy, this ambiguity is manageable. For portfolio-level analysis, cross-brand comparison, or computational delegation, it is disabling.

### 3.3 Consistency Versus Coherence

Aaker's framework prescribes consistency: the brand should communicate the same identity across all touchpoints, markets, and time periods. Consistency is the mechanism through which brand equity accumulates. The prescription is sound --- inconsistent brands confuse consumers and erode trust.

But consistency is a scalar quantity: a brand is more or less consistent. It does not distinguish between structural types of alignment. Sørensen [-@sorensen-2002-strength-corporate-culture] demonstrated that for organizational cultures, the *type* of cultural alignment predicts performance outcomes better than the *degree* of alignment. Strong cultures perform well in stable environments but poorly in volatile ones; the structure of the culture, not its strength, determines resilience.

Applied to brands: two brands can score identically on consistency metrics and have entirely different structural properties. A brand where all audiences perceive the same thing (what SBT terms signal coherence) and a brand where audiences perceive different things that reinforce each other (ecosystem coherence) both exhibit high consistency. But their responses to disruption diverge dramatically. The first transmits a crisis uniformly to all audiences. The second absorbs it selectively, sacrificing peripheral cohorts while strengthening core ones. Aaker's framework implicitly recognizes that consistency varies --- the core/extended distinction is one mechanism for managing it --- but it never taxonomizes the structural types of consistency or links them to differential resilience predictions.

These three boundaries define the space that the spectral formalization is designed to address. Crucially, the formalization is not a replacement: when observer cohorts are approximately homogeneous --- when all significant audiences weight the same dimensions in similar proportions --- the spectral model reduces to Aaker's single-identity framework. The three boundaries become visible only when observer heterogeneity is substantial. Section 7.1 develops this limiting-case relationship in full.

### 3.4 Boundary-Count Justification

The foregoing analysis identifies three structural boundaries in Aaker's framework; SBT addresses them through eight perceptual dimensions rather than four perspectives. A natural question is whether eight is the right number --- too few would replicate the bundling problems identified above, while too many would trade analytical tractability for decomposition at diminishing returns.

The count is not stipulated but derived. Zharnikov [-@zharnikov-2026-why-eight-completeness-necessity-sbt] establishes the completeness and necessity of the eight dimensions through a two-part argument: completeness (no dimension in the set can be explained as a weighted combination of the others) and necessity (removing any single dimension produces at least one pair of empirically distinguishable brand configurations that collapse to identical representations). The derivation proceeds by auditing the perceptual channels implicated across Aaker's four perspectives, Kapferer's six prism facets, and Keller's customer-based brand equity model, then applying orthogonality and parsimony criteria to extract the minimal non-redundant set. Eight dimensions satisfy both criteria; seven do not.

This paper inherits the count from Zharnikov [-@zharnikov-2026-why-eight-completeness-necessity-sbt] and treats Aaker's four perspectives as a coarser partition of the same perceptual space --- one that bundles channels that can, and often do, behave independently. The mapping in Table 1 makes this relationship explicit. The theoretical question of whether different cultural or market contexts might require a different dimensional basis is a legitimate open problem; Zharnikov [-@zharnikov-2026-why-eight-completeness-necessity-sbt] addresses it as a boundary condition on the framework's universality claim.

---

## 4. The Spectral Formalization

SBT [@zharnikov-2026-spectral-brand-theory-computational-framework] proposes that brand perception is irreducibly observer-dependent: different observer cohorts perceive structurally different brands from identical signal environments. The framework decomposes brand signals across eight perceptual dimensions, defines observer cohorts through formal spectral profiles, and models brand perception as probabilistic cloud formation that collapses into conviction through evidence accumulation. This section presents the explicit mapping between Aaker's conceptual architecture and SBT's formal apparatus.

### 4.1 Four Perspectives, Eight Dimensions

Aaker's four identity perspectives each bundle multiple independent perceptual channels. SBT unbundles them into eight parametrized dimensions, each representing a distinct channel through which observers perceive brand meaning [@zharnikov-2026-why-eight-completeness-necessity-sbt].

Table 1: Mapping Between Aaker's Four Identity Perspectives and SBT's Eight Perceptual Dimensions.

| Aaker Perspective | What It Bundles | SBT Dimensions |
|:---|:---|:---|
| Brand as Product | Product scope, attributes, quality, uses, users, country of origin | Semiotic (dim 1), Experiential (dim 4), Economic (dim 6) |
| Brand as Organization | Organizational values, culture, capabilities, local/global orientation | Ideological (dim 3), Social (dim 5), Cultural (dim 7) |
| Brand as Person | Brand personality, brand-customer relationships | Semiotic (dim 1), Narrative (dim 2) |
| Brand as Symbol | Visual imagery, metaphors, brand heritage | Semiotic (dim 1), Cultural (dim 7), Temporal (dim 8) |

*Notes*: Dimension order: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal. Semiotic appears across Brand as Product, Brand as Person, and Brand as Symbol, reflecting its role as the primary visual-identity channel; Cultural appears in both Brand as Organization and Brand as Symbol because cultural codes function simultaneously as an organizational asset and a symbolic resource. The Narrative dimension captures narrative processing as a distinct cognitive route through which consumers build brand connections, as distinct from analytical processing [@escalas-2004-narrative-processing-building-consumer]; this grounds the Brand as Person mapping in an empirically established perceptual mechanism rather than asserting it by stipulation. Mapping derived from Zharnikov [-@zharnikov-2026-spectral-brand-theory-computational-framework]; completeness and necessity of the eight dimensions established in Zharnikov [-@zharnikov-2026-why-eight-completeness-necessity-sbt].

Figure 1: Projection from Aaker's Four Perspectives to SBT's Eight Perceptual Dimensions (Theorem 1, Appendix A).

```{.mermaid width=60%}
flowchart LR
  A1[Brand-as-Product] --> S1[Experiential]
  A1 --> S2[Semiotic]
  A1 --> S3[Economic]
  A2[Brand-as-Organization] --> S4[Cultural]
  A2 --> S5[Social]
  A2 --> S6[Ideological]
  A3[Brand-as-Person] --> S7[Narrative]
  A3 --> S2
  A4[Brand-as-Symbol] --> S2
  A4 --> S4
  A4 --> S8[Temporal]
```

*Notes*: Arrows represent the non-zero weight entries in the linear map T from Appendix A. Each row of T corresponds to one Aaker perspective; each column to one SBT dimension. The Semiotic dimension (S2) receives projections from three perspectives, reflecting its role as the primary visual-identity channel across Product, Person, and Symbol. Weights are illustrative (equal within each perspective row); empirical calibration of T is an open research question.

The practical consequence of unbundling is diagnostic precision. Consider Aaker's "Brand as Product," which bundles product experience, price positioning, and product-attribute visual signals into a single perspective. Under the bundled view, a practitioner diagnosing declining product-perspective scores cannot distinguish between structurally different problems: consumers may be dissatisfied with the product experience (Experiential), or they may perceive the price as unfair relative to value (Economic). A luxury brand scoring poorly on "Brand as Product" almost certainly has an Experiential problem, not an Economic one --- yet Aaker's framework treats both through the same lens. SBT's decomposition reveals which dimension is failing for which cohort, directing intervention precisely.

The same logic applies to every perspective. "Brand as Organization" bundles the organization's ethical commitments (Ideological), its community and social signals (Social), and its cultural codes (Cultural). These channels can be independently weighted by different observer cohorts. A purpose-driven consumer may weight the Ideological dimension heavily while being indifferent to the Cultural dimension; a design professional may do the opposite. Aaker's framework captures both through a single perspective, which obscures the divergence. Under SBT, a brand manager can ask: "Our 'Brand as Organization' is perceived as weak --- but is it the values story (Ideological), the community signal (Social), or the cultural codes (Cultural) that is underperforming, and for which cohort?" The answer determines whether the intervention is a purpose campaign, a community-building program, or a creative refresh.

Similarly, "Brand as Symbol" bundles visual identity (Semiotic), cultural codes (Cultural), and heritage (Temporal). A brand's logo and its heritage are perceived through different cognitive mechanisms and weighted differently by different audiences. A re-collapse attempt that changes visual identity (Semiotic) without addressing heritage perception (Temporal) may solve one problem while creating another --- a distinction invisible under the bundled perspective.

Table 2 illustrates how the decomposition changes the diagnostic question for each perspective.

Table 2: How Dimensional Decomposition Changes the Brand Diagnostic Question.

| Aaker Perspective | Bundled Diagnostic | SBT Decomposed Diagnostic |
|:---|:---|:---|
| Brand as Product | "Is our product identity strong?" | "Is it the experience or the price perception that is failing --- and for which cohort?" |
| Brand as Organization | "Is our organizational identity compelling?" | "Is the problem in our values, our cultural codes, or our heritage --- and who notices?" |
| Brand as Person | "Is our brand personality clear?" | "Is it the story we tell (Narrative) or the community we convene (Social) that is resonating or failing?" |
| Brand as Symbol | "Is our symbolic identity distinctive?" | "Is the visual system working but heritage neglected, or vice versa --- and for whom?" |

*Notes*: Decomposed diagnostics are illustrative; actual dimension rankings for a given brand require cohort-level spectral profile measurement.

The eight dimensions were synthesized from prior frameworks [@zharnikov-2026-spectral-brand-theory-computational-framework; @zharnikov-2026-why-eight-completeness-necessity-sbt]. Kapferer's [-@kapferer-2008-new-strategic-brand] "physique" maps to the Semiotic dimension; his "culture" maps to Cultural and Ideological; his "relationship" maps to Experiential and Social. Aaker's [-@aaker-1996-building-strong-brands] functional benefits map to Experiential and Economic; emotional benefits to Narrative, Social, and Cultural; self-expressive benefits to Ideological, Social, and Semiotic. The synthesis preserves the insights of both frameworks while resolving their bundled categories into independently parameterizable channels.

The dimensional decomposition is not merely taxonomic. Each dimension has metric properties: signals can be inventoried, typed (designed, ambient, or synthetic), classified by emission type (positive, null, or structural absence), and rated for strength. This transforms Aaker's qualitative descriptions into structured data that can be computationally processed, cross-brand compared, and aggregated into portfolio-level analysis.

### 4.2 Core and Extended Identity as Spectral Weights

Aaker's distinction between core and extended identity elements is one of the most strategically useful concepts in brand management. Core elements define what the brand must always be; extended elements add richness and context. The limitation, as noted in Section 3.2, is that the distinction is subjectively assigned.

SBT formalizes this distinction through spectral weights. Each observer cohort has a weight profile across the eight dimensions --- a vector that specifies how much each dimension contributes to that cohort's brand perception. Core identity elements correspond to dimensions with the highest cohort-average weights: these are the dimensions that matter most to the brand's primary audiences and that, if altered, would destabilize the brand's perception clouds. Extended identity elements correspond to dimensions with moderate weights: present in the perception cloud but not critical.

Brand essence --- Aaker's "single thought that captures the soul of the brand" --- becomes the centroid of the perception cloud in spectral space. It is not a verbal summary but a geometric position: the point in eight-dimensional space around which the brand's perception clouds cluster across cohorts.

The advance is epistemological. Under Aaker's framework, core elements are chosen through strategic judgment. Under SBT, they are empirically discoverable: measure the spectral profiles of the brand's primary cohorts, compute cohort-average weights, and the core dimensions reveal themselves. The strategist's judgment is not eliminated --- it is informed by data and verifiable against measurement. The methodological precedent for this approach is INDSCAL [@carroll-1970-analysis-individual-differences], which introduced individual-difference dimensional weighting in multidimensional scaling. INDSCAL demonstrated that different individuals weight perceptual dimensions differently when evaluating stimuli --- the same structural insight that SBT extends from laboratory stimuli to brand perception at the cohort level.

### 4.3 Brand Image as Perception Cloud

Aaker's framework treats brand image --- what consumers actually think --- as a separate construct from brand identity, with the strategic goal of aligning image to identity. The identity-image gap is the central diagnostic of brand health.

SBT reframes brand image as a perception cloud: a probabilistic, multi-dimensional cluster of perceived signals that forms in each observer cohort's mind. The perception cloud is not a degraded version of the intended identity. It is a distinct perceptual object, co-constructed by the brand's signal environment and the observer's spectral profile. Two observer cohorts, exposed to identical brand signals, will form different perception clouds if their spectral profiles differ --- not because one perceives more accurately than the other, but because their perceptual apparatus weights different dimensions.

The identity-image gap thus becomes the rendering problem [@zharnikov-2026-spectral-brand-theory-computational-framework]: the irreducible distance between what the organization specifies (brand identity) and what observers perceive (perception clouds). Roy and Banerjee [-@roy-2014-identification-measurement-brand-identity] provided the first quantitative measurement of this gap, confirming that it exists and varies systematically across brand attributes. SBT formalizes *why* the gap is irreducible: specification impossibility [@zharnikov-2026-spectral-brand-theory-computational-framework] proves that no finite brand specification can fully determine perception in high-dimensional observer space. Some gap is structural, not strategic.

This reframing has practical consequences. Under Aaker's framework, the strategic goal is to close the identity-image gap through better execution. Under SBT, the strategic goal shifts to understanding which components of the gap are closeable (through improved signal design) and which are structural (arising from observer heterogeneity that no communication strategy can overcome). The distinction between manageable and irreducible gap components is diagnostically important and cannot be made within the original framework.

### 4.4 Value Proposition as Dimensional Activation

Aaker's value proposition framework distinguishes three types of benefits: functional (what the product does), emotional (how the product makes the consumer feel), and self-expressive (what the product says about the consumer). SBT maps these onto dimensional activation patterns.

Table 3: Mapping Between Aaker's Benefit Types and SBT's Dimensional Activation Patterns.

| Aaker Benefit Type | SBT Dimensional Activation |
|:---|:---|
| Functional benefits | Experiential + Economic |
| Emotional benefits | Narrative + Social + Cultural |
| Self-expressive benefits | Ideological + Social + Semiotic |

*Notes*: Activation patterns represent primary dimensional channels; actual weights are cohort-specific. The Social dimension participates in both emotional and self-expressive pathways, reflecting that community belonging is simultaneously an emotional experience and a self-expressive signal.

The mapping reveals a structural insight that Aaker's framework implies but does not formalize: the Social dimension participates in both emotional and self-expressive benefits. Community belonging is simultaneously an emotional experience and a self-expressive signal. Under Aaker's discrete benefit categories, this overlap is managed through practitioner interpretation. Under SBT's continuous dimensional weights, the overlap is explicit: the Social dimension carries weight in multiple benefit pathways simultaneously, and its relative contribution is parameterized per cohort.

The critical addition is that which benefits activate depends not only on the brand's intent but on the observer's spectral profile. A brand designed to deliver self-expressive benefits (strong Ideological and Semiotic signals) will activate those benefits only in cohorts that weight those dimensions. Cohorts that weight Experiential and Economic dimensions will perceive the same brand through a functional lens, regardless of the brand's self-expressive intent. This observer-dependent activation explains why purpose-driven brand strategies succeed with some audiences and fail with others: the strategy targets dimensions that only certain cohorts can perceive.

### 4.5 Observer Heterogeneity: The Key Addition

Aaker's framework describes one brand identity perceived by many audiences. Kapferer's prism acknowledges sender and receiver perspectives but treats the receiver as a single entity. Keller [-@keller-1993-conceptualizing-measuring-managing] customer-based brand equity model locates equity in the customer's mind --- the most important precedent for an observer-dependent approach --- but treats "the customer" as a unitary construct with one set of brand associations and one equity structure.

The empirical foundation established in Section 3.1 applies directly here: the same signal environment produces divergent brand perceptions across cohorts not through noise but through structural differences in observer spectral profiles.

SBT introduces the observer spectral profile: a formal parameter set that defines how each cohort perceives brand signals. The profile includes dimensional weights (how the observer prioritizes the eight dimensions), tolerances (how much inconsistency the observer accepts before perception destabilizes), priors (existing brand convictions stored in memory), and an identity gate (whether the observer can recognize the brand's signals as belonging to a single entity).

Cohorts are perceptual groupings, not demographic segments. This distinction is fundamental. Traditional market segmentation [@wedel-2000-market-segmentation-conceptual] divides audiences by observable characteristics --- age, income, geography, psychographic cluster. SBT cohorts are clusters in spectral-profile space: groups of observers whose perceptual profiles are similar enough that they form structurally similar perception clouds from the same signal environment. Two observers who share every demographic characteristic may belong to different SBT cohorts if their dimensional weights and priors diverge. Two observers from entirely different demographics may share a cohort if their spectral profiles converge.

The methodological ancestry of observer profiling traces to INDSCAL [@carroll-1970-analysis-individual-differences], which demonstrated that individuals weight perceptual dimensions differently when evaluating stimuli, and to latent class segmentation methods [@wedel-2000-market-segmentation-conceptual], which cluster consumers into perceptual segments post hoc rather than imposing a priori demographic boundaries. SBT extends this ancestry by integrating individual-difference weighting with multi-dimensional brand perception and non-ergodic temporal dynamics into a unified computational framework.

---

## 5. What the Formalization Adds

SBT preserves every structural insight in Aaker's framework while adding three capabilities that the original model cannot express. Each capability addresses one or more of the boundaries identified in Section 3. The capabilities are formalized below as numbered propositions with explicit falsification criteria [@zharnikov-2026-spectral-brand-theory-computational-framework].

### 5.1 Testable Predictions

Aaker's framework generates descriptions: "Brand X has a strong Brand as Organization perspective with innovation at its core." These descriptions are analytically useful but not falsifiable. No observation could prove the description wrong, because the framework provides no prediction about what should follow from the description.

SBT generates falsifiable propositions. Four core propositions follow from the formalization:

**P1 (Observer divergence).** *Structurally different observer spectral profiles produce divergent perception clouds from identical brand signal environments, and the divergence is predictable from profile distance in spectral space.*
Rationale: if perception is a function of both signal content and observer profile weights, then cohorts with orthogonal weight vectors cannot converge on the same perception cloud regardless of signal consistency.
Falsification: P1 is falsified if observers with documented spectral profile differences of magnitude δ > ε produce perception clouds whose centroid distance is not statistically distinguishable from zero across replicated signal environments.

**P2 (Coherence type predicts disruption response).** *Coherence type (not coherence degree) predicts the structural pattern of conviction change following a brand disruption event.*
Rationale: Sørensen [-@sorensen-2002-strength-corporate-culture] showed that cultural type predicts performance better than cultural strength; the coherence taxonomy applies the same principle to brand perception. Two brands with identical consistency scores but different coherence types respond to disruption through structurally distinct mechanisms.
Falsification: P2 is falsified if brands independently classified as Incoherent and Signal-coherent show indistinguishable conviction-change distributions across a panel of observers following an equivalent magnitude disruption [@zharnikov-2026-restoring-perceptual-separability-after-coherence].

**P3 (Spectral weights reveal empirical core identity).** *Dimensions identified as "core" through cohort-average spectral weight analysis predict conviction resilience under disruption better than strategist-assigned core/extended classifications.*
Rationale: Aaker's core/extended distinction is assigned through strategic judgment with no verification mechanism. If the SBT formalization is correct, empirically measured spectral weights provide a verifiable criterion that should outperform judgment-based assignment in predicting which disruptions destabilize the brand.
Falsification: P3 is falsified if strategist-assigned core elements and spectral-weight-ranked core dimensions produce indistinguishable predictions of conviction shift magnitude across a pre-registered set of disruption scenarios.

**P4 (AI observers exhibit systematic dimensional collapse).** *Large language models acting as brand observers collapse multi-dimensional spectral profiles toward Experiential and Economic dimensions, producing metameric perception for brands with distinct Ideological or Narrative profiles.*
Rationale: computational observers process brand signals through statistical patterns in training corpora rather than lived cultural experience, systematically under-weighting dimensions (Ideological, Cultural, Temporal) that require embodied cultural context to activate [@zharnikov-2026-dimensional-collapse-ai-mediated-search; @zharnikov-2026-ai-native-brand-identity-from].
Falsification: P4 is falsified if LLM-generated spectral profiles do not differ significantly from human-generated profiles on Ideological, Cultural, and Temporal dimensions across a balanced sample of brands with varying profile types.

### 5.2 AI Operability

Aaker's Brand Identity Model requires human workshops, strategic discussion, and practitioner judgment at every stage. This is appropriate for high-stakes brand strategy decisions and will remain so. But the model cannot be delegated to computational systems for routine analysis, portfolio-level scanning, or real-time monitoring.

SBT's dimensional decomposition can be executed by large language models using a structured prompt sequence with YAML output templates [@zharnikov-2026-spectral-brand-theory-computational-framework; @zharnikov-2026-ai-native-brand-identity-from]. Empirical study of LLM-mediated brand perception found that AI observers systematically collapse spectral profiles toward Experiential and Economic dimensions, producing Dimensional Coherence Index (DCI) scores of .291 for global brands and .357 for cross-cultural comparisons [@zharnikov-2026-dimensional-collapse-ai-mediated-search]. Cross-model replication (Claude Opus 4.6 and Gemini 3.1 Pro across five brands) produced identical coherence type classifications and identical letter grades for every brand in the sample, confirming that the analytical conclusions are framework-driven rather than model-specific.

This computational implementability does not replace practitioner judgment. It augments it by providing a rapid, structured, replicable analytical layer that practitioners can interrogate, challenge, and override. The relationship is analogous to financial modeling: no competent CFO delegates investment decisions to a spreadsheet, but no competent CFO makes investment decisions without one.

### 5.3 Coherence Taxonomy

Aaker prescribes consistency. SBT taxonomizes it. The five-type coherence classification [@zharnikov-2026-spectral-brand-theory-computational-framework] distinguishes brands by the structural relationship between their observer cohorts' perception clouds.

Table 4: Five Coherence Types and Their Disruption Response Patterns.

| Coherence Type | Pattern | Disruption Response | Exemplar |
|:---|:---|:---|:---|
| Ecosystem | Cohorts interdependent, reinforcing | Selective absorption | Hermès |
| Signal | Consistent signals, consistent perception | Uniform transmission | IKEA |
| Identity | Ideological core filters compatibility | Binary division | Patagonia |
| Experiential asymmetry | Direct vs. mediated perception gap | Geographic variation | Erewhon |
| Incoherent | Contradictory signals, irreconcilable clouds | Amplifying fragmentation | Tesla |

*Notes*: Coherence type classifications derived from Zharnikov [-@zharnikov-2026-spectral-brand-theory-computational-framework]. Exemplar brands are illustrative, not exhaustive. Recovery conditions following coherence shocks are formalized by the μ > λ threshold inequality in Zharnikov [-@zharnikov-2026-restoring-perceptual-separability-after-coherence].

Table 5: Comparison of Brand Identity Frameworks Across Structural Dimensions.

| Dimension | Aaker [-@aaker-1996-building-strong-brands] | Hatch and Schultz [-@hatch-2001-strategic-stars-aligned-your] | Balmer and Greyser [-@balmer-2002-managing-multiple-identities-corporation] | Kapferer [-@kapferer-2008-new-strategic-brand] | SBT |
|:---|:---|:---|:---|:---|:---|
| Number of dimensions | 4 perspectives | 3 alignment gaps (Vision, Culture, Image) | 5 identity types (AC²ID) | 6 prism facets | 8 perceptual dimensions |
| Origin discipline | Brand management | Organizational identity | Corporate identity | Brand management | Brand perception science |
| Measurement approach | Practitioner judgment; no standardized instrument | Gap audit (managerial elicitation) | Identity audit (qualitative) | Practitioner mapping | Parametric spectral profiles; computational or survey-based |
| Treats observer heterogeneity | No — single identity, one gap | Partial — Image facet acknowledges receiver | Partial — "Conceived" identity is receiver-side | Partial — Reflection and self-image facets | Yes — observer cohorts as primary analytical unit |
| Treats AI observers | No | No | No | No | Yes — P4 predicts dimensional collapse in LLM observers |
| Falsifiable propositions | None stated | None stated | None stated | None stated | P1–P4 with explicit falsification criteria |
| Limiting-case relation to SBT | Aaker is T·ψ projection onto 4 dimensions (Appendix A) | VCI alignment gaps recoverable from inter-cohort cloud distance | AC²ID identity types recoverable from cross-stakeholder cloud divergence | Kapferer facets correspond to SBT dimension subsets | — |

*Notes*: AC²ID = Actual, Communicated, Conceived, Ideal, Desired identity types. VCI = Vision-Culture-Image. Limiting-case relations are structural correspondences, not empirical equivalences; calibration is required before use as converters.

The taxonomy addresses Section 3.3's boundary directly. Sørensen [-@sorensen-2002-strength-corporate-culture] demonstrated that cultural type predicts outcomes better than cultural strength; the coherence taxonomy applies the same principle to brand perception. Two brands scoring 7/10 on a conventional consistency metric --- one with signal coherence (IKEA), one with ecosystem coherence (Hermès) --- will respond to identical disruptions in structurally different ways. The signal-coherent brand transmits the disruption uniformly. The ecosystem-coherent brand absorbs it selectively. The consistency score is identical; the strategic implications are opposite. The μ > λ threshold inequality [@zharnikov-2026-restoring-perceptual-separability-after-coherence] formalizes the recovery condition: brands below threshold cannot restore perceptual separability through signal correction alone and require structural coherence intervention.

This distinction cannot be made within Aaker's framework because it requires modeling multiple observer cohorts simultaneously and characterizing the structural relationship between their perception clouds --- capabilities that depend on the formal observer model.

### 5.4 Dynamic Modeling

Aaker's Brand Identity Model is a snapshot: it describes the brand's identity at a point in time. The framework acknowledges that brands evolve --- the core/extended distinction is partly a temporal concept, with core elements persisting through change --- but it does not model the dynamics of perception change.

SBT models brand perception as a non-ergodic process [@zharnikov-2026-spectral-brand-theory-computational-framework]: the temporal sequence in which brand signals are encountered affects the resulting conviction, even when the set of signals is identical. An observer who encounters a product failure before a brand's origin story forms a different conviction than one who encounters the same two signals in reverse order, because the first signal establishes a prior that filters interpretation of the second. This path dependence means that ensemble averages (cross-sectional brand tracking studies) systematically misrepresent individual cohort trajectories [@zharnikov-2026z-spectral-dynamics]. The velocity and acceleration of perception change in spectral space --- and the phase transitions that mark permanent conviction shifts --- have direct implications for how brand health is measured and when intervention is possible.

### 5.5 Portfolio Perception Interaction

Aaker's portfolio work classifies brand architecture types (branded house, house of brands, endorsed brands, sub-brands) but does not model how brands within a portfolio interact in observer perception space. When two brands occupy overlapping regions of spectral space, their signals interfere: an observer's perception of one brand is influenced by their perception of the other. SBT's eight-dimensional representation makes this interference visible and analyzable --- brands are positions in a shared perceptual space, and their proximity, overlap, and signal interactions can be formally characterized.

### 5.6 Boundary Conditions: When Aaker Suffices

The formalization in this section claims that SBT adds predictive and diagnostic value beyond Aaker's framework. That claim requires a boundary condition: there are circumstances in which Aaker's framework is sufficient and SBT adds only computational overhead.

Aaker's framework suffices when observer cohorts are approximately spectrally homogeneous --- when the primary audiences of a brand weight the eight dimensions in roughly similar proportions. Under this condition, the multi-cohort perception cloud collapses to a near-point in spectral space, the identity-image gap approaches zero for all cohorts simultaneously, and the formalization reduces to Aaker's single-identity model (Section 7.1). Brands operating in culturally homogeneous markets with low consumer heterogeneity, stable category conventions, and high-design signal environments approximate this condition.

Three explicit limitations on the formal relationship also bear stating. First, the limiting-case theorem in Appendix A applies to brand-identity content, not measurement instruments. Aaker's empirical measurement instruments (the Brand Personality Scale; Coleman's [-@coleman-2011-service-brand-identity-definition] operationalization) use different scales than SBT spectral profiles; Appendix A's T matrix is a conceptual mapping, not a psychometric converter. Second, the weights in T are illustrative: they specify which SBT dimensions contribute to each Aaker perspective but do not specify the magnitudes. Empirical calibration of T requires cross-validated measurement data. Third, the mapping is non-invertible: because T collapses eight dimensions to four, an Aaker representation cannot be expanded back to a unique SBT profile. Practitioners who have only Aaker-level measurements cannot reconstruct SBT-level diagnostics from them; the informational loss is structural, not a measurement artifact.

---

## 6. Worked Examples: Aaker and SBT Applied to the Same Brands

To illustrate that SBT reproduces Aaker's insights while generating additional predictions, this section applies both frameworks to three brands that represent different coherence architectures. The analyses are illustrative, not empirical: the SBT spectral profiles are expert-derived estimates reported in Zharnikov [-@zharnikov-2026-spectral-brand-theory-computational-framework], not measurements from consumer surveys or conjoint studies. Their purpose is to show what observer-specific predictions become available once the dimensional decomposition is applied, not to establish the profiles as ground truth. Primary empirical validation of the propositions in Section 5.1 requires independently collected perceptual data and is reserved for follow-on work.

### 6.1 Patagonia: Identity Coherence

**Aaker's analysis.** Patagonia exhibits a strong "Brand as Organization" identity, anchored in environmental activism and values-driven business practices. The brand personality is sincere, rugged, and competent (in Jennifer Aaker's [-@aaker-1997-dimensions-brand-personality] terms). Core identity elements include environmental mission, product durability, and activist stance. The value proposition combines functional benefits (durable outdoor gear), emotional benefits (belonging to a values community), and self-expressive benefits (declaring environmental commitment through brand choice).

**SBT's analysis.** Patagonia's spectral profile is Ideological-dominant, with the canonical profile [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5] across the eight dimensions [@zharnikov-2026-spectral-brand-theory-computational-framework]. The brand exhibits Identity coherence: a strong Ideological core creates tight coherence among purpose-aligned observers but actively repels misaligned ones. The coherence is not a property of the brand alone but of the relationship between the brand's signal architecture and the spectral profiles of its primary cohorts.

**What SBT adds.** Aaker's analysis identifies what Patagonia is. SBT predicts how it will behave under stress. Under Identity coherence, disruption produces a binary response: purpose-aligned cohorts rally ("this proves they're authentic"), while misaligned cohorts deepen their indifference or opposition. There is no middle ground. SBT also predicts which dimensions are critical: the brand can absorb Experiential disruptions (a product quality issue) because its primary cohorts weight Ideological signals more heavily; but an Ideological disruption (a perceived betrayal of environmental values) would trigger wholesale re-collapse in the core cohort, with no structural fallback. The type of disruption, not its magnitude, determines the outcome --- a prediction that Aaker's consistency-focused framework cannot generate. Whether the brand's coherence structure meets the μ > λ recovery threshold following such a shock is a testable question addressed by Zharnikov [-@zharnikov-2026-restoring-perceptual-separability-after-coherence].

### 6.2 IKEA: Signal Coherence

**Aaker's analysis.** IKEA has a strong "Brand as Product" identity, supported by "Brand as Symbol" (the Swedish design aesthetic, the blue-and-yellow palette, the distinctive store experience). Core identity elements include democratic design, affordability, and Scandinavian functionality. The value proposition is primarily functional (well-designed furniture at accessible prices), with emotional benefits derived from the participatory assembly experience and the store's distinctive atmosphere.

**SBT's analysis.** IKEA's spectral profile is [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0], with Semiotic and Economic dimensions dominant [@zharnikov-2026-spectral-brand-theory-computational-framework]. The brand exhibits Signal coherence: consistent designed signals produce consistent perception clouds across all cohorts. A first-time student furnishing a dormitory and a design professional evaluating furniture see different aspects of the brand but perceive the same core proposition. The D/A ratio (designed-to-ambient) is high (approximately 75:25), meaning the brand dominates its own signal environment.

**What SBT adds.** Aaker's analysis captures the consistency. SBT identifies a structural vulnerability invisible to the original framework. Under Signal coherence, disruption transmits uniformly to all cohorts --- there is no selective absorption, no peripheral cohort to sacrifice. A quality scandal would affect every observer approximately equally, requiring system-wide signal correction rather than targeted cohort management. SBT also identifies a signal fatigue risk: when designed signals become so consistent that they fade into background expectation, the brand loses perceptual salience without any decline in signal emission. The mechanism --- habituation through excess consistency --- is a paradoxical risk of signal coherence that Aaker's consistency prescription cannot diagnose.

### 6.3 Tesla: Incoherence

**Aaker's analysis.** Tesla has a dominant "Brand as Person" identity, with the founder's personality overwhelming all other perspectives. The brand personality is exciting, innovative, and daring --- but the personality's recent evolution has introduced volatility. The value proposition combines functional benefits (electric vehicle performance), self-expressive benefits (environmental commitment, technological identity), and emotional benefits (being part of a civilizational project).

**SBT's analysis.** Tesla's spectral profile is [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0], with Narrative dominant but Ideological severely conflicted [@zharnikov-2026-spectral-brand-theory-computational-framework]. The brand exhibits Incoherence: strong but contradictory signals produce irreconcilable perception clouds across cohorts. A Tech Loyalist (Experiential weight: 0.35, Ideological weight: 0.10, high tolerance) perceives the brand through the product and concludes "best EV on the market." A Progressive Boycotter (Ideological weight: 0.45, Experiential weight: 0.03, zero tolerance) perceives the brand through the founder's political activity and concludes "CEO's political vehicle." These are not different emphases on a shared brand --- they are irreconcilable convictions assembled from the same signal environment by observers with different spectral profiles.

**What SBT adds.** This is the case that most clearly demonstrates SBT's diagnostic advantage. Aaker's framework sees a strong brand with a volatile personality. Traditional brand equity scores --- awareness, consideration, favorability --- show Tesla as one of the world's strongest brands. SBT reveals it as one of the most architecturally fragile: maximum emission power with minimum structural health. The framework identifies the CEO as the source of approximately 65% of all brand-related signals, most of them ambient (not designed by the brand), dominating the Ideological, Narrative, and Social dimensions where different cohorts diverge most. The Experiential dimension (the actual product) is the brand's only unconflicted dimension --- simultaneously its greatest strength and its last remaining firewall.

Fournier and Eckhardt [-@fournier-2019-putting-person-back] identify the structural risk of person-brands: when the brand is inseparable from a single individual, the brand inherits that individual's volatility with no structural buffer. SBT formalizes this as a coherence type --- Incoherence --- and predicts its disruption behavior: amplifying. Each disruption widens existing cracks. A product recall reinforces the Boycotter's narrative. A CEO controversy reinforces the Loyalist's defensive posture. The system does not absorb disruption; it converts disruption into deeper division. This is the worst resilience profile in the taxonomy, and it cannot be diagnosed by frameworks that do not model multiple observer cohorts simultaneously. The μ > λ threshold condition [@zharnikov-2026-restoring-perceptual-separability-after-coherence] predicts that Incoherent brands fall below the recovery threshold after successive disruptions, making perceptual separability between conflicting cohorts permanent rather than recoverable.

### 6.4 Cross-Case Synthesis: The Differential-Prediction Pattern

The three cases illuminate a cross-cutting pattern that neither Aaker's framework nor conventional consistency metrics can detect. Under Aaker's Brand as Symbol perspective, Patagonia and Tesla are both identifiable as "high-symbol" brands: both carry strong associative imagery, both project personality, both rely heavily on the Brand as Symbol and Brand as Person perspectives for their market identity. A traditional brand equity assessment would classify them similarly on symbolic dimensions and note their high brand salience.

SBT differentiates them sharply. Patagonia's spectral profile [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5] and Tesla's [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0] diverge dramatically on the Ideological (9.5 versus 3.0), Cultural (7.0 versus 4.0), and Temporal (6.5 versus 2.0) dimensions. These are precisely the dimensions invisible to Aaker's bundled perspectives: Ideological is subsumed under Brand as Organization, Cultural is split between Brand as Organization and Brand as Symbol, and Temporal is subsumed under Brand as Symbol. The bundling conceals the divergence.

The predictive payoff is direct. Patagonia's Identity coherence and Tesla's Incoherence are not incidental differences in brand management quality; they follow structurally from the dimensional profiles. A high-Ideological brand with purpose-aligned cohorts exhibits Identity coherence because those cohorts are selected by the Ideological signal itself. A high-Narrative, low-Ideological brand with contradictory ambient signals exhibits Incoherence because no single dimension anchors cohort formation. IKEA, with its Semiotic-Economic dominance [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0] and designed-signal control, exhibits Signal coherence because both dominant dimensions are highly controllable and audience-agnostic.

The cross-case generalization is therefore: the limiting case of Aaker --- observer-homogeneous, high-design-signal brands like IKEA --- is the case where the framework performs best. The further a brand moves from that prototype, in terms of ideological polarization, ambient-signal dominance, or cultural heterogeneity of its audiences, the larger the SBT-Aaker diagnostic divergence. The formalization is least redundant precisely where brand management is most difficult.

---

## 7. Discussion: Implications and Invitation

### 7.1 The Relationship Between Frameworks

The relationship between Aaker's Brand Identity Model and SBT is not one of replacement but of formalization. Every insight in Aaker's framework has a formal counterpart in SBT. The four perspectives are preserved as bundled projections of eight dimensions. The core/extended distinction is preserved as the spectral weight hierarchy. The brand essence is preserved as the perception cloud centroid. The value proposition architecture is preserved as dimensional activation patterns. The identity-image gap is preserved --- and formalized --- as the rendering problem.

This relationship mirrors historical precedents in other fields. Classical economics was not wrong; behavioral economics formalized the boundary conditions under which classical assumptions hold and identified the systematic deviations that occur outside those conditions. Newtonian mechanics was not wrong; general relativity preserved it as the special case that applies at low velocities and weak gravitational fields. In each case, the predecessor theory was preserved as a limiting case of the successor theory --- valid under specific conditions, incomplete under general conditions.

Aaker's framework is the special case of SBT that applies when observer heterogeneity is minimal --- when all significant cohorts weight the same dimensions in approximately the same proportions. Under this condition, SBT's multi-cohort analysis reduces to Aaker's single-identity analysis, the perception cloud centroid aligns with the intended brand identity, and the formalization adds nothing beyond computational overhead. The condition holds for brands with high signal coherence (IKEA) operating in demographically homogeneous markets. It fails for brands with observer-dependent perception (Tesla), purpose-driven brands with ideological filtering (Patagonia), or any brand operating in markets where cultural heterogeneity produces divergent spectral profiles.

### 7.2 What SBT Inherits from Aaker

**What SBT inherits.** The multi-perspectival structure of brand identity. The core/extended hierarchy. The recognition that brands are simultaneously products, organizations, personalities, and symbols. The strategic principle that identity must be managed, not merely observed. These insights are preserved intact. Any analyst using SBT is implicitly using Aaker. The three capabilities SBT adds beyond this foundation are developed fully in Section 5 (testable propositions, AI operability, coherence taxonomy) and demonstrated in Section 6.

### 7.3 Practical Implications

Practitioners can continue using Aaker's vocabulary while grounding it in SBT's precision. The dimensional mapping (Tables 1 and 2) provides a translation layer between the two frameworks. A brand strategist who thinks in terms of "Brand as Organization" can now specify which components of that perspective --- Ideological, Social, or Cultural --- are critical for which observer cohorts, and test whether those components are actually perceived as intended.

The coherence taxonomy (Table 4) provides a new strategic diagnostic. Instead of asking "how consistent is our brand?" (a scalar question with a scalar answer), strategists can ask "what type of coherence does our brand exhibit?" (a structural question with strategic implications). The answer determines the crisis response playbook: selective absorption for ecosystem coherence, uniform repair for signal coherence, ideological reinforcement for identity coherence, experience investment for experiential asymmetry, or structural intervention for incoherence.

### 7.4 Limitations and Future Directions

The formalization introduces its own limitations. SBT's eight dimensions are a working decomposition synthesized from prior frameworks, not a proven exhaustive set. Their completeness and necessity are derived formally in Zharnikov [-@zharnikov-2026-why-eight-completeness-necessity-sbt], but empirical factor-analytic work on brand perception data would be needed to establish the dimensionality of the perceptual space in practice. The observer spectral profiles presented in the demonstration analyses are expert estimates, not empirically measured through surveys or conjoint analysis. The coherence taxonomy has been demonstrated on five brands; its generalizability across industries, cultures, and brand lifecycle stages remains to be established.

Hatch and Schultz [-@hatch-2001-strategic-stars-aligned-your] VCI (Vision-Culture-Image) alignment model identifies three gap types that brands must manage simultaneously. Balmer and Greyser [-@balmer-2002-managing-multiple-identities-corporation] AC2ID test identifies five identity types (actual, communicated, conceived, ideal, desired) that may diverge within any organization. Both frameworks point to the multi-stakeholder, multi-gap nature of brand identity --- a complexity that SBT's multi-cohort analysis is designed to formalize but that requires empirical validation at each stakeholder interface.

The most important validation gap is empirical. The four propositions in Section 5.1 generate testable predictions --- about observer-dependent perception divergence (P1), coherence type and crisis resilience (P2), spectral weight prediction of core identity (P3), and AI-mediated dimensional collapse (P4). These predictions await testing against independently collected consumer data. Until that testing is complete, SBT remains a theoretical framework with demonstrated analytical utility but unconfirmed empirical validity.

A formal gap also merits explicit acknowledgment: the claim that Aaker's framework is the limiting case of SBT under spectral-profile homogeneity is a geometric argument --- when cohort weight vectors converge, the multi-cohort perception cloud collapses to a single centroid aligned with intended identity, reproducing Aaker's single-identity model --- but it is not accompanied here by a formal metric-space proof. The limit is stated as a working derivation calibrated by the three worked examples; establishing the formal boundary conditions (how similar cohort weight vectors must be before the reduction holds, and what metric space properties are required) remains a priority for follow-on theoretical work.

### 7.5 Invitation

SBT is offered as a formalization that makes Aaker's framework testable, measurable, and computationally operable --- preserving the multi-perspectival structure that makes it powerful while supplying the parametric precision that empirical validation and portfolio-scale analysis require. The relationship between the two frameworks is like that between architectural blueprints and structural engineering calculations: the blueprints describe what the building should look like; the calculations determine whether it can stand. Both are necessary. Neither is sufficient alone. The formalization is offered in the spirit of extending Aaker's foundation, not replacing it.

---

## Acknowledgments

AI assistants (Claude Opus 4.8, Grok 4.20, Gemini 2.5 Pro) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

---

## References

::: {#refs}
:::

## Appendix A: Formal Aaker-as-Limiting-Case Theorem

### A.1 Setup

Let ψ ∈ R^8 denote the SBT brand identity vector for a given brand, with components ψ = (ψ_S, ψ_N, ψ_I, ψ_E, ψ_So, ψ_Ec, ψ_C, ψ_T) corresponding to the eight perceptual dimensions in canonical order: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal.

Aaker's [-@aaker-1996-building-strong-brands] Brand Identity Model organizes brand identity through four perspectives: Brand-as-Product (BAP), Brand-as-Organization (BAO), Brand-as-Person (BAPe), and Brand-as-Symbol (BASy). Define a four-dimensional Aaker representation a ∈ R^4 as a = (a_BAP, a_BAO, a_BAPe, a_BASy), where each component aggregates the perceptual content associated with that perspective.

The mapping question is: what is the formal relationship between ψ and a?

### A.2 Theorem 1 (Aaker as Linear Projection of SBT)

**Theorem 1.** *There exists a linear map T : R^8 → R^4 such that for any brand ψ, the Aaker representation a is given by a = T·ψ, where T is a 4×8 matrix encoding the dimension mapping established in Table 1.*

The map T is not an isomorphism: it is a projection that loses information. The theorem states only that the Aaker representation is recoverable from the SBT representation by linear combination; it does not state that the SBT representation is recoverable from the Aaker representation.

### A.3 Proof (Construction of T)

Construct T row by row, with weights w_i ≥ 0 within each row normalized to sum to 1 (equal weights are used here as the canonical illustrative case; empirical calibration of weights is addressed in A.6).

**Row 1 (BAP — Brand-as-Product):**
BAP is constituted by product scope, attributes, quality, uses, users, and country of origin. Per Table 1, the critical SBT dimensions are Experiential (ψ_E) and Economic (ψ_Ec), with Semiotic (ψ_S) contributing through product-attribute visual signals.

a_BAP = (1/3)·ψ_E + (1/3)·ψ_Ec + (1/3)·ψ_S

**Row 2 (BAO — Brand-as-Organization):**
BAO captures organizational values, culture, capabilities, and local/global orientation. Per Table 1, the critical dimensions are Cultural (ψ_C), Social (ψ_So), and Ideological (ψ_I).

a_BAO = (1/3)·ψ_C + (1/3)·ψ_So + (1/3)·ψ_I

**Row 3 (BAPe — Brand-as-Person):**
BAPe addresses brand personality and brand-customer relationship. Per Table 1, the critical dimensions are Narrative (ψ_N) and Semiotic (ψ_S).

a_BAPe = (1/2)·ψ_N + (1/2)·ψ_S

**Row 4 (BASy — Brand-as-Symbol):**
BASy encompasses visual imagery, metaphors, and brand heritage. Per Table 1, the critical dimensions are Semiotic (ψ_S), Cultural (ψ_C), and Temporal (ψ_T).

a_BASy = (1/3)·ψ_S + (1/3)·ψ_C + (1/3)·ψ_T

This defines T as the following 4×8 matrix (column order: S, N, I, E, So, Ec, C, T):

```
T = | 1/3  0    0    1/3  0    1/3  0    0   |
    | 0    0    1/3  0    1/3  0    1/3  0   |
    | 1/2  1/2  0    0    0    0    0    0   |
    | 1/3  0    0    0    0    0    1/3  1/3 |
```

The map a = T·ψ is linear by construction. □

### A.4 Corollary 1 (Information Loss — The Aaker Metamerism Gap)

**Corollary 1.** *T is non-injective: dim(R^8) = 8 > dim(R^4) = 4. There exist distinct SBT brand identities ψ_1 ≠ ψ_2 such that T·ψ_1 = T·ψ_2.*

**Proof.** The null space of T has dimension 8 − rank(T) ≥ 8 − 4 = 4. Any non-zero vector in the null space of T defines a displacement Δψ = ψ_1 − ψ_2 that T maps to zero. Since the null space is non-trivial, distinct brand configurations exist that are perceptually indistinguishable under Aaker's representation. □

This is the **Aaker metamerism gap**: just as two physically different spectral distributions can produce the same color sensation (metamers in colorimetry), two structurally different brands can produce the same Aaker score vector. The gap is not a measurement error; it is a structural consequence of projection from a higher-dimensional to a lower-dimensional space.

The metamerism gap is empirically observable. It occurs when two brands score identically on all four Aaker perspectives but differ on cohort-level SBT responses --- specifically when the diverging dimensions (Ideological, Temporal, or dimensions with asymmetric cohort weights) lie in the null space of T.

### A.5 Corollary 2 (Worked Example — Hermès vs. Patagonia)

Using the canonical spectral profiles [@zharnikov-2026-spectral-brand-theory-computational-framework]:

- Hermès: ψ_H = [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]
- Patagonia: ψ_P = [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]

Applying T (equal-weight illustrative case):

**Hermès Aaker scores:**
- a_BAP = (1/3)(9.5) + (1/3)(3.0) + (1/3)(9.0) = (9.5 + 3.0 + 9.0)/3 = 7.17
- a_BAO = (1/3)(9.0) + (1/3)(8.5) + (1/3)(7.0) = (9.0 + 8.5 + 7.0)/3 = 8.17
- a_BAPe = (1/2)(9.0) + (1/2)(9.5) = 9.25
- a_BASy = (1/3)(9.5) + (1/3)(9.0) + (1/3)(9.5) = 9.33

**Patagonia Aaker scores:**
- a_BAP = (1/3)(6.0) + (1/3)(5.0) + (1/3)(7.5) = (6.0 + 5.0 + 7.5)/3 = 6.17
- a_BAO = (1/3)(7.0) + (1/3)(8.0) + (1/3)(9.5) = (7.0 + 8.0 + 9.5)/3 = 8.17
- a_BAPe = (1/2)(9.0) + (1/2)(6.0) = 7.50
- a_BASy = (1/3)(6.0) + (1/3)(7.0) + (1/3)(6.5) = 6.50

The two brands share an identical BAO score (8.17) despite having markedly different Ideological and Cultural profiles. Hermès carries high Cultural weight (9.0) combined with moderate Ideological (7.0); Patagonia carries high Ideological weight (9.5) combined with lower Cultural (7.0). Under Aaker's Brand-as-Organization perspective, both aggregate to the same organizational-identity strength score. An analyst working within Aaker's framework would diagnose them as identically strong organizational brands and prescribe similar organizational-identity interventions.

Under SBT, the divergence is immediately visible. Hermès's organizational identity is primarily Cultural and Social (heritage and luxury community); Patagonia's is primarily Ideological (environmental mission). These brands require entirely different organizational-identity management strategies, respond to organizational crises through entirely different mechanisms, and are perceived through entirely different cohort filters. The metamerism gap --- the collapsed BAO score --- conceals this divergence. The null-space displacement is Δψ = ψ_H − ψ_P on the Ideological dimension: 7.0 − 9.5 = −2.5, exactly canceled in the BAO aggregate by the offsetting Cultural difference 9.0 − 7.0 = +2.0 and Social difference 8.5 − 8.0 = +0.5.

### A.6 Boundary Conditions

**Conceptual versus measurement equivalence.** Theorem 1 establishes a structural relationship between the conceptual content of the two frameworks, not between their empirical measurement instruments. Aaker's Brand Personality Scale [@aaker-1997-dimensions-brand-personality] and SBT spectral profile measurement use different scales, items, and response formats. T cannot be used as a direct converter between scores obtained from these instruments without cross-validated calibration on shared samples.

**Weight calibration.** The equal-weight assumption used in A.3 and A.5 is illustrative. The actual weights in T are empirical quantities: how much each SBT dimension contributes to each Aaker perspective is a question answered by measurement data, not by conceptual mapping alone. Calibrated weights will likely be asymmetric (Semiotic may carry more weight in BAP than Experiential in some brand categories; Temporal may dominate BASy for heritage brands while being negligible for technology brands). The theorem holds for any positive weight vector within each row; the illustrative equal-weight case makes the structure maximally transparent.

**Cross-cultural generalization.** The eight SBT dimensions and their mapping to Aaker's perspectives were synthesized from frameworks developed primarily in Western brand management contexts. Cross-cultural calibration of both T and the underlying spectral profiles is required before deploying the theorem in non-Western markets where the weighting of, for instance, the Social or Temporal dimension may differ systematically.

### A.7 Implications for the Mapping Critique

The concern that the Aaker-SBT relationship is "merely mapping" --- that Table 1 is taxonomic rather than theoretical --- is directly addressed by the formal apparatus above. A mapping identifies correspondences; a theorem establishes a provable structural relationship. Theorem 1 shows that the correspondence is not arbitrary (any eight-dimensional system could be mapped to any four-dimensional system) but specific: it follows from the dimensional structure of both frameworks and holds in the mathematical sense that a = T·ψ for all brands simultaneously.

Corollary 1 gives the theorem its teeth. The Aaker metamerism gap is not a rhetorical device but a derived consequence: it follows necessarily from the non-injectivity of T, and it is falsifiable --- one can look for pairs of brands with identical Aaker scores that produce divergent cohort-level SBT responses. If such pairs do not exist empirically, the conceptual mapping in Table 1 requires revision. The worked example in A.5 shows that the gap is not merely theoretical: it appears in the canonical brand profiles in the precise dimensions (Ideological and Cultural within BAO) where the two frameworks' diagnostic conclusions diverge most sharply.
