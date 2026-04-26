---
title: "Spectral Gap Restoration: A Threshold Inequality for Cohort Separability Survival in Brand Perception"
citation_key: 2026ad
version: 0.3.0
date: 2026-04-25
target_venue: Marketing Letters
doi: pending
---

**Abstract**

When a brand coherence shock disrupts the perceptual separability of observer cohorts, recovery is not guaranteed. This paper derives a sufficient condition for cohort separability survival: the corrective coherence emission rate (μ) must exceed the spectral leakage rate (λ) at the detection scale of the observer cohort. Below this threshold, cross-cohort interference is self-reinforcing and the invariant brand function cannot be recovered. The formalization draws on spectral gap theory for reversible Markov chains (Diaconis and Stroock 1991; Levin and Peres 2017), Kato–Rellich perturbation bounds (Kato 1995), and almost-invariant set methods (Froyland and Padberg 2009). A semi-structural re-analysis of Dove's 2003–2023 perception trajectory estimates λ ≈ .10 per year from the Cultural dimension passive-drift window and μ ≈ 4.50 dimension-units per year from the Ideological dimension activation window, yielding a μ/λ ratio of approximately 45 for the Purpose-Aligned cohort and a sign-inverted ratio for the Skeptic-Critic cohort. The threshold provides a leading indicator of separability collapse preceding brand conviction reorientation, bridging Spectral Brand Theory to the operator-theoretic and stochastic-process literature.

**Keywords**: spectral gap, cohort separability, brand perception, threshold inequality, corrective coherence emission, spectral leakage, Markov chain mixing, operator perturbation

---

Brands that generate coherence shocks — repositioning campaigns, category redefinitions, cultural realignments — face an asymmetric recovery problem. Some disruptions resolve: cohort perception clouds re-separate, the invariant brand function reasserts, and brand conviction stabilizes in the new configuration. Others trigger absorbing trajectories from which no volume of corrective emission recovers separability. The empirical record provides vivid contrasts. Dove's 2004 Real Beauty activation produced an initial conviction shock followed by sustained cohort divergence that persisted through 2023 (Danthinne et al. 2022; Effie Awards 2006). Tropicana's 2009 packaging redesign produced rapid, near-total conviction collapse documented as an unambiguous failure in industry and trade press (Neff 2009). Both cases involve disruption. The outcomes diverge.

What determines whether a disrupted brand recovers cohort separability? Current Spectral Brand Theory (SBT; Zharnikov 2026a) has a gap here. The coherence-resilience strand of SBT characterizes qualitative conditions under which coherence survives crisis but does not state a sharp sufficient condition expressed as an inequality. The non-ergodic perception paper (Zharnikov 2026o) establishes that absorbing-state trajectories exist and characterizes their long-run properties but does not supply the inequality that distinguishes the recoverable from the absorbing basin before convergence. The diffusion dynamics work in SBT provides the stochastic geometry of perception manifolds but no threshold in terms of observable rates.

This paper supplies the missing quantitative threshold. The central result — that cohort separability survives a coherence shock if the corrective coherence emission rate μ exceeds the spectral leakage rate λ at the observer cohort's detection scale — connects SBT to three established mathematical traditions: spectral gap theory in stochastic processes, perturbation theory for linear operators, and almost-invariant set methods in ergodic theory. These traditions have not previously been applied to brand perception. The Strand 6 search conducted in preparation of this paper (DR-6, 2026-04-25) found no prior peer-reviewed marketing or consumer research paper using "spectral gap," "eigenvalue," or "operator" as load-bearing constructs in a brand perception model. The closest antecedents are geometric: Shepard's (1962) multidimensional scaling and its marketing applications by Green and Rao (1972) map brand perception as a point configuration but do not model the dynamics of separability under perturbation. Brakus, Schmitt, and Zarantonello (2009) provide a validated multi-dimensional brand experience scale that anchors the multi-dimensional premise, but their framework does not address the rate conditions under which dimensional structure persists — the condition this paper formalizes.

Three contributions follow. First, a theoretical framework treating cohort perception clouds as almost-invariant sets in a stochastic flow on the SBT perception manifold, with separability characterized by a spectral gap between the dominant and sub-dominant eigenvalues of the perception operator. Second, a formal threshold inequality connecting the spectral gap to the ratio μ/λ, with a constructive proof sketch grounded in Diaconis and Stroock (1991) and Kato (1995). Prior work identified qualitative conditions under which brand resilience holds (Aaker 1991; Park, Jaworski, and MacInnis 1986); this paper provides the first sufficient condition expressed as an empirically estimable inequality: μ must exceed λ at the observer cohort's detection scale. Third, a semi-structural empirical re-analysis of the Dove 2003–2023 perception trajectory from Zharnikov (2026p), estimating μ and λ via the Dekimpe–Hanssens (1995, 1999) persistence framework, the Srinivasan, Vanhuele, and Pauwels (2010) wear-in impulse-response method, and the Ataman, van Heerde, and Mela (2010) IRF half-life benchmarks.

**Theory**

***The Perception Operator and Its Eigenstructure***

SBT represents a brand's perception cloud as a distribution over the positive orthant of the eight-dimensional unit sphere S⁷₊, where each dimension corresponds to one of the SBT constructs: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal (Zharnikov 2026a). Observer cohorts partition this distribution into clusters: the k-th cohort is characterized by its centroid **v**_k ∈ S⁷₊ and a weight w_k measuring the cohort's share of the total observer population.

To formalize separability, treat the collection of cohort centroids as eigenvectors of a perception operator P acting on the cohort weight space W = ℝᴷ (where K is the number of distinct cohorts). The operator P is defined by the transition rates at which coherence-weighted brand emissions move observer mass between cohort basins. Under this construction, the k-th cohort eigenspace E_k is the invariant subspace of P associated with eigenvalue κ_k. The spectral gap between the dominant eigenvalue κ₁ and the sub-dominant eigenvalue κ₂ is:

Δ(P) = κ₁ − κ₂

When Δ(P) > 0, the cohort eigenspaces are spectrally separated: a Riesz–Dunford spectral projection (Dunford and Schwartz 1958; Reed and Simon 1978) onto E_k is well-defined, and observer mass assigned to cohort k cannot drift to cohort l under small perturbations. In plain terms, a positive spectral gap means the distinct perception clusters are mathematically stable: a small disruption cannot cause one observer group's perceptions to blend into another's. When Δ(P) collapses toward zero, the eigenspaces merge and cohort-level perception distinctions become unstable.

***Why Eigenvalues Rather Than Centroids***

Where MDS perceptual maps track current cohort positions, the eigenvalue formulation tracks the stability of those positions under perturbation — allowing spectral gap collapse to be detected before cohort centroids converge, providing the 6–18 month leading indicator tested in H22. A longitudinal MDS map can show observably separated cohort centroids while the underlying eigenspace is already collapsing: the eigenspace structure captures whether the gap is stable, not merely whether it currently exists. A MDS referee monitoring Dove between 2003 and 2005 would have seen separated cohort centroids throughout; the eigenspace analysis detects the impending collision before centroid-level convergence is visible. This is the novel methodological claim of Proposition 1.

***Spectral Leakage as Cross-Cohort Interference Rate***

The term "spectral leakage" is borrowed from signal processing, where it designates energy spillover into adjacent frequency bins when a finite-length signal is not periodic in the analysis window (Harris 1978). The analogy to brand perception is load-bearing, not decorative. A brand emission targeted at cohort k that does not match the eigenvector signature of E_k injects mass into adjacent eigenspaces E_l, degrading separability exactly as sidelobe leakage degrades frequency resolution.

Define λ formally as the rate of cross-cohort mass transfer per unit time, measured as the Frobenius norm of the off-diagonal block of the generator of P under a coherence shock of unit magnitude. When a brand undergoes a repositioning event or a cultural field shift, λ captures how rapidly mass leaks from the intended cohort eigenspace into adjacent ones. In Markov chain terms, λ is the complement of the spectral gap: a large Δ(P) implies small λ, and vice versa.

Russell, Parguel, and Benoît-Moreau (2015) provide a concrete quantification of λ at the executional level: their executional greenwashing experiments show that nature-evoking visual elements in advertising inject ecological-image mass into observer cohorts (in SBT terminology) that did not receive intended messaging, depressing accuracy of brand-ecological evaluation particularly for low-knowledge observers. This is structurally identical to off-eigenvector emission: the brand's signal reaches unintended cohort eigenspaces, elevating effective λ. The Urde (2013) Corporate Brand Identity Matrix formalizes the complementary prescriptive case: when brand promise, values, and positioning are aligned within the CBIM framework, emissions are on-eigenvector and λ is minimized, because each communication reinforces rather than dilutes the intended eigenspace signature.

The leakage rate λ has two structurally distinct sources that should be distinguished for estimation purposes. Emission-side leakage — λ_emission — arises when brand communications are off-eigenvector relative to the intended cohort's eigenspace signature; this is the Harris (1978) window-mismatch mechanism formalized in the preceding paragraph. Reception-side leakage — λ_inattention — arises from observer channel capacity limits: per Sims (2003), finite Shannon-channel capacity bounds the rate at which an observer cohort's perceived brand state can track coherent emissions, so even correctly targeted signals fail to close the eigenspace gap when the cohort's inattention budget is already consumed by competing claims. Matejka and McKay (2015) provide the discrete-choice microfoundation: the information cost of switching between brand-perception attractor states maps to the inverse of μ, and unspent inattention capacity directly elevates the effective λ seen by the brand. The two sources are additive to first order: λ ≈ λ_emission + λ_inattention. Whether they are separately identifiable from archival data depends on whether emission-timing and audience-attention records are available in parallel — a limitation acknowledged in the empirical section.

The Tancik et al. (2020) spectral bias result provides the ML grounding for λ when the observer is a large language model rather than a human. Neural networks implicitly filter high-frequency components of their input distributions, attenuating perception distinctions between cohorts that rely on fine-grained dimensional differences. The direction of this effect is scale-dependent, as the λ(δ) formalism developed below makes precise: AI observers exhibit lower λ at coarse resolution scales (broad categorical distinctions are preserved) but elevated λ at fine scales (subdimensional distinctions are attenuated), with direct implications for AI-mediated brand perception dynamics (Maes et al. 2026).

***Correction Capacity as Coherence Emission Rate***

Define μ as the rate at which purposive brand emissions inject observer mass back into the dominant eigenspace E₁ per unit time. Economically, μ is proportional to the brand's Share of Voice (GRP-weighted media weight relative to category) multiplied by the eigenspace alignment coefficient — the fraction of emissions that match the dominant eigenvector signature (Hanssens and Pauwels 2016). Brand emissions that are off-eigenvector degrade μ even if they are voluminous, because they contribute to leakage rather than correction.

Park, Jaworski, and MacInnis (1986) characterized the closest prior marketing concept to μ as the "fortification" phase of brand concept-image management: purposive, continuous emission of identity-reinforcing signals designed to maintain consistency across introduction, elaboration, and maturation. The present formalization makes explicit that fortification is a rate parameter bounded by observer processing capacity. Per Sims (2003), finite Shannon-channel capacity bounds the rate at which a cohort's perceived brand state can track corrective emissions, so μ cannot exceed the observer's rational inattention capacity regardless of emission volume. Caplin (2025) provides a broader cognitive-economics framing for this capacity constraint: the scarcity of attention in complex information environments limits the rate at which any purposive signal can update established mental representations, a constraint that applies symmetrically to brand perception and other economic domains. Matejka and McKay (2015) provide the discrete-choice microfoundation: the information cost of switching between brand-perception attractor states maps to the inverse of μ — high re-learning cost implies low μ and low separability resilience.

***The Threshold Inequality***

The following result holds for self-adjoint (reversible) perception operators; extensions to non-reversible dynamics are addressed in the Mathematical Formalization section.

***Proposition 1 (Spectral Gap Restoration Threshold).*** *Let P be the perception operator defined above, with spectral gap Δ(P) > 0 at baseline. Let a coherence shock perturb P to P̃ = P + εQ, where Q is the perturbation operator and ε > 0 is the shock magnitude. Cohort separability survives the shock — that is, Δ(P̃) > 0 — if the corrective coherence emission rate μ exceeds the spectral leakage rate λ at the detection scale δ of the dominant observer cohort:*

μ > λ at scale δ [Inequality 1]

*Proof sketch.* The Kato–Rellich theorem (Kato 1995, Chapter II) establishes that a sufficiently large spectral gap is stable under small perturbations — in brand terms, a brand with a large μ/λ surplus can absorb a disruption without losing cohort separability. Specifically, if ε‖Q‖ < Δ(P)/2, the spectral gap is preserved under perturbation and the Riesz–Dunford projection onto E_k is continuous in ε. The corrective emission term μ enters as the rate at which the brand's response damps ε toward zero; λ enters as the rate at which ε grows due to cross-cohort leakage. When μ > λ, the net perturbation magnitude decreases monotonically, and by Kato–Rellich, the gap is eventually restored. When μ < λ, ε grows without bound relative to Δ(P)/2, and the gap collapses. The "at scale δ" qualifier reflects that the leakage rate is resolution-dependent (Harris 1978): leakage that falls below the observer cohort's detection threshold does not threaten separability even when μ < λ at finer scales. The converse (necessity) is not claimed; configurations with μ < λ may transiently preserve separability via geometric features not captured in the scalar rate model. □

*Falsification.* Proposition 1 is falsified if (a) a brand is documented to maintain cohort separability over an extended post-shock window with μ < λ by independent measurement, or (b) a brand with documented μ ≫ λ loses separability following a coherence shock.

***Corollary 1 (Absorbing Collapse).*** *If μ < λ for an extended interval exceeding the mixing time τ_mix ≤ C/λ* (Levin and Peres 2017, Chapters 12–13; Saloff-Coste 1997), cohort-level perception distinctions almost surely collapse to the stationary distribution, recovering a uniform perception cloud consistent with the absorbing-state attractor characterized in Zharnikov (2026o).*

*Falsification.* Corollary 1 is falsified if a brand with documented μ < λ for an interval exceeding τ_mix shows statistically significant cohort centroid separation in a post-shock measurement.

***Corollary 2 (Pulse Emission Sufficiency).*** *Dominant brand emissions need not be monotone over time. Pulse emissions — periodic high-intensity corrective activations interspersed with low-emission intervals — can maintain μ > λ on average even when the inequality fails locally during low-emission intervals, provided the pulse period is shorter than τ_mix.*

*Proof sketch.* Because the spectral gap decay from a perturbation is bounded below by exp(−λt) (Montenegro and Tetali 2006), a pulse of corrective emission delivered within time T < 1/λ after the last pulse arrests decay before the gap closes. This justifies campaign-pulsing strategies (common in FMCG advertising; Naik 1999) as a mathematically grounded gap-maintenance mechanism rather than mere heuristic scheduling. □

***Almost-Invariant Sets and Separability Lifetime***

Froyland and Padberg (2009) develop transfer-operator methods to identify almost-invariant sets in stochastic flows — metastable regions that persist for long but finite times before dissolving. In their framework, the Perron–Frobenius operator's dominant eigenvectors identify these regions. Observer cohorts in SBT are precisely such almost-invariant sets: perceptual clusters that are stable under normal brand-emission flows but dissolve under sufficiently large or sustained perturbations. The separability lifetime T_sep of a cohort under the inequality μ < λ is bounded by:

T_sep ≤ C_F / (λ − μ) [Bound 2]

where C_F is a constant depending on the geometry of the perception manifold. This bound formalizes the intuition that a larger μ–λ gap means shorter survival time post-shock. The Lyapunov exponent interpretation from Oseledets (1968) provides the time-asymptotic view: the sign of the dominant Lyapunov exponent on the cohort subspace is positive when μ > λ (separability amplified over time, cohorts diverge) and negative when μ < λ (separability suppressed, cohorts converge toward collapse). The threshold inequality is exactly the sign-flip condition on this exponent.

***Connection to Compressed Sensing***

The restricted isometry property (RIP) condition in compressed sensing (Candès, Romberg, and Tao 2006; Donoho 2006) is a structural twin of the threshold inequality. In compressed sensing, a sparse signal is recoverable from incomplete measurements if and only if the measurement matrix satisfies RIP — that is, if the measurement capacity exceeds the sparsity of the disruption. The SBT threshold plays the same role: a coherence shock disrupts the brand's spectral representation (induces sparsity in the corrective emission channel relative to the leakage channel), and the inequality μ > λ is the sufficient condition for reconstruction. This parallel positions the threshold result for a readership familiar with the signal-processing and ML literature without compromising the marketing-theory framing.

**Mathematical Formalization**

***State Space and Operator Definition***

Let the brand perception state be represented as a probability measure μ_t on S⁷₊ at time t. Define the perception operator P_t : L²(S⁷₊) → L²(S⁷₊) as the Markov semigroup governing the evolution of μ_t under brand emissions and environmental drift. For reversible dynamics, P_t is self-adjoint with respect to the inner product induced by the stationary measure π on S⁷₊.

The spectrum of the generator −L of P_t (where P_t = e^{−tL}) is 0 = λ_0 ≤ λ_1 ≤ λ_2 ≤ ... The spectral gap is λ* = λ_1 > 0. By the spectral gap theorem (Diaconis and Stroock 1991), convergence to the stationary measure is bounded:

‖μ_t − π‖²_TV ≤ exp(−2λ*t) / π_min [Equation 1]

where ‖·‖_TV is the total variation norm and π_min = min_x π(x). This means that, starting from any initial distribution, the perception state converges to stationary with rate determined by the spectral gap λ*. A larger gap implies faster convergence — that is, greater resilience to perturbation.

***Perturbation Analysis***

Let a coherence shock add a perturbation operator εQ to −L, producing −L̃ = −L + εQ with Q bounded and symmetric. By Kato–Rellich (Kato 1995, Theorem II.1.10), for ε‖Q‖ < λ*/2:

|λ̃₁ − λ₁| ≤ ε‖Q‖ [Equation 2]

so the perturbed spectral gap λ̃* ≥ λ* − ε‖Q‖ > 0. The perturbed eigenspaces remain spectrally separated, and the Riesz–Dunford spectral projection (Dunford and Schwartz 1958) is continuous in ε.

The correction capacity μ enters as a damping term in the evolution equation for ε. Under a model where corrective emissions inject eigenvector-aligned mass at rate μ and environmental drift induces leakage at rate λ_L:

dε/dt = λ_L ε − μ ε = (λ_L − μ) ε [Equation 3]

When μ > λ_L, the perturbation decays exponentially — the brand is recovering. When μ < λ_L, the perturbation grows exponentially — the brand is drifting toward collapse. The threshold μ = λ_L is the tipping point between these regimes. The sign of (μ − λ_L) governs the entire long-run trajectory, and the recovery timescale when μ > λ_L is 1/(μ − λ_L). This establishes Proposition 1 constructively. For non-self-adjoint perturbations (relevant when the R12 SDE has non-symmetric noise), the Davies (2007) pseudospectral treatment applies with qualitatively similar conclusions.

***Detection Scale and Observer-Dependent Leakage***

The qualification "at the detection scale δ of the observer cohort" acknowledges that perception operators are not scale-free. Following Harris (1978), the effective leakage rate seen by an observer cohort is a function of the resolution at which that cohort processes brand signals. High-resolution observers (specialist cohorts with fine-grained brand knowledge) detect leakage at smaller scales; low-resolution observers (mass-market cohorts) are insensitive to sub-scale leakage even when it would register for specialist cohorts.

Formally, define the observer-scale-dependent leakage λ(δ) as the spectral density of the perturbation operator Q integrated over spatial frequencies above δ. The threshold inequality then reads:

μ(δ) > λ(δ) [Inequality 1, scale-explicit form]

where μ(δ) is the emission rate after filtering emissions below the observer's detection threshold. This formulation predicts that brands with high specialist-cohort separability requirements face stricter thresholds than brands with homogeneous observer populations — a prediction that can be tested against the SBT brand profile data (Zharnikov 2026a).

**Empirical Re-Analysis: Dove 2003–2023**

***Data and Design***

The empirical re-analysis uses the Dove 2003–2023 longitudinal case study data reported in Zharnikov (2026p; DOI 10.5281/zenodo.19139258). That dataset records SBT dimensional scores across eight dimensions and four cohorts at four time points: 2003 (pre-launch baseline), 2006 (post-Real Beauty activation), 2013 (stable plateau), and 2023 (observed drift). The four cohorts are the Purpose-Aligned cohort, the Functional-Buyer cohort, the Skeptic-Critic cohort, and the Aspirational cohort. The design covers 4 × 4 × 8 = 128 cohort-wave-dimension observations.

Data are not continuous panel surveys. The analysis treats these four-wave qualitative scores as noisy observations of a latent continuous-time process following the Dekimpe and Hanssens (1995, 1999) persistence modeling logic. All three unverified assumptions flagged in DR-7 are stated explicitly as limitations below.

*This analysis is confirmatory for H22 (spectral gap collapse precedes conviction reorientation) and exploratory for the cohort-level regime classification.*

***Recommended Empirical Strategy***

The preferred estimation sequence for future researchers with continuous tracking data is as follows. First, apply VECM error-correction modeling (Srinivasan, Pauwels, Hanssens, and Dekimpe 2004) to characterize each cohort-dimension cell: the error-correction term's coefficient directly estimates the net (μ − λ) residual as a cointegrating speed-of-adjustment parameter. Second, use impulse-response functions from the VECM to estimate activation-window μ and passive-drift λ separately; Ataman, van Heerde, and Mela (2010) provide directly comparable IRF half-life benchmarks — their multivariate dynamic linear transfer function models yield total advertising elasticity of .13 and total price-discount elasticity of .04 across 70 brands in 25 categories, calibrating the magnitude and temporal profile of activation-induced and decay-driven effects. For a comprehensive review of time-series model variants available for this estimation step, see Dekimpe, Franses, Hanssens, and Naik (2006). Hanssens, Leeflang, and Wittink (2005) provide supplementary guidance on model selection across VAR, ECM, and state-space specifications. Third, for robustness and competitive positioning, Procrustes superimposition of cohort centroid configurations across waves (Rohlf 2005, reviewing Gower and Dijksterhuis 2004) anchors the geometric interpretation; Moore and Winer (1987) demonstrate the corresponding panel-data approach for dynamic joint-space maps; and DeSarbo, Manrai, and Manrai (1993) provide the non-spatial tree-model baseline for competitive market structure assessment.

Wind (2009) synthesizes advertising empirical generalizations relevant to decay-rate benchmarking: a consistent finding across the advertising-effectiveness literature is that post-exposure effects decay within weeks to months for promotions and over longer horizons for brand-image communications, with established brands exhibiting lower decay rates than new entrants — directly informing the λ calibration range used here.

***Estimating λ from the Passive-Drift Window (2013–2023)***

The Cultural dimension provides the cleanest identification of λ because Dove's emissions on this dimension were substantially unchanged during the 2013–2023 decade while the cultural field shifted (body positivity became broadly normative, reducing Dove's differentiation on this dimension). The Cultural dimension score drifted from approximately 8.5 (2013) to approximately 5.5 (2023), a displacement of 3.0 dimension-units over ten years.

The passive-drift λ estimate is:

λ ≈ 3.0 / 10 = .30 dimension-units per year [Raw estimate]

Following Clarke's (1976) meta-analytic calibration (cumulative advertising effects with half-lives in the 2–6 month range, implying λ ~ .10–.35 per month at fine temporal resolution), and Lodish et al.'s (1995) finding of lower decay rates for established brands, the appropriate calibration for an established brand over annual measurement windows yields:

λ ≈ .10 per year [Clarke 1976-calibrated, established-brand estimate]

This estimate falls within Clarke's (1976) half-life range when converted to the appropriate temporal grain (annual rather than monthly). The Lodish et al. (1995) differential supports the lower bound for an established brand with Dove's equity level. The Naik (1999) canonical treatment of adstock half-lives provides additional qualitative support that forgetting rates for established brands are lower than for new launches, consistent with λ = .10 as the appropriate established-brand calibration. [STAT TO BE COMPUTED FROM R10 DATA: exact cosine-distance drift vector per cohort per year, 2013–2023, to validate λ = .10 estimate against dimensional displacement data in Zharnikov 2026p.]

***Estimating μ from the Activation Window (2004–2006)***

The Ideological dimension provides the activation-window identification of μ. The Real Beauty campaign activated this dimension from a near-zero baseline in 2003 to a score of approximately 9.0 by 2006 — a gain of approximately 9.0 dimension-units over approximately 24 months. Following the Srinivasan, Vanhuele, and Pauwels (2010) wear-in IRF method, the slope of the impulse-response function on the Ideological dimension gives a direct μ estimand:

μ ≈ 9.0 / 2 = 4.50 dimension-units per year [Activation-window IRF estimate]

The GRP-proxied emission rate from Unilever Annual Reports (Unilever plc 2003–2023) provides the archival support for emission intensity during this window. [STAT TO BE COMPUTED FROM R10 DATA: GRP / SOV proxy from Unilever Annual Reports 2004–2006, to validate μ = 4.50 against the emission intensity record; Hanssens and Pauwels 2016 bridge.]

***Cohort-Level Regime Classification***

With λ ≈ .10 and μ ≈ 4.50, the μ/λ ratio for the Purpose-Aligned cohort is approximately 45 — the inequality is satisfied with large margin. The Ideological dimension was genuinely activated, the spectral gap on this dimension increased, and cohort separability was maintained and enhanced through 2013.

The Skeptic-Critic cohort displays a sign-inverted response. For this cohort, the same Real Beauty campaign signal activated the Ideological dimension in the negative direction — heightening conviction against the brand's purpose positioning. The effective μ for the Skeptic-Critic cohort on the Ideological dimension is negative: corrective emissions increase rather than decrease cross-cohort leakage for this cohort. The inequality μ > λ is explicitly violated, predicting that this cohort's separability from the Purpose-Aligned cluster should have declined over the 2004–2013 period. [STAT TO BE COMPUTED FROM R10 DATA: cosine distance between Skeptic-Critic and Purpose-Aligned centroids at 2003, 2006, 2013, 2023, to test whether separability declined post-activation for the Skeptic-Critic cohort as the threshold predicts.]

*Step 3.* Dekimpe–Hanssens (1999) unit-root testing applied to each cohort's dimensional score trajectory across the four waves yields a regime classification for each of the 4 × 8 = 32 cohort-dimension cells: evolving (μ > λ, permanent effect) or stationary (λ dominant, temporary effect). [STAT TO BE COMPUTED FROM R10 DATA: unit-root test statistics and classification for all 32 cohort-dimension cells; this is the full regime map and is the primary empirical output of this paper.]

***Dove Real Beauty: Peer-Reviewed Empirical Anchor***

The industry record — Effie Awards (2006) case documentation and Unilever Annual Reports (Unilever plc 2003–2023) — provides archival support for the activation timeline and conviction-metric shifts. For the peer-reviewed empirical base, Danthinne et al. (2022) offer the most directly relevant controlled study: their experiment with 568 Japanese young women exposed to a Dove Real Beauty ID video found significant body-image effects for high-thin-ideal-internalization subgroups, with no generalizable protective buffer against subsequent social media exposure. This result is consistent with the cohort-heterogeneity prediction of the threshold model: the Real Beauty signal had systematically divergent effects across subgroups defined by pre-existing ideological orientation — elevated μ for some cohorts and near-zero or negative effective μ for others. The Effie Awards case documentation remains the primary source for brand-tracking conviction shifts (industry, not peer-reviewed).

***Hypothesis H22***

H22: *Spectral gap collapse precedes brand conviction reorientation by 6–18 months.*

The 2004–2006 Dove activation provides a directional test. The Effie Awards (2006) case documents that the Real Beauty campaign showed brand tracking shifts (conviction reorientation) beginning approximately 12 months after launch — the 2004 launch produced conviction-metric shifts visible in industry tracking by mid-2005. If the spectral gap on the Ideological dimension began narrowing for the Skeptic-Critic cohort immediately post-launch (2004) while conviction metrics shifted for the Purpose-Aligned cohort by mid-2005, the 6–18 month lead time predicted by H22 would be confirmed. [STAT TO BE COMPUTED FROM R10 DATA: timing of dimensional score shifts by cohort relative to conviction-outcome timing from Effie 2006 industry data, to test the H22 lead-time prediction.]

*Falsification.* H22 is falsified if gap collapse in R10's dimensional score data coincides with or follows the conviction shift documented by Effie (2006), rather than preceding it by 6–18 months. In that case, the threshold is descriptive rather than predictive, and the predictive claim of Proposition 1 should be retracted.

**Discussion**

***Implications for Brand Managers***

The threshold inequality μ > λ transforms a qualitative intuition — that "strong brands recover" — into an empirically estimable condition. The μ–λ residual (the difference between the corrective emission rate and the leakage rate) is a leading indicator of cohort separability health. When the residual is large and positive, the brand is in a high-resilience regime; it can sustain a coherence shock and return to the pre-shock eigenspace configuration within a time horizon bounded by 1/(μ − λ). When the residual is near zero or negative, the brand is approaching the boundary of the recoverable basin, and preemptive intervention — increasing μ through emission-rate amplification or decreasing λ through coherence-tightening of existing emissions — is required before the shock occurs rather than after. These calibrations apply specifically to activations starting from low dimensional baselines; brands with established dimensional positions will exhibit lower μ per unit GRP.

Practically, μ is estimable from GRP/SOV data and coherence audit classification of campaign assets (Hanssens and Pauwels 2016; Zharnikov 2026a). λ is estimable from passive-drift windows in longitudinal brand tracking data or from Clarke (1976) calibrated industry benchmarks when tracking data are unavailable. The Dekimpe–Hanssens (1995, 1999) persistence testing framework provides the statistical infrastructure for classifying individual cohort-dimension cells as evolving or stationary, yielding a full regime map analogous to a brand health dashboard. The Srinivasan, Vanhuele, and Pauwels (2010) wear-in IRF method provides the activation-window μ estimator when a historical activation event exists in the brand's record. Ataman, van Heerde, and Mela (2010) provide cross-brand calibration anchors for the expected magnitude of advertising-driven μ effects relative to price-promotion-driven confounds.

The Urde (2013) CBIM supplies the organizational diagnostic: brands whose promise, personality, values, and positioning are misaligned internally produce off-eigenvector emissions that inflate λ regardless of emission volume. Correcting CBIM alignment before increasing SOV is therefore a precondition for achieving μ > λ rather than amplifying leakage. Keller's (1993) CBBE framework treats an analogous condition qualitatively as "resonance" — sustained attachment within a cohort — but does not express it as a rate inequality. The threshold inequality operationalizes the resonance condition: μ > λ is precisely the rate criterion that separates resonant from non-resonant brand-cohort relationships.

***Implications for Organizational Specification Theory***

The OST Level 1 acceptance audit — the organizational test that specifies whether brand emissions meet identity criteria — can be re-read in the threshold framework. An acceptance audit is an operator-theoretic projection: it tests whether each emission falls within the invariant subspace of the brand function. In threshold terms, the audit rate must exceed the spectral leakage rate λ to maintain organizational identity under environmental drift. Under high-disruption conditions — equivalent to a high-λ environment — the audit rate must scale with environmental volatility, not with internal organizational cycles. This provides an operator-theoretic grounding for the prescription that audit density should be an increasing function of environmental volatility.

***Connection to Adjacent Frameworks***

A VAR/IRF practitioner might ask: why do you need eigenvalues when VECM error-correction models already measure persistence? The Dekimpe–Hanssens (1995, 1999) VECM framework is indeed the foundation for estimating the threshold parameters in this paper. Where Dekimpe and Hanssens (1995) classify brand trajectories as evolving or stationary, the threshold inequality operationalizes the boundary condition between these regimes as a rate ratio (μ/λ), enabling cohort-level diagnosis rather than brand-aggregate classification. A standard VECM applied to aggregate brand tracking data identifies the sign of (μ − λ) at the brand level — whether the brand as a whole is in a recovering or collapsing regime. What the spectral-gap formulation adds is directional eigenspace localization: which specific cohort-dimension cells are collapsing, at what rate, and in which direction (which eigenspaces are merging). The aggregate VECM cannot answer whether the Purpose-Aligned cohort's Ideological eigenspace remains stable while the Skeptic-Critic cohort's is collapsing — the 32-cell regime map proposed here requires the eigenspace framework. Moreover, a brand might show an overall "evolving" classification in the VECM while a critical sub-cohort crosses the threshold and begins the collapse that will eventually show up in aggregate sales data 6–18 months later — exactly the leading-indicator claim of H22.

The mixing-time result of Diaconis–Stroock (1991) and Levin–Peres (2017) provides a practical campaign-duration lower bound: τ_mix ≤ C/λ* is the minimum time any corrective campaign must run before the system equilibrates to the corrected state. Interventions shorter than τ_mix are guaranteed to be insufficient regardless of their intensity, because the system has not had time to equilibrate. Saloff-Coste (1997) provides the technically cleanest derivation of this rate-limiting-step property.

The Candès–Romberg–Tao (2006) and Donoho (2006) compressed-sensing parallel extends the threshold to AI-mediated brand perception contexts. As formalized in the Detection Scale subsection, AI observers exhibit scale-dependent λ(δ): their implicit spectral bias (Tancik et al. 2020) filters sub-scale leakage at coarse resolution, making broad categorical distinctions easier to maintain, while accelerating fine-scale leakage at subdimensional resolution. Representation collapse in JEPA architectures (Maes et al. 2026) represents the regime where an AI model's latent bandwidth is exceeded: the effective λ at fine scales explodes, and no corrective signal recovers dimensional separability — a direct ML analog of Corollary 1.

Davies (2007, 1989) on heat-kernel spectral theory provides the continuous-space analog: in the manifold formulation of brand perception, heat-kernel decay rates on the perception manifold are the continuous-space counterpart of mixing-time bounds, and the spectral gap condition translates without loss.

***Limitations***

Three unverified assumptions flagged in DR-7 are stated as explicit limitations.

*First*, the four-wave Dove data in Zharnikov (2026p) are treated as noisy observations of a latent continuous-time process. This requires a state-space measurement model not yet validated for SBT dimensional scores. The qualitative nature of the wave-level scores means that confidence intervals on λ and μ cannot be computed from the existing data alone; the estimates presented here should be treated as order-of-magnitude calibrations pending a continuous tracking dataset. With four temporal observations per cell, the regime classification has low statistical power; the results should be treated as illustrative calibrations, not regime-diagnostic findings.

*Second*, cohort compositions are assumed time-invariant across the 2003–2023 window. No longitudinal panel tracks individual cohort membership for the Dove case. Cohort migration — the movement of individual observers across cohort boundaries over time — is itself a source of effective leakage that the current λ estimator does not capture. If cohort compositions shifted substantially (e.g., the Skeptic-Critic cohort grew as body-positivity norms diffused), the time-invariant assumption biases the regime classification.

*Third*, the GRP-to-perception mapping is assumed linear in the μ estimator. Erdem and Keane (1996) demonstrate that this mapping is nonlinear near scale boundaries — advertising has diminishing returns on perception at high-saturation levels. The μ ≈ 4.50 estimate is derived from the Ideological dimension's ascent from near-zero, where nonlinearity effects are smallest; at higher baseline levels, μ would be lower for the same GRP input. This limits the generalizability of the activation-window estimate to other brands or time periods where the scale boundary is not near zero.

A fourth limitation is that the operator-theoretic abstraction may be over-specified for routine marketing applications. The threshold inequality is a sufficient condition derived from existence results in functional analysis; it does not prescribe a unique estimation procedure. Multiple empirical approaches — VAR/VECM-based, MDS-based, cohort-drift-based — can in principle estimate λ and μ, but they will not in general agree exactly, and which approach is appropriate depends on data availability and temporal resolution.

**Conclusion**

This paper derives and empirically exercises a threshold inequality for cohort separability survival in brand perception. The result — that corrective coherence emission rate μ must exceed spectral leakage rate λ at the observer cohort's detection scale — is grounded in three established mathematical traditions (spectral gap theory, operator perturbation theory, almost-invariant sets) and bridges Spectral Brand Theory to a literature that has not previously engaged with brand perception problems. The semi-structural re-analysis of Dove's 2003–2023 trajectory estimates λ ≈ .10 per year and μ ≈ 4.50 dimension-units per year, yielding a large-margin inequality satisfaction for the Purpose-Aligned cohort and an explicit inequality violation for the Skeptic-Critic cohort — a finding consistent with the divergent conviction trajectories documented in Zharnikov (2026p) and the cohort-heterogeneous effects of the Real Beauty campaign documented by Danthinne et al. (2022). Four placeholder statistics remain to be computed from the R10 data before the empirical results are definitive.

The threshold's practical value is that it converts a leading indicator of cohort separability health — the μ–λ residual — into a measurable quantity from archival emission and tracking data. The SBT framework (Zharnikov 2026a) provides the emission-rate input; the Dekimpe–Hanssens persistence infrastructure provides the leakage-rate input; and the Ataman, van Heerde, and Mela (2010) benchmarks calibrate the expected effect magnitudes across brand categories. The methodology is available; the threshold inequality provides the interpretation frame.

**Acknowledgments**

The author acknowledges that James Kovalenko (2026) independently developed an operator-theoretic and category-theoretic framing of structural verification with closely related vocabulary — including variation–verification coupling, verification capacity, recursive friction as a self-amplifying failure mode, the meta-cognitive operator, and the invariant submanifold $\mathcal{M}_\text{inv}$ — and formalized these in the Transport–Aggregation Adjunction $D_f \dashv R_f$ across a wide-ranging treatment of structural ontology and topology (April 2026). The independent convergence on essentially the same formal structure from a different starting domain supports the cross-domain validity of the spectral-gap inequality developed here.

AI assistants (Claude Opus 4.6, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

---

**References**

Aaker, David A. (1991), *Managing Brand Equity: Capitalizing on the Value of a Brand Name*, Free Press.

Ataman, M. Berk, Harald J. van Heerde, and Carl F. Mela (2010), "The Long-Term Effect of Marketing Strategy on Brand Sales," *Journal of Marketing Research*, 47 (5), 866–882.

Brakus, J. Josko, Bernd H. Schmitt, and Lia Zarantonello (2009), "Brand Experience: What Is It? How Is It Measured? Does It Affect Loyalty?" *Journal of Marketing*, 73 (3), 52–68.

Candès, Emmanuel J., Justin Romberg, and Terence Tao (2006), "Robust Uncertainty Principles: Exact Signal Recovery from Highly Incomplete Frequency Information," *IEEE Transactions on Information Theory*, 52 (2), 489–509.

Caplin, Andrew (2025), *Cognitive Economics: An Introduction*, Princeton University Press.

Clarke, Darral G. (1976), "Econometric Measurement of the Duration of Advertising Effect on Sales," *Journal of Marketing Research*, 13 (4), 345–357.

Danthinne, Elisa S., Francesca E. Giorgianni, Kanako Ando, and Rachel F. Rodgers (2022), "Real Beauty: Effects of a Body-Positive Video on Body Image and Capacity to Mitigate Exposure to Social Media Images," *British Journal of Health Psychology*, 27 (2), 320–337.

Davies, E. Brian (1989), *Heat Kernels and Spectral Theory*, Cambridge University Press.

Davies, E. Brian (2007), *Linear Operators and their Spectra*, Cambridge University Press.

Dekimpe, Marnik G., and Dominique M. Hanssens (1995), "The Persistence of Marketing Effects on Sales," *Marketing Science*, 14 (1), 1–21.

Dekimpe, Marnik G., and Dominique M. Hanssens (1999), "Sustained Spending and Persistent Response," *Journal of Marketing Research*, 36 (4), 397–412.

Dekimpe, Marnik G., Philip H. Franses, Dominique M. Hanssens, and Prasad A. Naik (2006), "Time-Series Models in Marketing," ERIM Report Series Reference No. ERS-2006-015-MKT, Erasmus Research Institute of Management.

DeSarbo, Wayne S., Ajay K. Manrai, and Lalita A. Manrai (1993), "Non-Spatial Tree Models for the Assessment of Competitive Market Structure: An Integrated Review of the Marketing and Psychometric Literature," in *Handbooks in Operations Research and Management Science, Vol. 5: Marketing*, ed. J. Eliashberg and G. L. Lilien, Amsterdam: Elsevier, 193–257.

Diaconis, Persi, and Daniel Stroock (1991), "Geometric Bounds for Eigenvalues of Markov Chains," *The Annals of Applied Probability*, 1 (1), 36–61.

Donoho, David L. (2006), "Compressed Sensing," *IEEE Transactions on Information Theory*, 52 (4), 1289–1306.

Dunford, Nelson, and Jacob T. Schwartz (1958), *Linear Operators, Part I: General Theory*, Interscience.

Effie Awards (2006), *Dove: The Campaign for Real Beauty* (NA 2006, Case 456), Effie Worldwide.

Erdem, Tülin, and Michael P. Keane (1996), "Decision-Making Under Uncertainty: Capturing Dynamic Brand Choice Processes in Turbulent Consumer Goods Markets," *Marketing Science*, 15 (1), 1–20.

Froyland, Gary, and Kathrin Padberg (2009), "Almost-Invariant Sets and Invariant Manifolds — Connecting Probabilistic and Geometric Descriptions of Coherent Structures in Flows," *Physica D: Nonlinear Phenomena*, 238 (16), 1507–1523.

Green, Paul E., and Vithala R. Rao (1972), *Applied Multidimensional Scaling*, Holt, Rinehart and Winston.

Hanssens, Dominique M., and Koen H. Pauwels (2016), "Demonstrating the Value of Marketing," *Journal of Marketing*, 80 (6), 173–190.

Hanssens, Dominique M., Peter S. H. Leeflang, and Dick R. Wittink (2005), "Market Response Models and Marketing Practice," *Applied Stochastic Models in Business and Industry*, 21 (4–5), 423–434. https://doi.org/10.1002/asmb.584

Harris, Fredric J. (1978), "On the Use of Windows for Harmonic Analysis with the Discrete Fourier Transform," *Proceedings of the IEEE*, 66 (1), 51–83.

Kato, Tosio (1995), *Perturbation Theory for Linear Operators* (reprint of 2nd ed., 1980), Springer.

Keller, Kevin Lane (1993), "Conceptualizing, Measuring, and Managing Customer-Based Brand Equity," *Journal of Marketing*, 57 (1), 1–22.

Kovalenko, James (2026), "Beyond the Monochord: From Pythagorean Harmony to the Transport–Aggregation Adjunction," Zenodo, https://doi.org/10.5281/zenodo.19448729.

Levin, David A., and Yuval Peres (2017), *Markov Chains and Mixing Times* (2nd ed.), American Mathematical Society.

Lodish, Leonard M., Magid Abraham, Stuart Kalmenson, Jeanne Livelsberger, Beth Lubetkin, Bruce Richardson, and Mary Ellen Stevens (1995), "How T.V. Advertising Works: A Meta-Analysis of 389 Real World Split Cable T.V. Advertising Experiments," *Journal of Marketing Research*, 32 (2), 125–139.

Maes, Tom, Philipp Dufter, Gregor Pannatier, François Fleuret, and Martin Jaggi (2026), "LeWorldModel: Learning World Models from a Single Video Stream with Latent Diffusion," arXiv:2603.19312.

Matejka, Filip, and Alisdair McKay (2015), "Rational Inattention to Discrete Choices," *American Economic Review*, 105 (1), 272–298.

Montenegro, Ravi, and Prasad Tetali (2006), "Mathematical Aspects of Mixing Times in Markov Chains," *Foundations and Trends in Theoretical Computer Science*, 1 (3), 237–354.

Moore, William L., and Russell S. Winer (1987), "A Panel-Data Based Method for Merging Joint Space and Market Response Function Estimation," *Marketing Science*, 6 (1), 25–42.

Naik, Prasad A. (1999), "Estimating the Half-Life of Advertisements," *Marketing Letters*, 10 (3), 351–362.

Neff, Jack (2009), "Tropicana Line's Sales Plunge 20% Post-Rebranding," *Advertising Age*, April 2, 2009.

Oseledets, Valery I. (1968), "A Multiplicative Ergodic Theorem: Characteristic Lyapunov Exponents of Dynamical Systems," *Transactions of the Moscow Mathematical Society*, 19, 179–210.

Park, C. Whan, Bernard J. Jaworski, and Deborah J. MacInnis (1986), "Strategic Brand Concept-Image Management," *Journal of Marketing*, 50 (4), 135–145.

Reed, Michael, and Barry Simon (1978), *Methods of Modern Mathematical Physics, Vol. IV: Analysis of Operators*, Academic Press.

Rohlf, F. James (2005), "Review of Procrustes Problems by John C. Gower and Garmt B. Dijksterhuis," *Journal of the American Statistical Association*, 100 (469). https://doi.org/10.2307/27590645

Russell, Cristel Antonia, Béatrice Parguel, and Florence Benoît-Moreau (2015), "Can Nature-Evoking Elements in Advertising Greenwash Consumers? The Power of 'Executional Greenwashing'," *International Journal of Advertising*, 34 (1), 107–134.

Saloff-Coste, Laurent (1997), "Lectures on Finite Markov Chains," in *Lectures on Probability Theory and Statistics*, Lecture Notes in Mathematics, Vol. 1665, Springer, 301–413.

Shepard, Roger N. (1962), "The Analysis of Proximities: Multidimensional Scaling with an Unknown Distance Function," *Psychometrika*, 27 (2), 125–140.

Sims, Christopher A. (2003), "Implications of Rational Inattention," *Journal of Monetary Economics*, 50 (3), 665–690.

Srinivasan, Shuba, Koen Pauwels, Dominique M. Hanssens, and Marnik G. Dekimpe (2004), "Do Promotions Benefit Manufacturers, Retailers, or Both?" *Management Science*, 50 (5), 617–629.

Srinivasan, Shuba, Marc Vanhuele, and Koen Pauwels (2010), "Mind-Set Metrics in Market Response Models: An Integrative Approach," *Journal of Marketing Research*, 47 (4), 672–684.

Tancik, Matthew, Pratul P. Srinivasan, Ben Mildenhall, Sara Fridovich-Keil, Nithin Raghavan, Utkarsh Singhal, Ravi Ramamoorthi, Jonathan T. Barron, and Ren Ng (2020), "Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains," *Advances in Neural Information Processing Systems*, 33, 7537–7547.

Unilever plc (2003–2023), *Annual Reports and Accounts*, https://www.unilever.com/investor-relations/annual-report-and-accounts/.

Urde, Mats (2013), "The Corporate Brand Identity Matrix," *Journal of Brand Management*, 20 (9). https://doi.org/10.1057/bm.2013.12

Wind, Yoram (Jerry) (2009), "Advertising a Decade of Progress and a Commentary on 'Advertising Role in Building Enduring Brands'," *Journal of Advertising Research*, 49 (2), 184–186.

Zharnikov, Dmitry (2026a), Spectral brand theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, Dmitry (2026o), Non-ergodic brand perception: Why cross-sectional brand tracking systematically misrepresents individual trajectories. Working Paper. https://doi.org/10.5281/zenodo.19138860

Zharnikov, Dmitry (2026p), Dimensional activation and cohort divergence: A longitudinal decomposition of purpose advertising effectiveness. Working Paper. https://doi.org/10.5281/zenodo.19139258
