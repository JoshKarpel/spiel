from spiel.state import State


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
