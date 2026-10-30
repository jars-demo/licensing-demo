"""Recognise a license from its text, the way GitHub and license scanners do.

A license file is recognised by its words, not its file name. Copyright lines and the title are
set aside first, because they differ in every project. What is left must match the canonical text
word for word: change one condition and the file is no longer that license.
"""

import re
from functools import cache
from pathlib import Path

TEXTS = Path(__file__).resolve().parent / "texts"

# The canonical texts in texts/, as published by the SPDX and choosealicense.com projects.
KNOWN = ("MIT", "ISC", "Apache-2.0", "GPL-3.0", "AGPL-3.0", "OFL-1.1")

# How people write license names, mapped to the SPDX identifier tools expect.
ALIASES = {
    "mit": "MIT",
    "mit license": "MIT",
    "isc": "ISC",
    "isc license": "ISC",
    "apache-2.0": "Apache-2.0",
    "apache 2.0": "Apache-2.0",
    "apache license 2.0": "Apache-2.0",
    "apache license, version 2.0": "Apache-2.0",
    "gpl-3.0": "GPL-3.0",
    "gpl-3.0-only": "GPL-3.0",
    "gpl-3.0-or-later": "GPL-3.0",
    "agpl-3.0": "AGPL-3.0",
    "agpl-3.0-only": "AGPL-3.0",
    "agpl-3.0-or-later": "AGPL-3.0",
    "ofl-1.1": "OFL-1.1",
}

TITLES = {
    "mit license",
    "isc license",
    "apache license",
    "gnu general public license",
    "gnu affero general public license",
    "sil open font license",
}

# A copyright line has a year or a placeholder right after the word. License sentences such as
# "copyright notice that is included" never do, so they stay part of the license's words.
COPYRIGHT = re.compile(r"^\s*(copyright\s*(\(c\)|©)?\s*[\[<\d]|\(c\)\s*\d|©\s*\d)", re.I)
PLACEHOLDER = re.compile(r"\[(year|yyyy|fullname|email|name of copyright owner)\]|<year>", re.I)


def _normalise(text: str) -> str:
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")
    return " ".join(text.lower().split())


def _body(text: str) -> str:
    """The license's own words: no copyright lines, no title, whitespace and case ignored."""
    kept = []
    for line in text.splitlines():
        bare = line.strip().lower().rstrip(".")
        if COPYRIGHT.match(line) or bare in TITLES or bare.startswith("with reserved font name"):
            continue
        kept.append(line)
    return _normalise("\n".join(kept))


@cache
def canonical(spdx: str) -> str:
    return _body((TEXTS / f"{spdx}.txt").read_text(encoding="utf-8"))


def identify(text: str) -> str | None:
    """The SPDX id of a license text, if it is one of the known licenses, unmodified."""
    body = _body(text)
    for spdx in KNOWN:
        if body == canonical(spdx):
            return spdx
    return None


def resembles(text: str) -> str | None:
    """The license a text starts like, even when someone has changed its words."""
    body = _body(text)
    for spdx in KNOWN:
        if body[:300] and canonical(spdx)[:300] == body[:300]:
            return spdx
    return None


def spdx_of(name: str) -> str | None:
    """The SPDX id for a license name, or None when the name is not a valid identifier."""
    if name in KNOWN or name in {"GPL-3.0-only", "GPL-3.0-or-later", "AGPL-3.0-or-later"}:
        return ALIASES.get(name.lower(), name)
    return None


def loose_spdx(name: str) -> str | None:
    """What a person probably meant: 'MIT License' means MIT, even though it is not valid SPDX."""
    return ALIASES.get(name.strip().lower())


def copyright_lines(text: str) -> list[str]:
    """The copyright lines that name a real holder, skipping template placeholders."""
    return [
        line.strip()
        for line in text.splitlines()
        if COPYRIGHT.match(line)
        and not PLACEHOLDER.search(line)
        and "<" not in line
        and "free software foundation" not in line.lower()
    ]


def has_placeholders(text: str) -> bool:
    return any(COPYRIGHT.match(line) and PLACEHOLDER.search(line) for line in text.splitlines()[:5])
