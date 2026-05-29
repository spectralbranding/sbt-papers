[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](../LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](../LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# Brand Triangulation: A Geometric Framework for Multi-Observer Brand Positioning

**Paper**: Brand Triangulation: A Geometric Framework for Multi-Observer Brand Positioning

**Author**: Dmitry Zharnikov

**DOI**: [10.5281/zenodo.19482547](https://doi.org/10.5281/zenodo.19482547)

**Citation key**: 2026y

## Abstract

Brand positioning research faces a fundamental measurement problem: every observer cohort perceives the same brand differently, yet traditional frameworks treat this variation as noise rather than signal. We propose brand triangulation --- a geometric framework that borrows from GPS positioning theory to estimate brand spectral profiles from multiple observer cohorts while jointly solving for observer bias. We make four contributions. First, we formalize the GPS-SBT mapping, showing that observer cohorts function as positioning satellites whose geometric diversity determines measurement precision. Second, we introduce Perception DOP (Dilution of Precision), a computable metric that quantifies how well a given set of observer cohorts can resolve a brand's eight-dimensional spectral profile --- before any data is collected. Third, we propose differential brand measurement, a calibration protocol using reference brands with known spectral profiles to correct systematic observer bias across studies. Fourth, we establish identifiability conditions: the minimum observer configurations required for unique brand positioning. We position the framework against existing Bayesian heterogeneity approaches, showing that the geometric formulation provides pre-study design criteria (PDOP) that probabilistic methods lack. We illustrate the framework computationally using dimensional weight data from six large language models (4,860 API calls across fifteen brand pairs), showing that Perception DOP is consistent with measurement quality patterns and that differential correction reduces cross-observer variance. The framework transforms multi-observer disagreement from a methodological nuisance into the primary source of positioning information.

## Repository Contents

| File | Description |
|------|-------------|
| `paper.md` | Full paper (v1.2, ~14,200 words, 6 propositions, 45 references) |
| `paper.pdf` | PDF export (304K) |
| `paper.yaml` | Paper specification (machine-readable claims) |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTORS.yaml` | Contributor attribution (human + AI) |
| `PROVENANCE.yaml` | Version history |
| `DATA_MANIFEST.yaml` | Data sources and computed quantities |

## Key Concepts

- **Perception DOP**: A computable metric (analogous to GPS Dilution of Precision) that quantifies how well a given set of observer cohorts can resolve a brand's 8D spectral profile
- **Differential Brand Measurement**: Calibration protocol using reference brands (Hermes, IKEA, Patagonia) to correct systematic observer bias
- **Tri-binding Admissibility**: Three simultaneous conditions (geometric, governance, temporal) for brand health
- **Perception Kalman Filter**: Dynamic tracking of 8D brand trajectories over time

## Data

This paper reanalyzes R15 experiment data (Runs 2-4: 4,860 API calls, 6 LLMs, 15 brand pairs — the subset used for the GPS-SBT illustration). No new data collection. Source data: `../r15-ai-search-metamerism/experiment/`

## License

CC-BY-4.0

---

## 1 | Paper

- Manuscript: [paper.md](paper.md)
- Version: 1.4.0
- DOI: [10.5281/zenodo.19482547](https://doi.org/10.5281/zenodo.19482547)

## 2 | Companion Data

No companion dataset for this paper. Numerical demonstrations reanalyze R15 data: see `../r15-ai-search-metamerism/experiment/`.

## 3 | Reproduction

Companion computation lives under `code/` and `simulation/`:

- `code/compute_pdop_rmse.py` — Figure 2 PDOP-vs-RMSE log-log scatter; outputs `code/pdop_rmse.csv` and `code/figure2_pdop_rmse.png`
- `simulation/` — Monte Carlo PDOP validation supporting §9.6
- `experiment/L0_specification/`, `experiment/L4_analysis/` — specification and analysis artifacts

Run the PDOP script directly with Python 3.12 (see script docstring for the canonical run command).

## 4 | Citation

```bibtex
@misc{zharnikov2026r17,
  author = {Zharnikov, Dmitry},
  title  = {Brand Triangulation: A Geometric Framework for Multi-Observer Brand Positioning},
  year   = {2026},
  doi    = {10.5281/zenodo.19482547}
}
```

Machine-readable: [CITATION.cff](CITATION.cff).

## 5 | Licence

Code (if any): MIT — see hub-level [../LICENSE](../LICENSE). Data, figures, tables: CC BY 4.0 — see hub-level [../LICENSE-data](../LICENSE-data).

*Last updated: 2026-05-29*
