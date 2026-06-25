# Reproducibility — The Substrate Floor

Every numerical fact in [`../paper.md`](../paper.md) is reproducible from a committed, seeded,
read-only command. This file maps each paper claim to the exact command that produces it and the
value to expect. A captured run is committed at
[`../reports/REPRODUCED_FACTS_2026-06-24.md`](../reports/REPRODUCED_FACTS_2026-06-24.md).

All commands are deterministic and need no API keys. Dependencies: `numpy`, `pyyaml`
(and `matplotlib` for the figures).

## What reproduces standalone from this repository

The three companion scripts in this directory reproduce every quantitative headline in the paper
from committed inputs alone:

```
uv run --with numpy python code/verdict_regions_mc.py
uv run --with pyyaml python code/public_benchmark_reconciliation.py
uv run --with numpy --with matplotlib python code/make_figures.py
```

- `verdict_regions_mc.py` — the Monte-Carlo verdict-region characterization (fixed seed 20260624,
  200,000 draws per prior). Replicates the two-instrument lattice on the smallest sufficient model
  under three value priors (uniform / beta(2,5) / truncated-normal) with 95% nonparametric bootstrap
  CIs. Produces the paper's *Monte-Carlo Verdict Regions* and *Companion Computation Script* numbers.
- `public_benchmark_reconciliation.py` — reads the pinned, cited snapshot
  [`data/public_benchmark_snapshot.yaml`](../data/public_benchmark_snapshot.yaml) (three frontier
  models × MMLU/MATH/HumanEval accuracies + documented test-set sizes + full provenance, accessed
  2026-06-25) and runs each ordinal "A outperforms B" claim through the same `substrate_floor`
  lattice. Real, external, cross-kind data, reproducible from the committed snapshot (no live board).
  Headline: the widely-cited HumanEval code ranking is *not* certified — its 1–3pp gaps fall below
  HumanEval's ~.028 floor (N=164), so the code instrument abstains.
- `make_figures.py` — renders Figure 1 (nested floors + no-rescue schematic) and Figure 2 (the four
  verdict regions of the dispersion-by-consensus plane) deterministically (fixed seed 20260624) to
  [`../figures/`](../figures/).

### Fact → command map (standalone)

(uniform-prior headline values; the script also reports beta(2,5) and truncated-normal, and the
prior-robust ranges quoted in the paper: 4a .87–.97, 4b .18–.40, 4c .34–.48.)

| Paper fact | Value (uniform; 95% CI) | Command |
|---|---|---|
| Verdict-region fractions | corroborated .120 / contested .230 / substrate-conditional .250 / jointly-unresolved .400 | `code/verdict_regions_mc.py` |
| Lemma 4a non-pooling divergence | .880 [.878, .881] | `code/verdict_regions_mc.py` |
| Lemma 4b no-rescue divergence | .214 [.212, .216] | `code/verdict_regions_mc.py` |
| Lemma 4c typed-verdict divergence | .480 [.477, .482] | `code/verdict_regions_mc.py` |
| Public-benchmark cross-KIND verdicts (corroborated / jointly-unresolved / substrate-conditional) | 3 frontier models × MMLU/MATH/HumanEval | `code/public_benchmark_reconciliation.py` |
| Per-benchmark binomial floor by N (MMLU ~.003, MATH ~.005, HumanEval ~.028) | from documented test-set sizes | `code/public_benchmark_reconciliation.py` |

## The reference implementation (this directory)

The reconciliation lattice and its nested-floor schemas and honesty gates are the paper's central
artifact, included here as readable, auditable source:

- `substrate_floor.py` — the reconciliation lattice (realizes Algorithm 1 of the paper line for line).
- `floor_schema.py` / `ost_floor_schema.py` — the nested-floor schemas for the measurement and
  specification instrument kinds.
- `align_terms.py` — the alignment step-0 (the live-graph SSSOM aligner).
- `verify_contract.py` / `verify_ost_contract.py` — the per-instrument honesty gates (single live
  floor owner; self-certification).

The worked reconciliation cases that exercise all four typed verdicts are in
[`../cases/`](../cases/), with the external (non-corpus) vendor lens at
[`../cases/example_vendor_lens.yaml`](../cases/example_vendor_lens.yaml).

The worked-case *claim values* are illustrative inputs chosen to exercise the verdict regions (the
paper states this); the instrument *floors* are read live from pinned atlases and specification
audits maintained in the authors' project repository. Re-running the full worked-case battery
(`substrate_floor.py --all`, `verify_contract.py --all`, `verify_ost_contract.py --all`) therefore
requires those project artifacts; the companion scripts above reproduce every reported *number*
without them.
