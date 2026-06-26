#!/usr/bin/env python3
"""Run 2 / Run 3 confirmatory statistics for R15 (paper 2026v).

Reproduces the one-sample DCI tests, the conditional-metamerism test, and the
per-dimension weight tables (Tables 4-5) reported in the confirmatory-results
section. Computed from the v3.1 dataset of record (the dataset of record on
HuggingFace; fetch with ../../reproduce.sh).

Unit of analysis = (brand_pair x model) cell DCI (one observation per pair x
model, averaged over the 3 repetitions); this avoids pseudo-replication across
repetitions and makes each table's Semiotic+Economic equal its one-sample DCI
mean exactly. DCI_response = (economic + semiotic) / 100 on weights renormalized
to sum to 100. Baseline mu0 = .250 (uniform: economic and semiotic both 12.5).
Bootstrap SE: 1,000 resamples, fixed seed 42.

Run:
    cd experiment
    ./reproduce.sh                      # fetches L3 logs from HuggingFace
    python L4_analysis/aggregate_runs_2_3_confirmatory.py
"""
from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

from scipy import stats

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
# v3.1 dataset of record (downloaded by reproduce.sh); fall back to L3_sessions.
HF_DATA = EXPERIMENT_DIR / "_hf" / "r15-ai-search-metamerism" / "data"
L3_DIR = EXPERIMENT_DIR / "L3_sessions"
DATA_DIR = HF_DATA if HF_DATA.exists() else L3_DIR

DIMS = ["semiotic", "narrative", "ideological", "experiential",
        "social", "economic", "cultural", "temporal"]
WEIGHTED_PROMPT_TYPES = {"weighted_recommendation", "weighted_recommendation_spec"}
SIX_MODELS = {"claude", "gpt", "gemini", "deepseek", "qwen3_local", "gemma4_local"}
MU0 = 0.25
SEED = 42
N_BOOT = 1000


def load(files: list[str]) -> list[dict]:
    recs = []
    for fn in files:
        path = DATA_DIR / fn
        if not path.exists():
            continue
        with path.open() as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("model") not in SIX_MODELS:
                    continue
                if r.get("prompt_type") not in WEIGHTED_PROMPT_TYPES:
                    continue
                parsed = r.get("parsed") or {}
                w = parsed.get("weights") if isinstance(parsed, dict) else None
                if not isinstance(w, dict):
                    continue
                try:
                    w = {d: float(w.get(d, 0)) for d in DIMS}
                except (TypeError, ValueError):
                    continue
                if not (90 <= sum(w.values()) <= 110):
                    continue
                s = sum(w.values())
                w = {k: v * 100.0 / s for k, v in w.items()}
                recs.append({"model": r["model"],
                             "pair": r.get("pair_id") or r.get("brand_pair"),
                             "w": w})
    return recs


def cells(recs: list[dict]) -> dict[tuple, dict]:
    grp = defaultdict(list)
    for r in recs:
        grp[(r["pair"], r["model"])].append(r["w"])
    return {k: {d: mean(w[d] for w in v) for d in DIMS} for k, v in grp.items()}


def dci(vec: dict) -> float:
    return (vec["economic"] + vec["semiotic"]) / 100.0


def boot_se(vals: list[float]) -> float:
    rng = random.Random(SEED)
    n = len(vals)
    return stdev([mean(rng.choice(vals) for _ in range(n)) for _ in range(N_BOOT)])


def one_sample(cell_dci: list[float]) -> tuple:
    n = len(cell_dci)
    m = mean(cell_dci)
    sd = stdev(cell_dci)
    d = (m - MU0) / sd
    t = d * math.sqrt(n)
    p = 2 * stats.t.sf(abs(t), n - 1)
    return n, m, sd, t, p, d


def main() -> None:
    r2 = cells(load(["run2_global.jsonl", "run2_qwen_plus.jsonl"]))
    r3 = cells(load(["run3_local.jsonl", "run3_qwen_plus.jsonl"]))

    for name, c in [("Run 2 (global)", r2), ("Run 3 (local)", r3)]:
        cd = [dci(v) for v in c.values()]
        n, m, sd, t, p, d = one_sample(cd)
        print(f"\n== {name}: one-sample DCI vs {MU0} ==")
        print(f"   n(cells)={n}  M={m:.3f}  SD={sd:.3f}  "
              f"t({n - 1})={t:.2f}  p={p:.2e}  Cohen d={d:.2f}")
        bm = defaultdict(list)
        for (_, mdl), v in c.items():
            bm[mdl].append(dci(v))
        pm = {mdl: round(mean(vs), 3) for mdl, vs in bm.items()}
        print(f"   per-model DCI: {pm}  all>{MU0}: {all(x > MU0 for x in pm.values())}")
        print("   per-dimension weight (bootstrap SE) [% of 12.5]:")
        for dn in DIMS:
            vals = [v[dn] for v in c.values()]
            print(f"     {dn.capitalize():12s} {mean(vals):4.1f} "
                  f"({boot_se(vals):.2f})  {round(100 * mean(vals) / 12.5)}%")

    gc = [dci(v) for v in r2.values()]
    lc = [dci(v) for v in r3.values()]
    t, p = stats.ttest_ind(lc, gc, equal_var=True)
    n1, n2 = len(lc), len(gc)
    sp = math.sqrt(((n1 - 1) * stdev(lc) ** 2 + (n2 - 1) * stdev(gc) ** 2) / (n1 + n2 - 2))
    d = (mean(lc) - mean(gc)) / sp
    print("\n== Conditional metamerism (independent samples, cell unit) ==")
    print(f"   global n={n2} M={mean(gc):.3f} | local n={n1} M={mean(lc):.3f}")
    print(f"   t({n1 + n2 - 2})={t:.2f}  p={p:.2e}  Cohen d={d:.2f}  "
          f"({100 * (mean(lc) - mean(gc)) / MU0:.1f}% more severe vs baseline)")


if __name__ == "__main__":
    main()
