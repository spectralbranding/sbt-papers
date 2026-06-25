#!/usr/bin/env python3
"""Auto-derive an SSSOM alignment predicate for a term PAIR from the live substrate.

The substrate floor (`substrate_floor.py`, rule §0 "align before you adjudicate")
needs to know whether two substrates' verdicts on a "shared claim" really mean the
same thing, or only seem to (false agreement). Until now each verdict DECLARED its
SSSOM predicate (`alignment: exactMatch`) by hand. A hand-declared `exactMatch` is
exactly the optimism the alignment step exists to catch.

This module computes the predicate instead, by reading the live `terms` /
`term_relations` graph — the run-time counterpart of `negotiate_modules.py`, which
classifies the same interactions from module FILES (def_hash identity + refine
edges). It reuses negotiate's SSSOM vocabulary so the two aligners agree:

    identical term_key, identical def_hash   -> exactMatch   (negotiate: AGREEMENT)
    identical term_key, different def_hash    -> closeMatch   (negotiate: CONFLICT)
    `synonym` edge                            -> exactMatch
    `narrows` / `specializes` edge (a->b)     -> narrowMatch  (a is narrower than b)
        ... in the other direction            -> broadMatch
    `maps_to` edge                            -> relatedMatch (positional / partial overlap)
    `contrasts` edge                          -> relatedMatch (explicitly contrasted: high risk)
    no edge, distinct terms                   -> None         (UNALIGNED — strongest risk)

A non-`exactMatch` (or `None`) result is a false-(dis)agreement risk the caller
surfaces; it never silently trusts a cross-substrate comparison. A term absent
from the graph (e.g. a non-corpus external substrate, #9b) returns None with a
distinct reason, so the caller falls back to a declared predicate.

Read-only on the substrate. Run for inspection:

    uv run python code/align_terms.py brand-management-correspondence-theorem six-tier-ontology
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB = REPO / "research" / "corpus_substrate.sqlite"

EXACT = "exactMatch"
CLOSE = "closeMatch"
NARROW = "narrowMatch"
BROAD = "broadMatch"
RELATED = "relatedMatch"

# A directed term_relations edge (source --rel--> target), read in the direction
# (term_a, term_b), maps to the predicate "term_a <pred> term_b". The reverse
# direction inverts narrow/broad.
_FORWARD = {
    "synonym": EXACT,
    "narrows": NARROW,
    "specializes": NARROW,
    "maps_to": RELATED,
    "contrasts": RELATED,
}
_REVERSE = (
    {  # edge stored as (term_b --rel--> term_a): predicate for "term_a <pred> term_b"
        "synonym": EXACT,
        "narrows": BROAD,
        "specializes": BROAD,
        "maps_to": RELATED,
        "contrasts": RELATED,
    }
)
_CONFIDENCE = {EXACT: 0.95, NARROW: 0.9, BROAD: 0.9, CLOSE: 0.7, RELATED: 0.55}

# SKOS predicate ids (as written in an SSSOM mapping) -> our bare predicate vocabulary.
_SKOS_TO_PRED = {
    "skos:exactMatch": EXACT,
    "skos:closeMatch": CLOSE,
    "skos:narrowMatch": NARROW,
    "skos:broadMatch": BROAD,
    "skos:relatedMatch": RELATED,
    # tolerate the bare forms too
    EXACT: EXACT,
    CLOSE: CLOSE,
    NARROW: NARROW,
    BROAD: BROAD,
    RELATED: RELATED,
}


def connect(db: Path = DB) -> sqlite3.Connection:
    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    return con


def _term_row(con: sqlite3.Connection, key: str) -> sqlite3.Row | None:
    return con.execute(
        "SELECT term_key, owner_paper_key, def_hash FROM terms WHERE term_key = ?",
        (key,),
    ).fetchone()


def _edge(con: sqlite3.Connection, a: str, b: str) -> tuple[str, str] | None:
    """Return (relation_type, direction) for an edge between a and b, or None.

    direction is 'forward' for a->b, 'reverse' for b->a.
    """
    row = con.execute(
        "SELECT relation_type FROM term_relations "
        "WHERE source_term_key = ? AND target_term_key = ? LIMIT 1",
        (a, b),
    ).fetchone()
    if row:
        return (row["relation_type"], "forward")
    row = con.execute(
        "SELECT relation_type FROM term_relations "
        "WHERE source_term_key = ? AND target_term_key = ? LIMIT 1",
        (b, a),
    ).fetchone()
    if row:
        return (row["relation_type"], "reverse")
    return None


def compute_alignment(con: sqlite3.Connection, term_a: str, term_b: str) -> dict:
    """Derive the SSSOM predicate aligning term_a to term_b from the live graph.

    Returns {predicate, confidence, justification, basis} — predicate is None when
    the graph supports no alignment (unlinked distinct terms) or a term is absent
    (the caller then falls back to a declared predicate). basis is one of
    'identical' / 'def_hash' / 'edge:<rel>' / 'unlinked' / 'absent'.
    """
    ra, rb = _term_row(con, term_a), _term_row(con, term_b)
    absent = [t for t, r in ((term_a, ra), (term_b, rb)) if r is None]
    if absent:
        return {
            "predicate": None,
            "confidence": None,
            "basis": "absent",
            "justification": f"term(s) not in substrate: {', '.join(absent)}",
        }
    assert ra is not None and rb is not None  # narrowed by the absent check above

    if term_a == term_b:
        same = ra["def_hash"] == rb["def_hash"]
        pred = EXACT if same else CLOSE
        return {
            "predicate": pred,
            "confidence": _CONFIDENCE[pred],
            "basis": "identical" if same else "def_hash",
            "justification": (
                "same term_key, identical def_hash"
                if same
                else "same term_key, divergent def_hash"
            ),
        }

    edge = _edge(con, term_a, term_b)
    if edge is None:
        return {
            "predicate": None,
            "confidence": None,
            "basis": "unlinked",
            "justification": (
                f"no term_relations edge between '{term_a}' ({ra['owner_paper_key']}) "
                f"and '{term_b}' ({rb['owner_paper_key']}) — distinct, unlinked concepts"
            ),
        }
    rel, direction = edge
    table = _FORWARD if direction == "forward" else _REVERSE
    edge_pred = table.get(rel)
    arrow = (
        f"{term_a} -{rel}-> {term_b}"
        if direction == "forward"
        else f"{term_b} -{rel}-> {term_a}"
    )
    return {
        "predicate": edge_pred,
        "confidence": _CONFIDENCE.get(edge_pred) if edge_pred else None,
        "basis": f"edge:{rel}",
        "justification": f"{rel} edge ({arrow})",
    }


def align_external(con: sqlite3.Connection, mapping: dict) -> dict:
    """Align a genuinely EXTERNAL (non-corpus) substrate to a corpus claim via a DECLARED SSSOM
    mapping (#9b — the cross-vendor case). The external term is not in our graph, so we cannot
    COMPUTE the predicate (that is the point of a boundary). Instead the external author declares
    `{subject_id, predicate_id, object_id}` mapping its concept to a corpus term, and we VALIDATE
    the corpus side: the `object_id` MUST exist in `terms`, and the predicate must be a known SKOS
    mapping predicate. Returns {predicate (bare), confidence, basis, justification} — basis is
    'external-validated' (corpus anchor exists) or 'external-unanchored' (predicate forced to None
    so the caller surfaces the broken mapping as the strongest risk). We never invent the predicate;
    we only check that what the vendor claims lands on a real corpus concept.
    """
    obj = mapping.get("object_id")
    raw_pred = mapping.get("predicate_id")
    pred = _SKOS_TO_PRED.get(raw_pred) if isinstance(raw_pred, str) else None
    if pred is None:
        return {
            "predicate": None,
            "confidence": None,
            "basis": "external-unanchored",
            "justification": f"unknown SSSOM predicate: {raw_pred!r}",
        }
    if obj is None or _term_row(con, obj) is None:
        return {
            "predicate": None,
            "confidence": None,
            "basis": "external-unanchored",
            "justification": f"declared corpus anchor '{obj}' is not in the substrate",
        }
    return {
        "predicate": pred,
        "confidence": _CONFIDENCE.get(pred),
        "basis": "external-validated",
        "justification": (
            f"external mapping {mapping.get('subject_id')} {raw_pred} {obj} "
            f"(corpus anchor exists)"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("term_a")
    ap.add_argument("term_b")
    args = ap.parse_args()
    con = connect()
    r = compute_alignment(con, args.term_a, args.term_b)
    pred = r["predicate"] or "UNALIGNED"
    print(f"{args.term_a}  <->  {args.term_b}")
    print(f"  predicate : {pred}")
    print(f"  basis     : {r['basis']}")
    print(f"  why       : {r['justification']}")
    if r["confidence"] is not None:
        print(f"  confidence: {r['confidence']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
