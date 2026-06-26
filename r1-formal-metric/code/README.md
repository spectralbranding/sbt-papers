# Reference implementation — R1 (Brand Space Geometry, 2026d)

`metrics.py` is the NumPy reference implementation of the three metrics defined
in *Brand Space Geometry: A Formal Metric for Multi-Dimensional Brand
Perception*:

- **Aitchison distance** on the brand signal space $\mathcal{B} = \mathbb{R}^8_+$
  (`aitchison_distance`, via `clr` / `ilr`) — Definition 1, Theorem 1.
- **Fisher-Rao distance** on the observer simplex $\mathcal{O} = \Delta^7$
  (`fisher_rao_distance`), $d_{FR}(p,q) = 2\arccos(\sum_i \sqrt{p_i q_i})$ —
  Definition 2, Theorem 2.
- **Warped-product / observer-dependent distance** on the combined space
  $\mathcal{P}$ (`combined_distance`, `observer_distance`) — Definition 3,
  Proposition 3.
- **Null baseline** `expected_simplex_pair_distance` (root-mean-square distance
  $\sqrt{7/36}\approx.4410$, Theorem 4) and the Theorem 5(i) closed form
  `expected_observer_distance_sq` ($E_w[d_w^2] = \tfrac{1}{8}\lVert
  \mathrm{clr}(s_A)-\mathrm{clr}(s_B)\rVert^2$).

## Run

```
uv run python research/papers/2026d/code/metrics.py
```

The `__main__` smoke test uses a fixed seed (`20260326`) and reproduces:

- the null baseline $\sqrt{7/36}\approx.4410$ (the closed-form
  $E[\lVert w_A-w_B\rVert^2]=7/36$ checked against Monte Carlo);
- the $1/256$ positive-octant volume fraction (Proposition 4);
- the Theorem 5(i) closed form for $E_w[d_w^2]$(Hermès, IKEA) against a Monte
  Carlo estimate over uniform observers;
- the pairwise Aitchison distance $d(\text{Hermès},\text{Tesla})\approx 1.76$
  (Table 6).

Only NumPy is required.
