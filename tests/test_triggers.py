import pytest
from hypothesis import given
from hypothesis.strategies import slices

from spiel import Triggers


@pytest.mark.parametrize(
    "triggers, expected",
    [
        (Triggers(_times=(0,), now=0), 1),
        (Triggers(_times=(0, 1), now=1), 2),
        (Triggers(_times=(0, 1, 2), now=2), 3),
    ],
)
def test_length(triggers: Triggers, expected: int) -> None:
    assert len(triggers) == expected


@pytest.mark.parametrize(
    "triggers, idx, expected",
    [
        (Triggers(_times=(0, 1), now=1), 0, 0),
        (Triggers(_times=(0, 1), now=1), 1, 1),
        (Triggers(_times=(0, 1, 2), now=2), -1, 2),
    ],
)
def test_getitem(triggers: Triggers, idx: int, expected: int) -> None:
    assert triggers[idx] == expected


@given(s=slices(size=3))
def test_index_with_slice(s: slice) -> None:
    triggers = Triggers(_times=(0, 1, 2), now=2)
    assert triggers[s] == triggers._times[s]


@pytest.mark.parametrize(
    "triggers",
    [
        Triggers(_times=(0,), now=0),
        Triggers(_times=(0, 1), now=1),
        Triggers(_times=(0, 1, 2), now=2),
    ],
)
def test_iter(triggers: Triggers) -> None:
    assert tuple(iter(triggers)) == triggers._times


@pytest.mark.parametrize(
    "triggers, expected",
    [
        (Triggers(_times=(0, 1), now=5), 4),
        (Triggers(_times=(0, 1), now=1), 0),
        (Triggers(_times=(0, 1, 2), now=3), 1),
    ],
)
def test_time_since_last_trigger(triggers: Triggers, expected: float) -> None:
    assert triggers.time_since_last_trigger == expected


@pytest.mark.parametrize(
    "triggers, expected",
    [
        (Triggers(_times=(0, 1), now=5), 5),
        (Triggers(_times=(0, 1), now=1), 1),
        (Triggers(_times=(0, 1, 2), now=3), 3),
        (Triggers(_times=(3, 2), now=4), 1),
    ],
)
def test_time_since_first_trigger(triggers: Triggers, expected: float) -> None:
    assert triggers.time_since_first_trigger == expected


@pytest.mark.parametrize(
    "triggers, expected",
    [
        (Triggers(_times=(0,), now=0), False),
        (Triggers(_times=(0, 1), now=1), True),
    ],
)
def test_triggered(triggers: Triggers, expected: bool) -> None:
    assert triggers.triggered is expected


@pytest.mark.parametrize(
    "times, now",
    [
        ((), 0),  # no times
        ((0,), -1),  # now before last time
        ((5,), 4),  # now before last time
    ],
)
def test_invalid_triggers(times: tuple[float], now: float) -> None:
    with pytest.raises(ValueError):
        Triggers(_times=times, now=now)
