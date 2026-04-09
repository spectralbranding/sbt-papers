# Brand Triangulation: A Geometric Framework for Multi-Observer Brand Positioning

**Dmitry Zharnikov**

*Working Paper — April 2026*

*DOI: https://doi.org/10.5281/zenodo.19482547*

---

## Abstract

Brand positioning research faces a fundamental measurement problem: every observer cohort perceives the same brand differently, yet traditional frameworks treat this variation as noise rather than signal. We propose *brand triangulation* — a geometric framework borrowing from GPS positioning theory to estimate brand spectral profiles from multiple observer cohorts while jointly solving for observer bias. We make four contributions. First, we formalize the GPS-SBT mapping, showing that observer cohorts function as positioning satellites whose geometric diversity determines measurement precision. Second, we introduce *Perception DOP* (Dilution of Precision), a computable metric quantifying how well a given set of observer cohorts resolves a brand's eight-dimensional spectral profile — before any data is collected. Third, we propose *differential brand measurement*, a calibration protocol using reference brands with known spectral profiles to correct systematic observer bias across studies. Fourth, we establish identifiability conditions: the minimum observer configurations required for unique brand positioning. The geometric formulation provides pre-study design criteria that Bayesian heterogeneity approaches lack. We demonstrate the framework computationally using dimensional weight data from six large language models drawn from the R15 dataset (Runs 1--4; 4,860 API calls across fifteen brand pairs). Perception DOP predicts estimation error (Monte Carlo: R^2 = 0.926, log-log slope = 0.995, Spearman rho = 0.996, all p < 10^{-300}), and Brand Function specification — reinterpreted as a DOP improvement — reduces dimensional collapse by 20% (DCI 0.355→0.284 for local brands). The framework reframes multi-observer disagreement from a methodological nuisance into a primary source of positioning information.

**Keywords**: brand positioning, Spectral Brand Theory, dilution of precision, observer bias, brand measurement, GPS analogy, dimensional collapse

---

## 1. Introduction

### 1.1 The Brand Positioning Measurement Problem

A GPS receiver in contact with a single satellite knows only its distance from that satellite — a sphere of possible positions in three-dimensional space. A second satellite reduces the ambiguity to a circle; a third to two points; a fourth resolves position uniquely while simultaneously solving for the receiver's clock error. The geometry of the satellite configuration determines how precisely position can be recovered. Satellites clustered in one quadrant of the sky provide poor coverage: any estimate derived from them is unreliable along the poorly-covered dimension. Satellites spread across the sky provide strong geometric diversity and precise positioning. The GPS literature captures this precisely with a single scalar, the *Dilution of Precision*, computed directly from the satellite geometry before any measurement is made (Kaplan and Hegarty, 2017).

Brand positioning faces an exactly analogous problem. Every brand measurement study fields one or several observer cohorts — groups of individuals or systems whose perceptual profiles determine which dimensions of brand signal they are sensitive to. A study that surveys only young, urban, premium-market consumers is measuring from a single quadrant of the perceptual sky. Its estimates of heritage, cultural positioning, and ideological commitment will be unreliable — not because the brand lacks these properties, but because the measurement infrastructure lacks the geometric coverage to resolve them. A second cohort composed of rural, price-sensitive, older consumers provides complementary sensitivity. Their combination, if the spectral weight profiles are sufficiently diverse, can triangulate the brand's true eight-dimensional position.

This paper proposes that the multi-observer heterogeneity that contemporary brand measurement treats as a nuisance — a source of variance to be controlled by sample homogeneity or fixed-effects adjustment — is, precisely, the signal. Observer disagreement, when decomposed into structural differences in spectral weight profiles, is the geometric raw material from which brand position can be triangulated. Suppressing that heterogeneity discards information that the framework shows to be recoverable.

### 1.2 Diagnosing the Literature Gap

The dominant frameworks for brand positioning measurement share a structural assumption that is rarely stated explicitly: the existence of a canonical observer whose perception represents "the brand's position." Keller's (1993) customer-based brand equity model locates brand equity in the knowledge structures of individual consumers and aggregates across them, but it provides no mechanism for decomposing the systematic differences between consumer cohorts from the brand-level signal. Aaker's (1996) Brand Identity System is sender-side — it specifies what a brand should stand for — but offers no protocol for recovering that identity from structurally heterogeneous observer measurements. Ries and Trout's (1981) positioning framework is explicitly singular: the goal is to own a position in "the consumer's mind," with consumer treated as a representative agent. Kapferer's (2012) Brand Identity Prism distinguishes brand identity from brand image but provides no formal mechanism for reconciling image assessments from observers with different perceptual profiles.

The problem is not that these frameworks are wrong; it is that they were developed for an era of relatively homogeneous observer infrastructure. When most brand encounters occurred through mass media reaching broadly similar audiences, the representative-consumer assumption was a reasonable approximation. That assumption has become progressively less tenable as three developments have expanded observer heterogeneity structurally rather than merely statistically. First, Spectral Brand Theory (Zharnikov, 2026a) formalizes the observation that observer cohorts differ not merely in their preferences but in the dimensional weights they assign to brand signals — their spectral profiles — and that these structural differences produce systematic rather than random variation in brand measurement. Second, empirical work on AI-mediated brand perception (Zharnikov, 2026v) demonstrates that large language models constitute a distinct observer type with characteristic spectral profiles that collapse ideological, cultural, and temporal dimensions, producing brand assessments that are structurally incommensurable with human-cohort assessments rather than merely noisier versions of them. Third, research on spectral metamerism (Zharnikov, 2026e) establishes formally that brands which are distinctly differentiated in the full eight-dimensional space can be perceptually indistinguishable to observers whose spectral profiles assign low weight to the differentiating dimensions — and that this indistinguishability is a property of the measurement infrastructure, not of the brands themselves.

Taken together, these developments suggest that what the positioning literature has treated as measurement error is, in substantial part, structural information about the geometric relationship between observer spectral profiles and brand emission profiles. The framework we propose exploits this structure.

### 1.3 GPS-SBT Concept Mapping

The formal analogy between GPS positioning and brand measurement is precise rather than metaphorical. Table 1 maps the core GPS concepts to their SBT counterparts.

**Table 1.** GPS-SBT concept mapping

| GPS Concept | SBT Concept | Mathematical Role |
|---|---|---|
| Satellite | Observer cohort | Known reference point with distinct perspective |
| Satellite position (known orbit) | Spectral weight profile (measurable) | Calibration data |
| Pseudorange (distance + clock error) | Biased perception score | Raw measurement |
| Receiver position (3D, unknown) | Brand spectral profile (8D, unknown) | Target to estimate |
| Clock error (1 scalar, unknown) | Observer baseline bias | Nuisance parameter solved jointly |
| Speed of light (constant) | Perceptual bandwidth (bounded rationality) | Physical constraint |
| DOP (Dilution of Precision) | Perception DOP (PDOP) | Measurement quality metric |
| Minimum 4 satellites (3D + clock) | Minimum 9 cohorts (8D + bias, collapsed) | Identifiability condition |
| DGPS base station correction | Differential brand measurement | Error cancellation via calibration brands |
| Multi-constellation (GPS + GLONASS + Galileo) | Multi-type observers (human + AI + behavioral) | Robustness via independent observation types |
| Almanac (satellite catalog) | Observer cohort registry | Reference data for study design |
| Ephemeris updates | Cohort weight drift (taste evolution) | Calibration maintenance over time |
| Satellite geometry (spread vs. clustered) | Observer diversity (varied vs. homogeneous) | Determines measurement precision |

The critical insight that motivates the GPS analogy is not merely the structural similarity between satellite geometry and observer diversity. It is the GPS insight about clock error. GPS receivers contain cheap, systematically inaccurate clocks. Rather than requiring accurate clocks — which would be prohibitively expensive in consumer devices — GPS jointly estimates position and clock error from the overdetermined system of satellite equations. The clock error is not noise; it is a solvable unknown. Brand measurement contains an exact analog. Every observer cohort has systematic biases — familiarity effects, anchoring to prior associations, cultural reference points that inflate or deflate particular dimensions. The standard methodological response is to try to eliminate these biases through sampling design. The GPS insight is to embrace them as known unknowns and solve for them simultaneously with the brand position.

### 1.4 Contributions

This paper makes four contributions to brand positioning methodology.

First, we formalize the GPS-SBT mapping as a precise observation model, showing that brand spectral profile estimation from multiple observer cohorts is a weighted least-squares positioning problem whose structure is exactly analogous to satellite positioning. Observer bias enters as a set of scalar unknowns that are identified alongside the brand profile rather than treated as noise.

Second, we introduce *Perception DOP* as a computable, pre-study metric that quantifies how well a proposed set of observer cohorts can resolve a brand's eight-dimensional spectral profile. Perception DOP provides a formal basis for cohort selection in brand measurement studies: it enables researchers to evaluate alternative study designs before collecting data, identifying configurations that are geometrically well-posed.

Third, we propose *differential brand measurement*, a calibration protocol using reference brands with known spectral profiles to correct systematic observer bias — the brand measurement analog of Differential GPS. The protocol separates brand position change from observer drift in longitudinal studies, addressing a critical confound in brand tracking.

Fourth, we establish identifiability conditions specifying the minimum cohort configurations required for unique brand positioning. We show that brands are spectrally metameric not because they are genuinely indistinguishable but because the measurement infrastructure lacks the geometric coverage to resolve them — and we characterize precisely what geometric coverage is required.

(Contributions 1–4 are developed in Sections 3, 4, 5, and 9.6 respectively.)

### 1.5 Roadmap

The remainder of the paper proceeds as follows. Section 2 reviews the theoretical background, covering brand positioning measurement, SBT's multi-observer framework, and the relevant GPS theory. Section 3 develops the brand triangulation observation model and formalizes Perception DOP. Section 4 introduces differential brand measurement and the calibration protocol. Section 5 establishes identifiability conditions and connects the framework to spectral metamerism. Section 6 extends the framework to multi-constellation positioning, combining human, AI, and behavioral observer types. Section 7 develops dynamic brand triangulation, extending static positioning to temporal trajectories. Section 8 integrates Medesani and Macdonald's (2026) invariant corridor framework to define admissible positioning and brand health metrics. Section 9 presents an empirical demonstration using R15 data. Section 10 discusses implications for brand measurement practice and theory. Section 11 addresses limitations. Section 12 concludes.

---

## 2. Theoretical Background

### 2.1 Brand Positioning Measurement

The formal analysis of brand positioning as a measurement problem begins with the recognition that brand equity resides in the cognitive structures of observers. Keller (1993) established the foundational framework: brand equity is driven by the differential effect of brand knowledge on consumer response to marketing, where brand knowledge is structured as a network of associations varying in strength, favorability, and uniqueness. This framework generates a specific measurement implication: to assess brand positioning, one assesses the knowledge structures of consumers. Aaker (1991) elaborated the equity components — brand awareness, perceived quality, brand associations, and brand loyalty — as the assets through which brands create value.

These frameworks share a critical structural feature: they aggregate observer assessments rather than decomposing them. The standard brand tracking methodology surveys a representative sample of consumers and reports mean scores on awareness, consideration, and association measures. The variation across individual respondents is treated as measurement noise around a true underlying brand position. This aggregation assumption is defensible when observer heterogeneity is primarily distributional — when observers differ in degree but not in kind. It becomes systematically misleading when observer heterogeneity is structural, when different cohorts are sensitive to different dimensions of brand signal.

Kapferer (2012) distinguished brand identity — the self-projection of the brand, specified by management — from brand image — the perceptual result in the minds of observers. This distinction correctly identifies the duality between specification and reception, but it does not provide a framework for recovering identity from heterogeneous image assessments. De Chernatony (1999) similarly emphasizes the identity-image gap as the central diagnostic in brand management, framing the gap as a communication failure to be closed. Hatch and Schultz (2010) advance the argument further by proposing that brand meaning is co-created by multiple stakeholders — a position that implies the multi-observer heterogeneity this paper formalizes geometrically. Their framework identifies the need for governance mechanisms that manage stakeholder-driven meaning variation, but provides no metric for quantifying how much stakeholder perspectives diverge or what measurement geometry would be required to resolve the divergence. None of these frameworks models the structural reasons why different observer cohorts perceive different images from the same brand signals.

More recently, Bayesian approaches to brand positioning have formalized observer heterogeneity using hierarchical models. Wedel and Kamakura (2000) model consumer heterogeneity via latent class methods, treating segments as distributional subpopulations whose preferences differ in degree but who share a common perceptual space. Rossi, Allenby, and McCulloch (2005) develop the full Bayesian framework for decomposing individual-level heterogeneity into structural components, and this paradigm now dominates quantitative marketing research on brand choice. The geometric framework proposed here complements rather than competes with Bayesian heterogeneity modeling. Where Bayesian methods estimate the *distribution* of preferences across a population, brand triangulation estimates the *position* of a brand in dimensional space from observer cohorts whose spectral weight profiles are treated as known reference positions. The distinction is analogous to GPS: Bayesian methods characterize the population of receivers; GPS characterizes the position of a single receiver given known satellite positions. The two approaches answer different questions and can be combined — Bayesian estimation of cohort weight profiles followed by geometric triangulation of brand position.

The geometric approach to brand positioning has antecedents in multidimensional scaling and conjoint analysis. Green and Srinivasan (1978) establish the attribute-based decomposition of consumer preferences, estimating part-worth utilities that are the direct methodological predecessor of dimensional weight profiling; Netzer et al. (2008) survey subsequent advances in preference measurement and the treatment of respondent heterogeneity. DeSarbo and Rao (1986) develop constrained unfolding for joint space estimation of consumer and brand positions, and Carroll and Chang (1970) introduce INDSCAL — individual differences scaling — which estimates per-subject dimension weights in a common perceptual space. INDSCAL's per-subject weights are the direct methodological ancestor of SBT's observer spectral profiles (Zharnikov, 2026a). The present paper inverts the DeSarbo-Rao structure: rather than estimating both observer and brand positions jointly from preference data, we treat observer spectral profiles as approximately known reference positions and estimate brand profiles as the unknown targets. This produces a positioning problem formally analogous to GPS trilateration rather than to multidimensional unfolding.

### 2.2 Multi-Observer Brand Perception in SBT

Spectral Brand Theory (Zharnikov, 2026a) provides the formal architecture required to make progress on this problem. SBT models brand perception across eight typed dimensions: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal. The ordering is structurally meaningful — dimensions are presented in this sequence throughout SBT to maintain definitional consistency. A brand's emission profile is the vector **e**(t) = [e_1(t), ..., e_8(t)], encoding the intensity of brand signals across all eight dimensions at time t.

The critical structural feature of SBT is the observer spectral profile. Each observer possesses a weight vector **w** = [w_1, ..., w_8] on the simplex Σw_i = 1, determining the relative salience of each dimension in forming brand conviction. Brand conviction — the observer's formed assessment — is a function of the interaction between the brand's emission profile and the observer's spectral weights. Observers with similar weight vectors cluster into cohorts (Zharnikov, 2026f). Cohorts that weight the Temporal and Cultural dimensions heavily will form systematically different brand convictions from cohorts that weight the Experiential and Economic dimensions heavily, even when observing identical brand signals.

Spectral metamerism — the condition where structurally different brand profiles produce identical brand convictions in a specific observer — was formalized in Zharnikov (2026e). Two brands are metameric with respect to observer cohort k if their emission profiles e_A and e_B satisfy **w**_k · **e**_A = **w**_k · **e**_B, meaning the cohort's spectral weights project both profiles to the same brand conviction value. Brands can be metameric for one cohort and clearly distinguishable for another. Metamerism is therefore always observer-relative rather than a property of brands in isolation.

Zharnikov (2026v) introduced a specific and consequential observer type: the large language model. Six LLM architectures were profiled across fifteen brand pairs using 4,860 API calls, recovering spectral weight profiles for each model by inferring which dimensions drove response differentiation. The results demonstrated that LLMs collectively assign low weight to Narrative, Ideological, Cultural, and Temporal dimensions — precisely those dimensions on which many brands build their most durable differentiation. Cross-model cosine similarity of spectral profiles was 0.975, indicating that this dimensional bias is structural to AI-mediated observation rather than specific to any single architecture. LLMs constitute, in the GPS analogy, a coherent but poorly positioned satellite cluster: they all occupy the same region of perceptual sky, providing strong coverage of Experiential and Economic dimensions but near-zero coverage of the dimensions that most distinguish premium and purpose-driven brands.

### 2.3 GPS Positioning Theory and Dilution of Precision

GPS positioning determines receiver location in three-dimensional space (plus time) from the signal travel times broadcast by multiple satellites (Kaplan and Hegarty, 2017). Each satellite measurement provides a *pseudorange* — the apparent distance from satellite to receiver — which combines the true range with the receiver's unknown clock error. With n satellite measurements and four unknowns (three spatial coordinates plus clock error), the system is overdetermined for n > 4 and yields a least-squares position estimate.

The precision of this estimate depends critically on the geometric arrangement of the satellites, a dependence captured by the *Dilution of Precision* (DOP). The DOP matrix is derived from the observation geometry matrix H, whose rows encode the unit vectors from receiver to each satellite along with a unit column for the clock-bias dimension. The position covariance matrix is C = (H^T H)^{-1}, and scalar DOP metrics are derived as traces or diagonal elements of C. The Geometric DOP (GDOP = sqrt(trace(C))) captures overall positioning quality; Position DOP (PDOP), Horizontal DOP, and Vertical DOP decompose it along specific axes. A DOP value near 1.0 indicates excellent geometry; values above 6 indicate that positions will be unreliable (Misra and Enge, 2011).

The decisive practical insight is that DOP can be computed before any measurement is made — it is a property of the satellite geometry alone. A receiver or mission planner can evaluate whether a proposed observation window will provide adequate geometric coverage without collecting any data. This pre-study computability is precisely the property that makes DOP a useful survey-design criterion when adapted to brand measurement.

*Differential GPS* (DGPS) extends the basic framework by using base stations at precisely known positions to compute real-time corrections to pseudorange measurements. A base station observes the difference between its known position and its GPS-estimated position; this difference — the systematic error in the pseudorange measurements — is broadcast to nearby receivers, who apply it to correct their own estimates. DGPS accuracy can reach centimeters compared to meters for unaided GPS, because the correlated errors across nearby receivers cancel in the differential correction. The protocol works precisely because the base station's known position provides a reference against which systematic error can be computed.

---

## 3. The Brand Triangulation Framework

### 3.1 Observation Model

Let **x** ∈ R^8 denote the brand's true spectral profile — the eight-dimensional vector of emission intensities across the Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal dimensions. This is the quantity to be estimated.

Let cohort k possess spectral weight profile **w**_k ∈ R^8, where the weights are normalised to sum to one and are measurable in principle through dimensional profiling tasks. When cohort k observes the brand and reports a single aggregate perception score, the observation model is:

y_k = **w**_k^T **x** + b_k + ε_k

where y_k is the scalar perception score reported by cohort k, b_k is cohort k's systematic bias (analogous to GPS clock error), and ε_k is zero-mean observation noise. The bias b_k captures all systematic tendencies of cohort k to score brands above or below their true projection onto the cohort's dimensional weights — cultural reference anchors, familiarity effects, response scale habits. The model assumes that w_k is stationary within a measurement epoch; if weight profiles shift during data collection (e.g., through priming from prior brands in a survey sequence), the W matrix is misspecified. Randomization of brand presentation order within cohorts mitigates this concern.

The linear observation model is a first-order approximation. Psychophysical research establishes that perception often follows nonlinear functions — logarithmic (Weber-Fechner) or power-law (Stevens, 1957) relationships between stimulus intensity and perceived magnitude. We adopt the linear model for three reasons. First, the SBT dimensions are not raw stimuli but constructed semantic coordinates; the Weber-Fechner regime applies to sensory thresholds, not to evaluative judgments on bounded scales. Second, the linear model is the standard assumption in factor-analytic brand measurement (Du and Kamakura, 2015) and in optimal experimental design (Kuhfeld, Tobias, and Garratt, 1994), enabling direct comparison with existing methods. Third, the DOP framework extends naturally to nonlinear observation models via linearization around a nominal estimate — the standard procedure in GPS navigation, where the pseudorange equation is linearized around an approximate position (Kaplan and Hegarty, 2017). The linear case establishes the framework; nonlinear extensions follow the same architecture with local approximation. We note that bounded scales may introduce ceiling and floor effects, and that anchoring or order effects within a survey may induce nonlinearities beyond those captured by the bias term b_k. The sensitivity of PDOP predictions to such departures from linearity is an empirical question addressed partially by the Monte Carlo analysis (Section 9.6) and more fully by future human-cohort studies.

With N cohorts providing collapsed (scalar) observations, the system is:

**y** = W**x** + **b** + **ε**

where **y** ∈ R^N is the vector of cohort scores, W ∈ R^(N × 8) is the matrix of cohort spectral weight profiles stacked as rows, and **b** ∈ R^N is the vector of cohort biases. This system has 8 + N unknowns (**x** and **b**) and N equations. Identification requires constraints on **b** — conventionally, a mean-zero constraint Σb_k = 0, reducing the free parameters to 8 + (N − 1). The system is therefore identifiable when N ≥ 9 and the rows of W span R^8, a condition formalized in Proposition 3 below.

When each cohort provides full eight-dimensional dimensional scores rather than a single aggregate, the observation model expands. Cohort k's observation is:

**y**_k = W_k **x** + **b**_k + **ε**_k

where **y**_k ∈ R^8 is the dimensional score vector from cohort k, W_k ∈ R^(8 × 8) is cohort k's dimensional response matrix (encoding how its dimensional weights transform the brand's emission profile into reported dimensional scores), and **b**_k ∈ R^8 is a dimensional bias vector. With N cohorts providing eight-dimensional observations, the system has 8N equations and 8 + 8N unknowns — identifiable for N ≥ 2 under mild conditions on W_k, as Proposition 3 establishes.

The weighted least-squares estimator for **x** (treating **b** as a set of jointly estimated nuisance parameters) is:

(x̂, b̂) = argmin Σ_k (1/σ_k^2) ||y_k − **w**_k^T **x** − b_k||^2

subject to Σ_k b_k = 0, where σ_k^2 is the noise variance for cohort k.

### 3.2 Perception DOP

The geometry of the observer cohort configuration determines the precision of the brand position estimate, exactly as satellite geometry determines GPS positioning precision. The relevant matrix is the *observation geometry matrix* for brand positioning:

**W** = [**w**_1 | **w**_2 | ... | **w**_N]^T ∈ R^(N × 8)

The brand position covariance matrix (in the limit of equal-variance cohorts and after bias estimation) is:

**C** = (**W**^T **W**)^{−1}

The *Perception DOP* scalar is:

PDOP = sqrt(trace(**C**))

A low PDOP indicates that the observer cohort configuration covers perceptual space broadly, providing precise estimation across all eight dimensions. A high PDOP indicates that the cohorts are clustered in a region of perceptual space — that they share similar spectral weight profiles — and that estimates along the poorly-covered dimensions will be imprecise.

Per-dimension DOP values sqrt(C_ii) decompose the overall imprecision across individual dimensions. A configuration with low PDOP for Experiential and Economic dimensions but high PDOP for Cultural and Temporal dimensions characteristically results from a cohort set that aggregates observers with similar sensitivity to functional and economic brand signals but little variation in temporal or cultural sensitivity.

PDOP is computable before any brand measurement is made. Given a proposed set of cohorts with measurable spectral weight profiles W_1, ..., W_N, a researcher can evaluate the geometric quality of that configuration through matrix inversion. This computability transforms cohort selection from a practical convenience into a formal optimisation problem: among all feasible cohort configurations, choose those that minimize PDOP — or, per-dimension, choose configurations that allocate measurement precision to the dimensions most relevant to the research question.

The connection to the experimental design literature is immediate. Kuhfeld, Tobias, and Garratt (1994) develop efficient experimental designs for marketing research applications using D-optimal and A-optimal criteria — geometric criteria that are formally related to DOP minimization. D-optimal designs minimize the determinant of (W^T W)^{-1}, equivalent to maximizing the geometric mean of the eigenvalues of W^T W. A-optimal designs minimize trace(W^T W)^{-1}, which is precisely PDOP^2. The connection establishes that PDOP minimization in cohort selection is a special case of A-optimal experimental design applied to the brand positioning estimation problem, grounding it in a mature methodological literature.

**Proposition 1**: For a set of N observer cohorts with spectral weight profiles **w**_1, ..., **w**_N, the precision of brand position estimation is inversely proportional to Perception DOP. Cohort configurations that minimize PDOP — those with maximally diverse spectral weight profiles — yield the most precise brand positioning.

*Falsification*: P1 is falsified if empirical brand position estimates show no relationship between PDOP and estimation variance across different cohort configurations — that is, if randomly selected cohorts perform as well as DOP-optimized cohorts across repeated simulation or empirical studies. Concretely: if a study samples fifteen random cohort configurations, computes their PDOP values, and finds that PDOP does not predict estimation variance relative to a known ground-truth brand profile, P1 fails. The falsification requires that this null relationship hold across multiple brands and multiple estimation conditions, ruling out the possibility that a single well-designed study masks the relationship.

### 3.3 Sensitivity Plateau

A practical concern in applying Perception DOP to study design is the precision required in calibrating cohort spectral weight profiles. If the precision of DOP as a design criterion degrades rapidly as weight profile estimates become imprecise, the framework becomes infeasible in practice, since cohort weight profiles are themselves estimated with uncertainty.

Medesani and Macdonald (2026) establish a *sensitivity plateau* result in the context of invariant corridor governance: system behavior is robust to parameter choice within a broad stable region, and this plateau exists for structural reasons — it follows from the separation of time scales in the system rather than from any specific parameter configuration. Crucially, the plateau is dimension-independent: it holds regardless of the system's state-space dimensionality because the structural argument concerns the relationship between time scales, not dimensions.

This result applies directly to PDOP computation. The PDOP function of cohort weight profiles is not arbitrarily sensitive near optimal configurations — it has a plateau structure in which configurations near the optimum perform similarly well. Brand managers designing measurement studies do not require millimeter-precision calibration of cohort spectral weights; they require only that the proposed cohort configuration be within the plateau region. The existence of the plateau is structural rather than parameter-dependent (Medesani and Macdonald, 2026, Section 3), analogous to the sloppiness phenomenon that Transtrum et al. (2015) identify in model parameter spaces — the characteristic property that some combinations of parameters are tightly constrained while others are sloppy (poorly determined) but that sloppy directions do not degrade predictive performance.

The practical implication is that Perception DOP is a usable pre-study design criterion despite the estimation uncertainty in cohort weight profiles. Brand researchers need to ensure their cohort configuration is in the right regime of geometric diversity — not precisely on the minimum-PDOP configuration — and the plateau provides substantial latitude to achieve this.

### 3.4 What Brand Triangulation Measures: Emission, Not Conviction

A clarification of the target variable **x** is necessary before proceeding. R^8 appears twice in SBT: as the space of brand *emission* profiles (what the brand sends into the world) and as the space of brand *conviction* profiles (what observers construct in their minds). These are distinct objects. The emission profile is a property of the brand — its advertising, pricing, silence, heritage, distribution decisions. The conviction profile is a property of the observer-brand pair — a constructed assessment that depends on the observer's spectral weights, biases, and cognitive context. Different observers construct different convictions from identical emissions.

Brand Triangulation targets the *emission* profile. The observation model y_k = **w**_k^T **x** + b_k treats **x** as a single, observer-independent vector — the brand's signal — and the observations y_k as observer-dependent projections of that signal. The weight profiles **w**_k determine which dimensions of the emission each observer attends to; the bias terms b_k capture the systematic distortion that the conviction-construction process introduces. The estimation procedure inverts the projections to recover **x**, the shared source.

This is why the GPS analogy is mathematically precise rather than merely metaphorical. GPS recovers a single receiver position from multiple satellite observations, each of which measures a different projection (pseudorange) of that position. Brand Triangulation recovers a single emission profile from multiple observer observations, each of which measures a different projection (spectrally weighted perception) of that profile. In both cases, the target is objective and single-valued; the observations are apparatus-dependent and multiple-valued.

The distinction has a direct implication for the framework's domain of applicability. When observer diversity is low — when all cohorts share similar weight profiles — the projections are nearly collinear, and the emission profile is indistinguishable from any single cohort's conviction profile. Classical brand measurement frameworks that assume a representative consumer (Keller, 1993; Ries and Trout, 1981) are adequate in this regime. They are the Newtonian limit: the weak-field approximation in which curvature can be neglected and measurement is straightforward. When observer diversity is high — structurally different weight profiles across human cohorts, AI observers, and behavioral proxies — the projections diverge, classical methods confound emission with conviction, and triangulation becomes necessary. The framework proposed here is designed for this high-diversity regime, which the developments catalogued in Section 1.2 have made the empirically relevant one.

This hierarchical relationship — a simpler model as the limiting case of a richer one — has established precedents across measurement science. Holland and Hoskens (2003) show that Classical Test Theory is a first-order approximation to Item Response Theory: CTT's constant reliability is the population-average limit of IRT's ability-dependent information function, valid when items are approximately exchangeable. McFadden and Train (2000) demonstrate that the homogeneous multinomial logit model is the limiting case of the mixed logit when the variance of random coefficients approaches zero — the exact analog of Brand Triangulation reducing to single-observer measurement when spectral weight profiles converge. In each case, the "simple" framework holds in a low-diversity regime and breaks down as heterogeneity becomes structural rather than distributional. The perception space formalism has antecedents in psychophysics: Koenderink and van Doorn (2012) model pictorial space as a fiber bundle — a shared visual field (base space) with observer-dependent depth representations (fibers) — using gauge theory to characterize how visual measurements transform under changes of viewing condition. The mathematical architecture — a shared objective space with observer-dependent projections unified by a geometric structure — is the same architecture that Brand Triangulation applies to brand perception.

---

## 4. Differential Brand Measurement

### 4.1 The DGPS Analogy

Differential GPS achieves centimeter-level positioning accuracy by cancelling the correlated errors that are the dominant limitation of unaided GPS. A base station at a precisely known position continuously estimates the difference between its GPS-derived position and its true position. This difference — the systematic error in the pseudorange measurements reaching that base station — is broadcast to nearby receivers. Because receivers near the base station observe the same satellites through the same atmospheric layers, their systematic errors are highly correlated with those of the base station. Applying the base station's error estimate to the receiver's pseudoranges cancels the shared systematic component, leaving only the uncorrelated noise.

Brand measurement has an exact analog. A study researcher who knows the true spectral profile of certain calibration brands can compute the systematic error in any given cohort's brand assessments by comparing observed calibration scores to known calibration profiles. That error estimate, applied to the same cohort's assessments of target brands, cancels the systematic component of cohort bias — provided the bias is correlated across brands, which the model assumes. The method is *differential brand measurement*.

The canonical spectral profiles defined in Spectral Brand Theory serve precisely the role of DGPS base stations. The profiles:

- Hermes: [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5] (Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal)
- IKEA: [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]
- Patagonia: [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]

are established through cross-cohort analysis within the SBT framework and represent the closest available analog to a precisely known position. A circularity concern arises: these profiles are defined within SBT rather than validated against an external standard. The concern is mitigated by the differential correction structure itself — the protocol requires only that calibration profiles be *stable* across measurement epochs, not that they be *correct* in an absolute sense. Systematic errors in calibration profiles propagate as a constant offset across all corrected target estimates, preserving the relative positioning that is the primary quantity of interest. Independent validation of calibration profiles against consumer survey data remains a priority (Section 11). These three brands exhibit characteristically different profiles — Hermes concentrating in Semiotic, Temporal, and Experiential dimensions; IKEA in Semiotic and Economic; Patagonia in Ideological and Narrative — providing coverage of distinct regions of the eight-dimensional emission space. This diversity is the DGPS analog of base station placement: base stations are positioned to cover different geographic regions, and calibration brands are selected to cover different regions of perception space.

### 4.2 Calibration Protocol

The differential brand measurement protocol proceeds in four stages, designed to be embedded within any brand tracking study at modest additional cost.

Stage 1: Calibration brand selection. Choose three to five calibration brands whose spectral profiles are well-established and span diverse regions of the eight-dimensional space. The Hermes, IKEA, and Patagonia profiles above provide a minimum viable calibration set. Additional calibration brands should be selected to cover regions of emission space that the minimum set leaves geometrically thin — for example, a brand with strong Narrative and Cultural concentration, or one with distinctive Temporal-low and Economic-high concentration.

Stage 2: Study inclusion. Every measurement study — tracking wave, cohort profiling study, or experimental protocol — includes the calibration brands alongside the target brands being measured. Cohort respondents rate all brands, calibration and target, on the same dimensional scales.

Stage 3: Bias estimation. For each observer cohort k, compute the systematic error as the difference between observed calibration scores and known calibration profiles:

**δ**_k = **y**_k^(cal) − **x**^(cal)

where **y**_k^(cal) is cohort k's observed dimensional scores for the calibration brands and **x**^(cal) is the known calibration profile matrix. This yields a dimensional bias vector for cohort k that captures its systematic tendency to inflate or deflate specific dimensions relative to the ground truth.

Stage 4: Target correction. Apply the estimated bias to cohort k's assessments of all target brands:

**x**̂_k^(corrected) = **y**_k^(target) − **δ**_k

The corrected estimate removes the systematic component of cohort bias, leaving residuals that reflect genuine dimensional variation in the target brand's position across cohorts. Cross-cohort comparison of corrected estimates provides a more reliable picture of genuine brand positioning heterogeneity.

**Proposition 2**: Differential brand measurement using calibration brands with known spectral profiles reduces systematic cross-cohort variance. The correction is exact for linear bias and first-order effective for nonlinear bias, analogous to DGPS correction bounded by baseline distance.

*Falsification*: P2 is falsified if calibration correction fails to reduce cross-cohort variance for target brands — that is, if the bias affecting calibration brands is uncorrelated with the bias affecting target brands within the same cohort. Concretely: if a study applies the calibration correction to a set of cohorts measuring both calibration and target brands, and finds that the cross-cohort variance of corrected target estimates is statistically indistinguishable from uncorrected variance, P2 fails. The falsification should be assessed across multiple target brands and multiple cohort configurations to rule out brand-specific idiosyncrasy.

### 4.3 Separating Brand Drift from Observer Drift

A fundamental methodological challenge in longitudinal brand tracking is the confound between brand change and observer change. Between two measurement waves, a brand's spectral profile may shift — for example, due to a campaign emphasizing ideological repositioning — but the observer cohort's spectral weight profile may also shift, due to generational taste change, macroeconomic conditions, or competitive context shifts. Standard tracking methodologies report the change in mean dimensional scores without decomposing these sources.

Differential brand measurement provides a clean separation. Calibration brands, by construction, are brands whose spectral profiles are stable over the measurement interval — they are selected precisely because their positioning is well-established and unlikely to change substantially. If calibration brand scores change between measurement waves T1 and T2 for a given cohort, that change reflects observer drift rather than brand change. If target brand scores change while calibration scores remain stable, the change reflects genuine brand movement.

Du and Kamakura (2015) develop a primary dynamic factor analysis framework for longitudinal tracking studies that addresses a related confound: the need to separate structural changes in latent factors from changes in factor loadings. Their framework is formally compatible with the calibration approach proposed here; the calibration correction provides a pre-processing step that removes cohort-level systematic bias before the dynamic factor model is applied.

The separation matters practically for brand management decisions. A brand manager observing a decline in Ideological dimension scores between T1 and T2 needs to know whether the decline reflects brand-side changes (the brand's signals are weaker) or observer-side changes (observer cohorts have elevated their Ideological standards, making the brand appear weaker by comparison). The calibration protocol provides a principled answer rather than requiring managerial inference.

---

## 5. Identifiability and Metamerism

### 5.1 Minimum Observer Configurations

The identifiability question for brand triangulation is formally analogous to the GPS question: what is the minimum number of satellites required for unique position determination? In GPS, four satellites are required for three-dimensional position plus clock bias — one measurement per unknown. Brand triangulation has more unknowns.

For the collapsed (scalar) observation case — where each cohort provides a single aggregate perception score — the observation model has 8 + N unknowns (the eight-dimensional brand profile plus one bias per cohort, minus one for the normalization constraint). Unique identification requires that the system of N equations in 8 + (N − 1) unknowns be non-degenerate, which requires N ≥ 9 and the N cohort weight vectors **w**_1, ..., **w**_N to span R^8. The spanning condition is the brand-triangulation analog of the GPS condition that satellites span the full geometric sky: a set of cohorts that all share similar spectral weight profiles fails to span R^8 and cannot uniquely identify the brand profile, regardless of how many cohorts are included.

For the full eight-dimensional observation case — where each cohort provides separate scores on all eight dimensions — the system has 8N equations and 8 + 8N unknowns (brand profile plus dimensional bias vector per cohort). With the constraint that bias vectors sum to zero across cohorts, identification requires N ≥ 2 and the weight matrices W_k to be linearly independent. The eight-dimensional observation case is structurally more efficient, requiring far fewer cohorts because each cohort contributes eight constraints rather than one.

The identifiability threshold for the collapsed case — N ≥ 9 — has an immediate practical implication. The overwhelming majority of brand tracking studies employ one to three demographic cohorts. These studies operate well below the identifiability threshold and cannot, in principle, uniquely recover an eight-dimensional brand position, regardless of sample size within cohorts. Increasing N from 200 to 2,000 respondents within a single cohort does not reduce this fundamental under-determination; it only reduces the noise within a single biased observation.

The connection to admissible decision theory is instructive. Wald (1947) establishes conditions for the completeness of classes of decision functions — the conditions under which the set of decisions under consideration is rich enough that no relevant alternative exists outside the class. Applied here, the identifiability conditions characterize the class of observation configurations that are complete in the sense that they do not exclude any dimension of brand position information. An observation configuration below the threshold is inadmissible in Wald's sense: there always exists an augmented configuration that dominates it by recovering dimensions that the under-determined configuration cannot access.

**Proposition 3**: A brand's eight-dimensional spectral profile is uniquely identifiable from N observer cohorts if and only if: (a) for collapsed observations, N ≥ 9 and the cohort weight vectors span R^8; (b) for full eight-dimensional observations, N ≥ 2 and the weight matrices are linearly independent.

*Falsification*: P3 is falsified if unique brand profiles can be recovered from fewer cohorts than specified — for instance, if structural constraints on the brand profile space reduce the effective degrees of freedom below eight, so that fewer independent cohort observations suffice for identification. Concretely, if empirical work establishes that brand spectral profiles are characteristically constrained to a lower-dimensional manifold — for example, a four-dimensional subspace of the eight-dimensional emission space — the identifiability threshold would be correspondingly lower. P3 is a claim about the generically eight-dimensional character of brand perception, and it is falsified by evidence of systematic dimensional redundancy.

### 5.2 Metamerism as Geometric Underdetermination

The connection between identifiability failure and spectral metamerism is immediate. When the observer configuration falls below the identifiability threshold — fewer than nine cohorts for collapsed observations, or fewer than two with full-dimensional observations — the system of equations is underdetermined. Multiple brand profiles **x** produce identical cohort observations **y** = W**x** + **b**. The brands are spectrally metameric with respect to this observation infrastructure.

This formulation clarifies a conceptual point that the prior metamerism literature has not fully distinguished. Zharnikov (2026e) formalizes metamerism as a property of the observer-brand pair: brands A and B are metameric with respect to observer k if **w**_k · (**e**_A − **e**_B) = 0. This single-observer condition is a specific instance of the broader structural situation established here: metamerism arises whenever the observation infrastructure — the set of observers and their spectral weight profiles — cannot distinguish the brands. Single-observer metamerism is the extreme case where the observation infrastructure consists of a single cohort. Multi-observer metamerism, where two brands are indistinguishable to a set of N observers, requires that (**e**_A − **e**_B) lie in the null space of W — that the brands differ only along dimensions to which every observer in the set assigns zero weight.

This reframing of metamerism as geometric underdetermination has several implications. First, it identifies metamerism as a property of the measurement infrastructure rather than primarily a property of the brands. Brands are not intrinsically metameric; they are metameric relative to specific observer configurations. Adding a cohort with non-zero weight on the differentiating dimensions resolves the metamerism. Second, it connects to the conditional metamerism finding of Zharnikov (2026v): brands that are metameric under information-poor observation conditions (LLMs without Brand Function data) become distinguishable under information-rich conditions (LLMs with structured behavioral specifications). The conditioning event — information provision — changes the effective spectral weights of the observer, shifting the observer's position in perceptual space and potentially resolving the metamerism.

Molenaar (1985) develops a dynamic factor model for the analysis of multivariate time series that is formally relevant here. His model treats latent factors as evolving over time and the observed scores as linear functions of those latent factors. The brand profile **x** in the brand triangulation model corresponds to the latent factor vector in Molenaar's framework, and the cohort weight profiles W_k correspond to the factor loading matrices. Molenaar's identification conditions — his requirements on the number and structure of observed variables per latent factor — provide a complementary set of theoretical tools for analyzing when brand positions are identifiable in longitudinal settings.

The practical consequence of the identifiability analysis is a reframing of what standard brand tracking studies can reliably claim. A study with two demographic cohorts can distinguish brands along, at most, two independent dimensions. If those dimensions happen to be Experiential and Economic — the dimensions most commonly salient to demographically defined cohorts — the study characteristically fails to recover Narrative, Ideological, Cultural, and Temporal positioning. Brands that invest heavily in these dimensions appear perceptually equivalent to brands that do not. The brand managers are not deceived by market conditions; their measurement infrastructure lacks the geometric coverage to resolve the difference.

---

## 6. Multi-Constellation Positioning

GPS systems derive higher positioning accuracy and fault tolerance by fusing signals from multiple independent satellite constellations — GPS, GLONASS, Galileo, and BeiDou — each operated by different agencies, subject to different error patterns, and transmitting on different frequencies. The redundancy is not decorative: when one constellation's geometry degrades, the others compensate. Brand Triangulation benefits from the same architectural principle. A *multi-constellation positioning strategy* combines structurally distinct observer types whose systematic biases are geometrically non-collinear, ensuring that the limitations of any single constellation do not collapse the solution.

Three observer constellations are available to brand researchers, each with a distinctive measurement profile.

**Human observer cohorts** provide rich dimensional sensitivity. A human respondent who regularly purchases luxury goods attends to Semiotic and Temporal signals with precision that behavioral data cannot replicate. Human observers can be segmented into cohorts with demonstrably different *observer spectral profiles* — the 8-dimensional weight vectors that characterize how each cohort allocates perceptual attention across SBT dimensions. Premium buyers weight Semiotic high; sustainability-oriented observers weight Ideological high; price-sensitive buyers weight Economic high. This dimensional diversity is exactly what Perception DOP optimization requires (see Section 3). The limitations are familiar: data collection is slow, expensive, and structurally limited to small N. At survey scale, human cohort data rarely exceeds five or six distinct weight profiles, which may be insufficient to resolve all eight dimensions.

**AI observers (large language models)** are cheap, fast, and available at scale. Recent work establishes their viability as measurement instruments: Argyle et al. (2023) demonstrate that LLMs conditioned on demographic backstories produce algorithmically faithful response distributions ("silicon samples"); Li et al. (2024) validate LLMs for automated perceptual analysis with 75%+ agreement with human surveys on brand similarity; and Brand, Israeli, and Ngwe (2023) show that LLM-derived willingness-to-pay estimates are comparable to human conjoint studies. As Zharnikov (2026v) documents, LLMs exhibit statistically reliable dimensional weight profiles that can serve as observer positions in the triangulation geometry. The critical limitation is systematic bias: LLMs default to Economic and Semiotic signals when training data for a brand is sparse, producing a predictable Economic Default distortion. For global brands, DCI (Dimensional Collapse Index, defined as the combined weight on Economic and Semiotic dimensions) is 0.291 — near the theoretical baseline of 0.250 for a flat-weight observer. For local brands, DCI rises to 0.353, reflecting the Economic Default mechanism in operation (Zharnikov, 2026v). This bias is systematic and directional, meaning it can in principle be modeled and corrected rather than treated as noise. However, Goli and Singh (2024) document systematic divergences between LLM and human intertemporal preferences, reinforcing that observer geometry matters precisely because not all observer nodes are equivalent in spectral fidelity — the motivation for Perception DOP as a design criterion.

**Behavioral proxies** — purchase data, engagement metrics, social listening sentiment, click-through patterns — are indirect but scalable. Dew, Ansari, and Toubia (2022) demonstrate that multimodal representation learning can link visual, textual, and consumer-rating dimensions of brand perception, establishing a precedent for fusing heterogeneous observer sources into a coherent spectral position. They do not measure perception directly; they measure behavior that perception partly generates. A cohort of repeat purchasers who pay a premium contributes information about Economic and Experiential conviction without requiring a survey. The mapping from behavioral signals to dimensional weights is imprecise and requires calibration, but the scalability advantage is large. Behavioral proxies provide the high-N foundation on which human and AI observations are anchored.

### 6.1 Cross-Constellation Validity

Before combining constellations, cross-constellation consistency must be assessed. In GPS multi-constellation fusion, receiver integrity monitoring checks whether satellite signals from different constellations agree on the receiver's position; large discrepancies signal a faulty satellite or atmospheric anomaly. The brand measurement analog is direct: do human observers and AI observers agree on the brand's dimensional profile?

The theoretical basis for treating LLMs as observer nodes is grounded in the "Homo Silicus" framework (Horton, Filippas, and Manning, 2023), which treats LLMs as implicit computational models of human economic agents. Arora, Chakraborty, and Nishimura (2025) provide direct empirical support: human-LLM hybrid measurement outperforms either source alone, validating the multi-constellation approach. Cross-constellation consistency is not merely a quality check — it is itself a substantive finding. If human cohorts and LLMs assign similar dimensional weight profiles to a brand, this convergent agreement increases confidence in the triangulated position. If they disagree, the discrepancy locates the source of the disagreement in identifiable structural differences: training-data lag in the LLM, anchoring bias in the human cohort, or genuine dimensional ambiguity in the brand itself.

The R15 empirical record establishes that AI cross-model cosine similarity is 0.975 (Zharnikov, 2026v) — the six LLM constellations are internally consistent. They share a common systematic bias rather than random noise. This is the GPS analog of a correlated clock error: all receivers are wrong in the same direction because they share the same Reference Frame. The practical implication is that the AI constellation, taken alone, provides a precise but biased fix — exactly the situation that differential correction addresses (Section 4).

The high cross-model correlation raises an identification concern. The mean-zero bias constraint (Section 3) assumes that biases are sufficiently diverse to cancel in aggregate. When all AI observers share a common bias direction — the Economic Default — the common component is not identified by the mean-zero constraint alone. Differential brand measurement (Section 4) addresses this directly: the calibration correction removes the constellation-level bias estimated from calibration brands, not merely the per-observer deviation from the constellation mean. In a multi-constellation design combining human and AI observers, the correlated AI bias becomes one estimable constellation-level parameter rather than an unidentified confound.

### 6.2 The Economic Default Mechanism as Modeled Bias

Zharnikov (2026v) demonstrates that the Economic Default is a predictable, parameterizable bias: when a model lacks training data covering a brand's full dimensional range, it substitutes Economic signals (price, perceived value) for missing information. The mechanism is not random. Run 3 of the R15 experiment (Runs 1--4 subset), which probed local brands with minimal training data coverage, produced an Economic dimension weight 168% above its theoretical flat-weight baseline.

Geopolitical framing introduces a further systematic bias: the same brand evaluated in different city contexts produces significantly different dimensional weight profiles (mean absolute DCI delta = 0.040, p < 0.0001; Zharnikov, 2026v, H12), demonstrating that the bias vector b_j in the observation model (Equation 2) is not only architecture-dependent but context-dependent.

This predictability is the DOP framework's key opportunity. In GPS differential correction, the base station's systematic clock error is estimated from its known position and subtracted from rover measurements. The same logic applies here: using calibration brands whose dimensional profiles are known (Hermes, IKEA, Patagonia — see Section 4), the magnitude of the AI constellation's Economic Default can be estimated and removed from target brand measurements. The corrected measurements reflect a closer approximation of what a human constellation would observe.

**Proposition 4**: *Multi-constellation brand positioning — combining human observer cohorts, AI observers, and behavioral proxies — is expected to yield lower Perception DOP than any single constellation alone, provided the constellations exhibit structurally different spectral weight profiles. The theoretical basis is the geometric non-collinearity of AI and human weight profiles, as indicated by the Economic Default mechanism in AI observers* (Zharnikov, 2026v). *Empirical validation requires human cohort data (Section 11).*

*Falsification*: P4 is falsified if adding AI or behavioral observer data to human cohort data does not reduce PDOP — that is, if the additional constellations' weight profiles are collinear with human weight profiles and provide no new geometric information.

The condition for collinearity — and thus for failure of P4 — is clear: if AI weight profiles systematically reproduce human weight profiles (same dimensional emphases, same relative ordering), then the AI constellation is geometrically redundant. The available evidence runs in the opposite direction: the AI Economic Default produces dimensional over-weighting that most human cohorts do not share, suggesting structural non-collinearity.

---

## 7. Admissible Positioning

*Sections 7 and 8 extend the measurement framework to two complementary questions: where should the brand be (admissibility), and how is it moving (trajectory). These extensions are formally specified but not empirically tested in this paper; they are included to demonstrate the framework's generative capacity and to define the research agenda for subsequent work.*

Brand Triangulation determines where a brand is in 8-dimensional perception space. This section addresses a logically prior question: where should the brand be? Not every achievable position is a desirable one. A brand can achieve a stable, coherent, high-conviction position in a perception region that its specification explicitly prohibits. Measuring the position precisely does not diagnose this failure; it merely locates it. Diagnosing the failure requires a reference: the admissible region defined by the Brand Function.

The distinction between coherence and admissibility parallels a well-established conceptual split across multiple domains. In statistical decision theory, Wald (1947) distinguishes admissible decision functions — those not uniformly dominated by any alternative — from merely consistent ones. In quality management, Kane (1986) distinguishes process capability (the process is consistent and controlled) from process conformance (the process outputs are within specification). A process can be highly capable, producing outputs with low variance, while simultaneously producing outputs outside specification — perfectly coherent, perfectly inadmissible.

Simons (1994) formalizes the governance analog: boundary systems constrain strategic behavior not by specifying what to do, but by specifying what is prohibited. An organization operating within its boundary system is admissible; an organization that is internally consistent but has drifted outside its boundary system is inadmissible regardless of its coherence. Simon (1951) identifies the employment relationship itself as a form of bounded admissibility: an employee accepts authority within a specified zone of indifference, and actions within that zone are admissible whether or not they are optimal.

Brand admissibility extends this logic to the perceptual domain.

### 7.1 Invariant Corridors as Brand Perception Boundaries

The Brand Function (Zharnikov, 2026x) specifies a brand's intended position in 8-dimensional perception space: the dimensional weights that the brand aims to activate, the relative emphasis across Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal dimensions, and the boundaries of acceptable variation. This specification defines not a point but a region — an *admissible corridor* in 8D perception space.

Medesani & Macdonald (2026) formalize this structure in the context of microgrid frequency stability. They define an invariant corridor C(t) = [L(t), U(t)] as a bounded admissible region in state space that contracts under stress and recovers with hysteresis when stress subsides. The corridor is not a fixed box; it is a dynamically governed boundary whose width reflects operational freedom. The foundational mathematical treatment is Aubin (1991), whose viability theory establishes which initial states allow a dynamical system to remain within a constraint set under differential inclusion dynamics. Blanchini (1999) surveys the set invariance literature that provides the control-theoretic grounding for such corridors.

The brand measurement analog is direct. The Brand Function defines a corridor C ⊂ R^8 — the set of spectral profiles the brand owner specifies as acceptable. Brand Triangulation measures where the brand's current perception cloud is located. The *corridor distance* is the Euclidean distance from the measured position to the nearest boundary of C:

d_corridor = ||x_measured - proj_C(x_measured)||

where proj_C(x) denotes the nearest point in C to x. When d_corridor = 0, the brand is at the corridor boundary (a warning state). When the measured position is interior to C (d_corridor < 0 by convention), the brand is admissible. When d_corridor > 0, the brand has exited the corridor and is inadmissible.

Three properties of this formalization distinguish it from the coherence framework. First, admissibility is per-cohort: different observer cohorts may locate the brand at different positions, some of which may be inside C while others are outside. A brand may be admissible to its intended cohort and inadmissible to an unintended one. Second, admissibility is specification-relative: the corridor boundary is derived from the Brand Function, not from the distribution of observer scores. Third, admissibility is binary at the boundary and continuous in the interior: the corridor distance provides a gradient health metric for brands well inside C, but the legal/governance conclusion — admissible or inadmissible — is categorical.

The sensitivity plateau result from Medesani & Macdonald (2026) has direct practical value here. Establishing C precisely in 8 dimensions is demanding; brand managers may resist a framework that requires exact boundary specification. The plateau result establishes that governance properties are structurally robust to parameter choice within a broad stable region: the precise location of the corridor boundary does not need to be specified with engineering precision for the admissibility framework to function. This reduces the practical barrier to implementation.

### 7.2 Tri-Binding Admissibility

A brand's position may satisfy the geometric corridor condition while still being inadmissible in a governance sense. Medesani & Macdonald (2026), Section 8.5, establish that framework guarantees require three independent binding conditions to hold simultaneously — a *tri-binding admissibility* requirement. Partial satisfaction of the conditions provides no guarantees; each binding is individually necessary and all three are jointly sufficient.

The brand measurement mapping of the three bindings is as follows.

*Geometric binding* requires that the measured spectral profile lies within the Brand Function's admissible corridor in 8-dimensional perception space. This is the dimensional condition: the brand's position vector x_measured ∈ C. For Brand Triangulation, this is the quantity directly produced by the measurement framework — the triangulated position relative to the corridor. Geometric binding failure means the brand is coherently positioned in the wrong region.

*Governance binding* requires that a valid Brand Function specification exists and that an enforcement mechanism operates to constrain brand behavior toward the specified region. Governance binding addresses the upstream condition: there must be a specification for the corridor to exist, and there must be organizational authority capable of acting on corridor violations. A brand with a perfectly measured position but no Brand Function has no corridor — geometric binding is undefined, and governance binding trivially fails. The relevance of Simon's (1951) bounded admissibility is clear here: governance binding is the organizational equivalent of the authority relationship. Zharnikov (2026a) and Zharnikov (2026x) establish the Brand Function as the specification layer; Zharnikov (2026i) establishes the organizational layer through which enforcement operates.

*Temporal binding* requires that the measured perception trajectory is coherent with the brand's historical path. A brand that satisfies geometric and governance binding at the current measurement epoch but whose trajectory shows sustained drift toward the corridor boundary is not fully admissible: the temporal record reveals a governance failure in progress even if the current position is technically within C. Temporal binding connects to the Kalman filter framework developed in Section 8 and to the non-ergodic trajectory analysis of Zharnikov (2026o).

**Proposition 5**: *A brand position is* admissible *if and only if three conditions hold simultaneously: (a) the measured spectral profile lies within the Brand Function's admissible corridor in 8-dimensional perception space (geometric binding); (b) a valid Brand Function specification exists and an enforcement mechanism operates (governance binding); and (c) the measured trajectory is temporally coherent with the brand's historical perception path (temporal binding). Failure of any single binding dissolves all admissibility guarantees.*

*Falsification*: P5 is falsified if brands satisfying only one or two of the three binding conditions demonstrate equivalent long-term brand health outcomes to fully admissible brands — that is, if partial binding is sufficient for governance.

The industrial adhesive case illustrates the failure pattern with precision (Zharnikov, 2026a, Section 5.4). A commercial adhesive brand designed its Brand Function for the contractor corridor: high Economic (cost-effectiveness), high Experiential (bond strength, ease of use), moderate Semiotic (professional packaging), low Social (no lifestyle component). Over time, an unintended observer cohort emerged: substance abusers for whom the product "works" for inhalation. Within this cohort, the brand achieves perfect signal coherence — every touchpoint reinforces the same perception, brand conviction is high, the perception cloud is stable. By every coherence metric in the pre-v2.3 SBT framework, this brand scores as healthy.

Per-cohort admissibility analysis changes the verdict entirely. For the intended contractor cohort, the measured position is inside C. For the substance-abuse cohort, the measured position is far outside C: the Semiotic and Social dimensions are dominated by underground culture signals the Brand Function never emitted. Geometric binding fails for this cohort. Governance binding fails because no mechanism prevented the brand from being perceived and used differently. Temporal binding partially fails because the divergence has been accumulating for years without detection. All three bindings must hold simultaneously; none do for the unintended cohort.

The generalization identifies a structural pattern across brand governance failures:

**Table 2.** Brand governance failures: admissibility analysis across three brand types

| Brand | Intended corridor | Unintended cohort | Admissibility status |
|---|---|---|---|
| Industrial adhesive | Contractors | Substance abusers | Inadmissible: all three bindings fail |
| Luxury handbag | Heritage collectors | Conspicuous consumption | Partially inadmissible: geometric binding fails for conspicuous cohort |
| Tech platform | Developers | Misinformation spreaders | Inadmissible: governance binding fails |

In each case, aggregate coherence scores would have obscured the governance failure. Brand Triangulation's per-cohort measurement makes the inadmissibility visible.

### 7.3 Contraction/Recovery Asymmetry

A further contribution of Medesani & Macdonald (2026), Section 8.5, is the formalization of asymmetry in corridor dynamics. The contraction gain k_c (the rate at which the admissible corridor narrows under strain) exceeds the recovery gain k_r (the rate at which it expands during quiescence): k_c > k_r. This asymmetry is not a calibration artifact but a structural property of the governance system: the system is designed to respond rapidly to threats and recover conservatively.

For brand dynamics, this formalization provides the mathematical structure for an empirical observation documented across the SBT research program. Zharnikov (2026s) establishes that coherence-resilient brands survive crises better than coherence-fragile ones — an asymmetric D/A (Dilution/Amplification) ratio describes how quickly brand signals dissipate versus accumulate. The Medesani formalization treats this asymmetry as a geometric property of the corridor dynamics rather than merely an empirical regularity.

The brand management implications follow directly. Crisis trajectory corresponds to a corridor contraction velocity spike: the admissible region narrows rapidly as strain accumulates across multiple observer cohorts simultaneously. Recovery timeline estimation is possible from the k_r parameter: given the current corridor width and the recovery gain, the time to return to pre-crisis width is estimable. Esterhuizen, Levine & Streif (2021) demonstrate the parallel in epidemic management, where admissible invariant sets provide both a governance criterion and a recovery timeline framework — the structural analogy to brand crisis and recovery is direct.

Process invariance is the deeper implication. Medesani & Macdonald (2026), Section 9, state: "The true invariant is the corridor contraction operator itself." For brand governance, this reframes the notion of brand consistency. The invariant is not the brand's current position but the governing process by which the brand adapts under stress. A brand that maintains its contraction/recovery dynamics — its response process — preserves its admissibility guarantees even through significant positional change. A brand that abandons its governing process — *re-collapsing* without a valid Brand Function to anchor the new position — forfeits admissibility even if it lands in a geometrically acceptable region.

---

## 8. From Position to Trajectory

Sections 3–7 treat brand positioning as a static estimation problem: at a given measurement epoch, what is the brand's position in 8-dimensional perception space? This is the GPS analogy for a receiver at rest. Real brands are not at rest. They evolve through 8-dimensional perception space as marketing actions are taken, crises occur, consumer tastes shift, and cultural context changes. *Dynamic Brand Triangulation* extends the framework from position estimation to trajectory tracking.

### 8.1 Three Temporal Concepts

Brand Triangulation involves three distinct temporal concepts that GPS navigation separates carefully, and which must similarly be distinguished in brand measurement.

**Table 3.** Three temporal concepts in brand triangulation and their GPS equivalents

| Temporal Concept | GPS Equivalent | SBT Equivalent |
|---|---|---|
| Measurement timestamp | GPS epoch | When the survey or probe was conducted |
| Positional coordinate | Altitude (one of three spatial coordinates) | Temporal dimension — the 8th SBT coordinate: heritage, history, longevity |
| Object trajectory | Receiver motion over time | Brand perception dynamics — how the 8D profile changes across measurement epochs |

The third row is where dynamic tracking adds value. Most longitudinal brand trackers record time-series of scalar brand scores. Dynamic Brand Triangulation records time-series of 8-dimensional positions — vectors, not scalars — enabling trajectory analysis that scalar tracking cannot provide.

Temporal biases add a fourth temporal element. In GPS, clock error is a systematic temporal bias in the receiver that must be solved jointly with position. Brand measurement has analogous temporal biases: recency bias inflates the salience of recent brand experiences in human observer cohorts; training-data lag causes LLM observers to reflect the brand's reputation at the training cutoff rather than at the measurement epoch (the "hardcodedness" documented in Zharnikov, 2026v); nostalgia/anchoring causes human observers to hold prior perceptions even after the brand has changed. These biases are solvable, not merely noisy — the same joint estimation logic that GPS applies to clock error applies here.

### 8.2 Perception Velocity and Acceleration

Comparing brand positions at measurement epochs T1 and T2 yields a *perception velocity* vector in 8-dimensional perception space:

v = (x_{T2} − x_{T1}) / (T2 − T1)

where x is the 8-dimensional spectral profile and T is calendar time. The velocity vector carries three distinct signals. Its direction identifies which dimensions are changing — a velocity vector pointing in the Ideological dimension signals a values repositioning; a vector pointing in the Economic dimension may signal a pricing crisis. Its magnitude indicates the speed of change — crisis events produce sudden velocity spikes; organic evolution produces slow drift. Its second derivative d²x/dt² — acceleration — distinguishes a trajectory that is stabilizing (decelerating velocity) from one that is intensifying (accelerating velocity), which is the early warning signal of an accelerating crisis.

Calibration brands serve as temporal anchors for separating brand drift from observer drift. If Hermes, IKEA, and Patagonia — whose spectral profiles are well-established — show stable positions across measurement epochs while a target brand's measured position shifts, the shift is attributable to brand change. If calibration brand positions shift, the observers themselves changed — through taste evolution, generational cohort replacement, or LLM retraining — and the target brand measurements must be corrected accordingly. This is the GPS analog of distinguishing receiver motion from satellite orbit drift.

### 8.3 Perception Kalman Filter

Periodic brand measurements are noisy. Survey data suffer from response error, sample variation, and context effects. LLM probes vary with prompt phrasing. Behavioral proxies are confounded with non-brand factors. Combining these noisy estimates into a smoothed trajectory estimate requires a filtering framework.

The Kalman filter (Kalman, 1960) provides the optimal linear state estimator for systems that evolve according to known dynamics and are observed with Gaussian noise. The DOP-Kalman combination has been demonstrated outside navigation: Guo et al. (2022) show that DOP values can be adaptively fed into the Kalman covariance matrix to weight unreliable observer geometry in UWB indoor positioning. Its application is well established in marketing: Naik, Mantrala & Sawyer (1998) use a Kalman filter to track advertising quality as a latent state that evolves dynamically and is observed through sales response. Du & Kamakura (2015) develop primary dynamic factor analysis for brand tracking studies, directly addressing the separation of true latent change from measurement noise in panel data. Oud et al. (1990) establish the formal connection between Kalman filtering and longitudinal factor score estimation.

The *Perception Kalman filter* adapts this framework to 8-dimensional spectral tracking. The state vector is (x, v) where x ∈ R^8 is the brand's current spectral profile and v ∈ R^8 is its perception velocity. The prediction step uses the velocity estimate to project the brand's next position: x_{t+1|t} = x_t + v_t · Δt. The update step corrects the prediction with new observations from any constellation of human cohorts, AI observers, or behavioral proxies, weighted by each constellation's reliability (inverse observation variance). The Kalman gain allocates trust between prediction and observation as a function of their relative uncertainties.

**Proposition 6**: *Brand perception trajectories are estimable via a Perception Kalman filter that jointly tracks the 8-dimensional spectral profile and its first derivative (perception velocity). The filter's prediction error provides a real-time anomaly detector: deviations exceeding a threshold — calibrated via the sensitivity plateau established in Medesani & Macdonald (2026) — signal either genuine brand events or observer infrastructure changes, distinguishable by calibration brand stability.*

*Falsification*: P6 is falsified if the Kalman filter's prediction errors show no correlation with actual brand events (product launches, crises, repositioning campaigns) — that is, if the filter cannot distinguish signal from noise in longitudinal brand tracking data.

The anomaly detector built into P6 has a structural advantage over threshold-based detection: the sensitivity plateau (Medesani & Macdonald, 2026) ensures that calibration of the detection threshold is robust to parameter choice. The threshold need only be placed within the stable plateau region for the detection properties to hold, which reduces the calibration burden substantially.

Dynamic admissibility monitoring integrates the trajectory framework with the corridor analysis of Section 7. The predicted trajectory x_{t+h} for horizon h can be compared to the corridor C: if the predicted position exits C before the horizon, the system issues a governance warning. Recovery after a corridor exit can be modeled using the contraction/recovery asymmetry parameters (k_c, k_r) from Medesani & Macdonald (2026), producing a data-driven recovery timeline.

---

## 9. Empirical Demonstration

The theoretical framework of Sections 2–8 generates five testable implications. This section demonstrates each using Runs 1--4 of the R15 dataset (Zharnikov, 2026v), which provide the AI observer constellation — six LLMs scoring 15 brands across eight SBT dimensions in a structured weight elicitation protocol (the PRISM-B instrument). The complete R15 study (7 runs, 24 models, 15,435+ calls) substantially extends this constellation; the present section uses the Runs 1--4 subset. This constitutes an Option A empirical demonstration: a proof of concept using the AI constellation alone, with the human constellation noted as a necessary extension (Section 11).

### 9.1 Data and Method

The R15 dataset (Runs 1--4 subset) comprises 4,860 API calls across four experimental runs, using six LLMs as observer cohorts: Claude Sonnet 4.6, GPT-4o, Gemini 2.5 Flash, DeepSeek V3, Qwen3 30B, and Gemma 4 27B. Each model was asked to allocate 100 points across the eight SBT dimensions (Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal) for 15 brand pairs (10 global brands, 5 local brands). Run 4 introduced Brand Function specifications for local brands, providing a test of specification effects on the triangulation geometry. The structured elicitation protocol ensures that each model's responses are directly comparable across brands and across models.

Each model's aggregate weight profile constitutes one row of the observation weight matrix W. With six models, W is a 6 × 8 matrix.

### 9.2 DOP Computation

Table 4 reports the aggregate dimensional weight profile across all six models and all 15 brands.

**Table 4.** Aggregate dimensional weight profiles across six LLM observer cohorts (R15 Runs 1--4 data, N = 4,860 calls)

| Dimension | Mean weight | Ratio to flat-weight baseline (12.5) |
|---|---|---|
| Experiential | 18.8 | 150% |
| Semiotic | 14.8 | 118% |
| Economic | 14.3 | 114% |
| Narrative | 10.5 | 84% |
| Ideological | 8.2 | 66% |
| Temporal | 8.1 | 65% |
| Social | 7.8 | 62% |
| Cultural | 7.3 | 58% |

The weight matrix W is dominated by Experiential, Semiotic, and Economic dimensions. The covariance matrix C = (W^T W)^{-1} reveals the consequence: Cultural and Temporal dimensions have the highest per-dimension DOP values — these are the least geometrically resolved dimensions in the AI observer constellation. Any triangulated brand position is reliable along the Experiential-Semiotic-Economic axis and unreliable along the Cultural-Temporal axis.

This DOP pattern replicates a finding from navigation: when all satellites are clustered in one region of the sky, vertical (altitude) estimation degrades while horizontal estimation remains accurate. Here, all six AI observers are "clustered" in the Experiential-Economic sky — they collectively over-attend to those dimensions, leaving Cultural and Temporal geometrically underdetermined.

Comparing PDOP across observer subsets confirms the expected pattern: using all six models produces lower PDOP than using any five, which produces lower PDOP than any four. The marginal DOP reduction from adding each observer is largest when the new observer introduces a weight profile that is structurally non-collinear with existing observers. Models with lower Economic Default (Claude Sonnet 4.6, GPT-4o) add more DOP-reducing geometric diversity than models with higher Economic Default.

The complete R15 dataset confirms this cross-architecture convergence at scale: cosine similarity of 0.977 across 24 model architectures from seven training traditions (Zharnikov, 2026v, H2 supported).

### 9.3 Differential Correction Demonstration

Hermes, IKEA, and Patagonia serve as calibration brands. Their canonical spectral profiles are established in the SBT framework (Zharnikov, 2026a): Hermes = [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]; IKEA = [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]; Patagonia = [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5].

For each calibration brand b, the systematic error for model k is:

e_k = y_{k,b} − x_b

where y_{k,b} is the model's reported profile and x_b is the canonical profile. Averaging across the three calibration brands yields a per-model systematic error vector e_k ∈ R^8.

Applying the correction to target brand measurements — subtracting the estimated systematic error from each model's raw scores before triangulation — reduces cross-model variance in the triangulated position. The variance reduction is largest for the Economic dimension (where the Economic Default is most active) and smallest for the Experiential dimension (where all models converge). This pattern is consistent with the prediction that differential correction eliminates directional systematic bias while preserving genuine signal.

The practical implication echoes Kuhfeld, Tobias & Garratt (1994) on efficient experimental design: the calibration protocol should be embedded in the measurement instrument itself, not treated as a post-hoc correction. Canonical calibration brands should be included in every brand survey alongside target brands.

### 9.4 Conditional Metamerism as Underdetermination

The R15 finding that local brands have higher DCI than global brands — 0.353 versus 0.291, t(13) = 6.483, p < 0.0001, Cohen's d = 0.878 (Zharnikov, 2026v) — is reinterpreted within the triangulation framework as a DOP effect.

Local brands have less representation in LLM training data. The AI observer constellation therefore has less geometric information about local brands' dimensional positions, producing a higher-DOP fix. The Economic Default mechanism is the AI observer's response to this underdetermination: when the dimensional position cannot be resolved from training data, the observer collapses to Economic and Semiotic signals. This is the brand measurement analog of a GPS receiver that, unable to lock four satellites, defaults to a two-dimensional fix using the two strongest signals — a technically valid but geometrically impoverished positioning.

Run 4 of the R15 experiment introduces Brand Function specifications for local brands, providing explicit dimensional information that the models would otherwise infer from training data. DCI for local brands drops from 0.355 to 0.284 — a 20% reduction in dimensional collapse (Zharnikov, 2026v). In the triangulation framework, this is equivalent to providing ephemeris data for a satellite with a degraded broadcast signal: the specification corrects the observer's positional estimate, reducing the effective DOP. Zharnikov (2026x) frames this as the Brand Function's role in agentic commerce; the triangulation framework provides the geometric mechanism.

The conditional metamerism connection is direct (Zharnikov, 2026e). Local brands that appear indistinguishable under AI observation — metameric in the AI constellation — may be geometrically distinguishable once Brand Function specifications provide the missing dimensional information. Metamerism is an observer infrastructure problem, not a brand property. Brand Triangulation gives this claim geometric content.

### 9.5 Limitations of the Option A Demonstration

The R15 AI-only constellation demonstration establishes the geometric framework and provides initial support for the DOP, differential correction, and conditional metamerism predictions. Several limitations must be noted.

The human observer constellation is absent. Human cohorts are the primary measurement target for brand research; AI observers are a supplementary constellation. The multi-constellation DOP reduction claimed in P4 cannot be fully tested without human cohort data that has demonstrably different weight profiles from the AI constellation. Option B — a survey study with five or more demographically distinct human cohorts scoring the same 15 brands — remains the necessary empirical extension.

The present data constitute a single measurement epoch. Proposition 6 (Perception Kalman filter) and the trajectory framework of Section 8 require longitudinal data — at minimum two epochs with the same observer constellation scoring the same brands. Run 1 through Run 4 of R15 vary experimental conditions, not time; they do not constitute a temporal panel.

Six AI observer models may be below the identifiability threshold for collapsed (1D aggregate) observations. The Section 5 theorem requires N ≥ 9 collapsed-observation cohorts to achieve full 8-dimensional identifiability. The R15 constellation has 8D observations per model, which reduces the requirement to N ≥ 2 — the six-model constellation is formally sufficient. However, the DOP analysis shows that with six models clustered in the Experiential-Economic region of weight space, the Cultural and Temporal dimensions remain poorly resolved. Identifiability is necessary but not sufficient for precision.

Brand stimuli are categorical pairs (global vs. local) rather than a cross-category sample. DOP computation and calibration correction should be validated across product categories with different natural dimensional profiles before generalizing. More broadly, all calibration and target brands are B2C consumer brands. B2B brands, service brands, place brands, and personal brands may have fundamentally different dimensional profiles and observer structures; the framework's generalizability beyond B2C is an open question.

### 9.6 Monte Carlo Validation of PDOP Predictive Validity

To provide a formal statistical test for the claim that Perception DOP predicts measurement quality, we conducted a Monte Carlo simulation with 2,000 independent trials. Each trial generates a random ground-truth brand position in R^8, a random observer weight matrix W with N in {9, 10, 12, 15, 20} cohorts and varying geometric diversity (clustered, random, or near-optimal), and 20 replicated noisy observations y_k = w_k^T x + epsilon_k with sigma = 0.5. The brand position is estimated via OLS, and mean squared error (MSE) is computed against the known ground truth.

The theoretical prediction from the GPS-SBT analogy is that MSE = sigma^2 * PDOP^2. The simulation confirms this relationship:

**Table 5.** Monte Carlo validation of PDOP predictive validity (2,000 trials, 20 replications each)

| Test | Statistic | Value | Expected |
|---|---|---|---|
| MSE ~ sigma^2 * PDOP^2 | Slope | 0.968 [0.945, 0.991] | 1.000 |
| MSE ~ sigma^2 * PDOP^2 | R^2 | 0.926 | 1.000 |
| MSE ~ sigma^2 * PDOP^2 | p-value | < 10^{-300} | -- |
| log(RMSE) ~ log(PDOP) | Slope | 0.995 [0.981, 1.009] | 1.000 |
| log(RMSE) ~ log(PDOP) | R^2 | 0.994 | 1.000 |
| Spearman rank | rho | 0.996 | 1.000 |

*Note.* 95% confidence intervals (shown in brackets) computed via bootstrap (1,000 resamples). Full results in R17_pdop_simulation_results.json.

The log-log regression slope of 0.995 (expected 1.0) confirms the power-law relationship: RMSE scales linearly with PDOP, as GPS theory predicts. The slight departure from unity in the MSE regression slope (0.968) reflects the finite number of replications per trial.

Per-dimension validation confirms that the relationship holds across all eight SBT dimensions: Spearman correlations between per-dimension DOP^2 and per-dimension MSE range from 0.978 to 0.990 (all p < 10^{-300}). Dimensions with higher DOP — those less geometrically resolved by the observer configuration — produce proportionally larger estimation errors.

**Table 6.** RMSE by PDOP quartile (binned analysis)

| Quartile | PDOP range | Mean RMSE | Std RMSE | n |
|---|---|---|---|---|
| Q1 (best geometry) | 0.00 -- 0.84 | 0.192 | 0.075 | 500 |
| Q2 | 0.84 -- 2.04 | 0.702 | 0.179 | 499 |
| Q3 | 2.04 -- 4.71 | 1.644 | 0.428 | 500 |
| Q4 (worst geometry) | 4.71 -- 39.71 | 4.579 | 2.684 | 500 |

The 24-fold difference in RMSE between Q1 and Q4 configurations demonstrates that observer geometry dominates measurement precision — the same measurement noise sigma yields dramatically different estimation quality depending on the PDOP of the observer constellation.

**PDOP bounds for the N=9 minimum case.** The theoretical lower bound on PDOP for N observers in D=8 dimensions is 1/sqrt(N). For N=9, this yields PDOP >= 0.333. Numerical optimization (Nelder-Mead, 100 restarts) achieves PDOP = 0.388, with condition number 1.92 — confirming that near-optimal configurations exist close to the theoretical floor. The empirical distribution of PDOP under random weight assignment has median 3.67 and mean 5.07, indicating that typical configurations are far from optimal and that deliberate DOP-aware cohort selection offers substantial precision gains.

**Sensitivity plateau.** Perturbing the optimal weight matrix by Gaussian noise with standard deviation epsilon confirms the plateau structure: PDOP degrades by less than 10% for perturbations up to epsilon = 0.2 (relative to the D-scaled weight values). At epsilon = 0.3, degradation reaches 16%. This confirms the Medesani and Macdonald (2026) plateau prediction: researchers need approximate, not exact, weight profile calibration to achieve near-optimal measurement geometry.

The simulation code, raw results, and JSON output are archived at github.com/spectralbranding/sbt-papers/r17-brand-triangulation/ (R17_pdop_simulation.py, R17_pdop_simulation_results.json).

---

**Data and Code Availability.** Monte Carlo simulation code (R17_pdop_simulation.py) and results (R17_pdop_simulation_results.json) are available at github.com/spectralbranding/sbt-papers/r17-brand-triangulation/. The R15 empirical dataset used for validation is archived at doi.org/10.5281/zenodo.19422427.

---

## 10. Implications for Brand Research Methodology

The Brand Triangulation framework generates theoretical and practical implications for brand measurement that differ substantially from current standard approaches.

### 10.1 Theoretical Implications

The GPS-SBT mapping situates brand positioning within a class of geometric estimation problems for which principled solutions already exist. The connection to INDSCAL (Carroll & Chang, 1970) is foundational: INDSCAL's per-subject dimension weights are the direct methodological ancestor of SBT's observer spectral profiles, but INDSCAL treats observer positions as unknowns to be estimated jointly with brand positions. Brand Triangulation inverts this structure — treating observer weight profiles as approximately known reference positions and brand profiles as the unknown targets — producing a positioning problem analogous to GPS trilateration rather than multidimensional unfolding. This inversion is possible precisely because the observer profiling step (PRISM-B instrument; Zharnikov, 2026v) provides pre-measurement weight calibration.

The connection to Bayesian heterogeneity modeling (Wedel & Kamakura, 2000) is complementary rather than competitive. Bayesian methods characterize the *distribution* of spectral weights across a population; Brand Triangulation uses that distribution to estimate the *position* of a brand in dimensional space. The two approaches answer different questions and can be combined: Bayesian estimation of cohort weight profiles feeds the W matrix, which then drives PDOP computation and triangulated estimation. The geometric framework adds pre-study design criteria — PDOP — that the Bayesian approach does not provide.

### 10.2 Practical Implications

### 10.2.1 Pre-Study DOP Optimization

Current practice selects survey cohorts on demographic or category-usage grounds — age, gender, income, purchase frequency — without reference to measurement geometry. Brand Triangulation replaces this with a formal design criterion: select cohorts whose spectral weight profiles maximize geometric diversity, minimizing PDOP before data collection begins.

In practice, this requires pre-study elicitation of approximate weight profiles from pilot cohort members. The cost is modest; the benefit is large: the DOP computation tells the researcher which dimensional estimates will be reliable given the proposed cohort configuration, and which cohorts to add to resolve remaining deficits. Optimal design theory (Kuhfeld, Tobias & Garratt, 1994) provides the statistical framework for extending this criterion to choice experiment designs, connecting Brand Triangulation to a mature methodological literature.

### 10.2.2 Cross-Study Comparability Through Differential Correction

A persistent problem in brand tracking research is that estimates from different studies, different agencies, and different methodologies cannot be directly compared. Brand A scored 7.2 on Semiotic in Study 1 and 6.8 in Study 2: is this brand change or observer drift? Current practice cannot answer this question.

Differential correction solves it structurally. If both studies include the same calibration brands — Hermes, IKEA, Patagonia, measured by the same observer cohorts — the systematic difference between studies can be estimated and removed. What remains is the brand change signal. This enables genuine meta-analysis of brand tracking studies: aggregating results across research agencies, time periods, and methodological generations in a way that is currently impossible (Grimm et al., 2013; Molenaar, 1985).

### 10.2.3 Continuous Brand Monitoring via Kalman Filter

Current brand tracking is periodic and expensive: annual or semi-annual surveys with large samples, producing a time series of scalar scores that cannot distinguish brand change from measurement drift. The Perception Kalman filter enables a different operational model: a continuous stream of lightweight, high-frequency observations (AI probes, behavioral proxies, social listening sentiment) integrated with periodic high-quality human cohort surveys. The filter allocates trust between observation types as a function of their reliability, producing a smooth, continuously updated trajectory estimate.

The anomaly detection property of the filter (Proposition 6) converts this into a real-time governance tool: when prediction error exceeds the sensitivity plateau threshold, the system flags an event for investigation. Crisis detection, which currently relies on reputational monitoring systems that measure outcomes rather than dimensions, becomes a dimensional early-warning system — identifying which of the eight SBT dimensions is driving the anomaly before it becomes visible in sales or share data.

### 10.2.4 Brand Function as Ephemeris Data for AI Commerce

Zharnikov (2026x) establishes that AI purchasing agents — operating in agentic commerce environments — make brand decisions using dimensional weight profiles derived from training data. These profiles suffer from the Economic Default for brands with sparse training coverage. The Brand Function provides a structured specification that agents can read directly, bypassing the training-data inference step.

In the triangulation framework, this is the ephemeris data analogy: when a GPS satellite's broadcast signal is weak or absent, a receiver can use stored ephemeris data to maintain positioning. When an AI agent lacks training data about a brand's dimensional profile, a publicly available Brand Function specification provides the equivalent: a direct channel from the brand owner's specification to the agent's positioning algorithm. The DOP improvement from Run 4 in the R15 data (DCI 0.355→0.284) quantifies the effect: providing specification data improves the AI observer's geometric resolution by an amount equivalent to adding a new satellite with a well-characterized orbit.

### 10.3 Convergence with Other Evidence

The R15 empirical study (Zharnikov, 2026v) provides direct evidence for the dimensional collapse patterns this paper's DOP framework is designed to diagnose. Local brands exhibit higher Dimensional Collapse Index (DCI = 0.353) than global brands (DCI = 0.291), and this elevation is predicted by the triangulation framework as a DOP effect: lower training-data coverage reduces the AI observer constellation's geometric resolution, driving the Economic Default. The cross-model cosine similarity of 0.976 across 24 AI model architectures confirms that observer convergence is structural — precisely the condition where triangulation geometry becomes most informative, because all observers occupy the same region of perceptual sky and geometric diversity must be supplied by non-AI constellations. The Brand Function specification intervention in Run 4 (DCI 0.355→0.284, a 20% reduction) provides a direct empirical demonstration of the DOP improvement mechanism: structured dimensional information functions as ephemeris data, correcting the observer's positional estimate and improving geometric resolution.

### 10.4 Future Research

The most pressing empirical extension is an Option B study incorporating human observer cohorts with verified non-collinear weight profiles. Such a study would directly test Proposition 4 (multi-constellation DOP reduction) by comparing PDOP and estimation precision in AI-only versus mixed human-AI constellations. A concrete design would administer the PRISM-B 100-point weight allocation task to five demographically stratified cohorts — varying by age, cultural background, income, and brand involvement — alongside the AI constellation, using the same 15 brands and three calibration brands as R15.

Beyond the immediate human cohort extension, three research directions follow from the framework. First, implementing DOP-aware cohort selection in a live brand tracking study — selecting human cohort composition using pre-study PDOP computation — would test whether geometric optimization produces measurable precision gains relative to demographically-selected cohorts. Second, validating the calibration brand stability assumption across cultural contexts requires cross-cultural replication of the Hermes, IKEA, and Patagonia profiles, establishing whether these brands function as reliable DGPS base stations outside Western markets. Third, extending the 8-dimensional corridor proof (Section 7) to the multi-dimensional case requires the vector-valued invariant extension identified by Medesani & Macdonald (2026) as future work — a formal open problem that limits the current framework to approximation-based corridor assessment in R^8.

---

## 11. Limitations and Future Research

The present paper establishes the geometric framework for multi-observer brand positioning and provides an Option A empirical demonstration using AI observer constellations. Several limitations delimit the current contribution and identify priorities for extension.

The human observer constellation is the most important limitation. Human cohort data with demonstrably distinct spectral weight profiles — verifiably non-collinear in 8D weight space — is required to test P4 (multi-constellation DOP reduction) and to validate the differential correction protocol against an external standard. An Option B study design would administer a structured 8-dimensional weight elicitation to demographically diverse cohorts (five or more, stratified by age, income, cultural background, and brand involvement) alongside the AI constellation, using the same calibration brands and target brands as R15.

A concrete study design for Option B would administer the same 100-point weight allocation task used in R15 to five or more demographically distinct human cohorts — stratified by age, income, cultural background, and brand involvement — scoring the same 15 brands alongside the three calibration brands. This design directly tests whether human weight profiles are non-collinear with the AI constellation's Experiential-Economic clustering, validating P4.

The 8-dimensional corridor proof requires an extension of Medesani & Macdonald (2026). The invariant corridor framework is established in one dimension; Medesani & Macdonald identify multi-dimensional vector-valued invariants as Future Work. For Brand Triangulation, the 8D corridor is a hyperrectangle or ellipsoid in R^8, the contraction operator is a matrix rather than a scalar, and the sensitivity plateau becomes a higher-dimensional surface. The structural argument for plateau existence — derived from separated time scales rather than dimensionality — is portable, but the formal proof is an open problem that the present paper defers.

Cross-cultural calibration brand selection requires empirical validation. The canonical profiles of Hermes, IKEA, and Patagonia are established within the SBT framework (Zharnikov, 2026a) but have not been tested across cultural contexts where brand meaning may vary substantially. A calibration brand that is stable in Western markets may exhibit significant drift in Asian or African markets. Cross-cultural replication of the calibration base is a prerequisite for global application of differential correction.

Behavioral proxy integration methodology requires a theory-of-translation layer: the mapping from observed behavior (purchase frequency, price premium paid, engagement rate) to dimensional weight profiles is not direct, and calibration against human and AI observer data is necessary before behavioral proxies can be incorporated into the W matrix. The sloppiness analysis of Transtrum et al. (2015) — which identifies which parameter combinations observational data can resolve — provides a natural framework for characterizing which behavioral signals carry dimensional information and which are geometrically redundant.

Temporal stability of Perception DOP is a further open question. If observer cohorts' weight profiles drift over time — as tastes evolve, generations turn over, and LLMs are retrained — the W matrix changes, and DOP values computed at study design time may not hold at measurement time. The Kalman filter framework addresses this partially by including observer drift as an estimable state, but the magnitude and timescale of AI observer drift across retraining cycles is empirically unknown.

Structural absence — what the SBT framework terms "dark signals" (Zharnikov, 2026a) — introduces a systematic blind spot in the PDOP computation. When a brand deliberately suppresses emission on a dimension (e.g., Hermes on Economic, scoring 3.0), the signal is real — it shapes perception space — but may be invisible to observers whose weight profiles assign near-zero attention to that dimension. If all observers in the constellation share this blindness, the per-dimension DOP for the suppressed dimension approaches infinity, yet the overall PDOP may not reflect this because the dimension contributes minimally to the trace of the covariance matrix. The practical consequence is that PDOP systematically underestimates positioning uncertainty for brands whose competitive differentiation operates through absence rather than emission. The per-dimension DOP decomposition (Section 3.2) partially addresses this by flagging poorly resolved dimensions, but a formal correction quantifying measurement precision specifically on low-emission dimensions is an open problem. Differential brand measurement (Section 4) provides indirect detection: because calibration brands' known profiles include dark-signal dimensions, the systematic error pattern reveals what direct observation misses — the brand measurement analog of detecting dark matter through gravitational lensing rather than direct observation.

A deeper theoretical boundary concerns the sufficiency of the spectral profile for brand identification. Recent work in differential geometry establishes that two surfaces can share the same metric and the same mean curvature yet be genuinely non-congruent — the Bonnet pair phenomenon (Bobenko, Hoffmann & Sageman-Furnas, 2025). The brand measurement analog is the possibility that two brands with identical eight-dimensional spectral profiles and identical aggregate coherence scores may nevertheless produce systematically different perceptions in observers whose non-ergodic trajectories through perception space select different experiential "embeddings" of the same metric data. The spectral profile targeted by Brand Triangulation is necessary but may not be sufficient for brand identification in regimes where historical trajectory matters — brands with complex crisis histories, heritage brands whose current profile is path-dependent, or brands that have been re-collapsed from different starting positions. Non-ergodic trajectory analysis (Zharnikov, 2026o) provides the "second fundamental form" that resolves this ambiguity. The Bonnet boundary is relevant primarily in high-curvature regimes; for brands in typical measurement contexts, the spectral profile determines perception uniquely, and the framework operates without trajectory correction.

Finally, the framework's linear observation model assumes that the emission profile **x** is a well-defined, observer-independent object. Section 3.4 establishes the conceptual basis for this assumption: **x** is the brand's emission, not any particular observer's conviction. The assumption holds when observer biases are approximately linear and stable — when the conviction-construction process introduces systematic but predictable distortions. It may degrade in regimes where conviction construction is strongly nonlinear: ideological polarization can invert the sign of a dimension (a brand signal intended as progressive is perceived as regressive by an opposed cohort), and cultural appropriation can create perception where no emission exists. These extreme cases lie outside the linear model's domain and represent the boundary where the emission-level single-manifold framework requires extension to a richer geometric structure — potentially a fiber bundle over the emission space, with observer-dependent fibers encoding the nonlinear conviction-construction process (Zharnikov, 2026d). The precedent for such structures exists in psychophysics: Resnikoff (1974) models perceived color space using differential geometry; Sarti, Citti, and Petitot (2008) model the functional architecture of primary visual cortex as a principal fiber bundle where the retinal plane serves as the base manifold and orientation-scale variables constitute the fibers; and Koenderink and van Doorn (2012) formalize pictorial space as a fiber bundle where a shared visual field serves as the base space and observer-dependent depth representations constitute the fibers — a direct structural analog to the emission/conviction distinction proposed here. Characterizing the boundary where the linear approximation fails and the full fiber structure matters — empirically, not only geometrically — is a priority for subsequent theoretical work. More broadly, the linear observation model is the tangent-space approximation of a geodesic inverse problem on the Riemannian perception manifold; the Riemannian center of mass (Karcher, 1977) provides the curved-space generalization that connects flat-space brand triangulation to the Fisher-Rao metric geometry developed in Zharnikov (2026d).

---

## 12. Conclusion

Brand positioning has long been treated as a matter of subjective perception, resistant to the standards of geometric precision applied in natural science. The GPS analogy suggests that this resistance is structural, not fundamental: positioning uncertainty is a function of the observer geometry, not an intrinsic property of the phenomenon. When the observer constellation is well-configured — diverse in spectral weight profiles, numerous enough to satisfy identifiability conditions, and corrected for systematic bias — brand positioning becomes a tractable geometric estimation problem.

The theoretical contributions of this paper are four. First, Perception DOP provides an a priori measurement quality criterion: the precision of dimensional estimation is computable before data collection, enabling principled cohort selection that replaces demographic heuristics with geometric optimization. Second, differential brand measurement enables cross-study comparability by anchoring measurements to calibration brands with known spectral profiles, separating brand change from observer drift in longitudinal data. Third, multi-constellation positioning establishes that human observer cohorts, AI observers, and behavioral proxies provide structurally non-collinear weight profiles whose combination reduces overall DOP — the AI observer's Economic Default is not merely a defect but a structured bias that differential correction can address. Fourth, the admissibility framework — integrating the tri-binding conditions of Medesani & Macdonald (2026) with Wald's (1947) admissibility criterion and the Brand Function specification layer — completes the measurement architecture: it is not sufficient to know where a brand is; governance requires knowing whether that position is admissible relative to specification.

The practical transformation implied by this framework is substantial. Brand measurement upgrades from opinion polling to geometric estimation. Multi-observer disagreement, currently treated as noise to be averaged away, becomes signal: it locates the source of dimensional underdetermination in the observer configuration rather than in the brand. Longitudinal tracking, currently limited to scalar time series, extends to 8-dimensional trajectory estimation with real-time anomaly detection. Re-collapse — what traditional brand management calls "rebranding" — can be distinguished from corridor drift: the former is a deliberate governed transition to a new Brand Function; the latter is an ungoverned exit from the current one. And admissibility monitoring converts Brand Function specifications from governance documents into operational diagnostic tools, capable of identifying per-cohort governance failures that aggregate coherence scores cannot detect.

The framework's dependence on the GPS analogy is deliberate but bounded. GPS is instructive because navigation is a solved multi-observer positioning problem with a mature literature on precision, bias correction, and dynamic tracking. The mathematical structures — DOP, differential correction, Kalman filtering, multi-constellation fusion — transfer to brand measurement because the underlying geometry is the same: unknown position, multiple biased observers, known observer characteristics, goal of minimum-variance estimation. The analogy breaks where it must break: brands are not physical objects with fixed positions but social constructs whose "position" depends on the observer configuration itself. The framework does not deny this; it provides the geometric tools for characterizing and managing it.

Brand positioning is a geometric estimation problem. The framework proposed here characterizes the conditions under which it can be solved and provides computable criteria for evaluating whether a given observer configuration is sufficient.

---

## References

Aaker, D. A. (1991). *Managing Brand Equity: Capitalizing on the Value of a Brand Name*. Free Press.

Aaker, D. A. (1996). *Building Strong Brands*. Free Press.

Argyle, L. P., Busby, E. C., Fulda, N., Gubler, J., Rytting, C., & Wingate, D. (2023). Out of one, many: Using language models to simulate human samples. *Political Analysis*, 31(3), 337–351. DOI: 10.1017/pan.2023.2

Arora, N., Chakraborty, I., & Nishimura, Y. (2025). AI-human hybrids for marketing research: Leveraging large language models (LLMs) as collaborators. *Journal of Marketing*, 89(2), 43–70. DOI: 10.1177/00222429241276529

Aubin, J.-P. (1991). *Viability Theory*. Birkhauser. DOI: 10.1007/978-0-8176-4910-4

Aubin, J.-P., Bayen, A. M., & Saint-Pierre, P. (2011). *Viability Theory: New Directions*. Springer. DOI: 10.1007/978-3-642-16684-6

Bawa, V. S. (1976). Admissible portfolios for all individuals. *Journal of Finance*, 31(4), 1169–1183.

Berger, M. P. F., King, C. Y. J., & Wong, W. K. (2000). Minimax D-optimal designs for item response theory models. *Psychometrika*, 65(3), 377–390. DOI: 10.1007/BF02296152

Bertsekas, D. P., & Rhodes, I. B. (1971). On the minimax reachability of target sets and target tubes. *Automatica*, 7(2), 233–247.

Blanchini, F. (1999). Set invariance in control — A survey. *Automatica*, 35(11), 1747–1767. DOI: 10.1016/S0005-1098(99)00113-2

Bobenko, A. I., Hoffmann, T., & Sageman-Furnas, A. O. (2025). Compact Bonnet pairs: Isometric tori with the same curvatures. *Publications Mathematiques de l'IHES*, 142, 241–293. DOI: 10.1007/s10240-025-00159-z

Brand, J., Israeli, A., & Ngwe, D. (2023). Using LLMs for market research. HBS Working Paper No. 23-062. Harvard Business School.

Carroll, J. D., and Chang, J.-J. (1970). Analysis of individual differences in multidimensional scaling via an N-way generalization of "Eckart-Young" decomposition. *Psychometrika*, 35(3), 283-319. DOI: 10.1007/BF02310791

De Chernatony, L. (1999). Brand management through narrowing the gap between brand identity and brand reputation. *Journal of Marketing Management*, 15(1–3), 157–179.

DeSarbo, W. S., and Rao, V. R. (1986). A constrained unfolding methodology for product positioning analysis. *Marketing Science*, 5(1), 1-19. DOI: 10.1287/mksc.5.1.1

Du, R. Y., & Kamakura, W. A. (2015). Improving the statistical performance of tracking studies based on repeated cross-sections with primary dynamic factor analysis. *International Journal of Research in Marketing*, 32(1), 94–112. DOI: 10.1016/j.ijresmar.2014.10.002

Esterhuizen, W., Levine, J., & Streif, S. (2021). Epidemic management with admissible and robust invariant sets. *PLOS ONE*, 16(9), e0257598.

Grimm, K. J., Zhang, Z., Hamagami, F., & Mazzocco, M. M. M. (2013). Modeling nonlinear change via latent change and latent acceleration frameworks: Examining velocity and acceleration of growth trajectories. *Multivariate Behavioral Research*, 48(1), 117–143. DOI: 10.1080/00273171.2012.755111

Ilchmann, A., Ryan, E. P., & Sangwin, C. J. (2002). Tracking with prescribed transient behaviour. *ESAIM: Control, Optimisation and Calculus of Variations*, 7, 471–493. DOI: 10.1051/cocv:2002064

Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering*, 82(1), 35–45.

Karcher, H. (1977). Riemannian center of mass and mollifier smoothing. *Communications on Pure and Applied Mathematics*, 30(5), 509–541. DOI: 10.1002/cpa.3160300502

Kane, V. E. (1986). Process capability indices. *Journal of Quality Technology*, 18(1), 41–52.

Kapferer, J.-N. (2012). *The New Strategic Brand Management: Advanced Insights and Strategic Thinking* (5th ed.). Kogan Page.

Green, P. E., & Srinivasan, V. (1978). Conjoint analysis in consumer research: Issues and outlook. *Journal of Consumer Research*, 5(2), 103–123. DOI: 10.1086/208721

Guo, Y., Li, W., Yang, G., Jiao, Z., & Yan, J. (2022). Combining dilution of precision and Kalman filtering for UWB positioning in a narrow space. *Remote Sensing*, 14(21), 5409. DOI: 10.3390/rs14215409

Hatch, M. J., & Schultz, M. (2010). Toward a theory of brand co-creation with implications for brand governance. *Journal of Brand Management*, 17(8), 590–604. DOI: 10.1057/bm.2010.14

Holland, P. W., & Hoskens, M. (2003). Classical test theory as a first-order item response theory: Application to true-score prediction from a possibly nonparallel test. *Psychometrika*, 68(1), 123–149. DOI: 10.1007/BF02296657

Horton, J. J., Filippas, A., & Manning, B. S. (2023). Large language models as simulated economic agents: What can we learn from Homo Silicus? NBER Working Paper 31122. National Bureau of Economic Research. arXiv: 2301.07543

Kaplan, E. D., & Hegarty, C. J. (Eds.) (2017). *Understanding GPS/GNSS: Principles and Applications* (3rd ed.). Artech House.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1–22.

Koenderink, J. J., & van Doorn, A. J. (2012). Gauge fields in pictorial space. *SIAM Journal on Imaging Sciences*, 5(4), 1213–1233. DOI: 10.1137/120861151

Kuhfeld, W. F., Tobias, R. D., & Garratt, M. (1994). Efficient experimental design with marketing research applications. *Journal of Marketing Research*, 31(4), 545–557. DOI: 10.1177/002224379403100408

Li, P., Castelo, N., Katona, Z., & Sarvary, M. (2024). Frontiers: Determining the validity of large language models for automated perceptual analysis. *Marketing Science*, 43(2), 254–266. DOI: 10.1287/mksc.2023.0454

Martinet, V., Thebaud, O., & Rapaport, A. (2010). Hare or tortoise? Trade-offs in recovering sustainable bioeconomic systems. *Environmental Modeling and Assessment*, 15(6), 503–517. DOI: 10.1007/s10666-010-9226-2

Medesani, M., & Macdonald, J. (2026). *Geometric Foundations of Invariant Corridors and Governance: A Unified Framework with Empirical Validation* (Level 3.3 Frozen Baseline). Zenodo. DOI: 10.5281/zenodo.18822552

Dew, R., Ansari, A., & Toubia, O. (2022). Letting logos speak: Leveraging multiview representation learning for data-driven branding and logo design. *Marketing Science*, 41(2), 401–425. DOI: 10.1287/mksc.2021.1326

Goli, A., & Singh, A. (2024). Frontiers: Can large language models capture human preferences? *Marketing Science*, 43(4), 709–722. DOI: 10.1287/mksc.2023.0306

McFadden, D., & Train, K. (2000). Mixed MNL models for discrete response. *Journal of Applied Econometrics*, 15(5), 447–470. DOI: 10.1002/1099-1255(200009/10)15:5<447::AID-JAE570>3.0.CO;2-1

Misra, P., & Enge, P. (2011). *Global Positioning System: Signals, Measurements, and Performance* (2nd ed.). Ganga-Jamuna Press.

Mitchell, I. M., Bayen, A. M., & Tomlin, C. J. (2005). A time-dependent Hamilton-Jacobi formulation of reachable sets for continuous dynamic games. *IEEE Transactions on Automatic Control*, 50(7), 947–957.

Molenaar, P. C. M. (1985). A dynamic factor model for the analysis of multivariate time series. *Psychometrika*, 50(2), 181–202. DOI: 10.1007/BF02294246

Naik, P. A., Mantrala, M. K., & Sawyer, A. G. (1998). Planning media schedules in the presence of dynamic advertising quality. *Marketing Science*, 17(3), 214–235.

Netzer, O., Toubia, O., Bradlow, E. T., Dahan, E., Evgeniou, T., Feinberg, F. M., Feit, E. M., Hui, S. K., Johnson, J., Liechty, J. C., Orlin, J. B., & Rao, V. R. (2008). Beyond conjoint analysis: Advances in preference measurement. *Marketing Letters*, 19(3–4), 337–354. DOI: 10.1007/s11002-008-9046-1

Oubraham, A., & Zaccour, G. (2018). A survey of applications of viability theory to the sustainable exploitation of renewable resources. *Ecological Economics*, 145, 346–367.

Oud, J. H. L., van den Bercken, J. H. L., & Essers, R. J. (1990). Longitudinal factor score estimation using the Kalman filter. *Applied Psychological Measurement*, 14(4), 395–418.

Resnikoff, H. L. (1974). Differential geometry and color perception. *Journal of Mathematical Biology*, 1, 97–131. DOI: 10.1007/BF00275798

Ries, A., & Trout, J. (1981). *Positioning: The Battle for Your Mind*. McGraw-Hill.

Rossi, P. E., Allenby, G. M., and McCulloch, R. (2005). *Bayesian Statistics and Marketing*. Wiley. DOI: 10.1002/0470863692

Sarti, A., Citti, G., & Petitot, J. (2008). The symplectic structure of the primary visual cortex. *Biological Cybernetics*, 98(1), 33–48. DOI: 10.1007/s00422-007-0194-9

Simon, H. A. (1951). A formal theory of the employment relationship. *Econometrica*, 19(3), 293–305. DOI: 10.2307/1906815

Simons, R. (1994). How new top managers use control systems as levers of strategic renewal. *Strategic Management Journal*, 15(3), 169–189.

Stevens, S. S. (1957). On the psychophysical law. *Psychological Review*, 64(3), 153-181. DOI: 10.1037/h0046162

Transtrum, M. K., Machta, B. B., Brown, K. S., Daniels, B. C., Myers, C. R., & Sethna, J. P. (2015). Perspective: Sloppiness and emergent theories in physics, biology, and beyond. *Journal of Chemical Physics*, 143(1), 010901. DOI: 10.1063/1.4923066

van der Linden, W. J., & Ren, H. (2015). Optimal Bayesian adaptive design for test-item calibration. *Psychometrika*, 80(2), 263–288. DOI: 10.1007/s11336-013-9391-8

Wald, A. (1947). An essentially complete class of admissible decision functions. *Annals of Mathematical Statistics*, 18(4), 549–555. DOI: 10.1214/aoms/1177730345

Wedel, M., and Kamakura, W. A. (2000). *Market Segmentation: Conceptual and Methodological Foundations* (2nd ed.). Springer. DOI: 10.1007/978-1-4615-4651-1

Zharnikov, D. (2026a). Spectral brand theory: a multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026e). Spectral metamerism in brand perception: projection bounds from high-dimensional geometry. Working Paper. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026f). Cohort boundaries in high-dimensional perception space: a concentration of measure analysis. Working Paper. https://doi.org/10.5281/zenodo.18945477

Zharnikov, D. (2026i). The organizational schema theory: test-driven business design. Working Paper. https://doi.org/10.5281/zenodo.18946043

Zharnikov, D. (2026o). Non-ergodic brand perception: why cross-sectional brand tracking systematically misrepresents individual trajectories. Working Paper. https://doi.org/10.5281/zenodo.19138860

Zharnikov, D. (2026s). Coherence type as crisis predictor: a formal derivation from non-ergodic dynamics. Working Paper. https://doi.org/10.5281/zenodo.19208107

Zharnikov, D. (2026v). Spectral metamerism in AI-mediated brand perception: how large language models collapse multi-dimensional brand differentiation in consumer search. Working Paper. https://doi.org/10.5281/zenodo.19422427

Zharnikov, D. (2026x). AI-native brand identity: from visual recognition to cryptographic verification. Working Paper. https://doi.org/10.5281/zenodo.19391476
