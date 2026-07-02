# From Stated Perception to Revealed Choice: A Pre-Registered Instrument for the Choice-Perception Gap in AI Brand Perception (PRISM-C)

Dmitry Zharnikov

ORCID: 0009-0000-6893-9231

DOI: [10.5281/zenodo.21128342](https://doi.org/10.5281/zenodo.21128342)

Working Paper v1.0.0 – July 2026

## Abstract

As language models move from describing brands to choosing them on users' behalf, an unexamined assumption carries the weight: that what a model says about brands predicts what it does. PRISM-C measures that assumption. The instrument elicits a model's stated eight-dimension brand readings, projects each buyer need into the same space, and compares the need-nearest predicted pick with the model's revealed pick in a simulated agentic choice task — with the divergence judged against the choice elicitation's own cross-family operator floor, so a gap is measured, never asserted. In the pre-registered campaign (40 brands, 40 scenarios, 1,144 counterbalanced trials across four model families), the families were near-unanimous with one another (mean pick unanimity .972; floor .044) yet diverged from the predicted pick on .633 of trials — fourteen times the floor. Choice weighted the stated dimensions unequally, with sign reversals; position effects appeared only when options were perceptually indistinguishable; and pre-registered contrasts ruled out presentation order and tie-breaking noise in favor of a systematic brand-level choice policy the stated profile only partially carries. Stated-perception measurement does not transfer to agentic choice for free; the wedge between them is now an instrument-measured quantity.

**Keywords:** agentic commerce, revealed preference, stated preference, brand perception, AI observers, choice modeling, measurement instrument, preregistration

---

Every brand team watching agentic commerce arrive inherits a question with real money behind it: does the profile an AI system *reports* for a brand predict which brand that system will *pick* when a user delegates the choice? The two behaviors are already measured by two disconnected literatures. Perception-level instruments elicit what models say — multi-dimensional brand readings with noise floors and controls [@zharnikov-2026ax-brand-spectrometer; @zharnikov-2026as-prism-structured-measurement]. Choice-level audits measure what agentic systems do — and find first-proposal advantages with selection rates of 60–100% [@bansal-2025-magentic-marketplace-open], position effects, choice homogeneity, and model-dependent demand concentration [@allouah-2025-ai-agent-buying], and systematic responses to promotional cues addressed to machine audiences [@sabbah-2026-marketing-machines-how]. What no instrument yet measures is the seam between them: whether stated perception predicts revealed choice within the same observer. Classical economics named the two sides long ago — preference revealed by choice [@samuelson-1938-note-pure-theory] against preference stated to an elicitor, a comparison the stated-choice-methods tradition turned into a designed measurement [@louviere-2000-stated-choice-methods]. PRISM-C transplants that comparison to the AI observer, where the *same* subject can be asked and watched at scale under a frozen protocol. Prior LLM-preference work brackets the question from outside the observer: utility-parameter elicitation tests whether a simulated agent's choices match economic theory [@horton-2023-large-language-models; @filippas-2024-large-language-models], and preference-capture studies test whether model-elicited preferences match *human* preference structure [@goli-2024-llms-capture-human-preferences]. PRISM-C poses the within-observer question neither design reaches: whether the model's stated perception predicts the same model's revealed choice.

The obstacle, as with any perception claim lacking external ground truth, is metrological. A divergence between predicted and revealed picks is meaningless until two quantities are measured: how noisy the choice elicitation itself is (models disagreeing with models on identical trials), and how well the stated space can resolve the prediction at all (the margin between candidate brands against the stated instrument's own noise). Both come from the instrument, not from assumption — the floor discipline of ground-truth-absent measurement [@zharnikov-2026ax-brand-spectrometer; @zharnikov-2026ay-substrate-floor]. Without the first floor, ordinary chooser variability masquerades as a gap; without the second, a prediction the stated instrument cannot certify gets blamed for failing.

Three contributions are claimed. First, **the choice-perception gap as an instrument-measured quantity**: a pre-registered divergence rate between the revealed pick and the pick the observer's own stated readings imply, evaluated against a measured choice operator floor with a scenario-cluster bootstrap interval, planted-positive and near-duplicate-negative controls, and a pre-flight operator screen with a mechanical exclusion rule. Second, **the dimensional choice-weight model**: a conditional-logit decomposition [@mcfadden-1974-conditional-logit-analysis] of revealed choice onto the eight stated-dimension distances [@zharnikov-2026-spectral-brand-theory-computational-framework], making "which dimensions does agentic choice actually use?" estimable — the choice-side counterpart of the perception-side dimensional collapse measured in AI search [@zharnikov-2026-dimensional-collapse-ai-mediated-search]. Third, **a mechanism-disciplined design**: four candidate accounts of the gap — choice-time dimensional reweighting, position residue, frame divergence with brand-level pull, and readout tie-noise — were nominated with discriminating predictions *before* any data collection, so the campaign separates them rather than narrating one after the fact.

The paper proceeds as follows: the gap criterion; the instrument (protocol, banks, choice battery, pilot, estimator, controls); the validity argument for AI observers; results (confirmatory, weights, position, floors, mechanisms, boundaries, robustness); alternative explanations; and discussion with limitations.

## The Gap Criterion

***The predicted pick and the divergence rate***

Let each brand $b$ in a choice-set carry a stated reading $x_b \in \mathbb{R}^8$ (the pooled eight-dimension vector from the stated instrument) and let each scenario carry a need vector $n \in \mathbb{R}^8$ elicited by the same instrument from the scenario's need text, so brand and need live in one space [@zharnikov-2026-brand-space-geometry-formal-metric]. The **predicted pick** is the cosine-nearest brand to the need vector — the choice the stated readings themselves imply under nearest-need matching. The **revealed pick** is the brand the model actually selects when presented the need and the option list. A trial **diverges** when the two differ. The **choice-perception gap** is the divergence rate over trials, and it is admitted as a finding only when it clears the **choice operator floor** — the mean pairwise disagreement rate between chooser models from different provider families on identical trials — by the pre-registered factor $k = 2$, with a scenario-cluster bootstrap interval. Unanimous choosers who all contradict the prediction are evidence about the prediction; disagreeing choosers are noise, and the floor keeps the two apart.

***Floors, not assertions***

Both halves fail informatively. If chooser families disagree among themselves, the floor rises and an apparent gap stops counting — the elicitation cannot certify a divergence it cannot reproduce across its own operators. And because the *stated* side carries its own operator floor, the margin by which the predicted pick beats the runner-up is itself a measured quantity: a prediction whose margin sits below the stated floor is flagged as sub-resolution rather than treated as a confident forecast that choice then "violates." This double bookkeeping matters to the interpretation, and Results returns to it.

## The Instrument

***Pre-registered protocol***

PRISM-C ran under a frozen protocol [@nosek-2018-the-preregistration-revolution] with questionable-measurement safeguards [@flake-2020-measurement-schmeasurement-questionable] and an explicit confirmatory–exploratory boundary. Three hypotheses were pre-registered: H1 (existence) — the divergence rate's bootstrap 95% CI lower bound exceeds $k = 2$ times the choice operator floor; H2 (dimensional weighting) — a pre-registered "choice-weighty" subset (Economic, Experiential, Social) carries incremental predictive weight in a conditional-logit choice model (likelihood-ratio test at $\alpha = .017$); H3 (robustness to presentation) — the stated-to-revealed coefficient survives position counterbalancing (significant at $\alpha = .017$, shift within its CI). Family-wise $\alpha = .05$ was Bonferroni-split across the three. A pre-collection amendment, frozen before any pilot or confirmatory call, fixed the design constants (40 scenarios, eight counterbalanced arrangements, four chooser families), a mechanical operator-exclusion rule, four candidate mechanisms with discriminating secondary contrasts, and two boundary-condition tests — the mechanism battery is ex ante, not a post-hoc narration: every discriminating prediction in Table 4 predates the first API call. Everything outside the protocol is labelled exploratory.

***Scenario bank and need vectors***

The brand pool reuses, unchanged and frozen, the 40-brand stratified bank of the sibling metamerism campaign [@zharnikov-2026az-prism-m-metamerism]: a named public brand index stratified by the five coherence types [@zharnikov-2026-coherence-type-as-crisis-predictor] crossed with market orientation. Forty pre-registered need scenarios (20 consumer, 20 business) each carry a 3–5 brand choice-set from the pool, mixing coherence types and price tiers; no need text names a brand. Each scenario's need is rendered as ideal-brand prose (the renderer is forbidden to name or allude to any real brand) and extracted with the unchanged stated-instrument extractor, yielding the need vector. Stated readings for all 40 brands come through four standardized public-artifact channels under cross-family renderer–extractor operator pairs — renderer and extractor families never coincide [@zharnikov-2026ap-same-meaning-different-prose] — following the direct-elicitation, model-as-subject paradigm [@horton-2023-large-language-models; @filippas-2024-large-language-models].

***The choice battery***

For each (scenario, choice-set) trial, one chooser model per family receives the need and the option list as numbered "Brand — category" lines (nominative reference only) and returns a structured pick and ranking. Position is counterbalanced by a deterministic rotation scheme — the $n$ rotations of the base order (each option once in first position) plus rotations of the reversed order — giving eight arrangements for four- and five-option sets and the full six for three-option sets, per the power lesson of the sibling campaign that four channels under-power strict interval criteria. Every trial is an independent stateless call, so cross-set order carryover is removed by construction and option position is the operative presentation factor. **Table 1** pins the operators.

**Table 1: Cross-Family Operators (Pinned Model Versions).**

| Role | Anthropic | OpenAI | Alibaba | DeepSeek |
|------|-----------|--------|---------|----------|
| Stated renderer | claude-opus-4-8 (OP1) | gpt-5.5-2026-04-23 (OP2) | qwen3.7-max-2026-06-08 (OP3) | deepseek-v4-pro (OP4) |
| Stated extractor | claude-haiku-4-5-20251001 (OP2) | gpt-5.4-mini-2026-03-17 (OP1) | qwen3.6-flash-2026-04-16 (OP4) | deepseek-v4-flash (OP3) |
| Chooser | claude-opus-4-8 | gpt-5.5-2026-04-23 | qwen3.7-max-2026-06-08 | deepseek-v4-pro |

*Notes*: OP1–OP4 are the stated-reading renderer→extractor pairs; renderer and extractor families never coincide within a pair. Choosers are one model per family. Temperature 0 where the provider honors it; operator IDs are exact model-version strings verified available at collection.

***The pre-flight pilot***

Before the banks froze, a 56-call pilot screened every operator with a rule fixed ex ante: any family or pair whose concordance dispersion exceeds three times the median of the remaining units is excluded from the floor and retained only as a reported exploratory observer. The four chooser families were fully unanimous on all 40 pilot trials (discordance .000; floor .000). On the stated side, one pair's leave-one-out vector discordance (.0146) exceeded three times the median of the others (.0036): the deepseek-v4-pro renderer — an independent replication, on a new instrument, of the discordant-renderer localization the sibling campaign reported [@zharnikov-2026az-prism-m-metamerism]. The rule excluded that pair from the stated floor mechanically; its readings were still collected and analyzed separately. The pilot gate (post-exclusion choice floor at most .25) passed at .000, and the banks froze.

***The estimator and controls***

The analysis layer is a deterministic, seeded estimator: pooled stated vectors and per-brand floors (maximum pairwise cosine distance among per-pair vectors), need vectors and floors, predicted picks and margins, the divergence rate against the choice floor with a scenario-cluster bootstrap (2,000 replicates; clusters respect non-independence of trials sharing a scenario, per cluster-robust practice [@mackinnon-2023-cluster-robust-inference; @cheung-2023-diy-bootstrapping]), the conditional-logit weight model with likelihood-ratio tests, position-covariate and brand-intercept variants, and logistic mechanism contrasts. Two controls were pre-registered and collected: a **positive control** — five sets where one brand dominates the need among low-fit alternatives, which must be reliably chosen — and a **negative control** — five fictional near-duplicate twin pairs with identical one-line descriptions, which must show no stable preference beyond chance, and whose per-position pick rates double as a position-bias calibration. A 23-test unit suite, including both controls and weight-recovery tests on synthetic data with known weights, ran before any API spend.

## The AI-Observer Surface

The stated readings and the choices under test are produced by AI systems and consumed as produced by agentic surfaces: assistants that pick, carts that fill themselves. For claims about that surface, the AI observer is the measurement construct, not a proxy for a human panel — the same construct claim the sibling instruments state explicitly [@zharnikov-2026ax-brand-spectrometer], inverting the usual direction of the LLM-measurement validity literature, where models are validated against human gold standards because humans are the construct [@rathje-2024-gpt-effective-multilingual; @trott-2024-augment-psycholinguistic-datasets; @abdurahman-2024-perils-opportunities-llms]. The moment a claim extends to *human* stated-versus-revealed behavior, human subjects become mandatory; within this paper, every claim is about the AI-observer surface, in the agentic-commerce setting where that surface increasingly does the choosing [@zharnikov-2026-ai-native-brand-identity-from; @debruyn-2020-artificial-intelligence-marketing-pitfalls].

## Results

***Confirmatory results***

The campaign collected 2,104 parsed records with zero malformed after the redraw policy — 160 stated readings per operator pair, 40 need vectors per pair, 1,144 confirmatory choice trials, 160 control trials — from 2,981 logged calls. **Table 2** summarizes the confirmatory verdicts. The four chooser families were nearly unanimous with one another: mean within-scenario pick unanimity .972, choice operator floor .0437. Against that floor, the revealed pick diverged from the predicted pick on .633 of trials (724/1,144; per-family rates .619–.640), signal-to-noise 14.48, bootstrap 95% CI [.483, .779] — the lower bound clears the pre-registered criterion ($2 \times .0437 = .087$) more than five-fold. H1 is supported: the choice-perception gap exists, and it is not marginal. Both controls behaved — the dominating option was chosen on 120 of 120 positive-control trials, and no twin pair showed a stable preference (all per-set two-sided binomial $p \geq .070$).

**Table 2: Confirmatory Results at the Pre-Registered Criteria.**

| Quantity | Value |
|----------|-------|
| Confirmatory choice trials | 1,144 |
| Mean within-scenario pick unanimity | .972 |
| Choice operator floor | .0437 |
| Divergence rate (revealed ≠ predicted) | .633 (724/1,144) |
| Signal-to-noise (rate / floor) | 14.48 |
| Bootstrap 95% CI of the rate | [.483, .779] |
| H1 (gap exists, CI lower bound > 2 × floor) | supported |
| H2 (choice-weighty set, LR(3) = 204.86) | supported, p < .001 |
| H3 (survives counterbalancing, γ p = .011) | supported |
| Positive control (dominant picked) | passed (120/120) |
| Negative control (no stable twin preference) | passed (all p ≥ .070) |

*Notes*: Floor = mean pairwise disagreement rate between chooser families on identical (scenario, arrangement) trials. Bootstrap = scenario-cluster percentile, 2,000 replicates, fixed seed. α = .017 per confirmatory hypothesis (Bonferroni).

***The dimensional choice-weight model***

The conditional logit regresses each trial's revealed choice on the eight per-dimension stated distances between brand and need. Dropping the pre-registered choice-weighty set (Economic, Experiential, Social) costs a likelihood ratio of 204.86 on 3 df ($p < .001$; $\Delta$LL = 102.4; $\Delta$AIC = 198.9), so H2 is supported: choice weights the dimensions unequally, and the weighting is estimable (full-model McFadden pseudo-$R^2$ = .125). **Table 3** reports the weights. The structure is more interesting than a smooth reweighting: Ideological, Economic, Social, and Temporal proximity predict being chosen, while Experiential and Cultural proximity predict *not* being chosen — sign reversals in which the consensus favorite is typically *farther* from the need on those dimensions. The weight vector's effective dimensionality (participation ratio) is 5.95 of 8: compressed, but far from a collapse onto the three-dimension weighty set alone.

**Table 3: Dimensional Choice Weights (Conditional Logit on Negative Stated Distances).**

| Dimension | Weight | SE | | Dimension | Weight | SE |
|-----------|--------|----|----|-----------|--------|----|
| Ideological | 8.47 | 1.16 | | Semiotic | −3.51 | .82 |
| Economic | 5.86 | .71 | | Narrative | −1.07 | 1.85 |
| Social | 5.18 | 1.11 | | Experiential | −11.07 | 1.11 |
| Temporal | 2.99 | 1.14 | | Cultural | −12.08 | 1.02 |

*Notes*: Positive weight = stated proximity to the need on that dimension predicts being chosen; negative = stated proximity predicts being passed over. Choice-weighty set in the pre-registration: Economic, Experiential, Social. LR test of the weighty set: 204.86, df = 3, p < .001. McFadden pseudo-R² = .125.

***Position and order***

H3 is supported: with position covariates entered, the stated-to-revealed coefficient is essentially unmoved (γ = 39.21, SE = 15.45, $p$ = .011; shift from the uncounterbalanced estimate under .005 SE), and the position coefficients on real-brand trials are indistinguishable from zero (first-position β = −.010, SE = .113). The negative control shows where position bias actually lives: on the perceptually indistinguishable twins, first-position pick rates ran .625–.875 — the first-proposal advantage of the audit literature [@bansal-2025-magentic-marketplace-open; @allouah-2025-ai-agent-buying] at full strength. The refinement the calibration adds: in this design, position governed the pick only where perception had nothing to distinguish; given real brands, position effects vanished into unanimity.

***What the floors measured***

The stated side carries its own verdict. Per-brand stated floors ran .0011–.0173 (median .0028) over the kept operator triplet; need-vector floors ran .0018–.0733 (median .0096). Against those floors, the predicted pick's top-2 cosine margin — median .0010, maximum .0074 — sits *below* the median stated floor: for most contested scenarios, the stated readings cannot certify which brand is nearest the need. Prominent brands' readings compress into a narrow high-intensity band (the compression the sibling campaign flagged as positivity compression [@zharnikov-2026az-prism-m-metamerism]), so nearest-need prediction is noise-dominated even while revealed choice separates the same options decisively — unanimously, in most scenarios. The gap is therefore two wedges at once: dimensions choice weights differently, and distinctions the stated space cannot resolve at all.

***What the gap looks like***

At the scenario level the gap is all-or-nothing: in 25 of 40 scenarios the families' unanimous consensus pick differs from the predicted pick. The divergent picks read as informed category judgments, not noise. A quick, affordable family dinner is predicted (by nearest-need matching over stated readings) to a premium wellness grocer — every chooser picks the fast-food chain. A public-listing mandate is predicted to a payments-infrastructure firm — every chooser picks the investment bank. A video-meeting standardization is predicted to a networking-hardware vendor — every chooser picks the video platform. The choosers behave like competent agents; it is the stated-space predictor that fails to carry the need into the choice.

***Mechanisms***

Four candidate accounts were nominated before collection, each with a discriminating prediction; **Table 4** reports the verdicts. Presentation-order residue (M2) is ruled out: divergence is unrelated to the predicted pick's presented position ($p$ = .672), position betas are null on real brands, and H3 holds. Readout tie-noise (M4) is ruled out: divergence is unrelated to the stated top-2 margin ($p$ = .628) — as the compression account predicts, since nearly all margins are sub-floor — and divergence in the dominance region is .000 (0/120). Decision-subspace reweighting (M1) is partially supported: the weights are unequal with effective dimensionality 5.95, but divergence is not concentrated where non-weighty dimensions carry the prediction ($p$ = .755). The surviving account is the frame-divergence/brand-policy mechanism (M3): brand intercepts added to the dimensional model absorb a likelihood ratio of 2,204 on 38 df — reported as a diagnostic magnitude, since near-unanimous picks create complete separation — while the intercepts' correlation with index-membership prominence is not significant (Spearman ρ = −.263, $p$ = .111). The choosers share a systematic, brand-level choice policy that tracks category fit rather than raw prominence, and the eight-dimension stated reading carries only part of it.

A post-hoc theoretical reading — offered as interpretation, not as a tested claim — makes the signature pattern legible. The sign reversals are what an *objective mismatch* would produce: descriptive pretraining rewards accurate portrayal of a brand's cultural and experiential richness, while assistant alignment rewards picking whatever serves the stated need, deprioritizing exactly the dimensions that make a brand describable rather than suitable. And the brand-intercept fit is what a *representational mismatch* would produce: stated readings probe a description-shaped representation, while choice runs a decision policy over brand knowledge the eight-dimension projection only partially spans. Both readings are candidate generative processes for the measured gap, and both are directly probeable — the frame ablation and the logged-rationale probe designated below discriminate them.

**Table 4: Pre-Registered Mechanism Battery (Secondary Analyses).**

| Mechanism | Discriminating signature | Result | Verdict |
|-----------|--------------------------|--------|---------|
| M1 dimensional reweighting | Unequal weights; divergence tracks non-weighty advantage | LR p < .001; eff. dim. 5.95; tracking p = .755 | partial |
| M2 position residue | Divergence tracks predicted pick's position; H3 fails | p = .672; H3 holds; real-brand position betas null | ruled out |
| M3 brand-level policy | Brand intercepts absorb fit; modal-brand pull | LR 2,204 (38 df, separation caveat); prominence ρ = −.263, p = .111 | supported (fit-tracking) |
| M4 margin tie-noise | Divergence falls with top-2 margin; vanishes under dominance | margin p = .628; dominance divergence .000 | ruled out |

*Notes*: Secondary analyses per the pre-collection amendment; α = .05 uncorrected, interpreted jointly as pattern evidence. Separation caveat: with near-unanimous picks some brands are never chosen given the features, so the brand-intercept LR is a diagnostic magnitude, not a calibrated test.

***Boundary conditions and robustness***

One pre-registered boundary prediction failed and one held. B1 — the gap widens with need ambiguity — is not supported: divergence across need-entropy terciles is non-monotone (.640 low, .800 mid, .435 high), with the most ambiguous needs showing the *least* divergence. A post-hoc reading, flagged as such: a flat need vector discriminates weakly among brands for the *predictor* too, so the cosine pick drifts toward the category's modal-fit brand — the same brand the choosers' policy favors — and the two sides agree more often precisely where neither is being asked to make a fine distinction. B2 — the gap vanishes for dominating options — held exactly (.000 in the dominance region), bounding the phenomenon to contested choice-sets. The H1 verdict itself is threshold- and metric-invariant: supported at $k$ = 1.5, 2, and 3; under Euclidean (rate .707) and Mahalanobis (.728) predicted-pick alternates (which change 11 and 17 of 40 predictions); and with the excluded operator pair re-included in the stated pool (.756, 10 predictions change). Every alternate diverges *more* — the reported configuration is the most conservative. On the choice side, per-family divergence spans .619–.640 and leave-one-family-out floors span .0385–.0501: no single family drives the gap or the floor.

## Alternative Explanations

Three rivals deserve explicit treatment. First, *the straw-man predictor*: nearest-need cosine matching is a deliberately naive readout. It is also the pre-registered null predictor the stated instrument implies, and the answer does not rescue stated readings: the *fitted* choice-weight model — the best linear stated-perception predictor available to the data — still explains only McFadden .125 of choice, and every alternate distance metric widens the gap. Second, *invalid need vectors*: the need elicitation is one construction of the need, and its floors are the loosest in the design. But four independent model families given the same need text produce near-unanimous, facially sensible picks — the need text carries decision-relevant information; it is the projection into the eight-dimension space that loses it, which is the finding rather than a confound. Third, *choosers just pick the famous brand*: brand-level intercepts do absorb large fit, but their correlation with index-membership prominence is not significant, and the positive control shows choosers reliably picking an unglamorous dominating option over famous low-fit alternatives. The brand policy tracks fit, not fame.

## Discussion

***What a consumer of an AI-visibility score can now ask***

The practitioner translation is direct. To anyone selling or buying an "AI visibility" or "share of model" score built from stated elicitations: *does your score predict what the model picks?* — is now an answerable question, with a floor, controls, and a pre-registered protocol to answer it under. The campaign's answer for naive nearest-need consumption of stated readings is bracing: .633 divergence against a .044 floor, with the fitted dimensional model recovering only an eighth of choice variance. The stated reading is not meaningless — the single-index stated-to-revealed coefficient is significant, the weighty dimensions carry real weight — but it is a minority input into a choice policy these four model families share at this epoch and the profile does not fully expose. Perception-level measurement earns its place as an input to choice prediction, not a substitute for measuring choice [@zharnikov-2026as-prism-structured-measurement].

***The bias literature, refined***

The audit literature's position effects [@bansal-2025-magentic-marketplace-open; @allouah-2025-ai-agent-buying] appear here too — but only where perception is absent. The twin calibration reproduces first-position pick rates up to .875 on indistinguishable options; the same choosers on real brands show position betas indistinguishable from zero and .972 unanimity. The homogeneity finding also replicates and sharpens: four provider families act as nearly one chooser at the brand level, which is simultaneously reassuring for reproducibility and sobering for market dynamics — a shared choice policy concentrates demand wherever it points [@allouah-2025-ai-agent-buying]. And the choice-side sign reversals give the perception-side collapse literature [@zharnikov-2026-dimensional-collapse-ai-mediated-search] a counterpart: the dimensions a surface reports most fluently are not the dimensions its choices reward.

## Limitations

Five limitations bound the claims. First, **single epoch, pinned operators**: the unanimity of choosers and the discordance of one stated-side renderer are properties of these model versions at this date; drift is a separate instrument's province. Second, **simulated elicitation under a single choice frame**: choices are elicited under one controlled assistant frame with nominative option lists, not harvested from deployed agentic checkouts — the same boundary, accepted for the same control-and-reproducibility reasons, as the simulated choice-audit environments — and the frame-sensitivity of the gap (the M3 account's natural next probe) is untested here; a frame ablation is the designated protocol extension. Third, **the gap is predictor-relative**, and part of it is stated-space compression rather than choice-side reweighting: with median predicted-pick margins below the stated floor, anchor-calibrated extraction is the designated protocol remedy before the stated space is blamed alone. Fourth, **bank-relative and English-only**: 40 brands from one index frame, 40 authored scenarios, English prompts; the rate is a property of the (bank, predictor, operator set) triple. Fifth, **the brand-intercept diagnostic suffers complete separation** under near-unanimous choice and is reported as magnitude, not test; regularized or hierarchical brand-intercept estimation is the designated remedy when the diagnostic is promoted to a calibrated model.

## Companion Computation Script

All reported numbers reproduce from the seeded estimator and campaign scripts published with the paper: the pilot with its mechanical exclusion rule, the sharded collection harness (stated readings, need vectors, choice battery, controls), and the deterministic estimator (fixed seed 20260702; predicted picks, floors, divergence and bootstrap intervals, conditional-logit models, mechanism contrasts, boundary tests, robustness battery), with a 23-test unit suite (including both pre-registered controls and weight-recovery tests) that ran before any data collection. The estimator's entry point is `estimator.py --records <records> --exclude-ops OP4 --out <results> --robustness`; run commands are documented in the code README.

## Data and Code Availability

The frozen protocol layers (preregistration with its pre-collection amendment, instrument configuration, scenario and choice-set bank, the reused brand bank), the parsed measurement and choice records, the pilot report, the analysis outputs, and all computation code are published in the paper's public repository at https://github.com/spectralbranding/sbt-papers/tree/main/prism-c-choice; the complete append-only call logs (one record per model API call: prompts, parameters, responses), together with the protocol layers and records, are archived as a Hugging Face dataset at https://huggingface.co/datasets/spectralbranding/prism-c-choice (DOI 10.57967/hf/9397). The campaign comprised 2,981 logged model API calls (pilot: 56; confirmatory and controls: 2,925 including redraws) at an estimated total cost of 19.90 USD. The paper is archived under concept DOI 10.5281/zenodo.21128342 (this version: 10.5281/zenodo.21128343).

## Acknowledgments

AI assistants (Claude Fable 5, Grok 4.1) were used for initial literature search, for software development — authoring the experiment harness and the analysis and scoring scripts — and for orchestrating and running the reported experiments through those scripts, as well as for editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility. The rendering, extraction, and chooser models named in Table 1 served as the measurement instrument's operators — study apparatus, not authorship assistance — and their outputs constitute the dataset of record.

## Author Contributions (CRediT)

Dmitry Zharnikov: Conceptualization, Data curation, Formal analysis, Funding acquisition, Investigation, Methodology, Project administration, Resources, Software, Supervision, Validation, Writing — original draft, Writing — review and editing.

## References

::: {#refs}
:::
