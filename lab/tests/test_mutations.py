"""The checks test the promise, not the shape of one fix. Each case is edited into plausible wrong
fixes, which must fail, and into other right fixes, which must pass."""

from pathlib import Path

import pytest

from nest.checks import CHECKS

TEXTS = Path(__file__).resolve().parent.parent / "nest" / "texts"
SOLUTIONS = Path(__file__).resolve().parent / "solutions"
ROBIN = "Copyright (c) 2026 Robin Vale"
KESTREL = "Copyright (c) 2019 Kestrel Labs"


def text(name: str) -> str:
    return (TEXTS / f"{name}.txt").read_text(encoding="utf-8")


def mit(*holders: str) -> str:
    return text("MIT").replace("Copyright (c) [year] [fullname]", "\n".join(holders))


def solution(name: str, rel: str) -> str:
    return (SOLUTIONS / name / rel).read_text(encoding="utf-8")


def pyproject(license: str) -> str:
    return f'[project]\nname = "starling"\nversion = "0.4.0"\nlicense = "{license}"\n'


SOLVED_04 = {
    "LICENSES/Apache-2.0.txt": text("Apache-2.0"),
    "NOTICE": solution("case04_apache_copy", "NOTICE"),
}
CODE_04 = solution("case04_apache_copy", "starling/backoff.py").split("\n\n", 1)[1]
SOLVED_06 = {"NOTICE": solution("case06_logo", "NOTICE")}
FIXED_HEADER = solution("case06_logo", "templates/header.html")
FIXED_FOOTER = solution("case08_agpl", "templates/footer.html")
FIXED_SITE = solution("case08_agpl", "deploy/site.toml")
OFL = solution("case05_assets", "assets/fonts/OFL.txt")
ICONS = solution("case05_assets", "assets/icons/LICENSE")

WRONG = {
    "01 LICENSE that only says MIT": (1, {"LICENSE": "MIT\n", "pyproject.toml": pyproject("MIT")}),
    "01 MIT with the placeholders left in": (
        1,
        {"LICENSE": text("MIT"), "pyproject.toml": pyproject("MIT")},
    ),
    "01 MIT with an extra condition": (
        1,
        {"LICENSE": mit(ROBIN) + "\nNot for commercial use.\n", "pyproject.toml": pyproject("MIT")},
    ),
    "01 pyproject says MIT License": (
        1,
        {"LICENSE": mit(ROBIN), "pyproject.toml": pyproject("MIT License")},
    ),
    "02 make LICENSE match the README instead": (
        2,
        {
            "LICENSE": mit(ROBIN),
            "pyproject.toml": pyproject("MIT"),
            "web/package.json": '{"license": "MIT"}',
            "README.md": "# Starling\n\n## License\n\n[MIT](LICENSE)\n",
        },
    ),
    "02 Apache 2.0 is not an SPDX id": (
        2,
        {
            "pyproject.toml": pyproject("Apache 2.0"),
            "web/package.json": '{"license": "Apache-2.0"}',
            "README.md": "# Starling\n\n## License\n\n[Apache License 2.0](LICENSE)\n",
        },
    ),
    "02 README names two licenses": (
        2,
        {
            "pyproject.toml": pyproject("Apache-2.0"),
            "web/package.json": '{"license": "Apache-2.0"}',
            "README.md": "# Starling\n\n## License\n\n[Apache-2.0](LICENSE). It used to be MIT.\n",
        },
    ),
    "03 swap Robin's name for Kestrel's": (3, {"LICENSE": mit(KESTREL)}),
    "03 credit Kestrel in the README only": (
        3,
        {"README.md": f"# Starling\n\nBased on kestrel-template, {KESTREL}.\n"},
    ),
    "03 Kestrel's line in a NOTICE, without the license": (3, {"NOTICE": KESTREL + "\n"}),
    "04 header back, but no note of the change": (
        4,
        {
            **SOLVED_04,
            "starling/backoff.py": "# Copyright 2023 The Gustwind Authors\n"
            "# SPDX-License-Identifier: Apache-2.0\n\n" + CODE_04,
        },
    ),
    "04 everything but the license text": (
        4,
        {
            "NOTICE": SOLVED_04["NOTICE"],
            "starling/backoff.py": solution("case04_apache_copy", "starling/backoff.py"),
        },
    ),
    "04 relabel the copied file as MIT": (
        4,
        {
            **SOLVED_04,
            "starling/backoff.py": "# Copyright 2023 The Gustwind Authors\n"
            "# SPDX-License-Identifier: MIT\n# Changed by Robin Vale: added jitter.\n\n" + CODE_04,
        },
    ),
    "05 font license at the root, not by the font": (
        5,
        {"OFL.txt": OFL, "assets/icons/LICENSE": ICONS},
    ),
    "05 OFL with its placeholder copyright": (
        5,
        {"assets/fonts/OFL.txt": text("OFL-1.1"), "assets/icons/LICENSE": ICONS},
    ),
    "05 replace Starling's LICENSE with the OFL": (
        5,
        {"LICENSE": OFL, "assets/fonts/OFL.txt": OFL, "assets/icons/LICENSE": ICONS},
    ),
    "06 remove the logo instead": (
        6,
        {
            **SOLVED_06,
            "README.md": solution("case06_logo", "README.md"),
            "templates/header.html": "<header><span>Works with Driftwood DB</span></header>\n",
        },
    ),
    "06 add a notice, keep the partner claim": (6, SOLVED_06),
    "06 a notice with no disclaimer": (
        6,
        {
            "NOTICE": "assets/logos/driftwood.svg is a trademark of Driftwood Data.\n",
            "README.md": solution("case06_logo", "README.md"),
            "templates/header.html": FIXED_HEADER,
        },
    ),
    "07 downgrade to prettyout 1.9.0, losing colour": (
        7,
        {"requirements.txt": "prettyout==1.9.0\nclick-lite==3.0.2\n"},
    ),
    "07 richgrid, which has no license": (
        7,
        {"requirements.txt": "richgrid==5.0.0\nclick-lite==3.0.2\n"},
    ),
    "07 gridlock, which is AGPL": (7, {"requirements.txt": "gridlock==1.2.0\nclick-lite==3.0.2\n"}),
    "07 fasttable, which is source-available": (
        7,
        {"requirements.txt": "fasttable==3.1.0\nclick-lite==3.0.2\n"},
    ),
    "07 tabulette, not pinned": (7, {"requirements.txt": "tabulette\nclick-lite==3.0.2\n"}),
    "08 link to upstream inkpot, not your version": (
        8,
        {
            "vendor/inkpot/LICENSE": text("AGPL-3.0"),
            "deploy/site.toml": 'source_url = "https://github.com/inkpot-sync/inkpot"\n',
            "templates/footer.html": FIXED_FOOTER,
        },
    ),
    "08 delete the vendored license": (
        8,
        {
            "vendor/inkpot/LICENSE": None,
            "deploy/site.toml": FIXED_SITE,
            "templates/footer.html": FIXED_FOOTER,
        },
    ),
    "08 a footer link that goes nowhere": (
        8,
        {
            "vendor/inkpot/LICENSE": text("AGPL-3.0"),
            "deploy/site.toml": FIXED_SITE,
            "templates/footer.html": '<footer><a href="#">Source code</a></footer>\n',
        },
    ),
}

RIGHT = {
    "01 LICENSE.md and a copyright sign": (
        1,
        {
            "LICENSE.md": mit("Copyright © 2026 Robin Vale"),
            "pyproject.toml": pyproject("MIT"),
        },
    ),
    "03 Kestrel's notice and license in THIRD_PARTY_NOTICES.md": (
        3,
        {
            "THIRD_PARTY_NOTICES.md": "# Third-party notices\n\n## kestrel-template\n\n"
            + mit(KESTREL)
        },
    ),
    "04 the long Apache header and a NOTICE.md": (
        4,
        {
            "LICENSE-APACHE": text("Apache-2.0"),
            "NOTICE.md": SOLVED_04["NOTICE"],
            "starling/backoff.py": "# Copyright 2023 The Gustwind Authors\n"
            "# Licensed under the Apache License, Version 2.0.\n"
            "# Changes by Robin Vale, 2026: random jitter on each delay.\n\n" + CODE_04,
        },
    ),
    "05 icons credited in THIRD_PARTY_NOTICES.md": (
        5,
        {"assets/fonts/OFL.txt": OFL, "THIRD_PARTY_NOTICES.md": "## Feathery icons\n\n" + ICONS},
    ),
    "06 an independent-project line in the README": (
        6,
        {
            **SOLVED_06,
            "README.md": "# Starling for Driftwood\n\nNotes in Driftwood DB. Starling is an "
            "independent project and isn't affiliated with Driftwood Data.\n",
            "templates/header.html": FIXED_HEADER,
        },
    ),
    "08 the source on Codeberg": (
        8,
        {
            "vendor/inkpot/LICENSE": text("AGPL-3.0"),
            "deploy/site.toml": 'source_url = "https://codeberg.org/robin/starling-cloud"\n',
            "templates/footer.html": '<footer><a href="{{source_url}}">Source</a></footer>\n',
        },
    ),
}


def apply(root: Path, edits: dict[str, str | None]) -> Path:
    for rel, content in edits.items():
        path = root / rel
        if content is None:
            path.unlink()
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    return root


def passes(number: int, root: Path) -> bool:
    return all(ok for _, ok in CHECKS[number](root))


@pytest.mark.parametrize("name", list(WRONG))
def test_a_wrong_fix_fails(name, case):
    number, edits = WRONG[name]

    assert not passes(number, apply(case(number), edits))


@pytest.mark.parametrize("name", list(RIGHT))
def test_another_right_fix_passes(name, case):
    number, edits = RIGHT[name]

    assert passes(number, apply(case(number), edits))
