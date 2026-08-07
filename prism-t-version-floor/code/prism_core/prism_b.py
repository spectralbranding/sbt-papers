#!/usr/bin/env python3
"""prism_b.py — the shared PRISM-B stated-reading instrument.

The eight-dimension construct, the renderer/extractor prompt set, and the
dimension parser. This is the stated-reading layer every PRISM campaign
reuses unchanged (PRISM-M 2026az used it verbatim as its dims readout;
PRISM-C reuses it for brand stated readings AND need-vector elicitation).

Provenance: extracted verbatim from code/prism_m_lib.py
(2026az, commit dc75b6f5). Prompt wording is FROZEN — changing it forks the
instrument version.
"""

from __future__ import annotations

from .provider import parse_json_block

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

RENDERER_SYSTEM = (
    "You are an observer of brands as they appear through public artifacts. "
    "You describe what an attentive member of the public would perceive of a "
    "brand through ONE specific channel of its public presence, based on the "
    "brand's publicly observable artifacts in that channel as reflected in "
    "your knowledge. You do not have and must not assume any internal or "
    "ground-truth brand information. Write plain analytical prose. Do not "
    "score, rate, or rank; describe."
)

RENDERER_USER_TMPL = (
    "Brand (nominative reference only): {brand}\n"
    "Category: {category}\n"
    "Observation channel: {channel_desc}\n\n"
    "In 250-400 words of analytical prose, describe what this channel "
    "conveys about the brand's perceived: symbols and visual identity; story "
    "and narrative; values and ideology; product/service experience; social "
    "meaning and community; price/value positioning; cultural presence; and "
    "relationship to time (heritage vs novelty). Cover each aspect at least "
    "briefly; ground every claim in the kind of public material this channel "
    "contains."
)

EXTRACTOR_SYSTEM = (
    "You convert analytical prose about a brand's public perception into a "
    "strict structured score sheet. You see ONLY the prose below. You have no "
    "other knowledge of the brand and must not add any. Score conservatively "
    "from the prose. Output JSON only, no code fences, no commentary."
)

EXTRACTOR_USER_TMPL = (
    "Read the prose and emit JSON with EXACTLY these keys, each a float 0-10 "
    "(intensity of the perception on that dimension as conveyed by the "
    "prose):\n\n"
    '{{"semiotic": <f>, "narrative": <f>, "ideological": <f>, '
    '"experiential": <f>, "social": <f>, "economic": <f>, "cultural": <f>, '
    '"temporal": <f>}}\n\n'
    "semiotic=symbols/visual identity; narrative=story; ideological=values; "
    "experiential=product/service experience; social=social meaning/community; "
    "economic=price/value positioning; cultural=cultural presence; "
    "temporal=heritage/time relationship.\n\nProse to score:\n{prose}"
)


def parse_dims(raw: str) -> list[float]:
    d = parse_json_block(raw)
    vec = [float(d[k]) for k in DIMENSIONS]
    if not all(0.0 <= v <= 10.0 for v in vec):
        raise ValueError(f"dimension out of range: {vec}")
    return vec
