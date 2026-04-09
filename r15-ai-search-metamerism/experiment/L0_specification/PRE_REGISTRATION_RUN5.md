# Pre-Registration Protocol: R15 Run 5 — Cross-Cultural Information Asymmetry

**Date**: 2026-04-05 (written before data collection)
**Paper**: Zharnikov, D. (2026v). Spectral Metamerism in AI-Mediated Brand Perception.
**Target**: Under review
**DOI (Runs 1-4)**: 10.5281/zenodo.19422427

---

## 1. Hypotheses

**H5 (Cultural Training Data Advantage)**: Models trained primarily on a specific culture's web data will produce lower DCI (Dimensional Collapse Index) for brands from that culture than for brands from other cultures. Specifically:
- Chinese-trained models (Qwen3, DeepSeek) will have lower DCI for Nongfu Spring than Western-trained models
- Russian-trained models (YandexGPT, GigaChat) will have lower DCI for Tinkoff than Western-trained models
- Korean-trained models (EXAONE) will have lower DCI for Binggrae than Western-trained models
- Arabic-trained models (Falcon-H1-Arabic) will have lower DCI for Al Rawabi than Western-trained models
- Japanese-trained models (Swallow) will have lower DCI for Calbee than Western-trained models
- Indian-trained models (Sarvam-105B) will have lower DCI for Amul than Western-trained models

**H6 (Bidirectional Asymmetry)**: The cultural advantage is bidirectional — Western-trained models will have lower DCI for Evian/Lay's/Danone/Heineken than national models from non-Western cultures.

**H7 (Geopolitical Valence)**: Models will show systematic differences in perception of Tinkoff (Russia) vs PrivatBank (Ukraine), reflecting geopolitical framing in training data post-2022. Both are digital-first consumer banks occupying analogous market positions — same category, eliminating the category confound. This is exploratory (no directional prediction).

**H8 (Thin-Data Floor)**: APU Chinggis (Mongolia) will have the highest DCI across all models, establishing a floor for dimensional collapse when training data is near-zero.

**H9 (Capacity-Dependent Collapse)**: Smaller models (7-8B) will exhibit higher DCI than larger models (30B+) from the same culture, suggesting dimensional collapse is partially a function of model capacity rather than solely training data distribution. Testable pairs: Swallow 8B vs 70B (Japanese), ALLaM 7B vs Jais 70B (Arabic), YandexGPT 8B vs YandexGPT 5 Pro (Russian), Qwen3 30B vs Qwen3-235B (Chinese).

**H10 (Prompt Language Effect)**: Culture-matched models prompted in their native language will show lower DCI for local brands than the same models prompted in English. The magnitude of this effect will be larger for models with smaller parameter counts. Test: within-model paired comparison of English vs native-language weighted_recommendation prompts on culture-matched brand pairs.

**H11 (Supplementary pairs)**: VkusVill (Russia), Roshen (Ukraine), and APU Chinggis (Mongolia) are collected as supplementary data points. Their DCI values are expected to follow the same cross-cultural pattern as primary pairs. Not featured in publications due to category mismatches but included in session logs for replication purposes.

**H12 (Geopolitical Framing Effect)**: The same brand evaluated in two different city/country contexts will receive systematically different dimensional weight profiles. The brand, product, and prompt structure are held constant; only the city context changes. If LLMs encode geopolitical framing in their training data, dimensional weights for Ideological, Cultural, and Temporal dimensions will differ significantly between the two city contexts (2x2 design: city_a vs city_b x English vs native language).

Three brand pairs test distinct framing mechanisms:
1. **roshen_ru_ua** (Roshen chocolate, Moscow vs Kyiv): Tests framing in an active conflict context. Roshen was sold in both Russian and Ukrainian markets. Roshen's owner (Petro Poroshenko) became a public figure in Ukrainian politics post-2014. Models with heavy coverage of this period may associate the brand differently depending on city context.
2. **volvo_eu_cn** (Volvo XC90, Stockholm vs Shanghai): Tests ownership-transfer framing. Volvo is a Swedish brand acquired by Chinese Geely in 2010. Same product, same brand, two different ownership-narrative contexts. Models trained on Western vs Chinese web corpora may weight Narrative and Cultural dimensions differently.
3. **burgerking_us_ru** (Burger King, New York vs Moscow): Tests stay-vs-leave framing. Burger King continued operating in Russia after 2022 while McDonald's exited. The brand's decision to stay changed its meaning in each market. Models may weight Ideological dimension differently depending on city context.

Native-language condition (H12 x H10 interaction): For city contexts with a non-English native language, culture-matched models are additionally prompted in the native language. This tests whether the framing effect is amplified when the model operates in the language of the geopolitical context.

Analysis: For each framing pair, compute the per-dimension weight delta (city_b - city_a) per model. H12 is supported if at least two of the three pairs show a statistically significant non-zero delta on at least one dimension. Primary dimensions of interest: Ideological, Cultural, Temporal (soft dimensions most likely to encode geopolitical framing).

Pre-registration date: 2026-04-07 (framing experiment designed after Run 5 completion).

## 2. Design

### 2.1 Brand Pairs
7 cross-cultural pairs (see CROSSCULTURAL_BRAND_PAIRS in ai_search_metamerism.py):
1. China: Nongfu Spring vs Evian (bottled water)
2. Japan: Calbee vs Lay's (snacks)
3. UAE: Al Rawabi vs Danone (dairy)
4. Russia/Ukraine: Tinkoff vs PrivatBank (digital banking — geopolitical pair, same category)
5. Mongolia: APU Chinggis vs Heineken (beer)
6. South Korea: Binggrae vs Danone (dairy/beverages)
7. India: Amul vs Danone (dairy products)

### 2.2 Models
Open-weight models used where available to isolate cultural training data bias from commercial alignment confounds.

**Carried forward from Runs 2-4** (6 models):
- Claude Sonnet 4.6 (Anthropic, Western, proprietary — no open-weight exists)
- GPT-4o-mini (OpenAI, Western, proprietary — no open-weight exists)
- Gemini 2.5 Flash (Google, Western, proprietary — no open-weight exists)
- DeepSeek V3 (DeepSeek, Chinese, open-weight via SambaNova)
- Qwen3 30B (Alibaba, Chinese, local Ollama)
- Gemma 4 27B (Google, Western/multilingual, local Ollama)

**New national models** (Run 5):
- EXAONE 4.0 32B (LG AI Research, Korean, local GGUF)
- YandexGPT 5 Lite 8B (Yandex, Russian, local Ollama)
- GigaChat 3.1 Lightning (Sber, Russian, local GGUF, MIT license)
- Swallow 8B (Tokyo Tech, Japanese, local GGUF)
- Sarvam-105B (Sarvam AI, Indian, Indus API free tier, Apache 2.0)

**Free-tier cloud additions**:
- Qwen3-32B via Cerebras (same weights as Qwen3 local — replication check)
- Llama 3.3 70B via Groq (Western open-weight baseline)
- Qwen 2.5 72B via SambaNova (larger Chinese model)

### 2.3 Methodological Note: Open-Weight Preference
Open-weight models expose the training data distribution directly, without the commercial alignment layer (safety tuning, helpfulness optimization, brand-sensitivity guardrails) that proprietary APIs add. Since our experimental variable is cultural training data bias — not commercial alignment strategy — the open-weight variant provides a cleaner test of the hypothesis. Commercial alignment is a confound we are not testing; removing it strengthens the causal inference.

Proprietary APIs are retained only for models where no open-weight equivalent exists (Claude, GPT, Gemini).

### 2.4 Prompts
Same three prompt types as Runs 2-4 (backward compatible):
1. Weighted recommendation (100-point allocation across 8 dimensions)
2. Dimensional differentiation (0-10 per-dimension difference scores)
3. Dimension probe (individual brand scoring per dimension)

Temperature: 0.7 (same as Runs 2-4)
Max tokens: 2048 (same as Runs 2-4, except Qwen3 local: 4096)
Runs per prompt: 3 (same as Runs 2-4)

### 2.5 Native-Language Prompt Condition (H10)

For culture-matched model-brand pairs, the weighted_recommendation prompt is also run in the model's native language. This tests whether dimensional collapse is an artifact of English prompting vs a property of the model's cultural knowledge.

Design: within-model paired comparison (English vs native on the same brand pair).
Only weighted_recommendation is translated (primary DCI measure). Differentiation and probes remain English for JSON parse reliability.
JSON keys stay in English across all languages for consistent parsing. Only instructional text and dimension descriptions are translated.
Translations are manual, not machine-generated.

Languages: Chinese (zh), Russian (ru), Japanese (ja), Korean (ko), Arabic (ar), Hindi (hi).
Native calls per model: 1 native brand pair x 1 prompt x 3 runs = 3 additional calls per culture-matched model.
Total native calls: ~6 model-culture matches x 3 runs = ~18 additional calls.

### 2.6 Sample Size
- English: 8 pairs x 18 prompts/pair x 3 runs x ~21 models = ~9,072 calls
- Native-language: ~18 additional calls (culture-matched weighted_recommendation only)
- Total Run 5: ~9,090 calls
- With Runs 2-4 carried forward (4,860 calls), total dataset: ~13,950 calls

## 3. Analysis Plan

### 3.1 Primary Analysis (H5)
For each culture c with national model m_c:
- Compute DCI for m_c on the local brand from culture c
- Compute DCI for all other models on the same brand
- Test: paired t-test (m_c DCI vs mean other-model DCI)
- Report: Cohen's d, 95% CI, Bonferroni-corrected p-value (8 cultures)

### 3.2 Diagonal Advantage Matrix
Construct a models x cultures matrix of DCI values. The "diagonal" (each national model on its own culture's brand) should have systematically lower DCI than off-diagonal cells. Test via permutation test.

### 3.3 Backward Compatibility
For the 6 original models, compare DCI on Run 5 cross-cultural pairs to DCI on Run 3 local pairs (same model, different local brands). If DCI values are in the same range, backward compatibility is confirmed.

### 3.4 Exploratory (H7)
Compare Tinkoff vs PrivatBank DCI patterns across all models. Both are digital-first consumer banks (same category), so the geopolitical salience of the Russian-Ukrainian context since 2022 is the primary variable. No directional prediction — report descriptive statistics and flag any systematic pattern.

## 4. Stopping Rules

- If >20% of calls for any model produce invalid JSON (after retries), exclude that model and report the exclusion
- If a model's DCI variance across 3 runs exceeds 0.15 (indicating unreliable output), flag for manual review
- Do not add or remove models after data collection begins
- Do not modify prompts after data collection begins

## 5. Data and Code Availability

All session logs (JSONL), analysis code, and raw results will be deposited in:
- GitHub: spectralbranding/sbt-papers/r15-ai-search-metamerism/experiment/
- Zenodo: update existing DOI 10.5281/zenodo.19422427

## 6. Deviations from Runs 2-4

| Aspect | Runs 2-4 | Run 5 | Rationale |
|---|---|---|---|
| Brand pairs | 10 global + 5 local | 8 cross-cultural | Tests cultural training data asymmetry (new hypothesis) |
| Models | 6 (3 cloud + 2 local + 1 cloud Chinese) | 15+ (6 original + 6 national + 3+ cloud free-tier) | National models provide culture-specific test |
| Qwen variant | Qwen3 30B local | Same + Qwen3-32B Cerebras (replication) | Replication check: same weights, different endpoint |
| DeepSeek variant | DeepSeek V3 cloud API | DeepSeek V3 SambaNova | Open-weight, removes commercial alignment confound |
| Open-weight policy | Mixed (cloud + local) | Open-weight preferred | Isolates training data variable from alignment |
