import pytest

from spiel import Triggers


@pytest.mark.parametrize(
    "triggers, expected",
    [
        (Triggers(()), 0),
        (Triggers((0, 1)), 2),
        (Triggers((0, 1, 2)), 3),
    ],
)
def test_length(triggers: Triggers, expected: int) -> None:
    assert len(triggers) == expected


@pytest.mark.parametrize(
    "triggers, idx, expected",
    [
        (Triggers((0, 1)), 0, 0),
        (Triggers((0, 1)), 1, 1),
        (Triggers((0, 1, 2)), -1, 2),
    ],
)
def test_getitem(triggers: Triggers, idx: int, expected: int) -> None:
    assert triggers[idx] == expected


@pytest.mark.parametrize(
    "triggers",
    [
        Triggers(()),
        Triggers((0, 1)),
        Triggers((0, 1, 2)),
    ],
)
def test_iter(triggers: Triggers) -> None:
    assert tuple(iter(triggers)) == triggers.times


@pytest.mark.parametrize(
    "triggers, expected",
    [
        (Triggers((0, 1), now=5), 4),
        (Triggers((0, 1), now=1), 0),
        (Triggers((0, 1, 2), now=3), 1),
    ],
)
def test_time_since_last_trigger(triggers: Triggers, expected: float) -> None:
    assert triggers.time_since_last_trigger == expected


@pytest.mark.parametrize(
    "triggers, expected",
    [
        (Triggers((0, 1), now=5), 5),
        (Triggers((0, 1), now=1), 1),
        (Triggers((0, 1, 2), now=3), 3),
        (Triggers((3, 2), now=4), 1),
    ],
)
def test_time_since_first_trigger(triggers: Triggers, expected: float) -> None:
    assert triggers.time_since_first_trigger == expected
