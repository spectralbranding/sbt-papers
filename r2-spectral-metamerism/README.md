[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# Spectral Metamerism in Brand Perception: Projection Bounds from High-Dimensional Geometry

Working Paper v1.5.0 — March 2026

Author: Dmitry Zharnikov (ORCID [0009-0000-6893-9231](https://orcid.org/0009-0000-6893-9231))

DOI: [10.5281/zenodo.18945352](https://doi.org/10.5281/zenodo.18945352)

## 1 | Getting Started

This mirror contains the source manuscript (`paper.md`), the structured paper specification (`paper.yaml`), and machine-readable metadata (`CITATION.cff`, `CONTRIBUTORS.yaml`, `DATA_MANIFEST.yaml`, `PROVENANCE.yaml`). The paper is a theory contribution: it proves geometric and information-theoretic bounds on scalar brand grades. No environment setup is required to read the manuscript.

## 2 | Project Layout

```
r2-spectral-metamerism/
├── README.md            # this file
├── CITATION.cff         # machine-readable citation
├── paper.md             # source manuscript
├── paper.yaml           # structured paper spec (claims / dependencies / acceptance)
├── CONTRIBUTORS.yaml    # contributor record
├── DATA_MANIFEST.yaml   # data declarations
├── PROVENANCE.yaml      # provenance record
└── .here                # project anchor (relative-path resolution)
```

## 3 | Dependencies

No runtime dependencies for reading the manuscript. The Monte Carlo verification referenced in the paper (Section MC1) is implemented in the companion `R2_R3_computations.py` script shipped with the companion paper R3 mirror (`r3-warped-product-manifolds/`). To reproduce that simulation independently: Python 3.12 + `numpy`.

## 4 | Citation

Verbatim citation string:

> Zharnikov, D. (2026). *Spectral Metamerism in Brand Perception: Projection Bounds from High-Dimensional Geometry* (Working Paper v1.5.0). Zenodo. https://doi.org/10.5281/zenodo.18945352

Machine-readable form: see `CITATION.cff`. GitHub and Zenodo both render the "Cite this repository" widget directly from that file.

## 5 | Licence

- Code (scripts, configs, computational artifacts): MIT License — see `LICENSE`
- Data, figures, tables, manuscript prose: Creative Commons Attribution 4.0 International (CC BY 4.0) — see `LICENSE-data`

The two licences are tracked as separate files; the README declaration above is informational only.

---

*Last updated: 2026-05-29*
