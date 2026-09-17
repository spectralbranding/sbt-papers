# Floor-Cleared Brand Velocity: Measuring Multi-Epoch Spectral Velocity Against the Apparatus Floor

Dmitry Zharnikov

ORCID: 0009-0000-6893-9231

DOI: [10.5281/zenodo.21192878](https://doi.org/10.5281/zenodo.21192878)

Working Paper v1.0.0 – September 2026

## Abstract

A raw multi-epoch reading change from a large language model brand instrument confounds brand motion with model-version apparatus drift: a re-measured profile may move because the brand changed or because the reader did. This paper introduces floor-cleared brand velocity, a pre-registered measurement crediting spectral velocity only when a brand's live-panel displacement across two epochs exceeds the contemporaneous apparatus floor from a byte-identical pinned panel re-read across the epoch pair. It further pre-registers a motion-drift double dissociation over a partition fixed ex ante. Forty brands were read at two epochs 77 days apart. Mean live-panel displacement of .00560 gives an aggregate ratio of 1.916 (bootstrap lower bound 1.534), so the typical brand does not clear the threshold of two, and the dissociation interaction is null on both pairs. The brand signal is positive with intervals excluding zero under both metrics. Six of 40 brands clear the floor at the pre-registered threshold, meeting HV1's existence criterion, though five sit below the .0162 minimum detectable effect and the interval rests on two operator families. No vendor version shipped inside the window, so the floor the six cleared is apparatus non-determinism rather than version drift, and the correction is demonstrated against the wrong quantity.

**Keywords:** brand velocity, longitudinal measurement, large language models, model-version drift, noise floor, preregistration, double dissociation, spectral profile

---

When a large language model reads a brand's public artifacts and returns an eight-dimension spectral profile, re-reading the same brand months later yields a different profile — and the difference is ambiguous at its root. It may record that the brand moved. It may record only that the model moved. Documented behavioral change in versioned models across releases makes the second reading unavoidable: the same prompt on the same input can return a materially different answer after a vendor update [@chen-2024-chatgpt-behavior-changing]. The problem is the measurement-instrument analogue of concept drift, where the relationship a learner has fixed shifts underneath it over time [@gama-2014-concept-drift-survey; @lu-2019-learning-concept-drift] — except that here the drift is in the reader, not the world. A kinematic calculus of perception supplies the vocabulary for motion — velocity as the first time derivative of the spectral profile — but illustrates it rather than measuring it [@zharnikov-2026z-spectral-dynamics], and a single-epoch version-robustness instrument establishes that a fixed panel re-read across versions moves, without turning that movement into a correction a longitudinal claim can use [@zharnikov-2026ba-prism-t-version-floor]. Neither a calculus of motion nor a one-time robustness check licenses the claim that a brand moved: the raw multi-epoch change confounds brand-signal change with model-version apparatus drift, and the confound is real precisely because cross-version re-reads of a fixed panel do differ.

Two of the three ingredients this requires are already in print, and the paper claims neither. The instrument-reliability literature has established that a *pinned* set of items, re-read whenever a provider, model version, precision or decoding setting changes, is the right primitive for detecting that a language-model instrument has moved [@camuffo-2026-variance-aware-llm-annotation]. Separately, a pre-registered audit of black-box observers on shared endpoints has established that the instability is not confined to version boundaries at all: byte-identical requests replayed against the same model name disagree, across four providers, with none of the metadata those providers expose predicting the floor [@zhu-2026-clean-engineering-unstable-measurement]. A model name is not a frozen instrument, and a pinned set is how you find that out.

**What is missing is the step from detection to subtraction.** The reliability literature's pinned set is a calibration instrument: it carries known labels, and when agreement degrades the prescribed response is to pause, re-baseline or roll back [@camuffo-2026-variance-aware-llm-annotation]. That is the right response for a pipeline whose annotations must stay comparable, and it is why that literature has no need of a rate — nothing it measures is supposed to change. A rate becomes necessary only when the substantive quantity is itself expected to move over calendar time, which is a tracking question rather than an annotation-reliability one. **The two literatures have no reason to meet, and that is the structural reason this crossing is open** rather than merely unvisited. The commercial brand-monitoring layer, which does track perception over calendar time, meets the confound from the other side and carries no apparatus correction whatsoever.

This paper claims the crossing and nothing on either side of it: a **second, freshly collected panel read through the same operators as the pinned one over the same epoch pair**, a rule crediting the fresh panel's displacement only where it exceeds the pinned panel's, and the result expressed as a rate over the exact interval. The nearest prior result inside the corpus is an unfloored, profile-level version-stability spot-check [@zharnikov-2026-dimensional-collapse-ai-mediated-search], which asks whether a whole profile is stable across versions rather than whether a brand's displacement over calendar time clears the contemporaneous floor. The contribution is deliberately two-sided: a design under which brands demonstrably move beyond apparatus, or, if none clears, a measured upper bound on perceptual velocity relative to instrument drift. Both are informative; neither invents motion the floor cannot support.

## Theory

***The floor-clearance rule for motion***

The instrument credits motion only when a brand's live-panel displacement between two epochs clears the contemporaneous apparatus floor for the same epoch pair. The apparatus floor is the displacement of a byte-identical pinned panel re-read across the epoch pair: because nothing in that input changes, all of its movement is apparatus. **Where a vendor release falls inside the pair, that band is a version floor, and the parent instrument names it so** [@zharnikov-2026ba-prism-t-version-floor]; where none does, the band is still real and still the thing a live displacement must beat, because a pinned model name is not a frozen instrument [@zhu-2026-clean-engineering-unstable-measurement]. The version floor is therefore the named special case of the apparatus floor, and the term is used below wherever the parent's quantity is meant. A live-panel displacement that fails to exceed this floor is not evidence of brand motion, and the rule is no-rescue — a claim that fails its floor abstains rather than being salvaged by an auxiliary argument. This is the temporal member of a nested family of noise floors already used to discipline single-epoch readings, in which the cross-family operator floor sits inside the version floor and no reading is claimed below the larger of the applicable floors [@zharnikov-2026ax-brand-spectrometer; @zharnikov-2026ay-substrate-floor; @zharnikov-2026ba-prism-t-version-floor]. Treating a fixed panel's cross-version movement as the measurement's null is the longitudinal-invariance discipline that classical measurement theory demands before any change score is interpreted: a difference is signal only against a modeled floor of instrument variation [@novick-1966-classical-test-theory; @widaman-2010-factorial-invariance-longitudinal]. The rule's own failure condition is explicit — if a displacement below the version floor were independently shown to be genuine brand signal, the clearance bar would be too strict.

***Floor-cleared velocity***

Under the clearance rule, spectral velocity is an estimable, apparatus-corrected quantity: the floor-cleared live displacement between two epochs, measured in one-minus-cosine distance on the eight-dimension manifold and reported as a rate $\lVert \Delta r \rVert / \Delta t$ over the exact capture interval. The definition inherits the velocity construct from the spectral-dynamics calculus [@zharnikov-2026z-spectral-dynamics] and the distance from the formal brand-space metric the displacement is measured in [@zharnikov-2026-brand-space-geometry-formal-metric], on the eight-dimension construct the motion lives in [@zharnikov-2026-spectral-brand-theory-computational-framework]. Because a single brand traces a single trajectory through perception space, velocity is a longitudinal quantity along that path, not an ensemble average across brands [@zharnikov-2026-non-ergodic-brand-perception-why]. Both outcomes of estimating it are informative. A displacement that clears its floor is a measured brand motion. A displacement that does not is a measured upper bound on how fast perception moves relative to apparatus drift over the cadence — a quantity no prior study reports. The estimate fails only on precision: if floor-cleared velocity cannot be resolved with a finite bootstrap confidence interval at the panel size, the claim collapses to a power problem, which the Method addresses ahead of collection.

***Why dimensions differ in version sensitivity***

The eight dimensions are not equally exposed to a version update, and the reason is a property of reading rather than a property of brands. A brand reading is produced by a model reading a fixed artifact, and discourse-comprehension theory decomposes understanding a text into two representations: a text-based representation of the propositions the surface literally states, and a knowledge-based representation the reader builds by importing prior knowledge to fill what the text leaves implicit [@kintsch-1988-construction-integration]. Inferences split the same way — text-connecting inferences that bind only what is present, versus knowledge-based elaborative inferences that draw on world knowledge [@mckoon-1992-inference-during-reading]. Mapped onto the eight-dimension readout, a dimension is artifact-anchored to the degree its reading can be taken off features literally present in one artifact, and prior-dependent to the degree it requires importing brand and world knowledge the artifact does not contain. The Semiotic, Narrative, and Experiential dimensions read primarily off the signs, story, and depicted experience present in the artifact; the Ideological, Cultural, Social, Temporal, and Economic dimensions require inferred values, cultural position, identity signalling, historical trajectory, and market tier that one artifact underdetermines.

A model-version update changes the reader's parametric priors, not the artifact. Large language models store substantial world knowledge in their parameters [@petroni-2019-language-models-knowledge-bases], and when parametric knowledge and in-context evidence diverge, outputs move with the parametric side precisely on the questions the context underdetermines [@longpre-2021-entity-knowledge-conflicts]; post-training and alignment further shift a model's expressed values and stance [@ouyang-2022-training-language-models]. On a byte-identical artifact the text-based representation is unchanged across versions, so version drift concentrates where the reading leans on parametric priors — the prior-dependent set. A real-world event does the opposite: it changes the artifacts the brand emits — new signs, new stories, new depicted experiences — which a fixed reader picks up first and most on the artifact-anchored set. The mechanism is falsifiable at its root: if apparatus drift were dimension-flat, or concentrated on the artifact-anchored set, the account would be wrong. The second epoch returned a null interaction, which is reported in Results and weighed against the account in the Discussion.

***The motion-drift double dissociation***

Crossing the two sources with the two dimension sets yields a double dissociation, stated as a prediction before any second-epoch data exist. On the pinned panel across versions, drift loads the prior-dependent set {Ideological, Cultural, Social, Temporal, Economic}; on the live panel within a version across epochs, motion loads the artifact-anchored set {Semiotic, Narrative, Experiential}. Table 1 states the partition and its comprehension basis. This joint pattern identifies brand signal from apparatus drift more strongly than either floor alone, because it does not merely ask whether the live panel moved more than the pinned panel — it asks whether the two sources move on the dimensions the mechanism assigns them. The prediction is a direct consequence of the comprehension mechanism crossed with the version-floor decomposition [@zharnikov-2026ba-prism-t-version-floor], on the eight-dimension construct [@zharnikov-2026-spectral-brand-theory-computational-framework]. It fails, by design, if the two-set by two-source interaction is null or if the loadings do not separate by set.

**Table 1.** The Dimension Partition and Its Comprehension Basis.

| Dimension | Read primarily from | Class |
|---|---|---|
| Semiotic | signs, marks, visual-verbal surface present in the artifact | artifact-anchored |
| Narrative | the story the artifact literally tells | artifact-anchored |
| Experiential | the sensory and interaction detail the artifact depicts | artifact-anchored |
| Ideological | brand values and stance inferred beyond one artifact | prior-dependent |
| Cultural | cultural positioning imported as world knowledge | prior-dependent |
| Social | in-group and identity signalling imported as social knowledge | prior-dependent |
| Temporal | brand trajectory and era the artifact omits | prior-dependent |
| Economic | market tier and position imported as market knowledge | prior-dependent |

*Notes*: The artifact-anchored set is read from features present in the text-based representation; the prior-dependent set requires the knowledge-based representation the reader builds from priors [@kintsch-1988-construction-integration; @mckoon-1992-inference-during-reading]. The partition is inherited ex ante from the parent version-floor instrument [@zharnikov-2026ba-prism-t-version-floor] and is fixed before any second-epoch data.

***Non-circularity of the partition***

The obvious rival to a clean dissociation is circularity: that the dimension partition was chosen to match the result. It was not, and the design forecloses the charge twice. The partition is fixed ex ante, inherited from the parent apparatus rather than fit to any velocity data, and it is predicted independently by the comprehension mechanism before the second epoch is collected. A dissociation whose partition is pinned before the data and derived from an outside-the-corpus micro-process is a derived identification result, not a curve fit. The rival is therefore rejected by design rather than by a post-hoc test — the strongest position from which to report an interaction, because the analysis has no freedom to relocate the sets after seeing which dimensions moved.

## Method

***Population and inclusion***

The calibrated population is public, digital, English-language artifacts of consumer and B2B brands, read by versioned major-API and open-weights model families, over real vendor releases only, with byte-identical prompts across epochs. Inclusion is by artifact class and fixed before collection; ambiguous classes are excluded by rule rather than judgment. Scoping the population and freezing the instrument before data is the measurement discipline that keeps a longitudinal claim from being assembled after the fact [@flake-2020-measurement-schmeasurement-questionable]. The panel is the 40-brand by 4-artifact frozen set established at the first epoch, with one artifact per public channel — official, press, experience, and social.

***Cadence and the relaxation timescale***

A finite-difference velocity between two epochs is well-posed only if the epoch cadence is compatible with the timescale on which perception relaxes. That timescale runs on weeks to months, so a sub-week interval would measure mostly noise, violating the well-posedness condition, while a longer interval accumulates more displacement above the version floor and raises detection power [@zharnikov-2026aw-forming-a-perception]; coherence type is a candidate moderator of the relaxation rate and is logged for later analysis [@zharnikov-2026-coherence-type-as-crisis-predictor]. The cadence is pre-registered as a range — a target window of roughly 10 to 12 weeks after the first epoch — rather than a fixed point, to fit real vendor release timing and operator availability. If a vendor ships a new model version inside the window, capture occurs at that release, which strengthens the per-pair version-floor re-estimate; otherwise capture occurs near the window midpoint. The actual interval is recorded and velocity is reported as a rate over the exact dates; there is no optional stopping on a favorable result.

***Scope of the kinematic claim***

Velocity is a local tangent quantity on the eight-dimension manifold, and the kinematic claim holds only where the perception dynamics over the observation window are smooth — no crisis-driven jumps, no dimensional-creation events, no re-collapse. Smoothness over the window is specified as a precondition to be confirmed rather than assumed: a brand that undergoes a discontinuous event during the interval violates the local-tangent reading and is treated as out of scope for the velocity estimate for that pair. The confirmation was not recorded at the second-epoch capture, and the consequence is carried in Limitations rather than resolved by assertion.

***When the dissociation fails***

The double dissociation is bounded, and its failure conditions are pre-registered rather than discovered. It holds unless a real-world event is itself value-laden or cultural — shifting the prior-dependent dimensions through the artifacts — or a model version is retrained on materially new cultural corpora, which could contaminate the artifact-anchored dimensions. A values controversy that moves Ideological or Cultural readings via fresh live artifacts is the direct test of the first condition; a version trained on new cultural material that flattens the artifact-anchored loadings is the second. Stating both in advance is what makes the dissociation falsifiable rather than a just-so story.

***Identification assumptions***

Three assumptions are made without test but are relaxable and bounded by the robustness battery. First, the version floor estimated on the pinned panel for an epoch pair is a valid upper bound on the apparatus contribution to the live-panel displacement for the same pair — the apparatus acts equivalently on pinned and live inputs. If this fails, floor subtraction under- or over-corrects the velocity, and the leave-one-operator-out and negative-control checks bound the violation. Second, for the small displacements observed over one epoch pair, the one-minus-cosine distance approximates the local tangent metric, so the finite-difference displacement is a valid velocity estimate; the distance-metric robustness check tests this. Third, cross-family operator extraction within an epoch removes format and decoding apparatus effects, so residual pinned-panel movement across versions is attributable to model priors rather than tokenizer or instruction-following changes; a dimension-flat drift signature, rather than the dimension-structured signature the mechanism predicts, would diagnose a violation.

***Distance metric***

Displacement is measured in one-minus-cosine distance on the eight-dimension reading, the formal brand-space metric [@zharnikov-2026-brand-space-geometry-formal-metric]. For the small per-pair displacements the design targets, $1-\cos$ approximates the local tangent metric, and the approximation is treated as an assumption to be probed rather than a fact, with a Euclidean-embedding re-estimate reported alongside.

***Operator control***

Each panel is read under cross-family operator pairs — a segmenter model of one family feeding a classifier model of another — so that format and decoding idiosyncrasies of any single family are absorbed rather than counted as drift. Cross-family extraction is what lets residual pinned-panel movement be attributed to model priors, and the operator floor it defines is nested inside the version floor [@zharnikov-2026ax-brand-spectrometer].

***Instrument***

The instrument is a two-panel version-floor pipeline. The eight-dimension render-and-extract prompts, byte-identical across epochs, run under the cross-family operator pairs on both the byte-identical pinned panel and the freshly re-collected live panel, at each version epoch [@zharnikov-2026ba-prism-t-version-floor]. Every call is logged append-only, one record per brand, artifact, epoch, operator pair, panel, and version, carrying the prompt, raw response, parsed eight-dimension reading, hashes, and timestamps, with cross-operator extraction kept separate. The pinned panel's SHA-256 manifest is verified before any run; a hash mismatch invalidates the isolation and aborts the capture.

***The live panel's capture rubric***

The live panel is re-collected by the rule the first epoch actually operated under, which had to be recovered from its own sealed artifacts because the extraction path was never recorded. Three parts are fixed in advance. Material is gathered until a hard 2,500-character cut binds, with trailing whitespace stripped: 127 of the first epoch's 160 cells sit at or within ten characters of that cap and 117 end mid-word, which identifies a hard cut rather than a trim at a sentence boundary, so a mid-word ending is correct and not a defect to repair. Where a source genuinely holds less, the cell ends short, as 33 first-epoch cells do. And at each epoch the selection takes **the most substantial on-brand artifact available in the channel regardless of its date**; there is no recency requirement and no lower date bound, because the first epoch had none. If the same artifact still wins at the second epoch it is used again and the cell contributes zero displacement, which is the honest reading: the channel is surfacing what it surfaced before. A cell is never swapped for a fresher one to manufacture movement.

What the live panel therefore measures is stated plainly, because it is narrower than "current discourse": it is the brand signal carried by **what each channel most substantially surfaces**, which turns over slowly in thin channels and quickly in busy ones. A small social displacement for a brand whose most substantial thread is years old is a property of the channel, not a null result about the brand.

***The two panels***

The first epoch is the anchor at which the live panel coincides with the pinned panel at birth, so velocity is undefined there. The second epoch re-reads both panels under matched operators and contemporaneous versions. The pinned panel — the frozen 40-brand by 4-artifact byte-identical set — is re-read with nothing in its input changed, so all of its inter-epoch movement is apparatus drift; this yields the version floor for the epoch pair. The live panel re-collects fresh public artifacts for the same 40 brands, one per channel, by the same capture rubric, so its inter-epoch movement is version floor plus brand signal. Both panels are read under the first-epoch version snapshots, which isolate brand signal at fixed apparatus, and under the contemporaneous current versions, which give the live-epoch version floor; the exact version identifier is logged per call. Table 2 states the go/no-go gates that must pass before velocity is computed.

**Table 2.** Pre-Registered Go/No-Go Gates for the Second Epoch.

| Gate | Pass condition | If it fails |
|---|---|---|
| Pinned integrity | second-epoch pinned SHA-256 matches the first-epoch manifest | abort and re-serve exact bytes; isolation is void otherwise |
| Panel completeness | at least .90 of the 40 brands re-collected on the live panel | proceed; drop un-recollected brands from the live comparison as a pre-registered exclusion |
| Negative control | same-version two-run displacement within the operator floor | hold and diagnose instrument noise before trusting the floor |
| Positive control | a distant-version pair exceeds the operator floor | hold; the estimator is insensitive, investigate |
| Cadence adequacy | median live displacement not swamped by the bootstrap noise band | add an intermediate epoch before claiming velocity; do not force a null |
| Power precheck | the completed power simulation shows the panel can detect the target minimum effect | expand the panel before the second epoch |

*Notes*: Gates are frozen before the second-epoch capture. A clean pass authorizes computing the velocity (HV1) and dissociation (HV3) results; any hold or abort is reported rather than worked around.

***Velocity estimator***

For each brand over the epoch pair, under matched operators, the estimator computes the version floor as the pinned inter-epoch distance for the same pair, the live displacement as the live inter-epoch distance, the signal-to-noise ratio $S/N$ as live displacement over the version floor, and the floor-cleared velocity as the live displacement with the pinned-drift component removed by vector rejection. A brand's motion clears iff the source-cluster bootstrap 95% confidence-interval lower bound of $S/N$ exceeds the pre-registered threshold, reported at a strong $k = 2$ with the existence variant at $k = 1$ alongside. Because interventions within an artifact are not independent draws, uncertainty is clustered at the source level. Effect sizes — velocity magnitude with confidence interval, $S/N$, and per-dimension deltas — are reported regardless of clearance.

***Dissociation test***

Per dimension, live motion is compared against pinned version drift as a two-set — artifact-anchored versus prior-dependent — by two-source — live versus pinned — interaction contrast, Holm-corrected, with the interaction effect size and confidence interval. The predicted pattern is live motion loading {Semiotic, Narrative, Experiential} and pinned drift loading {Ideological, Cultural, Social, Temporal, Economic}. The contrast is the confirmatory test of the double dissociation, and its partition is the ex-ante set defined in Theory, not one chosen after inspecting which dimensions moved.

***Power***

The power analysis is complete and did not require new data; only the second-epoch results are calendar-gated. Given operator floors in the .0034 to .057 range and version floors below .03, the simulation asks two questions: the minimum velocity magnitude the 40-brand by 4-artifact panel can detect at a signal-to-noise ratio above 2, and the power of the dissociation interaction at that panel size. For the velocity test, the minimum detectable velocity is .0162 one-minus-cosine units at N = 40 brands — roughly 2.5 times the aggregate version floor of about .0064 — and .0160 at N = 60, so enlarging the panel barely moves the detection bar. For the dissociation, the two-set by two-source interaction reaches power .90 at N = 40 (and .97 at N = 60) for a medium effect of Cohen's d ≈ .49, Holm-corrected. The 40-brand by 4-artifact panel therefore suffices for at least 80% power on the dissociation, and no panel expansion is required before the second epoch. The companion simulation is `power_analysis.py` (fixed seed 20260704); run commands are documented in the code README.

## Pre-Registered Hypotheses

The frozen protocol commits two confirmatory hypotheses, each with a committed publishable null.

**HV1 (floor-cleared velocity).** At least one brand's floor-cleared spectral velocity clears the contemporaneous version floor at a signal-to-noise ratio whose bootstrap confidence-interval lower bound exceeds the pre-registered threshold. The falsifier is precision or rule: if no brand clears, the result is the measured upper bound on perceptual velocity relative to apparatus drift over the cadence; if the estimate carries no finite confidence interval at the panel size, the claim fails on power; and if a below-floor displacement were independently shown to be genuine signal, the clearance rule would be too strict.

**HV3 (motion-drift dissociation).** The two-set by two-source interaction is supported, with live motion loading the artifact-anchored set and pinned drift loading the prior-dependent set. The falsifier is a null interaction or loadings that do not separate by set; a real event that is value-laden or a version retrained on new cultural corpora are the pre-registered conditions under which the dissociation is expected to fail rather than a surprise.

## Results

The second epoch was captured on 2026-09-17, the pre-registered window midpoint at eleven weeks, giving $\Delta t = 77$ days against the VE-1 anchor of 2026-07-02. The campaign returned 1,920 readings over 1,920 distinct cells with no duplicates, no malformed vectors and no flagged redraws, under a single frozen prompt version; both sealed panels re-hashed to their manifests after collection as well as before. Two operator pairs enter every cross-epoch quantity. The third was dropped in advance when its extractor left its provider's catalog, because a floor estimated under an unmatched pair would carry an operator change inside the quantity that exists to isolate a version change; the third version ladder is reported within the epoch only, for the same reason.

***Velocity***

**HV1 is supported, and it is supported narrowly.** The pre-registered rule is an existence claim: motion is credited when at least one brand's floor-cleared velocity clears the version floor at a source-cluster bootstrap lower bound above $k = 2$. Six of 40 brands clear it.

**Table 3.** Brands Clearing the Version Floor at $k = 2$.

| Brand | Live displacement | $S/N$ | Bootstrap lower bound | Own version floor | Floor-cleared velocity |
|---|---:|---:|---:|---:|---:|
| FedEx | .01592 | 5.448 | 3.678 | .00453 | .01139 |
| Slack | .01385 | 4.739 | 2.530 | .00581 | .00804 |
| Uber | .01059 | 3.623 | 2.263 | .00299 | .00760 |
| Cisco | .00872 | 2.982 | 2.876 | .01296 | .00000 |
| Ryanair | .00872 | 2.982 | 2.691 | .00441 | .00431 |
| GE | .00659 | 2.256 | 2.114 | .00246 | .00413 |

*Notes*: $S/N$ is live displacement over the pooled version floor of .00292, the quantity the pre-registered clearance rule tests. Floor-cleared velocity removes the brand's own pinned-drift component by vector rejection and is therefore governed by the right-hand column rather than by the pooled floor. Cisco's own floor exceeds its live displacement, so it clears the ratio and contributes no velocity.

Five of the six carry a positive floor-cleared velocity; Cisco clears the pooled ratio while its own version floor exceeds its displacement, so its floor-cleared velocity is exactly zero. That divergence is a property of the estimator rather than of the brand: the clearance ratio is taken against the pooled floor and the cleared velocity against the brand's own, and the two disagree wherever a brand's apparatus band is unusually wide.

**The panel as a whole does not clear, and that is not the same question.** Mean live displacement across all 40 brands is .00560 (95% CI [.00448, .00683]) against the pooled floor of .00292, giving an aggregate $S/N$ of 1.916 with a bootstrap lower bound of 1.534. Per operator pair the aggregate ratio is 1.740 (95% CI [1.215, 2.552]) and 2.322 (95% CI [1.783, 2.969]). HV1 asks whether any brand moved beyond apparatus, not whether the typical brand did; the aggregate is reported because the answer to the second question is no, and a reader should have both.

**Three things bound how much weight the clearance carries, and all three are stated rather than discovered.** First, the pre-registered interval is a source-cluster bootstrap over operator families, and only two families survive the operator drop described in Method, so the interval resolves little more than whether both operators agree — a coarse criterion, though a conservative one. Second, the per-brand interval propagates uncertainty in the numerator only, treating the pooled floor as known exactly, so it understates total uncertainty. Third, the power simulation set the minimum detectable velocity at .0162 and five of the six clearing brands sit below that figure, which indicates that the per-brand interval is narrower than the simulation's error model rather than that the effects exceed what the design could detect. The existence claim is met on its own terms; it is not a demonstration that six brands moved by a margin the panel was powered to resolve.

Expressed as a rate over $\Delta t = 77$ days, panel live displacement runs at .0000727 per day and floor-cleared velocity at .0000387 per day. Floor-cleared velocity averages .00298 across the panel with a median of .00159, and 8 of 40 brands return exactly zero. The $k = 1$ existence variant is met by 18 of 40 brands.

**The measurement stands independently of the clearance count.** The brand signal, live displacement less the version floor, is positive with a confidence interval excluding zero in all four operator-by-metric cells: .00302 (95% CI [.00101, .00531], $d = .437$) and .00234 (95% CI [.00143, .00323], $d = .761$) under one-minus-cosine, .01887 (95% CI [.00767, .03105], $d = .494$) and .02698 (95% CI [.01695, .03774], $d = .788$) under the Euclidean embedding. The live panel reliably moves more than the frozen panel read by the same apparatus over the same interval.

**Table 4.** Aggregate Floor-Clearance by Operator Pair and Distance Metric.

| Operator pair | Metric | Live displacement | Version floor | Brand signal | $S/N$ | 95% CI on $S/N$ | Aggregate clears $k = 2$ |
|---|---|---:|---:|---:|---:|---|:--:|
| Pair 1 | one-minus-cosine | .00709 | .00408 | .00302 | 1.740 | [1.215, 2.552] | no |
| Pair 1 | Euclidean | .08855 | .06967 | .01887 | 1.271 | [1.104, 1.474] | no |
| Pair 2 | one-minus-cosine | .00411 | .00177 | .00234 | 2.322 | [1.783, 2.969] | no |
| Pair 2 | Euclidean | .06925 | .04227 | .02698 | 1.638 | [1.379, 1.938] | no |

*Notes*: $n = 40$ brands per cell, $\Delta t = 77$ days. Displacements are inter-epoch distances between artifact-averaged eight-dimension readings. Brand signal is live displacement less the version floor. Intervals are seeded brand-cluster bootstraps at 2,000 resamples. This table is the panel aggregate and is not HV1's criterion, which is the per-brand existence test of Table 3. The third operator pair enters no cross-epoch quantity.

***The motion-drift dissociation***

**HV3 is not supported.** The two-set by two-source interaction is null on both operator pairs: .01192 (95% CI [−.13521, .17109], $t = .154$, $p = .439$, Holm-adjusted $p = .879$, $d = .024$) and −.08925 (95% CI [−.19546, .01793], $t = −1.568$, $p = .938$, Holm-adjusted $p = .938$, $d = −.248$). Both intervals include zero, both adjusted $p$-values sit far from any threshold, and both effect sizes are negligible to small. The signs differ across pairs — one in the predicted direction, one against it — which is the pattern of a null rather than a reversal. The pre-registered falsifier fires as written: the interaction is null, so the dissociation fails.

Whether the pre-registered boundary condition explains the failure cannot be settled here. That condition reserves a prior-dependent loading of live motion for value-laden events, and the protocol requires a smoothness check — no crisis, rebrand or dimensional-creation event inside the window — to be confirmed and recorded at capture. No such record was made, so the boundary condition is neither invoked nor excluded, and that gap is carried as a limitation rather than resolved by assertion. What the interval does establish is that the dissociation does not appear over a window in which, as the next subsection shows, there was no version drift for it to dissociate from.

***Ruling out apparatus***

The rival that live-panel motion is entirely apparatus drift is **rejected for the six clearing brands and not rejected for the other 34**. The clearance test is what settles it, and it settles it brand by brand: for FedEx, Slack, Uber, Cisco, Ryanair and GE the live panel moved beyond twice the apparatus band under both operator pairs, which is what the rival denies is possible. For the remaining brands the rival stands, and no motion is claimed for them.

A second finding bears on the rival more directly, and it was not anticipated. **Both operator pairs carry identical model identifiers at both epochs**: no vendor shipped a new version for either pin during the 77 days. The pinned panel therefore did not measure version drift over this interval, because there was none to measure; what it measured is apparatus non-determinism over elapsed time. The negative control puts a figure on how much of it: same-version, same-bytes re-reads reproduce a distance of .883 of the full inter-epoch pinned displacement (95% CI [.652, 1.222]), and .920 of it under the Euclidean embedding (95% CI [.808, 1.046]). Both intervals include one. The quantity the design subtracts as a version floor is, at this epoch pair, statistically indistinguishable from the instrument reading the same bytes twice.

**This is not an anomaly of the present instrument, and independent pre-registered evidence says so.** An audit of black-box observers on shared endpoints reports that byte-identical requests replayed against the same model name disagree substantially, that waiting does not help, that four providers share the floor, and that none of the metadata those providers expose predicts it [@zhu-2026-clean-engineering-unstable-measurement]. Read against that result, a pinned panel moving over 77 days under an unchanged model identifier is the expected behaviour of shared serving infrastructure rather than a defect in this capture. It also explains why the floor could be substantial while no version shipped.

This is the pre-registered small-floor limitation in its strongest form, and it bounds what the six clearances mean. The band those brands beat is real and correctly estimated, so they moved beyond the apparatus; what cannot be said is that they moved beyond a *version* change, because none occurred. The clearance rule is demonstrated against apparatus non-determinism rather than against the vendor drift it was designed to remove, and an epoch pair spanning an actual release is required before the correction can be shown doing the work it was designed to do.

***Artifact turnover and the per-channel result***

The pre-registration fixed, before collection, that the panel's artifact turnover would be measured at the reading and reported whatever the velocity result, because a cell whose artifact has not changed cannot clear the floor by construction and that is a fact about the channel rather than about the brand.

**Table 5.** Artifact Turnover and Floor Clearance by Channel.

| Channel | Cells | Same URL reused | Same publisher | Median text similarity | Cells at similarity $\geq$ .90 | Cell-level $S/N$ |
|---|---:|---:|---:|---:|---:|---:|
| Official communications | 40 | 40 | 40 | .907 | 20 | 1.458 |
| Press coverage | 40 | 12 | 26 | .045 | 10 | 1.620 |
| Experience reports | 40 | 9 | 21 | .039 | 3 | 2.264 |
| Social discourse | 40 | 9 | 38 | .025 | 6 | 2.326 |
| All | 160 | 70 | 125 | .047 | 39 | 2.004 |

*Notes*: Similarity is character-level between the VE-1 and VE-2 texts of the same cell. Cell-level $S/N$ pools both operator pairs over 80 cell readings per channel and is diagnostic only; the pre-registered unit of analysis is the brand, whose reading averages four channels and therefore carries less noise.

**The advance prediction is confirmed.** Clearance rises monotonically as artifact turnover rises: official communications, where every cell reuses its URL and median similarity is .907, return the lowest ratio at 1.458, and social discourse, at median similarity .025, the highest at 2.326. Cells at similarity $\geq$ .95 — 58 of 320 readings — average $S/N = 1.405$ with 8 clearing $k = 2$, against 5.540 and 139 of 262 for the rest. Thirty-nine of 160 cells sit at similarity $\geq$ .90 and contribute approximately the floor by construction.

The age distribution of the second epoch's artifacts, recorded per cell and reported here because the selection rule imposes no date bound, confirms the same picture from the other side. Press cells are uniformly recent (40 of 40 dated, 37 from 2026). Experience cells are mostly recent but reach back to 2022 (36 of 40 dated, 23 from 2026). Social cells span the widest range by far — 2018 to 2026, with 12 of 40 predating 2026 — which is what a most-substantial-available rule produces in a channel whose best thread may be years old and unchallenged. Official cells carry almost no usable date at all (1 of 40), since a corporate page rarely states one. **The first epoch's manifest records no source date**, so the two panels' age distributions cannot be compared; only the second epoch's is reportable, and that asymmetry is itself a consequence of the capture method having been specified only at the second epoch.

No cell was dropped, reweighted or swapped on account of its similarity. Excluding the near-unchanged cells would make the remainder clear more easily and would be selection on the outcome; the table explains the result rather than improving it.

## Robustness

Each check below was committed in advance, with the parameter varied and the nodes it bears on named. All were run. None overturns the six clearances, and none strengthens them either: what the battery establishes is that the existence result is stable and that the aggregate shortfall is not an artifact of any single choice.

***Distance metric***

Velocity was re-estimated under a Euclidean embedding alongside one-minus-cosine, because an eleven-week interval yields a larger displacement and the cosine approximation degrades there. The two metrics agree on the verdict and disagree on the margin. Under one-minus-cosine the ratios are 1.740 and 2.322; under the Euclidean embedding, 1.271 and 1.638, with both intervals lying entirely below $k$. Neither metric clears on either operator pair, and at the relaxed $k = 1.5$ one cosine cell passes while no Euclidean cell does. The metric better suited to a displacement of this size is the one that fails more decisively, so the null does not depend on a favourable choice of distance.

***Leave-one-operator-out***

Floors and velocities were recomputed dropping each operator pair in turn. The verdict is stable: retaining only the first pair gives $S/N = 1.740$ with a lower bound of 1.307, retaining only the second gives 2.322 with a lower bound of 1.773, and the pooled analysis gives 1.916 with a lower bound of 1.534. No clearance appears or disappears with either pair removed.

**The check is materially weaker than designed, and the reason is on record.** It was specified over three operator pairs and runs over two, because the third pair's extractor left its provider's catalog before the second epoch and was dropped rather than substituted. Dropping one of two leaves a single operator source family, at which point the per-brand operator-uncertainty interval degenerates to a point. What this check establishes is that the panel-level verdict does not depend on either surviving pair. What it cannot establish is operator-family independence, and the result is not reported as though it could.

***Negative control***

The falsification control on the apparatus band: same-version, two-run displacements on the pinned panel, 160 readings over 40 brands under one operator pair. Mean re-run distance is .00360 against a contemporaneous operator floor of .00612 — a ratio of .588 with a 95% confidence interval of [.385, .886] — and .06410 against .09246 under the Euclidean embedding, a ratio of .693 (95% CI [.588, .822]). **The control passes on both metrics, with the interval excluding one in each case**, so the instrument's own non-determinism is not inflating the operator floor. Passing is the right outcome and not a foregone one: an independent pre-registered audit of the same phenomenon, at far greater call volume, found byte-identical replay disagreement large enough to fail gates set at conventional reliability thresholds [@zhu-2026-clean-engineering-unstable-measurement]. That this control clears its band is a property of the aggregation used here — a brand reading averages four artifacts, which cancels much of the per-call noise that study measures directly — not evidence that the underlying non-determinism is small.

Two further readings are reported because the control admits them and the result differs between them. Against the within-epoch version-ladder floor the ratio is .450 and .580, passing more comfortably still. Against the cross-epoch pinned displacement the ratio is .883 (95% CI [.652, 1.222]) and .920 (95% CI [.808, 1.046]), with both intervals including one — the finding discussed under *Ruling out apparatus*, and the reason this epoch pair cannot demonstrate a version correction. Per brand rather than on the mean, 30 of 40 re-runs sit inside their own operator floor, 35 of 40 inside the version-ladder floor and 18 of 40 inside the cross-epoch displacement. The aggregate comparison is the pre-registered form and the verdict rests on it; the per-brand counts are reported so that a reader can see the dispersion the aggregate conceals.

***Multiplicity***

The interaction and the per-brand clearances were re-reported under corrections stronger than Bonferroni. For the interaction the family is one test per admissible operator pair, and Holm leaves the adjusted values at .879 and .938, neither near any threshold under any of the three corrections. For the per-brand clearances the family is 40 tests, and the same six brands clear $k = 2$ uncorrected, under Bonferroni, under Holm and under Benjamini-Hochberg alike. **The existence result therefore survives multiplicity correction**, which is the check HV1 most needed: an existence claim over 40 brands is exactly the shape that a multiplicity correction exists to discipline. No resample of any clearing brand falls below $k$, while every other brand's bootstrap $p$-value exceeds .240, so the correction has a wide gap to work across.

**The gap itself is partly an artifact of resolution and is reported as one.** With two operator source families the cluster bootstrap draws from four equally likely resamples, which yields only 17 distinct $p$-values across 40 brands and a value of exactly zero wherever both operators agree. A correction cannot separate brands that the interval cannot separate, so the six survive every correction because the bootstrap has too few states to place them anywhere else, not because the evidence for them is overwhelming. The verdict does not depend on the choice of multiplicity control; the resolution limit is what bounds it.

***Capture method and discovery channel***

Two components of the live-panel displacement cannot be separated from brand signal by a two-epoch design, and both were pre-registered to be reported whatever the velocity result turned out to be.

**The capture method.** The first epoch's extraction path is unrecorded, so "the same rubric" cannot be verified against the thing that most determines which 2,500 characters a cell contains. A control was declared in advance on ten official-channel cells — the most stable content in the panel, where a large text difference is evidence about the method rather than about the brand — and run before the reading. Median similarity across the ten is .889 and the median length change is +.1%, with a range of −44.2% to +4.0% and six of ten inside ±3%. The criterion fixed in advance was a **pattern**: cells all shifting the same way would indicate the capture, cells scattering in both directions the pages. **They scatter** — six lengthened or held, four shortened, all ten under the same tool and the same URL — and one cell returned byte-identical, which shows the pipeline reproduces an unchanged page exactly. The three large drops are pages that visibly changed, which is what an official page does over eleven weeks and is exactly the ambiguity the control was declared to have. So no systematic capture-method difference is detectable at this resolution. **This bounds the limitation rather than removing it**: had the second epoch's extraction been systematically thinner or fatter, these ten cells would have moved together, and they did not.

**The discovery channel.** How an artifact was *found* is also unrecorded at the first epoch, and unlike the trimming rule it leaves no trace in the artifact bytes to recover it from. One capture group's web-search quota was exhausted before it began, so its fresh-source discovery ran through news feeds and direct fetches rather than a search engine. A different discovery channel reaches a different set of outlets, so the second epoch's *source distribution* may differ from the first for reasons that have nothing to do with the brands. What is reconstructible is reported instead of corrected: every manifest row records its URL, and the same-publisher column of Table 5 gives the per-channel count of cells that came back from the first epoch's outlet against a substituted one — 125 of 160 overall, and all 40 in the official channel by construction. Both epochs independently recorded blocks on the same outlets — Trustpilot, Reddit, ConsumerAffairs and G2 — which is evidence that the two discoveries met the same obstacles rather than diverging arbitrarily.

**Neither limitation is removable after the fact.** Two-epoch velocity cannot separate a capture-method component, or a discovery-channel component, from brand signal, and no analysis performed afterwards can. The controls bound both; a third epoch captured under the now-specified rubric is what would close them.

***Estimator sensitivity***

One pre-registered control did not pass, at either epoch, and it bounds the reading. The positive control is a deliberately distant version pair — roughly eighteen months apart, designated ex ante — which must move the pinned panel beyond the contemporaneous operator floor if the estimator is sensitive to version differences at all. It returns $S/N = .786$ (95% CI [.589, 1.103]) at the second epoch and .504 (95% CI [.381, .650]) at the first. It does not exceed the floor at either.

This is a standing property of the instrument rather than something the second epoch introduced, and it sharpens the interpretation of the null. At this instrument's noise level the version effect the design exists to remove is small relative to the dispersion between operator pairs, and over this particular interval it was absent entirely. The floor-clearance rule is well-posed and the apparatus implements it; what the data do not supply is a version change large enough to show the correction doing work.

## Discussion

***When events are cultural***

The dissociation is a claim about the typical case, not a universal law, and its most interesting boundary is the practitioner intuition that culturally charged brands move most after a model update. The mechanism predicts the opposite loading only when the event that moves the brand is itself value-laden: a values controversy revises the artifacts a brand emits along exactly the prior-dependent dimensions, so live motion can appear on {Ideological, Cultural} through fresh artifacts rather than through the reader's priors. This is pre-registered as the condition under which the dissociation is bounded, and the design turns the practitioner claim into a direct test rather than a caveat: if culturally charged brands show live artifact-driven motion on the prior-dependent set, the dissociation is bounded, not false. The observed interaction is null and the in-window smoothness check was not recorded, so the test was run but does not discriminate: the reading leaves the boundary condition open rather than settling it either way. What the null does cost is the comprehension account's most specific prediction. The account survives as a reading of where version drift should concentrate, but its distinctive claim — that motion and drift separate across a partition fixed in advance — has been tested once and not supported, over an interval that contained no version drift for it to separate from. A pair spanning a real release is what would put it at risk again, and until one is run the mechanism is better described as untested than as corroborated.

***Generalization beyond one instrument***

The demonstration runs on a single eight-dimension brand instrument, and transfer to other multidimensional-perception domains is untested here. The contribution generalizes as a method rather than as a result: the version-floor correction is what makes longitudinal measurement with model observers well-posed at all, and any domain in which an observer's readings drift across model versions faces the same confound and can adopt the same floor-clearance rule. A non-brand demonstration is future work; the present claim is scoped to the instrument on which it is measured.

## Limitations

Five limitations are priced into the claims. The first epoch's capture method and its discovery channel are both unrecorded, so a capture-method component and a source-distribution component of the live-panel displacement are not separable from brand signal at two epochs; the declared ten-cell control finds no systematic method difference and both epochs met the same blocked outlets, which bounds the two rather than removing them, and the second epoch's rubric is recorded so a third can be compared against a specification rather than an inference (medium). The pre-registered in-window smoothness check — confirming that no crisis, rebrand or dimensional-creation event fell inside the observation window — was not recorded at capture, so the boundary condition on the dissociation can be neither invoked nor excluded when reading its null, mitigated only by stating the gap and recording the check at the next epoch (medium). The cadence is an opportunistic two-epoch design: it yields velocity only — acceleration needs a third epoch and is held for a separate follow-up — and the epoch interval is set by real vendor timing within the relaxation-window guideline rather than chosen freely, mitigated by pre-registering the cadence against the relaxation timescale and reporting velocity as a dated rate (medium). A small version floor at the current epoch lowers the clearance bar, and this limitation arrived in its strongest form: no vendor shipped a new version for either operator pin inside the observation window, so the epoch pair contained no version drift and the pinned panel measured apparatus non-determinism instead. The negative control puts same-version re-reads at .883 of the full pinned displacement with an interval including one, and the positive control does not exceed the operator floor at either epoch, so the planned mitigation — demonstrating estimator sensitivity on a distant-version pair — is itself unavailable here. The floor remains the correct band for the live panel to beat and is correctly estimated; what this interval cannot show is the version correction doing work, and a later pair spanning an actual release is required for that (high, revised from low at the second epoch). And the instrument is a single eight-dimension brand apparatus, so the result's transfer to other domains is asserted as a method, not shown as a finding, mitigated by framing the contribution as the version-floor correction that enables longitudinal model-observer measurement and by noting a non-brand demonstration as future work (medium).

## Companion Computation Script

Every number reported above reproduces from seeded code published with the paper or with its parent, and the split between the two is itself part of the disclosure.

The paper's designated estimator is `velocity_estimator.py` (fixed seed 20260704). It takes one reading per panel, epoch, brand and operator, and returns the version floor, per-brand live displacement, floor-cleared velocity by vector rejection, the signal-to-noise ratio, and the source-cluster bootstrap intervals on which the pre-registered clearance rule is evaluated. The panel aggregate, the six per-brand clearances of Table 3 and the leave-one-operator-out recomputation all come from it. `power_analysis.py` (fixed seed 20260704) is the simulation that fixed the .0162 minimum detectable velocity before collection.

The per-ladder cross-epoch decomposition, the dissociation interaction, the negative control and the metric sweep are computed by the parent instrument's estimator (fixed seed 20260702), which is published with the parent paper rather than with this one, because the reliability battery is the parent's apparatus and is reused here unchanged rather than reimplemented. Its two cross-epoch assembly functions were corrected on 2026-09-17: both keyed their readings without the run index and so pooled the negative control's second run into the pinned panel of the one ladder whose top rung is the control's operator pair, which halved that ladder's floor while its live arm kept a single run. The parent's own published results are unaffected and reproduce bit-identically, because the corrected functions run only on a two-epoch path the parent never took. Every figure in this paper is computed after that correction.

Run commands and the record-layer schema are documented in the code README. The regression check that guards the correction is the parent's committed first-epoch results file, which must reproduce bit-identically after any further change.

## Data and Code Availability

The frozen pre-registration, the byte-identical render-and-extract prompts, the frozen pinned panel (40 brands by 4 artifacts, with a SHA-256 manifest per artifact), the append-only per-call JSONL logs, the velocity and floor-clearance estimator, and the completed power simulation publish with the paper in its public repository under `code/` and `data/`. The second-epoch readings, the velocity and dissociation results, and the empirical robustness outputs were collected on 2026-09-17 and publish with the paper; the second epoch's live and pinned panels carry their own SHA-256 manifest and per-cell capture dates. The complete append-only call logs for both epochs — one record per model API call, carrying prompts, parameters, responses and token usage — are archived as a Hugging Face dataset at DOI [10.57967/hf/10484](https://doi.org/10.57967/hf/10484), whose two-epoch state is revision `654458a`; the first epoch alone is DOI 10.57967/hf/9396 at revision `bebe3408e4ad`. Both DOIs resolve to the same repository URL, so the revision is what fixes which epochs a reader receives. Archived version of record: DOI [10.5281/zenodo.21192878](https://doi.org/10.5281/zenodo.21192878) (concept) and [10.5281/zenodo.21192879](https://doi.org/10.5281/zenodo.21192879) (v1.0.0). All artifact texts are excerpts of public digital brand artifacts, redistributed with per-record provenance.

## Acknowledgments

AI assistants (Claude Fable 5, Grok 4.1) were used for initial literature search, for software development — authoring the power-simulation and estimator scripts — and for editorial refinement; the companion power simulation and the velocity estimation were run through those scripts, and all theoretical claims, propositions, and interpretations are the author's sole responsibility. The segmenter and classifier models named in the operator-pair configuration serve as the measurement instrument's operators — study apparatus, not authorship assistance — and their logged outputs across both epochs constitute the dataset of record.

## Author Contributions (CRediT)

Dmitry Zharnikov: Conceptualization, Data curation, Formal analysis, Funding acquisition, Investigation, Methodology, Project administration, Resources, Software, Supervision, Validation, Writing — original draft, Writing — review and editing.

## References

::: {#refs}
:::
