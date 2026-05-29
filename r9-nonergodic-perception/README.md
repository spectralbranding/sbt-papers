[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](../LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](../LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# R9: Non-Ergodic Brand Perception

**Paper**: From Order Effects to Absorbing States: A Non-Ergodic Framework for Multi-Dimensional Brand Perception Dynamics

**Author**: Dmitry Zharnikov

**DOI**: [10.5281/zenodo.19138860](https://doi.org/10.5281/zenodo.19138860)

**Citation key**: 2026o

**Status**: Working paper v2.2

## Abstract

Brand tracking assumes cross-sectional averages (ensemble averages) yield the same information as individual trajectories over time (time averages) — an ergodicity assumption violated in brand perception. Drawing on Peters' (2019) framework from statistical physics, this paper identifies three structural sources of non-ergodicity: absorbing states from negative brand conviction, multiplicative signal dynamics, and path-dependent dimension weighting. Five formal propositions establish that signal order produces different perception profiles from identical signals; negative conviction functions as an absorbing state while positive conviction does not; cross-sectional tracking systematically overestimates brand health for absorption-risk brands; first signals anchor all subsequent updates in a dimension; and observer cohorts with different dimension weights produce divergent trajectories from identical signals. The paper specifies sufficient conditions for multiplicative perception updates and shows these conditions are empirically testable via longitudinal panel data. These propositions unify 80 years of scattered evidence on order effects, primacy, and belief updating within Spectral Brand Theory's eight-dimensional perception framework. The measurement implication is concrete: ensemble averages systematically misrepresent individual trajectories, and the bias direction and magnitude are predictable from brand coherence.

## Repository Contents

| File | Description |
|------|-------------|
| `paper.md` | Full paper (v2.2, 5 propositions, 37 refs, new §3.4 boundary conditions, §6.5 JCP implications) |
| `paper.yaml` | Paper specification (machine-readable claims, submission history) |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTORS.yaml` | Contributor attribution (human + AI) |
| `PROVENANCE.yaml` | Version history and submission records |
| `DATA_MANIFEST.yaml` | Data sources and external dependencies |

## Key Concepts

- **Non-Ergodicity**: Why population averages (ensemble averages) systematically differ from individual trajectories (time averages)
- **Absorbing States**: Negative brand conviction from which recovery is structurally improbable
- **Multiplicative Signal Dynamics**: Brand signals interact with existing perception rather than adding to a blank slate
- **Path-Dependent Dimension Weighting**: Different cohort weight vectors produce divergent trajectories from identical signal sequences
- **Empirical Anchor**: R15 dataset (21,601 API calls, 24 LLMs) corroborates cohort divergence findings

## Data

This paper uses the R15 empirical dataset as an anchor (Zharnikov 2026v, 21,601 API calls). Case study uses Dove/Unilever public financial filings and academic perception studies cited in DATA_MANIFEST.yaml.

## License

CC-BY-4.0

---

## 1 | Getting Started

This paper-slug directory lives inside the `sbt-papers` hub repository. Clone the hub and `cd` into this slug:

```bash
git clone https://github.com/spectralbranding/sbt-papers.git
cd sbt-papers/r9-nonergodic-perception
```

Environment setup (Python 3.12 + `uv`) is anchored at the hub root. See hub-level `pyproject.toml` and `reproduce.sh`.

## 2 | Project Layout

```
r9-nonergodic-perception/
├── README.md                  # this file
├── paper.md                   # full paper (v2.3)
├── paper.yaml                 # machine-readable paper spec
├── CITATION.cff               # citation metadata
├── CONTRIBUTORS.yaml          # contributor attribution
├── PROVENANCE.yaml            # version + submission history
├── DATA_MANIFEST.yaml         # data sources
└── code/
    └── simulate_absorption.py # companion computation script (Tables 2, 3)
```

No companion dataset for this paper. R15 empirical dataset is referenced as an external anchor only — see DATA_MANIFEST.yaml.

## 3 | Quick Start

Reproduce Tables 2 and 3 (discrete-time absorbing Markov chain simulation, seed 42, 1000 observers, 6 periods):

```bash
cd code
uv run python simulate_absorption.py
```

Hub-level reproduction (all slugs) is orchestrated from the hub root.

## 4 | Dependencies

- Python 3.12
- `numpy`

Pinned at the hub root `pyproject.toml`. Install with `uv sync` from hub root.

## 5 | Script Map

| Script | Reproduces |
|---|---|
| `code/simulate_absorption.py` | Table 2, Table 3 |

## 6 | Citation

Zharnikov, D. (2026). *From Order Effects to Absorbing States: A Non-Ergodic Framework for Multi-Dimensional Brand Perception Dynamics*. Working Paper v2.3. DOI: [10.5281/zenodo.19138860](https://doi.org/10.5281/zenodo.19138860).

Machine-readable citation: see `CITATION.cff` in this directory.

## 7 | Licence

Code (if any): MIT — see hub-level [../LICENSE](../LICENSE). Data, figures, tables: CC BY 4.0 — see hub-level [../LICENSE-data](../LICENSE-data).

*Last updated: 2026-05-29*
