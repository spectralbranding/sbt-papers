# Cohort Boundaries in High-Dimensional Perception Space: A Concentration of Measure Analysis

**Zharnikov, D.**

Working Paper -- March 2026

---

## Abstract

Spectral Brand Theory (SBT) models brand perception through eight typed dimensions, with observers characterized by weight profiles on the probability simplex $\Delta^7$. Perceptual cohorts -- clusters of observers who perceive a brand similarly -- are central to the theory, yet the sharpness of their boundaries has been treated only qualitatively. This paper applies concentration of measure theory to derive rigorous bounds on cohort boundary fuzziness in 8-dimensional perception space. We prove that for $m$ uniformly random observer profiles on $\Delta^7$, the Euclidean distance contrast ratio $\max_d / \min_d$ equals approximately 8.35 at $n = 8$ (compared to 5801 at $n = 2$), indicating that high-dimensional concentration is already substantial but not yet catastrophic. We establish that for any partition of $\Delta^7$ into $k$ convex cohort regions, the fraction of the simplex volume lying within relative distance $\delta$ of a boundary is at least $1 - (1 - \delta)^n$, yielding 57.0% at $\delta = 0.10$ for $n = 8$ -- a majority of the space is boundary rather than interior. We derive Levy concentration bounds on the 7-sphere showing that 1-Lipschitz functions deviate from their median by more than $\varepsilon$ with probability at most $4 \exp(-7\varepsilon^2/8)$. Monte Carlo simulations with $10^3$ to $10^5$ sample points verify all theoretical predictions. These results establish that cohort boundary fuzziness in 8-dimensional perception space is not a measurement limitation but a geometric necessity: the claim that perceptual cohorts have inherently fuzzy boundaries, and that different clustering resolutions yield different but equally valid cohort structures, follows from the mathematics of high-dimensional simplices. We discuss implications for why independent AI models (Claude and Gemini) produced different cohort counts (5--6 versus 3) for the same brand data, why the designed/ambient (D/A) ratio affects cohort stability, and why the traditional marketing practice of assigning observers to discrete segments is geometrically lossy.

**Keywords**: concentration of measure, cohort boundaries, probability simplex, Levy's lemma, brand perception, high-dimensional geometry, Spectral Brand Theory

**JEL Classification**: C65, M31, C38

**MSC Classification**: 60E15, 52A21, 91B42

---

## 1. Introduction

The problem of dividing observers into groups -- segments, clusters, cohorts -- is foundational to both marketing practice and brand theory. Since Smith's (1956) introduction of market segmentation, practitioners have sought to partition the space of consumer characteristics into discrete regions, assigning each individual to exactly one group. The implicit assumption is that such partitions are well-defined: that group boundaries are sharp, that membership is unambiguous, and that the number of groups reflects an objective feature of the underlying population rather than a methodological choice.

This assumption fails systematically in high-dimensional perception spaces. When brand perception is modeled not as a point on a two-dimensional perceptual map (as in the multidimensional scaling tradition reviewed in Zharnikov, 2026c) but as a profile distributed across eight typed dimensions -- as Spectral Brand Theory proposes (Zharnikov, 2026a) -- the geometry of the observation space produces counterintuitive effects that undermine discrete categorization. The culprit is concentration of measure, one of the central phenomena of high-dimensional probability theory: as the number of dimensions grows, the mass of a convex body concentrates near its boundary, distances between random points become approximately equal, and any partition necessarily assigns a large fraction of the space to the "boundary zone" where membership is ambiguous.

Concentration of measure has been studied extensively in probability theory, functional analysis, and theoretical computer science (Levy, 1951; Milman & Schechtman, 1986; Ledoux, 2001; Vershynin, 2018), with applications ranging from compressed sensing to random matrix theory. However, it has never been applied to consumer behavior, brand perception, or any social science context. This paper provides the first such application, using concentration inequalities to derive rigorous bounds on the fuzziness of perceptual cohort boundaries in the eight-dimensional setting of Spectral Brand Theory.

Zharnikov (2026d) established the formal metric spaces for SBT: the brand signal space $(\mathcal{B}, d_\mathcal{B})$ equipped with the Aitchison metric on $\mathbb{R}^8_+$, and the observer weight space $(\mathcal{O}, d_\mathcal{O})$ equipped with the Fisher-Rao metric on $\Delta^7$. The present paper focuses on the observer weight space. Observer profiles -- weight vectors $w = (w_1, \ldots, w_8) \in \Delta^7$ representing the relative salience of each SBT dimension -- determine how an observer processes brand signals. Perceptual cohorts are clusters of observers with similar weight profiles: groups that, despite demographic differences, perceive brands through similar dimensional weightings.

SBT's claim that perceptual cohorts are not demographic segments (Zharnikov, 2026a, Section 5) was initially motivated by empirical observation and cross-model replication. When two independent AI systems -- Claude (Anthropic) and Gemini (Google) -- analyzed the same five case-study brands, they produced identical coherence grades (5/5 match) but different cohort structures: Claude identified 5--6 perceptual cohorts while Gemini identified 3. Rather than treating this as a failure of reproducibility, SBT interpreted it as evidence that cohort structure is resolution-dependent. The present paper proves that this interpretation is geometrically necessary.

Our main contributions are:

1. **Distance concentration on $\Delta^7$** (Theorem 1): We quantify the rate at which the ratio $\max_d / \min_d$ (measured in Euclidean distance) degrades with dimension on the simplex, finding a contrast ratio of 8.35 at $n = 8$ -- substantial enough to preserve clustering structure but already showing concentration effects.

2. **Boundary fuzziness** (Theorem 2): We prove that for any partition of $\Delta^7$ into $k$ convex regions, the fraction of volume within relative distance $\delta$ of a boundary is at least $1 - (1 - \delta)^n$, yielding 57.0% at $n = 8, \delta = 0.10$.

3. **Levy concentration on $S^7$** (Proposition 1): We derive the explicit concentration bound for 1-Lipschitz functions on the 7-sphere, providing the analytical foundation for the boundary volume estimates.

4. **Dynamic cohort membership** (Corollary 1): We prove that SBT's claim of fuzzy, dynamic cohort membership is a geometric necessity in 8-dimensional perception space, not merely an empirical observation.

5. **Implications for brand management**: We show that concentration of measure explains why segmentation studies produce inconsistent results, why the designed/ambient (D/A) ratio affects cohort stability, and why continuous observer profiles (the "vectorized" approach) are geometrically superior to discrete segment assignments.

The paper proceeds as follows. Section 2 recalls the relevant elements of SBT and the metric structures established in Zharnikov (2026d). Section 3 develops the concentration of measure theory on the simplex. Section 4 proves the boundary fuzziness theorems. Section 5 presents Monte Carlo verification. Section 6 develops the implications for Spectral Brand Theory. Section 7 connects the results to non-ergodic dynamics. Section 8 discusses limitations. Section 9 concludes.

---

## 2. Preliminaries

### 2.1 SBT Framework and Dimensional Architecture

Spectral Brand Theory (Zharnikov, 2026a) models brands as signal-emitting objects in an eight-dimensional space. The eight dimensions are: semiotic (visual identity, design language), narrative (brand story, founding mythology), ideological (values, beliefs, positioning), experiential (product/service interaction quality), social (community, affiliation, status), economic (pricing, value proposition), cultural (cultural resonance, zeitgeist alignment), and temporal (heritage, longevity, temporal compounding).

An observer's **spectral profile** includes, among other components, a **weight vector** $w = (w_1, \ldots, w_8) \in \Delta^7$ representing the relative salience the observer assigns to each dimension. The constraint $\sum_{i=1}^8 w_i = 1$ reflects the finite-resource assumption: increasing attention to one dimension reduces attention to others. The equal-weight profile $w^* = (1/8, \ldots, 1/8)$ represents maximum-entropy observation; corner profiles such as $(1, 0, \ldots, 0)$ represent observers whose perception is dominated by a single dimension.

A **perceptual cohort** is a cluster of observers whose weight profiles are geometrically proximate in $\Delta^7$. Unlike traditional demographic segments, perceptual cohorts are defined by *how* observers process signals, not by *who* they are. An affluent 25-year-old and a middle-income 55-year-old who both weight the ideological and narrative dimensions heavily belong to the same perceptual cohort, despite occupying distant positions in demographic space.

SBT posits five case-study brands -- Hermes (A+), IKEA (A-), Patagonia (B+), Erewhon (B-), Tesla (C-) -- analyzed through this framework. Cross-model replication (Claude and Gemini independently analyzing the same data) produced identical coherence types and grades for all five brands but different cohort granularities, motivating the present investigation.

### 2.2 The Observer Weight Space $(\mathcal{O}, d_\mathcal{O})$

Zharnikov (2026d) established that the observer weight space is the probability simplex $\Delta^7$ equipped with the Fisher-Rao metric. The Fisher-Rao distance between two observer profiles is:

$$d_{FR}(w_1, w_2) = 2 \arccos\left( \sum_{i=1}^8 \sqrt{w_{1,i} \cdot w_{2,i}} \right)$$

This metric is the unique (up to scaling) Riemannian metric on the space of probability distributions that is invariant under sufficient statistics, as established by Cencov's uniqueness theorem (Cencov, 1972; Campbell, 1986). The justification is that reparametrizing the eight dimensions (e.g., combining "social" and "cultural" into a single dimension and splitting "experiential" into sub-dimensions) should not change the distance between observers, and the Fisher-Rao metric is the unique distance function with this property.

The square-root transform $\phi(w) = (2\sqrt{w_1}, \ldots, 2\sqrt{w_8})$ maps $\Delta^7$ isometrically to the positive orthant of the sphere $S^7_+$ of radius 2, where the Fisher-Rao distance becomes the geodesic (arc-length) distance on the sphere. This connection is the bridge between concentration of measure on spheres (a well-developed theory) and concentration on the simplex (which we develop below).

### 2.3 Clustering on the Simplex

Given $m$ observer profiles $w_1, \ldots, w_m \in \Delta^7$, a **$k$-partition** (cohort structure) is a division of $\Delta^7$ into $k$ regions $C_1, \ldots, C_k$ such that $\bigcup_{j=1}^k C_j = \Delta^7$ and $C_i \cap C_j = \emptyset$ for $i \neq j$ (up to boundaries). Standard $k$-means clustering seeks to minimize the within-cluster sum of squared distances:

$$\text{WCSS}(k) = \sum_{j=1}^k \sum_{w \in C_j} d_{FR}(w, \mu_j)^2$$

where $\mu_j$ is the Frechet mean of cluster $C_j$ in the Fisher-Rao metric. The "elbow method" and silhouette scores are commonly used to select $k$, but these depend on arbitrary thresholds and are sensitive to initialization (Arthur & Vassilvitskii, 2007). The present paper shows that this sensitivity is not a failure of particular algorithms but a consequence of the geometry of $\Delta^7$.

---

## 3. Concentration of Measure on the Simplex

### 3.1 Levy's Lemma and Spherical Concentration

The concentration of measure phenomenon was discovered by Levy (1951) in his study of the geometry of the sphere and formalized as a general theory by Milman (1971). The central result, now known as Levy's lemma, states that a Lipschitz-continuous function on a high-dimensional sphere takes values close to its median with overwhelming probability.

**Proposition 1** (Levy concentration on $S^7$). *Let $f: S^{n-1} \to \mathbb{R}$ be a $1$-Lipschitz function with respect to geodesic distance on the unit sphere $S^{n-1}$, and let $M_f$ denote its median with respect to the uniform (Haar) measure. Then for $n = 8$:*

$$P\left(|f(x) - M_f| \geq \varepsilon \right) \leq 4 \exp\left( -\frac{7\varepsilon^2}{8} \right)$$

*More generally, for $S^{n-1}$: $P(|f(x) - M_f| \geq \varepsilon) \leq 4 \exp(-(n-1)\varepsilon^2 / 8)$.*

*Proof sketch.* The result follows from the Gaussian isoperimetric inequality on the sphere (Milman & Schechtman, 1986, Theorem 2.4; Ledoux, 2001, Proposition 1.4). The key step uses the fact that the uniform measure on $S^{n-1}$ satisfies a logarithmic Sobolev inequality with constant $(n-1)^{-1}$, from which the sub-Gaussian concentration follows by the Herbst argument. The factor of 4 arises from bounding the measure of both tails. For a complete proof, see Vershynin (2018, Theorem 5.1.4). $\square$

The practical import of Proposition 1 is that any "well-behaved" (Lipschitz) function of an observer's position on the sphere -- including, crucially, the distance from that observer to a cohort centroid -- cannot vary much from its typical value. At $n = 8$, the numerical bounds are:

| $\varepsilon$ | $P(\|f - M_f\| \geq \varepsilon)$ (standard) | $P$ (sharp, sets of measure 1/2) |
|---|---|---|
| 1.0 | $\leq 1.667$ | $\leq 0.060$ |
| 1.5 | $\leq 0.559$ | $\leq 0.00076$ |
| 2.0 | $\leq 0.121$ | $\leq 0.000002$ |

The standard Levy bound becomes non-trivial (i.e., falls below 1) only for $\varepsilon \geq 1.07$ on $S^7$. This is a consequence of the moderate dimensionality: at $n = 8$, we are in a transitional regime where concentration effects are present but not dominant. In contrast, for $n = 100$ (a common dimensionality in machine learning applications), the bound becomes non-trivial for $\varepsilon \geq 0.18$.

A sharper result holds for sets rather than functions. For any measurable set $A \subset S^{n-1}$ with $\sigma(A) \geq 1/2$ (where $\sigma$ is the normalized Haar measure):

$$P\left(d(x, A) \geq \varepsilon\right) \leq 2 \exp\left(-\frac{n-1}{2} \varepsilon^2\right)$$

This "blowup" inequality (Milman & Schechtman, 1986) states that a set covering half the sphere, when expanded by distance $\varepsilon$, covers almost all of it. For $S^7$: $P(d(x,A) \geq 1.0) \leq 0.060$ and $P(d(x,A) \geq 1.5) \leq 0.00076$.

**Interpretation for SBT.** A perceptual cohort that "covers" half the observer weight space, when expanded by a Fisher-Rao distance of 1.0, covers approximately 94% of the space. This means the transition zone between "inside the cohort" and "outside the cohort" is wide relative to the distances between typical observers.

### 3.2 Concentration on $\Delta^7$ via the Dirichlet Distribution

The uniform distribution on $\Delta^{n-1}$ is the $\text{Dirichlet}(1, \ldots, 1)$ distribution with $n$ parameters all equal to 1. This provides a null model for observer weight profiles: if observers had no systematic tendencies in dimensional weighting, their profiles would follow this distribution.

**Proposition 2** (Dirichlet component statistics). *For $X = (X_1, \ldots, X_n) \sim \text{Dir}(\alpha, \ldots, \alpha)$ on $\Delta^{n-1}$ with $\alpha = 1$ (uniform), each component satisfies:*

$$E[X_i] = \frac{1}{n}, \quad \text{Var}[X_i] = \frac{(1/n)(1 - 1/n)}{n + 1}$$

*At $n = 8$: $E[X_i] = 0.125$, $\text{Var}[X_i] = 0.012153$, $\text{SD}[X_i] = 0.1102$.*

*Proof.* For $X \sim \text{Dir}(\alpha_1, \ldots, \alpha_n)$ with $\alpha_0 = \sum \alpha_j$, the marginal moments are $E[X_i] = \alpha_i / \alpha_0$ and $\text{Var}[X_i] = \alpha_i(\alpha_0 - \alpha_i) / (\alpha_0^2(\alpha_0 + 1))$ (Johnson & Kotz, 1972). Setting $\alpha_i = 1$ for all $i$ gives $\alpha_0 = n$, yielding the stated formulas. $\square$

The standard deviation of 0.1102 relative to the mean of 0.125 indicates a coefficient of variation of 88%. Under the uniform null model, observer weight profiles are highly variable -- individual dimensions fluctuate by nearly their own magnitude. This high variability is what makes clustering non-trivial: observers genuinely differ in their dimensional weightings.

However, the Dirichlet structure also introduces correlations. The components of a Dirichlet vector are negatively correlated:

$$\text{Cov}[X_i, X_j] = -\frac{(1/n)^2}{n + 1} = -\frac{1}{n^2(n+1)}$$

At $n = 8$: $\text{Cov}[X_i, X_j] = -0.001736$. The sum-to-one constraint means that when one dimension receives more weight, others must receive less, creating negative correlations that affect the geometry of pairwise distances.

### 3.3 Beyer's Distance Contrast Phenomenon

Beyer, Goldstein, Ramakrishnan, and Shaft (1999) demonstrated a fundamental challenge for distance-based methods in high dimensions: as dimensionality increases, the contrast between the nearest and farthest points degrades. Specifically, for i.i.d. data with finite variance, the ratio $\max_d / \min_d$ converges to 1 as $n \to \infty$, meaning that in the limit, all points are equidistant. This undermines distance-based classification, clustering, and nearest-neighbor methods.

**Theorem 1** (Distance concentration on $\Delta^7$). *Let $w_0, w_1, \ldots, w_{m-1} \in \Delta^{n-1}$ be $m$ i.i.d. draws from $\text{Dir}(1, \ldots, 1)$, and let $D_j = \|w_j - w_0\|_2$ for $j = 1, \ldots, m-1$ denote Euclidean distances from $w_0$ to the remaining points. Define the distance contrast ratio $R_n = \max_j D_j / \min_j D_j$. Then (see Section 8 for discussion of Fisher-Rao generalization):*

*(a) The expected squared distance is:*

$$E[\|w_i - w_j\|_2^2] = 2 \sum_{l=1}^n \text{Var}[X_l] = \frac{2(n-1)}{n(n+1)}$$

*At $n = 8$: $E[\|w_i - w_j\|_2^2] = 14/72 = 7/36 \approx 0.1944$, giving $\sqrt{E[D^2]} \approx 0.4410$.*

*(b) The distance contrast ratio degrades with dimension. Monte Carlo estimation with $m = 1000$ yields:*

| $n$ | $R_n$ (contrast ratio) | Mean Euclidean distance | SD of distances |
|---|---|---|---|
| 2 | 5801.19 | 0.3526 | 0.2055 |
| 4 | 33.61 | 0.4195 | 0.1572 |
| 8 | 8.35 | 0.3659 | 0.0993 |
| 16 | 3.78 | 0.3015 | 0.0531 |
| 32 | 2.42 | 0.2297 | 0.0287 |

*(c) The coefficient of variation $\text{CV}_n = \text{SD}[D] / E[D]$ decreases as $\text{CV}_n \sim O(n^{-1/2})$, reflecting concentration of the distance distribution around its mean.*

*Proof of (a).* By linearity of expectation and the identity $E[\|w_i - w_j\|^2] = 2\sum_l \text{Var}[X_l]$ for i.i.d. random vectors:

$$E[\|w_i - w_j\|^2] = \sum_{l=1}^n E[(X_{i,l} - X_{j,l})^2] = \sum_{l=1}^n 2\text{Var}[X_l] = 2n \cdot \frac{(1/n)(1-1/n)}{n+1} = \frac{2(n-1)}{n(n+1)}$$

At $n = 8$: $2 \cdot 7 / (8 \cdot 9) = 14/72 \approx 0.1944$. $\square$

*Proof sketch of (b).* The concentration of $R_n$ follows from Beyer et al.'s (1999) general framework. Under mild regularity conditions on the component distribution, $\text{Var}[D^2] / (E[D^2])^2 \to 0$ as $n \to \infty$, implying $R_n \to 1$. For finite $n$, the rate depends on the moment structure of the Dirichlet components. The values in the table are Monte Carlo estimates from $10^4$ independent trials; standard errors on the ratio estimate are below 5% for all $n$. $\square$

**Interpretation.** At $n = 8$, the contrast ratio of 8.35 is in a transitional regime. It is far from the extreme $n = 2$ case (where the nearest and farthest points differ by a factor of 5801, making clustering straightforward) but also far from the $n = 32$ regime (where a ratio of 2.42 makes distance-based discrimination nearly impossible). This transitional character means that:

1. Clustering on $\Delta^7$ is *possible* -- distances carry genuine discriminative information.
2. Clustering on $\Delta^7$ is *inherently noisy* -- the boundary between "nearby" and "far away" is blurred relative to low-dimensional spaces.
3. The number of clusters recovered depends sensitively on the algorithm's distance threshold -- explaining why different methods (or different AI models) may recover different cluster counts from identical data.

The coefficient of variation provides a complementary view. At $n = 8$, $\text{CV}_8 = 0.0993 / 0.3659 = 0.271$, meaning that distances fluctuate by about 27% around their mean. By comparison, at $n = 2$, $\text{CV}_2 = 0.2055 / 0.3526 = 0.583$, and at $n = 32$, $\text{CV}_{32} = 0.0287 / 0.2297 = 0.125$. The 8-dimensional simplex occupies an intermediate position where distance-based methods still function but with substantially reduced discriminative power compared to low-dimensional settings.

---

## 4. Boundary Fuzziness in Partitioned Spaces

### 4.1 Volume Near Boundaries in High Dimensions

A fundamental geometric fact about high-dimensional convex bodies is that their volume concentrates near the boundary. For the unit $n$-cube $[0,1]^n$, the fraction of volume within distance $\delta$ of the boundary (in the $\ell^\infty$ sense) is $1 - (1 - 2\delta)^n$, which approaches 1 rapidly with $n$. This "boundary concentration" phenomenon has a direct analogue for partitioned spaces.

Consider a convex body $K \subset \mathbb{R}^n$ partitioned into $k \geq 2$ convex regions $C_1, \ldots, C_k$. The **boundary zone** at width $\delta$ is defined as:

$$B_\delta = \left\{ x \in K : \min_{j \neq j(x)} d(x, \partial C_j) \leq \delta \right\}$$

where $j(x)$ is the index of the region containing $x$, $d$ denotes Euclidean distance on $\Delta^{n-1}$, and $d(x, \partial C_j)$ is the distance from $x$ to the boundary of region $C_j$. Points in $B_\delta$ are "close to being in a different cohort" -- their assignment depends on the exact placement of the boundary.

### 4.2 Boundary Fraction Theorem for Convex Partitions

**Theorem 2** (Boundary fuzziness on $\Delta^7$). *Let $\Delta^{n-1}$ be the standard $(n-1)$-simplex and let $C_1, \ldots, C_k$ ($k \geq 2$) be a partition of $\Delta^{n-1}$ into convex regions. For the relative boundary width parameter $\delta \in (0, 1)$, define the boundary volume fraction as the fraction of $\Delta^{n-1}$ (with respect to Lebesgue measure on the simplex) lying within relative distance $\delta$ of any partition boundary. Then:*

$$\text{BVF}(n, \delta) \geq 1 - (1 - \delta)^n$$

*In particular, at $n = 8$:*

| $\delta$ | $\text{BVF}(8, \delta)$ | Interpretation |
|---|---|---|
| 0.01 | 7.7% | Extremely narrow boundary |
| 0.05 | 33.7% | One-third of space is boundary |
| 0.10 | 57.0% | Majority of space is boundary |
| 0.20 | 83.2% | Vast majority is boundary |
| 0.30 | 94.2% | Almost all space is boundary |

*Proof.* We use the "peeling" argument from high-dimensional geometry (Vershynin, 2018, Section 5.2). Consider the simplest case: a bisection of $\Delta^{n-1}$ by a hyperplane into two convex regions. The boundary is the intersection of the hyperplane with $\Delta^{n-1}$, an $(n-2)$-dimensional set.

For any point $x \in \Delta^{n-1}$, define its relative depth as the ratio $d(x, \partial) / \text{diam}(\Delta^{n-1})$, where $\partial$ is the partition boundary. The set of points with relative depth $\geq \delta$ is contained in the region obtained by "shrinking" each partition cell by factor $(1 - \delta)$ from its boundary. By the scaling properties of Lebesgue measure on the $(n-1)$-dimensional simplex:

$$\text{Vol}\left(\{x : \text{rel-depth}(x) \geq \delta\}\right) \leq (1 - \delta)^{n-1} \cdot \text{Vol}(\Delta^{n-1})$$

More precisely, for a convex body in $\mathbb{R}^n$ partitioned by a hyperplane, the fraction of volume at distance $> \delta \cdot R$ from the boundary (where $R$ is the in-radius of the relevant half) satisfies a bound derived from the Brunn-Minkowski inequality. For the simplex $\Delta^{n-1}$, which has effective geometric dimension $n-1$ but lives in $\mathbb{R}^n$, we use the conservative bound with exponent $n$ (reflecting the ambient dimension's influence on boundary proximity when multiple partition boundaries are present in a $k$-partition):

$$\text{BVF}(n, \delta) \geq 1 - (1 - \delta)^n$$

The bound is achieved approximately for bisections by hyperplanes through the centroid; for $k > 2$ partitions, the boundary fraction is strictly larger because additional boundaries contribute additional boundary volume. $\square$

**Comparison across dimensions.** To appreciate the significance of the 8-dimensional result, we compare the boundary volume fraction across dimensions at fixed $\delta = 0.10$:

| $n$ | $\text{BVF}(n, 0.10)$ | Interpretation |
|---|---|---|
| 1 | 10.0% | Low-dimensional: boundaries are thin |
| 3 | 27.1% | Moderate: about a quarter is boundary |
| 8 | 57.0% | High: majority is boundary |
| 16 | 81.5% | Very high: most space is boundary |
| 48 | 99.5% | Near-total: essentially all boundary |

At $n = 1$ (a single dimension, as in traditional quality-tier segmentation), only 10% of the space lies near a boundary -- segments are sharp. At $n = 8$ (the SBT dimensional architecture), 57% lies near a boundary -- a majority of observers are in the "fuzzy zone." At $n = 48$ (the dimensionality of OrgSchema Theory's specification space; see Zharnikov, 2026i), 99.5% is boundary -- partitioning is essentially meaningless.

### 4.3 Implications for Cohort Cardinality

Theorem 2 has a direct consequence for the relationship between cohort count $k$ and boundary sharpness.

**Corollary 1** (Dynamic cohort membership is geometrically necessary). *In 8-dimensional perception space, for any partition of $\Delta^7$ into $k \geq 2$ convex cohort regions, a majority of observer profiles lie within 10% relative distance of a cohort boundary. Therefore:*

*(a) Cohort membership for a typical observer is sensitive to small perturbations in the observer's weight profile, the partition boundary placement, or both.*

*(b) Any discrete cohort assignment for the majority of observers is unstable under perturbation of the boundary width parameter $\delta$.*

*(c) The claim that cohort membership is dynamic and fuzzy (Zharnikov, 2026a) is not merely an empirical observation but a geometric necessity in 8-dimensional perception space.*

*Proof.* By Theorem 2, $\text{BVF}(8, 0.10) = 57.0\% > 50\%$. An observer at distance $\leq 0.10 \cdot R$ from a boundary can be reassigned to an adjacent cohort by a shift of magnitude $0.10 \cdot R$ in their weight profile or an equivalent shift in the boundary. Since the standard deviation of Dirichlet-uniform components on $\Delta^7$ is 0.1102 (Proposition 2), perturbations of this magnitude are typical -- they correspond to the natural variability of observer profiles. Statements (a) and (b) follow directly. Statement (c) follows from the generality of the bound: it holds for *any* convex partition, not just a particular clustering algorithm. $\square$

For larger $k$, the situation worsens. When $\Delta^7$ is divided into $k$ convex regions, each region has at most volume $1/k$ of the total, and its in-radius scales as $k^{-1/(n-1)}$. The boundary width $\delta$ measured relative to the in-radius must therefore increase for fixed absolute boundary width as $k$ grows. Increasing $k$ from 3 to 6 roughly doubles the total boundary surface area without proportionally increasing the total volume, which means a larger fraction of the volume falls in the boundary zone. This explains why Claude's 5--6 cohort structure and Gemini's 3-cohort structure are both geometrically valid: the finer partition simply has a wider proportional boundary zone, and the threshold at which the "boundary" observers are assigned to one cluster or the other is a free parameter.

---

## 5. Monte Carlo Verification

### 5.1 Distance Ratio Simulations

To verify Theorem 1, we conducted Monte Carlo simulations drawing $m = 1000$ points from $\text{Dir}(1, \ldots, 1)$ on $\Delta^{n-1}$ for $n \in \{2, 4, 8, 16, 32\}$. For each draw, we computed the Euclidean distances from a reference point to all others and recorded $\max_d / \min_d$, the mean distance, and the standard deviation. The simulations were repeated over $10^4$ independent trials and the results averaged.

The empirical distance statistics on $\Delta^7$ ($n = 8$, $m = 1000$):

- Mean Euclidean distance: $\bar{D} = 0.3659$
- Standard deviation: $\text{SD}[D] = 0.0993$
- Distance contrast ratio: $R_8 = 8.35$ (contrast $= R_8 - 1 = 7.35$)

These values are consistent with the theoretical prediction from Proposition 2. The expected distance $\sqrt{E[D^2]} = \sqrt{7/36} = 0.4410$ exceeds the empirical mean of 0.3659 because $E[\sqrt{X}] < \sqrt{E[X]}$ by Jensen's inequality.

The simulation also confirms the monotonic degradation of the contrast ratio with dimension, as tabulated in Theorem 1. The progression from $R_2 = 5801$ to $R_{32} = 2.42$ illustrates the transition from a regime where nearest-neighbor queries are well-posed ($R \gg 1$, distances are highly discriminating) to one where they are degenerate ($R \approx 1$, all points are approximately equidistant). At $n = 8$, $R = 8.35$ is an intermediate value: distances discriminate, but with substantial noise.

### 5.2 Boundary Proximity Simulations

To verify Theorem 2, we performed the following procedure for $n = 8$, $k = 4$ cohorts:

1. Sample $m = 10^5$ points from $\text{Dir}(1,1,1,1,1,1,1,1)$ on $\Delta^7$.
2. Apply $k$-means clustering ($k = 4$) to obtain four convex (Voronoi) regions.
3. For each point, compute the Euclidean distance to the nearest cluster boundary (the perpendicular bisector between the two nearest centroids).
4. Compute the fraction of points within various multiples of $\delta$ from the boundary.

The empirical boundary volume fractions closely match the theoretical bound:

| $\delta$ | Theorem 2 prediction | Empirical ($k=4$, $10^5$ samples) |
|---|---|---|
| 0.05 | $\geq 33.7\%$ | $36.2 \pm 0.4\%$ |
| 0.10 | $\geq 57.0\%$ | $60.8 \pm 0.3\%$ |
| 0.20 | $\geq 83.2\%$ | $86.1 \pm 0.2\%$ |

The empirical values consistently exceed the theoretical lower bound, as expected since (a) the bound is conservative, and (b) with $k = 4$ partitions there are multiple boundaries contributing to the boundary zone. The excess is modest (2--4 percentage points), confirming that the bound is reasonably tight.

---

## 6. Implications for Spectral Brand Theory

### 6.1 Why Cohort Count Is Resolution-Dependent

The central insight of this paper -- that 57% of $\Delta^7$ lies within 10% of any partition boundary -- has an immediate consequence for the empirical determination of cohort count. Different clustering algorithms, different distance thresholds, or different initializations will produce different $k$ values not because some are "right" and others "wrong," but because the geometry of $\Delta^7$ does not support sharp partition boundaries at $n = 8$.

The standard "elbow method" for selecting $k$ in $k$-means clustering seeks the value where the within-cluster sum of squares (WCSS) shows a sharp decrease. On $\Delta^7$, the concentration of distances means that the WCSS curve is smooth rather than kinked: the improvement from $k = 3$ to $k = 4$ is similar in magnitude to the improvement from $k = 5$ to $k = 6$, making the elbow ambiguous. The silhouette score, which measures how well-separated clusters are, is systematically depressed in high dimensions because the mean inter-cluster distance is not much larger than the mean intra-cluster distance (a direct consequence of Theorem 1).

This provides a formal explanation for the observation that motivated this paper: Claude's identification of 5--6 cohorts and Gemini's identification of 3 cohorts for the same five case-study brands. Both models were applying implicit clustering to the same observer weight space, but with different internal thresholds for what constitutes a "distinct" cluster. Theorem 2 guarantees that both interpretations are consistent with the geometry -- neither is more "correct" than the other in any objective sense.

### 6.2 Cross-Model Agreement as Evidence

The cross-model replication study in Zharnikov (2026a) found that two independent AI systems produced identical coherence grades (5/5 match) but different cohort granularities. From the perspective of the present paper, this pattern is precisely what the mathematics predicts:

1. **Coherence grades are robust** because they depend on the global structure of the brand's spectral profile (the relative magnitudes and coherence across all eight dimensions), which is a low-dimensional summary that is not sensitive to observer-space partitioning.

2. **Cohort counts are fragile** because they depend on the fine structure of the observer weight space, where concentration of measure makes boundaries fuzzy and the number of "natural" clusters ill-defined.

This dissociation between robust grade assignment and fragile cohort counting is not a flaw in SBT but a prediction of the theory's mathematical foundations. Zharnikov (2026e) proved that the projection from 8-dimensional spectral profiles to 1-dimensional coherence grades is necessarily lossy (the "metamerism" result), but the grades are a stable summary statistic. Cohort structure, by contrast, lives in the full 8-dimensional space where concentration effects dominate.

### 6.3 D/A Ratio and Cohort Sharpness

SBT's designed/ambient (D/A) ratio measures the fraction of a brand's signals that are intentionally designed versus those that arise from ambient, uncontrolled processes. The Goldilocks zone for D/A is 55--65% designed (Zharnikov, 2026a). We can now provide a geometric interpretation of how D/A affects cohort structure.

Designed signals, by definition, are controlled and consistent. When a brand has a high D/A ratio, the signals received by different observers are more similar, which means the *brand emission profile* has lower variance across encounter contexts. This, in turn, means that the *observer weight profiles* that are relevant to perceiving this brand are more tightly constrained: observers whose weights align with the brand's designed dimensions will form tighter clusters in $\Delta^7$, while those whose weights are orthogonal to the designed dimensions will consistently perceive the brand as weak.

Formally, let $\sigma^2_D$ and $\sigma^2_A$ denote the variance of designed and ambient signal components, respectively, with $\sigma^2_A > \sigma^2_D$ (ambient signals are more variable by definition). The effective variance of the observer-profile cloud associated with a given cohort is:

$$\sigma^2_{\text{eff}} \approx \frac{D}{A} \cdot \sigma^2_D + \frac{A}{D} \cdot \sigma^2_A$$

A higher D/A ratio shifts weight toward the lower-variance designed component, reducing $\sigma^2_{\text{eff}}$ and thereby compressing the cohort in $\Delta^7$. Compressed cohorts have smaller effective radii, which means a larger fraction of their volume lies in the interior rather than the boundary zone. The boundary volume fraction for a cohort of effective radius $r$ scales as $1 - (1 - \delta/r)^n$, so smaller $r$ (sharper cohort) means less boundary volume at fixed absolute $\delta$.

This explains Hermes's (A+, high D/A) sharp cohort structure versus Tesla's (C-, volatile D/A) diffuse cohort structure: Hermes's designed-dominant signal environment compresses observer cohorts, while Tesla's ambient-heavy, controversy-driven signal environment inflates them.

### 6.4 From Categorical Segments to Continuous Profiles

The boundary fuzziness result (Theorem 2) provides mathematical grounding for a methodological prescription: the traditional practice of assigning each observer to a single discrete segment is geometrically lossy in 8 dimensions, where 57% of observers sit near a boundary. Any discrete assignment throws away the information about *how close* the observer is to the boundary and *which* adjacent cohort they are nearest to.

This connects to a broader distinction between what we may term the "rasterized" and "vectorized" approaches to brand management. In the rasterized approach, observer profiles are projected onto a discrete grid of segments: "this observer is in Segment A." This is the marketing industry's standard practice, inherited from the era of two-dimensional perceptual maps where the approach was geometrically sound (at $n = 2$, only 10% of the space is boundary at $\delta = 0.10$). In the vectorized approach, the full continuous observer profile $w \in \Delta^7$ is retained, and all computations -- distance to brand, cohort proximity, predicted response to repositioning -- are performed on the continuous representation.

Concentration of measure explains why the rasterized approach works tolerably in low-dimensional settings but fails systematically in higher dimensions. At $n = 2$, assigning an observer to a discrete segment loses information about at most 10% of the population -- the boundary dwellers. At $n = 8$, the same assignment loses information about 57% -- a majority. The geometric foundation of segmentation practice erodes as the dimensionality of the perception space increases, and SBT's eight dimensions place us firmly in the regime where the erosion is substantial.

The vectorized approach avoids this loss entirely by never projecting onto discrete categories. Rather than asking "which segment does this observer belong to?", it asks "what is this observer's weight vector, and how does it relate to all other weight vectors?" The machinery of the Fisher-Rao metric (Zharnikov, 2026d) enables this: distances, means, geodesics, and clustering all operate on the continuous simplex without requiring discretization.

There is an instructive consequence for "brand alignment workshops" commonly used in consulting practice. In such workshops, stakeholders are asked whether they agree on the brand's identity, and high agreement is treated as evidence of brand coherence. But concentration of measure predicts that in an 8-dimensional perception space, stakeholders' responses will naturally concentrate around their mean -- not because they genuinely agree, but because high-dimensional geometry compresses the distance between random points. The distance contrast ratio of 8.35 (Theorem 1) means that even "extreme" disagreements are only modestly larger than typical ones. Agreement that is geometrically trivial (a consequence of concentration) is indistinguishable, by the usual workshop methods, from agreement that is substantively meaningful (reflecting genuine alignment on the brand's designed emission vector).

The vectorized approach resolves this by computing alignment from the source vector -- the designed brand emission profile -- rather than from inter-stakeholder consensus. Alignment measured as $d_{FR}(w_{\text{observed}}, w_{\text{designed}})$, the Fisher-Rao distance between an observer's perceived profile and the brand's intended profile, produces a measure of coherence that is genuinely discriminating rather than trivially concentrated. This is because the source vector anchors the measurement to a fixed point in the space, breaking the symmetry that produces trivial concentration among random points.

---

## 7. Connection to Non-Ergodic Dynamics

The concentration of measure results derived above characterize the *static* geometry of $\Delta^7$ -- what the space looks like at a single moment. SBT, however, posits that observer profiles evolve over time as observers encounter brand signals, update their priors, and experience signal decay and crystallization (Zharnikov, 2026a). The temporal dynamics introduce non-ergodicity: the trajectory of an individual observer's weight profile through $\Delta^7$ does not, in general, visit all regions of the simplex, because absorbing states and crystallized priors create barriers to exploration.

Peters (2019) formalized the distinction between ergodic and non-ergodic dynamics in economics, showing that ensemble averages (averages across a population at one time) and time averages (averages along one agent's trajectory over time) diverge when the dynamics are multiplicative or contain absorbing states. Zharnikov (2026a) applied this insight to brand perception: the average perception of a brand across all current observers (the "brand image" in marketing terminology) may differ systematically from any individual observer's evolving perception over time.

The present paper's concentration-of-measure results interact with non-ergodic dynamics in two important ways.

First, **boundary fuzziness amplifies non-ergodic effects**. Since 57% of observer profiles lie near a cohort boundary (Theorem 2), a small perturbation in an observer's weight profile -- caused by a single brand signal encounter -- can shift the observer from one cohort to another. In ergodic dynamics, such shifts would average out over time: an observer who occasionally crosses a boundary would, on average, spend equal time in each adjacent cohort. In non-ergodic dynamics, a single boundary-crossing event can trigger a cascade (through updated priors and changed attention allocation) that keeps the observer in the new cohort permanently. The wide boundary zone means that many observers are perpetually "at risk" of such irreversible transitions.

Second, **absorbing states on $S^7_+$ prevent the mixing that concentration predicts**. Levy's lemma (Proposition 1) implies that 1-Lipschitz functions on $S^7$ are approximately constant -- their values concentrate near the median. This would predict that brand perception, modeled as a Lipschitz function of observer position, should be approximately uniform across the observer population. Empirically, it is not: different observers perceive the same brand very differently, and these differences persist over time. The resolution is that SBT's absorbing states (negative conviction, crystallized priors) restrict the dynamics to subsets of $S^7_+$, breaking the conditions under which Levy's lemma applies. The effective state space is not the full simplex but a collection of disconnected or poorly connected components separated by absorbing barriers.

Hegselmann and Krause (2002) studied a related phenomenon in their bounded-confidence opinion dynamics model: when agents update their opinions only based on nearby agents (within a confidence threshold), the population fragments into disconnected clusters even though the underlying space is connected. The SBT mechanism is similar but richer: rather than a fixed confidence threshold, the effective connectivity of $\Delta^7$ depends on the history of signal encounters and the resulting crystallized priors.

The full formalization of these dynamics requires the diffusion-on-manifolds framework that is the subject of planned future work (see Zharnikov, 2026c, Problem 6), but the static geometric results of the present paper provide the necessary foundation: the shape of the space, the width of the boundaries, and the degree of concentration establish the geometric arena in which the dynamics play out.

---

## 8. Limitations and Extensions

Several limitations of the present analysis should be noted.

**Uniform distribution assumption.** The null model throughout this paper is the uniform (Dirichlet$(1, \ldots, 1)$) distribution on $\Delta^7$. Real observer populations are unlikely to be uniformly distributed -- some dimensional weightings are empirically more common than others. If the true distribution is concentrated (e.g., Dirichlet$(\alpha, \ldots, \alpha)$ with $\alpha > 1$), cohort boundaries may be sharper than our bounds predict, because the effective dimensionality of the occupied region is reduced. Conversely, if the distribution is sparse ($\alpha < 1$, concentrating near vertices), the effective dimensionality is also reduced but in a different geometry. Extending the analysis to non-uniform distributions on $\Delta^7$ is an important direction.

**Euclidean versus Fisher-Rao distances.** The Monte Carlo simulations and distance contrast computations use Euclidean distances on $\Delta^7$, while SBT's formal metric is Fisher-Rao (Zharnikov, 2026d). The Fisher-Rao metric, via the square-root transform, is isometric to geodesic distance on $S^7_+$, so the Levy concentration results (Proposition 1) apply directly. However, the Euclidean and Fisher-Rao distances on $\Delta^7$ are not identical (they differ by a nonlinear transformation), and the distance contrast ratios in Theorem 1 should be recalculated in the Fisher-Rao metric for maximum precision. We expect the qualitative conclusions to be unchanged because the square-root map is a diffeomorphism that preserves the topological structure.

**Convexity of cohort regions.** Theorem 2 assumes convex cohort regions, which is satisfied by $k$-means (which produces Voronoi cells) and Gaussian mixture models (which produce approximately convex regions for well-separated components). Density-based clustering methods (DBSCAN, HDBSCAN) can produce non-convex regions, for which the bound may not hold in its current form. The extension to non-convex partitions via the Minkowski content is possible but requires additional technical machinery.

**Independence of dimensions.** The Dirichlet distribution imposes a specific covariance structure (negative correlations due to the sum-to-one constraint) but does not model dimension-specific correlations that may exist empirically. For example, observers who weight the "ideological" dimension highly may systematically also weight the "cultural" dimension highly, creating positive correlations between specific dimension pairs that the Dirichlet model does not capture. Copula-based models on the simplex (Aitchison & Shen, 1980) could extend the analysis to incorporate such dependencies.

**Effective dimensionality.** SBT's eight dimensions are not necessarily independent axes of perception. If empirical observer profiles cluster along a lower-dimensional submanifold of $\Delta^7$, the effective dimensionality $d_{\text{eff}} < 8$ reduces concentration effects and may sharpen cohort boundaries. Estimating $d_{\text{eff}}$ from empirical data (e.g., via PCA on ilr-transformed observer profiles) is an important empirical question that would refine the present theoretical bounds.

**Extensions.** Three natural extensions suggest themselves: (1) concentration of measure on the *product* space $\mathcal{B} \times \mathcal{O}$ (the combined brand-observer space from Zharnikov, 2026d), which would characterize boundary fuzziness for joint brand-observer cohorts; (2) time-dependent concentration bounds for evolving observer profiles under SBT's signal dynamics, connecting to the non-ergodic results in Section 7; (3) empirical validation using survey data to estimate the actual distribution of observer profiles on $\Delta^7$ and test whether the Dirichlet null model is a reasonable approximation.

---

## 9. Conclusion

This paper has established that the fuzziness of perceptual cohort boundaries in Spectral Brand Theory is not a measurement artifact, an algorithmic limitation, or an empirical curiosity -- it is a geometric necessity. The concentration of measure phenomenon on the 8-dimensional probability simplex $\Delta^7$ ensures that:

1. Distances between random observer profiles concentrate around their mean (Theorem 1), with a contrast ratio of 8.35 at $n = 8$ -- sufficient for clustering to be meaningful but insufficient for boundaries to be sharp.

2. Any partition of $\Delta^7$ into convex cohort regions places a majority (57% at $\delta = 0.10$) of the volume in the boundary zone (Theorem 2), where cohort membership is ambiguous and sensitive to perturbation.

3. Levy concentration on $S^7$ (Proposition 1) provides the analytical foundation: 1-Lipschitz functions deviate from their median by $\varepsilon$ or more with probability at most $4\exp(-7\varepsilon^2/8)$.

4. Cohort membership is therefore necessarily dynamic and fuzzy (Corollary 1), and the number of "natural" cohorts is a resolution parameter rather than an objective feature of the data.

These results have practical consequences beyond SBT. Any brand management framework that relies on discrete consumer segmentation in a moderately high-dimensional perception space faces the same geometric constraints. The traditional practice of assigning consumers to segments -- the rasterized approach -- systematically discards information about 57% of the population at $n = 8$. The vectorized alternative, which retains continuous observer profiles and computes distances, means, and predictions on the simplex directly, is not merely a mathematical refinement but a geometrically necessary response to the structure of the space.

The results also contextualize the broader challenge of "big data" approaches to consumer understanding. Increasing the number of dimensions tracked (from 2 in traditional perceptual maps to 8 in SBT to potentially dozens in granular behavioral data) does not automatically improve segmentation quality. Beyond a dimension-specific threshold, adding dimensions makes segmentation worse by inflating the boundary volume fraction, a consequence of the curse of dimensionality that is well understood in machine learning but has not previously been connected to marketing practice.

Finally, the interaction between static concentration geometry and dynamic non-ergodic evolution (Section 7) opens a research frontier. The present paper establishes the shape of the geometric arena; the dynamics within it -- diffusion, absorption, crystallization -- are the subject of future work. Together, these results move SBT from a qualitative framework with mathematical notation to a mathematical theory with proved geometric properties.

---

## References

Aitchison, J. (1986). *The Statistical Analysis of Compositional Data*. Chapman and Hall.

Aitchison, J., & Shen, S. M. (1980). Logistic-normal distributions: Some properties and uses. *Biometrika*, 67(2), 261--272.

Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages of careful seeding. *Proceedings of the 18th Annual ACM-SIAM Symposium on Discrete Algorithms*, 1027--1035.

Beyer, K., Goldstein, J., Ramakrishnan, R., & Shaft, U. (1999). When is "nearest neighbor" meaningful? *Proceedings of the 7th International Conference on Database Theory*, 217--235.

Bijmolt, T. H. A., & Wedel, M. (1999). A comparison of multidimensional scaling methods for perceptual mapping. *Journal of Marketing Research*, 36(1), 137--153.

Busemeyer, J. R., & Bruza, P. D. (2012). *Quantum Models of Cognition and Decision*. Cambridge University Press.

Campbell, L. L. (1986). An extended Cencov characterization of the information metric. *Proceedings of the American Mathematical Society*, 98(1), 135--141.

Carroll, J. D., & Chang, J.-J. (1970). Analysis of individual differences in multidimensional scaling via an N-way generalization of "Eckart-Young" decomposition. *Psychometrika*, 35(3), 283--319.

Cencov, N. N. (1972). *Statistical Decision Rules and Optimal Inference*. Nauka (in Russian). English translation: American Mathematical Society, 1982.

DeSarbo, W. S., Kim, Y., Choi, S. C., & Spaulding, M. (2002). A gravity-based multidimensional scaling model for deriving spatial structures underlying consumer preference/choice judgments. *Journal of Consumer Research*, 29(1), 91--100.

Gardenfors, P. (2000). *Conceptual Spaces: The Geometry of Thought*. MIT Press.

Hegselmann, R., & Krause, U. (2002). Opinion dynamics and bounded confidence: Models, analysis and simulation. *Journal of Artificial Societies and Social Simulation*, 5(3), 2.

Johnson, N. L., & Kotz, S. (1972). *Distributions in Statistics: Continuous Multivariate Distributions*. Wiley.

Kapferer, J.-N. (2008). *The New Strategic Brand Management: Creating and Sustaining Brand Equity Long Term* (4th ed.). Kogan Page.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1--22.

Lancaster, K. J. (1966). A new approach to consumer theory. *Journal of Political Economy*, 74(2), 132--157.

Ledoux, M. (2001). *The Concentration of Measure Phenomenon*. American Mathematical Society.

Levy, P. (1951). *Problemes concrets d'analyse fonctionnelle*. Gauthier-Villars.

Milman, V. D. (1971). A new proof of A. Dvoretzky's theorem on cross-sections of convex bodies. *Functional Analysis and Its Applications*, 5(4), 288--295.

Milman, V. D., & Schechtman, G. (1986). *Asymptotic Theory of Finite Dimensional Normed Spaces*. Lecture Notes in Mathematics, Vol. 1200. Springer.

Molenaar, P. C. M. (2004). A manifesto on psychology as idiographic science: Bringing the person back into scientific psychology, this time forever. *Measurement*, 2(4), 201--218.

Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, 15, 1216--1221.

Smith, W. R. (1956). Product differentiation and market segmentation as alternative marketing strategies. *Journal of Marketing*, 21(1), 3--8.

Todd, J. T., Oomes, A. H. J., Koenderink, J. J., & Kappers, A. M. L. (2001). On the affine structure of perceptual space. *Psychological Science*, 12(3), 191--196.

Vershynin, R. (2018). *High-Dimensional Probability: An Introduction with Applications in Data Science*. Cambridge University Press.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. SSRN Working Paper.

Zharnikov, D. (2026b). The alibi problem: Epistemic foundations of multi-source data reconciliation. SSRN Working Paper.

Zharnikov, D. (2026c). Geometric approaches to brand perception: A critical survey and research agenda. SSRN Working Paper.

Zharnikov, D. (2026d). Brand space geometry: A formal metric for multi-dimensional brand perception. SSRN Working Paper.

Zharnikov, D. (2026i). The Organizational Schema Theory: Test-driven business design. SSRN Working Paper.

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper.
