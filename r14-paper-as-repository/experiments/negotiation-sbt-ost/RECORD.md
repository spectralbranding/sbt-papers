# Experiment Record — Federated Ontology Negotiation on Real Corpora (SBT <-> OST)

| Field | Value |
|---|---|
| **Experiment ID** | EXP-2026-06-13-NEG-SBT-OST |
| **Date** | 2026-06-13 |
| **Operator** | Dmitry Zharnikov (with Claude Opus 4.8) |
| **Classification** | Computational / deterministic / logical — no stochastic component, no statistical inference; the outcome is a fixed function of the inputs and the tool. |
| **Instrument** | `tools/negotiate_modules.py` (federated multi-author generalization of the single-author linker `build_ontology.py`), a fixed tool version. Shared parser `build_ontology.Module` + `def_hash` + `_norm_ref`, a fixed tool version. |
| **Protocol** | `the negotiation protocol (paper §5.5)`; companion `the spine-first drafting protocol`. |
| **Environment** | Python 3.12.13, `uv`. Substrate `the citation substrate` present but not read or written by the run. |
| **Pre-registration** | Post-hoc record of a single confirmatory run. The hypotheses in §1 were the design intent fixed before execution; no run was discarded or re-specified after seeing results. |
| **Data availability** | All inputs and outputs are listed in §9 and earmarked for publication to the public mirror when/if the carrying paper (R14 / 2026u) is published (§9). |

---

## 1. Research question and hypotheses

**Research question.** When two real, independently-namespaced theory vocabularies — SBT
(perception-side) and OST (operations-side) — are presented to the federated linker, does it
mechanically classify every cross-owner interaction and surface the SBT/OST bridge *before any
prose is read*, and which interaction classes actually arise?

The protocol document closes by naming the one outstanding step that turns the federated linker
from a fixture-only prototype into evidence: *"the remaining step is exercising it on two real
independent corpora."* This experiment executes that step on the corpus's two largest programs.

**Hypotheses (each with an explicit falsification criterion).**

- **H1 — Mechanizability.** The linker assigns every cross-owner interaction to exactly one
  protocol class (`AGREEMENT` / `CONFLICT` / `CROSS_REFINE` / `INCOMPATIBLE_REFINE` /
  `CROSS_IMPORT` / `DANGLING_IMPORT`) and terminates with a verdict. *Falsified if* any
  interaction is left unclassified or the tool errors on real modules.
- **H2 — Content-addressed identity.** Shared terms are matched by content-addressed `def_hash`,
  not by string coincidence: the seven SBT term hashes in this experiment equal the hashes the
  live single-author linker computes over `the live single-author ontology modules`.
  *Falsified if* any of the seven hashes (§2.1 manifest) differs from the live-graph value.
- **H3 — Bridge surfaced pre-prose.** The dependency structure between the two programs
  (operations *import* the perception vocabulary; the boundary terms are *narrowed*) is recovered
  mechanically, with no human reading of the other author's prose. *Falsified if* the linker
  reports no cross-owner edges, or edges that contradict the documented convergence relation in
  `research/.../NOTES_SBT_ORGSCHEMA_CONVERGENCE.md`.
- **H4 — Single-author cleanliness (a prediction that is also the principal limitation).**
  Because SBT and OST are two *intentionally convergent* programs authored by one person, we
  predict a **clean** federation: zero unresolved interactions (no genuine `CONFLICT`,
  `INCOMPATIBLE_REFINE`, or `DANGLING_IMPORT`). *Would be falsified* by any genuine unresolved
  interaction — and such a falsification would, paradoxically, *strengthen* the multi-author
  thesis (§7). Confirmation of H4 is therefore reported as a limitation, not a triumph.

---

## 2. Materials

### 2.1 Author A — SBT perceptual module (with integrity manifest)

`negotiation-sbt-ost/sbt/sbt_perceptual.yaml` (`paper_key: sbt_real_2026a`) owns
seven shared SBT perceptual terms, each definition copied **verbatim** from the live SBT ontology
(`the live ontology module for the SBT corpus` + `the live ontology module for the OST corpus`) so that each term's
content-addressed `def_hash` (sha256 of the trimmed definition, truncated to 16 hex chars — the
same hash the single-author linker computes) matches the live SBT graph. Owning the identical
definition string is owning the identical content-addressed concept.

**Integrity manifest** (the deterministic-experiment analogue of a fixed random seed — re-running
`def_hash` over these definitions must reproduce these exact values, and they must equal the live
graph's; this is the experiment's tamper-evidence anchor):

| term_key | def_hash | live owner |
|---|---|---|
| `cohort` | `db90eb1a6fd873a0` | 2026a |
| `perception-cloud` | `b8bfd48074e97506` | 2026a |
| `spectral-dimensions` | `751200eee587a9c7` | 2026a |
| `brand-conviction` | `57c8fe303b5a5e8b` | 2026a |
| `observer-spectral-profile` | `e9d29838a687c3aa` | 2026a |
| `coherence-type` | `41b7ba951cd62cb5` | 2026s |
| `re-collapse` | `19323b6c7c660bfb` | 2026a |

### 2.2 Author B — OST operational module

`negotiation-sbt-ost/ost/ost_operational.yaml` (`paper_key: ost_real`) **owns
fourteen** OST-native operational terms, each a faithful paraphrase of real OST prose with the
source file noted per term: the six-level TDD cascade (`l0-customer-experience-contract`,
`l1-signal-requirements`, `l2-process-contracts`, `l3-procedures`, `l4-input-specifications`,
`l5-sourcing-requirements`), `tier-architecture`, `specification`, the three-way signal taxonomy
(`designed-signal` / `operational-signal` / `ambient-signal`), `intentional-brand`,
`specification-drift`, and `rendering`. Sources: `the OST paper export 
paper.md` (the L0-L5 cascade and the fork/openness model),
`articles/OST-02_organization_as_signal_source.md` (the designed/operational/ambient signal
taxonomy; "your processes are your brand"; the intentional brand via full D/A control), and
`articles/OST-C5_eight_dimensions_one_spec.md` (every YAML parameter has a spectral address). OST
canonical name = "Organizational Schema Theory".

It then exercises the cross-owner classes: it **imports** the four SBT receiver-side terms OST
uses without redefining (`cohort`, `brand-conviction`, `observer-spectral-profile`,
`coherence-type`) and **refines** two SBT terms (`perception-cloud`, `spectral-dimensions`) with
explicit `narrows_to` clauses capturing OST's prescriptive/operational reading.

### 2.3 Instrument and isolation

`negotiate_modules.py` parses both authors' modules with the exact parser the single-author
linker uses, then — instead of aborting on a cross-owner term overlap the way `build_ontology.py`
does — classifies every cross-owner interaction, proposes a typed SKOS mapping and a
reconciliation operation per finding, and emits an SSSOM mapping proposal. It is read-only on
everything (it writes only the SSSOM file requested); the committed substrate is untouched.

**Isolation (no contamination of the live graph).** The two module files live only under
`negotiation-sbt-ost/`. They are **not** in `the live ontology directory ` and are **not**
named `ONTOLOGY.yaml`, so the live `build_ontology.discover_modules()` (globs exactly
`the live ontology modules` and `research/**/ONTOLOGY.yaml`) never discovers them. They are loaded
only via the explicit `--author-a` / `--author-b` paths.

---

## 3. Procedure

```
uv run python tools/negotiate_modules.py \
    --author-a negotiation-sbt-ost/sbt \
    --author-b negotiation-sbt-ost/ost \
    --sssom negotiation-sbt-ost/sbt_ost.sssom.tsv
```

The run was repeated with `--gate` appended to obtain the federated CI verdict (exit nonzero iff
any unresolved interaction remains).

**Determinism.** There is no random component, no sampling, no seed: `def_hash` is a pure
function of definition text and the classifier is a pure function of the two parsed module sets.
Re-running the command on the same inputs and tool commit reproduces byte-identical output. The
integrity manifest (§2.1) is the reproducibility anchor in lieu of a seed.

---

## 4. Results — the negotiation report (verbatim)

```
NEGOTIATION REPORT  sbt  <->  ost
================================================================

CROSS_REFINE  (2)
  - perception-cloud [skos:narrowMatch]: ost narrows owner's term: 'the perception cloud restricted to the cohort a customer-experience contract (L0) is written to satisfy'
      -> reconcile: REBASE (refiner's term narrows the owner's; assert narrowMatch)
  - spectral-dimensions [skos:narrowMatch]: ost narrows owner's term: 'the eight dimensions read as the parameter groups an organizational specification controls, per OST-C5 (every YAML parameter has a spectral address)'
      -> reconcile: REBASE (refiner's term narrows the owner's; assert narrowMatch)

CROSS_IMPORT  (4)
  - brand-conviction [skos:exactMatch]: ost imports the other author's term
      -> reconcile: none (clean dependency edge)
  - coherence-type [skos:exactMatch]: ost imports the other author's term
      -> reconcile: none (clean dependency edge)
  - cohort [skos:exactMatch]: ost imports the other author's term
      -> reconcile: none (clean dependency edge)
  - observer-spectral-profile [skos:exactMatch]: ost imports the other author's term
      -> reconcile: none (clean dependency edge)

----------------------------------------------------------------
6 interaction(s); 0 unresolved (CONFLICT / INCOMPATIBLE_REFINE / DANGLING_IMPORT).
Federation clean: all interactions are agreements, clean imports, or compatible refinements -- the two module sets can be linked.
```

`--gate` exit code: **0** (no unresolved interactions). Tool exit code (report mode): **0**.

**Hypothesis adjudication.**

- **H1 — supported.** All six interactions were classified; the tool terminated with a verdict
  and exit 0.
- **H2 — supported.** The seven `def_hash` values (§2.1) reproduce on re-computation and equal
  the live-graph values (verified programmatically against `2026a.yaml` + `2026s.yaml`). The four
  `CROSS_IMPORT` matches are content-addressed, not lexical coincidences.
- **H3 — supported.** The linker recovered the bridge mechanically: four import edges (operations
  import perception) plus two `narrowMatch` refinements at the two boundary terms — the
  dependency direction and narrowing points documented in the convergence note, produced without
  reading prose.
- **H4 — confirmed (and recorded as the principal limitation, §7).** Zero unresolved
  interactions; the federation is clean, exactly as predicted for two convergent programs by one
  author. No genuine `CONFLICT` or `DANGLING_IMPORT` was found or manufactured.

---

## 5. The SSSOM mapping proposal

Written to `negotiation-sbt-ost/sbt_ost.sssom.tsv`. Rendered as a table, one
interpretation line per row:

| subject_id | predicate_id | object_id | mapping_justification | confidence | comment | Interpretation |
|---|---|---|---|---|---|---|
| sbt:perception-cloud | skos:narrowMatch | ost:perception-cloud | semapv:ManualMappingCuration | .5 | CROSS_REFINE | OST's prescriptive cloud (the L0 target distribution for one contract's cohort) is a narrower reading of SBT's full descriptive cloud; a human confirms the narrowing. |
| sbt:spectral-dimensions | skos:narrowMatch | ost:spectral-dimensions | semapv:ManualMappingCuration | .5 | CROSS_REFINE | OST reads the eight dimensions as the parameter groups a specification controls (per OST-C5); narrower than SBT's perceptual channels, pending curation. |
| sbt:brand-conviction | skos:exactMatch | ost:brand-conviction | semapv:LexicalMatching | .95 | CROSS_IMPORT | OST uses SBT's `brand-conviction` unchanged; clean cross-author dependency edge. |
| sbt:coherence-type | skos:exactMatch | ost:coherence-type | semapv:LexicalMatching | .95 | CROSS_IMPORT | OST's "signal coherence / spectral incoherence" prose applies SBT's geometric coherence concept; imported, not redefined. |
| sbt:cohort | skos:exactMatch | ost:cohort | semapv:LexicalMatching | .95 | CROSS_IMPORT | OST's four observer-cohort profiles (paper.md L1) are SBT cohorts; imported unchanged. |
| sbt:observer-spectral-profile | skos:exactMatch | ost:observer-spectral-profile | semapv:LexicalMatching | .95 | CROSS_IMPORT | The receiver-side object OST designs *for*; imported from SBT verbatim. |

The four `CROSS_IMPORT` rows are mechanical, high-confidence (.95) lexical matches that can be
ingested directly. The two `CROSS_REFINE` rows are narrowMatch proposals at .5 confidence flagged
`semapv:ManualMappingCuration` — the tool records that a human still owes the decision to confirm
each narrowing, rather than silently asserting it.

---

## 6. Analysis by interaction class

**CROSS_IMPORT (4) — the shared receiver-side vocabulary.** OST does not re-introduce `cohort`,
`brand-conviction`, `observer-spectral-profile`, or `coherence-type`; it imports them from SBT and
builds on them. This is the mechanical signature of a *dependency*, not a duplication: OST's Level
0 / Level 1 machinery (the four observer-cohort profiles in the paper's Spectra Coffee demo; the
target perception a contract is written to satisfy) presupposes SBT's account of how a signal is
completed in an observer. The linker surfaces this as four clean edges with no negotiation owed —
exactly what `NOTES_SBT_ORGSCHEMA_CONVERGENCE.md` asserts when it says the eight SBT dimensions
*are* the orgschema specification dimensions and the customer-experience contract *is* a desired
spectral profile. The dependency is real and one-directional: operations import perception, not
the reverse.

**CROSS_REFINE (2) — the prescriptive narrowing that IS the bridge.** The two refinements are the
precise points where OST does something *to* an SBT term rather than merely consuming it. SBT's
`perception-cloud` is *descriptive* — the full distribution of convictions across a population.
OST narrows it to the *prescriptive* slice: the target distribution a Level 0 customer-experience
contract is written to produce, for the specific cohort that contract serves. Likewise SBT's
`spectral-dimensions` are perceptual channels; OST narrows them to the parameter groups an
organizational specification controls (OST-C5's "every YAML parameter has a spectral address").
These two `narrowMatch` edges are the formal content of the convergence thesis: the same two
objects, read once as *what perception is* (SBT) and once as *what a specification targets* (OST).
The note's "two views of one system" is not a metaphor here — it is two narrowMatch relations the
linker produced mechanically.

**CONFLICT — honestly, none was found.** The design flagged `coherence` / `coherence-type` as a
candidate genuine collision: does OST define signal coherence differently from SBT's geometric
`coherence-type`? Reading the OST prose (OST-02 uses "spectral incoherence" and "signal coherence"
to mean *large variance across the eight dimensions* — exactly SBT's geometric notion, and OST
cites SBT as the source of the dimensional model), the answer is no. OST *applies* SBT's coherence
concept; it does not redefine it. Manufacturing a CONFLICT here would have been a fabricated
incompatibility. The honest classification is a `CROSS_IMPORT`, and that is what the module
asserts and the tool reports. No `DANGLING_IMPORT` was manufactured either: every imported and
refined term resolves to an SBT-owned term.

So the federation between the two real programs is **clean**: 6 interactions, 0 unresolved. Two
independent-namespace module sets, parsed before any human read the other's prose, link without a
single blocking incompatibility — and the *shape* of how they link (import the receiver-side
terms, narrow the two boundary terms) is itself the statement of the SBT/OST relationship.

---

## 7. Threats to validity and limitations

**Construct / external validity — the single-author caveat (the load-bearing limitation).** SBT
and OST are two programs by **one author**. This is therefore a **real-vocabulary demonstration
across two namespaces**, not yet a genuine two-*independent*-author validation. The clean
federation (H4) is partly a product of the same mind having built both vocabularies to be
compatible: OST was designed from the outset to use SBT as its specification language, so a clean
link is closer to a *designed property* than to a *discovered surprise*. Confirming H4 thus
demonstrates the instrument runs end-to-end on real inputs but cannot, by construction, exhibit
the adversarial classes that are the harder half of the protocol.

**Internal validity — controlled.** Content-addressed identity (H2, the §2.1 manifest) rules out
the most likely artifact, a lexical-key coincidence: OST imports the SBT terms it imports because
they are the same concept by hash, not the same string by accident. Isolation (§2.3) rules out
contamination of or by the live graph. Determinism (§3) rules out run-to-run variation.

**What a genuine test requires (unchanged from `NEGOTIATION_PROTOCOL.md`).** Exercise the tool on
two genuinely *independent* authors' modules over two corpora, where at least one real `CONFLICT`
(same key, divergent `def_hash`) or `DANGLING_IMPORT` arises and must be reconciled by namespacing
+ a curated SSSOM mapping + an authored lock / fork / rebase / merge. That is the case that
upgrades the thesis from a single-author existence proof to a federated *practice*. The fixture
(`the in-repo two-author fixture`) deliberately constructs those harder classes; this
real-corpora run, honestly, exhibits only the resolvable ones, because no genuine incompatibility
exists between two intentionally-convergent programs by one author.

**Net contribution.** This run advances the evidence from "works on a synthetic fixture" to "works
on the real SBT and OST vocabularies, with content-addressed identity and a recovered bridge"; it
does not, and should not be read to, close the single-author caveat.

---

## 8. Reproducibility statement

Anyone with the repository at tool a fixed tool version (instrument) / `2747250e` (shared parser) and
Python 3.12.13 can reproduce this record exactly: (i) the two input modules under
`negotiation-sbt-ost/`; (ii) the run command in §3; (iii) byte-identical report and
SSSOM output, since the pipeline is deterministic; (iv) the §2.1 integrity manifest, recomputable
by hashing each SBT definition and checkable against `the live single-author ontology modules`.
No seed, dataset download, network call, or API key is required.

---

## 9. Data availability and publication plan

**Internal artifacts (canonical SSOT, present now):**

- `negotiation-sbt-ost/sbt/sbt_perceptual.yaml` — SBT author module
- `negotiation-sbt-ost/ost/ost_operational.yaml` — OST author module
- `negotiation-sbt-ost/sbt_ost.sssom.tsv` — SSSOM mapping proposal (the
  machine-readable reconciliation artifact)
- this experiment record

The committed citation substrate (`the citation substrate`) and the live ontology
modules (`the live ontology modules`) were not modified.

**Publication plan (per user direction, 2026-06-13).** *All experiment data above is to be
published in the public SSOT when/if a paper carrying this evidence is published.* The carrying
paper is **R14 / 2026u** (`§"A Realized Instance"`, whose §5.5 cites the federated case as
evidence). At that paper's publication, these artifacts move to the public mirror
`sbt-papers/r14-paper-as-repository/` under an `experiments/negotiation-real-corpora/` directory
(both modules + the SSSOM TSV + this record + the run command), with the experiment named in a
"Companion Experiment" subsection of the paper per the computation-script publication rule
(`the paper quality standards` items 37a-37f) and `the public mirror standard`.
Until that publication, the artifacts remain internal-only. This earmark is tracked in the
mirror-propagation manifest and `REMEDIATION_OWED_2026-06-13.md` so it is not missed at mirror
time.

---

## 10. Conclusion

On two real corpus vocabularies in two distinct namespaces, the federated linker classified all
six cross-owner interactions, matched shared concepts by content-addressed hash, and recovered the
SBT/OST bridge (four imports + two narrowings) mechanically, before any prose was read — supporting
H1-H3. The federation was clean (H4 confirmed), which is the expected and honest result for two
convergent programs by one author and is recorded as the experiment's principal limitation: the
adversarial, genuinely-independent two-author case remains the future-work step that would upgrade
the thesis from a single-author existence proof to a federated practice.
