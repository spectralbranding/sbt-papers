[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# How Many Brands Can a Market Hold? Sphere Packing Bounds for Multi-Dimensional Positioning

Public mirror for the R4 paper by Dmitry Zharnikov (2026g). This repository hosts the paper source, machine-readable citation metadata, and licensing files. Results in this paper are analytical; the companion computation script `r4_capacity_bounds.py` (referenced in Appendix A of the paper) lives in the paper's working repository and is published alongside the Zenodo upload.

## 1 | Getting Started

This is a paper-only mirror. No build step is required to read the paper.

- Read `paper.md` for the full manuscript.
- Read `paper.yaml` for the structured paper specification (claims, methodology, dependencies, results).
- Read `CITATION.cff` for machine-readable citation metadata (rendered automatically by GitHub and Zenodo).

## 2 | Project Layout

```
r4-sphere-packing/
├── README.md              # this file
├── LICENSE                # MIT (code)
├── LICENSE-data           # CC BY 4.0 (data, figures, tables)
├── CITATION.cff           # machine-readable citation metadata
├── paper.md               # full manuscript
├── paper.yaml             # structured paper specification
├── CONTRIBUTORS.yaml      # contributor metadata
├── DATA_MANIFEST.yaml     # data inventory
├── PROVENANCE.yaml        # provenance metadata
├── experiment/            # LLM stability experiment (Section 10.5)
│   ├── L0_specification/
│   ├── L2_prompts/
│   ├── L3_sessions/
│   ├── L4_analysis/
│   ├── hf_dataset/
│   └── requirements.txt
└── .here                  # project root anchor
```

## 3 | Quick Start

This paper's main results are analytical (volume-ratio capacity bounds, E_8 kissing-number decomposition, white-space fraction, correlation-induced effective dimensionality). No simulation pipeline is required to reproduce them — the bounds follow from closed-form expressions given the perceptual threshold parameter epsilon.

The Section 10.5 LLM competitive-interference experiment (250 calls, five models) is documented under `experiment/`. See `experiment/requirements.txt` for the Python environment used for that single subsection.

## 4 | Dependencies

- For reading: any Markdown or PDF viewer.
- For the Section 10.5 experiment: see `experiment/requirements.txt`.

## 5 | Citation

If you use this paper, please cite it as:

> Zharnikov, D. (2026). How many brands can a market hold? Sphere packing bounds for multi-dimensional positioning. Zenodo. https://doi.org/10.5281/zenodo.18945522

Machine-readable citation metadata: see `CITATION.cff` (rendered by GitHub via the "Cite this repository" button).

- DOI: [10.5281/zenodo.18945522](https://doi.org/10.5281/zenodo.18945522)
- ORCID: [0009-0000-6893-9231](https://orcid.org/0009-0000-6893-9231)

## 6 | Licence

- Code: MIT — see `LICENSE`
- Data, figures, tables, and other generated artifacts: CC BY 4.0 — see `LICENSE-data`

---

*Last updated: 2026-05-29*
