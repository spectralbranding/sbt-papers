[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# Non-ergodic brand perception: Diffusion dynamics on multi-dimensional perceptual manifolds

**Author**: Dmitry Zharnikov (ORCID: [0009-0000-6893-9231](https://orcid.org/0009-0000-6893-9231))
**DOI**: [10.5281/zenodo.18945659](https://doi.org/10.5281/zenodo.18945659)

## 1 | Getting Started

This mirror holds the manuscript, supporting numerical-illustration code, and figures for R6. The paper is theoretical (Ito calculus on Riemannian manifolds, spectral theory of diffusion generators, first-passage time analysis); the `code/` directory contains the Python script that produces the published figures.

Clone the repository and ensure Python 3.10+ is available with `numpy`, `scipy`, and `matplotlib`.

## 2 | Project Layout

```
r6-diffusion-dynamics/
├── paper.md                 # Manuscript (working paper v1.2.0)
├── paper.yaml               # Paper spec (claims, methodology, dependencies)
├── CITATION.cff             # Machine-readable citation
├── CONTRIBUTORS.yaml        # Contributor record
├── DATA_MANIFEST.yaml       # Data manifest
├── PROVENANCE.yaml          # Provenance record
├── code/
│   ├── r6_diffusion_dynamics.py
│   └── figures/
├── figures/
│   ├── r6_phase_diagram.png
│   └── r6_survival_curves.png
├── LICENSE                  # MIT (code)
├── LICENSE-data             # CC BY 4.0 (data + figures + tables)
└── README.md                # This file
```

## 3 | Quick Start

Run the numerical-illustration script to regenerate the published figures:

```bash
cd code
python r6_diffusion_dynamics.py
```

Outputs are written to `code/figures/` and mirrored to `figures/` at the mirror root.

## 4 | Dependencies

- Python 3.10+
- numpy
- scipy
- matplotlib

All analytical results (Theorems T1-T4) are proof-based and require no software. The numerical illustration for Proposition P7 (D/A Goldilocks derivation) uses the SBT baseline calibration values; no fitting to data is performed.

## 5 | Citation

If you use this work, please cite it as:

> Zharnikov, D. (2026). Non-ergodic brand perception: Diffusion dynamics on multi-dimensional perceptual manifolds. Zenodo. https://doi.org/10.5281/zenodo.18945659

Machine-readable citation metadata is available in [`CITATION.cff`](CITATION.cff). GitHub and Zenodo both render `CITATION.cff` natively (click "Cite this repository").

## 6 | Licence

- **Code** (scripts, configs, computational artifacts): [MIT License](LICENSE)
- **Data** (datasets, figures, tables, generated artifacts): [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-data)

---

*Last updated: 2026-05-29*
