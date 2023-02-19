import subprocess
import sys

from typer.testing import CliRunner

from spiel.cli import cli
from spiel.constants import PACKAGE_NAME


def test_help(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0


def test_help_via_main() -> None:
    result = subprocess.run([sys.executable, "-m", PACKAGE_NAME, "--help"])

    print(result.stdout)
    assert result.returncode == 0
