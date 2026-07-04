#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""score_stage1.py — PRISM-O (2026bd) Stage-1 H1(i) scoring + gate verdict.

Reads data/stage1_records.jsonl and reports, per operator pair and pooled:
- MACRO accuracy (mean per-rung recall over the five truth classes) for the
  FULL bank (as registered) and for the 14 HELD-OUT bases (B13-B26; B01-B12
  are worked examples embedded in the classifier prompt — anchored subset);
- per-rung recall table; malformed / segmenter-count flags;
- masked-vs-named agreement (contamination bound on identical text);
- Stage-2 gate verdict, frozen rule: BOTH full-bank macro >= .80 AND
  held-out macro >= .80 for EVERY Stage-1 operator pair.

Also aggregates PL3 cost telemetry (tokens + cost) into the Stage-2 estimate
inputs. Writes data/pl4_stage1_results.json + data/STAGE1_REPORT.md.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_o_lib import (  # noqa: E402
    DATA_DIR,
    LOGS_DIR,
    RUNGS,
    load_records,
)

GATE = 0.80


def macro_accuracy(records: list[dict]) -> tuple[float, dict]:
    by_rung: dict[str, list[int]] = defaultdict(list)
    for r in records:
        by_rung[r["rung_truth"]].append(1 if r["rung_pred"] == r["rung_truth"] else 0)
    per_rung = {k: (sum(v) / len(v), len(v)) for k, v in sorted(by_rung.items())}
    macro = sum(acc for acc, _ in per_rung.values()) / len(per_rung) if per_rung else float("nan")
    return macro, per_rung


def main() -> int:
    records = load_records(DATA_DIR / "stage1_records.jsonl")
    pairs = sorted({r["op_pair"] for r in records})
    results: dict = {"pairs": {}, "pooled": {}, "gate": {}}

    def block(recs):
        full_macro, full_rungs = macro_accuracy(recs)
        held = [r for r in recs if not r["anchored"]]
        held_macro, held_rungs = macro_accuracy(held)
        named = {(r["base_id"]): r["rung_pred"] for r in recs if r["variant"] == "named"}
        masked = {(r["base_id"]): r["rung_pred"] for r in recs if r["variant"] == "masked"}
        common = sorted(set(named) & set(masked))
        agree = [1 if named[b] == masked[b] else 0 for b in common]
        return {
            "n_records": len(recs),
            "full_macro": round(full_macro, 4),
            "full_per_rung": {k: {"recall": round(a, 4), "n": n} for k, (a, n) in full_rungs.items()},
            "heldout_macro": round(held_macro, 4),
            "heldout_per_rung": {k: {"recall": round(a, 4), "n": n} for k, (a, n) in held_rungs.items()},
            "masked_named_agreement": round(sum(agree) / len(agree), 4) if agree else None,
            "masked_named_n": len(agree),
            "malformed": sum(1 for r in recs if r["rung_pred"] == "MALFORMED"),
            "segmenter_count_ne_1": sum(1 for r in recs if r["n_interventions_detected"] != 1),
        }

    for p in pairs:
        results["pairs"][p] = block([r for r in records if r["op_pair"] == p])
    results["pooled"] = block(records)

    gate_pass = all(
        results["pairs"][p]["full_macro"] >= GATE and results["pairs"][p]["heldout_macro"] >= GATE
        for p in pairs
    )
    results["gate"] = {
        "rule": f"full_macro >= {GATE} AND heldout_macro >= {GATE} for every Stage-1 pair",
        "pass": gate_pass,
    }

    # PL3 cost telemetry. The logger's derived `tokens` field is empty for
    # this run (extraction gap in the shared layer, logged upstream); the raw
    # usage is intact in response_metadata.usage — read that, both provider
    # shapes, and price from the PL1 list-price table.
    from prism_o_lib import load_config, usage_from_log_record  # noqa: E402

    prices = load_config()["list_prices"]
    total_cost, total_in, total_out, n_calls = 0.0, 0, 0, 0
    for f in LOGS_DIR.glob("*.jsonl"):
        with f.open() as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                n_calls += 1
                tin, tout = usage_from_log_record(rec)
                total_in += tin
                total_out += tout
                model = rec.get("operator") or rec.get("model_version") or ""
                p = prices.get(model)
                if p:
                    total_cost += (tin * p["input"] + tout * p["output"]) / 1_000_000
    results["telemetry"] = {
        "calls": n_calls,
        "tokens_in": total_in,
        "tokens_out": total_out,
        "cost_usd_est": round(total_cost, 4),
        "mean_tokens_in_per_call": round(total_in / n_calls) if n_calls else None,
        "mean_tokens_out_per_call": round(total_out / n_calls) if n_calls else None,
    }

    (DATA_DIR / "pl4_stage1_results.json").write_text(json.dumps(results, indent=2))

    lines = [
        "# PRISM-O Stage-1 Report (H1(i) gate)",
        "",
        f"Records: {results['pooled']['n_records']} | calls: {n_calls} | "
        f"spend: ${results['telemetry']['cost_usd_est']:.2f}",
        "",
        "| pair | full macro | held-out macro | masked=named | malformed | seg!=1 |",
        "|---|---|---|---|---|---|",
    ]
    for p in pairs:
        b = results["pairs"][p]
        lines.append(
            f"| {p} | {b['full_macro']:.3f} | {b['heldout_macro']:.3f} | "
            f"{b['masked_named_agreement']} | {b['malformed']} | {b['segmenter_count_ne_1']} |"
        )
    b = results["pooled"]
    lines += [
        f"| pooled | {b['full_macro']:.3f} | {b['heldout_macro']:.3f} | "
        f"{b['masked_named_agreement']} | {b['malformed']} | {b['segmenter_count_ne_1']} |",
        "",
        f"**Stage-2 gate ({results['gate']['rule']}): "
        f"{'PASS' if results['gate']['pass'] else 'FAIL'}**",
        "",
        "Per-rung recall (pooled, full bank): "
        + ", ".join(
            f"{k} {v['recall']:.2f} (n={v['n']})"
            for k, v in results["pooled"]["full_per_rung"].items()
        ),
        "",
        "Per-rung recall (pooled, held-out): "
        + ", ".join(
            f"{k} {v['recall']:.2f} (n={v['n']})"
            for k, v in results["pooled"]["heldout_per_rung"].items()
        ),
    ]
    (DATA_DIR / "STAGE1_REPORT.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    sys.exit(main())
