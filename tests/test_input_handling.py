import pytest

from spiel.exceptions import DuplicateInputHandler
from spiel.input import InputHandlers, input_handler
from spiel.state import State


@pytest.fixture
def handlers() -> InputHandlers:
    return {}  # type: ignore


def test_register_already_registered_raises_error(handlers: InputHandlers) -> None:
    @input_handler("a")
    def a(state: State) -> None:  # pragma: never runs
        pass

    with pytest.raises(DuplicateInputHandler):

        @input_handler("a")
        def a(state: State) -> None:  # pragma: never runs
            pass
