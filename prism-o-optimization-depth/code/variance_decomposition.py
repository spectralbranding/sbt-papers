#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0", "numpy>=1.26"]
# ///
"""variance_decomposition.py — PRISM-O (2026bd) artifact-level variance shares.

Decomposes, per organization x channel (named arm, primary Stage-2 records),
the dispersion of per-cell mean depth (cell = operator pair x artifact) into
its two marginal components:

- between-artifact: variance (ddof=1) across artifacts of the pair-averaged
  artifact depth means — how much individual filings differ in depth;
- between-pair: variance (ddof=1) across operator pairs of the
  artifact-averaged pair depth means — how much model families disagree.

Shares are each component over their sum (marginal shares; the pair x
artifact interaction is not separated at one reading per cell). Cells with no
classified intervention are empty; org-channels need >= 3 pairs and >= 4
artifacts with data (mirrors the estimator's pair rule and the negative
control's artifact minimum). Deterministic; SEED fixed for consistency with
the PL4 estimator.

Writes research/prism_o/data/variance_decomposition.json and prints the
panel summary.

Run command:
    uv run python research/prism_o/code/variance_decomposition.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_o_lib import DATA_DIR, load_records  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "research"))

SEED = 20260703
MIN_PAIRS = 3
MIN_ARTIFACTS = 4
DEPTH = {"D1": 4.0, "D2": 3.0, "D3": 2.0, "D4": 1.0}


def main() -> int:
    np.random.seed(SEED)
    recs = []
    for shard in sorted(DATA_DIR.glob("stage2_records*.jsonl")):
        recs.extend(load_records(shard))
    # (org, channel) -> pair -> artifact -> [depths]
    cells: dict = {}
    for r in recs:
        if r.get("sentinel") or r.get("arm") != "named":
            continue
        v = DEPTH.get(r["rung_pred"])
        if v is None:
            continue
        cells.setdefault((r["org"], r["channel"]), {}).setdefault(
            r["op_pair"], {}
        ).setdefault(r["artifact_id"], []).append(v)

    rows = {}
    for (org, ch), byp in sorted(cells.items()):
        pairs = sorted(byp)
        arts = sorted({a for by in byp.values() for a in by})
        if len(pairs) < MIN_PAIRS or len(arts) < MIN_ARTIFACTS:
            continue
        # cell matrix of per-(pair, artifact) mean depth; NaN where empty
        m = np.full((len(pairs), len(arts)), np.nan)
        for i, p in enumerate(pairs):
            for j, a in enumerate(arts):
                if a in byp[p]:
                    m[i, j] = float(np.mean(byp[p][a]))
        art_means = np.nanmean(m, axis=0)  # pair-averaged, per artifact
        pair_means = np.nanmean(m, axis=1)  # artifact-averaged, per pair
        art_means = art_means[~np.isnan(art_means)]
        pair_means = pair_means[~np.isnan(pair_means)]
        if len(art_means) < 2 or len(pair_means) < 2:
            continue
        v_art = float(np.var(art_means, ddof=1))
        v_pair = float(np.var(pair_means, ddof=1))
        total = v_art + v_pair
        rows[f"{org}|{ch}"] = {
            "org": org,
            "channel": ch,
            "n_pairs": len(pairs),
            "n_artifacts": int(len(art_means)),
            "var_between_artifact": round(v_art, 4),
            "var_between_pair": round(v_pair, 4),
            "share_between_artifact": round(v_art / total, 4) if total > 0 else None,
        }

    def summarize(ch: str) -> dict:
        shares = [
            r["share_between_artifact"]
            for r in rows.values()
            if r["channel"] == ch and r["share_between_artifact"] is not None
        ]
        return {
            "n_org_channels": len(shares),
            "median_share_between_artifact": round(float(np.median(shares)), 3),
            "mean_share_between_artifact": round(float(np.mean(shares)), 3),
            "n_artifact_dominant": int(sum(s > 0.5 for s in shares)),
        }

    out = {
        "seed": SEED,
        "min_pairs": MIN_PAIRS,
        "min_artifacts": MIN_ARTIFACTS,
        "summary": {ch: summarize(ch) for ch in ("STATED", "ENACTED")},
        "per_org_channel": rows,
    }
    (DATA_DIR / "variance_decomposition.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out["summary"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
