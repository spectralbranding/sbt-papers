#!/usr/bin/env python3
"""Public-benchmark reconciliation — the substrate floor on real, external, cross-KIND data.

A genuinely EXTERNAL worked demonstration (instruments and data outside the spectral-branding
corpus): reconcile the ordinal claim "model A outperforms model B" across public LLM benchmarks
of different KINDS — MMLU (broad-knowledge MCQ), MATH (competition math), HumanEval (code
synthesis) — that share no raw output space. The reconciliation runs through the SAME committed
lattice as the corpus cases (code/substrate_floor.reconcile), proving the rule is
instrument-general, not corpus-specific.

Each benchmark is a noisy measurement of "is A better than B." Per instrument:
  margin       = acc_A - acc_B                              (signed advantage, proportion units)
  se_i         = sqrt(p(1-p)/N) per model; se = sqrt(se_A^2 + se_B^2)   (binomial sampling floor)
  z            = margin / se                                (two-proportion z statistic)
  verdict value= Phi(z) in [0,1]                            (confidence that A>B, the ordinal axis)
  status       = resolve iff |z| >= k_marginal, else abstain  (margin clears the instrument floor)
The substrate-axis floor is the 1-sigma resolution of the probability axis, Phi(1) - 0.5 ~ .341
(how finely an ordinal "A>B" verdict can be read at one standard error). The lattice then returns
the typed verdict. The per-instrument binomial floors differ by KIND mostly through N: HumanEval
(N=164) carries a far larger accuracy floor than MMLU (N=14042), so a few-point code gap can fall
BELOW HumanEval's floor and abstain while the same-size knowledge gap resolves — the nested-floor
discipline on real data.

Anti-fabrication: all accuracies + test-set sizes are pinned in the committed snapshot
data/public_benchmark_snapshot.yaml with full provenance + access date;
this script reads that file (no live board), so the result is reproducible and does not drift.

Reproduce:
    uv run --with pyyaml python code/public_benchmark_reconciliation.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit(
        "PyYAML required: uv run --with pyyaml python ... public_benchmark_reconciliation.py"
    )

RESEARCH = Path(__file__).resolve().parents[2]  # .../research
SF_DIR = Path(__file__).resolve().parents[1]  # .../this paper's folder
sys.path.insert(0, str(RESEARCH / "code"))
from substrate_floor import reconcile  # the SAME committed lattice the corpus cases use

K_MARGINAL = (
    1.0  # an instrument resolves the ranking iff its margin clears 1 sampling SE
)
K_RESOLVE = 2.0  # the consensus clears the substrate floor iff S/N >= 2
AXIS_FLOOR = 0.5 * (1 + math.erf(1 / math.sqrt(2))) - 0.5  # Phi(1) - 0.5 ~ .3413


def _phi(z: float) -> float:
    """Standard normal CDF via erf — no scipy dependency."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2)))


def _binom_se(p: float, n: int) -> float:
    return math.sqrt(max(p * (1 - p), 0.0) / n)


def build_case(snapshot: dict, claim: dict) -> tuple[dict, list[dict]]:
    """Build a substrate_floor reconciliation case for one 'A outperforms B' claim."""
    a, b = claim["a"], claim["b"]
    rows = []
    verdicts = []
    for inst in claim["instruments"]:
        bench = snapshot["benchmarks"][inst]
        n = int(bench["n"])
        acc_a = float(snapshot["models"][a][inst])
        acc_b = float(snapshot["models"][b][inst])
        margin = acc_a - acc_b
        se = math.sqrt(_binom_se(acc_a, n) ** 2 + _binom_se(acc_b, n) ** 2)
        z = margin / se if se > 0 else 0.0
        value = _phi(z)
        status = "resolve" if abs(z) >= K_MARGINAL else "abstain"
        rows.append(
            {
                "instrument": inst,
                "kind": bench["kind"],
                "margin_pp": round(margin * 100, 2),
                "floor_pp": round(se * 100, 2),
                "z": round(z, 2),
                "value": round(value, 3),
                "status": status,
            }
        )
        verdicts.append(
            {
                "substrate": inst,
                "claim_ref": f"{inst}: {a} vs {b}",
                "alignment": "exactMatch",  # one shared ordinal claim "A outperforms B"
                "status": status,
                "value": round(value, 4),
                "self_floor": round(AXIS_FLOOR, 4),
                "audit_pass": True,
            }
        )
    case = {
        "name": f"{a}_vs_{b}_{claim['label']}",
        "shared_claim": {
            "id": f"C-{claim['label']}",
            "text": f"{a} outperforms {b}.",
            "common_axis": "P(A outperforms B) in [0,1] from a two-proportion z-test per benchmark",
        },
        "k_resolve": K_RESOLVE,
        "k_marginal": K_MARGINAL,
        "substrate_verdicts": verdicts,
    }
    return case, rows


def main() -> None:
    snap_path = SF_DIR / "data" / "public_benchmark_snapshot.yaml"
    snapshot = yaml.safe_load(snap_path.read_text())

    print("# Public-benchmark reconciliation (substrate floor on real cross-KIND data)")
    print(f"# snapshot: {snapshot['source']}")
    print(
        f"# instrument floors are binomial SEs from documented N; axis floor Phi(1)-0.5 = {AXIS_FLOOR:.3f}\n"
    )

    # one-time per-instrument accuracy floors (N-driven), for the prose
    print(
        "Per-benchmark accuracy floor (binomial SE at ~85% accuracy, by test-set size N):"
    )
    for name, b in snapshot["benchmarks"].items():
        se = _binom_se(0.85, int(b["n"]))
        print(f"  {name:10s} N={b['n']:>6}  floor ~= {se*100:.2f} pp   ({b['kind']})")
    print()

    n_ok = 0
    for claim in snapshot["claims"]:
        case, rows = build_case(snapshot, claim)
        result = reconcile(case)
        verdict = result.get("verdict", result.get("errors"))
        print(
            f"## claim: {claim['a']} outperforms {claim['b']}  via {claim['instruments']}"
        )
        for r in rows:
            print(
                f"   {r['instrument']:10s} margin {r['margin_pp']:+6.2f}pp  floor {r['floor_pp']:.2f}pp  "
                f"z={r['z']:+.2f}  value={r['value']:.3f}  -> {r['status']}"
            )
        print(f"   => VERDICT: {str(verdict).upper()}")
        print(f"      {result.get('rationale', '')}\n")
        n_ok += 1

    print(
        f"[public-benchmark] {n_ok} reconciliation(s) computed from the committed snapshot."
    )


if __name__ == "__main__":
    main()
