#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0", "numpy>=1.26", "scipy>=1.12"]
# ///
"""analyze_posthoc.py — 2026bd post-campaign amendment analyses (PL0 v1.2).

Two clearly-labeled POST-HOC analyses that repair the two instrument findings
of the primary campaign; the primary pre-registered analysis is UNCHANGED and
reported first in the paper.

1. NESTED FLOOR (answers finding F6, negative control 9/46): the resolution
   criterion gains an artifact-sampling band under the operator band —
   artifact_floor(org) = SD of the seeded artifact-cluster bootstrap of
   gap_hat (B = 2000, seed 20260703); an organization resolves NESTED iff
   |gap_hat| > 2 x max(operator_floor, artifact_floor). The negative control
   re-runs under the analogous nested criterion: a pseudo-gap resolves only
   if it clears 2 x max(its across-pair SD, the org's artifact_floor).

2. RC1 TIE-BREAKER SENSITIVITY (answers limitation L5) from the re-read arm
   (rerun_rc1.py): per regime (downward=primary, up, tie), recompute Stage-1
   macro accuracy and the Stage-2 all-org gap summary + resolved counts
   (operator-floor criterion, primary definition) — the pre-registered
   three-regime stability check, executed late and labeled.

Writes data/pl4_posthoc_results.json. Run:
    uv run python research/prism_o/code/analyze_posthoc.py
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estimator_stage2 import DEPTH, SEED, SNR_K, mean_depth, org_channel_depths  # noqa: E402
from prism_o_lib import DATA_DIR, load_records  # noqa: E402


def load_all_stage2():
    recs = []
    for shard in sorted(DATA_DIR.glob("stage2_records_op*.jsonl")):
        recs.extend(load_records(shard))
    return recs


def gaps_from_depths(depths, pairs, org):
    gaps = {}
    for p in pairs:
        s = mean_depth(depths.get((org, "STATED"), {}).get(p, {}))
        e = mean_depth(depths.get((org, "ENACTED"), {}).get(p, {}))
        if not (np.isnan(s) or np.isnan(e)):
            gaps[p] = s - e
    return gaps


def nested_floor_analysis(recs) -> dict:
    rng = np.random.default_rng(SEED)
    depths = org_channel_depths(recs, "named")
    pairs = sorted({r["op_pair"] for r in recs if not r.get("sentinel")})
    orgs = sorted({r["org"] for r in recs if not r.get("sentinel")})
    out = {"criterion": "|gap_hat| > 2 x max(operator_floor, artifact_floor[boot SD])",
           "per_org": {}, }
    n_res_primary = n_res_nested = n_ok = 0
    for org in orgs:
        gaps = gaps_from_depths(depths, pairs, org)
        if len(gaps) < 3:
            continue
        n_ok += 1
        g = np.array(list(gaps.values()))
        gap_hat, op_floor = float(np.mean(g)), float(np.std(g, ddof=1))
        boots = []
        for _ in range(2000):
            bg = []
            for p in gaps:
                s_by = depths.get((org, "STATED"), {}).get(p, {})
                e_by = depths.get((org, "ENACTED"), {}).get(p, {})
                s_ids, e_ids = list(s_by), list(e_by)
                if not s_ids or not e_ids:
                    continue
                s = np.mean([v for a in (s_ids[i] for i in rng.integers(0, len(s_ids), len(s_ids))) for v in s_by[a]])
                e = np.mean([v for a in (e_ids[i] for i in rng.integers(0, len(e_ids), len(e_ids))) for v in e_by[a]])
                bg.append(s - e)
            if bg:
                boots.append(np.mean(bg))
        art_floor = float(np.std(boots, ddof=1)) if len(boots) > 1 else float("nan")
        res_primary = abs(gap_hat) > SNR_K * op_floor
        res_nested = abs(gap_hat) > SNR_K * max(op_floor, art_floor)
        n_res_primary += res_primary
        n_res_nested += res_nested
        out["per_org"][org] = {"gap_hat": round(gap_hat, 4), "operator_floor": round(op_floor, 4),
                               "artifact_floor": round(art_floor, 4),
                               "resolved_primary": bool(res_primary), "resolved_nested": bool(res_nested)}
    # negative control under the SAME nested machinery applied to the
    # half-split: the pseudo-gap must clear 2 x max(its across-pair SD, the
    # bootstrap SD of the pseudo-gap itself — artifacts resampled within
    # each half). This prices the half-split's own artifact sampling
    # variance, which the full-panel band under-prices by construction.
    neg = {"n_tested": 0, "n_pseudo_resolved_nested": 0}
    for (org, c), byp in depths.items():
        aids = sorted({a for by in byp.values() for a in by})
        if len(aids) < 4 or org not in out["per_org"]:
            continue
        half1, half2 = list(aids[0::2]), list(aids[1::2])
        pg = []
        for p in byp:
            m1, m2 = mean_depth(byp[p], set(half1)), mean_depth(byp[p], set(half2))
            if not (np.isnan(m1) or np.isnan(m2)):
                pg.append(m1 - m2)
        if len(pg) < 3:
            continue
        neg["n_tested"] += 1
        boots = []
        for _ in range(2000):
            bg = []
            for p in byp:
                h1 = [half1[i] for i in rng.integers(0, len(half1), len(half1))]
                h2 = [half2[i] for i in rng.integers(0, len(half2), len(half2))]
                v1 = [v for a in h1 for v in byp[p].get(a, [])]
                v2 = [v for a in h2 for v in byp[p].get(a, [])]
                if v1 and v2:
                    bg.append(np.mean(v1) - np.mean(v2))
            if bg:
                boots.append(np.mean(bg))
        split_art = float(np.std(boots, ddof=1)) if len(boots) > 1 else float("inf")
        if abs(np.mean(pg)) > SNR_K * max(float(np.std(pg, ddof=1)), split_art):
            neg["n_pseudo_resolved_nested"] += 1

    # class-stratified control: split WITHIN artifact class (alternating
    # artifacts of the same class into the two halves), so the pseudo-gap
    # holds class composition constant — isolates sampling noise from
    # class structure. Requires the class map from the pinned manifest.
    manifest = json.loads((DATA_DIR / "panel_pinned_manifest.json").read_text())
    cls_of = {(o["org"], a["channel"], a["artifact_id"]): a["class"]
              for o in manifest["orgs"] for a in o["artifacts"]}
    negc = {"n_tested": 0, "n_pseudo_resolved": 0}
    for (org, c), byp in depths.items():
        aids = sorted({a for by in byp.values() for a in by})
        if len(aids) < 4 or org not in out["per_org"]:
            continue
        by_cls: dict = defaultdict(list)
        for a in aids:
            by_cls[cls_of.get((org, c, a), "?")].append(a)
        half1, half2 = [], []
        for cls_aids in by_cls.values():
            half1 += cls_aids[0::2]
            half2 += cls_aids[1::2]
        if not half1 or not half2:
            continue
        pg = []
        for p in byp:
            m1, m2 = mean_depth(byp[p], set(half1)), mean_depth(byp[p], set(half2))
            if not (np.isnan(m1) or np.isnan(m2)):
                pg.append(m1 - m2)
        if len(pg) < 3:
            continue
        negc["n_tested"] += 1
        boots = []
        for _ in range(2000):
            bg = []
            for p in byp:
                h1 = [half1[i] for i in rng.integers(0, len(half1), len(half1))]
                h2 = [half2[i] for i in rng.integers(0, len(half2), len(half2))]
                v1 = [v for a in h1 for v in byp[p].get(a, [])]
                v2 = [v for a in h2 for v in byp[p].get(a, [])]
                if v1 and v2:
                    bg.append(np.mean(v1) - np.mean(v2))
            if bg:
                boots.append(np.mean(bg))
        split_art = float(np.std(boots, ddof=1)) if len(boots) > 1 else float("inf")
        if abs(np.mean(pg)) > SNR_K * max(float(np.std(pg, ddof=1)), split_art):
            negc["n_pseudo_resolved"] += 1
    out["negative_control_class_stratified"] = negc
    out["summary"] = {"n_ok": n_ok, "resolved_primary": n_res_primary,
                      "resolved_nested": n_res_nested}
    out["negative_control_nested"] = neg
    return out


def rc1_analysis(recs) -> dict:
    out = {}
    # Stage-1 accuracy per regime
    for regime in ("up", "tie"):
        f = DATA_DIR / f"stage1_rc1_{regime}.jsonl"
        if not f.exists():
            continue
        rows = load_records(f)
        by_rung = defaultdict(list)
        for r in rows:
            if r["rung_pred"] == "TIE":
                continue  # tie regime: flagged items excluded per spec
            by_rung[r["rung_truth"]].append(1 if r["rung_pred"] == r["rung_truth"] else 0)
        macro = float(np.mean([np.mean(v) for v in by_rung.values()])) if by_rung else float("nan")
        ties = sum(1 for r in rows if r["rung_pred"] == "TIE")
        out[f"stage1_{regime}"] = {"macro": round(macro, 4), "n": len(rows), "ties_flagged": ties}
    # Stage-2 gap summary per regime
    named = [r for r in recs if not r.get("sentinel") and r.get("arm") == "named"]
    pairs = sorted({r["op_pair"] for r in named})
    for regime in ("up", "tie"):
        f = DATA_DIR / f"stage2_rc1_{regime}.jsonl"
        if not f.exists():
            continue
        rr = load_records(f)
        # rebuild depths with the regime's rungs
        d: dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        ties = 0
        for r in rr:
            if r["rung_pred"] == "TIE":
                ties += 1
                continue
            v = DEPTH.get(r["rung_pred"])
            if v is not None:
                d[(r["org"], r["channel"])][r["op_pair"]][r["artifact_id"]].append(v)
        orgs = sorted({r["org"] for r in rr})
        gap_hats, n_resolved = [], 0
        for org in orgs:
            gaps = gaps_from_depths(d, pairs, org)
            if len(gaps) < 3:
                continue
            g = np.array(list(gaps.values()))
            gap_hat, floor = float(np.mean(g)), float(np.std(g, ddof=1))
            gap_hats.append(gap_hat)
            if abs(gap_hat) > SNR_K * floor:
                n_resolved += 1
        out[f"stage2_{regime}"] = {
            "n_ok": len(gap_hats), "mean_gap": round(float(np.mean(gap_hats)), 4) if gap_hats else None,
            "median_gap": round(float(np.median(gap_hats)), 4) if gap_hats else None,
            "n_positive": int(sum(1 for g in gap_hats if g > 0)),
            "n_resolved": n_resolved, "ties_flagged": ties, "n_reread": len(rr),
        }
    return out


def main() -> int:
    recs = load_all_stage2()
    results = {"seed": SEED,
               "amendment": "PL0 v1.2 post-campaign (labeled post hoc; primary analysis unchanged)",
               "nested_floor": nested_floor_analysis(recs),
               "rc1_sensitivity": rc1_analysis(recs)}
    (DATA_DIR / "pl4_posthoc_results.json").write_text(json.dumps(results, indent=2))
    print(json.dumps({"nested_summary": results["nested_floor"]["summary"],
                      "negative_control_nested": results["nested_floor"]["negative_control_nested"],
                      "rc1": results["rc1_sensitivity"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
