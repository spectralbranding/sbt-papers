[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# Specification Impossibility in Organizational Design: A High-Dimensional Geometric Analysis

**Author**: Dmitry Zharnikov (ORCID: [0009-0000-6893-9231](https://orcid.org/0009-0000-6893-9231))
**DOI**: [10.5281/zenodo.18945591](https://doi.org/10.5281/zenodo.18945591)
**Version**: 1.1.0

---

## 1 | Getting Started

This mirror contains the paper source (`paper.md`), structured metadata (`paper.yaml`), citation file (`CITATION.cff`), and the companion computation script under `code/`. The paper is analytical; no simulation or empirical data is required.

To verify the numerical results in the paper, you need Python 3.10+ with the standard library only (no external dependencies). See section 3.

## 2 | Project Layout

```
r5-specification-impossibility/
├── README.md                  # this file
├── CITATION.cff               # machine-readable citation
├── paper.md                   # paper source
├── paper.yaml                 # structured paper spec (claims, dependencies, results)
├── CONTRIBUTORS.yaml          # contributor roles
├── DATA_MANIFEST.yaml         # data inventory (none for this paper)
├── PROVENANCE.yaml            # build provenance
└── code/
    └── r5_specification_impossibility.py   # companion computation script
```

## 3 | Quick Start

Run the companion computation script to reproduce the numerical values cited in the paper (V_48(0.1), d_eff at gamma=0.5, Shannon entropy, fork subspace dimensions, comparison table):

```bash
cd code
python r5_specification_impossibility.py
```

The script prints all numerical results referenced in Theorem 1, Proposition 1, Theorem 2, Theorem 3, and the information-theoretic analysis (R1). See script docstring for the exact run command and expected output.

## 4 | Dependencies

- Python 3.10+
- Standard library only (`math`); no external packages required

No `pyproject.toml` is needed for a stdlib-only script. The paper itself has no build-time dependencies beyond a Markdown viewer.

## 5 | Script Map

| Script | Purpose | Outputs |
|---|---|---|
| `code/r5_specification_impossibility.py` | Verify all numerical claims in T1, P1, T2, T3, R1 | Console output: V_48(0.1), d_eff(gamma), entropy bits, comparison table |

## 6 | Citation

Zharnikov, D. (2026). *Specification Impossibility in Organizational Design: A High-Dimensional Geometric Analysis*. Working Paper. DOI: [10.5281/zenodo.18945591](https://doi.org/10.5281/zenodo.18945591).

Machine-readable citation: see `CITATION.cff`. GitHub and Zenodo both render this natively via the "Cite this repository" button.

## 7 | Licence

- **Code** (companion script, configs): MIT License — see [`LICENSE`](LICENSE)
- **Data, paper text, figures, tables**: Creative Commons Attribution 4.0 International (CC BY 4.0) — see [`LICENSE-data`](LICENSE-data)

---

*Last updated: 2026-05-29*
