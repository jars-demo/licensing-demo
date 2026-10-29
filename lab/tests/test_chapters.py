"""Every output quoted in a chapter is real: the case's run output, and the check once fixed."""

import re
from pathlib import Path

import pytest

from nest.__main__ import CASES
from nest.checks import CHECKS
from nest.runs import RUNS

WORKSHOP = Path(__file__).resolve().parents[2] / "workshop"


def chapter(number: int) -> str:
    [path] = WORKSHOP.glob(f"{number:02d}-*.md")
    return path.read_text(encoding="utf-8")


def block_after(text: str, heading: str) -> str:
    section = text.split(f"## {heading}\n", 1)[1]
    return re.search(r"```text\n(.*?)\n```", section, re.S).group(1)


@pytest.mark.parametrize("number", list(CASES))
def test_the_case_output_is_real(number, case, capsys):
    RUNS[number](case(number))

    assert block_after(chapter(number), "The case") == capsys.readouterr().out.rstrip("\n")


@pytest.mark.parametrize("number", list(CASES))
def test_the_check_output_is_real(number, case):
    lines = [f"  PASS  {label}" for label, _ in CHECKS[number](case(number, solved=True))]

    assert block_after(chapter(number), "Check it works") == "\n".join(lines)
