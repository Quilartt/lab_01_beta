"""Тесты CLI: запускают пакет через subprocess."""

import subprocess
import sys

import pytest


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Запускает python -m toolkit с аргументами."""
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
    )


# ── --help ────────────────────────────────────────────

def test_help_exit_code_zero() -> None:
    result = run_cli("--help")
    assert result.returncode == 0


def test_help_mentions_commands() -> None:
    result = run_cli("--help")
    assert "calc" in result.stdout
    assert "convert" in result.stdout


# ── Успешные команды ──────────────────────────────────

def test_calc_success() -> None:
    result = run_cli("calc", "2+3*4")
    assert result.returncode == 0
    assert result.stdout.strip() == "14.0"


def test_convert_success() -> None:
    result = run_cli("convert", "1000", "--from", "mm", "--to", "m")
    assert result.returncode == 0
    assert float(result.stdout.strip()) == pytest.approx(1.0)


# ── Пользовательские ошибки: stderr + код 2 ───────────

def test_calc_error_to_stderr() -> None:
    result = run_cli("calc", "1/0")
    assert result.returncode == 2
    assert result.stderr != ""


def test_convert_error_to_stderr() -> None:
    result = run_cli("convert", "1", "--from", "kg", "--to", "m")
    assert result.returncode == 2
    assert result.stderr != ""


def test_unknown_command() -> None:
    result = run_cli("foo", "bar")
    assert result.returncode == 2
    assert result.stderr != ""