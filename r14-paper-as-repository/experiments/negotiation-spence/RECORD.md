# Experiment Record — Federated Ontology Negotiation Producing a Genuine Same-Key CONFLICT (SBT <-> Spence)

| Field | Value |
|---|---|
| **Experiment ID** | EXP-2026-06-14-NEG-SPENCE-SBT |
| **Date** | 2026-06-14 |
| **Operator** | Dmitry Zharnikov (with Claude Opus 4.8) |
| **Classification** | Computational / deterministic / logical — no stochastic component, no statistical inference; the outcome is a fixed function of the inputs and the tool. |
| **Instrument** | `tools/negotiate_modules.py` (federated multi-author generalization of the single-author linker `build_ontology.py`). Shared parser `build_ontology.Module` + `def_hash` + `_norm_ref`. |
| **Protocol** | `the negotiation protocol (paper §5.5)`; companion `the spine-first drafting protocol`. |
| **Companion experiments** | `negotiation-sbt-ost/RECORD.md` (EXP-2026-06-13-NEG-SBT-OST — clean federation, CROSS_IMPORT + CROSS_REFINE) and `NEGOTIATION_INDEPENDENT_AAKER_SBT_2026-06-14.md` (EXP-2026-06-14-NEG-AAKER-SBT — first adversarial class, DANGLING_IMPORT). This record is the third real-corpora run and produces the one class neither prior run did: a genuine same-key CONFLICT. |
| **Environment** | Python 3.12, `uv`. Substrate `the citation substrate` and the live ontology `the live ontology modules` present but neither read nor written by the run. |
| **Pre-registration** | Post-hoc record of a single confirmatory run. The hypotheses in §1 (including the headline CONFLICT prediction in H2) were the design intent fixed before execution; no run was discarded or re-specified after seeing results. |
| **Data availability** | All inputs and outputs are listed in §9 and earmarked for publication to the public mirror when/if the carrying paper (R14 / 2026u) is published (§9). |

---

## 1. Research question and hypotheses

**Research question.** The two prior real-corpora runs left exactly one protocol class unexercised on
real inputs. SBT/OST (EXP-2026-06-13) was a *clean* federation by one author (CROSS_IMPORT +
CROSS_REFINE, zero unresolved). SBT/Aaker (EXP-2026-06-14) produced the first genuine adversarial,
`--gate`-failing class — `DANGLING_IMPORT` — but, by design of SBT's qualified naming, produced **no**
same-key `CONFLICT`: SBT renamed away from every incumbent brand-theory surface form
(`perception-cloud` not "brand image"; `brand-conviction` not "brand attitude"), so no bare key
collided. The genuine same-key `CONFLICT` class — the case the protocol's worked fixture constructs
and the case `--gate` most pointedly fails on — had never arisen on real corpora. This experiment asks:

> When a **genuinely independent vocabulary from a different discipline** — Michael Spence's economic
> signaling theory (Spence 1973) — and SBT both legitimately **own the bare term `signal`** with
> genuinely **incompatible definitions**, does the federated linker produce a real same-key
> `CONFLICT`, classify it as *same label, divergent definition*, and propose a `skos:closeMatch`
> manual-curation reconciliation? And does an honest unowned economic primitive yield a real
> `DANGLING_IMPORT` alongside it?

"signal" is a true cross-disciplinary **homonym**: it is a central, real construct in *both* programs,
under exactly the same English word, with definitions that share no content. This is precisely the
condition for a genuine same-key conflict — the condition SBT's qualified naming *avoids* with
brand-theory incumbents (per EXP-2026-06-14-NEG-AAKER-SBT) but **cannot** avoid against a
different-discipline vocabulary that independently owns the bare word.

**Hypotheses (each with an explicit falsification criterion).**

- **H1 — Mechanizability.** The linker assigns every cross-owner interaction to exactly one protocol
  class (`AGREEMENT` / `CONFLICT` / `CROSS_REFINE` / `INCOMPATIBLE_REFINE` / `CROSS_IMPORT` /
  `DANGLING_IMPORT`) and terminates with a verdict. *Falsified if* any interaction is left
  unclassified or the tool errors on real modules.

- **H2 — Genuine same-key CONFLICT under cross-disciplinary homonymy (the headline).** Two independent
  literatures that each genuinely own the bare term `signal` with **different `def_hash`** produce a
  genuine `CONFLICT`, classified as *same label, divergent definition*, carrying a `skos:closeMatch`
  proposal at confidence .5 flagged `semapv:ManualMappingCuration`, and the federation is reported
  NOT clean (`--gate` exits nonzero). *Falsified if* (a) the two `signal` definitions hash equal (an
  `AGREEMENT`, which would mean the definitions are not genuinely different), or (b) the tool does not
  classify the overlap as a same-label `CONFLICT`, or (c) `--gate` exits 0.

- **H3 — Genuine DANGLING_IMPORT from an unowned economic primitive.** An honest import of a primitive
  the Spence model presupposes but neither author owns (`labor-market`) yields a real
  `DANGLING_IMPORT`. *Falsified if* the imported primitive resolves to an owned term or is not
  reported as a `DANGLING_IMPORT`.

Adjudication is in §4.

---

## 2. Materials

### 2.1 Author A — SBT signal-owner module (with integrity manifest)

`negotiation-spence/sbt/sbt_signal.yaml` (`paper_key: sbt_signal`) **owns four**
terms. The headline term is `signal`, defined in SBT's brand-signal sense — *the composite ray a brand
emits across the eight perceptual dimensions, decomposed per observer cohort and completed into a brand
conviction by each observer's spectral profile*. This is a central, real SBT construct (SBT.2). It also
owns three **context terms** — `cohort`, `observer-spectral-profile`, `brand-conviction` — copied
**verbatim** from `negotiation-sbt-ost/sbt/sbt_perceptual.yaml` (themselves verbatim from
the live SBT ontology `the live ontology module for the SBT corpus`), so the `signal` conflict sits in a faithful SBT
mini-corpus: the brand signal is decomposed per `cohort` and completed by the `observer-spectral-profile`
into a `brand-conviction`.

**Integrity manifest** (the deterministic-experiment analogue of a fixed random seed; re-running
`def_hash` over these definitions reproduces these exact values, and the three context terms equal the
live-graph values — the tamper-evidence anchor, recomputed and confirmed for this run):

| term_key | def_hash | provenance |
|---|---|---|
| `signal` (SBT sense) | `bc51684f10b6b0c8` | SBT brand-signal definition (this module) |
| `cohort` | `db90eb1a6fd873a0` | verbatim from live `2026a` (matches perceptual module) |
| `observer-spectral-profile` | `e9d29838a687c3aa` | verbatim from live `2026a` (matches perceptual module) |
| `brand-conviction` | `57c8fe303b5a5e8b` | verbatim from live `2026a` (matches perceptual module) |

*(The three context-term hashes were re-computed live for this record and reproduce the values in the
companion runs' manifests exactly, confirming they are the same content-addressed concepts the live SBT
graph owns.)*

### 2.2 Author B — Spence economic-signaling module (new; faithfully transcribed, attributed)

`negotiation-spence/spence/spence_signaling.yaml` (`paper_key: spence_real`)
**owns six** terms from Michael Spence's canonical job-market signaling model, each a **faithful
paraphrase** attributed by author/year/venue — **no DOI is asserted** (per the no-fabricated-DOI rule).
Source: **Spence, Michael (1973), "Job Market Signaling," *Quarterly Journal of Economics* 87(3):355-374.**

| term_key | label | faithful content |
|---|---|---|
| `signal` | signal | an observable, **alterable** attribute a sender invests in at a **cost** to convey otherwise-unobservable type under information asymmetry (education is the paradigm); informative only when its marginal cost is **negatively correlated** with quality (single-crossing / Spence-Mirrlees) |
| `index` | index | an observable but **unalterable** attribute (age, sex) that cannot be chosen to convey type |
| `signaling-cost` | signaling cost | the cost of acquiring a signal level, which must be negatively correlated with quality for the signal to be informative |
| `separating-equilibrium` | separating equilibrium | different types choose different signal levels; the signal **reveals** type |
| `pooling-equilibrium` | pooling equilibrium | all types choose the same signal level; the signal **conveys nothing** |
| `productive-capability` | productive capability | the sender's true, unobservable type (worker productivity) the receiver wants to infer |

**Spence-purity.** "Screening" (the receiver-side complement) is Stiglitz / Rothschild-Stiglitz (1976),
**not** Spence, and is deliberately **omitted** to keep the module Spence-pure. Every owned term is from
Spence (1973). Definitions are **transcribed by the SBT author from the published source, not authored
by Spence himself** (§7). No fabricated definitions or identifiers were introduced.

**The two `signal` definitions are genuinely different — the mechanical basis of the conflict.** SBT's
`signal` is a *composite perceptual ray* completed in an observer; Spence's `signal` is an *alterable,
costly observable attribute* conveying hidden type under information asymmetry. They share the English
word and nothing of their content. Mechanically:

| `signal`, by author | def_hash |
|---|---|
| SBT (Author A) | `bc51684f10b6b0c8` |
| Spence (Author B) | `5898a8c112c12936` |

The hashes **differ** — `bc51684f10b6b0c8` ≠ `5898a8c112c12936` — which is the content-addressed
trigger for `CONFLICT` rather than `AGREEMENT`. Both modules carry the label "signal", so the linker
reports the conflict as *same label, divergent definition*.

**Exercising the cross-owner classes honestly.**

- *CONFLICT (same-key):* `signal` is owned by both authors with different `def_hash` and identical
  label → a genuine same-label CONFLICT. Not manufactured — both literatures really do own the bare
  word "signal" as a central construct.
- *DANGLING_IMPORT:* the module `import`s one primitive — `labor-market` — that the Spence (1973) model
  genuinely **presupposes** as its setting (employers and workers interact within it under information
  asymmetry) but that neither author's ontology owns. This is an honest import and yields a real
  `DANGLING_IMPORT`.
- *No cross-import / cross-refine onto SBT keys:* Spence (1973) predates and is independent of SBT and
  imports/refines **zero** SBT-owned terms.

### 2.3 Instrument and isolation

`negotiate_modules.py` parses both authors' modules with the exact parser the single-author linker uses,
then classifies every cross-owner interaction (shared `term_key`s and explicit `imports`/`refines` only),
proposes a typed SKOS mapping + reconciliation operation per finding, and emits an SSSOM proposal. It is
read-only on everything except the one SSSOM file it is asked to write.

**Isolation.** Both module files live only under `negotiation-spence/`. Neither is
in `the live ontology directory ` nor named `ONTOLOGY.yaml`, so the live `build_ontology.discover_modules()`
(globs exactly `the live ontology modules` and `research/**/ONTOLOGY.yaml`) never discovers them. They are
loaded only via the explicit `--author-a` / `--author-b` paths. The committed substrate and live ontology
were neither read nor written.

---

## 3. Procedure

```
uv run python tools/negotiate_modules.py \
    --author-a negotiation-spence/sbt \
    --author-b negotiation-spence/spence \
    --sssom negotiation-spence/sbt_spence.sssom.tsv
```

The run was repeated with `--gate` appended to obtain the federated CI verdict (exit nonzero iff any
unresolved interaction remains).

**Determinism.** No random component, no sampling, no seed: `def_hash` is a pure function of definition
text and the classifier is a pure function of the two parsed module sets. Re-running the command on the
same inputs and tool reproduces byte-identical output. The integrity manifest (§2.1) and the two
differing `signal` hashes (§2.2) are the reproducibility anchors in lieu of a seed.

---

## 4. Results — the negotiation report (verbatim)

```
NEGOTIATION REPORT  sbt  <->  spence
================================================================

CONFLICT  (1)
  - signal [skos:closeMatch]: same label, divergent definition; sbt='The composite ray a brand emits across the eight perceptual dimensions (semiotic, narrative, ideological, experiential, social, economic, cultural, temporal), decomposed per observer cohort and completed into a brand conviction by each observer's spectral profile. The signal does not carry meaning in itself; it is collapsed into a conviction only in the observer, so the same emission yields different convictions across cohorts.' vs spence='An observable, ALTERABLE attribute that a sender can invest in at a COST in order to convey otherwise-unobservable type or quality to a receiver under information asymmetry. In the job market, education is the paradigm signal: a worker chooses how much to acquire, and its cost is what links the choice to underlying productive capability. A signal is informative only when its marginal cost is negatively correlated with the sender's quality (the single-crossing / Spence-Mirrlees condition), so that high-quality senders can profitably acquire more of it than low-quality senders.'
      -> reconcile: NAMESPACE + curate mapping; FORK the key if concepts differ

DANGLING_IMPORT  (1)
  - labor-market: spence imports 'labor-market' owned by neither author
      -> reconcile: BLOCK until some author owns the term or the import is dropped

----------------------------------------------------------------
2 interaction(s); 2 unresolved (CONFLICT / INCOMPATIBLE_REFINE / DANGLING_IMPORT).
Federation NOT clean: the authors must reconcile the unresolved interactions (namespace + curate mappings, supply narrowings, or assign owners) before the modules link across authors.
```

`--gate` exit code: **1** (two unresolved interactions: one `CONFLICT`, one `DANGLING_IMPORT`). Tool exit
code (report mode): **0**.

**Class tally:** `CONFLICT` = 1; `DANGLING_IMPORT` = 1; `AGREEMENT` = 0; `CROSS_IMPORT` = 0;
`CROSS_REFINE` = 0; `INCOMPATIBLE_REFINE` = 0. Total interactions = 2; unresolved = 2.

**Hypothesis adjudication.**

- **H1 — supported.** Both interactions were classified (`CONFLICT`, `DANGLING_IMPORT`) and the tool
  terminated with a verdict; report-mode exit 0, gate-mode exit 1. No interaction was left unclassified;
  the tool did not error on real modules.

- **H2 — supported in full (the headline).** The bare term `signal`, owned by both independent
  literatures with **different `def_hash`** (`bc51684f10b6b0c8` ≠ `5898a8c112c12936`), produced a genuine
  `CONFLICT`, classified exactly as *same label, divergent definition*, carrying `skos:closeMatch` at
  confidence .5 with `semapv:ManualMappingCuration`. The federation is correctly reported NOT clean and
  `--gate` exits 1. None of the three falsification conditions occurred: the definitions did not hash
  equal (no `AGREEMENT`), the overlap was classified as a same-label `CONFLICT`, and the gate did not exit
  0. This is the **first genuine same-key `CONFLICT` produced on real corpora** in the negotiation program.

- **H3 — supported.** The honest import of the unowned economic primitive `labor-market` produced a real
  `DANGLING_IMPORT` (BLOCK until owned or dropped). It did not resolve to any owned term.

---

## 5. The SSSOM mapping proposal

Written to `negotiation-spence/sbt_spence.sssom.tsv`. The `DANGLING_IMPORT` carries
no `predicate` (it is a missing-owner gap, not a term↔term mapping), so it produces no SSSOM row; the
single emitted row is the headline CONFLICT mapping. Rendered as a table (decimals shown in the tool's
machine `0.x` form, as written to the TSV):

| subject_id | predicate_id | object_id | mapping_justification | confidence | comment |
|---|---|---|---|---|---|
| sbt:signal | skos:closeMatch | spence:signal | semapv:ManualMappingCuration | 0.5 | CONFLICT |

**Interpreting the headline `closeMatch` row (the proposed reconciliation).** The tool refuses to assert
`exactMatch` on a definitional mismatch: it proposes `skos:closeMatch` at confidence .5, flagged
`semapv:ManualMappingCuration` — recording that a *human decision is still owed*. The reconciliation
operation the tool proposes is **NAMESPACE + curate mapping; FORK the key if concepts differ**. Concretely,
the two authors have two compatible resolutions:

1. **NAMESPACE + curate.** Keep the bare key for neither; qualify the colliding keys as `sbt:signal`
   (the brand-signal sense — a composite perceptual ray) versus `spence:signal` (the market-signal sense
   — an alterable, costly observable conveying hidden type), and retain the `closeMatch` cross-walk as the
   human-curated record that the two are *related homonyms*, not the same concept.
2. **FORK the key.** Because the concepts genuinely differ (they share no definitional content — only the
   English word), the cleaner resolution is to FORK to disambiguated keys: SBT's `signal` → **`brand-signal`**
   and Spence's `signal` → **`market-signal`**, leaving the bare `signal` owned by neither and the
   `closeMatch` mapping documenting the homonym for retrieval.

Either resolution keeps the machine layer free of false-agreement risk: no two authors silently assert
`exactMatch` on a key that means different things in different disciplines. The `closeMatch` at .5 is the
honest middle: the tool says "same word, related-enough to cross-walk, but a human must confirm whether to
namespace or fork" — it does not decide the semantic question for the authors.

---

## 6. Analysis by interaction class

**CONFLICT (1) — the genuine cross-disciplinary homonym.** This is the result neither prior real-corpora
run could produce. SBT/OST was clean by single-author design; SBT/Aaker produced no same-key CONFLICT
*because SBT's qualified naming was built to avoid bare-key collisions with brand-theory incumbents*. The
Spence case defeats that avoidance for a precise, honest reason: Spence (1973) is from a **different
discipline** (information economics), independently owns the bare word `signal` as a central construct,
and could not have been designed for SBT compatibility — so SBT's rename discipline, which works against
brand-theory incumbents, has no purchase. Two literatures arriving independently at the same English word
with incompatible meanings is exactly the homonym condition, and the linker surfaces it mechanically —
matching on the shared key, then splitting `AGREEMENT` from `CONFLICT` on the content-addressed `def_hash`.
The two hashes differ because the definitions share no content, and the tool reports *same label, divergent
definition* with a `closeMatch` curation proposal. This is the protocol's `CONFLICT` class doing exactly
what it is for: refusing false agreement and pushing a real semantic decision to an explicit, justified,
manually-curated layer.

**DANGLING_IMPORT (1) — the honest economic primitive.** The Spence (1973) model presupposes a
`labor-market` as its setting and derives signaling within it, but neither author's ontology owns that
primitive. The linker correctly surfaces this as a `--gate`-failing `DANGLING_IMPORT`: the federation is
not clean until some author introduces and owns `labor-market`, or Spence drops the import. This mirrors
the SBT/Aaker `brand`/`consumer` result (a different-discipline vocabulary presupposes base nouns the
perception-metrology ontology does not own) and confirms the class is robust across independent corpora.

**No AGREEMENT, CROSS_IMPORT, or CROSS_REFINE — honestly.** Spence and SBT share no other key, and Spence
imports/refines no SBT term (he predates and is independent of SBT). The only term-level overlap is the
`signal` homonym, and the only honest import is the economic primitive. Nothing was manufactured to inflate
the interaction count.

**Why this is the strongest independence case so far.** Spence (1973) is Nobel-recognized (2001 Memorial
Prize), predates SBT by decades, and is from information economics rather than brand theory. It could not
have been designed for SBT compatibility — yet it shares the bare term `signal`, which is exactly the
condition for a genuine same-key conflict that SBT's qualified naming *avoids* with brand-theory incumbents
(per EXP-2026-06-14-NEG-AAKER-SBT) but *cannot* avoid against an independent different-discipline owner of
the bare word. The Aaker run showed the rename discipline converts would-be conflicts into cross-key
cross-walks *within* brand theory; the Spence run shows what happens when the colliding owner comes from
*outside* the discipline SBT renamed around — a genuine, unavoidable, mechanically-surfaced CONFLICT.

---

## 7. Threats to validity and limitations

**The independence ladder — where this rung sits.** Spence (1973) is the **most independent** vocabulary
negotiated against SBT so far: a different author, decades earlier, in a different discipline, with a
construct (`signal`) that genuinely collides on the bare key. It delivers the genuine same-key `CONFLICT`
the two prior runs structurally could not. **But the load-bearing caveat is unchanged from the Aaker run:**

1. **Still transcribed, not authored by Spence.** The Spence module's definitions are faithful paraphrases
   *the SBT author wrote* from Spence (1973) — not modules Spence authored himself in this schema. A
   transcriber's framing choices (which primitive to import, how to word a definition) are still the SBT
   author's. The independence is in the *vocabulary's provenance*, not yet in the *authoring act*.

2. **The conflict is resolved here only as a tool-proposed curation, not negotiated with a living Spence.**
   The tool proposes `closeMatch` @ .5 / NAMESPACE-or-FORK; it does not, and cannot, decide whether to
   namespace or fork, nor does it write the reconciled state back into either module. That decision is an
   authored edit. The genuine endpoint — two living authors resolving the `signal` homonym in dialogue,
   agreeing on `brand-signal` vs `market-signal` and curating the cross-walk together — is not reached here.

**On the CONFLICT being designed-in.** Unlike the SBT/Aaker CONFLICT *null* (which was a discovered
property of SBT's naming), this CONFLICT was *deliberately set up* by choosing a term (`signal`) both
literatures really own. That is honest — both ownerships are faithful to the real work, and the homonym is
real, not contrived — but the experiment demonstrates that *when* a genuine same-key homonym exists across
independent owners, the tool surfaces and classifies it correctly; it does not demonstrate that such
homonyms arise unbidden. The contribution is the mechanism's correctness on a real homonym, not a survey of
how often homonyms occur.

**Internal validity — controlled.** Content-addressed identity (the §2.1 manifest, recomputed and
confirmed; the two differing `signal` hashes in §2.2) rules out lexical artifacts: the CONFLICT fires
because the definitions genuinely differ by hash, and the three SBT context terms match the live graph by
hash. Isolation (§2.3) rules out contamination of or by the live graph. Determinism (§3) rules out
run-to-run variation.

**What the final rung still requires (unchanged in spirit).** A **living, genuinely independent co-author**
who authors *their own* modules in this schema and resolves a genuine same-key `CONFLICT` against SBT in
dialogue — namespacing or forking the colliding key (`brand-signal` vs `market-signal`) and curating the
SSSOM cross-walk together, then writing the reconciled state back. This experiment moves the evidence from
"genuine `DANGLING_IMPORT` against an independent incumbent" (Aaker) to "genuine same-key `CONFLICT` against
an independent different-discipline owner of the same word" (Spence) — but the authoring act and the
conflict's resolution remain single-sourced.

**Net contribution.** The first genuine same-key `CONFLICT` on real corpora, completing the protocol's
adversarial coverage; demonstration that SBT's qualified naming avoids collisions *within* brand theory but
cannot avoid a cross-disciplinary homonym, which the tool then surfaces and proposes a `closeMatch` +
NAMESPACE/FORK reconciliation for. It does not, and should not be read to, close the
*living-independent-co-author* caveat.

---

## 8. Reproducibility statement

Anyone with the repository and Python 3.12 can reproduce this record exactly: (i) the two input modules
`negotiation-spence/sbt/sbt_signal.yaml` and
`negotiation-spence/spence/spence_signaling.yaml`; (ii) the run command in §3; (iii)
byte-identical report and SSSOM output, since the pipeline is deterministic; (iv) the `--gate` exit code 1;
(v) the §2.1 / §2.2 integrity manifests — recomputable by hashing each definition with
`build_ontology.def_hash`, with the two `signal` hashes (`bc51684f10b6b0c8` SBT, `5898a8c112c12936` Spence)
confirming they differ and the three context-term hashes confirming they equal the live SBT graph
(`the live ontology module for the SBT corpus`). No seed, dataset download, network call, or API key is required.

---

## 9. Data availability and publication plan

**Internal artifacts (canonical SSOT, present now):**

- `negotiation-spence/sbt/sbt_signal.yaml` — SBT signal-owner module (new)
- `negotiation-spence/spence/spence_signaling.yaml` — Spence economic-signaling module (new)
- `negotiation-spence/sbt_spence.sssom.tsv` — tool-emitted SSSOM (the headline CONFLICT closeMatch row)
- this experiment record

The committed citation substrate (`the citation substrate`) and the live ontology modules
(`the live ontology modules`) were not modified.

**Publication plan (per user direction).** *All experiment data above is to be published in the public
SSOT when/if a paper carrying this evidence is published.* The carrying paper is **R14 / 2026u**
("negotiate a paper before you read it"). At that paper's publication these artifacts move to the public
mirror `sbt-papers/r14-paper-as-repository/` under an `experiments/negotiation-independent-spence/`
directory (both modules + the SSSOM TSV + this record + the run command), alongside the companion SBT/OST
and SBT/Aaker experiments, with the experiment named in a "Companion Experiment" subsection per the
computation-script publication rule (`the paper quality standards` items 37a-37f) and
`the public mirror standard`. Until that publication the artifacts remain internal-only. This
earmark is tracked alongside the SBT/OST and SBT/Aaker earmarks in the mirror-propagation manifest.

---

## 10. Conclusion — and the synthesis across all three real-corpora runs

Against Michael Spence's economic signaling theory (Spence 1973, *QJE* 87(3):355-374) — a genuinely
independent, Nobel-recognized vocabulary from a different discipline that independently owns the bare term
`signal` — the federated linker classified all interactions and terminated (H1), and produced the **first
genuine same-key `CONFLICT` on real corpora** (H2): the bare key `signal`, owned by both authors with
different `def_hash` (`bc51684f10b6b0c8` ≠ `5898a8c112c12936`), classified as *same label, divergent
definition* with a `skos:closeMatch` curation proposal at .5 and a NAMESPACE-or-FORK reconciliation, the
federation NOT clean (`--gate` exit 1). An honest unowned economic primitive (`labor-market`) yielded a
real `DANGLING_IMPORT` alongside it (H3).

**This completes the adversarial coverage on REAL corpora.** The three real-corpora runs now jointly
exercise the full protocol: SBT/OST gave the clean federation (CROSS_IMPORT + CROSS_REFINE, zero
unresolved); Aaker gave the genuine `DANGLING_IMPORT` adversarial class; and Spence now gives the genuine
same-key `CONFLICT` (+ a second `DANGLING_IMPORT`) — the one class neither prior run produced. The Spence
CONFLICT is the strongest independence case so far precisely because Spence predates SBT by decades, comes
from a different discipline, and could not have been designed for SBT compatibility, yet shares the bare
word `signal` — the exact condition for a genuine same-key conflict that SBT's qualified naming avoids with
brand-theory incumbents but cannot avoid against an outside-discipline owner of the same word. The honest
remaining limitation is unchanged: the Spence module is still transcribed by the SBT author, and the
conflict is resolved here only as a tool-proposed curation, not negotiated with a living Spence; the final
rung — a living, independent co-author authoring their own modules and resolving a genuine same-key
conflict in dialogue — remains future work.
