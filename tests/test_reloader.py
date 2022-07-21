from io import StringIO
from pathlib import Path
from textwrap import dedent
from time import sleep

from rich.console import Console

from spiel.constants import DECK
from spiel.load import DeckWatcher
from spiel.reloader import DeckReloader
from spiel.state import State


def test_reloader_triggers_when_file_modified(
    file_with_empty_deck: Path,
    console: Console,
    output: StringIO,
) -> None:
    state = State.from_file(file_with_empty_deck)
    reloader = DeckReloader(state=state, deck_path=file_with_empty_deck)

    with DeckWatcher(event_handler=reloader, path=file_with_empty_deck, poll=True):
        sleep(0.01)

        file_with_empty_deck.write_text(
            dedent(
                f"""\
                from spiel import Deck

                {DECK} = Deck(name="modified")
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
    state = State.from_file(file_with_empty_deck)
    reloader = DeckReloader(state=state, deck_path=file_with_empty_deck)

    with DeckWatcher(event_handler=reloader, path=file_with_empty_deck, poll=True):
        sleep(0.01)

        file_with_empty_deck.write_text(
            dedent(
                f"""\
    from spiel import Deck

    {DECK} = Deck(name="modified")
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
