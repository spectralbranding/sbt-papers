# R15 AI Search Metamerism Experiment

Tests whether LLMs produce convergent brand recommendations that mask structural
differences in brand perception clouds -- the phenomenon of spectral metamerism
applied to AI-mediated consumer search.

**Paper**: Zharnikov, D. (2026v). Spectral Metamerism in AI-Mediated Brand Perception.
**Target**: Under review
**DOI (Runs 1-4)**: 10.5281/zenodo.19422427

---

## Run Status

| Run | Design | Calls | Status | Key Result |
|-----|--------|-------|--------|------------|
| Run 1 | 10 global pairs, 3 models | ~540 | Complete | Pipeline verified |
| Run 2 | 10 global pairs, 6 models | ~3,240 | Complete | H1 SUPPORTED |
| Run 3 | 5 local brand pairs, 6 models | ~810 | Complete | H2 SUPPORTED (cosine=0.975), local DCI=0.355 |
| Run 4 | Brand Function resolution test, 6 models | ~90 | Complete | DCI 0.355→0.284 |
| Run 5 | 8 cross-cultural pairs, ~21 models | ~9,090 | **PENDING (~2026-04-08)** | H5-H10 pre-registered |

---

## The Research Question

When a consumer uses an LLM to ask "which brand should I choose?", does the LLM
faithfully represent the full spectrum of brand differentiation, or does it collapse
multi-dimensional differences to a small number of quantifiable dimensions?

The theoretical prediction: LLMs over-weight Economic and Semiotic dimensions (because
these are quantifiable and explicitly present in training data) and under-weight
Narrative, Ideological, Cultural, and Temporal dimensions (because these are
perception-dependent and difficult to extract from text corpora). The result is
spectral metamerism: brands that appear interchangeable through AI-mediated search
may have structurally different perception clouds when observed directly.

---

## Hypotheses

### Core (Runs 2-3, confirmed)

- **H1**: Economic and Semiotic dimensions are cited more than the uniform baseline (1/8 per dim). **SUPPORTED** (p < 0.0001)
- **H2**: Citation patterns are consistent across model families (Fleiss kappa >= 0.40). **SUPPORTED** (cosine = 0.975)
- **H3**: Cross-model variance is higher for soft dimensions (Narrative, Cultural, Temporal) than hard dimensions (Economic, Semiotic, Experiential)
- **H4**: Soft-dimension brand pairs show higher cross-model recommendation convergence

### Run 5 — Cross-Cultural Information Asymmetry (pre-registered 2026-04-05)

- **H5 (Cultural Training Data Advantage)**: National models will have lower DCI for their home-culture brands than for other-culture brands
- **H6 (Bidirectional Asymmetry)**: Western models will have lower DCI for global brands than national models
- **H7 (Geopolitical Valence)**: Models will show systematic DCI differences between VkusVill (Russia) and Roshen (Ukraine), reflecting post-2022 geopolitical framing in training data. Exploratory — no directional prediction.
- **H8 (Thin-Data Floor)**: APU Chinggis (Mongolia) will have the highest DCI across all models
- **H9 (Capacity-Dependent Collapse)**: Smaller models (7-8B) will exhibit higher DCI than larger models (30B+) from the same culture
- **H10 (Prompt Language Effect)**: Culture-matched models prompted in their native language will show lower DCI for local brands than when prompted in English

Full pre-registration: `L0_specification/PRE_REGISTRATION_RUN5.md`

---

## Run 5 Design

### Cross-Cultural Brand Pairs (8 pairs, 8 cultures)

| Pair | Local Brand | Global Brand | Category | Culture |
|------|-------------|--------------|----------|---------|
| china_water | Nongfu Spring | Evian | Bottled water | Chinese |
| japan_snacks | Calbee | Lay's | Snacks | Japanese |
| uae_dairy | Al Rawabi | Danone | Dairy | Arabic |
| russia_grocery | VkusVill | Whole Foods | Organic grocery | Russian |
| ukraine_confectionery | Roshen | Cadbury | Confectionery | Ukrainian |
| mongolia_beer | APU Chinggis | Heineken | Beer | Mongolian |
| korea_dairy | Binggrae | Danone | Dairy/beverages | Korean |
| india_dairy | Amul | Danone | Dairy products | Indian |

### Models (21 total — see `L1_configuration/models.yaml`)

**Tier 1 (30B+, primary analysis)**: 17 models across 7 cultures
**Tier 2 (7-30B, H9 capacity comparison)**: 4 models

Clusters:
- Western: Claude Sonnet 4.6, GPT-4o-mini, Gemini 2.5 Flash, Llama 3.3 70B, Grok-4.1, Gemma 4 27B
- Chinese: DeepSeek V3, Qwen3 30B, Qwen3-235B (Cerebras), GLM-4.7, Qwen3-32B (SambaNova), DeepSeek V3.2 (SambaNova), Kimi K2, Qwen3.5 27B
- Russian: GigaChat 2 Max, YandexGPT 5 Pro, T-Pro 2.0, YandexGPT 5 Lite 8B, GigaChat 3.1 Lightning
- Japanese: Swallow 70B (SambaNova), Swallow 8B (local)
- Korean: EXAONE 4.0 32B
- Arabic: Jais 70B, Falcon-H1-Arabic 7B, ALLaM-2-7B
- Indian: Sarvam-105B

Open-weight models are preferred over proprietary cloud APIs to isolate cultural training data
bias from commercial alignment confounds. Proprietary APIs retained only where no open-weight
equivalent exists (Claude, GPT, Gemini).

### Native-Language Prompt Condition (H10)

For culture-matched model-brand pairs, the `weighted_recommendation` prompt is also run in
the model's native language (Chinese, Russian, Japanese, Korean, Arabic, Hindi). This tests
whether dimensional collapse is an artifact of English prompting or a structural property
of the model's cultural knowledge.

- JSON keys remain in English for consistent parsing
- Only instructional text and dimension descriptions are translated (manually, not by machine)
- Total native-language calls: ~18 (6 culture-matched models x 1 prompt x 3 runs)

### Call Volume

| Condition | Formula | Total |
|-----------|---------|-------|
| Run 5 English | 8 pairs x 18 prompts x ~21 models x 3 runs | ~9,072 |
| Run 5 native-language | 6 culture-matched models x 1 prompt x 3 runs | ~18 |
| **Run 5 total** | | **~9,090** |
| With Runs 2-4 carried forward | + 4,860 calls | **~13,950 total** |

---

## OST Specification Cascade

| Level | Directory | Contents | Status |
|-------|-----------|----------|--------|
| L0 | `L0_specification/` | Hypotheses, design, pre-registrations | Ready |
| L1 | `L1_configuration/` | Model configs, API version records | Ready |
| L2 | `L2_prompts/` | Prompt templates reference | Pending population |
| L3 | `L3_sessions/` | JSONL session logs (generated at runtime) | Pending Run 5 |
| L4 | `L4_analysis/` | Results, summary tables (generated at runtime) | Pending Run 5 |

---

## Quick Start

Install dependencies:

```
uv pip install -r requirements.txt
```

Demo mode (no API keys required):

```
python ai_search_metamerism.py --demo
```

Run 5 cross-cultural (21 models, 8 pairs):

```
python ai_search_metamerism.py --live --runs 3 --run5 \
  --log L3_sessions/session_run5.jsonl \
  --output L4_analysis/results_run5.json \
  --summary L4_analysis/summary_run5.md
```

Standard Runs 2-4 format (6 models, 10 global pairs):

```
python ai_search_metamerism.py --live --runs 3 \
  --log L3_sessions/session_log.jsonl \
  --output L4_analysis/results.json \
  --summary L4_analysis/summary_tables.md
```

Required environment variables (Run 5):

```
# Cloud — Western
export ANTHROPIC_API_KEY=...        # Claude Sonnet 4.6
export OPENAI_API_KEY=...           # GPT-4o-mini
export GOOGLE_API_KEY=...           # Gemini 2.5 Flash

# Cloud — Chinese
export DEEPSEEK_API_KEY=...         # DeepSeek V3
export CEREBRAS_API_KEY=...         # Qwen3-235B, GLM-4.7
export SAMBANOVA_API_KEY=...        # Qwen3-32B, DeepSeek V3.2, Swallow 70B
export GROQ_API_KEY=...             # Llama 3.3 70B, Kimi K2, ALLaM-2-7B

# Cloud — national models
export GROK_API_KEY=...             # Grok-4.1 (xAI)
export SARVAM_API_KEY=...           # Sarvam-105B (Indian)
export GIGACHAT_API_KEY=...         # GigaChat 2 Max (Russian)
export YANDEX_AI_API_KEY=...        # YandexGPT 5 Pro, T-Pro 2.0 (Russian)

# Local Ollama (start with `ollama serve`, then pull models)
# Required models: qwen3:30b, gemma4:latest, qwen3.5:27b
# National models (GGUF via hf.co): EXAONE 4.0 32B, YandexGPT 5 Lite 8B,
#   GigaChat 3.1 Lightning, Swallow 8B, Falcon-H1-Arabic 7B, Jais 70B
```

Missing keys are skipped gracefully.

---

## Output Files

| File | Contents |
|------|----------|
| `L4_analysis/results_run5.json` | Full structured results: all calls, DCI per model/pair, test statistics |
| `L4_analysis/summary_run5.md` | Formatted Markdown tables: diagonal matrix, H9 pairs, H10 language effect |
| `L3_sessions/session_run5.jsonl` | Every API call with prompt, response, parsed output, latency, errors |
| `L1_configuration/models.yaml` | Full model registry: tier, culture, size, backend, API key env vars |
| `L0_specification/PRE_REGISTRATION_RUN5.md` | Run 5 pre-registration protocol |
| `L0_specification/protocol.md` | Original pre-registration (Runs 1-3) |
| `L0_specification/resolution_protocol.md` | Run 4 pre-registration (Brand Function resolution) |

---

## SBT Dimensions (order matters)

| # | Dimension | Plain Language | Type |
|---|-----------|----------------|------|
| 1 | Semiotic | Visual identity and brand recognition | hard |
| 2 | Narrative | Brand story and origin narrative | soft |
| 3 | Ideological | Values and beliefs the brand stands for | soft |
| 4 | Experiential | Quality and distinctiveness of customer experience | hard |
| 5 | Social | Social signaling and community | soft |
| 6 | Economic | Value proposition and pricing strategy | hard |
| 7 | Cultural | Cultural relevance and heritage | soft |
| 8 | Temporal | Brand heritage and time horizon | soft |

**Hard** (Semiotic, Economic, Experiential): quantifiable, explicit in training data
**Soft** (Narrative, Ideological, Social, Cultural, Temporal): perception-dependent

---

## Relationship to R16

R15 and R16 test opposite sides of the same phenomenon:

- **R16** asks: can LLMs *tell brands apart* when given more behavioral information?
  (Answer: yes -- specification augmentation resolves behavioral metamerism.)

- **R15** asks: when LLMs *do* make brand recommendations, which dimensions do they use?
  (Confirmed: they collapse to Economic + Semiotic, ignoring soft dimensions.)

Both support the theoretical claim that AI-mediated brand interaction produces a
perceptual reduction that SBT's 8-dimensional framework is designed to measure and counteract.

---

## Reproduction

```bash
# Demo (verify pipeline without API calls)
uv run python ai_search_metamerism.py --demo

# Live pilot (Run 5, cross-cultural)
uv run python ai_search_metamerism.py --live --runs 1 --run5 \
  --log L3_sessions/session_run5.jsonl
```

---

## Run It On Your Own Brands

The experiment is designed to be forked. You can test any brand pairs with any models:

1. **Fork the repo**: `git clone https://github.com/spectralbranding/sbt-papers.git`
2. **Edit brand pairs**: In `ai_search_metamerism.py`, modify the `BRAND_PAIRS` list. Each pair needs:
   - `id`: short identifier (e.g., `"my_category"`)
   - `brand_a`, `brand_b`: the two brands to compare
   - `category`: product category (e.g., `"coffee brand"`)
   - `differentiating_dims`: which SBT dimensions you expect to differ most
   - `dim_type`: `"hard"`, `"soft"`, or `"mixed"`
3. **Set API keys**: Any combination works --- even a single model is informative
4. **Run**: `python ai_search_metamerism.py --live --runs 3 --log L3_sessions/my_session.jsonl`
5. **Check results**: `summary_tables.md` shows dimensional weight profiles and hypothesis tests

**Cost**: ~$0.80 for 3,240 calls (10 pairs, 6 models, 3 runs). Local models via Ollama are free.

**What to look for**:
- Which dimensions does the model over-weight for your brands?
- Do different models agree (high cosine similarity = structural collapse)?
- Are your brand's key differentiators (the dimensions you care about) in the "collapsed" category?

If you find something interesting, open an issue or PR. This is how science compounds.
