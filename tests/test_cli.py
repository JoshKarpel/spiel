import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture
from typer.testing import CliRunner

from spiel.cli import cli
from spiel.constants import DEMO_FILE, PACKAGE_NAME, __version__


def test_help(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0


def test_help_via_main() -> None:
    result = subprocess.run([sys.executable, "-m", PACKAGE_NAME, "--help"])

    print(result.stdout)
    assert result.returncode == 0


def test_version(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["version"])

    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_plain_version(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["version", "--plain"])

    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_present_deck_on_missing_file(runner: CliRunner, tmp_path: Path) -> None:
    result = runner.invoke(cli, ["present", str(tmp_path / "missing.py")])

    assert result.exit_code == 1


@pytest.mark.parametrize("stdin", [""])
def test_display_demo_deck(runner: CliRunner, stdin: str) -> None:
    result = runner.invoke(cli, ["present", str(DEMO_FILE)], input=stdin)

    assert result.exit_code == 0


def test_demo_display(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["demo", "present"])

    assert result.exit_code == 0


def test_DEMO_FILE(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["demo", "source"])

    assert result.exit_code == 0


def test_demo_copy_to_new_path(runner: CliRunner, tmp_path: Path) -> None:
    target = tmp_path / "new"

    result = runner.invoke(cli, ["demo", "copy", str(target)])

    assert result.exit_code == 0


def test_demo_copy_to_existing_file(runner: CliRunner, tmp_path: Path) -> None:
    target = tmp_path / "new"
    target.touch()

    result = runner.invoke(cli, ["demo", "copy", str(target)])

    assert result.exit_code == 1


def test_demo_copy_to_existing_dir(runner: CliRunner, tmp_path: Path) -> None:
    target = tmp_path / "new"
    target.mkdir(parents=True)

    result = runner.invoke(cli, ["demo", "copy", str(target)])

    assert result.exit_code == 1


def test_demo_copy_error_during_copytree(
    runner: CliRunner,
    tmp_path: Path,
    mocker: MockFixture,
) -> None:
    mock = mocker.patch("shutil.copytree", MagicMock(side_effect=Exception("foobar")))

    target = tmp_path / "new"

    result = runner.invoke(cli, ["demo", "copy", str(target)])

    assert mock.called
    assert "foobar" in result.stdout
    assert result.exit_code == 1
