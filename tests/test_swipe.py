import pytest
from textual.widget import Widget

from spiel import Direction, Swipe, Transition


@pytest.fixture
def transition() -> Swipe:
    return Swipe()


@pytest.fixture
def from_widget() -> Widget:
    return Widget()


@pytest.fixture
def to_widget() -> Widget:
    return Widget()


@pytest.mark.parametrize(
    "direction, to_offset",
    [
        (Direction.Right, ("-0%", 0)),
    ],
)
def test_swipe_initialize(
    transition: Transition,
    from_widget: Widget,
    to_widget: Widget,
    direction: Direction,
    to_offset: tuple[object, object],
) -> None:
    transition.initialize(from_widget=from_widget, to_widget=to_widget, direction=direction)

    assert to_widget.styles.offset == to_offset


@pytest.mark.parametrize(
    "progress, direction, from_offset, to_offset",
    [
        (0, Direction.Right, ("-0%", 0), ("100%", 0)),
    ],
)
def test_swipe_progress(
    transition: Transition,
    from_widget: Widget,
    to_widget: Widget,
    progress: float,
    direction: Direction,
    from_offset: tuple[object, object],
    to_offset: tuple[object, object],
) -> None:
    transition.initialize(from_widget=from_widget, to_widget=to_widget, direction=direction)

    transition.progress(
        from_widget=from_widget,
        to_widget=to_widget,
        direction=direction,
        progress=progress,
    )

    assert (from_widget.styles.offset, to_widget.styles.offset) == (from_offset, to_offset)
