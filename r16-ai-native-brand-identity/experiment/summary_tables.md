# Behavioral Metamerism Pilot — Summary Tables

## Table 0: Experiment Metadata

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-03 |
| Category | DTC supplements |
| Models | claude, gpt, gemini, deepseek, qwen3_local, gemma4_local |
| Runs per condition | 3 |
| Total discrimination calls | 540 |
| Total prediction calls | 144 |
| Start time | 2026-04-03T16:11:54.711529+00:00 |
| End time | 2026-04-03T17:19:20.687179+00:00 |
| Script version | 5e99aacb33f2db579b63eb853c6d4efe3d0ba807 |
| Python version | 3.14.3 (main, Feb  4 |

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
| claude | statistical | VitaCore vs NutraPure | No | 0.82 | 1 |
| claude | augmented | VitaCore vs NutraPure | Yes | 0.95 | 1 |
| gpt | statistical | VitaCore vs NutraPure | Yes | 0.75 | 1 |
| gpt | augmented | VitaCore vs NutraPure | Yes | 0.90 | 1 |
| gemini | statistical | VitaCore vs NutraPure | No | 0.95 | 1 |
| gemini | augmented | VitaCore vs NutraPure | Yes | 0.95 | 1 |
| deepseek | statistical | VitaCore vs NutraPure | No | 0.65 | 1 |
| deepseek | augmented | VitaCore vs NutraPure | Yes | 0.85 | 1 |
| qwen3_local | statistical | VitaCore vs NutraPure | No | 0.50 | 1 |
| qwen3_local | augmented | VitaCore vs NutraPure | Yes | 0.85 | 1 |
| gemma4_local | statistical | VitaCore vs NutraPure | Yes | 0.75 | 1 |
| gemma4_local | augmented | VitaCore vs NutraPure | Yes | 0.95 | 1 |
| claude | statistical | VitaCore vs FormulaRx | Yes | 0.55 | 1 |
| claude | augmented | VitaCore vs FormulaRx | Yes | 0.92 | 1 |
| gpt | statistical | VitaCore vs FormulaRx | Yes | 0.80 | 1 |
| gpt | augmented | VitaCore vs FormulaRx | Yes | 0.85 | 1 |
| gemini | statistical | VitaCore vs FormulaRx | Yes | 0.85 | 1 |
| gemini | augmented | VitaCore vs FormulaRx | Yes | 0.95 | 1 |
| deepseek | statistical | VitaCore vs FormulaRx | Yes | 0.75 | 1 |
| deepseek | augmented | VitaCore vs FormulaRx | Yes | 0.85 | 1 |
| qwen3_local | statistical | VitaCore vs FormulaRx | Yes | 0.85 | 1 |
| qwen3_local | augmented | VitaCore vs FormulaRx | Yes | 0.85 | 1 |
| gemma4_local | statistical | VitaCore vs FormulaRx | Yes | 0.80 | 1 |
| gemma4_local | augmented | VitaCore vs FormulaRx | Yes | 0.92 | 1 |
| claude | statistical | VitaCore vs CleanDose | Yes | 0.52 | 1 |
| claude | augmented | VitaCore vs CleanDose | Yes | 0.91 | 1 |
| gpt | statistical | VitaCore vs CleanDose | Yes | 0.90 | 1 |
| gpt | augmented | VitaCore vs CleanDose | Yes | 0.90 | 1 |
| gemini | statistical | VitaCore vs CleanDose | Yes | 0.90 | 1 |
| gemini | augmented | VitaCore vs CleanDose | Yes | 0.85 | 1 |
| deepseek | statistical | VitaCore vs CleanDose | Yes | 0.80 | 1 |
| deepseek | augmented | VitaCore vs CleanDose | Yes | 0.85 | 1 |
| qwen3_local | statistical | VitaCore vs CleanDose | Yes | 0.85 | 1 |
| qwen3_local | augmented | VitaCore vs CleanDose | Yes | 0.85 | 1 |
| gemma4_local | statistical | VitaCore vs CleanDose | Yes | 0.90 | 1 |
| gemma4_local | augmented | VitaCore vs CleanDose | Yes | 0.95 | 1 |
| claude | statistical | VitaCore vs ApexStack | Yes | 0.62 | 1 |
| claude | augmented | VitaCore vs ApexStack | Yes | 0.92 | 1 |
| gpt | statistical | VitaCore vs ApexStack | Yes | 0.90 | 1 |
| gpt | augmented | VitaCore vs ApexStack | Yes | 0.90 | 1 |
| gemini | statistical | VitaCore vs ApexStack | Yes | 0.90 | 1 |
| gemini | augmented | VitaCore vs ApexStack | Yes | 0.95 | 1 |
| deepseek | statistical | VitaCore vs ApexStack | Yes | 0.80 | 1 |
| deepseek | augmented | VitaCore vs ApexStack | Yes | 0.85 | 1 |
| qwen3_local | statistical | VitaCore vs ApexStack | Yes | 0.85 | 1 |
| qwen3_local | augmented | VitaCore vs ApexStack | Yes | 0.85 | 1 |
| gemma4_local | statistical | VitaCore vs ApexStack | Yes | 0.90 | 1 |
| gemma4_local | augmented | VitaCore vs ApexStack | Yes | 0.95 | 1 |
| claude | statistical | VitaCore vs RootWell | Yes | 0.72 | 1 |
| claude | augmented | VitaCore vs RootWell | Yes | 0.92 | 1 |
| gpt | statistical | VitaCore vs RootWell | Yes | 0.80 | 1 |
| gpt | augmented | VitaCore vs RootWell | Yes | 0.90 | 1 |
| gemini | statistical | VitaCore vs RootWell | Yes | 0.90 | 1 |
| gemini | augmented | VitaCore vs RootWell | Yes | 0.95 | 1 |
| deepseek | statistical | VitaCore vs RootWell | Yes | 0.80 | 1 |
| deepseek | augmented | VitaCore vs RootWell | Yes | 0.85 | 1 |
| qwen3_local | statistical | VitaCore vs RootWell | Yes | 0.85 | 1 |
| qwen3_local | augmented | VitaCore vs RootWell | Yes | 0.85 | 1 |
| gemma4_local | statistical | VitaCore vs RootWell | Yes | 0.90 | 1 |
| gemma4_local | augmented | VitaCore vs RootWell | Yes | 0.92 | 1 |
| claude | statistical | NutraPure vs FormulaRx | Yes | 0.62 | 1 |
| claude | augmented | NutraPure vs FormulaRx | Yes | 0.97 | 1 |
| gpt | statistical | NutraPure vs FormulaRx | Yes | 0.80 | 1 |
| gpt | augmented | NutraPure vs FormulaRx | Yes | 0.90 | 1 |
| gemini | statistical | NutraPure vs FormulaRx | Yes | 0.90 | 1 |
| gemini | augmented | NutraPure vs FormulaRx | Yes | 0.95 | 1 |
| deepseek | statistical | NutraPure vs FormulaRx | Yes | 0.75 | 1 |
| deepseek | augmented | NutraPure vs FormulaRx | Yes | 0.85 | 1 |
| qwen3_local | statistical | NutraPure vs FormulaRx | Yes | 0.85 | 1 |
| qwen3_local | augmented | NutraPure vs FormulaRx | Yes | 0.85 | 1 |
| gemma4_local | statistical | NutraPure vs FormulaRx | Yes | 0.90 | 1 |
| gemma4_local | augmented | NutraPure vs FormulaRx | Yes | 0.95 | 1 |
| claude | statistical | NutraPure vs CleanDose | Yes | 0.62 | 1 |
| claude | augmented | NutraPure vs CleanDose | Yes | 0.97 | 1 |
| gpt | statistical | NutraPure vs CleanDose | Yes | 0.90 | 1 |
| gpt | augmented | NutraPure vs CleanDose | Yes | 0.90 | 1 |
| gemini | statistical | NutraPure vs CleanDose | Yes | 0.90 | 1 |
| gemini | augmented | NutraPure vs CleanDose | Yes | 0.95 | 1 |
| deepseek | statistical | NutraPure vs CleanDose | Yes | 0.75 | 1 |
| deepseek | augmented | NutraPure vs CleanDose | Yes | 0.85 | 1 |
| qwen3_local | statistical | NutraPure vs CleanDose | Yes | 0.85 | 1 |
| qwen3_local | augmented | NutraPure vs CleanDose | Yes | 0.85 | 1 |
| gemma4_local | statistical | NutraPure vs CleanDose | Yes | 0.90 | 1 |
| gemma4_local | augmented | NutraPure vs CleanDose | Yes | 0.95 | 1 |
| claude | statistical | NutraPure vs ApexStack | Yes | 0.72 | 1 |
| claude | augmented | NutraPure vs ApexStack | Yes | 0.88 | 1 |
| gpt | statistical | NutraPure vs ApexStack | Yes | 0.90 | 1 |
| gpt | augmented | NutraPure vs ApexStack | Yes | 0.90 | 1 |
| gemini | statistical | NutraPure vs ApexStack | Yes | 0.90 | 1 |
| gemini | augmented | NutraPure vs ApexStack | Yes | 0.95 | 1 |
| deepseek | statistical | NutraPure vs ApexStack | Yes | 0.80 | 1 |
| deepseek | augmented | NutraPure vs ApexStack | Yes | 0.85 | 1 |
| qwen3_local | statistical | NutraPure vs ApexStack | Yes | 0.85 | 1 |
| qwen3_local | augmented | NutraPure vs ApexStack | Yes | 0.85 | 1 |
| gemma4_local | statistical | NutraPure vs ApexStack | Yes | 0.90 | 1 |
| gemma4_local | augmented | NutraPure vs ApexStack | Yes | 0.92 | 1 |
| claude | statistical | NutraPure vs RootWell | Yes | 0.72 | 1 |
| claude | augmented | NutraPure vs RootWell | Yes | 0.97 | 1 |
| gpt | statistical | NutraPure vs RootWell | Yes | 0.90 | 1 |
| gpt | augmented | NutraPure vs RootWell | Yes | 0.90 | 1 |
| gemini | statistical | NutraPure vs RootWell | Yes | 0.90 | 1 |
| gemini | augmented | NutraPure vs RootWell | Yes | 0.95 | 1 |
| deepseek | statistical | NutraPure vs RootWell | Yes | 0.80 | 1 |
| deepseek | augmented | NutraPure vs RootWell | Yes | 0.90 | 1 |
| qwen3_local | statistical | NutraPure vs RootWell | Yes | 0.85 | 1 |
| qwen3_local | augmented | NutraPure vs RootWell | Yes | 0.85 | 1 |
| gemma4_local | statistical | NutraPure vs RootWell | Yes | 0.90 | 1 |
| gemma4_local | augmented | NutraPure vs RootWell | Yes | 0.95 | 1 |
| claude | statistical | FormulaRx vs CleanDose | Yes | 0.78 | 1 |
| claude | augmented | FormulaRx vs CleanDose | Yes | 0.92 | 1 |
| gpt | statistical | FormulaRx vs CleanDose | Yes | 0.90 | 1 |
| gpt | augmented | FormulaRx vs CleanDose | Yes | 0.85 | 1 |
| gemini | statistical | FormulaRx vs CleanDose | Yes | 0.95 | 1 |
| gemini | augmented | FormulaRx vs CleanDose | Yes | 0.95 | 1 |
| deepseek | statistical | FormulaRx vs CleanDose | Yes | 0.80 | 1 |
| deepseek | augmented | FormulaRx vs CleanDose | Yes | 0.85 | 1 |
| qwen3_local | statistical | FormulaRx vs CleanDose | Yes | 0.85 | 1 |
| qwen3_local | augmented | FormulaRx vs CleanDose | Yes | 0.85 | 1 |
| gemma4_local | statistical | FormulaRx vs CleanDose | Yes | 0.90 | 1 |
| gemma4_local | augmented | FormulaRx vs CleanDose | Yes | 0.95 | 1 |
| claude | statistical | FormulaRx vs ApexStack | Yes | 0.72 | 1 |
| claude | augmented | FormulaRx vs ApexStack | Yes | 0.95 | 1 |
| gpt | statistical | FormulaRx vs ApexStack | Yes | 0.80 | 1 |
| gpt | augmented | FormulaRx vs ApexStack | Yes | 0.90 | 1 |
| gemini | statistical | FormulaRx vs ApexStack | Yes | 0.90 | 1 |
| gemini | augmented | FormulaRx vs ApexStack | Yes | 0.95 | 1 |
| deepseek | statistical | FormulaRx vs ApexStack | Yes | 0.80 | 1 |
| deepseek | augmented | FormulaRx vs ApexStack | Yes | 0.85 | 1 |
| qwen3_local | statistical | FormulaRx vs ApexStack | Yes | 0.85 | 1 |
| qwen3_local | augmented | FormulaRx vs ApexStack | Yes | 0.85 | 1 |
| gemma4_local | statistical | FormulaRx vs ApexStack | Yes | 0.90 | 1 |
| gemma4_local | augmented | FormulaRx vs ApexStack | Yes | 0.95 | 1 |
| claude | statistical | FormulaRx vs RootWell | Yes | 0.82 | 1 |
| claude | augmented | FormulaRx vs RootWell | Yes | 0.91 | 1 |
| gpt | statistical | FormulaRx vs RootWell | Yes | 0.90 | 1 |
| gpt | augmented | FormulaRx vs RootWell | Yes | 0.90 | 1 |
| gemini | statistical | FormulaRx vs RootWell | Yes | 0.95 | 1 |
| gemini | augmented | FormulaRx vs RootWell | Yes | 0.95 | 1 |
| deepseek | statistical | FormulaRx vs RootWell | Yes | 0.80 | 1 |
| deepseek | augmented | FormulaRx vs RootWell | Yes | 0.85 | 1 |
| qwen3_local | statistical | FormulaRx vs RootWell | Yes | 0.85 | 1 |
| qwen3_local | augmented | FormulaRx vs RootWell | Yes | 0.85 | 1 |
| gemma4_local | statistical | FormulaRx vs RootWell | Yes | 0.90 | 1 |
| gemma4_local | augmented | FormulaRx vs RootWell | Yes | 0.95 | 1 |
| claude | statistical | CleanDose vs ApexStack | Yes | 0.82 | 1 |
| claude | augmented | CleanDose vs ApexStack | Yes | 0.92 | 1 |
| gpt | statistical | CleanDose vs ApexStack | Yes | 0.90 | 1 |
| gpt | augmented | CleanDose vs ApexStack | Yes | 0.90 | 1 |
| gemini | statistical | CleanDose vs ApexStack | Yes | 0.95 | 1 |
| gemini | augmented | CleanDose vs ApexStack | Yes | 1.00 | 1 |
| deepseek | statistical | CleanDose vs ApexStack | Yes | 0.80 | 1 |
| deepseek | augmented | CleanDose vs ApexStack | Yes | 0.85 | 1 |
| qwen3_local | statistical | CleanDose vs ApexStack | Yes | 0.85 | 1 |
| qwen3_local | augmented | CleanDose vs ApexStack | Yes | 0.85 | 1 |
| gemma4_local | statistical | CleanDose vs ApexStack | Yes | 0.95 | 1 |
| gemma4_local | augmented | CleanDose vs ApexStack | Yes | 0.95 | 1 |
| claude | statistical | CleanDose vs RootWell | Yes | 0.62 | 1 |
| claude | augmented | CleanDose vs RootWell | Yes | 0.91 | 1 |
| gpt | statistical | CleanDose vs RootWell | Yes | 0.80 | 1 |
| gpt | augmented | CleanDose vs RootWell | Yes | 0.90 | 1 |
| gemini | statistical | CleanDose vs RootWell | Yes | 0.85 | 1 |
| gemini | augmented | CleanDose vs RootWell | Yes | 0.95 | 1 |
| deepseek | statistical | CleanDose vs RootWell | Yes | 0.80 | 1 |
| deepseek | augmented | CleanDose vs RootWell | Yes | 0.90 | 1 |
| qwen3_local | statistical | CleanDose vs RootWell | Yes | 0.85 | 1 |
| qwen3_local | augmented | CleanDose vs RootWell | Yes | 0.85 | 1 |
| gemma4_local | statistical | CleanDose vs RootWell | Yes | 0.90 | 1 |
| gemma4_local | augmented | CleanDose vs RootWell | Yes | 0.95 | 1 |
| claude | statistical | ApexStack vs RootWell | Yes | 0.88 | 1 |
| claude | augmented | ApexStack vs RootWell | Yes | 0.97 | 1 |
| gpt | statistical | ApexStack vs RootWell | Yes | 0.90 | 1 |
| gpt | augmented | ApexStack vs RootWell | Yes | 0.90 | 1 |
| gemini | statistical | ApexStack vs RootWell | Yes | 0.95 | 1 |
| gemini | augmented | ApexStack vs RootWell | Yes | 0.95 | 1 |
| deepseek | statistical | ApexStack vs RootWell | Yes | 0.90 | 1 |
| deepseek | augmented | ApexStack vs RootWell | Yes | 0.90 | 1 |
| qwen3_local | statistical | ApexStack vs RootWell | Yes | 0.85 | 1 |
| qwen3_local | augmented | ApexStack vs RootWell | Yes | 0.85 | 1 |
| gemma4_local | statistical | ApexStack vs RootWell | Yes | 0.90 | 1 |
| gemma4_local | augmented | ApexStack vs RootWell | Yes | 0.95 | 1 |
| claude | statistical | VitaCore vs NutraPure | No | 0.82 | 2 |
| claude | augmented | VitaCore vs NutraPure | Yes | 0.95 | 2 |
| gpt | statistical | VitaCore vs NutraPure | No | 0.90 | 2 |
| gpt | augmented | VitaCore vs NutraPure | Yes | 0.90 | 2 |
| gemini | statistical | VitaCore vs NutraPure | No | 0.98 | 2 |
| gemini | augmented | VitaCore vs NutraPure | Yes | 0.95 | 2 |
| deepseek | statistical | VitaCore vs NutraPure | No | 0.75 | 2 |
| deepseek | augmented | VitaCore vs NutraPure | Yes | 0.85 | 2 |
| qwen3_local | statistical | VitaCore vs NutraPure | Yes | 0.85 | 2 |
| qwen3_local | augmented | VitaCore vs NutraPure | Yes | 0.85 | 2 |
| gemma4_local | statistical | VitaCore vs NutraPure | Yes | 0.90 | 2 |
| gemma4_local | augmented | VitaCore vs NutraPure | Yes | 0.95 | 2 |
| claude | statistical | VitaCore vs FormulaRx | Yes | 0.55 | 2 |
| claude | augmented | VitaCore vs FormulaRx | Yes | 0.92 | 2 |
| gpt | statistical | VitaCore vs FormulaRx | Yes | 0.80 | 2 |
| gpt | augmented | VitaCore vs FormulaRx | Yes | 0.90 | 2 |
| gemini | statistical | VitaCore vs FormulaRx | Yes | 0.85 | 2 |
| gemini | augmented | VitaCore vs FormulaRx | Yes | 0.95 | 2 |
| deepseek | statistical | VitaCore vs FormulaRx | Yes | 0.70 | 2 |
| deepseek | augmented | VitaCore vs FormulaRx | Yes | 0.85 | 2 |
| qwen3_local | statistical | VitaCore vs FormulaRx | Yes | 0.85 | 2 |
| qwen3_local | augmented | VitaCore vs FormulaRx | Yes | 0.85 | 2 |
| gemma4_local | statistical | VitaCore vs FormulaRx | Yes | 0.90 | 2 |
| gemma4_local | augmented | VitaCore vs FormulaRx | Yes | 0.92 | 2 |
| claude | statistical | VitaCore vs CleanDose | Yes | 0.52 | 2 |
| claude | augmented | VitaCore vs CleanDose | Yes | 0.91 | 2 |
| gpt | statistical | VitaCore vs CleanDose | Yes | 0.90 | 2 |
| gpt | augmented | VitaCore vs CleanDose | Yes | 0.90 | 2 |
| gemini | statistical | VitaCore vs CleanDose | Yes | 0.90 | 2 |
| gemini | augmented | VitaCore vs CleanDose | Yes | 0.00 | 2 |
| deepseek | statistical | VitaCore vs CleanDose | Yes | 0.80 | 2 |
| deepseek | augmented | VitaCore vs CleanDose | Yes | 0.85 | 2 |
| qwen3_local | statistical | VitaCore vs CleanDose | Yes | 0.85 | 2 |
| qwen3_local | augmented | VitaCore vs CleanDose | Yes | 0.85 | 2 |
| gemma4_local | statistical | VitaCore vs CleanDose | Yes | 0.90 | 2 |
| gemma4_local | augmented | VitaCore vs CleanDose | Yes | 0.92 | 2 |
| claude | statistical | VitaCore vs ApexStack | Yes | 0.62 | 2 |
| claude | augmented | VitaCore vs ApexStack | Yes | 0.92 | 2 |
| gpt | statistical | VitaCore vs ApexStack | Yes | 0.90 | 2 |
| gpt | augmented | VitaCore vs ApexStack | Yes | 0.90 | 2 |
| gemini | statistical | VitaCore vs ApexStack | Yes | 0.90 | 2 |
| gemini | augmented | VitaCore vs ApexStack | Yes | 0.85 | 2 |
| deepseek | statistical | VitaCore vs ApexStack | Yes | 0.80 | 2 |
| deepseek | augmented | VitaCore vs ApexStack | Yes | 0.85 | 2 |
| qwen3_local | statistical | VitaCore vs ApexStack | Yes | 0.85 | 2 |
| qwen3_local | augmented | VitaCore vs ApexStack | Yes | 0.85 | 2 |
| gemma4_local | statistical | VitaCore vs ApexStack | Yes | 0.90 | 2 |
| gemma4_local | augmented | VitaCore vs ApexStack | Yes | 0.92 | 2 |
| claude | statistical | VitaCore vs RootWell | Yes | 0.72 | 2 |
| claude | augmented | VitaCore vs RootWell | Yes | 0.92 | 2 |
| gpt | statistical | VitaCore vs RootWell | Yes | 0.85 | 2 |
| gpt | augmented | VitaCore vs RootWell | Yes | 0.90 | 2 |
| gemini | statistical | VitaCore vs RootWell | Yes | 0.95 | 2 |
| gemini | augmented | VitaCore vs RootWell | Yes | 0.95 | 2 |
| deepseek | statistical | VitaCore vs RootWell | Yes | 0.80 | 2 |
| deepseek | augmented | VitaCore vs RootWell | Yes | 0.85 | 2 |
| qwen3_local | statistical | VitaCore vs RootWell | Yes | 0.85 | 2 |
| qwen3_local | augmented | VitaCore vs RootWell | Yes | 0.85 | 2 |
| gemma4_local | statistical | VitaCore vs RootWell | Yes | 0.90 | 2 |
| gemma4_local | augmented | VitaCore vs RootWell | Yes | 0.92 | 2 |
| claude | statistical | NutraPure vs FormulaRx | Yes | 0.62 | 2 |
| claude | augmented | NutraPure vs FormulaRx | Yes | 0.97 | 2 |
| gpt | statistical | NutraPure vs FormulaRx | Yes | 0.90 | 2 |
| gpt | augmented | NutraPure vs FormulaRx | Yes | 0.90 | 2 |
| gemini | statistical | NutraPure vs FormulaRx | Yes | 0.85 | 2 |
| gemini | augmented | NutraPure vs FormulaRx | Yes | 0.95 | 2 |
| deepseek | statistical | NutraPure vs FormulaRx | Yes | 0.75 | 2 |
| deepseek | augmented | NutraPure vs FormulaRx | Yes | 0.85 | 2 |
| qwen3_local | statistical | NutraPure vs FormulaRx | Yes | 0.85 | 2 |
| qwen3_local | augmented | NutraPure vs FormulaRx | Yes | 0.85 | 2 |
| gemma4_local | statistical | NutraPure vs FormulaRx | Yes | 0.90 | 2 |
| gemma4_local | augmented | NutraPure vs FormulaRx | Yes | 0.95 | 2 |
| claude | statistical | NutraPure vs CleanDose | Yes | 0.62 | 2 |
| claude | augmented | NutraPure vs CleanDose | Yes | 0.97 | 2 |
| gpt | statistical | NutraPure vs CleanDose | Yes | 0.90 | 2 |
| gpt | augmented | NutraPure vs CleanDose | Yes | 0.90 | 2 |
| gemini | statistical | NutraPure vs CleanDose | Yes | 0.90 | 2 |
| gemini | augmented | NutraPure vs CleanDose | Yes | 0.95 | 2 |
| deepseek | statistical | NutraPure vs CleanDose | Yes | 0.75 | 2 |
| deepseek | augmented | NutraPure vs CleanDose | Yes | 0.85 | 2 |
| qwen3_local | statistical | NutraPure vs CleanDose | Yes | 0.85 | 2 |
| qwen3_local | augmented | NutraPure vs CleanDose | Yes | 0.85 | 2 |
| gemma4_local | statistical | NutraPure vs CleanDose | Yes | 0.90 | 2 |
| gemma4_local | augmented | NutraPure vs CleanDose | Yes | 0.95 | 2 |
| claude | statistical | NutraPure vs ApexStack | Yes | 0.72 | 2 |
| claude | augmented | NutraPure vs ApexStack | Yes | 0.88 | 2 |
| gpt | statistical | NutraPure vs ApexStack | Yes | 0.85 | 2 |
| gpt | augmented | NutraPure vs ApexStack | Yes | 0.90 | 2 |
| gemini | statistical | NutraPure vs ApexStack | Yes | 0.90 | 2 |
| gemini | augmented | NutraPure vs ApexStack | Yes | 0.90 | 2 |
| deepseek | statistical | NutraPure vs ApexStack | Yes | 0.80 | 2 |
| deepseek | augmented | NutraPure vs ApexStack | Yes | 0.85 | 2 |
| qwen3_local | statistical | NutraPure vs ApexStack | Yes | 0.85 | 2 |
| qwen3_local | augmented | NutraPure vs ApexStack | Yes | 0.85 | 2 |
| gemma4_local | statistical | NutraPure vs ApexStack | Yes | 0.90 | 2 |
| gemma4_local | augmented | NutraPure vs ApexStack | Yes | 0.90 | 2 |
| claude | statistical | NutraPure vs RootWell | Yes | 0.72 | 2 |
| claude | augmented | NutraPure vs RootWell | Yes | 0.97 | 2 |
| gpt | statistical | NutraPure vs RootWell | Yes | 0.90 | 2 |
| gpt | augmented | NutraPure vs RootWell | Yes | 0.90 | 2 |
| gemini | statistical | NutraPure vs RootWell | Yes | 0.90 | 2 |
| gemini | augmented | NutraPure vs RootWell | Yes | 0.95 | 2 |
| deepseek | statistical | NutraPure vs RootWell | Yes | 0.80 | 2 |
| deepseek | augmented | NutraPure vs RootWell | Yes | 0.90 | 2 |
| qwen3_local | statistical | NutraPure vs RootWell | Yes | 0.85 | 2 |
| qwen3_local | augmented | NutraPure vs RootWell | Yes | 0.85 | 2 |
| gemma4_local | statistical | NutraPure vs RootWell | Yes | 0.90 | 2 |
| gemma4_local | augmented | NutraPure vs RootWell | Yes | 0.95 | 2 |
| claude | statistical | FormulaRx vs CleanDose | Yes | 0.78 | 2 |
| claude | augmented | FormulaRx vs CleanDose | Yes | 0.92 | 2 |
| gpt | statistical | FormulaRx vs CleanDose | Yes | 0.90 | 2 |
| gpt | augmented | FormulaRx vs CleanDose | Yes | 0.90 | 2 |
| gemini | statistical | FormulaRx vs CleanDose | Yes | 0.95 | 2 |
| gemini | augmented | FormulaRx vs CleanDose | Yes | 0.95 | 2 |
| deepseek | statistical | FormulaRx vs CleanDose | Yes | 0.80 | 2 |
| deepseek | augmented | FormulaRx vs CleanDose | Yes | 0.85 | 2 |
| qwen3_local | statistical | FormulaRx vs CleanDose | Yes | 0.85 | 2 |
| qwen3_local | augmented | FormulaRx vs CleanDose | Yes | 0.85 | 2 |
| gemma4_local | statistical | FormulaRx vs CleanDose | Yes | 0.90 | 2 |
| gemma4_local | augmented | FormulaRx vs CleanDose | Yes | 0.95 | 2 |
| claude | statistical | FormulaRx vs ApexStack | Yes | 0.72 | 2 |
| claude | augmented | FormulaRx vs ApexStack | Yes | 0.93 | 2 |
| gpt | statistical | FormulaRx vs ApexStack | Yes | 0.90 | 2 |
| gpt | augmented | FormulaRx vs ApexStack | Yes | 0.90 | 2 |
| gemini | statistical | FormulaRx vs ApexStack | Yes | 0.95 | 2 |
| gemini | augmented | FormulaRx vs ApexStack | Yes | 0.95 | 2 |
| deepseek | statistical | FormulaRx vs ApexStack | Yes | 0.80 | 2 |
| deepseek | augmented | FormulaRx vs ApexStack | Yes | 0.85 | 2 |
| qwen3_local | statistical | FormulaRx vs ApexStack | Yes | 0.85 | 2 |
| qwen3_local | augmented | FormulaRx vs ApexStack | Yes | 0.85 | 2 |
| gemma4_local | statistical | FormulaRx vs ApexStack | Yes | 0.90 | 2 |
| gemma4_local | augmented | FormulaRx vs ApexStack | Yes | 0.95 | 2 |
| claude | statistical | FormulaRx vs RootWell | Yes | 0.82 | 2 |
| claude | augmented | FormulaRx vs RootWell | Yes | 0.92 | 2 |
| gpt | statistical | FormulaRx vs RootWell | Yes | 0.90 | 2 |
| gpt | augmented | FormulaRx vs RootWell | Yes | 0.90 | 2 |
| gemini | statistical | FormulaRx vs RootWell | Yes | 0.95 | 2 |
| gemini | augmented | FormulaRx vs RootWell | Yes | 0.95 | 2 |
| deepseek | statistical | FormulaRx vs RootWell | Yes | 0.80 | 2 |
| deepseek | augmented | FormulaRx vs RootWell | Yes | 0.85 | 2 |
| qwen3_local | statistical | FormulaRx vs RootWell | Yes | 0.85 | 2 |
| qwen3_local | augmented | FormulaRx vs RootWell | Yes | 0.85 | 2 |
| gemma4_local | statistical | FormulaRx vs RootWell | Yes | 0.90 | 2 |
| gemma4_local | augmented | FormulaRx vs RootWell | Yes | 0.95 | 2 |
| claude | statistical | CleanDose vs ApexStack | Yes | 0.82 | 2 |
| claude | augmented | CleanDose vs ApexStack | Yes | 0.93 | 2 |
| gpt | statistical | CleanDose vs ApexStack | Yes | 0.90 | 2 |
| gpt | augmented | CleanDose vs ApexStack | Yes | 0.90 | 2 |
| gemini | statistical | CleanDose vs ApexStack | Yes | 0.95 | 2 |
| gemini | augmented | CleanDose vs ApexStack | Yes | 0.95 | 2 |
| deepseek | statistical | CleanDose vs ApexStack | Yes | 0.80 | 2 |
| deepseek | augmented | CleanDose vs ApexStack | Yes | 0.85 | 2 |
| qwen3_local | statistical | CleanDose vs ApexStack | Yes | 0.85 | 2 |
| qwen3_local | augmented | CleanDose vs ApexStack | Yes | 0.85 | 2 |
| gemma4_local | statistical | CleanDose vs ApexStack | Yes | 0.90 | 2 |
| gemma4_local | augmented | CleanDose vs ApexStack | Yes | 0.95 | 2 |
| claude | statistical | CleanDose vs RootWell | Yes | 0.62 | 2 |
| claude | augmented | CleanDose vs RootWell | Yes | 0.91 | 2 |
| gpt | statistical | CleanDose vs RootWell | Yes | 0.80 | 2 |
| gpt | augmented | CleanDose vs RootWell | Yes | 0.90 | 2 |
| gemini | statistical | CleanDose vs RootWell | Yes | 0.80 | 2 |
| gemini | augmented | CleanDose vs RootWell | Yes | 0.90 | 2 |
| deepseek | statistical | CleanDose vs RootWell | Yes | 0.80 | 2 |
| deepseek | augmented | CleanDose vs RootWell | Yes | 0.85 | 2 |
| qwen3_local | statistical | CleanDose vs RootWell | Yes | 0.85 | 2 |
| qwen3_local | augmented | CleanDose vs RootWell | Yes | 0.85 | 2 |
| gemma4_local | statistical | CleanDose vs RootWell | Yes | 0.90 | 2 |
| gemma4_local | augmented | CleanDose vs RootWell | Yes | 0.95 | 2 |
| claude | statistical | ApexStack vs RootWell | Yes | 0.87 | 2 |
| claude | augmented | ApexStack vs RootWell | Yes | 0.95 | 2 |
| gpt | statistical | ApexStack vs RootWell | Yes | 0.90 | 2 |
| gpt | augmented | ApexStack vs RootWell | Yes | 0.90 | 2 |
| gemini | statistical | ApexStack vs RootWell | Yes | 0.95 | 2 |
| gemini | augmented | ApexStack vs RootWell | Yes | 0.95 | 2 |
| deepseek | statistical | ApexStack vs RootWell | Yes | 0.90 | 2 |
| deepseek | augmented | ApexStack vs RootWell | Yes | 0.90 | 2 |
| qwen3_local | statistical | ApexStack vs RootWell | Yes | 0.85 | 2 |
| qwen3_local | augmented | ApexStack vs RootWell | Yes | 0.85 | 2 |
| gemma4_local | statistical | ApexStack vs RootWell | Yes | 0.95 | 2 |
| gemma4_local | augmented | ApexStack vs RootWell | Yes | 0.95 | 2 |
| claude | statistical | VitaCore vs NutraPure | No | 0.82 | 3 |
| claude | augmented | VitaCore vs NutraPure | Yes | 0.95 | 3 |
| gpt | statistical | VitaCore vs NutraPure | Yes | 0.80 | 3 |
| gpt | augmented | VitaCore vs NutraPure | Yes | 0.90 | 3 |
| gemini | statistical | VitaCore vs NutraPure | No | 0.95 | 3 |
| gemini | augmented | VitaCore vs NutraPure | Yes | 0.95 | 3 |
| deepseek | statistical | VitaCore vs NutraPure | No | 0.70 | 3 |
| deepseek | augmented | VitaCore vs NutraPure | Yes | 0.90 | 3 |
| qwen3_local | statistical | VitaCore vs NutraPure | Yes | 0.85 | 3 |
| qwen3_local | augmented | VitaCore vs NutraPure | Yes | 0.85 | 3 |
| gemma4_local | statistical | VitaCore vs NutraPure | Yes | 0.75 | 3 |
| gemma4_local | augmented | VitaCore vs NutraPure | Yes | 0.92 | 3 |
| claude | statistical | VitaCore vs FormulaRx | Yes | 0.52 | 3 |
| claude | augmented | VitaCore vs FormulaRx | Yes | 0.92 | 3 |
| gpt | statistical | VitaCore vs FormulaRx | Yes | 0.80 | 3 |
| gpt | augmented | VitaCore vs FormulaRx | Yes | 0.90 | 3 |
| gemini | statistical | VitaCore vs FormulaRx | Yes | 0.85 | 3 |
| gemini | augmented | VitaCore vs FormulaRx | Yes | 0.95 | 3 |
| deepseek | statistical | VitaCore vs FormulaRx | Yes | 0.75 | 3 |
| deepseek | augmented | VitaCore vs FormulaRx | Yes | 0.85 | 3 |
| qwen3_local | statistical | VitaCore vs FormulaRx | Yes | 0.85 | 3 |
| qwen3_local | augmented | VitaCore vs FormulaRx | Yes | 0.85 | 3 |
| gemma4_local | statistical | VitaCore vs FormulaRx | Yes | 0.90 | 3 |
| gemma4_local | augmented | VitaCore vs FormulaRx | Yes | 0.92 | 3 |
| claude | statistical | VitaCore vs CleanDose | Yes | 0.62 | 3 |
| claude | augmented | VitaCore vs CleanDose | Yes | 0.92 | 3 |
| gpt | statistical | VitaCore vs CleanDose | Yes | 0.90 | 3 |
| gpt | augmented | VitaCore vs CleanDose | Yes | 0.90 | 3 |
| gemini | statistical | VitaCore vs CleanDose | Yes | 0.90 | 3 |
| gemini | augmented | VitaCore vs CleanDose | Yes | 0.95 | 3 |
| deepseek | statistical | VitaCore vs CleanDose | Yes | 0.75 | 3 |
| deepseek | augmented | VitaCore vs CleanDose | Yes | 0.85 | 3 |
| qwen3_local | statistical | VitaCore vs CleanDose | Yes | 0.85 | 3 |
| qwen3_local | augmented | VitaCore vs CleanDose | Yes | 0.85 | 3 |
| gemma4_local | statistical | VitaCore vs CleanDose | Yes | 0.90 | 3 |
| gemma4_local | augmented | VitaCore vs CleanDose | Yes | 0.95 | 3 |
| claude | statistical | VitaCore vs ApexStack | Yes | 0.62 | 3 |
| claude | augmented | VitaCore vs ApexStack | Yes | 0.92 | 3 |
| gpt | statistical | VitaCore vs ApexStack | Yes | 0.90 | 3 |
| gpt | augmented | VitaCore vs ApexStack | Yes | 0.90 | 3 |
| gemini | statistical | VitaCore vs ApexStack | Yes | 0.90 | 3 |
| gemini | augmented | VitaCore vs ApexStack | Yes | 0.95 | 3 |
| deepseek | statistical | VitaCore vs ApexStack | Yes | 0.80 | 3 |
| deepseek | augmented | VitaCore vs ApexStack | Yes | 0.85 | 3 |
| qwen3_local | statistical | VitaCore vs ApexStack | Yes | 0.85 | 3 |
| qwen3_local | augmented | VitaCore vs ApexStack | Yes | 0.85 | 3 |
| gemma4_local | statistical | VitaCore vs ApexStack | Yes | 0.90 | 3 |
| gemma4_local | augmented | VitaCore vs ApexStack | Yes | 0.95 | 3 |
| claude | statistical | VitaCore vs RootWell | Yes | 0.72 | 3 |
| claude | augmented | VitaCore vs RootWell | Yes | 0.91 | 3 |
| gpt | statistical | VitaCore vs RootWell | Yes | 0.90 | 3 |
| gpt | augmented | VitaCore vs RootWell | Yes | 0.85 | 3 |
| gemini | statistical | VitaCore vs RootWell | Yes | 0.90 | 3 |
| gemini | augmented | VitaCore vs RootWell | Yes | 0.95 | 3 |
| deepseek | statistical | VitaCore vs RootWell | Yes | 0.80 | 3 |
| deepseek | augmented | VitaCore vs RootWell | Yes | 0.85 | 3 |
| qwen3_local | statistical | VitaCore vs RootWell | Yes | 0.85 | 3 |
| qwen3_local | augmented | VitaCore vs RootWell | Yes | 0.85 | 3 |
| gemma4_local | statistical | VitaCore vs RootWell | Yes | 0.90 | 3 |
| gemma4_local | augmented | VitaCore vs RootWell | Yes | 0.95 | 3 |
| claude | statistical | NutraPure vs FormulaRx | Yes | 0.62 | 3 |
| claude | augmented | NutraPure vs FormulaRx | Yes | 0.97 | 3 |
| gpt | statistical | NutraPure vs FormulaRx | Yes | 0.90 | 3 |
| gpt | augmented | NutraPure vs FormulaRx | Yes | 0.90 | 3 |
| gemini | statistical | NutraPure vs FormulaRx | Yes | 0.85 | 3 |
| gemini | augmented | NutraPure vs FormulaRx | Yes | 0.95 | 3 |
| deepseek | statistical | NutraPure vs FormulaRx | Yes | 0.75 | 3 |
| deepseek | augmented | NutraPure vs FormulaRx | Yes | 0.85 | 3 |
| qwen3_local | statistical | NutraPure vs FormulaRx | Yes | 0.85 | 3 |
| qwen3_local | augmented | NutraPure vs FormulaRx | Yes | 0.85 | 3 |
| gemma4_local | statistical | NutraPure vs FormulaRx | Yes | 0.80 | 3 |
| gemma4_local | augmented | NutraPure vs FormulaRx | Yes | 0.95 | 3 |
| claude | statistical | NutraPure vs CleanDose | Yes | 0.62 | 3 |
| claude | augmented | NutraPure vs CleanDose | Yes | 0.97 | 3 |
| gpt | statistical | NutraPure vs CleanDose | Yes | 0.90 | 3 |
| gpt | augmented | NutraPure vs CleanDose | Yes | 0.90 | 3 |
| gemini | statistical | NutraPure vs CleanDose | Yes | 0.90 | 3 |
| gemini | augmented | NutraPure vs CleanDose | Yes | 0.95 | 3 |
| deepseek | statistical | NutraPure vs CleanDose | Yes | 0.75 | 3 |
| deepseek | augmented | NutraPure vs CleanDose | Yes | 0.85 | 3 |
| qwen3_local | statistical | NutraPure vs CleanDose | Yes | 0.85 | 3 |
| qwen3_local | augmented | NutraPure vs CleanDose | Yes | 0.85 | 3 |
| gemma4_local | statistical | NutraPure vs CleanDose | Yes | 0.90 | 3 |
| gemma4_local | augmented | NutraPure vs CleanDose | Yes | 0.90 | 3 |
| claude | statistical | NutraPure vs ApexStack | Yes | 0.72 | 3 |
| claude | augmented | NutraPure vs ApexStack | Yes | 0.88 | 3 |
| gpt | statistical | NutraPure vs ApexStack | Yes | 0.90 | 3 |
| gpt | augmented | NutraPure vs ApexStack | Yes | 0.90 | 3 |
| gemini | statistical | NutraPure vs ApexStack | Yes | 0.90 | 3 |
| gemini | augmented | NutraPure vs ApexStack | Yes | 0.90 | 3 |
| deepseek | statistical | NutraPure vs ApexStack | Yes | 0.80 | 3 |
| deepseek | augmented | NutraPure vs ApexStack | Yes | 0.85 | 3 |
| qwen3_local | statistical | NutraPure vs ApexStack | Yes | 0.85 | 3 |
| qwen3_local | augmented | NutraPure vs ApexStack | Yes | 0.85 | 3 |
| gemma4_local | statistical | NutraPure vs ApexStack | Yes | 0.90 | 3 |
| gemma4_local | augmented | NutraPure vs ApexStack | Yes | 0.92 | 3 |
| claude | statistical | NutraPure vs RootWell | Yes | 0.72 | 3 |
| claude | augmented | NutraPure vs RootWell | Yes | 0.97 | 3 |
| gpt | statistical | NutraPure vs RootWell | Yes | 0.90 | 3 |
| gpt | augmented | NutraPure vs RootWell | Yes | 0.90 | 3 |
| gemini | statistical | NutraPure vs RootWell | Yes | 0.90 | 3 |
| gemini | augmented | NutraPure vs RootWell | Yes | 0.95 | 3 |
| deepseek | statistical | NutraPure vs RootWell | Yes | 0.80 | 3 |
| deepseek | augmented | NutraPure vs RootWell | Yes | 0.85 | 3 |
| qwen3_local | statistical | NutraPure vs RootWell | Yes | 0.85 | 3 |
| qwen3_local | augmented | NutraPure vs RootWell | Yes | 0.85 | 3 |
| gemma4_local | statistical | NutraPure vs RootWell | Yes | 0.90 | 3 |
| gemma4_local | augmented | NutraPure vs RootWell | Yes | 0.95 | 3 |
| claude | statistical | FormulaRx vs CleanDose | Yes | 0.82 | 3 |
| claude | augmented | FormulaRx vs CleanDose | Yes | 0.92 | 3 |
| gpt | statistical | FormulaRx vs CleanDose | Yes | 0.90 | 3 |
| gpt | augmented | FormulaRx vs CleanDose | Yes | 0.90 | 3 |
| gemini | statistical | FormulaRx vs CleanDose | Yes | 0.90 | 3 |
| gemini | augmented | FormulaRx vs CleanDose | Yes | 0.95 | 3 |
| deepseek | statistical | FormulaRx vs CleanDose | Yes | 0.80 | 3 |
| deepseek | augmented | FormulaRx vs CleanDose | Yes | 0.85 | 3 |
| qwen3_local | statistical | FormulaRx vs CleanDose | Yes | 0.85 | 3 |
| qwen3_local | augmented | FormulaRx vs CleanDose | Yes | 0.85 | 3 |
| gemma4_local | statistical | FormulaRx vs CleanDose | Yes | 0.90 | 3 |
| gemma4_local | augmented | FormulaRx vs CleanDose | Yes | 0.95 | 3 |
| claude | statistical | FormulaRx vs ApexStack | Yes | 0.72 | 3 |
| claude | augmented | FormulaRx vs ApexStack | Yes | 0.95 | 3 |
| gpt | statistical | FormulaRx vs ApexStack | Yes | 0.90 | 3 |
| gpt | augmented | FormulaRx vs ApexStack | Yes | 0.90 | 3 |
| gemini | statistical | FormulaRx vs ApexStack | Yes | 0.95 | 3 |
| gemini | augmented | FormulaRx vs ApexStack | Yes | 0.95 | 3 |
| deepseek | statistical | FormulaRx vs ApexStack | Yes | 0.80 | 3 |
| deepseek | augmented | FormulaRx vs ApexStack | Yes | 0.85 | 3 |
| qwen3_local | statistical | FormulaRx vs ApexStack | Yes | 0.85 | 3 |
| qwen3_local | augmented | FormulaRx vs ApexStack | Yes | 0.85 | 3 |
| gemma4_local | statistical | FormulaRx vs ApexStack | Yes | 0.90 | 3 |
| gemma4_local | augmented | FormulaRx vs ApexStack | Yes | 0.92 | 3 |
| claude | statistical | FormulaRx vs RootWell | Yes | 0.82 | 3 |
| claude | augmented | FormulaRx vs RootWell | Yes | 0.92 | 3 |
| gpt | statistical | FormulaRx vs RootWell | Yes | 0.90 | 3 |
| gpt | augmented | FormulaRx vs RootWell | Yes | 0.90 | 3 |
| gemini | statistical | FormulaRx vs RootWell | Yes | 0.95 | 3 |
| gemini | augmented | FormulaRx vs RootWell | Yes | 0.95 | 3 |
| deepseek | statistical | FormulaRx vs RootWell | Yes | 0.90 | 3 |
| deepseek | augmented | FormulaRx vs RootWell | Yes | 0.90 | 3 |
| qwen3_local | statistical | FormulaRx vs RootWell | Yes | 0.85 | 3 |
| qwen3_local | augmented | FormulaRx vs RootWell | Yes | 0.85 | 3 |
| gemma4_local | statistical | FormulaRx vs RootWell | Yes | 0.92 | 3 |
| gemma4_local | augmented | FormulaRx vs RootWell | Yes | 0.95 | 3 |
| claude | statistical | CleanDose vs ApexStack | Yes | 0.82 | 3 |
| claude | augmented | CleanDose vs ApexStack | Yes | 0.92 | 3 |
| gpt | statistical | CleanDose vs ApexStack | Yes | 0.90 | 3 |
| gpt | augmented | CleanDose vs ApexStack | Yes | 0.90 | 3 |
| gemini | statistical | CleanDose vs ApexStack | Yes | 0.95 | 3 |
| gemini | augmented | CleanDose vs ApexStack | Yes | 0.95 | 3 |
| deepseek | statistical | CleanDose vs ApexStack | Yes | 0.80 | 3 |
| deepseek | augmented | CleanDose vs ApexStack | Yes | 0.85 | 3 |
| qwen3_local | statistical | CleanDose vs ApexStack | Yes | 0.85 | 3 |
| qwen3_local | augmented | CleanDose vs ApexStack | Yes | 0.85 | 3 |
| gemma4_local | statistical | CleanDose vs ApexStack | Yes | 0.95 | 3 |
| gemma4_local | augmented | CleanDose vs ApexStack | Yes | 0.95 | 3 |
| claude | statistical | CleanDose vs RootWell | Yes | 0.62 | 3 |
| claude | augmented | CleanDose vs RootWell | Yes | 0.91 | 3 |
| gpt | statistical | CleanDose vs RootWell | Yes | 0.90 | 3 |
| gpt | augmented | CleanDose vs RootWell | Yes | 0.90 | 3 |
| gemini | statistical | CleanDose vs RootWell | Yes | 0.85 | 3 |
| gemini | augmented | CleanDose vs RootWell | Yes | 0.95 | 3 |
| deepseek | statistical | CleanDose vs RootWell | Yes | 0.80 | 3 |
| deepseek | augmented | CleanDose vs RootWell | Yes | 0.85 | 3 |
| qwen3_local | statistical | CleanDose vs RootWell | Yes | 0.85 | 3 |
| qwen3_local | augmented | CleanDose vs RootWell | Yes | 0.85 | 3 |
| gemma4_local | statistical | CleanDose vs RootWell | Yes | 0.90 | 3 |
| gemma4_local | augmented | CleanDose vs RootWell | Yes | 0.92 | 3 |
| claude | statistical | ApexStack vs RootWell | Yes | 0.88 | 3 |
| claude | augmented | ApexStack vs RootWell | Yes | 0.97 | 3 |
| gpt | statistical | ApexStack vs RootWell | Yes | 0.90 | 3 |
| gpt | augmented | ApexStack vs RootWell | Yes | 0.90 | 3 |
| gemini | statistical | ApexStack vs RootWell | Yes | 0.95 | 3 |
| gemini | augmented | ApexStack vs RootWell | Yes | 0.95 | 3 |
| deepseek | statistical | ApexStack vs RootWell | Yes | 0.90 | 3 |
| deepseek | augmented | ApexStack vs RootWell | Yes | 0.90 | 3 |
| qwen3_local | statistical | ApexStack vs RootWell | Yes | 0.85 | 3 |
| qwen3_local | augmented | ApexStack vs RootWell | Yes | 0.85 | 3 |
| gemma4_local | statistical | ApexStack vs RootWell | Yes | 0.92 | 3 |
| gemma4_local | augmented | ApexStack vs RootWell | Yes | 0.95 | 3 |

## Table 3: Behavioral Prediction Accuracy

| Model | Condition | Brand | Scenario (abbrev) | Accuracy | Run |
|-------|-----------|-------|------------------|---------|-----|
| claude | statistical | VitaCore | A customer receives a defective product and reques... | 0.22 | 1 |
| claude | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 1 |
| gpt | statistical | VitaCore | A customer receives a defective product and reques... | 0.67 | 1 |
| gpt | augmented | VitaCore | A customer receives a defective product and reques... | 0.89 | 1 |
| gemini | statistical | VitaCore | A customer receives a defective product and reques... | 1.00 | 1 |
| gemini | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 1 |
| deepseek | statistical | VitaCore | A customer receives a defective product and reques... | 1.00 | 1 |
| deepseek | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 1 |
| qwen3_local | statistical | VitaCore | A customer receives a defective product and reques... | 0.89 | 1 |
| qwen3_local | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 1 |
| gemma4_local | statistical | VitaCore | A customer receives a defective product and reques... | 0.67 | 1 |
| gemma4_local | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 1 |
| claude | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.36 | 1 |
| claude | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.36 | 1 |
| gpt | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 1 |
| gpt | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 1 |
| gemini | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 1 |
| gemini | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.00 | 1 |
| deepseek | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 1 |
| deepseek | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 1 |
| qwen3_local | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 1 |
| qwen3_local | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 1 |
| gemma4_local | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.00 | 1 |
| gemma4_local | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.36 | 1 |
| claude | statistical | NutraPure | A customer receives a defective product and reques... | 1.00 | 1 |
| claude | augmented | NutraPure | A customer receives a defective product and reques... | 0.86 | 1 |
| gpt | statistical | NutraPure | A customer receives a defective product and reques... | 0.57 | 1 |
| gpt | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 1 |
| gemini | statistical | NutraPure | A customer receives a defective product and reques... | 0.00 | 1 |
| gemini | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 1 |
| deepseek | statistical | NutraPure | A customer receives a defective product and reques... | 0.00 | 1 |
| deepseek | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 1 |
| qwen3_local | statistical | NutraPure | A customer receives a defective product and reques... | 0.29 | 1 |
| qwen3_local | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 1 |
| gemma4_local | statistical | NutraPure | A customer receives a defective product and reques... | 0.00 | 1 |
| gemma4_local | augmented | NutraPure | A customer receives a defective product and reques... | 0.86 | 1 |
| claude | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 1 |
| claude | augmented | NutraPure | A competitor launches an identical product at 30% ... | 1.00 | 1 |
| gpt | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 1 |
| gpt | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 1 |
| gemini | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 1 |
| gemini | augmented | NutraPure | A competitor launches an identical product at 30% ... | 1.00 | 1 |
| deepseek | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 1 |
| deepseek | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.40 | 1 |
| qwen3_local | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 1 |
| qwen3_local | augmented | NutraPure | A competitor launches an identical product at 30% ... | 1.00 | 1 |
| gemma4_local | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 1 |
| gemma4_local | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.40 | 1 |
| claude | statistical | VitaCore | A customer receives a defective product and reques... | 0.22 | 2 |
| claude | augmented | VitaCore | A customer receives a defective product and reques... | 0.67 | 2 |
| gpt | statistical | VitaCore | A customer receives a defective product and reques... | 1.00 | 2 |
| gpt | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 2 |
| gemini | statistical | VitaCore | A customer receives a defective product and reques... | 1.00 | 2 |
| gemini | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 2 |
| deepseek | statistical | VitaCore | A customer receives a defective product and reques... | 1.00 | 2 |
| deepseek | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 2 |
| qwen3_local | statistical | VitaCore | A customer receives a defective product and reques... | 0.00 | 2 |
| qwen3_local | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 2 |
| gemma4_local | statistical | VitaCore | A customer receives a defective product and reques... | 0.89 | 2 |
| gemma4_local | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 2 |
| claude | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.36 | 2 |
| claude | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.36 | 2 |
| gpt | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 2 |
| gpt | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 2 |
| gemini | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.00 | 2 |
| gemini | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 2 |
| deepseek | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 2 |
| deepseek | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 2 |
| qwen3_local | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 2 |
| qwen3_local | augmented | VitaCore | A competitor launches an identical product at 30% ... | 1.00 | 2 |
| gemma4_local | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 2 |
| gemma4_local | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 2 |
| claude | statistical | NutraPure | A customer receives a defective product and reques... | 0.57 | 2 |
| claude | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 2 |
| gpt | statistical | NutraPure | A customer receives a defective product and reques... | 0.00 | 2 |
| gpt | augmented | NutraPure | A customer receives a defective product and reques... | 0.57 | 2 |
| gemini | statistical | NutraPure | A customer receives a defective product and reques... | 0.29 | 2 |
| gemini | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 2 |
| deepseek | statistical | NutraPure | A customer receives a defective product and reques... | 0.29 | 2 |
| deepseek | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 2 |
| qwen3_local | statistical | NutraPure | A customer receives a defective product and reques... | 0.29 | 2 |
| qwen3_local | augmented | NutraPure | A customer receives a defective product and reques... | 0.86 | 2 |
| gemma4_local | statistical | NutraPure | A customer receives a defective product and reques... | 0.57 | 2 |
| gemma4_local | augmented | NutraPure | A customer receives a defective product and reques... | 0.86 | 2 |
| claude | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 2 |
| claude | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.80 | 2 |
| gpt | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 2 |
| gpt | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.40 | 2 |
| gemini | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 2 |
| gemini | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 2 |
| deepseek | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 2 |
| deepseek | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 2 |
| qwen3_local | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 2 |
| qwen3_local | augmented | NutraPure | A competitor launches an identical product at 30% ... | 1.00 | 2 |
| gemma4_local | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 2 |
| gemma4_local | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 2 |
| claude | statistical | VitaCore | A customer receives a defective product and reques... | 1.00 | 3 |
| claude | augmented | VitaCore | A customer receives a defective product and reques... | 0.67 | 3 |
| gpt | statistical | VitaCore | A customer receives a defective product and reques... | 0.67 | 3 |
| gpt | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 3 |
| gemini | statistical | VitaCore | A customer receives a defective product and reques... | 1.00 | 3 |
| gemini | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 3 |
| deepseek | statistical | VitaCore | A customer receives a defective product and reques... | 0.67 | 3 |
| deepseek | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 3 |
| qwen3_local | statistical | VitaCore | A customer receives a defective product and reques... | 1.00 | 3 |
| qwen3_local | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 3 |
| gemma4_local | statistical | VitaCore | A customer receives a defective product and reques... | 1.00 | 3 |
| gemma4_local | augmented | VitaCore | A customer receives a defective product and reques... | 1.00 | 3 |
| claude | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.36 | 3 |
| claude | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 3 |
| gpt | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 3 |
| gpt | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.36 | 3 |
| gemini | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 3 |
| gemini | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 3 |
| deepseek | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 3 |
| deepseek | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 3 |
| qwen3_local | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 3 |
| qwen3_local | augmented | VitaCore | A competitor launches an identical product at 30% ... | 1.00 | 3 |
| gemma4_local | statistical | VitaCore | A competitor launches an identical product at 30% ... | 0.18 | 3 |
| gemma4_local | augmented | VitaCore | A competitor launches an identical product at 30% ... | 0.36 | 3 |
| claude | statistical | NutraPure | A customer receives a defective product and reques... | 0.29 | 3 |
| claude | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 3 |
| gpt | statistical | NutraPure | A customer receives a defective product and reques... | 0.57 | 3 |
| gpt | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 3 |
| gemini | statistical | NutraPure | A customer receives a defective product and reques... | 0.29 | 3 |
| gemini | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 3 |
| deepseek | statistical | NutraPure | A customer receives a defective product and reques... | 0.29 | 3 |
| deepseek | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 3 |
| qwen3_local | statistical | NutraPure | A customer receives a defective product and reques... | 0.29 | 3 |
| qwen3_local | augmented | NutraPure | A customer receives a defective product and reques... | 1.00 | 3 |
| gemma4_local | statistical | NutraPure | A customer receives a defective product and reques... | 0.00 | 3 |
| gemma4_local | augmented | NutraPure | A customer receives a defective product and reques... | 0.57 | 3 |
| claude | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 3 |
| claude | augmented | NutraPure | A competitor launches an identical product at 30% ... | 1.00 | 3 |
| gpt | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 3 |
| gpt | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 3 |
| gemini | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 3 |
| gemini | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.40 | 3 |
| deepseek | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 3 |
| deepseek | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.40 | 3 |
| qwen3_local | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 3 |
| qwen3_local | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.80 | 3 |
| gemma4_local | statistical | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 3 |
| gemma4_local | augmented | NutraPure | A competitor launches an identical product at 30% ... | 0.00 | 3 |

## Table 4: Cross-Model Recommendation Variance

| Condition | Variance | Interpretation |
|-----------|---------|----------------|
| statistical | 0.0083 | Higher variance: models disagree |
| augmented | 0.0048 | Lower variance: specification aligns models |

## Table 5: Statistical Tests and Effect Sizes

| Test | Statistic | p-value | Effect Size | Significant |
|------|-----------|---------|-------------|-------------|
| Chi-square (discrimination rate) | -1.0 | N/A | Cramer's V = 0.144 | N/A |
| Fisher's exact (discrimination rate) | --- | 0.0009 | Cohen's h = 0.406 | Yes * |
| Wilcoxon signed-rank (confidence) | 32893.500 | 0.0000 | Cohen's d = 0.791 | Yes * |
| F-test (variance ratio) | 1.740 | 0.0000 | --- | Yes * |

**BMI 95% CI** (VitaCore_vs_NutraPure): [0.976, 0.982] (bootstrap, n=1000)

## Table 6: Per-Model Discrimination Rates by Condition

| Model | Condition | N | Discrimination Rate | Mean Confidence |
|-------|-----------|---|--------------------:|----------------:|
| claude | statistical | 45 | 0.933 | 0.706 |
| claude | augmented | 45 | 1.000 | 0.932 |
| deepseek | statistical | 45 | 0.933 | 0.790 |
| deepseek | augmented | 45 | 1.000 | 0.859 |
| gemini | statistical | 45 | 0.933 | 0.910 |
| gemini | augmented | 45 | 1.000 | 0.922 |
| gemma4_local | statistical | 45 | 1.000 | 0.893 |
| gemma4_local | augmented | 45 | 1.000 | 0.940 |
| gpt | statistical | 45 | 0.978 | 0.874 |
| gpt | augmented | 45 | 1.000 | 0.897 |
| qwen3_local | statistical | 45 | 0.978 | 0.842 |
| qwen3_local | augmented | 45 | 1.000 | 0.850 |

## Table 7: Inter-Model Agreement Matrix

Proportion of brand-pair evaluations where both models agree on can_distinguish.

| Model | claude | deepseek | gemini | gemma4_local | gpt | qwen3_local |
|-------|------:|------:|------:|------:|------:|------:|
| claude | 1.000 | 1.000 | 1.000 | 0.967 | 0.978 | 0.978 |
| deepseek | 1.000 | 1.000 | 1.000 | 0.967 | 0.978 | 0.978 |
| gemini | 1.000 | 1.000 | 1.000 | 0.967 | 0.978 | 0.978 |
| gemma4_local | 0.967 | 0.967 | 0.967 | 1.000 | 0.989 | 0.989 |
| gpt | 0.978 | 0.978 | 0.978 | 0.989 | 1.000 | 0.978 |
| qwen3_local | 0.978 | 0.978 | 0.978 | 0.989 | 0.978 | 1.000 |

**Fleiss' kappa**: 0.536 (moderate agreement, n_subjects=90, n_raters=6)

---

## Interpretation

Fisher's exact significant: augmented condition shifts discrimination rate. Wilcoxon significant: augmented condition yields higher confidence scores. F-test significant: variance differs between conditions. Effect sizes: Cohen's h = 0.406 (small), Cohen's d = 0.791 (medium).

If BMI > 0.5 AND discrimination improves under augmented condition
AND cross-model variance decreases under augmented condition,
then Proposition 6 (behavioral metamerism) is supported:

> Brands with identical statistical profiles but structurally
> different behavioral signatures cannot be distinguished through
> statistical observation alone; behavioral specification is required.
