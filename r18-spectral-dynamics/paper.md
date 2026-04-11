# Spectral Dynamics: Velocity, Acceleration, and Phase Space in Multi-Dimensional Brand Perception

**Dmitry Zharnikov**

Working Paper | Citation key: 2026z | https://doi.org/10.5281/zenodo.19468204

---

## Abstract

Brand measurement frameworks capture where a brand is positioned but not where it is going. This paper introduces a differential calculus for multi-dimensional brand perception, extending Spectral Brand Theory's eight-dimensional measurement space from static profiles (Order 0) to velocity vectors (Order 1) and acceleration vectors (Order 2). We formalize brand velocity as the first time derivative of the spectral profile, brand acceleration as the second derivative, and define a 16-dimensional phase space combining position and velocity. Three theoretical contributions emerge. First, we show that velocity resolves metric ambiguity: brands with identical spectral profiles but different velocities are distinguishable in phase space, providing a constructive resolution to a problem structurally analogous to the Bonnet pair problem in differential geometry. Second, we introduce a directional coherence metric that quantifies alignment between a brand's actual trajectory and its strategic intent -- a formal measure of whether brand-building efforts are producing movement in intended directions. Third, we develop trajectory clustering, which segments brands by their dynamic behavior rather than static position, enabling detection of competitive convergence and divergence before they manifest in position. We illustrate the framework using Dove's 20-year brand evolution, computing velocity and acceleration vectors across four strategic periods. The framework connects state-space models in marketing science to the geometric structure of brand perception space, embedding existing Kalman filter approaches within a unified kinematic theory.

**Keywords**: brand dynamics, brand velocity, phase space, trajectory clustering, spectral brand theory, differential calculus, non-ergodic perception, Kalman filter

---

## 1. Introduction

Brand managers track brand position obsessively but brand trajectory almost never. Quarterly tracking studies report where a brand sits on various dimensions -- awareness, consideration, preference, equity -- and whether these scores went "up" or "down" since the last wave. The conceptual toolkit stops at directional arrows: trending up, trending down, stable. There is no formal framework for asking how *fast* a brand is moving, whether that movement is *accelerating* or *decelerating*, whether the brand's *direction* of movement is aligned with strategic intent, or whether two brands currently at different positions are on *converging trajectories* that will bring them into direct competition.

This gap persists despite the maturity of dynamic methods in marketing science. State-space models with Kalman filtering have been applied to brand goodwill (Naik & Raman, 2003), brand preference evolution (Sriram, Chintagunta, & Neelamegham, 2006), and advertising dynamics (Bruce, 2008). System dynamics models track stocks and flows of brand-related variables (Sterman, 2000). Trajectory modeling methods -- group-based trajectory models (Nagin, 1999, 2005), latent growth mixture models (Muthen & Shedden, 1999), functional data analysis (Ramsay & Silverman, 2005) -- are well-established in the social sciences. Yet, to the best of our knowledge, none of these methods has been applied to a *multi-dimensional brand position vector* with formal kinematic quantities (velocity, acceleration, phase space) as the primary analytical objects.

We address this gap by developing a differential calculus for brand perception within Spectral Brand Theory (SBT; Zharnikov, 2026a). SBT represents brands as profiles in an eight-dimensional perception space -- Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal -- where different observer cohorts weight these dimensions differently according to their spectral weight profiles (Zharnikov, 2026d). The framework has formalized the geometry of this space (Zharnikov, 2026d), the information loss from dimensional projection (Zharnikov, 2026e), the stochastic dynamics of perception evolution (Zharnikov, 2026j), the non-ergodicity of individual trajectories (Zharnikov, 2026o), and the multi-observer measurement problem via Brand Triangulation (Zharnikov, 2026y). What is missing is a measurement framework that bridges the theoretical dynamics (stochastic differential equations on manifolds) and practical tracking (how fast is the brand moving, and where is it heading?).

This paper makes three contributions:

1. **Brand kinematics.** We formalize brand velocity **v**(t) = d**x**/dt and acceleration **a**(t) = d**v**/dt as vector quantities in R^8, derive their discrete-time estimators, characterize noise amplification under differentiation, and connect them to the Kalman filter formulation already present in Brand Triangulation (Zharnikov, 2026y, Proposition 6).

2. **Velocity resolves metric ambiguity.** The Bonnet pair problem in differential geometry -- two surfaces with identical metrics but different shapes (Bobenko, Hoffmann, & Sageman-Furnas, 2025) -- has an analog in brand measurement: two brands with identical spectral profiles may be perceived differently if they arrived at those profiles via different trajectories. We prove that the phase space representation (**x**, **v**) resolves this ambiguity under mild regularity conditions, providing a constructive resolution to a theoretical boundary identified in Brand Triangulation.

3. **Trajectory-based competitive analysis.** We introduce directional coherence (the cosine similarity between velocity and strategy vectors) and trajectory clustering (segmenting brands by dynamic state rather than static position), enabling detection of competitive convergence and strategy-trajectory misalignment.

We illustrate the framework using Dove's brand evolution across four periods (2003--2023), computing velocity and acceleration from the dimensional activation data in Zharnikov (2026p). The illustration demonstrates both the framework's analytical power and its limitations (noise amplification, dimensional creation events, author-assigned profiles).

The paper is organized as follows. Section 2 reviews the theoretical background. Section 3 develops the differential calculus. Section 4 proves the Bonnet pair resolution. Section 5 introduces trajectory-based analysis. Section 6 provides the Dove illustration. Section 7 discusses managerial implications. Section 8 addresses limitations and future research. Section 9 concludes.

---

## 2. Theoretical Background

### 2.1 SBT Measurement Framework

Spectral Brand Theory (Zharnikov, 2026a) represents a brand's perceptual signature as a profile **x** in R^8_+, where the eight coordinates correspond to Semiotic (visual identity, logos, design language), Narrative (brand stories, origin myths, messaging), Ideological (values, purpose, ethical commitments), Experiential (product experience, service quality, sensory engagement), Social (community, tribe membership, social signaling), Economic (price positioning, value-for-money, accessibility), Cultural (cultural embeddedness, local adaptation, heritage resonance), and Temporal (longevity, tradition, perceived permanence).

Each observer cohort k possesses a spectral weight profile **w**_k on the probability simplex Delta^7 that determines which dimensions dominate their perception. The observation model is y_k = **w**_k^T **x** + b_k + epsilon_k, where b_k captures systematic bias and epsilon_k is observation noise (Zharnikov, 2026y, Section 3.1). The geometry of the observer weight space is equipped with the Fisher-Rao metric (Zharnikov, 2026d), and the warped product structure of the combined brand-observer space provides the Riemannian framework for perception geometry.

### 2.2 Non-Ergodic Perception Dynamics

Brand perception evolves stochastically on the positive orthant of the unit sphere S^7_+ (Zharnikov, 2026j). The Ito-form stochastic differential equation governing this evolution is:

d**X**_t = [-(7/2)sigma_0^2 **X**_t - kappa P_{**X**_t}(**X**_t - **x***) + alpha lambda_{enc} P_{**X**_t}(**s**/||**s**|| - **X**_t)] dt + sigma_0 P_{**X**_t} d**W**_t

where **x*** is the neutral prior, **s** is the brand's emission signal, kappa is the decay rate, alpha is signal strength, lambda_{enc} is encounter frequency, sigma_0 is diffusion intensity, and P_{**X**_t} projects onto the tangent space at **X**_t (Zharnikov, 2026j, Section 4.5).

The drift term mu(**X**_t, t) in this SDE is the *expected velocity* -- the instantaneous expected rate of change of the perception state. This is the theoretical foundation for the velocity concept we formalize below: velocity is not an add-on to the SBT framework but is already implicit in the dynamical model. What has been missing is the measurement framework that makes this implicit quantity explicit and practically computable.

Critically, brand perception is non-ergodic: the long-run time average for any individual observer does not converge to the cross-sectional ensemble average (Zharnikov, 2026o, Proposition 3; Zharnikov, 2026j, Theorem 4). This non-ergodicity arises from absorbing states (irreversible negative conviction), multiplicative dynamics (signal magnitude depends on current state), and path-dependent dimension weighting (Zharnikov, 2026o, Conditions C1--C3). The practical consequence is that cross-sectional brand tracking -- measuring a population of observers at one time point -- systematically misrepresents individual trajectories. Dynamic measurement requires tracking *trajectories*, not *snapshots*.

### 2.3 Brand Triangulation and the Kalman Filter

Brand Triangulation (Zharnikov, 2026y) addresses the multi-observer measurement problem: given observations from N cohorts with different spectral weight profiles, recover the brand's true emission profile **x**. The framework introduces Perception DOP (Dilution of Precision), which quantifies how observer geometry affects estimation quality:

PDOP = sqrt(trace((W^T W)^{-1}))

where W is the N x 8 matrix of stacked observer weight profiles.

For temporal tracking, Brand Triangulation introduces a Perception Kalman filter with the state vector (**x**, **v**), where **x** is the brand's spectral profile and **v** is its perception velocity (Zharnikov, 2026y, Proposition 6). The prediction step is **x**_{t+1|t} = **x**_t + **v**_t * Delta_t. The Kalman filter treats velocity instrumentally -- as a component of the state that improves temporal prediction. The present paper treats velocity *conceptually* -- as a first-class theoretical quantity with independent meaning, derived quantities, and diagnostic power.

### 2.4 State-Space Models in Marketing Science

State-space models have a productive history in marketing. Naik and Raman (2003) model "brand goodwill" as a latent state evolving under advertising inputs, using Kalman filtering to estimate the unobserved state from sales data. Their state variable captures a perception-like quantity (goodwill) but is scalar, not multi-dimensional. Bruce (2008) extends this to nonlinear dynamics via particle filters, tracking advertising theme quality and carryover effects. These models demonstrate the feasibility and value of latent-state estimation for brand-related dynamics.

However, none of these models operates in a multi-dimensional brand perception space. The state variables are scalar (goodwill, awareness, preference) or low-dimensional (brand vs. category effects). None defines velocity or acceleration as formal vector quantities in R^n. None introduces phase space or trajectory clustering. The present paper bridges this gap by embedding the state-space approach within SBT's eight-dimensional perception geometry.

### 2.5 Dynamical Systems in Strategic Management

The strategic management literature uses dynamical systems language extensively but almost exclusively metaphorically. Bourgeois and Eisenhardt (1988) define "high velocity environments" as those with rapid, discontinuous change in demand, competitors, and technology -- but "velocity" here is an informal descriptor, not a computed derivative. D'Aveni (1994) discusses "hypercompetition" with terms like "escalation" and "acceleration" but provides no mathematical formalization. Dooley and Van de Ven (1999) come closest to formal dynamical systems analysis, defining periodic, chaotic, and noise patterns in organizational change time series, though without applying kinematic quantities to strategic positioning.

The gap is clear: dynamics as metaphor is pervasive; dynamics as measurement is absent. This paper provides the measurement framework.

---

## 3. The Differential Calculus of Brand Perception

### 3.1 Position, Velocity, and Acceleration

**Definition 1 (Brand Position).** The spectral profile of a brand at time t is a vector **x**(t) = [x_1(t), ..., x_8(t)] in R^8_+, where each component x_d(t) represents the brand's emission intensity on dimension d at time t.

**Definition 2 (Brand Velocity).** The brand velocity is the first time derivative of the spectral profile:

**v**(t) = d**x**/dt = [dx_1/dt, ..., dx_8/dt]

The velocity vector **v**(t) is an element of R^8. Its d-th component v_d(t) = dx_d/dt represents the rate of change of perception on dimension d. Positive v_d indicates increasing perception; negative v_d indicates decline. The velocity vector encodes both direction (which dimensions are changing) and magnitude (how fast).

**Definition 3 (Brand Acceleration).** The brand acceleration is the second time derivative:

**a**(t) = d**v**/dt = d^2**x**/dt^2

The acceleration captures whether brand movement is intensifying (|**v**| increasing), stabilizing (|**v**| decreasing toward zero), or reversing (sign change in velocity components).

**Remark (Smoothness and the SDE).** The SDE of Zharnikov (2026j) produces sample paths that are continuous but almost surely nowhere differentiable -- a standard property of diffusion processes. The velocity defined here is therefore not the pathwise derivative (which does not exist) but the *expected rate of change conditioned on the current state*: **v**(t) = E[d**X**/dt | **X**_t] = mu(**X**_t, t), i.e., the drift function of the SDE. In practice, velocity is estimated from discrete-time measurements via finite differences or Kalman filtering (Section 3.7), both of which produce smooth estimates of the underlying drift. This is standard in all applications of state-space models to noisy processes: the estimated velocity is the posterior mean of the drift, not a pathwise derivative. All definitions, propositions, and theorems in this paper should be understood in this sense: "velocity" denotes the estimated drift, not a classical derivative of a non-differentiable sample path.

**Remark (Lossy projection of the dynamics).** The position $\mathbf{x}(t)$, velocity $\mathbf{v}(t)$, and acceleration $\mathbf{a}(t)$ are defined in the full 8-dimensional perception space $\mathbb{R}^8$. Any individual observer measurement, however, is a lossy projection of this state onto a lower-dimensional observable subspace determined by that observer's spectral weight vector. Reconstructing the full trajectory from observer-side measurements is therefore a source-coding problem with side information (Cover & Thomas, 2006): the rate of distortion depends on the observer's effective channel capacity and on the geometric diversity of the observer constellation, in the sense formalized by R17 (Zharnikov, 2026y). Velocities and accelerations recovered from a low-rank observer constellation are subject to the same rate-distortion bounds as the position estimates from which they are derived. We use this framing only to situate the differential calculus in standard information-theoretic terms; no estimator in this paper depends on it.

### 3.2 Discrete-Time Estimation

Brand perception is measured at discrete time points t_1, t_2, ..., t_M. The continuous derivatives must be approximated from finite differences.

**First-order (velocity) estimator.** Given measurements at t_i and t_{i+1}:

**v**_hat(t_{i+1/2}) = (**x**(t_{i+1}) - **x**(t_i)) / (t_{i+1} - t_i)

This is a centered difference estimator, attributed to the midpoint t_{i+1/2} = (t_i + t_{i+1})/2.

**Second-order (acceleration) estimator.** Given three measurements at t_i, t_{i+1}, t_{i+2}:

**a**_hat(t_{i+1}) = (**v**_hat(t_{(i+1)+(i+2)}/2) - **v**_hat(t_{i+(i+1)}/2)) / (t_{mid,2} - t_{mid,1})

where t_{mid,k} is the midpoint of the k-th velocity interval. This is a second-order central difference.

The Kalman filter (Kalman, 1960; Zharnikov, 2026y, Section 8.3) provides an optimal alternative when the system dynamics are approximately linear-Gaussian: the Kalman smoother simultaneously estimates position and velocity from a sequence of noisy observations, with the Kalman gain automatically balancing prediction (model) and correction (data). For non-linear dynamics, particle filters (Bruce, 2008) extend this estimation.

### 3.3 Noise Amplification Under Differentiation

Differentiation amplifies measurement noise. If position measurements have additive noise with standard deviation sigma_x, then:

- Velocity estimates have noise standard deviation sigma_v = sigma_x * sqrt(2) / Delta_t
- Acceleration estimates have noise standard deviation sigma_a = sigma_x * sqrt(6) / Delta_t^2

where Delta_t is the measurement interval. For short intervals, noise dominates signal. For long intervals, the derivative approximation degrades (dynamics may be nonlinear within the interval).

**Proposition 1 (Optimal measurement interval).** The mean squared error of the velocity estimator is minimized when Delta_t* balances truncation error (proportional to Delta_t^2 for smooth dynamics) against noise amplification (proportional to 1/Delta_t^2):

MSE(**v**_hat) = O(Delta_t^4) + O(sigma_x^2 / Delta_t^2)

The optimal interval satisfies Delta_t* ~ (sigma_x)^{1/3} / f''^{1/3}, where f'' characterizes the curvature of the true trajectory. For brand perception with typical noise levels (sigma_x ~ 0.3 on a 10-point scale) and moderate dynamics (annual change ~ 0.5 points), the optimal measurement interval is approximately 6--12 months -- consistent with standard brand tracking cadence.

*Proof sketch.* The truncation error of the first-order difference estimator for a twice-differentiable function is O(Delta_t^2 * max|f''|). The noise variance is sigma_x^2 * 2 / Delta_t^2. Setting d(MSE)/d(Delta_t) = 0 and solving yields the stated result.

**Practical implication.** Velocity estimation is robust with quarterly or semi-annual measurement. Acceleration estimation, requiring at least three time points and suffering O(1/Delta_t^4) noise amplification, requires either longer observation windows or explicit smoothing (Kalman filter). Third-order derivatives (jerk) are impractical with current brand tracking data frequencies.

### 3.4 Brand Speed and Derived Scalar Quantities

**Definition 4 (Brand Speed).** The brand speed is the scalar magnitude of the velocity vector:

s(t) = ||**v**(t)|| = sqrt(sum_d v_d(t)^2)

Brand speed measures how fast the brand's perception is changing, irrespective of direction. High speed indicates a brand in transition (deliberate repositioning, crisis response, campaign launch). Low speed indicates equilibrium (established position, stable market). Moderate speed with no strategic driver suggests drift -- unintended movement requiring investigation.

**Definition 5 (Directional Coherence).** Given a brand's velocity vector **v** and a strategy direction vector **d** (the intended direction of brand movement, defined by the brand manager), the directional coherence is:

DC(**v**, **d**) = (**v** . **d**) / (||**v**|| * ||**d**||) = cos(theta)

where theta is the angle between velocity and strategy direction in R^8.

Directional coherence ranges from -1 to +1:

- DC ~ +1: The brand is moving in its intended direction. Strategy is producing aligned perception change.
- DC ~ 0: The brand is moving, but orthogonally to intent. Marketing expenditure is generating *activity* (non-zero speed) but not *progress* (zero alignment with strategy).
- DC ~ -1: The brand is moving opposite to intent. Marketing is counterproductive -- a situation more common than typically acknowledged, especially during purpose campaigns that trigger backlash on unintended dimensions.

**Remark.** The strategy direction vector **d** must be defined by the brand manager *a priori*, representing the target direction of brand change -- e.g., "increase Ideological and Social while maintaining Economic" would be **d** = [0, 0, 1, 0, 1, 0, 0, 0] (unnormalized). This externality is a feature: directional coherence measures *alignment between action and intention*, which requires both to be specified independently.

### 3.5 Phase Space Representation

**Definition 6 (Brand Phase Space).** The phase space of brand perception is the 16-dimensional space P = R^8 x R^8, where each brand at time t occupies a point (**x**(t), **v**(t)) combining its spectral profile (position) and its velocity.

The phase space representation doubles the dimensionality of brand description from 8 to 16. This is not redundant: two brands occupying the same position **x** but with different velocities **v** are in fundamentally different states. One may be accelerating toward that position (approaching equilibrium); the other may be decelerating through it (about to reverse). Static measurement cannot distinguish them; phase space measurement can.

**Proposition 2 (Phase space trajectory uniqueness).** Under the SDE dynamics of Zharnikov (2026j), conditioned on the same realization of the driving Brownian motion, phase space trajectories (**x**(t), **v**(t)) are unique: two brands starting from distinct phase space points (**x**_0, **v**_0) != (**x**'_0, **v**'_0) remain distinct for all t > 0 with probability 1.

*Proof sketch.* Follows from the Lipschitz continuity of the drift and diffusion coefficients in the SBT SDE, which guarantees pathwise uniqueness of solutions (Zharnikov, 2026j, Theorem 1). Since position uniquely determines velocity via the trajectory, distinct initial conditions in phase space produce distinct trajectories.

This uniqueness means that the phase space description is *complete* in a way that position alone is not: if you know both where a brand is and how fast it is moving on each dimension, you can (in principle) predict its short-term future trajectory. Position alone permits no such prediction.

### 3.6 Dimensional Acceleration Profile

For each dimension d, the pair (v_d, a_d) defines a point in the two-dimensional *dimensional phase plane*. Plotting this pair across time reveals the dynamic regime of each dimension:

- **Stable attractor** (v_d ~ 0, a_d restoring): Small perturbations from equilibrium decay. The dimension returns to its resting value. Most dimensions for established brands in stable markets.
- **Growth regime** (v_d > 0, a_d > 0): Dimension increasing and accelerating. Reinforcing dynamics -- a campaign gaining momentum, a viral effect compounding.
- **Saturation** (v_d > 0, a_d < 0): Dimension still increasing but decelerating. Approaching a ceiling. Campaign fatigue, market saturation, diminishing returns.
- **Decline** (v_d < 0, a_d < 0): Dimension decreasing and decline accelerating. Crisis trajectory. Requires intervention.
- **Recovery** (v_d < 0, a_d > 0): Dimension still declining but deceleration indicates a floor. The worst is passing.

These regimes are directly actionable: a marketing manager observing (v_d > 0, a_d < 0) on a strategic dimension knows the current campaign is losing effectiveness before the dimension itself starts to decline -- an early warning signal invisible to position-only tracking.

### 3.7 Correspondence to the Kalman Filter

Brand Triangulation introduces a Perception Kalman filter with state (**x**, **v**) (Zharnikov, 2026y, Proposition 6). The relationship to the present framework is precise:

1. The Kalman filter's state vector (**x**, **v**) IS the phase space point from Definition 6.
2. The Kalman filter's prediction step (**x**_{t+1|t} = **x**_t + **v**_t * Delta_t) IS the first-order kinematic equation of motion.
3. The Kalman filter's posterior covariance matrix provides uncertainty bounds on both position and velocity estimates.
4. The Kalman gain automatically performs the noise-optimal smoothing discussed in Section 3.3.

The present paper thus provides the *theoretical semantics* for the Kalman filter state: velocity is not merely a latent variable that improves tracking accuracy (instrumental role); it is a first-class observable quantity with independent diagnostic value (conceptual role). The directional coherence, phase space representation, and trajectory clustering defined here are not available from the Kalman filter alone -- they require the kinematic interpretation developed in this section.

---

## 4. Velocity Resolves the Bonnet Ambiguity

### 4.1 The Bonnet Pair Problem in Brand Measurement

In differential geometry, Bonnet pairs are surfaces that share the same metric (first fundamental form) and the same mean curvature but are genuinely non-congruent -- different shapes that cannot be distinguished by metric measurements alone (Bobenko, Hoffmann, & Sageman-Furnas, 2025). The "missing information" is the second fundamental form: how the surface is embedded in the ambient space.

The analog in brand measurement is structural rather than exact (brand perception space is not a surface in the differential-geometric sense), but the identification problem is the same: two brands A and B may have identical spectral profiles **x**_A = **x**_B at a given time. If the only measurement is the spectral profile (Order 0), the brands are observationally equivalent -- indistinguishable by any profile-based framework. Yet they may be perceived differently by observers who have encountered them over time, because the brands arrived at the same profile via different trajectories.

This is not a hypothetical concern. Consider two brands that both score [7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0] -- a flat, undifferentiated profile. One brand reached this profile by declining from a distinctive peak (loss of differentiation). The other reached it by rising from a lower baseline (improvement across the board). Observers who experienced the decline perceive the brand as "fading"; observers who experienced the rise perceive it as "emerging." The spectral profile is identical; the perception is different. This is a Bonnet pair in brand measurement.

### 4.2 The Identification Problem

In statistical language, the Bonnet pair problem is an instance of observational equivalence (Rothenberg, 1971): two distinct parameter configurations produce identical observations under the available measurement model. When the measurement model captures only position **x**, any two brands at the same position are observationally equivalent.

The classical resolution in econometrics is to add identifying information -- instruments, exclusion restrictions, or additional observations that break the equivalence (Manski, 2007). In brand measurement, the additional information that resolves the equivalence is the *trajectory*: the time series of positions that reveals how the brand arrived at its current location.

### 4.3 Velocity as the Second Fundamental Form

**Theorem 1 (Velocity-Based Identification).** Let brands A and B have identical spectral profiles at time t: **x**_A(t) = **x**_B(t). If their velocity vectors differ, **v**_A(t) != **v**_B(t), then:

(a) The brands are distinguishable in phase space: (**x**_A, **v**_A) != (**x**_B, **v**_B).

(b) Under the SDE dynamics of Zharnikov (2026j), the brands' profiles will diverge for t' > t with probability 1: P(**x**_A(t') != **x**_B(t')) = 1 for any t' > t.

(c) The magnitude of divergence at t' = t + Delta_t is, to first order, ||**x**_A(t') - **x**_B(t')|| ~ ||**v**_A(t) - **v**_B(t)|| * Delta_t.

*Proof.* Part (a) is immediate from Definition 6. Part (b) follows from pathwise uniqueness of the SDE (Zharnikov, 2026j, Theorem 1): distinct velocity at time t implies distinct drift, which produces distinct trajectories for all subsequent times. The non-degeneracy of the diffusion coefficient ensures the probability is exactly 1, not merely positive. Part (c) is the Taylor expansion **x**(t + Delta_t) = **x**(t) + **v**(t) * Delta_t + O(Delta_t^2), applied to both brands and differenced.

**Interpretation.** Velocity plays the role of the second fundamental form in the Bonnet pair analogy. The spectral profile (metric) tells you the brand's current configuration. The velocity tells you how that configuration is embedded in time -- how the brand is moving through perception space. Just as the second fundamental form disambiguates Bonnet pairs in geometry, velocity disambiguates brands with identical current profiles.

### 4.4 Practical Implications

The velocity-based identification has immediate practical consequences:

1. **Competitive analysis.** Two brands at similar positions are often treated as substitutes. Velocity analysis may reveal that one is moving toward this position (a new entrant) while the other is moving away (an established brand repositioning). They are passing through the same point in opposite directions -- a competitive analysis that position-only measurement misses entirely.

2. **Crisis detection.** A brand at a high score on a dimension may be stable (v ~ 0) or decaying (v < 0). The position is the same; the velocity distinguishes health from impending decline.

3. **M&A assessment.** Two acquisition targets with similar brand profiles may differ dramatically in velocity. One with stable velocity is a lower-risk acquisition; one with high negative velocity is a declining asset, regardless of its current profile.

---

## 5. Trajectory-Based Analysis

### 5.1 Trajectory Clustering

Traditional brand segmentation clusters brands by position: brands with similar profiles are grouped together (strategic groups; Hunt, 1972). Trajectory clustering extends this by grouping brands by their dynamic state -- brands with similar (**x**, **v**) are in the same dynamic segment, even if their positions alone would place them in different groups.

Group-based trajectory modeling (Nagin, 1999, 2005) provides the statistical methodology: fit a finite mixture of trajectory shapes to longitudinal brand data, where each mixture component represents a distinct dynamic archetype. The extension to multi-dimensional brand profiles treats the eight-dimensional velocity vector as the trajectory shape parameter, clustering brands by their pattern of dimensional change rather than their dimensional levels.

### 5.2 Convergence and Divergence Detection

Two brands at different positions may be on converging trajectories if their velocity vectors point toward each other. Define the convergence indicator:

CI(A, B) = -(**v**_A - **v**_B) . (**x**_A - **x**_B) / (||**v**_A - **v**_B|| * ||**x**_A - **x**_B||)

This measures whether the relative velocity is closing or widening the gap between brands:

- CI > 0: Brands are converging (the brand that is "behind" on each dimension is moving faster on that dimension). Future competitors.
- CI < 0: Brands are diverging. Current proximity is temporary; they are differentiating.
- CI ~ 0: Brands are moving in parallel. Stable competitive relationship.

**Proposition 3 (Convergence time estimate).** For brands with convergence indicator CI > 0 and constant velocities, the time to positional convergence (||**x**_A - **x**_B|| < epsilon) is approximately:

t_conv ~ ||**x**_A - **x**_B|| / ||**v**_A - **v**_B||

This provides a first-order estimate of when two brands will occupy the same perceptual territory. The estimate degrades if velocities change (acceleration effects), but serves as a planning horizon for competitive response.

### 5.3 Dynamic Archetypes

Trajectory clustering reveals dynamic archetypes that have no analog in static segmentation:

- **Orbiting brands**: High speed, low net displacement. The brand moves rapidly across dimensions but returns to approximately the same position. Seasonal brands, fashion brands with cyclical repositioning.
- **Migrating brands**: High speed, high net displacement. The brand is repositioning deliberately and consistently. Dove 2003-2013 is an exemplar (Section 6).
- **Anchored brands**: Low speed, low displacement. Stable position with minimal change. Heritage luxury brands.
- **Drifting brands**: Moderate speed, no strategic direction. Movement without intent. The directional coherence metric (Definition 5) distinguishes drifting from migrating: both have non-zero speed, but drifters have low DC while migrators have high DC.

---

## 6. Illustration: Dove 2003--2023

### 6.1 Data

We use the dimensional profiles from Zharnikov (2026p), which assigns spectral profiles to Dove at four temporal cross-sections based on documented campaign activity, advertising content, public reception, and expert assessment.

**Table 1.** Dove spectral profiles at four temporal cross-sections (scale: 1-10)

| Dimension | 2003 | 2006 | 2013 | 2023 |
|---|---|---|---|---|
| Semiotic (S) | 5.0 | 5.5 | 6.0 | 7.0 |
| Narrative (N) | 4.0 | 7.5 | 8.5 | 7.5 |
| Ideological (I) | -- | 8.0 | 9.0 | 7.5 |
| Experiential (E) | 6.5 | 6.5 | 6.5 | 7.0 |
| Social (So) | 3.5 | 6.0 | 7.5 | 6.5 |
| Economic (Ec) | 7.0 | 7.0 | 7.0 | 6.5 |
| Cultural (C) | 4.0 | 8.5 | 8.0 | 5.5 |
| Temporal (T) | 6.0 | 6.5 | 7.0 | 7.5 |

Note: the Ideological dimension is marked "--" in 2003, indicating no meaningful ideological signal prior to the Real Beauty campaign. This dimensional creation event (null-to-positive transition) is a topological change that the differential calculus cannot capture as a standard derivative; we return to this in Section 8.1.

**Caveat.** These profiles are author-assigned based on qualitative assessment, not derived from survey data or experimental measurement. The illustration demonstrates the analytical framework, not empirical findings. The velocity and acceleration values computed below are illustrative of the method, not validated measurements of Dove's actual perceptual dynamics.

### 6.2 Velocity Vectors

We compute velocity vectors for three periods using the finite difference estimator (Section 3.2):

**Table 2.** Velocity vectors for three periods (units per year)

**Period 1: Ignition (2003--2006, Delta_t = 3 years)**

| Dim | v (units/yr) | Interpretation |
|---|---|---|
| S | +0.17 | Gradual semiotic evolution |
| N | +1.17 | Rapid narrative construction |
| I | -- | Dimensional creation (not a derivative) |
| E | 0.00 | Product experience unchanged |
| So | +0.83 | Community forming around campaign |
| Ec | 0.00 | Price positioning unchanged |
| C | +1.50 | Strong counter-cultural resonance |
| T | +0.17 | Modest heritage accumulation |

Brand speed (7 computable dimensions, excluding Ideological): ||**v**|| = 2.10 units/yr. This is a high-speed brand -- consistent with a major campaign launch creating rapid perceptual change. Note: brand speed in this period is computed over 7 dimensions because the Ideological velocity is undefined (dimensional creation event). Speeds in Periods 2 and 3 are computed over all 8 dimensions. Cross-period speed comparisons should account for this dimensional mismatch.

**Period 2: Expansion (2006--2013, Delta_t = 7 years)**

| Dim | v (units/yr) | Interpretation |
|---|---|---|
| S | +0.07 | Semiotic stabilizing |
| N | +0.14 | Narrative still growing, but slowly |
| I | +0.14 | Ideological continuing to build |
| E | 0.00 | Product unchanged |
| So | +0.21 | Social continuing to build |
| Ec | 0.00 | Price unchanged |
| C | -0.07 | Cultural beginning to decline |
| T | +0.07 | Heritage accumulating |

Brand speed: ||**v**|| = 0.31 units/yr. The brand has decelerated dramatically -- campaign maturation. The Cultural dimension has turned negative (early counter-cultural decay, as theorized in Zharnikov, 2026p, Proposition 4).

**Period 3: Normative Absorption (2013--2023, Delta_t = 10 years)**

| Dim | v (units/yr) | Interpretation |
|---|---|---|
| S | +0.10 | Slow semiotic evolution |
| N | -0.10 | Narrative declining |
| I | -0.15 | Ideological declining |
| E | +0.05 | Slight experiential improvement |
| So | -0.10 | Social declining |
| Ec | -0.05 | Mild economic erosion |
| C | -0.25 | Strong cultural decline |
| T | +0.05 | Heritage still accumulating |

Brand speed: ||**v**|| = 0.36 units/yr. Speed is slightly higher than Period 2, but the direction has reversed: most dimensions are now declining. This is the "normative absorption" phase where Dove's once-distinctive messaging has been adopted by competitors and absorbed into cultural expectations.

### 6.3 Acceleration Vectors

**Table 3.** Acceleration vectors between consecutive periods

Acceleration between Period 1 and Period 2 (estimated at midpoints 2004.5 and 2009.5, Delta_t_mid ~ 5 years):

| Dim | a (units/yr^2) | Regime |
|---|---|---|
| S | -0.020 | Decelerating (saturation) |
| N | -0.206 | Strong deceleration |
| So | -0.124 | Decelerating |
| C | -0.314 | Very strong deceleration, approaching reversal |
| T | -0.020 | Mild deceleration |

Acceleration between Period 2 and Period 3 (midpoints 2009.5 and 2018, Delta_t_mid ~ 8.5 years):

| Dim | a (units/yr^2) | Regime |
|---|---|---|
| S | +0.004 | Approximately constant (stable slow growth) |
| N | -0.028 | Continuing deceleration into decline |
| I | -0.034 | Decelerating into decline |
| So | -0.036 | Decelerating into decline |
| C | -0.021 | Decline continuing but rate stabilizing |
| T | -0.002 | Approximately constant |

### 6.4 Dynamic Interpretation

The velocity and acceleration vectors tell a story that position alone cannot:

1. **The Cultural dimension is the leading indicator.** Cultural velocity turned negative before any other dimension (Period 2: v_C = -0.07). The acceleration was strongly negative throughout (a_C = -0.314 in the first period). By the time Cultural decline is visible in the position data (dropping from 8.5 to 5.5), the velocity framework would have flagged the deceleration years earlier -- during the 2006-2013 period, when Cultural position was still near its peak.

2. **Narrative and Social follow Cultural with a lag.** These dimensions remain positive in Period 2 (v_N = +0.14, v_So = +0.21) but are decelerating. By Period 3, both have turned negative. The acceleration vectors in Period 1 predicted this reversal.

3. **Brand speed follows an inverted-U.** Speed peaks during ignition (2.10), drops during expansion (0.31), and rises slightly during absorption (0.36). The rising speed in Period 3 is deceptive -- the brand is not regaining momentum; it is losing ground across multiple dimensions simultaneously.

4. **The Experiential dimension is independent.** Experiential velocity is essentially zero throughout, consistent with the product (soap, body wash) remaining unchanged while the brand's meaning undergoes radical transformation. This dimensional independence validates the SBT dimensional taxonomy: the dimensions capture distinct aspects of brand perception that can change independently.

5. **Directional coherence analysis.** If Dove's strategy vector was **s** ~ [0, 0, 1, 0, 1, 0, 0, 0] (targeting Ideological and Social growth), then:
   - Period 1: DC ~ +0.72 (well-aligned; Ideological creation + Social growth)
   - Period 2: DC ~ +0.67 (still aligned; both dimensions growing)
   - Period 3: DC ~ -0.53 (misaligned; both target dimensions declining)

   The shift from positive to negative directional coherence marks the transition from effective to counterproductive campaigning -- the brand's continued messaging is no longer producing movement in the intended direction. This is a quantitative signal of the "counter-cultural decay" that Zharnikov (2026p, Proposition 4) describes qualitatively.

---

## 7. Managerial Implications

### 7.1 The Brand Speedometer

Brand speed (Definition 4) provides a simple, actionable KPI: how fast is the brand changing? A dashboard displaying brand speed over time reveals acceleration and deceleration patterns that position-only tracking misses. The speedometer is especially valuable during campaign launches (is speed increasing?), crises (is speed increasing in unintended directions?), and brand maintenance periods (is speed near zero, confirming stability?).

### 7.2 Strategy-Trajectory Alignment

Directional coherence (Definition 5) answers the question every CMO should ask but rarely can: "Is our brand moving in the direction we intend?" A DC below 0.3 indicates that marketing expenditure is generating perceptual change but not in the strategic direction. A DC below 0 indicates actively counterproductive investment. The Dove illustration (Section 6.4) shows DC declining from +0.72 to -0.53 over 20 years -- a quantitative signal that the campaign's effectiveness had reversed.

### 7.3 Competitive Early Warning

Convergence detection (Section 5.2) identifies future competitors before they become current competitors. Traditional competitive analysis compares current positions; trajectory analysis compares velocities. A brand entering your perceptual territory from a different starting position (high convergence indicator) is a strategic threat that position-only analysis would not flag until the brands are already in direct competition.

### 7.4 Measurement Frequency Recommendations

The noise amplification analysis (Section 3.3) implies that velocity estimation is robust at quarterly measurement intervals, while acceleration requires semi-annual or annual intervals with smoothing. Furthermore, different dimensions may require different measurement frequencies based on their characteristic timescales:

- **Fast dimensions** (Economic, Experiential): Responsive to short-term actions (pricing, product updates). Quarterly measurement is appropriate.
- **Medium dimensions** (Semiotic, Narrative, Social): Responsive to campaigns and communications. Semi-annual measurement is sufficient.
- **Slow dimensions** (Cultural, Temporal): Change slowly and respond to macro-trends. Annual measurement is sufficient; more frequent measurement would be dominated by noise.

This dimensional timescale separation reduces measurement cost while improving signal-to-noise on each dimension.

---

## 8. Discussion

### 8.1 Limitations

**Data frequency.** The Dove illustration uses four time points over 20 years. This provides three velocity estimates and two acceleration estimates -- the minimum for demonstrating the framework. Denser time series would improve the estimates and enable detection of nonlinear dynamics. The optimal measurement interval analysis (Proposition 1) provides guidance, but practical brand tracking rarely exceeds quarterly frequency.

**Noise amplification.** Differentiation amplifies measurement error (Section 3.3). Velocity estimates from two noisy measurements can be unreliable; acceleration estimates from three noisy measurements more so. The Kalman filter (Section 3.7) is the recommended practical estimator, as it performs optimal noise-variance tradeoff. Raw finite differences should be treated as illustrative, not definitive.

**Author-assigned profiles.** The Dove profiles are based on qualitative expert assessment, not survey or experimental data. The illustration demonstrates the analytical framework but does not validate it empirically. Validation requires application to measured brand tracking data with known measurement properties.

**Dimensional creation events.** The null-to-positive transition on Dove's Ideological dimension (2003 to 2006) is a topological change -- the dimension did not exist in the brand's perceptual space and then appeared. The differential calculus requires continuity; dimensional creation is a discontinuity. The framework handles smooth evolution well but requires supplementation for creation/destruction events. These events are rare (most brands do not create new perceptual dimensions) but theoretically important.

**Stationarity assumption.** The differential calculus assumes dynamics smooth enough to differentiate. Brand crises (Dieselgate, product recalls) create discontinuities where derivatives do not exist in the classical sense. The Kalman filter handles this through its innovation sequence: large prediction errors flag regime changes. A formal treatment would require jump-diffusion models (SDE with Poisson-driven jumps), extending Zharnikov (2026j).

### 8.2 Connection to the SBT Analogy Stack

The differential calculus completes a parallel between SBT and classical mechanics.

**Table 4.** Correspondence between classical mechanics and SBT brand dynamics

| Mechanics | SBT | Paper |
|---|---|---|
| Position **x** | Spectral profile | SBT (2026a) |
| Metric g_{ij} | Fisher-Rao + warped product | R1 (2026d) |
| Velocity **v** = d**x**/dt | Brand velocity | This paper |
| Acceleration **a** = d^2**x**/dt^2 | Brand acceleration | This paper |
| Phase space (**x**, **v**) | Brand phase space | This paper |
| Force **F** = m**a** | Brand force (future) | -- |
| Lagrangian L(**x**, **v**) | Perception Lagrangian (future) | -- |
| Geodesic motion | Inertial brand trajectory | R6 (2026j) |
| Non-ergodicity | Path-dependent perception | R9 (2026o) |

The force and Lagrangian rows are deliberately left for future work. Defining "brand force" requires a concept of "brand mass" (inertia) that does not yet have a clean SBT definition independent of force and acceleration. Without such a definition, F = ma is circular. The Lagrangian requires a potential function V(**x**) (the perception landscape) whose derivation from SBT primitives is a substantial theoretical program.

### 8.3 The Correspondence Principle for Dynamics

When brand velocity is negligible (||**v**|| ~ 0), the phase space representation collapses to position-only measurement, and the differential calculus adds no information. This is the "static limit" -- the regime in which classical brand measurement frameworks (Aaker, 1991; Keller, 1993) are adequate.

The static limit holds for:

- Established brands in stable markets with no active repositioning
- Short measurement horizons (within a single campaign cycle)
- Dimensions with slow intrinsic dynamics (Cultural, Temporal)

The dynamic framework is needed when:

- Brands are actively repositioning (Dove 2003-2006)
- Markets are disrupted (new entrants, technological shifts, regulatory changes)
- Dimensions have fast dynamics (Economic responses to pricing, Experiential responses to product changes)
- Non-ergodicity matters (individual trajectory divergence, as in Zharnikov, 2026o)

This correspondence principle parallels the SBT analogy stack: classical brand measurement is the "Newtonian limit" of the full dynamic framework, valid when the "velocity" of brand perception is small relative to measurement precision. The distinction between persistent and transient marketing effects (Dekimpe & Hanssens, 1995) maps naturally onto this framework: persistent effects produce sustained velocity (the brand moves to a new equilibrium), while transient effects produce temporary velocity that decays (the brand returns to its prior position). The velocity framework thus provides the measurement language for Dekimpe and Hanssens' persistence distinction applied to multi-dimensional brand perception.

### 8.4 Future Research

**Spectral force.** What causes brand acceleration? Each marketing action -- advertising, product launch, pricing change, endorsement -- is a force vector in R^8. The net force is the vector sum of concurrent actions. Identifying the force contribution of individual actions requires controlled experiments or structural models that decompose the observed acceleration into causal components.

**Perception Lagrangian.** A variational approach where brand trajectories minimize an action functional would connect SBT to optimal control theory, enabling prescriptive recommendations (what trajectory minimizes a cost function subject to resource constraints?).

**Temporal DOP.** Just as Perception DOP (Zharnikov, 2026y) quantifies how observer geometry affects position estimation, a Temporal DOP would quantify how measurement timing affects velocity estimation. Unevenly spaced measurements, missing waves, and varying sample sizes all affect velocity precision in ways that a temporal DOP metric could formalize.

**Empirical validation.** Application to measured brand tracking data (e.g., YouGov BrandIndex, Kantar BrandZ) would test whether the velocity and acceleration quantities computed from real data produce actionable and predictive insights. The Dove illustration is conceptual; validation requires data with known measurement properties and external criteria for evaluating velocity-based predictions.

---

## 9. Conclusion

Brand measurement has been fundamentally static: we know where brands are but not where they are going. This paper introduces a differential calculus for multi-dimensional brand perception that extends Spectral Brand Theory from position (Order 0) to velocity (Order 1) and acceleration (Order 2). Three contributions emerge: velocity resolves the Bonnet pair ambiguity in brand measurement (Theorem 1), directional coherence quantifies strategy-trajectory alignment (Definition 5), and trajectory clustering enables dynamic competitive analysis (Section 5).

The Dove illustration demonstrates that velocity and acceleration reveal dynamics invisible to position-only tracking -- the Cultural dimension's deceleration predicted its subsequent decline years before the decline appeared in position data. The framework connects naturally to existing state-space methods in marketing science, embedding the Kalman filter within a kinematic theory that gives velocity and acceleration independent diagnostic meaning.

The framework completes the dynamics layer of Spectral Brand Theory: the SDE model (Zharnikov, 2026j) describes how perception evolves; the non-ergodicity analysis (Zharnikov, 2026o) explains why trajectories diverge; the coherence-resilience derivation (Zharnikov, 2026s) predicts crisis vulnerability from dynamic signatures; and the present paper provides the measurement framework that makes these theoretical dynamics observable and actionable.

---

## References

Aaker, D. A. (1991). *Managing Brand Equity: Capitalizing on the Value of a Brand Name*. Free Press.

Bobenko, A. I., Hoffmann, T., & Sageman-Furnas, A. O. (2025). Compact Bonnet pairs: Isometric tori with the same curvatures. *Publications Mathematiques de l'IHES*, 142, 241--293. https://doi.org/10.1007/s10240-025-00159-z

Bourgeois, L. J., & Eisenhardt, K. M. (1988). Strategic decision processes in high velocity environments: Four cases in the microcomputer industry. *Management Science*, 34(7), 816--835.

Bruce, N. I. (2008). Pooling and dynamic forgetting effects in multitheme advertising: Tracking the advertising sales relationship with particle filters. *Marketing Science*, 27(4), 659--673.

Cover, T. M., & Thomas, J. A. (2006). *Elements of information theory* (2nd ed.). Wiley-Interscience.

D'Aveni, R. A. (1994). *Hypercompetition: Managing the Dynamics of Strategic Maneuvering*. Free Press.

Dekimpe, M. G., & Hanssens, D. M. (1995). The persistence of marketing effects on sales. *Marketing Science*, 14(1), 1--21.

Dooley, K. J., & Van de Ven, A. H. (1999). Explaining complex organizational dynamics. *Organization Science*, 10(3), 358--372.

Hunt, M. S. (1972). *Competition in the major home appliance industry, 1960--1970*. Doctoral dissertation, Harvard University.

Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering*, 82(1), 35--45.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1--22.

Manski, C. F. (2007). *Identification for Prediction and Decision*. Harvard University Press.

Muthen, B., & Shedden, K. (1999). Finite mixture modeling with mixture outcomes using the EM algorithm. *Biometrics*, 55(2), 463--469.

Nagin, D. S. (1999). Analyzing developmental trajectories: A semiparametric, group-based approach. *Psychological Methods*, 4(2), 139--157.

Nagin, D. S. (2005). *Group-Based Modeling of Development*. Harvard University Press.

Naik, P. A., & Raman, K. (2003). Understanding the impact of synergy in multimedia communications. *Journal of Marketing Research*, 40(4), 375--388.

Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, 15(12), 1216--1221. https://doi.org/10.1038/s41567-019-0732-0

Ramsay, J. O., & Silverman, B. W. (2005). *Functional Data Analysis* (2nd ed.). Springer.

Rothenberg, T. J. (1971). Identification in parametric models. *Econometrica*, 39(3), 577--591.

Sriram, S., Chintagunta, P. K., & Neelamegham, R. (2006). Effects of brand preference, product attributes, and marketing mix variables in technology product markets. *Marketing Science*, 25(5), 440--456.

Sterman, J. D. (2000). *Business Dynamics: Systems Thinking and Modeling for a Complex World*. McGraw-Hill.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026d). Brand space geometry: A formal metric for multi-dimensional brand perception. Working Paper. https://doi.org/10.5281/zenodo.18945295

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026j). Non-ergodic brand perception: Diffusion dynamics on multi-dimensional perceptual manifolds. Working Paper. https://doi.org/10.5281/zenodo.18945659

Zharnikov, D. (2026o). Non-ergodic brand perception: Why cross-sectional brand tracking systematically misrepresents individual trajectories. Working Paper. https://doi.org/10.5281/zenodo.19138860

Zharnikov, D. (2026p). Dimensional activation and cohort divergence: A longitudinal decomposition of purpose advertising effectiveness. Working Paper. https://doi.org/10.5281/zenodo.19139258

Zharnikov, D. (2026s). Coherence type as crisis predictor: A formal derivation from non-ergodic dynamics. Working Paper. https://doi.org/10.5281/zenodo.19208107

Zharnikov, D. (2026y). Brand triangulation: A geometric framework for multi-observer brand positioning. Working Paper.

---

## Disclosure

No funding was received for this research. No conflicts of interest to declare. The author used AI assistants (Claude, Anthropic) for literature verification, mathematical checking, and editorial review. All theoretical contributions, arguments, and errors are the author's own.

## Data Availability

The Dove dimensional profiles used in Section 6 are reproduced from Zharnikov (2026p, Table 1). No new data was collected for this paper.
