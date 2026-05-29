[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# Geometric Necessity of Fuzzy Cohort Boundaries: A Concentration Analysis of the 7-Simplex

Public mirror for Zharnikov (2026f) R3. Concentration-of-measure analysis on the probability simplex $\Delta^7$ establishing that, under the uniform Dirichlet null, a majority of observer-weight profiles lie within 10% relative distance of any cohort boundary — making discrete cohort assignment geometrically unstable in 8-dimensional perception space.

## 1 | Getting Started

This mirror contains the paper source (`paper.md`), structured spec (`paper.yaml`), machine-readable citation (`CITATION.cff`), and the Monte Carlo reproducibility script under `code/`. Python 3.12+ recommended; `uv` for environment management.

## 2 | Project Layout

```
r3-cohort-boundaries/
├── paper.md              # Manuscript source
├── paper.yaml            # Structured paper spec (claims, methodology, results)
├── CITATION.cff          # Machine-readable citation
├── CONTRIBUTORS.yaml     # Contributor record
├── DATA_MANIFEST.yaml    # Data manifest (no primary data; synthetic only)
├── PROVENANCE.yaml       # Provenance record
└── code/
    ├── r3_concentration_mc.py   # Monte Carlo: distance ratios + BVF
    └── README.md                # Per-script reproducibility notes
```

## 3 | Quick Start

Reproduce the numerical figures in Tables 2, 5, and 7:

```bash
uv run --with numpy --with scikit-learn python code/r3_concentration_mc.py
```

Random seed fixed at 42; output printed to stdout. See `code/README.md` for details.

## 4 | Dependencies

- Python 3.12+
- NumPy
- scikit-learn (k-means partition for boundary volume fraction)
- `uv` (recommended; handles dependency resolution per-invocation)

## 5 | Script Map

| Script | Produces |
|---|---|
| `code/r3_concentration_mc.py` | Table 2 (distance contrast ratio by dimension), Table 5 (boundary volume fraction at $n=8$, $k=4$), Table 7 (Euclidean vs Fisher-Rao contrast at $n=8$) |

## 6 | Citation

Zharnikov, D. (2026). Geometric necessity of fuzzy cohort boundaries: A concentration analysis of the 7-simplex. Zenodo. https://doi.org/10.5281/zenodo.18945477

DOI: [10.5281/zenodo.18945477](https://doi.org/10.5281/zenodo.18945477)

See `CITATION.cff` for machine-readable form (rendered by GitHub and Zenodo).

## 7 | Licence

- Code: MIT License (see `LICENSE` when present at repository root)
- Data, figures, tables, manuscript text: CC BY 4.0 (see `LICENSE-data` when present at repository root)

Dual-license discipline per `PUBLIC_MIRROR_STANDARD.md` v1.0.0.

---

*Last updated: 2026-05-29*
