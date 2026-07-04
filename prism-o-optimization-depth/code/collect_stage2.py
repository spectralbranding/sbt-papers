#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "pyyaml>=6.0"]
# ///
"""collect_stage2.py — PRISM-O (2026bd) Stage-2 panel collection + pinning.

Implements the PANEL_MANIFEST.yaml collection protocol against SEC EDGAR —
the single, free, reproducible public source. Frozen mechanical class
mapping (documents the manifest's artifact classes onto EDGAR objects):

ENACTED (reports of executed interventions):
  - 8-K with item 2.05 (costs associated with exit or disposal activities:
    restructurings, layoffs) or 2.01 (completed acquisition/disposition);
  - 8-K item 2.02 (results) exhibits whose text matches ENACTED_RX — earnings
    releases are where executed restructurings/reorganizations are routinely
    REPORTED; the ENACTED_RX-matched REGION (±REGION_CHARS) is extracted, not
    the whole release, to keep the enacted register clean;
  - 10-Q / 10-K restructuring-note excerpt (region around the densest
    "restructur" cluster when the term appears >= 3 times) — the periodic
    report of executed exit/disposal activity;
  - FPI 6-K whose exhibit text matches ENACTED_RX (completed restructuring/
    workforce reduction/divestiture/closure language), region-extracted.
  (Mapping widened 2026-07-03 BEFORE any Stage-2 reading — two passes: the
  original 2.05/2.01-only mapping starved the channel (large firms report
  executed restructurings in 2.02 exhibits and periodic-report notes far
  more often than they trigger item 2.05); pass 2 lowered the periodic-note
  term threshold to 2 and added DEF 14A strategy regions to STATED. Same
  frozen manifest classes throughout, more EDGAR objects mapped onto them;
  zero model readings had occurred at each widening.)
STATED (strategy prose):
  - annual report (10-K / 20-F) strategy excerpt (Item 1 region);
  - 8-K item 7.01/8.01 (or 6-K) exhibits matching STATED_RX (strategy/
    transformation/vision language) and NOT matching ENACTED_RX.
The manifest's earnings_call_prepared_remarks class is NOT collected: bulk
transcripts are paywalled; the class-set channel requirement (>= 3 artifacts
from the SET) is met from the remaining classes. Documented limitation.

Organizations without EDGAR filings fail the channel requirement
mechanically -> the stratum spare enters; residual shortfalls are recorded
in the pinned manifest (the frozen selection rule anticipates this).

Output: research/prism_o/panel/<ORG>/<CHANNEL>/<artifact_id>.txt (clipped,
plain text) + research/prism_o/data/panel_pinned_manifest.json (SHA-256 per
artifact, source URL, EDGAR accession, class, date, ai_announcer flag, org
name variants for the masking arm). Re-runnable; deterministic given EDGAR
state (selection = most recent class-matched, text >= MIN_CHARS).

Run:  uv run python research/prism_o/code/collect_stage2.py
(no API keys; SEC requires a User-Agent with contact email)
"""

from __future__ import annotations

import hashlib
import html as htmllib
import json
import re
import sys
import time
from pathlib import Path

import httpx
import yaml

PRISM_O_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PRISM_O_DIR / "data"
PANEL_DIR = PRISM_O_DIR / "panel"
UA = {"User-Agent": "PRISM-O research instrument (Dmitry Zharnikov, fermeradar@gmail.com)"}
WINDOW = ("2025-07-01", "2026-06-30")
PER_CHANNEL_MAX = 5
PER_CHANNEL_MIN = 3
MIN_CHARS = 1200
CLIP_CHARS = 14000
SLEEP = 0.15

ENACTED_RX = re.compile(
    r"restructur|workforce reduction|reduction in force|layoff|lay-off|"
    r"headcount reduction|divestiture (was |has been )?complet|"
    r"completed (the )?(divestiture|reorganization|sale of)|plant closure|"
    r"exit (costs|activities)|severance",
    re.I,
)
STATED_RX = re.compile(
    r"strateg|transformation|vision|long-term plan|operating model|"
    r"reposition|roadmap",
    re.I,
)
AI_RX = re.compile(r"\bAI\b|artificial intelligence|generative", re.I)

# Frozen roster -> ticker map (PANEL_MANIFEST strata order; None = no EDGAR
# registrant -> fails channel requirement mechanically).
TICKERS: dict[str, dict[str, str | None]] = {
    "technology": {
        "Microsoft": "MSFT", "Alphabet": "GOOGL", "Amazon": "AMZN",
        "Apple": "AAPL", "Meta Platforms": "META", "Salesforce": "CRM",
        "SAP": "SAP", "Oracle": "ORCL", "IBM": "IBM", "Intel": "INTC",
        "Adobe": "ADBE",
    },
    "financials": {
        "JPMorgan Chase": "JPM", "Bank of America": "BAC", "Wells Fargo": "WFC",
        "Goldman Sachs": "GS", "Morgan Stanley": "MS", "Citigroup": "C",
        "HSBC": "HSBC", "American Express": "AXP", "Allianz": None,
        "AXA": None, "ING Groep": "ING",
    },
    "healthcare": {
        "UnitedHealth Group": "UNH", "Johnson & Johnson": "JNJ", "Pfizer": "PFE",
        "Merck": "MRK", "Novartis": "NVS", "Roche": None,
        "AstraZeneca": "AZN", "Sanofi": "SNY", "CVS Health": "CVS",
        "Medtronic": "MDT", "GSK": "GSK",
    },
    "consumer": {
        "Walmart": "WMT", "Procter & Gamble": "PG", "Coca-Cola": "KO",
        "PepsiCo": "PEP", "Unilever": "UL", "Nike": "NKE",
        "McDonald's": "MCD", "Starbucks": "SBUX", "Target": "TGT",
        "Nestle": None, "Carrefour": None,
    },
    "industrials_energy": {
        "General Electric": "GE", "Siemens": None, "Caterpillar": "CAT",
        "Boeing": "BA", "Airbus": None, "Honeywell": "HON",
        "ExxonMobil": "XOM", "Shell": "SHEL", "BP": "BP",
        "Maersk": None, "Rolls-Royce": None,
    },
    "telecom_media_utilities": {
        "AT&T": "T", "Verizon": "VZ", "Deutsche Telekom": None,
        "Comcast": "CMCSA", "Walt Disney": "DIS", "Netflix": "NFLX",
        "Vodafone": "VOD", "Telefonica": "TEF", "Enel": None,
        "NextEra Energy": "NEE", "Orange": "ORAN",
    },
}


def get(url: str) -> httpx.Response:
    time.sleep(SLEEP)
    r = httpx.get(url, headers=UA, timeout=60, follow_redirects=True)
    r.raise_for_status()
    return r


def strip_html(raw: str) -> str:
    txt = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    txt = re.sub(r"(?s)<[^>]+>", " ", txt)
    txt = htmllib.unescape(txt)
    return re.sub(r"[ \t\xa0]+", " ", re.sub(r"\s*\n\s*", "\n", txt)).strip()


def cik_map() -> dict[str, int]:
    data = get("https://www.sec.gov/files/company_tickers.json").json()
    return {row["ticker"].upper(): int(row["cik_str"]) for row in data.values()}


def submissions(cik: int) -> dict:
    return get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json").json()


def filing_docs(cik: int, accession: str) -> list[dict]:
    acc = accession.replace("-", "")
    idx = get(f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/index.json").json()
    return idx.get("directory", {}).get("item", [])


def fetch_doc(cik: int, accession: str, name: str) -> str:
    acc = accession.replace("-", "")
    raw = get(f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{name}").text
    return strip_html(raw)


def best_exhibit_text(cik: int, accession: str, primary: str) -> str:
    """Prefer EX-99 press-release exhibits; fall back to the primary doc."""
    try:
        items = filing_docs(cik, accession)
    except Exception:
        items = []
    cands = [
        i["name"]
        for i in items
        if re.search(r"ex[-_]?99|ex99|press", i.get("name", ""), re.I)
        and i.get("name", "").lower().endswith((".htm", ".html", ".txt"))
    ]
    for name in cands[:2]:
        try:
            txt = fetch_doc(cik, accession, name)
            if len(txt) >= MIN_CHARS:
                return txt
        except Exception:
            continue
    try:
        return fetch_doc(cik, accession, primary)
    except Exception:
        return ""


REGION_CHARS = 7000


def enacted_region(text: str) -> str | None:
    """Region around the densest ENACTED_RX cluster; None if no match."""
    hits = [m.start() for m in ENACTED_RX.finditer(text)]
    if not hits:
        return None
    # densest window: hit with most neighbors within REGION_CHARS
    best = max(hits, key=lambda h: sum(1 for x in hits if abs(x - h) < REGION_CHARS))
    start = max(0, best - REGION_CHARS // 2)
    return text[start : start + REGION_CHARS * 2]


def strategy_excerpt(text: str) -> str:
    """Item-1 region of an annual report: from the first business/strategy
    marker past the table of contents to CLIP_CHARS."""
    low = text.lower()
    for marker in ("item 1. business", "item 1.business", "item 4. information",
                   "our strategy", "business overview", "item 1 business"):
        pos = low.find(marker, 3000)  # skip the table of contents
        if pos != -1:
            return text[pos : pos + CLIP_CHARS]
    return text[3000 : 3000 + CLIP_CHARS]


def collect_org(org: str, ticker: str, cik: int) -> dict:
    sub = submissions(cik)
    rec = sub["filings"]["recent"]
    rows = [
        {
            "form": rec["form"][i],
            "date": rec["filingDate"][i],
            "accession": rec["accessionNumber"][i],
            "primary": rec["primaryDocument"][i],
            "items": rec.get("items", [""] * len(rec["form"]))[i],
        }
        for i in range(len(rec["form"]))
        if WINDOW[0] <= rec["filingDate"][i] <= WINDOW[1]
    ]
    stated, enacted = [], []

    # annual report strategy excerpt (most recent in window)
    for row in sorted(rows, key=lambda r: r["date"], reverse=True):
        if row["form"] in ("10-K", "20-F"):
            txt = fetch_doc(cik, row["accession"], row["primary"])
            exc = strategy_excerpt(txt)
            if len(exc) >= MIN_CHARS:
                stated.append(
                    {"cls": "mission_strategy_section", "text": exc, **row}
                )
            # same annual report may carry the restructuring note (ENACTED)
            reg = enacted_region(txt)
            if reg and len(ENACTED_RX.findall(txt)) >= 3 and len(reg) >= MIN_CHARS:
                enacted.append({"cls": "restructuring_filing", "text": reg, **row})
            break

    # periodic reports (10-Q): restructuring-note excerpts (ENACTED;
    # threshold >= 2 term hits — >= 3 starved low-restructuring filers)
    for row in sorted(rows, key=lambda r: r["date"], reverse=True):
        if len(enacted) >= PER_CHANNEL_MAX:
            break
        if row["form"] == "10-Q":
            try:
                txt = fetch_doc(cik, row["accession"], row["primary"])
            except Exception:
                continue
            if len(ENACTED_RX.findall(txt)) >= 2:
                reg = enacted_region(txt)
                if reg and len(reg) >= MIN_CHARS:
                    enacted.append({"cls": "restructuring_filing", "text": reg, **row})

    # proxy statement (DEF 14A): strategy region (STATED — the letter-to-
    # shareholders / strategy discussion is mission_strategy_section prose)
    if len(stated) < PER_CHANNEL_MAX:
        for row in sorted(rows, key=lambda r: r["date"], reverse=True):
            if row["form"] == "DEF 14A":
                try:
                    txt = fetch_doc(cik, row["accession"], row["primary"])
                except Exception:
                    break
                hits = [m.start() for m in STATED_RX.finditer(txt)]
                if len(hits) >= 3:
                    best = max(hits, key=lambda h: sum(1 for x in hits if abs(x - h) < REGION_CHARS))
                    reg = txt[max(0, best - REGION_CHARS // 2) : best + REGION_CHARS]
                    if len(reg) >= MIN_CHARS:
                        stated.append({"cls": "mission_strategy_section", "text": reg, **row})
                break

    # 8-K item-coded + press-release classes
    for row in sorted(rows, key=lambda r: r["date"], reverse=True):
        items = row["items"] or ""
        if row["form"] == "8-K" and ("2.05" in items or "2.01" in items):
            if len(enacted) >= PER_CHANNEL_MAX:
                continue
            txt = best_exhibit_text(cik, row["accession"], row["primary"])
            if len(txt) >= MIN_CHARS:
                cls = "restructuring_filing" if "2.05" in items else "executed_reorganization_report"
                enacted.append({"cls": cls, "text": txt[:CLIP_CHARS], **row})
        elif row["form"] in ("8-K", "6-K") and (
            "7.01" in items or "8.01" in items or "2.02" in items or row["form"] == "6-K"
        ):
            if len(stated) >= PER_CHANNEL_MAX and len(enacted) >= PER_CHANNEL_MAX:
                continue
            txt = best_exhibit_text(cik, row["accession"], row["primary"])
            if len(txt) < MIN_CHARS:
                continue
            is_results = "2.02" in items
            if ENACTED_RX.search(txt) and len(enacted) < PER_CHANNEL_MAX:
                reg = enacted_region(txt)
                if reg and len(reg) >= MIN_CHARS:
                    enacted.append({"cls": "executed_reorganization_report", "text": reg, **row})
            elif (
                not is_results
                and STATED_RX.search(txt[:6000])
                and len(stated) < PER_CHANNEL_MAX
            ):
                stated.append({"cls": "transformation_announcement", "text": txt[:CLIP_CHARS], **row})
        if len(stated) >= PER_CHANNEL_MAX and len(enacted) >= PER_CHANNEL_MAX:
            break

    ai_flag = any(
        a["cls"] == "transformation_announcement" and AI_RX.search(a["text"][:6000])
        for a in stated
    )
    return {"org": org, "ticker": ticker, "cik": cik, "STATED": stated[:PER_CHANNEL_MAX],
            "ENACTED": enacted[:PER_CHANNEL_MAX], "ai_announcer": ai_flag}


def main() -> int:
    ciks = cik_map()
    manifest = {"collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "window": WINDOW, "protocol": "EDGAR mechanical mapping (module docstring)",
                "orgs": [], "excluded": [], "strata_shortfall": {}}
    for stratum, roster in TICKERS.items():
        names = list(roster)
        primaries, spare = names[:10], names[10]
        entered = 0
        queue = primaries + [spare]
        for org in queue:
            if entered >= 10:
                break
            ticker = roster[org]
            if ticker is None or ticker.upper() not in ciks:
                manifest["excluded"].append({"org": org, "reason": "no EDGAR registrant"})
                print(f"[skip] {org}: no EDGAR registrant", flush=True)
                continue
            try:
                result = collect_org(org, ticker, ciks[ticker.upper()])
            except Exception as exc:  # noqa: BLE001
                manifest["excluded"].append({"org": org, "reason": f"collection error: {exc}"})
                print(f"[skip] {org}: {exc}", flush=True)
                continue
            n_s, n_e = len(result["STATED"]), len(result["ENACTED"])
            if n_s < PER_CHANNEL_MIN or n_e < PER_CHANNEL_MIN:
                manifest["excluded"].append(
                    {"org": org, "reason": f"channel requirement unmet (S={n_s}, E={n_e})"}
                )
                print(f"[skip] {org}: S={n_s} E={n_e} < {PER_CHANNEL_MIN}", flush=True)
                continue
            org_entry = {"org": org, "ticker": result["ticker"], "cik": result["cik"],
                         "stratum": stratum, "ai_announcer": result["ai_announcer"],
                         "name_variants": [org, result["ticker"]], "artifacts": []}
            for channel in ("STATED", "ENACTED"):
                for j, a in enumerate(result[channel]):
                    aid = f"{channel[:1]}{j+1}"
                    p = PANEL_DIR / org.replace(" ", "_").replace("&", "and") / channel / f"{aid}.txt"
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(a["text"])
                    org_entry["artifacts"].append(
                        {"artifact_id": aid, "channel": channel, "class": a["cls"],
                         "form": a["form"], "date": a["date"], "accession": a["accession"],
                         "sha256": hashlib.sha256(a["text"].encode()).hexdigest(),
                         "chars": len(a["text"]),
                         "path": str(p.relative_to(PRISM_O_DIR))}
                    )
            manifest["orgs"].append(org_entry)
            entered += 1
            print(f"[ok] {org} ({stratum}): S={n_s} E={n_e} ai={result['ai_announcer']}", flush=True)
        manifest["strata_shortfall"][stratum] = 10 - entered
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "panel_pinned_manifest.json").write_text(json.dumps(manifest, indent=2))
    n = len(manifest["orgs"])
    print(f"[panel] {n} organizations pinned; shortfalls {manifest['strata_shortfall']}")
    return 0 if n >= 40 else 1


if __name__ == "__main__":
    sys.exit(main())
