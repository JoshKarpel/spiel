from _pytest.tmpdir import TempPathFactory
from hypothesis import given
from hypothesis import strategies as st
from rich.console import Console

from spiel import Options


@given(o=st.builds(Options))
def test_round_trip_to_dict(o: Options) -> None:
    assert o == Options.from_dict(o.as_dict())


@given(o=st.builds(Options))
def test_round_trip_to_toml(o: Options) -> None:
    assert o == Options.from_toml(o.as_toml())


@given(o=st.builds(Options))
def test_round_trip_to_file(o: Options, tmp_path_factory: TempPathFactory) -> None:
    dir = tmp_path_factory.mktemp(basename="options-roundtrip")
    path = dir / "options.toml"

    assert o == Options.load(o.save(path))


def test_can_render_options(console: Console, three_slide_options: Options) -> None:
    console.print(three_slide_options)
