import pytest
from rich.console import Console

from spiel.load import load_deck_and_options
from spiel.main import DEMO_SOURCE
from spiel.present import render_slide
from spiel.state import State


@pytest.fixture
def state() -> State:
    deck, options = load_deck_and_options(DEMO_SOURCE)
    return State(console=Console(), deck=deck, options=options)


def test_can_render_every_demo_slide(state: State) -> None:
    deck = state.deck

    for slide in deck:
        for _ in range(10):
            state.console.print(render_slide(state, slide))
            state.trigger()
        state.reset_trigger()
