import subprocess
import sys
import traceback
from pathlib import Path

import pytest
from typer.testing import CliRunner

from spiel.constants import PACKAGE_NAME, __version__
from spiel.main import app
from spiel.modes import Mode


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_help(runner: CliRunner) -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0


def test_help_via_main() -> None:
    result = subprocess.run([sys.executable, "-m", PACKAGE_NAME, "--help"])

    assert result.returncode == 0


def test_version(runner: CliRunner) -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert PACKAGE_NAME in result.stdout
    assert __version__ in result.stdout


@pytest.mark.parametrize("deck_path", (Path(__file__).parents[1] / "examples").glob("*.py"))
@pytest.mark.parametrize("mode", list(Mode))
@pytest.mark.parametrize("stdin", ["", "s", "d"])
def test_display_example_decks(runner: CliRunner, deck_path: Path, mode: Mode, stdin: str) -> None:
    result = runner.invoke(app, ["present", str(deck_path), "--mode", mode], input=stdin)

    assert result.exit_code == 0
