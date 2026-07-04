# PRISM-C Preregistration (PL0 Specification)

Dmitry Zharnikov · ORCID 0009-0000-6893-9231 · Working Paper v1.0.0 — July 2026

**Status:** PRE-DRAFT empirical scaffold. This is the frozen PL0 layer (pre-registered
protocol) of the PRISM-C choice study; it is *not* the paper. Per the new-R-paper pre-draft
workflow, paper drafting is gated on the Grok pre-draft review + user GO; this preregistration
is the data-collection protocol that precedes drafting. Companion: `INSTRUMENT_SCAFFOLD.md`.
Substrate paper row: `prism-c`.

---

## 1. Study information

**Title.** From Stated Perception to Revealed Choice: A Pre-Registered Choice-Level Instrument
for AI Brand Perception (PRISM-C).

**Research question.** Does an LLM's *stated* eight-dimension brand perception (PRISM-B) predict
its *revealed* choice among those brands in a simulated agentic task, and how large is the
choice-perception gap — the part of choice the stated reading does not explain? As LLMs move
from describing brands to choosing them for users, perception-level measurement (Zharnikov 2026v
PRISM-B) and choice-level measurement (Sabbah & Acar 2026; Bansal et al. 2025) may diverge;
PRISM-C measures the divergence.

**Instrument.** PRISM-C, the choice member of the PRISM family, sharing the PL0–PL4 scaffold
with PRISM-B. It reuses PRISM-B for the stated reading and adds a simulated choice-task battery
at PL2 and the stated-vs-revealed alignment estimator at PL4 (`INSTRUMENT_SCAFFOLD.md`).

**Confirmatory–exploratory boundary.** Everything in this PL0 document is confirmatory.
Unspecified analyses are exploratory and reported as such (Nosek et al. 2018; Flake & Fried 2020).

## 2. Hypotheses

- **H1 (choice-perception gap exists).** The model's revealed choice among a brand set is not
  fully predicted by the cosine-nearest brand to the elicited *need vector* under the stated
  eight-dimension readings: there is a systematic residual (the choice-perception gap) beyond
  the operator floor. *Existence, confirmatory.*
- **H2 (dimensional predictors of choice).** A pre-registered subset of the eight dimensions
  (Economic, Experiential, Social — the pre-registered "choice-weighty" set) predicts revealed
  choice incrementally over the others: choice weights the dimensions unequally, and the weighting
  is estimable. *Directional, confirmatory.*
- **H3 (position/order bias is controlled, not confounding).** After counterbalancing choice-set
  order and option position (the first-proposal / position biases documented by Bansal et al.
  2025; Allouah et al. 2025), the stated→revealed relationship survives — the gap is a perception
  phenomenon, not an artifact of presentation order. *Robustness, confirmatory.*

H1 and H2 are primary. Failure of H1 → stated perception fully predicts choice (perception
measurement carries cleanly to agentic behavior — a strong, useful null). Failure of H3 → the
apparent gap is a position-bias artifact (interpretation in §7).

## 3. Design

Discrete-choice design over pre-registered brand choice-sets, paired with PRISM-B stated
readings.

- **Stated reading.** Run PRISM-B on every brand in the choice-set bank under cross-family
  operator pairs; record the eight-dimension vector + operator floor per brand.
- **Choice task.** For each of ≥ 40 pre-registered need-scenarios, present a choice-set of 3–5
  brands and elicit the model's pick (and a ranked order), under counterbalanced option position
  and choice-set order, across cross-family operators.
- **Analysis.** The gap between the cosine-predicted pick (from the stated readings + the elicited
  need vector) and the revealed pick (H1); the dimensional choice-weight model (H2); the
  position/order-bias robustness check (H3).

## 4. Variables

- **Stated reading.** The eight-dimension PRISM-B brand vector (2026ax); the need vector is the
  same eight-dimension elicitation applied to the scenario's stated need.
- **Revealed choice.** The model's pick and ranked order over the choice-set.
- **Predicted choice.** The cosine-nearest brand to the need vector under the stated readings.
- **Choice-perception gap.** The rate at which revealed ≠ predicted, beyond the operator floor,
  with a source-cluster bootstrap CI.
- **Position/order factors (H3).** Option position and choice-set order (counterbalanced).

## 5. Pre-registered comparison conditions

The gap is compared across, at minimum: (a) **choice-weighty vs other dimensions** (H2),
(b) **counterbalanced vs raw order** (H3), (c) **operator family pair** (stability of the gap).
A negative control (a choice between a brand and a near-duplicate of itself) must show no stable
pick beyond chance; a positive control (a brand dominating on every dimension) must be reliably
chosen.

## 6. Analysis plan and inference criteria

- **Gap criterion.** The revealed pick *diverges* from the predicted pick when the divergence rate
  exceeds the operator floor of the choice elicitation (dispersion of the pick across cross-family
  operators) by the pre-registered k = 2 S/N rule (2026ax) — so a "gap" is measured against choice
  noise, never asserted.
- **H1 (gap exists).** Supported if the divergence rate's source-cluster bootstrap 95% CI lower
  bound exceeds the choice operator floor at S/N > 2.
- **H2 (dimensional predictors).** A choice model (conditional logit / hierarchical) regresses
  revealed choice on the eight stated-dimension distances to the need vector; H2 supported if the
  choice-weighty subset carries incremental predictive weight (ΔLL / ΔAIC clearing a pre-set
  threshold) over the other dimensions, at p < .017.
- **H3 (bias controlled).** Position/order entered as covariates; H3 supported if the
  stated→revealed coefficient remains significant (p < .017) and materially unchanged after
  counterbalancing (coefficient shift within its CI).
- **Effect sizes mandatory** (gap rate + CI, choice-weight coefficients, ΔLL), per
  PAPER_QUALITY_STANDARDS. Exact three-digit p-values, no leading zero.

**Alpha allocation.** Family-wise α = .05 split across H1 / H2 / H3 by Bonferroni → α = .017
each. Exploratory analyses carry no protected α and are labelled exploratory.

## 7. Stopping rules, exclusions, what would change the claim

- **Stopping rule.** Collection halts at the pre-set scenario × choice-set count. No optional
  stopping; no peeking-driven extension.
- **Exclusions (pre-registered).** A choice trial with an unparseable pick is re-drawn under the
  logged retry policy; a scenario whose need vector cannot be elicited above the operator floor is
  dropped (reported). A brand read below the artifact floor is flagged.
- **What would change the claim.** H1 null → stated perception predicts choice (perception
  measurement carries to agentic behavior; the corpus can claim it). H2 uniform → choice does not
  weight dimensions unequally; the eight-dimension detail buys nothing for choice. H3 fails → the
  gap is a position-bias artifact, not a perception phenomenon.

## 8. Companion computation + transparency

The PL4 stated-vs-revealed alignment estimator + choice model (fixed seed, run command, README)
publishes under `prism-c/code/` in the public mirror at submission (PAPER_QUALITY_STANDARDS
37a–37e). Frozen PL0 (this file), PL1 counterbalancing config, and the PL2 choice-set + scenario
bank are versioned before collection; PL3 session data is append-only and immutable.

## 9. Pre-collection amendment (2026-07-02 — frozen BEFORE pilot and confirmatory collection)

This section was added after the PL0 v1.0.0 freeze but **before any pilot or confirmatory
API call**; every item below is therefore ex ante with respect to all data. It records the
final design constants, the operator-screening rule, and the pre-registered secondary
(mechanism-discriminating) analyses from `MECHANISMS.md`.

### 9.1 Design constants (locked)

- **Scenario bank:** 40 pre-registered need-scenarios; choice-sets of 3–5 brands drawn from
  a ≥ 30-brand stated-reading bank spanning the five coherence types.
- **Counterbalancing:** each (scenario, choice-set) trial is presented in **8 counterbalanced
  position arrangements** (rotations + order reversals of the option list), so per-trial
  interval criteria are estimable (an interval criterion on 4 arrangements is under-powered;
  8 is the pre-set minimum).
- **Operator set:** four cross-family operator pairs (Anthropic / OpenAI / Alibaba / DeepSeek
  families; renderer ≠ extractor family for every stated reading), and the same four families
  as choice operators ("choosers"). Pinned model IDs in `PL1_CONFIG.yaml`.
- **Power note:** 40 scenarios × 8 arrangements × 4 chooser families ≈ 1,280 confirmatory
  choice trials, within the ~1,200–1,500-trial range required to detect a 15–20 percentage-
  point gap above the operator floor at α = .017 given the position-effect sizes reported by
  Bansal et al. (2025).

### 9.2 Pre-flight operator-concordance screen (frozen exclusion rule)

Before the bank freezes, a ~50-call pilot screens every candidate operator family for
concordance. **Exclusion rule, fixed ex ante:** a family whose pilot concordance dispersion
exceeds **3× the median dispersion of the remaining families** is excluded from the operator
floor and retained only as a reported exploratory observer. The decision follows the rule
mechanically; no post-hoc judgment enters. (Rationale: a systematically discordant observer
inside the floor inflates it and can mask or manufacture the gap; the rule makes the floor's
membership itself pre-registered.)

**Pilot gate:** the choice-perception gap must be *estimable above the operator floor* on
pilot data (the floor must not consume the measurable range) before the confirmatory bank
freezes. If the gate fails, collection STOPS and the failure is reported; no confirmatory
data is collected.

### 9.3 Pre-registered secondary analyses — mechanism discrimination

`MECHANISMS.md` (authored with this amendment) nominates four candidate mechanisms for the
gap — M1 choice-time dimensional reweighting, M2 salience/position residue, M3
elicitation-frame divergence with modal-brand concentration, M4 readout garbling at the
margin — each with discriminating predictions the H2 estimator separates:

- **M1:** effective dimensionality (participation ratio) of the fitted weight vector < 8;
  divergence probability increases with the share of the predicted pick's advantage carried
  by non-choice-weighty dimensions; survives counterbalancing.
- **M2:** position/order covariates absorb the divergence (H3 fails); divergence predicted
  by the presented position of the predicted pick.
- **M3:** brand-level alternative-specific constants capture significant weight and
  correlate with category prevalence; modal-brand over-selection uniform across scenarios.
- **M4:** divergence probability decreases in the stated top-2 cosine margin; conditional on
  margin, dimensional weights add no structure; divergence vanishes for dominating options.

These are **secondary analyses**: the confirmatory core remains H1–H3 under the §6 α
allocation. Mechanism contrasts are reported with exact p-values and effect sizes at
α = .05 uncorrected, interpreted jointly as pattern evidence for/against each mechanism,
not as individual confirmatory claims.

### 9.4 Pre-registered boundary conditions + heterogeneity test

- **B1 (need-vector ambiguity):** divergence rate increases across terciles of need-vector
  flatness (entropy of the normalized need vector).
- **B2 (dominance):** divergence shrinks to the operator floor in the positive-control
  (dominating-option) region.

Both are tested as pre-registered heterogeneity contrasts (divergence rate by tercile /
region, with bootstrap CIs), reported alongside H1.

### 9.5 Unit of analysis

Effect sizes are reported at the **(scenario, choice-set) trial level**; brand-level
aggregates appear only in robustness and descriptive tables, never as the primary unit
(avoiding unit-of-analysis drift between trial-level inference and brand-level summaries).

## References (protocol)

Allouah A, Besbes O, Figueroa JD, Kanoria Y, Kumar A. What Is Your AI Agent Buying?
Evaluation, Biases, Model Dependence, and Emerging Implications for Agentic E-Commerce.
arXiv:2508.02630. 2025.

Bansal G, Hua W, Huang Z, et al. Magentic Marketplace: An Open-Source Environment for
Studying Agentic Markets. arXiv:2510.25779. 2025.

Flake JK, Fried EI. Measurement schmeasurement. *Advances in Methods and Practices in
Psychological Science*. 2020;3(4):456-465.

Nosek BA, Ebersole CR, DeHaven AC, Mellor DT. The preregistration revolution. *PNAS*.
2018;115(11):2600-2606.

Sabbah J, Acar OA. Marketing to Machines: How AI Models Respond to Promotional Cues
(the Agentyx platform). SSRN Working Paper, doi:10.2139/ssrn.6406639. 2026.

Zharnikov D. Spectral Brand Theory. 2026a. · The Brand Spectrometer. 2026ax. · Cross-Family
Operator Discipline. 2026ap. · Dimensional Collapse in AI-Mediated Search. 2026v.
