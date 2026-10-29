"""Copy a case into a temporary folder, so tests can edit it without touching lab/cases/."""

import shutil
from pathlib import Path

import pytest

from nest.__main__ import CASES

LAB = Path(__file__).resolve().parent.parent


def copy_case(number: int, into: Path, solved: bool = False) -> Path:
    name = CASES[number][0]
    root = into / name
    shutil.copytree(LAB / "cases" / name, root)
    if solved:
        shutil.copytree(LAB / "tests" / "solutions" / name, root, dirs_exist_ok=True)
    return root


@pytest.fixture
def case(tmp_path):
    return lambda number, solved=False: copy_case(number, tmp_path, solved)
