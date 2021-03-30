import subprocess
import sys

from spiel.constants import PACKAGE_NAME, __version__
from tests.conftest import CLI


def test_help(cli: CLI) -> None:
    result = cli(["--help"])
    assert result.exit_code == 0


def test_help_via_main() -> None:
    result = subprocess.run([sys.executable, "-m", PACKAGE_NAME, "--help"])
    assert result.returncode == 0


def test_version(cli: CLI) -> None:
    result = cli(["version"])
    assert result.exit_code == 0
    assert PACKAGE_NAME in result.stdout
    assert __version__ in result.stdout
