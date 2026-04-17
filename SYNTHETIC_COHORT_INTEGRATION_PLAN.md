# Synthetic Cohort Experiments — Integration Plan

**Created**: 2026-04-16
**Branch**: feature/synthetic-cohort-experiments
**Status**: Robustness fix in progress, then cascading updates

---

## Execution Summary

| Exp | Paper | Calls | Valid | Hypotheses | Cost |
|-----|-------|-------|-------|------------|------|
| 1 | R15 | 800 | 790 (98.8%) | H1 SUP, H2 SUP, H3 SUP | ~$0.65 |
| 2 | R16 | 675 | 648 (96.0%) | H1 SUP, H2 NOT SUP, H3 CONF | ~$0.40 |
| 3 | R18 | 300 | 297 (99.0%) | H1 SUP, H2 SUP, H3 EXPL | ~$0.25 |
| 4 | R17 | 0 | 741 (reused) | H1 CONF, H2 FAILS*, H3 CONF | $0 |

*H2 metric invariance fails as SBT predicts (rho=.548) — this is a POSITIVE result.

Models: Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash, DeepSeek V3, Grok 4.1 Fast (xAI).
Grok replaced qwen3_local (33% success -> 97% success, adds social-media-corpus training tradition).

---

## Phase 0: Robustness Fix (BLOCKING)

**Problem**: Dimension-order robustness check yielded Spearman rho = .486, below the .90 invariance threshold. The original design (50 calls, random shuffles) was underpowered and used an improper comparison method (individual scrambled calls vs baseline means).

**Fix**: Latin-square balanced experiment.
- 8x8 Latin square: 8 orderings, each dimension appears exactly once in each position
- 5 cohorts x 5 brands x 2 models x 8 orderings = 400 calls
- Proper analysis: compare ordering-aggregated profiles, not individual-to-mean
- Expected outcome: rho > .90 when comparing ordering-averaged means (position variance << cohort variance)

**Files**:
- Script: `r15-ai-search-metamerism/experiment/L2_prompts/run15_robustness_latin_square.py`
- Data: `r15-ai-search-metamerism/experiment/L3_sessions/run15_robustness_latin_square.jsonl`
- Analysis: `r15-ai-search-metamerism/experiment/L4_analysis/run15_robustness_analysis.py`

---

## Phase 1: Paper Updates

After robustness passes, add synthetic cohort experiment sections to each paper.

### R15 (Spectral Metamerism)
- **Add**: Section 5.13 "Synthetic Cohort Differentiation"
- **Content**: 800 calls, H1-H3 all supported, behavioral vignette methodology, dimension-order robustness (Latin square)
- **Update**: call count from 21,350 to 22,550 (21,350 + 800 main + 400 robustness)
- **Update**: run count from "10 runs" to "12 runs" (add Run 15 + Run 15b)
- **File**: `research/R15_ai_search_metamerism.md`

### R16 (AI-Native Brand Identity)
- **Add**: Section 8 "Synthetic Cohort Pilot"
- **Content**: 675 calls, Brand Function x Cohort interaction, Run 14 null generalizes
- **Update**: call count from 684 to 1,359 (684 + 675)
- **File**: `research/R16_ai_native_brand_identity.md`

### R17 (Brand Triangulation)
- **Add**: Discussion subsection on measurement invariance
- **Content**: configural holds, metric fails (as predicted), scalar fails, Economic most observer-dependent
- **No new calls** (reuses Exp 1 data)
- **File**: `research/R17_brand_triangulation.md`

### R18 (Spectral Dynamics)
- **Add**: Section 9 "Empirical Pilot: Synthetic Velocity Detection"
- **Content**: 300 calls, velocity perception, Bonnet pair resolution, Temporal invariance
- **Update**: from "theoretical" to "theoretical + empirical pilot"
- **File**: `research/R18_spectral_dynamics.md`

### PRISM Instrument
- **Add**: Implementation Evidence subsection
- **Content**: Synthetic cohort pre-pilot demonstrates instrument sensitivity without semantic priming
- **Zenodo**: 10.5281/zenodo.19555265 — upload updated version
- **File**: `research/PRISM_INSTRUMENT.md` (or equivalent)

---

## Phase 2: Metadata Updates

### paper.yaml / spec.yaml (sbt-papers)
- `r15-ai-search-metamerism/paper.yaml`: update sample.size, run count, model list
- `r16-ai-native-brand-identity/paper.yaml`: update call count
- `r18-spectral-dynamics/paper.yaml`: add empirical section flag
- `prism-instrument/paper.yaml`: add implementation evidence

### Zenodo export YAML (spectral-branding)
- `export/R15-ai-search-metamerism/zenodo/zharnikov-2026v-r15.yaml`
- `export/R16-ai-native-identity/zenodo/zharnikov-2026x-r16.yaml`
- `export/R17-brand-triangulation/zenodo/zharnikov-2026y-r17.yaml`
- `export/R18-spectral-dynamics/zenodo/paper.yaml`
- `export/prism-instrument/zenodo/zharnikov-2026-prism-instrument.yaml`

---

## Phase 3: Website and Public Content Updates

### Website paper cards
- Update R15 card: call count, add "synthetic cohort pilot" badge
- Update R16 card: call count
- Update R18 card: add "empirical pilot" flag
- Update PRISM card: add "pre-validated" flag

### llms.txt
- Create/update llms.txt with current paper inventory and synthetic cohort experiment metadata

### PROJECT_CONTEXT.md
- Update R15, R16, R17, R18 entries with new call counts and experiment results

### ATLAS.md
- Update R15 entry with new call count
- Add cross-references for synthetic cohort experiments

---

## Phase 4: Published Content Audit

### Articles (spectral-branding/articles/) — 10+ files reference "21,350"
- `standalone_ai_brand_audit.md`
- `standalone_ai_shopping_fails_twice.md`
- `standalone_mobile_brand_meter.md`
- `standalone_category_translation.md`
- `standalone_brand_function_howto.md`
- `standalone_lexus_exception.md`
- `standalone_gravity_of_brands.md`
- `SBT-C5_economic_dimension_is_special.md`
- `SBT-C7_lossy_compression.md`

### X Threads (launch/x_threads/) — 7+ files
- `R15_RESULTS_THREAD.md`
- `R15_SAME_PERCEPTION_THREAD.md`
- `R15_PATAGONIA_THREAD.md`
- `H10_NATIVE_LANGUAGE_THREAD.md`
- `C5_ECONOMIC_DIMENSION_THREAD.md`
- `R15_TEMPERATURE_THREAD.md`

### LinkedIn Posts (launch/linkedin/)
- Check all POST_*.md for R15 references

### Content Plan
- `launch/R15_CONTENT_PLAN.md`

### Already Published (Substack/LinkedIn/X)
- Flag posts that are already live with stale "21,350" numbers
- Decision needed: update published posts? Add correction notes? Leave as historical?

---

## Phase 5: Dataset Uploads

### HuggingFace
- `spectralbranding/r15-synthetic-cohorts` (new dataset)
- `spectralbranding/r16-behavioral-metamerism-pilot` (new dataset)
- `spectralbranding/r18-dimensional-velocity` (new dataset)
- Update existing `spectralbranding/r15-ai-search-metamerism` README with cross-reference

### Zenodo
- R15 v2.4: new PDF + updated paper.yaml
- R16 v1.6: new PDF + updated paper.yaml
- R17 v1.2: new PDF + updated paper.yaml
- R18 v1.1: new PDF + updated paper.yaml
- PRISM v1.1: new PDF + updated paper.yaml (DOI 10.5281/zenodo.19555265)

---

## Dependency Chain

```
Phase 0 (robustness fix)
  -> Phase 1 (paper updates)
    -> Phase 2 (metadata updates)
      -> Phase 3 (website/llms.txt)
      -> Phase 4 (article/post audit)
      -> Phase 5 (dataset uploads)
```

Phase 3, 4, 5 can run in parallel after Phase 2 completes.
