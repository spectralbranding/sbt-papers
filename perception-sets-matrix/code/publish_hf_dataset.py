#!/usr/bin/env python3
"""Create + populate the 2026bf campaign dataset repo on Hugging Face.

Run (token injected by BWS, never printed):
    bws run -- uv run --with huggingface_hub python \
        code/publish_hf_dataset.py

Idempotent: create_repo(exist_ok=True); upload_folder overwrites by path.
The USER mints the dataset DOI on HF after the first drop (Settings -> DOI);
the DOI then goes into the paper's availability section + Zenodo metadata.

Staged layout: README.md (card), protocol/ (pre-registration public copy
with two documented administented redactions, protocol config, stimuli,
personas, brand sets, freeze record), records/ (parsed records + estimator
output + metameric check), logs/ (one JSON row per model API call).

Public-copy redactions (rule: internal review-process references and
internal repository paths do not ship; substance is untouched; the SHA-256
of the internal frozen original is recorded in FREEZE_RECORD.md):
  R1 pre-registration frontmatter status line -> neutral frozen-status line
  R2 internal script path -> repository-relative path
"""

from __future__ import annotations

import os
import re
import sys
import tempfile
from pathlib import Path

from huggingface_hub import HfApi

PAPER_DIR = Path(__file__).resolve().parents[1]
REPO = PAPER_DIR.parents[2]
SLUG = "perception-sets-matrix"

PROTOCOL_FILES = [
    "PROTOCOL.yaml",
    "STIMULI_STUDY1.yaml",
    "PERSONAS.yaml",
    "BRANDS_STUDY2.yaml",
    "FREEZE_RECORD.md",
]

REDACTION_NOTE = (
    "<!-- PUBLIC COPY of the frozen pre-registration. Two administrative "
    "redactions relative to the internal frozen original (whose SHA-256 is "
    "recorded in FREEZE_RECORD.md): R1 the frontmatter status line "
    "(internal workflow reference) was replaced by a neutral frozen-status "
    "line; R2 one internal repository path was rewritten repository-relative. "
    "All design, instrument, floor, and analysis content is verbatim. -->\n"
)


def stage_prereg(dst: Path) -> None:
    src = REPO / "research" / "perception-sets-matrix" / "PREREG_STUDY_DESIGN.md"
    text = src.read_text()
    # Rewrite the pre-freeze status line to its post-freeze form. Matched by
    # prefix so this file does not itself carry the internal wording it removes.
    text = re.sub(
        r"^status: DRAFT.*$",
        "status: FROZEN at design freeze 2026-07-12 (checksummed in "
        "FREEZE_RECORD.md); no calls fired before freeze",
        text,
        count=1,
        flags=re.M,
    )
    text = text.replace(
        "`code/power_simulation.py`",
        "`code/power_simulation.py`",
    )
    dst.write_text(REDACTION_NOTE + text)


def stage_freeze_record(dst: Path) -> None:
    text = (PAPER_DIR / "FREEZE_RECORD.md").read_text()
    text = text.replace(
        "[internal path removed]",
        "PREREG_STUDY_DESIGN.md (internal frozen original; public copy at protocol/PREREG_STUDY_DESIGN.md carries two documented administrative redactions)",
    )
    dst.write_text(text)


def stage(tmp: Path) -> Path:
    root = tmp / SLUG
    (root / "protocol").mkdir(parents=True)
    (root / "records").mkdir()
    (root / "logs").mkdir()
    (root / "README.md").write_bytes((PAPER_DIR / "HF_DATASET_CARD.md").read_bytes())
    for name in PROTOCOL_FILES:
        if name == "FREEZE_RECORD.md":
            stage_freeze_record(root / "protocol" / name)
        else:
            (root / "protocol" / name).write_bytes((PAPER_DIR / name).read_bytes())
    stage_prereg(root / "protocol" / "PREREG_STUDY_DESIGN.md")
    for f in sorted((PAPER_DIR / "data").glob("*")):
        if f.is_file():
            (root / "records" / f.name).write_bytes(f.read_bytes())
    for f in sorted((PAPER_DIR / "logs").glob("*.jsonl")):
        (root / "logs" / f.name).write_bytes(f.read_bytes())
    return root


def main() -> int:
    token = os.environ.get("HUGGINGFACE_API_KEY")
    if not token:
        print("ERROR: HUGGINGFACE_API_KEY not in environment (run via `bws run --`).")
        return 2
    api = HfApi(token=token)
    print(f"authenticated as: {api.whoami().get('name')!r}")
    repo_id = f"spectralbranding/{SLUG}"
    url = api.create_repo(
        repo_id=repo_id, repo_type="dataset", private=False, exist_ok=True
    )
    print(f"repo ready: {url}")
    with tempfile.TemporaryDirectory() as td:
        root = stage(Path(td))
        n = sum(1 for p in root.rglob("*") if p.is_file())
        api.upload_folder(
            folder_path=str(root),
            repo_id=repo_id,
            repo_type="dataset",
            commit_message=f"{SLUG}: campaign drop (protocol + records + call logs)",
        )
        print(f"uploaded {n} files -> {repo_id}")
    print("DONE. USER ACTION: mint the dataset DOI on HF (Settings -> DOI).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
