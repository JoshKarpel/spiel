from io import StringIO
from pathlib import Path
from textwrap import dedent

import pytest
from rich.console import Console

from spiel import Deck
from spiel.constants import DECK
from spiel.slide import Slide
from spiel.state import State


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
def three_slide_state(console: Console, three_slide_deck: Deck) -> State:
    return State(console=console, deck=three_slide_deck)


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
