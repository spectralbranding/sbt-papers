# Run 11 — Roshen Multi-City Framing Results

**Generated:** 2026-04-11T14:11:06.522695+00:00

## Design

Roshen evaluated as a same-brand framing experiment across 7 cities,
in English plus the local national language(s). Astana receives both
Kazakh and Russian native conditions; all other non-English cities
receive one native condition. Same prompt template, same model panel,
differing only in city name and prompt language.

## Cross-model mean DCI by (city, language)

DCI = w_economic + w_semiotic, normalised so the uniform baseline = 25.0.
Higher DCI = more dimensional collapse toward Economic + Semiotic.

| City     | Operational status | en DCI | native DCI (lang) | Δ (native − en) |
|----------|--------------------|-------:|------------------:|----------------:|
| Moscow | Lipetsk factory nationalized 2024 (defunct) | 44.238 | 38.0 (ru) | -6.238 (ru) |
| Kyiv | Home market; founded 1996; multiple Kyiv factories | 34.778 | 35.0 (uk) | +0.222 (uk) |
| Vilnius | Klaipėda factory ~15,500 t/yr (largest non-Ukraine operation) | 42.666 | 37.524 (lt) | -5.142 (lt) |
| Warsaw | No factory or official distributor; informal export market | 39.0 | 35.69 (pl) | -3.310 (pl) |
| Astana | Sales representative office in Almaty; no manufacturing | 43.881 | 34.667 (kk); 37.715 (ru) | -9.214 (kk); -6.166 (ru) |
| Tbilisi | Roshen Georgia distributor (Tbilisi); no manufacturing | 42.572 | 37.715 (ka) | -4.857 (ka) |
| Baku | Shops/distributors in Khirdalan; no manufacturing | 44.523 | 36.524 (az) | -7.999 (az) |

## Cross-model mean profile per (city, language)

| City | Lang | Sem | Nar | Ide | Exp | Soc | Eco | Cul | Tem | DCI |
|------|------|----:|----:|----:|----:|----:|----:|----:|----:|----:|
| Moscow | en | 17.8 | 7.3 | 6.7 | 12.8 | 9.8 | 26.4 | 12.2 | 8.4 | 44.238 |
| Moscow | ru | 14.7 | 8.0 | 7.4 | 15.8 | 8.8 | 23.3 | 12.2 | 10.3 | 38.000 |
| Kyiv | en | 15.1 | 7.1 | 11.1 | 11.8 | 11.3 | 19.7 | 16.6 | 8.6 | 34.778 |
| Kyiv | uk | 14.4 | 7.6 | 10.8 | 13.0 | 12.8 | 20.6 | 14.5 | 6.9 | 35.000 |
| Vilnius | en | 18.6 | 7.5 | 8.7 | 13.7 | 9.4 | 24.1 | 11.1 | 7.4 | 42.666 |
| Vilnius | lt | 14.7 | 7.7 | 9.9 | 16.0 | 10.4 | 22.9 | 11.0 | 8.6 | 37.524 |
| Warsaw | en | 17.0 | 8.8 | 9.7 | 11.6 | 10.8 | 22.0 | 13.4 | 7.2 | 39.000 |
| Warsaw | pl | 14.1 | 7.2 | 8.6 | 16.7 | 10.5 | 21.6 | 10.1 | 10.9 | 35.690 |
| Astana | en | 19.7 | 7.6 | 7.7 | 12.7 | 11.9 | 24.2 | 9.7 | 8.0 | 43.881 |
| Astana | kk | 15.3 | 9.2 | 9.7 | 20.6 | 11.2 | 19.4 | 8.2 | 6.6 | 34.667 |
| Astana | ru | 14.9 | 7.2 | 7.3 | 17.4 | 10.3 | 22.8 | 11.0 | 9.5 | 37.715 |
| Tbilisi | en | 18.8 | 7.5 | 7.3 | 13.0 | 10.4 | 23.8 | 11.5 | 8.3 | 42.572 |
| Tbilisi | ka | 14.4 | 7.4 | 7.2 | 19.5 | 12.0 | 23.3 | 9.8 | 7.3 | 37.715 |
| Baku | en | 18.8 | 8.1 | 6.0 | 14.0 | 10.3 | 25.7 | 10.6 | 7.4 | 44.523 |
| Baku | az | 17.2 | 8.8 | 8.3 | 18.6 | 12.5 | 19.3 | 8.8 | 7.0 | 36.524 |

## Variable separation

The 7-city design enables three contrasts that the original 2-city
Moscow/Kyiv test could not separate:

1. **Operational anchor** (Vilnius vs Warsaw): both EU/NATO and
   Ukraine-aligned, but only Vilnius has the Klaipėda factory.
   If Vilnius < Warsaw on collapse, AI uses operational reality.

2. **Discourse density** (Kyiv vs all others): home market vs
   foreign markets. The expected baseline is Kyiv = lowest collapse.

3. **Geopolitical alignment** (Moscow vs Astana/Tbilisi/Baku):
   conflict-hostile vs post-USSR neutral. Tests whether the
   Moscow effect is alignment-specific or generic foreign-context.

Per-contrast verdicts (populate after reviewing the deltas above):

- **Operational anchor effect**: 
- **Native language H10 × H12 interaction**: 
- **Conflict vs neutrality contrast**: 
- **Astana kk vs ru contrast**: 
