import pytest

from spiel import Deck
from spiel.app import load_deck
from spiel.constants import DEMO_FILE


@pytest.fixture
def deck() -> Deck:
    return load_deck(DEMO_FILE)


def test_can_render_every_demo_slide(deck: Deck) -> None:
    for slide in deck:
        slide.content()
