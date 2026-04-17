# R18: Spectral Dynamics

**Paper**: Spectral Dynamics: Velocity, Acceleration, and Phase Space in Multi-Dimensional Brand Perception

**Author**: Dmitry Zharnikov

**DOI**: [10.5281/zenodo.19468204](https://doi.org/10.5281/zenodo.19468204)

**Citation key**: 2026z

## Abstract

Brand measurement frameworks capture where a brand is positioned but not where it is going. This paper introduces a differential calculus for multi-dimensional brand perception, extending Spectral Brand Theory's eight-dimensional measurement space from static profiles (Order 0) to velocity vectors (Order 1) and acceleration vectors (Order 2). Three contributions emerge: (1) velocity resolves metric ambiguity --- brands with identical spectral profiles but different velocities are distinguishable in phase space, analogous to the Bonnet pair problem in differential geometry; (2) a directional coherence metric quantifies alignment between a brand's actual trajectory and its strategic intent; (3) trajectory clustering segments brands by dynamic behavior rather than static position, enabling detection of competitive convergence before it manifests in position. The framework is illustrated using Dove's 20-year brand evolution (2003--2023). The differential calculus connects naturally to Kalman filter estimation, embedding existing state-space approaches in marketing science within a unified kinematic theory for brand perception.

## Repository Contents

| File | Description |
|------|-------------|
| `paper.md` | Full paper (v1.1, ~7,500 words, 3 propositions, 1 theorem, 29 references) |
| `paper.pdf` | PDF export (267K, 20 pages) |
| `paper.yaml` | Paper specification (machine-readable claims) |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTORS.yaml` | Contributor attribution (human + AI) |
| `PROVENANCE.yaml` | Version history and submission timeline |
| `DATA_MANIFEST.yaml` | Data sources and reproducibility steps |

## Key Concepts

- **Brand Velocity**: First time derivative of the spectral profile --- direction and speed of brand movement per dimension
- **Brand Acceleration**: Second derivative --- whether movement is intensifying, stabilizing, or reversing
- **Phase Space**: 16-dimensional state (position + velocity) that disambiguates brands with identical profiles but different trajectories
- **Directional Coherence**: Cosine similarity between velocity and strategy vectors --- measures strategy-trajectory alignment
- **Trajectory Clustering**: Segmenting brands by dynamic behavior rather than static position

## Target Venue

Journal of Marketing Research (measurement methodology). Fallback: IJRM.

## Data

This paper uses Dove profiles from Zharnikov (2026p, Table 1). No new data collection. Source: `../r10-dove-case-study/`

## License

CC-BY-4.0
