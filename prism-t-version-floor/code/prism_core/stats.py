#!/usr/bin/env python3
"""stats.py — shared statistical machinery for PRISM PL4 estimators.

Distances, max-pairwise dispersion floors, the seeded source-cluster
bootstrap, and Holm correction. Provenance: generalized from
code/estimator.py (2026az, commit dc75b6f5).
"""

from __future__ import annotations

import itertools
from collections.abc import Callable, Sequence

import numpy as np

FLOOR_MIN = 1e-3


def dist_full(a, b, metric: str = "cosine", vi=None) -> float:
    """Distance between two eight-dimension vectors."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if metric == "cosine":
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na == 0 or nb == 0:
            return 1.0
        return float(1.0 - np.dot(a, b) / (na * nb))
    if metric == "euclidean":
        return float(np.linalg.norm(a - b) / np.sqrt(len(a) * 100.0))
    if metric == "mahalanobis":
        d = a - b
        return float(np.sqrt(d @ vi @ d) / np.sqrt(len(a)))
    raise ValueError(metric)


def dist_scalar(a, b) -> float:
    return float(abs(float(a) - float(b)))


def max_pairwise_dispersion(values: Sequence, dist: Callable = dist_scalar) -> float:
    """Dispersion floor: max pairwise distance among replicate values,
    lower-bounded by FLOOR_MIN. The generic form of the 2026az operator
    floor (values = one reading per operator pair / family)."""
    vals = [v for v in values if v is not None]
    if len(vals) < 2:
        return FLOOR_MIN
    return max(max(dist(x, y) for x, y in itertools.combinations(vals, 2)), FLOOR_MIN)


def cluster_bootstrap(
    clusters: Sequence,
    statistic: Callable[[list], float | None],
    *,
    n_boot: int = 2000,
    seed: int,
) -> tuple[float | None, float | None]:
    """Source-cluster bootstrap percentile 95% CI of a statistic.

    clusters : the resampling units (e.g. scenarios, brands); resampled with
               replacement per replicate.
    statistic: maps a resampled cluster list -> float (or None to skip the
               replicate).
    """
    rng = np.random.default_rng(seed)
    clusters = list(clusters)
    boots = []
    for _ in range(n_boot):
        sample = [clusters[i] for i in rng.integers(0, len(clusters), len(clusters))]
        v = statistic(sample)
        if v is not None and not (isinstance(v, float) and np.isnan(v)):
            boots.append(v)
    if not boots:
        return (None, None)
    arr = np.asarray(boots, float)
    return (float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5)))


def holm(pvals: dict) -> dict:
    """Holm step-down adjustment; returns adjusted p per key."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    adj, running = {}, 0.0
    for i, (k_, p) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))
        adj[k_] = running
    return adj


def participation_ratio(weights: Sequence[float]) -> float:
    """Effective dimensionality of a weight vector: (sum|w|)^2 / (n*sum w^2),
    scaled to [1/n, 1]*n -> returns the effective number of dimensions in
    [1, n]. Used by the M1 (decision-subspace collapse) contrast."""
    w = np.abs(np.asarray(weights, float))
    if not w.any():
        return float(len(w))
    return float((w.sum() ** 2) / (w**2).sum())
