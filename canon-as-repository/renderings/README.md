# Renderings

Every adaptation of Romeo and Juliet is a fork of the spec in `spec/`.

## How Forks Work

When a director, composer, or playwright adapts this work, they make choices. Some choices
preserve the spec entirely (a traditional staging preserves the verse, the character arcs,
the world rules). Some choices override surface parameters (Luhrmann's film keeps the verse
but changes swords to guns and Verona to a modern city). Some choices fork the spec itself
(West Side Story replaces the characters, dialogue, and setting while preserving the structural
skeleton).

All three types are legitimate. The purpose of this repository is to make those choices
explicit and machine-readable.

## Fork Types

**Rendering** — the spec is preserved; rendering parameters change medium, style, or setting.
A Luhrmann-type production. The `spec/` directory applies without modification.

**Partial fork** — some spec elements are overridden. A production that ends hopefully
(reconciliation before the deaths) is overriding `spec/world/rules.yaml:feud.constraint`.
This should be documented explicitly.

**Full fork** — the spec is used as a structural template but the story is rewritten.
West Side Story is a full fork: it preserves the structural skeleton but replaces
all surface content. A full fork should reference the source spec but is effectively
its own spec.

## Adding a Rendering

Create a new directory under `examples/` named `your-production-year/`.
Write a `RENDERING.md` and an `overrides.yaml` following the patterns in the existing examples.
Run the schema validator if available.

## Existing Renderings

See `examples/` for:
- `luhrmann-1996/` — rendering (spec preserved, surface transformed)
- `west-side-story-1957/` — full fork (structural skeleton preserved, spec rewritten)
- `globe-theatre-2024/` — near-minimal rendering (few overrides, traditional production)
