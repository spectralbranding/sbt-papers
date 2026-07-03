# Experiment Record — Federated Ontology Negotiation Against an Independent Incumbent Vocabulary (SBT <-> Aaker)

| Field | Value |
|---|---|
| **Experiment ID** | EXP-2026-06-14-NEG-AAKER-SBT |
| **Date** | 2026-06-14 |
| **Operator** | Dmitry Zharnikov (with Claude Opus 4.8) |
| **Classification** | Computational / deterministic / logical — no stochastic component, no statistical inference; the outcome is a fixed function of the inputs and the tool. |
| **Instrument** | `tools/negotiate_modules.py` (federated multi-author generalization of the single-author linker `build_ontology.py`). Shared parser `build_ontology.Module` + `def_hash` + `_norm_ref`. |
| **Protocol** | `the negotiation protocol (paper §5.5)`; companion `the spine-first drafting protocol`. |
| **Companion experiment** | `negotiation-sbt-ost/RECORD.md` (EXP-2026-06-13-NEG-SBT-OST) — the same instrument on the SBT/OST pair. This record is the next rung up the independence ladder. |
| **Environment** | Python 3.12.13, `uv`. Substrate `the citation substrate` and the live ontology `the live ontology modules` present but neither read nor written by the run. |
| **Pre-registration** | Post-hoc record of a single confirmatory run. The hypotheses in §1 (including the directional prediction in H2) were the design intent fixed before execution; no run was discarded or re-specified after seeing results. |
| **Data availability** | All inputs and outputs are listed in §9 and earmarked for publication to the public mirror when/if the carrying paper (R14 / 2026u) is published (§9). |

---

## 1. Research question and hypotheses

**Research question.** The SBT/OST companion run (EXP-2026-06-13) was honest about its central
limitation: SBT and OST are two programs by **one author**, intentionally built to converge, so the
federation was clean *by design* and could not exhibit the adversarial interaction classes
(`CONFLICT` / `DANGLING_IMPORT`) that are the harder half of the protocol. This experiment asks the
sharper, honest question:

> When a **genuinely independent incumbent** brand-theory vocabulary — David A. Aaker's canonical
> brand-equity / brand-identity / brand-personality model, authored decades before SBT and **not**
> designed to be compatible with it — is negotiated against SBT, does it produce *genuine
> adversarial interactions* (`CONFLICT` / `DANGLING_IMPORT`)? Or does SBT's deliberately-qualified
> naming (`perception-cloud` not "brand image"; `brand-conviction` not "brand attitude";
> `positioning-capacity` not "positioning"; `cohort` not "segment") *avoid* same-key collisions
> with the incumbent terms?

This is the empirical test of whether Aaker can serve as the *"genuinely independent second author"*
the protocol's final rung requires.

**Hypotheses (each with an explicit falsification criterion).**

- **H1 — Mechanizability.** The linker assigns every cross-owner interaction to exactly one protocol
  class (`AGREEMENT` / `CONFLICT` / `CROSS_REFINE` / `INCOMPATIBLE_REFINE` / `CROSS_IMPORT` /
  `DANGLING_IMPORT`) and terminates with a verdict. *Falsified if* any interaction is left
  unclassified or the tool errors on real modules.

- **H2 — Adversarial-class emergence under genuine independence (the real question).** A
  faithfully-transcribed *independent incumbent* vocabulary produces genuine adversarial classes.
  *Directional prediction, fixed before the run:* a real `DANGLING_IMPORT` arises (the incumbent
  presupposes base primitives — `brand`, `consumer` — that neither author's ontology owns), **but
  NO genuine same-key `CONFLICT`**, because SBT's qualified naming was *designed* to avoid bare-key
  collisions with incumbent terms. *Falsified if* (a) no adversarial class arises at all (a fully
  clean federation, as in the SBT/OST run), or (b) a same-key `CONFLICT` is found — which would
  *refute* the "qualified naming avoids collisions" claim and would be reported as such.

- **H3 — Cross-key invisibility (the scope boundary).** The genuine SBT<->incumbent relationships
  are *cross-key semantic* (e.g. `perception-cloud` vs `brand-image`; `brand-conviction` vs "brand
  attitude") and are therefore **invisible** to the key-based linker, which detects interactions
  only on shared `term_key`s and explicit `imports`/`refines`. Recovering them requires a
  hand-authored curated SSSOM, not the tool. *Falsified if* the tool surfaces any of the documented
  rename-boundary relationships on its own (it would have to detect cross-key synonymy, which its
  algorithm does not attempt).

**Adjudication is in §4 (H1, H2) and §6 (H3).**

---

## 2. Materials

### 2.1 Author A — SBT perceptual module (reused verbatim from the companion run; with integrity manifest)

`negotiation-sbt-ost/sbt/sbt_perceptual.yaml` (`paper_key: sbt_real_2026a`),
**reused unchanged** as author A. It owns seven shared SBT perceptual terms, each definition copied
verbatim from the live SBT ontology (`the live single-author ontology modules`) so that each
term's content-addressed `def_hash` (sha256 of the trimmed definition, truncated to 16 hex chars)
matches the live SBT graph.

**Integrity manifest** (the deterministic-experiment analogue of a fixed random seed; re-running
`def_hash` over these definitions reproduces these exact values and they equal the live-graph
values — the tamper-evidence anchor, recomputed and confirmed for this run):

| term_key | def_hash | live owner |
|---|---|---|
| `cohort` | `db90eb1a6fd873a0` | 2026a |
| `perception-cloud` | `b8bfd48074e97506` | 2026a |
| `spectral-dimensions` | `751200eee587a9c7` | 2026a |
| `brand-conviction` | `57c8fe303b5a5e8b` | 2026a |
| `observer-spectral-profile` | `e9d29838a687c3aa` | 2026a |
| `coherence-type` | `41b7ba951cd62cb5` | 2026s |
| `re-collapse` | `19323b6c7c660bfb` | 2026a |

*(`cohort` and `perception-cloud` were re-hashed live for this record and reproduce
`db90eb1a6fd873a0` / `b8bfd48074e97506` exactly.)*

The **broader** SBT vocabulary, against which the Aaker keys were checked for collisions, is the
full live ontology term set (`the live ontology modules`, ~190 owned keys). Its defining feature for
this experiment: SBT introduces brand-domain terms under **deliberately-qualified keys** —
`perception-cloud`, `brand-conviction`, `positioning-capacity`, `spectral-dimensions`,
`coherence-type`, `signal-coherence`, `spectral-identity` — never the bare incumbent forms
("brand image", "brand attitude", "positioning", "brand personality"). This qualification is the
documented rename boundary in `CLAUDE.md` ("cohort" not "segment"; "perception cloud" not "brand
image"; "brand conviction" not "brand attitude"; "re-collapse" not "rebranding").

### 2.2 Author B — Aaker incumbent module (new; faithfully transcribed, attributed per term)

`negotiation-aaker/aaker/aaker_brand_equity.yaml` (`paper_key: aaker_real`)
**owns nine** incumbent brand-theory terms, each a **faithful paraphrase** of David A. Aaker's real
published work with the source attributed per term in the `note`:

| term_key | label | attributed source |
|---|---|---|
| `brand-equity` | brand equity | Aaker (1991) *Managing Brand Equity*, ch. 1 — the five asset categories |
| `brand-identity` | brand identity | Aaker (1996) *Building Strong Brands*, ch. 2 — the four perspectives |
| `brand-image` | brand image | Aaker (1996) — image (perceived) vs identity (aspirational) |
| `brand-personality` | brand personality | J. Aaker (1997) *Dimensions of Brand Personality*, JMR 34(3):347-356 — the five dimensions |
| `brand-awareness` | brand awareness | Aaker (1991), ch. 2 — recognition → recall → top-of-mind |
| `brand-loyalty` | brand loyalty | Aaker (1991), ch. 3 — the central equity asset |
| `perceived-quality` | perceived quality | Aaker (1991), ch. 4 — perceived (not objective) quality |
| `brand-association` | brand association | Aaker (1991), ch. 5 — the organized association set IS the image |
| `positioning` | brand position | Aaker (1996), ch. 6 — the actively-communicated slice of the identity |

**Faithfulness note.** Definitions are paraphrases drawn from the SBT author's knowledge of Aaker's
canonical model — the brand-equity five asset categories (brand loyalty, brand awareness, perceived
quality, brand associations, other proprietary assets); the brand-identity four perspectives
(brand-as-product / -organization / -person / -symbol); the five brand-personality dimensions
(sincerity, excitement, competence, sophistication, ruggedness). They are **transcribed by the SBT
author from published sources, not authored by Aaker himself** (§7). No DOI is asserted for the two
books (they are monographs); the JMR article's identification is given by journal, volume, issue,
and page range as printed. No fabricated definitions or identifiers were introduced.

**Exercising the cross-owner classes honestly.**

- *CONFLICT (same-key):* checked against both the seven author-A keys and the broader ~190-key live
  SBT set. **None of the nine bare Aaker keys** (`brand-equity`, `brand-identity`, `brand-image`,
  `brand-personality`, `brand-awareness`, `brand-loyalty`, `perceived-quality`,
  `brand-association`, `positioning`) exactly matches any SBT-owned key. The closest near-misses —
  SBT owns `positioning-capacity` (not `positioning`), `perception-cloud` (not `brand-image`),
  `brand-conviction` (not the bare `brand-attitude`) — are *qualified away*. So **no genuine
  same-key CONFLICT exists, and none was manufactured.** The module lets the run report its absence.
- *DANGLING_IMPORT:* the module `import`s two primitives — `consumer` and `brand` — that the
  incumbent vocabulary genuinely **presupposes** but that neither author's ontology owns. Incumbent
  managerial brand theory assumes these base concepts as given rather than deriving them. This is an
  honest import and yields a real `DANGLING_IMPORT`.
- *No cross-import / cross-refine onto SBT keys:* Aaker predates and is independent of SBT and would
  not depend on SBT's keys, so the module imports/refines **zero** SBT-owned terms.

### 2.3 Instrument and isolation

`negotiate_modules.py` parses both authors' modules with the exact parser the single-author linker
uses, then classifies every cross-owner interaction (shared `term_key`s and explicit
`imports`/`refines` only — it does **not** attempt cross-key semantic synonymy), proposes a typed
SKOS mapping + reconciliation operation per finding, and emits an SSSOM proposal. It is read-only on
everything except the one SSSOM file it is asked to write.

**Isolation.** Both module files live only under `negotiation-sbt-ost/` (SBT, reused)
and `negotiation-aaker/` (Aaker, new). Neither is in `the live ontology directory ` nor
named `ONTOLOGY.yaml`, so the live `build_ontology.discover_modules()` (globs exactly
`the live ontology modules` and `research/**/ONTOLOGY.yaml`) never discovers them. They are loaded
only via the explicit `--author-a` / `--author-b` paths. The committed substrate and live ontology
were neither read nor written.

---

## 3. Procedure

```
uv run python tools/negotiate_modules.py \
    --author-a negotiation-sbt-ost/sbt \
    --author-b negotiation-aaker/aaker \
    --sssom negotiation-aaker/sbt_aaker.sssom.tsv
```

The run was repeated with `--gate` appended to obtain the federated CI verdict (exit nonzero iff any
unresolved interaction remains).

**Determinism.** No random component, no sampling, no seed: `def_hash` is a pure function of
definition text and the classifier is a pure function of the two parsed module sets. Re-running the
command on the same inputs and tool reproduces byte-identical output. The integrity manifest (§2.1)
is the reproducibility anchor in lieu of a seed.

---

## 4. Results — the negotiation report (verbatim)

```
NEGOTIATION REPORT  sbt  <->  aaker
================================================================

DANGLING_IMPORT  (2)
  - brand: aaker imports 'brand' owned by neither author
      -> reconcile: BLOCK until some author owns the term or the import is dropped
  - consumer: aaker imports 'consumer' owned by neither author
      -> reconcile: BLOCK until some author owns the term or the import is dropped

----------------------------------------------------------------
2 interaction(s); 2 unresolved (CONFLICT / INCOMPATIBLE_REFINE / DANGLING_IMPORT).
Federation NOT clean: the authors must reconcile the unresolved interactions (namespace + curate mappings, supply narrowings, or assign owners) before the modules link across authors.
```

`--gate` exit code: **1** (two unresolved `DANGLING_IMPORT` interactions). Tool exit code (report
mode): **0**.

**Class tally:** `DANGLING_IMPORT` = 2; `CONFLICT` = 0; `AGREEMENT` = 0; `CROSS_IMPORT` = 0;
`CROSS_REFINE` = 0; `INCOMPATIBLE_REFINE` = 0. Total interactions = 2; unresolved = 2.

**Hypothesis adjudication (H1, H2).**

- **H1 — supported.** Both interactions were classified (`DANGLING_IMPORT`) and the tool terminated
  with a verdict; report-mode exit 0, gate-mode exit 1. No interaction was left unclassified; the
  tool did not error on real modules.

- **H2 — supported in full, in both of its directional parts.**
  - *Adversarial class DID arise:* two genuine `DANGLING_IMPORT`s (`brand`, `consumer`) — exactly
    the prediction that an independent incumbent presupposes base primitives no theory-ontology
    owns. This is the **first genuine adversarial (`--gate`-failing) interaction class produced on
    real corpora** in the negotiation program; the SBT/OST companion run produced none. The
    federation is correctly reported NOT clean.
  - *No same-key CONFLICT arose:* zero `CONFLICT`. The nine bare incumbent keys did not collide with
    any SBT-owned key, because SBT's brand-domain terms are qualified (`perception-cloud`,
    `brand-conviction`, `positioning-capacity`, ...) precisely to avoid such collisions. The
    "qualified naming avoids bare-key collisions" claim is **corroborated, not refuted**: the
    falsification condition for H2 (a found `CONFLICT`) did not occur. This is an honest null on the
    CONFLICT class — and a meaningful one, because it is *evidence about SBT's naming discipline*,
    not a failure of the experiment.

---

## 5. The SSSOM mapping proposals

### 5.1 Tool-emitted SSSOM (mechanical) — `negotiation-aaker/sbt_aaker.sssom.tsv`

The tool wrote a **header-only** SSSOM:

```
subject_id	predicate_id	object_id	mapping_justification	confidence	comment
```

This is itself a finding, not an empty result. `render_sssom()` emits a row only for interaction
classes that yield a term<->term mapping (`AGREEMENT`, `CONFLICT`, `CROSS_REFINE`, `CROSS_IMPORT`);
`DANGLING_IMPORT` carries no `predicate` (it is a missing-owner gap, not a mapping), so it produces
no row. With the only interactions being two `DANGLING_IMPORT`s, the mechanical SSSOM is correctly
empty of mappings: **the key-based linker found a dependency gap but no term<->term correspondence
to assert.** The genuine SBT<->Aaker correspondences are cross-key and live in §5.2.

### 5.2 Hand-authored curated cross-key SSSOM (the artifact the tool cannot derive) — `negotiation-aaker/sbt_aaker_crosskey_curated.sssom.tsv`

Because the tool maps only same-key / import / refine, the *real* SBT<->Aaker relationships — which
are cross-**key** semantic — are invisible to it (§6, H3). This curated SSSOM is the SBT<->incumbent
**Rosetta stone**, hand-authored from the documented rename boundaries. Every row is
`semapv:ManualMappingCuration` at moderate confidence (these are human-curated judgments, not
mechanical matches):

| subject_id | predicate_id | object_id | confidence | rename boundary |
|---|---|---|---|---|
| sbt:perception-cloud | skos:closeMatch | aaker:brand-image | .7 | "perception cloud" not "brand image"; SBT distributional, Aaker an aggregate association set |
| sbt:brand-conviction | skos:closeMatch | aaker:brand-attitude | .6 | "brand conviction" not "brand attitude"; observer-relative vs dispositional (Aaker-era term) |
| sbt:cohort | skos:relatedMatch | aaker:market-segment | .5 | "cohort" not "segment"; perceptual vs demographic basis |
| sbt:re-collapse | skos:closeMatch | aaker:rebranding | .6 | "re-collapse" not "rebranding"; mechanism vs practice |
| sbt:coherence-type | skos:relatedMatch | aaker:brand-consistency | .5 | structural geometry type vs scalar managerial virtue |
| sbt:spectral-dimensions | skos:relatedMatch | aaker:brand-personality | .5 | different dimensional models (8 perceptual channels vs 5 human-trait dimensions) |

Three object keys (`aaker:brand-attitude`, `aaker:market-segment`, `aaker:brand-consistency`,
`aaker:rebranding`) are **incumbent-tradition terms**, not keys owned in the Aaker module — they are
the Aaker-era surface forms SBT renamed away from, recorded here as cross-walk targets. Only
`aaker:brand-image`, `aaker:brand-personality` are owned in the module. Confidence is moderate
throughout (.5–.7): these are deliberate human judgments about partial semantic overlap, not
mechanical lexical matches (which the tool reserves `1.0`/`.95` for). The single `skos:closeMatch`
at the highest confidence (.7) is `perception-cloud` ↔ `brand-image`, the cleanest of the
rename-boundary correspondences (same receiver-side referent, differing on distributional vs
aggregate modeling). `spectral-dimensions` ↔ `brand-personality` is the one **owned-key**
cross-walk and is deliberately only `relatedMatch` (.5): both are dimensional models, but with
different counts, axes, and referents — they do not align term-for-term.

---

## 6. Analysis by interaction class

**DANGLING_IMPORT (2) — the genuine adversarial result.** The incumbent vocabulary presupposes
`brand` and `consumer` as primitives and derives its nine terms on top of them, but neither author's
ontology *owns* those primitives. The linker correctly surfaces this as two `--gate`-failing
`DANGLING_IMPORT`s: the federation is not clean until some author introduces and owns `brand` and
`consumer`, or Aaker drops the imports. This is the substantive difference from the SBT/OST run,
which had zero unresolved interactions. Here the independence is real enough that the *foundational
grounding gap* between an incumbent managerial vocabulary and a perception-metrology vocabulary
shows up mechanically: the two programs do not even share an owner for the base nouns "brand" and
"consumer". This is the protocol's `DANGLING_IMPORT` doing exactly what it is for.

**CONFLICT — honestly, none.** The pre-run worry was that a bare incumbent key (`brand-image`,
`positioning`, the Aaker-era `brand-attitude`) might collide same-key with an SBT key and divergent
definition, producing a genuine `CONFLICT`. It does not, and the reason is the central finding:
**SBT renamed at exactly these boundaries.** SBT owns `perception-cloud` (not `brand-image`),
`brand-conviction` (not `brand-attitude`), `positioning-capacity` (not `positioning`), `cohort`
(not `segment`). The qualified keys mean the key-based linker sees *no shared key* to conflict on.
Manufacturing a `CONFLICT` — e.g. by renaming an Aaker key to a bare SBT-adjacent form to force a
collision — would have been a fabricated incompatibility and is explicitly *not* done. The honest
classification of the SBT<->Aaker term relationships is **cross-key**, captured in §5.2, not
same-key `CONFLICT`.

**Why the rename discipline produces this exact signature.** The result is a clean demonstration of
a *designed* property of SBT's terminology: by qualifying every brand-domain term away from its
incumbent surface form, SBT guarantees that an incumbent vocabulary negotiated against it produces
no bare-key collisions — only (a) the foundational `DANGLING_IMPORT` where the two programs fail to
share base primitives, and (b) cross-key correspondences that require curated mapping. The naming
discipline converts what *would* be same-key `CONFLICT`s (under naive shared naming) into
human-curated `closeMatch`/`relatedMatch` cross-walks. That is a feature: it keeps the machine layer
free of false-agreement risk (no two authors silently asserting `exactMatch` on a key that means
different things) and pushes the genuine semantic reconciliation to an explicit, justified,
manually-curated layer.

**H3 — supported.** The tool surfaced *none* of the six §5.2 rename-boundary correspondences on its
own; it cannot, because its algorithm keys on shared `term_key`s and explicit `imports`/`refines`,
not on latent cross-key synonymy. The six genuine relationships had to be hand-authored. This both
confirms H3 and delineates the **scope boundary** of the key-based linker (§7): it surfaces
key-collisions and explicit dependency edges, not semantic synonymy across differing keys. The
embedding-assist layer the modular-architecture design anticipates
(`SPINE_FIRST_DRAFTING_PROTOCOL.md`) is what would propose §5.2's mappings as candidates for a human
to confirm; absent it, the curated SSSOM is authored directly.

---

## 7. Threats to validity and limitations

**The independence ladder — where this rung sits (the central framing).** This incumbent
vocabulary is **more independent** than the SBT/OST pair: it was authored by a different person
(David A. Aaker), decades earlier, and was **not** built to be compatible with SBT. So it is a
genuine step up the evidence ladder from the single-author SBT/OST run, and it delivers what that
run structurally could not — a real `--gate`-failing adversarial class (`DANGLING_IMPORT`).
**But two caveats keep it short of the final rung:**

1. **Still transcribed, not authored by Aaker.** The Aaker module's definitions are faithful
   paraphrases *the SBT author wrote* from Aaker's published sources — not modules Aaker authored
   himself in this schema. A transcriber's framing choices (which primitives to import, how to word
   a definition) are still the SBT author's. The independence is in the *vocabulary's provenance*,
   not yet in the *authoring act*.

2. **The experiment reveals the key-based linker's scope boundary, not a complete reconciliation.**
   The tool surfaces (a) key-collisions and (b) explicit import/refine dependencies. It does **not**
   detect latent cross-key synonymy — the very relationships (§5.2) that constitute the real
   SBT<->incumbent correspondence. Those needed the embedding-assist layer the modular-architecture
   design anticipates, or, as here, direct human curation. So the mechanical layer's verdict
   ("federation not clean: own `brand`/`consumer` or drop the imports") is *correct but partial*: it
   says nothing about whether `perception-cloud` and `brand-image` are the same concept, because
   that question is outside its key-based reach.

**On the CONFLICT null.** The absence of a same-key `CONFLICT` is a real finding about SBT's naming
discipline, but it is *contingent on that discipline*. A different theory without SBT's rename
boundaries (one that did own a bare `brand-image` or `positioning` key) **would** produce a genuine
`CONFLICT` against Aaker. The null here is "SBT's qualified naming avoids the collision," not "no
incumbent vocabulary can ever conflict with a perception vocabulary." We do not over-generalize it.

**Internal validity — controlled.** Content-addressed identity (the §2.1 manifest, recomputed and
confirmed) rules out lexical-key artifacts on the SBT side. Isolation (§2.3) rules out contamination
of or by the live graph. Determinism (§3) rules out run-to-run variation. The CONFLICT check was run
against the **broader ~190-key live SBT set**, not only the seven author-A keys, so the "no
collision" finding is not an artifact of a small author-A vocabulary.

**What the final rung still requires (unchanged in spirit from the companion run).** A **living,
genuinely independent co-author** who authors *their own* modules in this schema — not a vocabulary
transcribed by the SBT author — and whose modules, negotiated against SBT, are reconciled live by
both parties (namespacing + curated SSSOM + authored lock / fork / rebase / merge), including, ideally,
a genuine same-key `CONFLICT` that the two authors resolve in dialogue. This experiment moves the
evidence from "clean federation between one author's two convergent programs" (SBT/OST) to "genuine
adversarial `DANGLING_IMPORT` against an independent incumbent vocabulary, with the cross-key
reconciliation made explicit" — but the authoring act remains single-sourced.

**Net contribution.** First genuine `--gate`-failing adversarial class on real corpora; empirical
confirmation that SBT's qualified naming converts would-be same-key `CONFLICT`s into curated cross-key
mappings; and an explicit delineation of the key-based linker's scope boundary (it needs the
embedding-assist or human-curation layer for cross-key synonymy). It does not, and should not be read
to, close the *living-independent-co-author* caveat.

---

## 8. Reproducibility statement

Anyone with the repository and Python 3.12.13 can reproduce this record exactly: (i) the SBT input
module `negotiation-sbt-ost/sbt/sbt_perceptual.yaml` (reused) and the Aaker input
module `negotiation-aaker/aaker/aaker_brand_equity.yaml`; (ii) the run command
in §3; (iii) byte-identical report and (header-only) tool SSSOM, since the pipeline is
deterministic; (iv) the `--gate` exit code 1; (v) the §2.1 integrity manifest, recomputable by
hashing each SBT definition and checkable against `the live single-author ontology modules`. The
curated cross-key SSSOM (§5.2) is a hand-authored artifact, not a tool output, and is reproduced by
reading it; it carries `semapv:ManualMappingCuration` on every row precisely to mark it as authored,
not derived. No seed, dataset download, network call, or API key is required.

---

## 9. Data availability and publication plan

**Internal artifacts (canonical SSOT, present now):**

- `negotiation-aaker/aaker/aaker_brand_equity.yaml` — Aaker incumbent author module (new)
- `negotiation-sbt-ost/sbt/sbt_perceptual.yaml` — SBT author module (reused from EXP-2026-06-13)
- `negotiation-aaker/sbt_aaker.sssom.tsv` — tool-emitted SSSOM (header-only; the mechanical result)
- `negotiation-aaker/sbt_aaker_crosskey_curated.sssom.tsv` — hand-authored cross-key Rosetta-stone SSSOM
- this experiment record

The committed citation substrate (`the citation substrate`) and the live ontology modules
(`the live ontology modules`) were not modified.

**Publication plan (per user direction).** *All experiment data above is to be published in the
public SSOT when/if a paper carrying this evidence is published.* The carrying paper is **R14 /
2026u** ("negotiate a paper before you read it"). At that paper's publication these artifacts move to
the public mirror `sbt-papers/r14-paper-as-repository/` under an
`experiments/negotiation-independent-aaker/` directory (the Aaker module + both SSSOMs + this record
+ the run command), alongside the companion SBT/OST experiment, with the experiment named in a
"Companion Experiment" subsection per the computation-script publication rule
(`the paper quality standards` items 37a-37f) and `the public mirror standard`. Until
that publication the artifacts remain internal-only. This earmark is tracked alongside the SBT/OST
earmark in the mirror-propagation manifest.

---

## 10. Conclusion

Against a genuinely independent incumbent vocabulary — David A. Aaker's canonical brand-equity /
brand-identity / brand-personality model, faithfully transcribed and attributed per term — the
federated linker classified all interactions and terminated (H1), and produced the **first genuine
`--gate`-failing adversarial class on real corpora**: two `DANGLING_IMPORT`s (`brand`, `consumer`),
the foundational primitives the incumbent presupposes but neither ontology owns (`--gate` exit 1).
Crucially, **no genuine same-key `CONFLICT` arose** — corroborating, not refuting, the prediction
that SBT's deliberately-qualified naming (`perception-cloud` not "brand image"; `brand-conviction`
not "brand attitude"; `positioning-capacity` not "positioning") avoids bare-key collisions with
incumbent terms (H2). The real SBT<->incumbent relationships proved to be **cross-key semantic** and
therefore invisible to the key-based linker (H3); they were captured in a hand-authored curated
SSSOM (§5.2), the SBT<->incumbent Rosetta stone the protocol's manual-curation layer accounts for.

**On the user's question** — can Aaker serve as the "genuinely independent second author"? Partially.
Aaker is the genuinely independent *incumbent vocabulary*, and negotiating it against SBT does
produce a real adversarial result (`DANGLING_IMPORT`) plus an honest CONFLICT null that is itself
evidence of SBT's naming discipline — a real step up the evidence ladder from the single-author
SBT/OST pair. But the module is transcribed *by the SBT author*, not authored by Aaker, and the
experiment exposes the key-based linker's scope boundary (it surfaces key-collisions and explicit
dependencies, not latent cross-key synonymy). The final rung — a *living* independent co-author
authoring their own modules and resolving a genuine same-key conflict in dialogue — remains future
work.
