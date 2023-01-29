from pathlib import Path

import pytest
from typer.testing import CliRunner

from spiel.cli import cli
from spiel.constants import DEMO_FILE


def test_present_on_missing_file(runner: CliRunner, tmp_path: Path) -> None:
    result = runner.invoke(cli, ["present", str(tmp_path / "missing.py")])

    assert result.exit_code == 2


@pytest.mark.parametrize("stdin", [""])
def test_display_demo(runner: CliRunner, stdin: str) -> None:
    result = runner.invoke(cli, ["present", str(DEMO_FILE)], input=stdin)

    assert result.exit_code == 0
