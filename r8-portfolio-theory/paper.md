# Spectral Portfolio Theory: Interference, Coherence, and Capacity in Multi-Brand Perception Space

**Zharnikov, D.**

Working Paper -- March 2026

---

## Abstract

Brand portfolio theory classifies portfolios by architecture -- monolithic, endorsed, house-of-brands -- but does not formalize how brands within the same portfolio interact in the observer's perception space. This paper develops spectral portfolio theory within Spectral Brand Theory (SBT), which models brands as emitters across eight typed dimensions perceived by heterogeneous observer cohorts. *Spectral interference* -- signals from one brand perturbing the perception cloud of another within shared cohorts -- is formalized, distinguishing *constructive interference* (compatible signals reinforcing mutual perception) from *destructive interference* (contradictory signals undermining it). Interference magnitude is bounded by cohort overlap and spectral proximity on high-weight dimensions, modulated by a parent-brand recognition gate. Single-brand coherence is extended to portfolio-level coherence through a three-layer metric (within-brand, cross-brand, and aggregate). Four portfolio archetypes are identified -- spectral cluster (LVMH), spectral spread (Procter & Gamble), spectral contradiction (Unilever), and spectral layering (Toyota/Lexus). A comparative analysis of LVMH and Unilever demonstrates that architecturally identical portfolios produce structurally opposite interference dynamics. Seven formal propositions are derived. The framework provides a formal basis for acquisition evaluation, portfolio rationalization, and cross-brand risk assessment that existing taxonomies cannot support.

**Keywords**: brand portfolio, spectral interference, constructive interference, destructive interference, portfolio coherence, observer cohorts, multi-dimensional brand perception, Spectral Brand Theory

**JEL Classification**: M31, M37, L11

---

## 1. Introduction

A consumer walks into a department store and encounters two products on adjacent shelves: Dove body wash and Axe deodorant. Both are manufactured by Unilever. If the consumer is aware of this shared parentage, the signals emitted by Axe -- historically rooted in hypersexualized advertising -- may contaminate the consumer's perception of Dove, whose "Campaign for Real Beauty" has positioned the brand as an advocate for authentic self-image. If the consumer is unaware, the two brands exist as independent objects in perception space, generating no mutual effect.

This scenario illustrates a phenomenon that brand portfolio theory has discussed qualitatively (Aaker & Joachimsthaler, 2000; Keller, 2008; Kapferer, 2008, 4th ed.) but has never formalized: the interaction of brands within a portfolio *as experienced in the observer's perception space*. Existing portfolio frameworks classify portfolios by architecture -- the organizational relationship between brands -- but not by interference -- the perceptual relationship between brands as processed by observers. Architecture describes how brands are structured by the firm; interference describes how brands interact in the mind.

The distinction matters because architecturally identical portfolios can produce structurally opposite perceptual effects. LVMH and Unilever both operate house-of-brands architectures with dozens of product brands beneath a corporate parent. Yet LVMH's portfolio produces predominantly constructive perceptual interactions (luxury brands reinforcing each other's luxury positioning), while Unilever's portfolio produces destructive interactions on the Ideological dimension (Dove's empowerment messaging contradicted by Axe's historical objectification). The architectural classification "house of brands" captures none of this difference. The urgency of this gap has increased as heightened information access -- what Swaminathan, Sorescu, Steenkamp, O'Guinn, and Schmitt (2020) call "hyperconnectedness" -- makes ownership structures more visible to consumers, effectively raising the awareness gate for portfolio interference. A framework that models brands as objects in multi-dimensional perception space -- and formalizes the mechanisms by which they interact within that space -- is required.

Spectral Brand Theory (Zharnikov, 2026a) provides the necessary foundation. SBT models a brand as an emitter of signals across eight typed dimensions (Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal), perceived by observers whose heterogeneous weight vectors determine which dimensions dominate their brand conviction. The framework distinguishes emission profiles (what brands signal) from perception clouds (what observers perceive), and has been applied to metamerism in dimensionality reduction (Zharnikov, 2026e), positioning capacity (Zharnikov, 2026g), and longitudinal case analysis of Dove (Zharnikov, 2026p).

This paper extends SBT to the portfolio level. The core contributions are:

1. **Spectral interference formalism** (Section 3): A formal model of how brands within a portfolio perturb each other's perception clouds in shared observer cohorts, with constructive and destructive interference as mathematically specified outcomes.

2. **Portfolio coherence metric** (Section 4): A three-layer coherence measure -- within-brand, cross-brand, and aggregate -- that extends SBT's single-brand coherence types to multi-brand portfolios.

3. **Four portfolio archetypes** (Section 5): A spectral classification of portfolio structures based on interference profiles, distinct from and complementary to architectural classifications.

4. **Portfolio capacity bounds** (Section 6): An extension of the sphere packing bounds from Zharnikov (2026g) to the multi-brand context, deriving the maximum number of non-interfering brands a portfolio can sustain.

5. **Seven formal propositions** (Section 7): Testable predictions about portfolio interference dynamics, coherence conditions, and capacity constraints.

6. **Comparative case analysis** (Section 8): LVMH versus Unilever as structurally opposite portfolio interference cases.

The paper contributes to two literatures. In brand portfolio theory, it provides, to the author's knowledge, the first formal model of cross-brand perceptual interaction that accounts for multi-dimensional perception and observer heterogeneity, moving beyond the architectural taxonomies of Aaker and Joachimsthaler (2000), the equity transfer models of Keller (2008), and the unidimensional signaling models of Erdem and Sun (2002). In SBT, it extends the single-brand framework to the portfolio level, connecting to the positioning capacity bounds of Zharnikov (2026g), the metamerism results of Zharnikov (2026e), and the longitudinal Dove analysis of Zharnikov (2026p).

---

## 2. Literature Review

### 2.1 Brand Portfolio Architecture

The dominant framework for brand portfolio management derives from Aaker and Joachimsthaler (2000), who proposed the "brand relationship spectrum" -- a continuum from branded house (all products under a single master brand, e.g., Virgin) to house of brands (distinct brands with minimal visible connection, e.g., Procter & Gamble). Intermediate forms include endorsed brands (sub-brands carrying a parent endorsement, e.g., Courtyard by Marriott) and sub-brands (jointly branded offerings, e.g., Sony PlayStation). Earlier empirical taxonomy work by Laforet and Saunders (1994) categorized how leading UK manufacturers organized their brand portfolios, providing the empirical foundation that Aaker and Joachimsthaler later codified. These frameworks' collective contribution was taxonomic: they gave practitioners a vocabulary for describing portfolio structure. Their limitation is that the taxonomy describes architectural form without modeling perceptual consequence.

Keller (2008) advanced the field by modeling equity transfer within portfolios. His customer-based brand equity (CBBE) model describes how associations with a parent brand can enhance or constrain sub-brand perceptions, introducing concepts of "brand leverage" and "brand dilution." However, CBBE treats brand equity as a unidimensional construct -- overall brand strength -- and therefore cannot represent differential effects across perceptual dimensions. A brand that transfers positive equity on the Experiential dimension but negative equity on the Ideological dimension is invisible to a unidimensional model.

Kapferer (2008, 4th ed.) provided a practitioner-oriented synthesis, introducing the "brand portfolio management" framework with emphasis on role assignment (strategic brands, cash cow brands, flanker brands, fighter brands). Kapferer's contribution was strategic rather than perceptual: he articulated *why* firms hold multiple brands but not *how* those brands interact in observer perception space.

### 2.2 Brand Extension, Fit, and Association Transfer

A large literature has examined how brand associations transfer across products bearing the same brand name. Aaker and Keller (1990) established that extension success depends on the perceived fit between the parent brand and the extension category, with complementarity and substitutability as the primary fit dimensions. Subsequent meta-analyses (Völckner & Sattler, 2006) confirmed fit as the dominant predictor of extension success across hundreds of studies. Meyvis and Janiszewski (2004) showed that brand breadth -- the range of contexts in which a brand has been applied -- moderates extension success, with broader brands being more resilient to fit violations.

These results are closely related to spectral interference but address a different question. Extension research models the transfer of associations from a single parent brand to a new product, holding the parent brand fixed. Portfolio interference theory, by contrast, models how multiple co-existing brands under shared ownership perturb each other's perception clouds bidirectionally. The fit construct in extension research maps to spectral proximity in SBT: brands whose emission profiles are close in the eight-dimensional space will experience more constructive interference, analogous to high-fit extension transfer. The critical difference is that spectral interference is observer-heterogeneous: what counts as "fit" depends on which dimensions the observing cohort weights, not on a category-level fit judgment.

Dilution effects in extension research also bear on portfolio interference. Loken and John (1993) showed that beliefs about a parent brand can be diluted by extensions with inconsistent attributes, and John, Loken, and Joiner (1998) demonstrated that flagship products can be diluted by poorly fitting extensions. Kumar (2005) found that counterextension failures produce stronger negative feedback than extension failures, and Swaminathan, Fox, and Reddy (2001) showed that extension introduction shifts market-level choice patterns. Dacin and Smith (1994) established that the number and quality of products in a portfolio moderate extension evaluations, linking portfolio characteristics to perceptual transfer. Sood and Keller (2012) showed that even the structure of brand names moderates the feedback effects of extension failures on parent brand beliefs. Balachander and Ghose (2003) documented reciprocal spillover: not only does the parent brand influence extension beliefs, but the extension influences beliefs about other products under the parent brand. These reciprocal effects are, in SBT's terms, portfolio interference effects -- the cross-brand perturbation of perception clouds modeled formally in Section 3.

### 2.3 Signaling Theory and Umbrella Branding

The closest existing formal approach to cross-brand perceptual interaction derives from information economics. Erdem and Swait (1998) formalized brand equity as a signaling phenomenon: brands reduce consumer uncertainty about product quality by serving as credible signals, with brand credibility determined by the brand's consistency and investment history. Their model generates a formal account of how brand equity transfers -- or fails to transfer -- across product categories.

Erdem and Sun (2002) extended this framework to umbrella branding, empirically modeling how advertising and promotional signals from one product under an umbrella brand affect beliefs about other products under the same umbrella. Their key finding is that positive umbrella signals increase both the quality expectation and perceived credibility of sibling products. Miklós-Thal (2012) provided a game-theoretic formalization of umbrella branding as a reputation-linking mechanism, proving that umbrella branding can only credibly signal *positive* quality correlation between products -- a result that the spectral framework generalizes by allowing directional interference (constructive on some dimensions, destructive on others) rather than restricting to uniformly positive signaling. These signaling models represent the closest existing formal approaches to cross-brand perceptual interaction.

Spectral portfolio theory extends the Erdem-Sun framework in three respects. First, where Erdem and Sun (2002) model quality signals as unidimensional (credibility-weighted quality perception), the spectral interference model operates dimension-by-dimension: a brand may enhance a sibling's credibility on the Experiential dimension while simultaneously undermining it on the Ideological dimension. This dimensional specificity is invisible to a unidimensional signaling model. Second, the signaling model treats all consumers as sharing the same quality-perception function; the spectral framework requires observer-heterogeneous weight vectors, so that the same portfolio signal is constructive for one cohort and destructive for another. Third, the signaling framework is primarily a model of belief updating about quality; the spectral framework models the full eight-dimensional perception cloud, including dimensions (Narrative, Ideological, Cultural, Temporal) that do not reduce to quality beliefs.

The divergence is sharpest in the Dove-Axe case. The Erdem-Sun signaling model predicts that Unilever's sustained investment in both brands increases perceived credibility for the umbrella -- consistent positive umbrella signals should raise quality expectations for both products. The spectral interference model makes the opposite prediction for the Purpose-Aligned cohort: awareness of shared ownership activates destructive interference on the Ideological dimension, reducing Dove's perceived coherence regardless of Unilever's investment history. The two frameworks make opposing predictions because the signaling model operates on unidimensional quality while the spectral model disaggregates by dimension and cohort. Empirical adjudication between these predictions would require measuring perception cloud shift upon ownership disclosure across cohorts with different dimensional weight profiles -- a test design specified in Section 8.5.

The Erdem-Swait-Sun framework thus handles within-dimension spillover credibility transfer, while spectral portfolio theory handles across-dimension, observer-heterogeneous perceptual interaction. The two frameworks are complementary, with spectral interference addressing the multi-dimensional, cohort-differentiated cases where signaling theory is incomplete.

### 2.4 Brand Spillover and Contamination

A substantial empirical literature has investigated cross-brand effects within portfolios. Brown and Dacin (1997) established that corporate associations influence consumer evaluations of new products, with corporate ability associations directly affecting product evaluations and corporate social responsibility associations shaping company evaluations. Srivastava and Shocker (1991) proposed that brand equity resides in the relationships between brands and their stakeholders, anticipating the portfolio-level perspective formalized here. Lei, Dawar, and Lemmink (2008) demonstrated that negative publicity about one brand in a portfolio can "spill over" to other brands, with the magnitude of spillover dependent on perceived brand relatedness. Simonin and Ruth (1998) found that brand alliance evaluations are shaped by the fit between the partnering brands' images, with poor fit generating negative evaluation transfer. Berens, van Riel, and van Bruggen (2005) showed that corporate brand associations influence product brand evaluations, with the direction of influence depending on the type of association (competence versus social responsibility).

Janakiraman, Sismeiro, and Dutta (2009) modeled perception spillovers across competing brands using a disaggregate model, identifying the conditions under which competitor brands benefit or suffer from a focal brand's actions. Their work is directly relevant to portfolio interference but examines between-competitor spillovers rather than within-portfolio interactions. Portfolio interference, as formalized in Section 3, operates through the awareness gate mechanism: it is conditioned on the observer's knowledge of shared parentage. Between-competitor spillovers operate through category-level associations and do not require ownership awareness. This distinction separates portfolio interference from the Janakiraman et al. (2009) framework, even as both address cross-brand perceptual effects.

The brand portfolio coherence literature also provides relevant empirical foundations. Nguyen, Zhang, and Calantone (2018) developed a brand portfolio coherence scale measuring the perceived consistency across brands in a portfolio, finding that higher coherence is associated with more favorable consumer evaluations of individual brands. Their empirical scale taps into the same construct that Section 4 formalizes as aggregate portfolio coherence ($\kappa_P$), though the Nguyen et al. scale does not distinguish within-brand from cross-brand coherence, nor does it account for observer heterogeneity in coherence perception. Kirca, Randhawa, Talay, and Akdeniz (2020) demonstrate empirically that product and brand portfolio strategies interact to affect brand performance, using longitudinal data from the U.S. automotive industry -- evidence that portfolio-level dynamics have measurable performance consequences beyond single-brand effects. Ward et al. (2025) provided the most recent empirical examination of portfolio brand cohesion, identifying consistency in symbolism and user imagery as the primary drivers of cohesion across portfolios. Their findings are consistent with the spectral interpretation: symbolism maps onto Semiotic emission, user imagery onto Social emission, and high cohesion on these dimensions corresponds to constructive interference in the awareness-gate framework.

The cannibalization literature provides a complementary perspective on portfolio interference. Jayarajan, Siddarth, and Silva-Risso (2018) empirically distinguish cannibalization from competition in multi-product portfolios, finding that within-portfolio product overlap has systematically different demand effects from cross-firm competition -- a structural distinction that aligns with the awareness-gate mechanism formalized in Section 3.

The empirical literature on brand architecture value is also relevant. Rao, Agarwal, and Dahlhoff (2004) empirically demonstrated that branded-house strategies are associated with higher firm value than house-of-brands strategies, suggesting that constructive interference (which is maximized under high parent brand visibility) generates measurable economic value. Morgan and Rego (2009) showed that portfolio composition characteristics -- including brand concentration and the presence of functionally broad anchor brands -- predict firm performance. These findings are consistent with Proposition 6 (constructive interference compounding) and Proposition 7 (portfolio capacity constraints) derived in Section 7.

These studies collectively establish that cross-brand effects exist and are economically consequential. What they do not provide is a formal model that (a) specifies the dimensions along which interference operates, (b) predicts the magnitude and direction of interference from the brands' perceptual profiles, or (c) accounts for observer heterogeneity in susceptibility to interference. The spillover literature demonstrates *that* interference occurs; this paper formalizes *how* it occurs and *when* it will be constructive versus destructive.

### 2.5 The Unilever Paradox in the Literature

The specific case of Unilever's portfolio contradiction -- Dove's empowerment messaging alongside Axe's objectification -- has attracted academic attention. Murray (2013) introduced the term "genderwashing" to describe the practice of marketing feminist empowerment through one brand while profiting from gender stereotyping through another. Murray documented early evidence that awareness of the Dove-Axe ownership connection contaminated Dove's brand perception among purpose-aligned consumers. Zharnikov (2026p) formalized this as *spectral interference on the Ideological dimension* within a longitudinal analysis of Dove.

What the literature lacks is a general framework that encompasses the Unilever case as a special instance of a broader class of portfolio interference phenomena. The Dove-Axe contradiction is not unique to Unilever; it is an instance of a structural pattern that arises whenever portfolio brands emit contradictory signals on the same dimension to overlapping observer cohorts. This paper provides the general framework.

### 2.6 Formal Portfolio Optimization

The most recent formal model of portfolio design in the marketing literature is Ke, Shin, and Yu (2022), who modeled product portfolio positioning as a mechanism to guide consumer search. Their framework operates on a Hotelling line (unidimensional positioning) and addresses pre-perception design: the firm chooses brand positions before consumers encounter them. The spectral portfolio framework differs in two fundamental respects: it operates in eight-dimensional perception space (not a Hotelling line), and it models post-awareness interference (how brands perturb each other once the observer perceives them) rather than pre-perception design optimization. The two frameworks are complementary -- Ke et al. optimize *where* to position brands; spectral interference theory predicts *what happens perceptually* after they are positioned.

### 2.7 Gap in the Literature

Three deficiencies characterize the existing brand portfolio literature, even after accounting for the signaling approach of Erdem and Sun (2002), the formal optimization model of Ke, Shin, and Yu (2022), the extension fit literature (Aaker & Keller, 1990; Völckner & Sattler, 2006), and the portfolio coherence work of Nguyen et al. (2018):

1. **No multi-dimensional formal model.** Existing frameworks classify portfolios by organizational architecture (Aaker & Joachimsthaler, 2000) or model equity transfer as a unidimensional construct (Keller, 2008; Erdem & Sun, 2002). None formalizes how brands interact across multiple independent perceptual dimensions, where a pair may be constructively interfering on some dimensions and destructively interfering on others simultaneously.

2. **No observer heterogeneity.** The spillover literature models the "average consumer" response to cross-brand contamination. It does not account for the fact that different observer cohorts -- with different spectral weight vectors -- may experience the same portfolio in structurally different ways. An observer who weights Ideological dimensions heavily will experience the Dove-Axe contradiction differently from one who weights Experiential dimensions.

3. **No portfolio-level coherence metric.** SBT has formalized single-brand coherence (Zharnikov, 2026a) and applied it to longitudinal case analysis (Zharnikov, 2026p). No existing framework extends coherence assessment to the portfolio level, where within-brand coherence, cross-brand coherence, and aggregate coherence are distinct constructs.

This paper addresses all three deficiencies.

---

## 3. The Spectral Interference Model

### 3.1 Preliminaries and Notation

The paper adopts the notation and definitions of Zharnikov (2026a). A brand's *emission profile* at time $t$ is a vector $\mathbf{e}_B(t) = [e_1, e_2, \ldots, e_8] \in \mathbb{R}^8_+$, where each component represents signal intensity on one of SBT's eight dimensions: Semiotic ($e_1$), Narrative ($e_2$), Ideological ($e_3$), Experiential ($e_4$), Social ($e_5$), Economic ($e_6$), Cultural ($e_7$), and Temporal ($e_8$). Each dimension carries signals of three types: *positive* (actively emitted), *null* (no signal), or *structural absence* (dark signal -- the conspicuous lack of expected signal).

**A note on observer dependence of emission profiles.** SBT's core thesis is that brand perception is observer-heterogeneous: what an observer perceives is a function of both the brand's emitted signals and the observer's spectral weight vector. This creates an important clarification for the interference model. Emission profiles $\mathbf{e}_B(t)$ are modeled as properties of the brand's communication output -- what the brand puts into the signal channel -- rather than as properties of individual observers' perceptions. However, the mapping from emission to perception is observer-dependent, governed by the observer's weight vector. In this sense, emission profiles are best understood as cohort-mean estimates: across a given observer cohort, the effective emission perceived by the average cohort member is a weighted function of $\mathbf{e}_B(t)$ and the cohort's mean spectral profile $\bar{\mathbf{w}}^{(C_k)}$. The worked examples in Sections 5 and 8 use illustrative cohort-mean estimates, not objectively measured signals. Empirical implementation would require spectral profile measurement instruments applied to representative observer samples (see Section 10.1).

An observer $j$ possesses an *observer spectral profile* -- a weight vector $\mathbf{w}_j = [w_1, \ldots, w_8] \in \Delta^7$ -- that determines the relative salience of each dimension in forming brand conviction. Observers with similar spectral profiles cluster into *cohorts* $C_k$ (Zharnikov, 2026a).

The *perception cloud* for cohort $C_k$ observing brand $B$ at time $t$ is the distribution of brand convictions across cohort members:

$$\Pi_{C_k}(B, t) = \{f(\mathbf{e}_B(t), \mathbf{w}_j) : j \in C_k\}$$

where $f$ is the conviction formation function that maps emission profiles and observer spectral profiles to brand conviction states (Zharnikov, 2026a).

### 3.2 Portfolio and Cohort Overlap

**Definition 1** (Brand portfolio). *A brand portfolio $\mathcal{P} = \{B_1, B_2, \ldots, B_n\}$ is a set of brands under common ownership by a parent entity $P$. Each brand $B_i$ has an emission profile $\mathbf{e}_{B_i}(t) \in \mathbb{R}^8_+$.*

**Definition 2** (Cohort overlap). *Two brands $B_i$ and $B_j$ share a cohort $C_k$ if observers in $C_k$ hold non-trivial perception clouds for both brands:*

$$\text{Overlap}(B_i, B_j) = \{C_k : |\Pi_{C_k}(B_i, t)| > \tau \text{ and } |\Pi_{C_k}(B_j, t)| > \tau\}$$

*where $\tau$ is the minimum cloud density threshold for meaningful brand awareness and $|\Pi_{C_k}(B, t)|$ denotes the proportion of cohort $C_k$ members with formed or forming perception clouds for brand $B$.*

The cohort overlap set is the critical precondition for interference. If two brands share no observer cohorts -- that is, no observers hold perception clouds for both brands simultaneously -- no interference can occur regardless of the brands' spectral profiles. This is the perceptual mechanism behind the house-of-brands architecture: by minimizing shared cohorts, the firm reduces interference. But as the analysis below demonstrates, cohort separation is never complete, and even small overlaps can generate significant interference when dimensional contradictions are severe.

**Definition 3** (Cohort overlap magnitude). *The overlap magnitude between brands $B_i$ and $B_j$ is:*

$$O(B_i, B_j) = \sum_{C_k \in \text{Overlap}(B_i, B_j)} |C_k| \cdot \min\left(|\Pi_{C_k}(B_i, t)|, |\Pi_{C_k}(B_j, t)|\right)$$

*where $|C_k|$ is the cohort size. The overlap magnitude is zero when the brands share no cohorts and maximal when both brands have fully formed perception clouds in all shared cohorts.*

### 3.3 The Awareness Gate

Spectral interference requires a cognitive precondition: the observer must be aware that brands $B_i$ and $B_j$ share a parent entity. Without this awareness, the brands exist as independent objects in perception space.

**Definition 4** (Awareness gate). *For observer $j$, the awareness gate $\alpha_j(B_i, B_j, P) \in [0, 1]$ represents the degree to which observer $j$ recognizes that brands $B_i$ and $B_j$ are owned by parent entity $P$. When $\alpha_j = 0$, the observer perceives no connection; when $\alpha_j = 1$, the observer has full knowledge of shared parentage.*

The awareness gate introduces an asymmetry between portfolio architectures. In a branded house (e.g., Virgin), $\alpha \approx 1$ for all observers, as the parent brand is visibly present on all products. In a house of brands (e.g., Procter & Gamble), $\alpha$ varies widely across observers, depending on brand literacy, media exposure, and engagement level.

**Remark.** The awareness gate distinguishes spectral interference from generic category effects. Without awareness of shared ownership, signals from Brand $A$ and Brand $B$ may still interact through category-level associations (e.g., all luxury brands forming a perceptual cluster). But such interactions are *category interference*, operating through market-level spectral proximity, not *portfolio interference*, which operates through the cognitive link of shared parentage. This paper addresses portfolio interference specifically; category interference is a distinct phenomenon, addressed in Zharnikov (2026g) through the sphere packing framework.

The threshold $\alpha_{\min}$ below which interference is effectively zero is a parameter to be estimated empirically, not derived theoretically. Conceptually, $\alpha_{\min}$ represents the minimum ownership-awareness level at which the perturbation to brand $B_i$'s perception cloud exceeds the observer's just-noticeable-difference threshold for brand conviction change. Estimation would require controlled disclosure experiments in which $\alpha$ is varied from 0 (no awareness of shared ownership) to 1 (full awareness), with perception cloud shift measured at each level to identify the onset of significant perturbation. The propositions in this paper remain testable conditional on $\alpha_{\min}$ estimation as a preliminary calibration step. In the illustrative computations that follow, $\alpha_{\min}$ is set to a plausible lower bound; sensitivity to this parameter is discussed in Section 10.

### 3.4 Spectral Interference: Formal Definition

**Definition 5** (Spectral interference). *For two brands $B_i$ and $B_j$ in portfolio $\mathcal{P}$, observed by cohort $C_k$ with awareness gate $\alpha_{C_k} > 0$, the spectral interference on dimension $d$ is:*

$$I_d(B_i, B_j, C_k) = \alpha_{C_k} \cdot \bar{w}_d^{(C_k)} \cdot (e_d^{(B_j)} - \mu_d)$$

*where $\bar{w}_d^{(C_k)}$ is the mean weight on dimension $d$ across cohort $C_k$, $e_d^{(B_j)}$ is brand $B_j$'s emission on dimension $d$, and $\mu_d$ is the dimension-$d$ category mean. The interference term represents the perturbation to cohort $C_k$'s perception cloud for brand $B_i$ caused by awareness of brand $B_j$'s signals.*

The interference operates dimension-by-dimension. This is critical: a brand may constructively interfere on one dimension and destructively interfere on another. The net effect depends on the observer cohort's spectral profile -- which dimensions they weight heavily.

**Remark** (Category mean in multi-category portfolios). *For portfolios spanning multiple product categories (fashion, spirits, perfumes in the case of LVMH; personal care, food, home care in the case of Unilever), the category mean $\mu_d$ in Definition 5 is computed relative to the focal brand $B_i$'s primary category. When evaluating the interference of brand $B_j$ (e.g., Hennessy, spirits) on brand $B_i$ (e.g., Louis Vuitton, fashion), $\mu_d$ is the fashion category mean on dimension $d$, and the deviation $(e_d^{(B_j)} - \mu_d)$ measures how $B_j$'s signal differs from the norms of $B_i$'s competitive context. This category-relative formulation ensures that cross-category interference captures the mechanism by which signals from a sibling in a different category disrupt the focal brand's positioning within its own competitive space. For within-category brand pairs, $\mu_d$ is unambiguous.*

**Definition 6** (Constructive interference). *Interference on dimension $d$ is constructive when the signals from both brands are compatible on that dimension relative to the observer's conviction:*

$$I_d(B_i, B_j, C_k) \text{ is constructive if } \text{sign}(e_d^{(B_i)} - \mu_d) = \text{sign}(e_d^{(B_j)} - \mu_d)$$

*That is, both brands deviate from the category mean in the same direction on dimension $d$. The observer's perception of Brand $B_i$ on dimension $d$ is reinforced by awareness that its sibling Brand $B_j$ emits a compatible signal.*

**Definition 7** (Destructive interference). *Interference on dimension $d$ is destructive when the signals from both brands are contradictory on that dimension:*

$$I_d(B_i, B_j, C_k) \text{ is destructive if } \text{sign}(e_d^{(B_i)} - \mu_d) \neq \text{sign}(e_d^{(B_j)} - \mu_d)$$

*The observer's perception of Brand $B_i$ on dimension $d$ is undermined by awareness that its sibling Brand $B_j$ emits a contradictory signal.*

### 3.5 Total Interference Magnitude

The total interference experienced by brand $B_i$ due to brand $B_j$ in cohort $C_k$ aggregates across dimensions, weighted by the cohort's spectral profile:

**Definition 8** (Total interference magnitude). *The total interference from brand $B_j$ on brand $B_i$ in cohort $C_k$ is:*

$$\mathcal{I}(B_i \leftarrow B_j, C_k) = \alpha_{C_k} \sum_{d=1}^{8} \bar{w}_d^{(C_k)} \cdot |e_d^{(B_j)} - e_d^{(B_i)}| \cdot \text{sgn}_d$$

*where $\text{sgn}_d = +1$ if the interference on dimension $d$ is constructive and $\text{sgn}_d = -1$ if destructive. The absolute magnitude (ignoring sign) is:*

$$|\mathcal{I}|(B_i \leftarrow B_j, C_k) = \alpha_{C_k} \sum_{d=1}^{8} \bar{w}_d^{(C_k)} \cdot |e_d^{(B_j)} - e_d^{(B_i)}|$$

**Theorem 1** (Interference bound). *The absolute interference magnitude is bounded:*

$$|\mathcal{I}|(B_i \leftarrow B_j, C_k) \leq \alpha_{C_k} \cdot d_{\text{max}} \cdot \max_d \bar{w}_d^{(C_k)}$$

*where $d_{\text{max}} = 8 \cdot \max_d |e_d^{(B_j)} - e_d^{(B_i)}|$ is the maximal dimension-weighted spectral distance. Interference is bounded above by the product of awareness, spectral distance, and maximum dimensional weight.*

*Proof.* By the triangle inequality on the weighted $\ell^1$ distance:

$$\sum_{d=1}^{8} \bar{w}_d^{(C_k)} \cdot |e_d^{(B_j)} - e_d^{(B_i)}| \leq \max_d \bar{w}_d^{(C_k)} \cdot \sum_{d=1}^{8} |e_d^{(B_j)} - e_d^{(B_i)}|$$

Since $\alpha_{C_k} \leq 1$, the bound follows. $\square$

The bound reveals three levers for managing interference: (1) reduce awareness (house-of-brands architecture), (2) reduce spectral distance on critical dimensions (portfolio coherence), or (3) reduce cohort overlap (target different observer populations). The interference bound also demonstrates that interference magnitude is not a property of the brands alone -- it depends on which cohort is experiencing the portfolio.

**Practical significance.** Interference $|\mathcal{I}|$ is practically significant when it exceeds the cohort's perception cloud dispersion $\sigma_{C_k}$ -- the typical spread of brand conviction within the cohort. When $|\mathcal{I}| < \sigma_{C_k}$, the perturbation is absorbed within normal perceptual noise; when $|\mathcal{I}| > \sigma_{C_k}$, the interference shifts the cohort's mean brand conviction by more than one standard deviation, producing measurable changes in brand evaluation and choice behavior. This normalization provides a reference scale for interpreting the computed interference values in Section 8.5.

### 3.6 Interference Asymmetry

Spectral interference is generally asymmetric:

$$\mathcal{I}(B_i \leftarrow B_j, C_k) \neq \mathcal{I}(B_j \leftarrow B_i, C_k)$$

The asymmetry arises because the perturbation to a brand's perception cloud depends not only on the interfering brand's signal but on the focal brand's existing position relative to the observer's conviction. A premium brand contaminated by a mass-market sibling suffers more than the mass-market brand gains, because the premium brand's perception cloud is more sensitive to downward perturbation on the Social and Semiotic dimensions than the mass-market brand's cloud is to upward perturbation. This connects to the conviction asymmetry formalized in Zharnikov (2026a): negative conviction forms faster and is more resistant to revision than positive conviction.

---

## 4. Portfolio Coherence Metric

### 4.1 From Single-Brand to Portfolio Coherence

SBT defines five single-brand coherence types based on how dimensional signals relate to each other (Zharnikov, 2026a): ecosystem ($A+$, all dimensions reinforce), signal ($A-$, most dimensions align), identity ($B+$, strong core on 2-3 dimensions), experiential asymmetry ($B-$, product excellent but other dimensions weak), and incoherent ($C-$, dimensional signals contradict each other). These types characterize the internal consistency of a single brand's emission profile.

Portfolio coherence extends this concept to the multi-brand case. A portfolio is not merely a collection of individually coherent brands; it has emergent coherence properties that arise from the interactions between brands. A portfolio of five individually $A+$ brands could produce a destructively interfering portfolio if those brands emit contradictory signals across the set.

### 4.2 Three Layers of Portfolio Coherence

**Definition 9** (Within-brand coherence). *The within-brand coherence $\kappa_W(B_i)$ is the standard SBT coherence type assigned to brand $B_i$'s emission profile, scored on the scale $A+ > A- > B+ > B- > C-$, mapped to numeric values $\{5, 4, 3, 2, 1\}$ for computation.*

**Definition 10** (Cross-brand coherence). *The cross-brand coherence between brands $B_i$ and $B_j$ in cohort $C_k$ is:*

$$\kappa_X(B_i, B_j, C_k) = \frac{\sum_{d=1}^{8} \bar{w}_d^{(C_k)} \cdot \mathbb{1}[\text{constructive}_d(B_i, B_j)]}{\sum_{d=1}^{8} \bar{w}_d^{(C_k)}}$$

*where $\mathbb{1}[\text{constructive}_d(B_i, B_j)] = 1$ if the brands' signals on dimension $d$ are constructive (same direction relative to category mean) and 0 otherwise. Cross-brand coherence ranges from 0 (all weighted dimensions destructive) to 1 (all weighted dimensions constructive).*

Cross-brand coherence is cohort-dependent. This is a crucial feature: two brands may be coherent as perceived by one cohort and incoherent as perceived by another, because different cohorts weight different dimensions. The Dove-Axe pair is highly coherent for the Product-Pragmatist cohort (which weights Experiential and Economic, where both brands perform well) but maximally incoherent for the Purpose-Aligned cohort (which weights Ideological, where the brands directly contradict).

**Definition 11** (Aggregate portfolio coherence). *The aggregate portfolio coherence for portfolio $\mathcal{P}$ in cohort $C_k$ is:*

$$\kappa_P(\mathcal{P}, C_k) = \frac{1}{|\mathcal{P}|} \sum_{B_i \in \mathcal{P}} \kappa_W(B_i) \cdot \frac{1}{|\mathcal{P}|-1} \sum_{B_j \neq B_i} O(B_i, B_j) \cdot \kappa_X(B_i, B_j, C_k)$$

*The aggregate metric weights within-brand coherence by the cohort-overlap-weighted average of cross-brand coherence across all brand pairs. A portfolio with high aggregate coherence has individually coherent brands that produce constructive interference in shared cohorts.*

### 4.3 Portfolio Coherence Types

Extending the five-level single-brand typology to portfolios:

**Table 1.** Portfolio coherence types and conditions for classification

| Portfolio Coherence Type | Condition | Description |
|--------------------------|-----------|-------------|
| Spectral resonance ($P_{A+}$) | $\kappa_X > 0.8$ across all major cohorts | All brand pairs constructively interfere on weighted dimensions |
| Spectral alignment ($P_{A-}$) | $\kappa_X > 0.6$ across major cohorts, no $\kappa_X < 0.3$ | Most brand pairs constructive; no severe contradictions |
| Spectral independence ($P_{B+}$) | $O(B_i, B_j) < \tau$ for most pairs | Brands occupy non-overlapping cohorts; minimal interference |
| Spectral tension ($P_{B-}$) | $\kappa_X \in [0.3, 0.6]$ for some major-cohort pairs | Mixed constructive/destructive; manageable contradictions |
| Spectral contradiction ($P_{C-}$) | $\kappa_X < 0.3$ for any pair in a major cohort | Destructive interference on high-weight dimensions in shared cohorts |

---

## 5. Four Portfolio Archetypes

### 5.1 Classification by Interference Profile

The interaction of spectral proximity (how similar brands' emission profiles are) and cohort overlap (how many observers perceive multiple brands) produces four structurally distinct portfolio archetypes. These archetypes are not mutually exclusive categories but ideal types that describe dominant patterns within a portfolio.

### 5.2 Spectral Cluster: LVMH

**Definition.** A *spectral cluster* portfolio contains brands whose emission profiles occupy proximate regions in the eight-dimensional perception space, with high cohort overlap and predominantly constructive interference.

LVMH Moet Hennessy Louis Vuitton operates approximately 75 brands (maisons) across six business groups. The fashion and leather goods division -- Louis Vuitton, Dior, Fendi, Givenchy, Celine, Loewe, Kenzo, Marc Jacobs -- forms a spectral cluster in SBT's eight-dimensional space. These brands share elevated signals on the Semiotic dimension (distinctive visual identities rooted in luxury craft), the Social dimension (exclusivity and status signaling), and an inverted Economic dimension (high price as signal of inaccessibility). The Temporal dimension is elevated across the cluster, with most maisons trading on heritage narratives measured in decades or centuries.

**Table 2.** Illustrative emission profiles for LVMH Fashion & Leather Goods cluster (assessed cohort-mean estimates, 0-10 scale)

| Dimension | Louis Vuitton | Dior | Fendi | Givenchy |
|-----------|:---:|:---:|:---:|:---:|
| Semiotic | 9.5 | 9.5 | 8.5 | 8.0 |
| Narrative | 8.5 | 9.0 | 7.0 | 7.5 |
| Ideological | 4.0 | 5.0 | 3.0 | 3.5 |
| Experiential | 9.0 | 8.5 | 8.0 | 7.5 |
| Social | 9.0 | 9.0 | 8.0 | 8.0 |
| Economic | 2.0 | 2.5 | 3.0 | 3.5 |
| Cultural | 8.0 | 8.5 | 7.0 | 7.5 |
| Temporal | 9.5 | 9.0 | 9.0 | 8.0 |

The cross-brand coherence for any pair within this cluster is high ($\kappa_X > 0.85$) for the luxury-connoisseur and luxury-aspirational cohorts. All four brands deviate from category means in the same direction on all high-weight dimensions. The interference is constructive: awareness that Louis Vuitton, Dior, Fendi, and Givenchy share an owner does not undermine any brand's perception -- it reinforces the perception of each as belonging to an elite class. The parent brand LVMH itself acquires positive associations as a steward of luxury heritage.

**Risk profile.** Spectral clusters are vulnerable to cluster-wide crisis. A scandal affecting any brand in the cluster can propagate to all others through the constructive interference mechanism operating in reverse: the same cohort overlap and spectral proximity that enable mutual reinforcement enable mutual contamination. When one luxury brand suffers reputational damage, the proximity of its emission profile to its siblings' profiles means the negative signal is not quarantined but transmitted.

### 5.3 Spectral Spread: Procter & Gamble

**Definition.** A *spectral spread* portfolio contains brands whose emission profiles occupy distant regions in perception space, with minimal cohort overlap and negligible interference (constructive or destructive).

Procter & Gamble operates brands across categories as diverse as laundry detergent (Tide), baby care (Pampers), personal grooming (Gillette), feminine hygiene (Always), and prestige beauty (SK-II). These brands occupy structurally different positions in the eight-dimensional space. Tide's profile is dominated by Economic and Experiential signals. Pampers weights Experiential (product reliability) and Narrative (care for infants). SK-II occupies a position closer to luxury, with elevated Semiotic, Social, and Economic-inverted signals. Gillette historically combined Experiential (product performance) with Social (masculine identity).

The cohort overlap across these brands is minimal. The observer who holds a perception cloud for Tide rarely holds a simultaneous perception cloud for SK-II -- the brands serve different functional categories with different observer populations. Where overlap exists (e.g., a household decision-maker who purchases both Tide and Pampers), the interference is negligible because the brands do not compete on the same dimensions. Tide's Experiential signal (cleaning efficacy) and Pampers' Experiential signal (baby comfort) are category-specific and do not interact.

**Risk profile.** Spectral spread portfolios sacrifice synergy for safety. The firm captures no constructive interference -- the brands do not reinforce each other. But they also generate no destructive interference. The P&G parent brand is largely invisible to consumers, and awareness of shared ownership produces no perturbation. The strategic cost is the absence of portfolio-level brand equity.

### 5.4 Spectral Contradiction: Unilever

**Definition.** A *spectral contradiction* portfolio contains brands whose emission profiles are both proximate enough to share observer cohorts and contradictory on high-weight dimensions within those shared cohorts.

Unilever presents the canonical case. Drawing on the longitudinal analysis of Dove in Zharnikov (2026p), the spectral contradiction emerges most acutely between Dove and Axe/Lynx on the Ideological dimension.

**Table 3.** Illustrative emission profiles for Unilever Dove-Axe-Ben & Jerry's triad (assessed cohort-mean estimates, 0-10 scale; Dove 2023 from Zharnikov 2026p)

| Dimension | Dove (2023) | Axe/Lynx | Ben & Jerry's |
|-----------|:---:|:---:|:---:|
| Semiotic | 7.0 | 6.5 | 7.5 |
| Narrative | 7.5 | 6.0 | 8.5 |
| Ideological | 7.5 | 2.0 | 9.0 |
| Experiential | 7.0 | 6.0 | 8.0 |
| Social | 6.5 | 7.0 | 7.5 |
| Economic | 6.5 | 7.5 | 4.5 |
| Cultural | 5.5 | 5.0 | 7.0 |
| Temporal | 7.5 | 5.5 | 6.5 |

The Dove-Axe cross-brand coherence $\kappa_X$ is severely dependent on the observing cohort. For the Product-Pragmatist cohort (high weight on Experiential and Economic), $\kappa_X \approx 0.75$ -- the brands are perceptually compatible because both deliver adequate functional performance at accessible price points. But for the Purpose-Aligned cohort (high weight on Ideological and Narrative), $\kappa_X \approx 0.15$ -- the brands are maximally contradictory on the dimension that matters most to this cohort. The contradiction is amplified by the Dove-Ben & Jerry's pair, which is coherent on Ideological ($\kappa_X \approx 0.85$ for the Purpose-Aligned cohort) but incoherent on Economic (mass-market accessibility versus premium pricing). The portfolio emits mixed signals that cannot be resolved into a coherent spectral identity at the corporate level.

The awareness gate moderates the damage. When the Purpose-Aligned cohort is unaware of the Dove-Axe ownership connection ($\alpha \approx 0$), no destructive interference occurs. But awareness is increasing over time. The rise of corporate transparency, investigative journalism, and social media has steadily eroded the house-of-brands shield. Zharnikov (2026p) documented the growth of the Skeptic-Critic cohort -- a group whose awareness of the Dove-Axe contradiction generates dark signals on the Ideological dimension that contaminate their entire Unilever perception.

**Risk profile.** Spectral contradiction portfolios face an escalating risk: as observer brand literacy increases and awareness gates rise, previously hidden contradictions become perceptible. The risk is not that the brands are poorly managed individually -- Dove and Axe are each internally coherent -- but that their coexistence under shared ownership creates portfolio-level incoherence in the perception space of shared cohorts.

### 5.5 Spectral Layering: Toyota/Lexus

**Definition.** A *spectral layering* portfolio contains brands that occupy different positions on the same dimensions, serving different cohorts with minimal overlap and constructive aspiration dynamics between layers.

Toyota and Lexus exemplify this pattern. Toyota's emission profile is dominated by Economic (value, reliability, accessibility) and Experiential (product quality, durability) signals. Lexus shifts the emphasis to Experiential (refinement, comfort, driving experience) and Social (premium status signaling), while Economic signals invert from accessibility to exclusivity.

**Table 4.** Illustrative emission profiles for Toyota/Lexus spectral layering (assessed cohort-mean estimates, 0-10 scale)

| Dimension | Toyota | Lexus |
|-----------|:---:|:---:|
| Semiotic | 6.5 | 8.5 |
| Narrative | 6.0 | 7.5 |
| Ideological | 5.0 | 4.0 |
| Experiential | 8.0 | 9.0 |
| Social | 5.0 | 8.0 |
| Economic | 8.5 | 3.5 |
| Cultural | 6.0 | 6.5 |
| Temporal | 8.0 | 7.0 |

The key feature of spectral layering is that the brands serve different cohorts on the same dimensions. The Value-Reliability cohort (high weight on Economic and Experiential) gravitates to Toyota. The Premium-Experience cohort (high weight on Experiential and Social) gravitates to Lexus. The cohort overlap is small -- few observers hold equally formed perception clouds for both brands.

Where overlap does exist, the interference is constructive through an aspiration mechanism. The Toyota owner who becomes aware of the Lexus connection does not experience destructive interference; instead, the Lexus brand creates an aspiration pathway -- an upward pull in perception space that enhances the Toyota brand by association with its premium sibling. This aspiration dynamic operates because the brands' signals move in the same direction on the Experiential dimension (both high, with Lexus higher) while diverging on the Economic dimension in a way that creates a natural upgrade path rather than a contradiction.

**Risk profile.** Spectral layering is vulnerable to layer collapse -- when the price or quality gap between layers narrows, the cohort separation erodes and the brands begin to compete rather than complement. If Toyota's quality and luxury features increase to the point where the Experiential gap with Lexus becomes negligible, the aspiration dynamic disappears and the brands cannibalize each other's cohorts.

---

## 6. Portfolio Capacity

### 6.1 Extension of Positioning Capacity

Zharnikov (2026g) established that the maximum number of distinguishable brand positions in SBT's eight-dimensional space is bounded by sphere packing density: at perceptual threshold $\varepsilon = 0.10$, the space admits at least $10^8$ distinguishable positions; at $\varepsilon = 0.20$, at least 390,625. These bounds describe the *market's* positioning capacity -- how many brands can be distinguished by observers.

Portfolio capacity is a different question: given a portfolio of $n$ brands, how many can coexist without generating destructive interference? The constraint is not distinguishability (which prevents confusion) but coherence (which prevents contradiction).

### 6.2 Portfolio Capacity Under Interference Constraints

**Definition 12** (Portfolio capacity). *The spectral portfolio capacity $K(\mathcal{P}, C_k, \theta)$ for portfolio $\mathcal{P}$ in cohort $C_k$ at interference tolerance $\theta$ is the maximum number of brands such that no pair generates destructive interference exceeding $\theta$:*

$$K(\mathcal{P}, C_k, \theta) = \max\{|\mathcal{P}'| : \mathcal{P}' \subseteq \mathcal{P}, |\mathcal{I}|(B_i \leftarrow B_j, C_k) < \theta \text{ for all } B_i, B_j \in \mathcal{P}'\}$$

The portfolio capacity is always less than or equal to the market positioning capacity, because portfolio interference imposes tighter constraints than mere distinguishability. Two brands can be perfectly distinguishable (far apart in perception space) yet generate severe destructive interference if they contradict on high-weight dimensions for their shared cohorts.

### 6.3 Capacity by Portfolio Archetype

The four archetypes have structurally different capacity implications:

**Spectral cluster.** Capacity is limited by the local packing density in the cluster region of perception space. The $E_8$ kissing number of 240 (Zharnikov, 2026g) provides an upper bound on nearest-neighbor positions, but the practical constraint is brand distinguishability within the cluster. LVMH's fashion cluster operates with approximately 8-10 brands in a narrow spectral region, well below the theoretical ceiling but approaching the practical threshold where consumers struggle to differentiate.

**Spectral spread.** Capacity is limited only by the total market positioning capacity, because brands occupy non-overlapping regions and generate negligible interference. P&G's portfolio of 60+ brands is feasible precisely because the brands are spectrally dispersed.

**Spectral contradiction.** Capacity is sharply limited on the contradicted dimensions. Each additional brand that emits signals on a contested dimension increases the destructive interference for all existing brands sharing that dimension. The Ideological dimension in Unilever's portfolio is effectively saturated: any new brand emitting ideological signals will interfere with either Dove (if progressive) or Axe (if regressive), or both.

**Spectral layering.** Capacity is limited by the number of distinguishable layers along the primary stratification axis. Toyota Motor Corporation operates three layers (Daihatsu, Toyota, Lexus) spanning the Economic dimension from high accessibility to low accessibility. Additional layers require sufficient spectral distance to maintain cohort separation.

### 6.4 The Interference Budget

**Definition 13** (Portfolio interference budget). *The total interference budget for brand $B_i$ in cohort $C_k$ is:*

$$\mathcal{I}_{\text{total}}(B_i, C_k) = \sum_{B_j \in \mathcal{P}, B_j \neq B_i} \mathcal{I}(B_i \leftarrow B_j, C_k)$$

*Brand $B_i$'s perception cloud in cohort $C_k$ is sustainable when $|\mathcal{I}_{\text{total}}| < \Theta(B_i, C_k)$, where $\Theta$ is the cloud stability threshold -- the maximum perturbation the perception cloud can absorb without undergoing state transition (from formed to forming, or from forming to stalled).*

The interference budget concept formalizes a constraint that portfolio managers have long understood intuitively: each additional brand in a portfolio does not merely add its own signals to the market; it perturbs the perception of every other brand in every shared cohort. The marginal cost of the $(n+1)$-th brand is not just its own brand-building expense but the interference it generates across the existing portfolio.

---

## 7. Formal Propositions

The preceding formal framework yields seven testable propositions.

### Proposition 1: Interference Conditionality

*Spectral interference between brands $B_i$ and $B_j$ within portfolio $\mathcal{P}$ operates if and only if three conditions hold simultaneously: (a) the brands share at least one observer cohort ($O(B_i, B_j) > 0$), (b) the awareness gate exceeds a minimum threshold ($\alpha_{C_k} > \alpha_{\min}$), and (c) the brands' emission profiles differ on at least one dimension weighted above a salience threshold by the shared cohort ($\exists d: \bar{w}_d^{(C_k)} > w_{\min}$ and $|e_d^{(B_i)} - e_d^{(B_j)}| > 0$). The absence of any one condition suppresses interference entirely.*

**Derivation.** From Definition 5, the interference term $I_d(B_i, B_j, C_k) = \alpha_{C_k} \cdot \bar{w}_d^{(C_k)} \cdot (e_d^{(B_j)} - \mu_d)$ is zero when $\alpha_{C_k} = 0$ (no awareness), when $\bar{w}_d^{(C_k)} = 0$ (dimension not weighted by cohort), or when $e_d^{(B_j)} = \mu_d$ (brand is indistinguishable from category mean on that dimension). The three conditions are jointly necessary and individually insufficient.

**Testability.** Measure the perception cloud for brand $B_i$ in a cohort before and after revealing the ownership connection to brand $B_j$. If conditions (a) and (c) hold, the change in perception cloud should be non-trivial only when $\alpha$ transitions from below to above threshold.

*Falsification*: P1 is falsified if significant perception cloud changes occur when any of the three conditions is absent -- for instance, if revealing ownership produces perception changes even when the brands share no observer cohorts, or when the brands' emission profiles are identical on all weighted dimensions.

### Proposition 2: Interference Direction Predictability

*The direction (constructive versus destructive) of spectral interference between brands $B_i$ and $B_j$ on dimension $d$ in cohort $C_k$ is determined by the sign concordance of the brands' deviations from the category mean on dimension $d$. Same-sign deviations produce constructive interference; opposite-sign deviations produce destructive interference. The direction is predictable from emission profiles alone, without requiring empirical measurement of the interference effect.*

**Derivation.** From Definitions 6 and 7, constructive interference occurs when $\text{sign}(e_d^{(B_i)} - \mu_d) = \text{sign}(e_d^{(B_j)} - \mu_d)$ and destructive when the signs differ. Both brands' emission profiles and the category mean are observable, making the direction computable ex ante.

**Testability.** For a portfolio of $n$ brands, compute the predicted direction of interference on each dimension for all $\binom{n}{2}$ brand pairs. Measure actual perception cloud perturbations through controlled awareness manipulations. The predicted direction should match the observed direction in significantly more than 50% of cases.

*Falsification*: P2 is falsified if the observed direction of interference is uncorrelated with sign concordance of emission profile deviations -- that is, if brands with same-sign deviations produce destructive interference as often as constructive, indicating that emission profiles alone do not determine interference direction.

### Proposition 3: Cohort-Dependent Portfolio Coherence

*The same portfolio can be simultaneously coherent for one observer cohort and contradictory for another. Formally, there exist portfolios $\mathcal{P}$ and distinct cohorts $C_k$, $C_l$ such that $\kappa_P(\mathcal{P}, C_k) > \kappa_P^{A-}$ (spectral alignment threshold) and $\kappa_P(\mathcal{P}, C_l) < \kappa_P^{C-}$ (spectral contradiction threshold).*

**Derivation.** Cross-brand coherence $\kappa_X$ (Definition 10) depends on the cohort's weight vector $\bar{w}_d^{(C_k)}$. A cohort that assigns zero weight to the Ideological dimension will not register the Dove-Axe contradiction. A cohort that assigns maximum weight to the Ideological dimension will register it maximally. Since SBT permits arbitrary weight vectors, the existence of portfolios with cohort-dependent coherence follows directly.

**Testability.** For a portfolio known to contain dimensional contradictions (e.g., Unilever), measure portfolio coherence perception across cohorts identified by their spectral weight vectors. The Purpose-Aligned cohort's portfolio coherence assessment should be significantly lower than the Product-Pragmatist cohort's assessment of the same portfolio.

*Falsification*: P3 is falsified if portfolio coherence assessments are statistically indistinguishable across cohorts with demonstrably different spectral weight profiles -- that is, if coherence perception is cohort-invariant despite dimensional contradictions in the portfolio.

### Proposition 4: Awareness Gate Moderation

*The magnitude of spectral interference is moderated by the awareness gate $\alpha$. In a house-of-brands architecture where parent brand recognition is below the awareness threshold ($\alpha < \alpha_{\min}$), spectral contradictions between sibling brands produce no interference, regardless of the magnitude of the dimensional contradiction. As $\alpha$ increases above threshold, destructive interference increases monotonically with $\alpha$.*

**Derivation.** From Definition 5, $I_d$ scales linearly with $\alpha_{C_k}$. When $\alpha_{C_k} < \alpha_{\min}$, the observer has insufficient awareness to link the brands, and the interference term is effectively zero. Above threshold, the linear scaling produces monotonic increase.

**Testability.** In a controlled experiment, expose observers to brand pairs with known dimensional contradictions under varying levels of ownership disclosure. Measure perception cloud perturbation as a function of disclosed ownership awareness. The perturbation should be negligible below threshold and increasing above it.

**Corollary (Shielding Theorem).** *A house-of-brands architecture functions as an interference shield if and only if the parent brand recognition gate remains below threshold across the portfolio's shared cohorts. The shield degrades monotonically as $\alpha$ increases, and cannot be restored once $\alpha$ exceeds threshold in a given cohort.*

*Falsification*: P4 is falsified if ownership disclosure produces significant perception cloud perturbations even when awareness levels are below the threshold -- that is, if interference operates independently of ownership awareness, suggesting that category-level association transfer (rather than ownership-gated interference) is the dominant mechanism.

This corollary has significant implications for corporate transparency trends. As media literacy increases and corporate ownership structures become more visible (through investigative journalism, social media, and regulatory disclosure requirements), the house-of-brands shield erodes. The interference that the architecture was designed to prevent begins to operate.

### Proposition 5: Interference Asymmetry

*Spectral interference is asymmetric: the perturbation of Brand $B_i$'s perception cloud by awareness of Brand $B_j$ differs in magnitude from the perturbation of Brand $B_j$'s cloud by awareness of Brand $B_i$. Specifically, the brand with higher single-brand coherence suffers greater relative perturbation from a lower-coherence sibling than vice versa.*

**Derivation.** A highly coherent brand ($A+$) has a tight perception cloud with low variance. A small perturbation to a tight cloud is proportionally larger than the same perturbation to a diffuse cloud. Conversely, an incoherent brand ($C-$) has a dispersed perception cloud that is less sensitive to marginal perturbation. Therefore, when a coherent brand is exposed to interference from an incoherent sibling, the proportional perturbation is larger than the reverse case.

**Testability.** Within a portfolio, identify brand pairs with asymmetric coherence levels. Measure the change in perception cloud dispersion for each brand upon disclosure of the sibling relationship. The higher-coherence brand should exhibit a larger proportional increase in cloud dispersion.

*Falsification*: P5 is falsified if interference is symmetric -- that is, if the proportional perception cloud perturbation is equal for high-coherence and low-coherence siblings, indicating that single-brand coherence does not moderate interference susceptibility.

### Proposition 6: Constructive Interference Compounding

*In a spectral cluster portfolio, constructive interference compounds across brand pairs: each additional brand whose emission profile is compatible with the cluster reinforces the perception of every existing brand. The total constructive interference experienced by any brand in a cluster of $n$ brands scales superlinearly with $n$, up to a saturation point determined by the cluster's spectral density.*

**Derivation.** For brand $B_i$ in a cluster, the total constructive interference from $n-1$ siblings is $\sum_{j \neq i} \mathcal{I}(B_i \leftarrow B_j, C_k)$. In a cluster where all pairs are constructive, each new brand adds a positive term. Moreover, the reinforcement is not merely additive: each new compatible brand increases the observer's conviction that the parent entity (LVMH) curates luxury, which increases the awareness gate for future acquisitions into the cluster. This positive feedback loop produces superlinear scaling.

**Testability.** Compare perception cloud intensity (conviction strength) for a brand presented in isolation versus presented as a member of progressively larger compatible clusters. Conviction strength should increase superlinearly up to a saturation point.

*Falsification*: P6 is falsified if conviction strength scales linearly (or sublinearly) with cluster size -- that is, if each additional compatible brand contributes a fixed marginal reinforcement with no compounding effect, indicating additive rather than superlinear dynamics.

### Proposition 7: Portfolio Capacity Constraint

*The maximum number of brands a portfolio can sustain without exceeding the interference budget of any brand in any shared cohort is constrained by the portfolio's spectral structure. For a spectral cluster, capacity is bounded by the local packing density divided by the minimum required inter-brand distance for constructive interference. For a spectral contradiction portfolio, each additional brand on a contested dimension reduces the effective capacity for all existing brands sharing that dimension.*

**Derivation.** From Definition 12, portfolio capacity $K$ requires that no pair exceeds the interference tolerance $\theta$. In a cluster, all pairs are constructive, so the binding constraint is distinguishability (from Zharnikov 2026g). In a contradiction, each additional brand on the contested dimension increases $|\mathcal{I}_{\text{total}}|$ for every other brand, and the budget constraint binds earlier.

**Testability.** Examine portfolios that have undergone brand rationalization (e.g., P&G's divestiture of 100+ brands in 2014). The divested brands should disproportionately be those that generated the highest destructive interference in the remaining portfolio.

*Falsification*: P7 is falsified if portfolios with high spectral contradiction sustain as many brands as spectrally clustered portfolios of comparable size and revenue -- that is, if contradiction imposes no capacity penalty, indicating that destructive interference does not accumulate with portfolio size.

---

## 8. Comparative Case Analysis: LVMH versus Unilever

### 8.1 Case Selection Rationale

LVMH and Unilever are selected as comparative cases because they share surface-level characteristics (global conglomerates, house-of-brands architecture, dozens of product brands, comparable revenue scale) yet produce structurally opposite interference dynamics. The comparison isolates the explanatory contribution of spectral interference theory: where architectural classification assigns both firms the same category, spectral analysis reveals diametrically opposed portfolio coherence.

### 8.2 LVMH: Constructive Interference in Practice

LVMH's 2023 revenue of EUR 86.2 billion (LVMH 2023) derives from approximately 75 brands across six business groups: Fashion & Leather Goods, Wines & Spirits, Perfumes & Cosmetics, Watches & Jewelry, Selective Retailing, and Other Activities. The portfolio's spectral structure is a nested cluster: a core luxury cluster (Fashion & Leather Goods) surrounded by adjacent clusters (Perfumes & Cosmetics, Watches & Jewelry) that share dimensions with the core but occupy distinct positions.

**Cross-brand coherence within the core cluster.** The four Fashion & Leather Goods brands profiled in Section 5.2 produce the following pairwise cross-brand coherence scores for the luxury-connoisseur cohort (high weight on Semiotic, Experiential, Temporal):

**Table 5.** Pairwise cross-brand coherence for LVMH Fashion & Leather Goods cluster (luxury-connoisseur cohort)

| Pair | $\kappa_X$ (luxury-connoisseur) | Dominant interference type |
|------|:---:|---|
| Louis Vuitton -- Dior | 0.92 | Constructive on all 8 dimensions |
| Louis Vuitton -- Fendi | 0.88 | Constructive; minor Narrative gap |
| Louis Vuitton -- Givenchy | 0.85 | Constructive; Semiotic distance |
| Dior -- Fendi | 0.86 | Constructive; Narrative gap |
| Dior -- Givenchy | 0.89 | Constructive on all weighted dimensions |
| Fendi -- Givenchy | 0.91 | Constructive; close profiles |

*Note: Coherence scores computed from assessed cohort-mean emission profiles (Tables 2-4). Values illustrate model mechanics; empirical measurement would require spectral profile instrumentation applied to representative observer samples.*

The minimum pairwise $\kappa_X$ in the cluster is 0.85, placing the portfolio in the spectral resonance ($P_{A+}$) category. Every brand reinforces every other brand for the cohort that matters most to the portfolio's commercial performance.

**Awareness gate effect.** Unlike Unilever, LVMH actively promotes the parent brand connection. The LVMH logo, the annual LVMH Prize for Young Fashion Designers, and executive visibility (Bernard Arnault's public role) elevate $\alpha$ toward 1.0 for the luxury-connoisseur cohort. This is rational precisely because the interference is constructive: higher awareness amplifies the mutual reinforcement.

### 8.3 Unilever: Destructive Interference in Practice

Unilever's 2023 revenue of EUR 59.6 billion (Unilever 2023) derives from approximately 400 brands across five business groups: Beauty & Personal Care, Home Care, Nutrition, Ice Cream, and Refreshment. The portfolio's spectral structure is a complex mixture: some sub-portfolios form clusters (Beauty & Personal Care premiums), some are spectrally spread (Home Care versus Nutrition), and some contain spectral contradictions (Dove versus Axe).

**Cross-brand coherence for the Dove-Axe-Ben & Jerry's triad.** Using the emission profiles from Section 5.4, the pairwise cross-brand coherence for the Purpose-Aligned cohort (from Zharnikov 2026p: high weight on Ideological [9.0], Narrative [8.0], Cultural [6.0]):

**Table 6.** Pairwise cross-brand coherence for Unilever Dove-Axe-Ben & Jerry's triad (Purpose-Aligned cohort)

| Pair | $\kappa_X$ (Purpose-Aligned) | Dominant interference type |
|------|:---:|---|
| Dove -- Axe | 0.15 | Destructive on Ideological, Narrative |
| Dove -- Ben & Jerry's | 0.85 | Constructive on Ideological, Narrative |
| Axe -- Ben & Jerry's | 0.10 | Destructive on Ideological |

*Note: Coherence scores computed from assessed cohort-mean emission profiles (Tables 2-4). Values illustrate model mechanics; empirical measurement would require spectral profile instrumentation applied to representative observer samples.*

The Dove-Axe pair and the Axe-Ben & Jerry's pair are in the spectral contradiction range ($\kappa_X < 0.3$). The Dove-Ben & Jerry's pair is constructively coherent, but this partial coherence cannot compensate for the Axe contradiction. The aggregate portfolio coherence for the Purpose-Aligned cohort is pulled into $P_{C-}$ (spectral contradiction) territory by the Axe anomaly.

For the Product-Pragmatist cohort (high weight on Experiential [9.0], Economic [8.0], Semiotic [5.0]):

**Table 7.** Pairwise cross-brand coherence for Unilever Dove-Axe-Ben & Jerry's triad (Product-Pragmatist cohort)

| Pair | $\kappa_X$ (Product-Pragmatist) | Dominant interference type |
|------|:---:|---|
| Dove -- Axe | 0.75 | Constructive on Experiential, Economic |
| Dove -- Ben & Jerry's | 0.55 | Mixed; Economic divergence |
| Axe -- Ben & Jerry's | 0.50 | Mixed; Economic divergence |

*Note: Coherence scores computed from assessed cohort-mean emission profiles (Tables 2-4). Values illustrate model mechanics; empirical measurement would require spectral profile instrumentation applied to representative observer samples.*

The same portfolio that is contradictory for the Purpose-Aligned cohort is moderately coherent for the Product-Pragmatist cohort. This confirms Proposition 3: portfolio coherence is cohort-dependent.

**Awareness gate dynamics.** Unilever has historically maintained low parent brand visibility -- a house-of-brands strategy designed to keep $\alpha$ low and thereby suppress the interference mechanism. The Unilever logo appears on packaging but is not prominently featured in brand advertising. However, several forces are elevating $\alpha$:

1. **Investigative journalism.** Exposés linking Dove's empowerment messaging to Unilever's operation of Fair & Lovely/Glow & Lovely (skin-lightening products) have circulated widely since the mid-2010s.

2. **Social media.** Viral posts juxtaposing Dove and Axe advertisements have become a recurring genre of brand criticism.

3. **Corporate sustainability reporting.** Unilever's own sustainability commitments -- prominently communicated under the corporate brand -- draw attention to the corporate-portfolio relationship.

4. **Academic criticism.** Murray's (2013) "genderwashing" analysis has been widely cited and entered popular discourse.

The net effect is a secular increase in $\alpha$ for the Purpose-Aligned and Skeptic-Critic cohorts -- precisely the cohorts most sensitive to the Ideological contradiction. As $\alpha$ rises, the house-of-brands shield degrades, and the destructive interference that was architecturally suppressed begins to operate.

### 8.4 Structural Comparison

**Table 8.** Structural comparison of LVMH and Unilever portfolio interference profiles

| Dimension | LVMH | Unilever |
|-----------|------|----------|
| Architecture | House of brands | House of brands |
| Spectral structure | Spectral cluster | Spectral contradiction |
| Cross-brand coherence (primary cohort) | 0.85-0.92 | 0.10-0.85 (pair-dependent) |
| Portfolio coherence type | $P_{A+}$ (resonance) | $P_{C-}$ (contradiction) for PA cohort |
| Awareness gate strategy | Amplify (constructive) | Suppress (destructive) |
| Parent brand visibility | High (intentional) | Low (defensive) |
| Interference direction | Constructive compounding | Destructive on Ideological |
| Risk structure | Cluster-wide crisis | Escalating contradiction |

The comparison demonstrates that the same architectural label -- "house of brands" -- maps to structurally opposite spectral portfolios. The explanatory power resides not in architecture but in the spectral interference profile.

### 8.5 Illustrative Computation: Cohort-Dependent Interference

To demonstrate the computational mechanics, consider the Dove-Axe pair from Table 3 under two cohorts with distinct spectral profiles:

- **Purpose-Aligned cohort** ($\mathbf{w} = [0.05, 0.20, 0.35, 0.05, 0.10, 0.05, 0.15, 0.05]$): Weights the Ideological dimension at 0.35, reflecting an observer group for whom brand purpose is the primary evaluation criterion.

- **Product-Pragmatist cohort** ($\mathbf{w} = [0.10, 0.05, 0.05, 0.30, 0.10, 0.25, 0.05, 0.10]$): Weights the Experiential and Economic dimensions at 0.30 and 0.25, reflecting an observer group focused on product performance and value.

Using the emission profiles from Table 3 and a personal care category mean of $\mu = [6.0, 5.5, 5.0, 6.5, 5.0, 6.0, 5.5, 5.0]$, the total interference $\mathcal{I}(\text{Dove} \leftarrow \text{Axe}, C_k)$ is computed at two awareness gate levels:

| | $\alpha = 0.3$ | $\alpha = 0.8$ |
|---|---|---|
| Purpose-Aligned | $\mathcal{I} = 0.3 \times 0.35 \times |3.0 - 5.0| = 0.21$ (Ideological dominant) | $\mathcal{I} = 0.8 \times 0.35 \times 2.0 = 0.56$ |
| Product-Pragmatist | $\mathcal{I} = 0.3 \times 0.05 \times |3.0 - 5.0| = 0.03$ (Ideological negligible) | $\mathcal{I} = 0.8 \times 0.05 \times 2.0 = 0.08$ |

The computation illustrates three properties simultaneously: (1) the same brand pair produces an order-of-magnitude difference in interference across cohorts (Proposition 3), (2) interference scales linearly with the awareness gate (Proposition 4), and (3) whether this interference is 'destructive' depends on which dimension dominates -- the Purpose-Aligned cohort experiences substantial Ideological disruption while the Product-Pragmatist cohort barely registers it. The illustrative scores are computed from assessed profiles; empirical application would require instrumenting both the emission profiles and the cohort weight vectors.

---

## 9. Discussion

### 9.1 Implications for Portfolio Design

The spectral interference framework reframes portfolio strategy from an architectural question ("how should brands be organized?") to a perceptual question ("how do brands interact in the observer's perception space?"). This reframing has several implications.

**Acquisition evaluation.** When a firm considers acquiring a new brand, the interference framework provides a formal basis for assessing perceptual fit. The acquirer should compute the cross-brand coherence $\kappa_X$ between the candidate brand and every existing portfolio brand, for every shared cohort. If the candidate introduces destructive interference on a high-weight dimension in a major cohort, the acquisition creates a spectral liability that may exceed the brand's standalone value.

**Brand rationalization.** The interference budget (Definition 13) provides a criterion for portfolio pruning, complementing Varadarajan, DeFanti, and Busch's (2006) analysis of how brand deletions affect corporate image and reputation. A brand should be divested when its destructive interference on other portfolio brands exceeds its contribution to portfolio revenue. P&G's 2014 divestiture of more than 100 brands -- reducing the portfolio from 170 to 65 brands -- can be interpreted as an (architecturally motivated but spectrally consequential) reduction of the interference budget. The retained brands were those with the highest standalone coherence and lowest cross-brand interference.

**New brand positioning.** When a portfolio firm launches a new brand, the spectral framework specifies the positioning constraint: the new brand must occupy a position in perception space that generates either constructive interference or negligible interference with existing portfolio brands, for all shared cohorts. This is a tighter constraint than mere market positioning (finding unoccupied space) because it considers the relational consequences within the portfolio.

### 9.2 Implications for Cross-Brand Risk Assessment

The interference framework reveals that brand risk is not merely a property of individual brands but of the portfolio structure. Three categories of portfolio risk emerge:

1. **Contagion risk** (spectral clusters): A crisis affecting one brand propagates to all brands in the cluster through the constructive interference mechanism operating in reverse. The same cohort overlap and spectral proximity that enabled mutual reinforcement enable mutual contamination. LVMH's cluster structure means that a major scandal at any maison would perturb the perception clouds of all other maisons.

2. **Contradiction risk** (spectral contradictions): Increasing awareness gates reveal hidden contradictions. Unilever faces a secular increase in destructive interference as corporate transparency norms rise and social media disseminates ownership information. The risk is not an event but a trend -- a gradual erosion of the house-of-brands shield.

3. **Collapse risk** (spectral layering): When the spectral distance between layers diminishes, cohort separation erodes and brands begin to cannibalize rather than complement. Toyota faces this risk if its quality trajectory narrows the gap with Lexus.

### 9.3 Relationship to Existing Portfolio Frameworks

The spectral interference model does not replace existing portfolio frameworks; it extends them along a dimension they do not address. Aaker and Joachimsthaler's (2000) architectural taxonomy describes the organizational relationship between brands. Keller's (2008) equity transfer model describes the direction of association flow. Kapferer's (2008, 4th ed.) role assignment describes the strategic purpose of each brand. The spectral interference model describes how brands interact in the observer's multi-dimensional perception space -- a question that none of the existing frameworks can answer because none represents perception as multi-dimensional and observer-heterogeneous.

The relationship is complementary, not competitive. An optimal portfolio strategy requires architectural design (Aaker), equity management (Keller), strategic role assignment (Kapferer), *and* interference management (this paper). The spectral framework adds the missing perceptual layer to the existing strategic layers.

A note on coordinate invariance: the four portfolio archetypes (spectral cluster, spectral spread, spectral contradiction, spectral layering) and the interference dynamics that generate them are geometric phenomena that do not depend on the specific choice of dimensional taxonomy. The eight SBT dimensions are one valid coordinate representation; the interference structure -- which brands reinforce and which undermine each other in shared cohorts -- is invariant under basis rotation and metric-preserving transformations. This coordinate-free character strengthens the framework's generalizability: the archetypes would be recoverable under any dimensional decomposition that preserves the perceptual geometry.

### 9.4 Connection to the SBT Research Program

This paper fills a specific gap in the SBT research program by extending the framework from single-brand to portfolio-level analysis. The connection to prior work is direct: the metamerism results from Zharnikov (2026e) explain why portfolio contradictions are invisible to scalar brand health metrics; the sphere packing bounds from Zharnikov (2026g) provide the positioning capacity ceiling that portfolio capacity cannot exceed; and the Dove longitudinal analysis from Zharnikov (2026p) provides the primary empirical illustration.

---

## 10. Limitations and Future Directions

### 10.1 Empirical Validation

The most significant limitation of this paper is that the spectral interference model has not been empirically tested through controlled measurement. The emission profiles and illustrative coherence scores used in the case analyses are assessed estimates (based on public corporate communications, advertising content, and academic perception studies) rather than values measured through spectral profile instrumentation applied to representative observer samples. The precision of the computed coherence scores (e.g., $\kappa_X = 0.92$) reflects the internal arithmetic of the model applied to these illustrative estimates, not the accuracy of empirical measurement. The propositions are formally derived from the SBT framework and are testable in principle, but the empirical tests have not yet been conducted.

Priority directions for empirical validation include:

1. **Awareness gate measurement.** Measuring $\alpha$ (parent brand recognition) across observer cohorts and correlating with perception cloud perturbation upon ownership disclosure.

2. **Cross-brand coherence validation.** Computing predicted cross-brand coherence from emission profiles and comparing with measured perception changes in controlled experiments.

3. **Portfolio coherence surveys.** Administering spectral profile measurement instruments to observer samples who evaluate multiple brands within the same portfolio, testing whether portfolio coherence assessments are cohort-dependent as Proposition 3 predicts.

### 10.2 Observer Spectral Resolution

The interference model assumes that observers can distinguish dimensional signals with sufficient resolution to register contradictions. In practice, observer spectral resolution varies -- some observers perceive brands in high-dimensional detail while others compress perception to two or three salient dimensions (Zharnikov, 2026e). The interaction between observer spectral resolution and interference susceptibility is a direction for future modeling.

### 10.3 Cultural Variation

The emission profiles and coherence assessments in this paper are based on perceptual patterns documented in Western academic literature. Observer cohort structure, dimensional salience, and awareness gate dynamics may differ systematically across cultural contexts. A brand pair that generates destructive interference on the Ideological dimension in a Western cohort may generate no interference in a cohort where the Ideological dimension carries low weight. Cross-cultural extension of the interference framework is a priority.

### 10.4 Dynamic Interference

This paper models interference at a point in time. In reality, interference dynamics evolve as awareness gates shift, emission profiles change, and cohort compositions evolve. Non-ergodic perception dynamics -- where interference effects compound multiplicatively over time rather than averaging ergodically -- provide the mathematical foundation for modeling dynamic interference. Integrating the portfolio interference model with non-ergodic dynamics is a natural next step. Medesani and Macdonald (2026) formalize a relevant asymmetry: the contraction gain k_c (the rate at which an admissible corridor narrows under strain) exceeds the recovery gain k_r (the rate at which it expands during quiescence). Applied to portfolio interference, this predicts that destructive interference accumulates faster than constructive interference dissipates -- brand damage from portfolio contradictions is faster than recovery from portfolio rationalization. This asymmetry may explain the empirical observation that portfolio contradictions, once publicly recognized, persist in consumer perception long after the offending brand has been repositioned. Per-dimension velocity tracking -- monitoring the rate and direction of change on each of the eight dimensions across measurement epochs -- provides an operational implementation path for detecting interference dynamics before they become visible in aggregate brand health metrics.

The Dove-Axe illustrative analysis uses emission profiles reflecting the historical peak of their Ideological dimension contradiction. Since approximately 2016, Axe/Lynx has undertaken significant repositioning, shifting from hypersexualized messaging toward inclusive masculine identity narratives (the 'Find Your Magic' campaign and subsequent messaging). Current emission profiles would likely show a narrowed Ideological gap, reducing the destructive interference magnitude computed in Tables 5-6. The structural point -- that architecturally identical portfolios can produce opposite interference dynamics depending on emission profile alignment -- remains valid regardless of any single brand's repositioning trajectory.

### 10.5 Empirical Proxies

Pending full spectral profile instrumentation, several empirical proxies may facilitate near-term testing: (a) brand perception surveys that decompose evaluation across SBT's eight dimensions; (b) sentiment analysis of social media discourse, coded by dimension; (c) conjoint analyses that vary brand portfolio disclosure; and (d) natural experiments in which corporate ownership becomes publicly known (e.g., following an acquisition announcement).

### 10.6 Graph-Theoretic Formalization

The portfolio interference model can be recast in graph-theoretic terms. Brands are nodes with eight-dimensional emission profiles as attributes; interference relationships are edges weighted by cohort overlap and spectral proximity. The four archetypes (cluster, spread, contradiction, layering) then correspond to graph-structural classes, and portfolio coherence becomes a graph-level property. Recent work on graph homomorphism distortion (Carrasco, Zaghen, Sumaraj, Bekkers, and Rieck, 2026) offers a metric that captures gradations of structural similarity between attributed graphs -- analogous to how the spectral framework captures gradations between brands that scalar brand equity treats as binary (same/different). Formalizing portfolio interference through graph homomorphism distortion would provide tighter bounds on portfolio capacity and enable computational optimization of portfolio composition.

### 10.7 Digital-Native Portfolios

The current framework is demonstrated on physical-product portfolios (luxury goods, FMCG, automotive). Digital-native portfolios -- Meta (Facebook, Instagram, WhatsApp), Alphabet (Google, YouTube, Waymo), Amazon (AWS, Prime, Whole Foods) -- represent a distinct archetype in which the parent brand is highly visible ($\alpha$ near 1.0) and interference operates partly through data-sharing and algorithmic association rather than traditional brand signals. In these portfolios, implicit awareness -- where the user does not consciously associate two services but behavioral data integration creates algorithmic coupling -- may require extending the awareness gate beyond conscious recognition. The 'spectral platform' archetype, in which interference flows through data infrastructure as well as brand signals, is a priority for empirical investigation and theoretical extension.

---

## 11. Conclusion

Brand portfolio theory has since Aaker and Joachimsthaler (2000) classified portfolios by architecture -- how brands are organized by the firm -- without formalizing how brands interact in the observer's perception space. This paper has introduced spectral portfolio theory, extending Spectral Brand Theory to the multi-brand context through the mechanism of spectral interference.

The core insight is that brands within a portfolio do not exist independently in the observer's mind. When an observer is aware that two brands share a parent entity, signals from one brand perturb the perception cloud of the other. The perturbation can be constructive (reinforcing mutual perception, as in LVMH's luxury cluster) or destructive (undermining mutual perception, as in Unilever's Ideological contradiction). The direction and magnitude of interference are predictable from the brands' emission profiles, the observer cohort's spectral weight vector, and the awareness gate.

Seven formal propositions have been derived, specifying the conditions under which interference operates (P1), the predictability of interference direction (P2), the cohort-dependence of portfolio coherence (P3), the moderating role of the awareness gate (P4), the asymmetry of interference between brands of different coherence levels (P5), the superlinear compounding of constructive interference in spectral clusters (P6), and the portfolio capacity constraint imposed by interference budgets (P7).

The framework reveals that the same architectural label -- "house of brands" -- can describe structurally opposite perceptual realities. LVMH and Unilever share the architecture but not the interference profile. The difference is not in how the brands are organized but in how they are perceived -- and specifically, in how their signals interact within the perception space of shared observer cohorts. Architectural classification alone cannot capture this difference. Spectral portfolio theory can.

The practical consequence is a shift in the locus of portfolio strategy. The question for portfolio managers is not only "how should the portfolio be structured?" but "how do the portfolio's brands interact in the perception space of each observer cohort they serve?" Answering this question requires the multi-dimensional, observer-heterogeneous framework that SBT provides. Spectral portfolio theory offers the formal tools -- interference metrics, coherence types, capacity bounds, and testable propositions -- to move brand portfolio management from architectural taxonomy to perceptual engineering.

---

## Appendix A: SBT Notation Summary

This appendix summarizes the core notation and concepts of Spectral Brand Theory (SBT) used throughout the paper. For full framework specification, see Zharnikov (2026a). DOI: 10.5281/zenodo.18945912.

**Brand emission profile.** $\mathbf{E} = [e_1, \ldots, e_8]$ where each $e_i \in [0, 10]$ is emission intensity on dimension $i$. Dimensions in order: Semiotic ($e_1$), Narrative ($e_2$), Ideological ($e_3$), Experiential ($e_4$), Social ($e_5$), Economic ($e_6$), Cultural ($e_7$), Temporal ($e_8$). Each dimension carries signals of three types: positive (actively emitted), null (no signal), or structural absence (dark signal -- the conspicuous lack of an expected signal).

**Observer spectral profile.** $\mathbf{w} = [w_1, \ldots, w_8] \in \Delta^7$ (the probability simplex), representing the relative salience of each dimension for a given observer. Weights sum to 1. Observers with high weight on Ideological ($w_3$) are sensitive to purpose and values signals; those with high weight on Economic ($w_6$) are sensitive to price and accessibility signals.

**Perception cloud.** The probabilistic representation of brand conviction formed through weighted signal accumulation across observer-brand interactions. A tight cloud indicates high-conviction observers; a diffuse cloud indicates heterogeneous or uncertain perceptions.

**Cohort.** A cluster of observers with similar spectral profiles -- close in the eight-dimensional weight space (Zharnikov, 2026a). Cohorts are perceptual, not demographic: a "Purpose-Aligned cohort" is defined by high weights on Ideological and Narrative, not by age or income.

**Coherence types** (single-brand, ordered from highest to lowest): ecosystem ($A+$, all dimensions reinforce), signal ($A-$, most dimensions align), identity ($B+$, strong core on 2-3 dimensions), experiential asymmetry ($B-$, product excellent but other dimensions weak), incoherent ($C-$, dimensional signals contradict each other).

---

## References

Aaker, D. A., & Joachimsthaler, E. (2000). *Brand leadership*. Free Press.

Aaker, D. A., & Keller, K. L. (1990). Consumer evaluations of brand extensions. *Journal of Marketing*, 54(1), 27-41.

Balachander, S., & Ghose, S. (2003). Reciprocal spillover effects: A strategic benefit of brand extensions. *Journal of Marketing*, 67(1), 4-13.

Berens, G., van Riel, C. B. M., & van Bruggen, G. H. (2005). Corporate associations and consumer product responses: The moderating role of corporate brand dominance. *Journal of Marketing*, 69(3), 35-48.

Brown, T. J., & Dacin, P. A. (1997). The company and the product: Corporate associations and consumer product responses. *Journal of Marketing*, 61(1), 68-84.

Carrasco, M., Zaghen, O., Sumaraj, K., Bekkers, E., & Rieck, B. (2026). Graph homomorphism distortion: A metric to distinguish them all and in the latent space bind them. arXiv:2511.03068v4.

Dacin, P. A., & Smith, D. C. (1994). The effect of brand portfolio characteristics on consumer evaluations of brand extensions. *Journal of Marketing Research*, 31(2), 229-242.

Erdem, T., & Swait, J. (1998). Brand equity as a signaling phenomenon. *Journal of Consumer Psychology*, 7(2), 131-157.

Erdem, T., & Sun, B. (2002). An empirical investigation of the spillover effects of advertising and sales promotions in umbrella branding. *Journal of Marketing Research*, 39(4), 408-420.

Jayarajan, D., Siddarth, S., & Silva-Risso, J. (2018). Cannibalization vs. competition: An empirical study of the impact of product durability on automobile demand. *International Journal of Research in Marketing*, 35(4), 641--660. DOI: 10.1016/j.ijresmar.2018.08.001

Janakiraman, R., Sismeiro, C., & Dutta, S. (2009). Perception spillovers across competing brands: A disaggregate model of how and when. *Journal of Marketing Research*, 46(4), 467-481.

John, D. R., Loken, B., & Joiner, C. (1998). The negative impact of extensions: Can flagship products be diluted? *Journal of Marketing*, 62(1), 19-32.

Kapferer, J.-N. (2008). *The new strategic brand management* (4th ed.). Kogan Page.

Kirca, A. H., Randhawa, P., Talay, M. B., & Akdeniz, M. B. (2020). The interactive effects of product and brand portfolio strategies on brand performance: Longitudinal evidence from the U.S. automotive industry. *International Journal of Research in Marketing*, 37(2), 421--439. DOI: 10.1016/j.ijresmar.2019.09.003

Ke, T. T., Shin, J., & Yu, J. (2022). A model of product portfolio design: Guiding consumer search through brand positioning. *Marketing Science*, 42(6), 1101-1124.

Keller, K. L. (2008). *Strategic brand management: Building, measuring, and managing brand equity* (3rd ed.). Pearson.

Kumar, P. (2005). Brand counterextensions: The impact of brand extension success versus failure. *Journal of Marketing Research*, 42(2), 183-194.

Laforet, S., & Saunders, J. (1994). Managing brand portfolios: How the leaders do it. *Journal of Advertising Research*, 34(5), 64-76.

Lei, J., Dawar, N., & Lemmink, J. (2008). Negative spillover in brand portfolios: Exploring the antecedents of asymmetric effects. *Journal of Marketing*, 72(3), 111-123.

Loken, B., & John, D. R. (1993). Diluting brand beliefs: When do brand extensions have a negative impact? *Journal of Marketing*, 57(3), 71-84.

LVMH Moët Hennessy Louis Vuitton. (2023). *2023 Annual report*. LVMH.

Medesani, M., & Macdonald, J. (2026). *Geometric Foundations of Invariant Corridors and Governance: A Unified Framework with Empirical Validation* (Level 3.3 Frozen Baseline). Zenodo. DOI: 10.5281/zenodo.18822552

Meyvis, T., & Janiszewski, C. (2004). When are broader brands stronger brands? An accessibility perspective on the success of brand extensions. *Journal of Consumer Research*, 31(2), 346-357.

Miklós-Thal, J. (2012). Linking reputations through umbrella branding. *Quantitative Marketing and Economics*, 10(3), 335-374.

Morgan, N. A., & Rego, L. L. (2009). Brand portfolio strategy and firm performance. *Journal of Marketing*, 73(1), 59-74.

Murray, D. P. (2013). Branding "real" social change in Dove's Campaign for Real Beauty. *Feminist Media Studies*, 13(1), 83-101.

Nguyen, T. T. H., Zhang, Y., & Calantone, R. J. (2018). Brand portfolio coherence: Scale development and empirical demonstration. *International Journal of Research in Marketing*, 35(1), 60-80.

Rao, V. R., Agarwal, M. K., & Dahlhoff, D. (2004). How is manifest branding strategy related to the intangible value of a corporation? *Journal of Marketing*, 68(4), 126-141.

Simonin, B. L., & Ruth, J. A. (1998). Is a company known by the company it keeps? Assessing the spillover effects of brand alliances on consumer brand attitudes. *Journal of Marketing Research*, 35(1), 30-42.

Sood, S., & Keller, K. L. (2012). The effects of brand name structure on brand extension evaluations and parent brand dilution. *Journal of Marketing Research*, 49(3), 373-382.

Srivastava, R. K., & Shocker, A. D. (1991). Brand equity: A perspective on its meaning and measurement. *Marketing Science Institute Working Paper*, 91-124.

Swaminathan, V., Fox, R. J., & Reddy, S. K. (2001). The impact of brand extension introduction on choice. *Journal of Marketing*, 65(4), 1-15.

Swaminathan, V., Sorescu, A., Steenkamp, J.-B. E. M., O'Guinn, T. C. G., & Schmitt, B. (2020). Branding in a hyperconnected world: Refocusing theories and rethinking boundaries. *Journal of Marketing*, 84(2), 24-46.

Umashankar, N., Bahadir, S. C., & Bharadwaj, S. G. (2016). Do brands with shared equity facilitate or hurt parent brand performance? *Journal of Brand Management*, 23(2), 119-134.

Unilever PLC. (2023). *Annual report and accounts 2023*. Unilever.

Varadarajan, R., DeFanti, M. P., & Busch, P. S. (2006). Brand portfolio, corporate image, and reputation: Managing brand deletions. *Journal of the Academy of Marketing Science*, 34(2), 195-205.

Völckner, F., & Sattler, H. (2006). Drivers of brand extension success. *Journal of Marketing*, 70(2), 18-34.

Ward, T., Trinh, G., Beal, V., Dawes, J., & Romaniuk, J. (2025). Keeping it in the family: Measures and drivers of portfolio brand cohesion. *Journal of Brand Management*, 32, 291-306.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper. https://doi.org/10.5281/zenodo.18945352

Zharnikov, D. (2026g). How many brands can a market hold? Sphere packing bounds for multi-dimensional positioning. Working Paper. https://doi.org/10.5281/zenodo.18945522

Zharnikov, D. (2026p). The spectral anatomy of purpose: A longitudinal analysis of Dove Real Beauty through multi-dimensional brand perception theory. Working Paper. https://doi.org/10.5281/zenodo.19139258
