from pathlib import Path
from textwrap import dedent

import pytest

from spiel import Deck, Options
from spiel.constants import DECK
from spiel.exceptions import NoDeckFound
from spiel.load import load_deck_and_options


def test_loading_from_empty_file_fails(empty_file: Path) -> None:
    with pytest.raises(NoDeckFound, match=DECK):
        load_deck_and_options(empty_file)


def test_loading_from_missing_file_fails(tmp_path: Path) -> None:
    missing_file = tmp_path / "no-such-path"

    with pytest.raises(FileNotFoundError, match="no-such-path"):
        load_deck_and_options(missing_file)


def test_can_load_deck_from_valid_file(file_with_empty_deck: Path) -> None:
    deck, options = load_deck_and_options(file_with_empty_deck)
    assert isinstance(deck, Deck)
    assert isinstance(options, Options)


def test_can_load_custom_options(empty_file: Path) -> None:
    empty_file.write_text(
        dedent(
            """\
            from spiel import Deck, Options

            deck = Deck(name="deck")
            options = Options(footer_time_format="foobar")
            """
        )
    )

    _, options = load_deck_and_options(empty_file)

    assert options.footer_time_format == "foobar"


def test_fails_to_load_not_deck(empty_file: Path) -> None:
    empty_file.write_text(
        dedent(
            """\
            from spiel import Deck

            deck = "not a Deck"
            """
        )
    )

    with pytest.raises(NoDeckFound):
        load_deck_and_options(empty_file)


def test_can_load_not_options(empty_file: Path) -> None:
    empty_file.write_text(
        dedent(
            """\
            from spiel import Deck

            deck = Deck(name="deck")
            options = "not an Options"
            """
        )
    )

    _, options = load_deck_and_options(empty_file)

    assert isinstance(options, Options)
