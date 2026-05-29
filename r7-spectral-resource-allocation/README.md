[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# Spectral Resource Allocation: Demand-Driven Investment in Multi-Dimensional Brand Space

**Author**: Dmitry Zharnikov (ORCID: [0009-0000-6893-9231](https://orcid.org/0009-0000-6893-9231))
**DOI**: [10.5281/zenodo.19009268](https://doi.org/10.5281/zenodo.19009268)

---

## 1 | Getting Started

This repository hosts the public source for the paper "Spectral Resource Allocation: Demand-Driven Investment in Multi-Dimensional Brand Space" together with its companion computation script and generated figures. The paper is analytical; the script reproduces all numerical illustrations and figures in the manuscript.

Python 3.12 is required. The companion script uses standard scientific-Python packages (numpy, scipy, matplotlib).

## 2 | Project Layout

```
r7-spectral-resource-allocation/
├── README.md                  # this file
├── CITATION.cff               # machine-readable citation
├── LICENSE                    # MIT (code)
├── LICENSE-data               # CC BY 4.0 (data, figures, tables)
├── paper.md                   # manuscript
├── paper.yaml                 # paper spec (claims, dependencies, results)
├── CONTRIBUTORS.yaml
├── DATA_MANIFEST.yaml
├── PROVENANCE.yaml
├── .here                      # project root anchor
├── code/
│   └── r7_spectral_resource_allocation.py
└── figures/
    ├── r7_alignment_gap_simplex.png
    ├── r7_founder_vs_cohort_weights.png
    └── r7_theorem5_interaction_adjustment.png
```

## 3 | Quick Start

Run the companion computation script from the repository root:

```bash
python code/r7_spectral_resource_allocation.py
```

The script regenerates the figures in `figures/` from analytical formulas (Theorems 1-5). No external data inputs are required; all numerical examples derive from the canonical five-brand case studies and hypothetical cohort weight profiles described in the manuscript.

## 4 | Dependencies

- Python >= 3.12
- numpy
- scipy
- matplotlib

Install:

```bash
pip install numpy scipy matplotlib
```

## 5 | Citation

If you use this work, please cite:

> Zharnikov, D. (2026). Spectral Resource Allocation: Demand-Driven Investment in Multi-Dimensional Brand Space. Working Paper. DOI: [10.5281/zenodo.19009268](https://doi.org/10.5281/zenodo.19009268)

Machine-readable citation metadata: [`CITATION.cff`](CITATION.cff). GitHub and Zenodo both render this natively (click "Cite this repository" for 12+ citation formats).

## 6 | Licence

- **Code** (scripts under `code/`): MIT License — see [`LICENSE`](LICENSE)
- **Data, figures, tables, manuscript text**: Creative Commons Attribution 4.0 International (CC BY 4.0) — see [`LICENSE-data`](LICENSE-data)

---

*Last updated: 2026-05-29*
