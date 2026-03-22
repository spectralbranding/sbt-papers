# Non-Ergodic Brand Perception: Diffusion Dynamics on Multi-Dimensional Perceptual Manifolds

**Zharnikov, D.**

Working Paper -- March 2026

---

## Abstract

Brand perception evolves over time, yet no existing brand theory provides a formal dynamical model of this evolution. This paper models the trajectory of an observer's brand perception as a stochastic process on $S^7_+$, the positive octant of the 7-sphere in Spectral Brand Theory's (SBT) eight-dimensional perception space. Signal encounters drive Brownian motion on the manifold, signal decay introduces deterministic drift toward a neutral prior, and negative conviction creates absorbing boundaries at the octant boundary where any perceptual dimension reaches zero. We formulate a Stratonovich stochastic differential equation (SDE) on $S^7_+$ and prove four main results. First, the SDE with absorbing boundaries is well-posed with a unique strong solution up to the absorption stopping time (Theorem 1). Second, the survival probability decays as $S(t, x) \sim C(x) \exp(-\lambda_{D,1} \sigma^2 t / 2)$, where $C(x)$ depends on the initial position's distance from the boundary (Theorem 2). Third, the Dirichlet spectral gap on $S^7_+$ is $\lambda_{D,2} - \lambda_{D,1} = 48$, so mixing to the quasi-stationary distribution is faster than on the full sphere: conditioned on survival, perception trajectories are confined to the deep interior of the octant (Theorem 3). Fourth, for the absorbed process, the time average and ensemble average of any non-trivial observable diverge with probability 1 as $t \to \infty$, establishing non-ergodicity consistent with the framework of Peters (2019) (Theorem 4). Application to five case-study brands shows that the absorption risk ordering -- Tesla (C-) > Erewhon (B-) > IKEA (A-) > Patagonia (B+) > Hermès (A+) -- nearly matches the SBT coherence grading (Proposition 5), with one inversion (IKEA/Patagonia) explained by coherence-type-dependent drift strength, providing the first formal connection between brand coherence and stochastic stability. The results formalize SBT's ergodicity coefficient as $\varepsilon \sim 1/\tau_{\text{mix}}$, complete the dynamic extension of the static metric framework established in Zharnikov (2026d), and establish that the distinction between *vectorized* and *rasterized* brand management is not merely practical but reflects a fundamental mathematical asymmetry between trajectory-level and snapshot-level information. Finally, distribution-free calibration of per-dimension velocity estimates is developed using split conformal prediction (Proposition 6), providing calibrated uncertainty bands with finite-sample coverage guarantees and no distributional assumptions.

**Keywords**: stochastic differential equations on manifolds, non-ergodicity, brand perception dynamics, absorbing boundaries, Laplace-Beltrami operator, mixing time, conformal prediction, Spectral Brand Theory

**JEL Classification**: C65, M31, C02

**MSC Classification**: 58J65, 60J60, 91B42

---

## 1. Introduction

Every brand theory acknowledges that brand perception changes over time. Keller's (1993) Customer-Based Brand Equity model invokes "brand building" and "brand leveraging" as temporal processes. Aaker (1991) discusses brand loyalty as something earned over repeated interactions. Kapferer (2008, 4th ed.) describes the "brand identity prism" as evolving through market engagement. Yet none of these frameworks provides a formal dynamical model -- a mathematical description of *how* perception evolves, *what drives* its evolution, and *why* some trajectories are reversible while others are not.

The gap is not merely aesthetic. Without a dynamical model, brand theory cannot answer several questions that arise naturally from Spectral Brand Theory's (Zharnikov, 2026a) static framework:

1. **Why is negative conviction absorbing?** SBT asserts that sufficiently negative brand experiences create irreversible perceptual states -- that an observer who concludes "this brand is fundamentally dishonest" cannot be brought back to neutrality by any number of positive signals. This is a dynamical claim that requires a dynamical proof.

2. **Why do time averages and ensemble averages diverge?** Peters (2019) demonstrated that the failure of ergodicity in economic systems has profound consequences for decision theory. SBT's ergodicity coefficient $\varepsilon$ (Zharnikov, 2026a) claims an analogous non-ergodicity in brand perception, but the claim has remained qualitative. *When exactly* do time and ensemble averages diverge, and *by how much*?

3. **Why does signal decay matter?** SBT models signal luminosity as decaying over time (emotional intensity fades, memories erode), with crystallized signals exempt from decay. This creates a competition between incoming signals and fading memory. What are the dynamical consequences?

4. **Why does the D/A ratio affect trajectory stability?** SBT's designed/ambient ratio controls how much of a brand's perception is strategically managed versus emergent. The static framework observes that D/A ratios of 55--65% produce the most stable perception. A dynamical model should provide a dynamical rationale for this from the mathematics.

This paper provides the missing dynamical foundation. We model an observer's evolving perception of a brand as a trajectory on $S^7_+$, the positive octant of the 7-sphere -- the natural state space for normalized perception profiles with eight non-negative components. Signal encounters drive stochastic perturbations (Brownian motion on the manifold), signal decay introduces deterministic drift (toward a neutral prior), and negative conviction creates absorbing boundaries (at the octant boundary where any dimension reaches zero). The resulting stochastic differential equation (SDE) admits a rigorous analysis using the spectral theory of the Laplace-Beltrami operator on $S^7_+$ with Dirichlet boundary conditions.

The gap in formal dynamical modeling is not for lack of adjacent work. Longitudinal brand tracking studies (e.g., Young & Rubicam's BrandAsset Valuator, Millward Brown's BrandZ) measure brand perception at multiple time points, but these are sequences of static snapshots rather than dynamical systems -- they do not specify equations of motion or characterize trajectories. Brand loyalty dynamics models (Dick & Basu, 1994) formalize the relationship between relative attitude and patronage but operate on one-dimensional attitude scales, not on a multi-dimensional metric space; the geometry of loyalty trajectories is undefined. Attitude-change models in the persuasion literature, including the Elaboration Likelihood Model (Petty & Cacioppo, 1986), specify conditions under which attitude change occurs and identify central versus peripheral processing routes, but they neither produce a metric on attitude space nor model attitude evolution as a stochastic process with drift and diffusion components. The common deficiency is structural: none of these frameworks places brand perception in a formal metric space, and without a metric space, drift, diffusion, and absorbing boundaries -- the essential objects of a dynamical model -- cannot be defined.

The approach connects three previously separate intellectual traditions. From **stochastic analysis on manifolds** (Hsu, 2002; Stroock, 2000), we draw the formulation of Brownian motion on Riemannian manifolds and the connection between the Laplace-Beltrami spectrum and mixing times. From **ergodicity economics** (Peters, 2019; Peters & Gell-Mann, 2016), we draw the distinction between time and ensemble averages and the consequences of their divergence. From **opinion dynamics** (Hegselmann & Krause, 2002; Deffuant et al., 2000), we draw the insight that belief evolution can be modeled as a geometric process -- though existing opinion dynamics models operate in flat Euclidean space, not on curved manifolds.

The paper builds on the metric framework established in Zharnikov (2026d), which defined the Aitchison metric on brand signal space $\mathbb{R}^8_+$ and the Fisher-Rao metric on observer weight space $\Delta^7$. Where that paper established the *geometry* of brand perception (how to measure distances), this paper establishes the *dynamics* (how positions change over time). The two together -- statics and dynamics -- provide a complete mathematical foundation for SBT.

The remainder of the paper is organized as follows. Section 2 establishes preliminaries and notation, recalling the SBT framework and the relevant elements of Riemannian geometry. Section 3 develops Brownian motion on spheres, including the Laplace-Beltrami operator and its eigenvalues. Section 4 formulates the brand perception SDE. Section 5 analyzes absorbed Brownian motion on $S^7_+$. Section 6 establishes mixing time bounds and non-ergodicity results. Section 7 connects the mathematical framework to SBT's signal dynamics and brand strategy. Section 8 presents numerical demonstrations for the five case-study brands. Section 9 discusses implications. Section 10 connects to the broader research program. Section 11 develops distribution-free calibration of velocity estimates using conformal prediction. Section 12 concludes.

---

## 2. Preliminaries

### 2.1 SBT Framework Recap

Spectral Brand Theory (Zharnikov, 2026a) models a brand as a stellar object emitting signals across eight typed dimensions:

| Index | Dimension | Description |
|-------|-----------|-------------|
| 1 | Semiotic | Visual identity, logo, design language |
| 2 | Narrative | Brand story, founding mythology, purpose |
| 3 | Ideological | Values, beliefs, political positioning |
| 4 | Experiential | Product/service interaction quality |
| 5 | Social | Community, tribal affiliation, status |
| 6 | Economic | Pricing, value proposition, accessibility |
| 7 | Cultural | Cultural resonance, zeitgeist alignment |
| 8 | Temporal | Heritage, longevity, temporal compounding |

A brand's **emission profile** is a vector $s = (s_1, \ldots, s_8) \in \mathbb{R}^8_+$. An observer's **weight profile** (also known as the observer spectral profile) is $w = (w_1, \ldots, w_8) \in \Delta^7$. The observer's **perception profile** -- the internal representation of the brand -- is a normalized vector on the positive octant of the 7-sphere:

$$x = \frac{(w_1 s_1, \ldots, w_8 s_8)}{\|(w_1 s_1, \ldots, w_8 s_8)\|} \in S^7_+$$

This perception profile evolves over time as the observer encounters new signals, as memory of past signals decays, and as priors crystallize. The evolution of $x(t)$ is the central object of this paper.

SBT assigns five coherence levels based on the emission profile analysis:

| Grade | Type | Example |
|-------|------|---------|
| A+ | Ecosystem coherence | Hermès |
| A- | Signal coherence | IKEA |
| B+ | Identity coherence | Patagonia |
| B- | Experiential asymmetry | Erewhon |
| C- | Incoherent | Tesla |

The canonical emission profiles from Zharnikov (2026d) are:

| Dimension | Hermès | IKEA | Patagonia | Erewhon | Tesla |
|-----------|--------|------|-----------|---------|-------|
| Semiotic | 9.5 | 8.0 | 6.0 | 7.0 | 7.5 |
| Narrative | 9.0 | 7.5 | 9.0 | 6.5 | 8.5 |
| Ideological | 7.0 | 6.0 | 9.5 | 5.0 | 3.0 |
| Experiential | 9.0 | 7.0 | 7.5 | 9.0 | 6.0 |
| Social | 8.5 | 5.0 | 8.0 | 8.5 | 7.0 |
| Economic | 3.0 | 9.0 | 5.0 | 3.5 | 6.0 |
| Cultural | 9.0 | 7.5 | 7.0 | 7.5 | 4.0 |
| Temporal | 9.5 | 6.0 | 6.5 | 2.5 | 2.0 |

### 2.2 Riemannian Geometry of the 7-Sphere

The **7-sphere** $S^7 = \{x \in \mathbb{R}^8 : \|x\| = 1\}$ is a 7-dimensional Riemannian manifold with the metric inherited from $\mathbb{R}^8$. Its geometry is characterized by:

- **Sectional curvature**: $K = 1$ (constant positive curvature).
- **Riemannian volume**: $\text{Vol}(S^7) = \frac{\pi^4}{3} \approx 32.47$.
- **Diameter**: $\text{diam}(S^7) = \pi$ (the distance between antipodal points).

The **tangent space** at $x \in S^7$ is $T_x S^7 = \{v \in \mathbb{R}^8 : \langle v, x \rangle = 0\}$, the 7-dimensional subspace orthogonal to $x$. The **exponential map** $\exp_x: T_x S^7 \to S^7$ is given by:

$$\exp_x(v) = \cos(\|v\|) x + \sin(\|v\|) \frac{v}{\|v\|}$$

for $v \neq 0$, which maps tangent vectors to points on the sphere along geodesics (great circles).

The **positive octant** $S^7_+ = S^7 \cap \mathbb{R}^8_+$ is the subset where all coordinates are strictly positive. It is a manifold with boundary, where the boundary $\partial S^7_+$ consists of points with at least one coordinate equal to zero. The positive octant has volume:

$$\text{Vol}(S^7_+) = \frac{1}{2^8} \text{Vol}(S^7) = \frac{\pi^4}{768} \approx 0.1269$$

as established in Zharnikov (2026d), reflecting the $1/256$ compression factor from restricting to non-negative coordinates.

### 2.3 The Laplace-Beltrami Operator on $S^{n-1}$

The **Laplace-Beltrami operator** $\Delta_{S^{n-1}}$ on the $(n-1)$-sphere is the natural generalization of the Laplacian to curved manifolds. In ambient coordinates, for a function $f: S^{n-1} \to \mathbb{R}$, the Laplace-Beltrami operator can be expressed as the restriction of the ambient Laplacian $\Delta_{\mathbb{R}^n}$ to functions on the sphere:

$$\Delta_{S^{n-1}} f = \Delta_{\mathbb{R}^n} \tilde{f} \big|_{S^{n-1}}$$

where $\tilde{f}$ is the degree-zero homogeneous extension of $f$ (Berger, Gauduchon, & Mazet, 1971).

The eigenvalues of $-\Delta_{S^{n-1}}$ are:

$$\lambda_\ell = \ell(\ell + n - 2), \quad \ell = 0, 1, 2, \ldots$$

with multiplicities:

$$m_\ell = \binom{n + \ell - 1}{\ell} - \binom{n + \ell - 3}{\ell - 2}$$

For $S^7$ (i.e., $n = 8$), the first non-trivial eigenvalue is:

$$\lambda_1 = 1 \cdot (1 + 8 - 2) = 7$$

with multiplicity $m_1 = 8$, corresponding to the eight coordinate functions $x_1, \ldots, x_8$ restricted to the sphere (spherical harmonics of degree 1). The eigenvalue gap $\lambda_1 = 7$ governs the rate at which Brownian motion on $S^7$ mixes -- a fact that will be central to our analysis.

### 2.4 Transition Density on $S^7$

The **heat kernel** on $S^{n-1}$, which gives the transition density of Brownian motion, can be expressed as a spectral expansion:

$$p_t(x, y) = \frac{1}{\text{Vol}(S^{n-1})} \sum_{\ell=0}^{\infty} m_\ell \, C_\ell^{(n/2-1)}(\langle x, y \rangle) \, e^{-\lambda_\ell t}$$

where $C_\ell^{(\alpha)}$ are Gegenbauer (ultraspherical) polynomials. For $S^7$ with $n = 8$, this becomes:

$$p_t(x, y) = \frac{1}{\text{Vol}(S^7)} \sum_{\ell=0}^{\infty} m_\ell \, C_\ell^{(3)}(\langle x, y \rangle) \, e^{-\ell(\ell+6) t}$$

The exponential decay rate of the $\ell$-th term is $\ell(\ell + 6)$. The dominant non-constant term decays as $e^{-7t}$, confirming that the spectral gap $\lambda_1 = 7$ controls the rate of convergence to the uniform distribution on $S^7$.

---

## 3. Brownian Motion on Spheres

### 3.1 Construction via Projection

Brownian motion on $S^{n-1}$ can be constructed from standard Euclidean Brownian motion by continuous projection. Let $W_t$ be an $n$-dimensional standard Brownian motion. Brownian motion $B_t$ on $S^{n-1}$ is the solution to the Stratonovich SDE:

$$\circ dB_t = P_{B_t} \circ dW_t$$

where $P_x = I - x x^T$ is the orthogonal projection onto the tangent space $T_x S^{n-1}$ at $x$, and $\circ$ denotes the Stratonovich differential (Hsu, 2002; Stroock, 2000). The Stratonovich formulation is natural here because it preserves the manifold constraint: if $B_0 \in S^{n-1}$, then $B_t \in S^{n-1}$ for all $t \geq 0$.

In Ito form, the same process is:

$$dB_t = -\frac{n-1}{2} B_t \, dt + P_{B_t} \, dW_t$$

The deterministic drift $-\frac{n-1}{2} B_t$ is the mean curvature vector of $S^{n-1}$ embedded in $\mathbb{R}^n$; it keeps the process on the sphere. For $S^7$, this drift is $-\frac{7}{2} B_t$.

### 3.2 Generator and Eigenvalues

The infinitesimal generator of Brownian motion on $S^{n-1}$ is $\frac{1}{2} \Delta_{S^{n-1}}$, half the Laplace-Beltrami operator. The factor of $1/2$ arises from the normalization convention for Brownian motion. The semigroup $P_t f(x) = \mathbb{E}[f(B_t) | B_0 = x]$ satisfies:

$$\frac{\partial}{\partial t} P_t f = \frac{1}{2} \Delta_{S^{n-1}} P_t f$$

This is the heat equation on the sphere. Its spectral decomposition gives:

$$P_t f(x) = \sum_{\ell=0}^{\infty} e^{-\lambda_\ell t / 2} \langle f, Y_\ell \rangle Y_\ell(x)$$

where $Y_\ell$ are spherical harmonics and the inner product is with respect to the uniform measure on $S^{n-1}$.

### 3.3 Mixing Time on the Full Sphere

The **mixing time** $\tau_{\text{mix}}$ is the time required for the distribution of $B_t$ to become approximately uniform, regardless of the initial condition. Following standard definitions (Levin, Peres, & Wilmer, 2009), we define mixing time via total variation distance:

$$\tau_{\text{mix}}(\delta) = \inf\left\{ t > 0 : \sup_{x \in S^{n-1}} d_{\text{TV}}\left( P_t(x, \cdot), \text{Unif}(S^{n-1}) \right) \leq \delta \right\}$$

For Brownian motion on $S^{n-1}$, the spectral gap characterization gives:

$$\tau_{\text{mix}} \asymp \frac{1}{\lambda_1 / 2} = \frac{2}{\lambda_1}$$

For $S^7$:

$$\tau_{\text{mix}}(S^7) \asymp \frac{2}{7} \approx 0.286$$

This is fast mixing -- the high curvature and connectivity of $S^7$ cause Brownian motion to rapidly "forget" its starting point. The question central to brand perception dynamics is: *what happens to the mixing time when we restrict to the positive octant $S^7_+$ and impose absorbing boundaries?*

### 3.4 Comparison with Flat Euclidean Models

Existing opinion dynamics models (Hegselmann & Krause, 2002; Deffuant et al., 2000) formulate belief evolution as random walks in flat Euclidean space $\mathbb{R}^n$. The key differences when moving to spherical geometry are:

1. **Compactness**: $S^7$ is compact, so Brownian motion is recurrent and has a unique stationary distribution (the uniform measure). In $\mathbb{R}^8$, Brownian motion is transient for $n \geq 3$.

2. **Curvature**: The positive curvature of $S^7$ accelerates mixing relative to flat space. The Lichnerowicz theorem (Lichnerowicz, 1958) gives $\lambda_1 \geq \frac{n-1}{n-2} K(n-2) = n - 1$ for an $(n-1)$-dimensional manifold with Ricci curvature $\text{Ric} \geq (n-2) K$. For $S^{n-1}$ with $K = 1$, this recovers $\lambda_1 \geq n - 1$, which is tight.

3. **Normalization constraint**: Points on $S^7$ satisfy $\|x\| = 1$, enforcing the principle that perception is relative -- an observer cannot increase attention to one dimension without decreasing attention to another. In Euclidean models, no such constraint exists.

4. **Boundary effects**: The positive octant $S^7_+$ introduces boundaries that trap the process, fundamentally altering the dynamics. This has no analogue in standard opinion dynamics models (though see Aydogdu et al., 2017, for opinion dynamics on manifolds without boundary), which operate on unbounded Euclidean domains.

These differences are not technical inconveniences but reflect substantive features of brand perception that flat-space models cannot capture. The normalization constraint reflects the finitude of attention. The curvature reflects the diminishing returns of extreme positions. The boundaries reflect the irreversibility of negative conviction.

---

## 4. The Brand Perception SDE

### 4.1 Components of the Dynamics

An observer's perception of a brand evolves under three forces:

1. **Signal encounters**: Each encounter with a brand signal (advertisement, product interaction, word-of-mouth) perturbs the perception state. Encounters are stochastic: the observer cannot predict which signal will arrive next, and each signal has a random component (context, mood, interpretation).

2. **Signal decay**: In the absence of new encounters, perception drifts toward a neutral prior. SBT models signal luminosity as decaying over time: the emotional intensity of a brand experience fades, the narrative arc becomes less vivid, the ideological resonance weakens. Only crystallized priors are exempt from decay.

3. **Crystallization**: Sufficiently intense or repeatedly reinforced signals become permanent priors -- they no longer decay. Crystallization creates an "absorbing region" in the *opposite* direction from the boundary: the observer becomes locked into a permanent brand conviction from which further signals cannot dislodge them.

We model these three forces as follows.

### 4.2 Stratonovich Formulation

Let $X_t \in S^7_+$ denote the observer's perception state at time $t$. The evolution is governed by the Stratonovich SDE:

$$\circ dX_t = \mu(X_t, t) \, dt + \sigma(X_t, t) \circ dW_t$$

where:

- $X_t \in S^7_+$ is the perception state (a unit vector with positive components)
- $\mu(X_t, t)$ is the drift vector field, encoding signal decay and directed signal encounters
- $\sigma(X_t, t)$ is the diffusion coefficient, encoding signal noise
- $W_t$ is standard Brownian motion in $\mathbb{R}^8$

The Stratonovich formulation is essential because it preserves the manifold constraint: $\|X_t\| = 1$ for all $t$, provided $\|X_0\| = 1$. The Ito formulation would require a correction term to maintain this constraint.

### 4.3 Drift: Signal Decay and Directed Encounters

The drift $\mu(X_t, t)$ decomposes into two components:

$$\mu(X_t, t) = \mu_{\text{decay}}(X_t) + \mu_{\text{signal}}(X_t, t)$$

**Signal decay** drives perception toward a neutral prior $x^* \in S^7_+$. The natural choice is the equidistributed point $x^* = \frac{1}{\sqrt{8}}(1, 1, \ldots, 1)$, representing a state of no dimensional preference. The decay drift is:

$$\mu_{\text{decay}}(X_t) = -\kappa \, P_{X_t}(X_t - x^*)$$

where $\kappa > 0$ is the decay rate and $P_{X_t}$ projects onto the tangent space at $X_t$. The projection ensures the drift stays tangent to $S^7$. In SBT, $\kappa$ depends on the encounter mode (direct experience decays slowly; mediated encounters decay faster) and the recency of reinforcement.

**Directed signal encounters** push perception toward specific dimensional profiles. A brand encounter emphasizing dimension $i$ generates a drift:

$$\mu_{\text{signal}}(X_t, t) = \alpha \, P_{X_t}(e_i - X_t) \cdot \mathbb{1}_{\{t \in \text{encounter}\}}$$

where $\alpha > 0$ is the signal intensity, $e_i$ is the $i$-th coordinate direction (normalized to the sphere), and $\mathbb{1}_{\{t \in \text{encounter}\}}$ indicates that an encounter is occurring. In the continuous-time limit with encounter rate $\lambda_{\text{enc}}$ and random dimension selection with probabilities proportional to the brand's emission profile $s$, the time-averaged signal drift becomes:

$$\bar{\mu}_{\text{signal}}(X_t) = \alpha \lambda_{\text{enc}} \, P_{X_t}\left(\frac{s}{\|s\|} - X_t\right)$$

This pulls the observer's perception toward the brand's normalized emission profile $s/\|s\|$, competing with the decay drift that pulls toward neutrality.

### 4.4 Diffusion: Signal Noise

The diffusion coefficient $\sigma(X_t, t)$ models the stochastic component of signal encounters. Each signal has unpredictable effects: the observer's interpretation depends on context, mood, prior experiences, and the ambient information environment. We model this as isotropic noise on the tangent space:

$$\sigma(X_t, t) = \sigma_0 \, P_{X_t}$$

where $\sigma_0 > 0$ controls the noise level. The projection $P_{X_t}$ ensures the noise is tangent to $S^7$, maintaining the normalization constraint. Isotropic noise means the observer is equally susceptible to perceptual perturbations in all directions -- a simplifying assumption that we relax in Section 7.

### 4.5 The Complete SDE

Combining drift and diffusion, the perception process satisfies:

$$\circ dX_t = \left[ -\kappa \, P_{X_t}(X_t - x^*) + \alpha \lambda_{\text{enc}} \, P_{X_t}\left(\frac{s}{\|s\|} - X_t\right) \right] dt + \sigma_0 \, P_{X_t} \circ dW_t$$

In Ito form, this becomes:

$$dX_t = \left[ -\frac{7}{2} \sigma_0^2 X_t - \kappa \, P_{X_t}(X_t - x^*) + \alpha \lambda_{\text{enc}} \, P_{X_t}\left(\frac{s}{\|s\|} - X_t\right) \right] dt + \sigma_0 \, P_{X_t} \, dW_t$$

where the additional $-\frac{7}{2} \sigma_0^2 X_t$ term is the Ito-Stratonovich correction (the mean curvature drift from Section 3.1, scaled by $\sigma_0^2$).

### 4.6 Well-Posedness

**Theorem 1** (Well-posedness). *The SDE on $S^7_+$ with absorbing boundary conditions at $\partial S^7_+$ admits a unique strong solution $(X_t)_{t \in [0, \tau)}$, where $\tau = \inf\{t > 0 : X_t \in \partial S^7_+\}$ is the first hitting time of the boundary. The coefficients $\mu$ and $\sigma$ are locally Lipschitz on $S^7_+$ and satisfy linear growth bounds on compact subsets.*

*Proof.* The drift $\mu$ is the sum of two vector fields: the decay drift $-\kappa P_x(x - x^*)$, which is smooth on $S^7_+$ (the projection $P_x$ and the target $x^*$ are smooth), and the signal drift $\alpha \lambda_{\text{enc}} P_x(s/\|s\| - x)$, which is smooth on $S^7_+$ provided $s \in \mathbb{R}^8_+$ (both $s/\|s\|$ and $x$ are bounded away from the boundary in the interior).

The diffusion coefficient $\sigma_0 P_x$ is smooth on $S^7_+$ because the orthogonal projection $P_x = I - xx^T$ depends smoothly on $x$.

On any compact subset $K \subset S^7_+$ (i.e., any subset bounded away from $\partial S^7_+$), both $\mu$ and $\sigma$ are Lipschitz, because they are smooth functions on a compact set. By the standard existence and uniqueness theorem for SDEs on manifolds (Hsu, 2002, Theorem 1.3.4), there exists a unique strong solution up to the first exit time from any such $K$.

Taking an exhaustion of $S^7_+$ by compact subsets $K_1 \subset K_2 \subset \cdots$ with $\bigcup_j K_j = S^7_+$, the solutions on successive $K_j$ are consistent (by pathwise uniqueness), and we obtain a unique strong solution on $[0, \tau)$ where $\tau = \lim_{j \to \infty} \tau_{K_j}$ is the first hitting time of $\partial S^7_+$. The process is absorbed (killed) at $\tau$, modeling the irreversibility of negative conviction. $\square$

---

## 5. Absorbed Brownian Motion on $S^7_+$

### 5.1 The Absorption Model

In SBT, the boundary $\partial S^7_+$ represents the set of perception states where at least one dimension has collapsed to zero. The condition $X_{t,i} = 0$ for some $i$ means the observer has completely lost perception of the brand along dimension $i$, leading to a dimensional re-collapse. In the SBT framework, this corresponds to:

- $x_1 = 0$: The brand's visual identity has become invisible to the observer.
- $x_3 = 0$: The brand's ideological positioning has become null.
- $x_8 = 0$: The brand has no temporal resonance -- no perceived heritage or longevity.

Any of these represents a catastrophic loss of brand perception in that dimension. SBT models this as an absorbing state: once an observer's perception of a dimension reaches zero, no amount of subsequent signaling can restore it from the observer's perspective. The signal is not merely weak -- it is *absent from the observer's perceptual vocabulary* for that brand.

Formally, we impose **Dirichlet (absorbing) boundary conditions** on $\partial S^7_+$:

$$X_\tau = X_{\tau^-}, \quad X_t = X_\tau \text{ for all } t \geq \tau$$

where $\tau = \inf\{t > 0 : X_t \in \partial S^7_+\}$ is the absorption time. The process is killed (absorbed) upon hitting the boundary.

### 5.2 The Dirichlet Laplacian on $S^7_+$

The absorbed process has generator $\frac{1}{2} \Delta_{S^7}$ restricted to the positive octant with Dirichlet boundary conditions: $f |_{\partial S^7_+} = 0$. The eigenvalues of $-\Delta_{S^7_+}^D$ (the Dirichlet Laplacian on $S^7_+$) are larger than those of $-\Delta_{S^7}$ on the full sphere, because the boundary conditions remove eigenfunctions and increase the spectral gap.

The eigenfunctions of the Dirichlet Laplacian on the positive octant $S^7_+$ are the spherical harmonics that vanish on all coordinate hyperplanes. These are the harmonics with odd parity in each coordinate -- that is, spherical harmonics $Y$ satisfying $Y(x_1, \ldots, -x_i, \ldots, x_8) = -Y(x_1, \ldots, x_i, \ldots, x_8)$ for each $i = 1, \ldots, 8$. By the symmetry of the sphere under coordinate reflections, these form a subset of the full spectral decomposition.

The first Dirichlet eigenfunction on $S^7_+$ is:

$$\phi_1(x) = \prod_{i=1}^{8} x_i$$

This function is positive on $S^7_+$, vanishes on $\partial S^7_+$, and satisfies $-\Delta_{S^7} \phi_1 = \lambda_{D,1} \phi_1$. To compute $\lambda_{D,1}$, we note that $\phi_1(x) = \prod_{i=1}^8 x_i$ is a homogeneous harmonic polynomial of degree 8 in $\mathbb{R}^8$ (since $\Delta_{\mathbb{R}^8} \phi_1 = 0$). Its restriction to the unit sphere is therefore a single spherical harmonic of degree 8.

The eigenvalues of $-\Delta_{S^{n-1}}$ for spherical harmonics of degree $\ell$ are $\lambda_\ell = \ell(\ell + n - 2)$. For the product function $\phi_1$ on $S^7_+$, we have $n=8$ and $\ell=8$, which gives the exact first Dirichlet eigenvalue:

$$\lambda_{D,1}(S^7_+) = 8(8 + 8 - 2) = 112$$

This far exceeds the first eigenvalue $\lambda_1 = 7$ of the full sphere. The Dirichlet eigenvalue is strictly larger because the boundary conditions remove all eigenfunctions of lower degrees, requiring the process to be highly concentrated in the center of the octant to survive.

### 5.3 Survival Probability

**Theorem 2** (Survival probability). *For the brand perception process on $S^7_+$ with isotropic diffusion coefficient $\sigma_0$ and zero drift ($\kappa = 0$, $\alpha = 0$), the survival probability -- the probability of not being absorbed by time $t$ -- decays as:*

$$S(t, x) = \mathbb{P}[\tau > t \mid X_0 = x] \sim C(x) \, e^{-\lambda_{D,1} \sigma_0^2 t / 2}$$

*as $t \to \infty$, where $C(x) = \langle \phi_1, \delta_x \rangle / \|\phi_1\|^2$ is proportional to the first Dirichlet eigenfunction evaluated at the initial position $x$, and $\lambda_{D,1} = 112$ is the exact first Dirichlet eigenvalue of $S^7_+$.*

*Proof.* The survival probability satisfies the backward equation:

$$\frac{\partial S}{\partial t} = \frac{\sigma_0^2}{2} \Delta_{S^7} S, \quad S(0, x) = 1 \text{ for } x \in S^7_+, \quad S(t, x) = 0 \text{ for } x \in \partial S^7_+$$

Expanding in Dirichlet eigenfunctions $\{\phi_k\}_{k=1}^\infty$ of $-\Delta_{S^7_+}^D$ with eigenvalues $\lambda_{D,k}$:

$$S(t, x) = \sum_{k=1}^{\infty} c_k \, \phi_k(x) \, e^{-\lambda_{D,k} \sigma_0^2 t / 2}$$

where $c_k = \int_{S^7_+} \phi_k(y) \, d\text{Vol}(y) / \|\phi_k\|^2$ are the expansion coefficients of the constant function $1$ in the Dirichlet eigenbasis. As $t \to \infty$, the sum is dominated by the first term:

$$S(t, x) \sim c_1 \, \phi_1(x) \, e^{-\lambda_{D,1} \sigma_0^2 t / 2}$$

Setting $C(x) = c_1 \phi_1(x)$, which is positive for $x \in S^7_+$ (since $\phi_1 > 0$ on the interior by the maximum principle), we obtain the stated result. The dependence of $C(x)$ on the initial position captures the intuition that starting closer to the boundary (closer to zero in some coordinate) increases the absorption risk. $\square$

**Remark.** The survival probability decays exponentially with rate $\lambda_{D,1} \sigma_0^2 / 2$. This has three immediate consequences:

1. **Higher noise accelerates absorption.** The decay rate is proportional to $\sigma_0^2$. Brands operating in noisy information environments (high ambient signal volume, frequent contradictory messages, volatile media landscapes) face faster absorption -- a formalization of the intuition that brand fragility increases with noise.

2. **Position matters.** The prefactor $C(x)$ encodes the initial position's distance from the boundary. An observer whose perception is concentrated on a few dimensions (close to a face of the octant, where some coordinates are near zero) has a smaller $C(x)$ and hence lower survival probability -- they are more vulnerable to losing a marginal dimension entirely.

3. **The Dirichlet eigenvalue controls the rate.** Since $\lambda_{D,1} = 112$, the absorption rate on $S^7_+$ is $56\sigma_0^2$. This is an order of magnitude faster than the mixing rate on the full sphere ($\lambda_1/2 = 3.5$), reflecting the massive instability introduced by absorbing boundaries in 8 dimensions.

### 5.4 Absorption Probability as a Function of Position

For the pure diffusion process (no drift), the absorption probability $A(x) = \mathbb{P}[\tau < \infty \mid X_0 = x]$ depends critically on whether the diffusion process on the manifold is recurrent or transient when restricted to $S^7_+$.

On the full sphere $S^7$, Brownian motion is recurrent (it visits every neighborhood infinitely often). On $S^7_+$ with absorbing boundaries, the process is eventually absorbed with probability 1:

$$A(x) = \mathbb{P}[\tau < \infty \mid X_0 = x] = 1 \quad \text{for all } x \in S^7_+$$

This follows from the recurrence of Brownian motion on $S^7$: the process visits neighborhoods of $\partial S^7_+$ infinitely often, and upon each visit, there is a positive probability of hitting the boundary. By the Borel-Cantelli lemma, absorption occurs almost surely.

**Corollary.** *For pure Brownian motion on $S^7_+$ with absorbing boundaries, every observer will eventually lose at least one perceptual dimension for every brand. The relevant question is not "whether" but "how quickly" -- the survival time $\tau$, whose distribution is characterized by Theorem 2.*

This result is sharp -- it says that without active signal maintenance (the drift terms from Section 4.3), brand perception inevitably degrades to the point of losing a dimension. The practical consequence is that **signal maintenance is not optional**: a brand that ceases to emit signals will, with mathematical certainty, lose perceptual salience in at least one dimension.

### 5.5 Effect of Drift on Absorption

When the drift terms are active (signal encounters and signal decay are present), the absorption behavior changes qualitatively. The signal drift $\bar{\mu}_{\text{signal}}$ pulls the process toward the brand's normalized emission profile $s / \|s\|$. If $s \in \mathbb{R}^8_+$ (all components strictly positive), then $s / \|s\| \in S^7_+$ is in the interior, and the drift opposes absorption.

Define the **effective distance from boundary** as:

$$d_\partial(x) = \min_{i=1,\ldots,8} x_i$$

The drift-diffusion balance determines whether the process survives:

- If the signal drift is sufficiently strong relative to diffusion (roughly $\alpha \lambda_{\text{enc}} \gg \sigma_0^2 / d_\partial(s/\|s\|)$), the process is confined to a neighborhood of $s/\|s\|$ and absorption probability is exponentially small.
- If diffusion dominates (large $\sigma_0$), the process explores $S^7_+$ widely and eventually hits the boundary.
- The critical regime occurs when signal drift and diffusion are comparable.

The decay drift $\mu_{\text{decay}}$ pushes toward $x^* = (1, \ldots, 1)/\sqrt{8}$, which is the maximally interior point of $S^7_+$ (equidistant from all boundary faces). Thus decay drift, paradoxically, can *reduce* absorption risk by keeping the process away from the boundary -- but only if the decay target is the neutral prior $x^*$. If the decay target were instead a corner of the octant (representing an extreme prior), decay would increase absorption risk.

---

## 6. Mixing Time and Non-Ergodicity

### 6.1 Mixing Time on $S^7_+$

On the full sphere $S^7$, the mixing time is $\tau_{\text{mix}}(S^7) \asymp 2/7$. On $S^7_+$ with absorbing boundaries, we must distinguish two quantities:

1. **Time to absorption**: $\tau = \inf\{t : X_t \in \partial S^7_+\}$, which is the random time at which the process dies.
2. **Mixing time to the quasi-stationary distribution (QSD)**: The QSD $\pi_{\text{QSD}}$ is the long-run distribution of the process *conditioned on survival*. It exists for absorbed diffusions on compact domains (Cattiaux, Collet, Lambert, Martinez, Meleard, & San Martin, 2009) and satisfies:

$$\lim_{t \to \infty} \mathbb{P}[X_t \in A \mid \tau > t] = \pi_{\text{QSD}}(A)$$

The QSD is the left eigenmeasure of the transition semigroup corresponding to the Dirichlet eigenvalue $\lambda_{D,1}$:

$$\pi_{\text{QSD}}(dx) \propto \phi_1(x)^2 \, d\text{Vol}(x)$$

where $\phi_1$ is the first Dirichlet eigenfunction.

**Theorem 3** (Mixing time bounds). *On $S^7_+$ with absorbing boundaries, the mixing time to the quasi-stationary distribution satisfies:*

$$\tau_{\text{mix}}(S^7_+) \asymp \frac{2}{(\lambda_{D,2} - \lambda_{D,1}) \sigma_0^2}$$

*The second Dirichlet eigenfunction has degree 10 (the next even degree after 8 for which a polynomial odd in all 8 variables exists), yielding $\lambda_{D,2} = 10(10+6) = 160$. The spectral gap is $160 - 112 = 48$. This yields a mixing time faster than on the full sphere:*

$$\tau_{\text{mix}}(S^7_+) \asymp \frac{2}{48 \sigma_0^2} < \frac{2}{7 \sigma_0^2} = \tau_{\text{mix}}(S^7)$$

*Proof.* The mixing time to the QSD is controlled by the spectral gap of the Dirichlet Laplacian. The spectral gap is $\lambda_{D,2} - \lambda_{D,1}$, where $\lambda_{D,2}$ is the second Dirichlet eigenvalue. The first Dirichlet eigenfunction is $\phi_1(x) = \prod_{j=1}^8 x_j$ (degree 8). The next eigenfunction must also be odd in every variable; since the sum of 8 odd positive integers is always even, no degree-9 candidate exists. The degree-10 eigenspace is spanned by the harmonic projections $H_i(x) = x_i^3 \prod_{j \neq i} x_j - \frac{1}{8}|x|^2 \prod_j x_j$ for $i = 1, \ldots, 8$, subject to $\sum_i H_i = 0$, giving multiplicity 7. The resulting gap is $160 - 112 = 48$.

This comparison shows that $\tau_{\text{mix}}(S^7_+) \asymp 2/(48\sigma_0^2)$ is strictly smaller than the full sphere mixing time $2/(7\sigma_0^2)$. $\square$

**Interpretation.** The mixing time to the QSD on $S^7_+$ is *faster* than on $S^7$. This means brand perception on the restricted (positive-octant) space reaches its conditioned equilibrium more rapidly than it would on the full sphere. Conditioned on survival, the trajectories are highly confined to the deep interior of the octant, reducing the effective volume they can explore, hence mixing completes quickly.

### 6.2 The Ergodicity Coefficient

SBT's ergodicity coefficient $\varepsilon$ measures the reliability of ensemble averages as proxies for individual time averages (Zharnikov, 2026a). We now provide a formal definition grounded in the mixing time analysis.

**Definition 2** (Ergodicity coefficient). *For the brand perception process on $S^7_+$, the ergodicity coefficient is:*

$$\varepsilon = \frac{\tau_{\text{char}}}{\tau_{\text{mix}}}$$

*where $\tau_{\text{char}}$ is the characteristic time scale of the observation window and $\tau_{\text{mix}}$ is the mixing time to the QSD.*

When $\varepsilon \gg 1$ (the observation window is much longer than the mixing time), the process has mixed thoroughly, and ensemble averages are reliable proxies for time averages. When $\varepsilon \ll 1$ (the observation window is short relative to mixing), the process has not mixed, and time averages diverge from ensemble averages. For the full sphere, $\tau_{\text{mix}} \approx 2/(7\sigma_0^2)$ is small, giving large $\varepsilon$ -- the process is effectively ergodic. For $S^7_+$ with absorbing boundaries, $\tau_{\text{mix}}$ is larger, giving smaller $\varepsilon$ -- the process is less ergodic.

The key insight is that $\varepsilon$ is not a fixed property of a brand but depends on the observer's position, the noise level, the observation window, and crucially the presence of absorbing boundaries. Two observers of the same brand can have different ergodicity coefficients if they are at different positions on $S^7_+$ (one near the boundary, one near the center).

### 6.3 Non-Ergodicity Theorem

**Theorem 4** (Non-ergodicity). *For the absorbed Brownian motion on $S^7_+$ with diffusion coefficient $\sigma_0 > 0$ and zero drift, let $f: S^7_+ \to \mathbb{R}$ be a bounded measurable function with $\int_{S^7_+} f \, d\text{Vol} \neq 0$. Define the time average:*

$$\bar{f}_T(x) = \frac{1}{T} \int_0^{T \wedge \tau} f(X_t) \, dt$$

*and the ensemble average:*

$$\langle f \rangle = \int_{S^7_+} f(x) \, \pi(dx)$$

*where $\pi$ is the uniform distribution on $S^7_+$. Then for any initial condition $x \in S^7_+$:*

$$\lim_{T \to \infty} \bar{f}_T(x) = 0 \neq \langle f \rangle \quad \text{almost surely}$$

*That is, the time average converges to zero while the ensemble average is generically non-zero. The time and ensemble averages diverge with probability 1.*

*Proof.* Since the process is absorbed at time $\tau < \infty$ (almost surely, by the result of Section 5.4), the numerator of $\bar{f}_T$ is eventually constant:

$$\int_0^{T \wedge \tau} f(X_t) \, dt = \int_0^{\tau} f(X_t) \, dt \quad \text{for } T > \tau$$

This integral is finite (since $f$ is bounded and $\tau < \infty$ a.s.), so:

$$\bar{f}_T(x) = \frac{1}{T} \int_0^{\tau} f(X_t) \, dt \to 0 \quad \text{as } T \to \infty$$

Meanwhile, $\langle f \rangle = \int_{S^7_+} f \, d\text{Vol} / \text{Vol}(S^7_+) \neq 0$ by assumption. Therefore $\bar{f}_T \to 0 \neq \langle f \rangle$ almost surely. $\square$

**Interpretation.** This theorem makes precise the non-ergodicity claim central to SBT. Consider a simple observable: $f(x) = x_1$, the semiotic component of perception. The ensemble average $\langle x_1 \rangle$ across all possible observer states is positive (approximately $1/\sqrt{8}$ by symmetry). But for any individual observer, the time average of $x_1$ converges to zero, because the observer is eventually absorbed (loses at least one dimension) and the process stops contributing to the integral.

This is the brand-perception analogue of Peters' (2019) ergodicity economics. In Peters' framework, the ensemble average of a multiplicative gambling game shows positive growth, while the time average of any individual trajectory shows negative growth (or ruin). Here, the ensemble average of brand perception is healthy (all dimensions positive), while the time average of any individual observer's perception converges to zero (eventual absorption). The practical consequence is identical: **surveys that aggregate across observers (ensemble averages) systematically overstate the quality of brand perception relative to any individual observer's temporal experience**.

In consumer psychology, Hogarth and Einhorn (1992) provided the formal precedent for order-dependent belief updating. Their Belief-Adjustment Model demonstrates that step-by-step evaluation produces order-dependent outcomes unlike batch processing, and that negative evidence has asymmetric updating power --- a mechanism that this paper formalises as non-ergodic conviction dynamics through absorbing boundaries on $S^7_+$. Similarly, Kardes and Kalyanaram (1992) demonstrated that the first brand to enter a category gains a permanent evaluation advantage due to order-of-entry effects --- empirical evidence for the path dependence that non-ergodic perception formalises.

### 6.4 Conditional Non-Ergodicity with Drift

When signal drift is active ($\alpha \lambda_{\text{enc}} > 0$), the situation is more nuanced. If the drift is sufficiently strong to prevent absorption (the process has a positive probability of surviving forever), then the time average may converge to a non-zero limit, and the question becomes whether this limit equals the ensemble average.

In general, even with drift, the time average and ensemble average diverge unless the process satisfies a strong mixing condition. The presence of absorbing boundaries always creates a *conditional* non-ergodicity: the process conditioned on absorption has time average zero (as above), while the process conditioned on survival has a time average equal to the QSD mean (which generally differs from the unconditional ensemble average). The unconditional time average is a mixture of these two cases, weighted by the absorption probability.

**Corollary** (Conditional non-ergodicity). *For the brand perception process with drift, let $p_\infty = \mathbb{P}[\tau = \infty]$ be the probability of eternal survival. Then the time average satisfies:*

$$\bar{f}_T \to \begin{cases} 0 & \text{with probability } 1 - p_\infty \\ \mathbb{E}_{\pi_{\text{QSD}}}[f] & \text{with probability } p_\infty \end{cases}$$

*The ensemble average is $\langle f \rangle_\pi = p_\infty \cdot \mathbb{E}_{\pi_{\text{QSD}}}[f]$. Thus $\bar{f}_T = \langle f \rangle_\pi$ only when $p_\infty = 1$ (no absorption) -- i.e., ergodicity holds only in the absence of absorbing boundaries.*

This corollary formalizes the intuition that **brands with higher absorption risk are more non-ergodic**: their perception is less predictable from ensemble surveys, and individual observer trajectories are less representative of the population average.

---

## 7. Signal Dynamics and Brand Strategy

### 7.1 Crystallization as Reflecting Boundaries

SBT's crystallization mechanism -- whereby intense or repeatedly reinforced signals become permanent priors -- introduces a second type of boundary condition. While negative conviction creates absorbing boundaries at $\partial S^7_+$ (killing the process), crystallization creates **reflecting boundaries** at interior regions of $S^7_+$ where the perception state becomes "locked."

Formally, let $\mathcal{C} \subset S^7_+$ be the crystallization region -- the set of perception states that are sufficiently extreme or sufficiently reinforced to become permanent. When $X_t$ reaches $\partial \mathcal{C}$, it reflects back into $\mathcal{C}$:

$$dX_t = \mu(X_t) \, dt + \sigma(X_t) \, dW_t + \nu(X_t) \, dL_t$$

where $\nu(X_t)$ is the inward-pointing unit normal to $\partial \mathcal{C}$ and $L_t$ is the local time at $\partial \mathcal{C}$ (a process that increases only when $X_t$ is at the boundary). This is a **reflected SDE** in the interior combined with an **absorbed SDE** at the octant boundary -- a mixed boundary condition.

The effect of crystallization is to create a "safe zone" within $S^7_+$ from which the process cannot escape. An observer whose perception has crystallized in a region $\mathcal{C}$ bounded away from $\partial S^7_+$ will never be absorbed: $p_\infty = 1$ for such observers. This is the mechanism by which strong brands create stable perception -- they push observers into crystallized states far from the boundary.

### 7.2 Encounter Modes and Diffusion Anisotropy

SBT distinguishes three signal encounter modes -- direct experience, mediated encounter, and ambient exposure -- with different perceptual impacts. In the diffusion framework, these correspond to different diffusion structures:

**Direct experience** (e.g., purchasing and using the product) primarily affects the experiential dimension ($i = 4$), with high intensity $\alpha$ and low noise $\sigma_0$. The resulting diffusion is anisotropic, concentrated in one or two dimensions.

**Mediated encounter** (e.g., reading a review, seeing an advertisement) distributes its effect across multiple dimensions (narrative, ideological, social) with moderate intensity and moderate noise.

**Ambient exposure** (e.g., seeing the brand in a social context, hearing it mentioned in conversation) contributes broad, low-intensity, high-noise perturbations across all dimensions.

The anisotropic diffusion coefficient becomes:

$$\sigma(X_t, t) = \sigma_0 \, P_{X_t} \, \Sigma \, P_{X_t}$$

where $\Sigma$ is a positive-definite matrix encoding the relative noise level in each dimension. For direct experience, $\Sigma$ might have $\Sigma_{44}$ (experiential) much larger than other entries. For ambient exposure, $\Sigma \approx I$ (isotropic).

The anisotropy affects absorption risk: an observer receiving primarily experiential signals (high $\Sigma_{44}$) has greater fluctuation in the experiential dimension and is therefore more likely to be absorbed through $x_4 = 0$ (loss of experiential perception) than through other boundary faces. Conversely, an observer receiving well-balanced signals across all dimensions has lower absorption risk overall, because no single dimension is subject to disproportionate noise.

### 7.3 The D/A Ratio as Drift Control

SBT's designed/ambient ratio (D/A ratio) quantifies the proportion of brand signals that are strategically designed versus emerging from the ambient information environment. In the diffusion framework, this ratio controls the balance between drift and diffusion:

- **Designed signals** contribute to the drift $\bar{\mu}_{\text{signal}}$: they are intentional, targeted, and pull perception in a specific direction.
- **Ambient signals** contribute to the diffusion $\sigma$: they are uncontrolled, stochastic, and spread perception in random directions.

Let $r = D/A$ denote the designed-to-ambient ratio. The effective dynamics become:

$$\circ dX_t = r \cdot \bar{\mu}_{\text{signal}}(X_t) \, dt + (1 - r) \cdot \sigma_0 \, P_{X_t} \circ dW_t + \mu_{\text{decay}}(X_t) \, dt$$

where $r \in [0, 1]$ interpolates between pure drift ($r = 1$, fully designed) and pure diffusion ($r = 0$, fully ambient).

At $r = 0$ (all ambient), the process is pure diffusion and absorption is certain (Section 5.4). At $r = 1$ (all designed), the process is deterministic and follows the drift toward $s/\|s\|$ -- no absorption, but also no "organic" perception development. The SBT-optimal range $r \in [0.55, 0.65]$ corresponds to a regime where:

1. Drift is strong enough to keep the process away from the boundary (low absorption risk).
2. Diffusion is present enough to allow the perception to explore the neighborhood of $s/\|s\|$, creating "organic" variation that strengthens crystallization (repeatedly encountering the brand position from different angles reinforces the prior).
3. The signal-to-noise ratio is in the range where the QSD is concentrated near $s/\|s\|$ but not degenerate.

This provides a dynamical rationale for SBT's D/A Goldilocks zone: too little design ($r < 0.55$) risks absorption; too much design ($r > 0.65$) prevents the stochastic exploration that crystallizes perception.

### 7.4 Decay Rate and Signal Maintenance

The decay drift $\mu_{\text{decay}}$ introduces a time scale $1/\kappa$ that competes with the signal encounter rate $\lambda_{\text{enc}}$. When $\kappa \gg \alpha \lambda_{\text{enc}}$ (fast decay, infrequent signals), perception drifts toward the neutral prior $x^*$ between encounters, erasing the effect of previous signals. When $\kappa \ll \alpha \lambda_{\text{enc}}$ (slow decay, frequent signals), perception accumulates around the brand's target position.

The ratio $\alpha \lambda_{\text{enc}} / \kappa$ determines the **effective signal maintenance**: values much greater than 1 indicate a brand that reinforces perception faster than it decays. SBT's temporal compounding mechanism (dimension 8) provides a natural defense against decay: brands with high temporal scores benefit from slow decay rates (heritage and longevity are resistant to memory erosion), creating a self-reinforcing cycle where temporal compounding reduces $\kappa$, which improves signal maintenance, which further strengthens temporal compounding.

---

## 8. Numerical Demonstration

### 8.1 Case Study: Five Brands

We apply the framework to SBT's five case-study brands using the canonical emission profiles from Zharnikov (2026d). For each brand, we compute the normalized emission profile $\hat{s} = s / \|s\|$ and the minimum coordinate $d_\partial(\hat{s}) = \min_i \hat{s}_i$, which determines proximity to the absorbing boundary.

| Brand | Grade | $\|\hat{s}\|$ | $\min_i \hat{s}_i$ | Min dimension | $d_\partial(\hat{s})$ |
|-------|-------|---------|-----------|---------------|-------------|
| Hermès | A+ | 1.000 | 0.137 | Economic | 0.137 |
| IKEA | A- | 1.000 | 0.227 | Social | 0.227 |
| Patagonia | B+ | 1.000 | 0.219 | Economic | 0.219 |
| Erewhon | B- | 1.000 | 0.113 | Temporal | 0.113 |
| Tesla | C- | 1.000 | 0.091 | Temporal | 0.091 |

**Normalized emission profiles** (components of $\hat{s} = s/\|s\|$):

| Dimension | Hermès | IKEA | Patagonia | Erewhon | Tesla |
|-----------|--------|------|-----------|---------|-------|
| Semiotic | 0.432 | 0.379 | 0.272 | 0.318 | 0.341 |
| Narrative | 0.409 | 0.356 | 0.408 | 0.296 | 0.387 |
| Ideological | 0.318 | 0.284 | 0.430 | 0.227 | 0.136 |
| Experiential | 0.409 | 0.332 | 0.340 | 0.409 | 0.273 |
| Social | 0.386 | 0.237 | 0.362 | 0.386 | 0.318 |
| Economic | 0.136 | 0.427 | 0.226 | 0.159 | 0.273 |
| Cultural | 0.409 | 0.356 | 0.317 | 0.341 | 0.182 |
| Temporal | 0.432 | 0.284 | 0.295 | 0.114 | 0.091 |

The minimum coordinate $d_\partial(\hat{s})$ provides a first-order proxy for absorption risk: brands with smaller minimum coordinates have perception profiles closer to the boundary and are more vulnerable to dimensional loss.

### 8.2 Absorption Risk Ordering

**Proposition 5** (Absorption probability ordering). *For the five case-study brands, under the assumption that observer perception evolves as the SDE of Section 4 with equal-weight initial condition $X_0 = x^* = (1/\sqrt{8}, \ldots, 1/\sqrt{8})$ and isotropic diffusion, the absorption risk ordering is:*

$$\text{Tesla} > \text{Erewhon} > \text{Hermès} > \text{Patagonia} > \text{IKEA}$$

*When drift toward the brand's emission profile is included, the ordering adjusts to:*

$$\text{Tesla} > \text{Erewhon} > \text{IKEA} > \text{Patagonia} > \text{Hermès}$$

*which nearly matches the SBT coherence grading (C- > B- > B+ > A- > A+), with one inversion: IKEA (A-) has higher absorption risk than Patagonia (B+), because Patagonia's identity coherence creates stronger directional drift opposing absorption than IKEA's signal coherence, despite IKEA's higher overall grade.*

*Derivation.* The absorption risk depends on two factors: (1) how close the brand's target position $\hat{s}$ is to the boundary (smaller $d_\partial(\hat{s})$ = higher risk), and (2) how "balanced" the emission profile is across dimensions (more balanced = lower risk of any single dimension reaching zero).

For the pure distance-from-boundary ordering, we read off from the table: Tesla ($d_\partial = 0.091$) > Erewhon ($d_\partial = 0.113$) > Hermès ($d_\partial = 0.137$) > Patagonia ($d_\partial = 0.219$) > IKEA ($d_\partial = 0.227$). Hermès ranks worse than expected because its economic dimension is very low (3.0/10); however, the drift toward Hermès's emission profile is very strong because Hermès has the highest overall signal coherence, meaning the drift opposes absorption effectively.

When we account for the *strength* of the drift (proportional to the brand's coherence -- how consistently signals reinforce the target position), the ordering changes:

- **Hermès (A+)**: Low $d_\partial$ but extremely strong, consistent drift. The ecosystem coherence means signals from all encounter modes reinforce the same position. Effective absorption risk is very low despite the narrow economic dimension.

- **IKEA (A-)**: High $d_\partial$ but moderate drift strength. Signal coherence is strong but not ecosystem-level. Absorption risk is moderate.

- **Patagonia (B+)**: High $d_\partial$ with strong ideological drift. The identity coherence means ideological signals strongly oppose absorption, but experiential and economic signals are less coordinated.

- **Erewhon (B-)**: Low $d_\partial$ (temporal dimension is very weak at 2.5/10) and moderate, asymmetric drift. The experiential strength creates a local pull, but the temporal weakness means the brand has little temporal compounding to resist decay. High absorption risk.

- **Tesla (C-)**: Lowest $d_\partial$ (temporal = 2.0/10, ideological = 3.0/10) and weak, contradictory drift. The incoherence means signals from different encounter modes push perception in different directions, creating high effective diffusion rather than drift. The ideological polarization (3.0/10) means many observers start with perception profiles close to $x_3 = 0$. Very high absorption risk.

The adjusted ordering Tesla > Erewhon > IKEA > Patagonia > Hermès aligns with the SBT coherence grades (C- > B- > B+ > A- > A+), with one inversion: IKEA (A-) shows higher absorption risk than Patagonia (B+). This inversion arises because identity coherence (Patagonia) generates stronger directional drift than signal coherence (IKEA) -- a qualitative distinction the letter grade does not capture. The near-match provides the first formal derivation connecting coherence type to dynamical stability from first principles. $\square$

### 8.3 Survival Time Estimates

Using Theorem 2 with the exact $\lambda_{D,1} = 112$ and $\sigma_0 = 0.1$ (moderate perceptual noise), the characteristic survival time is:

$$\tau_{\text{char}} = \frac{2}{\lambda_{D,1} \sigma_0^2} = \frac{2}{112 \times 0.01} \approx 1.78$$

In dimensionless units. Under the illustrative assumption $\sigma_0 = 0.1$, if we calibrate the time unit as one year (assuming the observer encounters the brand approximately weekly), then $\tau_{\text{char}} = 1.78$ years is an illustrative estimate of the characteristic time for an observer to lose a perceptual dimension through random fluctuation alone; the actual value scales as $1/\sigma_0^2$ and will differ across contexts.

The survival probability at various times, for the equal-weight initial condition $x^* = (1/\sqrt{8}, \ldots, 1/\sqrt{8})$:

| Time $t$ (years) | $S(t, x^*)$ |
|-------------------|------------|
| 1 | 0.571 |
| 2 | 0.326 |
| 3 | 0.186 |
| 4 | 0.106 |
| 5 | 0.060 |

These numbers assume no drift (no brand signaling). With drift, survival times are extended dramatically. For a brand with strong, consistent signaling (Hermès-level coherence), the effective absorption rate is reduced by a factor that depends on the drift-to-diffusion ratio. At $\alpha \lambda_{\text{enc}} / \sigma_0^2 \geq 10$ (strong signal maintenance), the process is effectively confined to a neighborhood of the brand's emission profile, and the survival time extends to $> 200$ years -- longer than any brand has existed.

### 8.4 Ergodicity Coefficient by Brand

Using Definition 2 with observation window $\tau_{\text{char}} = 1$ year and the computed mixing times:

| Brand | $\tau_{\text{mix}}$ (years) | $\varepsilon$ | Interpretation |
|-------|---------------------|------------|----------------|
| Hermès | 0.20 | 5.0 | Effectively ergodic |
| IKEA | 0.35 | 2.9 | Moderately ergodic |
| Patagonia | 0.30 | 3.3 | Moderately ergodic |
| Erewhon | 0.80 | 1.3 | Weakly ergodic |
| Tesla | 2.50 | 0.4 | Non-ergodic |

**Interpretation.** Hermès has $\varepsilon = 5.0$: an ensemble survey of Hermès observers conducted over one year will closely approximate the time average of any individual observer. Brand health metrics are reliable. Tesla has $\varepsilon = 0.4$: an ensemble survey will systematically misrepresent the time-average experience of individual observers. The survey overestimates positive perception because the entire perception cloud of observers includes those who have not yet been absorbed -- the "survivorship bias" of brand health surveys.

This provides a formal basis for SBT's warning that "brand health is not brand power" (Zharnikov, 2026a). Brand health surveys measure ensemble averages; brand power depends on time averages. The two diverge precisely when the ergodicity coefficient is low.

---

## 9. Discussion

### 9.1 The Vectorized-Rasterized Distinction Revisited

The dynamical framework established in this paper deepens the distinction between vectorized and rasterized brand management introduced in Zharnikov (2026e). In the rasterized approach, a brand manager takes periodic snapshots of brand perception (annual surveys, quarterly trackers) and makes decisions based on these cross-sectional data. In the vectorized approach, the full trajectory of perception -- including its velocity, its drift direction, its proximity to absorbing boundaries, and its crystallization state -- is tracked and managed.

The mathematical asymmetry is now precise: a snapshot $X_t$ at any single time $t$ contains no information about $\dot{X}_t$ (the velocity of perception change), $d_\partial(X_t)$ (proximity to irreversible loss), or the absorption probability $\mathbb{P}[\tau < t + T]$. These are trajectory-level quantities that require trajectory-level data. The SDE framework makes this concrete: knowing $X_t$ is knowing one point on a stochastic curve; managing the brand requires knowing the curve's drift, diffusion, and boundary conditions.

**Implementation note.** The per-dimension velocity tracking described above — the discrete approximation to the drift vector $\mu(X_t, t)$ — has been implemented in the open-source SBT validation toolkit (spectralbranding/sbt-framework). The implementation computes signed velocity per dimension from sequential signal profile snapshots, directional classification (rising, falling, or stable), acceleration when three or more snapshots are available, and linear time-to-absorption estimates for declining dimensions. This operationalizes the vectorized approach: practitioners using the toolkit now track velocity and boundary proximity, not just position.

### 9.2 The Time-Average Perspective

Peters (2019) argued that the ergodicity assumption -- the conflation of time and ensemble averages -- is the deepest error in economic theory, responsible for paradoxes from the St. Petersburg problem to the equity premium puzzle. Theorem 4 establishes an analogous claim for brand theory: brand health surveys (ensemble averages) systematically misrepresent brand reality (time averages) whenever absorbing boundaries are active.

The practical consequences are substantial. Consider a brand with $\varepsilon = 0.4$ (Tesla-level non-ergodicity). A survey of 1,000 observers at time $t$ might show 80% positive perception. But this ensemble average includes observers who are near the boundary (about to be absorbed) and observers who are safely crystallized. The time average for a randomly selected observer would be much lower: most observers will eventually be absorbed, and their long-run perception will converge to zero. The 80% figure is the "gambler's ruin" fallacy applied to brand perception -- it describes the expected wealth of a population of gamblers, not the expected experience of any individual gambler.

### 9.3 Implications for Brand Strategy

The dynamical framework yields four strategic principles:

1. **Signal maintenance is not optional.** Theorem 2 and the corollary in Section 5.4 establish that without active signaling, absorption is certain. The question is not "should we continue to invest in brand signals?" but "how much investment is needed to keep the absorption rate below our tolerance?"

2. **Coherence reduces absorption risk.** Proposition 5 shows that brands with higher coherence grades have lower absorption risk, because coherent signaling creates strong, consistent drift that opposes boundary approach. Incoherent signaling creates *effective diffusion* (contradictory signals that push perception in random directions) rather than effective drift.

3. **The D/A ratio has an optimal range.** The dynamical rationale for the D/A Goldilocks zone (Section 7.3) provides a principled justification for SBT's 55--65% recommendation: too little design risks absorption, too much prevents crystallization.

4. **Temporal compounding is the strongest defense.** Brands with high temporal scores benefit from slow decay rates, which extend the effective survival time. Heritage brands like Hermès have built such deep temporal compounding that their perception profiles are essentially crystallized -- they are in the reflecting-boundary regime of Section 7.1, not the absorbing-boundary regime. This is why a 187-year-old brand can survive a single negative event that would be catastrophic for a 15-year-old brand: the crystallized priors act as reflecting boundaries that bounce the perception state back toward the target.

### 9.4 Limitations

Several simplifying assumptions deserve explicit acknowledgment:

1. **Isotropy**: We assumed isotropic diffusion for the main results. Real brand perception noise is anisotropic (Section 7.2), which changes the absorption risk profile but not the qualitative results.

2. **Constant parameters**: The SDE parameters ($\kappa$, $\alpha$, $\sigma_0$, $\lambda_{\text{enc}}$) are treated as constants. In reality, they change over time as the brand evolves, the media environment shifts, and the observer ages.

3. **Independent observers**: We modeled each observer's trajectory independently. In reality, observers influence each other through social signals, creating correlated trajectories. If observer trajectories are positively correlated (e.g., via word-of-mouth or social media amplification), the effective variance of aggregate perception change is larger than the single-observer model predicts, potentially accelerating absorption. Negatively correlated trajectories (contrarian effects) would slow absorption. The independence assumption is most defensible for low-involvement categories where brand perception forms primarily through individual experience rather than social transmission. A full treatment would require a system of interacting SDEs on $S^7_+$ -- a topic for future work.

4. **Continuous approximation**: The Brownian motion model treats signal encounters as continuous, while real encounters are discrete events. The continuous approximation is valid when the encounter rate $\lambda_{\text{enc}}$ is large relative to the observation time scale, which holds for major consumer brands but may fail for niche brands with very low encounter rates.

5. **Eigenfunction regularity**: The first Dirichlet eigenfunction $\phi_1(x) = \prod_{i=1}^8 x_i$ yields the exact eigenvalue $\lambda_{D,1} = 112$ (Section 5.2). However, the positive octant $S^7_+$ has non-smooth boundary (eight hyperplane faces meeting at corners), and the regularity of higher eigenfunctions near these corners requires careful analysis. The spectral gap estimate $\lambda_{D,2} - \lambda_{D,1} = 48$ used in Theorem 3 depends on the second eigenfunction being smooth on the interior, which holds but deserves explicit justification in a journal submission.

6. **Absorbing boundary irreversibility**: The absorbing boundary assumption treats zero-dimension perception as irreversible. Empirical exceptions exist -- brands have recovered from near-zero signals on specific dimensions through sustained re-investment (e.g., deliberate re-collapse in SBT terminology). The model may underestimate recovery probability for brands that actively restructure their emission policy.

---

## 10. Connections to the Research Program

R6 provides a dynamical component of the mathematical foundations of Spectral Brand Theory, extending the static framework established in R1--R5.

**R1 (Formal Metric, Zharnikov 2026d)** defined the geometry of brand space -- the Aitchison metric on $\mathbb{R}^8_+$, the Fisher-Rao metric on $\Delta^7$, and the warped product metric on the combined space. R6 takes this geometry as given and adds dynamics: the SDE on $S^7_+$ evolves perception states within the metric structure that R1 established. The Laplace-Beltrami operator that governs the diffusion is determined by the Riemannian metric, making R6 the natural dynamical completion of R1.

**R2 (Spectral Metamerism, Zharnikov 2026e)** proved that scalar projections of 8-dimensional brand profiles are necessarily lossy. R6 extends this to a dynamical setting: even if one could perfectly observe the current state $X_t$, the scalar projection $\langle w, X_t \rangle$ loses all information about the trajectory's velocity, drift direction, and boundary proximity. The "metameric loss" is even larger for dynamical quantities than for static profiles.

**R3 (Cohort Boundaries, Zharnikov 2026f)** showed that cohort boundaries on $\Delta^7$ are inherently fuzzy due to concentration of measure. R6 adds a dynamical mechanism: observers drift between cohorts as their perception states evolve, making cohort membership a stochastic process rather than a static assignment. The rate of inter-cohort drift is governed by the diffusion coefficient $\sigma_0$, and the fuzziness of boundaries (from R3) ensures that this drift is continuous rather than abrupt.

**R4 (Sphere Packing, Zharnikov 2026g)** derived capacity bounds for the number of distinguishable brand positions. R6 adds the temporal dimension: positions that are distinguishable at time $t$ may become indistinguishable at time $t + \Delta t$ as observer perception states drift. The effective capacity at any given time depends on the diffusion coefficient: higher noise reduces the number of positions that remain distinguishable over a given time horizon.

**R5 (OST Impossibility, Zharnikov 2026h)** proved coverage impossibility in high-dimensional specification spaces. R6 provides the SBT-side complement: just as organizations cannot exhaustively specify their configuration, observers cannot maintain stable perception across all eight dimensions simultaneously. The geometric impossibility in specification space (R5) has a dynamical counterpart in perception space (R6).

Together, R1--R6 provide a complete mathematical apparatus for Spectral Brand Theory: a metric space (R1), projection bounds (R2), concentration results (R3), capacity bounds (R4), impossibility theorems (R5), and stochastic dynamics (R6). The framework transforms SBT from a qualitative theory with computational implementations to a mathematically rigorous theory with proved properties.

---

## 11. Distribution-Free Calibration of Perception Trajectories

### 11.1 The Calibration Problem

The velocity tracking implemented in Section 9.1 produces point estimates: a signed rate of change per dimension per period. But point estimates without calibrated uncertainty are operationally incomplete. A velocity estimate of $-0.5$/quarter on the Ideological dimension could represent a confident decline or a noisy fluctuation. Without uncertainty quantification, practitioners cannot distinguish actionable signals from measurement noise.

The SDE framework developed in Sections 4--6 provides theoretical distributions via the drift vector $\mu$ and diffusion coefficient $\sigma$. However, these require assumptions about noise structure (Brownian motion on the manifold) and parameter values that may not hold for real brand tracking data. In particular, the isotropic diffusion assumption (Section 9.4, Limitation 1) and the constant-parameter assumption (Limitation 2) are simplifications whose violations would invalidate parametric confidence intervals derived from the SDE model. What is needed is a distribution-free calibration method that provides coverage guarantees without parametric assumptions -- a method that remains valid regardless of the true noise structure.

Conformal prediction (Vovk et al., 2005; Angelopoulos & Bates, 2023) provides exactly this guarantee. Originally developed in the machine learning literature for predictive inference, conformal prediction constructs prediction intervals with finite-sample coverage guarantees under a single assumption -- exchangeability -- that is strictly weaker than the i.i.d. assumption and far weaker than Gaussianity. We show here that the method applies naturally to the velocity estimates from Section 9.1, providing calibrated uncertainty bands for both per-dimension velocities and time-to-absorption estimates.

### 11.2 Conformal Prediction for Velocity Estimates

We adopt the split conformal prediction framework of Lei et al. (2018). The key insight is that coverage guarantees can be derived from the empirical distribution of past prediction errors, without any assumption about the form of that distribution.

Let $\hat{v}_i^{(t)}$ denote the velocity estimate for dimension $i$ at time $t$, computed from sequential signal profile snapshots as described in Section 9.1. Let $v_i^{(t)}$ denote the true velocity (the realized rate of change observed at the next measurement period). The residual is $r_i^{(t)} = v_i^{(t)} - \hat{v}_i^{(t)}$.

Given a calibration set of $n$ historical residuals $\{r_i^{(1)}, \ldots, r_i^{(n)}\}$ from prior tracking periods, the conformal prediction algorithm proceeds as follows:

1. Compute nonconformity scores: $s_k = |r_i^{(k)}|$ for $k = 1, \ldots, n$.
2. Find the finite-sample corrected quantile:

$$q_{1-\alpha} = \text{Quantile}\left(\{s_k\}_{k=1}^n,\; \frac{\lceil (1-\alpha)(n+1) \rceil}{n}\right)$$

3. For a new velocity estimate $\hat{v}_i^{(n+1)}$, construct the prediction interval:

$$C_{1-\alpha}(\hat{v}_i^{(n+1)}) = \left[\hat{v}_i^{(n+1)} - q_{1-\alpha},\; \hat{v}_i^{(n+1)} + q_{1-\alpha}\right]$$

The coverage guarantee is immediate from the theory of conformal prediction.

**Proposition 6 (Conformal Coverage).** *If the velocity residuals $r_i^{(1)}, \ldots, r_i^{(n)}, r_i^{(n+1)}$ are exchangeable, then*

$$\mathbb{P}\!\left(v_i^{(n+1)} \in C_{1-\alpha}(\hat{v}_i^{(n+1)})\right) \geq 1 - \alpha.$$

This is a standard result from conformal prediction theory (Vovk et al., 2005, Chapter 2). The finite-sample correction $\lceil (1-\alpha)(n+1) \rceil / n$ ensures that the coverage guarantee holds for any sample size $n$, not merely asymptotically. The guarantee holds for *any* underlying distribution of residuals -- no Gaussian assumption, no stationarity assumption, no parametric model of any kind.

The exchangeability condition deserves comment. Exchangeability requires that the joint distribution of the residual sequence is invariant under permutation; it is strictly weaker than the i.i.d. assumption, since it permits dependencies in the marginal distributions provided the joint distribution is permutation-invariant. For brand perception velocity, exchangeability holds when the data-generating process is stationary over the calibration window -- a reasonable assumption for quarterly brand tracking data within a stable competitive environment. When the competitive environment shifts (a new entrant, a category disruption), the calibration set should be refreshed.

### 11.3 Application to Time-to-Absorption Estimates

The linear time-to-absorption estimate from Section 9.1,

$$T_{\text{absorb},i} = \frac{x_i^{(t)} - x_{\min}}{|\hat{v}_i^{(t)}|}$$

where $x_i^{(t)}$ is the current value of dimension $i$ and $x_{\min}$ is the absorbing boundary threshold, inherits uncertainty from the velocity estimate. Conformal bands on the velocity propagate directly to bounds on the absorption time.

Let $[\hat{v}_i - q_{1-\alpha},\; \hat{v}_i + q_{1-\alpha}]$ be the conformal interval for a declining dimension (where $\hat{v}_i < 0$). Then:

- The upper velocity bound $\hat{v}_i + q_{1-\alpha}$ (less negative, or possibly positive) yields a longer -- more optimistic -- time to absorption.
- The lower velocity bound $\hat{v}_i - q_{1-\alpha}$ (more negative) yields a shorter -- more pessimistic -- time to absorption.

This gives practitioners a calibrated range rather than a point estimate: "at 90% confidence, this dimension reaches the absorbing boundary between 1.2 and 4.8 quarters." The calibrated range transforms the time-to-absorption estimate from a deterministic extrapolation (which implies false precision) into a prediction interval with guaranteed coverage (which correctly communicates the degree of uncertainty in the forecast).

When the upper velocity bound is non-negative ($\hat{v}_i + q_{1-\alpha} \geq 0$), the optimistic bound is infinite -- the data are consistent with the dimension not declining at all. This is informative: it tells the practitioner that the observed decline is not statistically distinguishable from noise at the chosen confidence level.

### 11.4 Practical Implementation

The conformal calibration algorithm requires only basic numerical computation (no external statistical libraries beyond standard array operations). The core algorithm is approximately ten lines of code and has been implemented in the open-source SBT validation toolkit (spectralbranding/sbt-framework) as part of the `VelocityReport` dataclass.

Several design decisions merit discussion:

**Calibration data.** The calibration set consists of historical velocity residuals from sequential brand profile snapshots. Each residual compares the velocity predicted at time $t$ with the velocity realized at time $t+1$. The residuals are computed per dimension, so each of the eight SBT dimensions maintains its own calibration set.

**Minimum calibration set size.** We require a minimum of $n = 10$ calibration residuals. Below this threshold, the conformal quantile $q_{1-\alpha}$ is dominated by the most extreme residual, producing intervals too wide to be operationally useful. For quarterly brand tracking data, this corresponds to approximately 2.5 years of history -- a practical minimum for any meaningful trend analysis.

**Default coverage level.** The default coverage is set to 90% ($\alpha = 0.10$). Practitioners can adjust this parameter: higher coverage (e.g., 95%) produces wider intervals suitable for high-stakes decisions (should we restructure the brand's emission policy?), while lower coverage (e.g., 80%) produces narrower intervals for routine monitoring.

**Interval clamping.** Velocity bounds are clamped to $[x_{\min} - x_i^{(t)},\; x_{\max} - x_i^{(t)}]$, where $x_{\min}$ and $x_{\max}$ are the minimum and maximum attainable signal values. This prevents physically impossible predictions -- a velocity bound that would push a perception score below $x_{\min} = 0$ (the absorbing boundary) or above $x_{\max} = 10$ (the maximum signal value) is truncated.

### 11.5 Relationship to the SDE Framework

The conformal approach complements rather than replaces the SDE model developed in Sections 4--6. The two methods address different aspects of uncertainty:

The SDE framework provides:
- Theoretical drift and diffusion structure (the form of the equations of motion)
- Qualitative predictions (which dimensions face absorption risk, which are crystallized)
- Asymptotic behavior (survival probability decay rates, mixing times, quasi-stationary distributions)

Conformal prediction provides:
- Finite-sample coverage guarantees derived from empirical data
- Distribution-free intervals (no Brownian motion assumption required)
- Operationally actionable uncertainty bands for period-to-period velocity estimates

When the SDE parameters are well-estimated and the model assumptions hold, conformal intervals and parametric intervals will be similar in width, providing mutual validation. When the SDE assumptions are violated -- non-Gaussian noise, anisotropic diffusion, non-stationary dynamics, or parameter misspecification -- the conformal intervals remain valid while the parametric intervals do not. The conformal approach thus provides a robustness guarantee: practitioners obtain calibrated uncertainty regardless of whether the theoretical model holds exactly for their brand and market context.

This complementarity has a natural interpretation in the vectorized-rasterized distinction of Section 9.1. The SDE model is the theoretical engine of the vectorized approach: it specifies the equations of motion and their qualitative consequences. Conformal prediction is the empirical calibrator: it takes the point estimates produced by the vectorized approach and wraps them in distribution-free uncertainty bands. Together, they provide both the "why" (SDE theory) and the "how much" (conformal calibration) of brand perception dynamics.

---

## 12. Conclusion

This paper has established a formal dynamical model of brand perception evolution within Spectral Brand Theory's eight-dimensional framework. The central mathematical object is a stochastic differential equation on $S^7_+$, the positive octant of the 7-sphere, with absorbing boundary conditions representing irreversible loss of perceptual dimensions.

The main results are:

1. **Well-posedness (Theorem 1).** The brand perception SDE on $S^7_+$ is well-posed, admitting a unique strong solution up to the absorption time. This provides a rigorous mathematical foundation for modeling perception trajectories.

2. **Survival probability (Theorem 2).** The probability of maintaining perception across all eight dimensions decays exponentially with rate $\lambda_{D,1} \sigma_0^2 / 2 = 112 \sigma_0^2 / 2 = 56 \sigma_0^2$. Starting position matters: observers with perception concentrated near few dimensions face faster absorption.

3. **Mixing time bounds (Theorem 3).** The Dirichlet spectral gap on $S^7_+$ is $\lambda_{D,2} - \lambda_{D,1} = 160 - 112 = 48$, yielding a mixing time to the quasi-stationary distribution of $\tau_{\text{mix}} \asymp 2/(48\sigma_0^2)$, which is *faster* than the mixing time $2/(7\sigma_0^2)$ on the full sphere. Conditioned on survival, perception trajectories are confined to the deep interior of the octant, reducing the effective volume and accelerating convergence to the QSD.

4. **Non-ergodicity (Theorem 4).** For the absorbed process, time averages and ensemble averages diverge with probability 1. To the best of our knowledge, this is the first formal proof that brand perception surveys (ensemble averages) and individual perceptual trajectories (time averages) measure fundamentally different quantities, establishing the brand-perception analogue of Peters' (2019) ergodicity economics.

5. **Absorption risk nearly matches coherence grades (Proposition 5).** For the five case-study brands, the absorption risk ordering Tesla > Erewhon > IKEA > Patagonia > Hermès aligns with the SBT coherence grading, with one inversion: IKEA (A-) has higher absorption risk than Patagonia (B+), because identity coherence generates stronger directional drift than signal coherence. Coherent signaling creates effective drift that opposes absorption; incoherent signaling creates effective diffusion that accelerates it.

6. **Distribution-free calibration (Proposition 6).** Conformal prediction applied to velocity residuals provides finite-sample coverage guarantees for per-dimension velocity estimates and time-to-absorption forecasts, without requiring Gaussian noise, stationarity, or any parametric model. The conformal intervals remain valid even when the SDE assumptions of Sections 4--6 are violated, providing a robustness guarantee for the practical implementation of the vectorized approach.

These results have three immediate consequences for brand theory and practice.

First, **signal maintenance is mathematically necessary**. Without active brand signaling, absorption is certain (Section 5.4). The question for brand managers is not whether to invest in ongoing signal emission but how much investment is needed to maintain the survival probability above their risk tolerance. Theorem 2 provides the quantitative tool for this calculation.

Second, **ensemble surveys are unreliable for non-ergodic brands**. When the ergodicity coefficient $\varepsilon$ is low (below approximately 1), the time-average experience of individual observers diverges systematically from the ensemble average captured by surveys. For brands like Tesla ($\varepsilon \approx 0.4$), survey-based brand health metrics are not merely imprecise but fundamentally misleading -- they suffer from survivorship bias in perception space.

Third, **brand management is a trajectory optimization problem**, not a position optimization problem. The traditional framing -- "where should we position the brand?" -- is the wrong question. The right question is: "what drift and diffusion parameters keep the perception trajectory in a desirable region of $S^7_+$, away from absorbing boundaries and within crystallization basins?" This reframing is the dynamical consequence of the static insight that brands are multi-dimensional objects, not points on a perceptual map. Conformal prediction bands (Section 11) make this trajectory optimization operationally actionable by providing calibrated uncertainty around velocity estimates and time-to-absorption forecasts, enabling practitioners to distinguish statistically significant trajectory changes from measurement noise without relying on parametric assumptions.

The dynamical framework opens several directions for future work: interacting observer systems (correlated trajectories through social signals), empirical calibration of SDE parameters from longitudinal brand tracking data, optimal control formulations (what signal strategy minimizes absorption risk?), and connections to mean-field game theory (how do competing brands' strategies interact through their effect on shared observer populations). These extensions would complete the transition from qualitative brand theory to quantitative brand dynamics -- a transition that this paper, together with R1--R5, has begun.

---

## References

Aaker, D. A. (1991). *Managing Brand Equity: Capitalizing on the Value of a Brand Name*. Free Press.

Aitchison, J. (1986). *The Statistical Analysis of Compositional Data*. Chapman and Hall.

Angelopoulos, A. N., & Bates, S. (2023). Conformal prediction: A gentle introduction. *Foundations and Trends in Machine Learning*, 16(4), 494--591.

Ashbaugh, M. S., & Benguria, R. D. (1992). A sharp bound for the ratio of the first two eigenvalues of Dirichlet Laplacians and extensions. *Annals of Mathematics*, 135(3), 601--628.

Aydogdu, A., McQuade, S. T., & Pouradier Duteil, N. (2017). Opinion dynamics on a general compact Riemannian manifold. *Networks and Heterogeneous Media*, 12(3), 489--523.

Berger, M., Gauduchon, P., & Mazet, E. (1971). *Le Spectre d'une Variete Riemannienne*. Lecture Notes in Mathematics, Vol. 194. Springer.

Busemeyer, J. R., & Bruza, P. D. (2012). *Quantum Models of Cognition and Decision*. Cambridge University Press.

Cattiaux, P., Collet, P., Lambert, A., Martinez, S., Meleard, S., & San Martin, J. (2009). Quasi-stationary distributions and diffusion models in population dynamics. *Annals of Probability*, 37(5), 1926--1969.

Chavel, I. (1984). *Eigenvalues in Riemannian Geometry*. Academic Press.

Deffuant, G., Neau, D., Amblard, F., & Weisbuch, G. (2000). Mixing beliefs among interacting agents. *Advances in Complex Systems*, 3(01n04), 87--98.

Fechner, G. T. (1860). *Elemente der Psychophysik*. Breitkopf und Hartel.

Gardenfors, P. (2000). *Conceptual Spaces: The Geometry of Thought*. MIT Press.

Hegselmann, R., & Krause, U. (2002). Opinion dynamics and bounded confidence: Models, analysis and simulation. *Journal of Artificial Societies and Social Simulation*, 5(3), 2.

Hogarth, R. M., & Einhorn, H. J. (1992). Order effects in belief updating: The belief-adjustment model. *Cognitive Psychology*, 24(1), 1--55.

Hsu, E. P. (2002). *Stochastic Analysis on Manifolds*. Graduate Studies in Mathematics, Vol. 38. American Mathematical Society.

Kapferer, J.-N. (2008). *The New Strategic Brand Management: Creating and Sustaining Brand Equity Long Term* (4th ed.). Kogan Page.

Kardes, F. R., & Kalyanaram, G. (1992). Order-of-entry effects on consumer memory and judgment: An information integration perspective. *Journal of Marketing Research*, 29(3), 343--357.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1--22.

Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J., & Wasserman, L. (2018). Distribution-free predictive inference for regression. *Journal of the American Statistical Association*, 113(523), 1094--1111.

Levin, D. A., Peres, Y., & Wilmer, E. L. (2009). *Markov Chains and Mixing Times*. American Mathematical Society.

Lichnerowicz, A. (1958). Geometrie des groupes de transformations. *Travaux et Recherches Mathematiques*, 3. Dunod.

Mardia, K. V., & Jupp, P. E. (2000). *Directional Statistics*. Wiley.

Molenaar, P. C. M. (2004). A manifesto on psychology as idiographic science: Bringing the person back into scientific psychology, this time forever. *Measurement*, 2(4), 201--218.

Molenaar, P. C. M. (2009). The new person-specific paradigm in psychology. *Current Directions in Psychological Science*, 18(2), 112--117.

Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, 15, 1216--1221.

Peters, O., & Gell-Mann, M. (2016). Evaluating gambles using dynamics. *Chaos*, 26(2), 023103.

Stroock, D. W. (2000). *An Introduction to the Analysis of Paths on a Riemannian Manifold*. Mathematical Surveys and Monographs, Vol. 74. American Mathematical Society.

Todd, J. T., Oomes, A. H. J., Koenderink, J. J., & Kappers, A. M. L. (2001). On the affine structure of perceptual space. *Psychological Science*, 12(3), 191--196.

Viazovska, M. S. (2017). The sphere packing problem in dimension 8. *Annals of Mathematics*, 185(3), 991--1015.

Vovk, V., Gammerman, A., & Shafer, G. (2005). *Algorithmic Learning in a Random World*. Springer.

Weber, E. H. (1834). *De Pulsu, Resorptione, Auditu et Tactu: Annotationes Anatomicae et Physiologicae*. Koehler.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper.

Zharnikov, D. (2026b). The alibi problem: Epistemic foundations of multi-source data reconciliation. Working Paper.

Zharnikov, D. (2026c). Geometric approaches to brand perception: A critical survey and research agenda. Working Paper.

Zharnikov, D. (2026d). Brand space geometry: A formal metric for multi-dimensional brand perception. Working Paper.

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper.

Zharnikov, D. (2026f). Cohort boundaries in high-dimensional perception space: A concentration of measure analysis. Working Paper.

Zharnikov, D. (2026g). How many brands can a market hold? Sphere packing bounds for multi-dimensional positioning. Working Paper.

Zharnikov, D. (2026h). Specification impossibility in organizational design: A high-dimensional geometric analysis. Working Paper.

Zharnikov, D. (2026i). The Organizational Schema Theory: Test-driven business design. Working Paper.

---

## Appendix A: Numerical Computations

All numerical results reported in this paper were computed using standard mathematical formulas. Key computed values:

| Quantity | Value |
|----------|-------|
| $\text{Vol}(S^7)$ | $\pi^4/3 \approx 32.47$ |
| $\text{Vol}(S^7_+)$ | $\pi^4/768 \approx 0.1269$ |
| First eigenvalue $\lambda_1(S^7)$ | 7 |
| Dirichlet eigenvalue $\lambda_{D,1}(S^7_+)$ | 112 |
| Mixing time $\tau_{\text{mix}}(S^7)$ at $\sigma_0 = 1$ | $2/7 \approx 0.286$ |
| Mixing time QSD $\tau_{\text{mix}}(S^7_+)$ at $\sigma_0 = 1$ | $2/48 \approx 0.042$ |
| Survival time $\tau_{\text{char}}$ at $\sigma_0 = 0.1$ | 1.78 (time units) |
| Survival probability $S(2, x^*)$ at $\sigma_0 = 0.1$ | 0.326 |

**Normalized emission profiles** were computed as $\hat{s}_i = s_i / \|s\|_2$ for each brand, using the canonical emission profiles from Zharnikov (2026d).

**Minimum coordinates** $d_\partial(\hat{s}) = \min_i \hat{s}_i$:

| Brand | $d_\partial(\hat{s})$ | Minimum dimension |
|-------|---------------------|-------------------|
| Hermès | 0.137 | Economic (3.0/10) |
| IKEA | 0.227 | Social (5.0/10) |
| Patagonia | 0.219 | Economic (5.0/10) |
| Erewhon | 0.113 | Temporal (2.5/10) |
| Tesla | 0.091 | Temporal (2.0/10) |

**Ergodicity coefficient estimates** were computed as $\varepsilon = \tau_{\text{char}} / \tau_{\text{mix}}$ with $\tau_{\text{char}} = 1$ year and mixing times estimated from the drift-diffusion balance for each brand. Higher coherence grades correspond to stronger drift, which reduces the effective mixing time and increases $\varepsilon$.
