<!-- PUBLIC COPY of the frozen pre-registration. Two administrative redactions relative to the internal frozen original (whose SHA-256 is recorded in FREEZE_RECORD.md): R1 the frontmatter status line (internal workflow reference) was replaced by a neutral frozen-status line; R2 one internal repository path was rewritten repository-relative. All design, instrument, floor, and analysis content is verbatim. -->
---
title: "Pre-Registered Study Design — Perception Sets the Matrix"
paper_slug: perception-sets-matrix
status: FROZEN at design freeze 2026-07-12 (checksummed in FREEZE_RECORD.md); no calls fired before freeze
date: 2026-07-12
design_template: PRISM family (2026az/2026ba/2026bb/2026bd) — pre-registered instrument, frozen decision rules, operator floors, JSONL logging
---

# Pre-Registered Study Design

Design status: **pre-freeze draft**. This document becomes the frozen
pre-registration at GO (checksummed, then never edited — amendments go to an
append-only AMENDMENTS section per PRISM practice). No API calls are fired
before freeze.

Boundary reminder (HARD): the choice-propensity elicitation below is a **study
instrument** for this paper. It is not, and must never be described as, a Brand
Spectrometer capability (the Spectrometer's claim stays perception + valence).

---

## 1. Design overview

Two studies, one linking model.

| | Study 1 — causal core | Study 2 — real-brand replication |
|---|---|---|
| Brands | Synthetic within-category stimuli, 8-D profiles manipulated by design | 2 real categories × 5 real brands |
| Match m(c,b) | Set experimentally (profile grid) | Measured in-study (reading operators) |
| Inference | Experimental monotone-link test | Observational replication |
| Role | Identification | External validity |

The canonical five cross-category profiles (Hermès, IKEA, Patagonia, Erewhon,
Tesla) are NOT used anywhere in this design. (Pre-freeze correction
2026-07-12: they were initially slated as calibration references for a
known-profile recovery floor, but the corpus's own record — 2026d Table 5
notes and its stated limitation — establishes those vectors as ILLUSTRATIVE,
chosen to reflect qualitative case-study assessments, not derived from
empirical measurement. Author-assigned numbers cannot serve as measurement
ground truth. The known-profile recovery floor is therefore grounded in the
Study-1 authored pack targets instead, which are ground truth by
construction.)

## 2. Units, cohorts, and the pseudo-replication guard

- **Unit of analysis: the cohort×brand cell.** All primary inference is at
  cohort level. Within-cell replicate calls estimate instrument noise; they are
  never treated as independent respondents (signal-source clustering discipline;
  no individual-consumer claims).
- **Cohorts:** K = 10 cohort persona specifications per category, written as
  observer spectral profiles (8-vectors + a short natural-language persona
  rendering of that profile). Profiles chosen by space-filling design (maximin
  Latin hypercube over [1,10]^8, then rounded to .5) so that match values span
  their range rather than clustering. Each cohort spec additionally carries a
  **per-dimension salience weight vector** w_c (normalized to sum 1; assigned
  with the space-filling design and rendered into the persona text), used by
  the salience-weighted match variant and the auxiliary mechanism test (§7.3). Persona renderings are fully translated
  where a non-English category market is used (native-language prompt standard).
- **Hivemind caveat:** LLM cohort respondents risk variance collapse (artificial-
  hivemind line, Jiang et al. 2025). The space-filling profile design plus the
  operator-diversity requirement (§5) are the mitigations; residual homogeneity
  is reported, not hidden.

## 3. Brand stimuli

- **Study 1:** one fictional category (specialty coffee roasters — corpus
  precedent: the Spectra Coffee demo materials) with B = 6 synthetic brands.
  Each brand = a stimulus pack (short positioning page + 3 artifact snippets)
  authored to a TARGET 8-D profile on a grid spanning match distances to the
  cohort set. Stimulus-pack authoring is itself validated: reading operators
  must recover the target profiles within tolerance (§6 floor F3) BEFORE the
  propensity arm runs; packs failing recovery are re-authored (logged).
- **Study 2 (FIXED AT FREEZE 2026-07-12):** two real categories, 5 brands
  each, chosen for (a) genuine consideration-set membership, (b)
  public-artifact richness, (c) expected profile dispersion:
  - Quick-service coffee chains: Starbucks, Dunkin', Tim Hortons,
    Peet's Coffee, Blue Bottle Coffee.
  - Athletic footwear: Nike, Adidas, New Balance, Hoka, Asics.
  Study-2 readings are ELICITED (the operator's internalized public-artifact
  exposure, PRISM-M elicited mode), English-language market.

## 4. Elicitation instruments (two, strictly separated)

**4a. Perception reading (match side).** Standard eight-dimension reading of
each brand stimulus by READING operator instances: 8-vector on [1,10], canonical
dimension order (Semiotic, Narrative, Ideological, Experiential, Social,
Economic, Cultural, Temporal). Study 1 reads stimulus packs; Study 2 reads
public-artifact bundles. Readings are cohort-UNCONDITIONED for the brand profile
β_b (the brand's profile is an object-level measurement) and cohort-conditioned
only for the cohort's own profile θ_c validation.

**4b. Choice-propensity elicitation (propensity side).** ELICITING operator
instances receive: cohort persona spec + the category consideration set
(brand stimulus packs / artifact bundles, same materials as 4a) and produce:
1. **Primary: constant-sum allocation** — "of the next 10 category purchases
   this cohort makes, how many go to each brand" (sums to 10; sum-check floor).
2. **Secondary: per-brand 11-point purchase-probability scale** (Juster-style,
   0–10 verbal-anchored) — calibration cross-check on the constant-sum shares.
3. **Switching probe (descriptive only):** "cohort's current brand is X; next
   purchase probabilities over the set" — feeds the induced-matrix illustration,
   not the primary test.

**4c. Instrument separation (HARD, the K3 guard).**
- Reading calls and eliciting calls: disjoint operator instances, separate
  sessions, no shared conversational context. The ONLY shared input is the
  persona spec text and the stimulus materials.
- The match statistic m(c,b) entering the primary test is computed from 4a
  readings; the propensity p(c,b) from 4b. A single generation can therefore
  never manufacture the correlation.
- **Same-call contrast arm (deliberate):** a parallel condition where one call
  produces both reading and propensity. Pre-registered use: estimate
  common-method inflation Δτ = τ_same-call − τ_separated. If the separated-arm
  link is null while the same-call link is positive → kill condition K3.

## 5. Operators, floors, demotion

- **Operator pool (PINNED AT FREEZE 2026-07-12):** 3 model families × 2
  models = 6 primary operators; temperature 0 where the provider honors it
  (Anthropic 4.7+ and gpt-5.x: provider defaults, parameter omitted — recorded
  per call in the JSONL log):
  - OP1 claude-sonnet-5 (Anthropic), OP2 claude-haiku-4-5-20251001 (Anthropic)
  - OP3 gpt-5.5-2026-04-23 (OpenAI), OP4 gpt-5.4-mini-2026-03-17 (OpenAI)
  - OP5 deepseek-v4-pro (DeepSeek), OP6 deepseek-v4-flash (DeepSeek)
  - RESERVES (Alibaba): qwen3.7-max-2026-06-08, qwen3.6-flash-2026-04-16.
    Frozen replacement rule: a reserve substitutes a primary ONLY on hard API
    unavailability at collection (not on floor failure — floor failure is
    demotion, reported in full).
- **Arm sizes (FROZEN):** brand readings r = 3 (cohort-unconditioned);
  cohort-profile validation readings r = 1 per cohort; propensity
  elicitations r = 3 per cohort (each elicitation covers the full
  consideration set: constant-sum + Juster scale + one switching probe with
  the designated current brand rotating across replicates); same-call
  contrast arm r = 1 per cohort (one generation produces per-brand readings
  AND the constant-sum allocation; τ_same-call computed within that arm).
  Floors F1/F3 are computed from the campaign's own reading arm (no separate
  floor calls; revised pre-freeze 2026-07-12, see §1). Planned volume ≈ 198
  calls per operator ≈ 1,190 primary calls + validation gate + smoke.
- **Match-statistic constants (FROZEN):** unweighted m = 1 − d/d_max with d
  Euclidean on [1,10]^8, d_max = 9·√8; salience-weighted variant m_w = 1 −
  d_w/9 with d_w = √(Σ w_i Δ_i²), Σ w_i = 1; cosine variant = cosine
  similarity of raw vectors. Cohort salience weights w_c: seeded
  Dirichlet(1,…,1) draw per cohort, normalized (generated with the
  space-filling design, gen_design.py, seed 20260712); the top-3 salient
  dimensions are rendered into the persona text.
- **Floors (per operator, frozen; revised pre-freeze 2026-07-12 — see §1 on
  why the canonical five were removed):**
  - F1 reading test–retest: ICC(2,1) ≥ .60 on the operator's own repeated
    brand readings (r = 3), computed over brand × dimension rows with
    replicates as raters, pooled across the campaign's categories.
  - F2 propensity coherence: constant-sum check passes ≥ 95% of calls; Juster-
    scale vs constant-sum rank agreement τ ≥ .5 within operator.
  - F3 known-profile recovery (Study 1 only — the only place ground truth
    exists by construction): the operator's mean pack readings recover the
    authored Study-1 target profiles within mean absolute deviation ≤ 1.5
    scale points per dimension, averaged over packs.
  - F4 refusal/malform rate ≤ 5%.
- **Demotion rule:** an operator failing any floor is excluded from the primary
  pool (reported in full); if > half the pool fails → kill condition K4
  (negative methods result, published per the transparency standard).
- **Logging:** every call JSONL-logged (prompt, params, raw response, parse,
  timestamps, model ID) per the professional-logging standard; logs published
  with the mirror (LLM-call JSONL discipline of the public-mirror standard).

## 6. Sample-size logic

Cells per category×operator: 10 cohorts × 6 brands (Study 1) = 60 cells (50 in
Study 2). Simulation-based power (fixed-seed script
`code/power_simulation.py`, seed 20260712, 1,000
simulations × 1,000 permutations, published per PAQS 37a–37e): at n = 60 cells
with the within-cohort permutation null, a true monotone association of
τ = .30 is detected at α = .05 with power .952 per operator (.910 at n = 50);
τ = .20 (the K1 floor) with power .702 per operator, .980 pooled across 4
floor-passing operators (.952 pooled at n = 50). Replicates and arm sizes as frozen in §5: ≈ 400 primary calls per category
plus per-operator calibration floors (≈ 1,280 primary calls total) — within
one operator-day at standard rate limits; long runs sandbox-OFF per the
run-robustness standard.

## 7. Frozen analysis rules

1. **Primary test:** Kendall τ_b between m(c,b) and p(c,b) over cohort×brand
   cells, per category × operator; cell values = median over replicates.
   Null: permutation (brand labels shuffled within cohort, 10,000 draws, fixed
   seed). Pooling: median τ_b across floor-passing operators; category-level
   conclusion requires pooled permutation p < .05 AND pooled τ_b ≥ .20.
   Reporting: exact p three digits (floor p < .001), τ_b as the effect size,
   no leading zeros.
2. **Direction:** pre-registered positive. A significant negative pooled link =
   falsification, not a finding to reinterpret.
3. **Secondary (all labeled secondary):** isotonic-regression R² of p on m;
   Δτ common-method inflation (4c); **auxiliary mechanism test (fluency,
   spine P5)** — Δτ_w = τ_b(salience-weighted m) − τ_b(unweighted m), computed
   per category × operator and pooled by median over floor-passing operators,
   with a permutation interval; pre-registered direction Δτ_w ≥ 0 (congruence
   on cohort-salient dimensions carries more of the link if the link is
   fluency-carried); the fluency account is unsupported if pooled Δτ_w < 0
   with permutation p < .05 in both studies (P1 itself unaffected);
   induced-matrix layer — map Study-2 pooled
   propensities to Dirichlet (S, s), form P = (I + S·1sᵀ)/(S+1), check the
   double-jeopardy diagonal ordering against observed repeat-propensity
   ordering; intermediate-band mass (share of cells with p ∈ middle tercile of
   the fitted link) as a function of cohort-profile dispersion.
4. **Robustness (frozen list, no additions post-hoc):** cosine instead of
   Euclidean match; per-dimension salience weights from cohort spec; Spearman ρ
   instead of τ_b; leave-one-brand-out; leave-one-operator-out.
5. **No optional stopping:** all cells run to completion; missing cells (API
   failure after retries) reported and excluded listwise per cell.

## 8. What this design deliberately does not claim

- No individual-consumer inference (cohort-level only).
- No behavioral validation (stated propensity only; the intentions-to-behavior
  calibration gap is a stated limitation with its own literature anchor).
- No causal claim in Study 2 (observational replication of the experimental
  Study-1 link).
- No cross-category choice modeling.
- No Brand Spectrometer capability extension.
