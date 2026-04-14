#!/usr/bin/env python3
"""
R20 Portfolio-AI Experiment: Solo vs Portfolio Framing

Tests whether framing a brand as part of a corporate portfolio changes
LLM perception of that brand across 8 SBT dimensions.

Design (v2.0 extension):
  - 17 brands in 6 portfolios (LVMH, Unilever, P&G, Toyota, L'Oreal, Geely, Yandex)
  - 13 models from 7 training traditions (Western, Chinese, Russian, Indian, Japanese, European, Korean)
  - 3 conditions: SOLO, PORTFOLIO (user msg), SYSTEM_PORTFOLIO (system msg)
  - Recommendation prompts: SOLO + PORTFOLIO
  - Multi-turn: Turn 1 solo, Turn 2 reveal + re-rate
  - Native-language ablation: home portfolios in French, Chinese, Japanese, Russian
  - 5 repetitions per cell

Usage:
    uv run python run_portfolio.py [--model MODEL] [--dry-run]
    uv run python run_portfolio.py --recommendation [--model MODEL]
    uv run python run_portfolio.py --multiturn [--model MODEL]
    uv run python run_portfolio.py --native [--model MODEL]
    uv run python run_portfolio.py --ablation [--model MODEL]
    uv run python run_portfolio.py --reparse
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Experiment Configuration
# ---------------------------------------------------------------------------

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

DIMENSION_DESCRIPTIONS = {
    "semiotic": "visual and verbal identity (logos, packaging, design language)",
    "narrative": "brand storytelling (origin story, mythology, communication style)",
    "ideological": "values, beliefs, and purpose (what the brand stands for)",
    "experiential": "sensory and interaction experience (product feel, service quality)",
    "social": "community, status signaling (who uses this brand, what it says about them)",
    "economic": "pricing and value perception (affordability, luxury, value-for-money)",
    "cultural": "cultural codes and positioning (what culture or subculture it belongs to)",
    "temporal": "heritage and history (longevity, tradition, track record)",
}

PORTFOLIOS = {
    "LVMH": {
        "parent": "LVMH Moet Hennessy Louis Vuitton",
        "descriptor": "luxury conglomerate",
        "brands": [
            {"name": "Louis Vuitton", "category": "luxury fashion"},
            {"name": "Dior", "category": "luxury fashion and beauty"},
            {"name": "Fendi", "category": "luxury fashion"},
        ],
    },
    "Unilever": {
        "parent": "Unilever",
        "descriptor": "consumer goods conglomerate",
        "brands": [
            {"name": "Dove", "category": "personal care"},
            {"name": "Axe", "category": "personal care"},
            {"name": "Ben & Jerry's", "category": "ice cream"},
        ],
    },
    "P&G": {
        "parent": "Procter & Gamble",
        "descriptor": "consumer goods conglomerate",
        "brands": [
            {"name": "Tide", "category": "laundry detergent"},
            {"name": "Pampers", "category": "baby care"},
            {"name": "Gillette", "category": "grooming"},
        ],
    },
    "Toyota": {
        "parent": "Toyota Motor Corporation",
        "descriptor": "automotive conglomerate",
        "brands": [
            {"name": "Toyota", "category": "mass-market automotive"},
            {"name": "Lexus", "category": "luxury automotive"},
        ],
    },
    "L'Oreal": {
        "parent": "L'Oreal Group",
        "descriptor": "beauty and cosmetics conglomerate",
        "brands": [
            {"name": "L'Oreal Paris", "category": "mass-market beauty"},
            {"name": "Lancome", "category": "luxury beauty"},
            {"name": "Maybelline", "category": "mass-market cosmetics"},
        ],
    },
    "Geely": {
        "parent": "Geely Automobile Holdings",
        "descriptor": "Chinese automotive conglomerate",
        "brands": [
            {"name": "Volvo", "category": "premium automotive"},
            {"name": "Polestar", "category": "electric vehicle brand"},
            {"name": "Geely Auto", "category": "mass-market automotive"},
        ],
    },
    "Yandex": {
        "parent": "Yandex",
        "descriptor": "Russian technology conglomerate",
        "brands": [
            {"name": "Yandex", "category": "search engine and technology platform"},
            {"name": "Yandex Taxi", "category": "ride-hailing service"},
            {"name": "Yandex Market", "category": "e-commerce platform"},
        ],
    },
}

MODELS = [
    # --- Anthropic, Chinese, Meta/Groq, Google local ---
    {
        "id": "claude",
        "name": "Claude Sonnet 4",
        "provider": "anthropic",
        "model_id": "claude-sonnet-4-20250514",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "deepseek",
        "name": "DeepSeek V3",
        "provider": "deepseek",
        "model_id": "deepseek-chat",
        "tradition": "Chinese",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "llama",
        "name": "Llama 3.3 70B",
        "provider": "groq",
        "model_id": "llama-3.3-70b-versatile",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "gemma4",
        "name": "Gemma 4",
        "provider": "ollama",
        "model_id": "gemma4:latest",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    # --- OpenAI, Google API, xAI ---
    {
        "id": "gpt4omini",
        "name": "GPT-4o-mini",
        "provider": "openai",
        "model_id": "gpt-4o-mini",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "gemini25flash",
        "name": "Gemini 2.5 Flash",
        "provider": "google",
        "model_id": "gemini-2.5-flash",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 2048,  # Gemini 2.5 uses thinking tokens
    },
    {
        "id": "grok",
        "name": "Grok-3-mini",
        "provider": "xai",
        "model_id": "grok-3-mini",
        "tradition": "Western",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    # --- Cross-cultural additions ---
    {
        "id": "yandex",
        "name": "YandexGPT 5 Pro",
        "provider": "yandex",
        "model_id": "yandexgpt-5-pro/latest",
        "tradition": "Russian",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "sarvam",
        "name": "Sarvam M",
        "provider": "sarvam",
        "model_id": "sarvam-m",
        "tradition": "Indian",
        "temperature": 0.7,
        "max_tokens": 2048,  # Sarvam uses <think> blocks
    },
    {
        "id": "swallow",
        "name": "GPT-OSS-Swallow 20B",
        "provider": "yandex",
        "model_id": "gpt-oss-20b/latest",
        "tradition": "Japanese",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    # --- Extension: Chinese, European, Korean ---
    {
        "id": "qwen3",
        "name": "Qwen3 235B",
        "provider": "cerebras",
        "model_id": "qwen-3-235b-a22b-instruct-2507",
        "tradition": "Chinese",
        "temperature": 0.7,
        "max_tokens": 2048,  # Qwen uses thinking tokens
    },
    {
        "id": "mistral",
        "name": "Mistral Large",
        "provider": "mistral",
        "model_id": "mistral-large-2512",
        "tradition": "European",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    {
        "id": "exaone",
        "name": "EXAONE 3.5 32B",
        "provider": "ollama",
        "model_id": "exaone3.5:32b",
        "tradition": "Korean",
        "temperature": 0.7,
        "max_tokens": 500,
    },
]

# Models used in the system-prompt ablation (4 proven models)
ABLATION_MODEL_IDS = ["claude", "deepseek", "llama", "gemma4"]

REPETITIONS = 5


# ---------------------------------------------------------------------------
# Prompt Templates (1-5 PRISM-B scale)
# ---------------------------------------------------------------------------

SOLO_TEMPLATE = """You are evaluating the brand {brand} on eight dimensions of brand perception.
For each dimension, rate how strongly {brand} communicates through that channel
on a scale of 1 to 5, where 1 = Not at all, 2 = Slightly, 3 = Moderately,
4 = Strongly, 5 = Very strongly.

Dimensions:
{dimensions}

Respond in JSON format with the following keys:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Evaluate based on your knowledge of the brand. Provide only the JSON."""

PORTFOLIO_TEMPLATE = """You are evaluating the brand {brand} on eight dimensions of brand perception.

Context: {brand} is owned by {parent} ({descriptor}), which also owns {siblings}.

For each dimension, rate how strongly {brand} communicates through that channel
on a scale of 1 to 5, where 1 = Not at all, 2 = Slightly, 3 = Moderately,
4 = Strongly, 5 = Very strongly.

Dimensions:
{dimensions}

Respond in JSON format with the following keys:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Evaluate based on your knowledge of the brand. Provide only the JSON."""

SYSTEM_PORTFOLIO_TEMPLATE = """You have access to the following corporate context: {brand} is owned by {parent} ({descriptor}), which also owns {siblings}. Use this context when evaluating brands. Always rate all eight dimensions: semiotic, narrative, ideological, experiential, social, economic, cultural, temporal."""

# Recommendation category mapping for naturalistic prompts
RECOMMENDATION_CATEGORIES = {
    "Louis Vuitton": "luxury fashion brand",
    "Dior": "luxury fashion brand",
    "Fendi": "luxury fashion brand",
    "Dove": "personal care brand",
    "Axe": "personal care brand",
    "Ben & Jerry's": "ice cream brand",
    "Tide": "laundry detergent",
    "Pampers": "baby care brand",
    "Gillette": "grooming brand",
    "Toyota": "car brand",
    "Lexus": "luxury car brand",
    "L'Oreal Paris": "beauty brand",
    "Lancome": "luxury beauty brand",
    "Maybelline": "cosmetics brand",
    "Volvo": "car brand",
    "Polestar": "electric car brand",
    "Geely Auto": "car brand",
    "Yandex": "technology platform",
    "Yandex Taxi": "ride-hailing service",
    "Yandex Market": "e-commerce platform",
}

RECOMMENDATION_SOLO_TEMPLATE = """A friend asks you: "What do you think of {brand} as a {category}?"

Based on your overall impression of {brand}, rate it on each of the following
8 perception dimensions on a scale of 1 to 5 (1 = Not at all, 5 = Very strongly).

Dimensions:
{dimensions}

Respond in JSON format:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Provide only the JSON."""

RECOMMENDATION_PORTFOLIO_TEMPLATE = """A friend asks you: "What do you think of {brand}? I know it's part of {parent}."

Based on your overall impression of {brand} — keeping in mind it belongs to
{parent} ({descriptor}), alongside {siblings} — rate it on each of the following
8 perception dimensions on a scale of 1 to 5 (1 = Not at all, 5 = Very strongly).

Dimensions:
{dimensions}

Respond in JSON format:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Provide only the JSON."""

# ---------------------------------------------------------------------------
# Native-Language Portfolio Templates
# ---------------------------------------------------------------------------

# Native-language prompts for "home" portfolios — tests discourse-layer activation
NATIVE_LANGUAGE_PORTFOLIOS = {
    "L'Oreal": {
        "language": "fr",
        "language_name": "French",
        "solo_template": """Vous evaluez la marque {brand} sur huit dimensions de perception de marque.
Pour chaque dimension, evaluez la force avec laquelle {brand} communique a travers ce canal
sur une echelle de 1 a 5, ou 1 = Pas du tout, 2 = Legerement, 3 = Moderement,
4 = Fortement, 5 = Tres fortement.

Dimensions :
{dimensions}

Repondez au format JSON avec les cles suivantes :
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Evaluez selon votre connaissance de la marque. Fournissez uniquement le JSON.""",
        "portfolio_template": """Vous evaluez la marque {brand} sur huit dimensions de perception de marque.

Contexte : {brand} appartient au {parent} ({descriptor}), qui possede egalement {siblings}.

Pour chaque dimension, evaluez la force avec laquelle {brand} communique a travers ce canal
sur une echelle de 1 a 5, ou 1 = Pas du tout, 2 = Legerement, 3 = Moderement,
4 = Fortement, 5 = Tres fortement.

Dimensions :
{dimensions}

Repondez au format JSON avec les cles suivantes :
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Evaluez selon votre connaissance de la marque. Fournissez uniquement le JSON.""",
        "dimension_descriptions": {
            "semiotic": "identite visuelle et verbale (logos, packaging, langage de design)",
            "narrative": "storytelling de marque (histoire d'origine, mythologie, style de communication)",
            "ideological": "valeurs, croyances et raison d'etre (ce que la marque represente)",
            "experiential": "experience sensorielle et d'interaction (toucher du produit, qualite de service)",
            "social": "communaute, signalisation de statut (qui utilise cette marque, ce que cela dit d'eux)",
            "economic": "perception de prix et de valeur (accessibilite, luxe, rapport qualite-prix)",
            "cultural": "codes culturels et positionnement (a quelle culture ou sous-culture elle appartient)",
            "temporal": "heritage et histoire (longevite, tradition, historique)",
        },
    },
    "Geely": {
        "language": "zh",
        "language_name": "Chinese",
        "solo_template": """请您对品牌 {brand} 在以下八个品牌感知维度上进行评估。
对于每个维度，请评估 {brand} 通过该渠道传达信息的强度，
评分标准为1到5分，其中1 = 完全没有，2 = 略微，3 = 中等，
4 = 强烈，5 = 非常强烈。

维度：
{dimensions}

请以JSON格式回复，使用以下键：
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

根据您对该品牌的了解进行评估。请仅提供JSON。""",
        "portfolio_template": """请您对品牌 {brand} 在以下八个品牌感知维度上进行评估。

背景信息：{brand} 属于{parent}（{descriptor}），该集团还拥有{siblings}。

对于每个维度，请评估 {brand} 通过该渠道传达信息的强度，
评分标准为1到5分，其中1 = 完全没有，2 = 略微，3 = 中等，
4 = 强烈，5 = 非常强烈。

维度：
{dimensions}

请以JSON格式回复，使用以下键：
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

根据您对该品牌的了解进行评估。请仅提供JSON。""",
        "dimension_descriptions": {
            "semiotic": "视觉和语言标识（标志、包装、设计语言）",
            "narrative": "品牌叙事（起源故事、神话、沟通风格）",
            "ideological": "价值观、信念和使命（品牌代表什么）",
            "experiential": "感官和互动体验（产品触感、服务质量）",
            "social": "社群和地位信号（谁使用这个品牌，这说明了什么）",
            "economic": "价格和价值感知（平价、奢华、性价比）",
            "cultural": "文化符码和定位（属于哪种文化或亚文化）",
            "temporal": "传承和历史（持久性、传统、往绩）",
        },
    },
    "Toyota": {
        "language": "ja",
        "language_name": "Japanese",
        "solo_template": """ブランド {brand} を、以下の8つのブランド認知次元で評価してください。
各次元について、{brand} がそのチャネルを通じてどの程度強くコミュニケーションしているかを
1から5のスケールで評価してください。1 = 全くない、2 = わずかに、3 = 中程度に、
4 = 強く、5 = 非常に強く。

次元：
{dimensions}

以下のキーを使用してJSON形式で回答してください：
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

ブランドに関するあなたの知識に基づいて評価してください。JSONのみを提供してください。""",
        "portfolio_template": """ブランド {brand} を、以下の8つのブランド認知次元で評価してください。

背景情報：{brand} は{parent}（{descriptor}）に属しており、同グループには{siblings}もあります。

各次元について、{brand} がそのチャネルを通じてどの程度強くコミュニケーションしているかを
1から5のスケールで評価してください。1 = 全くない、2 = わずかに、3 = 中程度に、
4 = 強く、5 = 非常に強く。

次元：
{dimensions}

以下のキーを使用してJSON形式で回答してください：
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

ブランドに関するあなたの知識に基づいて評価してください。JSONのみを提供してください。""",
        "dimension_descriptions": {
            "semiotic": "視覚的・言語的アイデンティティ（ロゴ、パッケージ、デザイン言語）",
            "narrative": "ブランドストーリーテリング（起源の物語、神話、コミュニケーションスタイル）",
            "ideological": "価値観、信念、目的（ブランドが何を支持しているか）",
            "experiential": "感覚的・インタラクション体験（製品の触感、サービス品質）",
            "social": "コミュニティ、ステータスシグナル（誰がこのブランドを使い、それが何を示すか）",
            "economic": "価格と価値の認知（手頃さ、高級感、コストパフォーマンス）",
            "cultural": "文化的コードとポジショニング（どの文化やサブカルチャーに属するか）",
            "temporal": "遺産と歴史（長寿、伝統、実績）",
        },
    },
    "Yandex": {
        "language": "ru",
        "language_name": "Russian",
        "solo_template": """Оцените бренд {brand} по восьми измерениям восприятия бренда.
Для каждого измерения оцените, насколько сильно {brand} коммуницирует через данный канал,
по шкале от 1 до 5, где 1 = Совсем нет, 2 = Слегка, 3 = Умеренно,
4 = Сильно, 5 = Очень сильно.

Измерения:
{dimensions}

Ответьте в формате JSON со следующими ключами:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Оценивайте на основе ваших знаний о бренде. Предоставьте только JSON.""",
        "portfolio_template": """Оцените бренд {brand} по восьми измерениям восприятия бренда.

Контекст: {brand} принадлежит компании {parent} ({descriptor}), которой также принадлежат {siblings}.

Для каждого измерения оцените, насколько сильно {brand} коммуницирует через данный канал,
по шкале от 1 до 5, где 1 = Совсем нет, 2 = Слегка, 3 = Умеренно,
4 = Сильно, 5 = Очень сильно.

Измерения:
{dimensions}

Ответьте в формате JSON со следующими ключами:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Оценивайте на основе ваших знаний о бренде. Предоставьте только JSON.""",
        "dimension_descriptions": {
            "semiotic": "визуальная и вербальная идентичность (логотипы, упаковка, язык дизайна)",
            "narrative": "нарратив бренда (история происхождения, мифология, стиль коммуникации)",
            "ideological": "ценности, убеждения и предназначение (что олицетворяет бренд)",
            "experiential": "сенсорный опыт и взаимодействие (ощущение продукта, качество обслуживания)",
            "social": "сообщество, сигнализация статуса (кто пользуется этим брендом, что это говорит о них)",
            "economic": "восприятие цены и ценности (доступность, роскошь, соотношение цены и качества)",
            "cultural": "культурные коды и позиционирование (к какой культуре или субкультуре принадлежит)",
            "temporal": "наследие и история (долговечность, традиции, послужной список)",
        },
    },
}

MULTITURN_TURN1_TEMPLATE = """You are evaluating the brand {brand} on eight dimensions of brand perception.
For each dimension, rate how strongly {brand} communicates through that channel
on a scale of 1 to 5, where 1 = Not at all, 2 = Slightly, 3 = Moderately,
4 = Strongly, 5 = Very strongly.

Dimensions:
{dimensions}

Respond in JSON format with the following keys:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Evaluate based on your knowledge of the brand. Provide only the JSON."""

MULTITURN_TURN2_REVEAL = """Interesting. Did you know that {brand} is actually owned by {parent} ({descriptor}), which also owns {siblings}? Does this change how you see the brand? Please re-rate {brand} on the same 8 dimensions, using the same 1-5 scale.

Respond in JSON format:
{{"semiotic": <1-5>, "narrative": <1-5>, "ideological": <1-5>, "experiential": <1-5>, "social": <1-5>, "economic": <1-5>, "cultural": <1-5>, "temporal": <1-5>}}

Provide only the JSON."""


def format_dimensions() -> str:
    lines = []
    for i, dim in enumerate(DIMENSIONS, 1):
        lines.append(f"{i}. {dim.capitalize()}: {DIMENSION_DESCRIPTIONS[dim]}")
    return "\n".join(lines)


def format_dimensions_native(language_config: dict) -> str:
    """Format dimension descriptions in native language."""
    lines = []
    for i, dim in enumerate(DIMENSIONS, 1):
        desc = language_config["dimension_descriptions"][dim]
        lines.append(f"{i}. {dim.capitalize()}: {desc}")
    return "\n".join(lines)


def make_prompt(
    brand: str, condition: str, portfolio_key: str
) -> tuple[str, str | None]:
    """Return (user_prompt, system_prompt_or_None)."""
    dims_text = format_dimensions()

    if condition == "solo":
        return SOLO_TEMPLATE.format(brand=brand, dimensions=dims_text), None

    portfolio = PORTFOLIOS[portfolio_key]
    siblings = [b["name"] for b in portfolio["brands"] if b["name"] != brand]

    if condition == "portfolio":
        return (
            PORTFOLIO_TEMPLATE.format(
                brand=brand,
                parent=portfolio["parent"],
                descriptor=portfolio["descriptor"],
                siblings=", ".join(siblings),
                dimensions=dims_text,
            ),
            None,
        )

    if condition == "system_portfolio":
        system_msg = SYSTEM_PORTFOLIO_TEMPLATE.format(
            brand=brand,
            parent=portfolio["parent"],
            descriptor=portfolio["descriptor"],
            siblings=", ".join(siblings),
        )
        user_msg = SOLO_TEMPLATE.format(brand=brand, dimensions=dims_text)
        return user_msg, system_msg

    if condition == "recommendation_solo":
        category = RECOMMENDATION_CATEGORIES.get(brand, "brand")
        return (
            RECOMMENDATION_SOLO_TEMPLATE.format(
                brand=brand, category=category, dimensions=dims_text
            ),
            None,
        )

    if condition == "recommendation_portfolio":
        return (
            RECOMMENDATION_PORTFOLIO_TEMPLATE.format(
                brand=brand,
                parent=portfolio["parent"],
                descriptor=portfolio["descriptor"],
                siblings=", ".join(siblings),
                dimensions=dims_text,
            ),
            None,
        )

    # Multi-turn conditions are handled separately in run_multiturn()
    raise ValueError(f"Unknown condition: {condition}")


# ---------------------------------------------------------------------------
# API Providers
# ---------------------------------------------------------------------------


def call_anthropic(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import anthropic

    kwargs = {
        "model": model_config["model_id"],
        "max_tokens": model_config["max_tokens"],
        "temperature": model_config["temperature"],
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt
    client = anthropic.Anthropic()
    response = client.messages.create(**kwargs)
    return response.content[0].text


def call_openai(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import openai

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=messages,
    )
    return response.choices[0].message.content


def call_google(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import google.generativeai as genai

    kwargs = {}
    if system_prompt:
        kwargs["system_instruction"] = system_prompt
    model = genai.GenerativeModel(model_config["model_id"], **kwargs)
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
        ),
    )
    return response.text


def call_deepseek(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import openai

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    client = openai.OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=messages,
    )
    return response.choices[0].message.content


def call_ollama(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import urllib.request

    host = os.environ.get("OLLAMA_HOST", "localhost:11434")
    if not host.startswith("http"):
        host = f"http://{host}"
    url = f"{host}/api/chat"

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload_dict = {
        "model": model_config["model_id"],
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": model_config["temperature"],
            "num_predict": 8192,
        },
    }

    payload = json.dumps(payload_dict).encode()
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
    return data["message"]["content"]


def call_groq(prompt: str, model_config: dict, system_prompt: str | None = None) -> str:
    import openai

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    client = openai.OpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=messages,
    )
    return response.choices[0].message.content


def call_xai(prompt: str, model_config: dict, system_prompt: str | None = None) -> str:
    import openai

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    client = openai.OpenAI(
        api_key=os.environ["GROK_API_KEY"],
        base_url="https://api.x.ai/v1",
    )
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=messages,
    )
    return response.choices[0].message.content


def call_yandex(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import openai

    api_key = os.environ["YANDEX_AI_API_KEY"]
    folder_id = os.environ.get("YANDEX_FOLDER_ID", "b1g894jalgr7i0op2s70")

    client = openai.OpenAI(
        api_key=api_key,
        project=folder_id,
        base_url="https://llm.api.cloud.yandex.net/v1",
    )
    model_uri = f"gpt://{folder_id}/{model_config['model_id']}"

    messages = []
    sys_content = (
        "You are a brand analysis assistant. You MUST respond with ONLY a "
        "valid JSON object. No markdown, no explanation. Start with { and end with }."
    )
    if system_prompt:
        sys_content = system_prompt + "\n\n" + sys_content
    messages.append({"role": "system", "content": sys_content})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model_uri,
        messages=messages,
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
    )
    content = response.choices[0].message.content or ""
    content = re.sub(r"```(?:json)?\s*", "", content).strip()
    content = re.sub(r"```\s*$", "", content).strip()
    return content


def call_sarvam(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import urllib.request

    key = os.environ["SARVAM_API_KEY"]
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps(
        {
            "model": model_config["model_id"],
            "messages": messages,
            "max_tokens": model_config["max_tokens"],
            "temperature": model_config["temperature"],
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.sarvam.ai/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "api-subscription-key": key,
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


def call_cerebras(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import openai

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    client = openai.OpenAI(
        api_key=os.environ["CEREBRAS_API_KEY"],
        base_url="https://api.cerebras.ai/v1",
    )
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=messages,
    )
    content = response.choices[0].message.content or ""
    # Strip thinking blocks from Qwen
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    return content


def call_mistral(
    prompt: str, model_config: dict, system_prompt: str | None = None
) -> str:
    import openai

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    client = openai.OpenAI(
        api_key=os.environ["MISTRAL_API_KEY"],
        base_url="https://api.mistral.ai/v1",
    )
    response = client.chat.completions.create(
        model=model_config["model_id"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
        messages=messages,
    )
    return response.choices[0].message.content


PROVIDERS = {
    "anthropic": call_anthropic,
    "openai": call_openai,
    "google": call_google,
    "deepseek": call_deepseek,
    "ollama": call_ollama,
    "groq": call_groq,
    "xai": call_xai,
    "yandex": call_yandex,
    "sarvam": call_sarvam,
    "cerebras": call_cerebras,
    "mistral": call_mistral,
}


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------


def parse_scores(response_text: str) -> dict | None:
    """Extract 8-dimension scores from LLM response."""
    text = response_text.strip()
    # Strip <think>...</think> reasoning blocks (Sarvam, Qwen, etc.)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```", "", text)

    # Try direct JSON parse
    try:
        data = json.loads(text)
        if isinstance(data, dict) and all(d in data for d in DIMENSIONS):
            return {d: float(data[d]) for d in DIMENSIONS}
    except (json.JSONDecodeError, ValueError, KeyError):
        pass

    # Try to extract JSON from within text
    match = re.search(r"\{[^{}]*\}", text)
    if match:
        try:
            data = json.loads(match.group())
            if isinstance(data, dict) and all(d in data for d in DIMENSIONS):
                return {d: float(data[d]) for d in DIMENSIONS}
        except (json.JSONDecodeError, ValueError, KeyError):
            pass

    return None


# ---------------------------------------------------------------------------
# Experiment Runner
# ---------------------------------------------------------------------------


def get_all_cells(
    ablation: bool = False, conditions: list[str] | None = None
):
    """Generate all experiment cells."""
    cells = []
    if conditions:
        models = MODELS
    elif ablation:
        models = [m for m in MODELS if m["id"] in ABLATION_MODEL_IDS]
        conditions = ["system_portfolio"]
    else:
        models = MODELS
        conditions = ["solo", "portfolio"]

    for portfolio_key, portfolio in PORTFOLIOS.items():
        for brand_info in portfolio["brands"]:
            for condition in conditions:
                for model in models:
                    for rep in range(1, REPETITIONS + 1):
                        cell_id = (
                            f"{portfolio_key}_{brand_info['name'].replace(' ', '_').replace('&', 'and')}"
                            f"_{condition}_{model['id']}_rep{rep}"
                        )
                        cells.append(
                            {
                                "cell_id": cell_id,
                                "portfolio_key": portfolio_key,
                                "brand": brand_info["name"],
                                "category": brand_info["category"],
                                "condition": condition,
                                "model": model,
                                "repetition": rep,
                            }
                        )
    return cells


def run_experiment(
    model_filter: str | None = None,
    dry_run: bool = False,
    ablation: bool = False,
    conditions: list[str] | None = None,
):
    output_dir = Path(__file__).parent / "responses"
    output_dir.mkdir(exist_ok=True)

    cells = get_all_cells(ablation=ablation, conditions=conditions)
    if model_filter:
        cells = [c for c in cells if c["model"]["id"] == model_filter]

    total = len(cells)
    completed = 0
    errors = 0
    skipped = 0

    mode = "ABLATION (system prompt)" if ablation else "MAIN"
    print(f"R20 Portfolio-AI Experiment [{mode}]: {total} cells to process")
    print(f"Models: {', '.join(sorted(set(c['model']['id'] for c in cells)))}")
    print(f"Scale: 1-5 PRISM-B")
    print()

    # Track per-model failure rates for >20% abort
    model_stats: dict[str, dict[str, int]] = {}

    for cell in cells:
        output_file = output_dir / f"{cell['cell_id']}.json"

        if output_file.exists():
            skipped += 1
            continue

        user_prompt, system_prompt = make_prompt(
            cell["brand"], cell["condition"], cell["portfolio_key"]
        )

        if dry_run:
            print(f"[DRY RUN] {cell['cell_id']}")
            completed += 1
            continue

        provider_fn = PROVIDERS[cell["model"]["provider"]]
        mid = cell["model"]["id"]
        if mid not in model_stats:
            model_stats[mid] = {"ok": 0, "fail": 0}

        try:
            response_text = provider_fn(user_prompt, cell["model"], system_prompt)
            scores = parse_scores(response_text)

            record = {
                "cell_id": cell["cell_id"],
                "portfolio": cell["portfolio_key"],
                "brand": cell["brand"],
                "category": cell["category"],
                "condition": cell["condition"],
                "model_id": mid,
                "model_name": cell["model"]["name"],
                "provider": cell["model"]["provider"],
                "tradition": cell["model"]["tradition"],
                "temperature": cell["model"]["temperature"],
                "repetition": cell["repetition"],
                "prompt": user_prompt,
                "system_prompt": system_prompt,
                "response": response_text,
                "scores": scores,
                "parse_success": scores is not None,
                "scale": "1-5",
                "version": "1.0",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            with open(output_file, "w") as f:
                json.dump(record, f, indent=2)

            if scores:
                model_stats[mid]["ok"] += 1
            else:
                model_stats[mid]["fail"] += 1

            completed += 1
            status = "OK" if scores else "PARSE_FAIL"
            n_done = completed + skipped + errors
            print(
                f"[{n_done}/{total}] {cell['cell_id']} {status}"
                + (f" scores={list(scores.values())}" if scores else "")
            )

            # Rate limiting
            provider = cell["model"]["provider"]
            if provider == "ollama":
                time.sleep(0.1)
            elif provider in ("groq", "xai"):
                time.sleep(1.0)
            elif provider == "yandex":
                time.sleep(1.5)  # Conservative for Yandex
            elif provider == "sarvam":
                time.sleep(1.0)
            elif provider == "cerebras":
                time.sleep(0.5)
            elif provider == "mistral":
                time.sleep(0.5)
            else:
                time.sleep(0.5)

        except Exception as e:
            errors += 1
            model_stats[mid]["fail"] += 1
            n_done = completed + skipped + errors
            print(f"[{n_done}/{total}] {cell['cell_id']} ERROR: {e}")

        # Check >20% failure rate per model (after at least 10 attempts)
        ms = model_stats[mid]
        total_attempts = ms["ok"] + ms["fail"]
        if total_attempts >= 10 and ms["fail"] / total_attempts > 0.20:
            fail_pct = ms["fail"] / total_attempts * 100
            print(
                f"\n*** WARNING: {mid} has {fail_pct:.0f}% failure rate "
                f"({ms['fail']}/{total_attempts}). Consider substituting. ***\n"
            )

    print(
        f"\nComplete: {completed} new, {skipped} skipped, {errors} errors, {total} total"
    )
    print(f"Output: {output_dir}/")

    # Print per-model stats
    print("\nPer-model statistics:")
    for mid, ms in sorted(model_stats.items()):
        total_m = ms["ok"] + ms["fail"]
        pct = ms["ok"] / total_m * 100 if total_m > 0 else 0
        print(f"  {mid:20s}  {ms['ok']}/{total_m} OK ({pct:.0f}%)")

    # Print parse failure summary
    parse_failures = []
    for f in output_dir.glob("*.json"):
        with open(f) as fh:
            rec = json.load(fh)
            if not rec.get("parse_success"):
                parse_failures.append(rec["cell_id"])
    if parse_failures:
        print(f"\nParse failures ({len(parse_failures)}):")
        for pf in parse_failures:
            print(f"  {pf}")


# ---------------------------------------------------------------------------
# Re-parse failed responses
# ---------------------------------------------------------------------------


def reparse_failures():
    """Attempt to re-parse responses that failed initial parsing."""
    responses_dir = Path(__file__).parent / "responses"
    fixed = 0
    for f in sorted(responses_dir.glob("*.json")):
        with open(f) as fh:
            rec = json.load(fh)
        if rec.get("parse_success"):
            continue
        scores = parse_scores(rec["response"])
        if scores:
            rec["scores"] = scores
            rec["parse_success"] = True
            with open(f, "w") as fh:
                json.dump(rec, fh, indent=2)
            fixed += 1
            print(f"Fixed: {rec['cell_id']}")
    print(f"\nRe-parsed {fixed} responses")


# ---------------------------------------------------------------------------
# Multi-turn Runner
# ---------------------------------------------------------------------------


def run_multiturn(model_filter: str | None = None, dry_run: bool = False):
    """Run multi-turn experiment: Turn 1 = solo, Turn 2 = reveal portfolio + re-rate."""
    output_dir = Path(__file__).parent / "responses"
    output_dir.mkdir(exist_ok=True)

    dims_text = format_dimensions()
    cells = []
    for portfolio_key, portfolio in PORTFOLIOS.items():
        for brand_info in portfolio["brands"]:
            for model in MODELS:
                for rep in range(1, REPETITIONS + 1):
                    cell_id = (
                        f"{portfolio_key}_{brand_info['name'].replace(' ', '_').replace('&', 'and')}"
                        f"_multiturn_{model['id']}_rep{rep}"
                    )
                    cells.append(
                        {
                            "cell_id": cell_id,
                            "portfolio_key": portfolio_key,
                            "brand": brand_info["name"],
                            "category": brand_info["category"],
                            "model": model,
                            "repetition": rep,
                        }
                    )

    if model_filter:
        cells = [c for c in cells if c["model"]["id"] == model_filter]

    total = len(cells)
    completed = 0
    errors = 0
    skipped = 0

    print(f"R20 Multi-Turn Experiment: {total} cells to process")
    print(f"Models: {', '.join(sorted(set(c['model']['id'] for c in cells)))}")
    print()

    for cell in cells:
        output_file = output_dir / f"{cell['cell_id']}.json"
        if output_file.exists():
            skipped += 1
            continue

        if dry_run:
            print(f"[DRY RUN] {cell['cell_id']}")
            completed += 1
            continue

        brand = cell["brand"]
        portfolio = PORTFOLIOS[cell["portfolio_key"]]
        siblings = [b["name"] for b in portfolio["brands"] if b["name"] != brand]
        provider_fn = PROVIDERS[cell["model"]["provider"]]
        mid = cell["model"]["id"]

        try:
            # Turn 1: Solo rating
            turn1_prompt = MULTITURN_TURN1_TEMPLATE.format(
                brand=brand, dimensions=dims_text
            )
            turn1_response = provider_fn(turn1_prompt, cell["model"])
            turn1_scores = parse_scores(turn1_response)

            # Turn 2: Reveal portfolio and re-rate (multi-turn = send both messages)
            turn2_prompt = MULTITURN_TURN2_REVEAL.format(
                brand=brand,
                parent=portfolio["parent"],
                descriptor=portfolio["descriptor"],
                siblings=", ".join(siblings),
            )

            # For providers that support multi-turn via messages, we simulate it
            # by concatenating context. Most providers only take a single prompt.
            combined_prompt = (
                f"Previous evaluation of {brand}:\n{turn1_response}\n\n"
                f"{turn2_prompt}"
            )
            turn2_response = provider_fn(combined_prompt, cell["model"])
            turn2_scores = parse_scores(turn2_response)

            record = {
                "cell_id": cell["cell_id"],
                "portfolio": cell["portfolio_key"],
                "brand": brand,
                "category": cell["category"],
                "condition": "multiturn",
                "model_id": mid,
                "model_name": cell["model"]["name"],
                "provider": cell["model"]["provider"],
                "tradition": cell["model"]["tradition"],
                "temperature": cell["model"]["temperature"],
                "repetition": cell["repetition"],
                "turn1_prompt": turn1_prompt,
                "turn1_response": turn1_response,
                "turn1_scores": turn1_scores,
                "turn2_prompt": turn2_prompt,
                "turn2_response": turn2_response,
                "scores": turn2_scores,  # Final scores after reveal
                "parse_success": turn1_scores is not None and turn2_scores is not None,
                "scale": "1-5",
                "version": "1.0",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            with open(output_file, "w") as f:
                json.dump(record, f, indent=2)

            completed += 1
            status = "OK" if record["parse_success"] else "PARSE_FAIL"
            n_done = completed + skipped + errors
            print(f"[{n_done}/{total}] {cell['cell_id']} {status}")

            provider = cell["model"]["provider"]
            if provider == "ollama":
                time.sleep(0.1)
            elif provider in ("groq", "xai"):
                time.sleep(1.0)
            elif provider == "yandex":
                time.sleep(1.5)
            elif provider == "sarvam":
                time.sleep(1.0)
            elif provider == "cerebras":
                time.sleep(0.5)
            elif provider == "mistral":
                time.sleep(0.5)
            else:
                time.sleep(0.5)

        except Exception as e:
            errors += 1
            n_done = completed + skipped + errors
            print(f"[{n_done}/{total}] {cell['cell_id']} ERROR: {e}")

    print(
        f"\nComplete: {completed} new, {skipped} skipped, {errors} errors, {total} total"
    )


# ---------------------------------------------------------------------------
# Native-Language Ablation Runner
# ---------------------------------------------------------------------------


def run_native_language(model_filter: str | None = None, dry_run: bool = False):
    """Run native-language ablation: home portfolios in their native language."""
    output_dir = Path(__file__).parent / "responses"
    output_dir.mkdir(exist_ok=True)

    cells = []
    for portfolio_key, lang_config in NATIVE_LANGUAGE_PORTFOLIOS.items():
        portfolio = PORTFOLIOS[portfolio_key]
        dims_text = format_dimensions_native(lang_config)

        for brand_info in portfolio["brands"]:
            for condition in ["native_solo", "native_portfolio"]:
                for model in MODELS:
                    for rep in range(1, REPETITIONS + 1):
                        cell_id = (
                            f"{portfolio_key}_{brand_info['name'].replace(' ', '_').replace('&', 'and')}"
                            f"_{condition}_{model['id']}_rep{rep}"
                        )
                        cells.append(
                            {
                                "cell_id": cell_id,
                                "portfolio_key": portfolio_key,
                                "brand": brand_info["name"],
                                "category": brand_info["category"],
                                "condition": condition,
                                "model": model,
                                "repetition": rep,
                                "language": lang_config["language"],
                                "language_name": lang_config["language_name"],
                                "dims_text": dims_text,
                                "lang_config": lang_config,
                            }
                        )

    if model_filter:
        cells = [c for c in cells if c["model"]["id"] == model_filter]

    total = len(cells)
    completed = 0
    errors = 0
    skipped = 0

    print(f"R20 Native-Language Ablation: {total} cells to process")
    print(f"Languages: {', '.join(sorted(set(c['language_name'] for c in cells)))}")
    print(f"Models: {', '.join(sorted(set(c['model']['id'] for c in cells)))}")
    print()

    for cell in cells:
        output_file = output_dir / f"{cell['cell_id']}.json"
        if output_file.exists():
            skipped += 1
            continue

        if dry_run:
            print(f"[DRY RUN] {cell['cell_id']}")
            completed += 1
            continue

        portfolio = PORTFOLIOS[cell["portfolio_key"]]
        brand = cell["brand"]
        siblings = [b["name"] for b in portfolio["brands"] if b["name"] != brand]
        lang_config = cell["lang_config"]
        dims_text = cell["dims_text"]

        if cell["condition"] == "native_solo":
            user_prompt = lang_config["solo_template"].format(
                brand=brand, dimensions=dims_text
            )
        else:
            user_prompt = lang_config["portfolio_template"].format(
                brand=brand,
                parent=portfolio["parent"],
                descriptor=portfolio["descriptor"],
                siblings=", ".join(siblings),
                dimensions=dims_text,
            )

        provider_fn = PROVIDERS[cell["model"]["provider"]]
        mid = cell["model"]["id"]

        try:
            response_text = provider_fn(user_prompt, cell["model"])
            scores = parse_scores(response_text)

            record = {
                "cell_id": cell["cell_id"],
                "portfolio": cell["portfolio_key"],
                "brand": brand,
                "category": cell["category"],
                "condition": cell["condition"],
                "language": cell["language"],
                "language_name": cell["language_name"],
                "model_id": mid,
                "model_name": cell["model"]["name"],
                "provider": cell["model"]["provider"],
                "tradition": cell["model"]["tradition"],
                "temperature": cell["model"]["temperature"],
                "repetition": cell["repetition"],
                "prompt": user_prompt,
                "system_prompt": None,
                "response": response_text,
                "scores": scores,
                "parse_success": scores is not None,
                "scale": "1-5",
                "version": "2.0",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            with open(output_file, "w") as f:
                json.dump(record, f, indent=2)

            completed += 1
            status = "OK" if scores else "PARSE_FAIL"
            n_done = completed + skipped + errors
            print(
                f"[{n_done}/{total}] {cell['cell_id']} {status}"
                + (f" scores={list(scores.values())}" if scores else "")
            )

            provider = cell["model"]["provider"]
            if provider == "ollama":
                time.sleep(0.1)
            elif provider in ("groq", "xai"):
                time.sleep(1.0)
            elif provider in ("cerebras", "mistral"):
                time.sleep(0.5)
            elif provider == "yandex":
                time.sleep(1.5)
            elif provider == "sarvam":
                time.sleep(1.0)
            else:
                time.sleep(0.5)

        except Exception as e:
            errors += 1
            n_done = completed + skipped + errors
            print(f"[{n_done}/{total}] {cell['cell_id']} ERROR: {e}")

    print(
        f"\nComplete: {completed} new, {skipped} skipped, {errors} errors, {total} total"
    )


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="R20 Portfolio-AI Experiment")
    parser.add_argument(
        "--model",
        choices=[m["id"] for m in MODELS],
        help="Run single model only",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print prompts without calling APIs",
    )
    parser.add_argument(
        "--reparse",
        action="store_true",
        help="Re-parse failed responses",
    )
    parser.add_argument(
        "--ablation",
        action="store_true",
        help="Run system-prompt ablation (4 proven models only)",
    )
    parser.add_argument(
        "--recommendation",
        action="store_true",
        help="Run recommendation prompt conditions (solo + portfolio)",
    )
    parser.add_argument(
        "--multiturn",
        action="store_true",
        help="Run multi-turn experiment (Turn 1 solo, Turn 2 reveal + re-rate)",
    )
    parser.add_argument(
        "--native",
        action="store_true",
        help="Run native-language ablation (home portfolios in native language)",
    )
    args = parser.parse_args()

    if args.reparse:
        reparse_failures()
    elif args.multiturn:
        run_multiturn(model_filter=args.model, dry_run=args.dry_run)
    elif args.native:
        run_native_language(model_filter=args.model, dry_run=args.dry_run)
    elif args.recommendation:
        # Recommendation uses the same runner with different conditions
        run_experiment(
            model_filter=args.model,
            dry_run=args.dry_run,
            ablation=False,
            conditions=["recommendation_solo", "recommendation_portfolio"],
        )
    else:
        run_experiment(
            model_filter=args.model, dry_run=args.dry_run, ablation=args.ablation
        )
