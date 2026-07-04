# Measuring Optimization Depth: A Pre-Registered Instrument for the Stated-Actual Optimization Gap in Organizational Self-Description (PRISM-O)

Dmitry Zharnikov

ORCID: 0009-0000-6893-9231

DOI: [10.5281/zenodo.21159815](https://doi.org/10.5281/zenodo.21159815)

Working Paper v1.0.0 – July 2026

## Abstract

Organizations improve themselves at different depths — economic outputs, coordination structure, activity chains, delivered value — and a long literature holds both that deeper interventions are the durable ones and that organizational talk decouples from organizational action. Neither claim has a general-purpose measurement instrument. This paper introduces PRISM-O, a pre-registered instrument in which large language model operators classify every improvement intervention in a frozen two-channel panel of public artifacts — strategy prose versus reported concrete interventions — onto a four-rung optimization-depth ladder under a fixed mechanical rubric, reporting the stated-actual optimization gap only beyond twice the cross-family operator noise floor. Constructed-ground-truth validation is a ceiling result (macro accuracy 1.000, identity masking inert). On a pinned 40-organization filing panel, the floors speak: 4 of 35 organizations resolve, so by pre-registered rule the decoupling hypotheses demote to descriptive reporting — pooled depth distributions separate in the predicted stated-deeper direction (p < .001) but the permutation falsification bar is not cleared. Nearly half of segmented improvement spans specify nothing codable, more in strategy prose than in enacted reports. The instrument, rubric, bank, logs, and estimator publish for reuse; the instrument measures the public record, never internal ground truth.

**Keywords:** optimization depth, decoupling, content analysis, large language models, measurement instrument, preregistration, organizational change, noise floor

---

Every wave of management technology arrives with the same pair of open questions [@abrahamson-1996-management-fashion]. The first is about depth: when an organization says it is improving itself, at what layer does the improvement actually bind — the economics it reports, the structure it draws, the processes it runs, or the value it delivers? The second is about honesty: does what the organization *says* about its improvement match what it *does*? The 2025–2026 wave of AI adoption has made both questions acute — practitioner commentary alleges that much announced "AI transformation" is conventional cost reduction with new vocabulary, a claim that is, precisely, unmeasured — but the questions are old, and the previous wave already produced their canonical case study: the rhetoric of total quality management diverged from its enacted reality inside the same organizations that professed it [@zbaracki-1998-rhetoric-reality-total].

The depth question belongs to the process tradition. Reengineering held that durable improvement comes from redesigning activity chains rather than manipulating their outputs [@hammer-1993-reengineering-corporation-manifesto]; lean production located sustainable economics in the elimination of waste from the process itself, with financial results as a byproduct [@ohno-1988-toyota-production-system; @womack-1996-lean-thinking-banish]; and the mirroring argument explains why structure-only interventions revert — coordination structure reflects the process topology it coordinates, so changing the chart without changing the chain restores the chart [@conway-1968-how-do-committees]. The routines literature supplies the micro-foundation: organizational activity is carried by routines, and durable change is change in the routine, not in its reported performance [@feldman-2003-reconceptualizing-organizational-routines; @pentland-2005-organizational-routines-as]. All of this is doctrine with case evidence — none of it is an instrument.

The honesty question belongs to the decoupling tradition. Institutional theory predicted that formal claims and operational practice systematically separate [@meyer-1977-institutionalized-organizations-formal]; the organized-hypocrisy account sharpened the prediction into a production claim — talk, decisions, and actions as distinct organizational outputs, each answering its own audience [@brunsson-1989-the-organization-of]; the espoused-versus-in-use asymmetry made the same prediction at the level of the actors [@argyris-1978-organizational-learning-theory]; and the tradition's modern taxonomy distinguishes policy–practice decoupling (adopted policies left unimplemented) from means–ends decoupling (implemented practices disconnected from the outcomes they claim to serve) [@bromley-2012-smoke-mirrors-walking] — the stated–actual depth gap measured here is the policy–practice form made ordinal, with the depth ladder supplying the order. Which register a firm leads with is itself patterned — larger firms talk where smaller firms walk, on organizational-cost grounds [@wickert-2016-walking-and-talking] — so an instrument must read both registers rather than assume their relation. The canonical empirical measurement is construct-specific: announced stock repurchase programs versus their actual execution [@westphal-2001-decoupling-policy-from] — an elegant archival design that works precisely because repurchases leave a mandatory numerical trail, and that does not generalize to intervention types without one. Text-based measurement of symbolic management exists — espoused versus realized strategic orientation read from corporate narratives [@fiss-2006-symbolic-management-strategic] — but carries no ordered depth construct, no reusable rubric, and no criterion for when a reading outruns the instrument's own noise.

This paper contributes the missing apparatus. PRISM-O is a pre-registered measurement instrument in which AI operators read a frozen two-channel panel of an organization's public artifacts — a **stated channel** of strategy prose and an **enacted channel** of reported concrete interventions — classify every improvement intervention onto a four-rung **optimization-depth ladder** under a fixed mechanical rubric, and estimate the **stated-actual optimization gap**: the signed depth difference between what the organization claims to optimize and what its reported actions specify. Every element of the estimate carries measured uncertainty: depth readings and gaps are claimed only beyond noise floors estimated from cross-family operator disagreement on the identical panel, rubric validity is measured against a constructed-ground-truth vignette bank before any real organization is read, a pre-registered but deferred human-coding arm covers future convergent validation, and a channel-label permutation test must reject the no-signal null for any decoupling claim to stand.

Three phenomena that prior theory names but cannot quantify at scale become measurable in principle — and the campaign reports how far current operators actually resolve them. First, the AI-adoption pattern: announcements that claim process transformation while specifying only headcount targets — decoupling made countable, intervention by intervention. Second, restructuring reversion: the mirroring argument predicts structure-only interventions revert, and the instrument reads whether announced reorganizations come with respecified processes or without them. Third, the lean doctrine itself: whether "process before results" survives in enacted public records or lives only in stated ones. The practitioner form of the question the instrument answers is blunt: *is the transformation real or rhetorical?*

The instrument makes one deliberate scope commitment throughout: it measures the organization's PUBLIC signal. Bounded outside observation cannot recover internal configuration [@zharnikov-2026-specification-impossibility-organizational-design-high], and nothing here claims otherwise; both channels are registers of the public record, and the gap is *communicated* decoupling. This is the correct object for a growing class of consumers — analysts, counterparties, and AI agents act on the public record, not on internal truth — and the honest one for a text instrument.

## The Depth Ladder

***Four rungs, ordered by dependency***

An improvement intervention is an announced or reported change with an identifiable object: what is being changed. The instrument codes each intervention at one of four rungs by that object:

Table 1: The Optimization-Depth Ladder.

| Rung | Object the intervention changes | Typical forms |
|---|---|---|
| D4 — operations/economics | An economic quantity directly, with no specified change to what is done or how | Layoffs, hiring freezes, budget cuts, vendor renegotiation, "AI to do the same tasks cheaper" |
| D3 — organization | The coordination structure: reporting lines, team and department boundaries, decision rights, spans | Flattening, mergers of units, matrix adoption |
| D2 — process | The activity chain: activities added, removed, or resequenced; handoffs eliminated; acceptance criteria redefined | Workflow redesign, autonomous routing, handoff elimination |
| D1 — product/value | What value is delivered | Product redefinition, offer or market pivot, value-proposition restructuring |

*Notes*: Rungs D1–D3 correspond to the product, process, and organization tiers of the six-tier organizational ontology [@zharnikov-2026-dual-hierarchies-organizational-transferability-six]; D4 is the stack's economic output surface, deliberately not a tier; the D3 rung's objects — reporting lines, groupings, decision rights, spans — are the classical elements of coordination structure [@mintzberg-1979-structuring-organizations-synthesis]. The D-labels are new to this instrument. A meta rung — adopting an improvement framework itself — is out of scope and codes UNCLASSIFIED.

The ladder's order is a dependency chain, not a preference ranking. The coordination structure exists because activity chains do not run themselves from input to output; the activity chain exists to deliver the value specification; the economics are the output of all three [@zharnikov-2026-organizational-schema-theory-test-driven]. Two consequences follow and are treated as cited theory here, not as claims this paper tests. Deeper interventions cascade outward: a respecified process entails a different coordination load and different economics. Surface interventions revert: an intervention that changes reported quantities while leaving the deeper specification untouched leaves in place exactly the structure that produced the old quantities [@hammer-1993-reengineering-corporation-manifesto; @conway-1968-how-do-committees]. The durable-change locus sits at the process and product rungs [@ohno-1988-toyota-production-system; @feldman-2003-reconceptualizing-organizational-routines].

***What the rungs are not***

The ladder is not a maturity grade — not a staged capability model in the lineage of the CMM [@paulk-1993-capability-maturity-model] — and carries no normative claim that deeper is better for every organization at every moment; a firm in a liquidity crisis rationally intervenes at D4. What the ladder supports is a *descriptive* reading of where an organization's interventions bind, channel by channel — and it is the difference between channels, not the level itself, that the instrument's headline statistic reports.

## Position Among Measurement Approaches

***What exists and what is missing***

Three measurement traditions border the instrument, and each supplies a piece while missing the object. The decoupling tradition has exact empirical designs for specific constructs — announced repurchase programs against executed repurchases being the canonical case [@westphal-2001-decoupling-policy-from] — but each design is bespoke to an intervention type with a mandatory numerical trail; there is no reusable instrument for the depth gap across intervention types. The content-analysis tradition supplies the field's methodological benchmarks and its catalogue of reliability problems — coder subjectivity, source bias, unreported refinement [@duriau-2007-content-analysis-literature] — which any artifact-reading instrument must answer by construction. The process-audit tradition measures process maturity directly but by practitioner self-report [@hammer-2007-the-process-audit], which is precisely the register a decoupling instrument cannot trust: self-report of depth is the stated channel.

Computer-aided text analysis carries a decade of reliability standards for organizational constructs [@mckenny-2018-what-doesnt-get] and a rendering pipeline from text to theory [@hannigan-2019-topic-modeling-management]; recent computational work at this frontier brings large language models into organizational text analysis — as qualitative-analysis assistants [@garciaquevedo-2025-enhancing-theorization-using], as supervised scorers of performance text [@speer-2024-taking-it-easy], and as targets of measurement-error correction [@iqbal-2025-using-coreference-resolution] — and the annotation literature reports LLM reliability at or above crowd-worker level on social-science text classification [@gilardi-2023-chatgpt-outperforms-crowd; @ziems-2024-can-large-language-models]. What this line has not produced is a depth-ladder instrument with noise floors: an ordered organizational construct, a mechanical rubric, and a resolution criterion under which the instrument refuses to claim what it cannot distinguish from its own disagreement. A full-text sweep of this literature through mid-2026 — extended beyond registry depth to preprint servers — locates classifiers of adjacent constructs at sentence level, but no such instrument.

***The apparatus in one paragraph***

PRISM-O assembles that instrument from a metrological discipline developed in a published instrument family for a different construct domain [@zharnikov-2026as-prism-structured-measurement]. The discipline's elements — pre-registered protocol frozen before data, versioned prompts with structured output, append-only call logging, operator noise floors estimated from cross-family disagreement, a per-pair resolution criterion, mechanical pre-flight concordance screening, and committed publication of nulls — transfer to the organizational construct unchanged; only the construct, the rubric, and the panel design are new. The transfer is itself informative: the apparatus was built domain-neutral, and this paper is the producer-side test of that neutrality — the family's prior instruments read observer-side perception, while PRISM-O reads the producing organization through the same rendered public artifacts, the one place a firm-internal stack and an outside observer meet [@zharnikov-2026bc-producer-observer-seam]. Distinct internal configurations can be observationally equivalent from outside [@zharnikov-2026-organizational-metamerism-when-distinct-configurations]; the two-channel design exploits exactly the case where the stated register is indistinguishable while the enacted register resolves.

## Two Channels of the Public Record

***Channel assignment by artifact class***

The unit of analysis is the organization's public signal over a fixed twelve-month window. The panel frame and the channel-to-class mapping are ex-ante *parameters* of a deployment, not commitments of the instrument — this campaign instantiates them on the public record. Within the window, artifacts are assigned to channels by class, fixed ex ante: the STATED channel comprises strategy prose — mission and strategy sections, transformation announcements, earnings-call prepared remarks; the ENACTED channel comprises reports of executed interventions — restructuring filings, layoff notices, executed-reorganization reports, shipped process and product changes. Ambiguous classes are excluded by rule, not judgment. The channel split is a design assumption with teeth: if the two registers do not measure different things, the estimator's negative control (disjoint same-channel draws) and its permutation test (channel labels randomly reassigned within organization) will say so empirically.

***What "enacted" honestly means***

Enacted-channel artifacts are *reports of* concrete events, not the events themselves. The classes are restricted to filings and executed-change reports — verifiable, consequential, and costly to fabricate — which places them closer to behavior than strategy prose without making them behavior. The instrument therefore measures the gap between two registers of one public record; reading that gap as talk-versus-action leans on the verifiability of the enacted classes, and the Limitations section prices that lean explicitly. No performance or outcome claim is made anywhere in the design.

## The Depth-Coding Rubric

***Decision tree and tie-breaker***

Coding is mechanical. The coder — human or AI — walks a fixed decision tree from the deepest rung down: does the intervention specify a change to what value is delivered (D1)? to the activity chain (D2)? to the coordination structure (D3)? to an economic quantity directly (D4)? The first yes codes the intervention; an intervention that specifies changes at several rungs codes at the deepest rung it *specifies*. The decisive test is specified-not-promised: a rung counts only if the change at that rung names its object and its change, not an aspiration or a consequence. "We will transform how we work" promises D2 and specifies nothing; if the only specified object is a headcount target, the intervention codes D4. Ties between adjacent rungs after this test break downward, toward the surface. People-centered interventions follow the same object test: a training program that respecifies an activity chain codes D2, a decision-rights change codes D3, and skill or culture aspirations that specify no object code UNCLASSIFIED. Figure 1 renders the frozen tree exactly as it binds inside the classification prompt.

``` {.mermaid width=100%}
flowchart LR
    A["Intervention text"] --> B{"Changes WHAT VALUE<br/>is delivered?<br/>(product, offer, market,<br/>value proposition)"}
    B -- yes --> R1["D1<br/>product/value"]
    B -- no --> C{"Changes the<br/>ACTIVITY CHAIN?<br/>(activities, handoffs,<br/>acceptance criteria)"}
    C -- yes --> R2["D2<br/>process"]
    C -- no --> D{"Changes the<br/>COORDINATION STRUCTURE?<br/>(reporting lines, boundaries,<br/>decision rights, spans)"}
    D -- yes --> R3["D3<br/>organization"]
    D -- no --> E{"Targets an ECONOMIC<br/>QUANTITY directly?<br/>(headcount, cost,<br/>margin, budget)"}
    E -- yes --> R4["D4<br/>operations/economics"]
    E -- no --> U["UNCLASSIFIED<br/>(excluded from estimator,<br/>count reported)"]
```

**Figure 1.** The frozen depth-coding decision tree, as published with the instrument. The coder walks deep-to-surface — D1 first — and stops at the first yes; every object test is specified-not-promised, and ties between adjacent rungs after that test break downward, toward the surface.

Twelve annotated hard cases are frozen with the rubric and embedded in the classification prompt as worked examples, including matched minimal pairs at the hardest boundaries — the sharpest being tool rollout ("give every engineer the assistant": D4, a faster engine in an unchanged process) against tool-native redesign ("autonomous classification and routing with acceptance criteria, complex cases to the product team": D2). The full tree, cases, and the pre-registered three-regime tie-breaker sensitivity analysis are published with the instrument.

***The genre rival, answered by construction***

The obvious rival to any positive gap is genre: strategy prose may simply *sound* deeper regardless of substance, so a text instrument would detect register, not decoupling. The rubric is built against this rival twice over. The specified-not-promised test codes unspecified depth language toward the surface — deep-sounding prose that specifies nothing codes D4 or UNCLASSIFIED, not D2. And the vignette bank plants both registers with depth fixed by construction: if the rubric tracked genre rather than specified depth, Stage-1 accuracy would fail on the register-crossed vignettes.

## The AI Operator as Coder

The instrument's coders are large language model operators, on two grounds. The practical ground is scale with auditability: every classification is a logged, reproducible call with pinned model identifiers, versioned prompts, and structured output — the methodological transparency the field's reporting standards demand [@aguinis-2018-what-you-see] — a coding operation that can be re-run, re-audited, and extended at panel sizes human teams cannot price [@gilardi-2023-chatgpt-outperforms-crowd; @ziems-2024-can-large-language-models]. The methodological ground is that the instrument never leans on any single model's judgment: at least three cross-family operator pairs read the identical pinned panel, their disagreement IS the instrument's noise floor, and a mechanical concordance screen with a fixed exclusion rule runs before any confirmatory reading [@zharnikov-2026az-prism-m-metamerism]. Model-version epochs are stamped on every reading so that any future re-read is attributable to its apparatus [@zharnikov-2026ba-prism-t-version-floor]. One further ground is scope-honest rather than practical: for claims about how the public record reads under AI observation, AI observers are the measurement construct itself, not a proxy for human raters — human gold standards are required where humans are the construct [@rathje-2024-gpt-effective-multilingual; @abdurahman-2024-perils-opportunities-llms; @trott-2024-augment-psycholinguistic-datasets], and this paper makes no human-perception claim. A human-coded subsample — at least ten percent of all interventions, coded blind under the same rubric, reporting percent agreement, Cohen's κ, and Krippendorff's ordinal α [@hayes-2007-answering-the-call] — is pre-registered as a deferred arm for future convergent validation (the protocol's pre-collection amendment defers its collection); until it runs, no human-interpretability claim is made for the depth readings.

## Floors and Resolution

The estimator's discipline is that noise is the null. Per organization, the depth distribution of each channel is computed over coded interventions; the gap is the signed difference of mean depth rank (stated minus enacted, positive when the organization talks deeper than it acts). The operator floor is the dispersion of that gap across cross-family operator pairs reading the identical panel; a gap is **resolved** only when its magnitude exceeds twice the floor [@zharnikov-2026ax-brand-spectrometer]. Unresolved gaps are reported as unresolved — never dropped, never rescued by the most agreeable operator family [@zharnikov-2026ay-substrate-floor]. Because the ladder is ordinal, the mean-rank gap never stands alone: a distributional test must agree in direction, and median-rank and stochastic-dominance robustness checks are pre-registered alongside — treating an ordinal ladder's mean as self-sufficient is a known way to go wrong [@liddell-2018-analyzing-ordinal-data]. Uncertainty is clustered at the artifact level (source-cluster bootstrap), since interventions within an artifact are not independent draws.

Formally, each classified intervention $i$ carries the rung score

$$d(i) \in \{1, 2, 3, 4\}, \qquad \mathrm{D4} \mapsto 1, \quad \mathrm{D3} \mapsto 2, \quad \mathrm{D2} \mapsto 3, \quad \mathrm{D1} \mapsto 4,$$

so that deeper is larger. For organization $o$, operator pair $p$, and channel $c \in \{\mathrm{S}, \mathrm{E}\}$ (stated, enacted), let $\bar{D}^{(p)}_{o,c}$ denote the mean rung score over the pair's classified interventions in that channel. The per-pair gap and the gap estimate over the $P$ pairs are

$$g^{(p)}_{o} = \bar{D}^{(p)}_{o,\mathrm{S}} - \bar{D}^{(p)}_{o,\mathrm{E}}, \qquad \hat{g}_{o} = \frac{1}{P} \sum_{p=1}^{P} g^{(p)}_{o},$$

the operator floor is the across-pair dispersion of the gap on the identical pinned panel,

$$\phi_{o} = \left( \frac{1}{P-1} \sum_{p=1}^{P} \left( g^{(p)}_{o} - \hat{g}_{o} \right)^{2} \right)^{1/2},$$

and organization $o$ resolves if and only if the gap clears twice its floor,

$$\left| \hat{g}_{o} \right| > k\,\phi_{o}, \qquad k = 2,$$

with the $k$-sweep over $\{1.5, 3\}$ reported alongside. The post-campaign nested criterion (pre-registration §10.1) places the artifact-sampling band $\beta_{o}$ — the standard deviation of the seeded artifact-cluster bootstrap of $\hat{g}_{o}$ — under the operator band, so that a nested resolution requires

$$\left| \hat{g}_{o} \right| > k \max\left( \phi_{o}, \beta_{o} \right).$$

## Pre-Registered Hypotheses

The frozen protocol commits three hypotheses, each with a committed publishable null, at family-wise α = .05 (Bonferroni, α = .017 per hypothesis):

**H1 (measurability).** On the constructed vignette bank, operator classification recovers ground truth at macro accuracy ≥ .80; on the real panel, a majority of organizations' depth readings resolve beyond the operator floor. Failure publishes as the measured capability bound of LLM depth-coding.

**H2 (decoupling direction).** The stated channel reads deeper than the enacted channel: the panel-level signed gap is positive and resolved. The direction is the decoupling tradition's prediction [@meyer-1977-institutionalized-organizations-formal; @argyris-1978-organizational-learning-theory]; a floored null publishes as measured consistency of public organizational communication — itself a result the tradition does not predict.

**H3 (signal attribution).** For resolved organizations, gap dispersion across operator families stays within the operator floor: the gap is a property of the organization's public signal, not of the model family reading it. Failure demotes the finding to a family-conditional reading.

Power is pre-registered: the panel of at least sixty organizations targets at least forty-five resolved cases, which powers a half-rung gap at .80 under the frozen assumptions; below the minimum resolved count, hypothesis claims demote to descriptive reporting by rule [@nosek-2018-the-preregistration-revolution; @flake-2020-measurement-schmeasurement-questionable]. Figure 2 displays the frozen computation across resolved-panel sizes: at the registered assumptions the half-rung curve reaches .80 power at exactly the minimum-resolved target, a .75-rung gap is powered from 22 resolved organizations, and a quarter-rung gap stays under-powered at any feasible panel — the design is sized to detect gaps of managerial magnitude, not decimal residue.

![](figures/power_curves.png)

**Figure 2.** Pre-registered power curves: exact noncentral-t power of the two-sided one-sample test at α = .017 as a function of resolved-organization count, for mean gaps of .25, .50, and .75 rung units at the frozen across-organization SD of 1.0 rung. The dashed vertical line marks the minimum-resolved-N target of 45; the half-rung curve crosses .80 power at n = 45. Reproduced by [`code/power_analysis.py`](https://github.com/spectralbranding/sbt-papers/blob/main/prism-o-optimization-depth/code/power_analysis.py) at seed 20260703.

## Stage 1: Constructed Ground Truth

The pre-flight equipment ran first: every pinned model identifier was present in its family's live catalog, and the concordance screen found zero disagreement between the two Stage-1 pairs on the sixteen probe readings, so the mechanical exclusion rule removed nothing. On the full frozen bank (52 readings per pair, 208 logged calls), depth classification against constructed ground truth was a ceiling result: macro accuracy 1.000 for both operator pairs — on the full bank *and* on the fourteen held-out bases whose worked answers do not appear in the classifier prompt — with every rung at 1.00 recall, zero malformed outputs, and masked-equals-named agreement of 1.0 on identical text. The pre-registered gate (macro accuracy ≥ .80, applied to both the registered full-bank statistic and the conservative held-out statistic, per pair) passed with no margin consumed. Table 2 reports the per-rung layer of the ceiling: the confusion matrix is the identity for both pairs, so per-rung recall summarizes it without loss.

Table 2: Stage-1 Per-Rung Recall Against Constructed Ground Truth, by Operator Pair.

| Rung | n (full bank) | Anthropic → OpenAI | Alibaba → DeepSeek | n (held-out) | Held-out recall (both pairs) |
|---|---|---|---|---|---|
| D1 — product/value | 10 | 1.00 | 1.00 | 6 | 1.00 |
| D2 — process | 14 | 1.00 | 1.00 | 8 | 1.00 |
| D3 — organization | 10 | 1.00 | 1.00 | 6 | 1.00 |
| D4 — operations/economics | 14 | 1.00 | 1.00 | 6 | 1.00 |
| UNCLASSIFIED | 4 | 1.00 | 1.00 | 2 | 1.00 |

*Notes*: n = readings per rung per pair (named + masked variants of each base; 52 per pair on the full bank). Held-out = the fourteen bases whose worked answers do not appear in the classifier prompt (28 readings per pair). Every off-diagonal cell of the rung confusion matrix is zero, and zero outputs were malformed.

Two honest qualifications attach. The bank's vignettes are short and unambiguous by construction, so the ceiling validates the rubric's mechanics, not performance on messy filings — that is what Stage 2 measures. And segmenters split compound vignettes into two or three interventions in roughly half of readings (the two zero-detection cases were the UNCLASSIFIED probes, exactly as they should read); classification operated on the full vignette text, so H1(i) is unaffected.

## Stage 2: The Organization Panel

***Resolution: the floors speak***

The confirmatory campaign read 40 pinned organizations (372 artifacts, two channels, four cross-family operator pairs — segmenter → classifier: Anthropic → OpenAI, OpenAI → Anthropic, Alibaba → DeepSeek, DeepSeek → Alibaba, all model identifiers pinned and epoch-stamped in the published configuration — named plus a fifteen-organization masked arm; 8,143 intervention records). Thirty-five organizations carried at least three pair-complete channel readings. Of those, **4 of 35 (11%) resolved** at the pre-registered criterion — a gap magnitude exceeding twice the across-pair floor. The median floor was .584 rung units, an order of magnitude above the median absolute gap: cross-family operator disagreement on real filings swallows most of the panel. H1 is therefore supported only on constructed text: its second clause — majority resolution on the real panel — **fails**, and 4 of 35 is the measured capability bound. Four resolved organizations is also far below the pre-registered minimum of 45, so by the frozen rule **H2 and H3 demote to descriptive reporting; no confirmatory decoupling claim is made.** The instrument reports wholesale sub-resolution rather than manufacturing findings — the no-rescue discipline doing exactly what it is for. (A k-sweep leaves the picture unchanged: 4 resolved at k = 1.5, 2 at k = 3. One resolved organization carries a degenerate floor of .000 from few, identically-read interventions.)

***Descriptive structure***

What the panel shows descriptively tilts in the decoupling direction without confirming it. The all-organization mean gap is .176 rung units (median .059), positive for 20 of 35 organizations (malformed-output shares .006 per channel, the Stage-2 counterpart of Stage 1's zero); the four resolved organizations average .815 (d = .754 — at n = 4, p = .229, reported for completeness, not inference). The pooled depth distributions differ across channels in the predicted direction: two-sample Kolmogorov–Smirnov D = .158, p < .001, stated deeper. Among the resolved four, one organization is *negative* — its enacted record reads deeper than its strategy prose — the pre-registered heterogeneity case, present already at n = 4. But the binding falsification test does not clear: the observed panel mean lies inside the central .95 interval of the channel-label permutation distribution ([−.193, .184], 1,000 within-organization shuffles, fixed seed). Distribution-level structure exists; organization-level signal beyond the instrument's own noise does not, at this panel and this floor.

***Controls and the unspecific-rhetoric index***

The masked arm returns an empty contamination bound: masked-minus-named gap −.018 rung units (SD .206, 13 evaluable organizations) — organization identity moves readings by essentially nothing on identical text. The negative control, however, is not clean: 9 of 46 within-channel disjoint artifact splits pseudo-resolve at the primary criterion. A labeled post-hoc amendment (pre-registration §10.1) responds with a nested criterion: an artifact-sampling band — the seeded cluster-bootstrap SD of the gap — nests under the operator band, and resolution must clear twice the larger of the two. Under the nested criterion 3 of the 4 primary resolutions survive, now all positive (the negative-gap organization falls below its artifact band), and the control improves but does not vanish: 7 of 44 splits pseudo-resolve under the nested band and 5 of 42 when splits are stratified by artifact class. The residue is informative: an organization's public record is not depth-homogeneous within a register — individual filings genuinely differ, partly along class lines — and the nested band prices that heterogeneity into every resolution the instrument claims (see Limitations for the design consequence). Finally, the specified-not-promised rule produced a substantive by-product: **.470 of stated-channel and .393 of enacted-channel intervention spans code UNCLASSIFIED** — nearly half of improvement talk in the public record specifies nothing codable, and strategy prose is emptier than enacted reports by .077. The exploratory AI-announcer contrast is directionally positive and far from informative at n = 7 announcers (mean gap .239 vs .160, p = .814).

A variance decomposition of the primary records puts a number on that heterogeneity directly. Splitting each organization-channel's per-cell mean depth — one cell per operator pair × artifact — into its marginal components, between-artifact variance exceeds between-pair variance in 37 of 52 qualifying organization-channels (Table 3): the individual filings inside one register differ in depth more than the model families reading them disagree, and more so in strategy prose than in enacted reports. The noise the nested band prices is real, and it is the larger of the instrument's two dispersion sources.

Table 3: Artifact-Level Variance Decomposition of Per-Cell Mean Depth, by Channel.

| Channel | Organization-channels | Median between-artifact share | Mean between-artifact share | Artifact-dominant |
|---|---|---|---|---|
| Stated | 21 | .802 | .727 | 18 of 21 |
| Enacted | 31 | .628 | .597 | 19 of 31 |

*Notes*: Cell = one operator pair's mean depth over classified interventions in one artifact (named arm). Share = between-artifact marginal variance over the sum of the between-artifact and between-pair marginal variances; organization-channels qualify with at least three pairs and at least four artifacts carrying classified interventions. Artifact-dominant = share above .5. Reproduced by [`code/variance_decomposition.py`](https://github.com/spectralbranding/sbt-papers/blob/main/prism-o-optimization-depth/code/variance_decomposition.py) at seed 20260703.

***Tie-breaker sensitivity (post-hoc re-read arm)***

The pre-registered three-regime tie-breaker sensitivity could not be recomputed from the primary records — the tie-break binds inside the frozen classifier prompt — so a labeled post-campaign arm (pre-registration §10.2) re-classified every named-arm span (4,288 per regime) and the full Stage-1 bank under explicit regime overrides: ties-upward and ties-flagged-and-excluded. Every conclusion is stable: Stage-1 macro accuracy .99 and 1.00; resolved counts 3–4 across regimes; mean gap .110–.176; and genuinely tied codings almost never occur (3 of 4,288 spans flagged). The one nuance is reported rather than smoothed: under the tie-flagged regime the median gap crosses zero (−.003, against .059 under the primary regime) — the descriptive tilt is regime-robust in mean and fragile in median, exactly what a small signal under a dominant floor should look like.

## Rivals and Controls

Three rivals are registered against the design rather than argued after it, and each now carries its measured verdict. Prior knowledge: operators may know famous organizations and read reputation instead of text — bounded by the masked-identity arm [@zharnikov-2026ap-same-meaning-different-prose], and the bound came back empty (−.018 rung units at the mean; ruled out). Genre: answered by construction in the rubric and measured by the register-crossed vignettes, which coded at ceiling (ruled out at vignette level). Instrument noise: answered by the resolution criterion itself — and here the rival largely *won*: for 31 of 35 organizations the measured gap is not distinguishable from cross-family disagreement, which is precisely what the instrument is built to say out loud when it is true.

## Limitations

Seven limitations are priced into the claims, two of them measured by the campaign itself. The enacted channel is reports of actions, not actions (medium; the artifact classes are restricted to verifiable filings and executed-change reports, and no outcome claim is made). The vignette bank's representativeness of real intervention prose is argued by construction, not measured — and the Stage-1 ceiling against the Stage-2 sub-resolution is direct evidence that constructed and real texts are different regimes (medium; per-rung accuracy is reported, and the pre-registered, deferred human-coding arm marks the future convergent check — deferred, so no human-interpretability claim is made here). No causal or performance claims are available from this design (low). Confirmatory power exists only above the pre-registered minimum resolved panel — and the panel came in at 40 of the targeted 60 organizations (nine roster members have no public filing registrant; channel requirements excluded the rest), so the demotion rule governed the campaign's inference entirely (high, and disclosed rather than repaired). The negative control's 9 of 46 pseudo-resolutions show the across-pair floor under-prices within-channel artifact heterogeneity; a floor architecture that nests an artifact-sampling band under the operator band is the concrete design revision this measurement motivates (medium). The panel frame is a jurisdictional and linguistic scope condition: publicly listed filers with mandatory English-language disclosure (a regime that does not exist for private firms and differs across jurisdictions), so the enacted channel leans on a disclosure infrastructure the conclusions cannot outrun (medium). Finally, the pre-registered tie-breaker sensitivity was not executable within the original design — the tie-break binds inside the frozen classifier prompt, not in the estimator, a design oversight disclosed here — and was executed via the labeled post-campaign re-read arm (§10.2), which left every conclusion unchanged across the three regimes (low).

## Discussion

The campaign's headline is a boundary result, and the paper's deliverable survives it fully: a reusable, pre-registered, noise-floored procedure that turns "is the transformation real or rhetorical?" from commentary into measurement — including the honest answer that, at four cross-family operator pairs and a 40-organization filing panel, the question is mostly *sub-resolved*. Three readings of that outcome matter.

***What the boundary result teaches***

First, the floors did their job, and they localize the noise. Depth coding is not the problem: constructed interventions code at ceiling, and identity masking moves nothing. The disagreement lives in what different model families extract and code from long, messy filings — a median floor of .584 rung units — plus within-channel artifact heterogeneity the negative control exposed. That is an actionable decomposition: a tighter intervention-extraction discipline and an artifact-sampling band under the operator band are engineering, not hope.

Second, the descriptive layer is consistent with the decoupling tradition without certifying it. The pooled distributions separate in the predicted direction (stated deeper, p < .001), a majority of organizations tilt positive, and the sharpest single by-product is the unspecific-rhetoric index: nearly half of segmented improvement spans — and more in strategy prose than in enacted reports — specify nothing an auditor could code. The instrument's most robust measured fact about organizational self-description is not *which* depth it claims but *that it so often declines to specify any*.

Third, the committed-null discipline carried over from the instrument family priced this outcome in advance: the demotion was decided by a rule frozen before any artifact was read, the permutation bar was allowed to fail in public, and the one organization that acts deeper than it talks is reported rather than smoothed — decoupling direction and degree are known to vary with how firms respond to scrutiny [@crilly-2012-faking-it-or], a positive gap can be aspiration that precedes practice rather than hypocrisy that replaces it [@christensen-2013-csr-as-aspirational], and the instrument now gives that heterogeneity a measured form. A larger panel (the roster's non-filing members priced out a third of the target), a nested floor architecture, and the deferred human-coded subsample are the pre-registered path to a confirmatory verdict; the apparatus, the rubric, the bank, and every log are published for anyone to run it.

***A source-agnostic instrument, instantiated on the public record***

Nothing in the rubric, the segmenter–classifier roles, the floors, the controls, or the estimator depends on regulatory filings: the panel frame and the channel-to-class mapping are protocol parameters, and this campaign is one instantiation of them. A deployment in which an organization discloses a richer corpus to the instrument — structured intake responses, internal change records, process documentation, organizational-chart revisions — runs the same apparatus under the same floors and controls, with the pinning, provenance, and masking discipline unchanged. Two guards carry over rather than dissolve. First, self-reported depth claims are stated-register wherever they appear: an intake response about what the organization optimizes joins the stated channel by the same argument that disqualifies self-report as validation, while the realism gain concentrates in the enacted channel, where internal change records are more granular, dated, and verifiable than anything the public record carries — and where this campaign's own noise decomposition located the pathology (unspecific spans; within-channel artifact heterogeneity). Second, the scope statement is per-deployment: the instrument always measures the record submitted to it, a disclosed-corpus reading measures the submitted record rather than the public signal, and cross-organization comparison requires a shared panel frame. Framed this way, the public-record boundary of this paper is not a limit of the instrument but the parameterization under which its first campaign was honest to run.

## Data and Code Availability

The frozen pre-registration (v1.2: two pre-collection amendments dated before any model reading plus the labeled post-campaign robustness amendment), the rubric with its twelve worked cases, the vignette bank (v1.0.0), the pinned panel manifest (SHA-256 per artifact with EDGAR accession and source URL), the complete per-call JSONL logs (model versions, prompt hashes, token usage, cost, latency, retries), the campaign scripts, and the fixed-seed estimator (seed 20260703) publish with the paper:

- Dataset (records, logs, panel, protocol, code): DOI [10.57967/hf/9413](https://doi.org/10.57967/hf/9413) — https://huggingface.co/datasets/spectralbranding/prism-o-optimization-depth
- Code and paper mirror: https://github.com/spectralbranding/sbt-papers/tree/main/prism-o-optimization-depth
- Archived version of record: https://doi.org/10.5281/zenodo.21159815 (concept); v1.0.0 https://doi.org/10.5281/zenodo.21159816

Artifact texts are excerpts of public SEC EDGAR filings, redistributed with per-record provenance.

## Acknowledgments

AI assistants (Claude Fable 5, Grok 4.1) were used for initial literature search, for software development — authoring the collection pipeline, the campaign runners, and the analysis and scoring scripts — and for orchestrating and running the reported experiments through those scripts, as well as for editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility. The segmenter and classifier models named in the operator-pair configuration served as the measurement instrument's operators — study apparatus, not authorship assistance — and their logged outputs constitute the dataset of record.

## Author Contributions (CRediT)

Dmitry Zharnikov: Conceptualization, Data curation, Formal analysis, Funding acquisition, Investigation, Methodology, Project administration, Resources, Software, Supervision, Validation, Writing — original draft, Writing — review and editing.

## References

::: {#refs}
:::
