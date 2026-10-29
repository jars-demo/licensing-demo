"""Every case fails its check as shipped, and passes once fixed. The fixes live in solutions/."""

import pytest

from nest.__main__ import CASES
from nest.checks import CHECKS
from nest.runs import RUNS


@pytest.mark.parametrize("number", list(CASES))
def test_case_is_broken_as_shipped(number, case):
    results = CHECKS[number](case(number))

    assert not all(ok for _, ok in results)


@pytest.mark.parametrize("number", list(CASES))
def test_case_passes_with_a_real_fix(number, case):
    failed = [label for label, ok in CHECKS[number](case(number, solved=True)) if not ok]

    assert failed == []


@pytest.mark.parametrize("number", list(CASES))
def test_case_runs_and_prints_its_symptom(number, case, capsys):
    RUNS[number](case(number))

    assert len(capsys.readouterr().out.splitlines()) >= 4
