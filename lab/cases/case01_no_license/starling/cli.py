"""Starling: a tiny command-line notebook."""

import sys
from pathlib import Path

NOTES = Path.home() / ".starling" / "notes.txt"


def main() -> None:
    NOTES.parent.mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 1:
        with NOTES.open("a", encoding="utf-8") as notes:
            notes.write(" ".join(sys.argv[1:]) + "\n")
    elif NOTES.exists():
        print(NOTES.read_text(encoding="utf-8"), end="")
