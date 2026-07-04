#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26", "scipy>=1.12", "pyyaml>=6.0"]
# ///
"""estimator.py — PRISM-C PL4 choice-perception-gap estimator (2026bb).

Deterministic, seeded (SEED = 20260702). Implements the frozen PL0 criteria
(research/prism_c/PREREGISTRATION.md sections 6 + 9):

- stated brand vector: pooled mean over channels + op pairs; stated operator
  floor per brand = max pairwise cosine distance among per-op-pair vectors
- need vector per scenario: pooled mean over op pairs; floor analogous
- predicted pick per (scenario, choice-set): argmax cosine similarity
  (brand vector, need vector); top-2 margin recorded
- divergence: revealed pick != predicted pick, per trial
- choice operator floor: mean pairwise disagreement rate between chooser
  families on identical (scenario, arrangement) trials
- H1: divergence rate's scenario-cluster bootstrap 95% CI lower bound
  > k x floor (k = 2; sweep {1.5, 2, 3} in robustness)
- H2: conditional logit of revealed choice on the eight per-dimension
  |brand - need| distances; LR test of the pre-registered choice-weighty set
  {economic, experiential, social} vs the 5-dim restricted model, alpha=.017;
  effect sizes: delta-LL, delta-AIC, McFadden pseudo-R2, per-dim weights
- H3: position covariates (first-position indicator + normalized position
  index); supported if the stated->revealed coefficient (single-index cosine
  conditional logit) stays significant at .017 and shifts within its CI when
  position covariates enter
- mechanism contrasts (pre-registered SECONDARY, PL0 section 9.3):
  M1a participation ratio of |weights|; M1b divergence ~ non-choice-weighty
  advantage share; M2b divergence ~ presented position of predicted pick;
  M3a brand-ASC conditional logit (LR + ASC/prevalence-proxy correlation);
  M3b modal-brand over-selection on divergent trials; M4a divergence ~
  stated top-2 margin
- boundary heterogeneity (PL0 section 9.4): B1 divergence by need-vector
  entropy tercile; B2 divergence in the dominance (positive-control) region
- controls: positive = dominant option majority-picked per set and >= .9
  overall; negative = counterbalanced twin picks show no preference beyond
  chance (exact binomial two-sided at .05)
- robustness: k sweep; Euclidean + Mahalanobis predicted-pick alternates;
  per-family divergence + leave-one-family-out floors (exploratory)

Run:
    uv run python research/prism_c/code/estimator.py \
        --records research/prism_c/data/confirmatory_records.jsonl \
        --out research/prism_c/data/pl4_results.json --robustness
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import optimize, stats
from scipy.special import logsumexp

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH))
sys.path.insert(0, str(HERE))

from prism_core.stats import (  # noqa: E402
    FLOOR_MIN,
    cluster_bootstrap,
    dist_full,
    participation_ratio,
)
from prism_core.concordance import (  # noqa: E402
    pairwise_disagreement_floor,
    per_family_pick_table,
)

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
WEIGHTY = ("economic", "experiential", "social")  # pre-registered (PL0 H2)
WEIGHTY_IDX = [DIMENSIONS.index(d) for d in WEIGHTY]
OTHER_IDX = [i for i in range(8) if i not in WEIGHTY_IDX]
SEED = 20260702
K_DEFAULT = 2.0
N_BOOT = 2000
ALPHA_CONF = 0.017


# ---------------------------------------------------------------------------
# Data shaping
# ---------------------------------------------------------------------------
def split_records(records: list[dict]) -> dict:
    ok = [r for r in records if not r.get("flagged_malformed")]
    return {
        "stated": [r for r in ok if r["kind"] == "stated"],
        "need": [r for r in ok if r["kind"] == "need"],
        "choice": [r for r in ok if r["kind"] == "choice" and not r.get("control")],
        "positive": [
            r for r in ok if r["kind"] == "choice" and r.get("control") == "positive"
        ],
        "negative": [
            r for r in ok if r["kind"] == "choice" and r.get("control") == "negative"
        ],
    }


def stated_vectors(stated: list[dict]) -> tuple[dict, dict]:
    """brand -> pooled 8-vector; brand -> stated operator floor (max pairwise
    cosine distance among per-op-pair pooled vectors)."""
    per_op: dict = defaultdict(lambda: defaultdict(list))
    for r in stated:
        per_op[r["brand"]][r["op_pair"]].append(np.asarray(r["value"], float))
    vecs, floors = {}, {}
    for brand, ops in per_op.items():
        op_means = [np.mean(v, axis=0) for v in ops.values()]
        vecs[brand] = np.mean(op_means, axis=0)
        if len(op_means) >= 2:
            floors[brand] = max(
                max(dist_full(x, y) for x, y in itertools.combinations(op_means, 2)),
                FLOOR_MIN,
            )
        else:
            floors[brand] = FLOOR_MIN
    return vecs, floors


def need_vectors(need: list[dict]) -> tuple[dict, dict]:
    per_op: dict = defaultdict(lambda: defaultdict(list))
    for r in need:
        per_op[r["scenario"]][r["op_pair"]].append(np.asarray(r["value"], float))
    vecs, floors = {}, {}
    for sc, ops in per_op.items():
        op_means = [np.mean(v, axis=0) for v in ops.values()]
        vecs[sc] = np.mean(op_means, axis=0)
        floors[sc] = (
            max(
                max(dist_full(x, y) for x, y in itertools.combinations(op_means, 2)),
                FLOOR_MIN,
            )
            if len(op_means) >= 2
            else FLOOR_MIN
        )
    return vecs, floors


def cos_sim(a, b) -> float:
    return 1.0 - dist_full(a, b, "cosine")


def predicted_picks(
    choice: list[dict], svecs: dict, nvecs: dict, metric: str = "cosine", vi=None
) -> dict:
    """(scenario) -> {predicted, runner_up, margin, sims} over the scenario's
    choice-set (constant across arrangements)."""
    out = {}
    sets_by_scenario = {}
    for r in choice:
        sets_by_scenario.setdefault(r["scenario"], tuple(sorted(r["choice_set"])))
    for sc, cset in sets_by_scenario.items():
        if sc not in nvecs:
            continue
        sims = {}
        for b in cset:
            if b not in svecs:
                continue
            if metric == "cosine":
                sims[b] = cos_sim(svecs[b], nvecs[sc])
            else:
                sims[b] = -dist_full(svecs[b], nvecs[sc], metric, vi)
        if len(sims) < 2:
            continue
        ranked = sorted(sims, key=sims.get, reverse=True)
        out[sc] = {
            "predicted": ranked[0],
            "runner_up": ranked[1],
            "margin": sims[ranked[0]] - sims[ranked[1]],
            "sims": sims,
        }
    return out


def divergence_table(choice: list[dict], preds: dict) -> list[dict]:
    """Per-trial rows with divergence indicator + covariates."""
    rows = []
    for r in choice:
        sc = r["scenario"]
        if sc not in preds or r.get("pick") is None:
            continue
        p = preds[sc]
        pos_pred = r["arrangement"].index(p["predicted"])
        rows.append(
            {
                "scenario": sc,
                "family": r["family"],
                "arrangement_id": r["arrangement_id"],
                "pick": r["pick"],
                "predicted": p["predicted"],
                "diverged": r["pick"] != p["predicted"],
                "margin": p["margin"],
                "pos_of_predicted": pos_pred,
                "n_options": len(r["arrangement"]),
                "pos_of_pick": r["arrangement"].index(r["pick"]),
            }
        )
    return rows


# ---------------------------------------------------------------------------
# H1 — gap vs choice operator floor
# ---------------------------------------------------------------------------
def choice_floor(choice: list[dict]) -> float:
    if not choice:
        return FLOOR_MIN
    picks = per_family_pick_table(choice, key_fields=("scenario", "arrangement_id"))
    fl = pairwise_disagreement_floor(picks)
    if np.isnan(fl):
        return FLOOR_MIN
    return max(fl, FLOOR_MIN)


def test_h1(div_rows: list[dict], choice: list[dict], *, k=K_DEFAULT, seed=SEED):
    rate = float(np.mean([r["diverged"] for r in div_rows])) if div_rows else None
    floor = choice_floor(choice)
    scenarios = sorted({r["scenario"] for r in div_rows})
    by_sc_div = defaultdict(list)
    for r in div_rows:
        by_sc_div[r["scenario"]].append(r["diverged"])
    by_sc_choice = defaultdict(list)
    for r in choice:
        by_sc_choice[r["scenario"]].append(r)

    def rate_stat(sample):
        vals = [v for sc in sample for v in by_sc_div[sc]]
        return float(np.mean(vals)) if vals else None

    def ratio_stat(sample):
        vals = [v for sc in sample for v in by_sc_div[sc]]
        ch = [r for sc in sample for r in by_sc_choice[sc]]
        if not vals or not ch:
            return None
        fl = choice_floor(ch)
        return float(np.mean(vals)) / fl

    ci_rate = cluster_bootstrap(scenarios, rate_stat, n_boot=N_BOOT, seed=seed)
    ci_ratio = cluster_bootstrap(scenarios, ratio_stat, n_boot=N_BOOT, seed=seed + 1)
    supported = rate is not None and ci_rate[0] is not None and ci_rate[0] > k * floor
    return {
        "divergence_rate": rate,
        "n_trials": len(div_rows),
        "choice_operator_floor": floor,
        "snr": (rate / floor) if rate is not None else None,
        "rate_ci95": ci_rate,
        "snr_ci95": ci_ratio,
        "k": k,
        "supported": bool(supported),
    }


# ---------------------------------------------------------------------------
# Conditional logit (H2 / H3 / mechanisms)
# ---------------------------------------------------------------------------
def build_cl_trials(
    choice: list[dict], svecs: dict, nvecs: dict, preds: dict
) -> list[dict]:
    """One CL observation per choice record: feature matrix X (J x p_dim=8,
    per-dim NEGATIVE |brand-need| distance / 10) + position features +
    chosen index + brand names in presented order."""
    trials = []
    for r in choice:
        sc = r["scenario"]
        if sc not in preds or r.get("pick") is None or sc not in nvecs:
            continue
        arr = r["arrangement"]
        if any(b not in svecs for b in arr):
            continue
        nv = nvecs[sc]
        X = np.stack([-(np.abs(np.asarray(svecs[b], float) - nv) / 10.0) for b in arr])
        J = len(arr)
        pos_first = np.zeros(J)
        pos_first[0] = 1.0
        pos_index = np.arange(J, dtype=float) / max(J - 1, 1)
        cos = np.array([preds[sc]["sims"].get(b, np.nan) for b in arr])
        trials.append(
            {
                "scenario": sc,
                "family": r["family"],
                "X": X,
                "pos_first": pos_first,
                "pos_index": pos_index,
                "cos": cos,
                "chosen": arr.index(r["pick"]),
                "brands": arr,
            }
        )
    return trials


def _nll_and_grad(beta, feats, chosen_list):
    nll, grad = 0.0, np.zeros(len(beta))
    for X, ch in zip(feats, chosen_list):
        v = X @ beta
        lse = logsumexp(v)
        p = np.exp(v - lse)
        nll += lse - v[ch]
        grad += X.T @ p - X[ch]
    return nll, grad


def fit_cl(feats: list[np.ndarray], chosen_list: list[int], p: int) -> dict:
    """MLE conditional logit; Wald SEs from the numerical inverse Hessian."""
    x0 = np.zeros(p)
    res = optimize.minimize(
        _nll_and_grad,
        x0,
        args=(feats, chosen_list),
        jac=True,
        method="BFGS",
        options={"maxiter": 5000, "gtol": 1e-6},
    )
    beta = res.x
    # numerical Hessian of the NLL for SEs
    eps = 1e-5
    H = np.zeros((p, p))
    for i in range(p):
        e = np.zeros(p)
        e[i] = eps
        _, gp = _nll_and_grad(beta + e, feats, chosen_list)
        _, gm = _nll_and_grad(beta - e, feats, chosen_list)
        H[:, i] = (gp - gm) / (2 * eps)
    H = (H + H.T) / 2
    try:
        cov = np.linalg.inv(H)
        se = np.sqrt(np.clip(np.diag(cov), 0, None))
    except np.linalg.LinAlgError:
        se = np.full(p, np.nan)
    ll = -float(res.fun)
    n = len(feats)
    ll0 = -sum(np.log(len(c)) for c in feats)  # equal-prob null
    return {
        "beta": beta.tolist(),
        "se": se.tolist(),
        "ll": ll,
        "ll_null": float(ll0),
        "aic": 2 * p - 2 * ll,
        "mcfadden_r2": 1.0 - ll / ll0 if ll0 != 0 else None,
        "n_trials": n,
        "converged": bool(res.success),
    }


def lr_test(ll_full: float, ll_restricted: float, df: int) -> dict:
    lr = max(0.0, 2.0 * (ll_full - ll_restricted))
    return {
        "lr": lr,
        "df": df,
        "p": float(stats.chi2.sf(lr, df)),
        "delta_ll": ll_full - ll_restricted,
    }


def test_h2(trials: list[dict], alpha=ALPHA_CONF) -> dict:
    feats_full = [t["X"] for t in trials]
    chosen = [t["chosen"] for t in trials]
    full = fit_cl(feats_full, chosen, 8)
    feats_restr = [t["X"][:, OTHER_IDX] for t in trials]
    restr = fit_cl(feats_restr, chosen, len(OTHER_IDX))
    lr = lr_test(full["ll"], restr["ll"], df=len(WEIGHTY_IDX))
    weights = dict(zip(DIMENSIONS, full["beta"]))
    return {
        "full_model": full,
        "restricted_model_no_weighty": {k: v for k, v in restr.items() if k != "beta"}
        | {"beta": dict(zip([DIMENSIONS[i] for i in OTHER_IDX], restr["beta"]))},
        "weights": weights,
        "weights_se": dict(zip(DIMENSIONS, full["se"])),
        "lr_weighty": lr,
        "delta_aic": restr["aic"] - full["aic"],
        "alpha": alpha,
        "supported": bool(lr["p"] < alpha and lr["delta_ll"] > 0),
    }


def _single_index_fit(trials, with_position: bool):
    feats, chosen = [], []
    p = 3 if with_position else 1
    for t in trials:
        cols = [t["cos"]]
        if with_position:
            cols += [t["pos_first"], t["pos_index"]]
        feats.append(np.column_stack(cols))
        chosen.append(t["chosen"])
    return fit_cl(feats, chosen, p)


def test_h3(trials: list[dict], alpha=ALPHA_CONF) -> dict:
    """Single-index (cosine) conditional logit without vs with position
    covariates; supported if gamma stays significant and shifts within its
    no-position CI when position enters."""
    base = _single_index_fit(trials, with_position=False)
    adj = _single_index_fit(trials, with_position=True)
    g0, se0 = base["beta"][0], base["se"][0]
    g1, se1 = adj["beta"][0], adj["se"][0]
    z1 = g1 / se1 if se1 and se1 > 0 else np.nan
    p1 = float(2 * stats.norm.sf(abs(z1))) if np.isfinite(z1) else None
    shift_within_ci = abs(g1 - g0) <= 1.96 * se0 if se0 and se0 > 0 else False
    return {
        "gamma_raw": g0,
        "gamma_raw_se": se0,
        "gamma_adjusted": g1,
        "gamma_adjusted_se": se1,
        "position_betas": {"first": adj["beta"][1], "index": adj["beta"][2]},
        "position_se": {"first": adj["se"][1], "index": adj["se"][2]},
        "p_gamma_adjusted": p1,
        "shift_within_ci": bool(shift_within_ci),
        "alpha": alpha,
        "supported": bool(p1 is not None and p1 < alpha and shift_within_ci),
    }


# ---------------------------------------------------------------------------
# Logistic regression (mechanism contrasts on the divergence indicator)
# ---------------------------------------------------------------------------
def fit_logistic(x: np.ndarray, y: np.ndarray) -> dict:
    """y ~ intercept + x (1 covariate); MLE with Wald test."""
    X = np.column_stack([np.ones(len(x)), x])

    def nll(b):
        z = X @ b
        return float(np.sum(np.logaddexp(0, z) - y * z))

    def grad(b):
        z = X @ b
        p = 1 / (1 + np.exp(-z))
        return X.T @ (p - y)

    res = optimize.minimize(nll, np.zeros(2), jac=grad, method="BFGS")
    b = res.x
    z = X @ b
    p = 1 / (1 + np.exp(-z))
    W = p * (1 - p)
    H = X.T @ (X * W[:, None])
    try:
        cov = np.linalg.inv(H)
        se = np.sqrt(np.clip(np.diag(cov), 0, None))
        zstat = b[1] / se[1] if se[1] > 0 else np.nan
        pval = float(2 * stats.norm.sf(abs(zstat))) if np.isfinite(zstat) else None
    except np.linalg.LinAlgError:
        se, pval, zstat = np.full(2, np.nan), None, np.nan
    return {
        "intercept": float(b[0]),
        "slope": float(b[1]),
        "slope_se": float(se[1]),
        "slope_z": float(zstat) if np.isfinite(zstat) else None,
        "p": pval,
        "n": int(len(y)),
        "odds_ratio_per_sd": (
            float(np.exp(b[1] * np.std(x))) if np.std(x) > 0 else None
        ),
    }


def nonweighty_share(svecs, nvecs, sc, predicted, runner_up) -> float | None:
    """Share of the predicted pick's cosine advantage over the runner-up that
    is carried by the NON-choice-weighty dimensions (M1b). Decomposition on
    normalized vectors: advantage_d = nhat_d * (phat_d - rhat_d)."""
    nv = np.asarray(nvecs[sc], float)
    pv = np.asarray(svecs[predicted], float)
    rv = np.asarray(svecs[runner_up], float)
    nn, pn, rn = np.linalg.norm(nv), np.linalg.norm(pv), np.linalg.norm(rv)
    if 0 in (nn, pn, rn):
        return None
    contrib = (nv / nn) * (pv / pn - rv / rn)
    total = contrib.sum()
    if abs(total) < 1e-12:
        return None
    return float(contrib[OTHER_IDX].sum() / abs(total))


def mechanism_contrasts(trials, div_rows, svecs, nvecs, preds, index_status) -> dict:
    out = {}
    # --- M1a: participation ratio of the full-model weights
    full = fit_cl([t["X"] for t in trials], [t["chosen"] for t in trials], 8)
    out["M1a_participation_ratio"] = {
        "weights": dict(zip(DIMENSIONS, full["beta"])),
        "effective_dimensionality": participation_ratio(full["beta"]),
        "n_dims": 8,
    }
    # --- M1b: divergence ~ non-weighty advantage share
    xs, ys = [], []
    for r in div_rows:
        s = nonweighty_share(
            svecs,
            nvecs,
            r["scenario"],
            r["predicted"],
            preds[r["scenario"]]["runner_up"],
        )
        if s is not None:
            xs.append(s)
            ys.append(1.0 if r["diverged"] else 0.0)
    out["M1b_divergence_vs_nonweighty_share"] = (
        fit_logistic(np.asarray(xs), np.asarray(ys)) if len(set(ys)) > 1 else None
    )
    # --- M2b: divergence ~ presented position of the predicted pick
    xs = np.asarray(
        [r["pos_of_predicted"] / max(r["n_options"] - 1, 1) for r in div_rows]
    )
    ys = np.asarray([1.0 if r["diverged"] else 0.0 for r in div_rows])
    out["M2b_divergence_vs_predicted_position"] = (
        fit_logistic(xs, ys) if len(set(ys.tolist())) > 1 else None
    )
    # --- M3a: brand-ASC conditional logit (reference = alphabetical first)
    all_brands = sorted({b for t in trials for b in t["brands"]})
    ref = all_brands[0]
    asc_brands = [b for b in all_brands if b != ref]
    asc_idx = {b: i for i, b in enumerate(asc_brands)}
    feats_asc, chosen = [], []
    for t in trials:
        J = len(t["brands"])
        A = np.zeros((J, len(asc_brands)))
        for j, b in enumerate(t["brands"]):
            if b in asc_idx:
                A[j, asc_idx[b]] = 1.0
        feats_asc.append(np.hstack([t["X"], A]))
        chosen.append(t["chosen"])
    asc_fit = fit_cl(feats_asc, chosen, 8 + len(asc_brands))
    lr_asc = lr_test(asc_fit["ll"], full["ll"], df=len(asc_brands))
    ascs = dict(zip(asc_brands, asc_fit["beta"][8:]))
    member = {b: (index_status or {}).get(b) == "member" for b in ascs}
    if len(set(member.values())) > 1:
        a_vals = np.asarray([ascs[b] for b in ascs])
        m_vals = np.asarray([1.0 if member[b] else 0.0 for b in ascs])
        rho, rho_p = stats.spearmanr(a_vals, m_vals)
    else:
        rho, rho_p = None, None
    out["M3a_brand_asc"] = {
        "lr_vs_full": lr_asc,
        "reference_brand": ref,
        "top_ascs": dict(sorted(ascs.items(), key=lambda kv: -kv[1])[:8]),
        "asc_vs_index_member_spearman": {
            "rho": float(rho) if rho is not None else None,
            "p": float(rho_p) if rho_p is not None else None,
        },
    }
    # --- M3b: modal-brand over-selection on divergent trials
    modal = {}
    picks_by_sc = defaultdict(list)
    for r in div_rows:
        picks_by_sc[r["scenario"]].append(r["pick"])
    for sc, ps in picks_by_sc.items():
        modal[sc] = Counter(ps).most_common(1)[0][0]
    div = [r for r in div_rows if r["diverged"]]
    conv = [r for r in div_rows if not r["diverged"]]
    rate_div = (
        float(np.mean([r["pick"] == modal[r["scenario"]] for r in div]))
        if div
        else None
    )
    rate_conv = (
        float(np.mean([r["pick"] == modal[r["scenario"]] for r in conv]))
        if conv
        else None
    )
    out["M3b_modal_overselection"] = {
        "modal_pick_rate_divergent": rate_div,
        "modal_pick_rate_convergent": rate_conv,
        "note": "modal = per-scenario most frequent pick across all trials",
    }
    # --- M4a: divergence ~ stated top-2 margin
    xs = np.asarray([r["margin"] for r in div_rows])
    out["M4a_divergence_vs_margin"] = (
        fit_logistic(xs, ys) if len(set(ys.tolist())) > 1 else None
    )
    return out


# ---------------------------------------------------------------------------
# Boundary heterogeneity (PL0 section 9.4)
# ---------------------------------------------------------------------------
def need_entropy(v: np.ndarray) -> float:
    p = np.asarray(v, float)
    s = p.sum()
    if s <= 0:
        return 0.0
    p = p / s
    p = p[p > 0]
    return float(-(p * np.log(p)).sum() / np.log(8))


def boundary_tests(div_rows, nvecs, positive_rows, *, seed=SEED) -> dict:
    ent = {sc: need_entropy(v) for sc, v in nvecs.items()}
    rows = [r for r in div_rows if r["scenario"] in ent]
    if rows:
        es = np.asarray([ent[r["scenario"]] for r in rows])
        t1, t2 = np.quantile(es, [1 / 3, 2 / 3])
        terc = {}
        for lo, hi, name in [
            (-np.inf, t1, "low"),
            (t1, t2, "mid"),
            (t2, np.inf, "high"),
        ]:
            sub = [r for r, e in zip(rows, es) if lo < e <= hi]
            sc_list = sorted({r["scenario"] for r in sub})
            by_sc = defaultdict(list)
            for r in sub:
                by_sc[r["scenario"]].append(r["diverged"])

            def stat(sample, _by=by_sc):
                vals = [v for s in sample for v in _by[s]]
                return float(np.mean(vals)) if vals else None

            terc[name] = {
                "n": len(sub),
                "rate": float(np.mean([r["diverged"] for r in sub])) if sub else None,
                "ci95": (
                    cluster_bootstrap(sc_list, stat, n_boot=500, seed=seed)
                    if sc_list
                    else (None, None)
                ),
            }
        # higher entropy = flatter (more ambiguous) need vector
        b1 = {
            "terciles_by_need_entropy": terc,
            "monotone_increasing": (
                terc["low"]["rate"] is not None
                and terc["high"]["rate"] is not None
                and terc["low"]["rate"] < terc["high"]["rate"]
            ),
        }
    else:
        b1 = None
    b2 = {
        "dominance_region_divergence": (
            float(np.mean([r["pick"] != r["dominant"] for r in positive_rows]))
            if positive_rows
            else None
        ),
        "n": len(positive_rows),
    }
    return {"B1_need_ambiguity": b1, "B2_dominance": b2}


# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------
def positive_control(positive_rows: list[dict]) -> dict:
    by_set = defaultdict(list)
    for r in positive_rows:
        by_set[r["scenario"]].append(r)
    per_set = {}
    for sc, rows in by_set.items():
        dom = rows[0].get("dominant")
        rate = float(np.mean([r["pick"] == dom for r in rows]))
        per_set[sc] = {"dominant": dom, "picked_rate": rate, "n": len(rows)}
    overall = (
        float(np.mean([r["pick"] == r.get("dominant") for r in positive_rows]))
        if positive_rows
        else None
    )
    passed = (
        positive_rows
        and overall is not None
        and overall >= 0.9
        and all(v["picked_rate"] > 0.5 for v in per_set.values())
    )
    return {"passed": bool(passed), "overall_rate": overall, "per_set": per_set}


def negative_control(negative_rows: list[dict]) -> dict:
    by_set = defaultdict(list)
    for r in negative_rows:
        by_set[r["scenario"]].append(r)
    per_set, pvals = {}, {}
    for sc, rows in by_set.items():
        opts = sorted(rows[0]["choice_set"])
        n_a = sum(1 for r in rows if r["pick"] == opts[0])
        n = len(rows)
        p = float(stats.binomtest(n_a, n, 0.5).pvalue) if n else 1.0
        first_rate = (
            float(np.mean([r["pos_of_pick"] == 0 for r in rows]))
            if all("pos_of_pick" in r for r in rows)
            else None
        )
        per_set[sc] = {
            "n": n,
            "picks_option_a": n_a,
            "binom_p_two_sided": p,
            "first_position_pick_rate": first_rate,
        }
        pvals[sc] = p
    passed = bool(per_set) and all(p >= 0.05 for p in pvals.values())
    return {"passed": passed, "per_set": per_set}


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------
def analyze(
    records: list[dict],
    *,
    k=K_DEFAULT,
    seed=SEED,
    metric="cosine",
    index_status: dict | None = None,
    exclude_ops: tuple[str, ...] = (),
) -> dict:
    parts = split_records(records)
    if exclude_ops:
        # pilot-excluded operator pairs stay out of floors, pooled vectors
        # and predicted picks (PL0 section 9.2); they are analyzed separately
        # as exploratory observers.
        parts["stated"] = [
            r for r in parts["stated"] if r["op_pair"] not in exclude_ops
        ]
        parts["need"] = [r for r in parts["need"] if r["op_pair"] not in exclude_ops]
    svecs, sfloors = stated_vectors(parts["stated"])
    nvecs, nfloors = need_vectors(parts["need"])
    vi = None
    if metric == "mahalanobis" and svecs:
        x = np.stack(list(svecs.values()))
        vi = np.linalg.inv(np.cov(x.T) + np.eye(8) * 1e-6)
    preds = predicted_picks(parts["choice"], svecs, nvecs, metric, vi)
    div_rows = divergence_table(parts["choice"], preds)
    trials = build_cl_trials(parts["choice"], svecs, nvecs, preds)

    # positive-control divergence rows (need pos_of_pick for calibration)
    pos_rows = []
    for r in parts["positive"]:
        if r.get("pick") is None:
            continue
        pos_rows.append({**r, "pos_of_pick": r["arrangement"].index(r["pick"])})
    neg_rows = []
    for r in parts["negative"]:
        if r.get("pick") is None:
            continue
        neg_rows.append({**r, "pos_of_pick": r["arrangement"].index(r["pick"])})

    h1 = test_h1(div_rows, parts["choice"], k=k, seed=seed)
    h2 = test_h2(trials) if trials else None
    h3 = test_h3(trials) if trials else None
    mech = (
        mechanism_contrasts(trials, div_rows, svecs, nvecs, preds, index_status)
        if trials and div_rows
        else None
    )
    bound = boundary_tests(div_rows, nvecs, pos_rows, seed=seed)

    # exploratory: per-family divergence + leave-one-family-out floor
    fams = sorted({r["family"] for r in div_rows})
    per_family = {
        f: float(np.mean([r["diverged"] for r in div_rows if r["family"] == f]))
        for f in fams
    }
    loo_floor = {}
    for f in fams:
        sub = [r for r in parts["choice"] if r["family"] != f]
        loo_floor[f"without_{f}"] = choice_floor(sub) if sub else None

    return {
        "seed": seed,
        "k": k,
        "metric": metric,
        "n_brands_stated": len(svecs),
        "n_scenarios_with_need": len(nvecs),
        "n_choice_trials": len(div_rows),
        "stated_floors": {b: float(v) for b, v in sfloors.items()},
        "need_floors": {s: float(v) for s, v in nfloors.items()},
        "predicted": {
            sc: {
                "predicted": p["predicted"],
                "runner_up": p["runner_up"],
                "margin": float(p["margin"]),
            }
            for sc, p in preds.items()
        },
        "H1": h1,
        "H2": h2,
        "H3": h3,
        "mechanisms": mech,
        "boundary": bound,
        "positive_control": positive_control(pos_rows),
        "negative_control": negative_control(neg_rows),
        "exploratory": {
            "per_family_divergence": per_family,
            "leave_one_family_out_floor": loo_floor,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True, nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--robustness", action="store_true")
    ap.add_argument(
        "--exclude-ops",
        default=None,
        help="comma list of pilot-excluded operator pairs (PL0 section 9.2)",
    )
    ap.add_argument(
        "--index-status",
        default=None,
        help="optional path to brand bank yaml for prevalence proxy",
    )
    args = ap.parse_args()

    records = []
    for path in args.records:
        with open(path) as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))

    index_status = None
    if args.index_status:
        import yaml

        bank = yaml.safe_load(Path(args.index_status).read_text())
        index_status = {
            b["brand"]: b.get("index_status")
            for brands in bank["strata"].values()
            for b in brands
        }

    excl = tuple(args.exclude_ops.split(",")) if args.exclude_ops else ()
    result = analyze(records, index_status=index_status, exclude_ops=excl)

    if args.robustness:
        result["robustness"] = {}
        for k_alt in (1.5, 3.0):
            r = analyze(records, k=k_alt, exclude_ops=excl)
            result["robustness"][f"k_{k_alt}"] = {"H1": r["H1"]}
        for m_alt in ("euclidean", "mahalanobis"):
            r = analyze(records, metric=m_alt, exclude_ops=excl)
            result["robustness"][m_alt] = {
                "H1": r["H1"],
                "predicted_changed": sum(
                    1
                    for sc in result["predicted"]
                    if sc in r["predicted"]
                    and r["predicted"][sc]["predicted"]
                    != result["predicted"][sc]["predicted"]
                ),
            }
        if excl:
            r = analyze(records, index_status=index_status)  # all ops incl. excluded
            result["robustness"]["excluded_ops_included"] = {
                "H1": r["H1"],
                "predicted_changed": sum(
                    1
                    for sc in result["predicted"]
                    if sc in r["predicted"]
                    and r["predicted"][sc]["predicted"]
                    != result["predicted"][sc]["predicted"]
                ),
            }

    Path(args.out).write_text(json.dumps(result, indent=2, default=str))
    print(f"[pl4] written: {args.out}")
    h1 = result["H1"]
    print(
        f"  divergence rate = {h1['divergence_rate']} "
        f"(n={h1['n_trials']}) floor = {h1['choice_operator_floor']:.4f} "
        f"S/N = {h1['snr']:.2f} CI95(rate) {h1['rate_ci95']}"
    )
    print(f"  H1 supported: {h1['supported']}")
    if result["H2"]:
        print(
            f"  H2 LR p = {result['H2']['lr_weighty']['p']:.4g} "
            f"supported: {result['H2']['supported']}"
        )
    if result["H3"]:
        print(f"  H3 supported: {result['H3']['supported']}")
    print(f"  positive control passed: {result['positive_control']['passed']}")
    print(f"  negative control passed: {result['negative_control']['passed']}")


if __name__ == "__main__":
    main()
