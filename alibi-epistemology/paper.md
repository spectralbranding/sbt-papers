# The Atom-Cloud-Fact Epistemological Pipeline: From Financial Document Processing to Brand Perception Modeling

**Dmitry Zharnikov**

Working Paper — February 2026

*Contact: dmitry@spectralbranding.com*

| | |
|---|---|
| **Applied framework** | [github.com/spectralbranding/sbt-framework](https://github.com/spectralbranding/sbt-framework) |
| **Source code** | [github.com/viberesearch/alibi](https://github.com/viberesearch/alibi) |
| **SBT paper** | [Zenodo DOI](https://doi.org/10.5281/zenodo.18945912) |
| **License** | MIT |

---

## Abstract

This paper argues that the atom-cloud-fact pipeline constitutes an epistemological architecture demonstrably transferable across at least two structurally distinct domains. The pipeline models knowledge formation through three formally specified stages: atomic observation (typed, source-bound data extraction), probabilistic cloud formation (weighted multi-dimensional clustering), and fact collapse (threshold-based crystallization with full re-collapse on new evidence). Four propositions are developed: (P1) the pipeline's external-corroboration requirement structurally reduces confirmation bias relative to single-source methods; (P2) multi-model replication produces more robust assessments because framework-driven conclusions are replicable while model-specific artifacts are not — conditioned on architectural divergence and structural convergence, with human-subject validation required; (P3) three-stage epistemic separation prevents category errors conflating brand signals, perception clouds, and brand convictions; and (P4) cross-model disagreement is diagnostic of evidential ambiguity, not model failure. The architecture originated in financial document processing; its seven principles transfer with parametric extension to brand perception modeling, producing Spectral Brand Theory (SBT). Existing approaches — Bayesian updating, AGM revision, Dempster-Shafer theory, and symbolic expert systems — each fail structurally for at least one of four requirements: path-independence, observer heterogeneity, epistemic separation, or linguistic implementability. The cross-domain transfer supports the claim that the pipeline captures a general structure of knowledge formation from heterogeneous observation.

**Keywords:** epistemology, probabilistic knowledge, observation pipeline, domain transfer, computational framework, brand perception, confirmation bias

---

How does knowledge form from observation? The question is ancient — addressed by epistemologists from Peirce's (1931–1958) theory of abductive inference to Goldman's (1986) naturalized epistemology. The computational answer is surprisingly recent — and surprisingly underdeveloped.

In most software systems, "knowledge" is an input, not an output. A database stores facts that humans have already determined. A search engine retrieves documents that humans have already written. A machine learning classifier assigns labels that humans have already defined. The system manipulates knowledge; it does not *form* it.

But certain computational problems require the system to form knowledge from raw observations — to progress from "I see data point X" through "I hypothesize that X and Y belong together" to "I know that X and Y describe the same real-world event." This progression — observation to hypothesis to knowledge — has a structure. This paper describes that structure.

The atom-cloud-fact pipeline was developed for a specific problem: reconciling financial documents. A business generates receipts, invoices, bank statements, and payment confirmations. These documents describe the same underlying transactions — but differently. A receipt shows line items and a total. A bank statement shows a date and amount. An invoice shows a vendor and terms. The system must extract observations from each document, cluster observations that likely describe the same transaction, and determine when sufficient evidence exists to confirm that a specific purchase occurred.

The solution required three epistemological stages with formally distinct properties: observations that are typed and source-bound (atoms), hypotheses that are probabilistic and revisable (clouds), and knowledge that is threshold-based and subject to full recalculation (facts). Seven architectural principles emerged from the implementation, governing how observations are typed, how they cluster, and how knowledge crystallizes and re-crystallizes.

The principles transfer to brand perception modeling without domain specialization. When applied to brand perception — a domain with no obvious connection to receipt reconciliation — the same architecture produces a framework (Spectral Brand Theory) that generates capabilities that traditional single-observer brand frameworks cannot represent (Zharnikov 2026a, §2.6). The domain transfer works because the underlying epistemic structure is identical: heterogeneous observers perceive typed signals, cluster them into probabilistic impressions, and — if sufficient evidence accumulates — crystallize those impressions into stable convictions.

This paper makes three contributions: (1) it specifies the atom-cloud-fact pipeline as a domain-general epistemological architecture, formalizing the three-stage progression from observation to hypothesis to knowledge; (2) it isolates the re-collapse mechanism — full dissolution and rebuild of knowledge on new evidence — as the architectural commitment that distinguishes this framework from Bayesian updating and AGM revision; and (3) it demonstrates successful cross-domain transfer from financial document reconciliation to multi-cohort brand perception modeling, with the heterogeneous-observer extension as the key parametric adaptation. Each contribution maps to the empirical sections that follow.

The work can be read within the design-science tradition in information systems research (Hevner, March, Park, & Ram, 2004; Gregor & Jones, 2007): the artifact is the pipeline itself; its utility lies in enabling systems that natively support observer heterogeneity and non-incremental knowledge revision. The primary frame of the paper, however, is epistemological rather than artifact-evaluative — the pipeline is presented as a candidate general structure of knowledge formation, not solely as an IS design recommendation.

---

## 2. The Pipeline Architecture

### 2.1 Three Stages of Knowledge Formation

The pipeline models knowledge formation as a three-stage progression. Each stage has formally distinct properties:

```
Stage 1: OBSERVATION         Stage 2: HYPOTHESIS         Stage 3: KNOWLEDGE
─────────────────           ─────────────────           ─────────────────
Atoms                       Clouds                      Facts
- Typed                     - Probabilistic             - Threshold-based
- Source-bound              - Multi-source              - Revisable
- Immutable                 - Revisable                 - Rebuilt, not patched
- Dimensional               - Weighted                  - Observer-specific
```

Observer-specificity in the rightmost column applies in the brand perception domain, where multiple cohorts process the same signal environment with different scoring weights. In the financial domain, the system is the sole observer with fixed weights; observer-specificity is therefore latent in the architecture but becomes active only in the brand transfer described in the Domain Transfer section.

**Stage 1: Atomic Observation.** Raw data is extracted from source documents and decomposed into typed atoms. Each atom belongs to exactly one dimension (vendor, amount, date, etc.) and exactly one source document. Atoms are immutable — once extracted, they do not change. They are the ground truth of what was observed.

**Stage 2: Cloud Formation.** Atoms from different sources cluster into probabilistic hypothesis clouds — a process structurally analogous to gestalt grouping (Koffka, 1935), where discrete perceptual elements are assembled into coherent wholes through proximity, similarity, and closure. A cloud represents "these atoms probably describe the same real-world event." Clouds are scored through weighted multi-dimensional comparison. They are inherently uncertain and continuously revisable as new atoms arrive.

**Stage 3: Fact Collapse.** When a cloud's score exceeds a threshold, it collapses into a fact — confirmed knowledge. The collapse is functionally analogous to Kahneman's (2011) System 1 processing: once the evidence threshold is met, the hypothesis becomes an automatic, low-effort conviction rather than an effortful evaluation. Facts are not permanent: when new evidence arrives that contradicts an existing fact, the fact dissolves and the system rebuilds from the full atom set. This re-collapse mechanism ensures that knowledge is always consistent with the total evidence, not incrementally patched.

### 2.2 Seven Architectural Principles

Seven principles govern the pipeline's operation. Each was discovered through the financial implementation and proves transferable across domains with parametric adaptation:

Table 1: Seven Principles of the Atom-Cloud-Fact Architecture.

| # | Principle | Definition | Financial Implementation |
|---|-----------|-----------|------------------------|
| 1 | Dimensional typing | Observations belong to typed dimensions | 6 atom types: VENDOR, ITEM, PAYMENT, DATETIME, AMOUNT, TAX |
| 2 | Source binding | Each observation belongs to exactly one source | Atoms belong to exactly one document |
| 3 | Identity gate | Core identity match is a precondition for clustering | Vendor name must match before any other comparison |
| 4 | Asymmetric tolerances | Context determines what "close enough" means | Receipt + statement: 5-day tolerance; invoice + payment: 60 days |
| 5 | Weighted multi-dimensional scoring | Not all dimensions contribute equally | Vendor .30, amount .40, date .20, location .15, items .50 bonus |
| 6 | Re-collapse on new evidence | Knowledge is rebuilt from scratch, never patched | Facts recalculated from full atom set on any change |
| 7 | Epistemic separation | Observations, hypotheses, and knowledge are structurally distinct | Atoms, clouds, and facts stored and processed separately |

**Principle 1: Dimensional typing** ensures that observations are categorized before comparison. Two atoms can only be compared if they share a dimension. A vendor name does not "match" a price — they exist on different dimensions. This prevents false correlations and enables dimension-specific scoring.

**Principle 2: Source binding** ensures that no observation claims to have been made from two sources simultaneously. This prevents circular evidence: a receipt atom cannot corroborate itself by appearing in two clouds. Each atom is evidence from one source, period.

**Principle 3: Identity gate** is the most architecturally significant principle. Before any multi-dimensional comparison occurs, the system must determine: do these atoms describe the same entity? In financial processing, the vendor gate answers: are these two documents about the same merchant? If the gate fails, no further comparison is attempted — the atoms are noise to each other regardless of how well other dimensions align. The identity gate is a binary precondition, not a weighted score.

**Principle 4: Asymmetric tolerances** acknowledge that "close enough" is context-dependent — a form of fuzzy matching that resonates with Zadeh's (1965) formalization of graded set membership. A receipt and a bank statement for the same purchase might have different dates (the bank processes the charge days later). But an invoice and its payment might be separated by months. The tolerance is not a property of the dimension — it is a property of the source-pair interaction.

**Principle 5: Weighted multi-dimensional scoring** reflects the empirical reality that some dimensions are more diagnostic than others. An amount match is stronger evidence than a date match (many transactions happen on the same day; fewer share the same amount). The weights are additive contribution coefficients, not normalized probabilities: core dimensions (vendor .30, amount .40, date .20) yield a base score up to .90, while bonus dimensions (location .15, items .50) can push the score higher. Bonus dimensions apply only when those dimensions are present in the evidence; they are auxiliary multipliers that reward richer evidence, not required inputs. The total is capped at 1.0. This design rewards corroborating evidence from multiple dimensions without requiring every dimension to be present.

**Principle 6: Re-collapse** is the principle that most strongly distinguishes this architecture from incremental systems. When new evidence arrives, the system does not update the existing fact — it dissolves the fact and rebuilds from the complete atom set. This is computationally expensive but epistemically correct: the new evidence may change the entire interpretation of the data, not just append to it. A newly discovered receipt might reassign atoms from one cloud to another, changing which facts exist. Incremental update cannot handle this; full recalculation can.

**Principle 7: Epistemic separation** requires that atoms, clouds, and facts are stored and processed in separate systems with separate interfaces. An atom cannot be "promoted" to a fact — it must pass through cloud formation and collapse. A fact cannot be "demoted" to a cloud — it must be dissolved and the atoms re-clustered. This separation prevents epistemic shortcuts that would compromise the pipeline's integrity.

---

## 3. Financial Implementation

### 3.1 The Reconciliation Problem

The financial reconciliation problem is a variant of probabilistic record linkage — the task of identifying which records across different databases refer to the same real-world entity (Fellegi and Sunter, 1969; Christen, 2012). The atom-cloud-fact pipeline differs from classical record linkage in three respects: it operates on unstructured documents rather than database records, it maintains the three-stage epistemic separation (observation, hypothesis, knowledge) rather than collapsing directly to a match/non-match decision, and it supports the re-collapse principle (Principle 6) where established facts can be fully recalculated on new evidence. These differences are structural consequences of the pipeline's epistemological architecture rather than implementation choices.

A typical business generates four document types for a single transaction: a receipt (from the vendor), an invoice (from the vendor), a bank statement (from the financial institution), and a payment confirmation (from the payment processor). These documents contain overlapping but non-identical information:

Table 2: Document Types and Their Atom Dimensions in Financial Processing.

| Document | Atoms Extracted | Typical Dimensions |
|----------|-----------------|-------------------|
| Receipt | Vendor, items, amounts, tax, date, payment method | VENDOR, ITEM, AMOUNT, TAX, DATETIME, PAYMENT |
| Invoice | Vendor, items, amounts, terms, invoice number | VENDOR, ITEM, AMOUNT, DATETIME |
| Bank statement | Merchant name, amount, date, reference | VENDOR, AMOUNT, DATETIME |
| Payment confirmation | Vendor, amount, date, transaction ID | VENDOR, AMOUNT, DATETIME, PAYMENT |

The challenge: the same transaction appears in different documents with different representations. The receipt says "STARBUCKS #12345" while the bank statement says "SQ *STARBUCKS CORP." The receipt date is March 15; the bank posts on March 17. The receipt shows $4.95; the bank shows $5.20 (tip added). The atoms describe the same real-world event but differ on every dimension.

### 3.2 Pipeline in Action

**Atom extraction**: Each document is parsed into typed atoms. The receipt yields: VENDOR("STARBUCKS #12345"), AMOUNT($4.95), DATETIME(2026-03-15), ITEM("Tall Latte"), PAYMENT("Visa ...4821"). The bank statement yields: VENDOR("SQ *STARBUCKS CORP"), AMOUNT($5.20), DATETIME(2026-03-17).

**Identity gate**: The vendor atoms are compared through fuzzy matching. "STARBUCKS #12345" and "SQ *STARBUCKS CORP" pass the gate (both resolve to the Starbucks canonical entity). Without this gate pass, the atoms would never cluster.

**Cloud formation**: The atoms cluster into a cloud with the following scores: vendor match .85 (high confidence after canonical resolution), amount match .70 (close but not exact — the tip explains the difference), date match .80 (2-day gap within the 5-day tolerance for receipt-statement pairs), location match .90 (GPS coordinates from the receipt place the transaction within 100m of the known Starbucks). Weighted score: .30(.85) + .40(.70) + .20(.80) + .15(.90) = .255 + .280 + .160 + .135 = .830.

**Collapse**: The cloud-matching threshold is .50 — a bundle scoring below this is assigned to a new cloud rather than merged with an existing one. The cloud score (.830) comfortably exceeds the threshold. The cloud collapses into a fact: "Confirmed purchase at Starbucks, March 15, $5.20 (receipt $4.95 + tip)."

**Re-collapse trigger**: If a second receipt arrives for the same Starbucks on the same day (a colleague's lunch), the system dissolves the fact and recalculates. The new atom set might produce two clouds where there was one, splitting the bank charge differently. The fact is not patched — it is rebuilt from scratch.

---

## 4. Domain Transfer: From Financial Facts to Brand Perception

### 4.1 The Mapping

The domain transfer from financial processing to brand perception preserves all seven principles while changing the domain vocabulary:

Table 3: Domain Transfer Mapping: Financial to Brand Perception.

| Concept | Financial Domain | Brand Perception Domain |
|---------|-----------------|----------------------|
| **Atom** | Data point from a document (vendor, amount, date) | Signal from a brand source (logo, price, product experience) |
| **Dimension** | 6 types (VENDOR, ITEM, AMOUNT, DATETIME, TAX, PAYMENT) | 8 types (Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal) |
| **Source** | Document (receipt, invoice, statement) | Encounter type (campaign, store visit, product use, news, review) |
| **Identity gate** | Vendor canonical matching | Brand recognition (logo, name, visual identity) |
| **Cloud** | "These atoms probably describe the same transaction" | "This is what I think the brand is" (perception cloud) |
| **Fact** | Confirmed purchase | Brand conviction ("Tesla IS X") |
| **Re-collapse** | New document forces full recalculation | New evidence (scandal, product, campaign) forces conviction rebuild |
| **Observer** | The system (single, fixed weights) | Human cohort (heterogeneous, variable weights) |

### 4.2 The Critical Extension: Heterogeneous Observers

The financial pipeline has one observer: the system. Its weights are fixed (vendor .30, amount .40, date .20, location .15) — values hand-tuned during implementation to maximize reconciliation accuracy on a development dataset of approximately 500 transactions, then held constant across all subsequent processing. No formal sensitivity analysis was conducted; different datasets or business contexts would likely require recalibration. Every atom is processed through the same scoring function.

Brand perception has *many* observers, each with different weights. A Gen-Z consumer weights Social signals at .40 and Cultural at .30. A B2B buyer weights Economic at .40 and Experiential at .35. (These cohort labels are used here as shorthand for observers with characteristic weight patterns, not as demographic groupings.) Same signals, different weights, different clouds, different facts. Empirical evidence for this divergence across observer cohorts is documented in the spectral profile analysis reported in Zharnikov (2026e).

This is the critical extension that produces Spectral Brand Theory. The seven principles transfer with parametric extension: the pipeline stages are identical, but the single-observer assumption is replaced by a heterogeneous-observer model where each cohort has its own spectral profile — spectrum, weights, tolerances, and priors — that determines how they process the same signal environment.

The result: the same brand produces different "facts" in different observers' minds. These are not errors or variations on a "true" brand perception — they are the brand perceptions that the architecture can recover from the available signal environment. There is no brand-in-itself accessible outside some observing system, just as there is no "true reconciliation" independent of the matching algorithm's parameters. The parameters determine the output.

### 4.3 Principle Transfer Validation

Each of the seven principles operates identically in both domains:

**Dimensional typing** (Principle 1): Brand signals are typed by dimension. A logo is a semiotic signal. A price is an economic signal. A product experience is an experiential signal. Signals are compared within dimensions, not across them.

**Source binding** (Principle 2): Each brand signal originates from one encounter type. A social media impression is one source. A store visit is another. The same underlying brand attribute might generate atoms in both encounters, but the atoms are source-bound — the store visit atom and the Instagram atom are separate observations even if they describe the same product.

**Identity gate** (Principle 3): The observer must recognize the brand before any perception forms. Logo, name, visual identity serve this gate function. Without passing the gate, brand signals are noise — the observer does not cluster them because they do not recognize them as belonging to a single entity.

**Asymmetric tolerances** (Principle 4): Different observer cohorts have different tolerance for inconsistency. A brand employee has zero tolerance for ideological contradiction (they live inside the brand). A casual consumer has high tolerance for cultural inconsistency (they do not care about aesthetics). The tolerance is a property of the observer-dimension interaction, not the dimension alone.

**Weighted scoring** (Principle 5): This is the core mechanism of Spectral Brand Theory. Each observer cohort has a weight profile that determines how they cluster brand signals. The weights produce different perception clouds from the same signal set.

**Re-collapse** (Principle 6): A brand scandal introduces new signals that force conviction rebuild. The observer does not "update" their brand conviction — they dissolve it and re-form from the available evidence: the signals that have survived temporal decay plus crystallized priors, now including the new contradicting signals. This explains both brand resilience (strong convictions resist moderate contradicting evidence) and brand crises (overwhelming contradicting evidence forces wholesale re-evaluation).

**Epistemic separation** (Principle 7): Brand signals (atoms), brand impressions (clouds), and brand convictions (facts) are structurally distinct. A brand signal is not "the brand" — it is one observation. A brand impression is not a conviction — it is a probabilistic cluster. A brand conviction is not permanent — it can be dissolved and rebuilt.

---

## 5. Theoretical Propositions

The architecture and its cross-domain transfer support four theoretical propositions. Each is derived from the structural properties established in Sections 2–4 and is stated in a form that admits empirical testing.

**Proposition 1: External corroboration structurally reduces confirmation bias in brand assessment.**

The atom-cloud-fact pipeline requires that any fact be built from atoms drawn from multiple independent source types. A brand conviction cannot crystallize from a single encounter type — the cloud's weighted score integrates evidence across sources before any fact collapse occurs. This structural requirement means that conclusions which would be reached from any single source alone (a single focus group, a single social media dataset, a single competitor report) are necessarily subordinated to the multi-source cloud before becoming knowledge. Because confirmation bias operates by selectively attending to evidence that supports a prior belief (Nickerson, 1998), and because the pipeline's identity gate and weighted scoring require convergent evidence *across* independently typed sources rather than within a single preferred source, the architecture is structurally less susceptible to confirmation bias than single-source brand assessment methods. This proposition is testable: brand assessments produced through the pipeline should show lower intra-analyst agreement when consultants bring strong priors, compared to assessments produced through single-source analysis where prior-confirming evidence can be over-weighted without structural constraint.

*Falsification:* P1 is falsified if a controlled experiment shows no significant difference in confirmation-bias indicators (operationalized as prior-consistent over-weighting) between analysts using the pipeline and analysts using single-source methods, when analyst priors are experimentally manipulated and held constant across conditions.

**Proposition 2: Multi-model replication produces more robust brand assessments than single-model analysis.**

When the atom-cloud-fact pipeline is implemented through multiple large language models processing the same signal set independently, conclusions that appear in all model outputs are structurally more robust than conclusions that appear in only some. This follows from the pipeline's source-binding principle (Principle 2): atoms are source-bound, and different models constitute different observation sources. A conclusion that survives across models has been independently derived from the same signal set by observers with different internal architectures — it is, in the pipeline's terms, a high-confidence cloud approaching collapse. A conclusion that appears in only one model's output is an unconfirmed cloud: the evidence may be real or it may be a model-specific artifact. This proposition is testable: for any given brand, conclusions coded as appearing across multiple model outputs should demonstrate higher retest reliability (consistency across separate analytical sessions) than model-specific conclusions.

*Falsification:* P2 is falsified if cross-model agreement on structural features (dimension activation, coherence type) does not predict higher retest reliability than single-model conclusions in a pre-registered replication study — specifically, if model-specific conclusions show equal or greater stability across independent analytical sessions.

**Proposition 3: The three-stage epistemic separation prevents category errors that conflate brand signals, perception clouds, and brand convictions.**

Brand analysis methods that do not formally distinguish observation, hypothesis, and knowledge conflate three structurally distinct epistemic objects. A brand signal (that Tesla's advertising uses technical imagery) is an atom — typed, source-bound, immutable. A brand impression ("Tesla seems innovation-focused") is a cloud — probabilistic, multi-source, revisable. A brand conviction ("Tesla IS innovation") is a fact — threshold-crossed, stable, but subject to re-collapse. Conflating these objects produces specific analytical errors: treating signals as convictions (concluding that a single campaign has changed brand perception), treating clouds as facts (asserting that a probabilistic clustering constitutes established market knowledge), or treating convictions as permanent (failing to model how new signals force re-collapse). The pipeline's epistemic separation (Principle 7) prevents these errors by construction. This proposition is testable: brand analyses that lack formal stage separation should exhibit higher rates of the identified error types when subjected to structured coding review.

*Falsification:* P3 is falsified if a structured content analysis of published brand audits finds no significant difference in category-error frequency between reports that explicitly distinguish signals, clouds, and convictions and those that do not — when coded by independent raters blind to the coding hypothesis.

**Proposition 4: Cross-model disagreement is diagnostic of evidential ambiguity, not model failure.**

When multiple model implementations of the atom-cloud-fact pipeline disagree on a specific brand claim, that disagreement identifies a location in the evidence where the signal is genuinely ambiguous — a cloud that has not reached collapse threshold. This follows from the re-collapse principle (Principle 6): if sufficient unambiguous evidence existed, all model implementations would converge on the same fact because the evidence would be decisive. Disagreement implies that the available atoms do not suffice to push the cloud past threshold in all observers, which is precisely the definition of evidential ambiguity. This reframes cross-model disagreement from a quality problem (the models are inconsistent) to an analytical output (the evidence is insufficient to support this specific conviction). The diagnostic interpretation is testable: claims on which models disagree should correspond, when verified against primary evidence, to genuinely contested or ambiguous brand attributes — domains where consumer research itself produces inconsistent findings.

*Falsification:* P4 is falsified if cross-model disagreement locations, when mapped against independent consumer-survey data, do not show higher attribute-level ambiguity scores than cross-model agreement locations — that is, if disagreement is no more predictive of genuine evidential ambiguity than agreement.

---

## 6. Emergent Properties of the Transfer

The domain transfer does not merely replicate financial processing in a new vocabulary. Three properties emerge in the brand domain that were latent in the financial domain:

### 6.1 Observer Heterogeneity as a Feature

In financial processing, having multiple observers with different weights would be a bug — it would mean the system is inconsistent. In brand perception, observer heterogeneity is *the central feature*. The fact that different cohorts form different convictions from the same signal environment is not a system failure — it is the fundamental mechanism of how brands work. The pipeline architecture handles this naturally: each observer processes the same atoms through their own scoring function, producing their own clouds and facts.

### 6.2 Structural Absence

The financial pipeline assumes positive evidence: atoms are extracted from documents that exist. The brand domain introduces a phenomenon absent in the financial domain: *designed absence as a signal*. Hermès' strategy of deliberately restricting signal emission (no discounts, no online sales for core products, geographic scarcity) functions as a signal in the brand domain — the absence generates perception effects on dimensions other than the restricted one (Zharnikov, 2026a). This extends the atom model with a new emission type (structural absence) and a scarcity multiplier in the cloud formation formula.

### 6.3 Valence Asymmetry

Financial facts do not have valence — a confirmed purchase is neither good nor bad, it simply is. Brand convictions carry valence: positive, negative, or ambivalent. The domain transfer reveals a conjectured asymmetric property: negative convictions (built from ideological and social signals) may be more resilient than positive convictions (built from experiential and economic signals) because evidence-free negative convictions contain no contradicting dimensions that could introduce ambiguity (Zharnikov, 2026a). This conjecture is derived from the architecture's structural properties and remains to be tested against independent consumer data. The asymmetry is invisible in the financial domain, where all facts are valence-neutral.

---

## 7. Generalizability: Beyond Finance and Brands

The atom-cloud-fact pipeline is a candidate framework for any domain where heterogeneous observers perceive typed signals from multiple sources under uncertainty. Candidate domains include:

Table 4: Candidate Domains for the Atom-Cloud-Fact Architecture.

| Domain | Atoms | Observers | Cloud → Fact |
|--------|-------|-----------|-------------|
| **Political perception** | Policy signals, rhetoric, media coverage, personal encounters | Voter cohorts with different ideological profiles | Political impression → voting conviction |
| **Academic reputation** | Papers, citations, presentations, peer review, social media | Different academic communities (field, methodology, seniority) | Scholarly impression → reputation conviction |
| **Product evaluation** | Specs, reviews, demos, competitor comparisons, price | Consumer cohorts with different priority weights | Product impression → purchase conviction |
| **Medical diagnosis** | Symptoms, test results, patient history, imaging | Different specialists with different diagnostic weights | Diagnostic hypothesis → confirmed diagnosis |

The architecture's generalizability rests on a single structural condition: the domain must involve *typed observations from multiple sources that cluster under uncertainty into revisable knowledge*. Where this condition holds, the seven principles apply with parametric adaptation.

Among the candidate domains, three warrant near-term investigation as cross-domain replication tests. Medical diagnosis is the highest-priority case: heterogeneous specialists (radiologist, internist, pathologist) each weight symptoms across typed dimensions with different tolerances, and the re-collapse mechanism maps cleanly onto the clinical practice of revising diagnosis when new test results arrive. Legal evidence assessment is a second strong candidate: jurors and judges constitute heterogeneous observers weighting typed evidence — physical, testimonial, documentary — under formal epistemic-separation requirements that parallel the pipeline's own structure. Intelligence analysis is a third: the intelligence community's tradecraft explicitly distinguishes raw intelligence (atoms), working hypotheses (clouds), and finished assessments (facts), with full re-evaluation mandated when contradicting source material surfaces. Independent application of the pipeline in any of these domains, by researchers not affiliated with SBT, would provide the strongest test of the architecture's cross-domain transferability claim.

---

### 7.1 Limitations

Both the financial reconciliation architecture and SBT were developed by the same author, making the cross-domain transfer self-confirming. Independent replication of the atom-cloud-fact architecture in a domain not developed by this author would provide stronger evidence of transferability. Each candidate domain listed in the Generalizability section has its own mature computational literature; structural analogy to the atom-cloud-fact pipeline does not imply novelty relative to domain-specific approaches. The conditions under which multi-model LLM replication constitutes structural evidence — and where it does not — are examined in the following subsection.

---

### 7.2 Convergent Validity of Multi-Model Replication

Proposition P2 rests on the claim that agreement across multiple LLM implementations provides evidence of structural robustness. This claim requires qualification. LLM agreement is not equivalent to independent replication in the experimental sense. Four conditions determine whether cross-model convergence constitutes genuine structural evidence rather than correlated artifact.

**Condition 1: Different training data distributions.** Independent replication requires that observers draw on distinct evidence bases. This condition is partially satisfied across the models used in SBT analysis (Claude, Gemini, GPT-4): while all three draw from large internet text corpora, they differ in corpus construction, data vintages, filtering procedures, and proprietary supplementary data. The overlap is substantial but non-identical. This partial independence is weaker than the full independence of human subject experiments but stronger than single-model sensitivity analysis. Convergence across models with partially distinct corpora is better described as *quasi-independent replication* than as either full independence or redundancy.

**Condition 2: Different architectures.** This condition is more fully satisfied. Claude, Gemini, and GPT-4 instantiate transformer architectures trained with different objectives, different RLHF procedures, and different fine-tuning regimes. The differences in attention mechanisms, training objectives, and alignment procedures mean that model-specific artifacts — idiosyncratic tendencies in how each system parses qualitative evidence — are unlikely to align across all three unless the underlying signal is genuine. Architectural diversity provides the strongest available basis for treating multi-model agreement as structurally meaningful.

**Condition 3: Agreement on structural features, not numerical values.** The evidential weight of convergence depends critically on what the models agree about. Agreement on structural features — which dimensions are diagnostically active, which coherence type applies, whether cloud formation is stalled or progressing — is more robust than agreement on numerical values such as specific dimension scores or percentage estimates. Numerical outputs are sensitive to prompt framing, output format instructions, and scale anchoring. Structural classifications are more stable because they reflect the categorical organization of the evidence rather than its precise quantitative representation. The SBT analytical pipeline treats structural agreement as the primary validity criterion; numerical outputs are indicative and require human validation.

**Condition 4: Stability across prompt variations.** Genuine structural features should be recoverable through multiple prompt formulations. Zharnikov (2026a) reports a sensitivity analysis in which five prompt reformulations of the same brand profile analysis produced stable structural classifications (dimension identification, coherence type) while producing variable numerical scores. This asymmetry — structural stability with numerical variability — is the expected signature of a real architectural feature: the underlying signal exists, but its precise quantification is underdetermined by the available evidence.

One systematic source of correlated bias must be acknowledged. All major LLM training corpora overrepresent Western, English-language consumer brand discourse. Brands such as Hermès, IKEA, and Tesla receive extensive coverage in the training data, which means that convergent multi-model analysis of these brands may partly reflect shared training signal rather than independent structural inference. This bias is most severe for globally prominent brands with high media coverage; it is less severe for brands with limited international English-language discourse. Independent human-subject validation is the definitive test precisely because human observers are not trained on the same corpus as LLMs.

The overall assessment is that LLM agreement is *necessary but not sufficient* for structural validity. Convergence across architecturally distinct models on structural features across multiple prompt reformulations raises the prior that the identified features are real. It does not confirm them. Human-subject validation — presenting actual observers with brand stimuli and measuring whether their spectral profiles converge on the LLM-identified structure — is the required confirmatory test. Argyle et al. (2023) demonstrate that LLMs can simulate human population distributions on attitudinal surveys with reasonable fidelity, but also identify systematic divergences tied to training corpus composition — precisely the shared Western bias identified above. Their framework for evaluating LLM-as-simulacrum validity provides a methodological template for the human-subject validation studies proposed here.

---

## 8. Discussion: Why Existing Frameworks Fail the Multi-Domain Requirement

Four requirements define a framework adequate for the multi-domain knowledge-formation problem addressed here: (1) path-independence — conclusions must not depend on the order in which evidence arrives; (2) observer heterogeneity — the framework must natively model multiple observers with different scoring weights; (3) epistemic separation — observations, hypotheses, and knowledge must be structurally distinct objects; and (4) linguistic implementability — the framework must be expressible as natural language instructions for an LLM without requiring formal probability distributions or rule bases. We argue that each major existing approach fails at least one of these requirements structurally — not through poor design but through fundamental architectural choices that make the requirement incompatible with the framework's core commitments.

### 8.1 Bayesian Reasoning and AGM Revision

The atom-cloud-fact pipeline shares structural similarities with Bayesian reasoning — particularly as formalized in probabilistic networks (Pearl, 1988): both update beliefs based on new evidence. However, Bayesian reasoning fails requirement (1) structurally. Bayesian updating is incremental — prior beliefs are updated by multiplying with likelihood ratios. This means the order in which evidence arrives permanently shapes the posterior: a prior formed from early evidence filters all subsequent evidence through the lens that early evidence established. The atom-cloud-fact pipeline is *non-incremental*: on re-collapse, facts are dissolved and rebuilt from the complete evidence set. The result is always consistent with total evidence regardless of arrival order. This is not a refinement of Bayesian updating — it is an architectural rejection of incremental updating as the appropriate mechanism for domains where early evidence should not permanently privilege itself over later evidence.

The pipeline also differs from Dempster-Shafer evidence theory (Dempster, 1967; Shafer, 1976), which combines evidence through belief functions that handle ignorance explicitly. Dempster-Shafer fails requirement (3): it does not distinguish between observation, hypothesis, and confirmed knowledge as structurally separate objects — all evidence states are represented in the same belief-function formalism. The atom-cloud-fact pipeline does not model degrees of ignorance — it models degrees of match through weighted scoring, with ignorance represented implicitly as missing atoms rather than explicit uncertainty intervals.

AGM belief revision theory (Alchourrón, Gärdenfors, & Makinson, 1985) also fails requirement (1), for a different structural reason. AGM defines revision as operations on logically closed belief sets. Its core commitment — the principle of minimal change — requires the system to preserve as much of the prior belief set as possible when new evidence arrives. This commitment structurally privileges prior beliefs: the system actively works to retain them. The atom-cloud-fact pipeline rejects this commitment entirely. On re-collapse, nothing is preserved. Facts are dissolved and rebuilt from the complete atom set. The new evidence may change the entire interpretation of the data; minimal-change revision cannot handle this because it assumes the prior interpretation is substantially correct and needs only localized adjustment.

The distinction matters in practice. Bayesian updating can accumulate path-dependent biases — the order in which evidence arrives affects the posterior, even when it should not. The atom-cloud-fact pipeline addresses this through re-collapse: when new evidence arrives, facts are dissolved and rebuilt from the complete available evidence set rather than incrementally updated. This re-collapse mechanism resonates with Popper's (1959) falsificationism — existing knowledge is discarded when contradicted, not defended — and with Quine's (1951) holism, which argues that no individual belief can be evaluated in isolation from the total web of beliefs. The pipeline operationalizes Quine's insight: re-collapse rebuilds from the *total* atom set because any single atom might change the interpretation of all others. It also parallels Kuhn's (1962) account of paradigm shifts: when accumulated anomalies exceed the existing framework's capacity to accommodate them, the framework is not patched but replaced wholesale.

However, the pipeline's path-independence properties differ across domains because signal persistence is domain-specific. In financial reconciliation, atoms are permanent — an invoice discovered in January is as evidentially valid in December as on the day of discovery. The complete atom set is always available for re-collapse, making the pipeline genuinely path-independent: the order of document discovery does not and should not affect which transactions are confirmed.

In brand perception, atoms *decay*. A shop visit from five years ago contributes less to current cloud formation than a visit from yesterday — not because the pipeline discards it, but because human memory attenuates signal luminosity over time. Signals that were emotionally intense or sufficiently reinforced may crystallize into permanent priors, but routine encounters fade. The "available evidence set" at any moment of re-collapse is therefore not the complete historical set but the set of signals that have survived temporal decay plus whatever has crystallized. This makes brand perception path-dependent: the order and timing of encounters matter because they determine which signals are still luminous when re-collapse occurs. Peters (2019) identifies this property — multiplicative, path-dependent dynamics where sequence determines outcome — as the formal definition of non-ergodicity.

The pipeline architecture is the same in both domains. The difference is in the atoms: financial atoms persist; perceptual atoms decay. The architecture transfers across domains; signal persistence behavior is domain-specific.

The path-independence argument also benefits from Pearl's (2009) causal modeling framework, which identifies the conditions under which evidence-ordering effects propagate through probabilistic networks — conditions that the re-collapse mechanism is specifically designed to break by dissolving the accumulated posterior on each rebuild. Levi's (1991) theory of epistemic entrenchment similarly addresses when prior commitments should be abandoned entirely rather than minimally revised; the re-collapse principle can be read as operationalizing Levi's "full contraction" rather than his "partial contraction" — a wholesale rollback to the atom level, not a selective withdrawal of beliefs.

The architecture's behavior at extreme weight settings remains to be characterized. The financial weights (.30, .40, .20, .15) were hand-tuned on a single development dataset of approximately 500 transactions; their sensitivity to domain shifts, dataset characteristics, or adversarial inputs is unknown. This calibration uncertainty applies to the brand-domain weights as well, where cohort-level spectral profiles represent characteristic weight patterns rather than empirically validated parameters. Future work should characterize weight sensitivity through structured perturbation studies.

### 8.2 Symbolic vs. Probabilistic Reasoning

Classical expert systems (Buchanan & Shortliffe, 1984) fail requirement (2) structurally. Expert systems operate in the symbolic regime: deterministic rules transform structured inputs into conclusions. This architecture cannot accommodate observer heterogeneity because the rules are global — the same rule fires for all observers regardless of their weight profiles. There is no mechanism by which two observers processing the same inputs through the same rule base arrive at different conclusions, yet that is precisely what observer heterogeneity requires. Introducing observer-specific rules produces rule-set combinatorial explosion and destroys the interpretability that makes expert systems useful.

Purely statistical models fail requirement (3) in the opposite direction: they operate in the probabilistic regime (numerical functions mapping features to predictions) without structural separation between observation types. A regression model treats all input variables as epistemically equivalent — there is no built-in distinction between atomic observations, probabilistic hypotheses, and confirmed knowledge. The model produces a prediction, but the epistemic status of the inputs — are they observations, priors, hypotheses? — is not architecturally tracked.

The atom-cloud-fact pipeline resolves both failures through its hybrid structure. Atoms are symbolic — typed, named, structured, drawing on the representational traditions formalized by Enderton (2001) in mathematical logic and Sowa (2000) in knowledge representation. Clouds are probabilistic — scored, uncertain, revisable. Facts are quasi-symbolic — confirmed, stable, but subject to dissolution. This combination produces results that are both interpretable (every atom contributing to every fact is traceable) and uncertainty-aware (clouds that have not reached collapse threshold remain visible as unresolved hypotheses). The collapsed fact also contains a form of tacit knowledge (Polanyi, 1966): the fact "knows" more than its constituent atoms because the cloud formation process integrated contextual relationships — tolerances, temporal proximity, source interactions — that are not explicitly stored in the fact itself.

### 8.3 LLM Implementability

A distinctive property of the atom-cloud-fact pipeline is that it can be implemented through natural language instructions to a large language model, without custom code. The seven principles can be expressed as a system prompt: "Extract typed signals across these dimensions. Cluster them using these weights. Identify when the evidence threshold is met. Rebuild from scratch when new evidence contradicts existing conclusions."

This is not trivially possible with other epistemological frameworks. Bayesian networks require explicit probability distributions. Expert systems require formal rule bases. The classical AI approach — symbolic reasoning with logical inference (Russell & Norvig, 2020) — requires formalized knowledge bases. The atom-cloud-fact pipeline's principles are expressible in natural language because they describe *cognitive operations* (perceive, cluster, weigh, decide, revise) rather than *mathematical operations* (multiply, integrate, optimize). LLMs, trained on text describing human reasoning, can execute cognitive operations with surprising fidelity.

The SBT implementation demonstrates this: the seven-module analytical pipeline operates entirely as a structured prompt sequence, producing formal multi-cohort brand analysis through natural language instruction rather than code execution (Zharnikov 2026a; Zharnikov 2026t). This suggests that the atom-cloud-fact architecture is not merely computationally implementable but *linguistically implementable* — a property that may prove important as LLMs become the primary computational platform for analytical work. The claim is bounded, however: linguistic implementability has been validated in the brand perception domain with specific LLM families; systematic ablation studies across prompt reformulations and model generations are needed before the property can be asserted as general.

### 8.4 Comparative Requirements Matrix

The four requirements and five architectures are summarized in Table 5.

Table 5: Four-Requirement × Five-Architecture Comparison.

| Architecture | Path-independence | Observer heterogeneity | Epistemic separation | Linguistic implementability |
|---|---|---|---|---|
| **Bayesian (Pearl)** | FAIL — incremental updating permanently encodes evidence-arrival order in the posterior | FAIL — standard formulation assumes a single agent with fixed priors; multi-agent extensions require custom modifications | PARTIAL — beliefs are distinct from likelihoods, but observation and hypothesis share the same probability-space representation | FAIL — requires explicit probability distributions and likelihood specifications not expressible in plain language |
| **AGM (Alchourrón et al.)** | FAIL — minimal-change principle actively preserves prior belief sets, making revision order-dependent | FAIL — designed for a single rational agent; no native mechanism for heterogeneous-weight observers | PARTIAL — distinguishes belief sets from revision operators, but observation is not a first-class object; all inputs collapse to belief-set membership | FAIL — requires formal logic operations (contraction, revision, expansion) over logically closed sets |
| **Dempster-Shafer** | PARTIAL — combination rule is commutative (order of combination does not matter), but iterative updating across time steps is path-sensitive | FAIL — belief functions are defined for a single evidential frame; multi-observer extension requires separate frames with no native aggregation mechanism | FAIL — all evidence states (raw observation, hypothesis, confirmed belief) are represented in the same belief-function formalism; no structural distinction | FAIL — requires formal specification of basic probability assignments and the Dempster combination rule |
| **MYCIN / expert systems** | PASS — rule firings are order-independent given the same input state | FAIL — rules are global; same rule fires for all observers regardless of weight profiles; observer-specific rules produce combinatorial explosion | PARTIAL — production rules distinguish input conditions from output conclusions, but no formal atom/cloud/fact separation; working memory conflates observation types | PARTIAL — rules can be expressed in English-like syntax, but linguistic implementability in an LLM requires formal rule-base compilation, not natural-language instruction |
| **Atom-Cloud-Fact (this paper)** | PASS — re-collapse dissolves facts and rebuilds from complete atom set; arrival order has no residual effect | PASS — each observer cohort applies its own weight profile to the same atom set; heterogeneity is native to the architecture | PASS — atoms, clouds, and facts are structurally separate objects with separate interfaces; no promotion/demotion shortcuts permitted | PASS — all seven principles are expressible as natural-language cognitive operations executable by an LLM system prompt |

*Notes*: PASS = requirement met by core architecture. PARTIAL = partially addressed with qualifications. FAIL = structural incompatibility. AGM = Alchourrón, Gärdenfors & Makinson (1985). MYCIN = Buchanan & Shortliffe (1984).

---

## 9. Conclusion

The atom-cloud-fact pipeline is not a technique for financial document processing. It is an epistemological architecture — a formal model of how knowledge forms from heterogeneous observation. The financial domain provided the implementation context. The brand perception domain provided the demonstration through transfer. The architecture's seven principles — dimensional typing, source binding, identity gating, asymmetric tolerances, weighted scoring, re-collapse, and epistemic separation — capture general properties of observation-to-knowledge progression that are not domain-specific.

This paper develops four theoretical propositions with testable implications. P1 argues that the pipeline's external-corroboration requirement structurally reduces confirmation bias relative to single-source methods. P2 argues that multi-model replication identifies robust conclusions by treating model outputs as independent observer instances subject to Principle 2. P3 argues that the three-stage epistemic separation prevents specific category errors — treating signals as convictions, clouds as facts, or facts as permanent — that characterize analyses without formal stage separation. P4 argues that cross-model disagreement is diagnostic evidence of genuine evidential ambiguity, not analyst inconsistency. Each proposition is testable through structured comparison studies using coded brand analyses.

The framework also argues against existing alternatives: Bayesian updating and AGM revision fail the path-independence requirement through architectural commitments to incremental updating and minimal change respectively; classical expert systems fail the observer-heterogeneity requirement through their global rule architecture; purely probabilistic models fail the epistemic-separation requirement by conflating observation and inference; and all three fail the linguistic-implementability requirement to varying degrees.

Future empirical work should test P1 through controlled analyst studies comparing confirmation-bias indicators across single-source and pipeline-based assessments; P2 through retest reliability comparisons of single-model vs. multi-model brand conclusions; P3 through coded review of published brand audits for category-error frequency; and P4 through correlation of cross-model disagreement locations with independent measures of brand-attribute ambiguity in consumer research. Cross-domain replication — applying the pipeline in medical diagnosis, legal evidence assessment, or intelligence analysis, as proposed in the Generalizability section — would provide the strongest test of the cross-domain transferability claim.

The architecture is computationally implementable. The financial implementation processes real documents. The brand perception implementation operates as a structured prompt sequence for large language models. Both share the same seven principles and the same three-stage pipeline. The code is different. The epistemological structure — dimensional typing, source binding, identity gating, asymmetric tolerances, weighted scoring, re-collapse, and epistemic separation — holds across both implementations; whether it holds across additional domains remains an empirical question the four propositions are designed to open.

---

## Author Note

Dmitry Zharnikov is an independent researcher and strategist. He holds a Professional MBA (Entrepreneurship & Innovation) from Technische Universitat Wien and Wirtschaftsuniversitat Wien (dual degree, 2018). ORCID: https://orcid.org/0009-0000-6893-9231

---

## References

Alchourrón, C. E., Gärdenfors, P., & Makinson, D. (1985). On the logic of theory change: Partial meet contraction and revision functions. *The Journal of Symbolic Logic*, 50(2), 510–530.

Argyle, L. P., Busby, E. C., Fulda, N., Gubler, J. R., Rytting, C., & Wingate, D. (2023). Out of one, many: Using language models to simulate human samples. *Political Analysis*, 31(3), 337–351. https://doi.org/10.1017/pan.2023.2

Buchanan, B. G., & Shortliffe, E. H. (1984). *Rule-based expert systems: The MYCIN experiments of the Stanford Heuristic Programming Project*. Addison-Wesley.

Christen, P. (2012). *Data matching: Concepts and techniques for record linkage, entity resolution, and duplicate detection*. Springer.

Dempster, A. P. (1967). Upper and lower probabilities induced by a multivalued mapping. *The Annals of Mathematical Statistics*, 38(2), 325–339. https://doi.org/10.1214/aoms/1177698950

Enderton, H. B. (2001). *A mathematical introduction to logic* (2nd ed.). Academic Press.

Fellegi, I. P., & Sunter, A. B. (1969). A theory for record linkage. *Journal of the American Statistical Association*, 64(328), 1183–1210.

Goldman, A. I. (1986). *Epistemology and cognition*. Harvard University Press.

Gregor, S., & Jones, D. (2007). The anatomy of a design theory. *Journal of the Association for Information Systems*, 8(5), 312–335.

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly*, 28(1), 75–105.

Kahneman, D. (2011). *Thinking, fast and slow*. Farrar, Straus and Giroux.

Koffka, K. (1935). *Principles of Gestalt psychology*. Harcourt, Brace.

Kuhn, T. S. (1962). *The structure of scientific revolutions*. University of Chicago Press.

Levi, I. (1991). *The fixation of belief and its undoing: Changing beliefs through inquiry*. Cambridge University Press.

Nickerson, R. S. (1998). Confirmation bias: A ubiquitous phenomenon in many guises. *Review of General Psychology*, 2(2), 175–220. https://doi.org/10.1037/1089-2680.2.2.175

Pearl, J. (1988). *Probabilistic reasoning in intelligent systems: Networks of plausible inference*. Morgan Kaufmann.

Pearl, J. (2009). *Causality: Models, reasoning, and inference* (2nd ed.). Cambridge University Press.

Peirce, C. S. (1931–1958). *Collected papers of Charles Sanders Peirce* (C. Hartshorne & P. Weiss, Eds., Vols. 1–6). Harvard University Press.

Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, 15, 1216–1221. https://doi.org/10.1038/s41567-019-0732-0

Polanyi, M. (1966). *The tacit dimension*. Doubleday.

Popper, K. R. (1959). *The logic of scientific discovery*. Hutchinson.

Quine, W. V. O. (1951). Two dogmas of empiricism. *The Philosophical Review*, 60(1), 20–43.

Russell, S., & Norvig, P. (2020). *Artificial intelligence: A modern approach* (4th ed.). Pearson.

Shafer, G. (1976). *A mathematical theory of evidence*. Princeton University Press.

Sowa, J. F. (2000). *Knowledge representation: Logical, philosophical, and computational foundations*. Brooks/Cole.

Zadeh, L. A. (1965). Fuzzy sets. *Information and Control*, 8(3), 338–353.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026e). Spectral Brand Theory: Observer heterogeneity and cohort divergence in multi-dimensional brand perception. Working Paper.

Zharnikov, D. (2026t). Spectral Brand Theory: Linguistic implementability and LLM-based analytical pipelines. Working Paper.

---
*This paper is part of the Spectral Brand Theory research program. For the full atlas of 20+ interconnected papers, see [spectralbranding.com/atlas](https://spectralbranding.com/atlas).*

