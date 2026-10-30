"""nest scan: what a project says about its license, place by place, and where the places disagree.

It reads only files on disk, so you can point it at any repository you have cloned.
"""

import re
from pathlib import Path

from nest.licenses import ALIASES, has_placeholders, loose_spdx, spdx_of
from nest.project import Project, load


def names_in(text: str) -> set[str]:
    """Every license a piece of prose names, as SPDX ids."""
    lowered = text.lower()
    found = set()
    for alias, spdx in ALIASES.items():
        if re.search(rf"(?<![\w-]){re.escape(alias)}(?![\w-])", lowered):
            found.add(spdx)
    if "apache" in lowered:
        found.add("Apache-2.0")
    return found


def problems(project: Project) -> list[str]:
    found = []
    truth = project.license_id
    if project.license_file is None:
        found.append("no LICENSE file: the code is 'all rights reserved' and nobody may reuse it")
    elif truth is None:
        if project.looks_like:
            found.append(f"LICENSE starts like {project.looks_like}, but its words were changed")
        else:
            found.append("LICENSE is not a license text this tool recognises")
    if project.license_file is not None:
        if has_placeholders(project.license_text):
            found.append("LICENSE still has template placeholders in its copyright line")
        elif not project.holders and (truth or project.looks_like) in {"MIT", "ISC"}:
            # MIT and ISC carry the copyright inside the license. Apache and the GPL keep it in
            # NOTICE files and source headers, so their LICENSE has none.
            found.append("LICENSE has no copyright line naming who owns the code")
    if project.readme_section is None:
        found.append("README has no License section")
    else:
        named = names_in(project.readme_section)
        if truth and named and named != {truth}:
            listed = ", ".join(sorted(named))
            found.append(f"README's License section names {listed}, LICENSE is {truth}")
        if "(LICENSE)" not in project.readme_section:
            found.append("README's License section does not link to LICENSE")
    for item in project.manifests:
        if item.value is None:
            found.append(f"{item.where} declares no license")
        elif spdx_of(item.value) is None:
            meant = loose_spdx(item.value)
            hint = f' (use "{meant}")' if meant else ""
            found.append(f'{item.where}: "{item.value}" is not an SPDX identifier{hint}')
        elif truth and spdx_of(item.value) != truth:
            found.append(f"{item.where} says {item.value}, LICENSE is {truth}")
    return found


def report(root: Path) -> list[str]:
    project = load(root)
    w = max([21, *(len(item.where) + 1 for item in project.manifests)])  # the label column
    lines = []
    if project.license_file is None:
        lines.append(f"{'LICENSE':<{w}} (none)")
    else:
        status = "word for word" if project.license_id else "not recognised"
        lines.append(f"{project.license_file.name:<{w}} {project.license_id or '?'} · {status}")
        for holder in project.holders or ["(no copyright line)"]:
            lines.append(f"{'':<{w}} {holder}")
    section = project.readme_section
    shown = "(no License section)" if section is None else section.splitlines()[0][:60]
    lines.append(f"{'README':<{w}} {shown}")
    for item in project.manifests:
        lines.append(f"{item.where:<{w}} {item.value if item.value is not None else '(none)'}")
    notices = ", ".join(path.name for path in project.notices) or "(none)"
    lines.append(f"{'notices':<{w}} {notices}")
    issues = problems(project)
    lines.append("")
    if issues:
        lines.extend(f"  ✗ {issue}" for issue in issues)
    else:
        lines.append("  ✓ the license file, README and manifests agree")
    return lines


def scan(path: str) -> None:
    root = Path(path).resolve()
    print(f"nest scan {root.name}/\n")
    for line in report(root):
        print(line)
