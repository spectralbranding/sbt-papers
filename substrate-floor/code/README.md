# Reproducibility — The Substrate Floor

Every numerical fact in `[internal path removed]` is reproducible from a committed,
seeded, read-only command. This file is the manifest: each paper claim maps to the exact command
that produces it and the value to expect. A captured run of all commands is committed at
`[internal path removed]`.

All commands are deterministic and need no API keys. They read only committed artifacts (the
worked-case YAMLs and atlases under `[internal path removed]`). Dependencies: `numpy`, `pyyaml`.

## Companion computation script (this directory)

`verdict_regions_mc.py` — the Monte-Carlo verdict-region characterization (paper methods ME1,
robustness RC3). Replicates the two-instrument lattice of the reference implementation
(`code/substrate_floor.py`) on the smallest sufficient model and sweeps it under three
value priors (uniform / beta(2,5) / truncated-normal) with 95% nonparametric bootstrap CIs.

```
uv run --with numpy python code/verdict_regions_mc.py
```

Fixed seed 20260624, 200,000 draws per prior. Produces the numbers in the paper's
*Monte-Carlo Verdict Regions* and *Companion Computation Script* sections.

`make_figures.py` — renders the paper's two figures deterministically (fixed seed 20260624):
Figure 1 (nested floors + no-rescue schematic) and Figure 2 (the four verdict regions of the
dispersion-by-consensus plane at two floor widths). Figures are reproducible from source like every
number.

```
uv run --with numpy --with matplotlib python code/make_figures.py
```

## Fact → command map

(uniform-prior headline values; the script also reports beta(2,5) and truncated-normal, and the
prior-robust ranges quoted in the paper: 4a .87–.97, 4b .18–.40, 4c .34–.48.)

| Paper fact | Value (uniform; 95% CI) | Command |
|---|---|---|
| Verdict-region fractions | corroborated .120 / contested .230 / substrate-conditional .250 / jointly-unresolved .400 | `verdict_regions_mc.py` (this dir) |
| Lemma 4a non-pooling divergence | .880 [.878, .881] | `verdict_regions_mc.py` |
| Lemma 4b no-rescue divergence | .214 [.212, .216] | `verdict_regions_mc.py` |
| Lemma 4c typed-verdict divergence | .480 [.477, .482] | `verdict_regions_mc.py` |
| Corroborated worked case (dispersion .02, S/N 3.33) | `ma_fit_corroborated` | `substrate_floor.py --all` |
| Contested worked case (dispersion .55, S/N .86) | `ma_fit_contested` | `substrate_floor.py --all` |
| Substrate-conditional (S/N 8.0, entropy 1.0) | `ma_fit_substrate_conditional` | `substrate_floor.py --all` |
| Jointly-unresolved, all abstain | `ma_fit_jointly_unresolved` | `substrate_floor.py --all` |
| Agreement-on-noise → jointly-unresolved (dispersion .01, S/N .50) | `ma_fit_agreement_on_noise` | `substrate_floor.py --all` |
| Unaligned false-agreement → contested downgrade | `ma_fit_unaligned_false_agreement` | `substrate_floor.py --all` |
| External (non-corpus) lens → corroborated (S/N 3.67, closeMatch risk) | `ext_fit_corroborated_with_closematch` | `substrate_floor.py --all` |
| SBT live operator floor .0103, resolves magnitude .0812 | `example_harbor_full_reuse` | `verify_contract.py --all` |
| OST live coherence floor .083, resolves .21 / abstains .05 | `EXAMPLE_meridian_transfer` | `verify_ost_contract.py --all` |
| Public-benchmark cross-KIND verdicts (corroborated / jointly-unresolved / substrate-conditional) | 3 frontier models × MMLU/MATH/HumanEval | `public_benchmark_reconciliation.py` (this dir) |
| Per-benchmark binomial floor by N (MMLU ~.003, MATH ~.005, HumanEval ~.028) | from documented test-set sizes | `public_benchmark_reconciliation.py` |

`public_benchmark_reconciliation.py` reads the pinned, cited snapshot
`data/public_benchmark_snapshot.yaml` (model accuracies + documented N +
full provenance, accessed 2026-06-25) and runs each ordinal "A outperforms B" claim through the
SAME `[internal path removed]` lattice. Real, external, cross-kind data; reproducible
from the committed snapshot (no live board). The headline: the widely-cited HumanEval code ranking is
NOT certified — its 1–3pp gaps fall below HumanEval's ~.028 floor (N=164), so the code instrument
abstains.

where the bare tool names live in `[internal path removed]`:

```
uv run --with pyyaml python code/substrate_floor.py --all
uv run --with pyyaml python code/verify_contract.py --all
uv run --with pyyaml python code/verify_ost_contract.py --all
```

## Committed inputs (the facts the paper is based on)

- Reconciliation worked cases: `cases/reconciliation/` (the four typed verdicts).
- External-vendor lens: `[internal path removed]` (the non-corpus instrument).
- Specification-contract cases + atlases: under `[internal path removed]` (live floors read by the verify gates).
- Reference implementation: `code/substrate_floor.py` (lattice), `floor_schema.py` /
  `ost_floor_schema.py` (nested-floor schemas), `align_terms.py` (alignment step-0),
  `verify_contract.py` / `verify_ost_contract.py` (per-instrument honesty gates).
