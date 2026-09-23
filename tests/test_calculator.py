"""Тесты вычислительного ядра калькулятора."""

import pytest

from toolkit.calculator import calculate
from toolkit.errors import (
    DivisionByZero,
    EmptyExpression,
    MissingOperand,
    TwoOperators,
    UnknownSymbol,
)


# ── Позитивные (6 по ТЗ) ───────────────────────────────

@pytest.mark.parametrize(("expr", "expected"), [
    ("2+3*4", 14.0),          # приоритет
    ("10 / 4", 2.5),          # вещественное
    ("-2 * -3", 6.0),         # два унарных
    ("1+-2", -1.0),           # унарный после бинарного
    ("10-3-2", 5.0),          # левая ассоциативность
    (" 2 + 3 ", 5.0),         # пробелы игнорируются
    ("2.5*4", 10.0),          # вещественные
])
def test_calculate_positive(expr: str, expected: float) -> None:
    assert calculate(expr) == pytest.approx(expected)


# ── Негативные (4+ по ТЗ) ──────────────────────────────

def test_empty_expression() -> None:
    with pytest.raises(EmptyExpression):
        calculate("")


def test_unknown_symbol() -> None:
    with pytest.raises(UnknownSymbol):
        calculate("2+a")


def test_two_operators_in_a_row() -> None:
    with pytest.raises(TwoOperators):
        calculate("2*/3")


def test_missing_operand_at_end() -> None:
    with pytest.raises(MissingOperand):
        calculate("2+")


def test_only_operator() -> None:
    with pytest.raises(EmptyExpression):
        calculate("+")


def test_division_by_zero() -> None:
    with pytest.raises(DivisionByZero):
        calculate("1/0")


def test_double_dot() -> None:
    with pytest.raises(Exception):        # InvalidNumber или UnknownSymbol
        calculate("2..5")