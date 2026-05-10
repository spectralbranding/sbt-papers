# Canon as Repository: A Specification-Driven Architecture for Transmedia Intellectual Property

**Dmitry Zharnikov**

Working Paper v1.1.0 — 2026-05-10. https://doi.org/10.5281/zenodo.19355800

---

## Abstract

Creative intellectual property management is the conspicuous exception among mature domains of complex designed systems: engineering, medicine, software, and scientific publishing have each independently developed formal mechanisms to verify that artifacts satisfy their specifications; creative IP has not. Transmedia franchises accumulate contradictions as intellectual property is rendered across novels, films, games, and merchandise because no formal specification governs what the story *is* independently of how it is expressed. Building on transmedia storytelling theory (Jenkins, 2006, 2011; Ryan, 2001, 2015; Dena, 2009), world-building research (Wolf, 2012), and the rendering problem framework (Zharnikov, 2026l), this paper proposes a specification-driven architecture to close the gap. The canonical specification is reconceived as a version-controlled repository: editions are tagged commits; translations and adaptations are forks; canon governance operates through pull requests; and consistency validation functions as continuous integration. Style is a rendering parameter rather than a property of the specification; actors and translators function as rendering operators; and artificial intelligence clarifies the authorship question by distinguishing specification (the creative act) from rendering (the craft act). Seven testable propositions address franchise consistency, IP licensing as fork governance, and a future in which audiences become renderers — generating personalized expressions from a published canonical specification.

**Keywords**: transmedia storytelling, intellectual property, version control, canon, narrative consistency, creative AI

---

## 1. Introduction

Every mature domain of complex designed systems has independently developed formal mechanisms to verify that artifacts satisfy their specifications before deployment. Engineering uses tolerance inspection (standardized since the Industrial Revolution). Medicine uses clinical endpoint testing (formalized since the 1940s). Software uses continuous integration and test-driven development (Beck, 2002). Scientific publishing uses peer review (formalized since 1665). In each domain, the construct is the same — an artifact is validated against its specification before it is accepted as complete — even though each domain developed the construct independently in response to its own failure modes.

Creative intellectual property management is the conspicuous exception. Despite a rich theoretical literature on transmedia storytelling (Jenkins, 2006, 2011; Scolari, 2013), world-building (Wolf, 2012), and cross-media narrative (Ryan, 2001, 2015; Dena, 2009), no formal mechanism exists to verify that a new rendering of a franchise — a film, a game, a translation — is consistent with the established canon, to track when and why the canon changed, or to resolve contradictions between renderings that interpret the source differently. This absence is the gap that the present paper identifies and proposes to close.

The consequences of this gap are visible across the creative industries. In December 2017, Lucasfilm released *The Last Jedi*, a film that divided Star Wars audiences so thoroughly that the franchise's cultural coherence — maintained for four decades across hundreds of canonical texts — fractured visibly. The debate was not about cinematic quality. It was about *specification violation*: had the film's portrayal of Luke Skywalker contradicted the character's established properties? The question presupposed that a character has properties independent of any particular rendering — that somewhere, implicitly, a specification existed against which the film could be judged.

The same structural problem recurs across the screen industries. The Marvel Cinematic Universe maintains a team of continuity coordinators whose job is to track which facts are canonical across 33 films and dozens of Disney+ television series — a task that became visibly contested when Disney+ extensions introduced character behaviors and timelines that contradicted theatrical canon. The Harry Potter franchise has faced sustained criticism over retroactive canon modifications issued through social media rather than through the original texts. The *Game of Thrones* television adaptation diverged so substantially from its source material that audiences experienced it as a specification fork — two versions of the same intellectual property rendered from increasingly different underlying rules. More recently, *House of the Dragon* has navigated the challenge of establishing its own canon within a pre-existing specification, demonstrating that television franchises require explicit governance mechanisms for managing canonical inheritance.

The entertainment industry has developed semi-formal responses to this problem — Lucasfilm's Holocron continuity database (maintained by Leland Chee from 2000 to 2014), Marvel's continuity bible system, and community-driven wiki governance on platforms like Wookieepedia and Memory Alpha. These are real mechanisms for consistency tracking, and they demonstrate that the need for formal specification management is recognized in practice. However, they remain unversioned (lacking complete audit trails of canonical changes), unvalidated (relying on human memory rather than automated consistency checking), and medium-coupled (conflating what a story *is* with how it should appear in specific media). They are specifications in intent but not in architecture.

This paper proposes that the franchise consistency problem is an instance of the rendering problem (Zharnikov, 2026l) — the structural pattern in which a specification of bounded complexity is rendered into an implementation of vastly greater complexity, producing emergent phenomena that the specification does not contain. In the creative IP domain: the specification is the canon (characters, world rules, themes, constraints); the rendering is the medium-specific expression (novel, film, game, translation); and the emergent layer is audience perception — the meaning, emotion, and cultural significance that arise from the interaction between rendering and observer.

This paper advances three contributions:

1. *(Diagnostic)* Creative IP management is the only mature domain of complex designed systems that lacks a formal consistency-verification construct, despite semi-formal attempts — story bibles, continuity databases, fan wikis — that demonstrate the need.
2. *(Architectural)* The canon of any transmedia franchise can be reconceived as a versioned, validatable, governable specification, using version-control semantics as the implementation language rather than as the argument.
3. *(Media-studies relevance)* The framework reframes longstanding debates in transmedia and fan studies — canonicity, retcons, fix-it fics, the legitimacy of adaptation — as governance phenomena, and clarifies the authorship question raised by generative AI by locating originality in specification rather than rendering.

Git version control semantics are proposed as the implementation language not because creative IP IS software, but because software has developed the most widely adopted and well-understood formalization of versioning, branching, validation, and governance — a formalization that creative IP management currently lacks. The contribution is the gap, not the tool (Section 8.1).

---

## 2. Theoretical Foundation

### 2.1 The Rendering Problem

Zharnikov (2026l) identifies the rendering problem as a domain-independent structural pattern: a specification of bounded complexity is rendered into an implementation of vastly greater complexity, producing emergent phenomena that no specification contains. Three structural properties hold in every instance: (1) a specification gap — the implementation contains substantially more information than the specification; (2) a configuration layer — the same specification produces different implementations depending on contextual parameters; and (3) emergence — the system produces phenomena that, within the framework, cannot be predicted from the specification alone.

The rendering problem has been formalized across three prior domains — biological (genome to phenotype to consciousness), organizational (org-schema to operations to customer experience), and perceptual (brand emission policy to signal field to perception cloud) — each exhibiting the same three-layer structure: specification, implementation, emergence.

Creative intellectual property constitutes a fourth domain. The specification is the canon — the set of facts, rules, constraints, and relationships that define a fictional world and its inhabitants. The rendering is the medium-specific expression — a novel, film, game, translation, performance, or product. The emergent layer is audience perception — the meaning, emotional response, and cultural significance that arise from the interaction between a specific rendering and a specific observer. The specification gap is structural: no specification, however detailed, can determine all the information that a rendering must contain. A character specification that includes personality traits, speech patterns, physical appearance, and relational history still leaves open the infinite choices that constitute prose style, visual composition, vocal performance, and interactive design.

The specification constrains without determining. The gap between constraint and determination is where craft operates.

### 2.2 Transmedia Storytelling

Jenkins (2006) introduced the concept of transmedia storytelling as "a process where integral elements of a fiction get dispersed systematically across multiple delivery channels for the purpose of creating a unified and coordinated entertainment experience" (p. 95-96). This definition implicitly presupposes a specification layer: "integral elements of a fiction" that exist independently of their "delivery channels." Jenkins's formulation captures the intuition that a story has properties that persist across media, but does not formalize what those properties are, how they are maintained, or how consistency is validated. In a subsequent refinement, Jenkins (2011) distinguished transmedia *storytelling* (narrative extension) from transmedia *branding* (coordinated marketing across platforms), and argued that not all transmedia projects require a unified canon — some deliberately allow contradictions between extensions. This complication is important: the architecture proposed here applies to franchises that *choose* canonical consistency as a design goal, not to all transmedia projects indiscriminately.

Ryan (2001) provided the foundational theoretical framework for understanding how narrative structures behave across media. Her concept of medium affordances — the narrative possibilities that each medium enables or forecloses — established that different media preserve different dimensions of a story: a novel can represent interiority directly, a film cannot; a game can offer branching paths, a novel cannot. Ryan (2015) further distinguished "transmedia storytelling" (narrative extension across platforms) from "transmedial narratology" (the study of narrative across media). This observation is precisely the specification-rendering distinction: narrative structures that persist across media belong to the specification; structures that change with the medium belong to the rendering.

Dena (2009) offered the most rigorous design-theory treatment, showing that transmedia practice already involves implicit specification work: production teams maintain shared understandings of what the world *is* that constrain any particular rendering. The architecture formalizes what Dena observed in practice.

Scolari (2013) extended transmedia theory beyond the Anglophone tradition, showing that transmedia narratives are collaborative ecosystems in which multiple actors co-construct meaning across platforms — a property the pull request governance model (Section 4.3) is designed to formalize.

Wolf (2012) organized world-building into inventions, completeness, and consistency, treating world-building as an implicit specification activity in which the author constructs rules, histories, and geographies that constrain all subsequent renderings. Wolf does not formalize the specification or distinguish it architecturally from its renderings — a gap the present paper addresses.

### 2.3 Story Grammars and Computational Narratology

The idea that narrative has formal structure precedes digital computing. Propp (1928/1968) demonstrated that Russian folk tales share 31 narrative functions in a fixed sequential order — that the surface diversity of stories conceals an underlying structural specification. Propp's morphology is, in modern terms, a proto-specification: it defines WHAT happens (the function sequence) independently of HOW it is expressed (the specific characters, settings, and prose). A fairy tale in which a hero departs on a quest, encounters a donor, receives a magical agent, and defeats the villain instantiates Propp's grammar regardless of whether the hero is Ivan, Jack, or Frodo.

Gervás (2013) formalized this as a generative grammar — a specification from which individual story instances can be generated. The grammar specifies structural constraints; each story is a rendering that satisfies those constraints while adding the detail the grammar does not determine.

More recently, Pianzola et al. (2025) developed the GOLEM ontology (Graphs, Ontologies, and Linked Entities for Monitoring narrative and fiction) for tracking narrative provenance across versions and adaptations. GOLEM provides a formal vocabulary for identifying which narrative elements are preserved, modified, or lost across renderings — addressing, in ontological terms, the consistency problem that this paper addresses architecturally.

Sterman et al. (2022) found that creative professionals develop informal versioning systems — multiple copies, parallel drafts, checkpoint versions — that recapitulate Git semantics without using Git, arguing that creative work has the same structural need for version control as software development but lacks appropriate tools — a formalization that creative IP management currently lacks (Steinhoff, 2024). This paper extends their empirical observation into a formal architecture: the specification-rendering structure of creative IP maps onto version control semantics with systematic structural correspondence.

### 2.4 The Story Bible and Its Limitations

The entertainment industry's existing answer to the specification problem is the story bible — a document that records the essential properties of a fictional world for use by writers, producers, and licensees. Hayes (2011) produced a widely referenced template for transmedia production bibles, documenting the industry's best practice for capturing narrative specifications.

Story bibles exhibit three structural limitations that a formal specification architecture would resolve:

**Unversioned.** Story bibles are typically static documents or, at best, informally updated files. When a canon-altering event occurs in a new rendering (a character death, a retcon, a timeline revision), the story bible may or may not be updated. No audit trail records when the change was made, who authorized it, or what the previous version stated. In version control terms, the story bible has no commit history.

**Unvalidated.** No formal mechanism exists to check whether a new rendering is consistent with the story bible. Consistency checking is a human editorial process — knowledgeable individuals read new material and flag contradictions based on memory and expertise. As franchises grow in scope and duration (the Star Wars Expanded Universe contained over 300 canonical texts before its 2014 de-canonization), human consistency checking becomes unreliable. In version control terms, the story bible has no continuous integration.

**Medium-coupled.** Story bibles often conflate specification and rendering, describing not only what a character is but how they should appear, sound, and behave in specific media. This coupling constrains adaptation: a story bible that specifies "the character speaks with a British accent" has embedded a rendering decision (vocal performance) into the specification layer, preventing valid renderings in which the character speaks other languages or is rendered in a non-auditory medium.

The specification-driven architecture proposed in this paper addresses all three limitations: version control provides complete audit trails; validation rules enable automated consistency checking; and the formal separation of specification from rendering prevents medium-coupling.

### 2.5 Fan-Studies Positioning

Fan studies has developed a parallel tradition for analyzing how audiences negotiate canon. Hills (2002) demonstrated that fan engagement is structured by evaluative hierarchies — fans distinguish "good" from "bad" canon, policing specification fidelity through community debate. Hellekson and Busse (2006) showed that fan fiction communities have developed sophisticated internal governance norms: which character properties are sacrosanct, which world rules may be violated, and which authorial decisions are subject to community revision.

This paper's architectural treatment of canon complements rather than replaces fan-studies analysis. Fan studies treats canon as a social negotiation — a set of contested meanings co-produced by creators, industries, and audiences. This paper treats canon as an engineering specification — a structured artifact with version history, governance procedures, and consistency requirements. The two framings address different objects: fan studies describes how audiences *experience and contest* canon; this paper proposes how producers *maintain and govern* it. A fan community that produces "fix-it fics" correcting an unwanted character death is engaged in social negotiation; in architectural terms, the same community is generating specification-divergent forks. Both framings capture something real. The architectural account makes the governance structure legible; fan studies makes the cultural politics legible. Neither is sufficient alone.

---

## 3. The Specification Layer

### 3.1 What Belongs in the Specification

The specification of a creative work — its canon repository — contains the medium-independent facts, rules, and constraints that define the fictional world. This paper organizes these into five categories:

**Characters.** Traits (personality, values, fears, motivations), arcs (how the character changes), relationships, and constraints (behaviors excluded, speech registers, knowledge limits). The specification describes WHAT a character is, not HOW they appear in any particular medium.

**World rules.** The physics, technology, magic systems, social structures, and natural laws that govern the fictional world — axioms defining the possibility space for all events. World rules may evolve across versions, but at any given tag they are deterministic constraints on all renderings.

**Timeline.** The chronological sequence of events. The timeline is medium-independent: events occur in the same order regardless of medium. Flashbacks and nonlinear narration are rendering decisions — manipulations of presentation order, not alterations of the underlying timeline.

**Themes.** The central motifs, symbolic systems, and philosophical questions the work explores. A specification entry such as "the work examines the corruption of power" constrains all renderings to engage with that theme, even as the specific mechanisms vary across media.

**Constraints.** Meta-level governance rules: tone, content boundaries, and internal-logic rules. Constraints are not narrative content but rules that bound the space of valid renderings.

### 3.2 What Belongs in the Rendering

The rendering contains all medium-specific craft decisions: prose style, visual design, dialogue wording, performance, game mechanics, and musical score. Two novels can render the same specification in radically different prose styles without contradicting the specification; a film and a game can express the same characters and events through entirely different craft vocabularies. The rendering is where craft operates — within the constraints the specification establishes.

### 3.3 The Specification-Rendering Boundary

The boundary between specification and rendering is defined by a single criterion: **medium independence**. If an element of the work must be preserved across all valid renderings in all media, it belongs in the specification. If an element can legitimately vary between renderings without contradicting the work, it belongs in the rendering.

This criterion is not always easy to apply. Character appearance belongs in the specification if it drives plot events (a scar that identifies a character); it belongs in the rendering if it carries no narrative consequence. Setting geography belongs in the specification if spatial relationships constrain events; visual design of settings belongs in the rendering. Tone is typically a specification constraint — the work's overall register must be consistent — but the mechanisms by which tone is achieved (word choice, lighting, score) are rendering decisions.

The boundary is a design decision made by the specification's maintainers. Moving an element from rendering to specification increases consistency but reduces renderer freedom; moving it the other way increases freedom but reduces cross-rendering consistency. This trade-off is itself a governance question, addressed through the pull request mechanism described in Section 4.3.

---

## 4. Git Semantics for IP Lifecycle

The central architectural claim of this paper is that version control semantics map structurally onto intellectual property lifecycle operations. Table 1 presents the mapping; the subsections that follow develop each element.

Table 1: Git-to-IP Semantic Mapping.

| Git Concept | IP Lifecycle Operation | Example |
|---|---|---|
| Repository | Canon (the authoritative specification) | The Star Wars canon |
| Commit | Canonical event or rule change | "Han Solo dies in Episode VII" |
| Tag | Edition or version milestone | "Original Trilogy canon, v1.0" |
| Branch | Parallel development of canon | "What-if" storyline in development |
| Fork | Adaptation or translation | French translation; film adaptation |
| Pull request | Canon governance proposal | Screenwriter proposes character backstory |
| Merge | Canon incorporation | Proposed backstory accepted into canon |
| Merge conflict | Canon contradiction | Two renderings imply incompatible facts |
| CI/CD | Consistency validation | Automated check for timeline contradictions |
| .gitignore | Rendering-layer exclusions | Style guides, performance notes |
| README | Series bible summary | Overview of world, characters, themes |
| CHANGELOG | Canon evolution record | History of retcons and expansions |

*Notes*: The mapping is structural, not metaphorical. The claim is not that creative IP is like software, but that version control provides the most mature and widely adopted formalization of the consistency-verification construct that creative IP management currently lacks.

Table 2 places the proposed architecture in cross-domain context, showing that the consistency verification construct proposed here is not an innovation borrowed from software but a missing instance of a construct that multiple mature domains of complex designed systems have independently developed.

Table 2: Consistency Verification Constructs Across Design Domains.

| Design Domain | Verification Construct | Formalized | Mechanism |
|---|---|---|---|
| Engineering | Tolerance inspection | 1800s | Artifact measured against dimensional specifications before deployment |
| Medicine | Clinical endpoints | 1940s | Trial outcomes defined before enrollment; verified statistically |
| Financial auditing | Audit criteria | Ancient | Statements verified against predetermined standards |
| Software | Continuous integration / TDD | 2003 | Code tested against specifications on every change |
| Scientific publishing | Peer review | 1665 | Manuscript verified against community standards before publication |
| **Creative IP** | **???** | **Missing** | **No formal mechanism to verify rendering consistency with canon** |

*Notes*: "Formalized" indicates the approximate period when each domain developed a recognized, institutionalized consistency-verification mechanism. The Creative IP row is not missing data — no such mechanism currently exists.

### 4.1 Commits and Tags: Editions and Revisions

In Git, a commit records a discrete change to the repository, and a tag marks a named milestone. In the canon repository, a commit records a canonical change — a new character introduced, a world rule modified, a timeline event added — preserving the change, its author, its timestamp, and its rationale. The first published edition corresponds to a tagged commit `v1.0`; a revised edition is `v2.0`. The commit history records every change, enabling precise answers to "What changed between editions?" — information that story bibles, lacking any audit trail, cannot provide.

**Proposition 1.** *Every change to a creative work's specification can be represented as a commit to a version-controlled repository, preserving the change, its author, its timestamp, and its rationale, enabling complete reconstruction of any prior canonical state.*

When Disney acquired Lucasfilm in 2012 and reclassified the entire Expanded Universe as "Legends" in April 2014, the move functioned as a hard reset of the canonical branch — a forced rebase that discarded roughly 300 commits (novels, comics, games) and re-tagged a new `v1.0` from a different initial state. Had a versioned canon repository existed, every subsequent "What exactly changed?" dispute could have been resolved by diffing the pre- and post-2014 specification states rather than by consulting fan memory.

### 4.2 Forks: Translations, Adaptations, and Derivative Works

In Git, a fork creates an independent copy of a repository that shares the original's history but can evolve independently. In the canon repository architecture, every rendering is a fork: it takes the specification at a specific version and produces a medium-specific expression.

A translation is a fork from a tagged specification version; a film adaptation is a fork with more radical dimensional loss, gaining visuality and performance while losing interiority; a video game adaptation introduces interactivity and raises governance questions about whether player agency may alter canonical events. Each fork type illustrates the specification gap: the rendering must contain vast information the specification does not provide while respecting the constraints it does.

**Proposition 2.** *Every adaptation, translation, or derivative work from a creative specification can be represented as a fork from a tagged version of the canon repository, inheriting the specification's constraints while introducing medium-specific rendering decisions.*

The Marvel Cinematic Universe's Phase 4 multiverse story (2021–2023) introduced timeline variants — alternate-universe versions of existing characters — that share a partial specification with the main canonical branch. *Loki* (Disney+, 2021) establishes that divergent timelines fork from a "Sacred Timeline" main branch; *Doctor Strange in the Multiverse of Madness* (2022) depicts merge conflicts between branches as literal collision events. The franchise inadvertently made the fork-and-merge architecture of its own canon management visible to audiences, modeling precisely the structural relationship this paper formalizes.

### 4.3 Pull Requests: Canon Governance

In Git, a pull request (PR) is a proposal to merge changes from one branch or fork back into the main repository. The PR mechanism is fundamentally a governance tool: it enables review, discussion, and approval or rejection of proposed changes before they affect the canonical state.

In the canon repository architecture, pull requests formalize a process that franchises already perform informally: the negotiation of canon changes proposed by renderers. A screenwriter may discover that a character's backstory needs elaboration to make a scene work; in the canon repository architecture, the screenwriter submits a PR. If the IP owner approves, the backstory becomes a commit to the main repository and all future renderings must be consistent with it. This mechanism resolves the canonical/non-canonical ambiguity — are deleted scenes canonical? are author interviews? — structurally: content merged via an approved PR is canonical; content existing only in a fork is not.

**Proposition 3.** *Canon governance — the process by which proposed changes to a creative specification are reviewed, approved, or rejected — can be formalized as a pull request workflow with defined approval authorities, review criteria, and merge conditions.*

*House of the Dragon* (HBO, 2022–) required showrunners to submit effective pull requests to the *Game of Thrones* canonical specification before each major character or world-rule addition. When the series needed to establish the colors of Targaryen dragons — left underspecified in George R.R. Martin's source novels — production designers proposed a visual rendering decision that was subsequently ratified as specification-level fact by Martin's sign-off, making it binding on all future adaptations. The episode-by-episode negotiation between showrunner, novelist, and network recreates, informally, the review-approve-merge cycle that a formal pull request workflow would make explicit and auditable.

### 4.4 CI/CD: Consistency Validation

In software engineering, continuous integration and continuous deployment (CI/CD) refers to the automated testing of code changes against defined quality criteria before they are merged into the main branch. In the canon repository architecture, CI/CD corresponds to automated consistency validation: checks that run against every proposed change to the specification, and against every new rendering, to detect contradictions.

Four categories of consistency validation are identified:

**Character consistency.** Does a proposed scene violate a character's established properties? If the specification records that a character has a severe phobia, a scene depicting them casually confronting the phobic stimulus without acknowledgment is a validation failure. The validator does not judge aesthetic quality; it checks specification compliance.

**Timeline consistency.** Does a proposed event contradict established chronology? If Character A dies in Year 5 of the timeline, a scene set in Year 7 in which Character A appears alive is a validation failure — unless the specification includes a resurrection mechanism (a world rule that enables it).

**World rule consistency.** Does a proposed event violate established world rules? If the specification states that magic requires verbal incantation, a scene depicting silent magic is a validation failure — unless the specification has been updated to include an exception.

**Cross-rendering consistency.** Do two renderings (e.g., a novel and its film adaptation) imply contradictory facts about the specification? If the novel establishes a character as left-handed and the film depicts them as right-handed, a cross-rendering validator flags the discrepancy for resolution.

These validators are not hypothetical: NLP and knowledge-graph technologies already extract entities, relationships, and events from text for structured checking. The canon repository provides the knowledge base; the validators automate the checking, transforming consistency from a human editorial process that fails at scale to a governance process that scales.

**Proposition 4.** *Consistency validation across renderings of a creative specification can be automated through structured validation rules that check character properties, timeline chronology, world rules, and cross-rendering compatibility against the canonical specification.*

*Doctor Who* (BBC, 1963–) encodes its own consistency validator into the specification: the regeneration mechanic specifies that the Doctor's physical appearance and personality may change completely between incarnations, while continuity of memory, values, and history is preserved. This world rule acts as a compatibility bridge — a formally specified mechanism that allows radical rendering changes (new actor, new aesthetic) while validating continuity at the specification level. Every new Doctor effectively passes a character-consistency check not by matching prior renderings, but by satisfying the specification's memory-and-values constraints, leaving appearance as a rendering parameter.

### 4.5 Merge Conflicts: Canon Contradictions

In Git, a merge conflict occurs when two branches modify the same content in incompatible ways, requiring manual resolution. In the canon repository architecture, merge conflicts correspond to canon contradictions — situations in which two authorized renderings imply incompatible facts about the specification.

Canon contradictions are endemic in long-running franchises. Proctor (2017) provides a taxonomy of strategies for managing them, distinguishing "reboot," "retcon," "relaunch," "revival," and "refresh" as distinct modes of canon regeneration, each with different implications for continuity and audience expectation. The Star Wars franchise addressed contradictions through a four-tier canonicity system (G-canon, T-canon, C-canon, S-canon), later replaced by a binary canon/Legends split in 2014 — a wholesale retcon in Proctor's terms. The Doctor Who franchise maintains a deliberately ambiguous approach to canonicity, treating contradictions as features rather than bugs. The DC and Marvel comics universes periodically undergo "crisis" events whose narrative purpose is to resolve accumulated contradictions by resetting continuity — what Proctor calls "reboots."

In the canon repository architecture, these approaches correspond to different merge conflict resolution strategies:

- **Tiered canonicity** = branch priority rules: the main branch takes precedence over feature branches, which take precedence over forks
- **Continuity reset** = hard reset of the main branch to a new initial commit, discarding prior history
- **Deliberate ambiguity** = merge conflicts left unresolved, with rendering-level freedom to choose either interpretation

The canon repository architecture does not prescribe a resolution strategy; it provides the tooling to detect, record, and resolve contradictions transparently — preserving whatever approach the franchise's governance selects.

---

## 5. Rendering as Parameterized Projection

### 5.1 Medium as Dimensional Subspace

Each medium preserves some dimensions of the specification and loses others. This is not a failure of the medium; it is the structural consequence of projecting a high-dimensional specification into a lower-dimensional rendering space.

A novel preserves interiority with high fidelity but loses visuality. A film preserves visuality but loses interiority. A game preserves interactivity but loses authorial sequence control. A musical preserves emotional intensity but loses narrative density. The specification gap at each projection is structural, not a failure of craft — no film can render interiority as richly as a novel; no novel can render visuality as richly as a film. The dimensions lost in projection are trade-offs inherent in the medium's affordances (Ryan, 2001). "The book is always better" is a misunderstanding of the rendering problem: the book is not better; it preserves different dimensions.

**Proposition 5.** *Each medium constitutes a dimensional subspace of the full specification space, preserving some specification dimensions with high fidelity while structurally losing others, such that every rendering is an incomplete but valid projection of the canonical specification.*

The television adaptation of *Game of Thrones* (HBO, 2011–2019) demonstrates dimensional projection with explicit trade-offs. The source novels render interiority with high fidelity — Tyrion Lannister's political reasoning and self-doubt occupy chapters of internal monologue. The television rendering projects this interiority into visual performance and dialogue, preserving character arc and relational dynamics while losing the dense psychological specificity of first-person-adjacent narration. Neither is a failed rendering; each is a valid projection into a different dimensional subspace. The widely noted deterioration in perceived character consistency during Seasons 7–8 — when the series outpaced Martin's source specification — is precisely what the rendering problem predicts: renderers operating without a canonical specification diverge.

### 5.2 Style as Rendering Parameter

A rendering is not merely a projection of the specification into a medium. It is a *parameterized* projection: the same specification, in the same medium, can produce radically different renderings depending on style parameters. The relationship is formalized as:

```
output = render(spec, medium, style)
```

"Harry Potter rendered as a novel in Tolstoy's prose style" means: the same character specifications, world rules, timeline, and themes, expressed through Tolstoy's characteristic omniscient narration and psychological realism. "Harry Potter rendered as a film in Tarantino's directorial style" means: the same characters and events, expressed through Tarantino's characteristic nonlinear structure and tonal juxtaposition. The specification constrains; the style parameterizes.

Style is itself a formalizable specification: the rendering function takes two specifications as input — content (what to render) and style (how to render it). This double-specification structure explains both why style transfer is possible and why AI generation models work: they operationalize precisely this structure, accepting content prompts and style parameters as separate inputs.

### 5.3 Actors, Translators, Illustrators as Rendering Functions

If rendering is a parameterized function, then the human professionals who perform renderings are rendering operators. An actor takes a character specification and produces a performance rendering. A translator takes a textual specification and produces a linguistic rendering. An illustrator takes a narrative specification and produces a visual rendering.

This formalization clarifies several phenomena. The "Bond problem": six actors have rendered the same James Bond specification — same character traits, constraints, and arc; different rendering functions, different outputs. None is "the real Bond"; the specification constrains all of them equally. A "miscast" actor is a rendering function whose output violates specification constraints, not one who fails to match prior renderings. "Translation loss" is structural: puns, cultural references, and phonetic effects untranslatable from English to Japanese are dimensions of the source rendering that the target rendering cannot preserve — a specification gap, not a failure of craft.

### 5.4 The Audience as Renderer

The most consequential implication of the specification-rendering architecture is the possibility of audience-driven rendering. Murray (1997) anticipated this trajectory in *Hamlet on the Holodeck*, arguing that digital environments would eventually enable audiences to exercise agency within authored narrative structures — to become active participants in the rendering of stories rather than passive consumers of fixed expressions. The specification-rendering architecture formalizes Murray's vision: if the specification is formalized and published, and if rendering technology becomes sufficiently capable, then the audience member can generate personalized renderings from the canonical specification.

When specification and rendering are formally separated, an author can publish a story specification — characters, world rules, timeline, themes, constraints — from which different readers generate radically different renderings: a literary novel in Brazilian Portuguese, a graphic novel in Japanese manga style, an interactive text adventure. Each rendering is valid if it satisfies the specification's constraints. The pre-rendered product (the published novel, the released film) becomes one curated rendering among many possible expressions of the same specification.

Large language models already render prose from structured prompts; image and voice generation models do the same across visual and audio registers. The technology is immature but the trajectory is clear: rendering capability is advancing rapidly while specification — the curatorial judgment of what a story should be — remains a distinctively human activity.

**Proposition 6.** *When specification and rendering are formally separated, and rendering technology is sufficiently capable, observers with access to capable rendering tools can generate personalized renderings from a published canonical specification, transforming the author's role from renderer to specifier.*

Netflix's *Bandersnatch* (Black Mirror, 2018) represents an early partial implementation: viewer choices navigate branching narrative paths within a fixed specification. The specification (character psychology, world rules, theme of determinism) remained author-controlled; the viewer parameterized the rendering by selecting path branches. The experiment demonstrated both the appeal and the limits of audience-driven rendering without full specification publication — viewers controlled traversal order but not specification content, and the branching structure itself was a rendering decision, not a specification change.

---

## 6. AI in the Specification-Rendering Architecture

### 6.1 AI in Specification

Specification — the creative act of deciding what a story is about, who its characters are, what its world rules permit, and what themes it explores — remains primarily a human activity. AI can assist at the specification level: brainstorming character traits, exploring possibility spaces, identifying inconsistencies in draft specifications, generating "what-if" scenarios that the human author evaluates. But the curatorial judgment — "this is the story I want to tell; these are the constraints I choose to impose" — is a human act of intentional selection.

This distinction is not merely philosophical; it has legal consequences. In *Thaler v. Perlmutter* (D.D.C. 2023), the court held that AI cannot be a copyright author — that copyright requires human authorship. The U.S. Copyright Office's Part 2 report on copyrightability (2025) established an "expressive input" threshold: copyright attaches to the degree of human creative control over the output. In the specification-rendering architecture, the specification IS the locus of human creative control. The human who writes the character specification, defines the world rules, determines the timeline, and sets the thematic constraints has exercised precisely the kind of creative judgment that copyright protects. The rendering — whether performed by a human actor, a human translator, or an AI rendering engine — is the downstream execution of that creative judgment.

AI at the specification level constitutes genuine co-authorship. If an AI system generates a character backstory that the human author adopts unchanged, the AI has contributed to the specification — it has made a creative choice that constrains all subsequent renderings. The specification-rendering architecture makes this contribution visible and attributable: the commit log records who (or what) proposed each change and who approved it.

### 6.2 AI in Rendering

AI rendering capability is advancing rapidly across all media. Large language models render prose from structured outlines; image generation models render visual concepts from textual descriptions; voice synthesis models render speech from text; video generation models render moving images from structured prompts. In each case, the pattern is the same: the AI takes a specification (structured input that defines WHAT to render) and produces a rendering (detailed output that determines HOW it is expressed), filling the specification gap with the vast quantity of detail that the specification does not determine.

AI at the rendering level is a sophisticated tool, not an author. The specification-rendering architecture makes this distinction operationally precise: the AI generates rendering-level detail within specification-level constraints. Within this framework, the creative authority resides in the specification; the craft execution resides in the rendering. This is not a demotion of craft — rendering is extraordinarily complex, involves its own creative judgments (a performer's interpretation, a translator's choices), and the quality of AI rendering is not yet equivalent to expert human rendering in most domains. It is a structural observation about the locus of curatorial authority over what the story *is*, as distinct from the craft of how it is expressed.

### 6.3 Implications for Creative Labor

The specification-rendering architecture predicts a directional shift in creative labor: as AI rendering capability improves, human creative value moves up the stack from rendering to specification. Photography did not eliminate painting — it moved painting from visual recording to visual meaning-making; the photographer rendered reality while the painter specified meaning. The architecture predicts the same trajectory for creative industries: AI will automate rendering across media, and human creative labor will concentrate in specification — deciding WHAT stories to tell, defining WHAT characters to create, determining WHAT worlds to build.

This prediction is consistent with the labor provisions negotiated in recent creative industry disputes. The SAG-AFTRA 2023 agreement established provisions for informed consent regarding digital replicas of performers — operationalizing the principle that an actor's rendering function (their physical and vocal performance characteristics) is their property. The WGA 2023 agreement established that AI cannot be credited as a writer — operationalizing the principle that specification (writing) is a human creative act even when rendering (text generation) is performed by AI. Both provisions implicitly accept the specification-rendering distinction: the human controls the specification; the AI may assist with rendering; the human's creative authority over the specification is protected.

### 6.4 Observer-Specific Renderings

The combination of formalized specification and capable AI rendering enables observer-specific rendering: instead of one novel for all readers, the specification enables personalized renderings tailored to an observer's preferred language, medium, reading level, and aesthetic preferences. A single story specification could yield a literary novel in Brazilian Portuguese with expanded interiority, a young adult version in simplified English with increased dialogue, and an audio drama in Hindi — each satisfying the same specification constraints while parameterized for a different audience.

This mirrors a general pattern in observer-relative perception frameworks: the same source specification can produce different perceived outputs depending on how each rendering is parameterized for a given audience or observer context (Zharnikov, 2026a).

**Proposition 7.** *Observer-specific rendering — the generation of personalized renderings from a canonical specification, parameterized by observer preferences, language, medium, and reception context — preserves specification-level consistency while maximizing rendering-level accessibility.*

The near-term trajectory of streaming television offers a concrete instantiation: Disney+'s localized dubbing infrastructure already renders a single canonical specification — the MCU episode — into dozens of language-specific versions simultaneously, each using different vocal performance operators while preserving specification-level character consistency. The next step, currently in development across several studios, extends parameterization to pacing (longer or shorter cuts), accessibility features (audio description, signed rendering), and eventually AI-generated alternatives for elements like background dialogue — all governed by the same canonical specification, all required to pass the same consistency validators.

---

## 7. Industry Applications

### 7.1 Franchise Management

The most immediate application is franchise management. Current practice relies on editorial oversight — knowledgeable individuals who track canon informally — an approach that works at small scale but fails as franchises grow. The canon repository replaces this with formal governance: all renderings trace to the same versioned specification; canon changes are explicit commits with clear diffs; contradictions are detectable through CI/CD validators; and canon history is permanent and auditable.

### 7.2 Simulated Audience Testing

The specification-rendering architecture enables a novel form of audience research: running rendering specifications through parameterized "audience cohorts" — AI models with specified preferences, cultural backgrounds, and tolerance profiles — to predict reception per cohort before producing the rendering.

Reception varies systematically across cohorts defined by genre expectations, media literacy, and prior franchise engagement (Jenkins, 2006; Ryan, 2001). A franchise considering a tone shift could simulate reception before committing to production: the simulation predicts specification-rendering alignment per cohort — will each audience cohort perceive the rendering as consistent with the specification they have internalized — rather than commercial outcome.

### 7.3 IP Licensing as Fork Governance

IP licensing maps directly to fork governance. Johnson (2013) shows that franchise management is a negotiated system among producers, licensees, and audiences — not a top-down control structure. The canon repository provides a formal substrate within which that negotiation can be tracked and audited.

A license is a fork authorization with constraints:

- **Which version of the specification the licensee may fork from** (the licensed canon version)
- **Which specification elements the licensee may modify** (the license scope — can the licensee alter characters? add characters? change world rules?)
- **Which validation rules the licensee must satisfy** (the compliance requirements — must the derivative work pass timeline consistency checks? character consistency checks?)
- **Whether the licensee may submit PRs to the main repository** (the contribution rights — can a game developer's narrative innovations be incorporated into the canon?)

Fan fiction occupies a distinctive position in this framework. Fan works fork from the canonical specification without explicit authorization, and "fix-it fics" that override unpopular specification elements — character deaths, contested plot decisions — function structurally as community-authored pull requests that the official repository has declined to merge (Hills, 2002; Hellekson & Busse, 2006). The architecture formalizes this relationship: a fan work that respects all character specifications and world rules but adds new content is a specification-compliant fork; a fan work that rewrites character properties is specification-divergent. The distinction is structural and measurable, not evaluative.

### 7.4 Non-Western Transmedia Models

The architecture proposed here is grounded in Western franchise management, where canonical consistency is typically treated as a design goal. However, alternative transmedia traditions challenge the assumption that consistency is always desirable, and these counterexamples help define the architecture's scope.

The Japanese *media mix* model (Steinberg, 2012) offers the most instructive contrast. In the media mix, a fictional world is simultaneously expressed across manga, anime, light novels, games, and merchandise — but consistency across expressions is deliberately loose. The "world" (its aesthetic, its character types, its emotional register) is the shared specification, while narrative details vary freely across media. A character's backstory in the manga may contradict their backstory in the anime, and this is treated not as an error but as a feature of the creative ecosystem. In the terms of this paper, the Japanese media mix operates with a *thinner* specification — one that constrains world-feel and character identity but leaves narrative specifics to the rendering layer. The canon repository architecture accommodates this by treating specification thickness as a governance parameter: franchises choose how much to specify, and the architecture tracks consistency relative to whatever specification exists.

Korean webtoon-to-K-drama adaptations represent a different rendering model. The webtoon provides a visual and narrative specification; the live-action drama is a rendering that must project the webtoon's two-dimensional visual language into embodied performance while adapting serial pacing for broadcast rhythms. The dimensional projection is explicit: the webtoon specifies character appearance with a precision (stylized illustration) that the drama must reinterpret through casting and costume — a rendering decision constrained but not determined by the specification.

These models demonstrate that the architecture is not culturally prescriptive: it provides infrastructure within which any consistency policy — from strict canonicity to deliberate looseness — can be implemented and governed transparently.

---

## 8. Discussion

### 8.1 The Gap, Not the Tool

The contribution of this paper is not the application of Git semantics to creative IP — it is the identification that creative IP management lacks a formal consistency verification mechanism that the mature domains examined here (engineering, medicine, financial auditing, software, scientific publishing) have each independently developed. Each arrived at formal consistency verification in response to its own domain-specific failure modes. Creative IP management has not. That is the theoretical contribution: the gap.

Git semantics are proposed as the implementation because they provide the most widely adopted and well-understood formalization of versioning, branching, validation, and governance. But the choice of Git is instrumental. A different implementation — one that preserved version history, enabled branching for parallel development, enforced validation rules, and maintained audit trails — would serve the same architectural purpose. The argument does not depend on Git being "the right tool." It depends on the gap being real and the construct being widespread.

### 8.2 Connection to Adjacent Frameworks

The specification-driven architecture for creative IP is an instance of the rendering problem (Zharnikov, 2026l) applied to a new domain. The structural pattern — specification, rendering, perception, with specification gap at each transition — holds across five domains now identified:

Table 3: The Rendering Problem Across Five Domains.

| Domain | Specification | Rendering | Perception |
|---|---|---|---|
| Biological | Genome | Phenotype | Consciousness |
| Organizational | Org. schema | Operations | Customer experience |
| Brand | Brand specification | Marketing signals | Perception cloud |
| Creative IP | Canon repository | Novel, film, game | Audience meaning |
| Scientific knowledge | Paper specification | Published paper | Scientific community reception |

*Notes*: Organizational schema theory and brand specification theory are developed in Zharnikov (2026i) and Zharnikov (2026a) respectively. The scientific knowledge row is developed in Zharnikov (2026t, 2026u), which apply specification-driven thinking to scientific publishing — the same structural gap (absence of versioned specification) producing the same failure modes (unversioned claims, unvalidated outputs, medium-coupled reports) that this paper diagnoses in creative IP. The construct is cross-domain, not Git-specific.

The unifying pattern holds across all five domains: specification leads to rendering leads to perception, with a structural gap at each transition. Domain-specific phenomena — retcons in IP, brand dilution in marketing, organizational drift in management, phenotypic plasticity in biology, citation drift in science — are all manifestations of the same structural property.

### 8.3 The Authorship Question

Authorship, in this framework, is specification — the creative act of determining WHAT the story is. The renderer — whether human or AI — determines HOW it is expressed. This is consistent with legal frameworks in which copyright attaches to original creative choice: the specification is the locus of that choice, and the architecture makes the distinction visible rather than merely asserted. When AI enters the rendering process, the analysis does not change: the human who maintains the specification remains the author; the AI rendering from it is a tool.

### 8.4 Limitations

Several limitations constrain the scope and applicability of the proposed architecture.

**Specification completeness.** Some creative works resist specification. A lyric poem may have no separable specification — its meaning is entirely constituted by its rendering (word choice, rhythm, sound). A work of abstract visual art may have no narrative or thematic specification independent of its visual rendering. The specification-rendering architecture is most applicable to narrative works with identifiable characters, world rules, and events — franchises, series, and transmedia properties. It is least applicable to works whose meaning is inseparable from their form.

**Specification-rendering co-evolution.** Specification and rendering often co-evolve: Tolkien discovered Middle-earth through writing; Kubrick's films evolved during filming. The architecture is most applicable to franchises that have matured past the discovery phase. For works in active creation, it provides retrospective formalization rather than prospective governance.

**Specification formalization.** Much of what constitutes a creative work's identity — mood, sensibility, aesthetic "feel" — resists decomposition into discrete testable propositions. A validator can check whether a character is alive at a given timeline point, but not whether a scene "feels like Star Wars." The architecture addresses discrete, testable specification elements more effectively than continuous, tonal ones.

**Creative constraint.** Formalization may constrain creative discovery. The architecture is most useful for collaborative and multi-rendering contexts where consistency across renderers is essential; for single-author works, the overhead may exceed the benefit.

**Technological maturity.** The automated validators described in Section 4.4 require natural language understanding capabilities that are not yet reliable enough for production use. Current AI can detect simple timeline contradictions but struggles with nuanced character consistency checking — determining whether a character's behavior in a specific situation is consistent with their established personality requires interpretive judgment that AI does not yet perform reliably.

### 8.5 Future Work

Four directions merit investigation: (1) **Empirical validation** — applying the canon repository architecture to a real franchise, building validators, and measuring whether the architecture improves consistency compared to traditional editorial oversight. (2) **Prototype tooling** — a proof-of-concept combining version control with narrative-specific validators and audience simulation. (3) **Specification extraction** — semi-automated methods for extracting canonical specifications from existing renderings using NLP, making the architecture applicable to existing franchises. (4) **Formal metrics for specification gap** — information-theoretic measures of how much information a rendering contains beyond what the specification determines, enabling quantitative comparison across media and franchises.

---

## 9. Conclusion

This paper has argued that the franchise consistency problem — the accumulation of contradictions across transmedia renderings of creative intellectual property — is a structural consequence of the rendering problem: the pattern in which a specification of bounded complexity is rendered into an implementation of vastly greater complexity. The consistency problem persists because franchises lack a formal specification layer. Story bibles are unversioned, unvalidated, and medium-coupled. The result is the familiar syndrome of retcons, contradictions, and canon disputes.

The structural diagnosis — that creative IP is missing a consistency-verification construct that every other mature domain of complex designed systems has independently built — is the paper's primary claim; the Git-based architecture is the proposed instantiation, not the argument. Style is a rendering parameter rather than a property of the specification; actors and translators function as rendering operators; and the audience can become the renderer when specification and rendering technology are sufficiently mature.

For television and new media scholarship, the architecture offers three advances. Theoretically, it bridges transmedia storytelling theory with platform governance by supplying a formal language for canon as infrastructure — one that television studies can use to analyze continuity crises, retcon controversies, and streaming-era franchise expansion. Practically, it suggests concrete tooling — versioned canon repositories, automated consistency validators, simulated audience testing — that could reduce production friction and licensing disputes across screen industries. Politically, it reframes audience participation: when specifications are published, audiences equipped with capable rendering tools become co-creators rather than mere interpreters, shifting power from centralized IP owners toward distributed cultural production.

Most fundamentally, the specification-rendering architecture clarifies the authorship question at a moment when that question has become urgent. Authorship is specification: the creative act of deciding WHAT the story is. Rendering is the craft act of deciding HOW the story is expressed. AI is rapidly becoming capable of rendering; specification remains a distinctively human creative activity. The author's value is not in the prose, the image, or the performance. It is in the specification — the structured creative judgment that constrains all renderings and outlives every one of them.

---

## References

Beck, K. (2002). *Test-driven development: By example*. Addison-Wesley.

Dena, C. (2009). *Transmedia practice: Theorising the practice of expressing a fictional world across distinct media and environments* [PhD thesis, University of Sydney].

Gervás, P. (2013). Propp's morphology of the folk tale as a grammar for generation. In *Proceedings of the Workshop on Computational Models of Narrative* (OASIcs, Vol. 32, pp. 106–122). Schloss Dagstuhl. https://doi.org/10.4230/OASIcs.CMN.2013.106

Hayes, G. P. (2011). *How to write a transmedia production bible*. Screen Australia.

Hellekson, K., & Busse, K. (Eds.). (2006). *Fan fiction and fan communities in the age of the Internet*. McFarland.

Hills, M. (2002). *Fan cultures*. Routledge.

Jenkins, H. (2006). *Convergence culture: Where old and new media collide*. NYU Press.

Jenkins, H. (2011, August 1). Transmedia 202: Further reflections. *Confessions of an Aca-Fan*. http://henryjenkins.org/blog/2011/08/defining_transmedia_further_re.html

Johnson, D. (2013). *Media franchising: Creative license and collaboration in the culture industries*. NYU Press.

Murray, J. H. (1997). *Hamlet on the Holodeck: The future of narrative in cyberspace*. Free Press.

Pianzola, F., Cheng, L., Pannach, F., Yang, X., and Scotti, L. (2025). The GOLEM ontology for narrative and fiction. *Humanities*, 14(10), 193. https://doi.org/10.3390/h14100193

Proctor, W. (2017). Reboots and retroactive continuity. In M. J. P. Wolf (Ed.), *The Routledge companion to imaginary worlds* (pp. 361–371). Routledge.

Propp, V. (1928/1968). *Morphology of the folktale* (L. Scott, Trans., 2nd ed.). University of Texas Press.

Ryan, M.-L. (2001). *Narrative as virtual reality: Immersion and interactivity in literature and electronic media*. Johns Hopkins University Press.

Ryan, M.-L. (2015). Transmedia storytelling: Industry buzzword or new narrative experience? *Storyworlds: A Journal of Narrative Studies*, 7(2), 1–19.

Scolari, C. A. (2013). *Narrativas transmedia: Cuando todos los medios cuentan*. Deusto.

Steinberg, M. (2012). *Anime's media mix: Franchising toys and characters in Japan*. University of Minnesota Press.

Steinhoff, F. (2024). Version control for creative economies. *Convergence: The International Journal of Research into New Media Technologies*. https://doi.org/10.1177/13548565241234662 [VOL/PAGES TO CONFIRM]

Sterman, S., Nicholas, M. J., & Paulos, E. (2022). Towards creative version control. *Proceedings of the ACM on Human-Computer Interaction*, 6(CSCW2), Article 336. https://doi.org/10.1145/3555756

*Thaler v. Perlmutter*, No. 1:22-cv-01564-BAH (D.D.C. Aug. 18, 2023).

U.S. Copyright Office. (2025). *Copyright and artificial intelligence, Part 2: Copyrightability*. U.S. Copyright Office / Library of Congress.

Wolf, M. J. P. (2012). *Building imaginary worlds: The theory and history of subcreation*. Routledge.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026i). The Organizational Schema Theory: Test-driven business design. Working Paper. https://doi.org/10.5281/zenodo.18946043

Zharnikov, D. (2026l). The rendering problem: From genetic expression to brand perception. Working Paper. https://doi.org/10.5281/zenodo.19064426

Zharnikov, D. (2026t). Paper as specification: A machine-readable standard for scientific claims. Working Paper. https://doi.org/10.5281/zenodo.19210037

Zharnikov, D. (2026u). Research as repository: A Git-native protocol for scientific knowledge production. Working Paper. https://doi.org/10.5281/zenodo.19294864

---

## Acknowledgements

This research received no external funding. AI assistants (Claude Opus 4.7, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

## Data Availability

The canon-as-repository demonstration referenced in Section 4 is publicly available at https://github.com/spectralbranding/sbt-papers/tree/main/canon-as-repository under the MIT licence. No other datasets were used.

## Conflict of Interest

The author declares no competing interests.

---

## Changelog

- v1.1.0 (2026-05-10): URL migration — spec repository moved from standalone github.com/spectralbranding/canon-repo to consolidated github.com/spectralbranding/sbt-papers/tree/main/canon-as-repository. Metadata version bump; body unchanged.
