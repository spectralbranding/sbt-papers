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
| Run 5 | 7 cross-cultural pairs, 22 models, 8 cultures | 11,410 (7,999 successful) | **Complete (2026-04-06)** | H1 SUPPORTED (p<0.0001, DCI=35.6), H2 SUPPORTED (cosine=0.976), 69 native-language calls |
| H12 Framing | 3 framing pairs, same models as Run 5, 2 city contexts each | ~pending | **Pending** | H12: geopolitical framing effect on dimensional weights |

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
- **H7 (Geopolitical Valence)**: Models will show systematic DCI differences between Tinkoff (Russia) and PrivatBank (Ukraine), reflecting post-2022 geopolitical framing in training data. Both are digital-first consumer banks in the same category — category confound eliminated. Exploratory — no directional prediction.
- **H8 (Thin-Data Floor)**: APU Chinggis (Mongolia) will have the highest DCI across all models
- **H9 (Capacity-Dependent Collapse)**: Smaller models (7-8B) will exhibit higher DCI than larger models (30B+) from the same culture
- **H10 (Prompt Language Effect)**: Culture-matched models prompted in their native language will show lower DCI for local brands than when prompted in English

### H12 — Geopolitical Framing (pre-registered 2026-04-07)

- **H12 (Geopolitical Framing Effect)**: The same brand receives systematically different dimensional weight profiles when evaluated in two different geopolitical city contexts. Brand, product, and prompt structure are held constant; only the city context changes. Non-zero deltas on Ideological, Cultural, or Temporal dimensions confirm that LLMs encode geopolitical framing in their brand weights.

Three framing pairs (2x2 design: city context x prompt language):

| Pair ID | Brand | City A | City B | Framing Type |
|---------|-------|--------|--------|--------------|
| roshen_ru_ua | Roshen chocolate | Moscow | Kyiv | Active conflict |
| volvo_eu_cn | Volvo XC90 | Stockholm | Shanghai | Ownership transfer (Geely 2010) |
| burgerking_us_ru | Burger King | New York | Moscow | Stay-vs-leave decision (2022) |

Full pre-registration: `L0_specification/PRE_REGISTRATION_RUN5.md`

---

## Run 5 Design

### Cross-Cultural Brand Pairs (7 pairs, 8 cultures)

| Pair | Local Brand | Global Brand | Category | Culture |
|------|-------------|--------------|----------|---------|
| china_water | Nongfu Spring | Evian | Bottled water | Chinese |
| japan_snacks | Calbee | Lay's | Snacks | Japanese |
| uae_dairy | Al Rawabi | Danone | Dairy | Arabic |
| russia_ukraine_banking | Tinkoff (T-Bank) | PrivatBank | Digital banking | Russian/Ukrainian |
| mongolia_beer | APU Chinggis | Heineken | Beer | Mongolian |
| korea_dairy | Binggrae | Danone | Dairy/beverages | Korean |
| india_dairy | Amul | Danone | Dairy products | Indian |

### Models (22 active in Run 5 — see `L1_configuration/models.yaml`)

**Tier 1 (30B+, primary analysis)**: 17 models across 7 cultures
**Tier 2 (7-30B, H9 capacity comparison)**: 4 models

Clusters:
- Western: Claude Sonnet 4.6, GPT-4o-mini, Gemini 2.5 Flash, Llama 3.3 70B, Grok-4.1, Gemma 4 27B
- Chinese: DeepSeek V3, Qwen3 30B, Qwen3-235B (Cerebras), GLM-4.7, Qwen3-32B (SambaNova), DeepSeek V3.2 (SambaNova), Kimi K2, Qwen3.5 27B
- Russian: GigaChat 2 Max, YandexGPT 5 Pro, YandexGPT 5 Lite 8B, GigaChat 3.1 Lightning (T-Pro 2.0 produced 0 successful responses — excluded from analysis)
- Japanese: Swallow 70B (SambaNova), Swallow 8B (local)
- Korean: EXAONE 4.0 32B
- Arabic: Jais 70B, Falcon-H1-Arabic 7B, ALLaM-2-7B
- Indian: Sarvam-105B

Open-weight models are preferred over closed-weight cloud APIs to isolate cultural training data
bias from commercial alignment confounds. Paid APIs: Claude (Anthropic), GPT (OpenAI), Gemini
(Google), DeepSeek V3 cloud (DeepSeek). Free-tier APIs: Grok (xAI), Llama 3.3 / Kimi K2 /
ALLaM-2-7B (Groq), Qwen3-235B / GLM-4.7 (Cerebras), Qwen3-32B / DeepSeek V3.2 / Swallow 70B
(SambaNova), Sarvam-105B (Indus API), GigaChat 2 Max (Sber API), YandexGPT 5 Pro (Yandex AI
Studio). Local Ollama models incur no API cost.

### Native-Language Prompt Condition (H10)

For culture-matched model-brand pairs, the `weighted_recommendation` prompt is also run in
the model's native language (Chinese, Russian, Japanese, Korean, Arabic, Hindi). This tests
whether dimensional collapse is an artifact of English prompting or a structural property
of the model's cultural knowledge.

- JSON keys remain in English for consistent parsing
- Only instructional text and dimension descriptions are translated (manually, not by machine)
- Total native-language calls: ~18 (6 culture-matched models x 1 prompt x 3 runs)

### Call Volume (actual Run 5 results)

| Condition | Actual |
|-----------|--------|
| Run 5 total calls | 11,410 |
| Run 5 successful responses | 7,999 (70.1%) |
| Native-language calls (H10) | 69 |
| Runs 2-4 calls | 4,860 |
| **All runs total** | **16,270** |

---

## OST Specification Cascade

| Level | Directory | Contents | Status |
|-------|-----------|----------|--------|
| L0 | `L0_specification/` | Hypotheses, design, pre-registrations | Complete |
| L1 | `L1_configuration/` | Model configs, API version records | Complete |
| L2 | `L2_prompts/` | Prompt templates reference | Templates in script; rendered examples pending |
| L3 | `L3_sessions/` | JSONL session logs | Complete (run2-run5 logs committed) |
| L4 | `L4_analysis/` | Results, summary tables | Complete (run5_analysis.py + outputs) |

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

Run 5 cross-cultural (22 models, 7 pairs, 8 cultures):

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

H12 geopolitical framing only (3 pairs, 2 city contexts each):

```
python ai_search_metamerism.py --live --runs 3 --framing-only \
  --log L3_sessions/run_framing.jsonl \
  --output L4_analysis/results_framing.json \
  --summary L4_analysis/summary_framing.md
```

H12 framing combined with cross-cultural Run 5 pairs:

```
python ai_search_metamerism.py --live --runs 3 --crosscultural-only --framing \
  --log L3_sessions/run_h12.jsonl \
  --output L4_analysis/results_h12.json \
  --summary L4_analysis/summary_h12.md
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
export YANDEX_AI_API_KEY=...        # YandexGPT 5 Pro (Russian); T-Pro 2.0 uses same key but had 0 successful responses in Run 5

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
| `run5_results.json` | Run 5 full results (10.8MB): all calls, DCI per model/pair, test statistics |
| `run5_summary.md` | Run 5 summary tables: DCI by model, cosine similarity matrix, H5-H10 test results |
| `run5_gptoss_results.json` | Supplemental: gpt-oss-20b/Swallow run (435 calls) |
| `run5_gptoss_summary.md` | Supplemental summary for gpt-oss run |
| `L4_analysis/run5_analysis.py` | Post-processing analysis script |
| `L4_analysis/run5_analysis_results.json` | Analysis outputs: diagonal advantage matrix, H9/H10 tests |
| `L4_analysis/run5_dci_table.csv` | DCI per model per culture (H5 matrix) |
| `L4_analysis/run5_diagonal_advantage.csv` | Diagonal advantage scores (H5 primary measure) |
| `L3_sessions/run5_crosscultural.jsonl` | JSONL session log for Run 5 (14MB) |
| `L3_sessions/run5_gptoss_swallow.jsonl` | JSONL session log for supplemental run |
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
