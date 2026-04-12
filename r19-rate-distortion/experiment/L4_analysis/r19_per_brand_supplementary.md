# R19 Per-Brand R(D) Curves — Supplementary Analysis

**Status:** Exploratory (not pre-registered)
**Date:** 2026-04-12
**Source data:** `r19_per_cell.csv` — aggregated over 17 models × 3-5 reps per cell

---

## Method

For each brand × rate condition combination, mean distortion and standard deviation were computed by averaging across the per-model cell values. Standard deviations reflect between-model variation at a given (brand, rate) cell. The per-brand R(D) curves test whether the J-shape generalizes across the canonical SBT brand set or is brand-specific.

---

## Per-Brand R(D) Curves

Mean L1/2 total variation distance (averaged over 17 models), per brand × rate condition.

| Brand | R1 (26b) | R2 (19b) | R3 (13b) | R4 (8b) | R5 (3b) | Min |
|-------|---------|---------|---------|---------|---------|-----|
| Hermes | .144 | **.062** | .073 | .089 | .860 | R2 |
| IKEA | .167 | **.057** | .096 | .179 | .850 | R2 |
| Patagonia | .165 | **.055** | .083 | .133 | .838 | R2 |
| Tesla | .177 | **.138** | .139 | .291 | .882 | R2 |
| Erewhon | .184 | **.118** | .152 | .203 | .850 | R2 |

**R2 is the global minimum for all 5 brands (5/5).** The J-shape is universal across the canonical brand set, mirroring the universal J-shape across the 17-model panel.

---

## J-Shape Drop by Brand (R1 → R2 trough)

| Brand | D(R1) | D(R2) | Absolute drop | % drop |
|-------|-------|-------|--------------|--------|
| Patagonia | .165 | .055 | .110 | 66.7% |
| IKEA | .167 | .057 | .110 | 65.9% |
| Hermes | .144 | .062 | .082 | 56.9% |
| Erewhon | .184 | .118 | .066 | 35.9% |
| Tesla | .177 | .138 | .039 | 22.0% |

Patagonia shows the steepest proportional drop (66.7% reduction from R1 to R2 trough), followed closely by IKEA (65.9%) and Hermes (56.9%). Tesla shows the shallowest drop (22.0%), reflecting the difficulty AI models have encoding Tesla's anomalously low Ideological canonical value (3.0 / 10) at any format granularity. The Erewhon drop (35.9%) is intermediate.

---

## Lowest R2 Distortion (Best Canonical-Profile Alignment)

| Rank | Brand | D(R2) |
|------|-------|-------|
| 1 | Patagonia | .055 |
| 2 | IKEA | .057 |
| 3 | Hermes | .062 |
| 4 | Erewhon | .118 |
| 5 | Tesla | .138 |

Patagonia achieves the lowest absolute distortion at R2 (.055), meaning the 1-5 scale format produces the closest alignment to the canonical Patagonia spectral profile of any brand-format combination tested. Hermes and IKEA are essentially tied (.057 / .062). Tesla and Erewhon are substantially higher.

---

## Implication for Canonical-Profile Alignment

The 1-5 scale (R2, ~19 bits) consistently outperforms the 100-point free allocation (R1, ~26 bits) for all five brands, generalizing the universal J-shape finding across the canonical brand set. The bounded ordinal format suppresses encoder bias more effectively than the unconstrained allocation, regardless of which brand is being measured.

Brand-specific patterns:

1. **Patagonia, IKEA, Hermes** — well-known brands with rich training data and clear dimensional structure. Show the cleanest J-shapes and the lowest R2 distortion (~.055-.062). The encoder can recover their canonical profiles with high fidelity at the bounded format.
2. **Erewhon** — boutique premium brand with sparse training data. Higher distortion across all rate conditions (~.118 at R2), suggesting the encoder has less reliable internal representation.
3. **Tesla** — anomalously low Ideological canonical value (3.0) creates systematic difficulty. The binary R4 format produces extreme distortion (.291) because Yes/No quantization cannot represent the unusual dimensional asymmetry. The J-shape still holds (R2 is min) but the curve is shallower.

---

## Tesla as a Limiting Case

Tesla's R(D) curve is the most informative for understanding the J-shape mechanism. With canonical Ideological = 3.0 (lowest of the five brands), the encoder must distinguish "very low" from "low" from "moderate" on this dimension — a discrimination that's hard to encode in any quantized format. R1 gives the encoder freedom to express its own (often higher) ideological estimate; R2-R3 constrain the output to bounded scales; R4 forces a binary that often misclassifies; R5 collapses to a single dimension that can never be Ideological for Tesla.

The result: Tesla has the smallest J-shape drop (22.0%) and the highest R2 absolute distortion (.138). The encoder is doing something close to its best at R2, but its best is constrained by Tesla's unusual canonical structure.

---

## Cross-Brand Pattern

The five-brand J-shape pattern is robust: every brand achieves minimum distortion at R2 (1-5 scale, 19 bits), regardless of canonical profile structure. The bounded ordinal format is the universal sweet spot for AI brand-perception encoders, across both the model dimension (17 architectures) and the brand dimension (5 canonical SBT references).
