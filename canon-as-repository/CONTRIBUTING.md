# Contributing

This repository welcomes new renderings. A rendering is any production, adaptation,
or fork of Romeo and Juliet — or, more broadly, any creative work that adapts a canonical
source. The purpose is not completeness; it is demonstration of the architecture.

## How to Add a Rendering

### 1. Fork this repository

Create your own copy. You can submit a pull request when you are done if you want your
rendering listed here, but forking for your own use is the primary intended workflow.

### 2. Create your rendering directory

```
examples/your-production-year/
```

Use lowercase, hyphens, no spaces. Include the year. Examples:
- `examples/zeffirelli-1968/`
- `examples/taylor-swift-eras-tour-2025/`  (hypothetical)
- `examples/animated-film-2003/`

### 3. Write RENDERING.md

Your `RENDERING.md` should address:

- **Rendering type**: Is this a rendering (spec preserved, surface transformed), a partial fork
  (some spec elements modified), or a full fork (structural skeleton preserved, spec rewritten)?
- **Rendering parameters**: A table of the key choices made (medium, setting, dialogue, cast).
- **Spec compliance**: A table showing which spec elements are preserved, modified, or replaced.
  Check against `spec/characters/`, `spec/world/`, `spec/themes/`, and `spec/constraints/`.
- **Specification gap analysis**: What choices did this rendering make that the spec does not
  address? What did the rendering add that was not in the spec?

The analysis section is the most valuable part. A list of overrides without analysis is less
useful than a clear account of why the choices were made and what structural functions they serve.

### 4. Write overrides.yaml

Your `overrides.yaml` should be machine-readable. Follow the pattern in the existing examples:

```yaml
rendering:
  title: "..."
  year: YYYY
  medium: film | stage | musical | television | opera | ballet | other

  setting_overrides: ...
  dialogue_overrides: ...

  spec_compliance:
    characters: preserved | modified | replaced
    dialogue: preserved | modified | replaced
    world_rules: preserved | modified | replaced
    timeline: preserved | modified | replaced
    themes: preserved | modified | replaced

  overrides_requiring_documentation:
    - field: spec.path.to.field
      spec_value: "what the spec says"
      fork_value: "what you did instead"
      rationale: "why"
```

Any spec constraint that is not preserved must appear in `overrides_requiring_documentation`.
This is not a requirement for approval — it is a requirement for honest accounting.

### 5. Validate (optional)

If a validator is available, run it against your files. Schema definitions are in `schema/`.
A rendering that fails validation is not disqualified; it may be documenting an intentional
spec override, which is fine. The validator identifies what needs documentation.

### 6. Submit a pull request

If you want your rendering listed in the main README, submit a pull request with:
- Your `examples/your-production-year/` directory
- A one-line addition to the "Examples" section of the README

Pull requests are reviewed for:
- Clear documentation of spec compliance and overrides
- Honest accounting of choices (not claims of "total fidelity" that are not supported)
- Formatting consistency with existing examples

## What We Are Not Looking For

- Comprehensive catalogues of every Romeo and Juliet production in history
- Productions added without RENDERING.md analysis
- Renderings of works other than Romeo and Juliet (this repo is scoped to one source work)

## The Larger Project

This directory is a demo for the canon-as-repository architecture: the idea that creative IP is a
specification, and every rendering is a fork. If you want to apply this architecture to a
different canonical work, copy the directory and replace the spec files. The schema
and the RENDERING.md/overrides.yaml pattern are designed to be reusable.

The formal treatment of the underlying architecture is available at
[spectralbranding.com](https://spectralbranding.com). The companion research paper is at
https://github.com/spectralbranding/sbt-papers/tree/main/canon-as-repository.
