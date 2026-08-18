# R3 Computation Scripts

Reproducibility scripts for the numerical figures cited in the R3 paper
(Zharnikov 2026f, *Boundary Volume and Cohort Reassignment on the 7-Simplex: A
Concentration Analysis Under the Uniform Null*; DOI 10.5281/zenodo.18945477).

## Files

- `r3_concentration_mc.py` — every Monte Carlo figure in the paper:
  - **Table 3** distance contrast ratio degradation with dimension (Euclidean),
    with the standard error on each ratio estimate and independent replications
    of the degenerate $n = 2$ row.
  - **Table 4** Euclidean versus Fisher-Rao concentration at $n = 8$, plus the
    analytic Bhattacharyya coefficient and the Jensen gap between
    $2\arccos(E[\cdot])$ and $E[2\arccos(\cdot)]$.
  - **Table 7** boundary volume fraction, verifying Theorem 2 under the settled
    definition of $\delta$ and reporting the three rejected readings alongside
    it so the comparison is reproducible rather than asserted.
  - **Table 8** inter-cohort bisector proximity (Proposition 4), with the
    sensitivity to cohort count $k$ and to the random seed.
  - **Table 9** analytic check of the fixed-zone Dirichlet contraction.
  - **Table 10** re-fitted partitions on concentrated Dirichlet populations.

  It also runs `inradius_counterexample()`, the thin-box witness showing that
  normalising $\delta$ by a cell's in-radius claims a bound that
  Brunn-Minkowski does not deliver — the correction applied to Theorem 2 in
  v2.0.0.

## Running

```bash
uv run --with numpy --with scipy --with scikit-learn python r3_concentration_mc.py
```

Runtime is roughly two minutes on a laptop. Random seed is fixed at 42 except
where a table varies the seed deliberately (the seed-stability block of Table
8); trial counts and sample sizes match those quoted in the paper. Output is
printed to stdout.

## What changed in v2.0.0

Theorem 2 bounds the fraction of the simplex within relative distance $\delta$
of the boundary of its own convex cell. Two conventions were previously
ambiguous between the theorem and its verification, and the script now fixes
both explicitly:

- $\delta$ is normalised by the cell's **volume radius**
  $r_V = (\text{vol}(C)/\omega_d)^{1/d}$, $d = n-1$ — not by its in-radius. The
  in-radius form is not provable (see `inradius_counterexample()`).
- distance is measured to the **full** cell boundary: internal bisectors
  together with the faces of the simplex that bound the cell.

The previous version measured an absolute distance to the internal bisector
only and compared it against a bound derived for a relative distance to the
full boundary. The script reports both, so the mismatch is visible in the
output rather than only in the changelog.

## Provenance

Scripts published alongside the paper for transparency. Numerical figures in
the paper match the stdout of this script within the reported standard errors.
