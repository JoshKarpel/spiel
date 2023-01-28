import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis.strategies import floats
from textual.css.scalar import Scalar, ScalarOffset, Unit
from textual.widget import Widget

from spiel import Direction, Swipe, Transition


@pytest.fixture
def transition() -> Swipe:
    return Swipe()


Y = Scalar.parse("0", percent_unit=Unit.HEIGHT)


@pytest.mark.parametrize(
    "direction, to_offset",
    [
        (Direction.Right, ScalarOffset(Scalar.parse("100%"), Y)),
    ],
)
def test_swipe_initialize(
    from_widget: Widget,
    to_widget: Widget,
    direction: Direction,
    to_offset: tuple[object, object],
) -> None:
    Swipe().initialize(from_widget=from_widget, to_widget=to_widget, direction=direction)

    assert to_widget.styles.offset == to_offset


@pytest.mark.parametrize(
    "progress, direction, from_offset, to_offset",
    [
        (
            0,
            Direction.Right,
            ScalarOffset(Scalar.parse("-0%"), Y),
            ScalarOffset(Scalar.parse("100%"), Y),
        ),
        (
            25,
            Direction.Right,
            ScalarOffset(Scalar.parse("-25%"), Y),
            ScalarOffset(Scalar.parse("75%"), Y),
        ),
        (
            50,
            Direction.Right,
            ScalarOffset(Scalar.parse("-50%"), Y),
            ScalarOffset(Scalar.parse("50%"), Y),
        ),
        (
            75,
            Direction.Right,
            ScalarOffset(Scalar.parse("-75%"), Y),
            ScalarOffset(Scalar.parse("25%"), Y),
        ),
        (
            75.123,
            Direction.Right,
            ScalarOffset(Scalar.parse("-75.12%"), Y),
            ScalarOffset(Scalar.parse("24.88%"), Y),
        ),
        (
            75.126,
            Direction.Right,
            ScalarOffset(Scalar.parse("-75.13%"), Y),
            ScalarOffset(Scalar.parse("24.87%"), Y),
        ),
        (
            100,
            Direction.Right,
            ScalarOffset(Scalar.parse("-100%"), Y),
            ScalarOffset(Scalar.parse("0%"), Y),
        ),
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

    assert from_widget.styles.offset == from_offset
    assert to_widget.styles.offset == to_offset


@given(progress=floats(min_value=0, max_value=100))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_swipe_progress_always_balances_for_right(
    transition: Transition,
    from_widget: Widget,
    to_widget: Widget,
    progress: float,
) -> None:
    transition.initialize(from_widget=from_widget, to_widget=to_widget, direction=Direction.Right)

    transition.progress(
        from_widget=from_widget,
        to_widget=to_widget,
        direction=Direction.Right,
        progress=progress,
    )

    assert abs(from_widget.styles.offset.x.value) + to_widget.styles.offset.x.value == 100
