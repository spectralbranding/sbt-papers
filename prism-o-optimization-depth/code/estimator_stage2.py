#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0", "numpy>=1.26", "scipy>=1.12"]
# ///
"""estimator_stage2.py — PRISM-O (2026bd) PL4 estimator (frozen analysis plan).

Implements PREREGISTRATION.md §4/§6 (v1.1). All randomness seeded
(SEED = 20260703); run command: `uv run python research/prism_o/code/estimator_stage2.py`.

Depth score: D1=4, D2=3, D3=2, D4=1 (deeper = larger); UNCLASSIFIED and
MALFORMED excluded from means, shares reported per channel.

Per organization:
- per pair x channel: mean depth over classified interventions (named arm);
- per pair: gap_p = depth(STATED) - depth(ENACTED)  [positive = talks deeper];
- gap_hat = mean over pairs; operator floor = SD over pairs (ddof=1);
- RESOLVED iff |gap_hat| > SNR_K x floor (k = 2; sweep {1.5, 3} reported);
- artifact-cluster bootstrap CI (B = 2000) on gap_hat.

Panel (H2, alpha = .017): one-sample t on resolved gap_hats vs 0 + exact
sign test; effect size = mean gap in rung units + bootstrap CI; KS co-primary
(pooled stated vs enacted depth distributions) must agree in direction;
channel-label permutation falsification (1,000 within-org artifact-label
shuffles): observed panel mean outside the central .95 interval.

H3 instantiation (leave-one-out, non-circular): for each resolved org, every
pair's gap must sit within SNR_K x floor of the mean of the OTHER pairs'
gaps; H3 metric = fraction of resolved orgs where all pairs pass (the spine
FORK records this as the pre-registered dispersion statistic's mechanical
instantiation).

Controls: negative = within org x channel with >= 4 artifacts, odd/even
artifact split pseudo-gap must not resolve; contamination bound =
masked-arm gap_hat minus named-arm gap_hat on the masked subsample.
Secondary (exploratory): ai_announcer contrast.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_o_lib import DATA_DIR, load_records  # noqa: E402

SEED = 20260703
SNR_K = 2.0
B_BOOT = 2000
N_PERM = 1000
DEPTH = {"D1": 4.0, "D2": 3.0, "D3": 2.0, "D4": 1.0}


def fmt_p(p: float) -> str:
    if p < 0.001:
        return "p < .001"
    return f"p = {p:.3f}".replace("0.", ".")


def org_channel_depths(recs, arm="named"):
    """(org, channel) -> {op_pair: {artifact_id: [depths]}} for classified rungs."""
    d: dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in recs:
        if r.get("sentinel") or r.get("arm") != arm:
            continue
        v = DEPTH.get(r["rung_pred"])
        if v is not None:
            d[(r["org"], r["channel"])][r["op_pair"]][r["artifact_id"]].append(v)
    return d


def mean_depth(by_artifact: dict, arts=None) -> float:
    vals = [
        v
        for aid, vv in by_artifact.items()
        if arts is None or aid in arts
        for v in vv
    ]
    return float(np.mean(vals)) if vals else float("nan")


def org_gaps(depths, pairs, org):
    gaps = {}
    for p in pairs:
        s = mean_depth(depths.get((org, "STATED"), {}).get(p, {}))
        e = mean_depth(depths.get((org, "ENACTED"), {}).get(p, {}))
        if not (np.isnan(s) or np.isnan(e)):
            gaps[p] = s - e
    return gaps


def main() -> int:
    rng = np.random.default_rng(SEED)
    recs = []
    for shard in sorted(DATA_DIR.glob("stage2_records*.jsonl")):
        recs.extend(load_records(shard))
    manifest = json.loads((DATA_DIR / "panel_pinned_manifest.json").read_text())
    flags = {o["org"]: o["ai_announcer"] for o in manifest["orgs"]}
    pairs = sorted({r["op_pair"] for r in recs})
    orgs = sorted({r["org"] for r in recs})
    depths = org_channel_depths(recs, "named")

    # unclassified/malformed shares per channel
    shares = defaultdict(lambda: defaultdict(int))
    for r in recs:
        if r.get("sentinel") or r.get("arm") != "named":
            continue
        shares[r["channel"]]["n"] += 1
        if r["rung_pred"] == "UNCLASSIFIED":
            shares[r["channel"]]["uncl"] += 1
        elif r["rung_pred"] == "MALFORMED":
            shares[r["channel"]]["malformed"] += 1

    per_org = {}
    for org in orgs:
        gaps = org_gaps(depths, pairs, org)
        if len(gaps) < 3:  # PL0: >= 3 cross-family pairs required
            per_org[org] = {"status": "insufficient_pairs", "gaps": gaps}
            continue
        g = np.array(list(gaps.values()))
        gap_hat = float(np.mean(g))
        floor = float(np.std(g, ddof=1))
        resolved = abs(gap_hat) > SNR_K * floor
        # artifact-cluster bootstrap on gap_hat
        boots = []
        for _ in range(B_BOOT):
            bg = []
            for p in gaps:
                s_by = depths.get((org, "STATED"), {}).get(p, {})
                e_by = depths.get((org, "ENACTED"), {}).get(p, {})
                s_ids, e_ids = list(s_by), list(e_by)
                if not s_ids or not e_ids:
                    continue
                s_draw = [s_ids[i] for i in rng.integers(0, len(s_ids), len(s_ids))]
                e_draw = [e_ids[i] for i in rng.integers(0, len(e_ids), len(e_ids))]
                s = np.mean([v for a in s_draw for v in s_by[a]])
                e = np.mean([v for a in e_draw for v in e_by[a]])
                bg.append(s - e)
            if bg:
                boots.append(np.mean(bg))
        ci = (
            [round(float(np.percentile(boots, 2.5)), 3), round(float(np.percentile(boots, 97.5)), 3)]
            if boots
            else None
        )
        # H3 leave-one-out
        loo_ok = all(
            abs(gaps[p] - np.mean([gaps[q] for q in gaps if q != p])) <= SNR_K * floor
            for p in gaps
        ) if floor > 0 else True
        per_org[org] = {
            "status": "ok", "gaps": {k: round(v, 4) for k, v in gaps.items()},
            "gap_hat": round(gap_hat, 4), "floor": round(floor, 4),
            "resolved": bool(resolved), "ci95_cluster_boot": ci,
            "h3_loo_within_2floor": bool(loo_ok), "ai_announcer": flags.get(org),
        }
        for k in (1.5, 3.0):
            per_org[org][f"resolved_k{k}"] = bool(abs(gap_hat) > k * floor)

    ok_orgs = [o for o in orgs if per_org[o].get("status") == "ok"]
    resolved_orgs = [o for o in ok_orgs if per_org[o]["resolved"]]
    gap_hats_resolved = np.array([per_org[o]["gap_hat"] for o in resolved_orgs])
    gap_hats_all = np.array([per_org[o]["gap_hat"] for o in ok_orgs])

    # H2 on resolved orgs
    h2 = {"n_ok": len(ok_orgs), "n_resolved": len(resolved_orgs)}
    if len(resolved_orgs) >= 2:
        t, p_t = stats.ttest_1samp(gap_hats_resolved, 0.0)
        n_pos = int((gap_hats_resolved > 0).sum())
        p_sign = float(stats.binomtest(n_pos, len(gap_hats_resolved), 0.5).pvalue)
        h2.update(
            mean_gap=round(float(gap_hats_resolved.mean()), 4),
            sd_gap=round(float(gap_hats_resolved.std(ddof=1)), 4),
            cohens_d=round(float(gap_hats_resolved.mean() / gap_hats_resolved.std(ddof=1)), 3),
            t=round(float(t), 3), p_t=float(p_t), n_positive=n_pos, p_sign=p_sign,
            direction="stated deeper" if gap_hats_resolved.mean() > 0 else "enacted deeper",
            alpha=0.017,
            supported=bool(p_t < 0.017 and gap_hats_resolved.mean() > 0),
        )
    # KS co-primary on pooled depths
    pooled_s = [v for (o, c), byp in depths.items() if c == "STATED" for by in byp.values() for vv in by.values() for v in vv]
    pooled_e = [v for (o, c), byp in depths.items() if c == "ENACTED" for by in byp.values() for vv in by.values() for v in vv]
    ks, p_ks = stats.ks_2samp(pooled_s, pooled_e)
    h2["ks"] = {"D": round(float(ks), 4), "p": float(p_ks),
                "direction_agrees": bool(np.mean(pooled_s) - np.mean(pooled_e) > 0) == bool(h2.get("mean_gap", 0) > 0)}

    # permutation falsification: shuffle artifact channel labels within org
    org_art = defaultdict(lambda: defaultdict(dict))  # org -> artifact_key -> pair -> mean depth
    org_art_channel = defaultdict(dict)
    for (org, c), byp in depths.items():
        for p, by in byp.items():
            for aid, vv in by.items():
                org_art[org][(c, aid)][p] = float(np.mean(vv))
                org_art_channel[org][(c, aid)] = c
    perm_means = []
    for _ in range(N_PERM):
        vals = []
        for org in ok_orgs:
            arts = list(org_art[org])
            labels = [org_art_channel[org][a] for a in arts]
            perm = rng.permutation(labels)
            g = []
            for p in pairs:
                s = [org_art[org][a][p] for a, lab in zip(arts, perm) if lab == "STATED" and p in org_art[org][a]]
                e = [org_art[org][a][p] for a, lab in zip(arts, perm) if lab == "ENACTED" and p in org_art[org][a]]
                if s and e:
                    g.append(np.mean(s) - np.mean(e))
            if g:
                vals.append(np.mean(g))
        perm_means.append(float(np.mean(vals)))
    obs = float(gap_hats_all.mean()) if len(gap_hats_all) else float("nan")
    lo, hi = np.percentile(perm_means, [2.5, 97.5])
    h2["permutation"] = {"observed_panel_mean": round(obs, 4),
                         "perm95": [round(float(lo), 4), round(float(hi), 4)],
                         "outside": bool(obs < lo or obs > hi), "n_perm": N_PERM, "seed": SEED}

    # H3
    h3_pass = [o for o in resolved_orgs if per_org[o]["h3_loo_within_2floor"]]
    h3 = {"n_resolved": len(resolved_orgs), "n_all_pairs_within": len(h3_pass),
          "fraction": round(len(h3_pass) / len(resolved_orgs), 3) if resolved_orgs else None}

    # negative control: odd/even split pseudo-gap within org x channel
    neg = {"n_tested": 0, "n_pseudo_resolved": 0}
    for (org, c), byp in depths.items():
        aids = sorted({a for by in byp.values() for a in by})
        if len(aids) < 4:
            continue
        half1, half2 = set(aids[0::2]), set(aids[1::2])
        pg = []
        for p in byp:
            m1, m2 = mean_depth(byp[p], half1), mean_depth(byp[p], half2)
            if not (np.isnan(m1) or np.isnan(m2)):
                pg.append(m1 - m2)
        if len(pg) >= 3:
            neg["n_tested"] += 1
            if abs(np.mean(pg)) > SNR_K * np.std(pg, ddof=1):
                neg["n_pseudo_resolved"] += 1

    # contamination bound (masked subsample)
    depths_m = org_channel_depths(recs, "masked")
    contam = []
    for org in sorted({r["org"] for r in recs if r.get("arm") == "masked"}):
        gn = org_gaps(depths, pairs, org)
        gm = org_gaps(depths_m, pairs, org)
        common = set(gn) & set(gm)
        if len(common) >= 3:
            contam.append(np.mean([gm[p] for p in common]) - np.mean([gn[p] for p in common]))
    contamination = {"n_orgs": len(contam),
                     "mean_masked_minus_named": round(float(np.mean(contam)), 4) if contam else None,
                     "sd": round(float(np.std(contam, ddof=1)), 4) if len(contam) > 1 else None}

    # exploratory AI-announcer contrast
    ann = [per_org[o]["gap_hat"] for o in ok_orgs if per_org[o]["ai_announcer"]]
    non = [per_org[o]["gap_hat"] for o in ok_orgs if not per_org[o]["ai_announcer"]]
    contrast = {"n_announcers": len(ann), "n_non": len(non)}
    if len(ann) >= 2 and len(non) >= 2:
        t2, p2 = stats.ttest_ind(ann, non, equal_var=False)
        contrast.update(mean_announcer=round(float(np.mean(ann)), 4),
                        mean_non=round(float(np.mean(non)), 4),
                        welch_t=round(float(t2), 3), p=float(p2), exploratory=True)

    results = {
        "seed": SEED, "snr_k": SNR_K, "pairs": pairs,
        "n_orgs_read": len(orgs),
        "unclassified_malformed_shares": {
            c: {"n": v["n"], "unclassified_share": round(v["uncl"] / v["n"], 4),
                "malformed_share": round(v["malformed"] / v["n"], 4)}
            for c, v in shares.items()
        },
        "per_org": per_org, "H2": h2, "H3": h3,
        "negative_control": neg, "contamination_bound": contamination,
        "ai_announcer_contrast": contrast,
    }
    (DATA_DIR / "pl4_stage2_results.json").write_text(json.dumps(results, indent=2))
    print(json.dumps({k: results[k] for k in
                      ("n_orgs_read", "H2", "H3", "negative_control",
                       "contamination_bound", "ai_announcer_contrast",
                       "unclassified_malformed_shares")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
