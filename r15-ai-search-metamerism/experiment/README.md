# R15 AI Search Metamerism Experiment

Tests whether LLMs produce convergent brand recommendations that mask structural
differences in brand perception clouds -- the phenomenon of spectral metamerism
applied to AI-mediated consumer search.

**Paper**: Zharnikov, D. (2026v). Spectral Metamerism in AI-Mediated Brand Perception.


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

## Design

**10 brand pairs** spanning luxury, mass-market, purpose-driven, and technology:

| Pair | Brand A | Brand B | Primary Differentiator |
|------|---------|---------|------------------------|
| luxury_heritage | Hermes | Coach | Temporal + Cultural |
| purpose_driven | Patagonia | Columbia | Ideological + Narrative |
| premium_tech | Apple | Samsung | Experiential + Semiotic |
| artisanal_food | Erewhon | Whole Foods | Social + Economic |
| auto_disruption | Mercedes | Tesla | Temporal + Ideological |
| indie_beauty | Glossier | Maybelline | Narrative + Social |
| craft_spirits | Hendricks | Gordons | Cultural + Experiential |
| boutique_hotel | Aman | Four Seasons | Experiential + Temporal |
| heritage_sportswear | Nike | Shein | Narrative + Cultural |
| ethical_finance | Aspiration | Chase | Ideological + Social |

**3 prompt types per pair** (18 prompts per pair per run per model):
1. Recommendation: free prose recommendation -- which dimensions get cited?
2. Differentiation: structured JSON with key differences and differentiation score
3. Dimension probes: 8 probes x 2 brands, scoring 0-10 on each SBT dimension

**6 model families**: Claude Haiku 3.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3,
Qwen Plus (cloud), Qwen3 30B (local), Gemma 4 27B (local)

**Temperature**: 0.7 for all calls (cross-model variance is the signal, not suppressed)

**Total calls**: 10 pairs x 18 prompts x 6 models x 3 runs = 3,240 (standard)

---

## Hypotheses

- **H1**: Economic and Semiotic dimensions are cited more than the uniform baseline (1/8 per dim)
- **H2**: Citation patterns are consistent across model families (Fleiss kappa >= 0.40)
- **H3**: Cross-model variance is higher for soft dimensions (Narrative, Cultural, Temporal)
  than hard dimensions (Economic, Semiotic, Experiential)
- **H4**: Soft-dimension brand pairs show higher cross-model recommendation convergence

Full pre-registration: `L0_specification/protocol.md`

---

## OST Specification Cascade

| Level | Directory | Contents | Status |
|-------|-----------|----------|--------|
| L0 | `L0_specification/` | Hypotheses, design, pre-registration | Ready |
| L1 | `L1_configuration/` | Model configs, API version records | Ready |
| L2 | `L2_prompts/` | Prompt templates reference | Ready |
| L3 | `L3_sessions/` | JSONL session logs (generated at runtime) | Pending |
| L4 | `L4_analysis/` | Results, summary tables (generated at runtime) | Pending |

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

Pilot run (1 run, ~1,080 calls):

```
python ai_search_metamerism.py --live --runs 1 \
  --log L3_sessions/session_log.jsonl \
  --output L4_analysis/pilot_results.json \
  --summary L4_analysis/pilot_summary.md
```

Standard run (3 runs, ~3,240 calls):

```
python ai_search_metamerism.py --live --runs 3 \
  --log L3_sessions/session_log.jsonl \
  --output L4_analysis/results.json \
  --summary L4_analysis/summary_tables.md
```

Required environment variables:

```
export ANTHROPIC_API_KEY=...        # Claude Haiku 3.5
export OPENAI_API_KEY=...           # GPT-4o-mini
export GOOGLE_API_KEY=...           # Gemini 2.5 Flash
export DEEPSEEK_API_KEY=...         # DeepSeek V3
export DASHSCOPE_API_KEY=...        # Qwen Plus (optional -- backfill when available)
# Ollama: start with `ollama serve` and pull qwen3:30b, gemma4:latest
```

Missing keys are skipped gracefully.

---

## Output Files

| File | Contents |
|------|----------|
| `results.json` | Full structured results: all calls, citation frequencies, probe scores, statistics |
| `summary_tables.md` | Formatted Markdown tables: metadata, citation frequency, DCI, probe scores, tests |
| `L3_sessions/session_log.jsonl` | Every API call with prompt, response, parsed output, latency, errors |
| `metadata.yaml` | Package versions, hardware, git hash, model configs, API key hashes |
| `L0_specification/PRE_REGISTRATION.md` | Protocol written before data collection |

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
  (Prediction: they collapse to Economic + Semiotic, ignoring soft dimensions.)

Both support the theoretical claim that AI-mediated brand interaction produces a
perceptual reduction that SBT's 8-dimensional framework is designed to measure and counteract.

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

---

## Reproduction

```bash
# Demo (verify pipeline without API calls)
uv run python ai_search_metamerism.py --demo

# Live pilot
uv run python ai_search_metamerism.py --live --runs 1 --log L3_sessions/session_log.jsonl
```
