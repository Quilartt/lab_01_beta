import subprocess
import sys

import pytest

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import *

@pytest.mark.parametrize(("expr", "expected"), [
    ("2+3*4", 14.0),
    ("10/4", 2.5),
    ("-2 * -3", 6.0),
    ("1+-2", -1.0),
    ("10-3-2", 5.0),
    ("2.5*4", 10.0),
    (" 2 + 3 ", 5.0),
])
def test_calc_positive(expr, expected):
    assert calculate(expr) == expected


def test_calc_empty():
    with pytest.raises(EmptyExpression):
        calculate("")


def test_calc_unknown_symbol():
    with pytest.raises(UnknownSymbol):
        calculate("2+a")


def test_calc_two_operators():
    with pytest.raises(TwoOperators):
        calculate("2*/3")


def test_calc_division_by_zero():
    with pytest.raises(DivisionByZero):
        calculate("1/0")


def test_convert_length():
    assert convert("1000", "mm", "m") == pytest.approx(1.0)


def test_convert_mass():
    assert convert("1.5", "kg", "g") == pytest.approx(1500.0)


def test_convert_temp():
    assert convert("0", "c", "f") == pytest.approx(32.0)


def test_convert_absolute_zero():
    with pytest.raises(AbsoluteZeroException):
        convert("-300", "c", "k")


def test_convert_incompatible():
    with pytest.raises(IncompatibleUnits):
        convert("1", "kg", "m")


def test_convert_unknown_unit():
    with pytest.raises(UnknownUnit):
        convert("1", "foo", "m")


def test_convert_bad_value():
    with pytest.raises(InvalidValue):
        convert("abc", "m", "km")


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
    )


def test_cli_help():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "calc" in result.stdout


def test_cli_calc_success():
    result = run_cli("calc", "2+3*4")
    assert result.returncode == 0
    assert result.stdout.strip() == "14.0"


def test_cli_error_code():
    result = run_cli("calc", "1/0")
    assert result.returncode == 2
    assert result.stderr != ""