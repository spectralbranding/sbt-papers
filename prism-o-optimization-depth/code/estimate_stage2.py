#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""estimate_stage2.py — refined Stage-2 call-count + cost table (2026bd).

Builds the user-facing spend table required by the HARD STOP before Stage 2:
call counts per operator pair and role, token estimates anchored on Stage-1
MEASURED per-call telemetry (PL3 logs) with artifact-length scaling, priced
from the PL1 list-price table. Nothing here fires a call.

Planning parameters (panel manifest + PL0):
- 60 organizations x 2 channels; ARTIFACTS_PER_CHANNEL artifacts each;
- segmenter: 1 call per artifact; classifier: 1 call per intervention
  (INTERVENTIONS_PER_ARTIFACT planning mean);
- 4 operator pairs (OP1-OP4);
- masked subsample: 15 orgs x 2 channels, same pipeline;
- negative control: disjoint-draw re-read, 20 orgs x 1 channel-split.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_o_lib import (  # noqa: E402
    DATA_DIR,
    LOGS_DIR,
    load_config,
    usage_from_log_record,
)

ORGS = 60
CHANNELS = 2
ARTIFACTS_PER_CHANNEL = 5
INTERVENTIONS_PER_ARTIFACT = 3.0  # planning mean; Stage-1 cannot measure this (single-intervention bank)
ARTIFACT_TOKENS = 3500  # planning mean input length of one real artifact excerpt
MASKED_ORGS = 15
NEGCTRL_ORGS = 20


def stage1_role_telemetry() -> dict:
    """Measured mean in/out tokens per role per model from Stage-1 PL3 logs."""
    agg: dict = {}
    for f in LOGS_DIR.glob("*.jsonl"):
        with f.open() as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                role = rec.get("operator_role")
                model = rec.get("operator") or rec.get("model_version")
                if not role or not model:
                    continue
                tin, tout = usage_from_log_record(rec)
                a = agg.setdefault((role, model), {"n": 0, "in": 0, "out": 0})
                a["n"] += 1
                a["in"] += tin
                a["out"] += tout
    return {
        k: {"n": v["n"], "mean_in": v["in"] / v["n"], "mean_out": v["out"] / v["n"]}
        for k, v in agg.items()
        if v["n"]
    }


def main() -> int:
    cfg = load_config()
    prices = cfg["list_prices"]
    tele = stage1_role_telemetry()

    # Reading jobs: (label, n_org_channel_units)
    core_units = ORGS * CHANNELS
    masked_units = MASKED_ORGS * CHANNELS
    negctrl_units = NEGCTRL_ORGS  # one extra disjoint split per org
    total_units = core_units + masked_units + negctrl_units

    seg_calls_per_unit = ARTIFACTS_PER_CHANNEL
    cls_calls_per_unit = ARTIFACTS_PER_CHANNEL * INTERVENTIONS_PER_ARTIFACT

    rows = []
    grand_calls, grand_cost = 0, 0.0
    for op_id, op in cfg["operator_pairs"].items():
        for role, calls_per_unit in (
            ("segmenter", seg_calls_per_unit),
            ("classifier", cls_calls_per_unit),
        ):
            model = op[role]["model"]
            n_calls = round(total_units * calls_per_unit)
            t = tele.get((role, model))
            # Anchor on measured Stage-1 tokens; scale segmenter input from
            # vignette length (~measured) to artifact length.
            if t:
                mean_in, mean_out = t["mean_in"], t["mean_out"]
                if role == "segmenter":
                    mean_in = mean_in - 150 + ARTIFACT_TOKENS  # swap vignette for artifact
                    mean_out = mean_out * 2.5  # more interventions listed
                else:
                    mean_in = mean_in + 250  # intervention span from real artifact is longer
            else:  # OP2/OP4 models not exercised in Stage 1: use same-role measured mean
                same_role = [v for (r, _m), v in tele.items() if r == role]
                mean_in = (
                    sum(v["mean_in"] for v in same_role) / len(same_role)
                    if same_role
                    else (ARTIFACT_TOKENS + 400 if role == "segmenter" else 1800)
                )
                mean_out = (
                    sum(v["mean_out"] for v in same_role) / len(same_role) if same_role else 400
                )
                if role == "segmenter":
                    mean_in = mean_in - 150 + ARTIFACT_TOKENS
                    mean_out *= 2.5
                else:
                    mean_in += 250
            p = prices[model]
            cost = n_calls * (mean_in * p["input"] + mean_out * p["output"]) / 1_000_000
            rows.append(
                {
                    "op_pair": op_id,
                    "role": role,
                    "model": model,
                    "calls": n_calls,
                    "mean_tokens_in": round(mean_in),
                    "mean_tokens_out": round(mean_out),
                    "est_cost_usd": round(cost, 2),
                    "anchor": "measured" if t else "same-role mean",
                }
            )
            grand_calls += n_calls
            grand_cost += cost

    out = {
        "planning_parameters": {
            "orgs": ORGS,
            "channels": CHANNELS,
            "artifacts_per_channel": ARTIFACTS_PER_CHANNEL,
            "interventions_per_artifact_planning_mean": INTERVENTIONS_PER_ARTIFACT,
            "artifact_tokens_planning_mean": ARTIFACT_TOKENS,
            "masked_subsample_orgs": MASKED_ORGS,
            "negative_control_orgs": NEGCTRL_ORGS,
            "org_channel_units_total": total_units,
        },
        "rows": rows,
        "total_calls": grand_calls,
        "total_est_cost_usd": round(grand_cost, 2),
        "recommended_cap_usd": round(grand_cost * 1.5, 0),
        "note": "retries + malformed redraws inside the 1.5x headroom; the cap is enforced by the runner",
    }
    (DATA_DIR / "stage2_cost_estimate.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
