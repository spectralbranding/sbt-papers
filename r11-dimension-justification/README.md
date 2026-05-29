[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](../LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](../LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# Why eight? Completeness and necessity of the SBT dimensional taxonomy

Theoretical justification of the 8-dimensional SBT taxonomy via non-redundancy, minimal completeness, and concentration-of-measure resolution of low-dimensional MDS results.

## 1 | Paper

- [paper.md](paper.md)
- Version: v1.3
- DOI: [10.5281/zenodo.19207599](https://doi.org/10.5281/zenodo.19207599)

## 2 | Companion Data

No companion dataset for this paper. Section 8A reanalyzes R15 Run 5 LLM weight profiles; raw R15 data lives at the R15 slug. Derived results stored at [robustness-analysis/gap5_dimension_robustness_results.json](robustness-analysis/gap5_dimension_robustness_results.json).

## 3 | Reproduction

This slug ships two scripts:

- [code/dimension_volatility.py](code/dimension_volatility.py) — companion computation script for Section 8A DCI volatility analysis (methodology template; requires R15 Run 5 weight profiles as input).
- [robustness-analysis/gap5_dimension_robustness.py](robustness-analysis/gap5_dimension_robustness.py) — full reproducible pipeline for Tables 1-4 of Section 8A (drop-one, drop-pair, augmented 10D experiments).

Run individually with Python 3.12 (scipy, numpy). The hub orchestrator at [../reproduce.sh](../reproduce.sh) iterates all slugs.

## 4 | Citation

```bibtex
@misc{zharnikov2026r,
  author = {Zharnikov, Dmitry},
  title  = {Why eight? Completeness and necessity of the SBT dimensional taxonomy},
  year   = {2026},
  doi    = {10.5281/zenodo.19207599}
}
```

Machine-readable: [CITATION.cff](CITATION.cff).

## 5 | Licence

Code (if any): MIT — see hub-level [../LICENSE](../LICENSE). Data, figures, tables: CC BY 4.0 — see hub-level [../LICENSE-data](../LICENSE-data).

*Last updated: 2026-05-29*
