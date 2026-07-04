# PRISM-M Instrument Scaffold

Dmitry Zharnikov · ORCID 0009-0000-6893-9231 · Working Paper v1.0.0 — July 2026

**Status:** PRE-DRAFT empirical scaffold (companion to `PREREGISTRATION.md`). PRISM-M is the
metamerism member of the PRISM family; it inherits the **PL0–PL4 scaffold** from PRISM-B and
substitutes metamer-pair stimuli at PL2 and the operator-floored metameric-fraction estimator
at PL4. The eight-dimension construct, cross-family operator discipline, and per-pair
resolution criterion are shared with PRISM-B / the Brand Spectrometer (2026ax).

> Naming note: **PL0–PL4** are the PRISM *scaffold layers*. PRISM-M has no Likert items (it is
> an AI-observer instrument); its unit is the **metamer pair**, labelled `MP-<n>`.

---

## The PL0–PL4 scaffold, instantiated for metamerism

| Layer | PRISM-M instantiation |
|---|---|
| **PL0 Specification** | The frozen protocol — `PREREGISTRATION.md` (H1 existence, H2 aggregator-dependence, H3 universality; the metamer criterion; α allocation; stopping rules). |
| **PL1 Configuration** | Cross-family operator pairs (renderer ≠ extractor family, 2026ap); temperature 0 where honored; the aggregator battery (scalar health score, top-k ranking, recommendation pick); per-pair operator + aggregator floor passes; retry/redraw policy for malformed output. |
| **PL2 Prompts** | The PRISM-B eight-dimension extraction prompt (unchanged, shared) + the three aggregator prompts (score / rank / pick), each with a structured JSON output schema; version tag `prism-m/v1.0.0`. |
| **PL3 Sessions** | Append-only JSONL, one record per (pair, brand, operator-pair, readout): prompt, raw response, parsed vector/scalar, floor pass id, metadata, timestamp. Immutable; logged via the shared LLM-call logger. |
| **PL4 Analysis** | Deterministic, seeded estimator: per-pair full-readout distance + aggregator distance, operator/aggregator floors, the metameric-fraction with an operator-floored source-cluster bootstrap CI, the H2 severity-ladder test, the H3 cross-operator dispersion. Published under `prism-m/code/`. |

## Construct

The unit of measurement is the **metamer pair**: two brands whose eight-dimension PRISM-B
profiles are *resolved distinct* (distance clears the operator floor) but whose **aggregator
readout** is *unresolved* (within the aggregator's own floor). PRISM-M measures the
**metameric fraction** — the share of resolvable brand distinctions an aggregator destroys —
which operationalizes spectral metamerism (2026e) as a quantity, not a claim.

## Metamer-pair construction (PL2 / PL1)

1. **Brand pool.** ≥ 40 brand stimuli spanning the five SBT coherence types (ecosystem, signal,
   identity, experiential-asymmetry, incoherent; 2026s), each with ≥ 4 public artifacts so the
   artifact floor is estimable.
2. **Full readout.** Run PRISM-B (the Brand Spectrometer pipeline) on every brand under the
   cross-family operator pairs; record the eight-dimension vector + operator floor per brand.
3. **Candidate enumeration.** For each brand pair, compute the full-readout distance and the
   provisional scalar-aggregator distance. Retain candidates per the §6 retention rule
   (full S/N > 2 AND scalar S/N < 1); flag the marginal band.
4. **Freeze.** Version the retained pair bank as `prism-m/v1.0.0` PL2; lock before Stage 2.

## The aggregator battery (PL1)

Each aggregator is a projection T_k of the eight-dimension vector to a coarser readout, matching
a real downstream consumption surface (the correspondence-principle operators, 2026au):

- **A-SCORE** — a single brand-health scalar (the seven-metric scorecard grade A+..F mapped to
  [0,1]); the maximal garbling.
- **A-RANK** — top-k position in a "which brand best fits <need>" ranking prompt.
- **A-PICK** — the binary recommendation ("recommend this brand? yes/no") pick.

Each aggregator gets its OWN operator floor (dispersion across cross-family operator pairs), so
"unresolved on the aggregator" is measured against noise, never asserted.

## Metameric-fraction estimator (PL4)

For aggregator T_k over the frozen pair bank:

    metameric_fraction(T_k) = |{ pairs resolved on full readout AND unresolved on T_k }|
                              / |{ pairs resolved on full readout }|

reported with a source-cluster bootstrap 95% CI and the per-pair S/N magnitudes. H2 tests the
ladder fraction(A-SCORE) > fraction(A-RANK) > fraction(full = 0); H3 tests that the fraction for
a fixed T_k is stable across operator pairs within the operator floor (the substrate-floor
no-rescue logic, 2026ay, applied to the fraction).

## Controls (PL1)

- **Negative control** — a same-brand two-artifact-draw "pair" must NOT be flagged metameric
  (its full-readout distance is within the artifact floor, so it is not resolved-distinct).
- **Positive control** — a planted pair (profiles engineered distinct on a dimension the scalar
  weights to zero) MUST be flagged metameric; failure indicates the estimator is insensitive.

## References

Zharnikov D. Spectral Brand Theory. 2026a. · Spectral Metamerism. 2026e. · Coherence Type as
Crisis Predictor. 2026s. · Behavioral Metamerism in AI-Mediated Search. 2026x. · The Brand
Spectrometer. 2026ax. · The Correspondence Principle of Brand Management. 2026au. · Cross-Family
Operator Discipline. 2026ap. · The Substrate Floor. 2026ay.
