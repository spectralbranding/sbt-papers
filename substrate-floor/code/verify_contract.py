#!/usr/bin/env python3
"""Verify-contract gate: a rendering's asserted resolutions vs the LIVE noise floors.

This is the LIVE-FLOOR half of the Consult-Flow honesty check (open problem #4 / handoff
item #4). Its structural sibling `verify_case.py` (#20) checks a case's *shape*; this one
reads the instrument's own floors out of the pinned atlas *now* and rechecks every
asserted `resolution`. It is the consulting analogue of `verify_paper_bundle.py`: a paper
must not drift from its spine/ontology/citations; a rendering must not drift from its floors.

Contract + invariants: [internal path removed] A `verdicts[].resolution` block
declares, per claimed distinction, a magnitude + which atlas/floor it rests on (+ optionally
the floor value it was rendered against). The checks:

    C1 FLOOR RESOLVES   the pinned atlas exposes variance.noise_floor; the band resolves
    C2 WIDEST BINDS     the binding floor is the widest band present (advisory if narrower named)
    C3 MAGNITUDE TRACES cohort_pair magnitude matches the atlas pairwise_distance_matrix
    C4 RESOLVE>=FLOOR   a `resolved` verdict's magnitude clears the binding floor (else abstain)
    C5 CURRENCY         floor_at_render still matches the live floor (else STALE -> re-render)
    C0 (--strict)       every `resolved` verdict carries a checkable resolution block

ERROR and STALE fail the gate (nonzero exit). Read-only; no network, no substrate writes.

    uv run --with pyyaml python code/verify_contract.py CASE.yaml [CASE2.yaml ...]
    uv run --with pyyaml python code/verify_contract.py --all --strict
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import floor_schema

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit(
        "PyYAML required: uv run --with pyyaml python code/verify_contract.py ..."
    )

REPO = Path(__file__).resolve().parents[2]
CASES_DIR = REPO / "research" / "consult" / "cases"

KIND_ENUM = {"cohort_pair", "dimension", "cross_brand"}
METRIC_ENUM = {"cosine_distance", "sn_ratio"}
BAND_ENUM = {"operator", "artifact", "combined", "substrate"}
BASIS_ENUM = {"mean", "worst_case"}
DEFAULT_TOL = 1e-4  # atlas distances are reported to 4 decimals

# Finding severities. ERROR + STALE fail the gate; WARN/OK do not.
ERROR, STALE, WARN, OK = "ERROR", "STALE", "WARN", "OK"
FAILING = {ERROR, STALE}


class Finding:
    __slots__ = ("level", "msg")

    def __init__(self, level: str, msg: str):
        self.level = level
        self.msg = msg


# ----------------------------------------------------------------------------- atlas/floor IO


def _atlas_path(p: str, default_atlas: Path | None) -> Path | None:
    if not p and default_atlas:
        return default_atlas
    if not p:
        return None
    path = Path(p)
    return path if path.is_absolute() else (REPO / path)


def load_floors(atlas: Path) -> tuple[dict, str]:
    """Return (floor_bands, error). floor_bands maps (band, basis) -> value, plus the
    pairwise_distance_matrix under key '_matrix'.

    Reads the LIVE floor across BOTH corpus atlas schemas — the FLAT
    `variance.noise_floor` block (CPG/PL atlases) and Ferrari's PER-PAIR
    `variance.{operator,artifact}_sensitivity` — via `floor_schema.normalize_floor`, the
    single owner of the per-pair -> flat derivation (shared with run_case_instrument.py so
    the readiness check and this gate cannot disagree on the floor)."""
    try:
        data = yaml.safe_load(atlas.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as e:
        return {}, f"atlas unreadable: {e}"
    var = (data or {}).get("variance") or {}
    schema, floor = floor_schema.normalize_floor(var)
    if schema == floor_schema.NONE:
        return {}, (
            "atlas exposes no floor: neither a flat variance.noise_floor block nor a "
            "per-pair variance.{operator,artifact}_sensitivity block"
        )
    bands: dict = {}
    for band, basis, key in (
        ("operator", "mean", "operator_floor_mean"),
        ("artifact", "mean", "artifact_floor_mean"),
        ("substrate", "mean", "substrate_floor_mean"),
        ("operator", "worst_case", "operator_worst_case_max"),
        ("artifact", "worst_case", "artifact_worst_case_max"),
        ("substrate", "worst_case", "substrate_worst_case_max"),
    ):
        val = floor.get(key)
        if val is not None:
            bands[(band, basis)] = float(val)
    # combined = the widest band at each basis (use the normalized value; else derive).
    if floor.get("combined_floor") is not None:
        bands[("combined", "mean")] = float(floor["combined_floor"])
    else:
        means = [v for (b, basis), v in bands.items() if basis == "mean"]
        if means:
            bands[("combined", "mean")] = max(means)
    wc = [v for (b, basis), v in bands.items() if basis == "worst_case"]
    if wc:
        bands[("combined", "worst_case")] = max(wc)
    bands["_matrix"] = var.get("pairwise_distance_matrix") or {}
    return bands, ""


def matrix_distance(matrix: dict, a: str, b: str) -> float | None:
    row = matrix.get(a)
    if isinstance(row, dict) and b in row:
        return float(row[b])
    row = matrix.get(b)
    if isinstance(row, dict) and a in row:
        return float(row[a])
    return None


# ----------------------------------------------------------------------------- the checks


def check_resolution(
    res: dict, verdict: str, default_atlas: Path | None, tol: float
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

    # C1 — FLOOR RESOLVES (substrate/instrument-owned)
    atlas = _atlas_path(fref.get("atlas", ""), default_atlas)
    if atlas is None:
        f.append(
            Finding(ERROR, "floor_ref.atlas missing and no --floors default given")
        )
        return f
    if not atlas.exists():
        f.append(
            Finding(
                ERROR,
                f"floor_ref.atlas not found: {atlas} (live floor cannot be read "
                "— provide a reachable atlas or --floors)",
            )
        )
        return f
    bands, err = load_floors(atlas)
    if err:
        f.append(Finding(ERROR, f"{err} ({atlas})"))
        return f
    if band not in BAND_ENUM or basis not in BASIS_ENUM:
        return f  # already errored on the enums; can't bind a floor
    if (band, basis) not in bands:
        f.append(
            Finding(
                ERROR,
                f"atlas exposes no '{band}' floor at basis '{basis}' "
                f"(have: {sorted(b for b in bands if b != '_matrix')})",
            )
        )
        return f
    named_floor = bands[(band, basis)]

    # C2 — WIDEST FLOOR BINDS (cannot duck a wider band by naming a narrower one)
    same_basis = {
        k[0]: v for k, v in bands.items() if isinstance(k, tuple) and k[1] == basis
    }
    widest_band = max(same_basis, key=lambda b: same_basis[b])
    binding_floor = same_basis[widest_band]
    if binding_floor > named_floor + tol:
        f.append(
            Finding(
                WARN,
                f"claims the '{band}' floor ({named_floor:.4f}) but the '{widest_band}' "
                f"floor ({binding_floor:.4f}) is wider — bound to the wider floor",
            )
        )

    # C3 — MAGNITUDE TRACES TO THE INSTRUMENT (cohort_pair only; needs the matrix)
    if kind == "cohort_pair" and metric == "cosine_distance":
        pair = res.get("pair") or []
        if not (isinstance(pair, list) and len(pair) == 2):
            f.append(Finding(ERROR, "kind=cohort_pair needs pair: [cohortA, cohortB]"))
        else:
            d = matrix_distance(bands["_matrix"], pair[0], pair[1])
            if d is None:
                f.append(
                    Finding(
                        WARN,
                        f"pair {pair} not in the atlas pairwise_distance_matrix "
                        "— magnitude could not be corroborated against the instrument",
                    )
                )
            elif abs(d - mag) > tol:
                f.append(
                    Finding(
                        ERROR,
                        f"declared magnitude {mag:.4f} != live atlas distance {d:.4f} "
                        f"for pair {pair} (resolution does not trace to the instrument)",
                    )
                )

    # C4 — RESOLVE ONLY ABOVE THE FLOOR (the core honesty invariant)
    clears = mag >= binding_floor - tol
    if verdict == "resolved":
        if not clears:
            f.append(
                Finding(
                    ERROR,
                    f"RESOLVED below the live floor: magnitude {mag:.4f} < "
                    f"{widest_band} floor {binding_floor:.4f} — must abstain "
                    "('cannot resolve'), not assert a finding",
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
                    f"floor moved since render: floor_at_render {float(far):.4f} != "
                    f"live {widest_band} floor {binding_floor:.4f} — RE-RENDER due",
                )
            )

    if not any(x.level in FAILING for x in f):
        verdict_word = "clears" if verdict == "resolved" else "below"
        f.append(
            Finding(
                OK,
                f"{verdict}: magnitude {mag:.4f} {verdict_word} the live "
                f"{widest_band} floor {binding_floor:.4f}",
            )
        )
    return f


def check_case(
    path: Path, strict: bool, default_atlas: Path | None, tol: float
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
        findings = check_resolution(res, verdict, default_atlas, tol)
        for fnd in findings:
            print(f"  [{fnd.level}] {qid}: {fnd.msg}")
            if fnd.level in FAILING:
                failed = True

    if not found_any:
        print("  (no resolution blocks — use verify_case.py for the structural check)")
    verdict_line = "DRIFT (floor violation / stale)" if failed else "PASS"
    print(f"  -> {verdict_line}  [{n_checked} resolution(s) checked]")
    return not failed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("cases", nargs="*", default=[], help="case YAML path(s)")
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
        help="default atlas path for resolutions lacking floor_ref.atlas",
    )
    ap.add_argument("--tol", type=float, default=DEFAULT_TOL, help="numeric tolerance")
    args = ap.parse_args()

    if args.all:
        paths = sorted(CASES_DIR.glob("*.yaml"))
    else:
        paths = [Path(p) for p in args.cases]
    if not paths:
        sys.exit("no case files to check")

    default_atlas = _atlas_path(args.floors, None) if args.floors else None
    if args.floors and (default_atlas is None or not default_atlas.exists()):
        sys.exit(f"--floors atlas not found: {args.floors}")

    results = {
        p.name: check_case(p, args.strict, default_atlas, args.tol) for p in paths
    }
    n_fail = sum(1 for ok in results.values() if not ok)
    print(f"\n{'=' * 56}")
    print(f"{len(results) - n_fail}/{len(results)} case(s) honest; {n_fail} with drift")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
