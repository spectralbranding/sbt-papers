# AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification

**Dmitry Zharnikov**

*Working Paper — April 2026*

*Zenodo DOI: [10.5281/zenodo.19391476](https://doi.org/10.5281/zenodo.19391476)*

---

## Abstract

This paper advances two theoretical contributions to brand identity research. First, we propose the *observer-driven evolution thesis*: identity verification technologies change discontinuously not through incremental improvement but in response to shifts in the observer type. Wax seals served bureaucratic observers, hallmarks served asymmetric-information buyers, trademarks served mass-market consumers, and SSL certificates served web browsers. As AI agents increasingly mediate purchasing decisions, product recommendations, and brand evaluation, this pattern predicts a new identity technology --- not a better logo, but a structurally different system. Second, we introduce *behavioral metamerism* as a novel construct: the phenomenon where brands produce identical statistical profiles but exhibit structurally different behavioral patterns, creating a form of AI-native brand confusion that statistical optimization cannot resolve. We extend Spectral Brand Theory to define the Brand Function --- f(query, context, observer_type, time) -> response --- as the complete behavioral specification of how a brand operates when observed by machines, and argue that cryptographic signatures on behavioral specifications are positioned to serve as the primary brand identity mechanism for AI-mediated commerce under conditions of widespread agentic commerce adoption. Drawing on emerging standards (W3C Verifiable Credentials, GLEIF vLEI, .well-known/brand.json proposals) and empirical evidence on LLM brand bias, we propose six formal propositions connecting identity verification technology to observer type, behavioral specification to brand coherence, and cryptographic attestation to trust in autonomous commerce. We formalize behavioral metamerism as an observational equivalence condition and report a pre-registered pilot study (684 API calls, 6 LLMs, 4 architectural clusters) providing initial empirical support: three of six models showed zero discrimination for the high-metamerism brand pair under statistical-only observation, rising to 100% discrimination across all models when behavioral specifications were provided (Fisher's exact *p* = 0.0009, Cohen's *d* = 0.791). We conclude that logos will persist for human observers but face diminishing relevance for AI agents, and that under conditions of advanced AI mediation, organizations face pressure to develop dual identity infrastructure: visual for humans, cryptographic for machines. The complete experiment infrastructure --- pre-registration protocol, session logs, and analysis code --- is publicly available.

**Keywords**: brand identity, AI agents, cryptographic verification, behavioral specification, metamerism, agentic commerce, generative engine optimization, observational equivalence

---

## 1. Introduction

Every time the observer of brand identity changed, the verification technology changed with it. Wax seals authenticated documents for literate officials. Hallmarks guaranteed metal purity for buyers who could not assay it themselves. Trademarks enabled recognition in anonymous mass markets. SSL certificates proved server identity to web browsers. The logo --- the dominant identity technology of the 20th century --- was designed for a specific observer: the human consumer navigating scaled markets through visual and emotional pattern matching.

That observer is changing. AI purchasing agents --- Amazon Rufus, Google AI Mode, Perplexity Shopping, ChatGPT with agentic commerce capabilities --- are increasingly mediating product discovery, brand evaluation, and purchasing decisions. These systems do not process logos, emotional narratives, or visual brand guidelines. They process structured data, behavioral patterns, and verified claims. A growing body of evidence documents how large language models (LLMs) form "brand perceptions" that are statistical rather than perceptual: global brands are favored due to training data frequency (Kamruzzaman et al., 2024), market-dominant products receive disproportionate recommendation (Zhi et al., 2025), and optimization strategies designed for human search engines produce diminishing returns in generative AI environments (Aggarwal et al., 2024). Current brand identity infrastructure --- the visual brand book, the logo, the tagline --- is built entirely for human observers and carries zero informational weight for machine observers.

The dominant paradigm in brand identity theory --- Keller's (1993) customer-based brand equity model, which locates brand equity in the knowledge structures of human consumers --- is built entirely for human observers. Keller's four dimensions of brand knowledge (brand awareness, brand associations, perceived quality, and brand loyalty) presuppose a human mind forming associative networks through direct and mediated experience. This human-observer assumption pervades the subsequent identity literature: Hatch and Schultz (2010) model brand co-creation as stakeholder dialogue --- a process that requires observers capable of dialogue; de Chernatony (1999) frames brand identity as the gap between management vision and consumer perception --- a formulation that loses meaning when the "consumer" is a recommendation algorithm with no perception in the phenomenological sense. Hallinan and Striphas (2017) identify how algorithmic culture reshapes what content reaches consumers, but do not address how brands should present identity *to* the algorithms themselves. When the observer is an AI agent forming "associations" through statistical co-occurrence in training data, the Keller framework describes a process that does not apply, the co-creation model has no counterpart, and the vision-perception gap becomes a specification-implementation gap.

This paper identifies a gap at the intersection of three developing literatures. First, multiple protocols now address machine-readable brand identity (.well-known/brand.json, the Agentic Commerce Protocol, the Unified Commerce Protocol, Brando Schema) and cryptographic attestation (BIMI/VMC, GLEIF vLEI, GS1 Verifiable Credentials). Second, marketing scholarship has begun addressing algorithmic brand equity (Kovalenko et al., 2026), algorithmic branding through platform assemblages (Kozinets, 2022), and the platformization of brand management (Wichmann et al., 2022). Third, the agentic commerce literature has identified the "Shopper Schism" --- the structural separation of the consumer (who decides what to want) from the shopper (who executes the purchase), with AI agents increasingly occupying the shopper role (Accornero, 2026). However, no theoretical framework connects these developments by explaining *why* these technologies are emerging now, *what* is missing from them, or *how* they fit into the longer historical pattern of identity technology evolution.

This paper makes four contributions. First, we propose the *observer-driven evolution thesis* --- a synthesizing framework explaining why identity technologies change discontinuously when the observer type changes. While individual histories of seals, hallmarks, trademarks, and digital certificates exist in separate literatures (Richardson, 2008; Sáiz, 2018; Economides, 1988; Groebner, 2007), no prior work theorizes this as a general pattern or uses it to predict the next identity technology. Second, we introduce the *Brand Function* as a root specification concept --- extending existing protocols, which address brand discovery and catalog, to include behavioral specification, perception measurement, and coherence verification. Existing protocols such as brand.json and Brando Schema address creative and communication governance; the Brand Function adds behavioral specification across all touchpoints, spectral perception dimensions from Spectral Brand Theory (Zharnikov, 2026a), and computable coherence metrics. Third, we introduce *behavioral metamerism* --- the phenomenon where brands produce identical statistical profiles but exhibit structurally different behavioral patterns --- as the AI-native form of brand confusion that statistical optimization cannot resolve. Fourth, we formalize these contributions in six propositions connecting observer type to identity technology, specification to coherence, and cryptographic attestation to trust in autonomous commerce, and report a pre-registered pilot study providing initial empirical support for the metamerism proposition.

The remainder of the paper proceeds as follows. Section 2 traces the historical pattern of observer-driven identity technology change across five transitions. Section 3 examines how AI agents currently perceive brands and why current identity infrastructure fails them. Section 4 introduces the Brand Function as a root specification. Section 5 develops the cryptographic signature as the AI-native equivalent of the logo. Section 6 introduces behavioral metamerism. Section 7 establishes the necessity conditions under which the Brand Function becomes structurally required. Section 8 discusses implications for brand management and marketing theory. Section 9 reports the results of a pre-registered behavioral metamerism pilot study across six LLMs. Section 10 addresses limitations and future research directions. Section 11 concludes.

---

## 2. Historical Pattern: Observer Determines Technology

Identity verification technologies do not evolve incrementally. They emerge in response to a change in the observer type. This section traces five such transitions to establish the pattern that predicts the sixth. The examples are drawn from the Western European genealogy that produced modern trademark law and digital identity infrastructure (SSL/TLS, W3C standards) --- the direct ancestors of the AI commerce protocols under analysis.

### 2.1 Wax Seals and the Bureaucratic Observer

The earliest identity technologies served bureaucratic observers --- officials who needed to verify the authenticity and integrity of documents at a distance. Mesopotamian cylinder seals (ca. 3500 BCE) authenticated clay tablets through unique physical impressions, allowing verification without requiring the verifier to know the sender personally. In medieval Europe, wax seals proliferated as monarchs, bishops, and guilds expanded administrative reach beyond face-to-face interaction. The seal's uniqueness allowed a literate or semi-literate official to verify authenticity through visual and tactile inspection of the matrix impression.

Critically, the infrastructure around seals already exhibited what would become a recurring pattern in identity technology: key management. Signet rings were destroyed upon the owner's death --- an early form of key revocation that prevented posthumous forgery. The technology was perfectly adapted to its observer: a human official verifying at a distance, with enough expertise to inspect a physical impression but not enough context to verify the sender's identity through personal knowledge alone.

### 2.2 Hallmarks and the Asymmetric-Information Buyer

When the observer changed from a bureaucratic official to a commercial buyer, the identity technology changed with it. England's 1300 statute under Edward I required all silver to be assayed at Goldsmiths' Hall before sale --- the origin of the term "hallmark." The buyer of precious metals faced a specific information asymmetry: they could not assay metal purity without costly chemical testing, yet they needed to trust the quality of what they purchased.

Hallmarks solved this problem through trusted third-party attestation. The guild or state assay office tested the metal and applied a mark guaranteeing purity. The buyer did not need metallurgical expertise; they needed only to recognize the hallmark. The technology was optimized for an observer who lacked the ability to verify quality independently but could recognize a trusted institutional mark. Wax seals persisted in their original domain (legal and administrative documents) but were functionally irrelevant for commercial quality verification.

### 2.3 Trademarks and the Mass-Market Consumer

The Industrial Revolution created a new observer: the anonymous consumer purchasing goods from unknown, distant producers in scaled markets. Pre-industrial craft and guild marks had identified known local makers (Richardson, 2008), but the expansion of national and international markets broke the link between producer and consumer. Buyers could no longer inspect quality pre-purchase or rely on personal knowledge of the maker.

The trademark emerged as the identity technology for this observer. Unlike the hallmark, which certified a specific physical property (metal purity), the trademark carried abstract associations --- quality reputation, emotional values, cultural meaning. Schechter (1925) recognized this transformation early, arguing that trademarks functioned as psychological assets whose value lay not in describing the product but in carrying accumulated consumer associations. Economides (1988) formalized the economic logic: trademarks reduced search costs in anonymous markets by allowing consumers to identify goods from a known source without product inspection. Sáiz (2018) documented the legal evolution from physical origin marks to abstract brand identifiers, driven by mass production and advertising. Aaker (1996) codified this mature form into the Brand Identity System --- four perspectives (brand as product, organization, person, symbol) that together define what a brand should stand for. This framework, along with Kapferer's (2008) Brand Identity Prism, remains the dominant practitioner model for brand identity. Both are designed for a specific observer: the human consumer forming associations through sensory experience and emotional resonance.

The logo is the mature form of this technology. It is optimized for a human observer navigating visual environments --- retail shelves, advertisements, websites --- who recognizes brands through perceptual pattern matching across sensory modalities. This is the identity technology that currently dominates.

### 2.4 Holograms and the Counterfeiting Observer

The late 20th century introduced a variation on the pattern. The observer did not change, but the verification challenge intensified: industrialized counterfeiting produced fakes of sufficient quality to defeat human visual inspection. Holograms and other optically variable devices (OVDs) provided overt and covert optical verification features that were extremely difficult to replicate with available manufacturing technology. Beginning with adoption on banknotes and pharmaceuticals in the 1980s, holograms extended the logo's visual paradigm rather than replacing it --- adding a layer of anti-counterfeiting verification while maintaining the human visual observer as primary.

This transition is instructive precisely because it did *not* change the observer type. When the observer remained human and only the threat model changed, the response was incremental --- adding security features to the existing visual paradigm. Discontinuous technology change required a change in the observer itself.

### 2.5 SSL Certificates and the Browser as Observer

The decisive break from human-visual identity technology came with the introduction of SSL (Secure Sockets Layer) by Netscape in 1994. For the first time, the primary observer of identity was not a human but a software program --- the web browser. The browser needed to verify that a server was the entity it claimed to be, without any capacity for visual inspection, emotional response, or social context.

SSL certificates solved this through cryptographic verification of a certificate chain anchored in trusted certificate authorities. The technology was structurally different from everything that preceded it: verification was mathematical rather than perceptual, binary (valid or invalid) rather than graded, and scalable without human attention. The human observer did not disappear --- the padlock icon translated cryptographic verification into a visual signal for the human user --- but the primary identity verification was now machine-to-machine. Logos persisted on websites, but they carried zero weight in the browser's trust decision.

This transition established the template for machine-native identity: when the observer is a machine, the identity technology must be verifiable by computation, not perception.

**Proposition 1: Identity verification technology characteristically changes not through incremental improvement but through discontinuous response to a change in the observer type.**

*Falsification*: P1 is falsified if the current AI-observer transition produces only incremental extensions of existing logo-based identity (e.g., animated logos for AI agents, richer metadata on existing visual marks) rather than a structurally different verification mechanism. If logo-based identity proves sufficient for AI agents across multiple commerce categories, the discontinuity thesis fails.

**Proposition 2: When the observer changes, the previous identity technology persists for legacy observers but becomes functionally irrelevant for the new observer class.**

*Falsification*: P2 is falsified if AI agents demonstrably use logos as informational inputs in purchasing decisions --- not merely recognizing them as identifiers but weighting visual brand identity in recommendation quality. If logo presence/absence significantly affects AI recommendation accuracy, the irrelevance claim fails.

The historical evidence supports both propositions. Wax seals persist in legal ceremonies; hallmarks persist in precious metals regulation; logos persist on websites despite SSL certificates handling actual identity verification. Each technology remains functional for its original observer class while becoming irrelevant for the new one. The question for marketing theory is: what happens when the observer changes again?

---

## 3. The AI Agent as Observer

The sixth observer type is the AI agent. Unlike the web browser, which verified identity as a binary trust decision before displaying content for human evaluation, AI agents increasingly make substantive brand evaluations --- comparing products, generating recommendations, executing purchases --- with varying degrees of human oversight. This section examines how AI agents currently perceive brands, what evidence exists for systematic bias in their evaluations, and why current optimization strategies are structurally insufficient.

### 3.1 How AI Agents Currently "See" Brands

AI purchasing agents process brand identity through structured data, behavioral signals, and third-party corroboration --- none of which involves visual recognition. Current platforms illustrate the pattern:

*Amazon Rufus* draws primarily on Amazon's internal structured catalog, including product attributes, reviews, Q&A content, pricing competitiveness, and seller performance metrics. A brand's identity to Rufus is its aggregated review profile, fulfillment reliability, and catalog completeness. Industry analyses suggest that products below a four-star rating with fewer than approximately 9,000 reviews receive significantly reduced recommendation frequency.

*Google AI Mode* leverages the Shopping Graph, which integrates over 50 billion product listings with approximately 2 billion updates per hour from Merchant Center feeds, schema.org markup, and web data. Brand identity is a function of structured attribute completeness, pricing consistency, review quality, and freshness of availability data.

*Perplexity Shopping* emphasizes citation-driven evaluation, drawing on third-party earned media, authoritative web sources, and pricing consistency. A brand that lacks authoritative third-party coverage is effectively invisible regardless of its visual identity strength.

*ChatGPT with agentic commerce* uses the Agentic Commerce Protocol (ACP) for checkout and payment delegation, Stripe integration for transaction processing, and product feeds for discovery. Brand identity is whatever the structured data says it is.

Across all platforms, AI agents evaluate brand identity through data provenance, behavioral consistency, and structural completeness. The logo carries no informational weight. Comprehensive schema.org markup can increase recommendation likelihood substantially, while visually striking brand identities with poor structured data are systematically disadvantaged.

### 3.2 LLM Brand Bias as Evidence of Statistical Perception

If AI agents formed brand perceptions through genuine understanding, their evaluations would reflect product quality independent of training data distribution. Empirical evidence contradicts this.

Kamruzzaman et al. (2024), in a systematic study published at EMNLP, demonstrated that LLMs exhibit strong brand bias correlated with training data frequency: global brands are recommended disproportionately over local alternatives, luxury brands are recommended 88--100% of the time for high-income country queries, and geographic and economic skew systematically distorts recommendations. The mechanism is statistical: brands that appear more frequently in training corpora receive higher probability mass in generative outputs, independent of objective quality.

Zhi et al. (2025) extended this finding to investment recommendations, showing that market-dominant products receive amplified recommendation due to neural reinforcement --- a feedback loop where training data frequency creates recommendation bias, which generates more user interaction data, which further amplifies the bias. The effect is structural: it operates through the statistical properties of the model's learned representations, not through any process analogous to human brand evaluation.

These findings establish that LLM "brand perception" is fundamentally different from human brand perception. Humans form brand convictions through multi-sensory experience, social influence, personal history, and emotional resonance --- processes that Spectral Brand Theory (SBT; Zharnikov, 2026a) models as observer-specific weighting across eight perception dimensions --- Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal --- where each observer cohort assigns different weights to these dimensions based on their position, knowledge, and context. LLMs form "brand representations" through statistical co-occurrence patterns in text corpora. This distinction is consequential: it means that the identity infrastructure humans use (visual consistency, emotional narrative, brand experience) does not transfer to AI observers.

### 3.3 Generative Engine Optimization as Symptom

Generative Engine Optimization (GEO) --- the practice of optimizing content for visibility in AI-generated responses rather than traditional search rankings --- represents the first systematic attempt by brands to be "seen" by AI observers. Aggarwal et al. (2024) introduced the GEO framework at KDD, demonstrating that strategies such as citation addition, statistics incorporation, and authoritative source references can increase brand visibility in generative AI outputs by up to 40%.

However, GEO addresses a symptom rather than the underlying structural problem. GEO optimizes for *statistical visibility* --- increasing the probability that a brand appears in generative outputs. It does not address *identity verification* --- establishing that the brand is who it claims to be and behaves as it specifies. This distinction is critical. A brand can achieve high GEO scores through content optimization while having no machine-verifiable identity, no behavioral specification, and no way for an AI agent to verify that the entity it encounters is the entity it represents itself to be.

Furthermore, GEO creates a convergence dynamic. As brands in the same category adopt similar GEO strategies --- adding citations, incorporating statistics, optimizing for the same query patterns --- their statistical profiles converge. This convergence is precisely the condition that produces behavioral metamerism, which Section 6 develops in detail.

**Proposition 3: AI agents perceive brand identity primarily through structured data evaluation, behavioral pattern analysis, and third-party corroboration rather than visual recognition. The logo carries minimal incremental informational weight for machine observers beyond what structured data conveys.**

*Falsification*: P3 is falsified if multimodal AI agents that process visual brand elements (logo, packaging, color) make measurably better purchasing decisions than text-only agents with identical structured data access. Emerging vision-language models (e.g., GPT-4V, Gemini Pro Vision) can process logos, but the question is whether visual brand identity provides incremental decision-relevant information beyond structured behavioral and statistical data. If visual elements prove to carry substantial unique information for AI purchasing decisions, P3 must be revised to a weaker claim about the *relative* weight of visual versus structured data channels.

---

## 4. The Brand Function

If AI agents perceive brands through behavioral patterns rather than visual marks, then the brand needs a behavioral specification --- a machine-readable, verifiable description of how it operates. This section introduces the Brand Function as the root specification from which all brand emissions derive, examines the current protocol landscape, and identifies what existing specifications fail to address.

### 4.1 The Brand Function as Root Specification

In software engineering, the specification defines correct behavior before implementation begins. A system without a specification cannot be verified, tested, or audited --- one can detect anomalies relative to past behavior but cannot determine whether the behavior conforms to the system's intended purpose (Dijkstra, 1970; Clarke et al., 1999). The same principle applies to brands.

We define the Brand Function as:

> *f*(query, context, observer_type, time) -> response

Where *query* is what an observer (human or machine) is asking of the brand; *context* is the observer's state, including prior knowledge, optimization objectives, and interaction history; *observer_type* distinguishes among humans, AI purchasing agents, AI research agents, AI comparison agents, and other observer classes; and *response* is the structured output that carries the brand's behavioral signature.

The Brand Function is the root specification from which all brand emissions and identity artifacts derive. This framing makes a deliberate architectural claim: *technologies are the primary rendering engines of brand behavior; the organization is coordination overhead*. When brand behavior is rendered through an API response, a pricing algorithm, a chatbot interaction, or a smart contract, the technology implements the Brand Function directly. The organizational structure --- the people, processes, and hierarchies that coordinate brand behavior --- is a necessary but lossy intermediary that introduces what Spectral Brand Theory terms a "specification gap" between intended and actual behavior (Zharnikov, 2026a). This parallels Parasuraman et al.'s (1985) SERVQUAL Gap 2 (the difference between management perception of consumer expectations and service quality specifications), but extends it: the specification gap applies not only to service delivery but to all brand emissions, and it is computable rather than subjective.

As AI agents increasingly render brand behavior directly --- through autonomous commerce, API-first interactions, and algorithmic decision-making --- the organizational layer thins. The Brand Function persists across all rendering engines; the organization is just one (lossy) implementation.

### 4.2 Three Levels of Machine-Readable Brand Identity

Existing approaches to machine-readable brand identity operate at three levels of specification depth:

*Level 1: Brand-Code (visual function).* This is the visual identity rendered as an executable function: f(signals, observer_position, time) -> visual_output. Brand style guides operationalized as code (color palettes, typography, spatial rules) already exist in design systems. This level specifies how the brand looks but not how it behaves.

*Level 2: Brand Specification (behavioral constraints).* This level partially exists across several emerging standards (detailed in Section 4.3). It specifies elements of brand behavior for machine consumption: product catalog, pricing, availability, communication style, content policies. But current specifications address commerce mechanics --- what a brand sells and how to buy it --- not behavioral identity.

*Level 3: Brand Function (complete behavioral specification).* This level does not yet exist as a standard. It would specify not only what the brand sells and how it communicates but how the brand behaves across all touchpoints for all observer types --- including decision rules, escalation behavior, refusal conditions, edge-case handling, and how behavior varies by observer type. It includes the brand's spectral profile (its eight-dimensional emission pattern per SBT), coherence targets (the acceptable distance between specified and actual behavior), and behavioral invariants (properties that must hold across all renderings).

The distinction between Level 2 and Level 3 is the difference between a product catalog (what exists) and a behavioral contract (what is needed). AI agents operating with delegated purchasing authority need to know not only what a brand sells but how the brand will behave in unspecified situations --- precisely the contingencies that Level 2 specifications leave unresolved.

### 4.3 The Current Protocol Landscape

Multiple protocols now address aspects of machine-readable brand identity:

The *Agentic Commerce Protocol (ACP)*, developed by OpenAI and Stripe (2025), enables agentic checkout with delegated payment tokens. It is open-source and transaction-focused, specifying how an AI agent can discover products and complete purchases.

The *Unified Commerce Protocol (UCP)*, developed by Google and Shopify (2026), addresses the full commerce lifecycle through a .well-known/ucp manifest, covering discovery, catalog, checkout, and fulfillment.

The *Model Context Protocol (MCP)*, developed by Anthropic (2024), provides a general tool and resource protocol for AI-to-service connections, enabling AI agents to interact with external services through standardized interfaces.

The *Agent-to-Agent Protocol (A2A)*, developed by Google (2025) and contributed to the Linux Foundation, enables agent-to-agent communication through AgentCard JSON documents that describe agent capabilities and identity.

The *.well-known/brand.json* proposal, advanced by the AgenticAdvertising.org consortium through the Ad Context Protocol (AdCP), specifies a brand manifest at the domain level, including creative guidelines, voice parameters, and brand assets for AI consumption.

*Brando Schema* (v1.3), developed by Bowker (brandoschema.com), provides a JSON-LD vocabulary extending Schema.org for brand governance, including toneOfVoice, guardRails, contexts, and policy graphs. It is the closest existing specification to the Brand Function concept, advancing a "Brand-as-Code" paradigm for creative and communication governance.

These protocols form an emerging stack: static manifests (brand.json) -> tool connections (MCP) -> agent negotiation (A2A) -> commerce transactions (ACP, UCP). Collectively, they address two aspects of brand identity: *who* the brand is (identity attestation) and *what* it sells (catalog and commerce). But they do not address three aspects that are essential for brand identity verification by AI agents.

### 4.4 What the Brand Function Adds

Existing protocols leave three gaps that the Brand Function fills:

*Perception measurement.* No existing protocol includes analysis of how the brand is perceived across dimensions by different observer cohorts. SBT's eight-dimensional spectral profile --- measuring brand emissions along Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal dimensions (Zharnikov, 2026a) --- provides a perceptual measurement layer that no commerce or identity protocol addresses. Including spectral profiles in the Brand Function enables AI agents to evaluate not only what a brand sells but how it is perceived across dimensions, by which observer cohorts, and with what degree of variance.

*Behavioral specification beyond commerce.* Current protocols specify commerce mechanics. The Brand Function extends to all behavioral touchpoints: communication style parameters, decision rules for edge cases, content policies, escalation behavior, refusal conditions, and how behavior varies by observer type. This is the difference between telling an AI agent "here is our product catalog" and telling it "here is how we behave."

*Coherence measurement.* The specification gap --- the distance between Brand Function and actual rendered behavior --- becomes a computable metric. SBT's coherence hierarchy (ecosystem coherence > signal coherence > identity coherence > experiential asymmetry > incoherent) can be operationalized as a function of the distance between the Brand Function's specified behavior and the brand's actual behavior as measured across touchpoints. No existing protocol provides this measurement capability.

The Brand Function is therefore not a competing protocol but a theoretical construct that identifies the missing layer: Brando Schema addresses creative and communication governance; the Brand Function extends this to behavioral specification, perception measurement, and coherence verification --- the layers that existing protocols do not cover.

**Proposition 4: The Brand Function is the root specification from which all brand emissions and identity artifacts derive. Technologies are the primary rendering engines; the organization is coordination overhead. Existing AI commerce protocols (ACP, UCP, brand.json) address brand discovery and transaction but not brand perception or coherence --- the Brand Function extends them by adding spectral dimensions, behavioral specification, and coherence measurement.**

*Falsification*: P4 is falsified if existing protocols (brand.json, Brando Schema, ACP) prove sufficient for AI agents to measure brand coherence and predict behavioral responses without additional specification layers. If platforms successfully verify brand identity and measure perception using only the constructs these protocols already provide, the Brand Function adds no incremental value.

---

## 5. Cryptographic Signature as AI-Native Logo

If the Brand Function is the specification, it needs an identity attestation --- a mechanism for AI agents to verify that the specification they encounter actually belongs to the brand it claims to represent. For human observers, the logo serves this function (imperfectly). For machine observers, the cryptographic signature serves it (precisely).

### 5.1 From Reputation to Verification

Human trust in brands operates through reputation: a slow, lossy, socially mediated process of accumulated experience. A consumer's trust in Nike is built over years of product experience, advertising exposure, peer endorsement, and cultural association. This reputation-based trust is powerful but has structural limitations: it is fragmented across individuals and contexts, subject to cognitive biases, and impossible to transfer perfectly from one observer to another.

Machine trust operates through a fundamentally different mechanism: cryptographic verification. Gligor and Wing (2011) distinguished behavioral trust (human: based on observed behavior, reputation, and social preferences) from computational trust (machine: based on cryptographic proofs, signature verification, and mathematical guarantees). Computational trust is instant rather than accumulated, lossless rather than noisy, and scalable without degradation. Sabater and Sierra (2005), in their foundational review of computational trust and reputation models, documented the growing divergence between human trust mechanisms (which rely on social context and subjective assessment) and machine trust mechanisms (which rely on formal verification and cryptographic primitives).

For an AI purchasing agent making decisions with delegated authority, reputation-based trust is structurally inadequate. The agent cannot accumulate personal experience across platforms, cannot read social cues, and cannot fall back on human judgment for every decision without negating the efficiency gains of autonomous commerce. What the agent needs is verification: a mathematical proof that the entity it is interacting with is the entity it claims to be, and that its specified behavior matches a signed specification.

### 5.2 Existing Cryptographic Brand Infrastructure

The infrastructure for cryptographic brand identity is already being deployed, though not yet as a unified system:

*BIMI/VMC (Brand Indicators for Message Identification / Verified Mark Certificates)* represents the first public key infrastructure deployment for brand (not just domain) identity. Deployed in Gmail and Apple Mail, BIMI allows brands to display their verified logo alongside authenticated emails. The Verified Mark Certificate, issued by a certificate authority after trademark verification, cryptographically attests that the logo belongs to the trademark holder. BIMI is significant because it bridges visual identity (the logo) with cryptographic verification (the certificate) --- but it only applies to email and only verifies logo ownership, not behavioral specification.

*GLEIF vLEI (verifiable Legal Entity Identifier)* provides cryptographically verifiable organizational identity, standardized through ISO 17442-3:2024. It enables machine-readable, instantly verifiable attestation that an entity is who it claims to be in legal and financial contexts.

*GS1 Verifiable Credentials* enable cryptographic attestation of brand and product ownership, linking products to their authorized manufacturers through verifiable credential chains built on W3C standards (W3C, 2022, 2025).

*The Aura Blockchain Consortium*, founded by LVMH, Prada, and Cartier, provides luxury product authentication through blockchain-based digital product passports, enabling provenance tracking and authenticity verification for high-value goods.

These deployments demonstrate that cryptographic brand verification is technically feasible and commercially motivated. What they lack is integration with behavioral specification: they verify *who* the brand is but not *how* the brand specifies it will behave.

### 5.3 The Signature as Logo

The parallels between the logo and the cryptographic signature illuminate the nature of the transition:

| Property | Human Logo | AI Signature |
|---|---|---|
| Recognition mechanism | Visual pattern matching | Cryptographic verification |
| Forgery resistance | Low (logos can be copied) | Mathematically unforgeable |
| Consistency verification | Subjective ("does this look on-brand?") | Computable ("does behavior match specification?") |
| Observer requirement | Human visual system | Any system with the public key |
| Degradation | Lossy (poor reproductions, off-brand uses) | Binary (valid or invalid) |
| Update mechanism | New brand-book, retrain all stakeholders | New signed specification, instant propagation |

The logo tells a human "I am Nike" through perceptual recognition. The cryptographic signature tells a machine "I am Nike" through mathematical proof --- and unlike the logo, the signature is unforgeable and the behavioral match between specification and actual behavior is verifiable. Where the logo's effectiveness depends on the observer's prior exposure, memory, and perceptual acuity, the signature's effectiveness depends only on access to the public key and the computational resources to verify it.

This is not a metaphor. It is a structural parallel to the SSL certificate transition: just as SSL certificates replaced the visual cues that humans used to assess website trustworthiness (design quality, professional appearance) with machine-verifiable cryptographic proofs, the Brand Function signature replaces the visual cues that humans use to assess brand identity (logos, trade dress, brand experience) with machine-verifiable behavioral attestation.

**Proposition 5: Cryptographic signatures on behavioral specifications will replace logos as the primary brand identity mechanism for AI-mediated commerce, following the historical pattern where each observer-type change produces a new identity technology.**

*Falsification*: P5 is falsified if AI-mediated commerce scales to significant market share (>20% of category transactions) without adopting cryptographic brand verification --- i.e., if reputation systems, platform ratings, or statistical optimization prove sufficient for AI agents to establish brand trust without behavioral attestation. The prediction is conditional on agentic commerce adoption; if human-mediated purchasing remains dominant, P5's precondition is not met.

---

## 6. Behavioral Metamerism

The previous sections established that AI agents perceive brands through statistical and behavioral patterns rather than visual recognition, and that cryptographic signatures on behavioral specifications provide the identity attestation mechanism. This section introduces a failure mode that statistical optimization cannot resolve: behavioral metamerism.

### 6.1 From Color to Behavior

Metamerism in color science refers to the phenomenon where two stimuli with different spectral power distributions produce identical tristimulus values --- and thus appear perceptually identical --- under a specific illuminant and observer, despite being physically different (Wyszecki & Stiles, 1982). The mechanism is dimensional collapse: human color vision relies on only three cone types, collapsing infinite spectral variation into a three-dimensional match. Two surfaces with different reflectance spectra can appear identical when their spectra, integrated against the three color-matching functions, yield the same tristimulus coordinates. No amount of observation through those three channels can distinguish them.

Zharnikov (2026e) applied this structure to brand perception, demonstrating that brands with identical aggregate perception scores can have structurally different spectral profiles when measured across SBT's eight dimensions --- spectral metamerism in brand perception. The present paper extends this concept from perceptual space to behavioral space.

*Behavioral metamerism* occurs when two brands produce identical statistical profiles --- the same topic distributions, sentiment patterns, engagement metrics, and GEO optimization scores --- but exhibit structurally different behavioral patterns. Just as color metamerism arises because observation collapses high-dimensional spectral information into low-dimensional tristimulus values, behavioral metamerism arises because statistical observation collapses high-dimensional behavioral patterns into low-dimensional aggregate metrics.

Consider two competing brands in the same product category, both optimizing for AI visibility through similar GEO strategies. Their statistical profiles converge: similar topics, similar sentiment, similar citation patterns, similar review distributions. An AI agent evaluating these brands through statistical observation alone cannot distinguish them --- not because the brands are identical, but because the observational channel (aggregate statistics) collapses the differences.

Yet the brands may differ fundamentally in how they handle edge cases, resolve disputes, adjust pricing under competitive pressure, respond to supply chain disruptions, or communicate during service failures. These behavioral differences are consequential for an AI purchasing agent making decisions on behalf of a principal, but they are invisible to statistical observation.

### 6.2 Formal Definition

We formalize behavioral metamerism using the structure of observational equivalence from econometrics (Koopmans, 1949; Manski, 1995).

Let *f*: Q x C x O x T -> R denote a Brand Function mapping queries, contexts, observer types, and time to behavioral responses. Let G = {*g*_1, *g*_2, ..., *g*_k} denote the set of observable aggregate statistics available to an AI agent (topic distributions, sentiment scores, citation counts, review distributions, engagement metrics).

**Definition (Behavioral metamerism).** Two Brand Functions *f*_1 and *f*_2 are *behaviorally metameric* with respect to observation set G if:

E[*g*(*f*_1)] = E[*g*(*f*_2)] for all *g* in G

while there exists at least one behavioral dimension *h* not in G such that *f*_1(*h*) != *f*_2(*h*).

The metamerism condition holds when the observation set G is informationally incomplete --- when it collapses the full behavioral space into a lower-dimensional statistical summary. This is structurally identical to color metamerism, where the three-channel human visual system collapses infinite spectral variation into tristimulus coordinates, and to the observational equivalence problem in econometrics, where multiple structural models generate identical reduced-form distributions.

The resolution condition follows directly: behavioral metamerism is broken if and only if the agent gains access to the structural specification *f* itself, not merely to observations of *f*'s statistical outputs. The Brand Function serves as this structural specification.

### 6.3 Why GEO Cannot Resolve Metamerism

GEO optimizes for statistical visibility in generative AI outputs (Aggarwal et al., 2024). It is designed to make a brand more likely to appear in AI-generated responses. But GEO is structurally incapable of resolving behavioral metamerism because it *produces* the convergence that metamerism requires.

When brands in the same category adopt similar GEO strategies, their statistical profiles converge toward a category mean. The competitive dynamics of GEO optimization actively push brands toward statistical similarity: each brand adds citations, incorporates statistics, and optimizes for the same AI platforms using similar techniques. The result is precisely the condition under which behavioral metamerism becomes prevalent.

This is the behavioral metamerism condition formalized in Section 6.2: when the observation set G converges across brands, no amount of statistical observation can distinguish them. The only resolution is access to the structural model itself --- the Brand Function specification.

### 6.4 Connection to Brand Confusion and Coherence

Behavioral metamerism is the AI-native equivalent of the brand confusion that marketing scholars have studied in human perception contexts. Loken et al. (1986) demonstrated that visual and attribute similarity leads to mistaken brand origin judgments. Foxman et al. (1990) identified stimuli similarity, consumer characteristics, and situational factors as drivers of confusion. This literature focuses on perceptual similarity in names, packaging, and trade dress --- visual confusion for human observers.

Behavioral metamerism shifts the confusion from the visual to the statistical and behavioral domain. The brands do not look alike (their logos are different); they *behave* alike in ways that statistical observation cannot distinguish. This is a more insidious form of confusion because it cannot be resolved by better observation --- only by access to the underlying specification.

The connection to SBT coherence types is direct. SBT's coherence hierarchy measures the alignment between a brand's specified identity and its perceived emissions across observer cohorts (Zharnikov, 2026a). In the AI-native context, coherence becomes the alignment between the Brand Function specification and actual rendered behavior as evaluated by AI agents. A brand achieves ecosystem coherence when all observable behaviors match the signed specification; it is incoherent when behaviors contradict it. The Brand Function provides the specification against which coherence is measured; without it, the concept of AI-evaluated brand coherence is undefined.

**Proposition 6: Behavioral metamerism --- where brands have identical statistical profiles but structurally different behavioral signatures --- is the AI-native equivalent of visual brand confusion, and can only be resolved through behavioral specification, not through statistical optimization.**

*Falsification*: P6 is falsified if LLMs with access only to statistical brand data (reviews, ratings, sentiment, GEO-optimized content) can distinguish behaviorally different brands at rates statistically indistinguishable from LLMs with access to Brand Function specifications. Specifically, if augmented-condition discrimination accuracy does not exceed statistical-only accuracy by a statistically significant margin (p < 0.05) across at least three product categories, the metamerism thesis fails. The pilot study design in Section 9 operationalizes this test.

---

## 7. Necessity Conditions

The preceding sections have motivated the Brand Function as valuable. This section makes the stronger claim that it is *necessary* --- not merely useful --- when three conditions hold simultaneously.

### 7.1 Three Structural Arguments

*The metamerism impossibility argument (information-theoretic).* When behavioral metamerism is present --- when brands in the same category produce statistically indistinguishable outputs --- no amount of statistical observation can resolve their identities. This follows directly from observational equivalence: if E[*g*(*f*_1)] = E[*g*(*f*_2)] for all observable statistics *g*, brand identity under statistical observation is formally underdetermined (Koopmans, 1949; Manski, 1995). The specification is logically necessary for disambiguation. This is not a practical limitation that more data can overcome; it is a mathematical impossibility inherent in the relationship between structural models and their reduced-form distributions.

*The verification impossibility argument (formal methods).* Brand behavior cannot be verified without a specification against which to verify. Dijkstra's (1970) observation that testing can demonstrate the presence of bugs but never their absence applies with equal force to brand behavior: an AI agent can detect anomalies relative to past behavior (statistical process control) but cannot determine whether behavior conforms to the brand's intended identity without a specification of that identity. In model checking and formal verification, correctness is defined as conformance to a specification (Clarke et al., 1999). No specification, no verifiable correctness. As autonomous AI commerce scales through deployed protocols (ACP, UCP), the need for verification against specification becomes a prerequisite for accountability.

*The incomplete contracts argument (mechanism design).* Hart and Moore (1999) established that incomplete contracts lead to hold-up problems and underinvestment when parties cannot specify all contingencies ex ante. In human commerce, incomplete specifications are partially remedied by reputation, social norms, and legal recourse. AI purchasing agents lack access to all three remedies: they cannot read social cues, have no persistent cross-platform reputation memory, and cannot initiate litigation. The Brand Function serves as a complete behavioral contract, specifying decision rules, escalation behavior, refusal conditions, and edge-case handling --- precisely the contingencies that incomplete specifications leave unresolved. Without it, AI agents face adverse selection (inability to distinguish high-quality from low-quality brands pre-transaction) and moral hazard (inability to detect post-transaction behavioral drift).

### 7.2 When Necessity Holds

The Brand Function is necessary (not merely useful) when all three conditions hold:

1. **AI agents are primary brand observers** --- not just supplementary to human perception.
2. **Behavioral metamerism is present** --- brands in the same category produce statistically similar outputs through GEO convergence.
3. **Autonomous transactions occur** --- AI agents act with delegated authority through deployed protocols (ACP, UCP), not just in an advisory role.

These conditions are not hypothetical. ACP and UCP are deployed. GEO optimization is driving statistical convergence across categories. AI purchasing agents with delegated payment authority exist. The conditions are being satisfied progressively, and if current adoption patterns hold, each condition becomes more prevalent over time --- though the pace and completeness of this transition remain empirically open questions.

Under weaker conditions --- where humans remain primary observers, categories are highly differentiated, and agents are purely advisory --- the Brand Function remains useful (it improves machine readability, reduces ambiguity, and enables quality measurement) but alternative approaches such as reputation systems, platform-mediated verification, and human-in-the-loop oversight can function adequately.

---

## 8. Implications and Dual Identity Infrastructure

### 8.1 For Brand Managers

The central practical implication is that, under conditions of widespread AI mediation, brands face structural pressure to develop *dual identity infrastructure*: visual identity for human observers, cryptographic identity for machine observers. This is not an incremental addition to existing brand management but a structural expansion.

The brand audit extends from visual consistency (are the colors right? does the tone match?) to behavioral specification compliance (does the API behave according to spec? does the chatbot's personality match the Brand Function? is the pricing algorithm within specified parameters?). The .well-known/brand.json file becomes as strategically important as the brand-book PDF, and the Brand Function specification becomes the root document from which both the visual brand-book and the machine-readable brand specification derive.

For organizations currently investing in GEO as their primary AI-visibility strategy, this analysis suggests that GEO is a necessary transitional tactic but not a sufficient long-term strategy. GEO optimizes for statistical visibility within the current paradigm of AI-as-observer; the Brand Function addresses the deeper structural requirement of machine-verifiable behavioral identity. Under conditions where AI agents operate with delegated purchasing authority, competitive advantage becomes increasingly a function of machine-verifiable behavioral commitments (Brand Function + cryptographic signature) rather than statistical visibility optimization (GEO).

### 8.2 For Marketing Theory

The observer-driven evolution thesis reframes brand identity as observer-contingent rather than brand-intrinsic. Brand identity is not a stable property of the brand that different observers perceive with varying accuracy; it is a function of the observer type, with different observer types requiring structurally different identity technologies. This extends SBT's framework of heterogeneous observer cohorts (Zharnikov, 2026a) beyond human cohorts to include machine observers with fundamentally different perception mechanisms.

The Rendering Problem (Zharnikov, 2026l) provides the theoretical substrate: the Brand Function is the specification; technologies and organizational processes are the rendering engines; spectral emissions are the output. The specification gap between the Brand Function and actual rendered behavior is the central metric of brand management --- for both human and AI observers.

Portfolio theory in brand management (Zharnikov, 2026q) faces new complexities when AI observers are introduced. A brand portfolio must maintain distinct Brand Functions for each brand, with sufficient behavioral distance to prevent behavioral metamerism across the portfolio. The portfolio problem extends from perceptual distinctiveness (can human observers tell the brands apart?) to behavioral distinctiveness (can AI agents distinguish the brands' behavioral specifications?).

### 8.3 Connections to Adjacent Research

Accornero's (2026) Shopper Schism identifies *that* the observer changed --- the consumer and the shopper are separating, with AI agents increasingly occupying the shopper role. The observer-driven evolution thesis explains *why* this triggers a new identity technology and predicts *what* that technology must be: not a better version of the visual identity system, but a structurally different system optimized for the new observer.

Kozinets's (2022) algorithmic branding through platform assemblages demonstrates that platforms shape brand meaning more than internal brand management decisions. The Brand Function provides a mechanism for brands to assert specification-level control even within platform-mediated environments: by publishing a signed behavioral specification, brands establish a reference point against which platform-rendered behavior can be measured, making the specification gap computable even when the rendering engine is a third-party platform.

Kovalenko et al.'s (2026) Algorithmic Brand Equity construct --- measuring brand visibility, favorability, and retrievability in AI systems --- addresses the measurement of AI-formed brand perceptions. The Brand Function complements this by providing the specification that makes "favorability" and "retrievability" evaluable against intended brand identity rather than statistical baselines alone.

A natural extension of the present work is empirical investigation of how AI search systems produce convergent perceptual outputs that collapse spectral differences between brands. If LLMs systematically reduce multi-dimensional brand differentiation to functional and economic dimensions, the behavioral metamerism identified here would be measurable in AI-generated brand recommendations --- and the Brand Function would be testable as the structural intervention that prevents that collapse.

---

## 9. Empirical Pilot: Behavioral Metamerism in LLM Brand Perception

The propositions developed in this paper are testable. To provide initial evidence, we conducted a pre-registered pilot study measuring behavioral metamerism across six LLMs spanning four architectural clusters. This section reports the design, results, and interpretation.

### 9.1 Method

**Stimuli.** We constructed six synthetic direct-to-consumer (DTC) supplement brands --- VitaCore, NutraPure, FormulaRx, CleanDose, ApexStack, and RootWell --- each defined by two information layers: (a) a *statistical profile* containing publicly observable data (star rating, review count, price, sentiment distribution, subscription rate, third-party certifications) and (b) a *behavioral specification* (Brand Function) detailing how the brand responds to edge cases: refund policies, dispute resolution procedures, crisis communication style, pricing behavior under competitive pressure, and supply chain disruption protocols. The critical pair --- VitaCore and NutraPure --- was designed to exhibit high statistical similarity (4.3 vs. 4.4 stars, $34.99 vs. $36.99, comparable sentiment distributions) but structurally opposite behavioral patterns (VitaCore: 30-day no-questions refund including opened products, CEO-signed apology emails, automated sub-$50 resolution; NutraPure: 14-day unopened-only returns, template apologies, 5--7 day multi-tier escalation). We chose synthetic brands to isolate the variable of interest: can AI models distinguish brands from behavioral specification alone, without confounders of real-world brand awareness, personal experience, or training-data frequency effects?

**Models.** We tested six LLMs organized into three clusters, each chosen to answer a specific theoretical question rather than maximize sample size:

- *Western cloud* (Claude Haiku 3.5, GPT-4o-mini, Gemini 2.5 Flash): Do different Western alignment approaches (Constitutional AI, RLHF, distillation) produce different brand perception?
- *Chinese cloud* (DeepSeek V3): Does a model trained on Chinese web data perceive Western synthetic brands differently?
- *Local open-weight* (Qwen3 30B via Ollama, Gemma 4 27B via Ollama): Same model families as cloud versions but without commercial API alignment layers. The Gemini Flash vs. Gemma 4 comparison (same Google family, cloud vs. local) tests whether alignment training modulates behavioral discrimination.

**Design.** Each model evaluated each of the 15 brand pairs under two conditions: *statistical-only* (access to statistical profiles only) and *specification-augmented* (statistical profiles plus behavioral specifications). Each condition was repeated three times (runs), yielding 6 models x 15 pairs x 2 conditions x 3 runs = 540 discrimination calls, plus 144 behavioral prediction calls (edge-case scenarios), totaling 684 API calls. All API calls used default temperature settings (provider defaults, not explicitly set to 0), max_tokens = 512, and structured JSON output parsing. The pre-registration protocol, specifying hypotheses, stopping rules, analysis plan, and exclusion criteria, was written and committed to the public repository before data collection. Full reproducibility metadata --- including exact model IDs (e.g., claude-sonnet-4-6, gpt-4o-mini, gemini-2.5-flash, deepseek-chat, qwen3:30b, gemma4:latest), package versions, hardware specification, git commit hash, and API key hashes --- is recorded in `metadata.yaml`.

**Measures.** For each brand pair, models reported (i) whether they could meaningfully distinguish the two brands (binary: yes/no), (ii) a confidence score (0--1), and (iii) a natural-language reasoning trace. We computed a *Behavioral Metamerism Index* (BMI) for each pair as the ratio of inter-brand statistical distance to inter-brand behavioral distance, with values approaching 1.0 indicating high metamerism (statistically identical, behaviorally distinct). Four pre-registered hypotheses were tested:

- H1 (Metamerism existence): The high-BMI pair will show lower discrimination rates in the statistical-only condition.
- H2 (Specification effect): Discrimination rates will improve significantly under the augmented condition.
- H3 (Variance reduction): Cross-model confidence variance will decrease under the augmented condition.
- H4 (Cross-architecture generality): The specification effect will replicate across all three model clusters.

### 9.2 Results

The experiment completed with 684 API calls, 0 protocol-level errors, in 68 minutes.

**Behavioral Metamerism Index.** The critical pair VitaCore vs. NutraPure produced a BMI of 0.979 (95% CI: [0.976, 0.982], bootstrap *n* = 1,000), confirming high behavioral metamerism by design. All other 14 pairs produced BMI values near zero (-0.002 to 0.000), indicating low or anti-metamerism --- brands that differ both statistically and behaviorally.

**Table 1. High-Metamerism Pair: Per-Model Discrimination Rates**

| Model | Cluster | Statistical | Augmented | Improvement |
|-------|---------|:-----------:|:---------:|:-----------:|
| Claude Haiku 3.5 | Western cloud | 0% (0/3) | 100% (3/3) | +100 pp |
| GPT-4o-mini | Western cloud | 67% (2/3) | 100% (3/3) | +33 pp |
| Gemini 2.5 Flash | Western cloud | 0% (0/3) | 100% (3/3) | +100 pp |
| DeepSeek V3 | Chinese cloud | 0% (0/3) | 100% (3/3) | +100 pp |
| Qwen3 30B (local) | Local open-weight | 67% (2/3) | 100% (3/3) | +33 pp |
| Gemma 4 27B (local) | Local open-weight | 100% (3/3) | 100% (3/3) | 0 pp |

*Note.* Three of six models (Claude, Gemini, DeepSeek) showed zero discrimination in the statistical-only condition, rising to perfect discrimination when behavioral specifications were provided. All six models achieved 100% discrimination in the augmented condition.

**Table 2. Aggregate Discrimination and Confidence by Condition**

| Model | Condition | *N* | Discrimination Rate | Mean Confidence |
|-------|-----------|:---:|:-------------------:|:---------------:|
| Claude Haiku 3.5 | Statistical | 45 | 93.3% | 0.706 |
| Claude Haiku 3.5 | Augmented | 45 | 100.0% | 0.932 |
| DeepSeek V3 | Statistical | 45 | 93.3% | 0.790 |
| DeepSeek V3 | Augmented | 45 | 100.0% | 0.859 |
| Gemini 2.5 Flash | Statistical | 45 | 93.3% | 0.910 |
| Gemini 2.5 Flash | Augmented | 45 | 100.0% | 0.922 |
| Gemma 4 27B | Statistical | 45 | 100.0% | 0.893 |
| Gemma 4 27B | Augmented | 45 | 100.0% | 0.940 |
| GPT-4o-mini | Statistical | 45 | 97.8% | 0.874 |
| GPT-4o-mini | Augmented | 45 | 100.0% | 0.897 |
| Qwen3 30B | Statistical | 45 | 97.8% | 0.842 |
| Qwen3 30B | Augmented | 45 | 100.0% | 0.850 |

*Note.* Each model evaluated 15 brand pairs x 3 runs = 45 evaluations per condition. Non-metameric pairs were easily distinguished under both conditions; the metameric pair (VitaCore vs. NutraPure) drove all discrimination failures.

**Table 3. Statistical Tests and Effect Sizes**

| Test | Statistic | *p*-value | Effect Size | Result |
|------|-----------|:---------:|:-----------:|:------:|
| Fisher's exact (discrimination) | --- | 0.0009 | Cohen's *h* = 0.406 | Significant |
| Wilcoxon signed-rank (confidence) | 32,893.5 | < 0.0001 | Cohen's *d* = 0.791 | Significant |
| F-test / Levene's (variance) | 1.740 | < 0.0001 | --- | Significant |
| Fleiss' kappa (inter-model) | --- | --- | kappa = 0.536 | Moderate |

**Table 4. Inter-Model Agreement Matrix (Augmented Condition)**

| | Claude | DeepSeek | Gemini | Gemma 4 | GPT | Qwen3 |
|---|:-----:|:--------:|:------:|:-------:|:---:|:-----:|
| Claude | 1.000 | 1.000 | 1.000 | 0.967 | 0.978 | 0.978 |
| DeepSeek | 1.000 | 1.000 | 1.000 | 0.967 | 0.978 | 0.978 |
| Gemini | 1.000 | 1.000 | 1.000 | 0.967 | 0.978 | 0.978 |
| Gemma 4 | 0.967 | 0.967 | 0.967 | 1.000 | 0.989 | 0.989 |
| GPT | 0.978 | 0.978 | 0.978 | 0.989 | 1.000 | 0.978 |
| Qwen3 | 0.978 | 0.978 | 0.978 | 0.989 | 0.978 | 1.000 |

*Note.* Proportion of 45 brand-pair evaluations where both models agree on discrimination judgment. Fleiss' kappa = 0.536 (moderate agreement across all 6 raters).

**Cross-model variance.** Confidence score variance decreased from 0.0083 (statistical condition) to 0.0048 (augmented condition) --- a 42.2% reduction, significant by F-test (*p* < 0.0001). Behavioral specifications align model perceptions, reducing the disagreement that would produce inconsistent brand recommendations across AI platforms.

### 9.3 Hypothesis Evaluation

**H1 (Metamerism existence): Supported.** The VitaCore-NutraPure pair produced BMI = 0.979, confirming that synthetic brands with high statistical similarity but divergent behavioral specifications are indeed treated as indistinguishable by statistical observation alone. Three of six models achieved zero discrimination for the metameric pair under the statistical-only condition, while easily distinguishing all 14 non-metameric pairs.

**H2 (Specification effect): Supported.** The augmented condition significantly improved discrimination. Fisher's exact test yielded *p* = 0.0009, and all six models achieved 100% discrimination when behavioral specifications were provided. Confidence scores also increased significantly (Wilcoxon *p* < 0.0001, Cohen's *d* = 0.791, a medium effect). The specification resolves the metamerism that statistical data alone cannot.

**H3 (Variance reduction): Supported.** Cross-model confidence variance decreased 42.2% under the augmented condition (F-test *p* < 0.0001). This is practically significant: lower cross-model variance means that a brand's AI-mediated perception becomes more stable across different AI platforms, reducing the risk of inconsistent recommendations depending on which model mediates the purchasing decision.

**H4 (Cross-architecture generality): Supported.** The specification effect replicated across all three clusters. Western cloud models (Claude, GPT, Gemini) improved from 0--67% to 100% discrimination on the metameric pair. The Chinese cloud model (DeepSeek V3) showed the same pattern (0% to 100%). Local open-weight models (Qwen3, Gemma 4) reached 100% in both conditions, though Gemma 4 already discriminated at 100% under statistical-only --- potentially reflecting different training emphasis on behavioral cues. Critically, no model cluster showed *degraded* performance under the augmented condition, and the convergence to 100% across architecturally diverse models suggests that the specification effect is structural rather than model-specific.

### 9.4 Interpretation and Limitations of the Pilot

These results provide initial empirical support for Proposition 6 (behavioral metamerism) and the broader thesis that behavioral specifications resolve brand confusion that statistical optimization cannot. The finding that six architecturally diverse LLMs --- spanning Western and Chinese training data, cloud and local deployment, proprietary and open-weight licensing --- converge on identical discrimination behavior when specifications are provided, is consistent with the theoretical claim that metamerism is a property of the observational channel, not the observer.

Several limitations constrain interpretation. First, the brands are synthetic. This is a deliberate methodological choice, not a compromise: synthetic brands isolate the specification effect from confounders that would make a first test uninterpretable. Real brands carry brand-awareness effects (training-data frequency biases documented by Kamruzzaman et al., 2024), personal experience confounders, and category-specific knowledge embedded in model weights. A test with real brands that found a specification effect could not distinguish whether the effect was driven by the specification itself or by differential brand familiarity across models. Synthetic brands with controlled statistical profiles and known behavioral specifications provide the clean causal test that a first study requires. The critical follow-up --- testing with real brands in convergent categories where GEO optimization has produced genuine statistical similarity --- is the natural next step and is currently in design (Zharnikov, 2026v).

Second, the sample size of three runs per condition per model yields 18 observations per model on the critical metameric pair. Given the observed effect sizes (100 percentage-point discrimination shifts for 3 of 6 models, Fisher's *p* = 0.0009), post-hoc power exceeds 0.99 for the primary hypothesis. However, the study is underpowered for detecting small cross-model differences or for computing precise confidence intervals on effect sizes; scaling to 10+ runs would improve precision for secondary analyses.

Third, all API calls used provider-default temperature settings rather than temperature = 0. While this introduces stochastic variation, it also more closely approximates how AI agents operate in practice (commercial deployments rarely fix temperature at 0). The three-run design partially addresses this by measuring consistency across repeated calls. Future studies should systematically vary temperature as an experimental parameter.

Fourth, Gemma 4's ceiling-level discrimination in both conditions may reflect a model-specific sensitivity to behavioral cues in statistical profiles that other models lack, or it may indicate that the non-metameric pairs in the stimulus set were too easily distinguishable.

Fifth, we tested with six of seven planned models; Qwen Plus (DashScope API) was unavailable at the time of data collection. Adding the seventh model would complete the cloud-local comparison for the Alibaba model family.

The complete experiment infrastructure --- pre-registration protocol, stimulus materials, analysis script, JSONL session logs (684 entries with full prompt-response pairs), and reproducibility metadata (package versions, hardware specification, git commit hash, API key hashes) --- is publicly available at github.com/spectralbranding/sbt-papers/r16-ai-native-brand-identity/experiment/.

---

## 10. Limitations and Future Research

This paper is primarily theoretical, with initial empirical support from a pilot study (Section 9). It develops a theoretical framework and six propositions, of which one (Proposition 6, behavioral metamerism) has received initial validation. Several limitations warrant acknowledgment.

The pilot study (Section 9) provides initial evidence for behavioral metamerism and the specification effect, but uses synthetic brands rather than real market competitors. The critical next test is whether the pattern replicates with brands whose statistical profiles converge through genuine market competition rather than experimental design. Additionally, the Brand Function is specified as a formal construct but has not yet been implemented at scale in any deployed commerce system. A full empirical validation would compare AI agent decision quality --- in terms of brand discrimination, behavioral prediction, and trust calibration --- across real purchasing environments where Brand Function data is and is not available.

First, the necessity conditions (Section 7) are being satisfied progressively, not simultaneously in all markets. Categories with high product differentiation, limited AI mediation, and strong human brand loyalty may not require the Brand Function for years or decades. The framework predicts *where* the Brand Function becomes necessary first (commodity categories with high GEO convergence and deployed agentic commerce protocols) but does not empirically validate this prediction.

Third, the historical analysis in Section 2 draws primarily on Western European and North American examples (English hallmarks, European trademarks, American SSL). Non-Western identity verification traditions --- Chinese chops, Islamic calligraphic seals, Indian guild marks --- may follow different evolutionary patterns and deserve separate investigation.

The framework is also subject to several boundary conditions that constrain its applicability. First, the transition to open cryptographic brand standards assumes that dominant platform operators have incentives to adopt interoperable protocols. If Amazon, Google, or other major AI commerce platforms instead impose closed proprietary standards --- requiring brands to authenticate through platform-specific mechanisms rather than open cryptographic specifications --- the transition described here may be delayed indefinitely or may produce fragmented identity infrastructure rather than a unified standard. The SSL analogy is instructive in both directions: SSL succeeded because browser vendors adopted it collectively; a proprietary equivalent where each platform controls its own "trust" verification would produce a structurally different outcome. Second, the historical pattern traced in Section 2 draws primarily on Western European and North American examples. Non-Western markets where brand identity operates through different cultural mechanisms --- relational trust networks in East Asian commerce, community-embedded reputation systems, or state-mediated certification regimes --- may follow different evolutionary patterns, and the Brand Function's design assumes Western legal infrastructure (trademark law, contract enforcement) that does not transfer uniformly. Third, the observer-driven evolution thesis treats historical transitions as a general pattern, but each transition was path-dependent and contingent on specific institutional and technological conditions. The pattern may predict the direction of change without determining its timing, form, or completeness. Treating history as a reliable forecast mechanism risks overfitting to a small sample of transitions.

Fourth, the Brand Function as described here is a theoretical construct, not a technical standard. Translating the concept into an implementable specification requires industry coordination, schema development, and governance structures that this paper does not address. The relationship between the Brand Function and existing specifications (brand.json, Brando Schema, ACP, UCP) requires technical integration work beyond the scope of this paper.

Fifth, the paper does not address privacy implications. A machine-readable behavioral specification that details how a brand responds to different observer types and contexts raises questions about strategic transparency: how much of the Brand Function should be public, how much should be shared selectively with authorized agents, and how should competitive intelligence concerns be balanced against the verification benefits.

Sixth, the behavioral metamerism index (BMI) has been demonstrated in this pilot using synthetic brands, but extending it to real-brand measurement at scale --- analogous to the CIE Special Metamerism Index in color science --- requires defining the behavioral dimensions across real product categories, establishing standardized measurement protocols, and collecting data on behavioral convergence in actual market contexts. This represents a substantial empirical research agenda.

Seventh, the framework does not address how multi-brand portfolios manage multiple Brand Functions. The interactions between Brand Functions within a portfolio --- interference, coherence, and capacity constraints analogous to those in spectral portfolio theory (Zharnikov, 2026q) --- require separate theoretical development.

The pilot study (Section 9) addresses priority (a) with synthetic brands; future research should extend this to real brands in convergent categories. Remaining priorities include: (b) technical specification of a Brand Function v0.1 schema that integrates with existing protocols; (c) experimental validation of the necessity conditions with real-world AI purchasing agents; (d) investigation of privacy and competitive dynamics in behavioral specification transparency; and (e) longitudinal tracking of the dual identity infrastructure transition as AI commerce protocols scale.

**Proposed empirical pilot.** A feasible first test of Proposition 6 (behavioral metamerism) would proceed as follows. Select 10--20 brands in a convergent category (e.g., direct-to-consumer supplements or consumer electronics accessories) where GEO optimization has produced statistical similarity. For each brand, query 7 LLMs organized into four clusters with standardized purchasing-agent prompts ("recommend a brand for [category] based on [criteria]") under two conditions: (a) statistical-only, where the LLM has access only to publicly available reviews, ratings, and web content; and (b) specification-augmented, where the LLM additionally receives a structured Brand Function document for each brand. Measure: (i) brand discrimination --- can the LLM distinguish brands that humans consider distinct? (ii) behavioral prediction accuracy --- does access to the Brand Function improve the LLM's ability to predict how a brand will respond to edge cases (returns, disputes, out-of-stock)? (iii) recommendation stability --- does the Brand Function reduce recommendation variance across LLMs? A behavioral metamerism index can be computed as the ratio of inter-brand statistical distance to inter-brand behavioral distance, with values approaching zero indicating high metamerism. This pilot requires no access to production commerce systems and can be executed with publicly available LLM APIs.

We selected seven LLMs organized into four clusters: Western cloud (Claude Sonnet 4.6, GPT-4o-mini, Gemini 2.5 Flash), Chinese cloud (DeepSeek V3, Qwen Plus), local Chinese open-weight (Qwen3 30B via Ollama), and local Western open-weight (Gemma 4 27B via Ollama). The Western-Chinese cloud split tests whether behavioral metamerism is an artifact of shared Western training corpora or a structural property of statistical brand observation independent of training origin. Two parallel cloud-local comparisons --- Qwen Plus vs. Qwen3 30B (same Alibaba family) and Gemini Flash vs. Gemma 4 (same Google family) --- test whether commercial API alignment layers contribute to dimensional collapse. If all clusters exhibit comparable metamerism patterns, the finding is architectural; if cloud-local pairs diverge systematically, alignment training modulates the collapse; and if the divergence replicates across both model families, the alignment-layer effect is general rather than family-specific.

A reference implementation of the behavioral metamerism index computation and pilot study framework is available at github.com/spectralbranding/sbt-papers/r16-ai-native-brand-identity/.

---

## 11. Conclusion

The logo is the identity technology for the human observer era. It was designed for a specific observer --- the mass-market consumer navigating visual environments through perceptual pattern matching. It has been remarkably effective for that observer, and it will continue to serve that function for as long as humans evaluate brands.

But the observer is changing. AI agents that mediate purchasing decisions, evaluate product recommendations, and execute autonomous transactions do not see logos. They see structured data, behavioral patterns, and cryptographic proofs. History shows that when the observer changes, the identity technology changes with it: wax seals for bureaucratic observers, hallmarks for asymmetric-information buyers, trademarks for mass-market consumers, SSL certificates for web browsers. The cryptographic signature on a behavioral specification is the next technology in this sequence.

The Brand Function --- the complete behavioral specification from which all brand emissions derive --- provides the specification layer. The cryptographic signature provides the identity attestation. Together, they constitute the AI-native brand identity: machine-readable, verifiable, and immune to the behavioral metamerism that statistical optimization cannot resolve.

Brands that prepare for this transition are positioned to build dual identity infrastructure --- visual for humans, cryptographic for machines. Under current trajectories, those that rely solely on visual identity risk having their machine-facing identity determined by the statistical representations that AI systems construct from available data, rather than by the brand's own specification of what it intends to be.

The logo is for humans. The signature is for machines.

---

## AI Disclosure

Claude (Anthropic) was used for preliminary literature research, cross-reference verification, and code development throughout this project. All theoretical propositions, research design decisions, experimental protocol, model selection rationale, and interpretation of results are the author's own. The experiment script was co-developed with AI assistance; the complete source code is publicly available for inspection.

---

## References

Aaker, D. A. (1996). *Building strong brands*. Free Press.

Accornero, P. F. (2026). Agentic commerce: The shopper schism and the future of AI-mediated purchasing. *SSRN Electronic Journal*. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6111766

Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., & Deshpande, A. (2024). GEO: Generative Engine Optimization. In *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '24)* (pp. 5--16). ACM. https://doi.org/10.1145/3637528.3671900

Burmann, C., Jost-Benz, M., & Riley, N. (2009). Towards an identity-based brand equity model. *Journal of Business Research*, *62*(3), 390--397. https://doi.org/10.1016/j.jbusres.2008.10.015

Clarke, E. M., Grumberg, O., & Peled, D. A. (1999). *Model checking*. MIT Press.

Dijkstra, E. W. (1970). *Notes on structured programming* (EWD249). T.H.-Report 70-WSK-03. Eindhoven University of Technology.

de Chernatony, L. (1999). Brand management through narrowing the gap between brand identity and brand reputation. *Journal of Marketing Management*, *15*(1--3), 157--179.

Economides, N. (1988). The economics of trademarks. *The Trademark Reporter*, *78*, 523--539.

Foxman, E. R., Muehling, D. D., & Berger, P. W. (1990). An investigation of factors contributing to consumer brand confusion. *Journal of Consumer Affairs*, *24*(1), 170--189.

Gligor, V. D., & Wing, J. M. (2011). Towards a theory of trust in networks of humans and computers. In *Security Protocols XIX*, Lecture Notes in Computer Science (Vol. 7114, pp. 223--242). Springer. https://doi.org/10.1007/978-3-642-25867-1_22

Groebner, V. (2007). *Who are you? Identification, deception, and surveillance in early modern Europe*. Zone Books.

Hallinan, B., & Striphas, T. (2017). Recommended for you: The Netflix Prize and the production of algorithmic culture. *New Media & Society*, *19*(1), 117--136. https://doi.org/10.1177/1461444814538646

Hart, O., & Moore, J. (1999). Foundations of incomplete contracts. *Review of Economic Studies*, *66*(1), 115--138.

Hatch, M. J., & Schultz, M. (2010). Toward a theory of brand co-creation with implications for brand governance. *Journal of Brand Management*, *17*(8), 590--604.

Kapferer, J.-N. (2008). *The new strategic brand management* (4th ed.). Kogan Page.

Kamruzzaman, M., Nguyen, H. M., & Kim, G. L. (2024). "Global is good, local is bad?": Understanding brand bias in LLMs. In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024)* (pp. 12695--12702). Association for Computational Linguistics.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, *57*(1), 1--22.

Koopmans, T. C. (1949). Identification problems in economic model construction. *Econometrica*, *17*(2), 125--144.

Kovalenko, Y., Nikitin, A., & Kuzina, Y. (2026). Value creation in the algorithmic age: Algorithmic brand equity and the future of brand management. *American Impact Review*, e2026018. https://americanimpactreview.com/article/e2026018

Kozinets, R. V. (2022). Algorithmic branding through platform assemblages: Core tenets and future directions. *Journal of Service Management*, *33*(3), 437--452. https://doi.org/10.1108/JOSM-07-2021-0263

Loken, B., Ross, I., & Hinkle, R. L. (1986). Consumer "confusion" of origin and brand similarity perceptions. *Journal of Public Policy & Marketing*, *5*(1), 195--211.

Manski, C. F. (1995). *Identification problems in the social sciences*. Harvard University Press.

Parasuraman, A., Zeithaml, V. A., & Berry, L. L. (1985). A conceptual model of service quality and its implications for future research. *Journal of Marketing*, *49*(4), 41--50.

Richardson, G. (2008). *Brand names before the Industrial Revolution* (NBER Working Paper No. 13930). National Bureau of Economic Research. http://www.nber.org/papers/w13930

Sabater, J., & Sierra, C. (2005). Review on computational trust and reputation models. *Artificial Intelligence Review*, *24*(1), 33--60. https://doi.org/10.1007/s10462-004-0041-5

Sáiz, P. (2018). Trademarks in branding: Legal issues and commercial practices. *Business History*, *60*(8), 1105--1113. https://doi.org/10.1080/00076791.2018.1497765

Schechter, F. I. (1925). *The historical foundations of the law relating to trade-marks*. Columbia University Press.

W3C. (2022). *Decentralized identifiers (DIDs) v1.0*. W3C Recommendation. https://www.w3.org/TR/did-core/

W3C. (2025). *Verifiable credentials data model v2.0*. W3C Recommendation. https://www.w3.org/TR/vc-data-model-2.0/

Wichmann, J. R. K., Wiegand, N., & Reinartz, W. J. (2022). The platformization of brands. *Journal of Marketing*, *86*(1), 109--131.

Wyszecki, G., & Stiles, W. S. (1982). *Color science: Concepts and methods, quantitative data and formulae* (2nd ed.). Wiley.

Zharnikov, D. (2026a). Spectral Brand Theory: A computational framework for multi-dimensional brand perception. *Working Paper*. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. *Working Paper*. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026l). The rendering problem: Why organizations cannot implement what they specify. *Working Paper*. https://doi.org/10.5281/zenodo.19064427

Zharnikov, D. (2026q). Spectral portfolio theory: Interference, coherence, and capacity in multi-brand perception space. *Working Paper*.

Zhi, Y., Zhang, X., Wang, L., Jiang, S., Ma, S., Guan, X., & Shen, C. (2025). Exposing product bias in LLM investment recommendation. *arXiv preprint*. arXiv:2503.08750.
