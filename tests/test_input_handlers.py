import os
import string
from random import sample
from typing import List

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from rich.console import Console
from rich.text import Text
from typer import Exit

from spiel import Deck, Options, Slide
from spiel.input import (
    INPUT_HANDLERS,
    InputHandler,
    deck_mode,
    edit_example,
    edit_options,
    exit,
    jump_to_slide,
    next_slide,
    open_repl,
    previous_slide,
    slide_mode,
)
from spiel.modes import Mode
from spiel.state import State


def test_next_slide_goes_to_next_slide(three_slide_state: State) -> None:
    next_slide(three_slide_state)

    assert three_slide_state.current_slide is three_slide_state.deck[1]


def test_previous_slide_goes_to_previous_slide(three_slide_state: State) -> None:
    three_slide_state.jump_to_slide(2)

    previous_slide(three_slide_state)

    assert three_slide_state.current_slide is three_slide_state.deck[1]


def test_enter_deck_mode(three_slide_state: State) -> None:
    deck_mode(three_slide_state)

    assert three_slide_state.mode is Mode.DECK


def test_enter_slide_mode(three_slide_state: State) -> None:
    slide_mode(three_slide_state)

    assert three_slide_state.mode is Mode.SLIDE


def test_kill(three_slide_state: State) -> None:
    with pytest.raises(Exit):
        exit(three_slide_state)


TESTABLE_INPUT_HANDLERS = list(
    set(INPUT_HANDLERS.values()).difference(
        {
            exit,
            jump_to_slide,
            open_repl,
            edit_options,
            edit_example,
        }
    )
)


@given(input_handlers=st.lists(st.sampled_from(TESTABLE_INPUT_HANDLERS)))
@settings(max_examples=2_000 if os.getenv("CI") else 200)
def test_input_sequences_dont_crash(input_handlers: List[InputHandler]) -> None:
    state = State(
        console=Console(),
        deck=Deck(
            name="deck",
            slides=[
                Slide(
                    content=Text(f"This is slide {n + 1}"),
                    title="".join(sample(string.ascii_letters, 30)),
                )
                for n in range(30)
            ],
        ),
        options=Options(),
    )

    for input_handler in input_handlers:
        input_handler(state)
