#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26", "pyyaml>=6.0"]
# ///
"""metameric_check.py — supplementary pre-registered P4 check (amendment A4).

Implements the metameric-equality corollary check that was specified in the
pre-registration and the paper's Results shell but omitted from the frozen
estimator build: for each category and floor-passing operator, a brand pair
is METAMERIC when the distance between the operator's median brand profiles
falls below that operator's reading floor (median within-brand replicate
distance, the operator's own noise scale). For every metameric pair, the
cohort propensity difference |p(c,a) - p(c,b)| is compared to the
elicitation floor (median within-cohort replicate propensity dispersion).
Additive, read-only supplement; no frozen primary/secondary rule changes.

Run:
    uv run python code/metameric_check.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import yaml

import estimator as E

PAPER_DIR = Path(__file__).resolve().parent.parent


def main() -> None:
    results = json.loads((PAPER_DIR / "data" / "results.json").read_text())
    passing = results["floor_passing_operators"]
    personas_all = yaml.safe_load((PAPER_DIR / "PERSONAS.yaml").read_text())[
        "categories"
    ]
    s1 = yaml.safe_load((PAPER_DIR / "STIMULI_STUDY1.yaml").read_text())
    s2 = yaml.safe_load((PAPER_DIR / "BRANDS_STUDY2.yaml").read_text())
    cat_brands = {
        "coffee_roasters": [b["name"] for b in s1["brands"]],
        "qsr_coffee": [b["name"] for b in s2["qsr_coffee"]["brands"]],
        "athletic_footwear": [b["name"] for b in s2["athletic_footwear"]["brands"]],
    }
    ops_data = E.load_all(str(PAPER_DIR / "data" / "records_OP*.jsonl"))

    out: dict = {"metameric_pairs": [], "per_category_floor_summary": {}}
    for cat, brands in cat_brands.items():
        floor_list = []
        for op in passing:
            od = ops_data[op]
            med, floors = {}, {}
            ok = True
            for b in brands:
                reps = [np.array(v) for v in od["readings"].get((cat, b), [])]
                if len(reps) < 2:
                    ok = False
                    break
                med[b] = np.median(np.array(reps), axis=0)
                pd = [
                    float(np.linalg.norm(reps[i] - reps[j]))
                    for i in range(len(reps))
                    for j in range(i + 1, len(reps))
                ]
                floors[b] = float(np.median(pd))
            if not ok:
                continue
            floor_list.append(float(np.median(list(floors.values()))))
            # elicitation floor: within-cohort replicate propensity dispersion
            e_disp = []
            for c in personas_all[cat]:
                recs = od["eliciting"].get((cat, c["cohort_id"]), [])
                if len(recs) >= 2:
                    tbl = np.array(
                        [
                            [r["payload"]["constant_sum"][b] / 10 for b in brands]
                            for r in recs
                        ]
                    )
                    e_disp.append(float(np.mean(tbl.std(axis=0, ddof=1))))
            e_floor = float(np.median(e_disp)) if e_disp else float("nan")
            for i in range(len(brands)):
                for j in range(i + 1, len(brands)):
                    a, b = brands[i], brands[j]
                    d = float(np.linalg.norm(med[a] - med[b]))
                    pair_floor = max(floors[a], floors[b])
                    if d < pair_floor:
                        # metameric pair: compare propensity difference
                        dp = []
                        for c in personas_all[cat]:
                            recs = od["eliciting"].get((cat, c["cohort_id"]), [])
                            if recs:
                                pa = float(
                                    np.median(
                                        [
                                            r["payload"]["constant_sum"][a] / 10
                                            for r in recs
                                        ]
                                    )
                                )
                                pb = float(
                                    np.median(
                                        [
                                            r["payload"]["constant_sum"][b] / 10
                                            for r in recs
                                        ]
                                    )
                                )
                                dp.append(abs(pa - pb))
                        out["metameric_pairs"].append(
                            {
                                "category": cat,
                                "operator": op,
                                "pair": [a, b],
                                "profile_distance": round(d, 3),
                                "pair_reading_floor": round(pair_floor, 3),
                                "median_abs_propensity_diff": round(
                                    float(np.median(dp)), 4
                                ),
                                "elicitation_floor": round(e_floor, 4),
                                "within_elicitation_floor": bool(
                                    np.median(dp) <= e_floor
                                ),
                            }
                        )
        out["per_category_floor_summary"][cat] = {
            "median_reading_floor": (
                round(float(np.median(floor_list)), 3) if floor_list else None
            )
        }

    out["n_metameric_pairs"] = len(out["metameric_pairs"])
    path = PAPER_DIR / "data" / "metameric_check.json"
    path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2)[:2000])
    print(f"-> {path}")


if __name__ == "__main__":
    main()
