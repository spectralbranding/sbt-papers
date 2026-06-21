# R4 Computation Scripts

Reproducibility script for the numerical figures cited in the R4 paper
(Zharnikov 2026g, *How Many Brands Can a Market Hold? Sphere Packing Bounds for
Multi-Dimensional Positioning*; DOI 10.5281/zenodo.18945522).

## Files

- `r4_capacity_bounds.py` — independently recomputes (does not hard-code) every
  numerical value the paper reports, then prints a computed-vs-paper comparison
  marking MATCH / MISMATCH. Covers:
  - Table 2 — unit ball volume `V_n(1)` for `n` in {1,2,3,4,5,8,16,24,48}
  - Table 4 — positioning capacity bounds, lower `(1/eps)^8` and upper `((2+eps)/eps)^8`
  - Table 6 — white-space fractions `1 - n_b * eps^8` at `eps = .10`
  - Table 7 — category saturation thresholds `(1/eps)^d_eff`
  - Table 8 — effective dimensionality `n/(1+(n-1)rho)` and capacity collapse
  - Appendix A1 / B1 — key numerical values and dimensional capacity bounds
  - Figure 1 — deterministic enumeration of the 240 minimal vectors of the `E8`
    lattice at squared norm 2, decomposed as 112 specialist + 128 generalist
    (verified `112 + 128 = 240`, all at squared norm exactly 2)
  - In-text — `E8` packing density `pi^4/384 ~= .2537`, `N_E8 ~= 6.49e9` at
    `eps = .10`, corner effect `V_8(1)/2^8`, mean radius `sqrt(8/10)`

## Running

```bash
uv run --with numpy --with scipy python r4_capacity_bounds.py
```

Random seed is fixed at 42. There are no stochastic computations — every value is
closed-form or exact integer enumeration; the seed is included for repository
reproducibility-policy compliance. Output is printed to stdout, ending in a
PASS/FAIL summary.

## Provenance

Published alongside the paper for transparency. All paper-reported values are
reproduced within the stated display precision (68/68 comparisons MATCH).

### Effective-dimensionality measure

Proposition 5 defines effective dimensionality as `d_eff = trace/lambda_max =
n/(1+(n-1)rho)` for the equicorrelation matrix — the measure every tabulated
Table-8 value uses. The **participation ratio** `(sum lam)^2 / sum(lam^2)` is a
*different* effective-dimensionality measure that yields larger values (e.g.
`n=8, rho=.1`: `trace/lambda_max = 4.71` vs. participation ratio `7.48`). The
script computes **both** for transparency and prints them side by side; only
`trace/lambda_max` drives the paper's capacity-collapse numbers. No formula was
altered to force a match (68/68 comparisons MATCH).
