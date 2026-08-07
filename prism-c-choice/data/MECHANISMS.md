# PRISM-C Candidate Mechanisms for the Choice-Perception Gap

Dmitry Zharnikov · ORCID 0009-0000-6893-9231 · Working Paper v1.0.0 — July 2026

**Status:** pre-collection theory layer, authored 2026-07-02 BEFORE any pilot or
confirmatory data collection. Companion to `PREREGISTRATION.md` (PL0); the
discriminating predictions below are pre-registered as secondary analyses in the
PL0 §9 amendment. This document upgrades PRISM-C from a purely diagnostic
instrument to a mechanism-discriminating one: the same H2 choice-weight model that
estimates the dimensional weighting also separates four candidate accounts of WHY
stated perception and revealed choice diverge.

---

## The theoretical claim

The choice-perception gap, if it exists, is **structured, not noise**: the way an
LLM's revealed pick departs from its stated eight-dimension perception carries a
signature that identifies the generative process producing the departure. Four
candidate mechanisms, each with a discriminating prediction the estimator can
test, make the claim falsifiable in both directions — a gap with none of the four
signatures falsifies the structured-gap claim; no gap above the operator floor
falsifies the premise.

## M1 — Choice-time dimensional reweighting (decision-subspace collapse)

**Account.** Under choice pressure the model projects the eight-dimension stated
space onto a lower-rank decision subspace concentrated on the pre-registered
choice-weighty set (Economic, Experiential, Social). The stated reading reports
the full profile; the choice uses a compressed one. This is the choice-side
analogue of the perception-side dimensional collapse measured in AI-mediated
search (Zharnikov 2026v): there, retrieval collapses the profile the observer
*reports*; here, deciding collapses the profile the observer *uses*.

**Discriminating predictions (M1a-M1c).**
- **M1a.** The conditional-logit weight vector is unequal and concentrated: the
  choice-weighty dimensions carry incremental predictive weight (this is H2), and
  the effective dimensionality of the fitted weight vector (participation ratio
  of normalized |w|) is materially below 8.
- **M1b.** Divergence is *dimension-structured*: the probability that the
  revealed pick departs from the cosine-predicted pick increases with the share
  of the predicted pick's advantage carried by NON-choice-weighty dimensions
  (Semiotic, Narrative, Ideological, Cultural, Temporal). Gap trials concentrate
  where the discarded dimensions were doing the predicting.
- **M1c.** The gap survives counterbalancing (H3 holds) — the reweighting is a
  perception-use phenomenon, not a presentation artifact.

## M2 — Salience / position residue (presentation heuristic)

**Account.** The pick is substantially driven by presentation-order heuristics —
the first-proposal advantage (Bansal et al. 2025, selection rates of 60-100% for
first proposals) and option-position effects (Allouah et al. 2025) — rather than
by any perception at all. The "gap" would then be an artifact of where options
sit in the prompt, not of how the brand is perceived.

**Discriminating predictions (M2a-M2b).**
- **M2a.** Position/order covariates absorb the divergence: entering them
  collapses the raw-order divergence rate toward the operator floor, and the
  stated-distance coefficients shift materially (outside their counterbalanced
  CIs) between raw and counterbalanced estimates — i.e., H3 FAILS.
- **M2b.** Divergence is symmetric across dimensions (no M1b structure) but
  strongly predicted by the position of the predicted pick in the presented
  list (a predicted pick presented late diverges more).

M2 is the null-threat mechanism: it is the account on which PRISM-C's gap is not
a perception phenomenon. The counterbalanced design measures it rather than
assuming it away; if M2 carries the gap, the paper says so.

## M3 — Frame divergence with modal-brand concentration (elicitation-frame mismatch)

**Account.** The stated reading is produced under a *descriptive* frame; the
choice task invokes the model's *assistant* frame — trained preferences toward
safe, popular, default recommendations. Choices then concentrate on the
category-modal brand beyond what stated distances predict, matching the
model-dependent demand concentration documented for agentic purchases (Allouah
et al. 2025) and the instruction-frame sensitivity of promotional-cue response
(Sabbah & Acar 2026). The gap is a frame effect: what the model says under
"describe" and what it does under "act for the user" are produced by different
policies.

**Discriminating predictions (M3a-M3b).**
- **M3a.** A brand-level alternative-specific constant (ASC) added to the
  conditional logit captures significant weight: some brands are chosen above
  what any stated-dimension distance predicts, and the ASC ordering correlates
  with category prevalence (the modal-brand pull).
- **M3b.** Gap trials over-select the category-modal brand regardless of the
  need vector; the over-selection is uniform across need scenarios (unlike M1b's
  dimension-structured concentration).

## M4 — Readout garbling at the margin (argmax noise near ties)

**Account.** The pick is a 1-of-n maximal garbling of the internal reading — the
severest readout on the aggregator-severity ladder (Zharnikov 2026au; the PRISM-M
A-PICK finding). Even with equal dimensional weights and no frame effect, an
argmax readout plus operator noise produces divergence wherever the stated
margin between the top two candidates is small. The gap would then be
tie-breaking noise concentrated at close calls, not a systematic re-evaluation.

**Discriminating predictions (M4a-M4b).**
- **M4a.** Divergence probability is a decreasing function of the stated top-2
  cosine margin; conditional on the margin, the dimensional weights add no
  further structure (H2 weak or null once margin is controlled).
- **M4b.** Divergence vanishes for dominating options (the positive-control
  region) and rises toward chance as the margin approaches the stated-reading
  floor — the boundary-condition signature.

## Separability

| Signature | M1 reweighting | M2 position | M3 frame/modal | M4 margin noise |
|---|---|---|---|---|
| H2 unequal weights (choice-weighty set) | YES (M1a) | no | no | no (conditional on margin) |
| Divergence structured by non-choice-weighty advantage | YES (M1b) | no | no | no |
| Survives counterbalancing (H3) | YES | **NO** (M2a) | YES | YES |
| Position of predicted pick predicts divergence | no | YES (M2b) | no | no |
| Significant brand ASC / modal-brand pull | no | no | YES (M3a-b) | no |
| Top-2 margin predicts divergence | weak | no | no | YES (M4a) |

The mechanisms are not mutually exclusive; the secondary analyses estimate each
signature's contribution rather than crowning one winner. The confirmatory core
(H1-H3) remains as pre-registered; the mechanism contrasts are pre-registered
secondary analyses (PL0 §9).

## Boundary conditions (ex ante)

Two scope statements, pre-registered with a heterogeneity test (PL0 §9):

- **B1.** The gap widens with need-vector ambiguity: divergence rate increases
  across terciles of need-vector flatness (entropy of the normalized need
  vector). A need that pins few dimensions leaves the choice policy free to
  reweight (M1) or default to the modal brand (M3).
- **B2.** The gap shrinks to the operator floor for dominating options: when one
  brand's stated advantage is large on every dimension (positive-control
  region), all four mechanisms predict convergence — a gap that persists there
  would indicate elicitation failure, not perception structure.

## References (mechanism layer)

Allouah A, Besbes O, Figueroa JD, Kanoria Y, Kumar A. What Is Your AI Agent
Buying? Evaluation, Biases, Model Dependence, and Emerging Implications for
Agentic E-Commerce. arXiv:2508.02630. 2025.

Bansal G, Hua W, Huang Z, et al. Magentic Marketplace: An Open-Source
Environment for Studying Agentic Markets. arXiv:2510.25779. 2025.

Sabbah J, Acar OA. Marketing to Machines: How AI Models Respond to Promotional
Cues. SSRN Working Paper, doi:10.2139/ssrn.6406639. 2026.

Zharnikov D. Dimensional Collapse in AI-Mediated Search. 2026v. · The
Correspondence Principle of Brand Management. 2026au. · The Brand Spectrometer.
2026ax. · Cross-Family Operator Discipline. 2026ap.
