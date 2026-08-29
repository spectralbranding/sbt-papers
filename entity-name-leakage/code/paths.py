"""Resolve where the records are read from and where tables are written.

These scripts run in two places and the paths differ in both. In the authoring
checkout the frozen collections sit beside the paper; for a public reader they
arrive as a Hugging Face download, at whatever directory that reader chose. So
the collection directory is an argument, not a constant.

Resolution order for the data root: `--data-root`, then `$ENL_DATA_ROOT`, then
the authoring checkout if this is running inside one. A public reader has
neither of the last two, which is why a miss names the dataset rather than a
path they could not have.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
BUNDLE = CODE_DIR.parent

DATASET = "spectralbranding/entity-name-leakage"
COLLECTION = "second_collection"

# Where the frozen collection lives in the authoring checkout. Absent for every
# public reader, which is the normal case rather than an error.
_INTERNAL = (
    BUNDLE.parents[2] / "research" / "occasion_conditionality" / "name_effect_probe"
    if len(BUNDLE.parents) >= 3
    else None
)

_MISSING = f"""ERROR: the frozen records were not found.

They are published as a Hugging Face dataset, separately from this code:

    huggingface-cli download {DATASET} \\
        --repo-type dataset --local-dir enl-data
    uv run python code/{{script}} --data-root enl-data/{COLLECTION}

Or set $ENL_DATA_ROOT to the collection directory once and omit the flag.
Whichever you pass must be the directory holding `data/` and `PROTOCOL.yaml`."""


def out_dir() -> Path:
    """`output/tables/` beside the code, created on demand."""
    d = BUNDLE / "output" / "tables"
    d.mkdir(parents=True, exist_ok=True)
    return d


def add_data_arg(ap: argparse.ArgumentParser) -> None:
    ap.add_argument(
        "--data-root",
        default=None,
        metavar="DIR",
        help=(
            f"the frozen collection directory (holds data/ and PROTOCOL.yaml); "
            f"defaults to $ENL_DATA_ROOT, then the authoring checkout"
        ),
    )


def data_root(args: argparse.Namespace, script: str) -> Path:
    """The collection directory, or exit with instructions a reader can act on."""
    for cand in (args.data_root, os.environ.get("ENL_DATA_ROOT"), _INTERNAL):
        if cand and Path(cand).is_dir():
            return Path(cand)
    raise SystemExit(_MISSING.format(script=script))


def rel(p: Path) -> str:
    """A path as the bundle sees it, for printing.

    Never print a resolved path: it carries the authoring machine's directory
    layout into stdout, and stdout is what gets pasted into a log, an issue or a
    paper. `output/tables/guard_ratio.json` is also the more useful thing to
    read, because it is the path the published bundle actually has.
    """
    try:
        return str(Path(p).resolve().relative_to(BUNDLE))
    except ValueError:
        return str(p)
