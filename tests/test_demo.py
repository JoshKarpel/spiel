import pytest
from rich.console import Console

from spiel import Deck, Options
from spiel.load import load_deck
from spiel.main import DEMO_SOURCE
from spiel.present import render_slide
from spiel.state import State


@pytest.fixture
def demo_deck() -> Deck:
    return load_deck(DEMO_SOURCE)


@pytest.fixture
def demo_state(demo_deck: Deck) -> State:
    return State(deck=demo_deck, console=Console(), options=Options())


def test_can_render_every_demo_slide(demo_state: State, demo_deck: Deck) -> None:
    for slide in demo_deck:
        for _ in range(10):
            demo_state.console.print(render_slide(demo_state, slide))
            demo_state.trigger()
        demo_state.reset_trigger()
