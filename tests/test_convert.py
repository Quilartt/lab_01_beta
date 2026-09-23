"""Тесты ядра конвертера."""

import pytest

from toolkit.converter import convert
from toolkit.errors import (
    AbsoluteZeroException,
    IncompatibleUnits,
    InvalidValue,
    UnknownUnit,
)


# ── Длина ─────────────────────────────────────────────

def test_mm_to_m() -> None:
    assert convert("1000", "mm", "m") == pytest.approx(1.0)


def test_km_to_m() -> None:
    assert convert("1", "km", "m") == pytest.approx(1000.0)


# ── Масса ─────────────────────────────────────────────

def test_kg_to_g() -> None:
    assert convert("1.5", "kg", "g") == pytest.approx(1500.0)


# ── Температура ───────────────────────────────────────

def test_c_to_f() -> None:
    assert convert("0", "c", "f") == pytest.approx(32.0)


def test_c_to_k() -> None:
    assert convert("-273.15", "c", "k") == pytest.approx(0.0)


def test_f_to_c() -> None:
    assert convert("32", "f", "c") == pytest.approx(0.0)


def test_k_to_c() -> None:
    assert convert("0", "k", "c") == pytest.approx(-273.15)


# ── Регистр ───────────────────────────────────────────

def test_uppercase_units() -> None:
    assert convert("1000", "MM", "M") == pytest.approx(1.0)


def test_mixed_case_units() -> None:
    assert convert("1", "Kg", "G") == pytest.approx(1000.0)


# ── Негативные ────────────────────────────────────────

def test_below_absolute_zero() -> None:
    with pytest.raises(AbsoluteZeroException):
        convert("-300", "c", "k")


def test_incompatible_units() -> None:
    with pytest.raises(IncompatibleUnits):
        convert("1", "kg", "m")


def test_unknown_from_unit() -> None:
    with pytest.raises(UnknownUnit):
        convert("1", "foo", "m")


def test_unknown_to_unit() -> None:
    with pytest.raises(UnknownUnit):
        convert("1", "m", "foo")


def test_invalid_value() -> None:
    with pytest.raises(InvalidValue):
        convert("abc", "m", "km")


def test_incompatible_temp_and_length() -> None:
    with pytest.raises(IncompatibleUnits):
        convert("1", "c", "m")