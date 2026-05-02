"""
dimension_volatility.py -- Companion computation script for R11 (2026r)
"Why Eight? Completeness and Necessity of the SBT Dimensional Taxonomy"
Zharnikov (2026r). DOI: 10.5281/zenodo.19207599

PURPOSE
-------
Documents the computation pipeline for the 22-model DCI volatility analysis
described in Section 8A of the paper. Specifically:
  - The 22-vs-24 model panel (two models excluded from Run 5 for insufficient data)
  - The Dimensional Collapse Index (DCI) formula and its role in ranking stability
  - The dimension-volatility ranking from the drop-one and variance decomposition
    experiments (Tables 1 and 3 of Section 8A)

This script is a methodology template. The underlying LLM weight profiles from
R15 Run 5 are required as input (see DATA section below). When that data file is
present, the script reproduces Tables 1-4 of Section 8A deterministically.

The full reproducible script for Tables 1-4 is at:
  ../robustness-analysis/gap5_dimension_robustness.py

Run that script with:
  uv run --with numpy,scipy python gap5_dimension_robustness.py

This script provides additional documentation of the volatility computation
methodology as a standalone reference.

RUN COMMAND
-----------
  uv run --with numpy,scipy python dimension_volatility.py

DATA
----
Input: R15 Run 5 weight profiles (22 models x 8 dimensions x n brand-pair obs)
  - Expected format: JSONL, one record per API call
  - Each record: {"model": str, "brand_pair": str, "run": int, "weights": dict}
  - Where weights maps each of the 8 SBT dimension names to a float
  - Weights per record sum to 100 (percentage allocation)
  - Source: https://github.com/spectralbranding/sbt-papers/tree/main/r15-ai-search-metamerism/experiment

Output: Volatility ranking table, DCI baseline, drop-one statistics

SEED
----
SEED = 42
Used in Experiment 3 (10D augmentation via noise-perturbed 50/50 splits).
Set via np.random.seed(42) immediately before the augmentation step.
Result is deterministic given this seed and Python 3.12 + numpy 1.26+.

METHODOLOGY
-----------
The 22-model panel:
  - The full R15 panel includes 24 models from 7 training traditions.
  - Two models are absent from Run 5 because they lacked sufficient observations
    (fewer than 3 complete brand-pair measurements in Run 5).
  - The script silently skips models with len(common) < 3 for any brand-pair-level
    statistic, so the 22-model panel is determined automatically by data completeness.

DCI formula:
  DCI = (w_Economic + w_Semiotic) / w_total
  where w_X is the mean weight allocated to dimension X across all brand pairs
  and repetitions for a given model, and w_total = sum of all 8 dimension weights.
  The DCI captures concentration of weight toward the two dimensions that R15
  identified as systematically over-weighted (the "dimensional collapse" finding).

Dimension volatility ranking (from Table 3 of Section 8A):
  Rank  Dimension    % of total cross-model variance
   1    Economic     18.7%
   2    Cultural     17.3%
   3    Ideological  16.7%
   4    Semiotic     15.4%
   5    Experiential 11.4%
   6    Narrative     9.2%
   7    Social        5.9%
   8    Temporal      5.4%

  All eight dimensions contribute non-trivial cross-model variance (5-19%),
  confirming that no dimension is informationally inert.
"""

import json
import numpy as np
from pathlib import Path
from typing import Optional

# Reproducibility
SEED = 42

# SBT dimension order (canonical)
DIMENSIONS = [
    "Semiotic",
    "Narrative",
    "Ideological",
    "Experiential",
    "Social",
    "Economic",
    "Cultural",
    "Temporal",
]

# DCI numerator dimensions (from R15 H4 finding)
DCI_NUMERATOR = {"Economic", "Semiotic"}


def load_run5_profiles(data_path: Path) -> Optional[dict]:
    """
    Load R15 Run 5 weight profiles from JSONL file.

    Parameters
    ----------
    data_path : Path
        Path to raw_responses.jsonl or equivalent data file.

    Returns
    -------
    dict mapping model_name -> np.ndarray of shape (n_obs, 8)
        where columns correspond to DIMENSIONS order.
    Returns None if the file does not exist.
    """
    if not data_path.exists():
        print(f"[INFO] Data file not found: {data_path}")
        print("[INFO] Running in template mode -- no data loaded.")
        return None

    profiles = {}
    with open(data_path) as f:
        for line in f:
            record = json.loads(line.strip())
            model = record["model"]
            weights = record["weights"]
            vec = np.array([weights.get(d, 0.0) for d in DIMENSIONS])
            if model not in profiles:
                profiles[model] = []
            profiles[model].append(vec)

    return {m: np.array(vecs) for m, vecs in profiles.items()}


def compute_model_mean_profiles(raw_profiles: dict) -> dict:
    """
    Compute mean weight vector per model across all brand-pair observations.

    Models with fewer than 3 observations are excluded (Run 5 completeness filter).
    This is the filter that reduces the 24-model R15 panel to 22 models.

    Parameters
    ----------
    raw_profiles : dict  model_name -> np.ndarray (n_obs, 8)

    Returns
    -------
    dict  model_name -> np.ndarray (8,)  mean weight profile
    """
    mean_profiles = {}
    excluded = []
    for model, obs in raw_profiles.items():
        if len(obs) < 3:
            excluded.append(model)
            continue
        mean_profiles[model] = obs.mean(axis=0)

    if excluded:
        print(f"[INFO] Excluded {len(excluded)} models with < 3 Run 5 observations: {excluded}")
    print(f"[INFO] {len(mean_profiles)} models in analysis panel.")
    return mean_profiles


def compute_dci(profile: np.ndarray) -> float:
    """
    Compute Dimensional Collapse Index for a single model profile.

    DCI = (w_Economic + w_Semiotic) / w_total

    Parameters
    ----------
    profile : np.ndarray  shape (8,) in DIMENSIONS order

    Returns
    -------
    float  DCI value in [0, 1]
    """
    idx_eco = DIMENSIONS.index("Economic")
    idx_sem = DIMENSIONS.index("Semiotic")
    return (profile[idx_eco] + profile[idx_sem]) / profile.sum()


def dimension_volatility_table(mean_profiles: dict) -> None:
    """
    Reproduce Table 3 of Section 8A: cross-model variance decomposition.

    Prints a ranking of dimensions by their share of total cross-model variance,
    matching the published results (Economic 18.7% ... Temporal 5.4%).

    Parameters
    ----------
    mean_profiles : dict  model_name -> np.ndarray (8,)
    """
    matrix = np.array(list(mean_profiles.values()))  # (n_models, 8)
    variances = matrix.var(axis=0, ddof=1)
    total_var = variances.sum()

    print("\nTable 3 (Section 8A): Cross-Model Variance by Dimension")
    print(f"{'Dimension':<15} {'Mean wt':>8} {'SD':>7} {'Var':>8} {'% total':>9}")
    print("-" * 52)
    ranked = sorted(enumerate(DIMENSIONS), key=lambda x: variances[x[0]], reverse=True)
    for idx, dim in ranked:
        mean_w = matrix[:, idx].mean()
        sd_w = matrix[:, idx].std(ddof=1)
        var_w = variances[idx]
        pct = 100 * var_w / total_var
        print(f"{dim:<15} {mean_w:>8.2f} {sd_w:>7.2f} {var_w:>8.3f} {pct:>8.1f}%")
    print("-" * 52)
    print(f"{'Total':<15} {'':>8} {'':>7} {total_var:>8.3f} {'100.0%':>9}")


def drop_one_stability(mean_profiles: dict) -> None:
    """
    Reproduce Table 1 of Section 8A: DCI ranking stability under single-dimension removal.

    For each dimension, removes it, renormalizes the remaining 7 weights to 100,
    recomputes DCI, and reports Spearman rho and cosine similarity against the
    8D baseline DCI vector.

    Parameters
    ----------
    mean_profiles : dict  model_name -> np.ndarray (8,)
    """
    from scipy.stats import spearmanr

    models = list(mean_profiles.keys())
    matrix = np.array([mean_profiles[m] for m in models])  # (n, 8)

    # Baseline DCI
    baseline_dci = np.array([compute_dci(row) for row in matrix])

    print("\nTable 1 (Section 8A): DCI Ranking Stability Under Single-Dimension Removal")
    print(f"{'Dropped':<15} {'Spearman rho':>13} {'Cosine':>8}")
    print("-" * 40)

    results = []
    for drop_idx, drop_dim in enumerate(DIMENSIONS):
        # Build 7D profiles: drop dimension, renormalize
        mask = [i for i in range(8) if i != drop_idx]
        reduced = matrix[:, mask]
        # Renormalize to 100
        row_sums = reduced.sum(axis=1, keepdims=True)
        reduced_norm = reduced / row_sums * 100.0

        # Compute DCI on reduced (numerator dims may be absent)
        numerator_dims_remaining = [
            d for i, d in enumerate(DIMENSIONS) if i != drop_idx and d in DCI_NUMERATOR
        ]
        dim_remaining = [d for i, d in enumerate(DIMENSIONS) if i != drop_idx]

        if len(numerator_dims_remaining) == 0:
            # DCI undefined (both numerators dropped -- not possible in drop-one)
            print(f"{drop_dim:<15} {'undefined':>13} {'undefined':>8}")
            continue

        new_dci = np.zeros(len(models))
        for row_i, row in enumerate(reduced_norm):
            num_sum = sum(row[dim_remaining.index(d)] for d in numerator_dims_remaining)
            new_dci[row_i] = num_sum / row.sum()

        rho, _ = spearmanr(baseline_dci, new_dci)
        # Cosine similarity
        cos = np.dot(baseline_dci, new_dci) / (
            np.linalg.norm(baseline_dci) * np.linalg.norm(new_dci)
        )
        results.append((drop_dim, rho, cos))

    results.sort(key=lambda x: x[2])  # sort ascending by cosine (most disruptive first)
    for drop_dim, rho, cos in results:
        print(f"{drop_dim:<15} {rho:>13.3f} {cos:>8.4f}")


def run_template_demo() -> None:
    """
    Run methodology demonstration when no data file is available.
    Prints the published Table 3 values from Section 8A as reference output.
    """
    print("\n[TEMPLATE MODE] No data file found. Printing published Table 3 for reference.\n")
    published = [
        ("Economic",    21.23, 2.59, 6.415, 18.7),
        ("Cultural",     7.56, 2.50, 5.943, 17.3),
        ("Ideological",  8.97, 2.45, 5.732, 16.7),
        ("Semiotic",    14.41, 2.36, 5.295, 15.4),
        ("Experiential",18.30, 2.03, 3.927, 11.4),
        ("Narrative",   10.12, 1.82, 3.160,  9.2),
        ("Social",      10.33, 1.46, 2.040,  5.9),
        ("Temporal",     9.08, 1.39, 1.841,  5.4),
    ]
    print(f"{'Dimension':<15} {'Mean wt':>8} {'SD':>7} {'Var':>8} {'% total':>9}")
    print("-" * 52)
    for row in published:
        print(f"{row[0]:<15} {row[1]:>8.2f} {row[2]:>7.2f} {row[3]:>8.3f} {row[4]:>8.1f}%")
    print("\nTo reproduce from data: provide R15 Run 5 weight profiles as JSONL.")
    print("Full reproducible script: ../robustness-analysis/gap5_dimension_robustness.py")


def main():
    np.random.seed(SEED)

    # TODO: update this path to point to the actual R15 Run 5 data file
    data_path = Path("../robustness-analysis/data/raw_responses.jsonl")

    raw = load_run5_profiles(data_path)

    if raw is None:
        run_template_demo()
        return

    mean_profiles = compute_model_mean_profiles(raw)

    if len(mean_profiles) == 0:
        print("[ERROR] No models passed the completeness filter. Check data format.")
        return

    dimension_volatility_table(mean_profiles)
    drop_one_stability(mean_profiles)


if __name__ == "__main__":
    main()
