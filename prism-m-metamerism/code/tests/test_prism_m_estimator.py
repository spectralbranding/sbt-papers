"""Unit tests for the PRISM-M PL4 estimator on synthetic data.

Run BEFORE any API spend (PL0 discipline):
    uv run pytest code/tests/ -q
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# The PRISM suites (prism_m / prism_c / prism_t) each carry flat modules named
# estimator/synthetic; purge any cached copy imported by a sibling suite so a
# whole-repo pytest run binds THIS suite's modules, not a sibling's.
for _m in ("estimator", "synthetic"):
    sys.modules.pop(_m, None)

import numpy as np  # noqa: E402

import estimator  # noqa: E402
import synthetic  # noqa: E402


def _indexed(records):
    idx = estimator.index_records(records)
    data = idx["data"]
    brands = sorted(data)
    op_pairs = sorted({op for b in data for ro in data[b] for op in data[b][ro]})
    return data, brands, op_pairs


def test_positive_control_flags_planted_pair():
    result = estimator.positive_control()
    assert result["passed"], result


def test_negative_control_same_brand_draws_do_not_flag():
    records = synthetic.synthetic_bank_records()
    data, brands, op_pairs = _indexed(records)
    result = estimator.negative_control(data, brands, op_pairs)
    assert result["passed"], result["failures"]


def test_metamer_pair_detected_and_distinct_pair_not():
    records = synthetic.synthetic_bank_records()
    data, brands, op_pairs = _indexed(records)
    rows = estimator.classify_pairs(data, brands, op_pairs)
    by_pair = {tuple(sorted(r["pair"])): r for r in rows}
    m = by_pair[("M1", "M2")]
    assert m["resolved_full"], m
    assert m["metameric_score"], m
    d = by_pair[("D1", "D2")]
    assert d["resolved_full"], d
    assert not d["metameric_score"], d


def test_near_identical_pair_not_resolved():
    records = synthetic.synthetic_bank_records()
    data, brands, op_pairs = _indexed(records)
    rows = estimator.classify_pairs(data, brands, op_pairs)
    by_pair = {tuple(sorted(r["pair"])): r for r in rows}
    s = by_pair[("S1", "S2")]
    assert not s["resolved_full"], s


def test_fraction_and_bootstrap_ci_bounds():
    records = synthetic.synthetic_bank_records()
    data, brands, op_pairs = _indexed(records)
    rows = estimator.classify_pairs(data, brands, op_pairs)
    f, num, den = estimator.metameric_fraction(rows, "score")
    assert f is not None and 0.0 <= f <= 1.0
    assert num <= den
    ci = estimator.bootstrap_fractions(data, brands, op_pairs, n_boot=200, seed=7)
    lo, hi = ci["score"]
    assert lo is not None and hi is not None and lo <= hi
    assert 0.0 <= lo <= 1.0 and 0.0 <= hi <= 1.0


def test_bootstrap_is_seed_deterministic():
    records = synthetic.synthetic_bank_records()
    data, brands, op_pairs = _indexed(records)
    a = estimator.bootstrap_fractions(data, brands, op_pairs, n_boot=100, seed=42)
    b = estimator.bootstrap_fractions(data, brands, op_pairs, n_boot=100, seed=42)
    assert a == b


def test_h1_confirms_on_synthetic_metamer():
    records = synthetic.synthetic_bank_records()
    data, brands, op_pairs = _indexed(records)
    rows = estimator.classify_pairs(data, brands, op_pairs)
    h1 = estimator.test_h1(data, rows, op_pairs, seed=7)
    assert h1["supported"], h1
    confirmed = {tuple(p["pair"]) for p in h1["pairs"]}
    assert ("M1", "M2") in confirmed


def test_h3_stable_across_op_pairs_on_synthetic():
    records = synthetic.synthetic_bank_records()
    data, brands, op_pairs = _indexed(records)
    ci = estimator.bootstrap_fractions(data, brands, op_pairs, n_boot=200, seed=7)
    h3 = estimator.test_h3(
        data, brands, op_pairs, aggregator="score", pooled_ci=ci["score"]
    )
    assert h3["per_op_pair_fraction"], h3
    # synthetic data has identical structure per op-pair -> low dispersion
    assert h3["dispersion"] <= 0.25


def test_analyze_end_to_end_runs():
    records = synthetic.synthetic_bank_records()
    result = estimator.analyze(records, skip_pair_boot=True)
    assert result["n_brands"] == 6
    assert set(result["fractions"]) == {"score", "rank", "pick"}
    assert result["negative_control"]["passed"]


def test_distance_metrics_alternates():
    a = np.array([9, 8, 3, 8, 3, 8, 3, 9], float)
    b = np.array([3, 3, 8, 3, 9, 3, 8, 3], float)
    assert estimator.dist_full(a, b, "cosine") > 0.2
    assert estimator.dist_full(a, b, "euclidean") > 0.1
    assert abs(estimator.dist_full(a, a, "cosine")) < 1e-12
