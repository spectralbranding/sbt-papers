"""Link every paper's ONTOLOGY.yaml module into the substrate `terms` graph.

This is the ontology counterpart of sync_claims_from_spine.py (SPINE.yaml ->
claims) and the citations graph (references -> citations). It implements the
modular ontology system locked 2026-06-13 in
the spine-first drafting protocol §"The per-paper metadata bundle":

  modular authoring + link-time compatibility, ONE owning module per term.

Each paper owns an ONTOLOGY.yaml module that `owns` the terms it introduces,
`imports` terms owned by other modules (reference only), and may `refines` an
imported term (an explicit, compatible narrowing). A *linker* (this script)
composes all modules and ENFORCES compatibility before writing:

  * unique owner       -- each term_key is owned by exactly one module
  * no dangling        -- every import / refine / relation target resolves to
                          some module's `owns`
  * compatible refine  -- a refines must carry a narrows_to/note (no silent
                          contradictory redefinition)
  * acyclic            -- no cycle in narrows / specializes term relations

The substrate `terms` graph is the COMPILED OUTPUT of that link, not a
hand-authored file. The per-paper glossary (render_paper_glossary.py) is a
RENDERED projection of it. So "modular authoring" and "centralized storage"
coexist: modules are the source, the substrate is the build artifact.

Per the protocol's mechanism verdicts (§"More sophisticated mechanisms"):
  * the link-check is DB-enforced (FK / UNIQUE / CHECK) where possible, plus
    these explicit compatibility passes;
  * each definition carries a content-addressed `def_hash` (sha256) so a
    changed definition surfaces every dependent for re-validation.

NON-DESTRUCTIVE: this script only CREATEs the three ontology tables if missing
and rewrites their rows. It never touches the citations / claims graph, so it
is safe on the live DB (unlike init_substrate.py).

Module discovery: the live ontology modules  +  research/**/ONTOLOGY.yaml
The `paper_key` declared INSIDE each module is authoritative (not the path).

Run:  uv run python tools/build_ontology.py            # dry-run
      uv run python tools/build_ontology.py --apply
      uv run python tools/build_ontology.py --strict   # warnings -> errors
"""

from __future__ import annotations

import argparse
import hashlib
import sqlite3
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
DB = REPO / "research" / "corpus_substrate.sqlite"

REL_TYPES = ("synonym", "narrows", "specializes", "contrasts", "replaces", "maps_to")
ROLE_TYPES = ("owns", "imports", "refines")

# Non-destructive DDL (mirrors init_substrate.py; IF NOT EXISTS so the live
# citations/claims graph is never dropped).
DDL = """
CREATE TABLE IF NOT EXISTS terms (
    term_key TEXT PRIMARY KEY,
    canonical_label TEXT,
    definition TEXT,
    canonical_form TEXT,
    status TEXT,
    owner_paper_key TEXT REFERENCES papers(paper_key),
    replaces TEXT,
    def_hash TEXT
);
CREATE TABLE IF NOT EXISTS term_relations (
    source_term_key TEXT REFERENCES terms(term_key) ON DELETE CASCADE,
    target_term_key TEXT REFERENCES terms(term_key) ON DELETE CASCADE,
    relation_type TEXT NOT NULL CHECK (relation_type IN (
        'synonym', 'narrows', 'specializes', 'contrasts', 'replaces', 'maps_to'
    )),
    note TEXT,
    PRIMARY KEY (source_term_key, target_term_key, relation_type)
);
CREATE TABLE IF NOT EXISTS paper_terms (
    paper_key TEXT REFERENCES papers(paper_key) ON DELETE CASCADE,
    term_key TEXT REFERENCES terms(term_key) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('owns', 'imports', 'refines')),
    local_definition TEXT,
    section_path TEXT,
    PRIMARY KEY (paper_key, term_key, role)
);
CREATE INDEX IF NOT EXISTS idx_term_relations_source ON term_relations(source_term_key);
CREATE INDEX IF NOT EXISTS idx_paper_terms_term ON paper_terms(term_key);
"""


def def_hash(definition: str) -> str:
    """Content-addressed identity for a definition (per protocol ADOPT verdict)."""
    return hashlib.sha256((definition or "").strip().encode("utf-8")).hexdigest()[:16]


def discover_modules() -> list[Path]:
    paths: set[Path] = set()
    paths.update((REPO / "research" / "ontology").glob("*.yaml"))
    paths.update(REPO.glob("research/**/ONTOLOGY.yaml"))
    # Per-paper modules are lowercase paper-key filenames (e.g. 2026a.yaml,
    # foam-bridge-note.yaml). UPPERCASE-stem YAMLs in the live ontology directory  are
    # non-module docs/SSOTs (e.g. STANDARDS_CROSSWALK.yaml -- the standards
    # vocabulary crosswalk) and are not ontology modules.
    return sorted(
        p for p in paths if p.stem != p.stem.upper() or p.name == "ONTOLOGY.yaml"
    )


class Module:
    """One paper's parsed ONTOLOGY.yaml module."""

    def __init__(self, path: Path, data: dict):
        self.path = path
        self.paper_key = data.get("paper_key")
        self.schema_version = data.get("schema_version")
        self.owns = data.get("owns") or []
        self.imports = data.get("imports") or []
        self.refines = data.get("refines") or []

    @property
    def rel(self) -> str:
        return str(self.path.relative_to(REPO))


def parse_modules(paths: list[Path]) -> tuple[list[Module], list[str]]:
    mods: list[Module] = []
    errors: list[str] = []
    for p in paths:
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:  # pragma: no cover - surfaced to user
            errors.append(f"{p.relative_to(REPO)}: YAML parse error: {e}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{p.relative_to(REPO)}: top level is not a mapping")
            continue
        if not data.get("paper_key"):
            errors.append(f"{p.relative_to(REPO)}: missing paper_key")
            continue
        mods.append(Module(p, data))
    return mods, errors


def _norm_ref(entry) -> dict:
    """Normalize an imports/refines entry to a dict with term_key."""
    if isinstance(entry, str):
        return {"term_key": entry}
    if isinstance(entry, dict):
        return entry
    return {}


def link(mods: list[Module]) -> tuple[dict, list[str], list[str]]:
    """Compose modules into the linked graph and run compatibility checks.

    Returns (graph, errors, warnings).
    graph = {
      "terms": {term_key: {row..., owner, relations: [(src,dst,type,note)]}},
      "paper_terms": [(paper_key, term_key, role, local_definition, section_path)],
      "relations": [(src, dst, rel_type, note)],
    }
    """
    errors: list[str] = []
    warnings: list[str] = []

    # ---- pass 1: collect owners (unique-owner check) ----
    owners: dict[str, str] = {}  # term_key -> paper_key
    term_rows: dict[str, dict] = {}
    relations: list[tuple[str, str, str, str]] = []
    paper_terms: list[tuple] = []

    for m in mods:
        for o in m.owns:
            if not isinstance(o, dict) or not o.get("term_key"):
                errors.append(f"{m.rel}: owns entry missing term_key: {o!r}")
                continue
            tk = o["term_key"]
            if tk in owners:
                errors.append(
                    f"COLLISION: term '{tk}' owned by both {owners[tk]} "
                    f"({m.paper_key} in {m.rel}) -- a term has exactly one owner"
                )
                continue
            owners[tk] = m.paper_key
            definition = (o.get("definition") or "").strip()
            if not definition:
                warnings.append(f"{m.rel}: term '{tk}' has empty definition")
            term_rows[tk] = {
                "term_key": tk,
                "canonical_label": o.get("label") or tk,
                "definition": definition,
                "canonical_form": o.get("canonical_form") or o.get("label") or tk,
                "status": o.get("status") or "active",
                "owner_paper_key": m.paper_key,
                "replaces": "; ".join(o.get("replaces") or []) or None,
                "def_hash": def_hash(definition),
            }
            paper_terms.append((m.paper_key, tk, "owns", None, o.get("first_section")))
            # owns-level relations (term -> term)
            for r in o.get("relations") or []:
                if not isinstance(r, dict):
                    continue
                rt = r.get("type")
                dst = r.get("term_key")
                if rt not in REL_TYPES:
                    errors.append(
                        f"{m.rel}: term '{tk}' relation type '{rt}' not in {REL_TYPES}"
                    )
                    continue
                if not dst:
                    errors.append(
                        f"{m.rel}: term '{tk}' {rt} relation missing term_key"
                    )
                    continue
                relations.append((tk, dst, rt, r.get("note")))

    # ---- pass 2: imports / refines (no-dangling + compatible-refine) ----
    for m in mods:
        for imp in m.imports:
            ref = _norm_ref(imp)
            tk = ref.get("term_key")
            if not tk:
                errors.append(f"{m.rel}: imports entry missing term_key: {imp!r}")
                continue
            if tk not in owners:
                errors.append(
                    f"DANGLING IMPORT: {m.paper_key} imports '{tk}' but no module owns it"
                )
                continue
            if owners[tk] == m.paper_key:
                warnings.append(
                    f"{m.rel}: {m.paper_key} imports '{tk}' which it also owns (redundant)"
                )
            paper_terms.append(
                (m.paper_key, tk, "imports", None, ref.get("section_path"))
            )
        for rf in m.refines:
            ref = _norm_ref(rf)
            tk = ref.get("term_key")
            if not tk:
                errors.append(f"{m.rel}: refines entry missing term_key: {rf!r}")
                continue
            if tk not in owners:
                errors.append(
                    f"DANGLING REFINE: {m.paper_key} refines '{tk}' but no module owns it"
                )
                continue
            narrows_to = ref.get("narrows_to") or ref.get("note")
            if not narrows_to:
                errors.append(
                    f"INCOMPATIBLE REFINE: {m.paper_key} refines '{tk}' without a "
                    f"narrows_to/note (refinement must be an explicit narrowing)"
                )
                continue
            paper_terms.append(
                (m.paper_key, tk, "refines", str(narrows_to), ref.get("section_path"))
            )

    # ---- pass 3: relation targets resolve (no-dangling) ----
    for src, dst, rt, _note in relations:
        if dst not in owners:
            errors.append(
                f"DANGLING RELATION: '{src}' {rt} '{dst}' but no module owns '{dst}'"
            )

    # ---- pass 4: acyclicity over narrows / specializes ----
    hierarchy: dict[str, list[str]] = {}
    for src, dst, rt, _note in relations:
        if rt in ("narrows", "specializes") and dst in owners and src in owners:
            hierarchy.setdefault(src, []).append(dst)
    cyc = _find_cycle(hierarchy)
    if cyc:
        errors.append("CYCLE in narrows/specializes relations: " + " -> ".join(cyc))

    graph = {
        "terms": term_rows,
        "paper_terms": paper_terms,
        "relations": relations,
        "owners": owners,
    }
    return graph, errors, warnings


def _find_cycle(adj: dict[str, list[str]]) -> list[str]:
    """Return one cycle as a node list, or [] if acyclic (DFS)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {}
    stack: list[str] = []

    def dfs(node: str) -> list[str]:
        color[node] = GRAY
        stack.append(node)
        for nxt in adj.get(node, []):
            c = color.get(nxt, WHITE)
            if c == GRAY:
                idx = stack.index(nxt)
                return stack[idx:] + [nxt]
            if c == WHITE:
                r = dfs(nxt)
                if r:
                    return r
        stack.pop()
        color[node] = BLACK
        return []

    for n in list(adj):
        if color.get(n, WHITE) == WHITE:
            r = dfs(n)
            if r:
                return r
    return []


def write_graph(con: sqlite3.Connection, graph: dict) -> None:
    # Full recompile: DROP+CREATE the three ontology tables (child->parent order)
    # so any CHECK/column change in DDL takes effect (CREATE IF NOT EXISTS alone
    # cannot alter an existing table's CHECK -- e.g. adding the 'maps_to' edge
    # type). Only the ontology tables are touched; the citations/claims graph is
    # never referenced, so this stays non-destructive.
    con.execute("DROP TABLE IF EXISTS paper_terms")
    con.execute("DROP TABLE IF EXISTS term_relations")
    con.execute("DROP TABLE IF EXISTS terms")
    con.executescript(DDL)
    # register papers if missing (FK safety for owner_paper_key)
    paper_keys = {row["owner_paper_key"] for row in graph["terms"].values()}
    paper_keys |= {pt[0] for pt in graph["paper_terms"]}
    for pk in sorted(paper_keys):
        con.execute("INSERT OR IGNORE INTO papers (paper_key) VALUES (?)", (pk,))
    for row in graph["terms"].values():
        con.execute(
            "INSERT INTO terms (term_key, canonical_label, definition, "
            "canonical_form, status, owner_paper_key, replaces, def_hash) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (
                row["term_key"],
                row["canonical_label"],
                row["definition"],
                row["canonical_form"],
                row["status"],
                row["owner_paper_key"],
                row["replaces"],
                row["def_hash"],
            ),
        )
    for src, dst, rt, note in graph["relations"]:
        con.execute(
            "INSERT OR IGNORE INTO term_relations "
            "(source_term_key, target_term_key, relation_type, note) "
            "VALUES (?,?,?,?)",
            (src, dst, rt, note),
        )
    for pt in graph["paper_terms"]:
        con.execute(
            "INSERT OR IGNORE INTO paper_terms "
            "(paper_key, term_key, role, local_definition, section_path) "
            "VALUES (?,?,?,?,?)",
            pt,
        )
    con.commit()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="Write to the substrate")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = ap.parse_args()

    paths = discover_modules()
    print(f"ONTOLOGY modules: {len(paths)}")
    for p in paths:
        print(f"  {p.relative_to(REPO)}")
    mods, parse_errors = parse_modules(paths)

    graph, errors, warnings = link(mods)
    errors = parse_errors + errors

    n_terms = len(graph["terms"])
    n_rel = len(graph["relations"])
    n_pt = len(graph["paper_terms"])
    by_role: dict[str, int] = {}
    for pt in graph["paper_terms"]:
        by_role[pt[2]] = by_role.get(pt[2], 0) + 1
    print(
        f"\nLINKED GRAPH: {n_terms} terms, {n_rel} relations, "
        f"{n_pt} paper_terms {dict(sorted(by_role.items()))}"
    )

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  [warn] {w}")
    if args.strict:
        errors += warnings

    if errors:
        print(f"\nCOMPATIBILITY ERRORS ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(f"  [ERROR] {e}", file=sys.stderr)
        print(
            "\nLink FAILED. The substrate was not written. Fix the modules above.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    print(
        "\nCompatibility: OK (unique owner / no dangling / compatible refine / acyclic)"
    )

    if not args.apply:
        print("\n[DRY-RUN] re-run with --apply to write the substrate.")
        return

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    write_graph(con, graph)
    print(
        f"\n[APPLIED] terms={con.execute('select count(*) from terms').fetchone()[0]} "
        f"term_relations={con.execute('select count(*) from term_relations').fetchone()[0]} "
        f"paper_terms={con.execute('select count(*) from paper_terms').fetchone()[0]}"
    )
    con.close()
    print(
        "Regenerate the .sql mirror: uv run python research/code/sync_substrate.py --sql-only"
    )


if __name__ == "__main__":
    main()
