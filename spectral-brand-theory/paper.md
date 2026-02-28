# Spectral Brand Theory: A Computational Framework for Multi-Dimensional Brand Perception

**Dmitry Zharnikov**

Working Paper — February 2026

*Contact: dmitry@spectralbranding.com*

| | |
|---|---|
| **Open-source toolkit** | [github.com/spectralbranding/sbt-framework](https://github.com/spectralbranding/sbt-framework) |
| **Article series** | [spectralbranding.substack.com](https://spectralbranding.substack.com) |
| **SSRN** | *(link pending)* |
| **License** | MIT |

---

## Abstract

This paper introduces Spectral Brand Theory (SBT), a computational framework that models brands as multi-dimensional signal sources perceived through observer-specific spectral profiles. Unlike traditional brand frameworks that treat brand perception as a uniform property of the brand itself, SBT formalizes the observer as an active assembler of brand meaning — each observer cohort perceives a structurally different brand from the same signal environment. The framework decomposes brand signals across eight perceptual dimensions (semiotic, narrative, ideological, experiential, social, economic, cultural, temporal), defines observer cohorts through formal spectral profiles (sensitivity, weights, tolerances), and models brand perception as probabilistic cloud formation that collapses into conviction through evidence accumulation. We validate the framework through structured analysis of five brands spanning luxury (Hermès), mass-market (IKEA), mission-driven (Patagonia), technology (Tesla), and hyperlocal niche (Erewhon). The validation produces four novel mechanisms unavailable through existing frameworks: (1) structural absence as a brand strategy, where designed signal restriction generates value through what is not emitted; (2) a five-type coherence taxonomy, where brands with identical coherence scores exhibit fundamentally different resilience properties; (3) asymmetric conviction resilience, where evidence-free negative convictions are more stable than evidence-rich positive ones; and (4) the independence of brand power and brand health as measurable variables. The framework is computationally implementable: the entire analytical pipeline operates as a structured prompt sequence executable by large language models, compressing analysis that would require a multi-week consulting engagement into a single analytical session. An open-source toolkit is publicly available.

**Keywords:** brand perception, computational branding, observer heterogeneity, brand coherence, structural absence, AI-native framework

---

## 1. Introduction

Consider a thought experiment. Six people are asked to describe the same brand — Tesla. One says it is the most innovative technology platform since Apple. Another calls it Elon Musk's political vehicle. A third describes a betrayal of the environmental movement. A fourth sees a practical electric car with a controversial footnote. A fifth, who has never sat in one, holds a strong conviction about exactly what kind of person drives it. A sixth, in Shanghai, sees a premium Western status symbol and is puzzled by the question.

Same brand. Six descriptions. No overlap.

This is not a communication failure. It is a structural condition — and diagnosing it requires a vocabulary that traditional brand frameworks do not have. Aaker's (1996) brand identity system describes what the brand *is* but not how different observers perceive it differently. Kapferer's (2008) prism includes "reflection" and "self-image" facets that gesture toward the observer but do not formalize observer heterogeneity as a scoring function. Keller's (1993) customer-based brand equity model locates equity in the customer's mind — the closest precedent to SBT's approach — but treats "the customer" as a single model rather than a heterogeneous population of observers with different perceptual apparatuses. Sharp's (2010) empirical marketing science measures mental and physical availability without modeling the perception mechanisms that translate availability into conviction.

The gap is not in any single framework. It is in the field's implicit assumption that "the brand" is a coherent object that exists independently of who is observing it. This paper challenges that assumption directly.

Spectral Brand Theory (SBT) proposes that there is no brand-in-itself — only signals and observers. What we call "the brand" is always already a collapse: a conviction in someone's mind, assembled from whichever signals they could perceive through their particular spectral profile. Different observers, perceiving the same signal environment through different spectral sensitivities, form structurally different brand convictions. These convictions are not errors or variations on a "true" brand — they are the only brands that exist.

The framework contributes to branding theory in three ways:

1. **Formal observer model.** SBT defines each observer cohort through a spectral profile: which dimensions they can perceive (spectrum), how they weight those dimensions (weights), how much inconsistency they accept (tolerances), what they already believe (priors), and whether they can recognize the brand at all (identity gate). This transforms "different people perceive differently" from a qualitative observation into a parameterized scoring function.

2. **Perception pipeline.** SBT models brand perception as a multi-stage pipeline: signal emission → observer filtering → probabilistic cloud formation → threshold-based conviction collapse → re-collapse on new evidence. Each stage is formally specified and computationally implementable. The pipeline explains not only what observers currently believe but how those beliefs will change under disruption.

3. **Computational implementability.** Unlike prior branding frameworks, SBT can be directly executed as software. Signals are typed data structures. Observers are parameter sets. Perception is clustering output. Conviction is a threshold function. The entire pipeline operates as a structured prompt sequence for large language models, making multi-cohort brand analysis accessible without custom engineering.

The remainder of this paper is organized as follows. Section 2 presents the theoretical framework. Section 3 describes the validation methodology. Section 4 reports findings, focusing on four novel mechanisms that emerged from the five-brand validation. Section 5 discusses implications, limitations, and future directions. Section 6 concludes.

---

## 2. Theoretical Framework

### 2.1 Epistemic Foundation: Brands as Perceptual Objects

SBT's core claim is epistemic: a brand is not an object with properties but a perceptual process with observers. The metaphor is astronomical. A constellation of stars appears different from every point in the universe and to every creature with a different range of spectral sensitivity. The constellation "itself" — all stars from no perspective — is a theoretical construct no one actually experiences. What exists are observer-specific perceptions of a shared signal field.

Applied to brands: what a company designs and emits (logo, products, campaigns, pricing, culture) are signals. These signals exist across multiple perceptual dimensions. Each observer cohort filters these signals through its spectral profile, clusters the perceived signals into a probabilistic perception cloud, and — if sufficient evidence accumulates — collapses that cloud into a brand conviction. The conviction is observer-specific. The signal environment is shared. The brand, as commonly understood, is the observer's collapse product — not the company's intended identity.

This inversion has a philosophical precedent. Peirce's semiotics (1890s) established that meaning arises in the interpreter, not the sign. Barthes (1957) showed how cultural myths function as second-order semiotic systems that shape interpretation. Keller (1993) located brand equity in the customer's mind. SBT formalizes and extends these insights into a computational architecture.

### 2.2 Signal Architecture: Eight Perceptual Dimensions

SBT decomposes brand signals across eight dimensions, each representing a distinct channel through which observers perceive brand meaning:

| Dimension | Signal Type | Examples |
|-----------|------------|---------|
| **Semiotic** | Visual and sensory identity markers | Logo, name, colors, typography, packaging, sonic identity |
| **Narrative** | Story structures and temporal arcs | Origin story, founder myth, key events, brand legends |
| **Ideological** | Values, ethics, and purpose claims | Stated mission, ethical positions, political stance |
| **Experiential** | Direct encounter data | Product use, service quality, physical environment, UX |
| **Social** | Community and status signals | Tribal markers, peer signaling, social proof, exclusivity |
| **Economic** | Price and value communication | Pricing strategy, discounting behavior, perceived value |
| **Cultural** | Aesthetic and zeitgeist positioning | Design language, cultural references, humor, taste codes |
| **Temporal** | Heritage and time-depth signals | History, heritage, generational continuity, era associations |

**Table 1.** The eight perceptual dimensions of brand signal architecture.

The eight dimensions emerged from a synthesis of prior frameworks. Kapferer's (2008) "physique" maps to the semiotic dimension; his "culture" maps to cultural and ideological; his "relationship" maps to experiential and social. Aaker's (1996) functional benefits map to experiential and economic; emotional benefits to social and cultural; self-expressive benefits to ideological and social. The temporal dimension — heritage and time-depth — appears in prior work as an attribute of specific brands but has not been modeled as a universal perceptual channel. Our validation suggests it should be.

Each signal carries three properties:

- **Source type**: designed (created by the brand), ambient (generated by the environment — reviews, news, competitor framing, cultural commentary), or synthetic (AI-generated content, LLM summaries, algorithmic recommendations).
- **Emission type**: positive (signal actively present), null (unintentional absence), or structural absence (designed restriction that functions as a signal — see Section 4.1).
- **Strength**: rated 0–5, reflecting intensity of emission.

The signal concept extends economic signaling theory (Spence, 1973) and its application to brand credibility (Erdem & Swait, 1998) from a unidimensional quality indicator to a multi-dimensional perceptual architecture. In SBT, a brand emits not one signal but a structured field of typed signals across eight dimensions — and the observer, not the market, determines which signals are informative.

The ratio of designed to ambient signals — the **designed/ambient (D/A) ratio** — proves to be one of the framework's most diagnostic metrics. A brand whose perception is predominantly shaped by ambient signals (D/A < 0.40) faces a structural problem that no communication strategy can solve: the brand's story is being written by others.

### 2.3 Observer Model: Spectral Profiles

The observer model is SBT's primary theoretical contribution. Each observer cohort is defined by a formal spectral profile:

- **Spectrum**: which of the eight dimensions the observer can perceive (some dimensions are invisible to some cohorts)
- **Weights**: how the observer prioritizes perceived dimensions (a numeric weight per dimension, summing to 1.0)
- **Tolerances**: how much inconsistency the observer accepts before a perception cloud destabilizes
- **Priors**: existing brand convictions stored in memory
- **Identity gate**: whether the observer can recognize the brand's signals as belonging to a single entity (analogous to facial recognition — without it, signals are noise)
- **Encounter mode**: direct (product use, store visit), mediated (screens, content, secondhand accounts), or mixed

The weight-based observer profile is structurally analogous to multi-attribute attitude models (Fishbein & Ajzen, 1975), extending the attribute-weighting mechanism from product evaluation to perceptual dimensions with the critical additions of tolerances, priors, and the identity gate. The spectral profile determines not just *what* the observer sees but *how* they assemble what they see into meaning. Two observers exposed to identical signals will form different perception clouds if their weight profiles differ. This is not a failure of communication — it is the fundamental mechanism of brand perception.

**Figure 1. The Observer-Mediated Perception Pipeline**

```
Brand signals          Observer spectral         Perception          Conviction
(8 dimensions)    →    profile (filter)     →    cloud          →   (collapse)
                       spectrum, weights,         probabilistic       stable belief
                       tolerances, priors         cluster             about brand

+ Ambient signals       Identity gate            Cloud valence        Re-collapse
  (reviews, news,      (recognition              (positive /          on new
  competitors,          prerequisite)             negative /           evidence
  cultural context)                               ambivalent)
```

### 2.4 Cloud Formation and Conviction Collapse

The terminology — cloud, collapse — deliberately invokes quantum mechanical metaphor. A perception cloud is indeterminate; a conviction is a collapsed state. As in quantum measurement, the collapse is observer-dependent: different observers collapse the same signal environment into different convictions. The metaphor is structural, not mathematical — brand perception does not obey quantum mechanics, but it shares the epistemic property that observation determines outcome.

Brand perception follows a three-stage epistemic pipeline:

**Stage 1: Cloud formation.** Perceived signals cluster in the observer's mind, weighted by the observer's spectral profile. The resulting cluster is a *perception cloud* — a probabilistic, pre-conviction impression. Clouds have valence (positive, negative, or ambivalent) and confidence (weak, moderate, or strong). Critically, clouds can form through direct encounter (experiential signals dominate) or through mediated channels (ideological, social, and narrative signals dominate, experiential signals absent). Mediated clouds tend toward lower confidence but can exhibit higher stability when no experiential data introduces ambiguity (see Section 4.3).

**Stage 2: Conviction collapse.** When a cloud accumulates sufficient evidence — when enough signals align across enough dimensions with enough consistency — it collapses into a brand conviction. The conviction is a stable belief: "Tesla is X" or "Hermès means Y." The collapse threshold varies by observer: high-tolerance observers require less evidence; low-tolerance observers demand more.

**Stage 3: Re-collapse.** New evidence (a product failure, a CEO scandal, a brilliant campaign) introduces signals that contradict the existing conviction. If the contradicting evidence is strong enough, the conviction dissolves and the observer re-forms a cloud from the full evidence set — including the new signals. The conviction is rebuilt from scratch, never patched. This explains both brand resilience (convictions resist moderate contradicting evidence) and brand crises (sufficient contradicting evidence forces wholesale re-evaluation).

The re-collapse mechanism is borrowed directly from an epistemological architecture developed for financial document processing (Zharnikov, 2026b), where probabilistic facts about financial transactions are rebuilt from scratch whenever new evidence arrives, rather than incrementally updated. The domain transfer works because the underlying epistemic structure is identical: observations → hypotheses → knowledge, with the added complexity that brand "observations" are filtered through heterogeneous observer profiles rather than a single system.

### 2.5 Coherence as Structural Property

A brand's coherence is not the consistency of its messaging but the structural relationship between its observer cohorts' perception clouds. SBT defines coherence as the degree to which different observers' convictions are compatible — not identical, but compatible. This distinction is crucial: a brand where all observers perceive the same thing (signal coherence) and a brand where observers perceive different things that reinforce each other (ecosystem coherence) both exhibit high coherence, but their structural properties diverge dramatically (see Section 4.2).

Coherence is measured through a seven-metric scorecard:

| Metric | What It Measures |
|--------|-----------------|
| Dimensional coverage | How many dimensions the brand actively emits on |
| Gate permeability | What proportion of target observers recognize the brand |
| Cloud coherence | Compatibility of perception clouds across cohorts |
| Collapse strength | Confidence level of resulting convictions |
| Re-collapse resistance | Stability of convictions under disruption |
| Emission efficiency | Signal-to-noise ratio of designed signals |
| Designed/ambient ratio | Brand's control over its own signal environment |

**Table 2.** The seven-metric spectral scorecard.

---

## 3. Validation Methodology

### 3.1 Design

We validated SBT through structured analysis of five brands selected to span the brand architecture space:

| Brand | Selection Rationale | Architecture Type |
|-------|-------------------|-------------------|
| Patagonia | Mission-driven, ideological core, moderate scale | Identity coherence |
| Tesla | Maximum observer divergence, CEO-dominated signals | Incoherence |
| IKEA | Global consistency, designed-signal dominance | Signal coherence |
| Hermès | Scarcity-based luxury, structural absence strategy | Ecosystem coherence |
| Erewhon | Hyperlocal niche, mediated perception dominance | Experiential asymmetry |

**Table 3.** Five validation brands and selection rationale.

The five brands were chosen to stress-test different properties of the framework: Patagonia tests ideological filtering; Tesla tests extreme observer divergence and ambient signal dominance; IKEA tests consistent signal architecture at global scale; Hermès tests scarcity-based value creation and cross-cohort interdependence; Erewhon tests the framework's minimum viable scale and mediated perception dynamics.

### 3.2 Analytical Pipeline

Each brand was analyzed through six sequential modules, each producing structured YAML output that feeds into subsequent modules:

1. **Brand Decomposition**: inventory of signals across all eight dimensions, source type classification, emission type classification, dimensional heat map
2. **Observer Mapping**: 3–5 observer cohort spectral profiles with weights, tolerances, encounter modes, and cross-cohort dependencies
3. **Cloud Prediction**: per-cohort perception clouds with confidence bands, valence, formation mode, and inter-cohort divergence mapping
4. **Coherence Audit**: seven-metric scorecard, overall grade (A+ through F), coherence type classification
5. **Emission Strategy**: target conviction map, dimensional redesign, D/A ratio optimization, phased action plan
6. **Re-collapse Simulation**: 2–3 disruption scenarios per brand, per-cohort resilience scoring, cascade risk assessment, defensive recommendations

The pipeline was executed using Claude (Anthropic) as the analytical engine, with structured prompts and YAML output templates ensuring consistency across brands. Each module's output was assessed against four validation criteria: non-obvious (a brand strategist could not reach this through standard analysis), dimensionally specific (references specific dimensions and observer profiles), actionable (suggests concrete strategic changes), and observer-differentiated (shows how different cohorts perceive the same signals differently).

### 3.3 Insight Validation Protocol

Each brand analysis was followed by a structured insight assessment that evaluated the top findings against the four criteria. An insight was counted as validated only if it satisfied all four criteria simultaneously. Across five brands, 25 insights were formally assessed; all 25 satisfied all four criteria. The four mechanisms reported in Section 4 were selected as the most novel — insights that could not have been produced by any existing brand framework because the existing frameworks lack the necessary vocabulary.

### 3.4 Limitations of the Validation Approach

The validation has several methodological limitations that must be acknowledged.

First, observer weight assignments are expert estimates informed by behavioral inference, not empirically measured through surveys or experiments. The weights are most defensible for polarized brands (Tesla), where stated purchase behavior makes dimensional priorities visible, and least defensible for inaccessible cohorts (Hermès heritage collectors). Future work should validate weight assignments through conjoint analysis or behavioral experiments.

Second, cloud confidence scores are calibrated within each brand analysis but not across brands. A confidence of 0.85 in the Tesla analysis is not directly comparable to 0.85 in the Hermès analysis. We recommend using confidence bands (weak / moderate / strong) rather than cross-brand decimal comparison.

Third, the analytical pipeline was executed by a single LLM (Claude), introducing potential model-specific biases. Replication with alternative models (GPT-4, Gemini) and by human analysts would strengthen the validation.

Fourth, all five brands are well-known entities with extensive public information. The framework's performance on obscure or newly launched brands — where signal inventories are sparse — remains untested.

Fifth, the validation uses the framework's own analytical pipeline to produce the findings that validate the framework. While the four validation criteria (non-obvious, dimensionally specific, actionable, observer-differentiated) impose external constraints on what counts as a validated insight, the framework shapes which phenomena become visible. Independent validation — comparing SBT-generated findings against independently collected consumer survey data or established brand tracking metrics — would provide a stronger test of the framework's explanatory value.

---

## 4. Findings

The five-brand validation produced nine novel mechanisms. We report four in depth — selected as the most theoretically significant contributions that are unavailable through any existing brand framework.

### 4.1 Structural Absence: Value Creation Through Designed Signal Restriction

**Discovery context:** Hermès case study (Modules 1, 5).

Every brand framework in the literature assumes an emission model: design a signal, emit it, and measure whether it produces the desired perception. More signal generally means more perception. Broader distribution generally means broader awareness. The logic is additive.

Hermès inverts this logic entirely. The brand does almost nothing that brand strategy textbooks recommend. It does not advertise aggressively. It does not maximize reach. It does not hold sales. It does not sell its most iconic products online. It maintains wait lists measured in years. It operates approximately 300 stores worldwide.

By every standard metric of brand communication, Hermès should be weak. It scored A+ in our coherence audit — the highest grade in the study. Not despite the restrictions. Because of them.

We formalize this as **structural absence**: the deliberate withholding of signals that creates value through what is not emitted. The concept has precedent in semiotics — Eco (1976) analyzed how sign systems communicate through absence and overcoding — but has not been formalized as a brand strategy mechanism. The mechanism is analogous to dark matter in physics — invisible but gravitationally active, shaping the perception field without emitting observable signals.

SBT introduces a three-type emission taxonomy:

| Emission Type | Mechanism | Signal Present? | Example |
|--------------|-----------|----------------|---------|
| Positive | Brand actively emits signal | Yes | Product launch, campaign |
| Null | Signal absent, unintentional | No (neglect) | Unused heritage, dormant dimension |
| Structural absence | Designed restriction functions as signal | No (strategy) | Wait list, no discounts, geographic scarcity |

**Table 4.** Three emission types in the spectral model.

The key mechanism is cross-dimensional: restriction on one dimension generates a signal on a different dimension. Economic restriction (never discounting) produces a social signal (the product exists outside normal market forces). Experiential restriction (in-store purchase only) produces an economic signal (difficulty of access justifies the price). Social restriction (purchase rituals, relationship requirements) produces an experiential signal (the restriction process *is* the brand experience).

We model cloud formation with structural absence as:

> Cloud = Σ(emitted signals × weights) + Σ(absent signals × scarcity multiplier × weights)

The scarcity multiplier amplifies the perceived weight of signals that exist in the context of signals that are withheld. Hermès achieves the highest emission efficiency in the study (9/10) not by optimizing what it sends but by optimizing what it withholds — the signal-to-noise ratio approaches its maximum because noise has been structurally excluded.

**Dimensional constraints.** Structural absence does not operate on all dimensions. It operates primarily on social (exclusivity), economic (pricing discipline), and experiential (geographic scarcity) dimensions. It cannot operate on semiotic (there is no "absent logo" — visual identity requires presence) or narrative (the absence of a story is just absence — Hermès in fact has a rich narrative that *frames* the absence). This constraint is consistent with the finding that structural absence requires existing demand to restrict. The strategy is available only to brands with sufficient heritage and established desire to make the restriction legible as intention rather than failure.

**Prerequisite.** Our cross-brand comparison reveals that structural absence requires heritage legitimization. Hermès' 187 years of continuous operation makes its restrictions legible as "this is how we have always been" rather than "this is artificial scarcity." Brands without heritage depth cannot deploy structural absence at scale — the restriction is interpreted as arrogance, not tradition.

### 4.2 Five Types of Brand Coherence

**Discovery context:** Cross-brand comparison (Module 4 across all five brands).

Traditional brand analysis treats coherence as a single variable from low to high: how consistently is the brand perceived across audiences? Our five-brand validation reveals that coherence is not a single variable but a structural property that comes in five qualitatively distinct types, each with different resilience profiles.

| Coherence Type | Grade | Pattern | Resilience Profile | Brand |
|---------------|-------|---------|-------------------|-------|
| Ecosystem | A+ | Different clouds reinforce through functional interdependence | Selective — absorbs disruption by purification | Hermès |
| Signal | A- | Consistent designed signals → consistent clouds | Uniform — transmits disruption evenly | IKEA |
| Identity | B+ | Ideological core filters cohort compatibility | Binary — divides along ideology | Patagonia |
| Experiential asymmetry | B- | Evidence gap between direct and mediated observers | Geographic — different impact by location | Erewhon |
| Incoherent | C- | Contradictory signals → irreconcilable clouds | Amplifying — widens existing cracks | Tesla |

**Table 5.** Five-type coherence taxonomy with resilience profiles.

The critical finding is that two brands can score identically on coherence and have completely different structural properties. A brand with 7/10 signal coherence (the IKEA pattern: everyone perceives the same thing) and a brand with 7/10 ecosystem coherence (the Hermès pattern: different cohorts perceive different things that reinforce each other) would appear identical on any traditional scorecard. Their responses to disruption are radically different.

**Ecosystem coherence** (Hermès) exhibits selective resilience. When the Hermès secondary market collapses in our simulation, the Investment Buyer cohort is destroyed — but the Heritage Client and Cultural Connoisseur are *strengthened*: "now the speculators are gone." The ecosystem metabolizes the disruption by sacrificing peripheral elements while purifying the core. This capacity for selective absorption is unique to ecosystem coherence and explains the extraordinary durability of brands that exhibit it.

**Signal coherence** (IKEA) exhibits uniform resilience. When disrupted, the impact transmits evenly across all cohorts because the same designed signals reach everyone. There is no selective absorption — a quality scandal affects every observer equally. Recovery requires system-wide signal correction, not targeted cohort management.

**Identity coherence** (Patagonia) exhibits binary resilience. The brand divides along ideological lines under stress. Aligned cohorts rally ("this proves they are authentic"). Misaligned cohorts deepen their indifference or opposition. The ideological core is either a magnet or a wall — there is no middle ground.

**Experiential asymmetry** (Erewhon) exhibits geographic resilience. Disruption affects local and mediated observers differently because their perception clouds are built on incompatible evidence bases. A food safety incident at the physical store devastates direct-experience observers but barely registers with the Instagram audience. A social media backlash against wellness culture devastates the mediated observers but leaves local regulars unaffected.

**Incoherence** (Tesla) exhibits amplifying fragility. Each disruption widens existing cracks. The system does not absorb disruption — it converts disruption into deeper division. This is the worst resilience profile in the taxonomy.

The coherence type is determined by three structural properties: (1) cohort interdependence — how much one cohort's perception depends on another's behavior; (2) ideological centrality — how much coherence depends on a shared ideological commitment; and (3) encounter mode variance — how different the direct-encounter brand is from the mediated brand.

### 4.3 Asymmetric Conviction Resilience

**Discovery context:** Tesla case study (Modules 2, 3, 6).

Our analysis of Tesla revealed a counterintuitive structural property of brand perception: evidence-free negative convictions can be more stable than evidence-rich positive ones.

The Tesla Progressive Boycotter cohort holds a brand conviction with 0.82 confidence (classified as "strong"). This conviction is constructed from an ideological weight of 0.45 and a social weight of 0.20 — but an experiential weight of only 0.03. The Boycotter has never driven a Tesla, never visited a showroom, never used a Supercharger. Their entire brand image is constructed from ambient ideological and social signals encountered through screens.

The Tesla Tech Loyalist, who drives the car daily and has extensive product data, holds a conviction with 0.78 confidence — lower than the Boycotter's.

The person with the most evidence has less certainty than the person with the least.

This is not a cognitive error. It is a structural property of spectral perception. The Boycotter's conviction is uncontested because there is no experiential data to create cognitive dissonance. The ideological signal points in one direction. The social signal confirms it. No product encounter introduces nuance. The conviction is coherent *because* it is evidence-free.

The Loyalist, by contrast, has real product data. They know the car is excellent. They also know the service centers can be frustrating. They have experienced the gap between Autopilot promises and delivery. Their conviction includes contradictions — and evidence-rich convictions are inherently less certain than evidence-free ones because they contain more dimensions that can produce ambiguity.

This asymmetry has a critical resilience implication. In our disruption simulations, negative convictions consistently *strengthen* under brand stress, while positive convictions *weaken*. A brand crisis confirms what the negative-conviction holder already believed. But it introduces contradicting evidence for the positive-conviction holder, who must now reconcile their favorable experience with unfavorable news. The asymmetry is directional: positive → negative is far easier than negative → positive, because the latter requires experiential evidence that the negative-conviction holder's spectral profile is designed to exclude.

The strategic implication is stark: resources spent attempting to convert structurally locked negative cohorts are wasted. The Boycotter's experiential gate is effectively closed (0.03 weight). No test drive campaign will reach them because they are not evaluating the product — they are evaluating the ideology. Brands with locked negative cohorts must accept the structural constraint and invest in addressable cohorts instead.

### 4.4 Brand Power and Brand Health as Independent Variables

**Discovery context:** Cross-brand comparison (Module 4 across all five brands).

The five-brand validation produces a finding that inverts conventional brand wisdom: brand power (emission strength, awareness, cultural impact) and brand health (coherence, architectural integrity, resilience) are independent variables. A brand can maximize the first while minimizing the second.

| Brand | Traditional Power | Spectral Health | D/A Ratio | The Gap |
|-------|------------------|----------------|-----------|---------|
| Tesla | Highest (near-universal awareness, massive cultural impact) | Lowest (C-) | 30/65 | Maximum inversion |
| Hermès | Moderate (niche, exclusive, deliberately restricted) | Highest (A+) | 60/35 | Architecture > awareness |
| IKEA | High (global, ubiquitous, universally recognized) | High (A-) | 75/25 | Consistent alignment |
| Patagonia | Moderate (strong in category, limited outside it) | Moderate-high (B+) | 65/30 | Ideological filter |
| Erewhon | Low-moderate (hyperlocal, culturally outsized) | Low-moderate (B-) | 40/55 | Scale floor |

**Table 6.** Five-brand scorecard: brand power versus spectral health.

Traditional frameworks — BrandAsset Valuator (BAV), Interbrand's brand strength methodology, Keller's brand equity pyramid — measure dimensions of power: differentiation, relevance, esteem, knowledge, awareness, consideration. By these metrics, Tesla is among the world's most valuable brands. Seven of eight dimensions emit at strength 4 or higher. Gate permeability is 10/10 — everyone knows the brand.

But the spectral scorecard reveals Tesla's cloud coherence at 2/10, its designed/ambient ratio at 30/65, and its re-collapse resistance at 4/10. Maximum emission power, minimum architectural health.

The confusion between brand power and brand health is, we argue, the central error in traditional brand management. It leads to the systematic misdiagnosis of brands like Tesla (perceived as "strong" when structurally fragile) and the systematic undervaluation of brands like Hermès (perceived as "niche" when architecturally impregnable).

The D/A ratio is the single metric that most powerfully discriminates between power and health. Our five-brand comparison suggests an optimal zone of 55–65% designed signals. High enough to maintain narrative control. Low enough to allow authentic ambient reinforcement. Tesla, at 30% designed, is 25 points below the floor of this zone — meaning no communication strategy can fix its brand problem because 65% of the signal environment is beyond its control. Hermès, at 60% designed with *aligned* ambient signals, demonstrates that the direction of ambient signals matters as much as the ratio: its ambient signals amplify rather than contradict its designed signals.

**Figure 2. D/A Ratio and Coherence Across Five Brands**

```
Coherence
  10 |                                        * Hermès (60/35, A+)
     |                              * IKEA (75/25, A-)
   8 |
     |
   6 |
     |       * Patagonia (65/30, B+)
   4 |                    * Erewhon (40/55, B-)
     |
   2 |                              * Tesla (30/65, C-)
     |
   0 +----+----+----+----+----+----+----+----+----+----
     0   10   20   30   40   50   60   70   80   90  100
                    Designed/Ambient Ratio (% designed)
                         [Optimal zone: 55-65%]
```

---

## 5. Discussion

### 5.1 Relationship to Existing Frameworks

SBT does not replace existing brand frameworks. It explains why each of them works partially and where each breaks down.

Aaker's (1996) brand identity system describes the signal side of the equation — what the brand intends to emit — but lacks the observer model that explains why the same identity produces different perceptions in different cohorts. Kapferer's (2008) prism comes closest to SBT's dimensional approach, with its six facets mapping loosely to SBT's eight dimensions, but treats the facets as properties of the brand rather than perceptual channels through which observers filter signals.

Keller's (1993) customer-based brand equity is the most direct predecessor: equity lives in the customer's mind, brand knowledge equals awareness plus image. SBT extends Keller by modeling the customer as a heterogeneous population rather than a single model, by formalizing the perception-to-conviction pipeline, and by introducing the re-collapse mechanism that explains how brand equity is lost and rebuilt.

Sharp's (2010) empirical challenge to brand differentiation is complementary rather than contradictory. Sharp describes acquisition: passing the identity gate widely (SBT's "gate permeability"). SBT describes what happens *after* the gate: how different observers cluster signals differently and form different convictions. The frameworks address different stages of the same pipeline.

Gestalt psychology (Koffka, 1935) provides the perceptual foundations: cloud formation *is* gestalt perception applied to brand signals. Closure (collapsing an incomplete cloud), similarity (dimensional matching), and proximity (temporal clustering) are the mechanisms through which perception clouds form. Kahneman's (2011) dual-process theory maps to the collapse mechanism: strong brand convictions are System 1 shortcuts that bypass deliberate evaluation, while weak or forming clouds require effortful System 2 processing.

Peters' (2019) ergodicity economics offers an unexpected but structurally precise theoretical ancestor. Peters demonstrates that in multiplicative, path-dependent processes, ensemble averages (averaging across many agents at one moment) diverge systematically from time averages (following one agent across time). This divergence is the formal definition of non-ergodicity. SBT's finding that brand power (an ensemble measure — aggregate awareness across all observers at one moment) and brand health (a time-average measure — how brand architecture performs for any given cohort over its perceptual trajectory) are independent variables is a direct instantiation of Peters' thesis in brand perception. The asymmetric conviction resilience finding (Section 4.3) maps to Peters' concept of absorbing states in non-ergodic processes: once a negative conviction crosses a threshold with no experiential friction to reverse it, the observer is on a one-directional compounding trajectory. Peters' framework thus provides a unified root cause — non-ergodic multiplicative dynamics — for multiple independently discovered SBT phenomena.

In sum, SBT functions as a meta-framework. It provides the architecture within which Aaker, Kapferer, Keller, Sharp, cognitive science, and ergodicity economics each describe a single stage or dimension of the full perception pipeline.

### 5.2 Computational Implementability

A distinguishing property of SBT is that the entire framework can be executed computationally. Signals are typed data structures with dimension, source, emission type, and strength fields. Observer profiles are parameter sets with spectrum, weight, tolerance, and prior fields. Cloud formation is a weighted clustering operation. Conviction collapse is a threshold function. Re-collapse is a full recalculation from the updated evidence set.

This computational character enables AI-native implementation. The six-module analytical pipeline operates as a structured prompt sequence for large language models. In practice, a capable LLM (Claude, GPT-4, or equivalent) can execute all six modules in a single analytical session, producing:

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

2. **AI as mediation layer.** Algorithms increasingly mediate between brand signals and human observers. Social media feeds, recommendation engines, and search results filter which signals reach which observers. This mediation layer is itself a spectral filter — it changes which signals are visible to which cohorts based on platform-specific algorithmic logic.

3. **AI as synthetic observer.** LLM-powered recommendation systems ("what EV should I buy?") are a new class of observer with their own spectral profile: trained on text (biased toward narrative and ideological signals), weak on experiential and semiotic signals, and operating without tolerances or identity gates. These synthetic observers will increasingly influence human purchase decisions.

SBT accommodates all three changes within its existing architecture. The analytical pipeline was designed for AI execution from inception. The observer model includes encounter modes (direct, mediated, mixed) that capture algorithmic mediation. The signal taxonomy includes synthetic as a source type. The framework does not need to be retrofitted for the AI era because it was built for it.

### 5.4 Limitations and Future Directions

Several limitations warrant discussion.

**Weight validation.** Observer dimensional weights are currently expert estimates. While behavioral inference provides defensible ranges — particularly for polarized brands where stated purchase behavior makes priorities visible — empirical validation through conjoint analysis, behavioral experiments, or large-scale survey data would strengthen the framework's credibility.

**Cross-brand calibration.** Cloud confidence scores and coherence metrics are calibrated within each brand analysis but not across brands. Developing an absolute scale — or at minimum, calibration benchmarks across brand categories — is a priority for future work.

**Temporal dynamics.** The framework captures snapshots and simulates disruptions but does not formally model the rate of change. Two temporal properties require formalization: (1) *signal decay* — how individual signal contributions to cloud formation attenuate over time, with decay rates varying by emotional intensity, encounter mode (direct experiential signals persist longer than mediated ones), and reinforcement frequency; and (2) *cohort velocity* — growth rate and conviction migration speed metrics for longitudinal cohort tracking. Signal decay is particularly important because it makes cloud formation recency-weighted: the "evidence set" available at any moment of re-collapse is not the complete historical set but the set of signals that have survived temporal attenuation plus whatever has crystallized into permanent priors.

**Competitive analysis.** The current framework analyzes brands in isolation. Extending the model to competitive contexts — how Brand A's signal environment interacts with Brand B's in the same perceptual space — is a natural extension that the dimensional architecture supports but that has not been validated.

**Temporal compounding.** Our cross-brand comparison reveals that heritage compounds non-linearly — 20 years of heritage is supplementary, 50 years is moderate, 80 years approaches a compounding threshold, and 180+ years becomes the foundational architecture on which all other dimensions rest. Formalizing this compounding curve as a mathematical function within the temporal dimension model would strengthen the framework's predictive capacity.

**Non-ergodic dynamics.** Brand perception operates as a multiplicative, path-dependent process: each new signal multiplies (rather than adds to) an observer's existing cloud confidence. This makes brand perception structurally non-ergodic in Peters' (2019) sense — what happens to the "average observer" in a cross-sectional survey does not predict any individual cohort's perceptual trajectory over time. Introducing an ergodicity coefficient per brand-dimension pair — measuring the degree to which ensemble metrics reliably predict individual cohort trajectories — would strengthen the framework's diagnostic capacity by identifying which dimensions can be safely measured with aggregate surveys and which require longitudinal cohort-trajectory tracking.

---

## 6. Conclusion

Spectral Brand Theory contributes a formal, computational framework for modeling brand perception as an observer-mediated process. The core claim — there is no brand-in-itself, only signals and observers — produces an analytical architecture that explains phenomena traditional frameworks cannot: how the same brand can be simultaneously powerful and fragile (Tesla), how restricting signals can create more value than emitting them (Hermès), how five qualitatively different types of brand coherence determine resilience profiles that a single coherence score cannot distinguish, and how evidence-free convictions can be more stable than evidence-rich ones.

The framework is validated across five brands spanning luxury, mass-market, mission-driven, technology, and hyperlocal categories. The validation produced 25 non-obvious, dimensionally specific, actionable, observer-differentiated insights (five per brand, formally assessed against all four criteria — see Section 3.3) — a yield that suggests the framework captures genuine structural properties of brand perception rather than producing tautological outputs.

The framework's computational implementability — executable as a structured LLM prompt sequence with open-source templates — makes multi-cohort brand analysis accessible to practitioners without custom engineering, collapsing a multi-week consulting engagement into a single analytical session. The prompt kit, YAML templates, and framework documentation are publicly available.

SBT is not a replacement for strategic judgment. It is an analytical instrument — an X-ray machine for brand architecture. It sees the structure. The strategist decides what to build.

---

## References

Aaker, D. A. (1996). *Building strong brands*. Free Press.

Aaker, D. A., & Joachimsthaler, E. (2000). *Brand leadership*. Free Press.

Barthes, R. (1957). *Mythologies*. Seuil.

Berger, J. (2013). *Contagious: Why things catch on*. Simon & Schuster.

Christodoulides, G., & de Chernatony, L. (2010). Consumer-based brand equity conceptualization and measurement. *International Journal of Market Research*, 52(1), 43–66.

Damasio, A. R. (1994). *Descartes' error: Emotion, reason, and the human brain*. Putnam.

De Chernatony, L., & McDonald, M. (2003). *Creating powerful brands*. Butterworth-Heinemann.

Eco, U. (1976). *A theory of semiotics*. Indiana University Press.

Erdem, T., & Swait, J. (1998). Brand equity as a signaling phenomenon. *Journal of Consumer Psychology*, 7(2), 131–157.

Ehrenberg, A. S. C., Goodhardt, G. J., & Barwise, T. P. (1990). Double jeopardy revisited. *Journal of Marketing*, 54(3), 82–91.

Festinger, L. (1957). *A theory of cognitive dissonance*. Stanford University Press.

Fishbein, M., & Ajzen, I. (1975). *Belief, attitude, intention and behavior: An introduction to theory and research*. Addison-Wesley.

Holt, D. B. (2004). *How brands become icons: The principles of cultural branding*. Harvard Business Press.

Kahneman, D. (2011). *Thinking, fast and slow*. Farrar, Straus and Giroux.

Kapferer, J.-N. (2008). *The new strategic brand management* (4th ed.). Kogan Page.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1–22.

Keller, K. L., & Lehmann, D. R. (2006). Brands and branding: Research findings and future priorities. *Marketing Science*, 25(6), 740–759.

Koffka, K. (1935). *Principles of Gestalt psychology*. Harcourt, Brace.

Lakoff, G. (2004). *Don't think of an elephant!* Chelsea Green.

McLuhan, M. (1964). *Understanding media: The extensions of man*. McGraw-Hill.

Muniz, A. M., & O'Guinn, T. C. (2001). Brand community. *Journal of Consumer Research*, 27(4), 412–432.

Peirce, C. S. (1931–1958). *Collected papers of Charles Sanders Peirce* (C. Hartshorne & P. Weiss, Eds., Vols. 1–6). Harvard University Press.

Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, 15, 1216–1221. https://doi.org/10.1038/s41567-019-0732-0

Ries, A., & Trout, J. (1981). *Positioning: The battle for your mind*. McGraw-Hill.

Sharp, B. (2010). *How brands grow: What marketers don't know*. Oxford University Press.

Spence, M. (1973). Job market signaling. *The Quarterly Journal of Economics*, 87(3), 355–374.

Vargo, S. L., & Lusch, R. F. (2004). Evolving to a new dominant logic for marketing. *Journal of Marketing*, 68(1), 1–17.

Veblen, T. (1899). *The theory of the leisure class*. Macmillan.

Zharnikov, D. (2026b). The atom-cloud-fact epistemological pipeline: From financial document processing to brand perception modeling. Working paper. https://github.com/spectralbranding/sbt-papers/tree/main/alibi-epistemology

---

*This is a working paper. Comments welcome at dmitry@spectralbranding.com.*

*The open-source prompt kit, YAML templates, and framework documentation are available at github.com/spectralbranding/sbt-framework. An ongoing series of analytical articles applying SBT to specific brands is published at spectralbranding.substack.com.*

*License: MIT*

---

## Citation

```bibtex
@article{zharnikov2026spectral,
  title={Spectral Brand Theory: A Computational Framework for Multi-Dimensional Brand Perception},
  author={Zharnikov, Dmitry},
  year={2026},
  url={https://github.com/spectralbranding/sbt-papers}
}
```

Also available on:
- SSRN: *(link pending)*
- [spectralbranding.substack.com](https://spectralbranding.substack.com)
