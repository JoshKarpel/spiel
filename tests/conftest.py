from functools import partial
from typing import Callable, List

import pytest
from click.testing import Result
from typer.testing import CliRunner

from spiel.main import app

CLI = Callable[[List[str]], Result]


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def cli(runner: CliRunner) -> CLI:
    return partial(runner.invoke, app)
