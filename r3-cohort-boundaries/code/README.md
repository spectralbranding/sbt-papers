# R3 Computation Scripts

Reproducibility scripts for the numerical figures cited in the R3 paper
(Zharnikov 2026f, *Geometric Necessity of Fuzzy Cohort Boundaries: A
Concentration Analysis of the 7-Simplex*; DOI 10.5281/zenodo.18945477).

## Files

- `r3_concentration_mc.py` — Monte Carlo simulations for Tables 2, 5, and 7.
  Produces (a) distance contrast ratio degradation with dimension under
  Euclidean distance on the simplex, (b) empirical boundary volume fractions
  at $n = 8$, $k = 4$ partitions under both Euclidean and Fisher-Rao metrics,
  and (c) the side-by-side Euclidean vs Fisher-Rao contrast comparison at
  $n = 8$.

## Running

```bash
uv run --with numpy --with scikit-learn python r3_concentration_mc.py
```

Random seed is fixed at 42; trial counts and sample sizes match those quoted
in the paper. Output is printed to stdout.

## Provenance

Scripts published alongside the paper for transparency. Numerical figures
in the paper match the stdout of these scripts within the reported standard
errors.
