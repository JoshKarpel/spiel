from typing import Any

import pytest
from _pytest.tmpdir import TempPathFactory
from hypothesis import given, infer
from hypothesis import strategies as st
from hypothesis.strategies import SearchStrategy
from rich.console import Console

from spiel import Options
from spiel.exceptions import InvalidOptionValue
from spiel.repls import REPLS


def valid_options() -> SearchStrategy[Options]:
    return st.builds(
        Options,
        profiling=infer,
        repl=st.sampled_from(list(REPLS.keys())),
    )


@given(o=valid_options())
def test_round_trip_to_dict(o: Options) -> None:
    assert o == Options.from_dict(o.as_dict())


@given(o=valid_options())
def test_round_trip_to_toml(o: Options) -> None:
    assert o == Options.from_toml(o.as_toml())


@given(o=valid_options())
def test_round_trip_to_file(o: Options, tmp_path_factory: TempPathFactory) -> None:
    dir = tmp_path_factory.mktemp(basename="options-roundtrip")
    path = dir / "options.toml"

    assert o == Options.load(o.save(path))


def test_can_render_options(console: Console, three_slide_options: Options) -> None:
    console.print(three_slide_options)


@pytest.mark.parametrize(
    "key, value",
    [
        ("repl", "foobar"),
    ],
)
def test_reject_invalid_option_values(key: str, value: Any) -> None:
    with pytest.raises(InvalidOptionValue):
        Options(**{key: value})
