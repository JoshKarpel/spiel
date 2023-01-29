from typer.testing import CliRunner

from spiel import __version__
from spiel.cli import cli


def test_version(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["version"])

    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_plain_version(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["version", "--plain"])

    assert result.exit_code == 0
    assert __version__ in result.stdout
