# Dimension Robustness Analysis (Section 8A)

Empirical stress-test of SBT's eight-dimension framework, reported in Section 8A of the paper.

## Data Source

R15 Run 5 weight profiles (Zharnikov, 2026v): 22 LLMs, 8 brand pairs, 3 repetitions per pair per model, 11,298 API calls. Source data in the [R15 experiment directory](https://github.com/spectralbranding/sbt-papers/tree/main/r15-ai-search-metamerism/experiment).

## Files

- `gap5_dimension_robustness.py` -- Analysis script (Python 3.12, scipy, numpy)
- `gap5_dimension_robustness_results.json` -- Full structured results

## Experiments

1. **Drop-one (8D to 7D)**: Remove each dimension, recompute DCI, measure rank stability
2. **Drop-pair (8D to 6D)**: Remove all 28 dimension pairs, measure rank stability
3. **Augmented (8D to 10D)**: Split Experiential and Economic into sub-dimensions
4. **Variance decomposition**: Per-dimension share of cross-model variance
5. **Profile shape stability**: Mean pairwise cosine under dimension removal

## Key Results

- All drop-one cosines > .994 (N = 22 models)
- All drop-pair cosines > .993 (N = 27 computable pairs)
- Augmented 10D: rho = .9997 (no added discriminative power)
- All 8 dimensions carry 5.4-18.7% of cross-model variance

## Reproduction

```bash
python gap5_dimension_robustness.py
```

Requires R15 Run 5 JSONL data in the expected path. Outputs to stdout and writes `gap5_dimension_robustness_results.json`.
