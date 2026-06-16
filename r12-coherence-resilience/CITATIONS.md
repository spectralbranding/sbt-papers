# Resolving citations in `paper.md`

`paper.md` is the **source** artifact. Inline citations use the
Pandoc-Markdown `[@citation_key]` form (a stable, machine-readable key per
cited work). The full bibliographic record for every key lives in the
companion `2026s.bib` (BibTeX), committed alongside this file.

To render the paper with a formatted reference list in any venue style:

```bash
pandoc paper.md --citeproc --bibliography=2026s.bib \
  --csl <your-style>.csl -o paper.pdf
```

The rendered numbered / (Author Year) reference list is a **rendering**, not
part of the source. Machines should resolve `[@key]` against `2026s.bib`
directly. (Render-at-consumption: one canonical source, many venue renders.)
