# The Rendering Problem: From Genetic Expression to Brand Perception

[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](../LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](../LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

Working Paper — Dmitry Zharnikov (ORCID: [0009-0000-6893-9231](https://orcid.org/0009-0000-6893-9231))

DOI: [10.5281/zenodo.19064426](https://doi.org/10.5281/zenodo.19064426)

## 1 | Getting Started

This directory is the public mirror of the paper "The Rendering Problem: From Genetic Expression to Brand Perception". The canonical artifacts are:

- `paper.md` — full manuscript
- `paper.yaml` — structured paper spec (claims, methodology, acceptance criteria, dependencies)
- `CITATION.cff` — machine-readable citation
- `CONTRIBUTORS.yaml` — contributor metadata
- `DATA_MANIFEST.yaml` — data declaration
- `PROVENANCE.yaml` — provenance trail

Repository-level license files (MIT for code, CC BY 4.0 for data) live at the parent `sbt-papers/` root.

## 2 | Project Layout

```
rendering-problem/
├── README.md            # this file
├── .here                # project anchor for relative-path resolution
├── paper.md             # full manuscript
├── paper.yaml           # structured paper spec
├── CITATION.cff         # machine-readable citation
├── CONTRIBUTORS.yaml    # contributor metadata
├── DATA_MANIFEST.yaml   # data declaration
└── PROVENANCE.yaml      # provenance trail
```

## 3 | Quick Start

This paper is purely theoretical. No computational pipeline accompanies the manuscript; per `paper.yaml`, `code.available: false`. To read the paper, open `paper.md`. To cite, see Section 6 below or use `CITATION.cff` directly.

## 4 | Dependencies

No software dependencies. Conceptual dependencies are declared in `paper.yaml` under `dependencies:` and include the SBT and OST corpus anchors plus the biological, systems-theory, and non-ergodic-dynamics references named in the manuscript.

## 5 | Script Map

Not applicable — no scripts ship with this paper.

## 6 | Citation

Zharnikov, D. (2026). The Rendering Problem: From Genetic Expression to Brand Perception. Working Paper. DOI: [10.5281/zenodo.19064426](https://doi.org/10.5281/zenodo.19064426).

Machine-readable citation metadata is in `CITATION.cff`. GitHub and Zenodo both render this file natively; use the "Cite this repository" button on GitHub for formatted citations in 12+ formats.

## 7 | Licence

- **Code**: MIT License — see [`LICENSE`](../LICENSE) at the repository root.
- **Data, figures, tables, manuscript text**: Creative Commons Attribution 4.0 International (CC BY 4.0) — see [`LICENSE-data`](../LICENSE-data) at the repository root.

---

*Last updated: 2026-05-29*
