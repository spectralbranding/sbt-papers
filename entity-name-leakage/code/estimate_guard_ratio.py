# /// script
# requires-python = "==3.12.*"
# dependencies = ["numpy==2.4.3", "pyyaml==6.0.3"]
# ///
"""Phase-2: measure the guard's interaction/residual ratio from data already on disk.

NOT study code, and it collects nothing. It re-reads the FROZEN name-effect probe
records read-only and estimates the one quantity the power simulation cannot
assume: how large the text-by-entity interaction actually is, relative to the
within-cell residual.

Why this matters. The follow-up probe's guard compared the interaction against the
CLASS effect. Manipulation-check rule 2 Route B says the denominator must be the
WITHIN-CELL RESIDUAL, because a ratio taken against the main effect moves with the
main effect and with replicate count while the interaction is fixed. Nobody has
computed the residual-referenced ratio, so `simulate_guard_power.py` had to sweep
it. This pins it.

VALIDATION THAT CAN FAIL. Before reporting anything, the script recomputes the
probe's own published aggregate name effect (.824 run 1, .825 run 2, per
dimension). If this pipeline cannot reproduce those numbers to within .01, the
metric has been misunderstood and the script says so and exits nonzero rather than
reporting a ratio built on a misreading.

Run:
    uv run python code/estimate_guard_ratio.py --data-root <collection>

Reads only. Writes output/tables/guard_ratio.json. Deterministic; no seed needed.
"""

import argparse
import glob
import itertools
import json
import sys

import numpy as np
import yaml

import paths

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
PUBLISHED = {1: 0.824, 2: 0.825}  # the probe's own aggregate, per dimension
TOL = 0.01


def load(base):
    stim = yaml.safe_load(open(f"{base}/data/stimuli.yaml"))
    stratum = {e["entity"]: e["stratum"] for e in stim["nameswap"]}
    recs = []
    for f in sorted(glob.glob(f"{base}/data/run*/records_*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if r.get("arm") != "A2_NAMESWAP" or r.get("failed"):
                continue
            recs.append(r)
    return stratum, recs


def pair_class(s1, s2):
    inv1, inv2 = s1 == "P0", s2 == "P0"
    if inv1 and inv2:
        return "II"
    if inv1 != inv2:
        return "RI"
    return "RR_matched" if s1 == s2 else "RR_unmatched"


def vectors(recs):
    """(run, text, operator, entity) -> mean 8-vector over replicates."""
    acc = {}
    for r in recs:
        k = (r["run"], r["text_from"], r["operator"], r["entity"])
        acc.setdefault(k, []).append([r["vector"][d] for d in DIMS])
    return {k: np.mean(v, axis=0) for k, v in acc.items()}


def build(stratum, recs):
    vec = vectors(recs)
    keys = sorted({(k[0], k[1], k[2]) for k in vec})
    rows = []
    for run, text, op in keys:
        ents = sorted(e for (r, t, o, e) in vec if (r, t, o) == (run, text, op))
        for e1, e2 in itertools.combinations(ents, 2):
            diff = vec[(run, text, op, e1)] - vec[(run, text, op, e2)]
            # the probe's own per-dimension metric: Euclidean distance / sqrt(n_dims),
            # i.e. RMS -- NOT mean|delta|. See name_effect_probe/code/stats_core.py
            # (`euclidean` + `per_dimension`). Using mean|delta| under-reads it by ~30%.
            d = float(np.linalg.norm(diff) / np.sqrt(len(DIMS)))
            rows.append(
                {
                    "run": run,
                    "text": text,
                    "operator": op,
                    "cls": pair_class(stratum[e1], stratum[e2]),
                    "y": d,
                }
            )
    return rows


def two_way(rows):
    """Weighted text-by-class decomposition against the within-cell residual."""
    texts = sorted({r["text"] for r in rows})
    classes = ["II", "RR_matched", "RR_unmatched", "RI"]
    cell = {
        (t, c): [r["y"] for r in rows if r["text"] == t and r["cls"] == c]
        for t in texts
        for c in classes
    }
    n = np.array([[len(cell[(t, c)]) for c in classes] for t in texts], float)
    m = np.array(
        [
            [np.mean(cell[(t, c)]) if cell[(t, c)] else np.nan for c in classes]
            for t in texts
        ]
    )
    ss_within = sum(
        float(np.sum((np.array(v) - np.mean(v)) ** 2))
        for v in cell.values()
        if len(v) > 1
    )
    df_resid = int(n.sum() - np.count_nonzero(n))
    ms_resid = ss_within / df_resid

    grand = float((m * n).sum() / n.sum())
    row = (m * n).sum(axis=1) / n.sum(axis=1)
    col = (m * n).sum(axis=0) / n.sum(axis=0)
    inter = m - row[:, None] - col[None, :] + grand
    ss_inter = float((n * inter**2).sum())
    df_inter = (len(texts) - 1) * (len(classes) - 1)
    ms_inter = ss_inter / df_inter

    # variance-component form: E[MS_inter] = ms_resid + n_bar * var_inter
    n_bar = float(n.sum() / np.count_nonzero(n))
    var_inter = max((ms_inter - ms_resid) / n_bar, 0.0)
    return {
        "n_texts": len(texts),
        "n_obs": int(n.sum()),
        "ms_interaction": ms_inter,
        "ms_residual": ms_resid,
        "F": ms_inter / ms_resid,
        "df_interaction": df_inter,
        "df_residual": df_resid,
        "sd_interaction": var_inter**0.5,
        "sd_residual": ms_resid**0.5,
        "ratio_sd_interaction_over_sd_residual": (var_inter**0.5) / (ms_resid**0.5),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    paths.add_data_arg(ap)
    args = ap.parse_args()
    stratum, recs = load(paths.data_root(args, "estimate_guard_ratio.py"))
    rows = build(stratum, recs)

    # --- validation that can fail -------------------------------------------
    print("VALIDATION — reproducing the probe's own published aggregate\n")
    ok = True
    for run in (1, 2):
        got = float(np.mean([r["y"] for r in rows if r["run"] == run]))
        exp = PUBLISHED[run]
        good = abs(got - exp) <= TOL
        ok &= good
        print(
            f"  run {run}: recomputed {got:.3f}  published {exp:.3f}  "
            f"{'MATCH' if good else '*** MISMATCH ***'}"
        )
    if not ok:
        print(
            "\nFAILED: this pipeline does not reproduce the probe's published aggregate."
        )
        print("The pair metric has been misunderstood; no ratio is reported.")
        return 1
    print(
        "\n  -> the pipeline reproduces the published numbers; the metric is the right one\n"
    )

    out = {"validation": {f"run{r}": PUBLISHED[r] for r in PUBLISHED}, "runs": {}}
    print("RESIDUAL-REFERENCED GUARD, per run\n")
    for run in (1, 2):
        res = two_way([r for r in rows if r["run"] == run])
        out["runs"][f"run{run}"] = res
        print(f"  run {run}:  n={res['n_obs']} over {res['n_texts']} texts")
        print(
            f"      MS_interaction {res['ms_interaction']:.4f}   "
            f"MS_residual {res['ms_residual']:.4f}   F = {res['F']:.3f}"
            f"  (df {res['df_interaction']}, {res['df_residual']})"
        )
        print(
            f"      SD_interaction {res['sd_interaction']:.4f}   "
            f"SD_residual {res['sd_residual']:.4f}"
        )
        print(
            f"      RATIO (SD_inter / SD_resid) = "
            f"{res['ratio_sd_interaction_over_sd_residual']:.3f}\n"
        )

    ratios = [
        out["runs"][f"run{r}"]["ratio_sd_interaction_over_sd_residual"] for r in (1, 2)
    ]
    out["ratio_mean"] = float(np.mean(ratios))
    print(f"MEAN RATIO ACROSS RUNS = {np.mean(ratios):.3f}")
    print("\nThis is the number simulate_guard_power.py had to sweep. Read the")
    print("text-count requirement off that table at this ratio.")

    p = paths.out_dir() / "guard_ratio.json"
    json.dump(out, open(p, "w"), indent=2)
    print(f"\nWritten: {paths.rel(p)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
