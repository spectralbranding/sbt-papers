# PRISM-T Theory Grounding — the Version Floor as a Metrological Construct

Date: 2026-07-02. Phase-2 output feeding the SPINE (authored before any prose drafting,
per the spine-first protocol). Supplies the theoretical framing
beyond the corpus and the boundary conditions, using the six sources registered
2026-07-02 from `DR_PHASE_2_CITATIONS.md`. All external claims here trace to verified
substrate sources; corpus claims trace to the cited papers.

---

## 1. Classical test theory: the version floor as apparatus retest dispersion

Classical test theory decomposes an observed score into a true score and an error term,
and defines reliability through the dispersion of repeated parallel measurements
(Novick 1966, `novick-1966-classical-test-theory`). Test-retest reliability presumes the
*instrument* is the fixed element and the *respondent* contributes the retest error. An
LLM-observer instrument inverts the locus of error: the stimulus (a byte-identical
artifact panel plus byte-identical prompts) can be held genuinely fixed — a luxury no
human-respondent design has — while the apparatus itself is replaced between
administrations whenever the vendor ships a new model version. The **version floor** is
the CTT retest-dispersion quantity computed under this inversion: the dispersion across
model versions of a family reading a byte-identical panel. Because the input cannot have
changed, the version floor is a pure apparatus-error band, the temporal analogue of the
operator floor of 2026ax (dispersion across contemporaneous cross-family operator pairs).
In CTT terms: the operator floor bounds parallel-forms error at one time point; the
version floor bounds the additional error introduced when the "form" is a successor
version of the same instrument family.

## 2. Measurement invariance: version change as instrument non-invariance over time

The longitudinal measurement-invariance literature asks whether an instrument measures
the same construct across time — factorial invariance across repeated administrations is
the precondition for interpreting observed change as construct change (Widaman, Ferrer &
Conger 2010, `widaman-2010-factorial-invariance-longitudinal`; conventions in
`putnick-2016-measurement-invariance-conventions`). A vendor version change is a
potential invariance violation located in the *instrument*, not the population: the same
artifact panel may load onto the eight dimensions differently under the successor
version. PRISM-T operationalizes this as a magnitude bound rather than a latent-variable
test: the version floor is a non-parametric non-invariance band in construct units
(1 − cosine on the eight-dimension reading), estimable per version pair and per
dimension without a factor model, and re-estimable every time a version ships. The
measurement-practices critique (Flake, Pek & Hehman 2017,
`flake-2017-construct-validation-practice`; Flake & Fried 2020) is the discipline frame:
construct validity claims require the measurement layer to be interrogated, not assumed —
PRISM-T makes the temporal layer of that interrogation routine equipment.

## 3. Concept drift inverted: fixed data, moving model

The ML drift-monitoring literature (Gama et al. 2014, `gama-2014-concept-drift-survey`;
Lu et al. 2019, `lu-2019-learning-concept-drift`) studies deployed learners whose *data
distribution* drifts under a *fixed* model, and builds detectors for changes in P(X) and
P(y|X). PRISM-T is the mirror image: the data are fixed by construction (the pinned
panel is stored byte-identical) and the *model* moves (the vendor ships a version). The
identification logic is inherited but inverted — where concept-drift detection must
disentangle data change from model misfit, the pinned panel removes data change entirely,
so any pinned-panel movement is apparatus drift by construction. The live panel then
restores the ecological quantity (data change plus apparatus change), and the
live-minus-pinned difference estimates the brand signal. This inversion is what the
drift-monitoring literature does not supply: its detectors assume the model is the
constant; a measurement practice built on vendor-hosted LLMs cannot.

## 4. Contrast with Chen, Zaharia & Zou (2024): from documenting drift to flooring it

Chen, Zaharia & Zou (2024, `chen-2024-chatgpt-behavior-changing`) documented that the
March and June 2023 snapshots of GPT-3.5 and GPT-4 differ substantially on task accuracy
and behavior — the canonical demonstration that LLM behavior drifts across releases.
PRISM-T differs on four axes. (a) **Unit**: they measure task accuracy against ground
truth; PRISM-T measures drift in *construct units* (the eight-dimension brand reading),
where no ground truth exists and the comparison band must be instrument-computed
(the metameric-psychometrics move of 2026ax). (b) **Baseline**: their drift has no
contemporaneous comparison band; PRISM-T tests version drift against the operator floor —
drift "exists" only if a version change moves the reading more than swapping
same-generation cross-family operators does. (c) **Identification**: their design is
observational across snapshots; PRISM-T pre-registers a pinned/live two-panel
decomposition that separates apparatus drift from stimulus change. (d) **Interpretation**:
they report drift as a finding; PRISM-T pre-registers both outcomes (drift → the version
floor becomes mandatory equipment for longitudinal LLM measurement; null →
version-robustness becomes a measured, citable property with a CI). In short: Chen et
al. established that the phenomenon exists at the task level; PRISM-T turns it into a
calibrated reliability quantity at the measurement level.

## 5. Mechanism taxonomy: when should temporal non-invariance arise? (grounds H3)

Three mechanism classes predict *where* on the eight dimensions version drift should
concentrate, giving H3 its pre-registered dimension sets:

- **T1 — alignment updates.** Post-training value/safety recalibration between versions
  shifts value-laden readings: Ideological, Cultural, Social.
- **T2 — world-knowledge refresh.** A new training cutoff imports new facts about the
  brand's trajectory and market context, shifting knowledge-anchored readings even for a
  fixed artifact: Temporal, Economic.
- **T3 — format/decoding changes.** Tokenizer, decoding, or instruction-following changes
  alter surface behavior but not construct content; byte-identical prompts plus
  cross-family extraction (2026ap) are the designed controls, and any residual T3 effect
  should be dimension-flat, not dimension-structured.

The discriminating logic: on a *pinned* artifact, the model's contribution to the reading
is largest where the reading leans on model priors beyond the text, and smallest where
the reading is anchored in what the artifact literally displays. **Pre-registered H3
sets (fixed ex ante, before any collection): high-drift = {Ideological, Cultural,
Social, Temporal, Economic} (prior-dependent); format-anchored = {Semiotic, Narrative,
Experiential} (text-anchored).** H3 is tested as the mean per-dimension drift contrast
between the two sets (one Holm-corrected contrast, not eight per-dimension tests — the
power-preserving collapse chosen at design time). Exploratory per-dimension
decomposition is reported descriptively alongside.

## 6. Scope conditions (pre-registered boundary of the calibration claim)

The instrument is calibrated for: **public digital artifacts** (owned media, press,
review, forum text) of **consumer and B2B brands**, in **English**, read by **major API
families with stable versioned release channels and open-weights families** (the
replicable ladder — open-weights checkpoints are pinned by construction). Epochs are
**real vendor releases only**; synthetic versioning (fine-tunes, quantizations, prompt
variants) is excluded as a confound, as is any prompt change between epochs
(byte-identical prompts are part of the pinned input). Out of scope: non-English
artifacts (cross-language invariance is a separate question — 2026v Experiment B),
multimodal artifacts, private/paywalled artifact classes, and models without a version
identity (endpoints that silently mutate; these are measurable only as live-endpoint
drift, a weaker design noted in Limitations).

## 7. Nesting rule (unit of analysis discipline)

The unit is the **(brand, version-epoch) reading**. Floors nest: operator ⊆ version —
a longitudinal claim must clear the version floor, not merely the operator floor, and
the no-rescue rule of 2026ay applies (a reading that fails its floor abstains; it is not
rescued by an auxiliary argument). "The brand moved" is shorthand that is only licensed
when live-panel movement clears the version floor measured on the pinned panel for the
same epoch pair.

## 8. External boundary objects (the review's self-referentiality fix)

Three external phenomena the version floor should bound or predict:

1. **AI-visibility / GEO tracking dashboards.** Practitioner brand-visibility trackers
   re-query vendor endpoints continuously; any step-change coinciding with a model
   release is uninterpretable without a version floor — the instrument predicts such
   dashboards show release-synchronized discontinuities on prior-dependent readings.
2. **LLM-augmented brand-tracking in marketing-mix practice.** Where LLM-derived
   perception covariates feed longitudinal models, a version change induces a break in
   the covariate series; the version floor is the correction band a practitioner must
   subtract before attributing movement to campaigns.
3. **Replication across model vintages.** Any published LLM-observer brand finding
   (including this corpus's own) is implicitly indexed by model version; the version
   floor quantifies how far a finding should be expected to travel to a successor
   version — H13's cosines > .97 (2026v) are the first, unfloored estimate of exactly
   this quantity.

## 9. What the power analysis must show (delivered by `code/power_analysis.py`)

Given the empirical scales — operator floors from 2026ax in the .0034–.057 range
(1 − cosine at cohort level; operator-attributable variance .0072–.0142), H13
inter-version distances below .03 (cosines > .97) — the simulation must report, for the
panel design (n brands × m artifacts × k operator pairs × the version ladder), the
minimum detectable version-drift magnitude at S/N > 2 against the contemporaneous
operator floor under the source-cluster bootstrap, and the power of the H3 two-set
contrast at plausible effect sizes. Design conclusion feeds PL1 (panel size confirmed
at 40 brands × 4 artifacts) and the paper's Methods.

## References (grounding; all substrate-registered)

Novick 1966 · Widaman, Ferrer & Conger 2010 · Flake, Pek & Hehman 2017 · Flake & Fried
2020 · Gama et al. 2014 · Lu et al. 2019 · Chen, Zaharia & Zou 2024 · Nosek et al. 2018.
Corpus: 2026ax (operator floor), 2026ay (nesting/no-rescue), 2026v (H13, Experiment B),
2026ap (cross-family operators), 2026as (PRISM scaffold), 2026s (coherence types),
2026z (dynamics downstream consumer), 2026a (eight dimensions).
