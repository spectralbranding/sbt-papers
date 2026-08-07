#!/usr/bin/env python3
"""concordance.py — operator/family concordance diagnostics + the
pre-registered exclusion rule.

Two diagnostics generalized from the 2026az campaign (where the exploratory
concordance table localized a systematically discordant renderer family):

- vector_concordance: per-operator mean distance to the leave-one-out mean
  reading (stated-reading side).
- pick_concordance:   per-family disagreement rate with the majority pick on
  identical trials (choice side).

The exclusion rule (frozen ex ante, PRISM-C PL0 section 9.2): an operator or
family whose discordance score exceeds RULE_MULTIPLE x the median score of
the REMAINING operators is excluded from the floor and retained only as a
reported exploratory observer. The decision is mechanical.
"""

from __future__ import annotations

from collections import Counter, defaultdict

import numpy as np

from .stats import dist_full

RULE_MULTIPLE = 3.0


def vector_concordance(readings: dict[str, list]) -> dict[str, float]:
    """readings: operator -> list of 8-d vectors (aligned across operators by
    stimulus; each list index = one stimulus). Score per operator = mean
    cosine distance between its reading and the mean of the OTHER operators'
    readings on the same stimulus."""
    ops = sorted(readings)
    n_stim = min(len(readings[o]) for o in ops)
    scores = {}
    for op in ops:
        ds = []
        for i in range(n_stim):
            others = [
                np.asarray(readings[o][i], float)
                for o in ops
                if o != op and readings[o][i] is not None
            ]
            if not others or readings[op][i] is None:
                continue
            loo_mean = np.mean(others, axis=0)
            ds.append(dist_full(readings[op][i], loo_mean))
        scores[op] = float(np.mean(ds)) if ds else float("nan")
    return scores


def pick_concordance(picks: dict[str, list]) -> dict[str, float]:
    """picks: family -> list of picks (aligned by trial). Score per family =
    rate of disagreement with the majority pick of the OTHER families."""
    fams = sorted(picks)
    n_trials = min(len(picks[f]) for f in fams)
    scores = {}
    for fam in fams:
        dis = []
        for i in range(n_trials):
            others = [picks[f][i] for f in fams if f != fam and picks[f][i] is not None]
            if not others or picks[fam][i] is None:
                continue
            majority = Counter(others).most_common(1)[0][0]
            dis.append(0.0 if picks[fam][i] == majority else 1.0)
        scores[fam] = float(np.mean(dis)) if dis else float("nan")
    return scores


def apply_exclusion_rule(
    scores: dict[str, float], multiple: float = RULE_MULTIPLE
) -> dict:
    """Mechanical application of the frozen rule: exclude any unit whose
    score > multiple x median(scores of the remaining units)."""
    excluded, kept = [], []
    for unit, s in scores.items():
        rest = [v for u, v in scores.items() if u != unit and not np.isnan(v)]
        if not rest or np.isnan(s):
            kept.append(unit)
            continue
        med = float(np.median(rest))
        if med > 0 and s > multiple * med:
            excluded.append({"unit": unit, "score": s, "median_others": med})
        else:
            kept.append(unit)
    return {
        "kept": sorted(kept),
        "excluded": excluded,
        "rule": f"score > {multiple} x median(others)",
        "scores": scores,
    }


def pairwise_disagreement_floor(picks_by_family: dict[str, list]) -> float:
    """Choice operator floor: mean pairwise disagreement rate between
    families on identical trials."""
    fams = sorted(picks_by_family)
    if not fams:
        return float("nan")
    n_trials = min(len(picks_by_family[f]) for f in fams)
    rates = []
    for i, a in enumerate(fams):
        for b in fams[i + 1 :]:
            pair = [
                (picks_by_family[a][t], picks_by_family[b][t])
                for t in range(n_trials)
                if picks_by_family[a][t] is not None
                and picks_by_family[b][t] is not None
            ]
            if pair:
                rates.append(float(np.mean([x != y for x, y in pair])))
    return float(np.mean(rates)) if rates else float("nan")


def per_family_pick_table(records: list[dict], key_fields: tuple) -> dict[str, list]:
    """Align choice records into picks_by_family over the shared trial keys.
    records: dicts with 'family', 'pick', and key_fields identifying a trial."""
    by_trial: dict = defaultdict(dict)
    for r in records:
        trial = tuple(r[k] for k in key_fields)
        by_trial[trial][r["family"]] = r.get("pick")
    fams = sorted({r["family"] for r in records})
    trials = sorted(by_trial)
    return {f: [by_trial[t].get(f) for t in trials] for f in fams}
