#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26", "pyyaml>=6.0", "scipy>=1.11"]
# ///
"""estimator.py — PRISM-T PL4 estimator (2026ba).

Deterministic, seeded. Computes, from the parsed VE-1 record layer:
  - per-brand contemporaneous OPERATOR floor (cross-pair dispersion,
    post-exclusion) — the H1 baseline;
  - per-brand, per-ladder VERSION floor (max inter-rung pinned distance
    under the ladder's matched extractor);
  - H1: per version pair, S/N = mean-over-brands inter-version distance /
    mean-over-brands operator floor, with a seeded brand-cluster bootstrap
    95% CI; drift criterion CI_low > k (k = 2; sweep {1.5, 2, 3});
  - H3: the pre-registered two-set mean contrast (high-drift vs
    format-anchored) pooled over adjacent version pairs, paired over brands
    (one-sided t + bootstrap CI; per-dimension decomposition exploratory);
  - controls: negative (same-version run-2 distance within operator floor),
    positive (designated distant pair must exceed the floor);
  - H2 decomposition path (live drift − version floor = brand-signal
    estimate) — runs on any epoch with a live panel (VE-2+); on VE-1 the
    live panel coincides with the pinned capture by construction.
  - robustness: metric sweep (cosine / euclidean / mahalanobis-diagonal).

Fixed seed SEED = 20260702. Run:
    uv run python research/prism_t/code/estimator.py \
        --records research/prism_t/data/ve1_records.jsonl \
        --out research/prism_t/data/pl4_results.json --robustness
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats as sps

CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))
sys.path.insert(0, str(CODE_DIR.parents[1]))
from prism_core import stats as pstats  # noqa: E402
from prism_t_lib import (  # noqa: E402
    DIMENSIONS,
    H3_FORMAT_ANCHORED,
    H3_HIGH_DRIFT,
    SEED,
    load_config,
)

N_BOOT = 2000


# --- Reading assembly ----------------------------------------------------------


def brand_readings(records: list[dict]) -> dict:
    """index[(panel, brand, renderer, extractor, run)] -> mean 8-vector over
    channels (the brand reading), plus channel count for QC."""
    cells = defaultdict(list)
    for r in records:
        if r.get("dims") is None or r.get("flagged"):
            continue
        cells[
            (r["panel"], r["brand"], r["renderer"], r["extractor"], r.get("run", 1))
        ].append(np.asarray(r["dims"], float))
    return {k: np.mean(v, axis=0) for k, v in cells.items()}


def _reading(
    readings: dict, brand: str, renderer: str, extractor: str, *, panel="pinned", run=1
):
    return readings.get((panel, brand, renderer, extractor, run))


# --- Floors --------------------------------------------------------------------


def operator_floor_per_brand(
    readings: dict,
    op_pairs: dict,
    brands: list[str],
    *,
    excluded_ops: set[str] = frozenset(),
    metric: str = "cosine",
    vi=None,
) -> dict:
    """Per-brand contemporaneous operator floor: max pairwise distance among
    the (post-exclusion) operator-pair readings of the pinned panel."""
    floors = {}
    for b in brands:
        vecs = []
        for op_id, op in op_pairs.items():
            if op_id in excluded_ops:
                continue
            v = _reading(readings, b, op["renderer"]["model"], op["extractor"]["model"])
            if v is not None:
                vecs.append(v)
        if len(vecs) >= 2:
            floors[b] = pstats.max_pairwise_dispersion(
                vecs, lambda x, y: pstats.dist_full(x, y, metric, vi)
            )
    return floors


def version_distances(
    readings: dict,
    ladder: dict,
    brands: list[str],
    *,
    metric: str = "cosine",
    vi=None,
) -> dict:
    """d[(rung_i, rung_j)][brand] = pinned inter-version distance under the
    ladder's fixed extractor, for every rung pair (release order)."""
    ext = ladder["extractor"]["model"]
    rungs = [r["model"] for r in ladder["rungs"]]
    out: dict = {}
    for i in range(len(rungs)):
        for j in range(i + 1, len(rungs)):
            per_brand = {}
            for b in brands:
                vi_vec = _reading(readings, b, rungs[i], ext)
                vj_vec = _reading(readings, b, rungs[j], ext)
                if vi_vec is not None and vj_vec is not None:
                    per_brand[b] = pstats.dist_full(vi_vec, vj_vec, metric, vi)
            out[(rungs[i], rungs[j])] = per_brand
    return out


def version_floor_per_brand(vdists: dict, brands: list[str]) -> dict:
    """version_floor(brand) = max over rung pairs of the pinned distance."""
    floors = {}
    for b in brands:
        vals = [d[b] for d in vdists.values() if b in d]
        if vals:
            floors[b] = max(vals)
    return floors


# --- H1 -------------------------------------------------------------------------


def h1_snr(
    pair_dists: dict,
    op_floors: dict,
    *,
    seed: int = SEED,
) -> dict:
    """S/N for one version pair: mean-over-brands distance / mean-over-brands
    operator floor, brand-cluster bootstrap CI."""
    brands = sorted(set(pair_dists) & set(op_floors))
    if not brands:
        return {"n_brands": 0}

    def stat(sample):
        d = np.mean([pair_dists[b] for b in sample])
        f = np.mean([op_floors[b] for b in sample])
        return d / f if f > 0 else None

    lo, hi = pstats.cluster_bootstrap(brands, stat, n_boot=N_BOOT, seed=seed)
    point = stat(brands)
    return {
        "n_brands": len(brands),
        "mean_distance": float(np.mean([pair_dists[b] for b in brands])),
        "mean_operator_floor": float(np.mean([op_floors[b] for b in brands])),
        "snr": point,
        "ci95": [lo, hi],
    }


# --- H3 -------------------------------------------------------------------------


def per_dimension_drift(
    records: list[dict],
    ladder: dict,
    brands: list[str],
) -> dict:
    """drift[brand][dim] = mean |per-dimension delta| (0-10 scale) over the
    ladder's ADJACENT rung pairs, channel-mean readings."""
    readings = brand_readings(records)
    ext = ladder["extractor"]["model"]
    rungs = [r["model"] for r in ladder["rungs"]]
    out: dict = defaultdict(dict)
    for b in brands:
        deltas = []
        for i in range(len(rungs) - 1):
            v1 = _reading(readings, b, rungs[i], ext)
            v2 = _reading(readings, b, rungs[i + 1], ext)
            if v1 is not None and v2 is not None:
                deltas.append(np.abs(v2 - v1))
        if deltas:
            mean_delta = np.mean(deltas, axis=0)
            out[b] = {dim: float(mean_delta[k]) for k, dim in enumerate(DIMENSIONS)}
    return dict(out)


def h3_contrast(drift: dict, *, seed: int = SEED) -> dict:
    """Pre-registered two-set contrast: per brand, mean drift over the
    high-drift set minus mean over the format-anchored set; one-sided paired
    t over brands + brand-cluster bootstrap CI of the mean difference."""
    brands = sorted(drift)
    diffs = []
    for b in brands:
        hi = np.mean([drift[b][d] for d in H3_HIGH_DRIFT])
        lo_ = np.mean([drift[b][d] for d in H3_FORMAT_ANCHORED])
        diffs.append(hi - lo_)
    diffs = np.asarray(diffs)
    if len(diffs) < 3:
        return {"n_brands": len(diffs)}
    t, p_two = sps.ttest_1samp(diffs, 0.0)
    p_one = p_two / 2 if t > 0 else 1 - p_two / 2
    d_cohen = (
        float(np.mean(diffs) / np.std(diffs, ddof=1))
        if np.std(diffs, ddof=1) > 0
        else None
    )
    per_brand = dict(zip(brands, diffs.tolist()))

    def stat(sample):
        return float(np.mean([per_brand[b] for b in sample]))

    lo, hi = pstats.cluster_bootstrap(brands, stat, n_boot=N_BOOT, seed=seed)
    dim_means = {
        dim: float(np.mean([drift[b][dim] for b in brands])) for dim in DIMENSIONS
    }
    return {
        "n_brands": len(diffs),
        "mean_diff": float(np.mean(diffs)),
        "ci95": [lo, hi],
        "t": float(t),
        "p_one_sided": float(p_one),
        "cohen_d": d_cohen,
        "per_dimension_mean_drift": dim_means,  # exploratory decomposition
        "high_drift_set": H3_HIGH_DRIFT,
        "format_anchored_set": H3_FORMAT_ANCHORED,
    }


# --- H2 decomposition (live panel; VE-2+) ---------------------------------------


def h2_decomposition(
    records: list[dict],
    ladder: dict,
    brands: list[str],
    *,
    epoch_pair: tuple[str, str],
    seed: int = SEED,
    metric: str = "cosine",
) -> dict:
    """brand_signal(brand) = live inter-epoch drift − pinned version floor,
    under the ladder's top rung + matched extractor. Requires live-panel
    records at both epochs (VE-2+); on VE-1 alone this returns n_brands=0
    (live ≡ pinned at birth — PL0 §9.1)."""
    readings_by_epoch: dict = defaultdict(dict)
    for r in records:
        if r.get("dims") is None or r.get("flagged"):
            continue
        key = (r["panel"], r["epoch"], r["brand"], r["renderer"], r["extractor"])
        readings_by_epoch[key] = None  # marker; real assembly below
    # assemble channel-mean readings per (panel, epoch)
    cells = defaultdict(list)
    for r in records:
        if r.get("dims") is None or r.get("flagged"):
            continue
        cells[
            (r["panel"], r["epoch"], r["brand"], r["renderer"], r["extractor"])
        ].append(np.asarray(r["dims"], float))
    means = {k: np.mean(v, axis=0) for k, v in cells.items()}
    top = ladder["rungs"][-1]["model"]
    ext = ladder["extractor"]["model"]
    e1, e2 = epoch_pair
    live_drift, pinned_drift = {}, {}
    for b in brands:
        lv1 = means.get(("live", e1, b, top, ext))
        lv2 = means.get(("live", e2, b, top, ext))
        pv1 = means.get(("pinned", e1, b, top, ext))
        pv2 = means.get(("pinned", e2, b, top, ext))
        if lv1 is not None and lv2 is not None:
            live_drift[b] = pstats.dist_full(lv1, lv2, metric)
        if pv1 is not None and pv2 is not None:
            pinned_drift[b] = pstats.dist_full(pv1, pv2, metric)
    common = sorted(set(live_drift) & set(pinned_drift))
    if not common:
        return {"n_brands": 0, "note": "live panel needs two epochs (VE-2+)"}
    signal = {b: live_drift[b] - pinned_drift[b] for b in common}

    def stat(sample):
        return float(np.mean([signal[b] for b in sample]))

    lo, hi = pstats.cluster_bootstrap(common, stat, n_boot=N_BOOT, seed=seed)
    return {
        "n_brands": len(common),
        "mean_live_drift": float(np.mean([live_drift[b] for b in common])),
        "mean_pinned_version_floor": float(np.mean([pinned_drift[b] for b in common])),
        "mean_brand_signal": float(np.mean(list(signal.values()))),
        "ci95": [lo, hi],
    }


# --- Controls -------------------------------------------------------------------


def negative_control(
    records: list[dict],
    cfg: dict,
    brands: list[str],
    *,
    excluded_ops: set[str] = frozenset(),
    metric="cosine",
    vi=None,
) -> dict:
    """Same version, two runs: run-2 distance must sit within the operator
    floor (mean over brands; per-brand pass fraction reported). The floor is
    the post-exclusion floor — the same band every other test uses."""
    readings = brand_readings(records)
    neg = cfg["controls"]["negative"]
    rmodel, ext = neg["model"], neg["extractor"]["model"]
    op_floors = operator_floor_per_brand(
        readings,
        cfg["operator_pairs"],
        brands,
        excluded_ops=excluded_ops,
        metric=metric,
        vi=vi,
    )
    dists = {}
    for b in brands:
        v1 = _reading(readings, b, rmodel, ext, run=1)
        v2 = _reading(readings, b, rmodel, ext, run=2)
        if v1 is not None and v2 is not None:
            dists[b] = pstats.dist_full(v1, v2, metric, vi)
    common = sorted(set(dists) & set(op_floors))
    if not common:
        return {"n_brands": 0}
    within = [dists[b] <= op_floors[b] for b in common]
    return {
        "n_brands": len(common),
        "mean_rerun_distance": float(np.mean([dists[b] for b in common])),
        "mean_operator_floor": float(np.mean([op_floors[b] for b in common])),
        "pass_mean": float(np.mean([dists[b] for b in common]))
        <= float(np.mean([op_floors[b] for b in common])),
        "within_floor_fraction": float(np.mean(within)),
    }


# --- Orchestration ---------------------------------------------------------------


def analyze(
    records: list[dict],
    cfg: dict,
    *,
    excluded_ops: set[str] = frozenset(),
    metric: str = "cosine",
    snr_k: float = 2.0,
    seed: int = SEED,
) -> dict:
    readings = brand_readings(records)
    brands = sorted({r["brand"] for r in records})
    vi = None
    if metric == "mahalanobis":
        mat = np.array(
            [
                r["dims"]
                for r in records
                if r.get("dims") is not None and not r.get("flagged")
            ]
        )
        var = np.var(mat, axis=0, ddof=1)
        vi = np.diag(1.0 / np.maximum(var, 1e-6))
    op_floors = operator_floor_per_brand(
        readings,
        cfg["operator_pairs"],
        brands,
        excluded_ops=excluded_ops,
        metric=metric,
        vi=vi,
    )
    result: dict = {
        "metric": metric,
        "snr_k": snr_k,
        "excluded_ops": sorted(excluded_ops),
        "n_brands": len(brands),
        "operator_floor": {
            "mean": float(np.mean(list(op_floors.values()))) if op_floors else None,
            "median": float(np.median(list(op_floors.values()))) if op_floors else None,
            "max": float(np.max(list(op_floors.values()))) if op_floors else None,
        },
        "ladders": {},
    }
    pos = cfg["controls"]["positive"]
    for lname, ladder in cfg["ladders"].items():
        vd = version_distances(readings, ladder, brands, metric=metric, vi=vi)
        vf = version_floor_per_brand(vd, brands)
        pairs = {}
        for (ri, rj), dists in vd.items():
            r = h1_snr(dists, op_floors, seed=seed)
            r["drifts_at_k"] = (
                r.get("ci95", [None])[0] is not None and r["ci95"][0] > snr_k
            )
            adjacent = _is_adjacent(ladder, ri, rj)
            r["adjacent"] = adjacent
            r["positive_control"] = lname == pos["ladder"] and [ri, rj] == pos["pair"]
            pairs[f"{ri} -> {rj}"] = r
        drift = per_dimension_drift(records, ladder, brands)
        result["ladders"][lname] = {
            "extractor": ladder["extractor"]["model"],
            "version_floor": {
                "mean": float(np.mean(list(vf.values()))) if vf else None,
                "median": float(np.median(list(vf.values()))) if vf else None,
            },
            "pairs": pairs,
            "h3": h3_contrast(drift, seed=seed) if drift else {"n_brands": 0},
        }
    result["h1_supported"] = any(
        p["drifts_at_k"]
        for lad in result["ladders"].values()
        for p in lad["pairs"].values()
        if not p.get("positive_control")
    )
    result["negative_control"] = negative_control(
        records, cfg, brands, excluded_ops=excluded_ops, metric=metric, vi=vi
    )
    return result


def _is_adjacent(ladder: dict, ri: str, rj: str) -> bool:
    rungs = [r["model"] for r in ladder["rungs"]]
    return abs(rungs.index(ri) - rungs.index(rj)) == 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument(
        "--excluded-ops", default="", help="comma list from pilot, e.g. OP4"
    )
    ap.add_argument("--robustness", action="store_true")
    args = ap.parse_args()
    from prism_t_lib import load_records  # noqa: PLC0415

    records = load_records(Path(args.records))
    cfg = load_config()
    excluded = {s for s in args.excluded_ops.split(",") if s}
    out = {"primary": analyze(records, cfg, excluded_ops=excluded)}
    if args.robustness:
        out["robustness"] = {
            "k_sweep": {
                str(k): analyze(records, cfg, excluded_ops=excluded, snr_k=k)[
                    "h1_supported"
                ]
                for k in (1.5, 2.0, 3.0)
            },
            "euclidean": analyze(
                records, cfg, excluded_ops=excluded, metric="euclidean"
            ),
            "mahalanobis": analyze(
                records, cfg, excluded_ops=excluded, metric="mahalanobis"
            ),
        }
    Path(args.out).write_text(json.dumps(out, indent=2))
    print(f"[pl4] written -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
