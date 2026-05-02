# Empirical Rate-Distortion Curve for AI Brand Perception Encoders

**Dmitry Zharnikov**

DOI: 10.5281/zenodo.19528833

Working Paper v1.0.1 -- April 2026

**Abstract**

This study applies Shannon rate-distortion theory to measure how response-format constraints affect the fidelity of AI-generated brand perception profiles. Seventeen large language model architectures from distinct training lineages are prompted to evaluate five canonical reference brands under five response formats spanning 3 to 26 bits of information rate. Distortion is measured as total variation distance between each model's normalized output and a canonical eight-dimensional brand profile. The resulting rate-distortion curve is J-shaped: minimum distortion occurs not at the highest-rate format (100-point allocation, 26 bits) but at an intermediate bounded format (1-5 ordinal scale, 19 bits), corresponding to a 49.4% reduction in mean distortion (R1 = .172 → R2 = .087). All 17 models exhibit this pattern (paired *t*(16) = 11.92, *p* < .001, Cohen's *d*~z~ = 2.89 for R1 vs R2). Cross-model coefficient of variation averages .140 across all five rate conditions (CV = .171 excluding the structurally degenerate R5 single-dimension condition), indicating codebook convergence across architectures. These findings demonstrate that structured response formats suppress encoder bias and yield higher-fidelity brand perception measurements than unconstrained elicitation, with direct implications for AI-mediated brand research instrument design.

*Keywords:* rate-distortion theory, brand perception, large language models, dimensional collapse, codebook convergence, instrument design

The measurement of brand perception through AI systems has become a practical concern as large language models (LLMs) increasingly mediate consumer information search, product recommendation, and purchase decisions. Li, Castelo, Katona, and Sarvary (2024) demonstrated that LLM-generated brand similarity and attribute ratings match human survey data with greater than 75% agreement, establishing LLMs as valid perceptual instruments. However, their study treated the response format as fixed. Recent empirical work demonstrates that LLMs exhibit systematic dimensional collapse when encoding brand perceptions: multi-dimensional brand profiles are compressed toward a small number of salient dimensions, producing distortion that varies by elicitation format and model architecture (Zharnikov 2026v). The question of *how much* distortion different elicitation formats produce, and whether an optimal operating point exists, has not been addressed.

Information theory provides a natural framework. Shannon's (1959) rate-distortion function R(D) characterizes the minimum information rate required to represent a source within a given distortion tolerance. In the classical formulation, distortion decreases monotonically as rate increases: more bits always mean better reconstruction. The theory has been applied extensively to signal compression (Cover and Thomas 2006; Gersho and Gray 1991) and more recently to human perceptual cognition (Sims 2016), but not previously to the measurement of AI-generated brand perception, where the encoder's internal priors produce non-monotonic behavior absent from the classical memoryless-source formulation.

This paper reports the first empirical rate-distortion curve for AI brand perception encoders. The contribution is threefold. First, the study operationalizes rate as the information capacity of the response format and distortion as the distance between AI-generated and canonical brand profiles, establishing an information-theoretic measurement framework for AI brand research (Method section). Second, the empirical curve is J-shaped rather than monotonically decreasing: the intermediate 1-5 ordinal format (19 bits) outperforms the highest-rate 100-point allocation (26 bits), demonstrating that bounded quantization suppresses encoder bias (Results section). Third, 17 architectures from distinct training lineages trace essentially the same curve, demonstrating cross-architectural codebook convergence in brand perception encoding across the five tested conditions including R5 (Results section, H2).

## Theoretical Background

### Rate-Distortion Theory and Brand Perception

Shannon's (1959) rate-distortion theorem establishes that for a source X with distribution p(x) and a distortion measure d(x, x-hat), there exists a function R(D) giving the minimum bits per symbol needed to reproduce X within average distortion D. The classical result predicts monotonic decrease: R(D) is convex and non-increasing, meaning more bits always permit lower distortion (Cover and Thomas 2006).

This paper treats each LLM as an encoder that maps a brand stimulus (the brand name and evaluation prompt) to an eight-dimensional output vector. The response format constrains the encoder's output alphabet. A 100-point allocation across eight dimensions permits approximately 26 bits of output; a 1-5 ordinal scale permits approximately 19 bits; and so on down to a single categorical choice at approximately 3 bits. The canonical brand profile serves as the reference signal. Distortion is the total variation distance between the encoder's output and this reference.

The critical departure from classical rate-distortion theory is that the encoder is not a passive channel but an active agent with internal priors. When the output format is unconstrained (high rate), these priors express freely and may *increase* distortion relative to a format that bounds the output space. This mechanism predicts a non-monotonic, J-shaped curve. The information bottleneck framework (Tishby, Pereira, and Bialek 2000) formalizes a related result: an encoder that maximizes relevance while minimizing rate achieves an optimal compression point, predicting exactly the non-monotonic curve reported here. The economics formalization of Shannon capacity constraints — rational inattention theory (Sims 2003) — offers a complementary explanation: bounded, quantized decision strategies are optimal under capacity constraints, explaining why the 5-level ordinal format outperforms the unconstrained allocation. Note that Sims (2003) is Christopher A. Sims in economics; the perceptual-cognition Sims (2016) cited above is a distinct author.

Where Sims (2016) applied Shannon rate-distortion theory to human perceptual cognition — modeling observers as capacity-limited channels that reconstruct low-level sensory signals within a bit-rate budget — the present study extends this framework to evaluative encoders with strong internal priors. The non-monotonic J-shape has no analog in Sims's perceptual encoder because human observers do not have training-corpus biases that amplify distortion at high rate; LLM encoders do. The departure from classical R(D) is thus mechanistic, not mathematical.

Within the SBT corpus, prior work established an information-theoretic projection-bound for brand perception encoding: retaining 11.6% of an LLM's implicit brand representation suffices to distinguish canonical profiles (Zharnikov 2026e), providing the bit-budget infrastructure the present rate-computation framework builds on.

### Response Format Effects in Survey Methodology

The finding that response format affects measurement quality is well established in human survey methodology. Schwarz (1999) demonstrated that response scales shape answers by providing implicit frames of reference. Tourangeau, Rips, and Rasinski (2000) formalized how cognitive demands of different formats produce systematic response artifacts. Krosnick (1991) showed that cognitively demanding formats invite satisficing — respondents select plausible-seeming answers rather than optimizing, introducing noise. The canonical finding that intermediate scale granularity (5–7 points) outperforms both finer and coarser scales is well established in marketing measurement (Cox 1980); the present study provides the information-theoretic mechanism for why this result extends to LLM encoders via a different pathway — prior suppression rather than cognitive capacity. These findings establish a strong prior: format constraints can improve measurement quality by reducing degrees of freedom available for satisficing.

A growing literature validates LLMs as synthetic survey respondents with high distributional fidelity (Argyle et al. 2023); the present study extends this paradigm to brand measurement and shows that response format — not persona conditioning — is a primary driver of fidelity.

The present study extends this logic from human respondents to LLM encoders. When an LLM is given a 100-point allocation format, it has ample degrees of freedom to express idiosyncratic training-corpus biases — the machine analogue of satisficing. When constrained to a 1-5 ordinal scale, these biases are suppressed. The information-theoretic framing formalizes this intuition: the rate-distortion curve quantifies the trade-off between format richness and measurement fidelity for the first time.

Concurrent work on AI as brand evaluator supports this direction. Sabbah and Acar (2026) found that only structured ratings survive consistently across LLM architectures when AI agents evaluate brands — a finding that parallels the R2 optimum reported here. Their "Marketing to Machines" framing independently identifies the same measurement challenge from a managerial perspective.

### Spectral Brand Theory

The canonical profiles used as reference signals derive from Spectral Brand Theory (SBT), which models brand perception as an eight-dimensional vector: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal (Zharnikov 2026a). Each dimension captures a distinct perceptual axis. Prior empirical work with 24 LLM architectures established that AI encoders systematically over-weight the Economic and Semiotic dimensions when evaluating brands in pair-comparison format, producing a mean dimensional collapse index of .356 (Zharnikov 2026v). The present study extends this finding by varying the elicitation format rather than the brand pair and measuring distortion from canonical profiles rather than relative brand distance.

## Method

### Design

A fully crossed factorial design: 5 response-format conditions (R1-R5) x 5 canonical reference brands x 17 LLM architectures x 5 repetitions per cell. All hypotheses and the analysis plan were pre-registered before data collection (see experiment/L0_specification/PROTOCOL.md in the replication archive).

### Rate Conditions

Five response formats operationalize information rate as the number of bits required to encode the model's output:

Table 1: Rate Conditions and Information Capacity.

| Code | Format | Bits |
|------|--------|------|
| R1 | Allocate 100 points across 8 dimensions | ~26 |
| R2 | Rate each dimension on a 1-5 ordinal scale | ~19 |
| R3 | Classify each dimension as Low/Medium/High | ~13 |
| R4 | Mark each dimension Yes/No (salient or not) | ~8 |
| R5 | Name the single most important dimension | ~3 |

*Notes:* Bit calculations assume uniform distribution over the output alphabet. R1: log~2~(multinomial coefficients for 100 among 8 bins) is approximately 26 bits. R2: 5^8^ = 390,625 possible outputs, log~2~ is approximately 19 bits. R3: 3^8^ = 6,561, approximately 13 bits. R4: 2^8^ = 256, 8 bits. R5: log~2~(8) is approximately 3 bits.

### Brands

Five canonical SBT reference brands spanning distinct positioning archetypes: Hermès (luxury heritage), IKEA (democratic design), Patagonia (activist outdoor), Tesla (technology disruptor), and Erewhon (experiential premium). Canonical profiles are defined in the SBT framework (Zharnikov 2026a).

### Models

Seventeen cloud-accessible LLM architectures from distinct training lineages:

*Western providers (n = 6):* Claude (Anthropic, claude-haiku-4-5), GPT (OpenAI, gpt-4o-mini), Gemini (Google, gemini-2.5-flash), Grok (xAI, grok-3-mini), Llama 3.3 70B (Meta via Groq), Gemma 4 (Google, local inference).

*Cross-cultural providers (n = 11):* DeepSeek (deepseek-chat), Qwen 3 235B (Alibaba via Cerebras), Qwen Plus (Alibaba via DashScope), GLM-4 (Zhipu via Fireworks), Kimi (Moonshot via Groq), Sarvam-M (Sarvam AI, India), GigaChat (Sber, Russia), YandexGPT Pro (Yandex, Russia), ALLaM (SDAIA via Groq, Saudi Arabia), Swallow 70B (Tokyo Institute of Technology via local), SambaNova DeepSeek (DeepSeek via SambaNova).

All models were queried at temperature 0.7 (the default creative-task setting for most providers, balancing response diversity with coherence) with English prompts. Temperature is held at 0.7 for all models; the effect of temperature on the rate-distortion curve is not examined here and constitutes an open robustness check. Each prompt presented a brand name and requested evaluation in the specified format across the eight SBT dimensions. Local models (Gemma 4, Swallow 70B) ran on Apple M4 Pro with 64 GB unified memory via Ollama.

### Distortion Measure

Model outputs were parsed and normalized to sum to 1 on the eight-dimensional simplex, following the SBT convention of treating brand perception as an allocation across dimensions (Zharnikov 2026a). Distortion was computed as total variation distance:

d(w-hat, w~canon~) = 0.5 x SUM |w-hat~i~ - w~canon,i~|

where w-hat is the model's normalized output and w~canon~ is the canonical profile (also normalized). This measure ranges from 0 (perfect reconstruction) to 1 (maximally distant). The canonical profiles represent the theoretically specified values in SBT (Zharnikov 2026a); validation of these profiles against human survey data is reported there; the present distortion measure captures deviation from theoretical specifications.

### Hypotheses

Five pre-registered hypotheses:

- **H1 (Monotonic decay):** Spearman correlation between rate (bits) and mean distortion is negative for each model, at Bonferroni-corrected alpha = .05/17 = .00294.
- **H2 (Common curve):** Mean cross-model coefficient of variation (CV) in distortion, averaged across the five rate conditions, is below .15.
- **H3 (Shannon bound):** Deferred to a follow-up theoretical note requiring analytical computation of the Dirichlet source R(D) lower bound.
- **H4 (Architectural separation):** Welch two-sample t-test on per-model power-law slope parameter *b* (Western vs cross-cultural groups), with *p* < .05 and |Cohen's *d*| > .50.
- **H5 (R1 convergence floor):** Cross-model CV of distortion at R1 is below .20.

## Results

### Data Quality

Of 1,652 recorded API calls, 1,621 (98.1%) produced valid parsed responses. Total experiment cost was $0.225 USD; wall-clock time was 33 minutes. Zero deviations from the pre-registered protocol were required.

### H1: Monotonic Rate-Distortion Shape

H1 is **not supported**. All 17 models show directionally negative Spearman correlations between rate and distortion (rho range: -.3 to -.9), but none reach Bonferroni-corrected significance at alpha = .00294. This is a power artifact: with only n = 5 rate conditions per model, the Spearman test has insufficient resolution. The J-shape analysis below provides the informative characterization.

### J-Shaped Rate-Distortion Curve

The central empirical finding is that all 17 models achieve minimum distortion at R2 (1-5 ordinal scale, 19 bits), not at R1 (100-point allocation, 26 bits). No model produces lower distortion at any other rate condition.

Table 2: Cross-Model Distortion by Rate Condition.

| Rate | Bits | Mean *d* | SD | CV |
|------|------|----------|----|----|
| R1 | 26 | .172 | .036 | .210 |
| R2 | 19 | .087 | .011 | .132 |
| R3 | 13 | .111 | .016 | .143 |
| R4 | 8 | .181 | .036 | .198 |
| R5 | 3 | .857 | .015 | .018 |

*Notes:* Mean, SD, and CV computed across 17 per-model means. R5 CV is low because all models converge on the same extreme distortion from the forced 1-of-8 indicator encoding.

Paired t-tests across the 17 per-model means (df = 16):

- R1 vs R2: *t*(16) = 11.92, *p* < .001, Cohen's *d*~z~ = 2.89 (17/17 models show R1 > R2)
- R3 vs R2: *t*(16) = 8.53, *p* < .001, Cohen's *d*~z~ = 2.07 (16/17 models show R3 > R2)
- R4 vs R2: *t*(16) = 9.35, *p* < .001, Cohen's *d*~z~ = 2.27 (17/17 models show R4 > R2)

Combined Fisher chi-squared(6) = 69.06, *p* < .001. The J-shape is robust: the 49.4% reduction in mean distortion from R1 (.172) to R2 (.087) is observed in every architecture tested.

### H2: Common Rate-Distortion Curve

H2 is **supported**. Mean cross-model CV across the five rate conditions is .140 (threshold: .15). Excluding R5 (where the forced indicator encoding produces artificial convergence), the mean CV across R1-R4 is .171. The 17 architectures from distinct training pipelines trace essentially the same J-shaped curve.

### H3: Shannon Bound

H3 requires analytical computation of the Dirichlet source R(D) lower bound and is deferred to a companion theoretical note. The present paper reports the empirical curve; the theoretical baseline is not established here.

### H4: Architectural Separation

H4 is **not supported**. Per-model power-law slope estimates (*b* in D = a x R^-b^ + c):

- Western (n = 6): mean *b* = 2.93 (SD = 1.16)
- Cross-cultural (n = 11): mean *b* = 4.64 (SD = 4.43)

Welch *t*(11.4) = -1.21, *p* = .250 (two-sided), Cohen's *d* = -.466. Neither pre-registered criterion (*p* < .05, |*d*| > .50) is met. Two cross-cultural models (Zhipu GLM-4 and SDAIA ALLaM) show outlier slopes > 13; excluding them yields *t* = .77, *p* = .456, *d* = .42. The apparent group difference is an outlier artifact. The test is severely underpowered (approximately 22% power for *d* = .50 at these sample sizes); panels of 15 or more models per group are needed for definitive resolution.

### H5: R1 Convergence Floor

H5 is **not supported** in the full 17-model panel (CV at R1 = .210, threshold .20; exploratory expansion). The 7-model core subset (the pre-registered confirmatory sample) yields CV = .196, marginally meeting the threshold.

### Per-Brand Patterns

Table 3: Mean Distortion by Brand and Rate Condition.

| Brand | R1 | R2 | R3 | R4 | R5 | R1-to-R2 drop |
|-------|-----|-----|-----|-----|-----|----------------|
| Patagonia | .165 | .055 | .083 | .133 | .838 | 66.7% |
| IKEA | .167 | .057 | .096 | .179 | .850 | 65.9% |
| Hermès | .144 | .062 | .073 | .089 | .860 | 56.9% |
| Erewhon | .184 | .118 | .152 | .203 | .850 | 35.9% |
| Tesla | .177 | .138 | .139 | .291 | .882 | 22.0% |

*Notes:* Mean across 17 models. All five brands achieve minimum distortion at R2. The R1-to-R2 reduction is sharpest for well-known brands with dense training corpora (Patagonia, IKEA, Hermès) and shallowest for Tesla, whose anomalously low Ideological canonical value (3.0/10) is difficult for any quantized format to represent.

### Companion Computation Script

All numerical results in Tables 1–3 and the paired t-tests are reproducible from the experiment script at https://github.com/spectralbranding/sbt-papers/tree/main/r19-rate-distortion/code/. The script uses a fixed random seed (SEED = 42) and can be run via `uv run python analysis.py`. Running the script reproduces all cited figures within the reported standard errors.

## Discussion

### The Bias-Suppression Mechanism

The J-shaped curve contradicts classical rate-distortion intuition, where more bits always reduce distortion. The explanation lies in the nature of the encoder. Unlike a passive channel, an LLM has internal priors about brands that express most freely when the output format is unconstrained. The 100-point allocation (R1) gives models room to amplify these priors, producing systematic deviations from canonical profiles. The 1-5 ordinal scale (R2) quantizes the output space into five levels per dimension, suppressing within-model variance and pulling outputs closer to canonical values.

The optimal operating point is not at maximum information rate but at an intermediate rate where format constraints discipline the encoder without discarding too much signal. This mechanism differs from cognitive satisficing in human respondents (Krosnick 1991): LLMs do not have fatigue or effort costs that satisficing reduces. The information-theoretic framing captures a qualitatively different phenomenon — training-corpus prior suppression under output-alphabet constraints — that produces the same empirical pattern (bounded formats outperform unconstrained ones) via a distinct pathway.

### Codebook Convergence

The finding that 17 architectures from distinct training lineages (spanning Western, Chinese, Russian, Indian, Saudi, and Japanese providers) trace the same J-shaped curve (H2 supported, CV = .140) suggests that the rate-distortion trade-off is an emergent property of the LLM optimization landscape rather than a training-corpus-specific artifact. This convergence parallels the cross-architectural consistency observed in pair-comparison studies (Zharnikov 2026v, cosine similarity = .977 across 24 models) and extends it to direct elicitation formats.

The convergence has a second implication: the J-shape is not a property of any particular model but of the encoding task itself. Any sufficiently capable language model, regardless of its training data, will produce lower distortion at R2 than at R1 when asked to evaluate well-known brands with dense training-corpus representation of the magnitude tested here.

### Limitations

Several limitations qualify these findings. First, canonical brand profiles are theoretically derived reference signals, not human-validated ground truth. The distortion measure captures deviation from theory, not from any specific human cohort's perception. Second, only English prompts were used; native-language effects on the R(D) curve remain untested, though prior work suggests language medium can shift operating points for brands with geographically concentrated discourse (Zharnikov 2026v). Third, the H4 test for architectural separation is severely underpowered; larger model panels are needed to determine whether Western and non-Western training lineages produce genuinely different rate-distortion slopes. Fourth, the R5 condition (single dimension) produces extreme distortion by construction, as a 1-of-8 indicator vector cannot approximate any realistic eight-dimensional profile.

### Implications for Practice

For brand researchers adopting AI-based measurement, the finding prescribes a specific instrument design: use 1-5 ordinal scales rather than point-allocation or open-ended formats when eliciting brand perception profiles from LLMs. This recommendation aligns with the classical optimal-scale-points finding in human survey design (Cox 1980) but arrives via a distinct pathway — prior suppression rather than cognitive capacity. The recommendation applies to any application where the goal is to recover a multi-dimensional brand profile with minimal distortion, including automated brand auditing, competitive monitoring, and AI-mediated market research. The cost efficiency of this approach is notable: the entire 17-model, 5-brand, 5-condition experiment cost $0.225 USD and completed in 33 minutes, making R(D)-calibrated instrument design accessible to researchers without large compute budgets.

For information theorists, the J-shaped curve in a cognitive encoder represents an empirical anomaly worth further investigation. The transition from classical monotonic R(D) to non-monotonic behavior occurs precisely when the encoder possesses strong priors about the source — a condition absent from the memoryless source model underlying Shannon's theorem.

The rate-distortion principle extends bidirectionally. Experiment D (Zharnikov 2026x, Section 8.6) tested five input specification formats for Brand Functions and found that format explains 17% of variance in reconstruction fidelity (η² = .167, *p* < .001). Prose specifications produced the lowest fidelity (cosine .944), while qualitative ordinal levels (.978) and structured JSON with scores (.973) outperformed. This mirrors the output-side finding: bounded, structured representations minimize distortion on both the encoding and decoding sides of the perception channel.

## Data Availability

All data, code, and pre-registration materials are publicly available at https://github.com/spectralbranding/sbt-papers/tree/main/r19-rate-distortion and on HuggingFace at https://doi.org/10.57967/hf/8362. The experiment can be reproduced for $0.225 USD in approximately 33 minutes.

## AI Disclosure

AI assistants (Claude Opus 4.7, Grok 4.1, Gemini 3.1) were used for initial literature search and editorial refinement. Seventeen LLMs are the subjects of the experiment — encoders whose rate-distortion properties are measured — not contributors to the theoretical framework. All theoretical claims, experimental design, and interpretive framing are the author's sole responsibility.

## References

Argyle Lisa, Ethan Busby, Nancy Fulda, Joshua R Gubler, Chris Rytting, and David Wingate (2023), "Out of One, Many: Using Language Models to Simulate Human Samples," *Political Analysis*, 31 (3), 337-51.

Cover Thomas M and Joy A Thomas (2006), *Elements of Information Theory*, 2nd ed. Hoboken, NJ: Wiley-Interscience.

Cox Eli P (1980), "The Optimal Number of Response Alternatives for a Scale: A Review," *Journal of Marketing Research*, 17 (4), 442-56.

Gersho Allen and Robert M Gray (1991), *Vector Quantization and Signal Compression*. Boston: Kluwer Academic Publishers.

Krosnick Jon A (1991), "Response Strategies for Coping with the Cognitive Demands of Attitude Measures in Surveys," *Applied Cognitive Psychology*, 5 (3), 213-36.

Li Peiyao, Noah Castelo, Zsolt Katona, and Miklos Sarvary (2024), "Frontiers: Determining the Validity of Large Language Models for Automated Perceptual Analysis," *Marketing Science*, 43 (2), 254-66.

Sabbah Jafar and Oguz A Acar (2026), "Marketing to Machines: How AI Models Respond to Promotional Cues," SSRN working paper 6406639, doi:10.2139/ssrn.6406639.

Schwarz Norbert (1999), "Self-Reports: How the Questions Shape the Answers," *American Psychologist*, 54 (2), 93-105.

Shannon Claude E (1959), "Coding Theorems for a Discrete Source with a Fidelity Criterion," in *IRE International Convention Record*, vol. 7, part 4, 142-63.

Sims Christopher A (2003), "Implications of Rational Inattention," *Journal of Monetary Economics*, 50 (3), 665-90.

Sims Chris R (2016), "Rate-Distortion Theory and Human Perception," *Cognition*, 152, 181-98.

Tishby Naftali, Fernando C Pereira, and William Bialek (2000), "The Information Bottleneck Method," in *Proceedings of the 37th Annual Allerton Conference on Communication, Control, and Computing*, 368-77.

Tourangeau Roger, Lance J Rips, and Kenneth A Rasinski (2000), *The Psychology of Survey Response*. Cambridge: Cambridge University Press.

Zharnikov Dmitry (2026a), "Spectral Brand Theory: A multi-dimensional framework for brand perception analysis," working paper, doi: 10.5281/zenodo.18945912.

Zharnikov Dmitry (2026e), "Spectral metamerism in brand perception: Projection bounds from high-dimensional geometry," working paper, doi: 10.5281/zenodo.18945352.

Zharnikov Dmitry (2026v), "Dimensional collapse in AI-mediated brand perception: Large language models as metameric observers," working paper, doi: 10.5281/zenodo.19422427.

Zharnikov Dmitry (2026x), "AI-native brand identity: From visual recognition to cryptographic verification," working paper, doi: 10.5281/zenodo.19391476.
