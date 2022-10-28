from pathlib import Path
from textwrap import dedent

import pytest

from spiel import Deck
from spiel.app import load_deck
from spiel.constants import DECK
from spiel.exceptions import NoDeckFound


def test_loading_from_empty_file_fails(empty_file: Path) -> None:
    with pytest.raises(NoDeckFound, match=DECK):
        load_deck(empty_file)


def test_loading_from_missing_file_fails(tmp_path: Path) -> None:
    missing_file = tmp_path / "no-such-path"

    with pytest.raises(FileNotFoundError, match="no-such-path"):
        load_deck(missing_file)


def test_can_load_deck_from_valid_file(file_with_empty_deck: Path) -> None:
    deck = load_deck(file_with_empty_deck)
    assert isinstance(deck, Deck)


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
        load_deck(empty_file)
