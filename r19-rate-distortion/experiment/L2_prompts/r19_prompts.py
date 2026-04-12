"""R19 Rate-Distortion Sweep — Prompt Templates.

Five prompt templates, one per rate condition (R1-R5). All English only.
All expect JSON responses with a known schema.

Rate conditions:
  R1 (~26 bits): 100-point allocation across 8 dimensions
  R2 (~19 bits): 1-5 scale rating for each dimension
  R3 (~13 bits): Low/Medium/High classification for each dimension
  R4 (~8 bits):  Yes/No binary for each dimension
  R5 (~3 bits):  Single most important dimension
"""

from __future__ import annotations

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

# -------------------------------------------------------------------------------
# Dimension description block (English)
# -------------------------------------------------------------------------------

DIM_DESCRIPTIONS = {
    "semiotic": "Visual identity, logo, design system, packaging",
    "narrative": "Brand story, founding narrative, purpose and mission",
    "ideological": "Values, ethics, social stance, sustainability",
    "experiential": "Customer experience quality, service, touchpoints",
    "social": "Social signaling, community, status meaning",
    "economic": "Price point, value-for-money, accessibility",
    "cultural": "Cultural significance, connections to traditions",
    "temporal": "Heritage, longevity, historical depth",
}


def _dim_block_r1() -> str:
    """Dimension block for R1 (100-point allocation)."""
    lines = []
    for dim in DIMENSIONS:
        lines.append(f"- {dim}: {DIM_DESCRIPTIONS[dim]}")
    return "\n".join(lines)


def _dim_block_r2() -> str:
    """Dimension block for R2 (1-5 rating)."""
    lines = []
    for dim in DIMENSIONS:
        lines.append(f"- {dim}: {DIM_DESCRIPTIONS[dim]}")
    return "\n".join(lines)


def _dim_block_r3() -> str:
    """Dimension block for R3 (Low/Medium/High)."""
    lines = []
    for dim in DIMENSIONS:
        lines.append(f"- {dim}: {DIM_DESCRIPTIONS[dim]}")
    return "\n".join(lines)


def _dim_block_r4() -> str:
    """Dimension block for R4 (Yes/No binary)."""
    lines = []
    for dim in DIMENSIONS:
        lines.append(f"- {dim}: {DIM_DESCRIPTIONS[dim]}")
    return "\n".join(lines)


def _dim_block_r5() -> str:
    """Dimension block for R5 (single dimension)."""
    dims_str = ", ".join(DIMENSIONS)
    return f"The eight dimensions are: {dims_str}.\n\n" + "\n".join(
        f"- {dim}: {DIM_DESCRIPTIONS[dim]}" for dim in DIMENSIONS
    )


# -------------------------------------------------------------------------------
# Prompt template: R1 — 100-point allocation
# -------------------------------------------------------------------------------

R1_TEMPLATE = """\
You are a brand research assistant analyzing how AI systems encode brand perception.

Your task: Allocate exactly 100 points across the 8 brand perception dimensions below
to reflect the relative importance of each dimension in how {brand} is perceived and
communicated in the marketplace.

The 8 dimensions:
{dim_block}

Rules:
- The 8 values in "weights" MUST sum to exactly 100.
- Each value must be a number (integer or decimal), minimum 0.
- Respond with valid JSON only — no commentary outside the JSON.

Respond ONLY with valid JSON in this exact format:
{{"weights": {{"semiotic": N, "narrative": N, "ideological": N, "experiential": N, "social": N, "economic": N, "cultural": N, "temporal": N}}, "reasoning": "brief explanation"}}"""


def build_r1_prompt(brand: str) -> str:
    return R1_TEMPLATE.format(brand=brand, dim_block=_dim_block_r1())


# -------------------------------------------------------------------------------
# Prompt template: R2 — 1-5 scale rating
# -------------------------------------------------------------------------------

R2_TEMPLATE = """\
You are a brand research assistant analyzing how AI systems encode brand perception.

Your task: Rate each of the 8 brand perception dimensions below on a scale of 1 to 5,
reflecting how strongly {brand} exhibits or is associated with each dimension.

Scale: 1 = Very low / barely present, 3 = Moderate presence, 5 = Very high / dominant

The 8 dimensions:
{dim_block}

Rules:
- Each value in "ratings" must be an integer: 1, 2, 3, 4, or 5.
- You must rate ALL 8 dimensions.
- Respond with valid JSON only — no commentary outside the JSON.

Respond ONLY with valid JSON in this exact format:
{{"ratings": {{"semiotic": N, "narrative": N, "ideological": N, "experiential": N, "social": N, "economic": N, "cultural": N, "temporal": N}}, "reasoning": "brief explanation"}}"""


def build_r2_prompt(brand: str) -> str:
    return R2_TEMPLATE.format(brand=brand, dim_block=_dim_block_r2())


# -------------------------------------------------------------------------------
# Prompt template: R3 — Low/Medium/High classification
# -------------------------------------------------------------------------------

R3_TEMPLATE = """\
You are a brand research assistant analyzing how AI systems encode brand perception.

Your task: For each of the 8 brand perception dimensions below, classify how strongly
{brand} exhibits that dimension as: Low, Medium, or High.

- Low: The dimension is weak or barely present for this brand
- Medium: The dimension is moderately present
- High: The dimension is strongly present or central to the brand

The 8 dimensions:
{dim_block}

Rules:
- Each value in "classifications" must be exactly one of: "Low", "Medium", or "High"
- You must classify ALL 8 dimensions.
- Respond with valid JSON only — no commentary outside the JSON.

Respond ONLY with valid JSON in this exact format:
{{"classifications": {{"semiotic": "Low/Medium/High", "narrative": "Low/Medium/High", "ideological": "Low/Medium/High", "experiential": "Low/Medium/High", "social": "Low/Medium/High", "economic": "Low/Medium/High", "cultural": "Low/Medium/High", "temporal": "Low/Medium/High"}}, "reasoning": "brief explanation"}}"""


def build_r3_prompt(brand: str) -> str:
    return R3_TEMPLATE.format(brand=brand, dim_block=_dim_block_r3())


# -------------------------------------------------------------------------------
# Prompt template: R4 — Yes/No binary
# -------------------------------------------------------------------------------

R4_TEMPLATE = """\
You are a brand research assistant analyzing how AI systems encode brand perception.

Your task: For each of the 8 brand perception dimensions below, answer whether {brand}
strongly emits that dimension (true) or does not (false).

- true: The brand strongly exhibits this dimension as a defining characteristic
- false: This dimension is not a defining characteristic of the brand

The 8 dimensions:
{dim_block}

Rules:
- Each value in "present" must be exactly true or false (boolean).
- You must answer for ALL 8 dimensions.
- Respond with valid JSON only — no commentary outside the JSON.

Respond ONLY with valid JSON in this exact format:
{{"present": {{"semiotic": true/false, "narrative": true/false, "ideological": true/false, "experiential": true/false, "social": true/false, "economic": true/false, "cultural": true/false, "temporal": true/false}}, "reasoning": "brief explanation"}}"""


def build_r4_prompt(brand: str) -> str:
    return R4_TEMPLATE.format(brand=brand, dim_block=_dim_block_r4())


# -------------------------------------------------------------------------------
# Prompt template: R5 — Single most important dimension
# -------------------------------------------------------------------------------

R5_TEMPLATE = """\
You are a brand research assistant analyzing how AI systems encode brand perception.

Your task: From the 8 brand perception dimensions below, identify the SINGLE most
important dimension that defines how {brand} is perceived and what makes it distinctive.

{dim_block}

Rules:
- "top_dimension" must be exactly ONE of the 8 dimension names listed above.
- Choose the single most defining dimension for this brand.
- Respond with valid JSON only — no commentary outside the JSON.

Respond ONLY with valid JSON in this exact format:
{{"top_dimension": "dimension_name", "reasoning": "brief explanation"}}"""


def build_r5_prompt(brand: str) -> str:
    return R5_TEMPLATE.format(brand=brand, dim_block=_dim_block_r5())


# -------------------------------------------------------------------------------
# Dispatch
# -------------------------------------------------------------------------------

PROMPT_BUILDERS = {
    "R1": build_r1_prompt,
    "R2": build_r2_prompt,
    "R3": build_r3_prompt,
    "R4": build_r4_prompt,
    "R5": build_r5_prompt,
}

RATE_BITS = {
    "R1": 26,
    "R2": 19,
    "R3": 13,
    "R4": 8,
    "R5": 3,
}


def build_prompt(rate_condition: str, brand: str) -> str:
    """Build the prompt for a given rate condition and brand."""
    builder = PROMPT_BUILDERS.get(rate_condition)
    if builder is None:
        raise ValueError(f"Unknown rate condition: {rate_condition!r}")
    return builder(brand)
