from pathlib import Path

import pytest
from typer.testing import CliRunner

from spiel.app import load_deck
from spiel.cli import cli


def test_init_cli_command_fails_if_file_exists(runner: CliRunner, tmp_path: Path) -> None:
    target = tmp_path / "foo_bar.py"
    target.touch()

    result = runner.invoke(cli, ["init", str(target)])

    assert result.exit_code == 1


@pytest.fixture
def init_file(runner: CliRunner, tmp_path: Path) -> Path:
    target = tmp_path / "foo_bar.py"
    runner.invoke(cli, ["init", str(target)])

    return target


def test_title_slide_header_injection(init_file: Path) -> None:
    assert "# Foo Bar" in init_file.read_text()


def test_can_load_init_file(init_file: Path) -> None:
    deck = load_deck(init_file)

    assert deck.name == "Foo Bar"
