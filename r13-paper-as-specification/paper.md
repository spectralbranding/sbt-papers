# Paper as Specification: A Machine-Readable Standard for Scientific Claims

**Zharnikov, D.**

Independent Researcher, ORCID 0009-0000-6893-9231

March 2026

---

## Abstract

The verification crisis in science is a specification crisis. Papers communicate claims in natural language optimized for human comprehension but hostile to machine verification. We argue that three prior generation-specification cycles -- printing press + scientific method, internet + structured data, LLMs + paper specification -- establish a pattern: each generation breakthrough in information production was resolved by a specification breakthrough, not faster consumption. We introduce Paper Spec v0.1.0, an open YAML standard that makes a paper's claims, methodology, acceptance criteria, and results machine-readable without replacing the paper itself. The standard defines five verification layers (L0-L4) from schema validation to retraction cascade analysis. We demonstrate the standard on a twenty-paper corpus across two research programs, revealing dependency structures and specification deficiencies invisible in unstructured text. We advance four formal propositions on expressiveness, verification utility, dependency analysis, and cognitive value, each with explicit acceptance criteria and falsification conditions. The standard is human-writable in thirty minutes, incrementally adoptable, and compatible with existing preprint and publication workflows.

**Keywords**: scientific verification, machine-readable claims, reproducibility crisis, structured science, open science, dependency graphs

---

## 1. Introduction

In March 2026, Terence Tao observed that while AI was making mathematical research "richer and broader," it was not making it deeper -- and that the scientific community needed "a semi-formal language for the way that scientists actually talk to each other" (Tao, 2026, 59:20). In the same conversation, he described what he termed the "deductive overhang": the accumulation of verifiable consequences faster than the community can verify them (26:10). Tao's immediate context was mathematical proof, where verification is decidable -- a proof either satisfies the axioms or it does not. But the asymmetry he identified -- that generating candidate ideas is becoming cheap while rigorous verification remains hard -- applies with even greater force to empirical science, where verification is not decidable but depends on experimental design, statistical inference, and replication. The replication crisis, documented across psychology (Open Science Collaboration, 2015), medicine (Ioannidis, 2005), and economics (Camerer et al., 2016), had already demonstrated that the scientific ecosystem was producing claims faster than it could verify them. The scale of this strain is now quantified: peer-reviewed publications grew 5% per year between 2016 and 2022, while reviewer availability grew at less than half that rate (Hanson et al., 2024). LLMs threaten to widen this generation-verification gap by orders of magnitude -- not because they generate formal proofs, but because they generate the plausible prose in which scientific claims are expressed.

The standard response to the verification crisis has been methodological: pre-registration, registered reports, stricter statistical thresholds, open data mandates. These interventions address the quality of individual studies but not the scalability of verification itself. A registered report is still a PDF. Its hypotheses, acceptance criteria, and methodology are still expressed in natural language, legible to human readers but opaque to machines. When a foundational paper is retracted, identifying every downstream claim that depends on it requires a human to read every citing paper and judge the nature of the citation -- a task that is feasible for a paper with fifty citations and impossible for one with five thousand.

We argue that the verification crisis is, at its root, a specification crisis. Scientific papers are the last major information artifact that remains fundamentally unstructured. They are where websites were in 1995: human-readable, machine-opaque, and multiplying faster than any manual process can curate them. The solution is not faster reviewers, just as the solution to early web chaos was not faster librarians. The solution is structured specification.

This paper introduces Paper Spec v0.1.0, a YAML-based standard for machine-readable scientific paper specification. A `paper.yaml` file sits alongside a paper (in a repository, as supplementary material, or in a registry) and captures the paper's claims, methodology, acceptance criteria, results, dependencies, contradictions, and limitations in a format that any YAML parser can consume. The standard is designed to be human-writable in thirty minutes, incrementally adoptable (every section is optional except bibliographic metadata), and expressive enough to represent both empirical and theoretical research without loss of essential structure.

The remainder of this paper proceeds as follows. Section 2 establishes historical precedent by tracing the pattern through which generation breakthroughs in information production were resolved by specification breakthroughs. Section 3 characterizes the specification gap in contemporary science. Section 4 presents the Paper Spec standard. Section 5 defines the five verification layers that the standard enables. Section 6 demonstrates the standard on a twenty-paper corpus. Section 7 discusses connections to research assessment, peer review, and the use of paper.yaml as an independent artifact. Section 8 states four formal propositions. Section 9 addresses limitations. Section 10 concludes.

## 2. Historical Precedent: Generation and Specification

The relationship between information generation and information verification is not new. It has played out at least twice before at civilizational scale, and the resolution in each case followed the same pattern: not better filtering of the old kind, but a structural specification that made the new volume tractable.

### 2.1 The Printing Press and the Scientific Method

The printing press, operational in Europe by the 1450s, reduced the cost of producing written documents by roughly two orders of magnitude (Eisenstein, 1979). The immediate consequence was an explosion of pamphlets, treatises, and claims of every kind -- alchemical recipes alongside astronomical observations, political propaganda alongside anatomical descriptions. The generation breakthrough was mechanical; the verification problem was epistemic. How could a reader distinguish a reliable claim from an unreliable one when both arrived in the same printed format?

The specification solution emerged over the following two centuries: the scientific method. Bacon's *Novum Organum* (1620), the founding of the Royal Society (1660), and Newton's *Principia* (1687) collectively established a specification for credible knowledge claims: falsifiable predictions, controlled experiments, mathematical formalization, and independent replication. The scientific method did not reduce the volume of printed material. It provided a structural standard against which claims could be evaluated -- a specification for what counts as knowledge.

The lag between the generation breakthrough and the specification response is notable. Nearly two centuries elapsed between Gutenberg's press and the institutional consolidation of the scientific method. The intervening period -- the pamphlet wars, the Thirty Years' War, the proliferation of competing cosmologies -- was characterized by high information volume and low verification capacity. The specification, when it arrived, did not merely filter noise; it created a new category of structured claim that could accumulate reliably.

### 2.2 The Internet and Structured Data

The World Wide Web, publicly accessible from 1991, reduced the cost of publishing information by another two orders of magnitude. Early web pages were unstructured text with hyperlinks -- human-readable but machine-opaque. The generation breakthrough was connectivity; the verification problem was discovery. How could a user find reliable information when any page looked the same as any other?

The specification solutions arrived over the following decade: HTML metadata standards such as Dublin Core, search engine algorithms that exploited link structure as a quality signal (PageRank; Brin & Page, 1998), structured data vocabularies such as schema.org, and knowledge graphs that represented entities and relationships in machine-readable form (Bollacker et al., 2008). These standards did not reduce the volume of web content. They made it machine-parseable, enabling automated discovery, ranking, and verification.

The pattern is identical: a generation breakthrough created a volume problem that could not be solved by scaling the old verification method (human curation). The solution was a specification standard that made the new volume tractable to automated processing.

### 2.3 LLMs and the Specification Gap

Large language models, widely deployed from 2023, reduce the cost of generating plausible text -- including scientific hypotheses, literature reviews, and experimental designs -- by yet another order of magnitude. A researcher with access to an LLM can produce a hundred candidate hypotheses in an afternoon, complete with literature grounding and proposed methodologies. The generation breakthrough is cognitive; the verification problem is epistemic, just as it was in the fifteenth century.

The verification infrastructure, however, remains pre-digital. A scientific paper in 2026 is structurally identical to a scientific paper in 1996: a PDF containing natural language, evaluated by two to three human reviewers over a period of weeks to months. The claims are buried in prose. The acceptance criteria are implicit or absent. The dependency on prior work is expressed through citation, which indicates that a paper was read but not which specific claim is load-bearing. The conditions under which the claims would be falsified are rarely stated explicitly, and when they are, they are not machine-extractable.

The historical pattern predicts that this generation-verification gap will be resolved not by faster reviewers but by a specification standard for scientific claims -- a standard that makes the epistemic content of papers machine-readable, just as schema.org made the semantic content of web pages machine-readable. Paper Spec is our proposal for that standard.

## 3. The Specification Gap in Science

### 3.1 Papers as Unstructured Artifacts

A contemporary scientific paper is a remarkable artifact: it compresses months or years of intellectual work into ten to thirty pages of natural language, supported by figures, tables, and equations. It is optimized for a single use case: sequential reading by a domain expert. For every other use case -- systematic review, meta-analysis, replication planning, dependency tracking, retraction impact analysis, automated contradiction detection -- the paper must first be manually decoded by a human reader who extracts the relevant structured information.

This decoding is expensive, error-prone, and non-scalable. Systematic reviews require teams of researchers spending months reading hundreds of papers to extract comparable data points. Meta-analyses depend on the accuracy of manual coding, which varies across coders and studies. When a paper is retracted, identifying the downstream impact requires reading every citing paper -- an average of 35 citations per retracted paper, but occasionally thousands (Fang, Steen, & Casadevall, 2012). In each case, the bottleneck is the same: the information needed is present in the paper but not in a form that machines can process.

### 3.2 Existing Partial Solutions

Several initiatives have addressed fragments of this problem. We review them not to diminish their contributions but to identify the gap that remains.

**Registered Reports** (Chambers, 2013; Nosek & Lakens, 2014) require authors to pre-register hypotheses and analysis plans before data collection. This addresses specification of methodology and, in Stage 1, provides reviewers with explicit predictions. However, registered reports remain natural-language documents. They are not machine-parseable, and they apply only to prospective empirical studies, not to theoretical work, computational research, or post-hoc analyses.

**FAIR Data Principles** (Wilkinson et al., 2016) establish that scientific data should be Findable, Accessible, Interoperable, and Reusable. FAIR has been enormously influential in mandating data sharing, but it applies to data, not to the claims that data supports. A FAIR dataset without a machine-readable description of what the authors conclude from it is a car without a driver.

**Semantic Scholar** (Ammar et al., 2018) and **OpenAlex** (Priem et al., 2022) extract structured metadata from published papers using natural language processing. These systems are valuable for bibliometric analysis, but they reconstruct structure post-hoc from unstructured text -- an inherently lossy process. They extract what they can infer, not what the authors intended.

**Micropublications** (Clark et al., 2014) proposed decomposing papers into machine-readable claim-evidence-reasoning structures. The format was well-designed but never achieved adoption, likely because it required authors to learn a specialized vocabulary and toolchain.

**Nanopublications** (Groth, Gibson, & Velterop, 2010; Kuhn et al., 2021) represent atomic scientific assertions as RDF triples with provenance. Nanopublications are machine-readable by design, but RDF is not human-writable. No working scientist writes RDF triples as part of their research workflow. The adoption barrier is not conceptual but practical: the format demands too much from the author.

**JATS XML** (Journal Article Tag Suite; NISO, 2012) provides structural markup for journal articles -- sections, figures, tables, references. JATS describes document structure, not epistemic structure. It can tell a machine that Section 3 contains a table, but not that the table reports the results of testing Hypothesis 2.

**RO-Crate** (Soiland-Reyes et al., 2022) packages research objects -- data, code, documentation -- with structured metadata. RO-Crate solves the bundling problem but does not address claim specification. A research object that includes a well-packaged dataset and analysis code but no machine-readable description of what the research claims is better organized but not more verifiable.

**CiTO and the SPAR Ontologies** (Shotton, 2010; Peroni & Shotton, 2018) define vocabularies for typed citation relationships and scholarly publishing metadata. CiTO's relationship types -- "extends," "confirms," "disputes," "uses method in" -- are the most direct precursor to Paper Spec's `dependencies` section, which borrows its relationship-type approach. However, CiTO operates at the paper level; Paper Spec extends this to claim-level granularity, specifying not just that Paper A extends Paper B but which specific claim in A depends on which specific claim in B.

**TOP Guidelines** (Nosek et al., 2015) define eight transparency and openness standards (citation standards, data transparency, code transparency, materials transparency, design and analysis transparency, preregistration of studies, preregistration of analysis plans, and replication) with three levels of increasing stringency. TOP demonstrates that incrementally adoptable standards can gain traction in academic publishing -- the same design principle that underlies Paper Spec's "every section optional" architecture.

**CRediT** (Brand et al., 2015) standardizes author contribution roles. It specifies who did what, not what was claimed or found.

**Scienceverse** (Lakens & DeBruine, 2021) is the closest prior art to Paper Spec's ambition of making scientific claims machine-readable. Scienceverse provides an R package that stores hypotheses, analysis code, and data in a JSON structure, then auto-evaluates whether the results support the hypotheses. This is machine-readable hypothesis testing -- a genuine advance. However, scienceverse is limited in three ways that Paper Spec addresses: it operates at the hypothesis level, not the document level (it does not capture methodology, dependencies, acceptance criteria, or limitations as structured fields); it is bound to the R ecosystem (a researcher using Python, Julia, or no code at all cannot use it); and it does not model cross-paper dependencies (it cannot answer "which papers would be affected if this paper's hypothesis were retracted?"). Paper Spec can be understood as the document-level, language-agnostic generalization of what scienceverse achieves for individual hypothesis tests.

**The Open Research Knowledge Graph (ORKG)** (Jaradeh et al., 2019) takes the opposite approach to Paper Spec: rather than asking authors to specify their contributions, ORKG reconstructs structured contribution descriptions post-hoc through crowdsourcing and NLP extraction. ORKG is a valuable infrastructure project with active institutional support, and its structured representation of research problems, methods, and results is conceptually aligned with Paper Spec's goals. The design philosophy, however, differs fundamentally. Post-hoc extraction is inherently lossy: a crowd annotator or an NLP system cannot know which of a paper's twenty citations is a critical dependency whose retraction would invalidate the paper's core claims. Only the author knows this. Paper Spec places the specification burden on the author -- the only party with complete access to ground truth -- and keeps it lightweight enough (thirty minutes, a text editor) to be feasible.

**SciKGTeX** (Bless et al., 2023) embeds structured contribution annotations directly into LaTeX source code, from which ORKG can harvest structured metadata. SciKGTeX achieves low-barrier annotation (seven minutes per paper in usability testing) and demonstrates that researchers can produce structured metadata as part of their writing workflow. However, SciKGTeX is limited to LaTeX users and produces annotations at the contribution level, not the full-document level. Paper Spec provides a standalone companion file -- independent of any authoring tool or publishing platform -- that captures claims, acceptance criteria, dependencies, and limitations.

### 3.3 The Missing Layer

What none of these solutions provides is a single, human-writable, machine-parseable, format-agnostic file that captures the full epistemic content of a paper: what it claims, how those claims were tested, what would prove them wrong, what they depend on, and what their known limits are. Table 1 summarizes how each initiative addresses the key requirements.

**Table 1. Comparison of structured science standards.** HW = human-writable; MR = machine-readable; FA = format-agnostic; AC = acceptance criteria; DC = dependency criticality; IN = incremental adoption.

| Standard | HW | MR | Scope | FA | AC | DC | IN |
|----------|:-:|:-:|--------|:-:|:-:|:-:|:-:|
| Registered Reports | Yes | No | Methodology | Yes | Partial | No | No |
| FAIR | N/A | Yes | Data | Yes | No | No | Yes |
| Nanopublications | No | Yes | Assertion | Yes | No | Partial | No |
| Micropublications | No | Yes | Claim-evidence | Yes | No | No | No |
| CiTO / SPAR | No | Yes | Citation | Yes | No | No | No |
| scienceverse | Partial | Yes | Hypothesis | No | No | No | No |
| ORKG | No | Yes | Contribution | Yes | No | No | Partial |
| SciKGTeX | Partial | Yes | Contribution | No | No | No | Partial |
| RO-Crate | No | Yes | Research object | Yes | No | No | Yes |
| **Paper Spec** | **Yes** | **Yes** | **Full paper** | **Yes** | **Yes** | **Yes** | **Yes** |

This is the gap that Paper Spec fills.

## 4. Paper Spec: A Machine-Readable Standard

### 4.1 Design Principles

Paper Spec v0.1.0 is designed around six principles derived from the adoption failures of prior structured-science initiatives:

1. **Human-writable.** A working researcher should be able to write a `paper.yaml` for their paper in thirty minutes using a text editor. No specialized tooling, no ontology expertise, no RDF.

2. **Machine-parseable.** Standard YAML 1.2, validatable against a JSON Schema. Any programming language with a YAML parser can consume a `paper.yaml` file.

3. **Incremental adoption.** Every section is optional except `meta` (bibliographic metadata). A `paper.yaml` with nothing but metadata is still useful -- it is a structured bibliographic record. Each additional section adds independent value. There is no minimum threshold for utility.

4. **Minimal jargon.** Field names are self-explanatory to a researcher who has never seen the spec. If a field name requires a paragraph of explanation, it is the wrong name.

5. **Stable identifiers.** Claim IDs within a paper are stable across paper versions, enabling external references that survive revisions. When Paper B depends on Claim P3 from Paper A, that reference remains valid even after Paper A publishes a revised version.

6. **No opinions on content.** The spec describes structure, not quality. It does not judge whether a claim is good, whether a methodology is sound, or whether a p-value is meaningful. It records what the authors state.

These principles reflect a lesson from the history of successful standards: adoption requires low authoring cost, high individual benefit (even without network effects), and compatibility with existing workflows. HTML succeeded not because it was the best markup language but because it was simple enough for anyone to write. YAML occupies a similar position in the data serialization landscape: readable without training, writable without tooling, parseable without effort.

### 4.2 The Seven Questions

A `paper.yaml` file answers seven questions that every reader of a scientific paper eventually asks:

1. **What does this paper claim?** The `claims` section lists each truth claim with a unique ID, type (hypothesis, proposition, theorem, definition, conjecture), formal statement, testability, and status.

2. **How were those claims tested?** The `methodology` and `results` sections describe the study design, sample, analysis method, and outcomes mapped to specific claims.

3. **What would prove them wrong?** The `acceptance` section captures confirmation criteria and, critically, falsification criteria for each claim -- the conditions under which the authors consider their own claims refuted.

4. **Can I reproduce this?** The `data`, `code`, and `replication` sections specify what is available, where it is, and what a replicator would need.

5. **What does this depend on?** The `dependencies` section identifies not just cited papers but the specific claims in those papers that are load-bearing for the current work, with relationship types (extends, applies, tests, contradicts, refines) and criticality flags.

6. **What are its known limits?** The `limitations` and `contradictions` sections record acknowledged weaknesses and known conflicts with other published work.

7. **Where can I find it, and how did it get there?** The `repositories` section tracks all deposits across platforms. The `submission_history` section documents the paper's publication journey -- submissions, decisions, revisions -- in the interest of open science transparency.

### 4.3 Structure Overview

A `paper.yaml` file contains the following top-level keys:

```yaml
spec_version: "0.1.0"

meta:               # Required. Bibliographic metadata.
  title: "..."
  authors:
    - name: "Last, First"
      orcid: "0000-0000-0000-0000"
  doi: "10.xxxx/..."
  date: "2026-01-15"
  venue: "Journal Name"
  keywords: [...]

claims:             # The paper's truth claims.
  - id: "P1"
    type: proposition
    statement: "..."
    testable: true
    status: not_tested

methodology:        # How claims were tested.
  type: theoretical
  design: "proof by construction"

acceptance:         # Confirmation/falsification criteria.
  - claim_id: "P1"
    criterion: "..."
    falsification: "..."

dependencies:       # Load-bearing prior work.
  - doi: "10.xxxx/..."
    claim: "specific claim depended upon"
    relationship: extends
    critical: true

results:            # Outcomes mapped to claims.
  - claim_id: "P1"
    status: supported

limitations:        # Acknowledged limits.
  - description: "..."
    severity: moderate

repositories:       # Where the paper lives.
  - platform: "Zenodo"
    doi: "10.5281/zenodo.xxxxx"

submission_history: # Publication journey.
  - venue: "Journal Name"
    date_submitted: "2026-03-01"
    decision: under_review
```

The example above is abbreviated. The full specification, including all fields, types, enums, and validation rules, is published as a standalone document with a companion JSON Schema (https://github.com/spectralbranding/paper-spec).

### 4.4 A Worked Example

Consider Kahneman and Tversky's (1979) prospect theory paper. The `claims` section would contain:

```yaml
claims:
  - id: "H1"
    type: hypothesis
    statement: >
      People underweight outcomes that are merely probable
      compared to outcomes obtained with certainty (the
      certainty effect), leading to risk aversion in choices
      involving sure gains and risk seeking in choices
      involving sure losses.
    testable: true
    tested_in_paper: true
    status: supported

  - id: "H2"
    type: hypothesis
    statement: >
      The value function is defined on deviations from a
      reference point, is generally concave for gains and
      convex for losses, and is steeper for losses than
      for gains (loss aversion).
    testable: true
    tested_in_paper: true
    status: supported
    depends_on: ["H1"]
```

The corresponding `acceptance` entry:

```yaml
acceptance:
  - claim_id: "H1"
    criterion: >
      In forced-choice experiments, a statistically significant
      majority of subjects prefer a certain gain over a
      probabilistically equivalent or superior gamble, and
      prefer a gamble over a certain loss of equivalent
      expected value.
    falsification: >
      Subjects show no systematic preference for certainty
      in gains or gambling in losses -- choices are consistent
      with expected utility theory.
```

And the `dependencies` entry, identifying a specific prior claim this builds on:

```yaml
dependencies:
  - reference: >
      von Neumann, J., & Morgenstern, O. (1947). Theory of
      Games and Economic Behavior.
    claim: >
      Expected utility theory -- the baseline model that
      prospect theory replaces.
    relationship: contradicts
    critical: true
```

The power of this format becomes apparent when hundreds of such files exist. A machine can traverse the dependency graph, identify every paper whose critical dependencies include a retracted claim, flag contradictions between papers that reference the same prior work differently, and surface completeness gaps where claims lack falsification criteria.

## 5. Verification Layers: From Schema to Integrity

Paper Spec enables a hierarchy of five verification layers, each building on the previous:

### 5.1 L0: Schema Validation

The most basic layer: does the `paper.yaml` file conform to the JSON Schema? Are required fields present? Are enum values valid? Are claim IDs unique? L0 catches structural errors -- a misspelled field name, a missing author, a claim type of "hypothsis" -- and requires nothing more than a standard JSON Schema validator. L0 is fully automated and deterministic. It exists now, as a reference implementation in the Paper Spec repository.

### 5.2 L1: Internal Consistency

L1 checks logical consistency within a single `paper.yaml` file. Do all `claim_id` references in `acceptance` and `results` point to claims that exist in `claims`? Does every claim marked `tested_in_paper: true` have a corresponding entry in `results`? Does the `methodology.type` match the claim types (a paper with `methodology.type: empirical` should not contain claims of type `theorem`)? L1 can be implemented as a rules engine operating on the parsed YAML. No natural language processing is required. The rules are finite and enumerable.

### 5.3 L2: Completeness

L2 assesses whether the `paper.yaml` captures the paper's content adequately. Are there claims in the prose that are absent from the `claims` section? Are acceptance criteria vague ("the effect should be significant") or precise ("Cohen's d >= 0.5, p < .005")? Are major limitations acknowledged? L2 requires comparison between the `paper.yaml` and the paper text, which means it benefits from LLM assistance. An LLM can read the paper and the YAML in parallel and flag discrepancies: "Section 4 introduces Proposition 3, which is not listed in the claims section." L2 is not fully automated -- it produces suggestions, not verdicts -- but it dramatically reduces the cognitive load of completeness checking.

### 5.4 L3: Plausibility

L3 asks whether the paper's prose actually supports the claims stated in the YAML. Does the evidence presented in Section 5 justify the "supported" status of H1? Is the methodology described in the paper consistent with the methodology summarized in the YAML? This is a cross-document consistency check, and it is the layer where LLMs are most useful. A human reviewer performs exactly this check during peer review; an LLM can perform it in seconds, not as a replacement for human judgment but as a first-pass filter that flags obvious inconsistencies before a human reviewer sees the paper.

### 5.5 L4: External Integrity

L4 operates across a corpus of `paper.yaml` files. Given a network of papers with declared dependencies, L4 enables:

**Retraction cascade analysis.** When Paper A is retracted, which downstream papers have claims that critically depend on Paper A's claims? The dependency graph, constructed from the `dependencies` sections of all papers in the corpus, answers this question algorithmically. Without Paper Spec, answering it requires a human to read every citing paper and judge whether the citation is critical -- a task that scales linearly with the number of citations and is practically impossible for highly cited papers. Recent evidence confirms the urgency: Bar-Ilan and Halevi (2024) found that the majority of post-retraction citations are positive, suggesting that authors either do not know or do not check whether their cited sources have been retracted. A dependency graph with criticality flags would make retraction impact assessment automatic.

**Contradiction detection.** When Paper A and Paper B both depend on Paper C but draw opposite conclusions, the `contradictions` sections (supplemented by automated comparison of `results` sections) can flag the conflict. Currently, contradictions in the literature are discovered by individual readers who happen to have read both papers -- a process that depends on chance and expertise.

**Dependency graph traversal.** The full dependency network reveals the load-bearing structure of a research field: which papers are foundational (many critical dependents), which are peripheral (few dependents), and which are bridges connecting otherwise separate subfields. This structural information is invisible in citation counts, which treat all citations equally.

**Claim-level semantic search.** Instead of searching for papers by keyword, a researcher can search for specific claims: "Find all papers that claim working memory mediates the effect of sleep deprivation on decision quality." This is not possible with unstructured papers; it is trivial with a corpus of `paper.yaml` files.

## 6. Demonstration: A Twenty-Paper Corpus

### 6.1 The Corpus

We demonstrate Paper Spec by writing `paper.yaml` files for twenty papers: nineteen papers in the Spectral Brand Theory (Zharnikov, 2026a) and Organizational Schema Theory (Zharnikov, 2026i) research programs, plus the present paper. The papers span theoretical foundations, mathematical formalizations, empirical case studies, literature surveys, and cross-domain analogies. They range from 4,000 to 12,000 words and contain between two and seven formal propositions or theorems each.

The corpus is deliberately single-author and single-program. This is a limitation for generalizability but an advantage for demonstration: it provides a controlled environment where ground truth is fully known (the author wrote both the papers and the YAML files), the dependency structure is rich (the papers build on each other extensively), and the diversity of paper types is sufficient to test the standard's expressiveness.

### 6.2 Authoring Experience

The twenty `paper.yaml` files were written manually, without LLM assistance, over approximately twelve hours -- an average of thirty-six minutes per paper. The time varied predictably: papers with clearly stated propositions and explicit methodology (e.g., the formal metric paper) required twenty to twenty-five minutes. Papers with implicit claims embedded in discursive prose required forty-five to fifty minutes. In every case, the most time-consuming step was articulating acceptance criteria. Specifying what would confirm a claim is straightforward; specifying what would refute it requires the author to confront the limits of their own argument. This cognitive work is not overhead; it is the work that improves the paper itself.

### 6.3 What the Corpus Reveals

The twenty-paper corpus, once structured, reveals patterns that are invisible in the unstructured originals:

**Dependency depth.** The foundational paper (Zharnikov, 2026a) is a critical dependency for sixteen of the remaining nineteen papers. A retraction of the foundational paper would cascade through the entire program. This is unsurprising in hindsight, but the dependency graph makes the propagation path explicit: retraction of the foundational paper would invalidate the formal metric paper, which would in turn invalidate the projection bounds, cohort boundaries, and sphere packing papers, each of which has its own dependents. The cascade is not a flat list but a directed acyclic graph with depth four.

**Bottleneck identification.** Two papers -- the formal metric and the diffusion dynamics paper -- serve as bridges. Most downstream papers depend on the foundational paper through one of these two intermediaries. If a flaw were found in the formal metric, the practical impact would be nearly as severe as a flaw in the foundational paper itself, even though the formal metric has fewer direct citations.

**Claim density variation.** The number of formal claims per paper varies from two (the literature survey) to seven (the portfolio theory paper). Papers with more claims have more internal dependencies -- later claims depending on earlier claims within the same paper -- creating a within-paper cascade structure that mirrors the between-paper dependency graph.

**Falsification gap.** In the process of writing acceptance criteria, we identified three claims across the corpus whose falsification conditions were genuinely unclear -- not because the claims were unfalsifiable but because the original papers had not articulated the boundary between confirmation and refutation. Writing the `paper.yaml` forced this articulation, which in turn prompted revisions to the papers themselves. The specification process improved the specified artifact.

## 7. Discussion

### 7.1 Specification Gaps Across Domains

The specification gap in science -- the distance between what a researcher intends to claim and what a reader can extract -- is an instance of a broader pattern. Systematic gaps between specification, implementation, and perception recur across domains from genetics to organizational design (Zharnikov, 2026i, 2026l). Paper Spec addresses the first transition in the scientific case: from intention to expression.

### 7.2 Scalar Metrics and Structural Alternatives

The San Francisco Declaration on Research Assessment (DORA, 2012), the Leiden Manifesto (Hicks et al., 2015), and the Coalition for Advancing Research Assessment (CoARA, 2022) -- now encompassing over 700 organizations -- all argue that scalar metrics -- journal impact factors, h-indices, citation counts -- are poor proxies for research quality. A citation count treats all citations equally: a critical dependency that would invalidate downstream work if retracted is counted the same as a passing mention in a literature review. Paper Spec's dependency graph provides a structural alternative. When every citation is typed (extends, tests, contradicts) and flagged for criticality, the topology of a research field becomes visible in a way that no scalar metric can represent. This does not replace expert judgment -- DORA and the Leiden Manifesto are right that no metric can -- but it provides the structured substrate on which better assessments could be built.

### 7.3 The Future of Peer Review

Paper Spec is not a replacement for peer review. It is infrastructure that makes peer review more efficient. A reviewer who receives a paper with an accompanying `paper.yaml` file can immediately see the paper's claims, their status, their acceptance criteria, and their dependencies. The reviewer can verify, before reading a single paragraph, whether the paper has stated its claims clearly enough to be evaluated. L1 and L2 validation can be run automatically as part of the editorial workflow, flagging obvious issues (missing acceptance criteria, results that do not map to claims, methodology mismatches) before the paper reaches a reviewer.

This shifts the reviewer's role from extraction to evaluation. Currently, a substantial fraction of review time is spent determining what the paper claims. With a `paper.yaml` file, this extraction is done by the author and validated by machine. The reviewer can focus on what humans do best: assessing whether the evidence supports the claims, whether the methodology is appropriate, whether the interpretation is reasonable, and whether the contribution is significant.

### 7.4 Paper.yaml as Independent Artifact

A `paper.yaml` file need not travel with the paper. Because it is a self-contained, machine-readable document, it can be shared independently -- before publication, before data collection, or before the paper itself exists in any form. This makes it a versatile instrument at several stages of the research lifecycle. Shared before data collection, a `paper.yaml` file functions as machine-readable pre-registration: the claims, acceptance criteria, and falsification conditions are on record in a format that cannot be ambiguously reinterpreted after results are known. Shared during collaboration, it gives co-authors and advisors a structural overview of the paper's argument without requiring them to read a draft. Shared with grant agencies, it provides a precise description of what the proposed research will claim and how those claims will be evaluated. Shared before peer review, it enables structured review: reviewers see the claim structure upfront and can evaluate whether the paper delivers on its own stated terms. In each case, the author owns the `paper.yaml` file and controls when and how to share it -- it is a meta-passport for the research, not a surveillance instrument.

### 7.5 Adoption Barriers

The primary barrier to adoption is not technical but sociological. Researchers already face substantial documentation burdens: data management plans, ethics approvals, FAIR compliance, CRediT statements, ORCID maintenance. Adding a `paper.yaml` requirement would meet justified resistance. Paper Spec is designed to mitigate this through incremental adoption -- a `paper.yaml` with nothing but `meta` is already useful -- and through the principle that the authoring process produces value for the author (the cognitive work of articulating claims and acceptance criteria improves the paper).

A second barrier is institutional. Journals would need to accept `paper.yaml` as supplementary material, repositories would need to index it, and tooling would need to validate and visualize it. These are achievable goals, but they require coordination across stakeholders. The experience of schema.org -- which achieved adoption by providing immediate value to individual publishers (better search engine indexing) while building network effects over time -- is the relevant precedent.

## 8. Propositions

We advance four propositions that are empirically testable as the standard matures:

**Proposition 1 (Expressiveness).** A `paper.yaml` file can represent the core claims, methodology, acceptance criteria, and results of any empirical or theoretical paper without loss of essential structure. Specifically: for any paper P, a domain expert reading only the `paper.yaml` file can reconstruct the paper's claim structure -- the number, type, and logical dependencies of claims -- with high inter-rater agreement with a domain expert reading the full paper.

**Proposition 2 (Verification utility).** Given a corpus of `paper.yaml` files, automated verification of internal consistency (L1) and completeness (L2) can identify specification deficiencies that would take a human reviewer minutes to hours to detect. Specifically: L1 and L2 checks will flag at least one issue in the majority of first-draft `paper.yaml` files, where each flagged issue corresponds to a genuine specification deficiency (missing acceptance criterion, inconsistent claim status, results not mapped to claims).

**Proposition 3 (Dependency analysis).** The dependency graph constructed from `paper.yaml` files enables automated retraction impact analysis. Specifically: when a paper in the corpus is designated as retracted, the dependency graph identifies all downstream claims with `critical: true` dependencies on the retracted paper's claims, and this algorithmically identified set matches the set a domain expert would identify with high precision and recall.

**Proposition 4 (Cognitive value).** The specification overhead of writing a `paper.yaml` file (estimated thirty to sixty minutes per paper) is dominated by the cognitive work of articulating claims and acceptance criteria -- work that improves the paper itself. Specifically: researchers who write `paper.yaml` files for their papers before submission will report that the process identified at least one substantive issue (unclear claim, missing falsification criterion, unacknowledged limitation) in a substantial fraction of cases.

## 9. Limitations

This paper is theoretical. It proposes a standard and demonstrates it on a single-author corpus. Several limitations must be acknowledged.

**No adoption data.** We have no evidence that researchers outside the author's own program would use Paper Spec, find it useful, or encounter the adoption barriers we anticipate. The propositions are stated but not tested. Empirical validation requires a multi-author, multi-field pilot study.

**Single-author corpus.** The twenty-paper demonstration is drawn from a single research program by a single author. This means the author had complete access to ground truth -- the intended claims, the actual methodology, the genuine dependencies -- which a third-party specification writer would not. The thirty-six-minute average authoring time may not generalize to papers the author did not write. The dependency structure is unusually rich because the papers were designed as a coherent program; independent papers may have sparser dependency graphs and reveal less structure. Critically, a single-author corpus cannot test adoption: the author is maximally motivated and maximally informed, representing the easiest possible case for any specification exercise. The "falsification gap" finding (Section 6.3) -- that writing `paper.yaml` files surfaced unclear claims -- is suggestive but should be interpreted cautiously. Any structured self-reflection exercise (a checklist, a conversation with a colleague, a detailed outline) might produce similar discoveries. The distinctive value of Paper Spec over unstructured reflection is its machine-readability and its cumulative network effects, neither of which can be demonstrated on a self-authored corpus. Genuine validation requires independent researchers specifying papers they did not write, in fields with different methodological conventions, under realistic time pressures.

**Theoretical papers overrepresented.** Fifteen of the twenty papers in the corpus are primarily theoretical. The standard's expressiveness for empirical research, computational research, and meta-analyses is demonstrated by the remaining five but not extensively tested. Fields with complex statistical designs (e.g., clinical trials with adaptive protocols) or with non-standard methodologies (e.g., ethnographic research) may require extensions to the standard.

**No institutional validation.** We have not tested whether journals would accept `paper.yaml` files as supplementary material, whether repositories would index them, or whether reviewers would use them. The standard's utility at scale depends on institutional adoption, which this paper can only argue for, not demonstrate.

**Version 0.1.0.** The standard is at its initial version. Field names, enum values, and section structures may change based on community feedback. Early adopters face the risk of specification instability, mitigated by the semantic versioning policy and migration commitment described in the specification document.

## 10. Conclusion

Every generation breakthrough in information production has been resolved by a specification breakthrough. The printing press was tamed by the scientific method. The internet was tamed by structured data. Large language models, which have collapsed the cost of generating scientific hypotheses, demand an equivalent specification response for scientific claims themselves.

Paper Spec v0.1.0 is a proposal for that response: a YAML companion file that makes a paper's claims, methodology, acceptance criteria, results, dependencies, contradictions, and limitations machine-readable. It is human-writable in thirty minutes, machine-parseable by any YAML processor, and incrementally adoptable. It enables five layers of automated verification, from schema validation to cross-corpus dependency graph traversal.

The standard is not sufficient to solve the verification crisis. No specification can substitute for the scientific judgment of human reviewers or the empirical work of replication. But specification is necessary. Until the epistemic content of scientific papers is machine-readable, verification cannot scale. Paper Spec is an attempt to make it so.

---

## References

Ammar, W., Groeneveld, D., Bhagavatula, C., Beltagy, I., Crawford, M., Downey, D., ... & Weld, D. S. (2018). Construction of the literature graph in Semantic Scholar. *Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics*, 84-91.

Bar-Ilan, J., & Halevi, G. (2024). On the shoulders of fallen giants: What do references to retracted research tell us about citation behaviors? *Quantitative Science Studies*, 5(1), 188-212.

Bless, C., Garijo, D., & Auer, S. (2023). SciKGTeX -- A LaTeX package to semantically annotate contributions in scientific publications. *Proceedings of the ACM/IEEE Joint Conference on Digital Libraries (JCDL 2023)*.

Bollacker, K., Evans, C., Paritosh, P., Sturge, T., & Taylor, J. (2008). Freebase: A collaboratively created graph database for structuring human knowledge. *Proceedings of the 2008 ACM SIGMOD International Conference on Management of Data*, 1247-1250.

Brand, A., Allen, L., Altman, M., Hlava, M., & Scott, J. (2015). Beyond authorship: Attribution, contribution, collaboration, and credit. *Learned Publishing*, 28(2), 151-155.

Brin, S., & Page, L. (1998). The anatomy of a large-scale hypertextual web search engine. *Computer Networks and ISDN Systems*, 30(1-7), 107-117.

Camerer, C. F., Dreber, A., Forsell, E., Ho, T. H., Huber, J., Johannesson, M., ... & Wu, H. (2016). Evaluating replicability of laboratory experiments in economics. *Science*, 351(6280), 1433-1436.

Chambers, C. D. (2013). Registered reports: A new publishing initiative at Cortex. *Cortex*, 49(3), 609-610.

Clark, T., Ciccarese, P. N., & Goble, C. A. (2014). Micropublications: A semantic model for claims, evidence, arguments and annotations in biomedical communications. *Journal of Biomedical Semantics*, 5, 28.

CoARA. (2022). Agreement on reforming research assessment. Coalition for Advancing Research Assessment. https://coara.eu/agreement/the-agreement-full-text/

DORA. (2012). San Francisco Declaration on Research Assessment. https://sfdora.org/read/

Eisenstein, E. L. (1979). *The printing press as an agent of change*. Cambridge University Press.

Fang, F. C., Steen, R. G., & Casadevall, A. (2012). Misconduct accounts for the majority of retracted scientific publications. *Proceedings of the National Academy of Sciences*, 109(42), 17028-17033.

Groth, P., Gibson, A., & Velterop, J. (2010). The anatomy of a nanopublication. *Information Services and Use*, 30(1-2), 51-56.

Hanson, M. A., Barreiro, P. G., Crosetto, P., & Brockington, D. (2024). The strain on scientific publishing. *Quantitative Science Studies*, 5(4), 823-843.

Hicks, D., Wouters, P., Waltman, L., de Rijcke, S., & Rafols, I. (2015). Bibliometrics: The Leiden Manifesto for research metrics. *Nature*, 520(7548), 429-431. https://doi.org/10.1038/520429a

Ioannidis, J. P. A. (2005). Why most published research findings are false. *PLoS Medicine*, 2(8), e124.

Jaradeh, M. Y., Oelen, A., Farfar, K. E., Prinz, M., D'Souza, J., Kismihok, G., ... & Auer, S. (2019). Open Research Knowledge Graph: Next generation infrastructure for semantic scholarly knowledge. *Proceedings of the 10th International Conference on Knowledge Capture (K-CAP 2019)*, 243-246.

Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-292.

Kuhn, T., Taelman, R., Emonet, V., Hoekstra, R., Dumontier, M., & Bonino da Silva Santos, L. O. (2021). Semantic publishing with nanopublications. *PeerJ Computer Science*, 7, e387.

Lakens, D., & DeBruine, L. M. (2021). Improving transparency, falsifiability, and rigor by making hypothesis tests machine-readable. *Advances in Methods and Practices in Psychological Science*, 4(2), 1-12.

NISO (2012). *JATS: Journal Article Tag Suite* (ANSI/NISO Z39.96-2012). National Information Standards Organization.

Nosek, B. A., & Lakens, D. (2014). Registered reports: A method to increase the credibility of published results. *Social Psychology*, 45(3), 137-141.

Nosek, B. A., Alter, G., Banks, G. C., Borsboom, D., Bowman, S. D., Breckler, S. J., ... & Yarkoni, T. (2015). Promoting an open research culture. *Science*, 348(6242), 1422-1425.

Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science*, 349(6251), aac4716.

Peroni, S., & Shotton, D. (2018). The SPAR ontologies. *Proceedings of the International Semantic Web Conference (ISWC 2018)*, LNCS 11137, 119-136.

Priem, J., Piwowar, H., & Orr, R. (2022). OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts. *arXiv Preprint*, arXiv:2205.01833.

Shotton, D. (2010). CiTO, the Citation Typing Ontology. *Journal of Biomedical Semantics*, 1(Suppl 1), S6.

Soiland-Reyes, S., Sefton, P., Crosas, M., Castro, L. J., Coppens, F., Fernandez, J. M., ... & Groth, P. (2022). Packaging research artefacts with RO-Crate. *Data Science*, 5(2), 97-138.

Tao, T. (2026). How the world's top mathematician uses AI [Interview by D. Patel]. *Dwarkesh Podcast*. https://www.youtube.com/watch?v=Q8Fkpi18QXU

Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., Appleton, G., Axton, M., Baak, A., ... & Mons, B. (2016). The FAIR guiding principles for scientific data management and stewardship. *Scientific Data*, 3, 160018.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026i). The Organizational Schema Theory: Test-driven business design. Working Paper. https://doi.org/10.5281/zenodo.18946043

Zharnikov, D. (2026l). The rendering problem: From genetic expression to brand perception. Working Paper. https://doi.org/10.5281/zenodo.19064426
