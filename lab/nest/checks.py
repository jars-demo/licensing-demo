"""The checks: check_NN(root) -> [(label, ok)].

Each check tests the promise, not the shape of one fix. It reads the project as a scanner or a
lawyer would: the license words on disk, the notices that ship, the packages that get installed.
"""

import json
import re
import tomllib
from pathlib import Path

from nest.deps import PERMISSIVE, label, resolve
from nest.licenses import _body, canonical, copyright_lines, has_placeholders, identify
from nest.project import load, notices_text, read_text
from nest.scan import names_in

YEAR = re.compile(r"\b(19|20)\d\d\b")
CLAIM = re.compile(r"\b(official|endorsed|endorse|certified|partner|approved|sponsored)\b", re.I)
NEGATION = re.compile(r"\b(not|never|no|nor|neither|independent|unofficial)\b|n't\b", re.I)


def files(root: Path, within: str = ""):
    """Every text file in the project, except upstream/, which stands in for other repos."""
    for path in sorted((root / within).rglob("*")):
        rel = path.relative_to(root)
        if path.is_file() and rel.parts[0] != "upstream" and path.stat().st_size < 200_000:
            yield path, read_text(path)


def ships_license(root: Path, spdx: str, holder: str, within: str = "") -> bool:
    """Is this holder's copyright shipped together with the full license text?

    Either a license file of that kind names the holder, or a notices file holds both the
    holder's copyright line and the license's full words.
    """
    for _, text in files(root, within):
        if identify(text) == spdx and any(holder in line for line in copyright_lines(text)):
            return True
    if within:
        return False
    notices = notices_text(root)
    return holder in notices and canonical(spdx) in _body(notices)


def manifest_license(path: Path) -> str | None:
    if path.name == "pyproject.toml":
        value = tomllib.loads(read_text(path) or "").get("project", {}).get("license")
    else:
        value = json.loads(read_text(path) or "{}").get("license")
    return value if isinstance(value, str) else None


def still_robins_mit(root: Path) -> bool:
    project = load(root)
    return project.license_id == "MIT" and any("Robin Vale" in h for h in project.holders)


def check_01(root: Path) -> list[tuple[str, bool]]:
    project = load(root)
    named = any("Robin Vale" in h and YEAR.search(h) for h in project.holders)
    return [
        ("a LICENSE file at the root of the project", project.license_file is not None),
        ("LICENSE is the MIT license, word for word", project.license_id == "MIT"),
        (
            "its copyright line names Robin Vale and a year",
            named and not has_placeholders(project.license_text),
        ),
        (
            'pyproject.toml declares license = "MIT"',
            manifest_license(root / "pyproject.toml") == "MIT",
        ),
    ]


def check_02(root: Path) -> list[tuple[str, bool]]:
    project = load(root)
    section = project.readme_section or ""
    return [
        (
            "LICENSE is still Apache-2.0, the license Robin chose",
            project.license_id == "Apache-2.0",
        ),
        (
            "pyproject.toml declares the SPDX id Apache-2.0",
            manifest_license(root / "pyproject.toml") == "Apache-2.0",
        ),
        (
            "web/package.json declares Apache-2.0",
            manifest_license(root / "web" / "package.json") == "Apache-2.0",
        ),
        (
            "the README's License section names Apache 2.0, and only that",
            names_in(section) == {"Apache-2.0"},
        ),
        ("the README's License section links to LICENSE", "(LICENSE)" in section),
    ]


def check_03(root: Path) -> list[tuple[str, bool]]:
    project = load(root)
    return [
        ("LICENSE is still the MIT license, word for word", project.license_id == "MIT"),
        (
            "Robin Vale's copyright line is still there",
            any("Robin Vale" in h for h in project.holders),
        ),
        (
            "kestrel-template's notice, Copyright (c) 2019 Kestrel Labs, ships with the code",
            ships_license(root, "MIT", "2019 Kestrel Labs"),
        ),
    ]


def header(path: Path) -> list[str]:
    """The comment lines at the top of a Python file."""
    lines = []
    for line in read_text(path).splitlines():
        if not line.startswith("#"):
            break
        lines.append(line)
    return lines


def check_04(root: Path) -> list[tuple[str, bool]]:
    top = header(root / "starling" / "backoff.py")
    notices = notices_text(root)
    changed = [line for line in top if re.search(r"\b(modified|changed|changes)\b", line, re.I)]
    return [
        ("Starling's own LICENSE is still MIT", still_robins_mit(root)),
        (
            "starling/backoff.py keeps Gustwind's copyright line",
            any("Copyright 2023 The Gustwind Authors" in line for line in top),
        ),
        (
            "starling/backoff.py says it is under Apache-2.0",
            any(re.search(r"Apache(-| License,? (Version )?)2\.0", line) for line in top),
        ),
        ("starling/backoff.py says what was changed", bool(changed)),
        (
            "the full Apache License 2.0 text ships with Starling",
            any(identify(text) == "Apache-2.0" for _, text in files(root)),
        ),
        (
            "Starling's NOTICE carries Gustwind's NOTICE lines",
            "The Gustwind Authors" in notices and "Gale Systems" in notices,
        ),
    ]


def check_05(root: Path) -> list[tuple[str, bool]]:
    return [
        (
            "the Wren Sans license (OFL-1.1) ships next to the font",
            any(identify(text) == "OFL-1.1" for _, text in files(root, "assets/fonts")),
        ),
        (
            "and it carries the font's copyright line",
            ships_license(root, "OFL-1.1", "The Wren Sans Project Authors", "assets/fonts"),
        ),
        (
            "the Feathery icons' ISC license and copyright ship with Starling",
            ships_license(root, "ISC", "Feathery Contributors"),
        ),
        ("Starling's own LICENSE is still MIT, and still Robin's", still_robins_mit(root)),
    ]


def claims(root: Path) -> list[str]:
    """Sentences that claim an endorsement, from the README and the page templates."""
    found = []
    targets = [root / "README.md", *sorted((root / "templates").glob("*.html"))]
    for path in targets:
        for sentence in re.split(r"[.!?\n]", re.sub(r"<[^>]+>", "\n", read_text(path))):
            if CLAIM.search(sentence) and not NEGATION.search(sentence):
                found.append(f"{path.relative_to(root).as_posix()}: {sentence.strip()}")
    return found


def check_06(root: Path) -> list[tuple[str, bool]]:
    notices = notices_text(root)
    sentences = re.split(r"[.!?]", " ".join(notices.split()))
    disclaims = any(
        NEGATION.search(s) and re.search(r"endorse|official|affiliated|sponsor", s, re.I)
        for s in sentences
    )
    return [
        (
            "README and the header make no claim to be official, endorsed or a partner",
            not claims(root),
        ),
        (
            "the header still shows Driftwood's logo, so people recognise it",
            "driftwood.svg" in read_text(root / "templates" / "header.html"),
        ),
        (
            "a NOTICE names the logo file and Driftwood Data's trademark",
            "driftwood.svg" in notices and "Driftwood Data" in notices and "trademark" in notices,
        ),
        ("the NOTICE says Starling is not official or endorsed", disclaims),
    ]


def check_07(root: Path) -> list[tuple[str, bool]]:
    shipped, broken = resolve(root)
    provides = {thing for package in shipped for thing in package.provides}
    return [
        ("every requirement is pinned and found in the index", not broken),
        (
            "nothing Starling ships is copyleft, source-available or unlicensed",
            all(label(package) in PERMISSIVE for package in shipped),
        ),
        ("Starling still gets its tables and colour", {"tables", "colour"} <= provides),
        ("Starling's LICENSE is still MIT", still_robins_mit(root)),
    ]


def check_08(root: Path) -> list[tuple[str, bool]]:
    site = tomllib.loads(read_text(root / "deploy" / "site.toml") or "")
    url = str(site.get("source_url", ""))
    footer = read_text(root / "templates" / "footer.html")
    return [
        (
            "vendor/inkpot/ is under AGPL-3.0 again, word for word",
            identify(read_text(root / "vendor" / "inkpot" / "LICENSE")) == "AGPL-3.0",
        ),
        (
            "deploy/site.toml points source_url at the source of your version",
            url.startswith("https://") and "inkpot-sync/inkpot" not in url,
        ),
        (
            "every page footer links to that source",
            bool(re.search(r'href="\{\{\s*source_url\s*\}\}"', footer)),
        ),
        ("the rest of Starling Cloud keeps its MIT license", still_robins_mit(root)),
    ]


CHECKS = {
    1: check_01,
    2: check_02,
    3: check_03,
    4: check_04,
    5: check_05,
    6: check_06,
    7: check_07,
    8: check_08,
}
