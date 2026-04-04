## Pre-Registration Protocol

### Study
R15: Spectral Metamerism in AI-Mediated Brand Perception
Paper: Zharnikov (2026v), target JAR special call on AI + search

### Measurement Design (v2)
All dimensional measures are elicited via structured JSON prompts -- no
keyword extraction from free text. Three prompt types:
  1. Weighted Recommendation: 100 importance points allocated across 8 dims
  2. Dimensional Differentiation: 0-10 score for each dim for a brand pair
  3. Dimension Probe: 0-10 score for a single brand on a single dim

### Hypotheses

H1 (Dimensional over-weighting): LLMs will allocate significantly more weight
    to Economic and Semiotic dimensions than the uniform baseline (12.5 each).
    Test: one-sample t-test on Economic+Semiotic weight sum vs baseline 25.0.

H2 (Convergent collapse): Dimensional weight profiles will be highly similar
    across model families (mean cosine similarity >= 0.85 across model pairs),
    indicating that the collapse pattern is systematic rather than model-specific.

H3 (Differential probe variance): Cross-model variance in dimension-specific probe
    scores will be significantly lower for Economic and Semiotic dimensions than for
    Narrative, Cultural, and Temporal dimensions (t-test on variance, p < 0.05).

H4 (Differentiation gap): For brand pairs whose primary differentiators are soft
    dimensions (Narrative, Ideological, Cultural, Temporal), models will assign
    lower differentiation scores on those soft dimensions than on hard dimensions
    for the same pairs -- despite the pairs being designed to differ maximally on
    soft dimensions.

### Stopping Rules
- Minimum: 3 runs per prompt per model (established before data collection)
- If H1 t-test p > 0.10 after 3 runs: extend to 5 runs
- If H1 t-test p > 0.10 after 5 runs: report null result with power analysis

### Analysis Plan
Primary:
  - Dimensional weight profiles per model (from weighted_recommendation prompts)
  - One-sample t-test: Economic + Semiotic weight sum vs uniform baseline 25.0

Secondary:
  - Cosine similarity matrix across model weight profiles (H2)
  - t-test on cross-model probe score variance (hard vs soft dims) (H3)
  - Differentiation gap: soft-dim scores vs hard-dim scores for soft-designed pairs (H4)

Exploratory:
  - Per-brand-pair DCI vs human-judged spectral distance
  - Western vs Chinese vs local model cluster comparison

### Exclusion Criteria
- API errors resulting in unparseable responses: recorded with error field in JSONL
- Models with >50% error rate in any prompt type: excluded from aggregate statistics
- Weights that do not sum to 100 (+/-5 tolerance): recorded and flagged, included if
  ratable by renormalization
- Dimension probe responses where score cannot be parsed as 0-10 numeric: null
