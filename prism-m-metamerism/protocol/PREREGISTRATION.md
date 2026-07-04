# PRISM-M Preregistration (PL0 Specification)

Dmitry Zharnikov · ORCID 0009-0000-6893-9231 · Working Paper v1.0.0 — July 2026

**Status:** PRE-DRAFT empirical scaffold. This is the frozen PL0 layer (pre-registered
protocol) of the PRISM-M metamerism study; it is *not* the paper. Per the new-R-paper
pre-draft workflow, paper drafting is gated on the Grok pre-draft review + user GO; this
preregistration is the data-collection protocol that precedes drafting. Companion:
`INSTRUMENT_SCAFFOLD.md`. Substrate paper row: `prism-m`.

---

## 1. Study information

**Title.** Measuring Perceptual Indistinguishability: A Pre-Registered Metamerism Instrument
for AI Brand Perception (PRISM-M).

**Research question.** When do two brands with *structurally distinct* eight-dimension
perception profiles become *indistinguishable* under an aggregating readout — a single
brand-health score, a search ranking, a recommendation pick — and how large is that metameric
fraction? Spectral metamerism (Zharnikov 2026e) predicts that projecting the eight-dimension
profile to a scalar is a geometric garbling that maps distinct profiles to equal scalars;
behavioral metamerism (Zharnikov 2026x) observes the effect in AI-mediated search. PRISM-M
turns the prediction into a measured quantity.

**Instrument.** PRISM-M, the metamerism member of the PRISM family, sharing the PL0–PL4
scaffold with PRISM-B. It substitutes **metamer-pair stimuli** at PL2 and the
**operator-floored metameric-fraction estimator** at PL4 (`INSTRUMENT_SCAFFOLD.md`).

**Confirmatory–exploratory boundary.** Everything in this PL0 document is confirmatory.
Analyses not specified here are exploratory and reported as such regardless of significance
(Nosek, Ebersole, DeHaven, & Mellor 2018; Flake & Fried 2020).

## 2. Hypotheses

- **H1 (metameric collapse exists).** There exist brand pairs whose full eight-dimension
  PRISM-B profiles differ beyond the operator noise floor (resolved as distinct) yet whose
  aggregator readouts (§4) do not differ beyond the aggregator's own floor (unresolved) — a
  measured *metameric pair*. *Existence, confirmatory.*
- **H2 (aggregator-dependence).** The metameric fraction is monotone in the garbling severity
  of the aggregator: a single scalar health score collapses more pairs than a top-3 ranking,
  which collapses more than the full eight-dimension readout (which collapses none by
  construction). *Directional, confirmatory.*
- **H3 (cross-model universality).** The metameric fraction for a fixed aggregator is stable
  across cross-family operator pairs within the operator floor — the collapse is a property of
  the aggregator's geometry, not of one model family. *Directional, confirmatory.*

H1 and H2 are primary. Failure of H1 would falsify the spectral-metamerism prediction for AI
observers; failure of H2 would sever the garbling account (interpretation in §7).

## 3. Design

Metamer-search design over a pre-registered brand-pair bank.

- **Stage 1 — Pair construction (exploratory, ~200 candidate pairs).** From a stimulus set
  spanning the five coherence types (2026s), enumerate brand pairs; run PRISM-B on each brand;
  retain candidate *metamer pairs* whose eight-dimension distance clears the operator floor
  (distinct) but whose provisional scalar score is within the scalar floor (collapsed). Stage 1
  is exploratory; its only confirmatory commitment is the retention rule in §6. The candidate
  bank is frozen before Stage 2.
- **Stage 2 — Confirmation (confirmatory).** Re-run PRISM-B + the full aggregator battery (§4)
  on the frozen pairs under ≥ 3 cross-family operator pairs, with the operator + aggregator
  floors computed per pair. Test H1 (metameric pairs survive), H2 (fraction by aggregator),
  H3 (fraction stability across operators).

## 4. Variables

- **Full readout.** The eight-dimension PRISM-B cohort/brand vector; pairwise distance =
  1 − cosine similarity (2026ax).
- **Aggregators (the garbling operators under test).** (a) single scalar brand-health score
  (A+..F → [0,1]); (b) top-k search ranking position; (c) recommendation pick (chosen / not).
  Each is a measurable projection T_k of the full vector (correspondence-principle operator,
  2026au).
- **Metameric fraction.** The proportion of resolved-distinct pairs that the aggregator renders
  unresolved, over the pair bank, per aggregator, with an operator-floored bootstrap CI.
- **Operator moderators (H3).** Cross-family renderer × extractor pairs (2026ap).

## 5. Pre-registered comparison conditions

The metameric fraction is compared across, at minimum: (a) **aggregator type** (scalar vs
ranking vs pick — the H2 severity ladder), (b) **coherence type of the pair** (within-type vs
cross-type metamers; 2026s), (c) **operator family pair** (H3). A negative control pair
(same brand, two artifact draws) must NOT be flagged metameric; a positive control (a planted
scalar-equal, profile-distinct pair) must be.

## 6. Analysis plan and inference criteria

- **Resolution criterion (per readout).** A pair is *resolved* on a readout if its distance
  exceeds k · floor with pre-registered k = 2 (the PRISM-B / 2026ax per-pair S/N rule); the
  floor is the readout's own operator floor (max over cross-family alt-pairs). *Metameric* =
  resolved on the full eight-dimension readout AND unresolved on the aggregator.
- **Pair retention rule (Stage 1, frozen before Stage 2).** Retain a candidate metamer pair if
  its eight-dimension S/N > 2 (distinct) and its provisional scalar S/N < 1 (collapsed); pairs
  in the marginal band (1–2) are flagged, not retained.
- **H1 (existence).** Supported if ≥ 1 pair is metameric under the frozen criterion with the
  operator-floored bootstrap 95% CI of the full-readout S/N lower bound > 2 AND the aggregator
  S/N upper bound < 1.
- **H2 (aggregator-dependence).** Metameric fraction by aggregator compared by a Holm-corrected
  test of proportions across the severity ladder; supported if fraction(scalar) >
  fraction(ranking) > fraction(full = 0), each difference clearing its bootstrap CI.
- **H3 (universality).** Supported if the cross-operator dispersion of the metameric fraction
  for a fixed aggregator is within the operator floor (agreement is triangulation; 2026ay
  substrate-floor logic applied to the fraction).
- **Effect sizes mandatory** (the fraction itself, its CI, the S/N magnitudes), per
  PAPER_QUALITY_STANDARDS. Exact three-digit p-values, no leading zero.

**Alpha allocation.** Family-wise α = .05 split across H1 / H2 / H3 by Bonferroni → α = .017
each. Exploratory analyses carry no protected α and are labelled exploratory.

## 7. Stopping rules, exclusions, what would change the claim

- **Stopping rule.** Collection halts at the pre-set pair-bank size per stage. No optional
  stopping; no peeking-driven extension.
- **Exclusions (pre-registered).** A pair whose full-readout distance does not clear the
  operator floor (not distinct — cannot be a metamer) is excluded from H1/H2 (reported).
  Malformed/unparseable operator outputs are re-drawn under the logged retry policy.
- **What would change the claim.** H1 null (no metameric pairs) → the aggregate readout loses
  no resolvable distinction at this scale — a boundary on the garbling claim, reported as such.
  H2 non-monotone → the collapse is not explained by garbling severity; look for a
  content-specific artifact. H3 fails → the fraction is model-family-specific, not geometric.

## 8. Companion computation + transparency

The PL4 metameric-fraction estimator (pair distances, operator/aggregator floors, bootstrap
CIs, fixed seed, run command, README) publishes under `prism-m/code/` in the public mirror at
submission (PAPER_QUALITY_STANDARDS 37a–37e). Frozen PL0 (this file), PL1 configuration, and
the PL2 pair bank are versioned before collection; PL3 session data is append-only and
immutable.

## References (protocol)

Flake JK, Fried EI. Measurement schmeasurement: Questionable measurement practices and how to
avoid them. *Advances in Methods and Practices in Psychological Science*. 2020;3(4):456-465.

Nosek BA, Ebersole CR, DeHaven AC, Mellor DT. The preregistration revolution. *PNAS*.
2018;115(11):2600-2606.

Zharnikov D. Spectral Brand Theory. 2026a. · Spectral Metamerism. 2026e. · Coherence Type as
Crisis Predictor. 2026s. · Behavioral Metamerism in AI-Mediated Search. 2026x. · The Brand
Spectrometer. 2026ax. · The Correspondence Principle of Brand Management. 2026au. · Cross-Family
Operator Discipline. 2026ap. · The Substrate Floor. 2026ay.
