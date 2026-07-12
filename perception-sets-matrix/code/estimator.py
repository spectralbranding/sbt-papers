#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26", "pyyaml>=6.0"]
# ///
"""estimator.py — seeded deterministic analysis for the 2026bf campaign.

Implements the FROZEN analysis rules (PROTOCOL.yaml `analysis:` +
PREREG_STUDY_DESIGN.md section 7): operator floors F1-F4; the primary
monotone-link test (Kendall tau_b over cohort x brand cells, within-cohort
brand-label permutation null, 10,000 draws, one-sided positive, pooled by
median over floor-passing operators with shared permutations); isotonic R^2;
the same-call common-method contrast delta-tau; the fluency auxiliary
delta-tau_w (paired cohort-level swap permutation, direction >= 0); the
induced-matrix layer (Study-2 pooled propensities -> (S, s) by moment
matching -> P = (I + S 1 s^T)/(S+1), double-jeopardy diagonal ordering vs
the descriptive switching probes); intermediate-band mass vs cohort-profile
dispersion; the frozen robustness list (cosine match, salience weights,
Spearman rho, leave-one-brand-out, leave-one-operator-out, Study-2 brand
fixed effects [which subsume brand-level familiarity/salience], random-
profile falsification); and the four kill-condition verdicts K1-K4.

Fixed seed 20260712. Run:
    uv run python code/estimator.py \
        --records 'data/records_*.jsonl' \
        --out data/results.json
"""

from __future__ import annotations

import argparse
import glob
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
PAPER_DIR = HERE.parent
SEED = 20260712
N_PERM = 10_000
DIMS = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
]


# ---------------------------------------------------------------------------
# Small stats kernel (no scipy dependency; deterministic)
# ---------------------------------------------------------------------------
def kendall_tau_b(x: np.ndarray, y: np.ndarray) -> float:
    n = len(x)
    if n < 2:
        return float("nan")
    conc = disc = tx = ty = 0
    for i in range(n - 1):
        dx = x[i + 1 :] - x[i]
        dy = y[i + 1 :] - y[i]
        s = np.sign(dx) * np.sign(dy)
        conc += int(np.sum(s > 0))
        disc += int(np.sum(s < 0))
        tx += int(np.sum((dx == 0) & (dy != 0)))
        ty += int(np.sum((dy == 0) & (dx != 0)))
    n0 = n * (n - 1) / 2
    both = n0 - conc - disc - tx - ty  # pairs tied on both
    n1 = conc + disc + ty + both
    n2 = conc + disc + tx + both
    denom = math.sqrt(n1 * n2) if n1 > 0 and n2 > 0 else 0.0
    return (conc - disc) / denom if denom else 0.0


def spearman_rho(x: np.ndarray, y: np.ndarray) -> float:
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    if rx.std() == 0 or ry.std() == 0:
        return 0.0
    return float(np.corrcoef(rx, ry)[0, 1])


def isotonic_fit(m: np.ndarray, p: np.ndarray) -> np.ndarray:
    """PAV isotonic regression of p on m; returns fitted values (m order)."""
    order = np.argsort(m, kind="stable")
    y = p[order].astype(float)
    w = np.ones_like(y)
    # pool adjacent violators
    vals = list(y)
    wts = list(w)
    idx = [[i] for i in range(len(y))]
    i = 0
    while i < len(vals) - 1:
        if vals[i] > vals[i + 1] + 1e-12:
            tot = wts[i] + wts[i + 1]
            vals[i] = (vals[i] * wts[i] + vals[i + 1] * wts[i + 1]) / tot
            wts[i] = tot
            idx[i] += idx[i + 1]
            del vals[i + 1], wts[i + 1], idx[i + 1]
            while i > 0 and vals[i - 1] > vals[i] + 1e-12:
                tot = wts[i - 1] + wts[i]
                vals[i - 1] = (vals[i - 1] * wts[i - 1] + vals[i] * wts[i]) / tot
                wts[i - 1] = tot
                idx[i - 1] += idx[i]
                del vals[i], wts[i], idx[i]
                i -= 1
        else:
            i += 1
    fitted_sorted = np.empty(len(y))
    for v, members in zip(vals, idx):
        for j in members:
            fitted_sorted[j] = v
    fitted = np.empty(len(y))
    fitted[order] = fitted_sorted
    return fitted


def icc_2_1(mat: np.ndarray) -> float:
    """ICC(2,1): rows = targets, cols = raters (replicates)."""
    n, k = mat.shape
    if n < 2 or k < 2:
        return float("nan")
    row_m = mat.mean(axis=1)
    col_m = mat.mean(axis=0)
    grand = mat.mean()
    msr = k * np.sum((row_m - grand) ** 2) / (n - 1)
    msc = n * np.sum((col_m - grand) ** 2) / (k - 1)
    mse = (np.sum((mat - row_m[:, None] - col_m[None, :] + grand) ** 2)) / (
        (n - 1) * (k - 1)
    )
    denom = msr + (k - 1) * mse + k * (msc - mse) / n
    return float((msr - mse) / denom) if denom else float("nan")


# ---------------------------------------------------------------------------
# Match statistics
# ---------------------------------------------------------------------------
D_MAX = 9 * math.sqrt(8)


def match_euclid(theta: np.ndarray, beta: np.ndarray) -> float:
    return 1 - float(np.linalg.norm(theta - beta)) / D_MAX


def match_weighted(theta: np.ndarray, beta: np.ndarray, w: np.ndarray) -> float:
    return 1 - math.sqrt(float(np.sum(w * (theta - beta) ** 2))) / 9.0


def match_cosine(theta: np.ndarray, beta: np.ndarray) -> float:
    return float(np.dot(theta, beta) / (np.linalg.norm(theta) * np.linalg.norm(beta)))


# ---------------------------------------------------------------------------
# Record aggregation
# ---------------------------------------------------------------------------
def load_all(records_glob: str) -> dict:
    ops: dict = defaultdict(
        lambda: {
            "floors": defaultdict(list),
            "validate": defaultdict(list),
            "cohorts": {},
            "readings": defaultdict(list),
            "eliciting": defaultdict(list),
            "samecall": {},
            "n_failed": 0,
            "n_total": 0,
            "n_elicit_ok": 0,
            "n_elicit_fail": 0,
        }
    )
    for path in sorted(glob.glob(records_glob)):
        for line in Path(path).read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            o = ops[r["operator"]]
            o["n_total"] += 1
            if r.get("failed"):
                o["n_failed"] += 1
                if r["arm"] == "eliciting":
                    o["n_elicit_fail"] += 1
                continue
            arm = r["arm"]
            if arm == "floors":
                o["floors"][r["brand"]].append(r["payload"])
            elif arm == "validate":
                o["validate"][r["brand_id"]].append(r["payload"])
            elif arm == "cohorts":
                o["cohorts"][r["cohort_id"]] = r["payload"]
            elif arm == "readings":
                o["readings"][(r["category"], r["brand"])].append(r["payload"])
            elif arm == "eliciting":
                o["eliciting"][(r["category"], r["cohort_id"])].append(r)
                o["n_elicit_ok"] += 1
            elif arm == "samecall":
                o["samecall"][(r["category"], r["cohort_id"])] = r["payload"]
    return dict(ops)


# ---------------------------------------------------------------------------
# Floors
# ---------------------------------------------------------------------------
def compute_floors(op_data: dict, proto: dict, s1_targets: dict) -> dict:
    """F1 from the operator's own repeated brand readings (all categories);
    F3 from Study-1 pack means vs the AUTHORED targets — the only ground
    truth that exists by construction (the canonical corpus profiles are
    illustrative, not measurements, and are not used; pre-freeze correction
    2026-07-12)."""
    # F1: targets = (brand x dim) rows, raters = replicates
    rows = []
    for reps in op_data["readings"].values():
        if len(reps) >= 2:
            take = min(len(reps), 3)
            if take == 3 or not rows:
                rows.append(np.array(reps[:take]).T)  # 8 x take
    icc = float("nan")
    rows = [r for r in rows if r.shape[1] == 3]
    if len(rows) >= 3:
        icc = icc_2_1(np.vstack(rows))
    # F3: mean over Study-1 packs of per-pack MAD vs authored target
    mads = []
    for bname, target in s1_targets.items():
        reps = op_data["readings"].get(("coffee_roasters", bname), [])
        if reps:
            mean_read = np.array(reps).mean(axis=0)
            mads.append(float(np.mean(np.abs(mean_read - target))))
    f3 = float(np.mean(mads)) if mads else float("nan")
    # F2: sum-check rate + juster agreement
    n_ok, n_fail = op_data["n_elicit_ok"], op_data["n_elicit_fail"]
    f2_rate = n_ok / (n_ok + n_fail) if (n_ok + n_fail) else float("nan")
    taus = []
    for recs in op_data["eliciting"].values():
        for r in recs:
            cs = r["payload"]["constant_sum"]
            ju = r["payload"]["juster"]
            names = list(cs)
            t = kendall_tau_b(
                np.array([cs[n] for n in names], dtype=float),
                np.array([ju[n] for n in names], dtype=float),
            )
            if not math.isnan(t):
                taus.append(t)
    f2_tau = float(np.median(taus)) if taus else float("nan")
    # F4
    f4 = (
        op_data["n_failed"] / op_data["n_total"] if op_data["n_total"] else float("nan")
    )
    fl = proto["floors"]
    passes = {
        "F1": bool(icc >= fl["F1_icc_min"]) if not math.isnan(icc) else False,
        "F2": (
            bool(
                f2_rate >= fl["F2_sumcheck_rate"] and f2_tau >= fl["F2_juster_tau_min"]
            )
            if not (math.isnan(f2_rate) or math.isnan(f2_tau))
            else False
        ),
        "F3": bool(f3 <= fl["F3_mad_max"]) if not math.isnan(f3) else False,
        "F4": bool(f4 <= fl["F4_failure_rate_max"]) if not math.isnan(f4) else False,
    }
    return {
        "F1_icc": None if math.isnan(icc) else round(icc, 3),
        "F2_sumcheck_rate": None if math.isnan(f2_rate) else round(f2_rate, 3),
        "F2_juster_tau": None if math.isnan(f2_tau) else round(f2_tau, 3),
        "F3_mad": None if math.isnan(f3) else round(f3, 3),
        "F4_failure_rate": None if math.isnan(f4) else round(f4, 4),
        "passes": passes,
        "pass_all": all(passes.values()),
    }


# ---------------------------------------------------------------------------
# Cell tables
# ---------------------------------------------------------------------------
def cell_tables(
    op_data: dict, cat: str, personas: list[dict], brands: list[str]
) -> dict | None:
    """Per-operator cohort x brand tables: m (designed theta vs measured beta),
    m_w, m_cos, p (median constant-sum share), plus same-call variants."""
    betas = {}
    for b in brands:
        reps = op_data["readings"].get((cat, b), [])
        if not reps:
            return None
        betas[b] = np.median(np.array(reps), axis=0)
    K, B = len(personas), len(brands)
    m = np.zeros((K, B))
    m_w = np.zeros((K, B))
    m_cos = np.zeros((K, B))
    p = np.full((K, B), np.nan)
    for ki, c in enumerate(personas):
        theta = np.array(c["profile"])
        w = np.array(c["salience_weights"])
        recs = op_data["eliciting"].get((cat, c["cohort_id"]), [])
        shares = defaultdict(list)
        for r in recs:
            for b, v in r["payload"]["constant_sum"].items():
                shares[b].append(v / 10.0)
        for bi, b in enumerate(brands):
            beta = betas[b]
            m[ki, bi] = match_euclid(theta, beta)
            m_w[ki, bi] = match_weighted(theta, beta, w)
            m_cos[ki, bi] = match_cosine(theta, beta)
            if shares.get(b):
                p[ki, bi] = float(np.median(shares[b]))
    if np.isnan(p).any():
        # listwise per cell: drop cohorts with any missing cell
        keep = ~np.isnan(p).any(axis=1)
        m, m_w, m_cos, p = m[keep], m_w[keep], m_cos[keep], p[keep]
        personas = [c for c, k in zip(personas, keep) if k]
    # same-call tables
    sc_m, sc_p = [], []
    for c in personas:
        payload = op_data["samecall"].get((cat, c["cohort_id"]))
        if not payload:
            continue
        theta = np.array(c["profile"])
        row_m, row_p = [], []
        for b in brands:
            if b not in payload["readings"]:
                row_m = []
                break
            row_m.append(match_euclid(theta, np.array(payload["readings"][b])))
            row_p.append(payload["constant_sum"][b] / 10.0)
        if row_m:
            sc_m.append(row_m)
            sc_p.append(row_p)
    return {
        "m": m,
        "m_w": m_w,
        "m_cos": m_cos,
        "p": p,
        "sc_m": np.array(sc_m) if sc_m else None,
        "sc_p": np.array(sc_p) if sc_p else None,
        "betas": {b: betas[b].tolist() for b in brands},
        "n_cohorts": m.shape[0],
    }


def perm_null_pooled(
    ms: list[np.ndarray],
    ps: list[np.ndarray],
    rng: np.random.Generator,
    n_perm: int = N_PERM,
) -> tuple[float, np.ndarray]:
    """Observed pooled tau (median over operators) + shared-permutation null."""
    obs = float(
        np.median([kendall_tau_b(m.ravel(), p.ravel()) for m, p in zip(ms, ps)])
    )
    K, B = ms[0].shape
    null = np.empty(n_perm)
    for t in range(n_perm):
        perm_rows = [rng.permutation(B) for _ in range(K)]
        taus = []
        for m, p in zip(ms, ps):
            p_perm = np.vstack([p[k, perm_rows[k]] for k in range(K)])
            taus.append(kendall_tau_b(m.ravel(), p_perm.ravel()))
        null[t] = np.median(taus)
    return obs, null


def one_sided_p(obs: float, null: np.ndarray) -> float:
    return float((1 + np.sum(null >= obs)) / (1 + len(null)))


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------
def analyze(records_glob: str, out_path: str, n_perm: int = N_PERM) -> dict:
    rng = np.random.default_rng(SEED)
    proto = yaml.safe_load((PAPER_DIR / "PROTOCOL.yaml").read_text())
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
    ops_data = load_all(records_glob)
    op_ids = sorted(ops_data)

    results: dict = {
        "seed": SEED,
        "n_permutations": n_perm,
        "operators": {},
        "categories": {},
    }

    s1_targets = {b["name"]: np.array(b["target_profile"]) for b in s1["brands"]}
    floors = {op: compute_floors(ops_data[op], proto, s1_targets) for op in op_ids}
    results["operators"] = floors
    passing = [op for op in op_ids if floors[op]["pass_all"]]
    results["floor_passing_operators"] = passing
    results["K4_instrument_failure"] = len(passing) < len(op_ids) / 2

    fam = {o["id"]: o["family"] for o in proto["operators"] + proto["reserves"]}
    alpha = proto["analysis"]["alpha"]
    tau_floor = proto["analysis"]["tau_floor"]

    category_pass = {}
    family_taus: dict = defaultdict(list)
    study2_bands = []

    for cat, brands in cat_brands.items():
        personas = personas_all[cat]
        tables = {}
        for op in passing:
            t = cell_tables(ops_data[op], cat, personas, brands)
            if t is not None and t["n_cohorts"] >= 5:
                tables[op] = t
        if not tables:
            results["categories"][cat] = {"error": "no usable operator tables"}
            continue
        t_ops = sorted(tables)
        ms = [tables[o]["m"] for o in t_ops]
        ps = [tables[o]["p"] for o in t_ops]

        per_op_tau = {
            o: round(kendall_tau_b(tables[o]["m"].ravel(), tables[o]["p"].ravel()), 3)
            for o in t_ops
        }
        obs, null = perm_null_pooled(
            ms, ps, np.random.default_rng(SEED + hash(cat) % 1000), n_perm
        )
        p_val = one_sided_p(obs, null)

        # isotonic R^2 on pooled cells
        m_all = np.concatenate([m.ravel() for m in ms])
        p_all = np.concatenate([p.ravel() for p in ps])
        fitted = isotonic_fit(m_all, p_all)
        ss_res = float(np.sum((p_all - fitted) ** 2))
        ss_tot = float(np.sum((p_all - p_all.mean()) ** 2))
        r2 = 1 - ss_res / ss_tot if ss_tot else float("nan")

        # same-call contrast
        sc_taus, sep_taus_scops = [], []
        for o in t_ops:
            t = tables[o]
            if t["sc_m"] is not None and len(t["sc_m"]) >= 5:
                sc_taus.append(kendall_tau_b(t["sc_m"].ravel(), t["sc_p"].ravel()))
                sep_taus_scops.append(kendall_tau_b(t["m"].ravel(), t["p"].ravel()))
        tau_same = float(np.median(sc_taus)) if sc_taus else float("nan")
        delta_tau = (
            tau_same - float(np.median(sep_taus_scops)) if sc_taus else float("nan")
        )

        # fluency auxiliary: paired cohort-level swap permutation
        def pooled_delta(ms_u, ms_w, ps_):
            tu = np.median(
                [kendall_tau_b(a.ravel(), p.ravel()) for a, p in zip(ms_u, ps_)]
            )
            tw = np.median(
                [kendall_tau_b(a.ravel(), p.ravel()) for a, p in zip(ms_w, ps_)]
            )
            return float(tw - tu)

        mws = [tables[o]["m_w"] for o in t_ops]
        d_obs = pooled_delta(ms, mws, ps)
        K = ms[0].shape[0]
        d_null = np.empty(2000)
        rng_d = np.random.default_rng(SEED + 7)
        for t_i in range(2000):
            flips = rng_d.random(K) < 0.5
            ms_a = [np.where(flips[:, None], mw, m) for m, mw in zip(ms, mws)]
            ms_b = [np.where(flips[:, None], m, mw) for m, mw in zip(ms, mws)]
            d_null[t_i] = pooled_delta(ms_a, ms_b, ps)
        p_dw_pos = float((1 + np.sum(d_null >= d_obs)) / (1 + len(d_null)))
        p_dw_neg = float((1 + np.sum(d_null <= d_obs)) / (1 + len(d_null)))

        # robustness
        rob = {}
        rob["cosine_pooled_tau"] = round(
            float(
                np.median(
                    [
                        kendall_tau_b(
                            tables[o]["m_cos"].ravel(), tables[o]["p"].ravel()
                        )
                        for o in t_ops
                    ]
                )
            ),
            3,
        )
        rob["spearman_pooled"] = round(
            float(
                np.median(
                    [
                        spearman_rho(tables[o]["m"].ravel(), tables[o]["p"].ravel())
                        for o in t_ops
                    ]
                )
            ),
            3,
        )
        lobo = []
        B = len(brands)
        for bi in range(B):
            keep = [j for j in range(B) if j != bi]
            lobo.append(
                float(
                    np.median(
                        [
                            kendall_tau_b(
                                tables[o]["m"][:, keep].ravel(),
                                tables[o]["p"][:, keep].ravel(),
                            )
                            for o in t_ops
                        ]
                    )
                )
            )
        rob["leave_one_brand_out"] = {
            "min": round(min(lobo), 3),
            "max": round(max(lobo), 3),
        }
        if len(t_ops) > 1:
            looo = []
            for oi in range(len(t_ops)):
                sub = [o for j, o in enumerate(t_ops) if j != oi]
                looo.append(
                    float(
                        np.median(
                            [
                                kendall_tau_b(
                                    tables[o]["m"].ravel(), tables[o]["p"].ravel()
                                )
                                for o in sub
                            ]
                        )
                    )
                )
            rob["leave_one_operator_out"] = {
                "min": round(min(looo), 3),
                "max": round(max(looo), 3),
            }
        # brand fixed effects (subsumes brand-level familiarity/salience)
        fe_taus = []
        for o in t_ops:
            p_dm = tables[o]["p"] - tables[o]["p"].mean(axis=0, keepdims=True)
            m_dm = tables[o]["m"] - tables[o]["m"].mean(axis=0, keepdims=True)
            fe_taus.append(kendall_tau_b(m_dm.ravel(), p_dm.ravel()))
        rob["brand_fixed_effects_pooled_tau"] = round(float(np.median(fe_taus)), 3)
        # random-profile falsification
        rng_r = np.random.default_rng(SEED + 13)
        rand_taus = []
        for o in t_ops:
            K_o = tables[o]["m"].shape[0]
            rand_beta = {b: rng_r.uniform(1, 10, 8) for b in brands}
            m_rand = np.zeros_like(tables[o]["m"])
            for ki, c in enumerate([c for c in personas][:K_o]):
                theta = np.array(c["profile"])
                for bi, b in enumerate(brands):
                    m_rand[ki, bi] = match_euclid(theta, rand_beta[b])
            rand_taus.append(kendall_tau_b(m_rand.ravel(), tables[o]["p"].ravel()))
        rob["random_profile_pooled_tau"] = round(float(np.median(rand_taus)), 3)

        cat_pass = bool(p_val < alpha and obs >= tau_floor)
        category_pass[cat] = cat_pass
        for o in t_ops:
            family_taus[fam[o]].append(per_op_tau[o])

        cat_out = {
            "study": proto["categories"][cat]["study"],
            "operators_used": t_ops,
            "n_cohorts_per_op": {o: tables[o]["n_cohorts"] for o in t_ops},
            "per_operator_tau_b": per_op_tau,
            "pooled_tau_b": round(obs, 3),
            "permutation_p_one_sided": round(p_val, 4),
            "category_level_pass": cat_pass,
            "isotonic_R2_pooled": round(r2, 3),
            "same_call_tau": None if math.isnan(tau_same) else round(tau_same, 3),
            "delta_tau_common_method": (
                None if math.isnan(delta_tau) else round(delta_tau, 3)
            ),
            "delta_tau_w": round(d_obs, 3),
            "delta_tau_w_p_positive": round(p_dw_pos, 4),
            "delta_tau_w_p_negative": round(p_dw_neg, 4),
            "robustness": rob,
        }

        # induced-matrix layer + band mass (Study 2 categories; band for all)
        p_pooled = np.mean([tables[o]["p"] for o in t_ops], axis=0)  # K x B
        s_vec = p_pooled.mean(axis=0)
        s_vec = s_vec / s_vec.sum()
        var_c = p_pooled.var(axis=0, ddof=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            s_plus_1 = np.median(
                np.where(var_c > 0, s_vec * (1 - s_vec) / var_c, np.nan)
            )
        S = max(float(s_plus_1) - 1 if not math.isnan(float(s_plus_1)) else 1.0, 1.0)
        P = (np.eye(len(s_vec)) + S * np.outer(np.ones(len(s_vec)), s_vec)) / (S + 1)
        diag = np.diag(P)
        # observed repeat propensity from switching probes
        rep_obs = defaultdict(list)
        for op in t_ops:
            for recs in [
                ops_data[op]["eliciting"].get((cat, c["cohort_id"]), [])
                for c in personas
            ]:
                for r in recs:
                    sw = r["payload"].get("switching")
                    if sw and sw.get("current_brand") in brands and sw["next_purchase"]:
                        cur = sw["current_brand"]
                        rep_obs[cur].append(sw["next_purchase"].get(cur, np.nan))
        rep_vec = np.array(
            [np.nanmean(rep_obs[b]) if rep_obs.get(b) else np.nan for b in brands]
        )
        valid = ~np.isnan(rep_vec)
        dj_tau = (
            round(kendall_tau_b(diag[valid], rep_vec[valid]), 3)
            if valid.sum() >= 3
            else None
        )
        cat_out["induced_matrix"] = {
            "S": round(S, 3),
            "s": [round(float(x), 4) for x in s_vec],
            "diagonal": [round(float(x), 4) for x in diag],
            "dj_diag_vs_observed_repeat_tau": dj_tau,
            "observed_repeat_by_brand": {
                b: (
                    None
                    if math.isnan(float(rep_vec[i]))
                    else round(float(rep_vec[i]), 3)
                )
                for i, b in enumerate(brands)
            },
        }
        # intermediate band mass + cohort dispersion
        lo, hi = fitted.min(), fitted.max()
        t1, t2 = lo + (hi - lo) / 3, lo + 2 * (hi - lo) / 3
        band_mass = float(np.mean((fitted >= t1) & (fitted <= t2)))
        prof = np.array([c["profile"] for c in personas])
        disp = float(
            np.mean(
                [
                    np.linalg.norm(prof[i] - prof[j])
                    for i in range(len(prof))
                    for j in range(i + 1, len(prof))
                ]
            )
        )
        cat_out["band"] = {
            "mass": round(band_mass, 3),
            "cohort_dispersion": round(disp, 3),
        }
        if proto["categories"][cat]["study"] == 2:
            study2_bands.append((cat, band_mass, disp))
        results["categories"][cat] = cat_out

    # Kill conditions
    results["kill_conditions"] = {}
    results["kill_conditions"]["K1_no_link"] = not any(category_pass.values())
    fam_sign = {f: np.sign(np.median(v)) for f, v in family_taus.items() if v}
    fam_med = {f: round(float(np.median(v)), 3) for f, v in family_taus.items() if v}
    results["family_pooled_tau"] = fam_med
    results["kill_conditions"]["K2_operator_unstable"] = bool(
        any(
            fam_sign[a] * fam_sign[b] < 0
            and abs(fam_med[a]) >= tau_floor
            and abs(fam_med[b]) >= tau_floor
            for a in fam_sign
            for b in fam_sign
        )
    )
    sc_positive = any(
        (c.get("same_call_tau") or 0) >= tau_floor
        for c in results["categories"].values()
        if isinstance(c, dict)
    )
    results["kill_conditions"]["K3_common_method_artifact"] = bool(
        results["kill_conditions"]["K1_no_link"] and sc_positive
    )
    results["kill_conditions"]["K4_instrument_failure"] = results[
        "K4_instrument_failure"
    ]

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(results, indent=2))
    print(f"results -> {out_path}")
    return results


# ---------------------------------------------------------------------------
# Stimulus-validation gate (pre-campaign)
# ---------------------------------------------------------------------------
def stimulus_gate(records_glob: str) -> bool:
    proto = yaml.safe_load((PAPER_DIR / "PROTOCOL.yaml").read_text())
    s1 = yaml.safe_load((PAPER_DIR / "STIMULI_STUDY1.yaml").read_text())
    targets = {b["brand_id"]: np.array(b["target_profile"]) for b in s1["brands"]}
    ops_data = load_all(records_glob)
    per_pack: dict = defaultdict(list)
    for op, od in ops_data.items():
        for bid, reps in od["validate"].items():
            per_pack[bid].extend(reps)
    ok = True
    for bid, target in targets.items():
        reps = per_pack.get(bid, [])
        if not reps:
            print(f"  {bid}: NO VALIDATION READINGS")
            ok = False
            continue
        mean_read = np.array(reps).mean(axis=0)
        mad = float(np.mean(np.abs(mean_read - target)))
        verdict = "PASS" if mad <= proto["stimulus_gate_mad_max"] else "FAIL"
        if verdict == "FAIL":
            ok = False
        print(
            f"  {bid}: MAD={mad:.3f} {verdict}  (n={len(reps)})  mean={np.round(mean_read, 1).tolist()}"
        )
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", default=str(PAPER_DIR / "data" / "records_*.jsonl"))
    ap.add_argument("--out", default=str(PAPER_DIR / "data" / "results.json"))
    ap.add_argument(
        "--gate", action="store_true", help="run the stimulus-validation gate only"
    )
    ap.add_argument("--n-perm", type=int, default=N_PERM)
    a = ap.parse_args()
    if a.gate:
        ok = stimulus_gate(a.records)
        raise SystemExit(0 if ok else 1)
    analyze(a.records, a.out, a.n_perm)
