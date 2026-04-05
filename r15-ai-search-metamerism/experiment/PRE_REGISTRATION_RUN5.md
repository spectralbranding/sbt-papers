# Pre-Registration Protocol: R15 Run 5 — Cross-Cultural Information Asymmetry

**Date**: 2026-04-05 (written before data collection)
**Paper**: Zharnikov, D. (2026v). Spectral Metamerism in AI-Mediated Brand Perception.
**Target**: Journal of Advertising Research (JAR)
**DOI (Runs 1-4)**: 10.5281/zenodo.19422427

---

## 1. Hypotheses

**H5 (Cultural Training Data Advantage)**: Models trained primarily on a specific culture's web data will produce lower DCI (Dimensional Collapse Index) for brands from that culture than for brands from other cultures. Specifically:
- Chinese-trained models (Qwen3, DeepSeek) will have lower DCI for Nongfu Spring than Western-trained models
- Russian-trained models (YandexGPT, GigaChat) will have lower DCI for VkusVill than Western-trained models
- Korean-trained models (EXAONE) will have lower DCI for Binggrae than Western-trained models
- Arabic-trained models (Falcon-H1-Arabic) will have lower DCI for Al Rawabi than Western-trained models
- Japanese-trained models (Swallow) will have lower DCI for Calbee than Western-trained models

**H6 (Bidirectional Asymmetry)**: The cultural advantage is bidirectional — Western-trained models will have lower DCI for Evian/Lay's/Danone/Heineken than national models from non-Western cultures.

**H7 (Geopolitical Valence)**: Models will show systematic differences in perception of VkusVill (Russia) vs Roshen (Ukraine), reflecting geopolitical framing in training data post-2022. This is exploratory (no directional prediction).

**H8 (Thin-Data Floor)**: APU Chinggis (Mongolia) will have the highest DCI across all models, establishing a floor for dimensional collapse when training data is near-zero.

## 2. Design

### 2.1 Brand Pairs
7 cross-cultural pairs (see CROSSCULTURAL_BRAND_PAIRS in ai_search_metamerism.py):
1. China: Nongfu Spring vs Evian (bottled water)
2. Japan: Calbee vs Lay's (snacks)
3. UAE: Al Rawabi vs Danone (dairy)
4. Russia: VkusVill vs Whole Foods (organic grocery)
5. Ukraine: Roshen vs Cadbury (confectionery)
6. Mongolia: APU Chinggis vs Heineken (beer)
7. South Korea: Binggrae vs Danone (dairy/beverages)

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
- Falcon-H1-Arabic 7B (TII, Arabic/UAE, local GGUF)
- YandexGPT 5 Lite 8B (Yandex, Russian, local Ollama)
- GigaChat 20B-A3B (Sber, Russian, local GGUF, MIT license)
- Swallow 8B (Tokyo Tech, Japanese, local GGUF)

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

### 2.5 Sample Size
- 7 pairs x 3 prompt types x 3 runs x ~14 models = ~882 calls per model set
- Total: ~882 calls (original 6) + ~882 calls (new 8 national/cloud) = ~1,764 calls
- With Runs 2-4 carried forward (4,860 calls), total dataset: ~6,624 calls

## 3. Analysis Plan

### 3.1 Primary Analysis (H5)
For each culture c with national model m_c:
- Compute DCI for m_c on the local brand from culture c
- Compute DCI for all other models on the same brand
- Test: paired t-test (m_c DCI vs mean other-model DCI)
- Report: Cohen's d, 95% CI, Bonferroni-corrected p-value (7 cultures)

### 3.2 Diagonal Advantage Matrix
Construct a models x cultures matrix of DCI values. The "diagonal" (each national model on its own culture's brand) should have systematically lower DCI than off-diagonal cells. Test via permutation test.

### 3.3 Backward Compatibility
For the 6 original models, compare DCI on Run 5 cross-cultural pairs to DCI on Run 3 local pairs (same model, different local brands). If DCI values are in the same range, backward compatibility is confirmed.

### 3.4 Exploratory (H7)
Compare VkusVill vs Roshen DCI patterns across all models. No directional prediction — report descriptive statistics and flag any systematic pattern.

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
| Brand pairs | 10 global + 5 local | 7 cross-cultural | Tests cultural training data asymmetry (new hypothesis) |
| Models | 6 (3 cloud + 2 local + 1 cloud Chinese) | 14 (6 original + 5 national + 3 cloud free-tier) | National models provide culture-specific test |
| Qwen variant | Qwen3 30B local | Same + Qwen3-32B Cerebras (replication) | Replication check: same weights, different endpoint |
| DeepSeek variant | DeepSeek V3 cloud API | DeepSeek V3 SambaNova | Open-weight, removes commercial alignment confound |
| Open-weight policy | Mixed (cloud + local) | Open-weight preferred | Isolates training data variable from alignment |
