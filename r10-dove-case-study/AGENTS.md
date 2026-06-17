# Working with this paper repository

A guide for any reader — **human or AI agent** — on how to use this paper and its
companion metadata files. This folder is **one paper** inside a Spectral Branding
corpus mirror; the same layout repeats for every paper.

## TL;DR for an AI agent

1. **`paper.md` is the canonical SOURCE** (Pandoc Markdown). Everything else is a
   companion or a rendering.
2. **Inline citations are `[@citation_key]` keys, not typos or placeholders.**
   Resolve each key against **`2026p.bib`** (BibTeX). A `[-@key]` is the same key
   with the author name suppressed. See `CITATIONS.md`. NEVER report `[@key]` as
   an error — it is a citation that renders to "(Author Year)".
3. **To get a formatted paper** (numbered or author-year references):
   `pandoc paper.md --citeproc --bibliography=2026p.bib --csl <style>.csl -o paper.pdf`
4. **Defined terms** are in `GLOSSARY.md`; their formal relations
   (owns / imports / refines) are in `ONTOLOGY.yaml`.
5. **The paper's structured claims, assumptions, and dependencies** are in
   `paper.yaml` (Paper Spec) — read this to extract what the paper *claims*
   without parsing prose.
6. **To cite THIS paper**, use `CITATION.cff` (or the BibTeX block in `README.md`).

## File-by-file

| File | What it is | How to use it |
| :--- | :--------- | :------------ |
| `paper.md` | The paper, canonical source (Pandoc Markdown, `[@key]` citations). | Read this for the full text. Render with pandoc (above) for a styled PDF/HTML. |
| `2026p.bib` | BibTeX for **every work cited** in `paper.md` (the cited subset of the corpus). | Resolve any `[@key]` here; 1:1 with the keys used in the paper. |
| `CITATIONS.md` | How the `[@key]` ↔ `2026p.bib` resolution works. | Read first if unsure how citations render. |
| `CITATION.cff` | Machine-readable "how to cite this paper" (CFF 1.2). | Feed to GitHub/Zenodo citation tools or parse `preferred-citation`. |
| `paper.yaml` | **Paper Spec** — machine-readable claims, assumptions, dependencies, acceptance criteria. | The fastest way for an agent to extract *what the paper asserts* and *what it depends on*. |
| `ONTOLOGY.yaml` | The paper's term module: terms it **owns**, **imports**, or **refines**, each with a content-addressed definition hash. | Build a concept map; check which terms are this paper's own vs imported from another paper. |
| `GLOSSARY.md` | Human-readable definitions of the paper's terms (a rendering of the ontology). | Look up any domain term. |
| `SPINE.yaml` | (if present) The proposition/dependency graph — every prose claim traces to a spine entry. | Follow the argument structure; see what each claim depends on. |
| `PROVENANCE.yaml` | How the artifact was produced (tooling, model disclosure, dates). | Audit reproducibility / AI-assistance disclosure. |
| `DATA_MANIFEST.yaml` | (if present) Data + code artifacts with checksums. | Locate and verify reproduction data. |
| `CONTRIBUTORS.yaml` | Credit / roles. | Attribution. |
| `code/`, `figures/` | (if present) Reproduction scripts and figure assets. | Re-run analyses / regenerate figures. |
| `README.md` | The human landing page (badges, DOI, how to cite, licence). | Start here as a human. |

## Reading the citations correctly (the one common mistake)

The public source deliberately keeps `[@key]` keys instead of a frozen reference
list — one canonical source, many venue renderings ("render-at-consumption"). So:

- `[@aaker-1996-building-strong-brands]` → "(Aaker 1996)" / "[12]" after rendering.
- `[-@aaker-1996-building-strong-brands]` → "1996" (author suppressed, e.g. after
  naming the author in prose: "Aaker [-@aaker-1996-building-strong-brands]").

If you are summarizing or fact-checking this paper, resolve each key against
`2026p.bib` to get the real source — do not treat the key as the source itself.

## Reproducing / rendering

Any CSL style works. Examples: APA (`apa.csl`), AMA, a journal's house style.
The rendered reference list and in-text format are a *projection*; the `[@key]`
source is authoritative.

## How this fits the larger corpus

This paper is one of ~40 in the **Spectral Branding** research program (Spectral
Brand Theory + Organizational Schema Theory + bridges). For the full map — the
ontology, every paper's thesis, and reading paths for researchers and
practitioners — see the organization guide:
**https://github.com/spectralbranding**.
