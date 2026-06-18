# Companion Experiments — Federated Ontology Negotiation

Three deterministic runs of the cross-owner linker backing **Section 5.6** of
*Research as Repository*. Each run takes two authors' definition modules,
classifies every cross-owner interaction into one of six classes
(AGREEMENT / CROSS_IMPORT / CROSS_REFINE / CONFLICT / INCOMPATIBLE_REFINE /
DANGLING_IMPORT), and proposes a typed, justified reconciliation in
[SSSOM](https://mapping-commons.github.io/sssom/) — before either author reads
the other's prose.

| Directory | Class produced | Vocabularies |
|---|---|---|
| `negotiation-sbt-ost/` | CLEAN (4 cross-import + 2 cross-refine) | the author's perception-side and operations-side programs |
| `negotiation-aaker/` | DANGLING reference (+ curated cross-key map) | incumbent brand-equity vocabulary (Aaker 1991/1996) |
| `negotiation-spence/` | CONFLICT on the shared term *signal* (+ dangling) | information-economics signaling theory (Spence 1973) |

Together the three runs exercise the full interaction-class set on real,
independent vocabularies. The incumbent vocabularies are faithful paraphrases
transcribed from the cited published sources (attributed per term in each
module's `note:` fields and in each `RECORD.md`); the one open rung is a *living*
independent co-author authoring their own modules and resolving a conflict in
dialogue.

## Reproduce

```
bash reproduce.sh
```

Requires Python 3.12 and PyYAML (`pip install pyyaml`, or `uv run`). The two
adversarial runs leave unresolved interactions by design; `reproduce.sh` runs
report mode (exit 0) and writes each run's SSSOM next to its modules. Append
`--gate` for the nonzero federated-CI verdict.

## Layout

```
experiments/
  reproduce.sh                 one-command reproduction
  tools/                       the federated linker + its shared module parser
  negotiation-sbt-ost/         sbt/ + ost/ modules, SSSOM, RECORD.md
  negotiation-aaker/           aaker/ module, SSSOM + curated cross-key map, RECORD.md
  negotiation-spence/          sbt/ + spence/ modules, SSSOM, RECORD.md
```

Each `RECORD.md` states pre-registered hypotheses with falsification criteria, an
integrity manifest of the shared-term hashes, and a threats-to-validity section.
