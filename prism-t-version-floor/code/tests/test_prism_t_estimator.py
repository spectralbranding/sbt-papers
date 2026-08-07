"""Unit suite for the PRISM-T PL4 estimator — must pass BEFORE any API spend.

Runs the real estimator on seeded synthetic record sets (synthetic.py):
planted drift is detected, the null abstains, H3 is set-specific, the H2
decomposition recovers a planted brand signal, and controls behave.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# The PRISM suites (prism_m / prism_c / prism_t) each carry flat modules named
# estimator/synthetic; purge any cached copy imported by a sibling suite so a
# whole-repo pytest run binds THIS suite's modules, not a sibling's.
for _m in ("estimator", "synthetic"):
    sys.modules.pop(_m, None)
import estimator  # noqa: E402
from prism_t_lib import H3_FORMAT_ANCHORED  # noqa: E402
from synthetic import gen_records  # noqa: E402

estimator.N_BOOT = 500  # test-speed bootstrap; confirmatory uses 2000


def test_planted_drift_detected():
    records, cfg = gen_records(n_brands=30, sigma_op=0.2, drift=1.0, seed=11)
    res = estimator.analyze(records, cfg, seed=11)
    assert res["h1_supported"] is True
    h3 = res["ladders"]["fam-a-ladder"]["h3"]
    assert h3["mean_diff"] > 0
    assert h3["p_one_sided"] < 0.017


def test_null_abstains():
    records, cfg = gen_records(n_brands=30, sigma_op=0.2, drift=0.0, seed=12)
    res = estimator.analyze(records, cfg, seed=12)
    assert res["h1_supported"] is False
    neg = res["negative_control"]
    assert neg["n_brands"] == 30
    assert neg["pass_mean"] is True


def test_h3_set_specificity():
    # drift planted on the FORMAT-ANCHORED set must not support H3
    records, cfg = gen_records(
        n_brands=30,
        sigma_op=0.2,
        drift=1.0,
        drift_dims=H3_FORMAT_ANCHORED,
        seed=13,
    )
    res = estimator.analyze(records, cfg, seed=13)
    h3 = res["ladders"]["fam-a-ladder"]["h3"]
    assert h3["mean_diff"] < 0
    assert h3["p_one_sided"] > 0.5


def test_version_floor_bounds_pair_distances():
    records, cfg = gen_records(n_brands=10, sigma_op=0.2, drift=0.5, seed=14)
    readings = estimator.brand_readings(records)
    brands = sorted({r["brand"] for r in records})
    ladder = cfg["ladders"]["fam-a-ladder"]
    vd = estimator.version_distances(readings, ladder, brands)
    vf = estimator.version_floor_per_brand(vd, brands)
    for pair_dists in vd.values():
        for b, d in pair_dists.items():
            assert d <= vf[b] + 1e-12


def test_positive_control_designation():
    records, cfg = gen_records(n_brands=10, sigma_op=0.2, drift=0.5, seed=15)
    res = estimator.analyze(records, cfg, seed=15)
    pairs = res["ladders"]["fam-a-ladder"]["pairs"]
    pos = [k for k, p in pairs.items() if p["positive_control"]]
    assert pos == ["R0 -> R2"]
    # h1_supported must not rest on the positive-control pair alone
    non_pos_hits = [
        k for k, p in pairs.items() if p["drifts_at_k"] and not p["positive_control"]
    ]
    assert res["h1_supported"] == bool(non_pos_hits)


def test_h2_decomposition_recovers_brand_signal():
    records, cfg = gen_records(
        n_brands=30,
        sigma_op=0.2,
        drift=0.3,
        brand_signal=1.5,
        two_epochs=True,
        seed=16,
    )
    brands = sorted({r["brand"] for r in records})
    ladder = cfg["ladders"]["fam-a-ladder"]
    h2 = estimator.h2_decomposition(
        records, ladder, brands, epoch_pair=("VE-1", "VE-2"), seed=16
    )
    assert h2["n_brands"] == 30
    # live drift must exceed pinned drift; the signal estimate is positive
    assert h2["mean_live_drift"] > h2["mean_pinned_version_floor"]
    assert h2["mean_brand_signal"] > 0
    assert h2["ci95"][0] > 0


def test_h2_null_when_no_signal():
    records, cfg = gen_records(
        n_brands=30,
        sigma_op=0.2,
        drift=0.3,
        brand_signal=0.0,
        two_epochs=True,
        seed=17,
    )
    brands = sorted({r["brand"] for r in records})
    ladder = cfg["ladders"]["fam-a-ladder"]
    h2 = estimator.h2_decomposition(
        records, ladder, brands, epoch_pair=("VE-1", "VE-2"), seed=17
    )
    assert h2["ci95"][0] <= 0 <= h2["ci95"][1]


def test_ve1_alone_has_no_live_comparison():
    records, cfg = gen_records(n_brands=5, sigma_op=0.2, drift=0.3, seed=18)
    brands = sorted({r["brand"] for r in records})
    ladder = cfg["ladders"]["fam-a-ladder"]
    h2 = estimator.h2_decomposition(
        records, ladder, brands, epoch_pair=("VE-1", "VE-2"), seed=18
    )
    assert h2["n_brands"] == 0


def test_operator_exclusion_respected():
    records, cfg = gen_records(n_brands=10, sigma_op=0.2, drift=0.0, seed=19)
    res_all = estimator.analyze(records, cfg, seed=19)
    res_excl = estimator.analyze(records, cfg, excluded_ops={"OP4"}, seed=19)
    assert res_excl["excluded_ops"] == ["OP4"]
    assert (
        res_all["operator_floor"]["mean"] >= res_excl["operator_floor"]["mean"] - 1e-9
    )
