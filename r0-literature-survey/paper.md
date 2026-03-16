# Geometric Approaches to Brand Perception: A Critical Survey and Research Agenda

**Zharnikov, D.**

Working Paper -- March 2026

---

## Abstract

This paper presents a systematic survey of geometric and topological methods applied to brand perception, consumer behavior, and marketing science. Drawing on literature from multidimensional scaling, characteristics-space economics, conceptual spaces in cognitive science, non-Euclidean perceptual geometry, individual-differences modeling, topological data analysis, quantum cognition, opinion dynamics, and non-ergodicity research, we map the intellectual landscape at the intersection of formal geometry and brand theory. Our central finding is that a significant gap persists: no existing framework combines high-dimensional geometric structure, a generative signal mechanism, observer heterogeneity, and non-ergodic temporal dynamics into an integrated theory of brand perception. Multidimensional scaling, the dominant spatial method in marketing, typically operates in two to three dimensions and offers no generative mechanism. Conceptual spaces provide geometric foundations for cognition but lack temporal dynamics and observer-specific processing. Non-Euclidean perceptual geometry demonstrates that Euclidean distance is insufficient for modeling perception, yet this insight has not penetrated brand theory. Non-ergodicity has been formalized in psychology, decision science, and evolutionary biology, but has never been applied to brand perception or consumer loyalty trajectories. We propose six open problems at this intersection---concerning formal metrics on brand space, projection bounds, concentration of measure, positioning capacity, specification impossibility, and diffusion dynamics on perceptual manifolds---and argue that Spectral Brand Theory (Zharnikov, 2026a) represents a candidate framework positioned to address this compound gap.

**Keywords**: brand perception, geometric methods, multidimensional scaling, conceptual spaces, non-ergodicity, high-dimensional geometry, Spectral Brand Theory

**JEL Classification**: M31, C65, D91

**MSC Classification**: 91B42, 51K05, 62P20

**arXiv Subject Classes**: cs.LG, stat.ML

---

## 1. Introduction

Brand theory, as it has developed over the past four decades, is strikingly under-formalized. The foundational frameworks that guide both academic research and professional practice---Aaker's (1991) brand equity model, Keller's (1993) customer-based brand equity pyramid, Kapferer's (2008, 4th ed.) brand identity prism---are taxonomic rather than mathematical. They identify components, propose relationships, and offer measurement instruments, but they do not specify the formal structure of the space in which brands exist, the metric by which brand differences should be measured, or the dynamical laws governing how brand perceptions evolve over time. A recent systematic review confirmed that "no model allows comprehensive evaluation of brand equity" in a formally rigorous sense (Chernikov, 2024).

This absence of mathematical structure stands in sharp contrast to adjacent fields where geometric methods have produced transformative insights. In perception science, the discovery that human perceptual space is non-Euclidean---"at best Riemannian" (Todd, Oomes, Koenderink, and Kappers, 2001) and possibly non-Riemannian (Bujack, Teti, Miller, Caffrey, and Flatley, 2022)---has reshaped how researchers model visual and sensory experience. In cognitive science, Gardenfors's (2000) conceptual spaces framework demonstrated that natural concepts correspond to convex regions in geometric quality-dimension spaces, providing a formal bridge between perception and categorization. In economics, Lancaster's (1966) characteristics theory recast consumer choice as navigation through an n-dimensional attribute space, while Hotelling's (1929) spatial competition model placed firms on a geometric line. In physics and machine learning, high-dimensional geometry has revealed counterintuitive phenomena---concentration of measure, the curse of dimensionality, the Johnson-Lindenstrauss projection lemma---that fundamentally alter how systems behave as dimensions increase.

Meanwhile, the non-ergodicity revolution initiated by Peters (2019) has shown that the distinction between time averages and ensemble averages, long understood in statistical mechanics, has profound consequences for economics, psychology, and decision-making. When dynamics are multiplicative or absorbing states exist, population-level statistics (ensemble averages) systematically diverge from the trajectories of individual agents (time averages). This insight has been formalized in psychology by Molenaar (2004, 2009), tested experimentally by Meder, Rabe, Morville, and Tobler (2021) and Skjold, Brewer, and Peters (2024), and applied to evolutionary biology and organizational theory---but never to brand perception.

The purpose of this survey is to map these disparate literatures systematically and identify the precise intellectual gap that lies at their intersection. We argue that the gap is not merely an oversight but a structural consequence of disciplinary boundaries: marketing scholars have not engaged with high-dimensional geometry, while mathematicians and perception scientists have not examined brand phenomena. Spectral Brand Theory (SBT), proposed in Zharnikov (2026a), is a recent framework that models brands as eight-dimensional signal-emission profiles processed by heterogeneous observers through a generative pipeline with non-ergodic temporal dynamics. This survey establishes the intellectual genealogy for that framework and articulates six open problems that constitute a research agenda for mathematical brand theory.

A note on scope is required before proceeding. This survey is restricted to frameworks amenable to geometric formalization: frameworks that operate within metric spaces, manifolds, or at minimum well-defined vector spaces, and whose central claims can be stated as theorems about distances, curvature, or measure. Two important traditions in brand theory are deliberately excluded on these grounds. Holt's (2004) cultural branding tradition---exemplified in *How Brands Become Icons*---models brands as cultural resources whose meaning is constructed through collective storytelling, myth, and the appropriation of cultural contradictions. Fournier's (1998) relational tradition models the brand-consumer relationship on the analogy of interpersonal relationships, characterizing relationship quality along dimensions such as love, commitment, and intimacy. Both traditions have produced influential empirical work and provide deep insight into phenomena that geometric frameworks cannot easily capture: the political economy of cultural meaning-making, the role of community and ritual in brand worship, the dyadic quality of brand relationships over time. The exclusion of these traditions is a scope decision, not a value judgment.

The methodological basis for the exclusion is that both traditions are interpretive and qualitative rather than geometric and quantitative. Cultural branding proceeds through close reading of brand histories, consumer ethnographies, and cultural analysis; its central constructs (cultural contradiction, iconic myth) are not vectors, and its claims are not theorems. Relational branding similarly proceeds through interview, case study, and grounded theory; relationship quality dimensions are psychometric constructs, not geometric coordinates. Neither tradition has, to our knowledge, proposed a metric on the space of possible brand positions or derived formal bounds on brand differentiation. For the present survey---whose goal is to map the intellectual foundations of a formal geometric theory---the relevant question is not whether interpretive traditions provide valid accounts of brand phenomena (they do) but whether they contribute to the mathematical scaffolding that such a theory requires. They do not, and are therefore outside scope. Researchers seeking a comprehensive review of brand theory should consult interpretive and relational work alongside the present geometric survey.

The remainder of the paper is organized as follows. Sections 2 through 10 survey the relevant literatures in detail. Section 11 synthesizes these findings through a classification matrix assessing each tradition against six criteria. Section 12 formulates the research agenda as six specific open problems with mathematical formulations. Section 13 concludes.

## 2. Multidimensional Scaling in Marketing

### 2.1 Historical Foundations

The spatial representation of brand similarity in marketing traces its origins to Torgerson's (1952) development of classical (metric) multidimensional scaling. Torgerson demonstrated that a matrix of pairwise dissimilarities among stimuli could be embedded in a Euclidean space of low dimensionality, such that inter-point distances approximately preserved the original dissimilarity structure. This approach required the input proximities to possess metric properties---non-negativity, symmetry, the triangle inequality---and produced a configuration that was unique up to rotation, reflection, and translation.

The restriction to metric inputs was relaxed by Shepard (1962) and Kruskal (1964), who introduced non-metric MDS. In Kruskal's formulation, the algorithm seeks a spatial configuration whose inter-point distances have the same rank order as the original dissimilarities, without requiring that the relationship between distances and dissimilarities be linear. This innovation was consequential for marketing research because it acknowledged that consumer perceptual judgments are typically ordinal rather than interval-scaled. A consumer can reliably judge that Brand A is more similar to Brand B than to Brand C without being able to quantify the magnitude of the difference.

The subsequent decades saw extensive application of MDS to construct "perceptual maps" of product categories. Green and Rao (1972) demonstrated applications to consumer perception of breakfast cereals, automobiles, and other product categories. Cooper (1983) provided a comprehensive review of MDS applications in marketing research. Bijmolt and Wedel (1999) conducted a systematic comparison of MDS methods using marketing data, finding that non-metric approaches generally outperformed metric ones for typical marketing applications and that the choice of stress function and starting configuration significantly affected results.

### 2.2 Dimensionality: The Two-to-Three Convention

A striking feature of the MDS tradition in marketing is the near-universal restriction to two or three dimensions. This convention has both pragmatic and statistical justifications. Pragmatically, two-dimensional maps are visually interpretable: brand managers can literally see where their brand sits relative to competitors. Statistically, the "elbow" in the stress-versus-dimensionality curve typically occurs at two or three dimensions for marketing data, suggesting that additional dimensions capture noise rather than structure.

However, this convention obscures a deeper question: Is brand perception genuinely low-dimensional, or does the restriction to two to three dimensions reflect the limitations of human visual interpretation rather than the structure of brand experience? The stress function decreases monotonically with dimensionality; the "elbow" criterion is inherently subjective. When researchers have examined higher-dimensional solutions, they have found that axes beyond the second or third often lose correspondence to interpretable attributes and require post-hoc regression of external variables onto the coordinates to achieve meaning (Carroll and Chang, 1970).

This raises a fundamental issue that the MDS literature has not resolved. If the underlying perceptual space is genuinely higher-dimensional, low-dimensional MDS solutions are not merely approximate---they are systematically distorted projections. The Johnson-Lindenstrauss lemma (Johnson and Lindenstrauss, 1984) provides formal bounds on the distortion introduced by dimensionality reduction, but this result from theoretical computer science has never been connected to the MDS dimensionality-selection problem in marketing.

### 2.3 No Generative Mechanism

MDS, in all its variants, is a descriptive technique. It takes empirical dissimilarity data as input and produces a spatial configuration as output. It does not explain how brand perceptions are generated, how signals emitted by brands are processed by consumers, or why particular brands end up at particular locations in the space. The map is the territory, or rather, the map is all that MDS provides---without a theory of how the territory was formed.

This limitation is not unique to MDS; it is shared by all purely data-driven embedding methods, including modern approaches such as t-SNE (van der Maaten and Hinton, 2008) and UMAP (McInnes, Healy, Saul, and Grossberger, 2018). These methods have improved the quality of low-dimensional embeddings for visualization, but they remain descriptive rather than generative.

### 2.4 Bayesian and Probabilistic Extensions

Recent work has sought to enrich MDS with probabilistic structure. Oh and Raftery (2001) developed Bayesian MDS, which provides posterior distributions over point configurations rather than point estimates. Bakker and Poole (2013) applied Bayesian ideal-point models to political positioning data. These extensions address uncertainty quantification but do not add a generative mechanism or temporal dynamics.

The latent-class extensions of MDS (Bijmolt, Wedel, Pieters, and DeSarbo, 1998) allow for multiple consumer segments, each with its own spatial configuration or dimension weights. This is the closest the MDS tradition comes to modeling observer heterogeneity, but it treats segments as static, exogenous groupings rather than as emergent, dynamic observer cohorts.

## 3. Characteristics Space Models

### 3.1 Lancaster's New Consumer Theory

Lancaster's (1966) seminal paper, "A New Approach to Consumer Theory," proposed that consumers derive utility not from goods directly but from the characteristics (attributes) that goods embody. A good is modeled as a vector in an n-dimensional characteristics space, where each dimension corresponds to an objectively measurable attribute. Consumer choice is then a problem of navigating this space, subject to budget constraints that define a feasible set of characteristic bundles.

This reframing was geometrically consequential. Products are no longer abstract entities in a utility function; they are points (or rays, in the case of linear technologies) in a concrete vector space. Competition occurs when products occupy nearby positions in characteristics space. Innovation corresponds to the introduction of new products that access previously unoccupied regions.

Lancaster's framework has been extended in several directions. Rosen (1974) developed hedonic price theory, which relates the market price of a good to its position in characteristics space, with implicit prices for each characteristic determined by market equilibrium. This approach became foundational in housing economics and environmental valuation. In marketing, the characteristics-space perspective underpins conjoint analysis (Green and Srinivasan, 1978), where products are decomposed into attribute levels whose part-worths are estimated from consumer choice data.

### 3.2 Hotelling's Spatial Competition

Hotelling's (1929) "Stability in Competition" model placed competing firms on a linear segment (interpreted as geographic space or a single product attribute), with consumers distributed along the same line. Consumers choose the nearest firm, and firms compete by choosing locations. The model predicted the "principle of minimum differentiation"---that firms would cluster at the center of the line.

Extensions to multiple dimensions have been developed by dePalma, Ginsburgh, Papageorgiou, and Thisse (1985) and others. In multi-attribute space, the Hotelling model becomes a Voronoi partition problem: each firm captures all consumers who are closer to it than to any competitor. The geometry of Voronoi cells in high dimensions is significantly different from the one-dimensional case. In particular, the number of faces, edges, and vertices of Voronoi cells grows combinatorially with dimensionality, and the cells themselves become increasingly regular as dimension increases---a manifestation of concentration of measure.

### 3.3 Limitations

Lancaster's framework, despite its geometric elegance, embeds several restrictive assumptions. First, characteristics are assumed to be objective and universally perceived. All consumers observe the same attribute levels; they may differ in preferences (utility function weights) but not in perception. This rules out the observer heterogeneity that is central to brand experience, where the same brand signal may be perceived differently by different consumers depending on their prior experience, cultural context, and attentional weighting.

Second, the theory is static. Products have fixed positions in characteristics space; there is no mechanism for how perceptions of those positions evolve over time, how repeated exposure modifies the perceived attribute vector, or how signals decay. Third, the characteristics space is implicitly Euclidean and flat: distances are computed using the standard Euclidean metric, with no consideration of whether perceptual distances might be curved, dimension-dependent, or non-additive.

Peli and Nooteboom (1999) explored what happens as the number of characteristics dimensions grows in the context of organizational ecology, demonstrating that high-dimensional resource spaces create geometric "pockets" that sustain specialist niches. This is one of the few studies to examine the geometric consequences of dimensionality in a characteristics-space framework, but it focused on organizational populations rather than individual brand perception.

## 4. Conceptual Spaces

### 4.1 Gardenfors's Framework

Gardenfors's (2000) *Conceptual Spaces: The Geometry of Thought* represents perhaps the most ambitious attempt to place cognition on geometric foundations. The framework proposes three levels of cognitive representation: the subsymbolic level (neural networks), the conceptual level (geometric spaces), and the symbolic level (language and logic). The conceptual level is modeled as a collection of quality dimensions---cognitively meaningful attributes such as hue, brightness, temperature, pitch, or any other dimension along which stimuli can be ordered.

Quality dimensions are organized into domains, where a domain consists of a set of integral dimensions (dimensions that cannot be perceived independently, such as hue and saturation in color). Concepts are represented as regions in conceptual space, and the central theoretical claim is the *Criterion P*: natural properties correspond to convex regions in conceptual space. If two objects are both classified as "red" (or "luxurious" or "reliable"), then any object that lies on the straight line between them in the relevant quality-dimension space should also be classified as red (or luxurious or reliable).

This convexity criterion has deep implications. It provides a geometric characterization of what makes a concept "natural" versus "gerrymandered." It connects categorization to distance: a prototype sits at the center of a convex region, and the boundaries of the region define the limits of the category. It also enables the use of Voronoi tessellations, where category boundaries are determined by proximity to prototypes.

### 4.2 Applications to Brand and Product Perception

Several researchers have applied conceptual-spaces ideas to marketing contexts. Warglien and Gartner (2004) used conceptual spaces to model how brand meanings are constructed and communicated. Aisbett and Gibbon (2001) explored the mathematical properties of concept combination in conceptual spaces, with implications for how consumers combine brand attributes into overall judgments.

More recently, word embedding models from natural language processing (Mikolov, Sutskever, Chen, Corrado, and Dean, 2013) have been interpreted as high-dimensional conceptual spaces that encode brand meaning from textual data. Brands that are described in similar contexts end up close together in the embedding space, providing a data-driven approximation to the conceptual-spaces framework.

Vogt (2006) and Steels (2012) explored how conceptual spaces evolve through agent interaction, using "discrimination games" in which agents negotiate the boundaries of concepts through communicative encounters. This provides a rudimentary temporal dynamic but remains focused on concept formation rather than brand perception specifically.

### 4.3 Strengths and Gaps

The conceptual-spaces framework has several notable strengths for brand theory. It provides an explicit geometric foundation for multi-attribute perception. It connects perception to categorization via convexity. It is compatible with both top-down (linguistically defined) and bottom-up (perceptually grounded) quality dimensions.

However, four significant gaps limit its applicability to brand perception:

*No temporal dynamics*. Conceptual spaces are essentially static. While Gardenfors discusses conceptual change, the framework provides no formal model of how perceptions evolve over time in response to signal encounters, no mechanism for signal decay or memory effects, and no account of path dependence.

*No observer heterogeneity*. The framework assumes a universal conceptual space shared by all cognitive agents. Individual differences in how quality dimensions are weighted, how domains are organized, or how concepts are bounded are not modeled. Recent work on "personalized value spaces" (Bechberger, 2019) has begun to address this, but the field remains in its early stages.

*No generative mechanism*. Conceptual spaces describe the structure of concepts but not how concepts are created through the processing of signals. There is no analog to a brand emitting signals along multiple dimensions, those signals being filtered through observer-specific processing, and the result accumulating into a perception.

*Euclidean assumption*. Gardenfors assumes that quality dimensions are equipped with Euclidean or at least metric structure. This is a strong assumption given the evidence that human perceptual space is non-Euclidean (see Section 6).

## 5. Non-Euclidean Perceptual Geometry

### 5.1 The Structure of Perceptual Space

A foundational question for any geometric theory of brand perception is: What is the geometric structure of the space in which perceptions live? The default assumption in marketing---implicit in MDS, Lancaster's theory, and conjoint analysis---is that this space is Euclidean. Distances are computed using the Pythagorean formula. The triangle inequality holds strictly. The space is flat, with no curvature.

Evidence from perceptual psychology challenges this assumption at every level. Todd, Oomes, Koenderink, and Kappers (2001) conducted experiments on visual perception of three-dimensional scenes and found that observers are accurate at judging topological properties (connectedness, inside/outside), ordinal properties (relative distance), and affine properties (parallelism, betweenness), but are remarkably poor at judging Euclidean metric properties such as absolute distance, angle, and shape. Their conclusion was that "the effective geometry of spatial vision is, at best, some form of Riemannian geometry rather than Euclidean."

This "at best" qualification proved prescient. Bujack, Teti, Miller, Caffrey, and Flatley (2022), publishing in *Proceedings of the National Academy of Sciences*, demonstrated that perceptual color space is not merely non-Euclidean but non-Riemannian. They identified a "principle of diminishing returns" along the luminance axis: large color differences appear perceptually smaller than the sum of the small perceptual steps composing them. In Riemannian geometry, global distances are computed by integrating local metric elements along geodesics; the diminishing-returns finding violates this principle, implying that the metric structure of perceptual color space cannot be captured by any Riemannian manifold.

### 5.2 Implications for Brand Perception

If the geometry of perceptual space is non-Euclidean even for the relatively simple case of color (three dimensions: hue, saturation, luminance), the assumption that multi-attribute brand perception lives in a Euclidean space is almost certainly wrong. Brand perception involves dimensions that are more abstract, more culturally constructed, and more context-dependent than color. The semiotic, narrative, ideological, experiential, social, economic, cultural, and temporal dimensions proposed in SBT (Zharnikov, 2026a) are each likely to have their own metric structure, and the combined space is unlikely to be a simple product of Euclidean dimensions.

The practical implication is that Euclidean distance between brand profiles---the default in perceptual mapping, conjoint analysis, and MDS---may systematically misrepresent the perceptual differences that consumers actually experience. Large repositioning moves may appear smaller than the sum of incremental steps. Differences along some dimensions may be compressed relative to others in ways that depend on the observer's current position in the space.

### 5.3 Information Geometry

A candidate framework for modeling non-Euclidean perceptual spaces is information geometry (Amari, 2016). Information geometry equips the space of probability distributions with a Riemannian metric---the Fisher-Rao metric---derived from the Fisher information matrix. In this framework, the "distance" between two probability distributions is not the Euclidean distance between their parameters but the geodesic distance on the statistical manifold.

If brand perceptions are modeled as probability distributions over possible brand states (rather than as point estimates), information geometry provides a natural metric structure. The Fisher-Rao metric has desirable properties: it is invariant under sufficient statistics, it is the unique Riemannian metric invariant under Markov embeddings (Cencov, 1982), and it naturally accounts for the fact that differences in parameters have different perceptual significance depending on where one is in parameter space.

Information geometry has been applied to neuroscience (Amari, Nagaoka, and Harada, 2000) and signal processing (Costa, Hero, and Vignat, 2005), but not to brand perception or marketing. This represents an opportunity for formal brand theory.

## 6. Individual Differences and Dimension Weighting

### 6.1 The INDSCAL Tradition

The Individual Differences Scaling model (INDSCAL), introduced by Carroll and Chang (1970), was the first systematic attempt to model individual differences in perceptual space within a spatial framework. INDSCAL assumes that all individuals share a common set of perceptual dimensions but differ in the weights they assign to each dimension. Formally, the distance between stimuli $i$ and $j$ for subject $k$ is:

$$d_{ijk} = \left[ \sum_{r=1}^{R} w_{kr} (x_{ir} - x_{jr})^2 \right]^{1/2}$$

where $x_{ir}$ is the coordinate of stimulus $i$ on dimension $r$, and $w_{kr} \geq 0$ is the weight that subject $k$ assigns to dimension $r$. High weight means the dimension is perceptually salient for that individual; zero weight means the dimension is ignored.

INDSCAL was a significant conceptual advance because it formalized the idea that the same stimulus configuration could be perceived differently by different people. The weight vector $\mathbf{w}_k = (w_{k1}, \ldots, w_{kR})$ is a profile of dimensional salience---a precursor to what SBT calls the observer spectral profile. However, INDSCAL's weights are static (estimated from a single set of judgments), non-negative but otherwise unconstrained (no normalization requirement), and estimated within the MDS framework's typical two-to-three dimensions.

### 6.2 Latent-Class Unfolding Models

DeSarbo and colleagues (DeSarbo, Kim, Choi, and Spaulding, 2002; DeSarbo and Hoffman, 1986) developed a more sophisticated approach through latent-class MDS and unfolding models. These models assume that the population consists of a finite number of latent classes, each with its own ideal-point configuration and/or dimension weights. The latent classes are estimated simultaneously with the spatial configuration, allowing for endogenous segmentation.

The DeSarbo tradition represents the closest statistical precedent to SBT's observer cohort concept. In both frameworks, consumers are grouped based on their perceptual processing rather than demographic characteristics. The key differences are:

First, DeSarbo's latent classes are static, whereas SBT's observer cohorts are dynamic---observers drift between cohorts as priors evolve and signals decay.

Second, DeSarbo's models lack temporal dynamics. The ideal points and weights are estimated from cross-sectional data. There is no mechanism for how an observer's weights change over time in response to signal encounters.

Third, the models operate in low-dimensional spaces (typically two to four dimensions) and do not examine the geometric consequences of higher dimensionality, such as concentration of measure or projection distortion.

Fourth, and most fundamentally, DeSarbo's models are statistical estimation procedures, not generative theories. They fit models to data but do not specify how brand signals are generated, transmitted, filtered, and accumulated.

### 6.3 The Missing Step to Formal Metric Spaces

The dimension-weighting literature has established, both theoretically and empirically, that consumers differ in how they weight perceptual dimensions and that these differences are consequential for brand evaluation. What the literature has not done is take the next step: defining a formal metric space for these observer profiles, specifying the geometry of the space of possible weightings, or deriving the mathematical consequences of that geometry.

If observer profiles are normalized vectors (weights summing to one), they live on the probability simplex $\Delta^{R-1}$. If they are non-negative vectors of arbitrary magnitude, they live in the positive orthant $\mathbb{R}^R_+$. Each choice of space has different geometric properties---different notions of distance, different curvature, different concentration behavior. The dimension-weighting literature has treated weights as statistical parameters to be estimated rather than as geometric objects with intrinsic structure.

## 7. Topological Data Analysis in Marketing

### 7.1 TDA Fundamentals

Topological Data Analysis (TDA) provides tools for examining the "shape" of data through the lens of algebraic topology. The core method, persistent homology, constructs a nested sequence of simplicial complexes (a filtration) from point-cloud data and identifies topological features---connected components ($\beta_0$), loops ($\beta_1$), voids ($\beta_2$), and higher-dimensional analogues---that persist across multiple scales. Features that persist over a wide range of scales are interpreted as genuine structural properties, while those that appear and disappear quickly are treated as noise (Edelsbrunner and Harer, 2010; Carlsson, 2009).

Persistence diagrams and barcodes provide compact visual summaries of topological features and their lifespans. Importantly, TDA is coordinate-free: it depends only on pairwise distances between data points, not on any particular embedding. This makes it robust to the choice of distance metric and dimensionality reduction, unlike MDS-based approaches.

### 7.2 Applications in Adjacent Fields

TDA has found applications in several domains adjacent to marketing. In financial markets, Yen and Cheong (2021) used Betti numbers and Euler characteristics to detect structural changes associated with market crashes in the Singapore and Taiwan stock exchanges. During crashes, the market topology fragments---persistent topological features disappear as correlations between assets break down.

In social network analysis, persistent homology has been applied to detect community structure, identify influential nodes, and track the evolution of network topology over time. In biology, TDA has been used to analyze protein structures, neural population activity, and genomic data.

### 7.3 The Marketing Gap

Despite these applications, TDA has seen minimal adoption in marketing science. A search of major marketing and economics databases (Journal of Marketing Research, Journal of Consumer Research, Marketing Science, Journal of Marketing, and Management Science) yielded no published applications of persistent homology, Mapper algorithms, or other TDA methods to brand perception, consumer segmentation, or competitive positioning. The closest applications are in customer network analysis, where hypergraph models (Yen and Cheong, 2021) have been used to represent multi-item consumer collections, and in sentiment analysis, where topological features of text data have been explored.

This represents a missed opportunity. Brand perception data---multi-attribute ratings of multiple brands by multiple consumers---are naturally high-dimensional point clouds. TDA could reveal structural features of brand-perception spaces that are invisible to MDS: holes in the perceptual map (regions of brand space that no existing brand occupies), loops (cyclical patterns in brand evolution), and higher-dimensional voids (structural gaps in multi-attribute coverage). The coordinate-free nature of TDA would also sidestep the difficult question of which distance metric is "correct" for brand perception.

The absence of TDA in marketing is likely attributable to the same disciplinary boundary that has kept other advanced geometric methods out of brand theory: the techniques were developed by mathematicians and computer scientists who have no professional engagement with marketing phenomena.

## 8. Quantum Cognition Models

### 8.1 Hilbert Space Formalism for Decision-Making

Quantum cognition applies the mathematical formalism of quantum theory---complex Hilbert spaces, projection operators, unitary evolution---to model cognitive phenomena that violate the axioms of classical probability theory (Busemeyer and Bruza, 2012). The motivation is not that the brain is a quantum computer, but that the mathematical structure of quantum theory provides parsimonious accounts of several well-documented cognitive phenomena.

In this framework, a cognitive state is represented as a normalized vector $|\psi\rangle$ in a finite-dimensional Hilbert space $\mathcal{H}$. A judgment or decision corresponds to a measurement, which projects the state onto a subspace and yields probabilities via the Born rule: $P(\text{outcome}) = |\langle \phi | \psi \rangle|^2$. Crucially, successive measurements generally do not commute---the order in which questions are asked affects the answers---which provides a natural account of order effects in survey data.

Busemeyer and Bruza (2012) demonstrated that quantum models account for several empirical phenomena that classical models cannot easily explain:

*Conjunction fallacy*. Subjects judge the conjunction of two events as more probable than one of the events alone, violating classical probability. In the quantum model, this occurs because the state vector is projected through the conjunction subspace at a different angle than through either individual subspace.

*Order effects*. The probability of endorsing statement A followed by statement B differs from the probability of endorsing B followed by A. In quantum theory, this reflects the non-commutativity of the corresponding projection operators.

*Disjunction effect*. Subjects behave differently when told the outcome of a gamble than when left in uncertainty, even when they would make the same choice regardless of the outcome. The quantum model accounts for this through interference between the "win" and "lose" amplitudes.

### 8.2 Applications to Brand Perception

The quantum cognition framework has been applied to several aspects of consumer decision-making. Khrennikov (2016) and Pothos and Busemeyer (2022) have explored how quantum-like models capture context-dependence in preference formation. The "entanglement" concept has been used to model non-separable attribute evaluations, where the perception of one brand attribute (e.g., luxury) is intrinsically linked to another (e.g., exclusivity) in a way that exceeds classical correlation.

However, quantum cognition has not been applied to brand perception formation as a temporal, cumulative process. The models are primarily concerned with single-shot decisions: at the moment of choice, the cognitive state collapses from a superposition to a definite outcome. This snapshot formalism does not address how brand perceptions are built up over time through repeated signal encounters, how signals decay, or how past experiences create priors that shape future perception.

### 8.3 Relationship to SBT

The quantum cognition framework and SBT share certain structural features: both use vector spaces to represent perceptual states, both model observer-dependent processing, and both acknowledge non-classical effects in human cognition. However, the frameworks differ in important ways.

SBT uses a real-valued vector space (non-negative signal intensities across eight dimensions) rather than a complex Hilbert space. SBT's observer spectral profiles are explicit weighting functions on the signal dimensions, not abstract measurement bases. Most importantly, SBT provides a generative pipeline---emission, filtering, clustering, collapse---that quantum cognition lacks. Quantum cognition explains the structure of a single decision; SBT attempts to explain how the perceptual state that precedes the decision was formed through a history of signal encounters.

## 9. Opinion Dynamics and Multi-Agent Models

### 9.1 Bounded Confidence Models

The study of opinion dynamics examines how the beliefs of interacting agents evolve over time. The Hegselmann-Krause (HK) model (Hegselmann and Krause, 2002) and the Deffuant-Weisbuch (DW) model (Deffuant, Neau, Amblard, and Weisbuch, 2000) are the two canonical frameworks. Both incorporate "bounded confidence": agents update their opinions only when interacting with others whose opinions are sufficiently close.

In the HK model, each agent holds a real-valued opinion $x_i(t) \in [0, 1]$, and at each time step, updates by averaging the opinions of all agents within a confidence bound $\epsilon$:

$$x_i(t+1) = \frac{1}{|N_i(t)|} \sum_{j \in N_i(t)} x_j(t), \quad N_i(t) = \{j : |x_j(t) - x_i(t)| \leq \epsilon\}$$

The model produces three qualitative regimes depending on $\epsilon$: consensus (large $\epsilon$), polarization (intermediate $\epsilon$), and fragmentation (small $\epsilon$). These regimes have natural analogs in brand perception: consensus corresponds to a market where all consumers perceive brands similarly, fragmentation corresponds to highly heterogeneous observer cohorts.

Extensions to multiple dimensions (Lorenz, 2007) replace the scalar opinion with a vector $\mathbf{x}_i(t) \in \mathbb{R}^d$ and the confidence bound with a ball of radius $\epsilon$ in $\mathbb{R}^d$. Multi-dimensional bounded confidence exhibits qualitatively different behavior from the one-dimensional case: the number of final opinion clusters depends on both $\epsilon$ and the dimensionality $d$, and the geometry of the opinion space matters in ways that have not been fully explored.

### 9.2 DeGroot Social Learning

The DeGroot (1974) model provides a simpler framework for opinion dynamics, where agents update by forming weighted averages of their neighbors' opinions at each time step. Under mild connectivity conditions, the system converges to consensus. The model has been extensively studied in the context of social learning, information aggregation, and group decision-making.

Golub and Jackson (2010) extended DeGroot's model to study the speed of social learning and the conditions under which a society reaches approximately correct beliefs. They showed that the rate of convergence depends on the spectral gap of the influence matrix---the difference between the largest and second-largest eigenvalues---which determines how quickly disagreements decay.

### 9.3 Gaps Relative to Brand Perception

Opinion dynamics models share several features with brand perception: they model interacting agents with heterogeneous states, they exhibit emergent clustering, and they can produce path-dependent outcomes. However, they differ from the brand-perception problem in several fundamental ways:

*Flat Euclidean space*. Opinion dynamics models operate in Euclidean space (or on the real line), with distances measured using the standard Euclidean metric. There is no consideration of curved spaces, non-Euclidean metrics, or observer-dependent distance functions.

*No absorbing states*. Standard opinion dynamics models are dissipative: opinions converge toward consensus or stabilize at cluster centers. They do not model absorbing states---irreversible outcomes from which recovery is impossible. In brand perception, a sufficiently negative experience can produce permanent conviction ("I will never buy that brand again") that functions as an absorbing state.

*No signal generation*. Opinions evolve through peer-to-peer interaction; there is no analog to a brand organization emitting signals through deliberate actions, marketing communications, or product experiences. The opinion dynamics framework models social influence but not the organizational production of meaning.

*Symmetric interaction*. In most opinion dynamics models, interaction is symmetric or at least bidirectional: agent $i$ influences agent $j$ and vice versa. In brand perception, the relationship is fundamentally asymmetric: the brand emits signals and the observer processes them, but the observer's perception does not (directly) change the brand's emissions.

## 10. Non-Ergodicity Beyond Economics

### 10.1 Peters's Ergodicity Economics

Peters (2019) identified a fundamental error in the foundations of decision theory under uncertainty. Expected utility theory, since Bernoulli (1738), has evaluated gambles by their ensemble average---the average outcome across many parallel realizations. Peters showed that for multiplicative dynamics (where gains and losses compound), the ensemble average diverges from the time average experienced by a single agent over many sequential realizations. The ensemble average of a multiplicative gamble can be positive while the time average is negative, meaning that a gamble that looks favorable from a population perspective can be ruinous for any individual who plays it repeatedly.

The formal distinction is as follows. For a multiplicative process $W(t+1) = W(t) \cdot r_t$, where $r_t$ is a random return, the ensemble average growth rate is $\langle r \rangle = E[r_t]$ (the arithmetic mean of returns), while the time-average growth rate is $\bar{g} = E[\ln r_t]$ (the expected logarithmic return). The process is non-ergodic when $\langle r \rangle \neq e^{\bar{g}}$, which occurs whenever $r_t$ has non-zero variance.

This result has profound implications. "Risk aversion" in expected utility theory requires a concave utility function, which is treated as a psychological preference. In ergodicity economics, risk aversion is a structural consequence of the non-ergodic dynamics: agents who maximize the time-average growth rate behave as if they have logarithmic utility, not because of a psychological preference but because logarithmic utility happens to optimize long-run survival under multiplicative dynamics.

### 10.2 Non-Ergodicity in Psychology

Molenaar (2004) published what he termed a "manifesto on psychology as idiographic science," arguing that the standard practice of inferring individual psychological processes from group-level (between-person) data is valid only if the psychological system is ergodic---that is, only if the within-person process is stationary (its statistical properties do not change over time) and the population is homogeneous (all individuals share the same process). Since psychological processes are inherently non-stationary and populations are inherently heterogeneous, the ergodic assumption almost never holds.

Molenaar (2009) formalized this further and proposed person-specific (idiographic) analysis as the appropriate alternative: time-series analysis of individual trajectories rather than cross-sectional comparison of population aggregates. This has led to the development of several formal tools:

The *Ergodicity Information Index* (EII) measures the distance between within-person and between-person statistical structures (Fisher, Medaglia, and Jeronimus, 2018). When EII is near zero, the process is approximately ergodic and group-level statistics are informative about individuals. When EII is large, the process is non-ergodic and group-level statistics are misleading.

*Dynamic Factor Analysis* (DFA) allows factor structures to evolve over time within an individual, testing for factor invariance and capturing the non-stationarity that characterizes real psychological processes.

*P-technique Factor Analysis* captures the covariation of measures within a single person over many measurement occasions, providing idiographic factor structures that may differ qualitatively from nomothetic (group-level) factor structures.

Research citing Molenaar has identified several psychological processes that are fundamentally non-ergodic, including cognitive development and learning (non-stationarity of the developing brain makes cross-sectional education data unreliable), emotional regulation (daily fluctuations governed by idiographic parameters that do not aggregate), and behavioral health interventions (predictors of behavior change that vary between individuals).

### 10.3 Experimental Evidence

Meder, Rabe, Morville, and Tobler (2021) provided direct experimental evidence that humans are sensitive to the distinction between ergodic and non-ergodic environments. Participants in their experiments differentiated between additive gambles (where the ensemble and time averages coincide) and multiplicative gambles (where they diverge), exhibiting higher risk aversion in multiplicative settings. This is consistent with time-average optimization and inconsistent with expected-value maximization.

Skjold, Brewer, and Peters (2024) extended this to additive environments with absorbing boundaries (ruin). Even when dynamics are additive, the presence of a lower wealth bound creates non-ergodicity because trajectories that reach zero are absorbed (eliminated). Participants demonstrated sensitivity to the "distance to ruin," increasing risk aversion as their wealth approached the boundary. This behavior is naturally explained by time-average optimization, which accounts for the absorbing boundary, but is anomalous under standard expected utility theory.

Peters and Skjold (2024) used agent-based models to show that time-average optimization leads to the spontaneous emergence of cooperation and insurance in network settings, providing a mechanism-based account of social phenomena that standard economic theory attributes to psychological preferences or social norms.

### 10.4 Non-Ergodicity in Biology and Ecology

The non-ergodicity concept has found productive application in evolutionary biology. In population genetics, the ensemble-average fitness of a genotype (computed across many parallel populations) can differ from its time-average fitness (computed along a single lineage over many generations). This occurs because demographic stochasticity introduces multiplicative noise: a small population that experiences a sequence of bad years may go extinct even if its expected growth rate is positive.

Models using geometric Brownian motion for population dynamics (as in financial economics) exhibit a characteristic signature of non-ergodicity: the ensemble average grows exponentially while the median trajectory declines to zero (Bouchaud and Mezard, 2000). In biological terms, the "average species" thrives while most individual species go extinct---a pattern observed empirically in macroevolution.

The absorbing state in evolutionary dynamics is extinction. Once a lineage or population reaches zero, it cannot recover. This irreversibility is the biological analog of ruin in economics and, as we argue, of permanent negative conviction in brand perception.

### 10.5 The Marketing Gap

Despite the extensive application of non-ergodicity to psychology, decision science, ecology, and organizational theory, a comprehensive search reveals no published work applying Peters's formalism to brand perception, customer loyalty, or marketing metrics.

This gap is significant because brand perception exhibits all the hallmarks of non-ergodic dynamics:

*Multiplicative compounding*. Brand signals do not simply add to a running total; they interact with existing perceptions. A positive experience with a brand that already has positive associations is amplified; the same experience with a brand that has negative associations may be discounted or reinterpreted. This multiplicative interaction between new signals and existing priors is precisely the condition under which ensemble and time averages diverge.

*Absorbing states*. Negative brand conviction can be permanent. A consumer who has decided "I will never buy from that company" after a sufficiently negative experience has entered an absorbing state from which standard marketing signals cannot recover them. The existence of such absorbing states is predicted by the SBT framework and is anecdotally pervasive in practice.

*Path dependence*. The order in which brand signals are encountered matters. A consumer who first encounters a brand through a negative experience and then encounters positive signals will, in general, reach a different final perception than one who encounters the same signals in reverse order. This path dependence is a direct consequence of the multiplicative/non-linear nature of signal processing.

*Observer heterogeneity*. Individual consumer trajectories are governed by person-specific parameters (the observer spectral profile in SBT terms), making group-level statistics unreliable predictors of individual behavior---precisely the condition Molenaar (2004) identified as non-ergodicity in psychology.

The nearest work in marketing is Layton and Duffy (2018), who discuss path dependence in marketing systems (supply chains, distribution channels) but use the concept qualitatively and system-level rather than applying Peters's mathematical formalism to individual consumer perception trajectories.

## 11. Synthesis: The Geometric Brand Theory Gap

### 11.1 Classification Matrix

To systematically identify the gap, we assess each surveyed tradition against six criteria that a comprehensive geometric theory of brand perception should satisfy:

1. **Dimensionality**: Does the framework operate in high dimensions (more than three) and examine the geometric consequences of dimensionality?

2. **Metric structure**: Does the framework define a formal metric (or pseudo-metric) on the space of brand profiles, with proved properties (triangle inequality, etc.)?

3. **Observer heterogeneity**: Does the framework model individual differences in how observers process brand signals, beyond simple preference parameters?

4. **Temporal dynamics**: Does the framework model how perceptions evolve over time, including signal decay, compounding, and path dependence?

5. **Generative mechanism**: Does the framework specify how brand perceptions are generated through a causal process (signal emission, filtering, accumulation), rather than merely describing the resulting spatial configuration?

6. **Empirical validation**: Has the framework been tested against empirical data on brand perception?

**Table 1a. Classification matrix -- spatial and geometric traditions.**

| Tradition | Dimensionality | Metric structure | Observer heterogeneity | Temporal dynamics | Generative mechanism | Empirical validation |
|---|---|---|---|---|---|---|
| MDS (Torgerson, Kruskal, Bijmolt & Wedel) | Low (2-3) | Euclidean (assumed) | INDSCAL weights | Static | None | Extensive |
| Lancaster / Hotelling | Theoretically high; practically low | Euclidean (assumed) | Preference weights only | Static | None (positions given) | Moderate (hedonic pricing) |
| Conceptual Spaces (Gardenfors) | Variable, theory-agnostic | Euclidean (assumed) | Not modeled | Minimal | None | Limited (cognitive experiments) |
| Non-Euclidean Perception (Todd, Bujack) | Low (3D vision, color) | Riemannian / non-Riemannian | Individual distortions | Static | Sensory processing | Extensive (psychophysics) |
| Information Geometry (Amari) | High (parameter spaces) | Fisher-Rao | Implicit (different distributions) | Via geodesic flow | Statistical estimation | Strong (neuroscience) |
| INDSCAL / DeSarbo | Low (2-4) | Weighted Euclidean | Dimension weights / latent classes | Static | None | Extensive |

**Table 1b. Classification matrix -- dynamical, topological, and integrative traditions.**

| Tradition | Dimensionality | Metric structure | Observer heterogeneity | Temporal dynamics | Generative mechanism | Empirical validation |
|---|---|---|---|---|---|---|
| TDA (persistent homology) | High (point clouds) | Coordinate-free | Not modeled | Change-point detection only | None | Limited (finance, biology) |
| Quantum Cognition (Busemeyer) | Finite Hilbert space | Inner product | State vectors | Unitary evolution (single-shot) | Measurement collapse | Moderate (decision experiments) |
| Opinion Dynamics (HK, DeGroot) | 1-D or low-D | Euclidean | Agent-specific initial conditions | Full dynamics (convergence) | Peer influence | Simulation + limited empirical |
| Non-Ergodicity (Peters, Molenaar) | Not spatial | Not spatial | Person-specific trajectories | Full dynamics (path-dependent) | Multiplicative dynamics | Growing (experiments) |
| SBT | 8 | Proposed | Spectral profiles | Decay, absorbing | Signal-cloud-fact | 5-brand exploratory case study |

### 11.2 The Compound Gap

The classification matrix reveals that no existing tradition satisfies all six criteria. Each tradition excels on one or two criteria while leaving others unaddressed:

- MDS has extensive empirical validation but operates in low dimensions with no generative mechanism or temporal dynamics.
- Conceptual spaces provide geometric foundations for cognition but lack temporal dynamics, observer heterogeneity, and a generative mechanism.
- Non-Euclidean perceptual geometry establishes that Euclidean distance is inadequate but has been applied only to sensory perception (color, spatial vision), not to multi-attribute brand perception.
- Information geometry provides the most sophisticated metric structure but has not been applied to brand phenomena.
- INDSCAL and DeSarbo's models come closest to modeling observer heterogeneity but operate in low dimensions with no temporal dynamics or generative mechanism.
- Quantum cognition provides a sophisticated mathematical formalism but models single decisions rather than the cumulative formation of brand perception.
- Opinion dynamics models temporal dynamics and emergent clustering but operate in flat Euclidean space with no absorbing states or signal generation.
- Non-ergodicity provides the temporal dynamics and path-dependence framework but is not spatial and has not been applied to brand perception.

The gap is therefore not the absence of any one ingredient but the absence of their combination. No existing framework integrates high-dimensional geometric structure with a formal metric, observer-specific processing, non-ergodic temporal dynamics, and a generative signal mechanism.

### 11.3 SBT as a Candidate Framework

SBT (Zharnikov, 2026a) is positioned to address this compound gap. It proposes eight perceptual dimensions (semiotic, narrative, ideological, experiential, social, economic, cultural, temporal), models brands as signal-emission profiles in this eight-dimensional space, processes signals through observer spectral profiles (a five-component weighting function), accumulates filtered signals into perception clouds that exhibit path-dependent dynamics, and incorporates absorbing states (permanent negative conviction) that create non-ergodic behavior.

However, SBT as currently formulated (Zharnikov, 2026a) remains primarily a conceptual framework. Its eight-dimensional space lacks a formally defined metric. Its observer spectral profiles are described qualitatively but not situated in a well-defined geometric space with proved properties. Its non-ergodicity claims are motivated by analogy with Peters (2019) but not derived from a formal stochastic model. The research agenda proposed in the following section addresses these formalizations.

## 12. Research Agenda: Six Open Problems

The synthesis above identifies a compound gap at the intersection of high-dimensional geometry, formal metrics, observer heterogeneity, temporal dynamics, and generative mechanisms in brand theory. We now articulate six specific open problems that collectively constitute a research agenda for mathematical brand theory. Each problem is stated with a mathematical formulation and a target result.

### Problem 1: Formal Metric on Multi-Dimensional Brand Space

**Statement.** Define a mathematically rigorous metric space for multi-dimensional brand profiles and prove its fundamental properties.

**Context.** SBT's brand profiles are vectors in $\mathbb{R}^8_+$ (non-negative signal intensities across eight dimensions). Observer weight profiles live on the probability simplex $\Delta^7$ (weights summing to one). To make geometric analysis rigorous, one must specify: (a) the appropriate space (Euclidean, spherical, simplicial), (b) the appropriate distance function (Euclidean, cosine, Fisher-Rao, Jensen-Shannon), and (c) the geometric properties of the chosen space (curvature, geodesics, volume, concentration).

**Formulation.** Let $\mathcal{B} \subset \mathbb{R}^8_+$ be the space of normalized brand emission profiles and $\mathcal{O} = \Delta^7$ be the space of observer weight profiles. Define a distance function $d_\mathcal{B}: \mathcal{B} \times \mathcal{B} \to \mathbb{R}_+$ on brand space and a distance function $d_\mathcal{O}: \mathcal{O} \times \mathcal{O} \to \mathbb{R}_+$ on observer space. Verify that both satisfy the metric axioms (non-negativity, identity of indiscernibles, symmetry, triangle inequality). Compute geodesics, curvature, and volume elements for both spaces. Define the observer-dependent pseudo-metric $d_k(A, B) = \| W_k \circ (S_A - S_B) \|$ where $W_k$ is observer $k$'s weight vector, and characterize its kernel (brands indistinguishable to observer $k$).

**Target result.** A formally verified metric space with at least three non-trivial theorems about its geometric properties.

**Companion paper.** Zharnikov (2026d) develops this problem in full, defining three metric spaces (brand signal space, observer weight space, and combined brand-observer space) and proving their geometric properties including geodesics and concentration-of-measure bounds.

### Problem 2: Projection Bounds for Dimension-Reducing Summaries

**Statement.** Apply the Johnson-Lindenstrauss (JL) lemma to quantify the information loss inherent in reducing multi-dimensional brand profiles to scalar grades or low-dimensional summaries.

**Context.** SBT's L2 assessment produces a single grade (A+ through C-) from an eight-dimensional L1 spectral profile. This is a projection from $\mathbb{R}^8$ to $\mathbb{R}^1$. The JL lemma (Johnson and Lindenstrauss, 1984) states that $n$ points in $\mathbb{R}^d$ can be projected to $\mathbb{R}^k$ with pairwise distances preserved within factor $(1 \pm \epsilon)$, provided $k \geq C \epsilon^{-2} \ln n$. For a projection to $k = 1$, the distortion is maximal.

**Formulation.** Given $n$ brand profiles in $\mathbb{R}^8$ with pairwise distances $\{d_{ij}\}$, let $\pi: \mathbb{R}^8 \to \mathbb{R}^1$ be any linear projection (grading function). Prove that for any such $\pi$, there exist brand pairs $(A, B)$ with $d(A, B) > \delta$ but $|\pi(A) - \pi(B)| < \epsilon$, for explicitly computable $\delta, \epsilon$ depending on $n$. Derive the minimum projection dimensionality $k^*$ required to preserve all pairwise distances within factor $(1 \pm 0.1)$.

**Target result.** A "metamerism is inevitable" theorem proving that scalar brand grades necessarily conflate brands that differ in their full spectral profiles, with explicit bounds showing that metamerism is not a deficiency of a particular grading system but a geometric inevitability.

**Companion paper.** Zharnikov (2026e) develops this problem in full, deriving JL-based distortion bounds and proving that spectral metamerism is a geometric inevitability of any dimension-reducing brand assessment.

### Problem 3: Concentration of Measure and Cohort Boundaries

**Statement.** Use concentration inequalities to characterize the sharpness of observer cohort boundaries in the eight-dimensional observer-profile space.

**Context.** In high dimensions, the distances between random points concentrate around their mean: the ratio of maximum to minimum pairwise distance approaches one as dimensionality increases. On the probability simplex $\Delta^{n-1}$ with the uniform (Dirichlet) distribution, this concentration is already nontrivial at $n = 8$.

**Formulation.** Let $\{\mathbf{w}_1, \ldots, \mathbf{w}_m\}$ be $m$ independent uniform random points on $\Delta^7$. Compute the expected value and variance of pairwise distances $d(\mathbf{w}_i, \mathbf{w}_j)$ as a function of $m$ and $n = 8$. For any partition of $\Delta^7$ into $k$ convex cohort regions, derive a lower bound on the fraction of observer profiles within distance $\epsilon$ of a boundary.

**Target result.** A "boundary fuzziness" theorem establishing that observer cohort boundaries are inherently imprecise at $n = 8$, with quantifiable fuzziness that increases as the number of cohorts grows. This formalizes the SBT claim that observer cohorts are dynamic and fuzzy, not crisp segments.

**Companion paper.** Zharnikov (2026f) develops this problem in full, applying concentration of measure inequalities on the simplex to derive explicit boundary fuzziness bounds for perceptual cohorts.

### Problem 4: Sphere Packing and Positioning Capacity

**Statement.** Apply sphere packing theory to derive upper bounds on the number of perceptually distinguishable brand positions in eight-dimensional perception space.

**Context.** Two brands are perceptually distinguishable if their profiles differ by more than a just-noticeable difference (JND) threshold $\epsilon$. The maximum number of distinguishable positions is bounded by the maximum number of non-overlapping spheres of radius $\epsilon/2$ in the brand space. In eight dimensions, the densest sphere packing is the $E_8$ lattice, with kissing number 240 (Viazovska, 2017). This numerical coincidence is suggestive but not constitutive; the eight dimensions were derived from empirical domain analysis (Zharnikov, 2026b), not from mathematical structure.

**Formulation.** For perceptual threshold $\epsilon$ on the positive octant of the unit 8-sphere $S^7_+$, derive the packing capacity $N(\epsilon) = \text{vol}(S^7_+) / \text{vol}(B_8(\epsilon/2))$ as a function of $\epsilon$. Interpret the $E_8$ kissing number (240) as an upper bound on the number of nearest competitors for any brand position. Derive conditions under which a product category is "saturated" (number of brands approaches packing capacity for the category's effective dimensionality).

**Target result.** Explicit capacity bounds for realistic JND thresholds, with an interpretation of the $E_8$ structure as a geometric constraint on competitive dynamics.

**Companion paper.** Zharnikov (2026g) develops this problem in full, computing sphere packing capacity bounds on $S^7_+$ and interpreting the $E_8$ kissing number as an upper bound on competitive adjacency.

### Problem 5: Specification Impossibility in Organizational Design

**Statement.** Prove that comprehensive organizational specification is geometrically impossible in high-dimensional parameter spaces, formalizing the necessity of specialization.

**Context.** The companion OrgSchema Theory (OST) framework (Zharnikov, 2026i) uses an 8 x 6 activation matrix, creating a 48-dimensional specification space. The volume of the unit sphere in 48 dimensions is approximately $1.5 \times 10^{-15}$, meaning that any organization "occupies" an infinitesimal fraction of the specification hypercube.

**Formulation.** For specification space $\mathbb{R}^{48}$ with resolution $\epsilon$ per dimension, compute the number of distinguishable specifications $(1/\epsilon)^{48}$ and compare to physically realizable organizational configurations. Derive the effective dimensionality reduction achieved by the cascading structure (higher levels constrain lower levels), and prove that fork operations (shared subspace + private subspace) optimally balance specification coverage with organizational diversity.

**Target result.** A "coverage impossibility" theorem establishing that exhaustive specification is impossible in high-dimensional organizational spaces, with explicit constants showing that specialization is a geometric necessity.

**Companion paper.** Zharnikov (2026h) develops this problem in full, proving coverage impossibility in 48-dimensional specification space and deriving the dimensionality reduction achieved by OrgSchema's cascading structure.

### Problem 6: Diffusion Dynamics on Perceptual Manifolds

**Statement.** Model brand perception evolution as a stochastic diffusion process on the brand-perception manifold, connecting to non-ergodicity through mixing-time analysis.

**Context.** An observer's evolving perception of a brand can be modeled as a trajectory on $S^7_+$, driven by signal encounters (random perturbations), signal decay (deterministic drift), and crystallization (absorbing boundaries). The mixing time of this process---the time required for the process to "forget" its initial condition---determines whether the dynamics are ergodic.

**Formulation.** Define the stochastic differential equation $dX_t = \mu(X_t, t) \, dt + \sigma(X_t, t) \, dW_t$ on $S^7_+$, where $\mu$ encodes signal drift and decay, $\sigma$ encodes signal noise, and $W_t$ is Brownian motion on the manifold. Compute or bound the mixing time $\tau_{\text{mix}}$ as a function of the spectral gap of the Laplace-Beltrami operator on $S^7_+$ with absorbing boundary conditions. Show that the ergodicity coefficient $\varepsilon \sim 1/\tau_{\text{mix}}$ and that absorbing boundaries (crystallized negative conviction) increase $\tau_{\text{mix}}$ to infinity, producing non-ergodic dynamics.

**Target result.** A formally well-posed diffusion model on $S^7_+$ with proved non-ergodicity under absorbing-boundary conditions, recovering Peters's (2019) time-versus-ensemble distinction as a special case.

**Companion paper.** Zharnikov (2026j) develops this problem in full, modeling brand perception evolution as stochastic diffusion on the perceptual manifold with absorbing boundaries.

## 13. Conclusion

This survey has mapped the landscape of geometric methods applied to brand perception across ten intellectual traditions: multidimensional scaling, characteristics-space economics, conceptual spaces, non-Euclidean perceptual geometry, information geometry, individual-differences scaling, topological data analysis, quantum cognition, opinion dynamics, and non-ergodicity research. Each tradition contributes essential insights, but none provides a complete geometric theory of brand perception.

The MDS tradition has produced decades of empirical work on brand mapping but remains confined to low-dimensional, static, descriptive representations. Lancaster's characteristics theory placed products in geometric spaces but assumed homogeneous consumers and Euclidean structure. Gardenfors's conceptual spaces provide the most explicit geometric framework for cognition but lack temporal dynamics, observer heterogeneity, and a generative mechanism. The discovery that perceptual space is non-Euclidean---non-Riemannian, even, in the case of color---has not penetrated brand theory. Information geometry offers a natural metric framework but has not been applied to marketing. INDSCAL and DeSarbo's dimension-weighting models come closest to capturing observer heterogeneity but operate in low dimensions without temporal dynamics. TDA provides coordinate-free tools for analyzing high-dimensional data shapes but has not been applied to brand perception. Quantum cognition models single decisions in Hilbert spaces but not the cumulative formation of brand perception. Opinion dynamics models temporal evolution and emergent clustering but in flat spaces without absorbing states. And non-ergodicity research demonstrates that individual trajectories diverge from population averages but has not been applied to any marketing phenomenon.

The compound gap---the absence of a framework combining high-dimensional geometry, a formal metric, observer-specific processing, non-ergodic temporal dynamics, and a generative signal mechanism---is not an incremental missing piece. It represents a fundamental absence of mathematical structure in one of the most practically important domains of applied social science. Brands represent trillions of dollars in economic value (Brand Finance, 2025, though Brand Finance's scalar methodology is itself subject to the metamerism critique developed in this survey), yet the theory that describes how brand perceptions form and evolve has less mathematical structure than the theory of how we perceive color.

We have articulated six open problems that collectively constitute a research agenda for mathematical brand theory. These problems draw on well-established results in high-dimensional geometry---the Johnson-Lindenstrauss lemma, concentration of measure, sphere packing, stochastic diffusion on manifolds---that have never been applied to brand perception or, in most cases, to any social science context. The fact that Spectral Brand Theory (Zharnikov, 2026a) proposes exactly eight perceptual dimensions, and that eight is the dimensionality where the $E_8$ lattice achieves optimal sphere packing, is a coincidence that merits formal exploration.

The research program we propose would not merely formalize an existing framework. It would establish a new interdisciplinary connection between high-dimensional geometry and brand science, producing results with implications for perceptual psychology, marketing science, organizational theory, and the mathematics of social systems. Whether SBT proves to be the right framework for these formalizations, or whether the mathematical analysis reveals that a different framework is needed, the intellectual territory is genuinely unoccupied and the tools to explore it are available.

---

## Author Note

Dmitry Zharnikov is an independent researcher and strategist. He holds a Professional MBA (Entrepreneurship & Innovation) from Technische Universitat Wien and Wirtschaftsuniversitat Wien (dual degree, 2018), where his thesis examined strategic positioning of solar energy companies in Russia (Zharnikov, 2018). ORCID: https://orcid.org/0009-0000-6893-9231

---

## References

Aaker, D. A. (1991). *Managing Brand Equity: Capitalizing on the Value of a Brand Name*. Free Press.

Aisbett, J., and Gibbon, G. (2001). "A General Formulation of Conceptual Spaces as a Meso Level Representation." *Artificial Intelligence*, 133(1-2), 189-232.

Amari, S.-i. (2016). *Information Geometry and Its Applications*. Springer.

Amari, S.-i., Nagaoka, H., and Harada, D. (2000). *Methods of Information Geometry*. American Mathematical Society.

Bakker, R., and Poole, K. T. (2013). "Bayesian Metric Multidimensional Scaling." *Political Analysis*, 21(1), 125-140.

Bechberger, L. (2019). "Towards Grounded Conceptual Spaces." Doctoral dissertation, University of Osnabruck.

Bernoulli, D. (1738). "Specimen Theoriae Novae de Mensura Sortis." *Commentarii Academiae Scientiarum Imperialis Petropolitanae*, 5, 175-192. Translated by L. Sommer, *Econometrica*, 22(1), 23-36 (1954).

Bijmolt, T. H. A., and Wedel, M. (1999). "A Comparison of Multidimensional Scaling Methods for Perceptual Mapping." *Journal of Marketing Research*, 36(1), 137-153.

Bijmolt, T. H. A., Wedel, M., Pieters, R. G. M., and DeSarbo, W. S. (1998). "Judgments of Brand Similarity and Their Role in Brand Consideration Sets." *Marketing Letters*, 9(3), 231-246.

Brand Finance. (2025). *Global 500 2025: The Annual Report on the World's Most Valuable and Strongest Brands*. Brand Finance.

Bouchaud, J.-P., and Mezard, M. (2000). "Wealth Condensation in a Simple Model of Economy." *Physica A*, 282(3-4), 536-545.

Bujack, R., Teti, E., Miller, J., Caffrey, E., and Flatley, C. (2022). "The Non-Riemannian Nature of Perceptual Color Space." *Proceedings of the National Academy of Sciences*, 119(18), e2119753119.

Busemeyer, J. R., and Bruza, P. D. (2012). *Quantum Models of Cognition and Decision*. Cambridge University Press.

Carlsson, G. (2009). "Topology and Data." *Bulletin of the American Mathematical Society*, 46(2), 255-308.

Carroll, J. D., and Chang, J. J. (1970). "Analysis of Individual Differences in Multidimensional Scaling via an N-Way Generalization of Eckart-Young Decomposition." *Psychometrika*, 35(3), 283-319.

Cencov, N. N. (1982). *Statistical Decision Rules and Optimal Inference*. American Mathematical Society.

Chernikov, S. (2024). "Systematic Review of Brand Equity Evaluation Models." Working paper.

Coombs, C. H. (1964). *A Theory of Data*. Wiley.

Cooper, L. G. (1983). "A Review of Multidimensional Scaling in Marketing Research." *Applied Psychological Measurement*, 7(4), 427-450.

Costa, S. I. R., Hero, A. O., and Vignat, C. (2005). "On Solutions to Multivariate Maximum Alpha-Entropy Problems." In *Energy Minimization Methods in Computer Vision and Pattern Recognition*, Springer, 211-226.

Cox, T. F., and Cox, M. A. A. (2001). *Multidimensional Scaling* (2nd ed.). Chapman and Hall/CRC.

Deffuant, G., Neau, D., Amblard, F., and Weisbuch, G. (2000). "Mixing Beliefs Among Interacting Agents." *Advances in Complex Systems*, 3(1-4), 87-98.

DeGroot, M. H. (1974). "Reaching a Consensus." *Journal of the American Statistical Association*, 69(345), 118-121.

dePalma, A., Ginsburgh, V., Papageorgiou, Y. Y., and Thisse, J.-F. (1985). "The Principle of Minimum Differentiation Holds Under Sufficient Heterogeneity." *Econometrica*, 53(4), 767-781.

DeSarbo, W. S., and Hoffman, D. L. (1986). "Simple and Weighted Unfolding Threshold Models for the Spatial Representation of Binary Choice Data." *Applied Psychological Measurement*, 10(3), 247-264.

DeSarbo, W. S., Kim, Y., Choi, S. C., and Spaulding, M. (2002). "A Gravity-Based Multidimensional Scaling Model for Deriving Spatial Structures Underlying Consumer Preference/Choice Judgments." *Journal of Consumer Research*, 29(1), 91-100.

Edelsbrunner, H., and Harer, J. L. (2010). *Computational Topology: An Introduction*. American Mathematical Society.

Fisher, A. J., Medaglia, J. D., and Jeronimus, B. F. (2018). "Lack of Group-to-Individual Generalizability Is a Threat to Human Subjects Research." *Proceedings of the National Academy of Sciences*, 115(27), E6106-E6115.

Fournier, S. (1998). Consumers and their brands: Developing relationship theory in consumer research. *Journal of Consumer Research*, 24(4), 343-373.

Gardenfors, P. (2000). *Conceptual Spaces: The Geometry of Thought*. MIT Press.

Holt, D. B. (2004). *How brands become icons: The principles of cultural branding*. Harvard Business School Press.

Golub, B., and Jackson, M. O. (2010). "Naive Learning in Social Networks and the Wisdom of Crowds." *American Economic Journal: Microeconomics*, 2(1), 112-149.

Green, P. E., and Rao, V. R. (1972). *Applied Multidimensional Scaling: A Comparison of Approaches and Algorithms*. Holt, Rinehart and Winston.

Green, P. E., and Srinivasan, V. (1978). "Conjoint Analysis in Consumer Research: Issues and Outlook." *Journal of Consumer Research*, 5(2), 103-123.

Hegselmann, R., and Krause, U. (2002). "Opinion Dynamics and Bounded Confidence: Models, Analysis and Simulation." *Journal of Artificial Societies and Social Simulation*, 5(3), 2.

Hotelling, H. (1929). "Stability in Competition." *The Economic Journal*, 39(153), 41-57.

Johnson, W. B., and Lindenstrauss, J. (1984). "Extensions of Lipschitz Mappings into a Hilbert Space." *Contemporary Mathematics*, 26, 189-206.

Kapferer, J.-N. (2008). *The New Strategic Brand Management: Creating and Sustaining Brand Equity Long Term* (4th ed.). Kogan Page.

Keller, K. L. (1993). "Conceptualizing, Measuring, and Managing Customer-Based Brand Equity." *Journal of Marketing*, 57(1), 1-22.

Khrennikov, A. (2016). "Quantum-Like Model of Decision Making and Sense Perception Based on the Representation of the Contextual Probabilistic Model of Kolmogorovian Type in Complex Hilbert Space." *Biosystems*, 138, 49-56.

Kruskal, J. B. (1964). "Multidimensional Scaling by Optimizing Goodness of Fit to a Nonmetric Hypothesis." *Psychometrika*, 29(1), 1-27.

Lancaster, K. J. (1966). "A New Approach to Consumer Theory." *Journal of Political Economy*, 74(2), 132-157.

Layton, R. A., and Duffy, S. (2018). "Path Dependent and Path Creation Perspectives on Marketing System Development." *Journal of Macromarketing*, 38(1), 23-31.

Lorenz, J. (2007). "Continuous Opinion Dynamics Under Bounded Confidence: A Survey." *International Journal of Modern Physics C*, 18(12), 1819-1838.

McInnes, L., Healy, J., Saul, N., and Grossberger, L. (2018). "UMAP: Uniform Manifold Approximation and Projection." *Journal of Open Source Software*, 3(29), 861.

Meder, D., Rabe, F., Morville, T., and Tobler, P. N. (2021). "Ergodicity-Breaking Reveals Time Scales for Gambles in the Real World." *Chaos*, 31(2), 023122.

Mikolov, T., Sutskever, I., Chen, K., Corrado, G. S., and Dean, J. (2013). "Distributed Representations of Words and Phrases and Their Compositionality." *Advances in Neural Information Processing Systems*, 26, 3111-3119.

Molenaar, P. C. M. (2004). "A Manifesto on Psychology as Idiographic Science: Bringing the Person Back into Scientific Psychology, This Time Forever." *Measurement*, 2(4), 201-218.

Molenaar, P. C. M. (2009). "The New Person-Specific Paradigm in Psychology." *Current Directions in Psychological Science*, 18(2), 109-112.

Oh, M.-S., and Raftery, A. E. (2001). "Bayesian Multidimensional Scaling and Choice of Dimension." *Journal of the American Statistical Association*, 96(455), 1031-1044.

Peli, G., and Nooteboom, B. (1999). "Market Partitioning and the Geometry of the Resource Space." *American Journal of Sociology*, 104(4), 1132-1153.

Peters, O. (2019). "The Ergodicity Problem in Economics." *Nature Physics*, 15, 1216-1221.

Peters, O., and Skjold, A. (2024). "Time-Average Cooperation in Agent-Based Models." Working paper, London Mathematical Laboratory.

Pothos, E. M., and Busemeyer, J. R. (2022). "Quantum Cognition." *Annual Review of Psychology*, 73, 749-778.

Rosen, S. (1974). "Hedonic Prices and Implicit Markets: Product Differentiation in Pure Competition." *Journal of Political Economy*, 82(1), 34-55.

Shepard, R. N. (1962). "The Analysis of Proximities: Multidimensional Scaling with an Unknown Distance Function." *Psychometrika*, 27(2), 125-140.

Skjold, A., Brewer, M., and Peters, O. (2024). "Sensitivity to Non-Ergodicity in Additive Dynamics with Risk of Ruin." *Royal Society Open Science*, 11(1), 231240.

Steels, L. (2012). "Self-Organization and Selection in Cultural Language Evolution." In *Experiments in Cultural Language Evolution*, John Benjamins, 1-37.

Todd, J. T., Oomes, A. H. J., Koenderink, J. J., and Kappers, A. M. L. (2001). "On the Affine Structure of Perceptual Space." *Psychological Science*, 12(3), 191-196.

Torgerson, W. S. (1952). "Multidimensional Scaling: I. Theory and Method." *Psychometrika*, 17(4), 401-419.

Tucker, L. R. (1960). "Intra-Individual and Inter-Individual Multidimensionality." In H. Gulliksen and S. Messick (Eds.), *Psychological Scaling: Theory and Applications*, Wiley, 155-167.

van der Maaten, L., and Hinton, G. (2008). "Visualizing Data Using t-SNE." *Journal of Machine Learning Research*, 9, 2579-2605.

Vanhoyweghen, L. (2024). "Time Averages as a Better Null Model for Stated Preference." Working paper.

Viazovska, M. S. (2017). "The Sphere Packing Problem in Dimension 8." *Annals of Mathematics*, 185(3), 991-1015.

Vogt, P. (2006). "Language Evolution and Robotics: Issues on Symbol Grounding and Language Acquisition." In *Artificial Cognition Systems*, Idea Group, 176-209.

Warglien, M., and Gartner, W. B. (2004). "Entrepreneurial Leadership and the Creation of New Markets: Components of a Conceptual Space Theory." Working paper.

Yen, P. T.-W., and Cheong, S. A. (2021). "Using Topological Data Analysis (TDA) and Persistent Homology to Analyze the Stock Markets in Singapore and Taiwan." *Frontiers in Physics*, 9, 572216.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper.

Zharnikov, D. (2026d). Brand space geometry: A formal metric for multi-dimensional brand perception. Working Paper.

Zharnikov, D. (2026e). Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry. Working Paper.

Zharnikov, D. (2026f). Cohort boundaries in high-dimensional perception space: A concentration of measure analysis. Working Paper.

Zharnikov, D. (2026g). How many brands can a market hold? Sphere packing bounds for multi-dimensional positioning. Working Paper.

Zharnikov, D. (2026h). Specification impossibility in organizational design: A high-dimensional geometric analysis. Working Paper.

Zharnikov, D. (2026i). The Organizational Schema Theory: Test-driven business design. Working Paper.

Zharnikov, D. (2026j). Non-ergodic brand perception: Diffusion dynamics on multi-dimensional perceptual manifolds. Working Paper.

Zharnikov, D. (2018). Strategy of the leading energy generation companies in solar business in the Russian Federation: Features and challenges (MBA thesis). Technische Universitat Wien and Wirtschaftsuniversitat Wien. https://repositum.tuwien.at/handle/20.500.12708/79295

---

