# PRISM: A Structured Measurement Instrument for Multi-Dimensional Brand Perception

**Dmitry Zharnikov**

DOI: 10.5281/zenodo.19555265

Working Paper -- April 2026

---

## Abstract

Measuring brand perception requires instruments that capture multi-dimensional structure rather than collapsing it to a single equity score. This paper specifies PRISM (Perception Response Instrument for Structured Measurement), a family of standardized instruments for eliciting multi-dimensional brand perception from both artificial intelligence and human observers within the Spectral Brand Theory framework. The paper makes three contributions. First, it formalizes the PRISM architecture as a five-layer scaffold (L0 specification, L1 configuration, L2 prompts, L3 sessions, L4 analysis) that is domain-neutral and reproducible. Second, it provides the complete PRISM-B (Brand) specification: eight scale items mapped one-to-one to SBT dimensions, a 1--5 ordinal response format empirically demonstrated as the minimum-distortion operating point for AI observers across 17 large language model architectures (with human validation pending), an exact prompt template, and a scoring algorithm comprising the Dimensional Collapse Index and cross-observer cosine convergence. Third, it situates PRISM-B within a measurement family (PRISM-M for metamerism discrimination, PRISM-T for temporal tracking, PRISM-C for choice prediction) and establishes connection to multi-observer triangulation via Perception DOP. The instrument is specified here; validation against human-subject data is a separate future study.

**Keywords**: brand perception measurement, psychometrics, instrument design, Spectral Brand Theory, large language models, dimensional collapse, scale development, observer heterogeneity

---

Brand perception is multi-dimensional, yet existing measurement instruments face a structural limitation: they were designed for a world in which one type of observer -- the human consumer -- was the only observer that mattered. Churchill's (1979) paradigm for developing marketing constructs, and the instruments it produced, assume a homogeneous observer population whose responses can be aggregated without modeling observer-type differences. This assumption held when all brand encounters were human encounters. It fails when AI systems increasingly mediate consumer brand evaluation (Hermann and Puntoni 2024), generating brand assessments that structurally differ from human perception (Li, Castelo, Katona, and Sarvary 2024; Sabbah and Acar 2026). Ali (2025) demonstrated that generative AI reshapes perceived brand authenticity and consumer brand image, while France (2025) updated the Yoo-Donthu framework for digital brand equity, confirming that established measurement instruments require adaptation for technology-mediated brand encounters. The measurement problem is no longer "how do consumers perceive this brand?" but "how do different types of observers -- human cohorts, AI models, behavioral proxies -- perceive this brand, and how do we compare their perceptions on a common scale?"

Existing multi-dimensional instruments cannot answer this question because they were not designed to. Aaker's (1997) Brand Personality Scale measures trait attributions (sincerity, excitement, competence, sophistication, ruggedness) derived from factor analysis of human personality lexicons. Brakus, Schmitt, and Zarantonello's (2009) Brand Experience Scale measures experiential reactions (sensory, affective, behavioral, intellectual) that presuppose embodied consumer encounters. Yoo and Donthu's (2001) consumer-based brand equity scale measures loyalty, awareness, and perceived quality -- downstream outcomes of brand perception, not the dimensional structure of the perception itself. Geuens, Weijters, and De Wulf (2009) refined brand personality measurement but retained the personality-trait construct. None of these instruments measures which categories of brand *signal* an observer attends to, and none was designed for administration to AI observers without fundamental construct mismatch.

**Table 2.** Comparison of Multi-Dimensional Brand Measurement Instruments.

| Instrument | Construct (n dims) | Derivation | Observers | Format |
|:-----------|:-------------------|:-----------|:----------|:-------|
| Aaker BPS (1997) | Personality traits (5) | Factor analysis | Human only | 1--5 Likert |
| Brakus BXS (2009) | Experiential reactions (4) | Factor analysis | Human only | 1--7 Likert |
| Yoo-Donthu CBBE (2001) | Brand equity outcomes (3) | Factor analysis | Human only | 1--5 Likert |
| Geuens et al. (2009) | Personality traits (5) | Factor analysis | Human only | 1--7 Likert |
| **PRISM-B** | **Signal reception (8)** | **Theory-derived** | **AI + Human** | **1--5 ordinal** |

*Notes:* Factor analysis instruments derive dimensions from exploratory or confirmatory analysis of human response data. PRISM-B derives dimensions from the SBT signal taxonomy prior to measurement. Only PRISM-B can be administered to AI observers without construct mismatch.

This paper argues that the measurement gap is not merely an absence of instruments but a consequence of how instruments have been designed. The dominant paradigm -- Churchill (1979), refined by Rossiter (2002) and implemented by Brakus et al. (2009) -- derives dimensions empirically from human response patterns. Dimensions discovered this way are necessarily human-specific: they capture variance in human responses but provide no guarantee that the same dimensional structure applies to non-human observers. An instrument designed for commensurable AI-human measurement must instead derive its dimensions from the *signal* side -- what the brand emits -- rather than the *response* side -- how one particular observer type reacts. This signal-side derivation is what Spectral Brand Theory provides.

Spectral Brand Theory (SBT; Zharnikov 2026a) proposes that brand perception can be modeled as emission across eight typed dimensions (Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal) received by heterogeneous observer cohorts. Empirical work within SBT has demonstrated that these dimensions exhibit systematic observer-dependent variation: LLMs collapse perception toward Economic and Experiential dimensions (Zharnikov 2026v), cross-model convergence is extreme (cosine .977 across 24 architectures), and the magnitude of collapse depends on response format (Zharnikov 2026aa). Brand triangulation (Zharnikov 2026y) has formalized how multiple observers can be combined to recover brand emission profiles. A growing literature on LLMs as survey respondents (Argyle, Busby, Fulda, Gubler, Rytting, and Wingate 2023; Horton 2023; Sarstedt, Brand, Ringle, and Dolz 2024) has established that AI systems can generate survey-like responses, but has not addressed the instrument design question: what measurement format minimizes distortion across observer types?

This paper addresses that question. It specifies PRISM (Perception Response Instrument for Structured Measurement), defines its architecture, and provides the complete PRISM-B variant for brand perception measurement. The paper deliberately separates specification from validation: specifying the instrument requires formalizing what the items are, how they are scored, and why the format was chosen; validating the instrument requires human-subject data that is the target of a separate study. The distinction follows psychometric convention: test specifications (e.g., Educational Testing Service 2014) precede and are distinct from validity evidence reports.

Three contributions structure the paper. First, the PRISM architecture defines a reusable five-layer scaffold that separates protocol from domain content, enabling instrument variants to share infrastructure while varying items (developed in "PRISM Architecture"). Second, the PRISM-B specification provides the eight items, response format, prompt template, and scoring algorithm for brand perception measurement, with the response format justified by rate-distortion evidence as a novel application of Shannon's (1959) rate-distortion theory to psychometric format selection -- building on Sims's (2016) theoretical work connecting information-theoretic capacity limits to human perceptual judgment (developed in "PRISM-B Specification" and "Scoring Algorithm"). Third, the connection to multi-observer estimation via Perception DOP establishes how individual PRISM-B administrations aggregate into triangulated brand positioning (developed in "Multi-Observer Estimation and Perception DOP").

---

## PRISM Architecture

### *The Five-Layer Scaffold*

PRISM defines a five-layer measurement scaffold that separates the reusable protocol infrastructure from domain-specific content. The scaffold is the constant across all PRISM variants; specific instruments inherit the scaffold and add domain-specific prompts, items, and analysis routines.

**L0: Specification.** The pre-registered protocol layer. Contains hypotheses, stopping rules, brand/observer selection criteria, planned analyses, and alpha allocation. L0 is written and frozen before any data collection begins. Its purpose is to enforce the confirmatory-exploratory boundary (Nosek, Ebersole, DeHaven, and Mellor 2018): analyses specified at L0 are confirmatory; all others are exploratory regardless of their statistical significance.

**L1: Configuration.** The technical infrastructure layer. Contains model backend definitions (API endpoints, authentication, model identifiers), observer cohort definitions (for human administration), response format parameters (scale points, output schema), temperature and sampling parameters, and retry/timeout policies. L1 is declarative: it specifies what is measured and how the measurement infrastructure is configured, not the content of what is asked. In the AI observer context, L1 is implemented as a YAML configuration file; for human administration, L1 specifies the survey platform, randomization procedure, and demographic collection protocol.

**L2: Prompts.** The item layer. Contains the exact wording of each measurement prompt, the structured output schema (JSON for AI observers, Likert display for human respondents), version identifiers, and language variants. L2 is the only layer that differs across PRISM variants: PRISM-B has brand perception items, PRISM-M has metamerism discrimination items, PRISM-T has temporal comparison items. The prompt template is versioned so that cross-study comparisons can verify item equivalence.

**L3: Sessions.** The raw data layer. Every administration produces a session record containing the full prompt sent, the raw response received, the parsed structured output, observer metadata (model identifier for AI, demographic profile for human respondents), a timestamp, and a response validity flag. L3 is append-only and immutable: no session record is modified or deleted after collection. This ensures auditability and permits re-analysis with updated scoring algorithms. For AI observers, L3 is implemented as a JSONL file (one JSON object per API call). For human respondents, L3 is the equivalent raw response export from the survey platform.

**L4: Analysis.** The statistical computation layer. Contains scoring scripts that operate on L3 data to produce dimensional profiles, collapse indices, convergence metrics, and confidence intervals. L4 scripts are versioned alongside the instrument and are deterministic: given the same L3 data, they produce identical outputs. The analysis layer implements the scoring algorithm specified in the instrument definition (see "Scoring Algorithm" below).

### *Design Principles*

Three design principles govern the scaffold.

*Separation of concerns.* Each layer has a single responsibility. Changing the response format (L1) does not require changing the items (L2). Adding a new hypothesis (L0) does not require modifying the data collection infrastructure (L1/L3). This separation permits controlled experimentation on each layer independently -- for example, testing whether a 1--5 ordinal format outperforms a 1--7 format while holding items and analysis constant.

*Reproducibility by construction.* The combination of L0 (frozen protocol), L1 (declarative configuration), L2 (versioned prompts), and L3 (immutable session data) ensures that any PRISM study can be reproduced by forking the instrument repository and re-executing the L1 configuration against the same observer population. For AI observers, exact reproduction requires specifying model version identifiers; for human respondents, it requires equivalent sampling procedures.

*Observer-agnostic design.* The scaffold treats AI and human observers symmetrically. Both produce L3 session records in a common schema. Both are scored by the same L4 algorithms. The only differences are in L1 (API configuration vs. survey platform configuration) and L2 (JSON output schema vs. Likert display rendering). This symmetry enables the multi-observer estimation developed in "Multi-Observer Estimation and Perception DOP," where AI and human PRISM-B administrations are combined as distinct observer cohorts in a unified triangulation framework.

---

## PRISM-B Specification

### *Construct and Dimensional Mapping*

PRISM-B measures the observer's perceived intensity of a focal brand's signal across each of the eight SBT dimensions. Each item targets exactly one dimension. The construct is brand emission perception -- how intensely the observer perceives the brand's signal on a specific dimensional channel -- not brand personality, brand conviction, or purchase intention. The distinction is critical: brand personality instruments (Aaker 1997) measure trait attributions; brand conviction (the observer's formed assessment of a brand) is a downstream construct that depends on both the brand's emission and the observer spectral profile (Zharnikov 2026a). PRISM-B measures signal reception at the dimensional level, upstream of conviction formation.

### *Items*

Eight items, one per SBT dimension, administered for a focal brand:

**Table 1.** PRISM-B Scale Items.

| Item | Dimension | Signal Domain |
|:-----|:----------|:-------------|
| P1 | Semiotic | Distinctive visual identity, symbols, and design language |
| P2 | Narrative | Storytelling, founding mythology, and brand narrative |
| P3 | Ideological | Stated values, ethical commitments, and ideological positioning |
| P4 | Experiential | Product experience, sensory qualities, and functional performance |
| P5 | Social | Community belonging, status signaling, and social identity |
| P6 | Economic | Pricing strategy, value proposition, and economic positioning |
| P7 | Cultural | Cultural resonance, regional identity, and lifestyle alignment |
| P8 | Temporal | Heritage, longevity, temporal depth, and historical continuity |

*Notes:* Common stem for all items: "How strongly does [BRAND] communicate through [signal domain]?" where [BRAND] is the focal brand name. Response scale: 1 = Not at all, 2 = Slightly, 3 = Moderately, 4 = Strongly, 5 = Very strongly. Items are administered in fixed order (P1--P8) for AI observers; randomized order is recommended for human respondents. The stem targets perceived signal intensity, not evaluative judgment.

### *Response Format: 1--5 Ordinal Scale*

Each item is rated on a five-point ordinal scale:

1 = Not at all
2 = Slightly
3 = Moderately
4 = Strongly
5 = Very strongly

The five-point format is not arbitrary. It is the empirically observed minimum-distortion operating point for AI observers, derived from rate-distortion analysis of AI brand perception encoders. Zharnikov (2026aa) tested five response formats spanning 3 to 26 bits of information capacity across 17 LLM architectures and five canonical reference brands. The 1--5 ordinal format (approximately 19 bits, computed as log~2~(5^8^) = 18.6 bits for eight items) achieved the lowest distortion from canonical brand profiles, outperforming both the higher-rate 100-point allocation format (approximately 26 bits) and lower-rate formats. The effect is large: paired *t*(16) = 11.92, *p* < .001, Cohen's *d*~z~ = 2.89 for the 100-point versus 1--5 comparison. All 17 architectures from distinct training lineages exhibited this pattern without exception.

The mechanism is encoder bias suppression: when the response space is unconstrained (100 points across eight dimensions), LLM encoders express idiosyncratic training-corpus biases that increase distortion. The bounded five-point format constrains the output alphabet sufficiently to suppress these biases while preserving enough resolution to capture meaningful dimensional differentiation. This result is a concrete instance of the rate-distortion prediction formalized by Sims (2016), who demonstrated that human perceptual capacity limits produce optimal categorical encodings at intermediate rates -- precisely the pattern observed here for AI encoders. The parallel extends to human survey methodology, where Krosnick (1991) documented satisficing under cognitively demanding formats and Schwarz (1999) showed that response scales shape answers by providing implicit frames of reference. The convergence of information theory (Sims 2016), AI encoding (Zharnikov 2026aa), and survey design (Krosnick 1991; Schwarz 1999) on the same conclusion strengthens the format choice beyond any single line of evidence.

For human respondents, the five-point scale has a well-established psychometric literature. Five-point Likert scales provide adequate reliability for group-level comparison while imposing minimal cognitive load (Preston and Colman 2000). The convergence of the AI-optimal format with established human survey practice is fortuitous but practically important: it means the same response format can be administered to both observer types without methodological compromise.

### *Prompt Template for AI Observers*

The exact prompt template for PRISM-B administration to AI observers is:

```
You are evaluating the brand [BRAND] on eight dimensions of brand perception.
For each dimension, rate how strongly [BRAND] communicates through that channel
on a scale of 1 to 5, where 1 = Not at all, 2 = Slightly, 3 = Moderately,
4 = Strongly, 5 = Very strongly.

Respond in JSON format with the following keys:
{
  "semiotic": <1-5>,
  "narrative": <1-5>,
  "ideological": <1-5>,
  "experiential": <1-5>,
  "social": <1-5>,
  "economic": <1-5>,
  "cultural": <1-5>,
  "temporal": <1-5>
}

Evaluate based on your knowledge of the brand. Provide only the JSON.
```

Design decisions in the template:

*No preamble or persona assignment.* The prompt does not ask the model to "act as a consumer" or "imagine you are a brand expert." Persona prompts introduce confounds: they measure the model's simulation of a persona rather than its baseline brand perception encoding.

*Structured JSON output.* The response schema eliminates parsing ambiguity. Models that support structured output modes (function calling, JSON mode) should use them; models that do not are prompted for JSON and parsed with tolerance for minor formatting deviations.

*Dimension labels without definitions.* The prompt uses the dimension name (e.g., "semiotic") without providing the full SBT definition. This is deliberate: it measures what the observer encodes under each dimensional label using its own trained understanding, not its ability to follow an externally provided rubric. This design choice means PRISM-B captures the observer's effective dimensional mapping rather than testing comprehension of supplied definitions. For human respondents, the full item stems (Table 1) provide sufficient context; the dimension labels alone are used only in the AI JSON schema.

*No comparative framing.* Unlike the paired-comparison prompts used in the R15 empirical study (Zharnikov 2026v), the PRISM-B specification measures a single brand at a time. Paired comparisons are a research design choice layered on top of the instrument, not part of the instrument itself. Researchers using PRISM-B for brand-pair studies administer the instrument to each brand separately and compute derived measures (differences, ratios, cosine distances) from the resulting profiles.

### *Administration Protocol*

**For AI observers:**

1. Select models and configure L1 (endpoints, parameters, temperature = .7).
2. For each model-brand combination, administer the prompt template three times (three repetitions provide within-observer variance estimates; more repetitions are permitted for increased precision).
3. Parse each response as JSON. Responses that fail JSON parsing are flagged as invalid and re-prompted once. If the re-prompt also fails, the response is recorded as missing.
4. Validate that all eight values are integers in the range [1, 5]. Responses with out-of-range values are flagged and excluded from scoring.
5. Record each valid response as an L3 session record.

**For human respondents:**

1. Configure the survey platform with the eight items (Table 1) and the 1--5 response scale.
2. Randomize item order within each respondent to control order effects.
3. Administer for a focal brand. If measuring multiple brands, randomize brand order across respondents.
4. Collect demographic metadata (age, gender, cultural background, brand familiarity) as covariates.
5. Record all responses as L3 session records.

**Temperature setting.** For AI observers, temperature is set to .7 (the default creative-task setting for most providers). This reflects realistic conditions: temperature .7 balances response diversity with coherence and matches the conversational setting in which consumers interact with LLMs. Deterministic settings (temperature 0) suppress the within-model variance that is itself a measurement target.

---

## Scoring Algorithm

### *Profile Construction*

For a given observer *m* evaluating brand *b*, each repetition *c* produces a raw response vector:

$$\mathbf{r}_{mbc} = [r_{mbc,1}, \ldots, r_{mbc,8}]$$

where each $r_{mbc,i} \in \{1, 2, 3, 4, 5\}$. The observer-brand profile is the mean across repetitions:

$$\hat{\mathbf{r}}_{mb} = \frac{1}{C} \sum_{c=1}^{C} \mathbf{r}_{mbc}$$

where *C* is the number of valid repetitions. This mean vector preserves the 1--5 scale for interpretability.

### *Normalized Weight Vector*

For analyses requiring simplex-normalized profiles (e.g., cosine similarity, DCI computation), the profile is converted to a weight vector:

$$w_{mb,i} = \frac{\hat{r}_{mb,i}}{\sum_{j=1}^{8} \hat{r}_{mb,j}}$$

The normalized weight vector $\mathbf{w}_{mb}$ lies on the probability simplex $\sum_i w_{mb,i} = 1$ and represents the proportional allocation of perceived brand signal intensity across dimensions.

### *Dimensional Collapse Index*

The DCI measures the degree to which an observer's brand perception concentrates on the two dimensions most tied to verifiable, quantifiable brand attributes -- Economic and Semiotic:

$$DCI_{mb} = w_{mb,\text{Economic}} + w_{mb,\text{Semiotic}}$$

Under uniform perception (equal weight on all eight dimensions), the baseline DCI is $2/8 = .250$. Values above .250 indicate concentration toward verifiable dimensions; values below indicate preservation of perception-dependent dimensions.

The standard error of DCI is estimated from the repetition-level variance:

$$SE(DCI_{mb}) = \sqrt{\frac{s^2_{mb,\text{Econ}} + s^2_{mb,\text{Sem}} + 2 \cdot \text{cov}(r_{mb,\text{Econ}}, r_{mb,\text{Sem}})}{C \cdot (\sum_j \hat{r}_{mb,j})^2}}$$

where $s^2_{mb,i}$ is the sample variance of dimension *i*'s rating across repetitions. This permits confidence intervals on all reported DCI values and formal comparison across observer groups.

DCI admits an information-theoretic interpretation. Treating the eight-dimensional perception as a source variable and the observer's response as a lossy encoding, the concentration of weight on Economic and Semiotic dimensions represents a minimum-distortion encoding given the observer's effective channel capacity (Shannon 1959; Cover and Thomas 2006). The cross-model convergence (cosine .977 across 24 architectures; Zharnikov 2026v) demonstrates that independent encoders converge on the same rate-distortion-optimal codebook -- a result consistent with established vector quantization theory (Gersho and Gray 1991).

### *Cross-Observer Convergence*

The mean pairwise cosine similarity across *M* observers measures structural convergence in dimensional weighting:

$$\bar{\rho} = \frac{2}{M(M-1)} \sum_{m < m'} \frac{\hat{\mathbf{w}}_m \cdot \hat{\mathbf{w}}_{m'}}{\|\hat{\mathbf{w}}_m\| \|\hat{\mathbf{w}}_{m'}\|}$$

Values approaching 1.0 indicate that observers, despite different architectures or backgrounds, weight dimensions in structurally similar proportions. In the R15 empirical study, $\bar{\rho} = .977$ across 24 LLM architectures from seven training traditions (Zharnikov 2026v).

### *Per-Dimension Analysis*

For each dimension *i*, the observer-level deviation from the uniform baseline is:

$$\Delta_i = w_{mb,i} - .125$$

Positive deviations indicate dimensional inflation (the observer over-weights this dimension relative to uniform); negative deviations indicate dimensional suppression. Reporting per-dimension deviations alongside aggregate metrics (DCI, cosine) prevents the aggregate from masking meaningful dimensional heterogeneity -- a reporting requirement established in the paper quality standards (Section A.9 of the reporting guidelines).

---

## Multi-Observer Estimation and Perception DOP

### *From Individual Profiles to Triangulated Positioning*

A single PRISM-B administration produces one observer's perception of one brand -- a projection of the brand's emission profile through the observer's spectral weights. Multiple administrations across observers with diverse spectral profiles enable triangulation: recovering the brand's emission profile from the pattern of observer-dependent projections.

The observation model (Zharnikov 2026y) treats each observer cohort *k* as providing:

$$y_k = \mathbf{w}_k^T \mathbf{x} + b_k + \varepsilon_k$$

where $\mathbf{x} \in \mathbb{R}^8$ is the brand's emission profile (the target), $\mathbf{w}_k$ is the observer's spectral weight profile (measurable via PRISM-B), $b_k$ is the observer's systematic bias, and $\varepsilon_k$ is observation noise. With *N* observers providing eight-dimensional PRISM-B scores rather than a scalar aggregate, the system expands to 8*N* equations with $8 + 8N$ unknowns, identifiable for $N \geq 2$ under mild conditions on the weight profile matrix.

### *Perception DOP as Study Design Metric*

The precision of the triangulated brand profile depends on the geometric diversity of the observer configuration. The Perception DOP scalar quantifies this:

$$\text{PDOP} = \sqrt{\text{trace}((\mathbf{W}^T \mathbf{W})^{-1})}$$

where $\mathbf{W} \in \mathbb{R}^{N \times 8}$ is the matrix of observer spectral weight profiles. Low PDOP indicates broad coverage of perceptual space; high PDOP indicates that observers share similar spectral profiles and that some dimensions will be poorly resolved.

PDOP is computable before data collection. Given a proposed set of observer cohorts with PRISM-B-measured spectral profiles, a researcher evaluates the geometric quality of the configuration through matrix inversion. Monte Carlo validation demonstrates that PDOP predicts estimation error with $R^2 = .926$ and Spearman $\rho = .996$ (Zharnikov 2026y).

The practical implication for PRISM-B study design is that researchers should select observer cohorts (whether AI models, human demographic groups, or mixed panels) to minimize PDOP rather than to maximize sample size within a single cohort. A study with three geometrically diverse observer cohorts can outperform a study with 1,000 respondents from a single homogeneous cohort, because the former resolves all eight dimensions while the latter resolves only the dimensions to which that cohort is sensitive.

### *Differential Calibration*

Systematic observer bias ($b_k$) is corrected through differential calibration using reference brands with known spectral profiles. The protocol (Zharnikov 2026y) administers PRISM-B to a set of calibration brands -- brands whose emission profiles are established through prior multi-observer studies -- and computes the residual between observed and expected scores. This residual estimates $b_k$ for each observer cohort, which is then subtracted from all subsequent measurements. The procedure is analogous to Differential GPS, where base stations with known positions broadcast correction signals to nearby receivers.

Five canonical SBT reference brands serve as calibration standards: Hermes [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5], IKEA [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0], Patagonia [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5], Erewhon [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5], and Tesla [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0].

---

## The PRISM Instrument Family

PRISM-B is one member of a family of instruments sharing the L0--L4 scaffold. Each variant inherits the architecture and substitutes domain-specific items at L2 and scoring algorithms at L4.

**PRISM-M (Metamerism).** Measures behavioral discrimination between brand pairs. Where PRISM-B measures the perception of a single brand, PRISM-M presents two brands and asks whether the observer can distinguish them on each dimension. The response is binary per dimension (distinguishable / not distinguishable), with the metamerism index computed as the count of dimensions on which the pair is indistinguishable. PRISM-M operationalizes the spectral metamerism concept (Zharnikov 2026e): two brands are metameric to an observer if the observer's PRISM-M profile shows indistinguishability on the dimensions that differentiate them spectrally. The construct was empirically grounded in Zharnikov (2026x), which demonstrated behavioral metamerism in AI-native brand identity evolution.

**PRISM-T (Temporal).** Measures the same brand at two or more time points to capture brand velocity -- the rate and direction of change in the spectral profile. The items are identical to PRISM-B but administered with explicit temporal anchoring: "As of [DATE], how strongly does [BRAND] communicate through..." PRISM-T scoring computes the first-order difference vector $\Delta\mathbf{r} = \mathbf{r}_{t_2} - \mathbf{r}_{t_1}$ and the spectral velocity norm $\|\Delta\mathbf{r}\|$, connecting to the dynamics framework (Zharnikov 2026z) that formalizes brand velocity and acceleration.

**PRISM-C (Choice).** Under development. Extends the measurement framework to choice prediction by pairing PRISM-B profiles with revealed preference data. The hypothesis is that the dimensional profile difference between two brands, weighted by the observer's spectral weights, predicts choice probability in a manner consistent with random utility theory. PRISM-C is not specified in this paper and is listed here to mark the planned scope of the family.

---

## Testable Propositions

The following propositions are derivable from the instrument specification and the empirical findings that motivate it. They constitute the minimum set of psychometric predictions that a human-subject validation study must address.

**Proposition 1 (Convergent Validity).** PRISM-B's Experiential dimension (P4) will exhibit moderate positive correlation ($r > .40$) with the Sensory and Affective dimensions of the Brand Experience Scale (Brakus, Schmitt, and Zarantonello 2009), because both instruments capture perception of experiential brand signals albeit at different levels of granularity.

*Falsification*: P1 is falsified if the correlation between P4 and the combined BXS Sensory-Affective factor is below .20 in a sample of $N \geq 200$ human respondents across at least five brands, indicating that PRISM-B's Experiential construct does not overlap with established experiential measures.

**Proposition 2 (Discriminant Validity).** PRISM-B's eight-dimensional profile will exhibit discriminant validity from single-construct brand attitude measures: the correlation between PRISM-B's first principal component and a standard brand attitude scale (e.g., Spears and Singh 2004) will be below .50, indicating that PRISM-B captures dimensional structure rather than a general evaluative halo.

*Falsification*: P2 is falsified if the first principal component of PRISM-B ratings accounts for more than 60% of total variance and correlates above .70 with a single-item brand attitude measure, indicating that the instrument captures evaluation rather than dimensional structure.

**Proposition 3 (Cross-Observer Measurement Invariance).** The rank ordering of PRISM-B dimensional scores for a given brand will be positively correlated between AI observer cohorts and human observer cohorts (Spearman $\rho > .50$), indicating that the dimensional structure of the instrument transfers across observer types even if absolute scores differ.

*Falsification*: P3 is falsified if the mean Spearman correlation between AI-generated and human-generated dimensional rank orderings across five or more brands falls below .30, indicating that PRISM-B measures fundamentally different constructs in AI and human observers.

**Proposition 4 (Format Optimality).** The 1--5 ordinal format will produce lower distortion from expert-consensus brand profiles than a 1--7 format or a 100-point allocation format when administered to human respondents, replicating the J-shaped rate-distortion curve demonstrated for AI observers (Zharnikov 2026aa).

*Falsification*: P4 is falsified if human respondents produce lower distortion at any format other than 1--5, indicating that the AI-demonstrated rate-distortion optimum does not transfer to human measurement.

---

## Discussion

### *Theoretical Implications*

PRISM-B provides the first standardized measurement instrument within Spectral Brand Theory's eight-dimensional framework. The instrument translates a theoretical taxonomy of brand signal categories into a measurement protocol with exact items, response format, and scoring algorithm. This transition from conceptual framework to operationalized measurement is the step that enables empirical testing: propositions about dimensional collapse, observer heterogeneity, and spectral metamerism become testable hypotheses when the constructs have a defined measurement procedure.

The rate-distortion justification for the 1--5 ordinal format represents, to the author's knowledge, the first application of Shannon's (1959) rate-distortion theory to psychometric format selection, though the demonstration is currently limited to AI observers. Sims (2016) established the theoretical framework connecting information-theoretic capacity limits to human perceptual judgment; Zharnikov (2026aa) provided the empirical demonstration for AI encoders. The principle extends beyond brand perception: bounded response formats can outperform unconstrained formats when the respondent (whether human or AI) introduces systematic biases under high degrees of freedom. This finding connects psychometric instrument design to information-theoretic channel coding, suggesting that the optimal response format for any multi-dimensional perception instrument is not the one with maximum information capacity but the one that minimizes the combined distortion from encoder bias and quantization error.

The design of PRISM-B as an *ab initio* dual-observer instrument distinguishes it from the growing literature on LLMs as survey respondents. Argyle et al. (2023) demonstrated that LLMs can simulate human survey responses ("silicon samples"); Horton (2023) showed that LLMs behave as simulated economic agents; Pellert, Lechner, Wagner, Rammstedt, and Strohmaier (2024) applied standard personality inventories to LLMs and found measurable but homogeneous profiles. These studies adapt existing human instruments for AI administration. PRISM-B inverts this: it derives dimensions from brand signal taxonomy rather than human response factors, selects the response format via cross-observer rate-distortion optimization, and scores AI and human responses identically. The distinction matters because instruments designed for human factors may not capture the dimensional structure relevant to AI observers, and instruments post-hoc adapted for AI lack format optimization evidence. As AI agents increasingly generate brand assessments that influence consumer decisions (Hermann and Puntoni 2024), comparing how AI and human observers perceive the same brand on the same instrument becomes a first-order research question. PRISM-B provides the measurement infrastructure for such comparisons without requiring separate instruments or ad hoc score normalization.

### *Practical Implications*

For brand managers, PRISM-B provides a diagnostic tool for identifying which dimensions of brand perception are visible to AI search agents and which are collapsed. Administering PRISM-B to a panel of LLMs using the specified prompt template produces a dimensional profile that reveals the brand's AI-mediated perception. Dimensions with low scores relative to the brand's intended positioning represent vulnerability zones in AI-mediated consumer search. For brand managers, PRISM-B provides a diagnostic for AI visibility: low scores on non-Economic and non-Semiotic dimensions flag vulnerability in LLM-mediated search and recommendation, because these are the dimensions that AI observers systematically collapse. A brand whose Narrative or Cultural signal is strong in human perception but invisible to LLMs faces a growing discovery gap as AI-mediated channels expand.

For advertising researchers, PRISM-B standardizes multi-dimensional brand perception measurement in a way that enables cross-study comparison. Studies that use PRISM-B with the specified items, format, and scoring algorithm produce comparable measurements regardless of the observer population, brand category, or research context. This comparability is currently absent from the field: brand perception measurements are typically study-specific, preventing meta-analysis and cumulative knowledge building.

For psychometricians, the five-layer scaffold provides a template for developing AI-compatible measurement instruments in domains beyond brand perception. Any multi-dimensional construct that can be decomposed into independent dimensional items can be measured using the PRISM architecture with domain-specific L2 substitution.

### *Convergence with Adjacent Literature*

The finding that structured, bounded response formats outperform unconstrained formats converges with several established research streams. In human survey design, Krosnick (1991) documented satisficing under cognitively demanding formats -- a mechanism that operates identically in AI encoders as training-corpus bias expression. In information retrieval, the vocabulary mismatch problem (Furnas, Landauer, Gomez, and Dumais 1987) demonstrates that unconstrained language production diverges from the target conceptual space. In psychophysics, the category scaling literature (Stevens 1957; Parducci 1965) shows that bounded scales with named anchors produce more reliable cross-observer comparisons than magnitude estimation. PRISM-B's 1--5 ordinal format is consistent with all three literatures.

The observer-agnostic design aligns with the emerging consensus that AI systems should be evaluated using the same constructs applied to human cognition where applicable (Hagendorff, Fabi, and Kosinski 2023; Hashimoto and Oshio 2025; Serapio-Garcia, Safdari, Crepy, Sun, et al. 2025). Martini (2026) demonstrated that AI can generate psychometric scales with measurable validity properties, providing a methodological parallel to the present work; Stein, Lenzner, and Wentzel (2024) developed the ATTARI-12 scale for measuring attitudes toward AI, illustrating that new psychometric instruments are needed for constructs that did not exist under the traditional paradigm. The argument is not that AI and human perception are identical but that commensurable measurement enables meaningful comparison of how they differ.

The multi-observer architecture of PRISM-B connects to the stakeholder co-creation tradition in brand theory. Hatch and Schultz (2010) argued that brand meaning is jointly constructed by multiple stakeholders whose perspectives may conflict. PRISM-B operationalizes this insight: each observer cohort's dimensional profile is a distinct perspective on the brand, and the triangulation framework (Zharnikov 2026y) recovers the brand's emission profile from the pattern of stakeholder disagreement rather than averaging it away. In this sense, PRISM-B is closer to Hatch and Schultz's relational ontology than to Keller's (1993) representative-consumer model, while providing the quantitative measurement infrastructure that the co-creation tradition has lacked.

### *Synthetic Cohort Pre-Pilot*

A synthetic cohort pre-pilot demonstrates instrument sensitivity. Ten behaviorally distinct observer vignettes — with no SBT dimension names in any prompt — produce significantly different PRISM-B spectral profiles across all 8 dimensions (F ranging from 8.14 to 52.90, all p < .001, eta-squared .091 to .394). The Green Advocate cohort weights Ideological 61% higher than other cohorts (d = 1.53). The Spreadsheet Shopper cohort weights Economic 94% higher (d = 1.37). These effect sizes exceed conventional benchmarks for instrument sensitivity and demonstrate that PRISM-B measures observer-dependent perception, not prompt vocabulary.

A 400-call Latin-square robustness check reveals a primacy effect in JSON-based elicitation (eta-squared = .217) — dimensions listed first receive higher weights. Cohort effects dominate position effects on 5 of 8 dimensions (Pearson r = .849 between balanced and canonical-order profiles). Balanced dimension ordering is recommended as standard practice for future PRISM-B administrations. This finding refines the "Administration Protocol" specification: while fixed order (P1--P8) was originally specified for AI observers to ensure replicability, the primacy effect evidence suggests that balanced or randomized ordering — already recommended for human respondents — should be extended to AI administration to reduce systematic position bias.

---

## Limitations

Three limitations bound the present specification.

First, **no human validation data exist for PRISM-B as specified here**. The 1--5 ordinal format is the empirically observed minimum-distortion operating point for AI observers (Zharnikov 2026aa), but its psychometric properties (internal consistency, test-retest reliability, convergent and discriminant validity) for human respondents are unknown. Establishing these properties requires administering PRISM-B to human samples alongside established brand perception instruments (Aaker 1997; Brakus, Schmitt, and Zarantonello 2009; Keller 1993) and demonstrating that PRISM-B captures distinct variance not reducible to brand personality or brand experience. Human validation is especially critical given evidence that consumers penalize AI-generated content for perceived inauthenticity (Feuerriegel, Hartmann, Janiesch, and Zschech 2024), raising the question of whether AI-derived instrument properties transfer to human respondents who may engage with brand stimuli differently. This is the highest-priority future study and constitutes Gap 1 in the SBT research atlas.

Second, **the items are theoretically derived, not empirically generated**. The Churchill (1979) paradigm for developing marketing constructs begins with a large item pool, administers it to a development sample, and retains items based on factor loadings, inter-item correlations, and fit indices. PRISM-B follows the alternative Rossiter (2002) C-OAR-SE procedure, which argues that for constructs with concrete, observable referents, single-item measures are not only legitimate but preferable to multi-item scales that introduce redundancy. The dimensional taxonomy (Zharnikov 2026r) provides the structure, and each dimension receives a single item. Single-item-per-dimension instruments trade internal consistency estimation for parsimony and dimensional completeness. The trade-off is justified when the dimensions are conceptually independent and empirically separable (Bergkvist and Rossiter 2007), but the assumption of independence requires empirical verification.

Third, **cross-language equivalence is assumed but not demonstrated**. The current specification is English-language. Administering PRISM-B in other languages requires translation of the item stems (Table 1) and verification that the dimensional labels carry equivalent meaning. Preliminary evidence from the R15 cross-cultural study (Zharnikov 2026v), in which native-language prompts were administered in 15 languages, suggests that the dimensional structure is linguistically robust for AI observers, but this cannot be assumed for human respondents without formal translation-back-translation protocols and measurement invariance testing.

### *Robustness and Boundary Conditions*

Three boundary conditions bear on the generalizability of PRISM-B results. First, order effects: the synthetic cohort Latin-square analysis (see "Synthetic Cohort Pre-Pilot") reveals a primacy effect in JSON-based AI elicitation (eta-squared = .217), recommending balanced dimension ordering for AI observers. For human respondents, the administration protocol specifies item randomization within each respondent (see "Administration Protocol"), which is the standard psychometric defense against primacy and recency effects. Second, language invariance: the R15 cross-cultural study (Zharnikov 2026v) tested native-language prompts in 15 languages and found a null result on home-market bias (H10: mean = +.001, *p* = .716), suggesting that the dimensional structure of PRISM-B is robust to prompt language for AI observers. Whether this invariance holds for human respondents requires formal measurement invariance testing across translated versions. Third, temporal stability: Proposition 4 of the PRISM specification addresses format optimality, and the PRISM-T variant (see "The PRISM Instrument Family") is designed explicitly for temporal tracking, providing a built-in mechanism for assessing test-retest reliability and detecting genuine brand perception change versus measurement instability.

---

## Conclusion

This paper specifies PRISM, a family of standardized instruments for multi-dimensional brand perception measurement, and provides the complete PRISM-B specification for measuring brand signal perception across Spectral Brand Theory's eight dimensions. The 1--5 ordinal response format is the empirically observed minimum-distortion operating point for AI observers, and it aligns with established psychometric practice for human respondents. The five-layer scaffold (L0--L4) ensures reproducibility and cross-study comparability. The scoring algorithm provides both aggregate (DCI, cosine convergence) and per-dimension metrics. Connection to multi-observer triangulation via Perception DOP enables PRISM-B to serve as the measurement module in brand positioning studies that combine heterogeneous observer types.

The instrument is specified. Validation -- demonstrating that PRISM-B measures what it claims to measure in human populations -- is the necessary next step. The specification must exist first so that validation studies have a fixed target to evaluate rather than a moving one.

---

## References

Aaker, David A. (1991), *Managing Brand Equity*, Free Press.

Aaker, David A. (1996), *Building Strong Brands*, Free Press.

Aaker, Jennifer L. (1997), "Dimensions of Brand Personality," *Journal of Marketing Research*, 34 (3), 347--356.

Ali, Farzan (2025), "The Impact of Generative AI on Brand Authenticity and Consumer Brand Image," *Journal of Business Research*, 189, 115128.

Argyle, Lisa P., Ethan C. Busby, Nancy Fulda, Joshua R. Gubler, Christopher Rytting, and David Wingate (2023), "Out of One, Many: Using Language Models to Simulate Human Samples," *Political Analysis*, 31 (3), 337--351.

Bergkvist, Lars and John R. Rossiter (2007), "The Predictive Validity of Multiple-Item Versus Single-Item Measures of the Same Constructs," *Journal of Marketing Research*, 44 (2), 175--184.

Brakus, J. Josko, Bernd H. Schmitt, and Lia Zarantonello (2009), "Brand Experience: What Is It? How Is It Measured? Does It Affect Loyalty?" *Journal of Marketing*, 73 (3), 52--68.

Churchill, Gilbert A., Jr. (1979), "A Paradigm for Developing Better Measures of Marketing Constructs," *Journal of Marketing Research*, 16 (1), 64--73.

Cover, Thomas M. and Joy A. Thomas (2006), *Elements of Information Theory*, 2nd ed., Wiley-Interscience.

DeVellis, Robert F. (2017), *Scale Development: Theory and Applications*, 4th ed., SAGE.

Educational Testing Service (2014), *ETS Standards for Quality and Fairness*, Educational Testing Service.

Feuerriegel, Stefan, Jochen Hartmann, Christian Janiesch, and Patrick Zschech (2024), "Generative AI," *Business & Information Systems Engineering*, 66, 111--126.

France, Stephen L. (2025), "Digital Brand Equity: Conceptualization and Measurement," *Journal of Product and Brand Management*, 34 (2), 234--251.

Furnas, George W., Thomas K. Landauer, Louis M. Gomez, and Susan T. Dumais (1987), "The Vocabulary Problem in Human-System Communication," *Communications of the ACM*, 30 (11), 964--971.

Gersho, Allen and Robert M. Gray (1991), *Vector Quantization and Signal Compression*, Kluwer Academic Publishers.

Geuens, Maggie, Bert Weijters, and Kristof De Wulf (2009), "A New Measure of Brand Personality," *International Journal of Research in Marketing*, 26 (2), 97--107.

Hagendorff, Thilo, Sarah Fabi, and Michal Kosinski (2023), "Human-Like Intuitive Behavior and Reasoning Biases Emerged in Large Language Models but Disappeared in ChatGPT," *Nature Computational Science*, 3 (10), 833--838.

Hashimoto, Yasuhiro and Atsushi Oshio (2025), "Exploring Personality Structure Through LLM Agent: A Lexical Perspective," *Psychological Test Adaptation and Development*, 6.

Hatch, Mary Jo and Majken Schultz (2010), "Toward a Theory of Brand Co-Creation with Implications for Brand Governance," *Journal of Brand Management*, 17 (8), 590--604.

Hermann, Erik and Stefano Puntoni (2024), "Artificial Intelligence and Consumer Behavior," *Annual Review of Psychology*, 75, 27--56.

Horton, John J. (2023), "Large Language Models as Simulated Economic Agents," Working Paper, NBER 31122.

Kapferer, Jean-Noel (2008), *The New Strategic Brand Management*, 4th ed., Kogan Page.

Keller, Kevin Lane (1993), "Conceptualizing, Measuring, and Managing Customer-Based Brand Equity," *Journal of Marketing*, 57 (1), 1--22.

Krosnick, Jon A. (1991), "Response Strategies for Coping with the Cognitive Demands of Attitude Measures in Surveys," *Applied Cognitive Psychology*, 5 (3), 213--236.

Martini, Marco (2026), "Can AI Generate Valid Psychometric Scales?," *Behavior Research Methods*, 58, forthcoming.

Li, Yinglong, Marco Castelo, Zsolt Katona, and Miklos Sarvary (2024), "Frontiers: Determining the Validity of Large Language Models for Automated Perceptual Analysis," *Marketing Science*, 43 (2), 254--266.

Nosek, Brian A., Charles R. Ebersole, Alexander C. DeHaven, and David T. Mellor (2018), "The Preregistration Revolution," *Proceedings of the National Academy of Sciences*, 115 (11), 2600--2606.

Parducci, Allen (1965), "Category Judgment: A Range-Frequency Model," *Psychological Review*, 72 (6), 407--418.

Pellert, Max, Clemens M. Lechner, Claudia Wagner, Beatrice Rammstedt, and Markus Strohmaier (2024), "AI Psychometrics: Assessing the Psychological Profiles of Large Language Models Through Psychometric Inventories," *Perspectives on Psychological Science*, 19 (3).

Preston, Carolyn C. and Andrew M. Colman (2000), "Optimal Number of Response Categories in Rating Scales: Reliability, Validity, Discriminating Power, and Respondent Preferences," *Acta Psychologica*, 104 (1), 1--15.

Rossiter, John R. (2002), "The C-OAR-SE Procedure for Scale Development in Marketing," *International Journal of Research in Marketing*, 19 (4), 305--335.

Sabbah, Houssam and Oguz A. Acar (2026), "Marketing to Machines: Understanding AI Agents as a New Marketing Channel," Working Paper, SSRN 6406639.

Sarstedt, Marko, James Brand, Christian M. Ringle, and Tomislav Dolz (2024), "Using Large Language Models to Generate Silicon Samples in Consumer and Marketing Research," *Psychology and Marketing*, 41 (6).

Schwarz, Norbert (1999), "Self-Reports: How the Questions Shape the Answers," *American Psychologist*, 54 (2), 93--105.

Serapio-Garcia, Greg, Mustafa Safdari, Clement Crepy, Fangqiong Sun, et al. (2025), "A Psychometric Framework for Evaluating and Shaping Personality Traits in Large Language Models," *Nature Machine Intelligence*.

Shannon, Claude E. (1959), "Coding Theorems for a Discrete Source with a Fidelity Criterion," *IRE National Convention Record*, 7 (4), 142--163.

Sims, Chris R. (2016), "Rate-Distortion Theory and Human Perception," *Cognition*, 152, 181--198.

Stein, Jan-Philipp, Timo Lenzner, and Florian Wentzel (2024), "ATTARI-12: Development and Validation of a Scale for Measuring AI Attitudes," *Computers in Human Behavior Reports*, 14, 100418.

Spears, Nancy and Surendra N. Singh (2004), "Measuring Attitude Toward the Brand and Purchase Intentions," *Journal of Current Issues and Research in Advertising*, 26 (2), 53--66.

Stevens, S. S. (1957), "On the Psychophysical Law," *Psychological Review*, 64 (3), 153--181.

Yoo, Boonghee and Naveen Donthu (2001), "Developing and Validating a Multidimensional Consumer-Based Brand Equity Scale," *Journal of Business Research*, 52 (1), 1--14.

Zharnikov, Dmitry (2026a), "Spectral Brand Theory: A Multi-Dimensional Framework for Brand Perception Analysis," Working Paper, https://doi.org/10.5281/zenodo.18945912.

Zharnikov, Dmitry (2026e), "Spectral Metamerism in Brand Perception: Projection Bounds from High-Dimensional Geometry," Working Paper, https://doi.org/10.5281/zenodo.18945352.

Zharnikov, Dmitry (2026r), "Why Eight? Completeness and Necessity of the SBT Dimensional Taxonomy," Working Paper, https://doi.org/10.5281/zenodo.19207599.

Zharnikov, Dmitry (2026v), "Spectral Metamerism in AI-Mediated Brand Perception: How Large Language Models Collapse Multi-Dimensional Brand Differentiation in Consumer Search," Working Paper, https://doi.org/10.5281/zenodo.19422427.

Zharnikov, Dmitry (2026x), "AI-Native Brand Identity: Observer-Driven Evolution and Behavioral Metamerism," Working Paper, https://doi.org/10.5281/zenodo.19391476.

Zharnikov, Dmitry (2026y), "Brand Triangulation: A Geometric Framework for Multi-Observer Brand Positioning," Working Paper, https://doi.org/10.5281/zenodo.19482547.

Zharnikov, Dmitry (2026z), "Spectral Dynamics: Velocity, Acceleration, and Phase Space in Multi-Dimensional Brand Perception," Working Paper, https://doi.org/10.5281/zenodo.19468204.

Zharnikov, Dmitry (2026aa), "Empirical Rate-Distortion Curve for AI Brand Perception Encoders," Working Paper, https://doi.org/10.5281/zenodo.19528833.

