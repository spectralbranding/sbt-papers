#!/usr/bin/env python3
"""Verify-OST-contract gate: an OrgSchema rendering's resolutions vs the LIVE coherence floor.

The OST analogue of `verify_contract.py`. The Brand Spectrometer gate rechecks a rendering's
asserted cohort-difference magnitudes against the instrument's LIVE *noise* floor (operator /
artifact dispersion read out of the pinned atlas). This gate rechecks an OrgSchema rendering's
asserted operating-misfit magnitudes against the LIVE *coherence* floor read out of a pinned
spec-audit artifact (the Specification Coherence Index, 2026an, + the six-level OrgSchema Audit,
2026ar) via `ost_floor_schema` — the single owner of the coherence-floor derivation, shared with
`substrate_floor.py` so the OST endpoint's self_floor and this gate cannot disagree.

The honesty invariant is the same shape, lifted from measurement noise to specification noise:
a finding the specification is too incoherent / under-audited to support must ABSTAIN, not be
asserted. That refusal is a theorem, not a convention — 2026h (Specification Impossibility)
proves comprehensive specification is geometrically impossible.

Contract: [internal path removed] A `verdicts[].resolution` block declares,
per claimed distinction, a misfit magnitude in [0,1] + which spec-audit / band it rests on
(+ optionally the floor value it was rendered against). The checks:

    C1 FLOOR RESOLVES   the pinned spec-audit yields a coherence floor; the named band resolves
    C2 WIDEST BINDS     the binding floor is the widest band present (advisory if narrower named)
    C3 MAGNITUDE RANGE  the misfit magnitude is a normalized [0,1] verdict (OST has no distance
                        matrix — its instrument output is a specification, not a vector — so the
                        magnitude is operator-declared, not traced to an atlas)
    C4 RESOLVE>=FLOOR   a `resolved` verdict's magnitude clears the binding coherence floor
                        (else abstain — the spec cannot support the finding)
    C5 CURRENCY         floor_at_render still matches the live floor (else STALE -> re-render)
    C0 (--strict)       every `resolved` verdict carries a checkable resolution block

ERROR and STALE fail the gate (nonzero exit). Read-only; no network, no substrate writes.

    uv run --with pyyaml python code/verify_ost_contract.py CASE.yaml [CASE2.yaml ...]
    uv run --with pyyaml python code/verify_ost_contract.py --all --strict
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import ost_floor_schema

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit(
        "PyYAML required: uv run --with pyyaml python code/verify_ost_contract.py ..."
    )

REPO = Path(__file__).resolve().parents[2]
CASES_DIR = REPO / "research" / "consult" / "cases" / "ost_contract"

KIND_ENUM = {"experiential_misfit", "tier_transfer", "coherence"}
METRIC_ENUM = {"misfit_distance", "normalized_gap"}
BAND_ENUM = {"coherence", "audit", "combined"}
BASIS_ENUM = {"mean", "worst_case"}
DEFAULT_TOL = 1e-4

# Finding severities. ERROR + STALE fail the gate; WARN/OK do not.
ERROR, STALE, WARN, OK = "ERROR", "STALE", "WARN", "OK"
FAILING = {ERROR, STALE}

_BAND_KEY = {
    ("coherence", "mean"): "coherence_floor_mean",
    ("coherence", "worst_case"): "coherence_worst_case_max",
    ("audit", "mean"): "audit_floor_mean",
    ("audit", "worst_case"): "audit_worst_case_max",
    ("combined", "mean"): "combined_floor",
    ("combined", "worst_case"): "combined_worst_case_max",
}


class Finding:
    __slots__ = ("level", "msg")

    def __init__(self, level: str, msg: str):
        self.level = level
        self.msg = msg


# ----------------------------------------------------------------------------- audit/floor IO


def _audit_path(p: str, default_audit: Path | None) -> Path | None:
    if not p and default_audit:
        return default_audit
    if not p:
        return None
    path = Path(p)
    return path if path.is_absolute() else (REPO / path)


def load_floors(audit_file: Path) -> tuple[dict, str]:
    """Return (floor_bands, error). floor_bands maps (band, basis) -> value, read LIVE through
    `ost_floor_schema.normalize_ost_floor` (the single owner of the coherence-floor derivation,
    shared with substrate_floor.py so the gate and the endpoint self_floor cannot disagree).
    """
    try:
        data = yaml.safe_load(audit_file.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as e:
        return {}, f"spec-audit unreadable: {e}"
    schema, floor = ost_floor_schema.normalize_ost_floor(
        data if isinstance(data, dict) else {}
    )
    if schema == ost_floor_schema.NONE:
        return {}, (
            "spec-audit exposes no coherence floor: neither a specification_coherence_index "
            "nor a usable orgschema_audit block"
        )
    bands: dict = {}
    for (band, basis), key in _BAND_KEY.items():
        val = floor.get(key)
        if val is not None:
            bands[(band, basis)] = float(val)
    bands["_schema"] = schema
    return bands, ""


# ----------------------------------------------------------------------------- the checks


def check_resolution(
    res: dict, verdict: str, default_audit: Path | None, tol: float
) -> list[Finding]:
    f: list[Finding] = []

    kind = res.get("kind")
    metric = res.get("metric")
    mag = res.get("magnitude")
    if kind not in KIND_ENUM:
        f.append(Finding(ERROR, f"resolution.kind '{kind}' not in {sorted(KIND_ENUM)}"))
    if metric not in METRIC_ENUM:
        f.append(
            Finding(ERROR, f"resolution.metric '{metric}' not in {sorted(METRIC_ENUM)}")
        )
    if not isinstance(mag, (int, float)) or isinstance(mag, bool) or mag < 0:
        f.append(Finding(ERROR, "resolution.magnitude must be a number >= 0"))
        return f  # nothing downstream is checkable without a magnitude

    fref = res.get("floor_ref") or {}
    band = fref.get("band")
    basis = fref.get("basis", "mean")
    if band not in BAND_ENUM:
        f.append(Finding(ERROR, f"floor_ref.band '{band}' not in {sorted(BAND_ENUM)}"))
    if basis not in BASIS_ENUM:
        f.append(
            Finding(ERROR, f"floor_ref.basis '{basis}' not in {sorted(BASIS_ENUM)}")
        )

    # C3 — MAGNITUDE RANGE (OST has no distance matrix: a spec is not a vector, so the
    # magnitude is an operator-declared normalized verdict, not traced to an instrument matrix)
    if mag > 1.0 + tol:
        f.append(
            Finding(
                ERROR,
                f"misfit magnitude {mag:.4f} outside the normalized [0,1] verdict axis "
                "(OST resolutions live on a normalized misfit axis, not a raw distance)",
            )
        )

    # C1 — FLOOR RESOLVES (instrument-owned: the spec-audit's coherence floor)
    audit_file = _audit_path(fref.get("spec_audit", ""), default_audit)
    if audit_file is None:
        f.append(
            Finding(ERROR, "floor_ref.spec_audit missing and no --floors default given")
        )
        return f
    if not audit_file.exists():
        f.append(
            Finding(
                ERROR,
                f"floor_ref.spec_audit not found: {audit_file} (live coherence floor cannot "
                "be read — provide a reachable spec-audit or --floors)",
            )
        )
        return f
    bands, err = load_floors(audit_file)
    if err:
        f.append(Finding(ERROR, f"{err} ({audit_file})"))
        return f
    if band not in BAND_ENUM or basis not in BASIS_ENUM:
        return f  # already errored on the enums; cannot bind a floor
    if (band, basis) not in bands:
        f.append(
            Finding(
                ERROR,
                f"spec-audit exposes no '{band}' floor at basis '{basis}' "
                f"(have: {sorted(b for b in bands if isinstance(b, tuple))})",
            )
        )
        return f
    named_floor = bands[(band, basis)]

    # C2 — WIDEST FLOOR BINDS (cannot duck a wider band by naming a narrower one)
    same_basis = {
        k[0]: v for k, v in bands.items() if isinstance(k, tuple) and k[1] == basis
    }
    # `combined` is by construction the max(coherence, audit); break value ties toward it so the
    # canonical widest band is named (not an equal component band).
    widest_band = max(same_basis, key=lambda b: (same_basis[b], b == "combined"))
    binding_floor = same_basis[widest_band]
    if binding_floor > named_floor + tol:
        f.append(
            Finding(
                WARN,
                f"claims the '{band}' floor ({named_floor:.4f}) but the '{widest_band}' "
                f"floor ({binding_floor:.4f}) is wider — bound to the wider floor",
            )
        )

    # C4 — RESOLVE ONLY ABOVE THE FLOOR (the core honesty invariant)
    clears = mag >= binding_floor - tol
    if verdict == "resolved":
        if not clears:
            f.append(
                Finding(
                    ERROR,
                    f"RESOLVED below the live coherence floor: magnitude {mag:.4f} < "
                    f"{widest_band} floor {binding_floor:.4f} — the specification is too "
                    "incoherent / under-audited to support this finding; must abstain",
                )
            )
    elif verdict == "abstained":
        if clears:
            f.append(
                Finding(
                    WARN,
                    f"abstained though magnitude {mag:.4f} >= {widest_band} floor "
                    f"{binding_floor:.4f} — conservative under-claim (could resolve)",
                )
            )

    # C5 — CURRENCY / RE-RENDER (the render->verify->re-render trigger)
    far = res.get("floor_at_render")
    if isinstance(far, (int, float)) and not isinstance(far, bool):
        if abs(float(far) - binding_floor) > tol:
            f.append(
                Finding(
                    STALE,
                    f"coherence floor moved since render: floor_at_render {float(far):.4f} != "
                    f"live {widest_band} floor {binding_floor:.4f} — RE-RENDER due",
                )
            )

    if not any(x.level in FAILING for x in f):
        verdict_word = "clears" if verdict == "resolved" else "below"
        f.append(
            Finding(
                OK,
                f"{verdict}: magnitude {mag:.4f} {verdict_word} the live "
                f"{widest_band} coherence floor {binding_floor:.4f}",
            )
        )
    return f


def check_case(
    path: Path, strict: bool, default_audit: Path | None, tol: float
) -> bool:
    try:
        case = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as e:
        print(f"\n=== {path.name} ===\n  [ERROR] unreadable: {e}", file=sys.stderr)
        return False

    verdicts = case.get("verdicts") or []
    print(f"\n=== {path.name} ===")
    n_checked = 0
    failed = False
    found_any = False

    for v in verdicts:
        qid = v.get("question", "?")
        verdict = v.get("verdict")
        res = v.get("resolution")
        if not res:
            # C0 — resolved verdicts must be checkable under --strict
            if verdict == "resolved":
                lvl = ERROR if strict else WARN
                failed = failed or (lvl in FAILING)
                print(
                    f"  [{lvl}] {qid}: resolved verdict has no resolution block "
                    f"— {'unverifiable (--strict)' if strict else 'not machine-verifiable'}"
                )
            continue
        found_any = True
        n_checked += 1
        findings = check_resolution(res, verdict, default_audit, tol)
        for fnd in findings:
            print(f"  [{fnd.level}] {qid}: {fnd.msg}")
            if fnd.level in FAILING:
                failed = True

    if not found_any:
        print("  (no resolution blocks — use verify_case.py for the structural check)")
    verdict_line = "DRIFT (coherence-floor violation / stale)" if failed else "PASS"
    print(f"  -> {verdict_line}  [{n_checked} resolution(s) checked]")
    return not failed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "cases", nargs="*", default=[], help="OST contract case YAML path(s)"
    )
    g.add_argument(
        "--all", action="store_true", help=f"check every *.yaml in {CASES_DIR}"
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="every resolved verdict must carry a resolution block (C0)",
    )
    ap.add_argument(
        "--floors",
        help="default spec-audit path for resolutions lacking floor_ref.spec_audit",
    )
    ap.add_argument("--tol", type=float, default=DEFAULT_TOL, help="numeric tolerance")
    args = ap.parse_args()

    if args.all:
        paths = sorted(CASES_DIR.glob("*.yaml"))
    else:
        paths = [Path(p) for p in args.cases]
    if not paths:
        sys.exit("no case files to check")

    default_audit = _audit_path(args.floors, None) if args.floors else None
    if args.floors and (default_audit is None or not default_audit.exists()):
        sys.exit(f"--floors spec-audit not found: {args.floors}")

    results = {
        p.name: check_case(p, args.strict, default_audit, args.tol) for p in paths
    }
    n_fail = sum(1 for ok in results.values() if not ok)
    print(f"\n{'=' * 56}")
    print(f"{len(results) - n_fail}/{len(results)} case(s) honest; {n_fail} with drift")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
