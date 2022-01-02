import pytest

from spiel import Deck
from spiel.deck import get_function_body
from spiel.slide import Slide


def test_can_add_slide_to_deck(three_slide_deck: Deck) -> None:
    initial_len = len(three_slide_deck)
    new_slide = Slide()

    three_slide_deck.add_slides(new_slide)

    assert len(three_slide_deck) == initial_len + 1
    assert three_slide_deck[-1] is new_slide


def test_iterate_yields_deck_slides(three_slide_deck: Deck) -> None:
    assert list(iter(three_slide_deck)) == three_slide_deck.slides


def test_deck_contains_its_slides(three_slide_deck: Deck) -> None:
    for slide in three_slide_deck:
        assert slide in three_slide_deck


def test_get_function_body() -> None:
    def foo() -> None:  # pragma: never runs
        ...

    assert get_function_body(foo) == "...\n"


def test_get_function_body_raises_on_function_with_no_source() -> None:
    with pytest.raises(TypeError):
        get_function_body(str)  # type: ignore
