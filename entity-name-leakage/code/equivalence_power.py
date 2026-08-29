# /// script
# requires-python = "==3.12.*"
# dependencies = ["numpy==2.4.3"]
# ///
"""Phase-2: how many texts are needed to DEMONSTRATE neutrality, not merely fail to reject it.

`estimate_guard_ratio.py` measured the residual-referenced text-by-entity
interaction on the frozen probe data: SD_interaction / SD_residual = .066 and .039
across two runs, mean .053. Both F-tests are far from significant.

That changes the question. Manipulation-check rule 2 Route B is explicit that
"not rejected" is never "neutral", so a non-significant F establishes nothing. What
the design owes is an EQUIVALENCE statement: an upper confidence bound on the
interaction ratio that sits below a pre-specified bound.

This script asks: at the measured ratio, how does the 95% upper confidence bound on
the interaction ratio shrink with the number of texts? Read the required text count
off the bound the author is willing to defend.

Rule 5 applies to that bound and is NOT discharged here: a threshold must be
grounded, and stated relative to the value it takes when the effect is absent. This
script supplies the sampling behaviour; it does not invent the bound.

Run:
    uv run python code/equivalence_power.py

Seed is fixed. Output is deterministic.
"""

import json

import numpy as np

import paths

SEED = 20260829
N_SIM = 3000
N_TEXTS = [4, 8, 12, 16, 20, 24, 32, 48]
CELL_N = {"II": 15, "RR_matched": 30, "RR_unmatched": 45, "RI": 90}
CLASSES = list(CELL_N)
CLASS_MEAN = np.array([0.95, 1.16, 1.14, 1.13])
S_TEXT = 0.35
S_RESID = 0.42  # measured: SD_residual .420 / .425
TRUE_RATIO = 0.053  # measured mean across the two runs


def one(rng, n_text, ratio):
    n_c = np.array([CELL_N[c] for c in CLASSES])
    t_eff = rng.normal(0.0, S_TEXT, size=n_text)
    tc = rng.normal(0.0, ratio * S_RESID, size=(n_text, len(CLASSES)))
    cell_sum = np.zeros((n_text, len(CLASSES)))
    ss_within = 0.0
    for j, n in enumerate(n_c):
        mu = CLASS_MEAN[j] + t_eff[:, None] + tc[:, j][:, None]
        y = rng.normal(mu, S_RESID, size=(n_text, n))
        cell_sum[:, j] = y.sum(axis=1)
        ss_within += ((y - y.mean(axis=1, keepdims=True)) ** 2).sum()
    m = cell_sum / n_c[None, :]
    df_resid = n_text * n_c.sum() - n_text * len(CLASSES)
    ms_resid = ss_within / df_resid
    w = np.broadcast_to(n_c[None, :], m.shape)
    grand = (m * w).sum() / w.sum()
    row = (m * w).sum(axis=1) / w.sum(axis=1)
    col = (m * w).sum(axis=0) / w.sum(axis=0)
    inter = m - row[:, None] - col[None, :] + grand
    ms_inter = (w * inter**2).sum() / ((n_text - 1) * (len(CLASSES) - 1))
    n_bar = n_c.sum() / len(CLASSES)
    var_inter = max((ms_inter - ms_resid) / n_bar, 0.0)
    return float(np.sqrt(var_inter) / np.sqrt(ms_resid))


def main():
    rng = np.random.default_rng(SEED)
    print(
        f"Sampling behaviour of the interaction ratio at the MEASURED true value "
        f"{TRUE_RATIO:.3f}\n"
    )
    print(" n_texts |  median |  95th pct (upper bound you could defend)")
    print("-" * 58)
    out = {"true_ratio": TRUE_RATIO, "n_sim": N_SIM, "seed": SEED, "rows": []}
    for n_text in N_TEXTS:
        est = np.array([one(rng, n_text, TRUE_RATIO) for _ in range(N_SIM)])
        med, p95 = float(np.median(est)), float(np.percentile(est, 95))
        out["rows"].append({"n_texts": n_text, "median": med, "p95": p95})
        print(f" {n_text:7d} |  {med:.3f}  |  {p95:.3f}")

    print("\nReading. The 95th percentile is what an unlucky-but-honest run would")
    print("report as its upper bound. A design can only DEMONSTRATE neutrality")
    print("below a bound that sits above this number.")
    print("\nNOTE the four-text row: it is the collected design, and its upper bound")
    print("is why the existing data cannot settle neutrality even though its point")
    print("estimate is small.")

    p = paths.out_dir() / "equivalence_power.json"
    json.dump(out, open(p, "w"), indent=2)
    print(f"\nWritten: {paths.rel(p)}")


if __name__ == "__main__":
    main()
