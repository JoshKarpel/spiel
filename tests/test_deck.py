from hypothesis import HealthCheck, given, settings
from hypothesis.strategies import slices

from spiel import Deck, Slide


def test_can_add_slide_to_deck(three_slide_deck: Deck) -> None:
    initial_len = len(three_slide_deck)
    new_slide = Slide()

    three_slide_deck.add_slides(new_slide)

    assert len(three_slide_deck) == initial_len + 1
    assert three_slide_deck[-1] is new_slide


def test_iterate_yields_deck_slides(three_slide_deck: Deck) -> None:
    assert list(iter(three_slide_deck)) == three_slide_deck._slides


def test_deck_contains_its_slides(three_slide_deck: Deck) -> None:
    for slide in three_slide_deck:
        assert slide in three_slide_deck


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(s=slices(size=3))
def test_index_with_slice(three_slide_deck: Deck, s: slice) -> None:
    assert three_slide_deck[s] == three_slide_deck._slides[s]
