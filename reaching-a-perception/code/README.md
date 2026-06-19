# Companion computation — 2026av (cohort-reach handoff contract)

Two scripts. **Figure 1** (`broadcast_channel_loss_surface.py`) reproduces the
total-loss surface over cohort distinctiveness (`sin^2(beta)`) and per-impression
spill cost, and the frontier separating the broadcast-a-dimension bridge from the
minimal-loss-proxy bridge. **Figure 2 + Table 1** (`broadcast_channel_me2.py`)
reproduces the *Calibrated Demonstration* (the ME2 methods-companion fallback):
the calibration to the five canonical public brand profiles, the Monte-Carlo
resonance over-index with bootstrap CIs, and the two case studies.

## Run

```
uv run --with numpy --with matplotlib python code/broadcast_channel_loss_surface.py
uv run --with numpy --with matplotlib python code/broadcast_channel_me2.py
```

The first is deterministic (no randomness). The second is a seeded Monte Carlo
(`seed = 20260619`) — reproducible bit-for-bit. Neither uses the network or
credentials. Outputs: `figures/figure1_loss_surface.png`,
`figures/figure2_me2_overindex.png`, and `output/tables/me2_results.csv`.

## ME2 calibrated demonstration (`broadcast_channel_me2.py`)

Distinctiveness is calibrated to an **observed public proxy** — the five canonical
brand profiles (Hermes, IKEA, Patagonia, Erewhon, Tesla), the corpus's public
anchors, NOT the work-in-progress atom instrument. For a single-dimension
broadcast, a cohort's distinctiveness is the share of its *centered* profile's
energy carried by its dominant dimension (this removes the common positive-level
"halo" every brand shares). The five anchors give distinctiveness
`{.760, .358, .348, .336, .335}` (mean `.427`), fit by a method-of-moments
`Beta(2.59, 3.47)`. Drawing 10,000 cohorts and running each through the two-type
broadcast-channel model yields the resonance over-index `1.202` (95% CI
`[1.196, 1.207]`, Cohen's `d = 1.61`) and the broadcast-reachable fraction `.626`.
Two case studies instantiate the contract: a maintenance campaign (Hermes,
`s = .760` -> broadcast, cost `.074`) and a category-creation campaign (flat new
entrant, `s = .125` floor -> proxy/provenance). The routing threshold
`s* = 1 - L0/c_ref = .355` is inherited from Figure 1 so the two scripts are
calibrated consistently.

## Model

Two bridges compete for a target `(dimension, cohort)`:

- **Broadcast a dimension (route b):** total loss `L_b(s, c) = c * (1 - s)` —
  the spill cost `c` paid on the non-resonant impression fraction `(1 - s)`; a
  more distinct cohort (`s = sin^2(beta)` larger) self-selects more cleanly, so
  spill falls.
- **Minimal-loss proxy (route a):** total loss `L_a = L0`, the Blackwell-garbling
  decision loss `L(P*)` of reaching the cohort through its most informative
  addressable proxy, independent of broadcast spill.

The handoff contract routes to `min(L_b, L_a)`. The white dashed frontier is the
tie locus `c * (1 - s) = L0`. The **critical distinctiveness** is
`s_crit = 1 - L0 / c_ref` — the value of `s` at which broadcast ties the proxy at
a representative spill cost. With the documented constants `L0 = .20`,
`c_ref = .31`, `s_crit = .355`, matching the `~.35` scope-condition threshold in
the paper.

## Calibration

`L0` and `c_ref` are documented, representative constants (an illustrative
proxy-informativeness level and spill cost), not values fit to live data. `L0`
stands in for the median proxy-join loss — the decision loss implied by the
mutual information between perceptual-cohort membership and addressable proxy
features — and is replaced by the corpus-estimated value when the
`Empirical Strategy` proxy-loss estimation is run. The qualitative shape of the
surface and the frontier are invariant to the exact constants; only the location
of `s_crit` shifts.

## AI-disclosure tier

Tier B (companion computation): the figure derives from this fixed-parameter
deterministic script. No Monte Carlo randomness is used; the determinism is
exact.
