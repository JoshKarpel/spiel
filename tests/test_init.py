from pathlib import Path

import pytest
from typer.testing import CliRunner

from spiel import Options
from spiel.load import load_deck_and_options
from spiel.main import app


def test_init_cli_command_fails_if_file_exists(runner: CliRunner, tmp_path: Path) -> None:
    target = tmp_path / "foo_bar.py"
    target.touch()

    result = runner.invoke(app, ["init", str(target)])

    assert result.exit_code == 1


@pytest.fixture
def init_file(runner: CliRunner, tmp_path: Path) -> Path:
    target = tmp_path / "foo_bar.py"
    runner.invoke(app, ["init", str(target)])

    return target


def test_title_slide_header_injection(init_file: Path) -> None:
    assert "# Foo Bar" in init_file.read_text()


def test_can_load_init_file(init_file: Path) -> None:
    deck, options = load_deck_and_options(init_file)

    assert deck.name == "Foo Bar"
    assert options == Options()
