import os
from io import StringIO
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import settings
from rich.console import Console
from typer.testing import CliRunner

from spiel import Deck, Options
from spiel.constants import DECK
from spiel.slide import Slide
from spiel.state import State

settings.register_profile("default", deadline=None)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def three_slide_deck() -> Deck:
    deck = Deck(name="three-slides")
    deck.add_slides(Slide(), Slide(), Slide())
    return deck


@pytest.fixture
def output() -> StringIO:
    return StringIO()


@pytest.fixture
def console(output: StringIO) -> Console:
    return Console(
        file=output,
        force_terminal=True,
        width=80,
    )


@pytest.fixture
def three_slide_options() -> Options:
    return Options()


@pytest.fixture
def three_slide_state(
    console: Console, three_slide_deck: Deck, three_slide_options: Options
) -> State:
    return State(console=console, deck=three_slide_deck, options=three_slide_options)


@pytest.fixture
def empty_deck_source() -> str:
    return dedent(
        f"""\
        from spiel import Deck

        {DECK} = Deck(name="deck")
        """
    )


@pytest.fixture
def empty_file(tmp_path: Path) -> Path:
    file = tmp_path / "test_deck.py"

    file.touch()

    return file


@pytest.fixture
def file_with_empty_deck(empty_file: Path, empty_deck_source: str) -> Path:
    empty_file.write_text(empty_deck_source)

    return empty_file
