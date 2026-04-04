# R15 AI Search Metamerism -- Summary Tables

## Table 0: Experiment Metadata

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-03 |
| Models | claude, gpt, gemini, deepseek, qwen, qwen3_local, gemma4_local |
| Runs per prompt | 1 |
| Brand pairs | 10 |
| Total calls | 1260 |
| Temperature | 0.7 |
| Script version | 46d04933dd8186507c2cd84118e20f882f0f7b37 |

## Table 1: Dimensional Citation Frequency (Recommendation + Differentiation Prompts)

| Dimension | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Aggregate |
|-----------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| semiotic | 0.650 | 0.750 | 0.150 | 0.650 | 0.000 | 0.500 | 0.900 | 0.514 |
| narrative | 0.550 | 0.550 | 0.000 | 0.500 | 0.000 | 0.350 | 0.500 | 0.350 |
| ideological | 0.950 | 0.950 | 0.100 | 0.900 | 0.000 | 0.700 | 0.900 | 0.643 |
| experiential | 1.000 | 1.000 | 0.400 | 0.950 | 0.000 | 0.700 | 1.000 | 0.721 |
| social | 0.750 | 0.950 | 0.050 | 0.600 | 0.000 | 0.550 | 0.800 | 0.529 |
| economic | 0.950 | 0.850 | 0.250 | 0.850 | 0.000 | 0.700 | 0.900 | 0.643 |
| cultural | 0.800 | 0.900 | 0.100 | 0.850 | 0.000 | 0.800 | 0.950 | 0.629 |
| temporal | 0.800 | 0.750 | 0.150 | 0.600 | 0.000 | 0.750 | 0.850 | 0.557 |

## Table 2: Dimensional Collapse Index (Economic + Semiotic / Total)

Baseline (uniform): 2/8 = 0.250. Values above 0.250 indicate dimensional collapse.

| Model | DCI | vs Baseline | Interpretation |
|-------|-----|-------------|----------------|
| claude | 0.248 | -0.002 | Near-uniform |
| gpt | 0.239 | -0.011 | Near-uniform |
| gemini | 0.333 | +0.083 | Moderate |
| deepseek | 0.254 | +0.004 | Near-uniform |
| qwen | N/A | N/A | Insufficient data |
| qwen3_local | 0.238 | -0.012 | Near-uniform |
| gemma4_local | 0.265 | +0.015 | Near-uniform |

## Table 3: Mean Dimension Probe Scores (0-10) by Brand

### Aman

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 8.0 | 7.5 | -- | 9.5 | -- | 7.5 | 8.0 | 8.1 | 0.67 |
| narrative | soft | 8.0 | 7.5 | -- | 9.5 | -- | 7.5 | 7.0 | 7.9 | 0.92 |
| ideological | soft | 7.5 | 7.5 | -- | 8.0 | -- | 7.5 | 7.0 | 7.5 | 0.12 |
| experiential | hard | 8.5 | 7.5 | -- | 9.5 | -- | -- | 8.0 | 8.4 | 0.73 |
| social | soft | 8.5 | 7.5 | -- | 9.5 | -- | 7.5 | 7.0 | 8.0 | 1.00 |
| economic | hard | 6.5 | 7.5 | -- | 9.5 | -- | -- | 7.0 | 7.6 | 1.73 |
| cultural | soft | 6.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.5 | 7.7 | 0.70 |
| temporal | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |

### Apple

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 9.5 | 9.5 | -- | 10.0 | -- | -- | 9.5 | 9.6 | 0.06 |
| narrative | soft | 8.5 | 8.5 | -- | 9.5 | -- | 7.5 | 7.5 | 8.3 | 0.70 |
| ideological | soft | 7.0 | 7.5 | -- | 8.0 | -- | 7.5 | 7.0 | 7.4 | 0.17 |
| experiential | hard | 8.5 | 9.0 | -- | 9.5 | -- | 7.5 | 9.0 | 8.7 | 0.57 |
| social | soft | 8.5 | 8.5 | -- | 9.5 | -- | 7.5 | 8.5 | 8.5 | 0.50 |
| economic | hard | 7.5 | 8.5 | -- | 8.5 | -- | 7.5 | 8.5 | 8.1 | 0.30 |
| cultural | soft | 8.5 | 8.5 | -- | 9.5 | -- | 7.5 | 8.0 | 8.4 | 0.55 |
| temporal | soft | 7.5 | 8.5 | -- | 8.5 | -- | 7.5 | 7.5 | 7.9 | 0.30 |

### Aspiration

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 6.5 | 7.5 | -- | 7.0 | -- | 7.5 | 8.0 | 7.3 | 0.32 |
| narrative | soft | 6.5 | 7.5 | -- | 7.5 | -- | 7.5 | 8.0 | 7.4 | 0.30 |
| ideological | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 7.0 | 7.6 | 0.30 |
| experiential | hard | 6.5 | 7.5 | -- | 3.5 | -- | 7.5 | 8.0 | 6.6 | 3.30 |
| social | soft | 6.5 | 7.5 | -- | 7.5 | -- | -- | 8.5 | 7.5 | 0.67 |
| economic | hard | 7.5 | 7.5 | -- | 7.5 | -- | 7.5 | 8.0 | 7.6 | 0.05 |
| cultural | soft | 5.5 | 7.5 | -- | 4.5 | -- | 7.5 | 8.5 | 6.7 | 2.70 |
| temporal | soft | 3.5 | 7.5 | -- | 2.5 | -- | -- | 6.5 | 5.0 | 5.67 |

### Chase

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| narrative | soft | 6.5 | 7.5 | -- | 6.5 | -- | 7.5 | 7.0 | 7.0 | 0.25 |
| ideological | soft | 6.0 | 7.5 | -- | 6.0 | -- | 7.5 | 6.0 | 6.6 | 0.67 |
| experiential | hard | 6.5 | 7.5 | -- | 7.0 | -- | 7.5 | 7.5 | 7.2 | 0.20 |
| social | soft | 4.5 | 7.5 | -- | 2.5 | -- | 7.5 | 7.5 | 5.9 | 5.30 |
| economic | hard | 6.5 | 7.5 | -- | 7.5 | -- | 7.5 | 7.5 | 7.3 | 0.20 |
| cultural | soft | 4.5 | 7.5 | -- | 3.0 | -- | -- | 6.5 | 5.4 | 4.06 |
| temporal | soft | 7.5 | 7.5 | 7.5 | 8.5 | -- | 7.5 | 7.5 | 7.7 | 0.17 |

### Coach

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 8.0 | 7.5 | -- | 8.5 | -- | 7.5 | 7.5 | 7.8 | 0.20 |
| narrative | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 7.0 | 7.6 | 0.30 |
| ideological | soft | 6.5 | 7.5 | 7.5 | 7.0 | -- | 7.5 | 6.5 | 7.1 | 0.24 |
| experiential | hard | 7.5 | 7.5 | -- | 7.5 | -- | 7.5 | 7.5 | 7.5 | 0.00 |
| social | soft | 7.2 | 7.5 | -- | 7.5 | -- | 7.5 | 7.5 | 7.4 | 0.02 |
| economic | hard | 7.5 | 7.5 | -- | 7.5 | -- | 7.5 | 7.0 | 7.4 | 0.05 |
| cultural | soft | 7.0 | 7.5 | -- | 7.0 | -- | 7.5 | 7.0 | 7.2 | 0.08 |
| temporal | soft | 7.5 | 7.5 | -- | 8.0 | -- | 7.5 | 7.5 | 7.6 | 0.05 |

### Columbia

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 7.5 | 7.5 | -- | 7.0 | -- | 7.5 | 8.0 | 7.5 | 0.12 |
| narrative | soft | 7.0 | 7.5 | -- | 7.0 | -- | 7.5 | 7.0 | 7.2 | 0.08 |
| ideological | soft | 6.5 | 7.5 | 7.5 | 6.5 | -- | 7.5 | 7.0 | 7.1 | 0.24 |
| experiential | hard | 6.5 | 7.5 | -- | 5.5 | -- | 7.5 | 7.0 | 6.8 | 0.70 |
| social | soft | 6.5 | 7.5 | -- | 5.5 | -- | 7.5 | 7.0 | 6.8 | 0.70 |
| economic | hard | 7.5 | 7.5 | 7.5 | 7.5 | -- | 7.5 | 7.0 | 7.4 | 0.04 |
| cultural | soft | 6.5 | 7.5 | -- | 6.5 | -- | 7.5 | 7.0 | 7.0 | 0.25 |
| temporal | soft | 7.5 | 7.5 | 7.5 | 7.5 | -- | -- | 7.0 | 7.4 | 0.05 |

### Erewhon

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| narrative | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| ideological | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| experiential | hard | 7.5 | 7.5 | -- | 9.0 | -- | 7.5 | 8.5 | 8.0 | 0.50 |
| social | soft | 8.0 | 7.5 | -- | 9.0 | -- | 7.5 | 8.0 | 8.0 | 0.38 |
| economic | hard | 5.5 | 7.5 | -- | 2.0 | -- | 7.5 | 7.0 | 5.9 | 5.42 |
| cultural | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| temporal | soft | 7.5 | 7.5 | -- | 3.0 | -- | 7.5 | 7.0 | 6.5 | 3.88 |

### Four Seasons

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 8.0 | 7.5 | -- | 8.5 | -- | 7.5 | 8.5 | 8.0 | 0.25 |
| narrative | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| ideological | soft | 6.5 | 7.5 | -- | 7.0 | -- | 7.5 | 7.0 | 7.1 | 0.17 |
| experiential | hard | 9.0 | 8.5 | -- | 9.5 | -- | 7.5 | 8.5 | 8.6 | 0.55 |
| social | soft | 8.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.5 | 8.1 | 0.30 |
| economic | hard | 7.5 | 8.5 | -- | 9.0 | -- | -- | 8.5 | 8.4 | 0.40 |
| cultural | soft | 6.5 | 7.5 | -- | 7.5 | -- | 7.5 | 7.0 | 7.2 | 0.20 |
| temporal | soft | 8.0 | 8.5 | -- | 8.5 | -- | 7.5 | 8.0 | 8.1 | 0.18 |

### Glossier

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 8.5 | 7.5 | -- | 9.0 | -- | 7.5 | 8.0 | 8.1 | 0.43 |
| narrative | soft | 8.0 | 7.5 | -- | 9.0 | -- | 7.5 | 8.0 | 8.0 | 0.38 |
| ideological | soft | 6.5 | 7.5 | -- | 6.5 | -- | 7.5 | 7.0 | 7.0 | 0.25 |
| experiential | hard | 8.0 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.9 | 0.17 |
| social | soft | 8.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.5 | 8.1 | 0.30 |
| economic | hard | 7.5 | 7.5 | -- | 8.0 | -- | 7.5 | 7.5 | 7.6 | 0.05 |
| cultural | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| temporal | soft | 3.5 | 7.5 | -- | 3.5 | -- | -- | 5.5 | 5.0 | 3.67 |

### Gordons

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 8.0 | 7.5 | -- | 8.0 | -- | 7.5 | 8.0 | 7.8 | 0.08 |
| narrative | soft | 7.5 | 7.5 | -- | 8.0 | -- | 7.5 | 8.0 | 7.7 | 0.07 |
| ideological | soft | 5.5 | 7.5 | -- | 3.0 | -- | -- | 6.5 | 5.6 | 3.73 |
| experiential | hard | 6.5 | 7.5 | -- | 3.5 | -- | 7.5 | 7.5 | 6.5 | 3.00 |
| social | soft | 7.5 | 7.5 | -- | 2.5 | -- | -- | 6.5 | 6.0 | 5.67 |
| economic | hard | 7.0 | 7.5 | -- | 8.0 | -- | -- | 7.5 | 7.5 | 0.17 |
| cultural | soft | 7.5 | 7.5 | -- | 7.5 | -- | 7.5 | 6.5 | 7.3 | 0.20 |
| temporal | soft | 8.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 8.0 | 0.25 |

### Hendricks

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 8.5 | 7.5 | -- | 9.0 | -- | 7.5 | 8.5 | 8.2 | 0.45 |
| narrative | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.5 | 7.9 | 0.30 |
| ideological | soft | 6.0 | 7.5 | -- | 7.5 | -- | 7.5 | 6.5 | 7.0 | 0.50 |
| experiential | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.5 | 7.9 | 0.30 |
| social | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 7.5 | 7.7 | 0.20 |
| economic | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 7.0 | 7.6 | 0.30 |
| cultural | soft | 7.0 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.7 | 0.32 |
| temporal | soft | 6.5 | 7.5 | -- | 7.5 | -- | 7.5 | 7.0 | 7.2 | 0.20 |

### Hermes

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 9.0 | 9.0 | -- | 9.5 | -- | 7.5 | 9.0 | 8.8 | 0.57 |
| narrative | soft | 8.5 | 8.5 | -- | 9.5 | -- | 7.5 | 8.5 | 8.5 | 0.50 |
| ideological | soft | 6.5 | 7.5 | -- | 7.0 | -- | 7.5 | 7.0 | 7.1 | 0.17 |
| experiential | hard | 8.5 | 8.5 | -- | 9.5 | -- | 7.5 | 9.0 | 8.6 | 0.55 |
| social | soft | 9.0 | 8.5 | -- | 9.5 | -- | -- | 9.0 | 9.0 | 0.17 |
| economic | hard | 7.5 | 8.5 | -- | 9.5 | -- | -- | 9.0 | 8.6 | 0.73 |
| cultural | soft | 8.2 | 8.5 | -- | 9.5 | -- | 7.5 | 8.5 | 8.4 | 0.52 |
| temporal | soft | 9.0 | 9.0 | -- | 9.5 | -- | -- | 8.5 | 9.0 | 0.17 |

### Maybelline

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 7.5 | 7.7 | 0.20 |
| narrative | soft | 7.0 | 7.5 | -- | 7.0 | -- | 7.5 | 7.0 | 7.2 | 0.08 |
| ideological | soft | 6.5 | 7.5 | -- | 5.5 | -- | 7.5 | 6.5 | 6.7 | 0.70 |
| experiential | hard | 6.5 | 7.5 | -- | 5.5 | -- | 7.5 | 7.0 | 6.8 | 0.70 |
| social | soft | 6.5 | 7.5 | -- | 6.5 | -- | 7.5 | 7.5 | 7.1 | 0.30 |
| economic | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| cultural | soft | 7.2 | 7.5 | -- | 7.5 | -- | 7.5 | 7.0 | 7.3 | 0.05 |
| temporal | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 7.0 | 7.6 | 0.30 |

### Mercedes

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 9.0 | 9.0 | -- | 9.5 | -- | 7.5 | 9.0 | 8.8 | 0.57 |
| narrative | soft | 8.0 | 7.5 | -- | 9.0 | -- | 7.5 | 8.5 | 8.1 | 0.43 |
| ideological | soft | 6.5 | 7.5 | 7.5 | 7.0 | -- | 7.5 | 7.5 | 7.2 | 0.17 |
| experiential | hard | 7.5 | 7.5 | -- | 8.0 | -- | 7.5 | 8.5 | 7.8 | 0.20 |
| social | soft | 8.2 | 7.5 | 7.5 | 8.5 | -- | 7.5 | 8.0 | 7.9 | 0.19 |
| economic | hard | 7.5 | 8.0 | -- | 7.0 | -- | 7.5 | 8.5 | 7.7 | 0.32 |
| cultural | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 7.5 | 7.7 | 0.20 |
| temporal | soft | 9.0 | 9.0 | -- | 9.5 | -- | 7.5 | 8.5 | 8.7 | 0.57 |

### Nike

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 9.5 | 9.5 | -- | 9.5 | -- | -- | 9.0 | 9.4 | 0.06 |
| narrative | soft | 8.5 | 8.5 | -- | 9.5 | -- | 7.5 | 8.5 | 8.5 | 0.50 |
| ideological | soft | 7.0 | 7.5 | -- | 7.5 | -- | 7.5 | 7.0 | 7.3 | 0.07 |
| experiential | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| social | soft | 8.5 | 7.5 | -- | 9.0 | -- | 7.5 | 8.5 | 8.2 | 0.45 |
| economic | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| cultural | soft | 8.5 | 8.5 | -- | 9.5 | -- | 7.5 | 8.5 | 8.5 | 0.50 |
| temporal | soft | 8.0 | 8.5 | 7.5 | 8.5 | -- | 7.5 | 7.5 | 7.9 | 0.24 |

### Patagonia

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 8.5 | 8.5 | -- | 9.0 | -- | 7.5 | 9.0 | 8.5 | 0.38 |
| narrative | soft | 9.0 | 8.5 | -- | 9.5 | -- | 7.5 | 9.0 | 8.7 | 0.57 |
| ideological | soft | 9.0 | 9.5 | -- | 9.5 | -- | 7.5 | 9.5 | 9.0 | 0.75 |
| experiential | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.5 | 7.9 | 0.30 |
| social | soft | 8.5 | 8.5 | -- | 9.5 | -- | 7.5 | 9.0 | 8.6 | 0.55 |
| economic | hard | 7.5 | 7.5 | -- | 9.0 | -- | 7.5 | 8.5 | 8.0 | 0.50 |
| cultural | soft | 8.0 | 7.5 | -- | 9.0 | -- | 7.5 | 9.0 | 8.2 | 0.57 |
| temporal | soft | 8.0 | 8.5 | -- | 9.0 | -- | 7.5 | 8.0 | 8.2 | 0.33 |

### Samsung

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 8.0 | 8.5 | -- | 8.5 | -- | 7.5 | 8.5 | 8.2 | 0.20 |
| narrative | soft | 6.5 | 7.5 | -- | 6.5 | -- | 7.5 | 7.0 | 7.0 | 0.25 |
| ideological | soft | 6.5 | 7.5 | -- | 6.5 | -- | 7.5 | 6.5 | 6.9 | 0.30 |
| experiential | hard | 7.0 | 7.5 | -- | 7.0 | -- | 7.5 | 7.5 | 7.3 | 0.08 |
| social | soft | 6.5 | 7.5 | -- | 6.5 | -- | 7.5 | 7.0 | 7.0 | 0.25 |
| economic | hard | 7.5 | 7.5 | -- | 8.0 | -- | 7.5 | 7.5 | 7.6 | 0.05 |
| cultural | soft | 6.5 | 7.5 | -- | 7.0 | -- | 7.5 | 6.5 | 7.0 | 0.25 |
| temporal | soft | 7.5 | 7.5 | -- | 8.0 | -- | 7.5 | 7.0 | 7.5 | 0.12 |

### Shein

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 7.0 | 7.5 | -- | 8.0 | -- | 7.5 | 6.5 | 7.3 | 0.32 |
| narrative | soft | 3.5 | 7.5 | -- | 2.5 | -- | -- | 5.5 | 4.8 | 4.92 |
| ideological | soft | 1.5 | 4.0 | -- | 1.5 | -- | -- | 3.0 | 2.5 | 1.50 |
| experiential | hard | 4.5 | 7.5 | -- | 5.5 | -- | 7.5 | 6.5 | 6.3 | 1.70 |
| social | soft | 4.5 | 7.5 | -- | 2.5 | -- | -- | 8.5 | 5.8 | 7.58 |
| economic | hard | 8.0 | 7.5 | -- | 8.5 | -- | 7.5 | 8.5 | 8.0 | 0.25 |
| cultural | soft | 6.5 | 6.0 | -- | 8.5 | -- | 7.5 | 6.5 | 7.0 | 1.00 |
| temporal | soft | 2.5 | 3.0 | -- | 1.5 | -- | -- | 1.0 | 2.0 | 0.83 |

### Tesla

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 8.0 | 8.5 | -- | 9.0 | -- | 7.5 | 9.0 | 8.4 | 0.42 |
| narrative | soft | 8.5 | 8.5 | -- | 9.5 | -- | 7.5 | 8.5 | 8.5 | 0.50 |
| ideological | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| experiential | hard | 7.0 | 7.5 | -- | 8.5 | -- | 7.5 | 7.5 | 7.6 | 0.30 |
| social | soft | 8.0 | 8.5 | -- | 9.5 | -- | 7.5 | 8.5 | 8.4 | 0.55 |
| economic | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.5 | 7.9 | 0.30 |
| cultural | soft | 7.5 | 7.5 | 7.5 | 8.5 | -- | 7.5 | 7.5 | 7.7 | 0.17 |
| temporal | soft | 4.5 | 7.5 | -- | 7.5 | -- | 7.5 | 5.5 | 6.5 | 2.00 |

### Whole Foods

| Dimension | Type | claude | gpt | gemini | deepseek | qwen | qwen3_local | gemma4_local | Mean | Cross-Model Var |
|-----------|------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| semiotic | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| narrative | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 7.0 | 7.6 | 0.30 |
| ideological | soft | 7.5 | 7.5 | -- | 8.0 | -- | 7.5 | 8.0 | 7.7 | 0.07 |
| experiential | hard | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 7.5 | 7.7 | 0.20 |
| social | soft | 7.5 | 7.5 | -- | 8.5 | -- | 7.5 | 8.0 | 7.8 | 0.20 |
| economic | hard | 5.5 | 7.5 | -- | 6.0 | -- | 7.5 | 7.0 | 6.7 | 0.82 |
| cultural | soft | 7.0 | 7.5 | -- | 8.0 | -- | 7.5 | 8.0 | 7.6 | 0.17 |
| temporal | soft | 7.0 | 7.5 | -- | 7.0 | -- | 7.5 | 6.5 | 7.1 | 0.17 |

## Table 4: Cross-Model Probe Score Variance by Dimension Type

Prediction (H3): soft-dimension variance > hard-dimension variance.

| Brand | Hard Dim Mean Var | Soft Dim Mean Var | Hard < Soft? |
|-------|------------------:|------------------:|:------------:|
| Aman | 1.044 | 0.487 | No |
| Apple | 0.312 | 0.431 | Yes |
| Aspiration | 1.225 | 2.242 | Yes |
| Chase | 0.200 | 1.289 | Yes |
| Coach | 0.083 | 0.167 | Yes |
| Columbia | 0.289 | 0.154 | No |
| Erewhon | 2.042 | 1.119 | No |
| Four Seasons | 0.399 | 0.188 | No |
| Glossier | 0.217 | 1.123 | Yes |
| Gordons | 1.081 | 1.064 | No |
| Hendricks | 0.350 | 0.331 | No |
| Hermes | 0.618 | 0.340 | No |
| Maybelline | 0.367 | 0.282 | No |
| Mercedes | 0.367 | 0.344 | No |
| Nike | 0.154 | 0.329 | Yes |
| Patagonia | 0.392 | 0.556 | Yes |
| Samsung | 0.108 | 0.231 | Yes |
| Shein | 0.758 | 2.062 | Yes |
| Tesla | 0.342 | 0.717 | Yes |
| Whole Foods | 0.408 | 0.181 | No |

## Table 5: Statistical Tests

| Hypothesis | Test | Result | Supported? |
|------------|------|--------|------------|
| H1 (Economic+Semiotic over-weighting) | Binomial (p=0.4607) | Rate=0.252 vs baseline=0.250 | No |
| H2 (Cross-model convergence) | Fleiss kappa=-0.131 | Threshold >= 0.40 | No |
| H3 (Soft-dim higher variance) | t-test (p=0.2080), d=0.139 | Mean var hard=0.538, soft=0.682 | No |
| H4 (Soft-dim pair convergence) | Agreement rates | Soft=0.686, Hard=0.714 | No |

## Table 6: Aggregate Citation Rates by Dimension

Uniform baseline = 0.125 (1/8). Values > baseline = over-cited.

| Dimension | Type | Agg Rate | vs Baseline | Over-cited? |
|-----------|------|:--------:|:-----------:|:-----------:|
| semiotic | hard | 0.514 | +0.389 | Yes |
| narrative | soft | 0.350 | +0.225 | Yes |
| ideological | soft | 0.643 | +0.518 | Yes |
| experiential | hard | 0.721 | +0.596 | Yes |
| social | soft | 0.529 | +0.404 | Yes |
| economic | hard | 0.643 | +0.518 | Yes |
| cultural | soft | 0.629 | +0.504 | Yes |
| temporal | soft | 0.557 | +0.432 | Yes |

---

## Interpretation

If H1 is supported: LLMs systematically collapse multi-dimensional brand perception
to Economic and Semiotic dimensions, producing spectral metamerism in AI-mediated search.

If H2 is supported: This collapse is consistent across model families, indicating it
is a property of text-based training corpora rather than any specific architecture.

If H3 is supported: LLMs have differential dimensional sensitivity -- they measure
Economic and Semiotic with high cross-model agreement but diverge on Cultural and
Temporal dimensions, which are observer-dependent and perception-dense.

If H4 is supported: Brands differentiated on "soft" dimensions (Narrative, Ideological,
Cultural, Temporal) appear more similar through AI-mediated search than brands
differentiated on "hard" dimensions -- a direct operational consequence of spectral
metamerism.

Theoretical implication: Brands that invest in soft-dimension differentiation face an
AI search penalty. Their perception clouds are real but invisible to the AI mediator.
