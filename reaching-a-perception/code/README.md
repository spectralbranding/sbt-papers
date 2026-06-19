# Companion computation — 2026av (cohort-reach handoff contract)

Reproduces **Figure 1** of *Reaching a Perception: From Perceptual Cohort to
Reachable Audience* — the total-loss surface over cohort distinctiveness
(`sin^2(beta)`) and per-impression spill cost, and the frontier separating the
broadcast-a-dimension bridge from the minimal-loss-proxy bridge.

## Run

```
uv run --with numpy --with matplotlib python code/broadcast_channel_loss_surface.py
```

Deterministic (no randomness, no network, no credentials). Outputs
`figures/figure1_loss_surface.png` and prints the critical distinctiveness at the
representative spill cost.

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
