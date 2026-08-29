# /// script
# requires-python = "==3.12.*"
# dependencies = ["numpy==2.4.3"]
# ///
"""Does the leakage concentrate on particular dimensions, or spread across them?

A reviewer will ask, and the frozen records answer it. Reads only.

VALIDATION THAT CAN FAIL: the root-mean-square of the per-dimension means must
reproduce the published aggregate (.824 / .825) to within .02, since the
aggregate IS the RMS over dimensions. If it does not, the decomposition is not
of the reported quantity and the script says so.

Run:
    uv run python code/per_dimension_leakage.py --data-root <collection>
"""

import argparse
import glob
import itertools
import json
import sys

import numpy as np

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
PUBLISHED = {1: 0.824, 2: 0.825}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    paths.add_data_arg(ap)
    args = ap.parse_args()
    base = paths.data_root(args, "per_dimension_leakage.py")

    recs = []
    for f in sorted(glob.glob(f"{base}/data/run*/records_*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if r.get("arm") == "A2_NAMESWAP" and not r.get("failed"):
                recs.append(r)
    acc = {}
    for r in recs:
        acc.setdefault(
            (r["run"], r["text_from"], r["operator"], r["entity"]), []
        ).append([r["vector"][d] for d in DIMS])
    vec = {k: np.mean(v, axis=0) for k, v in acc.items()}

    out = {}
    print("Per-dimension absolute movement under a name exchange\n")
    print(f"{'dimension':<14}  run 1   run 2")
    print("-" * 32)
    per = {}
    for run in (1, 2):
        keys = sorted({(k[1], k[2]) for k in vec if k[0] == run})
        diffs = []
        for text, op in keys:
            ents = sorted(e for (r, t, o, e) in vec if (r, t, o) == (run, text, op))
            for a, b in itertools.combinations(ents, 2):
                diffs.append(np.abs(vec[(run, text, op, a)] - vec[(run, text, op, b)]))
        per[run] = np.mean(diffs, axis=0)
    for i, d in enumerate(DIMS):
        print(f"{d:<14}  {per[1][i]:.3f}   {per[2][i]:.3f}")
        out[d] = [float(per[1][i]), float(per[2][i])]

    print("\nVALIDATION — RMS over dimensions must reproduce the published aggregate\n")
    ok = True
    for run in (1, 2):
        keys = sorted({(k[1], k[2]) for k in vec if k[0] == run})
        mags = []
        for text, op in keys:
            ents = sorted(e for (r, t, o, e) in vec if (r, t, o) == (run, text, op))
            for a, b in itertools.combinations(ents, 2):
                diff = vec[(run, text, op, a)] - vec[(run, text, op, b)]
                mags.append(np.linalg.norm(diff) / np.sqrt(len(DIMS)))
        got = float(np.mean(mags))
        good = abs(got - PUBLISHED[run]) <= 0.02
        ok &= good
        print(
            f"  run {run}: {got:.3f} vs published {PUBLISHED[run]:.3f}  "
            f"{'MATCH' if good else '*** MISMATCH ***'}"
        )
    if not ok:
        print("\nFAILED: decomposition is not of the reported quantity.")
        return 1

    spread = {r: (per[r].max() - per[r].min()) for r in (1, 2)}
    ratio = {r: (per[r].max() / per[r].min()) for r in (1, 2)}
    print(f"\nmax/min ratio: run 1 {ratio[1]:.2f}x, run 2 {ratio[2]:.2f}x")
    print(f"range: run 1 {spread[1]:.3f}, run 2 {spread[2]:.3f} rubric points")
    top = {r: DIMS[int(np.argmax(per[r]))] for r in (1, 2)}
    bot = {r: DIMS[int(np.argmin(per[r]))] for r in (1, 2)}
    print(f"largest: run 1 {top[1]}, run 2 {top[2]}")
    print(f"smallest: run 1 {bot[1]}, run 2 {bot[2]}")
    print(
        "\nAgreement on which dimension moves most/least across runs is the"
        "\nreproducibility question; a swap means the ordering is not stable."
    )

    json.dump(
        {"per_dimension": out, "max_min_ratio": ratio, "range": spread},
        open(paths.out_dir() / "per_dimension.json", "w"),
        indent=2,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
