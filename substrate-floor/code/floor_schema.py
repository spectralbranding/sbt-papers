#!/usr/bin/env python3
"""floor_schema.py — canonical normalization of the corpus's TWO atlas floor schemas.

The corpus stores an instrument's noise floor two ways:

  FLAT      (CPG/PL atlases — pepsi_vs_olipop, olipop_vs_poppi, pl_pilot_2627):
            ``variance.noise_floor.{operator_floor_mean, artifact_floor_mean,
            combined_floor, *_worst_case_max, substrate_*}``.
  PER-PAIR  (Ferrari — ferrari_luce_fresh_2606): no flat block; the floor lives as
            ``variance.{operator,artifact}_sensitivity.<cohort>.max_alt_distance``.

Two consumers must read the SAME floor or they silently disagree:

  - ``run_case_instrument.py`` (producer-side readiness — is the floor present and
    readable before the contract gates against it?), and
  - ``verify_contract.py`` (the live-floor honesty gate itself).

If the bridge normalized the per-pair schema one way and the gate another, the bridge
would report CONTRACT-READY against one number while the gate gated against a different
one — exactly the kind of drift the bundle gates exist to forbid. So this module is the
**single owner** of the per-pair -> flat derivation; both import it.

Derivation (per-pair -> flat), over the cohort sensitivity blocks:

    operator_floor_mean      = mean over cohorts of operator max_alt_distance
    operator_worst_case_max  = max  over cohorts of operator max_alt_distance
    artifact_*               = the same over artifact_sensitivity
    combined_floor (mean)    = max(operator_floor_mean, artifact_floor_mean)
    combined_worst_case_max  = max(operator_worst_case_max, artifact_worst_case_max)

This is the conservative single-floor reduction of the per-pair data: ``combined`` takes
the widest band so a resolution cannot duck a wider floor (the operator ⊆ artifact ⊆
substrate nesting of VERIFY_CONTRACT.md C2). The per-pair atlas ALSO carries a finer,
pair-specific floor (``per_pair_signal_to_noise[].noise_floor`` = max of the two endpoint
cohorts' ``max_alt_distance``); gating at that granularity is a documented future
enhancement — the flat reduction here is what both tools agree on today.

Pure + read-only: takes a parsed ``variance`` dict, does no IO and no network.
"""

from __future__ import annotations

# Schema verdicts returned by normalize_floor (so neither consumer re-derives them).
FLAT = "flat"  # a flat variance.noise_floor block the gate reads directly
PER_PAIR = "per_pair"  # per-cohort sensitivity; normalized here to a flat floor
NONE = "none"  # neither — matrix-only / no floor data at all

_PLACES = 4  # atlas distances are reported to 4 decimals


def _is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _cohort_maxes(sens: dict) -> list[float]:
    """The per-cohort ``max_alt_distance`` values out of a *_sensitivity block."""
    if not isinstance(sens, dict):
        return []
    return [
        float(c["max_alt_distance"])
        for c in sens.values()
        if isinstance(c, dict) and _is_number(c.get("max_alt_distance"))
    ]


def _mean(xs: list[float]):
    return round(sum(xs) / len(xs), _PLACES) if xs else None


def _max(xs: list[float]):
    return round(max(xs), _PLACES) if xs else None


def normalize_floor(variance: dict) -> tuple[str, dict]:
    """Return ``(schema, floor)``.

    ``schema`` is one of ``FLAT`` / ``PER_PAIR`` / ``NONE``. ``floor`` maps the normalized
    flat band names to values (``None`` when a band is absent) plus ``has_matrix``:

        operator_floor_mean, operator_worst_case_max,
        artifact_floor_mean, artifact_worst_case_max,
        substrate_floor_mean, substrate_worst_case_max,
        combined_floor, combined_worst_case_max, has_matrix
    """
    var = variance or {}
    nf = var.get("noise_floor") or {}
    has_matrix = bool(var.get("pairwise_distance_matrix"))

    # FLAT schema — read the bands the atlas already states.
    if isinstance(nf, dict) and (
        "combined_floor" in nf
        or "operator_floor_mean" in nf
        or "artifact_floor_mean" in nf
    ):
        op = nf.get("operator_floor_mean")
        art = nf.get("artifact_floor_mean")
        sub = nf.get("substrate_floor_mean")
        combined = nf.get("combined_floor")
        if combined is None:
            present = [v for v in (op, art, sub) if v is not None]
            combined = max(present) if present else None
        wc = [
            v
            for v in (
                nf.get("operator_worst_case_max"),
                nf.get("artifact_worst_case_max"),
                nf.get("substrate_worst_case_max"),
            )
            if v is not None
        ]
        return FLAT, {
            "operator_floor_mean": op,
            "operator_worst_case_max": nf.get("operator_worst_case_max"),
            "artifact_floor_mean": art,
            "artifact_worst_case_max": nf.get("artifact_worst_case_max"),
            "substrate_floor_mean": sub,
            "substrate_worst_case_max": nf.get("substrate_worst_case_max"),
            "combined_floor": combined,
            "combined_worst_case_max": max(wc) if wc else None,
            "has_matrix": has_matrix,
        }

    # PER-PAIR schema (Ferrari) — derive the flat bands from the sensitivity blocks.
    op_maxes = _cohort_maxes(var.get("operator_sensitivity") or {})
    art_maxes = _cohort_maxes(var.get("artifact_sensitivity") or {})
    if op_maxes or art_maxes:
        op_mean, art_mean = _mean(op_maxes), _mean(art_maxes)
        op_wc, art_wc = _max(op_maxes), _max(art_maxes)
        means = [v for v in (op_mean, art_mean) if v is not None]
        wcs = [v for v in (op_wc, art_wc) if v is not None]
        return PER_PAIR, {
            "operator_floor_mean": op_mean,
            "operator_worst_case_max": op_wc,
            "artifact_floor_mean": art_mean,
            "artifact_worst_case_max": art_wc,
            "substrate_floor_mean": None,
            "substrate_worst_case_max": None,
            "combined_floor": max(means) if means else None,
            "combined_worst_case_max": max(wcs) if wcs else None,
            "has_matrix": has_matrix,
        }

    return NONE, {"has_matrix": has_matrix}
