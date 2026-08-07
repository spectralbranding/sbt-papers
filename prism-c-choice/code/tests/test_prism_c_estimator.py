"""PRISM-C PL4 unit suite — MUST pass before any API spend (session rule).

Run: uv run pytest code/tests/ -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

CODE = Path(__file__).resolve().parents[1]
RESEARCH = CODE.parents[1]
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(RESEARCH))
# The PRISM suites (prism_m / prism_c / prism_t) each carry flat modules named
# estimator/synthetic; purge any cached copy imported by a sibling suite so a
# whole-repo pytest run binds THIS suite's modules, not a sibling's.
for _m in ("estimator", "synthetic"):
    sys.modules.pop(_m, None)

import synthetic as syn  # noqa: E402
from estimator import (  # noqa: E402
    WEIGHTY_IDX,
    analyze,
    choice_floor,
    need_entropy,
    split_records,
)
from prism_c_lib import arrangements, parse_choice  # noqa: E402
from prism_core.concordance import (  # noqa: E402
    apply_exclusion_rule,
    pairwise_disagreement_floor,
)
from prism_core.stats import participation_ratio  # noqa: E402

RNG = np.random.default_rng(syn.SEED)


# ---------------------------------------------------------------------------
# Counterbalancing
# ---------------------------------------------------------------------------
def test_arrangements_n4_exactly_8_unique_balanced():
    opts = ["A", "B", "C", "D"]
    arrs = arrangements(opts, 8)
    assert len(arrs) == 8
    assert len({tuple(a) for a in arrs}) == 8
    firsts = [a[0] for a in arrs]
    for o in opts:
        assert firsts.count(o) == 2  # each option first exactly twice


def test_arrangements_small_sets_use_full_scheme():
    assert len(arrangements(["A", "B", "C"], 8)) == 6
    assert len(arrangements(["A", "B"], 8)) == 2
    # n=5: 8 arrangements, every option appears in first position
    arrs5 = arrangements(["A", "B", "C", "D", "E"], 8)
    assert len(arrs5) == 8
    assert {a[0] for a in arrs5} == {"A", "B", "C", "D", "E"}


def test_arrangements_deterministic():
    a1 = arrangements(["A", "B", "C", "D"], 8)
    a2 = arrangements(["A", "B", "C", "D"], 8)
    assert a1 == a2


# ---------------------------------------------------------------------------
# Choice parsing
# ---------------------------------------------------------------------------
def test_parse_choice_tolerates_fences_and_case():
    raw = '```json\n{"pick": "ikea", "ranking": ["IKEA", "Apple", "Sephora"]}\n```'
    out = parse_choice(raw, ["IKEA", "Apple", "Sephora"])
    assert out["pick"] == "IKEA"
    assert out["ranking"] == ["IKEA", "Apple", "Sephora"]


def test_parse_choice_accepts_descriptor_echo():
    raw = (
        '{"pick": "Rolex - luxury watches", "ranking": '
        '["Rolex - luxury watches", "Hermès - luxury fashion", '
        '"Apple - consumer technology", "Nike - sportswear"]}'
    )
    opts = ["Hermès", "Rolex", "Apple", "Nike"]
    out = parse_choice(raw, opts)
    assert out["pick"] == "Rolex"
    assert out["ranking"] == ["Rolex", "Hermès", "Apple", "Nike"]


def test_parse_choice_rejects_off_list_pick():
    with pytest.raises(ValueError):
        parse_choice('{"pick": "Nike"}', ["IKEA", "Apple"])


def test_parse_choice_drops_bad_ranking_keeps_pick():
    out = parse_choice(
        '{"pick": "Apple", "ranking": ["Apple", "Apple"]}', ["IKEA", "Apple"]
    )
    assert out["pick"] == "Apple"
    assert out["ranking"] is None


# ---------------------------------------------------------------------------
# Floors + exclusion rule
# ---------------------------------------------------------------------------
def test_pick_floor_zero_when_families_agree():
    picks = {"f1": ["A", "B"], "f2": ["A", "B"], "f3": ["A", "B"]}
    assert pairwise_disagreement_floor(picks) == 0.0


def test_pick_floor_counts_disagreement():
    picks = {"f1": ["A", "A"], "f2": ["A", "B"]}
    assert pairwise_disagreement_floor(picks) == pytest.approx(0.5)


def test_exclusion_rule_flags_discordant_family():
    scores = {"a": 0.05, "b": 0.06, "c": 0.055, "d": 0.30}
    res = apply_exclusion_rule(scores)
    assert [e["unit"] for e in res["excluded"]] == ["d"]
    assert set(res["kept"]) == {"a", "b", "c"}


def test_exclusion_rule_keeps_all_when_concordant():
    res = apply_exclusion_rule({"a": 0.05, "b": 0.06, "c": 0.055, "d": 0.07})
    assert not res["excluded"]


def test_participation_ratio_bounds():
    assert participation_ratio([1] * 8) == pytest.approx(8.0)
    assert participation_ratio([1, 0, 0, 0, 0, 0, 0, 0]) == pytest.approx(1.0)


def test_need_entropy_direction():
    flat = need_entropy(np.full(8, 5.0))
    peaked = need_entropy(np.array([9.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]))
    assert flat > peaked


# ---------------------------------------------------------------------------
# Fixtures: shared synthetic banks
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def bank():
    brands = syn.synth_brands(10)
    scenarios = syn.synth_scenarios(brands, n_scenarios=14, set_size=4)
    stated = syn.stated_records(brands)
    need = syn.need_records(scenarios)
    return brands, scenarios, stated, need


# ---------------------------------------------------------------------------
# H1 machinery
# ---------------------------------------------------------------------------
def test_h1_null_on_gap_free_data(bank):
    brands, scenarios, stated, need = bank
    choice = syn.choice_records_predicted(scenarios, brands)
    res = analyze(stated + need + choice)
    assert res["H1"]["divergence_rate"] == pytest.approx(0.0)
    assert res["H1"]["supported"] is False


def test_h1_detects_planted_reweighting_gap(bank):
    brands, scenarios, stated, need = bank
    beta = np.zeros(8)
    for i in WEIGHTY_IDX:
        beta[i] = 12.0  # choice uses ONLY the weighty dims (M1-style collapse)
    choice = syn.choice_records_cl(scenarios, brands, beta)
    res = analyze(stated + need + choice)
    # concordant families (identical deterministic picks) -> floor ~ FLOOR_MIN
    assert res["H1"]["divergence_rate"] > 0.1
    assert res["H1"]["supported"] is True


# ---------------------------------------------------------------------------
# H2 weight recovery + discrimination
# ---------------------------------------------------------------------------
def test_h2_supported_when_weighty_drive_choice(bank):
    brands, scenarios, stated, need = bank
    beta = np.zeros(8)
    for i in WEIGHTY_IDX:
        beta[i] = 12.0
    choice = syn.choice_records_cl(
        scenarios, brands, beta, gumbel_scale=0.3, rng=np.random.default_rng(7)
    )
    res = analyze(stated + need + choice)
    assert res["H2"]["supported"] is True
    # recovered weighty weights dominate the others
    w = res["H2"]["weights"]
    weighty_mean = np.mean([w["economic"], w["experiential"], w["social"]])
    other_mean = np.mean(
        [v for k, v in w.items() if k not in ("economic", "experiential", "social")]
    )
    assert weighty_mean > other_mean


def test_h2_not_supported_when_weighty_carry_nothing(bank):
    brands, scenarios, stated, need = bank
    beta = np.full(8, 8.0)
    for i in WEIGHTY_IDX:
        beta[i] = 0.0  # choice ignores the weighty set entirely
    choice = syn.choice_records_cl(
        scenarios, brands, beta, gumbel_scale=0.3, rng=np.random.default_rng(8)
    )
    res = analyze(stated + need + choice)
    assert res["H2"]["supported"] is False


# ---------------------------------------------------------------------------
# H3 position machinery
# ---------------------------------------------------------------------------
def test_h3_position_boost_detected(bank):
    brands, scenarios, stated, need = bank
    beta = np.full(8, 6.0)
    choice = syn.choice_records_cl(
        scenarios,
        brands,
        beta,
        position_boost=1.5,
        gumbel_scale=0.3,
        rng=np.random.default_rng(9),
    )
    res = analyze(stated + need + choice)
    # the first-position coefficient must come out positive
    assert res["H3"]["position_betas"]["first"] > 0


# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------
def test_positive_control_pass_and_fail():
    ok = analyze(syn.positive_control_records(obey=True))
    assert ok["positive_control"]["passed"] is True
    bad = analyze(syn.positive_control_records(obey=False))
    assert bad["positive_control"]["passed"] is False


def test_negative_control_pass_and_fail():
    ok = analyze(syn.negative_control_records(biased=False))
    assert ok["negative_control"]["passed"] is True
    bad = analyze(syn.negative_control_records(biased=True))
    assert bad["negative_control"]["passed"] is False


# ---------------------------------------------------------------------------
# End-to-end shape + determinism
# ---------------------------------------------------------------------------
def test_analyze_end_to_end_keys_and_determinism(bank):
    brands, scenarios, stated, need = bank
    beta = np.zeros(8)
    for i in WEIGHTY_IDX:
        beta[i] = 12.0
    records = (
        stated
        + need
        + syn.choice_records_cl(scenarios, brands, beta)
        + syn.positive_control_records()
        + syn.negative_control_records()
    )
    r1 = analyze(records)
    r2 = analyze(records)
    for key in (
        "H1",
        "H2",
        "H3",
        "mechanisms",
        "boundary",
        "positive_control",
        "negative_control",
        "exploratory",
    ):
        assert key in r1
    assert r1["H1"] == r2["H1"]  # seeded bootstrap => identical CIs
    assert (
        r1["mechanisms"]["M1a_participation_ratio"]["effective_dimensionality"] < 6.0
    )  # planted collapse onto 3 dims


def test_split_records_drops_malformed(bank):
    _, _, stated, _ = bank
    bad = dict(stated[0])
    bad["flagged_malformed"] = True
    parts = split_records(stated + [bad])
    assert len(parts["stated"]) == len(stated)


def test_choice_floor_on_mixed_families(bank):
    brands, scenarios, stated, need = bank
    beta_a = np.full(8, 6.0)
    rows = syn.choice_records_cl(scenarios, brands, beta_a)
    # perturb one family's picks to create disagreement
    for r in rows:
        if r["family"] == "deepseek":
            r["pick"] = r["arrangement"][0]
    fl = choice_floor(rows)
    assert fl > 0.0
