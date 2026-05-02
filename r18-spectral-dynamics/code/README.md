# R18 Companion Computation Scripts

Reproduces Tables 2 and 3 (Dove brand velocity and acceleration vectors) and
Figure 2 (Dove (Cultural, Ideological) phase trajectory) of the R18 paper
*Spectral Dynamics: Velocity, Acceleration, and Phase Space in Multi-
Dimensional Brand Perception* (Zharnikov 2026z).

## Run

Tables 2 and 3 (Python standard library only):

```
python3 compute_velocity_acceleration.py
```

Figure 2 (numpy + matplotlib via PEP 723 inline-deps):

```
uv run --script phase_portrait.py
```

## Inputs

Table 1 of the paper (Dove spectral profiles at 2003, 2006, 2013, 2023; eight
dimensions; scale 1-10). The Ideological dimension is undefined at 2003
(dimensional creation event).

## Method

- **Velocity** = centered finite difference of consecutive period positions,
  attributed to the period midpoint.
- **Acceleration** = centered finite difference of consecutive period-midpoint
  velocities.
- Both estimators are deterministic given Table 1 inputs. A fixed seed
  (`SEED = 20260501`) is set only to lock random behavior for any future Monte
  Carlo extension.

## Outputs

- `table2_velocity.json` — velocity vectors per period plus brand speed and the
  number of dimensions used (7 for Period 1, 8 for Periods 2 and 3).
- `table2_velocity.csv` — flat CSV of the same.
- `table3_acceleration.json` — acceleration vectors between consecutive period
  midpoints.
- `table3_acceleration.csv` — flat CSV of the same.
- `figure2_dove_phase.png` — Dove (Cultural, Ideological) phase trajectory across
  the three time points where both dimensions are defined (2006, 2013, 2023),
  with arrow segments showing direction of motion across the Expansion and
  Normative-Absorption periods.

## Reference

Zharnikov, Dmitry (2026z), "Spectral Dynamics: Velocity, Acceleration, and Phase
Space in Multi-Dimensional Brand Perception," working paper.
https://doi.org/10.5281/zenodo.19468204
