"""Resolve a requirements file against a small package index, the way a license scanner does.

The index (index.json, next to the requirements) lists each package version with its license,
what it needs and what it gives the app. Every requirement is pinned, so the result is exact.
"""

import json
from dataclasses import dataclass
from pathlib import Path

# Licenses an MIT project can ship without changing its own license.
PERMISSIVE = {"MIT", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Apache-2.0"}


@dataclass(frozen=True)
class Package:
    name: str
    version: str
    license: str | None
    via: str | None  # the package that pulled it in, or None for a direct requirement
    provides: tuple[str, ...]


def pins(text: str) -> list[tuple[str, str]]:
    found = []
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if line:
            name, _, version = line.partition("==")
            found.append((name.strip(), version.strip()))
    return found


def resolve(root: Path) -> tuple[list[Package], list[str]]:
    """Every package the app ships, direct and transitive, and any requirement that is broken."""
    index = json.loads((root / "index.json").read_text(encoding="utf-8"))
    requirements = (root / "requirements.txt").read_text(encoding="utf-8")
    shipped: list[Package] = []
    broken: list[str] = []
    queue = [(name, version, None) for name, version in pins(requirements)]
    while queue:
        name, version, via = queue.pop(0)
        if any(p.name == name for p in shipped):
            continue
        entry = index.get(name, {}).get(version) if version else None
        if entry is None:
            broken.append(f"{name}=={version}" if version else f"{name} (not pinned)")
            continue
        shipped.append(Package(name, version, entry["license"], via, tuple(entry["provides"])))
        # Depth first, so each package is listed right under the one that pulled it in.
        queue[0:0] = [(*dep.split("=="), name) for dep in entry["requires"]]
    return shipped, broken


def label(package: Package) -> str:
    return package.license or "UNKNOWN"
