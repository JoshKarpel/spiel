from io import StringIO
from pathlib import Path
from textwrap import dedent
from time import sleep

import pytest
from rich.console import Console

from spiel import Deck
from spiel.constants import DECK
from spiel.exceptions import NoDeckFound
from spiel.load import DeckReloader, DeckWatcher, load_deck
from spiel.state import State


def test_loading_from_empty_file_fails(empty_file: Path) -> None:
    with pytest.raises(NoDeckFound, match=DECK):
        load_deck(empty_file)


def test_loading_from_missing_file_fails(tmp_path: Path) -> None:
    missing_file = tmp_path / "no-such-path"

    with pytest.raises(FileNotFoundError, match="no-such-path"):
        load_deck(missing_file)


def test_can_load_deck_from_valid_file(file_with_empty_deck: Path) -> None:
    assert isinstance(load_deck(file_with_empty_deck), Deck)


def test_reloader_triggers_when_file_modified(
    file_with_empty_deck: Path,
    console: Console,
    output: StringIO,
) -> None:
    state = State(console=Console(), deck=load_deck(file_with_empty_deck))
    reloader = DeckReloader(state=state, deck_path=file_with_empty_deck)

    with DeckWatcher(event_handler=reloader, path=file_with_empty_deck, poll=True):
        sleep(0.01)

        file_with_empty_deck.write_text(
            dedent(
                """\
    from spiel import Deck

    DECK = Deck(name="modified")
    """
            )
        )

        sleep(0.01)

        for attempt in range(10):
            console.print(state.message)
            result = output.getvalue()
            if state.deck.name == "modified" and "Reloaded deck" in result:
                return  # test succeeded
            sleep(0.1)

        assert (
            False
        ), f"Reloader never triggered, current file contents:\n{file_with_empty_deck.read_text()}"  # pragma: debugging


def test_reloader_captures_error_in_message(
    file_with_empty_deck: Path,
    console: Console,
    output: StringIO,
) -> None:
    state = State(console=Console(), deck=load_deck(file_with_empty_deck))
    reloader = DeckReloader(state=state, deck_path=file_with_empty_deck)

    with DeckWatcher(event_handler=reloader, path=file_with_empty_deck, poll=True):
        sleep(0.01)

        file_with_empty_deck.write_text(
            dedent(
                """\
    from spiel import Deck

    DECK = Deck(name="modified")
    foobar
    """
            )
        )

        sleep(0.01)

        for attempt in range(10):
            console.print(state.message)
            result = output.getvalue()
            if "NameError" in result and "foobar" in result:
                return  # test succeeded
            sleep(0.1)

        assert (
            False
        ), f"Reloader never triggered, current file contents:\n{file_with_empty_deck.read_text()}"  # pragma: debugging
