#!/usr/bin/env python3
"""Reproduce R18 Tables 2 and 3 (Dove brand velocity and acceleration vectors).

Inputs:
    Table 1 (R18 paper): Dove spectral profiles at four temporal cross-sections,
    scale 1-10, eight dimensions (Semiotic, Narrative, Ideological, Experiential,
    Social, Economic, Cultural, Temporal). The Ideological dimension is null
    (None) at 2003 (dimensional creation event).

Method:
    Velocity = centered finite difference of position between consecutive periods,
    attributed to the period midpoint. Acceleration = centered finite difference
    of velocity between consecutive period-midpoint velocities. Both estimators
    are deterministic given Table 1 inputs; no random component.

Outputs:
    table2_velocity.json
    table2_velocity.csv
    table3_acceleration.json
    table3_acceleration.csv

Run:
    python3 compute_velocity_acceleration.py

Reference:
    Zharnikov, D. (2026z). Spectral Dynamics: Velocity, Acceleration, and Phase
    Space in Multi-Dimensional Brand Perception. Working Paper.
    https://doi.org/10.5281/zenodo.19468204
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

# Fixed seed for reproducibility of any future Monte Carlo extensions; the
# finite-difference computation itself has no random component.
SEED = 20260501
random.seed(SEED)

DIMENSIONS = [
    "Semiotic",
    "Narrative",
    "Ideological",
    "Experiential",
    "Social",
    "Economic",
    "Cultural",
    "Temporal",
]

# Table 1: Dove spectral profiles. None marks the dimensional creation event
# (Ideological 2003) where the dimension is undefined; velocity is undefined
# for that period on that dimension.
TABLE_1: dict[int, list[float | None]] = {
    2003: [5.0, 4.0, None, 6.5, 3.5, 7.0, 4.0, 6.0],
    2006: [5.5, 7.5, 8.0, 6.5, 6.0, 7.0, 8.5, 6.5],
    2013: [6.0, 8.5, 9.0, 6.5, 7.5, 7.0, 8.0, 7.0],
    2023: [7.0, 7.5, 7.5, 7.0, 6.5, 6.5, 5.5, 7.5],
}

# Period definitions: (label, t_start, t_end). dt is the year span.
PERIODS = [
    ("Period 1: Ignition", 2003, 2006),
    ("Period 2: Expansion", 2006, 2013),
    ("Period 3: Normative Absorption", 2013, 2023),
]


def velocity_for_period(start: int, end: int) -> list[float | None]:
    """Centered finite difference between two periods. None if either side undefined."""
    dt = end - start
    out: list[float | None] = []
    for d in range(8):
        x0 = TABLE_1[start][d]
        x1 = TABLE_1[end][d]
        if x0 is None or x1 is None:
            out.append(None)
        else:
            out.append(round((x1 - x0) / dt, 4))
    return out


def acceleration_between(v_a: list[float | None], v_b: list[float | None],
                         t_mid_a: float, t_mid_b: float) -> list[float | None]:
    """Centered finite difference between two velocity midpoints."""
    dt = t_mid_b - t_mid_a
    out: list[float | None] = []
    for d in range(8):
        if v_a[d] is None or v_b[d] is None:
            out.append(None)
        else:
            out.append(round((v_b[d] - v_a[d]) / dt, 4))
    return out


def brand_speed(v: list[float | None]) -> tuple[float, int]:
    """Magnitude over computable dimensions; returns (speed, n_dims)."""
    sq = [x * x for x in v if x is not None]
    speed = round(sum(sq) ** 0.5, 4)
    return speed, len(sq)


def main() -> None:
    out_dir = Path(__file__).resolve().parent

    # --- Table 2: velocity vectors ---
    velocities: dict[str, dict] = {}
    for label, t0, t1 in PERIODS:
        v = velocity_for_period(t0, t1)
        speed, n = brand_speed(v)
        midpoint = (t0 + t1) / 2.0
        velocities[label] = {
            "t_start": t0,
            "t_end": t1,
            "dt_years": t1 - t0,
            "midpoint_year": midpoint,
            "velocity": dict(zip(DIMENSIONS, v)),
            "brand_speed": speed,
            "n_dims_used": n,
        }

    (out_dir / "table2_velocity.json").write_text(
        json.dumps(velocities, indent=2)
    )
    with (out_dir / "table2_velocity.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["period"] + DIMENSIONS + ["brand_speed", "n_dims_used"])
        for label, payload in velocities.items():
            row = [label] + [payload["velocity"][d] for d in DIMENSIONS]
            row += [payload["brand_speed"], payload["n_dims_used"]]
            w.writerow(row)

    # --- Table 3: acceleration vectors ---
    period_labels = list(velocities.keys())
    accelerations: dict[str, dict] = {}
    for i in range(len(period_labels) - 1):
        a_label = period_labels[i]
        b_label = period_labels[i + 1]
        v_a = list(velocities[a_label]["velocity"].values())
        v_b = list(velocities[b_label]["velocity"].values())
        t_mid_a = velocities[a_label]["midpoint_year"]
        t_mid_b = velocities[b_label]["midpoint_year"]
        a_vec = acceleration_between(v_a, v_b, t_mid_a, t_mid_b)
        accelerations[f"{a_label} -> {b_label}"] = {
            "t_mid_a": t_mid_a,
            "t_mid_b": t_mid_b,
            "dt_mid_years": round(t_mid_b - t_mid_a, 4),
            "acceleration": dict(zip(DIMENSIONS, a_vec)),
        }

    (out_dir / "table3_acceleration.json").write_text(
        json.dumps(accelerations, indent=2)
    )
    with (out_dir / "table3_acceleration.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["transition"] + DIMENSIONS + ["dt_mid_years"])
        for label, payload in accelerations.items():
            row = [label] + [payload["acceleration"][d] for d in DIMENSIONS]
            row += [payload["dt_mid_years"]]
            w.writerow(row)

    print("Wrote:")
    for fname in (
        "table2_velocity.json",
        "table2_velocity.csv",
        "table3_acceleration.json",
        "table3_acceleration.csv",
    ):
        print(f"  {out_dir / fname}")


if __name__ == "__main__":
    main()
