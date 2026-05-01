# AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification

**Dmitry Zharnikov**

*Working Paper v1.8.1 — April 2026*

*Zenodo DOI: [10.5281/zenodo.19391476](https://doi.org/10.5281/zenodo.19391476)*

---

**Abstract**

Brand identity verification technologies have historically changed discontinuously in response to shifts in the primary observer type. This paper formalizes the *observer-driven evolution thesis* and extends it to the current transition from human to AI agents. The Brand Function is defined as *f*(query, context, observer_type, time) → response, constituting the complete behavioral specification required for machine observers. Cryptographic signatures on this function are predicted to replace logos as the primary identity mechanism for text-primary AI agents.

The framework introduces *behavioral metamerism* --- the condition in which brands converge on statistically indistinguishable profiles while differing in structurally relevant behavioral contingencies --- an equivalence that statistical optimization (including generative engine optimization) cannot resolve. Six falsifiable propositions link observer type to identity technology, specification to coherence, and cryptographic attestation to computational trust.

Existing protocols address discovery and transaction but omit perception measurement, behavioral specification, and coherence verification. The Brand Function fills these gaps by integrating spectral perception dimensions, observer-contingent decision rules, and computable coherence metrics. The analysis implies that brands must develop dual identity infrastructure: visual for humans, cryptographically attested behavioral specifications for machines. Theoretical contributions reposition brand equity as observer-contingent; managerial implications center on verifiable behavioral contracts that reduce adverse selection and moral hazard in delegated purchasing.

**Keywords**: brand identity, AI agents, cryptographic verification, behavioral specification, metamerism, agentic commerce, generative engine optimization, observational equivalence

---

Every time the observer of brand identity changed, the verification technology changed with it. Wax seals authenticated documents for literate officials. Hallmarks guaranteed metal purity for buyers who could not assay it themselves. Trademarks enabled recognition in anonymous mass markets. SSL certificates proved server identity to web browsers. The logo --- the dominant identity technology of the 20th century --- was designed for a specific observer: the human consumer navigating scaled markets through visual and emotional pattern matching.

That observer is changing. AI purchasing agents --- Amazon Rufus, Google AI Mode, Perplexity Shopping, ChatGPT with agentic commerce capabilities --- are increasingly mediating product discovery, brand evaluation, and purchasing decisions. Text-primary systems of this kind do not process logos, emotional narratives, or visual brand guidelines as informational inputs to their decisions; they process structured data, behavioral patterns, and verified claims (multimodal agents are addressed separately below and in Proposition 3's caveat). A growing body of evidence documents how large language models (LLMs) form "brand perceptions" that are statistical rather than perceptual: global brands are favored due to training data frequency (Kamruzzaman et al. 2024), market-dominant products receive disproportionate recommendation (Zhi et al. 2025), and optimization strategies designed for human search engines produce diminishing returns in generative AI environments (Aggarwal et al. 2024). Current brand identity infrastructure --- the visual brand book, the logo, the tagline --- is built entirely for human observers and carries near-zero informational weight for text-primary machine observers.

Kannan and Li (2017) mapped the digital touchpoints where technology mediates the marketing process --- from search and social to mobile commerce. The AI agent is the next generation of that digital mediation, but it differs structurally from all prior digital touchpoints: it does not present information to a human who then decides, but evaluates and decides itself. The Brand Function extends the touchpoint framework Kannan and Li proposed to this agentic era, where the touchpoints are machine-to-machine and the brand must specify behavior for an observer that processes structured data rather than sensory experience.

The dominant paradigm in brand identity theory --- Keller's (1993) customer-based brand equity model, which locates brand equity in the knowledge structures of human consumers --- is built entirely for human observers. Keller's four dimensions of brand knowledge (brand awareness, brand associations, perceived quality, and brand loyalty) presuppose a human mind forming associative networks through direct and mediated experience. This human-observer assumption pervades the subsequent identity literature: Hatch and Schultz (2010) model brand co-creation as stakeholder dialogue --- a process that requires observers capable of dialogue; de Chernatony (1999) frames brand identity as the gap between management vision and consumer perception --- a formulation that loses meaning when the "consumer" is a recommendation algorithm with no perception in the phenomenological sense; Fournier (1998) extends the human-observer paradigm furthest by theorizing brands as relationship partners in consumers' lives, with relationship quality emerging from sustained dyadic interaction --- exactly the relational substrate that an AI purchasing agent, lacking biographical continuity and affective state, cannot supply. Hallinan and Striphas (2016) identify how algorithmic culture reshapes what content reaches consumers, but do not address how brands should present identity *to* the algorithms themselves. When the observer is an AI agent forming "associations" through statistical co-occurrence in training data, the Keller framework describes a process that does not apply, the Fournier relational paradigm has no counterpart on the agent side (relationships persist for human co-consumers but collapse for the AI mediator), the co-creation model loses its dialogic basis, and the vision-perception gap becomes a specification-implementation gap.

This paper identifies a gap at the intersection of three developing literatures. First, multiple protocols now address machine-readable brand identity (.well-known/brand.json, the Agentic Commerce Protocol, the Unified Commerce Protocol, Brando Schema) and cryptographic attestation (BIMI/VMC, GLEIF vLEI, GS1 Verifiable Credentials). Second, marketing scholarship has begun addressing algorithmic brand equity (Kovalenko et al. 2026), algorithmic branding through platform assemblages (Kozinets 2022), and the platformization of brand management (Wichmann et al. 2022). Third, the agentic commerce literature has identified the "Shopper Schism" --- the structural separation of the consumer (who decides what to want) from the shopper (who executes the purchase), with AI agents increasingly occupying the shopper role (Accornero 2026). Puntoni et al. (2021) identify delegation as one of four core tensions in consumer-AI interaction --- the moment when a consumer transfers purchasing authority to an AI agent. The Brand Function addresses this delegation tension directly: when consumers delegate to AI agents, the behavioral contract provided by the Brand Function becomes the mechanism through which delegated purchasing decisions can be verified against the brand's intended identity. However, no theoretical framework connects these developments by explaining *why* these technologies are emerging now, *what* is missing from them, or *how* they fit into the longer historical pattern of identity technology evolution.

This paper makes three contributions, formalized as six falsifiable propositions. First, it proposes the *observer-driven evolution thesis* --- a synthesizing framework explaining why identity technologies change discontinuously when the observer type changes. While individual histories of seals, hallmarks, trademarks, and digital certificates exist in separate literatures (Richardson 2008; Sáiz and Castro 2018; Economides 1988; Groebner 2007), no prior work theorizes this as a general pattern or uses it to predict the next identity technology. Second, it introduces the *Brand Function* as a root specification concept --- extending existing protocols, which address brand discovery and catalog, to include behavioral specification, perception measurement, and coherence verification. Existing protocols such as brand.json and Brando Schema (Bowker 2026) address creative and communication governance; the Brand Function adds behavioral specification across all touchpoints, spectral perception dimensions from Spectral Brand Theory (Zharnikov 2026a), and computable coherence metrics. Third, it introduces *behavioral metamerism* --- the phenomenon where brands produce identical statistical profiles but exhibit structurally different behavioral patterns --- as the AI-native form of brand confusion that statistical optimization cannot resolve. Six propositions connecting observer type to identity technology, specification to coherence, and cryptographic attestation to trust in autonomous commerce formalize these contributions; each carries an explicit falsification condition.

The framework is scoped to B2C agentic commerce contexts. B2B markets, where behavioral contracts already operate through procurement specifications, RFPs, and ERP integration, are likely to require modified treatment that is left for separate work. Within the B2C scope, the central claims about logo irrelevance apply most strongly to text-based and text-primary AI agents; multimodal agents are addressed in Proposition 3's caveat.

For interactive marketers, the practical implication is immediate: AI systems can no longer be treated as passive channels through which brand messages reach human consumers. They are evaluative observers whose trust must be earned through machine-verifiable behavioral contracts, not visual consistency. Managers who plan brand strategy for the next decade must account for two distinct identity systems operating in parallel --- one for humans, one for machines.

The remainder of the paper proceeds as follows. The Historical Pattern section traces the observer-driven identity technology change across five transitions. The AI Agent as Observer section examines how AI agents currently perceive brands and why current identity infrastructure fails them. The Brand Function section introduces the root specification concept and reports a supplementary format-optimization experiment. The Cryptographic Signature section develops the AI-native equivalent of the logo and grounds it in the cryptographic identity literature. The Behavioral Metamerism section introduces the core failure mode. The Necessity Conditions section establishes when the Brand Function becomes structurally required. The Implications section discusses brand management and marketing theory implications. The Limitations section addresses future research directions.

---

## Historical Pattern: Observer Determines Technology

Identity verification technologies do not evolve incrementally. They emerge in response to a change in the observer type. Five transitions establish the pattern that predicts the sixth. The examples trace the Western European genealogy that produced modern trademark law and digital identity infrastructure --- the direct ancestors of the AI commerce protocols under analysis. Non-Western identity verification traditions (Chinese chops, Islamic calligraphic seals, Indian guild marks) exist in parallel and deserve separate investigation, as the Limitations section acknowledges.

**Wax seals** served the first non-personal observer: the bureaucratic official verifying documents at a distance. Mesopotamian cylinder seals (ca. 3500 BCE) authenticated clay tablets through unique physical impressions. Medieval signet rings were destroyed upon death --- an early form of key revocation. The technology was adapted to an observer who could inspect a physical impression but lacked personal knowledge of the sender.

**Hallmarks** emerged when the observer shifted from official to commercial buyer. England's 1300 statute required silver to be assayed at Goldsmiths' Hall before sale, introducing trusted third-party attestation. The buyer needed only to recognize an institutional mark, not possess metallurgical expertise. Wax seals persisted for legal documents but were irrelevant for commercial quality verification.

**Trademarks** responded to the Industrial Revolution's anonymous consumer. Pre-industrial craft marks identified known local makers (Richardson 2008); mass production broke this link. Trademarks carried abstract associations --- quality, emotion, culture --- rather than certifying physical properties (Schechter 1925; Economides 1988). Aaker (1996) and Kapferer (2008) codified this mature form into brand identity systems designed for a specific observer: the human consumer forming associations through sensory experience. The logo is the mature expression of this technology.

**Holograms** are instructive because the observer did *not* change. When industrialized counterfeiting intensified the threat but the observer remained human, the response was incremental --- adding optical verification features to the existing visual paradigm. Discontinuous technology change required a change in the observer itself.

**SSL certificates** (Netscape 1994) marked the decisive break. For the first time, the primary identity observer was a software program --- the web browser. Verification became mathematical rather than perceptual, binary rather than graded, and scalable without human attention. Logos persisted on websites but carried zero weight in the browser's trust decision. This transition established the template: when the observer is a machine, the identity technology must be verifiable by computation, not perception.

**Proposition 1: Identity verification technology characteristically changes not through incremental improvement but through discontinuous response to a change in the observer type.**

*Falsification*: P1 is falsified if the current AI-observer transition produces only incremental extensions of existing logo-based identity (e.g., animated logos for AI agents, richer metadata on existing visual marks) rather than a structurally different verification mechanism. If logo-based identity proves sufficient for AI agents across multiple commerce categories, the discontinuity thesis fails.

**Proposition 2: When the observer changes, the previous identity technology persists for legacy observers but becomes functionally irrelevant for the new observer class.**

*Falsification*: P2 is falsified if AI agents demonstrably use logos as informational inputs in purchasing decisions --- not merely recognizing them as identifiers but weighting visual brand identity in recommendation quality. If logo presence/absence meaningfully affects AI recommendation accuracy, the irrelevance claim fails.

The historical evidence supports both propositions. Wax seals persist in legal ceremonies; hallmarks persist in precious metals regulation; logos persist on websites despite SSL certificates handling actual identity verification. Each technology remains functional for its original observer class while becoming irrelevant for the new one. The question for marketing theory is: what happens when the observer changes again?

---

## The AI Agent as Observer

The sixth observer type is the AI agent. Unlike the web browser, which verified identity as a binary trust decision before displaying content for human evaluation, AI agents increasingly make substantive brand evaluations --- comparing products, generating recommendations, executing purchases --- with varying degrees of human oversight. In the taxonomy of Huang and Rust (2021), the AI purchasing agents examined here operate primarily at the "thinking AI" level --- processing structured data to arrive at purchasing decisions --- though emerging multimodal capabilities may introduce "feeling AI" components that the Brand Function's multi-dimensional specification anticipates. This section examines how AI agents currently perceive brands, what evidence exists for systematic bias in their evaluations, and why current optimization strategies are structurally insufficient.

### How AI Agents Currently "See" Brands

AI purchasing agents process brand identity through structured data, behavioral signals, and third-party corroboration --- none of which involves visual recognition. Current platforms illustrate the pattern:

*Amazon Rufus* draws primarily on Amazon's internal structured catalog, including product attributes, reviews, Q&A content, pricing competitiveness, and seller performance metrics. A brand's identity to Rufus is its aggregated review profile, fulfillment reliability, and catalog completeness. Industry analyses suggest that products below a four-star rating with fewer than approximately 9,000 reviews receive substantially reduced recommendation frequency.

*Google AI Mode* leverages the Shopping Graph, which integrates over 50 billion product listings with approximately 2 billion updates per hour from Merchant Center feeds, schema.org markup, and web data. Brand identity is a function of structured attribute completeness, pricing consistency, review quality, and freshness of availability data.

*Perplexity Shopping* emphasizes citation-driven evaluation, drawing on third-party earned media, authoritative web sources, and pricing consistency. A brand that lacks authoritative third-party coverage is effectively invisible regardless of its visual identity strength.

*ChatGPT with agentic commerce* uses the Agentic Commerce Protocol (ACP) for checkout and payment delegation, Stripe integration for transaction processing, and product feeds for discovery. Brand identity is whatever the structured data says it is.

Across all platforms, the text-primary AI agents surveyed here evaluate brand identity through data provenance, behavioral consistency, and structural completeness; the logo carries near-zero informational weight in this regime. Comprehensive schema.org markup --- the structured-data infrastructure documented by Guha, Brickley, and MacManus (2016) --- can increase recommendation likelihood substantially, while visually striking brand identities with poor structured data are systematically disadvantaged. Tomaino et al. (2022), studying how consumers attribute human-like qualities to AI assistants, found that anthropomorphic framing meaningfully alters consumer trust calibration --- yet text-primary purchasing agents have no perceptual channel for visual brand cues, making anthropomorphic brand logos structurally inaccessible to the evaluative mechanism that drives recommendations. The failure of logos for text-primary AI agents is not a gap in AI capability but a structural consequence of how these agents process information.

### LLM Brand Bias as Evidence of Statistical Perception

If AI agents formed brand perceptions through genuine understanding, their evaluations would reflect product quality independent of training data distribution. Empirical evidence contradicts this.

Kamruzzaman et al. (2024), in a systematic study published at EMNLP, demonstrated that LLMs exhibit strong brand bias correlated with training data frequency: global brands are recommended disproportionately over local alternatives, luxury brands are recommended 88--100% of the time for high-income country queries, and geographic and economic skew systematically distorts recommendations. The mechanism is statistical: brands that appear more frequently in training corpora receive higher probability mass in generative outputs, independent of objective quality.

Zhi et al. (2025) extended this finding to investment recommendations, showing that market-dominant products receive amplified recommendation due to neural reinforcement --- a feedback loop where training data frequency creates recommendation bias, which generates more user interaction data, which further amplifies the bias. The effect is structural: it operates through the statistical properties of the model's learned representations, not through any process analogous to human brand evaluation.

Complementary evidence comes from the agent evaluation literature. Lyu et al. (2025) benchmark AI shopping agents on task completion --- whether the agent can find the right product given multi-attribute queries with filters and sorting preferences across five product categories. Even the best deep research systems achieve only 30% holistic task success, and performance drops sharply with query complexity. This establishes that current AI agents fail at the navigation level before perception is even at issue. DeepShop evaluates agent *capability* (can it complete the task?) but not agent *perception* (does it perceive the brand correctly?). The present paper addresses the perception gap: the Brand Function provides the specification layer that ensures that when AI agents do successfully locate products, they also correctly represent the brand's multi-dimensional identity to the consumer. For empirical measurement of the perceptual failure mode, see Zharnikov (2026v).

These findings establish that LLM "brand perception" is fundamentally different from human brand perception. Humans form brand convictions through multi-sensory experience, social influence, personal history, and emotional resonance --- processes that SBT models as observer-specific spectral weighting across eight dimensions (Zharnikov 2026a). LLMs form "brand representations" through statistical co-occurrence patterns in text corpora. This distinction is consequential: it means that the identity infrastructure humans use (visual consistency, emotional narrative, brand experience) does not transfer to AI observers. De Bruyn et al. (2020), in a foundational JIM analysis of AI in marketing, identified biased AI and badly defined objective functions as structural pitfalls of AI marketing systems --- behavioral metamerism is a direct consequence of both, arising when brands optimize for the same statistical objective (GEO visibility) and the AI's learned representations inherit training-data frequency bias.

The broader JIM conversation on AI-mediated marketing has established both the promise and structural risks of this transition. Ramesh and Chawla (2022) survey the chatbot marketing literature and identify brand personality transfer as a critical gap --- chatbots can simulate brand voice but cannot verify brand identity, precisely the verification problem this paper formalizes. Pagani and Wind (2024) argue that AI unlocks marketing creativity but requires new governance frameworks to manage the loss of human oversight --- a governance challenge that the Brand Function specification (Cryptographic Signature section) directly addresses. Shankar and Balasubramanian (2009) anticipated many of these dynamics in the mobile marketing context, noting that as marketing channels shift from human-centric to technology-mediated, identity verification mechanisms must evolve correspondingly.

### Generative Engine Optimization as Symptom

Generative Engine Optimization (GEO) --- the practice of optimizing content for visibility in AI-generated responses rather than traditional search rankings --- represents the first systematic attempt by brands to be "seen" by AI observers. Aggarwal et al. (2024) introduced the GEO framework at KDD, demonstrating that strategies such as citation addition, statistics incorporation, and authoritative source references can increase brand visibility in generative AI outputs by up to 40%. Acar and Schweidel (2026) document cases in practitioner research where LLMs miscategorize brand positioning --- a prestige Scotch brand (Ballantine's) described as a mass-market offering --- providing real-world evidence for the systematic AI misperception that the present paper theorizes as behavioral metamerism.

However, GEO addresses a symptom rather than the underlying structural problem. GEO optimizes for *statistical visibility* --- increasing the probability that a brand appears in generative outputs. It does not address *identity verification* --- establishing that the brand is who it claims to be and behaves as it specifies. This distinction is critical. A brand can achieve high GEO scores through content optimization while having no machine-verifiable identity, no behavioral specification, and no way for an AI agent to verify that the entity it encounters is the entity it represents itself to be.

Furthermore, GEO creates a convergence dynamic. As brands in the same category adopt similar GEO strategies --- adding citations, incorporating statistics, optimizing for the same query patterns --- their statistical profiles converge. This convergence is precisely the condition that produces behavioral metamerism, which the Behavioral Metamerism section develops in detail.

**Proposition 3: AI agents do not perceive brand identity through visual recognition but through structured data evaluation, behavioral pattern analysis, and third-party corroboration. The logo carries near-zero informational weight for text-based AI agents, and minimal informational weight in text-only AI mediation more broadly.**

*Caveat on multimodal agents*: Multimodal AI agents (GPT-4V, Gemini Vision) do process visual elements including logos, packaging, and color. The near-zero weight claim applies specifically to text-based agents operating through structured data and language models. As multimodal agents gain commerce capabilities, the visual identity layer may recover partial informational weight --- though the structural data and behavioral specification layers are predicted to remain primary.

*Falsification*: P3 is falsified if multimodal AI agents that process visual brand elements (logo, packaging, color) make measurably better purchasing decisions than text-only agents with identical structured data. If visual brand identity provides incremental information value to AI agents beyond what structured data conveys, the "near-zero weight" claim is too strong.

---

## The Brand Function

If AI agents perceive brands through behavioral patterns rather than visual marks, then the brand needs a behavioral specification --- a machine-readable, verifiable description of how it operates. This section introduces the Brand Function as the root specification from which all brand emissions derive, examines the current protocol landscape, and identifies what existing specifications fail to address.

### The Brand Function as Root Specification

In software engineering, the specification defines correct behavior before implementation begins. A system without a specification cannot be verified, tested, or audited --- one can detect anomalies relative to past behavior but cannot determine whether the behavior conforms to the system's intended purpose (Dijkstra 1970; Clarke et al. 1999). The same principle applies to brands.

The Brand Function is defined as:

> *f*(query, context, observer_type, time) -> response

Where *query* is what an observer (human or machine) is asking of the brand; *context* is the observer's state, including prior knowledge, optimization objectives, and interaction history; *observer_type* distinguishes among humans, AI purchasing agents, AI research agents, AI comparison agents, and other observer classes; and *response* is the structured output that carries the brand's behavioral signature.

The Brand Function is the root specification from which all brand emissions and identity artifacts derive. This framing makes a deliberate architectural claim: *technologies are the primary rendering engines of brand behavior; the organization is coordination overhead*. When brand behavior is rendered through an API response, a pricing algorithm, a chatbot interaction, or a smart contract, the technology implements the Brand Function directly. The organizational structure --- the people, processes, and hierarchies that coordinate brand behavior --- is a necessary but lossy intermediary that introduces what Spectral Brand Theory terms a "specification gap" between intended and actual behavior (Zharnikov 2026a).

This distinction has a precise structural form. The Brand Function is an *output specification* --- it defines *WHAT* the brand produces: the response to a query, the quality criteria the response must meet, and the acceptance conditions by which an observer determines conformance. The internal rendering pipeline --- organizational processes, approval hierarchies, supply chain logistics, technology stack --- is a *coordination specification*, defining *what to DO* to produce that output. AI agents can read the WHAT and evaluate whether a brand's behavior conforms to it; they cannot read the DO, because coordination specifications are internal and do not constitute brand identity claims. The irreducibility of the Brand Function follows: it is the WHAT layer that neither AI nor delegation can compress away, while the DO layers are precisely what agentic execution compresses toward zero.

This parallels Parasuraman et al.'s (1985) SERVQUAL Gap 2 (the difference between management perception of consumer expectations and service quality specifications), but extends it: the specification gap applies not only to service delivery but to all brand emissions, and it is computable rather than subjective.

As AI agents increasingly render brand behavior directly --- through autonomous commerce, API-first interactions, and algorithmic decision-making --- the organizational layer thins. The Brand Function persists across all rendering engines; the organization is just one (lossy) implementation.

The Brand Function serves a role analogous to satellite ephemeris data in GPS: it provides the positioning information that enables AI observers to fix a brand's location in perception space. Without ephemeris data, a GPS receiver cannot compute position from satellite signals; without a Brand Function, an AI agent cannot compute brand identity from statistical signals alone.

### Three Levels of Machine-Readable Brand Identity

Existing approaches to machine-readable brand identity operate at three levels of specification depth:

*Level 1: Brand-Code (visual function).* This is the visual identity rendered as an executable function: f(signals, observer_position, time) -> visual_output. Brand style guides operationalized as code (color palettes, typography, spatial rules) already exist in design systems. This level specifies how the brand looks but not how it behaves.

*Level 2: Brand Specification (behavioral constraints).* This level partially exists across several emerging standards (detailed in the Current Protocol Landscape subsection). It specifies elements of brand behavior for machine consumption: product catalog, pricing, availability, communication style, content policies. But current specifications address commerce mechanics --- what a brand sells and how to buy it --- not behavioral identity.

*Level 3: Brand Function (complete behavioral specification).* This level does not yet exist as a standard. It would specify not only what the brand sells and how it communicates but how the brand behaves across all touchpoints for all observer types --- including decision rules, escalation behavior, refusal conditions, edge-case handling, and how behavior varies by observer type. It includes the brand's spectral profile (its eight-dimensional emission pattern per SBT), coherence targets (the acceptable distance between specified and actual behavior), and behavioral invariants (properties that must hold across all renderings).

The distinction between Level 2 and Level 3 is the difference between a product catalog (what exists) and a behavioral contract (what is needed). AI agents operating with delegated purchasing authority need to know not only what a brand sells but how the brand will behave in unspecified situations --- precisely the contingencies that Level 2 specifications leave unresolved.

### The Current Protocol Landscape

Multiple protocols now address aspects of machine-readable brand identity:

The *Agentic Commerce Protocol (ACP)*, developed by OpenAI and Stripe (2025), enables agentic checkout with delegated payment tokens. It is open-source and transaction-focused, specifying how an AI agent can discover products and complete purchases.

The *Unified Commerce Protocol (UCP)*, developed by Google and Shopify (2026), addresses the full commerce lifecycle through a .well-known/ucp manifest, covering discovery, catalog, checkout, and fulfillment.

The *Model Context Protocol (MCP)*, developed by Anthropic (2024), provides a general tool and resource protocol for AI-to-service connections, enabling AI agents to interact with external services through standardized interfaces.

The *Agent-to-Agent Protocol (A2A)*, developed by Google (2025) and contributed to the Linux Foundation, enables agent-to-agent communication through AgentCard JSON documents that describe agent capabilities and identity.

The *.well-known/brand.json* proposal, advanced by the AgenticAdvertising.org consortium through the Ad Context Protocol (AdCP), specifies a brand manifest at the domain level, including creative guidelines, voice parameters, and brand assets for AI consumption.

*Brando Schema* (v1.3), developed by Bowker (brandoschema.com), provides a JSON-LD vocabulary extending Schema.org for brand governance, including toneOfVoice, guardRails, contexts, and policy graphs. It is the closest existing specification to the Brand Function concept, advancing a "Brand-as-Code" paradigm for creative and communication governance.

These protocols form an emerging stack: static manifests (brand.json) -> tool connections (MCP) -> agent negotiation (A2A) -> commerce transactions (ACP, UCP). Collectively, they address two aspects of brand identity: *who* the brand is (identity attestation) and *what* it sells (catalog and commerce). But they do not address three aspects that are essential for brand identity verification by AI agents.

### What the Brand Function Adds

Existing protocols leave three gaps that the Brand Function fills:

*Perception measurement.* No existing protocol includes analysis of how the brand is perceived across dimensions by different observer cohorts. SBT's eight-dimensional spectral profile --- measuring brand emissions along Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal dimensions (Zharnikov 2026a) --- provides a perceptual measurement layer that no commerce or identity protocol addresses. Including spectral profiles in the Brand Function enables AI agents to recognize that a brand has multi-dimensional identity --- the structural awareness that Run 14 of the R15 experimental program (Zharnikov 2026v) shows is the operative mechanism, rather than per-dimension signal granularity.

*Behavioral specification beyond commerce.* Current protocols specify commerce mechanics. The Brand Function extends to all behavioral touchpoints: communication style parameters, decision rules for edge cases, content policies, escalation behavior, refusal conditions, and how behavior varies by observer type. This is the difference between telling an AI agent "here is our product catalog" and telling it "here is how we behave."

*Coherence measurement.* The specification gap --- the distance between Brand Function and actual rendered behavior --- becomes a computable metric. SBT's coherence hierarchy (ecosystem coherence > signal coherence > identity coherence > experiential asymmetry > incoherent) can be operationalized as a function of the distance between the Brand Function's specified behavior and the brand's actual behavior as measured across touchpoints. No existing protocol provides this measurement capability.

The Brand Function is therefore not a competing protocol but a theoretical construct that identifies the missing layer: Brando Schema addresses creative and communication governance; the Brand Function extends this to behavioral specification, perception measurement, and coherence verification --- the layers that existing protocols do not cover. Empirical evidence from Run 14 of the R15 experimental program (Zharnikov 2026v) confirms that the specification effect operates at the structural level: enriching specific dimensions with additional signal detail does not reduce per-dimension collapse beyond what the standard Brand Function already achieves, indicating that the operative mechanism is informing the model that multi-dimensional identity exists, not the granularity of per-dimension description.

**Proposition 4: The Brand Function is the root specification from which all brand emissions and identity artifacts derive. Technologies are the primary rendering engines; in this framework, organizational structure functions as coordination overhead relative to the Brand Function specification. Existing AI commerce protocols (ACP, UCP, brand.json) address brand discovery and transaction but not brand perception or coherence --- the Brand Function extends them by adding spectral dimensions, behavioral specification, and coherence measurement.**

*Falsification*: P4 is falsified if existing protocols (brand.json, Brando Schema, ACP) prove sufficient for AI agents to measure brand coherence and predict behavioral responses without additional specification layers. If platforms successfully verify brand identity and measure perception using only the constructs these protocols already provide, the Brand Function adds no incremental value.

### Brand Function Format Optimization (Supplementary)

A supplementary experiment tested whether the structural *format* of the Brand Function affects its effectiveness as an identity signal for AI observers. The full JSON document --- containing dimensional scores, positioning text, and key signals --- is the canonical proposed form; comparing it against alternative encodings establishes whether structure or content carries the identity signal for machine observers.

**Design.** Two runs tested five format conditions: F1 = JSON (scores + positioning + key signals), F2 = prose narrative, F3 = tabular, F4 = ranked list, and F5 = score-only vector. Each run crossed 5 brands x 5 formats x 5 models x 3 replications = 375 calls. Run 1 revealed input leakage: formats exposing raw numerical scores (F3, F4, F5) produced near-echo responses, with F5 exhibiting 89% near-echoes and an artificially inflated cosine of .998. Run 2 corrected this by replacing raw scores with text descriptions (F3), ranked text without scores (F4), and qualitative ordinal levels --- "Very High," "High," "Moderate," "Low," "Very Low" --- (F5). A sum-enforcement instruction ("weights MUST sum to exactly 100") was added to all conditions. Run 2 returned 375 valid responses (100% completion), total cost $0.13.

**Results.** Format explained a medium-large share of variance in cosine fidelity to canonical brand profiles: *F*(4, 370) = 18.516, *p* < .001, eta-sq = .167. The format ranking by mean cosine was: F5 qualitative levels (.978) > F1 JSON (.973) > F4 ranked text (.954) > F2 prose (.944) > F3 tabular descriptions (.935). The structured-format advantage hypothesis (JSON outperforms all alternatives) was not supported --- F5 qualitative levels slightly exceeded F1 JSON, though the difference was non-significant (*d* = -.095). The prose penalty hypothesis was supported: F1 versus F2 yielded *d* = .608, *p* < .001 after Bonferroni correction. Cross-model consistency was high (Kendall's W = .84), and weight-sum compliance improved from 55.5% in Run 1 to 87.7% within the 95--105 tolerance band in Run 2.

**Interpretation: the anchoring discovery.** The contrast between Run 1 and Run 2 is the central finding. Run 1's .998 cosine for bare scores was input leakage, not comprehension; once scores were removed, the ranking shifted to favor *information richness* over *structural precision*. Qualitative ordinal levels and full JSON both achieve high fidelity because both convey the relative standing of dimensions without triggering score echoing. Prose hurts because it introduces interpretive noise --- the model must extract dimensional weights from narrative, a lossy transformation that degrades fidelity (*d* = .608 penalty relative to JSON). This result is the input-side counterpart to the output-side finding in Zharnikov (2026aa), where ordinal response scales outperform free-form text: across both the specification layer (input) and the measurement layer (output), structured formats dominate prose for AI observers. (Results are from prompted LLM response experiments; generalizability to deployed agentic commerce contexts requires further validation.)

**Implications for the Brand Function specification.** For machine consumption, dimensional scores or their qualitative ordinal equivalents carry the identity signal; the positioning text and key signals that the full JSON format includes do not measurably improve AI comprehension fidelity. However, the full specification remains valuable for three functions that the experiment did not test: (1) human auditability --- stakeholders reviewing the Brand Function need interpretive context that bare scores cannot provide; (2) cross-observer calibration --- the positioning text anchors dimensional scores to behavioral intent, enabling the admissibility judgments described in the When Necessity Holds subsection; and (3) documentation of brand intent for governance and dispute resolution. The Brand Function specification thus serves dual audiences: for machine consumption, the dimensional scores carry the signal; for human stakeholders, the positioning text provides interpretive context. Organizations implementing Brand Functions should ensure that both layers are present, recognizing that the machine-facing and human-facing layers serve structurally different purposes.

---

## Cryptographic Signature as AI-Native Logo

If the Brand Function is the specification, it needs an identity attestation --- a mechanism for AI agents to verify that the specification they encounter actually belongs to the brand it claims to represent. For human observers, the logo serves this function (imperfectly). For machine observers, the cryptographic signature serves it (precisely).

### From Reputation to Verification

Human trust in brands operates through reputation: a slow, lossy, socially mediated process of accumulated experience. A consumer's trust in Nike is built over years of product experience, advertising exposure, peer endorsement, and cultural association. This reputation-based trust is powerful but has structural limitations: it is fragmented across individuals and contexts, subject to cognitive biases, and impossible to transfer perfectly from one observer to another.

Machine trust operates through a fundamentally different mechanism: cryptographic verification. Gligor and Wing (2011) distinguished behavioral trust (human: based on observed behavior, reputation, and social preferences) from computational trust (machine: based on cryptographic proofs, signature verification, and mathematical guarantees). Computational trust is instant rather than accumulated, lossless rather than noisy, and scalable without degradation. Sabater and Sierra (2005), in their foundational review of computational trust and reputation models, documented the growing divergence between human trust mechanisms (which rely on social context and subjective assessment) and machine trust mechanisms (which rely on formal verification and cryptographic primitives). Josang, Ismail, and Boyd (2007), surveying online trust and reputation systems for the IS literature, identify the structural limitations of reputation-based trust at scale --- Sybil attacks, cold-start problems, whitewashing, and unfair ratings --- precisely the failure modes that AI purchasing agents inherit when they depend on platform reputation signals alone.

Marketing scholarship on trust has emphasized relational, commitment-based mechanisms (Morgan and Hunt 1994); the computational trust modeled here is structurally distinct --- mathematical proof rather than accumulated relational evidence --- suggesting that AI-mediated commerce requires a different theoretical vocabulary for trust than the relationship marketing tradition provides. For an AI purchasing agent making decisions with delegated authority, reputation-based trust is structurally inadequate. The agent cannot accumulate personal experience across platforms, cannot read social cues, and cannot fall back on human judgment for every decision without negating the efficiency gains of autonomous commerce. What the agent needs is verification: a mathematical proof that the entity it is interacting with is the entity it claims to be, and that its specified behavior matches a signed specification.

### Cryptographic Identity Foundations

The cryptographic verification proposal advanced here draws on a well-developed scholarly tradition that the marketing literature has not yet engaged. Diffie and Hellman (1976) established the mathematical foundation for public-key cryptography --- the asymmetric primitive that makes signatures unforgeable without the private key and verifiable by anyone with the public key. Cameron's (2005) Laws of Identity articulated seven design principles (user control, minimal disclosure, justifiable parties, directed identity, pluralism of operators, human integration, consistent experience) that any identity system, including the Brand Function, should satisfy --- the tiered disclosure proposal advanced in the Limitations section is an application of Cameron's minimal disclosure law to organizational brand identity. Allen's (2016) Path to Self-Sovereign Identity formalized ten SSI principles that motivated the W3C DID/VC stack the present paper builds on. Tobin and Reed's (2017) Sovrin specification provided the first architectural treatment of decentralized organizational identity --- the precedent for the GLEIF vLEI infrastructure cited above --- and frames the trust-anchor governance debate (CA-based versus DID-based attestation) that the Brand Function leaves architecture-agnostic. Schema.org's evolution (Guha, Brickley, and MacManus 2016) traces how structured data infrastructure succeeds through pragmatic adoption incentives rather than technical elegance, a precedent directly relevant to the adoption pathway predicted for the Brand Function.

The Brand Function's contribution against this tradition is additive: where SSI and verifiable credentials attest *who* an organization is, the Brand Function adds a layer attesting *how* the organization specifies it will behave for a given observer type. The credential payload extends from organizational identity to behavioral specification.

### Existing Cryptographic Brand Infrastructure

The infrastructure for cryptographic brand identity is already being deployed, though not yet as a unified system:

*BIMI/VMC (Brand Indicators for Message Identification / Verified Mark Certificates)* represents the first public key infrastructure deployment for brand (not just domain) identity. Deployed in Gmail and Apple Mail, BIMI allows brands to display their verified logo alongside authenticated emails. The Verified Mark Certificate, issued by a certificate authority after trademark verification, cryptographically attests that the logo belongs to the trademark holder. BIMI is important because it bridges visual identity (the logo) with cryptographic verification (the certificate) --- but it only applies to email and only verifies logo ownership, not behavioral specification.

*GLEIF vLEI (verifiable Legal Entity Identifier)* provides cryptographically verifiable organizational identity, standardized through ISO 17442-3:2024. It enables machine-readable, instantly verifiable attestation that an entity is who it claims to be in legal and financial contexts.

*GS1 Verifiable Credentials* enable cryptographic attestation of brand and product ownership, linking products to their authorized manufacturers through verifiable credential chains built on W3C standards (W3C 2022; W3C 2025).

*The Aura Blockchain Consortium*, founded by LVMH, Prada, and Cartier, provides luxury product authentication through blockchain-based digital product passports, enabling provenance tracking and authenticity verification for high-value goods.

These deployments demonstrate that cryptographic brand verification is technically feasible and commercially motivated. What they lack is integration with behavioral specification: they verify *who* the brand is but not *how* the brand specifies it will behave.

### The Signature as Logo

The parallels between the logo and the cryptographic signature illuminate the nature of the transition:

Table 1: Comparison of Human Logo and AI Cryptographic Signature as Identity Mechanisms.

| Property | Human Logo | AI Signature |
|---|---|---|
| Recognition mechanism | Visual pattern matching | Cryptographic verification |
| Forgery resistance | Low (logos can be copied) | Mathematically unforgeable |
| Consistency verification | Subjective ("does this look on-brand?") | Computable ("does behavior match specification?") |
| Observer requirement | Human visual system | Any system with the public key |
| Degradation | Lossy (poor reproductions, off-brand uses) | Binary (valid or invalid) |
| Update mechanism | New brand-book, retrain all stakeholders | New signed specification, instant propagation |

*Notes*: AI = artificial intelligence. The contrast is constructed from the protocol literature reviewed in the text (BIMI/VMC, GLEIF vLEI, GS1 Verifiable Credentials, W3C DID/VC standards) and applies to text-primary AI agents; multimodal agents that process visual elements are addressed in Proposition 3's caveat.

The logo tells a human "I am Nike" through perceptual recognition. The cryptographic signature tells a machine "I am Nike" through mathematical proof --- and unlike the logo, the signature is unforgeable and the behavioral match between specification and actual behavior is verifiable. Where the logo's effectiveness depends on the observer's prior exposure, memory, and perceptual acuity, the signature's effectiveness depends only on access to the public key and the computational resources to verify it.

This is not a metaphor. It is a structural parallel to the SSL certificate transition: just as SSL certificates replaced the visual cues that humans used to assess website trustworthiness (design quality, professional appearance) with machine-verifiable cryptographic proofs, the Brand Function signature replaces the visual cues that humans use to assess brand identity (logos, trade dress, brand experience) with machine-verifiable behavioral attestation.

**Proposition 5: Cryptographic signatures on behavioral specifications will replace logos as the primary brand identity mechanism for AI-mediated commerce, following the historical pattern where each observer-type change produces a new identity technology.**

*Falsification*: P5 is falsified if AI-mediated commerce scales to substantial market share (>20% of category transactions) without adopting cryptographic brand verification --- i.e., if reputation systems, platform ratings, or statistical optimization prove sufficient for AI agents to establish brand trust without behavioral attestation. The prediction is conditional on agentic commerce adoption; if human-mediated purchasing remains dominant, P5's precondition is not met.

---

## Behavioral Metamerism

The previous sections established that AI agents perceive brands through statistical and behavioral patterns rather than visual recognition, and that cryptographic signatures on behavioral specifications provide the identity attestation mechanism. This section introduces a failure mode that statistical optimization cannot resolve: behavioral metamerism.

### From Color to Behavior

Metamerism in color science refers to the phenomenon where two stimuli with different spectral power distributions produce identical tristimulus values --- and thus appear perceptually identical --- under a specific illuminant and observer, despite being physically different (Wyszecki and Stiles 1982). The mechanism is dimensional collapse: human color vision relies on only three cone types, collapsing infinite spectral variation into a three-dimensional match. Two surfaces with different reflectance spectra can appear identical when their spectra, integrated against the three color-matching functions, yield the same tristimulus coordinates. No amount of observation through those three channels can distinguish them.

Zharnikov (2026e) applied this structure to brand perception, demonstrating that brands with identical aggregate perception scores can have structurally different spectral profiles when measured across SBT's eight dimensions --- spectral metamerism in brand perception. The present paper extends this concept from perceptual space to behavioral space.

*Behavioral metamerism* occurs when two brands produce identical statistical profiles --- the same topic distributions, sentiment patterns, engagement metrics, and GEO optimization scores --- but exhibit structurally different behavioral patterns. Just as color metamerism arises because observation collapses high-dimensional spectral information into low-dimensional tristimulus values, behavioral metamerism arises because statistical observation collapses high-dimensional behavioral patterns into low-dimensional aggregate metrics.

Consider two competing brands in the same product category, both optimizing for AI visibility through similar GEO strategies. Their statistical profiles converge: similar topics, similar sentiment, similar citation patterns, similar review distributions. An AI agent evaluating these brands through statistical observation alone cannot distinguish them --- not because the brands are identical, but because the observational channel (aggregate statistics) collapses the differences.

Yet the brands may differ fundamentally in how they handle edge cases, resolve disputes, adjust pricing under competitive pressure, respond to supply chain disruptions, or communicate during service failures. These behavioral differences are consequential for an AI purchasing agent making decisions on behalf of a principal, but they are invisible to statistical observation.

### Formal Definition

Behavioral metamerism is formalized using the structure of observational equivalence from econometrics (Koopmans 1949; Manski 1995).

Let *f*: Q x C x O x T -> R denote a Brand Function mapping queries, contexts, observer types, and time to behavioral responses. Let G = {*g*_1, *g*_2, ..., *g*_k} denote the set of observable aggregate statistics available to an AI agent (topic distributions, sentiment scores, citation counts, review distributions, engagement metrics).

**Definition (Behavioral metamerism).** Two Brand Functions *f*_1 and *f*_2 are *behaviorally metameric* with respect to observation set G if:

E[*g*(*f*_1)] = E[*g*(*f*_2)] for all *g* in G

while there exists at least one behavioral dimension *h* not in G such that *f*_1(*h*) != *f*_2(*h*).

The metamerism condition holds when the observation set G is informationally incomplete --- when it collapses the full behavioral space into a lower-dimensional statistical summary. This is structurally identical to color metamerism, where the three-channel human visual system collapses infinite spectral variation into tristimulus coordinates, and to the observational equivalence problem in econometrics, where multiple structural models generate identical reduced-form distributions.

The resolution condition follows directly: behavioral metamerism is broken if and only if the agent gains access to the structural specification *f* itself, not merely to observations of *f*'s statistical outputs. The Brand Function serves as this structural specification.

### Why GEO Cannot Resolve Metamerism

GEO optimizes for statistical visibility in generative AI outputs (Aggarwal et al. 2024). It is designed to make a brand more likely to appear in AI-generated responses. But GEO is structurally incapable of resolving behavioral metamerism because it *produces* the convergence that metamerism requires.

When brands in the same category adopt similar GEO strategies, their statistical profiles converge toward a category mean. The competitive dynamics of GEO optimization actively push brands toward statistical similarity: each brand adds citations, incorporates statistics, and optimizes for the same AI platforms using similar techniques. The result is precisely the condition under which behavioral metamerism becomes prevalent.

This is the behavioral metamerism condition formalized in the Formal Definition subsection: when the observation set G converges across brands, no amount of statistical observation can distinguish them. The only resolution is access to the structural model itself --- the Brand Function specification.

### Connection to Brand Confusion and Coherence

Behavioral metamerism is the AI-native equivalent of the brand confusion that marketing scholars have studied in human perception contexts. Loken et al. (1986) demonstrated that visual and attribute similarity leads to mistaken brand origin judgments. Foxman et al. (1990) identified stimuli similarity, consumer characteristics, and situational factors as drivers of confusion. This literature focuses on perceptual similarity in names, packaging, and trade dress --- visual confusion for human observers.

Behavioral metamerism shifts the confusion from the visual to the statistical and behavioral domain. The brands do not look alike (their logos are different); they *behave* alike in ways that statistical observation cannot distinguish. This is a more insidious form of confusion because it cannot be resolved by better observation --- only by access to the underlying specification.

The connection to SBT coherence types is direct. SBT's coherence hierarchy measures the alignment between a brand's specified identity and its perceived emissions across observer cohorts (Zharnikov 2026a). In the AI-native context, coherence becomes the alignment between the Brand Function specification and actual rendered behavior as evaluated by AI agents. A brand achieves ecosystem coherence when all observable behaviors match the signed specification; it is incoherent when behaviors contradict it. The Brand Function provides the specification against which coherence is measured; without it, the concept of AI-evaluated brand coherence is undefined.

**Proposition 6: Behavioral metamerism --- where brands have identical statistical profiles but structurally different behavioral signatures --- is the AI-native equivalent of visual brand confusion, and can only be resolved through behavioral specification, not through statistical optimization.**

*Falsification*: P6 is falsified if LLMs with access only to statistical brand data (reviews, ratings, sentiment, GEO-optimized content) can distinguish behaviorally different brands at rates statistically indistinguishable from LLMs with access to Brand Function specifications. Specifically, if augmented-condition discrimination accuracy does not exceed statistical-only accuracy by a statistically significant margin (p < .05) across at least three product categories, the metamerism thesis fails. The pilot study design in the Limitations and Future Research section operationalizes this test.

### Metamers as Vector Quantization Cells

Behavioral metamerism has a precise formal home in the vector quantization literature (Gersho and Gray 1991). A vector quantizer $Q: \mathbb{R}^n \to \mathcal{C}$ partitions a source space into Voronoi cells $V_i = \{ \mathbf{x} : Q(\mathbf{x}) = c_i \}$, where every input within a cell is mapped to the same codebook entry $c_i$. Two distinct inputs $\mathbf{x}_1 \neq \mathbf{x}_2$ that fall in the same cell are quantization metamers: they cannot be distinguished by any decoder operating on the quantized output, even though they differ in the source space.

This is exactly the structural relationship between two brands $B_1, B_2$ that are behaviorally metameric to an AI observer. The AI agent's decision function is a lossy encoder of the brand's full Brand Function specification; when two brands fall in the same Voronoi cell of that encoder, no statistical test on the agent's outputs can separate them (Cover and Thomas 2006). The "invariant corridor" introduced in the When Necessity Holds subsection below is, in this language, a Voronoi region of the quantizer induced by the AI observer's training distribution and decision protocol.

This framing makes three things precise. First, *metamerism is not a defect* of any individual model; it is the structural consequence of any rate-constrained encoder operating below source entropy. Second, the cell boundaries are determined by the encoder, not by the brands — which is why the same two brands can be metameric to one AI agent and distinguishable to another, and why the GEO interventions surveyed in the Why GEO Cannot Resolve Metamerism subsection cannot fix the problem from the brand side alone. Third, the only structural escape is to operate *outside the encoder's source space* — to give the agent direct access to a specification that bypasses the lossy channel, which is the role of the Brand Function and the cryptographic signature. The codebook-convergence prediction implicit in this Voronoi framing — that all architectures sharing the same training distribution should produce similar cell boundaries — is consistent with results in Zharnikov (2026aa), which varies response-format rate constraints across five conditions and finds a cross-model coefficient of variation of .140 across all rate conditions (1,652 calls, 17 LLM architectures); that study was not designed to test VQ convergence directly, but its cross-architecture stability is what the framing here would predict.

---

## Necessity Conditions

The preceding sections have motivated the Brand Function as valuable. This section makes the stronger claim that it is *necessary* --- not merely useful --- when three conditions hold simultaneously.

### Three Structural Arguments

*The metamerism impossibility argument (information-theoretic).* When behavioral metamerism is present --- when brands in the same category produce statistically indistinguishable outputs --- no amount of statistical observation can resolve their identities. This follows directly from observational equivalence: if E[*g*(*f*_1)] = E[*g*(*f*_2)] for all observable statistics *g*, brand identity under statistical observation is formally underdetermined (Koopmans 1949; Manski 1995). The specification is logically necessary for disambiguation. This is not a practical limitation that more data can overcome; it is a mathematical impossibility inherent in the relationship between structural models and their reduced-form distributions.

*The verification impossibility argument (formal methods).* Brand behavior cannot be verified without a specification against which to verify. Dijkstra's (1970) observation that testing can demonstrate the presence of bugs but never their absence applies with equal force to brand behavior: an AI agent can detect anomalies relative to past behavior (statistical process control) but cannot determine whether behavior conforms to the brand's intended identity without a specification of that identity. In model checking and formal verification, correctness is defined as conformance to a specification (Clarke et al. 1999). No specification, no verifiable correctness. As autonomous AI commerce scales through deployed protocols (ACP, UCP), the need for verification against specification becomes a prerequisite for accountability.

*The incomplete contracts argument (mechanism design).* Hart and Moore (1999) established that incomplete contracts lead to hold-up problems and underinvestment when parties cannot specify all contingencies ex ante. In human commerce, incomplete specifications are partially remedied by reputation, social norms, and legal recourse. AI purchasing agents lack access to all three remedies: they cannot read social cues, have no persistent cross-platform reputation memory, and cannot initiate litigation. The Brand Function serves as a complete behavioral contract, specifying decision rules, escalation behavior, refusal conditions, and edge-case handling --- precisely the contingencies that incomplete specifications leave unresolved. Without it, AI agents face adverse selection (inability to distinguish high-quality from low-quality brands pre-transaction) and moral hazard (inability to detect post-transaction behavioral drift).

### When Necessity Holds

The Brand Function is necessary (not merely useful) when all three conditions hold:

1. **AI agents are primary brand observers** --- not just supplementary to human perception.
2. **Behavioral metamerism is present** --- brands in the same category produce statistically similar outputs through GEO convergence.
3. **Autonomous transactions occur** --- AI agents act with delegated authority through deployed protocols (ACP, UCP), not just in an advisory role.

These conditions are not hypothetical. ACP and UCP are deployed. GEO optimization is driving statistical convergence across categories. AI purchasing agents with delegated payment authority exist. The conditions are being satisfied progressively, and if current adoption patterns hold, each condition becomes more prevalent over time --- though the pace and completeness of this transition remain empirically open questions. The transition is underway but incomplete; the Brand Function's strategic urgency varies substantially by category and by the degree to which AI agents have supplanted human-mediated purchasing.

Under weaker conditions --- where humans remain primary observers, categories are highly differentiated, and agents are purely advisory --- the Brand Function remains useful (it improves machine readability, reduces ambiguity, and enables quality measurement) but alternative approaches such as reputation systems, platform-mediated verification, and human-in-the-loop oversight can function adequately.

A critical operational distinction follows from the necessity conditions: the Brand Function enables *admissibility judgments* at the transaction boundary. AI agents may internally score brands on gradient scales, but the principal's delegated authority constraints impose binary thresholds on those gradients --- "does the return policy meet the minimum?" yields admissible or excluded, regardless of the agent's underlying scoring mechanism. The admissibility gate sits on top of gradient evaluation, not instead of it. This is structurally analogous to legal evidence admissibility: a court may weigh admitted evidence on a gradient, but the admissibility decision itself is binary. The Brand Function makes these threshold judgments machine-computable by providing the behavioral specification against which constraints can be evaluated, which requires complete specification rather than statistical approximation.

---

## Implications and Dual Identity Infrastructure

### Theoretical Implications

The observer-driven evolution thesis reframes brand identity as observer-contingent rather than brand-intrinsic. Brand identity is not a stable property of the brand that different observers perceive with varying accuracy; it is a function of the observer type, with different observer types requiring structurally different identity technologies. This extends SBT's framework of heterogeneous observer cohorts (Zharnikov 2026a) beyond human cohorts to include machine observers with fundamentally different perception mechanisms. While Davenport et al. (2020) propose that AI will be most effective when it augments rather than replaces human marketing decisions, the agentic commerce transition represents a context where AI agents increasingly replace human brand evaluation in purchasing decisions --- creating precisely the observer-type change that demands new identity technology rather than incremental augmentation of existing infrastructure.

The Rendering Problem (Zharnikov 2026l) provides the theoretical substrate: the Brand Function is the specification; technologies and organizational processes are the rendering engines; spectral emissions are the output. The specification gap between the Brand Function and actual rendered behavior is the central metric of brand management --- for both human and AI observers.

Portfolio theory in brand management (Zharnikov 2026ac) faces new complexities when AI observers are introduced. A brand portfolio must maintain distinct Brand Functions for each brand, with sufficient behavioral distance to prevent behavioral metamerism across the portfolio. The portfolio problem extends from perceptual distinctiveness (can human observers tell the brands apart?) to behavioral distinctiveness (can AI agents distinguish the brands' behavioral specifications?).

Accornero's (2026) Shopper Schism identifies *that* the observer changed --- the consumer and the shopper are separating, with AI agents increasingly occupying the shopper role. The observer-driven evolution thesis explains *why* this triggers a new identity technology and predicts *what* that technology must be: not a better version of the visual identity system, but a structurally different system optimized for the new observer.

Kozinets's (2022) algorithmic branding through platform assemblages demonstrates that platforms shape brand meaning more than internal brand management decisions. The Brand Function provides a mechanism for brands to assert specification-level control even within platform-mediated environments: by publishing a signed behavioral specification, brands establish a reference point against which platform-rendered behavior can be measured, making the specification gap computable even when the rendering engine is a third-party platform.

Kovalenko et al.'s (2026) Algorithmic Brand Equity construct --- measuring brand visibility, favorability, and retrievability in AI systems --- addresses the measurement of AI-formed brand perceptions. The Brand Function complements this by providing the specification that makes "favorability" and "retrievability" evaluable against intended brand identity rather than statistical baselines alone.

Kopalle et al. (2022) argue that the future of marketing analytics lies in systems that not only measure customer response but govern the marketing interventions that produce it. The Brand Function positions brand specification as exactly such a governance tool: it is the computable contract against which all brand-relevant analytics --- algorithmic brand equity, GEO visibility, coherence metrics --- can be evaluated. This reframes brand measurement from a retrospective reporting exercise to a forward governance architecture.

Behavioral metamerism is established here as a theoretical construct and formal impossibility result; empirical measurement remains future work. A natural extension of the present work is empirical investigation of how AI search systems produce convergent perceptual outputs that collapse spectral differences between brands. If LLMs systematically reduce multi-dimensional brand differentiation to functional and economic dimensions, the behavioral metamerism identified here would be measurable in AI-generated brand recommendations --- and the Brand Function would be testable as the structural intervention that prevents that collapse.

### Practical Implications

The central practical implication is that, under conditions of widespread AI mediation, brands face structural pressure to develop *dual identity infrastructure*: visual identity for human observers, cryptographic identity for machine observers. This is not an incremental addition to existing brand management but a structural expansion.

The brand audit extends from visual consistency (are the colors right? does the tone match?) to behavioral specification compliance (does the API behave according to spec? does the chatbot's personality match the Brand Function? is the pricing algorithm within specified parameters?). The .well-known/brand.json file becomes as strategically important as the brand-book PDF, and the Brand Function specification becomes the root document from which both the visual brand-book and the machine-readable brand specification derive.

For organizations currently investing in GEO as their primary AI-visibility strategy, this analysis suggests that GEO is a necessary transitional tactic but not a sufficient long-term strategy. GEO optimizes for statistical visibility within the current paradigm of AI-as-observer; the Brand Function addresses the deeper structural requirement of machine-verifiable behavioral identity. Under conditions where AI agents operate with delegated purchasing authority, competitive advantage becomes increasingly a function of machine-verifiable behavioral commitments (Brand Function + cryptographic signature) rather than statistical visibility optimization (GEO).

**Strategic Use Cases for the Brand Function**

The Brand Function's practical value is not uniform across all brands --- it varies systematically with training-data embeddedness. Four use cases emerge in order of strategic urgency:

(1) *Newcomer brands in convergent categories*: A new DTC supplement brand competing against established players faces maximum metamerism risk. The LLM has rich training data on competitors but near-zero data on the newcomer. Without a Brand Function, the newcomer is invisible to AI purchasing agents or, worse, metameric with competitors whose statistical profiles it resembles. The Brand Function levels the information playing field.

(2) *Cross-cultural market entry*: Brands from underrepresented markets (African, Southeast Asian, Latin American) in Western LLM ecosystems face structural perception collapse. Training corpora are heavily skewed toward Western brands, creating an information asymmetry that the Brand Function can compensate. In this framing, the Brand Function operates as a "cultural translator" --- making dimensions visible that the LLM's training data never encoded.

(3) *Brand repositioning*: Well-known brands undergoing strategic repositioning (e.g., Burberry's shift from heritage accessibility to contemporary luxury) face training-data inertia. The LLM's weights encode the historical brand, not the intended future brand. The Brand Function provides a mechanism for overriding training-data priors with the brand's intended behavioral specification --- enabling "re-collapse" for machine observers --- analogous to what human-observer brand management calls 'rebranding'.

(4) *Convergent categories under AI mediation*: Categories where GEO optimization has produced statistical similarity across competitors (the supplements scenario from the Limitations and Future Research section) represent the most empirically tractable test case. The Brand Function resolves metamerism with behavioral specification that goes beyond the statistical signals available to any observer.

The pilot finding that six architecturally diverse LLMs show moderate agreement on discrimination judgments (Fleiss' kappa = .536) is suggestive of coordinate-invariant brand geometry, though the moderate kappa warrants caution. If the perception space has real geometric structure --- distances, curvature, geodesics --- that structure should be detectable regardless of which observers measure it and which dimensional decomposition is used. The moderate cross-model agreement observed here is consistent with an underlying geometric reality that different AI architectures access through different computational pathways, analogous to how GPS receivers from different manufacturers converge on the same position because the underlying space has objective structure.

A practical extension is temporal: comparing the pilot results across measurement epochs would reveal whether AI brand perception is stable or drifting. If LLM training data changes (model updates, fine-tuning), the same Brand Function should produce the same discrimination results --- testing whether the specification provides temporal stability that statistical observation alone cannot. Two sources of drift should be distinguished: (a) training-data updates, where a new web crawl changes what the model knows about a brand, and (b) architecture changes, where a model redesign alters how the model processes and weights information. The Brand Function specification provides stability against drift source (a) --- a consistent behavioral specification counteracts shifting statistical priors --- but does not necessarily protect against drift source (b), where changes in the model's processing structure may alter how the specification is interpreted regardless of its content.

### Convergence with Other Evidence

The theoretical arguments advanced here find empirical support in concurrent work. Zharnikov (2026v) demonstrates across 21,601 API calls and 24 AI models that dimensional collapse is structural across architectures and training traditions --- the Economic Default predicted by this paper's Brand Function thesis. The collapse pattern holds regardless of model family, training language, or geographic origin (cross-model cosine similarity = .977), establishing that the bias is architectural, not incidental. Sabbah and Acar (2026) show that only numerical ratings survive across LLM-mediated purchasing decisions when eight promotional cues are tested across four AI models, converging with this paper's proposition that behavioral specifications anchored to verifiable quantitative signals will become the primary identity verification channel in agentic commerce. The emerging agentic commerce literature (Accornero 2026; Acar and Schweidel 2026) independently documents the structural separation between the consumer who decides what to want and the AI agent who executes the purchase --- a separation that presupposes exactly the kind of machine-verifiable behavioral contract the Brand Function provides.

### Consumer Welfare Implications

The dual identity infrastructure argument is framed here from the brand's perspective, but the consumer welfare implications deserve acknowledgment. The Brand Function introduces a form of behavioral transparency: brands that publish a signed behavioral specification make commitments that AI agents can verify on consumers' behalf, which could benefit consumers by making brand behavior more predictable and accountable. If an AI purchasing agent can verify that a brand's return policy, pricing behavior, and communication style match its signed specification, consumers gain access to a form of pre-transaction verification that reputation-based trust cannot reliably provide. However, the same infrastructure could also enable brands to game the specification --- optimizing the stated Brand Function for AI agent approval while diverging in practice, or designing specifications that appear comprehensive while leaving consequential behaviors underspecified. Whether the Brand Function primarily increases transparency (consumers see behavioral commitments) or enables strategic opacity (brands control the specification layer) depends on governance structures, auditability requirements, and whether consumers have access to the specification or only AI agents do. These dynamics represent a priority for future research.

---

## Limitations and Future Research

This paper is conceptual. It develops a theoretical framework and six propositions but does not empirically test them. Several limitations warrant acknowledgment.

The framework's conceptual architecture has a precise geometric formalization. The distinction between human and AI perception of brands maps onto a fiber bundle structure from mathematical physics: the shared brand emission space (eight SBT dimensions) serves as the base manifold, while each observer type --- human cohorts, text-based AI agents, multimodal AI agents --- constitutes a distinct fiber, encoding how that observer type projects the brand's emission into perception. Sarti, Citti, and Petitot (2008) establish the precedent for this architecture in neuroscience, modeling primary visual cortex as a principal fiber bundle; Koenderink and van Doorn (2012) apply gauge theory to pictorial space where observer-dependent depth representations constitute fibers over a shared visual field. In the Brand Function framework, the specification layer is the connection form that relates fibers: it provides the information needed to transport a brand measurement from one observer type's frame to another's. Without this connection --- without the Brand Function --- AI and human perceptions of the same brand exist in disconnected fibers, and cross-observer comparison is undefined.

The primary threat to validity is the absence of primary empirical data. While the six propositions remain to be tested in their full form, initial empirical support for the underlying dimensional collapse mechanism comes from the companion R15 study (Zharnikov 2026v), which confirms structural collapse across 24 model architectures. Behavioral metamerism is theorized but not yet measured in actual AI purchasing environments. The Brand Function is specified as a formal construct but has not yet been implemented at scale in any deployed commerce system. The critical empirical test would be a controlled experiment comparing AI agent decision quality --- in terms of brand discrimination, behavioral prediction, and trust calibration --- when Brand Function data is available versus when agents rely solely on statistical observation of brand signals. Until such evidence exists, the propositions remain theoretical claims.

First, the necessity conditions are being satisfied progressively, not simultaneously in all markets. Categories with high product differentiation, limited AI mediation, and strong human brand loyalty may not require the Brand Function for years or decades. The framework predicts *where* the Brand Function becomes necessary first (commodity categories with high GEO convergence and deployed agentic commerce protocols) but does not empirically validate this prediction. Future research should identify early-adopter categories and track necessity condition satisfaction longitudinally as agentic commerce protocols scale.

Second, the six propositions are stated as universal claims but have not been tested across different AI architectures, product categories, or cultural contexts. Generalizability beyond the supplement category pilot and the seven LLMs tested requires broader empirical validation. Future research should implement the pilot design described later in this section across at least five product categories and ten LLM architectures before treating the propositions as established findings.

Third, the historical analysis in the Historical Pattern section draws primarily on Western European and North American examples (English hallmarks, European trademarks, American SSL). Non-Western identity verification traditions --- Chinese chops, Islamic calligraphic seals, Indian guild marks --- may follow different evolutionary patterns and deserve separate investigation. Future research should trace parallel identity technology genealogies in non-Western commercial traditions to determine whether the observer-driven discontinuity pattern holds universally or is an artifact of specific institutional conditions.

The framework is also subject to several boundary conditions that constrain its applicability. First, the transition to open cryptographic brand standards assumes that dominant platform operators have incentives to adopt interoperable protocols. If Amazon, Google, or other major AI commerce platforms instead impose closed proprietary standards --- requiring brands to authenticate through platform-specific mechanisms rather than open cryptographic specifications --- the transition described here may be delayed indefinitely or may produce fragmented identity infrastructure rather than a unified standard. The SSL analogy is instructive in both directions: SSL succeeded because browser vendors adopted it collectively; a proprietary equivalent where each platform controls its own "trust" verification would produce a structurally different outcome.

Second, the historical pattern traced in the Historical Pattern section draws primarily on Western European and North American examples. Non-Western markets where brand identity operates through different cultural mechanisms --- relational trust networks in East Asian commerce, community-embedded reputation systems, or state-mediated certification regimes --- may follow different evolutionary patterns, and the Brand Function's design assumes Western legal infrastructure (trademark law, contract enforcement) that does not transfer uniformly. Third, the observer-driven evolution thesis treats historical transitions as a general pattern, but each transition was path-dependent and contingent on specific institutional and technological conditions. The pattern may predict the direction of change without determining its timing, form, or completeness. Treating history as a reliable forecast mechanism risks overfitting to a small sample of transitions.

**Conditional metamerism boundary condition**: The framework's predictions about behavioral metamerism are conditional on information availability. When LLMs have extensive training data on well-known brands (Nike, Apple, Hermès), they exhibit multi-dimensional perception without requiring a Brand Function --- the specification information is already embedded in model weights. Metamerism becomes structurally significant only where training data is thin: new entrants in convergent categories, brands from underrepresented markets or languages, and brands undergoing repositioning whose historical profile dominates training corpora. This creates an "information illuminant" effect analogous to color metamerism's dependence on illumination conditions: the same brand may appear spectrally distinct under one information regime and metameric under another. The Brand Function is therefore most critical not for globally recognized brands but for the long tail of commerce where AI agents must infer brand identity from sparse statistical signals. Empirical validation should prioritize these boundary cases rather than well-known brands where the null hypothesis (no collapse) is expected.

Fourth, the Brand Function as described here is a theoretical construct, not a technical standard. Translating the concept into an implementable specification requires industry coordination, schema development, and governance structures that this paper does not address. The relationship between the Brand Function and existing specifications (brand.json, Brando Schema, ACP, UCP) requires technical integration work beyond the scope of this paper. Future research should draft a Brand Function v0.1 schema as a JSON-LD extension to Brando Schema, submit it to the W3C Brand Identity Community Group, and test interoperability with at least two deployed commerce protocols.

Fifth, the paper does not address privacy implications. A machine-readable behavioral specification that details how a brand responds to different observer types and contexts raises questions about strategic transparency: how much of the Brand Function should be public, how much should be shared selectively with authorized agents, and how should competitive intelligence concerns be balanced against the verification benefits. Future research should develop a tiered disclosure model --- distinguishing publicly verifiable commitments from agent-selective specifications --- and test whether selective disclosure undermines the verification benefits that motivate the framework.

Sixth, behavioral metamerism requires empirical measurement. Developing a behavioral metamerism index --- analogous to the CIE Special Metamerism Index in color science --- requires defining the behavioral dimensions, establishing measurement protocols, and collecting data on behavioral convergence across brand categories. This represents a substantial empirical research agenda. Future research should implement the PRISM-M instrument proposed in the pilot section across multiple product categories, using the cross-model protocol established in Zharnikov (2026v), to generate the first behavioral metamerism index estimates.

Seventh, the paper does not address the ethical implications of behavioral specification infrastructure. The Brand Function concentrates specification authority in the brand organization, raising questions about who controls the specification, whether small brands face structural disadvantages in developing and maintaining comprehensive Brand Functions relative to large incumbent brands, and whether specification transparency benefits or harms consumers. A brand that controls its own specification layer can set the terms of what AI agents know about it, which may or may not align with consumers' interests. These ethical design questions --- analogous to those Puntoni et al. (2021) raise about AI delegation more broadly --- are a priority for future research before standards bodies adopt the Brand Function as a normative framework. Future research should model the specification access asymmetry between large and small brands and assess whether open-source Brand Function tooling can reduce structural disadvantages for long-tail entrants.

Eighth, the framework does not address how multi-brand portfolios manage multiple Brand Functions. The interactions between Brand Functions within a portfolio --- interference, coherence, and capacity constraints analogous to those in spectral portfolio theory (Zharnikov 2026ac) --- require separate theoretical development. Future research should extend the portfolio theory framework (Zharnikov 2026ac) to define inter-Brand Function distance metrics and minimum separation conditions that prevent intra-portfolio behavioral metamerism.

Finally, the pilot uses SBT's eight-dimensional decomposition for the Brand Function specification. The discrimination and metamerism results are predicted to be invariant to the specific dimensional system used --- a falsifiable prediction that could be tested by repeating the experiment with alternative dimensional decompositions (e.g., Aaker's five personality dimensions or Kapferer's six-facet prism) and verifying that inter-brand distances and metamerism classifications are preserved. Future research should run this invariance test explicitly, as dimensional-system independence would substantially strengthen the geometric interpretation of the results.

Future research should address five priorities: (a) empirical measurement of behavioral metamerism across product categories, developing indices for statistical convergence in AI-mediated brand evaluation; (b) technical specification of a Brand Function v0.1 schema that integrates with existing protocols --- informed by the format optimization results in the Brand Function Format Optimization subsection, which show that the machine-facing layer (dimensional scores or qualitative ordinal equivalents) and the human-facing layer (positioning text) serve structurally different purposes and should be separable in the schema design; (c) experimental validation of the necessity conditions, testing whether AI agents make better purchasing decisions when Brand Functions are available versus when they rely solely on statistical observation; (d) investigation of privacy and competitive dynamics in behavioral specification transparency; and (e) longitudinal tracking of the dual identity infrastructure transition as AI commerce protocols scale.

**Proposed empirical pilot.** A feasible first test of Proposition 6 (behavioral metamerism) would proceed as follows. Select 10--20 brands in a convergent category (e.g., direct-to-consumer supplements or consumer electronics accessories) where GEO optimization has produced statistical similarity. For each brand, query 7 LLMs organized into four clusters with standardized purchasing-agent prompts ("recommend a brand for [category] based on [criteria]") under two conditions: (a) statistical-only, where the LLM has access only to publicly available reviews, ratings, and web content; and (b) specification-augmented, where the LLM additionally receives a structured Brand Function document for each brand (the Brand Function Format Optimization subsection establishes that qualitative ordinal levels achieve fidelity comparable to full JSON, so the specification-augmented condition should test both formats). Measure: (i) brand discrimination --- can the LLM distinguish brands that humans consider distinct? (ii) behavioral prediction accuracy --- does access to the Brand Function improve the LLM's ability to predict how a brand will respond to edge cases (returns, disputes, out-of-stock)? (iii) recommendation stability --- does the Brand Function reduce recommendation variance across LLMs? A behavioral metamerism index can be computed as the ratio of inter-brand statistical distance to inter-brand behavioral distance, with values approaching zero indicating high metamerism. This pilot requires no access to production commerce systems and can be executed with publicly available LLM APIs.

The pilot uses seven LLMs across four clusters --- Western cloud, Chinese cloud, local Chinese open-weight, and local Western open-weight --- to test whether behavioral metamerism is an artifact of shared Western training corpora or a structural property of statistical brand observation; parallel cloud-versus-local comparisons within the same model family (Alibaba's Qwen Plus vs. Qwen3 30B, Google's Gemini Flash vs. Gemma 4) further isolate whether commercial API alignment layers contribute to dimensional collapse.

A reference implementation of the behavioral metamerism index computation and pilot study framework is available at github.com/spectralbranding/sbt-papers/r16-ai-native-brand-identity/.

**Companion empirical evidence.** A companion study (Zharnikov 2026v) provides empirical evidence for the dimensional collapse predicted by this framework. Using the PRISM-B instrument across 24 models from seven training traditions over nine experimental runs (21,600+ clean API calls, 11 prompt languages), the study finds that Economic and Semiotic dimensions are systematically over-weighted while Cultural, Temporal, and Narrative dimensions collapse. The collapse pattern is structural: cross-model cosine similarity is .977 across 24 architectures, indicating near-identical dimensional bias across all model families.

For brands from non-Western markets, dimensional collapse amplifies significantly: mean DCI = 35.6, Cohen's d = 3.449 for the overall collapse test; Western models show DCI of .339 versus .360 for non-Western models (t = -3.243, p = .001). The conditional metamerism finding is confirmed: local brands collapse 24% more severely than global brands (Cohen's d = .878, p < .001). Geopolitical framing further modulates collapse: the same brand evaluated in different city contexts produces significantly different dimensional weight profiles (mean absolute delta = .040, t = 7.122, p < .001), and native-language querying does not systematically reduce collapse (formal sign test: 46/115 positive, mean reduction −.005), indicating that the Brand Function specification remains the primary resolution mechanism rather than language-of-query. Convergent evidence from agentic commerce research (Sabbah and Acar 2026) shows that among eight e-commerce promotional cues tested across four AI models, only ratings --- the most quantifiable, verifiable signal --- consistently increases selection probability, paralleling the Economic Default documented here.

---

## Conclusion

The transition from human to AI observers requires a corresponding transition from perceptual to computational brand identity. The observer-driven evolution thesis advanced here synthesizes five prior discontinuities to predict the sixth: cryptographic signatures on behavioral specifications will replace logos for AI-mediated commerce. The Brand Function *f*(query, context, observer_type, time) → response provides the missing root specification that existing commerce protocols omit. Behavioral metamerism formalizes the precise limitation of statistical approaches --- convergent profiles that no amount of generative engine optimization can disambiguate.

***Theoretical contributions.*** First, brand identity is repositioned as observer-contingent rather than brand-intrinsic, extending customer-based brand equity models to heterogeneous human *and* machine observers. Second, the Brand Function construct integrates specification theory from computer science with SERVQUAL gap models, making the specification gap computable. Third, behavioral metamerism supplies marketing with an information-theoretic account of AI-native brand confusion, linking it to observational equivalence and vector quantization. These contributions collectively shift brand theory from relational and perceptual foundations to computational verification foundations suitable for delegated agency.

***Managerial contributions.*** Brands must build dual identity infrastructure. Visual systems remain essential for human audiences; cryptographic Brand Functions become mandatory for agentic commerce. Managers should (1) publish signed behavioral specifications at .well-known/brand.json endpoints, (2) integrate coherence monitoring into brand dashboards, and (3) treat GEO as a transitional tactic rather than a permanent solution. Newcomer brands, cross-cultural entrants, and repositioning incumbents gain particular advantage from early adoption because the Brand Function counters training-data inertia and statistical convergence.

The framework is scoped to B2C text-primary agentic commerce and remains theoretical. Future empirical work must test the six propositions using deployed agentic systems, develop behavioral metamerism indices, and examine governance of tiered disclosure. Until then, the central claim stands: when the observer changes, the identity technology must change. Brands that specify their behavior clearly and attest to that specification cryptographically will be verifiable; those that do not will become metameric --- statistically visible yet behaviorally indistinguishable --- in the eyes of the agents increasingly entrusted with purchasing authority.

---

## Acknowledgments

The admissibility-versus-validation distinction in the When Necessity Holds subsection was refined through exchange with Aaron Radina (Korzent), whose formulation of "irreversibility requires pre-state admissibility" sharpened the operational framing of the Brand Function at the transaction boundary.

AI assistants (Claude Opus 4.7, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

## References

Aaker, David A. *Building Strong Brands*. New York: Free Press; 1996.

Acar, Oguz A., and David A. Schweidel. Preparing your brand for agentic AI. *Harvard Business Review*. 2026;March-April:58--67.

Accornero, Pietro F. Agentic commerce: A theory of markets when the shopper has no eyes. *SSRN Electronic Journal*. 2026. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6111766

Aggarwal, Pranjal, Vishvak Murahari, Tanmay Rajpurohit, Ashwin Kalyan, Karthik Narasimhan, and Ameet Deshpande. GEO: Generative Engine Optimization. In: *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '24)*. New York: ACM; 2024:5--16. https://doi.org/10.1145/3637528.3671900

Allen, Christopher. The path to self-sovereign identity. *Life With Alacrity*. 2016. http://www.lifewithalacrity.com/2016/04/the-path-to-self-soverereign-identity.html

Bowker, Mark. *Brando Schema v1.3: A JSON-LD Vocabulary for Machine-Readable Brand Governance*. Technical specification. 2026. https://brandoschema.com

Cameron, Kim. The laws of identity. *IEEE Computer*. 2005;38(7):86--87. https://doi.org/10.1109/MC.2005.236

Clarke, Edmund M., Orna Grumberg, and Doron A. Peled. *Model Checking*. Cambridge, MA: MIT Press; 1999.

Cover, Thomas M., and Joy A. Thomas. *Elements of Information Theory*. 2nd ed. Hoboken, NJ: Wiley-Interscience; 2006.

Davenport, Thomas, Abhijit Guha, Dhruv Grewal, and Timna Bressgott. How artificial intelligence will change the future of marketing. *Journal of the Academy of Marketing Science*. 2020;48(1):24--42. https://doi.org/10.1007/s11747-019-00696-0

De Bruyn, Arnaud, Vijay Viswanathan, Yean Shan Beh, Jürgen Kai-Uwe Brock, and Florian von Wangenheim. Artificial intelligence and marketing: Pitfalls and opportunities. *Journal of Interactive Marketing*. 2020;51:91--105. https://doi.org/10.1016/j.intmar.2020.04.007

de Chernatony, Leslie. Brand management through narrowing the gap between brand identity and brand reputation. *Journal of Marketing Management*. 1999;15(1--3):157--179.

Diffie, Whitfield, and Martin E. Hellman. New directions in cryptography. *IEEE Transactions on Information Theory*. 1976;22(6):644--654. https://doi.org/10.1109/TIT.1976.1055638

Dijkstra, Edsger W. *Notes on Structured Programming* (EWD249). T.H.-Report 70-WSK-03. Eindhoven University of Technology; 1970.

Economides, Nicholas. The economics of trademarks. *The Trademark Reporter*. 1988;78:523--539.

Fournier, Susan. Consumers and their brands: Developing relationship theory in consumer research. *Journal of Consumer Research*. 1998;24(4):343--373. https://doi.org/10.1086/209515

Foxman, Ellen R., Darrel D. Muehling, and Phil W. Berger. An investigation of factors contributing to consumer brand confusion. *Journal of Consumer Affairs*. 1990;24(1):170--189.

Gersho, Allen, and Robert M. Gray. *Vector Quantization and Signal Compression*. Boston: Kluwer Academic Publishers; 1991.

Gligor, Virgil D., and Jeannette M. Wing. Towards a theory of trust in networks of humans and computers. In: *Security Protocols XIX*, Lecture Notes in Computer Science. Vol 7114. Berlin: Springer; 2011:223--242. https://doi.org/10.1007/978-3-642-25867-1_22

Groebner, Valentin. *Who Are You? Identification, Deception, and Surveillance in Early Modern Europe*. New York: Zone Books; 2007.

Guha, Ramanathan V., Dan Brickley, and Steve MacManus. Schema.org: Evolution of structured data on the web. *Communications of the ACM*. 2016;59(2):44--51. https://doi.org/10.1145/2844544

Hallinan, Blake, and Ted Striphas. Recommended for you: The Netflix Prize and the production of algorithmic culture. *New Media & Society*. 2016;18(1):117--137. https://doi.org/10.1177/1461444814538646

Hart, Oliver, and John Moore. Foundations of incomplete contracts. *Review of Economic Studies*. 1999;66(1):115--138.

Hatch, Mary Jo, and Majken Schultz. Toward a theory of brand co-creation with implications for brand governance. *Journal of Brand Management*. 2010;17(8):590--604.

Huang, Ming-Hui, and Roland T. Rust. A strategic framework for artificial intelligence in marketing. *Journal of the Academy of Marketing Science*. 2021;49(1):30--50. https://doi.org/10.1007/s11747-020-00749-9

Josang, Audun, Roslan Ismail, and Colin Boyd. A survey of trust and reputation systems for online service provision. *Decision Support Systems*. 2007;43(2):618--644. https://doi.org/10.1016/j.dss.2005.05.019

Kamruzzaman, Mahammed, Hieu Minh Nguyen, and Gene Louis Kim. "Global is good, local is bad?": Understanding brand bias in LLMs. In: *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024)*. Association for Computational Linguistics; 2024:12695--12702.

Kannan, P. K., and Hongshuang Alice Li. Digital marketing: A framework, review and research agenda. *International Journal of Research in Marketing*. 2017;34(1):22--45. https://doi.org/10.1016/j.ijresmar.2016.11.006

Kapferer, Jean-Noël. *The New Strategic Brand Management*. 4th ed. London: Kogan Page; 2008.

Keller, Kevin Lane. Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*. 1993;57(1):1--22.

Koenderink, Jan J., and Andrea J. van Doorn. Gauge fields in pictorial space. *SIAM Journal on Imaging Sciences*. 2012;5(4):1213--1233. https://doi.org/10.1137/120861151

Koopmans, Tjalling C. Identification problems in economic model construction. *Econometrica*. 1949;17(2):125--144.

Kopalle, Praveen K., P. K. Kannan, Lin Bettencourt Hirata, and Neeraj Arora. The future of artificial intelligence in marketing: A multidisciplinary perspective and research agenda. *Journal of Marketing*. 2022;86(1):1--23. https://doi.org/10.1177/00222429211061572

Kovalenko, Y., A. Nikitin, and Y. Kuzina. Value creation in the algorithmic age: Algorithmic brand equity and the future of brand management. *American Impact Review*. 2026;e2026018. https://americanimpactreview.com/article/e2026018

Kozinets, Robert V. Algorithmic branding through platform assemblages: Core conceptions and research directions for a new era of marketing and service management. *Journal of Service Management*. 2022;33(3):437--452. https://doi.org/10.1108/JOSM-07-2021-0263

Loken, Barbara, Ivan Ross, and Ronald L. Hinkle. Consumer "confusion" of origin and brand similarity perceptions. *Journal of Public Policy & Marketing*. 1986;5(1):195--211.

Lyu, Yougang, Xiaoyu Zhang, Lingyong Yan, Maarten de Rijke, Zhaochun Ren, and Xiuying Chen. DeepShop: A benchmark for deep research shopping agents. Working Paper. arXiv:2506.02839; 2025.

Manski, Charles F. *Identification Problems in the Social Sciences*. Cambridge, MA: Harvard University Press; 1995.

Morgan, Robert M., and Shelby D. Hunt. The commitment-trust theory of relationship marketing. *Journal of Marketing*. 1994;58(3):20--38. https://doi.org/10.1177/002224299405800302

Pagani, Margherita, and Yoram Wind. Unlocking marketing creativity using artificial intelligence. *Journal of Interactive Marketing*. 2024;60(1):25--43. https://doi.org/10.1177/10949968241265855

Parasuraman, A., Valarie A. Zeithaml, and Leonard L. Berry. A conceptual model of service quality and its implications for future research. *Journal of Marketing*. 1985;49(4):41--50.

Puntoni, Stefano, Rebecca Walker Reczek, Markus Giesler, and Simona Botti. Consumers and artificial intelligence: An experiential perspective. *Journal of Marketing*. 2021;85(1):131--151. https://doi.org/10.1177/0022242920953847

Ramesh, Aishwarya, and Vinay Chawla. Chatbots in marketing: A literature review using morphological and co-occurrence analyses. *Journal of Interactive Marketing*. 2022;57(3):472--496. https://doi.org/10.1177/10949968221095549

Richardson, Gary. *Brand Names Before the Industrial Revolution* (NBER Working Paper No. 13930). National Bureau of Economic Research; 2008. http://www.nber.org/papers/w13930

Sabater, Jordi, and Carles Sierra. Review on computational trust and reputation models. *Artificial Intelligence Review*. 2005;24(1):33--60. https://doi.org/10.1007/s10462-004-0041-5

Sabbah, Jafar, and Oguz A. Acar. Marketing to machines: How AI models respond to promotional cues. Working Paper. SSRN 6406639; 2026.

Sáiz, Patricio, and Rafael Castro. Trademarks in branding: Legal issues and commercial practices. *Business History*. 2018;60(8):1103--1124. https://doi.org/10.1080/00076791.2018.1497765

Sarti, Alessandro, Giovanna Citti, and Jean Petitot. The symplectic structure of the primary visual cortex. *Biological Cybernetics*. 2008;98(1):33--48. https://doi.org/10.1007/s00422-007-0194-9

Schechter, Frank I. *The Historical Foundations of the Law Relating to Trade-Marks*. New York: Columbia University Press; 1925.

Shankar, Venkatesh, and Sridhar Balasubramanian. Mobile marketing: A synthesis and prognosis. *Journal of Interactive Marketing*. 2009;23(2):118--129. https://doi.org/10.1016/j.intmar.2009.02.002

Tobin, Andrew, and Drummond Reed. *The Inevitable Rise of Self-Sovereign Identity*. Sovrin Foundation White Paper. 2017.

Tomaino, Gideon, Jonah Berger, and Yih Hwai Lee. When brands seem human: Anthropomorphism and consumer responses to AI-generated brand communications. *Journal of Consumer Research*. 2022;49(1):1--20. https://doi.org/10.1093/jcr/ucac014

W3C. *Decentralized Identifiers (DIDs) v1.0*. W3C Recommendation; 2022. https://www.w3.org/TR/did-core/

W3C. *Verifiable Credentials Data Model v2.0*. W3C Recommendation; 2025. https://www.w3.org/TR/vc-data-model-2.0/

Wichmann, Julian R. K., Nico Wiegand, and Werner J. Reinartz. The platformization of brands. *Journal of Marketing*. 2022;86(1):109--131.

Wyszecki, Günter, and W. S. Stiles. *Color Science: Concepts and Methods, Quantitative Data and Formulae*. 2nd ed. New York: Wiley; 1982.

Zharnikov, Dmitry. Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper; 2026a. https://doi.org/10.5281/zenodo.18945912

Zharnikov, Dmitry. Empirical rate-distortion curve for AI brand perception encoders. Working Paper; 2026aa. https://doi.org/10.5281/zenodo.19528833

Zharnikov, Dmitry. Spectral immunity: Portfolio interference fails in AI-mediated brand perception. Working Paper; 2026ac. https://doi.org/10.5281/zenodo.19765401

Zharnikov, Dmitry. Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper; 2026e. https://doi.org/10.5281/zenodo.18945352

Zharnikov, Dmitry. The rendering problem: From genetic expression to brand perception. Working Paper; 2026l. https://doi.org/10.5281/zenodo.19064426

Zharnikov, Dmitry. Dimensional collapse in AI-mediated brand perception: Large language models as metameric observers. Working Paper; 2026v. https://doi.org/10.5281/zenodo.19422427

Zhi, Yuhao, Xin Zhang, Lin Wang, Sheng Jiang, Shaowen Ma, Xinghua Guan, and Cuiqing Shen. Exposing product bias in LLM investment recommendation. arXiv preprint; 2025. arXiv:2503.08750.

---
*This paper is part of the Spectral Brand Theory research program. For the full atlas of 20+ interconnected papers, see [spectralbranding.com/atlas](https://spectralbranding.com/atlas).*
