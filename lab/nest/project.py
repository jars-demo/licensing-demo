"""Read everything a project says about its licence: the file, the README and the manifests."""

import json
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from nest.licenses import copyright_lines, identify, resembles

LICENSE_NAMES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING")
NOTICE_NAMES = ("NOTICE", "NOTICE.md", "THIRD_PARTY_NOTICES.md", "docs/third-party-notices.md")
# Not part of the project's own declarations: dependencies, build output, and test fixtures, which
# are small projects of their own. Hidden folders (.git, .next, .venv) are skipped too.
SKIP = {"node_modules", "venv", "out", "dist", "build", "upstream", "fixtures", "testdata", "cases"}
SKIP |= {"solutions", "__pycache__"}


@dataclass
class Declared:
    where: str
    value: str | None


@dataclass
class Project:
    root: Path
    license_file: Path | None = None
    license_text: str = ""
    license_id: str | None = None
    looks_like: str | None = None
    holders: list[str] = field(default_factory=list)
    readme_section: str | None = None
    manifests: list[Declared] = field(default_factory=list)
    notices: list[Path] = field(default_factory=list)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def readme_licence_section(readme: str) -> str | None:
    """The text under a '## License' (or Licence) heading, up to the next heading."""
    match = re.search(r"^#+\s*licen[cs]e\s*$(.*?)(?=^#|\Z)", readme, re.I | re.M | re.S)
    return match.group(1).strip() if match else None


def nested(root: Path, path: Path) -> bool:
    """Is this file inside a sub-project with its own licence file? Then that licence covers it."""
    folder = path.parent
    while folder != root:
        if any((folder / name).is_file() for name in LICENSE_NAMES):
            return True
        folder = folder.parent
    return False


def manifests(root: Path) -> list[Declared]:
    found = []
    for path in sorted(root.rglob("*")):
        parts = path.relative_to(root).parts
        if SKIP & set(parts) or any(part.startswith(".") for part in parts) or not path.is_file():
            continue
        if nested(root, path):
            continue
        where = path.relative_to(root).as_posix()
        if path.name == "pyproject.toml":
            project = tomllib.loads(read_text(path)).get("project", {})
            value = project.get("license")
            if isinstance(value, dict):  # the old table form: license = {text = "MIT"}
                value = value.get("text") or value.get("file")
            found.append(Declared(where, value))
        elif path.name == "package.json":
            found.append(Declared(where, json.loads(read_text(path)).get("license")))
    return found


def load(root: Path) -> Project:
    project = Project(root=root)
    for name in LICENSE_NAMES:
        if (root / name).is_file():
            project.license_file = root / name
            project.license_text = read_text(root / name)
            project.license_id = identify(project.license_text)
            project.looks_like = resembles(project.license_text)
            project.holders = copyright_lines(project.license_text)
            break
    project.readme_section = readme_licence_section(read_text(root / "README.md"))
    project.manifests = manifests(root)
    project.notices = [root / name for name in NOTICE_NAMES if (root / name).is_file()]
    return project


def notices_text(root: Path) -> str:
    """Every notice file in the project, joined, for checks that do not mind which file is used."""
    return "\n".join(read_text(root / name) for name in NOTICE_NAMES)
