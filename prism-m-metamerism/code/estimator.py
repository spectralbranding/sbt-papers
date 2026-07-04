#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26", "scipy>=1.12", "pyyaml>=6.0"]
# ///
"""estimator.py — PRISM-M PL4 metameric-fraction estimator (2026az).

Deterministic, seeded (SEED = 20260702). Implements the frozen PL0 criteria
(research/prism_m/PREREGISTRATION.md section 6):

- readout value per (brand, op_pair): mean over channel draws
- distances: full readout = 1 - cosine similarity between eight-dimension
  brand vectors (2026ax); aggregators = |a - b| on the normalized scalar
- operator floor per brand per readout: max pairwise distance among the
  brand's per-op-pair values (dispersion across cross-family alt-pairs);
  pair floor = max(floor_a, floor_b), lower-bounded by FLOOR_MIN
- S/N per pair per readout = distance / pair floor
- resolved on a readout iff S/N > k (pre-registered k = 2)
- metameric under aggregator T iff resolved on full AND S/N_T < 1
- metameric_fraction(T) = |metameric under T| / |resolved on full|
- source-cluster bootstrap: brands are the clusters; resample brands with
  replacement, recompute floors/distances/fractions per replicate;
  percentile 95% CI
- H1: exists a pair whose bootstrap (channel-resampled) full-readout S/N
  lower bound > 2 AND aggregator S/N upper bound < 1
- H2: fraction(A-SCORE) > fraction(A-RANK) > fraction(full = 0);
  McNemar exact on paired pair-level outcomes (score vs rank) +
  exact binomial for fraction(rank) > 0, Holm-corrected, alpha = .017
- H3: per-op-pair fractions (leave-one-op-pair-out floors); dispersion =
  max pairwise |f_i - f_j|; supported if dispersion <= the pooled
  fraction's bootstrap 95% half-width (2026ay no-rescue logic)
- controls: negative = same-brand cross-channel pseudo-pair must NOT be
  resolved-distinct; positive = planted scalar-equal profile-distinct pair
  MUST flag metameric
- robustness: k in {1.5, 2, 3}; Euclidean and Mahalanobis full-readout
  distance alternates; prompt-ablation subsample comparison

Run:
    uv run python research/prism_m/code/estimator.py \
        --stage2 research/prism_m/data/stage2_records.jsonl \
        --out research/prism_m/data/pl4_results.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

DIMENSIONS = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
]
SEED = 20260702
FLOOR_MIN = 1e-3
K_DEFAULT = 2.0
N_BOOT = 2000
AGGREGATORS = ("score", "rank", "pick")


# ---------------------------------------------------------------------------
# Data shaping
# ---------------------------------------------------------------------------
def index_records(records: list[dict]) -> dict:
    """-> data[brand][readout][op_pair][channel] = value (list for repeats)."""
    data: dict = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    )
    meta: dict = {}
    for r in records:
        if r.get("flagged_malformed") or r.get("value") is None:
            continue
        if r.get("prompt_variant", "main") != "main":
            continue
        data[r["brand"]][r["readout"]][r["op_pair"]][r["channel"]].append(r["value"])
        meta[r["brand"]] = {
            "coherence_type": r.get("coherence_type"),
            "sector": r.get("sector"),
            "goods_type": r.get("goods_type"),
        }
    return {"data": data, "meta": meta}


def brand_value(data, brand, readout, op_pair, channels=None):
    """Mean over channel draws for one (brand, readout, op_pair)."""
    chans = data[brand][readout][op_pair]
    keys = channels if channels is not None else sorted(chans)
    vals = [v for c in keys for v in chans.get(c, [])]
    if not vals:
        return None
    arr = np.asarray(vals, dtype=float)
    return arr.mean(axis=0)


def dist_full(a, b, metric="cosine", vi=None):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if metric == "cosine":
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na == 0 or nb == 0:
            return 1.0
        return float(1.0 - np.dot(a, b) / (na * nb))
    if metric == "euclidean":
        return float(np.linalg.norm(a - b) / np.sqrt(len(a) * 100.0))
    if metric == "mahalanobis":
        d = a - b
        return float(np.sqrt(d @ vi @ d) / np.sqrt(len(a)))
    raise ValueError(metric)


def dist_scalar(a, b):
    return float(abs(float(a) - float(b)))


# ---------------------------------------------------------------------------
# Floors
# ---------------------------------------------------------------------------
def operator_floor(data, brand, readout, op_pairs, metric="cosine", vi=None):
    """Max pairwise distance among the brand's per-op-pair values."""
    vals = []
    for op in op_pairs:
        v = brand_value(data, brand, readout, op)
        if v is not None:
            vals.append(v)
    if len(vals) < 2:
        return FLOOR_MIN
    dists = []
    for x, y in itertools.combinations(vals, 2):
        if readout == "dims":
            dists.append(dist_full(x, y, metric, vi))
        else:
            dists.append(dist_scalar(x, y))
    return max(max(dists), FLOOR_MIN)


def channel_floor(data, brand, readout, op_pairs, metric="cosine", vi=None):
    """Artifact floor: mean over op-pairs of the max pairwise distance among
    per-channel draws (used by the negative control)."""
    per_op = []
    for op in op_pairs:
        chans = data[brand][readout][op]
        vals = [
            (
                np.asarray(v, float).mean(axis=0)
                if readout == "dims"
                else float(np.mean(v))
            )
            for v in ([chans[c] for c in sorted(chans)])
            if v
        ]
        if len(vals) < 2:
            continue
        dists = []
        for x, y in itertools.combinations(vals, 2):
            dists.append(
                dist_full(x, y, metric, vi) if readout == "dims" else dist_scalar(x, y)
            )
        per_op.append(max(dists))
    return max(float(np.mean(per_op)) if per_op else FLOOR_MIN, FLOOR_MIN)


# ---------------------------------------------------------------------------
# Pair classification
# ---------------------------------------------------------------------------
def mahalanobis_vi(data, brands, op_pairs):
    vecs = []
    for b in brands:
        for op in op_pairs:
            v = brand_value(data, b, "dims", op)
            if v is not None:
                vecs.append(v)
    x = np.asarray(vecs, float)
    cov = np.cov(x.T) + np.eye(len(DIMENSIONS)) * 1e-6
    return np.linalg.inv(cov)


def classify_pairs(
    data,
    brands,
    op_pairs,
    *,
    k=K_DEFAULT,
    metric="cosine",
    vi=None,
    aggregators=AGGREGATORS,
    pair_list=None,
):
    """Per-pair S/N on each readout + metamer flags. Returns list of dicts."""
    floors = {
        b: {
            ro: operator_floor(data, b, ro, op_pairs, metric, vi)
            for ro in ("dims", *aggregators)
        }
        for b in brands
    }
    values = {
        b: {
            ro: brand_value_pooled(data, b, ro, op_pairs)
            for ro in ("dims", *aggregators)
        }
        for b in brands
    }
    pairs = (
        pair_list
        if pair_list is not None
        else list(itertools.combinations(sorted(brands), 2))
    )
    out = []
    for a, b in pairs:
        if values[a]["dims"] is None or values[b]["dims"] is None:
            continue
        row = {"pair": (a, b)}
        d_full = dist_full(values[a]["dims"], values[b]["dims"], metric, vi)
        floor_full = max(floors[a]["dims"], floors[b]["dims"])
        row["snr_full"] = d_full / floor_full
        row["resolved_full"] = row["snr_full"] > k
        for ro in aggregators:
            va, vb = values[a][ro], values[b][ro]
            if va is None or vb is None:
                row[f"snr_{ro}"] = None
                row[f"metameric_{ro}"] = None
                continue
            d = dist_scalar(va, vb)
            fl = max(floors[a][ro], floors[b][ro])
            row[f"snr_{ro}"] = d / fl
            row[f"metameric_{ro}"] = bool(
                row["resolved_full"] and row[f"snr_{ro}"] < 1.0
            )
        out.append(row)
    return out


def brand_value_pooled(data, brand, readout, op_pairs):
    vals = []
    for op in op_pairs:
        v = brand_value(data, brand, readout, op)
        if v is not None:
            vals.append(v)
    if not vals:
        return None
    return np.mean(np.asarray(vals, float), axis=0)


def metameric_fraction(pair_rows, aggregator):
    resolved = [r for r in pair_rows if r["resolved_full"]]
    if not resolved:
        return None, 0, 0
    met = [r for r in resolved if r.get(f"metameric_{aggregator}")]
    return len(met) / len(resolved), len(met), len(resolved)


# ---------------------------------------------------------------------------
# Bootstrap (source-cluster: brands are clusters)
# ---------------------------------------------------------------------------
def bootstrap_fractions(
    data,
    brands,
    op_pairs,
    *,
    k=K_DEFAULT,
    metric="cosine",
    vi=None,
    n_boot=N_BOOT,
    seed=SEED,
    aggregators=AGGREGATORS,
):
    rng = np.random.default_rng(seed)
    brands = sorted(brands)
    boots = {ro: [] for ro in aggregators}
    for _ in range(n_boot):
        sample = list(rng.choice(brands, size=len(brands), replace=True))
        uniq = sorted(set(sample))
        # pairs among distinct sampled brands, weighted by multiplicity
        counts = {b: sample.count(b) for b in uniq}
        rows = classify_pairs(
            data,
            uniq,
            op_pairs,
            k=k,
            metric=metric,
            vi=vi,
            aggregators=aggregators,
        )
        for ro in aggregators:
            num = den = 0
            for r in rows:
                a, b = r["pair"]
                w = counts[a] * counts[b]
                if r["resolved_full"]:
                    den += w
                    if r.get(f"metameric_{ro}"):
                        num += w
            boots[ro].append(num / den if den else np.nan)
    ci = {}
    for ro in aggregators:
        arr = np.asarray([x for x in boots[ro] if not np.isnan(x)])
        ci[ro] = (
            (float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5)))
            if len(arr)
            else (None, None)
        )
    return ci


def bootstrap_pair_snr(
    data,
    a,
    b,
    op_pairs,
    *,
    readouts,
    metric="cosine",
    vi=None,
    n_boot=N_BOOT,
    seed=SEED,
):
    """Channel-resampled bootstrap of a single pair's S/N per readout
    (floors recomputed across op-pairs per replicate). For H1 CIs."""
    rng = np.random.default_rng(seed)
    out = {ro: [] for ro in readouts}
    channels = {
        br: sorted(set().union(*[set(data[br]["dims"][op]) for op in op_pairs]))
        for br in (a, b)
    }
    for _ in range(n_boot):
        ch = {
            br: list(rng.choice(channels[br], size=len(channels[br]), replace=True))
            for br in (a, b)
        }
        for ro in readouts:
            vals, floors = {}, {}
            ok = True
            for br in (a, b):
                per_op = []
                for op in op_pairs:
                    v = brand_value(data, br, ro, op, channels=ch[br])
                    if v is not None:
                        per_op.append(v)
                if len(per_op) < 1:
                    ok = False
                    break
                vals[br] = np.mean(np.asarray(per_op, float), axis=0)
                if len(per_op) >= 2:
                    ds = [
                        (
                            dist_full(x, y, metric, vi)
                            if ro == "dims"
                            else dist_scalar(x, y)
                        )
                        for x, y in itertools.combinations(per_op, 2)
                    ]
                    floors[br] = max(max(ds), FLOOR_MIN)
                else:
                    floors[br] = FLOOR_MIN
            if not ok:
                continue
            d = (
                dist_full(vals[a], vals[b], metric, vi)
                if ro == "dims"
                else dist_scalar(vals[a], vals[b])
            )
            out[ro].append(d / max(floors[a], floors[b]))
    return {
        ro: (
            (
                float(np.percentile(v, 2.5)),
                float(np.percentile(v, 97.5)),
            )
            if v
            else (None, None)
        )
        for ro, v in out.items()
    }


# ---------------------------------------------------------------------------
# Hypothesis tests
# ---------------------------------------------------------------------------
def test_h1(data, pair_rows, op_pairs, *, metric="cosine", vi=None, seed=SEED):
    """H1 supported if >= 1 metameric pair (any aggregator in the H2 ladder,
    primary = score) has bootstrap full-S/N lower bound > 2 AND aggregator
    S/N upper bound < 1."""
    supported_pairs = []
    candidates = [
        r for r in pair_rows if r.get("metameric_score") or r.get("metameric_rank")
    ]
    for r in candidates:
        a, b = r["pair"]
        ci = bootstrap_pair_snr(
            data,
            a,
            b,
            op_pairs,
            readouts=("dims", "score", "rank"),
            metric=metric,
            vi=vi,
            seed=seed,
        )
        rec = {"pair": [a, b], "snr_ci": ci}
        for agg in ("score", "rank"):
            lo_full = ci["dims"][0]
            hi_agg = ci[agg][1]
            if (
                r.get(f"metameric_{agg}")
                and lo_full is not None
                and hi_agg is not None
                and lo_full > K_DEFAULT
                and hi_agg < 1.0
            ):
                rec.setdefault("confirmed_under", []).append(agg)
        if rec.get("confirmed_under"):
            supported_pairs.append(rec)
    return {"supported": bool(supported_pairs), "pairs": supported_pairs}


def holm(pvals: dict) -> dict:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    adj, running = {}, 0.0
    for i, (k_, p) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))
        adj[k_] = running
    return adj


def test_h2(pair_rows, alpha=0.017):
    """Ladder fraction(score) > fraction(rank) > fraction(full)=0.
    (a) McNemar exact on paired metamer outcomes score vs rank;
    (b) exact binomial for fraction(rank) > 0."""
    resolved = [r for r in pair_rows if r["resolved_full"]]
    both = [
        r
        for r in resolved
        if r.get("metameric_score") is not None and r.get("metameric_rank") is not None
    ]
    n01 = sum(1 for r in both if r["metameric_score"] and not r["metameric_rank"])
    n10 = sum(1 for r in both if r["metameric_rank"] and not r["metameric_score"])
    n_disc = n01 + n10
    p_mcnemar = (
        float(stats.binomtest(n01, n_disc, 0.5, alternative="greater").pvalue)
        if n_disc
        else 1.0
    )
    n_rank_met = sum(1 for r in both if r["metameric_rank"])
    # exact binomial vs a nominal floor-consistent null rate of 0 -> any
    # occurrence rejects; report the count and a conservative p vs p0=.01
    p_rank_gt0 = (
        float(
            stats.binomtest(n_rank_met, len(both), 0.01, alternative="greater").pvalue
        )
        if both
        else 1.0
    )
    adj = holm({"score_gt_rank": p_mcnemar, "rank_gt_full": p_rank_gt0})
    return {
        "n_resolved": len(resolved),
        "n01_score_only": n01,
        "n10_rank_only": n10,
        "p_score_gt_rank": p_mcnemar,
        "p_rank_gt_full": p_rank_gt0,
        "holm_adjusted": adj,
        "supported": all(v < alpha for v in adj.values()),
    }


def test_h3(
    data,
    brands,
    op_pairs,
    *,
    k=K_DEFAULT,
    metric="cosine",
    vi=None,
    aggregator="score",
    pooled_ci=None,
):
    """Per-op-pair fractions with leave-one-op-pair-out floors; dispersion vs
    pooled bootstrap 95% half-width."""
    per_op = {}
    for held in op_pairs:
        others = [o for o in op_pairs if o != held]
        floors = {
            b: {
                ro: operator_floor(data, b, ro, others, metric, vi)
                for ro in ("dims", aggregator)
            }
            for b in brands
        }
        rows = []
        for a, b in itertools.combinations(sorted(brands), 2):
            va = brand_value(data, a, "dims", held)
            vb = brand_value(data, b, "dims", held)
            sa = brand_value(data, a, aggregator, held)
            sb = brand_value(data, b, aggregator, held)
            if any(x is None for x in (va, vb, sa, sb)):
                continue
            snr_f = dist_full(va, vb, metric, vi) / max(
                floors[a]["dims"], floors[b]["dims"]
            )
            snr_a = dist_scalar(sa, sb) / max(
                floors[a][aggregator], floors[b][aggregator]
            )
            rows.append((snr_f > k, snr_f > k and snr_a < 1.0))
        den = sum(1 for r in rows if r[0])
        num = sum(1 for r in rows if r[1])
        per_op[held] = num / den if den else None
    fr = [v for v in per_op.values() if v is not None]
    dispersion = (
        max(abs(x - y) for x, y in itertools.combinations(fr, 2))
        if len(fr) > 1
        else 0.0
    )
    half_width = (
        (pooled_ci[1] - pooled_ci[0]) / 2.0
        if pooled_ci and None not in pooled_ci
        else None
    )
    return {
        "per_op_pair_fraction": per_op,
        "dispersion": dispersion,
        "pooled_ci_half_width": half_width,
        "supported": (half_width is not None and dispersion <= half_width),
    }


# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------
def negative_control(data, brands, op_pairs, *, k=K_DEFAULT, metric="cosine", vi=None):
    """Pre-registered wording (PL0 section 5 / scaffold Controls): a same-brand
    two-artifact-draw pseudo-pair must NOT be flagged METAMERIC. Operationalized
    over same-brand cross-channel pseudo-pairs (values pooled over op-pairs):
    flagged iff full-readout S/N > k AND scalar S/N < 1 against the brand's own
    operator floors. Also reports the stricter resolved-distinct rate as a
    diagnostic (channel facets may legitimately carry signal)."""
    flags, resolved_only = [], 0
    n_tested = 0
    for b in brands:
        fl_dims = operator_floor(data, b, "dims", op_pairs, metric, vi)
        fl_sc = operator_floor(data, b, "score", op_pairs, metric, vi)
        chans = sorted(set().union(*[set(data[b]["dims"][op]) for op in op_pairs]))
        for c1, c2 in itertools.combinations(chans, 2):
            v1 = [brand_value(data, b, "dims", op, channels=[c1]) for op in op_pairs]
            v2 = [brand_value(data, b, "dims", op, channels=[c2]) for op in op_pairs]
            s1 = [brand_value(data, b, "score", op, channels=[c1]) for op in op_pairs]
            s2 = [brand_value(data, b, "score", op, channels=[c2]) for op in op_pairs]
            v1 = [x for x in v1 if x is not None]
            v2 = [x for x in v2 if x is not None]
            s1 = [x for x in s1 if x is not None]
            s2 = [x for x in s2 if x is not None]
            if not (v1 and v2 and s1 and s2):
                continue
            n_tested += 1
            d_f = dist_full(
                np.mean(np.asarray(v1, float), axis=0),
                np.mean(np.asarray(v2, float), axis=0),
                metric,
                vi,
            )
            d_s = dist_scalar(float(np.mean(s1)), float(np.mean(s2)))
            snr_f = d_f / fl_dims
            snr_s = d_s / max(fl_sc, FLOOR_MIN)
            if snr_f > k:
                resolved_only += 1
                if snr_s < 1.0:
                    flags.append(
                        {
                            "brand": b,
                            "channels": [c1, c2],
                            "snr_full": snr_f,
                            "snr_scalar": snr_s,
                        }
                    )
    return {
        "passed": not flags,
        "n_tested": n_tested,
        "n_flagged_metameric": len(flags),
        "n_resolved_distinct_diagnostic": resolved_only,
        "flags": flags[:20],
    }


def positive_control(*, k=K_DEFAULT):
    """Planted pair: profiles distinct on a dimension the scalar weights to
    zero, scalar-equal. Runs the classifier on synthetic records; MUST flag."""
    # Import THIS suite's synthetic.py by file path: the flat name "synthetic"
    # exists in every PRISM suite, and a whole-repo pytest run may have a
    # sibling suite's copy cached in sys.modules at call time.
    import importlib.util as _ilu

    _p = Path(__file__).resolve().parent / "synthetic.py"
    _spec = _ilu.spec_from_file_location("prism_m_synthetic", _p)
    _syn = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_syn)
    planted_positive_records = _syn.planted_positive_records

    records = planted_positive_records()
    idx = index_records(records)
    data = idx["data"]
    brands = sorted(data)
    op_pairs = sorted({op for b in data for ro in data[b] for op in data[b][ro]})
    rows = classify_pairs(
        data, brands, op_pairs, k=k, pair_list=[("PLANT_A", "PLANT_B")]
    )
    flagged = bool(rows and rows[0].get("metameric_score"))
    return {
        "passed": flagged,
        "rows": [
            {k_: (v if not isinstance(v, tuple) else list(v)) for k_, v in r.items()}
            for r in rows
        ],
    }


# ---------------------------------------------------------------------------
# Exploratory suite (labelled exploratory per PL0 section 1; no protected alpha)
# ---------------------------------------------------------------------------
def operator_concordance(data, brands, op_pairs, *, metric="cosine", vi=None):
    """Per-op-pair-combination distance summary across brands (the diagnostic
    that localizes a deviant operator pair)."""
    sums = {}
    for a, b_ in itertools.combinations(op_pairs, 2):
        ds = []
        for br in brands:
            x = brand_value(data, br, "dims", a)
            y = brand_value(data, br, "dims", b_)
            if x is not None and y is not None:
                ds.append(dist_full(x, y, metric, vi))
        if ds:
            sums[f"{a}-{b_}"] = {
                "median": float(np.median(ds)),
                "max": float(np.max(ds)),
            }
    return sums


def leave_one_operator_out(records, *, k=K_DEFAULT, seed=SEED):
    """Symmetric sensitivity: re-run the full frozen analysis with each
    operator pair held out (floors + values recomputed on the remainder)."""
    all_ops = sorted({r["op_pair"] for r in records})
    out = {}
    for held in all_ops:
        subset = [r for r in records if r["op_pair"] != held]
        res = analyze(subset, k=k, seed=seed, skip_pair_boot=True)
        out[f"without_{held}"] = {
            "fractions": res["fractions"],
            "H2": res["H2"],
            "H3": res["H3"],
            "negative_control": {
                kk: vv for kk, vv in res["negative_control"].items() if kk != "flags"
            },
            "n_resolved": res["fractions"]["score"]["n_resolved"],
        }
    return out


def ablation_comparison(all_records, *, metric="cosine"):
    """Prompt-ablation robustness: per (brand, channel, op_pair) present in
    BOTH variants, the dims distance between main and ablated readings,
    reported relative to the brand's operator floor."""
    main = [r for r in all_records if r.get("prompt_variant", "main") == "main"]
    abl = [r for r in all_records if r.get("prompt_variant") == "ablated"]
    if not abl:
        return {"n": 0}
    m_idx = index_records(main)["data"]

    def cell(rows):
        d = {}
        for r in rows:
            if r["readout"] == "dims" and r.get("value") is not None:
                d[(r["brand"], r["channel"], r["op_pair"])] = np.asarray(
                    r["value"], float
                )
        return d

    a_cells = cell(abl)
    m_cells = cell(main)
    ops = sorted({r["op_pair"] for r in main})
    rel = []
    for key, av in a_cells.items():
        mv = m_cells.get(key)
        if mv is None:
            continue
        fl = operator_floor(m_idx, key[0], "dims", ops, metric)
        rel.append(dist_full(av, mv, metric) / fl)
    return {
        "n": len(rel),
        "median_shift_over_floor": float(np.median(rel)) if rel else None,
        "max_shift_over_floor": float(np.max(rel)) if rel else None,
        "share_within_floor": (
            float(np.mean([x <= 1.0 for x in rel])) if rel else None
        ),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def analyze(records, *, k=K_DEFAULT, metric="cosine", seed=SEED, skip_pair_boot=False):
    idx = index_records(records)
    data, meta = idx["data"], idx["meta"]
    brands = sorted(data)
    op_pairs = sorted({op for b in data for ro in data[b] for op in data[b][ro]})
    vi = mahalanobis_vi(data, brands, op_pairs) if metric == "mahalanobis" else None

    pair_rows = classify_pairs(data, brands, op_pairs, k=k, metric=metric, vi=vi)
    fractions = {}
    for ro in AGGREGATORS:
        f, num, den = metameric_fraction(pair_rows, ro)
        fractions[ro] = {"fraction": f, "n_metameric": num, "n_resolved": den}
    ci = bootstrap_fractions(
        data, brands, op_pairs, k=k, metric=metric, vi=vi, seed=seed
    )
    for ro in AGGREGATORS:
        fractions[ro]["ci95"] = ci[ro]

    h1 = (
        test_h1(data, pair_rows, op_pairs, metric=metric, vi=vi, seed=seed)
        if not skip_pair_boot
        else {"skipped": True}
    )
    h2 = test_h2(pair_rows)
    h3 = test_h3(
        data,
        brands,
        op_pairs,
        k=k,
        metric=metric,
        vi=vi,
        aggregator="score",
        pooled_ci=ci["score"],
    )
    neg = negative_control(data, brands, op_pairs, k=k, metric=metric, vi=vi)

    return {
        "seed": seed,
        "k": k,
        "metric": metric,
        "n_brands": len(brands),
        "op_pairs": op_pairs,
        "fractions": fractions,
        "H1": h1,
        "H2": h2,
        "H3": h3,
        "negative_control": neg,
        "pair_rows": [{**r, "pair": list(r["pair"])} for r in pair_rows],
        "meta": meta,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage2", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument(
        "--robustness",
        action="store_true",
        help="also run k in {1.5,3} and euclidean/mahalanobis",
    )
    args = ap.parse_args()

    records = []
    with open(args.stage2) as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    main_records = [r for r in records if r.get("prompt_variant", "main") == "main"]
    result = analyze(main_records)
    result["positive_control"] = positive_control()

    # exploratory suite (PL0 section 1: analyses not pre-registered are
    # exploratory and reported as such)
    idx = index_records(main_records)
    data, brands = idx["data"], sorted(idx["data"])
    ops = sorted({op for b in data for ro in data[b] for op in data[b][ro]})
    result["exploratory"] = {
        "operator_concordance": operator_concordance(data, brands, ops),
        "leave_one_operator_out": leave_one_operator_out(main_records),
        "prompt_ablation": ablation_comparison(records),
    }
    # full exploratory analysis on the concordant triplet (identified by the
    # leave-one-out table): the subset whose held-out variant maximizes
    # resolved pairs
    loo = result["exploratory"]["leave_one_operator_out"]
    best = max(loo, key=lambda k_: loo[k_]["n_resolved"])
    if loo[best]["n_resolved"] > 0:
        held = best.replace("without_", "")
        subset = [r for r in main_records if r["op_pair"] != held]
        result["exploratory"]["concordant_subset"] = {
            "held_out": held,
            "analysis": analyze(subset, seed=SEED),
        }

    if args.robustness:
        result["robustness"] = {}
        for k_alt in (1.5, 3.0):
            r = analyze(records, k=k_alt, skip_pair_boot=True)
            result["robustness"][f"k_{k_alt}"] = {
                "fractions": r["fractions"],
                "H2": r["H2"],
            }
        for m_alt in ("euclidean", "mahalanobis"):
            r = analyze(records, metric=m_alt, skip_pair_boot=True)
            result["robustness"][m_alt] = {
                "fractions": r["fractions"],
                "H2": r["H2"],
            }

    Path(args.out).write_text(json.dumps(result, indent=2, default=str))
    print(f"[pl4] written: {args.out}")
    for ro in AGGREGATORS:
        fr = result["fractions"][ro]
        print(
            f"  fraction({ro}) = {fr['fraction']} "
            f"({fr['n_metameric']}/{fr['n_resolved']}) CI95 {fr['ci95']}"
        )
    print(f"  H1 supported: {result['H1'].get('supported')}")
    print(f"  H2 supported: {result['H2'].get('supported')}")
    print(f"  H3 supported: {result['H3'].get('supported')}")
    print(f"  negative control passed: {result['negative_control']['passed']}")
    print(f"  positive control passed: {result['positive_control']['passed']}")


if __name__ == "__main__":
    main()
