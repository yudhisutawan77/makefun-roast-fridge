"""One Line, One Laugh: Roast Your Fridge.

Stdlib only. Writes a single roast line (<=200 chars) to the output
path, resolved from the environment:

- $ENTRY_OUT (a file, or a directory -> entry.txt inside it)
- $MAKEFUN_OUTPUT_DIR (the kit harness directory -> entry.txt inside it)
- $ENTRY_OUT_DIR (a directory -> entry.txt inside it)
- otherwise /output/entry.txt
"""

import os
from pathlib import Path

SETUP = "My fridge light died months ago, so dinner is now a trust exercise between me and "
TWIST = "whatever's growing in the back."

MAX_CHARS = 200


def build_roast() -> str:
    """Compose the roast: a specific, recognisable detail up front,
    the twist paying off in the last few words."""
    return (SETUP + TWIST).strip()


def validate_roast(text: str) -> str:
    """The gate wants 1-200 UTF-8 chars, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over {MAX_CHARS}")
    return text


def entry_output_path() -> Path:
    """Work out where entry.txt goes, file or directory envs alike.

    ENTRY_OUT wins; a path with no .txt suffix (or one that is already
    a directory) is treated as a directory holding entry.txt. Then the
    kit harness directory, then ENTRY_OUT_DIR / OUTPUT, then the
    default /output/entry.txt.
    """
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        path = Path(entry_out)
        if path.is_dir() or path.suffix != ".txt":
            return path / "entry.txt"
        return path
    makefun_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if makefun_dir:
        return Path(makefun_dir) / "entry.txt"
    for var in ("ENTRY_OUT_DIR", "OUTPUT"):
        value = os.environ.get(var)
        if value:
            path = Path(value)
            if path.is_dir() or path.suffix != ".txt":
                return path / "entry.txt"
            return path
    return Path("/output/entry.txt")


def main() -> None:
    text = validate_roast(build_roast())
    path = entry_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
