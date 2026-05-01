#!/usr/bin/env python3
"""
R10 -- Competitive Interference Test (250 API calls)

Tests whether competitor category (direct / adjacent / distant) modulates the
spectral profile of 5 SBT canonical brands.

Usage (OpenAI):
    OPENAI_API_KEY=sk-... uv run --with "openai,scipy,numpy" python competitive_interference_250.py

Usage (Anthropic fallback -- used automatically if OPENAI_API_KEY is unset):
    ANTHROPIC_API_KEY=sk-ant-... uv run --with "anthropic,scipy,numpy" python competitive_interference_250.py

Output:
    data/raw_responses.jsonl  -- every API call captured
    data/results.json         -- summary stats per (brand, dimension, comparison)

Fixed seed: numpy seed 42 set before analysis (API calls are stochastic by design).
"""
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

TEMPERATURE = 0.7
REPS = 16  # 5 brands x 3 categories x 16 reps = 240 calls

DIMENSIONS = [
    "Semiotic", "Narrative", "Ideological", "Experiential",
    "Social", "Economic", "Cultural", "Temporal",
]

CONDITIONS = {
    "Hermes": {
        "direct":   "Louis Vuitton",
        "adjacent": "Chanel",
        "distant":  "Rolex",
    },
    "IKEA": {
        "direct":   "Ashley Furniture",
        "adjacent": "West Elm",
        "distant":  "Target",
    },
    "Patagonia": {
        "direct":   "REI Co-op",
        "adjacent": "The North Face",
        "distant":  "Allbirds",
    },
    "Erewhon": {
        "direct":   "Whole Foods",
        "adjacent": "Sprouts",
        "distant":  "Equinox",
    },
    "Tesla": {
        "direct":   "Lucid Motors",
        "adjacent": "Rivian",
        "distant":  "Porsche",
    },
}

PROMPT = """You are a brand-perception observer. Allocate exactly 100 points across the eight Spectral Brand Theory dimensions to characterize {focal} when evaluated alongside its competitor {competitor}.

Dimensions:
1. Semiotic -- symbolic / sign-based identity
2. Narrative -- storytelling / brand mythology
3. Ideological -- values / convictions / moral stance
4. Experiential -- sensory / functional / product attributes
5. Social -- community / belonging / identity-signaling
6. Economic -- price / value / accessibility
7. Cultural -- heritage / regional / generational embedding
8. Temporal -- history / age / continuity

Higher points = more salient for {focal} when contrasted with {competitor}. Your allocations must sum to exactly 100.

Output JSON only with the eight dimension names as keys (capitalized as above) and integer point allocations as values. No explanation."""


def parse_response(text):
    t = text.strip()
    if t.startswith("```"):
        lines = t.split("\n")
        inner = []
        for line in lines:
            if line.startswith("```"):
                continue
            inner.append(line)
        t = "\n".join(inner).strip()
    if t.lower().startswith("json"):
        t = t[4:].strip()
    obj = json.loads(t)
    # Build a case-insensitive lookup
    obj_lower = {k.lower(): v for k, v in obj.items()}
    weights = {}
    for d in DIMENSIONS:
        # Try exact match first, then case-insensitive
        if d in obj:
            weights[d] = int(obj[d])
        elif d.lower() in obj_lower:
            weights[d] = int(obj_lower[d.lower()])
        else:
            weights[d] = 0
    return weights, obj  # return raw obj for diagnostics


def call_openai(client, focal, competitor, model):
    prompt = PROMPT.format(focal=focal, competitor=competitor)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        max_tokens=400,
    )
    return resp.choices[0].message.content


def call_anthropic(client, focal, competitor, model):
    prompt = PROMPT.format(focal=focal, competitor=competitor)
    resp = client.messages.create(
        model=model,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def main():
    # Determine provider
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    if openai_key:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        model = "gpt-4o-mini"
        provider = "openai"
        call_fn = lambda focal, competitor: call_openai(client, focal, competitor, model)
        print(f"Using OpenAI ({model})", flush=True)
    elif anthropic_key:
        import anthropic as anthropic_sdk
        client = anthropic_sdk.Anthropic(api_key=anthropic_key)
        model = "claude-haiku-4-5-20251001"
        provider = "anthropic"
        call_fn = lambda focal, competitor: call_anthropic(client, focal, competitor, model)
        print(f"Using Anthropic ({model})", flush=True)
    else:
        print("ERROR: Set OPENAI_API_KEY or ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)

    raw_path = DATA / "raw_responses.jsonl"
    raw_f = raw_path.open("w")

    records = []
    total = 0
    errors = 0
    for focal, competitors in CONDITIONS.items():
        for category, competitor in competitors.items():
            for rep in range(REPS):
                try:
                    text = call_fn(focal, competitor)
                    weights, raw_obj = parse_response(text)
                    rec = {
                        "focal": focal, "competitor": competitor,
                        "category": category, "rep": rep,
                        "weights": weights,
                        "raw_obj": raw_obj,
                        "raw_text": text,
                        "model": model,
                        "provider": provider,
                    }
                    records.append(rec)
                    raw_f.write(json.dumps(rec) + "\n")
                    raw_f.flush()
                    total += 1
                    if total % 20 == 0:
                        print(f"  ...{total} calls done", flush=True)
                except Exception as e:
                    errors += 1
                    print(f"FAILED ({focal}/{category}/rep{rep}): {e}", file=sys.stderr)
                time.sleep(0.1)
    raw_f.close()
    print(f"Total calls: {total} ({errors} errors)", flush=True)

    # Analysis -- per-brand x per-dimension one-way ANOVA across 3 competitor categories
    np.random.seed(42)  # fixed seed for reproducibility of any bootstrap steps

    by_focal_dim = {}
    for r in records:
        focal = r["focal"]
        cat = r["category"]
        for d, v in r["weights"].items():
            by_focal_dim.setdefault((focal, d), {}).setdefault(cat, []).append(v)

    anovas = []
    for (focal, d), groups in by_focal_dim.items():
        if len(groups) < 3 or any(len(v) < 2 for v in groups.values()):
            continue
        g_direct = groups.get("direct", [])
        g_adjacent = groups.get("adjacent", [])
        g_distant = groups.get("distant", [])
        if not (g_direct and g_adjacent and g_distant):
            continue
        g = [g_direct, g_adjacent, g_distant]
        F, p = stats.f_oneway(*g)
        # Compute largest pairwise Cohen's d
        ds = []
        pairs = [(g_direct, g_adjacent), (g_direct, g_distant), (g_adjacent, g_distant)]
        pair_names = ["direct-vs-adjacent", "direct-vs-distant", "adjacent-vs-distant"]
        for (a, b), name in zip(pairs, pair_names):
            pooled = ((np.std(a, ddof=1)**2 + np.std(b, ddof=1)**2) / 2) ** 0.5
            if pooled == 0:
                continue
            d_val = abs(np.mean(a) - np.mean(b)) / pooled
            ds.append({"pair": name, "d": float(d_val)})
        max_d = max((x["d"] for x in ds), default=0.0)
        df1 = 2
        df2 = sum(len(v) for v in g) - 3
        anovas.append({
            "focal": focal, "dimension": d,
            "F": float(F), "df1": df1, "df2": df2, "p": float(p),
            "max_pairwise_d": float(max_d),
            "pairwise_ds": ds,
            "n_per_group": [len(v) for v in g],
        })

    n_tests = len(anovas)
    bonf_alpha = 0.05 / n_tests if n_tests else 0.05
    n_signif = sum(1 for a in anovas if a["p"] < bonf_alpha)
    if anovas:
        largest = max(anovas, key=lambda a: a["max_pairwise_d"])
    else:
        largest = {}

    summary = {
        "n_calls_total": total,
        "n_errors": errors,
        "model": model,
        "provider": provider,
        "temperature": TEMPERATURE,
        "reps_per_condition": REPS,
        "n_brands": len(CONDITIONS),
        "n_categories": 3,
        "n_tests": n_tests,
        "bonferroni_alpha": bonf_alpha,
        "n_significant_after_bonferroni": n_signif,
        "largest_effect": largest,
        "all_anovas": anovas,
    }
    out_path = DATA / "results.json"
    out_path.write_text(json.dumps(summary, indent=2))

    # Print summary without the verbose all_anovas list
    brief = {k: v for k, v in summary.items() if k != "all_anovas"}
    print("\n=== RESULTS SUMMARY ===")
    print(json.dumps(brief, indent=2))
    print(f"\nFull results saved to: {out_path}")


if __name__ == "__main__":
    main()
