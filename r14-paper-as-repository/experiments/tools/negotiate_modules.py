"""Federated cross-owner negotiation for ontology modules (the multi-author linker).

The single-author linker (build_ontology.py) ERRORS on a unique-owner collision:
within one corpus a term has exactly one owning module, full stop. That is the
right behavior when modules are temporal slices of ONE author's program,
reconciled by rebase. It is the WRONG behavior across authors: when two
independent authors each legitimately own a term, the collision is not a bug to
abort on -- it is a negotiation to surface.

This tool is that federated generalization. Given two authors' module sets, it
does NOT error on cross-owner overlap; instead it classifies every cross-owner
interaction and proposes a reconciliation, so two authors can see -- mechanically,
before reading each other's prose -- exactly where their vocabularies agree,
conflict, or extend one another. This is the evidence that upgrades the
"negotiate a paper before you read it" claim from single-author existence proof
to the federated case (see the negotiation protocol (paper §5.5)).

Interaction classes (per shared/cross term):
  AGREEMENT        both authors own the same term_key with IDENTICAL def_hash.
                   Reconcile by MERGE: assert skos:exactMatch; either author may
                   import the other's term with no change.
  CONFLICT         both own the same term_key with DIFFERENT def_hash. A genuine
                   incompatibility. Reconcile by NAMESPACE (author-qualify the
                   colliding keys) + a curated mapping (skos:closeMatch when the
                   concept is the same but the definition differs;
                   skos:relatedMatch when the key collides on distinct concepts);
                   then FORK the loser's key if the concepts truly differ.
  CROSS_REFINE     author X refines a term owned by author Y, with a narrows_to.
                   Compatible: reconcile by REBASE -- X's refinement becomes a
                   skos:narrowMatch / `narrows` edge onto Y's term.
  INCOMPATIBLE_REFINE  X refines Y's term without a narrows_to. Unresolved until
                   X supplies an explicit narrowing.
  CROSS_IMPORT     X imports a term the OTHER author owns. Clean dependency edge;
                   no negotiation needed.
  DANGLING_IMPORT  X imports a term NEITHER author owns. Unresolved: someone must
                   own it, or X must drop the import.

Default behavior REPORTS (exit 0). With --gate it exits nonzero when any
unresolved interaction remains (CONFLICT / INCOMPATIBLE_REFINE / DANGLING_IMPORT)
-- the federated CI semantics. --sssom writes the proposed mappings as an SSSOM
TSV (subject/predicate/object/justification/confidence), the standard this
corpus emits into for typed, justified term mappings (Matentzoglu et al. 2022).

Run:
  uv run python tools/negotiate_modules.py \
      --author-a the in-repo two-author fixtureauthorA \
      --author-b the in-repo two-author fixtureauthorB
  ...  --sssom out.tsv      # also emit the SSSOM mapping proposal
  ...  --gate               # exit nonzero on unresolved interactions
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Reuse the single-author linker's parser + content-addressing so the two
# linkers can never disagree on how a module is read or a definition hashed.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_ontology import Module, def_hash, _norm_ref  # noqa: E402

import yaml  # noqa: E402

# Interaction classes that block a clean federation (the --gate set).
UNRESOLVED = {"CONFLICT", "INCOMPATIBLE_REFINE", "DANGLING_IMPORT"}

# SKOS mapping predicate proposed per interaction class.
PREDICATE = {
    "AGREEMENT": "skos:exactMatch",
    "CONFLICT": "skos:closeMatch",  # same concept, divergent definition
    "CROSS_REFINE": "skos:narrowMatch",  # refiner's term is narrower
    "CROSS_IMPORT": "skos:exactMatch",  # importing the other's term verbatim
}

# Reconciliation operation proposed per interaction class (the lock/fork/rebase/
# merge vocabulary from SPINE_FIRST_DRAFTING_PROTOCOL.md, generalized to owners).
OPERATION = {
    "AGREEMENT": "MERGE (assert exactMatch; either may import the other)",
    "CONFLICT": "NAMESPACE + curate mapping; FORK the key if concepts differ",
    "CROSS_REFINE": "REBASE (refiner's term narrows the owner's; assert narrowMatch)",
    "INCOMPATIBLE_REFINE": "BLOCK until refiner supplies an explicit narrows_to",
    "CROSS_IMPORT": "none (clean dependency edge)",
    "DANGLING_IMPORT": "BLOCK until some author owns the term or the import is dropped",
}


def load_author(spec: str) -> tuple[str, list[Module]]:
    """Load one author's modules from a directory or a single file path.

    Returns (author_label, modules). The author label is the directory name
    (or file stem) -- the namespace used to qualify colliding term keys.
    """
    p = Path(spec)
    if p.is_dir():
        paths = sorted(p.glob("*.yaml")) + sorted(p.glob("*.yml"))
        label = p.name
    else:
        paths = [p]
        label = p.stem
    mods: list[Module] = []
    for fp in paths:
        data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict) and data.get("paper_key"):
            mods.append(Module(fp, data))
    return label, mods


def index_author(mods: list[Module]) -> dict:
    """Build {owns: {tk: row}, imports: {tk}, refines: {tk: narrows_to|None}}."""
    owns: dict[str, dict] = {}
    imports: set[str] = set()
    refines: dict[str, str | None] = {}
    for m in mods:
        for o in m.owns:
            if isinstance(o, dict) and o.get("term_key"):
                d = (o.get("definition") or "").strip()
                owns[o["term_key"]] = {
                    "definition": d,
                    "def_hash": def_hash(d),
                    "label": o.get("label") or o["term_key"],
                    "paper_key": m.paper_key,
                }
        for imp in m.imports:
            tk = _norm_ref(imp).get("term_key")
            if tk:
                imports.add(tk)
        for rf in m.refines:
            ref = _norm_ref(rf)
            tk = ref.get("term_key")
            if tk:
                refines[tk] = ref.get("narrows_to") or ref.get("note")
    return {"owns": owns, "imports": imports, "refines": refines}


def negotiate(a_label: str, a: dict, b_label: str, b: dict) -> list[dict]:
    """Classify every cross-owner interaction between two authors. Returns a list
    of finding dicts: {class, term_key, detail, predicate, operation}."""
    findings: list[dict] = []

    def add(cls: str, tk: str, detail: str):
        findings.append(
            {
                "class": cls,
                "term_key": tk,
                "detail": detail,
                "predicate": PREDICATE.get(cls),
                "operation": OPERATION[cls],
            }
        )

    a_owns, b_owns = a["owns"], b["owns"]

    # 1. terms owned by BOTH -> AGREEMENT or CONFLICT
    for tk in sorted(set(a_owns) & set(b_owns)):
        if a_owns[tk]["def_hash"] == b_owns[tk]["def_hash"]:
            add(
                "AGREEMENT",
                tk,
                f"identical definition (def_hash {a_owns[tk]['def_hash']})",
            )
        else:
            same_concept = a_owns[tk]["label"].lower() == b_owns[tk]["label"].lower()
            note = (
                "same label, divergent definition"
                if same_concept
                else "key collides on differing labels"
            )
            add(
                "CONFLICT",
                tk,
                f"{note}; {a_label}='{a_owns[tk]['definition']}' vs "
                f"{b_label}='{b_owns[tk]['definition']}'",
            )

    # 2. cross-refines: each author refining a term the OTHER owns
    for refiner_label, refiner, owner_owns in (
        (a_label, a, b_owns),
        (b_label, b, a_owns),
    ):
        for tk, narrows_to in refiner["refines"].items():
            if tk in owner_owns:
                if narrows_to:
                    add(
                        "CROSS_REFINE",
                        tk,
                        f"{refiner_label} narrows owner's term: '{narrows_to}'",
                    )
                else:
                    add(
                        "INCOMPATIBLE_REFINE",
                        tk,
                        f"{refiner_label} refines without a narrows_to",
                    )
            elif tk not in refiner["owns"]:
                add(
                    "DANGLING_IMPORT",
                    tk,
                    f"{refiner_label} refines '{tk}' owned by neither author",
                )

    # 3. cross-imports: each author importing a term
    both_owned = set(a_owns) | set(b_owns)
    for importer_label, importer, other_owns in (
        (a_label, a, b_owns),
        (b_label, b, a_owns),
    ):
        for tk in sorted(importer["imports"]):
            if tk in other_owns:
                add(
                    "CROSS_IMPORT",
                    tk,
                    f"{importer_label} imports the other author's term",
                )
            elif tk in importer["owns"]:
                continue  # redundant self-import; not a cross-owner concern
            elif tk not in both_owned:
                add(
                    "DANGLING_IMPORT",
                    tk,
                    f"{importer_label} imports '{tk}' owned by neither author",
                )

    return findings


def render_report(a_label: str, b_label: str, findings: list[dict]) -> str:
    by_class: dict[str, list[dict]] = {}
    for f in findings:
        by_class.setdefault(f["class"], []).append(f)
    lines = [
        f"NEGOTIATION REPORT  {a_label}  <->  {b_label}",
        "=" * 64,
    ]
    order = [
        "CONFLICT",
        "INCOMPATIBLE_REFINE",
        "DANGLING_IMPORT",
        "CROSS_REFINE",
        "AGREEMENT",
        "CROSS_IMPORT",
    ]
    for cls in order:
        items = by_class.get(cls, [])
        if not items:
            continue
        lines.append(f"\n{cls}  ({len(items)})")
        for f in items:
            pred = f" [{f['predicate']}]" if f["predicate"] else ""
            lines.append(f"  - {f['term_key']}{pred}: {f['detail']}")
            lines.append(f"      -> reconcile: {f['operation']}")
    unresolved = [f for f in findings if f["class"] in UNRESOLVED]
    lines.append("\n" + "-" * 64)
    lines.append(
        f"{len(findings)} interaction(s); {len(unresolved)} unresolved "
        f"(CONFLICT / INCOMPATIBLE_REFINE / DANGLING_IMPORT)."
    )
    if unresolved:
        lines.append(
            "Federation NOT clean: the authors must reconcile the unresolved "
            "interactions (namespace + curate mappings, supply narrowings, or "
            "assign owners) before the modules link across authors."
        )
    else:
        lines.append(
            "Federation clean: all interactions are agreements, clean imports, "
            "or compatible refinements -- the two module sets can be linked."
        )
    return "\n".join(lines)


def render_sssom(a_label: str, b_label: str, findings: list[dict]) -> str:
    """Emit the proposed mappings as an SSSOM TSV (Matentzoglu et al. 2022).

    Only interactions that yield a term<->term mapping are emitted (AGREEMENT,
    CONFLICT, CROSS_REFINE, CROSS_IMPORT). The justification distinguishes a
    mechanical lexical/hash match from a proposal needing manual curation.
    """
    rows = [
        "subject_id\tpredicate_id\tobject_id\tmapping_justification\tconfidence\tcomment"
    ]
    for f in findings:
        if not f["predicate"]:
            continue
        subj = f"{a_label}:{f['term_key']}"
        obj = f"{b_label}:{f['term_key']}"
        if f["class"] == "AGREEMENT":
            just, conf = "semapv:LexicalMatching", "1.0"
        elif f["class"] == "CROSS_IMPORT":
            just, conf = "semapv:LexicalMatching", "0.95"
        else:  # CONFLICT, CROSS_REFINE -> human must confirm
            just, conf = "semapv:ManualMappingCuration", "0.5"
        comment = f["class"]
        rows.append(f"{subj}\t{f['predicate']}\t{obj}\t{just}\t{conf}\t{comment}")
    return "\n".join(rows)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--author-a", required=True, help="dir or file of author A's modules"
    )
    ap.add_argument(
        "--author-b", required=True, help="dir or file of author B's modules"
    )
    ap.add_argument(
        "--sssom", metavar="PATH", help="write the proposed mappings as an SSSOM TSV"
    )
    ap.add_argument(
        "--gate",
        action="store_true",
        help="exit nonzero if any interaction is unresolved",
    )
    args = ap.parse_args()

    a_label, a_mods = load_author(args.author_a)
    b_label, b_mods = load_author(args.author_b)
    if not a_mods or not b_mods:
        print(
            "ERROR: each author must provide at least one module with a paper_key",
            file=sys.stderr,
        )
        raise SystemExit(2)

    a = index_author(a_mods)
    b = index_author(b_mods)
    findings = negotiate(a_label, a, b_label, b)

    print(render_report(a_label, b_label, findings))

    if args.sssom:
        Path(args.sssom).write_text(
            render_sssom(a_label, b_label, findings) + "\n", encoding="utf-8"
        )
        print(f"\n[SSSOM] mapping proposal written: {args.sssom}")

    unresolved = [f for f in findings if f["class"] in UNRESOLVED]
    if args.gate and unresolved:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
