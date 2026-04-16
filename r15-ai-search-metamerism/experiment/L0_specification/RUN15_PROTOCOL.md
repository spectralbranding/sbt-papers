# Run 15: Synthetic Cohort Differentiation Protocol

**Date**: 2026-04-16
**Paper**: R15 — Spectral Metamerism in AI-Mediated Brand Perception (Zharnikov, 2026v)
**Precedent**: Ghasemi, Astvansh & Sepehri (2026), JAMS Study 5

---

## Methodology Selection: Why Behavioral Vignettes

Three approaches were evaluated for synthetic cohort construction:

1. **Trait-label embedding** (Ghasemi et al. 2026). Fast and simple. Risk: keywords prime dimension weights directly. "Sustainability-conscious" maps to Ideological, "status-oriented" maps to Semiotic/Social. Observed differentiation may reflect prompt vocabulary, not simulated observer perspective.

2. **Purchase history anchoring.** Model infers profile from behavioral records. Risk: brand overlap contamination requires separate stimulus set.

3. **Behavioral vignettes** (selected). Each cohort defined by 3-5 sentence description of behaviors, habits, and life context. No SBT dimension name or synonym appears in vignette text. Model must infer perceptual profile from described behavior.

### Why Vignettes Were Selected
- **Eliminates semantic priming**: no dimension name or close synonym in persona definition
- **Ecological validity**: real people are defined by behavior, not trait labels
- **Instrument stress test**: PRISM-B must translate behavior into dimensional weights
- **Stronger falsifiability**: if PRISM-B fails to differentiate behaviorally distinct vignettes, the instrument lacks sensitivity

### Design Safeguards
- **Dimension-order robustness check**: 50 calls with scrambled dimension order. If Spearman rho > .90 between fixed and randomized, dimension ordering does not confound results.
- **Two-stage prompt separation**: behavioral vignette in system prompt, PRISM-B evaluation in user prompt.

---

## Pre-Registered Hypotheses

- **H1**: Synthetic cohorts with different trait profiles produce significantly different spectral profiles for the same brand (ANOVA on DCI, p < .05)
- **H2**: Trait-profile similarity predicts spectral-profile similarity (Mantel test, r > .30)
- **H3**: Dimension-specific sensitivity: cohorts whose vignettes imply a particular dimension weight that dimension higher (C1 -> Ideological, C2 -> Semiotic, C3 -> Economic) without any dimension name appearing in the vignette

---

## Design

- 10 synthetic cohort profiles (behavioral vignettes, see below)
- 5 canonical brands: Hermes, IKEA, Patagonia, Erewhon, Tesla
- 5 LLM providers: Claude (claude-haiku-4-5), GPT (gpt-4o-mini), Gemini (gemini-2.5-flash), DeepSeek (deepseek-chat), Ollama (qwen3:30b)
- 3 repetitions per cell
- Total: 10 x 5 x 5 x 3 = 750 main + 50 robustness = **800 API calls**
- Temperature: .7 for all models
- Random seed: 42

---

## Cohort Profiles

| ID | Name | Implied Dims | Key Behaviors |
|----|------|-------------|---------------|
| C1 | Green Advocate | Ideological, Narrative | Cycles to work, food co-op volunteer, checks certifications |
| C2 | Taste Curator | Semiotic, Social | Gallery district, members-only dining, three tailors |
| C3 | Spreadsheet Shopper | Economic, Experiential | Per-unit cost tracking, teardown reviews, benchmark scores |
| C4 | Feed Native | Social, Semiotic | Unboxing videos, micro-trends, color palette folders |
| C5 | Long Habit | Temporal, Cultural | Same cafe 22 years, resoled shoes twice, handwritten ledger |
| C6 | Collective Organizer | Social, Cultural | Sunday dinners, building potluck, birthday calendar |
| C7 | Experience Collector | Experiential, Narrative | Flights to unknown cities, journal per trip, glassblowing course |
| C8 | Decade Planner | Economic, Temporal | 10-year cost of ownership, maintenance log, 40-year manufacturers |
| C9 | Deep Reader | Narrative, Ideological | Annotates margins, letters to editors, personal reference library |
| C10 | Spec Evaluator | Experiential, Semiotic | Technical documentation, benchmark tests, disassembles devices |

---

## Analysis Plan

1. Parse JSONL, normalize weights to sum to 1
2. Compute per-cohort mean spectral profiles (10 x 8)
3. ANOVA: cohort as factor, per-dimension weight as DV (8 separate ANOVAs)
4. Effect sizes: eta-squared for each dimension
5. Mantel test: trait-profile distance matrix vs spectral-profile distance matrix
6. Cosine similarity matrix across all 10 cohorts
7. H3 targeted tests: compare specific dimension weights for predicted cohorts
8. Robustness check: Spearman rho between fixed and randomized dimension-order results

---

## Success Criteria

- H1: at least 4/8 dimensions show significant cohort effects (p < .05)
- H2: Mantel r > .30
- H3: at least 2/3 predictions confirmed

---

## Exclusion Criteria

- API errors: recorded with error field, excluded from analysis
- Weights not summing to 100 (+/-5): renormalized and flagged
- Unparseable JSON: recorded as error, excluded
