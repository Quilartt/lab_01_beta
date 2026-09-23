import pytest

from toolkit.calculator import calculate


@pytest.mark.parametrize(("expr", "expected"), [
    ("2+3*4", 14.0),
    ("10/4", 2.5),
    ("-2 * -3", 6.0),
    ("1+-2", -1.0),
    ("10-3-2", 5.0),
    (" 2 + 3 ", 5.0),
])
def test_calculate_positive(expr, expected):
    assert calculate(expr) == expected


@pytest.mark.parametrize("expr", ["", "2+a", "2*/3", "1/0", "2+", "+"])
def test_calculate_negative(expr):
    with pytest.raises(ValueError):
        calculate(expr)