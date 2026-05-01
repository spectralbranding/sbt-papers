# From Order Effects to Absorbing States: A Non-Ergodic Framework for Multi-Dimensional Brand Perception Dynamics

**Dmitry Zharnikov**

Working Paper v2.2 -- May 2026

---

## Abstract

Brand tracking assumes cross-sectional averages (ensemble averages) yield the same information as individual trajectories over time (time averages)—an ergodicity assumption violated in brand perception. Drawing on Peters' (2019) framework from statistical physics, this paper identifies three structural sources of non-ergodicity: absorbing states from negative brand conviction, multiplicative signal dynamics, and path-dependent dimension weighting. Five formal propositions establish that signal order produces different perception profiles from identical signals; negative conviction functions as an absorbing state while positive conviction does not; cross-sectional tracking systematically overestimates brand health for absorption-risk brands; first signals anchor all subsequent updates in a dimension; and observer cohorts with different dimension weights produce divergent trajectories from identical signals. The paper specifies sufficient conditions for multiplicative perception updates and shows these conditions are empirically testable via longitudinal panel data. These propositions unify 80 years of scattered evidence on order effects, primacy, and belief updating within Spectral Brand Theory's eight-dimensional perception framework. The measurement implication is concrete: ensemble averages systematically misrepresent individual trajectories, and the bias direction and magnitude are predictable from brand coherence.

**Keywords**: non-ergodicity, belief updating, order effects, absorbing states, brand perception, path dependence, brand tracking, Spectral Brand Theory

---

Eighty years of consumer psychology have accumulated converging evidence that perception order matters: Asch's (1946) primacy effects, Hogarth and Einhorn's (1992) belief-adjustment model, Anderson's (1981) information integration theory, and Kardes and Kalyanaram's (1992) order-of-entry demonstrations all point to the same structural fact — the sequence in which signals are encountered shapes the perception formed from them in ways that are not recoverable by aggregation. Yet each of these research traditions has treated its order-effect findings as domain-specific phenomena. This paper argues that they are manifestations of a single underlying structure: non-ergodicity in brand perception dynamics.

The practical consequence is a measurement problem of systematic scope. Every major brand tracking system — from Kantar BrandZ to YouGov BrandIndex to NPS — operates on the same methodological principle: survey a cross-section of consumers at regular intervals, compute averages, and report the resulting scores as "brand health." This approach treats the population average at time *t* as informationally equivalent to the trajectory of any individual consumer through time. In the language of statistical physics, brand tracking assumes ergodicity: that time averages equal ensemble averages.

This paper argues this assumption is systematically violated.

Peters (2019), in a landmark paper in *Nature Physics*, demonstrated that the ergodicity assumption pervades economic theory and produces systematic errors whenever dynamics are non-additive. When a gamble's payoffs multiply (rather than add) with existing wealth, the expected value computed across a population of gamblers diverges from the time-average growth rate experienced by any individual gambler. The population average shows growth; the typical individual experiences ruin. The mathematical structure is not exotic — it is the difference between arithmetic and geometric means — but its consequences are profound. Peters and Gell-Mann (2016) showed that much of expected utility theory can be reinterpreted as an ergodicity correction: a mathematical patch applied to force non-ergodic dynamics into an ergodic framework. Doctor, Wakker, and Wang (2020) provide a formal rebuttal that sharpens the boundary conditions under which the ergodicity critique applies and those under which classical expected-utility reasoning survives, a boundary analysis directly relevant to specifying when the present framework's predictions hold in brand contexts.

Brand perception exhibits the same structural features that produce non-ergodicity in economic systems. Brand signals do not add to a blank slate; they interact multiplicatively with existing perceptions. A luxury brand's service failure (negative Experiential signal) is perceived differently by an observer who already holds positive Narrative and Temporal convictions than by one who does not — the existing perceptual state modulates the impact of new information. Memory decays, creating irreversibilities. Certain negative experiences produce conviction states from which recovery is structurally improbable — the consumer who concludes "this company is fundamentally dishonest" does not merely hold a low score that future positive signals can increment upward. And different consumers weight dimensions differently, so identical signal sequences produce divergent trajectories.

The contribution of this paper is threefold. First, we identify brand perception as a non-ergodic process and specify the three structural features that produce the non-ergodicity: absorbing states, multiplicative dynamics, and path-dependent weighting. Second, we develop five formal propositions that derive testable predictions from the non-ergodic framework. Third, we connect the scattered empirical evidence from consumer psychology — primacy effects, order effects, belief updating, path dependence — to a unified theoretical explanation. The propositions are grounded in Spectral Brand Theory's (Zharnikov, 2026a) eight-dimensional perception space, where non-ergodicity operates across multiple dimensions simultaneously, and draw on the formal dynamic model developed in Zharnikov (2026j). The unification claim applies to the B2C, high-involvement brand perception setting studied here; extension to commodity or low-involvement categories is a separate empirical question.

The implications for practice are immediate. If brand perception is non-ergodic, then cross-sectional brand tracking is not merely noisy — it is systematically biased. The direction of the bias is predictable: cross-sectional methods overestimate brand health for brands at risk of absorbing states and underestimate the strategic importance of touchpoint sequence. Brand managers who treat signal order as noise are discarding a first-order strategic variable.

---

## Theoretical Background

### 2.1 The Ergodicity Problem in Economics

The ergodicity concept originates in statistical mechanics, where Boltzmann's ergodic hypothesis asserts that a system's time average equals its ensemble average — that observing one particle for a long time yields the same statistical information as observing many particles at one instant (Birkhoff 1931). Peters (2019) demonstrated that this assumption, imported implicitly into economic theory, produces foundational errors.

Consider the simplest illustration. An investment grows by 50% with probability 0.5 and shrinks by 40% with probability 0.5 each period. The ensemble average (expected value) after one period is 1.05 — a 5% expected gain. Across a population of investors, the average wealth grows. But the time average for any individual investor, computed as the geometric mean, is $\sqrt{1.5 \times 0.6} \approx 0.949$ — a 5.1% loss per period. The typical individual goes bankrupt while the population average grows, because the population average is dominated by a shrinking fraction of increasingly wealthy survivors.

The divergence between ensemble and time averages arises from three structural features: (a) multiplicative dynamics, where outcomes scale existing states rather than adding to them; (b) irreversibilities or absorbing states, where certain outcomes remove participants from the process; and (c) heterogeneous trajectories, where individual paths diverge even under identical stochastic rules. Peters and Gell-Mann (2016) showed that expected utility theory can be understood as an implicit ergodicity correction — the utility function's concavity approximates the transformation needed to convert a non-ergodic process into an ergodic one. Doctor et al. (2020) offer a precise set of conditions delimiting this reinterpretation, establishing that the ergodicity critique is strongest when dynamics are strictly multiplicative and long-run behavior is the criterion.

The critical insight for brand research is methodological: whenever dynamics are non-ergodic, cross-sectional averages provide misleading information about individual trajectories. If brand perception dynamics share the structural features that produce non-ergodicity in economic systems — multiplicativity, absorbing states, heterogeneous trajectories — then brand tracking methods that rely on cross-sectional averaging are systematically biased.

### 2.2 Path Dependence in Consumer Psychology

The consumer psychology literature contains extensive evidence of order effects, primacy, and path dependence in perception formation — evidence that is consistent with non-ergodic dynamics, though it has never been interpreted through that lens.

**Primacy in impression formation.** Asch's (1946) foundational experiments demonstrated that the order of trait adjectives systematically affects impression formation. Describing a person as "intelligent, industrious, impulsive, critical, stubborn, envious" produces a more favorable impression than presenting the same adjectives in reverse order. The first traits encountered establish a frame through which subsequent traits are interpreted — a form of path dependence that violates the ergodic assumption of order-independence.

**Belief updating and order effects.** Hogarth and Einhorn (1992) developed the most comprehensive formal model of order effects in belief updating. Their belief-adjustment model demonstrates that the same set of evidence, presented in different orders, produces systematically different final beliefs. Critically, they distinguish between step-by-step processing (where beliefs are updated after each piece of evidence) and end-of-sequence processing (where all evidence is integrated simultaneously). Step-by-step processing — the mode most relevant to real-world brand perception, where signals arrive sequentially over time — produces the strongest order effects. The model shows that recency effects dominate in short sequences while primacy effects dominate in long sequences, and that the direction of asymmetry depends on the strength of individual evidence items relative to the current belief anchor.

**Order-of-entry effects.** Kardes and Kalyanaram (1992) demonstrated that pioneering brands benefit from a structural advantage in consumer memory and judgment that persists beyond any quality differential. The first brand encountered in a category establishes the reference point against which subsequent entrants are judged — an anchoring effect that operates at the category level and compounds over time. This is path dependence at the market level: the sequence in which brands enter a consumer's awareness permanently shapes subsequent perception.

**Signal integration order.** Smith and Vogt (1995) showed that the order of advertising and negative word-of-mouth exposure produces different cognitive processing and perception outcomes. Consumers who encounter advertising before negative word-of-mouth develop different perceptual structures than those who encounter the same information in reverse order. This finding is directly relevant to brand crisis management, where the question of whether consumers encountered the crisis signal before or after a reservoir of positive brand signals materially affects the outcome.

**Path-dependent consumption.** Siray (2016) developed formal models of consumption paths in which the sequence of consumption experiences — not merely the set of experiences — determines preference formation. This work brings the mathematical vocabulary of path dependence into consumer behavior, demonstrating that consumption histories are not commutative: experiencing product A before product B produces different preferences than experiencing B before A.

**Information integration and Bayesian updating.** Anderson's (1981) Foundations of Information Integration Theory provides a systematic account of how people combine multiple pieces of information into unified judgments. Anderson's work demonstrates that integration is typically not simple averaging — weights are assigned dynamically based on the diagnosticity and extremity of each information cue, creating the kind of nonlinear, path-sensitive updating that the present framework formalizes. Dzyabura and Hauser (2019) show that consumers actively learn their own preference weights through sequential product experience, demonstrating that the dimension-weighting process is itself dynamic and path-dependent — consistent with Source 3 of the non-ergodic framework (discussed under Three Sources of Non-Ergodicity). Kruschke (2008) extends this line of work with a Bayesian attention-shifting model in which the allocation of processing capacity to different cues depends on the observer's history of prior cue-outcome experiences — precisely the kind of state-dependent weighting that Source 3 formalizes.

Bayesian updating assumes a well-defined likelihood function and, given sufficient data, converges to the true parameter regardless of the prior. This convergence property is the defining feature of Bayesian models: they are inherently ergodic in the sense that posteriors ultimately agree across agents with different priors, provided data accumulates.

Non-ergodic perception violates this convergence because absorbing states are structurally non-Bayesian: an observer who reaches the conviction that a brand is fundamentally dishonest does not update this conviction in proportion to new evidence. The absorbing state corresponds to a collapsed likelihood function where no evidence is deemed diagnostic in the positive direction. This is precisely what Bayesian models cannot accommodate — a state from which no data updates the belief. The non-ergodic framework, by formalizing absorbing states and path-dependent dynamics, captures a regime of sequential information processing that lies outside the Bayesian paradigm.

These findings collectively demonstrate that brand perception violates a necessary condition for ergodicity: exchangeability of observations. In an ergodic process, the order of observations does not matter — permuting the sequence produces the same long-run statistics. In brand perception, the order is a first-order determinant of outcomes.

### 2.3 Spectral Brand Theory and Dynamic Perception

Spectral Brand Theory (Zharnikov, 2026a) models brand perception as an eight-dimensional vector space defined by Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal dimensions. Each observer forms a perception profile — a weighted combination of brand signals filtered through their individual dimension weights (the observer spectral profile). Observers cluster into cohorts based on similar dimension weights, and cohort-level perception patterns emerge as perception clouds in eight-dimensional space.

Zharnikov (2026j) developed the formal dynamic model, modeling perception evolution as a stochastic process on the positive octant of the 7-sphere ($S^7_+$), with signal encounters driving Brownian motion, signal decay creating drift toward a neutral prior, and negative conviction creating absorbing boundaries. That paper established four theorems: well-posedness of the stochastic differential equation, survival probability decay rates, spectral gap bounds for mixing, and formal non-ergodicity (time-average and ensemble-average divergence with probability 1).

The present paper translates the mathematical machinery of Zharnikov (2026j) into a conceptual framework accessible to consumer psychology and brand management researchers. Where Zharnikov (2026j) operates in the language of stochastic differential equations and Laplace-Beltrami operators, this paper operates in the language of propositions, empirical evidence, and managerial implications. The two papers are complements: Zharnikov (2026j) provides the mathematical foundation; this paper provides the theoretical interpretation and connects to the empirical literature.

Three features of the SBT dynamic model are essential for the argument that follows:

1. **Multi-dimensional simultaneous dynamics.** Brand perception does not evolve on a single attitude scale. It evolves on eight dimensions simultaneously, with signals potentially affecting multiple dimensions at once. A crisis event does not merely lower a score; it reshapes the geometry of the perception profile across Experiential, Narrative, and Social dimensions simultaneously. This multi-dimensionality means that path dependence operates in higher-dimensional space than any single-dimension model can capture.

2. **Three emission types.** SBT distinguishes positive signals (active, intentional brand emissions), null signals (absence of expected signals), and structural absence (dark signals — the systematic failure to emit in a dimension where emission is expected). Structural absence is particularly important for non-ergodicity because it creates a form of path dependence invisible to traditional measurement: a brand that has never signaled on a dimension creates a perception vacuum that subsequent signals fill differently than they would in the presence of an existing perceptual anchor.

3. **Coherence as trajectory stability.** SBT's coherence typology (ecosystem > signal > identity > experiential asymmetry > incoherent) maps directly to trajectory stability in the dynamic model. Ecosystem-coherent brands (e.g., Hermès) have emission profiles that produce stable, interior trajectories with low absorption risk. Incoherent brands (e.g., Tesla) have profiles that produce volatile trajectories with high absorption risk. This connection between static coherence type and dynamic trajectory stability is a key prediction of the non-ergodic framework.

---

## The Non-Ergodic Brand Perception Model

### 3.1 Formal Definition: When Time-Averages Differ from Ensemble-Averages in Brand Perception

We begin with a formal statement of what non-ergodicity means in the brand perception context. Let $x_i(t) \in \mathbb{R}^8_+$ denote observer *i*'s perception profile of a brand at time *t*. The perception profile is a normalized vector capturing the observer's internal representation of the brand across eight dimensions. The perception space and its geometric properties are formalized in Zharnikov (2026d); the present model inherits that metric structure.

**Definition 1 (Ensemble average).** The ensemble average at time *t* is the cross-sectional mean across *N* observers:

$$\bar{x}^{(E)}(t) = \frac{1}{N} \sum_{i=1}^{N} x_i(t)$$

This is what brand tracking measures: survey *N* consumers at time *t*, compute the average.

**Definition 2 (Time average).** The time average for observer *i* over the interval $[0, T]$ is:

$$\bar{x}_i^{(T)} = \frac{1}{T} \int_0^T x_i(t) \, dt$$

This is what brand tracking does not measure: track one consumer's perception continuously over time.

**Definition 3 (Ergodicity in brand perception).** Brand perception is ergodic if, for all observers *i* and all sufficiently large *T*:

$$\bar{x}_i^{(T)} \to \bar{x}^{(E)}(t) \quad \text{as } T \to \infty$$

That is, the long-run time average for any individual converges to the cross-sectional average. If this condition holds, brand tracking (which measures ensemble averages) provides valid information about individual trajectories.

**Claim.** Brand perception is non-ergodic: $\bar{x}_i^{(T)} \not\to \bar{x}^{(E)}(t)$ in general. The divergence arises from three structural sources.

### 3.2 Three Sources of Non-Ergodicity

#### Source 1: Absorbing States

An absorbing state is a perceptual configuration from which no transition is possible — or more precisely, from which the probability of transition is negligible. In brand perception, absorbing states arise from deeply negative brand conviction.

Consider an observer who, through accumulated negative experiences, reaches the conviction that a brand is fundamentally dishonest. This conviction does not occupy the same psychological space as a merely low attitude score. It functions as a categorical judgment — a boundary crossing that restructures the observer's entire perceptual relationship to the brand. Subsequent positive signals are processed through the lens of this conviction: a generous corporate donation is interpreted as reputation-laundering; a quality improvement is dismissed as temporary; a sincere apology is perceived as strategic.

In the language of SBT's dynamic model (Zharnikov, 2026j), the absorbing state corresponds to the boundary of the positive octant $S^7_+$ — the region where one or more perceptual dimensions reach zero. Once an observer's perception of a brand's Narrative or Ideological integrity reaches zero, the trajectory is effectively absorbed: it does not return to the interior.

Absorbing states produce non-ergodicity through a selection mechanism. Over time, observers are progressively absorbed at the boundary, removing them from the active population. The ensemble average at time *t* is computed only over survivors — those who have not yet been absorbed. But the time average for any individual includes the period before absorption and the absorbing state itself. As the population is depleted by absorption, the ensemble average increasingly represents a positively selected subpopulation, systematically diverging from typical individual trajectories.

This mechanism is mathematically identical to the survivorship bias in Peters' (2019) wealth dynamics: the population average shows growth because it averages over survivors, while the typical individual experiences ruin. The mathematical treatment of Markov chains with absorbing boundaries, formalized in Kemeny and Snell (1960), provides the foundational lineage for the absorbing-state construction here.

#### Source 2: Multiplicative Dynamics

Brand signals do not add to perception in the way that deposits add to a bank account. They multiply with existing perceptual states. A positive Experiential signal for Hermès — an exquisite in-store experience — has a different perceptual impact on an observer who already holds strong positive Semiotic and Temporal convictions than on an observer who encounters the brand for the first time. The existing perceptual context amplifies or attenuates the signal.

Formally, if $x_i^{(d)}(t)$ is observer *i*'s perception in dimension *d* at time *t*, and $s^{(d)}$ is an incoming signal in dimension *d*, the update rule is not additive:

$$x_i^{(d)}(t+1) \neq x_i^{(d)}(t) + \alpha \cdot s^{(d)}$$

Rather, it is multiplicative or interaction-dependent:

$$x_i^{(d)}(t+1) = f(x_i^{(d)}(t), s^{(d)}, x_i^{(-d)}(t))$$

where $x_i^{(-d)}(t)$ denotes the observer's perception in all dimensions other than *d*. The cross-dimensional interaction term is essential: it captures the fact that a brand's Experiential signal is perceived in the context of its Narrative, Ideological, and other dimensions.

The interaction function $f(\cdot)$ exhibits multiplicative-like properties in the following sense: the impact of an incoming signal $s^{(d)}$ is proportional to the observer's current perceptual state $x_i^{(d)}(t)$ and its cross-dimensional context $x_i^{(-d)}(t)$. A signal that doubles perceived Experiential quality has a larger absolute effect on an observer who already holds strong cross-dimensional perceptions than on one who does not, because the cross-dimensional context amplifies the signal's reach. More precisely, the update function is concave in the signal when the current state is large, meaning that the marginal perceptual gain from an additional unit of positive signal diminishes with existing perceptual strength. This concavity is the essential property: whenever the update function is concave or nonlinear (rather than purely additive), Jensen's inequality implies that the arithmetic mean of outcomes (the ensemble average) exceeds the geometric mean (the time average experienced by any individual observer). The ensemble average therefore systematically overstates the growth rate experienced by typical individuals — even without strict multiplicativity in the narrow mathematical sense.

#### Source 3: Path-Dependent Dimension Weighting

In SBT, each observer possesses an observer spectral profile — a vector of dimension weights $w = (w_1, \ldots, w_8)$ that determines how strongly each dimension contributes to the observer's perception. These weights are not fixed; they are shaped by the observer's history of signal encounters.

An observer whose first significant brand encounter is Experiential (e.g., a product trial) develops an Experiential-weighted perceptual frame. Subsequent signals are filtered through this frame: Narrative signals are interpreted through the lens of Experiential expectations, Ideological signals are evaluated for consistency with Experiential quality. An observer whose first encounter is Narrative (e.g., reading a brand origin story) develops a different frame. The two observers, encountering identical subsequent signals, produce divergent perception trajectories.

This path dependence in dimension weighting means that even within a single observer cohort (a group with similar initial dimension weights), trajectory divergence accumulates over time as individual signal histories shape individual weight profiles. The ensemble average over the cohort captures the centroid of a dispersing cloud, not the trajectory of any individual member.

Zharnikov (2026v) provides direct empirical evidence of degenerate weighting in non-human observers: large language models evaluated in a sequential-allocation format exhibit a first-listed dimension premium (+6.1 points, d = 1.39, p < .001) that virtually disappears under independent Likert elicitation (d = .22). This format-mediated suppression of path-dependent weighting in AI observers — a population whose priors do not accumulate across sessions — establishes a useful baseline: the path-dependence signal identified here is carried by the sequential allocation mechanism, not merely by perceptual encoding. Human observers accumulate cross-session histories, and the weighting dynamics are expected to be stronger, not weaker, than this LLM baseline.

### 3.3 The Belief-Adjustment Mechanism: Connecting Hogarth and Einhorn (1992) to Peters (2019)

The three sources of non-ergodicity identified above are not merely theoretical constructs. They connect directly to Hogarth and Einhorn's (1992) belief-adjustment model, one of the most widely applied formal models of sequential belief updating in the consumer psychology literature.

In the Hogarth-Einhorn model, belief revision proceeds as:

$$S_k = S_{k-1} + w_k [s(x_k) - R]$$

where $S_k$ is the belief after *k* pieces of evidence, $s(x_k)$ is the evaluation of evidence piece *k*, $R$ is the reference point (either the initial anchor $S_0$ or the current belief $S_{k-1}$), and $w_k$ is the adjustment weight.

Two features of this model connect it to non-ergodic dynamics. First, the reference point $R$ is path-dependent: it depends on the current state, which depends on the entire history of prior updates. This creates the interaction between current state and new information that characterizes multiplicative dynamics. Second, the adjustment weight $w_k$ depends on the strength of the evidence relative to the reference point, creating an asymmetry between positive and negative updates: strong negative evidence (large negative $s(x_k) - R$) produces larger adjustments than equivalently strong positive evidence, because the reference point shifts toward the negative direction with each update.

The Hogarth-Einhorn model was developed to explain order effects in belief updating. We reinterpret it as evidence of non-ergodic dynamics: the path dependence and asymmetric adjustment that produce order effects are precisely the features that produce time-average versus ensemble-average divergence. This reinterpretation does not contradict the original model; it embeds it in a more general framework.

In the SBT context, the Hogarth-Einhorn mechanism operates on each of eight dimensions simultaneously. The reference point in each dimension is the observer's current perception in that dimension, which depends on the entire history of signals in that dimension (and, through cross-dimensional interactions, on signals in all other dimensions). The adjustment weight depends on the observer's dimension-specific sensitivity (captured by the observer spectral profile) and on the signal type (positive, null, or structural absence). The result is a high-dimensional belief-updating process with order dependence operating across all eight dimensions simultaneously.

### 3.4 Boundary Conditions

The non-ergodic framework developed in this paper applies with full force under conditions that are common in high-involvement brand perception but may be weakened or absent elsewhere. Four boundary conditions govern the scope of the propositions.

**Low-involvement categories.** In categories where consumers engage in minimal deliberative processing — commodity goods, habitual repurchases, low-stakes service decisions — the multiplicative update mechanism (Source 2) is attenuated. When signals are processed heuristically rather than relationally, the cross-dimensional context does not amplify incoming information, and the update function approximates the additive regime in which ergodicity holds. The propositions apply primarily to categories where consumers actively integrate signals across multiple brand dimensions.

**Commodity and undifferentiated goods.** Source 3 (path-dependent dimension weighting) requires that consumers possess heterogeneous observer spectral profiles — meaningfully different weightings across the eight SBT dimensions. In commodity categories where brand differentiation is minimal, dimension weights may cluster tightly, suppressing the cohort divergence mechanism. The propositions assume sufficient brand dimensionality to activate differential weighting.

**Short-horizon decisions.** Absorbing states (Source 1) develop through sustained accumulation of negative conviction. For single-occasion purchase decisions or very short-horizon evaluations, the trajectory may not be long enough for absorbing states to form. P2 and P3 are most relevant in ongoing brand relationships where conviction builds across repeated encounters.

**Elicitation modality.** As the R15 evidence (Zharnikov 2026v) documents, the primacy mechanism operates through sequential allocation processes rather than perceptual encoding per se. Measurement designs that elicit independent ratings across dimensions may underestimate path-dependent effects compared to sequential or holistic elicitation formats. This is a methodological boundary condition: the propositions describe perceptual dynamics, but their empirical signature depends on whether measurement instruments preserve or suppress the sequential structure.

---

## Propositions

We now state five formal propositions that derive from the non-ergodic brand perception model. Each proposition is followed by its theoretical argument and its connection to the three sources of non-ergodicity identified above.

### Proposition 1: Signal Order Effect

*The same set of brand signals, encountered in different temporal orders, produces structurally different perception profiles in the observer. The difference is not noise; it is a systematic function of the interaction between signal sequence and the observer's evolving perceptual state.*

**Theoretical argument.** Consider an observer who encounters two signals: a strong positive Experiential signal (E+) and a strong negative Ideological signal (I-). In sequence [E+, I-], the observer first forms a positive Experiential anchor, then encounters the negative Ideological signal. The existing positive Experiential perception provides a partially protective context: the observer may interpret the Ideological signal as a specific failure within a generally positive brand, limiting its impact on non-Ideological dimensions. In sequence [I-, E+], the observer first forms a negative Ideological anchor, then encounters the positive Experiential signal. The existing negative perception creates a skeptical frame: the positive experience may be interpreted as inconsistent with the brand's fundamental character, or as a deliberate attempt to compensate for known failures.

The asymmetry arises from Source 2 (multiplicative dynamics): each signal's perceptual impact is modulated by the existing perceptual state, which is itself the product of all prior signals. Since the existing state at the time of each signal encounter differs between the two sequences, the final states differ. The difference is not random variation; it is a deterministic function of the sequence-state interaction.

In the SBT framework, this proposition has a geometric interpretation. The two signal sequences trace different paths on $S^7_+$. Because the manifold is curved (perception profiles are normalized), the paths are not merely displaced versions of each other — they arrive at structurally different locations in eight-dimensional space, with different dimension ratios and different distances from absorbing boundaries.

**Source of non-ergodicity:** Multiplicative dynamics (Source 2), path-dependent weighting (Source 3).

*Falsification.* P1 would be challenged if repeated experimental manipulations of signal order (holding the signal set constant) produce statistically indistinguishable final perception profiles across all eight SBT dimensions — that is, if a log-linear model of sequential belief updating shows no significant sequence × state interaction term, and permutation tests on longitudinal panel data yield order effects no larger than measurement noise. A finding that identical signal sets presented in different temporal orders converge to the same perception profile would challenge the multiplicative-interaction claim and reduce the framework to an additive (ergodic) special case.

### Proposition 2: Absorbing State Asymmetry

*Negative brand conviction functions as an absorbing state: once an observer crosses the threshold from negative perception to negative conviction, the probability of return to neutral or positive perception is negligible. Positive brand conviction does not function as an absorbing state: even strongly positive conviction can be disrupted by sufficiently negative signals.*

**Theoretical argument.** The asymmetry between positive and negative conviction reflects a fundamental asymmetry in human psychology: negative events are processed more deeply, weighted more heavily, and remembered longer than equivalently valenced positive events — a pattern that Baumeister et al. (2001) term "bad is stronger than good" and document across evaluation, learning, and social relationships. In the brand context, this asymmetry is amplified by the trust asymmetry (Slovic, 1993): trust is built incrementally through repeated consistent positive signals and destroyed rapidly through single sufficiently negative signals. In SBT's language, positive conviction creates a perceptual state deep in the interior of $S^7_+$, far from absorbing boundaries. The distance from the boundary provides a buffer: negative signals move the perception toward the boundary, but if the starting position is sufficiently interior, many negative signals are required to reach absorption. The trajectory remains reversible as long as it stays in the interior.

Negative conviction, by contrast, corresponds to a position at or near the boundary of $S^7_+$ — a point where one or more dimensions are at or near zero. At the boundary, the dynamics change qualitatively. In SBT's formal model (Zharnikov, 2026j), the boundary is absorbing: trajectories that reach it do not return. The psychological mechanism is the shift from evaluative processing to categorical processing. An observer with a slightly negative perception is still evaluating the brand incrementally, processing each new signal on its merits. An observer who has reached the conviction that the brand is "fundamentally dishonest" or "irredeemably harmful" has shifted to categorical processing: all subsequent signals are interpreted through the lens of the categorical judgment, and no individual signal is sufficient to overturn the category.

This asymmetry is the direct analog of ruin in Peters' (2019) economic framework. An investor with positive wealth can always suffer losses; an investor who reaches zero (bankruptcy) is permanently removed from the game. The absorbing barrier at zero produces the divergence between time and ensemble averages that is the hallmark of non-ergodicity.

**Source of non-ergodicity:** Absorbing states (Source 1).

*Falsification.* P2 would be challenged if longitudinal absorption rate measurement shows symmetric recovery probabilities: specifically, if observers who cross from negative perception to negative conviction return to neutral or positive perception at rates statistically comparable to the rate at which observers who cross from positive to negative perception recover (i.e., if the return probability from negative conviction is not significantly lower than the return probability from negative perception). A symmetric recovery distribution — or one in which sufficiently strong positive signals predictably restore absorbed observers — would undermine the absorbing-boundary interpretation and reduce P2 to a standard asymmetric-updating model.

### Proposition 3: Ensemble-Time Divergence

*Cross-sectional brand tracking systematically overestimates brand health for brands with absorbing-state risk. The magnitude of overestimation increases with: (a) the brand's proximity to absorbing boundaries (lower coherence), (b) the variance of signal quality, and (c) the duration of the tracking period.*

**Theoretical argument.** Cross-sectional brand tracking computes the ensemble average at each measurement point. The ensemble average includes only observers who have not been absorbed — those who still hold non-zero perception across all measured dimensions. Observers who have reached negative conviction (the absorbing state) either drop out of the sample (they refuse to respond to surveys about brands they have written off), provide extreme negative responses that are treated as outliers, or are systematically underrepresented because tracking surveys typically sample from brand-aware populations that exclude fully absorbed observers.

The result is survivorship bias of precisely the type that Peters (2019) identifies in wealth dynamics. At time $t=0$, the ensemble and time averages coincide (no one has been absorbed yet). As time progresses, observers are absorbed at a rate that depends on the brand's proximity to absorbing boundaries. Those who remain in the ensemble are a positively selected subgroup — they are the observers whose individual trajectories have, by fortune of signal sequence and initial position, avoided absorption. Their average overstates the perception that a typical observer would hold if tracked over time.

The overestimation is worse for low-coherence brands for a precise reason: incoherent brands have emission profiles that place observers closer to absorbing boundaries on average. An incoherent brand like Tesla, with high variance across dimensions (Zharnikov, 2026a), produces trajectories that frequently approach the boundary of $S^7_+$, leading to higher absorption rates and greater survivorship bias in the remaining ensemble. An ecosystem-coherent brand like Hermès, with balanced, elevated emission across all dimensions, produces trajectories that remain deep in the interior, rarely approaching absorption, and thus exhibits minimal ensemble-time divergence.

**Source of non-ergodicity:** Absorbing states (Source 1), multiplicative dynamics (Source 2).

*Falsification.* P3 would be challenged if a carefully matched longitudinal panel study — one that tracks individual observers over multiple waves while correcting for attrition through inverse probability weighting — finds that individual time averages converge to the ensemble average with probability approaching 1 as the panel duration increases. Concretely, if the variance of the individual-level deviation $|\bar{x}_i^{(T)} - \bar{x}^{(E)}(t)|$ decreases to zero as $T \to \infty$ for a high-absorption-risk brand (low coherence, high signal variance), P3 would not be supported. A finding that ensemble averages accurately predict individual-level long-run perception — even after correcting for panel attrition — would indicate that the survivorship-bias mechanism is empirically negligible.

### Proposition 4: First-Signal Anchoring

*The first signal an observer encounters in a given perceptual dimension anchors all subsequent updates in that dimension. The anchoring effect diminishes with each subsequent signal but does not vanish: the first signal permanently biases the steady-state perception in the direction of its valence.*

**Theoretical argument.** When an observer has no prior perception in a dimension (the dimension is perceptually empty — what SBT calls structural absence), the first signal encountered in that dimension fills a vacuum. There is no existing state to moderate the signal's impact, no prior belief to dilute the new information. The first signal becomes the reference point — the anchor — against which all subsequent signals are evaluated.

This proposition connects to Hogarth and Einhorn's (1992) belief-adjustment model through the reference point mechanism. In their framework, the initial belief $S_0$ serves as the anchor for subsequent updating. When $S_0$ is formed by the first signal (rather than by a pre-existing prior), the first signal has disproportionate influence because every subsequent update is computed as a deviation from a reference that the first signal established.

The proposition also connects to Kardes and Kalyanaram's (1992) order-of-entry effects: the first brand encountered in a product category establishes the perceptual reference point for all subsequent brands. We extend this from the category level to the dimension level within SBT: the first signal in any of the eight dimensions establishes the perceptual anchor for that dimension.

The mathematical mechanism is the interaction between structural absence and multiplicative dynamics. In a dimension with no prior signal, the observer's perception is zero or undefined. The first signal sets the initial value. Since all subsequent updates are multiplicative (they scale with the current value), the first signal's contribution is compounded into every subsequent state. Even after many updates, the influence of the first signal persists as a component of the current state — diminished by subsequent updates but never fully eliminated.

The practical implication is a "first-signal premium": the first touchpoint in any dimension has outsized influence on long-run perception. This is distinct from mere recency or primacy effects; it is a structural feature of sequential updating in a previously empty dimension.

An illustrative baseline is available from a serial position experiment using large language model observers (Zharnikov 2026v, Section 5.15). In this non-human context, JSON sum-to-100 allocation produces a first-listed dimension premium of +6.1 points above the last (d = 1.39, p < .001), while independent 1–5 Likert ratings virtually eliminate the effect (d = .22). This baseline is informative not as primary evidence for P4 — LLM observers lack the cross-session memory accumulation that characterizes human brand perception — but as an elicitation-modality diagnostic: the primacy mechanism operates through the sequential allocation process rather than perceptual encoding per se. Human observers accumulate cross-session histories, and the weighting dynamics are expected to be stronger, not weaker, than this LLM baseline. The format-dependence result also establishes a methodological boundary condition for P4 tests: measurement instruments must preserve sequential structure to detect the anchoring effect (see also Boundary Conditions).

**Source of non-ergodicity:** Multiplicative dynamics (Source 2), path-dependent weighting (Source 3).

*Falsification.* P4 would be challenged if a within-subject experimental design — presenting matched first signals of different valence in randomly assigned perceptual dimensions, then exposing all subjects to the same subsequent signal sequence — finds no significant long-run difference in steady-state perception attributable to the first-signal manipulation. Specifically, if a mixed-effects model of per-dimension perception over a multi-period horizon shows that the first-signal coefficient decays to statistical non-significance within a finite and short window (e.g., three to five subsequent signals), P4's claim of persistent anchoring would not be supported. If subsequent signal exposure, accumulated over a moderate number of encounters, effectively resets the first-signal anchor to zero, the proposition would reduce to a transient primacy effect rather than a structural feature of sequential updating.

### Proposition 5: Cohort Trajectory Divergence

*Observer cohorts with different dimension weights, exposed to identical signal sequences, produce divergent perception trajectories. The divergence increases over time and does not converge — there is no long-run equilibrium in which different cohorts perceive the brand identically.*

**Theoretical argument.** In SBT, observer cohorts are defined by clusters of similar observer spectral profiles — similar dimension weights. A Semiotic-dominant cohort (high weight on visual identity, design language) perceives the same brand signals differently than a Narrative-dominant cohort (high weight on brand story, founding mythology) or an Ideological-dominant cohort (high weight on values, political positioning).

When two cohorts with different dimension weights $w_A$ and $w_B$ encounter the same signal $s$, they produce different perception updates because the signal is filtered through different weights. After one signal, the difference is $|w_A \odot s - w_B \odot s|$ (where $\odot$ denotes element-wise multiplication and $|\cdot|$ is the appropriate metric). After two signals, the difference includes the interaction between the first update and the second signal, which differs for the two cohorts because their first-round updates were different. The divergence compounds with each signal encounter.

Critically, the divergence does not converge to zero in the long run. In an ergodic system, all observers would converge to the same stationary distribution regardless of their processing weights, given sufficient data. In the non-ergodic brand perception system, the stationarity condition fails: each cohort's trajectory is shaped by the interaction between its specific dimension weights and the specific signal sequence, and these interactions produce permanently different long-run states.

This proposition provides the theoretical foundation for SBT's cohort concept. Cohorts are not merely demographic categories; they are perceptual communities whose perception trajectories diverge structurally from other communities exposed to the same brand signals. The divergence is not a failure of communication (the signals are identical) but a structural consequence of heterogeneous perception (the observer spectral profiles differ).

Grier and Brumbaugh's (1999) research on target and non-target market perceptions provides direct evidence: the same advertisement produces different perceived meanings depending on the observer's cultural perspective. Puntoni et al. (2011) show that the same advertising language activates different emotional responses depending on bilingual processing mode. Both findings are manifestations of cohort trajectory divergence: identical signals, filtered through different observer spectral profiles, produce divergent perceptions that accumulate over time.

**Source of non-ergodicity:** Path-dependent weighting (Source 3).

*Falsification.* P5 would be challenged if cohorts defined by significantly different observer spectral profiles (verified through pre-exposure dimension-weight elicitation) converge to indistinguishable perception trajectories after exposure to a sufficient number of shared brand signals — that is, if a multi-level model of cohort-level perception over time finds no significant cohort × time interaction, and the within-cohort variance in trajectory end-states does not exceed the between-cohort variance. A finding that heterogeneous dimension weights produce only transient differences that resolve into a common attractor would indicate that the cross-cohort divergence mechanism is dominated by ergodicity-restoring forces not captured by the current framework.

### 4.5 When Is Perception Multiplicative? Sufficiency Conditions

The non-ergodicity results in Propositions 1-5 depend on perception updates being multiplicative rather than additive. This section states sufficient conditions for the multiplicative regime and identifies the empirically testable boundary between the two regimes.

Three conditions, each independently sufficient, establish multiplicative updating dynamics:

**(C1) Signal relativity.** Each new signal is interpreted relative to current perception, not on an absolute scale. Formally, the update function $f$ satisfies $f(x, s) = x \cdot g(s/x)$ rather than $f(x, s) = x + h(s)$, where $g(\cdot)$ and $h(\cdot)$ are monotone functions. When the perceived magnitude of a signal depends on the ratio of the signal to current perception — when observers ask "is this twice as good as I already believed?" rather than "does this add ten points to my score?" — the dynamics are multiplicative. This is the natural mode of comparative evaluation: consumers calibrate new signals against their existing perceptual anchor.

**(C2) Confirmation bias modulation.** Prior perception modulates signal interpretation strength. Hogarth and Einhorn's (1992) belief-adjustment model provides direct formal support: evidence weight depends on the order in which it is encountered and on the current belief state, consistent with multiplicative accumulation. An observer who already holds strong positive Narrative conviction interprets a new Narrative signal as confirmation and assigns it high weight; an observer with weak priors assigns the same signal a lower weight. The weight is not fixed but scales with the current state — the defining property of multiplicative dynamics.

**(C3) Proportional decay.** Forgetting reduces perception by a fraction per unit time rather than by a constant amount. This is the Weber-Fechner decay law applied to brand memory: the rate of forgetting is proportional to the current memory strength. The differential equation governing this process is $\frac{dx}{dt} = -\lambda x$, whose solution is $x(t) = x(0) e^{-\lambda t}$ — an exponential, not linear, decay. Exponential decay is multiplicative: the perception at time $t+1$ is a fixed fraction $e^{-\lambda}$ of the perception at time $t$, regardless of absolute level. Linear decay ($\frac{dx}{dt} = -c$) would be additive and ergodic; proportional decay makes each time step a multiplication.

A key observation follows from this taxonomy: when any of C1-C3 holds uniformly across the observer population, the dynamics are multiplicative and the five propositions apply. When all three conditions fail uniformly — signals are evaluated on absolute scales, priors do not modulate interpretation, and forgetting is linear — the dynamics become additive and ergodic. Time averages converge to ensemble averages, and cross-sectional brand tracking provides valid individual-level information. This is precisely the implicit assumption of classical brand tracking (Keller, 1993; Aaker, 1991): that perception updates add to a cumulative score, that each new touchpoint contributes independently of the current state, and that memory decays linearly. The non-ergodic framework reveals this as a special case rather than the general case.

The accumulator dynamics developed by Busemeyer and Townsend (1993) in decision field theory provide a complementary formalization. In their framework, preference states evolve via a stochastic differential equation in which the valence of each option is weighted by the observer's current attention state — an explicitly multiplicative structure. The model generates order effects, preference reversals, and path dependence as natural predictions, reinforcing the view that multiplicative updating is the rule in sequential perceptual processes rather than the exception.

**Empirical testability.** The multiplicative versus additive distinction is directly testable via longitudinal panel data. If updating is multiplicative, repeated brand perception measurements will be better described by a log-linear model (regressing log-perception at time $t+1$ on log-perception at time $t$ and log-signal strength) than by a linear additive model (regressing perception at $t+1$ on perception at $t$ and signal strength). The log-linear model's fit advantage over the linear model quantifies the degree to which perception dynamics are multiplicative rather than additive in a given brand-market context. Panel datasets with repeated individual-level perception measurement and known signal exposure histories provide the necessary data structure. Netzer, Lattin, and Srinivasan (2008) demonstrate that hidden Markov models estimated on individual-level panel data recover latent state trajectories that are systematically suppressed by cross-sectional models — directly validating the infrastructure needed to test multiplicative regime transitions in brand perception data. Erdem and Keane (1996) provide an earlier existence proof that dynamic brand choice models estimated on individual-level panel data outperform static cross-sectional models precisely because they capture state-dependence and updating dynamics.

---

## Empirical Foundations

This section maps existing empirical evidence to each of the five propositions. The evidence was not generated to test non-ergodicity; it was generated to test narrower hypotheses about order effects, primacy, and path dependence. The non-ergodic framework reveals these disparate findings as manifestations of a single underlying structure.

### 5.1 Evidence for P1 (Signal Order Effect)

**Hogarth and Einhorn (1992).** The belief-adjustment model was tested across 128 experimental conditions varying evidence type, evidence strength, evidence length, and processing mode. The central finding — that the same evidence in different orders produces different final beliefs — directly supports P1. The effect sizes are substantial: in step-by-step processing with mixed evidence, order manipulations produce final belief differences of 10-25% of the scale range. The model's parameters (adjustment weights and reference points) provide quantitative predictions about the magnitude of the order effect as a function of evidence characteristics.

**Smith and Vogt (1995).** In their experimental study of advertising and negative word-of-mouth integration, Smith and Vogt found that the ad-before-WOM sequence produced higher brand perception outcomes than the WOM-before-ad sequence, even though the total information was identical. Moreover, the processing depth differed: subjects in the WOM-first condition engaged in more counterarguing during subsequent ad exposure, while subjects in the ad-first condition showed more straightforward integration. This demonstrates that signal order does not merely shift the endpoint; it alters the processing trajectory — changing not just where observers end up but how they get there.

**Asch (1946).** Asch's impression formation experiments are the earliest systematic demonstration of P1. The "intelligent-industrious-impulsive-critical-stubborn-envious" versus "envious-stubborn-critical-impulsive-industrious-intelligent" manipulation produced dramatically different impressions from identical trait sets. While Asch's experiments concern person perception rather than brand perception, the underlying mechanism — sequential interpretation through an evolving frame — is identical.

### 5.2 Evidence for P2 (Absorbing State Asymmetry)

**Slovic (1993).** Slovic's trust asymmetry principle — that trust is destroyed more easily than it is created — provides the psychological foundation for P2. Slovic showed that a single negative event can undermine years of trust-building, while no single positive event can restore trust that has been fundamentally lost. This asymmetry between destruction and construction is the behavioral manifestation of the absorbing-state property: the boundary at zero trust is approached easily but returned from with great difficulty, if at all.

**Siray (2016).** Siray's formal analysis of path-dependent consumption provides evidence that certain consumption trajectories lead to states from which preferences become locked in. While Siray does not use the language of absorbing states, the mathematical structure is equivalent: certain preference states, once reached through particular consumption sequences, exhibit resistance to reversal that increases with the time spent in the state.

**Brand crisis literature.** Cleeren, Dekimpe, and van Heerde (2017) provide a comprehensive review of brand crisis research demonstrating that recovery is systematically incomplete: brands suffering fundamental trust violations (e.g., Volkswagen's emissions scandal, Boeing's 737 MAX crisis) recover on average perception metrics while exhibiting a persistent cohort of consumers who never return to pre-crisis levels. This pattern is precisely what absorbing-state dynamics predict: some observers are permanently absorbed while others — those whose trajectories remain in the interior — recover. The ensemble average shows partial recovery; many individual trajectories show complete absorption. The observed heterogeneity in recovery outcomes, rather than being unexplained noise, is a direct signature of the asymmetric absorbing-boundary mechanism in P2.

### 5.3 Evidence for P3 (Ensemble-Time Divergence)

Direct evidence for P3 requires longitudinal individual-level tracking data — precisely the data that traditional brand tracking does not collect. However, indirect evidence comes from two sources.

**Panel attrition in brand tracking.** Brand tracking panels experience systematic attrition: respondents who hold strongly negative brand perceptions are less likely to participate in subsequent waves. This attrition is not random; it selectively removes absorbed observers, producing precisely the survivorship bias that P3 predicts. Practitioners are aware of this bias but treat it as a methodological nuisance rather than a structural feature of non-ergodic dynamics.

**NPS distribution bimodality.** Net Promoter Score distributions are frequently bimodal, with clusters at the extremes (promoters and detractors) and fewer respondents in the middle. This distribution is consistent with a non-ergodic process with absorbing boundaries: over time, observers migrate toward extreme states (positive conviction or negative conviction), with the negative extreme functioning as an absorbing state. The cross-sectional NPS average, which nets promoters against detractors, obscures the fundamentally different trajectory types represented by the two groups.

### 5.4 Evidence for P4 (First-Signal Anchoring)

**Kardes and Kalyanaram (1992).** Their demonstration of order-of-entry effects provides the most direct evidence for P4 at the category level. The first brand encountered in a category enjoys a persistent memory and judgment advantage that cannot be fully explained by quality differences, advertising spending, or distribution advantages. The mechanism is anchoring: the first brand fills a perceptual vacuum and establishes the reference point for all subsequent evaluation.

**Tversky and Kahneman (1974).** The anchoring heuristic, while not specific to brand perception, provides the general cognitive mechanism underlying P4. Initial values (anchors) disproportionately influence subsequent judgments, even when the anchor is arbitrary. In the brand context, the first signal in a dimension is not arbitrary — it carries real information — but the anchoring mechanism is the same: the first value encountered serves as the reference point for subsequent updating.

**Asch (1946).** Asch's primacy findings can be reinterpreted as first-signal anchoring within the impression formation process. The first trait adjective establishes the interpretive frame; subsequent adjectives are assimilated to this frame or, if discrepant, are given reduced weight. The mechanism is identical to P4: the first signal in the dimension of personality evaluation anchors all subsequent updates.

### 5.5 Evidence for P5 (Cohort Trajectory Divergence)

**Grier and Brumbaugh (1999).** Their study of target and non-target market perceptions of advertising demonstrates that identical ad stimuli produce different perceptual outcomes depending on the observer's cultural background. African American consumers and White consumers, viewing the same advertisements, extracted different meanings, evaluated different dimensions, and formed different perception outcomes. In SBT terms, these are different observer cohorts with different dimension weights (particularly on the Social, Cultural, and Ideological dimensions) producing divergent perception from identical signals.

**Puntoni, de Langhe, and van Osselaer (2011).** Their research on bilingualism and advertising shows that the same advertising message in a bilingual's first versus second language activates different emotional processing, producing different perceptual outcomes. This is dimension-weight variation at the individual level: the same observer, processing the same content through different linguistic channels, applies different weights to the Narrative and Experiential dimensions.

**McCracken (1986).** McCracken's model of meaning transfer in advertising, while not empirical in the quantitative sense, provides the theoretical framework for understanding why observer heterogeneity produces trajectory divergence: meaning is not in the signal but is constructed by the observer, and different observers construct different meanings from identical signals.

---

Table 1: Summary of Empirical Evidence Mapped to Propositions.

| Proposition | Key Evidence | Finding | SBT Interpretation |
|---|---|---|---|
| P1: Signal Order | Hogarth & Einhorn (1992) | Same evidence, different order → different beliefs | Multiplicative dynamics: signal impact depends on current state |
| P1: Signal Order | Smith & Vogt (1995) | Ad-before-WOM ≠ WOM-before-ad | Cross-dimensional path dependence in processing |
| P1: Signal Order | Asch (1946) | Trait order affects impression | First-encountered traits establish interpretive frame |
| P2: Absorbing State | Slovic (1993) | Trust destruction >> trust creation | Boundary at zero conviction is absorbing |
| P2: Absorbing State | Siray (2016) | Preference lock-in from consumption paths | Path-dependent states resist reversal |
| P3: Ensemble-Time | Panel attrition patterns | Negative observers drop out | Survivorship bias = ensemble-time divergence |
| P4: First Signal | Kardes & Kalyanaram (1992) | Pioneer advantage persists | First entrant fills perceptual vacuum |
| P4: First Signal | Tversky & Kahneman (1974) | Anchoring heuristic | Initial values disproportionately influence updates |
| P5: Cohort Divergence | Grier & Brumbaugh (1999) | Target vs. non-target market | Different dimension weights → different perceptions |
| P5: Cohort Divergence | Puntoni et al. (2011) | Language activates different processing | Observer spectral profiles shape signal reception |

*Notes*: Evidence was not generated to test non-ergodicity directly; findings are reinterpreted through the non-ergodic framework as convergent validation.

---

## Implications for Brand Management

### 6.1 The Tracking Fallacy: Why NPS and Brand Tracking Are Non-Ergodic Artifacts

If brand perception is non-ergodic, then the standard methodology of brand tracking — survey a cross-section, compute averages, compare across time — produces a measurement artifact rather than a measurement of brand health. The artifact has a predictable structure: it overestimates health for brands at risk of absorbing states and underestimates the dispersion of individual trajectories.

Consider Table 2, which illustrates the divergence between ensemble and time averages for a hypothetical brand with absorbing-state risk.

---

Table 2: Ensemble vs. Time Average Divergence (Illustrative).

| Time | Active Observers | Absorbed Observers | Ensemble Average (Active Only) | True Population Average (Including Absorbed) |
|---|---|---|---|---|
| t=0 | 1000 | 0 | 7.0 | 7.0 |
| t=1 | 980 | 20 | 7.1 | 6.8 |
| t=2 | 950 | 50 | 7.2 | 6.5 |
| t=3 | 900 | 100 | 7.4 | 6.0 |
| t=4 | 830 | 170 | 7.5 | 5.3 |
| t=5 | 750 | 250 | 7.6 | 4.5 |

*Notes*: Values are illustrative; generative assumptions (absorption rate, initial perception distribution) are documented in the companion computation script (see Companion Computation Script subsection). Absorption rates are calibrated to a low-coherence brand profile consistent with Zharnikov (2026a) incoherent-type parameters.

---

The ensemble average (what brand tracking reports) increases over time — the brand appears to be strengthening. The true population average (including absorbed observers at zero) decreases — the brand is actually deteriorating. The divergence grows over time, and the direction of the bias is consistently positive: brand tracking tells a more optimistic story than the reality.

This is not a pathological edge case. Any brand with non-zero absorption risk — which is to say, any brand that can suffer a fundamental loss of trust with any fraction of its observer base — exhibits this divergence. The magnitude depends on the absorption rate, which in turn depends on the brand's coherence type. Low-coherence brands with high-variance emission profiles (Tesla, in SBT's analysis) exhibit rapid absorption and large divergence. High-coherence brands with balanced emission profiles (Hermès) exhibit slow absorption and small divergence.

The practical recommendation is not to abandon brand tracking but to supplement it with trajectory-level measurement — tracking individual observers over time (panel studies with careful attention to attrition), measuring the rate of absorption (how many observers cross from negative perception to negative conviction between waves), and correcting ensemble averages for survivorship bias. Sriram, Balachander, and Kalwani (2007) demonstrate that store-level panel data can be used to monitor brand equity dynamics over time, recovering temporal heterogeneity that cross-sectional brand tracking conceals — the kind of individual-trajectory decomposition that the non-ergodic framework requires.

### 6.2 Touchpoint Sequence as Strategic Variable

P1 (Signal Order Effect) implies that the sequence in which consumers encounter brand touchpoints is not a second-order operational detail but a first-order strategic variable. Two consumers who encounter the same set of brand touchpoints in different orders will form structurally different perceptions.

Current brand management practice treats touchpoint sequence as largely uncontrollable — consumers encounter brand signals in whatever order their life circumstances dictate. While this is partially true, two strategic levers are available.

First, **controlled-sequence touchpoints.** In direct-to-consumer channels, retail environments, and digital customer journeys, brands control the sequence of signal presentation. The non-ergodic framework implies that this control is more valuable than commonly appreciated. An e-commerce brand that leads with Experiential signals (product quality, user reviews) before Narrative signals (brand story, founder journey) will produce different perception profiles than one that leads with Narrative — and the difference is not merely aesthetic but structural, affecting absorbing-state proximity and long-run trajectory stability.

Second, **first-signal management.** P4 (First-Signal Anchoring) implies that the highest-leverage touchpoint is the first one. Brands should invest disproportionately in the quality, dimensionality, and valence of the first signal that new observers encounter. The design of customer journey touchpoint sequences is a recognized practice (Lemon & Verhoef, 2016), but the non-ergodic framework adds a specific and previously unrecognized prediction: the same touchpoints, encountered in different orders, will produce permanently divergent perception trajectories — not just different endpoints at time *t*, but structurally different long-run distributions. Existing order-effect models (Hogarth & Einhorn, 1992) predict the direction of sequential bias (primacy versus recency) but not this systematic divergence between what population-level tracking records and what individual trajectories actually experience. The non-ergodic framework specifically predicts that brand tracking scores can improve at the population level while individual perception trajectories decline — because the tracked ensemble is progressively purified by absorption of the most negative observers. Among order-effect models that assume reversible attitude updating, none generates this prediction; the absorbing-state extension here is necessary for it to follow. This is a testable, distinctive implication of the non-ergodic framework.

### 6.3 The First-Signal Premium

The first-signal anchoring effect (P4) creates a structural premium for first signals in each dimension — one that is in principle measurable through longitudinal panel studies that track per-dimension perception from a consumer's first brand encounter (see Limitations and Future Empirical Research). In practical terms, this means:

1. **Category pioneers** have a structural perception advantage that extends beyond first-mover advantages in distribution or awareness. The perceptual anchor set by the first brand in a category is a long-lived asset that competitors must work against, not merely match.

2. **New dimension entry** — the first time a brand signals in a previously inactive dimension — is a high-leverage strategic moment. When Patagonia first entered the Ideological dimension with environmental activism, it set an anchor that has persisted for decades and continues to shape how consumers interpret its signals across all dimensions. Brands entering new dimensions should treat the first signal as a permanent architectural choice, not a tactical communication decision.

3. **Structural absence** (SBT's "dark signal") is particularly dangerous in the context of first-signal anchoring. A dimension where the brand has never signaled is a vacuum waiting to be filled by the first signal encountered — which may come from competitors, media, or word-of-mouth rather than from the brand itself. Managing structural absence by proactively signaling in all eight dimensions is a defensive strategy against uncontrolled first-signal anchoring.

### 6.4 Absorbing States and Brand Crisis Management

P2 (Absorbing State Asymmetry) and P3 (Ensemble-Time Divergence) together reframe brand crisis management. The conventional view treats brand crises as events that damage brand perception — a loss of points on a scale that can be recovered through communication, reform, and time. The non-ergodic framework reveals that crises are potential absorbing-state events: they can push some fraction of observers across the boundary from negative perception to negative conviction, permanently removing them from the brand's accessible audience.

The critical distinction is between recoverable and non-recoverable crisis damage:

**Recoverable damage** moves observers toward the boundary without crossing it. The perception profile shifts, individual dimensions decline, but no dimension reaches zero. Recovery is possible through subsequent positive signals, though the path dependence of the damage means that recovery does not return to the pre-crisis state — it reaches a new state that reflects the crisis as part of the brand's history.

**Non-recoverable damage** pushes observers across the boundary. One or more dimensions reach zero in the observer's perception (e.g., perceived integrity reaches zero). The observer enters an absorbing state. No amount of subsequent positive signaling can restore the absorbed dimension to positive values, because all subsequent signals are processed through the lens of the categorical negative judgment.

The formal derivation of absorption-rate orderings across coherence types — establishing precisely why ecosystem-coherent brands absorb observers at slower rates than incoherent brands under equivalent negative signal shocks — is developed in Zharnikov (2026s), which provides the analytical complement to the qualitative argument here.

Cohort heterogeneity affects crisis trajectories as well. van Heerde, Gijsbrechts, and Pauwels (2004) demonstrate that consumer cohorts differ systematically in their sensitivity to price promotions and competitive actions; the same logic applies to crisis signals, where cohorts with higher Ideological weighting will reach absorbing boundaries faster under integrity-violation crises than cohorts with primarily Experiential weighting. Borah, Banerjee, Lin, Jain, and Eisingerich (2020) show that online brand community engagement patterns predict which consumer groups will amplify versus attenuate negative events — a finding consistent with the cohort-trajectory-divergence mechanism in P5 applied to crisis contexts.

The practical implication is that crisis management should be evaluated not by the average perception score post-crisis (the ensemble average) but by the absorption rate: what fraction of observers crossed from perception to conviction? The absorption rate determines the permanent population loss, while the perception shift determines the recoverable damage. A crisis that produces a large perception shift but low absorption is ultimately less damaging than a crisis that produces a small perception shift but high absorption.

### 6.5 Implications for Consumer-Psychology Research

The non-ergodic framework carries direct implications for how consumer psychology constructs its measurement designs, evaluates its empirical findings, and frames its theoretical contributions.

- **Measurement design.** Experiments that present stimuli in fixed order and report group-level perception outcomes conflate signal-sequence effects with genuine stimulus effects. P1 implies that any between-subjects design with a non-randomized stimulus sequence is susceptible to confounding between the experimental manipulation and the order of encounter. Consumer psychology studies testing order effects, primacy, or belief updating should report sequence-by-condition interaction tests as standard practice, not post-hoc checks. Within-subjects designs are especially vulnerable: the history of prior sessions creates path-dependent priors that standard counterbalancing cannot fully eliminate.

- **Ergodicity-assumption testing.** Most consumer psychology longitudinal studies report wave-level means and test differences with standard repeated-measures models. These models implicitly assume that individual trajectories are exchangeable — an ergodicity assumption. P3 implies that this assumption should be tested explicitly in longitudinal brand perception studies: if absorption rates are non-negligible, panel attrition is non-random, and wave-level means overstate the typical trajectory. Inverse probability weighting or trajectory-disaggregated reporting (distributions, not just means) should be reported alongside conventional means.

- **Longitudinal study design.** The non-ergodic framework identifies three empirically tractable design targets: (a) individual-level time averages (requires continuous or dense repeated measurement per respondent rather than sparse cross-sectional waves); (b) absorption rate measurement (requires instruments that distinguish low perceptions from conviction-level categorical rejection — standard Likert scales may be inadequate); and (c) multi-dimensional trajectory analysis across all eight SBT dimensions (requires moving beyond single-item brand perception measures to multi-dimensional perception instruments). Panels designed with these targets will be positioned to directly test P1–P5 and to extend the non-ergodic framework into domain-specific brand-category comparisons.

---

## Discussion

### 7.1 Relationship to SBT's Formal Dynamic Model

The propositions developed in this paper are conceptual translations of the formal results in Zharnikov (2026j). The relationship is summarized in Table 3.

---

Table 3: Correspondence Between Propositions and Formal Results in Zharnikov (2026j).

| This Paper | Zharnikov (2026j) | Mathematical Object |
|---|---|---|
| P1: Signal Order Effect | Path dependence of SDE solutions | Non-commutativity of stochastic integrals on $S^7_+$ |
| P2: Absorbing State Asymmetry | Theorem 2 (survival probability) | Absorbing boundary at $\partial S^7_+$ with exponential decay |
| P3: Ensemble-Time Divergence | Theorem 4 (non-ergodicity) | $\lim_{T\to\infty} \bar{f}^{(T)} \neq \langle f \rangle^{(E)}$ a.s. |
| P4: First-Signal Anchoring | Drift term dependence on initial condition | $C(x)$ factor in survival probability $S(t,x) \sim C(x) e^{-\lambda t}$ |
| P5: Cohort Trajectory Divergence | Weight-dependent diffusion coefficient | Different $\sigma(w)$ → different trajectory distributions |

*Notes*: Mathematical objects refer to the stochastic differential equation framework on the positive octant of the 7-sphere $S^7_+$ as specified in Zharnikov (2026j). Theorem numbering follows the working-paper version v1.0.

---

The two papers serve complementary audiences. Zharnikov (2026j), with its stochastic differential equations and spectral theory, addresses the mathematical community and provides rigorous foundations. This paper, with its propositions and empirical mappings, addresses consumer psychology and brand management researchers and provides the interpretive framework. Zharnikov (2026z) provides a kinematic complement to the dynamic framework developed here: where this paper characterizes the divergence between time and ensemble averages, Zharnikov (2026z) characterizes the velocity and acceleration of perception trajectories in phase space, enabling a more fine-grained description of how quickly observers approach absorbing boundaries. The two frameworks together suggest that the full empirical agenda requires both trajectory-level statistics (this paper) and phase-space measurement (Zharnikov 2026z).

### 7.2 Relationship to Classical Brand Theory

The non-ergodic framework does not invalidate Aaker (1991), Keller (1993), or Kapferer (2008, 4th ed.). It identifies the implicit assumption under which their frameworks are valid and specifies when that assumption fails.

**Aaker's brand equity model.** Aaker's (1991) five components of brand equity (awareness, associations, perceived quality, loyalty, proprietary assets) are cross-sectional constructs measured through ensemble averages. The non-ergodic framework reveals that these measurements are valid descriptions of brand health to the extent that perception dynamics are approximately ergodic — that is, when the brand has low absorption risk, low signal variance, and a homogeneous observer base. For high-coherence brands with stable emission profiles, Aaker's framework provides a reasonable approximation. For low-coherence brands with volatile emission profiles, it systematically misrepresents brand health through survivorship bias.

**Keller's CBBE model.** Keller's (1993) Customer-Based Brand Equity model describes a building-block hierarchy from salience to resonance. The non-ergodic framework adds a dynamic dimension: the path through the hierarchy matters, not just the endpoints. An observer who builds from Experiential salience (product trial) to Narrative resonance (brand story appreciation) develops a different perceptual structure than one who builds from Narrative salience to Experiential resonance, even if both reach the same "level" in Keller's hierarchy. Keller's model describes the static architecture; the non-ergodic framework describes the path dependence of construction.

**Kapferer's brand identity prism.** Kapferer's (2008, 4th ed.) identity prism distinguishes sender-constructed and receiver-constructed facets of brand identity. The non-ergodic framework operationalizes the receiver construction process: different receivers (observer cohorts) with different dimension weights construct different identities from the same sender emissions, and the construction process is path-dependent. Kapferer's insight that brand identity is co-created between sender and receiver is formalized in the non-ergodic framework as the interaction between emission profile (sender) and observer spectral profile (receiver) in a path-dependent dynamic process.

The relationship between the non-ergodic framework and classical brand theory is analogous to the relationship Peters (2019) identifies between ergodicity economics and classical expected utility theory: the classical framework is an implicit ergodicity assumption that works well in certain regimes (high coherence, low absorption, homogeneous observers) and fails systematically in others.

### 7.3 Connection to Process Invariance and Dynamic Admissibility

The non-ergodic framework developed in this paper connects to a complementary construct from systems-governance theory: process invariance under temporal stress. Medesani and Macdonald (2026), in a control-theoretic study of bounded contraction operators in microgrid systems, formalize the distinction between *state invariance* (preservation at a snapshot) and *process invariance* (preservation along trajectories under perturbation), holding that "integrity is preserved by constraining evolution under stress, not the instantaneous state." Their formulation, though developed for engineered systems, is the systems-theoretic counterpart of the present paper's central thesis: trajectories, not snapshots, carry the diagnostic information. Extending Medesani and Macdonald's process-invariance condition to brand perception, a brand that satisfies instantaneous coherence (all dimensions within acceptable ranges at $t$) but exhibits absorbing-state trajectories (one or more dimensions drifting toward the boundary over time) satisfies process invariance in the static sense while failing it dynamically. This trajectory-level admissibility provides the per-cohort diagnostic complement to the non-ergodic framework's population-level bias prediction: where P3 predicts that ensemble averages overestimate health for absorbing-state brands, the process-invariance condition specifies the per-observer-cohort condition under which that overestimation is most severe — namely, when the cohort's evolution path violates invariance under the signal perturbations that characterize real market conditions. Together, the two frameworks suggest that longitudinal brand health measurement should assess both the trajectory distribution across the population (non-ergodicity correction) and the admissibility of individual cohort trajectories under perturbation.

### 7.4 Limitations and Future Empirical Research

The framework developed in this paper is scoped to consumer brand perception (B2C contexts). Extension to B2B brand perception requires additional analysis: in B2B settings, purchasing decisions typically involve committees, formal evaluation processes, and contractual relationships that may introduce ergodicity-restoring mechanisms — competitive bidding forces perceptual convergence, contractual terms create defined reset points, and formal review cycles impose structured reconsideration that can disrupt absorbing states. Whether the three sources of non-ergodicity (absorbing conviction, nonlinear dynamics, path-dependent weighting) operate with the same force in B2B perception is an open empirical question and a productive direction for future research.

A geometric formalization of the non-ergodic divergence mechanism is suggested by recent work in differential geometry. Bobenko, Hoffmann, and Sageman-Furnas (2025) prove that two surfaces can share the same metric and the same mean curvature yet be genuinely non-congruent — the Bonnet pair phenomenon. The brand perception analog is direct: two observers who arrive at identical spectral profiles via different non-ergodic trajectories are Bonnet pairs — metrically equivalent but experientially distinct. The observer's trajectory through perception space is the "second fundamental form" that resolves the ambiguity: the metric (spectral profile) is necessary but not sufficient for brand identification in regimes where path dependence is strong. This connects the present paper's dynamic framework to the static measurement framework of brand triangulation (Zharnikov, 2026y), which recovers the metric but requires trajectory information to resolve Bonnet-type ambiguity. The kinematic characterization of those trajectories — their velocity, acceleration, and phase-space geometry — is the subject of Zharnikov (2026z), which provides the measurement complement needed to operationalize Bonnet-pair disambiguation empirically.

A further limitation of this paper is that its propositions are derived theoretically and supported by existing evidence that was generated for other purposes. While the evidence is consistent with non-ergodic dynamics, it was not designed to test non-ergodicity directly. Direct tests would require:

1. **Longitudinal individual-level tracking.** Following individual observers' brand perceptions over multiple time periods, with controlled signal exposure, to measure time averages and compare them to ensemble averages.

2. **Absorption rate measurement.** Tracking the rate at which observers cross from negative perception to negative conviction, and measuring the probability of return.

3. **Multi-dimensional trajectory analysis.** Measuring perception on all eight SBT dimensions over time, for multiple cohorts, to test P5 (Cohort Trajectory Divergence) directly.

4. **Experimental manipulation of signal sequence.** Presenting identical brand signals in different orders to matched groups and measuring the resulting perception profiles.

A second limitation is the reliance on the SBT framework for the multi-dimensional structure. While the propositions about non-ergodicity do not depend on the specific number or identity of dimensions (they would hold in any multi-dimensional perception space with the three sources of non-ergodicity), the connection to specific managerial recommendations (e.g., managing structural absence across eight dimensions) does depend on the SBT dimensionality. The empirical validation of SBT's eight-dimensional structure (Zharnikov, 2026a) is an ongoing research program; the non-ergodic framework developed here will be strengthened as that validation progresses.

A further limitation concerns the multiplicative assumption that underlies all five propositions. The sufficiency conditions (C1-C3) specify when perception dynamics are multiplicative rather than additive, and proposes that log-linear versus linear model fit on longitudinal panel data is the primary empirical test. Testing this assumption at scale — across brands, categories, and observer cohorts — is a priority for future empirical work, since the degree to which any given brand-market context departs from the multiplicative regime determines how severely the propositions apply.

A third limitation is the difficulty of measuring absorbing states empirically. Negative conviction — the categorical judgment that a brand is fundamentally flawed — is not simply a low score on a standard perception scale. It requires measurement instruments that distinguish between degrees of negative perception (recoverable) and categorical negative conviction (absorbing). Developing such instruments is a prerequisite for testing P2 and P3 directly.

---

## Conclusion

Brand perception is non-ergodic. The time average of an individual consumer's brand perception does not converge to the cross-sectional average across consumers. This claim, formalized through five propositions and grounded in Peters' (2019) ergodicity framework, provides a unified interpretive lens for 80 years of empirical findings — from Asch's (1946) primacy effects to Hogarth and Einhorn's (1992) belief-adjustment model to contemporary path-dependence research — connecting them within a single theoretical explanation.

The implications are both theoretical and practical. Theoretically, the non-ergodic framework reveals that classical brand theory (Aaker, 1991; Keller, 1993; Kapferer, 2008, 4th ed.) operates under an implicit ergodicity assumption that is valid for high-coherence brands with stable emission profiles and fails for low-coherence brands with volatile profiles.

Practically, the framework identifies three high-leverage interventions. First, brand tracking should be supplemented with individual-level trajectory measurement and corrected for survivorship bias — the divergence between what tracking reports and what consumers actually experience. Second, touchpoint sequence should be managed as a strategic variable, not treated as uncontrollable noise, with particular attention to first signals in each perceptual dimension. Third, crisis management should shift from evaluating average perception recovery (ensemble measure) to measuring absorption rate (the fraction of observers who crossed from perception to conviction), because absorption is permanent while perception shifts are recoverable.

The paper connects to Spectral Brand Theory's broader research program (Zharnikov, 2026a, 2026d, 2026j) by providing the interpretive bridge between the formal mathematics of non-ergodic perception dynamics (Zharnikov, 2026j) and the empirical and managerial implications. Non-ergodicity is not a mathematical curiosity; it is the reason why brand management requires trajectory-level thinking — what SBT calls vectorized rather than rasterized brand management — and why the distinction between these two modes is not a preference but a structural necessity.

The touchpoint sequence is not noise. It is signal.

---

## Acknowledgments

AI assistants (Claude Opus 4.7, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

---

## Companion Computation Script

The illustrative values in Table 2 (absorption trajectory over six time periods) are generated by a simulation script published at `https://github.com/spectralbranding/sbt-papers/tree/main/r9-nonergodic-perception/code/`. The script uses a discrete-time absorbing Markov chain with parameters: initial perception = 7.0 (scale 0–10), absorption threshold = 0 (any dimension reaching 0), absorption probability per period = .020 (calibrated to a low-coherence brand profile from Zharnikov 2026a incoherent-type parameters), random seed = 42. Run command: `python simulate_absorption.py --seed 42 --periods 6`. The script reproduces Table 2 exactly.

---

## References

Aaker, D. A. (1991). *Managing brand equity: Capitalizing on the value of a brand name*. Free Press.

Anderson, N. H. (1981). *Foundations of information integration theory*. Academic Press.

Asch, S. E. (1946). Forming impressions of personality. *Journal of Abnormal and Social Psychology*, *41*(3), 258–290.

Baumeister, R. F., Bratslavsky, E., Finkenauer, C., & Vohs, K. D. (2001). Bad is stronger than good. *Review of General Psychology*, *5*(4), 323–370.

Birkhoff, G. D. (1931). Proof of the ergodic theorem. *Proceedings of the National Academy of Sciences*, *17*(12), 656–660.

Bobenko, A. I., Hoffmann, T., & Sageman-Furnas, A. O. (2025). Compact Bonnet pairs: Isometric tori with the same curvatures. *Publications Mathematiques de l'IHES*, *142*, 241–293. https://doi.org/10.1007/s10240-025-00159-z

Borah, A., Banerjee, S., Lin, Y.-T., Jain, A., & Eisingerich, A. B. (2020). Improvised marketing interventions in social media. *Journal of Marketing*, *84*(2), 69–91.

Busemeyer, J. R., & Townsend, J. T. (1993). Decision field theory: A dynamic-cognitive approach to decision making in an uncertain environment. *Psychological Review*, *100*(3), 432–459.

Cleeren, K., Dekimpe, M. G., & van Heerde, H. J. (2017). Marketing research on brand crises. *Journal of the Academy of Marketing Science*, *45*(6), 771–788.

Doctor, J. N., Wakker, P. P., & Wang, T. V. (2020). Economists' views on the ergodicity problem. *Nature Physics*, *16*(12), 1168–1169.

Dzyabura, D., & Hauser, J. R. (2019). Recommending products when consumers learn their preference weights. *Marketing Science*, *38*(3), 417–441.

Erdem, T., & Keane, M. P. (1996). Decision-making under uncertainty: Capturing dynamic brand choice processes in turbulent consumer goods markets. *Marketing Science*, *15*(1), 1–20.

Grier, S. A., & Brumbaugh, A. M. (1999). Noticing cultural differences: Ad meanings created by target and non-target markets. *Journal of Advertising*, *28*(1), 79–93.

Hogarth, R. M., & Einhorn, H. J. (1992). Order effects in belief updating: The belief-adjustment model. *Cognitive Psychology*, *24*(1), 1–55.

Kapferer, J.-N. (2008). *The new strategic brand management: Creating and sustaining brand equity long term* (4th ed.). Kogan Page.

Kardes, F. R., & Kalyanaram, G. (1992). Order-of-entry effects on consumer memory and judgment: An information integration perspective. *Journal of Marketing Research*, *29*(3), 343–357.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, *57*(1), 1–22.

Kemeny, J. G., & Snell, J. L. (1960). *Finite Markov chains*. Van Nostrand.

Kruschke, J. K. (2008). Bayesian approaches to associative learning: From passive to active learning. *Learning & Behavior*, *36*(3), 210–226.

Lemon, K. N., & Verhoef, P. C. (2016). Understanding customer experience throughout the customer journey. *Journal of Marketing*, *80*(6), 69–96.

McCracken, G. (1986). Culture and consumption: A theoretical account of the structure and movement of the cultural meaning of consumer goods. *Journal of Consumer Research*, *13*(1), 71–84.

Medesani, M., & Macdonald, J. (2026). Geometric foundations of invariant corridors and governance: A unified framework with empirical validation (Level 3.3). *Working Paper*. https://doi.org/10.5281/zenodo.18822552

Netzer, O., Lattin, J. M., & Srinivasan, V. (2008). A hidden Markov model of customer relationship dynamics. *Marketing Science*, *27*(2), 185–204.

Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, *15*(12), 1216–1221.

Peters, O., & Gell-Mann, M. (2016). Evaluating gambles using dynamics. *Chaos*, *26*(2), 023103.

Puntoni, S., de Langhe, B., & van Osselaer, S. M. J. (2011). Bilingualism and the emotional intensity of advertising language. *Journal of Consumer Research*, *38*(5), 1001–1025.

Siray, S. (2016). *Path-dependent consumption* (Doctoral dissertation). Freie Universitat Berlin.

Slovic, P. (1993). Perceived risk, trust, and democracy. *Risk Analysis*, *13*(6), 675–682.

Smith, R. E., & Vogt, C. A. (1995). The effects of integrating advertising and negative word-of-mouth communications on message processing and response. *Journal of Consumer Psychology*, *4*(2), 133–151.

Sriram, S., Balachander, S., & Kalwani, M. U. (2007). Monitoring the dynamics of brand equity using store-level data. *Journal of Marketing*, *71*(2), 61–78.

Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, *185*(4157), 1124–1131.

van Heerde, H. J., Gijsbrechts, E., & Pauwels, K. (2004). Fanning the flames? How media coverage of a price war affects retailers, consumers, and investors. *Journal of Marketing Research*, *41*(4), 393–409.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026d). Brand space geometry: A formal metric for multi-dimensional brand perception. Working Paper. https://doi.org/10.5281/zenodo.18945295

Zharnikov, D. (2026j). Non-ergodic brand perception: Diffusion dynamics on multi-dimensional perceptual manifolds. Working Paper. https://doi.org/10.5281/zenodo.18945659

Zharnikov, D. (2026s). Coherence type as crisis predictor: A formal derivation from non-ergodic dynamics. Working Paper. https://doi.org/10.5281/zenodo.19208107

Zharnikov, D. (2026v). Dimensional collapse in AI-mediated brand perception: Large language models as metameric observers. Working Paper. https://doi.org/10.5281/zenodo.19422427

Zharnikov, D. (2026y). Brand triangulation: A geometric framework for multi-observer brand positioning. Working Paper. https://doi.org/10.5281/zenodo.19482547

Zharnikov, D. (2026z). Spectral dynamics: Velocity, acceleration, and phase space in multi-dimensional brand perception. Working Paper. https://doi.org/10.5281/zenodo.19468204
