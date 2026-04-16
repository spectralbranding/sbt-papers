# Experiment B: Cross-Language Semantic Drift in Brand Perception

**Protocol version**: 1.0
**Date**: 2026-04-16
**Status**: PRE-REGISTERED (committed before data collection)
**Paper target**: R15 Section 5.14 extension or PRISM paper extension
**Open Problem**: Extends Problem #1 (measurement invariance across languages)

---

## Research Question

Do the 8 SBT dimensions carry the same meaning across languages, or do dimensional concepts themselves drift when dimension labels are presented in native languages?

**Key distinction from R15 Run 5**: Run 5 tested native-language *prompting* (does the language of the prompt affect DCI?). This experiment tests native-language *dimension labels* (does "Ideological" mean the same thing when expressed as its equivalent in Japanese vs Arabic?).

---

## Design

- **Languages**: 8 (English, Chinese, Russian, Japanese, Korean, Arabic, Hindi, Spanish)
- **Brands**: 5 canonical (Hermes, IKEA, Patagonia, Erewhon, Tesla)
- **Models**: 5 (Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Grok 4.1 Fast)
- **Repetitions**: 3 per cell
- **Dimension ordering**: Latin-square balanced (8 cyclic orderings)
- **Temperature**: .7
- **Total calls**: 8 languages x 5 brands x 5 models x 3 reps = **600 calls**
- **Estimated cost**: ~$2

### Prompt Design

Bilingual dimension labels (native + English in parentheses) ensure the model maps correctly to the target dimension. The test is whether the *weight allocation* changes when dimensions are presented in the target language. The instruction text and response format remain in English to isolate the effect of dimension label language from general prompt language.

### Latin-Square Balanced Orderings

8 cyclic orderings constructed from the canonical dimension order:
```
Order 0: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal
Order 1: Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal, Semiotic
Order 2: Ideological, Experiential, Social, Economic, Cultural, Temporal, Semiotic, Narrative
Order 3: Experiential, Social, Economic, Cultural, Temporal, Semiotic, Narrative, Ideological
Order 4: Social, Economic, Cultural, Temporal, Semiotic, Narrative, Ideological, Experiential
Order 5: Economic, Cultural, Temporal, Semiotic, Narrative, Ideological, Experiential, Social
Order 6: Cultural, Temporal, Semiotic, Narrative, Ideological, Experiential, Social, Economic
Order 7: Temporal, Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural
```

Each call is assigned an ordering index = `(language_idx * 5 * 3 + brand_idx * 3 + rep_idx) % 8`.

---

## Hypotheses

### H1: Configural Invariance (Cross-Language Profile Similarity)
Cross-language profiles for the same brand correlate > .90 (cosine similarity). If the 8 dimensions carry equivalent meaning across languages, the weight allocation pattern should be stable.

- **Test**: For each brand, compute mean spectral profile per language (8 dimensions). Compute pairwise cosine similarity across all 28 language pairs. Report median and minimum cosine.
- **Success criterion**: Median cosine > .90 for all 5 brands.
- **Failure criterion**: Median cosine < .80 for any brand.

### H2: Language-Dependent Dimensional Weight Shifts
Specific dimensions show language-dependent weight shifts reflecting cultural-semantic associations:
- **H2a**: Ideological weight in Arabic > English (Arabic "ideology" concept has stronger religious/political valence)
- **H2b**: Cultural weight in Japanese > English (Japanese "culture" concept has stronger tradition/heritage valence)
- **H2c**: Economic weight in Hindi > English (Hindi-speaking markets show stronger price-sensitivity framing)

- **Test**: Independent-samples t-test per hypothesis (15 observations per language per brand, pooled across brands = 75 per language). Bonferroni-corrected alpha = .05 / 3 = .0167.
- **Effect size**: Cohen's d with 95% bootstrap CI (10,000 iterations).

### H3: Collectivist Language Clustering
Languages with collectivist cultural backgrounds (Chinese, Japanese, Korean) weight Social higher than individualist languages (English, Spanish).

- **Test**: Independent-samples t-test comparing Social dimension weight: collectivist group (zh, ja, ko; pooled n = 225) vs individualist group (en, es; pooled n = 150).
- **Alpha**: .05 (single test, no correction needed).
- **Effect size**: Cohen's d with 95% bootstrap CI.

---

## Power Analysis

### Effect size priors (from R15 synthetic cohort experiments)
- Small cohort effect: eta-sq = .091
- Medium cohort effect: eta-sq = .25
- Large cohort effect: eta-sq = .394

### H1 (descriptive, no inferential test needed)
Cosine similarity computed on mean profiles. With 15 observations per cell (5 brands x 3 reps), central limit theorem ensures stable means.

### H2 (t-tests, 3 comparisons)
- Per-language sample: 75 observations (5 brands x 5 models x 3 reps)
- For Cohen's d = .50 (medium effect), power = .80, alpha = .0167 (Bonferroni):
  - Required n per group: ~73 (from G*Power two-sample t-test)
  - Available n per group: 75 (English) vs 75 (target language)
  - **Power adequate for medium effects.**
- For Cohen's d = .30 (small effect): power ~.40. Underpowered for small effects; noted as limitation.

### H3 (t-test, 1 comparison)
- Collectivist group: 225 observations (3 languages x 75 each)
- Individualist group: 150 observations (2 languages x 75 each)
- For Cohen's d = .30, alpha = .05: power ~.82.
- **Power adequate for small-to-medium effects.**

---

## Multiple Comparison Correction

- H2: 3 tests, Bonferroni correction (alpha = .0167)
- Per-dimension exploratory ANOVAs (8 tests): Bonferroni correction (alpha = .00625)
- FDR (Benjamini-Hochberg) reported alongside Bonferroni when >10 comparisons

---

## Dimension Label Translations

All translations use bilingual format: `"NativeLabel (English)"`.

### Chinese (zh)
- 符号学 (Semiotic), 叙事 (Narrative), 意识形态 (Ideological), 体验 (Experiential), 社会 (Social), 经济 (Economic), 文化 (Cultural), 时间 (Temporal)

### Russian (ru)
- Семиотический (Semiotic), Нарративный (Narrative), Идеологический (Ideological), Эмпирический (Experiential), Социальный (Social), Экономический (Economic), Культурный (Cultural), Темпоральный (Temporal)

### Japanese (ja)
- 記号論的 (Semiotic), 物語的 (Narrative), イデオロギー的 (Ideological), 体験的 (Experiential), 社会的 (Social), 経済的 (Economic), 文化的 (Cultural), 時間的 (Temporal)

### Korean (ko)
- 기호학적 (Semiotic), 서사적 (Narrative), 이념적 (Ideological), 체험적 (Experiential), 사회적 (Social), 경제적 (Economic), 문화적 (Cultural), 시간적 (Temporal)

### Arabic (ar)
- سيميائي (Semiotic), سردي (Narrative), أيديولوجي (Ideological), تجريبي (Experiential), اجتماعي (Social), اقتصادي (Economic), ثقافي (Cultural), زمني (Temporal)

### Hindi (hi)
- चिह्नशास्त्रीय (Semiotic), कथात्मक (Narrative), वैचारिक (Ideological), अनुभवात्मक (Experiential), सामाजिक (Social), आर्थिक (Economic), सांस्कृतिक (Cultural), कालिक (Temporal)

### Spanish (es)
- Semiótico (Semiotic), Narrativo (Narrative), Ideológico (Ideological), Experiencial (Experiential), Social (Social), Económico (Economic), Cultural (Cultural), Temporal (Temporal)

### English (en) — control
- Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal

---

## Analysis Plan

### Primary Analyses (pre-registered)

1. **Per-language mean spectral profiles**: 8 languages x 5 brands x 8 dimensions. Visualization: 5 heatmaps (one per brand), 8 rows (languages), 8 columns (dimensions).

2. **Cross-language cosine similarity matrix**: For each brand, compute 28 pairwise cosine similarities across 8 languages. Report median, min, max per brand. Test H1.

3. **Per-dimension ANOVA**: Language (8 levels) as between-subjects factor, dimension weight as DV. 8 separate ANOVAs (one per dimension). Report F-statistic, p-value, eta-squared. Bonferroni-corrected alpha = .00625.

4. **H2 targeted t-tests**: Three planned comparisons (ar vs en on Ideological; ja vs en on Cultural; hi vs en on Economic). Report t, df, p (uncorrected and Bonferroni-corrected), Cohen's d, 95% CI.

5. **H3 collectivist vs individualist t-test**: Compare Social weight between collectivist (zh+ja+ko) and individualist (en+es) groups. Report t, df, p, Cohen's d, 95% CI.

### Exploratory Analyses (labeled EXPLORATORY)

6. **Measurement invariance sequence**: Configural -> metric -> scalar, adapted for LLM weight-allocation data. Using Tucker's congruence coefficient and multi-group CFA if sample size permits.

7. **Cultural dimension clustering**: Hierarchical clustering on language-averaged profiles (Ward's method, cosine distance). Dendrogram visualization. Test whether collectivist languages (zh, ja, ko) cluster together.

8. **Model x Language interaction**: Two-way ANOVA (Model x Language) per dimension. Tests whether semantic drift magnitude is model-dependent.

9. **Per-brand language sensitivity**: Which brands show the most cross-language variation? Coefficient of variation across languages per brand.

---

## Exclusion Criteria

- API errors with unparseable responses: recorded with error field in JSONL, excluded from analysis
- Weights not summing to 100 (+-5 tolerance): renormalized if parseable, flagged
- Models with >50% error rate for any language: excluded from that language's analysis
- Dimension labels not correctly mapped to JSON keys: parsing attempts case-insensitive match on English label

---

## Random Seeds

- Call order randomization seed: 42
- Bootstrap CI seed: 12345
- Latin-square assignment: deterministic from `(lang_idx * 5 * 3 + brand_idx * 3 + rep_idx) % 8`

---

## Canonical Brand Profiles

- Hermes: [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]
- IKEA: [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]
- Patagonia: [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]
- Erewhon: [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5]
- Tesla: [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]

Dimension order: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal

---

## Models

| Name | Model ID | Provider | API Key |
|------|----------|----------|---------|
| Claude Haiku 4.5 | claude-haiku-4-5 | Anthropic | ANTHROPIC_API_KEY |
| GPT-4o-mini | gpt-4o-mini | OpenAI | OPENAI_API_KEY |
| Gemini 2.5 Flash | gemini-2.5-flash | Google | GOOGLE_API_KEY |
| DeepSeek V3 | deepseek-chat | DeepSeek | DEEPSEEK_API_KEY |
| Grok 4.1 Fast | grok-4-1-fast-non-reasoning | xAI | GROK_API_KEY |

---

## Success Criteria

- **H1 supported**: Median cosine > .90 for all 5 brands
- **H2 supported**: At least 1 of 3 directional predictions confirmed (p < .0167, Cohen's d > .30)
- **H3 supported**: Collectivist group Social weight significantly higher (p < .05, Cohen's d > .20)

## Failure Criteria

- **H1 fails**: Median cosine < .80 for any brand -> dimensions do NOT carry equivalent meaning
- **H2 fails**: No directional prediction confirmed -> weight shifts are random, not culturally systematic
- **H3 fails**: No collectivist clustering -> individualism/collectivism does not map to Social dimension weighting

---

*This protocol was committed before any API calls were made. Any analysis not specified above is labeled EXPLORATORY in the results.*
