"""nest: eight licensing mistakes in one small open-source project.

list          every case, and which ones are fixed
run N         show case N's mistake, the way a scanner sees it
check N       check your fix
hint N        a nudge from Maggie
scan PATH     scan any project on disk: LICENSE, README and manifests
compat [A B]  can code under license A go into a project under license B?
"""

import argparse
import json
import sys
from pathlib import Path

from nest.checks import CHECKS
from nest.runs import RUNS
from nest.scan import scan

LAB = Path(__file__).resolve().parent.parent

CASES = {
    1: ("case01_no_license", "The repo nobody could use"),
    2: ("case02_disagree", "Three answers to one question"),
    3: ("case03_template", "The name that went missing"),
    4: ("case04_apache_copy", "The file that forgot where it came from"),
    5: ("case05_assets", "The font with no papers"),
    6: ("case06_logo", "The partner nobody signed up"),
    7: ("case07_deps", "The copyleft two levels down"),
    8: ("case08_agpl", "The fork that hid its source"),
}

HINTS = {
    1: [
        "Run `nest scan` on the case. What is missing, and what does that mean for users?",
        "Robin wants MIT. Where does the exact text come from? Not from memory.",
        "Add LICENSE with the MIT text and a 'Copyright (c) 2026 Robin Vale' line, then declare "
        'license = "MIT" in pyproject.toml.',
    ],
    2: [
        "Three places name a license. Which one is the legal text, and which two describe it?",
        "Robin chose Apache-2.0. Is 'MIT License' a valid SPDX identifier? Is 'ISC'?",
        "Make pyproject.toml and web/package.json say Apache-2.0, and rewrite the README's "
        "License section to name Apache 2.0 and link to LICENSE.",
    ],
    3: [
        "Open upstream/kestrel-template/LICENSE. Whose name is on it?",
        "MIT's one condition: the copyright notice and permission notice go with every copy.",
        "Keep Robin's line and add 'Copyright (c) 2019 Kestrel Labs' back above it, in LICENSE.",
    ],
    4: [
        "Compare starling/backoff.py with upstream/gustwind/gustwind/backoff.py. What got lost?",
        "Apache-2.0 section 4 asks for four things: the license, notices kept, changes stated and "
        "the NOTICE carried over.",
        "Restore the two header lines, add a line saying what Robin changed, ship the license in "
        "LICENSES/Apache-2.0.txt, and copy Gustwind's NOTICE lines into a NOTICE file.",
    ],
    5: [
        "Fonts and icons are software too. What licenses do upstream/ say they use?",
        "The OFL travels with the font. ISC wants its copyright and permission notice in copies.",
        "Copy upstream/wren-sans/OFL.txt into assets/fonts/, and upstream/feathery/LICENSE into "
        "assets/icons/.",
    ],
    6: [
        "Read the README and the header out loud. What do they claim about Driftwood Data?",
        "A logo is a trademark. Use it to say what you work with, never to say who backs you.",
        "Say 'Works with Driftwood DB', keep the logo, and add a NOTICE: whose mark it is, why it "
        "is used, and that Starling is not endorsed by them.",
    ],
    7: [
        "Run the case. Which package is not permissive, and who asked for it?",
        "Starling needs both tables and colour. Read index.json for packages that give both.",
        "Replace prettyout==2.1.0 with tabulette==0.4.0. Its colour comes from pigment, MIT.",
    ],
    8: [
        "Compare vendor/inkpot/LICENSE with upstream/inkpot/LICENSE. Can Robin change it?",
        "AGPL-3.0 section 13: network users of a modified version must be offered its source.",
        "Copy the AGPL text back, set source_url to your fork's public repo (not upstream), and "
        'add <a href="{{ source_url }}">Source code</a> to the footer.',
    ],
}


def say(text: str) -> None:
    print("     __")
    print(f"   <(o )___   {text}")
    print("    ( ._> /")
    print("     `---'", flush=True)


def case_root(number: int) -> Path:
    return LAB / "cases" / CASES[number][0]


def fixed(number: int) -> bool:
    return all(ok for _, ok in CHECKS[number](case_root(number)))


def cmd_list(args: argparse.Namespace) -> None:
    for number, (_, title) in CASES.items():
        print(f"  {number}  {title:<42} {'fixed' if fixed(number) else ''}".rstrip(), flush=True)


def cmd_run(args: argparse.Namespace) -> None:
    say(f"Case {args.n}: {CASES[args.n][1]}.")
    print()
    RUNS[args.n](case_root(args.n))


def cmd_check(args: argparse.Namespace) -> None:
    results = CHECKS[args.n](case_root(args.n))
    for label, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    print()
    if all(ok for _, ok in results):
        say(f"Case {args.n} fixed. Every shiny thing has its papers.")
    else:
        say(f"Not yet. Try: uv run python -m nest hint {args.n}")
        sys.exit(1)


def cmd_hint(args: argparse.Namespace) -> None:
    say("Here is where I would look:")
    for hint in HINTS[args.n]:
        print(f"  - {hint}")


def cmd_scan(args: argparse.Namespace) -> None:
    scan(args.path)


def cmd_compat(args: argparse.Namespace) -> None:
    data = json.loads((Path(__file__).parent / "compat.json").read_text(encoding="utf-8"))
    licenses = data["licenses"]
    if args.found and args.into:
        found = data["same_as"].get(args.found, args.found)
        verdict, why = data["verdicts"][found][args.into]
        words = {"yes": "yes", "cond": "yes, with conditions", "no": "no"}
        article = "an" if args.into[0] in "AM" else "a"
        print(f"{args.found} code into {article} {args.into} project: {words[verdict]}\n  {why}")
        return
    print((f"{'found ↓  into →':<16}" + "".join(f"{name:<14}" for name in licenses)).rstrip())
    marks = {"yes": "yes", "cond": "conditions", "no": "no"}
    for found in data["verdicts"]:
        row = "".join(f"{marks[data['verdicts'][found][into][0]]:<14}" for into in licenses)
        print(f"{found:<16}{row}".rstrip())


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # the same output on every terminal
    parser = argparse.ArgumentParser(prog="nest", description="Eight licensing mistakes.")
    sub = parser.add_subparsers(required=True)
    sub.add_parser("list", help="every case and which are fixed").set_defaults(func=cmd_list)
    for name, func, text in [
        ("run", cmd_run, "show case N's mistake"),
        ("check", cmd_check, "check your fix"),
        ("hint", cmd_hint, "a nudge from Maggie"),
    ]:
        p = sub.add_parser(name, help=text)
        p.add_argument("n", type=int, choices=CASES, metavar="N")
        p.set_defaults(func=func)
    p = sub.add_parser("scan", help="scan any project on disk")
    p.add_argument("path")
    p.set_defaults(func=cmd_scan)
    data = json.loads((Path(__file__).parent / "compat.json").read_text(encoding="utf-8"))
    p = sub.add_parser("compat", help="license compatibility")
    p.add_argument("found", nargs="?", choices=data["found"])
    p.add_argument("into", nargs="?", choices=data["licenses"])
    p.set_defaults(func=cmd_compat)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
