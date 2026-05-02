# R9 Companion Computation Scripts

This directory contains the reproducibility scripts for paper R9: *From Order
Effects to Absorbing States: A Non-Ergodic Framework for Multi-Dimensional
Brand Perception Dynamics* (Zharnikov 2026o).

Paper DOI: `10.5281/zenodo.19138860`
Repository path: `sbt-papers/r9-nonergodic-perception/`

## Scripts

### `simulate_absorption.py`

Reproduces:

- **Table 2** in the paper (Ensemble vs. Time Average Divergence under a
  low-coherence reference brand profile, six periods).
- **Table 3** in the paper (Simulated ensemble-time gap across the five
  canonical SBT brand profiles: Hermès, IKEA, Patagonia, Erewhon, Tesla).

Method: Discrete-time absorbing Markov chain. N = 1000 observers begin at an
interior perception state (7.0 on a 0–10 scale). At each period an observer
is absorbed with probability lambda; the per-period absorption rate is
calibrated to the coefficient of variation of each brand's canonical
eight-dimension emission profile (low-coherence profiles drive observers to
absorbing boundaries faster). New absorptions are drawn 70 percent from the
lowest tertile of active observers and 30 percent at random across the rest,
modelling the survivorship-selection mechanism described in Proposition 3.
Surviving observers experience a small positive drift consistent with
multiplicative-update dynamics.

Random seed: `42` (fixed at script top, exposed via `--seed`).

Run command:

```
uv run --with numpy python simulate_absorption.py --seed 42 --periods 6
```

Stdout matches the values cited in Tables 2 and 3 of the paper.

## Provenance

Each script is the ground truth for any value cited as "Monte Carlo,"
"simulated," "computed," or "empirical" in the paper. Per the project's
Paper Quality Standards section 37d, if a script revision changes a number,
the paper's table is updated to match. The internal SSOT for the paper text
lives at `research/R9_nonergodic_perception.md` in the spectral-branding
repository; this `code/` directory is mirrored to the public
`sbt-papers/r9-nonergodic-perception/` repository alongside the public
`paper.md`.
