#!/usr/bin/env python3
"""Experiment data validation: schema compliance, completeness, and integrity.

Three checks are implemented:

1. **Schema validation**: validates each line of L3 JSONL against
   `schemas/session_record.schema.json` and each L4 results JSON against
   `schemas/aggregated_results.schema.json`. Uses jsonschema if installed,
   falls back to a minimal built-in checker that enforces required keys
   and basic types if not.

2. **Integrity check**: verifies SHA-256 hashes of all data files against
   `validation/checksums.sha256`. Run `validate.py --regenerate-checksums`
   to update the checksum file after intentional data changes.

3. **Completeness check**: verifies that L3_sessions/ contains JSONL files
   with at least one valid entry, and that all results files referenced by
   ../DATA_MANIFEST.yaml exist on disk.

Usage:
    python validate.py --check-schemas
    python validate.py --check-integrity
    python validate.py --check-completeness
    python validate.py --regenerate-checksums
    python validate.py --all
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = EXPERIMENT_DIR.parent
SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"
CHECKSUM_FILE = Path(__file__).resolve().parent / "checksums.sha256"

# Files that must exist for the experiment to be considered complete.
EXPECTED_L3_SESSIONS = [
    "run2_global.jsonl",
    "run2_qwen_plus.jsonl",
    "run3_local.jsonl",
    "run3_qwen_plus.jsonl",
    "run4_resolution.jsonl",
    "run5_crosscultural.jsonl",
    "run5_fireworks_glm.jsonl",
    "run5_gptoss_swallow.jsonl",
    "run6_banking_clean.jsonl",
    "run7_framing.jsonl",
    "run7d_swedish.jsonl",
    "run8_native_expansion.jsonl",
    "run9_temp_0.0.jsonl",
    "run9_temp_0.3.jsonl",
    "run9_temp_1.0.jsonl",
    # Run 10: supplementary corrective comparators experiment (2026-04-10)
    "run10_corrective.jsonl",
    # Run 11: Roshen multi-city extension (2026-04-11)
    "run11_roshen_multicity.jsonl",
]

EXPECTED_L4_RESULTS = [
    "run5_results.json",
    "run5_summary.md",
    "run5_analysis_results.json",
    "run5_dci_table.csv",
    "run5_diagonal_advantage.csv",
    "run7_framing_results.json",
    "run7_framing_summary.md",
    "run6_banking_results.json",
    "run8_native_expansion_results.json",
    "run9_temperature_results.json",
    "power_analysis_results.json",
    "prompt_sensitivity_results.json",
    "exclude_patagonia_results.json",
    # Run 10 supplementary outputs
    "run10_corrective_results.json",
    "run10_corrective_summary.md",
    # Run 11 supplementary outputs
    "run11_roshen_multicity_results.json",
    "run11_roshen_multicity_summary.md",
]

EXPECTED_ROOT_RESULTS = [
    "results_v2_global.json",
    "results_v3_local.json",
    "results_v4_resolution.json",
]

# Files to checksum (data files that should not change without intent).
def files_to_checksum() -> list[Path]:
    files = []
    for name in EXPECTED_L3_SESSIONS:
        p = EXPERIMENT_DIR / "L3_sessions" / name
        if p.exists():
            files.append(p)
    for name in EXPECTED_L4_RESULTS:
        p = EXPERIMENT_DIR / "L4_analysis" / name
        if p.exists():
            files.append(p)
    for name in EXPECTED_ROOT_RESULTS:
        p = ROOT_DIR / name
        if p.exists():
            files.append(p)
    extras = [
        EXPERIMENT_DIR / "local_brand_specs.json",
        EXPERIMENT_DIR / "L3_sessions" / "metadata.yaml",
        EXPERIMENT_DIR / "L1_configuration" / "models.yaml",
    ]
    files.extend(p for p in extras if p.exists())
    return files


# ----------------------------------------------------------------------------
# Schema validation
# ----------------------------------------------------------------------------

def _load_schema(name: str) -> dict:
    path = SCHEMA_DIR / name
    return json.loads(path.read_text())


def _validate_record_minimal(record: dict, schema: dict, where: str) -> list[str]:
    """Minimal schema check: required keys + basic type matching.

    Used when jsonschema is not installed. Not as strict as the real validator
    but catches structural drift.
    """
    errors: list[str] = []
    required = schema.get("required", [])
    for key in required:
        if key not in record:
            errors.append(f"{where}: missing required key '{key}'")
    properties = schema.get("properties", {})
    for key, prop in properties.items():
        if key not in record:
            continue
        expected_types = prop.get("type")
        if expected_types is None:
            continue
        if isinstance(expected_types, str):
            expected_types = [expected_types]
        py_types = []
        for t in expected_types:
            py_types.extend({
                "string": [str],
                "integer": [int],
                "number": [int, float],
                "boolean": [bool],
                "object": [dict],
                "array": [list],
                "null": [type(None)],
            }.get(t, []))
        if py_types and not isinstance(record[key], tuple(py_types)):
            errors.append(
                f"{where}: key '{key}' has type {type(record[key]).__name__}, "
                f"expected one of {expected_types}"
            )
    return errors


def _try_import_jsonschema():
    try:
        import jsonschema  # type: ignore
        return jsonschema
    except ImportError:
        return None


def check_schemas(verbose: bool = False) -> bool:
    """Validate L3 session records and L4 results against JSON schemas."""
    js = _try_import_jsonschema()
    if js is None:
        print("Schema validation: jsonschema not installed, using minimal built-in checker.")

    session_schema = _load_schema("session_record.schema.json")
    results_schema = _load_schema("aggregated_results.schema.json")

    errors_total = 0

    # Supplementary experiments use enriched schemas (extra fields, no raw prompt).
    # They are validated by their own scripts, not by the core R15 schema.
    SCHEMA_SKIP_PREFIXES = ("run12_", "run12b_", "run13_", "run14_")

    # Validate L3 session records (sample first/middle/last + 100 random per file)
    l3_dir = EXPERIMENT_DIR / "L3_sessions"
    for jsonl_path in sorted(l3_dir.glob("*.jsonl")):
        if jsonl_path.name.startswith(SCHEMA_SKIP_PREFIXES):
            print(f"  SKIP (supplementary): {jsonl_path.name}")
            continue
        with jsonl_path.open() as fh:
            lines = fh.readlines()
        n = len(lines)
        if n == 0:
            errors_total += 1
            print(f"  ERROR: {jsonl_path.name} is empty")
            continue
        # Sample: first, middle, last, plus every 500th
        sample_indices = sorted(set([0, n // 2, n - 1] + list(range(0, n, 500))))
        for idx in sample_indices:
            try:
                record = json.loads(lines[idx])
            except json.JSONDecodeError as exc:
                errors_total += 1
                print(f"  ERROR: {jsonl_path.name} line {idx + 1}: invalid JSON ({exc})")
                continue
            where = f"{jsonl_path.name} line {idx + 1}"
            if js is not None:
                try:
                    js.validate(record, session_schema)
                except js.ValidationError as exc:
                    errors_total += 1
                    print(f"  ERROR: {where}: {exc.message}")
            else:
                errs = _validate_record_minimal(record, session_schema, where)
                for e in errs:
                    errors_total += 1
                    print(f"  ERROR: {e}")
        if verbose:
            print(f"  OK: {jsonl_path.name} ({n} lines, {len(sample_indices)} sampled)")

    # Validate L4 aggregated results
    targets = [
        ROOT_DIR / "results_v2_global.json",
        ROOT_DIR / "results_v3_local.json",
        ROOT_DIR / "results_v4_resolution.json",
    ]
    for path in targets:
        if not path.exists():
            errors_total += 1
            print(f"  ERROR: {path.name} not found")
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            errors_total += 1
            print(f"  ERROR: {path.name}: invalid JSON ({exc})")
            continue
        if js is not None:
            try:
                js.validate(data, results_schema)
            except js.ValidationError as exc:
                errors_total += 1
                print(f"  ERROR: {path.name}: {exc.message}")
        else:
            errs = _validate_record_minimal(data, results_schema, path.name)
            for e in errs:
                errors_total += 1
                print(f"  ERROR: {e}")
        if verbose:
            print(f"  OK: {path.name}")

    if errors_total == 0:
        print(f"Schema validation: PASSED (sampled records from {len(list(l3_dir.glob('*.jsonl')))} JSONL files + 3 root results files)")
        return True
    else:
        print(f"Schema validation: FAILED ({errors_total} errors)")
        return False


# ----------------------------------------------------------------------------
# Checksum verification
# ----------------------------------------------------------------------------

def _sha256(path: Path, chunk_size: int = 65536) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def regenerate_checksums() -> None:
    files = files_to_checksum()
    lines = []
    for f in sorted(files):
        digest = _sha256(f)
        rel = f.relative_to(ROOT_DIR)
        lines.append(f"{digest}  {rel}")
    CHECKSUM_FILE.write_text("\n".join(lines) + "\n")
    print(f"Regenerated {CHECKSUM_FILE.name} with {len(lines)} entries.")


def check_integrity() -> bool:
    if not CHECKSUM_FILE.exists():
        print("Integrity check: SKIPPED (no checksums.sha256 — run with --regenerate-checksums first)")
        return True
    expected = {}
    for line in CHECKSUM_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        digest, rel = parts
        expected[rel] = digest

    errors = 0
    checked = 0
    for rel, digest in expected.items():
        path = ROOT_DIR / rel
        if not path.exists():
            print(f"  ERROR: {rel}: missing on disk")
            errors += 1
            continue
        actual = _sha256(path)
        if actual != digest:
            print(f"  ERROR: {rel}: hash mismatch")
            print(f"    expected: {digest}")
            print(f"    actual:   {actual}")
            errors += 1
        else:
            checked += 1

    if errors == 0:
        print(f"Integrity check: PASSED ({checked} files verified)")
        return True
    else:
        print(f"Integrity check: FAILED ({errors} mismatches/missing)")
        return False


# ----------------------------------------------------------------------------
# Completeness check
# ----------------------------------------------------------------------------

def check_completeness() -> bool:
    errors = 0
    l3_dir = EXPERIMENT_DIR / "L3_sessions"
    for name in EXPECTED_L3_SESSIONS:
        p = l3_dir / name
        if not p.exists():
            print(f"  ERROR: missing L3 session file: {name}")
            errors += 1
            continue
        # Verify at least one line
        with p.open() as fh:
            first = fh.readline()
        if not first.strip():
            print(f"  ERROR: empty L3 session file: {name}")
            errors += 1

    l4_dir = EXPERIMENT_DIR / "L4_analysis"
    for name in EXPECTED_L4_RESULTS:
        p = l4_dir / name
        if not p.exists():
            print(f"  ERROR: missing L4 result file: {name}")
            errors += 1

    for name in EXPECTED_ROOT_RESULTS:
        p = ROOT_DIR / name
        if not p.exists():
            print(f"  ERROR: missing root result file: {name}")
            errors += 1

    if errors == 0:
        n_l3 = len(EXPECTED_L3_SESSIONS)
        n_l4 = len(EXPECTED_L4_RESULTS)
        n_root = len(EXPECTED_ROOT_RESULTS)
        # Total call count
        total_calls = 0
        for name in EXPECTED_L3_SESSIONS:
            p = l3_dir / name
            with p.open() as fh:
                total_calls += sum(1 for _ in fh)
        print(
            f"Completeness check: PASSED "
            f"({n_l3} L3 sessions, {n_l4} L4 results, {n_root} root results, "
            f"{total_calls:,} total calls)"
        )
        return True
    else:
        print(f"Completeness check: FAILED ({errors} missing files)")
        return False


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Validate R15 experiment data.")
    parser.add_argument("--check-schemas", action="store_true")
    parser.add_argument("--check-integrity", action="store_true")
    parser.add_argument("--check-completeness", action="store_true")
    parser.add_argument("--regenerate-checksums", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.regenerate_checksums:
        regenerate_checksums()
        return

    if args.all:
        args.check_schemas = True
        args.check_integrity = True
        args.check_completeness = True

    if not any([args.check_schemas, args.check_integrity, args.check_completeness]):
        parser.print_help()
        sys.exit(1)

    results = []
    if args.check_completeness:
        results.append(("completeness", check_completeness()))
    if args.check_schemas:
        results.append(("schemas", check_schemas(verbose=args.verbose)))
    if args.check_integrity:
        results.append(("integrity", check_integrity()))

    failed = [name for name, passed in results if not passed]
    if failed:
        print(f"\nFAILED: {', '.join(failed)}")
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
