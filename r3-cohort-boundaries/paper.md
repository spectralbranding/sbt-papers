# Geometric Necessity of Fuzzy Cohort Boundaries: A Concentration Analysis of the 7-Simplex

**Dmitry Zharnikov**

ORCID: 0009-0000-6893-9231

Working Paper v1.1.0 — March 2026 (Updated May 2026)

https://doi.org/10.5281/zenodo.18945477

---

## Abstract

This paper applies concentration-of-measure techniques to the probability simplex $\Delta^7$ under the uniform Dirichlet$(1,\ldots,1)$ null. Three results follow. First, the Euclidean distance contrast ratio degrades to approximately 7.5 at $n = 8$, placing the space in a transitional regime where clustering remains informative yet noisy. Second, for any convex $k$-partition of $\Delta^7$, the volume fraction within relative Euclidean distance $\delta = .10$ of any boundary is at least 52.2%. Third, Lévy's lemma on the 7-sphere yields $P(|f - M_f| \geq \varepsilon) \leq 4\exp(-7\varepsilon^2/8)$ for 1-Lipschitz functions. Monte Carlo simulations with $10^5$ draws confirm the predictions within sampling error. These bounds imply that a majority of observer profiles lie near at least one cohort boundary under the uniform null, making discrete assignment inherently unstable. The uniform distribution maximizes boundary volume; symmetric Dirichlet$(\alpha,\ldots,\alpha)$ with $\alpha \geq 3$ reduces the fraction by $\alpha^{-7/2}$, producing operationally crisp boundaries (below 2%) for empirically plausible $\alpha$. The results give a geometric foundation for preferring continuous observer profiles over discrete cohort labels once perceptual dimensionality exceeds five. Fisher-Rao recalculation via the sphere isometry confirms the qualitative conclusions.

**Keywords**: concentration of measure, cohort boundaries, probability simplex, Lévy's lemma, brand perception, high-dimensional geometry, Spectral Brand Theory

**JEL Classification**: C65, M31, C38

**MSC Classification**: 60E15, 52A21, 91B42

---

## 1.

Market segmentation -- partitioning observers into discrete groups assumed to possess internally homogeneous and externally heterogeneous response profiles -- has been foundational practice since Smith (1956); Wedel and Kamakura (2000) review the canonical latent-class and mixture-model machinery. Practitioners routinely treat cohort boundaries as sharp, membership as unambiguous, and the number of groups as an objective feature of the underlying population rather than a methodological choice. This paper demonstrates that such assumptions systematically fail in moderately high-dimensional perceptual spaces.

Consumer perception is naturally represented as a compositional weight vector $w \in \Delta^{n-1}$ allocating finite attention across $n$ attributes. When $n = 8$ -- as arises in multi-attribute models that separately track Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal components (hereafter the multi-attribute observer-weight construction; see Zharnikov 2026a for branding-domain context) -- the geometry of the simplex forces substantial mass near any partition boundary. Concentration of measure (Ledoux 2001; Vershynin 2018; Wainwright 2019) implies that distances between typical points concentrate tightly around their mean, eroding contrast, and that volume concentrates near boundaries. Consequently, for any convex partition of $\Delta^7$, more than half the probability mass lies within a relative distance $\delta = .10$ of at least one boundary.

**Related literature.** The mathematical theory of concentration on spheres and simplices is developed in Lévy (1951), Milman and Schechtman (1986), Ledoux (2001), Boucheron, Lugosi, and Massart (2013), Vershynin (2018), Wainwright (2019), and Giraud (2014); the convex-body / Brunn-Minkowski toolkit is consolidated in Schneider (2014). The boundary phenomena of high-dimensional geometry are surveyed by Donoho and Tanner (2009). Discrete-segmentation critiques in adjacent fields include Bühlmann, Kalisch, and Meier (2014) for biological high-dimensional inference, Bronnenberg, Dubé, and Gentzkow (2016) for preference heterogeneity, Evgeniou, Boussios, and Zacharia (2005) for regularization in choice models, and Rossi and Allenby (2003) for Bayesian mixture treatments. Methodological warnings about over-fitting categorical structure to high-dimensional consumer data appear in Wedel and Kannan (2016), Netzer, Feldman, Goldenberg, and Fresko (2012), and Kriegel, Kröger, and Zimek (2009). A counterpoint is Gorban and Tyukin (2018) "blessing of dimensionality": individual points become stochastically separable as dimension grows -- compatible with the present majority-near-boundary result at a different level of analysis (Section 3.3). The contribution here is to make the geometric obstruction explicit for the moderate-dimensional simplex $\Delta^7$ relevant to multi-attribute perceptual modeling, and to derive a quantitative volume bound that translates into operational guidance about discrete versus continuous cohort representation.

This paper derives explicit non-asymptotic bounds on both phenomena under the uniform Dirichlet null. The two principal contributions are:

1. **Boundary-volume bounds for convex $k$-partitions of the probability simplex** (Theorem 2 and Corollaries 1--2), establishing that at $n = 8$, $\delta = .10$, at least 52.2% of $\Delta^7$ lies near any partition boundary under the uniform null, and that this fraction shrinks as $\alpha^{-(n-1)/2}$ when observer weights are concentrated rather than uniform.

2. **Methodological implication for discrete versus continuous cohort representation** in moderate-dimensional perceptual spaces. The bounds quantify the information loss from rasterized cohort labels relative to vectorized observer profiles, and identify $n \approx 5$ as the dimensionality threshold beyond which discrete assignment systematically misrepresents a majority of the population.

The paper proceeds as follows. Section 2 recalls the relevant geometry (with $\Delta^7$ and the Fisher-Rao metric established in Zharnikov 2026d). Section 3 develops concentration of measure on the simplex. Section 4 proves the boundary fuzziness theorems. Section 5 presents Monte Carlo verification. Section 6 develops the implications for branding practice. Section 7 connects the results to non-ergodic dynamics. Section 8 extends the analysis to concentrated Dirichlet$(\alpha,\ldots,\alpha)$ distributions, showing that the uniform case is the worst case and that real populations have sharper boundaries. Section 9 discusses limitations. Section 10 concludes.

---

## 2. Preliminaries

### 2.1 SBT Framework and Dimensional Architecture

Spectral Brand Theory (Zharnikov, 2026a) models brands as signal-emitting objects in an eight-dimensional space. The eight dimensions are: Semiotic (visual identity, design language), Narrative (brand story, founding mythology), Ideological (values, beliefs, positioning), Experiential (product/service interaction quality), Social (community, affiliation, status), Economic (pricing, value proposition), Cultural (cultural resonance, zeitgeist alignment), and Temporal (heritage, longevity, temporal compounding).

An observer's **spectral profile** includes, among other components, a **weight vector** $w = (w_1, \ldots, w_8) \in \Delta^7$ representing the relative salience the observer assigns to each dimension. The constraint $\sum_{i=1}^8 w_i = 1$ reflects the finite-resource assumption: increasing attention to one dimension reduces attention to others. The equal-weight profile $w^* = (1/8, \ldots, 1/8)$ represents maximum-entropy observation; corner profiles such as $(1, 0, \ldots, 0)$ represent observers whose perception is dominated by a single dimension. The theoretical justification for exactly eight dimensions — their completeness and necessity — is developed in Zharnikov (2026r); the present paper takes the 8-dimensional architecture as given and derives its geometric consequences.

A **perceptual cohort** is a cluster of observers whose weight profiles are geometrically proximate in $\Delta^7$. Unlike traditional demographic segments, perceptual cohorts are defined by *how* observers process signals, not by *who* they are. An affluent 25-year-old and a middle-income 55-year-old who both weight the Ideological and Narrative dimensions heavily belong to the same perceptual cohort, despite occupying distant positions in demographic space.

SBT posits five case-study brands -- Hermès (A+), IKEA (A-), Patagonia (B+), Erewhon (B-), Tesla (C-) -- analyzed through this framework. Cross-model replication (Claude and Gemini independently analyzing the same data) produced identical coherence types and grades for all five brands but different cohort granularities, motivating the present investigation.

### 2.2 The Observer Weight Space $(\mathcal{O}, d_\mathcal{O})$

Zharnikov (2026d) established that the observer weight space is the probability simplex $\Delta^7$ equipped with the Fisher-Rao metric. The Fisher-Rao distance between two observer profiles is:

$$d_{FR}(w_1, w_2) = 2 \arccos\left( \sum_{i=1}^8 \sqrt{w_{1,i} \cdot w_{2,i}} \right)$$

This metric is the unique (up to scaling) Riemannian metric on the space of probability distributions that is invariant under sufficient statistics, as established by Cencov's uniqueness theorem (Cencov, 1972; Campbell, 1986). Amari and Nagaoka (2000) provide the canonical information-geometry treatment of the Fisher-Rao metric and its dual connections, situating Cencov's result within the broader framework of statistical manifolds. The justification is that reparametrizing the eight dimensions (e.g., combining "social" and "cultural" into a single dimension and splitting "experiential" into sub-dimensions) should not change the distance between observers, and the Fisher-Rao metric is the unique distance function with this property.

The square-root transform $\phi(w) = (2\sqrt{w_1}, \ldots, 2\sqrt{w_8})$ maps $\Delta^7$ isometrically to the positive orthant of the sphere $S^7_+$ of radius 2, where the Fisher-Rao distance becomes the geodesic (arc-length) distance on the sphere. This connection is the bridge between concentration of measure on spheres (a well-developed theory) and concentration on the simplex (which we develop below).

### 2.3 Clustering on the Simplex

Given $m$ observer profiles $w_1, \ldots, w_m \in \Delta^7$, a **$k$-partition** (cohort structure) is a division of $\Delta^7$ into $k$ regions $C_1, \ldots, C_k$ such that $\bigcup_{j=1}^k C_j = \Delta^7$ and $C_i \cap C_j = \emptyset$ for $i \neq j$ (up to boundaries). Standard $k$-means clustering seeks to minimize the within-cluster sum of squared distances:

$$\text{WCSS}(k) = \sum_{j=1}^k \sum_{w \in C_j} d_{FR}(w, \mu_j)^2$$

where $\mu_j$ is the Frechet mean of cluster $C_j$ in the Fisher-Rao metric. The "elbow method" and silhouette scores are commonly used to select $k$, but these depend on arbitrary thresholds and are sensitive to initialization (Arthur & Vassilvitskii, 2007). The present paper shows that this sensitivity is not a failure of particular algorithms but a consequence of the geometry of $\Delta^7$.

---

## 3. Concentration of Measure on the Simplex

### 3.1 Lévy's Lemma and Spherical Concentration

The concentration of measure phenomenon was identified by Lévy (1951) in his study of sphere geometry and developed into its modern form by Milman (1971) and Gromov and Milman (1983); Ledoux (2001) provides a systematic treatment. The central result, now known as Lévy's lemma, states that a Lipschitz-continuous function on a high-dimensional sphere takes values close to its median with overwhelming probability.

**Assumption (Euclidean distance throughout Sections 3.1–3.3 and 4–5).** Distance computations in Sections 3.1–3.3 and 4–5 use Euclidean distance on $\Delta^{n-1}$. SBT's formal observer-space metric is Fisher-Rao (Zharnikov 2026d), which via the square-root transform is isometric to geodesic distance on $S^7_+$; Lévy concentration (Proposition 1) therefore applies directly. The precise Euclidean numerical bounds -- contrast ratio 7.46 and boundary fraction 52.2% at $n = 8$, $\delta = .10$ -- are recomputed under Fisher-Rao in Section 3.4; the qualitative conclusions are unchanged.

Note also that Talagrand's (1995) canonical product-space isoperimetric framework is the modern reference for concentration inequalities; however, the Dirichlet distribution on $\Delta^{n-1}$ is not a product measure (the sum-to-one constraint induces dependence among components), so Talagrand's product-space bounds do not apply directly and the sphere-isometry route via Milman and Schechtman (1986) is used here.

**Proposition 1** (Lévy concentration on $S^{n-1}$, specialized to $S^7$). *Let $f: S^{n-1} \to \mathbb{R}$ be a $1$-Lipschitz function with respect to geodesic distance on the unit sphere $S^{n-1}$, and let $M_f$ denote its median with respect to the uniform (Haar) measure. Then for general $S^{n-1}$:*

$$P\left(|f(x) - M_f| \geq \varepsilon \right) \leq 4 \exp\left( -\frac{(n-1)\varepsilon^2}{8} \right)$$

*Specializing to $n = 8$ (the SBT case, $S^7$): $P(|f(x) - M_f| \geq \varepsilon) \leq 4 \exp(-7\varepsilon^2/8)$.*

*Proof sketch.* The result follows from the Gaussian isoperimetric inequality on the sphere (Milman & Schechtman, 1986, Theorem 2.4; Ledoux, 2001, Proposition 1.4). The key step uses the fact that the uniform measure on $S^{n-1}$ satisfies a logarithmic Sobolev inequality with constant $(n-1)^{-1}$, from which the sub-Gaussian concentration follows by the Herbst argument. The factor of 4 arises from bounding the measure of both tails. For a complete proof, see Vershynin (2018, Theorem 5.1.4); for a systematic nonasymptotic treatment, see Boucheron, Lugosi, and Massart (2013). $\square$

The practical import of Proposition 1 is that any "well-behaved" (Lipschitz) function of an observer's position on the sphere -- including, crucially, the distance from that observer to a cohort centroid -- cannot vary much from its typical value. At $n = 8$, the numerical bounds are:

**Table 1: Lévy Concentration Bounds on $S^7$ at Selected Deviation Thresholds.**

| $\varepsilon$ | $P(\|f - M_f\| \geq \varepsilon)$ (standard) | $P$ (sharp, sets of measure 1/2) |
|---|---|---|
| 1.0 | $\leq 1.667$ | $\leq 0.060$ |
| 1.5 | $\leq 0.559$ | $\leq 0.00076$ |
| 2.0 | $\leq 0.121$ | $\leq 0.000002$ |

*Notes*: Standard bound: $4\exp(-(n-1)\varepsilon^2/8)$ at $n=8$. Sharp bound: $2\exp(-(n-1)\varepsilon^2/2)$ for sets of measure $\geq 1/2$. Values $> 1$ are vacuous bounds; concentration becomes non-trivial for $\varepsilon \geq 1.07$ on $S^7$.

The standard Lévy bound becomes non-trivial (i.e., falls below 1) only for $\varepsilon \geq 1.07$ on $S^7$. This is a consequence of the moderate dimensionality: at $n = 8$, we are in a transitional regime where concentration effects are present but not dominant. In contrast, for $n = 100$ (a common dimensionality in machine learning applications), the bound becomes non-trivial for $\varepsilon \geq 0.18$.

A sharper result holds for sets rather than functions. For any measurable set $A \subset S^{n-1}$ with $\sigma(A) \geq 1/2$ (where $\sigma$ is the normalized Haar measure):

$$P\left(d(x, A) \geq \varepsilon\right) \leq 2 \exp\left(-\frac{n-1}{2} \varepsilon^2\right)$$

This "blowup" inequality (Milman & Schechtman, 1986) states that a set covering half the sphere, when expanded by distance $\varepsilon$, covers almost all of it. For $S^7$: $P(d(x,A) \geq 1.0) \leq 0.060$ and $P(d(x,A) \geq 1.5) \leq 0.00076$.

**Interpretation for SBT.** A perceptual cohort that "covers" half the observer weight space, when expanded by a Fisher-Rao distance of 1.0, covers approximately 94% of the space. This means the transition zone between "inside the cohort" and "outside the cohort" is wide relative to the distances between typical observers.

### 3.2 Concentration on $\Delta^7$ via the Dirichlet Distribution

The uniform distribution on $\Delta^{n-1}$ is the $\text{Dirichlet}(1, \ldots, 1)$ distribution with $n$ parameters all equal to 1. This provides a null model for observer weight profiles: if observers had no systematic tendencies in dimensional weighting, their profiles would follow this distribution. **Important caveat**: the uniform distribution here is a worst-case mathematical bound, not an empirical model of actual observer populations. The results of Corollary 1 and Theorem 2 hold under this null; Section 8 shows that any real population with $\alpha > 1$ has strictly smaller boundary fractions. The null model should not be read as a claim that populations are uniformly distributed.

**Proposition 2** (Dirichlet component statistics). *For $X = (X_1, \ldots, X_n) \sim \text{Dir}(\alpha, \ldots, \alpha)$ on $\Delta^{n-1}$ with $\alpha = 1$ (uniform), each component satisfies:*

$$E[X_i] = \frac{1}{n}, \quad \text{Var}[X_i] = \frac{(1/n)(1 - 1/n)}{n + 1}$$

*At $n = 8$: $E[X_i] = 0.125$, $\text{Var}[X_i] = 0.012153$, $\text{SD}[X_i] = 0.1102$.*

*Proof.* For $X \sim \text{Dir}(\alpha_1, \ldots, \alpha_n)$ with $\alpha_0 = \sum \alpha_j$, the marginal moments are $E[X_i] = \alpha_i / \alpha_0$ and $\text{Var}[X_i] = \alpha_i(\alpha_0 - \alpha_i) / (\alpha_0^2(\alpha_0 + 1))$ (Johnson & Kotz, 1972). Setting $\alpha_i = 1$ for all $i$ gives $\alpha_0 = n$, yielding the stated formulas. $\square$

*Falsification*: Proposition 2 is falsified if empirical observer weight profiles drawn from any Dirichlet$(1,\ldots,1)$ model show component variance differing from $1/[n(n+1)] = .012$ at $n = 8$ by more than Monte Carlo sampling error.

The standard deviation of 0.1102 relative to the mean of 0.125 indicates a coefficient of variation of 88%. Under the uniform null model, observer weight profiles are highly variable -- individual dimensions fluctuate by nearly their own magnitude. This high variability is what makes clustering non-trivial: observers genuinely differ in their dimensional weightings.

However, the Dirichlet structure also introduces correlations. The components of a Dirichlet vector are negatively correlated:

$$\text{Cov}[X_i, X_j] = -\frac{(1/n)^2}{n + 1} = -\frac{1}{n^2(n+1)}$$

At $n = 8$: $\text{Cov}[X_i, X_j] = -0.001736$. The sum-to-one constraint means that when one dimension receives more weight, others must receive less, creating negative correlations that affect the geometry of pairwise distances.

**Geometric versus statistical fuzziness.** Readers familiar with Latent Dirichlet Allocation (Blei, Ng, and Jordan 2003) will recognise the Dirichlet-on-simplex framework and may wonder whether the boundary fuzziness derived here is simply the familiar posterior uncertainty of LDA. The distinction is important. In LDA, documents are assigned to topics with probabilities that form a Dirichlet posterior; this posterior sharpens as more data are observed — in the limit of infinite data, each document belongs to a definite topic. The fuzziness in the present paper is different in kind: it is *geometric* fuzziness intrinsic to the structure of $\Delta^{n-1}$ under any partition, regardless of sample size. Theorem 2 holds for the deterministic geometric volume of the simplex — it says nothing about posterior uncertainty. A researcher with arbitrarily many observations can estimate observer weight vectors $w \in \Delta^7$ with arbitrary precision, yet still face the fact that at least 52% of those precisely-located profiles lie near a partition boundary. The boundary fuzziness here derives from the Brunn-Minkowski inequality, not from data sparsity.

### 3.3 Beyer's Distance Contrast Phenomenon

Beyer, Goldstein, Ramakrishnan, and Shaft (1999) demonstrated a fundamental challenge for distance-based methods in high dimensions: as dimensionality increases, the contrast between the nearest and farthest points degrades. Specifically, for i.i.d. data with finite variance, the ratio $\max_d / \min_d$ converges to 1 as $n \to \infty$, meaning that in the limit, all points are equidistant. This undermines distance-based classification, clustering, and nearest-neighbor methods.

**Theorem 1** (Distance concentration on $\Delta^7$). *Let $w_0, w_1, \ldots, w_{m-1} \in \Delta^{n-1}$ be $m$ i.i.d. draws from $\text{Dir}(1, \ldots, 1)$, and let $D_j = \|w_j - w_0\|_2$ for $j = 1, \ldots, m-1$ denote Euclidean distances from $w_0$ to the remaining points. Define the distance contrast ratio $R_n = \max_j D_j / \min_j D_j$. Then (see Section 8 for discussion of Fisher-Rao generalization):*

*(a) The expected squared distance is:*

$$E[\|w_i - w_j\|_2^2] = 2 \sum_{l=1}^n \text{Var}[X_l] = \frac{2(n-1)}{n(n+1)}$$

*At $n = 8$: $E[\|w_i - w_j\|_2^2] = 14/72 = 7/36 \approx 0.1944$, giving $\sqrt{E[D^2]} \approx 0.4410$.*

*(b) The distance contrast ratio degrades with dimension. Monte Carlo estimation with $m = 1000$ yields:*

**Table 2: Distance Contrast Ratio Degradation with Dimension on the Simplex.**

| $n$ | $R_n$ (contrast ratio) | Mean Euclidean distance | SD of distances |
|---|---|---|---|
| 2 | 9797.06 | .4681 | .3065 |
| 4 | 31.94 | .5024 | .1878 |
| 8 | 7.46 | .4254 | .1052 |
| 16 | 3.80 | .3249 | .0563 |
| 32 | 2.47 | .2397 | .0294 |

*Notes*: $R_n = \max_j D_j / \min_j D_j$ for $m = 1000$ i.i.d. draws from Dir$(1,\ldots,1)$ on $\Delta^{n-1}$. Monte Carlo estimates from $10^4$ independent trials; SEs on ratio estimates $< 1\%$ for $n \geq 4$. Distances are Euclidean. Reproducible from `code/r3_concentration_mc.py` in the companion repository (seed 42).

*(c) The coefficient of variation $\text{CV}_n = \text{SD}[D] / E[D]$ decreases as $\text{CV}_n \sim O(n^{-1/2})$, reflecting concentration of the distance distribution around its mean.*

*Proof of (a).* By linearity of expectation and the identity $E[\|w_i - w_j\|^2] = 2\sum_l \text{Var}[X_l]$ for i.i.d. random vectors:

$$E[\|w_i - w_j\|^2] = \sum_{l=1}^n E[(X_{i,l} - X_{j,l})^2] = \sum_{l=1}^n 2\text{Var}[X_l] = 2n \cdot \frac{(1/n)(1-1/n)}{n+1} = \frac{2(n-1)}{n(n+1)}$$

At $n = 8$: $2 \cdot 7 / (8 \cdot 9) = 14/72 = 7/36 \approx .1944$. The identity $E[\|w_i - w_j\|^2] = 7/36$ was first derived in Zharnikov (2026d) for the warped-product manifold structure of the observer weight space; the derivation here recovers it directly from Dirichlet moment formulas. $\square$

*Proof sketch of (b).* The concentration of $R_n$ follows from Beyer et al.'s (1999) general framework. Under mild regularity conditions on the component distribution, $\text{Var}[D^2] / (E[D^2])^2 \to 0$ as $n \to \infty$, implying $R_n \to 1$. For finite $n$, the rate depends on the moment structure of the Dirichlet components. The values in the table are Monte Carlo estimates from $10^4$ independent trials; standard errors on the ratio estimate are below 5% for all $n$. $\square$

**Interpretation.** At $n = 8$, the contrast ratio of 7.46 is in a transitional regime. It is far from the extreme $n = 2$ case (where the nearest and farthest points differ by a factor of nearly $10^4$, making clustering straightforward) but also far from the $n = 32$ regime (where a ratio of 2.47 makes distance-based discrimination nearly impossible). This transitional character means that:

1. Clustering on $\Delta^7$ is *possible* -- distances carry genuine discriminative information.
2. Clustering on $\Delta^7$ is *inherently noisy* -- the boundary between "nearby" and "far away" is blurred relative to low-dimensional spaces.
3. The number of clusters recovered depends sensitively on the algorithm's distance threshold -- explaining why different methods (or different AI models) may recover different cluster counts from identical data.

The coefficient of variation provides a complementary view. At $n = 8$, $\text{CV}_8 = 0.1052 / 0.4254 = 0.247$, meaning that distances fluctuate by about 25% around their mean. By comparison, at $n = 2$, $\text{CV}_2 = 0.3065 / 0.4681 = 0.655$, and at $n = 32$, $\text{CV}_{32} = 0.0294 / 0.2397 = 0.123$. The 8-dimensional simplex occupies an intermediate position where distance-based methods still function but with substantially reduced discriminative power compared to low-dimensional settings.

**Relation to the blessing of dimensionality.** Gorban and Tyukin (2018) observed that in high-dimensional spaces, almost all data points become stochastically separable from a given random point — a counterintuitive "blessing" that enables powerful linear classifiers with high probability. The concentration results above and Gorban and Tyukin's separability result are compatible at different levels of analysis: Gorban and Tyukin characterise the separability of *individual points* from a fixed reference, whereas Theorem 1 and Theorem 2 characterise the concentration of *pairwise distances* and the *volume of boundary zones under any partition*. High separability of individual points does not prevent boundary zones from being voluminous — the majority-near-boundary result is a statement about the geometry of partition regions, not about pairwise distinguishability.

### 3.4 Fisher-Rao Recalculation

The numerical bounds in Sections 3.1–3.3 use Euclidean distance on $\Delta^7$ for tractability. Because SBT's canonical observer-space metric is Fisher-Rao (Zharnikov 2026d), this subsection presents the corresponding Fisher-Rao bounds via the square-root isometry to the sphere (Cencov 1981; Amari and Nagaoka 2000).

**Distance contrast under Fisher-Rao.** The square-root transform $\phi: \Delta^{n-1} \to S^{n-1}_+$, $\phi(w) = 2(\sqrt{w_1}, \ldots, \sqrt{w_n})$, sends Dir$(1,\ldots,1)$ on $\Delta^7$ to a (non-uniform) distribution on the positive orthant $S^7_+$ of radius 2, with the Fisher-Rao distance becoming the geodesic (arc-length) distance. The expected pairwise Fisher-Rao distance under uniform Dir$(1,\ldots,1)$ is computable analytically via $E[\sum_i \sqrt{p_i q_i}] = n \cdot E[\sqrt{X_i}]^2$ for $X_i \sim$ Beta$(1, n-1)$. At $n = 8$, $E[\sqrt{X_i}] = \Gamma(3/2)\Gamma(8)/\Gamma(8.5) \approx .3183$, giving $E[\sum_i \sqrt{p_i q_i}] \approx .811$ and a typical Fisher-Rao distance of $2\arccos(.811) \approx 1.255$ rad.

Monte Carlo simulation with $m = 1000$ and $10^3$ trials (script: `code/r3_concentration_mc.py` in the companion repository) yields the figures in Table 7.

**Table 7: Distance Concentration on $\Delta^7$ under Euclidean and Fisher-Rao Metrics.**

| Metric | $R_8$ (contrast ratio) | Mean distance | CV |
|---|---|---|---|
| Euclidean | 7.46 ± .02 | .4254 | .247 |
| Fisher-Rao | 5.72 ± .01 | 1.22 rad | .230 |

*Notes*: Monte Carlo with $m = 1000$ draws from Dir$(1,\ldots,1)$ at $n = 8$, $10^4$ trials in each metric (seed 42). Fisher-Rao distance is the geodesic distance on $S^7_+$ (radius 2) under the square-root isometry. Both metrics place $\Delta^7$ in the transitional regime ($R_8 \in [5, 10]$).

The Fisher-Rao contrast ratio is somewhat lower than Euclidean (5.72 vs 7.46) but in the same transitional regime: clustering is possible but noisy. The slight reduction reflects the curvature of the spherical embedding, which compresses pairwise distances near the equator of $S^7_+$ relative to the chord-length Euclidean metric.

**Boundary volume fraction under Fisher-Rao.** Theorem 2's bound $\text{BVF}(n, \delta) \geq 1 - (1 - \delta)^{n-1}$ depends on the intrinsic dimension of the simplex $\Delta^{n-1}$, which is $n - 1$. The Fisher-Rao isometry to $S^7_+$ preserves the intrinsic dimension; the same Brunn-Minkowski peeling argument applies on the spherical patch with the geodesic volume element (Schneider 2014, Section 6.5). The bound therefore transfers verbatim:

$$\text{BVF}^{\text{FR}}(n, \delta) \geq 1 - (1 - \delta)^{n-1}$$

with $\delta$ now interpreted as relative geodesic distance to the boundary, and the same numerical value 52.2% at $n = 8$, $\delta = .10$. The Lévy concentration bound (Proposition 1) is itself a Fisher-Rao result on $S^7$, so no additional translation is required.

The two-metric comparison shows that the qualitative conclusions of the paper -- transitional concentration regime, majority-near-boundary, geometric necessity of fuzzy cohort assignment -- hold under both metrics. Numerical bounds on the contrast ratio differ modestly (Fisher-Rao $\approx 70\%$ of Euclidean); the boundary-volume bound is identical in form and value.

---

## 4. Boundary Fuzziness in Partitioned Spaces

### 4.1 Volume Near Boundaries in High Dimensions

A fundamental geometric fact about high-dimensional convex bodies is that their volume concentrates near the boundary. For the unit $n$-cube $[0,1]^n$, the fraction of volume within distance $\delta$ of the boundary (in the $\ell^\infty$ sense) is $1 - (1 - 2\delta)^n$, which approaches 1 rapidly with $n$. This "boundary concentration" phenomenon has a direct analogue for partitioned spaces.

Consider a convex body $K \subset \mathbb{R}^n$ partitioned into $k \geq 2$ convex regions $C_1, \ldots, C_k$. The **boundary zone** at width $\delta$ is defined as:

$$B_\delta = \left\{ x \in K : \min_{j \neq j(x)} d(x, \partial C_j) \leq \delta \right\}$$

where $j(x)$ is the index of the region containing $x$, $d$ denotes Euclidean distance on $\Delta^{n-1}$, and $d(x, \partial C_j)$ is the distance from $x$ to the boundary of region $C_j$. Points in $B_\delta$ are "close to being in a different cohort" -- their assignment depends on the exact placement of the boundary.

### 4.2 Boundary Fraction Theorem for Convex Partitions

**Theorem 2** (Boundary fuzziness on $\Delta^7$). *Let $\Delta^{n-1}$ be the standard $(n-1)$-simplex and let $C_1, \ldots, C_k$ ($k \geq 2$) be a partition of $\Delta^{n-1}$ into convex regions. For the relative boundary width parameter $\delta \in (0, 1)$, define the boundary volume fraction as the fraction of $\Delta^{n-1}$ (with respect to Lebesgue measure on the simplex) lying within relative distance $\delta$ of any partition boundary. Then:*

$$\text{BVF}(n, \delta) \geq 1 - (1 - \delta)^{n-1}$$

*The exponent $n-1$ reflects the intrinsic dimension of the simplex $\Delta^{n-1}$, which is embedded in $\mathbb{R}^n$ but lies on the affine hyperplane $\sum_i w_i = 1$ and so has dimension $n-1$ as a manifold. In particular, at $n = 8$:*

**Table 3: Boundary Volume Fraction at $n = 8$ Across Relative Boundary Widths.**

| $\delta$ | $\text{BVF}(8, \delta)$ | Interpretation |
|---|---|---|
| .01 | 6.8% | Extremely narrow boundary |
| .05 | 30.2% | About one-third of space is boundary |
| .10 | 52.2% | Majority of space is boundary |
| .20 | 79.0% | Vast majority is boundary |
| .30 | 91.8% | Almost all space is boundary |

*Notes*: $\text{BVF}(n, \delta) = 1 - (1-\delta)^{n-1}$ with $n - 1 = 7$ for $\Delta^7$. Values are lower bounds on the fraction of $\Delta^7$ lying within relative Euclidean distance $\delta$ of any convex partition boundary.

*Proof.* The argument uses the Brunn-Minkowski peeling technique for convex bodies (Schneider 2014, Theorem 7.1.1; Vershynin 2018, Section 5.2). Consider first the simplest case: a bisection of $\Delta^{n-1}$ by a hyperplane through its centroid into two convex regions $C_1, C_2$.

For any point $x \in \Delta^{n-1}$, define its relative depth as the ratio $d(x, \partial) / R$, where $\partial$ is the partition boundary and $R$ is the in-radius of the cell containing $x$. The set of points with relative depth $\geq \delta$ is contained in the homothet of the cell scaled by factor $(1 - \delta)$ from the boundary. Because the simplex $\Delta^{n-1}$ is an $(n-1)$-dimensional manifold (lying on the affine hyperplane $\sum_i w_i = 1$ in $\mathbb{R}^n$), Lebesgue measure on $\Delta^{n-1}$ scales as the $(n-1)$th power of linear dimensions:

$$\text{Vol}\left(\{x : \text{rel-depth}(x) \geq \delta\}\right) \leq (1 - \delta)^{n-1} \cdot \text{Vol}(\Delta^{n-1})$$

Taking complements gives the boundary volume fraction $\text{BVF}(n, \delta) \geq 1 - (1 - \delta)^{n-1}$. The Brunn-Minkowski inequality on the convex bodies $C_1, C_2$ extends the bound from hyperplane bisections to arbitrary convex partitions: for $k > 2$ convex regions the boundary fraction is strictly larger because additional boundaries contribute additional boundary volume (Schneider 2014, Section 7.1). The bound is therefore conservative for $k \geq 3$. $\square$

**Conservative bound versus tighter ambient-dimension calculation.** An earlier presentation of this result used the ambient-dimension exponent $n$ rather than the intrinsic-dimension exponent $n-1$, yielding 57.0% at $\delta = .10$ rather than 52.2%. The intrinsic-dimension calculation is the correct headline figure: the $(n-1)$ exponent reflects the simplex's true geometric dimension, and the resulting bound 52.2% is tight in the sense that it is approached by hyperplane bisections through the centroid. The ambient-dimension calculation is conservative (over-estimates the fraction by approximately five percentage points at $n = 8$, $\delta = .10$) and is appropriate when multiple partition boundaries interact in a way that effectively expands the boundary zone in $\mathbb{R}^n$. For exposition, the intrinsic-dimension figure is used throughout. Monte Carlo with $k = 4$ Voronoi partitions (Section 5.2) yields empirical boundary fractions of 62.5% at $\delta = .10$, comfortably exceeding both bounds and confirming that 52.2% is conservative for realistic $k$.

**Comparison across dimensions.** To appreciate the significance of the 8-dimensional result, we compare the boundary volume fraction across simplex dimensions at fixed $\delta = .10$:

**Table 4: Boundary Volume Fraction Across Simplex Dimensions at Fixed $\delta = .10$.**

| $n$ | Intrinsic dim. ($n-1$) | $\text{BVF}(n, .10)$ | Interpretation |
|---|---|---|---|
| 2 | 1 | 10.0% | Low-dimensional: boundaries are thin |
| 3 | 2 | 19.0% | Moderate: about one-fifth is boundary |
| 8 | 7 | 52.2% | High: majority is boundary |
| 16 | 15 | 79.4% | Very high: most space is boundary |
| 48 | 47 | 99.3% | Near-total: essentially all boundary |

*Notes*: $\text{BVF}(n, \delta) = 1 - (1-\delta)^{n-1}$. At $\delta = .10$, these are lower bounds on the fraction of the simplex that lies within 10% relative distance of any convex partition boundary.

At $n = 2$ (a single intrinsic dimension, as in traditional quality-tier segmentation), only 10% of the space lies near a boundary -- segments are sharp. At $n = 8$ (the multi-attribute perceptual architecture), 52% lies near a boundary -- a majority of observers are in the "fuzzy zone." At $n = 48$ (the dimensionality of OrgSchema Theory's specification space; see Zharnikov 2026i), 99.3% is boundary -- partitioning is essentially meaningless.

### 4.3 Implications for Cohort Cardinality

Theorem 2 has a direct consequence for the relationship between cohort count $k$ and boundary sharpness.

**Corollary 1** (Dynamic cohort membership is geometrically necessary). *In 8-dimensional perception space, for any partition of $\Delta^7$ into $k \geq 2$ convex cohort regions, a majority of observer profiles lie within 10% relative distance of a cohort boundary. Therefore:*

*(a) Cohort membership for a typical observer is sensitive to small perturbations in the observer's weight profile, the partition boundary placement, or both.*

*(b) Any discrete cohort assignment for the majority of observers is unstable under perturbation of the boundary width parameter $\delta$.*

*(c) The claim that cohort membership is dynamic and fuzzy (Zharnikov, 2026a) is not merely an empirical observation but a geometric necessity in 8-dimensional perception space under uniform observer-weight distributions (Dirichlet-uniform on $\Delta^7$).*

*Proof.* By Theorem 2, $\text{BVF}(8, 0.10) \geq 52.2\% > 50\%$. An observer at distance $\leq 0.10 \cdot R$ from a boundary can be reassigned to an adjacent cohort by a shift of magnitude $0.10 \cdot R$ in their weight profile or an equivalent shift in the boundary. Since the standard deviation of Dirichlet-uniform components on $\Delta^7$ is 0.1102 (Proposition 2), perturbations of this magnitude are typical -- they correspond to the natural variability of observer profiles. Statements (a) and (b) follow directly. Statement (c) follows from the generality of the bound: it holds for *any* convex partition, not just a particular clustering algorithm. $\square$

*Falsification*: Corollary 1 is falsified if a study of observer weight profiles drawn from Dir$(1,\ldots,1)$ on $\Delta^7$ demonstrates that, in any convex $k$-partition, fewer than 50% of profiles lie within 10% relative distance of a boundary — contradicting the $\geq 57\%$ prediction of Theorem 2.

For larger $k$, the situation worsens. When $\Delta^7$ is divided into $k$ convex regions, each region has at most volume $1/k$ of the total, and its in-radius scales as $k^{-1/(n-1)}$. The boundary width $\delta$ measured relative to the in-radius must therefore increase for fixed absolute boundary width as $k$ grows. Increasing $k$ from 3 to 6 roughly doubles the total boundary surface area without proportionally increasing the total volume, which means a larger fraction of the volume falls in the boundary zone. This explains why Claude's 5--6 cohort structure and Gemini's 3-cohort structure are both geometrically valid: the finer partition simply has a wider proportional boundary zone, and the threshold at which the "boundary" observers are assigned to one cluster or the other is a free parameter.

---

## 5. Monte Carlo Verification

### 5.1 Distance Ratio Simulations

To verify Theorem 1, we conducted Monte Carlo simulations drawing $m = 1000$ points from $\text{Dir}(1, \ldots, 1)$ on $\Delta^{n-1}$ for $n \in \{2, 4, 8, 16, 32\}$. For each draw, we computed the Euclidean distances from a reference point to all others and recorded $\max_d / \min_d$, the mean distance, and the standard deviation. The simulations were repeated over $10^4$ independent trials and the results averaged.

The empirical distance statistics on $\Delta^7$ ($n = 8$, $m = 1000$):

- Mean Euclidean distance: $\bar{D} = 0.4254$
- Standard deviation: $\text{SD}[D] = 0.1052$
- Distance contrast ratio: $R_8 = 7.46$ (contrast $= R_8 - 1 = 6.46$)

These values are consistent with the theoretical prediction from Proposition 2. The empirical mean 0.4254 sits just below the theoretical $\sqrt{E[D^2]} = \sqrt{7/36} = 0.4410$ because $E[D] \leq \sqrt{E[D^2]}$ by Jensen's inequality (equivalently, $\sqrt{E[D^2]} - E[D] = \text{Var}(D)/(2\,E[D]) \approx 0.013$ for the observed variance).

The simulation also confirms the monotonic degradation of the contrast ratio with dimension, as tabulated in Theorem 1. The progression from $R_2 \approx 10^4$ to $R_{32} = 2.47$ illustrates the transition from a regime where nearest-neighbor queries are well-posed ($R \gg 1$, distances are highly discriminating) to one where they are degenerate ($R \approx 1$, all points are approximately equidistant). At $n = 8$, $R = 7.46$ is an intermediate value: distances discriminate, but with substantial noise.

### 5.2 Boundary Proximity Simulations

To verify Theorem 2, we performed the following procedure for $n = 8$, $k = 4$ cohorts:

1. Sample $m = 10^5$ points from $\text{Dir}(1,1,1,1,1,1,1,1)$ on $\Delta^7$.
2. Apply $k$-means clustering ($k = 4$) to obtain four convex (Voronoi) regions.
3. For each point, compute the Euclidean distance to the nearest cluster boundary (the perpendicular bisector between the two nearest centroids).
4. Compute the fraction of points within various multiples of $\delta$ from the boundary.

The empirical boundary volume fractions closely match the theoretical bound:

**Table 5: Monte Carlo Verification of Boundary Volume Fraction at $n = 8$.**

| $\delta$ | Theorem 2 prediction | Empirical ($k=4$, $10^5$ samples) |
|---|---|---|
| .05 | $\geq 30.2\%$ | $35.9\%$ |
| .10 | $\geq 52.2\%$ | $62.5\%$ |
| .20 | $\geq 79.0\%$ | $91.6\%$ |

*Notes*: $N = 10^5$ points drawn from Dir$(1,\ldots,1)$ on $\Delta^7$. $k = 4$ Voronoi partition obtained by $k$-means (seed 42). Boundary distance computed as absolute Euclidean distance to the perpendicular bisector between the two nearest centroids; $\delta$ is interpreted as an absolute Euclidean threshold (matching Theorem 2 when the simplex's effective diameter is order one). Empirical fractions reproducible from `code/r3_concentration_mc.py`.

The empirical values consistently exceed the theoretical lower bound, as expected since (a) the bound is conservative for $k \geq 3$, and (b) with $k = 4$ partitions there are multiple boundaries contributing to the boundary zone. The empirical excess of 6--13 percentage points reflects the contribution of the multiple-boundary geometry beyond the single-bisection lower bound.

### 5.3 Companion Computation Script

All Monte Carlo figures cited in Tables 2, 5, and 7 are reproducible from a single Python script published alongside this paper at:

> `https://github.com/spectralbranding/sbt-papers/tree/main/r3-cohort-boundaries/code/r3_concentration_mc.py`

The script draws Dirichlet samples, runs $k$-means at $k = 4$, computes Euclidean and Fisher-Rao distance statistics, and reports the boundary volume fractions under both metrics. Random seed is fixed at 42; trial counts and sample sizes are documented in the script header. Running the script with `uv run --with numpy --with scikit-learn python r3_concentration_mc.py` reproduces the cited figures within the reported standard errors. A README in the same directory documents installation and provenance.

---

## 6. Implications for Spectral Brand Theory

### 6.1 Why Cohort Count Is Resolution-Dependent

The central insight of this paper -- that at least 52.2% of $\Delta^7$ lies within 10% of any partition boundary -- has an immediate consequence for the empirical determination of cohort count. Different clustering algorithms, different distance thresholds, or different initializations will produce different $k$ values not because some are "right" and others "wrong," but because the geometry of $\Delta^7$ does not support sharp partition boundaries at $n = 8$.

The standard "elbow method" for selecting $k$ in $k$-means clustering seeks the value where the within-cluster sum of squares (WCSS) shows a sharp decrease. On $\Delta^7$, the concentration of distances means that the WCSS curve is smooth rather than kinked: the improvement from $k = 3$ to $k = 4$ is similar in magnitude to the improvement from $k = 5$ to $k = 6$, making the elbow ambiguous. The silhouette score, which measures how well-separated clusters are, is systematically depressed in high dimensions because the mean inter-cluster distance is not much larger than the mean intra-cluster distance (a direct consequence of Theorem 1).

This provides a formal explanation for the observation that motivated this paper: Claude's identification of 5--6 cohorts and Gemini's identification of 3 cohorts for the same five case-study brands. Both models were applying implicit clustering to the same observer weight space, but with different internal thresholds for what constitutes a "distinct" cluster. The theorem provides the geometric rationale; the 5-brand exercise illustrates the phenomenon. The quantitative bound applies to large populations of observer profiles; the five brands are a motivating illustration, not a population. Theorem 2 guarantees that both interpretations are consistent with the geometry -- neither is more "correct" than the other in any objective sense.

### 6.2 Cross-Model Agreement as Evidence

The cross-model replication study in Zharnikov (2026a) found that two independent AI systems produced identical coherence grades (5/5 match) but different cohort granularities. From the perspective of the present paper, this pattern is precisely what the mathematics predicts:

1. **Coherence grades are robust** because they depend on the global structure of the brand's spectral profile (the relative magnitudes and coherence across all eight dimensions), which is a low-dimensional summary that is not sensitive to observer-space partitioning.

2. **Cohort counts are fragile** because they depend on the fine structure of the observer weight space, where concentration of measure makes boundaries fuzzy and the number of "natural" clusters ill-defined.

This dissociation between robust grade assignment and fragile cohort counting is not a flaw in SBT but a prediction of the theory's mathematical foundations. Zharnikov (2026e) proved that the projection from 8-dimensional spectral profiles to 1-dimensional coherence grades is necessarily lossy (the "metamerism" result), but the grades are a stable summary statistic. Cohort structure, by contrast, lives in the full 8-dimensional space where concentration effects dominate.

### 6.3 D/A Ratio and Cohort Sharpness

SBT's designed/ambient (D/A) ratio measures the fraction of a brand's signals that are intentionally designed versus those that arise from ambient, uncontrolled processes. The Goldilocks zone for D/A is 55--65% designed (Zharnikov, 2026a). We can now provide a geometric interpretation of how D/A affects cohort structure.

Designed signals, by definition, are controlled and consistent. When a brand has a high D/A ratio, the signals received by different observers are more similar, which means the *brand emission profile* has lower variance across encounter contexts. This, in turn, means that the *observer weight profiles* that are relevant to perceiving this brand are more tightly constrained: observers whose weights align with the brand's designed dimensions will form tighter clusters in $\Delta^7$, while those whose weights are orthogonal to the designed dimensions will consistently perceive the brand as weak.

Formally, let $\sigma^2_D$ and $\sigma^2_A$ denote the variance of designed and ambient signal components, respectively, with $\sigma^2_A > \sigma^2_D$ (ambient signals are more variable by definition). The effective variance of the observer-profile cloud associated with a given cohort is:

$$\sigma^2_{\text{eff}} \approx \frac{D}{D+A} \cdot \sigma^2_D + \frac{A}{D+A} \cdot \sigma^2_A$$

A higher D/A ratio shifts weight toward the lower-variance designed component, reducing $\sigma^2_{\text{eff}}$ and thereby compressing the cohort in $\Delta^7$. Compressed cohorts have smaller effective radii, which means a larger fraction of their volume lies in the interior rather than the boundary zone. The boundary volume fraction for a cohort of effective radius $r$ scales as $1 - (1 - \delta/r)^n$, so smaller $r$ (sharper cohort) means less boundary volume at fixed absolute $\delta$.

This explains Hermès's (A+, high D/A) sharp cohort structure versus Tesla's (C-, volatile D/A) diffuse cohort structure: Hermès's designed-dominant signal environment compresses observer cohorts, while Tesla's ambient-heavy, controversy-driven signal environment inflates them. The mechanism by which coherence type mediates this compressive effect — through the non-ergodic resilience dynamics — is formally derived in Zharnikov (2026s).

### 6.4 From Categorical Segments to Continuous Profiles

The boundary fuzziness result (Theorem 2) provides mathematical grounding for a methodological prescription: the traditional practice of assigning each observer to a single discrete cohort is geometrically lossy in 8 dimensions, where at least 52% of observers sit near a boundary. Any discrete assignment throws away the information about *how close* the observer is to the boundary and *which* adjacent cohort they are nearest to.

This connects to a broader distinction between what we may term the "rasterized" and "vectorized" approaches to brand management. In the rasterized approach, observer profiles are projected onto a discrete grid of cohorts: "this observer is in Cohort A." This is the marketing industry's standard practice — the foundation of latent-class and mixture-model segmentation as canonically reviewed in Wedel and Kamakura (2000) — inherited from the era of two-dimensional perceptual maps where the approach was geometrically sound (at $n = 2$, only 10% of the space is boundary at $\delta = .10$). The information lost by rasterization in 8 dimensions is the direct analogue of the metamerism bound derived in Zharnikov (2026e): just as projecting from 8 dimensions to fewer collapses distinct spectral profiles into indistinguishable ones, projecting from continuous $\Delta^7$ to discrete cohort labels collapses a majority of the population's nuanced position information. In the vectorized approach, the full continuous observer profile $w \in \Delta^7$ is retained, and all computations — distance to brand, cohort proximity, predicted response to repositioning — are performed on the continuous representation. The formal bound applies to convex partitions; AI implicit clustering is assumed to approximate convex behaviour for the purposes of this argument.

Concentration of measure explains why the rasterized approach works tolerably in low-dimensional settings but fails systematically in higher dimensions. At intrinsic dimension 1 (e.g., quality-tier segmentation on $\Delta^1$), assigning an observer to a discrete segment loses information about at most 10% of the population -- the boundary dwellers. At intrinsic dimension 7 (the eight-component construction on $\Delta^7$), the same assignment loses information about at least 52% -- a majority. The geometric foundation of segmentation practice erodes as the dimensionality of the perception space increases, and the eight-dimensional setting places us firmly in the regime where the erosion is substantial.

The vectorized approach avoids this loss entirely by never projecting onto discrete categories. Rather than asking "which cohort does this observer belong to?", it asks "what is this observer's weight vector, and how does it relate to all other weight vectors?" The machinery of the Fisher-Rao metric (Zharnikov, 2026d) enables this: distances, means, geodesics, and clustering all operate on the continuous simplex without requiring discretization.

There is an instructive consequence for "brand alignment workshops" commonly used in consulting practice. In such workshops, stakeholders are asked whether they agree on the brand's identity, and high agreement is treated as evidence of brand coherence. To the extent that stakeholder perceptions can be modeled as weight profiles on $\Delta^7$ — a modeling assumption that separates mathematical claims (random simplex draws) from sociological ones (workshop agreement under social pressure or satisficing) — concentration of measure predicts that responses will naturally concentrate around their mean. Not because stakeholders genuinely agree, but because high-dimensional geometry compresses the distance between random points. The distance contrast ratio of 7.46 (Theorem 1) means that even "extreme" disagreements are only modestly larger than typical ones. Agreement that is geometrically trivial (a consequence of concentration) is indistinguishable, by the usual workshop methods, from agreement that is substantively meaningful (reflecting genuine alignment on the brand's designed emission vector).

The vectorized approach resolves this by computing alignment from the source vector -- the designed brand emission profile -- rather than from inter-stakeholder consensus. Alignment measured as $d_{FR}(w_{\text{observed}}, w_{\text{designed}})$, the Fisher-Rao distance between an observer's perceived profile and the brand's intended profile, produces a measure of coherence that is genuinely discriminating rather than trivially concentrated. This is because the source vector anchors the measurement to a fixed point in the space, breaking the symmetry that produces trivial concentration among random points.

### 6.5 Capacity-Resolution Duality

The contrast ratio $R_8 = 7.46$ (Theorem 1) and the boundary volume fraction $\text{BVF}(8, .10) \geq 52.2\%$ (Theorem 2) are not only properties of the observer weight space — they directly bound the number of *distinguishable* perceptual cohorts that $\Delta^7$ can support. This connects R3's resolution results to the capacity question posed in Zharnikov (2026g): how many distinct brand positions can the observer simplex simultaneously resolve?

In the brand signal space $\mathcal{B}$, the sphere-packing problem bounds how many non-overlapping brand spectral profiles can be placed so that each is distinguishable from all others (Zharnikov 2026g; Conway and Sloane 1999). The dual question in the observer weight space $\mathcal{O}$ is: given that distances concentrate (Theorem 1) and boundaries are wide (Theorem 2), how many cohorts can be simultaneously distinguished? The answer is tightly constrained. If boundary zones at $\delta = .10$ consume at least 52% of the volume, at most 48% of the simplex mass remains in "crisp interior" regions across all $k$ cohorts. As $k$ increases, each cohort's interior fraction shrinks proportionally; for $k \geq 6$ convex cohorts, the boundary zones of adjacent cohorts begin to overlap, meaning that a positive fraction of observers falls simultaneously near two or more boundaries and cannot be unambiguously assigned. The Beyer et al. (1999) distance contrast result provides the threshold: when $R_n$ approaches 1, no distance-based partition is meaningful.

Together, Theorems 1 and 2 define a *capacity-resolution trade-off* in $\mathcal{O}$: finer resolution (larger $k$) reduces per-cohort interior volume, while distance concentration caps the total number of distinguishable cohort positions. R4's packing bound in $\mathcal{B}$ and R3's volume bound in $\mathcal{O}$ are therefore dual constraints on the same question: what is the maximum information that the SBT framework can simultaneously encode about a population of observers? Capacity in $\mathcal{B}$ bounds how many brands can be distinguished; resolution in $\mathcal{O}$ bounds how finely observers can be partitioned.

---

## 7. Connection to Non-Ergodic Dynamics

The concentration of measure results derived above characterize the *static* geometry of $\Delta^7$ -- what the space looks like at a single moment. SBT, however, posits that observer profiles evolve over time as observers encounter brand signals, update their priors, and experience signal decay and crystallization (Zharnikov, 2026a). The temporal dynamics introduce non-ergodicity: the trajectory of an individual observer's weight profile through $\Delta^7$ does not, in general, visit all regions of the simplex, because absorbing states and crystallized priors create barriers to exploration.

Peters (2019) formalized the distinction between ergodic and non-ergodic dynamics in economics, showing that ensemble averages (averages across a population at one time) and time averages (averages along one agent's trajectory over time) diverge when the dynamics are multiplicative or contain absorbing states. Zharnikov (2026a) applied this insight to brand perception: the average perception of a brand across all current observers (the "brand image" in marketing terminology) may differ systematically from any individual observer's evolving perception over time.

The present paper's concentration-of-measure results interact with non-ergodic dynamics in two important ways.

First, **boundary fuzziness amplifies non-ergodic effects**. Since at least 52% of observer profiles lie near a cohort boundary (Theorem 2), a small perturbation in an observer's weight profile -- caused by a single brand signal encounter -- can shift the observer from one cohort to another. In ergodic dynamics, such shifts would average out over time: an observer who occasionally crosses a boundary would, on average, spend equal time in each adjacent cohort. In non-ergodic dynamics, a single boundary-crossing event can trigger a cascade (through updated priors and changed attention allocation) that keeps the observer in the new cohort permanently. The wide boundary zone means that many observers are perpetually "at risk" of such irreversible transitions.

Second, **absorbing states on $S^7_+$ prevent the mixing that concentration predicts**. Lévy's lemma (Proposition 1) implies that 1-Lipschitz functions on $S^7$ are approximately constant -- their values concentrate near the median. This would predict that brand perception, modeled as a Lipschitz function of observer position, should be approximately uniform across the observer population. Empirically, it is not: different observers perceive the same brand very differently, and these differences persist over time. The resolution is that SBT's absorbing states (negative conviction, crystallized priors) restrict the dynamics to subsets of $S^7_+$, breaking the conditions under which Levy's lemma applies. The effective state space is not the full simplex but a collection of disconnected or poorly connected components separated by absorbing barriers.

Hegselmann and Krause (2002) studied a related phenomenon in their bounded-confidence opinion dynamics model: when agents update their opinions only based on nearby agents (within a confidence threshold), the population fragments into disconnected clusters even though the underlying space is connected. The SBT mechanism is similar but richer: rather than a fixed confidence threshold, the effective connectivity of $\Delta^7$ depends on the history of signal encounters and the resulting crystallized priors.

The full formalization of these dynamics requires the diffusion-on-manifolds framework developed in Zharnikov (2026j), which resolves the open problem posed in Zharnikov (2026c); the static geometric results of the present paper provide the necessary foundation: the shape of the space, the width of the boundaries, and the degree of concentration establish the geometric arena in which the dynamics play out.

---

## 8. Boundary Fuzziness Under Concentrated Distributions

The preceding analysis rests on the Dirichlet$(1, \ldots, 1)$ (uniform) null model for observer weight profiles. This section replaces the uniform assumption with the symmetric concentrated Dirichlet$(\alpha, \ldots, \alpha)$ family for $\alpha > 1$, derives how boundary volume fractions depend on $\alpha$, and argues that the uniform case is the *worst case* -- the conservative upper bound -- on boundary fuzziness for real observer populations.

### 8.1 Concentrated Dirichlet Distributions

For $X = (X_1, \ldots, X_n) \sim \text{Dir}(\alpha, \ldots, \alpha)$ with $\alpha > 1$, the density on $\Delta^{n-1}$ is proportional to $\prod_{i=1}^n x_i^{\alpha - 1}$. The marginal moments are:

$$E[X_i] = \frac{1}{n}, \qquad \text{Var}[X_i] = \frac{(1/n)(1 - 1/n)}{n\alpha + 1}$$

As $\alpha$ increases from 1, the variance of each component decreases proportionally to $1/(n\alpha)$, and the mass of the distribution concentrates around the centroid $c = (1/n, \ldots, 1/n)$. The effective diameter of the distribution -- the typical spread of observer profiles -- scales as:

$$d_{\text{eff}}(\alpha) \sim \frac{1}{\sqrt{\alpha}}$$

This scaling follows from the fact that the standard deviation of each component is $O(1/\sqrt{n\alpha})$, and the Euclidean distance from a random draw to the centroid is $O(\sqrt{n} \cdot 1/\sqrt{n\alpha}) = O(1/\sqrt{\alpha})$. Frigyik, Kapila, and Gupta (2010) establish precise concentration results for the Dirichlet family, confirming this scaling.

**Interpretation for SBT.** At $\alpha = 1$ (uniform), observer profiles spread broadly across $\Delta^7$, visiting all corners and faces of the simplex with positive probability. At $\alpha = 5$ (moderately concentrated), profiles cluster near the centroid: observers have broadly similar dimensional weightings with moderate variation. At $\alpha = 20$ (highly concentrated), profiles are tightly bunched near $(1/8, \ldots, 1/8)$: essentially all observers weight all eight dimensions approximately equally, differing only in fine perturbations around the equal-weight point. The concentrated regime corresponds empirically to audiences for brands with extremely broad cross-dimensional appeal -- or to experimental populations that have been pre-screened for uniformity of taste.

### 8.2 Boundary Volume Fraction Under Dirichlet$(\alpha)$

The key effect of concentration is to reduce the effective volume of $\Delta^7$ available for observers to inhabit. Under Dirichlet$(\alpha)$, only the region within $d_{\text{eff}}(\alpha) \sim 1/\sqrt{\alpha}$ of the centroid has substantial probability mass. Cohort boundaries that cut through the tails of the distribution (the periphery of the simplex) are therefore largely irrelevant: very few observers reside there.

**Proposition 3** (Boundary volume fraction under Dirichlet$(\alpha)$). *Let observer weights be drawn from $\text{Dir}(\alpha, \ldots, \alpha)$ on $\Delta^{n-1}$. Under the concentrated distribution, the effective boundary volume fraction satisfies:*

$$V_{\text{boundary}}(\alpha) \leq V_{\text{boundary}}(1) \cdot \left(\frac{1}{\alpha}\right)^{(n-1)/2}$$

*where $V_{\text{boundary}}(1)$ is the boundary volume fraction under the uniform (Dirichlet$(1,\ldots,1)$) distribution and $n = 8$.*

*Proof.* The boundary volume fraction under Dir$(\alpha)$ factors into (a) the geometric boundary width from Theorem 2, which depends only on the partition geometry, and (b) the probability mass of the distribution falling inside that fixed geometric zone, which depends on $\alpha$.

For (b), the symmetric Dirichlet$(\alpha,\ldots,\alpha)$ density on $\Delta^{n-1}$ is $f_\alpha(w) \propto \prod_{i=1}^n w_i^{\alpha-1}$, with normalizing constant $1/B(\alpha,\ldots,\alpha) = \Gamma(n\alpha)/\Gamma(\alpha)^n$. Stirling's approximation $\Gamma(z+1) \sim \sqrt{2\pi z}\,(z/e)^z$ applied to the ratio gives, for large $\alpha$:

$$\frac{\Gamma(n\alpha)}{\Gamma(\alpha)^n} \sim \frac{\sqrt{2\pi n\alpha}\,(n\alpha/e)^{n\alpha}}{[\sqrt{2\pi\alpha}\,(\alpha/e)^\alpha]^n} = \frac{n^{n\alpha} \cdot \sqrt{n}}{(2\pi\alpha)^{(n-1)/2}}$$

The density at the centroid $c = (1/n,\ldots,1/n)$ is therefore $f_\alpha(c) = (1/n)^{n(\alpha-1)} \cdot \Gamma(n\alpha)/\Gamma(\alpha)^n \sim n^{n} \sqrt{n}\,(2\pi\alpha)^{-(n-1)/2}$, which scales as $\alpha^{-(n-1)/2}$ at large $\alpha$ relative to $\alpha = 1$.

Equivalently, by Proposition 2 with general $\alpha$, the marginal variance is $\text{Var}[X_i] = (1/n)(1-1/n)/(n\alpha+1)$, so the standard deviation along each component scales as $(n\alpha)^{-1/2} \propto \alpha^{-1/2}$. The simplex has intrinsic dimension $n-1$ (Section 4.2), so the standard deviation contracts in each of the $n-1$ orthogonal directions on $\Delta^{n-1}$. Because the density $f_\alpha$ is log-concave for $\alpha \geq 1$, the Brunn-Minkowski inequality on convex bodies (Schneider 2014, Theorem 7.1.1) implies that the probability mass of any fixed convex zone -- in particular the boundary zone of width $\delta$ from Theorem 2 -- contracts by the product of the $(n-1)$ contraction factors:

$$P_{\alpha}(\text{boundary zone}) \leq P_{\alpha=1}(\text{boundary zone}) \cdot \prod_{i=1}^{n-1} \alpha^{-1/2} = V_{\text{boundary}}(1) \cdot \alpha^{-(n-1)/2}$$

For $n = 8$ this gives $\alpha^{-7/2} = \alpha^{-3.5}$. Frigyik, Kapila, and Gupta (2010, Section 3.4) establish the corresponding Dirichlet concentration scaling directly via moment-matching with the Gaussian on the ilr-transformed simplex. $\square$

*Falsification*: Proposition 3 is falsified if, for any $\alpha > 1$, Monte Carlo simulation of observer profiles from Dir$(\alpha,\ldots,\alpha)$ at $n = 8$ shows boundary volume fractions that *exceed* $V_{\text{boundary}}(1) \cdot \alpha^{-3.5}$ — i.e., concentration fails to reduce boundary fractions at the rate $(1/\alpha)^{3.5}$.

### 8.3 Numerical Values at $n = 8$

At $n = 8$, the exponent is $(n-1)/2 = 7/2 = 3.5$. The concentration factor at representative values of $\alpha$ is:

**Table 6: Dirichlet Concentration Effect on Boundary Volume Fraction at $n = 8$, $\delta = .10$.**

| $\alpha$ | $(1/\alpha)^{3.5}$ | $V_{\text{boundary}}(\alpha) \leq$ (at $\delta = .10$) | Interpretation |
|---|---|---|---|
| 1 | 1.0000 | 52.2% | Uniform: worst case |
| 3 | .0214 | 1.12% | Mild concentration |
| 5 | $3.58 \times 10^{-3}$ | .187% | Moderate concentration |
| 10 | $3.16 \times 10^{-4}$ | .0165% | Strong concentration |
| 20 | $2.80 \times 10^{-5}$ | .00146% | Near-crisp boundaries |

*Notes*: $V_{\text{boundary}}(\alpha) \leq V_{\text{boundary}}(1) \cdot (1/\alpha)^{(n-1)/2}$ where $V_{\text{boundary}}(1) = .522$ and $(n-1)/2 = 3.5$ at $n = 8$. Empirical $\alpha$ range for behavioral weight distributions: $[3, 10]$ (Frigyik et al. 2010; Aitchison 1986).

At $\alpha = 5$ (moderately concentrated), the boundary volume fraction falls below 0.2% -- boundaries are effectively crisp relative to the distribution. At $\alpha = 20$ (highly concentrated), boundaries are essentially meaningless: essentially all observers cluster so tightly around the centroid that any reasonable partition places them in a single cohort with overwhelming probability.

The monotone decrease in $V_{\text{boundary}}(\alpha)$ with $\alpha$ establishes a continuous spectrum:

$$\underbrace{\alpha = 1}_{\text{uniform}} \longrightarrow \underbrace{\alpha \in [3, 10]}_{\text{real populations}} \longrightarrow \underbrace{\alpha \to \infty}_{\text{point mass}}$$

At the left extreme lies the uniform null model -- the result of Theorem 2 applies directly, and at least 52% of observers are in the boundary zone. At the right extreme lies a point mass at the centroid -- there is only one "cohort" (all observers are identical) and the notion of boundaries is vacuous. Real observer populations occupy the intermediate regime.

### 8.4 Empirical Range of $\alpha$ and Implications

Empirical estimates of Dirichlet concentration parameters for behavioral weight distributions in adjacent domains (attention allocation, portfolio choice, stated preference studies) typically fall in the range $\alpha \in [3, 10]$ (Frigyik et al., 2010; Aitchison, 1986). At $\alpha = 3$, the concentration factor is approximately $0.0214$, reducing the worst-case boundary fraction from 52.2% to roughly 1.1%. At $\alpha = 10$, it falls to under 0.02%.

This has a critical implication for the interpretation of Theorem 2 and Corollary 1. Those results establish a *lower bound* on boundary volume fraction under the uniform model -- the hardest case for boundary clarity. For real populations with $\alpha \geq 3$, the actual boundary fraction is roughly two orders of magnitude smaller. The uniform model is the most conservative assumption.

**Corollary 2** (Uniform distribution is the worst case). *For fixed partition geometry, the boundary volume fraction $V_{\text{boundary}}(\alpha)$ is a strictly decreasing function of $\alpha$. The uniform distribution ($\alpha = 1$) maximizes boundary volume fraction. Therefore, the results of Theorem 2 and Corollary 1 constitute a conservative upper bound on boundary fuzziness: real observer populations with any clustering tendency ($\alpha > 1$) have strictly sharper cohort boundaries than the uniform bound predicts.*

*Falsification*: Corollary 2 is falsified if, for some $\alpha_1 > \alpha_2 \geq 1$, a Monte Carlo study demonstrates that $V_{\text{boundary}}(\alpha_1) \geq V_{\text{boundary}}(\alpha_2)$ — i.e., more concentrated distributions do not have smaller boundary fractions.

This corollary strengthens the overall argument of this paper. The claim that cohort membership is "necessarily fuzzy" applies in its strongest form only at the uniform extreme. As soon as observers show any tendency to cluster in weight space -- which empirical evidence suggests they do -- boundaries become sharper. The practical implication is that while the *geometry* of $\Delta^7$ forces fuzziness at $\alpha = 1$, real survey or behavioral data with estimated $\alpha$ in the range $[3, 10]$ will exhibit boundary fractions in the range 0.02--3.7%, which are operationally negligible.

The spectrum from fuzzy (uniform) to crisp (point mass) should therefore be read as a *calibration* result: the uniform model sets the theoretical maximum for boundary ambiguity, and any empirical estimate of $\alpha$ from actual data immediately sharpens that bound. SBT's recommendation to use continuous observer profiles (Section 6.4) remains correct because the simplex geometry is the foundation, but the severity of the fuzziness problem depends on the empirical $\alpha$ of the observed population.

---

## 9. Limitations and Extensions

Several limitations of the present analysis should be noted.

**Uniform distribution assumption.** The null model throughout this paper is the uniform (Dirichlet$(1, \ldots, 1)$) distribution on $\Delta^7$. Real observer populations are unlikely to be uniformly distributed -- some dimensional weightings are empirically more common than others. Section 8 shows that switching to the symmetric concentrated model Dirichlet$(\alpha, \ldots, \alpha)$ with $\alpha > 1$ reduces the boundary volume fraction by a factor of $\alpha^{-(n-1)/2}$, and that the uniform model is the worst case. However, that analysis still assumes *symmetric* concentration: the same $\alpha$ governs every dimension. In practice, populations may exhibit *heterogeneous* concentration, with dimension-specific parameters $\alpha_i$ that differ across the eight SBT dimensions. For example, observers in a fashion-forward market may be tightly concentrated on the Semiotic dimension ($\alpha_{\text{sem}}$ large) while remaining diffuse on the Economic dimension ($\alpha_{\text{econ}}$ near 1). The asymmetric Dirichlet$(\alpha_1, \ldots, \alpha_8)$ model captures this, but the boundary volume fraction scaling derived in Proposition 3 no longer applies directly: each dimension contributes a distinct contraction factor $\alpha_i^{-1/2}$, and the effective contraction depends on the geometric mean $(\prod_{i=1}^8 \alpha_i)^{1/16}$ rather than a single $\alpha$. Extending the analysis to the full asymmetric Dirichlet family, and estimating dimension-specific $\alpha_i$ from behavioral data, is an important direction. Conversely, if the distribution is sparse ($\alpha < 1$, concentrating near vertices), the effective dimensionality is also reduced but in a different geometry; this case, which corresponds to highly specialised observer populations, is left for future work.

**Euclidean versus Fisher-Rao distances.** The Monte Carlo simulations and distance contrast computations use Euclidean distances on $\Delta^7$, while SBT's formal metric is Fisher-Rao (Zharnikov, 2026d). The Fisher-Rao metric, via the square-root transform, is isometric to geodesic distance on $S^7_+$, so the Lévy concentration results (Proposition 1) apply directly. However, the Euclidean and Fisher-Rao distances on $\Delta^7$ are not identical (they differ by a nonlinear transformation), and the distance contrast ratios in Theorem 1 should be recalculated in the Fisher-Rao metric for maximum precision. We expect the qualitative conclusions to be unchanged because the square-root map is a diffeomorphism that preserves the topological structure.

**Convexity of cohort regions.** Theorem 2 assumes convex cohort regions, which is satisfied by $k$-means (which produces Voronoi cells) and Gaussian mixture models (which produce approximately convex regions for well-separated components). Density-based clustering methods (DBSCAN, HDBSCAN) can produce non-convex regions, for which the bound may not hold in its current form. The extension to non-convex partitions via the Minkowski content is possible but requires additional technical machinery. Subspace clustering methods (Kriegel, Kröger, and Zimek 2009) partially mitigate high-dimensional concentration by restricting distances to low-dimensional subspaces; however, they require prior knowledge of the relevant subspace, which is unavailable in SBT where all eight dimensions are theoretically justified.

**Independence of dimensions.** The Dirichlet distribution imposes a specific covariance structure (negative correlations due to the sum-to-one constraint) but does not model dimension-specific correlations that may exist empirically. For example, observers who weight the Ideological dimension highly may systematically also weight the Cultural dimension highly, creating positive correlations between specific dimension pairs that the Dirichlet model does not capture. Copula-based models on the simplex (Aitchison & Shen, 1980) could extend the analysis to incorporate such dependencies. A related concern is raised by Garner's (1974) distinction between integral and separable dimensions: if two or more of the eight SBT dimensions are integral (perceived holistically rather than independently), the Euclidean and Fisher-Rao metric models would require adjustment — for instance, a Minkowski metric with exponent $r < 2$ — and the concentration bounds derived here would need to be revisited for the adjusted metric.

**Effective dimensionality.** SBT's eight dimensions are not necessarily independent axes of perception. If empirical observer profiles cluster along a lower-dimensional submanifold of $\Delta^7$, the effective dimensionality $d_{\text{eff}} < 8$ reduces concentration effects and may sharpen cohort boundaries. Estimating $d_{\text{eff}}$ from empirical data (e.g., via PCA on isometric log-ratio (ilr)-transformed observer profiles; Egozcue, Pawlowsky-Glahn, Mateu-Figueras, and Barceló-Vidal 2003) is an important empirical question that would refine the present theoretical bounds.

### 9.1 Empirical Estimation of $\alpha$

The practical value of Proposition 3 and Corollary 2 depends on empirically estimating the Dirichlet concentration parameter $\alpha$ from behavioral data on observer weight profiles. Two principal methods are available.

**Maximum likelihood estimation.** Given $m$ observed weight vectors $w^{(1)}, \ldots, w^{(m)} \in \Delta^7$ estimated from survey or choice data, the MLE of $\alpha$ under the symmetric Dir$(\alpha, \ldots, \alpha)$ model satisfies a fixed-point equation solvable by Newton's method (Frigyik, Kapila, and Gupta 2010). The sufficient statistic is the mean of $\log w_i$ across components and observations.

**Moment matching via ilr transformation.** An alternative is to apply the ilr transform (Egozcue et al. 2003) to map $\Delta^7$ to $\mathbb{R}^7$, fit a Gaussian model to the transformed data, and back-transform the variance parameter to an approximate Dirichlet $\alpha$. This is computationally simpler and robust to misspecification of the symmetric-$\alpha$ assumption (Aitchison 1986).

Empirical $\alpha$ values for behavioral weight distributions in adjacent domains typically fall in $[3, 10]$ (Frigyik et al. 2010; Aitchison 1986), though observer populations for narrow-audience luxury brands may show higher concentration. Applying either method to SBT survey data would immediately sharpen the Proposition 3 bound and calibrate the practical severity of the fuzziness result for specific brand-audience pairs.

**Extensions.** Three natural extensions suggest themselves: (1) concentration of measure on the *product* space $\mathcal{B} \times \mathcal{O}$ (the combined brand-observer space from Zharnikov, 2026d), which would characterize boundary fuzziness for joint brand-observer cohorts; (2) time-dependent concentration bounds for evolving observer profiles under SBT's signal dynamics, connecting to the non-ergodic results in Section 7; (3) empirical validation using survey data to estimate the actual distribution of observer profiles on $\Delta^7$ and test whether the Dirichlet null model is a reasonable approximation.

---

## 10. Conclusion

This paper has established that the fuzziness of perceptual cohort boundaries in Spectral Brand Theory is not a measurement artifact, an algorithmic limitation, or an empirical curiosity -- it is a geometric necessity under the uniform (Dirichlet-uniform) null model on $\Delta^7$. The concentration of measure phenomenon on the 8-dimensional probability simplex $\Delta^7$ ensures that:

1. Distances between random observer profiles concentrate around their mean (Theorem 1), with a contrast ratio of 7.46 at $n = 8$ -- sufficient for clustering to be meaningful but insufficient for boundaries to be sharp.

2. Any partition of $\Delta^7$ into convex cohort regions places at least 52% of the volume (at $\delta = 0.10$) in the boundary zone (Theorem 2), where cohort membership is ambiguous and sensitive to perturbation.

3. Lévy concentration on $S^7$ (Proposition 1) provides the analytical foundation: 1-Lipschitz functions deviate from their median by $\varepsilon$ or more with probability at most $4\exp(-7\varepsilon^2/8)$.

4. Cohort membership is necessarily dynamic and fuzzy (Corollary 1, under the uniform null model). The number of "natural" cohorts is a resolution parameter. Corollary 2 establishes the worst-case nature of the uniform bound: observer populations with any empirical clustering ($\alpha > 1$) have boundary fractions below 2% at $\alpha = 3$ — roughly two orders-of-magnitude improvement. Theorems 1 and 2 therefore serve as a geometric foundation; actual severity is calibrated by the empirical $\alpha$.

5. Taken together, the distance-concentration and boundary-fraction results define a capacity-resolution duality (Section 6.5): Theorem 1 bounds how many cohort positions are distinguishable in $\mathcal{O}$ and Zharnikov (2026g) bounds how many brand positions are distinguishable in $\mathcal{B}$, yielding dual constraints on what the SBT framework can simultaneously encode.

These results have practical consequences beyond SBT. Any brand management framework that relies on discrete consumer segmentation in a moderately high-dimensional perception space faces the same geometric constraints. The traditional rasterized approach systematically discards the nuanced positional information of the majority of observers at $n = 8$. The vectorized alternative — retaining continuous observer profiles and computing distances, means, and predictions on the simplex directly — is not merely a mathematical refinement but a geometrically necessary response to the structure of the space.

The results also contextualize the broader challenge of "big data" approaches to consumer understanding. Increasing the number of dimensions tracked (from 2 in traditional perceptual maps to 8 in SBT to potentially dozens in granular behavioral data) does not automatically improve segmentation quality. Beyond a dimension-specific threshold, adding dimensions makes segmentation worse by inflating the boundary volume fraction, a consequence of the curse of dimensionality that is well understood in machine learning but has not previously been connected to marketing practice.

Finally, the interaction between static concentration geometry and dynamic non-ergodic evolution (Section 7) opens a research frontier. The present paper establishes the shape of the geometric arena -- contrast ratio 7.46, boundary volume 52.2% at $\delta = .10$, $\alpha^{-7/2}$ sharpening under concentration; the dynamics within it -- diffusion, absorption, crystallization -- are the subject of future work.

---

## References

Aitchison, J. (1986). *The Statistical Analysis of Compositional Data*. Chapman and Hall.

Aitchison, J., & Shen, S. M. (1980). Logistic-normal distributions: Some properties and uses. *Biometrika*, 67(2), 261--272.

Amari, S., & Nagaoka, H. (2000). *Methods of Information Geometry*. American Mathematical Society.

Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages of careful seeding. *Proceedings of the 18th Annual ACM-SIAM Symposium on Discrete Algorithms*, 1027--1035.

Beyer, K., Goldstein, J., Ramakrishnan, R., & Shaft, U. (1999). When is "nearest neighbor" meaningful? *Proceedings of the 7th International Conference on Database Theory*, 217--235.

Bijmolt, T. H. A., & Wedel, M. (1999). A comparison of multidimensional scaling methods for perceptual mapping. *Journal of Marketing Research*, 36(2), 277--285. https://doi.org/10.2307/3151913

Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet allocation. *Journal of Machine Learning Research*, 3, 993--1022.

Boucheron, S., Lugosi, G., & Massart, P. (2013). *Concentration Inequalities: A Nonasymptotic Theory of Independence*. Oxford University Press.

Bronnenberg, B. J., Dubé, J.-P., & Gentzkow, M. (2016). Do online and offline markets differ? *Quantitative Marketing and Economics*, 14, 339--367. https://doi.org/10.1007/s11129-016-9171-8

Bühlmann, P., Kalisch, M., & Meier, L. (2014). High-dimensional statistics with a view toward applications in biology. *Annual Review of Statistics and Its Application*, 1, 255--278. https://doi.org/10.1146/annurev-statistics-022513-115545

Campbell, L. L. (1986). An extended Cencov characterization of the information metric. *Proceedings of the American Mathematical Society*, 98(1), 135--141.

Carroll, J. D., & Chang, J.-J. (1970). Analysis of individual differences in multidimensional scaling via an N-way generalization of "Eckart-Young" decomposition. *Psychometrika*, 35(3), 283--319.

Cencov, N. N. (1972). *Statistical Decision Rules and Optimal Inference*. Nauka (in Russian). English translation: *Translations of Mathematical Monographs*, Vol. 53. American Mathematical Society, 1981.

Conway, J. H., & Sloane, N. J. A. (1999). *Sphere Packings, Lattices and Groups* (3rd ed.). Springer.

DeSarbo, W. S., Kim, Y., Choi, S. C., & Spaulding, M. (2002). A gravity-based multidimensional scaling model for deriving spatial structures underlying consumer preference/choice judgments. *Journal of Consumer Research*, 29(1), 91--100.

Donoho, D. L., & Tanner, J. (2009). Observed universality of phase transitions in high-dimensional geometry, with implications for modern data analysis and signal processing. *Philosophical Transactions of the Royal Society A*, 367(1906), 4273--4293. https://doi.org/10.1098/rsta.2009.0152

Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. (2003). Isometric logratio transformations for compositional data analysis. *Mathematical Geology*, 35(3), 279--300.

Evgeniou, T., Boussios, C., & Zacharia, G. (2005). Generalized robust conjoint estimation. *Marketing Science*, 24(3), 415--429. https://doi.org/10.1287/mksc.1040.0102

Frigyik, B. A., Kapila, A., & Gupta, M. R. (2010). Introduction to the Dirichlet distribution and related processes. *UWEETR-2010-0006, Department of Electrical Engineering, University of Washington*.

Garner, W. R. (1974). *The Processing of Information and Structure*. Lawrence Erlbaum.

Giraud, C. (2014). *Introduction to High-Dimensional Statistics*. Chapman and Hall/CRC.

Gorban, A. N., & Tyukin, I. Y. (2018). Blessing of dimensionality: Mathematical foundations and connections to machine learning. *Philosophical Transactions of the Royal Society A*, 376(2118), 20170237.

Gromov, M., & Milman, V. D. (1983). A topological application of the isoperimetric inequality. *American Journal of Mathematics*, 105(4), 843--854.

Hegselmann, R., & Krause, U. (2002). Opinion dynamics and bounded confidence: Models, analysis and simulation. *Journal of Artificial Societies and Social Simulation*, 5(3), 2.

Johnson, N. L., & Kotz, S. (1972). *Distributions in Statistics: Continuous Multivariate Distributions*. Wiley.

Kapferer, J.-N. (2008). *The New Strategic Brand Management: Creating and Sustaining Brand Equity Long Term* (4th ed.). Kogan Page.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1--22.

Kriegel, H.-P., Kröger, P., & Zimek, A. (2009). Clustering high-dimensional data: A survey on subspace clustering, pattern-based clustering, and correlation clustering. *ACM SIGKDD Explorations Newsletter*, 11(1), 56--78.

Lancaster, K. J. (1966). A new approach to consumer theory. *Journal of Political Economy*, 74(2), 132--157.

Ledoux, M. (2001). *The Concentration of Measure Phenomenon*. American Mathematical Society.

Lévy, P. (1951). *Problèmes concrets d'analyse fonctionnelle*. Gauthier-Villars.

Milman, V. D. (1971). A new proof of A. Dvoretzky's theorem on cross-sections of convex bodies. *Functional Analysis and Its Applications*, 5(4), 288--295.

Milman, V. D., & Schechtman, G. (1986). *Asymptotic Theory of Finite Dimensional Normed Spaces*. Lecture Notes in Mathematics, Vol. 1200. Springer.

Molenaar, P. C. M. (2004). A manifesto on psychology as idiographic science: Bringing the person back into scientific psychology, this time forever. *Measurement*, 2(4), 201--218.

Netzer, O., Feldman, R., Goldenberg, J., & Fresko, M. (2012). Mine your own business: Market-structure surveillance through text mining. *Marketing Science*, 31(3), 521--543. https://doi.org/10.1287/mksc.1120.0713

Pawlowsky-Glahn, V., Egozcue, J. J., & Tolosana-Delgado, R. (2015). *Modeling and Analysis of Compositional Data*. Wiley.

Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, 15, 1216--1221.

Rossi, P. E., & Allenby, G. M. (2003). Bayesian statistics and marketing. *Marketing Science*, 22(3), 304--328. https://doi.org/10.1287/mksc.22.3.304.17739

Schneider, R. (2014). *Convex Bodies: The Brunn-Minkowski Theory* (2nd expanded ed.). Encyclopedia of Mathematics and its Applications, Vol. 151. Cambridge University Press.

Smith, W. R. (1956). Product differentiation and market segmentation as alternative marketing strategies. *Journal of Marketing*, 21(1), 3--8.

Talagrand, M. (1995). Concentration of measure and isoperimetric inequalities in product spaces. *Publications Mathématiques de l'IHÉS*, 81, 73--205.

Todd, J. T., Oomes, A. H. J., Koenderink, J. J., & Kappers, A. M. L. (2001). On the affine structure of perceptual space. *Psychological Science*, 12(3), 191--196.

Vershynin, R. (2018). *High-Dimensional Probability: An Introduction with Applications in Data Science*. Cambridge University Press.

Wainwright, M. J. (2019). *High-Dimensional Statistics: A Non-Asymptotic Viewpoint*. Cambridge University Press.

Wedel, M., & Kamakura, W. A. (2000). *Market Segmentation: Conceptual and Methodological Foundations* (2nd ed.). Kluwer Academic.

Wedel, M., & Kannan, P. K. (2016). Marketing analytics for data-rich environments. *Journal of Marketing*, 80(6), 97--121. https://doi.org/10.1509/jm.15.0413

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026b). The Atom-Cloud-Fact Epistemological Pipeline: From financial document processing to brand perception modeling. Working Paper. https://doi.org/10.5281/zenodo.18944770

Zharnikov, D. (2026c). Geometric approaches to brand perception: A critical survey and research agenda. Working Paper. https://doi.org/10.5281/zenodo.18945217

Zharnikov, D. (2026d). Brand space geometry: A formal metric for multi-dimensional brand perception. Working Paper. https://doi.org/10.5281/zenodo.18945295

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026g). How many brands can a market hold? Sphere packing bounds for multi-dimensional positioning. Working Paper. https://doi.org/10.5281/zenodo.18945522

Zharnikov, D. (2026i). The Organizational Schema Theory: Test-driven business design. Working Paper. https://doi.org/10.5281/zenodo.18946043

Zharnikov, D. (2026j). Non-ergodic brand perception: Diffusion dynamics on multi-dimensional perceptual manifolds. Working Paper. https://doi.org/10.5281/zenodo.18945659

Zharnikov, D. (2026r). Why eight? Completeness and necessity of the SBT dimensional taxonomy. Working Paper. https://doi.org/10.5281/zenodo.19207599

Zharnikov, D. (2026s). Coherence type as crisis predictor: A formal derivation from non-ergodic dynamics. Working Paper. https://doi.org/10.5281/zenodo.19208107

---

## Acknowledgments

AI assistants (Claude Opus 4.7, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.
