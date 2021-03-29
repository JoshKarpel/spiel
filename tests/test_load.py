from time import sleep
from pathlib import Path
from textwrap import dedent

import pytest

from spiel.constants import DECK
from spiel.exceptions import NoDeckFound
from spiel.load import load_deck, DeckReloader, DeckWatcher
from spiel.slides import Deck
from spiel.state import State
from pytest_mock.plugin import MockerFixture


@pytest.fixture
def empty_file(tmp_path: Path) -> Path:
    file = tmp_path / "test_deck.py"

    file.touch()

    return file


@pytest.fixture
def valid_file(empty_file: Path) -> Path:
    empty_file.write_text(
        dedent(
            """\
    from spiel import Deck
    
    DECK = Deck(name="deck")
    """
        )
    )

    return empty_file


def test_loading_from_empty_file_fails(empty_file: Path) -> None:
    with pytest.raises(NoDeckFound, match=DECK):
        load_deck(empty_file)


def test_loading_from_missing_file_fails(tmp_path: Path) -> None:
    missing_file = tmp_path / "no-such-path"

    with pytest.raises(FileNotFoundError, match="no-such-path"):
        load_deck(missing_file)


def test_can_load_deck_from_valid_file(valid_file: Path) -> None:
    assert isinstance(load_deck(valid_file), Deck)


def test_reloader_triggers_when_file_modified(valid_file: Path) -> None:
    delay = 1  # a small delay is needed after starting the watcher and before checking for the reload (they happen async)

    state = State(load_deck(valid_file))
    reloader = DeckReloader(state=state, deck_path=valid_file)

    with DeckWatcher(event_handler=reloader, path=valid_file, poll=True):
        sleep(delay)

        valid_file.write_text(
            dedent(
                """\
    from spiel import Deck
    
    DECK = Deck(name="modified")
    """
            )
        )

        sleep(delay)

        assert state.deck.name == "modified"
