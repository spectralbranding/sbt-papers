#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26", "pyyaml>=6.0", "scipy>=1.11"]
# ///
"""power_analysis.py — simulation-based power analysis for PRISM-T (2026ba).

The pre-draft review's fatal gap 3: does n brands x 4 artifacts x 4 operator
pairs give sufficient precision to detect version drift at S/N > 2 under the
brand-cluster bootstrap, and what is the minimum detectable per-dimension
drift for the H3 two-set contrast?

The simulation runs the REAL PL4 estimator (`estimator.analyze`) on synthetic
record sets from `synthetic.gen_records`; nothing is re-implemented. Noise
scales are anchored to the empirical record: operator-floor magnitudes from
2026ax (cohort-level 1−cosine .0034–.057) and the H13 prior (inter-version
distances < .03, 2026v). sigma_op is swept so the induced synthetic operator
floor spans that range (the printed table reports the induced floor per cell).

Fixed seed 20260702 (replicate r uses seed SEED + r). Bootstrap draws are
reduced to 500 for the power grid (documented; the confirmatory analysis
uses 2,000).

Run:
    uv run python research/prism_t/code/power_analysis.py \
        --out research/prism_t/data/power_analysis.json
Quick smoke (tiny grid):
    uv run python research/prism_t/code/power_analysis.py --quick --out /tmp/pa.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))
import estimator  # noqa: E402
from prism_t_lib import SEED  # noqa: E402
from synthetic import gen_records  # noqa: E402

ALPHA_H3 = 0.017  # Bonferroni allocation (PL0 §6)


def run_cell(
    *,
    n_brands: int,
    sigma_op: float,
    drift: float,
    n_replicates: int,
    n_boot: int = 500,
) -> dict:
    h1_hits, h3_hits, floors, snrs = 0, 0, [], []
    estimator.N_BOOT = n_boot
    for r in range(n_replicates):
        records, cfg = gen_records(
            n_brands=n_brands,
            sigma_op=sigma_op,
            drift=drift,
            seed=SEED + r,
        )
        res = estimator.analyze(records, cfg, seed=SEED + r)
        if res["h1_supported"]:
            h1_hits += 1
        lad = res["ladders"]["fam-a-ladder"]
        if (
            lad["h3"].get("p_one_sided") is not None
            and lad["h3"]["p_one_sided"] < ALPHA_H3
        ):
            h3_hits += 1
        floors.append(res["operator_floor"]["mean"])
        best = max(
            (p["snr"] for p in lad["pairs"].values() if p.get("snr") is not None),
            default=None,
        )
        if best is not None:
            snrs.append(best)
    return {
        "n_brands": n_brands,
        "sigma_op": sigma_op,
        "drift": drift,
        "n_replicates": n_replicates,
        "h1_power": h1_hits / n_replicates,
        "h3_power": h3_hits / n_replicates,
        "induced_operator_floor_mean": float(np.mean(floors)),
        "best_pair_snr_median": float(np.median(snrs)) if snrs else None,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()

    if args.quick:
        brands_grid, sigma_grid = [40], [0.3]
        drift_grid, n_rep = [0.0, 0.5], 5
    else:
        brands_grid = [30, 40, 50]
        sigma_grid = [0.15, 0.3, 0.6]
        drift_grid = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0]
        n_rep = 100

    cells = []
    for nb in brands_grid:
        for so in sigma_grid:
            for dr in drift_grid:
                cell = run_cell(n_brands=nb, sigma_op=so, drift=dr, n_replicates=n_rep)
                cells.append(cell)
                print(
                    f"[power] n={nb} sigma_op={so} drift={dr}: "
                    f"H1 {cell['h1_power']:.2f} H3 {cell['h3_power']:.2f} "
                    f"floor {cell['induced_operator_floor_mean']:.4f}",
                    flush=True,
                )

    # minimum detectable drift (>= .80 power) per (n, sigma) for H1 and H3
    mde = {}
    for nb in brands_grid:
        for so in sigma_grid:
            row = [c for c in cells if c["n_brands"] == nb and c["sigma_op"] == so]
            row.sort(key=lambda c: c["drift"])
            mde[f"n{nb}_s{so}"] = {
                "h1_mde": next((c["drift"] for c in row if c["h1_power"] >= 0.8), None),
                "h3_mde": next((c["drift"] for c in row if c["h3_power"] >= 0.8), None),
                "h1_false_positive_at_null": next(
                    (c["h1_power"] for c in row if c["drift"] == 0.0), None
                ),
                "h3_false_positive_at_null": next(
                    (c["h3_power"] for c in row if c["drift"] == 0.0), None
                ),
            }
    out = {
        "seed": SEED,
        "n_boot": 500,
        "alpha_h3": ALPHA_H3,
        "design": "n brands x 4 channels x 4 operator pairs; 3-rung ladder",
        "anchors": {
            "operator_floor_2026ax_range": [0.0034, 0.057],
            "h13_interversion_distance_upper": 0.03,
        },
        "cells": cells,
        "minimum_detectable_drift": mde,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=2))
    print(f"[power] written -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
