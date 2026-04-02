# Behavioral Metamerism Pilot — Summary Tables

**Category**: DTC supplements  
**Models**: simulated  
**Runs per condition**: 3

## Table 1: Behavioral Metamerism Index (BMI) by Brand Pair

| Brand Pair | BMI | Interpretation |
|-----------|-----|----------------|
| VitaCore vs NutraPure | 0.979 | HIGH metamerism |
| NutraPure vs RootWell | -0.000 | Low / anti-metamerism |
| VitaCore vs ApexStack | -0.000 | Low / anti-metamerism |
| VitaCore vs RootWell | -0.000 | Low / anti-metamerism |
| CleanDose vs RootWell | -0.000 | Low / anti-metamerism |
| NutraPure vs ApexStack | -0.000 | Low / anti-metamerism |
| FormulaRx vs ApexStack | -0.000 | Low / anti-metamerism |
| NutraPure vs CleanDose | -0.000 | Low / anti-metamerism |
| ApexStack vs RootWell | -0.000 | Low / anti-metamerism |
| VitaCore vs FormulaRx | -0.001 | Low / anti-metamerism |
| VitaCore vs CleanDose | -0.001 | Low / anti-metamerism |
| NutraPure vs FormulaRx | -0.001 | Low / anti-metamerism |
| CleanDose vs ApexStack | -0.001 | Low / anti-metamerism |
| FormulaRx vs RootWell | -0.001 | Low / anti-metamerism |
| FormulaRx vs CleanDose | -0.002 | Low / anti-metamerism |

## Table 2: Discrimination Results by Condition

| Model | Condition | Brand Pair | Can Distinguish | Confidence | Run |
|-------|-----------|-----------|----------------|-----------|-----|
| simulated | statistical | VitaCore vs NutraPure | No | 0.35 | 1 |
| simulated | augmented | VitaCore vs NutraPure | Yes | 0.92 | 1 |
| simulated | statistical | FormulaRx vs CleanDose | No | 0.40 | 1 |
| simulated | augmented | FormulaRx vs CleanDose | Yes | 0.88 | 1 |
| simulated | statistical | ApexStack vs RootWell | No | 0.38 | 1 |
| simulated | augmented | ApexStack vs RootWell | Yes | 0.95 | 1 |

## Table 3: Behavioral Prediction Accuracy

| Model | Condition | Brand | Scenario (abbrev) | Accuracy | Run |
|-------|-----------|-------|------------------|---------|-----|
| simulated | statistical | VitaCore | A customer receives a defective product and reques... | 0.40 | 1 |
| simulated | augmented | VitaCore | A customer receives a defective product and reques... | 0.95 | 1 |
| simulated | statistical | NutraPure | A customer receives a defective product and reques... | 0.30 | 1 |
| simulated | augmented | NutraPure | A customer receives a defective product and reques... | 0.92 | 1 |

## Table 4: Cross-Model Recommendation Variance

| Condition | Variance | Interpretation |
|-----------|---------|----------------|
| statistical | 0.1200 | Higher variance: models disagree |
| augmented | 0.0200 | Lower variance: specification aligns models |

## Table 5: Statistical Tests

| Test | Statistic | p-value | Significant |
|------|-----------|---------|-------------|
| Chi-square (discrimination rate) | -1.0 | N/A | N/A |
| Fisher's exact (discrimination rate) | — | 0.1000 | No |
| Wilcoxon signed-rank (confidence) | -1.0 | N/A | N/A |
| F-test (variance ratio) | 0.514 | 0.6786 | No |

**BMI 95% CI** (VitaCore_vs_NutraPure): [0.976, 0.982] (bootstrap, n=1000)

**Interpretation**: Discrimination rate difference not statistically significant (may need larger N). Wilcoxon not significant: confidence score shift inconclusive.
