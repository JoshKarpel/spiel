from spiel.input import deck_mode, next_slide, previous_slide, slide_mode
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
