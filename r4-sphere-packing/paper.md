# How Many Brands Can a Market Hold? Sphere Packing Bounds for Multi-Dimensional Positioning

**Dmitry Zharnikov**

ORCID: 0009-0000-6893-9231

Working Paper v1.3.0 — May 2026

https://doi.org/10.5281/zenodo.18945522

---

## Abstract

How many distinguishable brand positions can a market sustain? We formalize brand perception as points in $\mathbb{R}^8_+$ under the Aitchison metric (Aitchison 1986; Egozcue et al. 2003), which is isometric to Euclidean distance on a 7-dimensional hyperplane after centered log-ratio transformation. Two brands are distinguishable if their distance exceeds perceptual threshold $\varepsilon$. The problem maps onto sphere packing. Because the $E_8$ lattice achieves the unique optimal packing in eight dimensions (Viazovska 2017), its density ($\pi^4/384 \approx .2537$) and kissing number (240) supply structural bounds. We derive five results: (1) volume-ratio capacity is at least $(1/\varepsilon)^8$, equaling $10^8$ positions at $\varepsilon = .10$; (2) each position has at most 240 nearest neighbors decomposing into 112 specialist (two-dimensional) and 128 generalist (eight-dimensional) vectors; (3) 10,000 brands occupy less than .01% of the unit 8-ball; (4) category saturation occurs near $(1/\varepsilon)^{d_\text{eff}}$; (5) average inter-dimension correlation $\rho = .3$ collapses effective dimensionality to approximately 2.6 and capacity by five orders of magnitude. An LLM stability experiment (250 calls, five models) finds null competitive-interference effects, consistent with fixed geometry. The $E_8$ connection is structural, not literal: it establishes the mathematical ceiling on positioning capacity. We discuss implications for white-space strategy, correlation management, and observer-dependent capacity.

**Keywords**: sphere packing, $E_8$ lattice, brand positioning, market capacity, kissing number, perceptual threshold, high-dimensional geometry, Spectral Brand Theory

**JEL Classification**: C65, M31, L11

**MSC Classification**: 52C17, 11H31, 91B42

---

## Positioning in High-Dimensional Space

The concept of "positioning" is among the most influential ideas in modern marketing. Since Ries and Trout (1981) argued that brands compete for distinct positions in the consumer's mind, the metaphor of a "positioning space" has become central to brand strategy. Building on Aaker's (1991, 1997) foundational frameworks for brand equity and brand personality, subsequent research has developed rich taxonomies of brand dimensions -- yet for all the geometric language, the actual geometry has never been formalized. No one has answered the most basic quantitative question the metaphor implies: *how many distinguishable positions does the space actually contain?*

Previous attempts to formalize brand positioning have been limited to low-dimensional settings. Hotelling (1929) places firms on a line. MDS in marketing (Green & Rao 1972; Bijmolt & Wedel 1999) typically produces 2- or 3-dimensional perceptual maps. Lancaster's (1966) characteristics space allows arbitrary dimensionality in principle but has not addressed the capacity question. Gardenfors (2000) provides a general theory of conceptual spaces but does not compute packing bounds. Cognitive science models of structured representation (Tenenbaum et al. 2011) show that human concept learning exploits the statistical structure of high-dimensional hypothesis spaces, motivating the question of how many distinct hypotheses -- and thus how many distinct brand positions -- a structured representational space can sustain.

Geometric approaches to brand perception have a long history (reviewed in Zharnikov 2026c), but none has derived capacity bounds. Spectral Brand Theory (Zharnikov 2026a) provides the framework that makes a formal treatment possible, modeling brands as emitters across eight typed dimensions perceived by observers on $\Delta^7$. Zharnikov (2026d) established the Aitchison metric on $\mathbb{R}^8_+$; Zharnikov (2026e) proved that projecting 8D profiles to scalar grades produces spectral metamerism; Zharnikov (2026f) showed that concentration of measure makes cohort boundaries inherently fuzzy.

This paper asks the next natural question: given the 8-dimensional brand space with a formal metric, *how many non-overlapping positions does it contain?* The mathematical tool is sphere packing theory. In eight dimensions, the densest possible packing is known exactly: Viazovska (2017) proved that the $E_8$ lattice is optimal, earning the Fields Medal in 2022. The $E_8$ lattice has a packing density of $\pi^4/384 \approx .2537$, a kissing number of 240, and deep connections to exceptional structures in mathematics -- properties that yield surprisingly concrete positioning bounds.

**Important caveat, stated at the outset.** The $E_8$ connection is *structural*, not *literal*. It provides the mathematical ceiling on packing efficiency, not a claim that brands arrange themselves as lattice points -- any more than hexagonal optimality in 2D claims oranges form perfect hexagons. Throughout, we maintain strict separation between proved mathematical results and interpretive application to branding.

Our main contributions are:

1. **Positioning capacity bounds** (Proposition 1): For perceptual threshold $\varepsilon$ on the unit 8-ball, the number of distinguishable positions is bounded below by $(1/\varepsilon)^8$, yielding $10^8$ positions at $\varepsilon = .10$.

2. **Local competition structure** (Proposition 2): The $E_8$ kissing number of 240 bounds the number of nearest-competitor positions, with a decomposition into specialist (112) and generalist (128) competitive vectors.

3. **White space abundance** (Proposition 3): Even with 10,000 brands at $\varepsilon = .10$, 99.99% of the positioning space remains unoccupied.

4. **Category saturation criterion** (Proposition 4): A product category is saturated when the number of brands approaches the packing capacity for that category's effective dimensionality.

5. **Correlation-induced capacity collapse** (Proposition 5): When SBT dimensions are correlated at average $\rho = .3$, effective dimensionality drops to approximately 2.6 and positioning capacity collapses from $10^8$ to approximately $10^3$.

The paper proceeds as follows. The Preliminaries section recalls the SBT framework and the formal metric. The Sphere Packing Fundamentals section develops the core mathematical apparatus. Positioning Capacity in 8 Dimensions derives the main capacity results. White Space and Market Saturation analyzes unoccupied positioning space. Effective Dimensionality and Correlation addresses correlation-induced capacity collapse. Why Eight Dimensions Is Special explores the exceptional mathematical properties of $E_8$. Applications and Examples develops category-level applications. Limitations and Caveats consolidates the paper's scope conditions. The Discussion connects findings to the broader research program. The Conclusion closes with implications for positioning strategy.

---

## Preliminaries

### SBT Framework Recap

Spectral Brand Theory (Zharnikov 2026a) models brand perception through an eight-dimensional signal architecture:

Table 1: SBT Eight Dimensions.

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

*Notes*: Dimension order is canonical (Zharnikov 2026a). Emission profiles are vectors in $\mathbb{R}^8_+$; observer weight profiles lie on $\Delta^7$.

A brand's **emission profile** (spectral profile) is a vector $s = (s_1, \ldots, s_8) \in \mathbb{R}^8_+$ representing signal strength across each dimension. An observer's **weight profile** is a vector $w = (w_1, \ldots, w_8) \in \Delta^7$ representing the relative salience of each dimension to that observer.

SBT distinguishes five coherence types -- ecosystem ($A+$), signal ($A-$), identity ($B+$), experiential asymmetry ($B-$), and incoherent ($C-$) -- assessed across five case-study brands: Hermès ($A+$), IKEA ($A-$), Patagonia ($B+$), Erewhon ($B-$), and Tesla ($C-$).

### Brand Space with the Aitchison Metric

Zharnikov (2026d) established the Aitchison metric on brand emission profiles:

$$d_{\mathcal{B}}(s_A, s_B) = \left\| \text{clr}(s_A) - \text{clr}(s_B) \right\|_2$$

where $\text{clr}_k(s) = \log(s_k / g(s))$ is the centered log-ratio transform and $g(s) = (\prod_{k=1}^8 s_k)^{1/8}$ is the geometric mean. This metric is justified by the ratio-based, compositional, and reference-invariant nature of brand perception (Aitchison 1986; Egozcue et al. 2003). The clr transform maps $\mathbb{R}^8_+$ isometrically to a 7-dimensional hyperplane in $\mathbb{R}^8$ where the Aitchison metric becomes standard Euclidean distance, allowing direct application of sphere packing results. Because the Aitchison metric makes the clr-transformed space isometric to a flat Euclidean hyperplane, the $E_8$ and sphere-packing results — which are established for Euclidean $\mathbb{R}^8$ — apply directly. An observer-weighted Fisher-Rao metric, if adopted, would introduce positive curvature and require spherical or hyperbolic packing bounds instead.

### The Perceptual Threshold

The *just-noticeable difference* (JND) concept from psychophysics (Weber 1834; Fechner 1860) provides the foundation for the perceptual threshold.

**Definition 1** (Distinguishability). *Two brands $A$ and $B$ are* distinguishable *if $d_{\mathcal{B}}(s_A, s_B) > \varepsilon$, where $\varepsilon$ is the perceptual threshold. They are* confusable *if $d_{\mathcal{B}}(s_A, s_B) \leq \varepsilon$.*

The threshold $\varepsilon$ is a parameter, not a constant -- it depends on observer expertise, dimensional salience, comparison context, and engagement level. We compute bounds for $\varepsilon = .05$ (expert observers), $\varepsilon = .10$ (attentive observers), and $\varepsilon = .20$ (casual observers). Empirical calibration is a direction for future work.

### From Distinguishability to Sphere Packing

If two brands must differ by at least $\varepsilon$ in Aitchison distance to be distinguishable, then each brand "occupies" a ball of radius $\varepsilon/2$ in the clr-transformed space. (If two brands both sit at the center of their respective balls, and the balls do not overlap, then their distance is at least $\varepsilon/2 + \varepsilon/2 = \varepsilon$, ensuring distinguishability.)

The maximum number of distinguishable brand positions is therefore bounded by the maximum number of non-overlapping balls of radius $\varepsilon/2$ that can be packed into the region of brand space. This is a sphere packing problem.

---

## Sphere Packing Fundamentals

### The Sphere Packing Problem

The sphere packing problem asks: what is the densest arrangement of non-overlapping spheres of a given radius in $n$-dimensional Euclidean space? The problem has been studied since at least Kepler's 1611 conjecture about optimal packing in three dimensions (proved by Hales 2005), and is one of the central problems in discrete geometry (Conway & Sloane 1999).

A **packing** $\mathcal{P}$ in $\mathbb{R}^n$ is a collection of non-overlapping balls of radius $r$. The **packing density** $\Delta$ is the fraction of space covered by the balls:

$$\Delta = \lim_{R \to \infty} \frac{\text{Volume of balls in } B(0, R)}{\text{Volume of } B(0, R)}$$

The **kissing number** $\tau(n)$ is the maximum number of non-overlapping unit spheres that can simultaneously touch a central unit sphere in $\mathbb{R}^n$.

### Volume of the $n$-Ball

The volume of the unit ball in $\mathbb{R}^n$ is

$$V_n(1) = \frac{\pi^{n/2}}{\Gamma(n/2 + 1)}$$

and the volume of a ball of radius $r$ is $V_n(r) = V_n(1) \cdot r^n$. The unit ball volume exhibits a striking non-monotone behavior:

Table 2: Unit Ball Volume $V_n(1)$ Across Selected Dimensions.

| $n$ | $V_n(1)$ |
|-----|----------|
| 1 | 2.000 |
| 2 | 3.142 |
| 3 | 4.189 |
| 4 | 4.935 |
| 5 | 5.264 (maximum) |
| 8 | **4.059** |
| 16 | .2353 |
| 24 | $1.930 \times 10^{-3}$ |
| 48 | $1.377 \times 10^{-12}$ |

*Notes*: Values computed via $V_n(1) = \pi^{n/2} / \Gamma(n/2 + 1)$. Volume peaks near $n = 5$ and declines rapidly thereafter, reflecting concentration of measure.

The unit ball volume peaks near $n = 5$ and then decreases rapidly. By $n = 8$, it has already dropped below its value at $n = 2$. This non-monotonicity is a manifestation of the concentration of measure phenomenon: in high dimensions, the volume of a ball is concentrated in a thin shell near its surface, and the "corners" of the enclosing cube contain almost all the volume.

For the positioning capacity problem, the relevant quantity is the ratio $V_n(1) / V_n(\varepsilon/2) = (2/\varepsilon)^n$, which grows exponentially with dimension. This ratio determines the maximum number of small balls that fit inside the unit ball.

### Packing Density Bounds

The packing density is bounded above and below by classical results. The linear programming (LP) bound framework of Cohn and Elkies (2003) provides the methodological foundation for both upper bounds and exact results: Viazovska's (2017) proof that $E_8$ is optimal builds directly on this framework by constructing a "magic function" certifying that no packing can exceed the $E_8$ density. The volume-ratio bound of Proposition 1 is structurally identical to Shannon's (1948) channel-capacity argument: the maximum number of distinguishable codewords in a channel with noise radius $\varepsilon$ equals the packing number of the signal space, establishing a formal equivalence between positioning capacity and communication channel capacity.

**Volume ratio bound (upper).** Any packing of balls of radius $r$ in the unit ball $B(0, 1)$ satisfies

$$N \leq \frac{V_n(1 + r)}{V_n(r)} = \left(\frac{1 + r}{r}\right)^n$$

because each ball must lie entirely within $B(0, 1 + r)$, and the balls are disjoint.

**Minkowski-Hlawka bound (lower).** There exist packings in $\mathbb{R}^n$ with density at least $\zeta(n) / 2^{n-1}$, where $\zeta(n)$ is the Riemann zeta function. This is a non-constructive existence result.

**Simple volume bound (lower).** The number of non-overlapping balls of radius $r$ in $B(0, 1)$ is at least

$$N \geq \frac{V_n(1)}{V_n(2r)} = \frac{1}{(2r)^n}$$

This follows by the standard packing-number argument: $N \cdot V_8(\varepsilon) \geq V_8(1)$, since if the $N$ expanded balls (each of radius $2r = \varepsilon$) failed to cover the unit ball, an additional center could be added, contradicting maximality. For our purposes with $r = \varepsilon/2$:

$$N \geq \frac{1}{\varepsilon^n}$$

### The Kissing Number Problem

The kissing number $\tau(n)$ is known exactly for only a few dimensions (Pfender & Ziegler 2004):

Table 3: Exact Kissing Numbers in Selected Dimensions.

| $n$ | $\tau(n)$ | Configuration |
|-----|-----------|---------------|
| 1 | 2 | Trivial |
| 2 | 6 | Hexagonal |
| 3 | 12 | Face-centered cubic |
| 4 | 24 | $D_4$ lattice |
| **8** | **240** | **$E_8$ lattice** |
| 24 | 196,560 | Leech lattice |

*Notes*: Kissing number is exact only in dimensions 1, 2, 3, 4, 8, and 24. In all other dimensions only bounds are known. Pfender & Ziegler 2004.

The kissing number is known exactly in only these dimensions plus $n = 1$. In all other dimensions, only bounds are known. The exactness in $n = 8$ and $n = 24$ is a consequence of the exceptional algebraic structures underlying the $E_8$ and Leech lattices.

---

## Positioning Capacity in 8 Dimensions

### Volume Ratio Bounds

We now apply the sphere packing framework to brand positioning in SBT's 8-dimensional space.

**Proposition 1** (Positioning capacity). *(Note: This argument is structurally the Hamming bound (Hamming 1950) applied geometrically rather than to a discrete alphabet.) For a perceptual threshold $\varepsilon > 0$ in the unit 8-ball of the clr-transformed brand space, the maximum number of distinguishable brand positions $N$ satisfies:*

$$\left(\frac{1}{\varepsilon}\right)^8 \leq N \leq \left(\frac{2 + \varepsilon}{\varepsilon}\right)^8$$

*In particular:*

Table 4: Positioning Capacity Bounds in the Unit 8-Ball by Perceptual Threshold.

| $\varepsilon$ | Lower bound | Upper bound |
|---------------|-------------|-------------|
| .05 | $2.56 \times 10^{10}$ | $7.98 \times 10^{12}$ |
| .10 | $1.00 \times 10^{8}$ | $3.78 \times 10^{10}$ |
| .15 | $3.90 \times 10^{6}$ | $1.78 \times 10^{9}$ |
| .20 | $3.91 \times 10^{5}$ | $2.14 \times 10^{8}$ |
| .30 | $1.52 \times 10^{4}$ | $1.19 \times 10^{7}$ |
| .50 | $2.56 \times 10^{2}$ | $3.91 \times 10^{5}$ |

*Notes*: Lower bound = $(1/\varepsilon)^8$; upper bound = $((2 + \varepsilon)/\varepsilon)^8$. $\varepsilon$ = perceptual threshold in Aitchison distance units.

*Proof.* The lower bound follows from the simple volume bound (derived in the Packing Density Bounds subsection above): $N \geq V_8(1) / V_8(\varepsilon) = (1/\varepsilon)^8$, where we note that $V_8(r) = V_8(1) \cdot r^8$ and the $V_8(1)$ factors cancel. The upper bound follows from the covering argument: each ball of radius $\varepsilon/2$ centered at a position within $B(0, 1)$ is contained in $B(0, 1 + \varepsilon/2)$, so $N \leq V_8(1 + \varepsilon/2) / V_8(\varepsilon/2) = ((2 + \varepsilon)/\varepsilon)^8$. $\square$

**Plain-English interpretation.** At a moderate perceptual threshold ($\varepsilon = .10$, meaning brands must differ by at least 10% of the space's diameter to be distinguishable), the 8-dimensional brand space can accommodate at least 100 million distinct positions. Even at a generous threshold ($\varepsilon = .20$), there are nearly 400,000 distinguishable positions. The "crowded market" complaint is, at least in principle, a failure to exploit available dimensionality.

*Falsification*: Proposition 1 is falsified if a set of more than $(2 + \varepsilon)^8 / \varepsilon^8$ mutually distinguishable brand profiles (verified by pairwise Aitchison distance $> \varepsilon$) can be identified in the clr-transformed unit 8-ball, or if fewer than $(1/\varepsilon)^8$ non-overlapping $\varepsilon$-balls fit in that space.

### The $E_8$ Lattice and Its Properties

The $E_8$ lattice is a remarkable mathematical object with connections to number theory, Lie algebras, string theory, and now -- we argue interpretively -- brand positioning theory. It can be defined as the set of points in $\mathbb{R}^8$ whose coordinates are either all integers or all half-integers (integers plus $1/2$), with the additional constraint that the coordinates sum to an even number.

Viazovska (2017) proved that the $E_8$ lattice achieves the densest possible sphere packing in $\mathbb{R}^8$:

$$\Delta_8 = \frac{\pi^4}{384} \approx .2537$$

This means that in the densest possible arrangement, spheres cover approximately 25.37% of 8-dimensional space. The remaining 74.63% is interstitial space -- gaps between the spheres.

The $E_8$ packing density provides a tighter estimate of positioning capacity than the simple volume bounds:

$$N_{E_8} = \Delta_8 \cdot \frac{V_8(R)}{V_8(\varepsilon/2)}$$

where $R$ is the radius of the region of interest. For the unit ball at $\varepsilon = .10$:

$$N_{E_8} \approx .2537 \times \frac{V_8(1)}{V_8(.05)} \approx 6.49 \times 10^{9}$$

This estimate treats the unit ball as if it were a large region of an infinite lattice; boundary effects may shift the estimate by $\sim\varepsilon$ relative to the exact finite-volume result (a 6–8% correction at $\varepsilon = .10$). This $E_8$-based estimate falls between the simple lower and upper bounds, as expected. It represents the capacity achievable by the optimal packing, which is tighter than the volume ratio upper bound but higher than the simple lower bound because the latter does not account for efficient packing arrangements.

### The Kissing Number: Specialist vs. Generalist Decomposition

**Interpretive note.** The result that follows establishes a precise mathematical property of the $E_8$ lattice in eight dimensions. It is important to read the competitive interpretation as structurally motivated analogy, not empirical claim: real brand competition is asymmetric, category-bounded, and observer-dependent in ways that no lattice model captures. The 112/128 decomposition and the 240 kissing number describe the geometry of the optimal packing arrangement, not regularities observed in markets.

**Proposition 2** (Local competition). *Each brand position in the $E_8$ lattice packing has exactly 240 nearest-neighbor positions -- the maximum possible in 8 dimensions. These 240 neighbors decompose into two structurally distinct classes:*

*(a) 112 "specialist" vectors of the form $(\pm 1, \pm 1, 0, 0, 0, 0, 0, 0)$ in all permutations of coordinates. These are concentrated on exactly 2 of the 8 dimensions.*

*(b) 128 "generalist" vectors of the form $(\pm 1/2, \pm 1/2, \pm 1/2, \pm 1/2, \pm 1/2, \pm 1/2, \pm 1/2, \pm 1/2)$ with an even number of minus signs. These are distributed across all 8 dimensions.*

*Proof.* The 240 minimal vectors of the $E_8$ lattice are well-known (Conway & Sloane 1999, Chapter 4). The first class consists of all vectors with exactly two nonzero coordinates, each $\pm 1$: there are $\binom{8}{2} \times 2^2 = 28 \times 4 = 112$ such vectors. The second class consists of all vectors with all eight coordinates equal to $\pm 1/2$ and an even number of negative coordinates: there are $2^8 / 2 = 128$ such vectors. Both classes have squared norm equal to 2, so all 240 vectors lie on the sphere of radius $\sqrt{2}$. No other lattice points lie at this distance, so these are precisely the nearest neighbors. That $\tau(8) \leq 240$ (tightness) follows from the general LP bound of Kabatyanskii and Levenshtein (1978), which in eight dimensions yields exactly this upper limit. $\square$

**Tightness and boundary caveat.** The 240 upper bound is achieved only for maximally dense ($E_8$-optimal) arrangements; typical brand distributions will have far fewer nearest competitors. Moreover, this bound applies to interior positions in the lattice; boundary positions have fewer nearest neighbors, and given concentration-of-measure results (Zharnikov 2026f), boundary effects may be pervasive in finite brand spaces.

**Plain-English interpretation.** If a brand occupies a position in the maximally efficient packing of 8-dimensional perception space, it has at most 240 nearest competitors. These competitors come in two distinct types:

- **112 specialist competitors** that match the focal brand on 6 of 8 dimensions but differ sharply on exactly 2 dimensions. In SBT terms, these are brands that share most of their spectral profile but diverge on a specific pair of dimensions -- for example, matching on narrative, ideological, experiential, social, cultural, and temporal dimensions but differing on semiotic and economic dimensions.

- **128 generalist competitors** that differ from the focal brand moderately on all 8 dimensions simultaneously. These are brands that occupy a slightly shifted position across the entire spectrum -- not dramatically different on any single dimension, but consistently different across all of them.

**Interpretive caveat.** The 112/128 decomposition describes the geometry of the $E_8$ lattice, not an empirical observation about competitive dynamics. The specialist/generalist interpretation is structurally motivated but remains an analogy -- real competitive dynamics involve asymmetric substitution, category boundaries, and observer heterogeneity that no lattice model captures.

**Figure 1: Decomposition of the 240 minimal vectors of $E_8$ into specialist and generalist shells.**

``` {.mermaid width=55%}
graph TD
    K[E_8 kissing number = 240<br/>minimal vectors at squared norm 2]
    K --> S[Specialist shell<br/>112 vectors<br/>form: two coordinates plus or minus 1, six zeros]
    K --> G[Generalist shell<br/>128 vectors<br/>form: all eight coordinates plus or minus 1/2, even sign parity]
    S --> S1[Concentrated on 2 of 8 dimensions<br/>C(8,2) times 2-squared = 28 times 4 = 112]
    G --> G1[Distributed across all 8 dimensions<br/>2-to-the-8 divided by 2 = 128]
    S1 -. competitive interpretation .-> SC[Sharp differentiation<br/>on a small dimension subset]
    G1 -. competitive interpretation .-> GC[Diffuse differentiation<br/>across the full spectrum]
```

*Notes*: Solid arrows trace the algebraic decomposition (Conway & Sloane 1999, ch. 4); both shells lie at squared norm 2 and together exhaust the kissing configuration. Dashed arrows trace the structural-analogy reading flagged in the interpretive caveat above; the analogy is motivated by the geometry, not asserted as an empirical regularity. The 112:128 ratio is approximately .47:.53 by construction.

*Falsification*: Proposition 2 is falsified if the $E_8$ lattice's minimal vectors can be shown to number other than 240, or if more than 240 non-overlapping unit spheres in $\mathbb{R}^8$ can simultaneously touch a central unit sphere. (Both are mathematically proved impossible; the proposition would be falsified at the mathematical level, not the empirical one.)

### Comparison Across Dimensions

To appreciate the significance of eight dimensions, we compare positioning capacity across dimensionalities at a fixed perceptual threshold of $\varepsilon = .10$:

Table 5: Positioning Capacity by Dimensionality at $\varepsilon = .10$.

| Dimensions $n$ | Capacity $\geq (1/\varepsilon)^n$ | Interpretation |
|-----------------|-------------------------------------|----------------|
| 2 | $10^2$ (100) | Traditional perceptual map |
| 3 | $10^3$ (1,000) | 3D brand model |
| 4 | $10^4$ (10,000) | Multi-attribute model |
| 6 | $10^6$ (1 million) | Rich attribute space |
| **8** | **$10^8$ (100 million)** | **SBT full dimensionality** |
| 12 | $10^{12}$ (1 trillion) | Hypothetical fine-grained model |
| 16 | $10^{16}$ | Theoretical upper bound |

*Notes*: Capacity grows exponentially with dimension. Projection from 8D to 2D collapses capacity by a factor of $10^6$.

The exponential growth in capacity with dimension explains a persistent puzzle in marketing practice: why do perceptual maps (typically 2D) consistently show markets as "crowded," while practitioners report finding viable new positions? The answer is that 2D maps represent a projection that collapses capacity from $10^8$ to $10^2$ -- a factor of one million. Positions that are well-separated in 8 dimensions become overlapping in 2 dimensions, exactly the spectral metamerism phenomenon formalized in Zharnikov (2026e).

---

## White Space and Market Saturation

### The Abundance of Unoccupied Positions

**Proposition 3** (White space abundance). *For $n_b$ brands in the unit 8-ball with perceptual threshold $\varepsilon$, the fraction of the positioning space not covered by any brand's perceptual neighborhood is approximately:*

$$f_{\text{white}} \approx 1 - n_b \cdot \varepsilon^8$$

*provided $n_b \cdot \varepsilon^8 \ll 1$ (so that overlaps between neighborhoods are negligible).*

*In particular, at $\varepsilon = .10$:*

Table 6: White Space Fraction by Number of Brands at $\varepsilon = .10$.

| Number of brands $n_b$ | White space fraction |
|-------------------------|---------------------|
| 100 | 99.9999% |
| 1,000 | 99.9990% |
| 10,000 | 99.9900% |
| 100,000 | 99.9000% |
| 1,000,000 | 99.0000% |

*Notes*: White space fraction $\approx 1 - n_b \cdot \varepsilon^8$; assumes non-overlapping perceptual neighborhoods. Approximation quality deteriorates as $n_b \cdot \varepsilon^8$ approaches order unity; rows with $n_b \geq 10^5$ should be read as upper-bound estimates.

*Proof.* Each brand's perceptual neighborhood is a ball of radius $\varepsilon$ in the clr-transformed space. The volume of each neighborhood relative to the unit ball is $V_8(\varepsilon) / V_8(1) = \varepsilon^8$. For $n_b$ brands with non-overlapping neighborhoods, the covered fraction is $n_b \cdot \varepsilon^8$. At $\varepsilon = .10$, each neighborhood occupies a fraction $10^{-8}$ of the unit ball, so 100 brands cover $100 \times 10^{-8} = 10^{-6}$ of the space, and 10,000 brands cover $10^{-4}$. $\square$

**Plain-English interpretation.** The 8-dimensional positioning space is almost entirely empty. Even with 10,000 brands -- far more than any single product category contains -- 99.99% of the space is unoccupied. This is a direct consequence of the curse of dimensionality: volumes in high dimensions are much larger than low-dimensional intuition suggests.

*Falsification*: Proposition 3 is falsified if the actual covered fraction of the 8-dimensional brand space, measured via volume integration over observed brand positions, exceeds $n_b \cdot \varepsilon^8$ by a margin inconsistent with the non-overlap assumption -- i.e., if brands cluster so densely that the approximation $f_\text{white} \approx 1 - n_b \cdot \varepsilon^8$ systematically overestimates white space.

### Why White Space Identification Is Harder Than It Seems

The abundance of white space might seem to make positioning easy: just pick an unoccupied region. The empirical literature shows that first movers into unoccupied positions gain lasting advantages (Carpenter & Nakamoto 1989), consistent with the geometric argument that unoccupied positions are abundant but difficult to discover. In practice, white space identification is notoriously difficult (Keller & Lehmann 2006), and the geometry of high-dimensional space explains why.

**The corner effect.** The ratio $V_8(1) / 2^8 = 4.059 / 256 \approx .016$. Only 1.6% of the hypercube's volume lies within the inscribed ball; the remaining 98.4% occupies "corners" that are likely outside the feasible brand space.

**Concentration near boundaries.** As Zharnikov (2026f) showed, high-dimensional distributions concentrate near boundaries. A uniformly random point in the 8-ball has expected distance $\sqrt{8/10} \approx .89$ from the origin -- the "interior" is geometrically smaller than it appears.

**Projection collapse.** White space that exists in 8 dimensions may be invisible in 2D projections -- the positioning analog of the metamerism result in Zharnikov (2026e).

### Category Saturation

**Proposition 4** (Category saturation criterion). *A product category with effective dimensionality $d_{\text{eff}}$ and perceptual threshold $\varepsilon$ is* saturated *when the number of brands $n_b$ approaches the packing capacity:*

$$n_b \approx \left(\frac{1}{\varepsilon}\right)^{d_{\text{eff}}}$$

*For categories with different effective dimensionalities:*

Table 7: Category Saturation Capacity by Effective Dimensionality at $\varepsilon = .10$.

| Effective dimensionality $d_{\text{eff}}$ | Capacity at $\varepsilon = .10$ | Example categories |
|---|---|---|
| 2 | 100 | Commodity goods (price + basic quality) |
| 3 | 1,000 | Consumer packaged goods |
| 5 | 100,000 | Fashion, consumer electronics |
| 8 | $10^8$ | Luxury, lifestyle brands |

*Notes*: Category examples are illustrative; empirical $d_{\text{eff}}$ estimation requires PCA on observer-perceived brand profiles.

*Proof sketch.* The capacity bound $(1/\varepsilon)^n$ from Proposition 1, applied with $n = d_{\text{eff}}$. Saturation occurs when the number of brands approaches this bound, meaning that most positions within the feasible region are occupied and new entrants necessarily encroach on existing brands' perceptual neighborhoods. $\square$

**Plain-English interpretation.** Saturation depends on effective dimensionality, not raw brand count. A commodity market ($d_{\text{eff}} \approx 2$) saturates at approximately 100 brands. A luxury market ($d_{\text{eff}} \approx 8$) can accommodate 100 million distinguishable positions. The strategic implication is that brands should seek to activate independent dimensions, not merely more dimensions.

*Falsification*: Proposition 4 is falsified if a product category's observed brand count consistently and substantially exceeds $(1/\varepsilon)^{d_\text{eff}}$ (estimated via PCA on observer-perceived brand profiles) without measurable perceptual overlap -- indicating that the effective dimensionality estimate was too low, not that capacity is unbounded.

The category examples in the table above are illustrative, not empirical. Determining the effective dimensionality of a specific product category requires empirical measurement -- for example, via PCA on observer-perceived brand profiles or analysis of which SBT dimensions drive differentiation in that category. This is a direction for future empirical work.

---

## Effective Dimensionality and Correlation

### When Dimensions Correlate

SBT posits eight conceptually distinct dimensions, but in practice these dimensions may be correlated. A luxury brand that scores high on the semiotic dimension (sophisticated visual identity) is likely also to score high on the cultural dimension (cultural resonance) and the temporal dimension (heritage). Such correlations reduce the effective dimensionality of the space and, consequently, the positioning capacity.

**Proposition 5** (Dimensional correlation reduces capacity). *If the eight SBT dimensions have average pairwise correlation $\rho$, the effective dimensionality is:*

$$d_{\text{eff}} = \frac{n}{1 + (n-1)\rho}$$

*and the positioning capacity at threshold $\varepsilon$ is approximately $(1/\varepsilon)^{d_{\text{eff}}}$. For $n = 8$:*

Table 8: Effective Dimensionality and Positioning Capacity by Average Pairwise Correlation ($n = 8$, $\varepsilon = .10$).

| Correlation $\rho$ | $d_{\text{eff}}$ | Capacity at $\varepsilon = .10$ |
|---------------------|-------------------|----------------------------------|
| .0 | 8.00 | $10^8$ |
| .1 | 4.71 | $\sim 10^5$ |
| .2 | 3.33 | $\sim 10^3$ |
| .3 | 2.58 | $\sim 10^3$ |
| .5 | 1.78 | $\sim 10^2$ |
| .7 | 1.36 | $\sim 10^1$ |

*Notes*: $d_{\text{eff}} = n / (1 + (n-1)\rho)$, equicorrelation case. Capacity is approximate; computed as $(1/\varepsilon)^{d_\text{eff}}$.

**Figure 2: Capacity-collapse curve under average pairwise correlation ($n = 8$, $\varepsilon = .10$).**

```mermaid
xychart-beta
    title "Positioning capacity collapses as inter-dimension correlation rises"
    x-axis "Average pairwise correlation rho" [".0", ".1", ".2", ".3", ".5", ".7"]
    y-axis "log10 capacity" 0 --> 9
    line [8, 5, 3, 3, 2, 1]
```

*Figure 2: Log-base-10 positioning capacity as a function of average pairwise correlation rho among SBT dimensions (n = 8, epsilon = .10). Plotted values are log10((1/epsilon)^d_eff) rounded to the nearest integer; exact values from Table 8 are 8.00, 4.71, 3.33, 2.58, 1.78, 1.36. The curve is steepest in the low-correlation regime (rho in [.0, .2]): even modest positive correlation collapses capacity by three or more orders of magnitude before rho = .2 is reached. Proposition 5 result.*

*Notes*: Mermaid rendering of the same data shown in Table 8. The vertical axis is $\log_{10}$ of capacity; the horizontal axis is the average pairwise correlation $\rho$ (non-uniformly spaced sample points). Capacity contracts by approximately five orders of magnitude as $\rho$ moves from $.0$ to $.7$, reflecting the participation-ratio collapse of $d_{\text{eff}}$ from 8.00 to 1.36 over the same interval. The curve is steepest in the low-correlation regime ($\rho \in [.0, .2]$): a small positive correlation already costs more than three orders of magnitude of capacity.

*Proof.* The effective dimensionality formula follows from the eigenvalue structure of a correlation matrix with uniform off-diagonal entries $\rho$. Such a matrix has one eigenvalue $\lambda_1 = 1 + (n-1)\rho$ and $(n-1)$ eigenvalues $\lambda_k = 1 - \rho$ for $k = 2, \ldots, n$. The "participation ratio" $d_{\text{eff}} = (\sum \lambda_k)^2 / \sum \lambda_k^2$ simplifies to $n / (1 + (n-1)\rho)$ in this equicorrelation case. Capacity at reduced dimensionality follows from Proposition 1 applied with $n = d_{\text{eff}}$ (rounding to the nearest integer for the lower bound computation). $\square$

*Falsification*: Proposition 5 is falsified if an empirically estimated correlation matrix of SBT dimension scores produces a participation-ratio effective dimensionality that does not predict observed positioning capacity (measured by independent brand counts and pairwise distinguishability) at the rate $(1/\varepsilon)^{d_\text{eff}}$ -- or if the equicorrelation assumption systematically misrepresents the eigenvalue structure of real brand-perception data.

### Implications for SBT

The capacity collapse under correlation has profound implications for brand strategy:

**At $\rho = 0$** (fully independent dimensions): The eight SBT dimensions provide maximum differentiation power. Capacity is $10^8$, and white space is abundant. This is the theoretical ideal -- a brand that manages to differentiate on all eight dimensions simultaneously exploits the full positioning capacity.

**At $\rho = .3$** (moderate correlation): Effective dimensionality drops to approximately 2.6, and capacity collapses from $10^8$ to approximately $10^3$ -- a reduction by a factor of 100,000. This estimate assumes uniform inter-dimension correlation; for non-uniform correlation matrices with the same average $\rho$, $d_{\text{eff}}$ may be substantially higher or lower depending on whether the dominant eigenvalue absorbs most variance or variance is distributed across several modes. If SBT dimensions are moderately correlated in a given category (e.g., luxury goods where semiotic, cultural, and temporal signals tend to be high together), the positioning space is much smaller than the nominal 8-dimensional capacity suggests.

**At $\rho = .7$** (high correlation): The eight dimensions effectively collapse to approximately 1.4, and the market capacity is approximately 10 -- barely a handful of distinguishable positions. This represents a category where nearly all dimensions co-vary, leaving little room for differentiation.

The implication is that **a brand's strategic task is not just to occupy a position but to de-correlate its dimensional profile.** A brand that achieves a profile where its eight dimension scores are relatively independent of each other -- high on some, moderate on others, low on still others, in a pattern that does not simply mirror the category's typical correlation structure -- gains disproportionate positioning advantage because it exploits more of the available dimensionality.

This connects to SBT's concept of coherence types. The $A+$ (ecosystem) coherence type, which requires strong performance across all dimensions, is rare precisely because it requires occupying a position in a high-dimensional region where most brands cluster. The $B+$ (identity) coherence type, which tolerates dimensional trade-offs, may actually be *strategically advantageous* for positioning because it creates profiles that are more dimensionally distinctive. These dimensional-correlation effects are formally connected to coherence-resilience ordering in Zharnikov (2026s).

### Empirical Estimates of Dimensional Correlation

Among the SBT case studies, Hermès ($A+$) has the most uniform profile (high across most dimensions, though the Economic dimension (3.0) is a notable exception to this general pattern, suggesting high within-brand correlation overall), while Tesla ($C-$) has the most variable profile (very high on narrative, very low on ideological and temporal, suggesting greater dimensional independence). The critical point is that correlation structure may vary by *category*: luxury goods may have inherently correlated dimensions (semiotic $\leftrightarrow$ cultural $\leftrightarrow$ temporal), while technology may have more independent dimensions (experiential vs. economic vs. ideological). Category-level correlation structure determines positioning capacity as much as raw dimensionality.

---

## Why Eight Dimensions Is Special

### $E_8$ Optimality

Viazovska's (2017) proof that $E_8$ achieves the densest packing in $\mathbb{R}^8$ uses modular forms to construct a "magic function" certifying optimality among *all* packings, not just lattice packings. The optimal packing is known exactly in only $n = 1, 2, 3, 8,$ and $24$. The cases $n = 8$ and $n = 24$ (Cohn et al., 2017, using the Leech lattice) are exceptional: their proofs are elegant and suggest that something about these dimensions is deeply special. For brand positioning, the significance is that in $n = 8$ we have *exact* answers: the packing density $\pi^4/384$, the kissing number 240, and the full nearest-neighbor configuration. Independent grounds for the eight-dimensional choice based on meaning-channel completeness are developed in Zharnikov (2026r); the present mathematical considerations and the corpus-internal scientific motivation thus converge on $n = 8$.

### Division Algebras and Parallelizable Spheres

**Interpretive caveat: the following connections are speculative and included for intellectual context only.**

The number 8 is exceptional in mathematics: the normed division algebras ($\mathbb{R}, \mathbb{C}, \mathbb{H}, \mathbb{O}$) have dimensions 1, 2, 4, and 8 (Hurwitz 1898); the spheres $S^0, S^1, S^3, S^7$ are the only parallelizable spheres (Adams 1962). The $E_8$ lattice's optimality connects to these structures through unimodular lattices and modular forms.

Whether SBT's eight dimensions have any deeper connection to these structures is unknown. SBT's dimensions were derived from qualitative analysis (Zharnikov 2026a), not mathematical considerations. The coincidence is fortunate for the analysis but is not evidence of a structural connection.

### The $E_8$ Kissing Configuration and Competitive Geometry

The 240 kissing vectors form the root system of the exceptional Lie group $E_8$, decomposing into: 112 specialist vectors ($\binom{8}{2} \times 4 = 28 \times 4$), giving 4 competitive directions for each of the 28 dimension-pairs; and 128 generalist vectors ($2^8 / 2 = 2^7$), reflecting a binary higher/lower choice on each dimension with an even-parity constraint.

The specialist-to-generalist ratio is $112:128 \approx 47\%:53\%$, suggesting that in an optimally packed market, roughly half of competitive threats come from sharp differentiation on a few dimensions and half from diffuse differentiation across all dimensions. Whether this ratio has empirical relevance is an open question. The spherical-codes framework of Delsarte, Goethals, and Seidel (1977) provides the algebraic foundation for kissing-number bounds: that $\tau(8) = 240$ is tight follows from their LP technique applied to the $E_8$ root system.

---

## Applications and Examples

### Luxury Fashion: High Effective Dimensionality

Luxury fashion brands (Hermès, Chanel, Louis Vuitton, Gucci, Prada) arguably activate all eight SBT dimensions -- from distinctive visual identity (semiotic) through heritage depth (temporal). If these dimensions are moderately independent ($\rho \approx .2$), effective dimensionality is approximately 3.3, yielding a category capacity of roughly $10^3$ -- about 1,000 distinguishable luxury positions. This is consistent with the global luxury market supporting several hundred distinct houses without apparent saturation.

If the luxury category's dimensions are more tightly correlated ($\rho \approx .5$, reflecting a "luxury halo" where positive signals co-occur), effective dimensionality drops to 1.8 and capacity drops to approximately 100 -- suggesting approaching saturation, a claim some industry analysts have made (Kapferer & Bastien 2012).

### Commodity Goods: Low Effective Dimensionality

At the other extreme, commodity goods (bottled water, paper towels, basic canned goods) may activate only 2--3 SBT dimensions meaningfully -- primarily economic (price) and experiential (basic product quality), with limited differentiation on semiotic, narrative, ideological, social, cultural, or temporal dimensions. With $d_{\text{eff}} \approx 2$, the category capacity is approximately $10^2 = 100$, which saturates quickly. This is consistent with the observation that commodity categories tend to consolidate around a small number of brands, with generic/store brands capturing the undifferentiated middle.

### Long-Tail Market Fragmentation

The capacity bounds help explain the long-tail phenomenon in digital markets. When distribution costs approach zero, the vast white space (99.99% unoccupied at 10,000 brands) becomes accessible to niche brands. Long-tail brands succeed by occupying positions in high-dimensional regions that established brands ignore -- differentiating on dimension combinations (e.g., ideological + experiential + social) that mass-market competitors may not recognize as competitive axes.

### Why "White Space" Identification Is Harder Than Marketers Think

Despite the mathematical abundance of white space, practical identification encounters three geometric obstacles: (1) **projection blindness** -- most tools operate in 2--3 dimensions, collapsing capacity from $10^8$ to $10^2$; (2) **feasibility constraints** -- not all positions in $\mathbb{R}^8_+$ are achievable, given category norms, resources, and observer expectations; and (3) **observer heterogeneity** -- white space for one perceptual cohort may be occupied for another, because different observer weight profiles yield different perceptual distances (Zharnikov 2026d; 2026f). These obstacles explain the gap between mathematical abundance and practical difficulty without invalidating the capacity bounds.

---

## Limitations and Caveats

This section consolidates the caveats that have been flagged throughout the paper. We consider them essential to the intellectual honesty of the contribution.

### Anisotropy: SBT Dimensions Are Not Symmetric

The sphere packing analysis assumes isotropic space: equal scaling in all directions. SBT's eight dimensions are unlikely to be isotropic. Some dimensions may have wider perceptual ranges than others (e.g., the economic dimension may span a larger range of distinguishable values than the temporal dimension), and the perceptual threshold $\varepsilon$ may vary by dimension. The psychophysical distinction between integral and separable dimensions (Garner 1974) is directly relevant: integral dimensions (where attention cannot be selectively focused) are naturally modeled with Euclidean distance, whereas separable dimensions support city-block metrics (Shepard 1987). The sphere-packing apparatus assumes Euclidean $\varepsilon$-balls throughout; for separable-dimension pairs, ellipsoidal or city-block packing bounds would be more appropriate.

In an anisotropic space, the "spheres" of Proposition 1 become ellipsoids, and the packing problem becomes substantially harder. The $E_8$ lattice no longer provides the optimal packing for ellipsoids (the optimal ellipsoid packing depends on the aspect ratios). The capacity bounds of Proposition 1 remain valid as order-of-magnitude estimates, because the volume ratio argument does not depend on isotropy, but the exact constants change.

### The $E_8$ Connection Is Interpretive, Not Literal

We emphasize again: the $E_8$ lattice provides the mathematical ceiling on sphere packing density in 8 dimensions. The connection to brand positioning is that *if* brand perception space is 8-dimensional and *if* the metric is approximately Euclidean (which the clr transform ensures for the Aitchison metric), *then* the $E_8$ density bounds apply. This does not mean:

- That brands arrange themselves on an $E_8$ lattice
- That the 240 kissing number literally describes competitive dynamics
- That the specialist/generalist decomposition is a law of markets
- That the $E_8$ structure has any causal role in brand perception

The correct interpretation is: $E_8$ provides an *upper bound on structural order*. The actual distribution of brands in perception space is noisy, irregular, non-uniform, and far from any lattice. The $E_8$ bound tells us the mathematical limit of what would be possible if brands were arranged with perfect geometric efficiency.

### Observer Dependence

The entire analysis assumes a single, fixed metric -- the Aitchison metric on brand emission profiles. But SBT's core insight is that brand distance is observer-dependent (Zharnikov 2026d): the observer-weighted metric $d_k(A, B) = \|W_k \circ (\text{clr}(s_A) - \text{clr}(s_B))\|_2$, where $W_k$ is observer $k$'s weight vector, can make the same brand pair appear close or far depending on the observer.

In the observer-dependent metric, the "spheres" of the packing problem are no longer spheres but observer-dependent ellipsoids. The positioning capacity is therefore also observer-dependent: a market that appears saturated to one perceptual cohort may have abundant white space for another. A full treatment of observer-dependent packing bounds would require integrating over the observer distribution on $\Delta^7$, which is a direction for future work.

### Noise and Measurement Uncertainty

Brand perception is inherently noisy. An observer's perception of a brand fluctuates across encounters (mood, context, recent experiences), and different observers perceive the same brand differently. The packing analysis assumes precise, deterministic positions, whereas real brand positions are distributions (perception clouds in SBT's terminology).

When brand positions are noisy, the effective perceptual threshold increases (because noise adds to the minimum distance required for reliable discrimination), and the capacity decreases. A noisy version of Proposition 1 would replace $\varepsilon$ with $\varepsilon + 2\sigma$, where $\sigma$ is the standard deviation of perceptual noise, reducing capacity by a factor of $((\varepsilon + 2\sigma)/\varepsilon)^8$.

### Bounded Region Assumption

The capacity bounds are computed for a unit ball. The actual brand space may not be bounded, or may have a different shape. If the feasible region is smaller than the unit ball (because not all dimension combinations are achievable), the capacity is proportionally reduced. If the region is non-convex (because some dimension combinations are mutually incompatible), the packing problem becomes harder and the simple volume bounds may overestimate capacity.

### Boundary Conditions: When the Bounds Apply

The capacity bounds and the $E_8$ apparatus hold under a conjunction of scope conditions that should be stated explicitly. First, **dimensional independence**: the bounds assume that the eight SBT dimensions generate an effectively eight-dimensional space; if dimensions collapse through correlation (Proposition 5), the applicable bounds are those for $d_{\text{eff}} < 8$ (see Zharnikov 2026r for the completeness and necessity argument). Second, **Aitchison-metric assumption**: the flat-Euclidean geometry is correct only under the clr transform and the compositional-ratio model of perception; empirical data should be checked for distributional assumptions before applying the bounds (Zharnikov 2026d). Third, **salience-of-differentiation regime**: the packing bounds are tight when observer cohorts are sensitive to differences across all eight dimensions; in low-salience categories, effective capacity converges toward Sharp's (2010) mental-availability model rather than the geometric ceiling. Fourth, **interior vs boundary positioning**: concentration of measure (Zharnikov 2026f) pushes brand profiles toward the boundary of the feasible region, and boundary positions have fewer nearest-competitor slots than interior positions. Taken together, the bounds are best read as ceiling estimates that become tighter as dimensional independence increases, metric assumptions are satisfied, observer cohorts are differentiation-sensitive, and brands occupy interior positions.

---

## Discussion

### Connection to R2: Metamerism as Failed Positioning

The positioning capacity analysis provides quantitative context for Zharnikov (2026e): in 8 dimensions there are $10^8$ distinguishable positions, but in 1 dimension only $1/\varepsilon = 10$ at $\varepsilon = .10$. The projection collapses $10^7$ positions onto each grade level, making metamerism overwhelmingly likely.

### Connection to R3: Concentration Near Boundaries

Zharnikov (2026f) showed that 57% of $\Delta^7$ lies within relative distance .10 of a cohort boundary. The positioning capacity analysis reveals the complement: even with $10^8$ positions available, concentration pushes actual brand profiles toward thin shells. Both "who is observing" and "where brands are" concentrate in geometrically constrained regions, despite the theoretical abundance of the full space.

### Tension with Empirical Brand Growth Research

The capacity analysis above establishes a theoretical upper bound on positioning diversity. A productive tension arises from empirical work by Sharp (2010), whose analysis of market data shows that most real markets converge on a small number of highly salient brands regardless of the theoretical positioning space available. Sharp argues that mental availability and physical availability -- not differentiated positioning -- drive brand growth, and that brand differentiation strategies are routinely overstated as competitive advantages. This directly challenges the prescriptive implication that brands should "exploit 8-dimensional white space."

The two frameworks are asking different questions, and the distinction is essential. This paper asks: *how many brands CAN a market hold?* Sharp asks: *how many brands DO consumers consider?* The theoretical capacity of $10^8$ positions is a mathematical ceiling; Sharp's findings establish that the practical consideration set is bounded at far fewer alternatives, because most consumers do not perceive or value dimensional differentiation across all eight axes in any given product category. R4's geometric capacity predicts market structure when dimensional differentiation is salient to the relevant observer cohorts (low $\rho$); Sharp's mental availability dominates when brand differentiation is cognitively discounted (high $\rho \to d_{\text{eff}} \approx 1$--$2$). The two frameworks are boundary conditions on each other, not contradictions. The gap between geometric capacity and practical salience represents an opportunity cost that future empirical work should quantify.

### Future Directions

Natural extensions include: (1) **empirical calibration of $\varepsilon$** via JND experiments adapted from psychophysics; (2) **anisotropic packing** with dimension-specific thresholds; (3) **observer-dependent capacity** by integrating packing bounds over observer distributions on $\Delta^7$; (4) **dynamic capacity** as the metric evolves under signal decay and crystallization, connecting to R6 (Zharnikov forthcoming); (5) **empirical dimensionality estimation** via PCA on observed brand profiles to test Proposition 5; and (6) **category-level analysis** comparing observed saturation patterns against predicted capacity at estimated effective dimensionality.

### Empirical Test: Competitive Interference in LLM Perception Space

The sphere packing model assumes that brands occupy fixed positions in perception space regardless of competitive context. If nearby competitors shift a brand's perceived profile -- through contrast effects (Simonson & Tversky 1992) or assimilation (Herr 1986) -- then positions would be context-dependent, and the fixed-geometry assumptions underlying Propositions 1--5 would require qualification. Experiment C tests this assumption directly.

**Design.** Five focal brands (Hermès, IKEA, Patagonia, Erewhon, Tesla) were each paired with three competitor types spanning a distance gradient: *direct* competitors (Hermès/Louis Vuitton, IKEA/H&M Home, Patagonia/Arc'teryx, Erewhon/Whole Foods, Tesla/Rivian), *adjacent* competitors (Hermès/Rolex, IKEA/Muji, Patagonia/REI, Erewhon/Blue Bottle, Tesla/Apple), and *distant* competitors (Hermès/Walmart, IKEA/Ferrari, Patagonia/Shein, Erewhon/McDonald's, Tesla/Toyota). Four conditions were administered: solo (brand rated alone), self-comparison (brand rated for "distinctiveness vs. category peers" -- a prompt-format baseline), paired (brand rated alongside a named competitor), and context (competitor mentioned as market context). Five models (Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Grok 4.1 Fast) each completed one replication per condition-pair combination, yielding 250 calls with 250 valid responses (100% completion).

**Results.** All three hypotheses returned null. H1 (profiles shift when a competitor is present): a binomial sign test on 8 per-dimension comparisons found 0 of 8 in the predicted direction (p = 1.00, one-sided); Cohen's d ranged from -.187 to +.169, all trivial. H2 (shift magnitude increases with competitor distance): F = .623, p = .538, eta-sq = .008. H3 (direct competitors produce contrast while distant competitors produce assimilation): t = -.502, p = .616, d = -.029. The self-comparison control confirmed that prompt-format differences alone are negligible (Euclidean shift = 2.10, no dimension significant).

**Exploratory finding.** GPT-4o-mini exhibited a mean profile shift of 15.37 across conditions, nearly double the 8.5--9.3 range observed for the other four models. Erewhon was the most susceptible focal brand (shift = 11.73 vs. 9.4--10.1 for others), consistent with its weak Temporal anchoring (2.5). Neither anomaly reached per-dimension significance.

**Interpretation.** The null result is scientifically valuable: PRISM-B measures stable internal representations, not context-dependent judgments. Brands occupy fixed positions in perception space regardless of which competitors are nearby, consistent with the fixed-geometry assumptions of sphere packing. The capacity bounds derived in the Positioning Capacity and White Space sections hold as intrinsic constraints, not context-dependent artifacts. Had competitive interference been large, the effective dimensionality of perception space would itself be context-dependent, undermining the fixed-geometry framework on which Propositions 1--5 rest. The Erewhon finding aligns with the Anisotropy subsection: brands with weak anchoring on one or more dimensions exhibit greater volatility, even when that volatility does not reach statistical significance. The GPT-4o-mini anomaly suggests that some model architectures have more permeable perceptual boundaries, a finding that warrants investigation across a larger model sample. A subsequent gpt-4o-mini-only replication with 16 repetitions per condition (Zharnikov 2026p, 240 calls) confirms this anomaly: per-(brand × dimension) ANOVAs detect 11 of 40 cells reaching Bonferroni significance (largest Hermès/Narrative d = 3.27), clustering on identity-intensive dimensions for prestige and purpose brands. The pattern is consistent with the present cross-model null on aggregate H1/H2/H3 tests: the high-replication single-model design has the per-cell power to surface model-specific instability that the broader-model lower-replication design flags as exploratory anomaly only.

---

## Conclusion

This paper has established formal bounds on the number of distinguishable brand positions in Spectral Brand Theory's eight-dimensional perception space, drawing on sphere packing theory and, in particular, the $E_8$ lattice whose optimality in eight dimensions was proved by Viazovska (2017).

The central results are:

1. **Positioning capacity grows exponentially with dimension** (Proposition 1). At perceptual threshold $\varepsilon = .10$, the 8-dimensional space admits at least $10^8$ distinguishable positions -- six orders of magnitude more than a 2-dimensional perceptual map. The persistent perception that markets are "crowded" often reflects projection to an inadequately low-dimensional representation, not genuine scarcity of positions.

2. **Local competition is bounded by the kissing number** (Proposition 2). Each position has at most 240 nearest competitors in the optimal $E_8$ packing, decomposing into 112 specialist (2-dimension) and 128 generalist (8-dimension) competitive vectors. This provides a geometric framework for analyzing competitive proximity, with the caveat that it describes mathematical structure, not empirical regularity.

3. **White space is overwhelmingly abundant** (Proposition 3). Even with 10,000 brands, 99.99% of the positioning space is unoccupied. The practical difficulty of identifying white space is not a scarcity problem but a *perception* problem -- the available dimensions are not fully exploited.

4. **Category saturation depends on effective dimensionality** (Proposition 4). A commodity market with $d_{\text{eff}} \approx 2$ saturates at approximately 100 brands. A luxury market with $d_{\text{eff}} \approx 8$ can accommodate 100 million. The strategic implication: brands should seek to activate independent dimensions, not just more dimensions.

5. **Dimensional correlation is the critical variable** (Proposition 5). At average correlation $\rho = .3$, capacity collapses from $10^8$ to $10^3$. A brand's most valuable strategic asset may be its ability to de-correlate its dimensional profile -- to achieve a pattern of strengths and weaknesses that does not simply mirror the category's correlation structure.

These results advance the mathematical foundations of Spectral Brand Theory from a framework with a formal metric (Zharnikov 2026d) to one with formal capacity bounds. The analysis is explicitly honest about its limitations: the $E_8$ connection is interpretive, not literal; real brand space is anisotropic and noisy; observer dependence complicates any single capacity number; and empirical calibration of the perceptual threshold remains to be done. The strength of the contribution lies not in claiming that markets are $E_8$ lattices but in providing the first formal answer -- grounded in proved mathematical results -- to the question with which we began: *how many brands can a market hold?*

The answer, it turns out, depends less on the market and more on how many dimensions of perception are activated and how independently they vary. In the full 8-dimensional SBT space with independent dimensions, the answer is: far more than currently exist.

---

## Acknowledgments

AI assistants (Claude Opus 4.7, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

---

## References

Aaker, D. A. (1991). *Managing Brand Equity: Capitalizing on the Value of a Brand Name*. Free Press.

Aaker, J. L. (1997). Dimensions of brand personality. *Journal of Marketing Research*, 34(3), 347--356.

Adams, J. F. (1962). Vector fields on spheres. *Annals of Mathematics*, 75(3), 603--632.

Aitchison, J. (1986). *The Statistical Analysis of Compositional Data*. Chapman and Hall.

Bijmolt, T. H. A., & Wedel, M. (1999). A comparison of multidimensional scaling methods for perceptual mapping. *Journal of Marketing Research*, 36(2), 277--285. https://doi.org/10.1177/002224379903600211

Carpenter, G. S., & Nakamoto, K. (1989). Consumer preference formation and pioneering advantage. *Journal of Marketing Research*, 26(3), 285--298. https://doi.org/10.1177/002224378902600303

Cohn, H., & Elkies, N. (2003). New upper bounds on sphere packings I. *Annals of Mathematics*, 157(2), 689--714. https://doi.org/10.4007/annals.2003.157.689

Cohn, H., Kumar, A., Miller, S. D., Radchenko, D., & Viazovska, M. (2017). The sphere packing problem in dimension 24. *Annals of Mathematics*, 185(3), 1017--1033.

Conway, J. H., & Sloane, N. J. A. (1999). *Sphere Packings, Lattices and Groups* (3rd ed.). Springer.

Delsarte, P., Goethals, J. M., & Seidel, J. J. (1977). Spherical codes and designs. *Geometriae Dedicata*, 6(3), 363--388.

Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. (2003). Isometric logratio transformations for compositional data analysis. *Mathematical Geology*, 35(3), 279--300.

Fechner, G. T. (1860). *Elemente der Psychophysik*. Breitkopf und Hartel.

Gardenfors, P. (2000). *Conceptual Spaces: The Geometry of Thought*. MIT Press.

Gardenfors, P. (2014). *The Geometry of Meaning: Semantics Based on Conceptual Spaces*. MIT Press.

Garner, W. R. (1974). *The Processing of Information and Structure*. Erlbaum.

Green, P. E., & Rao, V. R. (1972). *Applied Multidimensional Scaling: A Comparison of Approaches and Algorithms*. Holt, Rinehart and Winston.

Hamming, R. W. (1950). Error detecting and error correcting codes. *Bell System Technical Journal*, 29(2), 147--160.

Hales, T. C. (2005). A proof of the Kepler conjecture. *Annals of Mathematics*, 162(3), 1065--1185.

Herr, P. M. (1986). Consequences of priming: Judgment and behavior. *Journal of Personality and Social Psychology*, 51(6), 1106--1115.

Hotelling, H. (1929). Stability in competition. *Economic Journal*, 39(153), 41--57.

Hurwitz, A. (1898). Uber die Composition der quadratischen Formen von beliebig vielen Variablen. *Nachrichten von der Gesellschaft der Wissenschaften zu Gottingen*, 309--316.

Kabatyanskii, G. A., & Levenshtein, V. I. (1978). Bounds for packings on a sphere and in space. *Problems of Information Transmission*, 14(1), 1--17.

Kapferer, J.-N. (2008). *The New Strategic Brand Management: Creating and Sustaining Brand Equity Long Term* (4th ed.). Kogan Page.

Kapferer, J.-N., & Bastien, V. (2012). *The Luxury Strategy: Break the Rules of Marketing to Build Luxury Brands* (2nd ed.). Kogan Page.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1--22.

Keller, K. L., & Lehmann, D. R. (2006). Brands and branding: Research findings and future priorities. *Marketing Science*, 25(6), 740--759.

Lancaster, K. J. (1966). A new approach to consumer theory. *Journal of Political Economy*, 74(2), 132--157.

Pfender, F., & Ziegler, G. M. (2004). Kissing numbers, sphere packings, and some unexpected proofs. *Notices of the American Mathematical Society*, 51(8), 873--883.

Ries, A., & Trout, J. (1981). *Positioning: The Battle for Your Mind*. McGraw-Hill.

Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379--423.

Tenenbaum, Joshua B., Charles Kemp, Thomas L. Griffiths, and Noah D. Goodman (2011). How to grow a mind: Statistics, structure, and abstraction. *Science*, 331(6022):1279--1285. https://doi.org/10.1126/science.1192788

Sharp, B. (2010). *How brands grow: What marketers don't know*. Oxford University Press.

Shepard, R. N. (1987). Toward a universal law of generalization for psychological science. *Science*, 237(4820), 1317--1323. https://doi.org/10.1126/science.3629243

Simonson, I., & Tversky, A. (1992). Choice in context: Tradeoff contrast and extremeness aversion. *Journal of Marketing Research*, 29(3), 281--295.

Viazovska, M. S. (2017). The sphere packing problem in dimension 8. *Annals of Mathematics*, 185(3), 991--1015.

Weber, E. H. (1834). *De Pulsu, Resorptione, Auditu et Tactu: Annotationes Anatomicae et Physiologicae*. Koehler.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026c). Geometric approaches to brand perception: A critical survey and research agenda. Working Paper. https://doi.org/10.5281/zenodo.18945217

Zharnikov, D. (2026d). Brand space geometry: A formal metric for multi-dimensional brand perception. Working Paper. https://doi.org/10.5281/zenodo.18945295

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026f). Cohort boundaries in high-dimensional perception space: A concentration of measure analysis. Working Paper. https://doi.org/10.5281/zenodo.18945477

Zharnikov, D. (2026r). Why eight? Completeness and necessity of the SBT dimensional taxonomy. Working Paper. https://doi.org/10.5281/zenodo.19207599

Zharnikov, D. (2026s). Coherence type as crisis predictor: A formal derivation from non-ergodic dynamics. Working Paper. https://doi.org/10.5281/zenodo.19208107

## Appendix A: Numerical Computations

All numerical results reported in this paper were computed using the companion code `R4_R5_computations.py` (Python 3.12, numpy, scipy). Key computed values:

Table A1: Key Numerical Values.

| Quantity | Value |
|----------|-------|
| Unit ball volume $V_8(1)$ | $4.059 \times 10^0$ |
| $E_8$ packing density $\pi^4/384$ | .253670 |
| $E_8$ kissing number | 240 (= 112 + 128) |
| Capacity at $\varepsilon = .05$ | $\geq 2.56 \times 10^{10}$ |
| Capacity at $\varepsilon = .10$ | $\geq 1.00 \times 10^{8}$ |
| Capacity at $\varepsilon = .20$ | $\geq 3.91 \times 10^{5}$ |
| White space: 100 brands, $\varepsilon = .10$ | 99.9999% |
| White space: 10,000 brands, $\varepsilon = .10$ | 99.9900% |
| Effective dim. at $\rho = .3$ | $d_{\text{eff}} = 2.58$ |
| Capacity at $d_{\text{eff}} = 2.58$, $\varepsilon = .10$ | $\sim 10^3$ |

*Notes*: All values computed via `R4_R5_computations.py` (Python 3.12, numpy, scipy).

The $E_8$-based capacity estimate (using the exact packing density) for $\varepsilon = .10$ is $6.49 \times 10^9$, which falls between the simple lower bound ($10^8$) and the upper bound ($3.78 \times 10^{10}$). All reported lower bounds use the conservative simple volume bound $(1/\varepsilon)^8$.

### *Companion Computation Script*

All numerical figures in this paper -- the unit-ball volumes of Table 2, the capacity bounds of Table 4, the white-space fractions of Table 6, the saturation thresholds of Table 7, the effective-dimensionality and capacity-collapse values of Table 8, the appendix tables A1 and B1, and the kissing-shell decomposition of Figure 1 -- are reproducible from a single companion script in the public mirror:

`https://github.com/spectralbranding/sbt-papers/tree/main/r4-sphere-packing/code/r4_capacity_bounds.py`

Run command:

`uv run --with numpy --with scipy python r4_capacity_bounds.py`

The script fixes `SEED = 42` at file top, exposes the volume function $V_n(r)$, the participation-ratio function $d_{\text{eff}}(n, \rho)$, the simple volume bound $(1/\varepsilon)^n$, the covering upper bound $((2 + \varepsilon)/\varepsilon)^n$, the $E_8$ packing-density estimate, and a deterministic enumeration of the 112 + 128 = 240 minimal vectors of $E_8$ at squared norm 2. All values reported in this appendix and in the body tables match the script's stdout to the displayed precision; the kissing-shell counts are exact.

## Appendix B: Dimensional Capacity Comparison

For reference, positioning capacity lower bounds $(1/\varepsilon)^n$ at $\varepsilon = .10$ across dimensions:

Table B1: Dimensional Capacity, Optimal Packings, and Kissing Numbers at $\varepsilon = .10$.

| $n$ | Capacity | Known optimal packing | Kissing number |
|-----|----------|----------------------|----------------|
| 1 | 10 | Trivial | 2 |
| 2 | 100 | Hexagonal | 6 |
| 3 | 1,000 | FCC / HCP | 12 |
| 4 | 10,000 | $D_4$ lattice | 24 |
| 6 | $10^6$ | $E_6$ lattice | 72 |
| **8** | **$10^8$** | **$E_8$ lattice (proved optimal)** | **240** |
| 12 | $10^{12}$ | Coxeter-Todd lattice | 756 |
| 16 | $10^{16}$ | Barnes-Wall lattice | 4,320 |
| 24 | $10^{24}$ | Leech lattice (proved optimal) | 196,560 |

*Notes*: FCC = face-centered cubic; HCP = hexagonal close packing. Optimality proved only in dimensions 1, 2, 3, 8, and 24.

The jump in kissing number from 72 ($n = 6$) to 240 ($n = 8$) is exceptionally large -- a factor of 3.33 for adding just 2 dimensions. This reflects the special algebraic structure of $E_8$ and is not characteristic of generic dimensional increases.

---
*This paper is part of the Spectral Brand Theory research program. For the full atlas of 20+ interconnected papers, see [spectralbranding.com/atlas](https://spectralbranding.com/atlas).*
