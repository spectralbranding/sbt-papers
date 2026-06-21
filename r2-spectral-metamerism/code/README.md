# code/ — companion computation for R2 / 2026e

Companion script for *Spectral Metamerism: Brand Perception Under Projection* (R2). See the paper header for the concept DOI.

## Script map

| Script | Purpose | Run command | Outputs |
|--------|---------|-------------|---------|
| `R2_R3_computations.py` | Monte Carlo metameric-fraction computation reproducing Table 8 (fraction of brand pairs well-separated in 8D but indistinguishable under a random 1D projection). Exposes the random-projection generator the R3 paper (2026f) reuses for its concentration-of-measure tests. Random seed `42`. | `uv run --with numpy python R2_R3_computations.py` (or `python R2_R3_computations.py` if numpy present) | text report to stdout |

## Model (paper "Monte Carlo" section)

`N=50` brand profiles in `R^8_+` via component-wise log-normal (underlying normal `mu=0.5, sigma=0.5`); distances and the 1D projection are computed on the **log-profiles** ("Euclidean on log-profiles"). A pair is metameric iff `d_8D > 1.0` and `d_1D < 0.3` under a uniformly random unit projection direction.

## Reproduction status

The script does **not** hard-code any published value. Status:

- **MATCH (the paper's actual claim):** the metameric fraction is stable at **~31–39%**. The 2000-trial mean at `SEED=42` is **31.6%** (5th–95th pct 26.4%–37.6%), consistent with the stated band. Notably the first seed-42 trial reproduces Table 8's Trial 1 **exactly** (474 pairs, 38.7%), indicating the original computation used this seed.
- **Not bit-reproducible:** the specific per-trial counts for Trials 2 and 3 (388 / 31.7%, 374 / 30.5%) depend on the paper's unrecorded per-trial seeds. This is a reporting gap in the paper (seeds not stated), not a model discrepancy; the stable band the qualitative claim rests on reproduces.

## Publication-location note (for the author / main session)

The paper's prose points to this script in the shared `sbt-framework` repository (`https://github.com/spectralbranding/sbt-framework`). It was **absent there** at audit time. The author should decide whether the canonical home is `sbt-framework` (as the prose says) or the paper's own mirror `sbt-papers/r2-spectral-metamerism/code/` (the convention the rest of the corpus follows); register/mirror accordingly. This is a substrate/mirror task, not done here.

## Dependencies

`numpy`. No network access, no API keys, no data files.

---

*Drafted 2026-06-21 — fills the missing `R2_R3_computations.py` named in the paper's Monte Carlo section and Acknowledgments (code only; not yet mirrored/registered).*
