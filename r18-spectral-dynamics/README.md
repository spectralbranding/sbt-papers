[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](../LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](../LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# Spectral Dynamics: Velocity, Acceleration, and Phase Space in Multi-Dimensional Brand Perception

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

## Data

This paper uses Dove profiles from Zharnikov (2026p, Table 1). No new data collection. Source: `../r10-dove-case-study/`

## License

CC-BY-4.0

---

## 1 | Paper

See [paper.md](paper.md).

- **Version**: 1.3.0
- **DOI**: [10.5281/zenodo.19468204](https://doi.org/10.5281/zenodo.19468204)

## 2 | Companion Data

No companion dataset for this paper. Illustrative Dove profiles are sourced from Zharnikov (2026p, Table 1) in the sibling `../r10-dove-case-study/` directory.

## 3 | Reproduction

Companion computation scripts in [`code/`](code/) reproduce Tables 2-3 and Figure 2 from the paper using Python 3 standard library + numpy + matplotlib. See [`code/README.md`](code/README.md) for details.

```bash
cd code/
python3 compute_velocity_acceleration.py
python3 phase_portrait.py
```

## 4 | Citation

```bibtex
@article{zharnikov2026z,
  author  = {Zharnikov, Dmitry},
  title   = {Spectral Dynamics: Velocity, Acceleration, and Phase Space in Multi-Dimensional Brand Perception},
  year    = {2026},
  doi     = {10.5281/zenodo.19468204},
  url     = {https://doi.org/10.5281/zenodo.19468204}
}
```

Machine-readable: [CITATION.cff](CITATION.cff).

## 5 | Licence

Code (if any): MIT — see hub-level [../LICENSE](../LICENSE). Data, figures, tables: CC BY 4.0 — see hub-level [../LICENSE-data](../LICENSE-data).

---

*Last updated: 2026-05-29*
