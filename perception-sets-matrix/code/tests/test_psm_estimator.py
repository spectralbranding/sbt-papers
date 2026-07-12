"""Unit suite for the 2026bf estimator — runs BEFORE any API spend.

Controls (pre-registered):
  - planted positive: propensities generated as a monotone function of the
    designed match -> the estimator must detect the link and the
    random-profile falsification must destroy it;
  - null: propensities independent of match -> no category-level pass;
  - weighted planted: propensities generated from salience-WEIGHTED match ->
    delta_tau_w must come out positive.
Plus kernel tests: tau_b, ICC, isotonic PAV, induced matrix, parsers.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
PAPER_DIR = CODE.parent
sys.path.insert(0, str(CODE))

import estimator as E  # noqa: E402
import psm_lib as L  # noqa: E402

PROTO = yaml.safe_load((PAPER_DIR / "PROTOCOL.yaml").read_text())
PERSONAS = yaml.safe_load((PAPER_DIR / "PERSONAS.yaml").read_text())["categories"]
S1 = yaml.safe_load((PAPER_DIR / "STIMULI_STUDY1.yaml").read_text())
CAT = "coffee_roasters"
BRANDS = [b["name"] for b in S1["brands"]]
TARGETS = {b["name"]: np.array(b["target_profile"]) for b in S1["brands"]}


# ---------------------------------------------------------------------------
# Kernel tests
# ---------------------------------------------------------------------------
def test_kendall_tau_b_known():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    assert E.kendall_tau_b(x, x) == pytest.approx(1.0)
    assert E.kendall_tau_b(x, -x) == pytest.approx(-1.0)
    y = np.array([1, 3, 2, 4, 5], dtype=float)
    assert E.kendall_tau_b(x, y) == pytest.approx(0.8)


def test_icc_perfect_and_noisy():
    targets = np.repeat(np.arange(10, dtype=float)[:, None], 3, axis=1)
    assert E.icc_2_1(targets) == pytest.approx(1.0)
    rng = np.random.default_rng(0)
    noisy = targets + rng.normal(0, 3.0, targets.shape)
    assert E.icc_2_1(noisy) < 0.9


def test_isotonic_fit_monotone():
    m = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    p = np.array([0.0, 0.3, 0.2, 0.5, 0.6])
    f = E.isotonic_fit(m, p)
    order = np.argsort(m)
    assert np.all(np.diff(f[order]) >= -1e-12)


def test_induced_matrix_properties():
    s = np.array([0.4, 0.3, 0.2, 0.1])
    S = 2.5
    P = (np.eye(4) + S * np.outer(np.ones(4), s)) / (S + 1)
    assert np.allclose(P.sum(axis=1), 1.0)
    assert np.allclose(s @ P, s)  # stationary
    assert np.all(np.diff(np.diag(P)[np.argsort(s)]) >= 0)  # DJ ordering


def test_parse_elicitation_and_samecall():
    names = ["A", "B"]
    raw = json.dumps(
        {
            "constant_sum": {"A": 7, "B": 3},
            "juster": {"A": 8, "B": 4},
            "switching": {"current_brand": "A", "next_purchase": {"A": 0.7, "B": 0.3}},
        }
    )
    out = L.parse_elicitation("```json\n" + raw + "\n```", names)
    assert out["constant_sum"] == {"A": 7, "B": 3}
    bad = json.dumps({"constant_sum": {"A": 5, "B": 3}, "juster": {"A": 1, "B": 1}})
    with pytest.raises(ValueError):
        L.parse_elicitation(bad, names)
    sc = json.dumps(
        {
            "readings": {
                "A": {d: 5 for d in L.DIMENSIONS},
                "B": {d: 7 for d in L.DIMENSIONS},
            },
            "constant_sum": {"A": 4, "B": 6},
        }
    )
    out2 = L.parse_samecall(sc, names)
    assert out2["readings"]["B"] == [7.0] * 8


# ---------------------------------------------------------------------------
# Synthetic campaign generator
# ---------------------------------------------------------------------------
def largest_remainder(weights: np.ndarray, total: int = 10) -> np.ndarray:
    raw = weights / weights.sum() * total
    base = np.floor(raw).astype(int)
    rem = total - base.sum()
    order = np.argsort(-(raw - base))
    base[order[:rem]] += 1
    return base


def synth_records(tmp_path: Path, mode: str) -> str:
    """mode: 'planted' | 'null' | 'weighted'."""
    rng = np.random.default_rng(42)
    personas = PERSONAS[CAT]
    for op_id in ["OP1", "OP3"]:
        path = tmp_path / f"records_{op_id}.jsonl"
        rows = []
        for bname, target in TARGETS.items():
            for rep in range(3):
                rows.append(
                    {
                        "record_key": f"readings|{op_id}|{CAT}|{bname}|r{rep}",
                        "arm": "readings",
                        "operator": op_id,
                        "model": "m",
                        "family": "f",
                        "category": CAT,
                        "brand": bname,
                        "replicate": rep,
                        "payload": list(np.clip(target + rng.normal(0, 0.2, 8), 1, 10)),
                    }
                )
        for ci, c in enumerate(personas):
            theta = np.array(c["profile"])
            w = np.array(c["salience_weights"])
            if mode == "weighted":
                m_vec = np.array(
                    [E.match_weighted(theta, TARGETS[b], w) for b in BRANDS]
                )
            else:
                m_vec = np.array([E.match_euclid(theta, TARGETS[b]) for b in BRANDS])
            for rep in range(3):
                if mode == "null":
                    weights = rng.uniform(0.5, 1.5, len(BRANDS))
                else:
                    weights = (m_vec - m_vec.min() + 0.03) ** 2 + rng.normal(
                        0, 0.002, len(BRANDS)
                    )
                    weights = np.clip(weights, 1e-4, None)
                alloc = largest_remainder(weights)
                juster = np.round(
                    9 * (weights - weights.min()) / (np.ptp(weights) + 1e-9)
                ).astype(int)
                cur = BRANDS[(ci + rep) % len(BRANDS)]
                nxt = weights / weights.sum()
                rows.append(
                    {
                        "record_key": f"eliciting|{op_id}|{c['cohort_id']}|r{rep}",
                        "arm": "eliciting",
                        "operator": op_id,
                        "model": "m",
                        "family": "f",
                        "category": CAT,
                        "cohort_id": c["cohort_id"],
                        "replicate": rep,
                        "current_brand": cur,
                        "payload": {
                            "constant_sum": {b: int(a) for b, a in zip(BRANDS, alloc)},
                            "juster": {b: int(j) for b, j in zip(BRANDS, juster)},
                            "switching": {
                                "current_brand": cur,
                                "next_purchase": {
                                    b: float(v) for b, v in zip(BRANDS, nxt)
                                },
                            },
                        },
                    }
                )
            sc_alloc = largest_remainder(
                (m_vec - m_vec.min() + 0.03) ** 2
                if mode != "null"
                else rng.uniform(0.5, 1.5, len(BRANDS))
            )
            rows.append(
                {
                    "record_key": f"samecall|{op_id}|{c['cohort_id']}|r0",
                    "arm": "samecall",
                    "operator": op_id,
                    "model": "m",
                    "family": "f",
                    "category": CAT,
                    "cohort_id": c["cohort_id"],
                    "payload": {
                        "readings": {
                            b: list(np.clip(TARGETS[b] + rng.normal(0, 0.2, 8), 1, 10))
                            for b in BRANDS
                        },
                        "constant_sum": {b: int(a) for b, a in zip(BRANDS, sc_alloc)},
                    },
                }
            )
        with path.open("w") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")
    return str(tmp_path / "records_*.jsonl")


# ---------------------------------------------------------------------------
# Planted-positive / null / weighted controls
# ---------------------------------------------------------------------------
def test_planted_positive(tmp_path):
    g = synth_records(tmp_path, "planted")
    res = E.analyze(g, str(tmp_path / "results.json"), n_perm=300)
    assert set(res["floor_passing_operators"]) == {"OP1", "OP3"}
    cat = res["categories"][CAT]
    assert cat["pooled_tau_b"] >= 0.3
    assert cat["permutation_p_one_sided"] < 0.05
    assert cat["category_level_pass"] is True
    assert abs(cat["robustness"]["random_profile_pooled_tau"]) < 0.25
    assert res["kill_conditions"]["K1_no_link"] is False
    assert res["kill_conditions"]["K4_instrument_failure"] is False


def test_null_control(tmp_path):
    g = synth_records(tmp_path, "null")
    res = E.analyze(g, str(tmp_path / "results.json"), n_perm=300)
    cat = res["categories"][CAT]
    assert abs(cat["pooled_tau_b"]) < 0.2
    assert cat["category_level_pass"] is False
    assert res["kill_conditions"]["K1_no_link"] is True


def test_weighted_planted_delta_tau_w_positive(tmp_path):
    g = synth_records(tmp_path, "weighted")
    res = E.analyze(g, str(tmp_path / "results.json"), n_perm=300)
    cat = res["categories"][CAT]
    assert cat["delta_tau_w"] > 0
    assert cat["delta_tau_w_p_positive"] < 0.1


def test_stimulus_gate_pass_and_fail(tmp_path, capsys):
    # validation readings at the targets -> PASS
    for op_id in ["OP1"]:
        path = tmp_path / f"records_{op_id}.jsonl"
        with path.open("w") as fh:
            for b in S1["brands"]:
                for rep in range(3):
                    fh.write(
                        json.dumps(
                            {
                                "record_key": f"validate|{op_id}|{b['brand_id']}|r{rep}",
                                "arm": "validate",
                                "operator": op_id,
                                "model": "m",
                                "family": "f",
                                "brand": b["name"],
                                "brand_id": b["brand_id"],
                                "replicate": rep,
                                "payload": b["target_profile"],
                            }
                        )
                        + "\n"
                    )
    assert E.stimulus_gate(str(tmp_path / "records_*.jsonl")) is True
    # shift one pack far off -> FAIL
    with (tmp_path / "records_OP1.jsonl").open("a") as fh:
        for rep in range(20):
            fh.write(
                json.dumps(
                    {
                        "record_key": f"validate|OP1|B1|x{rep}",
                        "arm": "validate",
                        "operator": "OP1",
                        "model": "m",
                        "family": "f",
                        "brand": "x",
                        "brand_id": "B1",
                        "replicate": rep,
                        "payload": [1.0] * 8,
                    }
                )
                + "\n"
            )
    assert E.stimulus_gate(str(tmp_path / "records_*.jsonl")) is False
