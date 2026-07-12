#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""gen_web_appendix.py — render WEB_APPENDIX.md from the frozen estimator output.

Deterministic projection: every table value is read verbatim from
data/results.json (frozen estimator, seed 20260712) and
data/metameric_check.json (supplementary pre-registered check, amendment A4).
No value is computed here beyond formatting; re-running after re-running the
estimator regenerates the appendix byte-identically.

Tables: A1 per-operator floor panel; A2 induced-matrix detail per category
(S, share vector, closed-form diagonal, observed repeat propensities);
A3 intermediate-band mass and cohort-profile dispersion; A4 metameric pairs.

Run:
    uv run python code/gen_web_appendix.py
"""

from __future__ import annotations

import json
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parent.parent

CATEGORY_LABELS = {
    "coffee_roasters": "Specialty coffee (synthetic, Study 1)",
    "qsr_coffee": "Quick-service coffee (Study 2)",
    "athletic_footwear": "Athletic footwear (Study 2)",
}

OPERATOR_MODELS = {
    "OP1": "claude-sonnet-5",
    "OP2": "claude-haiku-4-5-20251001",
    "OP3": "gpt-5.5-2026-04-23",
    "OP4": "gpt-5.4-mini-2026-03-17",
    "OP5": "deepseek-v4-pro",
    "OP6": "deepseek-v4-flash",
}


def fmt(x: float, nd: int = 3) -> str:
    """AMA decimal format: no leading zero for |x| < 1."""
    s = f"{x:.{nd}f}"
    if s.startswith("0."):
        s = s[1:]
    elif s.startswith("-0."):
        s = "-" + s[2:]
    return s


def main() -> None:
    results = json.loads((PAPER_DIR / "data" / "results.json").read_text())
    metameric = json.loads((PAPER_DIR / "data" / "metameric_check.json").read_text())

    out = []
    out.append("# Web Appendix — Perception Sets the Matrix (2026bf)\n")
    out.append(
        "All values in this appendix are read verbatim from the frozen "
        "estimator output (`data/results.json`, seed "
        f"{results['seed']}, {results['n_permutations']:,}-draw permutation "
        "nulls) and the supplementary metameric check "
        "(`data/metameric_check.json`, protocol amendment A4). Regenerate "
        "with `uv run python code/gen_web_appendix.py`.\n"
    )

    # A1 — per-operator floor panel
    out.append("## Table A1: Per-Operator Floor Panel.\n")
    out.append(
        "| Operator | Model | F1 ICC(2,1) | F2 sum-check rate | F2 Juster "
        "tau | F3 recovery MAD | F4 failure rate | Passes all |"
    )
    out.append("|---|---|---|---|---|---|---|---|")
    for op in sorted(results["operators"]):
        o = results["operators"][op]
        out.append(
            f"| {op} | {OPERATOR_MODELS[op]} | {fmt(o['F1_icc'])} | "
            f"{fmt(o['F2_sumcheck_rate'])} | {fmt(o['F2_juster_tau'])} | "
            f"{o['F3_mad']:.3f} | {fmt(o['F4_failure_rate'])} | "
            f"{'yes' if o['pass_all'] else 'no'} |"
        )
    out.append(
        "\n*Notes*: Frozen floors — F1 reading test-retest ICC(2,1) >= .60; "
        "F2 constant-sum check rate >= .95 and Juster-vs-constant-sum rank "
        "agreement tau >= .5; F3 known-profile recovery mean absolute "
        "deviation <= 1.5 scale points per dimension (authored Study-1 "
        "targets); F4 refusal/malformed-output rate <= .05. OP1 was demoted "
        "on F2 and F4 per the frozen demotion rule and excluded from the "
        "primary pool (reported in the paper).\n"
    )

    # A2 — induced-matrix detail
    out.append("## Table A2: Induced-Matrix Detail by Category.\n")
    for cat, label in CATEGORY_LABELS.items():
        c = results["categories"][cat]
        im = c["induced_matrix"]
        brands = list(im["observed_repeat_by_brand"])
        out.append(f"### {label}\n")
        out.append(
            f"Concentration S = {im['S']:.3f}; induced diagonal vs observed "
            f"repeat ordering tau = {fmt(im['dj_diag_vs_observed_repeat_tau'])}.\n"
        )
        out.append("| Brand | Share s | Closed-form diagonal | Observed repeat |")
        out.append("|---|---|---|---|")
        for i, b in enumerate(brands):
            out.append(
                f"| {b} | {fmt(im['s'][i])} | {fmt(im['diagonal'][i])} | "
                f"{fmt(im['observed_repeat_by_brand'][b])} |"
            )
        out.append("")
    out.append(
        "*Notes*: Share vector s from mean propensity shares; S by "
        "moment-matching the across-cohort propensity dispersion to the "
        "Dirichlet variance relation; diagonal from the closed form "
        "P = (I + S 1 s^T) / (S + 1). Observed repeat propensities from the "
        "descriptive switching probes (illustrative arm).\n"
    )

    # A3 — band mass and dispersion
    out.append("## Table A3: Intermediate-Band Mass and Cohort-Profile Dispersion.\n")
    out.append("| Category | Band mass | Cohort-profile dispersion |")
    out.append("|---|---|---|")
    for cat, label in CATEGORY_LABELS.items():
        c = results["categories"][cat]
        out.append(
            f"| {label} | {fmt(c['band']['mass'])} | "
            f"{c['band']['cohort_dispersion']:.3f} |"
        )
    out.append(
        "\n*Notes*: The space-filling cohort design fixed dispersion nearly "
        "constant across categories, so the pre-registered dispersion-"
        "tracking secondary had no leverage this campaign (band mass tracked "
        "link strength instead); the dispersion prediction awaits a design "
        "that varies dispersion deliberately.\n"
    )

    # A4 — metameric pairs
    out.append("## Table A4: Operator-Level Metameric Pairs (Amendment A4).\n")
    out.append(
        "| Category | Operator | Pair | Profile distance | Reading floor | "
        "Median propensity diff | Elicitation floor | Within floor |"
    )
    out.append("|---|---|---|---|---|---|---|---|")
    for p in metameric["metameric_pairs"]:
        out.append(
            f"| {p['category']} | {p['operator']} | "
            f"{p['pair'][0]} - {p['pair'][1]} | {p['profile_distance']:.3f} | "
            f"{p['pair_reading_floor']:.3f} | "
            f"{fmt(p['median_abs_propensity_diff'])} | "
            f"{fmt(p['elicitation_floor'])} | "
            f"{'yes' if p['within_elicitation_floor'] else 'no'} |"
        )
    out.append(
        "\n*Notes*: A pair is metameric for an operator when the distance "
        "between the operator's median brand profiles falls below that "
        "operator's own reading floor. In all six pairs the median cohort "
        "propensity difference exceeds the elicitation floor — the "
        "metameric-equality prediction (P4) is violated where exercisable.\n"
    )

    (PAPER_DIR / "WEB_APPENDIX.md").write_text("\n".join(out))
    print(f"Wrote {PAPER_DIR / 'WEB_APPENDIX.md'}")


if __name__ == "__main__":
    main()
