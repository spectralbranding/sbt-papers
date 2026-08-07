# PRISM-T Instrument Scaffold

Dmitry Zharnikov · ORCID 0009-0000-6893-9231 · Working Paper v1.0.0 — July 2026

**Status:** PRE-DRAFT empirical scaffold (companion to `PREREGISTRATION.md`). PRISM-T is the
temporal member of the PRISM family; it inherits the **PL0–PL4 scaffold** from PRISM-B and
holds artifacts + prompts constant while varying the model version at PL1. The eight-dimension
construct, cross-family operator discipline, and per-pair resolution criterion are shared with
PRISM-B / the Brand Spectrometer (2026ax).

> Naming note: **PL0–PL4** are the PRISM *scaffold layers*. PRISM-T's unit is the
> **(brand, version-epoch)** reading; version epochs are labelled `VE-<n>`.

---

## The PL0–PL4 scaffold, instantiated for temporal drift

| Layer | PRISM-T instantiation |
|---|---|
| **PL0 Specification** | The frozen protocol — `PREREGISTRATION.md` (H1 drift exists, H2 pinned isolation, H3 dimension structure; the drift criterion; α allocation; stopping rules). |
| **PL1 Configuration** | The model-version ladder (≥ 2 epochs of ≥ 1 family; ideally 2 families); cross-family operator pairs within each epoch (2026ap); temperature 0 where honored; the pinned-vs-live panel switch; retry/redraw policy. **The version is the only thing that moves on the pinned panel.** |
| **PL2 Prompts** | The PRISM-B eight-dimension render + extract prompts, byte-identical across epochs (a changed prompt would confound version drift); version tag `prism-t/v1.0.0`. |
| **PL3 Sessions** | Append-only JSONL, one record per (brand, artifact, version-epoch, operator-pair, panel): prompt, raw response, parsed vector, epoch id, panel id (pinned/live), metadata, timestamp. Immutable; logged via the shared LLM-call logger. **The pinned artifact panel is stored byte-identical.** |
| **PL4 Analysis** | Deterministic, seeded estimator: the version floor (pinned inter-epoch distance), the operator-floor baseline (contemporaneous), the pinned-vs-live drift decomposition (brand-signal estimate), the per-dimension drift split, all with source-cluster bootstrap CIs. Published under `prism-t/code/`. |

## Construct

The unit is the **(brand, version-epoch) reading**. PRISM-T measures the **version floor** — the
dispersion of a brand's eight-dimension reading across model versions of a family reading a
byte-identical artifact panel — and decomposes an observed longitudinal change into *apparatus
drift* (version floor) and *brand signal* (live-panel change beyond the version floor). It
extends the Brand Spectrometer's operator floor from a same-time cross-model band to an
across-time cross-version band.

## The two panels (PL1 / PL3)

- **Pinned panel.** ≥ 30 brands × ≥ 4 public artifacts, captured once and stored byte-identical.
  Re-read at every version epoch. Because the input never changes, ALL change on the pinned panel
  is apparatus drift — this is the isolation that makes the decomposition valid.
- **Live panel.** The same brands, re-collected fresh at each epoch. Its change = version floor +
  brand signal; subtracting the pinned version floor estimates the brand signal.

## Version-floor estimator (PL4)

For a brand across epochs {VE-1, VE-2, …} on the pinned panel under matched operators:

    version_floor(brand) = max over epoch-pairs of  distance( reading(VE-i), reading(VE-j) )

compared against the contemporaneous operator floor (the H1 baseline). A version pair *drifts*
when the pinned inter-version S/N (inter-version distance / operator floor) clears k = 2. The
per-dimension decomposition attributes the drift across the eight bands (H3: high-drift vs
format-anchored sets). The substrate-floor no-rescue logic (2026ay) governs the nesting:
operator ⊆ version, so a longitudinal finding must clear the version floor, not merely the
operator floor.

## Controls (PL1)

- **Negative control** — same version, two runs: must fall within the operator floor (no drift),
  else the instrument's own non-determinism is inflating the version floor.
- **Positive control** — a deliberately distant version pair (an old vs a current model): must
  exceed the operator floor, else the estimator is insensitive to real version change.

## References

Zharnikov D. Spectral Brand Theory. 2026a. · Coherence Type as Crisis Predictor. 2026s. · The
Brand Spectrometer. 2026ax. · Cross-Family Operator Discipline. 2026ap. · The Substrate Floor.
2026ay.
