import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from spiel.constants import PACKAGE_NAME, __version__
from spiel.main import app


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


def test_demo_display(runner: CliRunner) -> None:
    result = runner.invoke(app, ["demo", "present"])

    assert result.exit_code == 0


def test_demo_source(runner: CliRunner) -> None:
    result = runner.invoke(app, ["demo", "source"])

    assert result.exit_code == 0


def test_demo_copy_to_new_path(runner: CliRunner, tmp_path: Path) -> None:
    target = tmp_path / "new"

    result = runner.invoke(app, ["demo", "copy", str(target)])
    print(result.stdout)

    assert result.exit_code == 0


def test_demo_copy_to_existing_file(runner: CliRunner, tmp_path: Path) -> None:
    target = tmp_path / "new"
    target.touch()

    result = runner.invoke(app, ["demo", "copy", str(target)])

    assert result.exit_code == 2


def test_demo_copy_to_existing_dir(runner: CliRunner, tmp_path: Path) -> None:
    target = tmp_path / "new"
    target.mkdir(parents=True)

    result = runner.invoke(app, ["demo", "copy", str(target)])

    assert result.exit_code == 2
