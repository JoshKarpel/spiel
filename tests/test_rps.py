import pytest

from spiel.rps import RPSCounter


@pytest.fixture
def counter() -> RPSCounter:
    return RPSCounter()


def test_internals(counter: RPSCounter) -> None:
    # 3 renders in 4 seconds
    counter.render_time_history.extend([1, 2, 5])

    assert counter.renders_per_second() == 3 / 4


def test_not_enough_samples(counter: RPSCounter) -> None:
    counter.render_time_history.extend([1])

    # 1 sample isn't enough

    assert counter.renders_per_second() == 0


def test_custom_length() -> None:
    assert RPSCounter(render_history_length=5).render_time_history.maxlen == 5
