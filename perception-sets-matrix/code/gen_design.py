"""Seeded design generator for the 2026bf campaign (Perception Sets the Matrix).

Generates, deterministically from SEED = 20260712:
  - 30 cohort persona specifications (10 per category x 3 categories):
    observer spectral profiles by maximin Latin hypercube over [1,10]^8
    rounded to .5; per-cohort salience weight vectors (Dirichlet(1,...,1),
    normalized); natural-language persona renderings from fixed phrase banks
    (no numbers in the text - cohort-profile validation readings must recover
    the vector from the prose alone).
  - A match-coverage diagnostic: the spread of m(c,b) over Study-1
    cohort x target-profile cells (targets read from STIMULI_STUDY1.yaml).

Run:
    uv run --with scipy python code/gen_design.py

Writes ../PERSONAS.yaml (committed design artifact; regeneration is
byte-identical under the fixed seed).
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import yaml
from scipy.stats import qmc

HERE = Path(__file__).resolve().parent
PAPER_DIR = HERE.parent

SEED = 20260712
DIMENSIONS = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
]
CATEGORIES = {
    "coffee_roasters": "specialty coffee roasters (Study 1, synthetic brands)",
    "qsr_coffee": "quick-service coffee chains",
    "athletic_footwear": "athletic footwear",
}
K = 10  # cohorts per category

# Phrase banks: (low <4, mid 4-7, high >=7) per dimension, cohort-side voice.
PHRASES = {
    "semiotic": (
        "pays little attention to logos, packaging, or visual style",
        "notices design and visual identity without dwelling on it",
        "is strongly drawn to distinctive symbols, packaging, and visual craft",
    ),
    "narrative": (
        "has no patience for brand storytelling",
        "enjoys a good origin story but does not require one",
        "seeks out brands with rich stories - founders, places, journeys",
    ),
    "ideological": (
        "treats values-talk in this category as noise",
        "prefers responsible brands when the choice is otherwise equal",
        "chooses primarily by values - ethics, politics, and principles come first",
    ),
    "experiential": (
        "is indifferent to the finer points of the product experience",
        "appreciates a well-made product experience when it is offered",
        "is exacting about sensory and service quality in every detail",
    ),
    "social": (
        "does not care what their choices signal to anyone",
        "is mildly aware of what a brand choice says about them",
        "treats brand choices as social statements and badges of belonging",
    ),
    "economic": (
        "barely looks at prices in this category",
        "weighs price against quality like most careful shoppers",
        "hunts value relentlessly - price per unit is the first filter",
    ),
    "cultural": (
        "is detached from trends and cultural buzz around brands",
        "keeps an eye on what is culturally current without chasing it",
        "gravitates to brands at the center of the cultural conversation",
    ),
    "temporal": (
        "prefers the new - novelty and the latest thing over any tradition",
        "balances a taste for the established with openness to the new",
        "is devoted to heritage - age, tradition, and proven longevity matter",
    ),
}


def band(v: float) -> int:
    return 0 if v < 4.0 else (1 if v < 7.0 else 2)


def render_persona(cat_desc: str, vec: list[float], weights: list[float]) -> str:
    clauses = [PHRASES[d][band(v)] for d, v in zip(DIMENSIONS, vec)]
    top3 = sorted(range(8), key=lambda i: -weights[i])[:3]
    salient = ", then ".join(DIMENSIONS[i] for i in top3)
    body = (
        f"A cohort of {cat_desc} buyers. This cohort "
        + "; ".join(clauses[:4])
        + ". It "
        + "; ".join(clauses[4:])
        + ". When choosing in this category, the aspects that carry the most "
        f"weight for this cohort, in order, are: {salient}."
    )
    return body


def main() -> None:
    rng = np.random.default_rng(SEED)
    personas = {}
    for ci, (cat, cat_desc) in enumerate(CATEGORIES.items()):
        sampler = qmc.LatinHypercube(d=8, seed=SEED + ci)
        grid = sampler.random(K)  # in [0,1)
        vecs = np.round((1 + grid * 9) * 2) / 2  # [1,10] rounded to .5
        w = rng.dirichlet(np.ones(8), size=K).round(4)
        w = w / w.sum(axis=1, keepdims=True)
        rows = []
        for k in range(K):
            vec = [float(x) for x in vecs[k]]
            weights = [round(float(x), 4) for x in w[k]]
            rows.append(
                {
                    "cohort_id": f"{cat}_C{k+1:02d}",
                    "profile": vec,
                    "salience_weights": weights,
                    "persona_text": render_persona(cat_desc, vec, weights),
                }
            )
        personas[cat] = rows

    out = {
        "seed": SEED,
        "dimensions": DIMENSIONS,
        "note": (
            "Committed design artifact, generated by code/gen_design.py at "
            "design freeze. Persona texts contain no numbers; validation "
            "readings must recover the profile from the prose."
        ),
        "categories": personas,
    }
    (PAPER_DIR / "PERSONAS.yaml").write_text(
        yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=78)
    )
    print(f"PERSONAS.yaml written: {sum(len(v) for v in personas.values())} cohorts")

    # Match-coverage diagnostic vs Study-1 targets, if stimuli file exists.
    stim_path = PAPER_DIR / "STIMULI_STUDY1.yaml"
    if stim_path.exists():
        stim = yaml.safe_load(stim_path.read_text())
        d_max = 9 * math.sqrt(8)
        ms = []
        for c in personas["coffee_roasters"]:
            for b in stim["brands"]:
                d = math.dist(c["profile"], b["target_profile"])
                ms.append(1 - d / d_max)
        ms = np.array(ms)
        print(
            f"Study-1 match coverage over {len(ms)} cells: "
            f"min={ms.min():.3f} p25={np.percentile(ms, 25):.3f} "
            f"median={np.median(ms):.3f} p75={np.percentile(ms, 75):.3f} "
            f"max={ms.max():.3f}"
        )


if __name__ == "__main__":
    main()
