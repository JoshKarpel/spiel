from collections.abc import Callable
from io import StringIO

import pytest
from rich.console import Console
from rich.layout import Layout
from rich.text import Text

from spiel import Slide
from spiel.present import render_slide, split_layout_into_deck_grid
from spiel.state import State


@pytest.mark.parametrize(
    "make_slide",
    [
        lambda: Slide(content=Text("foobar")),
        lambda: Slide(content=lambda: Text("foobar")),
        lambda: Slide(content=lambda triggers: Text("foobar")),
    ],
)
def test_can_render_slide(
    make_slide: Callable[[], Slide],
    console: Console,
    output: StringIO,
    three_slide_state: State,
) -> None:
    renderable = render_slide(state=three_slide_state, slide=make_slide())

    console.print(renderable)

    result = output.getvalue()

    assert "foobar" in result


def test_can_render_deck_grid(three_slide_state: State) -> None:
    root = Layout()
    split_layout_into_deck_grid(root, three_slide_state)
