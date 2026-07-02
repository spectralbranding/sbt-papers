# Measuring Perceptual Indistinguishability: A Pre-Registered Metamerism Instrument for AI Brand Perception (PRISM-M)

Dmitry Zharnikov

ORCID: 0009-0000-6893-9231

DOI: [10.5281/zenodo.21125785](https://doi.org/10.5281/zenodo.21125785)

Working Paper v1.0.0 – July 2026

## Abstract

When two entities with structurally distinct multi-dimensional perception profiles receive identical aggregate readouts — one health score, one ranking slot, one binary pick — the distinction the full instrument could see has been destroyed. Existing treatments assert such indistinguishability; this paper measures it. PRISM-M is a pre-registered instrument built on a dual-floor procedure: a pair counts as a measured metamer only when the full readout resolves it beyond the instrument's own operator noise floor while the aggregate readout, with its own separately measured floor, does not. The procedure is demonstrated end-to-end on AI brand perception: 40 brands from a stratified public-index frame, read through four artifact channels by four cross-family operator pairs, against a battery of three aggregators (scalar score, ranking, binary pick), with planted-positive and same-brand-negative controls. The pre-registered campaign returns a boundary result that exhibits the discipline: one discordant renderer inflates every noise floor, and the instrument reports wholesale sub-resolution rather than manufacturing findings, while its concordance diagnostic localizes the discordance and exploratory analysis of the concordant operator triplet shows the predicted metameric structure — half of resolvable brand distinctions destroyed by a scalar score.

**Keywords:** metamerism, observational equivalence, measurement instrument, noise floor, signal detection, brand perception, AI observers, preregistration

---

Every consumer of an aggregate metric inherits a question they usually cannot ask: what did this number destroy? A brand tracker reduces a brand to one health grade; a recommendation surface reduces it to a ranking slot; an agentic assistant reduces it to a yes-or-no pick. Each reduction is a projection of a richer perceptual state, and projections collide: entities whose full perceptual profiles differ structurally can land on the same grade, the same slot, the same pick. Color science named this phenomenon *metamerism* — physically distinct spectra that one observer cannot tell apart [@wyszecki-1982-color-science-concepts] — and econometrics formalized its inferential shadow as *observational equivalence*: distinct structures indistinguishable in the data a given observation scheme yields [@koopmans-1949-172125144; @manski-1995-untitled]. In brand research the phenomenon has been proven geometrically — projecting an eight-dimension perception profile to a scalar necessarily maps distinct profiles to equal scalars [@zharnikov-2026-spectral-metamerism-brand-perception-projection] — and demonstrated behaviorally in AI-mediated search [@zharnikov-2026-dimensional-collapse-ai-mediated-search; @zharnikov-2026-ai-native-brand-identity-from]. What no instrument yet does is measure how often it happens.

The obstacle is not conceptual but metrological. "These two are indistinguishable under the score" is an assertion until two quantities are measured: how far apart the pair sits on the *full* readout relative to the noise of the full instrument, and how close together it sits on the *aggregate* readout relative to the noise of the aggregate readout. Both noise levels must come from the instrument itself, because for perception there is no external ground truth to calibrate against — a difficulty that ground-truth-absent measurement resolves by validating against self-computed noise floors rather than latent true scores [@zharnikov-2026ax-brand-spectrometer]. Without the first floor, any two noisy readings look "distinct"; without the second, any two quantized scores look "identical." The contribution of this paper is a procedure that supplies both floors, a criterion built on them, controls that check the criterion's sensitivity and specificity, and a pre-registered campaign that runs the whole apparatus on real brands with real aggregators — and reports what the floors permit, including when they permit nothing.

Three contributions are claimed. First, a **general dual-floor procedure for indistinguishability testing**: given any high-dimensional perceptual instrument and any coarser projection of its readout, the procedure defines a measured *metamer* (resolved on the full readout beyond the operator floor; unresolved on the projection within the projection's own floor) and a **metameric fraction** — the share of resolvable distinctions the projection destroys — with a source-cluster bootstrap interval. The procedure is instrument-general; brand perception is the demonstration, not the boundary. Second, an **aggregator battery as a severity ladder**: three readouts matching real consumption surfaces — a scalar brand-health grade, a recommendation ranking, a binary pick — each formalized as a projection operator [@zharnikov-2026au-correspondence-principle-brand] in the comparison-of-experiments sense [@blackwell-1951-comparison-of-experiments; @blackwell-1953-equivalent-comparisons], each with its own measured floor, and a pre-registered monotonicity prediction across them. Third, **metrological discipline for indistinguishability claims**, exercised under fire: the campaign's confirmatory verdict is that *no* pair resolves above the four-family operator floor — one operator reads brands differently enough to swallow every pairwise distinction — and the instrument reports that refusal as the finding, localizes the discordance to a specific operator role with a concordance diagnostic, and quarantines everything the tighter concordant-triplet floor shows behind an explicit exploratory label. An instrument for measuring what aggregation destroys must first be honest about what it cannot itself resolve; the boundary result is the discipline demonstrated, not the discipline failed.

The paper proceeds as follows: the dual-floor procedure and metamer criterion; the instrument (protocol, stimulus frame, channels, operators, aggregators, estimator, controls); the validity argument for AI observers as the measurement surface; results (confirmatory, diagnostic, exploratory, robustness); alternative explanations; and discussion with limitations.

## A Dual-Floor Procedure for Indistinguishability

***The metamer criterion***

Let each entity $b$ carry a full readout $x_b \in \mathbb{R}^p$ produced by a measurement instrument, and let $T$ be a coarser readout (a projection of the perceptual state into a scalar, a rank, or a binary call). Write $d_F(a,b)$ for the distance between two entities on the full readout and $d_T(a,b)$ for their distance on the coarse readout. The procedure requires two noise floors, both measured, neither assumed:

- the **operator floor** $\phi_F(b)$ of the full readout for entity $b$: the maximum pairwise distance among the readings of $b$ produced by independent cross-family operator pairs reading the same material;
- the **aggregator floor** $\phi_T(b)$: the same dispersion computed on the coarse readout itself.

A pair is *resolved* on a readout when its distance exceeds $k$ times the pair floor (the maximum of the endpoints' floors), with $k = 2$ pre-registered. The **metamer criterion** is then a conjunction:

$$\text{metamer}(a,b;T) \iff \frac{d_F(a,b)}{\max(\phi_F(a), \phi_F(b))} > k \;\wedge\; \frac{d_T(a,b)}{\max(\phi_T(a), \phi_T(b))} < 1$$

— resolved as distinct by the full instrument, unresolved by the aggregate readout, both judgments made against measured noise. The criterion is a descendant of signal detection theory's discriminability logic [@green-1966-signal-detection-theory], transplanted to a setting that denies SDT its premises: with no ground-truth signal state and no trial-level noise distribution to estimate, noise is measured instead as cross-operator dispersion, and the discriminability judgment is made twice — once per readout. Its relation to the comparison-of-experiments ordering is likewise empirical rather than derived: the dual-floor test is a sufficient-condition check for garbling-visible information destruction, a companion to the Blackwell order [@blackwell-1951-comparison-of-experiments], not a theorem within it. The **metameric fraction** of aggregator $T$ over a frozen entity bank is the share of resolved-distinct pairs that $T$ leaves unresolved. It is reported per bank and per aggregator with a cluster-bootstrap interval, never as a universal constant.

***Floors, not assertions***

Both halves of the criterion fail informatively. If the full instrument's operators disagree about an entity, $\phi_F$ grows and the pair cannot be resolved — the procedure refuses to certify a distinction the instrument cannot reproduce across its own operators. If the aggregate readout is noisy, $\phi_T$ grows and apparent score collisions stop counting as collapse — the procedure refuses to blame the aggregator for its own measurement noise. This is the nested-floor, no-rescue logic of ground-truth-absent measurement [@zharnikov-2026ay-substrate-floor]: when signal does not exceed the instrument's own noise, the honest output is sub-resolution, and no post-hoc re-weighting of operators is permitted to rescue a finding. The procedure is general: any perceptual instrument with a high-dimensional readout and any coarser projection of it — survey batteries against single items, embedding spaces against similarity scores, multi-dimensional quality readouts against star ratings — can be tested identically.

## The Instrument

***Pre-registered protocol***

PRISM-M instantiates the procedure for AI brand perception under a frozen, pre-registered protocol [@nosek-2018-the-preregistration-revolution] with an explicit confirmatory–exploratory boundary and questionable-measurement safeguards [@flake-2020-measurement-schmeasurement-questionable]. Three hypotheses were pre-registered. H1 (existence): at least one brand pair satisfies the metamer criterion with bootstrap interval support (full-readout signal-to-noise lower bound above 2; aggregator upper bound below 1). H2 (severity): the metameric fraction is monotone in aggregator coarseness — fraction(scalar score) > fraction(ranking) > fraction(full readout) = 0 by construction. H3 (universality): for a fixed aggregator the fraction is stable across cross-family operator pairs within the operator floor. Family-wise $\alpha = .05$ was Bonferroni-split to $.017$ per hypothesis; analyses outside the frozen protocol are labelled exploratory throughout. The design is two-stage: Stage 1 constructs a candidate metamer-pair bank under a frozen retention rule (full-readout signal-to-noise above 2 *and* provisional scalar signal-to-noise below 1; the marginal band between 1 and 2 flagged, not retained); the bank freezes before Stage 2 re-measures it under the full operator set and aggregator battery. Collection halts at the pre-set bank sizes; no optional stopping.

***The stimulus frame***

The brand bank replaces convenience sampling with an explicit frame: the Interbrand Best Global Brands published top-100 ranking, stratified by the five Spectral Brand Theory coherence types [@zharnikov-2026-coherence-type-as-crisis-predictor] crossed with market orientation (B2C/B2B), four brands per cell, 40 brands total. Where a stratum contains fewer than four qualifying index members — a structural scarcity, since identity-concentrated, experiential-asymmetric, and incoherent brands rarely sustain top-global-brand value — a pre-registered supplementation rule completes the cell with the type's canonical exemplar and prominent rubric-matching brands, with index status recorded per brand. Each brand carries a goods-type covariate (experience/search/credence), and balance diagnostics (cell counts, index-member share, category dispersion, assignment-versus-measured-shape agreement) are reported by the analysis code. Explicit stimulus frames with published norms are the emerging standard for brand stimuli [@raffaelli-2024-brand-recognition-norms]; coherence-type assignments were made from public brand knowledge before any readout and are validated against the measured profiles as a diagnostic. The stratification does not stand or fall with the typology: under any alternative typology it functions as a profile-shape diversity device over an external index, and the reported balance diagnostics — not the type labels — carry the representativeness argument.

***Reading brands through channels***

The instrument reads each brand through four standardized public-artifact channels — official communications, press coverage, customer experience reports, and social discourse. For each (brand, channel) cell, a *renderer* model writes 250–400 words of channel-conditioned analytical prose from its exposure to the brand's public artifacts in that channel, and an *extractor* model from a **different provider family** converts the prose into the eight-dimension perception vector (Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal [@zharnikov-2026-spectral-brand-theory-computational-framework]) plus the three aggregator readouts. The renderer-extractor family separation, and the reversal of family roles across the operator set, follow the cross-family operator discipline that prevents one family's priors from setting both the reading and its scoring [@zharnikov-2026ap-same-meaning-different-prose]. Direct elicitation of model-internalized brand perception follows the design of the dimensional-collapse experiments this instrument standardizes [@zharnikov-2026-dimensional-collapse-ai-mediated-search] and the model-as-experimental-subject paradigm [@horton-2023-large-language-models; @filippas-2024-large-language-models]. The channel dimension makes the artifact floor estimable: the same brand read through different channels gives the within-brand dispersion against which same-brand controls are evaluated.

**Table 1.** Cross-Family Operator Pairs (Pinned Model Versions).

| Pair | Renderer (family) | Extractor (family) | Stages |
|------|-------------------|--------------------|--------|
| OP1 | claude-opus-4-8 (Anthropic) | gpt-5.4-mini-2026-03-17 (OpenAI) | 1, 2 |
| OP2 | gpt-5.5-2026-04-23 (OpenAI) | claude-haiku-4-5-20251001 (Anthropic) | 2 |
| OP3 | qwen3.7-max-2026-06-08 (Alibaba) | deepseek-v4-flash (DeepSeek) | 1, 2 |
| OP4 | deepseek-v4-pro (DeepSeek) | qwen3.6-flash-2026-04-16 (Alibaba) | 2 |

*Notes*: Renderer and extractor families never coincide within a pair; each family carries both roles across the set. Operator IDs are exact model-version strings, verified available at collection; temperature 0 where the provider honors it. Stage 1 runs the two family-disjoint pairs; Stage 2 runs all four.

***The aggregator battery***

Three aggregators are tested, each matching a real consumption surface and each formalized as a projection $T$ of the perceptual state [@zharnikov-2026au-correspondence-principle-brand]: **A-SCORE**, a single brand-health grade on an eleven-step scale (A+ through F) mapped linearly to $[0,1]$ — the scorecard surface (ordinal-to-interval linearity is an assumption, mitigated by measuring the scalar floor on the same mapped scale); **A-RANK**, the brand's position in a ten-slot ranked recommendation list, normalized — the AI-search surface; and **A-PICK**, a binary recommend/do-not-recommend call — the agentic surface. All three are extracted from the *same* rendered prose by the *same* cross-family extractor that produced the eight-dimension vector, so aggregator noise is measured under identical conditions, and each aggregator carries its own operator floor. The battery is ordered by coarseness, and H2's monotonicity prediction makes garbling severity a testable property rather than an interpretation: in the comparison-of-experiments ordering, a readout that garbles more should destroy more resolvable structure [@blackwell-1951-comparison-of-experiments].

***The metameric-fraction estimator***

The analysis layer is a deterministic, seeded estimator. Full-readout distance is $1 - \cos(x_a, x_b)$ between brand vectors (channel means, equally weighted, pooled over operator pairs — channel salience is deliberately not modeled); aggregator distance is the absolute difference of normalized scalars. The operator floor of a brand on a readout is the maximum pairwise distance among the brand's per-operator-pair values; the pair floor is the maximum of the endpoints' floors, and per-pair signal-to-noise is distance over pair floor — the per-pair resolution rule of the base instrument [@zharnikov-2026ax-brand-spectrometer]. Uncertainty comes from a source-cluster bootstrap with brands as clusters (2,000 replicates, fixed seed), respecting the non-independence of pairs sharing a brand, per current cluster-robust practice [@mackinnon-2023-cluster-robust-inference] and in-venue bootstrap-interval precedent [@cheung-2023-diy-bootstrapping; @yang-2026-bootstrap-confidence-intervals]; the floor plays the role reliability coefficients play for scale scores [@flora-2020-coefficient-omega-tutorial], adapted to a setting with no latent true score.

***Controls***

Two controls were pre-registered and unit-tested against the estimator before any data collection. The **planted positive**: a synthetic pair engineered to be scalar-equal but profile-distinct (mirror-image strengths on dimensions the scalar averages away) must be flagged metameric — estimator sensitivity. The **same-brand negative**: cross-channel pseudo-pairs of a single brand must *not* be flagged metameric — estimator specificity. Both are evaluated against the same measured floors as real pairs.

## Convergent Validity and the AI-Observer Surface

An instrument-validation reader will ask where the human raters are. The answer is a construct claim, stated explicitly rather than assumed. The aggregate readouts under test — brand-health scores, recommendation rankings, binary picks — are produced by AI systems and consumed *as produced* by downstream surfaces: search results ranked by models, assistants that pick, dashboards that grade. For claims about that deployed surface, the AI observer is the measurement construct itself, not a proxy for a human panel; validating the readouts against human raters would validate a different construct. This inverts the usual direction of the LLM-measurement validity literature, where models are validated against human gold standards precisely because humans are the construct [@rathje-2024-gpt-effective-multilingual; @trott-2024-augment-psycholinguistic-datasets]; the conditions under which LLM-based measurement is defensible — task-matched validation, transparency about what the model stands in for [@abdurahman-2024-perils-opportunities-llms] — are met here by not having the model stand in for anything. The boundary is equally explicit: the moment a claim extends to *human* brand perception, human convergent validity becomes mandatory, and a human-panel companion instrument is the designated vehicle for it. Within this paper, every claim is about the AI-observer surface.

## Results

***Stage 1: bank construction***

Stage 1 read all 40 bank brands through all four channels under the two family-disjoint operator pairs: 640 parsed records from 960 logged calls, zero malformed extractions after the redraw policy. Of 780 candidate pairs, 23 satisfied the frozen retention rule (full-readout signal-to-noise above 2 with provisional scalar signal-to-noise below 1), 19 fell in the flagged marginal band, and the retained pairs — spanning 17 distinct brands — froze as the metamer-pair bank before Stage 2. The retained pairs have strong face validity for the construct: they are dominated by cross-sector pairs whose profiles differ structurally while their scalar grades collide in the mid-range (a project-management software firm against a fast-food chain; an investment bank against an enterprise-software vendor), which is precisely what a scalar-collision phenomenon should look like from above.

***Confirmatory results***

Stage 2 re-measured the 17 frozen-bank brands under all four operator pairs and the full battery: 1,088 parsed records from 1,421 logged calls, zero malformed. **Table 2** summarizes the confirmatory verdicts. At the pre-registered criterion — floors computed across all four operator pairs, $k = 2$, cosine distance — 0 of 136 pairs resolved on the full readout; the maximum pair signal-to-noise was 1.63. With an empty resolved set, no metameric fraction is defined, H1 is not supported, and H2 and H3 are undefined at the confirmatory level. Both controls behaved: the planted positive was flagged metameric, and 0 of 102 same-brand pseudo-pairs were flagged (perfect specificity at the four-operator floor). Per the pre-registered interpretation table, an H1 null is a boundary statement, and this one is unusually specific: it does not say brands are indistinguishable, it says *this four-family instrument cannot certify any brand distinction above its own cross-operator disagreement* — which shifts the question to where that disagreement lives.

**Table 2.** Confirmatory Results at the Pre-Registered Criterion (All Four Operator Pairs).

| Quantity | Value |
|----------|-------|
| Frozen pairs evaluated | 136 |
| Pairs resolved on full readout (S/N > 2) | 0 |
| Maximum pair S/N | 1.63 |
| Metameric fraction (any aggregator) | undefined (0 resolved) |
| H1 (existence) | not supported |
| H2 (severity ladder) | undefined at confirmatory level |
| H3 (cross-operator stability) | undefined at confirmatory level |
| Positive control (planted pair flagged) | passed |
| Negative control (0/102 same-brand pairs flagged) | passed |

*Notes*: S/N = signal-to-noise (pair distance over pair floor). The resolved set is empty because every brand's operator floor is dominated by one discordant operator pair (see Table 3); the pre-registered no-rescue rule forbids dropping it.

***What the floors measured***

Per-brand full-readout floors ranged from .0014 to .0755 while the median brand-pair distance was .0024 — the floors sat above the signal. Decomposing the floors localizes the cause: they are dominated, for every brand, by distances involving one operator pair. **Table 3** gives the concordance table. The three combinations among OP1, OP2, and OP3 — spanning Anthropic, OpenAI, Alibaba, and DeepSeek in both roles — agree to a median per-brand distance of .0009 to .0020. Every combination involving OP4 is five- to ten-fold larger (median .0101 to .0125; maximum .0755). Three of four cross-family operator pairs replicate one another closely; the fourth reads brands differently, and under the no-rescue rule its disagreement becomes everyone's floor [@zharnikov-2026ay-substrate-floor]. The instrument's refusal to resolve is therefore not a malfunction but the designed response to a real property of the operator set — a property the confirmatory analysis surfaced and quantified rather than averaged away.

**Table 3.** Operator-Pair Concordance: Per-Brand Full-Readout Distance Between Operator Pairs.

| Combination | Median | Maximum |
|-------------|--------|---------|
| OP1–OP2 | .0009 | .0037 |
| OP1–OP3 | .0018 | .0078 |
| OP2–OP3 | .0020 | .0057 |
| OP1–OP4 | .0109 | .0675 |
| OP2–OP4 | .0101 | .0698 |
| OP3–OP4 | .0125 | .0755 |

*Notes*: Distances are $1 - \cos$ between the same brand's vectors under two operator pairs, medians and maxima across the 17 Stage-2 brands. Exploratory diagnostic.

***Localizing the discordant operator***

Within OP4, which role diverges — the renderer that writes the reading, or the extractor that scores it? A cross-extractor diagnostic (exploratory, eight logged calls) re-scored one OP1-rendered and one OP4-rendered prose of the same brand-channel cell with all four extractor families. On the OP1 prose, the four extractors agreed within roughly two scale points on every dimension. On the OP4 prose, *all four* extractor families — including the extractors of the concordant pairs — produced markedly lower Economic and Temporal readings, with OP4's own extractor the most extreme. The divergence therefore travels with the prose: deepseek-v4-pro *as renderer* writes a systematically more critical, more discriminating reading of the same brands (its readings span the 2–9 band where the concordant renderers compress into 6–9), and its extractor amplifies rather than causes the difference. The rival interpretation — a malfunctioning operator — does not survive the diagnostic: the renders are coherent prose that every extractor family reads consistently, and systematic-but-different is exactly what a differently-trained observer looks like to a metameric instrument. To this instrument, OP4 is a fourth observer that genuinely perceives differently; whether one wants a floor that spans it depends on whether the deployed surface includes such observers — a scoping decision the concordance diagnostic now makes explicit and quantitative.

***The concordant-triplet picture***

A symmetric leave-one-operator-out sensitivity analysis (exploratory) re-ran the entire frozen pipeline four times, holding out each operator pair in turn. Holding out any concordant pair changes nothing (0 resolved); holding out OP4 restores resolution: 14 of 136 pairs resolve above the triplet floor. **Table 4** reports the metameric fractions within the concordant triplet. The scalar score destroys half of the resolvable distinctions (fraction .500, 7 of 14; bootstrap 95% CI .000–.846); the ranking destroys the fewest (.286, 4 of 14; CI .000–1.000); the binary pick destroys nearly all (.929, 13 of 14; CI .750–1.000). The point ordering — pick > score > rank > full = 0 — runs in the frozen prediction's direction for the pre-registered scalar-versus-ranking contrast, but the paired contrast does not reach the pre-registered threshold (McNemar exact on discordant pairs, 6 score-only versus 3 rank-only, p = .254), while fraction(rank) > 0 does (Holm-adjusted p < .001). Cross-operator stability holds within the triplet: per-operator-pair scalar fractions of .277, .563, and .419 under leave-one-out floors give a dispersion of .286, within the pooled bootstrap half-width of .423 — where operators concord, the fraction is a property of the aggregator, not of the operator. Two further exploratory observations: even at the tighter triplet floor, no single pair clears the strict H1 interval criterion (with four channels per brand, per-pair channel-resampled bootstrap intervals are wide — a design-resolution bound, quantified in Limitations); and the same-brand negative control at the triplet floor flags 10 of 102 pseudo-pairs (9.8%) — a brand's official-channel and social-channel readings can be structurally distinct on the full readout while carrying identical scalar grades. That is simultaneously the specificity boundary of the tighter floor and a substantive within-brand observation: channel-facet metamerism, the score's blindness to a brand's internal perceptual structure.

**Table 4.** Exploratory Metameric Fractions Within the Concordant Operator Triplet (OP4 Held Out).

| Aggregator | Fraction | Count | Bootstrap 95% CI |
|------------|----------|-------|------------------|
| A-PICK (binary pick) | .929 | 13/14 | [.750, 1.000] |
| A-SCORE (scalar grade) | .500 | 7/14 | [.000, .846] |
| A-RANK (ranking slot) | .286 | 4/14 | [.000, 1.000] |
| Full eight-dimension readout | .000 | 0/14 | by construction |

*Notes*: Exploratory; the operator subset was selected post hoc by the symmetric leave-one-out table (only the OP4-held-out variant restores resolution). Fractions are shares of the 14 resolved-distinct pairs left unresolved by each aggregator; source-cluster bootstrap with brands as clusters, 2,000 replicates, fixed seed. Severity ordering by point estimate: pick > score > rank > full; scalar-versus-ranking paired contrast p = .254 (McNemar exact); fraction(rank) > 0 at Holm-adjusted p < .001.

***Robustness***

The sub-resolution verdict is not an artifact of the threshold or the metric: at $k = 3$, under Euclidean distance, and under Mahalanobis distance, 0 pairs resolve; relaxing to $k = 1.5$ resolves exactly one pair, which the scalar then collapses (fraction 1/1). Prompt wording is not the driver either: a terse-prompt ablation subsample (10 brands, one channel, two operator pairs) placed 19 of 20 readings (95%) within one operator floor of their main-prompt counterparts (median shift .24 floors; maximum 1.99). The pattern across all four robustness axes — threshold, metric, prompt, and operator subset — is one-dimensional: everything turns on whether OP4 is inside the floor, and nothing else moves the verdict.

## Alternative Explanations

Two rivals deserve explicit treatment beyond the operator-malfunction account already rejected. First, *grade quantization*: the eleven-step scale mechanically produces collisions, so perhaps the fraction measures the scale's coarseness rather than perceptual garbling. Two observations bound this rival. The scalar floor is measured on the same quantized scale, so collisions below the floor are the deployed readout's actual discriminative behavior — quantization is part of what the surface destroys, not a confound of measuring it. And the ten-slot ranking, of essentially equal cardinality, destroys *fewer* distinctions (.286 versus .500), which a pure-quantization account does not predict: the score and the rank differ in what they ask the observer to collapse, not merely in how many buckets they offer. Second, *positivity compression*: the concordant extractors concentrate readings in the 6–9 band, which deflates full-readout distances for prominent brands and could inflate apparent collisions. This is acknowledged rather than refuted: the planted positive shows the estimator flags genuinely distinct profiles when they exist, but compression bounds the separations real prominent brands can exhibit, and it is listed as a limitation with a direct remedy (calibration prompts or anchor-scored extraction in the next protocol version).

## Discussion

***What a consumer of an aggregate metric can now ask***

The practical payload of the instrument is a pair of questions that were previously rhetorical. To the producer of a brand-health score: *what fraction of the distinctions your full instrument can resolve does your headline number destroy?* — answerable per bank and per aggregator, with an interval. To the consumer of any AI-mediated readout: *does the operator set behind this number agree with itself well enough for the number to certify anything?* — answerable from the concordance table before a single substantive claim is made. The campaign's own answers are instructive in both directions. Where the operator triplet concords, the scalar score destroyed half of the resolvable brand distinctions and the binary pick nearly all of them — the coarser the consumption surface, the more structure dies, in the direction the garbling account predicts [@zharnikov-2026au-correspondence-principle-brand]. And where an operator dissents, the honest answer to *both* questions is "sub-resolution," delivered by the same apparatus that would otherwise have delivered the fraction. The severity ladder also speaks to a long-running measurement debate: the single-item-versus-multi-item question [@bergkvist-2007-predictive-validity-multipleitem; @diamantopoulos-2012-guidelines-single-item; @ailawadi-2003-revenue-premium-outcome] has been argued on predictive-validity grounds; the metameric fraction quantifies its information-destruction side directly — how many resolvable distinctions the single number never sees, whatever its predictive performance.

***A boundary result as validation***

It would have been easy to deliver a cleaner paper: drop the discordant operator, report fraction .500 with its interval, confirm the ladder's direction, and mention the fourth operator in a footnote. The pre-registered no-rescue rule exists precisely to forbid that, and this campaign is a live demonstration of why the rule has teeth. The four-family floor was the honest floor for the operator set as registered; the verdict at that floor is sub-resolution; and everything the concordant triplet shows — including results that favor the instrument's motivating theory — stays behind an exploratory label because the subset was chosen after seeing the concordance table. What elevates the boundary result above a null is that the apparatus explains itself: the concordance diagnostic localizes the floor inflation to one operator pair, the cross-extractor diagnostic localizes it within that pair to the renderer role, and the leave-one-out table shows the localization is exhaustive. An instrument whose failure modes are this legible fails better than most instruments succeed — and the legibility, not the fraction, is the transferable contribution.

## Limitations

Four limitations bound the claims, each mapped to a design remedy. First, **single epoch, pinned operators**: the concordance structure — three families tight, one divergent — is a property of these model versions at this date; model updates can reorder it, and temporal drift is a separate instrument's province. Second, **channel count bounds confirmatory power**: with four channels per brand, per-pair channel-resampled bootstrap intervals are too wide for the strict H1 interval criterion even where point estimates are clear; the remedy is a larger channel set (eight or more), not a weaker criterion, and the design's failure to power its own strictest test is reported as such. Third, **the AI-observer surface is elicited, not fetched, and English-only**: readings draw on the models' internalized public-artifact exposure through channel-conditioned English prompts rather than grounding each reading on fetched artifact excerpts; fetched-artifact grounding is the base instrument's mode, human panels are a companion instrument's, and non-English observation requires native-language operators before any claim extends to it — this campaign measures the English-language AI-observer surface only. Fourth, **fractions are bank-relative**: the frozen bank spans five coherence types and two sectors under an explicit frame, but it is 40 brands from one index; the fraction is a property of the (bank, aggregator, operator set) triple and is reported with all three fixed. Positivity compression of the concordant extractors (see Alternative Explanations) is a fifth, measurement-level caveat with a protocol-level remedy.

## Companion Computation Script

All reported numbers reproduce from the seeded estimator and campaign scripts published with the paper: the two-stage collection harness, the pair-bank freeze, the deterministic estimator (fixed seed 20260702; distances, floors, fractions, bootstrap intervals, hypothesis tests, controls, concordance and leave-one-out diagnostics, robustness battery), and the synthetic-control generators, with a unit suite (10 tests, including both pre-registered controls) that ran before any data collection. Run commands are documented in the code README; the estimator's single entry point is `estimator.py --stage2 <records> --out <results> --robustness`.

## Data and Code Availability

The frozen protocol layers (preregistration, instrument configuration, stimulus bank, pair bank), the parsed measurement records, the analysis outputs, and all computation code are published in the paper's public repository at https://github.com/spectralbranding/sbt-papers/tree/main/prism-m-metamerism; the complete append-only call logs (one record per model API call: prompts, parameters, responses, token usage, cost), together with the protocol layers and records, are archived as a Hugging Face dataset at https://huggingface.co/datasets/spectralbranding/prism-m-metamerism (DOI 10.57967/hf/9398). The campaign comprised 2,416 logged model API calls (Stage 1: 960; Stage 2: 1,421 including the ablation subsample; smoke and diagnostic: 35) at an estimated total cost of 13.40 USD. The paper is archived under concept DOI 10.5281/zenodo.21125785 (this version: 10.5281/zenodo.21125786).

## Acknowledgments

AI assistants (Claude Fable 5, Grok 4.1) were used for initial literature search, for software development — authoring the experiment harness and the analysis and scoring scripts — and for orchestrating and running the reported experiments through those scripts, as well as for editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility. The rendering and extraction models named in Table 1 served as the measurement instrument's operators — study apparatus, not authorship assistance — and their outputs constitute the dataset of record.

## Author Contributions (CRediT)

Dmitry Zharnikov: Conceptualization, Data curation, Formal analysis, Funding acquisition, Investigation, Methodology, Project administration, Resources, Software, Supervision, Validation, Writing — original draft, Writing — review and editing.

## References

::: {#refs}
:::
