## Pre-Registration Protocol

### Hypotheses
H1: Brands with high statistical similarity (BMI > 0.5) will show low discrimination rates
    under the statistical-only condition across all LLM families.
H2: Specification-augmented condition will significantly improve discrimination rates
    (Fisher's exact p < 0.05, Cohen's h > 0.3).
H3: Cross-model variance in brand recommendations will be lower in the augmented condition
    than the statistical condition (F-test p < 0.05).
H4: The metamerism-discrimination relationship will replicate across Western and Chinese
    model clusters (no significant cluster x condition interaction).

### Stopping Rules
- Minimum: 3 runs per condition per model (established before data collection)
- If Fisher's exact p > 0.10 after 3 runs: extend to 5 runs
- If Fisher's exact p > 0.10 after 5 runs: report null result

### Analysis Plan
- Primary: Fisher's exact test on discrimination rates (statistical vs augmented)
- Secondary: Wilcoxon signed-rank on confidence scores, F-test on variance
- Effect sizes: Cohen's h (discrimination), Cohen's d (confidence), Cramer's V (association)
- Exploratory: Per-model and per-cluster analysis, inter-model agreement

### Exclusion Criteria
- API errors resulting in unparseable responses are recorded as {can_distinguish: false, confidence: 0.5}
  and flagged in the session log
- Models with >50% error rate in any condition are excluded from aggregate statistics
  but reported separately
