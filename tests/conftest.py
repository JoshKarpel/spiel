from functools import partial
from typing import Callable, List

import pytest
from click.testing import Result
from typer.testing import CliRunner

from spiel.main import app
from spiel.slides import Deck, Slide
from spiel.state import State

CLI = Callable[[List[str]], Result]


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def cli(runner: CliRunner) -> CLI:
    return partial(runner.invoke, app)


@pytest.fixture
def three_slide_deck() -> Deck:
    return Deck(name="three-slides", slides=[Slide(), Slide(), Slide()])


@pytest.fixture
def three_slide_state(three_slide_deck: Deck) -> State:
    return State(deck=three_slide_deck)
