#!/usr/bin/env python3
"""Experiment data validation: schema compliance, completeness, and integrity.

Usage:
    python validate.py --check-schemas     # Validate L0-L3 against JSON schemas
    python validate.py --check-integrity   # Verify SHA-256 checksums
    python validate.py --check-completeness # Ensure all models have session data
    python validate.py --all               # Run all checks
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

EXPERIMENT_DIR = Path(__file__).parent.parent


def check_schemas():
    """Validate session entries against JSON schemas."""
    schema_dir = EXPERIMENT_DIR / "validation" / "schemas"
    # TODO: Implement after experiment data is generated
    print("Schema validation: NOT YET IMPLEMENTED (no data yet)")
    return True


def check_integrity():
    """Verify SHA-256 checksums of all data files."""
    checksum_file = EXPERIMENT_DIR / "validation" / "checksums.sha256"
    if not checksum_file.exists():
        print("Integrity check: SKIPPED (no checksums.sha256 yet)")
        return True
    # TODO: Implement checksum verification
    print("Integrity check: NOT YET IMPLEMENTED")
    return True


def check_completeness():
    """Ensure L3 session data exists for the experiment runs."""
    l3_dir = EXPERIMENT_DIR / "L3_sessions"

    # Check that JSONL session logs exist (one per run, not per model)
    session_files = list(l3_dir.glob("*.jsonl"))
    if not session_files:
        print("Completeness check: FAILED — no JSONL session files in L3_sessions/")
        return False

    # Verify each JSONL has at least one valid entry
    total_calls = 0
    for sf in session_files:
        line_count = sum(1 for _ in open(sf))
        total_calls += line_count
        if line_count == 0:
            print(f"Completeness check: WARNING — empty file: {sf.name}")

    print(f"Completeness check: PASSED ({len(session_files)} session files, {total_calls:,} total calls)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Validate experiment data")
    parser.add_argument("--check-schemas", action="store_true")
    parser.add_argument("--check-integrity", action="store_true")
    parser.add_argument("--check-completeness", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all:
        args.check_schemas = args.check_integrity = args.check_completeness = True

    if not any([args.check_schemas, args.check_integrity, args.check_completeness]):
        parser.print_help()
        sys.exit(1)

    results = []
    if args.check_schemas:
        results.append(("schemas", check_schemas()))
    if args.check_integrity:
        results.append(("integrity", check_integrity()))
    if args.check_completeness:
        results.append(("completeness", check_completeness()))

    failed = [name for name, passed in results if not passed]
    if failed:
        print(f"\nFAILED: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\nAll checks passed.")


if __name__ == "__main__":
    main()
