# Spectral Metamerism in Brand Perception: Projection Bounds from High-Dimensional Geometry

**Dmitry Zharnikov**

ORCID: 0009-0000-6893-9231

Working Paper v1.1.0 — March 2026 (Updated May 2026)

https://doi.org/10.5281/zenodo.18945352

---

## Abstract

Scalar brand metrics compress high-dimensional perceptual signals into single numbers, yet the information cost of this compression has never been formally quantified. This paper introduces *spectral metamerism* to brand theory: structurally distinct brand profiles that produce identical scalar evaluations. Drawing on Spectral Brand Theory (SBT), which models brands across eight typed dimensions perceived by heterogeneous observers, the paper proves metamerism is a geometric inevitability of dimensionality reduction. Applying the Johnson-Lindenstrauss lemma, it establishes that projecting $\mathbb{R}^8$ to $\mathbb{R}^1$ requires distortion exceeding 152% for 10 brands and 198% for 50 brands. Any such projection creates a 7-dimensional null space of "invisible" brand differences. Information-theoretically, a 5-point grade captures 2.32 bits of a $\sim$20-bit spectral profile, retaining 11.6% of available information. Monte Carlo simulations confirm that 31--39% of brand pairs are metameric under random projection. The analysis yields a fundamental distinction between *rasterized* brand management -- human projection through cognitive and communicative bottlenecks -- and *vectorized* brand management, in which the full spectral profile serves as single source of truth and channel outputs are computed projections with known, bounded loss. These results provide the first formal geometric and information-theoretic lower bounds on the fidelity of scalar brand grades.

**Keywords**: spectral metamerism, Johnson-Lindenstrauss lemma, dimensionality reduction, brand perception, null space, information loss, Spectral Brand Theory

**JEL Classification**: C65, M31, C02

**MSC Classification**: 15A04, 60D05, 91B42

---

Every brand manager has experienced the unsettling discovery that two brands with identical scores on a Brand Health Tracker are, in practice, nothing alike. A luxury house scoring 78/100 on "brand strength" and a mass-market retailer scoring the same 78/100 are not, in any meaningful sense, equivalent -- yet the number says they are. The standard response is to add more metrics, more dimensions to the dashboard. The question this paper addresses is more fundamental: *how much information does a scalar grade necessarily destroy, and is there a principled lower bound on the dimensionality required to faithfully represent brand perception?*

The question is not merely academic. In industries from luxury goods to technology, brand evaluation increasingly drives capital allocation, partnership decisions, and strategic positioning. When a private equity firm evaluates acquisition targets using a single "brand value" number, or when a CMO reports brand health to the board via a composite index, the implicit assumption is that the scalar adequately represents the underlying brand reality. This paper proves that assumption is mathematically untenable.

The mechanism by which scalar grades fail has a precise analogue in physics. In color science, *metamerism* refers to the phenomenon whereby physically different spectral power distributions produce identical color percepts when projected through the three cone types of the human retina (Wyszecki & Stiles, 1982). Two fabrics that match under fluorescent light but diverge under daylight are metamers: their spectra differ, but the 3-dimensional projection (through L, M, S cone sensitivities) collapses the difference. Cohen and Kappauf's (1982) Fundamental Theorem of Colorimetry formalizes this: any projection creates a null space of "invisible" spectral differences, and metamerism is not an engineering failure but a mathematical consequence of dimensionality reduction. The decomposition into fundamental metamer and metameric black traces to the algebraic treatment of smooth metameric spectra developed by van Trigt (1990).

Spectral Brand Theory (Zharnikov, 2026a) provides the architecture for extending this insight to brand perception. SBT models a brand as an emitter of signals across eight typed dimensions -- Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal -- perceived by observers with heterogeneous salience profiles on the probability simplex $\Delta^7$. The framework's Level 1 (L1) output is the full 8-dimensional spectral profile; its Level 2 (L2) output is a scalar grade mapped to five coherence levels (A+, A-, B+, B-, C-). The transition from L1 to L2 is precisely a projection from $\mathbb{R}^8_+$ to $\mathbb{R}^1$ -- the same operation that produces metamerism in color science.

This paper supplies the foundational definition of spectral metamerism in brand perception under SBT. Downstream specializations apply this construct to LLM-mediated cohorts (Zharnikov, 2026v), creative IP repositories (Zharnikov, 2026w), behavioral specifications of AI agents (Zharnikov, 2026x), and multi-brand portfolio audits. Each retains the null-space and projection-bound structure formalized here while adapting the source space to its empirical setting.

This paper formalizes the analogy and proves three core results:

1. **Metamerism is geometrically inevitable.** For any linear projection from $\mathbb{R}^8$ to $\mathbb{R}^1$, the 7-dimensional null space guarantees the existence of brand pairs that are distant in 8D but indistinguishable in 1D, with explicitly computable bounds.

2. **Scalar grades are provably unfaithful.** The Johnson-Lindenstrauss lemma establishes that preserving pairwise distances among even 10 brands within factor $(1 \pm \epsilon)$ in one dimension requires $\epsilon > 1.52$ -- distortion exceeding 152%.

3. **The information deficit is quantifiable.** A 5-point grade captures $\log_2(5) \approx 2.32$ bits of a $\sim$20-bit profile, retaining 11.6% of available information. This is not an implementation detail but a channel capacity bound.

These results have a direct practical consequence that we develop throughout the paper: the distinction between *rasterized* and *vectorized* brand management. In rasterized mode, a brand manager serves as a human projection operator, mentally collapsing the full brand specification into simplified narratives and then attempting to re-expand them for each context -- performing exactly the lossy projection that the JL lemma warns about. In vectorized mode, the 8-dimensional spectral profile serves as the single source of truth, and channel-specific outputs are computed projections with known, bounded information loss. The shift from rasterized to vectorized is not a preference but a mathematical necessity once one accepts that brands are multi-dimensional objects living in $\mathbb{R}^8_+$.

The paper builds on the metric framework established in Zharnikov (2026d), which defined the Aitchison metric on brand signal space $\mathbb{R}^8_+$, the Fisher-Rao metric on observer weight space $\Delta^7$, and the warped product metric on the combined brand-observer space. We take these metrics as given and study what happens when the spaces they equip are projected to lower dimensions.

The remainder of the paper is organized as follows. Section 2 establishes preliminaries and notation. Section 3 formalizes spectral metamerism in brand perception. Section 4 applies the Johnson-Lindenstrauss lemma. Section 5 analyzes the null space structure. Section 6 derives information-theoretic bounds. Section 7 presents Monte Carlo verification. Section 8 develops the practical implications through the vectorized-versus-rasterized lens. Section 9 connects to MDS and survey design. Section 10 discusses limitations, and Section 11 concludes.

---

## 2. Preliminaries

### 2.1 SBT Framework and Notation

We adopt the notation and definitions of Zharnikov (2026a, 2026d). A brand's *emission profile* (spectral profile) is a vector $s = (s_1, \ldots, s_8) \in \mathbb{R}^8_+$ representing signal strength across the eight SBT dimensions:

Table 1: The Eight SBT Dimensions and Their Semantic Scope.

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

*Notes*: Dimensions follow the canonical SBT ordering established in Zharnikov (2026a). All eight dimensions are required for a complete spectral profile; omitting any dimension reduces the representation to a sub-space of $\mathbb{R}^8_+$.

An *observer spectral profile* is a weight vector $w = (w_1, \ldots, w_8) \in \Delta^7$ on the probability simplex, representing the relative salience the observer assigns to each dimension. The *cloud confidence* for observer $w$ encountering brand $s$ is the inner product $\langle s, w \rangle$, a scalar representing the observer's overall brand evaluation.

SBT's coherence assessment produces two layers of output:

- **L1 (spectral profile)**: The full 8-dimensional vector $s \in \mathbb{R}^8_+$.
- **L2 (grade)**: A scalar mapped to the five-level scale $\{A+, A-, B+, B-, C-\}$.

The L2 grade is computed from L1 via an aggregation function $\phi: \mathbb{R}^8_+ \to \mathbb{R}$, typically a weighted combination or composite score that is then binned into one of five levels. The precise form of $\phi$ varies by implementation, but in all cases it is a function from $\mathbb{R}^8$ to $\mathbb{R}^1$ -- a projection.

### 2.2 The L1/L2 Distinction as Dimensionality Reduction

The central object of study in this paper is the mapping

$$\phi: \mathbb{R}^8_+ \to \mathbb{R}$$

which takes a full spectral profile and produces a scalar grade. When $\phi$ is linear, this is a standard linear projection. When $\phi$ is nonlinear (e.g., a thresholded weighted sum), the information loss is at least as severe as in the linear case, because nonlinear maps cannot generally increase the information capacity of the output space.

For the case-study data from Zharnikov (2026a), we use the canonical emission profiles established in Zharnikov (2026d):

Table 2: Canonical Emission Profiles for Five Case-Study Brands.

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

*Notes*: Canonical profiles from Zharnikov (2026a, 2026d). L2 grades are A+, A-, B+, B-, and C- respectively. All dimension scores are on the $[1, 10]$ scale.

These brands receive L2 grades of A+, A-, B+, B-, and C- respectively. The Aitchison distances computed in Zharnikov (2026d) range from .88 (Hermès-Patagonia) to 1.76 (Hermès-Tesla), establishing that these brands are well-separated in 8D space.

### 2.3 Metrics from R1

We recall the key metrics established in Zharnikov (2026d):

- **Aitchison distance** on $\mathbb{R}^8_+$: $d_{\mathcal{B}}(s_A, s_B) = \|\text{clr}(s_A) - \text{clr}(s_B)\|_2$, where $\text{clr}_k(s) = \log(s_k / g(s))$ and $g(s)$ is the geometric mean. This metric respects the multiplicative, compositional nature of brand signal profiles.

- **Fisher-Rao distance** on $\Delta^7$: $d_{\mathcal{O}}(w_A, w_B) = 2\arccos\left(\sum_{i=1}^8 \sqrt{w_{A,i} w_{B,i}}\right)$, justified by Cencov's uniqueness theorem as the unique reparameterization-invariant metric on statistical models.

- **Observer-dependent brand distance**: $d_w(s_A, s_B) = \sqrt{\sum_k w_k (\text{clr}_k(s_A) - \text{clr}_k(s_B))^2}$, a weighted Euclidean distance in CLR coordinates that generalizes the INDSCAL model (Carroll & Chang, 1970).

---

## 3. Metamerism in Brand Perception

### 3.1 Definition

**Definition 1** (Spectral metamerism in brand perception). Two brand profiles $s_A, s_B \in \mathbb{R}^8_+$ are *metameric with respect to a projection* $\phi: \mathbb{R}^8_+ \to \mathbb{R}$ if:

$$\phi(s_A) = \phi(s_B) \quad \text{and} \quad d_{\mathcal{B}}(s_A, s_B) > 0$$

That is, two brands are metameric when they receive the same grade despite having distinct spectral profiles.

More generally, two brands are *$(\epsilon, \delta)$-metameric* if:

$$|\phi(s_A) - \phi(s_B)| < \epsilon \quad \text{and} \quad d_{\mathcal{B}}(s_A, s_B) > \delta$$

for thresholds $\epsilon$ (grade indistinguishability) and $\delta$ (profile distinctness).

The terminology is deliberately borrowed from color science, where metamerism has been studied formally since Grassmann (1853) and rigorously axiomatized by Cohen and Kappauf (1982). The analogy is structural, not metaphorical: in both cases, a high-dimensional physical stimulus is projected through a lower-dimensional sensor array, and the projection's null space creates equivalence classes of physically distinct stimuli that produce identical responses.

### 3.2 The Color Science Parallel

In color perception, the visible spectrum is a continuous function $S(\lambda)$ over wavelengths $\lambda \in [380, 780]$ nm -- effectively an infinite-dimensional object. The human visual system projects this through three cone sensitivity functions, producing a 3-dimensional tristimulus response:

$$T_j = \int_{380}^{780} S(\lambda) \bar{c}_j(\lambda) \, d\lambda, \quad j \in \{L, M, S\}$$

Cohen and Kappauf's (1982) Fundamental Theorem of Colorimetry states that any spectral distribution $S$ decomposes uniquely as $S = S^* + B$, where $S^*$ is the *fundamental metamer* (projection onto the row space of the sensitivity matrix) and $B$ is the *metameric black* (component in the null space). The metameric black represents spectral information that is invisible to human color perception -- it is "there" physically but "absent" perceptually. The algebraic structure of this decomposition, and in particular the characterization of smoothest-fit solutions in the null space, was formalized by van Trigt (1990).

In brand perception under SBT, the parallel is exact:

Table 3: Structural Analogy Between Color Science Metamerism and Brand Perception Metamerism.

| Color Science | Brand Perception (SBT) |
|---------------|----------------------|
| Spectral power distribution ($\infty$-dim) | Spectral profile ($\mathbb{R}^8_+$) |
| Cone sensitivities (3 types) | Projection function $\phi$ (1D output) |
| Tristimulus values (3D) | Scalar grade (1D) |
| Metameric pair | Brands with same grade, different profiles |
| Metameric black (null space) | "Invisible" profile differences |
| Dimension of null space: $\infty - 3$ | Dimension of null space: $8 - 1 = 7$ |

*Notes*: The analogy is structural. Color metamerism arises from projection through the three human cone types; brand metamerism arises from projection through a scalar aggregation function $\phi$. Both create null spaces of physically real but perceptually or evaluatively invisible differences.

The crucial difference is scale: in color science, the null space is infinite-dimensional, making metamerism ubiquitous. In brand perception, the null space is 7-dimensional out of 8 total -- still overwhelmingly dominant. Seven-eighths of the brand's dimensional structure is invisible to any scalar grade.

### 3.3 Constructive Example from Case Studies

Consider the Hermès-Tesla pair. In 8D Aitchison space, their distance is 1.76 -- the maximum in the case-study set. They receive grades of A+ and C- respectively, which are maximally separated on the 5-point scale. This is a case where the 1D projection happens to preserve the 8D ordering.

Now consider a constructive metameric pair. Suppose Brand X has profile $(9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5)$ -- identical to Hermès -- and Brand Y has profile $(3.0, 3.0, 9.5, 3.0, 3.0, 9.5, 3.0, 3.0)$. Brand Y is a hypothetical ideologically-driven, economically-positioned brand with minimal signal on all other dimensions. Under a simple average projection $\phi(s) = \frac{1}{8}\sum_k s_k$, Hermès scores $(9.5 + 9.0 + 7.0 + 9.0 + 8.5 + 3.0 + 9.0 + 9.5)/8 = 8.06$, while Brand Y scores $(3.0 + 3.0 + 9.5 + 3.0 + 3.0 + 9.5 + 3.0 + 3.0)/8 = 4.63$. These are far apart under this projection.

But consider the projection $\phi(s) = s_3 + s_6$ (sum of Ideological and Economic dimensions). Now Hermès scores $7.0 + 3.0 = 10.0$ and Brand Y scores $9.5 + 9.5 = 19.0$. Under a different projection, $\phi(s) = s_1 + s_8$ (Semiotic + Temporal), Hermès scores $9.5 + 9.5 = 19.0$ while Brand Y scores $3.0 + 3.0 = 6.0$. The relative ranking reverses entirely depending on the projection direction.

This is not a pathological construction. It illustrates that every brand manager who intuitively compares brands using different criteria is performing a different projection, and each projection has a different null space. The brand manager who focuses on "heritage and design" will rank brands differently from one who focuses on "value proposition and ideology" -- not because either is wrong, but because each is projecting through a different 1D subspace of $\mathbb{R}^8$. This is precisely the rasterization problem: the human operator cannot hold all 8 dimensions simultaneously and is forced to project, losing 7 dimensions of information in the process.

---

## 4. Johnson-Lindenstrauss Bounds

### 4.1 The JL Lemma

The Johnson-Lindenstrauss lemma (Johnson & Lindenstrauss, 1984) establishes the fundamental limit on distance preservation under dimensionality reduction.

**Lemma (Johnson-Lindenstrauss).** *For any $0 < \epsilon < 1$, any integer $N \geq 1$, and any set of $N$ points $V = \{x_1, \ldots, x_N\}$ in $\mathbb{R}^n$, there exists a linear map $f: \mathbb{R}^n \to \mathbb{R}^k$ with*

$$k \geq \frac{C \ln N}{\epsilon^2}$$

*such that for all $i, j$:*

$$(1 - \epsilon) \|x_i - x_j\|^2 \leq \|f(x_i) - f(x_j)\|^2 \leq (1 + \epsilon) \|x_i - x_j\|^2$$

The constant $C$ has been progressively sharpened. The Dasgupta-Gupta (2003) form gives:

$$k \geq \frac{4 \ln N}{\epsilon^2/2 - \epsilon^3/3}$$

The Larsen-Nelson (2017) tight lower bound establishes that the $\Omega(\epsilon^{-2} \log N)$ dependence is optimal: no linear map can achieve $(1 \pm \epsilon)$-distortion with fewer dimensions. Note the direction of the two results: the original Johnson-Lindenstrauss (1984) lemma is an *upper bound* -- it shows that a faithful embedding *exists* in $k \geq C\ln N / \epsilon^2$ dimensions. The Larsen-Nelson (2017) contribution is the matching *lower bound* -- showing that no linear map can achieve $(1 \pm \epsilon)$-distortion with *fewer* than $\Omega(\epsilon^{-2} \log N)$ dimensions. For our purpose (establishing that 1D scalar grades are provably unfaithful), it is the Larsen-Nelson lower bound that does the work.

A related line of work on structured random projections (Achlioptas, 2003; Kane & Nelson, 2014) shows that binary or sparse $\pm 1$ projection matrices achieve JL guarantees with the same $\Omega(\epsilon^{-2} \log N)$ dimension bound. Structured projections do not change the $k = 1$ infeasibility result derived below.

### 4.2 Application to 8D-to-1D Projection

The JL lemma is typically invoked when the source dimension $n$ is very large (e.g., $n = 10^6$) and the target dimension $k$ is much smaller but still large enough to preserve structure ($k \sim 10^2$). Our setting is unusual: the source dimension is small ($n = 8$) and the target dimension is minimal ($k = 1$). In this regime, the lemma tells us not that "reduction is possible" but rather "reduction is catastrophic."

For a fixed target dimension $k$, the minimum distortion required to accommodate $N$ points is:

$$\epsilon \geq \sqrt{\frac{\ln N}{k}}$$

**Theorem 1** (Distortion bound for scalar grades). *For any set of $N$ brand profiles in $\mathbb{R}^8$ and any linear projection $f: \mathbb{R}^8 \to \mathbb{R}^1$, the distortion parameter $\epsilon$ required for $(1 \pm \epsilon)$ distance preservation satisfies:*

$$\epsilon \geq \sqrt{\ln N}$$

*In particular:*

Table 4: Required Distortion for Scalar-Grade Projection by Competitive Set Size.

| $N$ (brands) | $\epsilon_{\min}$ | Distortion |
|:---:|:---:|:---:|
| 5 | $\geq 1.27$ | 127% |
| 10 | $\geq 1.52$ | 152% |
| 50 | $\geq 1.98$ | 198% |
| 100 | $\geq 2.15$ | 215% |
| 500 | $\geq 2.49$ | 249% |

*Notes*: Distortion values are computed as $\epsilon_{\min} = \sqrt{\ln N}$ with conservative constant $C = 1$. This is a conservative choice: the true constant from Larsen and Nelson (2017) is smaller, so the actual minimum distortion may be below $\sqrt{\ln N}$. The qualitative conclusion -- that $\epsilon$ grows without bound as $N$ increases -- holds regardless of the constant. Values apply to worst-case point configurations; structured brand manifolds may permit lower distortion for specific datasets.

*Proof.* Setting $k = 1$ in the Larsen-Nelson lower bound gives $\epsilon \geq \sqrt{C \ln N / k} = \sqrt{C \ln N}$. With the conservative constant $C = 1$, we obtain $\epsilon \geq \sqrt{\ln N}$. For $N = 10$: $\epsilon \geq \sqrt{\ln 10} \approx \sqrt{2.303} \approx 1.52$. $\square$

**Plain-English interpretation.** A distortion of $\epsilon = 1.52$ means the 1D grade can represent two brands as 252% of their true distance or as little as 0% (placing them at the same point). For 50 brands, the situation worsens to $\epsilon \approx 1.98$: the grade can inflate distances by nearly 3x or erase them entirely. A 1D grade is not a "rough approximation" of 8D distances; it is a geometrically unfaithful representation that can reverse orderings, collapse distinct brands, and separate similar ones.

A compressed-sensing reader might object that sparse brand profiles could be recovered from a scalar grade. We note three obstacles. First, no known sparsity basis for brand profiles exists in Aitchison geometry -- the CLR transform does not produce sparse representations for the kind of structured variation observed in practice (Aitchison, 1986). Second, CS recovery requires $\Omega(k \log(8/k))$ measurements (Candès & Tao, 2006; Donoho, 2006), not one; a single scalar grade provides one measurement regardless of the profile's sparsity structure. Third, even if some brand profiles were sparse in some basis, the standard grade design does not exploit that sparsity structure, so the worst-case JL lower bound applies. The null-space argument is therefore robust to sparsity assumptions.

For the practitioner performing brand evaluation -- the consultant compiling a competitive analysis, the CMO presenting to the board -- Theorem 1 quantifies a known intuition: the single number is not just imprecise but *systematically misleading*. The brand manager who converts the 8-dimensional brand specification into a slide deck is performing exactly this projection, becoming a human instance of the mapping $f: \mathbb{R}^8 \to \mathbb{R}^1$. Every time they summarize the brand as "premium" or "challenger" or "heritage," they are choosing a projection direction and discarding 7 dimensions of information. The JL lemma tells us that no choice of direction avoids the distortion.

### 4.3 Minimum Faithful Dimension

The converse question is equally important: how many dimensions are needed to faithfully represent brand relationships?

**Theorem 2** (Minimum faithful projection dimension). *To preserve pairwise Euclidean distances among $N$ brands within factor $(1 \pm \epsilon)$, the projection dimension must satisfy:*

$$k \geq \frac{4 \ln N}{\epsilon^2/2 - \epsilon^3/3}$$

*For $\epsilon = 0.3$ (30% distortion tolerance):*

Table 5: Minimum Faithful Projection Dimension at 30% Distortion Tolerance.

| $N$ (brands) | $k_{\min}$ |
|:---:|:---:|
| 5 | $\geq 179$ |
| 10 | $\geq 256$ |
| 50 | $\geq 435$ |
| 100 | $\geq 512$ |
| 500 | $\geq 691$ |

*Notes*: Values from Dasgupta-Gupta (2003) bound with $\epsilon = 0.3$. These are worst-case bounds over arbitrary point configurations. Real brand profiles constrained by market and cultural forces likely require fewer dimensions for a given distortion level.

*For $\epsilon = 0.1$ (10% distortion tolerance):*

Table 6: Minimum Faithful Projection Dimension at 10% Distortion Tolerance.

| $N$ (brands) | $k_{\min}$ |
|:---:|:---:|
| 5 | $\geq 1,380$ |
| 10 | $\geq 1,974$ |
| 50 | $\geq 3,353$ |
| 100 | $\geq 3,947$ |

*Notes*: Values from Dasgupta-Gupta (2003) bound with $\epsilon = 0.1$. The dimension requirements grow roughly as $\ln N$, so adding brands to a competitive set increases required dimensions only logarithmically.

*Proof.* Direct substitution into the Dasgupta-Gupta bound. $\square$

**Plain-English interpretation.** To maintain even 30% fidelity in a competitive set of 50 brands, you need at least 435 dimensions. SBT's 8 dimensions are vastly fewer. Does this mean the 8-dimensional model is itself too coarse? No -- because the JL bound applies to *arbitrary* point configurations where no structure is assumed. Brand profiles are not arbitrary points; they lie on a low-dimensional manifold within $\mathbb{R}^8$ constrained by market forces, production costs, cultural norms, and physical limits. The JL bound is a worst-case guarantee. The practical message is that 8 dimensions are far richer than 1 dimension, even if they may not be sufficient for worst-case distance preservation in very large brand sets. Sphere-packing analysis (Zharnikov, 2026g) establishes how many distinguishable brands fit in 8-dimensional spectral space; the present paper establishes how many of those become metameric under 1D projection -- the two analyses are duals.

The JL minimum-dimension result also illuminates why the brand manager's task is impossible to perform faithfully in human working memory. Cognitive science establishes that human working memory capacity is approximately $4 \pm 1$ chunks (Cowan, 2001), a more conservative estimate than the earlier $7 \pm 2$ figure of Miller (1956). A brand manager attempting to hold a brand's identity "in mind" for communication is projecting from 8 continuous dimensions onto roughly 3--5 discrete chunks -- an operation that the JL lemma shows cannot preserve distances for more than a handful of brands. The human operator is not failing through incompetence but through the geometry of the task itself.

**Corollary 1** (The 5-level grade as geometric inevitability). *SBT's 5-level grade (A+, A-, B+, B-, C-) is a 1D projection that necessarily loses most of the 8D structure. The loss is not a design flaw but a geometric consequence of compressing $\mathbb{R}^8$ to $\mathbb{R}^1$. No alternative grade scale (7-point, 10-point, continuous) fundamentally resolves the problem; the null space remains 7-dimensional regardless of the output scale's granularity. This result also implies that the 11.6% information retention figure (Section 6.2) is an upper bound on what any scalar grade can convey, not a property of the specific 5-point discretization.*

*Proof.* The null space dimension is $n - k = 8 - 1 = 7$ for any mapping from $\mathbb{R}^8$ to $\mathbb{R}^1$, independent of the discretization of the output. A finer output scale (e.g., $[0, 100]$) increases the bits available from $\log_2 5 \approx 2.32$ to $\log_2 100 \approx 6.64$, but the 7D null space persists. The information retention rises from 11.6% to 33.2%, but $\sim$67% of structural information remains irrecoverable. $\square$

**Remark** (Manifold restriction). The JL bounds above assume brand profiles may occupy arbitrary positions in $\mathbb{R}^8$. In practice, real brand profiles likely concentrate on a lower-dimensional manifold within $\mathbb{R}^8_+$ -- for example, if Semiotic and Cultural dimensions co-vary, the effective dimensionality may be 5--6 rather than 8. On such a manifold, the distortion bounds would be tighter (less information lost per projection) because the null space of the scalar projection intersects a smaller fraction of the data's effective support. However, the qualitative conclusion is unchanged: the 7-dimensional null space of any $\mathbb{R}^8 \to \mathbb{R}^1$ projection exists regardless of the data manifold's intrinsic dimension, and metamerism (distinct profiles mapping to the same grade) remains inevitable for any linear or scalar evaluation scheme. Nonlinear dimensionality reduction methods such as Isomap (Tenenbaum, de Silva & Langford, 2000) can preserve local geodesic structure more faithfully than linear projections, but they optimize for visualization rather than faithful distance preservation and do not recover the lost null-space dimensions for analytical purposes. A dimension-free upper bound on Lipschitz embeddings of finite metric spaces in Hilbert space is provided by Bourgain (1985), but that bound applies to the best possible embedding, not the scalar grade case where $k$ is fixed at 1.

---

## 5. Null Space Analysis

### 5.1 Dimension of the Null Space

For any linear projection $\phi: \mathbb{R}^n \to \mathbb{R}^k$, the rank-nullity theorem gives:

$$\dim(\ker(\phi)) = n - k$$

For the 8D-to-1D case:

$$\dim(\ker(\phi)) = 8 - 1 = 7$$

**Theorem 3** (Null space and inevitable metamerism). *For any linear projection $\phi: \mathbb{R}^8 \to \mathbb{R}^1$, the null space $\ker(\phi)$ is a 7-dimensional linear subspace of $\mathbb{R}^8$. For any brand profile $s \in \mathbb{R}^8_+$, the set of metameric profiles*

$$M_s = \{s' \in \mathbb{R}^8_+ : \phi(s') = \phi(s)\}$$

*is the intersection of the 7-dimensional affine subspace $s + \ker(\phi)$ with the positive orthant $\mathbb{R}^8_+$. This intersection is a convex set of dimension at most 7. Moreover, for any $\delta > 0$, there exist metameric pairs $(s_A, s_B)$ with $\|s_A - s_B\| > \delta$ and $|\phi(s_A) - \phi(s_B)| = 0$.*

*Proof.* The preimage $\phi^{-1}(\phi(s)) = s + \ker(\phi)$ is a 7-dimensional affine subspace of $\mathbb{R}^8$. The positive orthant $\mathbb{R}^8_+$ is a convex cone. The intersection of the affine subspace with the convex cone is convex. Its dimension is at most $\min(7, 8) = 7$ and generically equals 7, since for any $s$ in the interior of $\mathbb{R}^8_+$, the affine subspace intersects the orthant in a neighborhood of $s$.

For the second statement: let $v \in \ker(\phi)$ be any nonzero null-space vector. For $s$ in the interior of $\mathbb{R}^8_+$ and sufficiently small $t > 0$, the profile $s + tv$ also lies in $\mathbb{R}^8_+$ (by openness of the interior). Since $\phi(s + tv) = \phi(s) + t\phi(v) = \phi(s) + 0 = \phi(s)$, the pair $(s, s+tv)$ is metameric with distance $\|s - (s+tv)\| = t\|v\|$. By choosing $t > \delta/\|v\|$ (while remaining in $\mathbb{R}^8_+$), we achieve metameric separation exceeding $\delta$. $\square$

**Plain-English interpretation.** For every brand that receives a given grade, there is a 7-dimensional family of other brands that would receive the same grade despite having completely different spectral profiles. This is not a sparse set of edge cases -- it is a 7-dimensional continuum. Among 8 independent dimensions of brand identity, the grade captures the variation along exactly one direction and is blind to the other seven.

### 5.2 Constructive Metameric Pairs

We can construct explicit metameric pairs from the case-study data. Let $\phi(s) = \mathbf{u}^T \text{clr}(s)$ for some unit vector $\mathbf{u} \in \mathbb{R}^8$. Any perturbation $\delta$ in $\ker(\phi)$ (i.e., $\mathbf{u}^T \delta = 0$) produces a metameric profile: $\phi(s + \delta) = \phi(s)$.

Consider Hermès with $\text{clr}(s_H) \approx (0.227, 0.173, -0.078, 0.173, 0.116, -0.926, 0.173, 0.227)$. Take the simplest projection direction $\mathbf{u} = (1, 1, 1, 1, 1, 1, 1, 1)/\sqrt{8}$ (the equal-weight direction). Then the null space consists of all vectors orthogonal to $\mathbf{1}$ -- that is, all vectors whose components sum to zero.

The perturbation $\delta = (0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5, -0.5)$ sums to zero and thus lies in $\ker(\phi)$. The profile $\text{clr}(s_H) + \delta$ would score identically to Hermès under the equal-weight grade but would represent a brand with dramatically amplified Semiotic, Narrative, Social, and Cultural signals and suppressed Ideological, Experiential, Economic, and Temporal signals -- a qualitatively different brand architecture.

The Aitchison distance between the original and perturbed profiles is $\|\delta\|_2 = \sqrt{8 \cdot 0.25} = \sqrt{2} \approx 1.41$, which is comparable to the Hermès-Tesla distance of 1.76. Brands nearly as different as the most separated pair in the case-study set can share the same scalar grade.

This construction makes vivid the rasterization problem. When a brand manager tells a design team "we're an A+ brand like Hermès," they are communicating the 1D projection (the grade) and implicitly asking the team to reconstruct the 7 null-space dimensions from context, intuition, and prior experience. Different team members will reconstruct different null-space components, producing divergent interpretations that are all consistent with the stated grade. The vectorized alternative -- communicating the full 8D spectral profile -- eliminates this ambiguity by specifying the exact point in $\mathbb{R}^8_+$ rather than the equivalence class in $\mathbb{R}^1$.

### 5.3 Observer-Dependent Null Spaces

In SBT, the projection $\phi$ is not arbitrary -- it is determined by the observer's weight profile $w \in \Delta^7$. For a fixed observer $w$, the scalar evaluation is $\phi_w(s) = \langle w, \text{clr}(s) \rangle$, and the null space is:

$$\ker(\phi_w) = \{ \delta \in \mathbb{R}^8 : \langle w, \delta \rangle = 0 \}$$

Different observers have different null spaces. An aesthete observer $w_\alpha = (0.25, 0.15, 0.05, 0.20, 0.10, 0.05, 0.15, 0.05)$ is blind to perturbations orthogonal to $w_\alpha$; a pragmatist observer $w_\beta = (0.05, 0.05, 0.10, 0.15, 0.05, 0.35, 0.05, 0.20)$ is blind to a different 7D subspace. Brands that are metameric for observer $\alpha$ may be sharply distinguished by observer $\beta$, and vice versa.

**Proposition 1** (Null space complementarity). *For two observers $w_A, w_B \in \Delta^7_\circ$ with $w_A \neq w_B$, the intersection $\ker(\phi_{w_A}) \cap \ker(\phi_{w_B})$ has dimension 6 (generically). A brand pair that is metameric for both observers simultaneously must have its profile difference in this 6-dimensional intersection. The combined observations of two distinct observers reduce the effective null space from 7D to 6D.*

*Proof.* Each $\ker(\phi_w)$ is a hyperplane in $\mathbb{R}^8$ (dimension 7). Two distinct hyperplanes in $\mathbb{R}^8$ generically intersect in a subspace of dimension $7 + 7 - 8 = 6$. On $\Delta^7$, two observers with $w_A \neq w_B$ necessarily have non-proportional weight vectors (the simplex normalization forces this), so the generic case is the universal case here; the dimension-6 bound holds for all pairs of distinct observers. $\square$

This has a striking implication for perceptual cohort formation: observers who share similar weight profiles (close on $\Delta^7$ in the Fisher-Rao metric) also share nearly identical null spaces, and therefore agree on which brands are "equivalent" and which are "different." Disagreement between cohorts about brand quality is not noise -- it is the geometrically inevitable consequence of projecting through different subspaces (Zharnikov, 2026f).

Eight observers with weight vectors spanning the 7-dimensional affine subspace of $\Delta^7$ would reduce the effective null space to at most 1 dimension -- nearly, but not entirely, eliminating metameric ambiguity. Full null-space elimination would require observations from outside the simplex (i.e., observers who weight dimensions negatively or super-unitarily), which is outside the SBT behavioral model. This is the mathematical basis for multi-stakeholder brand assessment: diversity of perspective is not merely desirable but geometrically necessary for faithful brand representation, even if complete elimination of metamerism is not achievable within the simplex constraint.

*Falsification*: Proposition 1 is falsified if two observers with statistically distinct weight profiles (Fisher-Rao distance $> \delta$) produce identical metameric pair classifications across a set of $\geq 20$ brand profiles -- implying their null spaces are not generically distinct.

---

## 6. Information-Theoretic Bounds

### 6.1 Variance Retention

For a set of brand profiles in $\mathbb{R}^8$ with independent, equal-variance dimensions, the optimal 1D projection (the first principal component) captures exactly $1/8 = 12.5\%$ of the total variance.

**Theorem 4** (Variance retention bound). *For $n$ independent, identically-distributed dimensions projected to $k$ dimensions, the maximum fraction of variance retained is $k/n$. For $n = 8$, $k = 1$:*

$$\frac{\text{Var}(\phi(s))}{\text{Var}(s)} \leq \frac{1}{8} = 12.5\%$$

*The remaining $87.5\%$ of variance is lost -- distributed across the 7 null-space dimensions. The variance bound transfers to the Aitchison setting via the CLR isometry; see Appendix A.2 and Zharnikov (2026d) for details.*

*Proof.* Under the independence assumption, the covariance matrix $\Sigma = \sigma^2 I_8$ has 8 equal eigenvalues. The optimal $k$-dimensional projection (PCA) captures the top $k$ eigenvalues, for a total of $k\sigma^2 / 8\sigma^2 = k/8$. For $k = 1$, this is $1/8 = 12.5\%$. $\square$

**Remark.** When dimensions are correlated (as they may be for real brand profiles -- e.g., Semiotic and Cultural signals may co-vary for heritage luxury brands), the first principal component may capture more than $12.5\%$ of variance. But this improvement comes at a cost: the projection direction that maximizes captured variance may not align with the semantically meaningful brand quality axis. PCA maximizes variance, not interpretability. A first principal component that combines "Semiotic minus Economic plus Temporal" is statistically optimal but practically uninterpretable to a brand manager. This is another manifestation of the rasterization trap: optimizing the projection for statistical fidelity produces an axis that no human can intuit, while optimizing for human interpretability (e.g., "overall quality") produces a statistically suboptimal projection.

### 6.2 Grade Information Capacity

Theorem 4 bounded variance retention (a geometric quantity); Theorem 5 below bounds Shannon information capacity (a channel-theoretic quantity). The two quantities address different facets of fidelity and need not coincide.

**Theorem 5** (Information-theoretic bound). *A discrete grade scale with $L$ levels has channel capacity:*

$$C_{\text{grade}} = \log_2 L$$

*An 8-dimensional continuous profile with $B$ bits of resolution per dimension has total information content:*

$$I_{\text{profile}} = n \cdot B$$

*The information retention ratio is:*

$$\rho = \frac{C_{\text{grade}}}{I_{\text{profile}}} = \frac{\log_2 L}{n \cdot B}$$

*For SBT's 5-point grade scale ($L = 5$) and a profile with $B = 2.5$ bits per dimension ($\approx 6$ distinguishable levels per dimension, conservative for a $[1, 10]$ scale):*

$$\rho = \frac{\log_2 5}{8 \times 2.5} = \frac{2.32}{20} = 11.6\%$$

*Proof.* The capacity of a discrete channel with $L$ symbols is $\log_2 L$ bits, achieved by the uniform distribution over levels. The information content of the continuous profile is the sum of per-dimension entropies. With $B = 2.5$ bits per dimension (corresponding to approximately 6 reliably distinguishable levels on a $[1, 10]$ scale), the total is $8 \times 2.5 = 20$ bits. The ratio follows directly. $\square$

**Plain-English interpretation.** The 5-point grade captures 2.32 bits of a 20-bit profile. This means 88.4% of the brand's identity -- as encoded in its 8-dimensional spectral profile -- is invisible to the grade. The grade can distinguish among $2^{2.32} = 5$ brand states; the full profile can distinguish among $2^{20} \approx 10^6$ states. The grade compresses a million-state space into five bins. This is an information loss ratio that should give pause to anyone using scalar grades for consequential decisions.

The information-theoretic bound has a direct consequence for the vectorized-versus-rasterized distinction. In rasterized mode, the brand manager communicates through a channel of approximately $\log_2 5 \approx 2.32$ bits per grade utterance (or somewhat more if they use verbal qualifiers, but bounded by human communication bandwidth). In vectorized mode, the full 20-bit specification is transmitted directly -- as a data structure, not a narrative. The bandwidth advantage of vectorized transmission is nearly 9x, and this advantage scales with the complexity of the brand.

### 6.3 Rate-Distortion Perspective

Under the rate-distortion framework (Shannon, 1948; Berger, 1971), for a Gaussian source $X \sim \mathcal{N}(0, \Sigma)$ in $\mathbb{R}^8$ with equal eigenvalues $\lambda_1 = \cdots = \lambda_8 = \sigma^2$, the rate-distortion function is:

$$R(D) = \sum_{i=1}^{8} \max\left(0, \frac{1}{2} \log_2 \frac{\lambda_i}{\theta}\right)$$

where $\theta$ is set by the distortion constraint. For a 1D representation (rate $= \frac{1}{2}\log_2(\sigma^2/\theta)$ for the retained component), the expected distortion is:

$$D = \sum_{i=2}^{8} \lambda_i = 7\sigma^2$$

which is $7/8 = 87.5\%$ of the total variance -- converging with the PCA analysis of Section 6.1. The "reverse water-filling" algorithm allocates all available rate to the single largest eigenvalue direction and ignores the remaining 7 dimensions entirely.

*Note on distributional assumption.* The Gaussian source is adopted as an analytical tractability assumption. A formally correct rate-distortion analysis would require log-normal or truncated-Gaussian sources to respect the positivity constraint of $\mathbb{R}^8_+$. The qualitative conclusion -- that 1D projection incurs $7\sigma^2$ expected distortion -- holds for any source with equal marginal variances, including log-normal after reparameterization in CLR coordinates.

---

## 7. Monte Carlo Verification

### 7.1 Simulation Design

To verify the theoretical bounds, we conduct Monte Carlo simulations using the companion code documented in `R2_R3_computations.py` (Zharnikov, 2026e). The simulation:

1. Generates $N = 50$ random brand profiles in $\mathbb{R}^8_+$ (log-normal distribution, $\mu = 0.5$, $\sigma = 0.5$, ensuring positivity).
2. Draws a random unit projection vector $\mathbf{u} \in \mathbb{R}^8$ (Gaussian, normalized).
3. Projects all profiles onto the 1D subspace defined by $\mathbf{u}$.
4. Computes all $\binom{50}{2} = 1225$ pairwise distances in both 8D (Euclidean on log-profiles) and 1D.
5. Counts *metameric pairs*: brand pairs with $d_{8D} > 1.0$ but $d_{1D} < 0.3$.

The log-normal distribution ($\mu = 0.5$, $\sigma = 0.5$) is a convenient positive distribution that produces realistic variation in signal strength (geometric mean $\approx e^{0.5} \approx 1.65$, coefficient of variation $\approx 50\%$). The sensitivity of the metameric fraction to alternative generating distributions -- e.g., uniform on $[1, 10]^8$ or empirically calibrated from the five case-study brands -- is a direction for future work. The qualitative conclusion that a substantial fraction of pairs are metameric is robust to the specific distribution as long as profiles are spread over the ambient space.

### 7.2 Results

Three independent trials (different random seeds):

Table 7: Monte Carlo Metameric Pair Frequency Across Three Independent Trials.

| Trial | Metameric Pairs | Fraction | Total Pairs |
|:---:|:---:|:---:|:---:|
| 1 | 474 | 38.7% | 1225 |
| 2 | 388 | 31.7% | 1225 |
| 3 | 374 | 30.5% | 1225 |

*Notes*: Brand profiles drawn from log-normal distribution ($\mu = 0.5$, $\sigma = 0.5$) on $\mathbb{R}^8_+$. Metameric threshold: $d_{8D} > 1.0$ and $d_{1D} < 0.3$ under a uniformly random projection direction. The metameric fraction is stable at 31--39% across trials; sensitivity analysis shows robustness to threshold variation within $\pm 20\%$.

**Result.** Across three trials, 31--39% of brand pairs that are well-separated in 8D become indistinguishable in 1D under a single random projection. This is consistent with the theoretical prediction: a 7-dimensional null space "hides" most of the 8D structure, producing metameric collisions for a substantial fraction of all pairs.

### 7.3 Interpretation

The simulation confirms that metamerism is not a rare pathology but a prevalent phenomenon. In a competitive set of 50 brands, roughly one-third of all pairwise comparisons are metameric under any given scalar grade. The specific pairs that are metameric depend on the projection direction (i.e., the weighting scheme used to compute the grade), but the *fraction* of metameric pairs is stable at $\sim$30--40% regardless of the direction.

Note that the 31--39% estimate is for uniformly random projection directions. Real observer populations are not uniformly distributed on $\Delta^7$ but cluster into cohorts (Zharnikov, 2026f). The metameric fraction under a clustered observer ensemble could differ from this estimate; measuring this sensitivity is a direction for future work. Similarly, purpose-designed composites (e.g., equal-weight averages, first principal components) may have lower metameric fractions for specific brand populations where the dominant variance aligns with the projection. The null-space and channel-capacity results of Sections 5 and 6 are projection-independent; only the Monte Carlo estimate is direction-specific.

This has immediate practical consequences. When a brand tracking study reports that Brand A and Brand B have "similar" scores, there is approximately a one-in-three chance that the similarity is metameric -- an artifact of the projection rather than a genuine similarity in brand structure. To determine whether a similar score reflects true proximity or metameric coincidence, one must examine the full spectral profiles. The scalar grade alone cannot distinguish the two cases.

For the brand manager interpreting tracking data, this means that vectorized diagnosis -- examining the 8D profile differences directly -- is not a luxury but a necessity for any pair comparison flagged by the scalar grade. The 1D grade can serve as a screening tool (brands with very different grades are almost certainly far apart in 8D), but grade similarity is geometrically ambiguous.

---

## 8. From Rasterized to Vectorized Brand Management

### 8.1 The Rasterization Problem

Section 1 introduced the rasterized/vectorized distinction; the results of Sections 4--7 now permit a formal characterization. Traditional brand management is *rasterized*: the term is borrowed from computer graphics, where a rasterized image is a pixel grid -- a fixed-resolution projection of an underlying geometric description. Once rasterized, information about the original geometry is lost.

In brand management, the rasterization process works as follows:

1. **The brand specification exists** as a high-dimensional object -- whether formalized as an SBT spectral profile in $\mathbb{R}^8_+$ or informally as "the brand identity." Even brands without explicit frameworks have objective multi-dimensional signal structures that could, in principle, be measured.

2. **The brand manager projects** this object into communicable form: decks, guidelines, brand books, verbal briefings. Each communication act is a projection -- a mapping from $\mathbb{R}^8$ to a lower-dimensional channel. The brand book is a 2D static document; the verbal briefing is a sequential 1D narrative; the brand pyramid is a hierarchical reduction to a single apex concept.

3. **The recipients reconstruct** from the projected form. A designer receiving a brief must reconstruct the 8D brand intent from a 1D or 2D communication. Different recipients reconstruct different null-space components, producing divergent interpretations that are all consistent with the communicated projection but inconsistent with each other -- and potentially inconsistent with the original intent.

The JL bounds tell us the distortion is at least 152% for 10-brand competitive sets. The null-space analysis tells us 7 out of 8 dimensions are invisible. The information-theoretic bounds tell us 88.4% of the specification is lost. These are not arguments for better brand books; they are proofs that the rasterized paradigm is informationally inadequate.

The brand manager operating in rasterized mode is, mathematically, a "prophet" or "evangelist" -- a person who tries to convert the single source of truth into signs. This is an inevitably lossy process because human working memory and communication bandwidth are finite-dimensional projections. Moreover, the brand manager's own observer profile $w \in \Delta^7$ introduces systematic bias: the dimensions they attend to most heavily are the dimensions they communicate most faithfully, while the dimensions they de-weight are precisely those that disappear into their personal null space.

### 8.2 The Vectorized Alternative

Vectorized brand management retains the full-dimensional specification as the single source of truth (SSOT) and produces channel-specific outputs as computed projections with known, bounded information loss.

**Brand audits become vector comparisons.** Instead of subjective "does this feel on-brand?" judgments, compute $d_{\mathcal{B}}(s_{\text{intended}}, s_{\text{observed}})$ using the Aitchison metric and compare to a significance threshold. The threshold can be derived from concentration bounds (Zharnikov, 2026d, Section 6): the expected squared distance between random profiles on $\Delta^7$ is $7/36$, providing a null-model baseline. A measured distance significantly above this baseline indicates genuine misalignment; a distance near the baseline may be noise.

**Channel briefs become subspace specifications.** Instead of "make it feel premium," specify: "For the Instagram channel, project onto the $[s_1, s_5, s_7]$ subspace (Semiotic, Social, Cultural) with minimum signal strengths $(0.7, 0.5, 0.6)$." This is a mathematically precise instruction that can be verified by measuring the output's spectral profile on the relevant dimensions. Different channels may require different subspace projections, but each projection is derived from the same 8D SSOT, with the null-space dimensions explicitly identified.

**The brand manager's role transforms.** In rasterized mode, the brand manager is the "keeper of the vision" -- a single point of failure whose departure can destabilize brand coherence because the vision exists primarily in their mental model. In vectorized mode, the brand manager is the "custodian of the vector" -- responsible for maintaining, updating, and validating the 8D specification, but not required to be the sole channel through which brand identity is communicated. The specification is transferable, auditable, and computable. The custodian's role is quality control: ensuring that channel projections remain faithful to the source vector, detecting dimensional drift before it compounds, and updating the specification when strategic repositioning is intended.

### 8.3 When Scalar Grades Suffice

The case against scalar grades is not absolute. Theorem 1 establishes worst-case bounds; there are scenarios where 1D projections are adequate:

1. **Coarse screening.** When the goal is to partition a large set into "investigate further" and "ignore," a scalar grade with $\epsilon > 1$ may still correctly separate the top and bottom quartiles. The distortion affects mid-range brands most severely.

2. **Univariate dominance.** When one dimension overwhelmingly determines the outcome of interest (e.g., Economic positioning for price-elasticity analysis), the natural projection onto that dimension captures most of the relevant variance. The JL bound is a worst case over arbitrary point configurations; structured configurations may permit lower distortion.

3. **Communication to non-specialist audiences.** A board-level report may require a scalar grade for executive communication, provided the audience understands it is a lossy summary. The information-theoretic bound of 11.6% retention should be disclosed as a caveat.

The 31--39% metameric fraction is for uniformly random projection directions; equal-weight or PCA-based composites may achieve lower metameric fractions for specific brand populations where dominant variance aligns with the projection direction. This does not alter the null-space argument, which is projection-independent.

The vectorized approach does not eliminate scalar grades; it contextualizes them. In a vectorized system, the grade is a *derived output* with known properties -- known projection direction, known null space, known information loss -- rather than a primary measurement that obscures its own limitations. This is the fundamental difference: in rasterized management, the grade is the reality; in vectorized management, the grade is a view of the reality.

---

## 9. Connection to MDS and Survey Design

### 9.1 MDS Dimensionality Selection

Multidimensional scaling (MDS) has been the dominant geometric method in marketing for half a century (Torgerson, 1958; Kruskal, 1964; Bijmolt & Wedel, 1999). The standard practice is to choose the MDS dimensionality by inspecting a "stress plot" -- stress as a function of dimensions -- and selecting the "elbow" point where additional dimensions provide diminishing returns.

The JL framework provides a principled alternative. Given $N$ brands and a desired distortion tolerance $\epsilon$, Theorem 2 gives the minimum dimension for faithful distance preservation. For marketing applications with $N = 50$ brands and $\epsilon = 0.3$:

$$k_{\min} = \frac{4 \ln 50}{0.3^2/2 - 0.3^3/3} \approx 435$$

This exceeds SBT's 8 dimensions by a large factor, but the comparison is misleading. MDS dimensions are empirically extracted and may not correspond to meaningful attributes; SBT dimensions are theoretically motivated and semantically interpretable. The JL bound applies to arbitrary point configurations; SBT profiles are constrained by the structure of the eight typed dimensions. The relevant question for MDS practitioners is not "how many dimensions does the JL lemma require?" but rather "is my chosen dimensionality capturing the theoretically relevant structure?"

SBT's contribution to the MDS dimensionality debate is to provide a theoretical target: 8 dimensions, with known semantic content, chosen on theoretical grounds rather than empirical stress minimization. The metamerism analysis shows that anything fewer than 8 loses identifiable structure; the JL analysis shows that even 8 dimensions require care when projecting further.

### 9.2 Survey Instrument Design

The information-theoretic bounds have direct implications for survey design. A survey instrument that measures brand perception on a single composite scale (e.g., "overall brand strength on a 1-10 scale") is performing the 8D-to-1D projection at the data collection stage, before any analysis can recover the lost structure. Wedel and Kannan (2016), surveying the state of marketing analytics in data-rich environments, observe that composite brand metrics remain the default in practice despite their known limitations -- a pattern this paper's formal bounds help explain: if the fidelity ceiling of any scalar grade is 11.6%, deploying richer data collection instruments requires a parallel shift to vectorized analytics, not merely higher-resolution scalar measurement.

The minimum survey instrument for capturing SBT's 8-dimensional structure requires at least one reliable item per dimension. With $B \approx 2.5$ bits per item (a 6-point scale), an 8-item instrument captures $\sim$20 bits -- the full information content of the spectral profile. A single-item instrument captures $\sim$2.5 bits, losing $87.5\%$ of the available information.

The JL perspective also implies that *composite indices* (such as those constructed by averaging multiple items) are not necessarily superior to single items, unless the averaging scheme preserves the geometric structure. An unweighted average of 8 dimension scores projects onto the $(1,1,\ldots,1)/\sqrt{8}$ direction, which is optimal only if all dimensions contribute equally to the phenomenon of interest -- an assumption that SBT's observer-heterogeneity framework explicitly rejects. Observers with different weight profiles would require different projection directions to minimize distortion for their specific perspective. A survey that forces all observers through the same composite index is imposing a single null space on a population with heterogeneous null spaces -- a form of measurement-induced metamerism.

---

## 10. Discussion and Limitations

### 10.1 The Role of Nonlinearity

Our analysis focuses on linear projections. Real brand evaluation may involve nonlinear aggregation (e.g., "a single very low dimension score overrides other dimensions" -- the identity-gate mechanism in SBT). Nonlinear projections from $\mathbb{R}^8$ to $\mathbb{R}^1$ can, in principle, capture more structure than linear projections -- but they cannot exceed the channel capacity bound of $\log_2 L$ bits for an $L$-level output. The information-theoretic results (Section 6) are independent of linearity.

### 10.2 Source Dimension Assumptions

We assume $n = 8$ throughout. If the "true" dimensionality of brand perception is less than 8 (e.g., because some SBT dimensions are highly correlated), the null-space dimension is correspondingly reduced. Conversely, if brand perception is richer than 8 dimensions (as suggested by the fine-grained distinctions within individual dimensions), the metamerism problem is even more severe. The 8-dimensional model represents SBT's current theoretical commitment, and the results scale straightforwardly with the assumed dimensionality. The sphere-packing duality (Zharnikov, 2026g) provides the complementary bound: that paper establishes how many distinguishable brands fit in 8-dimensional spectral space, while the present paper establishes how many of those become metameric under 1D projection.

### 10.3 Empirical Validation

The case-study profiles used in Section 2.2 are illustrative, derived from qualitative assessment rather than empirical measurement. Empirical validation would require (a) survey instruments capturing 8-dimensional brand perception, (b) scalar grade instruments administered to the same respondents, and (c) direct measurement of metameric pair frequency. This is a natural direction for future work; the present paper establishes the theoretical bounds that such empirical work would test. The concentration-of-measure argument explaining why the metameric fraction is direction-stable at $\sim$30--40% is developed formally in Zharnikov (2026f). Empirical applications to AI-mediated brand perception are reported in Zharnikov (2026v) and Zharnikov (2026x).

### 10.4 Relationship to Factor Analysis and PCA

PCA and factor analysis are data-dependent dimensionality reduction methods that choose the projection to maximize captured variance. The JL analysis is data-independent -- it provides worst-case guarantees over all possible point configurations. The two approaches are complementary: PCA tells you the best projection for a specific dataset; JL tells you the worst-case loss for any dataset. For brand management, the PCA approach risks overfitting to a specific competitive set, while the JL approach provides robust bounds that hold regardless of the specific brands being analyzed. The possibility of partially compensating for projection loss through prior knowledge of the perceptual space has a precedent in color science: Maloney (1986) showed that surface spectral reflectance functions can be approximately recovered from tristimulus values using a small number of basis functions, because natural reflectances occupy a low-dimensional subspace. Whether analogous priors exist for brand profiles -- allowing partial recovery of null-space dimensions from contextual cues -- is a direction for future work.

### 10.5 Beyond Linear Projections

Modern nonlinear dimensionality reduction methods (t-SNE, UMAP; see Tenenbaum, de Silva & Langford, 2000, for the foundational isomap approach) can embed high-dimensional data in lower dimensions while preserving local structure better than linear methods. However, these methods optimize for visualization, not for faithful distance preservation. A t-SNE embedding of 8D brand profiles in 2D may produce visually appealing clusters, but the distances in the embedding are not proportional to the Aitchison distances in the original space. For analytical purposes -- computing brand distances, detecting metamerism, measuring coherence -- the original 8D representation remains necessary.

### 10.6 Observer-Dependent Metamerism

This paper treats the projection $\phi$ as a fixed function. In full SBT, the projection is observer-dependent: different observers weight dimensions differently, producing different null spaces (Section 5.3). The full metamerism analysis for the warped product manifold (Zharnikov, 2026d) would require studying how the null space structure varies across the observer space $\Delta^7$, a direction we leave for future work. Proposition 1 provides the first step: two distinct observers reduce the effective null space from 7D to 6D, and the general case of $m$ observers with linearly independent weight profiles reduces it to $(8 - m)$ dimensions. The cohort-clustering implications of observer-dependent null spaces are analyzed in Zharnikov (2026f).

---

## 11. Conclusion

This paper has established that spectral metamerism -- the phenomenon whereby structurally distinct brand profiles produce identical scalar evaluations -- is not a measurement artifact but a geometric inevitability. Three independent lines of argument converge on this conclusion.

Together these results formalize the distinction between rasterized and vectorized brand management. The rasterized paradigm -- where human operators project high-dimensional brand identity through their own cognitive bottlenecks -- is provably lossy, with quantifiable bounds on the information loss. The vectorized paradigm -- where the full spectral profile serves as the single source of truth and channel outputs are computed projections -- preserves the complete brand specification and produces derivatives with known, bounded distortion.

SBT's 8-dimensional spectral profile is therefore not optional complexity. It is the minimum representation required to avoid the metameric collapse that scalar grades inevitably produce. The practical recommendation is clear: use scalar grades for coarse screening and communication, but conduct all analytical work -- brand audits, competitive analysis, consistency monitoring, strategic positioning -- in the full 8-dimensional space where metamerism cannot hide structural differences.

Future work includes empirical measurement of metameric pair frequency in real brand data (testing the 31--39% prediction in Zharnikov, 2026v and Zharnikov, 2026x), extension to the warped product manifold (observer-dependent metamerism bounds in Zharnikov, 2026f), and application to organizational specification through OrgSchema Theory (Zharnikov, 2026i), where the 48-dimensional specification space makes the metamerism problem dramatically more severe. We are not aware of published work that has previously established formal distortion bounds for scalar brand grades or quantified the metameric fraction in competitive brand sets.

---

## Acknowledgments

AI assistants (Claude Opus 4.7, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

---

## References

Achlioptas, D. (2003). Database-friendly random projections: Johnson-Lindenstrauss with binary coins. *Journal of Computer and System Sciences*, 66(4), 671--687.

Aaker, D. A. (1991). *Managing Brand Equity*. Free Press.

Aaker, J. L. (1997). Dimensions of brand personality. *Journal of Marketing Research*, 34(3), 347--356.

Aitchison, J. (1986). *The Statistical Analysis of Compositional Data*. Chapman & Hall.

Amari, S.-i. (2016). *Information Geometry and Its Applications*. Springer.

Berger, T. (1971). *Rate Distortion Theory: A Mathematical Basis for Data Compression*. Prentice-Hall.

Bijmolt, T. H. A., & Wedel, M. (1999). A comparison of multidimensional scaling methods for perceptual mapping. *Journal of Marketing Research*, 36(2), 277--285. https://doi.org/10.1177/002224379903600211

Borg, I., & Groenen, P. J. F. (2005). *Modern Multidimensional Scaling* (2nd ed.). Springer.

Bourgain, J. (1985). On Lipschitz embedding of finite metric spaces in Hilbert space. *Israel Journal of Mathematics*, 52(1-2), 46--52.

Brand Finance. (2025). *Global 500 Brand Valuation Report*. Brand Finance.

Busemeyer, J. R., & Bruza, P. D. (2012). *Quantum Models of Cognition and Decision*. Cambridge University Press.

Candès, E. J., & Tao, T. (2006). Near-optimal signal recovery from random projections: Universal encoding strategies? *IEEE Transactions on Information Theory*, 52(12), 5406--5425. https://doi.org/10.1109/TIT.2006.885507

Carroll, J. D., & Chang, J.-J. (1970). Analysis of individual differences in multidimensional scaling via an N-way generalization of "Eckart-Young" decomposition. *Psychometrika*, 35(3), 283--319.

Cohen, J. B., & Kappauf, W. E. (1982). Metameric color stimuli, fundamental metamers, and Wyszecki's metameric blacks. *American Journal of Psychology*, 95(4), 537--564.

Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*, 24(1), 87--114.

Dasgupta, S., & Gupta, A. (2003). An elementary proof of a theorem of Johnson and Lindenstrauss. *Random Structures & Algorithms*, 22(1), 60--65.

DeSarbo, W. S., Kim, Y., Choi, S. C., & Spaulding, M. (2002). A gravity-based multidimensional scaling model for deriving spatial structures underlying consumer preference/choice judgments. *Journal of Consumer Research*, 29(1), 91--100.

Donoho, D. L. (2006). Compressed sensing. *IEEE Transactions on Information Theory*, 52(4), 1289--1306.

Gardenfors, P. (2000). *Conceptual Spaces: The Geometry of Thought*. MIT Press.

Grassmann, H. (1853). Zur Theorie der Farbenmischung. *Annalen der Physik*, 165(5), 69--84.

Johnson, W. B., & Lindenstrauss, J. (1984). Extensions of Lipschitz mappings into a Hilbert space. *Contemporary Mathematics*, 26, 189--206.

Kane, D. M., & Nelson, J. (2014). Sparser Johnson-Lindenstrauss transforms. *Journal of the ACM*, 61(1), 1--23.

Kapferer, J.-N. (2008). *The New Strategic Brand Management* (4th ed.). Kogan Page.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1--22.

Kruskal, J. B. (1964). Multidimensional scaling by optimizing goodness of fit to a nonmetric hypothesis. *Psychometrika*, 29(1), 1--27.

Lancaster, K. J. (1966). A new approach to consumer theory. *Journal of Political Economy*, 74(2), 132--157.

Larsen, K. G., & Nelson, J. (2017). Optimality of the Johnson-Lindenstrauss lemma. In *Proceedings of the 58th Annual IEEE Symposium on Foundations of Computer Science (FOCS)* (pp. 633--638).

Maloney, L. T. (1986). Evaluation of linear models of surface spectral reflectance with small numbers of parameters. *Journal of the Optical Society of America A*, 3(10), 1673--1683.

Miller, G. A. (1956). The magical number seven, plus or minus two: Some limits on our capacity for processing information. *Psychological Review*, 63(2), 81--97.

Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379--423.

Shepard, R. N. (1987). Toward a universal law of generalization for psychological science. *Science*, 237(4820), 1317--1323.

Tenenbaum, J. B., de Silva, V., & Langford, J. C. (2000). A global geometric framework for nonlinear dimensionality reduction. *Science*, 290(5500), 2319--2323. https://doi.org/10.1126/science.290.5500.2319

Torgerson, W. S. (1958). *Theory and Methods of Scaling*. Wiley.

van Trigt, C. (1990). Smoothest-fit solution and the fundamental metamers. *Color Research & Application*, 15(2), 68--75.

Wedel, M., & Kannan, P. K. (2016). Marketing analytics for data-rich environments. *Journal of Marketing*, 80(6), 97--121. https://doi.org/10.1509/jm.15.0413

Wyszecki, G., & Stiles, W. S. (1982). *Color Science: Concepts and Methods, Quantitative Data and Formulae* (2nd ed.). Wiley.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026c). Geometric approaches to brand perception: A critical survey and research agenda. Working Paper. https://doi.org/10.5281/zenodo.18945217

Zharnikov, D. (2026d). Brand space geometry: A formal metric for multi-dimensional brand perception. Working Paper. https://doi.org/10.5281/zenodo.18945295

Zharnikov, D. (2026f). Cohort boundaries in high-dimensional perception space: A concentration of measure analysis. Working Paper. https://doi.org/10.5281/zenodo.18945477

Zharnikov, D. (2026g). How many brands can a market hold? Sphere packing bounds for multi-dimensional positioning. Working Paper. https://doi.org/10.5281/zenodo.18945522

Zharnikov, D. (2026i). The Organizational Schema Theory: Test-driven business design. Working Paper. https://doi.org/10.5281/zenodo.18946043

Zharnikov, D. (2026v). Dimensional collapse in AI-mediated brand perception: Large language models as metameric observers. Working Paper. https://doi.org/10.5281/zenodo.19422427

Zharnikov, D. (2026w). Canon as repository: A specification-driven architecture for transmedia intellectual property. Working Paper. https://doi.org/10.5281/zenodo.19355800

Zharnikov, D. (2026x). AI-native brand identity: From visual recognition to cryptographic verification. Working Paper. https://doi.org/10.5281/zenodo.19391476

---

## Mathematical Appendix

### A.1 Proof Details for Theorem 1

The distortion bound derives from the Larsen-Nelson (2017) tight lower bound for the Johnson-Lindenstrauss lemma. For a set of $N$ points in $\mathbb{R}^n$ and any linear map $f: \mathbb{R}^n \to \mathbb{R}^k$, the distortion parameter $\epsilon$ satisfying:

$$(1 - \epsilon)\|x_i - x_j\|^2 \leq \|f(x_i) - f(x_j)\|^2 \leq (1 + \epsilon)\|x_i - x_j\|^2 \quad \forall i,j$$

must satisfy $k = \Omega(\epsilon^{-2} \log N)$. Rearranging for fixed $k = 1$:

$$1 = \Omega(\epsilon^{-2} \log N) \implies \epsilon^2 = \Omega(\log N) \implies \epsilon = \Omega(\sqrt{\log N})$$

Using the specific constant from the conservative form: $\epsilon \geq \sqrt{\ln N}$, where $\ln$ denotes the natural logarithm.

### A.2 Relationship Between Aitchison and Euclidean Null Spaces

The null-space analysis in Section 5 is stated for Euclidean distances on raw profiles. Under the Aitchison metric (which operates on centered log-ratio transforms), the null space of a linear projection $\phi(\text{clr}(s)) = \mathbf{u}^T \text{clr}(s)$ is the set:

$$\ker(\phi \circ \text{clr}) = \{s \in \mathbb{R}^8_+ : \mathbf{u}^T \text{clr}(s) = c\}$$

for some constant $c$. This is a level set of a linear function in CLR coordinates, which corresponds to a curved surface in the original $\mathbb{R}^8_+$ space (because the CLR transform is logarithmic). The dimension of this level set is still 7 (by the implicit function theorem, since $\text{clr}$ is a smooth diffeomorphism from $\mathbb{R}^8_+$ to its image), so the null-space analysis carries through with the Aitchison geometry.

### A.3 Monte Carlo Methodology

The simulation generates brand profiles as $s_k = \exp(X_k)$ where $X_k \sim \mathcal{N}(0.5, 0.25)$ independently for each dimension. This ensures $s_k \in \mathbb{R}^8_+$ with a log-normal distribution that produces realistic variation in signal strength (geometric mean $\approx e^{0.5} \approx 1.65$, coefficient of variation $\approx 50\%$).

The random projection vector $\mathbf{u}$ is drawn from $\mathcal{N}(0, I_8)$ and normalized to unit length. By rotational invariance of the Gaussian distribution, this produces a uniformly random direction on $S^7$.

A pair $(s_i, s_j)$ is classified as metameric if $d_{8D}(s_i, s_j) > 1.0$ (substantial separation in 8D) and $d_{1D}(s_i, s_j) < 0.3$ (near-indistinguishable in 1D). The thresholds are chosen to identify cases of clear 8D separation that are collapsed by the projection; sensitivity analysis shows the metameric fraction is robust to threshold variation within $\pm 20\%$.

### A.4 Summary of Numerical Results

For reference, the key computed values used throughout the paper:

Table 8: Summary of Key Computed Values Cited Throughout the Paper.

| Quantity | Value | Section |
|----------|-------|---------|
| Null space dimension ($\mathbb{R}^8 \to \mathbb{R}^1$) | 7 | 5.1 |
| Variance retained (1D, independent dims) | 12.5% | 6.1 |
| Required distortion: $N=10$ | $\epsilon \geq 1.52$ (152%) | 4.2 |
| Required distortion: $N=50$ | $\epsilon \geq 1.98$ (198%) | 4.2 |
| Grade information capacity (5-point) | 2.32 bits | 6.2 |
| Full profile information (8D) | $\sim$20 bits | 6.2 |
| Information retention ratio | 11.6% | 6.2 |
| Metameric pair frequency (Monte Carlo) | 31--39% | 7.2 |
| JL minimum $k$ for $\epsilon=0.3$, $N=10$ | $\geq 256$ | 4.3 |
| JL minimum $k$ for $\epsilon=0.3$, $N=50$ | $\geq 435$ | 4.3 |

*Notes*: All distortion values computed with conservative constant $C = 1$; see Theorem 1 notes and Appendix A.1 for the Larsen-Nelson lower bound context. Cross-reference Sections 4--7 for derivations.
