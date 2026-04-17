#!/usr/bin/env python3
"""Qwen3 235B supplement for Compounding x Format v2.

Replaces Claude (which refused constraint/step_3 due to ethical override)
with Qwen3 235B via Groq (free endpoint). Runs all 3 conditions.
"""
import json, os, time, hashlib, re, uuid, datetime
from pathlib import Path
from openai import OpenAI

TEMPERATURE = 0.7
MAX_TOKENS = 512
MAX_TOKENS_STEP1 = 1024
DIMENSIONS = ["Semiotic","Narrative","Ideological","Experiential","Social","Economic","Cultural","Temporal"]

BRANDS = {
    "Hermes": {"category": "luxury fashion"},
    "Patagonia": {"category": "outdoor apparel"},
    "Erewhon": {"category": "grocery retail"},
    "Tesla": {"category": "electric vehicles"},
    "IKEA": {"category": "home furnishing"},
}

SYSTEM_PROMPT_PIPELINE = "You are a helpful AI shopping assistant."
SYSTEM_PROMPT_CONTROL = "You are evaluating brand perception."

CONSTRAINT_TEXT = """When evaluating brands, you must distribute your attention equally across all eight perceptual dimensions: Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, and Temporal. Do not over-weight any single dimension. Each dimension is equally important for a complete brand evaluation. Avoid defaulting to price or product features — heritage, values, cultural resonance, and social meaning are equally valid evaluation criteria."""

BF_DIR = Path(__file__).parent.parent / "L1_configuration" / "brand_functions"
OUTFILE = Path(__file__).parent.parent / "L3_sessions" / "exp_compounding_format_v2_qwen_supplement.jsonl"

client = OpenAI(api_key=os.environ["CEREBRAS_API_KEY"], base_url="https://api.cerebras.ai/v1")
MODEL_ID = "qwen-3-235b-a22b-instruct-2507"


def call_api(messages, max_tok):
    resp = client.chat.completions.create(
        model=MODEL_ID, messages=messages, temperature=TEMPERATURE, max_tokens=max_tok
    )
    return resp.choices[0].message.content


def load_bf(brand):
    slug = brand.lower().replace(" ", "_")
    p = BF_DIR / f"{slug}.json"
    if p.exists():
        return json.loads(p.read_text())
    return None


def format_bf(bf):
    lines = [f"BRAND SPECIFICATION: {bf['brand']}"]
    for dim in [d.lower() for d in DIMENSIONS]:
        dd = bf.get("dimensions", {}).get(dim, {})
        lines.append(f"{dim.upper()} ({dd.get('score','N/A')}/10): {dd.get('positioning','')}")
    return "\n".join(lines)


def build_sys(condition, brand, base):
    if condition == "baseline":
        return base
    elif condition == "information":
        bf = load_bf(brand)
        if bf:
            return (
                f"You have access to the following verified brand specification for "
                f"{brand}. Use this information when evaluating the brand.\n\n"
                f"{format_bf(bf)}\n\n---\n\n{base}"
            )
        return base
    elif condition == "constraint":
        return CONSTRAINT_TEXT + "\n\n---\n\n" + base
    return base


def parse_weights(text):
    for pattern in [r'\{[^{}]*"weights"[^{}]*\{[^{}]+\}[^{}]*\}', r'\{[^{}]+\}']:
        matches = re.findall(pattern, text, re.DOTALL)
        for m in matches:
            try:
                p = json.loads(m)
                if "weights" in p:
                    p = p["weights"]
                if len(p) >= 7:
                    w = {k: float(v) for k, v in p.items() if isinstance(v, (int, float))}
                    if len(w) >= 7:
                        return w, True
            except Exception:
                continue
    return None, False


def main():
    count = 0
    valid_wb = 0
    total_wb = 0

    print(f"Qwen3 235B supplement: 3 conditions x 5 brands x 2 reps")
    print(f"Expected: 30 pipelines (90 steps) + 30 controls = 120 calls")
    print()

    for condition in ["baseline", "information", "constraint"]:
        for brand_name in BRANDS:
            for rep in range(1, 3):
                bidx = list(BRANDS.keys()).index(brand_name)
                dim_order = DIMENSIONS[(bidx + rep) % 8 :] + DIMENSIONS[: (bidx + rep) % 8]

                # Pipeline
                sys_p = build_sys(condition, brand_name, SYSTEM_PROMPT_PIPELINE)
                conv_id = str(uuid.uuid4())
                history = [{"role": "system", "content": sys_p}]

                for step in range(1, 4):
                    cat = BRANDS[brand_name]["category"]
                    if step == 1:
                        prompt = (
                            f"I am shopping for products in the {cat} category. "
                            f"Can you recommend 5 brands I should consider? "
                            f"For each brand, briefly explain what makes it distinctive."
                        )
                        max_tok = MAX_TOKENS_STEP1
                    elif step == 2:
                        prompt = (
                            f"Now compare {brand_name} specifically against one of the "
                            f"other brands you mentioned. Allocate 100 points across these "
                            f"8 dimensions to show how {brand_name} is perceived: "
                            f"{', '.join(dim_order)}. Return JSON."
                        )
                        max_tok = MAX_TOKENS
                    else:
                        prompt = (
                            f"Based on our conversation, make your final recommendation. "
                            f"Allocate 100 points across the same 8 dimensions for your "
                            f"recommended brand: {', '.join(dim_order)}. Return JSON."
                        )
                        max_tok = MAX_TOKENS

                    history.append({"role": "user", "content": prompt})
                    start = time.time()
                    try:
                        response = call_api(history, max_tok)
                    except Exception as e:
                        response = f"ERROR: {e}"
                    elapsed = int((time.time() - start) * 1000)
                    history.append({"role": "assistant", "content": response})

                    weights, valid = (None, False) if step == 1 else parse_weights(response)
                    if step >= 2:
                        total_wb += 1
                        if valid:
                            valid_wb += 1

                    record = {
                        "experiment": "exp_compounding_format_v2_qwen_supplement",
                        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                        "model_id": MODEL_ID,
                        "model_provider": "cerebras",
                        "brand": brand_name,
                        "condition": f"step_{step}",
                        "bf_condition": condition,
                        "repetition": rep,
                        "system_prompt_hash": hashlib.sha256(sys_p.encode()).hexdigest()[:16],
                        "user_prompt": prompt,
                        "raw_response": response[:2000],
                        "parsed_weights": weights,
                        "weights_valid": valid,
                        "response_time_ms": elapsed,
                        "conversation_id": conv_id,
                        "conversation_turn": step,
                        "dim_order": dim_order,
                    }
                    with open(OUTFILE, "a") as f:
                        f.write(json.dumps(record) + "\n")

                    status = "OK" if valid else ("--" if step == 1 else "FAIL")
                    print(
                        f"  [{condition[:4]}] {brand_name:<10} step{step} rep{rep} "
                        f"-> {status} ({elapsed}ms)"
                    )
                    count += 1
                    time.sleep(1)

                # Control
                sys_c = build_sys(condition, brand_name, SYSTEM_PROMPT_CONTROL)
                ctrl_prompt = (
                    f"Evaluate the brand {brand_name} across 8 perceptual dimensions. "
                    f"Allocate 100 points: {', '.join(dim_order)}. Return JSON."
                )
                start = time.time()
                try:
                    ctrl_resp = call_api(
                        [{"role": "system", "content": sys_c}, {"role": "user", "content": ctrl_prompt}],
                        MAX_TOKENS,
                    )
                except Exception as e:
                    ctrl_resp = f"ERROR: {e}"
                elapsed = int((time.time() - start) * 1000)
                weights, valid = parse_weights(ctrl_resp)
                total_wb += 1
                if valid:
                    valid_wb += 1

                record = {
                    "experiment": "exp_compounding_format_v2_qwen_supplement",
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "model_id": MODEL_ID,
                    "model_provider": "cerebras",
                    "brand": brand_name,
                    "condition": "control",
                    "bf_condition": condition,
                    "repetition": rep,
                    "system_prompt_hash": hashlib.sha256(sys_c.encode()).hexdigest()[:16],
                    "user_prompt": ctrl_prompt,
                    "raw_response": ctrl_resp[:2000],
                    "parsed_weights": weights,
                    "weights_valid": valid,
                    "response_time_ms": elapsed,
                    "dim_order": dim_order,
                }
                with open(OUTFILE, "a") as f:
                    f.write(json.dumps(record) + "\n")

                status = "OK" if valid else "FAIL"
                print(f"  [{condition[:4]}] {brand_name:<10} ctrl  rep{rep} -> {status} ({elapsed}ms)")
                count += 1
                time.sleep(1)

    print(f"\nDone. {count} calls. Valid weight-bearing: {valid_wb}/{total_wb} ({100*valid_wb/total_wb:.0f}%)")
    print(f"Output: {OUTFILE}")


if __name__ == "__main__":
    main()
