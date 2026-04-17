# R9: Non-Ergodic Brand Perception

**Paper**: Non-Ergodic Brand Perception: A Longitudinal Decomposition of Purpose Advertising Effectiveness

**Author**: Dmitry Zharnikov

**DOI**: [10.5281/zenodo.19138860](https://doi.org/10.5281/zenodo.19138860)

**Citation key**: 2026o

**Status**: Working paper v2.1

## Abstract

Brand tracking assumes cross-sectional averages (ensemble averages) yield the same information as individual trajectories over time (time averages) — an ergodicity assumption violated in brand perception. Drawing on Peters' (2019) framework from statistical physics, this paper identifies three structural sources of non-ergodicity: absorbing states from negative brand conviction, multiplicative signal dynamics, and path-dependent dimension weighting. Five formal propositions establish that signal order produces different perception profiles from identical signals; negative conviction functions as an absorbing state while positive conviction does not; cross-sectional tracking systematically overestimates brand health for absorption-risk brands; first signals anchor all subsequent updates in a dimension; and observer cohorts with different dimension weights produce divergent trajectories from identical signals. The paper specifies sufficient conditions for multiplicative perception updates and shows these conditions are empirically testable via longitudinal panel data. These propositions unify 80 years of scattered evidence on order effects, primacy, and belief updating within Spectral Brand Theory's eight-dimensional perception framework. The measurement implication is concrete: ensemble averages systematically misrepresent individual trajectories, and the bias direction and magnitude are predictable from brand coherence.

## Repository Contents

| File | Description |
|------|-------------|
| `paper.md` | Full paper (v2.1, 5 propositions, empirical anchor from R15) |
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
