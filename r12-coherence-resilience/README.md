[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](../LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](../LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# Coherence Type Over Coherence Score: A Stochastic Differential Equation Derivation of Brand Resilience

Companion mirror for Zharnikov (2026) R12 — formal SDE derivation of the coherence-type-over-coherence-score principle in Spectral Brand Theory.

---

## 1 | Paper

- Manuscript: [paper.md](paper.md)
- Version: 1.2
- DOI: [10.5281/zenodo.19208107](https://doi.org/10.5281/zenodo.19208107)
- Spec: [paper.yaml](paper.yaml)

## 2 | Companion Data

No companion dataset for this paper. Numerical illustrations are produced by the companion computation scripts (Section 3) and stored under `code/data/`.

## 3 | Reproduction

Companion computation scripts live in [`code/`](code/):

- `coherence_resilience_computations.py` — closed-form absorption probability and recovery-time computations for the five coherence types.
- `coherence_resilience_mc.py` — Monte Carlo simulation of the SDE on S^7_+ for validation against the closed-form ordering.

Run from the slug root:

```bash
python code/coherence_resilience_computations.py
python code/coherence_resilience_mc.py
```

Outputs land in `code/data/` (`results.json`, `run.log`). Hub-level orchestrator: [../reproduce.sh](../reproduce.sh) iterates all slugs.

## 4 | Citation

```bibtex
@article{zharnikov2026r12,
  author  = {Zharnikov, Dmitry},
  title   = {Coherence Type Over Coherence Score: A Stochastic Differential Equation Derivation of Brand Resilience},
  year    = {2026},
  version = {1.2},
  doi     = {10.5281/zenodo.19208107},
  url     = {https://doi.org/10.5281/zenodo.19208107}
}
```

Machine-readable: [CITATION.cff](CITATION.cff).

## 5 | Licence

Code (if any): MIT — see hub-level [../LICENSE](../LICENSE). Data, figures, tables: CC BY 4.0 — see hub-level [../LICENSE-data](../LICENSE-data).

---

*Last updated: 2026-05-29*
