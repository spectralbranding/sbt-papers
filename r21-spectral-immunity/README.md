# R21: Spectral Immunity

**Spectral Immunity: Why Brand Portfolio Interference Disappears for AI Observers**

Citation key: `2026ac` | Supersedes: R8 (`2026q`) + R20 (`2026ab`)

## Summary

Brand portfolio theory predicts that corporate ownership generates perceptual interference when observers recognize shared parentage. This paper formalizes the interference mechanism across eight typed perception dimensions and tests it with 13 large language models from seven training traditions. Across 9,925 observations, 40 brands, and seven portfolio archetypes, portfolio framing produces near-zero perceptual change (mean |delta DCI| = .26, TOST equivalent for 18/20 brands). The awareness gate is necessary but not sufficient for interference; a perception channel with adequate bandwidth is also required.

This version incorporates Grok-review-recommended improvements: bandwidth constraint formalization grounded in rate-distortion theory (Cover and Thomas 2006) and rational inattention (Sims 2003; Matejka and McKay 2015); Peng et al. (2023) meta-analytic baseline framing (2,134 effect sizes) without fabricated magnitudes; expanded LLM-perception literature integration (Brand, Israeli and Ngwe 2023; Hermann and Puntoni 2025; Dubois, Dawson and Jaiswal 2025); and Appendix C with verbatim prompt templates for all four modalities plus a native-language example with back-translation.

## Key Finding

**Spectral immunity**: AI observers encode brand output (the WHAT layer) and discard organizational coordination context (the DO layer), including corporate ownership and portfolio membership.

## Files

| File | Description |
|------|-------------|
| `paper.md` | Full manuscript (markdown) |
| `paper.yaml` | Machine-readable paper specification |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTORS.yaml` | Contributor attribution |
| `DATA_MANIFEST.yaml` | Data sources and links |
| `PROVENANCE.yaml` | Fork history and submission records |

## Data

- **HuggingFace**: [spectralbranding/r20-portfolio-ai-perception](https://huggingface.co/datasets/spectralbranding/r20-portfolio-ai-perception) (9,925 observations)
- **Zenodo**: [10.5281/zenodo.19765401](https://doi.org/10.5281/zenodo.19765401)

## Target Venue

Marketing Science (INFORMS)

## Relationship to R8 and R20

This paper merges R8's theoretical framework (spectral interference formalism, awareness gate mechanism, portfolio archetypes) with R20's empirical data (9,925 observations across 40 brands and 13 models). R8 and R20 remain on Zenodo as historical records but are superseded by this merged paper.
