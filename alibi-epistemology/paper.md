# The Atom-Cloud-Fact Epistemological Pipeline: From Financial Document Processing to Brand Perception Modeling

**Dmitry Zharnikov**

Working Paper — February 2026

*Contact: dmitry@spectralbranding.com*

| | |
|---|---|
| **Applied framework** | [github.com/spectralbranding/sbt-framework](https://github.com/spectralbranding/sbt-framework) |
| **SBT paper** | [spectral-brand-theory/paper.md](../spectral-brand-theory/paper.md) |
| **License** | MIT |

---

## Abstract

This paper describes a domain-agnostic epistemological architecture — the atom-cloud-fact pipeline — that models the progression from observation to knowledge through three formally specified stages: atomic observation (typed, source-bound data extraction), probabilistic cloud formation (weighted multi-dimensional clustering), and fact collapse (threshold-based knowledge crystallization with full re-collapse on new evidence). The architecture was originally developed for automated financial document processing, where receipts, invoices, and bank statements must be reconciled into confirmed purchase facts despite incomplete, contradictory, and multi-source evidence. We document the architecture's seven core principles, demonstrate its implementation in financial fact extraction, and show how the same principles transfer without modification to an entirely different domain: brand perception modeling. The domain transfer produces Spectral Brand Theory (SBT), a computational framework for multi-dimensional brand analysis that models brands as signal sources and audiences as spectral observers — each assembling a different "brand" from the same signal environment. The successful transfer suggests the atom-cloud-fact pipeline captures a general structure of how knowledge forms from heterogeneous observations, not a domain-specific technique.

**Keywords:** epistemology, probabilistic knowledge, observation pipeline, domain transfer, computational framework

---

## 1. Introduction

How does knowledge form from observation? The question is ancient. The computational answer is surprisingly recent — and surprisingly underdeveloped.

In most software systems, "knowledge" is an input, not an output. A database stores facts that humans have already determined. A search engine retrieves documents that humans have already written. A machine learning classifier assigns labels that humans have already defined. The system manipulates knowledge; it does not *form* it.

But certain computational problems require the system to form knowledge from raw observations — to progress from "I see data point X" through "I hypothesize that X and Y belong together" to "I know that X and Y describe the same real-world event." This progression — observation to hypothesis to knowledge — has a structure. This paper describes that structure.

The atom-cloud-fact pipeline was developed for a specific problem: reconciling financial documents. A business generates receipts, invoices, bank statements, and payment confirmations. These documents describe the same underlying transactions — but differently. A receipt shows line items and a total. A bank statement shows a date and amount. An invoice shows a vendor and terms. The system must extract observations from each document, cluster observations that likely describe the same transaction, and determine when sufficient evidence exists to confirm that a specific purchase occurred.

The solution required three epistemological stages with formally distinct properties: observations that are typed and source-bound (atoms), hypotheses that are probabilistic and revisable (clouds), and knowledge that is threshold-based and subject to full recalculation (facts). Seven architectural principles emerged from the implementation, governing how observations are typed, how they cluster, and how knowledge crystallizes and re-crystallizes.

The unexpected finding was that these principles are not specific to financial documents. When applied to brand perception modeling — a domain with no obvious connection to receipt reconciliation — the same architecture produces a framework (Spectral Brand Theory) that generates novel analytical capabilities unavailable through existing brand frameworks (Zharnikov, 2026a). The domain transfer works because the underlying epistemic structure is identical: heterogeneous observers perceive typed signals, cluster them into probabilistic impressions, and — if sufficient evidence accumulates — crystallize those impressions into stable convictions.

This paper documents the architecture, its principles, the original financial implementation, and the domain transfer to brand perception. It argues that the atom-cloud-fact pipeline captures a general pattern of knowledge formation from heterogeneous observation — applicable wherever multiple observers perceive typed signals from multiple sources under uncertainty.

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
- Dimensional               - Weighted                  - Observer-specific*
```

*Observer-specificity applies in the brand perception domain. In the financial domain, the system is the sole observer with fixed weights.

**Stage 1: Atomic Observation.** Raw data is extracted from source documents and decomposed into typed atoms. Each atom belongs to exactly one dimension (vendor, amount, date, etc.) and exactly one source document. Atoms are immutable — once extracted, they do not change. They are the ground truth of what was observed.

**Stage 2: Cloud Formation.** Atoms from different sources cluster into probabilistic hypothesis clouds. A cloud represents "these atoms probably describe the same real-world event." Clouds are scored through weighted multi-dimensional comparison. They are inherently uncertain and continuously revisable as new atoms arrive.

**Stage 3: Fact Collapse.** When a cloud's score exceeds a threshold, it collapses into a fact — confirmed knowledge. Facts are not permanent: when new evidence arrives that contradicts an existing fact, the fact dissolves and the system rebuilds from the full atom set. This re-collapse mechanism ensures that knowledge is always consistent with the total evidence, not incrementally patched.

### 2.2 Seven Architectural Principles

Seven principles govern the pipeline's operation. Each was discovered through the financial implementation but proves to be domain-agnostic:

| # | Principle | Definition | Financial Implementation |
|---|-----------|-----------|------------------------|
| 1 | Dimensional typing | Observations belong to typed dimensions | 6 atom types: VENDOR, ITEM, PAYMENT, DATETIME, AMOUNT, TAX |
| 2 | Source binding | Each observation belongs to exactly one source | Atoms belong to exactly one document |
| 3 | Identity gate | Core identity match is a precondition for clustering | Vendor name must match before any other comparison |
| 4 | Asymmetric tolerances | Context determines what "close enough" means | Receipt + statement: 5-day tolerance; invoice + payment: 60 days |
| 5 | Weighted multi-dimensional scoring | Not all dimensions contribute equally | Vendor 0.30, amount 0.40, date 0.20, items 0.50 bonus |
| 6 | Re-collapse on new evidence | Knowledge is rebuilt from scratch, never patched | Facts recalculated from full atom set on any change |
| 7 | Epistemic separation | Observations, hypotheses, and knowledge are structurally distinct | Atoms, clouds, and facts stored and processed separately |

**Table 1.** Seven principles of the atom-cloud-fact architecture.

**Principle 1: Dimensional typing** ensures that observations are categorized before comparison. Two atoms can only be compared if they share a dimension. A vendor name does not "match" a price — they exist on different dimensions. This prevents false correlations and enables dimension-specific scoring.

**Principle 2: Source binding** ensures that no observation claims to have been made from two sources simultaneously. This prevents circular evidence: a receipt atom cannot corroborate itself by appearing in two clouds. Each atom is evidence from one source, period.

**Principle 3: Identity gate** is the most architecturally significant principle. Before any multi-dimensional comparison occurs, the system must determine: do these atoms describe the same entity? In financial processing, the vendor gate answers: are these two documents about the same merchant? If the gate fails, no further comparison is attempted — the atoms are noise to each other regardless of how well other dimensions align. The identity gate is a binary precondition, not a weighted score.

**Principle 4: Asymmetric tolerances** acknowledge that "close enough" is context-dependent. A receipt and a bank statement for the same purchase might have different dates (the bank processes the charge days later). But an invoice and its payment might be separated by months. The tolerance is not a property of the dimension — it is a property of the source-pair interaction.

**Principle 5: Weighted multi-dimensional scoring** reflects the empirical reality that some dimensions are more diagnostic than others. An amount match is stronger evidence than a date match (many transactions happen on the same day; fewer share the same amount). The weights are calibrated to the domain.

**Principle 6: Re-collapse** is the principle that most strongly distinguishes this architecture from incremental systems. When new evidence arrives, the system does not update the existing fact — it dissolves the fact and rebuilds from the complete atom set. This is computationally expensive but epistemically correct: the new evidence may change the entire interpretation of the data, not just append to it. A newly discovered receipt might reassign atoms from one cloud to another, changing which facts exist. Incremental update cannot handle this; full recalculation can.

**Principle 7: Epistemic separation** requires that atoms, clouds, and facts are stored and processed in separate systems with separate interfaces. An atom cannot be "promoted" to a fact — it must pass through cloud formation and collapse. A fact cannot be "demoted" to a cloud — it must be dissolved and the atoms re-clustered. This separation prevents epistemic shortcuts that would compromise the pipeline's integrity.

---

## 3. Financial Implementation

### 3.1 The Reconciliation Problem

A typical business generates four document types for a single transaction: a receipt (from the vendor), an invoice (from the vendor), a bank statement (from the financial institution), and a payment confirmation (from the payment processor). These documents contain overlapping but non-identical information:

| Document | Atoms Extracted | Typical Dimensions |
|----------|-----------------|-------------------|
| Receipt | Vendor, items, amounts, tax, date, payment method | VENDOR, ITEM, AMOUNT, TAX, DATETIME, PAYMENT |
| Invoice | Vendor, items, amounts, terms, invoice number | VENDOR, ITEM, AMOUNT, DATETIME |
| Bank statement | Merchant name, amount, date, reference | VENDOR, AMOUNT, DATETIME |
| Payment confirmation | Vendor, amount, date, transaction ID | VENDOR, AMOUNT, DATETIME, PAYMENT |

**Table 2.** Document types and their atom dimensions in financial processing.

The challenge: the same transaction appears in different documents with different representations. The receipt says "STARBUCKS #12345" while the bank statement says "SQ *STARBUCKS CORP." The receipt date is March 15; the bank posts on March 17. The receipt shows $4.95; the bank shows $5.20 (tip added). The atoms describe the same real-world event but differ on every dimension.

### 3.2 Pipeline in Action

**Atom extraction**: Each document is parsed into typed atoms. The receipt yields: VENDOR("STARBUCKS #12345"), AMOUNT($4.95), DATETIME(2026-03-15), ITEM("Tall Latte"), PAYMENT("Visa ...4821"). The bank statement yields: VENDOR("SQ *STARBUCKS CORP"), AMOUNT($5.20), DATETIME(2026-03-17).

**Identity gate**: The vendor atoms are compared through fuzzy matching. "STARBUCKS #12345" and "SQ *STARBUCKS CORP" pass the gate (both resolve to the Starbucks canonical entity). Without this gate pass, the atoms would never cluster.

**Cloud formation**: The atoms cluster into a cloud with the following scores: vendor match 0.85 (high confidence after canonical resolution), amount match 0.70 (close but not exact — the tip explains the difference), date match 0.80 (2-day gap within the 5-day tolerance for receipt-statement pairs). Weighted score: 0.30(0.85) + 0.40(0.70) + 0.20(0.80) = 0.255 + 0.280 + 0.160 = 0.695.

**Collapse**: The threshold for receipt-statement reconciliation is 0.60. The cloud score (0.695) exceeds the threshold. The cloud collapses into a fact: "Confirmed purchase at Starbucks, March 15, $5.20 (receipt $4.95 + tip)."

**Re-collapse trigger**: If a second receipt arrives for the same Starbucks on the same day (a colleague's lunch), the system dissolves the fact and recalculates. The new atom set might produce two clouds where there was one, splitting the bank charge differently. The fact is not patched — it is rebuilt from scratch.

---

## 4. Domain Transfer: From Financial Facts to Brand Perception

### 4.1 The Mapping

The domain transfer from financial processing to brand perception preserves all seven principles while changing the domain vocabulary:

| Concept | Financial Domain | Brand Perception Domain |
|---------|-----------------|----------------------|
| **Atom** | Data point from a document (vendor, amount, date) | Signal from a brand source (logo, price, product experience) |
| **Dimension** | 6 types (VENDOR, ITEM, AMOUNT, DATETIME, TAX, PAYMENT) | 8 types (semiotic, narrative, ideological, experiential, social, economic, cultural, temporal) |
| **Source** | Document (receipt, invoice, statement) | Encounter type (campaign, store visit, product use, news, review) |
| **Identity gate** | Vendor canonical matching | Brand recognition (logo, name, visual identity) |
| **Cloud** | "These atoms probably describe the same transaction" | "This is what I think the brand is" (perception cloud) |
| **Fact** | Confirmed purchase | Brand conviction ("Tesla IS X") |
| **Re-collapse** | New document forces full recalculation | New evidence (scandal, product, campaign) forces conviction rebuild |
| **Observer** | The system (single, fixed weights) | Human cohort (heterogeneous, variable weights) |

**Table 3.** Domain transfer mapping.

### 4.2 The Critical Extension: Heterogeneous Observers

The financial pipeline has one observer: the system. Its weights are fixed (vendor 0.30, amount 0.40, date 0.20). Every atom is processed through the same scoring function.

Brand perception has *many* observers, each with different weights. A Gen-Z consumer weights social signals at 0.40 and cultural at 0.30. A B2B buyer weights economic at 0.40 and experiential at 0.35. Same signals, different weights, different clouds, different facts.

This is the critical extension that produces Spectral Brand Theory. The seven principles transfer directly. The pipeline stages transfer directly. But the single-observer assumption is replaced by a heterogeneous-observer model where each cohort has its own spectral profile — spectrum, weights, tolerances, and priors — that determines how they process the same signal environment.

The result: the same brand produces different "facts" in different observers' minds. These are not errors or variations on a "true" brand perception. They are the only brand perceptions that exist. There is no brand-in-itself, just as there is no "true reconciliation" independent of the matching algorithm's parameters. The parameters determine the output.

### 4.3 Principle Transfer Validation

Each of the seven principles operates identically in both domains:

**Dimensional typing** (Principle 1): Brand signals are typed by dimension. A logo is a semiotic signal. A price is an economic signal. A product experience is an experiential signal. Signals are compared within dimensions, not across them.

**Source binding** (Principle 2): Each brand signal originates from one encounter type. A social media impression is one source. A store visit is another. The same underlying brand attribute might generate atoms in both encounters, but the atoms are source-bound — the store visit atom and the Instagram atom are separate observations even if they describe the same product.

**Identity gate** (Principle 3): The observer must recognize the brand before any perception forms. Logo, name, visual identity serve this gate function. Without passing the gate, brand signals are noise — the observer does not cluster them because they do not recognize them as belonging to a single entity.

**Asymmetric tolerances** (Principle 4): Different observer cohorts have different tolerance for inconsistency. A brand employee has zero tolerance for ideological contradiction (they live inside the brand). A casual consumer has high tolerance for cultural inconsistency (they do not care about aesthetics). The tolerance is a property of the observer-dimension interaction, not the dimension alone.

**Weighted scoring** (Principle 5): This is the core mechanism of Spectral Brand Theory. Each observer cohort has a weight profile that determines how they cluster brand signals. The weights produce different perception clouds from the same signal set.

**Re-collapse** (Principle 6): A brand scandal introduces new signals that force conviction rebuild. The observer does not "update" their brand image — they dissolve it and re-form from the available evidence: the signals that have survived temporal decay plus crystallized priors, now including the new contradicting signals. This explains both brand resilience (strong convictions resist moderate contradicting evidence) and brand crises (overwhelming contradicting evidence forces wholesale re-evaluation).

**Epistemic separation** (Principle 7): Brand signals (atoms), brand impressions (clouds), and brand convictions (facts) are structurally distinct. A brand signal is not "the brand" — it is one observation. A brand impression is not a conviction — it is a probabilistic cluster. A brand conviction is not permanent — it can be dissolved and rebuilt.

---

## 5. Emergent Properties of the Transfer

The domain transfer does not merely replicate financial processing in a new vocabulary. Three properties emerge in the brand domain that were latent in the financial domain:

### 5.1 Observer Heterogeneity as a Feature

In financial processing, having multiple observers with different weights would be a bug — it would mean the system is inconsistent. In brand perception, observer heterogeneity is *the central feature*. The fact that different cohorts form different convictions from the same signal environment is not a system failure — it is the fundamental mechanism of how brands work. The pipeline architecture handles this naturally: each observer processes the same atoms through their own scoring function, producing their own clouds and facts.

### 5.2 Structural Absence

The financial pipeline assumes positive evidence: atoms are extracted from documents that exist. The brand domain introduces a phenomenon absent in the financial domain: *designed absence as a signal*. Hermes' strategy of deliberately restricting signal emission (no discounts, no online sales for core products, geographic scarcity) functions as a signal in the brand domain — the absence generates perception effects on dimensions other than the restricted one (Zharnikov, 2026a). This extends the atom model with a new emission type (structural absence) and a scarcity multiplier in the cloud formation formula.

### 5.3 Valence Asymmetry

Financial facts do not have valence — a confirmed purchase is neither good nor bad, it simply is. Brand convictions carry valence: positive, negative, or ambivalent. The domain transfer reveals an asymmetric property: negative convictions (built from ideological and social signals) are more resilient than positive convictions (built from experiential and economic signals) because evidence-free negative convictions contain no contradicting dimensions that could introduce ambiguity (Zharnikov, 2026a). This asymmetry is invisible in the financial domain, where all facts are valence-neutral.

---

## 6. Generalizability: Beyond Finance and Brands

The atom-cloud-fact pipeline applies to any domain where heterogeneous observers perceive typed signals from multiple sources under uncertainty. Candidate domains include:

| Domain | Atoms | Observers | Cloud → Fact |
|--------|-------|-----------|-------------|
| **Political perception** | Policy signals, rhetoric, media coverage, personal encounters | Voter cohorts with different ideological profiles | Political impression → voting conviction |
| **Academic reputation** | Papers, citations, presentations, peer review, social media | Different academic communities (field, methodology, seniority) | Scholarly impression → reputation conviction |
| **Product evaluation** | Specs, reviews, demos, competitor comparisons, price | Consumer segments with different priority weights | Product impression → purchase conviction |
| **Medical diagnosis** | Symptoms, test results, patient history, imaging | Different specialists with different diagnostic weights | Diagnostic hypothesis → confirmed diagnosis |

**Table 4.** Candidate domains for the atom-cloud-fact architecture.

The architecture's generalizability rests on a single structural condition: the domain must involve *typed observations from multiple sources that cluster under uncertainty into revisable knowledge*. Where this condition holds, the seven principles apply without modification.

---

## 7. Discussion: Relationship to Existing Epistemological Frameworks

### 7.1 Bayesian Reasoning

The atom-cloud-fact pipeline shares structural similarities with Bayesian reasoning: both update beliefs based on new evidence. However, the pipeline differs in a critical respect. Bayesian updating is incremental — prior beliefs are updated by multiplying with likelihood ratios. The atom-cloud-fact pipeline is *non-incremental*: on re-collapse, facts are dissolved and rebuilt from the complete evidence set. This is epistemically stronger (the result is always consistent with the total evidence) but computationally more expensive.

The re-collapse mechanism also differs from formal belief revision as modeled by AGM theory (Alchourrón, Gärdenfors, & Makinson, 1985), which defines contraction and revision as operations on logically closed belief sets. AGM revision preserves as much of the prior belief set as possible (the principle of minimal change); the atom-cloud-fact pipeline preserves nothing — it dissolves the fact and rebuilds from the complete atom set. This makes the pipeline epistemically more radical than AGM revision but computationally simpler: there is no need to determine which beliefs to retain.

The distinction matters in practice. Bayesian updating can accumulate path-dependent biases — the order in which evidence arrives affects the posterior, even when it should not. The atom-cloud-fact pipeline addresses this through re-collapse: when new evidence arrives, facts are dissolved and rebuilt from the complete available evidence set rather than incrementally updated.

However, the pipeline's path-independence properties differ across domains because signal persistence is domain-specific. In financial reconciliation, atoms are permanent — an invoice discovered in January is as evidentially valid in December as on the day of discovery. The complete atom set is always available for re-collapse, making the pipeline genuinely path-independent: the order of document discovery does not and should not affect which transactions are confirmed.

In brand perception, atoms *decay*. A shop visit from five years ago contributes less to current cloud formation than a visit from yesterday — not because the pipeline discards it, but because human memory attenuates signal luminosity over time. Signals that were emotionally intense or sufficiently reinforced may crystallize into permanent priors, but routine encounters fade. The "available evidence set" at any moment of re-collapse is therefore not the complete historical set but the set of signals that have survived temporal decay plus whatever has crystallized. This makes brand perception path-dependent: the order and timing of encounters matter because they determine which signals are still luminous when re-collapse occurs. Peters (2019) identifies this property — multiplicative, path-dependent dynamics where sequence determines outcome — as the formal definition of non-ergodicity.

The pipeline architecture is the same in both domains. The difference is in the atoms: financial atoms persist; perceptual atoms decay. The architecture is domain-agnostic; signal persistence behavior is domain-specific.

### 7.2 Symbolic vs. Probabilistic Reasoning

The pipeline occupies a space between purely symbolic and purely probabilistic approaches. Atoms are symbolic — typed, named, structured. Clouds are probabilistic — scored, uncertain, revisable. Facts are quasi-symbolic — confirmed, stable, but subject to dissolution. This hybrid structure allows the system to handle both the structured certainty of known data types and the genuine uncertainty of multi-source reconciliation.

Classical expert systems (Buchanan & Shortliffe, 1984) operate in the symbolic regime: rules transform structured inputs into conclusions. Statistical models operate in the probabilistic regime: numerical functions map features to predictions. The atom-cloud-fact pipeline uses symbolic structure at the observation level (dimensional typing, identity gates) and probabilistic computation at the hypothesis level (weighted scoring, threshold collapse). This combination produces results that are both interpretable (you can trace exactly which atoms contributed to which fact) and uncertainty-aware (you can see which clouds have not yet collapsed).

### 7.3 LLM Implementability

A distinctive property of the atom-cloud-fact pipeline is that it can be implemented through natural language instructions to a large language model, without custom code. The seven principles can be expressed as a system prompt: "Extract typed signals across these dimensions. Cluster them using these weights. Identify when the evidence threshold is met. Rebuild from scratch when new evidence contradicts existing conclusions."

This is not trivially possible with other epistemological frameworks. Bayesian networks require explicit probability distributions. Expert systems require formal rule bases. The atom-cloud-fact pipeline's principles are expressible in natural language because they describe *cognitive operations* (perceive, cluster, weigh, decide, revise) rather than *mathematical operations* (multiply, integrate, optimize). LLMs, trained on text describing human reasoning, can execute cognitive operations with surprising fidelity.

The SBT implementation demonstrates this: the six-module analytical pipeline operates entirely as a structured prompt sequence, producing formal multi-cohort brand analysis through natural language instruction rather than code execution (Zharnikov, 2026a). This suggests that the atom-cloud-fact architecture is not merely computationally implementable but *linguistically implementable* — a property that may prove important as LLMs become the primary computational platform for analytical work.

---

## 8. Conclusion

The atom-cloud-fact pipeline is not a technique for financial document processing. It is an epistemological architecture — a formal model of how knowledge forms from heterogeneous observation. The financial domain provided the implementation context. The brand perception domain provided the validation through transfer. The architecture's seven principles — dimensional typing, source binding, identity gating, asymmetric tolerances, weighted scoring, re-collapse, and epistemic separation — appear to capture general properties of observation-to-knowledge progression that are not domain-specific.

The successful transfer to brand perception (producing Spectral Brand Theory) suggests that the pipeline's value lies not in its domain expertise but in its epistemic structure. Any domain where observers perceive typed signals from multiple sources under uncertainty — and must form revisable knowledge from those observations — is a candidate for the atom-cloud-fact architecture.

The architecture is computationally implementable. The financial implementation processes real documents. The brand perception implementation operates as a structured prompt sequence for large language models. Both share the same seven principles and the same three-stage pipeline. The code is different. The epistemology is identical.

---

## References

Alchourrón, C. E., Gärdenfors, P., & Makinson, D. (1985). On the logic of theory change: Partial meet contraction and revision functions. *The Journal of Symbolic Logic*, 50(2), 510–530.

Buchanan, B. G., & Shortliffe, E. H. (1984). *Rule-based expert systems: The MYCIN experiments of the Stanford Heuristic Programming Project*. Addison-Wesley.

Dempster, A. P. (1967). Upper and lower probabilities induced by a multivalued mapping. *The Annals of Mathematical Statistics*, 38(2), 325–339.

Enderton, H. B. (2001). *A mathematical introduction to logic* (2nd ed.). Academic Press.

Goldman, A. I. (1986). *Epistemology and cognition*. Harvard University Press.

Kahneman, D. (2011). *Thinking, fast and slow*. Farrar, Straus and Giroux.

Koffka, K. (1935). *Principles of Gestalt psychology*. Harcourt, Brace.

Kuhn, T. S. (1962). *The structure of scientific revolutions*. University of Chicago Press.

Pearl, J. (1988). *Probabilistic reasoning in intelligent systems: Networks of plausible inference*. Morgan Kaufmann.

Peirce, C. S. (1931–1958). *Collected papers of Charles Sanders Peirce* (C. Hartshorne & P. Weiss, Eds., Vols. 1–6). Harvard University Press.

Polanyi, M. (1966). *The tacit dimension*. Doubleday.

Popper, K. R. (1959). *The logic of scientific discovery*. Hutchinson.

Quine, W. V. O. (1951). Two dogmas of empiricism. *The Philosophical Review*, 60(1), 20–43.

Russell, S., & Norvig, P. (2020). *Artificial intelligence: A modern approach* (4th ed.). Pearson.

Shafer, G. (1976). *A mathematical theory of evidence*. Princeton University Press.

Sowa, J. F. (2000). *Knowledge representation: Logical, philosophical, and computational foundations*. Brooks/Cole.

Zadeh, L. A. (1965). Fuzzy sets. *Information and Control*, 8(3), 338–353.

Zharnikov, D. (2026a). Spectral Brand Theory: A computational framework for multi-dimensional brand perception. Working paper. https://github.com/spectralbranding/sbt-papers/tree/main/spectral-brand-theory

---

## Citation

```bibtex
@article{zharnikov2026alibi,
  title={The Atom-Cloud-Fact Epistemological Pipeline: From Financial Document Processing to Brand Perception Modeling},
  author={Zharnikov, Dmitry},
  year={2026},
  url={https://github.com/spectralbranding/sbt-papers}
}
```
