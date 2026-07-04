#!/usr/bin/env python3
"""synthetic.py — seeded synthetic generators for PRISM-T (2026ba).

Emits records in the exact schema the PL4 estimator consumes, so unit tests
and the power analysis exercise the REAL estimator code path. All generators
are deterministic given a seed.

Model:
  reading(brand, channel, renderer-rung r, extractor e)
    = clip( profile_b + bias_{op} + rung_shift_r + eps, 0, 10 )
  bias_{op}      ~ N(0, sigma_op^2)  per operator combo, per dim (systematic)
  rung_shift_r   = r * drift on the drifting dims (cumulative across rungs)
  eps            ~ N(0, sigma_art^2) per (brand, channel, rung, op, run)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))
sys.path.insert(0, str(CODE_DIR.parents[1]))
from prism_core.prism_b import DIMENSIONS  # noqa: E402
from prism_t_lib import H3_HIGH_DRIFT  # noqa: E402

CHANNELS = ["official", "press", "experience", "social"]


def synthetic_config(n_rungs: int = 3) -> dict:
    """A pared PL1-shaped config: 4 operator pairs + ONE 3-rung ladder whose
    top rung coincides with OP1 (mirroring the real shared-top-rung design)."""
    rungs = [{"model": f"R{i}", "family": "fam-a"} for i in range(n_rungs)]
    return {
        "operator_pairs": {
            "OP1": {
                "renderer": rungs[-1],
                "extractor": {"model": "E1", "family": "fam-b"},
            },
            "OP2": {
                "renderer": {"model": "P2", "family": "fam-b"},
                "extractor": {"model": "E2", "family": "fam-a"},
            },
            "OP3": {
                "renderer": {"model": "P3", "family": "fam-c"},
                "extractor": {"model": "E3", "family": "fam-d"},
            },
            "OP4": {
                "renderer": {"model": "P4", "family": "fam-d"},
                "extractor": {"model": "E4", "family": "fam-c"},
            },
        },
        "ladders": {
            "fam-a-ladder": {
                "extractor": {"model": "E1", "family": "fam-b"},
                "rungs": rungs,
            }
        },
        "controls": {
            "negative": {
                "model": rungs[-1]["model"],
                "family": "fam-a",
                "extractor": {"model": "E1", "family": "fam-b"},
                "runs": 2,
            },
            "positive": {
                "ladder": "fam-a-ladder",
                "pair": [rungs[0]["model"], rungs[-1]["model"]],
            },
        },
    }


def _emit(
    records,
    brand,
    channel,
    renderer,
    extractor,
    dims,
    *,
    run=1,
    panel="pinned",
    epoch="VE-1",
):
    records.append(
        {
            "panel": panel,
            "epoch": epoch,
            "brand": brand,
            "channel": channel,
            "renderer": renderer,
            "renderer_family": "syn",
            "extractor": extractor,
            "extractor_family": "syn",
            "run": run,
            "dims": [float(x) for x in np.clip(dims, 0.0, 10.0)],
            "flagged": False,
            "ts": "1970-01-01T00:00:00+00:00",
        }
    )


def gen_records(
    *,
    n_brands: int = 40,
    n_rungs: int = 3,
    sigma_op: float = 0.3,
    sigma_art: float = 0.15,
    drift: float = 0.0,
    drift_dims: list[str] | None = None,
    brand_signal: float = 0.0,
    two_epochs: bool = False,
    seed: int = 1,
) -> tuple[list[dict], dict]:
    """Generate a full synthetic VE-1 record set (+ optional VE-2 live/pinned
    records carrying `brand_signal` on the live panel only).

    drift: per-dimension shift per ADJACENT rung pair on `drift_dims`
           (default: the pre-registered high-drift set).
    """
    rng = np.random.default_rng(seed)
    cfg = synthetic_config(n_rungs)
    drift_dims = H3_HIGH_DRIFT if drift_dims is None else drift_dims
    drift_mask = np.array([1.0 if d in drift_dims else 0.0 for d in DIMENSIONS])

    brands = [f"brand{i:02d}" for i in range(n_brands)]
    profiles = {b: rng.uniform(2.0, 9.0, len(DIMENSIONS)) for b in brands}

    # Systematic operator bias per (renderer, extractor) combo. Ladder rungs
    # share ONE family base bias (a null world has NO inter-rung difference;
    # `drift` is the only deterministic inter-rung shift), while the four
    # contemporaneous operator pairs get individual biases — their dispersion
    # IS the operator floor. The top rung coincides with OP1, so OP1 carries
    # the ladder's shared bias.
    ladder = cfg["ladders"]["fam-a-ladder"]
    ladder_bias = rng.normal(0.0, sigma_op, len(DIMENSIONS))
    bias = {}
    for r in ladder["rungs"]:
        bias[(r["model"], ladder["extractor"]["model"])] = ladder_bias
    for op in cfg["operator_pairs"].values():
        combo = (op["renderer"]["model"], op["extractor"]["model"])
        if combo not in bias:
            bias[combo] = rng.normal(0.0, sigma_op, len(DIMENSIONS))

    rung_ids = [r["model"] for r in ladder["rungs"]]
    top = rung_ids[-1]
    ext = ladder["extractor"]["model"]

    def rung_shift(renderer):
        # anchored at the TOP rung (the current state, shared with the
        # contemporaneous operator pairs); earlier rungs shift backward,
        # so drift never inflates the contemporaneous operator floor.
        if renderer in rung_ids:
            return (rung_ids.index(renderer) - (len(rung_ids) - 1)) * drift * drift_mask
        return np.zeros(len(DIMENSIONS))

    records: list[dict] = []
    for b in brands:
        for ch in CHANNELS:
            # contemporaneous operator pairs (floor) — top-rung epoch
            for op in cfg["operator_pairs"].values():
                rmodel, emodel = op["renderer"]["model"], op["extractor"]["model"]
                dims = (
                    profiles[b]
                    + bias[(rmodel, emodel)]
                    + rung_shift(rmodel)
                    + rng.normal(0.0, sigma_art, len(DIMENSIONS))
                )
                _emit(records, b, ch, rmodel, emodel, dims)
            # ladder rungs (top rung already emitted as OP1)
            for rid in rung_ids[:-1]:
                dims = (
                    profiles[b]
                    + bias[(rid, ext)]
                    + rung_shift(rid)
                    + rng.normal(0.0, sigma_art, len(DIMENSIONS))
                )
                _emit(records, b, ch, rid, ext, dims)
            # negative control: same version, run 2
            dims = (
                profiles[b]
                + bias[(top, ext)]
                + rung_shift(top)
                + rng.normal(0.0, sigma_art, len(DIMENSIONS))
            )
            _emit(records, b, ch, top, ext, dims, run=2)

    if two_epochs:
        # VE-2: pinned re-read (version drift only) + live re-read (version
        # drift + brand signal). Top rung vs a "next version" NR.
        nr = "NR"
        bias_nr = rng.normal(0.0, sigma_op, len(DIMENSIONS))
        signal_mask = np.ones(len(DIMENSIONS))
        for b in brands:
            for ch in CHANNELS:
                for panel, extra in (("pinned", 0.0), ("live", brand_signal)):
                    # epoch VE-1 baseline for this panel under the top rung
                    dims1 = (
                        profiles[b]
                        + bias[(top, ext)]
                        + rng.normal(0.0, sigma_art, len(DIMENSIONS))
                    )
                    _emit(records, b, ch, top, ext, dims1, panel=panel, epoch="VE-1")
                    # epoch VE-2 read under the shipped next version
                    dims2 = (
                        profiles[b]
                        + bias_nr
                        + drift * drift_mask
                        + extra * signal_mask
                        + rng.normal(0.0, sigma_art, len(DIMENSIONS))
                    )
                    _emit(records, b, ch, top, ext, dims2, panel=panel, epoch="VE-2")
        # register NR as a rung so h2 can address the top-rung pair by config
        _ = nr  # documented: h2 uses the top rung at both epochs

    return records, cfg
