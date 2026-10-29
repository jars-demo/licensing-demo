"""run N: show what is wrong with each case, the way a reviewer or a scanner would see it."""

import tomllib
from pathlib import Path

from nest.checks import claims, header, ships_licence
from nest.deps import PERMISSIVE, label, resolve
from nest.licenses import copyright_lines, identify
from nest.project import notices_text, read_text
from nest.scan import report


def licence_of(path: Path) -> str:
    text = read_text(path)
    holders = copyright_lines(text)
    return f"{identify(text) or '?'} · {holders[0] if holders else '(no copyright line)'}"


def run_scan(root: Path) -> None:
    print(f"nest scan {root.name}/\n")
    print("\n".join(report(root)))


def run_03(root: Path) -> None:
    run_scan(root)
    upstream = copyright_lines(read_text(root / "upstream/kestrel-template/LICENSE"))[0]
    found = ships_licence(root, "MIT", "2019 Kestrel Labs")
    print()
    print(f"{'starling/cli_base.py':<30}from kestrel-template")
    print(f"{'kestrel-template is':<30}MIT · {upstream}")
    print(f"{'that notice, in Starling':<30}{'shipped' if found else 'nowhere'}")


def run_04(root: Path) -> None:
    theirs = header(root / "upstream/gustwind/gustwind/backoff.py")
    ours = header(root / "starling/backoff.py")
    print(f"{'upstream backoff.py':<26}{theirs[0]}")
    print(f"{'':<26}{theirs[1]}")
    print(f"{'starling/backoff.py':<26}{ours[0] if ours else '(no header)'}")
    print(f"{'what changed':<26}jitter added, not recorded")
    has_text = any(
        identify(read_text(p)) == "Apache-2.0"
        for p in root.rglob("*")
        if p.is_file() and "upstream" not in p.parts
    )
    print(f"{'Apache 2.0 text':<26}{'shipped' if has_text else 'not shipped'}")
    lines = "carried over" if "Gale Systems" in notices_text(root) else "none"
    print(f"{'Gustwind NOTICE lines':<26}{lines}")


def run_05(root: Path) -> None:
    font = ships_licence(root, "OFL-1.1", "The Wren Sans Project Authors", "assets/fonts")
    icons = ships_licence(root, "ISC", "Feathery Contributors")
    rows = [
        ("assets/fonts/WrenSans-Regular.woff2", "OFL-1.1", font),
        ("assets/icons/ (3 icons, Feathery)", "ISC", icons),
    ]
    print(f"{'file':<38}{'licence':<10}licence shipped")
    for name, spdx, ok in rows:
        print(f"{name:<38}{spdx:<10}{'yes' if ok else 'no'}")
    print()
    print(f"Starling's LICENSE: {licence_of(root / 'LICENSE')}")


def run_06(root: Path) -> None:
    found = claims(root)
    for claim in found:
        print(f"claim:   {claim}")
    notice = "yes" if "trademark" in notices_text(root) else "none"
    print(f"logo:    assets/logos/driftwood.svg, the mark of Driftwood Data\nnotice:  {notice}")


def run_07(root: Path) -> None:
    shipped, broken = resolve(root)
    for package in shipped:
        indent = "  " if package.via else ""
        name = f"{indent}{package.name} {package.version}"
        flag = "" if label(package) in PERMISSIVE else "   ✗ not permissive"
        print(f"{name:<22}{label(package):<16}{', '.join(package.provides)}{flag}")
    for item in broken:
        print(f"{item:<22}not in the index")
    bad = [p for p in shipped if label(p) not in PERMISSIVE]
    print()
    print(f"Starling is MIT. Packages it ships that are not permissive: {len(bad)}")
    for p in bad:
        via = f", pulled in by {p.via}" if p.via else ""
        print(f"  {p.name} {p.version}: {label(p)}{via}")


def run_08(root: Path) -> None:
    site = tomllib.loads(read_text(root / "deploy/site.toml"))
    footer = read_text(root / "templates/footer.html")
    print(f"{'vendor/inkpot/LICENSE':<26}{licence_of(root / 'vendor/inkpot/LICENSE')}")
    print(f"{'upstream/inkpot/LICENSE':<26}{identify(read_text(root / 'upstream/inkpot/LICENSE'))}")
    print(f"{'vendor/inkpot/CHANGES.md':<26}modified by Robin Vale")
    print(f'{"deploy/site.toml":<26}source_url = "{site.get("source_url", "")}"')
    linked = "links to the source" if "source_url" in footer else "no link to the source"
    print(f"{'templates/footer.html':<26}{linked}")


RUNS = {1: run_scan, 2: run_scan, 3: run_03, 4: run_04, 5: run_05, 6: run_06, 7: run_07, 8: run_08}
