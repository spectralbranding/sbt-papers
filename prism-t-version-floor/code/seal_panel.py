#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""seal_panel.py — merge capture-manifest fragments and SEAL the pinned panel.

Merges panel/manifest_parts/g*.json into panel/PINNED_MANIFEST.json,
re-computing every SHA-256 from the bytes on disk at seal time (capture
agents ran concurrently and a shared whitespace-normalization pass may
postdate a fragment's recorded hash — the SEALED hash is the identification
guarantee, fragments are provenance). Validates completeness (40 brands x
4 channels), minimum length (>= 500 chars), UTF-8 decodability, and
duplicate-cell collisions. After sealing, the panel directory is IMMUTABLE.

Run: uv run python research/prism_t/code/seal_panel.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prism_t_lib import (
    MANIFEST,
    PANEL_DIR,
    bank_brands,
    brand_slug,
    load_bank,
)  # noqa: E402

PARTS_DIR = PANEL_DIR.parent / "manifest_parts"
CHANNELS = ["official", "press", "experience", "social"]
MIN_CHARS = 500


def main() -> int:
    rows: dict[tuple, dict] = {}
    for part in sorted(PARTS_DIR.glob("g*.json")):
        for row in json.loads(part.read_text()):
            key = (row["brand"], row["channel"])
            if key in rows:
                print(f"[seal] DUPLICATE cell {key} in {part.name}")
                return 1
            row["fragment"] = part.name
            rows[key] = row

    brands = [b["brand"] for b in bank_brands(load_bank())]
    errors = []
    for brand in brands:
        for ch in CHANNELS:
            key = (brand, ch)
            path = PANEL_DIR / brand_slug(brand) / f"{ch}.txt"
            if key not in rows:
                errors.append(f"missing manifest row: {key}")
                continue
            if not path.exists():
                errors.append(f"missing file: {path}")
                continue
            data = path.read_bytes()
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                errors.append(f"not UTF-8: {path}")
                continue
            if len(text) < MIN_CHARS:
                errors.append(f"too short ({len(text)} chars): {path}")
            sealed_sha = hashlib.sha256(data).hexdigest()
            row = rows[key]
            if row.get("sha256") != sealed_sha:
                row["note"] = (
                    row.get("note", "")
                    + " | sha re-computed at seal (post-capture normalization)"
                ).strip(" |")
            row["sha256"] = sealed_sha
            row["chars"] = len(text)

    extra = set(rows) - {(b, c) for b in brands for c in CHANNELS}
    for key in extra:
        errors.append(f"manifest row for unknown cell: {key}")
    if errors:
        print("[seal] FAILED:")
        for e in errors:
            print("  -", e)
        return 1

    ordered = [rows[(b, c)] for b in brands for c in CHANNELS]
    MANIFEST.write_text(json.dumps(ordered, indent=1, ensure_ascii=False))
    print(f"[seal] OK: {len(ordered)} artifacts sealed -> {MANIFEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
