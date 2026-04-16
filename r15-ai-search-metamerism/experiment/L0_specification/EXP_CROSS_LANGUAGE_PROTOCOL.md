# Experiment B: Cross-Language Semantic Drift in Brand Perception

**Protocol version**: 1.1
**Date**: 2026-04-16
**Status**: PRE-REGISTERED (committed before data collection)
**Paper target**: R15 Section 5.14 extension or PRISM paper extension
**Open Problem**: Extends Problem #1 (measurement invariance across languages)

---

## Research Question

Do the 8 SBT dimensions carry the same meaning across languages, or do dimensional concepts themselves drift when dimension labels are presented in native languages without English anchors?

**Key distinction from R15 Run 5**: Run 5 tested native-language *prompting* (does the language of the prompt affect DCI?). This experiment tests native-language *dimension labels* (does the weight allocation change when "Ideological" is presented only as its native equivalent, without the English anchor?).

---

## Design

### Two-Condition Paired Design

Each language is tested under two conditions:

- **Condition A (bilingual anchor)**: Dimension labels include both native and English: `"符号学 (Semiotic)": <number>`. The English parenthetical anchors the model's interpretation. This is the **control**.
- **Condition B (native-only)**: Dimension labels are native-only: `"符号学": <number>`. No English anchor. This is the **test condition**.

The hypothesis is that the native-only condition (B) produces different weights than the bilingual anchor (A), and that the magnitude and direction of this drift is language- and dimension-specific.

### Parameters

- **Languages**: 8 (English, Chinese, Russian, Japanese, Korean, Arabic, Hindi, Spanish)
- **Conditions**: 2 (bilingual anchor, native-only)
- **Brands**: 5 canonical (Hermes, IKEA, Patagonia, Erewhon, Tesla)
- **Models**: 3 (Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash)
- **Repetitions**: 2 per cell
- **Dimension ordering**: Latin-square balanced (8 cyclic orderings)
- **Temperature**: .7
- **Total calls**: 8 languages x 5 brands x 3 models x 2 conditions x 2 reps = **480 calls**
- **Note**: English has only 1 condition (bilingual = native for English), so English contributes 5 x 3 x 1 x 2 = 30 calls. The 7 non-English languages contribute 7 x 5 x 3 x 2 x 2 = 420 calls. **Actual total: 450 calls.**
- **Estimated cost**: ~$1.50

### Prompt Design

The instruction text and response format remain in English for both conditions. Only the JSON key labels change between conditions. This isolates the effect of dimension label language from general prompt language.

**Condition A prompt (Chinese example)**:
```
Evaluate the brand {brand} by allocating importance weights across
eight dimensions. Weights must sum to 100.

Respond in JSON:
{
  "符号学 (Semiotic)": <number>,
  "叙事 (Narrative)": <number>,
  "意识形态 (Ideological)": <number>,
  "体验 (Experiential)": <number>,
  "社会 (Social)": <number>,
  "经济 (Economic)": <number>,
  "文化 (Cultural)": <number>,
  "时间 (Temporal)": <number>
}
```

**Condition B prompt (Chinese example)**:
```
Evaluate the brand {brand} by allocating importance weights across
eight dimensions. Weights must sum to 100.

Respond in JSON:
{
  "符号学": <number>,
  "叙事": <number>,
  "意识形态": <number>,
  "体验": <number>,
  "社会": <number>,
  "经济": <number>,
  "文化": <number>,
  "时间": <number>
}
```

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

Each call is assigned an ordering index deterministically.

---

## Hypotheses

### H1: Cross-Language Configural Invariance Under Bilingual Anchoring
Under Condition A (bilingual), cross-language profiles for the same brand correlate > .90 (cosine similarity). The English parenthetical anchors meaning, so profiles should be stable.

- **Test**: For each brand, compute mean spectral profile per language from Condition A. Compute pairwise cosine similarity across all 28 language pairs. Report median and minimum.
- **Success criterion**: Median cosine > .90 for all 5 brands.

### H2: Native-Only Labels Produce Semantic Drift
Condition B (native-only) produces significantly different weight profiles than Condition A (bilingual) for at least 4 of 7 non-English languages.

- **Test**: Paired-sample comparison per language. For each language, compute the mean absolute weight difference across 8 dimensions between Condition A and Condition B (paired by brand, model, rep). Wilcoxon signed-rank test (robust to non-normality).
- **Correction**: Bonferroni for 7 tests (alpha = .05 / 7 = .00714).
- **Effect size**: Mean absolute drift magnitude (percentage points) with 95% bootstrap CI.

### H3: Dimension-Specific Cultural Drift Directions
When English anchors are removed (Condition B vs A), specific dimensions shift in culturally predictable directions:
- **H3a**: Arabic Ideological weight increases (Islamic/political valence of native term stronger than "Ideological")
- **H3b**: Japanese Cultural weight increases (native "culture" concept carries stronger tradition/heritage load)
- **H3c**: Hindi Economic weight increases (native economic framing carries stronger price-sensitivity connotation)

- **Test**: Paired t-test per hypothesis (Condition B minus Condition A weight for the target dimension, per language). Bonferroni-corrected alpha = .05 / 3 = .0167.
- **Effect size**: Cohen's d (paired) with 95% bootstrap CI (10,000 iterations).

### H4: Collectivist Language Social Dimension Amplification
Under Condition B (native-only), collectivist languages (Chinese, Japanese, Korean) show larger Social dimension weights than individualist languages (English baseline from Condition A, Spanish Condition B).

- **Test**: Independent-samples t-test: collectivist group Condition B Social weights vs individualist group Social weights.
- **Alpha**: .05 (single test).
- **Effect size**: Cohen's d with 95% bootstrap CI.

---

## Power Analysis

### H2 (Wilcoxon signed-rank, 7 tests)
- Per-language Condition A sample: 30 observations (5 brands x 3 models x 2 reps)
- Per-language Condition B sample: 30 observations (paired)
- For medium effect (r = .30), power = .80, alpha = .00714: minimum n ~ 28 per group.
- Available n = 30. **Power adequate for medium effects.**

### H3 (paired t-tests, 3 comparisons)
- Per-language paired observations: 30
- For Cohen's d = .50 (medium), alpha = .0167: power ~.65. **Borderline for medium effects; large effects (d > .70) well-powered.**
- Limitation noted: small within-language sample (30 pairs). Compensated by effect being pooled across brands.

### H4 (t-test, 1 comparison)
- Collectivist group: 90 observations (3 languages x 30)
- Individualist group: 60 observations (English 30 + Spanish 30)
- For Cohen's d = .30, alpha = .05: power ~.62. **Adequate for medium effects only.**

---

## Dimension Label Translations

### Chinese (zh)
- Bilingual: 符号学 (Semiotic), 叙事 (Narrative), 意识形态 (Ideological), 体验 (Experiential), 社会 (Social), 经济 (Economic), 文化 (Cultural), 时间 (Temporal)
- Native-only: 符号学, 叙事, 意识形态, 体验, 社会, 经济, 文化, 时间

### Russian (ru)
- Bilingual: Семиотический (Semiotic), Нарративный (Narrative), Идеологический (Ideological), Эмпирический (Experiential), Социальный (Social), Экономический (Economic), Культурный (Cultural), Темпоральный (Temporal)
- Native-only: Семиотический, Нарративный, Идеологический, Эмпирический, Социальный, Экономический, Культурный, Темпоральный

### Japanese (ja)
- Bilingual: 記号論的 (Semiotic), 物語的 (Narrative), イデオロギー的 (Ideological), 体験的 (Experiential), 社会的 (Social), 経済的 (Economic), 文化的 (Cultural), 時間的 (Temporal)
- Native-only: 記号論的, 物語的, イデオロギー的, 体験的, 社会的, 経済的, 文化的, 時間的

### Korean (ko)
- Bilingual: 기호학적 (Semiotic), 서사적 (Narrative), 이념적 (Ideological), 체험적 (Experiential), 사회적 (Social), 경제적 (Economic), 문화적 (Cultural), 시간적 (Temporal)
- Native-only: 기호학적, 서사적, 이념적, 체험적, 사회적, 경제적, 문화적, 시간적

### Arabic (ar)
- Bilingual: سيميائي (Semiotic), سردي (Narrative), أيديولوجي (Ideological), تجريبي (Experiential), اجتماعي (Social), اقتصادي (Economic), ثقافي (Cultural), زمني (Temporal)
- Native-only: سيميائي, سردي, أيديولوجي, تجريبي, اجتماعي, اقتصادي, ثقافي, زمني

### Hindi (hi)
- Bilingual: चिह्नशास्त्रीय (Semiotic), कथात्मक (Narrative), वैचारिक (Ideological), अनुभवात्मक (Experiential), सामाजिक (Social), आर्थिक (Economic), सांस्कृतिक (Cultural), कालिक (Temporal)
- Native-only: चिह्नशास्त्रीय, कथात्मक, वैचारिक, अनुभवात्मक, सामाजिक, आर्थिक, सांस्कृतिक, कालिक

### Spanish (es)
- Bilingual: Semiótico (Semiotic), Narrativo (Narrative), Ideológico (Ideological), Experiencial (Experiential), Social (Social), Económico (Economic), Cultural (Cultural), Temporal (Temporal)
- Native-only: Semiótico, Narrativo, Ideológico, Experiencial, Social, Económico, Cultural, Temporal

### English (en) -- control
- English: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal
- (Only one condition: bilingual = native for English)

---

## Analysis Plan

### Primary Analyses (pre-registered)

1. **Per-language x condition mean spectral profiles**: 8 languages x 2 conditions x 5 brands x 8 dimensions. Visualization: paired heatmaps per brand.

2. **H1 -- Cross-language cosine similarity under bilingual anchoring**: 28 pairwise cosines from Condition A profiles per brand.

3. **H2 -- Condition A vs B drift magnitude**: Per language, mean absolute weight difference across 8 dimensions. Wilcoxon signed-rank test. Visualization: bar chart of drift magnitude per language.

4. **H3 -- Dimension-specific cultural drift**: Paired t-tests for 3 hypothesized dimension-language combinations.

5. **H4 -- Collectivist Social amplification**: Independent-samples t-test on Social weights.

### Exploratory Analyses (labeled EXPLORATORY)

6. **Model x Language x Condition interaction**: 3-way ANOVA per dimension.

7. **Drift direction heatmap**: For each language, signed drift (Condition B minus A) per dimension. 7 languages x 8 dimensions heatmap.

8. **Hierarchical clustering on native-only profiles**: Do languages cluster by linguistic family or cultural distance?

9. **Per-brand language sensitivity**: Which brands show the most cross-language variation?

---

## Exclusion Criteria

- API errors with unparseable responses: recorded with error field, excluded from analysis
- Weights not summing to 100 (+-5 tolerance): renormalized if parseable, flagged
- Models with >50% error rate for any language: excluded from that language's analysis
- Native-only label parsing: match against native label dictionary (case-insensitive, whitespace-tolerant)

---

## Random Seeds

- Call order randomization: 42
- Bootstrap CI: 12345
- Latin-square assignment: deterministic from call parameters

---

## Canonical Brand Profiles

- Hermes: [9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]
- IKEA: [8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]
- Patagonia: [6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]
- Erewhon: [7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5]
- Tesla: [7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]

---

## Models

| Name | Model ID | Provider | API Key |
|------|----------|----------|---------|
| Claude Haiku 4.5 | claude-haiku-4-5 | Anthropic | ANTHROPIC_API_KEY |
| GPT-4o-mini | gpt-4o-mini | OpenAI | OPENAI_API_KEY |
| Gemini 2.5 Flash | gemini-2.5-flash | Google | GOOGLE_API_KEY |

---

## Success Criteria

- **H1 supported**: Median cosine > .90 for all 5 brands under bilingual condition
- **H2 supported**: At least 4 of 7 languages show significant drift (p < .00714)
- **H3 supported**: At least 1 of 3 directional predictions confirmed (p < .0167, Cohen's d > .30)
- **H4 supported**: Collectivist group Social weight significantly higher (p < .05)

---

*This protocol was committed before any API calls were made. Any analysis not specified above is labeled EXPLORATORY in the results.*
