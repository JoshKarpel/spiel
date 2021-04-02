from typing import Text

import pytest
from rich.console import Console

from spiel import Deck
from spiel.state import State, TextLike


def test_initial_state_has_first_slide_current(three_slide_state: State) -> None:
    assert three_slide_state.current_slide is three_slide_state.deck[0]


def test_next_from_first_to_second(three_slide_state: State) -> None:
    three_slide_state.next_slide()
    assert three_slide_state.current_slide is three_slide_state.deck[1]


def test_next_from_first_to_third(three_slide_state: State) -> None:
    three_slide_state.next_slide(move=2)
    assert three_slide_state.current_slide is three_slide_state.deck[2]


def test_jump_to_third_slide(three_slide_state: State) -> None:
    three_slide_state.jump_to_slide(2)
    assert three_slide_state.current_slide is three_slide_state.deck[2]


def test_jump_before_beginning_results_in_beginning(three_slide_state: State) -> None:
    three_slide_state.jump_to_slide(-5)
    assert three_slide_state.current_slide is three_slide_state.deck[0]


def test_jump_past_end_results_in_end(three_slide_state: State) -> None:
    three_slide_state.jump_to_slide(len(three_slide_state.deck) + 5)
    assert three_slide_state.current_slide is three_slide_state.deck[-1]


def test_next_from_last_slide_stays_put(three_slide_state: State) -> None:
    three_slide_state.jump_to_slide(2)

    three_slide_state.next_slide()
    assert three_slide_state.current_slide is three_slide_state.deck[2]


def test_previous_from_first_slide_stays_put(three_slide_state: State) -> None:
    three_slide_state.previous_slide()

    assert three_slide_state.current_slide is three_slide_state.deck[0]


@pytest.mark.parametrize(
    "width, expected",
    [
        (20, 1),
        (30, 1),
        (40, 1),
        (60, 2),
        (80, 2),
        (95, 3),
        (120, 4),
    ],
)
def test_deck_grid_width(width: int, expected: int, three_slide_deck: Deck) -> None:
    console = Console(width=width)
    state = State(console=console, deck=three_slide_deck)

    assert state.deck_grid_width == expected


@pytest.mark.parametrize(
    "message, expected",
    [
        (Text("foobar"), Text("foobar")),
        (lambda: Text("wizbang"), Text("wizbang")),
    ],
)
def test_set_message(message: TextLike, expected: Text, three_slide_state: State) -> None:
    three_slide_state.set_message(message)

    assert three_slide_state.message == expected
