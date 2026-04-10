# Research as Repository: A Git-Native Protocol for Scientific Knowledge Production

**Dmitry Zharnikov**

Working Paper v1.1 — April 2026

---

## Abstract

Scientific evaluation relies on a self-reinforcing loop: universities evaluate researchers by journal prestige, journals evaluate papers partly by institutional affiliation, and no one evaluates the research directly — because direct evaluation at scale has lacked the necessary infrastructure. This paper proposes a protocol that provides that infrastructure by treating every research program as a version-controlled repository. A paper is a render of the research at a point on its timeline: a frozen snapshot forked to a journal so the community can confirm the findings. The protocol introduces fork-based submission, automated compliance gates, attributed reviewer commits, provenance chains, structural funding and affiliation metadata, AI-traceability by design — every AI-assisted edit becomes a commit with auditable metadata — and a commit-reveal privacy primitive that lets researchers establish cryptographic priority and provenance through public commit hashes while keeping content disclosure under their control. The protocol further introduces a Research Wiki layer within the repository — adapting Karpathy's (2026) three-layer knowledge pattern — that creates five types of git-timestamped intellectual work proof: discovery (when a source was first encountered), priority (when an idea was first articulated), attestation (when an idea was shared with a third party), derivation (how the argument developed from sources to conclusions), and independence (whether researchers developed ideas independently). The protocol optimizes the knowledge production process, not the paper: existing publishing reforms improve the rendered artifact; this protocol makes the research itself structurally transparent. Combined with the Paper Spec standard (Zharnikov, 2026t), which specifies what a paper claims, the repository protocol specifies how the research was built, evaluated, and decided upon.

**Keywords**: scientific publishing, version control, peer review, research infrastructure, open science, provenance, knowledge production, research evaluation, AI transparency, intellectual work proof, research wiki, scholarly communication

---

## 1. Introduction

### 1.1 The Document Assumption

The global scientific publishing system processes approximately 3 million papers per year (UNESCO, 2021) through a pipeline built on a single assumption: a paper is a document. A PDF file. A static artifact transmitted from author to editor to reviewer to publisher. Every tool in the pipeline — manuscript submission portals, editorial management systems, reviewer interfaces, typesetting workflows — treats the paper as an opaque binary object that moves between mailboxes.

This assumption was adequate when papers were physically printed and mailed. It is now a significant structural constraint on every reform the scientific community has attempted in the past two decades.

Open access reforms — accelerated by mandates such as Plan S (cOAlition S, 2018) — change *who can read* the document. They do not change the document. Preprint servers change *when* the document becomes available. They do not change its structure. Registered reports change *what sequence* the document follows. They do not change how it is tracked. Post-publication review adds commentary *about* the document. It does not integrate with the document's own history.

Each reform addresses one dimension of the publishing problem while leaving the document assumption intact. The result is a system that has been incrementally improved on six dimensions simultaneously — access, timing, sequence, commentary, data sharing, reproducibility — without any reform touching the structural foundation that constrains all of them.

Scientific publishing is the only knowledge-intensive domain without formal version control and provenance infrastructure. Legal systems track case law revisions. Financial auditing requires audit trails. Clinical research mandates trial registration. Supply chain management maintains chain of custody. Software engineering uses Git. Each domain independently developed provenance tracking because each discovered that knowledge integrity requires it. Publishing has not.

**Table 1.** Provenance mechanisms across knowledge-intensive domains.

| Domain | Provenance mechanism | When adopted |
|--------|---------------------|-------------|
| Legal | Case law revision tracking, legislative history | 19th century |
| Financial auditing | Audit trails, SOX compliance | 1930s (SEC), 2002 (SOX) |
| Clinical research | Trial registration (clinicaltrials.gov) | 2005 (ICMJE requirement) |
| Supply chain | Chain of custody, GS1 standards | 1970s-2000s |
| Software engineering | Version control (CVS→SVN→Git) | 1986-2005 |
| Scientific publishing | None (document assumption) | — |

Software engineering faced the same problem in the 1990s. Source code was treated as a collection of files transmitted between developers via email, FTP, or shared drives. Every collaboration problem — tracking changes, attributing contributions, managing parallel versions, reverting errors — was solved ad hoc. The solution was not incremental improvement of file-sharing tools. It was a structural reconception: source code is not a collection of files. It is a *repository* — a versioned, branched, contributor-attributed, cryptographically auditable history of every change ever made.

Git (Torvalds, 2005) implemented this reconception. Ram (2013) demonstrated that Git can facilitate greater reproducibility and transparency in science, and Bryan (2018) provided the pedagogical bridge — showing working scientists how version control integrates into everyday research practice. Within a decade, Git became the universal infrastructure for collaborative software development. GitHub (2008) added the social and collaboration layer: forking, pull requests, issue tracking, and visibility. The combination transformed software from an opaque craft practice into a transparent, auditable, contributor-traceable engineering discipline.

This paper proposes the same structural reconception for scientific research. The reconception produces a four-level hierarchy:

1. A **research program** is a repository — the single source of truth, evolving over time.
2. A **paper** is a render of that repository at a point on its timeline — a frozen snapshot, a communication event.
3. A **submission** is a fork — sharing that render with the community for confirmation.
4. A **publication** is a merge — acceptance of the fork into a journal's curated collection.

A paper is not a document. It is a tagged release from a repository, frozen at a specific stage and forked to a journal for evaluation. The submission process is not a file transfer. It is a fork request. Peer review is not an email exchange. It is a set of attributed commits on a review branch. Publication is not a format conversion. It is a merge into a journal's collection with a minted DOI.

### 1.2 What the Protocol Replaces

The urgency of structural reform is well established. Ioannidis (2005) demonstrated that most published research findings are false — a conclusion driven in part by the absence of transparent, auditable research processes. The TOP Guidelines (Nosek et al., 2015) defined eight transparency standards for open research culture, but implementing those standards within the current document paradigm remains difficult because the paradigm itself lacks the infrastructure for structured transparency.

The current pipeline has five structural gaps that are difficult to address within the document paradigm:

**Gap 1: No version history.** The reproducibility crisis prompted a wave of editorial reform (McNutt, 2014), yet the underlying infrastructure remains unchanged. Stodden, Seiler, and Ma (2018) found that even among journals with explicit reproducibility policies, fewer than 40% of their sampled articles made code and data available — demonstrating that policy without infrastructure fails. A submitted manuscript has no auditable record of how it was written. The editor sees a finished product. The twenty drafts, the deleted sections, the data re-analyses, the contributor who rewrote Section 4 — all invisible. When questions arise about research integrity, the only evidence is the authors' word and whatever files happen to be on their hard drives.

**Gap 2: No contributor traceability.** CRediT (Contributor Roles Taxonomy) added contributor roles to published papers in 2014. But CRediT is a self-reported annotation attached to the final document. It has no connection to the actual work. There is no mechanism to verify that the person listed as "Methodology" actually wrote the methods section. The contribution record is a claim, not a proof.

**Gap 3: No submission provenance.** When an author submits to Journal A, Journal B has no way to know. Dual submission policies rely entirely on author honesty. When a paper is rejected by three journals and accepted by the fourth, the fourth journal's editor has no access to the prior reviews. The same paper is re-reviewed from scratch at each venue — a massive duplication of expert labor.

**Gap 4: No review attribution.** Peer reviewers contribute substantive intellectual work — identifying errors, suggesting improvements, catching methodological flaws. Their contributions are acknowledged in a single generic sentence ("We thank the anonymous reviewers") and then erased. A reviewer who saves a paper from a fatal statistical error receives the same credit as one who submits a two-sentence review: none.

**Gap 5: No machine interface.** The entire pipeline is human-readable only. A PDF cannot be queried, diff'd, branched, or programmatically analyzed without lossy conversion. AI tools that could assist with literature review, consistency checking, or cross-paper analysis must first solve the extraction problem — converting unstructured text back into structured data — before doing any useful work.

The protocol proposed here closes all five gaps by replacing the document assumption with a repository assumption. The paper becomes a Git repository. Submission becomes a fork. Review becomes a branch. Publication becomes a release. Every operation is versioned, attributed, and machine-readable by construction.

### 1.3 Relationship to Prior Work

The Paper Spec standard (Zharnikov, 2026t) addresses Gap 5 by defining a machine-readable YAML companion file (`paper.yaml`) that captures what a paper claims, what would falsify those claims, and what the paper depends on. Paper Spec is the *specification layer* — it declares the paper's epistemic content in structured form.

**Paper Spec in brief.** The Paper Spec standard (Zharnikov, 2026t) defines a YAML companion file (`paper.yaml`) with five structural elements: (1) typed claims with unique identifiers and dependency links; (2) methodology description with reproducibility requirements; (3) acceptance criteria — what would confirm each claim and, critically, what would falsify it; (4) a dependency graph linking claims to prior work with criticality flags; and (5) submission history tracking venue, decision, and revision scope. The standard is published as an open repository with 20 worked examples from published research (github.com/spectralbranding/paper-spec). The present protocol treats `paper.yaml` as one file in the repository structure; Paper Spec defines its internal schema.

The present protocol is the *process layer* — it specifies how the paper is built, submitted, reviewed, and published. Paper Spec and Research-as-Repository compose: `paper.yaml` travels with the repository, is versioned alongside the manuscript, and is included in every fork. Together, they make both the content and the lifecycle of a paper fully machine-readable.

The Registered Reports format (Chambers, 2013) addresses the sequence problem by splitting peer review into pre-data and post-data stages. The present protocol subsumes Registered Reports as a special case: a Stage 1 submission is a fork at a specific commit; Stage 2 is a subsequent fork from a later commit in the same repository. The fork chain records the two-stage structure automatically.

DORA (San Francisco Declaration on Research Assessment, 2012), the Leiden Manifesto (Hicks et al., 2015), and CoARA (Coalition for Advancing Research Assessment, 2022) all advocate for multi-dimensional research evaluation. The present protocol provides the infrastructure that makes multi-dimensional evaluation tractable: when every contribution, every review, and every decision is recorded in structured form, evaluation can query specific dimensions rather than collapsing to scalar proxies.

### 1.4 The Value Stream: Knowledge Development as the Core Process

Existing reform proposals — and the platforms that implement them — share a common limitation: they optimize individual stations on the publishing production line without examining the production line itself.

Manubot (Himmelstein et al., 2019) improves authoring. COAR Notify improves cross-platform notification. ORKG (Auer, 2019) improves indexing. Signposting improves machine discovery. Each addresses one gap — and each optimizes the *paper* (the rendered artifact). Open access optimizes who can read the paper. Preprints optimize when the paper becomes available. Registered reports optimize what sequence the paper follows. JATS XML optimizes the paper's machine-readability.

The present protocol does not optimize the paper. It optimizes the *knowledge production process* that papers communicate. The repository is the research — the evolving SSOT where knowledge is built. Papers are renders of that research at specific stages, shared with the community for confirmation. The distinction is not semantic. When you optimize the paper, you get better documents. When you optimize the knowledge process, better papers follow as a structural consequence — just as better brand signals follow from a well-specified brand architecture, rather than the reverse.

None of the existing reforms asks the structural question: *what is the value stream of scientific knowledge production, and which activities on the production line are value-creating versus waste?*

Lean manufacturing (Ohno, 1988) distinguishes between value-creating activities (those the customer would pay for) and muda (waste — activities that consume resources but do not create value). Applied to scientific publishing:

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

This reflects a principle well established in process reengineering (Hammer & Champy, 1993) and Lean thinking (Womack & Jones, 1996): specify the process first, then derive the organizational structure from the process — not the other way around. Organizational Schema Theory (OST) formalizes this principle for organizational design (Zharnikov, 2026i); the present protocol applies it to scholarly communication. Current scientific publishing derives its processes from its organizational structure (journals define formats, timelines, and workflows; researchers conform). The protocol inverts this: the knowledge development process defines the requirements; journals, preprint servers, and review systems are services that fulfill those requirements.

This inversion shifts the value of journals to a different level. In the document paradigm, the journal is the destination — research culminates in publication. In the repository paradigm, knowledge development is the core process and it continues regardless of any single publication event. A journal publication is not an endpoint but a *peer alignment event*: a synchronization point where the scientific community confirms that a render of the ongoing research is sound at this stage. The research repository existed before the fork and continues after the merge. The journal's role is not to validate the research (that is the community's function) but to curate the alignment — selecting which renders, at which stages, merit community attention. Publications are important, but they are instruments of peer alignment, not the core process itself.

### 1.5 Related Work

Several platforms and standards address subsets of the gaps identified above. None integrates all five into a unified protocol.

**Table 2a.** Protocol feature coverage. Columns indicate whether a system supports each of the six protocol features described in Section 1.2. Full = structurally integrated; Partial = addressed but not fully integrated; No = not addressed.

| System | VC | Fork | Gate | Rev | Prov | Coll |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|
| Manubot (Himmelstein et al., 2019) | Full | -- | -- | -- | -- | -- |
| JOSS (Katz et al., 2018) | Full | Partial | Partial | Full | -- | -- |
| Octopus.ac (Freeman, 2021) | Partial | -- | -- | Full | Partial | -- |
| OJS/PKP (Willinsky, 2005) | -- | -- | Partial | -- | -- | -- |
| COAR Notify | -- | -- | -- | -- | Partial | Partial |
| Signposting | -- | -- | -- | -- | -- | Partial |
| CryptSubmit (Gipp et al., 2017) | -- | -- | -- | -- | Full | -- |
| PubPub (MIT Media Lab) | Partial | -- | -- | -- | Partial | -- |
| eLife (Eisen et al., 2022) | -- | -- | -- | Partial | -- | Partial |
| RO-Crate (Soiland-Reyes et al., 2022) | -- | -- | Partial | -- | -- | Partial |
| FAIR4RS (Barker et al., 2022) | -- | -- | -- | -- | -- | -- |
| DataCite | -- | -- | -- | -- | -- | Partial |
| **This protocol** | **Full** | **Full** | **Full** | **Full** | **Full** | **Full** |

Column key: VC = version control, Fork = fork-based submission, Gate = compliance gate, Rev = reviewer attribution, Prov = provenance chain, Coll = collections as users. Dashes indicate the feature is absent.

**Table 2b.** System context and adoption.

| System | Adoption | Key limitation |
|--------|----------|----------------|
| Manubot | ~500 papers | Authoring only, no submission/review |
| JOSS | ~3,000 papers | Software papers only |
| Octopus.ac | Pilot (2022-) | Proprietary platform, not Git-native |
| OJS/PKP | 25,000+ journals | No version control, no structured review |
| COAR Notify | Pilot (2023-) | Notification only, no manuscript management |
| CryptSubmit | Prototype (2017) | Timestamping only, no full lifecycle |
| PubPub | ~200 communities | Web-native, not Git-native |
| eLife | Active (2022-) | Platform-specific, not protocol-native |
| RO-Crate | Growing adoption | Packages artifacts, not processes |
| This protocol | Proposal | Partial prototype: compliance gate, schemas, validator, self-referential implementation (github.com/spectralbranding/paper-repo). Fork lifecycle and federation: conceptual |

The table reveals a structural distinction. RO-Crate packages research artifacts (data, code, documents) with rich metadata into a standardized container — it is preservation-focused. FAIR4RS extends the FAIR principles (Wilkinson et al., 2016) to research software, defining machine-readable metadata requirements for findability, accessibility, interoperability, and reusability. DataCite provides DOI minting and metadata standards for research data. These standards focus on *artifacts* — the outputs of research. The present protocol focuses on the *process* — how those artifacts are authored, submitted, reviewed, and decided upon. The two concerns are complementary: an RO-Crate can package a paper repository's artifacts; FAIR4RS principles inform how the repository's code and scripts are documented; DataCite-compatible DOIs are minted for releases and forks. The protocol inherits these standards rather than replacing them.

eLife's "Publish, then Review" model (Eisen et al., 2022) is the closest real-world implementation of the "collections as users" concept: authors post preprints first, and eLife curates reviewed preprints into its collection with public reviews attached. The model demonstrates that decoupling publication from review is operationally viable — but it remains platform-specific rather than protocol-native. The present protocol generalizes this pattern: any collection user can curate any repository fork, with review records that are portable across venues.

Manubot is the closest predecessor for the authoring layer — it implements Git-native collaborative writing with CI/CD rendering (Himmelstein et al., 2019). The present protocol extends this pattern from authoring to the full submission-review-publication lifecycle. JOSS implements review-as-GitHub-issues for software papers; the present protocol generalizes this to all disciplines with structured reviewer commits rather than free-form issue comments. Octopus decomposes papers into modular linked units with open review — sharing the modular philosophy but using a proprietary platform rather than Git repositories. Overlay journals (e.g., Discrete Analysis on arXiv) already implement a lightweight version of "collections as users" by curating papers hosted on preprint servers.

The protocol's contribution is not any single feature but the integration: a unified Git-native lifecycle where authoring, compliance, submission, blinding, review, provenance, and publication are operations on a single versioned repository.

### 1.6 Claims

This paper advances seven claims:

1. **C1.** Fork-based submission creates cryptographic provenance that makes submission history structurally auditable.
2. **C2.** Blinding-as-function replaces manual anonymization with a configurable system property.
3. **C3.** Review-as-commits creates attributed, portable review records with measurable depth.
4. **C4.** Collections-as-users unifies preprint servers, journals, and archives under a single protocol.
5. **C5.** A compliance gate (`journal_spec.yaml`) substantially reduces formatting-related desk rejections.
6. **C6.** Provenance-by-design makes dual submission structurally detectable.
7. **C7.** The protocol's machine-readable structure enables AI-native querying across the full research lifecycle.

Each claim includes a falsification condition specified in the accompanying `paper.yaml`.

---

## 2. The Protocol

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

The manuscript (`paper.md`) is the single source of truth. All renderings are generated from it: structurally meaningful outputs (JATS XML for indexing, HTML for web display) and legacy compatibility outputs (PDF, DOCX) that serve readers and venues not yet operating on the repository directly. The repository contains the generating function, not the rendered output. Software tools used in the analysis are cited following the FORCE11 software citation principles (Smith et al., 2016), with version, DOI, and repository URL recorded in `paper.yaml` dependencies.

The protocol does not mandate Markdown specifically. Any plain-text, diff-friendly format serves as the SSOT: Markdown, LaTeX, Quarto, or R Markdown. The essential requirement is that the source format is version-controllable (plain text, not binary) and renderable to multiple outputs. Fields that predominantly use LaTeX (physics, mathematics) or Word (biomedical, humanities) would require either format bridging tools or a GUI abstraction layer that presents the Git operations through a familiar editing interface — analogous to how GitHub Desktop made Git accessible to non-engineers.

JATS XML (Journal Article Tag Suite) is the dominant machine-readable format for published articles. The protocol does not replace JATS — it generates JATS as one rendering output from the repository source. The submission gate (Section 2.3) can include JATS validation as a compliance check. The relationship is: the repository stores the source; JATS is one of several delivery formats the CI pipeline produces.

**The two-layer architecture: text in Git, data in archives.** Scientific papers across all disciplines produce two categories of artifacts: text-based artifacts (manuscripts, code, analysis scripts, small structured data) and binary/large artifacts (microscopy images, genomic sequences, medical imaging, satellite data, audio recordings, simulation outputs). Git handles the first category natively. It handles the second category poorly — storing full copies of every version of every binary file makes repositories impractically large.

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

`DATA_MANIFEST.yaml` in the repository declares every external data dependency with its DOI, checksum, and access conditions — extending Altman and King's (2007) proposed standard for scholarly citation of quantitative data from a citation convention to a machine-enforceable dependency:

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

**Figure 1.** Architecture of the fork-based submission lifecycle.

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

**Table 3.** Compliance gate checks and implementation difficulty.

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

The protocol supports all modes identified in Ross-Hellauer's (2017) systematic taxonomy of open peer review, and the structured commit model accommodates the emergent innovations catalogued by Tennant et al. (2017). The reviewer's identity on the branch is controlled by the editor:

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

The reviewer controls which individual reviews are public, but aggregate statistics (total count, average depth, journal list) are always visible. Early evidence suggests that open reviewer identification does not reduce review quality (van Rooyen et al., 1999). This creates verifiable review reputation without requiring full transparency.

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

The most radical architectural implication: if every paper is a repository, then preprint servers, journals, and institutional archives are not platforms — they are **users** on a shared platform who curate collections of frozen forks.

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

`CONTRIBUTORS.yaml` in the research repository links to each contributor's profile rather than duplicating affiliation data. When a paper is forked, the system resolves: "at the time of the commits in this fork, what was this contributor's affiliation?" The answer comes from the researcher's profile timeline intersected with the commit timestamps — not from a form field. This eliminates the "affiliation at time of research vs. affiliation at time of publication" footnote problem that currently requires manual disambiguation. Verification is structural: a commit signed from an `@mit.edu` email domain corroborates an MIT affiliation entry, and an institution can optionally GPG-sign the profile entry to confirm the appointment.

The three-level separation — affiliations (person), funding (project), authorship (paper) — means each can be updated independently without touching the others, and each is verified against its own source of truth rather than self-reported on a form.

### 2.10 Federation and Local Sovereignty

A critical design constraint: scientists will not entrust their life's work to a centralized platform they do not control. Any protocol that requires a single hosting provider — even a well-intentioned one — replicates the power dynamics of the current publisher oligopoly in a new form.

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

When every paper is a repository with structured metadata (`paper.yaml`), machine-readable content (Markdown), and auditable provenance (`PROVENANCE.yaml`), the entire corpus becomes queryable:

**Cross-paper consistency**: An AI agent can detect when Paper B's claims depend on Paper A's results, and Paper A has been retracted or revised. The dependency chain is explicit in `paper.yaml`.

**Real-time literature review**: "Find all papers whose claims depend on Peters (2019) ergodicity framework and have been accepted by a Q1 journal in the last 6 months" — answerable in seconds from structured metadata.

**Language independence**: The repository stores structured claims. An AI can translate the natural-language manuscript while preserving the machine-readable claim structure. A Japanese researcher can read a Brazilian paper's claims in Japanese, verify them against the original structured metadata, and cite the specific claim by ID.

**Change propagation**: When a foundational paper updates a key result, every paper that cites that result can be automatically flagged. The dependency graph is explicit. Currently, citation is a string in a reference list. In the repository protocol, citation is a typed link to a specific claim in a specific version of a specific repository.

**Reviewer assistance**: An AI can pre-screen a fork against the journal's scope, check the `paper.yaml` claims for internal consistency, flag potential conflicts with known results, and prepare a structured briefing for the human reviewer — all before the reviewer opens the manuscript.

**AI contribution traceability**: Git does not just track the researcher's work. It tracks their AI's work too. Every AI-assisted edit becomes a commit with structured metadata: the tool used, the model version, and a hash of the prompt that generated the output. This makes AI contribution structurally transparent and auditable — not as a self-reported disclosure statement, but as a verifiable chain of operations embedded in the repository's history. The AI disclosure problem that journals are currently struggling to solve through policy becomes an engineering problem with an engineering solution: the commit log.

### 2.12 Toward a Normative Specification

The preceding sections describe the protocol conceptually — its architecture, its components, and their interactions. A production-grade implementation requires a normative specification: a formal, unambiguous document that defines message formats, authentication flows, error handling, and API contracts with sufficient precision that independent implementers can build interoperable systems.

The normative specification would contain four structural components:

**Message schemas.** Every interaction between protocol participants — fork requests, review responses, editorial decisions, provenance queries, collection acceptance notifications — requires a formally defined message format. These schemas would specify required and optional fields, data types, validation rules, and versioning semantics. The COAR Notify protocol (which defines notifications between repositories and review services) provides a foundation: the Research-as-Repository protocol can extend COAR Notify's Linked Data Notifications with paper-specific message types (fork-request, review-commit, decision-record, provenance-query).

**Authentication and signing.** The provenance chain's integrity depends on verified identity. GPG-signed commits — already standard in high-security software development — provide cryptographic proof that a specific person made a specific change at a specific time. The normative specification would define an institutional key infrastructure: universities and publishers maintain signing keys; individual researchers sign with ORCID-linked keys; AI tools sign with tool-specific keys that encode model version and configuration. Signposting (typed HTTP links for scholarly objects) provides the discovery layer: a paper repository's landing page advertises its provenance endpoint, its review branches, and its collection memberships through machine-readable link headers.

**Error handling.** Production systems fail. The specification must define behavior for validation failures (which checks are blocking vs. advisory, how failures are reported, what retry semantics apply), conflict resolution (what happens when two forks target the same journal simultaneously, how merge conflicts in review branches are resolved), and timeout policies (how long a fork remains active before automatic expiration, what happens to review branches when a reviewer becomes unresponsive).

**API endpoints.** The federation protocol (Section 2.10) requires a defined interface — whether REST endpoints, protocol-level messages, or both — through which independent hosts exchange provenance metadata, fork requests, and decision records. DataCite's REST API for DOI minting and metadata retrieval provides a model for the provenance query interface. ORCID's OAuth-based identity verification provides a model for the authentication flow.

The normative specification is future work. It requires multi-stakeholder input from publishers (who must implement fork acceptance and review branch management), libraries (who must implement collection curation and long-term preservation), platform providers (who must implement the federation protocol), and researchers (who must validate that the specification serves their workflows without imposing unreasonable burden). The governance model — whether the specification is maintained by an existing standards body (NISO, W3C, IETF) or a new consortium — is itself a design decision that affects adoption. The conceptual architecture in this paper is the necessary prerequisite: one must know what the protocol does before specifying how it does it.

### 2.13 The Research Wiki: Structured Knowledge Accumulation

The repository protocol addresses how research is built, evaluated, and decided upon. It does not address how the researcher *organizes the knowledge that informs the research* — the literature, the sources, the correspondence, the evolving understanding that precedes and surrounds the paper. This gap is currently filled by reference managers (Zotero, Mendeley, EndNote) that operate outside the research repository: no version control, no provenance chain, no structural integration with the paper's claims. The researcher's intellectual process — what was read, when, in what order, and how it influenced the argument — is invisible.

Karpathy (2026) proposes a three-layer pattern for personal knowledge management: raw sources (immutable ground truth), a wiki (LLM-maintained structured knowledge), and a schema (specification governing what the wiki tracks). The pattern applies directly to research: the sources are the literature and data the researcher consults; the wiki is the organized, cross-referenced understanding; the schema defines the research program's knowledge structure.

We propose an optional `.wiki/` directory within the research repository:

```
research-repo/
  paper.md
  paper.yaml
  experiment/
  .wiki/                          # Research knowledge base
    schema.yaml                   # What to track and how to organize
    sources/                      # Raw materials (PDFs, URLs-as-markdown, datasets)
    pages/                        # LLM-maintained wiki pages (by topic, author, concept)
    correspondence/               # Emails, messages, reviews (redactable)
    ingest.jsonl                  # Chronological source ingestion log
    contradictions.md             # Sources that conflict with paper's claims
    .gitignore                    # Optional: exclude large PDFs from public push
```

The `.wiki/` directory is dot-prefixed by convention (hidden in standard directory listings) and can be selectively excluded from public repository access via `.gitignore` while retaining full git history locally. The researcher controls what is shared. The provenance chain — *when* each source was added, *what* was read, *how* the understanding evolved — is preserved regardless.

#### 2.13.1 Intellectual Work Proofs

The research wiki creates five structurally distinct types of intellectual work proof, each addressing a different verification need. All derive from git's cryptographic properties: every commit is SHA-256 hashed, timestamped, and signed, creating a tamper-evident chain.

**Discovery proof.** When was a source first encountered? The `ingest.jsonl` log records each source addition with a timestamp, file hash, and optional annotation. A researcher who adds `smith-2024-brand-equity.pdf` on February 12 has a cryptographically verifiable record of access to that source on that date. This is currently unprovable — reference managers record when a citation was added to a library, but not when the source was actually read or consulted, and the record is not tamper-evident.

```jsonl
{"timestamp": "2026-02-12T14:23:07Z", "action": "ingest", "source": "smith-2024-brand-equity.pdf", "sha256": "a3f2...", "note": "Found via backward citation from Jones (2023). Relevant to H2."}
{"timestamp": "2026-02-15T09:41:33Z", "action": "ingest", "source": "https://doi.org/10.1234/example", "sha256": "b7c1...", "note": "Peters (2019) ergodicity framework. Restructures Section 3 argument."}
```

**Priority proof.** When was an idea first articulated? The commit history shows the exact moment a concept appeared in the manuscript. A diff between consecutive commits reveals: "On March 3, the author added the concept of dimensional collapse to Section 4." If two researchers independently develop the same idea, git timestamps establish priority to the commit — not to the publication date, which may lag by months or years.

**Attestation proof.** When was an idea shared with a third party? The `.wiki/correspondence/` directory stores emails, messages, or review exchanges where the researcher communicated ideas to others. A researcher who emails a colleague on January 15 describing a novel method, and adds that email to the repository on January 16, has a git-timestamped record that the idea existed and was communicated before the paper was written. The correspondent can independently verify the exchange if a dispute arises. Correspondence can be stored in full, redacted (with the unredacted version's hash preserved for future verification), or as metadata-only entries (date, correspondent, subject, hash of original).

```jsonl
{"timestamp": "2026-01-16T08:12:00Z", "action": "correspondence", "type": "email_sent", "to": "colleague@university.edu", "subject": "New method for dimensional weight estimation", "sha256_of_original": "d4e5...", "redacted": true, "note": "Described the PDOP approach before drafting Section 3."}
{"timestamp": "2026-03-22T11:30:00Z", "action": "correspondence", "type": "message_received", "from": "reviewer@journal.org", "subject": "Pre-submission feedback", "sha256_of_original": "f6a7...", "note": "Suggested adding Monte Carlo validation. Led to Section 9.6."}
```

**Derivation proof.** How did the argument develop? The full commit history of the paper — not just the final version — shows the intellectual trajectory: which sources led to which ideas, which ideas were abandoned, which were restructured. A reviewer or evaluator can inspect the diff graph and see: "The author initially framed this as a measurement problem (commits 1-12), then reframed as a geometric estimation problem after encountering DeSarbo and Rao (1986) on February 20 (commit 13), and the current argument crystallized after the Monte Carlo simulation on April 5 (commit 34)." This is the intellectual equivalent of a lab notebook — currently absent from all published research.

**Independence proof.** Did the researcher develop an idea independently of another researcher? If two groups publish similar findings, the git history of each repository can establish: (a) when each group first committed the idea, (b) whether either group had access to the other's work (via `ingest.jsonl` — if the other group's preprint was never ingested, independence is structurally demonstrated), and (c) the derivation path that led each group to the same conclusion independently. This addresses a verification need that the current system handles only through informal attestation ("we developed this independently") with no structural evidence.

#### 2.13.2 The LLM-Maintained Knowledge Layer

The wiki pages in `.wiki/pages/` are not manually maintained. Following Karpathy's (2026) pattern, the LLM processes each ingested source and updates the relevant wiki pages: adding cross-references, noting contradictions, linking to the paper's claims. The `schema.yaml` governs what the wiki tracks — for a brand perception research program, this might include pages per theoretical construct, per cited author, per methodology, and per dataset. The schema is itself version-controlled, so changes in research focus are traceable.

Three maintenance operations map directly to the research workflow:

**Ingest.** A new source (PDF, URL, dataset, correspondence) is added to `sources/`. The LLM reads it, updates relevant wiki pages, adds entries to `ingest.jsonl`, and flags any contradictions with the paper's current claims.

**Query.** The researcher asks a question ("Which papers use Bayesian heterogeneity models for brand positioning?"). The LLM searches wiki pages and synthesizes an answer. Valuable findings are filed back into the wiki, making the knowledge base self-improving.

**Lint.** The LLM performs health checks: orphan pages (sources cited in the paper but missing from the wiki), missing cross-references, contradictions between wiki pages and the paper's current claims, and citation completeness (every reference in `paper.yaml` should have a corresponding source in `.wiki/sources/`).

The lint operation is particularly powerful for citation integrity. A paper that claims 45 references but whose wiki contains only 38 source files has 7 citations that may be fabricated, copied from another paper's reference list, or added without consulting the source. This does not prove fabrication — the researcher may have consulted a library copy — but it creates a structural signal that current publishing infrastructure cannot detect at all.

#### 2.13.3 Privacy and Selective Disclosure

The research wiki is private by default. The `.gitignore` file within `.wiki/` can exclude large source files (PDFs) from the public repository while preserving their metadata (filenames, SHA-256 hashes, timestamps) in the tracked `ingest.jsonl`. This creates a verifiable chain without publishing copyrighted materials: the hash proves the researcher possessed a specific version of a specific file at a specific time, without distributing the file itself.

Selective disclosure supports multiple scenarios:

- **Standard submission**: `.wiki/` excluded from the public fork. The paper stands on its own merits.
- **Transparency signal**: `ingest.jsonl` included in the public fork. Reviewers can verify the chronological development of the knowledge base.
- **Full disclosure**: `.wiki/` fully public. The research process itself becomes a citable artifact.
- **Audit response**: `.wiki/` disclosed to a specific party (institution, funder, ethics board) in response to a verification request, without public disclosure.

The choice is the researcher's. The protocol does not mandate disclosure — it makes disclosure possible, verifiable, and granular.

#### 2.13.4 The Commit-Reveal Mechanism

The same privacy primitive that protects copyrighted source PDFs in the wiki applies to the researcher's own work. A commit hash is a tamper-evident fingerprint. Publishing the hash is not the same as publishing the content — and this distinction resolves the apparent trade-off between open science and confidentiality that has historically blocked git-native research adoption in academia.

Concretely: every commit in a research repository produces a SHA-256 hash that uniquely identifies the contents of the repository at that moment, signed by the author's GPG key, and timestamped by the git history (or anchored externally to a public timestamping service for stronger guarantees). The hash can be made public — establishing that the work in this exact form existed at this exact moment, by this exact author — without revealing what the work contains. Any third party who later receives the contents can recompute the hash and verify that nothing has been altered between commit time and disclosure time.

This is **commit-reveal**: priority and provenance are established immediately at the moment of commit; content disclosure stays under the author's control and can be made selectively, partially, conditionally, or never. The mechanism applies uniformly to all artifacts in the repository — drafts, datasets, derivations, claims, correspondence — not just to imported sources subject to copyright.

The mechanism supports several disclosure architectures that previously required either premature publication or trust in centralized intermediaries:

- **Solo private repository with public hash anchors**: A researcher works in a fully private repository. At meaningful milestones (a key derivation, a hypothesis pre-registration, a draft completion), the researcher publishes the current commit hash to a public anchor (a tweet, a blog post, a hash-only registry, a blockchain timestamp). The hash establishes the existence of that exact state on that exact date. Years later, in the event of a priority dispute, the researcher reveals the contents and any party can verify that the disclosed file produces the previously published hash.
- **Consortium private branch with public anchors**: A multi-institution collaboration runs a shared private branch. Periodic commit hashes are published to a public registry. The collaboration retains exclusive access to the contents while accumulating an unfalsifiable public timeline of progress. If a member institution leaves and disputes priority, the public anchors resolve the question.
- **Hybrid public-private repository**: Some directories are public (e.g., `paper.yaml`, `references/`), others are private (e.g., `.wiki/`, raw data). The commit graph is partially visible. Hashes of the private directories appear in the commit history and can be cited even when the directories themselves are not browsable.
- **Embargoed disclosure**: A paper is committed in full at time *t*, but the public reveals only the hash. At time *t + n* (after a journal embargo, a patent filing, or a coordinated multi-paper release), the contents are made public. The hash proves the contents have not been edited during the embargo period.

For misconduct prevention specifically, this is the structural alternative to centralized institutional databanks. A scientist's reputation is the verifiable history of their commits. There is no need for an institution to "report" misconduct to a central registry at the moment of an employment transition: the misconduct, if it occurred, is visible (or at minimum, the absence of any verifiable record of the work is visible) at the granularity of the commit graph. A researcher who fabricates results cannot retroactively edit a signed, hashed commit without breaking the chain. A researcher who plagiarizes cannot claim priority over a hash that was published before they joined the field.

The protocol does not require any researcher to make their work public. It requires only that the choice of when, what, and to whom to disclose belongs to the researcher — and that the cryptographic infrastructure makes that choice meaningful, granular, and verifiable.

---

## 3. Design Principles

### 3.1 Single Source of Truth (SSOT)

The author's repository is the one and only source of truth for the paper. All other representations — PDFs, preprints, published versions, translations — are renderings. If the rendering disagrees with the repository, the repository is correct.

This inverts the current hierarchy, where the published PDF is the canonical version and the author's files are disposable. In the repository protocol, the published version is a tagged release from the repository — one rendering among many, distinguished only by its DOI and journal badge.

### 3.2 Functions by Design

Every feature that the current system implements through policy, the repository protocol implements through structure:

**Table 4.** Policy-based vs structure-based implementation of publishing functions.

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

The four-level hierarchy introduced in Section 1.1 — repository, paper, fork, publication — is not merely an analogy to software engineering. It is an instance of a general structural pattern: the specification-implementation-perception pipeline, in which a specification is rendered into an implementation that produces observer-dependent perception.

**The hierarchy.** The mapping is exact:

1. **Research program = repository.** The single source of truth for the research, evolving across commits. Analogous to a brand specification or an organizational schema.
2. **Paper = render.** A frozen snapshot of the research at a specific commit — a communication event, not the research itself. Analogous to brand signals emitted into the market or operational processes executed by an organization.
3. **Fork = sharing.** The render is transmitted to the community for confirmation. The fork is lossy: no single paper captures the full repository, just as no single brand interaction captures the full brand specification.
4. **Publication = merge.** The community (journal) evaluates the render and either merges it into its collection or closes the fork. Analogous to the perception that forms after the signal reaches its audience.

**Table 5.** Cross-domain comparison: specification-rendering-perception across three sibling frameworks.

| Structural layer          | Branding (SBT)             | Organization (OST)         | Research (this protocol)   |
|---------------------------|----------------------------|----------------------------|----------------------------|
| Specification             | Brand spec (8 dimensions)  | Org schema (L0-L5)         | Research repository (SSOT) |
| Implementation / Render   | Brand signals (emissions)  | Operations (processes)     | Paper (frozen snapshot)    |
| Perception / Evaluation   | Perception cloud (observer)| Performance metrics        | Community review (peers)   |

The rendering is lossy at every layer. A brand specification cannot be fully conveyed by any finite set of signals. An organizational schema cannot be perfectly executed by any operational process. A research repository cannot be fully captured by any single paper. And the perception is observer-dependent: different consumers perceive different brands from the same signals; different employees experience different organizations from the same processes; different reviewers perceive different papers from the same manuscript.

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

The urgency of structural AI traceability is no longer hypothetical. Lu et al. (2026) demonstrate a fully autonomous AI system — The AI Scientist — that generates research ideas, runs experiments, writes complete manuscripts, and performs its own peer review. An AI-generated paper passed peer review at a top-tier machine learning workshop. The authors themselves identify the risks: "the potential to overwhelm the peer-review process, artificially inflate research credentials, repurpose the ideas of others without giving proper credit" (Lu et al., 2026, p. 917). The Research-as-Repository protocol provides the infrastructure response: when The AI Scientist operates within a research repository, every generated paragraph is a commit, every experiment a branch, and every AI reviewer's assessment an attributed review. The contribution is auditable by construction.

### 4.5 For the System

The cumulative effect is that scientific publishing becomes a transparent, auditable, machine-readable graph of knowledge production. The Matthew Effect — where early prestige compounds into career advantage through mechanisms invisible to evaluation systems — becomes structurally traceable. The specification gap in peer review (Zharnikov, 2026t) becomes closeable. Funding compliance — Plan S open-access mandates, funder data-sharing requirements — becomes structural: checked by the compliance gate against `FUNDING.yaml` conditions at fork time, not declared on a form and hoped for.

Post-publication commentary follows the same pattern: a reader can fork the published repository, add a critique as a committed review branch, and submit it to the journal's collection. The critique carries the same provenance and attribution as the original review. Living papers — research updated continuously — become the natural mode, with each version a tagged commit rather than a separate publication.

The same CI pipeline that validates compliance can also validate reproducibility: running the analysis code in the repository against the declared data manifest and confirming that the stated results are computationally reachable. Reproducibility becomes a compliance check, not a separate initiative.

### 4.6 For Universities and Research Evaluation

Scientific evaluation currently relies on a self-reinforcing loop: universities evaluate researchers by journal prestige, journals evaluate papers partly by institutional affiliation, and hiring and funding decisions rely on journal prestige — the loop perpetuates. Direct evaluation of the actual science is prohibitively expensive, so journal brands serve as scalar proxies for quality assessment.

The protocol makes direct evaluation tractable. A hiring committee can query a candidate's repositories for contribution depth — measured in commits and diffs, not author position on a byline. Review quality is captured in a portable portfolio that demonstrates scholarly judgment across venues and topics. Collaboration patterns are visible as cross-repository activity: who works with whom, on what, and how substantively. Research trajectory is legible as a commit graph over years, showing not just what was published but how ideas developed, pivoted, and matured.

This does not eliminate peer review — it makes peer review data *available* for evaluation, instead of collapsing it to a binary signal: "published in Nature" or not. A tenure committee reviewing a candidate's repository can see which sections the candidate wrote, which reviewers engaged deeply with the work, and how the candidate responded to criticism — the kind of granular evidence that no CV, h-index, or journal impact factor can provide.

The protocol does not replace prestige. It replaces the *need* for prestige as a proxy, by making the underlying quality data directly accessible. DORA (2012), the Leiden Manifesto (Hicks et al., 2015), and CoARA (2022) have called for precisely this shift — multi-dimensional, evidence-based research evaluation — but no system has yet delivered the data infrastructure to support it. The protocol provides that infrastructure.

### 4.7 For Funders and Government

The chain from grant to impact — grant funds researcher, researcher commits code and text, commits aggregate into papers, papers generate citations and downstream research — is currently traceable only at the coarsest level: which grants funded which papers. The protocol makes this chain traceable at commit-level granularity. Every commit carries contributor attribution and can reference a funding source declared in `FUNDING.yaml`. The result is a verifiable lineage from specific expenditure to specific intellectual output.

Compliance becomes structural rather than bureaucratic. Funder requirements — open access mandates, data sharing, preregistration, AI disclosure — are encoded as conditions in `FUNDING.yaml` and checked by the compliance gate at fork time. Progress reports become redundant: the repository's tagged releases *are* the progress reports, with full provenance showing what was accomplished, by whom, and when. ROI measurement becomes possible at a resolution that current systems cannot approach: which commits, from which researchers, funded by which grants, produced which cited results. Publicly funded research acquires a verifiable paper trail from first commit to published result.

### 4.8 For Society

Tax-funded research currently enters a pipeline whose internal workings are invisible to the public that finances it. The protocol makes the research process — not just the final paper — transparently auditable. Trust in science is expected to increase when provenance is visible: the public can see not just the conclusion but the process that produced it, including how objections were raised and addressed during review.

Retraction cascades become structurally traceable. When a foundational result is retracted, the dependency graphs encoded in `paper.yaml` files across the federation can flag all downstream papers that cited or depended on the retracted claims — an operation that currently requires manual literature searches and takes months. The AI disclosure question — which concerns the public, not just journal editors — has a structural answer: the commit history shows exactly what AI tools contributed, making the question auditable rather than declarative.

### 4.9 For Junior Researchers

AI tools are compressing the "building" phase of a research career — the years of manual literature review, data cleaning, and methodological trial-and-error where junior researchers traditionally develop architectural judgment about how research works. If AI handles the construction, the question becomes: where do junior researchers develop the judgment that senior researchers currently bring?

Review portfolios provide one answer. Reviewing is learning — evaluating others' claims, methods, and arguments develops exactly the critical judgment that AI cannot shortcut. The protocol makes review a credited activity with a portable record, transforming it from invisible service labor into a visible training mechanism. A junior researcher's contribution is legible from their first commit — not hidden behind senior author names on a byline where the fourth author's actual role is unknowable.

The protocol does not solve the pipeline problem. But it provides the infrastructure for career development paths that do not depend on the traditional model of building invisibly for years before receiving credit. When contributions are commits, even early-career researchers have a verifiable record of what they built and how they think.

### 4.10 Stakeholder Summary

**Table 6.** Stakeholder benefit summary.

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

## 5. Limitations and Open Questions

### 5.1 Implementation Roadmap

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

The example illustrates that the validator catches a specific compliance failure (self-citation ratio exceeding the journal's threshold) with an actionable diagnostic. The present paper's own self-citation ratio is 5.7% (2 of 35 references).

The author sees the exact failure (self-citation ratio), fixes it in their repository, and re-runs the validator. The entire cycle takes minutes, not the weeks currently consumed by desk-rejection-and-resubmission rounds.

A realistic adoption sequence: (1) a preprint server or overlay journal implements the fork gate as a GitHub Action — this requires only the validator and a `journal_spec.yaml`, both of which exist; (2) an existing editorial management system (OJS is open-source and extensible) adds git-linked submission as an optional flow alongside traditional upload; (3) a funder (e.g., Wellcome Trust, which already mandates open data) requires `PROVENANCE.yaml` for funded papers, creating demand-side pressure. Each step is independently useful and does not require the others.

The companion artifacts — schemas, examples, and validator — are published as an open-source package at the paper's public repository (github.com/spectralbranding/paper-repo).

**This paper as its own first implementation.** The present paper is authored, versioned, and structured according to the protocol it proposes. The repository contains: `paper.yaml` (7 typed claims with falsification conditions), `CONTRIBUTORS.yaml` (4 contributors including 3 AI tools with disclosure statements), `PROVENANCE.yaml` (fork history — populated as the paper is submitted to venues), `DATA_MANIFEST.yaml` (empty — this is a conceptual paper with no external data), the `journal_spec.yaml` schema, a worked Journal of Marketing example, and the `validate_paper.py` compliance validator. Every claim can be traced to a specific commit. Every contributor's role is verified against the commit log. The paper is its own proof of concept — not a prototype of the full fork-and-review protocol, but a demonstration that the repository structure, metadata schemas, and compliance tooling are functional and internally consistent. The public repository is at github.com/spectralbranding/paper-repo.

### 5.2 Evaluation Framework

The protocol's seven claims (Section 1) are conceptual propositions, not empirically validated results. Future pilot implementations should be evaluated against concrete, measurable success criteria. The following metrics define what "working" means for each structural innovation:

**Desk rejection rate reduction.** The compliance gate (Section 2.3) should eliminate formatting-related desk rejections entirely. Target: 80% reduction in desk rejections attributable to formatting, metadata, or compliance failures at adopting journals. Measurement: compare desk rejection rates (and reasons) for git-linked submissions versus traditional submissions at the same journal over a 12-month period.

**Resubmission turnaround.** When a paper requires formatting or compliance fixes (not substantive revision), the current cycle of editor-return, author-reformat, resubmission consumes days to weeks. The compliance gate reduces this to a local validation loop. Target: median resubmission time for formatting and compliance fixes reduced from weeks to hours. Measurement: time between "submission returned" and "resubmission received" for git-linked versus traditional workflows.

**Reviewer engagement depth.** The review branch model (Section 2.5) makes reviewer effort structurally visible. Engagement depth can be measured via commit count, diff size (lines of substantive commentary), and time-on-review (first commit to final recommendation). These metrics do not measure review *quality* — a short, incisive review may be more valuable than a long, unfocused one — but they provide a quantitative baseline that does not currently exist. Target: establish normative ranges for review depth across disciplines as a foundation for reviewer recognition.

**Dual submission detection.** The provenance chain (Section 2.7) makes concurrent submissions structurally detectable within the protocol. Target: 100% structural detection of concurrent identical submissions to journals that participate in the federation protocol. Measurement: false negative rate (submissions that evade detection) and false positive rate (legitimate parallel submissions, e.g., to a preprint server and a journal, incorrectly flagged).

**AI contribution traceability.** The AI-native layer (Section 2.11) records AI-assisted edits as attributed commits. Target: every AI-assisted edit attributed in commit history with tool name, model version, and prompt hash. Measurement: percentage of AI-assisted edits that carry complete attribution metadata in pilot repositories; comparison of declared AI involvement versus commit-log evidence.

These metrics are evaluation criteria for future pilots, not claims of achieved performance. The protocol is conceptual; the metrics define what a successful implementation would demonstrate.

### 5.3 Limitations

1. **Adoption barrier.** The protocol requires journals, authors, and reviewers to adopt new tooling. The transition cost is non-trivial. A realistic adoption path may begin with a single journal or preprint server implementing the protocol alongside traditional workflows during a transition period, after which the traditional workflow becomes redundant.

2. **Partial prototype only.** The compliance gate layer has been prototyped: a public repository (github.com/spectralbranding/paper-repo) contains the validator, schemas, journal specification examples, and a self-referential implementation of this paper as a compliant paper repository. However, the full fork-and-review lifecycle — fork creation, blinding function, reviewer branch management, provenance chain propagation, and collections-as-users federation — remains a conceptual architecture without implementation. A proof-of-concept implementing these components for a single journal or preprint server is the necessary validation step. The most realistic first adopter is likely a preprint server (which already accepts structured deposits) or an overlay journal (which already curates externally hosted papers), not a traditional publisher whose business model depends on controlling the manuscript pipeline.

3. **Git literacy.** The majority of researchers outside computer science and engineering have never used Git. Humanities, social sciences, and many natural science fields work primarily in Word processors. The protocol requires a GUI abstraction layer — a "GitHub Desktop for papers" — that presents repository operations (commit, fork, branch) through familiar editing metaphors. Without this, adoption is limited to computationally literate disciplines. The three-tier architecture (Section 2.10) mitigates this: Tier 1 (local Git) benefits only those who already use version control; the full protocol benefits only materialize at Tier 3, which requires broader tool development.

4. **Gaming.** Commit histories can be manufactured. A contributor could inflate their commit count through trivial changes. Mitigation: review branches are created by editors, not authors; and contribution metrics should weight substance (lines changed in methods section) over quantity (total commits).

5. **Privacy.** The always-visible provenance chain reveals submission history, which some authors may consider sensitive. The protocol's "existence visible, outcome optional" compromise attempts to balance structural integrity against author privacy, but the appropriate threshold is a community decision.

6. **Legacy corpus.** The existing body of 50+ million published papers has no repository structure. Retroactive conversion is impractical. The protocol applies to new papers going forward; legacy papers remain in their current form.

7. **Governance.** The protocol is designed as a federated network (Section 2.10), not a centralized platform. Like email, any institution can run its own server. The governance question reduces to: who maintains the protocol specification? Existing models (IETF for internet protocols, W3C for web standards, NISO for information standards) provide precedents. The protocol specification could be maintained as an Internet-Draft, with community review periods and versioned releases following RFC conventions. The protocol specification itself can be versioned in a Git repository. Reference implementations should be host-agnostic: Gitea and Forgejo provide self-hosted alternatives to GitHub and GitLab, ensuring that no single commercial platform becomes a dependency. Git's distributed architecture inherently supports offline work — a researcher can commit locally with no network connectivity, and synchronization happens when connectivity returns — which makes the protocol viable in low-bandwidth and intermittent-connectivity environments without requiring any centralized infrastructure to be always available.

8. **Intellectual property.** When an editor owns a fork and reviewers commit to it, the ownership of review content is unclear under current copyright law. The protocol should specify that review commits are licensed under a standard open license (e.g., CC-BY) at creation time.

### 5.4 Stakeholder Incentives and Barriers

**Publishers.** The publisher oligopoly (Lariviere et al., 2015) derives revenue from controlling the manuscript pipeline — submission portals, typesetting, branding, and access. The protocol disperses this control. The protocol's adoption does not require traditional publisher cooperation — it routes around them via preprint servers (which already accept structured deposits), overlay journals (which already curate externally hosted papers), and society publishers (which often operate at cost and may value the efficiency gains). Open-access publishers whose revenue comes from APCs rather than pipeline control are natural early adopters — the protocol reduces their operational costs without threatening their business model. Traditional publishers can join when the network effects make it costly not to.

**Editors.** The compliance gate eliminates formatting desk rejections — a direct time savings. The reviewer branch model provides structured data on reviewer engagement — useful for identifying reliable reviewers. Editors benefit immediately from the gate and incrementally from the review model. The hybrid flow (Section 2.2) provides a transitional compatibility mode, but the git-native flow gives editors structural advantages — version history, contributor verification, and diff capability — that the traditional flow cannot match.

**Reviewers.** The portable review portfolio creates career credit for an activity that currently generates none. The privacy controls (Section 3.3) allow reviewers to accumulate reputation without revealing specific reviews. The risk is that visible review depth creates pressure to over-invest in each review; the mitigation is that depth metrics are aggregate, not per-review.

**Authors.** The primary adoption barrier is Git literacy (Limitation 3). For authors who already use Git (common in computer science, physics, and computational biology), the protocol offers immediate benefits: version history, contributor traceability, and compliance checking. For authors in Word-dominant fields, the protocol requires a GUI abstraction layer that does not yet exist at production quality.

**Legal and intellectual property.** Reviewer commits on journal forks create intellectual contributions with unclear copyright status under current law. The protocol should specify that all review commits are licensed CC-BY-4.0 at creation time — reviewers retain attribution rights but grant reuse. This requires explicit consent at the point of reviewer invitation, analogous to the copyright transfer agreements authors currently sign.

**Privacy.** The irrevocable provenance chain raises concerns: some authors may not want rejection history visible, even as "existence of fork" without decision outcome. The protocol's current design (existence always visible, outcome optionally visible) is a compromise. An alternative — fully private provenance visible only to fork recipients — weakens the dual-submission prevention. The appropriate default is a community decision that may vary by discipline: clinical research may require full transparency; humanities may prefer privacy. The protocol supports both configurations.

### 5.5 Ethics, Legal, and Equity Considerations

The protocol's structural advantages — transparency, traceability, machine readability — carry risks that must be addressed explicitly rather than discovered through adoption.

**Platform dependence.** The protocol is Git-native but must not entrench the dominance of any specific hosting platform. GitHub's current market position makes it the path of least resistance for implementation, but a protocol that requires GitHub replicates the power asymmetry it aims to dissolve — trading publisher lock-in for platform lock-in. The federation architecture (Section 2.10) mitigates this structurally: any Git-compatible host can participate. However, institutional hosting capacity varies enormously. A well-funded research university can run its own Gitea instance; a university in the Global South may lack the systems administration staff to do so. The protocol specification must remain host-agnostic, and reference implementations must be tested on self-hosted infrastructure, not only on commercial platforms.

**Accessibility.** Git's command-line interface is inaccessible to many researchers — not only those unfamiliar with version control but also those with visual, motor, or cognitive disabilities for whom terminal interaction presents barriers. The GUI abstraction layer noted in Limitation 3 is not merely a convenience; it is an accessibility requirement. Any reference implementation must meet WCAG 2.1 AA standards. Screen reader compatibility, keyboard navigation, and high-contrast modes are not optional features — they are prerequisites for equitable adoption.

**Global equity.** The protocol assumes reliable internet connectivity for federation (Tier 3), remote hosting (Tier 2), and even efficient collaboration (Tier 1 with remote co-authors). Researchers in regions with intermittent connectivity, bandwidth constraints, or restricted access to international platforms face structural disadvantages. The protocol's local-first design (Tier 1) partially addresses this — all authoring operations work offline. But submission, review, and publication require network access. Future implementations should consider offline-first synchronization patterns (analogous to Git's own design for intermittent connectivity) and lightweight federation protocols that minimize bandwidth requirements.

**Labor implications.** Reviewer attribution is a corrective to the current invisibility of review labor. But making review depth measurable creates a new risk: the metrics could become targets. If hiring committees begin evaluating candidates on review portfolio depth, the protocol inadvertently creates pressure for unsustainable overwork — reviewers investing more hours per review to build visible records. The framing matters: reviewer attribution should recognize *existing* labor that currently goes uncredited, not demand *additional* labor. Aggregate metrics (total reviews, journal breadth) are safer signals than per-review depth metrics, which could incentivize quantity over judgment.

**Legal and intellectual property.** Reviewer commits on journal forks constitute intellectual contributions — structured, attributed, and timestamped. Their copyright status under current law is ambiguous: is a review comment a work-for-hire (if the reviewer is compensated), a voluntary contribution (if unpaid), or a derivative work (if it modifies the manuscript text)? The protocol should require that all review commits be licensed CC-BY-4.0 at the point of reviewer invitation, before any review work begins. This parallels the copyright transfer agreements authors currently sign at submission — extending the same contractual clarity to reviewers.

**Patent-bound and pre-disclosure research.** Some research is aimed at patents and must remain private until intellectual property is filed. Git handles this natively: private repositories with access control. `PROVENANCE.yaml` can carry a `visibility` field (`public` or `private_until: [date]`) that the compliance gate enforces — blocking fork requests to public venues while the visibility constraint is active. Once the patent is filed, the repository goes public. The full commit history then proves priority, prior art, and inventorship timeline with cryptographic certainty — stronger IP protection than any paper notebook. The protocol does not require openness; it requires *structural readiness* for openness, activated when the researcher decides the time is right.

**Privacy and the irrevocable record.** The provenance chain is append-only by design — this is what makes it trustworthy. But irrevocability means that submission history, rejection patterns, and review timelines are permanently recorded. A researcher who submits to ten journals before acceptance has a visible record of nine rejections (or at minimum, nine prior forks). The protocol's current design makes fork *existence* always visible while keeping *decisions* optionally visible (Section 5.3, Limitation 5). The appropriate default — how much provenance is visible to whom — should be community-configured and may vary by discipline. Clinical research, where transparency serves patient safety, may require fuller disclosure than humanities, where submission patterns carry different professional implications.

---

## 6. Conclusion

The contribution of this paper is not the application of Git to publishing. It is the identification that scientific publishing lacks version control — a construct every other knowledge-intensive domain independently developed when it recognized that knowledge integrity requires provenance tracking.

The structural gap in scientific publishing is not access, timing, or format. It is the document assumption — the treatment of a paper as a static file rather than a living repository with history, contributors, branches, and provenance. But the deeper gap is evaluative: the scientific community cannot evaluate research directly at scale, so it relies on journal prestige as a proxy — creating a loop that rewards publication venue over contribution quality.

The Research-as-Repository protocol addresses both gaps. It replaces the document assumption with Git-native semantics: research programs are repositories, papers are renders, submissions are forks, reviews are attributed commits, and journals are collection curators. It breaks the prestige loop by making research contribution structurally evaluable — contribution depth, review quality, collaboration patterns, and research trajectory become queryable data, available to hiring committees, funders, and the public without relying on journal brands as shortcuts.

The protocol optimizes the knowledge production process, not the paper. Existing publishing reforms — open access, preprints, registered reports — improve the rendered artifact. This protocol makes the research itself transparent: every commit attributed, every AI contribution auditable, every grant traceable to specific results, every affiliation verified by the infrastructure rather than declared on a form.

The four-level hierarchy — research program as repository, paper as render, fork as sharing, publication as merge — reveals that scientific publishing is an instance of a general specification-implementation-perception pipeline (Section 3.4). The same pattern appears in branding and organizational design. The protocol makes this pipeline's structure visible, auditable, and formally describable.

Every stakeholder gains: authors own their research; reviewers build portable portfolios; editors get auditable workflows; universities can evaluate researchers directly; funders trace ROI at commit granularity; junior researchers gain visibility from day one; society gets transparent, auditable science. The protocol does not replace prestige. It replaces the need for prestige as a proxy.

This paper proposes the conceptual architecture. A formal, implementable standard — with normative message schemas, authentication flows, and error handling — is the necessary next step. The compliance gate, schemas, and self-referential implementation are available at github.com/spectralbranding/paper-repo.

---

## References

Barker, M., Chue Hong, N. P., Katz, D. S., et al. (2022). Introducing the FAIR Principles for research software. *Scientific Data*, 9, 622. https://doi.org/10.1038/s41597-022-01710-x

Bryan, J. (2018). Excuse me, do you have a moment to talk about version control? *The American Statistician*, 72(1), 20-27. https://doi.org/10.1080/00031305.2017.1399928

Chambers, C. D. (2013). Registered Reports: A new publishing initiative at Cortex. *Cortex*, 49(3), 609-610.

cOAlition S. (2018). Plan S: Making full and immediate Open Access a reality. https://www.coalition-s.org/

Coalition for Advancing Research Assessment (CoARA). (2022). Agreement on reforming research assessment.

Hicks, D., Wouters, P., Waltman, L., de Rijcke, S., & Rafols, I. (2015). Bibliometrics: The Leiden Manifesto for research metrics. *Nature*, 520(7548), 429-431.

San Francisco Declaration on Research Assessment (DORA). (2012).

Altman, M., & King, G. (2007). A proposed standard for the scholarly citation of quantitative data. *D-Lib Magazine*, 13(3/4).

Auer, S., Kovtun, V., Prinz, M., Kasprzik, A., Stocker, M., & Vidal, M. E. (2019). Towards an Open Research Knowledge Graph. *Serials Review*, 45(4). https://doi.org/10.1080/0361526X.2019.1540272

COAR Notify. (2023). COAR Notify Protocol: Linked data notifications for scholarly communication. https://notify.coar-repositories.org/

DataCite. (2024). DataCite Metadata Schema. https://schema.datacite.org/

Eisen, M. B., Akhmanova, A., Behrens, T. E., et al. (2022). Implementing a "Publish, then Review" model of publishing. *eLife*, 11, e64910. https://doi.org/10.7554/eLife.64910

Freeman, A. (2021). Octopus: A new approach to scientific publishing. https://www.octopus.ac/

Gipp, B., Meuschke, N., & Gernandt, A. (2017). Decentralized Trusted Timestamping using the Crypto Currency Bitcoin. *Proceedings of the ACM/IEEE Joint Conference on Digital Libraries (JCDL)*.

GitHub. (2008). GitHub: Social coding platform. https://github.com/

Hammer, M., & Champy, J. (1993). *Reengineering the Corporation: A Manifesto for Business Revolution*. Harper Business.

Ioannidis, J. P. A. (2005). Why most published research findings are false. *PLOS Medicine*, 2(8), e124. https://doi.org/10.1371/journal.pmed.0020124

Himmelstein, D. S., Rubinetti, V., Slochower, D. R., et al. (2019). Open collaborative writing with Manubot. *PLOS Computational Biology*, 15(6), e1007128. https://doi.org/10.1371/journal.pcbi.1007128

Karpathy, A. (2026). LLM Wiki: A pattern for personal knowledge bases [Idea file]. GitHub Gist. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Katz, D. S., Barba, L. A., Niemeyer, K. E., & Smith, A. M. (2018). Journal of Open Source Software (JOSS): design and first-year review. *PeerJ Computer Science*, 4, e147.

McNutt, M. (2014). Reproducibility. *Science*, 343(6168), 229. https://doi.org/10.1126/science.1250475

Lariviere, V., Haustein, S., & Mongeon, P. (2015). The oligopoly of academic publishers in the digital era. *PLOS ONE*, 10(6), e0127502.

Lu, C., Lu, C., Lange, R. T., Yamada, Y., Hu, S., Foerster, J., Ha, D., & Clune, J. (2026). Towards end-to-end automation of AI research. *Nature*, 651, 914-920. https://doi.org/10.1038/s41586-026-10265-5

Nosek, B. A., Alter, G., Banks, G. C., et al. (2015). Promoting an open research culture. *Science*, 348(6242), 1422-1425. https://doi.org/10.1126/science.aab2374

Ohno, T. (1988). *Toyota Production System: Beyond Large-Scale Production*. Productivity Press.

Ram, K. (2013). Git can facilitate greater reproducibility and increased transparency in science. *Source Code for Biology and Medicine*, 8(1), 7.

Ross-Hellauer, T. (2017). What is open peer review? A systematic review. *F1000Research*, 6, 588. https://doi.org/10.12688/f1000research.11369.2

Signposting. (2022). Signposting the Scholarly Web. https://signposting.org/

Stodden, V., Seiler, J., & Ma, Z. (2018). An empirical analysis of journal policy effectiveness for computational reproducibility. *Proceedings of the National Academy of Sciences*, 115(11), 2584-2589.

Tennant, J. P., Dugan, J. M., Graziotin, D., et al. (2017). A multi-disciplinary perspective on emergent and future innovations in peer review. *F1000Research*, 6, 1151.

Smith, A. M., Katz, D. S., & Niemeyer, K. E. (2016). Software citation principles. *PeerJ Computer Science*, 2, e86. https://doi.org/10.7717/peerj-cs.86

PubPub. (2017). PubPub: Open publishing platform. MIT Knowledge Futures Group. https://www.pubpub.org/

Soiland-Reyes, S., Sefton, P., Crosas, M., et al. (2022). Packaging research artefacts with RO-Crate. *Data Science*, 5(1), 97-138. https://doi.org/10.3233/DS-210053

Torvalds, L. (2005). Git: Fast version control system [Software]. https://git-scm.com/

UNESCO. (2021). UNESCO Science Report: The race against time for smarter development.

van Rooyen, S., Godlee, F., Evans, S., Black, N., & Smith, R. (1999). Effect of open peer review on quality of reviews and on reviewers' recommendations. *BMJ*, 318(7175), 23-27.

Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018. https://doi.org/10.1038/sdata.2016.18

Willinsky, J. (2005). Open Journal Systems: An example of open source software for journal management and publishing. *Library Hi Tech*, 23(4), 504-519.

Womack, J. P., & Jones, D. T. (1996). *Lean Thinking: Banish Waste and Create Wealth in Your Corporation*. Simon & Schuster.

Zharnikov, D. (2026i). Organization as specification: A test-driven approach to business design. Working Paper. https://doi.org/10.5281/zenodo.18946043

Zharnikov, D. (2026t). Paper as specification: A machine-readable standard for scientific claims. Working Paper. https://doi.org/10.5281/zenodo.19210037
