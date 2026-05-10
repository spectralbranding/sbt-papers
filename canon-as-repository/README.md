# Canon as Repository: Version-Controlled Specification for Creative IP

Creative IP is a specification. Every rendering is a fork.

This repository demonstrates that architecture using Shakespeare's Romeo and Juliet. The play's canonical form — its characters, world rules, themes, and constraints — lives in `spec/`. Every production, adaptation, and reimagining is a fork of that spec: a set of rendering decisions layered on top of a shared foundation. Some renderings preserve the spec almost entirely (a traditional Globe production). Others transform it so deeply they become a new spec with the same skeleton (West Side Story).

The argument is structural, not metaphorical. A specification defines what must be preserved across instantiations. A rendering defines how. Git's branching model maps cleanly onto how IP actually works: the canon is the main branch; every adaptation is a fork; every revision to the canon is a commit; every edition is a tag.

This repository is the proof-of-concept companion to:

> Zharnikov, D. (2026w). Canon as repository: A specification-driven architecture for transmedia intellectual property. *Working Paper v1.1.0.* https://doi.org/10.5281/zenodo.19355800

---

## How It Works

### `spec/` — The Canon

The spec directory contains the canonical definition of the work: character arcs, world rules, thematic constraints, and tone requirements. These are the elements that must be preserved (or explicitly overridden) in any rendering.

- `spec/characters/` — one file per character; defines traits, arc, relationships, constraints, and speech register
- `spec/world/` — world rules, locations, timeline
- `spec/themes/` — central and secondary thematic structure
- `spec/constraints/` — cross-cutting constraints (tone, register, structural requirements)

### `examples/` — Rendering Forks

Each subdirectory under `examples/` represents a specific production or adaptation. Every rendering contains:

- `RENDERING.md` — prose description of the adaptation's choices and spec compliance
- `overrides.yaml` — machine-readable rendering parameters: what was changed, what was preserved

### `schema/` — Validation

JSON Schema-style definitions for character and world files. A validator can check that any spec file conforms to the schema and that any rendering's overrides reference valid spec fields.

---

## The Spec/Rendering Distinction

| Belongs in `spec/`                          | Belongs in `overrides.yaml`               |
|---------------------------------------------|-------------------------------------------|
| Character arc (what happens to them)        | Casting (who plays them)                  |
| Relationship dynamics                       | Visual style, costume, set design         |
| World rules (feud is structural, non-negotiable) | Setting period or location              |
| Thematic structure                          | Medium (stage, film, musical)             |
| Tone shift (comedy to tragedy at Act 3.1)   | Soundtrack or musical language            |
| Constraint: Romeo's death must be voluntary | Whether guns or swords are used           |
| Timeline (the compressed 4-5 days)          | Pacing and runtime                        |

The spec captures structural necessity. The rendering captures contingent choices. A constraint in the spec is a constraint on all forks: you can change the setting to New York, but Tony must still die by his own choice.

---

## Git Semantics for IP

| Git operation         | IP operation                                              |
|-----------------------|-----------------------------------------------------------|
| Commit                | Revision to the canon (Shakespeare edits Act 3)           |
| Tag                   | Edition (First Folio 1623, Arden Third Edition 2012)      |
| Fork                  | Adaptation (West Side Story, Luhrmann's film)             |
| Branch                | Variant in development (a director's working draft)       |
| Pull request          | Proposed canon change (submitted for scholarly consensus) |
| CI / schema check     | Consistency validation (does this rendering break a spec constraint?) |
| Diff                  | What changed between two productions                      |
| Merge conflict        | Irreconcilable interpretive disagreement                  |

---

## Quick Start

Fork the sbt-papers repository (or this folder). Create a new directory under `examples/` named `your-production-year/`. Write a `RENDERING.md` describing your adaptation and what spec elements you preserved, modified, or overrode. Add an `overrides.yaml` with your rendering parameters using the schema in `schema/`.

---

## Three Examples

This repository includes three renderings that illustrate the spectrum of spec compliance:

**Baz Luhrmann's Romeo + Juliet (1996)** — a rendering that preserves Shakespeare's verse and character arcs while overriding the setting (modern Verona Beach), weapons (guns branded as swords), and visual language (postmodern baroque). The spec is almost entirely intact; the rendering is transformed.

**West Side Story (1957)** — a transformative fork. Bernstein, Sondheim, and Robbins did not render Romeo and Juliet; they forked the spec. Romeo becomes Tony, Juliet becomes Maria, the feud becomes ethnic conflict. The character names, dialogue, and setting are all overridden. What is preserved is the structural skeleton: love across enmity, a catalyst death, a tragic ending that exposes the feud's cost.

**Globe Theatre (2024)** — a traditional period production. Minimal overrides, Elizabethan staging, original verse. This example demonstrates that a rendering with few overrides is not "more faithful" — it is simply a rendering with fewer parameters changed. Every production, including the most traditional, makes rendering choices not specified in the spec.

---

## Connection to the Rendering Problem

This demo is part of a research program studying the structural gap between specification and rendering across domains — from brand identity to scientific publishing to organizational design. The same architecture (spec → rendering → perception) applies wherever a source structure must be instantiated in a medium it was not designed for.

The formal treatment is available at [spectralbranding.com](https://spectralbranding.com). The working paper "The Rendering Problem: Why Specifications Survive Their Instantiations" is available on Zenodo (DOI: 10.5281/zenodo.19064427).

---

## Cite this Repository

```bibtex
@article{zharnikov2026w,
  title={Canon as repository: A specification-driven architecture for transmedia intellectual property},
  author={Zharnikov, Dmitry},
  year={2026},
  url={https://doi.org/10.5281/zenodo.19355800},
  doi={10.5281/zenodo.19355800}
}
```

---

## Author

Dmitry Zharnikov

## License

MIT — see `LICENSE`
