# Research as Repository: A Git-Native Protocol for Scientific Knowledge Production

**Dmitry Zharnikov**

Working Paper v2.0 — April 2026

---

## Abstract

Scientific evaluation relies on a self-reinforcing loop: universities evaluate researchers by journal prestige, journals evaluate papers partly by institutional affiliation, and no one evaluates the research directly — because direct evaluation at scale has lacked the necessary infrastructure. This paper proposes a protocol that provides that infrastructure by treating every research program as a version-controlled repository. A paper becomes a tagged render of the research at a point on its timeline — a frozen snapshot forked to a journal so the community can confirm the findings. The protocol introduces fork-based submission, automated compliance gates, attributed reviewer commits, provenance chains, and AI-traceability by design. A commit-reveal privacy primitive enables researchers to establish cryptographic priority through public commit hashes while retaining control over content disclosure. A Research Wiki layer — adapting Karpathy's (2026) three-layer knowledge pattern — creates five types of git-timestamped intellectual work proof: discovery, priority, attestation, derivation, and independence. The protocol has been implemented across 25 research papers, with a working compliance-gate validator and machine-readable claim specifications. Existing publishing reforms improve the rendered artifact; this protocol makes the research itself structurally transparent.

**Keywords**: scientific publishing, version control, peer review, research infrastructure, open science, provenance, knowledge production, scholarly communication

---

Scientific evaluation operates through a self-reinforcing loop: universities evaluate researchers by journal prestige, journals evaluate papers partly by institutional affiliation, and direct evaluation of the science itself remains prohibitively expensive at scale. The loop persists not because it is optimal but because no infrastructure exists to replace it.

The global scientific publishing system processes approximately 3 million papers per year (UNESCO, 2021) through a pipeline built on a single assumption: a paper is a document. A PDF. A static artifact transmitted from author to editor to reviewer to publisher. Every tool in the pipeline — manuscript submission portals, editorial management systems, reviewer interfaces, typesetting workflows — treats the paper as an opaque binary object that moves between mailboxes.

This assumption was adequate when papers were physically printed and mailed. It is now a significant structural constraint on every reform the scientific community has attempted. Open access reforms change who can read the document (cOAlition S, 2018). Preprint servers change when the document becomes available. Registered reports change what sequence the document follows (Chambers, 2013). Post-publication review adds commentary about the document. Each reform addresses one dimension of the publishing problem while leaving the document assumption intact. The result is a system that has been incrementally improved on multiple dimensions simultaneously — access, timing, sequence, commentary, data sharing, reproducibility — without any reform touching the structural foundation that constrains all of them.

Scientific publishing is the only knowledge-intensive domain without formal version control — a construct independently developed in software engineering (Git), legal systems (case law revision tracking), financial auditing (audit trails and SOX compliance), supply chain management (chain of custody), and clinical research (trial registration). Each domain independently developed provenance tracking because each discovered that knowledge integrity requires it. Publishing has not.

**Table 1.** Provenance mechanisms across knowledge-intensive domains.

| Domain | Provenance mechanism | When adopted |
|--------|---------------------|-------------|
| Legal | Case law revision tracking, legislative history | 19th century |
| Financial auditing | Audit trails, SOX compliance | 1930s (SEC), 2002 (SOX) |
| Clinical research | Trial registration (clinicaltrials.gov) | 2005 (ICMJE requirement) |
| Supply chain | Chain of custody, GS1 standards | 1970s-2000s |
| Software engineering | Version control (CVS, SVN, Git) | 1986-2005 |
| Scientific publishing | None (document assumption) | -- |

The cross-domain pattern is not a software engineering import; it is a convergent discovery. When any knowledge-intensive domain reaches sufficient scale and complexity, it independently develops provenance infrastructure. Publishing's absence from this pattern is an anomaly — one that explains a constellation of persistent problems.

The current pipeline has five structural gaps that the document paradigm cannot address:

**Gap 1: No version history.** A submitted manuscript has no auditable record of how it was written. The editor sees a finished product. The twenty drafts, the deleted sections, the data re-analyses, the contributor who rewrote Section 4 — all invisible. The reproducibility crisis prompted a wave of editorial reform (McNutt, 2014), yet the underlying infrastructure remains unchanged. Stodden, Seiler, and Ma (2018) found that even among journals with explicit reproducibility policies, fewer than 40% of sampled articles made code and data available — demonstrating that policy without infrastructure fails. Ioannidis (2005) demonstrated that most published research findings are false, a conclusion driven in part by the absence of transparent, auditable research processes. The TOP Guidelines (Nosek et al., 2015) defined eight transparency standards, but implementing them within the document paradigm remains difficult because the paradigm itself lacks the infrastructure for structured transparency.

**Gap 2: No contributor traceability.** CRediT (Contributor Roles Taxonomy) added contributor roles to published papers in 2014. But CRediT is a self-reported annotation attached to the final document — it has no connection to the actual work. There is no mechanism to verify that the person listed as "Methodology" actually wrote the methods section. The contribution record is a claim, not a proof.

**Gap 3: No submission provenance.** When a paper is rejected by three journals and accepted by a fourth, the fourth journal's editor has no access to prior reviews. The same paper is re-reviewed from scratch at each venue — a massive duplication of expert labor. Dual submission policies rely entirely on author honesty. The prior editorial engagement, however substantive, leaves no structural trace.

**Gap 4: No review attribution.** Peer reviewers contribute substantive intellectual work — identifying errors, suggesting improvements, catching methodological flaws. Their contributions are acknowledged in a single generic sentence ("We thank the anonymous reviewers") and then erased. A reviewer who saves a paper from a fatal statistical error receives the same credit as one who submits a two-sentence review: none.

**Gap 5: No machine interface.** The entire pipeline is human-readable only. A PDF cannot be queried, diffed, branched, or programmatically analyzed without lossy conversion. AI tools that could assist with literature review, consistency checking, or cross-paper analysis must first solve the extraction problem — converting unstructured text back into structured data — before doing any useful work.

This paper proposes a protocol that closes all five gaps by replacing the document assumption with a repository assumption. The contribution is not the application of Git to publishing — it is the identification that scientific publishing lacks version control, and the provision of the first unified Git-native process layer for the entire research lifecycle. The protocol produces a four-level hierarchy:

1. A **research program** is a repository — the single source of truth, evolving over time.
2. A **paper** is a render of that repository at a point on its timeline — a frozen snapshot.
3. A **submission** is a fork — sharing that render with the community for confirmation.
4. A **publication** is a merge — acceptance of the fork into a journal's curated collection.

Software engineering faced the same structural problem in the 1990s. Source code was treated as a collection of files transmitted between developers. Every collaboration problem was solved ad hoc. The solution was not incremental improvement of file-sharing tools. It was a structural reconception: source code is not a collection of files, it is a repository — a versioned, branched, contributor-attributed, cryptographically auditable history. Git (Torvalds, 2005) implemented this reconception. Ram (2013) demonstrated that Git can facilitate greater reproducibility and transparency in science, Bryan (2018) provided the pedagogical bridge for working scientists, and Vuorre and Curley (2018) formalized a tutorial on Git version control for social science researchers. The present paper extends this reconception from code to the full research lifecycle.

The protocol advances seven claims, each with falsification conditions specified in machine-readable form: (C1) fork-based submission creates cryptographic provenance that makes submission history structurally auditable; (C2) blinding-as-function replaces manual anonymization with a configurable system property; (C3) review-as-commits creates attributed, portable review records; (C4) collections-as-users unifies preprint servers, journals, and archives under a single protocol; (C5) a compliance gate substantially reduces formatting-related desk rejections; (C6) provenance-by-design makes dual submission structurally detectable; and (C7) the protocol's machine-readable structure enables AI-native querying across the full research lifecycle.

---

## Related Work

Several platforms and standards address subsets of the gaps identified above. None integrates all five into a unified protocol. The existing landscape divides into three categories: artifact-focused standards, process reforms, and infrastructure proposals.

### *Artifact-Focused Standards*

RO-Crate (Soiland-Reyes et al., 2022) packages research artifacts — data, code, documents — with rich metadata into a standardized container. It answers the question "what outputs did this research produce and how should they be packaged?" but not "how was the research conducted?" FAIR4RS (Barker et al., 2022) extends the FAIR principles (Wilkinson et al., 2016) to research software, defining machine-readable metadata for findability, accessibility, interoperability, and reusability. DataCite provides DOI minting and metadata standards. Altman and King (2007) proposed a standard for scholarly citation of quantitative data. Signposting provides typed HTTP links for scholarly object discovery.

These standards focus on artifacts — the outputs of research. The present protocol focuses on the process — how those artifacts are authored, submitted, reviewed, and decided upon. The two concerns are complementary: an RO-Crate can package a paper repository's artifacts; FAIR4RS principles inform how the repository's code is documented; DataCite DOIs are minted for releases and forks. The protocol inherits these standards rather than replacing them.

### *Process Reforms*

Registered Reports (Chambers, 2013) split peer review into pre-data and post-data stages, addressing the sequence problem. The present protocol subsumes this as a special case: a Stage 1 submission is a fork at a specific commit; Stage 2 is a subsequent fork from a later commit, and the fork chain records the two-stage structure automatically. DORA (2012), the Leiden Manifesto (Hicks et al., 2015), and CoARA (2022) advocate multi-dimensional research evaluation but provide no data infrastructure to support it. The present protocol provides that infrastructure: when every contribution, review, and decision is recorded in structured form, evaluation can query specific dimensions rather than collapsing to scalar proxies.

Flake and Fried (2020) demonstrated that questionable measurement practices persist partly because measurement transparency infrastructure is absent — a parallel problem in a different domain that converges on the same structural diagnosis: transparency requires infrastructure, not merely norms. Ross-Hellauer (2017) provided a systematic taxonomy of open peer review innovations, and Tennant et al. (2017) catalogued emergent innovations in peer review practices. The present protocol's structured review model accommodates the full range of review modes these taxonomies identify.

### *Infrastructure Proposals*

Manubot (Himmelstein et al., 2019) implements Git-native collaborative writing with CI/CD rendering — the closest predecessor for the authoring layer. The present protocol extends this pattern from authoring to the full submission-review-publication lifecycle. JOSS (Katz et al., 2018) implements review-as-GitHub-issues for software papers; the present protocol generalizes this to all disciplines with structured reviewer commits rather than free-form issue comments. Octopus (Freeman, 2021) decomposes papers into modular linked units with open review — sharing the modular philosophy but using a proprietary platform rather than Git repositories. PubPub (MIT Knowledge Futures Group) provides a web-native open publishing platform with versioning but is not Git-native.

eLife's "Publish, then Review" model (Eisen et al., 2022) is the closest real-world implementation of the "collections as users" concept: authors post preprints first, and eLife curates reviewed preprints into its collection with public reviews attached. The model demonstrates that decoupling publication from review is operationally viable but remains platform-specific. CryptSubmit (Gipp et al., 2017) provides decentralized timestamping for priority claims but does not address the full lifecycle. COAR Notify defines notifications between repositories and review services — the messaging layer, not the manuscript management layer.

Brembs (2023) proposes replacing journals entirely with decentralized infrastructure — a vision that shares the present protocol's diagnosis of the journal system's structural limitations but takes a more radical architectural position. The present protocol does not require journal replacement; it repositions journals as collection curators within a Git-native ecosystem, preserving their evaluative function while dissolving their monopoly on the manuscript pipeline.

The Paper Spec standard (Zharnikov, 2026t) is a companion to the present protocol. Paper Spec defines a machine-readable YAML file (`paper.yaml`) that captures what a paper claims, what would falsify those claims, and what the paper depends on — with five structural elements: typed claims with unique identifiers and dependency links, methodology description, acceptance and falsification criteria, a dependency graph, and submission history. Paper Spec is the specification layer; the present protocol is the process layer. Together, they make both the content and the lifecycle of a paper fully machine-readable.

Existing approaches optimize artifacts or notifications; none provides a unified process layer that makes authoring, compliance, submission, blinding, review, provenance, and publication operations on a single versioned repository.

**Table 2.** Protocol feature coverage across existing systems.

| System | VC | Fork | Gate | Rev | Prov | Coll |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|
| Manubot (Himmelstein et al., 2019) | Full | -- | -- | -- | -- | -- |
| JOSS (Katz et al., 2018) | Full | Partial | Partial | Full | -- | -- |
| Octopus (Freeman, 2021) | Partial | -- | -- | Full | Partial | -- |
| COAR Notify | -- | -- | -- | -- | Partial | Partial |
| CryptSubmit (Gipp et al., 2017) | -- | -- | -- | -- | Full | -- |
| eLife (Eisen et al., 2022) | -- | -- | -- | Partial | -- | Partial |
| RO-Crate (Soiland-Reyes et al., 2022) | -- | -- | Partial | -- | -- | Partial |
| **This protocol** | **Full** | **Full** | **Full** | **Full** | **Full** | **Full** |

Column key: VC = version control, Fork = fork-based submission, Gate = compliance gate, Rev = reviewer attribution, Prov = provenance chain, Coll = collections as users.

---

## The Protocol

The protocol maps the scientific publishing lifecycle onto Git-native operations. Each stage has automated checks, human judgment points, and structural artifacts (the provenance chain). The protocol does not automate science — it automates a significant fraction of the administrative overhead that currently consumes editorial and author labor, reserving human attention for the intellectual work that only humans can do.

### *Repository as Single Source of Truth*

The protocol's fundamental unit is the research repository — a versioned history of a research program that may produce one or many papers over its lifetime. A researcher working on a single core idea for years maintains one repository; each paper is a tagged release. Two papers from the same repository share commit ancestry, making their relationship structurally visible rather than merely declared via citations. This also makes "salami slicing" — splitting one study into artificially separate publications — structurally detectable, since the common ancestry and overlapping content are visible in the diff history.

The manuscript (Markdown, LaTeX, or any diff-friendly plain-text format) is the single source of truth. All renderings — PDF, DOCX, JATS XML, HTML — are generated outputs. The repository stores the generating function, not the rendered output. Software tools used in the analysis are cited following the FORCE11 software citation principles (Smith et al., 2016), with version, DOI, and repository URL recorded in `paper.yaml` dependencies.

The repository has a minimal required structure: the manuscript source, a `paper.yaml` companion (structured claims per the Paper Spec standard), `CONTRIBUTORS.yaml` (contributor roles verified against commit history, following CRediT taxonomy but with structural verification), `PROVENANCE.yaml` (fork and submission history), and `DATA_MANIFEST.yaml` (links to external data archives with DOIs and checksums). The protocol adopts a two-layer architecture: the repository stores text-based artifacts that Git handles natively; large binary data (microscopy images, genomic sequences, simulation outputs) lives in linked external archives (Zenodo, Dryad, GenBank) declared in `DATA_MANIFEST.yaml` — extending Altman and King's (2007) citation standard from a convention to a machine-enforceable dependency with checksums and access metadata.

### *Paper as Tagged Render, Submission as Fork*

The four-level hierarchy introduced above operates as follows. The research repository evolves continuously through commits — writing, analysis, revision. When results reach a communicable stage, the author tags a release, freezing the repository at that commit. Submitting to a journal creates a fork: a read-only copy of the repository at the tagged commit, transferred to the journal's editorial control.

The fork operation: (1) creates a read-only copy at the specified commit; (2) transfers ownership to the journal editor; (3) records the fork in the author's `PROVENANCE.yaml` (irrevocable); (4) strips or anonymizes contributor identities per the journal's blinding policy; and (5) grants the journal access to the fork as a Git repository, enabling editors and reviewers to operate on the versioned source — reviewing diffs, commenting on commits, and making attributed edits on review branches.

The author cannot modify the fork after creation. They can revoke the fork (withdrawing the submission — recorded in provenance), continue working on their main branch (the fork is a snapshot, not a lock), or create additional forks to other journals — but each new fork carries the full provenance chain, making existing forks visible to subsequent editors. This makes dual submission structurally detectable within the protocol.

For journals not yet operating in the git-native workflow, existing submission portals (ScholarOne, Editorial Manager, OJS) accept traditional file uploads as a transitional compatibility mode. The git-native flow gives editors capabilities the traditional flow cannot match: version history, contributor verification, and diff capability. These structural advantages, not mandates, drive the transition.

### *Review as Attributed Commits*

The editor creates a review branch for each reviewer on the journal fork. Each reviewer's branch is a complete, timestamped, attributed record of their review. The commit history shows when the reviewer worked (timestamps), what they reviewed (which sections, which claims), how deeply they engaged (number of commits, lines of commentary), and what they recommended (final commit on the branch). The protocol supports all review modes: open review (real name and ORCID visible), single-blind (reviewer identity visible to editor only), and pseudonymous (persistent pseudonym across reviews at this journal).

A reviewer's account belongs to the reviewer, not the journal. Over time, the reviewer accumulates a portable review portfolio: total reviews, journals served, average engagement depth, and specializations. The reviewer controls which individual reviews are public, but aggregate statistics are always visible. Early evidence suggests that open reviewer identification does not reduce review quality (van Rooyen et al., 1999). This creates verifiable review reputation: a reviewer who writes substantive critique is visibly different from one who submits vague praise. Depth is measurable, quality is portable across journals, credit is structural, and accountability is implicit.

The editorial decision is itself a commit. Acceptance merges the fork into the journal's collection with a minted DOI. Rejection closes the fork. The review record persists in either case — and with three-way consent (author, editor, reviewers), prior reviews can transfer to subsequent journals, reducing the massive duplication of expert labor that the current system produces.

### *The Compliance Gate*

In the current system, a significant fraction of editorial labor is consumed by non-compliant submissions: wrong fonts, incorrect reference styles, figures at inadequate resolution, abstracts exceeding word limits, missing ethics declarations. The formatting-rejection-resubmission cycle is administrative overhead that creates no knowledge.

In the repository protocol, each journal publishes a submission specification (`journal_spec.yaml`) — a machine-readable document defining its compliance requirements: word count ranges, abstract length, reference style, figure format and resolution, self-citation limits, required disclosures, and blinding configuration. The fork operation runs this specification as a validation pipeline before the fork is accepted. If any check fails, the fork is not created. The author sees exactly which requirements are unmet, fixes them locally, and retries. The journal fork is compliant by construction.

This inverts the current compliance model. Currently: the author guesses at requirements from a lengthy "Instructions for Authors" document, manually formats, submits, waits days or weeks for an editorial assistant to check compliance, receives the paper back for fixes, reformats, and resubmits — often multiple rounds — before the paper ever reaches a reviewer. In the repository protocol: the journal publishes `journal_spec.yaml`, the author runs local validation, all failures appear instantly with exact diagnostics, and when all checks pass the fork is created and the paper arrives fully compliant.

Every blocking check is automatable with existing tools: word count (parse Markdown), abstract length (parse frontmatter), reference style (lint against CSL definitions), figure format and DPI (read image metadata), self-citation ratio (count author-name matches), DOI completeness (check reference fields), and required disclosure presence (check for YAML fields or section headings). Optional advisory checks (scope matching via embedding similarity, reference coverage via citation graphs, statistical reporting completeness) use AI but are non-blocking. No new AI research is needed — only integration.

### *Blinding as Deterministic Function*

Blinding is a configurable system function applied to the fork at creation time, not a manual task performed by the author. The journal specifies its blinding policy as parameters: strip author names, affiliations, ORCIDs, acknowledgments, figure metadata (EXIF data, embedded author info); anonymize self-citations; optionally preserve role descriptions without identity. The system applies these rules automatically when generating the reviewer-facing version. The function is complete (covers every field, including figure metadata and code comments that authors routinely forget), configurable (different journals apply different policies), verifiable (deterministic and auditable — an author cannot "accidentally" leave identifying information visible), and reversible (the editor can lift the blind selectively after the review decision).

### *Provenance by Design*

Every fork creates an irrevocable, append-only record in `PROVENANCE.yaml`. The provenance chain records each fork's target venue, creation timestamp, source commit, status (active, closed, revoked), outcome (merged or not merged), and aggregate review statistics (number of reviewers, total commentary lines). Fork existence is always visible to subsequent fork recipients; the decision outcome is visible only if the author chooses to disclose it.

This architecture has three consequences. First, dual submission becomes structurally detectable: if a fork is active, any new fork carries this information. Second, rejection history is optionally transparent: an author can reveal their full submission history to demonstrate thoroughness, or keep outcomes private. Third, review labor is preserved: when a paper moves from one journal to the next, the subsequent editor can see that prior reviewers invested substantive effort and can request access to those reviews with appropriate consent.

### *Collections as Users*

If every paper is a repository, then preprint servers, journals, and institutional archives are not platforms — they are users on a shared protocol who curate collections of frozen forks. arXiv is a user account that accepts forks into its collection with minimal curation criteria and mints arXiv IDs. Zenodo is a user account that accepts forks and mints DOIs. Nature is a user account that curates forks through editorial review, merging accepted forks into its collection with a Nature badge and DOI. The paper exists once, in the author's repository; collections hold linked snapshots with different acceptance criteria and different badges.

This eliminates format conversion between venues, multiple uploads to separate platforms, version fragmentation across preprint, published, and institutional copies, and the access barriers of separate endorsement and account systems. Overlay journals — which already curate papers hosted on preprint servers — implement a lightweight version of this pattern today.

### *AI-Native Layer*

When every paper is a repository with structured metadata (`paper.yaml`), machine-readable content, and auditable provenance, the entire corpus becomes queryable. Cross-paper dependency checking becomes a graph query: an AI agent detects when Paper B's claims depend on Paper A's results and Paper A has been retracted. Real-time literature review operates on structured claims rather than extracted text. Language independence follows: the repository stores structured claims that can be translated while preserving machine-readable claim structure. Reviewer assistance through pre-screening — comparing claims against known results, checking internal consistency, assessing scope fit — becomes a structured operation.

AI contribution traceability becomes an engineering problem rather than a policy problem. Every AI-assisted edit is a commit with structured metadata: the tool, the model version, and a hash of the prompt. The commit log makes AI contribution auditable by construction. Lu et al. (2026) demonstrate fully autonomous AI systems that generate complete research manuscripts and perform their own peer review; the protocol provides the infrastructure response by making every generated paragraph a commit and every AI review an attributed branch. The AI disclosure problem that journals currently struggle to solve through policy becomes a structural property of the repository.

### *The Research Wiki and Intellectual Work Proofs*

The protocol addresses how research is built, evaluated, and decided upon. It does not address how the researcher organizes the knowledge that informs the research — the literature, the sources, the correspondence, the evolving understanding that precedes and surrounds the paper. This gap is currently filled by reference managers (Zotero, Mendeley) that operate outside the research repository: no version control, no provenance chain, no structural integration with the paper's claims. The researcher's intellectual process — what was read, when, in what order, and how it influenced the argument — is invisible.

Karpathy (2026) proposes a three-layer pattern for personal knowledge management: raw sources (immutable ground truth), a wiki (LLM-maintained structured knowledge), and a schema (specification governing what the wiki tracks). The pattern applies directly to research: the sources are the literature and data the researcher consults; the wiki is the organized, cross-referenced understanding; the schema defines the research program's knowledge structure.

The protocol introduces an optional `.wiki/` directory within the repository containing: `schema.yaml` (what to track and how to organize), `sources/` (PDFs, URLs-as-markdown, datasets), `pages/` (LLM-maintained wiki pages by topic, author, concept), `correspondence/` (emails, messages, reviews — redactable), `ingest.jsonl` (chronological source ingestion log), and `contradictions.md` (sources that conflict with the paper's claims). The directory is dot-prefixed (hidden by convention) and selectively excludable from public access via `.gitignore` while retaining full Git history locally.

The research wiki creates five structurally distinct types of intellectual work proof, all deriving from Git's cryptographic properties (SHA-256 hashing, timestamping, signing):

**Discovery proof.** When was a source first encountered? The `ingest.jsonl` log records each source addition with a timestamp, file hash, and annotation. A researcher who adds a source PDF on February 12 has a cryptographically verifiable record of access to that source on that date — currently unprovable through any existing tool. Reference managers record when a citation was added to a library but not when the source was actually consulted, and the record is not tamper-evident.

**Priority proof.** When was an idea first articulated? The commit history shows the exact moment a concept appeared in the manuscript. A diff between consecutive commits reveals precisely when an idea entered the text. If two researchers independently develop the same idea, Git timestamps establish priority to the commit — not to the publication date, which may lag by months or years.

**Attestation proof.** When was an idea shared with a third party? The `.wiki/correspondence/` directory stores communications where the researcher shared ideas with others — emails, messages, review exchanges. Correspondence can be stored in full, redacted (with the unredacted version's hash preserved for future verification), or as metadata-only entries (date, correspondent, subject, hash of original).

**Derivation proof.** How did the argument develop? The full commit history shows the intellectual trajectory: which sources led to which ideas, which ideas were abandoned, which were restructured. A reviewer or evaluator can inspect the diff graph and trace the research evolution — the intellectual equivalent of a lab notebook, currently absent from all published research.

**Independence proof.** Did the researcher develop an idea independently? If two groups publish similar findings, the Git history of each repository can establish: when each group first committed the idea, whether either group had access to the other's work (via `ingest.jsonl` — if the other group's preprint was never ingested, independence is structurally demonstrated), and the derivation path that led each group to the same conclusion independently.

The wiki's LLM-maintained knowledge layer follows Karpathy's pattern: the LLM processes each ingested source and updates relevant wiki pages, adding cross-references, noting contradictions, and linking to the paper's claims. Three maintenance operations map to the research workflow: ingest (add a source, update wiki pages, flag contradictions), query (ask questions, file valuable findings back into the wiki), and lint (check for orphan pages, missing cross-references, and citation integrity — a paper claiming 45 references whose wiki contains only 38 source files has 7 citations that may warrant scrutiny).

Privacy is granular. The `.wiki/` directory is private by default. The `.gitignore` within it can exclude large source files while preserving their metadata (filenames, hashes, timestamps) in the tracked `ingest.jsonl`. Selective disclosure supports multiple scenarios: standard submission (wiki excluded), transparency signal (ingest log included), full disclosure (wiki fully public), or audit response (disclosed to a specific party without public disclosure). The choice is the researcher's.

### *The Commit-Reveal Mechanism*

The same privacy primitive that protects copyrighted source PDFs in the wiki applies to the researcher's own work. Every commit produces a SHA-256 hash — a tamper-evident fingerprint signed by the author's GPG key and timestamped by the Git history. Publishing the hash establishes that the work in this exact form existed at this exact moment, by this exact author, without revealing what the work contains. Any third party who later receives the contents can recompute the hash and verify that nothing has been altered.

This is commit-reveal: priority and provenance are established at the moment of commit; content disclosure stays under the author's control and can be made selectively, partially, conditionally, or never. The mechanism resolves the apparent trade-off between open science and confidentiality that has historically blocked Git-native research adoption in academia.

The mechanism supports several disclosure architectures. A solo researcher can work in a fully private repository and publish commit hashes to public anchors (a registry, a blockchain timestamp) at meaningful milestones — a key derivation, a hypothesis pre-registration, a draft completion. Years later, in a priority dispute, the researcher reveals the contents and any party verifies the hash. A consortium can accumulate an unfalsifiable public timeline while retaining exclusive content access. A hybrid repository can make some directories public and others private, with hashes of private directories visible in the commit history. An embargoed paper can be committed in full at time *t* but revealed only after a journal embargo, patent filing, or coordinated release — the hash proves the contents were not edited during the embargo period.

For misconduct prevention, this is the structural alternative to centralized institutional databanks. A researcher who fabricates results cannot retroactively edit a signed, hashed commit without breaking the chain. A researcher who plagiarizes cannot claim priority over a hash published before they joined the field. The protocol does not require any researcher to make their work public — it requires only that the choice of when, what, and to whom to disclose is meaningful, granular, and verifiable.

### *Normative Specification*

A production-grade implementation requires a formal normative specification defining four structural components: message schemas (fork requests, review responses, editorial decisions, provenance queries — extending COAR Notify's Linked Data Notifications with paper-specific message types), authentication and signing (GPG-signed commits with ORCID-linked keys and institutional key infrastructure, with Signposting for discovery), error handling (blocking vs. advisory failures, conflict resolution for simultaneous forks, timeout policies for unresponsive reviewers), and API endpoints for federation (modeled on DataCite's REST API for provenance queries and ORCID's OAuth for identity verification).

The normative specification is future work requiring multi-stakeholder input from publishers, libraries, platform providers, and researchers. The governance model — whether maintained by NISO, W3C, IETF, or a new consortium — is itself a design decision. The conceptual architecture in this paper is the prerequisite: one must know what the protocol does before specifying how it does it.

---

## Implementation Evidence

The protocol is not hypothetical. It has been implemented across 25 research papers in the Spectral Brand Theory research program (Zharnikov, 2026a), providing a self-referential proof of concept that demonstrates the protocol's feasibility across a multi-year, multi-venue research lifecycle.

### *Repository-Level Implementation*

All 25 papers maintain the protocol's required metadata files: `paper.yaml` (structured claims with unique identifiers, dependency links, and falsification conditions per the Paper Spec standard), `CONTRIBUTORS.yaml` (human and AI contributor attribution with commit-verified roles), `PROVENANCE.yaml` (complete submission history including venue, decision, and revision scope), and `DATA_MANIFEST.yaml` (data dependencies with DOIs and checksums). The papers span six theoretical layers — from foundational axioms to empirical validation — and have been submitted to 15 journals across marketing, management, information science, and scholarly communication. This generates a provenance dataset that demonstrates the protocol's capacity to track multi-venue submission lifecycles, including desk rejections, revise-and-resubmit cycles, and venue transitions.

### *Compliance Gate Validator*

A working compliance-gate validator (290 lines of Python) is published at github.com/spectralbranding/paper-repo. The validator checks a paper repository against a `journal_spec.yaml` file, validating word count, abstract length, keyword range, reference count, self-citation ratio, figure formats, and required statements (AI disclosure, data availability, funding, conflict of interest). It runs locally in under one second and produces a pass/fail report with specific failure messages.

A worked example encodes the Journal of Marketing's submission requirements as `journal_spec_jm.yaml` (130 fields covering manuscript format, blinding rules, figure specifications, and 46 compliance checks derived from actual JM submission guidelines). The validator catches specific compliance failures (e.g., self-citation ratio exceeding the journal's 25% threshold) with actionable diagnostics, demonstrating that real journal requirements can be encoded in machine-readable form and validated automatically.

### *Self-Referential Implementation*

The R14 paper itself is authored, versioned, and structured according to the protocol it proposes. The repository contains `paper.yaml` (7 typed claims with falsification conditions), `CONTRIBUTORS.yaml` (contributors including AI tools with disclosure statements), `PROVENANCE.yaml` (fork history populated as the paper is submitted to venues), and the compliance-gate validator. Every claim can be traced to a specific commit. Every contributor's role is verified against the commit log. The paper is its own proof of concept — not a prototype of the full fork-and-review protocol, but a demonstration that the repository structure, metadata schemas, and compliance tooling are functional and internally consistent.

### *Research Wiki Partial Implementation*

The Research Wiki layer is partially implemented through session-based development logs that record source ingestion, idea development, and decision traces across 100+ research sessions. The full `.wiki/` directory structure with LLM-maintained pages remains a design specification; the underlying provenance data (when sources were encountered, how arguments evolved, which ideas were abandoned) is captured in the repository's commit history and session documentation.

### *What Remains Conceptual*

The compliance-gate layer is implemented and functional. The repository structure, metadata schemas, and validation tooling are proven across 25 papers. However, the full fork-and-review lifecycle — fork creation by journal portals, blinding function automation, reviewer branch management, provenance chain propagation across federated hosts, and collections-as-users federation — remains a conceptual architecture. The most realistic first adopter is a preprint server (which already accepts structured deposits) or an overlay journal (which already curates externally hosted papers), where the integration surface is minimal and the structural advantages are immediate.

---

## Limitations and Future Work

### *Partial Prototype*

The implemented components (compliance gate, repository structure, metadata schemas, validator) demonstrate feasibility for the authoring and pre-submission layers. The post-submission layers (fork creation, review branches, federation) require integration with editorial management systems. OJS (Open Journal Systems) is open-source and extensible — a natural platform for a pilot implementation. The protocol's federation architecture follows the email model (SMTP): any server can communicate with any other using a shared protocol, with no central authority. This requires only that participating hosts implement the message schemas, not that they adopt any particular platform.

### *Git Literacy Barrier*

The majority of researchers outside computer science, physics, and computational biology have never used Git. Humanities, social sciences, and many natural science fields work primarily in Word processors. The protocol requires a GUI abstraction layer — a "GitHub Desktop for papers" — that presents repository operations (commit, fork, branch) through familiar editing metaphors. Without this, adoption is limited to computationally literate disciplines.

The three-tier adoption architecture mitigates this: Tier 1 (local Git for version control) benefits researchers who already use Git, with no institutional adoption required. Tier 2 (remote hosting with `paper.yaml`) adds structured metadata and machine readability. Tier 3 (full federation with fork-based submission and review) requires broader tool development. Crucially, Tier 1 is useful immediately, alone, on a single researcher's laptop. The protocol delivers value to a single researcher before it delivers value to the system.

### *No Empirical Adoption Data*

The protocol's seven claims are conceptual propositions, not empirically validated results. Future pilot implementations should be evaluated against concrete metrics: desk rejection rate reduction (target: 80% reduction for formatting-related causes), resubmission turnaround (target: hours instead of weeks for compliance fixes), reviewer engagement depth (commit count, commentary lines — establishing normative ranges as a foundation for recognition), dual submission detection rates, and AI contribution traceability completeness. These define what a successful implementation would demonstrate.

### *Legacy Corpus and Forward-Only Design*

The existing body of 50+ million published papers has no repository structure. Retroactive conversion is impractical. The protocol applies to new papers going forward. This is a structural limitation shared with every infrastructure transition — email did not retroactively convert postal mail, but the value of the new infrastructure drove adoption nonetheless.

### *Equity, Accessibility, and Global Considerations*

The protocol assumes reliable internet connectivity for federation (Tier 3) and remote hosting (Tier 2). Researchers in regions with intermittent connectivity face structural disadvantages. The local-first design partially addresses this: all authoring operations work offline, and Git's distributed architecture inherently supports intermittent connectivity. Future implementations should consider lightweight federation protocols that minimize bandwidth requirements.

The GUI abstraction layer is not merely a convenience — it is an accessibility requirement. Any reference implementation must meet WCAG 2.1 AA standards for screen reader compatibility, keyboard navigation, and high-contrast modes. Platform dependence is a further risk: the protocol must remain host-agnostic, with reference implementations tested on self-hosted infrastructure (Gitea, Forgejo), ensuring that no single commercial platform becomes a dependency.

### *Gaming, Privacy, and Legal Considerations*

Commit histories can be manufactured through trivial changes; mitigation requires weighting substance (lines changed in methods sections) over quantity (total commits). The irrevocable provenance chain reveals submission history, which some authors may consider sensitive; the "existence visible, outcome optional" compromise balances integrity against privacy, but the appropriate threshold is a community decision that may vary by discipline. Reviewer commits on journal forks create intellectual contributions with unclear copyright status; the protocol should require CC-BY-4.0 licensing at the point of reviewer invitation, extending to reviewers the same contractual clarity that copyright transfer agreements currently provide to authors.

### *Implementation Roadmap*

A realistic adoption sequence: (1) a preprint server or overlay journal implements the fork gate as a GitHub Action, requiring only the validator and a `journal_spec.yaml` — both of which exist; (2) an existing editorial management system (OJS) adds git-linked submission as an optional flow alongside traditional upload; (3) a funder (e.g., Wellcome Trust, which already mandates open data) requires `PROVENANCE.yaml` for funded papers, creating demand-side pressure. Each step is independently useful and does not require the others. The companion artifacts — schemas, examples, validator, and self-referential implementation — are published at github.com/spectralbranding/paper-repo.

---

## Conclusion

The contribution of this paper is threefold.

First, it identifies that scientific publishing lacks version control — a construct every other knowledge-intensive domain independently developed when it recognized that knowledge integrity requires provenance tracking. The diagnosis is cross-domain, not technology-specific: legal systems, financial auditing, clinical research, supply chains, and software engineering all converged on the same structural solution. Publishing's absence from this pattern is the anomaly that explains persistent problems in reproducibility, contributor attribution, review quality, and research evaluation.

Second, it introduces the commit-reveal mechanism as a privacy primitive for open science. The apparent trade-off between transparency and confidentiality — the tension that has historically blocked Git-native research adoption — dissolves when priority and provenance are established through public commit hashes while content disclosure remains under the author's control. The Research Wiki's five intellectual work proofs (discovery, priority, attestation, derivation, independence) demonstrate that cryptographic provenance can serve verification needs that no current infrastructure addresses.

Third, it proposes that collections-as-users unifies platforms under a single protocol. When preprint servers, journals, and institutional archives are reconceived as user accounts curating collections of frozen forks, the fragmentation of the current landscape — separate uploads, separate formats, separate metadata, separate access policies — reduces to a single architectural pattern.

The practical consequences follow from the architecture. Journals gain compliance-by-construction: every fork arrives fully formatted, with structured metadata, verified contributor roles, and complete disclosure statements. Reviewers gain portable credit: review labor becomes visible, attributed, and career-relevant. Authors retain ownership: the research repository is the single source of truth, and publications are tagged releases rather than transfers of custody. Funders gain commit-level visibility into how grants produce results. The protocol does not replace prestige — it replaces the need for prestige as a proxy, by making the underlying quality data directly accessible. DORA (2012), the Leiden Manifesto (Hicks et al., 2015), and CoARA (2022) called for precisely this shift; the protocol provides the data infrastructure to support it.

The protocol enables not a better document but a transparent, evaluable knowledge production process. Existing publishing reforms — open access, preprints, registered reports — improve the rendered artifact. This protocol makes the research itself structurally transparent: every commit attributed, every AI contribution auditable, every submission traceable, every review credited.

The compliance gate, schemas, validator, and self-referential implementation are available at github.com/spectralbranding/paper-repo.

---

## References

Altman, M., & King, G. (2007). A proposed standard for the scholarly citation of quantitative data. *D-Lib Magazine*, 13(3/4).

Barker, M., Chue Hong, N. P., Katz, D. S., et al. (2022). Introducing the FAIR Principles for research software. *Scientific Data*, 9, 622. https://doi.org/10.1038/s41597-022-01710-x

Brembs, B. (2023). Replacing academic journals. *Royal Society Open Science*, 10(7), 230206. https://doi.org/10.1098/rsos.230206

Bryan, J. (2018). Excuse me, do you have a moment to talk about version control? *The American Statistician*, 72(1), 20-27. https://doi.org/10.1080/00031305.2017.1399928

Chambers, C. D. (2013). Registered Reports: A new publishing initiative at Cortex. *Cortex*, 49(3), 609-610.

cOAlition S. (2018). Plan S: Making full and immediate Open Access a reality. https://www.coalition-s.org/

Coalition for Advancing Research Assessment (CoARA). (2022). Agreement on reforming research assessment.

COAR Notify. (2023). COAR Notify Protocol: Linked data notifications for scholarly communication. https://notify.coar-repositories.org/

DataCite. (2024). DataCite Metadata Schema. https://schema.datacite.org/

Eisen, M. B., Akhmanova, A., Behrens, T. E., et al. (2022). Implementing a "Publish, then Review" model of publishing. *eLife*, 11, e64910. https://doi.org/10.7554/eLife.64910

Flake, J. K., & Fried, E. I. (2020). Measurement schmeasurement: Questionable measurement practices and how to avoid them. *Advances in Methods and Practices in Psychological Science*, 3(4), 456-465. https://doi.org/10.1177/2515245920952393

Freeman, A. (2021). Octopus: A new approach to scientific publishing. https://www.octopus.ac/

Gipp, B., Meuschke, N., & Gernandt, A. (2017). Decentralized Trusted Timestamping using the Crypto Currency Bitcoin. *Proceedings of the ACM/IEEE Joint Conference on Digital Libraries (JCDL)*.

Hicks, D., Wouters, P., Waltman, L., de Rijcke, S., & Rafols, I. (2015). Bibliometrics: The Leiden Manifesto for research metrics. *Nature*, 520(7548), 429-431.

Himmelstein, D. S., Rubinetti, V., Slochower, D. R., et al. (2019). Open collaborative writing with Manubot. *PLOS Computational Biology*, 15(6), e1007128. https://doi.org/10.1371/journal.pcbi.1007128

Ioannidis, J. P. A. (2005). Why most published research findings are false. *PLOS Medicine*, 2(8), e124. https://doi.org/10.1371/journal.pmed.0020124

Karpathy, A. (2026). LLM Wiki: A pattern for personal knowledge bases [Idea file]. GitHub Gist. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Katz, D. S., Barba, L. A., Niemeyer, K. E., & Smith, A. M. (2018). Journal of Open Source Software (JOSS): design and first-year review. *PeerJ Computer Science*, 4, e147.

Lu, C., Lu, C., Lange, R. T., Yamada, Y., Hu, S., Foerster, J., Ha, D., & Clune, J. (2026). Towards end-to-end automation of AI research. *Nature*, 651, 914-920. https://doi.org/10.1038/s41586-026-10265-5

McNutt, M. (2014). Reproducibility. *Science*, 343(6168), 229. https://doi.org/10.1126/science.1250475

Nosek, B. A., Alter, G., Banks, G. C., et al. (2015). Promoting an open research culture. *Science*, 348(6242), 1422-1425. https://doi.org/10.1126/science.aab2374

Ram, K. (2013). Git can facilitate greater reproducibility and increased transparency in science. *Source Code for Biology and Medicine*, 8(1), 7.

Ross-Hellauer, T. (2017). What is open peer review? A systematic review. *F1000Research*, 6, 588. https://doi.org/10.12688/f1000research.11369.2

San Francisco Declaration on Research Assessment (DORA). (2012).

Signposting. (2022). Signposting the Scholarly Web. https://signposting.org/

Smith, A. M., Katz, D. S., & Niemeyer, K. E. (2016). Software citation principles. *PeerJ Computer Science*, 2, e86. https://doi.org/10.7717/peerj-cs.86

Soiland-Reyes, S., Sefton, P., Crosas, M., et al. (2022). Packaging research artefacts with RO-Crate. *Data Science*, 5(1), 97-138. https://doi.org/10.3233/DS-210053

Stodden, V., Seiler, J., & Ma, Z. (2018). An empirical analysis of journal policy effectiveness for computational reproducibility. *Proceedings of the National Academy of Sciences*, 115(11), 2584-2589.

Tennant, J. P., Dugan, J. M., Graziotin, D., et al. (2017). A multi-disciplinary perspective on emergent and future innovations in peer review. *F1000Research*, 6, 1151.

Torvalds, L. (2005). Git: Fast version control system [Software]. https://git-scm.com/

UNESCO. (2021). UNESCO Science Report: The race against time for smarter development.

van Rooyen, S., Godlee, F., Evans, S., Black, N., & Smith, R. (1999). Effect of open peer review on quality of reviews and on reviewers' recommendations. *BMJ*, 318(7175), 23-27.

Vuorre, M., & Curley, J. P. (2018). Curating research assets: A tutorial on the Git version control system. *Advances in Methods and Practices in Psychological Science*, 1(2), 219-236. https://doi.org/10.1177/2515245918754826

Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018. https://doi.org/10.1038/sdata.2016.18

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception measurement. Working Paper. https://doi.org/10.5281/zenodo.18833187

Zharnikov, D. (2026t). Paper as specification: A machine-readable standard for scientific claims. Working Paper. https://doi.org/10.5281/zenodo.19210037

---
*This paper is part of the Spectral Brand Theory research program. For the full atlas of 20+ interconnected papers, see [spectralbranding.com/atlas](https://spectralbranding.com/atlas).*
