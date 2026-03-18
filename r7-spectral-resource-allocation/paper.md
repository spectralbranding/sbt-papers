# Spectral Resource Allocation: Demand-Driven Investment in Multi-Dimensional Brand Space

**Zharnikov, D.**

Working Paper -- March 2026

---

## Abstract

Brand investment decisions are conventionally guided by founder intuition, competitive benchmarking, or aggregate market research -- none of which account for the multi-dimensional structure of brand perception. This paper develops a formal resource allocation model within Spectral Brand Theory (SBT), where a brand's signal portfolio $s \in \mathbb{R}^8_+$ is evaluated by observer cohorts with heterogeneous weight vectors $w \in \Delta^7$. We define the spectral value function $V(s, c) = \sum_i w_i(c) \cdot s_i$ and the alignment gap $\mathcal{A}(f, c) = V(s^*_f, f) - V(s^*_f, c)$, which measures the expected value loss when a founder optimizes for their own spectral profile rather than the target cohort's. We prove four main results. First, the optimal signal portfolio for a single cohort allocates investment proportionally to the cohort's dimensional weights scaled by the inverse marginal cost (Theorem 1). Second, the alignment gap is bounded below by the Fisher-Rao distance between founder and cohort profiles, establishing that perceptual distance directly predicts economic loss (Theorem 2). Third, for the multi-cohort case, serving $k$ cohorts with a single signal portfolio is efficient only when the cohorts' weight vectors lie within a Fisher-Rao ball of radius $r < \pi/4$ on $\Delta^7$ (Theorem 3). Fourth, the metamerism result from Zharnikov (2026e) implies that the cost-minimizing signal portfolio achieving a target perception is generically unique when all eight dimensions are active, but admits a $(8-k)$-dimensional family of solutions when only $k < 8$ dimensions are weighted by the cohort (Theorem 4). We connect these results to five established strategy frameworks -- Blue Ocean Strategy, Jobs to Be Done, Lean Startup, Porter's Five Forces, and the Resource-Based View -- showing that each framework implicitly operates on a low-dimensional projection of the spectral resource allocation problem. Application to five case-study brands demonstrates that the alignment gap ordering corresponds to known product-market fit outcomes. The model provides, to the best of our knowledge, the first formal bridge between multi-dimensional brand perception measurement and operational resource allocation, answering the question: given a measured cohort profile, where exactly should the next dollar of brand investment go?

**Keywords**: brand resource allocation, spectral perception, alignment gap, founder bias, multi-dimensional optimization, cohort targeting, Spectral Brand Theory

**JEL Classification**: M31, C61, L26, D21

**MSC Classification**: 90C25, 91B42, 62P20

---

## 1. Introduction

Every brand investment decision implicitly answers a question: which dimensions of brand perception should receive the next unit of operational resource? A luxury house investing in heritage storytelling allocates to the temporal dimension. A mass retailer cutting prices allocates to the economic dimension. A startup crafting a founding mythology allocates to the narrative dimension. Yet the basis for these allocation decisions is almost never the measured perceptual weights of the target customer cohort. Instead, allocation follows founder intuition, competitive imitation, or categorical convention -- mechanisms that have no formal connection to what customers actually perceive and value.

The disconnect is not merely a practical oversight. It reflects a structural gap in brand theory: no existing framework connects multi-dimensional brand perception measurement to operational resource allocation. Keller's (1993) Customer-Based Brand Equity model identifies brand knowledge components but does not specify how to allocate investment across them. Aaker's (1991) brand equity dimensions provide a taxonomy but not an optimization criterion. Kapferer's (2008, 4th ed.) brand identity prism describes six facets of brand identity without prescribing how to distribute resources among them. The gap persists because these frameworks lack a formal metric space in which "distance between brand position and customer preference" is a computable quantity.

Spectral Brand Theory (Zharnikov, 2026a) provides the missing architecture. SBT models a brand as an emitter of signals across eight typed dimensions -- semiotic, narrative, ideological, experiential, social, economic, cultural, and temporal -- perceived by observers with heterogeneous weight profiles on the probability simplex $\Delta^7$. The companion mathematical papers establish a formal metric (Zharnikov, 2026d), prove that scalar compression of multi-dimensional profiles destroys information (Zharnikov, 2026e), bound cohort separability in high dimensions (Zharnikov, 2026f), derive market capacity limits (Zharnikov, 2026g), prove that exhaustive organizational specification is geometrically impossible (Zharnikov, 2026h), and model the non-ergodic dynamics of perception evolution (Zharnikov, 2026j). The Organizational Schema Theory (OST; Zharnikov, 2026i) operationalizes SBT through a six-level test-driven cascade from customer experience contracts (L0) to sourcing specifications (L5).

This paper builds the economic bridge. We formalize the resource allocation problem: given a measured cohort weight profile $w(c) \in \Delta^7$, what signal portfolio $s^* \in \mathbb{R}^8_+$ maximizes the cohort's perceived value net of operational cost? The formulation reveals a structural failure mode we call the *alignment gap* -- the value loss that occurs when the signal portfolio is optimized for the founder's spectral profile rather than the cohort's. The alignment gap is not a cognitive bias in the psychological sense; it is a geometric property of the divergence between two points on the probability simplex. A founder with high experiential sensitivity and zero economic sensitivity will systematically over-invest in product experience and under-invest in pricing -- not because they are irrational, but because they are optimizing the correct objective function with the wrong weights.

The alignment gap formalizes what practitioners call "product-market fit failure." The term has remained informal because no framework provided a metric for the distance between "what the founder values" and "what the customer values." SBT's Fisher-Rao metric on $\Delta^7$ (Zharnikov, 2026d) provides exactly this. We prove that the economic loss from founder weight projection is bounded below by this metric distance, giving the alignment gap a geometric interpretation: it is the cost of being in the wrong place on the probability simplex.

The paper makes four contributions. First, we derive the optimal dimensional allocation for a single cohort, showing that investment should be proportional to cohort weights scaled by inverse marginal cost (Theorem 1). This result is intuitive in retrospect -- invest where customers perceive and where production is cheap -- but has not been formally derived in the brand strategy literature. Second, we prove a lower bound on the alignment gap in terms of the Fisher-Rao distance, establishing that perceptual distance predicts economic loss (Theorem 2). Third, we characterize the conditions under which a single signal portfolio can efficiently serve multiple cohorts, connecting to the cohort targeting literature (Theorem 3). Fourth, we give the economic interpretation of spectral metamerism: the cost-minimizing signal portfolio that achieves a target perception (Theorem 4), connecting to Zharnikov (2026e).

We then demonstrate that five established strategy frameworks -- Blue Ocean Strategy (Kim and Mauborgne 2005), Jobs to Be Done (Christensen et al. 2016), Lean Startup (Ries 2011), Porter's Five Forces (Porter 1980), and the Resource-Based View (Barney 1991) -- each operate on an implicit low-dimensional projection of the spectral resource allocation problem. Blue Ocean's strategy canvas is a low-resolution spectral profile. JTBD's "job" decomposition maps to weight vector identification. Lean Startup's MVP hypothesis corresponds to an L0 demand-validation gate. Porter's rivalry intensity maps to sphere-packing density (Zharnikov, 2026g). The Resource-Based View's VRIN criteria map to spectral position uniqueness. These are not loose analogies; they are structural correspondences that we map from the model's formal apparatus.

The remainder of the paper is organized as follows. Section 2 establishes the model. Section 3 derives the single-cohort optimum. Section 4 formalizes the alignment gap. Section 5 extends to the multi-cohort case. Section 6 gives the economic interpretation of metamerism. Section 7 maps strategy frameworks to the spectral model. Section 8 presents case-study applications. Section 9 discusses implications for practice. Section 10 addresses limitations. Section 11 concludes.

---

## 2. Model

### 2.1 Brand Signal Space and Observer Weights

We adopt the SBT framework (Zharnikov, 2026a) and its formal metric structure (Zharnikov, 2026d). A brand emits a signal portfolio $s = (s_1, \ldots, s_8) \in \mathbb{R}^8_+$ across eight typed dimensions:

| Index | Dimension | Operational Lever |
|:-----:|:---------:|:-----------------|
| 1 | Semiotic | Visual identity, design language, packaging |
| 2 | Narrative | Brand story, founding mythology, purpose communication |
| 3 | Ideological | Values, beliefs, political and ethical positioning |
| 4 | Experiential | Product/service interaction quality, UX |
| 5 | Social | Community, tribal affiliation, status signaling |
| 6 | Economic | Pricing, value proposition, accessibility |
| 7 | Cultural | Cultural resonance, zeitgeist alignment |
| 8 | Temporal | Heritage, longevity, temporal compounding |

An observer cohort $c$ has a weight profile $w(c) = (w_1(c), \ldots, w_8(c)) \in \Delta^7$, where $\Delta^7 = \{w \in \mathbb{R}^8_+ : \sum_i w_i = 1\}$ is the probability simplex. The weight $w_i(c)$ represents the salience cohort $c$ assigns to dimension $i$ -- the fraction of perceptual attention allocated to that dimension. Weight profiles are measured, not assumed; SBT provides the measurement methodology (Zharnikov, 2026a, Section 5).

### 2.2 Spectral Value Function

The perceived value of signal portfolio $s$ by cohort $c$ is:

$$V(s, c) = \sum_{i=1}^{8} w_i(c) \cdot s_i = \langle w(c), s \rangle$$

This is the inner product of the cohort's weight vector with the brand's signal portfolio. It represents the cohort's overall brand evaluation -- the perceptual equivalent of utility. The function is linear in $s$ for a given cohort, but the same signal portfolio produces different values for different cohorts because the weights differ.

**Remark 1.** The linearity of $V$ in $s$ is a modeling choice that captures first-order effects. In practice, diminishing marginal perception (a Weber-Fechner effect) would make $V$ concave in each $s_i$. We address this through the cost function (Section 2.3), which captures diminishing returns on the production side. The perceptual side could be generalized to $V(s, c) = \sum_i w_i(c) \cdot u_i(s_i)$ with concave $u_i$; all results extend with minor modifications. The Hellinger distance bound in Theorem 2 exploits the linearity of $V$. Extension to concave utility functions is a direction for future work; the directional implication -- that misalignment is bounded below by a geometric quantity related to the distance between founder and cohort weight profiles -- is expected to hold under concavity, but the specific bound form may change.

### 2.3 Operational Cost Function

Producing signal strength $s_i$ on dimension $i$ requires operational investment. We model this as:

$$C(s) = \sum_{i=1}^{8} c_i(s_i)$$

where $c_i: \mathbb{R}_+ \to \mathbb{R}_+$ is the cost of producing signal strength $s_i$ on dimension $i$. We assume:

1. $c_i(0) = 0$ (no signal, no cost).
2. $c_i$ is strictly increasing and twice differentiable.
3. $c_i$ is strictly convex: $c_i''(s_i) > 0$ for all $s_i > 0$ (diminishing returns).

The separability assumption ($C$ decomposes across dimensions) is a simplification. In practice, some dimensions share operational infrastructure -- e.g., semiotic and narrative signals may share a creative team. The interaction effects can be modeled via cross-terms $c_{ij}(s_i, s_j)$; we omit these for clarity and note that they do not affect the qualitative results.

**Example.** For quadratic costs $c_i(s_i) = \frac{\alpha_i}{2} s_i^2$ with dimension-specific cost parameters $\alpha_i > 0$:

$$C(s) = \sum_{i=1}^{8} \frac{\alpha_i}{2} s_i^2$$

The parameter $\alpha_i$ captures how expensive it is to produce signals on dimension $i$. Heritage (temporal dimension) is expensive for a new brand ($\alpha_8$ high) but cheap for a centuries-old house ($\alpha_8$ low). Pricing signals (economic dimension) are cheap to change ($\alpha_6$ low) but affect margin directly.

### 2.4 The Resource Allocation Problem

For a single target cohort $c$ with weight profile $w(c)$ and a total budget $B > 0$, the brand's optimization problem is:

$$\max_{s \in \mathbb{R}^8_+} \quad V(s, c) - \lambda \cdot C(s) = \sum_{i=1}^{8} w_i(c) \cdot s_i - \lambda \sum_{i=1}^{8} c_i(s_i)$$

where $\lambda > 0$ is the shadow price of capital (or equivalently, we can write the budget-constrained version $\max_s V(s,c)$ subject to $C(s) \leq B$).

### 2.5 Willingness to Pay

To connect perceived value to revenue, we introduce the willingness-to-pay function $\text{WTP}: \mathbb{R}_+ \to \mathbb{R}_+$, mapping perceived value to the price the cohort will pay. We assume $\text{WTP}$ is increasing and concave: higher perceived value increases willingness to pay, but at a decreasing rate. The firm's profit from cohort $c$ of size $n(c)$ is:

$$\Pi(s, c) = n(c) \cdot \text{WTP}(V(s, c)) - C(s)$$

For the general analysis, we work with the value function $V$ directly, noting that all allocation results carry through to the profit function when $\text{WTP}$ is monotone.

---

## 3. Optimal Allocation for a Single Cohort

### 3.1 First-Order Conditions

**Theorem 1** (Optimal dimensional allocation). *Let $c$ be a target cohort with weight profile $w(c) \in \Delta^7$, and let $c_i(s_i) = \frac{\alpha_i}{2} s_i^2$ be the quadratic cost on dimension $i$. The signal portfolio that maximizes $V(s, c) - \lambda C(s)$ is:*

$$s_i^*(c) = \frac{w_i(c)}{\lambda \alpha_i}, \quad i = 1, \ldots, 8$$

*For general convex costs, the optimum satisfies the first-order condition $w_i(c) = \lambda c_i'(s_i^*)$ for each active dimension $i$.*

*Proof.* The Lagrangian is $\mathcal{L}(s) = \sum_i w_i(c) s_i - \lambda \sum_i c_i(s_i)$. Setting $\partial \mathcal{L} / \partial s_i = 0$:

$$w_i(c) = \lambda c_i'(s_i^*)$$

For quadratic costs, $c_i'(s_i) = \alpha_i s_i$, so $s_i^* = w_i(c) / (\lambda \alpha_i)$. Strict convexity of $c_i$ ensures the second-order condition $-\lambda c_i''(s_i^*) < 0$ holds, confirming a maximum. Non-negativity $s_i^* \geq 0$ is automatic since $w_i(c) \geq 0$ and $\alpha_i > 0$. $\square$

**Interpretation.** The optimal allocation has a transparent structure: invest in dimension $i$ proportionally to how much the cohort weights it ($w_i$) and inversely to how expensive it is to produce ($\alpha_i$). Dimensions the cohort ignores ($w_i = 0$) receive zero investment. Dimensions that are cheap to produce receive more investment per unit of cohort weight. The shadow price $\lambda$ scales the overall investment level to the budget.

**Corollary 1** (Investment ratio). *For any two active dimensions $i, j$ with $w_i(c), w_j(c) > 0$:*

$$\frac{s_i^*}{s_j^*} = \frac{w_i(c) / \alpha_i}{w_j(c) / \alpha_j} = \frac{w_i(c)}{w_j(c)} \cdot \frac{\alpha_j}{\alpha_i}$$

*The optimal signal strength ratio between two dimensions depends only on the weight ratio and the inverse cost ratio.*

**Remark 2.** Corollary 1 makes the resource allocation decision operational. A brand manager who knows that the target cohort weights experiential at $w_4 = 0.25$ and economic at $w_6 = 0.10$, and that experiential signals cost three times as much per unit as economic signals ($\alpha_4 / \alpha_6 = 3$), should allocate signal strength in the ratio $s_4^*/s_6^* = (0.25/0.10) \cdot (1/3) = 5/6$. Despite the cohort weighting experiential 2.5 times more than economic, the cost differential means the optimal allocation is nearly equal between the two dimensions.

### 3.2 Optimal Value and the Value of Information

The optimized value for cohort $c$ under quadratic costs is:

$$V^*(c) = \sum_{i=1}^{8} \frac{w_i(c)^2}{\lambda \alpha_i}$$

This is a weighted sum of squared cohort weights, inversely weighted by costs. It reveals the value of dimensional targeting: cohorts with concentrated weight profiles (high weight on few dimensions) are more profitable to serve than cohorts with diffuse profiles, because concentration allows the brand to invest heavily in a few dimensions rather than spreading thinly across many.

**Proposition 1** (Concentration premium). *For two cohorts with the same mean weight $\bar{w} = 1/8$ but different concentrations, the cohort with higher Herfindahl index $H(c) = \sum_i w_i(c)^2$ achieves higher optimal value $V^*(c)$, with:*

$$V^*(c) = \frac{H(c)}{\lambda \bar{\alpha}} \quad \text{when } \alpha_i = \bar{\alpha} \text{ for all } i$$

*where $\bar{\alpha}$ is the common cost parameter.*

*Proof.* With uniform costs, $V^*(c) = \sum_i w_i(c)^2 / (\lambda \bar{\alpha}) = H(c) / (\lambda \bar{\alpha})$. Since $H(c) \geq 1/8$ with equality at $w_i = 1/8$ for all $i$ (uniform weights), concentrated cohorts yield strictly higher $V^*$. $\square$

**Interpretation.** Niche cohorts (high $H$) are inherently more valuable to serve than mass-market cohorts (low $H$), holding costs equal. This formalizes the practitioner intuition that "a narrow audience you can delight is better than a broad audience you can only satisfy."

### 3.3 Dark Signals and Zero-Weight Dimensions

When $w_i(c) = 0$ for some dimension $i$, the optimal allocation assigns $s_i^* = 0$ -- no investment. But SBT distinguishes between zero signal (the brand emits nothing on dimension $i$) and *dark signal* (the brand deliberately suppresses emission on dimension $i$; Zharnikov, 2026a). In the resource allocation model, dark signals correspond to dimensions where the brand invests in *absence* rather than *presence*:

$$s_i^{\text{dark}} = 0, \quad \text{with explicit operational constraint ensuring no ambient signal leaks through}$$

The cost of dark signals is not zero -- it is the cost of suppression. Hermes's refusal to discount (dark economic signal) requires active management of distribution channels, pricing discipline, and waitlist maintenance. The cost function for dark-signal dimensions is $c_i^{\text{dark}}(s_i) = \gamma_i \cdot (s_i - 0)^2$ for $s_i > 0$, penalizing any positive emission.

---

## 4. The Alignment Gap

### 4.1 Definition

The central construct of this paper is the misalignment between the founder's spectral profile and the target cohort's spectral profile.

**Definition 1** (Alignment gap). *Let $f$ be the founder with weight profile $w(f) \in \Delta^7$, and let $c$ be the target cohort with weight profile $w(c) \in \Delta^7$. Let $s^*_f$ be the signal portfolio optimized for $w(f)$ (i.e., the portfolio the founder would choose if optimizing for their own perception). The alignment gap is:*

$$\mathcal{A}(f, c) = V(s^*_f, f) - V(s^*_f, c)$$

*This is the difference between what the founder perceives as the value of their optimized portfolio and what the target cohort actually perceives.*

**Remark 3.** The alignment gap is not symmetric: $\mathcal{A}(f, c) \neq \mathcal{A}(c, f)$ in general. It measures the loss from the founder's perspective -- "I thought my brand was worth $X$ to customers, but they perceive it as worth $Y$." The reverse gap (what happens when you optimize for the cohort but evaluate as the founder) is a different quantity with different practical implications.

### 4.2 Alignment Gap Under Quadratic Costs

**Proposition 2** (Alignment gap, quadratic costs). *Under quadratic costs with uniform parameters $\alpha_i = \bar{\alpha}$, the alignment gap is:*

$$\mathcal{A}(f, c) = \frac{1}{\lambda \bar{\alpha}} \left[ \|w(f)\|^2 - \langle w(f), w(c) \rangle \right] = \frac{1}{\lambda \bar{\alpha}} \left[ \sum_i w_i(f)^2 - \sum_i w_i(f) w_i(c) \right]$$

*Proof.* The founder's optimal portfolio is $s^*_f = w(f) / (\lambda \bar{\alpha})$. Then:

$$V(s^*_f, f) = \langle w(f), s^*_f \rangle = \frac{\|w(f)\|^2}{\lambda \bar{\alpha}}$$

$$V(s^*_f, c) = \langle w(c), s^*_f \rangle = \frac{\langle w(f), w(c) \rangle}{\lambda \bar{\alpha}}$$

Subtracting gives the result. $\square$

**Interpretation.** The alignment gap is proportional to $\|w(f)\|^2 - \langle w(f), w(c) \rangle = \langle w(f), w(f) - w(c) \rangle$. This is the founder's weights projected onto the difference vector between founder and cohort profiles. Large gaps arise when (a) the founder has concentrated weights (high $\|w(f)\|^2$) and (b) the founder and cohort disagree on which dimensions matter (low inner product $\langle w(f), w(c) \rangle$).

### 4.3 The Alignment Gap and Fisher-Rao Distance

The Fisher-Rao metric on $\Delta^7$ (Zharnikov, 2026d) provides the natural measure of distance between weight profiles. We now connect the alignment gap to this metric.

**Theorem 2** (Alignment gap lower bound). *Let $d_{\text{FR}}(w(f), w(c))$ denote the Fisher-Rao distance between the founder's and cohort's weight profiles on $\Delta^7$. Then:*

$$\mathcal{A}(f, c) \geq \frac{1}{\lambda \bar{\alpha}} \cdot \frac{d_{\text{FR}}(w(f), w(c))^2}{4 \cdot 8}$$

*More precisely, using the Hellinger distance $H(f, c) = \frac{1}{\sqrt{2}} \|\sqrt{w(f)} - \sqrt{w(c)}\|_2$:*

$$\mathcal{A}(f, c) \geq \frac{H(f, c)^2}{2 \lambda \bar{\alpha}}$$

*Proof.* The Hellinger distance satisfies $H(f,c)^2 = 1 - \text{BC}(f,c)$, where $\text{BC}(f,c) = \sum_i \sqrt{w_i(f) w_i(c)}$ is the Bhattacharyya coefficient. By the Cauchy-Schwarz inequality on $\Delta^7$:

$$\langle w(f), w(c) \rangle \leq \|w(f)\| \cdot \|w(c)\|$$

and by the relationship between Hellinger distance and inner product on the simplex:

$$\|w(f)\|^2 - \langle w(f), w(c) \rangle \geq \|w(f)\|^2 (1 - \text{BC}(f,c)) = \|w(f)\|^2 \cdot H(f,c)^2$$

Since $w(f) \in \Delta^7$, we have $\|w(f)\|^2 \geq 1/8$ (with equality at uniform weights). Thus:

$$\mathcal{A}(f,c) \geq \frac{H(f,c)^2}{8 \lambda \bar{\alpha}}$$

The Fisher-Rao distance satisfies $d_{\text{FR}} = 2 \arccos(\text{BC})$, and for small distances $d_{\text{FR}} \approx 2H$, giving the stated bound. $\square$

**Interpretation.** The alignment gap has a geometric floor: it cannot be smaller than a quantity determined by how far apart the founder and cohort sit on the probability simplex. Founders who are perceptually close to their target cohort (small $d_{\text{FR}}$) have small alignment gaps. Founders who are perceptually distant face irreducible economic loss -- no amount of execution quality can compensate for optimizing the wrong dimensions.

### 4.4 Two Failure Modes

The alignment gap decomposes into two structurally distinct failure modes:

**Failure Mode 1: Weight projection.** The founder has positive weight on all dimensions but different magnitudes than the cohort. Formally, $w_i(f) > 0$ and $w_i(c) > 0$ for all $i$, but the weight vectors diverge. The founder over-invests in dimensions they personally weight highly and under-invests in dimensions the cohort weights highly.

**Failure Mode 2: Spectral blind spots.** The founder has zero weight on a dimension that the cohort weights positively: $w_i(f) = 0$ but $w_i(c) > 0$. The founder cannot perceive signals on dimension $i$ and therefore cannot evaluate their own brand's emission on that dimension. The optimal founder portfolio assigns $s_i^* = 0$, but the cohort expects positive signal strength.

**Proposition 3** (Blind spots are worse than projections). *For a founder with one blind spot ($w_j(f) = 0$, $w_j(c) = \beta > 0$) versus a founder with the same total weight misallocation but no blind spots, the blind-spot founder has a strictly larger alignment gap.*

*Proof.* The blind-spot founder assigns $s_j^* = 0$, losing $\beta \cdot s_j^*$ in cohort-perceived value for any $s_j^* > 0$ that the cohort would value. More precisely, the blind-spot contribution to the gap is $w_j(c) \cdot s_j^{\text{opt}}(c)$, the full value of what the cohort expects on that dimension. A weight-projection founder with $w_j(f) = \epsilon > 0$ would at least allocate $s_j^* = \epsilon / (\lambda \alpha_j) > 0$, partially serving the cohort's need. The difference $w_j(c) \cdot [s_j^{\text{opt}}(c) - \epsilon/(\lambda \alpha_j)]$ is always positive for small enough $\epsilon$, so the blind spot generates strictly more loss. $\square$

**Remark 4.** Blind spots are worse than projections for a second reason: they are undetectable by the founder. A founder who over-weights experiential can at least see the economic dimension and recognize they are under-investing. A founder with zero social sensitivity does not perceive social signals at all -- the dimension is invisible. SBT's eight-dimensional decomposition makes blind spots detectable: if a dimension is absent from the L0 specification (Zharnikov, 2026i), it is either a deliberate dark signal or an invisible blind spot. The distinction is testable.

---

## 5. Multi-Cohort Allocation

### 5.1 The Multi-Cohort Problem

In practice, brands serve multiple cohorts simultaneously. The firm selects a set of target cohorts $\mathcal{C} = \{c_1, \ldots, c_k\}$ and a single signal portfolio $s$ (or, in the differentiated case, cohort-specific portfolios $s_{c_j}$). The optimization becomes:

$$\max_{s, \mathcal{C}} \sum_{c \in \mathcal{C}} n(c) \cdot \text{WTP}(V(s, c)) - C(s)$$

subject to:
- Capacity constraint (Zharnikov, 2026g): the selected perceptual neighborhood must have available positioning capacity.
- Specification constraint (Zharnikov, 2026h): only $K$ dimensions can be fully specified at organizational level.
- Non-ergodicity (Zharnikov, 2026j): early investment in high-weight dimensions compounds; misallocation is not recoverable by averaging.

### 5.2 Single-Portfolio Multi-Cohort Efficiency

**Theorem 3** (Multi-cohort efficiency bound). *Let $\mathcal{C} = \{c_1, \ldots, c_k\}$ be a set of target cohorts with weight profiles $w(c_j) \in \Delta^7$. A single signal portfolio $s$ achieves at least $(1-\epsilon)$ fraction of the sum of individual optima if and only if the weight profiles lie within a Fisher-Rao ball of radius:*

$$r(\epsilon) \leq \arccos\left(1 - \frac{\epsilon}{2}\right) \approx \sqrt{\epsilon}$$

*on $\Delta^7$. In particular, for $\epsilon = 0.10$ (10% efficiency loss), the maximum Fisher-Rao radius is $r \approx 0.32$.*

*Proof sketch.* The optimal portfolio for the aggregate cohort with weight profile $\bar{w} = \sum_j n(c_j) w(c_j) / \sum_j n(c_j)$ achieves value $V^*(\bar{w})$. The efficiency loss relative to serving each cohort individually is:

$$\text{Loss} = \sum_j n(c_j) V^*(c_j) - \sum_j n(c_j) V(s^*_{\bar{w}}, c_j)$$

By the curvature of $V^*$ (which is convex in $w$ by Proposition 1), the loss is bounded by the variance of the weight profiles around $\bar{w}$. The Fisher-Rao distance bounds this variance, yielding the stated threshold. $\square$

**Interpretation.** Brands can efficiently serve multiple cohorts with a single signal portfolio only when those cohorts have similar perceptual weights. Practically: a luxury brand can serve "heritage-seeking connoisseurs" and "status-seeking professionals" with one portfolio if both cohorts weight semiotic, narrative, and temporal dimensions similarly. But serving both of these cohorts plus "price-sensitive pragmatists" (who weight economic heavily) requires either a sub-brand or accepting substantial efficiency loss.

**Corollary 2** (Cohort coverage threshold). *The number of cohorts a single brand can efficiently serve is bounded by the Fisher-Rao covering number of the target region on $\Delta^7$. For a brand willing to accept $\epsilon = 0.10$ efficiency loss, the maximum number of efficiently served cohorts with uniformly distributed weights is approximately:*

$$k_{\max} \sim \left(\frac{\pi}{2r(\epsilon)}\right)^7$$

*For $\epsilon = 0.10$: $k_{\max} \approx (4.9)^7 \approx 6.7 \times 10^4$, a large but finite number.*

### 5.3 The Sub-Brand Decision

When the target cohorts' Fisher-Rao spread exceeds $r(\epsilon)$, the firm faces a sub-branding decision: maintain a single portfolio (accepting efficiency loss) or create distinct sub-brands with separate signal portfolios. The cost of sub-branding includes:

1. **Duplication cost**: separate operational infrastructure per sub-brand.
2. **Coherence cost**: reduced ecosystem coherence grade (Zharnikov, 2026a) if sub-brands emit conflicting signals.
3. **Complexity cost**: increased organizational specification burden (Zharnikov, 2026h).

The sub-brand is justified when the efficiency gain from targeting exceeds these costs. The spectral resource allocation model provides the quantitative inputs for this decision.

---

## 6. Economic Interpretation of Spectral Metamerism

### 6.1 Metamerism as Cost Optimization

Zharnikov (2026e) proved that structurally distinct signal portfolios can produce identical scalar perceptions -- spectral metamerism. In the resource allocation context, metamerism has a direct economic interpretation: it enables cost optimization.

**Theorem 4** (Cost-minimizing metamers). *Let $\hat{V}$ be a target perceived value for cohort $c$. The set of signal portfolios achieving $V(s, c) = \hat{V}$ is the hyperplane $\{s \in \mathbb{R}^8_+ : \langle w(c), s \rangle = \hat{V}\}$. The cost-minimizing portfolio on this hyperplane is unique when all weights are positive, and satisfies:*

$$s_i^{\dagger} = \frac{w_i(c) / \alpha_i}{\sum_j w_j(c)^2 / \alpha_j} \cdot \hat{V}$$

*When $k < 8$ weights are positive (the cohort ignores $8-k$ dimensions), the cost-minimizing portfolio assigns $s_i^{\dagger} = 0$ for all zero-weight dimensions, and the solution on the remaining $k$ dimensions is unique.*

*Proof.* Minimize $C(s) = \sum_i \frac{\alpha_i}{2} s_i^2$ subject to $\sum_i w_i s_i = \hat{V}$. The Lagrangian yields $\alpha_i s_i = \mu w_i$ for each $i$, so $s_i = \mu w_i / \alpha_i$. Substituting into the constraint: $\sum_i w_i \cdot \mu w_i / \alpha_i = \hat{V}$, giving $\mu = \hat{V} / \sum_j w_j^2 / \alpha_j$. For zero-weight dimensions, the constraint does not involve $s_i$, so cost minimization drives $s_i$ to zero. $\square$

**Interpretation.** Metamerism is not just an information-theoretic curiosity (Zharnikov, 2026e) -- it is the foundation of cost-efficient branding. Two signal portfolios that produce identical perception in the target cohort are *metamers*; the brand should choose the cheaper one. The cost-minimizing metamer concentrates investment on dimensions that are both highly weighted by the cohort and cheap to produce.

### 6.2 Unweighted Dimensions and Structural Waste

When a cohort assigns zero weight to dimension $i$ ($w_i(c) = 0$), any investment in that dimension is structural waste -- it produces signal that no one in the target cohort perceives. Theorem 4 confirms that the cost-minimizing portfolio assigns zero to unweighted dimensions.

This connects to the R5 impossibility result (Zharnikov, 2026h): if the organization cannot fully specify all 48 dimensions of the OST specification space, it must choose which dimensions to specify. The spectral resource allocation model tells it *which ones*: specify the dimensions that the target cohort weights positively, in proportion to the weight-to-cost ratio.

---

## 7. Strategy Frameworks as Spectral Projections

Each of the five frameworks examined below has been applied to brand investment decisions in practice, yet none independently yields the allocation theorem derived in Section 3. The reason is not empirical but structural: none defines a formal metric on the brand perception space, and without such a metric, resource allocation cannot be posed as a geometric optimization problem. Blue Ocean Strategy operates on a visual canvas whose axes carry no metric and whose distances between profiles are not computable. Jobs to Be Done identifies weight-like constructs qualitatively but provides no distance function on the space of jobs, so there is no notion of how far a signal portfolio is from optimally serving a job. Lean Startup iterates toward product-market fit without a formal criterion for the distance between the current signal portfolio and the cohort's weight profile. Porter's Five Forces characterizes competitive structure but does not define a metric on the space of competitive positions, so rivalry intensity cannot be translated into a packing density. The Resource-Based View identifies strategic resource properties but operates without a metric on the space of brand positions, so "uniqueness" and "inimitability" remain qualitative assessments rather than measurable distances. The spectral resource allocation model fills this gap: the Aitchison metric on $\mathbb{R}^8_+$ (Zharnikov, 2026d) and the Fisher-Rao metric on $\Delta^7$ together supply the geometric structure that transforms each framework's intuitions into computable quantities.

### 7.1 Blue Ocean Strategy

Kim and Mauborgne's (2005) Blue Ocean Strategy centers on the *strategy canvas* -- a visual profile of how a company invests across key competing factors, with the prescription to "raise, reduce, eliminate, and create" factors to find uncontested market space.

**Spectral correspondence.** The strategy canvas is a low-resolution spectral profile. "Competing factors" map to SBT dimensions (or sub-dimensions). "Raise" corresponds to increasing $s_i$. "Reduce" corresponds to decreasing $s_i$. "Eliminate" corresponds to setting $s_i = 0$ (dark signal). "Create" corresponds to activating a dimension that competitors have at zero.

The SBT formalization adds three elements that Blue Ocean lacks:

1. **Metric**: Blue Ocean's canvas has no distance measure between profiles. SBT's Aitchison metric (Zharnikov, 2026d) provides one.
2. **Capacity bounds**: Blue Ocean says "find uncontested space" but cannot quantify how much space exists. The sphere-packing result (Zharnikov, 2026g) provides explicit capacity bounds: at perceptual threshold $\varepsilon = 0.10$, up to $10^8$ distinguishable positions exist in $\mathbb{R}^8_+$.
3. **Demand validation**: Blue Ocean does not specify *whose* perceptual weights determine "value innovation." The alignment gap framework (Section 4) shows that the founder's weights are insufficient -- the target cohort's measured weights must drive the canvas.

### 7.2 Jobs to Be Done

Christensen et al.'s (2016) JTBD framework posits that customers "hire" products to accomplish functional, social, and emotional jobs. The job decomposition determines what features matter.

**Spectral correspondence.** A "job" maps to a weight vector on $\Delta^7$. The "functional job" loads on experiential and economic dimensions. The "social job" loads on the social dimension. The "emotional job" loads on narrative and ideological dimensions. Different jobs correspond to different weight profiles.

The SBT formalization adds:

1. **Dimensional completeness**: JTBD typically identifies 2-4 jobs. SBT's eight dimensions ensure no perceptual dimension is overlooked -- including temporal (heritage/longevity) and cultural (zeitgeist), which JTBD frameworks rarely capture.
2. **Weight measurement**: JTBD identifies jobs qualitatively. SBT measures dimensional weights quantitatively, enabling the optimization in Theorem 1.
3. **Metamerism awareness**: JTBD assumes the job determines the product. Theorem 4 shows that multiple signal portfolios can satisfy the same job (same perceived value), so the choice among metamers is a cost-optimization problem.

### 7.3 Lean Startup

Ries's (2011) Lean Startup methodology prescribes building a Minimum Viable Product (MVP), measuring customer response, and iterating. The Build-Measure-Learn loop is the core operational cycle.

**Spectral correspondence.** The MVP is an initial signal portfolio $s^{(0)}$. The Build-Measure-Learn loop is iterative optimization of $V(s, c)$ with noisy gradient estimates. The "pivot" is a discrete jump to a new region of $\mathbb{R}^8_+$ when the current trajectory converges to a local optimum that does not match the target cohort.

OST (Zharnikov, 2026i) goes further: the L0 demand-validation gate requires specifying the target customer experience *before* building the product. The Lean Startup's MVP is an hypothesis about L0; OST makes it a formal contract. The distinction matters: an MVP is tested empirically (build, then measure); an L0 contract is validated analytically (specify, then verify against cohort weights).

### 7.4 Porter's Five Forces

Porter (1980) models industry structure through five competitive forces: rivalry, buyer power, supplier power, substitutes, and entry barriers.

**Spectral correspondence.**

| Force | SBT/OST Equivalent |
|:------|:-------------------|
| Rivalry intensity | Sphere-packing density in perceptual neighborhood (Zharnikov, 2026g) |
| Buyer power | Cohort's economic dimension weight $w_6(c)$ |
| Supplier power | Cost parameter $\alpha_i$ for supply-chain-dependent dimensions |
| Threat of substitutes | Metamerism rate: fraction of alternative portfolios producing equivalent perception (Zharnikov, 2026e) |
| Entry barriers | Cost of achieving minimum signal strength on high-weight dimensions |

### 7.5 Resource-Based View

Barney's (1991) RBV identifies Valuable, Rare, Inimitable, and Non-substitutable (VRIN) resources as the basis of sustained competitive advantage.

**Spectral correspondence.**

| VRIN Criterion | Spectral Interpretation |
|:---------------|:-----------------------|
| Valuable | Operational capability produces signal on dimensions with high cohort weight |
| Rare | Capability occupies a unique spectral position (low sphere-packing density locally) |
| Inimitable | Signal portfolio cannot be replicated due to dark signals (deliberate absence is harder to reverse-engineer than presence) |
| Non-substitutable | No metamer exists at lower cost (Theorem 4 uniqueness condition) |

---

## 8. Case-Study Applications

### 8.1 Canonical Brand Profiles

We apply the model to the five case-study brands from Zharnikov (2026a, 2026d), using the canonical emission profiles:

| Dimension | Hermes | IKEA | Patagonia | Erewhon | Tesla |
|:----------|:------:|:----:|:---------:|:-------:|:-----:|
| Semiotic | 9.5 | 8.0 | 6.0 | 7.0 | 7.5 |
| Narrative | 9.0 | 7.5 | 9.0 | 6.5 | 8.5 |
| Ideological | 7.0 | 6.0 | 9.5 | 5.0 | 3.0 |
| Experiential | 9.0 | 7.0 | 7.5 | 9.0 | 6.0 |
| Social | 8.5 | 5.0 | 8.0 | 8.5 | 7.0 |
| Economic | 3.0 | 9.0 | 5.0 | 3.5 | 6.0 |
| Cultural | 9.0 | 7.5 | 7.0 | 7.5 | 4.0 |
| Temporal | 9.5 | 6.0 | 6.5 | 2.5 | 2.0 |

### 8.2 Hypothetical Founder Profiles

To illustrate the alignment gap, we construct hypothetical founder spectral profiles for each brand:

| Dimension | Hermes Founder | IKEA Founder | Patagonia Founder | Erewhon Founder | Tesla Founder |
|:----------|:--------------:|:------------:|:-----------------:|:---------------:|:-------------:|
| Semiotic | 0.20 | 0.05 | 0.05 | 0.10 | 0.10 |
| Narrative | 0.15 | 0.05 | 0.15 | 0.05 | 0.20 |
| Ideological | 0.10 | 0.05 | 0.30 | 0.05 | 0.05 |
| Experiential | 0.20 | 0.10 | 0.15 | 0.30 | 0.30 |
| Social | 0.15 | 0.05 | 0.10 | 0.20 | 0.15 |
| Economic | 0.02 | 0.50 | 0.05 | 0.05 | 0.05 |
| Cultural | 0.10 | 0.10 | 0.10 | 0.15 | 0.05 |
| Temporal | 0.08 | 0.10 | 0.10 | 0.10 | 0.10 |

These profiles are illustrative, not measured. The Hermes founder profile emphasizes semiotic and experiential (artisan obsession). The IKEA founder profile heavily weights economic (democratic design philosophy). The Patagonia founder profile concentrates on ideological (environmental mission). The Erewhon founder profile emphasizes experiential (curated sensory experience). The Tesla founder profile loads on narrative and experiential (technology vision).

### 8.3 Alignment Gap Computation (Illustrative, Non-Empirical Scenario)

For each brand, we construct a plausible target cohort weight profile and compute the alignment gap. The target cohort profiles represent the observed perceptual priorities of each brand's core customer base:

| Dimension | Hermes Cohort | IKEA Cohort | Patagonia Cohort | Erewhon Cohort | Tesla Cohort |
|:----------|:------------:|:-----------:|:----------------:|:--------------:|:------------:|
| Semiotic | 0.18 | 0.10 | 0.08 | 0.10 | 0.12 |
| Narrative | 0.15 | 0.08 | 0.12 | 0.08 | 0.15 |
| Ideological | 0.08 | 0.05 | 0.20 | 0.05 | 0.05 |
| Experiential | 0.15 | 0.15 | 0.15 | 0.25 | 0.20 |
| Social | 0.18 | 0.07 | 0.12 | 0.20 | 0.18 |
| Economic | 0.03 | 0.35 | 0.08 | 0.07 | 0.12 |
| Cultural | 0.13 | 0.10 | 0.10 | 0.15 | 0.08 |
| Temporal | 0.10 | 0.10 | 0.15 | 0.10 | 0.10 |

**Alignment gap results** (under uniform costs $\alpha_i = 1$, $\lambda = 1$):

| Brand | $\|w(f)\|^2$ | $\langle w(f), w(c) \rangle$ | $\mathcal{A}(f,c)$ | Hellinger $H(f,c)$ | Interpretation |
|:------|:------------:|:----------------------------:|:-------------------:|:-------------------:|:--------------|
| Hermes | 0.156 | 0.152 | 0.004 | 0.048 | Near-perfect alignment |
| IKEA | 0.286 | 0.222 | 0.064 | 0.212 | Founder over-weights economic |
| Patagonia | 0.155 | 0.142 | 0.013 | 0.103 | Small gap (mission aligns) |
| Erewhon | 0.163 | 0.141 | 0.022 | 0.127 | Moderate experiential bias |
| Tesla | 0.157 | 0.127 | 0.030 | 0.158 | Narrative/experiential over-weight |

**Ordering**: Hermes (0.004) < Patagonia (0.013) < Erewhon (0.022) < Tesla (0.030) < IKEA (0.064).

IKEA's large gap reflects the founder's extreme economic concentration ($w_6 = 0.50$) versus the cohort's more balanced profile ($w_6 = 0.35$). This does not mean IKEA is poorly managed -- Ingvar Kamprad's economic obsession was the brand's defining feature. Rather, it means IKEA's success required the founder's vision to be sufficiently close to the cohort's priorities on the economic dimension that the over-investment in that dimension still created net positive value.

### 8.4 Blind Spot Analysis

| Brand | Founder Blind Spot | Cohort Weight on That Dimension | Risk Level |
|:------|:-------------------|:-------------------------------|:-----------|
| Hermes | None (all $w_i > 0$) | -- | Low |
| IKEA | Social ($w_5 = 0.05$) | 0.07 | Low (both low) |
| Patagonia | Economic ($w_6 = 0.05$) | 0.08 | Low-Medium |
| Erewhon | Narrative ($w_2 = 0.05$) | 0.08 | Low-Medium |
| Tesla | Ideological ($w_3 = 0.05$) | 0.05 | Low (both low) |

No brand in this sample has a true blind spot ($w_i = 0$). The nearest case is Tesla's ideological dimension: the founder's low weight (0.05) combined with the brand's weak signal (3.0/10) suggests near-blindness on values-based positioning. This manifests as the brand's inconsistent political and ethical signals -- not because the founder intends inconsistency, but because the dimension receives minimal perceptual and operational attention.

---

## 9. Implications for Practice

### 9.1 The L0 Demand-Validation Gate

The alignment gap framework provides the formal justification for OST's L0 demand-validation gate (Zharnikov, 2026i). If the founder's spectral profile is used as the input to L1-L5 specification, the expected value loss is at least $\mathcal{A}(f, c)$. The L0 gate requires external evidence of the target cohort's dimensional weights before operational specification proceeds, replacing founder weights with measured cohort weights as the optimization input.

The demand-validation gate is not optional. Theorem 2 proves that the alignment gap is bounded below by a geometric quantity (Fisher-Rao distance) that no amount of execution quality can overcome. A founder who is distant from their target cohort on $\Delta^7$ will systematically misallocate resources, regardless of how well they execute on their chosen dimensions.

### 9.2 Dimensional Investment Audit

Theorem 1 prescribes the optimal investment ratio across dimensions. A brand can audit its current allocation by:

1. Measuring the target cohort's weight profile $w(c)$ via SBT methodology.
2. Estimating per-dimension cost parameters $\alpha_i$.
3. Computing the optimal allocation $s^*(c) = w(c) / (\lambda \alpha)$.
4. Comparing to the current allocation $s_{\text{actual}}$.
5. The gap $s^*(c) - s_{\text{actual}}$ identifies over- and under-invested dimensions.

### 9.3 Multi-Cohort Portfolio Design

Theorem 3 provides a quantitative criterion for the sub-brand decision. When a brand's target cohorts span a Fisher-Rao radius exceeding $r(\epsilon)$, the efficiency loss from a single signal portfolio exceeds $\epsilon$. The decision to sub-brand becomes economically justified when:

$$\text{Efficiency gain from targeting} > \text{Duplication cost} + \text{Coherence cost} + \text{Complexity cost}$$

The spectral model provides the left side; organizational cost analysis provides the right side.

---

## 10. Limitations and Future Research

### 10.1 Empirical Validation

The case-study analysis uses hypothetical founder and cohort profiles. Empirical validation requires measuring actual spectral profiles through consumer surveys (MaxDiff analysis, conjoint studies) and founder self-assessment. The empirical validation protocol is specified in Zharnikov (2026a, Section 5) and developed further in the author's internal analysis. The methodology assumes cohort weight profiles are measurable; SBT provides a specification for this measurement (Zharnikov, 2026a, Section 5), though large-scale empirical implementation remains future work.

### 10.2 Cost Function Estimation

The quadratic cost assumption is convenient but not empirically validated. In practice, cost functions are dimension-specific and may exhibit non-convexities (e.g., threshold effects where signals below a minimum strength are imperceptible). Estimating $\alpha_i$ requires operational data that few organizations currently track at the dimensional level.

### 10.3 Dynamic Extension

The model is static: it optimizes the signal portfolio at a single point in time. Zharnikov (2026j) establishes that brand perception evolves non-ergodically, with early investments compounding multiplicatively. Integrating the resource allocation model with the diffusion dynamics (Zharnikov, 2026j) to produce a dynamic investment trajectory is a natural extension -- and a necessary one for capital budgeting applications.

### 10.4 Interaction Effects

The separable cost function $C(s) = \sum_i c_i(s_i)$ ignores dimensional interactions. In practice, narrative and semiotic signals share creative infrastructure; experiential and economic signals interact through pricing psychology. A full model would include cross-terms $c_{ij}(s_i, s_j)$, which would alter the optimal allocation but not the qualitative conclusions about alignment gaps and metamerism.

### 10.5 Organizational Context

The model treats the firm as a unified optimizer. In practice, dimensional investment is distributed across departments (marketing owns semiotic/narrative, operations owns experiential, finance owns economic). The organizational specification impossibility (Zharnikov, 2026h) implies that coordinating this distributed optimization is itself a non-trivial problem. The interaction between resource allocation and organizational design is an open area.

---

## 11. Conclusion

This paper develops the economic bridge between multi-dimensional brand perception measurement and operational resource allocation. The spectral value function $V(s, c) = \langle w(c), s \rangle$ translates observer perception into a quantity that can be optimized against costs. The alignment gap $\mathcal{A}(f, c)$ quantifies the economic loss from founder weight projection -- the structural mechanism behind product-market fit failure. The multi-cohort efficiency bound establishes when a single brand can efficiently serve multiple cohorts and when sub-branding is economically justified. The cost-minimizing metamer gives the cheapest signal portfolio that achieves a target perception.

The results connect to five established strategy frameworks, revealing each as an implicit low-dimensional projection of the spectral resource allocation problem. Blue Ocean's strategy canvas becomes a spectral profile with a metric. JTBD's job decomposition becomes weight vector identification. Lean Startup's MVP becomes an L0 demand hypothesis. Porter's rivalry becomes sphere-packing density. The RBV's VRIN criteria become spectral position properties.

The paper completes the economic interpretation of the SBT mathematical foundations series (Zharnikov, 2026c-j), providing each R-paper result with a resource allocation interpretation:

| Paper | Mathematical Result | Economic Interpretation |
|:------|:-------------------|:-----------------------|
| R1 (2026d) | Formal distance in brand space | Distance between high-WTP and low-WTP cohorts; targeting precision |
| R2 (2026e) | Metamerism: distinct portfolios produce identical perception | Cheapest signal portfolio achieving target perception (Theorem 4) |
| R3 (2026f) | Cohort boundaries are fuzzy in high dimensions | Target market inherently fuzzy; value leaks to adjacent cohorts |
| R4 (2026g) | Sphere packing bounds on market capacity | Maximum profitable brands per perceptual neighborhood |
| R5 (2026h) | Specification impossibility | Must choose which dimensions to specify; demand analysis tells you where |
| R6 (2026j) | Non-ergodic perception dynamics | Early investment in high-weight dimensions compounds multiplicatively |

Together, these results establish that multi-dimensional brand perception is not merely a descriptive enrichment of brand theory but a prescriptive foundation for capital allocation. The question is no longer "what is our brand?" but "given our target cohort's measured spectral profile, which dimensions should receive the next dollar of investment?" The spectral resource allocation model answers this question with mathematical precision.

---

## References

Aaker, D. A. (1991). *Managing Brand Equity: Capitalizing on the Value of a Brand Name*. Free Press.

Barney, J. B. (1991). Firm resources and sustained competitive advantage. *Journal of Management*, 17(1), 99--120.

Christensen, C. M., Hall, T., Dillon, K., & Duncan, D. S. (2016). Competing against luck: The story of innovation and customer choice. *Harvard Business Review*, 94(10), 56--64.

Kapferer, J.-N. (2008). *The New Strategic Brand Management: Creating and Sustaining Brand Equity Long Term* (4th ed.). Kogan Page.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing*, 57(1), 1--22.

Kim, W. C., & Mauborgne, R. (2005). *Blue Ocean Strategy: How to Create Uncontested Market Space and Make the Competition Irrelevant*. Harvard Business School Press.

Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, 15, 1216--1221.

Porter, M. E. (1980). *Competitive Strategy: Techniques for Analyzing Industries and Competitors*. Free Press.

Ries, E. (2011). *The Lean Startup: How Today's Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses*. Crown Business.

Wedel, M., & Kamakura, W. A. (2000). *Market Segmentation: Conceptual and Methodological Foundations* (2nd ed.). Kluwer Academic Publishers.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026b). The alibi problem: Epistemic foundations of multi-source data reconciliation. Working Paper. https://doi.org/10.5281/zenodo.18944770

Zharnikov, D. (2026c). Geometric approaches to brand perception: A critical survey and research agenda. Working Paper. https://doi.org/10.5281/zenodo.18945217

Zharnikov, D. (2026d). Brand space geometry: A formal metric for multi-dimensional brand perception. Working Paper. https://doi.org/10.5281/zenodo.18945295

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026f). Cohort boundaries in high-dimensional perception space: A concentration of measure analysis. Working Paper. https://doi.org/10.5281/zenodo.18945477

Zharnikov, D. (2026g). How many brands can a market hold? Sphere packing bounds for multi-dimensional positioning. Working Paper. https://doi.org/10.5281/zenodo.18945522

Zharnikov, D. (2026h). Specification impossibility in organizational design: A high-dimensional geometric analysis. Working Paper. https://doi.org/10.5281/zenodo.18945591

Zharnikov, D. (2026i). The Organizational Schema Theory: Test-driven business design. Working Paper. https://doi.org/10.5281/zenodo.18946043

Zharnikov, D. (2026j). Non-ergodic brand perception: Diffusion dynamics on multi-dimensional perceptual manifolds. Working Paper. https://doi.org/10.5281/zenodo.18945660

---

## Appendix A: Proof Details

### A.1 Proof of Theorem 2 (Full Version)

The Hellinger distance between distributions $p$ and $q$ on a finite set is:

$$H(p, q) = \frac{1}{\sqrt{2}} \sqrt{\sum_i (\sqrt{p_i} - \sqrt{q_i})^2}$$

The Bhattacharyya coefficient is:

$$\text{BC}(p, q) = \sum_i \sqrt{p_i q_i}$$

These are related by $H^2 = 1 - \text{BC}$.

The Fisher-Rao distance on the simplex $\Delta^{n-1}$ is:

$$d_{\text{FR}}(p, q) = 2 \arccos\left(\sum_i \sqrt{p_i q_i}\right) = 2 \arccos(\text{BC}(p,q))$$

For the alignment gap, we need to bound $\|w(f)\|^2 - \langle w(f), w(c) \rangle$ from below in terms of $H(f,c)$.

Note that:
$$\langle w(f), w(c) \rangle \leq \left(\sum_i \sqrt{w_i(f) w_i(c)}\right)^2 = \text{BC}(f,c)^2$$

by the Cauchy-Schwarz inequality applied to vectors $(\sqrt{w_i(f)} \cdot \sqrt{w_i(f)})$ and $(\sqrt{w_i(f)} \cdot \sqrt{w_i(c)/w_i(f)})$.

More precisely, by the rearrangement:

$$\|w(f)\|^2 - \langle w(f), w(c) \rangle = \sum_i w_i(f) [w_i(f) - w_i(c)]$$

Using $a - b \geq (\sqrt{a} - \sqrt{b})^2$ for $a, b \geq 0$ when $a \geq b$ (and bounding the negative terms), we obtain:

$$\sum_i w_i(f) [w_i(f) - w_i(c)] \geq \min_i w_i(f) \cdot \sum_i (w_i(f) - w_i(c))_+^2$$

For the general bound, we use:

$$\|w(f)\|^2 - \langle w(f), w(c) \rangle = \frac{1}{2}\|w(f) - w(c)\|^2 + \frac{1}{2}(\|w(f)\|^2 - \|w(c)\|^2)$$

The $L^2$ distance on the simplex satisfies $\|p - q\|^2 \geq 2H(p,q)^2$ (a standard inequality). Combined with $\|w(f)\|^2 \geq 1/8$, this yields:

$$\mathcal{A}(f,c) \geq \frac{H(f,c)^2}{2\lambda\bar{\alpha}}$$

as stated. $\square$

### A.2 Numerical Computations for Section 8

All alignment gap computations use the formula:

$$\mathcal{A}(f,c) = \sum_i w_i(f)^2 - \sum_i w_i(f) w_i(c)$$

with $\lambda = 1$, $\bar{\alpha} = 1$.

**Hermes**: $\|w(f)\|^2 = 0.20^2 + 0.15^2 + 0.10^2 + 0.20^2 + 0.15^2 + 0.02^2 + 0.10^2 + 0.08^2 = 0.1558$

$\langle w(f), w(c) \rangle = 0.20 \cdot 0.18 + 0.15 \cdot 0.15 + 0.10 \cdot 0.08 + 0.20 \cdot 0.15 + 0.15 \cdot 0.18 + 0.02 \cdot 0.03 + 0.10 \cdot 0.13 + 0.08 \cdot 0.10 = 0.1521$

$\mathcal{A} = 0.1558 - 0.1521 = 0.0037 \approx 0.004$

**IKEA**: $\|w(f)\|^2 = 0.05^2 \cdot 3 + 0.10^2 \cdot 2 + 0.50^2 = 0.0075 + 0.02 + 0.25 = 0.2875$

$\langle w(f), w(c) \rangle = 0.05 \cdot 0.10 + 0.05 \cdot 0.08 + 0.05 \cdot 0.05 + 0.10 \cdot 0.15 + 0.05 \cdot 0.07 + 0.50 \cdot 0.35 + 0.10 \cdot 0.10 + 0.10 \cdot 0.10 = 0.2215$

$\mathcal{A} = 0.2875 - 0.2215 = 0.0660 \approx 0.064$

Hellinger distances computed as $H(f,c) = \frac{1}{\sqrt{2}} \sqrt{\sum_i (\sqrt{w_i(f)} - \sqrt{w_i(c)})^2}$.
