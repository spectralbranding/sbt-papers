---
license: cc-by-nc-nd-4.0
task_categories:
  - text-generation
language:
  - en
  - zh
  - ru
  - ja
  - ko
  - ar
  - hi
  - es
tags:
  - brand-perception
  - spectral-brand-theory
  - measurement-invariance
  - cross-language
pretty_name: "Experiment B: Cross-Language Semantic Drift in Brand Perception"
size_categories:
  - n<1K
---

# Experiment B: Cross-Language Semantic Drift in Brand Perception

## Summary

Tests whether SBT dimension labels carry the same meaning across 8 languages by comparing bilingual-anchored labels (control) vs native-only labels (test). 450 API calls across 3 LLMs (Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash).

## Key Findings

- **H1 (Configural Invariance) SUPPORTED**: Median cosine = .992, min = .966 across all language pairs under bilingual anchoring. The 8 dimensions carry equivalent meaning when English anchors are present.
- **H2 (Native-Only Drift) NOT SUPPORTED**: 0/7 languages showed significant drift at Bonferroni-corrected alpha. Removing English anchors produces small (~1-2pp) but non-significant shifts.
- **H3 (Cultural Drift Directions) NOT SUPPORTED**: Arabic Ideological (+1.38pp, p=.278), Japanese Cultural (-1.39pp, wrong direction), Hindi Economic (+0.81pp, p=.581). Trends present but underpowered.
- **H4 (Collectivist Social) NOT SUPPORTED**: Collectivist (12.14) vs individualist (12.10), d=.009. No meaningful difference.
- **EXPLORATORY**: All 7 languages show consistent Experiential deflation (-2.0 to -4.5pp) and Economic/Narrative inflation when English anchors are removed. This universal pattern suggests bilingual labels inflate Experiential through the English word's broader semantic scope.

## Dataset Structure

    data/exp_cross_language.jsonl     # 450 records
    prompts/
      system_prompts.json
      brand_profiles.json
      dimension_translations.json
    analysis/
      exp_cross_language_results.json
      exp_cross_language_summary.md
    protocol/
      PROTOCOL.md
      experiment_config.yaml

## Citation

    Zharnikov, D. (2026). Spectral Metamerism in AI-Mediated Brand Perception.

## License

CC-BY-NC-ND-4.0
