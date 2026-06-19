# Research as Repository: Infrastructure for Transparent, Attributed, and Machine-Readable Scholarly Communication

Dmitry Zharnikov

ORCID: 0009-0000-6893-9231

DOI: [10.5281/zenodo.19294864](https://doi.org/10.5281/zenodo.19294864)

Working Paper v2.2.0 – March 2026 (revised June 2026)

---

## Abstract

Scientific evaluation relies on a self-reinforcing loop: universities evaluate researchers by journal prestige, journals evaluate papers partly by institutional affiliation, and no one evaluates the research directly — because direct evaluation at scale has lacked the necessary infrastructure. This paper proposes a protocol that provides that infrastructure by treating every research program as a version-controlled repository. A paper is a render of the research at a point on its timeline: a frozen snapshot forked to a journal so the community can confirm the findings. Grounded in information science scholarship on structured knowledge objects [@renear-2009-strategic-reading-ontologies], compound scholarly outputs [@borgman-2015-big-data-little], and knowledge infrastructures [@edwards-2013-knowledge-infrastructures-intellectual; @leonelli-2016-datacentric-biology-philosophical], the protocol introduces fork-based submission, automated compliance gates, attributed reviewer commits, provenance chains, structural funding and affiliation metadata, AI-traceability by design, and a commit-reveal privacy primitive that lets researchers establish cryptographic priority and provenance through public commit hashes while keeping content disclosure under their control. The protocol optimizes the knowledge production process, not the paper: existing publishing reforms improve the rendered artifact; this protocol makes the research itself structurally transparent. Combined with the Paper Spec standard [@zharnikov-2026m-projection-cascade-why], which specifies what a paper claims, the repository protocol specifies how the research was built, evaluated, and decided upon.

**Keywords**: scientific publishing, version control, peer review, research infrastructure, open science, provenance, knowledge production, research evaluation, AI transparency, intellectual work proof, research wiki, scholarly communication

---

## 1. Introduction

### 1.1 A Gap Every Other Domain Has Already Solved

The global scientific publishing system processes approximately 3 million papers per year [@unesco-2021-unesco-science-report-race] through a pipeline built on a single assumption: a paper is a document. A PDF file. A static artifact transmitted from author to editor to reviewer to publisher [@renear-2009-strategic-reading-ontologies]. Every tool in the pipeline — manuscript submission portals, editorial management systems, reviewer interfaces, typesetting workflows — treats the paper as an opaque binary object that moves between mailboxes.

This assumption was adequate when papers were physically printed and mailed. It is now a significant structural constraint on every reform the scientific community has attempted in the past two decades.

The document assumption has deep historical roots: the codex as the unit of scholarly communication predates the printing press, and centuries of legal, commercial, and epistemic investment in the document form have made it seem natural [@willinsky-2018-intellectual-properties-learning]. Open access reforms — accelerated by mandates such as Plan S [@coalition-2018-plan-s-making-full] — change *who can read* the document. They do not change the document. Preprint servers change *when* the document becomes available. They do not change its structure. Registered reports change *what sequence* the document follows. They do not change how it is tracked. Post-publication review adds commentary *about* the document. It does not integrate with the document's own history.

Each reform addresses one dimension of the publishing problem while leaving the document assumption intact. The result is a system that has been incrementally improved on six dimensions simultaneously — access, timing, sequence, commentary, data sharing, reproducibility — without any reform touching the structural foundation that constrains all of them.

Information science has identified this structural gap for decades. Renear and Palmer [-@renear-2009-strategic-reading-ontologies] showed that meaningful machine mediation of scientific claims requires structured, ontology-grounded representations — not static documents. Borgman [-@borgman-2015-big-data-little] demonstrated that scholarly objects are inherently compound, bundles of heterogeneous artifacts linked by provenance rather than monolithic files. Edwards, Jackson, Bowker, and colleagues [-@edwards-2013-knowledge-infrastructures-intellectual] characterized knowledge infrastructures — the material and social systems through which reliable knowledge is produced — and found scholarly communication among the most underdeveloped in this regard. Leonelli [-@leonelli-2016-datacentric-biology-philosophical] showed how data-centric research practices depend on provenance-aware infrastructure to remain interpretable across communities and over time.

Scientific publishing is the only knowledge-intensive domain without formal version control and provenance infrastructure. Legal systems track case law revisions. Financial auditing requires audit trails. Clinical research mandates trial registration. Supply chain management maintains chain of custody. Software engineering uses Git. Each domain independently developed provenance tracking because each discovered that knowledge integrity requires it. Publishing has not.

Table 1: Provenance mechanisms across knowledge-intensive domains.

| Domain | Provenance mechanism | When adopted |
|--------|---------------------|-------------|
| Legal | Case law revision tracking, legislative history | 19th century |
| Financial auditing | Audit trails, SOX compliance | 1930s (SEC), 2002 (SOX) |
| Clinical research | Trial registration (clinicaltrials.gov) | 2005 (ICMJE requirement) |
| Supply chain | Chain of custody, GS1 standards | 1970s-2000s |
| Software engineering | Version control (CVS→SVN→Git) | 1986-2005 |
| Scientific publishing | None (document assumption) | — |

Software engineering faced the same problem in the 1990s. Source code was treated as a collection of files transmitted between developers via email, FTP, or shared drives. Every collaboration problem — tracking changes, attributing contributions, managing parallel versions, reverting errors — was solved ad hoc. The solution was not incremental improvement of file-sharing tools. It was a structural reconception: source code is not a collection of files. It is a *repository* — a versioned, branched, contributor-attributed, cryptographically auditable history of every change ever made.

Git [@torvalds-2005-git-fast-version] implemented this reconception. Ram [-@ram-2013-git-can-facilitate] demonstrated that Git can facilitate greater reproducibility and transparency in science; Blischak, Davenport, and Wilson [-@blischak-2016-quick-introduction-version] and Perez-Riverol et al. [-@perezriverol-2016-ten-simple-rules] provided the empirical evidence and practical guidance for Git adoption across scientific disciplines; and Bryan [-@bryan-2018-excuse-me-do] provided the pedagogical bridge — showing working scientists how version control integrates into everyday research practice. Within a decade, Git became the universal infrastructure for collaborative software development. GitHub [-@github-2008-github-social-coding-platform] added the social and collaboration layer: forking, pull requests, issue tracking, and visibility. The combination transformed software from an opaque craft practice into a transparent, auditable, contributor-traceable engineering discipline.

This paper proposes the same structural reconception for scientific research. The reconception produces a four-level hierarchy:

1. A **research program** is a repository — the single source of truth, evolving over time.
2. A **paper** is a render of that repository at a point on its timeline — a frozen snapshot, a communication event.
3. A **submission** is a fork — sharing that render with the community for confirmation.
4. A **publication** is a merge — acceptance of the fork into a journal's curated collection.

A paper is not a document. It is a tagged release from a repository, frozen at a specific stage and forked to a journal for evaluation. The submission process is not a file transfer. It is a fork request. Peer review is not an email exchange. It is a set of attributed commits on a review branch. Publication is not a format conversion. It is a merge into a journal's collection with a minted DOI.

### 1.2 What the Protocol Replaces

The urgency of structural reform is well established. Ioannidis [-@ioannidis-2005-why-most-published] demonstrated that most published research findings are false — a conclusion driven in part by the absence of transparent, auditable research processes. The TOP Guidelines [@nosek-2015-promoting-open-research] defined eight transparency standards for open research culture, but implementing those standards within the current document paradigm remains difficult because the paradigm itself lacks the infrastructure for structured transparency. Empirical work tracking submissions across rejection and acceptance shows that publication-bias signatures emerge before peer review [@brodeur-2023-unpacking-phacking-publication], implying that infrastructure capable of preserving and querying the full submission record — including desk rejections — is necessary for accurate diagnosis of where bias enters.

The current pipeline has five structural gaps that are difficult to address within the document paradigm:

**Gap 1: No version history.** The reproducibility crisis prompted a wave of editorial reform [@mcnutt-2014-reproducibility-science-3436168], yet the underlying infrastructure remains unchanged. Stodden, Seiler, and Ma [-@stodden-2018-empirical-analysis-journal] found that even among journals with explicit reproducibility policies, fewer than 10% of authors provided sufficient materials to reproduce their results — demonstrating that policy without infrastructure fails. A submitted manuscript has no auditable record of how it was written. The editor sees a finished product. The twenty drafts, the deleted sections, the data re-analyses, the contributor who rewrote Section 4 — all invisible. When questions arise about research integrity, the only evidence is the authors' word and whatever files happen to be on their hard drives.

**Gap 2: No contributor traceability.** CRediT (Contributor Roles Taxonomy) added contributor roles to published papers in 2014. But CRediT is a self-reported annotation attached to the final document. It has no connection to the actual work. There is no mechanism to verify that the person listed as "Methodology" actually wrote the methods section. The contribution record is a claim, not a proof.

**Gap 3: No submission provenance.** When an author submits to Journal A, Journal B has no way to know. Dual submission policies rely entirely on author honesty. When a paper is rejected by three journals and accepted by the fourth, the fourth journal's editor has no access to the prior reviews. The same paper is re-reviewed from scratch at each venue — a massive duplication of expert labor.

**Gap 4: No review attribution.** Peer reviewers contribute substantive intellectual work — identifying errors, suggesting improvements, catching methodological flaws. Their contributions are acknowledged in a single generic sentence ("We thank the anonymous reviewers") and then erased. A reviewer who saves a paper from a fatal statistical error receives the same credit as one who submits a two-sentence review: none.

**Gap 5: No machine interface.** The entire pipeline is human-readable only. A PDF cannot be queried, diff'd, branched, or programmatically analyzed without lossy conversion. AI tools that could assist with literature review, consistency checking, or cross-paper analysis must first solve the extraction problem — converting unstructured text back into structured data — before doing any useful work. This is no longer hypothetical: Biswas et al. [-@goldberg-2026-aiassisted-peer-review] deployed AI review at scale across 22,977 AAAI-26 submissions and were forced to apply olmOCR — optical character recognition applied to PDFs — as a preprocessing step precisely because papers lacked machine-readable structure. The repository protocol proposed here eliminates that step: a paper stored as a Git repository with Markdown source and `paper.yaml` is queryable without any format conversion.

The protocol proposed here closes all five gaps by replacing the document assumption with a repository assumption. The paper becomes a Git repository. Submission becomes a fork. Review becomes a branch. Publication becomes a release. Every operation is versioned, attributed, and machine-readable by construction.

### 1.3 Relationship to Prior Work

The Paper Spec standard [@zharnikov-2026m-projection-cascade-why] addresses Gap 5 by defining a machine-readable YAML companion file (`paper.yaml`) that captures what a paper claims, what would falsify those claims, and what the paper depends on. Paper Spec is the *specification layer* — it declares the paper's epistemic content in structured form.

**Paper Spec in brief.** The Paper Spec standard [@zharnikov-2026m-projection-cascade-why] defines a YAML companion file (`paper.yaml`) with five structural elements: (1) typed claims with unique identifiers and dependency links; (2) methodology description with reproducibility requirements; (3) acceptance criteria — what would confirm each claim and, critically, what would falsify it; (4) a dependency graph linking claims to prior work with criticality flags; and (5) submission history tracking venue, decision, and revision scope. The standard is published as an open repository with 20 worked examples from published research (github.com/spectralbranding/paper-spec). The present protocol treats `paper.yaml` as one file in the repository structure; Paper Spec defines its internal schema.

The present protocol is the *process layer* — it specifies how the paper is built, submitted, reviewed, and published. Paper Spec and Research-as-Repository compose: `paper.yaml` travels with the repository, is versioned alongside the manuscript, and is included in every fork. Together, they make both the content and the lifecycle of a paper fully machine-readable.

The Registered Reports format [@chambers-2013-registered-reports-new] addresses the sequence problem by splitting peer review into pre-data and post-data stages. The present protocol subsumes Registered Reports as a special case: a Stage 1 submission is a fork at a specific commit; Stage 2 is a subsequent fork from a later commit in the same repository. The fork chain records the two-stage structure automatically.

DORA [@dora-2013-san-francisco-declaration-research], the Leiden Manifesto [@hicks-2015-bibliometrics-leiden-manifesto], and CoARA [@coara-2022-agreement-reforming-research-assessment] all advocate for multi-dimensional research evaluation. The present protocol provides the infrastructure that makes multi-dimensional evaluation tractable: when every contribution, every review, and every decision is recorded in structured form, evaluation can query specific dimensions rather than collapsing to scalar proxies.

### 1.4 The Value Stream: Knowledge Development as the Core Process

Existing reform proposals — and the platforms that implement them — share a common limitation: they optimize individual stations on the publishing production line without examining the production line itself.

Manubot [@himmelstein-2019-open-collaborative-writing] improves authoring. COAR Notify improves cross-platform notification. ORKG [@auer-2018-towards-open-research] improves indexing. Signposting improves machine discovery. Each addresses one gap — and each optimizes the *paper* (the rendered artifact). Open access optimizes who can read the paper. Preprints optimize when the paper becomes available. Registered reports optimize what sequence the paper follows. JATS XML optimizes the paper's machine-readability.

The present protocol does not optimize the paper. It optimizes the *knowledge production process* that papers communicate. The repository is the research — the evolving SSOT where knowledge is built. Papers are renders of that research at specific stages, shared with the community for confirmation. The distinction is not semantic. When the focus is on optimizing the paper, the result is better documents. When the focus is on optimizing the knowledge process, better papers follow as a structural consequence — just as better brand signals follow from a well-specified brand architecture, rather than the reverse.

None of the existing reforms asks the structural question: *what is the value stream of scientific knowledge production, and which activities on the production line are value-creating versus waste?*

Lean manufacturing [@ohno-1988-toyota-production-system] distinguishes between value-creating activities (those the customer would pay for) and muda (waste — activities that consume resources but do not create value). Applied to scientific publishing:

**Value-creating activities** (the knowledge production process):

- Formulating hypotheses
- Designing experiments and analyses
- Collecting and analyzing data
- Writing arguments and interpretations
- Peer evaluation of claims (the intellectual substance of review)
- Integrating new knowledge into the existing corpus

**Non-value-creating activities** (administrative process around the value stream):

- Formatting manuscripts to journal specifications
- Uploading files through submission portals
- Manually blinding manuscripts
- Re-reviewing papers rejected elsewhere (duplicate expert labor)
- Converting between file formats (LaTeX to DOCX to JATS XML to PDF)
- Tracking submission status through email
- Manually entering metadata into multiple platforms
- Negotiating copyright transfer agreements

In many disciplines and at many journals, the current system routes the value stream *through* the administrative process. A researcher cannot share a finding with the community without first navigating formatting requirements, submission portals, and editorial management systems that were designed for publisher convenience, not knowledge flow. The administrative burden is not adjacent to the value stream — it is woven into it, forcing every knowledge-creating act to pass through non-value-creating checkpoints.

The Research-as-Repository protocol restructures this relationship. The value stream flows continuously in the author's repository: writing, analyzing, versioning, collaborating. The administrative functions — submission, blinding, review assignment, publication, indexing — are *services that operate on the repository* rather than *checkpoints the repository must pass through*. A fork is a service call, not a format conversion. Blinding is a function, not a manual task. Publication is a tag, not a production pipeline.

This reflects a principle well established in process reengineering [@hammer-1993-reengineering-corporation-manifesto] and Lean thinking [@womack-1996-lean-thinking-banish]: specify the process first, then derive the organizational structure from the process — not the other way around. Organizational Schema Theory (OST) formalizes this principle for organizational design [@zharnikov-2026-organizational-schema-theory-test-driven]; the present protocol applies it to scholarly communication. Current scientific publishing derives its processes from its organizational structure (journals define formats, timelines, and workflows; researchers conform). The protocol inverts this: the knowledge development process defines the requirements; journals, preprint servers, and review systems are services that fulfill those requirements.

This inversion shifts the value of journals to a different level. In the document paradigm, the journal is the destination — research culminates in publication. In the repository paradigm, knowledge development is the core process and it continues regardless of any single publication event. A journal publication is not an endpoint but a *peer alignment event*: a synchronization point where the scientific community confirms that a render of the ongoing research is sound at this stage. The research repository existed before the fork and continues after the merge. The journal's role is not to validate the research (that is the community's function) but to curate the alignment — selecting which renders, at which stages, merit community attention. Publications are important, but they are instruments of peer alignment, not the core process itself.

### 1.5 Related Work

Several platforms and standards address subsets of the gaps identified above. None integrates all five into a unified protocol.

Table 2a: Protocol feature coverage. Columns indicate whether a system supports each of the six protocol features described in Section 1.2. Full = structurally integrated; Partial = addressed but not fully integrated; No = not addressed.

| System | VC | Fork | Gate | Rev | Prov | Coll |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|
| Manubot [@himmelstein-2019-open-collaborative-writing] | Full | -- | -- | -- | -- | -- |
| JOSS [@smith-2018-journal-open-source] | Full | Partial | Partial | Full | -- | -- |
| Octopus.ac [@freeman-2021-octopus-new-approach] | Partial | -- | -- | Full | Partial | -- |
| OJS/PKP [@willinsky-2005-open-journal-systems] | -- | -- | Partial | -- | -- | -- |
| COAR Notify | -- | -- | -- | -- | Partial | Partial |
| Signposting | -- | -- | -- | -- | -- | Partial |
| CryptSubmit [@gipp-2015-decentralized-trusted-timestamping] | -- | -- | -- | -- | Full | -- |
| PubPub (MIT Media Lab) [@pubpub-2017-pubpub-open-publishing-platform] | Partial | -- | -- | -- | Partial | -- |
| eLife [@eisen-2020-implementing-publish-then] | -- | -- | -- | Partial | -- | Partial |
| RO-Crate [@soilandreyes-2022-packaging-research-artefacts] | -- | -- | Partial | -- | -- | Partial |
| FAIR4RS [@barker-2022-introducing-fair-principles] | -- | -- | -- | -- | -- | -- |
| DataCite | -- | -- | -- | -- | -- | Partial |
| **This protocol** | **Full** | **Full** | **Full** | **Full** | **Full** | **Full** |

Column key: VC = version control, Fork = fork-based submission, Gate = compliance gate, Rev = reviewer attribution, Prov = provenance chain, Coll = collections as users. Dashes indicate the feature is absent.

Table 2b: System context and adoption.

| System | Adoption | Key limitation |
|--------|----------|----------------|
| Manubot | ~500 papers | Authoring only, no submission/review |
| JOSS | ~3,000 papers | Software papers only |
| Octopus.ac | Pilot (2022-) | Proprietary platform, not Git-native |
| OJS/PKP | 25,000+ journals | No version control, no structured review |
| COAR Notify | Pilot (2023-) | Notification only, no manuscript management |
| CryptSubmit | Prototype, 2015 | Timestamping only, no full lifecycle |
| PubPub | ~200 communities | Web-native, not Git-native |
| eLife | Active (2020-) | Platform-specific, not protocol-native |
| RO-Crate | Growing adoption | Packages artifacts, not processes |
| This protocol | Proposal | Partial prototype: compliance gate, schemas, validator, self-referential implementation (github.com/spectralbranding/paper-repo). Fork lifecycle and federation: conceptual |

The table reveals a structural distinction. RO-Crate packages research artifacts (data, code, documents) with rich metadata into a standardized container — it is preservation-focused. FAIR4RS extends the FAIR principles [@wilkinson-2016-fair-guiding-principles] to research software, defining machine-readable metadata requirements for findability, accessibility, interoperability, and reusability. DataCite [@datacite-2024-datacite-metadata-schema] provides DOI minting and metadata standards for research data. These standards focus on *artifacts* — the outputs of research. The present protocol focuses on the *process* — how those artifacts are authored, submitted, reviewed, and decided upon. The two concerns are complementary: an RO-Crate can package a paper repository's artifacts; FAIR4RS principles inform how the repository's code and scripts are documented; DataCite-compatible DOIs are minted for releases and forks. The protocol inherits these standards rather than replacing them.

eLife's "Publish, then Review" model [@eisen-2020-implementing-publish-then] is the closest real-world implementation of the "collections as users" concept: authors post preprints first, and eLife curates reviewed preprints into its collection with public reviews attached. The model demonstrates that decoupling publication from review is operationally viable — but it remains platform-specific rather than protocol-native. The present protocol generalizes this pattern: any collection user can curate any repository fork, with review records that are portable across venues.

Manubot is the closest predecessor for the authoring layer — it implements Git-native collaborative writing with CI/CD rendering [@himmelstein-2019-open-collaborative-writing]. The present protocol extends this pattern from authoring to the full submission-review-publication lifecycle. JOSS implements review-as-GitHub-issues for software papers; the present protocol generalizes this to all disciplines with structured reviewer commits rather than free-form issue comments. Octopus decomposes papers into modular linked units with open review — sharing the modular philosophy but using a proprietary platform rather than Git repositories. Overlay journals (e.g., Discrete Analysis on arXiv) already implement a lightweight version of "collections as users" by curating papers hosted on preprint servers.

The protocol's contribution is not any single feature but the integration: a unified Git-native lifecycle where authoring, compliance, submission, blinding, review, provenance, and publication are operations on a single versioned repository.

The contribution of this paper is threefold. First, it provides a structural diagnosis: scientific publishing is the only knowledge-intensive domain without version control and provenance infrastructure, a gap visible when compared with legal, financial, clinical, supply-chain, and software domains that each independently developed formal provenance systems. Second, it proposes a concrete reconception — treating research programs as versioned repositories — that closes five persistent structural gaps simultaneously, without replacing peer review or mandating centralized platforms. Third, the protocol is incrementally adoptable: Tier 1 (local Git) delivers immediate value to an individual researcher with no institutional coordination; the full protocol benefits materialize as journals and preprint servers join the federation.

### 1.6 Claims

This paper advances seven claims:

1. **C1.** Fork-based submission creates cryptographic provenance that makes submission history structurally auditable.
2. **C2.** Blinding-as-function replaces manual anonymization with a configurable system property.
3. **C3.** Review-as-commits creates attributed, portable review records with measurable depth.
4. **C4.** Collections-as-users unifies preprint servers, journals, and archives under a single protocol.
5. **C5.** A compliance gate (`journal_spec.yaml`) substantially reduces formatting-related desk rejections.
6. **C6.** Provenance-by-design makes dual submission structurally detectable.
7. **C7.** The protocol's machine-readable structure enables structured querying across the full research lifecycle, including AI-assisted cross-paper analysis.

Each claim includes a falsification condition specified in the accompanying `paper.yaml`.

---

## 2. The Protocol

The four-level hierarchy (Figure 1) is the central architectural claim of this paper. Each level is a structural transformation of the level above, preserving cryptographic provenance throughout.

```{=typst}
#block(breakable: false)[
```

```{.mermaid width="100%"}
flowchart LR
    R[Research program<br/>= versioned repository]
    P[Paper<br/>= tagged render of repo at commit C]
    S[Submission<br/>= fork of repo at commit C]
    J[Journal / preprint server<br/>= curated collection of forks]
    R -->|tag v1.0| P
    P -->|fork at C| S
    S -->|merge / accept| J
    J -.->|metadata back to repo| R
```

Figure 1: The four-level Research-as-Repository hierarchy. Each level is a structural transformation of the level above, preserving cryptographic provenance. The dashed line shows publication metadata flowing back to the source repository, closing the loop and supporting the rendering-isomorphism (§3.4).

```{=typst}
]
```

The protocol maps the scientific publishing lifecycle onto a CI/CD (Continuous Integration / Continuous Delivery) pipeline — the same architecture that transformed software from artisanal craft to engineered discipline. In software CI/CD, every code change triggers automated validation, testing, and deployment. In the paper protocol, every stage of the knowledge lifecycle triggers analogous automated operations:

```
AUTHOR REPO (Continuous Integration)
    |
    |-- commit: writing, analysis, revision
    |   → CI: paper.yaml schema validation
    |   → CI: reference completeness check
    |   → CI: figure quality verification
    |   → CI: internal consistency (claims match data)
    |
    |-- fork request to journal (Delivery Gate)
    |   → GATE: journal_spec.yaml compliance
    |   → GATE: blinding automation
    |   → GATE: provenance chain verification
    |   → GATE: AI pre-submission advisory (scope, novelty, coverage)
    |   |
    |   PASS → fork created, enters review pipeline
    |   FAIL → author sees exact failures, fixes locally, retries
    |
    |-- review pipeline (Continuous Review)
    |   → reviewer branches created
    |   → commits: structured review comments
    |   → editorial merge: decision commit
    |
    |-- acceptance (Release)
    |   → tagged release with DOI
    |   → badge from journal collection
    |   → provenance record closed
    |   → AI-native index updated (ORKG, Semantic Scholar)
    |
    |-- post-publication (Continuous Monitoring)
        → dependency alerts (cited paper retracted/updated)
        → correction commits (errata as patches)
        → community forks (post-publication review)
```

Each stage has automated checks (the CI), human judgment points (the review), and structural artifacts (the provenance chain). The protocol does not automate science — it automates a significant fraction of the administrative overhead that currently consumes editorial and author labor, so that human attention is reserved for the intellectual work that only humans can do.

### 2.1 The Research Repository

The protocol's fundamental unit is the **research repository** — a versioned history of a research program that may produce one or many papers over its lifetime. A researcher working on a single core idea for years maintains one repository; each paper is a **tagged release** — a frozen snapshot of the research at a specific stage of development, forked to a journal for review.

This mirrors how software projects operate: one repository, many releases. A paper is not a separate project — it is a milestone in the research trajectory. Two papers from the same repository share commit ancestry, making their relationship structurally visible (not just declared via citations). This also makes "salami slicing" — splitting one study into artificially separate publications — structurally detectable, since the common ancestry and overlapping content are visible in the diff history.

The simplest case is a single-paper repository, which has the following structure:

```
paper/
  paper.md              # Manuscript (Markdown SSOT)
  paper.yaml            # Paper Spec (claims, methods, dependencies)
  data/                 # Data files, analysis scripts
  figures/              # Generated figures
  CONTRIBUTORS.yaml     # Contributor roles (verified, not self-reported)
  PROVENANCE.yaml       # Fork history, submission records
  LICENSE               # Content license
  .paperrc              # Repository configuration
```

A multi-paper research repository extends this pattern:

```
research-program/
  papers/
    paper-01/             # First paper (e.g., foundational framework)
      paper.md
      paper.yaml
    paper-02/             # Second paper (e.g., mathematical extension)
      paper.md
      paper.yaml
    paper-03/             # Third paper (e.g., empirical validation)
      paper.md
      paper.yaml
  shared/
    data/                 # Shared data and analysis
    figures/              # Shared figures
  CONTRIBUTORS.yaml       # Links to researcher profiles
  FUNDING.yaml            # Grant timeline scoped to commits
  ACKNOWLEDGMENTS.md      # Version-controlled
  PROVENANCE.yaml         # Fork history (one per paper per venue)
  LICENSE
```

Each paper's `paper.yaml` declares dependencies on other papers in the same repository (via relative paths) and on external work (via DOIs). Fork requests are scoped to a specific paper directory — the journal receives only that paper's content, but the fork carries the full repository's provenance chain.

The branch structure of the research repository naturally visualizes the intellectual genealogy of the research program:

```
main (core thesis: multi-dimensional brand perception)
  │
  ├── tag: paper-01 → fork → Journal A    (foundational framework)
  │
  ├── branch: mathematical-foundations
  │     ├── tag: paper-02 → fork → Journal B    (formal metric)
  │     ├── tag: paper-03 → fork → Journal C    (projection bounds)
  │     └── tag: paper-04 → fork → Journal D    (capacity analysis)
  │
  ├── branch: empirical-validation
  │     ├── tag: paper-05 → fork → Journal E    (longitudinal case study)
  │     └── (in progress — not yet tagged)
  │
  ├── branch: cross-domain
  │     ├── tag: paper-06 → fork → Journal F    (applied to org design)
  │     └── tag: paper-07 → fork → Journal G    (applied to publishing)
  │
  └── branch: methodology
        └── tag: paper-08 → fork → Journal H    (measurement instrument)
```

The main branch carries the core thesis; topic branches represent sub-ideas being explored; tags mark papers — communication events where findings are shared with the community for confirmation. A reader can inspect the commit graph and see which ideas branched from which, which were abandoned, and which converged — the tree of supportive sub-ideas that constitutes the research program's structure. This is information that no sequence of PDFs can convey.

The manuscript (`paper.md`) is the single source of truth. All renderings are generated from it: structurally meaningful outputs (JATS XML for indexing, HTML for web display) and legacy compatibility outputs (PDF, DOCX) that serve readers and venues not yet operating on the repository directly. The repository contains the generating function, not the rendered output. Software tools used in the analysis are cited following the FORCE11 software citation principles [@smith-2016-software-citation-principles], with version, DOI, and repository URL recorded in `paper.yaml` dependencies.

The protocol does not mandate Markdown specifically. Any plain-text, diff-friendly format serves as the SSOT: Markdown, LaTeX, Quarto, or R Markdown. The essential requirement is that the source format is version-controllable (plain text, not binary) and renderable to multiple outputs. Fields that predominantly use LaTeX (physics, mathematics) or Word (biomedical, humanities) would require either format bridging tools or a GUI abstraction layer that presents the Git operations through a familiar editing interface — analogous to how GitHub Desktop made Git accessible to non-engineers.

JATS XML (Journal Article Tag Suite) is the dominant machine-readable format for published articles. The protocol does not replace JATS — it generates JATS as one rendering output from the repository source. The submission gate (Section 2.3) can include JATS validation as a compliance check. The relationship is: the repository stores the source; JATS is one of several delivery formats the CI pipeline produces.

**The two-layer architecture: text in Git, data in archives.** Scientific papers across all disciplines produce two categories of artifacts: text-based artifacts (manuscripts, code, analysis scripts, small structured data) and binary/large artifacts (microscopy images, genomic sequences, medical imaging, satellite data, audio recordings, simulation outputs). This distinction reflects Borgman's [-@borgman-2015-big-data-little] compound knowledge object framework, in which a research output is a bundle of heterogeneous artifacts linked by shared provenance rather than a single monolithic document — a structure that also enables the kind of data reuse that researchers find most valuable when provenance is preserved [@pasquetto-2019-uses-reuses-scientific]. Git handles the first category natively. It handles the second category poorly — storing full copies of every version of every binary file makes repositories impractically large.

The protocol adopts the same architecture that software engineering uses for code and assets: the repository stores the text layer; large data lives in linked external archives.

```
Paper repository (Git — text layer)
    paper.md / paper.tex         Manuscript source
    paper.yaml                   Claims, methods, dependencies
    analysis/                    Code, scripts, notebooks
    figures/                     Generated figures (SVG, small PNG)
    CONTRIBUTORS.yaml            Contributor roles
    PROVENANCE.yaml              Fork history
    DATA_MANIFEST.yaml           Links to external data

External data archives (linked by DOI)
    Zenodo, Dryad, Figshare      General-purpose
    GenBank                      Genomic sequences
    PDB                          Protein structures
    EMPIAR                       Cryo-EM maps
    Dataverse                    Social science datasets
    PANGAEA                      Earth science data
```

`DATA_MANIFEST.yaml` in the repository declares every external data dependency with its DOI, checksum, and access conditions — extending Altman and King's [-@altman-2007-proposed-standard-scholarly] proposed standard for scholarly citation of quantitative data from a citation convention to a machine-enforceable dependency:

```yaml
data_manifest:
  - id: "microscopy-dataset"
    description: "Confocal microscopy images, 47 samples"
    archive: "Zenodo"
    doi: "10.5281/zenodo.XXXXXXX"
    size_gb: 12.4
    format: "TIFF (16-bit, 2048x2048)"
    checksum_sha256: "a1b2c3..."
    access: public

  - id: "patient-records"
    description: "De-identified clinical trial data, N=340"
    archive: "Dryad"
    doi: "10.5061/dryad.XXXXXXX"
    size_gb: 0.3
    format: "CSV"
    checksum_sha256: "d4e5f6..."
    access: restricted    # requires DUA
```

This separation is not a limitation of the protocol — it is the correct architecture. The Zenodo-GitHub integration already implements this pattern: code in GitHub, data in Zenodo, linked by DOI. The protocol formalizes the linkage with checksums and access metadata so that the data manifest is part of the reproducibility chain.

For figures, the protocol favors generated figures: analysis scripts in the repository produce figures from data at build time, the same way CI/CD generates build artifacts from source code. A figure that is generated from a script in the repository is reproducible by construction. A figure that is a binary file in the repository is reproducible only if the reader trusts that it matches the claimed analysis. Fields where figures must be hand-drawn or photographed (art history, field biology, clinical medicine) store the figure files directly — Git handles moderate-sized images (under ~10MB each) adequately, and Git LFS extends this to larger files when needed.

**CONTRIBUTORS.yaml** records every person who contributed to the repository, verified by their commit history:

```yaml
contributors:
  - name: "Alice Chen"
    orcid: "0000-0001-2345-6789"
    roles: [conceptualization, methodology, writing-original]
    commits: 847
    first_commit: 2025-06-15
    last_commit: 2026-03-20

  - name: "Bob Martinez"
    orcid: "0000-0002-3456-7890"
    roles: [data-curation, formal-analysis]
    commits: 312
    first_commit: 2025-09-01
    last_commit: 2026-02-14

  - name: "Claude (Anthropic)"
    type: ai_tool
    roles: [writing-review, consistency-checking]
    commits: 0  # AI contributions tracked via author commits
    disclosure: "Used for manuscript preparation and mathematical verification"
```

Roles follow CRediT taxonomy but are *verified against commit history*: a contributor listed as "Methodology" must have commits touching the methods section. The verification can be automated.

### 2.2 Fork-Based Submission and the Hybrid Flow

*Terminological note.* "Submission" is legacy terminology retained throughout this paper for readability. The protocol-native term is "fork request" — the author requests that a journal fork their repository at a specific commit. Similarly, "manuscript" refers to the rendered output of a repository; the protocol's primary object is the fork itself.

The protocol's design is git-native: the author links their research repository to the submission portal, the portal creates a fork scoped to the specific paper directory, and the compliance gate runs automatically. This is the target architecture. During a transition period, existing portals will also accept traditional file uploads (.docx/.pdf) as a **transitional compatibility mode** — outside the protocol's architecture, serving authors and journals not yet operating in the git-native workflow.

**Git-native flow** (protocol design): Author links their research repository to the submission portal — the same way ORCID accounts are linked today. The portal handles metadata (manuscript type, keywords, suggested reviewers, cover letter). The repository handles the manuscript. On submission, the portal creates a fork from the linked repository and runs the compliance gate.

**Traditional flow** (transitional compatibility): Author uploads .docx/.pdf through ScholarOne, Editorial Manager, or OJS. The portal handles metadata. This mode persists during adoption but operates outside the protocol — no fork is created, no provenance is recorded, no compliance gate runs. As adoption spreads, this pathway becomes redundant.

```
ScholarOne / Editorial Manager / OJS
    |
    |-- Step 1: Author fills metadata form (unchanged)
    |-- Step 2: Author either:
    |   (a) links git repo + selects commit [git-native]  OR
    |   (b) uploads .docx/.pdf [transitional compatibility]
    |
    |-- Step 3 (git-native only):
    |   Portal creates fork → runs journal_spec validation
    |   If PASS: submission completes
    |   If FAIL: author sees failures, fixes locally, retries
    |
    |-- Step 4: Editor receives manuscript
    |   Git-native: editor operates on the fork — full version
    |     history, contributor data, provenance, diff capability
    |   Transitional: editor receives a rendered document without
    |     structural metadata or provenance
```

*Architecture of the fork-based submission lifecycle.*

```
Research Repository (author)
    |
    |-- fork request -->  Journal Fork (frozen)
    |                        |
    |                        |-- review branch (Reviewer 1)
    |                        |-- review branch (Reviewer 2)
    |                        |
    |                        |-- editorial decision
    |                        |       |
    |                  [merge into collection] or [close fork]
    |
    |-- fork request -->  Preprint Collection (Zenodo)
    |                        |
    |                  [merged -- DOI minted]
    |
    |-- continue working on main branch
    |
    |-- tag: paper-02 (next paper)
```

The research repository is the SSOT; forks are frozen snapshots owned by the receiving venue. Review branches are attributed to individual reviewers. The editorial decision either merges the fork into the journal's collection or closes it.

This hybrid approach has three adoption advantages. First, it piggybacks on existing OAuth infrastructure (if ScholarOne can link an ORCID, it can link a GitHub account). Second, the transitional pathway means no journal is forced to adopt the protocol immediately — but the structural advantages of the git-native flow (provenance, compliance automation, contributor traceability) create migration pressure over time. Third, the git-native flow gives editors capabilities the traditional flow cannot: version history, contributor verification, and structured review branches. These advantages, not mandates, drive the transition.

For journals that support the git-linked flow, submitting a paper creates a **fork** — a frozen, cryptographically linked snapshot of the repository at a specific commit.

```
AUTHOR REPO                          JOURNAL FORK
    |                                     |
    |--- commit a1b2c3 ----[fork]-------> |  frozen at a1b2c3
    |                                     |  owned by editor
    |    (author continues working)       |  author cannot modify
    |                                     |
```

The fork operation:

1. **Creates** a read-only copy of the repository at the specified commit
2. **Transfers ownership** to the journal editor
3. **Records** the fork in the author's `PROVENANCE.yaml` (irrevocable)
4. **Strips** or anonymizes contributor identities per the journal's blinding policy
5. **Grants the journal access** to the fork as a Git repository, enabling editors and reviewers to operate directly on the versioned source — reviewing diffs, commenting on commits, and making attributed edits on review branches. The fork itself — not a rendered export — is the primary object of editorial work, preserving full traceability throughout the review process. (During the transition period, the CI pipeline can generate rendered outputs — PDF, DOCX — for journals not yet operating in the git-native workflow.)

The author **cannot modify** the fork after creation. They can:

- **Revoke** the fork (withdrawing the submission) — the revocation is recorded in provenance
- **Continue working** on their main branch — the fork is a snapshot, not a lock
- **Create additional forks** to other journals — but each new fork carries the full provenance chain, making the existing fork visible

### 2.3 The Submission Gate: Compliance as CI/CD

In the current system, a significant fraction of editorial labor is consumed by non-compliant submissions. Manuscripts arrive with wrong fonts, incorrect reference styles, figures at inadequate resolution, abstracts exceeding word limits, and missing ethics declarations. Editors desk-reject or return these papers, wasting both editorial time and author time. The author reformats and resubmits — sometimes multiple rounds — before the paper ever reaches a reviewer. This is administrative overhead (muda in lean terminology): labor that creates no knowledge.

In the repository protocol, each journal publishes a **submission specification** — a machine-readable document that defines its compliance requirements:

```yaml
# journal_spec.yaml — published by the journal, readable by the author's toolchain
journal:
  name: "Journal of Marketing"
  submission_spec_version: "2026.1"

manuscript:
  format: markdown              # source format
  word_count:
    min: 5000
    max: 12000
    includes: [body]
    excludes: [abstract, references, appendices, tables, figure_captions]
  abstract:
    max_words: 200
    structure: null              # null = flowing | structured = IMRaD headings
  keywords:
    min: 4
    max: 6
  sections_required: [introduction, literature_review, methodology, results, discussion, conclusion]

references:
  style: apa7
  self_citation_max_percent: 25
  min_count: 20
  doi_required: true            # every reference must have a DOI or URL

figures:
  format: [png, svg, tiff]
  min_dpi: 300
  max_file_size_mb: 10
  color_mode: [rgb, cmyk]       # grayscale required for print? specify here
  captions_required: true

tables:
  format: [csv, markdown]       # no embedded Excel
  max_count: 10

ethics:
  ai_disclosure_required: true
  data_availability_required: true
  conflict_of_interest_required: true
  funding_statement_required: true

blinding:
  mode: double-blind
  # ... (detailed blinding config as in Section 2.4)

review:
  type: double-blind            # double-blind | single-blind | open
  suggested_reviewers:
    min: 3
    max: 5
  cover_letter_required: true
```

**The fork operation runs the spec as a validation pipeline before the fork is accepted.** This is the CI/CD model applied to paper submission:

```
AUTHOR REPO
    |
    |--- author requests fork to "Journal of Marketing"
    |
    |--- GATE: journal_spec.yaml validation runs locally
    |    |
    |    |-- [CHECK] Word count: 9,217 ✓ (within 5,000-12,000)
    |    |-- [CHECK] Abstract: 187 words ✓ (≤200)
    |    |-- [CHECK] Keywords: 5 ✓ (4-6)
    |    |-- [CHECK] References: 42, all with DOIs ✓
    |    |-- [CHECK] Self-citation: 19% ✓ (≤25%)
    |    |-- [CHECK] Figures: 3 PNG, all 300+ DPI ✓
    |    |-- [CHECK] AI disclosure: present ✓
    |    |-- [CHECK] Data availability: present ✓
    |    |-- [CHECK] Cover letter: present ✓
    |    |-- [CHECK] paper.yaml: valid schema ✓
    |    |
    |    ALL CHECKS PASSED → fork created
    |
    |--- JOURNAL FORK (compliant by construction)
```

If any check fails, the fork is **not created**. The author sees exactly which requirements are unmet, fixes them in their repository, and retries. The email exchange, desk rejection, and reformatting cycle is substantially reduced — eliminated entirely for formatting-related causes within the protocol. The journal fork is compliant by construction.

**This inverts the current compliance model.** Currently:

1. Author guesses at formatting requirements from a 15-page "Instructions for Authors" PDF
2. Author manually formats the manuscript
3. Author submits
4. Editorial assistant checks compliance (days to weeks)
5. Paper returned for formatting fixes (another round trip)
6. Author reformats, resubmits
7. Eventually reaches editor for substantive evaluation

In the repository protocol:

1. Journal publishes `journal_spec.yaml` (machine-readable, unambiguous)
2. Author runs `paper validate --spec journal_spec.yaml` locally
3. All failures shown instantly with exact fix instructions
4. Author fixes in their repo, re-runs validation
5. When all checks pass, fork is created — paper arrives at editor fully compliant

**The author-facing pre-submission layer.** The validation pipeline can include optional AI-assisted checks that run before the gate:

```yaml
# Optional pre-submission AI checks (author-facing, advisory only)
pre_submission:
  scope_check:
    enabled: true
    description: "Does this paper match the journal's stated scope?"
    method: "Compare paper.yaml claims against journal's published topic list"
    blocking: false   # advisory — author decides

  novelty_signal:
    enabled: true
    description: "How does this paper relate to recent publications in this journal?"
    method: "Compare paper.yaml claims against last 2 years of journal's published papers"
    blocking: false

  reference_coverage:
    enabled: true
    description: "Are key works in this field cited?"
    method: "Check paper.yaml dependencies against known citation graphs"
    blocking: false

  statistical_review:
    enabled: true
    description: "Are sample sizes, tests, and effect sizes reported per journal standards?"
    method: "Parse methodology section for reporting completeness"
    blocking: false
```

These AI checks are **advisory, not blocking**. They help the author assess fit before investing in the submission. A researcher can see: "Your paper's claims overlap 72% with Journal X's scope but only 31% with Journal Y's — consider submitting to X first." This replaces the current guesswork of reading "Instructions for Authors" and hoping.

**Implementability.** Every check in the gate is technically straightforward:

Table 3: Compliance gate checks and implementation difficulty.

| Check | Implementation | Difficulty |
|---|---|---|
| Word count | Parse Markdown, count tokens by section | Trivial |
| Abstract length | Parse frontmatter or delimited section | Trivial |
| Reference style | Lint against CSL style definition (CSL already exists for every major style) | Moderate — CSL libraries exist |
| Figure format/DPI | Read image metadata (Pillow, ImageMagick) | Trivial |
| Self-citation ratio | Count author-name matches in reference list | Easy |
| DOI completeness | Check each reference for DOI field | Easy |
| AI disclosure presence | Check for required section heading or YAML field | Trivial |
| Scope matching (AI) | Embed paper abstract + journal scope, compute similarity | Moderate — embedding models exist |
| Reference coverage (AI) | Compare citation list against field's citation graph | Moderate — Semantic Scholar API |
| Statistical reporting (AI) | Parse methods section for reporting standards | Hard — but tools like statcheck exist |

The hard checks (scope matching, reference coverage, statistical reporting) are advisory and optional. The blocking checks are all automatable with existing tools. No new AI research is needed — only integration.

**Consequences.** When every submission arrives fully compliant:

- **Editors** spend zero time on formatting desk rejections — 100% of their time goes to substantive evaluation
- **Authors** never wait weeks to learn their margins were wrong — they know in seconds
- **Reviewers** never receive papers missing basic elements — every paper has all required sections, disclosures, and metadata
- **The system** eliminates an entire class of muda: the formatting-rejection-resubmission cycle

This is the specification principle: what can be specified should be automated. Human judgment is reserved for what cannot be specified — the intellectual evaluation of the paper's contribution.

### 2.4 Blinding as a System Function

Current blinding requires authors to manually remove their names, anonymize self-citations, and hope that no identifying information leaks through. This is error-prone, labor-intensive, and structurally unverifiable.

In the repository protocol, blinding is a **configurable system function** applied to the fork at creation time. The journal specifies its blinding policy as a parameter:

```yaml
# Journal configuration
blinding:
  mode: double-blind          # single-blind | double-blind | open
  strip_author_names: true
  strip_affiliations: true
  strip_orcids: true
  strip_acknowledgments: true
  preserve_roles: true         # "Author 1 (methodology, formal analysis)"
  anonymize_self_citations: true
  strip_figure_metadata: true  # EXIF data, embedded author info
  strip_funding_sources: false # some journals require this visible
```

The system applies these rules automatically when generating the reviewer-facing version of the fork. The original fork retains all identity information (for the editor's use); the reviewer-facing view is a projection that suppresses the specified fields.

This offers several structural advantages over manual blinding:

- **Complete**: every field is covered, including figure metadata, code comments, and embedded document properties that authors routinely forget
- **Configurable**: different journals apply different policies without requiring authors to re-blind for each venue
- **Verifiable**: the blinding function is deterministic and auditable — an author cannot "accidentally" leave identifying information visible
- **Reversible**: after the review decision, the editor can lift the blind selectively (e.g., revealing author identity to reviewers who request it post-decision)

### 2.5 Review as Attributed Commits

The editor creates a **review branch** for each reviewer on the journal fork:

```
JOURNAL FORK
    |
    |--- main (frozen manuscript)
    |
    |--- review/reviewer-1
    |    |-- commit: "Section 3 methodology critique" (2026-04-01)
    |    |-- commit: "Statistical test recommendation" (2026-04-01)
    |    |-- commit: "Minor: typos and formatting" (2026-04-02)
    |    └-- commit: "RECOMMENDATION: major revision" (2026-04-05)
    |
    |--- review/reviewer-2
    |    |-- commit: "Theoretical framework assessment" (2026-04-03)
    |    └-- commit: "RECOMMENDATION: accept with minor" (2026-04-07)
    |
    └--- editorial/decision
         └-- commit: "DECISION: revise and resubmit" (2026-04-10)
```

Each reviewer's branch is a complete, timestamped, attributed record of their review. The commit history shows:

- **When** the reviewer worked (timestamps)
- **What** they reviewed (which sections, which claims)
- **How deeply** they engaged (number of commits, lines of commentary)
- **What they recommended** (final commit on the branch)

The protocol supports all modes identified in Ross-Hellauer's [-@rosshellauer-2017-what-is-open] systematic taxonomy of open peer review, updated evidence on adoption and efficacy documented in Ross-Hellauer and Horbach [-@rosshellauer-2024-additional-experiments-required], and the structured commit model accommodates the emergent innovations catalogued by Tennant et al. [-@tennant-2017-multidisciplinary-perspective-emergent]. The reviewer's identity on the branch is controlled by the editor:

- **Open review**: real name and ORCID visible
- **Single-blind**: reviewer identity visible to editor only; authors see "Reviewer 1"
- **Pseudonymous**: reviewer has a persistent pseudonym across reviews at this journal

### 2.6 Reviewer Ownership and Portable Review History

A reviewer's account belongs to the reviewer, not the journal. When a reviewer completes a review, their branch on the journal fork is linked to their personal profile. Over time, the reviewer accumulates a **review portfolio**:

```yaml
# Reviewer profile (owned by reviewer, not journal)
review_history:
  total_reviews: 47
  journals: ["Nature", "Science", "PNAS", "JM", "QSS"]
  avg_depth: 12.3 commits per review
  specializations: [methodology, statistics, theory]

  # Individual reviews — visibility controlled by reviewer
  reviews:
    - journal: "Nature"
      year: 2026
      decision: "accept"
      depth: 18 commits
      visible: true     # reviewer chose to make this public

    - journal: "JM"
      year: 2026
      decision: "reject"
      depth: 7 commits
      visible: false    # reviewer chose to keep private
```

The reviewer controls which individual reviews are public, but aggregate statistics (total count, average depth, journal list) are always visible. Early evidence suggests that open reviewer identification does not reduce review quality [@vanrooyen-1999-effect-open-peer-review]. This creates verifiable review reputation without requiring full transparency.

**Consequences for reviewer incentives:**

- **Depth is measurable**: A reviewer who writes 18 commits of substantive critique is visibly different from one who writes 2 commits of vague praise
- **Quality is portable**: A reviewer's track record follows them across journals — a strong review history at Nature signals credibility to QSS
- **Credit is structural**: Hiring committees and grant panels can query a candidate's review portfolio alongside their publication record
- **Accountability is implicit**: A reviewer who consistently gives superficial reviews has a visible pattern — not because anyone punished them, but because the data structure records it

### 2.7 Provenance by Design

Every fork creates an irrevocable record in the author's `PROVENANCE.yaml`:

```yaml
provenance:
  forks:
    - id: "fork-001"
      target: "Journal of Marketing"
      target_type: journal
      created: 2026-03-20T14:00:00Z
      source_commit: a3f7c2e
      status: closed          # active | closed | revoked (legacy: "returned")
      outcome: not_merged     # merged | not_merged (legacy: "accepted" / "rejected")
      closed_date: 2026-03-28
      decision_public: false  # author controls visibility
      reviewers: 3
      review_depth: 847       # total comment lines

    - id: "fork-002"
      target: "Journal of Advertising Research"
      target_type: journal
      created: 2026-04-05T10:00:00Z
      source_commit: b4e8d3f  # different commit — paper was revised
      status: active
      outcome: null
      prior_forks_visible: true  # JAR editor can see fork-001 exists
```

**Critical property**: The `forks` list is append-only. An author cannot delete a fork record. This means:

1. **Dual submission becomes structurally detectable within the protocol.** If fork-001 has `status: active`, any new fork carries this information. The receiving editor sees that another fork is active.

2. **Rejection history is optionally transparent.** The *existence* of fork-001 is always visible to subsequent fork recipients. The *decision* (rejected) is visible only if the author sets `decision_public: true`. An author can reveal their rejection history to demonstrate thoroughness, or keep it private.

3. **Review labor is preserved.** When a paper moves from Journal A (rejected) to Journal B, Journal B's editor can see that three reviewers spent 847 lines of commentary on the paper. The editor can (with author consent and reviewer consent) request access to those reviews — reducing duplicate labor. This requires a three-way consent protocol: author agrees to share, original editor agrees to release, and original reviewers agree to transfer their reviews.

### 2.8 Collections as Users

Among the more consequential architectural implications: if every paper is a repository, then preprint servers, journals, and institutional archives are not platforms — they are **users** on a shared platform who curate collections of frozen forks.

```
AUTHOR REPO (the paper)
    |
    |-- fork → "arXiv" user → accepted into arXiv collection
    |   (paper receives arXiv badge + arXiv ID)
    |
    |-- fork → "Zenodo" user → accepted into Zenodo community
    |   (paper receives DOI)
    |
    |-- fork → "Nature" user → enters review workflow
    |   (if accepted: paper receives Nature badge + DOI)
    |
    |-- fork → "MIT Libraries" user → accepted into institutional repo
    |   (paper receives handle)
```

In this architecture:

- **arXiv** is a user account that accepts forks into its collection. Curation criteria: formatting compliance, subject classification, basic quality check. The paper gets an arXiv ID badge.
- **Zenodo** is a user account that accepts forks and mints DOIs. Curation criteria: metadata completeness.
- **Nature** is a user account that curates forks through editorial review. Forks that pass review are merged into the collection and receive a Nature badge + DOI; forks that do not pass are closed without merge.
- **SSRN** is a user account that curates working paper collections.

The paper exists once. It lives in the author's repository. Preprint servers, journals, and archives hold frozen forks — snapshots at specific commits, curated into collections with different acceptance criteria and different badges.

This eliminates:

- **Format conversion**: the repository generates whatever output each collection requires
- **Multiple uploads**: fork once, accepted into collection
- **Version fragmentation**: the author's repo is the SSOT; every collection holds a linked snapshot
- **Access barriers**: arXiv endorsement, SSRN account approval, journal submission portals — all replaced by fork requests that carry verifiable provenance

### 2.9 Funding, Affiliations, and Provenance Metadata

Three categories of metadata shape how a paper is credited, acknowledged, and governed — and the current system conflates all three into free-text fields on a submission form. The repository protocol separates them structurally: affiliations belong to the *person*, funding belongs to the *project*, and authorship records belong to the *paper*. Each has its own lifecycle, its own source of truth, and its own verification mechanism.

**Funding as structural metadata.** A research program accumulates funding over time — grants begin and end, overlap, and attach to different stages of the work. `FUNDING.yaml` records this timeline, with each grant entry scoped to a commit range or set of tagged paper releases:

```yaml
funding:
  - funder: "National Science Foundation"
    funder_id: "https://ror.org/021nxhr62"
    grant_id: "NSF-2025-001"
    period: "2025-01 / 2026-06"
    scope_papers: ["paper-01", "paper-02"]
    conditions:
      open_access: required
      data_sharing: required
    verified: true

  - funder: null
    period: "2024-01 / 2024-12"
    note: "Self-funded initial exploration"
```

Funders are read-only watchers of the repository, not owners. The researcher always owns the repo. When a paper is forked to a journal, the compliance gate resolves which funding entries cover the commits in that fork and generates acknowledgment text automatically — a funder whose grant covers those commits cannot be accidentally omitted. Funder conditions (open access mandates, data sharing requirements) are fields in `FUNDING.yaml` that the gate enforces against `journal_spec.yaml`. Plan S compliance becomes a YAML field checked at fork time, not a policy document the author must remember to consult. When funding ends, the entry receives a `period_end` date; the research continues; the funder's watch access expires. Unfunded periods are explicitly recorded (`funder: null`), making the funding timeline complete rather than leaving gaps that invite ambiguity.

**Affiliations as researcher profile.** Affiliations change independently of any research project — a contributor moves from MIT to Stanford mid-project, or holds joint appointments at two institutions. The current system asks the author to enter their affiliation on a submission form, creating a snapshot that may be wrong by the time the paper is published. The repository protocol separates affiliation from the research repo entirely. Each researcher maintains a personal profile — a Git-native timeline of institutional affiliations, analogous to ORCID but versioned and cryptographically signed:

```yaml
affiliations:
  - institution: "Massachusetts Institute of Technology"
    ror: "https://ror.org/042nb2s44"
    period: "2022-09 / 2025-08"
  - institution: "Stanford University"
    ror: "https://ror.org/00f54p054"
    period: "2025-09 / present"
```

`CONTRIBUTORS.yaml` in the research repository links to each contributor's profile rather than duplicating affiliation data. When a paper is forked, the system resolves: "at the time of the commits in this fork, what was this contributor's affiliation?" The answer comes from the researcher's profile timeline intersected with the commit timestamps — not from a form field. This eliminates the "affiliation at time of research vs. affiliation at time of publication" footnote problem that currently requires manual disambiguation. Verification is structural: a commit signed from an `mit.edu` email domain corroborates an MIT affiliation entry, and an institution can optionally GPG-sign the profile entry to confirm the appointment.

The three-level separation — affiliations (person), funding (project), authorship (paper) — means each can be updated independently without touching the others, and each is verified against its own source of truth rather than self-reported on a form.

### 2.10 Federation and Local Sovereignty

A critical design constraint: scientists will not entrust their life's work to a centralized platform they do not control. Any protocol that requires a single hosting provider — even a well-intentioned one — replicates the power dynamics of the current publisher oligopoly in a new form. The Principles for Open Scholarly Infrastructures [@bilder-2015-principles-open-scholarly-infrastructures] articulate why: trustworthy scholarly infrastructure must operate under stakeholder governance, maintain transparent operations, and carry a formal wind-down plan — none of which are guaranteed by proprietary platforms regardless of their current intentions.

Git is inherently decentralized. A Git repository is a complete, self-contained history that can be cloned, moved, and operated on without any server. The Research-as-Repository protocol leverages this property through a three-tier architecture:

**Tier 1: Local-first authoring.** The author's repository lives on their own machine. All writing, data analysis, and version history happen locally. No internet connection is required for any authoring operation. The author owns their files — not a platform, not an institution, not a publisher. This is how Git already works for software. No new infrastructure is needed.

**Tier 2: Optional remote hosting.** The author may push their repository to any Git-compatible host: GitHub, GitLab, a university's self-hosted Gitea instance, or a personal server. The choice of host is the author's. The protocol imposes no requirement on where the repository is hosted — only on its structure (the presence of `paper.yaml`, `CONTRIBUTORS.yaml`, `PROVENANCE.yaml`).

Multiple remotes are supported natively by Git. An author can push to their university's GitLab AND to GitHub AND to a personal backup — simultaneously, with no conflict. If one host disappears, the repository survives on the others and on the author's local machine.

**Tier 3: Federated discovery and provenance.**

Fork-based submission requires that the receiving party (a journal, a preprint server) can verify the provenance chain. This does not require a central registry. It requires a **federation protocol** — a way for independent hosts to exchange provenance metadata.

The model is email (SMTP), not social media (Twitter). Email works because any server can send to any other server using a shared protocol. No central authority controls who can send or receive. The Research-as-Repository federation protocol works the same way:

```
Author (hosted on University GitLab)
    |
    |-- fork request --> Journal (hosted on their own OJS+Git)
    |   |
    |   |-- provenance check: query author's remote for PROVENANCE.yaml
    |   |-- verify: no active forks to other journals
    |   |-- accept fork: clone at specified commit
    |
    |-- fork request --> arXiv (hosted on arXiv infrastructure)
        |
        |-- provenance check: same query, same verification
        |-- accept: add to collection, mint identifier
```

Each participant runs their own infrastructure. The protocol specifies the message format (provenance queries, fork requests, decision records) and the verification rules (how to check a provenance chain). No central platform is involved.

**Adoption gradient.** The three tiers allow incremental adoption:

1. **Minimal adoption**: Author uses Git locally for version control. Benefits: full history, contributor tracking, backup. Cost: learning Git (many researchers already use it for code).

2. **Moderate adoption**: Author pushes to a remote host and includes `paper.yaml`. Benefits: structured metadata, machine readability, DOI minting via Zenodo-GitHub integration (already exists). Cost: maintaining the YAML companion.

3. **Full adoption**: Author participates in the federation protocol — submitting via fork, receiving review branches, carrying provenance. Benefits: all five gaps closed. Cost: journals must implement the protocol.

Tier 1 is useful immediately, alone, with no institutional adoption. This is critical: the protocol must deliver value to a single researcher on their laptop before it delivers value to the system.

### 2.11 The AI-Native Layer

When every paper is a repository with structured metadata (`paper.yaml`), machine-readable content (Markdown), and auditable provenance (`PROVENANCE.yaml`), the entire corpus becomes queryable. This extends and makes structurally verifiable the kind of machine-indexed scholarly graph that open scholarly indexes such as OpenAlex already enable at the document level [@priem-2022-openalex-fullyopen-index]:

**Cross-paper consistency**: An AI agent can detect when Paper B's claims depend on Paper A's results, and Paper A has been retracted or revised. The dependency chain is explicit in `paper.yaml`.

**Real-time literature review**: "Find all papers whose claims depend on the Peters ergodicity framework and have been accepted by a Q1 journal in the last 6 months" — answerable in seconds from structured metadata.

**Language independence**: The repository stores structured claims. An AI can translate the natural-language manuscript while preserving the machine-readable claim structure. A Japanese researcher can read a Brazilian paper's claims in Japanese, verify them against the original structured metadata, and cite the specific claim by ID.

**Change propagation**: When a foundational paper updates a key result, every paper that cites that result can be automatically flagged. The dependency graph is explicit. Currently, citation is a string in a reference list. In the repository protocol, citation is a typed link to a specific claim in a specific version of a specific repository.

**Reviewer assistance**: An AI can pre-screen a fork against the journal's scope, check the `paper.yaml` claims for internal consistency, flag potential conflicts with known results, and prepare a structured briefing for the human reviewer — all before the reviewer opens the manuscript.

**AI contribution traceability**: Git does not just track the researcher's work. It tracks their AI's work too. Every AI-assisted edit becomes a commit with structured metadata: the tool used, the model version, and a hash of the prompt that generated the output. This makes AI contribution structurally transparent and auditable — not as a self-reported disclosure statement, but as a verifiable chain of operations embedded in the repository's history. The AI disclosure problem that journals are currently struggling to solve through policy becomes an engineering problem with an engineering solution: the commit log.

### 2.12 Toward a Normative Specification

The preceding sections describe the protocol conceptually — its architecture, its components, and their interactions. A production-grade implementation requires a normative specification: a formal, unambiguous document that defines message formats, authentication flows, error handling, and API contracts with sufficient precision that independent implementers can build interoperable systems.

The normative specification would contain four structural components:

**Message schemas.** Every interaction between protocol participants — fork requests, review responses, editorial decisions, provenance queries, collection acceptance notifications — requires a formally defined message format. These schemas would specify required and optional fields, data types, validation rules, and versioning semantics. The COAR Notify protocol [@coar-2023-coar-notify-protocol] (which defines notifications between repositories and review services) provides a foundation: the Research-as-Repository protocol can extend COAR Notify's Linked Data Notifications with paper-specific message types (fork-request, review-commit, decision-record, provenance-query).

**Authentication and signing.** The provenance chain's integrity depends on verified identity. GPG-signed commits — already standard in high-security software development — provide cryptographic proof that a specific person made a specific change at a specific time. The normative specification would define an institutional key infrastructure: universities and publishers maintain signing keys; individual researchers sign with ORCID-linked keys; AI tools sign with tool-specific keys that encode model version and configuration. Signposting [@signposting-2022-signposting-scholarly-web] (typed HTTP links for scholarly objects) provides the discovery layer: a paper repository's landing page advertises its provenance endpoint, its review branches, and its collection memberships through machine-readable link headers.

**Error handling.** Production systems fail. The specification must define behavior for validation failures (which checks are blocking vs. advisory, how failures are reported, what retry semantics apply), conflict resolution (what happens when two forks target the same journal simultaneously, how merge conflicts in review branches are resolved), and timeout policies (how long a fork remains active before automatic expiration, what happens to review branches when a reviewer becomes unresponsive).

**API endpoints.** The federation protocol (Section 2.10) requires a defined interface — whether REST endpoints, protocol-level messages, or both — through which independent hosts exchange provenance metadata, fork requests, and decision records. DataCite's REST API for DOI minting and metadata retrieval provides a model for the provenance query interface. ORCID's OAuth-based identity verification provides a model for the authentication flow.

The normative specification is future work. It requires multi-stakeholder input from publishers (who must implement fork acceptance and review branch management), libraries (who must implement collection curation and long-term preservation), platform providers (who must implement the federation protocol), and researchers (who must validate that the specification serves their workflows without imposing unreasonable burden). The governance model — whether the specification is maintained by an existing standards body (NISO, W3C, IETF) or a new consortium — is itself a design decision that affects adoption. The conceptual architecture in this paper is the necessary prerequisite: one must know what the protocol does before specifying how it does it.

### 2.13 The Research Wiki: Structured Knowledge Accumulation

The repository protocol addresses how research is built, evaluated, and decided upon. It does not address how the researcher *organizes the knowledge that informs the research* — the literature, the sources, the correspondence, the evolving understanding that precedes and surrounds the paper. Reference managers (Zotero, Mendeley, EndNote) fill this role today but operate outside the research repository: no version control, no provenance chain, no structural integration with the paper's claims.

Karpathy [-@karpathy-2026-llm-wiki-pattern] proposes a three-layer pattern for personal knowledge management: raw sources (immutable ground truth), a wiki (LLM-maintained structured knowledge), and a schema (specification governing what the wiki tracks). This paper proposes an optional `.wiki/` directory that applies this pattern within the research repository (full specification at github.com/spectralbranding/paper-repo):

```
.wiki/
  schema.yaml        # What to track and how to organize
  sources/           # Raw materials (PDFs, URLs-as-markdown, datasets)
  pages/             # LLM-maintained wiki pages (by topic, author, concept)
  correspondence/    # Emails, messages, reviews (redactable)
  ingest.jsonl       # Chronological source ingestion log
  contradictions.md  # Sources that conflict with paper's claims
```

The `.wiki/` directory is private by default (excluded from public forks via `.gitignore`), retaining full git history locally. The researcher controls what is shared. The provenance chain — when each source was added, what was read, how the understanding evolved — is preserved regardless.

#### 2.13.1 Intellectual Work Proofs

The research wiki creates five structurally distinct types of intellectual work proof via git's cryptographic properties (every commit is SHA-256 hashed, timestamped, and signed):

- **Discovery proof**: when a source was first encountered — the `ingest.jsonl` log records each addition with timestamp and file hash, creating a verifiable record that reference managers cannot provide.
- **Priority proof**: when an idea was first articulated — the commit history shows the exact moment a concept appeared in the manuscript, establishing priority at the commit, not the publication date.
- **Attestation proof**: when an idea was shared with a third party — the `.wiki/correspondence/` directory stores timestamped exchanges, allowing a researcher to demonstrate that an idea predated its public disclosure.
- **Derivation proof**: how the argument developed — the full commit history of the paper shows the intellectual trajectory, the equivalent of a lab notebook for conceptual research.
- **Independence proof**: whether an idea was developed independently — if another group's preprint never appears in `ingest.jsonl`, independence is structurally demonstrated rather than informally asserted.

#### 2.13.2 Privacy and the Commit-Reveal Mechanism

The `.wiki/` directory is private by default. PDF source files can be excluded from public pushes while their SHA-256 hashes remain in the tracked `ingest.jsonl` — proving possession of a specific file at a specific date without distributing copyrighted content.

The same mechanism applies to the researcher's own work. A commit hash is a tamper-evident fingerprint: publishing the hash establishes that the work existed in that exact form at that moment, without revealing the content. This is **commit-reveal** — priority and provenance are established at commit time; disclosure is the author's to control, selectively and verifiably. A researcher can anchor commit hashes publicly at key milestones (a derivation, a pre-registration, a draft completion) and disclose content later, with any party able to verify that the revealed content matches the previously published hash. The mechanism supports embargo, consortium collaboration, hybrid public-private repositories, and misconduct prevention without requiring any centralized databank.

---

## 3. Design Principles

### 3.1 Single Source of Truth (SSOT)

The author's repository is the one and only source of truth for the paper. All other representations — PDFs, preprints, published versions, translations — are renderings. If the rendering disagrees with the repository, the repository is correct. This principle has deep roots in information science philosophy: Furner [-@furner-2010-philosophy-information-studies] identifies provenance and origination as foundational concepts in the epistemology of information objects, providing the philosophical grounding for why a versioned source-of-truth structure is not merely a technical convenience but an epistemic requirement for scientific integrity.

This inverts the current hierarchy, where the published PDF is the canonical version and the author's files are disposable. In the repository protocol, the published version is a tagged release from the repository — one rendering among many, distinguished only by its DOI and journal badge.

### 3.2 Functions by Design

Every feature that the current system implements through policy, the repository protocol implements through structure:

Table 4: Policy-based vs structure-based implementation of publishing functions.

| Current approach | Repository approach |
|---|---|
| Dual submission ban (policy, honor system) | Provenance chain makes active forks visible (structural) |
| Double-blind review (manual anonymization) | Blinding function configurable per journal (automated) |
| CRediT roles (self-reported annotation) | Contributor roles verified against commit history (auditable) |
| Peer review acknowledgment ("We thank...") | Review branches with attributed commits (structural credit) |
| Preprint posting (separate upload to separate platform) | Fork to collection user (same repository, different badge) |
| Retraction (editorial notice on published PDF) | Revert commit in repository + propagated flag to all forks |

### 3.3 Minimal Mandatory Transparency, Maximal Optional Transparency

The protocol distinguishes between information that must always be visible and information whose visibility the participant controls:

**Always visible** (structural integrity):

- That a fork exists (a submission happened)
- That a fork was revoked (a submission was withdrawn)
- Aggregate review statistics (number of reviewers, total depth)
- Contributor roles (but not necessarily identities — blinding may apply)

**Author controls**:

- Whether each fork's decision (accepted/rejected) is public
- Whether the full provenance chain is public or visible only to fork recipients
- Whether post-publication corrections are visible as diffs or only as current state

**Reviewer controls**:

- Whether their identity is revealed on specific reviews
- Which individual reviews appear in their public portfolio
- Aggregate statistics are always visible; individual details are opt-in

**Editor controls**:

- Blinding configuration for the journal fork
- Whether review branches are preserved after decision
- Whether reviews can be transferred to subsequent journals (with reviewer consent)

### 3.4 The Rendering Problem Isomorphism

The four-level hierarchy introduced in Section 1.1 — repository, paper, fork, publication — is not merely an analogy to software engineering. It is an instance of a general structural pattern: the specification-implementation-perception pipeline [@zharnikov-2026l-rendering-problem-genetic], in which a specification is rendered into an implementation that produces observer-dependent perception.

**The hierarchy.** The mapping is exact:

1. **Research program = repository.** The single source of truth for the research, evolving across commits. Analogous to a brand specification or an organizational schema.
2. **Paper = render.** A frozen snapshot of the research at a specific commit — a communication event, not the research itself. Analogous to brand signals emitted into the market or operational processes executed by an organization.
3. **Fork = sharing.** The render is transmitted to the community for confirmation. The fork is lossy: no single paper captures the full repository, just as no single brand interaction captures the full brand specification.
4. **Publication = merge.** The community (journal) evaluates the render and either merges it into its collection or closes the fork. Analogous to the perception that forms after the signal reaches its audience.

Table 5: Cross-domain comparison: specification-rendering-perception across three sibling frameworks.

| Structural layer          | Branding (SBT)             | Organization (OST)         | Research (this protocol)   |
|---------------------------|----------------------------|----------------------------|----------------------------|
| Specification             | Brand spec (8 dimensions)  | Org schema (L0-L5)         | Research repository (SSOT) |
| Implementation / Render   | Brand signals (emissions)  | Operations (processes)     | Paper (frozen snapshot)    |
| Perception / Evaluation   | Perception cloud (observer)| Performance metrics        | Community review (peers)   |

*Notes*: SBT = Spectral Brand Theory [@zharnikov-2026-spectral-brand-theory-computational-framework]; OST = Organizational Schema Theory [@zharnikov-2026-organizational-schema-theory-test-driven]. The rendering-problem isomorphism across all three frameworks is formalized in Zharnikov [-@zharnikov-2026l-rendering-problem-genetic].

The rendering is lossy at every layer [@zharnikov-2026l-rendering-problem-genetic]. A brand specification cannot be fully conveyed by any finite set of signals. An organizational schema cannot be perfectly executed by any operational process. A research repository cannot be fully captured by any single paper. And the perception is observer-dependent: different consumers perceive different brands from the same signals; different employees experience different organizations from the same processes; different reviewers perceive different papers from the same manuscript. This isomorphism connects to the "between meaning and machine" problem in information science [@ribes-2009-between-meaning-machine]: the gap between local epistemic practice and the formal representations machines can act on.

**Self-reference.** This paper is itself an instance of the pattern it describes. The research (this repository) is rendered into a paper (this manuscript) that produces community evaluation (peer review at the target journal). The reader is currently experiencing the perception layer of a specification-implementation-perception pipeline whose specification layer is a Git repository. The rendering is lossy — several hundred commits of research development are compressed into a single manuscript. And the evaluation is observer-dependent — different reviewers will perceive different papers from this same text.

---

## 4. Implications

### 4.1 For Authors

The research repository replaces the fragmented workflow of Word documents, email attachments, submission portals, and manual record-keeping with a single versioned repository that serves all purposes:

- **Writing**: collaborative editing with full attribution
- **Submission**: fork to journal (one operation, full provenance)
- **Preprint**: fork to arXiv/Zenodo collection (same operation)
- **Revision**: continue working on main branch; create new fork when ready
- **Publication**: tagged release with DOI
- **Post-publication**: corrections as commits, visible to all fork holders. In a repository system, there is no distinction between a "correction" and normal development — a correction is just a commit. The concept of "errata" as a special publication type is a document-era artifact

### 4.2 For Reviewers

Review labor becomes visible, portable, and creditable. The reviewer's work is no longer a private communication between reviewer and editor — it is an attributed intellectual contribution with a verifiable record. This has direct implications for career evaluation: a researcher with a strong review portfolio demonstrates scholarly judgment that publication counts alone cannot capture.

### 4.3 For Editors

The editor gains structured data about every paper in the pipeline: who contributed what, how the paper has been received elsewhere, and what the reviewer community thinks — not as a stack of PDFs in an inbox, but as a queryable graph of repositories, forks, and review branches. The reviewer portfolio system enables automated reviewer discovery: an editor can query for researchers with demonstrated review expertise in specific topics, methods, or claim types — matching reviewers to papers by structural competence rather than personal networks.

### 4.4 For AI Transparency

One of the most contested questions in contemporary science is the role of AI in research: which parts of a paper were written, analyzed, or suggested by AI tools? Current disclosure mechanisms are text statements ("AI was used for...") that no one can verify. A researcher can declare any level of AI involvement — or none — and the declaration is unfalsifiable.

The repository protocol offers a structural approach to this problem. When AI tools interact with a paper repository, their contributions are commits — the same versioned, timestamped, attributed operations that track human contributions. The `CONTRIBUTORS.yaml` file records each AI tool with its type (`ai_tool`), its specific roles (writing-review, consistency-checking, formal-analysis), and a disclosure statement. The commit history shows exactly which sections were modified in commits attributed to AI-assisted sessions.

Crucially, the commit metadata can encode the specific AI tool, model version, and a hash of the prompt that produced the output — making every AI-assisted edit not just visible but reproducible. A reviewer or editor can query the repository: "Show me every commit where an AI tool was involved, what model was used, and what it was asked to do." This transforms AI disclosure from a binary yes/no statement into a granular, auditable record of exactly how AI contributed to the paper.

This does not fully solve the AI transparency problem — an author can still commit AI-generated text under their own name. But it shifts the default from unverifiable declaration to auditable history. A repository where Claude is listed in CONTRIBUTORS.yaml with 0 commits but the manuscript was written in 3 days raises the same questions a code review would raise: the attribution and the evidence do not match. The git log creates a structural expectation of consistency between declared contributions and observed activity — an expectation that does not exist when the only disclosure is a sentence in the acknowledgments.

The urgency of structural AI traceability is no longer hypothetical. Lu et al. [-@lu-2026-towards-endtoend-automation] demonstrate a fully autonomous AI system — The AI Scientist — that generates research ideas, runs experiments, writes complete manuscripts, and performs its own peer review. An AI-generated paper passed peer review at a top-tier machine learning workshop. The authors themselves identify the risks: "the potential to overwhelm the peer-review process, artificially inflate research credentials, repurpose the ideas of others without giving proper credit" (Lu et al., 2026, p. 917). The Research-as-Repository protocol provides the infrastructure response: when The AI Scientist operates within a research repository, every generated paragraph is a commit, every experiment a branch, and every AI reviewer's assessment an attributed review. The contribution is auditable by construction.

### 4.5 For the System

The cumulative effect is that scientific publishing becomes a transparent, auditable, machine-readable graph of knowledge production. The Matthew Effect — where early prestige compounds into career advantage through mechanisms invisible to evaluation systems — becomes structurally traceable. The specification gap that motivates Paper Spec [@zharnikov-2026m-projection-cascade-why] becomes closeable across the full research lifecycle, not just in the manuscript text. Funding compliance — Plan S open-access mandates, funder data-sharing requirements — becomes structural: checked by the compliance gate against `FUNDING.yaml` conditions at fork time, not declared on a form and hoped for.

Post-publication commentary follows the same pattern: a reader can fork the published repository, add a critique as a committed review branch, and submit it to the journal's collection. The critique carries the same provenance and attribution as the original review. Living papers — research updated continuously — become the natural mode, with each version a tagged commit rather than a separate publication.

The same CI pipeline that validates compliance can also validate reproducibility: running the analysis code in the repository against the declared data manifest and confirming that the stated results are computationally reachable. Reproducibility becomes a compliance check, not a separate initiative.

### 4.6 For Universities and Research Evaluation

Scientific evaluation currently relies on a self-reinforcing loop: universities evaluate researchers by journal prestige, journals evaluate papers partly by institutional affiliation, and hiring and funding decisions rely on journal prestige — the loop perpetuates. Direct evaluation of the actual science is prohibitively expensive, so journal brands serve as scalar proxies for quality assessment.

The protocol makes direct evaluation tractable. A hiring committee can query a candidate's repositories for contribution depth — measured in commits and diffs, not author position on a byline. Review quality is captured in a portable portfolio that demonstrates scholarly judgment across venues and topics. Collaboration patterns are visible as cross-repository activity: who works with whom, on what, and how substantively. Research trajectory is legible as a commit graph over years, showing not just what was published but how ideas developed, pivoted, and matured.

This does not eliminate peer review — it makes peer review data *available* for evaluation, instead of collapsing it to a binary signal: "published in Nature" or not. A tenure committee reviewing a candidate's repository can see which sections the candidate wrote, which reviewers engaged deeply with the work, and how the candidate responded to criticism — the kind of granular evidence that no CV, h-index, or journal impact factor can provide.

The protocol does not replace prestige. It reduces reliance on prestige as a proxy, by making the underlying quality data directly accessible. DORA [-@dora-2013-san-francisco-declaration-research], the Leiden Manifesto [@hicks-2015-bibliometrics-leiden-manifesto], and CoARA [-@coara-2022-agreement-reforming-research-assessment] have called for precisely this shift — multi-dimensional, evidence-based research evaluation — but no system has yet delivered the data infrastructure to support it. The protocol provides that infrastructure. The structural inadequacy of journal-level evaluation is now acknowledged at the policy level: in April 2026, the Chinese Academy of Sciences discontinued its 22-year journal ranking system, citing the need to assess what research actually contributes rather than where it is published [@liu-2026-china-discontinues-prominent]. The CAS decision illustrates what DORA, the Leiden Manifesto, and CoARA have argued in principle — that journal-level metrics are a lossy compression of multi-dimensional research quality — and it signals that the institutional consensus is shifting toward evaluation systems capable of capturing contribution directly.

### 4.7 For Funders and Government

The chain from grant to impact — grant funds researcher, researcher commits code and text, commits aggregate into papers, papers generate citations and downstream research — is currently traceable only at the coarsest level: which grants funded which papers. The protocol makes this chain traceable at commit-level granularity. Every commit carries contributor attribution and can reference a funding source declared in `FUNDING.yaml`. The result is a verifiable lineage from specific expenditure to specific intellectual output.

Compliance becomes structural rather than bureaucratic. Funder requirements — open access mandates, data sharing, preregistration, AI disclosure — are encoded as conditions in `FUNDING.yaml` and checked by the compliance gate at fork time. Progress reports become redundant: the repository's tagged releases *are* the progress reports, with full provenance showing what was accomplished, by whom, and when. ROI measurement becomes possible at a resolution that current systems cannot approach: which commits, from which researchers, funded by which grants, produced which cited results. Publicly funded research acquires a verifiable paper trail from first commit to published result. Recent meta-research [@huang-2020-evaluating-impact-open] shows that policy-effectiveness evaluation depends on the data infrastructure available — an argument the present protocol turns into actionable architecture: when funder compliance conditions are YAML fields checked at fork time, the gap between mandate and measurable outcome narrows structurally rather than administratively.

### 4.8 For Society

Tax-funded research currently enters a pipeline whose internal workings are invisible to the public that finances it. The protocol makes the research process — not just the final paper — transparently auditable. Trust in science is expected to increase when provenance is visible: the public can see not just the conclusion but the process that produced it, including how objections were raised and addressed during review.

Retraction cascades become structurally traceable. When a foundational result is retracted, the dependency graphs encoded in `paper.yaml` files across the federation can flag all downstream papers that cited or depended on the retracted claims — an operation that currently requires manual literature searches and takes months. The AI disclosure question — which concerns the public, not just journal editors — has a structural answer: the commit history shows exactly what AI tools contributed, making the question auditable rather than declarative.

### 4.9 For Junior Researchers

AI tools are compressing the "building" phase of a research career — the years of manual literature review, data cleaning, and methodological trial-and-error where junior researchers traditionally develop architectural judgment about how research works. If AI handles the construction, the question becomes: where do junior researchers develop the judgment that senior researchers currently bring?

Review portfolios provide one answer. Reviewing is learning — evaluating others' claims, methods, and arguments develops exactly the critical judgment that AI cannot shortcut. The protocol makes review a credited activity with a portable record, transforming it from invisible service labor into a visible training mechanism. A junior researcher's contribution is legible from their first commit — not hidden behind senior author names on a byline where the fourth author's actual role is unknowable.

The protocol does not solve the pipeline problem. But it provides the infrastructure for career development paths that do not depend on the traditional model of building invisibly for years before receiving credit. When contributions are commits, even early-career researchers have a verifiable record of what they built and how they think.

### 4.10 Stakeholder Summary

Table 6: Stakeholder benefit summary.

| Stakeholder | Current pain | Protocol benefit |
|-------------|-------------|-----------------|
| Authors | Formatting waste, opaque decisions, AI disclosure uncertainty | Own their research. Full contribution credit. AI transparent by design. |
| Reviewers | Invisible labor, no credit, no portfolio | Attributed work. Portable portfolio. Measurable depth. |
| Junior researchers | Pipeline collapse, invisible contributions | Visible from first commit. Review as credited training. |
| Editors | Desk rejection waste, reviewer matching hard | Compliance gate. Structural reviewer matching. Auditable pipeline. |
| Journals | Role threatened by preprints | Elevated from gatekeeper to curator. Quality of curation measurable. |
| Universities | Rely on journal prestige as proxy | Evaluate researchers on structural data: commits, reviews, trajectory. |
| Funders | Compliance is bureaucratic, ROI unmeasurable | Grant-to-impact chain traceable. Compliance as YAML field. |
| Society | Publicly funded research opaque | Transparent, auditable research. Trust through provenance. |

---

## 5. A Realized Instance: The Author's Corpus as a Running Repository

Sections 2 through 4 describe the protocol as a proposal. This section reports that the central reconception is no longer only proposed: the author's own research corpus runs a working instantiation of it. The instantiation does not implement the full federated lifecycle — fork acceptance, review branches, and cross-host federation remain conceptual (Table 2b) — but it does realize the protocol's deepest claim, that a research program is a versioned, machine-readable repository of which papers are renders. It does so on a live body of work, and it runs on this very paper. The system is therefore presented here as an existence proof and a design, not as a validated social practice; the distinction is made precise in Section 5.5.

### 5.1 The Substrate Is the Repository

The corpus is maintained as a single content-addressed store — a substrate — that unifies three graphs: the *terms* each paper introduces, the *claims* each paper makes, and the *citations* each paper relies on. Every human-facing artifact derived from the corpus (a paper's reference list, its glossary, its bibliographic exports) is a projection of that substrate, regenerated on demand rather than hand-maintained. This is the *substrate-as-repository*: the concrete instantiation of the repository reconception of Section 2, where the repository is the single source of truth and the paper is one render among many. The design principle is the paper's own SSOT principle (Section 3.1) applied to the corpus's metadata rather than to a single manuscript's prose.

The substrate makes the four-level hierarchy operational at the level of meaning rather than of files. Where Section 2 frames a *paper* as a render of a *repository*, the substrate adds a finer claim: the structured content a paper asserts — its definitions, its propositions, its evidentiary dependencies — is itself extractable, queryable, and recombinable independent of the prose that renders it for a particular reader.

### 5.2 The Linker Is a Type-Checker; the Gate Is Continuous Integration

Two software-engineering patterns make the substrate trustworthy as it grows.

First, each paper declares a small *ontology module*: the terms it introduces and owns, the terms it imports from other papers, and any term it explicitly refines. A linker resolves these modules against one another and enforces *link-time compatibility* — exactly the discipline a compiler applies to a codebase of separately authored files. The checks are concrete: one owner per term (no two papers may silently claim the same definitional authority), no dangling import or refinement (every imported term must be owned somewhere), compatible refinement (a paper that narrows an imported term must say so explicitly), and acyclicity of the narrowing relation. Each term additionally carries a content-addressed definition hash, so that when an upstream definition changes, every downstream paper that imported it is mechanically surfaced for re-validation — definitional drift becomes a detectable event rather than an invisible erosion. At the time of writing, fifty paper modules link into a graph of 171 terms and 443 ownership-and-import edges with these constraints satisfied.

Second, an anti-drift gate plays the role of continuous integration. After any paper is created or edited, and before any change is committed, the gate aggregates four consistency checks — citation alignment, the ontology link, the synchronization between a paper's claim graph and its structured spine, and a surface-form terminology scan — into a single pass-or-fail verdict, and it fails the build on hard drift: a dangling import, an incompatible refinement, definitional drift, or a paper that has diverged from its companion artifacts. The gate is read-only and runs in seconds; a test suite, including a control that fails if the system's documentation describes a tool or table that no longer exists, guards the gate itself. Across the corpus the gate currently reports zero authority failures, zero missing citations, and zero phantom citations.

The combination — a link-time compatibility check plus a build-failing cross-artifact drift gate, operated continuously over one corpus — is the part of the realized system with the least precedent, and Section 5.4 isolates why.

### 5.3 Spine-First Drafting Is the Generative Discipline

The substrate is not merely annotated after the fact; it governs drafting. Under the corpus's spine-first protocol, no prose may be written without a corresponding entry in the paper's structured spine — the typed graph of its observations, methods, claims, dependencies, and evidence. A new claim requires first extending the spine (a *fork*) or else dropping the claim (a *rebase*); prose that does not trace to a spine node is not admissible. The protocol thereby separates the paper's *meaning* (the spine graph), its *semantics* (the ontology module that fixes what its words denote), and its *meaningfulness* (the prose rendering for a particular audience) — and lets a reviewer evaluate each independently.

This paper is itself drafted under that discipline. Its structured spine was built before this section's prose; every claim in this section traces to a node in it; the bundle that travels with the paper — its prose, its spine, its ontology module, and its rendered glossary — is checked by the same gate described in Section 5.2. The self-reference of Section 3.4 is thus not only rhetorical: the manuscript is a render of the substrate, and the render is held consistent with its source by the running system the section describes.

### 5.4 Relationship to Existing Standards: What Is Emitted, What Is New

The realized system deliberately does not reinvent the semantic-publishing stack. About half of it aligns with, and is designed to emit into, established standards; those standards are treated as projection targets rather than competitors, consistent with the corpus's own thesis that one should publish the source of truth and render at the point of consumption. Concretely, the citation-role taxonomy aligns with CiTO [@shotton-2010-cito-citation-typing]; the spine's claim-evidence structure with micropublications [@clark-2014-micropublications-semantic-model] and the argument interchange format [@chesnevar-2006-argument-interchange-format]; the spine's claims as provenance-bearing units with nanopublications (Groth et al. [-@groth-2010-anatomy-nanopublication-information]; Kuhn et al. [-@kuhn-2021-semantic-microcontributions-with]); the content-addressed definition identity with Trusty URIs [@kuhn-2014-trusty-uris]; the per-paper bundle with RO-Crate [@soilandreyes-2022-packaging-research-artefacts] and the FAIR principles [@wilkinson-2016-fair-guiding-principles]; the term-relation vocabulary with SKOS [@miles-bechhofer-2009-skos-reference]; typed term mappings with SSSOM [@matentzoglu-2022-sssom]; one-term-one-owner governance with OBO Foundry orthogonality [@smith-2007-obo-foundry]; and the linker's compatible-refinement check with conservative-extension theory for modular ontology reuse (Cuenca Grau et al. [-@cuencagrau-2008-modular-reuse-ontologies]). Table 7 summarizes the alignment.

Table 7: Layers of the realized system and the established standards each aligns with or emits into.

| Layer of the realized system | Established standard aligned with / emitted into |
|---|---|
| Citation-role taxonomy | CiTO, the Citation Typing Ontology [@shotton-2010-cito-citation-typing] |
| Claim → evidence → method structure of the spine | Micropublications [@clark-2014-micropublications-semantic-model]; argument interchange [@chesnevar-2006-argument-interchange-format] |
| Spine claims as publishable, provenance-bearing units | Nanopublications (Groth et al. [-@groth-2010-anatomy-nanopublication-information]; Kuhn et al. [-@kuhn-2021-semantic-microcontributions-with]) |
| Content-addressed definition identity | Trusty URIs [@kuhn-2014-trusty-uris] |
| The per-paper bundle (prose + spine + ontology + glossary) | RO-Crate [@soilandreyes-2022-packaging-research-artefacts]; FAIR principles [@wilkinson-2016-fair-guiding-principles] |
| Term-relation vocabulary (synonym, narrows, maps-to) | SKOS [@miles-bechhofer-2009-skos-reference] |
| Typed, justified term mappings | SSSOM [@matentzoglu-2022-sssom] |
| One-term-one-owner governance | OBO Foundry orthogonality [@smith-2007-obo-foundry] |
| The linker's compatible-refinement check | Conservative-extension / modular-reuse theory for ontologies (Cuenca Grau et al. [-@cuencagrau-2008-modular-reuse-ontologies]) |

*Notes*: The substrate remains the single source of truth; each standard above is a render target, in the same sense that BibTeX and the reference list are render targets of the citations graph. The corpus adopts these vocabularies and emits into them rather than re-keying its internal model onto any one of them.

What none of these standards provides — and what the realized system contributes — can be stated precisely. First, the *per-paper module as a codebase symbol*: SKOS, OWL, and OBO have no notion of a paper as the unit of definitional ownership with a compiler-style symbol table of exports, imports, and refinements resolved at link time. Second, a *single substrate unifying terms, claims, and citations*: each standard solves one layer (vocabularies, mappings, citations, claims, or packaging), and none unifies all three in one content-addressed store of which papers are projections. Third, the *link-time compatibility check plus build-failing anti-drift gate* applied continuously to one corpus: content-addressing makes single artifacts tamper-evident and ontology quality-control exists, but a gate that fails the build on dangling import, incompatible refinement, or cross-artifact drift is a software-engineering pattern, not an ontology-publishing one. Fourth, the *spine-first generative drafting protocol*: every prior model annotates or packages work after it is written, whereas this protocol forbids prose without a prior spine entry. The system can therefore be positioned exactly: it treats a single-author research corpus as a linkable module system, emits the linked artifacts into the standards above, and adds the link-time compatibility check, the spine-first drafting protocol, and the cross-artifact drift gate that those standards do not provide.

### 5.5 Scope of the Existence Proof

Two limits bound what the realized instance demonstrates, and both are recorded honestly rather than elided.

The system is *single-author*. The semantic-publishing standards above all assume multi-author federation: many parties contribute terms and mappings that must be reconciled. The corpus's modules are instead temporal slices of one author's evolving program, reconciled by rebase rather than by negotiation between independent owners. The link-time compatibility check is therefore exercised within one authority, not across competing ones. This is a deliberate and defensible regime for a single research program, but it is a different regime from the federated one the standards target.

Consequently, the strong reading of the protocol — that the bundle opens a *new mode of scholarly communication*, in which a reader (or a reader's tooling) can negotiate a paper's terminology and contest its claims at the level of the structured graph before reading its prose — is warranted here only as an existence proof and a design. Its full validation requires two things: an explicit *negotiation protocol* specifying how two authors reconcile incompatible modules (when the same term is defined differently, or one author would refine what another owns), and multi-author adoption of it. The first now exists in prototype. Where the single-author linker *aborts* on a collision — within one corpus a term has exactly one owner — a federated cross-owner linker instead *classifies* every cross-author interaction and proposes a typed, justified reconciliation: agreement (identical definitions merge), conflict (divergent definitions are namespaced and mapped, or forked), compatible refinement (one author's term is rebased as a narrowing of the other's), and dangling reference (an import neither author owns is blocked). Run over a deliberate two-author fixture, it surfaces each class mechanically and emits the proposed mappings in a standard interchange format — the federated link-time compatibility check, before either author reads the other's prose. It has since been exercised on two *real* corpus vocabularies — the author's perception-side and operations-side theory programs, presented as two independently namespaced module sets: the linker classified all six cross-owner interactions, matched the shared concepts by content-addressed hash, and recovered the bridge between the programs (the operations vocabulary imports the perception vocabulary; two boundary terms are narrowed) mechanically, before any prose was read. That run is clean by construction — because the two programs were authored to be compatible, it exhibits the resolvable interaction classes (clean imports and compatible refinements) but not the adversarial ones. To surface those, the linker was further exercised against two vocabularies the author did *not* build for compatibility: an incumbent brand-equity vocabulary (Aaker) and an information-economics one (signaling theory). The incumbent run produced a genuine *dangling reference* — the incumbent vocabulary presupposes primitives (*brand*, *consumer*) that neither ontology owns — and, tellingly, *no* same-term conflict, because the corpus's deliberately qualified naming (*perception cloud* rather than *brand image*, *cohort* rather than *segment*) was designed to avoid exactly such collisions; the genuine cross-theory relations there are semantic rather than lexical, and had to be supplied as a curated mapping the key-level linker cannot infer. The signaling-theory run produced the remaining class: a genuine definitional *conflict* on the shared bare term *signal* — the economic signal, an observable costly attribute conveying unobservable type under information asymmetry, against the brand signal, the composite ray across the eight dimensions — which the linker flagged (the two definitions hash differently), refused to assert as an exact match, and proposed instead as a namespaced close-match for human curation. Across these three runs the full interaction-class set is exercised on real, independent vocabularies. What remains future work is the social step the mechanism cannot supply: these independent modules were still transcribed by one author from published work, and each conflict was reconciled only as a tool-proposed mapping, not negotiated with the living author. Full validation requires a *living* independent co-author authoring their own modules and resolving a conflict in dialogue — multi-author adoption as a validated social practice, not the mechanism itself. The claim advanced here is correspondingly bounded: the repository reconception is realizable, has been realized on a live corpus, runs on this paper, and its federated generalization is prototyped and demonstrated across the full interaction-class set on real independent vocabularies; whether it becomes a shared social practice among independent authors is an empirical question their adoption must answer.

### 5.6 Companion Experiments and Reproducibility

The federated generalization in Section 5.5 is backed by three companion experiments, each a deterministic, content-addressed run of the cross-owner linker over two namespaced module sets. They are published with this paper (see Data Availability), so a reader can reproduce the classification and the proposed mappings before reading this prose — the protocol's own claim, applied to its own evidence.

The linker assigns every cross-owner interaction to exactly one of six classes. Table 8 names them with the SKOS predicate [@miles-bechhofer-2009-skos-reference] and reconciliation operation each carries; Figure 2 is the decision procedure that assigns them. Three of the six — *conflict*, *incompatible refinement*, and *dangling import* — are unresolved and fail the compatibility gate; the other three resolve mechanically. The three experiments below are organized as the evaluation of this taxonomy: a clean run that exercises the resolvable classes, and two adversarial runs that surface the unresolved ones.

Table 8: The six cross-owner interaction classes of the federated linker.

| Class | Trigger | Resolved? | SKOS predicate | Reconciliation operation |
|---|---|---|---|---|
| `AGREEMENT` | both authors own the key; identical `def_hash` | yes | `skos:exactMatch` | MERGE — assert the match; either author imports the term unchanged |
| `CROSS_IMPORT` | one author imports a term the other owns | yes | `skos:exactMatch` | none — a clean cross-author dependency edge |
| `CROSS_REFINE` | one author refines a term the other owns, with an explicit `narrows_to` | yes | `skos:narrowMatch` | REBASE — the refinement becomes a `narrows` edge onto the owner's term |
| `CONFLICT` | both own the same key; divergent `def_hash` | no | `skos:closeMatch` / `relatedMatch` | NAMESPACE the colliding keys and curate the mapping; FORK the key if the concepts truly differ |
| `INCOMPATIBLE_REFINE` | one author refines another's term with no `narrows_to` | no | — | BLOCK until an explicit narrowing is supplied |
| `DANGLING_IMPORT` | an import or refine targets a term neither author owns | no | — | BLOCK until some author owns the term or the import is dropped |

*Notes*: Identity is content-addressed — `def_hash` is the SHA-256 of the trimmed definition text — so "same definition" is mechanical, not a judgment call. The three unresolved classes are what the `--gate` mode fails the build on, the federated continuous-integration semantics. Proposed mappings are emitted in the SSSOM interchange format [@matentzoglu-2022-sssom], each carrying a justification (lexical or hash match versus a proposal a human must confirm) and a confidence.

```{=typst}
#block(breakable: false)[
```

```{.mermaid width="70%"}
flowchart TD
  S[Cross-owner interaction] --> Q1{Same term key owned by both?}
  Q1 -->|no| Q2{Targets a term neither author owns?}
  Q2 -->|yes| DI[DANGLING_IMPORT — BLOCK]
  Q2 -->|no| Q3{Refine of the other's term?}
  Q3 -->|no| CI[CROSS_IMPORT — clean edge]
  Q3 -->|"yes, with narrows_to"| CR[CROSS_REFINE — REBASE]
  Q3 -->|"yes, no narrows_to"| IR[INCOMPATIBLE_REFINE — BLOCK]
  Q1 -->|yes| Q4{Identical def_hash?}
  Q4 -->|yes| AG[AGREEMENT — MERGE]
  Q4 -->|no| CF[CONFLICT — NAMESPACE + FORK]
```

Figure 2: The cross-owner linker's decision procedure. Every interaction between two authors' modules is classified into exactly one of six classes by mechanical tests on ownership, import or refine, the presence of an explicit narrowing, and the content-addressed definition hash. The three terminal states marked BLOCK or CONFLICT are the unresolved classes that fail the federated compatibility gate.

```{=typst}
]
```

- *EXP-2026-06-13-NEG-SBT-OST* (clean federation): the author's perception-side and operations-side vocabularies; six interactions, zero unresolved (four cross-imports, two compatible refinements).
- *EXP-2026-06-14-NEG-AAKER-SBT* (dangling reference): an incumbent brand-equity vocabulary [@aaker-1991-managing-brand-equity; @aaker-1996-building-strong-brands] against the perception-side vocabulary; a genuine dangling import (an incumbent primitive neither side owns) and no same-term conflict — the qualified naming forecloses it — with the genuine cross-theory relations supplied as a hand-curated cross-key mapping the key-level linker cannot infer.
- *EXP-2026-06-14-NEG-SPENCE-SBT* (definitional conflict): information-economics signaling theory [@spence-1973-job-market-signaling] against the perception-side vocabulary; a genuine conflict on the shared term *signal* (the two definitions hash differently), which the linker refuses to assert as an exact match and proposes as a namespaced close-match for human curation.

Each run is deterministic: term identity is a content-addressed hash of the definition text and the classifier is a pure function of the two parsed module sets, so the report and the emitted mapping file reproduce byte-for-byte at a fixed tool version, with no random seed. Each experiment record states pre-registered hypotheses with falsification criteria, an integrity manifest of the shared-term hashes (checkable against the live graph), and a threats-to-validity section; the full attributions for the published brand-equity and signaling-theory vocabularies are given in those records. The compatibility gate exits nonzero on the two adversarial runs — the intended federated continuous-integration behavior when unresolved interactions remain. Together the three runs exercise the full interaction-class set (clean import and refinement, dangling reference, definitional conflict) on real, independent vocabularies.

*Data and code availability.* The complete experiment code and data are published with this paper under `experiments/` in its public repository (github.com/spectralbranding/sbt-papers, `r14-paper-as-repository/`): the cross-owner linker (`negotiate_modules.py`), the single-author linker it generalizes (`build_ontology.py`), the two namespaced module sets per experiment, the emitted and curated mapping files, the three experiment records, and a one-command reproduction script. All three runs reproduce with `bash experiments/reproduce.sh`; the classification is deterministic — content-addressed term identity and a pure-function classifier — and requires no data download, network call, or credential. The per-paper spine and ontology bundle are in the same repository, and software dependencies, versions, and the repository URL are recorded in `paper.yaml` following the FORCE11 software-citation principles [@smith-2016-software-citation-principles].

---

## 6. Limitations and Open Questions

### 6.1 Implementation Roadmap

The protocol's compliance gate has been prototyped. A reference validator (`validate_paper.py`, 290 lines of Python) checks a paper repository against a `journal_spec.yaml` file, validating word count, abstract length, keyword range, reference count, self-citation ratio, figure formats, and required statements (AI disclosure, data availability, funding, conflict of interest). The validator runs locally in under one second and produces a pass/fail report with specific failure messages.

A worked example demonstrates feasibility: the Journal of Marketing's submission requirements have been encoded as `journal_spec_jm.yaml` (130 fields covering manuscript format, blinding rules, figure specifications, math notation rules, and 46 compliance checks derived from actual JM submission guidelines). The following output is a demonstration of the validator against a hypothetical paper repository — not this paper's own validation results:

```
Validating against: Journal of Marketing
Repository: /path/to/paper
------------------------------------------------------------
  [OK]   Manuscript: paper.md
  [OK]   Paper Spec companion: paper.yaml
  [OK]   Word count: 9,217 (limit: page-based)
  [OK]   Abstract: 187 words (max: 200)
  [FAIL] References: self-citation 27.3% > maximum 25%
  [OK]   Statement: ai_disclosure
  [OK]   Figures: all compliant
------------------------------------------------------------
Results: 6 passed, 1 failed, 0 warnings
Submission gate: BLOCKED — fix failures before submitting
```

The example illustrates that the validator catches a specific compliance failure (self-citation ratio exceeding the journal's threshold) with an actionable diagnostic. The present paper's own self-citation ratio is 5.4% (4 of 74 references) after IS-canon restoration, cross-corpus additions, and user-confirmed citation replacements.

The author sees the exact failure (self-citation ratio), fixes it in their repository, and re-runs the validator. The entire cycle takes minutes, not the weeks currently consumed by desk-rejection-and-resubmission rounds.

A realistic adoption sequence: (1) a preprint server or overlay journal implements the fork gate as a GitHub Action — this requires only the validator and a `journal_spec.yaml`, both of which exist; (2) an existing editorial management system (OJS is open-source and extensible) adds git-linked submission as an optional flow alongside traditional upload; (3) a funder (e.g., Wellcome Trust, which already mandates open data) requires `PROVENANCE.yaml` for funded papers, creating demand-side pressure. European open-science policy has already established that infrastructure reform requires political coordination and is achievable: the European Open Science Cloud became operational through exactly this combination of mandate and incremental adoption [@burgelman-2021-politics-open-science]. Each step is independently useful and does not require the others.

The companion artifacts — schemas, examples, and validator — are published as an open-source package at the paper's public repository (github.com/spectralbranding/paper-repo).

**This paper as its own first implementation.** The present paper is authored, versioned, and structured according to the protocol it proposes. The repository contains: `paper.yaml` (7 typed claims with falsification conditions), `CONTRIBUTORS.yaml` (4 contributors including 3 AI tools with disclosure statements), `PROVENANCE.yaml` (fork history — populated as the paper is submitted to venues), `DATA_MANIFEST.yaml` (empty — this is a conceptual paper with no external data), the `journal_spec.yaml` schema, a worked Journal of Marketing example, and the `validate_paper.py` compliance validator. Every claim can be traced to a specific commit. Every contributor's role is verified against the commit log. The paper is its own proof of concept — not a prototype of the full fork-and-review protocol, but a demonstration that the repository structure, metadata schemas, and compliance tooling are functional and internally consistent. The public repository is at github.com/spectralbranding/paper-repo.

### 6.2 Evaluation Framework

The protocol's seven claims (Section 1) are conceptual propositions, not empirically validated results. Future pilot implementations should be evaluated against concrete, measurable success criteria. The following metrics define what "working" means for each structural innovation:

**Desk rejection rate reduction.** The compliance gate (Section 2.3) should eliminate formatting-related desk rejections entirely. Target: 80% reduction in desk rejections attributable to formatting, metadata, or compliance failures at adopting journals. Measurement: compare desk rejection rates (and reasons) for git-linked submissions versus traditional submissions at the same journal over a 12-month period.

**Resubmission turnaround.** When a paper requires formatting or compliance fixes (not substantive revision), the current cycle of editor-return, author-reformat, resubmission consumes days to weeks. The compliance gate reduces this to a local validation loop. Target: median resubmission time for formatting and compliance fixes reduced from weeks to hours. Measurement: time between "submission returned" and "resubmission received" for git-linked versus traditional workflows.

**Reviewer engagement depth.** The review branch model (Section 2.5) makes reviewer effort structurally visible. Engagement depth can be measured via commit count, diff size (lines of substantive commentary), and time-on-review (first commit to final recommendation). These metrics do not measure review *quality* — a short, incisive review may be more valuable than a long, unfocused one — but they provide a quantitative baseline that does not currently exist. Target: establish normative ranges for review depth across disciplines as a foundation for reviewer recognition.

**Dual submission detection.** The provenance chain (Section 2.7) makes concurrent submissions structurally detectable within the protocol. Target: 100% structural detection of concurrent identical submissions to journals that participate in the federation protocol. Measurement: false negative rate (submissions that evade detection) and false positive rate (legitimate parallel submissions, e.g., to a preprint server and a journal, incorrectly flagged).

**AI contribution traceability.** The AI-native layer (Section 2.11) records AI-assisted edits as attributed commits. Target: every AI-assisted edit attributed in commit history with tool name, model version, and prompt hash. Measurement: percentage of AI-assisted edits that carry complete attribution metadata in pilot repositories; comparison of declared AI involvement versus commit-log evidence.

These metrics are evaluation criteria for future pilots, not claims of achieved performance. The protocol is conceptual; the metrics define what a successful implementation would demonstrate.

### 6.3 Limitations

1. **Adoption barrier.** The protocol requires journals, authors, and reviewers to adopt new tooling. The transition cost is non-trivial. A realistic adoption path may begin with a single journal or preprint server implementing the protocol alongside traditional workflows during a transition period, after which the traditional workflow becomes redundant.

2. **Partial prototype only.** The compliance gate layer has been prototyped: a public repository (github.com/spectralbranding/paper-repo) contains the validator, schemas, journal specification examples, and a self-referential implementation of this paper as a compliant paper repository. However, the full fork-and-review lifecycle — fork creation, blinding function, reviewer branch management, provenance chain propagation, and collections-as-users federation — remains a conceptual architecture without implementation. A proof-of-concept implementing these components for a single journal or preprint server is the necessary validation step. The most realistic first adopter is likely a preprint server (which already accepts structured deposits) or an overlay journal (which already curates externally hosted papers), not a traditional publisher whose business model depends on controlling the manuscript pipeline.

3. **Git literacy.** The majority of researchers outside computer science and engineering have never used Git. Humanities, social sciences, and many natural science fields work primarily in Word processors. Blischak, Davenport, and Wilson [-@blischak-2016-quick-introduction-version] document the adoption barriers in detail, and Perez-Riverol et al. [-@perezriverol-2016-ten-simple-rules] provide practitioner guidance for scientific teams; even with such resources, the learning curve remains a real constraint for non-technical disciplines. The protocol requires a GUI abstraction layer — a "GitHub Desktop for papers" — that presents repository operations (commit, fork, branch) through familiar editing metaphors. Without this, adoption is limited to computationally literate disciplines. The three-tier architecture (Section 2.10) mitigates this: Tier 1 (local Git) benefits only those who already use version control; the full protocol benefits only materialize at Tier 3, which requires broader tool development.

4. **Gaming.** Commit histories can be manufactured. A contributor could inflate their commit count through trivial changes. Mitigation: review branches are created by editors, not authors; and contribution metrics should weight substance (lines changed in methods section) over quantity (total commits).

5. **Privacy.** The always-visible provenance chain reveals submission history, which some authors may consider sensitive. The protocol's "existence visible, outcome optional" compromise attempts to balance structural integrity against author privacy, but the appropriate threshold is a community decision.

6. **Legacy corpus.** The existing body of 50+ million published papers has no repository structure. Retroactive conversion is impractical. The protocol applies to new papers going forward; legacy papers remain in their current form.

7. **Governance.** The protocol is designed as a federated network (Section 2.10), not a centralized platform. Like email, any institution can run its own server. The governance question reduces to: who maintains the protocol specification? Existing models (IETF for internet protocols, W3C for web standards, NISO for information standards) provide precedents. The protocol specification could be maintained as an Internet-Draft, with community review periods and versioned releases following RFC conventions. The protocol specification itself can be versioned in a Git repository. Reference implementations should be host-agnostic: Gitea and Forgejo provide self-hosted alternatives to GitHub and GitLab, ensuring that no single commercial platform becomes a dependency. Git's distributed architecture inherently supports offline work — a researcher can commit locally with no network connectivity, and synchronization happens when connectivity returns — which makes the protocol viable in low-bandwidth and intermittent-connectivity environments without requiring any centralized infrastructure to be always available.

8. **Intellectual property.** When an editor owns a fork and reviewers commit to it, the ownership of review content is unclear under current copyright law. The protocol should specify that review commits are licensed under a standard open license (e.g., CC-BY) at creation time.

### 6.4 Stakeholder Incentives and Barriers

**Publishers.** The publisher oligopoly [@larivire-2015-oligopoly-academic-publishers] derives revenue from controlling the manuscript pipeline — submission portals, typesetting, branding, and access. The protocol disperses this control. The protocol's adoption does not require traditional publisher cooperation — it routes around them via preprint servers (which already accept structured deposits), overlay journals (which already curate externally hosted papers), and society publishers (which often operate at cost and may value the efficiency gains). Open-access publishers whose revenue comes from APCs rather than pipeline control are natural early adopters — the protocol reduces their operational costs without threatening their business model. Traditional publishers can join when the network effects make it costly not to.

**Editors.** The compliance gate eliminates formatting desk rejections — a direct time savings. The reviewer branch model provides structured data on reviewer engagement — useful for identifying reliable reviewers. Editors benefit immediately from the gate and incrementally from the review model. The hybrid flow (Section 2.2) provides a transitional compatibility mode, but the git-native flow gives editors structural advantages — version history, contributor verification, and diff capability — that the traditional flow cannot match.

**Reviewers.** The portable review portfolio creates career credit for an activity that currently generates none. The privacy controls (Section 3.3) allow reviewers to accumulate reputation without revealing specific reviews. The risk is that visible review depth creates pressure to over-invest in each review; the mitigation is that depth metrics are aggregate, not per-review.

**Authors.** The primary adoption barrier is Git literacy (Limitation 3). For authors who already use Git (common in computer science, physics, and computational biology), the protocol offers immediate benefits: version history, contributor traceability, and compliance checking. For authors in Word-dominant fields, the protocol requires a GUI abstraction layer that does not yet exist at production quality.

**Legal and intellectual property.** Reviewer commits on journal forks create intellectual contributions with unclear copyright status under current law. The protocol should specify that all review commits are licensed CC-BY-4.0 at creation time — reviewers retain attribution rights but grant reuse. This requires explicit consent at the point of reviewer invitation, analogous to the copyright transfer agreements authors currently sign.

**Privacy.** The irrevocable provenance chain raises concerns: some authors may not want rejection history visible, even as "existence of fork" without decision outcome. The protocol's current design (existence always visible, outcome optionally visible) is a compromise. An alternative — fully private provenance visible only to fork recipients — weakens the dual-submission prevention. The appropriate default is a community decision that may vary by discipline: clinical research may require full transparency; humanities may prefer privacy. The protocol supports both configurations.

### 6.5 Ethics, Legal, and Equity Considerations

The protocol's structural advantages — transparency, traceability, machine readability — carry risks that must be addressed explicitly rather than discovered through adoption.

**Platform dependence.** The protocol is Git-native but must not entrench the dominance of any specific hosting platform. GitHub's current market position makes it the path of least resistance for implementation, but a protocol that requires GitHub replicates the power asymmetry it aims to dissolve — trading publisher lock-in for platform lock-in. The federation architecture (Section 2.10) mitigates this structurally: any Git-compatible host can participate. However, institutional hosting capacity varies enormously. A well-funded research university can run its own Gitea instance; a university in the Global South may lack the systems administration staff to do so. The protocol specification must remain host-agnostic, and reference implementations must be tested on self-hosted infrastructure, not only on commercial platforms.

**Accessibility.** Git's command-line interface is inaccessible to many researchers — not only those unfamiliar with version control but also those with visual, motor, or cognitive disabilities for whom terminal interaction presents barriers. The GUI abstraction layer noted in Limitation 3 is not merely a convenience; it is an accessibility requirement. Any reference implementation must meet WCAG 2.1 AA standards. Screen reader compatibility, keyboard navigation, and high-contrast modes are not optional features — they are prerequisites for equitable adoption.

**Global equity.** The protocol assumes reliable internet connectivity for federation (Tier 3), remote hosting (Tier 2), and even efficient collaboration (Tier 1 with remote co-authors). Researchers in regions with intermittent connectivity, bandwidth constraints, or restricted access to international platforms face structural disadvantages. The protocol's local-first design (Tier 1) partially addresses this — all authoring operations work offline. But submission, review, and publication require network access. Future implementations should consider offline-first synchronization patterns (analogous to Git's own design for intermittent connectivity) and lightweight federation protocols that minimize bandwidth requirements.

**Labor implications.** Reviewer attribution is a corrective to the current invisibility of review labor. But making review depth measurable creates a new risk: the metrics could become targets. If hiring committees begin evaluating candidates on review portfolio depth, the protocol inadvertently creates pressure for unsustainable overwork — reviewers investing more hours per review to build visible records. The framing matters: reviewer attribution should recognize *existing* labor that currently goes uncredited, not demand *additional* labor. Aggregate metrics (total reviews, journal breadth) are safer signals than per-review depth metrics, which could incentivize quantity over judgment.

**Legal and intellectual property.** Reviewer commits on journal forks constitute intellectual contributions — structured, attributed, and timestamped. Their copyright status under current law is ambiguous: is a review comment a work-for-hire (if the reviewer is compensated), a voluntary contribution (if unpaid), or a derivative work (if it modifies the manuscript text)? The protocol should require that all review commits be licensed CC-BY-4.0 at the point of reviewer invitation, before any review work begins. This parallels the copyright transfer agreements authors currently sign at submission — extending the same contractual clarity to reviewers.

**Patent-bound and pre-disclosure research.** Some research is aimed at patents and must remain private until intellectual property is filed. Git handles this natively: private repositories with access control. `PROVENANCE.yaml` can carry a `visibility` field (`public` or `private_until: [date]`) that the compliance gate enforces — blocking fork requests to public venues while the visibility constraint is active. Once the patent is filed, the repository goes public. The full commit history then proves priority, prior art, and inventorship timeline with cryptographic certainty — stronger IP protection than any paper notebook. The protocol does not require openness; it requires *structural readiness* for openness, activated when the researcher decides the time is right.

**Privacy and the irrevocable record.** The provenance chain is append-only by design — this is what makes it trustworthy. But irrevocability means that submission history, rejection patterns, and review timelines are permanently recorded. A researcher who submits to ten journals before acceptance has a visible record of nine rejections (or at minimum, nine prior forks). The protocol's current design makes fork *existence* always visible while keeping *decisions* optionally visible (Section 6.3, Limitation 5). The appropriate default — how much provenance is visible to whom — should be community-configured and may vary by discipline. Clinical research, where transparency serves patient safety, may require fuller disclosure than humanities, where submission patterns carry different professional implications.

---

## 7. Conclusion

The Research-as-Repository protocol demonstrates that the document assumption is no longer technically necessary nor epistemically defensible. By replacing static artifacts with versioned, provenance-rich repositories, the protocol makes scientific knowledge production structurally transparent, auditable, and machine-queryable without centralizing control or mandating platform adoption. Its theoretical contribution lies in the specification-implementation-perception pipeline: a general pattern that unifies research communication with parallel frameworks in branding and organizational design. This isomorphism reveals why provenance infrastructure matters — renders are necessarily lossy, perceptions are observer-dependent, and only the underlying specification can support reliable evaluation.

For electronic publishing platforms the implications are immediate. Journals can shift from PDF wrangling and formatting enforcement to semantic curation and review-quality assessment. Preprint servers and overlay journals become first-class collection curators in a federated ecosystem. Compliance, blinding, and provenance become services operating on repositories rather than bottlenecks authors must navigate. AI assistance moves from opaque disclosure statements to auditable commit histories. Research assessment bodies gain queryable data on contribution depth, review portfolios, and intellectual trajectories — precisely the multi-dimensional evidence demanded by DORA, Leiden, and CoARA but previously unavailable at scale.

The largest remaining risk is adoption inertia. The protocol therefore adopts a three-tier local-first design that delivers value to individual researchers before system-level buy-in is required. The compliance gate and validator already exist; a single preprint server or society journal implementing the fork gate would create immediate network effects. Governance should follow open standards processes (IETF/NISO model) with host-agnostic reference implementations and align with the Principles for Open Scholarly Infrastructures [@bilder-2015-principles-open-scholarly-infrastructures]: stakeholder-driven governance, transparent operations, and a documented wind-down plan.

This article does not claim the protocol solves the reproducibility crisis, eliminates prestige bias, or fully domesticates AI in research. It claims only that these problems are materially harder to solve without version control, provenance, and structured metadata as foundational infrastructure. By supplying that infrastructure, the protocol makes direct evaluation of research at scale technically feasible for the first time. The scientific community can now choose whether to use it.

---

## Acknowledgments

AI assistants (Claude Opus 4.8, Grok 4.20, Gemini 2.5 Pro) were used for initial literature search, for software development — implementing and running the companion computation script(s) that reproduce the paper's reported numerical and simulation results — and for editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility. Here the companion software is the federated cross-owner linker (`negotiate_modules.py`) and the single-author linker it generalizes (`build_ontology.py`), which produce the three negotiation experiments of Section 5.6 from author-transcribed module sets; the author reviewed the code and verified that all three runs reproduce deterministically.

---

## References

::: {#refs}
:::
