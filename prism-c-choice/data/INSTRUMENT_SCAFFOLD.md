# PRISM-C Instrument Scaffold

Dmitry Zharnikov · ORCID 0009-0000-6893-9231 · Working Paper v1.0.0 — July 2026

**Status:** PRE-DRAFT empirical scaffold (companion to `PREREGISTRATION.md`). PRISM-C is the
choice member of the PRISM family; it inherits the **PL0–PL4 scaffold** from PRISM-B, reuses
PRISM-B unchanged for the stated reading, and adds a simulated choice-task battery at PL2 and
the stated-vs-revealed alignment estimator at PL4. The eight-dimension construct and
cross-family operator discipline are shared with the Brand Spectrometer (2026ax).

> Naming note: **PL0–PL4** are the PRISM *scaffold layers*. PRISM-C's unit is the
> **(scenario, choice-set) trial**, labelled `CT-<n>`.

---

## The PL0–PL4 scaffold, instantiated for choice

| Layer | PRISM-C instantiation |
|---|---|
| **PL0 Specification** | The frozen protocol — `PREREGISTRATION.md` (H1 gap exists, H2 dimensional predictors, H3 bias controlled; the gap criterion; α allocation; stopping rules). |
| **PL1 Configuration** | Choice-set construction; counterbalanced option position and choice-set order (against the first-proposal / position biases, Bansal 2025 / Allouah 2025); cross-family operator pairs (2026ap); temperature 0 where honored; retry/redraw policy for unparseable picks. |
| **PL2 Prompts** | (a) the PRISM-B eight-dimension render+extract prompt (unchanged) for the stated readings and the need-vector elicitation; (b) the choice-elicitation prompt (pick + ranked order over the choice-set for a need scenario), with a structured JSON output schema; version tag `prism-c/v1.0.0`. |
| **PL3 Sessions** | Append-only JSONL, one record per (scenario, choice-set, position-arrangement, operator-pair): prompt, raw response, parsed pick/order, stated readings id, metadata, timestamp. Immutable; logged via the shared LLM-call logger. |
| **PL4 Analysis** | Deterministic, seeded estimator: the cosine-predicted pick (need vector vs stated readings), the revealed-pick divergence rate, the choice operator floor (pick dispersion across operators), the conditional-logit choice-weight model, the position/order robustness check — all with source-cluster bootstrap CIs. Published under `prism-c/code/`. |

## Construct

The unit is the **(scenario, choice-set) trial**. PRISM-C measures the **choice-perception gap**
— the part of the model's revealed choice that its stated eight-dimension perception does not
predict — and the **dimensional choice weights** that map stated perception to revealed choice.
Stated perception is measured perception-level (PRISM-B, "what the model says"); revealed choice
is measured choice-level ("what the model does"), the complement flagged in the PRISM family map.

## Choice-set and scenario construction (PL2 / PL1)

1. **Brand pool + stated readings.** Run PRISM-B on ≥ 30 brands across the five coherence types
   (2026s); record the eight-dimension vector + operator floor per brand.
2. **Need scenarios.** ≥ 40 pre-registered need-scenarios ("a shopper who wants X"); each need is
   itself passed through the PRISM-B elicitation to produce an eight-dimension *need vector*, so
   need and brand live in the same space.
3. **Choice-sets.** For each scenario, a 3–5-brand choice-set (mixing coherence types and price
   tiers); every set is presented in ≥ 2 counterbalanced position arrangements and choice-set
   orders to neutralize position bias.
4. **Freeze.** Version the scenario + choice-set bank as `prism-c/v1.0.0` PL2; lock before the
   confirmatory run.

## Stated-vs-revealed alignment estimator (PL4)

For each trial:

- **Predicted pick** = argmax over the choice-set of cosine( brand_reading, need_vector ) under
  the stated PRISM-B readings.
- **Revealed pick** = the model's actual pick in the choice task.
- **Gap** = the rate of (revealed ≠ predicted) across trials, measured against the **choice
  operator floor** (dispersion of the revealed pick across cross-family operators) at the k = 2
  S/N rule — so the gap is real only when it clears choice noise.

The **dimensional choice-weight model** (conditional logit) regresses the revealed choice on the
eight stated-dimension distances to the need vector, testing whether the choice-weighty subset
(Economic, Experiential, Social) carries incremental weight (H2). The position/order factors enter
as covariates for the H3 robustness check.

## Controls (PL1)

- **Negative control** — a choice between a brand and a near-duplicate of itself: no stable pick
  beyond chance, else the elicitation is manufacturing a preference from noise.
- **Positive control** — a brand dominating on every dimension for the scenario: must be reliably
  chosen, else the choice task is not tracking perception at all.

## References

Allouah A, et al. What Is Your AI Agent Buying? (ACES). arXiv:2508.02630. 2025. · Bansal G,
et al. Magentic Marketplace. arXiv:2510.25779. 2025. · Sabbah J, Acar OA. Marketing to
Machines (the Agentyx platform). SSRN 6406639. 2026.

Zharnikov D. Spectral Brand Theory. 2026a. · Coherence Type as Crisis Predictor. 2026s. · The
Brand Spectrometer. 2026ax. · Cross-Family Operator Discipline. 2026ap. · Dimensional Collapse in
AI-Mediated Search. 2026v.
