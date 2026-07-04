#!/usr/bin/env python3
"""synthetic.py — seeded synthetic record generators for PRISM-M PL4 tests.

Provides the planted POSITIVE control (PL1: a scalar-equal, profile-distinct
pair that the estimator MUST flag metameric) and a general synthetic-bank
generator used by the unit tests. No API calls; fully deterministic.
"""

from __future__ import annotations

import numpy as np

SEED = 20260702
CHANNELS = ["official", "press", "experience", "social"]
OP_PAIRS = ["OP1", "OP2", "OP3", "OP4"]
DIMENSIONS = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
]


def _records_for_brand(
    brand: str,
    profile: np.ndarray,
    scalar: float,
    rank: float,
    pick: float,
    rng: np.random.Generator,
    noise: float = 0.15,
    scalar_noise: float = 0.02,
    coherence_type: str = "synthetic",
    sector: str = "b2c",
) -> list[dict]:
    rows = []
    for op in OP_PAIRS:
        for ch in CHANNELS:
            vec = np.clip(profile + rng.normal(0, noise, 8), 0, 10)
            rows.append(
                {
                    "brand": brand,
                    "coherence_type": coherence_type,
                    "sector": sector,
                    "goods_type": "experience",
                    "channel": ch,
                    "op_pair": op,
                    "readout": "dims",
                    "value": [round(float(v), 3) for v in vec],
                    "flagged_malformed": False,
                    "prompt_variant": "main",
                }
            )
            for ro, base in (("score", scalar), ("rank", rank), ("pick", pick)):
                v = float(np.clip(base + rng.normal(0, scalar_noise), 0, 1))
                if ro == "pick":
                    v = float(base)  # picks are stable in synthetic data
                rows.append(
                    {
                        "brand": brand,
                        "coherence_type": coherence_type,
                        "sector": sector,
                        "goods_type": "experience",
                        "channel": ch,
                        "op_pair": op,
                        "readout": ro,
                        "value": round(v, 4),
                        "flagged_malformed": False,
                        "prompt_variant": "main",
                    }
                )
    return rows


def planted_positive_records(seed: int = SEED) -> list[dict]:
    """The PL1 positive control: two profiles distinct on dimensions the
    scalar readout averages away (mirror-image strengths), equal scalar."""
    rng = np.random.default_rng(seed)
    prof_a = np.array([9.0, 8.5, 3.0, 8.0, 3.5, 8.0, 3.0, 9.0])
    prof_b = np.array([3.0, 3.5, 8.5, 3.0, 9.0, 3.5, 8.5, 3.0])
    rows = []
    rows += _records_for_brand("PLANT_A", prof_a, 0.7, 0.3, 1.0, rng)
    rows += _records_for_brand("PLANT_B", prof_b, 0.7, 0.3, 1.0, rng)
    return rows


def synthetic_bank_records(seed: int = SEED) -> list[dict]:
    """A 6-brand synthetic bank with known structure:
    - M1/M2: a true metamer pair (distinct profiles, equal scalar+rank)
    - D1/D2: distinct profiles AND distinct scalars (resolved, not metameric)
    - S1/S2: near-identical profiles (not resolved on the full readout)
    """
    rng = np.random.default_rng(seed)
    rows = []
    rows += _records_for_brand(
        "M1", np.array([9.0, 8.0, 3.0, 8.5, 3.0, 8.0, 3.5, 9.0]), 0.65, 0.35, 1.0, rng
    )
    rows += _records_for_brand(
        "M2", np.array([3.0, 3.5, 8.5, 3.0, 9.0, 3.0, 8.5, 3.5]), 0.65, 0.35, 1.0, rng
    )
    rows += _records_for_brand(
        "D1", np.array([9.0, 9.0, 8.5, 9.0, 8.5, 4.0, 9.0, 9.0]), 0.9, 0.1, 1.0, rng
    )
    rows += _records_for_brand(
        "D2", np.array([4.0, 3.5, 3.0, 4.0, 3.5, 8.0, 3.0, 3.0]), 0.2, 0.85, 0.0, rng
    )
    base = np.array([7.0, 6.5, 6.0, 7.0, 6.5, 6.0, 6.5, 7.0])
    rows += _records_for_brand("S1", base, 0.6, 0.4, 1.0, rng)
    rows += _records_for_brand("S2", base + 0.05, 0.6, 0.4, 1.0, rng)
    return rows
