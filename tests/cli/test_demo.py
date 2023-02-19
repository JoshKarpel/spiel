from pathlib import Path
from unittest.mock import MagicMock

from pytest_mock import MockFixture
from typer.testing import CliRunner

from spiel.cli import cli


def test_demo_display(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["demo", "present"])

    assert result.exit_code == 0


def test_demo_source(runner: CliRunner) -> None:
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
