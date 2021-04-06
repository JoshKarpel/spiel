from io import StringIO

import pytest
from pytest_mock import MockFixture
from rich.console import Console

from spiel.exceptions import DuplicateInputHandler
from spiel.input import (
    SPECIAL_CHARACTERS,
    InputHandlers,
    SpecialCharacters,
    get_character,
    handle_input,
    input_handler,
)
from spiel.modes import Mode
from spiel.state import State


@pytest.fixture
def handlers() -> InputHandlers:
    return {}  # type: ignore


def test_register_already_registered_raises_error(handlers: InputHandlers) -> None:
    @input_handler("a", help="")
    def a(state: State) -> None:  # pragma: never runs
        pass

    with pytest.raises(DuplicateInputHandler):

        @input_handler("a", help="")
        def a(state: State) -> None:  # pragma: never runs
            pass


@pytest.mark.parametrize("input, expected", SPECIAL_CHARACTERS.items())
def test_get_character_recognizes_special_characters(
    input: str, expected: SpecialCharacters
) -> None:
    io = StringIO(input)

    assert get_character(io) == expected


def test_handle_input_calls_matching_handler_and_returns_its_return_value(
    console: Console, three_slide_state: State, mocker: MockFixture
) -> None:
    mock = mocker.MagicMock(return_value="foobar")

    result = handle_input(
        state=three_slide_state,
        stream=StringIO("a"),
        handlers={("a", three_slide_state.mode): mock},
    )

    assert mock.called
    assert result == "foobar"


def test_handle_input_returns_none_for_missed_input_based_on_character(
    console: Console, three_slide_state: State, mocker: MockFixture
) -> None:
    mock = mocker.MagicMock(return_value="foobar")

    result = handle_input(
        state=three_slide_state,
        stream=StringIO("a"),
        handlers={("b", three_slide_state.mode): mock},
    )

    assert result is None


def test_handle_input_returns_none_for_missed_input_based_on_mode(
    console: Console, three_slide_state: State, mocker: MockFixture
) -> None:
    mock = mocker.MagicMock(return_value="foobar")
    three_slide_state.mode = Mode.SLIDE

    result = handle_input(
        state=three_slide_state,
        stream=StringIO("a"),
        handlers={("a", Mode.HELP): mock},
    )

    assert result is None
