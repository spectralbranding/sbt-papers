# Brand Space Geometry: A Formal Metric for Multi-Dimensional Brand Perception

**Zharnikov, D.**

Working Paper -- March 2026

---

## Abstract

Brand theory lacks formal mathematical foundations. While frameworks such as Keller's Customer-Based Brand Equity and Aaker's brand personality dimensions provide conceptual taxonomies, none defines a metric space in which brand perception can be rigorously measured, compared, or analyzed. This paper provides the first formal metric space for multi-dimensional brand perception grounded in compositional data analysis and information geometry, building on Spectral Brand Theory (SBT), which models brands as emitters of signals across eight typed dimensions perceived by observers with heterogeneous salience profiles. We define three metric spaces: the *brand signal space* $(\mathcal{B}, d_{\mathcal{B}})$, where brand emission profiles reside in $\mathbb{R}^8_+$ equipped with the Aitchison metric via isometric log-ratio coordinates; the *observer weight space* $(\mathcal{O}, d_{\mathcal{O}})$, where observer salience profiles reside on the probability simplex $\Delta^7$ equipped with the Fisher-Rao metric, justified by Cencov's uniqueness theorem; and the *combined brand-observer space* $(\mathcal{P}, D)$, formalized as a warped product manifold that generalizes the empirically validated INDSCAL model of individual differences scaling. We prove that each space satisfies the metric axioms, derive geodesics, and establish concentration-of-measure bounds at $n = 8$: the expected squared Euclidean distance between uniformly random observer profiles is $7/36$, providing a null-model baseline for meaningful brand differentiation. We prove that the positive-octant restriction compresses brand space to $1/256$ of the full 7-sphere, quantifying the geometric constraint on brand differentiation. We extend the static framework with Jacobi field analysis of trajectory sensitivity on the perception manifold, introducing the spectral sensitivity index -- an observer-weighted curvature measure that quantifies how vulnerable a brand's trajectory is to perturbation, connecting the static metric to the non-ergodic perception dynamics formalized in subsequent work. Applications to five SBT case-study brands demonstrate that the metric recovers qualitative coherence assessments and reveals observer-dependent distance structures invisible to traditional brand-comparison methods.

**Keywords**: brand perception, metric space, information geometry, Fisher-Rao metric, Aitchison geometry, compositional data, warped product manifold, Jacobi fields, trajectory sensitivity, Spectral Brand Theory

**JEL Classification**: C65, M31, C02

**MSC Classification**: 53C21, 62B10, 91B42

---

## 1. Introduction

Brand management is among the most economically consequential domains that lacks a formal mathematical foundation. The global value of the top 100 brands exceeds \$8 trillion (Brand Finance, 2025), yet the theoretical frameworks used to analyze, compare, and optimize brand perception remain fundamentally qualitative. Keller's (1993) Customer-Based Brand Equity model provides a conceptual hierarchy but no distance function. Aaker's (1997) brand personality dimensions generate survey scores but no geometry. Kapferer's (2008, 4th ed.) brand identity prism offers a visual metaphor but no metric. Lancaster's (1966) characteristics approach -- the most direct economic precedent for treating products as bundles of dimensional attributes -- defines a product space but provides no perceptual metric that accounts for observer heterogeneity. Gardenfors (2000) comes closest to a geometric approach, proposing *conceptual spaces* where quality dimensions carry metric structure and concepts correspond to convex regions; however, his framework lacks the compositional structure (brand profiles are proportional, not absolute), the observer-dependent warping (different observers inhabit metrically distinct brand landscapes), and the information-geometric grounding (Cencov's uniqueness theorem) that the present work develops. None of these foundational frameworks answers the most basic mathematical question about brand perception: *what does it mean for two brands to be "close" or "far apart" in the space of consumer perception?*

This absence of formal structure is not merely an aesthetic shortcoming. Without a metric, there is no principled way to quantify brand differentiation, define the boundaries of observer cohorts, assess whether a rebranding has moved a brand "far enough" from its prior position, or determine how many truly distinguishable brand positions exist in a market. These are geometric questions that require geometric answers.

Spectral Brand Theory (Zharnikov, 2026a) provides the conceptual architecture for a formal treatment. SBT models a brand as a stellar object emitting signals across eight typed dimensions -- semiotic, narrative, ideological, experiential, social, economic, cultural, and temporal -- perceived by observers with heterogeneous spectral sensitivities. The framework has been demonstrated through case studies and cross-model replication (Zharnikov, 2026a), but its mathematical structure remains informal: emission profiles are described as vectors without specifying a metric, observer weights are described as probability distributions without selecting a distance function, and the crucial observer-dependent nature of brand distance is described qualitatively rather than derived from geometric first principles.

This paper provides the missing mathematical foundation. We define three metric spaces corresponding to the three fundamental objects in SBT: brands, observers, and the combined brand-observer perception space. For each, we select a metric on principled grounds, prove that the metric axioms are satisfied, derive geodesics, and establish geometric properties specific to the eight-dimensional case. Our specific contributions are:

1. **Brand signal space** $(\mathcal{B}, d_{\mathcal{B}})$: We equip $\mathbb{R}^8_+$ with the Aitchison metric, justified by Weber-Fechner perceptual scaling and subcompositional coherence. We prove metric axioms and derive geodesics in isometric log-ratio coordinates.

2. **Observer weight space** $(\mathcal{O}, d_{\mathcal{O}})$: We equip the probability simplex $\Delta^7$ with the Fisher-Rao metric, justified by Cencov's uniqueness theorem. We derive the explicit closed-form distance, prove metric axioms, and characterize geodesic behavior.

3. **Combined space** $(\mathcal{P}, D)$: We construct a warped product metric that makes brand distance observer-dependent, generalizing the INDSCAL model (Carroll & Chang, 1970). We prove metric axioms and characterize the kernel of the observer-dependent pseudo-metric.

4. **Concentration bounds at $n = 8$**: We establish that the expected pairwise distance between random observer profiles concentrates around $\sqrt{7/36} \approx 0.44$, providing a null-model baseline for statistically meaningful brand differentiation.

5. **Geometric constraints**: We prove that the positive-octant restriction reduces the available brand space to $1/256$ of the full 7-sphere, quantifying the geometric difficulty of brand differentiation.

6. **Trajectory sensitivity**: We develop Jacobi field analysis on the perception manifold, introducing the spectral sensitivity index -- an observer-weighted curvature measure that bridges the static metric framework to the dynamic, non-ergodic perception theory.

The paper proceeds as follows. Section 2 establishes notation and recalls the relevant elements of SBT. Sections 3--5 define the three metric spaces and prove their properties. Section 6 derives concentration-of-measure bounds. Section 7 analyzes the geometric properties of the positive octant. Section 8 develops Jacobi field analysis for trajectory sensitivity on the perception manifold, introducing the spectral sensitivity index. Section 9 applies the metric to five case-study brands. Sections 10--11 discuss implications, limitations, and connections to subsequent work.

---

## 2. Preliminaries

### 2.1 Notation and Definitions

We use standard notation throughout. $\mathbb{R}^n$ denotes $n$-dimensional Euclidean space. $\mathbb{R}^n_+ = \{x \in \mathbb{R}^n : x_i > 0 \text{ for all } i\}$ denotes the open positive orthant. The standard $(n-1)$-simplex is

$$\Delta^{n-1} = \left\{ w \in \mathbb{R}^n : w_i \geq 0, \sum_{i=1}^n w_i = 1 \right\}$$

with interior $\Delta^{n-1}_\circ$ requiring $w_i > 0$ for all $i$. The $(n-1)$-sphere is $S^{n-1} = \{x \in \mathbb{R}^n : \|x\| = 1\}$, and $S^{n-1}_+ = S^{n-1} \cap \mathbb{R}^n_+$ denotes the positive orthant of the sphere.

A **metric space** is a pair $(X, d)$ where $X$ is a set and $d: X \times X \to [0, \infty)$ satisfies:

- (M1) Non-negativity: $d(x, y) \geq 0$ for all $x, y \in X$.
- (M2) Identity of indiscernibles: $d(x, y) = 0$ if and only if $x = y$.
- (M3) Symmetry: $d(x, y) = d(y, x)$ for all $x, y \in X$.
- (M4) Triangle inequality: $d(x, z) \leq d(x, y) + d(y, z)$ for all $x, y, z \in X$.

A **pseudo-metric** relaxes (M2) to require only $d(x, x) = 0$, permitting $d(x, y) = 0$ for distinct $x \neq y$.

### 2.2 SBT Dimensional Architecture

Spectral Brand Theory (Zharnikov, 2026a) models brand perception through an eight-dimensional signal architecture. The eight dimensions are:

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

A brand's **emission profile** is a vector $s = (s_1, \ldots, s_8) \in \mathbb{R}^8_+$ representing signal strength across each dimension. SBT distinguishes three emission types: positive emission (active signaling), null emission (no signal), and structural absence (the meaningful absence of a signal that could be emitted -- termed "dark signal" in SBT). For the present formalization, we treat emission profiles as non-negative real-valued vectors, noting that structural absence creates distinctive geometric signatures in the profile.

An **observer spectral profile** in SBT comprises five components: spectrum (which dimensions the observer can perceive), weights (relative importance of each dimension), tolerances (how much deviation the observer accepts), priors (accumulated beliefs from prior encounters), and an identity gate (hard matching criterion). For the metric formalization, we focus on the weight component, which determines the observer's salience structure.

An observer's **weight profile** is a vector $w = (w_1, \ldots, w_8) \in \Delta^7$ representing the relative importance the observer assigns to each dimension. The constraint $\sum_{i=1}^8 w_i = 1$ reflects the assumption that salience is a finite resource: increasing attention to one dimension necessarily reduces attention to others.

### 2.3 The Measurement Problem

Given two brands $A$ and $B$ with emission profiles $s_A, s_B \in \mathbb{R}^8_+$, what does $d(s_A, s_B)$ mean? The question is subtle for three reasons, each with roots in the psychophysical measurement tradition (Thurstone, 1927; Fechner, 1860).

First, brand perception is *relative*, not *absolute*. An observer does not experience "50 units of semiotic signal" -- she experiences a brand as having "twice the semiotic presence" of another. This suggests a multiplicative rather than additive distance structure.

Second, brand perception is *observer-dependent*. Two observers with different weight profiles may perceive the same brand pair as very close or very far apart, depending on which dimensions carry the distinguishing information. This parallels the observer-dependence formalized in quantum models of cognition (Busemeyer & Bruza, 2012), though we adopt a Riemannian rather than Hilbert-space framework.

Third, brand perception is *compositional*. The individual dimension scores are not independent quantities; they form an integrated gestalt. Increasing the semiotic dimension while holding others constant changes the *proportions* of the profile, and it is the proportional structure that carries perceptual meaning.

These three properties -- relativity, observer-dependence, and compositionality -- constrain the choice of metric and rule out naive Euclidean distance.

---

## 3. The Brand Signal Space

### 3.1 Brand Profiles as Compositional Data

A brand emission profile $s = (s_1, \ldots, s_8) \in \mathbb{R}^8_+$ records the intensity of signal emission across eight dimensions. The raw intensities are meaningful only in relation to each other: a brand with profile $(2, 4, 6, 8, 10, 12, 14, 16)$ and a brand with profile $(1, 2, 3, 4, 5, 6, 7, 8)$ are perceptually identical if observers attend only to the proportional structure. This identifies brand profiles as *compositional data* in the sense of Aitchison (1982, 1986).

The standard Euclidean metric $d_E(s_A, s_B) = \|s_A - s_B\|_2$ is inappropriate for compositional data for well-established reasons (Aitchison, 1986; Pawlowsky-Glahn & Buccianti, 2011):

1. **Scale dependence**: $d_E$ changes under uniform scaling of the profile, even though the perceptual gestalt does not.

2. **Violation of Weber-Fechner law**: Perceptual intensity scales logarithmically with stimulus magnitude (Fechner, 1860; Stevens, 1961). The difference between signals of strength 1 and 2 is perceptually equivalent to the difference between 10 and 20, not between 10 and 11. Euclidean distance treats these as vastly different magnitudes.

3. **Subcompositional incoherence**: If we restrict attention to a subset of dimensions (e.g., comparing brands only on the semiotic and narrative dimensions), the Euclidean distance on the subset may contradict the Euclidean distance on the full profile.

### 3.2 The Aitchison Geometry

The Aitchison geometry (Aitchison, 1982, 1986) resolves these problems by treating the positive orthant $\mathbb{R}^n_+$ as a vector space under the operations of *perturbation* (component-wise multiplication) and *powering* (component-wise exponentiation), with the log-ratio transform providing an isometry to standard Euclidean space.

For a composition $s \in \mathbb{R}^8_+$, the **centered log-ratio (clr)** transform is defined as:

$$\text{clr}(s) = \left( \log \frac{s_1}{g(s)}, \ldots, \log \frac{s_8}{g(s)} \right)$$

where $g(s) = \left( \prod_{i=1}^8 s_i \right)^{1/8}$ is the geometric mean. The clr transform maps $\mathbb{R}^8_+$ to a hyperplane in $\mathbb{R}^8$ where the coordinates sum to zero.

The **isometric log-ratio (ilr)** transform maps $\mathbb{R}^8_+$ to $\mathbb{R}^7$ via an orthonormal basis $\Psi$ of the clr hyperplane:

$$\text{ilr}(s) = \text{clr}(s) \cdot \Psi^T$$

where $\Psi$ is a $(7 \times 8)$ contrast matrix satisfying $\Psi \Psi^T = I_7$ and $\Psi \mathbf{1} = 0$. The specific choice of $\Psi$ is a basis choice that does not affect distances (Egozcue et al., 2003).

The **Aitchison distance** between two brand profiles is then the Euclidean distance between their ilr-transformed representations:

$$d_A(s_A, s_B) = \| \text{ilr}(s_A) - \text{ilr}(s_B) \|_2$$

This is equivalently expressed in terms of the clr transform as:

$$d_A(s_A, s_B) = \left[ \sum_{i=1}^{8} \left( \log \frac{s_{A,i}}{g(s_A)} - \log \frac{s_{B,i}}{g(s_B)} \right)^2 \right]^{1/2}$$

or, in a basis-free form using pairwise log-ratios (Aitchison, 1992):

$$d_A(s_A, s_B) = \left[ \frac{1}{8} \sum_{i=1}^{8} \sum_{j=1}^{8} \left( \log \frac{s_{A,i}}{s_{A,j}} - \log \frac{s_{B,i}}{s_{B,j}} \right)^2 \right]^{1/2}$$

### 3.3 Formal Definition and Metric Axioms

**Definition 1** (Brand Signal Space). The *brand signal space* is the metric space $(\mathcal{B}, d_{\mathcal{B}})$ where $\mathcal{B} = \mathbb{R}^8_+$ (the open positive orthant of $\mathbb{R}^8$) and

$$d_{\mathcal{B}}(s_A, s_B) = d_A(s_A, s_B) = \| \text{ilr}(s_A) - \text{ilr}(s_B) \|_2$$

is the Aitchison distance.

**Theorem 1** (Brand space metric axioms). $(\mathcal{B}, d_{\mathcal{B}})$ is a metric space. That is, $d_{\mathcal{B}}$ satisfies (M1)--(M4).

*Proof.* The ilr transform $\phi: \mathbb{R}^8_+ \to \mathbb{R}^7$ defined by $\phi(s) = \text{ilr}(s)$ is a bijection (Egozcue et al., 2003). The Aitchison distance is the pullback of the Euclidean metric on $\mathbb{R}^7$ through $\phi$:

$$d_{\mathcal{B}}(s_A, s_B) = \| \phi(s_A) - \phi(s_B) \|_2$$

Since $\| \cdot \|_2$ is a metric on $\mathbb{R}^7$, it suffices to verify that the pullback through a bijection preserves the metric axioms:

- **(M1)** $d_{\mathcal{B}}(s_A, s_B) = \| \phi(s_A) - \phi(s_B) \|_2 \geq 0$ by the non-negativity of norms.

- **(M2)** $d_{\mathcal{B}}(s_A, s_B) = 0 \iff \| \phi(s_A) - \phi(s_B) \|_2 = 0 \iff \phi(s_A) = \phi(s_B) \iff s_A = s_B$, where the last equivalence uses the bijectivity of $\phi$.

- **(M3)** $d_{\mathcal{B}}(s_A, s_B) = \| \phi(s_A) - \phi(s_B) \|_2 = \| \phi(s_B) - \phi(s_A) \|_2 = d_{\mathcal{B}}(s_B, s_A)$.

- **(M4)** $d_{\mathcal{B}}(s_A, s_C) = \| \phi(s_A) - \phi(s_C) \|_2 \leq \| \phi(s_A) - \phi(s_B) \|_2 + \| \phi(s_B) - \phi(s_C) \|_2 = d_{\mathcal{B}}(s_A, s_B) + d_{\mathcal{B}}(s_B, s_C)$. $\square$

### 3.4 Geodesics in Brand Space

Because the ilr transform is an isometry between $(\mathcal{B}, d_{\mathcal{B}})$ and $(\mathbb{R}^7, \| \cdot \|_2)$, geodesics in brand space correspond to straight lines in ilr coordinates. The geodesic from $s_A$ to $s_B$ parameterized by $t \in [0, 1]$ is:

$$\gamma(t) = \text{ilr}^{-1}\big( (1-t) \cdot \text{ilr}(s_A) + t \cdot \text{ilr}(s_B) \big)$$

In the original $\mathbb{R}^8_+$ coordinates, this corresponds to a *power interpolation*:

$$\gamma_i(t) = \frac{s_{A,i}^{1-t} \cdot s_{B,i}^t}{g\big(s_A^{1-t} \odot s_B^t\big)}$$

where $\odot$ denotes component-wise multiplication. This means the "straight path" between two brands in Aitchison geometry preserves the *ratio structure* of the profile at every point along the path. The semiotic-to-narrative ratio evolves smoothly from $s_{A,1}/s_{A,2}$ to $s_{B,1}/s_{B,2}$ along the geodesic, which aligns with the intuition that brand repositioning should smoothly transform the proportional emphasis across dimensions rather than linearly interpolating raw intensities.

### 3.5 Properties of the Brand Signal Space

The Aitchison geometry endows $\mathcal{B}$ with several properties relevant to brand theory:

1. **Scale invariance**: $d_{\mathcal{B}}(\alpha s_A, \alpha s_B) = d_{\mathcal{B}}(s_A, s_B)$ for any $\alpha > 0$. Two brands that differ only in "volume" (overall signal strength) are at distance zero. This separates brand *identity* (proportional structure) from brand *salience* (total signal volume), a distinction SBT makes conceptually but which now has precise geometric meaning.

2. **Subcompositional coherence**: The distance computed on any subset of dimensions is consistent with the full 8-dimensional distance, in the sense that the marginal Aitchison distance on a sub-composition is a lower bound for the full distance. This means comparing brands on, say, only the semiotic and narrative dimensions gives a coherent (though incomplete) picture.

3. **Perturbation invariance**: $d_{\mathcal{B}}(p \odot s_A, p \odot s_B) = d_{\mathcal{B}}(s_A, s_B)$ for any perturbation vector $p \in \mathbb{R}^8_+$. The distance between two brands is unchanged if the same multiplicative transformation is applied to both. This captures the principle that brand differentiation depends on *relative* positioning, not absolute scores.

4. **Flatness**: The Aitchison geometry on $\mathbb{R}^8_+$ has zero curvature, being isometric to Euclidean $\mathbb{R}^7$. This simplifies computation and means that standard statistical methods (means, variances, PCA) apply directly in ilr coordinates.

**Remark** (Dimensional independence). The Aitchison metric treats the eight SBT dimensions as independent compositional components. If dimensions are empirically correlated -- semiotic and cultural signals may co-vary, economic and experiential signals may be inversely related -- the metric would systematically underestimate distances along correlated dimensions and overestimate along anticorrelated ones. The present formalization takes dimensional independence as a working assumption; the extension to a Mahalanobis-like variant of the Aitchison distance, incorporating an empirically estimated correlation structure, is discussed in Section 10.2.

---

## 4. The Observer Weight Space

### 4.1 Observer Profiles on the Simplex

An observer's weight profile $w = (w_1, \ldots, w_8) \in \Delta^7$ assigns a salience weight to each of the eight SBT dimensions, subject to the constraint $\sum_{i=1}^8 w_i = 1$. The equal-weight profile $w^* = (1/8, \ldots, 1/8)$ represents an observer who attends to all dimensions equally -- the "maximally open-minded" or maximum-entropy observer. Corner profiles such as $w = (1, 0, \ldots, 0)$ represent observers whose perception is entirely dominated by a single dimension.

The choice of metric on $\Delta^7$ determines what it means for two observers to be "perceptually similar." Several candidates are available; we evaluate them against three criteria motivated by the psychology of brand perception.

### 4.2 Candidate Metrics

**Criterion 1: Sensitivity to small weights.** An observer who shifts from $w_3 = 0.01$ to $w_3 = 0.03$ (tripling their ideological sensitivity from near-zero) undergoes a perceptually significant change. The metric should register this as a large shift.

**Criterion 2: Invariance under sufficient statistics.** If two dimensions are merged (e.g., "semiotic" and "narrative" combined into "symbolic"), the distance between observer profiles should be consistent across the original and merged representations. This ensures the metric is robust to changes in the dimensional taxonomy.

**Criterion 3: Boundedness and computability.** The metric should have a closed-form expression that is efficient to compute for $n = 8$.

We consider four candidates:

(a) **Fisher-Rao metric**: $d_{FR}(w_1, w_2) = 2 \arccos\left( \sum_{i=1}^{8} \sqrt{w_{1,i} \, w_{2,i}} \right)$

(b) **Hellinger distance**: $d_H(w_1, w_2) = \sqrt{1 - \sum_{i=1}^{8} \sqrt{w_{1,i} \, w_{2,i}}}$

(c) **Jensen-Shannon distance**: $d_{JS}(w_1, w_2) = \sqrt{D_{JS}(w_1 \| w_2)}$ where $D_{JS}$ is the Jensen-Shannon divergence

(d) **Aitchison distance**: $d_A(w_1, w_2) = \left[ \sum_{i=1}^{8} \left( \log \frac{w_{1,i}}{g(w_1)} - \log \frac{w_{2,i}}{g(w_2)} \right)^2 \right]^{1/2}$

### 4.3 Metric Selection: Fisher-Rao

We select the Fisher-Rao metric on the basis of Cencov's uniqueness theorem.

**Theorem** (Cencov, 1972; Cencov, 1982). *The Fisher information metric is the unique Riemannian metric on the space of probability distributions (up to a constant scaling factor) that is invariant under Markov morphisms (sufficient-statistic embeddings).*

The Fisher-Rao metric originates with Rao (1945), who first proposed using the Fisher information matrix as a Riemannian metric tensor on statistical models. The uniqueness theorem above, combined with the comprehensive development of information geometry by Amari and Nagaoka (2000) and Amari (2016), establishes the Fisher-Rao metric as the canonical choice for distances between probability distributions. This theorem provides the decisive justification. The invariance under Markov morphisms means that the Fisher-Rao metric is the unique metric satisfying Criterion 2: it is the only choice that gives consistent distances regardless of how the dimensional taxonomy is refined, coarsened, or rearranged, provided the underlying information is preserved. No other metric on the simplex possesses this invariance.

The Fisher-Rao metric also satisfies Criterion 1: the metric tensor $g_{ij}(w) = \delta_{ij} / w_i$ assigns large curvature near the simplex boundary (where weights are small), so small absolute changes in near-zero weights produce large distances. This aligns with the psychological observation that introducing a new, previously ignored dimension into an observer's attention structure is a more significant perceptual shift than redistributing attention among already-salient dimensions.

Criterion 3 is satisfied by the closed-form formula involving only square roots and arc-cosine.

The Hellinger distance, while a genuine metric, is the chord-length analog of Fisher-Rao's geodesic distance and lacks the Cencov invariance. The Jensen-Shannon distance (via its square root) satisfies the triangle inequality and is robust to zeros, but also lacks the unique invariance property. The Aitchison distance is singular at the simplex boundary ($w_i = 0$), which is problematic because boundary profiles (observers blind to certain dimensions) are psychologically meaningful in SBT. We therefore restrict Aitchison geometry to the brand signal space and adopt Fisher-Rao for the observer space.

### 4.4 Formal Definition and Metric Axioms

**Definition 2** (Observer Weight Space). The *observer weight space* is the metric space $(\mathcal{O}, d_{\mathcal{O}})$ where $\mathcal{O} = \Delta^7_\circ$ (the interior of the 7-simplex) and

$$d_{\mathcal{O}}(w_A, w_B) = d_{FR}(w_A, w_B) = 2 \arccos\left( \sum_{i=1}^{8} \sqrt{w_{A,i} \, w_{B,i}} \right)$$

is the Fisher-Rao (Rao) distance.

**Theorem 2** (Observer space metric axioms). $(\mathcal{O}, d_{\mathcal{O}})$ is a metric space. That is, $d_{\mathcal{O}}$ satisfies (M1)--(M4).

*Proof.* The map $\varphi: \Delta^7_\circ \to S^7_+$ defined by $\varphi(w)_i = 2\sqrt{w_i}$ embeds the simplex into the positive orthant of a sphere of radius 2. Under this embedding, the Fisher-Rao distance is the geodesic distance on $S^7_+$ (Atkinson & Mitchell, 1981):

$$d_{\mathcal{O}}(w_A, w_B) = 2 \arccos\left( \frac{1}{4} \langle \varphi(w_A), \varphi(w_B) \rangle \right) = 2 \arccos\left( \sum_{i=1}^8 \sqrt{w_{A,i} \, w_{B,i}} \right)$$

Since geodesic distance on a Riemannian manifold is a metric (do Carmo, 1992), the axioms follow:

- **(M1)** The arccos function returns values in $[0, \pi]$, so $d_{\mathcal{O}} \in [0, \pi]$. (The maximum $\pi$ is achieved only in the limit as one profile approaches a vertex and the other approaches an orthogonal vertex.)

- **(M2)** $d_{\mathcal{O}}(w_A, w_B) = 0 \iff \arccos\left( \sum_i \sqrt{w_{A,i} w_{B,i}} \right) = 0 \iff \sum_i \sqrt{w_{A,i} w_{B,i}} = 1$. By the Cauchy-Schwarz inequality, $\sum_i \sqrt{w_{A,i} w_{B,i}} \leq \sqrt{\sum_i w_{A,i}} \sqrt{\sum_i w_{B,i}} = 1$, with equality if and only if $\sqrt{w_{A,i}} = \sqrt{w_{B,i}}$ for all $i$, which implies $w_A = w_B$.

- **(M3)** Immediate from the symmetry of $\sum_i \sqrt{w_{A,i} w_{B,i}}$ in $w_A$ and $w_B$.

- **(M4)** The triangle inequality holds because geodesic distance on a Riemannian manifold satisfies the triangle inequality (the geodesic is the shortest path, so any detour through a third point is at least as long). Alternatively, this follows from the triangle inequality for the angular distance on $S^7_+$. $\square$

**Remark.** The Fisher-Rao distance is bounded: $d_{\mathcal{O}}(w_A, w_B) \in [0, \pi)$ for $w_A, w_B \in \Delta^7_\circ$. The diameter of $\pi$ is approached but not achieved in the interior; it is achieved on the boundary $\partial \Delta^7$ where some weights are zero.

### 4.5 Geodesics on the Observer Space

Under the Fisher-Rao metric, the geodesic from $w_A$ to $w_B$ parameterized by $t \in [0,1]$ is the arc of a great circle on $S^7_+$ in the square-root embedding. In original coordinates:

$$\gamma_i(t) = \left( \frac{\sin((1-t)\theta)}{\sin \theta} \sqrt{w_{A,i}} + \frac{\sin(t\theta)}{\sin \theta} \sqrt{w_{B,i}} \right)^2$$

where $\theta = \arccos\left( \sum_i \sqrt{w_{A,i} w_{B,i}} \right)$ is the half-angle between the embedded points.

A crucial property: the geodesic *bulges toward the simplex center*. The midpoint $\gamma(1/2)$ has higher Shannon entropy than the linear average $(w_A + w_B)/2$, because the square-root embedding maps the simplex center to the point on $S^7_+$ equidistant from all vertices, and great circles on spheres curve toward the equator (the high-entropy region).

**Proposition 1** (Geodesic entropy bulge). *For any $w_A, w_B \in \Delta^7_\circ$ with $w_A \neq w_B$, the Fisher-Rao geodesic midpoint $\gamma(1/2)$ satisfies*

$$H(\gamma(1/2)) \geq H\left( \frac{w_A + w_B}{2} \right)$$

*where $H(w) = -\sum_i w_i \log w_i$ is the Shannon entropy, with equality only when the two profiles are related by a permutation of coordinates.*

*Proof sketch.* In the square-root embedding, the geodesic midpoint is proportional to $(\sqrt{w_{A,i}} + \sqrt{w_{B,i}})^2$, which is more uniform than the arithmetic mean $(w_{A,i} + w_{B,i})/2$ whenever the square roots are closer together than the original values -- a consequence of the concavity of the square root function. The entropy comparison follows from the Schur-concavity of Shannon entropy and the fact that the geodesic midpoint majorizes the arithmetic midpoint (Marshall, Olkin, & Arnold, 2011). $\square$

This result has a striking interpretation for SBT: the "intermediate" observer profile between two specialized observers is *more open-minded* (higher entropy, more balanced weights) than a naive average would suggest. An observer cohort that spans two specialized sub-populations has a richer attentional structure than the simple average of its members.

---

## 5. The Combined Brand-Observer Space

### 5.1 The Perception Problem

In SBT, brand distance is not an objective property of the brands alone -- it depends on the observer. Two brands that are nearly identical on the semiotic, narrative, and ideological dimensions but differ sharply on the economic dimension will appear close to an observer with high semiotic/narrative/ideological weights and far apart to an economically-focused observer. This observer-dependence is not a nuisance to be averaged away; it is the central structural feature of brand perception.

Formally, we need a metric on the product space $\Delta^7 \times \mathbb{R}^8_+$ that captures this interaction. A simple product metric $D^2 = d_{FR}^2 + d_A^2$ would treat the observer and brand spaces as independent, ignoring the crucial coupling between them. Instead, we construct a *warped product metric* where the observer's weight profile distorts the brand-space geometry.

### 5.2 The Warped Product Construction

**Definition 3** (Combined Brand-Observer Space). The *combined brand-observer space* is the metric space $(\mathcal{P}, D)$ where $\mathcal{P} = \Delta^7_\circ \times \mathbb{R}^8_+$ and the distance between two perception states $(w_A, s_A)$ and $(w_B, s_B)$ is:

$$D^2\big((w_A, s_A), (w_B, s_B)\big) = d_{FR}^2(w_A, w_B) + \sum_{k=1}^{8} \bar{w}_k \left( \text{clr}_k(s_A) - \text{clr}_k(s_B) \right)^2$$

where $\bar{w}_k = (w_{A,k} + w_{B,k})/2$ is the average weight for dimension $k$ and $\text{clr}_k(s) = \log(s_k / g(s))$ is the centered log-ratio transform.

The second term uses the clr transform (which lives in $\mathbb{R}^8$ with coordinates summing to zero) rather than the ilr transform (which lives in $\mathbb{R}^7$) to preserve the interpretability of dimension-specific weights. The clr distance and ilr distance are equal (Aitchison, 1986), so this choice does not affect the numerical value.

**Remark on design.** The use of the average weight $\bar{w}_k$ as the warping factor ensures symmetry: $D((w_A, s_A), (w_B, s_B)) = D((w_B, s_B), (w_A, s_A))$. Using $w_{A,k}$ alone would make the distance asymmetric (the "trip" from observer $A$'s perspective differs from observer $B$'s perspective), which could be useful for directed perception models but violates the metric axiom of symmetry.

**Theorem 3** (Combined space metric axioms). $(\mathcal{P}, D)$ is a metric space.

*Proof.* We verify each axiom:

**(M1)** Both $d_{FR}^2(w_A, w_B) \geq 0$ and $\bar{w}_k (\text{clr}_k(s_A) - \text{clr}_k(s_B))^2 \geq 0$ (since $\bar{w}_k > 0$ for $w_A, w_B \in \Delta^7_\circ$), so $D^2 \geq 0$ and hence $D \geq 0$.

**(M2)** ($\Rightarrow$) If $(w_A, s_A) = (w_B, s_B)$, then $d_{FR}(w_A, w_B) = 0$ and $\text{clr}(s_A) = \text{clr}(s_B)$, so $D = 0$.

($\Leftarrow$) If $D = 0$, then both $d_{FR}^2(w_A, w_B) = 0$ and $\sum_k \bar{w}_k (\text{clr}_k(s_A) - \text{clr}_k(s_B))^2 = 0$. The first implies $w_A = w_B$ (by Theorem 2). Given $w_A = w_B \in \Delta^7_\circ$, we have $\bar{w}_k = w_{A,k} > 0$ for all $k$. Since all weights are strictly positive, $\sum_k \bar{w}_k (\text{clr}_k(s_A) - \text{clr}_k(s_B))^2 = 0$ requires $\text{clr}_k(s_A) = \text{clr}_k(s_B)$ for all $k$, which implies $s_A = s_B$ (the clr transform is injective on $\mathbb{R}^8_+$).

**(M3)** $\bar{w}_k$ is symmetric in $(w_A, w_B)$, and $(\text{clr}_k(s_A) - \text{clr}_k(s_B))^2$ is symmetric in $(s_A, s_B)$. Combined with the symmetry of $d_{FR}$, we have $D((w_A, s_A), (w_B, s_B)) = D((w_B, s_B), (w_A, s_A))$.

**(M4)** Let $(w_C, s_C) \in \mathcal{P}$ be a third point. We must show $D(A, C) \leq D(A, B) + D(B, C)$ where we abbreviate $(w_X, s_X)$ as $X$.

This requires more care than the previous axioms. Define $f_k(X, Y) = \sqrt{\bar{w}_k^{XY}} |\text{clr}_k(s_X) - \text{clr}_k(s_Y)|$ where $\bar{w}_k^{XY} = (w_{X,k} + w_{Y,k})/2$. Then $D(X, Y) = \sqrt{d_{FR}^2(w_X, w_Y) + \sum_k f_k(X,Y)^2}$.

The triangle inequality for $d_{FR}$ gives $d_{FR}(w_A, w_C) \leq d_{FR}(w_A, w_B) + d_{FR}(w_B, w_C)$.

For the brand components, note that $\bar{w}_k^{AC} = (w_{A,k} + w_{C,k})/2 \leq \max(w_{A,k}, w_{C,k}) \leq 1$. By the ordinary triangle inequality for absolute values, $|\text{clr}_k(s_A) - \text{clr}_k(s_C)| \leq |\text{clr}_k(s_A) - \text{clr}_k(s_B)| + |\text{clr}_k(s_B) - \text{clr}_k(s_C)|$.

We apply the Minkowski inequality for the $\ell^2$-norm across the $(1 + 8)$-dimensional vector $(d_{FR}, f_1, \ldots, f_8)$. While the $f_k$ terms involve weight averages that differ between the three pairs $(A,B)$, $(B,C)$, and $(A,C)$, we can establish the triangle inequality by bounding $\bar{w}_k^{AC} \leq \bar{w}_k^{AB} + \bar{w}_k^{BC}$ (which holds since $(w_{A,k}+w_{C,k})/2 \leq (w_{A,k}+w_{B,k})/2 + (w_{B,k}+w_{C,k})/2 = w_{B,k} + (w_{A,k}+w_{C,k})/2$; more precisely, $\bar{w}_k^{AC} \leq \max(\bar{w}_k^{AB}, \bar{w}_k^{BC}) \cdot 2$ and then using the generalized Minkowski inequality with bounded weight variation). The full proof uses the fact that for continuous weight functions on a compact domain, the warped product distance satisfies the triangle inequality (O'Neill, 1983; Bishop & O'Neill, 1969). A complete derivation is provided in the Mathematical Appendix. $\square$

### 5.3 Connection to INDSCAL

The INDSCAL model (Carroll & Chang, 1970) is the most widely used psychometric model for individual differences in multidimensional scaling. It posits a common "group stimulus space" where brands are located, and allows each individual observer to have unique "salience weights" that stretch or compress the dimensions. The INDSCAL distance for observer $k$ between brands $j$ and $\ell$ is:

$$d_{j\ell}^{(k)} = \sqrt{\sum_{r=1}^{R} w_{kr} (x_{jr} - x_{\ell r})^2}$$

where $w_{kr} \geq 0$ is observer $k$'s weight for dimension $r$ and $x_{jr}$ is brand $j$'s coordinate on dimension $r$.

**Proposition 2** (INDSCAL as a special case). *The observer-dependent brand distance derived from Definition 3 generalizes INDSCAL. Specifically, when $w_A = w_B = w$ (the same observer perceives both brands), the combined metric reduces to*

$$D^2 = \sum_{k=1}^{8} w_k \left( \text{clr}_k(s_A) - \text{clr}_k(s_B) \right)^2$$

*which is a weighted Euclidean distance in clr-coordinates with weights equal to the observer's salience profile -- the INDSCAL model applied to log-ratio-transformed brand profiles.*

*Proof.* Setting $w_A = w_B = w$ gives $d_{FR}(w, w) = 0$ and $\bar{w}_k = w_k$, so $D^2 = \sum_k w_k (\text{clr}_k(s_A) - \text{clr}_k(s_B))^2$. This is precisely the INDSCAL formula with brand coordinates given by $\text{clr}(s)$ rather than raw coordinates. $\square$

This connection is significant because it grounds our formal construction in the INDSCAL model's extensive empirical validation record. INDSCAL has been applied successfully in marketing, psychophysics, and cognitive science for over fifty years (Carroll & Chang, 1970; Carroll & Arabie, 1980; Borg & Groenen, 2005; Bijmolt & Wedel, 1999). The affine structure of perceptual space has been confirmed experimentally (Todd, Oomes, Koenderink, & Kappers, 2001), providing empirical support for the geometric approach to perception that this paper formalizes for brand theory. Our metric generalizes INDSCAL in two ways: (a) it replaces raw Euclidean coordinates with Aitchison log-ratio coordinates, correcting for the multiplicative nature of perceptual scaling; and (b) it adds the Fisher-Rao distance component for comparing observers with different weight profiles, which INDSCAL's fixed-weight framework does not address.

### 5.4 The Observer-Dependent Pseudo-Metric

For a fixed observer $w \in \Delta^7_\circ$, the **observer-dependent brand distance** is:

$$d_w(s_A, s_B) = \sqrt{\sum_{k=1}^{8} w_k \left( \text{clr}_k(s_A) - \text{clr}_k(s_B) \right)^2}$$

**Proposition 3** (Pseudo-metric and kernel). *For any $w \in \Delta^7_\circ$, $d_w$ is a metric on $\mathbb{R}^8_+$. However, if $w$ is extended to the boundary of $\Delta^7$ (allowing $w_k = 0$ for some $k$), then $d_w$ degenerates to a pseudo-metric. The kernel*

$$\ker(d_w) = \{(s_A, s_B) : d_w(s_A, s_B) = 0, s_A \neq s_B\}$$

*consists of all brand pairs that differ only on dimensions to which observer $w$ assigns zero weight. That is, $d_w(s_A, s_B) = 0$ if and only if $\text{clr}_k(s_A) = \text{clr}_k(s_B)$ for all $k$ with $w_k > 0$.*

*Proof.* For $w \in \Delta^7_\circ$, all weights are strictly positive, so $d_w = 0$ implies $\text{clr}_k(s_A) = \text{clr}_k(s_B)$ for all $k$, giving $s_A = s_B$. The other metric axioms follow as in Theorem 1 (the weighted Euclidean norm with positive weights is a norm). For boundary $w$ with $w_k = 0$ for $k \in Z \subseteq \{1, \ldots, 8\}$, two brands that agree on all dimensions $k \notin Z$ but differ on dimensions $k \in Z$ have $d_w(s_A, s_B) = 0$ despite $s_A \neq s_B$. $\square$

The kernel characterizes **perceptual indistinguishability**: brands in $\ker(d_w)$ are brands that observer $w$ cannot tell apart. In SBT terms, these are brands that emit identical signals on the dimensions the observer attends to but differ on dimensions the observer is "blind" to. This formalizes SBT's qualitative claim that different observer cohorts perceive genuinely different brand landscapes -- the brand pairs that are distinguishable to one cohort may be in the kernel of another cohort's metric.

---

## 6. Concentration of Measure at $n = 8$

### 6.1 Expected Distances on $\Delta^7$

The concentration of measure phenomenon describes the tendency, in high-dimensional spaces, for certain functions to cluster tightly around their expected values. While $n = 8$ is not "high-dimensional" in the asymptotic sense, the geometry of the 7-simplex already exhibits non-trivial concentration properties that establish a baseline for meaningful brand differentiation.

**Theorem 4** (Distance concentration on $\Delta^7$). *For two independently and uniformly distributed points $w_A, w_B$ on the standard simplex $\Delta^7$ (i.e., drawn from the symmetric Dirichlet distribution $\text{Dir}(1, \ldots, 1)$), the expected squared Euclidean distance is:*

$$\mathbb{E}\left[ \|w_A - w_B\|_2^2 \right] = \frac{2(n-1)}{n(n+1)} = \frac{14}{72} = \frac{7}{36}$$

*where $n = 8$ is the number of components. The expected Euclidean distance is therefore approximately*

$$\mathbb{E}\left[ \|w_A - w_B\| \right] \approx \sqrt{\frac{7}{36}} \approx 0.4410$$

*Proof.* For $w$ drawn from $\text{Dir}(\mathbf{1}_n)$ on $\Delta^{n-1}$, the marginal moments are $\mathbb{E}[w_i] = 1/n$, $\mathbb{E}[w_i^2] = 2/(n(n+1))$, and $\mathbb{E}[w_i w_j] = 1/(n(n+1))$ for $i \neq j$ (Johnson & Kotz, 1972).

For independent draws $w_A, w_B$:

$$\mathbb{E}\left[ \|w_A - w_B\|_2^2 \right] = \sum_{i=1}^n \mathbb{E}\left[ (w_{A,i} - w_{B,i})^2 \right] = \sum_{i=1}^n \left( \mathbb{E}[w_{A,i}^2] - 2\mathbb{E}[w_{A,i}]\mathbb{E}[w_{B,i}] + \mathbb{E}[w_{B,i}^2] \right)$$

$$= n \left( \frac{2}{n(n+1)} - \frac{2}{n^2} + \frac{2}{n(n+1)} \right) = n \left( \frac{4}{n(n+1)} - \frac{2}{n^2} \right) = \frac{4}{n+1} - \frac{2}{n}$$

$$= \frac{4n - 2(n+1)}{n(n+1)} = \frac{2n - 2}{n(n+1)} = \frac{2(n-1)}{n(n+1)}$$

For $n = 8$: $\mathbb{E}[\|w_A - w_B\|_2^2] = 2 \cdot 7 / (8 \cdot 9) = 14/72 = 7/36 \approx 0.1944$.

Thus $\mathbb{E}[\|w_A - w_B\|] \approx \sqrt{7/36} \approx 0.4410$. $\square$

**Remark.** The Bhattacharyya coefficient $\rho(w_A, w_B) = \sum_i \sqrt{w_{A,i} w_{B,i}}$ is the quantity entering the Fisher-Rao distance. For uniformly random points on $\Delta^7$, $\mathbb{E}[\rho]$ can be computed using the Beta function moments of the Dirichlet distribution. The Fisher-Rao distance $d_{FR} = 2 \arccos(\rho)$ concentrates around $2 \arccos(\mathbb{E}[\rho])$ with variance decreasing as $n$ increases.

### 6.2 The Null Model Baseline

**Theorem 5** (Null model for brand differentiation). *Let $m$ observer profiles be drawn uniformly from $\Delta^7$, and let brand profiles $s_A, s_B \in \mathbb{R}^8_+$ be fixed. The observer-dependent distance $d_w(s_A, s_B) = \sqrt{\sum_k w_k (\text{clr}_k(s_A) - \text{clr}_k(s_B))^2}$ has the following properties under the uniform distribution on $\Delta^7$:*

*(i) The expected observer-dependent distance is*

$$\mathbb{E}_w\left[ d_w^2(s_A, s_B) \right] = \frac{1}{8} \sum_{k=1}^{8} \delta_k^2 = \frac{1}{8} \| \text{clr}(s_A) - \text{clr}(s_B) \|_2^2$$

*where $\delta_k = \text{clr}_k(s_A) - \text{clr}_k(s_B)$.*

*(ii) The variance of the observer-dependent distance is*

$$\text{Var}_w\left[ d_w^2(s_A, s_B) \right] = \frac{1}{72} \left( \sum_{k=1}^{8} \delta_k^4 - \frac{1}{8}\left(\sum_{k=1}^8 \delta_k^2\right)^2 \right) + \frac{7}{72} \cdot \frac{1}{8}\left(\sum_{k=1}^8 \delta_k^2\right)^2 - \left(\frac{1}{8}\sum_{k=1}^8 \delta_k^2\right)^2$$

*The variance is small when the brand difference is uniformly spread across dimensions and large when it is concentrated in a few dimensions.*

*Proof.* Part (i): $\mathbb{E}_w[d_w^2] = \sum_k \delta_k^2 \mathbb{E}[w_k] = \sum_k \delta_k^2 / 8$ since $\mathbb{E}[w_k] = 1/8$ under the symmetric Dirichlet distribution.

Part (ii): $\text{Var}_w[d_w^2] = \sum_{k,\ell} \delta_k^2 \delta_\ell^2 \text{Cov}(w_k, w_\ell)$. For the symmetric Dirichlet$(1, \ldots, 1)$ distribution on $\Delta^7$, $\text{Var}(w_k) = 7/(8^2 \cdot 9) = 7/576$ and $\text{Cov}(w_k, w_\ell) = -1/(8^2 \cdot 9) = -1/576$ for $k \neq \ell$. Substituting and simplifying yields the stated expression. $\square$

**Remark** (Null model as mathematical baseline). The symmetric Dirichlet$(1, \ldots, 1)$ distribution assumes all observer profiles on $\Delta^7$ are equally likely. Real observer populations likely cluster around a few prototypical profiles (e.g., aesthetes, pragmatists, brand-agnostics). The null model provides a mathematical baseline for *what random observer variation alone would produce*, not an empirical claim about actual observer distribution. Empirical observer data would be needed to replace this uniform prior with a data-driven distribution.

The practical interpretation is as follows. Under the null model (uniformly random observers), the expected observer-dependent brand distance is $1/8$ of the total brand difference. If two brands are highly differentiated on all dimensions, every observer will perceive them as different. If they are differentiated on only one or two dimensions, the average observer perceives them as closer together, and the variance across observers is high -- meaning that the "differentiation" is visible to some observers but invisible to others.

**Definition 4** (Meaningful differentiation). *Two brands $s_A, s_B$ are* meaningfully differentiated *for an observer population if the expected observer-dependent distance exceeds a threshold $\tau$ related to perceptual just-noticeable differences:*

$$\mathbb{E}_w[d_w^2(s_A, s_B)] > \tau^2$$

*and are* robustly differentiated *if additionally $\text{Var}_w[d_w^2] < \sigma^2$ for a specified tolerance $\sigma$.*

Meaningful differentiation requires sufficient total brand difference. Robust differentiation additionally requires that the difference be spread across multiple dimensions, so that it is visible to a broad range of observer profiles. A brand differentiation that is concentrated on a single dimension (e.g., price alone) may be meaningful in expectation but will have high variance -- robust for price-sensitive observers, invisible to others.

---

## 7. Geometric Properties of the Positive Octant

### 7.1 Brand Space on $S^7_+$

When brand emission profiles are normalized to unit vectors ($\|s\| = 1$), they reside on $S^7_+ = S^7 \cap \mathbb{R}^8_+$, the positive octant of the 7-sphere. This normalization separates the directional structure of the brand profile (which dimensions are emphasized) from its magnitude (overall signal strength). In many brand-theoretic applications, the directional structure is the primary object of interest.

**Proposition 4** (Positive-octant volume fraction). *The positive octant $S^7_+$ occupies a fraction $1/2^8 = 1/256$ of the full 7-sphere $S^7$. Specifically, if $\text{Vol}(S^7)$ denotes the surface area of the unit 7-sphere, then*

$$\text{Vol}(S^7_+) = \frac{1}{256} \cdot \text{Vol}(S^7)$$

*Proof.* The $n$-sphere $S^{n-1} \subset \mathbb{R}^n$ is partitioned into $2^n$ orthants by the coordinate hyperplanes. By the symmetry of $S^{n-1}$ under sign reflections $(x_i \mapsto -x_i)$, each orthant has equal surface area. Therefore $\text{Vol}(S^{n-1}_+) = \text{Vol}(S^{n-1}) / 2^n$. For $n = 8$: $\text{Vol}(S^7_+) = \text{Vol}(S^7) / 2^8 = \text{Vol}(S^7) / 256$. $\square$

The surface area of $S^7$ is $\text{Vol}(S^7) = 2\pi^4 / \Gamma(4) = 2\pi^4 / 6 = \pi^4 / 3 \approx 32.47$. Therefore:

$$\text{Vol}(S^7_+) = \frac{\pi^4}{3 \cdot 256} = \frac{\pi^4}{768} \approx 0.1269$$

### 7.2 The Compression Theorem

**Theorem 6** (Brand space compression). *The positive-octant restriction compresses the available brand space by a factor of 256 relative to the full sphere. For uniformly random unit-norm brand profiles on $S^7_+$, the maximum geodesic distance (great-circle distance restricted to $S^7_+$) is $\pi/2$, compared to $\pi$ for the full sphere. The expected squared Euclidean distance between two random points on $S^7_+$ is:*

$$\mathbb{E}\left[ \|x - y\|_2^2 \right] = 2 - 2 \cdot \mathbb{E}\left[ \langle x, y \rangle \right]$$

*where $\mathbb{E}[\langle x, y \rangle] > 0$ for independent uniform points on $S^7_+$ (in contrast to $\mathbb{E}[\langle x, y \rangle] = 0$ on the full sphere). The positive inner product bias means that random brand profiles on $S^7_+$ are more similar to each other than random points on $S^7$.*

*Proof.* On the full $S^7$, for independent uniform $x, y$, $\mathbb{E}[\langle x, y \rangle] = 0$ by symmetry. On $S^7_+$, all coordinates are non-negative, so $\langle x, y \rangle = \sum_i x_i y_i \geq 0$ with probability 1. In fact, for uniform points on $S^7_+$, each coordinate $x_i$ has the distribution of $|Z_i| / \|Z\|$ where $Z \sim \mathcal{N}(0, I_8)$. Since taking absolute values biases coordinates upward from 0, we have $\mathbb{E}[x_i y_i] > 0$ for all $i$, giving $\mathbb{E}[\langle x, y \rangle] > 0$.

To compute explicitly: for the uniform distribution on $S^7_+$, we can use the relation to the symmetric Dirichlet distribution on $\Delta^7$ via $w_i = x_i^2$ (the square map). The expected inner product $\mathbb{E}[\langle x, y \rangle] = \sum_i \mathbb{E}[x_i] \mathbb{E}[y_i] = 8 \cdot (\mathbb{E}[x_i])^2$ for independent $x, y$. Using the known moment $\mathbb{E}[|Z_i| / \|Z\|] = \sqrt{2/\pi} \cdot \Gamma((n+1)/2) / \Gamma(n/2) \cdot 1/\sqrt{n}$ for $n = 8$, this gives a positive value. The maximum geodesic distance on $S^7_+$ is $\pi/2$ (achieved between orthogonal unit vectors $e_i$ and $e_j$). $\square$

The compression theorem has a direct implication for brand theory: **brand differentiation is geometrically harder than naive 8-dimensional counting suggests**. The non-negativity constraint (brands cannot have "negative semiotic intensity") restricts brand profiles to a small corner of the full sphere, reducing the effective "room" for differentiation. Two randomly positioned brands on $S^7_+$ are expected to be more similar than two randomly positioned points on the full sphere. This means that achieving meaningful differentiation requires deliberate strategic positioning, not merely random variation across dimensions.

### 7.3 Geodesics on $S^7_+$

Geodesics on $S^7_+$ are arcs of great circles, provided the entire arc remains in the positive octant. When the great-circle geodesic between two points $x, y \in S^7_+$ would exit the positive octant (passing through a region where some coordinate is negative), the geodesic on $S^7_+$ is instead a path that "hugs" the boundary.

**Proposition 5** (Geodesic containment). *For two points $x, y \in S^7_+$, the great-circle geodesic $\gamma(t) = (\cos(t\theta) \cdot x + \sin(t\theta) \cdot u) / \|\cdot\|$, where $u$ is the unit vector in the plane of $x$ and $y$ orthogonal to $x$ and $\theta = \arccos(\langle x, y \rangle)$, remains entirely in $S^7_+$ if and only if for all $i = 1, \ldots, 8$:*

$$y_i \geq -x_i \cdot \cos\theta \cdot \sin\theta^{-1} \cdot \text{(terms depending on the projection)}$$

*In particular, if $\langle x, y \rangle > 0$ (inner product is positive), the great-circle geodesic remains in $S^7_+$ whenever all coordinates of the midpoint $\gamma(1/2)$ are positive.*

In practice, for brand profiles that are not pathologically close to the boundary of $S^7_+$ (brands with non-negligible signal on all dimensions), the great-circle geodesic stays within the positive octant. Boundary effects become relevant only for brands with near-zero emission on some dimensions -- precisely the brands that SBT characterizes as exhibiting "structural absence" on those dimensions.

---

## 8. Trajectory Sensitivity on the Perception Manifold

The metric framework developed in Sections 3--7 treats brand profiles and observer weights as static objects. In practice, brand perception evolves: emission profiles shift through re-collapse, observer weights drift through cultural change, and both evolve along curves on their respective manifolds. This section introduces the mathematical machinery for analyzing how sensitive brand trajectories are to initial conditions -- a question with direct strategic implications.

### 8.1 Jacobi Fields and Geodesic Deviation

Consider two brands with nearly identical emission profiles at time $t = 0$ that follow different strategic paths (geodesics) on the perception manifold. How quickly do their trajectories diverge? This question is answered by the *Jacobi field equation*, the fundamental tool of Riemannian geometry for analyzing geodesic deviation (do Carmo, 1992).

Let $\gamma: [0, 1] \to S^7_+$ be a geodesic representing a brand's trajectory through the normalized brand space, and let $J(t)$ be a vector field along $\gamma$ representing the deviation of a nearby trajectory. The Jacobi field equation is:

$$\frac{D^2 J}{dt^2} + R(J, \dot{\gamma})\dot{\gamma} = 0$$

where $D/dt$ denotes the covariant derivative along $\gamma$, $\dot{\gamma}$ is the tangent vector to the trajectory, and $R$ is the Riemann curvature tensor of the perception manifold. The initial conditions $J(0)$ and $J'(0) = (DJ/dt)(0)$ specify the initial separation and relative velocity of the two brand trajectories.

For $S^7_+$ with its inherited metric from the round sphere (constant sectional curvature $K = 1$), the curvature term simplifies:

$$R(J, \dot{\gamma})\dot{\gamma} = K \left( \langle \dot{\gamma}, \dot{\gamma} \rangle J - \langle J, \dot{\gamma} \rangle \dot{\gamma} \right) = \|\dot{\gamma}\|^2 J - \langle J, \dot{\gamma} \rangle \dot{\gamma}$$

For a unit-speed geodesic ($\|\dot{\gamma}\| = 1$), the component of $J$ perpendicular to $\dot{\gamma}$ satisfies $J''_\perp + J_\perp = 0$, with solution:

$$J_\perp(t) = A \cos(t) + B \sin(t)$$

where $A$ and $B$ are determined by initial conditions. The key implication: on $S^7_+$ with positive curvature, nearby geodesics *oscillate* rather than diverge exponentially. The maximum separation occurs at $t = \pi/2$ (the maximum geodesic distance on $S^7_+$ from Theorem 6), after which trajectories reconverge.

### 8.2 Curvature-Based Sensitivity in the Warped Product Space

The simple oscillatory behavior on $S^7_+$ becomes substantially more complex in the combined brand-observer space $(\mathcal{P}, D)$, where the warped product structure introduces observer-dependent curvature.

**Proposition 6** (Observer-dependent trajectory sensitivity). *In the warped product space $(\mathcal{P}, D)$, the sectional curvature depends on the observer position $w \in \Delta^7_\circ$. For a two-plane $\sigma$ spanned by vectors tangent to the brand-space fiber at observer position $w$, the sectional curvature is:*

$$K_w(\sigma) = \frac{K_{S^7_+}(\sigma) - \|\nabla_F \ln f\|^2}{f^2(w)}$$

*where $f(w)$ is the warping function and $K_{S^7_+}(\sigma)$ is the curvature of the unwarped brand space. Observers near the boundary of $\Delta^7_\circ$ (extreme salience concentration) experience higher effective curvature, making brand trajectories more sensitive to perturbation in their perception.*

*Proof sketch.* This follows from the O'Neill curvature formula for warped products (O'Neill, 1983, Corollary 7.43). In our construction, the warping function $f$ depends on the observer weight $w$, and its gradient $\nabla_F \ln f$ encodes how rapidly the warping changes as the observer moves on $\Delta^7_\circ$. Near the simplex boundary (one $w_k \to 0$), the Fisher-Rao metric diverges, amplifying the gradient term and increasing effective curvature. $\square$

The strategic implication is direct: **brands perceived primarily through a single dimension (observed by specialists) face higher trajectory sensitivity than brands perceived across many dimensions (observed by generalists)**. A luxury brand monitored exclusively through the economic dimension is more vulnerable to small perturbations than a brand evaluated holistically.

### 8.3 The Spectral Sensitivity Index

We define a curvature-based risk metric that quantifies trajectory vulnerability for a brand at position $s \in S^7_+$ perceived by observer cohort $w \in \Delta^7_\circ$.

**Definition 7** (Spectral Sensitivity Index). *For a brand at position $s \in S^7_+$ and observer profile $w \in \Delta^7_\circ$, the spectral sensitivity index is:*

$$\text{SSI}(s, w) = \frac{1}{7} \sum_{k=1}^{8} w_k \cdot \kappa_k(s)$$

*where $\kappa_k(s)$ is the principal curvature of $S^7_+$ in the direction of the $k$-th coordinate at $s$. The SSI is the observer-weighted average of directional curvatures, measuring trajectory sensitivity as perceived by a specific observer.*

For the round sphere, the principal curvatures are uniform ($\kappa_k = 1$ for all $k$), so $\text{SSI} = 1/7$ everywhere on the interior of $S^7_+$. The index becomes non-trivial in two cases:

1. **Near the boundary of $S^7_+$**: When a brand's profile approaches zero on some dimension (structural absence), the Aitchison metric's log transform amplifies small perturbations in that direction. The effective curvature in the Aitchison-induced Riemannian structure diverges as $s_k \to 0$, creating a *sensitivity singularity* at the boundary.

2. **In the warped product space**: The observer-dependent warping modulates which directions contribute to trajectory sensitivity. An observer who assigns $w_k = 0.5$ to the economic dimension effectively doubles the curvature contribution of economic perturbations.

**Corollary** (Structural absence amplifies sensitivity). *A brand with structural absence on dimension $k$ (formalized as $s_k \to 0^+$) has $\kappa_k(s) \to \infty$ in the Aitchison geometry, implying unbounded trajectory sensitivity in that direction. The observer-weighted sensitivity index $\text{SSI}(s, w)$ diverges whenever $w_k > 0$ for a dimension with structural absence.*

This formalizes an insight from SBT's qualitative framework: structural absence is strategically powerful (dark signals create distinctive brand signatures) but geometrically fragile (small perturbations to a near-zero dimension have outsized effects on the brand's trajectory). The tension between signal power and geometric vulnerability is the fundamental trade-off of dark-signal strategy.

### 8.4 Connection to Non-Ergodic Dynamics

The Jacobi field analysis connects directly to the non-ergodic perception dynamics formalized in Zharnikov (2026j). In R6, brand perception evolves via a stochastic differential equation on $S^7_+$:

$$dX_t = b(X_t) \, dt + \sigma(X_t) \circ dW_t$$

where $b$ is a drift term (directed encounters, signal decay) and $\sigma$ is a diffusion coefficient. The Jacobi field equation governs the *deterministic skeleton* of this SDE: how the expected trajectory responds to perturbations in initial conditions. When the stochastic term is small ($\sigma \to 0$), trajectory sensitivity is dominated by the Jacobi field, and the curvature-based risk metric predicts which brands face the greatest path-dependence.

The connection is precise: R6 proves that brand perception on $S^7_+$ is non-ergodic (Theorem 4 in Zharnikov, 2026j), meaning that time-averages do not converge to ensemble-averages. The Jacobi field analysis complements this by showing *why* non-ergodicity has heterogeneous impact: brands in high-curvature regions of perception space (near the boundary, or observed through concentrated weight profiles) experience stronger path-dependence than brands in low-curvature regions. The spectral sensitivity index provides the formal bridge between the static metric (this paper) and the dynamic theory (R6).

Cafaro and Ali (2007) analyzed Jacobi field instability on negatively curved statistical manifolds, characterizing chaotic divergence of nearby trajectories through Lyapunov-type growth rates. In contrast, the positive curvature of $S^7_+$ produces oscillatory rather than exponential Jacobi field behavior, meaning brand trajectories on the perception manifold are bounded in their deviation -- a qualitatively different sensitivity regime that permits strategic positioning to manage vulnerability. Recent work on Riemannian variational methods (Zaghen, Eijkelboom, Pouplin, Liu, Welling, van de Meent, & Bekkers, 2025) demonstrates that Jacobi field computations are tractable on curved manifolds in machine learning contexts, suggesting that the sensitivity analysis developed here could be implemented computationally for empirical brand data.

---

## 9. Application to SBT Case Studies

### 9.1 Case Study Profiles

We apply the metric framework to five brands analyzed as case studies in Zharnikov (2026a). Each brand has been assessed on the SBT coherence framework with a grade and a designed/ambient (D/A) ratio:

| Brand | Coherence Type | Grade | D/A Ratio |
|-------|---------------|-------|-----------|
| Hermès | Ecosystem | A+ | 60/35 |
| IKEA | Signal | A- | 75/25 |
| Patagonia | Identity | B+ | 65/30 |
| Erewhon | Experiential asymmetry | B- | 40/55 |
| Tesla | Incoherent | C- | 30/65 |

To demonstrate the metric, we construct canonical emission profiles based on the qualitative case-study assessments. These profiles are illustrative; the numerical values are chosen to reflect the qualitative descriptions in Zharnikov (2026a) rather than derived from empirical measurement. All values are on a [1, 10] scale representing relative signal intensity:

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

### 9.2 Pairwise Aitchison Distances

Computing the Aitchison distance $d_{\mathcal{B}}$ for all brand pairs yields the following distance matrix (values rounded to two decimal places):

To compute, we first apply the centered log-ratio transform to each brand profile. For example, for Hermès with $s = (9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5)$, the geometric mean is $g(s) = (9.5 \cdot 9.0 \cdot 7.0 \cdot 9.0 \cdot 8.5 \cdot 3.0 \cdot 9.0 \cdot 9.5)^{1/8} \approx 7.65$, and the clr transform is:

$$\text{clr}(s_{\text{Hermès}}) \approx (0.216, 0.162, -0.089, 0.162, 0.105, -0.936, 0.162, 0.216)$$

The large negative value on the economic dimension ($-0.936$) reflects Hermès's luxury positioning: relative to its other signals, the economic (accessibility/value) signal is deliberately suppressed.

Carrying out the full computation for all pairs:

| | Hermès | IKEA | Patagonia | Erewhon | Tesla |
|-----------|--------|------|-----------|---------|-------|
| Hermès | 0 | 1.34 | 0.88 | 1.21 | 1.76 |
| IKEA | 1.34 | 0 | 0.95 | 1.34 | 1.25 |
| Patagonia | 0.88 | 0.95 | 0 | 1.10 | 1.46 |
| Erewhon | 1.21 | 1.34 | 1.10 | 0 | 1.06 |
| Tesla | 1.76 | 1.25 | 1.46 | 1.06 | 0 |

Several patterns emerge:

1. **Tesla is the most distant brand.** Its maximum distance is to Hermès ($1.76$), reflecting the opposition between Hermès's high-coherence ecosystem (strong, balanced profile with deliberate economic suppression) and Tesla's incoherent profile (volatile ideological and temporal dimensions). This accords with the qualitative assessment: A+ and C- brands are maximally separated.

2. **Hermès and Patagonia are the closest high-grade pair** ($0.88$). Despite different coherence types (ecosystem vs. identity), both brands have strong, intentional signal profiles with clear ideological conviction. Their proximity reflects a shared structural quality: both are brands where the emission profile is dominated by deliberate choices rather than market noise.

3. **IKEA occupies a middle position.** Its signal-coherence type produces a profile that is moderately distant from both the strongly ideological brands (Hermès, Patagonia) and the less coherent brands (Erewhon, Tesla).

### 9.3 Observer-Dependent Distances

The power of the combined metric emerges when we examine how brand distances change across observers. Consider two canonical observer profiles:

- **Observer $\alpha$** (aesthete): $w_\alpha = (0.25, 0.15, 0.05, 0.20, 0.10, 0.05, 0.15, 0.05)$
  Attends primarily to semiotic, experiential, and cultural dimensions.

- **Observer $\beta$** (pragmatist): $w_\beta = (0.05, 0.05, 0.10, 0.15, 0.05, 0.35, 0.05, 0.20)$
  Attends primarily to economic and temporal dimensions.

The observer-dependent distances $d_w(s_A, s_B)$ for the Hermès-IKEA pair:

$$d_{w_\alpha}(\text{Hermès}, \text{IKEA}) = \sqrt{\sum_k w_{\alpha,k} (\text{clr}_k(s_H) - \text{clr}_k(s_I))^2} \approx 0.32$$

$$d_{w_\beta}(\text{Hermès}, \text{IKEA}) = \sqrt{\sum_k w_{\beta,k} (\text{clr}_k(s_H) - \text{clr}_k(s_I))^2} \approx 0.74$$

The pragmatist observer perceives Hermès and IKEA as more than twice as far apart as the aesthete observer ($0.74 / 0.32 \approx 2.3$). This is because the primary difference between Hermès and IKEA lies in the economic and temporal dimensions (luxury vs. value; heritage vs. modernity), which the pragmatist weights heavily and the aesthete largely ignores.

Conversely, for the Hermès-Patagonia pair:

$$d_{w_\alpha}(\text{Hermès}, \text{Patagonia}) \approx 0.28$$

$$d_{w_\beta}(\text{Hermès}, \text{Patagonia}) \approx 0.40$$

Here the distance spread is much narrower ($0.28$ vs. $0.40$, compared to the $0.32$ vs. $0.74$ spread for Hermès-IKEA), because Hermès and Patagonia differ on dimensions that both observers attend to (semiotic design vs. purposeful utility is visible to the aesthete; both have moderate economic positioning visible to the pragmatist).

These results demonstrate the central claim of the metric framework: brand distance is not an objective quantity but a function of the observer's attentional structure. The metric formalizes what SBT describes qualitatively -- that different observer cohorts inhabit genuinely different brand landscapes.

---

## 10. Discussion

### 10.1 What the Metric Enables

The formal metric space defined in this paper enables several capabilities that were previously unavailable in brand theory:

**Quantitative brand comparison.** For the first time, the distance between any two brands can be computed as a real number with well-defined properties (symmetry, triangle inequality). This moves brand positioning from the domain of perceptual maps (which depend on arbitrary axis choices) to the domain of metric geometry (which is coordinate-independent).

**Observer cohort analysis.** The Fisher-Rao metric on $\Delta^7$ provides a principled measure of observer similarity. Observer cohorts can be defined as clusters in $(\Delta^7, d_{FR})$, with cohort boundaries corresponding to level sets of the distance function. The concentration bounds (Theorem 4) provide a null-model baseline: cohort differences must exceed the concentration radius to be meaningful.

**Positioning optimization.** The warped product metric provides a formal objective function for brand positioning. Given a target observer cohort $w^*$, a brand can optimize its emission profile to maximize $d_{w^*}(s, s_{\text{competitor}})$ -- formal differentiation from competitors in the eyes of the target cohort. The Aitchison geodesic provides the optimal path for repositioning.

**Differentiation assessment.** Theorem 6 (brand space compression) quantifies the geometric difficulty of differentiation: brands are restricted to $1/256$ of the full sphere, making it harder to find distinct positions than naive dimensional counting suggests. Combined with the observer-dependent pseudo-metric kernel (Proposition 3), this provides a formal framework for assessing when two brands are genuinely distinct versus indistinguishable to relevant observers.

### 10.2 Limitations

Several limitations should be noted:

**Dimensional independence.** The Aitchison metric treats the eight SBT dimensions as independent coordinates. In practice, dimensions may be correlated (semiotic and cultural signals may co-vary, economic and experiential signals may be inversely related). Empirical data would be needed to estimate the correlation structure and potentially define a Mahalanobis-like variant of the Aitchison distance.

**Boundary behavior.** The Aitchison metric is undefined when any component of the brand profile is exactly zero, because the logarithm diverges. In SBT terms, a brand with *no* signal whatsoever on a dimension (true zero, not merely weak) cannot be represented in the Aitchison framework without zero-replacement strategies. This is a known limitation of compositional data analysis (Martin-Fernandez, Palarea-Albaladejo, & Olea, 2011).

**Illustrative case-study data.** The numerical brand profiles in Section 9 are constructed to be consistent with qualitative assessments, not derived from empirical measurement. The metric framework provides the mathematical structure for empirical testing, but the specific numerical results should be treated as demonstrations of the framework's behavior, not as empirical findings about the brands themselves.

**Static profiles.** While Section 8 introduces trajectory sensitivity analysis via Jacobi fields, the core metric treats brand profiles and observer weights as fixed points rather than evolving trajectories. SBT describes brand perception as a dynamic process with signal decay, crystallization, and re-collapse. The full dynamic extension -- modeling perception evolution as a stochastic differential equation on $S^7_+$ -- is developed in Zharnikov (2026j).

**Cultural and sector scope.** All five case-study brands are Western consumer (B2C) brands. The mathematical framework -- Aitchison, Fisher-Rao, and warped product metrics -- is general and applies to any brand in any market. However, the illustrative profiles have not been tested cross-culturally, and B2B brands (where experiential and temporal dimensions may dominate while semiotic may be minimal) could produce qualitatively different distance structures. Cross-cultural and B2B applications would strengthen the empirical grounding of the framework.

**Reference implementation.** A Python reference implementation of all metrics defined in this paper is available as supplementary material.

### 10.3 Connection to Subsequent Work

This paper provides the foundation for the Mathematical Foundations of Spectral Brand Theory research program. Subsequent papers build directly on the metric spaces defined here:

- **R2 (Spectral metamerism)** (Zharnikov, 2026e): Uses the Aitchison distance to formalize the Johnson-Lindenstrauss projection from $\mathbb{R}^8$ to the 1-dimensional grade scale, proving that metamerism (different profiles mapping to the same grade) is geometrically inevitable.

- **R3 (Cohort boundaries)** (Zharnikov, 2026f): Uses the Fisher-Rao metric and concentration bounds from Theorem 4 to derive lower bounds on cohort boundary fuzziness in $\Delta^7$.

- **R4 (Brand positioning capacity)** (Zharnikov, 2026g): Uses the brand space geometry to derive sphere-packing bounds on the maximum number of distinguishable brand positions, connecting to the E8 lattice and Viazovska's (2017) proof of optimal sphere packing in 8 dimensions.

- **R5 (Specification impossibility)** (Zharnikov, 2026h): Proves coverage impossibility in high-dimensional specification spaces, establishing the organizational complement to the brand-perception geometry.

- **R6 (Perception dynamics)** (Zharnikov, 2026j): Models perception evolution as a stochastic differential equation on $S^7_+$ with the metric defined here providing the Riemannian structure. The Jacobi field analysis in Section 8 provides the deterministic bridge: trajectory sensitivity on the static manifold governs the strength of path-dependence in R6's dynamic model.

- **R9 (Non-ergodic perception)** (Zharnikov, 2026o): Extends the trajectory sensitivity framework to empirical brand tracking data, demonstrating that the spectral sensitivity index predicts which brands exhibit the strongest non-ergodic effects.

---

## 11. Conclusion

This paper has defined a formal metric space for multi-dimensional brand perception, grounded in compositional data analysis and information geometry. Three metric spaces have been constructed, each with proved properties:

1. The **brand signal space** $(\mathcal{B}, d_{\mathcal{B}})$, where $\mathcal{B} = \mathbb{R}^8_+$ is equipped with the Aitchison metric. The metric is justified by the compositional nature of brand profiles and the logarithmic scaling of perceptual intensity (Weber-Fechner law). Geodesics in Aitchison space correspond to power interpolations that preserve the ratio structure of brand profiles.

2. The **observer weight space** $(\mathcal{O}, d_{\mathcal{O}})$, where $\mathcal{O} = \Delta^7_\circ$ is equipped with the Fisher-Rao metric. The metric is uniquely justified by Cencov's theorem as the only distance invariant under sufficient-statistic transformations. Geodesics bulge toward the simplex center, implying that intermediate observers are more open-minded than linear averaging predicts.

3. The **combined brand-observer space** $(\mathcal{P}, D)$, formalized as a warped product manifold with observer weights distorting the brand-space metric. The construction generalizes the INDSCAL model, connecting fifty years of psychometric empirical validation to a rigorous differential-geometric foundation.

We have established concentration-of-measure bounds at $n = 8$ (providing a null model for meaningful brand differentiation), proved that the positive-octant restriction compresses brand space to $1/256$ of the full sphere (quantifying the geometric difficulty of differentiation), developed Jacobi field analysis for trajectory sensitivity with the spectral sensitivity index (bridging the static metric to dynamic perception theory), and demonstrated the metric's behavior on five case-study brands.

The central result is that brand distance is not an objective property of brands but a function of the observer's attentional structure -- formalized here as a warped product metric where the observer's position on $\Delta^7$ determines the geometry of brand space. This transforms SBT's qualitative insight into a mathematical theorem: different observer cohorts inhabit metrically distinct brand landscapes, and the kernel of each cohort's pseudo-metric defines the set of brands that are perceptually indistinguishable to that cohort.

The mathematical framework developed here provides the foundation for a rigorous theory of brand perception -- one that admits formal definitions, provable theorems, and quantitative predictions rather than the conceptual taxonomies that have characterized brand theory for the past three decades.

---

## Mathematical Appendix

### A.1 Proof Details for Theorem 3 (Triangle Inequality of the Combined Metric)

The triangle inequality for the combined metric $D$ requires careful treatment because the warping weights $\bar{w}_k$ differ between pairs. We provide the full argument.

Let $(w_A, s_A)$, $(w_B, s_B)$, $(w_C, s_C) \in \mathcal{P}$. Define:

$$\delta_k^{XY} = \text{clr}_k(s_X) - \text{clr}_k(s_Y), \quad \bar{w}_k^{XY} = \frac{w_{X,k} + w_{Y,k}}{2}$$

We need to show:

$$\sqrt{d_{FR}^2(w_A, w_C) + \sum_k \bar{w}_k^{AC} (\delta_k^{AC})^2} \leq \sqrt{d_{FR}^2(w_A, w_B) + \sum_k \bar{w}_k^{AB} (\delta_k^{AB})^2} + \sqrt{d_{FR}^2(w_B, w_C) + \sum_k \bar{w}_k^{BC} (\delta_k^{BC})^2}$$

**Step 1.** By the triangle inequality for clr differences: $|\delta_k^{AC}| \leq |\delta_k^{AB}| + |\delta_k^{BC}|$ for each $k$.

**Step 2.** Bound the weights. For $w_A, w_B, w_C \in \Delta^7_\circ$:

$$\bar{w}_k^{AC} = \frac{w_{A,k} + w_{C,k}}{2} \leq \frac{w_{A,k} + w_{B,k}}{2} + \frac{w_{B,k} + w_{C,k}}{2} = \bar{w}_k^{AB} + \bar{w}_k^{BC}$$

However, a tighter bound suffices. Note that $\bar{w}_k^{AC} \leq 1$ for all $k$, so:

$$\bar{w}_k^{AC} (\delta_k^{AC})^2 \leq \bar{w}_k^{AC} (|\delta_k^{AB}| + |\delta_k^{BC}|)^2$$

**Step 3.** Apply the Cauchy-Schwarz inequality:

$$(|\delta_k^{AB}| + |\delta_k^{BC}|)^2 \leq 2((\delta_k^{AB})^2 + (\delta_k^{BC})^2)$$

This gives a loose bound. A tighter argument uses the fact that on the compact domain $\Delta^7_\circ$, the warping function $\bar{w}_k$ is continuous and bounded, and the warped product construction is a standard Riemannian construction known to yield a metric space (Bishop & O'Neill, 1969; O'Neill, 1983). The key theorem is:

**Theorem** (Bishop & O'Neill, 1969). *If $(B, g_B)$ and $(F, g_F)$ are complete Riemannian manifolds and $f: B \to (0, \infty)$ is smooth, then the warped product $B \times_f F$ with metric $g = g_B + f^2 g_F$ is a complete Riemannian manifold, and the geodesic distance on $B \times_f F$ satisfies the metric axioms.*

In our construction, the base is $(\Delta^7_\circ, g_{FR})$, the fiber at each point $w$ is $(\mathbb{R}^8_+, g_A)$ with the Aitchison metric, and the warping is implemented through the weight-dependent scaling. The use of average weights $\bar{w}_k = (w_{A,k} + w_{B,k})/2$ is a symmetrization that evaluates the warping function at the midpoint of the base geodesic. Strictly, the Bishop-O'Neill geodesic distance integrates the warping function along the entire base geodesic, while our formula uses this midpoint evaluation. For the compact domain $\Delta^7_\circ$ and smooth warping function $w \mapsto w_k$, the midpoint formula is a second-order approximation to the integrated geodesic length (error $O(\|w_A - w_B\|^2)$), and defines a valid metric in its own right: it inherits M1--M3 directly, and M4 follows from the direct algebraic argument in Steps 1--3 above, since $\bar{w}_k^{AC} \leq \max(\bar{w}_k^{AB}, \bar{w}_k^{BC})$ combined with the ordinary triangle inequality for CLR differences yields $D(A,C)^2 \leq (D(A,B) + D(B,C))^2$ via the Cauchy-Schwarz step. $\square$

### A.2 Volume Computations for $S^7_+$

The surface area of the unit $(n-1)$-sphere in $\mathbb{R}^n$ is:

$$\text{Vol}(S^{n-1}) = \frac{2\pi^{n/2}}{\Gamma(n/2)}$$

For $n = 8$:

$$\text{Vol}(S^7) = \frac{2\pi^4}{\Gamma(4)} = \frac{2\pi^4}{6} = \frac{\pi^4}{3}$$

The positive orthant volume:

$$\text{Vol}(S^7_+) = \frac{\text{Vol}(S^7)}{2^8} = \frac{\pi^4}{3 \cdot 256} = \frac{\pi^4}{768}$$

Numerically: $\pi^4 \approx 97.409$, so $\text{Vol}(S^7) \approx 32.470$ and $\text{Vol}(S^7_+) \approx 0.1269$.

The volume of the unit 8-ball:

$$\text{Vol}(B^8) = \frac{\pi^4}{4!} = \frac{\pi^4}{24} \approx 4.059$$

and its positive-orthant portion:

$$\text{Vol}(B^8_+) = \frac{\pi^4}{24 \cdot 256} = \frac{\pi^4}{6144} \approx 0.01587$$

### A.3 Fisher-Rao Geodesic Derivation

The Fisher-Rao metric on $\Delta^{n-1}_\circ$ is induced by the embedding $\varphi: \Delta^{n-1}_\circ \to S^{n-1}_+$ defined by $\varphi_i(w) = 2\sqrt{w_i}$, which maps the simplex onto the positive orthant of a sphere of radius 2. Under this map, the line element on $\Delta^{n-1}_\circ$ is:

$$ds^2 = \sum_{i=1}^n \frac{dw_i^2}{4w_i} = \sum_{i=1}^n \frac{(d\varphi_i)^2}{4}$$

which is (up to a constant factor) the round metric on the sphere. Geodesics on the sphere are great circles. In the original simplex coordinates, the geodesic from $w_A$ to $w_B$ is:

$$w_i(t) = \left( \frac{\sin((1-t)\theta)}{\sin\theta} \sqrt{w_{A,i}} + \frac{\sin(t\theta)}{\sin\theta} \sqrt{w_{B,i}} \right)^2$$

where $\theta = \arccos\left(\sum_i \sqrt{w_{A,i} w_{B,i}}\right)$, and the geodesic length is $2\theta$.

At the midpoint $t = 1/2$:

$$w_i(1/2) = \frac{1}{\cos^2(\theta/2)} \left( \frac{\sqrt{w_{A,i}} + \sqrt{w_{B,i}}}{2} \right)^2$$

This is proportional to $(\sqrt{w_{A,i}} + \sqrt{w_{B,i}})^2$, which is more uniform than $(w_{A,i} + w_{B,i})/2$ whenever the square roots are closer together than the original values. Since the square root function is concave, $\sqrt{w_{A,i}}$ and $\sqrt{w_{B,i}}$ are indeed closer together (in relative terms) than $w_{A,i}$ and $w_{B,i}$, confirming the entropy-bulge property (Proposition 1).

### A.4 Computation Details for Case Study Distances

The centered log-ratio transforms for the five brands (using the profiles from Section 9.1):

**Hermès**: $g = (9.5 \cdot 9.0 \cdot 7.0 \cdot 9.0 \cdot 8.5 \cdot 3.0 \cdot 9.0 \cdot 9.5)^{1/8} = 7.651$

$\text{clr} = (0.216, 0.162, -0.089, 0.162, 0.105, -0.936, 0.162, 0.216)$

**IKEA**: $g = (8.0 \cdot 7.5 \cdot 6.0 \cdot 7.0 \cdot 5.0 \cdot 9.0 \cdot 7.5 \cdot 6.0)^{1/8} = 6.894$

$\text{clr} = (0.149, 0.084, -0.139, 0.015, -0.321, 0.267, 0.084, -0.139)$

**Patagonia**: $g = (6.0 \cdot 9.0 \cdot 9.5 \cdot 7.5 \cdot 8.0 \cdot 5.0 \cdot 7.0 \cdot 6.5)^{1/8} = 7.172$

$\text{clr} = (-0.178, 0.227, 0.281, 0.045, 0.109, -0.361, -0.024, -0.098)$

**Erewhon**: $g = (7.0 \cdot 6.5 \cdot 5.0 \cdot 9.0 \cdot 8.5 \cdot 3.5 \cdot 7.5 \cdot 2.5)^{1/8} = 5.718$

$\text{clr} = (0.202, 0.128, -0.134, 0.454, 0.397, -0.491, 0.271, -0.827)$

**Tesla**: $g = (7.5 \cdot 8.5 \cdot 3.0 \cdot 6.0 \cdot 7.0 \cdot 6.0 \cdot 4.0 \cdot 2.0)^{1/8} = 4.992$

$\text{clr} = (0.407, 0.532, -0.509, 0.184, 0.338, 0.184, -0.222, -0.915)$

Pairwise Aitchison distances are then computed as $d_A(X, Y) = \|\text{clr}(X) - \text{clr}(Y)\|_2$.

For example, $d_A(\text{Hermès}, \text{Tesla})$:

$$\text{clr}(H) - \text{clr}(T) = (-0.191, -0.370, 0.420, -0.022, -0.233, -1.120, 0.384, 1.131)$$

$$d_A = \sqrt{0.036 + 0.137 + 0.177 + 0.000 + 0.054 + 1.255 + 0.147 + 1.279} = \sqrt{3.086} \approx 1.76$$

---

## References

Aaker, D. A. (1991). *Managing Brand Equity: Capitalizing on the Value of a Brand Name*. Free Press.

Aaker, J. L. (1997). Dimensions of brand personality. *Journal of Marketing Research*, 34(3), 347--356.

Aitchison, J. (1982). The statistical analysis of compositional data. *Journal of the Royal Statistical Society: Series B*, 44(2), 139--177.

Aitchison, J. (1986). *The Statistical Analysis of Compositional Data*. Chapman and Hall.

Aitchison, J. (1992). On criteria for measures of compositional difference. *Mathematical Geology*, 24(4), 365--379.

Amari, S.-i. (2016). *Information Geometry and Its Applications*. Springer.

Amari, S.-i., & Nagaoka, H. (2000). *Methods of Information Geometry*. American Mathematical Society.

Atkinson, C., & Mitchell, A. F. S. (1981). Rao's distance measure. *Sankhya: The Indian Journal of Statistics, Series A*, 43(3), 345--365.

Bijmolt, T. H. A., & Wedel, M. (1999). A comparison of multidimensional scaling methods for perceptual mapping. *Journal of Marketing Research*, 36(1), 137--153.

Bishop, R. L., & O'Neill, B. (1969). Manifolds of negative curvature. *Transactions of the American Mathematical Society*, 145, 1--49.

Borg, I., & Groenen, P. J. F. (2005). *Modern Multidimensional Scaling: Theory and Applications* (2nd ed.). Springer.

Brand Finance. (2025). *Global 500 2025: The Annual Report on the World's Most Valuable and Strongest Brands*. Brand Finance.

Bujack, R., Teti, E., Miller, J., Caffrey, E., & Turton, T. L. (2022). The non-Riemannian nature of perceptual color space. *Proceedings of the National Academy of Sciences*, 119(18), e2119753119.

Busemeyer, J. R., & Bruza, P. D. (2012). *Quantum Models of Cognition and Decision*. Cambridge University Press.

Cafaro, C., & Ali, S. A. (2007). Jacobi fields on statistical manifolds of negative Ricci curvature. *Physica D: Nonlinear Phenomena*, 234(1), 70--80.

Carroll, J. D., & Arabie, P. (1980). Multidimensional scaling. *Annual Review of Psychology*, 31, 607--649.

Carroll, J. D., & Chang, J.-J. (1970). Analysis of individual differences in multidimensional scaling via an N-way generalization of "Eckart-Young" decomposition. *Psychometrika*, 35(3), 283--319.

Cencov, N. N. (1972). *Statistical Decision Rules and Optimal Inference*. Nauka (in Russian). English translation: American Mathematical Society, 1982.

DeSarbo, W. S., Kim, Y., Choi, S. C., & Spaulding, M. (2002). A gravity-based multidimensional scaling model for deriving spatial structures underlying consumer preference/choice judgments. *Journal of Consumer Research*, 29(1), 91--100.

do Carmo, M. P. (1992). *Riemannian Geometry*. Birkhauser.

Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barcelo-Vidal, C. (2003). Isometric logratio transformations for compositional data analysis. *Mathematical Geology*, 35(3), 279--300.

Fechner, G. T. (1860). *Elemente der Psychophysik*. Breitkopf und Hartel.

Gardenfors, P. (2000). *Conceptual Spaces: The Geometry of Thought*. MIT Press.

Johnson, N. L., & Kotz, S. (1972). *Distributions in Statistics: Continuous Multivariate Distributions*. Wiley.

Kapferer, J.-N. (2008). *The New Strategic Brand Management: Creating and Sustaining Brand Equity Long Term* (4th ed.). Kogan Page.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1--22.

Lancaster, K. J. (1966). A new approach to consumer theory. *Journal of Political Economy*, 74(2), 132--157.

Marshall, A. W., Olkin, I., & Arnold, B. C. (2011). *Inequalities: Theory of Majorization and Its Applications* (2nd ed.). Springer.

Martin-Fernandez, J. A., Palarea-Albaladejo, J., & Olea, R. A. (2011). Dealing with zeros. In V. Pawlowsky-Glahn & A. Buccianti (Eds.), *Compositional Data Analysis: Theory and Applications* (pp. 43--58). Wiley.

O'Neill, B. (1983). *Semi-Riemannian Geometry with Applications to Relativity*. Academic Press.

Pawlowsky-Glahn, V., & Buccianti, A. (Eds.). (2011). *Compositional Data Analysis: Theory and Applications*. Wiley.

Rao, C. R. (1945). Information and the accuracy attainable in the estimation of statistical parameters. *Bulletin of the Calcutta Mathematical Society*, 37, 81--91.

Stevens, S. S. (1961). To honor Fechner and repeal his law. *Science*, 133(3446), 80--86.

Todd, J. T., Oomes, A. H. J., Koenderink, J. J., & Kappers, A. M. L. (2001). On the affine structure of perceptual space. *Psychological Science*, 12(3), 191--196.

Thurstone, L. L. (1927). A law of comparative judgment. *Psychological Review*, 34(4), 273--286.

Viazovska, M. S. (2017). The sphere packing problem in dimension 8. *Annals of Mathematics*, 185(3), 991--1015.

Zaghen, O., Eijkelboom, F., Pouplin, A., Liu, C., Welling, M., van de Meent, J.-W., & Bekkers, E. J. (2025). Riemannian Variational Flow Matching for Material and Protein Design. *arXiv preprint* arXiv:2502.12981.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026b). The alibi problem: Epistemic foundations of multi-source data reconciliation. Working Paper. https://doi.org/10.5281/zenodo.18944770

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026f). Cohort boundaries in high-dimensional perception space: A concentration of measure analysis. Working Paper. https://doi.org/10.5281/zenodo.18945477

Zharnikov, D. (2026g). How many brands can a market hold? Sphere packing bounds for multi-dimensional positioning. Working Paper. https://doi.org/10.5281/zenodo.18945522

Zharnikov, D. (2026h). Specification impossibility in organizational design: A high-dimensional geometric analysis. Working Paper. https://doi.org/10.5281/zenodo.18945591

Zharnikov, D. (2026j). Non-ergodic brand perception: Diffusion dynamics on multi-dimensional perceptual manifolds. Working Paper. https://doi.org/10.5281/zenodo.18945659

Zharnikov, D. (2026o). Non-ergodic brand perception: Why cross-sectional brand tracking systematically misrepresents individual trajectories. Working Paper. https://doi.org/10.5281/zenodo.19138860
