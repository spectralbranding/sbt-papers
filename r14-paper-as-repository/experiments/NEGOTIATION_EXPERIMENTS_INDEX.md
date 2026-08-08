# Negotiation experiments — index and mirror-packaging manifest

Index of the three federated ontology-negotiation experiments backing R14/2026u
Section 5.6. All three run the same tool (`code/negotiate_modules.py`) over
two namespaced module sets; together they exercise the full interaction-class set on
real, independent vocabularies. One-command reproduction:
`bash [internal path removed]`.

## The three runs

| Experiment ID | Class produced | Modules (internal) | Record |
|---|---|---|---|
| EXP-2026-06-13-NEG-SBT-OST | CLEAN (4 cross-import + 2 cross-refine) | `experiments/negotiation_real_corpora/{sbt,ost}/` | `experiments/NEGOTIATION_REAL_CORPORA_SBT_OST_2026-06-13.md` |
| EXP-2026-06-14-NEG-AAKER-SBT | DANGLING (+ curated cross-key SSSOM) | `experiments/negotiation_independent_aaker/{aaker}/` (author A = the SBT-OST `sbt/`) | `experiments/NEGOTIATION_INDEPENDENT_AAKER_SBT_2026-06-14.md` |
| EXP-2026-06-14-NEG-SPENCE-SBT | CONFLICT (+ DANGLING) | `experiments/negotiation_independent_spence/{sbt,spence}/` | `experiments/NEGOTIATION_INDEPENDENT_SPENCE_SBT_2026-06-14.md` |

Synthesis: SBT/OST = clean by construction (two convergent programs, one author);
Aaker = an independent incumbent vocabulary that produces a genuine dangling reference
but no same-key conflict (the qualified naming forecloses it); Spence = an independent
cross-disciplinary vocabulary sharing the bare term *signal*, producing the genuine
definitional conflict. Honest open limitation: all three module sets are
author-transcribed and each conflict is resolved only as a tool-proposed curation —
the final rung is a living independent co-author resolving a conflict in dialogue.

## Reproducibility

Deterministic. Term identity is a content-addressed hash of the definition text;
the classifier is a pure function of the two parsed module sets. No seed, no network,
no credentials. Each record carries pre-registered hypotheses with falsifiers, an
integrity manifest of the shared-term `def_hash` values (checkable against the live
ontology graph), and a threats-to-validity section.

## Mirror-packaging manifest (for the user's manual mirror step — NOT yet executed)

Per `[internal path removed]` + PAQS items 37a-37f, when R14/2026u is
mirrored to `sbt-papers/r14-paper-as-repository/`, copy the artifacts into an
`experiments/` tree with this layout (the paper's Section 5.6 Data Availability points
here):

```
r14-paper-as-repository/
  experiments/
    README.md                         <- a public-facing version of this index
    reproduce.sh                      <- [internal path removed]
    negotiation-sbt-ost/              <- experiments/negotiation_real_corpora/{sbt,ost}/ + sbt_ost.sssom.tsv + the record
    negotiation-aaker/                <- experiments/negotiation_independent_aaker/* + the record
    negotiation-spence/               <- experiments/negotiation_independent_spence/* + the record
```

Trim the internal-only framing when mirroring (per the no-internal-files rule): the
experiment records may keep their hypotheses/limitations (academically required
transparency), but drop any session/internal-path references and resolve the
`experiments/` paths to the public layout above. The full vocabulary attributions
(Aaker 1991/1996; Spence 1973 QJE 87(3)) live in the records and are the public
citation of record for the experiment inputs; if the venue wants them in the paper
body, register them as verified sources and cite in Section 5.6 (a quick, optional
add — held off to avoid over-citing illustrative experiment inputs in a working paper).

This manifest is tracked alongside `REMEDIATION_OWED_2026-06-13.md` Section 1b
(publication earmark). Mirror + Zenodo remain the user's single final manual batch.
