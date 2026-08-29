# The Label Moves the Reading: Entity-Name Leakage in Language-Model Dimensional Ratings of a Fixed Text

Dmitry Zharnikov

ORCID: 0009-0000-6893-9231

Concept DOI: [10.5281/zenodo.22161305](https://doi.org/10.5281/zenodo.22161305)

Working Paper v1.0.0 – August 2026

## Abstract

A dimensional rating produced by a language model over a written artifact is normally treated as a reading of that artifact. This study shows it is not purely that. Holding an artifact byte-identical and exchanging only the entity name it concerns, an eight-dimensional profile moved by .55 to .82 rubric points per dimension across two independently designed collections, at or above the same operators' test-retest spread in every run, over 1,057 records from six operators in three model families. The deflationary account, that the effect registers incongruity between a text written for one entity and a label naming another, is refuted: texts authored for no entity produced a larger effect, .824 against .584. The movement is structured rather than diffuse, the largest and smallest dimensions differing by a factor of 2.4 with both extremes reproducing across runs. Which of three routes carries the leakage is not identified, and the study reports why. A re-analysis shows the guard that blocked the decomposition referred its interaction to the entity main effect rather than the within-cell residual; referred correctly, the interaction is roughly five percent of residual. The exchange procedure is offered as a diagnostic for other rubric instruments.

**Keywords**: language models; measurement validity; dimensional rating; entity effects; name bias; instrument diagnostics; pre-registration

---


Instruments that ask a language model to score written material on fixed dimensions are now common enough to have a methods literature of their own. Their readings are treated, and reported, as readings *of* the material scored. That treatment carries an assumption which is rarely stated and, as far as this study can establish, has not been tested directly: that the identity of the entity the material concerns does not itself enter the score.

The assumption is not obviously safe. Adjacent work establishes that form carries meaning-like signal in both people and models. Word form alone predicts valence independently of meaning [@gatti-2024-valence-without-meaning], sound-meaning association is measurable in language models [@marklova-2025-iconicity-large-language; @loakman-2024-ears-see-eyes], and the consumer-research tradition on name sound and preference is older than any of it [@lowrey-2007-phonetic-symbolism-brand; @moorthy-2018-is-nike-female; @motoki-2022-connotative-meanings-sound]. In people, a name inserted into an otherwise fixed vignette moves experimental responses [@majnemer-2022-names-from-nowhere]. What none of that work does is hold a multi-sentence artifact constant while exchanging only the entity label and observing a dimensional profile, which is the measurement this study reports.

The distinction matters because the two designs answer different questions. Rating a word or a pseudoword asks what the form evokes. Rating an artifact asks what the artifact says. If the second question is answered partly by the label, then every downstream use of such a reading inherits a component it did not intend to measure, and the size of that component is an instrument property worth knowing.

## Background

Two literatures use these models for different purposes, and this study belongs to the second. One treats them as stand-ins for human respondents — conditioned models reproducing sub-population response distributions [@argyle-2023-out-one-many], acting as economic agents [@horton-2023-large-language-models], and the question of whether they can replace human participants at all [@dillion-2023-can]. The other treats them as instruments and studies how they produce a rating. The measurement reported here belongs to the second, but it bears directly on the first: **if a rating of a byte-identical text moves with the entity label, then any design that varies entity names across conditions carries an uncontrolled component of exactly this size.** That is a consequence for the substitution literature which follows from an instrument result, and it is stated here rather than left to the reader.

That entity identity can bias a language model's output is itself established: brand identity systematically shifts model judgements between global and local brands [@kamruzzaman-2024-global-good-local], and the broader use of these models as psychological assessors now has its own review literature [@brickman-2025-large-language-models]. What that work leaves open is whether identity enters a rating that is nominally *of a fixed text*, which is the question here.

The closest instrument-level neighbours make the point by contrast. Language models produce dimensional ratings that correlate with human norms well enough to augment psycholinguistic datasets, including under a contextualized condition where the rated item is embedded in surrounding material [@trott-2024-augment-psycholinguistic-datasets], and their perceptual judgments of stimuli can be compared directly against human judgments on the same items [@dickson-2025-comparing-perceptual-judgments]. Recent work in the same venue examines how context assembles the lexical functions such ratings draw on [@kello-2025-contextual-assembly-lexical], which is the mechanism a label would have to act through. In both cases the rated object is the thing the rating is about. The manipulation reported here leaves the rated object untouched and changes only what it is *called*, which is why it isolates a component neither design can see: contextualization varies the surroundings of the rated item, whereas a name exchange varies the identity claim while holding the surroundings fixed.

### *What this study establishes, and what it does not*

Two things are established. The effect exists and reproduces across two collections built on different texts and different name sets. The most obvious deflationary explanation for it is false.

One thing is not established, and the study is organised so that this is visible rather than buried. Three routes could carry the leakage — what the model has stored about the particular entity, mere familiarity with it, or the name as a bare token sequence — and the collected design cannot separate them. The study reports the barrier, re-analyses it, and states what a design that cleared it would need.

### *Scope*

Every claim here concerns language-model cohorts and the readings they produce. Nothing in it is a claim about people, and the silicon-sample cautions apply in full [@sarstedt-2024-using-large-language]. The instrument is a constrained, theory-scored dimensional rubric; whether the same holds for open-ended dimensional batteries is untested. The material is nine entity names in one product domain, in English, in artifacts of roughly a paragraph.

## Method

### *The instrument and the operators*

The rubric scores a written artifact on eight fixed dimensions, each on a 1-10 integer scale: semiotic, narrative, ideological, experiential, social, economic, cultural and temporal. The dimension set and its exact wording are fixed by a published multilingual prompt file that forms part of a prior study's instrument, so the rubric administered here is not authored for this study and cannot be adjusted to suit it. The operator returns one integer per dimension and no free text; a response that cannot be parsed into eight integers is recorded as a parse failure rather than coerced.

An example makes the manipulation concrete. One artifact reads, in part, *"{entity} adds to its range slowly and removes from it rarely. Decisions about what to make are taken by people who cook, and are argued over for longer than the market would prefer."* In one cell `{entity}` is filled with a prevalent real cookware brand and in another with an invented one; every other byte, including sentence order and punctuation, is identical, and the two profiles are compared.

Table 1: The operator pool.

| Operator | Family | Decoding |
|---|---|---|
| OP1 | A | temperature and top-p not accepted; provider defaults |
| OP2 | A | temperature accepted; top-p not accepted |
| OP3 | B | temperature and top-p not accepted; provider defaults |
| OP4 | B | temperature and top-p accepted |
| OP5 | C | temperature and top-p accepted; output cap 16,000 tokens |
| OP6 | C | temperature and top-p accepted; output cap 16,000 tokens |

*Notes*: Three families, two operators each. Exact model identifiers are pinned literally in the released protocol rather than named here, because they are long version strings and the protocol is the authoritative record. Decoding parameters differ across operators because the providers accept different ones; the protocol records what each accepts and the harness sets only what is accepted rather than silently dropping a parameter. Output caps are set far above what the response needs, after one operator returned 13 empty responses in 144 at a cap that appeared ample. The roster admits no reserves: a retired pin halts collection rather than being substituted, because substituting into a frozen roster changes the instrument mid-series. It was administered to six operators drawn from three model families, each operator seeing a prompt that differs from its neighbours in exactly one slot. Model identifiers are pinned literally in each collection's protocol rather than resolved at runtime, because two independently collected runs are compared against each other and an operator that changed silently between them would be indistinguishable from the effect under test.

The operator pool is drawn from commercially served models rather than open-weight ones, and that choice costs something the study should name. Open-weight models can be versioned and inspected by the researcher, which is the stronger position for transparency and reproducibility [@hussain-2024-tutorial-open-source]. The offsetting consideration here is that the instrument whose behaviour is under study is administered through commercial endpoints in its ordinary use, so a pool composed entirely of open-weight models would measure a different instrument from the one in question. Literal pinning plus full call logging is the mitigation, not a substitute: it fixes what was used and makes the mismatch auditable rather than removing it. Whether the leakage measured here survives on an open-weight pool that the researcher can actually version is a stated open question.

Every call is logged with its prompt hash, parameters and response, and the harness enforces a completeness gate that refuses a partial run rather than analysing one. Purpose-built packages for language-model behavioural experimentation now exist and set a reasonable floor for what such logging should capture, including responses and token probabilities [@duan-2024-macbehaviour-r-package]; the harness used here meets that floor for responses and adds prompt-purity verification, which checks that arms differ in exactly one slot, and checksummed pre-registration of the protocol, stimuli and analysis code. It does not capture token probabilities, which is a real gap for anyone wanting to model the reading's uncertainty rather than its location. Reporting follows the consensus checklist for language models in behavioural science [@feuerriegel-2026-reporting-checklist-large]; the item-by-item mapping is released with the dataset.

### *The contrast*

The manipulation exchanges the entity name and nothing else. Within a name contrast the artifact text is byte-identical; the name occupies a single slot in an otherwise fixed paragraph. The design substitutes rather than removes: no artifact is ever presented with its entity struck out, because an ablated artifact is both incongruous and still carries the entity in its residual content, so a reading taken from it answers the mismatch rather than the missing prior.

### *The magnitude and its yardstick*

A name-exchange magnitude is the Euclidean distance between two entities' profiles over the same text and the same operator, divided by the square root of the number of dimensions, which returns it to the instrument's per-dimension scale. Magnitudes are reported both in rubric points and in units of the instrument's own test-retest spread — the same operator's variation over repeat presentations of an identical prompt. A magnitude above 1.0 in those units means exchanging a name moves the reading further than re-asking the same question moves it.

The choice of yardstick is a stated assumption rather than a neutral one. A between-operator reference would be wider and would make the same effect look smaller; both are available in the released records.

### *Two collections*

The first collection paired four artifact texts, each written for a specific prevalent brand, against an invented name. The second was built to break that design's confound: nine entities across three prevalence strata — three prevalent, three low-prevalence, three invented — crossed with four artifacts authored for no entity, yielding 36 name pairs per text in four classes. Both collections ran twice, independently.

### *The reproduction requirement*

Every verdict must hold in both runs. A verdict that differs between them is **removed, not confirmed**. This rule is applied without exception and it has removed verdicts in this program before.

## Results

### *The effect, and its reproduction*

Exchanging the entity name over byte-identical text moved the eight-dimensional profile in every run of both collections (Table 2).

Table 2: Name-exchange magnitude across two collections and four runs.

| Collection | Texts | Per dimension | In test-retest units | Records |
|---|---|---|---|---|
| First | 4, each written for a specific brand | .584 / .523 | 1.194 / 1.016 | 193 |
| Second | 4, written for no entity | **.824 / .825** | 1.152 / 1.092 | 864 |

*Notes*: Values are run 1 / run 2, reported separately and never pooled. Test-retest units are multiples of the same operator's spread over repeat presentations of an identical prompt; above 1.0 means the exchange moves the reading further than re-asking does. Six operators across three model families in both collections; no instrument failures in either.

The magnitude clears the instrument's own replicate noise in all four runs, and the second collection's two runs agree to three decimal places. Both collections returned every planned cell.

On the second collection's 864 records per run the aggregate is estimated tightly: mean .824, 95% CI [.793, .855] in run 1, and mean .825, 95% CI [.794, .856] in run 2. Both intervals lie entirely above the test-retest reference the magnitude is judged against.

Decomposing the same records over their crossed factors places the variance where it matters for what follows. The artifact accounts for 17.9% and 16.8% of total sum of squares across the two runs, the operator for 7.2% and 6.1%, and the name class for **.6% and .5%**; the remainder is within-cell. The name class — the factor the decomposition of interest is defined over — is the *smallest* of the three, which is the first indication that a ratio referred to it will not be stable.

### *Against the incongruity account*

The obvious deflationary reading is that the effect registers a mismatch: an artifact written for one entity carries traces of it, and attaching a different label creates an incongruity the model detects. That account predicts that artifacts written for no entity should shrink the effect toward noise.

They enlarged it, from .584 to .824 per dimension — a 41% increase on texts authored for nobody. The effect is not a mismatch artifact of the first collection's stimulus construction, and the account is rejected.

### *The leakage is structured, and the structure reproduces*

The movement is not spread evenly over the eight dimensions (Table 3). The largest and smallest dimensions differ by a factor of 2.39 in the first run and 2.38 in the second, and the ordering agrees: the semiotic dimension moves most in both runs, the ideological dimension least in both.

Table 3: Per-dimension movement under a name exchange, second collection.

| Dimension | Run 1 | Run 2 |
|---|---|---|
| Semiotic | **.859** | **.839** |
| Cultural | .742 | .728 |
| Social | .659 | .679 |
| Economic | .542 | .542 |
| Experiential | .499 | .520 |
| Temporal | .492 | .583 |
| Narrative | .490 | .466 |
| Ideological | **.360** | **.353** |

*Notes*: Mean absolute movement in rubric points, over all name pairs within a text and operator. Ordered by run 1. The root mean square over dimensions reproduces the aggregate of .824 and .825 reported in Table 2, which is the validation the producing script runs before reporting.

This matters for what the effect can be. A process that merely added noise when the label changed would not produce a dimension ordering that reproduces across independently collected runs; the agreement on both extremes, and a max-to-min ratio matching to two decimal places, is not what noise looks like. That the semiotic dimension — the one concerned with signs and naming — absorbs the most movement, and the ideological the least, is coherent with leakage rather than with instability, though the study does not test that reading and it is offered as an observation rather than a mechanism.

### *Against a prevalence account*

A second rival holds that leakage tracks how well known an entity is, so that what looks like a label effect is a memorised-prior effect. A pre-registered test regressed frame-sensitivity on corpus prevalence in four variants across two runs. None of the eight estimates reached significance, seven of the eight pointed opposite to the predicted direction, and the stratum means showed no gradient in either run — the most prevalent stratum carried the largest effect both times, and invented entities, which have no prior to anchor, were among the smallest.

This bounds what may be concluded. The test addresses *prevalence*, not whether the model knows the entity at all, and the two must not be collapsed. It is also a failure to reject rather than an equivalence test, so it does not license the claim that the reading is invariant to fame.

### *What is not settled*

Three routes remain: prior content about the particular entity, familiarity independent of content, and the name as a bare token sequence. The second collection contains the contrast that would separate them — real entities against real entities at matched prevalence, alongside invented against invented — and those class means are not reported here.

They are withheld because the collection's pre-registered neutrality guard did not return the same verdict in both runs, and its precedence rule bars reading the class contrasts when it does not. Under the reproduction requirement a guard that flips cannot license reading past it. The decomposition is therefore recorded as **not identified**, and the class means are not reported in any form, including as suggestive.

### *What the guard was measuring*

The guard tested whether the artifacts are neutral with respect to entity — whether a text suits some names better than others — by comparing a text-by-entity interaction against the *entity main effect*. That comparison has a structural defect: the reference quantity moves with the main effect and with replicate count, while the interaction it is meant to calibrate does not. The variance decomposition above shows the defect is not hypothetical here — the class effect is roughly half a percent of total variance, so a ratio taken against it is a ratio of two small quantities, and small quantities in a denominator are what produce a verdict that flips.

Referred instead to the within-cell residual, the same records give a different picture (Table 4).

Table 4: The text-by-entity interaction under the within-cell residual.

| | Run 1 | Run 2 |
|---|---|---|
| Interaction mean square | .2178 | .1959 |
| Residual mean square | .1764 | .1808 |
| $F(9, 848)$ | 1.235 | 1.084 |
| $\mathrm{SD}_{\text{interaction}} / \mathrm{SD}_{\text{residual}}$ | .066 | .039 |

*Notes*: The .05 critical value at these degrees of freedom is approximately 1.89; neither run approaches it. The estimating pipeline reproduces the collection's own published aggregate name effect to .824 and .825 before any ratio is reported, and refuses to report otherwise.

The interaction is roughly five percent of the residual in both runs. The blocking verdict was therefore a property of the reference quantity rather than of the data.

This does **not** establish that the artifacts are neutral. A non-significant $F$ is a failure to reject, and neutrality is a claim that requires an equivalence statement — an upper bound on the interaction that sits below a threshold defensible in advance. What it establishes is narrower and still consequential: the quantity that blocked the decomposition was not the quantity that should have been consulted.

### *How tightly neutrality could be bounded*

A Monte Carlo at the measured ratio gives the upper confidence limit a design of each size could defend (Table 5).

Table 5: Upper 95% confidence limit on the interaction-to-residual ratio, by number of artifacts.

| Artifacts | 4 | 8 | 12 | 16 | 20 | 24 | 32 | 48 |
|---|---|---|---|---|---|---|---|---|
| Upper limit | .159 | .130 | .117 | .108 | .103 | .100 | .094 | .086 |

*Notes*: 3,000 simulated experiments per column at the measured ratio of .053, fixed seed, cell counts matching the collected design. Returns flatten after roughly twenty-four artifacts.

The collected four-artifact design can bound the ratio only below .159, which is why the existing records cannot settle neutrality even though their point estimate is small. Sixteen artifacts would reach .108 and twenty-four .100.

The bound against which such a limit should be judged is not proposed here. A threshold chosen because an affordable design happens to reach it is not a threshold, and equivalence procedures differ in what they can discriminate at these sample sizes [@linde-2023-decisions-about-equivalence].

## Discussion

The finding is a property of an instrument, not of a brand, a category or a person. What it says is that this class of constrained rubric instrument, as instantiated here, returns a number that is partly about the label on the material rather than the material, and that the component is large enough to see against the instrument's own noise. How far that travels to other rubrics is the question the diagnostic below exists to let other people answer on their own instruments.

### *What a reader of any such instrument can do about it*

The procedure is portable, though this study demonstrates it on one instrument only. Take an artifact, score it, exchange the entity name for another of matched type, score it again, and express the difference in units of the same operator's test-retest spread. The result is an estimate of how much of the instrument's reading the label carries.

The estimate is a lower bound unless it is paired with a second measurement: a blind probe asking whether the original entity remains identifiable from the text once the name is exchanged. If it does, the exchange relabelled the artifact without removing what the model knew, and the leakage measured is only the part that survived. That probe is specified below and has not been run.

### *What it means for studies that use these models as respondents*

The most likely objection from the substitution literature is that an instrument result does not obviously matter to a design that uses models as participants. It does, and the mechanism is direct. A silicon-sample study that presents different entities to different conditions — different brands, different firms, different named actors — is varying the label alongside whatever it means to vary, and the readings it collects carry a component attributable to the name rather than to the manipulation. The size measured here is at or above the same operators' test-retest spread, so it is not negligible relative to the noise such designs already accept. **The remedy is cheap and is the diagnostic above**: run the exchange on a handful of the study's own stimuli and report the number, rather than assuming it is zero.

### *Why the denominator result is worth reporting separately*

A neutrality guard is a gate: it decides whether a downstream analysis may be read. This one blocked a decomposition on a comparison whose reference quantity was inappropriate, and the block looked like a finding about instability in the data. It was not. Guards of this shape are common in pre-registered designs precisely because they are meant to be decided in advance, which also means their defects are locked in before anyone sees whether they matter.

The general form of the lesson is that a threshold must be stated relative to the value the statistic takes when the effect is absent. A ratio that moves with a nuisance quantity does not have a stable null to be judged against.

### *Limitations*

The route carrying the leakage is unidentified, and this study does not claim otherwise. The first collection's contrasts each paired a prevalent real entity against an invented one, so that collection alone cannot separate what a model knows about an entity from the unfamiliarity of an invented name; the second collection resolves that confound by design, and reading it is what the guard blocked. The material is nine names in one product domain, so transfer to other categories is untested. No human comparison was collected, so the effect cannot be sized against what a label does to a person reading the same text; the nearest human evidence is on a different response class [@majnemer-2022-names-from-nowhere]. Most consequentially, whether the exchanged name removes what the model knows has not been measured, so every magnitude reported here may be a lower bound.

### *Pre-registered continuation*

Three things are specified in advance and none has been run. A blind multi-family recovery probe, scored against the exchange's own variant list, run to completion before any further outcome collection. A re-estimation on sixteen to twenty-four artifacts, sufficient to bound the interaction tightly enough to license the decomposition. And a decision, taken in writing before that collection rather than after it, on which equivalence procedure the bound is stated under.

## Data and Code Availability

This paper is archived at [10.5281/zenodo.22161305](https://doi.org/10.5281/zenodo.22161305), which always resolves to its most recent version; version 1.0.0 is [10.5281/zenodo.22161306](https://doi.org/10.5281/zenodo.22161306).

### *The dataset of record*

The instrument records for both collections are released in full: every call with its prompt hash, parameters and response, alongside the frozen protocols, stimulus packs and freeze records that fix what was decided before collection began. The freeze records carry SHA-256 checksums for the protocol, the stimulus pack and the analysis code, so a reader can confirm that the analysis was written against the pre-registration rather than against the data.

### *Companion computation script*

The reported re-analysis and both simulations are reproducible from published scripts. `estimate_guard_ratio.py` produces Table 4, `equivalence_power.py` produces Table 5, `per_dimension_leakage.py` produces Table 3, and `simulate_guard_power.py` produces the guard-reproducibility analysis referenced in the discussion. Each carries a fixed seed and its run command in its docstring; all three were run twice and produce byte-identical output. `estimate_guard_ratio.py` validates itself against the collection's own published aggregate before reporting and exits without reporting if that validation fails.

## Acknowledgments

AI assistants (Claude, Gemini, Grok, GPT and DeepSeek model families) were used for initial literature search, for software development — authoring the experiment harness and the analysis and scoring scripts — and for orchestrating and running the reported experiments through those scripts, as well as for editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility. The language models in the operator pool functioned as measurement instruments, not as authors.

## Author Contributions (CRediT)

Conceptualization, methodology, investigation, formal analysis, writing — original draft, writing — review and editing, and supervision: Dmitry Zharnikov. The author is solely responsible for the study design, the pre-registered decision rules, the interpretation of the results, and the decision to report the route decomposition as unidentified.

## References
