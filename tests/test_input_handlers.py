import pytest

from spiel.exceptions import DuplicateInputHandler
from spiel.input import InputHandlers, action
from spiel.state import State


@pytest.fixture
def handlers() -> InputHandlers:
    return {}  # type: ignore


def test_register_already_registered_raises_error(handlers: InputHandlers) -> None:
    @action("a")
    def a(state: State) -> None:  # pragma: never runs
        pass

    with pytest.raises(DuplicateInputHandler):

        @action("a")
        def a(state: State) -> None:  # pragma: never runs
            pass
