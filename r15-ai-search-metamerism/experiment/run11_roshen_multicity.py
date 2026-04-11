#!/usr/bin/env python3
"""Run 11 — Roshen Multi-City Geopolitical Framing Extension.

Extends the H12 Roshen test from a 2-city design (Moscow/Kyiv) to a
7-city design that separates three confounded variables in the original:
geopolitical alignment, operational anchor, and discourse density.

DESIGN

The original H12 Roshen pair (Run 7) compared Moscow vs Kyiv and showed
the largest framing effect in the dataset. But "Moscow vs Kyiv" conflates:

  1. Geopolitical alignment    (Russian context vs Ukrainian context)
  2. Manufacturing anchor      (factory presence vs commercial-distribution-only presence)
  3. Discourse density         (sanitized foreign coverage vs rich domestic coverage)

Run 11 adds five cities with different combinations of these properties,
so the experiment can distinguish them empirically:

| City     | Country   | Roshen relationship                          | Geopolitics       |
|----------|-----------|----------------------------------------------|-------------------|
| Moscow   | Russia    | Lipetsk factory nationalized 2024 (defunct) | Conflict / hostile|
| Kyiv     | Ukraine   | Home market; founded 1996                    | Home              |
| Vilnius  | Lithuania | Klaipėda Confectionery Factory ~15,500 t/yr — largest non-Ukraine manufacturing operation | EU / NATO / Ukraine-aligned |
| Warsaw   | Poland    | Active commercial distribution: Roshen-Polska Sp. z o.o. (registered 2001, Jarosław) + Roshen Europe Sp. z o.o. (Warsaw); no manufacturing in Poland | EU / NATO / Ukraine-aligned |
| Astana   | Kazakhstan| Sales representative office (Almaty); no manufacturing | Mixed; CIS member |
| Tbilisi  | Georgia   | Distributor (Roshen Georgia, Tbilisi); no manufacturing | Mixed; EU candidate |
| Baku     | Azerbaijan| Shops/distributors only; no manufacturing | Mixed; CSTO observer|

OPERATIONAL NOTE — only Lithuania (Klaipėda factory) hosts actual
manufacturing outside Ukraine within the city set tested. Hungary's
Budapest plant (Bonbonetti Choco) ceased production in 2023; Russia's
Lipetsk factory was nationalized in 2024. Poland (Warsaw + Jarosław)
has active commercial distribution via Roshen-Polska Sp. z o.o. and
Roshen Europe Sp. z o.o., covering candy / chocolate / wafer / biscuit /
jelly segments through importers and specialty retailers — but no
manufacturing line. Astana, Tbilisi, and Baku host commercial operations
only (sales offices, distributors, retail) — no manufacturing. The
contrast is therefore "manufacturing presence (Vilnius via Klaipėda) vs
commercial-distribution presence (Warsaw)", not "factory vs nothing".

This separation enables the following contrasts:

- Vilnius vs Warsaw: factory anchor effect, holding EU/NATO alignment fixed
- Vilnius vs Astana/Tbilisi/Baku: factory vs sales-only commercial presence
- Astana/Tbilisi/Baku vs Moscow: post-USSR neutrality vs post-USSR hostility
- All vs Kyiv: discourse density baseline (home market)
- All English vs all native: H12 × H10 interaction at scale

NATIVE LANGUAGE PROTOCOL

Each city is prompted in BOTH English and the local national language,
to test whether the H12 framing effect interacts with H10 (native
language). Astana receives THREE conditions: English, Kazakh (state
language), and Russian (widely spoken in Astana and the lingua franca
of Kazakh urban commerce). All other cities get two conditions
(English + the one national language).

Languages used:
- ru (Russian)        — Moscow + Astana
- uk (Ukrainian)      — Kyiv
- lt (Lithuanian)     — Vilnius
- pl (Polish)         — Warsaw
- kk (Kazakh)         — Astana
- ka (Georgian)       — Tbilisi
- az (Azerbaijani)    — Baku

Total conditions: 7 cities × 2 langs + 1 (Astana extra) = 15.

EXPERIMENT VOLUME

15 conditions × 7 models × 3 runs = 315 calls
Estimated cost: under $1.00 (most calls are local Ollama or cheap cloud)
Wall-clock: 30-60 minutes (network-bound)

MODEL PANEL

Same 7-model panel as Run 10:
- claude / gpt / gemini / deepseek / qwen3_local / gemma4_local / yandexgpt_pro

OUTPUT

L3_sessions/run11_roshen_multicity.jsonl     — raw session log
L4_analysis/run11_roshen_multicity_results.json — aggregated DCI per (city, lang, model)
L4_analysis/run11_roshen_multicity_summary.md   — human-readable comparison tables

USAGE

    cd experiment
    .venv/bin/python run11_roshen_multicity.py --demo    # offline dry run
    .venv/bin/python run11_roshen_multicity.py --smoke   # 1 city × 7 models × 1 run
    .venv/bin/python run11_roshen_multicity.py --live    # full experiment
    .venv/bin/python run11_roshen_multicity.py --analyze-only  # re-aggregate
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import time
from pathlib import Path
from statistics import mean
from typing import Any

# Reuse the main script's API callers, parser, and prompt template.
sys.path.insert(0, str(Path(__file__).parent))
import ai_search_metamerism as asm  # noqa: E402


# ----------------------------------------------------------------------------
# Gemini truncation fix: monkey-patch a high-token caller for Run 11
# ----------------------------------------------------------------------------
# Gemini 2.5 Flash counts thinking tokens against max_output_tokens. With the
# default 2048-token budget, framing prompts often leave too few tokens for
# the actual JSON response and truncate mid-output. Fix: bump to 8192 and
# disable thinking via thinking_budget=0 for this run only.

def _call_gemini_run11(prompt: str, model: str = "gemini-2.5-flash") -> str:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    cfg_kwargs: dict[str, Any] = {
        "temperature": asm.EXPERIMENT_TEMPERATURE,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
        "system_instruction": (
            "You are a brand research assistant. Respond with valid JSON only."
        ),
    }
    # Disable thinking budget if the SDK supports it (Gemini 2.5 series)
    try:
        cfg_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
    except Exception:
        pass

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(**cfg_kwargs),
        )
        text = response.text
        if text and text.strip():
            return text
    except Exception:
        pass

    # Fallback: standard call without JSON mode
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=asm.EXPERIMENT_TEMPERATURE,
            max_output_tokens=8192,
        ),
    )
    try:
        text = response.text
    except Exception:
        if response.candidates:
            text = response.candidates[0].content.parts[0].text
        else:
            raise ValueError("Gemini returned no usable response candidates")
    return text


# Patch Gemini in the API caller registry for Run 11 only.
asm.API_CALLERS["gemini"] = _call_gemini_run11

EXPERIMENT_DIR = Path(__file__).resolve().parent
L3_DIR = EXPERIMENT_DIR / "L3_sessions"
L4_DIR = EXPERIMENT_DIR / "L4_analysis"
OUT_LOG = L3_DIR / "run11_roshen_multicity.jsonl"
OUT_RESULTS = L4_DIR / "run11_roshen_multicity_results.json"
OUT_SUMMARY = L4_DIR / "run11_roshen_multicity_summary.md"

DIMENSIONS = [
    "semiotic", "narrative", "ideological", "experiential",
    "social", "economic", "cultural", "temporal",
]

BRAND = "Roshen"
PRODUCT = "chocolate"

# ----------------------------------------------------------------------------
# City × language conditions
# ----------------------------------------------------------------------------

# Each tuple: (city_name, country_code, [list of language codes])
# The "en" English condition is always included as the baseline.
CITY_CONDITIONS: list[tuple[str, str, list[str]]] = [
    ("Moscow",  "RU", ["en", "ru"]),
    ("Kyiv",    "UA", ["en", "uk"]),
    ("Vilnius", "LT", ["en", "lt"]),
    ("Warsaw",  "PL", ["en", "pl"]),
    ("Astana",  "KZ", ["en", "kk", "ru"]),  # Kazakh (state) + Russian (widespread)
    ("Tbilisi", "GE", ["en", "ka"]),
    ("Baku",    "AZ", ["en", "az"]),
]


# Roshen operational status per city (used in summary, not in prompt)
CITY_OPERATIONAL_STATUS: dict[str, str] = {
    "Moscow":  "Lipetsk factory nationalized 2024 (defunct)",
    "Kyiv":    "Home market; founded 1996; multiple Kyiv factories",
    "Vilnius": "Klaipėda Confectionery Factory ~15,500 t/yr (largest non-Ukraine manufacturing)",
    "Warsaw":  "No factory in Poland; active commercial distribution via Roshen-Polska Sp. z o.o. (Jarosław) + Roshen Europe Sp. z o.o. (Warsaw)",
    "Astana":  "Sales representative office (Almaty); no manufacturing",
    "Tbilisi": "Roshen Georgia distributor (Tbilisi); no manufacturing",
    "Baku":    "Shops/distributors in Khirdalan; no manufacturing",
}


# ----------------------------------------------------------------------------
# Native dimension descriptions for languages NOT yet in
# ai_search_metamerism.NATIVE_DIMENSION_DESCRIPTIONS (lt, pl, kk, ka, az)
# ----------------------------------------------------------------------------

# These are referenced as plain native-speaker descriptors. Quality bar:
# good enough that a fluent reader recognises the dimension; not literary.

LOCAL_NATIVE_DIM_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "lt": {
        "semiotic": "Vizualinis identitetas, logotipas, dizainas, įpakavimas",
        "narrative": "Prekės ženklo istorija, įkūrimo pasakojimas, paskirtis",
        "ideological": "Vertybės, etika, socialinė pozicija, tvarumas",
        "experiential": "Klientų patirties kokybė, aptarnavimas, įpakavimo atidarymas",
        "social": "Socialiniai signalai, bendruomenė, ką reiškia turėti šį prekės ženklą",
        "economic": "Kaina, vertė už pinigus, kainodaros strategija",
        "cultural": "Kultūrinė reikšmė, sąsajos su tradicijomis ir judėjimais",
        "temporal": "Paveldas, istorija, ryšys su laiku",
    },
    "pl": {
        "semiotic": "Tożsamość wizualna, logo, wzornictwo, opakowanie",
        "narrative": "Historia marki, opowieść założycielska, misja",
        "ideological": "Wartości, etyka, postawa społeczna, zrównoważony rozwój",
        "experiential": "Jakość doświadczenia klienta, obsługa, rozpakowywanie",
        "social": "Sygnały społeczne, wspólnota, znaczenie posiadania marki",
        "economic": "Cena, wartość za pieniądze, strategia cenowa",
        "cultural": "Znaczenie kulturowe, powiązania z tradycjami i ruchami",
        "temporal": "Dziedzictwo, historia, związek z czasem",
    },
    "kk": {
        "semiotic": "Көрнекі бейне, логотип, дизайн, орам",
        "narrative": "Бренд тарихы, негізін қалаушы оқиға, мақсат",
        "ideological": "Құндылықтар, этика, әлеуметтік ұстаным, тұрақтылық",
        "experiential": "Тұтынушы тәжірибесінің сапасы, қызмет, қаптаманы ашу",
        "social": "Әлеуметтік белгілер, қауымдастық, бренд иеленудің мағынасы",
        "economic": "Баға, ақшаға тұратын құн, баға стратегиясы",
        "cultural": "Мәдени маңыз, дәстүрлермен және қозғалыстармен байланыс",
        "temporal": "Мұра, тарих, уақытпен байланыс",
    },
    "ka": {
        "semiotic": "ვიზუალური იდენტობა, ლოგო, დიზაინი, შეფუთვა",
        "narrative": "ბრენდის ისტორია, დამფუძნებლის ნარატივი, მიზანი",
        "ideological": "ღირებულებები, ეთიკა, სოციალური პოზიცია, მდგრადობა",
        "experiential": "მომხმარებლის გამოცდილების ხარისხი, მომსახურება, შეფუთვის გახსნა",
        "social": "სოციალური სიგნალები, საზოგადოება, ბრენდის ფლობის მნიშვნელობა",
        "economic": "ფასი, ფულის ღირებულება, ფასების სტრატეგია",
        "cultural": "კულტურული მნიშვნელობა, ტრადიციებთან და მოძრაობებთან კავშირები",
        "temporal": "მემკვიდრეობა, ისტორია, დროსთან კავშირი",
    },
    "az": {
        "semiotic": "Vizual identifikasiya, loqo, dizayn, qablaşdırma",
        "narrative": "Brendin tarixi, qurucu hekayəsi, məqsəd",
        "ideological": "Dəyərlər, etika, sosial mövqe, davamlılıq",
        "experiential": "Müştəri təcrübəsinin keyfiyyəti, xidmət, qutunu açma",
        "social": "Sosial siqnallar, icma, brendə sahib olmağın mənası",
        "economic": "Qiymət, pulun dəyəri, qiymət strategiyası",
        "cultural": "Mədəni əhəmiyyət, ənənələr və hərəkatlarla əlaqələr",
        "temporal": "İrs, tarix, zamanla əlaqə",
    },
}


def dim_block_for_lang(lang: str) -> str:
    """Return the 8-dimension block in the requested language.
    Falls back to English if the language is unknown."""
    if lang == "en":
        return asm._dim_block()
    # Try the main script's native dim descriptions first
    if lang in asm.NATIVE_DIMENSION_DESCRIPTIONS:
        return asm._dim_block_native(lang)
    # Then fall back to Run 11's local native descriptions
    if lang in LOCAL_NATIVE_DIM_DESCRIPTIONS:
        descs = LOCAL_NATIVE_DIM_DESCRIPTIONS[lang]
        return "\n".join(
            f"- {dim} ({dim.capitalize()}): {descs[dim]}"
            for dim in DIMENSIONS
        )
    # Last resort: English
    return asm._dim_block()


# ----------------------------------------------------------------------------
# Native framing prompt templates for cities not covered by
# ai_search_metamerism.NATIVE_GEOPOLITICAL_FRAMING (lt, pl, kk, ka, az)
# ----------------------------------------------------------------------------

# Each template uses {place} and {what} as natural-language phrases supplied
# below. JSON keys remain English for parsing.

LOCAL_NATIVE_FRAMING: dict[str, str] = {
    "lt": (
        "Esate AI pirkimo asistentas. Padedate pirkėjui, gyvenančiam {place}, "
        "priimti sprendimą.\n"
        "Pirkėjas svarsto galimybę įsigyti {what}.\n\n"
        "Remdamiesi savo žiniomis apie prekės ženklą {brand} ir tuo, kaip jį "
        "suvokia pirkėjai {place}, paskirstykite tiksliai 100 taškų tarp aštuonių "
        "prekės ženklo dimensijų — taip, kad paskirstymas atspindėtų, kurie "
        "prekės ženklo aspektai svarbiausi būtent šiam pirkėjui priimant "
        "sprendimą. Taškų suma turi būti lygiai 100.\n\n"
        "{dim_block}\n\n"
        "Atsakykite TIK galiojančiu JSON tokio formato:\n"
        '{{"weights": {{"semiotic": N, "narrative": N, "ideological": N, '
        '"experiential": N, "social": N, "economic": N, "cultural": N, '
        '"temporal": N}}, "reasoning": "jūsų paaiškinimas"}}'
    ),
    "pl": (
        "Jesteś asystentem zakupowym AI. Pomagasz kupującemu, który mieszka "
        "{place}, podjąć decyzję.\n"
        "Kupujący rozważa zakup {what}.\n\n"
        "Opierając się na swojej wiedzy o marce {brand} i o tym, jak jest "
        "postrzegana przez kupujących {place}, rozdziel dokładnie 100 punktów "
        "pomiędzy osiem wymiarów marki — tak, aby rozkład odzwierciedlał, "
        "które aspekty marki są najważniejsze właśnie dla tego kupującego "
        "przy podejmowaniu decyzji o zakupie. Suma punktów musi wynosić "
        "dokładnie 100.\n\n"
        "{dim_block}\n\n"
        "Odpowiedz TYLKO poprawnym JSON-em w następującym formacie:\n"
        '{{"weights": {{"semiotic": N, "narrative": N, "ideological": N, '
        '"experiential": N, "social": N, "economic": N, "cultural": N, '
        '"temporal": N}}, "reasoning": "twoje wyjaśnienie"}}'
    ),
    "kk": (
        "Сіз — AI сатып алу көмекшісісіз. Сіз {place} тұратын сатып алушыға "
        "шешім қабылдауға көмектесесіз.\n"
        "Сатып алушы {what} сатып алу мүмкіндігін қарастырып отыр.\n\n"
        "{brand} брендін және оны {place} тұратын сатып алушылардың қалай "
        "қабылдайтынын білуіңізге сүйене отырып, сегіз бренд өлшемі арасында "
        "дәл 100 ұпайды бөліңіз — бұл бөлу сатып алушының шешім қабылдау "
        "кезінде брендтің қандай аспектілері маңызды екенін көрсетсін. "
        "Ұпайлардың қосындысы дәл 100 болуы керек.\n\n"
        "{dim_block}\n\n"
        "Тек жарамды JSON форматында жауап беріңіз:\n"
        '{{"weights": {{"semiotic": N, "narrative": N, "ideological": N, '
        '"experiential": N, "social": N, "economic": N, "cultural": N, '
        '"temporal": N}}, "reasoning": "сіздің түсіндірмеңіз"}}'
    ),
    "ka": (
        "თქვენ ხართ AI შოპინგ ასისტენტი. თქვენ ეხმარებით მყიდველს, რომელიც "
        "ცხოვრობს {place}, მიიღოს გადაწყვეტილება.\n"
        "მყიდველი განიხილავს {what}-ის შეძენის შესაძლებლობას.\n\n"
        "ბრენდ {brand}-ის შესახებ თქვენი ცოდნისა და იმის გათვალისწინებით, "
        "თუ როგორ აღიქვამენ მას მყიდველები {place}, გაანაწილეთ ზუსტად 100 "
        "ქულა რვა ბრენდის განზომილებას შორის — ისე, რომ განაწილებამ "
        "ასახოს, რომელი ასპექტებია ყველაზე მნიშვნელოვანი ამ კონკრეტული "
        "მყიდველისთვის გადაწყვეტილების მიღებისას. ქულების ჯამი უნდა იყოს "
        "ზუსტად 100.\n\n"
        "{dim_block}\n\n"
        "უპასუხეთ მხოლოდ ვალიდური JSON-ით შემდეგი ფორმატით:\n"
        '{{"weights": {{"semiotic": N, "narrative": N, "ideological": N, '
        '"experiential": N, "social": N, "economic": N, "cultural": N, '
        '"temporal": N}}, "reasoning": "თქვენი ახსნა"}}'
    ),
    "az": (
        "Siz AI alış-veriş köməkçisisiniz. {place} yaşayan alıcıya qərar "
        "verməsində kömək edirsiniz.\n"
        "Alıcı {what} almaq imkanını nəzərdən keçirir.\n\n"
        "{brand} brendi haqqında biliyinizə və {place} yaşayan alıcıların "
        "onu necə qəbul etdiyinə əsaslanaraq, brendin səkkiz ölçüsü arasında "
        "tam olaraq 100 xal paylayın — bu paylaşma alıcının qərar qəbul "
        "edərkən brendin hansı aspektlərinin daha vacib olduğunu əks "
        "etdirsin. Xalların cəmi tam olaraq 100 olmalıdır.\n\n"
        "{dim_block}\n\n"
        "Yalnız etibarlı JSON formatında cavab verin:\n"
        '{{"weights": {{"semiotic": N, "narrative": N, "ideological": N, '
        '"experiential": N, "social": N, "economic": N, "cultural": N, '
        '"temporal": N}}, "reasoning": "izahınız"}}'
    ),
}


# Native phrasings of {place} (full prepositional phrase) and {what} (purchase
# target with correct case) per (city, language) cell.
NATIVE_PHRASES: dict[tuple[str, str], dict[str, str]] = {
    # Moscow ru already handled by ai_search_metamerism.NATIVE_GEOPOLITICAL_FRAMING
    # but we'll provide our own values to keep this script self-contained.
    ("Moscow",  "ru"): {"brand": "Рошен",  "place": "в Москве",      "what": "шоколада Рошен"},
    ("Kyiv",    "uk"): {"brand": "Roshen", "place": "у Києві",       "what": "шоколаду Roshen"},
    ("Vilnius", "lt"): {"brand": "Roshen", "place": "Vilniuje",      "what": "Roshen šokolado"},
    ("Warsaw",  "pl"): {"brand": "Roshen", "place": "w Warszawie",   "what": "czekolady Roshen"},
    ("Astana",  "kk"): {"brand": "Рошен",  "place": "Астанада",      "what": "Рошен шоколадын"},
    ("Astana",  "ru"): {"brand": "Рошен",  "place": "в Астане",      "what": "шоколада Рошен"},
    ("Tbilisi", "ka"): {"brand": "Roshen", "place": "თბილისში",      "what": "Roshen შოკოლადის"},
    ("Baku",    "az"): {"brand": "Roshen", "place": "Bakıda",        "what": "Roshen şokoladı"},
}


def build_prompt(city: str, lang: str) -> str:
    """Build the framing prompt for a (city, lang) cell."""
    dim_block = dim_block_for_lang(lang)
    if lang == "en":
        return asm.GEOPOLITICAL_FRAMING_PROMPT.format(
            city=city, brand=BRAND, product=PRODUCT, dim_block=dim_block,
        )

    # Native template + native phrasing lookup
    template = LOCAL_NATIVE_FRAMING.get(lang)
    if template is None:
        # Try the main script's native templates (ru, uk, etc.)
        template = asm.NATIVE_GEOPOLITICAL_FRAMING.get(lang)
    if template is None:
        # Fall back to English
        return asm.GEOPOLITICAL_FRAMING_PROMPT.format(
            city=city, brand=BRAND, product=PRODUCT, dim_block=dim_block,
        )

    phrases = NATIVE_PHRASES.get((city, lang), {})
    return template.format(
        brand=phrases.get("brand", BRAND),
        place=phrases.get("place", city),
        what=phrases.get("what", f"{BRAND} {PRODUCT}"),
        dim_block=dim_block,
    )


# ----------------------------------------------------------------------------
# Model panel
# ----------------------------------------------------------------------------

MODEL_PANEL = [
    "claude",
    "gpt",
    "gemini",
    "deepseek",
    "qwen3_local",
    "gemma4_local",
    "yandexgpt_pro",
]


# ----------------------------------------------------------------------------
# Live execution
# ----------------------------------------------------------------------------

def run_live(n_runs: int, smoke: bool = False) -> None:
    L3_DIR.mkdir(parents=True, exist_ok=True)
    L4_DIR.mkdir(parents=True, exist_ok=True)

    # Filter to credentialed models
    valid_models: list[str] = []
    for model_name in MODEL_PANEL:
        if model_name not in asm.API_CALLERS:
            print(f"  SKIP: {model_name} not in API_CALLERS")
            continue
        key_var = asm.API_KEY_VARS.get(model_name)
        if key_var and "local" not in model_name and key_var not in os.environ:
            print(f"  SKIP: {model_name} ({key_var} not set)")
            continue
        valid_models.append(model_name)
    if not valid_models:
        print("ERROR: no valid models available; aborting.")
        sys.exit(1)
    print(f"Valid models: {valid_models}")

    cities = CITY_CONDITIONS[:1] if smoke else CITY_CONDITIONS

    # Build the cell list
    cells: list[tuple[str, str]] = []
    for city, _country, langs in cities:
        for lang in langs:
            cells.append((city, lang))
    total = len(cells) * len(valid_models) * n_runs
    print(f"Run 11 — Roshen Multi-City Framing")
    print(f"Cells: {len(cells)} | Models: {len(valid_models)} | Runs: {n_runs}")
    print(f"Total calls: {total}")
    print(f"Output log: {OUT_LOG}")

    # Clear previous log so the aggregator sees only this run's records
    if OUT_LOG.exists():
        OUT_LOG.unlink()

    done = 0
    for run_idx in range(1, n_runs + 1):
        for city, lang in cells:
            prompt = build_prompt(city, lang)
            label = f"Roshen ({city}) [{lang}]"
            for model_name in valid_models:
                caller = asm.API_CALLERS[model_name]
                done += 1
                print(
                    f"  [{done}/{total}] run={run_idx} model={model_name} "
                    f"city={city} lang={lang}"
                )
                log_ctx = {
                    "prompt_type": (
                        "geopolitical_framing"
                        if lang == "en"
                        else "geopolitical_framing_native"
                    ),
                    "brand_pair": label,
                    "pair_id": f"roshen_multicity_{city.lower()}",
                    "dimension": None,
                    "brand": BRAND,
                    "city": city,
                    "run": run_idx,
                    "prompt_language": lang,
                }
                t0 = time.monotonic()
                try:
                    raw = asm.call_with_retry(
                        caller, prompt, model_name,
                        log_path=str(OUT_LOG), log_context=log_ctx,
                    )
                    latency = int((time.monotonic() - t0) * 1000)
                    parsed = {}
                    try:
                        parsed = asm.parse_llm_json(raw)
                    except Exception:
                        pass
                    # call_with_retry already wrote the JSONL line via log_path,
                    # so we don't need to append again here.
                    _ = (raw, latency, parsed)
                except Exception as exc:
                    print(f"    [error] {model_name} {city} {lang}: {exc}")

    if OUT_LOG.exists():
        records = sum(1 for _ in OUT_LOG.open())
        print(f"Wrote {records} records to {OUT_LOG}")


# ----------------------------------------------------------------------------
# Aggregation
# ----------------------------------------------------------------------------

def parse_weights(record: dict) -> dict[str, float] | None:
    parsed = record.get("parsed") or {}
    if not isinstance(parsed, dict):
        return None
    weights = parsed.get("weights")
    if not isinstance(weights, dict):
        return None
    try:
        w = {dim: float(weights.get(dim, 0)) for dim in DIMENSIONS}
    except (TypeError, ValueError):
        return None
    total = sum(w.values())
    if not (90 <= total <= 110):
        return None
    return w


def aggregate(records: list[dict]) -> dict[str, Any]:
    """Aggregate per (city, lang, model)."""
    by_cell: dict[tuple[str, str, str], list[dict[str, float]]] = {}
    for r in records:
        city = r.get("city")
        lang = r.get("prompt_language")
        model = r.get("model")
        if city is None:
            # Recover from pair_id if "city" key absent
            pair_id = r.get("pair_id", "")
            if pair_id.startswith("roshen_multicity_"):
                city = pair_id.replace("roshen_multicity_", "").capitalize()
        if not (city and lang and model):
            continue
        w = parse_weights(r)
        if w is None:
            continue
        by_cell.setdefault((city, lang, model), []).append(w)

    cell_profiles: dict[str, dict[str, dict[str, float]]] = {}
    for (city, lang, model), profs in by_cell.items():
        cell_profiles.setdefault(f"{city}|{lang}", {})[model] = {
            dim: round(mean(p[dim] for p in profs), 3) for dim in DIMENSIONS
        }

    # Cross-model mean per (city, lang)
    cell_means: dict[str, dict[str, float]] = {}
    cell_dci: dict[str, float] = {}
    for cell_key, by_model in cell_profiles.items():
        means_per_dim = {
            dim: round(mean(by_model[m][dim] for m in by_model), 3)
            for dim in DIMENSIONS
        }
        cell_means[cell_key] = means_per_dim
        cell_dci[cell_key] = round(
            means_per_dim["economic"] + means_per_dim["semiotic"], 3
        )

    return {
        "n_records": len(records),
        "n_valid_records": sum(len(profs) for profs in by_cell.values()),
        "cell_profiles": cell_profiles,
        "cell_means": cell_means,
        "cell_dci": cell_dci,
    }


def write_summary(results: dict[str, Any]) -> None:
    cell_dci = results["cell_dci"]
    cell_means = results["cell_means"]

    lines = [
        "# Run 11 — Roshen Multi-City Framing Results",
        "",
        f"**Generated:** {_dt.datetime.now(_dt.timezone.utc).isoformat()}",
        "",
        "## Design",
        "",
        "Roshen evaluated as a same-brand framing experiment across 7 cities,",
        "in English plus the local national language(s). Astana receives both",
        "Kazakh and Russian native conditions; all other non-English cities",
        "receive one native condition. Same prompt template, same model panel,",
        "differing only in city name and prompt language.",
        "",
        "## Cross-model mean DCI by (city, language)",
        "",
        "DCI = w_economic + w_semiotic, normalised so the uniform baseline = 25.0.",
        "Higher DCI = more dimensional collapse toward Economic + Semiotic.",
        "",
        "| City     | Operational status | en DCI | native DCI (lang) | Δ (native − en) |",
        "|----------|--------------------|-------:|------------------:|----------------:|",
    ]
    for city, _country, langs in CITY_CONDITIONS:
        en_key = f"{city}|en"
        en_dci = cell_dci.get(en_key)
        en_str = f"{en_dci}" if en_dci is not None else "—"
        native_langs = [lg for lg in langs if lg != "en"]
        # Compose native DCI cell — may have multiple langs (Astana)
        nat_parts = []
        delta_parts = []
        for nl in native_langs:
            nk = f"{city}|{nl}"
            nd = cell_dci.get(nk)
            if nd is not None:
                nat_parts.append(f"{nd} ({nl})")
                if en_dci is not None:
                    delta_parts.append(f"{nd - en_dci:+.3f} ({nl})")
        op_status = CITY_OPERATIONAL_STATUS.get(city, "")
        lines.append(
            f"| {city} | {op_status} | {en_str} | "
            f"{'; '.join(nat_parts) if nat_parts else '—'} | "
            f"{'; '.join(delta_parts) if delta_parts else '—'} |"
        )

    lines += [
        "",
        "## Cross-model mean profile per (city, language)",
        "",
        "| City | Lang | Sem | Nar | Ide | Exp | Soc | Eco | Cul | Tem | DCI |",
        "|------|------|----:|----:|----:|----:|----:|----:|----:|----:|----:|",
    ]
    for city, _country, langs in CITY_CONDITIONS:
        for lang in langs:
            key = f"{city}|{lang}"
            m = cell_means.get(key, {})
            if not m:
                continue
            row = [city, lang]
            row += [f"{m.get(d, 0):.1f}" for d in DIMENSIONS]
            row.append(f"{cell_dci.get(key, 0):.3f}")
            lines.append("| " + " | ".join(row) + " |")

    lines += [
        "",
        "## Variable separation",
        "",
        "The 7-city design enables three contrasts that the original 2-city",
        "Moscow/Kyiv test could not separate:",
        "",
        "1. **Operational anchor** (Vilnius vs Warsaw): both EU/NATO and",
        "   Ukraine-aligned, but only Vilnius has the Klaipėda factory.",
        "   If Vilnius < Warsaw on collapse, AI uses operational reality.",
        "",
        "2. **Discourse density** (Kyiv vs all others): home market vs",
        "   foreign markets. The expected baseline is Kyiv = lowest collapse.",
        "",
        "3. **Geopolitical alignment** (Moscow vs Astana/Tbilisi/Baku):",
        "   conflict-hostile vs post-USSR neutral. Tests whether the",
        "   Moscow effect is alignment-specific or generic foreign-context.",
        "",
        "Per-contrast verdicts (populate after reviewing the deltas above):",
        "",
        "- **Operational anchor effect**: ",
        "- **Native language H10 × H12 interaction**: ",
        "- **Conflict vs neutrality contrast**: ",
        "- **Astana kk vs ru contrast**: ",
        "",
    ]

    OUT_SUMMARY.write_text("\n".join(lines))
    print(f"Wrote {OUT_SUMMARY}")


def aggregate_and_write() -> None:
    if not OUT_LOG.exists():
        print(f"ERROR: {OUT_LOG} does not exist; nothing to aggregate.")
        sys.exit(1)
    records = []
    with OUT_LOG.open() as fh:
        for line in fh:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    print(f"Loaded {len(records)} records from {OUT_LOG}")
    results = aggregate(records)
    OUT_RESULTS.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"Wrote {OUT_RESULTS}")
    write_summary(results)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description="Run 11 Roshen multi-city framing")
    p.add_argument("--demo", action="store_true", help="Offline dry run")
    p.add_argument("--smoke", action="store_true", help="1 city × all models × 1 run")
    p.add_argument("--live", action="store_true", help="Full experiment")
    p.add_argument("--analyze-only", action="store_true",
                   help="Re-aggregate from existing JSONL log")
    p.add_argument("--runs", type=int, default=3,
                   help="Repetitions per (city, lang, model) cell")
    args = p.parse_args()

    if not (args.demo or args.smoke or args.live or args.analyze_only):
        p.print_help()
        sys.exit(1)

    if args.demo:
        cities = CITY_CONDITIONS[:1] if False else CITY_CONDITIONS
        n_runs = 1
        cells = sum(len(langs) for _, _, langs in cities)
        print(f"DEMO — would run {cells} cells × {len(MODEL_PANEL)} models × {n_runs} runs")
        for city, country, langs in cities:
            for lang in langs:
                preview = build_prompt(city, lang).split("\n")[0][:80]
                print(f"  {city} ({country}) [{lang}]: {preview}...")
        return

    if args.smoke:
        run_live(n_runs=1, smoke=True)
    elif args.live:
        run_live(n_runs=args.runs, smoke=False)

    if not args.demo:
        aggregate_and_write()


if __name__ == "__main__":
    main()
