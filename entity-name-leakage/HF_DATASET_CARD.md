---
license: cc-by-4.0
language:
  - en
tags:
  - llm-as-a-judge
  - measurement
  - evaluation
  - prompt-sensitivity
  - preregistered
pretty_name: Entity-Name Leakage in Dimensional LLM Readings
size_categories:
  - 1K<n<10K
configs:
  - config_name: first_collection
    data_files:
      - split: run1
        path: first_collection/data/run1/records_*.jsonl
      - split: run2
        path: first_collection/data/run2/records_*.jsonl
  - config_name: second_collection
    data_files:
      - split: run1
        path: second_collection/data/run1/records_*.jsonl
      - split: run2
        path: second_collection/data/run2/records_*.jsonl
---

# Entity-Name Leakage in Dimensional LLM Readings

Instrument records of record for the study *The Label Moves the Reading*, which holds a written
artifact byte-identical, exchanges only the entity name it concerns, and measures what an
eight-dimensional rating does in response.

Two independently designed collections, each run twice, are released whole: every call with its
prompt, parameters, prompt hash and response, alongside the frozen protocols, stimulus packs,
harness code and freeze records that fix what was decided before collection began.

## What is here

| Directory | Collection | Design | Name-swap records |
|---|---|---|---|
| `first_collection/` | Corpus-prevalence probe | Four artifact texts, each written for a specific prevalent brand, each paired against an invented name | 97 (run 1) + 96 (run 2) |
| `second_collection/` | Name-effect probe | Nine entities across three prevalence strata, crossed with four texts authored for no entity | 432 (run 1) + 432 (run 2) |

Each collection directory holds:

```
PROTOCOL.yaml          pre-registration, frozen before the first live call
FREEZE_RECORD.md       SHA-256 over the protocol, stimulus pack and harness
data/stimuli.yaml      the artifact texts and the entity slot
data/prevalence.yaml   the corpus-prevalence capture the strata were built on
data/run1/, data/run2/ instrument records, one JSONL per operator
logs/run1/, logs/run2/ the full call log for each run
code/                  the collection harness and its unit tests
output/                each run's own report and result tables
```

The record files carry both arms. `A2_NAMESWAP` is the name-exchange contrast the study reports;
`A1_GRADIENT` is the frame-gradient arm collected alongside it. The counts above are the
`A2_NAMESWAP` rows, and they are the records the paper's Table 2 reports.

## Verifying the freeze

Every SHA-256 in a collection's `FREEZE_RECORD.md` is stated over a path relative to that
collection's own directory, so the freeze is checkable in place rather than on trust:

```bash
cd second_collection && shasum -a 256 PROTOCOL.yaml data/stimuli.yaml code/*.py
```

**Eight files will not match, and that is the mechanism working rather than failing.** A freeze
record fixes the state before collection; anything changed afterwards is recorded as an append-only
entry in that protocol's `AMENDMENTS:` block, and the checksum mismatch is how a reader finds it
without taking anyone's word for what changed.

| Collection | Does not match | Recorded as |
|---|---|---|
| `first_collection` | `code/probe_lib.py`, `code/tests/test_probe_lib.py` | A2 — the token cap was raised for the two operators it was silently binding on |
| `second_collection` | `code/analyze.py`, `code/stats_core.py`, `code/tests/test_name_effect_core.py`, `code/tests/test_probe_lib.py` | A1 — the reporting module rewritten during run 1, before any collected value was read; A2 — the neutrality guard corrected to compute the interaction its own protocol sentence defined |
| both | `PROTOCOL.yaml` | the amendments themselves, appended at the bottom and never edited in place |

Amendment A2 on `second_collection` is the one to read first. It changed analysis code *after* both
runs had been collected and read, says so in those words, and did not change the verdict — the guard
still fires, so the decomposition the paper wanted is still not licensed. The more permissive variant
that would have cleared the guard was computed, reported as a diagnostic, and deliberately not
adopted as the decision rule.

Every other checksummed file is byte-identical to what was frozen. Byte-identity is also why the
frozen files still carry the authoring paths they were checksummed with: rewriting those strings to
tidy them would invalidate the record this dataset exists to make verifiable.

## Reproducing the reported analysis

The analysis scripts live with the paper, not here. Each carries its own pinned dependencies inline,
so `uv` provisions them and nothing else needs installing:

```bash
git clone https://github.com/spectralbranding/sbt-papers
hf download spectralbranding/entity-name-leakage --repo-type dataset --local-dir enl-data
cd sbt-papers/entity-name-leakage
./reproduce.sh ../../enl-data/second_collection
```

Or one at a time, which is what `reproduce.sh` does:

```bash
uv run code/estimate_guard_ratio.py  --data-root ../../enl-data/second_collection
uv run code/per_dimension_leakage.py --data-root ../../enl-data/second_collection
uv run code/equivalence_power.py
uv run code/simulate_guard_power.py
```

Tables are written to `output/tables/`. `estimate_guard_ratio.py` recomputes this collection's own
published aggregate name effect first and refuses to report a ratio unless it reproduces to within
.01, so a misread of the metric stops the run instead of producing a number.

## Scope

The material is nine names in one product domain, cookware. The stimulus texts are authored copy
that makes no factual claim about any real company, so nothing here asserts anything true or false
of a named firm. Model identifiers are pinned literally in each protocol rather than resolved at
run time, because two independently collected runs are compared against each other and an operator
that changed silently between them would be indistinguishable from the effect under test.

Whether the exchanged name removes what the model already knows has not been measured. Every
magnitude in the paper may therefore be a lower bound.

## Licence

Records, protocols and stimulus packs: CC BY 4.0. Harness code under each `code/`: MIT.

## Citation

Zharnikov, Dmitry (2026). *The Label Moves the Reading: Entity-Name Leakage in Language-Model Dimensional Ratings of a Fixed Text*. Zenodo.
https://doi.org/10.5281/zenodo.22161305
