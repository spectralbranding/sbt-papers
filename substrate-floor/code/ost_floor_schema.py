#!/usr/bin/env python3
"""ost_floor_schema.py — canonical derivation of the OST *coherence floor*.

The OST analogue of `floor_schema.py`. Where the Brand Spectrometer's noise floor
answers "how much apparent cohort separation is attributable to MEASUREMENT noise
(who measured / which artifacts)?", an OrgSchema reading rests not on a measurement
but on a *specification*. The analogous question is:

    how much apparent operating-misfit is attributable to the SPECIFICATION being
    incoherent or incompletely audited, rather than a real difference?

A finding drawn from a half-specified, year-over-year-unstable operating model is the
OST equivalent of a cohort gap below the noise floor — it must ABSTAIN. So an OST
"resolution" gates against a *coherence floor* with two component bands that parallel
the Spectrometer's operator/artifact bands:

  COHERENCE band  (<- the Specification Coherence Index, 2026an).  SCI in [0, 1] is the
                  year-over-year stability of the firm's specification narrative. If the
                  spec is unstable (low SCI), apparent structure read from it could be an
                  artifact of that instability. incoherence = 1 - SCI. This is the
                  OPERATOR-floor analogue: noise from the spec's own self-consistency.
  AUDIT band      (<- the six-level OrgSchema Audit, 2026ar).  Each cascade level is
                  Healthy / Partial / Failing. A finding that leans on a level that is
                  only Partial/Failing rests on an unpinned cascade. audit_gap = the mean
                  level gap (Healthy->0, Partial->.5, Failing->1). This is the
                  ARTIFACT-floor analogue: noise from incomplete coverage.
  COMBINED        = max(coherence, audit) — the conservative widest band, exactly
                  `floor_schema`'s operator (subset) artifact (subset) ... nesting. A
                  resolution cannot duck a wider band by naming a narrower one.

Why ABSTAIN rather than fabricate below the floor is not a convention but a theorem:
2026h (Specification Impossibility) proves comprehensive specification is geometrically
impossible — you specify what binds and accept that full coverage is out of reach — so a
finding the spec cannot support must be refused, not invented.

The categorical audit states (Healthy/Partial/Failing — 2026ar produces no scalar) map to
a numeric gap via the weights below. That mapping is a MODELING CHOICE owned here (like the
per-pair -> flat derivation `floor_schema` owns), documented and overridable: an artifact may
declare a numeric `completeness` in [0, 1] per level (the spec's own measured coverage) and
that wins over the categorical default — the same continuous/sharp duality SCI itself carries.

Two consumers must read the SAME coherence floor or they silently disagree:
  - `verify_ost_contract.py` (the OST live-floor honesty gate), and
  - `substrate_floor.py` (the OST endpoint's self_floor, read live from a spec-audit
    artifact via `floor_ref.spec_audit`).
So this module is the single owner; both import it. Pure + read-only: takes a parsed
spec-audit dict, does no IO and no network.
"""

from __future__ import annotations

# Schema verdicts returned by normalize_ost_floor (so neither consumer re-derives them).
SCORED = "scored"  # at least one level carries a numeric `completeness`
CATEGORICAL = "categorical"  # Healthy/Partial/Failing states only
NONE = "none"  # neither SCI nor a usable audit — no floor at all

_PLACES = 4

# The six OrgSchema Audit levels (2026ar), in cascade order. Canonical keys an artifact's
# `orgschema_audit` block may use (any subset; absent levels are simply not scored).
AUDIT_LEVELS = (
    "level_0_experience_contracts",
    "level_1_signal_requirements",
    "level_2_process_contracts",
    "level_3_procedures",
    "level_4_input_specifications",
    "level_5_sourcing_requirements",
)

# Categorical state -> level gap (the modeling choice this module owns). Healthy pins the
# level (no gap); Failing leaves it entirely unpinned (full gap); Partial is the midpoint.
STATE_GAP = {"healthy": 0.0, "partial": 0.5, "failing": 1.0}


def _is_number(x: object) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _round(x: float | None) -> float | None:
    return round(x, _PLACES) if x is not None else None


def _sci_value(audit: dict) -> tuple[float | None, float | None]:
    """(mean SCI, worst-case SCI) in [0, 1] from the artifact's SCI block.

    Accepts a bare number, or a block ``{value, ci_95_lower?, worst_case?}``. The worst-case
    SCI (the lower CI bound or an explicit worst_case) drives the coherence band's worst case —
    the most pessimistic incoherence the spec admits."""
    sci = audit.get("specification_coherence_index")
    if sci is None:
        sci = audit.get("sci")
    if _is_number(sci):
        v = float(sci)  # type: ignore[arg-type]
        return v, v
    if isinstance(sci, dict):
        val = sci.get("value")
        if not _is_number(val):
            return None, None
        mean = float(val)  # type: ignore[arg-type]
        worst = sci.get("worst_case")
        if not _is_number(worst):
            worst = sci.get("ci_95_lower")
        worst_v = float(worst) if _is_number(worst) else mean  # type: ignore[arg-type]
        return mean, min(worst_v, mean)
    return None, None


def _level_gaps(audit_block: dict) -> tuple[list[float], str]:
    """(per-level gaps in [0,1], schema). A level may be a categorical state string, or a
    block ``{state?, completeness?}`` where a numeric ``completeness`` in [0,1] overrides the
    categorical default (gap = 1 - completeness)."""
    gaps: list[float] = []
    scored = False
    for level in AUDIT_LEVELS:
        entry = audit_block.get(level)
        if entry is None:
            continue
        comp = entry.get("completeness") if isinstance(entry, dict) else None
        if _is_number(comp):
            scored = True
            gaps.append(max(0.0, min(1.0, 1.0 - float(comp))))  # type: ignore[arg-type]
            continue
        state = entry.get("state") if isinstance(entry, dict) else entry
        if isinstance(state, str) and state.lower() in STATE_GAP:
            gaps.append(STATE_GAP[state.lower()])
    return gaps, (SCORED if scored else CATEGORICAL)


def normalize_ost_floor(audit: dict) -> tuple[str, dict]:
    """Return ``(schema, floor)``.

    ``schema`` is ``SCORED`` / ``CATEGORICAL`` / ``NONE``. ``floor`` maps the band names to
    values (``None`` when a band is absent):

        coherence_floor_mean, coherence_worst_case_max,
        audit_floor_mean, audit_worst_case_max,
        combined_floor, combined_worst_case_max, has_audit

    coherence = 1 - SCI (mean) / 1 - worst-SCI (worst case); audit = mean / max level gap;
    combined = max over the MEASURED bands (a null band is not measured and never binds — the
    same honesty `floor_schema` keeps for an operator-only floor)."""
    audit = audit or {}

    sci_mean, sci_worst = _sci_value(audit)
    coh_mean = _round(1.0 - sci_mean) if sci_mean is not None else None
    coh_worst = _round(1.0 - sci_worst) if sci_worst is not None else None

    audit_block = audit.get("orgschema_audit") or {}
    gaps, audit_schema = (
        _level_gaps(audit_block) if isinstance(audit_block, dict) else ([], CATEGORICAL)
    )
    has_audit = bool(gaps)
    audit_mean = _round(sum(gaps) / len(gaps)) if gaps else None
    audit_worst = _round(max(gaps)) if gaps else None

    if coh_mean is None and not has_audit:
        return NONE, {"has_audit": False}

    means = [v for v in (coh_mean, audit_mean) if v is not None]
    worsts = [v for v in (coh_worst, audit_worst) if v is not None]
    schema = SCORED if audit_schema == SCORED else CATEGORICAL
    return schema, {
        "coherence_floor_mean": coh_mean,
        "coherence_worst_case_max": coh_worst,
        "audit_floor_mean": audit_mean,
        "audit_worst_case_max": audit_worst,
        "combined_floor": max(means) if means else None,
        "combined_worst_case_max": max(worsts) if worsts else None,
        "has_audit": has_audit,
    }
