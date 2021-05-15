import pytest

from spiel.main import DEMO_SOURCE
from spiel.present import render_slide
from spiel.state import State


@pytest.fixture
def state() -> State:
    return State.from_file(DEMO_SOURCE)


def test_can_render_every_demo_slide(state: State) -> None:
    deck = state.deck

    for slide in deck:
        for _ in range(10):
            state.console.print(render_slide(state, slide))
            state.trigger()
        state.reset_trigger()
