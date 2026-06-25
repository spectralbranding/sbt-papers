#!/usr/bin/env python3
"""The substrate floor — calibration-conflict reconciliation across substrates (#9).

When a client's agent composes more than one substrate (lens) on the SAME decision, "whose
floor wins?" is the wrong question — it smuggles authority back in. This tool implements the
honest mechanism from the theory memo (`SUBSTRATE_CONSULTING_THEORY_2026-06-23.md` §4a/4b):
the **substrate floor** — the metameric-psychometrics move lifted one level up. Inside one
instrument the Spectrometer computes an *operator floor* (dispersion across operator pairs)
and abstains below it; across instruments the integrator computes a *substrate floor*
(dispersion across substrates) and treats cross-substrate **agreement as triangulation** and
**disagreement as the floor itself**.

The four moves (§4a):
  0. ALIGN before you adjudicate. Two substrates may not mean the same thing by the same term;
     apparent conflict is often a vocabulary mismatch (false conflict) and apparent agreement a
     shared word with divergent meaning (false agreement). A verdict's SSSOM alignment predicate
     to the shared claim C is either DECLARED, or — when the verdict names its `align_term` —
     COMPUTED from the live terms graph by `align_terms` (#9a, the run-time counterpart of
     `negotiate_modules.py`; unlinked anchor terms -> `unaligned`, the strongest risk). A
     non-`exactMatch` predicate is surfaced as a false-(dis)agreement RISK, never silently
     trusted — and a computed one cannot be wished away by an optimistic hand-declaration. A
     computed `unaligned` among the resolvers DOWNGRADES corroborated -> contested (move 2): you
     cannot corroborate across concepts the graph does not map to each other.
  1. CLASSIFY: coverage gap (a substrate is silent — a union, not a conflict) vs floor/answer
     disagreement among the resolvers.
  2. RECONCILE to a typed verdict, not a single answer — the lattice:
       corroborated          — >=2 resolve, agree within their floors, consensus clears the
                               effective floor  -> cross-substrate replication (highest confidence)
       contested             — >=2 resolve, disagree BEYOND their floors -> characterize why;
                               human judgment required by construction
       substrate-conditional — exactly 1 resolves (the rest abstain) -> holds only under that
                               apparatus; report the condition
       jointly-unresolved    — all abstain, OR resolvers agree but on a consensus below the
                               effective floor (agreement on noise) -> honestly unknown
  3. The RECURSION — floors NEST: operator (subset) artifact (subset) substrate. A finding
     survives only if its signal clears the OUTERMOST floor in play:
       effective_floor = max(substrate_dispersion, each endpoint's own combined floor)
     Agreement across substrates does not rescue a finding if each substrate is individually
     noisy; cross-substrate disagreement is the operator floor of the market.

What the substrate floor computes (§4b), on the aligned claim's VERDICT (not the raw output —
substrates have incommensurable output spaces): each covering substrate emits, for C, a triple
`{resolve(value, self_floor) | abstain}` on a common normalized axis. The substrate dispersion
is the max pairwise distance over the resolvers (the operator-floor move, lifted); the
categorical layer is the entropy of the {resolve, abstain} distribution. Audit-failing
substrates (those that cannot self-certify, §1) are EXCLUDED, never averaged in.

A self_floor is each endpoint's own combined (operator+artifact) nested floor — declared, or
read LIVE from a real atlas via `floor_schema` (the same single owner `verify_contract` uses,
so an endpoint's floor cannot drift). Read-only on the filesystem; consumes a reconciliation
case (a fictional worked example today, the cross-substrate analogue of a contract case).

    uv run --with pyyaml python code/substrate_floor.py --all
    uv run --with pyyaml python code/substrate_floor.py CASE.yaml [CASE2 ...]
"""

from __future__ import annotations

import argparse
import math
import sqlite3
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit(
        "PyYAML required: uv run --with pyyaml python code/substrate_floor.py ..."
    )

sys.path.insert(0, str(Path(__file__).resolve().parent))

import floor_schema  # noqa: E402  (the single owner of the atlas floor derivation)
import ost_floor_schema  # noqa: E402  (the single owner of the OST coherence-floor derivation)
import align_terms  # noqa: E402  (#9a — the live-graph SSSOM aligner; computes what was declared)

REPO = Path(__file__).resolve().parents[2]
CASES_DIR = REPO / "research" / "consult" / "cases" / "reconciliation"

PLACES = 4
EXACT_ALIGN = "exactMatch"
# UNALIGNED: the graph supports NO mapping between two anchor terms (distinct, unlinked
# concepts). The weakest tier — the strongest false-agreement risk — surfaced when the
# alignment is COMPUTED (#9a) rather than declared.
UNALIGNED = "unaligned"
# SSSOM predicates that are weaker than exact -> a false-(dis)agreement risk (you may be
# comparing not-quite-the-same claim). The full catalog the upstream aligner emits.
NEAR_ALIGN = {"closeMatch", "narrowMatch", "broadMatch", "relatedMatch", UNALIGNED}
ALIGN_PREDICATES = {EXACT_ALIGN} | NEAR_ALIGN
# severity order for picking a verdict's WEAKEST (most risky) pairwise predicate.
_ALIGN_SEVERITY = {
    EXACT_ALIGN: 0,
    "closeMatch": 1,
    "narrowMatch": 2,
    "broadMatch": 2,
    "relatedMatch": 3,
    UNALIGNED: 4,
}
STATUSES = {"resolve", "abstain"}

CORROBORATED = "corroborated"
CONTESTED = "contested"
SUBSTRATE_CONDITIONAL = "substrate-conditional"
JOINTLY_UNRESOLVED = "jointly-unresolved"
LATTICE = {CORROBORATED, CONTESTED, SUBSTRATE_CONDITIONAL, JOINTLY_UNRESOLVED}


# --- floor reading (declared, or live from a real atlas) ---------------------


def atlas_combined_floor(
    atlas_rel: str, band: str = "combined", basis: str = "mean"
) -> tuple[float | None, str]:
    """Read an endpoint's own combined nested floor LIVE from an atlas, via floor_schema —
    the same derivation verify_contract uses, so an endpoint's self_floor cannot drift from
    its atlas. Returns (value, error)."""
    path = Path(atlas_rel)
    if not path.is_absolute():
        path = REPO / atlas_rel
    if not path.exists():
        return None, f"atlas not found: {atlas_rel}"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as e:
        return None, f"atlas unreadable: {e}"
    schema, floor = floor_schema.normalize_floor((data or {}).get("variance") or {})
    if schema == floor_schema.NONE:
        return None, f"atlas exposes no floor: {atlas_rel}"
    key = {
        ("combined", "mean"): "combined_floor",
        ("combined", "worst_case"): "combined_worst_case_max",
        ("operator", "mean"): "operator_floor_mean",
        ("artifact", "mean"): "artifact_floor_mean",
    }.get((band, basis))
    if key is None:
        return None, f"unsupported band/basis: {band}/{basis}"
    val = floor.get(key)
    if val is None:
        return None, f"atlas has no {band}/{basis} floor"
    return float(val), ""


def spec_audit_combined_floor(
    audit_rel: str, band: str = "combined", basis: str = "mean"
) -> tuple[float | None, str]:
    """Read an OST endpoint's own combined COHERENCE floor LIVE from a spec-audit artifact, via
    ost_floor_schema — the SAME derivation verify_ost_contract uses, so the OST endpoint's
    self_floor cannot drift from its audit. This is the OST analogue of atlas_combined_floor:
    where the SBT endpoint reads a measurement noise floor from an atlas, the OST endpoint reads
    a specification coherence floor (incoherence 1-SCI + audit gap) from a spec-audit. Both
    endpoints of the substrate floor are now instrument-owned. Returns (value, error).
    """
    path = Path(audit_rel)
    if not path.is_absolute():
        path = REPO / audit_rel
    if not path.exists():
        return None, f"spec-audit not found: {audit_rel}"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as e:
        return None, f"spec-audit unreadable: {e}"
    schema, floor = ost_floor_schema.normalize_ost_floor(
        data if isinstance(data, dict) else {}
    )
    if schema == ost_floor_schema.NONE:
        return None, f"spec-audit exposes no coherence floor: {audit_rel}"
    key = {
        ("combined", "mean"): "combined_floor",
        ("combined", "worst_case"): "combined_worst_case_max",
        ("coherence", "mean"): "coherence_floor_mean",
        ("audit", "mean"): "audit_floor_mean",
    }.get((band, basis))
    if key is None:
        return None, f"unsupported band/basis: {band}/{basis}"
    val = floor.get(key)
    if val is None:
        return None, f"spec-audit has no {band}/{basis} floor"
    return float(val), ""


def self_floor_of(v: dict) -> tuple[float | None, str, str]:
    """(value, source, error) for a resolver's own combined floor. Either a declared
    `self_floor`, or a live read via `floor_ref`: an SBT measurement floor from an atlas
    (`floor_ref: {atlas, band, basis}`) OR an OST coherence floor from a spec-audit
    (`floor_ref: {spec_audit, band, basis}`) — both instrument-owned, neither can drift.
    """
    if v.get("self_floor") is not None:
        try:
            return float(v["self_floor"]), "declared", ""
        except (TypeError, ValueError):
            return None, "", f"self_floor not a number: {v.get('self_floor')!r}"
    ref = v.get("floor_ref")
    if isinstance(ref, dict) and ref.get("atlas"):
        val, err = atlas_combined_floor(
            ref["atlas"], ref.get("band", "combined"), ref.get("basis", "mean")
        )
        return val, f"atlas:{ref['atlas']}", err
    if isinstance(ref, dict) and ref.get("spec_audit"):
        val, err = spec_audit_combined_floor(
            ref["spec_audit"], ref.get("band", "combined"), ref.get("basis", "mean")
        )
        return val, f"spec_audit:{ref['spec_audit']}", err
    return None, "", "a resolver needs self_floor or floor_ref"


# --- the reconciliation ------------------------------------------------------


def _pairwise_max(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return max(abs(a - b) for i, a in enumerate(values) for b in values[i + 1 :])


def _entropy(counts: list[int]) -> float:
    """Normalized Shannon entropy of a categorical distribution (0 = unanimous, 1 = maximally
    split). The categorical layer of the substrate floor: how split the resolve/abstain vote is.
    """
    total = sum(counts)
    nz = [c for c in counts if c > 0]
    if total == 0 or len(nz) < 2:
        return 0.0
    h = -sum((c / total) * math.log2(c / total) for c in nz)
    return round(h / math.log2(len(nz)), PLACES)


def _load_external_mapping(ext_ref: str) -> dict:
    """Load an external substrate descriptor's declared SSSOM mapping (#9b)."""
    path = Path(ext_ref) if Path(ext_ref).is_absolute() else REPO / ext_ref
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}
    return doc.get("sssom_mapping") or {}


def _inject_computed_alignments(con: sqlite3.Connection | None, verdicts: list) -> None:
    """Replace a verdict's HAND-DECLARED alignment with one derived from the live substrate.

    #9a (corpus, in-graph): when a verdict names its anchor `align_term`, its effective alignment
    is the WEAKEST (most risky) predicate over its pairs with the other anchored verdicts (via the
    live terms graph) — so an unlinked cross-framework pair surfaces as a risk a declared
    `exactMatch` would have hidden.

    #9b (external, cross-vendor): when a verdict names an `external_ref` (a non-corpus substrate
    descriptor), its concept is not in our graph, so the alignment is VALIDATED rather than
    computed — the external author's declared SSSOM mapping must land on a real corpus anchor; an
    `unaligned` result for a broken/unanchored mapping then triggers the same downgrade.

    Verdicts with neither anchor keep their declared predicate. No-op without a substrate
    connection (hermetic runs fall back to the declared predicate).
    """
    if con is None:
        return
    # #9b — external substrates first: validate each declared mapping against the corpus anchor.
    for v in verdicts:
        if not v.get("external_ref"):
            continue
        r = align_terms.align_external(con, _load_external_mapping(v["external_ref"]))
        v["alignment"] = r["predicate"] or UNALIGNED
        v["alignment_basis"] = "external"
        v["alignment_detail"] = r["justification"]
    # #9a — corpus pairwise alignment among the in-graph anchored verdicts.
    bearers = [v for v in verdicts if v.get("align_term")]
    if len(bearers) < 2:
        return
    for v in bearers:
        worst, worst_sev, detail = EXACT_ALIGN, 0, []
        for w in bearers:
            if w is v:
                continue
            r = align_terms.compute_alignment(con, v["align_term"], w["align_term"])
            pred = r["predicate"] or UNALIGNED
            detail.append(f"{w.get('substrate', '?')}:{pred}")
            sev = _ALIGN_SEVERITY.get(pred, _ALIGN_SEVERITY[UNALIGNED])
            if sev > worst_sev:
                worst, worst_sev = pred, sev
        v["alignment"] = worst
        v["alignment_basis"] = "computed"
        v["alignment_detail"] = "; ".join(detail)


def reconcile(case: dict, con: sqlite3.Connection | None = None) -> dict:
    """Compute the substrate floor + the typed-verdict lattice for one shared claim. Returns a
    result dict (never raises on a contested/abstaining outcome — those are valid honest
    verdicts); the `errors` key is non-empty only on a MALFORMED case."""
    errors: list[str] = []
    sc = case.get("shared_claim") or {}
    if not sc.get("id") or not sc.get("common_axis"):
        errors.append(
            "shared_claim needs id + common_axis (the commensurable verdict axis)"
        )
    k_resolve = float(case.get("k_resolve", 2.0))
    k_marginal = float(case.get("k_marginal", 1.0))
    verdicts = case.get("substrate_verdicts") or []
    _inject_computed_alignments(con, verdicts)  # #9a: compute alignment where anchored
    if len(verdicts) < 2:
        errors.append("a cross-substrate reconciliation needs >=2 substrate_verdicts")

    excluded, covering = [], []
    for v in verdicts:
        name = v.get("substrate", "?")
        if v.get("status") not in STATUSES:
            errors.append(f"[{name}] status must be one of {sorted(STATUSES)}")
            continue
        if v.get("alignment") not in ALIGN_PREDICATES:
            errors.append(
                f"[{name}] alignment must be an SSSOM predicate {sorted(ALIGN_PREDICATES)}"
            )
        if not v.get(
            "audit_pass", True
        ):  # §1 self-certification: excluded, never averaged
            excluded.append(name)
            continue
        covering.append(v)

    resolvers = [v for v in covering if v.get("status") == "resolve"]
    abstainers = [v for v in covering if v.get("status") == "abstain"]

    # resolver floors + values
    res_rows: list[dict] = []
    res_values: list[float] = []
    res_floors: list[float] = []
    near_align: list[str] = []
    unaligned_resolvers: list[str] = []
    for v in resolvers:
        name = v.get("substrate", "?")
        if v.get("value") is None:
            errors.append(f"[{name}] a resolver needs a value on the common axis")
            continue
        fl, src, err = self_floor_of(v)
        if err or fl is None:
            errors.append(f"[{name}] {err or 'no floor'}")
            continue
        res_values.append(float(v["value"]))
        res_floors.append(fl)
        if v.get("alignment") in NEAR_ALIGN:
            basis = v.get("alignment_basis", "declared")
            near_align.append(f"{name}({v['alignment']},{basis})")
            if v.get("alignment") == UNALIGNED:
                unaligned_resolvers.append(name)
        res_rows.append(
            {
                "substrate": name,
                "value": float(v["value"]),
                "self_floor": fl,
                "floor_source": src,
            }
        )

    if errors:
        return {"shared_claim": sc.get("id"), "errors": errors}

    # --- the substrate floor + nesting ---
    dispersion = round(_pairwise_max(res_values), PLACES)
    max_self_floor = round(max(res_floors), PLACES) if res_floors else None
    # nested: operator (subset) artifact (subset) substrate. The effective floor is the widest.
    floor_bands: list[float] = [dispersion]
    if max_self_floor is not None:
        floor_bands.append(max_self_floor)
    effective_floor = round(max(floor_bands), PLACES)
    consensus = round(sum(res_values) / len(res_values), PLACES) if res_values else None
    sn = (
        round(abs(consensus) / effective_floor, 2)
        if (consensus is not None and effective_floor > 0)
        else None
    )
    # do the resolvers agree WITHIN their own measurement floors? (real agreement, not an
    # artifact of one being noisier than its separation from the other)
    within_floor = max_self_floor is not None and dispersion <= max_self_floor
    entropy = _entropy([len(resolvers), len(abstainers)])

    # --- the lattice ---
    if len(resolvers) == 0:
        verdict, why = JOINTLY_UNRESOLVED, "every covering substrate abstains"
    elif len(resolvers) == 1:
        if sn is not None and sn >= k_resolve:
            verdict, why = (
                SUBSTRATE_CONDITIONAL,
                f"one substrate resolves (S/N {sn} >= {k_resolve}); the rest abstain — "
                f"the finding holds only under that apparatus",
            )
        else:
            verdict, why = (
                JOINTLY_UNRESOLVED,
                f"the lone resolver does not clear its own floor (S/N {sn})",
            )
    elif not within_floor:
        verdict, why = (
            CONTESTED,
            f"resolvers disagree beyond their floors (dispersion {dispersion} > "
            f"max self-floor {max_self_floor}) — characterize why; human judgment required",
        )
    elif sn is not None and sn >= k_resolve:
        verdict, why = (
            CORROBORATED,
            f"resolvers agree within their floors (dispersion {dispersion} <= "
            f"{max_self_floor}) and the consensus clears the effective floor "
            f"(S/N {sn} >= {k_resolve})",
        )
    else:
        band = "marginal" if (sn is not None and sn >= k_marginal) else "below floor"
        verdict, why = (
            JOINTLY_UNRESOLVED,
            f"resolvers agree but the consensus is {band} (S/N {sn} < {k_resolve}) — "
            f"agreement on noise, honestly unknown",
        )

    # ALIGNMENT downgrade: you cannot CORROBORATE across concepts that don't align. If any
    # resolver's anchor term is UNALIGNED with another's (the graph supports no mapping), the
    # numeric agreement may be a FALSE agreement across distinct concepts — downgrade to
    # contested so a human judges whether the findings are even about the same thing. (A
    # weaker-than-exact-but-mapped predicate, e.g. relatedMatch, stays an annotation; only a
    # complete absence of mapping forces the downgrade.)
    if verdict == CORROBORATED and unaligned_resolvers:
        verdict, why = (
            CONTESTED,
            f"resolvers agree numerically, but their anchor terms are UNALIGNED in the graph "
            f"({', '.join(unaligned_resolvers)}) — possible false agreement across distinct "
            f"concepts; human judgment required before corroborating",
        )

    result = {
        "shared_claim": sc.get("id"),
        "common_axis": sc.get("common_axis"),
        "k_resolve": k_resolve,
        "k_marginal": k_marginal,
        "covering": [v.get("substrate") for v in covering],
        "excluded_audit_fail": excluded,
        "resolvers": res_rows,
        "abstainers": [v.get("substrate") for v in abstainers],
        "substrate_dispersion": dispersion,
        "max_self_floor": max_self_floor,
        "effective_floor": effective_floor,
        "consensus": consensus,
        "signal_to_noise": sn,
        "within_floor": within_floor,
        "verdict_entropy": entropy,
        "alignment_risk": near_align,  # non-exact alignments: false-(dis)agreement risk
        "verdict": verdict,
        "rationale": why,
        "errors": [],
    }
    return result


# --- reporting / gate --------------------------------------------------------


def _render(case_name: str, r: dict) -> tuple[str, bool]:
    """(text, ok). ok=False only on a MALFORMED case or an expect-mismatch — NOT on a
    contested/unresolved verdict (those are valid honest outcomes)."""
    if r.get("errors"):
        lines = [f"[{case_name}] MALFORMED:"]
        lines += [f"    - {e}" for e in r["errors"]]
        return "\n".join(lines), False
    L = [f"[{case_name}] {r['shared_claim']} -> {r['verdict'].upper()}"]
    L.append(
        f"    covering={r['covering']}  resolvers={[x['substrate'] for x in r['resolvers']]}  abstain={r['abstainers']}"
    )
    if r["excluded_audit_fail"]:
        L.append(f"    excluded (audit fail, §1): {r['excluded_audit_fail']}")
    L.append(
        f"    dispersion={r['substrate_dispersion']}  max_self_floor={r['max_self_floor']}  "
        f"effective_floor={r['effective_floor']}  consensus={r['consensus']}  S/N={r['signal_to_noise']}"
    )
    L.append(
        f"    within_floor={r['within_floor']}  verdict_entropy={r['verdict_entropy']}"
    )
    if r["alignment_risk"]:
        L.append(
            f"    ALIGNMENT RISK (non-exact, possible false agreement): {r['alignment_risk']}"
        )
    L.append(f"    why: {r['rationale']}")
    return "\n".join(L), True


def run(paths: list[Path], con: sqlite3.Connection | None = None) -> int:
    ok = True
    n = 0
    for p in paths:
        try:
            doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as e:
            print(f"[{p.name}] unreadable: {e}", file=sys.stderr)
            ok = False
            continue
        # a file may hold one case or a list under `cases:`
        cases = doc["cases"] if isinstance(doc, dict) and "cases" in doc else [doc]
        for case in cases:
            n += 1
            label = case.get("name") or case.get("shared_claim", {}).get("id") or p.stem
            r = reconcile(case, con)
            text, good = _render(label, r)
            expect = case.get("expect")
            if good and expect and expect not in LATTICE:
                text += f"\n    [BAD expect: '{expect}' not a lattice verdict]"
                good = False
            elif good and expect and r["verdict"] != expect:
                text += f"\n    [EXPECT MISMATCH: got '{r['verdict']}', expected '{expect}']"
                good = False
            print(text)
            ok = ok and good
    print(f"\n[substrate-floor] {n} reconciliation(s); {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("cases", nargs="*", help="reconciliation case YAML(s)")
    ap.add_argument(
        "--all", action="store_true", help=f"reconcile every *.yaml in {CASES_DIR}"
    )
    args = ap.parse_args()
    if args.all:
        paths = sorted(CASES_DIR.glob("*.yaml"))
        if not paths:
            sys.exit(f"no reconciliation cases in {CASES_DIR}")
    elif args.cases:
        paths = [Path(c) if Path(c).is_absolute() else REPO / c for c in args.cases]
    else:
        ap.error("pass case file(s) or --all")
    # Connect to the substrate so anchored verdicts get a COMPUTED alignment (#9a);
    # absent the DB (hermetic / external), the declared predicate stands.
    con = align_terms.connect() if align_terms.DB.exists() else None
    return run(paths, con)


if __name__ == "__main__":
    raise SystemExit(main())
