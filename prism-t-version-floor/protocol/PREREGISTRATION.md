# PRISM-T Preregistration (PL0 Specification)

Dmitry Zharnikov · ORCID 0009-0000-6893-9231 · Working Paper v1.0.0 — July 2026

**Status:** PRE-DRAFT empirical scaffold. This is the frozen PL0 layer (pre-registered
protocol) of the PRISM-T temporal study; it is *not* the paper. Per the new-R-paper pre-draft
workflow, paper drafting is gated on the Grok pre-draft review + user GO; this preregistration
is the data-collection protocol that precedes drafting. Companion: `INSTRUMENT_SCAFFOLD.md`.
Substrate paper row: `prism-t`.

---

## 1. Study information

**Title.** Separating Instrument Drift from Brand Signal: A Pre-Registered Model-Version
Tracking Instrument for AI Brand Perception (PRISM-T).

**Research question.** When an AI-observer brand instrument is re-run after the model vendor
ships a new version, how much of the change in the eight-dimension reading is *apparatus drift*
(the same artifacts read differently by a new model) versus *brand signal change* (the artifacts
themselves changed)? The Brand Spectrometer computes an **operator floor** from dispersion
across contemporaneous cross-family operators (Zharnikov 2026ax); PRISM-T extends it to a
**version floor** — dispersion across model *versions* of a family reading a *fixed* artifact
panel — so a longitudinal reading can attribute change to instrument or to brand.

**Instrument.** PRISM-T, the temporal member of the PRISM family, sharing the PL0–PL4 scaffold
with PRISM-B. It holds artifacts and prompts constant and varies the model version at PL1; the
version-floor + drift-vs-signal decomposition is the PL4 addition (`INSTRUMENT_SCAFFOLD.md`).

**Confirmatory–exploratory boundary.** Everything in this PL0 document is confirmatory.
Unspecified analyses are exploratory and reported as such (Nosek et al. 2018; Flake & Fried 2020).

## 2. Hypotheses

- **H1 (version drift exists).** Re-running the fixed-artifact panel on a later model version of
  the same family produces an eight-dimension reading that differs from the earlier version's by
  more than the *contemporaneous operator floor* — i.e. a version change moves the instrument
  more than swapping same-generation operators does. *Existence, confirmatory.*
- **H2 (pinned-artifact isolation).** With the artifact panel held byte-identical, any drift is
  attributable to the model version, not the brand: the version-floor measured on the pinned
  panel isolates apparatus drift. A separate *live* panel (fresh artifacts) is expected to move
  by version-floor PLUS brand signal; the difference estimates brand signal. *Decomposition,
  confirmatory.*
- **H3 (drift is dimension-structured).** Version drift is not uniform across the eight
  dimensions: it concentrates on the dimensions most sensitive to model world-knowledge and
  alignment changes (e.g. Ideological, Cultural), pre-registered as the high-drift set, and is
  smaller on format-anchored dimensions (e.g. Semiotic). *Directional, confirmatory.*

H1 and H2 are primary. Failure of H1 → LLM brand instruments are version-robust (a reassuring
null, reported as such); failure of H2 → the pinned/live decomposition does not isolate drift
(interpretation in §7).

## 3. Design

Fixed-panel, version-ladder design.

- **Panel (frozen).** A pinned artifact panel: ≥ 30 brands × ≥ 4 public artifacts each, spanning
  the five coherence types (2026s), captured once and stored byte-identical (PL3 immutable). A
  parallel *live* panel re-collects fresh artifacts for the same brands at each epoch.
- **Version ladder.** ≥ 2 model-version epochs of ≥ 1 model family (ideally 2 families, to
  separate family-idiosyncratic drift). At each epoch, run the full PRISM-B pipeline on BOTH the
  pinned and the live panel under the cross-family operator pairs.
- **Analysis.** Version floor from the pinned panel (H1, H2); pinned-vs-live difference for the
  brand-signal estimate (H2); per-dimension drift decomposition (H3).

## 4. Variables

- **Reading.** The eight-dimension PRISM-B brand vector; pairwise distance = 1 − cosine (2026ax).
- **Version floor.** Max distance between an epoch's pinned reading and later epochs' pinned
  readings under matched operators — the apparatus-drift band.
- **Operator floor (baseline).** Contemporaneous cross-family dispersion within one epoch (the
  PRISM-B operator floor) — the comparison band for H1.
- **Brand-signal estimate.** live-panel drift − pinned-panel version floor (H2).
- **Dimension moderator (H3).** The pre-registered high-drift vs format-anchored dimension sets.

## 5. Pre-registered comparison conditions

Drift is compared across, at minimum: (a) **pinned vs live panel** (the isolation of H2),
(b) **version epoch pair** (adjacent vs distant versions), (c) **dimension set** (high-drift vs
format-anchored, H3). A negative control (same version, two runs) must fall within the operator
floor (no drift); a positive control (a deliberately mismatched version pair) must exceed it.

## 6. Analysis plan and inference criteria

- **Drift criterion.** A version pair *drifts* on the pinned panel if the pinned inter-version
  distance exceeds k · operator_floor with pre-registered k = 2 (the 2026ax per-pair S/N rule),
  the operator floor being the contemporaneous cross-family band.
- **H1 (drift exists).** Supported if the pinned inter-version S/N (inter-version distance /
  operator floor) has a source-cluster bootstrap 95% CI lower bound > 2 for ≥ 1 version pair.
- **H2 (isolation).** Supported if (a) the pinned-panel drift is attributable to version (the
  artifacts are byte-identical, so nothing else moved) AND (b) the live-panel drift exceeds the
  pinned version floor, with the difference (brand-signal estimate) clearing its bootstrap CI.
- **H3 (dimension structure).** Per-dimension drift compared high-drift vs format-anchored by a
  Holm-corrected test; supported if the high-drift set's mean per-dimension drift exceeds the
  format-anchored set's, clearing the CI.
- **Effect sizes mandatory** (drift magnitudes, S/N, per-dimension deltas + CIs), per
  PAPER_QUALITY_STANDARDS. Exact three-digit p-values, no leading zero.

**Alpha allocation.** Family-wise α = .05 split across H1 / H2 / H3 by Bonferroni → α = .017
each. Exploratory analyses carry no protected α and are labelled exploratory.

## 7. Stopping rules, exclusions, what would change the claim

- **Stopping rule.** Collection halts at the pre-set panel size per epoch. Epochs are added only
  when a real vendor version ships (no synthetic version manufacturing); no optional stopping.
- **Exclusions (pre-registered).** A brand whose live artifacts could not be re-collected at an
  epoch is dropped from the H2 live comparison for that epoch (reported), retained for pinned.
  Malformed operator outputs are re-drawn under the logged retry policy.
- **What would change the claim.** H1 null → LLM brand instruments are version-robust at this
  scale (a bound on the drift concern; reassuring). H2 fails (pinned drift ≈ live drift) → the
  decomposition cannot separate apparatus from brand; a confound remains. H3 uniform → drift is
  not knowledge/alignment-structured; look for a global calibration shift.

## 8. Companion computation + transparency

The PL4 version-floor + drift-decomposition estimator (fixed seed, run command, README)
publishes under `prism-t/code/` in the public mirror at submission (PAPER_QUALITY_STANDARDS
37a–37e). Frozen PL0 (this file), PL1 version-ladder config, and the PL2 prompt set are
versioned before collection; the pinned artifact panel and PL3 session data are append-only and
immutable — the pinned panel is the guarantee that byte-identical inputs isolate version drift.

## 9. Pre-collection amendments (2026-07-02, recorded BEFORE any data collection)

Recorded at PL1-authoring time, before the pre-flight pilot and before any campaign API
call, per the amendment discipline established in the PRISM-C campaign (PL0 §9 there).

- **9.1 Back-catalog version epochs.** A live read-only catalog check (2026-07-02) found
  multiple REAL, already-shipped vendor versions simultaneously servable per family
  (Anthropic claude-opus-4-1 → 4-5 → 4-6 → 4-7 → 4-8; OpenAI dated snapshots
  gpt-4o-2024-11-20 → gpt-5-2025-08-07 → gpt-5.5-2026-04-23; Alibaba
  qwen3-max-2025-09-23 → qwen3.5-plus-2026-02-15 → qwen3.7-max-2026-06-08).
  Interpretation fixed ex ante: for the PINNED panel, a reading is a function of
  (artifact bytes, prompt bytes, model version) only — calendar time enters only through
  the version snapshot — so reading the pinned panel under several already-shipped
  versions at one calendar time is a valid version-epoch set for H1 and H3. This is not
  synthetic version manufacturing (§7): every rung is a real vendor release. H2's
  live-panel decomposition is calendar-bound by construction (brand signal accrues in
  time): at VE-1 the live panel coincides with the pinned capture (live ≡ pinned at
  birth), so H2 completes at a later calendar epoch (VE-2) when the live panel is
  re-collected. Version epochs are labelled by version, VE-1 = the 2026-07 capture.
- **9.2 H3 dimension sets (fixed ex ante).** High-drift (prior-dependent) =
  {Ideological, Cultural, Social, Temporal, Economic}; format-anchored (text-anchored) =
  {Semiotic, Narrative, Experiential}. H3 is ONE Holm-corrected two-set mean contrast
  (not eight per-dimension tests); per-dimension decomposition is exploratory.
  Mechanism taxonomy and rationale: `THEORY_GROUNDING.md` §5.
- **9.3 Panel.** The pinned panel reuses the frozen 40-brand stratified bank
  (`research/prism_m/PL2_BRAND_BANK.yaml`, prism-m/v1.0.0: five coherence types ×
  B2C/B2B × 4) at 40 brands × 4 artifacts (one per PL1 channel: official, press,
  experience, social), captured 2026-07-02 as real public web artifacts, stored
  byte-identical with SHA-256 manifest under `research/prism_t/panel/`. This exceeds
  the §3 minimum (≥ 30 × ≥ 4).
- **9.4 Pre-flight operator-concordance pilot.** Before the PL1 ladder freezes, a ~50-call
  screen of the candidate operator pairs runs with the mechanical exclusion rule fixed ex
  ante (discordance score > 3 × median of remaining units — the PRISM-C rule); a
  discordant pair is excluded from the stated floors (still collected, reported
  exploratory). The July-2026 epoch's known discordant observer
  (deepseek-v4-pro-as-renderer, 2026az/2026bb) is expected to trip this rule.
- **9.5 Decision provenance.** Provider set, ladder families, and the $100 budget cap
  were delegated by the user to the session (2026-07-02, "execute autonomously");
  defaults mirror the confirmed 2026az/2026bb campaign decisions.

## References (protocol)

Flake JK, Fried EI. Measurement schmeasurement. *Advances in Methods and Practices in
Psychological Science*. 2020;3(4):456-465.

Nosek BA, Ebersole CR, DeHaven AC, Mellor DT. The preregistration revolution. *PNAS*.
2018;115(11):2600-2606.

Zharnikov D. Spectral Brand Theory. 2026a. · Coherence Type as Crisis Predictor. 2026s. · The
Brand Spectrometer. 2026ax. · Cross-Family Operator Discipline. 2026ap. · The Substrate Floor.
2026ay.
